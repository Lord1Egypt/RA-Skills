# Simple Todo Manager — Setup Guide

## What This Does
A lightweight todo list skill for OpenClaw that lets you add, list, complete, and remove tasks right from your chat. No databases, no complex setup — just a simple markdown file that your agent manages.

Perfect for quick task capture, daily planning, or keeping track of small projects without leaving your OpenClaw workflow.

## Requirements
- OpenClaw instance (any model: Opus, Sonnet, Haiku, etc.)
- Write access to your workspace directory
- That's it. No API keys, no external services.

## Installation

1. **Copy the skill file** to your OpenClaw skills directory:
```bash
mkdir -p ~/clawd/skills/simple-todo
cp SKILL.md ~/clawd/skills/simple-todo/SKILL.md
```

2. **Add to your agent config** (usually in AGENTS.md or your main config):
```markdown
## Skills
- [simple-todo](./skills/simple-todo/SKILL.md)
```

3. **Restart or reload** your OpenClaw instance.

## Test It
Try these commands to verify it's working:

**Add a task:**
> "Add 'buy groceries' to my todo list"

Expected: Task gets added with medium priority and today's date.

**List tasks:**
> "Show me my todos"

Expected: You see your tasks grouped by status, sorted by priority.

**Complete a task:**
> "Mark 'buy groceries' as done"

Expected: Task gets checked off with completion timestamp.

## Configuration Options

| Option | Default | Description |
|--------|---------|-------------|
| `todo_file` | `./todo.md` | Where the todo list is stored (relative to workspace root) |
| `default_priority` | `medium` | Priority for new tasks: low, medium, or high |
| `auto_archive_days` | `7` | Auto-remove completed tasks after N days (0 = never) |

To change settings, edit the Configuration section at the top of SKILL.md.

## FAQ

**Q: Where is my todo data stored?**
A: In a plain markdown file at the path you configure. Default is `./todo.md` in your workspace.

**Q: Can I use this with multiple agents?**
A: Yes, as long as they all point to the same todo file path.

**Q: Does it support due dates?**
A: Not yet. This is intentionally simple. For complex project management, you'll want a more full-featured skill.

**Q: Can I sync this across devices?**
A: If your todo file is in a synced directory (Dropbox, iCloud, git repo), yes.

## Known Limitations
- No due dates or reminders
- No subtasks
- No categories/tags (yet)
- Single file per workspace

---
*Built as a minimal test skill for ClawHub publishing validation.*
