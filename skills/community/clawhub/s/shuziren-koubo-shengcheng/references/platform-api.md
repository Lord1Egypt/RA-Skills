# Platform API Reference

This skill talks to this project's platform API with either:

```text
X-API-Token: <CHANJING_PLATFORM_API_TOKEN>
```

Or the legacy pair:

```text
X-API-Key: <CHANJING_PLATFORM_API_KEY>
X-API-Secret: <CHANJING_PLATFORM_API_SECRET>
```

## Endpoints

### Public resources

- `GET /api/openclaw/public-digital-humans`
- `GET /api/openclaw/public-voices`
- `GET /api/openclaw/fonts`

### Owned resources

- `GET /api/openclaw/digital-humans/mine`
- `GET /api/openclaw/voices/mine`
- `GET /api/openclaw/videos/mine`

### Training and synthesis

- `POST /api/openclaw/digital-humans/train`
- `POST /api/openclaw/voices/train`
- `POST /api/openclaw/videos/talking-head`

### Tasks

- `GET /api/openclaw/tasks/{task_id}`
- `POST /api/openclaw/tasks/{task_id}/sync`

## Video Synthesis Contract

Required fields:
- `title`
- `digital_human_id`
- one audio source:
  - TTS: `script`
  - Audio drive: `audio_file_id` or `audio_url`

Optional fields:
- `voice_id`
- `background_file_id`
- `background_url`
- `video_width`
- `video_height`
- `callback_url`
- `extra_payload`
- subtitle-related fields
- rendering-related fields

## Defaulting Policy

When optional fields are omitted, the platform API should supply its own defaults and then submit to Chanjing.

Current important defaults on the platform side:
- TTS `voice_speed`: defaults to `1.0`
- TTS `voice_volume`: defaults to `100`
- TTS `voice_language`: defaults to `"cn"`
- `background_color`: defaults to `#EDEDED`
- `video_width`: defaults to `1080`
- `video_height`: defaults to `1920`
- `add_compliance_watermark`: defaults to `false`
- If subtitle is enabled and `subtitle_font_type` is omitted, the platform tries to use `思源宋体 CN`
- If subtitle is enabled and `subtitle_border_width` is omitted, the platform defaults it to `2`
- If no background is provided, the platform auto-generates a white PNG background
- If TTS is used and `voice_id` is omitted, the platform tries to resolve the trained digital human's bound `audio_man_id`

## Subtitle Font Selection

To let the user choose a subtitle font:
1. Call `GET /api/openclaw/fonts`
2. Show the returned `id`, `name`, `preview`, `ttf_path`
3. Pass the selected font `id` as `subtitle_font_type`

## Notes

- `subtitle_show` enables subtitle config when synthesizing a video.
- Platform API request fields keep the `subtitle_*` names, then the backend maps them to Chanjing's upstream keys such as `font_id`, `color`, `stroke_color`, `stroke_width`, `subtitles`.
- Do not send `add_compliance_watermark` or `compliance_watermark_position` unless the user explicitly requests an AI compliance watermark.
- `subtitle_data_url` in task result is the subtitle timeline file returned by upstream.
- `is_rgba_mode=true` does not support subtitles or background.
