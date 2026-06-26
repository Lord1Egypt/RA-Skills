#!/usr/bin/env python3
"""
Type a text sequence with optional delays.

Usage:
    python type_sequence.py <text> [interval]

Examples:
    python type_sequence.py "Hello World"
    python type_sequence.py "Fast text" 0.05
"""

import sys
import pyautogui

def type_text(text, interval=0.1):
    """Type text with specified interval between characters."""
    print(f"Typing: {text}")
    print(f"Interval: {interval}s")
    
    pyautogui.write(text, interval=interval)
    print("Done!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python type_sequence.py <text> [interval]")
        print("  text: The text to type (wrap in quotes if contains spaces)")
        print("  interval: Seconds between characters (default: 0.1)")
        sys.exit(1)
    
    text = sys.argv[1]
    interval = float(sys.argv[2]) if len(sys.argv) > 2 else 0.1
    
    pyautogui.PAUSE = 0.5
    pyautogui.FAILSAFE = True
    
    type_text(text, interval)
