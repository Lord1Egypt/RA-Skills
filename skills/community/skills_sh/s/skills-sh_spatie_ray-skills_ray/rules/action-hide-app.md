---
name: action-hide-app
description: Hide app action payload for Ray
metadata:
  tags: action, hide, window
---

## Hide App Action

Hides the Ray application window. Use this when you want to minimize or hide Ray from view.

### When to Use

- When the user asks to hide or minimize Ray
- After displaying information that doesn't need to stay visible
- To reduce screen clutter

### Payload Structure

```json
{
  "type": "hide_app",
  "content": [],
  "origin": {...}
}
```

**Key points:**

- Type is `hide_app`
- Content is always an empty array `[]`
- No additional parameters required

### curl Example

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"hide_app","content":[],"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```
