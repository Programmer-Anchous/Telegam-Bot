# import logging
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
# from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

# from config import BOT_TOKEN

# # Enable logging
# logging.basicConfig(
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
# )
# logger = logging.getLogger(__name__)


# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Sends a message with three inline buttons attached."""
#     keyboard = [
#         [
#             InlineKeyboardButton("Option 1", callback_data="1"),
#             InlineKeyboardButton("Option 2", callback_data="2"),
#         ],
#         [InlineKeyboardButton("Option 3", callback_data="3")],
#     ]

#     reply_markup = InlineKeyboardMarkup(keyboard)

#     await update.message.reply_text("Please choose:", reply_markup=reply_markup)


# async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Parses the CallbackQuery and updates the message text."""
#     query = update.callback_query

#     # CallbackQueries need to be answered, even if no notification to the user is needed
#     # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
#     await query.answer()

#     await query.edit_message_text(text=f"Selected option: {query.data}")


# async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     """Displays info on how to use the bot."""
#     await update.message.reply_text("Use /start to test this bot.")


# def main() -> None:
#     """Run the bot."""
#     # Create the Application and pass it your bot's token.
#     application = Application.builder().token(BOT_TOKEN).build()

#     application.add_handler(CommandHandler("start", start))
#     application.add_handler(CallbackQueryHandler(button))
#     application.add_handler(CommandHandler("help", help_command))

#     # Run the bot until the user presses Ctrl-C
#     application.run_polling()


# if __name__ == "__main__":
#     main()


import logging
from telegram.ext import Application, filters
from telegram.ext import CommandHandler, MessageHandler
from config import BOT_TOKEN

from datetime import time, date, datetime


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.DEBUG
)

logger = logging.getLogger(__name__)


async def time(update, context):
    time = datetime.now()
    await update.message.reply_text(
        f"Время сейчас: {datetime.strftime(time, '%H:%M:%S')}"
    )


async def date(update, context):
    date = datetime.now()
    await update.message.reply_text(
        f"Дата сегодня: {datetime.strftime(date, '%d.%m.%Y')}"
    )


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет {user.mention_html()}! Я эхо-бот. Напишите мне что-нибудь, и я пришлю это назад!",
    )


async def echo(update, context):
    await update.message.reply_text(update.message.text)


def main():
    application = Application.builder().token(BOT_TOKEN).build()

    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(text_handler)

    application.add_handler(CommandHandler("time", time))
    application.add_handler(CommandHandler("date", date))
    application.add_handler(CommandHandler("start", start))

    application.run_polling()


if __name__ == "__main__":
    main()
