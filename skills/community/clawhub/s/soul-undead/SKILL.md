---
name: soul-undead
description: Backup, restore, initialize, and sync core OpenClaw workspace markdown files with the fixed private GitHub repository `soul-undead`. Use when the user wants reinstall-safe recovery of AGENTS.md, HEARTBEAT.md, IDENTITY.md, SOUL.md, TOOLS.md, USER.md, and MEMORY.md, or wants those files kept synced to GitHub after real saved changes. Always check GitHub CLI authentication first; if not authenticated, stop and guide the user to complete `gh auth login`.
---

# Soul Undead

Manage these fixed core files from the OpenClaw workspace:

- `AGENTS.md`
- `HEARTBEAT.md`
- `IDENTITY.md`
- `SOUL.md`
- `TOOLS.md`
- `USER.md`
- `MEMORY.md`

Fixed repository name:

- `soul-undead`

Repository visibility is always **private**.

## What this skill does

This skill is for preserving and restoring the core markdown files that define an OpenClaw workspace identity and behavior. It is designed for these situations:

- First-time setup of a private backup repo for the core files
- Restoring the core files onto a new machine after reinstalling OpenClaw
- Manually syncing saved local changes back to the GitHub backup repo

This skill intentionally does **not** scan the whole workspace and does **not** back up every markdown file. It only manages this fixed core file set.

## Rules

- Always check `gh auth status` first.
- If GitHub authentication is missing, stop and tell the user to run `gh auth login`.
- Do not scan the whole workspace.
- Do not ask the user to choose files unless they explicitly ask for a different scope.
- Treat the fixed GitHub repo as the authority during first-time initialization on a new machine.
- Before any remote restore overwrites local files, create a timestamped local backup snapshot under `skills/soul-undead/local-backups/`.
- Do not keep a persistent local export mirror; sync should act directly on the GitHub private repo.

## Important behavior: first restore can overwrite local default files

On a new machine, OpenClaw may already have generated local default markdown files. This skill does **not** treat those default files as authoritative.

If all of the following are true:

- GitHub authentication succeeds
- The fixed repo `soul-undead` exists
- The local state file does not yet say `initialized: true`

then this skill will treat that run as a **first-time restore scenario** and pull the remote file set down to the local workspace.

That means the remote files can overwrite local default files created by a fresh OpenClaw installation.

To reduce risk, the restore order is always:

1. save the current local file set into a timestamped snapshot
2. pull the remote file set from GitHub
3. overwrite the current local files with the remote version

The snapshot is stored under:

- `~/.openclaw/workspace/skills/soul-undead/local-backups/<timestamp>/`

That snapshot is the local fallback if the restore direction was wrong or the remote version is not the one the user wants.

## State file

Use a local state file to mark successful initialization:

- `~/.openclaw/workspace/skills/soul-undead/.workspace-backup-state.json`

Write:

```json
{"initialized": true, "repo": "soul-undead"}
```

Only after one of these succeeds:

1. Restore succeeds from the default GitHub repo
2. First-time repo creation and initial upload succeeds

Do not write `initialized: true` on failure.

## Required dependencies

This skill assumes these tools are available:

- `git`
- `gh` (GitHub CLI)
- `python3`

Minimum expectations:

- `gh auth status` must succeed before any restore or sync
- The active GitHub account must have permission to read/create/push the private repo

If `gh` is installed but not authenticated, stop and tell the user to run:

```bash
gh auth login
```

If a dependency is missing, tell the user exactly which command/tool must be installed before continuing.

## Required user-facing reminders before execution

Before executing restore, first-time init, or sync, explicitly remind the user of the relevant points below.

### Always remind

- This skill only manages these files: `AGENTS.md`, `HEARTBEAT.md`, `IDENTITY.md`, `SOUL.md`, `TOOLS.md`, `USER.md`, `MEMORY.md`
- The GitHub repository is private and fixed to `soul-undead`
- `gh auth login` is required if GitHub CLI authentication is missing

### If first-time restore may happen

Explicitly warn that:

- if the remote repo already exists, the skill may restore remote files onto the local workspace during first initialization
- this can overwrite local default markdown files created by a fresh OpenClaw install
- before overwrite, the skill will create a timestamped local backup snapshot under `skills/soul-undead/local-backups/`

### If sync/upload is the user's intent

Explicitly confirm the task as sync/upload intent and avoid accidentally running restore-first behavior.

## Workflow

### 1. Check GitHub authentication

Run:

```bash
gh auth status
```

If authentication fails, stop and guide the user to run:

```bash
gh auth login
```

### 2. Initialization / restore decision

Use the bundled script:

```bash
bash <skill-dir>/scripts/init_or_sync.sh
```

Behavior:

- Uses the fixed repo name `soul-undead`
- Uses the fixed core file set only
- If the state file is missing or not initialized:
  - If the GitHub repo exists, first snapshot the current local files, then restore from GitHub, then overwrite the local file set
  - If the GitHub repo does not exist, create it as private and upload the local file set directly to GitHub
  - On success, write `initialized: true`
- If already initialized, sync local saved changes directly to GitHub

### 3. Sync after saved changes

After initialization is complete, use the same script again whenever the tracked files may have changed.

Behavior:

- Reads the fixed file set directly from the workspace
- Writes each tracked file directly to the GitHub private repo
- Also maintains `README.md` and `restore.sh` in the GitHub repo
- Does not keep a persistent local export mirror

## Preview / dry-run design (not implemented yet)

If preview support is added later, it should report intent without making changes.

The preview should show these four things:

1. **Planned path**
   - `restore from remote`
   - `first-time init + upload`
   - `sync upload`
   - `no-op`

2. **Affected files**
   - Which of the fixed core files would be overwritten locally
   - Or which of the fixed core files would be written to GitHub

3. **Safety actions**
   - Whether a local timestamped snapshot would be created before remote restore
   - The expected backup path under `skills/soul-undead/local-backups/<timestamp>/`

4. **Precondition status**
   - Whether `gh auth status` passes
   - Whether the default repo exists
   - Whether the state file is initialized

Preview mode should never:

- overwrite local files
- create or update the GitHub repo
- write remote file contents
- write `initialized: true`

## Failure handling

Use these failure rules:

### GitHub auth failure
- Do not continue
- Tell the user to run `gh auth login`

### Missing dependency
- Do not continue
- Tell the user which dependency is missing: `git`, `gh`, or `python3`

### Repo does not exist during first use
- Treat it as first-time initialization
- Create the private repo
- Upload the local fixed file set directly to GitHub
- Only then write `initialized: true`

### Remote restore fails
- Do not write `initialized: true`
- Keep the local backup snapshot that was created before overwrite
- Tell the user restore failed and where the local snapshot is stored

### Remote restore succeeds but the restored version is wrong
- Treat the local pre-restore snapshot as the rollback source of truth
- Restore the desired files back from `local-backups/<timestamp>/` into the workspace
- After confirming the workspace is correct again, sync that corrected local version back to GitHub

### Sync/push fails
- Do not change initialization state
- Tell the user the sync failed
- Leave the local files untouched so sync can be retried later

## Defaults

- Workspace path: `~/.openclaw/workspace`
- State file: `~/.openclaw/workspace/skills/soul-undead/.workspace-backup-state.json`
- Local restore-safety backup path: `~/.openclaw/workspace/skills/soul-undead/local-backups/<timestamp>/`
- Repository visibility: **private**
- Repository name: `soul-undead`
- Tracked files: fixed core file set only

## Notes

- On a new machine, remote restore wins over freshly generated local default md files during first initialization.
- The remote repo stores helper files such as `README.md` and `restore.sh` alongside the tracked markdown files.
- This skill is intentionally minimal: no whole-workspace scan, no persistent local export repo mirror.
