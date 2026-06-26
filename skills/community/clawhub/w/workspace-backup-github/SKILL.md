---
name: workspace-backup-github
description: |
  Backup AI Agent workspace to GitHub - One-click backup for OpenClaw, Claude Code, Cursor, and other AI Agent workspaces to a private GitHub repository. Supports two modes: (1) Auto mode - scheduled automatic backup (2) Manual mode - interactive setup wizard. Automatically guides users through: GitHub Token config → Repository creation → Initial backup → Scheduled backup setup. Perfect for: AI Agent developers, multi-device users, anyone who wants to protect their workspace from data loss.
  Trigger keywords: backup, github backup, auto backup, workspace backup, backup to github, git backup, scheduled backup, sync to github
metadata: {"openclaw": {"emoji": "📦"}}
---

# Workspace GitHub Backup

One-click backup solution for AI Agent workspaces to a private GitHub repository.

## Quick Start

> **First time setup:** Tell me "setup GitHub backup" and I'll guide you through the interactive wizard!

> **Already configured:** Just say "backup now" to trigger an immediate backup.

---

## Features

### Two Backup Modes

| Mode | Trigger | Description |
|------|---------|-------------|
| **Manual** | "setup backup" | Interactive Q&A to configure |
| **Auto** | After setup | Scheduled via OpenClaw Cron |

### What Gets Backed Up ✅

| Files/Directories | Description |
|-------------------|-------------|
| `skills/` | All installed skills |
| `memory/` | Daily memory files |
| `AGENTS.md` | Agent configuration |
| `SOUL.md` | AI identity definition |
| `USER.md` | User information |
| `IDENTITY.md` | AI identity info |
| `TOOLS.md` | Local tools config |
| `HEARTBEAT.md` | Heartbeat tasks |
| Config files | README.md, SYNC.md, etc. |

### What's Excluded ❌

| Pattern | Description |
|---------|-------------|
| `.clawhub/` | ClawHub cache |
| `.openclaw/` | Runtime data |
| `node_modules/` | Dependencies |
| `*.log` | Log files |
| `*.tmp` | Temp files |
| `.DS_Store` | System files |
| API Keys | Sensitive info in env vars |

---

## Interactive Setup Wizard

When user says "setup GitHub backup", ask these questions one by one:

### Question 1: GitHub Username
> Please tell me your GitHub username.

Wait for answer (e.g., "johnsmith")

### Question 2: Repository Name
> What name would you like for your backup repository?
> Suggestion: `ai-workspace-backup` or `agent-workspace`

Wait for answer

### Question 3: GitHub Token
> Now let's generate a GitHub Token:
> 1. Go to https://github.com/settings/tokens
> 2. Click "Generate new token (classic)"
> 3. Note: `backup-token`
> 4. Check the `repo` permission (full control of private repositories)
> 5. Click "Generate token"
> 6. Copy and paste the Token here

Wait for token (format: ghp_xxx)

### Question 4: Backup Time
> When would you like automatic backup to run each day?
> - A) 3:00 AM (midnight owl)
> - B) 7:00 AM (morning)
> - C) 12:00 PM (noon)
> - D) 6:00 PM (evening)
> 
> Or tell me your preferred time (e.g., "every day at 5 PM")

Wait for selection

### Question 5: Confirm
> Configuration summary:
> - GitHub Username: [username]
> - Repository: [repo-name]
> - Backup Time: [time]
> 
> Reply "confirm" or "yes" to start setup, or tell me what to change.

After confirmation:
1. Initialize Git repo
2. Run first backup
3. Set up OpenClaw Cron

---

## Usage Commands

### Manual Triggers

```bash
# Immediate backup
"backup now"
"backup immediately"
"run backup now"

# Check status
"backup status"
"when did we last backup"
"show backup status"

# Restore
"restore from GitHub"
"recover workspace"

# Modify setup
"change backup time"
"pause auto backup"
```

### Trigger Keywords

The skill activates when user or agent says:
- "setup GitHub backup"
- "backup to github"
- "auto backup"
- "manual backup"
- "backup now"
- "backup status"
- "workspace backup"
- "git backup"
- "scheduled backup"
- "sync to github"

---

## Troubleshooting

### Common Issues

| Problem | Cause | Solution |
|---------|-------|----------|
| "Permission denied" | Invalid token | Regenerate token with `repo` scope |
| "Repository not found" | Wrong repo name | Check spelling |
| "Push failed" | No network | Check connection |
| "Cron not running" | Config error | Run `openclaw cron list` |

### Manual Fix Commands

```bash
# Check remote
git remote -v

# Reset remote with new token
git remote set-url origin https://x-access-token:TOKEN@github.com/user/repo.git

# View cron jobs
openclaw cron list

# Manual backup
cd /root/.openclaw/workspace
git add skills/ memory/ AGENTS.md SOUL.md USER.md IDENTITY.md TOOLS.md HEARTBEAT.md README.md SYNC.md .gitignore
git commit -m "Backup: $(date +%Y-%m-%d)"
git push origin main
```

---

## For Other AI Agents

If you're another AI agent using this skill:

1. **First backup:** Run the setup wizard to configure
2. **Subsequent backups:** Use `openclaw cron add` to set schedule
3. **Manual trigger:** Execute git add/commit/push commands
4. **Status check:** Run `git log -1` to see last backup time

Example cron setup:
```bash
openclaw cron add --name "workspace-backup" --cron "0 3 * * *" --message "Execute workspace backup" --agent main
```

---

## Security Notes

- Token is stored in Git remote URL (not in files)
- Sensitive data (API keys, passwords) are NOT backed up
- Backup archive contains no credentials
- Use a private repository for backup
- If token is compromised, revoke it immediately in GitHub Settings

---

## Recovery Guide

When user needs to restore:

```bash
# 1. Clone the backup repo
git clone https://github.com/[username]/[repo].git /tmp/restore

# 2. Restore files
cp -r /tmp/restore/* ~/.openclaw/workspace/

# 3. Reconfigure environment variables
# (sensitive info not in backup)
```

---

## Author

Created by Jeremy for OpenClaw community. Published to ClawHub for anyone to use and improve.