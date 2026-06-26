---
name: file-contents
description: How to send file contents to Ray
metadata:
  tags: file, contents, payload
---

## File Contents Payload

The file contents payload displays the contents of a file with the filename as the label.

### When to Use

Use the file contents payload when you want to:

- Display the contents of a file
- Show configuration files
- Debug file content

### Payload Structure

```json
{
  "type": "custom",
  "content": {
    "content": "file contents here (HTML-encoded)",
    "label": "filename.txt"
  },
  "origin": {
    "function_name": "code-agent",
    "file": "code-agent",
    "line_number": 1,
    "hostname": "my-computer"
  }
}
```

### Content Fields

- `content`: The file contents, HTML-encoded with newlines converted to `<br />`
- `label`: The filename (basename only, e.g., `config.json` not `/path/to/config.json`)

### Formatting Rules

Before sending, the file contents must be formatted:

1. HTML-encode all entities using `htmlentities()` equivalent
2. Replace newlines with `<br />`

### Error Handling

If the file does not exist:
- `content`: `"File not found: '/path/to/file'"`
- `label`: `"File"`

### Examples

#### Display file contents

```bash
# Read file and send to Ray
FILE_PATH="/path/to/config.json"
FILE_NAME=$(basename "$FILE_PATH")
FILE_CONTENT=$(cat "$FILE_PATH" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g; s/"/\&quot;/g' | sed ':a;N;$!ba;s/\n/<br \/>/g')

curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":"'"$FILE_CONTENT"'","label":"'"$FILE_NAME"'"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### Simple inline example

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":"line 1<br />line 2<br />line 3","label":"example.txt"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### File not found

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":"File not found: '\''/path/to/missing.txt'\''","label":"File"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```
