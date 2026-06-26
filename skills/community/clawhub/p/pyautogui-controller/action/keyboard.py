import time
import pyautogui
import pyperclip
from app.config import InputConfig


class KeyboardController:
    def __init__(self, config: InputConfig):
        pyautogui.FAILSAFE = True
        self.config = config

    def hotkey(self, *keys: str):
        pyautogui.hotkey(*keys)
        time.sleep(self.config.post_action_delay)

    def clear_input(self):
        self.hotkey('ctrl', 'a')
        pyautogui.press('backspace')
        time.sleep(self.config.post_action_delay)

    def type_text(self, text: str):
        if self._should_use_clipboard(text):
            original = pyperclip.paste()
            pyperclip.copy(text)
            time.sleep(0.05)
            pyautogui.hotkey('ctrl', 'v')
            time.sleep(self.config.post_action_delay)
            pyperclip.copy(original)
            return
        pyautogui.write(text, interval=self.config.type_interval)
        time.sleep(self.config.post_action_delay)

    def _should_use_clipboard(self, text: str) -> bool:
        return self.config.use_clipboard_for_non_ascii and any(ord(ch) > 127 for ch in text)
