#!/usr/bin/env python3
"""Legacy compatibility wrapper.

Prefer the new layered architecture in core/orchestrator.py.
This module keeps old call sites working.
"""

from app.config import AppConfig
from core.orchestrator import Orchestrator


class SmartBrowser:
    def __init__(self):
        self.runner = Orchestrator(AppConfig())

    def open_and_navigate(self, url: str, wait_time: int = 5):
        return self.runner.execute(f"打开浏览器访问 {url}")

    def handle_verification(self, timeout: int = 30) -> bool:
        # Legacy placeholder: verification should be handled by perception + click flows.
        return False

    def find_input_box(self):
        candidates = self.runner.vision.locate_candidates(target_type=None)
        return candidates[0].center if candidates else None

    def input_text(self, text: str, use_clipboard: bool = True):
        return self.runner.execute(f"在输入框输入 '{text}'")

    def send_message(self, key: str = 'return'):
        self.runner.keyboard.hotkey(key)
        return True


class NaturalLanguageController:
    def __init__(self):
        self.runner = Orchestrator(AppConfig())

    def execute(self, command: str):
        return self.runner.execute(command)
