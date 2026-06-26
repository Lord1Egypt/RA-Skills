# Changelog

## [1.0.0] - 2026-03-17

### Added
- Initial release
- Single keyword rank lookup via ClawHub search API
- Batch keyword tracking with summary table
- Competitor analysis mode (`--competitors`)
- Top N results view (`--top N`)
- Verbose output with scores and descriptions (`--verbose`)
- JSON export for scripting and trend tracking (`--json`)
- Input validation and security checks
- Auto-retry on rate limiting (HTTP 429)
- Graceful error handling per keyword (no batch abort)
- Emoji medals for top 3 positions (🥇🥈🥉)
- Summary statistics (ranked count, average rank, best rank)
