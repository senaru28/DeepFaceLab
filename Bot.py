import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Load environment variables from .env file
load_dotenv()

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    """Send a greeting message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(f'Hi {user.first_name}! Welcome to the bot.')

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a help message when the command /help is issued."""
    update.message.reply_text('This is a help message. List of commands: /start, /help.')

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error_handler(update: Update, context: CallbackContext) -> None:
    """Log the error and send a message to notify the user."""
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    if update and update.message:
        update.message.reply_text('An unexpected error occurred. Please try again later.')

def main():
    """Start the bot."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error('No token provided! Please set the TELEGRAM_BOT_TOKEN environment variable.')
        return

    updater = Updater(token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    dp.add_error_handler(error_handler)

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()
