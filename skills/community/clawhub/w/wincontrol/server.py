#!/usr/bin/env python3
"""
WinControl - Frame Capture + Actions API
Captures on POST request, returns file location
Port 8767: Actions (HTTP API for control)
"""

import json
import os
import shutil
import signal
import sys
import atexit
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse

import win32api
import win32con
import mss
from PIL import Image

# Config
QUALITY = 90      # High quality for clear UI text
ACTION_PORT = 8767

# Get skill folder for screenshots (same folder as server.py)
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_PATH = os.path.join(SKILL_DIR, 'screenshot.jpg')

# Screen dimensions
try:
    screen_w = win32api.GetSystemMetrics(0)
    screen_h = win32api.GetSystemMetrics(1)
except Exception as e:
    print(f"[WinControl] Error getting screen dimensions: {e}")
    screen_w, screen_h = 1920, 1080  # Fallback


def cleanup_files():
    """Delete screenshot on shutdown"""
    try:
        if os.path.exists(SCREENSHOT_PATH):
            os.remove(SCREENSHOT_PATH)
            print(f"\n[WinControl] Deleted screenshot. Goodbye!")
        else:
            print(f"\n[WinControl] No screenshot to delete. Goodbye!")
    except Exception as e:
        print(f"\n[WinControl] Could not delete screenshot: {e}")


def signal_handler(signum, frame):
    """Handle Ctrl+C and other shutdown signals"""
    sig_name = signal.Signals(signum).name
    print(f"\n[WinControl] Received {sig_name}, shutting down...")
    cleanup_files()
    sys.exit(0)


# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)   # Ctrl+C
signal.signal(signal.SIGTERM, signal_handler)  # Termination
atexit.register(cleanup_files)                 # Normal exit


def capture(quality=None):
    """Capture screen and save to screenshot.jpg in skill folder
    
    Args:
        quality: JPEG quality (1-100), uses default if None
    """
    q = quality if quality is not None else QUALITY
    try:
        with mss.mss() as sct:
            try:
                img = sct.grab(sct.monitors[1])
                im = Image.frombytes("RGB", img.size, img.bgra, "raw", "BGRX")
            except Exception as e:
                return {"ok": False, "error": f"Screen capture failed: {e}"}
            
            try:
                im.save(SCREENSHOT_PATH, format='JPEG', quality=q, optimize=True)
            except Exception as e:
                return {"ok": False, "error": f"Failed to save image: {e}"}
            
            return {"ok": True, "path": SCREENSHOT_PATH, "quality": q}
    except Exception as e:
        print(f"Capture error: {e}")
        return {"ok": False, "error": str(e)}


# ========== ACTION HANDLERS ==========

def validate_coords(x, y, name="coordinates"):
    """Validate screen coordinates"""
    try:
        x, y = int(x), int(y)
        if x < 0 or y < 0:
            return None, f"{name} must be positive"
        return (x, y), None
    except (TypeError, ValueError):
        return None, f"{name} must be integers"


def handle_click(x, y, button="left"):
    """Click at screen coordinates"""
    coords, error = validate_coords(x, y)
    if error:
        return {"ok": False, "error": error}
    x, y = coords
    
    valid_buttons = ["left", "right", "middle"]
    if button not in valid_buttons:
        return {"ok": False, "error": f"Invalid button. Use: {valid_buttons}"}
    
    try:
        nx = int(x * 65535 / screen_w)
        ny = int(y * 65535 / screen_h)
        flags = win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE
        
        if button == "left":
            win32api.mouse_event(flags | win32con.MOUSEEVENTF_LEFTDOWN, nx, ny, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, nx, ny, 0, 0)
        elif button == "right":
            win32api.mouse_event(flags | win32con.MOUSEEVENTF_RIGHTDOWN, nx, ny, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, nx, ny, 0, 0)
        elif button == "middle":
            win32api.mouse_event(flags | win32con.MOUSEEVENTF_MIDDLEDOWN, nx, ny, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_MIDDLEUP, nx, ny, 0, 0)
        return {"ok": True, "x": x, "y": y, "button": button}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def handle_drag(x1, y1, x2, y2, button="left"):
    """Drag from (x1,y1) to (x2,y2)"""
    start, error = validate_coords(x1, y1, "start coordinates")
    if error:
        return {"ok": False, "error": error}
    
    end, error = validate_coords(x2, y2, "end coordinates")
    if error:
        return {"ok": False, "error": error}
    
    valid_buttons = ["left", "right"]
    if button not in valid_buttons:
        return {"ok": False, "error": f"Invalid button. Use: {valid_buttons}"}
    
    try:
        x1, y1 = start
        x2, y2 = end
        nx1 = int(x1 * 65535 / screen_w)
        ny1 = int(y1 * 65535 / screen_h)
        nx2 = int(x2 * 65535 / screen_w)
        ny2 = int(y2 * 65535 / screen_h)
        
        down_flag = win32con.MOUSEEVENTF_LEFTDOWN if button == "left" else win32con.MOUSEEVENTF_RIGHTDOWN
        up_flag = win32con.MOUSEEVENTF_LEFTUP if button == "left" else win32con.MOUSEEVENTF_RIGHTUP
        
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE, nx1, ny1, 0, 0)
        win32api.mouse_event(down_flag, nx1, ny1, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE, nx2, ny2, 0, 0)
        win32api.mouse_event(up_flag, nx2, ny2, 0, 0)
        return {"ok": True, "from": [x1, y1], "to": [x2, y2], "button": button}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def handle_move(x, y):
    """Move mouse cursor to screen coordinates (no click)"""
    coords, error = validate_coords(x, y)
    if error:
        return {"ok": False, "error": error}
    x, y = coords
    
    try:
        nx = int(x * 65535 / screen_w)
        ny = int(y * 65535 / screen_h)
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE, nx, ny, 0, 0)
        return {"ok": True, "x": x, "y": y}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def handle_scroll(x, y, direction="down", amount=3):
    """Scroll at position"""
    coords, error = validate_coords(x, y)
    if error:
        return {"ok": False, "error": error}
    x, y = coords
    
    if direction not in ["down", "up"]:
        return {"ok": False, "error": "Direction must be 'down' or 'up'"}
    
    try:
        amount = int(amount)
        if amount < 1 or amount > 10:
            return {"ok": False, "error": "Amount must be between 1 and 10"}
    except (TypeError, ValueError):
        return {"ok": False, "error": "Amount must be an integer"}
    
    try:
        nx = int(x * 65535 / screen_w)
        ny = int(y * 65535 / screen_h)
        win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE | win32con.MOUSEEVENTF_MOVE, nx, ny, 0, 0)
        wheel_delta = -120 * amount if direction == "down" else 120 * amount
        win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, wheel_delta, 0)
        return {"ok": True, "x": x, "y": y, "direction": direction, "amount": amount}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def handle_enter(keys):
    """Handle mixed key input: list of strings/text/keys/combos
    
    Examples:
    - ["Hello"] -> types "Hello"
    - ["Enter"] -> presses Enter key
    - ["Ctrl", "C"] -> Ctrl+C combo
    - ["Hello", "Enter", "Ctrl", "A"] -> types Hello, presses Enter, then Ctrl+A
    """
    if not isinstance(keys, list):
        return {"ok": False, "error": "keys must be an array"}
    
    if not keys:
        return {"ok": False, "error": "keys array cannot be empty"}
    
    if len(keys) > 100:
        return {"ok": False, "error": "Too many keys (max 100)"}
    
    try:
        # Define key mappings
        modifiers = {
            'Ctrl': win32con.VK_CONTROL, 'Control': win32con.VK_CONTROL,
            'Alt': win32con.VK_MENU, 'Shift': win32con.VK_SHIFT,
            'Win': win32con.VK_LWIN, 'Windows': win32con.VK_LWIN,
        }
        special_keys = {
            'Enter': 0x0D, 'Return': 0x0D, 'Escape': 0x1B, 'Esc': 0x1B,
            'Backspace': 0x08, 'Tab': 0x09, 'Space': 0x20,
            'Delete': 0x2E, 'Del': 0x2E,
            'Up': 0x26, 'Down': 0x28, 'Left': 0x25, 'Right': 0x27,
            'Home': 0x24, 'End': 0x23, 'PageUp': 0x21, 'PageDown': 0x22,
            'F1': 0x70, 'F2': 0x71, 'F3': 0x72, 'F4': 0x73,
            'F5': 0x74, 'F6': 0x75, 'F7': 0x76, 'F8': 0x77,
            'F9': 0x78, 'F10': 0x79, 'F11': 0x7A, 'F12': 0x7B,
        }
        
        i = 0
        while i < len(keys):
            if not isinstance(keys[i], str):
                return {"ok": False, "error": f"Key at index {i} must be a string"}
            
            key = keys[i]
            
            # Check if this is a modifier followed by another key (combo)
            if key in modifiers and i + 1 < len(keys) and keys[i + 1] not in modifiers:
                # It's a combo: modifier + key
                combo_keys = [key]
                j = i + 1
                # Collect all non-modifier keys that follow
                while j < len(keys) and keys[j] not in modifiers:
                    combo_keys.append(keys[j])
                    j += 1
                
                # Execute combo
                vks = []
                for k in combo_keys:
                    if k in modifiers:
                        vks.append(modifiers[k])
                    elif k in special_keys:
                        vks.append(special_keys[k])
                    elif len(k) == 1:
                        vks.append(win32api.VkKeyScan(k) & 0xFF)
                    else:
                        return {"ok": False, "error": f"Unknown key in combo: {k}"}
                
                # Press all keys down
                for vk in vks:
                    win32api.keybd_event(vk, 0, 0, 0)
                # Release in reverse order
                for vk in reversed(vks):
                    win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
                
                i = j
            
            # Check if it's a single special key
            elif key in special_keys:
                vk = special_keys[key]
                win32api.keybd_event(vk, 0, 0, 0)
                win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
                i += 1
            
            # Otherwise treat as text to type
            else:
                for char in key:
                    if char == ' ':
                        vk = 0x20
                        win32api.keybd_event(vk, 0, 0, 0)
                        win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
                    elif char.isupper():
                        vk = win32api.VkKeyScan(char) & 0xFF
                        win32api.keybd_event(win32con.VK_SHIFT, 0, 0, 0)
                        win32api.keybd_event(vk, 0, 0, 0)
                        win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
                        win32api.keybd_event(win32con.VK_SHIFT, 0, win32con.KEYEVENTF_KEYUP, 0)
                    else:
                        vk = win32api.VkKeyScan(char) & 0xFF if char.isalpha() else ord(char)
                        win32api.keybd_event(vk, 0, 0, 0)
                        win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)
                i += 1
        
        return {"ok": True, "keys": keys, "count": len(keys)}
    except Exception as e:
        return {"ok": False, "error": str(e)}


# ========== ACTION SERVER ==========

class ActionHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        try:
            self.send_response(status)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        except Exception as e:
            print(f"Error sending response: {e}")
    
    def _send_error(self, message, status=400):
        self._send_json({"ok": False, "error": message}, status)
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        try:
            path = urlparse(self.path).path
            content_len = int(self.headers.get('Content-Length', 0))
            
            if content_len > 10 * 1024 * 1024:  # Max 10MB body
                self._send_error("Request body too large", 413)
                return
            
            body = self.rfile.read(content_len).decode('utf-8') if content_len > 0 else '{}'
        except Exception as e:
            self._send_error(f"Failed to read request: {e}", 400)
            return
        
        try:
            data = json.loads(body) if body else {}
        except json.JSONDecodeError as e:
            self._send_error(f"Invalid JSON: {e}", 400)
            return
        except Exception as e:
            self._send_error(f"Failed to parse body: {e}", 400)
            return
        
        result = {"ok": False, "error": "Unknown endpoint"}
        
        try:
            if path == '/capture':
                cap_result = capture(quality=data.get('quality'))
                result = cap_result
            elif path == '/move':
                result = handle_move(data.get('x'), data.get('y'))
            elif path == '/click':
                result = handle_click(data.get('x'), data.get('y'), data.get('button', 'left'))
            elif path == '/drag':
                result = handle_drag(data.get('x1'), data.get('y1'), 
                                    data.get('x2'), data.get('y2'),
                                    data.get('button', 'left'))
            elif path == '/scroll':
                result = handle_scroll(data.get('x'), data.get('y'),
                                      data.get('direction', 'down'), data.get('amount', 3))
            elif path == '/enter':
                result = handle_enter(data.get('keys', []))
            else:
                self._send_error(f"Unknown endpoint: {path}", 404)
                return
        except Exception as e:
            self._send_error(f"Server error: {e}", 500)
            return
        
        self._send_json(result)
    
    def do_GET(self):
        try:
            path = urlparse(self.path).path
            
            if path == '/ping':
                self._send_json({"ok": True})
            else:
                self._send_json({"endpoints": [
                    "POST /capture     - Capture screen, optional {quality: 1-100}",
                    "POST /move        - {x, y} - Move cursor without clicking",
                    "POST /click       - {x, y, button?}",
                    "POST /drag        - {x1, y1, x2, y2, button?}",
                    "POST /scroll      - {x, y, direction?, amount?}",
                    "POST /enter       - {keys: []} - text, special keys, or combos",
                    "GET  /ping        - Health check"
                ]})
        except Exception as e:
            self._send_error(f"Server error: {e}", 500)
    
    def log_message(self, format, *args):
        """Log requests with timestamps"""
        print(f"[{self.log_date_time_string()}] {args[0] if args else format}")


def action_server():
    try:
        server = HTTPServer(('localhost', ACTION_PORT), ActionHandler)
        print(f"[WinControl] Action API: http://localhost:{ACTION_PORT}")
        print(f"[WinControl] Screenshot saved to: {SCREENSHOT_PATH}")
        print(f"[WinControl] Press Ctrl+C to stop and cleanup\n")
        server.serve_forever()
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"[WinControl] Error: Port {ACTION_PORT} is already in use")
            print("[WinControl] Is another instance already running?")
        else:
            print(f"[WinControl] Server error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[WinControl] Fatal error: {e}")
        sys.exit(1)


# ========== MAIN ==========

if __name__ == "__main__":
    print(f"[WinControl] Server Starting...")
    print(f"[WinControl] Screen: {screen_w}x{screen_h} @ {QUALITY}% quality")
    print(f"[WinControl] Screenshot path: {SCREENSHOT_PATH}")
    print("")
    
    action_server()
