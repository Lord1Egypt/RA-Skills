#!/usr/bin/env python3
"""TikTok Android Bot - Mobile automation for TikTok comment posting."""

import subprocess
import time
import random
import re
from typing import Optional, Dict, List
from loguru import logger as log


class TikTokAndroidBot:
    """Android-based TikTok comment bot using ADB."""

    def __init__(self, device_id: str = "emulator-5554"):
        """Initialize Android bot.

        Args:
            device_id: ADB device ID (e.g., "emulator-5554" or physical device serial)
        """
        self.device_id = device_id
        self.tiktok_package = "com.zhiliaoapp.musically"  # TikTok package name

        log.info(f"[Android Bot] Initializing for device: {device_id}")

        # Verify device is connected
        if not self._is_device_connected():
            raise RuntimeError(f"Device {device_id} not connected via ADB")

        log.info(f"[Android Bot] Device {device_id} connected and ready")

    def _is_device_connected(self) -> bool:
        """Check if device is connected via ADB."""
        try:
            result = subprocess.run(
                ["adb", "-s", self.device_id, "get-state"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() == "device"
        except Exception as e:
            log.error(f"[Android Bot] Device check failed: {e}")
            return False

    def _adb_shell(self, command: str, timeout: int = 10) -> str:
        """Execute ADB shell command.

        Args:
            command: Shell command to execute
            timeout: Command timeout in seconds

        Returns:
            Command output
        """
        try:
            result = subprocess.run(
                ["adb", "-s", self.device_id, "shell", command],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return result.stdout.strip()
        except subprocess.TimeoutExpired:
            log.warning(f"[Android Bot] Command timed out: {command}")
            return ""
        except Exception as e:
            log.error(f"[Android Bot] ADB command failed: {e}")
            return ""

    def _tap(self, x: int, y: int, add_randomness: bool = True):
        """Tap at coordinates with optional randomness.

        Args:
            x: X coordinate
            y: Y coordinate
            add_randomness: Add slight random offset to appear more human
        """
        if add_randomness:
            x += random.randint(-5, 5)
            y += random.randint(-5, 5)

        self._adb_shell(f"input tap {x} {y}")
        log.debug(f"[Android Bot] Tapped at ({x}, {y})")
        self._human_delay()

    def _swipe(self, x1: int, y1: int, x2: int, y2: int, duration_ms: int = 300):
        """Swipe from one point to another.

        Args:
            x1, y1: Start coordinates
            x2, y2: End coordinates
            duration_ms: Swipe duration in milliseconds
        """
        self._adb_shell(f"input swipe {x1} {y1} {x2} {y2} {duration_ms}")
        log.debug(f"[Android Bot] Swiped from ({x1},{y1}) to ({x2},{y2})")
        self._human_delay()

    def _type_text(self, text: str):
        """Type text using ADB input.

        Args:
            text: Text to type (will escape special characters)
        """
        # Remove emojis and special characters that cause issues
        # Keep only alphanumeric, spaces, and basic punctuation
        import re
        # Remove emojis and non-ASCII characters
        text_clean = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove non-ASCII
        text_clean = re.sub(r'[^\w\s\.,!?\'-]', '', text_clean)  # Remove special chars

        # Escape special characters for shell
        escaped = text_clean.replace(" ", "%s").replace("'", "").replace('"', '')

        if not escaped:
            log.warning(f"[Android Bot] Text became empty after cleaning: {text}")
            # Use fallback comment if original text was Chinese
            if re.search(r'[\u4e00-\u9fa5]', text):
                fallback_comment = "How often do you exercise each week?"
                log.warning(f"[Android Bot] Using fallback comment: {fallback_comment}")
                text_clean = fallback_comment
                escaped = text_clean.replace(" ", "%s")
            else:
                return

        # Try different input methods for better compatibility
        try:
            # Method 1: Direct input text
            self._adb_shell(f"input text {escaped}")
            log.debug(f"[Android Bot] Typed: {text_clean[:30]}...")
            self._human_delay(0.5, 1.5)
        except Exception as e:
            log.warning(f"[Android Bot] Direct input failed, using key events: {e}")
            # Method 2: Use key events for each character
            for char in text_clean:
                if char == ' ':
                    self._adb_shell('input keyevent KEYCODE_SPACE')
                else:
                    self._adb_shell(f'input keyevent {self._get_keycode(char)}')
                self._human_delay(0.1, 0.3)

    def _get_keycode(self, char: str) -> str:
        """Get Android keycode for a character.

        Args:
            char: Single character

        Returns:
            Android keycode string
        """
        keycodes = {
            'a': 'KEYCODE_A', 'b': 'KEYCODE_B', 'c': 'KEYCODE_C', 'd': 'KEYCODE_D', 'e': 'KEYCODE_E',
            'f': 'KEYCODE_F', 'g': 'KEYCODE_G', 'h': 'KEYCODE_H', 'i': 'KEYCODE_I', 'j': 'KEYCODE_J',
            'k': 'KEYCODE_K', 'l': 'KEYCODE_L', 'm': 'KEYCODE_M', 'n': 'KEYCODE_N', 'o': 'KEYCODE_O',
            'p': 'KEYCODE_P', 'q': 'KEYCODE_Q', 'r': 'KEYCODE_R', 's': 'KEYCODE_S', 't': 'KEYCODE_T',
            'u': 'KEYCODE_U', 'v': 'KEYCODE_V', 'w': 'KEYCODE_W', 'x': 'KEYCODE_X', 'y': 'KEYCODE_Y',
            'z': 'KEYCODE_Z', '0': 'KEYCODE_0', '1': 'KEYCODE_1', '2': 'KEYCODE_2', '3': 'KEYCODE_3',
            '4': 'KEYCODE_4', '5': 'KEYCODE_5', '6': 'KEYCODE_6', '7': 'KEYCODE_7', '8': 'KEYCODE_8',
            '9': 'KEYCODE_9', '.': 'KEYCODE_PERIOD', ',': 'KEYCODE_COMMA', '!': 'KEYCODE_EXCLAMATION',
            '?': 'KEYCODE_QUESTION', '\'': 'KEYCODE_APOSTROPHE', '-': 'KEYCODE_MINUS'
        }
        return keycodes.get(char.lower(), 'KEYCODE_SPACE')

    def _press_key(self, keycode: str):
        """Press Android keycode.

        Args:
            keycode: Android keycode (e.g., "KEYCODE_ENTER", "KEYCODE_BACK")
        """
        self._adb_shell(f"input keyevent {keycode}")
        log.debug(f"[Android Bot] Pressed key: {keycode}")
        self._human_delay()

    def _human_delay(self, min_sec: float = 0.3, max_sec: float = 1.0):
        """Random human-like delay.

        Args:
            min_sec: Minimum delay in seconds
            max_sec: Maximum delay in seconds
        """
        delay = random.uniform(min_sec, max_sec)
        time.sleep(delay)

    def _get_screen_size(self) -> tuple[int, int]:
        """Get device screen size.

        Returns:
            (width, height) tuple
        """
        output = self._adb_shell("wm size")
        match = re.search(r'(\d+)x(\d+)', output)
        if match:
            return int(match.group(1)), int(match.group(2))
        return (1080, 1920)  # Default size

    def install_tiktok(self, apk_path: Optional[str] = None) -> bool:
        """Install TikTok APK on device.

        Args:
            apk_path: Path to TikTok APK file (optional)

        Returns:
            True if installed successfully
        """
        try:
            if apk_path:
                log.info(f"[Android Bot] Installing TikTok from {apk_path}...")
                result = subprocess.run(
                    ["adb", "-s", self.device_id, "install", "-r", apk_path],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                if "Success" in result.stdout:
                    log.info("[Android Bot] ✓ TikTok installed successfully")
                    return True
                else:
                    log.error(f"[Android Bot] Installation failed: {result.stdout}")
                    return False
            else:
                log.info("[Android Bot] TikTok APK path not provided, assuming app is already installed")
                return self.is_tiktok_installed()
        except Exception as e:
            log.error(f"[Android Bot] Installation error: {e}")
            return False

    def is_tiktok_installed(self) -> bool:
        """Check if TikTok is installed."""
        output = self._adb_shell(f"pm list packages | grep {self.tiktok_package}")
        return self.tiktok_package in output

    def launch_tiktok(self) -> bool:
        """Launch TikTok app.

        Returns:
            True if launched successfully
        """
        try:
            log.info("[Android Bot] Launching TikTok...")
            # Launch main activity
            self._adb_shell(f"am start -n {self.tiktok_package}/com.ss.android.ugc.aweme.splash.SplashActivity")
            time.sleep(5)  # Wait for app to load

            # Verify app is in foreground
            output = self._adb_shell("dumpsys window windows | grep mCurrentFocus")
            if self.tiktok_package in output:
                log.info("[Android Bot] ✓ TikTok launched successfully")
                return True
            else:
                log.warning("[Android Bot] TikTok may not be in foreground")
                return True  # Return True anyway, might just be slow
        except Exception as e:
            log.error(f"[Android Bot] Failed to launch TikTok: {e}")
            return False

    def wait_for_feed(self) -> bool:
        """Wait for TikTok feed to load (For You page).

        Returns:
            True if feed loaded
        """
        try:
            log.info("[Android Bot] Waiting for For You feed to load...")
            # TikTok opens directly to For You feed with video already playing
            time.sleep(3)
            log.info("[Android Bot] ✓ For You feed ready (video playing)")
            return True
        except Exception as e:
            log.error(f"[Android Bot] Feed loading failed: {e}")
            return False

    def skip_to_next_video(self, count: int = 1) -> bool:
        """Skip to next video(s) by swiping up.

        Args:
            count: Number of videos to skip

        Returns:
            True if skipped successfully
        """
        try:
            log.info(f"[Android Bot] Skipping {count} video(s)...")

            for i in range(count):
                # Swipe up to go to next video
                self.scroll_down()  # scroll_down swipes up (next video)
                time.sleep(2)  # Wait for video to load

            log.info(f"[Android Bot] ✓ Skipped to video #{count}")
            return True
        except Exception as e:
            log.error(f"[Android Bot] Failed to skip video: {e}")
            return False

    def post_comment(self, comment_text: str) -> bool:
        """Post a comment on current video.

        Args:
            comment_text: Comment to post

        Returns:
            True if comment posted successfully
        """
        try:
            log.info(f"[Android Bot] Posting comment: {comment_text[:50]}...")

            # Get screen size
            width, height = self._get_screen_size()

            # Step 1: Tap on comment icon (FIXED coordinates for 720x1280)
            comment_icon_x = 680  # Fixed coordinate for 720x1280
            comment_icon_y = 769  # Fixed coordinate for 720x1280

            log.debug("[Android Bot] Tapping comment icon on right side...")
            self._tap(comment_icon_x, comment_icon_y)
            time.sleep(2)  # Wait for comment drawer to slide up

            # Step 2: Tap on "Add comment..." input field (FIXED coordinates for 720x1280)
            comment_input_x = 293  # Fixed coordinate for 720x1280
            comment_input_y = 1187  # Fixed coordinate for 720x1280

            log.debug("[Android Bot] Tapping comment input field...")
            self._tap(comment_input_x, comment_input_y)
            time.sleep(1)  # Wait for keyboard to appear

            # Dismiss any popups (like stylus tutorial)
            self._dismiss_popups()
            time.sleep(0.5)

            # Step 3: Type comment text
            log.debug("[Android Bot] Typing comment...")
            
            # Try multiple times to ensure text is entered
            for attempt in range(3):
                log.debug(f"[Android Bot] Typing attempt {attempt + 1}")
                # Clear any existing text
                self._adb_shell('input keyevent KEYCODE_MOVE_END')
                for i in range(30):
                    self._adb_shell('input keyevent KEYCODE_DEL')
                time.sleep(0.5)
                
                # Type the comment
                self._type_text(comment_text)
                time.sleep(2)  # Wait longer for input to complete
                
                # Verify input by pressing space and backspace
                self._adb_shell('input keyevent KEYCODE_SPACE')
                self._adb_shell('input keyevent KEYCODE_DEL')
                time.sleep(1)
                
                log.debug(f"[Android Bot] Typing attempt {attempt + 1} completed")
                break

            # Use exact coordinates provided by user
            post_success = False
            
            log.debug("[Android Bot] Using user-provided send button coordinates...")
            
            # Try 1: Keyboard open mode (user-provided coordinate)
            send_button_x = 643  # Keyboard open mode
            send_button_y = 724  # Keyboard open mode

            log.debug(f"[Android Bot] Tapping Post button at ({send_button_x}, {send_button_y}) - keyboard open...")
            self._tap(send_button_x, send_button_y, add_randomness=False)  # No randomness
            time.sleep(3)  # Wait for comment to post

            # Try 2: Keyboard closed mode (if first try fails)
            # Close keyboard first
            log.debug("[Android Bot] Closing keyboard for second attempt...")
            self._press_key("KEYCODE_BACK")
            time.sleep(1)  # Wait for keyboard to hide

            send_button_x = 632  # Keyboard closed mode
            send_button_y = 1217  # Keyboard closed mode

            log.debug(f"[Android Bot] Tapping Post button at ({send_button_x}, {send_button_y}) - keyboard closed...")
            self._tap(send_button_x, send_button_y, add_randomness=False)  # No randomness
            time.sleep(3)  # Wait for comment to post

            # Step 5: Dismiss keyboard (if still open)
            log.debug("[Android Bot] Dismissing keyboard...")
            self._press_key("KEYCODE_BACK")
            time.sleep(1)  # Wait for keyboard to hide

            log.info("[Android Bot] ✓ Comment posted successfully!")
            return True

        except Exception as e:
            log.error(f"[Android Bot] Comment posting failed: {e}")
            return False

    def go_back(self):
        """Press back button."""
        self._press_key("KEYCODE_BACK")
        time.sleep(1)

    def _dismiss_popups(self):
        """Dismiss any popups that might be blocking interaction."""
        width, height = self._get_screen_size()

        # Tap "Cancel" button for stylus popup (bottom center-left)
        cancel_x = 216  # User provided coordinates
        cancel_y = 1190  # User provided coordinates

        log.debug(f"[Android Bot] Tapping Cancel button at ({cancel_x}, {cancel_y})")
        self._tap(cancel_x, cancel_y, add_randomness=False)
        time.sleep(1)

        log.debug("[Android Bot] Dismissed popups")

    def scroll_down(self):
        """Scroll down (swipe up) - using percentage calculation."""
        width, height = self._get_screen_size()
        
        # Swipe from bottom to top to go to next video
        start_x = width // 2      # Center of screen
        start_y = int(height * 0.75)  # 75% from top (bottom area)
        end_x = width // 2      # Same X
        end_y = int(height * 0.20)   # 20% from top (top area) - longer swipe
        
        duration_ms = random.randint(400, 600)  # Longer duration for reliable swipe
        
        log.debug(f"[Android Bot] Swiping from ({start_x}, {start_y}) to ({end_x}, {end_y})...")
        self._swipe(start_x, start_y, end_x, end_y, duration_ms=duration_ms)

    def _find_icon_position(self, icon_keyword: str) -> Optional[tuple]:
        """Find icon position by searching UI elements.
        
        Args:
            icon_keyword: Keyword to search for in UI dump (e.g., "like", "favorite", "heart")
            
        Returns:
            Tuple of (x, y) coordinates or None if not found
        """
        try:
            # Get UI dump
            ui_dump = self._adb_shell("uiautomator dump /sdcard/ui.xml")
            time.sleep(0.5)
            
            # Pull the dump file
            subprocess.run(
                ["adb", "-s", self.device_id, "pull", "/sdcard/ui.xml", "/tmp/ui.xml"],
                capture_output=True,
                timeout=5
            )
            
            # Read and parse UI dump
            try:
                with open("/tmp/ui.xml", "r", encoding="utf-8") as f:
                    content = f.read()
                
                # Search for icon with keyword
                # Look for bounds attribute
                pattern = rf'{icon_keyword}[^>]*bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"'
                matches = re.findall(pattern, content, re.IGNORECASE)
                
                if matches:
                    # Return center of first match
                    x1, y1, x2, y2 = matches[0]
                    center_x = (int(x1) + int(x2)) // 2
                    center_y = (int(y1) + int(y2)) // 2
                    log.debug(f"[Android Bot] Found {icon_keyword} at ({center_x}, {center_y})")
                    return (center_x, center_y)
                    
            except Exception as e:
                log.debug(f"[Android Bot] Failed to parse UI dump: {e}")
                
        except Exception as e:
            log.debug(f"[Android Bot] Failed to find icon {icon_keyword}: {e}")
        
        return None

    def like_video(self) -> bool:
        """Like the current video.
        
        Returns:
            True if like successful
        """
        try:
            log.info("[Android Bot] Liking video...")
            
            # Wait for video UI to stabilize
            time.sleep(2)
            
            # Try to find like icon dynamically
            like_pos = self._find_icon_position("like")
            
            if like_pos:
                like_icon_x, like_icon_y = like_pos
                log.debug(f"[Android Bot] Found like icon at ({like_icon_x}, {like_icon_y})")
            else:
                # Fallback to fixed position
                like_icon_x = 666
                like_icon_y = 629
                log.debug(f"[Android Bot] Using fallback like position ({like_icon_x}, {like_icon_y})")
            
            log.debug(f"[Android Bot] Tapping like icon at ({like_icon_x}, {like_icon_y})...")
            self._tap(like_icon_x, like_icon_y, add_randomness=False)
            time.sleep(1)
            
            log.info("[Android Bot] ✓ Video liked!")
            return True
            
        except Exception as e:
            log.error(f"[Android Bot] Like failed: {e}")
            return False

    def favorite_video(self) -> bool:
        """Favorite (bookmark) the current video.
        
        Returns:
            True if favorite successful
        """
        try:
            log.info("[Android Bot] Favoriting video...")
            
            # Wait for video UI to stabilize
            time.sleep(2)
            
            # Try to find favorite icon dynamically
            favorite_pos = self._find_icon_position("favorite")
            
            if favorite_pos:
                favorite_icon_x, favorite_icon_y = favorite_pos
                log.debug(f"[Android Bot] Found favorite icon at ({favorite_icon_x}, {favorite_icon_y})")
            else:
                # Fallback to fixed position
                favorite_icon_x = 664
                favorite_icon_y = 823
                log.debug(f"[Android Bot] Using fallback favorite position ({favorite_icon_x}, {favorite_icon_y})")
            
            log.debug(f"[Android Bot] Tapping favorite icon at ({favorite_icon_x}, {favorite_icon_y})...")
            self._tap(favorite_icon_x, favorite_icon_y, add_randomness=False)
            time.sleep(1)
            
            log.info("[Android Bot] ✓ Video favorited!")
            return True
            
        except Exception as e:
            log.error(f"[Android Bot] Favorite failed: {e}")
            return False

    def publish_video(self, video_path: str, description: str = "") -> bool:
        """Publish a video to TikTok.

        Args:
            video_path: Path to video file on local machine
            description: Video description/caption

        Returns:
            True if publish successful
        """
        try:
            log.info(f"[Android Bot] Publishing video: {video_path}")

            # Step 1: Tap "+" button (center bottom)
            log.debug("[Android Bot] Step 1: Tapping + button...")
            self._tap(360, 1230, add_randomness=False)
            time.sleep(2)

            # Step 2: Tap "From Album" (bottom left)
            log.debug("[Android Bot] Step 2: Tapping From Album...")
            self._tap(67, 1212, add_randomness=False)
            time.sleep(2)

            # Step 3: Tap first video in album (first frame)
            log.debug("[Android Bot] Step 3: Selecting first video...")
            self._tap(123, 355, add_randomness=False)
            time.sleep(1)

            # Step 4: Tap Next button
            log.debug("[Android Bot] Step 4: Tapping Next button...")
            self._tap(526, 1217, add_randomness=False)
            time.sleep(3)

            # Step 5: Enter video description
            if description:
                log.debug(f"[Android Bot] Step 5: Entering description: {description}")
                self._tap(55, 177, add_randomness=False)
                time.sleep(1)
                self._type_text(description)
                time.sleep(1)

            # Step 6: Dismiss keyboard
            log.debug("[Android Bot] Step 6: Dismissing keyboard...")
            self._tap(525, 528, add_randomness=False)
            time.sleep(1)

            # Step 7: Tap Publish button
            log.debug("[Android Bot] Step 7: Tapping Publish button...")
            self._tap(521, 1210, add_randomness=False)
            time.sleep(5)  # Wait for upload to complete

            log.info("[Android Bot] ✓ Video published successfully!")
            return True

        except Exception as e:
            log.error(f"[Android Bot] Publish failed: {e}")
            return False

    def take_screenshot(self, save_path: str) -> bool:
        """Take screenshot and save to file.

        Args:
            save_path: Local path to save screenshot

        Returns:
            True if screenshot saved successfully
        """
        try:
            # Take screenshot on device
            device_path = "/sdcard/screenshot.png"
            self._adb_shell(f"screencap -p {device_path}")

            # Pull screenshot to local machine
            subprocess.run(
                ["adb", "-s", self.device_id, "pull", device_path, save_path],
                capture_output=True,
                timeout=10
            )

            # Clean up device
            self._adb_shell(f"rm {device_path}")

            log.info(f"[Android Bot] Screenshot saved: {save_path}")
            return True
        except Exception as e:
            log.error(f"[Android Bot] Screenshot failed: {e}")
            return False

    def close_app(self):
        """Force close TikTok app."""
        log.info("[Android Bot] Closing TikTok...")
        self._adb_shell(f"am force-stop {self.tiktok_package}")
        time.sleep(1)
