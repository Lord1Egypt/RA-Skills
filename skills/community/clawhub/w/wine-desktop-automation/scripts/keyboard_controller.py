import pyautogui
import time
from typing import List
from ..utils.logger import get_logger
from ..utils.config import get_config

logger = get_logger(__name__)
config = get_config()


class KeyboardController:
    def __init__(self):
        self._setup_pyautogui()

    def _setup_pyautogui(self):
        pyautogui.PAUSE = config.get('KEYBOARD_DELAY', 0.05)

    def type(self, text: str, interval: float = 0.01) -> None:
        pyautogui.typewrite(text, interval=interval)
        logger.debug(f'Typed text: {text[:50]}...')

    def press(self, key: str, presses: int = 1, interval: float = 0.1) -> None:
        pyautogui.press(key, presses=presses, interval=interval)
        logger.debug(f'Pressed key: {key}')

    def hotkey(self, *keys: str) -> None:
        pyautogui.hotkey(*keys)
        logger.debug(f'Hotkey pressed: {"+".join(keys)}')

    def press_key(self, key: str) -> None:
        pyautogui.keyDown(key)
        logger.debug(f'Key pressed down: {key}')

    def release_key(self, key: str) -> None:
        pyautogui.keyUp(key)
        logger.debug(f'Key released: {key}')

    def write(self, text: str) -> None:
        self.type(text)

    def enter(self) -> None:
        self.press('enter')

    def tab(self) -> None:
        self.press('tab')

    def escape(self) -> None:
        self.press('esc')

    def space(self) -> None:
        self.press('space')

    def backspace(self, presses: int = 1) -> None:
        self.press('backspace', presses=presses)

    def delete(self, presses: int = 1) -> None:
        self.press('delete', presses=presses)

    def arrow_up(self, presses: int = 1) -> None:
        self.press('up', presses=presses)

    def arrow_down(self, presses: int = 1) -> None:
        self.press('down', presses=presses)

    def arrow_left(self, presses: int = 1) -> None:
        self.press('left', presses=presses)

    def arrow_right(self, presses: int = 1) -> None:
        self.press('right', presses=presses)

    def page_up(self, presses: int = 1) -> None:
        self.press('pgup', presses=presses)

    def page_down(self, presses: int = 1) -> None:
        self.press('pgdn', presses=presses)

    def home(self) -> None:
        self.press('home')

    def end(self) -> None:
        self.press('end')

    def copy(self) -> None:
        self.hotkey('ctrl', 'c')

    def paste(self) -> None:
        self.hotkey('ctrl', 'v')

    def cut(self) -> None:
        self.hotkey('ctrl', 'x')

    def select_all(self) -> None:
        self.hotkey('ctrl', 'a')

    def undo(self) -> None:
        self.hotkey('ctrl', 'z')

    def redo(self) -> None:
        self.hotkey('ctrl', 'y')

    def save(self) -> None:
        self.hotkey('ctrl', 's')

    def open(self) -> None:
        self.hotkey('ctrl', 'o')

    def new(self) -> None:
        self.hotkey('ctrl', 'n')

    def find(self) -> None:
        self.hotkey('ctrl', 'f')

    def print_screen(self) -> None:
        self.press('printscreen')

    def screenshot(self) -> None:
        self.hotkey('win', 'printscreen')

    def alt_tab(self) -> None:
        self.hotkey('alt', 'tab')

    def ctrl_alt_delete(self) -> None:
        self.hotkey('ctrl', 'alt', 'delete')

    def f1(self) -> None:
        self.press('f1')

    def f2(self) -> None:
        self.press('f2')

    def f3(self) -> None:
        self.press('f3')

    def f4(self) -> None:
        self.press('f4')

    def f5(self) -> None:
        self.press('f5')

    def f6(self) -> None:
        self.press('f6')

    def f7(self) -> None:
        self.press('f7')

    def f8(self) -> None:
        self.press('f8')

    def f9(self) -> None:
        self.press('f9')

    def f10(self) -> None:
        self.press('f10')

    def f11(self) -> None:
        self.press('f11')

    def f12(self) -> None:
        self.press('f12')


keyboard = KeyboardController()
