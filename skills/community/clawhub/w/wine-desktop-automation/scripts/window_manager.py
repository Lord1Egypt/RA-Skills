import subprocess
import time
import re
from typing import List, Optional, Tuple
from dataclasses import dataclass
from ..utils.logger import get_logger
from ..utils.config import get_config

logger = get_logger(__name__)
config = get_config()


@dataclass
class WindowInfo:
    window_id: str
    title: str
    class_name: str
    position: Tuple[int, int]
    size: Tuple[int, int]
    desktop: int

    def __repr__(self):
        return f'WindowInfo(id={self.window_id}, title="{self.title}", class="{self.class_name}")'


class WindowManager:
    def __init__(self):
        self._check_xdotool()

    def _check_xdotool(self):
        try:
            subprocess.run(['xdotool', '--version'], 
                         capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error('xdotool not found. Please install it with: sudo apt-get install xdotool')
            raise RuntimeError('xdotool is required but not installed')

    def _run_xdotool(self, args: List[str]) -> str:
        try:
            result = subprocess.run(['xdotool'] + args, 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            logger.error(f'xdotool command failed: {e}')
            logger.error(f'Error output: {e.stderr}')
            return ''

    def list_windows(self) -> List[WindowInfo]:
        windows = []
        output = self._run_xdotool(['search', '--onlyvisible', '--name', '.*'])
        
        if not output:
            return windows

        window_ids = output.split('\n')
        for window_id in window_ids:
            if not window_id.strip():
                continue
            
            try:
                title = self._run_xdotool(['getwindowname', window_id])
                class_name = self._run_xdotool(['getwindowclassname', window_id])
                geometry = self._run_xdotool(['getwindowgeometry', window_id])
                
                pos_match = re.search(r'Position: (\d+),(\d+)', geometry)
                size_match = re.search(r'Geometry: (\d+)x(\d+)', geometry)
                
                if pos_match and size_match:
                    position = (int(pos_match.group(1)), int(pos_match.group(2)))
                    size = (int(size_match.group(1)), int(size_match.group(2)))
                    
                    window_info = WindowInfo(
                        window_id=window_id,
                        title=title,
                        class_name=class_name,
                        position=position,
                        size=size,
                        desktop=0
                    )
                    windows.append(window_info)
                    
            except Exception as e:
                logger.warning(f'Failed to get info for window {window_id}: {e}')
                continue

        return windows

    def find_window(self, title_pattern: str, fuzzy: bool = True) -> Optional[WindowInfo]:
        windows = self.list_windows()
        
        for window in windows:
            if fuzzy:
                if title_pattern.lower() in window.title.lower():
                    logger.info(f'Found window: {window}')
                    return window
            else:
                if window.title == title_pattern:
                    logger.info(f'Found window: {window}')
                    return window
        
        logger.warning(f'Window not found: {title_pattern}')
        return None

    def activate(self, title_pattern: str, fuzzy: bool = True) -> bool:
        window = self.find_window(title_pattern, fuzzy)
        if window:
            self._run_xdotool(['windowactivate', window.window_id])
            time.sleep(0.2)
            logger.info(f'Activated window: {window.title}')
            return True
        return False

    def minimize(self, title_pattern: str, fuzzy: bool = True) -> bool:
        window = self.find_window(title_pattern, fuzzy)
        if window:
            self._run_xdotool(['windowminimize', window.window_id])
            logger.info(f'Minimized window: {window.title}')
            return True
        return False

    def maximize(self, title_pattern: str, fuzzy: bool = True) -> bool:
        window = self.find_window(title_pattern, fuzzy)
        if window:
            self._run_xdotool(['windowmaximize', window.window_id])
            logger.info(f'Maximized window: {window.title}')
            return True
        return False

    def restore(self, title_pattern: str, fuzzy: bool = True) -> bool:
        window = self.find_window(title_pattern, fuzzy)
        if window:
            self._run_xdotool(['windowmap', window.window_id])
            self.activate(title_pattern, fuzzy)
            logger.info(f'Restored window: {window.title}')
            return True
        return False

    def close(self, title_pattern: str, fuzzy: bool = True) -> bool:
        window = self.find_window(title_pattern, fuzzy)
        if window:
            self._run_xdotool(['windowclose', window.window_id])
            logger.info(f'Closed window: {window.title}')
            return True
        return False

    def kill(self, title_pattern: str, fuzzy: bool = True) -> bool:
        window = self.find_window(title_pattern, fuzzy)
        if window:
            self._run_xdotool(['windowkill', window.window_id])
            logger.info(f'Killed window: {window.title}')
            return True
        return False

    def get_position(self, title_pattern: str, fuzzy: bool = True) -> Optional[Tuple[int, int]]:
        window = self.find_window(title_pattern, fuzzy)
        if window:
            return window.position
        return None

    def get_size(self, title_pattern: str, fuzzy: bool = True) -> Optional[Tuple[int, int]]:
        window = self.find_window(title_pattern, fuzzy)
        if window:
            return window.size
        return None

    def get_geometry(self, title_pattern: str, fuzzy: bool = True) -> Optional[Tuple[int, int, int, int]]:
        window = self.find_window(title_pattern, fuzzy)
        if window:
            x, y = window.position
            width, height = window.size
            return (x, y, width, height)
        return None

    def move_window(self, title_pattern: str, x: int, y: int, 
                   fuzzy: bool = True) -> bool:
        window = self.find_window(title_pattern, fuzzy)
        if window:
            self._run_xdotool(['windowmove', window.window_id, str(x), str(y)])
            logger.info(f'Moved window {window.title} to ({x}, {y})')
            return True
        return False

    def resize_window(self, title_pattern: str, width: int, height: int,
                     fuzzy: bool = True) -> bool:
        window = self.find_window(title_pattern, fuzzy)
        if window:
            self._run_xdotool(['windowsize', window.window_id, str(width), str(height)])
            logger.info(f'Resized window {window.title} to {width}x{height}')
            return True
        return False

    def focus_window(self, window_id: str) -> bool:
        try:
            self._run_xdotool(['windowfocus', window_id])
            return True
        except Exception as e:
            logger.error(f'Failed to focus window {window_id}: {e}')
            return False

    def get_active_window(self) -> Optional[WindowInfo]:
        try:
            window_id = self._run_xdotool(['getactivewindow'])
            if window_id:
                title = self._run_xdotool(['getwindowname', window_id])
                class_name = self._run_xdotool(['getwindowclassname', window_id])
                geometry = self._run_xdotool(['getwindowgeometry', window_id])
                
                pos_match = re.search(r'Position: (\d+),(\d+)', geometry)
                size_match = re.search(r'Geometry: (\d+)x(\d+)', geometry)
                
                if pos_match and size_match:
                    position = (int(pos_match.group(1)), int(pos_match.group(2)))
                    size = (int(size_match.group(1)), int(size_match.group(2)))
                    
                    return WindowInfo(
                        window_id=window_id,
                        title=title,
                        class_name=class_name,
                        position=position,
                        size=size,
                        desktop=0
                    )
        except Exception as e:
            logger.error(f'Failed to get active window: {e}')
        
        return None

    def wait_for_window(self, title_pattern: str, timeout: int = 10, 
                       fuzzy: bool = True) -> Optional[WindowInfo]:
        start_time = time.time()
        while time.time() - start_time < timeout:
            window = self.find_window(title_pattern, fuzzy)
            if window:
                return window
            time.sleep(0.5)
        
        logger.warning(f'Timeout waiting for window: {title_pattern}')
        return None


window = WindowManager()
