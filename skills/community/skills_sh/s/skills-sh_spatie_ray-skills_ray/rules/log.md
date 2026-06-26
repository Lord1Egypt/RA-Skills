---
name: log
description: How to send a log to Ray
metadata:
  tags: log, payload
---

## Log Payload

The log payload is used for general value logging. It displays one or more values in Ray.

### When to Use

Use the log payload when you want to:

- Display simple values or messages
- Log multiple values at once
- Show debugging information

### Payload Structure

```json
{
  "type": "log",
  "content": {
    "values": ["value1", "value2", "..."],
    "meta": []
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

- `values`: Array of values to display. Each value will be shown as a separate item.
- `meta`: Array of metadata objects. Can include `{"clipboard_data": "text"}` to set clipboard content.

### Examples

#### Simple message

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"log","content":{"values":["Hello from Claude"],"meta":[]},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"my-computer"}}],"meta":{}}'
```

#### Multiple values

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"log","content":{"values":["Status: OK","Count: 42","Ready: true"],"meta":[]},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"my-computer"}}],"meta":{}}'
```

#### With clipboard data

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"log","content":{"values":["Click to copy this text"],"meta":[{"clipboard_data":"This text will be copied to clipboard"}]},"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"my-computer"}}],"meta":{}}'
```
