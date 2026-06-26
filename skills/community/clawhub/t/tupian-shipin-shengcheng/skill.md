---
name: 图片视频生成
description: "可调用 banana、sora、veo 等模型生成图片视频，适合图片、视频与短剧素材生产。"
metadata: {"openclaw":{"requires":{"anyBins":["python","python3"]}}}
---

# Image And Video Generation Skill

Use this skill when OpenClaw should call this platform relay API for:
- VEO video models
- Banana image models
- Sora video models

Read these references before using the scripts:
- [references/setup.md](./references/setup.md)
- [references/platform-api.md](./references/platform-api.md)
- [references/model-guide.md](./references/model-guide.md)

## Environment

Preferred:
- `EASYCLAW_PLATFORM_API_TOKEN`

Compatible fallback:
- `CHANJING_PLATFORM_API_TOKEN`
- `EASYCLAW_PLATFORM_API_KEY`
- `EASYCLAW_PLATFORM_API_SECRET`
- `CHANJING_PLATFORM_API_KEY`
- `CHANJING_PLATFORM_API_SECRET`

Optional base URL override:
- `EASYCLAW_PLATFORM_BASE_URL`
- `CHANJING_PLATFORM_BASE_URL`

Important guidance:
- Always tell the user to get the platform token from `http://easyclaw.bar/shuziren/user/`
- The token is issued by this platform, not by the upstream provider
- The base URL defaults to `http://easyclaw.bar/shuzirenapi`
- Do not modify OpenClaw core code or `openclaw.json` to make this skill work

## Important Rules

- Only execute the provided Python scripts under `scripts/`
- Do not hand-write HTTP requests
- Do not probe unrelated platform routes such as `/api/me`, auth routes, or non-skill routes
- If a needed capability is not exposed by an existing script, update a script first
- Submit requests only through `scripts/generate_video.py`
- Query an existing task only through `scripts/fetch_video.py`
- `scripts/generate_video.py` must submit exactly one task for one user intent
- After submission, the skill must create the watcher in the same run unless the user explicitly asks for `--no-watch`
- The watcher must be implemented inside the skill scripts, not by modifying OpenClaw core behavior
- The watcher checks task status every 30 seconds by default
- Before creating the watcher, pass the current OpenClaw session binding to `scripts/generate_video.py` with `--notify-session-key`
- `--notify-session-key` may be either the real OpenClaw session key or the current delivery target such as `easyclaw:bot:11`
- Prefer the current session key from `session_status`; do not guess another session when the current one can be resolved
- When the task reaches a terminal state, the watcher must return the result and delete its own cron job
- If watcher creation fails, tell the user submission succeeded but automatic notification was not armed
- Do not promise automatic notification unless a non-empty watcher `job_id` is returned
- Do not claim there will be fallback polling or periodic checking unless that behavior is actually implemented and armed
- Pass only the parameters the user specified
- Prefer guided builder flags because they validate model-specific requirements and return clearer errors
- Use raw JSON or raw multipart mode only when the user needs fields not exposed by the guided builder

## Async Workflow

For VEO, Banana, and Sora generation:

1. Run `scripts/generate_video.py`
2. Let the script submit the request
3. Pass the current session binding with `--notify-session-key` so the watcher can write the final result back to the originating session
4. Let the script create the cron watcher in the same execution by default
5. Return the submission result and watcher state
6. The watcher will call `scripts/cron_watch_task.py` every 30 seconds
7. If the task is still running, the watcher returns exactly `NO_REPLY`
8. If the task succeeds or fails, the watcher writes the final result into the original session, returns `NO_REPLY`, and removes the cron job

Do not replace this with model-side polling or ad hoc direct requests.

## Script Selection

- Submit generation request: `scripts/generate_video.py`
- Query one task by id: `scripts/fetch_video.py`

## Submit Modes

`scripts/generate_video.py` supports:

- Guided builder mode
  - Use flags such as `--prompt`, `--reference-file`, `--image-url`, `--style`, `--size`, `--aspect-ratio`
  - This mode validates model-specific rules
  - Use `--list-models` or `--describe-model <model>` when guidance is needed

- JSON request mode
  - Use `--payload-json` or `--payload-file`
  - Use this when the upstream payload needs custom JSON fields

- Multipart form-data mode
  - Use repeated `--field name=value`
  - Use repeated `--file-field name=path`
  - Use this for local file uploads such as `input_reference`

Do not mix JSON payload args with multipart field args in one command.

## Model Usage

### VEO video models

Typical models:
- `veo_3_1-fast`
- `veo_3_1-fast-fl`
- `veo_3_fast`
- `veo_3`

Rules:
- `veo_3_1-fast` supports text-to-video and reference-image video with up to 3 images
- `veo_3_1-fast-fl` requires 1 or 2 images
- If the user selects `veo_3_1-fast-fl` and does not provide the required images, stop and tell them exactly what is missing
- VEO JSON mode does not accept HTTP image URLs for `input_reference`; use local files or Base64 JSON in raw mode

### Banana image models

Standard Banana:
- `nano_banana_2`
- `nano_banana_pro`
- `nano_banana_pro-1K`
- `nano_banana_pro-2K`
- `nano_banana_pro-4K`

Gemini Banana:
- `nano_banana_2-landscape`
- `nano_banana_2-portrait`
- `nano_banana_pro-1K-landscape`
- `nano_banana_pro-1K-portrait`
- `nano_banana_pro-2K-landscape`
- `nano_banana_pro-2K-portrait`
- `nano_banana_pro-4K-landscape`
- `nano_banana_pro-4K-portrait`

Rules:
- Standard Banana uses `prompt` plus optional `metadata`
- Gemini Banana uses `contents` plus `generationConfig`
- Guided builder mode supports both families and performs basic validation

### Sora video models

Typical models:
- `sora-2-landscape-10s`
- `sora-2-portrait-10s`
- `sora-2-landscape-15s`
- `sora-2-portrait-15s`
- `sora-2-pro-landscape-25s`
- `sora-2-pro-portrait-25s`
- `sora-2-pro-landscape-hd-15s`
- `sora-2-pro-portrait-hd-15s`

Rules:
- Prompt is required
- `image_url` and local `input_reference` are mutually exclusive
- Use raw JSON or raw multipart when extra provider-specific fields are required

## Examples

Print the built-in model guide:

```bash
python "{baseDir}/scripts/generate_video.py" --list-models
```

Describe one model:

```bash
python "{baseDir}/scripts/generate_video.py" --describe-model "veo_3_1-fast-fl"
```

Submit VEO with JSON:

```bash
python "{baseDir}/scripts/generate_video.py" --model "veo_3_1-fast" --payload-json "{\"model\":\"veo_3_1-fast\",\"prompt\":\"a cat running in snow\",\"size\":\"1920x1080\"}"
```

Submit VEO with local reference files:

```bash
python "{baseDir}/scripts/generate_video.py" --model "veo_3_1-fast" --prompt "animate this portrait" --reference-file "C:\path\reference1.jpg" --reference-file "C:\path\reference2.jpg"
```

Submit VEO start/end frame mode:

```bash
python "{baseDir}/scripts/generate_video.py" --model "veo_3_1-fast-fl" --prompt "animate between these two frames" --start-frame-file "C:\path\start.jpg" --end-frame-file "C:\path\end.jpg"
```

Submit Banana standard:

```bash
python "{baseDir}/scripts/generate_video.py" --model "nano_banana_pro" --prompt "a coffee cup on a wooden desk" --aspect-ratio "1:1" --reference-url "https://example.com/ref.png"
```

Submit Gemini Banana:

```bash
python "{baseDir}/scripts/generate_video.py" --model "nano_banana_2-landscape" --prompt "a futuristic city skyline"
```

Submit Sora with image URL:

```bash
python "{baseDir}/scripts/generate_video.py" --model "sora-2-landscape-10s" --payload-json "{\"model\":\"sora-2-landscape-10s\",\"prompt\":\"turn this into a cinematic teaser\",\"image_url\":\"https://example.com/source.png\",\"style\":\"cinematic\"}"
```

Submit only without watcher:

```bash
python "{baseDir}/scripts/generate_video.py" --model "veo_3_1-fast" --payload-file "C:\path\payload.json" --no-watch
```

Query an existing task:

```bash
python "{baseDir}/scripts/fetch_video.py" --task-id "task_123"
```
