---
name: self-backup
description: Backup important OpenClaw workspace files to a GitHub repository. Use when: (1) user wants to backup workspace configuration, (2) sync OpenClaw settings to GitHub, (3) preserve automation scripts and personal configuration, (4) create remote backup of AGENTS.md, SOUL.md, MEMORY.md, and other workspace files. Configurable for any GitHub repository.
---

# Self Backup

Backup critical OpenClaw workspace files to your GitHub repository for safe keeping and version control.

## Setup

### 1. Install GitHub CLI (if not already installed)
```bash
# Ubuntu/Debian
sudo apt install gh

# macOS
brew install gh

# Other platforms: https://cli.github.com/
```

### 2. Login to GitHub
```bash
gh auth login
```

### 3. Configure your backup repository
Edit the configuration in the backup script or set environment variables:

```bash
# Set your repository URL (replace with your repo)
export BACKUP_REPO_URL="https://github.com/YOUR_USERNAME/YOUR_BACKUP_REPO.git"

# Or edit the script directly
nano scripts/backup.sh
```

### 4. Create your backup repository
```bash
# Create a private repository for your backups
gh repo create YOUR_USERNAME/openclaw-backup --private --description "OpenClaw workspace backup"
```

## What Gets Backed Up

### Core Configuration Files
- `AGENTS.md` - Workflow documentation and procedures
- `SOUL.md` - Personal assistant personality and behavior
- `USER.md` - Personal profile and preferences  
- `MEMORY.md` - Long-term memory and important context
- `IDENTITY.md` - Assistant identity and emoji
- `TOOLS.md` - Tool configuration and local notes
- `AUTOMATION.md` - Cron and scheduling documentation
- `openclaw.json` - OpenClaw system settings (tokens sanitized for security)

### Scripts & Automation
- `scripts/` directory - All automation scripts
- `memory/` directory - Daily memory logs (last 30 days)
- Custom configuration files

### Skills Configuration
- `skills/` directory - Local skill installations (metadata only)
- Skill customizations

## Repository Structure

Files are organized in the backup repository as:
```
/
├── config/           # Core configuration files
├── scripts/          # Automation scripts  
├── memory/          # Daily memory logs
├── skills/          # Skill configurations
└── backup-info.md   # Backup metadata
```

## Usage

### First-time setup:
```bash
scripts/setup.sh
```

### Regular backups:
```bash
scripts/backup.sh
```

### Options:
```bash
scripts/backup.sh --force      # Force push even with conflicts
scripts/backup.sh --dry-run    # Show what would be backed up
```

## Security Features

- **Automatic token sanitization**: All sensitive tokens (Discord, Telegram, API keys) are automatically redacted
- **Private repository recommended**: Keep your configuration private
- **Structure preservation**: All settings preserved, only sensitive data redacted
- **Safe restore**: Easy to restore and re-enter tokens

## Configuration

Edit these variables in `scripts/backup.sh`:

```bash
# Your GitHub repository URL
REPO_URL="https://github.com/YOUR_USERNAME/YOUR_BACKUP_REPO.git"

# Workspace directory (usually auto-detected)
WORKSPACE_DIR="$HOME/.openclaw/workspace"
```

## Manual Backup

To backup specific files manually:
```bash
# Clone your backup repository
git clone https://github.com/YOUR_USERNAME/YOUR_BACKUP_REPO.git /tmp/backup
cd /tmp/backup

# Copy important files
cp ~/.openclaw/workspace/AGENTS.md config/
cp ~/.openclaw/workspace/SOUL.md config/
# ... etc

# Commit and push
git add .
git commit -m "Manual backup $(date)"
git push origin main
```

## Restore Process

To restore from backup:
```bash
# Clone the backup
git clone https://github.com/YOUR_USERNAME/YOUR_BACKUP_REPO.git

# Copy files back to workspace
cp backup/config/* ~/.openclaw/workspace/
cp -r backup/scripts/* ~/.openclaw/workspace/scripts/
# ... etc

# Re-enter your actual tokens in openclaw.json
nano ~/.openclaw/openclaw.json
```

## Troubleshooting

### GitHub Authentication Issues
```bash
# Re-login to GitHub
gh auth logout
gh auth login
```

### Permission Denied
```bash
# Check repository exists and you have access
gh repo view YOUR_USERNAME/YOUR_BACKUP_REPO
```

### Git Configuration
```bash
# Set git identity if needed
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```