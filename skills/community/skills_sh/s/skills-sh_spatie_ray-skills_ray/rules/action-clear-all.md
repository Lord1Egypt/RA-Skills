---
name: action-clear-all
description: Clear all logs action payload for Ray
metadata:
  tags: action, clear, logs
---

## Clear All Action

Clears all logs from the Ray window & archives the current session to disk. Use this to start fresh with a clean log view.

### When to Use

- When the user asks to clear or reset Ray logs
- Before starting a new debugging session
- To remove clutter from previous operations

### Payload Structure

```json
{
  "type": "clear_all",
  "content": [],
  "origin": {...}
}
```

**Key points:**

- Type is `clear_all`
- Content is always an empty array `[]`
- No additional parameters required

### curl Example

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"clear_all","content":[],"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```
