# Wait Commands

Wait for conditions to be met before continuing.

## Commands

| Subcommand | Description | Parameters | Example |
|------------|-------------|------------|---------|
| `sleep` | Wait for duration | `duration_ms` (positional) | `wait sleep 2000` |
| `window` | Wait for window | `title` (positional), `--exact`, `--class`, `--timeout`, `--interval`, `--disappear` | `wait window "记事本" --exact` |
| `text` | Wait for text | `--window-id`, `text` (positional), `--exact`, `--timeout`, `--interval`, `--disappear` | `wait --window-id 12345 text "确定"` |
| `uia` | Wait for UIA element | `--window-id`, `--text`, `--control-type`, `--class`, `--automation-id`, `--exact`, `--timeout`, `--interval`, `--disappear` | `wait --window-id 12345 uia --text "确定" --control-type Button` |
| `ocr` | Wait for OCR text | `--window-id`, `text` (positional), `--exact`, `--confidence-threshold`, `--timeout`, `--interval`, `--disappear` | `wait --window-id 12345 ocr "[3条]"` |
| `image` | Wait for image | `--window-id`, `--image-path`, `--threshold`, `--timeout`, `--interval`, `--disappear` | `wait --window-id 12345 image --image-path button.png` |

## Common Parameters

All wait commands (except `sleep`) support:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `--timeout` | 30.0 | Timeout in seconds |
| `--interval` | 500 | Poll interval in milliseconds |
| `--disappear` | false | Wait for element to disappear instead of appear |

**Note**: `--window-id` can be specified anywhere in the command line.

## Usage

### Wait for Window

```powershell
# Wait for window to appear
wait window "记事本" --exact

# Wait for window with class filter
wait window "对话框" --class "#32770"

# Wait for window to disappear
wait window "加载中" --disappear --timeout 10
```

### Wait for Text/UIA/OCR/Image

```powershell
# Wait for text
wait --window-id <id> text "确定" --exact

# Wait for UIA element
wait --window-id <id> uia --text "提交" --control-type Button

# Wait for OCR text
wait --window-id <id> ocr "[新消息]" --timeout 60

# Wait for image
wait --window-id <id> image --image-path button.png --threshold 0.95
```

## Output Format

### Success (element appeared)

Returns matched elements with boundary markers:
```
--- WINGUICTL_CONTENT nonce=<nonce> ---
- "确定" [control_type="Button" class="Button" automation_id="okButton" relative_rect=(100,200 80x30)]
--- END_WINGUICTL_CONTENT nonce=<nonce> ---
```

### Success (element disappeared)

Returns JSON:
```json
{
  "ok": true,
  "code": "OK",
  "message": "window_disappear executed",
  "data": {
    "title": "加载中",
    "elapsed_ms": 3000
  }
}
```

### Timeout

Returns JSON with error:
```json
{
  "ok": false,
  "code": "FAILED",
  "message": "window_timeout failed",
  "data": {
    "title": "记事本",
    "timeout_sec": 30,
    "disappear": false,
    "error": "timeout waiting for window to appear"
  }
}
```

## Use Cases

### Wait for Dialog

```powershell
# After clicking button, wait for dialog
uia-control --window-id <id> --element-id "openButton" click
wait window "打开" --class "#32770" --timeout 5
```

### Wait for Loading

```powershell
# Wait for loading indicator to disappear
wait --window-id <id> ocr "加载中" --disappear --timeout 30
```

### Wait for Message

```powershell
# Wait for new message badge
wait --window-id <wx_id> ocr "[新消息]" --timeout 60
```

## Error Codes

| Code | Description |
|------|-------------|
| `OK` | Success (condition met) |
| `FAILED` | Timeout or error |
