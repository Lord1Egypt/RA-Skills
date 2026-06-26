---
name: custom
description: How to send custom content to Ray
metadata:
  tags: custom, payload
---

## Custom Payload

The custom payload displays arbitrary content with a custom label. No formatting is applied to the content.

### When to Use

Use the custom payload when you want to:

- Display content with a specific label
- Show data that doesn't fit other payload types
- Create custom-labeled debug output

### Payload Structure

```json
{
  "type": "custom",
  "content": {
    "content": "my custom content",
    "label": "My Label"
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

- `content`: The content to display (passed through as-is, no formatting)
- `label`: Custom label for the payload (can be empty string)

### Examples

#### Simple custom content

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":"my custom content","label":"Custom"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### With descriptive label

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":"Operation completed successfully","label":"Status"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### Empty label

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":"Just the content, no label","label":""},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```

#### Debug marker

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"custom","content":{"content":"Reached checkpoint A","label":"Debug"},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```
