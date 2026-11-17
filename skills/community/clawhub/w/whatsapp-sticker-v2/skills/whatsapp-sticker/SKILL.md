---
name: whatsapp-sticker
description: "Convert images into WebP stickers and send native WhatsApp stickers through an existing Baileys bridge."
---

# WhatsApp Sticker

Use this skill when the user asks to convert an image into a WhatsApp sticker and send it to a specified chat.

## Requirements

- Node.js 20 or newer.
- FFmpeg with `libwebp` support.
- A trusted, running Baileys bridge exposing `/health` and `/send-media`.
- An authenticated WhatsApp session owned and configured by the user.
- A valid recipient chat ID and a local image file.

## Usage

Run:

`node convert-send.mjs /absolute/path/to/image.jpg RECIPIENT_CHAT_ID`

The script converts the image to a 512 × 512 WebP sticker, attempts to keep it under 100 KB, checks bridge connectivity, and requests native sticker delivery.

## Configuration

- `WHATSAPP_BRIDGE_URL`: bridge base URL; defaults to `http://127.0.0.1:3000`.
- `WHATSAPP_BRIDGE_FILE`: path to the compatible bridge's `bridge.js`.
- `WHATSAPP_CHECK_BRIDGE_HASH`: set to `false` only when intentionally using a trusted bridge without matching hash support.

Keep the bridge bound to localhost unless remote access is deliberately secured. Never expose an unauthenticated sending endpoint to the public internet.

## Safety

- Use only chat IDs supplied or confirmed by the user.
- Never create or export another person's WhatsApp session.
- Do not claim a sticker was delivered unless the bridge confirms the request.
- Do not publish session files, credentials, private chat IDs, or personal data.

