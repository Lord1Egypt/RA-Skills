---
name: volcengine-video-studio
description: Production-ready Volcengine/ARK video generation for prompt-to-video, image-to-video, and draft-video refinement. Use when users want a hands-on skill that can submit jobs, poll status, inspect task payloads, and download finished outputs with Seedance-compatible models. 中文：适合火山引擎 / ARK 兼容接口的视频生成实战工作流；支持文生视频、图生视频、草稿视频优化、任务提交与轮询、结果检查和成片下载。
---

# volcengine-video-studio

Use this skill to actually submit, poll, inspect, and download Volcengine / ARK video generation jobs instead of only drafting prompts.

## 中文说明

这是一个面向 **火山引擎 / ARK 兼容视频生成接口** 的生产可用型 skill，重点不是只写视频提示词，而是把整条生成链路真正跑通，从提交任务、轮询状态，到拿回结果、下载成片，都能一把做完。

它特别适合下面这些对外场景：

- 文生视频
- 图生视频
- 草稿视频二次优化
- 提交生成任务并持续轮询状态
- 检查任务返回内容与原始 payload
- 将生成好的视频自动下载到本地

如果你想要的是一个**能真实发起任务、能追踪任务进度、能拿到最终视频文件、适合实战交付**的火山视频 skill，这个版本就是为这种需求准备的。

Treat the prompt and optional reference media as runtime input for each task. Do not reuse documentation example prompts or example media in a real generation request unless the user explicitly asks for that exact example.

## What this skill is good at

- text-to-video from a task-specific prompt
- image-to-video using a local file, data URL, or remote image URL
- draft-video refinement with a guiding prompt
- polling existing tasks and downloading finished outputs
- switching between a faster default model and a stronger alternate model

## Default path

Run the bundled script with the actual prompt for the current task:

```bash
python3 scripts/generate_video.py "当前任务的实际视频提示词"
```

To switch to the alternate model for one run:

```bash
VOLCENGINE_VIDEO_MODEL=doubao-seedance-1-5-pro-251215 \
python3 scripts/generate_video.py "当前任务的实际视频提示词"
```

By default the script:

- submits the task
- polls until the task finishes
- extracts returned video URLs from the task payload
- downloads generated files into `~/Desktop/volcengine-videos/<timestamp>-<slug>/`

## Required config

The script reads config from env vars:

- `VOLCENGINE_API_KEY` or `ARK_API_KEY`
- `VOLCENGINE_VIDEO_MODEL` (recommended)
- `VOLCENGINE_VIDEO_ENDPOINT` or `VOLCENGINE_ENDPOINT` or `ARK_BASE_URL`

Recommended video models:

- `doubao-seedance-1-0-pro-fast-251015` — default, faster iteration
- `doubao-seedance-1-5-pro-251215` — alternate higher-tier option

Default behavior:

- if `VOLCENGINE_VIDEO_MODEL` is unset, the script defaults to `doubao-seedance-1-0-pro-fast-251015`
- avoid relying on `VOLCENGINE_MODEL` for video runs when that env var is also used for image generation

Typical endpoint:

- `https://ark.cn-beijing.volces.com/api/v3`

The script calls:

- `POST /contents/generations/tasks`
- `GET /contents/generations/tasks/{task_id}`

## Common workflows

### 1. Text to video

```bash
python3 scripts/generate_video.py "为当前需求编写的视频提示词" \
  --ratio 16:9 \
  --duration 5
```

### 2. Image to video

```bash
python3 scripts/generate_video.py "描述你希望图片如何动起来" \
  --image ~/Desktop/reference.png \
  --ratio 9:16 \
  --duration 5
```

### 3. Draft/sample video to final video

```bash
python3 scripts/generate_video.py "说明要保留什么、增强什么" \
  --video ~/Desktop/draft.mp4
```

### 4. Inspect an existing task only

```bash
python3 scripts/generate_video.py --task-id <task_id> --wait false
```

### 5. Submit only, do not wait

```bash
python3 scripts/generate_video.py "当前任务的实际视频提示词" \
  --ratio 16:9 \
  --wait false
```

### 6. Use raw content JSON when the target model needs a custom body

```bash
python3 scripts/generate_video.py --content-json '[
  {"type":"text","text":"当前任务的实际视频提示词"},
  {"type":"image_url","image_url":{"url":"https://example.com/reference.png"}}
]'
```

## Local media support

For `--image` and `--video`:

- local file path → converted to `data:` URL automatically
- `https://...` URL → sent as-is
- `data:...` URL → sent as-is

This makes local reference media usable without manual upload steps.

## Key options

- `--ratio 16:9|9:16|1:1|adaptive`
- `--duration <seconds>`
- `--frames <count>`
- `--seed <int>`
- `--resolution <value>`
- `--camera-fixed true|false`
- `--watermark true|false`
- `--callback-url <https-url>`
- `--poll-interval <seconds>`
- `--timeout <seconds>`
- `--download-results true|false`
- `--download-dir <path>`
- `--print-request`

## Execution checklist

1. Confirm whether the user wants text-to-video, image-to-video, or draft-video refinement.
2. Treat the prompt as task-specific runtime input; never carry over example prompt text or example media into a real run unless explicitly requested.
3. Choose prompt-first mode by default; use `--content-json` only when the API shape must be customized.
4. Pass local reference media directly with `--image` or `--video`.
5. Prefer `--duration` for whole-second clips and `--frames` only when finer control is required.
6. Poll by default so the final answer includes actual output URLs or downloaded files.
7. Mention the saved file paths when downloads are enabled.
8. If the API returns an unexpected structure, surface the raw JSON instead of guessing.

## Troubleshooting

- Missing key → set `VOLCENGINE_API_KEY`
- Missing or wrong model → set `VOLCENGINE_VIDEO_MODEL`
- If a video run accidentally picks an image model (for example `doubao-seedream-4-5`) → explicitly set `VOLCENGINE_VIDEO_MODEL` instead of reusing `VOLCENGINE_MODEL`
- Missing endpoint → set `VOLCENGINE_VIDEO_ENDPOINT`
- 401/403 → key invalid or missing permission
- 404 → endpoint wrong or region mismatch
- 400 → unsupported model/parameter combination
- Task remains queued too long → check quota, rate limit, or model availability
- No obvious video URL in response → inspect `raw`

## References

- `references/sources.md`
- `references/api-notes.md`
ing `VOLCENGINE_MODEL`
- Missing endpoint → set `VOLCENGINE_VIDEO_ENDPOINT`
- 401/403 → key invalid or missing permission
- 404 → endpoint wrong or region mismatch
- 400 → unsupported model/parameter combination
- Task remains queued too long → check quota, rate limit, or model availability
- No obvious video URL in response → inspect `raw`

## References

- `references/sources.md`
- `references/api-notes.md`
