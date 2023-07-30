import asyncio, json
from pyrogram import Client
class tgSendMessage:
    def __init__(self, app_id, app_hash, session, message, channel, uid):
        self.session = session
        self.message = message
        self.channel = channel
        self.app_id = app_id
        self.app_hash = app_hash
        self.uid = uid
        with open('unique.json', 'r', encoding='utf-8') as f:
            self.jsonUid = json.load(f)
    async def sendMessage(self):
        async with Client(self.session, self.app_id, self.app_hash) as app:
            await app.join_chat(self.channel)
            if self.uid in self.jsonUid:
                await app.send_message(chat_id=self.channel, text=self.message, reply_to_message_id=self.jsonUid[self.uid])
                del self.jsonUid[self.uid]
                with open('unique.json', 'w', encoding='utf-8') as f:
                    json.dump(self.jsonUid, f)
            else:
                last = await app.send_message(chat_id=self.channel, text=self.message)
                self.jsonUid[self.uid] = last.id
                with open('unique.json', 'w', encoding='utf-8') as f:
                    json.dump(self.jsonUid, f)
    def send(self):
        asyncio.run(self.sendMessage())

#Usage:
# tgSendMessage(app_id="14384400", app_hash="3c0f0e18a32e4de6aa5746439bdef7f5", session="sessions/905415520697", message="asdas", channel="testingTgGrup", uid="1231").send()