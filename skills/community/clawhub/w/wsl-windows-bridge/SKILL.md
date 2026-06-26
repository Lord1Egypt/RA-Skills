---
name: wsl-windows-bridge
description: 'WSL ↔ Windows cross-system bridge for OpenClaw agents. Provides win-python / win-ps / win-cmd / win-copy / win-run-py / win-path to invoke Windows Python (Anaconda), execute PowerShell/CMD commands, and read/write Windows files from WSL2. Ideal for quantitative trading (QMT/xtquant), cross-system file operations, and Windows environment scripting.'
license: MIT
compatibility: 'WSL2 + Windows 10/11, Windows Python (Anaconda or any), PowerShell'
metadata:
  openclaw:
    emoji: 🪟
    requires:
      bins: ["bash", "wslpath", "powershell.exe", "cmd.exe"]
      env: []
    primaryEnv: null
---

# WSL ↔ Windows Cross-System Bridge

> Seamless access to Windows Python, PowerShell, CMD, and filesystem from WSL2.

## Features

| Command | Purpose |
|---------|---------|
| `win-python` | Invoke Windows Python (Anaconda or any) |
| `win-ps` | Execute PowerShell commands |
| `win-cmd` | Execute CMD commands |
| `win-copy` | Copy files between WSL and Windows |
| `win-run-py` | Run .py scripts with logging |
| `win-path` | Convert paths WSL `/mnt/*` ↔ Windows `D:\*` |

## Requirements

- WSL2 (Ubuntu 20.04+)
- Windows 10 or Windows 11
- Windows Python (Anaconda recommended)
- PowerShell

## First-Time Setup

```bash
cd ~/.openclaw/workspace/skillpublish/wsl-windows-bridge/scripts/
bash setup.sh
```

The setup script will:
1. Auto-detect your Windows Python location (supports `/mnt/d`, `/mnt/c`, `/mnt/e`)
2. Copy all wrappers to `~/.openclaw/bin/`
3. Generate `~/.openclaw/env.windows.sh` with correct paths
4. Set permissions and run verification

**Manual setup (without setup.sh):**
```bash
cp -r scripts/* ~/.openclaw/bin/
chmod +x ~/.openclaw/bin/win-*
# Then manually edit env.windows.sh to set correct paths
```

## Quick Start

### Basic Usage

**⚠️ exec non-interactive shell note:**
```bash
# Recommended for exec environment
source ~/.bashrc && source ~/.openclaw/env.windows.sh && win-python ...

# Or directly (wrappers handle .bashrc internally)
~/.openclaw/bin/win-python ...
```

### Common Scenarios

**Invoke Windows Python to run a script:**
```bash
source ~/.bashrc && source ~/.openclaw/env.windows.sh

# Single-line command
win-python -c "import xtquant; print(xtquant.__version__)"

# Run a script file
win-python "$WIN_SCRIPTS/my_task.py" --arg value
```

**Execute PowerShell:**
```bash
win-ps "Get-Process python | Select-Object Name,Id | Format-Table"
win-ps "Get-Service | Where-Object {\$_.DisplayName -like '*QMT*'}"
```

**File copy:**
```bash
win-copy /tmp/result.csv /mnt/d/app/output/result.csv
```

**Path conversion:**
```bash
win-path /mnt/d/app
# → D:\app

win-path --to-wsl D:\app
# → /mnt/d/app
```

### Quantitative Trading Example (QMT/xtquant)

```bash
source ~/.bashrc && source ~/.openclaw/env.windows.sh

# Get HS300 constituent stocks
win-python -c "
from xtquant import xtdata
stocks = xtdata.get_stock_list_in_sector('沪深300')
print(f'HS300: {len(stocks)} stocks')
print(stocks[:5])
"

# Download historical data
win-python -c "
from xtquant import xtdata
xtdata.download_history_data('600000.SH', start_time='20260101', end_time='20260405')
print('Download complete')
"
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WIN_ROOT` | `/mnt/d` | Windows root directory |
| `WIN_ANACONDA` | `/mnt/d/app/anaconda` | Anaconda installation path |
| `WIN_PYTHON` | `$WIN_ANACONDA/python.exe` | Python executable |
| `WIN_PS` | `.../powershell.exe` | PowerShell path |
| `WIN_SCRIPTS` | `/mnt/d/app/scripts` | Common scripts directory |

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `command not found: win-python` | env.windows.sh not sourced | `source ~/.bashrc && source ~/.openclaw/env.windows.sh` |
| `Permission denied` | UAC permission | Use `D:\app\` or user directory as target |
| Chinese garbled logs | QMT log encoding | Ignore; actual data is correct |

## File Structure

```
~/.openclaw/workspace/skillpublish/wsl-windows-bridge/
├── SKILL.md
├── _meta.json
├── README.md
└── scripts/
    ├── setup.sh          ← Auto-install (auto-detects Python path)
    ├── env.windows.sh   ← Template (setup.sh generates actual config)
    ├── win-python
    ├── win-ps
    ├── win-cmd
    ├── win-copy
    ├── win-run-py
    └── win-path
```

## Maintenance

- **Author**: @DEACONHAN
- **Version**: 0.1.0 (draft)
- **Issues**: https://github.com/jarvis-agent/wsl-windows-bridge/issues
