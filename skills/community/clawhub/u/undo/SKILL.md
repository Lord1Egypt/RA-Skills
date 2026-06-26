---
name: undo
description: |
  File edit time machine for AI agents. Automatically snapshot file changes after every Write, Edit, or Shell operation,
  and provide undo/revert capabilities to any previous state. Supports: undo last change, undo N steps, undo to timestamp,
  undo to named checkpoint, list change history, and create checkpoints.
  Use this skill after the user says "track changes", "enable undo", or when they want to safely experiment with file edits.
  Also activates automatically when the user asks to "undo", "revert", "go back", "restore", or "show history" of file changes.
homepage: https://github.com/yourname/undo-skill
user-invocable: true
metadata:
  openclaw:
    emoji: '⏪'
    requires: { bins: ['node'] }
    primaryEnv: ''
---

# Undo.skill — File Edit Time Machine

> **CRITICAL**: After EVERY file modification (Write, Edit, MultiEdit, Shell commands that change files), you MUST run the snapshot script. This is non-negotiable — without snapshots, undo is impossible.

## Base Directory

All scripts are located in this skill's directory. Use `{baseDir}` to reference them:

```bash
SCRIPTS="{baseDir}/scripts"
```

## Quick Reference

| Command | Purpose |
|---------|---------|
| `node "$SCRIPTS/init.js" /path/to/project` | Start tracking a project |
| `node "$SCRIPTS/snapshot.js" /path/to/project "Description"` | Record current state |
| `node "$SCRIPTS/undo.js" /path/to/project --steps 1` | Undo last change |
| `node "$SCRIPTS/undo.js" /path/to/project --to <name>` | Undo to checkpoint |
| `node "$SCRIPTS/undo.js" /path/to/project --timestamp "2026-04-10T14:00"` | Undo to time |
| `node "$SCRIPTS/list.js" /path/to/project` | List change history |
| `node "$SCRIPTS/checkpoint.js" /path/to/project "name"` | Create named checkpoint |
| `node "$SCRIPTS/watcher.js" /path/to/project &` | Start background watcher |

## Output Format

**Every script outputs exactly one line of JSON.** Parse it with your environment's JSON parser — do NOT read the human text.

### init.js

```json
{"action":"init","status":"success","initialized":true,"project":"/abs/path","storagePath":"~/.local/share/...","message":"Tracking initialized"}
```

```json
{"action":"init","status":"success","initialized":false,"project":"/abs/path","storagePath":"~/.local/share/...","message":"Already tracked"}
```

### snapshot.js

```json
{"action":"snapshot","status":"success","committed":true,"project":"/abs/path","description":"Added error handling","hash":"abc1234","changedFiles":["src/index.js"],"fileCount":1}
```

```json
{"action":"snapshot","status":"success","committed":false,"project":"/abs/path","description":"..."}
```
(committed=false means no changes since last snapshot)

### list.js

```json
{
  "action":"list",
  "status":"success",
  "project":"/abs/path",
  "count":3,
  "commits":[
    {
      "hash":"abc1234",
      "date":"2026-04-10 14:05:12 +0800",
      "timestamp":"2026-04-10T06:05:12.000Z",
      "description":"Added error handling",
      "files":[{"status":"M","path":"src/index.js"}],
      "isCheckpoint":false,
      "isInitial":false
    }
  ],
  "checkpoints":[{"name":"checkpoint/before-refactor","hash":"def5678"}]
}
```

### undo.js

```json
{"action":"undo","status":"success","undone":true,"mode":"steps","project":"/abs/path","steps":1,"targetHash":"abc1234","checkpointBranch":"checkpoint/undo-1712736312000"}
```

```json
{"action":"undo","status":"error","error":"not_enough_history","mode":"steps","project":"/abs/path","requested":5}
```

### checkpoint.js

```json
{"action":"checkpoint","status":"success","project":"/abs/path","checkpoint":"before-refactor","branch":"checkpoint/before-refactor"}
```

### watcher.js

On start:
```json
{"action":"watcher-start","status":"success","project":"/abs/path","pid":12345,"debounceMs":5000,"pollMs":2000}
```

On each auto-snapshot:
```json
{"action":"watcher-snapshot","status":"success","committed":true,"project":"/abs/path","hash":"abc1234","description":"[watcher] added: 1, modified: 2","timestamp":"2026-04-10T06:05:12.000Z","files":{"added":["new.js"],"changed":["index.js"],"deleted":[]}}
```

On stop:
```json
{"action":"watcher-stop","status":"stopped","project":"/abs/path"}
```

### Error Codes

| error code | meaning | action |
|---|---|---|
| `missing_project_path` | No path argument given | Pass absolute path |
| `git_not_found` | Git not installed and auto-install failed | Install git manually (see `detail.manual_install_hint`, try `apt-get install git` / `brew install git` / `pkg install git`) |
| `not_tracked` | Project not initialized | Run init.js first |
| `no_changes` | Nothing changed since last snapshot | Safe to skip |
| `not_enough_history` | Not enough snapshots to undo requested depth | Use fewer steps |
| `checkpoint_not_found` | Named checkpoint doesn't exist | Check list.js output |
| `checkpoint_exists` | Checkpoint name already taken | Use a different name |
| `invalid_timestamp` | Timestamp format invalid | Use ISO 8601 |
| `no_commits_before_timestamp` | No snapshots before that time | Use earlier time or different approach |

## First-Time Setup

After installing this skill, run init.js on the user's project before any other commands:

```bash
node "$SCRIPTS/init.js" /path/to/project
```

This attempts to auto-install git if missing, then initializes tracking. If git auto-install fails, it returns a structured error with platform details and install hints — use that info to guide manual installation.

## Core Workflow

### Rule 1: Snapshot After Every File Change

After ANY Write/Edit/Shell that modifies files, immediately run:

```bash
node "$SCRIPTS/snapshot.js" /path/to/project "Brief description of what changed"
```

Description guidelines:
- Specific: "Refactored auth middleware to use JWT" not "changed files"
- Mention key files
- Include intent
- Under 80 chars for the summary

### Rule 2: Checkpoint Before Major Operations

```bash
node "$SCRIPTS/checkpoint.js" /path/to/project "before-refactor"
```

### Rule 3: List History When Asked

```bash
node "$SCRIPTS/list.js" /path/to/project
```

Parse the `commits` array. Each entry has `hash`, `timestamp`, `description`, `files`, and `isCheckpoint` flag.

### Rule 4: Undo on Request

```bash
# Undo last N changes
node "$SCRIPTS/undo.js" /path/to/project --steps 3

# Undo to named checkpoint
node "$SCRIPTS/undo.js" /path/to/project --to before-refactor

# Undo to specific time (ISO 8601)
node "$SCRIPTS/undo.js" /path/to/project --timestamp "2026-04-10T14:00"
```

After successful undo, inform the user that previous state is preserved on the branch from the JSON's `checkpointBranch` field.

### Rule 5: Watcher for Long Sessions

```bash
node "$SCRIPTS/watcher.js" /path/to/project &
```

Auto-snapshots if you forget. PID in startup JSON. Stop with `kill <PID>`.

## How It Works (Architecture)

```
~/.local/share/undo-skill/repos/
├── abc123def456/          # Bare git repo (MD5 hash of project path, 12 chars)
│   ├── HEAD
│   ├── refs/heads/main    # Latest snapshot
│   ├── refs/heads/checkpoint/undo-1712736312000
│   ├── refs/heads/checkpoint/before-refactor
│   └── _worktree/         # Temp working directory (auto-managed)
└── projects.json           # hash → absolute path mapping
```

- Storage: External bare git repo, indexed by MD5 of absolute project path
- Project isolation: The project's own `.git` is NEVER touched
- Branch strategy: `main` = current state; `checkpoint/*` = preserved states (never deleted)
- Undo: Creates checkpoint branch at HEAD → resets to target → force-pushes main

## Important Notes

1. **ALWAYS snapshot after writes** — #1 rule, no exceptions
2. **Output is JSON** — parse the JSON line, ignore any other text
3. **Don't double-snapshot** — one change = one snapshot
4. **Describe accurately** — the description is how users and future AI understand history
5. **Absolute paths only** — always pass full absolute path
6. **Undo preserves history** — previous states live forever as `checkpoint/*` branches
