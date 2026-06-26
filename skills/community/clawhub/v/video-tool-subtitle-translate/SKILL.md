---
name: video-tool-subtitle-translate
description: "Translate subtitles in an existing HTTPS video via WeryAI (video-subtitle-translate). Use when the user wants subtitle translation, not erasure or text-to-video."
metadata: { "openclaw": { "emoji": "🌐", "primaryEnv": "WERYAI_API_KEY", "paid": true, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
tags: [video, weryai, video-tools]
---

# WeryAI video tool — subtitle translate

This skill is **self-contained**: it documents and runs **only** the **`subtitle-translate`** workflow on an **existing** video given by URL. It is **not** text-to-video or image-to-video generation from scratch.

**Entry script:** `scripts/video_subtitle_translate.js` (alongside this `SKILL.md`).

**Runtime:** `WERYAI_API_KEY`, Node.js 18+.

**Inputs:** `video_url` must be a **public `https://` URL**; `target_language` is a language code string (e.g. `en`, `zh`, `ja`). This script does not read local files and does not perform upload-file flows.

## What this package ships (verify before trust)

Canonical layout for **this** skill only:

- `SKILL.md`, `eval.yaml`
- `scripts/video_subtitle_translate.js` (**the only** runnable script in scope)

If your copy also contains `scripts/video_gen.js`, `scripts/video_toolkits.js`, `references/WERYAI_VIDEO_API.md`, or other CLIs, those files are **not** part of this skill’s contract — they may come from another repo sync or an over-broad install. **Do not run** them when you only want subtitle-translate; remove them or reinstall from a clean source. Inspect what you run: `node scripts/video_subtitle_translate.js spec`.

**Other tools** (multi-endpoint CLIs, local-file upload to growth/upload-file APIs, extra environment variables in those CLIs) are **out of scope** for this package. This skill’s script uses **only** `WERYAI_API_KEY` and public `https://` URLs.

## API surface (this tool only)

- **Required:** `video_url` (public `https://` URL), `target_language` (e.g. `en`, `zh`, `ja`, `ko`, `fr`, `de`, `es`)

From **this skill root**, run `node scripts/video_subtitle_translate.js spec` to print the full tool schema (endpoint, required fields, defaults, enums) as JSON.

## Pre-submit gate (mandatory)

Do **not** run `submit` / `wait` until the user explicitly confirms the video URL and `target_language`. Paid runs are not idempotent.

## Workflow

Prefer `--dry-run` to validate JSON. Use `wait` to submit and poll until the task finishes; use `submit` only when the user wants a `task_id` without blocking, then `status` for later checks. Share final URLs as Markdown links `[Video](https://…)`.

## CLI

From **this skill root**:

```sh
node scripts/video_subtitle_translate.js wait \
  --json '{"video_url":"https://example.com/video.mp4","target_language":"en"}'

node scripts/video_subtitle_translate.js submit \
  --json '{"video_url":"https://example.com/video.mp4","target_language":"en"}'

node scripts/video_subtitle_translate.js status --task-id <task-id>
```

Dry-run:

```sh
node scripts/video_subtitle_translate.js wait \
  --json '{"video_url":"https://example.com/video.mp4","target_language":"en"}' \
  --dry-run
```

## Security

Never write `WERYAI_API_KEY` into files. Keep **only** `WERYAI_API_KEY` set for this workflow; do not rely on undocumented env vars in sibling scripts if any were mistakenly present. The in-scope script reads **only** `WERYAI_API_KEY` (no other env keys). **`video_subtitle_translate.js`** accepts **only** `https://` media URLs (no disk read / no upload-file). Base URL and poll intervals are constants in the script, not env-driven.

Do **not** pass local filesystem paths or run tools that accept them unless you have **explicitly** reviewed and consented to their upload behavior — that is never required for this skill.

## Out of scope

- Removing or painting out subtitles without translation
- New video generation from text only

## References

- [WeryAI llms.txt](https://docs.weryai.com/llms.txt)
