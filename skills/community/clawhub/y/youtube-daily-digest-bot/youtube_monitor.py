import feedparser
import json
import os
import logging
from typing import List, Dict

from config import YOUTUBE_CHANNELS, DB_FILE

logger = logging.getLogger(__name__)

def load_db() -> Dict[str, List[str]]:
    """Loads the database of processed video IDs."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading DB: {e}")
            return {}
    return {}

def save_db(db: Dict[str, List[str]]):
    """Saves the database of processed video IDs."""
    try:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"Error saving DB: {e}")

def get_new_videos() -> List[Dict]:
    """
    Checks the RSS feeds for all configured channels and returns a list
    of new videos that haven't been processed yet.
    """
    db = load_db()
    new_videos = []

    for channel_id, channel_name in YOUTUBE_CHANNELS.items():
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        logger.info(f"Checking RSS feed for {channel_name} ({channel_id})...")
        
        try:
            feed = feedparser.parse(rss_url)
            
            if channel_id not in db:
                db[channel_id] = []
                
            for entry in feed.entries:
                video_id = entry.yt_videoid
                if video_id not in db[channel_id]:
                    # Found a new video
                    video_info = {
                        'channel_name': channel_name,
                        'channel_id': channel_id,
                        'video_id': video_id,
                        'title': entry.title,
                        'link': entry.link,
                        'published': entry.published
                    }
                    new_videos.append(video_info)
                    
                    # Add to local DB so we don't process it again next time
                    db[channel_id].append(video_id)
                    logger.info(f"Found new video: {entry.title} ({video_id})")
                    
        except Exception as e:
            logger.error(f"Error checking channel {channel_name}: {e}")

    # Save immediately to prevent duplicate processing
    if new_videos:
        save_db(db)

    return new_videos

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    videos = get_new_videos()
    print(f"Total new videos found: {len(videos)}")
    if not videos:
        print("No new videos found. (Are they already in db.json?)")
    for v in videos:
        print(v['title'], "-", v['link'])
