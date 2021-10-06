import asyncio

from pyrogram.errors import FloodWait, UserIsBlocked, PeerIdInvalid, InputUserDeactivated
from LaylaRobot import pbot, filters
from pyrogram.types import Message
from LaylaRobot.modules.sql.broadcast_db import add_to_broadcastbase, full_broadcastbase, present_in_broadcastbase, del_from_broadcastbase

@pbot.on_message(group=1)
async def add_to_db(bot:pbot,message:Message):
    chat_id = message.chat.id
    if not present_in_broadcastbase(chat_id):
        add_to_broadcastbase(chat_id)

@pbot.on_message(filters.command('broadcast') & filters.badmins)
async def pyro_broadcast(bot:pbot,message:Message):
    reply_message = message.reply_to_message
    if reply_message:
        chats = full_broadcastbase()
        success = 0
        for chat in chats:
            if reply_message.poll:
                try:
                    await reply_message.forward(int(chat.chat_id))
                    success += 1
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await reply_message.forward(int(chat.chat_id))
                    print(f"Broadcast send to {chat.chat_id}")
                    success += 1
                except UserIsBlocked:
                    print(f"Broadcast failed to {chat.chat_id} (Blocked)")
                except PeerIdInvalid:
                    print(f"Broadcast failed to {chat.chat_id} (PeerId)")
                except InputUserDeactivated:
                    print(f"Broadcast failed to {chat.chat_id} (Deactivated)")
                    del_from_broadcastbase(chat.chat_id)
                except Exception as e:
                    print(f"Broadcast failed to {chat.chat_id} ({e})")
                try:
                    failed = len(chats) - success
                    await message.reply("Broadcast send Successfully")
                    await message.reply(
                        f"<b>Statistics :</b>\n\n\n👥Total users : {len(chats)}\n\n✅Successfull : {success}\n\n❌Failed : {failed}")
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await message.reply("Broadcast send Successfully")
                    await message.reply(
                        f"<b>Statistics :</b>\n\n\n👥Total users : {len(chats)}\n\n✅Successfull : {success}\n\n❌Failed : {failed}")
            else:
                try:
                    await reply_message.copy(int(chat.chat_id))
                    success += 1
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await reply_message.copy(int(chat.chat_id))
                    print(f"Broadcast send to {chat.chat_id}")
                    success += 1
                except UserIsBlocked:
                    print(f"Broadcast failed to {chat.chat_id} (Blocked)")
                except PeerIdInvalid:
                    print(f"Broadcast failed to {chat.chat_id} (PeerId)")
                except InputUserDeactivated:
                    print(f"Broadcast failed to {chat.chat_id} (Deactivated)")
                    del_from_broadcastbase(chat.chat_id)
                except Exception as e:
                    print(f"Broadcast failed to {chat.chat_id} ({e})")
                try:
                    failed = len(chats) - success
                    await message.reply("Broadcast send Successfully")
                    await message.reply(
                        f"<b>Statistics :</b>\n\n\n👥Total users : {len(chats)}\n\n✅Successfull : {success}\n\n❌Failed : {failed}")
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await message.reply("Broadcast send Successfully")
                    await message.reply(
                        f"<b>Statistics :</b>\n\n\n👥Total users : {len(chats)}\n\n✅Successfull : {success}\n\n❌Failed : {failed}")


