---
name: seedream-5-byteplus
description: Generate images with Seedream 5 through the BytePlus Ark API using a direct API key. Use when the user wants Seedream 5 image generation, mentions BytePlus Ark, Seedream, or has a Seedream/Ark API key. If the user asks for a specific format, poster, wallpaper, social post, or exact dimensions, ask for the required size or aspect ratio before generating.
---

# Seedream 5 via BytePlus Ark

Generate images through **BytePlus Ark** using the bundled script in `scripts/seedream-generate.sh`.

## Quick start

1. Ensure `SEEDREAM_API_KEY` is available in the environment or in `/root/.clawdbot/.env`.
2. Run:

```bash
/root/clawd/skills/seedream-5-byteplus/scripts/seedream-generate.sh "your prompt here" [output-file]
```

Example:

```bash
/root/clawd/skills/seedream-5-byteplus/scripts/seedream-generate.sh \
  "A cinematic scene of a monkey sitting proudly on top of a red Ferrari sports car" \
  /root/clawd/output/seedream-monkey-ferrari.jpg
```

The script prints the saved file path on success.

## When to use this skill

Use this skill when:
- The user has a **Seedream / BytePlus Ark API key**
- The user wants **Seedream 5** specifically
- The user mentions **BytePlus Ark**, **Seedream**, or `seedream-5-0-260128`

Do **not** use this skill for:
- Black Forest Labs direct FLUX API
- fal.ai keys (`FAL_KEY`)
- OpenAI image generation
- Google Gemini image generation

## Ask about size when needed

If the user clearly needs a specific layout or delivery format, ask for the target size or aspect ratio before generating.

Examples:
- social post
- story / reel cover
- wallpaper
- poster
- banner
- print asset
- exact pixel dimensions

If the user does not care, use the default size.

## Default behavior

The script defaults to:
- model: `seedream-5-0-260128`
- size: `2K`
- response format: `url`
- watermark: `false`

Override these with environment variables before running:

```bash
export SEEDREAM_MODEL=seedream-5-0-260128
export SEEDREAM_SIZE=1K
```

Then call the script normally.

## How it works

The script sends a POST request to the BytePlus Ark image generation endpoint, extracts the returned image URL, and downloads the image locally.

## Troubleshooting

- If the script says `SEEDREAM_API_KEY not set`, add the key to the environment first.
- If generation fails, inspect the JSON returned by the API; the script prints it to stderr.
- If the provider returns no image URL, inspect the raw response to confirm the response schema.

## scripts/

- `scripts/seedream-generate.sh` — direct Seedream 5 image generation via BytePlus Ark API
