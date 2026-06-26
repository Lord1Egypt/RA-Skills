import time
from typing import Dict, Optional, Tuple

import pyautogui

from perception.ocr_engine import OCREngine
from perception.screen_capture import ScreenCapture


class ActionVerifier:
    def __init__(self, capture: ScreenCapture, ocr_engine: Optional[OCREngine] = None):
        self.capture = capture
        self.ocr = ocr_engine

    def snapshot_state(self, region: Optional[Tuple[int, int, int, int]] = None) -> Dict:
        path = self.capture.screenshot_to_file(prefix="state", region=region)
        return {"screenshot": path, "timestamp": time.time(), "region": region}

    def state_changed(self, before: Dict, after: Dict) -> bool:
        return before.get("screenshot") != after.get("screenshot")

    def focus_region(self, bbox, padding: int = 12):
        x, y, w, h = bbox
        return (max(0, x - padding), max(0, y - padding), w + padding * 2, h + padding * 2)

    def pixel_changed(self, point: Tuple[int, int], before_rgb, tolerance: int = 12) -> bool:
        try:
            current = pyautogui.pixel(point[0], point[1])
        except Exception:
            return False
        return any(abs(int(current[i]) - int(before_rgb[i])) > tolerance for i in range(3))

    def read_pixel(self, point: Tuple[int, int]):
        return pyautogui.pixel(point[0], point[1])

    def read_region_text(self, region: Tuple[int, int, int, int]) -> str:
        if not self.ocr or not getattr(self.ocr, "available", False):
            return ""
        img = self.capture.screenshot(region=region)
        items = self.ocr.detect_text(img)
        return " ".join([item.text for item in items]).strip()
