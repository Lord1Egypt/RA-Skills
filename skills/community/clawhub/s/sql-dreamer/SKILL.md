# openclaw-sql-dreamer — SKILL.md

> OpenClaw skill: SQL-backed memory corpus feeder and dream output archiver.

## What This Skill Does

OpenClaw's native dreamer reads `memory/YYYY-MM-DD.md` files — raw session logs containing noise, errors, and real insights all mixed together. This skill:

1. **Pre-dream feed** — queries SQL for high-importance memories, writes a clean daily file
2. **Post-dream archiver** — stores dream outputs (light/REM/deep) to SQL tables durably
3. **File cleanup** — prunes dream output files older than N days

The OpenClaw dreamer runs unchanged. This skill wraps around it.

## Installation

```bash
git clone https://github.com/High-Falootin/openclaw-SQL-dreamer.git
cd openclaw-SQL-dreamer
pip install -r requirements.txt
cp config/example.yml config/config.yml
# Edit config/config.yml
python sql/migrate.py
```

## Configuration Reference

All settings live in `config/config.yml` (never committed — see `.gitignore`).

| Field | Type | Default | Description |
|---|---|---|---|
| `sql.server` | string | — | SQL Server hostname |
| `sql.database` | string | — | Database name |
| `sql.username` | string | — | SQL username |
| `sql.password` | string | — | Via env `SQL_PASSWORD` |
| `corpus.importance_threshold` | int | 7 | Min importance (1-10) for dream corpus |
| `corpus.lookback_days` | int | 2 | Days back to pull memories |
| `dreaming.workspace_dir` | string | — | OpenClaw workspace root |
| `dreaming.archive_after_days` | int | 7 | Days before dream files are pruned |
| `confluence.enabled` | bool | false | Enable Confluence publishing |

## Scripts

| Script | When | What |
|---|---|---|
| `scripts/pre_dream_sql_feed.py` | 3:00 AM (before dream) | Queries SQL, writes clean memory file |
| `scripts/post_dream_archiver.py` | 4:00 AM (after dream) | Archives dream outputs to SQL, prunes old files |
| `scripts/confluence_dream_publisher.py` | 4:30 AM (optional) | Pushes wiki syntheses to Confluence |

## SQL Tables Created

Run `python sql/migrate.py` to create:

- `dreams.DreamCorpus` — memories queued for each cycle
- `dreams.DreamLight` — light sleep candidates
- `dreams.DreamREM` — REM themes and reflections
- `dreams.DreamDeep` — deep sleep promotions

## Crontab Example

```cron
# Pre-dream SQL feed (30 min before your OpenClaw dream cron)
0 7 * * * python /path/to/scripts/pre_dream_sql_feed.py

# Post-dream archiver (1 hour after dream cycle)
0 8 * * * python /path/to/scripts/post_dream_archiver.py

# Confluence publisher (optional)
30 8 * * * python /path/to/scripts/confluence_dream_publisher.py
```

## Security

This is a public repo. **Never commit:**
- `.env` files
- `config/config.yml`
- Passwords, tokens, API keys

Use environment variables for all secrets:
```bash
export SQL_PASSWORD="..."
export CONFLUENCE_API_TOKEN="..."
```

## Updated Crontab (after HFTC-28)

```cron
# Pre-dream SQL feed (30 min before dream cycle)
0 7 * * * python /path/to/scripts/pre_dream_sql_feed.py

# Post-dream archiver + phase signal reconciler (1 hr after dream)
0 8 * * * python /path/to/scripts/post_dream_archiver.py
5 8 * * * python /path/to/scripts/phase_signal_reconciler.py

# Confluence publisher (optional, 90 min after dream)
30 8 * * * python /path/to/scripts/confluence_dream_publisher.py
```
