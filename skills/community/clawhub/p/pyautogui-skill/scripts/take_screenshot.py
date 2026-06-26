#!/usr/bin/env python3
"""
Take a screenshot (full screen or region).

Usage:
    python take_screenshot.py [output_path] [x y width height]

Examples:
    python take_screenshot.py screen.png
    python take_screenshot.py region.png 0 0 300 400
"""

import sys
import pyautogui

def take_screenshot(output_path="screenshot.png", region=None):
    """Take a screenshot and save it."""
    if region:
        print(f"Taking screenshot of region: {region}")
        screenshot = pyautogui.screenshot(region=region)
    else:
        print("Taking full screenshot")
        screenshot = pyautogui.screenshot()
    
    screenshot.save(output_path)
    print(f"Saved to: {output_path}")
    return True

if __name__ == "__main__":
    pyautogui.PAUSE = 0.5
    pyautogui.FAILSAFE = True
    
    if len(sys.argv) > 5:
        # Region mode: x y width height
        output_path = sys.argv[1] if len(sys.argv) > 1 else "screenshot.png"
        region = (int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]))
        take_screenshot(output_path, region)
    elif len(sys.argv) > 1:
        # Just output path
        take_screenshot(sys.argv[1])
    else:
        # Default
        take_screenshot()
