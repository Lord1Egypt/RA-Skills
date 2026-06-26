import time
import schedule
import logging
from datetime import datetime

from config import POLL_INTERVAL_MINUTES
from youtube_monitor import get_new_videos
from extractor import extract_content
from ai_summarizer import summarize_content
from tg_notifier import send_telegram_message

# Configure basic logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def process_video(video: dict):
    """
    End-to-end pipeline for a single video:
    1. Extract content (text or audio)
    2. Summarize with Gemini
    3. Send to Telegram
    """
    logger.info(f"==> Processing Video: {video['title']} ({video['video_id']})")
    
    # 1. Extract content
    content_payload = extract_content(video['video_id'])
    
    if not content_payload:
        logger.error(f"Failed to extract any content for video {video['video_id']}")
        # Optionally notify admin
        # send_telegram_message(f"⚠️ Failed to extract content for: {video['link']}")
        return
        
    # 2. Summarize
    logger.info("Generating summary...")
    summary = summarize_content(content_payload)
    
    if summary and not summary.startswith("Error"):
        # 3. Format Telegram Message
        # Combine video details and the Gemini summary
        message = (
            f"🎬 **New Video from {video['channel_name']}**\n"
            f"📌 [{video['title']}]({video['link']})\n"
            f"🕒 _{video['published']}_\n\n"
            f"🤖 **Gemini AI Summary:**\n"
            f"{summary}"
        )
        logger.info("Sending summary to Telegram...")
        # send_telegram_message uses max 4096 chars and chunks naturally
        send_telegram_message(message)
    else:
        logger.error(f"Failed to summarize video {video['video_id']}. Error: {summary}")

def job():
    """Scheduled job to check for new videos and process them."""
    logger.info("--- Starting scheduled YouTube RSS check ---")
    try:
        new_videos = get_new_videos()
        
        if not new_videos:
            logger.info("No new videos found in this cycle.")
            return
            
        logger.info(f"Found {len(new_videos)} new videos to process.")
        for video in new_videos:
            process_video(video)
            
    except Exception as e:
        logger.error(f"Error during job execution: {e}")
    finally:
        logger.info("--- Check complete. Waiting for next cycle. ---")

def main():
    logger.info(f"Starting YouTube Summarizer Bot. Polling interval: {POLL_INTERVAL_MINUTES} minutes.")
    
    # Note: Izmir is in the Europe/Istanbul timezone (UTC+3)
    # The `schedule` library runs based on the local system time of the machine where the script is hosted.
    # We will assume this machine is in your local timezone. We schedule for 08:00 AM.
    # If the hosting machine is UTC, 8 AM Izmir (UTC+3) would be 05:00 UTC.
    # Assuming the machine time matches your local time (Izmir time):
    schedule.every().day.at("08:00").do(job)
    
    # Keep the script running
    while True:
        try:
            schedule.run_pending()
            time.sleep(60)
        except KeyboardInterrupt:
            logger.info("Bot stopped manually.")
            break
        except Exception as e:
            logger.error(f"Unexpected error in main loop: {e}")
            time.sleep(60) # Wait a bit before crashing out or looping

if __name__ == "__main__":
    main()
