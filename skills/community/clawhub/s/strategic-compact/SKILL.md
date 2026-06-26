---
name: strategic-compact
description: "Manual context compaction at logical workflow boundaries rather than arbitrary auto-compaction. Use after completing exploration phases, before switching major tasks, or when context approaches limits. Preserves context through task phases. Trigger phrases: context limit, compact, memory pressure, save context, phase transition. Adapted from everything-claude-code by @affaan-m (MIT)"
metadata: {"clawdbot":{"emoji":"📦","requires":{"bins":[],"env":[]},"os":["darwin","linux","win32"]}}
---

# Strategic Compact Skill

Manual `/compact` at logical workflow boundaries, not arbitrary auto-compaction points.

## When to Activate

- Running long sessions approaching context limits (200K+ tokens)
- Multi-phase tasks (research → plan → implement → test)
- Switching between unrelated tasks within the same session
- After completing a major milestone before starting new work

## Quick Start

1. Identify logical phase boundaries in your work
2. Save important findings to files before compacting
3. Use `/compact` with a context message (e.g., "/compact Now implementing auth")
4. Continue work referencing saved files, not conversation history

## Key Concepts

- **Auto-compaction problem** — Triggers at arbitrary points, often mid-task
- **Strategic compaction** — Compact after exploration/planning, before execution
- **Persistence** — Project instructions, git state, and files on disk survive; conversation history and intermediate reasoning don't
- **Checkpoint discipline** — Save learnings to files; use git commits to mark progress
- **Token awareness** — 150K → consider; 180K → plan; 200K+ → should have already compacted

## Common Usage

Most frequent patterns:
- Research → build (compact after documentation phase)
- Exploration → execution (compact after CLAUDE.md is written)
- Debug → next feature (compact after fix is committed)
- Failed approach → new strategy (compact to clear dead-end reasoning)

## References

- `references/compaction-guide.md` — Decision table, what survives, patterns, token budgeting, optimization strategies
- `references/tool-integration.md` — Script documentation, configuration, integration methods
- **Compaction command** — `/compact [optional message]`
- **Status check** — Check session context size before major operations
- **Memory files** — Save to disk (survives compaction)
- **Git commits** — Mark progress (persists across compaction)
