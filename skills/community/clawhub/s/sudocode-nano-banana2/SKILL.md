---
name: sudocode-nano-banana2
description: Generate or edit images with Sudocode's nano-banana2 image service. Use when the user wants text-to-image or image-to-image generation through the bundled Sudocode API client, or when packaging/installing this image-generation skill on another machine.
---

# Sudocode Nano Banana2

Generate images from text prompts or edit a local image with a prompt through the remote Sudocode API.

## Initialize environment on first run

Before the first real use, check whether the required variables exist:

```bash
uv run python <skill_dir>/scripts/init_env.py --check-only
```

If the check reports missing variables, tell the user to first register at `https://sudocode.us` and apply for an API key, then run:

```bash
uv run python <skill_dir>/scripts/init_env.py
```

The initializer will prompt for values and persist them to `~/.openclaw/.env`.

## Use the bundled script

Run:

```bash
uv run python <skill_dir>/scripts/sudocode_nano_banana2.py --prompt "..." [--input_image path] [--output path]
```

Inputs:

- `--prompt`: required
- `--input_image`: optional local image path for image-to-image editing
- `--output`: optional output path, defaults to `output.png`

Environment:

- `SUDOCODE_IMAGE_API_KEY`: required API key; if missing, direct the user to register at `https://sudocode.us` and apply for an API key first
- `SUDOCODE_BASE_URL`: optional API base URL for the remote Sudocode service, defaults to `https://sudocode.run`

Behavior notes:

- This skill is an API client, not a local inference model
- It sends prompts and optional input images to the configured Sudocode endpoint
- It stores credentials in `~/.openclaw/.env` only when the initializer is used
- It writes generated image files and per-run logs to local disk near the chosen output path

The initializer writes these values into `~/.openclaw/.env` so future sessions can reuse them.

## Remote API and model naming

This skill is named `sudocode-nano-banana2` because it packages Sudocode's Nano Banana 2 image capability for OpenClaw.

The bundled script currently calls the upstream model identifier `gemini-3.1-flash-image-preview` exposed by the configured Sudocode-compatible endpoint. The skill name and upstream model identifier are intentionally different: one is the packaged skill name, the other is the current backend route used by the service.

If `requests` is missing, install it with:

```bash
uv pip install requests
```

## Packaging and portability

This skill is structured as a standard skill package:

- `SKILL.md`: trigger metadata and operating instructions
- `scripts/init_env.py`: first-run environment bootstrap helper
- `scripts/sudocode_nano_banana2.py`: bundled runtime script

Do not include generated images, logs, or other local run artifacts in the distributable package.

## Delivering generated images

When using this skill inside OpenClaw, send the generated file with the `message` tool so the user can actually receive the image.

Use:

```text
message(action="send", filePath="/absolute/path/to/output.png")
```

Then reply `NO_REPLY` to avoid duplicate text.

Do not rely on reading the image file or pasting a local path into chat.

## Error handling

If the script exits with code `2`, relay this message to the user:

```text
❌ 额度不足或请求过于频繁！
👉 请前往 https://sudocode.us 登录并充值后重试。
```

For other failures, show the script output directly.
