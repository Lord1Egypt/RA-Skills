---
name: mindkeeper
description: Time Machine for Your AI's Brain — version control for agent context files. Use when the user asks about changes in SOUL.md, AGENTS.md, MEMORY.md, or other agent context files; when they want to undo, rollback, or compare versions; or when they need a checkpoint before risky edits.
version: 1.2.4
homepage: https://github.com/seekcontext/mindkeeper
repository: https://github.com/seekcontext/mindkeeper
---

# Mindkeeper — Time Machine for Your AI's Brain

Use mindkeeper tools when the user asks about changes, history, or versions of their agent context files (`AGENTS.md`, `SOUL.md`, `USER.md`, `IDENTITY.md`, `TOOLS.md`, `HEARTBEAT.md`, `MEMORY.md`, `memory/`, `skills/`).

## Bootstrap (One-time setup)

**When the user enables mindkeeper or asks for mindkeeper capability**, first try `mind_status`. If it fails (tool not found or similar):

1. **Ask for confirmation** — Tell the user: "Mindkeeper needs the mindkeeper-openclaw plugin to work. I'll need to run `openclaw plugins install mindkeeper-openclaw` and restart the Gateway. May I proceed?" **Do not install or restart until the user explicitly confirms.**

2. **After user confirms** — Run this flow:
   - **Install the plugin** — Run via bash:
     ```bash
     openclaw plugins install mindkeeper-openclaw
     ```
   - **Restart Gateway if the runtime supports it** — Use the available runtime mechanism to restart Gateway. If restart is unavailable or fails, tell the user: "Plugin installed. Restart your Gateway manually to apply."
   - **Confirm** — If restart succeeded, tell the user: "Mindkeeper is ready. Restart complete — you can now ask about history, diffs, rollbacks, or snapshots." If restart did not happen, tell the user that the plugin is installed but Gateway must be restarted before the tools will appear.

3. **Alternative** — If the user prefers to install manually, tell them: "Run `openclaw plugins install mindkeeper-openclaw` in your terminal, then restart your Gateway. After that, mindkeeper will be ready."

If `mind_status` succeeds, the plugin is already installed; skip the bootstrap and proceed with the user's request.

## Tool Preference

In OpenClaw Plugin mode, prefer the `mind_*` tools over CLI commands for normal mindkeeper operations.

- Use `mind_status`, `mind_history`, `mind_diff`, `mind_snapshot`, and `mind_rollback` whenever they are available.
- Do not use `openclaw mind ...` or `mindkeeper ...` for routine history, diff, snapshot, or rollback requests if the plugin tools are available.
- CLI commands are for one-time setup, troubleshooting, manual user workflows, or when the user explicitly asks for terminal commands.

## Available Tools

| Tool | Purpose |
|------|---------|
| `mind_status` | Show what files are tracked and whether there are unsaved changes |
| `mind_history` | Browse the change log for one file or all files |
| `mind_diff` | Compare any two versions of a file side-by-side |
| `mind_rollback` | Restore a file to a previous version (always preview first) |
| `mind_snapshot` | Save a named checkpoint before making significant changes |

## Tracking Scope

Mindkeeper tracks these files by default:

- `AGENTS.md`, `SOUL.md`, `USER.md`, `IDENTITY.md`
- `TOOLS.md`, `HEARTBEAT.md`, `MEMORY.md`
- `memory/**/*.md`
- `skills/**/*.md`

Excluded by default: `BOOTSTRAP.md`, `canvas/**`, `.git/`, `.mindkeeper/`.

## When to Use

| User says… | Action |
|-----------|--------|
| "What changed in SOUL.md?" | `mind_history` with `file: "SOUL.md"` |
| "Show me the diff from last week" | `mind_history` to find the commit, then `mind_diff` |
| "Undo that change" / "Roll back AGENTS.md" | Full rollback procedure (see below) |
| "Save a checkpoint before I experiment" | `mind_snapshot` with a descriptive name |
| "Is mindkeeper tracking my files?" | `mind_status` |
| "What does my history look like?" | `mind_history` without a file filter |

## Direct Edit Requests

If the user asks to directly edit a tracked file such as `SOUL.md`, `AGENTS.md`, or `MEMORY.md`, make the edit directly.

- Do not block on CLI availability.
- Do not mention unavailable CLI commands unless the user explicitly asked for a CLI-based workflow.
- Mindkeeper's background watcher should capture the change automatically after the edit.
- If relevant, you may mention that the change should now be tracked by mindkeeper.

## Tool Usage Guide

### mind_status
Call this first when the user asks about history, tracking state, snapshots, or rollback, or if you're unsure whether mindkeeper is initialized.
```
mind_status → { initialized, workDir, pendingChanges, snapshots }
```

You do not need to call `mind_status` before a simple direct edit request unless the user specifically asks about tracking or history.

### mind_history
Returns a list of commits with short hash, date, and message.
- `file` (optional): filter to a specific file path, e.g. `"SOUL.md"`
- `limit` (optional): number of entries to return (default 10, increase for longer searches)

```
mind_history({ file: "SOUL.md", limit: 20 })
→ { count, entries: [{ oid, date, message }] }
```

### mind_diff
Compares two versions of a file. `from` and `to` are short or full commit hashes from `mind_history`.
- Omit `to` to compare `from` against the current version (HEAD).

```
mind_diff({ file: "SOUL.md", from: "a1b2c3d4" })
→ { file, from, to, additions, deletions, unified }
```

### mind_snapshot
Creates a named checkpoint of the current state of all tracked files. Use before risky changes.
- `name`: short identifier, e.g. `"stable-v2"` or `"before-experiment"`
- `message` (optional): longer description

```
mind_snapshot({ name: "stable-v2", message: "Personality tuned, rules finalized" })
→ { success, snapshot, commit: { oid, message } }
```

### mind_rollback
**Always use the two-step procedure.** Never skip the preview.

**Step 1 — Preview:**
```
mind_rollback({ file: "SOUL.md", to: "a1b2c3d4", preview: true })
→ { preview: true, diff: { unified, additions, deletions }, instruction }
```
Show the diff to the user and ask for confirmation.

**Step 2 — Execute (only after user confirms):**
```
mind_rollback({ file: "SOUL.md", to: "a1b2c3d4", preview: false })
→ { preview: false, success: true, commit: { oid, message } }
```
After success, tell the user: **"Run `/new` to apply the changes to your current session."**

## Important Notes

- **This skill is the guide, the plugin is the engine** — the `mindkeeper-openclaw` plugin provides the actual `mind_*` tools and watcher; this skill teaches the AI how to bootstrap and use them safely
- **Use plugin tools first** — in OpenClaw Plugin mode, prefer `mind_*` tools over CLI commands for normal operations
- **Rollback is per-file** — it only restores the specified file, not all files at once
- **Rollbacks are non-destructive** — every rollback creates a new commit, so it can itself be undone
- **Auto-snapshots run in the background** — the user doesn't need to manually save; mindkeeper captures every change automatically
- **LLM commit messages are plugin-only for now** — currently supported only through the OpenClaw plugin; standalone CLI mode falls back to template messages
- **Named snapshots are the safety net** — encourage users to snapshot before major personality or rule changes
- **If history is empty** — mindkeeper may not have initialized yet, or no changes have been made since install. Call `mind_status` to check.
- **Commit hashes** — always use the `oid` field from `mind_history` results. Short 8-character hashes are fine.
- **Keep user-facing messages focused** — if a task can be completed with file edits or `mind_*` tools, do not distract the user with unavailable CLI details
