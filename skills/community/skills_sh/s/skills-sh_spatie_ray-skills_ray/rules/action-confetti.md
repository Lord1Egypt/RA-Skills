---
name: action-confetti
description: Confetti action payload for Ray
metadata:
  tags: action, confetti, celebrate
---

## Confetti Action

Triggers a confetti animation in the Ray application. Use this to celebrate completed tasks, successful operations, or any moment worth celebrating.

### When to Use

- After completing a complex task successfully
- When a long-running operation finishes
- To celebrate milestones or achievements
- When the user explicitly requests celebration

### Payload Structure

```json
{
  "type": "confetti",
  "content": [],
  "origin": {...}
}
```

**Key points:**

- Type is `confetti`
- Content is always an empty array `[]`
- No additional parameters required

### curl Example

```bash
curl -X POST http://localhost:23517/ \
  -H "Content-Type: application/json" \
  -d '{"uuid":"'$(uuidgen)'","payloads":[{"type":"confetti","content":[],"origin":{"function_name":"code-agent","file":"code-agent","line_number":1,"hostname":"'$(hostname)'"}}],"meta":{}}'
```
