# CapCut MCP Server Reference

> Protocol: MCP (stdio) | 11 tools available

## Setup

```json
{
  "mcpServers": {
    "capcut-api": {
      "command": "python3.10",
      "args": ["mcp_server.py"],
      "cwd": "/path/to/CapCutAPI-dev",
      "env": {
        "PYTHONPATH": "/path/to/CapCutAPI-dev"
      }
    }
  }
}
```

## Tool Reference

### create_draft
Create a new video project. Returns `draft_id`.
```json
{"width": 1920, "height": 1080}
```

### get_video_duration
Get the duration of a video file in seconds.
```json
{"video_url": "/absolute/path/to/video.mp4"}
```

### add_video
Add a video segment to the timeline.
```json
{
  "draft_id": "dfd_cat_xxx",
  "video_url": "/path/to/video.mp4",
  "start": 12.5,
  "end": 28.3,
  "volume": 1.0
}
```
Set `volume: 0.0` to mute (for silent segments where narration replaces audio).
Set `volume: 1.0` to keep original audio (`keep_original_audio: true`).

### add_audio
Add narration or background audio.
```json
{
  "draft_id": "dfd_cat_xxx",
  "audio_url": "/path/to/narration_001.mp3",
  "start": 4.2,
  "end": 6.2,
  "volume": 1.0
}
```

### add_subtitle
Add an SRT subtitle file to the project.
```json
{
  "draft_id": "dfd_cat_xxx",
  "srt_path": "/path/to/subtitles.srt",
  "font_style": "default",
  "position": "bottom"
}
```

### add_text
Add a text overlay (used for narration cards on silent segments).
```json
{
  "draft_id": "dfd_cat_xxx",
  "text": "[Alex walks to the whiteboard]",
  "start": 4.2,
  "end": 6.2,
  "font_size": 36,
  "font_color": "#FFFFFF",
  "shadow_enabled": true,
  "shadow_color": "#000000",
  "shadow_alpha": 0.8,
  "background_color": "#1E1E1E",
  "background_alpha": 0.6,
  "background_round_radius": 10
}
```

### add_effect
Add visual effects to a segment.
```json
{
  "draft_id": "dfd_cat_xxx",
  "effect_type": "fade_in",
  "parameters": {},
  "duration": 0.3
}
```

### add_image / add_sticker / add_video_keyframe
See the CapCut MCP server documentation for full parameter reference.

### save_draft
Finalize and save the project. Must be called last.
```json
{"draft_id": "dfd_cat_xxx"}
```

## Return Format
```json
{
  "success": true,
  "result": {
    "draft_id": "dfd_cat_xxx",
    "draft_url": "https://..."
  }
}
```
