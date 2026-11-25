# Video translation: translate_video

Task type: `VIDEO_VOICE_OVER_TASK`. Mode: `async`; actual behavior and account access depend on the response.

[Complete translation contract](https://vibbit.apifox.cn/515706553e0) · [Creation](https://vibbit.apifox.cn/515705766e0). For voice changes, speech retries and language rendering, read [translation revisions](translation-revision.md).

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
| `align_original_subtitle_position` | boolean | No |
| `translate_and_align_original_title` | boolean | No |
| `persona_mode` | string | No |
| `template_type` | integer | No |
| `template_configs` | objects | No |
| `default_digital_human_id` | id | No |
| `default_prompt` | string | No |
| `default_voice` | object or null | No |
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
| align_original_subtitle_position | Default false; requires source-subtitle removal and enabled target subtitles |
| translate_and_align_original_title | Default false; requires source-subtitle removal and an existing enabled template title slot; target body subtitles may be disabled |
| persona_mode | voice-only (default) or with-avatar; lip_sync_enabled still controls lip sync |
| business_id / default_digital_human_id | Existing project/avatar IDs; positive signed long |
| default_prompt | At most 10000 characters |
| default_voice | Optional object or null; omit/null preserves the original flow. Set only for explicitly requested replacement after explaining its scope |
| settings | Use only documented extension keys; direct fields win. No template contents or selection fields here |
| template_type | Only 0 ordinary packaging is currently supported; omit when no template is chosen |
| template_configs | Ordinary template candidates containing only template_id |

Use canonical fields from describe, not aliases, embedded task_id, or retired subtitle_template_ids. Offline validation does not prove account access, target-language support, or media reachability/encoding.

Each source_video may supply real file_name, file_size (bytes), file_type, mime_type, upload_time, duration (seconds), width, height, frame_rate, video_codec, audio_codec, container_format. Omit unavailable metadata; do not insert zero placeholders.

Items may include material_id, digital_human_id, prompt (up to 10000 characters), and settings. Omitted target_languages inherits the parent language; if supplied it contains 1-16 nonempty language codes, each up to 32 characters. Items can override subtitle_enabled, lip_sync_enabled, remove_subtitles_enabled, and template selection fields. Empty/omitted templates follow service inheritance; an empty array does not establish that a parent template was cleared.

Both alignment switches also support video-level overrides: explicit false overrides the parent and omission inherits. Verify an actual enabled title slot rather than inventing one. Dynamic subtitle workflows remain disabled.

voice_over_clips is an object array with from/to (seconds), text, audio_url, speed, keep_original_voice, lip_sync, lip_sync_video_url. Use only for requested preset clips with real inputs; it is not a voice-cloning or arbitrary voice-selection API.

## Voice selection at creation

Preserve original voices by default, as in the example. Apply [voice intent and scope](../capabilities/processing/video-translation.md#voice-intent-and-scope) before adding this parent-level create field:

```json
{ "default_voice": { "reference_audio_url": "https://example.com/reference.mp3" } }
```

It applies to ALL videos and target languages in this batch. Every speaker without a dedicated mapping uses this same voice; it does not select a detected person or sentence. Only reference_audio_url is supported, not audio_id or speaker_id. Never place it in settings, items or video settings. A non-null object must contain only that URL. The service trims surrounding whitespace; HTTP(S) URL paths must end in .mp3, case-insensitively, and may carry complete signed query parameters. Empty objects, blank URLs and non-MP3 paths are rejected.

Prepare local reference audio as an actual MP3 when needed and use [generic upload](upload_info.md) for its object_url before creation. Do not create an unnecessary translation task just to obtain the task-scoped audio-upload signature. Existing voice asset audio_id belongs only in operations accepting speaker mappings. The reference URL must remain valid through first dubbing and later retries.

Priority: dedicated speaker mapping, then default_voice, then the segment's original voice. This default is create-only; update_speaker_voices cannot modify or clear it. Clearing dedicated mappings falls back to this default when present. The creation contract documents parent/item query echoes; the client tolerates older responses without the field and retains only public reference_audio_url.

## Templates and integer precision

Use template_type=0 and template_configs for ordinary packaging, with at most 100 candidates containing only a positive template_id. No background, watermark, cover, or track-editing fields are accepted. Changing templates after submission needs a new task and must not silently incur another charge.

When the ID is missing, use [translation template selection](../resources/packaging-templates.md#translation-template-selection) to query `mixed_cut` / `video-editor`, include the account's visible scopes, paginate as needed, and inspect actual details. Query a supplied real ID directly. The list query's string template_type is not this operation's numeric template_type.

Supply large IDs as decimal strings, e.g. "2100065567327711232" (example only). The client preserves precision and sends exact JSON integer tokens for long fields. It also preserves large numeric tokens in input files. Do not round them in another parser.

Dry-run body keeps large IDs as safe display strings; body_json contains exact wire serialization. Do not re-encode the display object to replace the client request.

## Results and review

Public results also expose speaker_voice_mappings, resynthesis_by_language and per-language delivered media, voice_over_clips, subtitle_asr_sentences and translated_segments_snapshot. Current drafts can differ from old deliveries. from/to are seconds; subtitle begin_time/end_time are milliseconds. voice_reference_audio_url is the original voice reference, not a newly bound voice. Internal snapshots, vendor checkpoints and audio fingerprints are excluded from projected output.

For existing-video speech corrections, use [segment retries and language rendering](translation-revision.md) to reuse visuals and valid unaffected speech. Resume the operation journal to verify its exact business receipt; a plain parent status or old URL does not verify a new render.

Query the original ID every 5-10 seconds, with 50-second waits by default. Creation is not automatically retried. Progress counts both successful and failed items; 100% does not mean all succeeded.

Parse task_result.result. Prefer results_by_language[language].output_video_url; use the item's output_video_url only where no language map exists. Never substitute source/intermediate videos for missing final output.

FAILED/INSUFFICIENT_POINTS parents retain successful videos. Partial success exits 5; no deliverable/all failed exits 1. Journals keep source-URL hashes and expected languages, not raw URLs, translations, or keys. Resume checks coverage. Direct status lacks original expectations; ambiguous/duplicate sources may produce requested_languages_checked=false, requiring comparison to the original request.

Manual mode returns the required review context rather than blindly polling for human approval. Review phases/details become review when returned by the task query. Allowed fields include phase, languages, video items, sub_task_id, child status, source URLs, ASR, translations, storyboards, and errors. review_visibility=available means actual details were returned; unavailable means query later or obtain review context. It does not mean review passed.

Use [translation review](../capabilities/processing/video-translation.md), [edit](translation-review.md#update-translation), and [approve](translation-review.md#confirm-translation). Invalid JSON is a protocol error, not something to silently repair into success. Inspect final language, media availability, and quality.

[Result reference](https://vibbit.apifox.cn/515706553e0).
