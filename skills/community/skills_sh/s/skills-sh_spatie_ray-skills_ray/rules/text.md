---
name: text
description: How to send plain text to Ray
metadata:
  tags: text, payload
---

## Text Payload

The text payload displays plain text with preserved whitespace formatting.

### When to Use

Use the text payload when you want to:

- Display plain text with spaces and newlines preserved
- Show preformatted text content
- Display text that shouldn't be interpreted as HTML

### Payload Structure

```json
{
  "type": "custom",
  "content": {
    "content": "HTML-escaped text with &nbsp; for spaces and <br> for newlines",
    "label": "Text"
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

- `content`: The text content with HTML escaping applied
- `label`: Always `"Text"`

### Formatting Rules

Before sending, the text must be formatted:

1. HTML-escape special characters (`<`, `>`, `&`, `"`, `'`)
2. Replace spaces with `&nbsp;`
3. Replace newlines with `<br>`

### Examples

#### Simple text

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":"Hello&nbsp;World","label":"Text"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### Multi-line text

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":"Line&nbsp;1<br>Line&nbsp;2<br>Line&nbsp;3","label":"Text"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### Text with special characters

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":"if&nbsp;(x&nbsp;&lt;&nbsp;10)&nbsp;{<br>&nbsp;&nbsp;return&nbsp;true;<br>}","label":"Text"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```
