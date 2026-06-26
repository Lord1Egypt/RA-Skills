---
name: superpowers-open-using-superpowers-open
description: >
  Use when starting any conversation with OpenClaw. Establishes how to find and use SuperpowersOpen skills. Requires checking for applicable skills before any response, including clarifying questions.
metadata:
  openclaw:
    always: true
    emoji: "⚡"
    homepage: https://github.com/superpowers-open/superpowers-open
---

# Using SuperpowersOpen

## Instruction Priority

SuperpowersOpen skills override default system prompt behavior, but **user instructions always take precedence**:

1. **User's explicit instructions** (CLAUDE.md, GEMINI.md, AGENTS.md, direct requests) — highest priority
2. **SuperpowersOpen skills** — override default system behavior where they conflict
3. **Default system prompt** — lowest priority

If CLAUDE.md says "don't use TDD" and a skill says "always use TDD," follow the user's instructions. The user is in control.

## How SuperpowersOpen Skills Work

SuperpowersOpen skills are installed under `~/.openclaw/skills/superpowers-open/`. OpenClaw discovers them automatically via their `description` frontmatter field. Each skill's description specifies triggering conditions — when OpenClaw encounters a matching situation, the skill loads and guides behavior.

You do NOT need to manually invoke skills. Check each skill's description to determine if it applies to the current task.

## Tool Mapping

SuperpowersOpen skills are adapted from the Claude Code superpowers ecosystem. This table maps original tool references to OpenClaw equivalents:

| Superpowers (Claude Code) | OpenClaw equivalent |
|---|---|
| `Skill` tool | Skills auto-load via description matching |
| `Task` tool (dispatch subagent) | **Not available.** Guide the user to open a new session and manually perform the task. |
| `TodoWrite` / task tracking | Native task/list tools or checkbox (`- [ ]`) syntax |
| `Read`, `Write`, `Edit` | OpenClaw native file tools |
| `Bash` | OpenClaw native shell tools |
| `EnterPlanMode` / `ExitPlanMode` | **Not available.** Skills that reference these have been adapted to remove them. |

## Unavailable Skills

Two superpowers skills require subagent support and are NOT included in SuperpowersOpen:
- `subagent-driven-development` — requires dispatching subagents per task
- `dispatching-parallel-agents` — requires parallel subagent dispatch

When a workflow would normally use these, use `superpowers-open:executing-plans` (inline execution) instead.

## Cross-Skill References

When one SuperpowersOpen skill references another, it uses the format:

```
**REQUIRED:** Use superpowers-open:brainstorming
```

When you see this, look for the matching skill in `~/.openclaw/skills/superpowers-open/` and follow its guidance.

## Skill Types

**Rigid** (TDD, debugging, verification): Follow exactly. Don't adapt away discipline.

**Flexible** (patterns): Adapt principles to context.

The skill itself tells you which.

## User Instructions

Instructions say WHAT, not HOW. "Add X" or "Fix Y" doesn't mean skip workflows.
