#!/usr/bin/env python3
"""
Scrcpy Controller Integration
Provides advanced device control through scrcpy server connection.
Supports real-time video streaming and direct control message injection.
"""

import socket
import struct
import threading
import time
import subprocess
import os
import re
from typing import Optional, Tuple, List, Callable, Dict, Any
from enum import IntEnum
from dataclasses import dataclass
import json


# ==================== Control Message Types ====================

class ControlMessageType(IntEnum):
    """Control message types matching scrcpy protocol."""
    INJECT_KEYCODE = 0
    INJECT_TEXT = 1
    INJECT_TOUCH_EVENT = 2
    INJECT_SCROLL_EVENT = 3
    BACK_OR_SCREEN_ON = 4
    EXPAND_NOTIFICATION_PANEL = 5
    EXPAND_SETTINGS_PANEL = 6
    COLLAPSE_PANELS = 7
    GET_CLIPBOARD = 8
    SET_CLIPBOARD = 9
    SET_DISPLAY_POWER = 10
    ROTATE_DEVICE = 11
    UHID_CREATE = 12
    UHID_INPUT = 13
    UHID_DESTROY = 14
    OPEN_HARD_KEYBOARD_SETTINGS = 15
    START_APP = 16
    RESET_VIDEO = 17


class KeyEventAction(IntEnum):
    """Android KeyEvent action constants."""
    ACTION_DOWN = 0
    ACTION_UP = 1
    ACTION_MULTIPLE = 2


class MotionEventAction(IntEnum):
    """Android MotionEvent action constants."""
    ACTION_DOWN = 0
    ACTION_UP = 1
    ACTION_MOVE = 2
    ACTION_CANCEL = 3
    ACTION_POINTER_DOWN = 5
    ACTION_POINTER_UP = 6
    ACTION_HOVER_MOVE = 7


class KeyCode(IntEnum):
    """Common Android KeyEvent codes."""
    KEYCODE_UNKNOWN = 0
    KEYCODE_HOME = 3
    KEYCODE_BACK = 4
    KEYCODE_CALL = 5
    KEYCODE_ENDCALL = 6
    KEYCODE_VOLUME_UP = 24
    KEYCODE_VOLUME_DOWN = 25
    KEYCODE_POWER = 26
    KEYCODE_CAMERA = 27
    KEYCODE_CLEAR = 28
    KEYCODE_MENU = 82
    KEYCODE_ENTER = 66
    KEYCODE_TAB = 61
    KEYCODE_DEL = 67  # Backspace
    KEYCODE_FORWARD_DEL = 112  # Delete
    KEYCODE_ESCAPE = 111
    KEYCODE_SPACE = 62
    KEYCODE_DPAD_UP = 19
    KEYCODE_DPAD_DOWN = 20
    KEYCODE_DPAD_LEFT = 21
    KEYCODE_DPAD_RIGHT = 22
    KEYCODE_DPAD_CENTER = 23
    KEYCODE_APP_SWITCH = 187
    KEYCODE_NOTIFICATION = 83


class MetaKey(IntEnum):
    """Android KeyEvent meta state constants."""
    META_NONE = 0
    META_ALT_ON = 2
    META_ALT_LEFT_ON = 16
    META_ALT_RIGHT_ON = 32
    META_SHIFT_ON = 1
    META_SHIFT_LEFT_ON = 64
    META_SHIFT_RIGHT_ON = 128
    META_SYM_ON = 4
    META_CTRL_ON = 4096
    META_CTRL_LEFT_ON = 8192
    META_CTRL_RIGHT_ON = 16384
    META_META_ON = 65536
    META_META_LEFT_ON = 131072
    META_META_RIGHT_ON = 262144


# ==================== Data Classes ====================

@dataclass
class Position:
    """Touch position with screen size context."""
    x: int
    y: int
    screen_width: int
    screen_height: int


@dataclass
class TouchPoint:
    """Single touch point for multi-touch."""
    pointer_id: int
    x: int
    y: int
    pressure: float = 1.0


# ==================== Scrcpy Controller ====================

class ScrcpyController:
    """
    Direct scrcpy server controller.
    Connects to the scrcpy server running on the device and sends control messages.
    """
    
    # Default ports
    DEFAULT_LOCAL_PORT_FIRST = 27183
    DEFAULT_LOCAL_PORT_LAST = 27199
    
    # Constants
    POINTER_ID_MOUSE = -1
    POINTER_ID_GENERIC_FINGER = -2
    POINTER_ID_VIRTUAL_FINGER = -3
    
    MAX_TEXT_LENGTH = 300
    MAX_CLIPBOARD_LENGTH = (1 << 18) - 14  # 256k - header
    
    def __init__(self, adb_path: str = "adb", device_id: Optional[str] = None,
                 scrcpy_server_path: Optional[str] = None):
        """
        Initialize scrcpy controller.
        
        Args:
            adb_path: Path to adb executable.
            device_id: Optional device serial number.
            scrcpy_server_path: Path to scrcpy-server.jar. If None, will try to find it.
        """
        self.adb_path = adb_path
        self.device_id = device_id
        self.scrcpy_server_path = scrcpy_server_path
        
        self.control_socket: Optional[socket.socket] = None
        self.video_socket: Optional[socket.socket] = None
        self.local_port: Optional[int] = None
        self.server_process: Optional[subprocess.Popen] = None
        
        self.screen_width: int = 1080
        self.screen_height: int = 1920
        
        self._is_connected = False
        self._receive_thread: Optional[threading.Thread] = None
    
    # ==================== Connection Management ====================
    
    def start_server(self, max_size: int = 0, bit_rate: int = 8000000,
                     max_fps: int = 0, display_id: int = 0) -> bool:
        """
        Start scrcpy server on the device.
        
        Args:
            max_size: Maximum video size (0 for unlimited).
            bit_rate: Video bit rate.
            max_fps: Maximum FPS (0 for unlimited).
            display_id: Display ID to mirror.
            
        Returns:
            True if server started successfully.
        """
        # Find server JAR
        if not self.scrcpy_server_path:
            # Try common locations
            possible_paths = [
                os.path.expanduser("~/.local/share/scrcpy/scrcpy-server"),
                "/usr/local/share/scrcpy/scrcpy-server",
                "/usr/share/scrcpy/scrcpy-server",
                "scrcpy-server.jar",
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    self.scrcpy_server_path = path
                    break
        
        if not self.scrcpy_server_path or not os.path.exists(self.scrcpy_server_path):
            print("Warning: scrcpy-server not found. Using ADB commands only.")
            return False
        
        # Push server to device
        cmd = [self.adb_path]
        if self.device_id:
            cmd.extend(["-s", self.device_id])
        cmd.extend(["push", self.scrcpy_server_path, "/data/local/tmp/scrcpy-server.jar"])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Failed to push server: {result.stderr}")
            return False
        
        # Start server on device
        server_cmd = (
            f"CLASSPATH=/data/local/tmp/scrcpy-server.jar "
            f"app_process / com.genymobile.scrcpy.Server "
            f"2.7 log_level=info max_size={max_size} bit_rate={bit_rate} "
            f"max_fps={max_fps} display_id={display_id} control=true audio=false"
        )
        
        cmd = [self.adb_path]
        if self.device_id:
            cmd.extend(["-s", self.device_id])
        cmd.extend(["shell", server_cmd])
        
        self.server_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        return True
    
    def connect(self, local_port: Optional[int] = None) -> bool:
        """
        Connect to the scrcpy server.
        
        Args:
            local_port: Local port for connection. If None, finds available port.
            
        Returns:
            True if connected successfully.
        """
        if local_port:
            self.local_port = local_port
        else:
            self.local_port = self._find_available_port()
        
        if not self.local_port:
            return False
        
        # Setup port forwarding
        cmd = [self.adb_path]
        if self.device_id:
            cmd.extend(["-s", self.device_id])
        cmd.extend(["forward", f"tcp:{self.local_port}", "localabstract:scrcpy"])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Failed to setup port forwarding: {result.stderr}")
            return False
        
        # Connect to server
        try:
            self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.control_socket.connect(("127.0.0.1", self.local_port))
            self._is_connected = True
            
            # Get device info (dummy socket first)
            self._read_device_info()
            
            return True
        except socket.error as e:
            print(f"Failed to connect: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the server."""
        self._is_connected = False
        
        if self.control_socket:
            self.control_socket.close()
            self.control_socket = None
        
        if self.server_process:
            self.server_process.terminate()
            self.server_process = None
        
        # Remove port forwarding
        if self.local_port:
            cmd = [self.adb_path]
            if self.device_id:
                cmd.extend(["-s", self.device_id])
            cmd.extend(["forward", "--remove", f"tcp:{self.local_port}"])
            subprocess.run(cmd, capture_output=True)
    
    def _find_available_port(self) -> Optional[int]:
        """Find an available local port."""
        for port in range(self.DEFAULT_LOCAL_PORT_FIRST, self.DEFAULT_LOCAL_PORT_LAST + 1):
            try:
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_socket.bind(("127.0.0.1", port))
                test_socket.close()
                return port
            except socket.error:
                continue
        return None
    
    def _read_device_info(self):
        """Read device info from server (dummy socket)."""
        # This would read the device name and screen size
        # For simplicity, we'll query via adb
        cmd = [self.adb_path]
        if self.device_id:
            cmd.extend(["-s", self.device_id])
        cmd.extend(["shell", "wm", "size"])
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        match = re.search(r'(\d+)x(\d+)', result.stdout)
        if match:
            self.screen_width = int(match.group(1))
            self.screen_height = int(match.group(2))
    
    @property
    def is_connected(self) -> bool:
        return self._is_connected
    
    # ==================== Control Message Building ====================
    
    def _send_message(self, data: bytes) -> bool:
        """Send raw control message."""
        if not self._is_connected or not self.control_socket:
            return False
        
        try:
            self.control_socket.sendall(data)
            return True
        except socket.error:
            return False
    
    def _build_keycode_message(self, action: int, keycode: int, 
                                 repeat: int = 0, metastate: int = 0) -> bytes:
        """Build inject keycode message."""
        # Format: type(1) + action(1) + keycode(4) + repeat(4) + metastate(4)
        return struct.pack(">BBIII", 
                          ControlMessageType.INJECT_KEYCODE,
                          action, keycode, repeat, metastate)
    
    def _build_text_message(self, text: str) -> bytes:
        """Build inject text message."""
        text_bytes = text.encode('utf-8')[:self.MAX_TEXT_LENGTH]
        length = len(text_bytes)
        # Format: type(1) + length(4) + text
        return struct.pack(">BI", ControlMessageType.INJECT_TEXT, length) + text_bytes
    
    def _build_touch_message(self, action: int, pointer_id: int,
                              position: Position, pressure: float,
                              action_button: int = 0, buttons: int = 0) -> bytes:
        """Build inject touch event message."""
        # Format: type(1) + action(1) + pointer_id(8) + position(4+4+4+4) + 
        #         pressure(4) + action_button(4) + buttons(4)
        return struct.pack(">BBqIIIIfII",
                          ControlMessageType.INJECT_TOUCH_EVENT,
                          action, pointer_id,
                          position.x, position.y,
                          position.screen_width, position.screen_height,
                          pressure, action_button, buttons)
    
    def _build_scroll_message(self, position: Position, 
                               hscroll: float, vscroll: float,
                               buttons: int = 0) -> bytes:
        """Build inject scroll event message."""
        return struct.pack(">BIIIIfII",
                          ControlMessageType.INJECT_SCROLL_EVENT,
                          position.x, position.y,
                          position.screen_width, position.screen_height,
                          hscroll, vscroll, buttons)
    
    def _build_back_or_screen_on_message(self, action: int) -> bytes:
        """Build back or screen on message."""
        return struct.pack(">BB", ControlMessageType.BACK_OR_SCREEN_ON, action)
    
    def _build_set_clipboard_message(self, text: str, paste: bool = False,
                                      sequence: int = 0) -> bytes:
        """Build set clipboard message."""
        text_bytes = text.encode('utf-8')[:self.MAX_CLIPBOARD_LENGTH]
        length = len(text_bytes)
        # Format: type(1) + sequence(8) + paste(1) + length(4) + text
        return struct.pack(">BQ?I", ControlMessageType.SET_CLIPBOARD, 
                          sequence, paste, length) + text_bytes
    
    def _build_start_app_message(self, name: str) -> bytes:
        """Build start app message."""
        name_bytes = name.encode('utf-8')
        length = len(name_bytes)
        return struct.pack(">BI", ControlMessageType.START_APP, length) + name_bytes
    
    # ==================== Public Control Methods ====================
    
    # Key Events
    def send_key(self, keycode: int, action: int = KeyEventAction.ACTION_DOWN,
                 metastate: int = 0) -> bool:
        """
        Send a key event.
        
        Args:
            keycode: Android KeyCode.
            action: KeyEvent action (DOWN, UP, or MULTIPLE).
            metastate: Meta key state (Alt, Ctrl, Shift, etc.).
            
        Returns:
            True if successful.
        """
        msg = self._build_keycode_message(action, keycode, 0, metastate)
        return self._send_message(msg)
    
    def press_key(self, keycode: int, metastate: int = 0) -> bool:
        """
        Press and release a key.
        
        Args:
            keycode: Android KeyCode.
            metastate: Meta key state.
            
        Returns:
            True if successful.
        """
        self.send_key(keycode, KeyEventAction.ACTION_DOWN, metastate)
        time.sleep(0.05)
        return self.send_key(keycode, KeyEventAction.ACTION_UP, metastate)
    
    def press_home(self) -> bool:
        """Press HOME button."""
        return self.press_key(KeyCode.KEYCODE_HOME)
    
    def press_back(self) -> bool:
        """Press BACK button."""
        return self.press_key(KeyCode.KEYCODE_BACK)
    
    def press_menu(self) -> bool:
        """Press MENU button."""
        return self.press_key(KeyCode.KEYCODE_MENU)
    
    def press_power(self) -> bool:
        """Press POWER button."""
        return self.press_key(KeyCode.KEYCODE_POWER)
    
    def press_enter(self) -> bool:
        """Press ENTER button."""
        return self.press_key(KeyCode.KEYCODE_ENTER)
    
    def press_tab(self) -> bool:
        """Press TAB button."""
        return self.press_key(KeyCode.KEYCODE_TAB)
    
    def press_delete(self) -> bool:
        """Press DELETE (backspace) button."""
        return self.press_key(KeyCode.KEYCODE_DEL)
    
    def press_volume_up(self) -> bool:
        """Press VOLUME UP."""
        return self.press_key(KeyCode.KEYCODE_VOLUME_UP)
    
    def press_volume_down(self) -> bool:
        """Press VOLUME DOWN."""
        return self.press_key(KeyCode.KEYCODE_VOLUME_DOWN)
    
    def dpad_up(self) -> bool:
        """Press DPAD UP."""
        return self.press_key(KeyCode.KEYCODE_DPAD_UP)
    
    def dpad_down(self) -> bool:
        """Press DPAD DOWN."""
        return self.press_key(KeyCode.KEYCODE_DPAD_DOWN)
    
    def dpad_left(self) -> bool:
        """Press DPAD LEFT."""
        return self.press_key(KeyCode.KEYCODE_DPAD_LEFT)
    
    def dpad_right(self) -> bool:
        """Press DPAD RIGHT."""
        return self.press_key(KeyCode.KEYCODE_DPAD_RIGHT)
    
    # Text Input
    def input_text(self, text: str) -> bool:
        """
        Input text.
        
        Args:
            text: Text to input.
            
        Returns:
            True if successful.
        """
        msg = self._build_text_message(text)
        return self._send_message(msg)
    
    # Touch Events
    def tap(self, x: int, y: int, duration_ms: int = 100) -> bool:
        """
        Tap at coordinates.
        
        Args:
            x: X coordinate.
            y: Y coordinate.
            duration_ms: Duration of tap.
            
        Returns:
            True if successful.
        """
        position = Position(x, y, self.screen_width, self.screen_height)
        
        # Touch down
        msg = self._build_touch_message(
            MotionEventAction.ACTION_DOWN,
            self.POINTER_ID_GENERIC_FINGER,
            position, 1.0
        )
        self._send_message(msg)
        
        time.sleep(duration_ms / 1000.0)
        
        # Touch up
        msg = self._build_touch_message(
            MotionEventAction.ACTION_UP,
            self.POINTER_ID_GENERIC_FINGER,
            position, 0.0
        )
        return self._send_message(msg)
    
    def long_press(self, x: int, y: int, duration_ms: int = 1000) -> bool:
        """
        Long press at coordinates.
        
        Args:
            x: X coordinate.
            y: Y coordinate.
            duration_ms: Duration of press.
            
        Returns:
            True if successful.
        """
        return self.tap(x, y, duration_ms)
    
    def swipe(self, start_x: int, start_y: int, 
              end_x: int, end_y: int, duration_ms: int = 300) -> bool:
        """
        Swipe from one point to another.
        
        Args:
            start_x: Starting X coordinate.
            start_y: Starting Y coordinate.
            end_x: Ending X coordinate.
            end_y: Ending Y coordinate.
            duration_ms: Duration of swipe.
            
        Returns:
            True if successful.
        """
        steps = max(10, duration_ms // 20)  # 20ms per step
        dx = (end_x - start_x) / steps
        dy = (end_y - start_y) / steps
        
        # Touch down
        position = Position(start_x, start_y, self.screen_width, self.screen_height)
        msg = self._build_touch_message(
            MotionEventAction.ACTION_DOWN,
            self.POINTER_ID_GENERIC_FINGER,
            position, 1.0
        )
        self._send_message(msg)
        
        # Move
        for i in range(1, steps + 1):
            x = int(start_x + dx * i)
            y = int(start_y + dy * i)
            position = Position(x, y, self.screen_width, self.screen_height)
            msg = self._build_touch_message(
                MotionEventAction.ACTION_MOVE,
                self.POINTER_ID_GENERIC_FINGER,
                position, 1.0
            )
            self._send_message(msg)
            time.sleep(0.02)
        
        # Touch up
        position = Position(end_x, end_y, self.screen_width, self.screen_height)
        msg = self._build_touch_message(
            MotionEventAction.ACTION_UP,
            self.POINTER_ID_GENERIC_FINGER,
            position, 0.0
        )
        return self._send_message(msg)
    
    def scroll(self, x: int, y: int, 
               hscroll: float = 0, vscroll: float = -1.0) -> bool:
        """
        Scroll at coordinates.
        
        Args:
            x: X coordinate.
            y: Y coordinate.
            hscroll: Horizontal scroll amount (-1.0 to 1.0).
            vscroll: Vertical scroll amount (-1.0 to 1.0).
            
        Returns:
            True if successful.
        """
        position = Position(x, y, self.screen_width, self.screen_height)
        msg = self._build_scroll_message(position, hscroll, vscroll)
        return self._send_message(msg)
    
    def scroll_up(self, x: int = None, y: int = None) -> bool:
        """Scroll up."""
        if x is None:
            x = self.screen_width // 2
        if y is None:
            y = self.screen_height // 2
        return self.scroll(x, y, 0, -1.0)
    
    def scroll_down(self, x: int = None, y: int = None) -> bool:
        """Scroll down."""
        if x is None:
            x = self.screen_width // 2
        if y is None:
            y = self.screen_height // 2
        return self.scroll(x, y, 0, 1.0)
    
    # System Controls
    def expand_notifications(self) -> bool:
        """Expand notification panel."""
        msg = struct.pack(">B", ControlMessageType.EXPAND_NOTIFICATION_PANEL)
        return self._send_message(msg)
    
    def expand_settings(self) -> bool:
        """Expand settings panel."""
        msg = struct.pack(">B", ControlMessageType.EXPAND_SETTINGS_PANEL)
        return self._send_message(msg)
    
    def collapse_panels(self) -> bool:
        """Collapse all panels."""
        msg = struct.pack(">B", ControlMessageType.COLLAPSE_PANELS)
        return self._send_message(msg)
    
    def rotate_device(self) -> bool:
        """Rotate device screen."""
        msg = struct.pack(">B", ControlMessageType.ROTATE_DEVICE)
        return self._send_message(msg)
    
    def set_display_power(self, on: bool) -> bool:
        """Set display power state."""
        msg = struct.pack(">BB", ControlMessageType.SET_DISPLAY_POWER, 1 if on else 0)
        return self._send_message(msg)
    
    def turn_screen_off(self) -> bool:
        """Turn screen off."""
        return self.set_display_power(False)
    
    def turn_screen_on(self) -> bool:
        """Turn screen on."""
        return self.set_display_power(True)
    
    def back_or_screen_on(self, action: int = KeyEventAction.ACTION_DOWN) -> bool:
        """
        Send BACK or turn screen on if off.
        
        Args:
            action: KeyEvent action.
            
        Returns:
            True if successful.
        """
        msg = self._build_back_or_screen_on_message(action)
        result = self._send_message(msg)
        if action == KeyEventAction.ACTION_DOWN:
            time.sleep(0.05)
            self._send_message(self._build_back_or_screen_on_message(KeyEventAction.ACTION_UP))
        return result
    
    def open_keyboard_settings(self) -> bool:
        """Open hard keyboard settings."""
        msg = struct.pack(">B", ControlMessageType.OPEN_HARD_KEYBOARD_SETTINGS)
        return self._send_message(msg)
    
    def start_app(self, package: str) -> bool:
        """
        Start an application.
        
        Args:
            package: Package name or search name (prefix with ? for search).
            
        Returns:
            True if successful.
        """
        msg = self._build_start_app_message(package)
        return self._send_message(msg)
    
    def reset_video(self) -> bool:
        """Reset video capture."""
        msg = struct.pack(">B", ControlMessageType.RESET_VIDEO)
        return self._send_message(msg)
    
    # Clipboard
    def set_clipboard(self, text: str, paste: bool = False) -> bool:
        """
        Set clipboard text.
        
        Args:
            text: Text to set.
            paste: Also paste after setting.
            
        Returns:
            True if successful.
        """
        msg = self._build_set_clipboard_message(text, paste)
        return self._send_message(msg)
    
    # Multi-touch (Advanced)
    def multi_touch(self, points: List[TouchPoint], action: int) -> bool:
        """
        Perform multi-touch operation.
        
        Args:
            points: List of touch points.
            action: MotionEvent action.
            
        Returns:
            True if successful.
        """
        for point in points:
            position = Position(point.x, point.y, self.screen_width, self.screen_height)
            msg = self._build_touch_message(
                action, point.pointer_id, position, point.pressure
            )
            self._send_message(msg)
        return True
    
    def pinch(self, center_x: int, center_y: int, 
              start_distance: int = 200, end_distance: int = 50) -> bool:
        """
        Perform pinch gesture.
        
        Args:
            center_x: Center X coordinate.
            center_y: Center Y coordinate.
            start_distance: Initial finger distance.
            end_distance: Final finger distance.
            
        Returns:
            True if successful.
        """
        # This is a simplified pinch simulation
        steps = 20
        for i in range(steps + 1):
            ratio = i / steps
            distance = start_distance + (end_distance - start_distance) * ratio
            half_dist = distance // 2
            
            # Two finger positions
            points = [
                TouchPoint(0, center_x - half_dist, center_y),
                TouchPoint(1, center_x + half_dist, center_y)
            ]
            
            action = MotionEventAction.ACTION_DOWN if i == 0 else \
                    (MotionEventAction.ACTION_UP if i == steps else MotionEventAction.ACTION_MOVE)
            
            self.multi_touch(points, action)
            time.sleep(0.02)
        
        return True


# ==================== Context Manager ====================

class ScrcpySession:
    """Context manager for scrcpy session."""
    
    def __init__(self, controller: ScrcpyController):
        self.controller = controller
    
    def __enter__(self):
        self.controller.start_server()
        self.controller.connect()
        return self.controller
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.controller.disconnect()


# ==================== CLI Interface ====================

def main():
    """CLI interface for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Scrcpy Controller')
    parser.add_argument('--device', '-d', help='Device serial number')
    parser.add_argument('--tap', nargs=2, type=int, metavar=('X', 'Y'), help='Tap')
    parser.add_argument('--swipe', nargs=4, type=int, metavar=('X1', 'Y1', 'X2', 'Y2'), help='Swipe')
    parser.add_argument('--home', action='store_true', help='Press HOME')
    parser.add_argument('--back', action='store_true', help='Press BACK')
    parser.add_argument('--text', '-t', help='Input text')
    
    args = parser.parse_args()
    
    controller = ScrcpyController(device_id=args.device)
    
    try:
        print("Starting scrcpy server...")
        controller.start_server()
        
        print("Connecting...")
        if controller.connect():
            print("Connected!")
            
            if args.tap:
                controller.tap(*args.tap)
                print(f"Tapped at ({args.tap[0]}, {args.tap[1]})")
            
            if args.swipe:
                controller.swipe(*args.swipe)
                print(f"Swiped")
            
            if args.home:
                controller.press_home()
                print("Pressed HOME")
            
            if args.back:
                controller.press_back()
                print("Pressed BACK")
            
            if args.text:
                controller.input_text(args.text)
                print(f"Input text: {args.text}")
        else:
            print("Failed to connect")
    finally:
        controller.disconnect()


if __name__ == '__main__':
    main()
