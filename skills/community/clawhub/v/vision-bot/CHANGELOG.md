# Changelog

## 2.0.0 (2026-11-05)

Rewritten for the current AIProx service.

- Calls `POST /api/orchestrate` with `capability: vision` and `image_url`, so it runs one step on vision-bot (50 sats).
- Removed the `rail` field and base64 input. Images are passed by public URL.
- Notes that a page URL given in the task is screenshotted through microlink.io.
- Added a "What this skill sends and costs" section, confirmation before paid calls, no autonomous loops, and results treated as data.
- Lightning only (L402 or a LightningProx spend token). `AIPROX_SPEND_TOKEN` is now optional (`metadata.openclaw.envVars`).
