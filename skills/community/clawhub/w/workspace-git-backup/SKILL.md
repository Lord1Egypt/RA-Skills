---
name: workspace-git-backup
description: Set up automatic scheduled backups to GitHub or GitLab. Use when users want to backup their OpenClaw workspace or other directories. Supports GitHub CLI for easy repo creation. Works on macOS (launchd) and Linux (cron).
---

# GitHub Backup

Automatic scheduled backup of any directory to a remote Git repository.

## Setup Flow

When user asks for backup setup, follow these steps:

### 1. Ask for backup directory

Default: `~/.openclaw/workspace`

### 2. Configure remote repository

**If GitHub CLI (`gh`) is available and authenticated:**

Ask user:
- "新建 GitHub 仓库 还是 同步到已有仓库？"

**New repo:**
```bash
gh repo create <name> --private --source=<backup-path> --remote=origin
```

**Existing repo:**
```bash
# List repos
gh repo list --limit 50

# Add remote (user provides repo name or URL)
git -C <backup-path> remote add origin <url>
```

**If no GitHub CLI:**
- Ask user for repository URL directly

### 3. Create config file

```bash
cat > ~/.openclaw/workspace/.backup-config.json << 'EOF'
{
  "backupPath": "<backup-path>",
  "gitRemote": "<repo-url>",
  "schedule": "0 12,0 * * *",
  "updateTimestamp": true
}
EOF
```

### 4. Install backup script

```bash
mkdir -p ~/.openclaw/scripts
cp <skill-path>/scripts/backup.sh ~/.openclaw/scripts/github-backup.sh
chmod +x ~/.openclaw/scripts/github-backup.sh
```

### 5. Install scheduled task

**macOS (launchd):**
```bash
bash <skill-path>/scripts/install-launchd.sh
```

**Linux (cron):**
```bash
bash <skill-path>/scripts/install-cron.sh
```

### 6. Optional: First backup

```bash
bash ~/.openclaw/scripts/github-backup.sh
```

## Commands

After setup, user can:

| Command | Action |
|---------|--------|
| `bash ~/.openclaw/scripts/github-backup.sh` | Manual backup |
| `bash <skill-path>/scripts/manage.sh status` | Check status |
| `bash <skill-path>/scripts/manage.sh logs` | View logs |
| `bash <skill-path>/scripts/manage.sh uninstall` | Remove scheduled task |

## Configuration

Config: `~/.openclaw/workspace/.backup-config.json`

| Field | Default | Description |
|-------|---------|-------------|
| `backupPath` | `~/.openclaw/workspace` | Directory to backup |
| `gitRemote` | required | Repository URL |
| `schedule` | `0 12,0 * * *` | Cron: 12:00 & 00:00 daily |
| `updateTimestamp` | true | Update README timestamp |

## Backup Script Logic

```
Check for git changes
  └── No changes → exit
  └── Has changes → continue
       ↓
Update README timestamp (optional)
       ↓
git add . && git commit -m "chore: 自动备份"
       ↓
git push
```

## Files Created

| File | Location |
|------|----------|
| Backup script | `~/.openclaw/scripts/github-backup.sh` |
| Config | `~/.openclaw/workspace/.backup-config.json` |
| Log | `~/.openclaw/logs/github-backup.log` |
| launchd plist | `~/Library/LaunchAgents/com.openclaw.github-backup.plist` |
| cron entry | Via crontab |

## Example Dialog

```
User: 帮我配置 workspace 自动备份

Agent:
1. 检测 gh CLI → 已登录
2. "新建仓库还是用已有的？" → "新建"
3. "仓库名称？" → "openclaw-backup"
4. "公开还是私有？" → "私有"
5. 执行: gh repo create openclaw-backup --private --source=~/.openclaw/workspace --remote=origin
6. 创建配置文件
7. 安装定时任务
8. "安装完成，每天 12:00 和 00:00 自动备份"
```
