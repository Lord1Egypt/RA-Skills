"""
Windows Automation Skill for OpenClaw
Provides Windows desktop automation using PyAutoGUI.
"""
import pyautogui
import subprocess
import pyperclip
import platform
import os

# Disable failsafe for smoother operation
pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0.1


def windows_click(x: float, y: float, button: str = "left", clicks: int = 1) -> str:
    """Click at specified screen coordinates."""
    pyautogui.click(x, y, clicks=clicks, button=button)
    return f"Clicked at ({x}, {y}) with {button} button"


def windows_double_click(x: float, y: float) -> str:
    """Double click at position."""
    pyautogui.doubleClick(x, y)
    return f"Double clicked at ({x}, {y})"


def windows_right_click(x: float, y: float) -> str:
    """Right click at position."""
    pyautogui.rightClick(x, y)
    return f"Right clicked at ({x}, {y})"


def windows_move(x: float, y: float, duration: float = 0.2) -> str:
    """Move mouse to position."""
    pyautogui.moveTo(x, y, duration=duration)
    return f"Moved to ({x}, {y})"


def windows_type(text: str, interval: float = 0.05) -> str:
    """Type text using keyboard."""
    pyautogui.write(text, interval=interval)
    return f"Typed: {text[:50]}..."


def windows_press(key: str) -> str:
    """Press a single key."""
    pyautogui.press(key)
    return f"Pressed: {key}"


def windows_hotkey(*keys) -> str:
    """Press keyboard shortcut combination."""
    pyautogui.hotkey(*keys)
    return f"Hotkey: {'+'.join(keys)}"


def windows_scroll(clicks: int) -> str:
    """Scroll the screen."""
    pyautogui.scroll(clicks)
    return f"Scrolled {clicks} clicks"


def windows_screenshot(filename: str = None) -> str:
    """Take a screenshot."""
    if filename is None:
        filename = "screenshot.png"
    path = pyautogui.screenshot(filename)
    return f"Saved to: {path}"


def windows_cursor_position() -> dict:
    """Get current cursor position."""
    x, y = pyautogui.position()
    return {"x": x, "y": y}


def windows_screen_size() -> dict:
    """Get screen resolution."""
    width, height = pyautogui.size()
    return {"width": width, "height": height}


def windows_launch_app(name: str) -> str:
    """Launch a Windows application."""
    subprocess.Popen(["cmd", "/c", "start", "", name])
    return f"Launched: {name}"


def windows_command(command: str) -> str:
    """Run a PowerShell or cmd command."""
    result = subprocess.run(
        ["powershell", "-Command", command],
        capture_output=True,
        text=True
    )
    return result.stdout if result.stdout else result.stderr


def windows_clipboard_read() -> str:
    """Read clipboard content."""
    return pyperclip.paste()


def windows_clipboard_write(text: str) -> str:
    """Write text to clipboard."""
    pyperclip.copy(text)
    return f"Copied to clipboard: {text[:50]}..."


def windows_system_info() -> dict:
    """Get basic system information."""
    info = {
        "platform": platform.system(),
        "version": platform.version(),
        "screen_size": windows_screen_size(),
        "cursor_position": windows_cursor_position()
    }
    return info
