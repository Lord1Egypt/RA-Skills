---
name: reinstall-openclaw
description: "Safely uninstall and reinstall OpenClaw while preserving user configurations, credentials, memory files, skills, and custom settings. Includes backup and restore procedures."
metadata:
  {
    "openclaw":
      {
        "emoji": "🦞",
        "requires": { "bins": ["node", "npm", "wsl"] },
        "install": [],
      },
  }
---

# Reinstall OpenClaw Skill

This skill provides complete procedures to safely uninstall and reinstall OpenClaw while preserving all user configurations, credentials, memory files, skills, and custom settings.

## Use Cases

- Clean reinstall of OpenClaw to fix corrupted installations
- Remove third-party modifications and restore to official version
- Upgrade to latest version with fresh installation
- Migrate OpenClaw to a new environment with existing configurations

## Prerequisites

- WSL (Ubuntu 20.04 or later) or Linux/macOS with Node.js
- Node.js 18+ and npm/pnpm
- Access to WSL terminal (for Windows users)

---

## Complete Procedure

### Step 1: Check Current Installation

First, identify the OpenClaw installation location and version:

```bash
# Check OpenClaw version
npx openclaw --version

# Find OpenClaw npm package location
npm root -g

# List global npm packages
npm list -g --depth=0
```

### Step 2: Backup All User Data

Create a complete backup of all user configurations:

```bash
# Create backup directory with timestamp
BACKUP_DIR=~/openclaw-backup-$(date +%Y%m%d)
mkdir -p $BACKUP_DIR

# Backup entire .openclaw directory
cp -r ~/.openclaw $BACKUP_DIR/

# Verify backup
ls -la $BACKUP_DIR/
```

#### What to Backup (Already included in ~/.openclaw)

| Directory/File | Description |
|---------------|-------------|
| `openclaw.json` | Main configuration (gateway token, API keys, channel configs) |
| `credentials/` | API credentials and secrets |
| `memory/` | SQLite memory database |
| `agents/` | Agent configurations and sessions |
| `skills/` | Installed skills |
| `workspace/` | User workspace (SOUL.md, IDENTITY.md, AGENTS.md, etc.) |
| `feishu/` | Feishu configuration |
| `identity/` | Device identity files |
| `devices/` | Paired devices |
| `cron/` | Scheduled cron jobs |

### Step 3: Stop OpenClaw Services

Stop all running OpenClaw processes:

```bash
# Stop gateway if running
npx openclaw gateway stop

# Kill any remaining processes
pkill -f openclaw
pkill -f "node.*openclaw"

# Verify no processes running
ps aux | grep openclaw
```

### Step 4: Uninstall OpenClaw

Use the official uninstall command:

```bash
# Full uninstall (removes everything including CLI - optional)
npx openclaw uninstall --all --yes

# OR uninstall but keep CLI (recommended)
npx openclaw uninstall --state --workspace --yes
```

**Note**: The `--all` flag removes the CLI as well. If you want to keep the CLI for reinstallation, omit this flag.

### Step 5: Clean Up Remaining Files

Remove any remaining files that might interfere:

```bash
# Remove npm cache (optional but recommended)
npm cache clean --force

# Remove old OpenClaw npm package if still exists
sudo npm uninstall -g openclaw

# Remove any remaining .openclaw directories
rm -rf ~/.openclaw
rm -rf ~/.openclaw-dev
```

### Step 6: Install Latest OpenClaw

Install the latest official version:

```bash
# Install globally
sudo npm install -g openclaw@latest

# Verify installation
npx openclaw --version
```

### Step 7: Restore User Configuration

Restore your backed-up configurations:

```bash
# Restore .openclaw directory
cp -r ~/openclaw-backup-YYYYMMDD/* ~/.openclaw/

# Set correct permissions
chmod 700 ~/.openclaw
```

### Step 8: Run Health Check and Fix

```bash
# Run doctor to check for issues
npx openclaw doctor --fix
```

### Step 9: Start OpenClaw Gateway

```bash
# Start the gateway
npx openclaw gateway

# Check health
npx openclaw health

# Check status
npx openclaw status
```

---

## Complete One-Liner Backup Script

Run this before uninstalling to create a timestamped backup:

```bash
# Create automatic backup
BACKUP_DIR=~/openclaw-backup-$(date +%Y%m%d-%H%M%S) && mkdir -p $BACKUP_DIR && cp -r ~/.openclaw/* $BACKUP_DIR/ && echo "Backup created: $BACKUP_DIR"
```

---

## Complete One-Liner Restore Script

Run this after reinstallation to restore configurations:

```bash
# Restore from latest backup
LATEST_BACKUP=$(ls -td ~/openclaw-backup-* | head -1) && cp -r $LATEST_BACKUP/* ~/.openclaw/ && chmod 700 ~/.openclaw && echo "Restored from: $LATEST_BACKUP"
```

---

## Troubleshooting

### Gateway won't start after restore

```bash
# Stop any stale processes
npx openclaw gateway stop

# Force start
npx openclaw gateway --force
```

### Port already in use

```bash
# Find process using the port
lsof -i :18788

# Kill it
kill <PID>
```

### Configuration errors after restore

```bash
# Run doctor to fix
npx openclaw doctor --fix
```

### Permission issues

```bash
# Fix .openclaw permissions
chmod 700 ~/.openclaw
chmod 600 ~/.openclaw/openclaw.json
chmod 700 ~/.openclaw/credentials
```

---

## Files Reference

### Configuration File (~/.openclaw/openclaw.json)

Key settings to preserve:
- `gateway.port` - Gateway port (default: 18788)
- `gateway.auth.token` - Gateway authentication token
- `channels.feishu` - Feishu app credentials
- `models.providers` - API keys for AI models

### Backup Contents

```
~/.openclaw/
├── openclaw.json          # Main config
├── credentials/           # API secrets
├── memory/main.sqlite     # Memory database
├── agents/main/           # Agent configs
├── skills/                # Installed skills
├── workspace/             # User workspace
│   ├── SOUL.md
│   ├── IDENTITY.md
│   ├── AGENTS.md
│   └── USER.md
├── feishu/                # Feishu config
├── identity/              # Device identity
├── devices/               # Paired devices
└── cron/                  # Scheduled jobs
```

---

## Important Notes

1. **Always backup before uninstalling** - Never skip the backup step
2. **Keep backup in a safe place** - Copy to external storage or cloud
3. **Test after restore** - Verify all configurations work correctly
4. **Third-party modifications** - This procedure removes all third-party patches and returns to official version
5. **Memory files are preserved** - The SQLite memory database is included in the backup
