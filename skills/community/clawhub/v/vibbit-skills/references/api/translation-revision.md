# Translation voices, segment speech retries, and language rendering

[Public contract](https://vibbit.apifox.cn/515706553e0). These commands modify an existing VIDEO_VOICE_OVER_TASK; they do not create a new parent or change the visible performer. First delivery still uses [creation](translate_video.md) and [storyboard confirmation](translation-review.md#confirm-translation).

Query the real parent first for its subtask, languages, ASR speakers, current draft, voice mappings and phase. Continue within the user's existing revision authorization without another approval. Voice updates and segment retries allow TRANSLATION_REVIEW, STORYBOARD_REVIEW, COMPLETED (historical GENERATED), or RENDERING while siblings run. The selected subtask must be COMPLETED with no active language render. The service validates phases and asset access.

## Change a speaker's voice

Input for `update_speaker_voices`; replace example IDs and URLs with actual values:

```json
{
  "sub_task_id": "2100065567327711232",
  "speaker_voice_mappings": [
    { "speaker_id": 0, "reference_audio_url": "https://example.com/reference.mp3" },
    { "speaker_id": 1, "audio_id": "2100065567327711233" }
  ]
}
```

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" update_speaker_voices --task-id task-RETURNED_NUMERIC_ID --input /absolute/path/voices.json --dry-run
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" update_speaker_voices --task-id task-RETURNED_NUMERIC_ID --input /absolute/path/voices.json --submission-id SAVED_VOICE_OPERATION
```

The array **replaces all bindings**, with 0–100 entries. Preserve every existing binding still needed; a one-speaker change is not an array patch. `[]` clears dedicated bindings. It restores source voices only when no default_voice exists; otherwise speakers fall back to that global voice. Use real, unique ASR speaker_id values; null is reserved for a historical unnumbered default group. Each entry chooses either an accessible voice asset audio_id or an HTTP(S) reference_audio_url whose path ends in `.mp3`; query parameters are allowed. Material IDs and an avatar's voice field are not interchangeable with voice asset IDs.

Follow [voice intent and scope](../capabilities/processing/video-translation.md#voice-intent-and-scope); default to preserving voices. Read parent/item default_voice first. Dedicated mappings take precedence over the global default, then source voices; speech retries retain this priority. The global default is create-only and cannot be changed or cleared by this endpoint. If the user wants source voices back while a global default remains, explain the limitation and assess the next route. Do not report success after merely clearing mappings or silently recreate the whole paid batch.

Saving does not run TTS or render. A real configuration change invalidates old previews across all languages of this video while preserving delivered videos. During first review, save and confirm the storyboard. After delivery, retry affected speech and render its language again. Derive affected languages and segments from real speakers/mappings, then check which other speech remains valid in the service draft; an old preview URL alone does not prove reuse is valid.

## Upload a reference MP3

Reuse an accessible MP3 URL directly. For a local file:

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" upload_reference_audio --task-id task-RETURNED_NUMERIC_ID --file /absolute/path/reference.mp3
```

The client GETs `/tasks/{taskId}/reference-audio/upload-signature`, uploads to OSS using the returned directory/policy, sets success_action_status=200 and puts the file last in multipart. Bind the returned reference_audio_url separately. Size and expiry follow the actual policy. Local extension/file checks do not verify codec, duration, sound or identity quality.

Uploading does not save a binding, generate speech or create a reusable voice asset. Without --file, only a non-sensitive instruction summary is returned, without temporary credentials. The signature GET uses the selected site's Key; OSS never receives the OpenAPI Bearer token. Existing exact storage-host, TLS, directory, policy and size checks remain enforced.

## Retry only incorrect speech segments

Input for `retry_segments`:

```json
{
  "sub_task_id": "2100065567327711232",
  "target_language": "en",
  "request_id": "retry-unique-001",
  "segments": [{ "id": "1", "translated_text": "Welcome to our new collection." }]
}
```

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" retry_segments --task-id task-RETURNED_NUMERIC_ID --input /absolute/path/retry.json --submission-id SAVED_RETRY_OPERATION
```

Send 1–100 existing, unique IDs and nonempty text; only id and translated_text belong in each entry. Timing, source text, speakers and lip-sync settings inherit the server draft. This synchronously generates preview speech without rendering; short sentences may be retried as an audio group. Split larger changes into language-specific batches, retaining separate journals and business IDs.

For unchanged voices, retry only incorrect speech and reuse valid unaffected audio/visuals. Voice changes require all actually affected speech to be retried. Preview real available audio for text, pronunciation and timing; disclose when listening was unavailable.

## Render one language again

Re-query the draft, then send the target language's **complete already voiced segment list** to `resynthesize_language`:

```json
{
  "sub_task_id": "2100065567327711232",
  "target_language": "en",
  "request_id": "render-unique-001",
  "translated_segments_by_language": {
    "en": [{
      "id": "1", "from": 0, "to": 2.5,
      "source_text": "Welcome to our new collection.",
      "translated_text": "Welcome to our new collection.",
      "speaker_id": 0, "lip_sync": false
    }]
  }
}
```

```bash
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" resynthesize_language --task-id task-RETURNED_NUMERIC_ID --input /absolute/path/render.json --submission-id SAVED_RENDER_OPERATION --wait
node "$VIBBIT_SKILL_DIR/scripts/vibbit.js" resume --state /absolute/path/returned-render-journal.json
```

The single segment is only a format example: send all 1–10000 actual segments. The map has exactly one key, equal to target_language. Preserve the complete server ID set, times, speakers and voiced text. lip_sync may change as requested. Do not submit audio_url, fingerprints or internal fields; do not alter timing to hide duration issues.

Rendering assembles trusted existing speech and does not run TTS or generate missing speech. Retry invalid/missing audio first. The selected subtask must be COMPLETED; the parent must be COMPLETED or RENDERING while siblings run. Use confirm_translation for first delivery. Other languages/videos are not rerendered.

## Requests, receipts, and recovery

All three writes POST `/tasks`, with native input: task_type=VIDEO_VOICE_OVER_TASK and input_info.input containing operation, public task_id and the documented payload. The CLI fills operation/task_id from the command and --task-id; input files do not add that envelope. Quote large long IDs to preserve precision; speaker_id is an integer.

Retries/renders require a business request_id, up to 128 characters. It differs from the response tracing data.request_id and local --submission-id. Retain the same business ID for one intent; recent identical requests only reuse speech when it is still valid, and changing IDs may charge again. Journals retain the minimal scope/business ID without text, reference URLs or credentials. Never automatically resend an uncertain write; recover the original journal first.

For rendering, match the **current request_id, status and error_message** in items[].resynthesis_by_language[target language]. The parent can remain COMPLETED and keep old URLs while the new operation runs. `resume` checks the journal's exact subtask and receipt, waits for a matching receipt, and retains previous_artifacts on failure. Only a successful matching receipt sets delivery_current=true and returns that language's final output_video_url plus its available subtitle-free version.

Voice/segment updates return render_performed=false; prior videos are previous_artifacts, never a new delivery. A plain status --task-id has no per-operation intent; resume the render journal instead. Current draft text can differ from old delivered media. Use each result's subtitle_asr_sentences and translated_segments_snapshot when checking delivered captions, without mandatory extra ASR. from/to are seconds; begin_time/end_time are milliseconds.

For TXT/SRT/VTT, use [transcript tools](../runtime/transcript-tools.md): normalize the real --sub-task-id and --language delivery, then export. Do not substitute an edited draft for delivered speech captions.

Unified writes, compatible edit/confirm routes and signature GET default to 5 requests/second; polling remains at least 5 seconds apart. HTTP 200 still requires business code=200. A conflicting render may return business code 1000: inspect the existing operation rather than automatically changing IDs. Continue authorized polling and checks under the [task lifecycle](../runtime/task-lifecycle.md).
