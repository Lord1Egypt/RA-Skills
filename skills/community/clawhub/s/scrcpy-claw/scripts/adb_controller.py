#!/usr/bin/env python3
"""
Android Device Controller via ADB
Provides comprehensive device control capabilities through ADB commands.
"""

import subprocess
import json
import time
import os
import re
from typing import List, Tuple, Optional, Dict, Any


class ADBController:
    """
    ADB-based Android device controller.
    Provides methods for touch, keyboard, system control, and device info.
    """
    
    def __init__(self, device_id: Optional[str] = None, adb_path: str = "adb"):
        """
        Initialize ADB controller.
        
        Args:
            device_id: Optional device serial number. If None, uses the first connected device.
            adb_path: Path to adb executable. Defaults to 'adb' (assumes in PATH).
        """
        self.adb_path = adb_path
        self.device_id = device_id
        self._verify_adb()
        
    def _verify_adb(self) -> None:
        """Verify ADB is available and device is connected."""
        try:
            result = subprocess.run(
                [self.adb_path, "devices"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if "devices" not in result.stdout:
                raise RuntimeError("ADB not found. Please ensure ADB is installed and in PATH.")
        except FileNotFoundError:
            raise RuntimeError(f"ADB executable not found at: {self.adb_path}")
    
    def _run_adb(self, args: List[str], timeout: int = 30) -> Tuple[int, str, str]:
        """
        Execute ADB command and return result.
        
        Args:
            args: Arguments to pass to adb.
            timeout: Command timeout in seconds.
            
        Returns:
            Tuple of (return_code, stdout, stderr).
        """
        cmd = [self.adb_path]
        if self.device_id:
            cmd.extend(["-s", self.device_id])
        cmd.extend(args)
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    
    # ==================== Device Information ====================
    
    def get_device_info(self) -> Dict[str, Any]:
        """Get comprehensive device information."""
        info = {}
        
        # Get device properties
        _, props, _ = self._run_adb(["shell", "getprop"])
        for line in props.strip().split('\n'):
            match = re.match(r'\[([^\]]+)\]: \[([^\]]*)\]', line)
            if match:
                key, value = match.groups()
                info[key] = value
        
        # Get screen resolution
        _, size, _ = self._run_adb(["shell", "wm", "size"])
        if "Physical size:" in size:
            info['screen_size'] = size.split("Physical size:")[1].strip()
        
        # Get screen density
        _, density, _ = self._run_adb(["shell", "wm", "density"])
        if "Physical density:" in density:
            info['screen_density'] = density.split("Physical density:")[1].strip()
        
        return info
    
    def get_screen_size(self) -> Tuple[int, int]:
        """Get screen resolution as (width, height)."""
        _, output, _ = self._run_adb(["shell", "wm", "size"])
        match = re.search(r'(\d+)x(\d+)', output)
        if match:
            return int(match.group(1)), int(match.group(2))
        return 1080, 1920  # Default fallback
    
    def list_devices(self) -> List[Dict[str, str]]:
        """List all connected devices."""
        _, output, _ = self._run_adb(["devices", "-l"])
        devices = []
        for line in output.strip().split('\n')[1:]:
            if line.strip():
                parts = line.split()
                if len(parts) >= 2:
                    devices.append({
                        'id': parts[0],
                        'status': parts[1],
                        'info': ' '.join(parts[2:]) if len(parts) > 2 else ''
                    })
        return devices
    
    def screenshot(self, output_path: str = None) -> Optional[str]:
        """
        Take a screenshot.
        
        Args:
            output_path: Local path to save screenshot. If None, saves to temp.
            
        Returns:
            Path to the saved screenshot file.
        """
        if output_path is None:
            output_path = os.path.join(os.getcwd(), f"screenshot_{int(time.time())}.png")
        
        # Take screenshot on device
        self._run_adb(["shell", "screencap", "-p", "/sdcard/screenshot_temp.png"])
        # Pull to local
        self._run_adb(["pull", "/sdcard/screenshot_temp.png", output_path])
        # Clean up
        self._run_adb(["shell", "rm", "/sdcard/screenshot_temp.png"])
        
        return output_path
    
    # ==================== Touch Operations ====================
    
    def tap(self, x: int, y: int, duration_ms: int = 100) -> bool:
        """
        Tap at specified coordinates.
        
        Args:
            x: X coordinate.
            y: Y coordinate.
            duration_ms: Duration of tap in milliseconds.
            
        Returns:
            True if successful.
        """
        cmd = ["shell", "input", "tap", str(x), str(y)]
        # Note: duration is not directly supported by 'input tap'
        # For duration, we use swipe from point to same point
        if duration_ms > 100:
            cmd = ["shell", "input", "swipe", str(x), str(y), str(x), str(y), str(duration_ms)]
        
        ret, _, _ = self._run_adb(cmd)
        return ret == 0
    
    def double_tap(self, x: int, y: int, interval_ms: int = 100) -> bool:
        """
        Double tap at specified coordinates.
        
        Args:
            x: X coordinate.
            y: Y coordinate.
            interval_ms: Interval between taps.
            
        Returns:
            True if successful.
        """
        self.tap(x, y)
        time.sleep(interval_ms / 1000.0)
        return self.tap(x, y)
    
    def long_press(self, x: int, y: int, duration_ms: int = 1000) -> bool:
        """
        Long press at specified coordinates.
        
        Args:
            x: X coordinate.
            y: Y coordinate.
            duration_ms: Duration of press.
            
        Returns:
            True if successful.
        """
        cmd = ["shell", "input", "swipe", str(x), str(y), str(x), str(y), str(duration_ms)]
        ret, _, _ = self._run_adb(cmd)
        return ret == 0
    
    def swipe(self, start_x: int, start_y: int, end_x: int, end_y: int, 
              duration_ms: int = 300) -> bool:
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
        cmd = ["shell", "input", "swipe", 
               str(start_x), str(start_y), str(end_x), str(end_y), str(duration_ms)]
        ret, _, _ = self._run_adb(cmd)
        return ret == 0
    
    def swipe_direction(self, direction: str, distance_ratio: float = 0.5) -> bool:
        """
        Swipe in a direction.
        
        Args:
            direction: One of 'up', 'down', 'left', 'right'.
            distance_ratio: Ratio of screen size to swipe (0.0-1.0).
            
        Returns:
            True if successful.
        """
        width, height = self.get_screen_size()
        center_x, center_y = width // 2, height // 2
        distance = int(min(width, height) * distance_ratio)
        
        directions = {
            'up': (center_x, center_y + distance // 2, center_x, center_y - distance // 2),
            'down': (center_x, center_y - distance // 2, center_x, center_y + distance // 2),
            'left': (center_x + distance // 2, center_y, center_x - distance // 2, center_y),
            'right': (center_x - distance // 2, center_y, center_x + distance // 2, center_y)
        }
        
        if direction.lower() not in directions:
            raise ValueError(f"Invalid direction: {direction}. Use 'up', 'down', 'left', or 'right'.")
        
        sx, sy, ex, ey = directions[direction.lower()]
        return self.swipe(sx, sy, ex, ey)
    
    def pinch(self, center_x: int, center_y: int, 
              start_distance: int = 200, end_distance: int = 50) -> bool:
        """
        Perform pinch gesture (zoom).
        Note: This is simulated and may not work perfectly on all apps.
        
        Args:
            center_x: Center X coordinate.
            center_y: Center Y coordinate.
            start_distance: Initial finger distance.
            end_distance: Final finger distance.
            
        Returns:
            True if successful.
        """
        # Simulate pinch with multiple swipes (limited by ADB capabilities)
        # For true multi-touch, consider using scrcpy control interface
        print("Note: Pinch via ADB is simulated. For better results, use scrcpy integration.")
        
        # Approximate with center swipe
        self.swipe(
            center_x - start_distance // 2, center_y,
            center_x - end_distance // 2, center_y, 300
        )
        return True
    
    # ==================== Keyboard Operations ====================
    
    def input_text(self, text: str) -> bool:
        """
        Input text (supports spaces and special characters).
        
        Args:
            text: Text to input.
            
        Returns:
            True if successful.
        """
        # Escape special characters for shell
        escaped = text.replace(' ', '%s').replace('&', '\\&').replace('(', '\\(').replace(')', '\\)')
        cmd = ["shell", "input", "text", escaped]
        ret, _, _ = self._run_adb(cmd)
        return ret == 0
    
    def keyevent(self, keycode: int) -> bool:
        """
        Send key event.
        
        Args:
            keycode: Android KeyEvent code.
            
        Returns:
            True if successful.
        """
        cmd = ["shell", "input", "keyevent", str(keycode)]
        ret, _, _ = self._run_adb(cmd)
        return ret == 0
    
    # Common keycodes
    KEYCODE_HOME = 3
    KEYCODE_BACK = 4
    KEYCODE_MENU = 82
    KEYCODE_POWER = 26
    KEYCODE_VOLUME_UP = 24
    KEYCODE_VOLUME_DOWN = 25
    KEYCODE_VOLUME_MUTE = 164
    KEYCODE_ENTER = 66
    KEYCODE_TAB = 61
    KEYCODE_ESCAPE = 111
    KEYCODE_DELETE = 67
    KEYCODE_APP_SWITCH = 187
    KEYCODE_NOTIFICATION = 83
    
    def press_home(self) -> bool:
        """Press HOME button."""
        return self.keyevent(self.KEYCODE_HOME)
    
    def press_back(self) -> bool:
        """Press BACK button."""
        return self.keyevent(self.KEYCODE_BACK)
    
    def press_menu(self) -> bool:
        """Press MENU button."""
        return self.keyevent(self.KEYCODE_MENU)
    
    def press_power(self) -> bool:
        """Press POWER button."""
        return self.keyevent(self.KEYCODE_POWER)
    
    def press_enter(self) -> bool:
        """Press ENTER button."""
        return self.keyevent(self.KEYCODE_ENTER)
    
    def volume_up(self) -> bool:
        """Press VOLUME UP."""
        return self.keyevent(self.KEYCODE_VOLUME_UP)
    
    def volume_down(self) -> bool:
        """Press VOLUME DOWN."""
        return self.keyevent(self.KEYCODE_VOLUME_DOWN)
    
    def open_app_switch(self) -> bool:
        """Open app switcher (recent apps)."""
        return self.keyevent(self.KEYCODE_APP_SWITCH)
    
    # ==================== System Operations ====================
    
    def open_url(self, url: str) -> bool:
        """
        Open URL in browser.
        
        Args:
            url: URL to open.
            
        Returns:
            True if successful.
        """
        cmd = ["shell", "am", "start", "-a", "android.intent.action.VIEW", "-d", url]
        ret, _, _ = self._run_adb(cmd)
        return ret == 0
    
    def start_app(self, package: str, activity: str = None) -> bool:
        """
        Start an application.
        
        Args:
            package: Package name (e.g., 'com.android.settings').
            activity: Optional activity name. If None, launches main activity.
            
        Returns:
            True if successful.
        """
        if activity:
            cmd = ["shell", "am", "start", "-n", f"{package}/{activity}"]
        else:
            cmd = ["shell", "monkey", "-p", package, "-c", "android.intent.category.LAUNCHER", "1"]
        ret, _, _ = self._run_adb(cmd)
        return ret == 0
    
    def force_stop(self, package: str) -> bool:
        """
        Force stop an application.
        
        Args:
            package: Package name.
            
        Returns:
            True if successful.
        """
        cmd = ["shell", "am", "force-stop", package]
        ret, _, _ = self._run_adb(cmd)
        return ret == 0
    
    def clear_app_data(self, package: str) -> bool:
        """
        Clear application data.
        
        Args:
            package: Package name.
            
        Returns:
            True if successful.
        """
        cmd = ["shell", "pm", "clear", package]
        ret, _, _ = self._run_adb(cmd)
        return ret == 0
    
    def list_packages(self) -> List[str]:
        """
        List all installed packages.
        
        Returns:
            List of package names.
        """
        _, output, _ = self._run_adb(["shell", "pm", "list", "packages"])
        packages = []
        for line in output.strip().split('\n'):
            if line.startswith('package:'):
                packages.append(line.replace('package:', ''))
        return packages
    
    def get_current_app(self) -> Dict[str, str]:
        """
        Get current foreground app info.
        
        Returns:
            Dictionary with 'package' and 'activity' keys.
        """
        _, output, _ = self._run_adb(["shell", "dumpsys", "activity", "activities", "|", "grep", "mResumedActivity"])
        # Alternative method
        _, output, _ = self._run_adb(["shell", "dumpsys", "activity", "top"])
        
        result = {'package': '', 'activity': ''}
        for line in output.split('\n'):
            if 'ACTIVITY' in line:
                match = re.search(r'(\S+)/(\S+)', line)
                if match:
                    result['package'] = match.group(1)
                    result['activity'] = match.group(2)
                    break
        return result
    
    def set_clipboard(self, text: str) -> bool:
        """
        Set clipboard text.
        
        Args:
            text: Text to set.
            
        Returns:
            True if successful.
        """
        # Using service call (works on most devices)
        cmd = ["shell", "am", "broadcast", "-a", "clipper.set", "-e", "text", text]
        ret, _, _ = self._run_adb(cmd)
        return ret == 0
    
    def get_clipboard(self) -> str:
        """
        Get clipboard text.
        Note: This is limited and may not work on all devices/Android versions.
        
        Returns:
            Clipboard text or empty string.
        """
        _, output, _ = self._run_adb(["shell", "am", "broadcast", "-a", "clipper.get"])
        return output
    
    def expand_notifications(self) -> bool:
        """Expand notification panel."""
        return self.keyevent(self.KEYCODE_NOTIFICATION)
    
    def collapse_notifications(self) -> bool:
        """Collapse notification panel."""
        return self.keyevent(4)  # BACK
    
    # ==================== File Operations ====================
    
    def push_file(self, local_path: str, remote_path: str) -> bool:
        """
        Push file to device.
        
        Args:
            local_path: Local file path.
            remote_path: Remote path on device.
            
        Returns:
            True if successful.
        """
        cmd = ["push", local_path, remote_path]
        ret, _, _ = self._run_adb(cmd)
        return ret == 0
    
    def pull_file(self, remote_path: str, local_path: str) -> bool:
        """
        Pull file from device.
        
        Args:
            remote_path: Remote path on device.
            local_path: Local file path.
            
        Returns:
            True if successful.
        """
        cmd = ["pull", remote_path, local_path]
        ret, _, _ = self._run_adb(cmd)
        return ret == 0
    
    def install_apk(self, apk_path: str) -> bool:
        """
        Install APK file.
        
        Args:
            apk_path: Path to APK file.
            
        Returns:
            True if successful.
        """
        cmd = ["install", "-r", apk_path]  # -r for reinstall
        ret, _, _ = self._run_adb(cmd)
        return ret == 0
    
    def uninstall(self, package: str) -> bool:
        """
        Uninstall package.
        
        Args:
            package: Package name.
            
        Returns:
            True if successful.
        """
        cmd = ["uninstall", package]
        ret, _, _ = self._run_adb(cmd)
        return ret == 0
    
    # ==================== Network Operations ====================
    
    def connect_wifi(self, ip_port: str) -> bool:
        """
        Connect to device over WiFi.
        
        Args:
            ip_port: IP:Port (e.g., '192.168.1.100:5555').
            
        Returns:
            True if successful.
        """
        cmd = ["connect", ip_port]
        ret, _, _ = self._run_adb(cmd)
        return ret == 0
    
    def disconnect_wifi(self, ip_port: str = None) -> bool:
        """
        Disconnect from WiFi device.
        
        Args:
            ip_port: IP:Port. If None, disconnects all.
            
        Returns:
            True if successful.
        """
        if ip_port:
            cmd = ["disconnect", ip_port]
        else:
            cmd = ["disconnect"]
        ret, _, _ = self._run_adb(cmd)
        return ret == 0
    
    def tcpip(self, port: int = 5555) -> bool:
        """
        Restart ADB in TCP mode.
        
        Args:
            port: Port number.
            
        Returns:
            True if successful.
        """
        cmd = ["tcpip", str(port)]
        ret, _, _ = self._run_adb(cmd)
        return ret == 0
    
    # ==================== Recording ====================
    
    def start_screen_record(self, output_path: str = "/sdcard/recording.mp4", 
                           time_limit: int = 180, bit_rate: int = 8000000) -> bool:
        """
        Start screen recording (background).
        
        Args:
            output_path: Output path on device.
            time_limit: Time limit in seconds (max 180).
            bit_rate: Video bit rate.
            
        Returns:
            True if successful.
        """
        cmd = ["shell", "screenrecord", "--time-limit", str(time_limit), 
               "--bit-rate", str(bit_rate), output_path, "&"]
        ret, _, _ = self._run_adb(cmd)
        return ret == 0


# ==================== Action Recording & Playback ====================

class ActionRecorder:
    """
    Record and playback action sequences.
    """
    
    def __init__(self, controller: ADBController):
        self.controller = controller
        self.recorded_actions: List[Dict[str, Any]] = []
        self.is_recording = False
        self.start_time: float = 0
    
    def start_recording(self):
        """Start recording actions."""
        self.recorded_actions = []
        self.is_recording = True
        self.start_time = time.time()
    
    def stop_recording(self) -> List[Dict[str, Any]]:
        """Stop recording and return recorded actions."""
        self.is_recording = False
        return self.recorded_actions
    
    def record_action(self, action_type: str, params: Dict[str, Any]):
        """Record an action with timestamp."""
        if not self.is_recording:
            return
        
        action = {
            'type': action_type,
            'params': params,
            'timestamp': time.time() - self.start_time
        }
        self.recorded_actions.append(action)
    
    def playback(self, actions: List[Dict[str, Any]], speed: float = 1.0):
        """
        Playback recorded actions.
        
        Args:
            actions: List of recorded actions.
            speed: Playback speed (1.0 = normal, 2.0 = double speed).
        """
        last_time = 0
        for action in actions:
            delay = (action['timestamp'] - last_time) / speed
            if delay > 0:
                time.sleep(delay)
            
            self._execute_action(action['type'], action['params'])
            last_time = action['timestamp']
    
    def _execute_action(self, action_type: str, params: Dict[str, Any]):
        """Execute a single action."""
        action_map = {
            'tap': lambda p: self.controller.tap(p['x'], p['y']),
            'swipe': lambda p: self.controller.swipe(p['start_x'], p['start_y'], 
                                                      p['end_x'], p['end_y']),
            'keyevent': lambda p: self.controller.keyevent(p['keycode']),
            'text': lambda p: self.controller.input_text(p['text']),
            'home': lambda p: self.controller.press_home(),
            'back': lambda p: self.controller.press_back(),
        }
        
        if action_type in action_map:
            action_map[action_type](params)
    
    def save_to_file(self, filepath: str):
        """Save recorded actions to JSON file."""
        with open(filepath, 'w') as f:
            json.dump(self.recorded_actions, f, indent=2)
    
    def load_from_file(self, filepath: str) -> List[Dict[str, Any]]:
        """Load recorded actions from JSON file."""
        with open(filepath, 'r') as f:
            return json.load(f)


# ==================== CLI Interface ====================

def main():
    """CLI interface for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Android Device Controller via ADB')
    parser.add_argument('--device', '-d', help='Device serial number')
    parser.add_argument('--screenshot', '-s', help='Take screenshot', metavar='OUTPUT_PATH')
    parser.add_argument('--tap', nargs=2, type=int, metavar=('X', 'Y'), help='Tap at coordinates')
    parser.add_argument('--swipe', nargs=4, type=int, metavar=('X1', 'Y1', 'X2', 'Y2'), help='Swipe')
    parser.add_argument('--text', '-t', help='Input text')
    parser.add_argument('--key', '-k', type=int, help='Send key event')
    parser.add_argument('--home', action='store_true', help='Press HOME')
    parser.add_argument('--back', action='store_true', help='Press BACK')
    parser.add_argument('--info', '-i', action='store_true', help='Get device info')
    parser.add_argument('--packages', '-p', action='store_true', help='List packages')
    parser.add_argument('--start-app', metavar='PACKAGE', help='Start app')
    
    args = parser.parse_args()
    
    controller = ADBController(args.device)
    
    if args.screenshot:
        controller.screenshot(args.screenshot)
        print(f"Screenshot saved to {args.screenshot}")
    
    if args.tap:
        controller.tap(args.tap[0], args.tap[1])
        print(f"Tapped at ({args.tap[0]}, {args.tap[1]})")
    
    if args.swipe:
        controller.swipe(*args.swipe)
        print(f"Swiped from ({args.swipe[0]}, {args.swipe[1]}) to ({args.swipe[2]}, {args.swipe[3]})")
    
    if args.text:
        controller.input_text(args.text)
        print(f"Input text: {args.text}")
    
    if args.key is not None:
        controller.keyevent(args.key)
        print(f"Sent key event: {args.key}")
    
    if args.home:
        controller.press_home()
        print("Pressed HOME")
    
    if args.back:
        controller.press_back()
        print("Pressed BACK")
    
    if args.info:
        info = controller.get_device_info()
        print(json.dumps(info, indent=2))
    
    if args.packages:
        packages = controller.list_packages()
        print("\n".join(packages[:20]))  # Show first 20
        print(f"... Total: {len(packages)} packages")
    
    if args.start_app:
        controller.start_app(args.start_app)
        print(f"Started app: {args.start_app}")


if __name__ == '__main__':
    main()
