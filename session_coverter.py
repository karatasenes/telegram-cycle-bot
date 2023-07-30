import asyncio, json, pathlib
from pyrogram import Client
filepath = str(pathlib.Path(__file__).parent.absolute())
class SessionMaker:
    def __init__(self, number):
        self.number = number
        with open('config.json', 'r', encoding='utf-8') as f:
            con = json.load(f)
            self.app_id = con['app_id']
            self.app_hash = con['app_hash']
    async def craetor(self):
        async with Client(f"{self.number}", api_id=self.app_id, api_hash=self.app_hash, phone_number=self.number) as app:
            await app.send_message("me", "Sample message..")
            print("Session has been created!")
    
    def start(self):
        asyncio.run(self.craetor())
