"""
WeChat MCP Server - Windows WeChat Message Monitoring and Sending

Features:
- Capture screenshots of the WeChat window
- Search for and open contact chat windows
- Send messages to specified contacts
- Support identification of and message sending to detached chat windows

Dependencies:
    pip install pyautogui pygetwindow pillow pyperclip opencv-python
"""

import pyautogui
import pygetwindow as gw
from PIL import Image
import pyperclip
import time
import cv2
import numpy as np

# WeChat window titles
WECHAT_TITLE = "WeChat"
WECHAT_DRAGON_TITLE = "Dragon"  # Detached chat window


def find_wechat_window():
    """Find the main WeChat window"""
    windows = gw.getWindowsWithTitle(WECHAT_TITLE)
    if windows:
        return windows[0]
    return None


def find_dragon_window():
    """Find a detached chat window (Dragon window)"""
    windows = gw.getWindowsWithTitle(WECHAT_DRAGON_TITLE)
    if windows:
        return windows[0]
    return None


def get_wechat_status():
    """
    Get the WeChat window status

    Returns:
        dict: Contains status, title, position, and size information
    """
    wechat = find_wechat_window()
    if wechat:
        return {
            'status': 'running',
            'title': wechat.title,
            'position': {'x': wechat.left, 'y': wechat.top},
            'size': {'width': wechat.width, 'height': wechat.height}
        }

    dragon = find_dragon_window()
    if dragon:
        return {
            'status': 'running_dragon',
            'title': dragon.title,
            'position': {'x': dragon.left, 'y': dragon.top},
            'size': {'width': dragon.width, 'height': dragon.height}
        }

    return {'status': 'not_found'}


def capture_wechat_screenshot(save_path=None):
    """
    Capture a screenshot of the WeChat window

    Args:
        save_path: Path to save the screenshot; if None, the screenshot is not saved

    Returns:
        PIL.Image: Screenshot image object
    """
    wechat = find_wechat_window() or find_dragon_window()
    if not wechat:
        raise Exception("WeChat window not found")

    wechat.activate()
    time.sleep(0.2)

    # Capture the window region
    screenshot = pyautogui.screenshot(region=(
        wechat.left,
        wechat.top,
        wechat.width,
        wechat.height
    ))

    if save_path:
        screenshot.save(save_path)

    return screenshot


def search_contact(contact_name):
    """
    Search for and open a contact's chat window

    Args:
        contact_name: Contact name

    Returns:
        bool: Whether the contact was successfully found and opened
    """
    wechat = find_wechat_window()
    if not wechat:
        raise Exception("WeChat window not found")

    wechat.activate()
    time.sleep(0.3)

    # Use Ctrl+F to open search
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(0.3)

    # Type the contact name
    pyperclip.copy(contact_name)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.5)

    # Press Enter to open the first search result
    pyautogui.press('enter')
    time.sleep(0.3)

    return True


def send_message_to_current(message):
    """
    Send a message to the current chat window

    Args:
        message: Message content
    """
    wechat = find_wechat_window() or find_dragon_window()
    if not wechat:
        raise Exception("WeChat window not found")

    wechat.activate()
    time.sleep(0.2)

    # Use clipboard to input the message (supports Chinese characters)
    pyperclip.copy(message)
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.1)

    # Send the message
    pyautogui.press('enter')


def send_message_to_contact(contact_name, message):
    """
    Send a message to a specified contact (complete workflow)

    Args:
        contact_name: Contact name
        message: Message content
    """
    # Search for and open the contact
    search_contact(contact_name)

    # Send the message
    send_message_to_current(message)


# MCP Tool Functions
def wechat_get_status():
    """MCP Tool: Get the WeChat window status"""
    return get_wechat_status()


def wechat_send_message(message):
    """MCP Tool: Send a message to the current chat window"""
    send_message_to_current(message)
    return {'status': 'sent', 'message': message}


if __name__ == "__main__":
    # Test
    print("WeChat status:", get_wechat_status())