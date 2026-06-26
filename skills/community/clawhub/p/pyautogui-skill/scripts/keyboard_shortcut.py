#!/usr/bin/env python3
"""
Execute keyboard shortcuts/hotkeys.

Usage:
    python keyboard_shortcut.py <key1> [key2] [key3] ...

Examples:
    python keyboard_shortcut.py ctrl c
    python keyboard_shortcut.py ctrl shift n
    python keyboard_shortcut.py command space
"""

import sys
import pyautogui

def press_hotkey(*keys):
    """Press a combination of keys as a hotkey."""
    key_list = list(keys)
    print(f"Pressing: {'+'.join(key_list)}")
    pyautogui.hotkey(*key_list)
    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python keyboard_shortcut.py <key1> [key2] [key3] ...")
        print("")
        print("Common keys:")
        print("  Modifiers: ctrl, shift, alt, command (Mac), win (Windows)")
        print("  Special: enter, tab, space, escape, backspace")
        print("  Arrows: up, down, left, right")
        print("  Function: f1-f12")
        print("")
        print("Examples:")
        print("  python keyboard_shortcut.py ctrl c      # Copy")
        print("  python keyboard_shortcut.py ctrl v      # Paste")
        print("  python keyboard_shortcut.py ctrl s      # Save")
        sys.exit(1)
    
    keys = sys.argv[1:]
    
    pyautogui.PAUSE = 0.5
    pyautogui.FAILSAFE = True
    
    press_hotkey(*keys)
