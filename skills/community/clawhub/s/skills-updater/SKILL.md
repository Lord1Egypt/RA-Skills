# Skills Updater - 技能自动升级器

自动检测、备份和升级 OpenClaw 技能，支持智能缓存、重试机制、预演模式和详细报告。

Automatically detect, update, and manage OpenClaw skills with intelligent caching, backup, and reporting.

## Features

✅ **Auto-detection** — Scans all installed skills and detects available updates  
✅ **Smart caching** — 24h TTL cache reduces unnecessary API calls  
✅ **Automatic backup** — Creates dated backups before each update  
✅ **Dry-run mode** — Preview changes without modifying anything  
✅ **Detailed reporting** — Generates upgrade summaries to workspace/memory  
✅ **Retry logic** — Exponential backoff handles rate limits gracefully  
✅ **Security hardened** — No hardcoded secrets, proper SSL, secure permissions  

## Installation

```bash
clawhub install skills-updater
```

## Usage

### Check for updates (no API calls, uses cache)
```bash
python3 ~/.openclaw/skills/skills-updater/scripts/check-skill-updates.py --cache-only
```

### Preview updates without making changes
```bash
python3 ~/.openclaw/skills/skills-updater/scripts/check-skill-updates.py --dry-run
```

### Auto-upgrade all skills
```bash
python3 ~/.openclaw/skills/skills-updater/scripts/check-skill-updates.py --auto
```

### Verbose output
```bash
python3 ~/.openclaw/skills/skills-updater/scripts/check-skill-updates.py --auto -v
```

## How It Works

1. **Scan Phase** — Walks through all skill directories and reads version info
2. **Cache Check** — Looks up latest version from cached data (24h old or newer)
3. **Detection** — Identifies skills where `current < latest`
4. **Backup** — Creates timestamped folder copy of each skill before update
5. **Update** — Downloads and applies latest version from ClawHub
6. **Report** — Writes summary to `~/.openclaw/workspace/memory/skill-upgrades-YYYY-MM-DD.md`

## Safety

- **Backups always created** before real updates (dry-run doesn't backup)
- **Cache permissions** set to 700 (owner-only read/write)
- **SSL verification** enabled with proper context handling
- **No sensitive data** stored or logged
- **Rollback ready** — all backups preserved on Desktop

## API Reference

### Command-line Options

| Flag | Effect |
|------|--------|
| `--cache-only` | Use cached data, no API calls |
| `--dry-run` | Show what would update, don't do it |
| `--auto` | Perform actual updates with backups |
| `-v`, `--verbose` | Show detailed logs |
| `-h`, `--help` | Display help |

### Exit Codes

- `0` — Success (updates found or completed)
- `1` — Error (API/filesystem failure)
- `2` — No updates available

## Backup & Recovery

Updates create backups at:
```
~/Desktop/skill-backups/
├── skill-name-1.0.0-20260325-094830/
├── skill-name-1.0.0-20260325-120000/
└── ...
```

To restore:
```bash
cp -r ~/Desktop/skill-backups/skill-name-VERSION-TIMESTAMP ~/.openclaw/skills/skill-name
```

## Configuration

Edit top of script to customize:

```python
SKILLS_DIRS = [...]          # Where to look for skills
BACKUP_DIR = ...             # Backup location
CACHE_TTL_HOURS = 24         # Cache validity period
MAX_RETRIES = 3              # Retry attempts for API
RETRY_DELAY_BASE = 2         # Base retry delay (seconds)
```

## Performance

Tested performance metrics:

- **Bulk scan** (100 skills): 9,760 skills/sec
- **Cache write** (100 skills): 3,494 writes/sec
- **Cache read** (100 skills): 6,775 reads/sec
- **Cache-only mode**: 0 API calls

## Troubleshooting

### "Connection timeout"
- Check internet / proxy settings
- Use `--cache-only` to work offline

### "Permission denied on backup"
- Ensure write access to `~/Desktop/skill-backups/`
- Check disk space

### "Update failed but backup succeeded"
- Backup is preserved at ~/Desktop/skill-backups/
- Manual restore: `cp -r` the backup folder

## License

MIT

## Credits

Built by 狗剩 (Goason) for OpenClaw.

---

**Latest Version:** 1.1.0
**Last Updated:** 2026-03-29  
**Status:** Production Ready ✅
