# Dependencies and Installation

This skill uses Python-based automation tools.

## Required

### Browser automation
- Python 3.10+
- `playwright`
- Browser binaries installed via `playwright install`

Install:
```bash
pip install playwright
playwright install
```

### Desktop automation
- Python 3.10+
- `pyautogui`

Install:
```bash
pip install pyautogui
```

## Optional but recommended

### Image-based targeting
- `opencv-python`

Why:
- Enables confidence-based image matching in PyAutoGUI

Install:
```bash
pip install opencv-python
```

### Screenshot / image handling
- `pillow`

Install:
```bash
pip install pillow
```

## Suggested combined setup

```bash
pip install playwright pyautogui opencv-python pillow
playwright install
```

## Windows notes

- Run scripts from the same Python environment that has the packages installed
- If image matching is used, install `opencv-python` or confidence-based matching may fail
- Keep display scaling stable when using coordinate-based automation

## Quick verification

Browser:
```bash
python -c "from playwright.sync_api import sync_playwright; print('playwright ok')"
```

Desktop:
```bash
python -c "import pyautogui; print('pyautogui ok')"
```
