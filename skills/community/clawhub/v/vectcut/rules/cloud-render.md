---
name: cloud-render
description: Render a VectCut draft into a playable/downloadable video via the cloud rendering API. Use this skill whenever the user wants to render a draft, export a draft to video, generate a video from a draft ID, or mentions cloud rendering. Also trigger when the user says "render this draft", "export video", "generate video from draft", or similar rendering-related requests.
---

# Cloud Render Skill

Submit a cloud rendering task to the VectCut backend, poll for completion, and return a playable/downloadable video URL.

API documentation:
- Generate video: https://s37mlnofqq.apifox.cn/416815247e0
- Task status: https://docs.vectcut.com/321247406e0

## When to use

- User wants to render/export a draft into a video
- User provides a draft ID and wants a video URL
- User mentions cloud rendering, video export, or draft rendering

## Workflow

### Prerequisites

- Python 3 with `requests` library installed
- Check `VECTCUT_API_KEY` before execution; if missing, call `vectcut-login` first and continue only after login succeeds

### Execution

Run the render script with the draft ID:

```bash
python <skill-path>/scripts/cloud_render.py "<draft_id>"
```

Optional arguments for resolution and framerate:

```bash
python <skill-path>/scripts/cloud_render.py "<draft_id>" [resolution] [framerate]
```

- `resolution`: 480P / 720P (default) / 1080P / 2K / 4K
- `framerate`: 24 (default) / 25 / 30 / 50 / 60

### What the script does

1. **Submit** — `POST /cut_jianying/generate_video` with `draft_id`, optional `resolution` and `framerate`. The backend returns a `task_id`.

2. **Poll** — `POST /cut_jianying/task_status` with `task_id`, polling every 5 seconds until the task reaches `SUCCESS` or `FAILURE`.

   Status flow: `PENDING` → `DOWNLOADING` → `PROCESSING` → `EXPORTING` → `UPLOADING` → `SUCCESS`

3. **Result** — On success, the response contains a `result` field with the video URL (playable and downloadable).

### Output

The script prints a JSON object on success:

```json
{
  "draft_id": "dfd_cat_1765957250_ba36ded9",
  "task_id": "6c653617-8133-4c51-8bd0-8635e9e25879",
  "status": "SUCCESS",
  "video_url": "http://player.install-ai-guider.top/dfd_xxx.mp4?..."
}
```

The `video_url` can be opened in a browser to play or download the rendered video.

### Error handling

- If `VECTCUT_API_KEY` is not set, call `vectcut-login` first, then rerun this skill
- If the task fails, the script prints the error message from the backend
- If polling times out (default 10 minutes), the script exits with a timeout error

### Configuration

| Parameter | Source | Value |
|-----------|--------|-------|
| API Key | Env var `VECTCUT_API_KEY` | (required) |
| Backend URL | Hardcoded | `https://open.vectcut.com` |
| Poll interval | Hardcoded | 5 seconds |
| Timeout | Hardcoded | 600 seconds (10 min) |
