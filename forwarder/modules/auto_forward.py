import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram.errors import FloodWait
from config import Config
from translation import Translation

from forwarder import FROM_CHATS, LOGGER, SKIP_NO, LIMIT, TO_CHATS, FILTER_TYPE, dispatcher


from typing import Union

from telegram import Message, MessageId
from telegram.ext import CallbackContext, Filters, MessageHandler
from telegram.error import ChatMigrated
from telegram.update import Update

FILTER = Config.FILTER_TYPE
FROM = Config.FROM_CHATS
TO = Config.TO_CHATS

def send_message(message: Message, chat_id: int) -> Union[MessageId, Message]:
    if REMOVE_TAG:
        return message.copy(chat_id)
    return message.forward(chat_id)



def forward(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    if not message or not chat:
        return
    from_chat_name = chat.title or chat.first_name

    for chat in TO_CHATS:
        to_chat_name = (
            context.bot.get_chat(chat).title or context.bot.get_chat(chat).first_name
        )
        try:
            send_message(message, chat)
        except ChatMigrated as err:
            send_message(message, err.new_chat_id)
            LOGGER.warning(f"Chat {chat} has been migrated to {err.new_chat_id}!! Edit the config file!!")
        except:
            LOGGER.exception(
                'Error while forwarding message from chat "{}" to chat "{}".'.format(
                    from_chat_name, to_chat_name
                )
            )


try:
    FORWARD_HANDLER = MessageHandler(
        Filters.chat(FROM_CHATS) & ~Filters.status_update & ~Filters.command,
        forward,
        run_async=True,
    )



@Client.on_message(filters.private & filters.command("run"))
async def run(bot, message):
    if str(message.from_user.id) not in Config.OWNER_ID:
        return
    buttons = [[
        InlineKeyboardButton('🚫 STOP', callback_data='stop_btn')
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    m = await bot.send_message(
        text="<b>File Forwording Started😉</b>",
        reply_markup=reply_markup,
        chat_id=message.chat.id
    )

    files_count = 0
    async for message in bot.USER.search_messages(chat_id=FROM,offset=Config.SKIP_NO,limit=Config.LIMIT,filter=FILTER):
        try:
            if message.video:
                file_name = message.video.file_name
            elif message.document:
                file_name = message.document.file_name
            elif message.audio:
                file_name = message.audio.file_name
            else:
                file_name = None
            await bot.copy_message(
                chat_id=TO,
                from_chat_id=FROM,
                parse_mode="md",       
                caption=Translation.CAPTION.format(file_name),
                message_id=message.message_id
            )
            files_count += 1
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(e.x)
            await bot.copy_message(
                chat_id=TO,
                from_chat_id=FROM,
                parse_mode="md",       
                caption=Translation.CAPTION.format(file_name),
                message_id=message.message_id
            )
            files_count += 1
            await asyncio.sleep(1)
        except Exception as e:
            print(e)
            pass
   # await m.delete()
    buttons = [[
        InlineKeyboardButton('📜 Support', url='https://t.me/inbliz')
    ]] 
    reply_markup = InlineKeyboardMarkup(buttons)
    await m.edit(
        text=f"<u><b>Successfully Forwarded</b></u>\n\n<b>Total Forwarded Files:-</b> <code>{files_count}</code> <b>Files</b>\n<b>Thanks For Using Me❤️</b>",
        reply_markup=reply_markup
    )

    dispatcher.add_handler(FORWARD_HANDLER)

except ValueError:  # When FROM_CHATS list is not set because user doesn't know chat id(s)
    LOGGER.warn("I can't FORWARD_HANDLER because your FROM_CHATS list is empty.")
