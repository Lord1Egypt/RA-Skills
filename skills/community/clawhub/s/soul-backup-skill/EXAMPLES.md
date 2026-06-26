# Examples

## Example 1: Daily Automated Backup

Create a daily backup at 2 AM with automatic naming:

```bash
# Add to crontab: crontab -e
0 2 * * * cd ~/.openclaw/workspace-YOUR-AGENT/soul-backup-skill && node scripts/backup.mjs --name "daily-$(date +\%Y-\%m-\%d)"
```

## Example 2: Pre-Deployment Backup

Before deploying changes to production:

```bash
cd soul-backup-skill
node scripts/backup.mjs --name "pre-deploy-$(git rev-parse --short HEAD)" --desc "Backup before deploying commit abc123"
```

## Example 3: Recover from Accidental Deletion

You accidentally deleted `SOUL.md`:

```bash
# Restore just that file
node scripts/restore.mjs --file SOUL.md

# Verify it's back
cat ../SOUL.md
```

## Example 4: Rollback Bad Configuration

You modified `AGENTS.md` and broke your agent:

```bash
# List backups to find the right one
node scripts/list.mjs

# Preview restore
node scripts/restore.mjs --timestamp 2026-03-04T23-30-00 --dry-run

# Restore
node scripts/restore.mjs --timestamp 2026-03-04T23-30-00
```

## Example 5: Validate Backup Integrity

Check all backups for corruption:

```bash
# Validate all
node scripts/validate.mjs

# Validate specific backup
node scripts/validate.mjs --timestamp 2026-03-04T23-30-00
```

## Example 6: Named Backup Before Major Refactor

Before rewriting your SOUL files:

```bash
node scripts/backup.mjs --name "pre-refactor-v2" --desc "Before rewriting SOUL.md personality"
```

Later, restore it:

```bash
node scripts/restore.mjs --name "pre-refactor-v2"
```

## Example 7: Weekly Validation Cron

Automatically validate backups every Sunday at 3 AM:

```bash
# Add to crontab: crontab -e
0 3 * * 0 cd ~/.openclaw/workspace-YOUR-AGENT/soul-backup-skill && node scripts/validate.mjs
```

## Example 8: Emergency Recovery (Scripts Won't Run)

If Node.js is broken or scripts won't execute:

```bash
# Manual restore from backup directory
cd ~/.openclaw/workspace-YOUR-AGENT
cp -r soul-backup-skill/backups/2026-03-04T23-30-00/* .
```

## Example 9: Rollback After Bad Restore

You restored the wrong backup:

```bash
# Every restore creates a pre-restore backup
node scripts/list.mjs | grep pre-restore

# Restore the pre-restore backup
node scripts/restore.mjs --timestamp pre-restore-2026-03-05T01-20-00
```

## Example 10: Verbose Backup Listing

See detailed information about all backups:

```bash
node scripts/list.mjs --verbose
```

Output:

```
📦 Found 3 backup(s)

📅 2026-03-05T01-20-00
   Created: Mar 5, 2026, 01:20:00 AM
   Files: 6 (4.83 KB)
   Location: /path/to/backups/2026-03-05T01-20-00
   Files backed up:
     ✅ SOUL.md (2194 bytes)
     ✅ USER.md (343 bytes)
     ✅ AGENTS.md (747 bytes)
     ✅ IDENTITY.md (636 bytes)
     ✅ TOOLS.md (860 bytes)
     ✅ HEARTBEAT.md (168 bytes)
     ⚠️  BOOTSTRAP.md (not found at backup time)

📌 pre-refactor-v2 (named)
   Created: Mar 4, 2026, 11:30:00 PM
   Description: Before rewriting SOUL.md personality
   Files: 7 (5.12 KB)
   Location: /path/to/backups/named/pre-refactor-v2
   Files backed up:
     ✅ SOUL.md (2194 bytes)
     ✅ USER.md (343 bytes)
     ✅ AGENTS.md (747 bytes)
     ✅ IDENTITY.md (636 bytes)
     ✅ TOOLS.md (860 bytes)
     ✅ HEARTBEAT.md (168 bytes)
     ✅ BOOTSTRAP.md (512 bytes)

💡 Latest backup: 2026-03-05T01-20-00
   To restore: node scripts/restore.mjs --timestamp 2026-03-05T01-20-00
```
