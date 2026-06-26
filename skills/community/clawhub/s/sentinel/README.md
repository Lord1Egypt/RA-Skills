# Sentinel — AI Agent State Guardian

**Automated backup, integrity monitoring, and self-healing for AI agent workspaces.**

Sentinel continuously monitors your critical files, detects unexpected changes, creates automatic backups, and can self-heal from corruption. Built for AI agents that can't afford to lose state, memory, or configuration data.

---

## The Problem

AI agents maintain critical state in files: memory logs, configuration, user profiles, conversation history. When these files get corrupted, accidentally deleted, or unexpectedly modified:

- **Memory loss** — Your agent forgets important context
- **Broken behavior** — Config corruption leads to unpredictable actions
- **No rollback** — Once a file is overwritten, it's gone forever
- **Silent failures** — You don't know something broke until it's too late

Manual backups don't work. You forget to run them. Automated backups without integrity checking just back up corruption.

## What Sentinel Does

### 1. **Continuous Monitoring** (`sentinel.py`)
- Tracks critical files you specify (exact paths or glob patterns)
- Computes SHA-256 hashes for change detection
- Detects corruption (empty files, unexpected modifications)
- Skips files currently in use by running processes
- Runs on a configurable schedule (default: every 10 minutes)

### 2. **Automatic Backups**
- Creates timestamped backups when files change
- Preserves directory structure in backup directory
- Keeps configurable number of versions per file
- Never deletes files — moves them to backup instead

### 3. **Self-Healing**
- Detects file corruption (empty files, hash mismatches)
- Automatically restores from last known good backup
- Logs all restoration events for audit trail
- Configurable auto-restore policy (can be disabled)

### 4. **Restoration Tools** (`sentinel_restore.py`)
- Interactive backup selection with preview
- Restore latest backup with one command
- Restore from specific timestamp
- Safety backups before restoration
- Verification before restore (checks for empty backups)

### 5. **Workspace Manifests** (`sentinel_manifest.py`)
- Generate complete workspace snapshots
- Full file inventory with hashes, sizes, timestamps
- Compare manifests to detect changes
- Diff reports (added, deleted, modified files)
- Export to JSON for version control

---

## Quick Start

```bash
# 1. Configure Sentinel
cp config_example.py sentinel_config.py
# Edit sentinel_config.py with your workspace path and critical files

# 2. Run once to test
python3 sentinel.py --once

# 3. Run continuous monitoring
python3 sentinel.py --continuous

# 4. Check status
python3 sentinel.py --status

# 5. Restore a file if needed
python3 sentinel_restore.py --file memory/2026-02-21.md --latest

# 6. Generate workspace manifest
python3 sentinel_manifest.py --output workspace_manifest.json
```

---

## Design Philosophy

### Safety Over Speed
Sentinel prioritizes data integrity over performance. It will skip files that are in use rather than risk corrupting them during backup.

### Zero Data Loss
Sentinel never deletes files. Ever. Files are moved to backups, not removed. Even if a file appears to be a duplicate or garbage, it's preserved until you explicitly delete it.

### Change Detection, Not Paranoia
Sentinel tracks file changes and alerts you, but doesn't assume every change is malicious. Changed files are backed up; you decide if the change was intentional.

### Self-Healing When Safe
Auto-restore only triggers for clear corruption cases (empty files, missing files). Unexpected modifications are flagged but not auto-restored unless you configure it.

### No External Dependencies
Pure Python stdlib. No pip installs, no version conflicts, no supply chain risk.

---

## Use Cases

### For AI Agent Users
- **Memory protection** — Prevent loss of conversation history and learned context
- **Config safety** — Roll back broken configuration changes
- **State recovery** — Restore agent state after crashes or corruption
- **Change auditing** — Track what changed and when across your workspace

### For AI Agent Developers
- **Development safety net** — Experiment freely, restore when things break
- **Testing rollback** — Restore clean state between test runs
- **Deployment verification** — Compare production vs. development manifests
- **Incident forensics** — Reconstruct what happened before a failure

### For Multi-Agent Systems
- **Per-agent workspaces** — Isolate and protect each agent's state
- **Cross-agent comparison** — Detect divergence between agents
- **Shared file protection** — Monitor files accessed by multiple agents
- **Recovery orchestration** — Restore multiple agents to consistent state

---

## What's Included

| File | Purpose |
|------|---------|
| `sentinel.py` | Main monitoring and backup engine |
| `sentinel_restore.py` | File restoration tool with interactive selection |
| `sentinel_manifest.py` | Workspace manifest generator and comparator |
| `config_example.py` | Configuration template with all options documented |
| `LIMITATIONS.md` | What Sentinel doesn't do |
| `LICENSE` | MIT License |

---

## Configuration

See `config_example.py` for full details. Key settings:

### Critical Files
```python
CRITICAL_FILES = [
    "agent.md",          # Exact file
    "memory/*.md",       # Glob pattern
    "**/*.json",         # Recursive glob
]
```

### Backup Settings
```python
BACKUP_DIR = "/path/to/backups"
MAX_BACKUP_VERSIONS = 10  # Keep last 10 versions per file
AUTO_RESTORE_ON_CORRUPTION = True  # Self-heal empty/corrupted files
```

### Monitoring
```python
CHECK_INTERVAL_SECONDS = 600  # Check every 10 minutes
SKIP_FILES_IN_USE = True      # Don't touch locked files
```

### Alerting
```python
LOG_FILE = "/path/to/sentinel.log"
ALERT_FILE = "/path/to/sentinel_alerts.txt"
ALERT_ON_FILE_CHANGE = True
ALERT_ON_CORRUPTION = True
```

---

## Advanced Usage

### Run as Background Service

**Linux (systemd):**
```ini
[Unit]
Description=Sentinel AI Agent State Guardian

[Service]
Type=simple
ExecStart=/usr/bin/python3 /path/to/sentinel.py --continuous
Restart=always

[Install]
WantedBy=multi-user.target
```

**macOS (launchd):**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.shadowrose.sentinel</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/path/to/sentinel.py</string>
        <string>--continuous</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

### Compare Workspace States
```bash
# Generate baseline
python3 sentinel_manifest.py --output baseline.json

# Make changes to workspace...

# Compare current state to baseline
python3 sentinel_manifest.py --compare baseline.json --diff-output changes.json
```

### Restore Multiple Files
```bash
# List all backups
python3 sentinel_restore.py --list

# Restore interactively
for file in memory/*.md; do
    python3 sentinel_restore.py --file "$file" --interactive
done
```

---

## Requirements

- Python 3.8+
- No external dependencies (stdlib only)
- Works on Linux, macOS, Windows
- ~50KB disk space for code
- Backup storage depends on your workspace size

---

## License

MIT — See `LICENSE` file.


---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**SECURITY DISCLAIMER:** This software provides supplementary security measures and 
is NOT a replacement for professional security auditing, penetration testing, or 
compliance frameworks. No software can guarantee complete protection against all 
threats. Users operating in regulated industries (healthcare, finance, legal) should 
consult qualified security professionals and verify compliance with applicable 
regulations (GDPR, HIPAA, SOC2, etc.) independently.
---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at . If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
