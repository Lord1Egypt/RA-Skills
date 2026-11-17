# Video translation: translate_video

Task type: `VIDEO_VOICE_OVER_TASK`. Mode: `async`; actual behavior and account access depend on the response.

[API reference](https://vibbit.apifox.cn/515705766e0)

Set auto_translate explicitly. With auto_translate=false, query the returned task until task_result.result exposes the safe review details and phase before editing or confirming.

This Skill currently supports ordinary subtitles and ordinary packaging templates. Dynamic subtitle templates are temporarily unavailable: both task and video settings reject `template_type=1` and `subtitle_template_configs`, including known template IDs.

## Inputs

Client fields and minimum requirements follow; the server may impose additional checks.

| Field | Type | Required |
| --- | --- | --- |
| `business_id` | id | No |
| `task_name` | string | No |
| `source_language` | string | No |
| `target_language` | string | No |
| `translation_style` | string | No |
| `default_speed` | number | No |
| `auto_translate` | boolean | Yes |
| `subtitle_enabled` | boolean | No |
| `lip_sync_enabled` | boolean | No |
| `remove_subtitles_enabled` | boolean | No |
| `persona_mode` | string | No |
| `template_type` | integer | No |
| `template_configs` | objects | No |
| `default_digital_human_id` | id | No |
| `default_prompt` | string | No |
| `settings` | object | No |
| `items` | objects | Yes |

Replace example URLs/IDs with real accessible assets and resources before submitting.

~~~json
{
  "auto_translate": true,
  "target_language": "en",
  "items": [
    {
      "source_video": {
        "url": "https://example.com/source.mp4"
      }
    }
  ]
}
~~~

## Call

~~~bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" translate_video --input /absolute/path/request.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" translate_video --input /absolute/path/request.json
~~~

The client sends a native object in `input_info.input`. Do not change encoding and automatically resubmit after an error.



[Authentication](../runtime/authentication.md) · [Task lifecycle](../runtime/task-lifecycle.md) · [Troubleshooting](../runtime/troubleshooting.md)

## Input constraints and defaults

| Field | Rules |
| --- | --- |
| items | 1-100 objects; source_video.url is the only mandatory source-media field |
| auto_translate | Explicit boolean required by client; true for automatic output, false for manual review (service default false) |
| source_language / target_language | At most 32 characters; service defaults auto / zh-CN. Always set the user's requested language explicitly |
| task_name / translation_style | At most 200 / 64 characters; service defaults describe video translation / natural conversational style |
| default_speed | Finite 0.5-3.0, service default 1.0; client rejects out-of-range values rather than silently clamping |
| subtitle_enabled | Default true; burn in target-language subtitles |
| lip_sync_enabled / remove_subtitles_enabled | Default false; enable only as needed |
| persona_mode | voice-only (default) or with-avatar; lip_sync_enabled still controls lip sync |
| business_id / default_digital_human_id | Existing project/avatar IDs; positive signed long |
| default_prompt | At most 10000 characters |
| settings | Use only documented extension keys; direct fields win. No template contents or selection fields here |
| template_type | Only 0 ordinary packaging is currently supported; omit when no template is chosen |
| template_configs | Ordinary template candidates containing only template_id |

Use canonical fields from describe, not aliases, embedded task_id, or retired subtitle_template_ids. Offline validation does not prove account access, target-language support, or media reachability/encoding.

Each source_video may supply real file_name, file_size (bytes), file_type, mime_type, upload_time, duration (seconds), width, height, frame_rate, video_codec, audio_codec, container_format. Omit unavailable metadata; do not insert zero placeholders.

Items may include material_id, digital_human_id, prompt (up to 10000 characters), and settings. Omitted target_languages inherits the parent language; if supplied it contains 1-16 nonempty language codes, each up to 32 characters. Items can override subtitle_enabled, lip_sync_enabled, remove_subtitles_enabled, and template selection fields. Empty/omitted templates follow service inheritance; an empty array does not establish that a parent template was cleared.

voice_over_clips is an object array with from/to (seconds), text, audio_url, speed, keep_original_voice, lip_sync, lip_sync_video_url. Use only for requested preset clips with real inputs; it is not a voice-cloning or arbitrary voice-selection API.

## Templates and integer precision

Use template_type=0 and template_configs for ordinary packaging, with at most 100 candidates containing only a positive template_id. No background, watermark, cover, or track-editing fields are accepted. Changing templates after submission needs a new task and must not silently incur another charge.

Supply large IDs as decimal strings, e.g. "2100065567327711232" (example only). The client preserves precision and sends exact JSON integer tokens for long fields. It also preserves large numeric tokens in input files. Do not round them in another parser.

Dry-run body keeps large IDs as safe display strings; body_json contains exact wire serialization. Do not re-encode the display object to replace the client request.

## Results and review

Query the original ID every 5-10 seconds, with 50-second waits by default. Creation is not automatically retried. Progress counts both successful and failed items; 100% does not mean all succeeded.

Parse task_result.result. Prefer results_by_language[language].output_video_url; use the item's output_video_url only where no language map exists. Never substitute source/intermediate videos for missing final output.

FAILED/INSUFFICIENT_POINTS parents retain successful videos. Partial success exits 5; no deliverable/all failed exits 1. Journals keep source-URL hashes and expected languages, not raw URLs, translations, or keys. Resume checks coverage. Direct status lacks original expectations; ambiguous/duplicate sources may produce requested_languages_checked=false, requiring comparison to the original request.

Manual mode hands control back rather than waiting ten minutes. Review phases/details become review when returned by the task query. Allowed fields include phase, languages, video items, sub_task_id, child status, source URLs, ASR, translations, storyboards, and errors. review_visibility=available means actual details were returned; unavailable means query later or obtain review context. It does not mean review passed.

Use [translation review](../capabilities/processing/video-translation.md), [edit](update_translation.md), and [approve](confirm_translation.md). Invalid JSON is a protocol error, not something to silently repair into success. Inspect final language, media availability, and quality.

[Result reference](https://vibbit.apifox.cn/515706553e0).
