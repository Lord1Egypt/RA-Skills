# -*- coding: utf-8 -*-
import sys
import time
import pyperclip
import pyautogui

def send_wechat_message(message):
    print("Sending WeChat message...")
    
    # Check for WeChat window
    wechat_windows = [w for w in pyautogui.getWindowsWithTitle("WeChat") if w.title]
    if not wechat_windows:
        wechat_windows = [w for w in pyautogui.getWindowsWithTitle("微信") if w.title]
    
    if not wechat_windows:
        print("ERROR: WeChat window not found!")
        print("Please open WeChat and click the chat window first")
        return False
    
    # Activate WeChat window
    wechat_windows[0].activate()
    time.sleep(0.3)
    
    # Copy message to clipboard
    pyperclip.copy(message)
    time.sleep(0.1)
    
    # Paste message
    pyautogui.hotkey('ctrl', 'v')
    time.sleep(0.2)
    
    # Press Enter to send
    pyautogui.press('enter')
    
    print("SUCCESS!")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python wx_send.py <message>")
        sys.exit(1)
    
    message = sys.argv[1]
    success = send_wechat_message(message)
    sys.exit(0 if success else 1)
