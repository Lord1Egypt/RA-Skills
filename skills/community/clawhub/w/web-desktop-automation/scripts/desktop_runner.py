"""PyAutoGUI desktop automation template.

Usage:
    python scripts/desktop_runner.py

Install:
    pip install pyautogui
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Optional, Tuple

import pyautogui


@dataclass
class DesktopConfig:
    pause_seconds: float = 0.2
    fail_safe: bool = True


class DesktopRunner:
    def __init__(self, config: Optional[DesktopConfig] = None) -> None:
        self.config = config or DesktopConfig()
        pyautogui.PAUSE = self.config.pause_seconds
        pyautogui.FAILSAFE = self.config.fail_safe

    def move(self, x: int, y: int, duration: float = 0.2) -> None:
        pyautogui.moveTo(x, y, duration=duration)

    def click(self, x: int, y: int, button: str = "left") -> None:
        pyautogui.click(x, y, button=button)

    def double_click(self, x: int, y: int) -> None:
        pyautogui.doubleClick(x, y)

    def write(self, text: str, interval: float = 0.02) -> None:
        pyautogui.write(text, interval=interval)

    def hotkey(self, *keys: str) -> None:
        pyautogui.hotkey(*keys)

    def press(self, key: str) -> None:
        pyautogui.press(key)

    def screenshot(self, path: str) -> None:
        pyautogui.screenshot(path)

    def locate(self, image_path: str, confidence: float = 0.9) -> Optional[Tuple[int, int, int, int]]:
        return pyautogui.locateOnScreen(image_path, confidence=confidence)

    def click_image(self, image_path: str, confidence: float = 0.9) -> bool:
        box = self.locate(image_path, confidence=confidence)
        if not box:
            return False
        center = pyautogui.center(box)
        pyautogui.click(center.x, center.y)
        return True

    def sleep(self, seconds: float) -> None:
        time.sleep(seconds)


if __name__ == "__main__":
    runner = DesktopRunner()
    runner.sleep(1)
    print(pyautogui.position())
