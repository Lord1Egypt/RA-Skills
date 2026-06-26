#!/usr/bin/env python3
"""
Telegram Bot - Simple bot framework using python-telegram-bot
"""

import argparse
import os
import sys
from pathlib import Path

# Try to import telegram, install if needed
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
except ImportError:
    print("Installing python-telegram-bot...")
    os.system("pip install python-telegram-bot")
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command."""
    await update.message.reply_text("Hello! I'm your bot. Type /help for commands.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command."""
    await update.message.reply_text(
        "Available commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help\n"
        "/echo [text] - Echo back your message"
    )


async def echo_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /echo command."""
    text = ' '.join(context.args) if context.args else "Please provide text"
    await update.message.reply_text(text)


async def echo_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo back incoming messages."""
    await update.message.reply_text(update.message.text)


def load_handler(handler_path: str):
    """Load custom handler from Python file."""
    if not os.path.exists(handler_path):
        print(f"Handler file not found: {handler_path}")
        return None
    
    # Add directory to path
    sys.path.insert(0, os.path.dirname(handler_path))
    
    # Import module
    module_name = Path(handler_path).stem
    try:
        return __import__(module_name)
    except Exception as e:
        print(f"Error loading handler: {e}")
        return None


def run_bot(token: str, handler_path: str = None, poll: bool = False):
    """Run the bot."""
    application = Application.builder().token(token).build()
    
    # Add default handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("echo", echo_command))
    
    # Add message handler (echo)
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo_message))
    
    # Load custom handler if provided
    if handler_path:
        handler_module = load_handler(handler_path)
        if handler_module and hasattr(handler_module, 'handle_update'):
            application.add_handler(
                MessageHandler(filters.ALL, handler_module.handle_update)
            )
    
    # Run
    if poll:
        print("Running in polling mode...")
        application.run_polling()
    else:
        print("Running in webhook mode (set --webhook-url)...")


def main():
    parser = argparse.ArgumentParser(description='Telegram Bot')
    parser.add_argument('--token', required=True, help='Bot API token')
    parser.add_argument('--handler', help='Custom handler Python file')
    parser.add_argument('--webhook-url', help='Webhook URL')
    parser.add_argument('--port', type=int, default=8443, help='Webhook server port')
    parser.add_argument('--poll', action='store_true', help='Use polling instead of webhook')
    
    args = parser.parse_args()
    run_bot(args.token, args.handler, args.poll)


if __name__ == '__main__':
    main()
