---
name: self-improving-meta
description: "Optional OpenClaw session-start reminder to log infrastructure issues. Log-only. Does not edit files."
metadata: {"openclaw":{"emoji":"🔧","events":["agent:bootstrap"]}}
---

# Meta Self-Improvement Hook

Optional OpenClaw reminder. Default skill behavior is still log-only. Enable this hook only if you want a session-start reminder in main sessions.

This OpenClaw hook is **not matcher-gated**. Unlike Claude Code / Codex hooks (explicit meta signals), `agent:bootstrap` runs at session start for the main agent. That is why it is opt-in and must stay workspace-local.

## What It Does

- Fires on `agent:bootstrap` (before workspace files are injected)
- Injects a **log-only** reminder to consider `.learnings/` entries
- Skips subagent sessions
- Does not modify files, extract skills, send messages, or call the network

## Reminder Content

Log only. Do not rewrite `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `MEMORY.md`, hooks, or skills from this reminder.

| Trigger | Target File | Category |
|---------|-------------|----------|
| Agent misinterprets prompt file instruction | `LEARNINGS.md` | `instruction_ambiguity` |
| Hook fails or produces no output | `META_ISSUES.md` | hook_failure |
| Skill doesn't activate when expected | `META_ISSUES.md` | skill_gap |
| Two rules contradict each other | `LEARNINGS.md` | `rule_conflict` |
| Context window feels cramped/truncated | `LEARNINGS.md` | `context_bloat` |
| Memory entry is stale or wrong | `LEARNINGS.md` | `prompt_drift` |
| Missing skill capability | `FEATURE_REQUESTS.md` | feature request |

## Configuration

Keep the hook in **this workspace**. Do not install into `~/.openclaw/hooks/`.

```bash
mkdir -p .openclaw/hooks
cp -r hooks/openclaw .openclaw/hooks/self-improving-meta
```
