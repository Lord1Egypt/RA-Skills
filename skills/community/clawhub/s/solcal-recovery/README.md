# SolCal Recovery — Complete OpenClaw Repair Toolkit

A beginner-friendly toolkit to get Sol (or any OpenClaw AI) back online when things go wrong. Includes AI-powered repair assistance using Ollama.

## What's Included

| Script | What It Does |
|--------|------------|
| `SolCal-Recovery.sh` | Main diagnostic + AI repair |
| `start-sol.sh` | Quick start Sol |
| `save-sol.sh` | Backup all Sol data |
| `restore-sol.sh` | Restore from backup |
| `emergency-repair.sh` | Nuclear option - reset everything |
| `ai-repair.sh` | Ask AI for help with your issue |

## Quick Start

```bash
cd SolCal-Recovery

# Make scripts executable
chmod +x *.sh

# Run diagnostics
bash SolCal-Recovery.sh

# Or just start Sol
bash start-sol.sh
```

## Detailed Guide

### Prerequisites

1. **OpenClaw installed**
   ```bash
   brew install openclaw
   ```

2. **Ollama (optional, for AI repair)**
   ```bash
   curl -fsSL https://ollama.ai/install | sh
   ```

---

## Script Commands

### 1. Run Full Diagnostic
```bash
bash SolCal-Recovery.sh
```

Checks:
- OpenClaw installed?
- Gateway running?
- Gateway connected?
- API keys configured?
- Network working?

### 2. Start Sol
```bash
bash start-sol.sh
```

Starts the gateway if not running. Reports status.

### 3. Save Sol State
```bash
bash save-sol.sh
```

Backs up to `~/SolCal-Backups/YYYYMMDD_HHMMSS/`:
- Config (`openclaw.json`)
- Sessions
- Skills
- GitHub token

### 4. Restore Sol State
```bash
bash restore-sol.sh ~/SolCal-Backups/20260403_120000
```

Restores from a backup folder.

### 5. Emergency Repair
```bash
bash emergency-repair.sh
```

 Nuclear option:
1. Stops gateway
2. Clears logs  
3. Checks/reinstalls OpenClaw
4. Starts fresh
5. Verifies working

### 6. AI Repair Assistant
```bash
bash ai-repair.sh "Sol won't respond"
```

Uses local Ollama (llama3.2:1b) to diagnose and suggest fixes.

---

## Common Issues & Fixes

### Sol Won't Start
```bash
bash SolCal-Recovery.sh diagnose
# OR
bash emergency-repair.sh
```

### API Key Not Working
```bash
# Edit config
open ~/.openclaw/openclaw.json

# Check auth section has your key
"auth": {
  "profiles": {
    "minimax": {
      "api_key": "YOUR_KEY_HERE"
    }
  }
}
```

### Gateway Not Responding
```bash
# Check if running
openclaw gateway status

# Restart
openclaw gateway restart

# Or force restart
pkill -f openclaw
openclaw gateway start
```

### Network Blocked
```bash
# Check network
curl https://api.minimax.io

# Check firewall
sudo pfctl -d  # Temporarily disable
```

---

## The AI Repair Feature

The toolkit uses Ollama with a small model (llama3.2:1b) to:
1. Read your system status
2. Understand your issue
3. Suggest specific commands

It runs completely offline after downloading the model.

### Setup AI Repair
```bash
# First time setup
bash SolCal-Recovery.sh ollama

# Then use
bash ai-repair.sh "your issue here"
```

---

## Workflow When Sol Goes Offline

1. **Quick Check**
   ```bash
   bash start-sol.sh
   ```

2. **If Not Working - Diagnose**
   ```bash
   bash SolCal-Recovery.sh
   ```

3. **Auto-Repair**
   ```bash
   bash SolCal-Recovery.sh repair
   ```

4. **Still Broken - Emergency**
   ```bash
   bash emergency-repair.sh
   ```

5. **Need AI Help**
   ```bash
   bash ai-repair.sh "describe the problem"
   ```

---

## File Structure

```
SolCal-Recovery/
├── SolCal-Recovery.sh    # Main diagnostic
├── start-sol.sh        # Quick start
├── save-sol.sh         # Backup
├── restore-sol.sh      # Restore
├── emergency-repair.sh # Nuclear reset
├── ai-repair.sh      # AI assistant
└── README.md        # This file
```

---

## Tips

- Run diagnostics regularly to catch issues early
- Run `save-sol.sh` weekly
- Keep the `~/SolCal-Backups/` folder backed up somewhere safe
- The AI repair needs ~2GB for the model

## Troubleshooting

### "Command not found: openclaw"
```bash
brew install openclaw
```

### "Gateway timeout"
```bash
openclaw gateway stop
openclaw gateway start
```

### "API key invalid"
```bash
open ~/.openclaw/openclaw.json
# Edit and save new key
```

---

*Build for Sol by Sol. Get back online quickly.*