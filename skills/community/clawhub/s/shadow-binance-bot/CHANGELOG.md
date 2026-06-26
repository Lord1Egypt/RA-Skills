# Changelog

All notable changes to this project will be documented in this file.

---

## [v1.3.3] - 2026-04-06

### Fixed — Registry Metadata Integrity (Final)
- Added `metadata.openclaw` block to SKILL.md YAML frontmatter with explicit:
  - `requires.env` listing all three environment variables
  - `requires.bins` listing Node.js >=18 runtime requirement
  - `security.credentials` declaring BINANCE_API_KEY and BINANCE_API_SECRET
  - `security.posture: read-only`, `trading: false`, `withdrawal: false`
- This ensures the registry-level metadata shown at the top of submission is **identical** to what SKILL.md requires, closing the last remaining gap
- The `registry:` block (added in v1.3.2) now has a parallel `metadata.openclaw.requires` section so **both** the platform's registry summary **and** the openclaw metadata block declare the same credentials and runtime requirements

### Security Posture (now explicit in metadata)
- `metadata.openclaw.security` declares: read-only posture, no trading, no withdrawal
- Platform operators can confirm the skill only reads Binance data and never places orders or moves funds

---

## [v1.3.2] - 2026-04-06

### Fixed — Registry Metadata Integrity
- Added explicit `registry:` block to SKILL.md metadata containing:
  - `platform: openclaw` and `runtime: node >=18.0.0`
  - Full credential descriptions (`BINANCE_API_KEY (required)`, etc.)
  - Security posture (`capabilities: read-only, no-trading, no-withdrawal`)
- This addresses the LLM scanner concern about a mismatch between "registry metadata shown to the platform" vs. SKILL.md
- The `requires:` section continues to list env vars and binaries as before for backward compatibility

### Security
- Added `license: MIT` to SKILL.md metadata block
- `registry.capabilities` now explicitly declares read-only/no-trading/no-withdrawal posture
- SKILL.md and README already recommend read-only API keys and IP restriction — this update makes that explicit in registry metadata

---

## [v1.3.1] - 2026-04-05

### Fixed — Registry Metadata Consistency
- SKILL.md registry metadata now includes `binaries: node >=18.0.0` requirement (was previously omitted)
- SKILL.md `requires.env` section already correctly listed `BINANCE_API_KEY`, `BINANCE_API_SECRET`, and `SPOT_SYMBOLS` — no change needed there
- Version bumped to `1.3.1` to reflect metadata correction

### Security
- Registry metadata now accurately reflects runtime requirements (Node.js) and credentials (env vars)
- No code changes — metadata only

---

## [v1.3.0] - 2026-04-04

### Fixed — Credentials & Platform Compatibility
- `src/index.cjs` now reads `process.env` first for `BINANCE_API_KEY`, `BINANCE_API_SECRET`, and `SPOT_SYMBOLS`. Platforms that inject credentials as environment variables will work automatically. Falls back to `config.env` for local development.
- SKILL.md and README updated to document both credential methods (env vars and config file).
- README now clearly shows Method 1 (env vars) as the recommended approach, with Method 2 (config file) as a local dev alternative.
- `config.env.example` clarifies the file is optional when env vars are set.

### Security
- SKILL.md Security & Privacy section updated to reflect dual credential method.

---

## [v1.2.0] - 2026-04-04

### Added
- **Demo Mode** with realistic mock data when no API keys are configured
- **Configurable Spot symbols** via `SPOT_SYMBOLS` env var in `config.env`
- **GitHub Actions CI** workflow (`.github/workflows/test.yml`) for automated testing
- **CODEOWNERS** file for PR routing
- **`SPOT_SYMBOLS` to `requires.env`** in SKILL.md

### Fixed
- `SKILL.md` moved from `skill/SKILL.md` to repo root (ClawHub requirement)
- `.gitignore` title comment removed (was breaking standard format)
- README step numbering fixed for Binance API key creation instructions
- README project structure updated to reflect `SKILL.md` at root and `tests/` directory
- CONTRIBUTING.md updated — "if tests exist" hedge removed (69 tests now exist)

### Security
- `config.env.example` now includes IP restriction reminder

---

## [v1.1.0] - 2026-04-04

### Added
- Unit tests for `analyzer.cjs` (22 tests covering futures/spot/behavior analysis)
- Unit tests for `shadowSim.cjs` (47 tests covering all strategy simulators)
- `.editorconfig` for consistent coding style across editors

### Fixed
- `simulateSelectiveTrading` now uses real trade counts per hour (`h.total`) instead of hardcoded estimates
- `simulateSpotDCA` gracefully handles missing `totalVolume` data
- `analyzeByHour` no longer mutates the original `pnlTrades` array passed in
- `getAllSpotTrades` now returns errors alongside partial results instead of silently skipping
- `binance.cjs` HTTPS requests now have a 10-second timeout (prevents indefinite hangs)
- `getMotivation` conditional boundaries clarified (no overlapping conditions)
- All magic number thresholds moved to named constants in `coach.cjs`
- All source files are now properly separated (were previously concatenated in git)

### Changed
- Console output changed from Unicode box-drawing chars to ASCII-compatible characters
- `package.json` `npm test` now runs the actual test suites
- Version bumped to `1.1.0` to reflect significant fixes and additions

### Security
- Request timeouts prevent indefinite resource consumption
- Improved error reporting surfaces partial API failures

---

## [v1.0.0] - 2026-03-11

### Added
- Initial release
- Basic Shadow Binance Bot functionality
- Futures income analysis with win/loss tracking
- Spot trade analysis for multiple symbols
- Shadow strategy simulation engine
- AI coaching feedback with behavioral pattern detection
- Demo Mode for when API keys are not configured

### Notes
- First public version
