import logging
from telegram.ext import Application, filters
from telegram.ext import CommandHandler, MessageHandler
from config import BOT_TOKEN

from io import BytesIO
from requests import get
from pil_filters import filters_and_effects

from PIL import Image


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

logger = logging.getLogger(__name__)


info_text = """
Send me a photo and in the caption write the numbers corresponding to the effects you want to apply:
1 - blur
2 - contour
3 - detail
4 - edge_enhance
5 - emdoss
6 - find_edged
7 - sharpen
8 - smooth
"""

start_text = f"""
Hi! I can put effects on your photo.
{info_text}
commands:
/start
/info
"""

def pil_to_bytes(pil_photo):
    new_photo = pil_photo.copy()
    buf = BytesIO()
    new_photo.save(buf, format="JPEG")
    bytes_new_photo = buf.getvalue()
    return bytes_new_photo


async def start(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=start_text)


async def info(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=info_text)


async def answer(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


async def handle_photo(update, context):
    photo = await update.message.effective_attachment[-1].get_file()
    url = photo.file_path
    response = get(url)
    bytes_obj = BytesIO(response.content)

    text = update.message.caption
    text = text.strip()

    pil_photo = Image.open(bytes_obj)
    for index in text.split():
        pil_photo = filters_and_effects[int(index) - 1](pil_photo)
    
    bytes_new_photo = pil_to_bytes(pil_photo)

    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=bytes_new_photo)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, answer)
    application.add_handler(text_handler)

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    application.run_polling()


if __name__ == "__main__":
    main()
