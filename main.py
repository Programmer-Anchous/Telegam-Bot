import logging

from PIL import Image

from io import BytesIO

from requests import get

from telegram.ext import Application, filters
from telegram.ext import CommandHandler, MessageHandler
from config import BOT_TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        f"Hi! I can put effects on your photo.",
    )


async def answer(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def handle_photo(update, context):
    photo = await update.message.effective_attachment[-1].get_file()
    url = photo.file_path
    response = get(url)
    bytes_obj = BytesIO(response.content)

    text = update.message.caption

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=bytes_obj)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, answer)
    application.add_handler(text_handler)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    application.run_polling()


if __name__ == "__main__":
    main()