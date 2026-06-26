import asyncio
import logging
import sys
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    handlers=[
        logging.FileHandler("bot.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from health_check import run_all_health_checks
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler
from telegram_ui import handle_start, handle_button, handle_status
from config import TELEGRAM_BOT_TOKEN


def main():
    logger.info("Simmer Weather Bot starting — running health checks")

    asyncio.get_event_loop().run_until_complete(run_all_health_checks())

    logger.info("All health checks passed — starting Telegram bot")
    print("🚀 Starting Telegram bot...")

    app = (
        ApplicationBuilder()
        .token(TELEGRAM_BOT_TOKEN)
        .build()
    )

    app.add_handler(CommandHandler("start", handle_start))
    app.add_handler(CommandHandler("status", handle_status))
    app.add_handler(CallbackQueryHandler(handle_button, pattern="^(predict_|status)"))

    logger.info("Bot is polling for updates")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
