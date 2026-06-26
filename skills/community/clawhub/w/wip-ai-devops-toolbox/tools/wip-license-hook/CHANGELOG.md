# Changelog

## 0.1.0 (2026-02-15)

### Initial Release

- Core license detection engine with fingerprinting for 14 license types
- License ledger (`LICENSE-LEDGER.json`) with dependency tracking
- LICENSE file snapshot archiving with date-stamped copies
- Auto-detection of package managers: npm, pip, cargo, go modules
- Git pre-pull hook (hard gate — blocks merge on license change)
- Git pre-push hook (advisory — warns but doesn't block)
- Upstream fork license monitoring via git remote
- Static HTML dashboard generator with dark theme
- CLI with commands: init, scan, check, gate, report, dashboard, alert, install, badge
- Offline mode (skips network calls, uses cached data)
- Shields.io badge URL generation
