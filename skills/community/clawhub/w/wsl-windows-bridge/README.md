# wsl-windows-bridge

WSL ↔ Windows cross-system bridge for OpenClaw agents.

## What This Does

Provides six commands (`win-python`, `win-ps`, `win-cmd`, `win-copy`, `win-run-py`, `win-path`) that let OpenClaw agents running in WSL2 seamlessly call Windows Python, execute PowerShell/CMD commands, and read/write Windows files.

## Architecture

```
User downloads skill
        ↓
Run setup.sh (auto-detects Windows Python location)
        ↓
~/.openclaw/bin/win-*    ← executables
~/.openclaw/env.windows.sh ← environment config
        ↓
Agent calls: source ~/.bashrc && source ~/.openclaw/env.windows.sh && win-python ...
```

## File Structure

```
~/.openclaw/workspace/skillpublish/wsl-windows-bridge/
├── SKILL.md           ← OpenClaw skill entry point
├── _meta.json         ← ClaHub metadata
├── README.md          ← This file
└── scripts/
    ├── setup.sh        ← Auto-install (auto-detects Python path)
    ├── env.windows.sh ← Template (setup.sh generates actual config)
    ├── win-python
    ├── win-ps
    ├── win-cmd
    ├── win-copy
    ├── win-run-py
    └── win-path
```

## Key Design Decisions

### 1. Non-interactive bash compatibility

exec in OpenClaw uses non-interactive bash which doesn't auto-source `.bashrc`. Solution: each wrapper starts with:

```bash
if [ -z "$BASH_ENV" ] && [ -f "$HOME/.bashrc" ]; then
    source "$HOME/.bashrc" 2>/dev/null
fi
```

### 2. Dynamic path resolution

Hardcoding `/home/username` breaks when others use it. Solution: `setup.sh` auto-detects Python location across `/mnt/d`, `/mnt/c`, `/mnt/e` and generates config with the user's actual `$HOME`.

### 3. Windows Python path not fixed

Different users install Anaconda in different drives/locations. Solution: `setup.sh` scans common mount points to find `python.exe`.

## Publishing to ClaHub

```bash
clawhub login --token <your-token>
clawhub publish ~/.openclaw/workspace/skillpublish/wsl-windows-bridge \
    --slug wsl-windows-bridge \
    --name "WSL Windows Bridge" \
    --version 0.1.0
```

## Maintenance

- **Author**: @DEACONHAN
- **Version**: 0.1.0 (draft)
