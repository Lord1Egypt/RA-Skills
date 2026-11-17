# Changelog

## 2.0.0 (2026-11-05)

Rewritten for the current AIProx service.

- Calls `POST /v1/search` (35 sats) instead of a 50-sat multi-step orchestrate run.
- The response is now documented as AIProx returns it: `summary`, `key_findings` and up to 5 `sources`. No raw results.
- Added the search-content terms (no storing, reselling, redistributing or AI training).
- Added a "What this skill sends and costs" section, confirmation before paid calls, no autonomous loops, and results treated as data.
- Lightning only (L402 or a LightningProx spend token). `AIPROX_SPEND_TOKEN` is now optional (`metadata.openclaw.envVars`).
