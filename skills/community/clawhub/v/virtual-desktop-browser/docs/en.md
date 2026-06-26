# Virtual Desktop Browser Skill (English)

Run **Chromium in non-headless mode** on **Xvfb virtual display (fixed 1200x720x24)** and perform **human-like automation** with PyAutoGUI. Ideal for bot-resistant sites like Xiaohongshu and X/Twitter.

[中文](../README.md) | [Español](es.md) | [العربية](ar.md)

---

## Features

| Feature | Description |
|---------|-------------|
| Virtual Display | Xvfb standalone X Server, 1200x720x24 |
| Non-headless Browser | Chromium with GUI in virtual screen |
| Mouse Simulation | Move, click (left/right/middle/double), drag |
| Keyboard Simulation | Text input, hotkeys, key combos |
| Scroll | Vertical and horizontal scrolling |
| Screenshot | Full or region capture, Base64 PNG |
| Image Matching | Find template images on screen (OpenCV) |
| Pixel Color | Read RGB color at coordinates |
| Window Management | Focus window by title substring |
| Auto Display Assignment | Avoids multi-session conflicts (:99 ~ :199) |
| Safety Abort | Mouse to bottom-right corner stops all (Failsafe) |

---

## Installation

### System dependencies (Ubuntu/Debian)

```bash
apt-get update
apt-get install -y xvfb chromium-browser \
  libnss3 libgconf-2-4 libxss1 libasound2 \
  libatk1.0-0 libatk-bridge2.0-0 libcups2 \
  libdrm2 libgbm1 libgtk-3-0 libxshmfence1 x11-utils
```

### Python dependencies

```bash
pip install -r requirements.txt
```

### Install skill

```bash
npx skills add https://github.com/NHZallen/virtual-desktop-browser-skill
```

---

## Tool Reference

### `browser_start(url=None, display=None)`

Start Xvfb and Chromium.

| Parameter | Type | Description |
|-----------|------|-------------|
| `url` | str (optional) | Initial URL, default about:blank |
| `display` | str (optional) | X display, e.g. `:99`. Auto-assigned if omitted |

**Returns:**
```json
{
  "status": "started",
  "display": ":99",
  "xvfb_pid": 12345,
  "chrome_pid": 12346,
  "resolution": "1200x720x24"
}
```

---

### `browser_stop()`

Close Chromium and Xvfb, release resources.

**Returns:** `{ "status": "stopped" }`

---

### `browser_snapshot(region=None)`

Capture virtual screen, returns Base64 PNG.

| Parameter | Type | Description |
|-----------|------|-------------|
| `region` | tuple (optional) | `(left, top, width, height)` |

**Returns:**
```json
{
  "image_base64": "iVBORw0KGgo...",
  "width": 1200,
  "height": 720
}
```

---

### `browser_click(x, y, button='left', clicks=1, duration=0.5)`

Move mouse and click.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `x` | int | required | X coordinate |
| `y` | int | required | Y coordinate |
| `button` | str | `left` | `left` / `right` / `middle` |
| `clicks` | int | `1` | Click count (1=single, 2=double) |
| `duration` | float | `0.5` | Movement time in seconds (0=instant) |

---

### `browser_type(text, interval=0.05, wpm=None)`

Type text at current focus.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | str | required | Text to type |
| `interval` | float | `0.05` | Key interval in seconds |
| `wpm` | int (optional) | — | Words per minute for human-like speed |

---

### `browser_hotkey(keys, interval=0.05)`

Press key combination.

| Parameter | Type | Description |
|-----------|------|-------------|
| `keys` | list[str] | Key names, e.g. `["ctrl", "c"]` |
| `interval` | float | Key interval in seconds |

---

### `browser_scroll(clicks=1, direction='vertical', x=None, y=None)`

Scroll mouse wheel.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `clicks` | int | `1` | Scroll amount (+up/left, −down/right) |
| `direction` | str | `vertical` | `vertical` or `horizontal` |
| `x`, `y` | int (optional) | — | Scroll position |

---

### `browser_find_image(image_path, confidence=0.8)`

Find template image on screen.

**Returns:** `{ "found": true, "x": 100, "y": 200, "width": 50, "height": 50 }` or `{ "found": false }`

---

### `browser_get_pixel_color(x, y)`

Get pixel RGB color.

**Returns:** `{ "r": 255, "g": 255, "b": 255 }`

---

### `browser_activate_window(title_substring)`

Focus window by partial title match.

---

## Lifecycle

```
browser_start() → operations → browser_stop()
```

Start once, run multiple operations, then stop manually. No auto-shutdown. Multi-session: use different `display` numbers.

---

## Example: Browse Xiaohongshu

```python
browser_start(url="https://www.xiaohongshu.com/explore")
time.sleep(3)
browser_scroll(clicks=-3)
browser_snapshot()
browser_stop()
```

---

## Safety

- **Failsafe:** Move mouse to bottom-right corner (1199, 719) to abort
- **Independent Display:** Each session runs on its own X Server

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `Missing: Xvfb` | `apt-get install -y xvfb` |
| `Missing: chromium-browser` | `apt-get install -y chromium-browser` |
| PyAutoGUI DISPLAY error | Confirm `browser_start()` was called |
| Image matching fails | Use high-contrast template, lower `confidence` |

---

## Author

Creator: **Allen Niu**  
License: MIT-0
