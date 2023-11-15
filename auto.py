import asyncio
import random
from telethon.sync import TelegramClient, events

api_id = '28647716'
api_hash = 'a09b61a894a34a9564b5d070f292b4a9'
phone_number = '+919198291748'
file_path = 'data.txt'
group_usernames = ['alterchkbot']

client = TelegramClient('session_name', api_id, api_hash)

# Flags to control sending
send_cards_flag = True

# Function to read data from the text file
def read_data():
    with open(file_path, 'r') as file:
        data = file.readlines()
        # Extracting BIN, expiry month, and expiry year from the file
        bin_val = data[0].split('=')[1].strip()
        exp_m_val = data[1].split('=')[1].strip()
        exp_y_val = data[2].split('=')[1].strip()
    return bin_val, exp_m_val, exp_y_val

# Function to update data in the text file
async def update_data(bin_val, exp_m_val, exp_y_val, cvv_val):
    data = f"bin = {bin_val}\nexpm = {exp_m_val}\nexpy = {exp_y_val}\ncvv = {cvv_val}"
    with open(file_path, 'w') as file:
        file.write(data)

# Function to generate a card with provided BIN, expiry month, and expiry year, and random CVV
def gen_card(bin, exp_m, exp_y):
    cvv = str(random.randint(0, 999)).zfill(3)
    card_number = bin
    for _ in range(15 - len(bin)):
        digit = random.randint(0, 9)
        card_number += str(digit)
    digits = [int(x) for x in card_number]
    for i in range(0, 16, 2):
        digits[i] *= 2
        if digits[i] > 9:
            digits[i] -= 9
    total = sum(digits)
    check_digit = (10 - (total % 10)) % 10
    card_number += str(check_digit)

    return f".es {card_number}|{exp_m}|{exp_y}|{cvv}"

async def send_message(client, group_username, card_info):
    await client.send_message(group_username, card_info)

async def send_cards():
    global send_cards_flag
    while True:
        if send_cards_flag:
            bin_val, exp_m_val, exp_y_val = read_data()
            card_info = gen_card(bin_val, exp_m_val, exp_y_val)
            for group_username in group_usernames:
                await send_message(client, group_username, card_info)
        await asyncio.sleep(37)

@client.on(events.NewMessage(pattern=r'/update'))
async def handle_update(event):
    try:
        message = event.message.text
        command, data = message.split(maxsplit=1)
        bin_val, exp_m_val, exp_y_val, cvv_val = data.split()

        await update_data(bin_val, exp_m_val, exp_y_val, cvv_val)
        await event.respond('Data updated successfully!')
    except ValueError:
        await event.respond('Invalid command format. Use "/update <bin> <expm> <expy> <cvv>"')

@client.on(events.NewMessage(pattern=r'/start'))
async def handle_start(event):
    global send_cards_flag
    send_cards_flag = True
    await event.respond('Sending of credit card information started!')

@client.on(events.NewMessage(pattern=r'/stop'))
async def handle_stop(event):
    global send_cards_flag
    send_cards_flag = False
    await event.respond('Sending of credit card information stopped!')

# Start the client and tasks
client.start()
client.loop.create_task(send_cards())
client.run_until_disconnected()
