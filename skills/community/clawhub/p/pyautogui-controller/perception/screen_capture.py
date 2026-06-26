from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple
import pyautogui
from PIL import Image


class ScreenCapture:
    def __init__(self, out_dir: Path):
        self.out_dir = out_dir
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def screenshot(self, region: Optional[Tuple[int, int, int, int]] = None) -> Image.Image:
        return pyautogui.screenshot(region=region)

    def screenshot_to_file(self, prefix: str = "shot", region: Optional[Tuple[int, int, int, int]] = None) -> str:
        img = self.screenshot(region=region)
        path = self.out_dir / f"{prefix}_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png"
        img.save(path)
        return str(path)
