---
name: "openclaw-context-maintainer"
description: "Compress OpenClaw session context safely with backups and restore steps."
license: "MIT-0"
---

# OpenClaw Context Maintainer

Use this skill when an OpenClaw session is getting too large, noisy, or slow and you need to reduce token burn without losing the active thread.

## Workflow

1. Check whether compression is actually needed.
2. Back up the current session or source material first.
3. Preserve the newest context and the active task.
4. Summarize only stale context into a compact block.
5. Verify that names, numbers, decisions, blockers, and open tasks survived.
6. Restore from backup if the result is weak.

## Rules

- Never compress blindly.
- Keep recent context visible.
- Do nothing if the session is already lean.
- Treat compression as hygiene, not memory replacement.
- Promote durable lessons to `MEMORY.md`, `AGENTS.md`, or `TOOLS.md` when needed.

## Best fit

- Long troubleshooting threads
- Repeated back-and-forth
- Obsolete status chatter
- Old tool noise
- Sessions approaching practical context limits

## Avoid

- Blind truncation
- Compressing active reasoning in flight
- Using compression instead of actual memory capture
- Removing recent user decisions or open tasks

## Verification

- Session still reads naturally
- Active task remains clear
- Backup exists
- Restore path exists
