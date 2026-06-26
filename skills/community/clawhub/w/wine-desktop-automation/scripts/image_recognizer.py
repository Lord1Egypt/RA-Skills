import pyautogui
import time
import os
from typing import Optional, List, Tuple
from dataclasses import dataclass
from PIL import Image
from ..utils.logger import get_logger
from ..utils.config import get_config

logger = get_logger(__name__)
config = get_config()


@dataclass
class MatchResult:
    x: int
    y: int
    width: int
    height: int
    confidence: float
    center_x: int
    center_y: int

    def __repr__(self):
        return f'MatchResult(center=({self.center_x}, {self.center_y}), confidence={self.confidence:.2f})'


class ImageRecognizer:
    def __init__(self):
        self._default_confidence = config.get('IMAGE_CONFIDENCE', 0.9)
        self._default_timeout = config.get('IMAGE_MATCH_TIMEOUT', 30)

    def find(self, image_path: str, confidence: Optional[float] = None,
             region: Optional[Tuple[int, int, int, int]] = None,
             grayscale: bool = False) -> Optional[MatchResult]:
        if not os.path.exists(image_path):
            logger.error(f'Image file not found: {image_path}')
            return None

        confidence = confidence or self._default_confidence
        
        try:
            location = pyautogui.locateOnScreen(
                image_path,
                confidence=confidence,
                region=region,
                grayscale=grayscale
            )
            
            if location:
                match = self._create_match_result(location, confidence)
                logger.info(f'Found image: {image_path} at {match}')
                return match
            else:
                logger.debug(f'Image not found: {image_path}')
                return None
                
        except Exception as e:
            logger.error(f'Error finding image {image_path}: {e}')
            return None

    def find_all(self, image_path: str, confidence: Optional[float] = None,
                 region: Optional[Tuple[int, int, int, int]] = None,
                 grayscale: bool = False) -> List[MatchResult]:
        if not os.path.exists(image_path):
            logger.error(f'Image file not found: {image_path}')
            return []

        confidence = confidence or self._default_confidence
        
        try:
            locations = pyautogui.locateAllOnScreen(
                image_path,
                confidence=confidence,
                region=region,
                grayscale=grayscale
            )
            
            matches = [self._create_match_result(loc, confidence) for loc in locations]
            logger.info(f'Found {len(matches)} instances of image: {image_path}')
            return matches
            
        except Exception as e:
            logger.error(f'Error finding all instances of {image_path}: {e}')
            return []

    def wait_for(self, image_path: str, timeout: Optional[int] = None,
                 confidence: Optional[float] = None,
                 region: Optional[Tuple[int, int, int, int]] = None,
                 grayscale: bool = False) -> Optional[MatchResult]:
        timeout = timeout or self._default_timeout
        start_time = time.time()
        
        logger.info(f'Waiting for image: {image_path} (timeout: {timeout}s)')
        
        while time.time() - start_time < timeout:
            match = self.find(image_path, confidence, region, grayscale)
            if match:
                return match
            time.sleep(0.5)
        
        logger.warning(f'Timeout waiting for image: {image_path}')
        return None

    def wait_until_gone(self, image_path: str, timeout: Optional[int] = None,
                       confidence: Optional[float] = None,
                       region: Optional[Tuple[int, int, int, int]] = None,
                       grayscale: bool = False) -> bool:
        timeout = timeout or self._default_timeout
        start_time = time.time()
        
        logger.info(f'Waiting for image to disappear: {image_path} (timeout: {timeout}s)')
        
        while time.time() - start_time < timeout:
            match = self.find(image_path, confidence, region, grayscale)
            if not match:
                logger.info(f'Image disappeared: {image_path}')
                return True
            time.sleep(0.5)
        
        logger.warning(f'Timeout waiting for image to disappear: {image_path}')
        return False

    def screenshot(self, filename: Optional[str] = None,
                   region: Optional[Tuple[int, int, int, int]] = None) -> Image.Image:
        try:
            screenshot = pyautogui.screenshot(region=region)
            
            if filename:
                screenshot.save(filename)
                logger.info(f'Screenshot saved: {filename}')
            
            return screenshot
            
        except Exception as e:
            logger.error(f'Error taking screenshot: {e}')
            raise

    def screenshot_region(self, x: int, y: int, width: int, height: int,
                         filename: Optional[str] = None) -> Image.Image:
        return self.screenshot(filename, region=(x, y, width, height))

    def locate_center(self, image_path: str, confidence: Optional[float] = None,
                     region: Optional[Tuple[int, int, int, int]] = None,
                     grayscale: bool = False) -> Optional[Tuple[int, int]]:
        match = self.find(image_path, confidence, region, grayscale)
        if match:
            return (match.center_x, match.center_y)
        return None

    def pixel_matches_color(self, x: int, y: int, color: Tuple[int, int, int],
                           tolerance: int = 10) -> bool:
        try:
            return pyautogui.pixelMatchesColor(x, y, color, tolerance)
        except Exception as e:
            logger.error(f'Error checking pixel color at ({x}, {y}): {e}')
            return False

    def get_pixel_color(self, x: int, y: int) -> Optional[Tuple[int, int, int]]:
        try:
            return pyautogui.pixel(x, y)
        except Exception as e:
            logger.error(f'Error getting pixel color at ({x}, {y}): {e}')
            return None

    def search_color(self, color: Tuple[int, int, int], tolerance: int = 10,
                    region: Optional[Tuple[int, int, int, int]] = None) -> Optional[Tuple[int, int]]:
        try:
            screenshot = self.screenshot(region=region)
            width, height = screenshot.size
            
            for y in range(height):
                for x in range(width):
                    pixel = screenshot.getpixel((x, y))
                    if self._color_match(pixel, color, tolerance):
                        if region:
                            return (region[0] + x, region[1] + y)
                        return (x, y)
            
            return None
            
        except Exception as e:
            logger.error(f'Error searching for color: {e}')
            return None

    def _create_match_result(self, location, confidence: float) -> MatchResult:
        return MatchResult(
            x=location.left,
            y=location.top,
            width=location.width,
            height=location.height,
            confidence=confidence,
            center_x=location.left + location.width // 2,
            center_y=location.top + location.height // 2
        )

    def _color_match(self, pixel: Tuple[int, int, int], 
                    target: Tuple[int, int, int], tolerance: int) -> bool:
        return all(abs(p - t) <= tolerance for p, t in zip(pixel, target))

    def save_template(self, x: int, y: int, width: int, height: int,
                     filename: str) -> bool:
        try:
            screenshot = self.screenshot_region(x, y, width, height)
            screenshot.save(filename)
            logger.info(f'Template saved: {filename}')
            return True
        except Exception as e:
            logger.error(f'Error saving template: {e}')
            return False

    def get_screen_size(self) -> Tuple[int, int]:
        return pyautogui.size()

    def on_screen(self, x: int, y: int) -> bool:
        return pyautogui.onScreen(x, y)


image = ImageRecognizer()
