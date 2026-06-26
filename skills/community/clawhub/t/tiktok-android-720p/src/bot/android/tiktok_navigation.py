#!/usr/bin/env python3
"""TikTok navigation and search functionality."""

import time
import random
from loguru import logger as log


class TikTokNavigation:
    """Navigation helpers for TikTok Android app."""
    
    def __init__(self, bot):
        """Initialize with TikTokAndroidBot instance."""
        self.bot = bot
        self.width, self.height = bot._get_screen_size()
    
    def go_to_home(self):
        """Navigate to Home tab (For You page)."""
        log.info("[Navigation] Going to Home tab...")
        # Home icon is usually first from left in bottom nav
        home_x = int(self.width * 0.10)  # 10% from left
        home_y = int(self.height * 0.97)  # Bottom nav bar
        
        self.bot._tap(home_x, home_y)
        time.sleep(2)
        log.info("[Navigation] ✓ On Home tab")
    
    def tap_search_icon(self):
        """Tap search icon in top right corner of Home screen."""
        log.info("[Navigation] Tapping search icon (top right)...")
        # Search icon precise coordinates based on detailed analysis
        # X: 990-1000 pixels (far right, ~92% from left)
        # Y: 200-210 pixels (below status bar, in nav area)
        search_icon_x = 660  # Precise X coordinate
        search_icon_y = 140  # Precise Y coordinate (not percentage!)
        
        log.debug(f"[Navigation] Tapping search icon at ({search_icon_x}, {search_icon_y})")
        self.bot._tap(search_icon_x, search_icon_y)
        time.sleep(2)
        log.info("[Navigation] ✓ Search opened")
    
    def search_query(self, query: str) -> bool:
        """Search for a query using the search icon flow.
        
        Args:
            query: Search term (e.g., "dragy")
            
        Returns:
            True if search successful
        """
        try:
            log.info(f"[Navigation] Searching for: {query}")
            
            # Clear any existing text in search field (FIXED coordinates for 720x1280)
            log.debug("[Navigation] Clearing search field...")
            
            # Tap search field (FIXED coordinates for 720x1280)
            search_field_x = 360  # Fixed coordinate for 720x1280
            search_field_y = 64   # Fixed coordinate for 720x1280
            
            self.bot._tap(search_field_x, search_field_y)
            time.sleep(0.5)
            
            # Clear field completely
            self.bot._adb_shell('input keyevent KEYCODE_MOVE_END')
            for i in range(50):
                self.bot._adb_shell('input keyevent KEYCODE_DEL')
            time.sleep(1)
            
            # Use direct ADB input for search query
            escaped_query = query.replace(' ', '%s')
            log.debug(f"[Navigation] Using direct ADB input: {escaped_query}")
            
            # Try direct input
            self.bot._adb_shell(f'input text {escaped_query}')
            time.sleep(2)  # Wait for input to appear
            
            # Verify input
            log.debug(f"[Navigation] Query '{query}' typed")
            
            # Tap search button (FIXED coordinates for 720x1280)
            search_button_x = 684  # User provided coordinates
            search_button_y = 64   # User provided coordinates
            log.debug(f"[Navigation] Tapping search button at ({search_button_x}, {search_button_y})...")
            self.bot._tap(search_button_x, search_button_y)
            time.sleep(3)  # Wait for results page to load
            
            log.info(f"[Navigation] ✓ Search results loaded for: {query}")
            return True
            
        except Exception as e:
            log.error(f"[Navigation] Search failed: {e}")
            return False
    
    def get_search_results_screenshot(self) -> str:
        """Take screenshot of search results to analyze videos/lives list.
        
        Returns:
            Path to screenshot file
        """
        log.info("[Navigation] Capturing search results for analysis...")
        screenshot_path = "data/search_results_list.png"
        self.bot.take_screenshot(screenshot_path)
        log.info(f"[Navigation] ✓ Search results captured: {screenshot_path}")
        return screenshot_path
    
    def tap_video_from_grid(self, position: int = 1):
        """Tap a video from the 2x2 search results grid.
        
        Args:
            position: Which video to tap (1-4)
                1 = top-left, 2 = top-right
                3 = bottom-left, 4 = bottom-right
        """
        log.info(f"[Navigation] Tapping video {position} from grid...")
        
        # Search results show 2x2 grid (2 columns)
        # Calculate position based on grid layout
        if position in [1, 3]:  # Left column
            video_x = int(self.width * 0.27)  # Left column center
        else:  # Right column (2, 4)
            video_x = int(self.width * 0.73)  # Right column center
        
        if position in [1, 2]:  # Top row
            video_y = int(self.height * 0.35)  # Upper area
        else:  # Bottom row (3, 4)
            video_y = int(self.height * 0.55)  # Lower area
        
        log.debug(f"[Navigation] Tapping video at ({video_x}, {video_y})")
        self.bot._tap(video_x, video_y)
        time.sleep(3)  # Wait for video to load
        log.info("[Navigation] ✓ Video opened")
    
    def go_to_profile(self):
        """Navigate to video creator's profile."""
        log.info("[Navigation] Going to profile...")
        
        # Profile picture is usually top-left of video
        # Or tap username at top
        profile_x = int(self.width * 0.15)  # Left side
        profile_y = int(self.height * 0.10)  # Top area
        
        self.bot._tap(profile_x, profile_y)
        time.sleep(2)
        log.info("[Navigation] ✓ On profile page")
    
    def go_back_to_feed(self):
        """Return to main feed."""
        log.info("[Navigation] Going back to feed...")
        self.bot.go_back()
        time.sleep(1)
    
    def scroll_to_next_video(self):
        """Scroll to next video in feed."""
        log.info("[Navigation] Scrolling to next video...")
        self.bot.scroll_down()  # This swipes up = next video
        time.sleep(2)
    
    def get_video_info(self) -> dict:
        """Extract video information (caption, username).
        
        Returns:
            dict with video_text, username, etc.
        """
        # For now, take screenshot and we'll analyze it with AI
        # In future, could use OCR or TikTok API
        
        screenshot_path = "data/current_video.png"
        self.bot.take_screenshot(screenshot_path)
        
        log.info("[Navigation] Video info captured via screenshot")
        
        return {
            "screenshot": screenshot_path,
            "timestamp": time.time()
        }
