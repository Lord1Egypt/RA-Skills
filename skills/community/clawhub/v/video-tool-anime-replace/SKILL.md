---
name: video-tool-anime-replace
description: "Replace or move an element in an existing HTTPS video with WeryAI anime-style processing (video-anime-replace). Use when the user wants anime-style object replace or move on a video URL, not text-to-video generation."
metadata: { "openclaw": { "emoji": "🎨", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
tags: [video, weryai, video-tools]
---

# WeryAI video tool — anime replace

This skill is **self-contained**: it documents and runs **only** the **`anime-replace`** workflow on an **existing** video given by URL. It is **not** text-to-video or image-to-video generation from scratch.

**Entry script:** `scripts/video_anime_replace.js` (alongside this `SKILL.md`).

**Runtime:** `WERYAI_API_KEY`, Node.js 18+.

**Inputs:** `video_url` and `image_url` must be **public `https://` URLs**. This script does not read local files and does not perform upload-file flows.

## What this package ships (verify before trust)

Canonical layout for **this** skill only:

- `SKILL.md`, `eval.yaml`
- `scripts/video_anime_replace.js` (**the only** runnable script in scope)

If your copy also contains `scripts/video_gen.js`, `scripts/video_toolkits.js`, `references/WERYAI_VIDEO_API.md`, or other CLIs, those files are **not** part of this skill’s contract — they may come from another repo sync or an over-broad install. **Do not run** them when you only want anime-replace; remove them or reinstall from a clean source. Inspect what you run: `node scripts/video_anime_replace.js spec`.

**Other tools** (multi-endpoint CLIs, local-file upload to growth/upload-file APIs, extra environment variables in those CLIs) are **out of scope** for this package. This skill’s script uses **only** `WERYAI_API_KEY` and public `https://` URLs.

## API surface (this tool only)

- **Required:** `video_url`, `image_url` (public `https://` URLs)
- **Optional:** `type` (`move` | `replace`), `resolution` (`480p` | `580p` | `720p`)
- **Defaults:** `type=replace`, `resolution=720p`

From **this skill root**, run `node scripts/video_anime_replace.js spec` to print the full tool schema (endpoint, required fields, defaults, enums) as JSON.

## Pre-submit gate (mandatory)

Do **not** run `submit` / `wait` until the user explicitly confirms URLs and non-default `type` / `resolution`. Paid runs are not idempotent.

## Workflow

Prefer `--dry-run` to validate JSON. Use `wait` to submit and poll until the task finishes; use `submit` only when the user wants a `task_id` without blocking, then `status` for later checks. Share final URLs as Markdown links `[Video](https://…)`.

## CLI

From **this skill root**:

```sh
node scripts/video_anime_replace.js wait \
  --json '{"video_url":"https://example.com/video.mp4","image_url":"https://example.com/ref.jpg"}'

node scripts/video_anime_replace.js submit \
  --json '{"video_url":"https://example.com/video.mp4","image_url":"https://example.com/ref.jpg","type":"replace","resolution":"720p"}'

node scripts/video_anime_replace.js status --task-id <task-id>
```

Dry-run:

```sh
node scripts/video_anime_replace.js wait \
  --json '{"video_url":"https://example.com/video.mp4","image_url":"https://example.com/ref.jpg"}' \
  --dry-run
```

## Security

Never write `WERYAI_API_KEY` into files. Keep **only** `WERYAI_API_KEY` set for this workflow; do not rely on undocumented env vars in sibling scripts if any were mistakenly present. The in-scope script reads **only** `WERYAI_API_KEY` (no other env keys). **`video_anime_replace.js`** accepts **only** `https://` media URLs (no disk read / no upload-file). Base URL and poll intervals are constants in the script, not env-driven.

Do **not** pass local filesystem paths or run tools that accept them unless you have **explicitly** reviewed and consented to their upload behavior — that is never required for this skill.

## Out of scope

- Any other WeryAI video-tool endpoints (subtitle, upscale, extend, face change, etc.)
- Text-to-video or image-to-video from scratch

## References

- [WeryAI llms.txt](https://docs.weryai.com/llms.txt)
- [Submit Video Anime Replace Task](https://docs.weryai.com/api-references/video-tools/submit-video-anime-replace-task)
