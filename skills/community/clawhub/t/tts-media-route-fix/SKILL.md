---
name: tts-media-route-fix
description: Fix and verify OpenClaw TTS media-route behavior in installed dist builds. Use when users report that tts.convert returns unusable audio URLs, media TTS MP3 routes serve HTML instead of binary audio, Bearer auth is not enforced on media routes, Range requests fail, or temporary TTS files are not cleaned up. Applies to hashed gateway-cli dist files and includes backup, patch, restart, and curl verification workflow.
---

# TTS Media Route Fix

## Overview

Apply a production-safe patch workflow for OpenClaw installs where `tts.convert` and `/media/tts/<id>.mp3` routing are broken or incomplete.
Always back up hashed dist files before edits, patch minimally, restart gateway, and verify with authenticated range curl.

## Workflow

1. Locate active hashed `gateway-cli-*.js` files.
2. Back up each file to `*.bak` before modifying.
3. Patch HTTP handler for `GET/HEAD /media/tts/<id>.mp3` with auth, validation, binary output, and Range.
4. Ensure `tts.convert` payload returns `audioUrl` under `/media/tts/<id>.mp3` and mp3 metadata.
5. Restart gateway.
6. Verify with Bearer-authenticated curl (including `--range`).
7. Confirm temporary file TTL cleanup (2–5 minutes).

## Commands

### 1) Find hashed dist targets

Use `scripts/find_gateway_cli.sh` to locate candidate files:

```bash
bash scripts/find_gateway_cli.sh
```

If multiple candidates exist, patch only the currently used runtime build(s).

### 2) Back up before edits

For each target:

```bash
cp /path/to/gateway-cli-<hash>.js /path/to/gateway-cli-<hash>.js.bak
```

Never skip backups.

### 3) Patch requirements

Implement or fix handler for `GET` and `HEAD` at `/media/tts/<id>.mp3`:

- Validate filename strictly (no traversal, fixed suffix `.mp3`).
- Require Bearer token with same gateway auth policy.
- Serve binary MP3 with `Content-Type: audio/mpeg`.
- Support Range and send `Accept-Ranges: bytes`.
- Correct status behavior: `404`, `405`, `416`, `200/206`.

For `tts.convert`, ensure response structure:

```json
{
  "ok": true,
  "payload": {
    "audioUrl": "/media/tts/<id>.mp3",
    "mimeType": "audio/mpeg",
    "format": "mp3"
  }
}
```

TTL behavior: keep files temporary and auto-clean in 2–5 minutes.

### 4) Restart gateway

```bash
openclaw gateway restart
```

### 5) Verify media route

Use `scripts/verify_tts_media_route.sh` or run manually:

```bash
curl -i -H "Authorization: Bearer <token>" \
  "http://<host>:<port>/media/tts/<id>.mp3" \
  --range 0-127
```

Expected:

- HTTP `200` or `206`
- `Content-Type: audio/mpeg`
- Binary content (not HTML / control-ui page)

## Guardrails

- Patch minimally; avoid unrelated refactors.
- Keep auth checks identical to existing gateway Bearer model.
- Preserve existing routing behavior outside `/media/tts/*`.
- If patching fails, restore `.bak` and retry.

## Resources

### scripts/

- `find_gateway_cli.sh` — locate hashed runtime files for patching.
- `verify_tts_media_route.sh` — quick authenticated range-check for MP3 route.

### references/

- `patch-checklist.md` — concise checklist of required behaviors and acceptance criteria.
