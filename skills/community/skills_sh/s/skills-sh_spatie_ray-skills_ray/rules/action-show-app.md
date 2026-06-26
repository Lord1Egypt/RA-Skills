---
name: action-show-app
description: Show app action payload for Ray
metadata:
  tags: action, show, window
---

## Show App Action

Shows the Ray application window and brings it to the foreground. Use this when you want to make Ray visible to the user.

### When to Use

- When the user asks to show or open Ray
- Before sending important logs that the user should see immediately
- To bring Ray to the user's attention

### Payload Structure

```json
{
  "type": "show_app",
  "content": [],
  "origin": {...}
}
```

**Key points:**

- Type is `show_app`
- Content is always an empty array `[]`
- No additional parameters required

### curl Example

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"show_app","content":[],"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```
