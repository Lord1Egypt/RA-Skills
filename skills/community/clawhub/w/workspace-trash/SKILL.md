---
name: workspace-trash
description: Soft-delete protection for workspace files. Intercept file deletions and move them to a recoverable trash instead of permanent removal. Use when deleting, removing, or cleaning up files in the workspace. Triggers on /trash, /trash:view, /trash:empty, /trash:restore, or any file deletion request. Also use when the agent needs to rm/delete/remove any file — always trash instead of permanently deleting.
requiredBinaries:
  - node
  - mv
  - cp
  - rm
  - find
  - awk
  - date
  - basename
  - dirname
---

# Workspace Trash

Never permanently delete workspace files. Always use trash instead of `rm`.

## Dependencies

- **Node.js** (`node`) — required for manifest (JSON) management
- **POSIX utilities** — `mv`, `cp`, `rm`, `find`, `awk`, `date`, `basename`, `dirname`

## Configuration

| Variable | Default | Description |
|---|---|---|
| `OPENCLAW_HOME` | `$HOME/.openclaw` | OpenClaw root directory. Only files under this path can be trashed. |
| `OPENCLAW_WORKSPACE` | `$OPENCLAW_HOME/workspace` | Primary workspace directory. Trash lives at `$OPENCLAW_WORKSPACE/.trash/`. |

These variables are standard OpenClaw environment variables and are typically already set. The script uses safe defaults if unset.

## Slash Commands

- `/trash` — Show trash menu (view, empty, restore options)
- `/trash:view` — List all items in trash
- `/trash:empty` — Permanently delete all trash contents (confirm first!)
- `/trash:restore` — List items and ask which to restore

## Script

```bash
bash skills/workspace-trash/scripts/trash.sh <action> [args...]
```

Actions: `move`, `list`, `restore <id|index>`, `empty`, `size`

## Security

- **Scope lock:** Only files under `$OPENCLAW_HOME` (default `~/.openclaw/`) can be trashed. Paths outside this boundary are refused.
- **Symlink resolution:** All paths are resolved to their real location before the scope check, preventing symlink traversal attacks.
- **No shell interpolation of user data:** All user-provided paths and filenames are passed to Node.js via environment variables (`process.env`), never via string interpolation into `node -e` scripts. This prevents code injection via crafted filenames.
- **`--` separators:** All `mv`, `cp`, and `rm` calls use `--` to prevent filenames starting with `-` from being interpreted as flags.

## Destructive Operations

- **`empty` action:** Uses `rm -rf` to permanently delete all trash contents. This is **irreversible**. The agent must always confirm with the user and show what will be deleted before running this action.
- **Cross-filesystem fallback:** When `mv` fails across filesystem boundaries, the script falls back to `cp -a` + `rm -rf`. The source is only deleted after a successful copy.

## Rules

1. **NEVER use `rm` or `rm -rf` on OpenClaw files.** Always use the trash script's `move` action instead.
2. When asked to delete/remove/clean up files, use `trash.sh move <path>` — not rm.
3. Before emptying trash, always confirm with the user and show what will be deleted.
4. The trash lives at `.trash/` in the primary workspace root. A `.manifest.json` tracks original paths for restoration.
5. **Scope: any file under `~/.openclaw/`** — primary workspace, agent workspaces (`workspace-*`), and other OpenClaw directories. The script refuses paths outside `~/.openclaw/`.
6. **Cross-filesystem support:** Agent workspaces may be on different mounts. The script uses `cp -a` + `rm` as a fallback when `mv` fails across filesystems. Restore also handles cross-filesystem moves.
7. Restore by index number (from list) or by trash name. Items from agent workspaces show `[agent]` tag in list view.
8. When multiple files are being deleted, pass them all in one command: `trash.sh move file1 file2 dir1`
