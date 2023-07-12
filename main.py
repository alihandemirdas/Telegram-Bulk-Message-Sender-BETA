import asyncio
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import SendMessageRequest
import telethon.tl.functions as _fn
import re
from telethon import functions, types

api_id = ''
api_hash = ''
phone_number = ''

message = """Mesajınız"""
groups = []
group_ids = []

def get_username(string):
    match = re.search(r"username='(.+)'", string)
    if match:
        return match.group(1)
    else:
        return None

async def bot():
    async with TelegramClient('session_name', api_id, api_hash) as client:
        print("geldi")
        await client.connect()
        print("geçti")
        if not await client.is_user_authorized():
            await client.send_code_request(phone_number)
            await client.sign_in(phone_number, input('Enter the code: '))
        
        # #Txt dosyasındaki grupların usernamelerini listeye ekler
        # with open("groups.txt","r",encoding="utf-8") as dosya:
        #     for satir in dosya.readlines():
        #         groups.append(satir)

        # #Listedeki gruplara 60 saniye aralıklarla katılır
        # for group in groups:
        #     result = client(functions.channels.JoinChannelRequest(
        #         channel=group
        #     ))
        #     time.sleep(60)
     
        async for dialog in client.iter_dialogs():
            if dialog.is_group:
                group_ids.append(dialog.id)
                # #Katılmış olduğumuz grupların kullanıcı adlarını çeker ve listeye atar
                # en = dialog.entity
                # username = get_username(str(en))
                # groups.append(username)
        
        while True:
            for group_id in group_ids:
                await client(SendMessageRequest(
                    peer=group_id,
                    message=message
                ))
            await asyncio.sleep(300)


asyncio.run(bot())
