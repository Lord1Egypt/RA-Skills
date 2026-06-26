---
name: pyautogui
description: "Desktop automation via PyAutoGUI. Use when: user needs to automate mouse/keyboard actions, GUI testing, click/type sequences, screen-based workflows, or repetitive desktop tasks. NOT for: web automation (use Playwright/Selenium), mobile automation, or image recognition at scale."
metadata: { "openclaw": { "emoji": "🖱️", "requires": { "bins": ["python3"], "pip": ["pyautogui", "pyscreeze"] } } }
---

# PyAutoGUI Skill

Desktop automation using PyAutoGUI for mouse, keyboard, and screen control.

## When to Use

✅ **USE this skill when:**

- Automating repetitive mouse/keyboard tasks
- GUI testing and interaction
- Click/type sequences for desktop apps
- Taking screenshots for automation
- Simple image location on screen
- Moving mouse to specific coordinates
- Keyboard shortcuts and hotkeys
- Form filling automation

❌ **DON'T use this skill when:**

- Web browser automation → use Playwright or Selenium
- Mobile app automation → use Appium
- Complex image recognition → use OpenCV/ML models
- Accessibility automation → use platform-native APIs
- High-speed automation → PyAutoGUI has safety delays

## Safety First

PyAutoGUI includes fail-safes. **NEVER disable them:**

```python
# Fail-safe: Move mouse to (0,0) to abort
pyautogui.FAILSAFE = True  # Keep this!

# Add pauses for safety
pyautogui.PAUSE = 0.5  # Seconds between actions
```

## Quick Start

```python
import pyautogui

# Basic movement
pyautogui.moveTo(100, 100, duration=0.5)
pyautogui.click()

# Typing
pyautogui.write('Hello world!', interval=0.1)

# Keyboard shortcuts
pyautogui.hotkey('ctrl', 'c')  # Copy
pyautogui.hotkey('ctrl', 'v')  # Paste
```

## Core Operations

### Mouse Control

```python
import pyautogui

# Get screen size
width, height = pyautogui.size()

# Current position
x, y = pyautogui.position()

# Move mouse (duration in seconds)
pyautogui.moveTo(100, 100, duration=0.5)
pyautogui.moveRel(0, 50, duration=0.3)  # Relative move

# Clicks
pyautogui.click()           # Left click at current position
pyautogui.click(x=100, y=100)
pyautogui.rightClick()
pyautogui.doubleClick()
pyautogui.dragTo(200, 200, duration=0.5)

# Button control
pyautogui.mouseDown()
pyautogui.mouseUp()
```

### Keyboard Control

```python
import pyautogui

# Type text
pyautogui.write('Hello!', interval=0.1)  # interval between chars

# Special keys
pyautogui.press('enter')
pyautogui.press(['up', 'up', 'down', 'down'])

# Key hold
pyautogui.keyDown('shift')
pyautogui.write('CAPS')
pyautogui.keyUp('shift')

# Hotkeys (shortcuts)
pyautogui.hotkey('ctrl', 's')      # Save
pyautogui.hotkey('ctrl', 'shift', 'n')  # New folder (Windows)
pyautogui.hotkey('command', 'space')    # Spotlight (Mac)
```

### Special Key Names

```
# Modifiers
'ctrl', 'shift', 'alt', 'command' (Mac), 'win' (Windows)

# Navigation
'enter', 'tab', 'space', 'escape', 'backspace', 'delete'
'up', 'down', 'left', 'right'
'home', 'end', 'pageup', 'pagedown'

# Function keys
'f1' through 'f12'

# Other
'capslock', 'numlock', 'scrolllock'
'printscreen', 'pause'
```

### Screenshots

```python
import pyautogui

# Full screenshot
screenshot = pyautogui.screenshot()
screenshot.save('screen.png')

# Region screenshot
screenshot = pyautogui.screenshot(region=(0, 0, 300, 400))

# To file directly
pyautogui.screenshot('saved.png')
```

### Image Location

```python
import pyautogui

# Find image on screen
location = pyautogui.locateOnScreen('button.png', confidence=0.8)

if location:
    x, y = pyautogui.center(location)
    pyautogui.click(x, y)

# Find all occurrences
locations = pyautogui.locateAllOnScreen('icon.png', confidence=0.8)

# Get center point
center = pyautogui.center(location)  # Returns (x, y)
```

**Note:** `confidence` requires Pillow. Range 0-1, higher = more strict matching.

## Common Workflows

### Form Filling

```python
import pyautogui
import time

pyautogui.PAUSE = 0.5

# Click first field
pyautogui.click(x=100, y=200)
pyautogui.write('John Doe')

# Tab to next field
pyautogui.press('tab')
pyautogui.write('john@example.com')

# Submit
pyautogui.press('enter')
```

### Window Management (OS-dependent)

```python
import pyautogui

# Minimize (Windows)
pyautogui.hotkey('win', 'down')

# Maximize
pyautogui.hotkey('win', 'up')

# Switch apps (Alt+Tab)
pyautogui.hotkey('alt', 'tab')

# Close window
pyautogui.hotkey('alt', 'f4')  # Windows
pyautogui.hotkey('command', 'w')  # Mac
```

### Screenshot + Click Pattern

```python
import pyautogui

# Locate and click a button
button = pyautogui.locateOnScreen('submit_btn.png', confidence=0.9)
if button:
    x, y = pyautogui.center(button)
    pyautogui.click(x, y)
else:
    print("Button not found!")
```

## Configuration

### Timing & Safety

```python
import pyautogui

# Pause between ALL actions (seconds)
pyautogui.PAUSE = 0.5

# Fail-safe (move to corner to stop)
pyautogui.FAILSAFE = True

# Timeout for locateOnScreen (seconds)
pyautogui.locateOnScreen('img.png', timeout=10)
```

### Platform Detection

```python
import platform

system = platform.system()

if system == "Darwin":
    # macOS shortcuts
    cmd = 'command'
elif system == "Windows":
    cmd = 'win'
else:
    cmd = 'ctrl'
```

## Scripts

See `scripts/` for reusable automation scripts:

- `scripts/click_image.py` - Locate and click an image
- `scripts/type_sequence.py` - Type a text sequence
- `scripts/take_screenshot.py` - Capture screen region

## Troubleshooting

### "PyAutoGUI not working"

1. **Permissions (macOS):**
   - System Settings → Privacy & Security → Accessibility
   - Add Terminal/Python to allowed apps

2. **Permissions (Windows):**
   - Run as Administrator if needed

3. **Linux:**
   ```bash
   sudo apt-get install python3-dev python3-pip
   sudo apt-get install scrot python3-tk python3-dev
   pip3 install pyautogui
   ```

### Image Not Found

- Check image path (use absolute paths)
- Adjust `confidence` (try 0.7-0.9)
- Ensure screenshot matches current screen resolution
- Image scale may differ (retina displays)

### Too Slow

```python
# Reduce pause (but keep safe!)
pyautogui.PAUSE = 0.1

# Remove duration for instant moves
pyautogui.moveTo(100, 100)  # No duration = instant
```

### Too Fast / Unreliable

```python
# Increase pause
pyautogui.PAUSE = 1.0

# Add explicit waits
import time
time.sleep(2)  # Wait for UI to load
```

## Best Practices

1. **Always test visually first** - Watch the automation run
2. **Use delays** - Give UI time to respond
3. **Add error handling** - Check if elements exist
4. **Log actions** - Debug when things go wrong
5. **Use images carefully** - Resolution changes break image matching
6. **Respect the fail-safe** - Never disable it

## Installation

```bash
pip install pyautogui pyscreeze pillow
```

**macOS additional:**
```bash
brew install python-tk
```

**Linux additional:**
```bash
sudo apt-get install python3-dev python3-pip scrot python3-tk
```

## Notes

- PyAutoGUI coordinates start at top-left (0, 0)
- Movement is relative to primary monitor
- Multi-monitor setups use combined coordinate space
- Some apps may require elevated permissions
- Image matching is pixel-perfect by default (use confidence for fuzzy matching)
