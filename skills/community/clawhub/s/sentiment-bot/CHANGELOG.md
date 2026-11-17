# Changelog

## 2.0.0 (2026-11-05)

Rewritten for the current AIProx service.

- Calls `POST /api/orchestrate` with `capability: sentiment-analysis` (one step on sentiment-bot, 50 sats). The old example body had no `task` and was refused with a 400.
- Removed batch, comparative, trend and URL modes, which are not reachable through AIProx. One text per call.
- Added a "What this skill sends and costs" section, confirmation before paid calls, no autonomous loops, and results treated as data.
- Lightning only (L402 or a LightningProx spend token). `AIPROX_SPEND_TOKEN` is now optional (`metadata.openclaw.envVars`).
