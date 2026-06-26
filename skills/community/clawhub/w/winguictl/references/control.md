# Control Commands

Directly control Win32 controls and UIA elements.

## ⚠️ Security Warning

Control commands manipulate UI elements. Verify correct `hwnd`, `automation_id`, or `runtime_id` before operations.

## Win32 Control Operations

Control Win32 controls via HWND handles. Use `snapshot hwnd` to obtain `hwnd`.

### Commands

| Subcommand | Description | Parameters |
|------------|-------------|------------|
| `click` | Click control | `--hwnd` |
| `double-click` | Double-click control | `--hwnd` |
| `right-click` | Right-click control | `--hwnd` |
| `get-text` | Get control text | `--hwnd` |
| `set-text` | Set control text | `--hwnd`, `text` (positional) |
| `set-focus` | Set focus to control | `--hwnd` |
| `type-keys` | Type keys to control | `--hwnd`, `keys` (positional) |
| `send-chars` | Send chars to inactive window | `--hwnd`, `chars` (positional) |
| `send-keystrokes` | Send keystrokes to inactive window | `--hwnd`, `keystrokes` (positional) |
| `check` | Check checkbox | `--hwnd` |
| `uncheck` | Uncheck checkbox | `--hwnd` |
| `check-by-click` | Check checkbox by click | `--hwnd` |
| `uncheck-by-click` | Uncheck checkbox by click | `--hwnd` |
| `is-checked` | Get checkbox state | `--hwnd` |
| `combo-select` | Select combobox item | `--hwnd`, `item` (positional), `--index` |
| `combo-items` | Get combobox items | `--hwnd` |
| `combo-selected-index` | Get selected index | `--hwnd` |
| `combo-selected-text` | Get selected text | `--hwnd` |
| `listbox-select` | Select listbox item | `--hwnd`, `item` (positional) |
| `listbox-items` | Get listbox items | `--hwnd` |
| `listbox-selected-indices` | Get selected indices | `--hwnd` |

### Usage

```powershell
# Click control
control --hwnd 12345 click

# Set text
control --hwnd 12345 set-text "New Text"

# Select combobox item
control --hwnd 12345 combo-select "Option 1"
control --hwnd 12345 combo-select 0 --index
```

## UIA Element Operations

Control UIA elements via automation_id or runtime_id. Use `snapshot uia` to obtain element IDs.

### Commands

| Subcommand | Description | Parameters |
|------------|-------------|------------|
| `click` | Click element | `--window-id`, `--element-id` |
| `double-click` | Double-click element | `--window-id`, `--element-id` |
| `right-click` | Right-click element | `--window-id`, `--element-id` |
| `invoke` | Invoke element (buttons) | `--window-id`, `--element-id` |
| `toggle` | Toggle element state | `--window-id`, `--element-id`, `--target-state` |
| `get-toggle-state` | Get toggle state | `--window-id`, `--element-id` |
| `get-text` | Get element text | `--window-id`, `--element-id` |
| `get-value` | Get element value | `--window-id`, `--element-id` |
| `set-value` | Set element value | `--window-id`, `--element-id`, `value` (positional) |
| `set-text` | Set element text | `--window-id`, `--element-id`, `text` (positional), `--verify-change` |
| `set-focus` | Set focus to element | `--window-id`, `--element-id` |
| `type-keys` | Type keys to element | `--window-id`, `--element-id`, `keys` (positional) |
| `select` | Select element | `--window-id`, `--element-id` |
| `is-selected` | Check if selected | `--window-id`, `--element-id` |
| `expand` | Expand node | `--window-id`, `--element-id` |
| `collapse` | Collapse node | `--window-id`, `--element-id` |
| `is-expanded` | Check if expanded | `--window-id`, `--element-id` |
| `scroll` | Scroll element | `--window-id`, `--element-id`, `direction` (positional), `--amount`, `--count` |
| `combo-select` | Select combobox item | `--window-id`, `--element-id`, `item` (positional), `--index` |
| `combo-items` | Get combobox items | `--window-id`, `--element-id` |
| `combo-selected-text` | Get selected text | `--window-id`, `--element-id` |
| `combo-selected-index` | Get selected index | `--window-id`, `--element-id` |
| `list-items` | Get list items | `--window-id`, `--element-id` |
| `list-select` | Select list item | `--window-id`, `--element-id`, `item` (positional) |
| `list-selected-items` | Get selected items | `--window-id`, `--element-id` |
| `tab-select` | Select tab | `--window-id`, `--element-id`, `item` (positional) |
| `tab-selected` | Get selected tab | `--window-id`, `--element-id` |
| `tab-count` | Get tab count | `--window-id`, `--element-id` |
| `slider-value` | Get slider value | `--window-id`, `--element-id` |
| `slider-set` | Set slider value | `--window-id`, `--element-id`, `value` (positional) |
| `slider-min` | Get slider minimum | `--window-id`, `--element-id` |
| `slider-max` | Get slider maximum | `--window-id`, `--element-id` |
| `window-close` | Close window | `--window-id`, `--element-id` |
| `window-minimize` | Minimize window | `--window-id`, `--element-id` |
| `window-maximize` | Maximize window | `--window-id`, `--element-id` |
| `window-restore` | Restore window | `--window-id`, `--element-id` |
| `window-state` | Get window state | `--window-id`, `--element-id` |
| `transform-move` | Move element | `--window-id`, `--element-id`, `--absolute-x`, `--absolute-y` |
| `transform-resize` | Resize element | `--window-id`, `--element-id`, `width` `height` (positional) |
| `transform-rotate` | Rotate element | `--window-id`, `--element-id`, `degrees` (positional) |

### Usage

```powershell
# Click element
uia-control --window-id 12345 --element-id "42-3155764" click

# Set text (idempotent)
uia-control --window-id 12345 --element-id "Edit1" set-text "Hello" --verify-change

# Toggle with target state (idempotent)
uia-control --window-id 12345 --element-id "Check1" toggle --target-state on

# Scroll
uia-control --window-id 12345 --element-id "List1" scroll down --amount page --count 3
```

## Element ID Format

- **automation_id**: String identifier (e.g., `"Button1"`)
- **runtime_id**: Hyphen-separated numeric ID (e.g., `"42-3155764"`)

**Prefer `runtime_id`** - guaranteed unique within desktop session. `automation_id` may have duplicates in Qt apps.

## Click Method Selection

| Command | Mechanism | Best For |
|---------|-----------|----------|
| `uia-control click` | UIA InvokePattern | Standard Windows controls, WinUI3 |
| `action click --element-id` | Mouse simulation at center | **WeChat, custom controls** |

**Recommendation**: Try `uia-control click` first. If no effect, use `action click --element-id`.

## Idempotent Operations

### Toggle with Target State

```powershell
# Only toggles if current state differs
uia-control --window-id <id> --element-id "Check1" toggle --target-state on
```

Response includes `toggled: true/false` to indicate whether toggle was performed.

### Set Text with Verify Change

```powershell
# Only sets if current value differs
uia-control --window-id <id> --element-id "Edit1" set-text "Hello" --verify-change
```

Response includes `changed: true/false` and `reason` to indicate whether text was modified.

## Scroll Parameters

| Parameter | Values | Description |
|-----------|--------|-------------|
| `direction` | `up`, `down`, `left`, `right` | Scroll direction (positional) |
| `--amount` | `line`, `page` | Scroll amount |
| `--count` | Integer (default: 1) | Number of scrolls |

**Note**: `uia-control scroll` uses `--amount line|page`. Different from `action scroll` which uses integer `--amount` (wheel notches).

## UIA Actions

`supported_actions` in `snapshot uia` output shows available operations:

| Action | Required Pattern |
|--------|-----------------|
| `invoke` | InvokePattern |
| `get-value`, `set-value`, `set-text` | ValuePattern |
| `toggle`, `get-toggle-state` | TogglePattern |
| `expand`, `collapse`, `is-expanded` | ExpandCollapsePattern |
| `scroll` | ScrollPattern |
| `select`, `is-selected` | SelectionItemPattern |
| `slider-value`, `slider-set`, `slider-min`, `slider-max` | RangeValuePattern |
| `window-close`, `window-minimize`, `window-maximize`, `window-restore`, `window-state` | WindowPattern |
| `transform-move`, `transform-resize`, `transform-rotate` | TransformPattern |

**Always available**: `click`, `double-click`, `right-click`, `set-focus`, `type-keys`

## Best Practices

- **Re-snapshot after actions**: UI state changes after operations
- **Prefer runtime_id**: More reliable than automation_id
- **Use idempotent operations**: Prevent unnecessary changes
- **Verify element support**: Check `supported_actions` before using UIA patterns
