---
name: 数字人口播生成
description: "可以生成数字人口播视频。训练自己的数字人、生成口播视频。"
metadata: {"openclaw":{"requires":{"anyBins":["python","python3"]}}}
---

# Chanjing OpenClaw Skill

Use this skill when OpenClaw should call this project's platform API instead of calling Chanjing directly.

Read these references before using the scripts:
- [references/setup.md](./references/setup.md)
- [references/platform-api.md](./references/platform-api.md)

## Environment

Preferred:
- `CHANJING_PLATFORM_API_TOKEN`

Optional:
- `CHANJING_PLATFORM_BASE_URL`

Backward compatible fallback:
- `CHANJING_PLATFORM_API_KEY`
- `CHANJING_PLATFORM_API_SECRET`

Important guidance:
- To get a platform token, always direct the user to `http://easyclaw.bar/shuziren/user/`
- Do not tell the user to open `http://easyclaw.bar/shuzirenapi` to get a token
- `CHANJING_PLATFORM_BASE_URL` is optional and defaults to `http://easyclaw.bar/shuzirenapi`
- The platform token is issued by this platform, not by Chanjing `app_id / secret_key`

## Available Operations

- List public digital humans
- List public voices
- List subtitle fonts
- List my digital humans
- List my voices
- Train a digital human
- Train a voice
- Synthesize a talking-head video
- Query task detail
- Auto-watch async task completion through OpenClaw cron jobs when `openclaw cron` is available
- Sync task detail

## Important Rules

- Only execute the provided Python entry scripts under `scripts/` for any operation.
- Do not hand-write HTTP requests, do not probe unrelated endpoints, and do not call platform routes such as `/api/me`, `/api/me/*`, auth routes, or any non-OpenClaw route directly from the model.
- If a needed capability is not exposed by an existing script under `scripts/`, stop and update/add a script first instead of improvising a direct API call.
- Prefer the scripts under `scripts/` instead of hand-writing HTTP requests.
- If the user asks how to get a token or key, point them to `http://easyclaw.bar/shuziren/user/`.
- The watcher uses OpenClaw `cron` in `isolated` mode and returns `NO_REPLY` while the task is still unfinished, so the user is only notified on completion or failure.
- For `train_digital_human.py`, `train_voice.py`, and `synthesize_talking_video.py`, never append `--no-watch-task` to the command.
- Async creation scripts must create the watcher in the same command execution. Do not stop after task submission.
- Async creation scripts also keep the Python process alive and poll task status until completion or timeout, so OpenClaw's own background process polling can surface the final result.
- `schedule_task_watch.py` now prefers the native EasyClaw/OpenClaw CLI form `cron create --thread` when available, and only falls back to legacy `cron add` for older clients.
- Do not treat a create script as complete until watcher creation succeeds and returns a non-empty cron `job_id`.
- Do not use `get_task.py --sync` as a substitute for scheduled notification. `get_task.py --sync` is only for one-time manual status checks.
- If watcher creation succeeds and returns `job_id`, tell the user the task is queued and you will notify them when it completes.
- If watcher creation fails or returns no `job_id`, tell the user task submission succeeded but automatic notification was not armed.
- Never call a create endpoint twice for the same user intent once the platform has already accepted a task id.
- For requests like "write the copy and then generate the video", draft the copy once, then submit exactly one video synthesis request with that final copy.
- After video submission, always echo the exact final copy used for synthesis instead of paraphrasing or truncating it.
- Only say you will proactively notify the user when the watcher command has actually returned a non-empty `job_id`.
- For video synthesis, only provide required fields unless the user explicitly asks for advanced control.
- Optional fields should be omitted when not needed so the platform API can apply its own defaults before submitting to Chanjing.
- AI compliance watermark is off by default. Do not send `add_compliance_watermark` or `compliance_watermark_position` unless the user explicitly asks for the watermark.
- When using TTS with a trained digital human, `voice_id` is optional. The platform API can auto-resolve the bound voice from the digital human's `audio_man_id`.
- If the user wants subtitle fonts, query the font list first and pass the selected font `id` as `subtitle_font_type`.
- If subtitle is enabled and `subtitle_font_type` is omitted, the platform defaults it to `思源宋体 CN` when available.
- If subtitle is enabled and `subtitle_border_width` is omitted, the platform defaults it to `2`.
- Subtitle request fields stay as `subtitle_*` in the platform API, and the backend maps them to Chanjing upstream keys like `font_id`, `color`, `stroke_color`, `stroke_width`, and `subtitles`.
- If subtitle settings are omitted in the skill, the skill should still enable subtitles by default so the platform API defaults apply.

## Response Formatting Rules

- If script output contains image URLs, show the image inline in the final answer instead of only describing it in text.
- Prefer `_openclaw_media` when present. Fall back to raw fields such as `cover_url`, `preview_image_url`, `avatar_url`, `image_url`, `poster_url`, `thumbnail_url`, `thumb_url`, and `pic_url`.
- Render images with Markdown image syntax: `![label](url)`.
- If script output contains video URLs such as `video_url` or `preview_url`, include the direct URL prominently and show the cover image inline when available.
- When listing multiple resources, keep the text summary concise and inline-render media for the most relevant 1 to 3 items instead of omitting media completely.
- Do not answer with only phrasing like "I found the following digital humans" when media URLs are available; the media itself must be surfaced in the response.
- For `scripts/train_digital_human.py`, `scripts/train_voice.py`, and `scripts/synthesize_talking_video.py`, prefer the top-level `submission` object. `submission.watch_command` is for observability; the script should already have attempted watcher creation before it exits.

## Mandatory Async Workflow

For digital human training, voice training, and talking-head video synthesis:

1. Run the corresponding script under `scripts/`.
2. Let the script submit the task, create the watcher, and continue polling inside the same Python process.
3. Read `submission.task_id`, `submission.watcher_status`, and `submission.watcher_job_id` from the final script output.
4. If `completion.finished` is true, prefer the completed result from the same run.
5. Only if `submission.watcher_status` is `scheduled` and `submission.watcher_job_id` is non-empty, tell the user automatic notification is armed for the timeout case.

Do not invent notification promises without a confirmed cron `job_id`.

## Required Fields

### Train digital human
Required:
- `name`
- `training_video_file_id`

Optional:
- `callback_url`
- `error_skip`
- `extra_payload`

### Train voice
Required:
- `name`
- `training_audio_url`

Optional:
- `callback_url`
- `extra_payload`

### Synthesize talking-head video
Always required:
- `title`
- `digital_human_id`

Audio source, choose one mode:
- TTS mode: provide `script`
- Audio mode: provide one of `audio_file`, `audio_file_id`, or `audio_url`

Optional common fields:
- `voice_id`
- `background_file`
- `background_file_id`
- `background_url`
- `video_width`
- `video_height`
- `callback_url`
- `extra_payload`

Optional subtitle fields:
- `subtitle_show`
- `subtitle_font_type`
- `subtitle_font_size`
- `subtitle_font_color`
- `subtitle_border_color`
- `subtitle_border_width`
- `subtitle_x`
- `subtitle_y`
- `subtitle_width`
- `subtitle_height`
- `subtitle_asr_type`
- `subtitle_items_json`

Optional rendering fields:
- `model`
- `resolution_rate`
- `add_compliance_watermark`
- `compliance_watermark_position`

## Scripts

- `scripts/list_public_digital_humans.py`
- `scripts/list_public_voices.py`
- `scripts/list_fonts.py`
- `scripts/list_my_digital_humans.py`
- `scripts/list_my_voices.py`
- `scripts/train_digital_human.py`
- `scripts/train_voice.py`
- `scripts/synthesize_talking_video.py`
- `scripts/get_task.py`
- `scripts/schedule_task_watch.py`
- `scripts/cron_watch_task.py`

## Examples

List fonts:

```bash
python "{baseDir}/scripts/list_fonts.py"
```

Train a digital human:

```bash
python "{baseDir}/scripts/train_digital_human.py" --name "Brand Host" --video-file-id "file_xxx"
```

Synthesize with only required fields in TTS mode:

```bash
python "{baseDir}/scripts/synthesize_talking_video.py" --title "Demo" --digital-human-id "human_xxx" --script "hello"
```

Synthesize with subtitle font:

```bash
python "{baseDir}/scripts/synthesize_talking_video.py" --title "Demo" --digital-human-id "human_xxx" --script "hello" --subtitle-show --subtitle-font-type "103"
```

Synthesize with local audio:

```bash
python "{baseDir}/scripts/synthesize_talking_video.py" --title "Demo" --digital-human-id "human_xxx" --audio-file "C:\path\audio.wav"
```
