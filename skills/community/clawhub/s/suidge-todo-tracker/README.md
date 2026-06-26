# Todo Tracker

A self-managed todo list for AI Agents. The Agent can proactively track follow-up items and remind users at appropriate times via heartbeat checks.

## Features

- **Self-managed** — Agent manages the todo list autonomously
- **Heartbeat-driven** — Checks via heartbeat every 30 minutes
- **Time-aware** — Triggers reminders at specified times
- **Auto-cleanup** — Removes completed items after 24 hours
- **Persistent** — All items stored in JSON file

## Installation

1. Copy `templates/todo.json` to `memory/todo.json`
2. Update `HEARTBEAT.md` with todo check step
3. Update `AGENTS.md` with trigger keywords

See `setup.md` for detailed instructions.

## Usage

```
User: 提醒我明天上午跟进那个插件更新问题
Agent: 好的，已添加到待跟进清单。明天上午我会提醒你。

[Next morning, heartbeat triggers]

Agent: 主人，你之前让我提醒你跟进插件更新问题，现在要处理吗？
```

## Files

| File | Purpose |
|------|---------|
| `SKILL.md` | Core skill instructions |
| `setup.md` | Installation guide |
| `data-structure.md` | JSON schema |
| `examples.md` | Usage examples |
| `templates/todo.json` | Template file |

## License

MIT
