# Find Commands

Find elements in a window by text, UIA, OCR, or image.

## Commands

| Subcommand | Description | Key Parameters | Output Fields |
|------------|-------------|----------------|---------------|
| `text` | Find visible text | `text`, `--exact` | `text`, `control_type`, `class`, `confidence`, `relative_rect` |
| `uia` | Find UIA controls | `--text`, `--control-type`, `--class`, `--automation-id`, `--action`, `--exact` | `control_type`, `class`, `automation_id`, `runtime_id`, `supported_actions`, `relative_rect` |
| `ocr` | Find OCR text | `text`, `--exact`, `--confidence-threshold` | `text`, `confidence`, `relative_rect` |
| `image` | Find image template | `--image-path`, `--threshold`, `--overlap-threshold` | `confidence`, `relative_rect` |

## Usage

```powershell
# Find text (fuzzy match)
find --window-id <id> text "Submit"

# Find UIA controls
find --window-id <id> uia --text "OK" --control-type Button
find --window-id <id> uia --automation-id "SubmitButton"
find --window-id <id> uia --action set-text

# Find OCR text
find --window-id <id> ocr "Confirm" --confidence-threshold 0.7

# Find image
find --window-id <id> image --image-path button.png --threshold 0.95
```

## Output Format

All find commands return content with boundary markers:
```
--- WINGUICTL_CONTENT nonce=<nonce> ---
- "Submit" [control_type="Button" class="Button" confidence=0.95 relative_rect=(150,200 80x30)]
--- END_WINGUICTL_CONTENT nonce=<nonce> ---
```

**Key Fields**:
- `relative_rect`: Window-relative coordinates (can use directly with `action click`)
- `confidence`: Match confidence (0-1) for OCR/image
- `runtime_id`: UIA element ID for `uia-control` commands

## UIA Find Options

### Filters

| Parameter | Description | Match Type |
|-----------|-------------|------------|
| `--text` | Element text/name | Fuzzy (default) or exact |
| `--control-type` | UIA control type | Fuzzy (case-insensitive) |
| `--class` | Window class name | Fuzzy or exact |
| `--automation-id` | Automation ID | Fuzzy or exact |
| `--action` | Supported UIA action | Exact match |
| `--exact` | Enable exact matching | For `--text`, `--class`, `--automation-id` |

### Performance Options

For **Qt applications**, use these flags to improve performance:

| Flag | Effect | Note |
|------|--------|------|
| `--skip-actions` | Skip collecting supported actions | `--action` filter is ignored |
| `--skip-state` | Skip collecting element state | State info unavailable |

### Control Types

Common UIA control types (case-insensitive fuzzy match):

| Type | Description |
|------|-------------|
| `Button` | Button |
| `CheckBox` | Checkbox |
| `ComboBox` | Combo box |
| `Edit` | Text input (also matches `Document` in WinUI3) |
| `List` | List |
| `ListItem` | List item |
| `Menu` | Menu |
| `MenuItem` | Menu item |
| `Tab` | Tab control |
| `TabItem` | Tab item |
| `Text` | Static text |
| `Tree` | Tree view |
| `TreeItem` | Tree item |
| `Window` | Window |

## Image Find Options

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--image-path` | (required) | Template image file path |
| `--threshold` | 0.9 | Match confidence threshold (0-1) |
| `--overlap-threshold` | 0.5 | IoU threshold for deduplication (0-1) |

### Overlap Threshold

- **Lower values** (e.g., 0.3): More aggressive deduplication, fewer results
- **Higher values** (e.g., 0.7): Less aggressive deduplication, more overlapping matches
- **Value of 0**: No deduplication, all matches returned
- **Value of 1**: Maximum deduplication, only non-overlapping matches

## OCR Warning

OCR captures all visible text, which may include sensitive information. Close sensitive windows before running OCR commands.

## Dependencies

- `text`/`uia`: `pywinauto`
- `ocr`: `wx-ocr` (optional)
- `image`: `opencv-python` (optional)
