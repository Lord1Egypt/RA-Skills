import httpx
import logging
from app.config import config

logger = logging.getLogger(__name__)

TELEGRAM_API = "https://api.telegram.org/bot{token}/{method}"


async def send_message(text: str, chat_id: str = None) -> dict:
    """
    Send a formatted message to a Telegram chat.

    Args:
        text:    Markdown-formatted message text.
        chat_id: Override default chat ID (optional).

    Returns:
        Telegram API response as dict.
    """
    target_chat = chat_id or config.TELEGRAM_CHAT_ID
    url = TELEGRAM_API.format(token=config.TELEGRAM_BOT_TOKEN, method="sendMessage")

    payload = {
        "chat_id":    target_chat,
        "text":       text,
        "parse_mode": "Markdown",
        "disable_web_page_preview": True,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        try:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            logger.info(f"Message sent to chat {target_chat}")
            return response.json()
        except httpx.HTTPStatusError as e:
            logger.error(f"Telegram API error: {e.response.text}")
            raise
        except httpx.RequestError as e:
            logger.error(f"Network error when contacting Telegram: {e}")
            raise


async def send_photo(photo_url: str, caption: str = None, chat_id: str = None) -> dict:
    """Send a photo with optional caption."""
    target_chat = chat_id or config.TELEGRAM_CHAT_ID
    url = TELEGRAM_API.format(token=config.TELEGRAM_BOT_TOKEN, method="sendPhoto")

    payload = {
        "chat_id":   target_chat,
        "photo":     photo_url,
        "caption":   caption or "",
        "parse_mode": "Markdown",
    }

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        return response.json()
