# Recommended Hook: Context Capture on Commit

Automatically remind Claude to capture learnings after every git commit. This pairs with Mode 1 (Session Capture) — the hook triggers the prompt, the skill handles the capture.

## Setup

Create this file at `~/.claude/hookify.context-capture-reminder.local.md` for global coverage, or `project/.claude/hookify.context-capture-reminder.local.md` for a single project:

```markdown
---
name: context-capture-reminder
enabled: true
event: bash
pattern: git\s+commit
action: warn
---

Context check: Were any patterns, gotchas, or commands discovered during this work that should be captured to CLAUDE.md or .claude/rules/? If yes, update them now before moving on. If nothing new was learned, carry on.
```

## How It Works

1. You finish work and commit
2. The hook fires after the `git commit` Bash call
3. Claude pauses to consider whether anything learned during this work should be persisted
4. If yes, Claude updates CLAUDE.md or creates/updates a `.claude/rules/` file
5. If nothing new, Claude continues

## Why Commit Time?

- Context is fresh — you just finished the work
- You're creating a permanent record anyway
- Natural checkpoint before moving to the next task
- Pairs with `git log` for tracing when a pattern was discovered

## Requires

This hook uses the [hookify](https://github.com/jezweb/claude-skills) plugin for Claude Code. If you don't have hookify, you can add the same reminder as a line in your CLAUDE.md:

```markdown
## Workflow
- Before committing: check if any discoveries should be captured to CLAUDE.md or .claude/rules/
```
