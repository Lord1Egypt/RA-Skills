# WhatsApp Sticker

Convert images into lightweight WebP stickers and send them as **native WhatsApp stickers** through an existing, trusted Baileys bridge.

This skill is designed for [Hermes Agent](https://github.com/NousResearch/hermes-agent) environments where a WhatsApp bridge is already configured and connected.

## Features

- **Native WhatsApp stickers** — sends stickers as sticker media, not ordinary images.
- **Automatic conversion** — converts supported image formats into WebP.
- **Sticker dimensions** — resizes and pads images to fit within 512 × 512 pixels while preserving aspect ratio.
- **Size optimization** — reduces image quality progressively to target a file size of 100 KB or less.
- **Bridge health checks** — verifies that the WhatsApp bridge is connected before sending.
- **Bridge integrity check** — optionally verifies that the running bridge matches the local bridge script.
- **Automatic cleanup** — removes temporary converted files after execution.
- **No new WhatsApp session** — uses an existing authenticated bridge.

## Requirements

Before using this skill, make sure you have:

- Node.js 20 or newer.
- FFmpeg with `libwebp` encoding support.
- A configured and authenticated Baileys WhatsApp bridge.
- A bridge exposing compatible `/health` and `/send-media` endpoints.
- A valid WhatsApp chat ID and a local image file.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/SakumDisiniPa/whatsapp-sticker.git
cd whatsapp-sticker
```

Replace `USERNAME` with the GitHub account or organization that owns the repository.

### 2. Install FFmpeg

On Ubuntu or Debian:

```bash
sudo apt update
sudo apt install ffmpeg
```

Verify the installation:

```bash
ffmpeg -version
ffmpeg -encoders | grep libwebp
```

### 3. Configure the WhatsApp bridge

Start your existing Baileys bridge and make sure its health endpoint reports a connected WhatsApp session.

By default, the script expects the bridge at:

```text
http://127.0.0.1:3000
```

The bridge must implement the endpoint contract documented below. This skill does not create or authenticate a WhatsApp session.

## Usage

Run the conversion and sending script:

```bash
node convert-send.mjs /absolute/path/to/image.jpg RECIPIENT_CHAT_ID
```

For example, replace the image path and recipient ID with values you control:

```bash
node convert-send.mjs "$HOME/Pictures/sticker.png" "YOUR_CHAT_ID"
```

The script will:

1. Validate the supplied image path and recipient.
2. Check the bridge health and connection status.
3. Verify bridge integrity when hash checking is enabled.
4. Convert the image to a 512 × 512 WebP sticker.
5. Attempt to keep the output at or below 100 KB.
6. Send the converted file through the bridge as native sticker media.
7. Report the result and remove the temporary file.

**Note:** The bridge's success response confirms the result reported by the bridge; it does not necessarily guarantee that the recipient has viewed or received the sticker.

## Configuration

The script supports these environment variables:

| Variable | Default | Description |
|---|---|---|
| `WHATSAPP_BRIDGE_URL` | `http://127.0.0.1:3000` | Base URL of the configured bridge |
| `WHATSAPP_BRIDGE_FILE` | Hermes bridge script path | Path to the compatible `bridge.js` file |
| `WHATSAPP_CHECK_BRIDGE_HASH` | Enabled | Set to `false` to disable the bridge script hash check |

Example:

```bash
export WHATSAPP_BRIDGE_URL="http://127.0.0.1:3000"
export WHATSAPP_BRIDGE_FILE="$HOME/.hermes/hermes-agent/scripts/whatsapp-bridge/bridge.js"

node convert-send.mjs "$HOME/Pictures/sticker.png" "YOUR_CHAT_ID"
```

Only disable hash checking if you understand why the bridge does not support the expected integrity check and you trust the bridge implementation.

## Bridge API

The script expects a compatible local HTTP bridge.

### Health check

```http
GET /health
```

The response should indicate that the WhatsApp session is connected. If hash checking is enabled, the bridge must also expose the expected script hash.

### Send sticker

```http
POST /send-media
Content-Type: application/json
```

Request body:

```json
{
  "chatId": "RECIPIENT_CHAT_ID",
  "filePath": "/absolute/path/to/sticker.webp",
  "mediaType": "sticker"
}
```

The bridge should validate the request, access the specified local file, and return a structured response indicating whether the send operation succeeded.

**Important:** This repository does not include the WhatsApp bridge itself. Endpoint compatibility depends on your existing bridge implementation.

## Project Structure

```text
whatsapp-sticker/
├── SKILL.md
├── README.md
└── convert-send.mjs
```

## Security

- Use only recipient IDs supplied or explicitly confirmed by the user.
- Keep WhatsApp session files and credentials private.
- Never commit session directories, authentication tokens, personal chat IDs, or private logs.
- Bind the bridge to localhost unless remote access is deliberately secured.
- Never expose an unauthenticated media-sending endpoint to the public internet.
- Validate incoming paths and requests in the bridge to prevent unauthorized file access.
- Use only trusted bridge code and dependencies.

A local bridge URL is not a substitute for authentication if the service is exposed beyond the local machine.

## Troubleshooting

### Bridge is unavailable

Check whether the bridge is running:

```bash
curl -s http://127.0.0.1:3000/health
```

If the endpoint cannot be reached, start or repair the existing bridge.

### WhatsApp is disconnected

Reconnect the existing WhatsApp session using your bridge's normal authentication procedure. Do not publish session files or credentials.

### FFmpeg is missing

Install FFmpeg and verify that the `libwebp` encoder is available.

### Bridge hash mismatch

The running bridge may be using a different version from the bridge script on disk. Restart or update the bridge using its normal process manager, then check the health endpoint again.

### Sticker exceeds the size limit

The script progressively lowers WebP quality. If the output still exceeds the limit, try a simpler image or reduce its visual complexity.

## License

Choose a license before publishing this project. If you want others to reuse, modify, and redistribute the code, consider adding an appropriate open-source license such as the MIT License.

---

Built for Hermes Agent users who want a simple workflow for converting images and sending native WhatsApp stickers through an existing Baileys bridge.
