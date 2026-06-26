---
name: runninghub-video
description: Use RunningHub official standard-model APIs for image-to-video generation. Trigger when the user asks to use RunningHub, 可灵, Seedance, 万相, or other RunningHub video endpoints to turn one image or start/end frames into a video, especially when local files need to be uploaded first, tasks need polling via `/openapi/v2/query`, or completed videos should be downloaded automatically.
---

# RunningHub Video

Use this skill to submit image-to-video jobs to RunningHub, poll task status, and download the finished video locally.

## Quick Start

1. Confirm the user wants RunningHub image-to-video rather than HTML/CSS animation or local FFmpeg edits.
2. Use `scripts/runninghub_video.py` instead of hand-writing `curl` unless the user explicitly asks for raw API calls.
3. Accept either:
   - a public image URL
   - a local image path that should be uploaded through RunningHub's binary upload endpoint first
4. Wait for `/openapi/v2/query` unless the user explicitly asks for submit-only behavior.
5. Download the returned media immediately because RunningHub-hosted outputs and uploaded media links can expire.

## Default Workflow

### 1. Pick the model

Use these stable shortcuts unless the user names a different endpoint:

- `wan-2.2`: default choice for general image-to-video generation in this skill
- `kling-v3.0-std`: strong alternative for high-quality single-image or start/end-frame generation
- `seedance-2.0-global`: quality-oriented alternative with resolution and audio switches
- `seedance-2.0-global-fast`: faster/cheaper Seedance variant
- `wan-2.2`: Wan 2.2 image-to-video endpoint with RunningHub's numeric field names

### 2. Prepare the inputs

- If the user provides a local file path, pass it directly to the script. The script uploads it to `POST /openapi/v2/media/upload/binary` and reuses the returned `download_url`.
- If the user provides a public URL or a `data:` URI, pass it through unchanged.
- If the user wants stronger transition control and the chosen model supports it, include an end frame.

### 3. Submit and wait

Run the helper from the skill directory:

```powershell
python "C:\Users\Administrator\.codex\skills\runninghub-video\scripts\runninghub_video.py" `
  --image "C:\path\to\start.png" `
  --prompt "镜头缓慢推进，人物抬头微笑，风吹动头发" `
  --out-dir "C:\path\to\outputs"
```

For start/end frame generation:

```powershell
python "C:\Users\Administrator\.codex\skills\runninghub-video\scripts\runninghub_video.py" `
  --image "C:\path\to\start.png" `
  --end-image "C:\path\to\end.png" `
  --prompt "从平静站立过渡到转身回望，镜头平滑推进" `
  --duration 5 `
  --out-dir "C:\path\to\outputs"
```

### 4. Return useful output

When you finish, report:

- which model/endpoint was used
- the `taskId`
- whether local images were uploaded first
- the saved output path(s)
- any prompt or parameter choices worth remembering

## Command Patterns

### Kling 3.0 std

```powershell
python "C:\Users\Administrator\.codex\skills\runninghub-video\scripts\runninghub_video.py" `
  --model kling-v3.0-std `
  --image "C:\path\to\image.png" `
  --prompt "电影感镜头，小幅推近，人物表情逐渐变化" `
  --duration 5 `
  --cfg-scale 0.8 `
  --sound true
```

### Seedance 2.0 global

```powershell
python "C:\Users\Administrator\.codex\skills\runninghub-video\scripts\runninghub_video.py" `
  --model seedance-2.0-global `
  --image "C:\path\to\image.png" `
  --prompt "书页翻动时，文字化作发光蝴蝶飞散" `
  --resolution 720p `
  --ratio adaptive `
  --audio true `
  --real-person-mode true
```

### Wan 2.2

```powershell
python "C:\Users\Administrator\.codex\skills\runninghub-video\scripts\runninghub_video.py" `
  --image "C:\path\to\image.png" `
  --prompt "产品绕镜头缓慢旋转，补光扫过金属表面" `
  --duration 5 `
  --wan-resolution auto
```

## Parameters Worth Tuning

- `--prompt`: motion, camera movement, atmosphere, and audio intent
- `--duration`: model-specific duration string; keep it to values shown in the official endpoint docs
- `--end-image`: use when the endpoint supports start/end-frame control
- `--out-dir`: always set an explicit output directory for easier follow-up work
- `--submit-only`: use when the user wants a task id without waiting
- `--poll-interval` and `--timeout`: useful for long renders

## Troubleshooting

- If upload fails, verify the local file exists and the API key is valid.
- If the task returns moderation or content-verification errors, keep the same image but soften the prompt or remove risky wording.
- If the task succeeds but no download happens, inspect the raw query response and the returned `results` array.
- If the user asks for a model not covered by the helper yet, read [references/api_reference.md](references/api_reference.md), then extend the script instead of crafting a one-off request.

## References

- Read [references/api_reference.md](references/api_reference.md) for the exact endpoints, payload shapes, and polling behavior used by this skill.
