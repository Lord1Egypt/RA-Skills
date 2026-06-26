---
name: virtual-desktop-browser
description: Launch Chromium in non-headless mode inside Xvfb virtual display (fixed 1200x720x24) and automate with human-like mouse/keyboard/screenshot operations. Use for bot-resistant sites like Xiaohongshu and X/Twitter where GUI simulation is required.
---

# Virtual Desktop Browser Skill

This skill provides a deterministic GUI automation runtime:
- Xvfb virtual display (`1200x720x24`)
- Chromium non-headless browser
- PyAutoGUI control (click/type/hotkey/scroll)

## Required system packages

```bash
apt-get update
apt-get install -y xvfb chromium-browser \
  libnss3 libgconf-2-4 libxss1 libasound2 \
  libatk1.0-0 libatk-bridge2.0-0 libcups2 \
  libdrm2 libgbm1 libgtk-3-0 libxshmfence1 x11-utils
```

## Python dependencies

```bash
pip install -r requirements.txt
```

## Tool surface

All tools return JSON dicts.

- `browser_start(url=None, display=None)` — start Xvfb + Chromium
- `browser_stop()` — close processes
- `browser_snapshot(region=None)` — screenshot as Base64 PNG
- `browser_click(x, y, button='left', clicks=1, duration=0.5)` — move + click
- `browser_type(text, interval=0.05, wpm=None)` — type at focus
- `browser_hotkey(keys, interval=0.05)` — key combos
- `browser_scroll(clicks=1, direction='vertical', x=None, y=None)` — mouse wheel
- `browser_find_image(image_path, confidence=0.8)` — template matching (OpenCV)
- `browser_get_pixel_color(x, y)` — read RGB
- `browser_activate_window(title_substring)` — focus window by title

## Notes

- Browser lifecycle is manual: start once, multi-step flow, then stop.
- Display auto-assigns (`:99..:199`) if not provided.
- Failsafe: moving mouse to bottom-right corner triggers pyautogui abort.

## Language

See `docs/` for translations:
- [English](docs/en.md)
- [Español](docs/es.md)
- [العربية](docs/ar.md)
