# Safe Data Path Guidelines for Skills

## Core Principle

Skill directories are **completely overwritten** on every update / reinstall.
Any data written *inside* the skill dir will be lost.

## Recommended Paths

Put persistent data in `.skill-data/<skill-name>/` under a base dir that
matches the runtime environment and is outside the skill dir:

| Data type | Sub-path |
|-----------|----------|
| User config | `.skill-data/<skill-name>/config.json` |
| Cache | `.skill-data/<skill-name>/cache/` |
| Token / credentials | `.skill-data/<skill-name>/credentials.json` |
| Logs | `.skill-data/<skill-name>/logs/` |
| Runtime state | `.skill-data/<skill-name>/state.json` |

The base dir is auto-detected in this order (first existing wins):

1. `$CLAWHUB_WORKDIR` (if set)
2. `$OPENCLAW_WORKSPACE` (if set)
3. `~/.openclaw/workspace`
4. `~/.local/share` (XDG-ish fallback, exists on most Linux/macOS)
5. `~` (home dir, always present)

## Python Example

```python
import os
from pathlib import Path

SKILL_NAME = "my-skill"
base = (
    os.environ.get("CLAWHUB_WORKDIR")
    or os.environ.get("OPENCLAW_WORKSPACE")
    or str(Path.home())
)
DATA_DIR = Path(base).expanduser() / ".skill-data" / SKILL_NAME
DATA_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_FILE = DATA_DIR / "config.json"
```

## Detection Rules

`check_data_safety.py` flags these risky patterns:

1. `__file__` used to construct write paths (data written inside the skill package)
2. Relative paths like `./config/`, `./cache/` (resolved against the skill dir)
3. Pre-existing `.json` / `.yaml` / `.cfg` / `.token` files inside the skill dir

## Allowed Inside the Skill Dir

- `SKILL.md` (required)
- `README.md` (recommended)
- `LICENSE` (required for some targets)
- `references/*.md` (reference docs)
- `assets/*` (static resources)
- `scripts/*.py` / `scripts/*.sh` (executable scripts)
- `package.json` / `requirements.txt` (read-only dependency manifests)
- `profiles/*.json` (read-only configuration profiles)
