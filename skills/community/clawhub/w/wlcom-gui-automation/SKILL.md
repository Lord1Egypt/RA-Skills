---
name: wlcom-gui-automation
description: Use wlcctrl on KylinOS V11 Desktop / UKUI / wlcom Wayland desktops for GUI automation tests: discover outputs/windows, handle scale-aware coordinates, move/click/type with keyboard and mouse, capture windows/screens/regions, move/resize windows, and verify results from screenshots.
---

# wlcom GUI Automation

Use this skill when automating GUI tests on KylinOS V11 Desktop（银河麒麟桌面操作系统 V11）using wlcom's `wlcctrl` command.

## Ground rules

- V11 uses Wayland + UKUI + `wayland-compositor`/`wlcom`; do not assume X11 tools are authoritative.
- Prefer `wlcctrl` for window discovery, screenshots, pointer movement, clicks, keys, and window placement.
- Always inspect scale before calculating pointer coordinates.
- `wlcctrl --mousemove` is **absolute**, despite the man page saying displacement.
- On tested V11 machines, `--mousemove` input must be **logical coordinate × output scale**; `--getmouselocation` returns logical coordinates.
- `--windowmove -x/-y` uses logical coordinates; do **not** multiply by scale.
- Current `wlcctrl v1.0.0` help/man shows screenshot support, but no recording subcommand. If recording is required, check for other wlcom tools or use an approved recorder.

## Quick workflow

```bash
# 1. Confirm tool and version
command -v wlcctrl
wlcctrl --version

# 2. Inspect output UUID and scale
wlcctrl --outputs
wlcctrl --getdisplaygeometry <output_uuid>
gsettings get org.ukui.SettingsDaemon.plugins.xsettings scaling-factor 2>/dev/null || true

# 3. Find target window
wlcctrl --list
wlcctrl --search '<app_id_or_title_regex>'
wlcctrl --getactivewindow
wlcctrl --getwindowgeometry <w_uuid>

# 4. Capture for visual coordinate identification
wlcctrl --windowcapture <w_uuid> --path /tmp/window.png

# 5. Move and click by scaled pointer coordinates
# logical_screen_x = window_x + screenshot_relative_x
# logical_screen_y = window_y + screenshot_relative_y
# mousemove_x = round(logical_screen_x * scale)
# mousemove_y = round(logical_screen_y * scale)
wlcctrl --mousemove <mousemove_x>,<mousemove_y>
wlcctrl --getmouselocation
wlcctrl --mousebutton 1

# 6. Verify by screenshot or pixel/window state
wlcctrl --windowcapture <w_uuid> --path /tmp/after.png
```

## Helper scripts

The skill includes scripts under `scripts/`:

- `scripts/wlcctrl-info.sh` — print version, outputs, display geometry, scale candidates, active window, and mouse location.
- `scripts/wlcctrl-window-click.sh <window_uuid> <relative_x> <relative_y> [button]` — click a point relative to a window screenshot. It reads window geometry and output scale, converts to scaled `--mousemove` input, verifies location, then clicks.
- `scripts/wlcctrl-move-window.sh <window_uuid> <x> <y>` — move a window using logical coordinates and verify geometry.

Resolve script paths relative to this `SKILL.md` directory before running.

## Common commands

### Outputs and scale

```bash
wlcctrl --outputs
wlcctrl --getdisplaygeometry <output_uuid>
```

Look for:

```text
physical size: 300x190 mm
scale: 1.750000
mode: 2880 x 1800 @ 90
position: 0, 0
```

`xdpyinfo` may report Xwayland logical DPI (for example `96x96`) and should not be used alone for Wayland coordinate conversion.

### Windows

```bash
wlcctrl --list
wlcctrl --search '<regex>'
wlcctrl --getactivewindow
wlcctrl --getwindowname <w_uuid>
wlcctrl --getwindowgeometry <w_uuid>
wlcctrl --windowactivate <w_uuid>
wlcctrl --windowmove <w_uuid> -x 0 -y 0
wlcctrl --windowsize <w_uuid> -w 800 -h 600
```

### Screenshots

```bash
wlcctrl --windowcapture <w_uuid> --path /tmp/window.png
wlcctrl --fullscreencapture --path /tmp/full.png
wlcctrl --setarea <x,y,width,height> --path /tmp/area.png
wlcctrl --workspacecapture <workspace_uuid:output_uuid> --path /tmp/workspace.png
```

### Keyboard and pointer

```bash
wlcctrl --key ctrl+alt+t
wlcctrl --keystring 'text to type'
wlcctrl --mousebutton 1
wlcctrl --mousepress 1 --mouserelease 1
wlcctrl --scroll -y 10
wlcctrl --getmouselocation
```

For drag actions, move to start, press, move to end, release. Remember `--mousemove` coordinates are scaled absolute coordinates.

## Coordinate recipe

Given:

- output scale = `S`
- window geometry = `(WX, WY) WIDTH x HEIGHT`
- target point in captured window image = `(RX, RY)`

Then:

```text
logical_x = WX + RX
logical_y = WY + RY
mousemove_x = round(logical_x * S)
mousemove_y = round(logical_y * S)
```

Run:

```bash
wlcctrl --mousemove "${mousemove_x},${mousemove_y}"
wlcctrl --getmouselocation   # should be near logical_x,logical_y
wlcctrl --mousebutton 1
```

Known tested example on one V11 machine:

- output `eDP-1`, scale `1.75`
- calculator window `geometry: (607, 176) 432 x 628`
- `=` center in window screenshot `(376,593)`
- logical target `(983,769)`
- `--mousemove` input about `(1720,1346)`
- `--getmouselocation` returns about `(983,769)`

## Test pattern

For a reliable GUI automation test:

1. Normalize the window: activate and optionally move to `(0,0)`.
2. Capture the window.
3. Identify target controls from screenshot coordinates.
4. Click via scaled absolute `--mousemove` + `--mousebutton`.
5. Capture again and verify visually or with OCR/image analysis.
6. Log every `wlcctrl` command and its output for reproducibility.

## Safety

- Avoid `--windowclose` and `--windowkill` unless the user explicitly asks.
- Before sending destructive keystrokes, confirm target window UUID/title.
- Store test screenshots/logs under a project `artifacts/` directory when possible.
