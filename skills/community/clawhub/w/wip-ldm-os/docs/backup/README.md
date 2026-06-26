# Backup

## One Script, One Place

`~/.ldm/bin/ldm-backup.sh` runs daily at 3:00 AM via LaunchAgent `ai.openclaw.ldm-backup`. It backs up everything to `~/.ldm/backups/`, then tars it to iCloud for offsite.

## What Gets Backed Up

| Source | Method | What's in it |
|--------|--------|-------------|
| `~/.ldm/memory/crystal.db` | sqlite3 .backup | Irreplaceable memory (all agents) |
| `~/.ldm/agents/` | cp -a | Identity files, journals, daily logs |
| `~/.ldm/state/` | cp -a | Config, version, registry |
| `~/.ldm/config.json` | cp | Workspace pointer, org |
| `~/.openclaw/memory/main.sqlite` | sqlite3 .backup | OC conversations |
| `~/.openclaw/memory/context-embeddings.sqlite` | sqlite3 .backup | Embeddings |
| `~/.openclaw/workspace/` | tar | Shared context, daily logs |
| `~/.openclaw/agents/main/sessions/` | tar | OC session JSONL |
| `~/.openclaw/openclaw.json` | cp | OC config |
| `~/.claude/CLAUDE.md` | cp | CC instructions |
| `~/.claude/settings.json` | cp | CC settings |
| `~/.claude/projects/` | tar | CC auto-memory + transcripts |
| Workspace directory | tar (excludes node_modules, .git/objects, old backups, _trash) | Entire workspace |

**NOT backed up:** node_modules/, .git/objects/ (reconstructable), extensions (reinstallable), ~/.claude/cache.

## Backup Structure

```
~/.ldm/backups/2026-03-24--09-50-22/
  ldm/
    memory/crystal.db
    agents/
    state/
    config.json
  openclaw/
    memory/main.sqlite
    memory/context-embeddings.sqlite
    workspace.tar
    sessions.tar
    openclaw.json
  claude/
    CLAUDE.md
    settings.json
    projects.tar
  <workspace>.tar
```

## iCloud Offsite

After local backup, the entire dated folder is compressed and copied to iCloud. The destination path is read from `~/.ldm/config.json` at `paths.icloudBackup`.

One file per backup. iCloud syncs it across devices. Rotation matches the local retention setting.

## How to Run

```bash
~/.ldm/bin/ldm-backup.sh                    # run backup now
~/.ldm/bin/ldm-backup.sh --dry-run          # preview what would be backed up
~/.ldm/bin/ldm-backup.sh --keep 14          # keep 14 days instead of 7
~/.ldm/bin/ldm-backup.sh --include-secrets   # include ~/.ldm/secrets/
```

You can also run via the CLI:

```bash
ldm backup                                   # run backup now
ldm backup --dry-run                         # preview with sizes
ldm backup --pin "before upgrade"            # pin latest backup so rotation skips it
```

## How to Restore

```bash
~/.ldm/bin/ldm-restore.sh                           # list available backups
~/.ldm/bin/ldm-restore.sh 2026-03-24--09-50-22      # restore everything
~/.ldm/bin/ldm-restore.sh --only ldm <backup>       # restore only crystal.db + agents
~/.ldm/bin/ldm-restore.sh --only openclaw <backup>  # restore only OC data
~/.ldm/bin/ldm-restore.sh --from-icloud <file>      # restore from iCloud tar
~/.ldm/bin/ldm-restore.sh --dry-run <backup>        # preview
```

After restore: `openclaw gateway restart` then `crystal status` to verify.

## Schedule

| What | When | How |
|------|------|-----|
| Backup | 3:00 AM | LaunchAgent `ai.openclaw.ldm-backup` |

One LaunchAgent. One script. No Full Disk Access currently (target: midnight via LDMDevTools.app once PID error is fixed). Verify is built into the script (exit code + log).

## Config

All backup settings live in `~/.ldm/config.json`:
- `paths.workspace` ... workspace path
- `paths.icloudBackup` ... iCloud offsite destination
- `backup.keep` ... retention days (default: 7)
- `backup.includeSecrets` ... whether to include `~/.ldm/secrets/`
- `org` ... used for tar filename prefix

## Logs

`~/.ldm/logs/backup.log` (LaunchAgent stdout/stderr)

## Technical Details

See [TECHNICAL.md](./TECHNICAL.md) for config schema, LaunchAgent plist, rotation logic, and script internals.
