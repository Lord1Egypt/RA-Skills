# Skill Guardian Cron Configuration

## Automated Execution (1-2 times daily)

### Option 1: System Cron (推荐)

Add to crontab:

```bash
# Edit crontab
crontab -e

# Add lines for morning (8am) and evening (8pm) runs
0 8 * * * cd /root/.openclaw/workspace && python3 skills/skill-guardian/scripts/auto_run.py >> logs/skill-guardian.log 2>&1
0 20 * * * cd /root/.openclaw/workspace && python3 skills/skill-guardian/scripts/auto_run.py >> logs/skill-guardian.log 2>&1
```

### Option 2: OpenClaw Cron

Add to OpenClaw config:

```json
{
  "cron": [
    {
      "name": "skill-guardian-morning",
      "schedule": "0 8 * * *",
      "command": "python3 skills/skill-guardian/scripts/auto_run.py",
      "cwd": "/root/.openclaw/workspace"
    },
    {
      "name": "skill-guardian-evening", 
      "schedule": "0 20 * * *",
      "command": "python3 skills/skill-guardian/scripts/auto_run.py",
      "cwd": "/root/.openclaw/workspace"
    }
  ]
}
```

### Option 3: Heartbeat Mode

Add to HEARTBEAT.md:

```markdown
## Skill Guardian Check
Run twice daily (approx 8am/pm):
```
python3 skills/skill-guardian/scripts/auto_run.py
```
```

## Manual Execution

```bash
# Full auto-run (check pending + updates + apply)
python3 skills/skill-guardian/scripts/auto_run.py

# Individual steps
python3 skills/skill-guardian/scripts/process_pending.py  # Promote pending skills
python3 skills/skill-guardian/scripts/check_updates.py    # Check for updates
python3 skills/skill-guardian/scripts/apply_updates.py --all  # Apply updates
```

## Log Rotation

```bash
# Add to crontab for log rotation
0 0 * * 0 cd /root/.openclaw/workspace && mv logs/skill-guardian.log logs/skill-guardian.log.1
```
