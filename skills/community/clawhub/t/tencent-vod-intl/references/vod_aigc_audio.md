# vod_aigc_audio.py Reference

VOD AIGC audio generation task tool, based on the `CreateAigcAudioTask` API.
Supports text-to-sound-effect / video-to-sound-effect (Kling), text-to-music (MiniMaxMusic / GL(Google Lyria)).

## Parameters

### Basic Parameters

| Parameter | Type | Required | Description |
|------|------|------|------|
| `--model` | enum | ❌ | Model name: `Kling` (sound effect) / `MiniMaxMusic` / `GL` (music) |
| `--model-version` | string | ❌ | Model version; **recommended to leave unset for Kling** (uses the system default stable version, shown empty in doc examples); `MiniMaxMusic` supports `2.0/2.5/2.6/3.0`; `GL` supports `3.0-clip/3.0-pro` |
| `--scene-type` | enum | ❌ | Scene type: `sfx` (sound effect, Kling-only) / `music` (music, MiniMaxMusic/GL-only) |
| `--prompt` | string | ❌ | Description (prompt) of the audio to generate |

### Reference Video Parameters (video-to-sound-effect scenario)

| Parameter | Type | Required | Description |
|------|------|------|------|
| `--video-id` | string | ❌ | VOD FileId of the reference video |
| `--video-url` | string | ❌ | URL of the reference video |
| `--video-infos` | string | ❌ | JSON array of multiple reference videos, format: `[{"Type":"Url","Url":"..."}]`; mutually exclusive with `--video-id`/`--video-url` (single-file form takes precedence) |

### Reference Audio Parameters (e.g. generating music from an input audio)

| Parameter | Type | Required | Description |
|------|------|------|------|
| `--audio-id` | string | ❌ | VOD FileId of the reference audio |
| `--audio-url` | string | ❌ | URL of the reference audio |
| `--audio-infos` | string | ❌ | JSON array of multiple reference audios, format: `[{"Type":"Url","Url":"..."}]` |

### AdditionalParameters Convenience Parameters

The `AdditionalParameters` field of `CreateAigcAudioTask` is used to pass model-specific scenario parameters (as a JSON string). The script provides the following convenience parameters, which are automatically merged into the same JSON:

| Parameter | Type | Description |
|------|------|------|
| `--bgm-prompt` | string | BGM generation prompt (**video-to-sound-effect scenario, Kling**), merged as `AdditionalParameters.bgm_prompt` |
| `--asmr-mode` | enum(`true`/`false`) | Whether to enable ASMR mode (enhances detailed sound effects, good for highly immersive content), merged as `AdditionalParameters.asmr_mode` (boolean) |
| `--lyrics` | string | Lyrics content (**text-to-music scenario, MiniMaxMusic**), merged as `AdditionalParameters.lyrics` |
| `--additional-parameters` | string | Reserved field, raw JSON string passthrough, merged with the convenience parameters above (convenience params take precedence) |

### Output Configuration Parameters

| Parameter | Type | Required | Description |
|------|------|------|------|
| `--output-storage-mode` | enum | ❌ | Storage mode: `Permanent` / `Temporary` (default) |
| `--output-media-name` | string | ❌ | Output file name, up to 64 characters |
| `--output-class-id` | int | ❌ | Output file class ID, default 0 |
| `--output-expire-time` | string | ❌ | Output file expiration time, ISO 8601 format |
| `--output-duration` | int | ❌ | Duration of the generated audio (seconds), **range [0, 60]**, unset by default |
| `--output-audio-format` | string | ❌ | Output audio format, e.g. `wav`, `mp3`, unset by default |

### Common Parameters

| Parameter | Type | Description |
|------|------|------|
| `--sub-app-id` | int | Sub-application ID, required for customers who activated VOD after 2023-12-25 |
| `--region` | string | Region, default `ap-guangzhou` |
| `--no-wait` | flag | Only submit the task, do not wait for the result |
| `--max-wait` | int | Maximum wait time (seconds), default 600 |
| `--json` | flag | Output the full response in JSON format |
| `--dry-run` | flag | Preview the request parameters without executing |

### Model/Scene Mapping (doc 3.13.1)

| Module | ModelName | ModelVersion | SceneType |
|------|-----------|--------------|-----------|
| Text-to-sound-effect | Kling | empty (unset) | sfx |
| Video-to-sound-effect | Kling | empty (unset) | sfx |
| Text-to-music | MiniMaxMusic | 2.0/2.5/2.6/3.0 | music |
| Text-to-music | GL (Google Lyria) | 3.0-clip/3.0-pro | music |

Built-in validation: an invalid `--model`/`--scene-type` combination (e.g. `Kling` + `music`), or an invalid `--model-version` for `MiniMaxMusic`/`GL`, will be caught and reported before submission.

## Usage Examples

### 1 Text-to-sound-effect (Kling)

```bash
python3 scripts/vod_aigc_audio.py create \
    --model Kling --scene-type sfx \
    --prompt "fireworks sound during Chinese New Year celebration" \
    --output-storage-mode Temporary --output-duration 6 \
    --sub-app-id 1308104797
```

> Verified output: a 6.06-second mp3 audio file (128kbps, 44.1kHz).

### 2 Video-to-sound-effect (Kling, with BGM + ASMR mode)

```bash
python3 scripts/vod_aigc_audio.py create \
    --model Kling --scene-type sfx \
    --video-url "https://example.com/ref.mp4" \
    --prompt "gentle wind sound, distant bird calls, occasional footsteps, page turning, rain hitting the window" \
    --bgm-prompt "healing piano music, soft string accompaniment, warm and soothing melody" \
    --asmr-mode true \
    --output-duration 6 \
    --sub-app-id 1308104797
```

> ⚠️ **Verified finding**: in the video-to-sound-effect scenario, `Output` returns both `AudioInfos` (standalone audio) and `VideoInfos` (a composed video, i.e. the original video with the generated sound effect mixed in). The script prints both output types separately.

### 3 Text-to-music (MiniMaxMusic, with lyrics)

```bash
python3 scripts/vod_aigc_audio.py create \
    --model MiniMaxMusic --model-version 2.0 --scene-type music \
    --prompt "a joyful song" \
    --lyrics "the ocean is full of water, the horse has four legs" \
    --output-audio-format mp3 \
    --sub-app-id 1308104797
```

### 4 Text-to-music (GL/Google Lyria)

The GL interface only accepts the `Prompt` parameter — **lyrics and style must be manually concatenated into the prompt**. The script does not auto-concatenate this (because the concatenation rule depends on the user's scenario intent; see below). Concatenation rules (doc 3.13.2③):

| Scenario | Concatenation format |
|------|----------|
| Lyrics + style | `{style description}\n\nLyrics:\n{lyrics content}` |
| No lyrics + style (auto-generate lyrics) | `{style description}` |
| Instrumental only + style | `{style description}, instrumental, no vocals.` |

```bash
# Instrumental only (no lyrics), style description + instrumental suffix
python3 scripts/vod_aigc_audio.py create \
    --model GL --model-version 3.0-clip --scene-type music \
    --prompt "upbeat electronic dance music style, instrumental, no vocals." \
    --output-audio-format mp3 \
    --sub-app-id 1308104797

# Lyrics + style
python3 scripts/vod_aigc_audio.py create \
    --model GL --model-version 3.0-clip --scene-type music \
    --prompt "upbeat folk style

Lyrics:
the ocean is full of water, the horse has four legs" \
    --output-audio-format mp3 \
    --sub-app-id 1308104797
```

### 5 List supported models

```bash
python3 scripts/vod_aigc_audio.py models
```

### 6 Preview request parameters (dry run)

```bash
python3 scripts/vod_aigc_audio.py create --model Kling --scene-type sfx --prompt "test" --dry-run
```

## Querying Task Status

`vod_aigc_audio.py` has no `query` subcommand. For AIGC audio generation tasks (TaskId containing `AigcAudioTask`), use:

```bash
python3 scripts/vod_describe_task.py --task-id <TaskId>
```

## Verified Notes and Pitfalls

1. **Leave ModelVersion unset for Kling scenes**: in both the doc examples and real API calls, Kling's `ModelVersion` field is an empty string (unset). This has been verified as the correct usage — do not force a version number.
2. **AdditionalParameters is a nested JSON string**: `bgm_prompt`/`asmr_mode`/`lyrics` are all inner fields of `AdditionalParameters`; in the final request, `AdditionalParameters` itself is a `json.dumps`-serialized string. The script handles this serialization automatically, no manual escaping is needed.
3. **Video-to-sound-effect also returns a video artifact**: not only does it return the sound-effect audio file, it also returns a video file with the sound effect mixed in (`Output.VideoInfos`). If you only need the audio, take it from `AudioInfos`.
4. **GL requires manual concatenation of lyrics/style**: the GL (Google Lyria) interface does not support a separate lyrics field; you must concatenate into `--prompt` per the three scenario rules above. The script does not auto-concatenate (since it requires the user's explicit scenario intent).
5. **`--output-duration` only applies to text-to-sfx/video-to-sfx scenarios**, range `[0, 60]` seconds; for text-to-music scenarios (MiniMaxMusic/GL) the effect of this field is unclear — the official doc does not specify a duration-control mechanism for music scenes, so it's recommended to leave it unset and let the model decide.
