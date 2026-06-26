#!/usr/bin/env python3
"""
Locate an image on screen and click it.

Usage:
    python click_image.py <image_path> [confidence]

Examples:
    python click_image.py button.png
    python click_image.py submit.png 0.9
"""

import sys
import pyautogui

def click_image(image_path, confidence=0.8):
    """Locate image on screen and click its center."""
    print(f"Searching for: {image_path}")
    
    location = pyautogui.locateOnScreen(image_path, confidence=confidence)
    
    if location:
        x, y = pyautogui.center(location)
        print(f"Found at: {location}")
        print(f"Clicking at: ({x}, {y})")
        pyautogui.click(x, y)
        return True
    else:
        print("Image not found on screen!")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python click_image.py <image_path> [confidence]")
        sys.exit(1)
    
    image_path = sys.argv[1]
    confidence = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8
    
    pyautogui.PAUSE = 0.5
    pyautogui.FAILSAFE = True
    
    success = click_image(image_path, confidence)
    sys.exit(0 if success else 1)
