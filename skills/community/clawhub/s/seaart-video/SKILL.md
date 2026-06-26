---
name: seaart-video
version: "1.0.0"
description: Use this skill to generate high-quality AI videos using the SeaArt platform (seaart.ai). Supports both Text-to-Video and Image-to-Video generation using various models. Use this whenever the user wants to "create a video", "generate a video", "turn this image into a video", or explicitly mentions SeaArt video generation.
tags: ["video", "ai", "seaart", "text-to-video", "image-to-video"]
metadata:
  clawdbot:
    requires:
      env:
        - name: SEAART_TOKEN
          primary: true
          description: SeaArt session token (T cookie). Treat like a password.
      binaries:
        - name: python3
          primary: true
        - name: pip3
          description: Required to install the requests library if not present.
---

# SeaArt Video Generator

This skill helps you generate AI videos via the SeaArt platform. You can create videos from text prompts (Text-to-Video) or animate existing images (Image-to-Video).

## Prerequisites: SeaArt Token

To use this skill, you need a SeaArt authentication token. This token is passed in the `T` cookie.

### How to get your token:
1. Log into your account on [seaart.ai](https://www.seaart.ai) in your browser.
2. Open Developer Tools (F12 or Right Click -> Inspect).
3. Go to the "Application" tab (or "Storage" in Firefox).
4. Expand "Cookies" and select `https://www.seaart.ai`.
5. Find the cookie named `T`.
6. Copy its value (it will look like a long string: `eyJhbGci...`).

### How to store your token:
To avoid passing the token every time, store it as an environment variable (`SEAART_TOKEN`).

Run the following command in your terminal (never paste the token into chat):

```
/update-config set SEAART_TOKEN="your_token_value_here"
```

> **Security note:** Never share your token in chat messages or logs. The token will be persisted in your local agent config by `/update-config` — ensure only you have access to that config file.

## Supported Models and Parameters

We currently support the following models for video generation.

**Default Model:** SeaArt Sono Cast (if user doesn't specify, use this one)

| Model Name | `model_no` | `model_ver_no` | Notes |
|------------|------------|----------------|-------|
| **SeaArt Sono Cast** (Default) | `d4t763te878c73csvcf0` | `21a5fc20-68dd-4d4b-9afd-7bfe2e8f5166` | Great overall quality. |
| **Vidu Q3 Turbo** | `d6l3adte878c73dr6a3g` | `26ca53e1-e6f2-44e4-8227-13e38bb73945` | |
| **Kling 3.0** | `d62lo1te878c73f8eua0` | `93636e78-3d55-4416-92e3-d7d3b89f023d` | |
| **Wan 2.6** | `d4t6pkle878c73cpsif0` | `5856d251-5b8f-4704-970e-e301982eb532` | |

### Supported Aspect Ratios (Text-to-Video only)
- `16:9` (Landscape)
- `9:16` (Portrait) - Default
- `1:1` (Square)
- `4:3`
- `3:4`

## How to use this skill

When a user asks to generate a video, follow these steps:

### 1. Check for the Token
First, check if the `SEAART_TOKEN` environment variable is set. You can do this by running a simple bash command: `echo $SEAART_TOKEN`.
If it's empty, ask the user to provide their token. Once they provide it, you should guide them to set it as an environment variable in their specific environment (OpenClaw, Claude Code, or terminal) as described above. Wait for them to do this before proceeding.

### 2. Gather Requirements
If the token is available, ensure you have:
- The prompt (what should happen in the video)
- The type (Text-to-Video or Image-to-Video)
- If Image-to-Video, the image URL
- The desired model (default to SeaArt Sono Cast)
- If Text-to-Video, the desired aspect ratio (default to 9:16)

### 3. Generate the Video
Use the included python script to start the generation and poll for completion.

```bash
# For Text-to-Video
python3 ~/.claude/skills/seaart-video/scripts/generate.py \
  --type t2v \
  --prompt "A child crying" \
  --model seaart-sono-cast \
  --aspect-ratio "9:16"

# For Image-to-Video
python3 ~/.claude/skills/seaart-video/scripts/generate.py \
  --type i2v \
  --prompt "He got married" \
  --image-url "https://image.cdn2.seaart.me/..." \
  --model seaart-sono-cast
```

The script will handle making the request and polling the status until the video is complete, then return the final video URL.

## Example Usage

**User:** "Can you make a video of a cat playing with a ball of yarn using Kling 3.0?"

**Claude:**
1. Checks for `$SEAART_TOKEN`. Let's assume it's set.
2. Runs the generation script:
```bash
python3 ~/.claude/skills/seaart-video/scripts/generate.py --type t2v --prompt "A cat playing with a ball of yarn" --model kling3.0
```
3. Presents the final video URL to the user.

---

## External Endpoints

| URL | Method | Data Sent |
|-----|--------|-----------|
| `https://www.seaart.ai/api/v1/task/v2/video/text-to-video` | POST | Prompt, model ID, aspect ratio, generation params |
| `https://www.seaart.ai/api/v1/task/v2/video/img-to-video` | POST | Prompt, image URL, model ID, generation params |
| `https://www.seaart.ai/api/v1/task/batch-progress` | POST | Task ID (for polling status) |

All requests are authenticated via your `SEAART_TOKEN` cookie, which never leaves your machine in plaintext — it is only sent to `*.seaart.ai` as an HTTP cookie header.

---

## Security & Privacy

- **What leaves your machine**: Your text prompt, any image URLs you provide, and your `SEAART_TOKEN` are sent to `seaart.ai` servers as an HTTP cookie header on every API request.
- **Token storage**: `SEAART_TOKEN` is persisted locally in your agent config file by `/update-config`. Ensure only you have access to that config. It is not logged or transmitted by this skill beyond the API calls to seaart.ai listed above.
- **No additional data persistence**: This skill does not write any other files to disk. Generated video URLs are returned inline.
- **Input handling**: All inputs are passed as structured JSON fields via the `requests` library — no shell interpolation is used.

---

## Trust Statement

By using this skill, your prompt and any provided image URLs are sent to [seaart.ai](https://www.seaart.ai). Only install and use this skill if you trust SeaArt with your creative content. This skill is not affiliated with or endorsed by SeaArt.
