---
name: seedance-storyboard
description: End-to-end Asset-First storyboard-to-video pipeline on HotAPI using Seedream 5.0 (character/scene/prop locking) and Seedance 2.5 / 2.0 (reference-to-video, draft-first 480p preview, 1080p finalize, and offline HTML review board). Use for multi-shot AI short dramas, consistent-character video generation, or executing exported project_bundle.json manifests into real media assets.
metadata:
  product: "HotAPI"
  version: "1.0"
---

# Seedance Storyboard Runner (`HotAPI`)

Compile and execute Asset-First multi-shot video storyboards end-to-end against HotAPI without manual web-UI shuffling. Generates and locks reusable character/scene/prop references with Seedream 5.0, renders multi-shot segments via Seedance 2.5 / 2.0 `reference-to-video` (with optional 480p `draft: true` preview before committing to 1080p `draft-to-video` finalization), and builds a self-contained offline HTML review board.

## When to use

- Producing multi-shot AI short dramas, commercials, or narrative shorts that require cross-shot character and scene consistency.
- Turning structured storyboard prompts into real Seedream images and Seedance videos via CLI or agent automation.
- Executing exported `project_bundle.json` manifests (e.g., from upstream director/screenplay skills) into real visual assets and playable video clips.

## Sources of truth

- Exact request/response schemas: [OpenAPI 3.1](https://api.hotapi.ai/docs/json)
- Model catalog & capabilities: [HotAPI models](https://hotapi.ai/en/docs/models)
- Live per-second & per-image rates: [HotAPI pricing](https://hotapi.ai/en/pricing)

OpenAPI wins if any parameter description and request schema disagree.

## 4-Step Workflow

### 1. Lock pipeline parameters before generating

Confirm or set these defaults in `storyboard.json`:

- **Video model**: `seedance-2.5-spicy` (up to 30 ref images, 4–30s, supports `draft` + 1080p `draft-to-video`), `seedance-2.5-flash-spicy` (up to 10 ref images, 4–30s, 480p/720p, no draft), or `seedance-2.0-spicy` / `seedance-2.0-fast-spicy` / `seedance-2.0-mini-spicy` (up to 9 ref images, 4–15s, no draft).
- **Image model**: `seedream-5.0-pro-spicy` (2K) or `seedream-5.0-lite-spicy` (2K/3K/4K).
- **Aspect ratio**: `16:9` (default), `9:16`, or `21:9` (`1:1`, `4:3`, `3:4` also supported).
- **Draft-first workflow**: Enabled by default on `seedance-2.5-spicy` (`render --draft` at 480p → visual review in `board.html` → `finalize` approved segments to 1080p).

### 2. Author `storyboard.json` (or import an existing bundle)

Write a `storyboard.json` manifest (see `examples/sample-storyboard.json`), or convert an existing `project_bundle.json`:

```bash
python3 scripts/storyboard_runner.py import-bundle path/to/project_bundle.json -o storyboard.json
```

Top-level fields in `storyboard.json`:
- `project`: `{ title, video_model, image_model, video_aspect, asset_aspect, generate_audio, output_format }`
- `assets[]`: `[{ id, type, prompt, aspect_ratio?, local_file?, url? }]`
- `segments[]`: `[{ id, duration_seconds, prompt?, asset_refs?, audio_refs?, video_refs?, shots?: [{ id, start, end, action, camera, dialogues?: [{ character_id, text }] }] }]`

Note: Generating character portraits with Seedream 5.0 also produces trusted synthetic face references that work directly with Seedance `reference-to-video` without real-photo face verification prompts.

### 3. Pre-flight validate (zero credits spent)

Run mechanical and budget validation before touching any paid API endpoint:

```bash
python3 scripts/storyboard_runner.py validate storyboard.json
```

`validate` checks global ID uniqueness, dangling `asset_refs`, contiguous shot timing (`0..duration_seconds`), per-model duration and reference-image limits, dialogue pacing warnings, and outputs an upfront credit + USD cost estimate. Fix all errors (exit code 0) before proceeding.

### 4. Execute assets → draft render → review board → 1080p finalize

```bash
export HOTAPI_KEY="your_hotapi_api_key"

# 1. Generate or upload locked asset images (skips already-locked assets on rerun)
python3 scripts/storyboard_runner.py assets storyboard.json --out-dir ./out

# 2. Render 480p draft previews (or pass --resolution 720p without --draft)
python3 scripts/storyboard_runner.py render storyboard.json --out-dir ./out --draft

# 3. Build self-contained offline review board
python3 scripts/storyboard_runner.py board storyboard.json --out-dir ./out

# 4. After reviewing ./out/board.html, promote approved drafts to 1080p
python3 scripts/storyboard_runner.py finalize storyboard.json --out-dir ./out --only seg_01,seg_02
```

Use `--dry-run` on `assets`, `render`, or `finalize` to inspect exact HTTP endpoints and payloads without `HOTAPI_KEY` or credit spend.

## Hard integration rules

1. **Secrets boundary**: Read `HOTAPI_KEY` strictly from the environment. Never commit keys, write them to `state.json`, or echo them in logs.
2. **Idempotent submissions**: Send a deterministic `Idempotency-Key` per action + spec hash so retries never double-bill.
3. **Persist before polling**: Write every returned task `id` into `<out-dir>/state.json` immediately after `POST`, before polling `GET /v1/tasks/{id}`. Stop polling on `succeeded`, `failed`, `cancelled`, or `expired`.
4. **Durable downloads & upload freshness**: Download every asset and video locally before HotAPI's `expires_at` deadline. When passing local asset files to `render`, re-upload via `POST /v1/uploads` automatically if a cached upload URL is within 300s of expiry.
5. **Zero-credit CI**: Keep automated tests strictly against a local mock HTTP server (`test_storyboard_runner.py`). Never spend live credits in tests.
