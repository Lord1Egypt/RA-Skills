---
name: yummy-shared
version: 1.0.0
description: "Use when operating yummycli for the first time, checking Gemini credential status, handling yummycli JSON command output, or applying shared CLI safety rules before image generation or editing."
always: true
metadata:
  requires:
    bins: ["yummycli"]
  openclaw:
    requires:
      bins: ["yummycli"]
      env: ["GEMINI_API_KEY"]
    primaryEnv: GEMINI_API_KEY
  hermes:
    tags: [yummycli, shared, gemini, authentication]
    requires_toolsets: ["yummycli"]
install:
  - kind: node
    package: "@yummysource/yummycli"
    bins: ["yummycli"]
---

# yummycli Shared Rules

Shared operating rules for `yummycli`.

## Authentication

Before running Gemini image commands, confirm the provider is configured:

```bash
yummycli auth status --provider gemini
```

If Gemini is not configured, initialize it:

```bash
yummycli gemini init --api-key "<api-key>"
```

## Output Contract

All `yummycli` generation commands return JSON on stdout. Read the response and use the `output` field as the generated file path.

Image example:

```json
{
  "provider": "gemini",
  "output": "gemini_20260410123456_789.png",
  "model": "gemini-3.1-flash-image-preview",
  "inputImageCount": 2
}
```

Video example:

```json
{
  "provider": "gemini",
  "output": "veo_20260417_142301_047.mp4",
  "model": "veo-3.1-fast-generate-preview",
  "duration_seconds": 8,
  "aspect_ratio": "16:9",
  "resolution": "1080p",
  "elapsed_seconds": 73
}
```

## Safety Rules

- Only use local image files explicitly provided by the user.
- Preserve the order of repeated `--input-image` flags.
- Do not overwrite a user-specified output path unless the command is intentionally run that way.
- If the command returns a validation error, fix the arguments before retrying.
- Report the final output path back to the user after a successful run.
