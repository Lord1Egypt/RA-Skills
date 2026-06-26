import time
from dataclasses import dataclass
from typing import Optional

from action.browser_dom_backend import BrowserDOMBackend
from action.keyboard import KeyboardController
from action.mouse import MouseController
from action.window_manager import WindowManager
from app.config import AppConfig


@dataclass
class BrowserCommandResult:
    success: bool
    detail: str = ""


class BrowserBackend:
    """Browser-focused low-level operations."""

    def __init__(self, config: AppConfig, mouse: MouseController, keyboard: KeyboardController):
        self.config = config
        self.mouse = mouse
        self.keyboard = keyboard
        self.window_manager = WindowManager()
        self.dom = BrowserDOMBackend(enabled=config.runtime.use_dom_backend)

    def ensure_browser_window(self) -> BrowserCommandResult:
        keywords = self.config.runtime.preferred_window_titles
        if self.window_manager.activate_window(keywords):
            return BrowserCommandResult(True, "window_activated")
        return BrowserCommandResult(False, "window_not_found")

    def get_browser_window(self):
        return self.window_manager.find_window(self.config.runtime.preferred_window_titles)

    def focus_address_bar(self) -> BrowserCommandResult:
        self.ensure_browser_window()
        self.mouse.click_point(
            self.config.runtime.browser_address_bar_x,
            self.config.runtime.browser_address_bar_y,
            safe=True,
        )
        time.sleep(0.15)
        return BrowserCommandResult(True, "address_bar_focused")

    def navigate(self, url: str) -> BrowserCommandResult:
        self.focus_address_bar()
        self.keyboard.hotkey("ctrl", "a")
        self.keyboard.type_text(url)
        self.keyboard.hotkey("enter")
        return BrowserCommandResult(True, url)

    def reload(self) -> BrowserCommandResult:
        self.keyboard.hotkey("ctrl", "r")
        return BrowserCommandResult(True, "reload")

    def dom_focus_input(self, target_text: Optional[str] = None, url: Optional[str] = None) -> BrowserCommandResult:
        result = self.dom.focus_input(target_text=target_text, url=url)
        return BrowserCommandResult(result.success, result.detail)

    def dom_click(self, target_text: Optional[str] = None, role: Optional[str] = None, url: Optional[str] = None) -> BrowserCommandResult:
        result = self.dom.click(target_text=target_text, role=role, url=url)
        return BrowserCommandResult(result.success, result.detail)

    def dom_type_into(self, text: str, target_text: Optional[str] = None, role: Optional[str] = None, url: Optional[str] = None) -> BrowserCommandResult:
        result = self.dom.type_into(text=text, target_text=target_text, role=role, url=url)
        return BrowserCommandResult(result.success, result.detail)
