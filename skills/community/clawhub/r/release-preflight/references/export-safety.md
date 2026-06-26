# export safety

## Default private-path patterns
- `memory/`
- `logs/audit/`
- `<openclaw-local-dir>/`
- `.venv`
- `.venv-`
- `tmp/`
- `.DS_Store`

## Default text file extensions to scan
- `.md`
- `.txt`
- `.json`
- `.yml`
- `.yaml`
- `.sh`
- `.py`
- `.js`
- `.ts`

## Identity leakage hints
Flag text content that contains:
- absolute user-home paths such as `<user-home>/...`
- private system paths such as `<system-private>/...`
- local workspace paths
- host-specific names that look personal or machine-local
