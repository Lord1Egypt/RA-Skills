import requests
import logging
from config import TG_BOT_TOKEN, TG_CHAT_ID

logger = logging.getLogger(__name__)

def send_telegram_message(text: str, parse_mode: str = 'Markdown') -> bool:
    """
    Sends a message to the configured Telegram Chat ID.
    If the message is too long for a single Telegram message (limit 4096),
    it will attempt to split it.
    """
    if not TG_BOT_TOKEN or TG_BOT_TOKEN == "YOUR_TG_BOT_TOKEN":
        logger.warning("Telegram Bot Token is not configured. Skipping notification.")
        return False
        
    url = f"https://api.telegram.org/bot{TG_BOT_TOKEN}/sendMessage"
    
    # Telegram API has a max limit of 4096 characters per message
    MAX_LEN = 4000
    
    if len(text) <= MAX_LEN:
        messages = [text]
    else:
        # Simple chunking by paragraph
        messages = []
        current_chunk = ""
        for par in text.split('\n'):
            if len(current_chunk) + len(par) + 1 > MAX_LEN:
                messages.append(current_chunk)
                current_chunk = par + '\n'
            else:
                current_chunk += par + '\n'
        if current_chunk:
            messages.append(current_chunk)

    success = True
    for idx, msg in enumerate(messages):
        payload = {
            "chat_id": TG_CHAT_ID,
            "text": msg,
            "parse_mode": parse_mode
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            logger.info(f"Successfully sent Telegram message part {idx + 1}/{len(messages)}")
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error sending Telegram message: {response.text}")
            success = False
            # Also try sending without Markdown formatting if Markdown parsing failed
            if parse_mode:
                logger.info("Trying to send without parsing formatting...")
                payload["parse_mode"] = ""
                try:
                    res = requests.post(url, json=payload)
                    res.raise_for_status()
                    success = True
                except Exception as ex:
                    logger.error(f"Still failed: {ex}")
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            success = False

    return success
