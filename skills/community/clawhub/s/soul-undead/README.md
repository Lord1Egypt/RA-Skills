# soul-undead

A publishable OpenClaw skill project for backing up and restoring core workspace markdown files with a GitHub repository.

## Purpose

`soul-undead` manages this fixed set of core files:

- `AGENTS.md`
- `HEARTBEAT.md`
- `IDENTITY.md`
- `SOUL.md`
- `TOOLS.md`
- `USER.md`
- `MEMORY.md`

It supports two primary flows:

1. **Sync local core files to GitHub**
2. **Restore from GitHub to local workspace**

Before a remote restore overwrites local files, it creates a local timestamped snapshot for rollback safety.

## Included in this publishable project

- `SKILL.md`
- `scripts/init_or_sync.sh`
- `assets/logic-diagram-zh.png`
- `assets/logic-diagram-en.png`

## Not included in the publishable project

These are runtime artifacts and should not be committed or published:

- `local-backups/`
- `.workspace-backup-state.json`

They are created automatically when the installed skill runs.

## Diagrams

### English

![soul-undead logic diagram (EN)](assets/logic-diagram-en.png)


## Notes

- The default repo name is `soul-undead`.
- The skill uses `gh`, `git`, and `python3`.
- `gh auth login` must succeed before restore or sync.
- On first initialization, if the remote repo already exists, the skill restores remote files to local after creating a local snapshot.
- If the restored remote version is wrong, roll back from `local-backups/<timestamp>/` and sync the corrected local version back to GitHub.
