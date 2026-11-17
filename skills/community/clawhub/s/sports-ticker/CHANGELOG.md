# Changelog

## [3.3.0] - 2026-08-31

### Changed
- Docs now describe OpenClaw 2.0 automation setup: primary command `openclaw automations` (the old `openclaw cron` remains as an alias), wake flag `--wake` (no `--wake-mode` flag).
- Added note: exec in automations requires an approval grant in 2.0; without a grant the automation fails silently. Approvals run through the Control UI.
- `auto_setup_crons.py`: `--commands` help text now says what the flag does (JSON plus agent instructions), and the JSON output tells the agent to create automations instead of referring to the removed "cron tool".
- Removed `package.json`. It declared an npm package that was never published and had no `main`, dependencies, or scripts. ClawHub CLI 0.22+ refuses to publish any folder containing a `package.json` as a skill.

### Fixed
- Corrected the 3.0.5 entry below: `--commands` was never removed from `auto_setup_crons.py`. It still exists and outputs JSON.

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
- Raw CLI command output from `auto_setup_crons.py`. The `--commands` flag itself stayed and now emits JSON. (An earlier version of this entry claimed the flag was removed; it was not.)

### Migration
If you were parsing CLI command output from these scripts, update to parse JSON instead. The JSON format includes full cron specifications ready for the OpenClaw cron API.

## [3.0.3] - 2026-02-04

- Privacy cleanup: removed hardcoded paths and personal info from docs
