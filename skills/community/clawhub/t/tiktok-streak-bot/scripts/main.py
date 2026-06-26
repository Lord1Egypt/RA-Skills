import os
import sys
import json
import logging
from datetime import datetime

# Add the current directory to sys.path to allow relative imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config_loader import ConfigLoader
from state_manager import StateManager
from scheduler import Scheduler
from lib.browser import BrowserManager
from lib.session import SessionManager
from lib.streak import StreakManager
from lib.utils import setup_logging

def main():
    # Paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "data/config.json")
    usernames_path = os.path.join(base_dir, "data/usernames.json")
    cookies_path = os.path.join(base_dir, "data/cookies.json")
    state_path = os.path.join(base_dir, "data/state.json")
    log_path = os.path.join(base_dir, "data/tiktok_bot.log")

    # Setup logging
    setup_logging(log_path)
    logging.info("--- TikTok Streak Bot Started ---")

    # Load configuration
    config_loader = ConfigLoader(config_path)
    config = config_loader.load()
    if not config:
        logging.error("Failed to load configuration. Exiting.")
        return

    # Load state
    state_manager = StateManager(state_path)
    state_manager.load()

    # Load usernames
    if os.path.exists(usernames_path):
        with open(usernames_path, 'r', encoding='utf-8') as f:
            usernames = json.load(f)
    else:
        logging.error(f"Usernames file not found at {usernames_path}. Exiting.")
        return

    # Initialize browser
    browser = BrowserManager(
        headless=config.get("headless", True),
        user_agent=config.get("user_agent")
    )
    page = browser.start()

    # Initialize session
    session = SessionManager(browser.context, cookies_path)
    if not session.load_cookies():
        logging.warning("No cookies loaded. Manual login may be required.")
        # In a real scenario, we might want to pause for manual login here
        # but for an automated skill, we assume cookies are provided.

    # Initialize and run streak manager
    streak_manager = StreakManager(page, config, state_manager, usernames)
    
    try:
        streak_manager.run()
        # Save session cookies after run
        session.context = streak_manager.sender.page.context
        session.save_cookies()
    except Exception as e:
        logging.error(f"An error occurred during execution: {e}")
    finally:
        browser.stop()
        logging.info("--- TikTok Streak Bot Finished ---")

if __name__ == "__main__":
    main()
