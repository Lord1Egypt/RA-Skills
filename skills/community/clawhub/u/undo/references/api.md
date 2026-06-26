# Undo.skill — API Reference

> Human-readable specification for all scripts in this skill.

## Data Storage

All snapshot data is stored in an external location, never in the target project:

```
~/.local/share/undo-skill/
├── repos/
│   ├── <project-hash>/          # Bare git repo per project
│   │   ├── HEAD
│   │   ├── config
│   │   ├── objects/
│   │   ├── refs/
│   │   └── _worktree/           # Temporary working tree (auto-managed)
│   └── projects.json            # Hash → absolute path mapping
└── (future: config, logs, etc.)
```

**Project hash**: MD5 hash of the project's absolute path, truncated to 12 chars.

**Why external storage?**
- Doesn't interfere with the project's own `.git`
- Works even if the project isn't a git repo
- No `.gitignore` modifications needed
- Clean separation of concerns

## Scripts

### `init.js <project-path>`

Initialize undo tracking for a project.

**Behavior:**
1. Resolves `<project-path>` to absolute path
2. Computes hash and checks if already tracked
3. Creates bare git repo at `~/.local/share/undo-skill/repos/<hash>/`
4. Clones to temp work tree, copies all project files (excluding `node_modules`, `.git`, etc.)
5. Makes initial commit and pushes to bare repo
6. Records hash→path mapping in `projects.json`
7. Cleans up temp work tree

**Output:**
```
✅ Initialized tracking for /absolute/path/to/project
   Snapshots stored in: ~/.local/share/undo-skill/repos/abc123def456
```
or
```
ℹ️  Already tracked
```

**Exit codes:**
- `0` — Success (including "already tracked")
- `1` — Failure (prints error message)

---

### `snapshot.js <project-path> [description]`

Record the current state of files as a snapshot.

**Behavior:**
1. Ensures project is tracked (init'd)
2. Syncs temp work tree with bare repo
3. Copies current project files into work tree
4. Stages all changes (`git add -A`)
5. If no changes, exits with "No changes to snapshot"
6. Creates commit with structured message:
   ```
   🔄 [auto] 2026-04-10 14:05:12 | Description provided by user

   Files changed:
   M  src/index.js
   A  src/utils.ts
   D  src/old-file.js
   ```
7. Pushes to bare repo

**Commit message format:**
- Line 1: `🔄 [auto] <YYYY-MM-DD HH:mm:ss> | <description>`
- Blank line
- `Files changed:` header
- Git status lines (M/A/D/R followed by file path)

**Output:**
```
✅ Snapshot created: Description provided by user
   Hash: abc1234
```
or
```
ℹ️  No changes to snapshot
```

**Exit codes:**
- `0` — Success (including "no changes")
- `1` — Failure

---

### `list.js <project-path> [--limit N] [--json]`

List the change history for a tracked project.

**Options:**
- `--limit N` — Show only the last N entries (default: 20)
- `--json` — Output as JSON array instead of human-readable text

**Human-readable output:**
```
Change history for /path/to/project:

[5] 2026-04-10 14:05:12  🔄 Refactored auth middleware to use JWT
    └─ M src/auth.js
    └─ A src/jwt.js
    └─ D src/session.js

[4] 2026-04-10 14:03:45  🔄 Added utility functions for date formatting
    └─ A src/utils.ts (+45 lines)

[3] 2026-04-10 14:01:00  🔄 Added error handling to main route
    └─ M src/index.js (+8, -2)

[2] 2026-04-10 13:58:30  🏁 checkpoint: before-refactor

[1] 2026-04-10 13:55:00  🌱 initial commit
```

**JSON output:**
```json
[
  {
    "hash": "abc1234",
    "date": "2026-04-10 14:05:12 +0800",
    "subject": "🔄 [auto] 2026-04-10 14:05:12 | Refactored auth middleware to use JWT",
    "files": ["M src/auth.js", "A src/jwt.js", "D src/session.js"]
  }
]
```

**Markers:**
- `🌱` — Initial commit
- `🏁` — Named checkpoint
- `🔄` — Regular snapshot

**Exit codes:**
- `0` — Success
- `1` — Project not tracked or other error

---

### `undo.js <project-path> [options]`

Revert to a previous state.

**Options:**
- `--steps N` — Undo N changes (default: 1)
- `--to <checkpoint-name>` — Undo to a named checkpoint
- `--timestamp <ISO>` — Undo to a specific time (ISO 8601 format)
- `--dry-run` — Show what would happen without changing files

**Behavior for `--steps N`:**
1. Finds `HEAD~N` as the target commit
2. Creates a branch `checkpoint/undo-<timestamp>` at current HEAD (preserves current state)
3. Resets work tree to target commit
4. Copies files back to the actual project directory
5. Force-pushes to update bare repo's main branch

**Behavior for `--to <name>`:**
1. Looks for branch `checkpoint/<name>` (or just `<name>`)
2. Saves current HEAD to `checkpoint/undo-before-<timestamp>`
3. Resets to the checkpoint branch
4. Copies files back to project

**Behavior for `--timestamp <ISO>`:**
1. Walks commit history in date order
2. Finds the latest commit at or before the given timestamp
3. Saves current HEAD to a checkpoint branch
4. Resets to that commit
5. Copies files back to project

**Output on success:**
```
↩️  Undoing last 1 change(s)
✅ Undid 1 step(s). Previous state saved to branch "checkpoint/undo-1712736312000"
   Previous state preserved on branch: checkpoint/undo-1712736312000
   To restore: git checkout checkpoint/undo-1712736312000
```

**Safety:**
- Undo NEVER deletes history — it always saves the current state to a branch first
- The user can always restore the pre-undo state via the checkpoint branch
- Multiple undos create multiple checkpoint branches

**Exit codes:**
- `0` — Success
- `1` — Failure (not enough history, checkpoint not found, etc.)

---

### `checkpoint.js <project-path> <checkpoint-name>`

Create a named checkpoint at the current state.

**Behavior:**
1. Creates a git branch named `checkpoint/<name>` at current HEAD
2. Does NOT modify any files

**Naming:**
- Spaces are converted to hyphens
- Lowercased
- Example: "before DB migration" → `checkpoint/before-db-migration`

**Output on success:**
```
✅ Checkpoint "before-db-migration" created
   Branch: checkpoint/before-db-migration
```

**Output if already exists:**
```
❌ Checkpoint "before-db-migration" already exists
```

**Exit codes:**
- `0` — Success
- `1` — Already exists or project not tracked

---

### `watcher.js <project-path>`

Background file watcher that auto-snapshots on changes.

**Behavior:**
1. Polls all files in the project every `UNDO_WATCHER_POLL` ms (default: 2000ms)
2. Compares current file states (mtime + size) with the last known state
3. If changes detected, waits `UNDO_WATCHER_DEBOUNCE` ms (default: 5000ms) before snapshotting
4. Debounces rapid changes into a single snapshot
5. Skips snapshoting if one was taken within the debounce window

**Ignored directories:**
- `node_modules`
- `.git`
- `dist`, `build`, `.next`
- `coverage`

**Ignored extensions:**
- `.log`, `.tmp`, `.swp`, `.swo`, `.pyc`

**Output:**
```
[watcher] Watching: /path/to/project
[watcher] Debounce: 5000ms, Poll: 2000ms
[watcher] PID: 12345
[watcher] Press Ctrl+C to stop
[watcher] Detected 3 file change(s)
[watcher] Taking snapshot: [watcher] modified: src/index.js; added: src/utils.ts
[watcher] ✅ Snapshot created: [watcher] modified: src/index.js; added: src/utils.ts
```

**Environment variables:**
- `UNDO_WATCHER_DEBOUNCE` — Debounce time in ms (default: 5000)
- `UNDO_WATCHER_POLL` — Poll interval in ms (default: 2000)

**Stopping:**
- `Ctrl+C` / `SIGINT` — Graceful shutdown
- `kill <PID>` / `SIGTERM` — Graceful shutdown
- `kill %1` — If running as background job in bash

---

## Library API (`lib/git.js`)

Internal module used by all scripts. Not intended for direct use by the LLM.

### Exports

| Function | Description |
|----------|-------------|
| `getProjectHash(projectPath)` | Returns the 12-char MD5 hash for a project path |
| `getBareRepoPath(projectPath)` | Returns the bare repo path for a project |
| `isTracked(projectPath)` | Returns boolean — is the project being tracked? |
| `initProject(projectPath)` | Initialize tracking. Returns `{ initialized, barePath, message }` |
| `createSnapshot(projectPath, description)` | Create a snapshot commit. Returns `{ committed, hash, message }` |
| `getHistory(projectPath, limit)` | Get commit history. Returns `{ commits: [...], error? }` |
| `getCheckpoints(projectPath)` | List checkpoint branches. Returns `string[]` |
| `undoSteps(projectPath, steps)` | Undo N steps. Returns `{ success, message, targetHash, checkpointBranch }` |
| `undoToCheckpoint(projectPath, name)` | Undo to checkpoint. Returns same shape as undoSteps |
| `undoToTimestamp(projectPath, timestamp)` | Undo to timestamp. Returns same shape as undoSteps |
| `createCheckpoint(projectPath, name)` | Create named checkpoint. Returns `{ success, message, branch }` |

---

## Git Branch Strategy

```
main (bare repo)
├── checkpoint/undo-1712736312000    ← saved before undoing 1 step
├── checkpoint/undo-1712736300000    ← saved before undoing to timestamp
├── checkpoint/before-refactor       ← user-created checkpoint
├── checkpoint/before-db-migration   ← user-created checkpoint
└── checkpoint/undo-before-1712736320000  ← saved before undo-to-checkpoint
```

- `main` always points to the latest snapshot (the "current" state)
- `checkpoint/*` branches preserve historical states
- Branches are NEVER deleted automatically
- Force-push to `main` is used during undo, but branches remain intact
