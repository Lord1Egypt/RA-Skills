# Driver Test Steps

This document describes how to test the Win32Driver and UIADriver functionality.

---

## Preparation

### Install Dependencies

```powershell
pip install -r requirements.txt
```

### Launch Test Applications and Get Window IDs

```powershell
Start-Process calc
Start-Process notepad
python scripts\winguictl.py window list
```

Example output:
```
- "计算器" [window_id="14294402" absolute_rect=(591,150 600x700) pid="56816" process="ApplicationFrameHost.exe"]
- "无标题 - Notepad" [window_id="1119842" absolute_rect=(2102,182 894x805) pid="11776" process="Notepad.exe"]
```

---

## Window Management Tests

| Feature | Command | ☑ |
|---------|---------|---|
| List windows | `window list` | ☑ |
| Focus window | `window --window-id <id> focus` | ☑ |
| Close window | `window --window-id <id> close` | ☑ |
| Minimize window | `window --window-id <id> minimize` | ☑ |
| Maximize window | `window --window-id <id> maximize` | ☑ |
| Restore window | `window --window-id <id> restore` | ☑ |
| Move window | `window --window-id <id> move --x 100 --y 100` | ☑ |
| Resize window | `window --window-id <id> resize --width 800 --height 600` | ☑ |

```powershell
python scripts\winguictl.py window list
python scripts\winguictl.py window --window-id <window_id> focus
python scripts\winguictl.py window --window-id <window_id> close
python scripts\winguictl.py window --window-id <window_id> minimize
python scripts\winguictl.py window --window-id <window_id> maximize
python scripts\winguictl.py window --window-id <window_id> restore
python scripts\winguictl.py window --window-id <window_id> move --x 100 --y 100
python scripts\winguictl.py window --window-id <window_id> resize --width 800 --height 600
```

---

## Action Tests

| Feature | Command | ☑ |
|---------|---------|---|
| Type text | `action --window-id <id> type --text "Hello World"` | ☑ |
| Press key | `action --window-id <id> press-key --key "{ENTER}"` | ☑ |
| Hotkey | `action --window-id <id> hotkey --keys "{CTRL}" "{S}"` | ☑ |
| Click coordinates | `action --window-id <id> click --relative-x 100 --relative-y 100` | ☑ |
| Click element | `action --window-id <id> click --element-id num1Button` | ☑ |
| Click image | `action --window-id <id> click-image --image-path template.png` | ☑ |
| Drag | `action --window-id <id> drag --relative-x1 100 --relative-y1 100 --relative-x2 200 --relative-y2 200` | ☑ |
| Clear text | `action --window-id <id> clear-text` | ☑ |
| Scroll | `action --window-id <id> scroll --direction down --amount 3` | ☑ |
| Dry-run | `action --window-id <id> click --relative-x 100 --relative-y 100 --dry-run` | ☑ |

```powershell
python scripts\winguictl.py action --window-id <window_id> type --text "Hello World"
python scripts\winguictl.py action --window-id <window_id> press-key --key "{ENTER}"
python scripts\winguictl.py action --window-id <window_id> press-key --key "{ESC}"
python scripts\winguictl.py action --window-id <window_id> hotkey --keys "{CTRL}" "{S}"
python scripts\winguictl.py action --window-id <window_id> click --relative-x 100 --relative-y 100
python scripts\winguictl.py action --window-id <window_id> click --element-id num1Button
python scripts\winguictl.py action --window-id <window_id> drag --relative-x1 100 --relative-y1 100 --relative-x2 200 --relative-y2 200
python scripts\winguictl.py action --window-id <window_id> clear-text
python scripts\winguictl.py action --window-id <window_id> scroll --direction down --amount 3
```

---

## Snapshot Tests

| Feature | Command | ☑ |
|---------|---------|---|
| UIA snapshot | `snapshot --window-id <id> uia` | ☑ |
| UIA (fast) | `snapshot --window-id <id> uia --skip-actions` | ☑ |
| HWND snapshot | `snapshot --window-id <id> hwnd` | ☑ |
| OCR snapshot | `snapshot --window-id <id> ocr` | ☑ |

```powershell
python scripts\winguictl.py snapshot --window-id <window_id> uia
python scripts\winguictl.py snapshot --window-id <window_id> uia --skip-actions
python scripts\winguictl.py snapshot --window-id <window_id> hwnd
python scripts\winguictl.py snapshot --window-id <window_id> ocr
```

---

## Find Tests

| Feature | Command | ☑ |
|---------|---------|---|
| Find by text | `find --window-id <id> text "Hello"` | ☑ |
| Find by text (exact) | `find --window-id <id> text "Hello" --exact` | ☑ |
| Find UIA by text | `find --window-id <id> uia --text "One"` | ☑ |
| Find UIA by control type | `find --window-id <id> uia --control-type Button` | ☑ |
| Find by OCR | `find --window-id <id> ocr "Text"` | ☑ |
| Find by image | `find --window-id <id> image --image-path template.png` | ☑ |

```powershell
python scripts\winguictl.py find --window-id <window_id> text "Hello"
python scripts\winguictl.py find --window-id <window_id> text "Hello" --exact
python scripts\winguictl.py find --window-id <window_id> uia --text "One"
python scripts\winguictl.py find --window-id <window_id> uia --control-type Button
python scripts\winguictl.py find --window-id <window_id> uia --control-type Edit
python scripts\winguictl.py find --window-id <window_id> ocr "Text"
python scripts\winguictl.py find --window-id <window_id> image --image-path template.png
```

---

## Screenshot Tests

| Feature | Command | ☑ |
|---------|---------|---|
| Full window | `screenshot --window-id <id> --output screenshot.png` | ☑ |
| Region | `screenshot --window-id <id> --output region.png --x 100 --y 100 --width 200 --height 200` | ☑ |

```powershell
python scripts\winguictl.py screenshot --window-id <window_id> --output screenshot.png
python scripts\winguictl.py screenshot --window-id <window_id> --output region.png --x 100 --y 100 --width 200 --height 200
```

---

## Win32Driver Tests

### Get Control hwnd

```powershell
python scripts\winguictl.py snapshot --window-id <window_id> hwnd
```

Notepad output example:
```
- "" [control_type="Edit" class="RichEditD2DPT" hwnd="1317464" visible=true enabled=true control_id="0"]
```

### Test Operations

| Feature | Command | ☑ |
|---------|---------|---|
| Click | `control --hwnd <hwnd> click` | ☑ |
| Double click | `control --hwnd <hwnd> double-click` | ☑ |
| Right click | `control --hwnd <hwnd> right-click` | ☑ |
| Set text | `control --hwnd <hwnd> set-text "Test"` | ☑ |
| Get text | `control --hwnd <hwnd> get-text` | ☑ |
| Set focus | `control --hwnd <hwnd> set-focus` | ☑ |
| Type keys | `control --hwnd <hwnd> type-keys "Hello"` | ☑ |
| Type special keys | `control --hwnd <hwnd> type-keys "{CTRL}a{CTRL}{DELETE}"` | ☑ |
| Send chars (inactive) | `control --hwnd <hwnd> send-chars "Hello"` | ☑ |
| Send keystrokes (inactive) | `control --hwnd <hwnd> send-keystrokes "{ENTER}"` | ☑ |
| Check checkbox | `control --hwnd <hwnd> check` | ☑ |
| Uncheck checkbox | `control --hwnd <hwnd> uncheck` | ☑ |
| Checkbox state | `control --hwnd <hwnd> is-checked` | ☑ |
| Combo select | `control --hwnd <hwnd> combo-select 0` | ☑ |
| Combo select by text | `control --hwnd <hwnd> combo-select "Text"` | ☑ |
| Combo items | `control --hwnd <hwnd> combo-items` | ☑ |
| Combo selected index | `control --hwnd <hwnd> combo-selected-index` | ☑ |
| Combo selected text | `control --hwnd <hwnd> combo-selected-text` | ☑ |
| Combo select by index | `control --hwnd <hwnd> combo-select 0 --index` | ☑ |
| Listbox select | `control --hwnd <hwnd> listbox-select 0` | ☑ |
| Listbox items | `control --hwnd <hwnd> listbox-items` | ☑ |
| Listbox selected indices | `control --hwnd <hwnd> listbox-selected-indices` | ☑ |

```powershell
# Click operations
python scripts\winguictl.py control --hwnd <hwnd> click
python scripts\winguictl.py control --hwnd <hwnd> double-click
python scripts\winguictl.py control --hwnd <hwnd> right-click

# Text operations
python scripts\winguictl.py control --hwnd <hwnd> set-text "Test text"
python scripts\winguictl.py control --hwnd <hwnd> get-text
python scripts\winguictl.py control --hwnd <hwnd> set-focus

# Keyboard input
python scripts\winguictl.py control --hwnd <hwnd> type-keys "Hello World"
python scripts\winguictl.py control --hwnd <hwnd> type-keys "{CTRL}a{CTRL}{DELETE}"

# Silent input (inactive window)
python scripts\winguictl.py control --hwnd <hwnd> send-chars "Hello"
python scripts\winguictl.py control --hwnd <hwnd> send-keystrokes "{ENTER}New line{ENTER}"

# Checkbox
python scripts\winguictl.py control --hwnd <hwnd> check
python scripts\winguictl.py control --hwnd <hwnd> uncheck
python scripts\winguictl.py control --hwnd <hwnd> is-checked
python scripts\winguictl.py control --hwnd <hwnd> check-by-click
python scripts\winguictl.py control --hwnd <hwnd> uncheck-by-click

# Combobox
python scripts\winguictl.py control --hwnd <hwnd> combo-select 0
python scripts\winguictl.py control --hwnd <hwnd> combo-select "Text"
python scripts\winguictl.py control --hwnd <hwnd> combo-select 0 --index
python scripts\winguictl.py control --hwnd <hwnd> combo-items
python scripts\winguictl.py control --hwnd <hwnd> combo-selected-index
python scripts\winguictl.py control --hwnd <hwnd> combo-selected-text

# Listbox
python scripts\winguictl.py control --hwnd <hwnd> listbox-select 0
python scripts\winguictl.py control --hwnd <hwnd> listbox-items
python scripts\winguictl.py control --hwnd <hwnd> listbox-selected-indices
```

---

## UIADriver Tests

### Get Element IDs

```powershell
python scripts\winguictl.py snapshot --window-id <window_id> uia
```

Calculator output example:
```
- "一" [control_type="Button" class="Button" automation_id="num1Button" enabled=true rect=(78,593 64x47) runtime_id="42-11150588-4-65"]
- "加" [control_type="Button" class="Button" automation_id="plusButton" enabled=true rect=(275,593 63x47) runtime_id="42-11150588-4-61"]
```

Notepad text editor:
```
- "文本编辑器" [control_type="Document" class="RichEditD2DPT" enabled=true runtime_id="42-1317464"]
```

#### Element ID Format

The `--element-id` parameter accepts:
- **automation_id**: e.g., `num1Button`, `plusButton`, `equalButton`
- **runtime_id**: e.g., `42-11150588-4-65`

```powershell
# Using automation_id
python scripts\winguictl.py uia-control --window-id <window_id> --element-id num1Button click

# Using runtime_id
python scripts\winguictl.py uia-control --window-id <window_id> --element-id "42-11150588-4-65" click
```

### Test Operations

| Feature | Command | ☑ |
|---------|---------|---|
| Click | `uia-control --element-id <id> click` | ☑ |
| Double click | `uia-control --element-id <id> double-click` | ☑ |
| Right click | `uia-control --element-id <id> right-click` | ☑ |
| Invoke | `uia-control --element-id <id> invoke` | ☑ |
| Get text | `uia-control --element-id <id> get-text` | ☑ |
| Set text | `uia-control --element-id <id> set-text "Test"` | ☑ |
| Set text (verify) | `uia-control --element-id <id> set-text "Test" --verify-change` | ☑ |
| Set focus | `uia-control --element-id <id> set-focus` | ☑ |
| Type keys | `uia-control --element-id <id> type-keys "Hello"` | ☑ |
| Type special keys | `uia-control --element-id <id> type-keys "{ENTER}"` | ☑ |
| Scroll down | `uia-control --element-id <id> scroll down` | ☑ |
| Scroll line | `uia-control --element-id <id> scroll down --amount line --count 5` | ☑ |
| Expand | `uia-control --element-id <id> expand` | ☑ |
| Collapse | `uia-control --element-id <id> collapse` | ☑ |
| Is expanded | `uia-control --element-id <id> is-expanded` | ☑ |
| Toggle | `uia-control --element-id <id> toggle` | ☑ |
| Toggle target state | `uia-control --element-id <id> toggle --target-state on` | ☑ |
| Get toggle state | `uia-control --element-id <id> get-toggle-state` | ☑ |
| Select | `uia-control --element-id <id> select` | ☑ |
| Is selected | `uia-control --element-id <id> is-selected` | ☑ |
| Get value | `uia-control --element-id <id> get-value` | ☑ |
| Set value | `uia-control --element-id <id> set-value 50` | ☑ |
| Combo select | `uia-control --element-id <id> combo-select 0` | ☑ |
| Combo select by index | `uia-control --element-id <id> combo-select 0 --index` | ☑ |
| Combo items | `uia-control --element-id <id> combo-items` | ☑ |
| Combo selected text | `uia-control --element-id <id> combo-selected-text` | ☑ |
| Combo selected index | `uia-control --element-id <id> combo-selected-index` | ☑ |
| List items | `uia-control --element-id <id> list-items` | ☑ |
| List select | `uia-control --element-id <id> list-select 0` | ☑ |
| List selected items | `uia-control --element-id <id> list-selected-items` | ☑ |
| Tab select | `uia-control --element-id <id> tab-select 0` | ☑ |
| Tab selected | `uia-control --element-id <id> tab-selected` | ☑ |
| Tab count | `uia-control --element-id <id> tab-count` | ☑ |
| Slider value | `uia-control --element-id <id> slider-value` | ☑ |
| Slider set | `uia-control --element-id <id> slider-set 50.0` | ☑ |
| Slider min | `uia-control --element-id <id> slider-min` | ☑ |
| Slider max | `uia-control --element-id <id> slider-max` | ☑ |
| Window close | `uia-control --element-id <id> window-close` | ☑ |
| Window minimize | `uia-control --element-id <id> window-minimize` | ☑ |
| Window maximize | `uia-control --element-id <id> window-maximize` | ☑ |
| Window restore | `uia-control --element-id <id> window-restore` | ☑ |
| Window state | `uia-control --element-id <id> window-state` | ☑ |
| Transform move | `uia-control --element-id <id> transform-move --absolute-x 100 --absolute-y 200` | ☑ |
| Transform resize | `uia-control --element-id <id> transform-resize 100 200` | ☑ |
| Transform rotate | `uia-control --element-id <id> transform-rotate 45.0` | ☑ |

```powershell
# Click operations
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> click
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> double-click
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> right-click
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> invoke

# Text operations
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> set-text "Test text"
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> set-text "Test text" --verify-change
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> get-text
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> set-focus

# Keyboard input
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> type-keys "Hello World"
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> type-keys "{ENTER}"

# Scroll
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> scroll down
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> scroll up
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> scroll down --amount line --count 5

# Expand/collapse
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> expand
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> collapse
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> is-expanded

# Toggle
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> toggle
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> toggle --target-state on
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> get-toggle-state

# Selection
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> select
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> is-selected

# Value
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> get-value
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> set-value 50

# Combobox
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> combo-select 0
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> combo-select 0 --index
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> combo-items
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> combo-selected-text
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> combo-selected-index

# List
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> list-items
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> list-select 0
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> list-selected-items

# Tab
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> tab-select 0
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> tab-selected
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> tab-count

# Slider
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> slider-value
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> slider-set 50.0
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> slider-min
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> slider-max

# WindowPattern
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> window-close
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> window-minimize
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> window-maximize
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> window-restore
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> window-state

# Transform
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> transform-move --absolute-x 100 --absolute-y 200
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> transform-resize 100 200
python scripts\winguictl.py uia-control --window-id <window_id> --element-id <element_id> transform-rotate 45.0
```

---

## Wait Tests

| Feature | Command | ☑ |
|---------|---------|---|
| Sleep | `wait sleep 500` | ☑ |
| Wait for window | `wait window "Notepad" --timeout 5` | ☑ |
| Wait for window (exact) | `wait window "计算器" --exact --timeout 10` | ☑ |
| Wait for window disappear | `wait window "计算器" --disappear --timeout 10` | ☑ |
| Wait for text | `wait --window-id <id> text "Hello" --timeout 10` | ☑ |
| Wait for UIA element | `wait --window-id <id> uia --automation-id num1Button --timeout 10` | ☑ |
| Wait for OCR text | `wait --window-id <id> ocr "Text" --timeout 10` | ☑ |
| Wait for image | `wait --window-id <id> image --image-path template.png --timeout 10` | ☑ |

```powershell
python scripts\winguictl.py wait sleep 500
python scripts\winguictl.py wait window "Notepad" --timeout 5
python scripts\winguictl.py wait window "计算器" --exact --timeout 10
python scripts\winguictl.py wait window "计算器" --disappear --timeout 10
python scripts\winguictl.py wait --window-id <window_id> text "Hello" --timeout 10
python scripts\winguictl.py wait --window-id <window_id> text "Hello" --exact --timeout 10
python scripts\winguictl.py wait --window-id <window_id> uia --automation-id num1Button --timeout 10
python scripts\winguictl.py wait --window-id <window_id> uia --text "One" --control-type Button --timeout 10
python scripts\winguictl.py wait --window-id <window_id> ocr "Text" --timeout 10
python scripts\winguictl.py wait --window-id <window_id> image --image-path template.png --timeout 10
```

---

## Clipboard Tests

| Feature | Command | ☑ |
|---------|---------|---|
| Copy text | `clipboard copy-text "Hello"` | ☑ |
| Copy files | `clipboard copy-files a.txt b.txt` | ☑ |
| Get text | `clipboard get-text` | ☑ |

```powershell
python scripts\winguictl.py clipboard copy-text "Hello World"
python scripts\winguictl.py clipboard copy-files C:\path\to\file1.txt C:\path\to\file2.txt
python scripts\winguictl.py clipboard get-text
```

---

## Complete Test Examples

### Notepad Complete Test

```powershell
# 1. Focus and type text
python scripts\winguictl.py window --window-id 1119842 focus
python scripts\winguictl.py action --window-id 1119842 clear-text
python scripts\winguictl.py action --window-id 1119842 type --text "Hello from winguictl test!`nLine 2: 12345"

# 2. Control operations (get/set text via hwnd)
python scripts\winguictl.py snapshot --window-id 1119842 hwnd
python scripts\winguictl.py control --hwnd <edit_hwnd> get-text
python scripts\winguictl.py control --hwnd <edit_hwnd> set-text "Replaced by control set-text!"

# 3. UIA operations
python scripts\winguictl.py find --window-id 1119842 uia --control-type Edit
python scripts\winguictl.py find --window-id 1119842 text "Replaced"
python scripts\winguictl.py find --window-id 1119842 ocr "Replaced"

# 4. Screenshot
python scripts\winguictl.py screenshot --window-id 1119842 --output notepad_test.png

# 5. Close
python scripts\winguictl.py window --window-id 1119842 close
```

### Calculator UIA Test

```powershell
# 1. Get UIA snapshot
python scripts\winguictl.py snapshot --window-id 14294402 uia --skip-actions

# 2. Test calculation: 1 + 2 = 3
python scripts\winguictl.py uia-control --window-id 14294402 --element-id num1Button invoke
python scripts\winguictl.py uia-control --window-id 14294402 --element-id plusButton invoke
python scripts\winguictl.py uia-control --window-id 14294402 --element-id num2Button invoke
python scripts\winguictl.py uia-control --window-id 14294402 --element-id equalButton invoke

# 3. Verify result
python scripts\winguictl.py uia-control --window-id 14294402 --element-id CalculatorResults get-text
# Output: "显示为 3"

# 4. Screenshot
python scripts\winguictl.py screenshot --window-id 14294402 --output calculator_result.png

# 5. Close
python scripts\winguictl.py window --window-id 14294402 close
```

---

## Known Issues and Notes

### Element ID Resolution

- **automation_id** is preferred for stable element identification
- **runtime_id** is more reliable but changes between sessions
- If `automation_id` lookup fails, try using `runtime_id` from snapshot output

### ComboBox Operations

- `combo-items` automatically expands the ComboBox to retrieve items
- For custom ComboBox controls (like file type selector in Save dialog), items may not be directly accessible
- Standard Win32 ComboBox controls work best with `combo-items` and `combo-selected-index`

### Window Close

- `window close` may fail if the application shows a confirmation dialog
- Use `action hotkey --keys "{ALT}" "{F4}"` as an alternative
- For force close, use PowerShell: `Stop-Process -Name Notepad -Force`

### Notepad Save Dialog

The Save dialog contains multiple ComboBox types:
- **File name ComboBox**: Custom control (`AppControlHost`), limited functionality
- **File type ComboBox**: Custom control (`AppControlHost`), limited functionality
- **Encoding ComboBox**: Standard Win32 ComboBox, full functionality

### UWP Applications (Calculator, Settings)

- UWP apps use `ApplicationFrameHost.exe` as the process, not the app's own process
- UIA snapshots on UWP apps may be slow; use `--skip-actions` for better performance
- Window close works but may trigger a confirmation prompt
