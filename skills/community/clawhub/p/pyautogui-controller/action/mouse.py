import time
from typing import Tuple
import pyautogui
from app.config import InputConfig


class MouseController:
    def __init__(self, config: InputConfig):
        pyautogui.FAILSAFE = True
        self.config = config
        self.screen_width, self.screen_height = pyautogui.size()

    def clamp(self, x: int, y: int) -> Tuple[int, int]:
        x = min(max(int(x), 1), self.screen_width - 1)
        y = min(max(int(y), 1), self.screen_height - 1)
        return x, y

    def move_to(self, x: int, y: int, safe: bool = False):
        x, y = self.clamp(x, y)
        duration = self.config.move_duration_safe if safe else self.config.move_duration_fast
        pyautogui.moveTo(x, y, duration=duration)

    def click_point(self, x: int, y: int, safe: bool = False, clicks: int = 1):
        self.move_to(x, y, safe=safe)
        time.sleep(self.config.click_pause)
        pyautogui.click(x, y, clicks=clicks)
        time.sleep(self.config.post_action_delay)

    def click_bbox(self, bbox, safe: bool = False):
        x, y, w, h = bbox
        sample_points = [
            (x + w // 2, y + h // 2),
            (x + w // 2, y + max(4, h // 3)),
            (x + max(4, w // 3), y + h // 2),
            (x + min(w - 4, (w * 2) // 3), y + h // 2),
        ]
        for px, py in sample_points:
            px, py = self.clamp(px, py)
            self.click_point(px, py, safe=safe)
            return (px, py)
