#!/usr/bin/env python3
"""
GUI Controller - Mouse, keyboard, screenshot, and visual control.

Capabilities:
  - Mouse: move, click, double-click, right-click, drag, scroll, get position
  - Keyboard: type text, press hotkeys, key combinations
  - Screenshot: full screen, region, save to file
  - OCR: extract text from screen regions
  - Visual: find image/pattern on screen, click by color

Requirements: Windows 10/11, Python 3.x
Dependencies: pyautogui (auto-installed), pillow (auto-installed), pytesseract (optional, for OCR)
"""

import sys
import os
import json
import subprocess
import argparse

if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if sys.stderr.encoding != 'utf-8':
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import run_ps as _run_ps

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_DIR = os.path.join(SCRIPT_DIR, "..", "screenshots")

# ========== Dependency Management ==========

def _ensure_deps(modules=None):
    """Ensure required Python packages are installed. Returns True on success."""
    if modules is None:
        modules = []
    missing = []
    for mod in modules:
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    if not missing:
        return True
    # Build pip install command
    pkg_map = {
        "pyautogui": "pyautogui",
        "PIL": "pillow",
        "pytesseract": "pytesseract",
    }
    pkgs = []
    for m in missing:
        pkgs.append(pkg_map.get(m, m))
    pip = sys.executable
    if not pip:
        return False
    cmd = [pip, "-m", "pip", "install"] + pkgs
    print(f"INFO: Installing missing packages: {', '.join(pkgs)}", file=sys.stderr)
    try:
        subprocess.run(cmd, capture_output=True, timeout=120)
        return True
    except Exception as e:
        print(f"ERROR: Failed to install packages: {e}", file=sys.stderr)
        return False


def _get_gui():
    """Import and return pyautogui, installing if needed."""
    _ensure_deps(["pyautogui", "PIL"])
    try:
        import pyautogui
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        return pyautogui
    except ImportError:
        print("ERROR: pyautogui not available. Run: pip install pyautogui pillow")
        sys.exit(1)


# ========== Mouse Control ==========

def mouse_move(x, y, duration=0.3):
    """Move mouse to absolute screen coordinates (x, y)."""
    gui = _get_gui()
    gui.moveTo(x, y, duration=duration)
    print(f"OK: Mouse moved to ({x}, {y})")


def mouse_click(x=None, y=None, button="left", clicks=1, duration=0.2):
    """Click at position. Uses current position if x,y not provided."""
    gui = _get_gui()
    if x is not None and y is not None:
        gui.moveTo(x, y, duration=duration)
    if clicks == 1:
        gui.click(button=button)
    else:
        gui.click(button=button, clicks=clicks, interval=0.1)
    pos = gui.position()
    print(f"OK: {button} click x{clicks} at ({pos.x}, {pos.y})")


def mouse_right_click(x=None, y=None):
    """Right-click at position."""
    mouse_click(x, y, button="right")


def mouse_double_click(x=None, y=None):
    """Double-click at position."""
    mouse_click(x, y, clicks=2)


def mouse_drag(start_x, start_y, end_x, end_y, duration=0.5, button="left"):
    """Drag from one position to another."""
    gui = _get_gui()
    gui.moveTo(start_x, start_y, duration=0.2)
    gui.dragTo(end_x, end_y, duration=duration, button=button)
    print(f"OK: Dragged from ({start_x},{start_y}) to ({end_x},{end_y})")


def mouse_scroll(x=None, y=None, clicks=5, direction="up"):
    """Scroll mouse wheel. Positive clicks=up, negative=down."""
    gui = _get_gui()
    if x is not None and y is not None:
        gui.moveTo(x, y, duration=0.2)
    amount = clicks if direction == "up" else -clicks
    gui.scroll(amount)
    pos = gui.position()
    print(f"OK: Scrolled {direction} {abs(clicks)} clicks at ({pos.x}, {pos.y})")


def mouse_position():
    """Get current mouse position."""
    gui = _get_gui()
    pos = gui.position()
    size = gui.size()
    result = json.dumps({
        "x": pos.x,
        "y": pos.y,
        "screen_width": size.width,
        "screen_height": size.height
    })
    print(result)


# ========== Keyboard Control ==========

def keyboard_type(text, interval=0.02):
    """Type text character by character at current cursor position."""
    gui = _get_gui()
    gui.typewrite(text, interval=interval)
    print(f"OK: Typed {len(text)} characters")


def keyboard_press(keys):
    """Press a key or key combination (e.g., 'ctrl', 'alt+tab', 'ctrl+shift+esc')."""
    gui = _get_gui()
    gui.hotkey(*keys.split("+"))
    print(f"OK: Pressed {keys}")


def keyboard_hotkey(*key_list):
    """Press multiple keys simultaneously. Keys as separate args."""
    gui = _get_gui()
    gui.hotkey(*key_list)
    print(f"OK: Pressed {'+'.join(key_list)}")


def keyboard_key_down(key):
    """Hold down a key (useful for drag with shift/ctrl)."""
    gui = _get_gui()
    gui.keyDown(key)
    print(f"OK: Key down: {key}")


def keyboard_key_up(key):
    """Release a held key."""
    gui = _get_gui()
    gui.keyUp(key)
    print(f"OK: Key up: {key}")


# ========== Screenshot ==========

def screenshot_full(filepath=None):
    """Take a full screen screenshot. Save to file if path provided."""
    gui = _get_gui()
    img = gui.screenshot()
    if filepath:
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        img.save(filepath)
        print(f"OK: Screenshot saved to {filepath}")
    else:
        # Save to default location
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        auto_path = os.path.join(SCREENSHOT_DIR, "screenshot.png")
        img.save(auto_path)
        print(f"OK: Screenshot saved to {auto_path}")
        print(f"INFO: File size: {os.path.getsize(auto_path)} bytes")
    return img


def screenshot_region(x, y, width, height, filepath=None):
    """Take a screenshot of a specific region."""
    gui = _get_gui()
    img = gui.screenshot(region=(x, y, width, height))
    if filepath:
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
        img.save(filepath)
        print(f"OK: Region screenshot saved to {filepath}")
    else:
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)
        auto_path = os.path.join(SCREENSHOT_DIR, "region.png")
        img.save(auto_path)
        print(f"OK: Region screenshot saved to {auto_path}")
    return img


def screenshot_active_window(filepath=None):
    """Take a screenshot of the active (foreground) window."""
    gui = _get_gui()
    # Use PowerShell to get foreground window bounds
    script = r"""
Add-Type @"
using System;
using System.Runtime.InteropServices;
public class WinRect {
    [DllImport("user32.dll")]
    public static extern bool GetWindowRect(IntPtr hWnd, out RECT lpRect);
    [DllImport("user32.dll")]
    public static extern IntPtr GetForegroundWindow();
    [StructLayout(LayoutKind.Sequential)]
    public struct RECT { public int Left, Top, Right, Bottom; }
}
"@
$hwnd = [WinRect]::GetForegroundWindow()
$rect = New-Object WinRect+RECT
[WinRect]::GetWindowRect($hwnd, [ref]$rect)
Write-Output "$($rect.Left),$($rect.Top),$($rect.Right),$($rect.Bottom)"
"""
    stdout, _, code = _run_ps(script, timeout=5)
    if code == 0 and stdout:
        parts = stdout.split(",")
        if len(parts) == 4:
            left, top, right, bottom = [int(p.strip()) for p in parts]
            w = right - left
            h = bottom - top
            img = gui.screenshot(region=(left, top, w, h))
            if filepath:
                os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
                img.save(filepath)
                print(f"OK: Window screenshot saved to {filepath}")
            else:
                os.makedirs(SCREENSHOT_DIR, exist_ok=True)
                auto_path = os.path.join(SCREENSHOT_DIR, "window.png")
                img.save(auto_path)
                print(f"OK: Window screenshot saved to {auto_path}")
            return img
    print("ERROR: Could not capture active window")
    return None


def get_screen_size():
    """Get screen resolution."""
    gui = _get_gui()
    size = gui.size()
    print(json.dumps({"width": size.width, "height": size.height}))


# ========== Visual / OCR ==========

def ocr_region(x, y, width, height, lang="chi_sim+eng"):
    """Extract text from a screen region using Tesseract OCR."""
    _ensure_deps(["pytesseract"])
    try:
        import pytesseract
        from PIL import Image
    except ImportError:
        # Fallback: use PowerShell + Windows OCR
        print(_ocr_region_powershell(x, y, width, height))
        return

    gui = _get_gui()
    img = gui.screenshot(region=(x, y, width, height))
    try:
        text = pytesseract.image_to_string(img, lang=lang)
        text = text.strip()
        if text:
            print(f"OK: OCR result:\n{text}")
        else:
            print("OK: OCR result: (no text detected)")
    except Exception as e:
        # Fallback to PowerShell OCR
        print(_ocr_region_powershell(x, y, width, height))


def _ocr_region_powershell(x, y, width, height):
    """Fallback OCR using Windows built-in OCR via PowerShell."""
    gui = _get_gui()
    import tempfile
    # Save screenshot temporarily
    tmp = os.path.join(tempfile.gettempdir(), "ocr_temp.png")
    img = gui.screenshot(region=(x, y, width, height))
    img.save(tmp)

    script = f"""
Add-Type -AssemblyName System.Runtime.WindowsRuntime
$bytes = [System.IO.File]::ReadAllBytes('{tmp}')
# Use Windows.Media.Ocr if available
try {{
    # .NET approach with Windows OCR
    [Windows.Storage.StorageFile, Windows.Storage, ContentType=WindowsRuntime] | Out-Null
    [Windows.Media.Ocr.OcrEngine, Windows.Media.Ocr, ContentType=WindowsRuntime] | Out-Null
    Write-Output "INFO: Windows OCR available but requires async API. Use pytesseract for better results."
    Write-Output "INFO: Screenshot saved at {tmp}"
}} catch {{
    Write-Output "INFO: OCR not available. Screenshot saved at {tmp}"
    Write-Output "INFO: Install Tesseract OCR for text extraction: choco install tesseract"
}}
"""
    stdout, _, code = _run_ps(script, timeout=10)
    return stdout if stdout else f"INFO: Screenshot saved at {tmp}"


def ocr_full(lang="chi_sim+eng"):
    """OCR the entire screen."""
    gui = _get_gui()
    size = gui.size()
    ocr_region(0, 0, size.width, size.height, lang)


def find_image(template_path, confidence=0.9):
    """Find an image template on screen. Returns position or error."""
    import glob
    # Search in screenshots dir if relative path
    if not os.path.isabs(template_path):
        paths = glob.glob(os.path.join(SCREENSHOT_DIR, template_path))
        if paths:
            template_path = paths[0]
        else:
            paths = glob.glob(os.path.join(SCRIPT_DIR, "..", "assets", template_path))
            if paths:
                template_path = paths[0]

    if not os.path.exists(template_path):
        print(f"ERROR: Template image not found: {template_path}")
        return

    gui = _get_gui()
    try:
        location = gui.locateOnScreen(template_path, confidence=confidence)
        if location:
            center = gui.center(location)
            result = json.dumps({
                "found": True,
                "x": center.x,
                "y": center.y,
                "width": location.width,
                "height": location.height
            })
            print(f"OK: Found template at center ({center.x}, {center.y})")
            print(result)
        else:
            print(f"OK: Template not found on screen (confidence threshold: {confidence})")
    except Exception as e:
        print(f"ERROR: {e}")


def click_image(template_path, button="left", confidence=0.9, offset_x=0, offset_y=0):
    """Find an image on screen and click it."""
    import glob
    if not os.path.isabs(template_path):
        paths = glob.glob(os.path.join(SCREENSHOT_DIR, template_path))
        if paths:
            template_path = paths[0]

    if not os.path.exists(template_path):
        print(f"ERROR: Template image not found: {template_path}")
        return

    gui = _get_gui()
    try:
        location = gui.locateOnScreen(template_path, confidence=confidence)
        if location:
            center = gui.center(location)
            target_x = center.x + offset_x
            target_y = center.y + offset_y
            gui.click(x=target_x, y=target_y, button=button)
            print(f"OK: Clicked template at ({target_x}, {target_y})")
        else:
            print(f"ERROR: Template not found on screen")
    except Exception as e:
        print(f"ERROR: {e}")


def find_color(target_color, region=None):
    """Find all pixels matching a color on screen. Color as (R,G,B) or hex."""
    gui = _get_gui()
    if isinstance(target_color, str):
        # Parse hex color like "#FF0000"
        target_color = target_color.lstrip("#")
        target_color = tuple(int(target_color[i:i+2], 16) for i in (0, 2, 4))

    if region:
        img = gui.screenshot(region=region)
        offset_x, offset_y = region[0], region[1]
    else:
        img = gui.screenshot()
        offset_x, offset_y = 0, 0

    width, height = img.size
    matches = []
    tolerance = 10  # Color matching tolerance

    # Sample every few pixels for performance
    step = 2
    for y_pos in range(0, height, step):
        for x_pos in range(0, width, step):
            pixel = img.getpixel((x_pos, y_pos))
            if all(abs(pixel[i] - target_color[i]) <= tolerance for i in range(3)):
                matches.append({
                    "x": x_pos + offset_x,
                    "y": y_pos + offset_y
                })
                if len(matches) >= 50:
                    break
        if len(matches) >= 50:
            break

    if matches:
        print(f"OK: Found {len(matches)} pixels matching color {target_color}")
        print(f"INFO: First match at ({matches[0]['x']}, {matches[0]['y']})")
    else:
        print(f"OK: No pixels found matching color {target_color}")
    return matches


def pixel_color(x, y):
    """Get the color of a pixel at (x, y)."""
    gui = _get_gui()
    pixel = gui.pixel(x, y)
    print(json.dumps({
        "x": x,
        "y": y,
        "RGB": [pixel.red, pixel.green, pixel.blue],
        "hex": f"#{pixel.red:02X}{pixel.green:02X}{pixel.blue:02X}"
    }))


def list_screenshots():
    """List previously saved screenshots."""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    files = []
    for f in sorted(os.listdir(SCREENSHOT_DIR)):
        if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
            fp = os.path.join(SCREENSHOT_DIR, f)
            files.append({
                "name": f,
                "path": fp,
                "size_bytes": os.path.getsize(fp)
            })
    if files:
        print(json.dumps(files, ensure_ascii=False, indent=2))
    else:
        print("OK: No screenshots saved yet")


# ========== Main CLI ==========

def main():
    parser = argparse.ArgumentParser(description="GUI Controller - Mouse, Keyboard, Screenshot, OCR")
    sub = parser.add_subparsers(dest="category")

    # Mouse
    p_mouse = sub.add_parser("mouse", help="Mouse control")
    mouse_sub = p_mouse.add_subparsers(dest="action")
    mouse_sub.add_parser("position", help="Get current mouse position")

    m_move = mouse_sub.add_parser("move", help="Move mouse")
    m_move.add_argument("--x", type=int, required=True)
    m_move.add_argument("--y", type=int, required=True)
    m_move.add_argument("--duration", type=float, default=0.3)

    m_click = mouse_sub.add_parser("click", help="Left click")
    m_click.add_argument("--x", type=int)
    m_click.add_argument("--y", type=int)

    m_rclick = mouse_sub.add_parser("right-click", help="Right click")
    m_rclick.add_argument("--x", type=int)
    m_rclick.add_argument("--y", type=int)

    m_dclick = mouse_sub.add_parser("double-click", help="Double click")
    m_dclick.add_argument("--x", type=int)
    m_dclick.add_argument("--y", type=int)

    m_drag = mouse_sub.add_parser("drag", help="Drag from A to B")
    m_drag.add_argument("--start-x", type=int, required=True)
    m_drag.add_argument("--start-y", type=int, required=True)
    m_drag.add_argument("--end-x", type=int, required=True)
    m_drag.add_argument("--end-y", type=int, required=True)
    m_drag.add_argument("--duration", type=float, default=0.5)

    m_scroll = mouse_sub.add_parser("scroll", help="Scroll wheel")
    m_scroll.add_argument("--x", type=int)
    m_scroll.add_argument("--y", type=int)
    m_scroll.add_argument("--clicks", type=int, default=5)
    m_scroll.add_argument("--direction", choices=["up", "down"], default="up")

    # Keyboard
    p_kb = sub.add_parser("keyboard", help="Keyboard control")
    kb_sub = p_kb.add_subparsers(dest="action")

    kb_type = kb_sub.add_parser("type", help="Type text")
    kb_type.add_argument("--text", type=str, required=True)

    kb_press = kb_sub.add_parser("press", help="Press key or combo")
    kb_press.add_argument("--keys", type=str, required=True, help="e.g., 'ctrl+c', 'alt+tab'")

    kb_down = kb_sub.add_parser("key-down", help="Hold key")
    kb_down.add_argument("--key", type=str, required=True)

    kb_up = kb_sub.add_parser("key-up", help="Release key")
    kb_up.add_argument("--key", type=str, required=True)

    # Screenshot
    p_ss = sub.add_parser("screenshot", help="Screenshot capture")
    ss_sub = p_ss.add_subparsers(dest="action")
    ss_sub.add_parser("full", help="Full screen")
    ss_sub.add_parser("active-window", help="Active window")

    ss_region = ss_sub.add_parser("region", help="Screen region")
    ss_region.add_argument("--x", type=int, required=True)
    ss_region.add_argument("--y", type=int, required=True)
    ss_region.add_argument("--width", type=int, required=True)
    ss_region.add_argument("--height", type=int, required=True)

    ss_list = ss_sub.add_parser("list", help="List saved screenshots")

    ss_size = ss_sub.add_parser("size", help="Get screen resolution")

    # Visual / OCR
    p_vis = sub.add_parser("visual", help="Visual recognition and OCR")
    vis_sub = p_vis.add_subparsers(dest="action")

    vis_ocr = vis_sub.add_parser("ocr", help="OCR a screen region")
    vis_ocr.add_argument("--x", type=int, default=0)
    vis_ocr.add_argument("--y", type=int, default=0)
    vis_ocr.add_argument("--width", type=int)
    vis_ocr.add_argument("--height", type=int)
    vis_ocr.add_argument("--lang", type=str, default="chi_sim+eng")

    vis_find = vis_sub.add_parser("find", help="Find image template on screen")
    vis_find.add_argument("--template", type=str, required=True)
    vis_find.add_argument("--confidence", type=float, default=0.9)

    vis_click_img = vis_sub.add_parser("click-image", help="Find and click an image")
    vis_click_img.add_argument("--template", type=str, required=True)
    vis_click_img.add_argument("--confidence", type=float, default=0.9)
    vis_click_img.add_argument("--offset-x", type=int, default=0)
    vis_click_img.add_argument("--offset-y", type=int, default=0)

    vis_color = vis_sub.add_parser("find-color", help="Find pixels by color")
    vis_color.add_argument("--color", type=str, required=True, help="Hex color, e.g., '#FF0000'")
    vis_color.add_argument("--x", type=int)
    vis_color.add_argument("--y", type=int)
    vis_color.add_argument("--width", type=int)
    vis_color.add_argument("--height", type=int)

    vis_pixel = vis_sub.add_parser("pixel", help="Get color of a pixel")
    vis_pixel.add_argument("--x", type=int, required=True)
    vis_pixel.add_argument("--y", type=int, required=True)

    args = parser.parse_args()

    try:
        # Mouse
        if args.category == "mouse":
            if args.action == "position":
                mouse_position()
            elif args.action == "move":
                mouse_move(args.x, args.y, args.duration)
            elif args.action == "click":
                mouse_click(args.x, args.y)
            elif args.action == "right-click":
                mouse_right_click(args.x, args.y)
            elif args.action == "double-click":
                mouse_double_click(args.x, args.y)
            elif args.action == "drag":
                mouse_drag(args.start_x, args.start_y, args.end_x, args.end_y, args.duration)
            elif args.action == "scroll":
                mouse_scroll(args.x, args.y, args.clicks, args.direction)
            else:
                p_mouse.print_help()

        # Keyboard
        elif args.category == "keyboard":
            if args.action == "type":
                keyboard_type(args.text)
            elif args.action == "press":
                keyboard_press(args.keys)
            elif args.action == "key-down":
                keyboard_key_down(args.key)
            elif args.action == "key-up":
                keyboard_key_up(args.key)
            else:
                p_kb.print_help()

        # Screenshot
        elif args.category == "screenshot":
            if args.action == "full":
                screenshot_full()
            elif args.action == "active-window":
                screenshot_active_window()
            elif args.action == "region":
                screenshot_region(args.x, args.y, args.width, args.height)
            elif args.action == "list":
                list_screenshots()
            elif args.action == "size":
                get_screen_size()
            else:
                p_ss.print_help()

        # Visual
        elif args.category == "visual":
            if args.action == "ocr":
                gui = _get_gui()
                size = gui.size()
                w = args.width if args.width else size.width
                h = args.height if args.height else size.height
                ocr_region(args.x, args.y, w, h, args.lang)
            elif args.action == "find":
                find_image(args.template, args.confidence)
            elif args.action == "click-image":
                click_image(args.template, confidence=args.confidence,
                           offset_x=args.offset_x, offset_y=args.offset_y)
            elif args.action == "find-color":
                region = None
                if all(hasattr(args, a) and getattr(args, a) is not None
                       for a in ["x", "y", "width", "height"]):
                    region = (args.x, args.y, args.width, args.height)
                find_color(args.color, region)
            elif args.action == "pixel":
                pixel_color(args.x, args.y)
            else:
                p_vis.print_help()
        else:
            parser.print_help()
    except KeyboardInterrupt:
        print("\nInterrupted by user (mouse moved to corner as failsafe)")
    except Exception as e:
        print(f"ERROR: {e}")


if __name__ == "__main__":
    main()
