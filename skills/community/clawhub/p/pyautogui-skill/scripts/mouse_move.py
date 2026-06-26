#!/usr/bin/env python3
"""
Move mouse to specified coordinates or relative position.

Usage:
    python mouse_move.py <x> <y> [duration]
    python mouse_move.py --relative <dx> <dy> [duration]

Examples:
    python mouse_move.py 100 200
    python mouse_move.py 500 500 1.0
    python mouse_move.py --relative 0 50 0.3
"""

import sys
import pyautogui

def move_mouse(x, y, duration=0.5, relative=False):
    """Move mouse to position or relative offset."""
    if relative:
        print(f"Moving relative: ({x}, {y}) over {duration}s")
        pyautogui.moveRel(x, y, duration=duration)
    else:
        print(f"Moving to: ({x}, {y}) over {duration}s")
        pyautogui.moveTo(x, y, duration=duration)
    
    final_x, final_y = pyautogui.position()
    print(f"Final position: ({final_x}, {final_y})")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python mouse_move.py <x> <y> [duration]")
        print("       python mouse_move.py --relative <dx> <dy> [duration]")
        sys.exit(1)
    
    relative = "--relative" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--relative"]
    
    if len(args) < 2:
        print("Error: Need at least x and y coordinates")
        sys.exit(1)
    
    x = int(args[0])
    y = int(args[1])
    duration = float(args[2]) if len(args) > 2 else 0.5
    
    pyautogui.PAUSE = 0.5
    pyautogui.FAILSAFE = True
    
    move_mouse(x, y, duration, relative)
