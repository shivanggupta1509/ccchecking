import asyncio
import re
import random
import datetime
from os import system
from telethon.sync import TelegramClient

# Function to generate a card with fixed BIN, expiry month, and expiry year, and random CVV
def gen_card(bin, exp_m, exp_y, cvv):
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

    # Fixed expiry month and year
    exp_m = "07"
    exp_y = "2025"
    # CVV
    if cvv == "":
        cvv = str(random.randint(0, 999)).zfill(3)
    else:
        cvv = cvv.zfill(3)

    return f".es {card_number}|{exp_m}|{exp_y}|{cvv}"

async def send_message(client, group_username, card_info):
    await client.send_message(group_username, card_info)

async def main():
    api_id = '28647716'
    api_hash = 'a09b61a894a34a9564b5d070f292b4a9'
    phone_number = '+919198291748'
    group_usernames = ['alterchkbot']
    fixed_bin = "54255045019"

    async with TelegramClient(phone_number, api_id, api_hash) as client:
        while True:
            for group_username in group_usernames:
                card_info = gen_card(fixed_bin, "", "", "")
                await send_message(client, group_username, card_info)
            await asyncio.sleep(37)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
