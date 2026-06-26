# Changelog

## [3.2.0] - 2026-03-27

### Changed
- v3.2.0 — Phase 1 stability: removed hardcoded API key, added web search fallback for non-ESPN teams, added score caching
- **ticker.py:** Removed hardcoded Brave API key fallback — now uses env var only; if key absent, skips Brave and tries Serper directly
- **live_monitor.py:** Teams without `espn_id` are no longer skipped — they are checked via web search (Brave/Serper) with change-detection against cache
- **cache.py (new):** Score cache module — reads/writes `.score_cache.json`; stores last_result, match_date, source, cached_at per team
- **ticker.py + live_monitor.py:** Write to cache on result found; show cached "Last result: … (DD.MM.)" when no live data and no API key

## [3.0.7] - 2026-03-03

### Fixed
- `find_team_match()` now filters by today's UTC date (`today_only=True` default) — prevents matches from future weeks from being reported as "today"

## [3.0.6] - 2026-03-03

### Changed
- Added ESPN endpoint validation and synchronized security/docs updates.


## [3.0.5] - 2026-02-11

### Changed
- **setup_crons.py:** No longer uses `subprocess.run` — outputs JSON configurations instead of executing commands directly
- **auto_setup_crons.py:** Outputs JSON configs instead of CLI command strings
- **Agent-Native Pattern:** Scripts now output structured JSON that the agent processes via the OpenClaw cron tool. This is safer and more aligned with OpenClaw's architecture.

### Removed
- `--commands` flag from auto_setup_crons.py (was outputting raw CLI commands)

### Migration
If you were parsing CLI command output from these scripts, update to parse JSON instead. The JSON format includes full cron specifications ready for the OpenClaw cron API.

## [3.0.3] - 2026-02-04

- Privacy cleanup: removed hardcoded paths and personal info from docs
