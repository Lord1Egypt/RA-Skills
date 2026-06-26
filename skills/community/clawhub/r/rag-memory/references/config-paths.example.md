# Config Paths Reference (Example)

This file documents where configuration, credentials, and runtime state live.
Copy to `config-paths.md` and fill in your actual values.

## Skill folder (source of truth)

| File | Purpose |
|---|---|
| `~/.openclaw/skills/rag-memory/config.env` | All credentials and tuning for sync script (gitignored) |
| `~/.openclaw/skills/rag-memory/sync_to_qdrant.py` | Main sync script |
| `~/.openclaw/skills/rag-memory/venv/` | Python virtualenv |
| `~/.openclaw/skills/rag-memory/plugin/` | OpenClaw plugin source |
| `~/.openclaw/skills/rag-memory/systemd/` | Systemd unit source copies — edit here, then `sudo cp` to deploy |

## OpenClaw runtime

| File | Purpose |
|---|---|
| `~/.openclaw/openclaw.json` | Main config — plugin entry under `plugins.entries.rag-memory` |
| `~/.openclaw/extensions/rag-memory/` | Installed plugin (managed by `openclaw plugins install`) |
| `~/.openclaw/workspace/memory/` | Memory .md files (MEMORY.md, daily logs, TOOLS.md) |

## Systemd (deployed copies)

| File | Purpose |
|---|---|
| `/etc/systemd/system/sysclaw-rag-sync.service` | Full sync service |
| `/etc/systemd/system/sysclaw-rag-sync.timer` | Nightly trigger (03:00) |
| `/etc/systemd/system/sysclaw-rag-watch.path` | Watches memory dir for .md changes |
| `/etc/systemd/system/sysclaw-rag-watch.service` | Incremental sync on file change |

## Qdrant

Collections are hosted at `https://qdrant.example.com` (set `QDRANT_HOST` in config.env).

- `{QDRANT_COLLECTION_PREFIX}_memory` — daily logs + long-term facts
- `{QDRANT_COLLECTION_PREFIX}_docs` — tools + skill docs

## Database

| Database | Purpose |
|---|---|
| `your_db_name` @ `host:5432` | `memory_entries`, `daily_logs`, `tools`, `qdrant_sync_log` |

## Credential locations (for key rotation)

| Credential | Where it lives |
|---|---|
| `QDRANT_COLLECTION_PREFIX` | `config.env` + `openclaw.json` plugin config — must match |
| `EMBED_API_KEY` | `config.env` + `openclaw.json` plugin config — must match |
| `QDRANT_API_KEY` | `config.env` + `openclaw.json` plugin config — must match |
| `POSTGRES_DSN` | `config.env` only |
| `score_threshold` | `config.env` (reference) + `openclaw.json` plugin config — keep in sync manually |
