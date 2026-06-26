# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Quicker Connector** is an OpenClaw skill that bridges OpenClaw (AI automation gateway) with [Quicker](https://getquicker.net/), a Windows automation tool. It allows users to list, search, match (via AI), and execute Quicker actions from natural language input. Windows-only — requires `QuickerStarter.exe`.

## Commands

```bash
# Initialize (interactive setup to configure CSV path)
python scripts/init_quicker.py

# Run the main skill entry point
python scripts/quicker_skill.py

# Run full test suite
python tests/test_quicker_connector.py

# Run simpler integration test
python tests/test_quicker.py

# Verify optimization
python verify_optimization.py
```

There is no build step — this is a pure Python project with no dependencies beyond the standard library (csv, sqlite3, subprocess, json, re, os).

## Architecture

All business logic lives in `scripts/quicker_connector.py` (~1015 lines). The entry point `scripts/quicker_skill.py` parses user input and calls into the connector.

**Core classes:**

- `CSVActionReader` — reads Quicker CSV exports, handles UTF-8/GBK encoding detection, caches results
- `DatabaseActionReader` — reads Quicker's SQLite DB (`quicker.db`) as an alternative data source; auto-detects schema
- `ActionMatcher` — keyword extraction + category mapping (Chinese↔English) + relevance scoring (0–1 scale); returns top-N `MatchResult` objects
- `QuickerActionRunner` — executes actions via `QuickerStarter.exe` using `quicker:runaction:{id}?parameters` URIs; supports sync (with timeout) and async modes
- `QuickerConnector` — façade combining all components; manages `config.json`; lazy-loads runner only when execution is needed
- `EncodingDetector` — detects CSV file encoding by trying UTF-8-sig → UTF-8 → GBK → GB2312 → GB18030 → Latin-1

**Data classes:** `QuickerAction`, `MatchResult`, `QuickerActionResult`

**Data flow:**
```
User input → quicker_skill.py → QuickerConnector
  → CSVActionReader or DatabaseActionReader  (load actions)
  → ActionMatcher                            (find best match)
  → QuickerActionRunner                      (execute if requested)
```

## Configuration

Runtime config is stored in `config.json` (gitignored, user-generated). Key fields:
- `csv_path` — path to Quicker CSV export
- `db_path` — path to Quicker SQLite database
- `initialized` — boolean flag

Skill manifest (capabilities, triggers, permissions, settings) is defined in `skill.json` and `skill_optimized.json`. The optimized version is the current production manifest (v1.2.0).

## Key Design Decisions

- **Dual data source**: CSV and DB readers share the same interface; CSV is preferred, DB is fallback
- `auto_select_threshold` (default 0.8) — if top match score ≥ this value, auto-execute without confirmation
- Permissions declared in `skill_optimized.json` restrict subprocess execution to `QuickerStarter.exe` paths and disable network access
