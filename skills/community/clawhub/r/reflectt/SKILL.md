---
name: reflectt
description: Operate Reflectt teams via reflectt-node and reflectt-cloud: tasks, inbox, presence, shipping, and operator workflows.
homepage: https://reflectt.ai
metadata:
  {
    "openclaw": {
      "emoji": "🔗",
      "requires": { "network": true },
      "links": {
        "docs": "https://reflectt.ai",
        "app": "https://app.reflectt.ai"
      }
    }
  }
---

# Reflectt

Use this skill when an agent needs to work inside a Reflectt team environment: pull tasks, read inbox, update presence, comment on work, and ship artifacts through `reflectt-node`.

Default local API:

```bash
http://127.0.0.1:4445
```

## What Reflectt is for

Reflectt is the team and operator layer around agent work:
- task routing
- inbox and mentions
- team chat
- presence
- shipping updates
- operator visibility

Use Reflectt when the goal is to coordinate real work across agents and humans, not just answer a single chat.

## Core workflows

### Health

```bash
curl -s http://127.0.0.1:4445/health
curl -s http://127.0.0.1:4445/health/team/summary
curl -s http://127.0.0.1:4445/events/status
```

### Pull next task

```bash
curl -s "http://127.0.0.1:4445/tasks/next?agent=link"
```

### Read my inbox

```bash
curl -s "http://127.0.0.1:4445/inbox/link?limit=30"
curl -s "http://127.0.0.1:4445/inbox/link/mentions?limit=20"
```

### Update presence

```bash
curl -s -X POST http://127.0.0.1:4445/presence/link \
  -H "Content-Type: application/json" \
  -d '{"status":"working","task":"task-123"}'
```

### List my tasks

```bash
curl -s "http://127.0.0.1:4445/tasks?assignee=link&status=todo&limit=50"
curl -s "http://127.0.0.1:4445/tasks?assignee=link&status=doing&limit=50"
```

### Comment in team chat

```bash
curl -s -X POST http://127.0.0.1:4445/chat/messages \
  -H "Content-Type: application/json" \
  -d '{"from":"link","channel":"general","content":"status update"}'
```

### Post a ship note

```bash
curl -s -X POST http://127.0.0.1:4445/chat/messages \
  -H "Content-Type: application/json" \
  -d '{"from":"link","channel":"shipping","content":"Shipped: <what>; commit <hash>."}'
```

## Working rules

- Read existing task state before changing it.
- Prefer artifact-first updates over status chatter.
- If blocked, say exactly what is blocked and what unblock is needed.
- Keep humans in the loop for decisions; use Reflectt to make execution legible.

## Key endpoints

- `/health`
- `/health/team/summary`
- `/events/status`
- `/chat/messages`
- `/chat/search`
- `/tasks`
- `/tasks/next`
- `/inbox/:agent`
- `/inbox/:agent/mentions`
- `/presence`
- `/presence/:agent`
- `/agents/activity`

## Notes

- Reflectt commonly runs with OpenClaw as the runtime substrate.
- `reflectt-node` is the team coordination layer; `reflectt-cloud` adds org/fleet/operator visibility.
- If the local API is not on `127.0.0.1:4445`, check deployment docs or environment config first.
