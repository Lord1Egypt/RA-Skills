# vectcut-api Reference

> Version: v1.0 | Default address: http://localhost:8765

---

## Starting the Service

```bash
pip install vectcut-api --break-system-packages
vectcut-api serve --port 8765
# Verify: curl http://localhost:8765/health
```

---

## POST /api/v1/generate — Generate CapCut Draft

### Request Body

```json
{
  "project_name": "My Clip Project",
  "video_path": "/absolute/path/to/video.mp4",
  "clips": [
    {
      "clip_id": "clip_001",
      "start_time": 12.5,
      "end_time": 28.3,
      "subtitles": [
        {"start": 12.5, "end": 15.2, "text": "First line of dialogue"},
        {"start": 15.2, "end": 18.0, "text": "Second line of dialogue"}
      ]
    }
  ],
  "options": {
    "subtitle_style": "default",
    "subtitle_position": "bottom",
    "font_size": 36,
    "transition": "none",
    "bgm_path": null,
    "bgm_volume": 0.3,
    "output_resolution": "1080p",
    "output_format": "draft_json"
  }
}
```

### Enum Values

**subtitle_style:** `default` (white text, black outline) | `highlight` (yellow background) | `card` (semi-transparent black box) | `none`

**subtitle_position:** `bottom` | `top` | `center`

**transition:** `none` | `fade` | `slide_left` | `slide_right` | `zoom`

**output_resolution:** `1080p` (1920×1080) | `720p` | `portrait_1080p` (1080×1920 vertical, TikTok-ready) | `portrait_720p`

**output_format:** `draft_json` (CapCut) | `premiere_xml` (Adobe Premiere)

### Success Response

```json
{
  "success": true,
  "draft_path": "/tmp/vectcut_output/draft_content.json",
  "draft_content": { "...CapCut draft object..." },
  "meta": {
    "clip_count": 5,
    "total_duration": 222.5,
    "subtitle_count": 38
  }
}
```

### Error Response

```json
{
  "success": false,
  "error_code": "VIDEO_NOT_FOUND",
  "error_message": "Video file does not exist"
}
```

---

## GET /api/v1/health

```json
{"status": "ok", "version": "1.0.0"}
```

## GET /api/v1/styles

Returns all available subtitle styles with preview image URLs.

---

## Python Helper Function

```python
import requests, json
from pathlib import Path

def call_vectcut_api(video_path, clips, project_name="My Project",
                     subtitle_style="default", transition="none",
                     output_resolution="1080p", api_base="http://localhost:8765"):
    # Health check
    try:
        r = requests.get(f"{api_base}/api/v1/health", timeout=5)
        assert r.json()["status"] == "ok"
    except Exception as e:
        raise RuntimeError(f"vectcut-api is unavailable. Please start the service first: {e}")

    payload = {
        "project_name": project_name,
        "video_path": str(Path(video_path).resolve()),
        "clips": clips,
        "options": {
            "subtitle_style": subtitle_style,
            "subtitle_position": "bottom",
            "font_size": 36,
            "transition": transition,
            "bgm_path": None,
            "output_resolution": output_resolution,
            "output_format": "draft_json"
        }
    }

    resp = requests.post(f"{api_base}/api/v1/generate", json=payload, timeout=60)
    resp.raise_for_status()
    result = resp.json()

    if not result["success"]:
        raise RuntimeError(f"{result['error_code']}: {result['error_message']}")

    out = "draft_content.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(result["draft_content"], f, ensure_ascii=False, indent=2)

    return result, out
```

---

## Error Codes

| error_code | Meaning | Resolution |
|-----------|---------|-----------|
| `VIDEO_NOT_FOUND` | Video path does not exist | Check the absolute path |
| `INVALID_CLIP_TIME` | Timestamp exceeds video duration | Verify start/end values |
| `UNSUPPORTED_FORMAT` | Unsupported video format | Convert to mp4 with ffmpeg |
| `SUBTITLE_OVERLAP` | Subtitle timestamps overlap | Check segment merge logic |
| `SERVICE_ERROR` | Internal service error | Check vectcut-api logs |
