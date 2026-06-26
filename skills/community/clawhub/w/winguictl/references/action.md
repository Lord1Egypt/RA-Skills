# Action Commands

Execute interaction operations (click, drag, type, scroll).

## ⚠️ Security Warning

Action commands simulate mouse/keyboard input. **Always use `--dry-run` to preview** before execution. Verify correct `window_id` before performing actions.

## Commands

| Subcommand | Description | Parameters | Example |
|------------|-------------|------------|---------|
| `click` | Click coordinates or element | `--relative-x/y` OR `--absolute-x/y` OR `--element-id` | `action --window-id 12345 click --relative-x 100 --relative-y 200` |
| `click-image` | Click matching image | `--image-path`, `--threshold` | `action --window-id 12345 click-image --image-path button.png` |
| `drag` | Drag from point to point | `--relative-x/y1/2` OR `--absolute-x/y1/2`, `--duration-ms` | `action --window-id 12345 drag --relative-x1 100 --relative-y1 200 --relative-x2 400 --relative-y2 200` |
| `type` | Type text | `--text` | `action --window-id 12345 type --text "hello"` |
| `press-key` | Press single key | `--key` | `action --window-id 12345 press-key --key "{ENTER}"` |
| `hotkey` | Press key chord | `--keys` | `action --window-id 12345 hotkey --keys "{CTRL}" "{A}"` |
| `clear-text` | Clear focused text field | None | `action --window-id 12345 clear-text` |
| `scroll` | Mouse wheel scroll | `--direction`, `--amount`, coordinates (optional) | `action --window-id 12345 scroll --direction down --amount 3` |

## Click Methods

| Method | Command | Mechanism | Best For |
|--------|---------|-----------|----------|
| Element center | `action click --element-id` | Mouse simulation at center | **WeChat, custom controls** |
| UIA pattern | `uia-control click` | UIA InvokePattern | Standard Windows controls, WinUI3 |
| Coordinates | `action click --relative-x/y` | Mouse simulation at point | Fallback when element ID unavailable |

**Recommendation**: Try `uia-control click` first. If no effect, use `action click --element-id`.

## Coordinate Modes

| Mode | Parameters | Description |
|------|------------|-------------|
| Relative | `--relative-x`, `--relative-y` | Window-relative (requires `--window-id`) |
| Absolute | `--absolute-x`, `--absolute-y` | Screen-absolute coordinates |
| Element | `--element-id` | Click element center (requires `--window-id`) |

**Validation**: Relative coordinates must be within window bounds: `0 <= x < width`, `0 <= y < height`.

## Keyboard Operations

### Key Format

All keyboard commands use pywinauto-style braced keys: `{ENTER}`, `{TAB}`, `{ESC}`, `{SPACE}`, `{CTRL}`, `{SHIFT}`, `{ALT}`, etc.

- `type`: Embed keys in text: `"line1{ENTER}line2"`
- `press-key`: Single key: `"{ENTER}"`
- `hotkey`: List or concatenated: `"{CTRL}" "{A}"` or `"{CTRL}{A}"`

### Common Hotkeys

| Operation | Command |
|-----------|---------|
| Select all | `hotkey --keys "{CTRL}" "{A}"` |
| Copy | `hotkey --keys "{CTRL}" "{C}"` |
| Paste | `hotkey --keys "{CTRL}" "{V}"` |
| Cut | `hotkey --keys "{CTRL}" "{X}"` |
| Undo | `hotkey --keys "{CTRL}" "{Z}"` |
| Save | `hotkey --keys "{CTRL}" "{S}"` |

## Scroll

| Parameter | Values | Description |
|-----------|--------|-------------|
| `--direction` | `up`, `down`, `left`, `right` | Scroll direction (required) |
| `--amount` | Integer (default: 1) | Number of wheel notches |
| Coordinates | `--relative-x/y` OR `--absolute-x/y` OR `--element-id` | Scroll position (default: window center, requires `--window-id`) |

**Note**: `action scroll` uses integer `--amount` (wheel notches). Different from `uia-control scroll` which uses `--amount line|page`.

## Output Information

Both `--dry-run` and execution output include:

**Window Info**: `window_id`, `window_title`

**Coordinates**: `relative` (window-relative), `absolute` (screen-absolute)

**Element at Point** (UIA): `name`, `control_type`, `class_name`, `automation_id`, `runtime_id`

**Control Info** (Win32): `hwnd`, `control_text`, `control_class`, `control_type`

## Execution Behavior

Before executing actions, commands will:
1. Focus target window (bring to foreground)
2. Move mouse cursor to specified position
3. Execute the action

This ensures proper input delivery.

## Best Practices

- **Re-snapshot after actions**: UI state changes after clicks/typing
- **Use `--dry-run`**: Preview operations before execution
- **Prefer element IDs**: More reliable than coordinates
- **Validate coordinates**: Ensure within window bounds
