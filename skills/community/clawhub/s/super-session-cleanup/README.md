# session-cleanup

> Session cleanup skill for Claw-family agents (OpenClaw, WorkBuddy, QClaw, etc.)

Track and clean up all artifacts produced during an agent session: temporary files, installed packages, skills, and other transient resources.

## Features

- **Session Tracking** — Automatically record temp files, pip/npm packages, system software, and skills created during a conversation
- **Smart Cleanup** — Trash-first deletion with OS-specific implementations (Windows Recycle Bin, macOS Trash, Linux gio/trash-put)
- **Safety First** — Forbidden root protection, workspace source code preservation, dry-run preview mode
- **Skip List** — Mark items to preserve with partial matching support
- **Pre-check** — pip/npm uninstall skips packages that aren't actually installed
- **Cross-platform** — Windows, macOS, and Linux support

## Installation

Copy the `session-cleanup` folder to your WorkBuddy skills directory:

```bash
# User-level (available across all projects)
cp -r session-cleanup ~/.workbuddy/skills/

# Project-level (shared among team members)
cp -r session-cleanup .workbuddy/skills/
```

## Usage

### As a Skill (recommended)

Activate tracking at session start, then clean up when done:

| Command | Action |
|---|---|
| `开启清理追踪` / `session cleanup start` | Start tracking session artifacts |
| `清理垃圾文件` / `cleanup now` | Clean up all tracked items |
| `列出临时文件` / `show session log` | Show current tracked list |
| `跳过 <name>` / `skip <name>` | Mark an item for preservation |
| `清除记录` / `clear log` | Delete tracking file (no actual files) |

### As a CLI tool

```bash
# Initialize tracking
python scripts/cleanup.py --init /path/to/workspace

# Add items
python scripts/cleanup.py --add temp_files "/tmp/demo.py" --track-file /path/to/session-track.json
python scripts/cleanup.py --add pip_packages "requests" --track-file /path/to/session-track.json

# Preview cleanup
python scripts/cleanup.py --track-file /path/to/session-track.json --dry-run

# Execute cleanup
python scripts/cleanup.py --track-file /path/to/session-track.json

# Direct path deletion
python scripts/cleanup.py --paths "/tmp/a.py" "/tmp/b.txt" --dry-run

# From manifest JSON
python scripts/cleanup.py --manifest manifest.json --workspace /path/to/workspace
```

## File Structure

```
session-cleanup/
├── SKILL.md                    # Skill definition & workflow instructions
├── README.md                   # This file
├── LICENSE                     # MIT License
├── scripts/
│   ├── cleanup.py              # CLI cleanup utility
│   ├── test_regression.py      # Regression test suite (33 tests)
│   ├── test_full_functional.py # Full functional test suite (57 tests)
│   └── test_simulated_session.py # Simulated session lifecycle test (43 tests)
├── references/
│   └── cleanup-guide.md        # Uninstall command reference by OS/package manager
└── assets/                     # (reserved for future assets)
```

## Safety Rules

1. Never auto-delete files outside temp/scratch/generated paths without confirmation
2. Never delete workspace source code, project configuration, or `.workbuddy/` directory
3. Never use `rm -rf` or `del /S /Q` on home, desktop, downloads, or project roots
4. Skills deletion is permanent — always warn before removing
5. Max 10 file deletions per batch, verify after each batch

## Changelog

See [SKILL.md](SKILL.md#changelog) for full version history.

## License

MIT — see [LICENSE](LICENSE) for details.
