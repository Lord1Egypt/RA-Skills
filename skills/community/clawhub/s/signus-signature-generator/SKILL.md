---
name: signus-font-signature
description: Generate signature images via the Signus API and return image files for chat delivery. Use when asked for signature generation through Signus API.
---

# Signus Font Signature

## User-facing language
- Always write user-facing text in English unless the user explicitly asks for another language.

## Runtime requirements
- Node.js 18+.
- Install dependencies in this skill folder before first run:
```bash
cd /home/node/.openclaw/workspace/skills/signus-font-signature && npm install
```

## Inputs
Provide exactly one identity source:
- `name` (e.g., `"Allon Mason"`), OR
- `firstName` + `lastName`, OR
- `initials` (e.g., `"AM"`)

Optional:
- `count` — max number of images to return.

## Validation
- Accept exactly one identity source.
- Reject empty/blank values.
- If `count` is provided, treat as numeric limit.

## Run
```bash
node /home/node/.openclaw/workspace/skills/signus-font-signature/scripts/generate_font_signatures.js '<json payload>'
```

Examples:
```bash
node /home/node/.openclaw/workspace/skills/signus-font-signature/scripts/generate_font_signatures.js '{"name":"Allon Mason","count":10}'
```

```bash
node /home/node/.openclaw/workspace/skills/signus-font-signature/scripts/generate_font_signatures.js '{"firstName":"Allon","lastName":"Mason"}'
```

## Detailed execution flow
1. Parse payload and normalize identity into `name`.
2. Create output directory:
   - `~/.openclaw/media/signatures-font/<name>-<timestamp>/`
3. Request font generation using fixed trusted host (`https://api.signus.ai`) and endpoint order:
   - primary: `POST /api/signus/v0/signature-generations/font`
   - fallback: `POST /api/signus/v0/users/me/signature-generations/font`
4. Process response by content-type:
   - ZIP/octet-stream: extract with in-process JS unzip library (`adm-zip`), then collect image files.
   - JSON: read `payload.thisPageItems[]`, then download each image from:
     - `/api/signus/v0/signature-generations/font/{generationId}/signatures/{generatedSignatureId}/{clean|watermark}.png`
5. Return:
   - `count`
   - `directory`
   - `signatures[]: { id, filePath }`
6. Send images to chat via `message action=send` and `media=<filePath>`.

## Authentication model
- This skill does **not** handle API tokens or env-based credentials.
- It assumes the primary public endpoint can be used without explicit `Authorization` header.
- The `/users/me/...` fallback may work only where implicit session/auth exists.
- If your deployment requires explicit auth, update the script design first (do not inject secrets into payloads by default).

## Security notes
- No environment-variable reads.
- No shell command execution.
- Network target is fixed to `https://api.signus.ai`.
- Writes only under `~/.openclaw/media/signatures-font/`.
- Keep this skill focused on Signus API signature generation and chat-ready image outputs.
