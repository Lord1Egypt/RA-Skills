# Clipboard Commands

Clipboard operations for copying files/text and getting text.

## Commands

| Subcommand | Description | Parameters | Example |
|------------|-------------|------------|---------|
| `copy-files` | Copy files to clipboard | `files` (positional, one or more) | `clipboard copy-files "C:\file1.txt" "C:\file2.txt"` |
| `copy-text` | Copy text to clipboard | `text` (positional) | `clipboard copy-text "Hello, World!"` |
| `get-text` | Get text from clipboard | None | `clipboard get-text` |

## Usage

### Copy Files

```powershell
# Copy single file
clipboard copy-files "C:\Documents\report.pdf"

# Copy multiple files
clipboard copy-files "C:\file1.txt" "C:\file2.txt" "D:\images\photo.png"
```

### Copy Text

```powershell
# Copy simple text
clipboard copy-text "Hello, World!"

# Copy text with spaces (use quotes)
clipboard copy-text "This is a longer text string"
```

### Get Text

```powershell
# Get text from clipboard
clipboard get-text
```

## Output Format

### copy-files

```json
{
  "ok": true,
  "code": "OK",
  "message": "copy_files executed",
  "data": {
    "files": ["C:\\file1.txt", "C:\\file2.txt"],
    "count": 2
  }
}
```

### copy-text

```json
{
  "ok": true,
  "code": "OK",
  "message": "copy_text executed",
  "data": {
    "text": "Hello, World!",
    "length": 13
  }
}
```

### get-text

Returns content with boundary markers:
```
--- WINGUICTL_CONTENT nonce=<nonce> ---
<clipboard text content>
--- END_WINGUICTL_CONTENT nonce=<nonce> ---
```

### Error (no text in clipboard)

```json
{
  "ok": false,
  "code": "FAILED",
  "message": "get_text failed",
  "data": {
    "error": "no text in clipboard"
  }
}
```

## Use Case: Prepare Files for Upload

```powershell
# Step 1: Copy files to clipboard
clipboard copy-files "C:\Documents\report.pdf"

# Step 2: Focus target application window
window --window-id 12345 focus

# Step 3: Paste (Ctrl+V)
action --window-id 12345 hotkey --keys "{CTRL}" "v"
```

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `failed to copy files to clipboard` | Clipboard access denied or invalid paths | Ensure paths exist and application has clipboard access |
| `failed to copy text to clipboard` | Clipboard access denied | Close other applications using clipboard |
| `no text in clipboard` | Clipboard empty or contains non-text data | Copy text to clipboard first |
