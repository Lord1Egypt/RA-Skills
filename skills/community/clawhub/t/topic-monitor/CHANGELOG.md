# Changelog

## [1.5.2] - 2026-03-29

### Fixed
- Removed personal chat_id from published config

## [1.5.1] - 2026-03-29

### Fixed
- **Critical: `alert_on` config was completely ignored** — topics with `alert_on: ["github_release"]` never triggered high-priority alerts because the code never read the field. GitHub releases were scored like regular web search results and often fell below the importance threshold. This was a day-1 bug present since the feature was documented.
- Now: when a result's source matches any entry in `alert_on`, it is automatically forced to HIGH priority with score 0.9, bypassing normal scoring.

## [1.5.0] - 2026-03-26

### Added
- RSS/Atom feed monitoring as first-class source alongside web search
- Feed auto-discovery from any URL
- OPML import/export support
- ETag/Last-Modified caching for efficient feed polling
- Boolean query filters: `exclude_keywords` and `required_keywords` per topic
- Sentiment analysis (positive/negative/neutral/mixed) in importance scoring
- `alert_on_sentiment_shift` config option per topic
- Sentiment history tracking in state
- GitHub release monitoring via `github_repos` config
- Vendored feedparser (zero pip install needed)
- Feed discovery via `manage_topics.py discover-feed`
- OPML import via `manage_topics.py import-opml`

## [1.3.5] - 2026-03-03

### Changed
- Hardened subprocess handling and synced monitor docs/metadata.


## [1.3.3] - 2026-02-11

### Changed

- **Subprocess env hardening:** `monitor.py` now uses an allowlist for web-search-plus subprocess environment (`PATH`, `HOME`, `LANG`, `TERM` + search provider keys only).
- **Discord delivery flow:** Removed webhook-style delivery from skill docs/flow; Discord alerts are now emitted as structured JSON (`DISCORD_ALERT`) for OpenClaw agent delivery (same pattern as Telegram).
- **No direct HTTP calls:** Alerting/search integration is documented as agent-mediated JSON output + subprocess execution, without direct outbound HTTP from topic-monitor skill code.

## [1.3.2] - 2026-02-11

### 🆕 Real Alerting System

The alerting system is now fully functional (was a stub before):

- **Telegram Alerts:** Send immediate alerts for high-priority findings
- **Multi-Channel Support:** Telegram, Discord, and Email
- **Smart Filtering:** Importance scoring determines what gets alerted

### Changed

- **State Files:** Now stored in `.data/` directory (configurable via `TOPIC_MONITOR_DATA_DIR`)
- **Telegram ID:** Configured via `TOPIC_MONITOR_TELEGRAM_ID` environment variable (no hardcoded values)
- **web-search-plus Path:** Now relative by default, configurable via `WEB_SEARCH_PLUS_PATH`
- **No Hardcoded Paths:** All paths and IDs are now configurable

### Environment Variables

New environment variables for configuration:

| Variable | Default | Description |
|----------|---------|-------------|
| `TOPIC_MONITOR_TELEGRAM_ID` | — | Telegram chat ID for alerts |
| `TOPIC_MONITOR_DATA_DIR` | `.data/` | State and findings directory |
| `WEB_SEARCH_PLUS_PATH` | Relative | Path to web-search-plus script |

### Migration

If you had hardcoded paths in config.json, update to use environment variables:
```bash
export TOPIC_MONITOR_TELEGRAM_ID="your_telegram_id"
```

## [1.2.1] - 2026-02-04

- Privacy cleanup: removed hardcoded paths and personal info from docs
