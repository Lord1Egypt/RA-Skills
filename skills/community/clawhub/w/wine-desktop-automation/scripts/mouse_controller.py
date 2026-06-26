import pyautogui
import time
from typing import Tuple, Optional
from ..utils.logger import get_logger
from ..utils.config import get_config

logger = get_logger(__name__)
config = get_config()


class MouseController:
    def __init__(self):
        self._setup_pyautogui()

    def _setup_pyautogui(self):
        pyautogui.PAUSE = config.get('MOUSE_DELAY', 0.1)
        pyautogui.FAILSAFE = True

    def move(self, x: int, y: int, duration: float = 0.5) -> None:
        pyautogui.moveTo(x, y, duration=duration)
        logger.debug(f'Mouse moved to ({x}, {y})')

    def move_relative(self, dx: int, dy: int, duration: float = 0.5) -> None:
        pyautogui.moveRel(dx, dy, duration=duration)
        logger.debug(f'Mouse moved relative by ({dx}, {dy})')

    def click(self, x: Optional[int] = None, y: Optional[int] = None, 
              button: str = 'left', clicks: int = 1, interval: float = 0.1) -> None:
        if x is not None and y is not None:
            self.move(x, y, duration=0.1)
        pyautogui.click(button=button, clicks=clicks, interval=interval)
        logger.debug(f'Mouse clicked: button={button}, clicks={clicks}')

    def double_click(self, x: Optional[int] = None, y: Optional[int] = None) -> None:
        if x is not None and y is not None:
            self.move(x, y, duration=0.1)
        pyautogui.doubleClick()
        logger.debug('Mouse double clicked')

    def right_click(self, x: Optional[int] = None, y: Optional[int] = None) -> None:
        if x is not None and y is not None:
            self.move(x, y, duration=0.1)
        pyautogui.rightClick()
        logger.debug('Mouse right clicked')

    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, 
             duration: float = 1.0, button: str = 'left') -> None:
        self.move(start_x, start_y, duration=0.1)
        pyautogui.dragTo(end_x, end_y, duration=duration, button=button)
        logger.debug(f'Mouse dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})')

    def drag_relative(self, dx: int, dy: int, duration: float = 1.0, 
                      button: str = 'left') -> None:
        pyautogui.dragRel(dx, dy, duration=duration, button=button)
        logger.debug(f'Mouse dragged relative by ({dx}, {dy})')

    def scroll(self, clicks: int, x: Optional[int] = None, y: Optional[int] = None) -> None:
        if x is not None and y is not None:
            self.move(x, y, duration=0.1)
        pyautogui.scroll(clicks)
        logger.debug(f'Mouse scrolled {clicks} clicks')

    def get_position(self) -> Tuple[int, int]:
        x, y = pyautogui.position()
        logger.debug(f'Current mouse position: ({x}, {y})')
        return x, y

    def on_screen(self, x: int, y: int) -> bool:
        return pyautogui.onScreen(x, y)


mouse = MouseController()
