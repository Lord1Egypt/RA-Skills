---
name: video-subtitle-translation-dubbing
description: Multi-language video subtitle translation and automatic dubbing skill (supports English, Chinese, Japanese, Spanish, French, German, Korean, etc.).
version: 0.1.4
metadata:
  openclaw:
    requires:
      bins:
        - ffmpeg
        - ffprobe
    emoji: "🎬"
    homepage: https://github.com/zbjincheng/openclaw-skill-videotranslate
---

# video-subtitle-translation-dubbing

[English] | [简体中文](./skill.zh-CN.md)

**OpenClaw Skill** — Multi-language video subtitle translation and automatic dubbing, producing high-quality multi-track, multi-subtitle videos on demand.

- **Name**: `video-subtitle-translation-dubbing`
- **Version**: `0.1.4`
- **Entrypoint**: `translation_dubbing_skill.run`
- **Manifest**: [`manifest.yaml`](./manifest.yaml)

## Overview

This skill processes input videos (via external subtitles or by auto-extracting embedded subtitle tracks) and produces:

- An independent translated target-language subtitle file (UTF-8 SRT/VTT)
- A muxed `.mkv` video file

Callers select one of two processing modes via `processing_mode`:

| Processing Mode | TTS | Audio Track | Subtitle Tracks |
|---|---|---|---|
| `subtitle_only` | Skipped | Source audio track only (default) | Target subtitle (default) + Source subtitle |
| `subtitle_and_dubbing` (default) | Synthesizes target voiceover | Target dubbing (default) + Source audio | Target subtitle (default) + Source subtitle |

## Quick Start

```python
from translation_dubbing_skill import parse_manifest, run

params = parse_manifest({
    "video_path": "/path/to/input.mp4",
    "subtitle_path": "/path/to/input.en.srt",   # Optional
    "source_language": "en",
    "target_language": "zh-CN",
    "processing_mode": "subtitle_and_dubbing",
    "translation_provider": "llm",
    "translation_endpoint": "https://api.example.com/v1/chat/completions",
    "translation_credential": "sk-...",
    "translation_config": {"model_name": "gpt-4o-mini"},
    "tts_provider": "edge",
    "tts_endpoint": "none",
    "tts_credential": "none",
})

result = await run(params)
print(result.output_video_path, result.output_subtitle_path)
```

## Inputs

| Field | Type | Required | Description |
|---|---|---|---|
| `video_path` | path | Yes | Input video file path (extension must be in `supported_video_formats`) |
| `subtitle_path` | path | No | External subtitle file (`.srt` / `.vtt`); extracts embedded track if omitted |
| `source_language` | string | Yes | Source video/subtitle language code (default `en`) |
| `target_language` | string | Yes | Target translation/TTS language code (default `zh-CN`) |
| `processing_mode` | enum | Yes | `subtitle_only` \| `subtitle_and_dubbing` (default) |
| `voice_id` | string | No | TTS voice identifier; ignored in `subtitle_only` mode |
| `translation_provider` | enum | Yes | `llm` \| `web` |
| `translation_endpoint` | string | Yes | HTTP endpoint for translation service |
| `translation_credential` | secret | Yes | API key / credential (desensitized as `***` in logs/errors) |
| `translation_config` | object | No | Custom translation provider configuration |
| `translation_rate_limit` | object | No | Adaptive scheduler configuration (batch/payload/concurrency) |
| `tts_provider` | enum | Conditional | `llm` \| `web` \| `edge`; required when mode is `subtitle_and_dubbing` |
| `tts_endpoint` | string | Conditional | HTTP endpoint for TTS service |
| `tts_credential` | secret | Conditional | API key / credential for TTS service |
| `tts_config` | object | No | Custom TTS provider configuration |
| `tts_rate_limit` | object | No | Adaptive scheduler configuration for TTS |

For full parameter definitions and defaults, see [`manifest.yaml`](./manifest.yaml).

## Outputs

| Field | Type | Description |
|---|---|---|
| `output_video_path` | path | Path to the synthesized `.mkv` video |
| `output_subtitle_path` | path | Path to the translated target-language UTF-8 subtitle file |

### Output Video Track Structure

**`subtitle_and_dubbing`** mode:

```
streams:
  video:  video  (codec copy, preserving resolution/fps/encoding)
  audio:  target (AAC, language=target, default=1, title="Target Dubbing")
          source (copy, language=source, default=0, title="Original Audio")
  subs:   target (SRT, language=target, default=1, title="Target Subtitle")
          source (SRT, language=source, default=0, title="Original Subtitle")
```

**`subtitle_only`** mode:

```
streams:
  video:  video  (codec copy)
  audio:  source (copy, language=source, default=1)
  subs:   target (SRT, language=target, default=1)
          source (SRT, language=source, default=0)
```

## Progress Reporting

The skill reports progress stage-by-stage via the progress callback injected by the OpenClaw runtime:

```
parsing → translating → [tts] → muxing → done
```

- `translating` stage includes `completed / total` counts (monotonic non-decreasing)
- `tts` stage occurs only in `subtitle_and_dubbing` mode and also reports progress counts
- `done` stage returns `output_video_path / output_subtitle_path` in `extra`

## Pluggable Providers

Built-in providers (auto-registered via `@register` upon module loading):

| Kind | Provider Type | Description |
|---|---|---|
| `translation` | `llm` | Invokes LLM chat completion endpoints with batch JSON payloads |
| `translation` | `web` | Invokes 3rd-party translation REST APIs |
| `tts` | `llm` | Invokes LLM TTS endpoints (supports batching) |
| `tts` | `web` | Invokes 3rd-party TTS REST APIs (single item) |
| `tts` | `edge` | Invokes built-in Microsoft Edge Read-Aloud TTS service |

New providers can be added by implementing the protocol under `translation_dubbing_skill.providers.{translation,tts}` and decorating with `@register(kind, provider_type)`. **No caller code changes required.**

## Adaptive Scheduler

Translation and TTS requests are driven by `AdaptiveScheduler`, featuring 3D adaptive tuning:

- **Batch Size** (`batch_size`): Number of entries per request
- **Payload Size** (`payload_size`): Text length measured in tokens or characters
- **Concurrency** (`concurrency`): Number of simultaneous in-flight requests

Uses AIMD strategy: scales up on consecutive successes; scales down on `429` (`RateLimitError`) with exponential backoff; reduces `payload_size` and re-slices without penalty on `413` / context window overflow (`PayloadTooLargeError`); retries with backoff on `5xx` / timeouts (`TransientError`).

Default parameters are specified in `manifest.yaml` under `translation_rate_limit / tts_rate_limit.default`.

## Error Handling

All exceptions inherit from `SkillError`, carrying a `stage / code / reason / context` tuple. Sensitive keys (`credential / api_key / authorization`) are automatically masked as `***` during `to_dict()` serialization.

## Prerequisites

- **Python** ≥ 3.11
- **ffmpeg** / **ffprobe**: Must be available in `PATH`. Used for subtitle extraction, audio time-stretching, video muxing, and media probing.
- **httpx**: HTTP client
- **pydub**: Audio segment manipulation and peak normalization
- **PyYAML**: Manifest parsing

## License

See `LICENSE` and `pyproject.toml` in the repository root.
