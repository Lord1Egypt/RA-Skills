---
name: video-dub
description: Windows-first video localization pipeline for downloading, transcribing, translating, dubbing, and retiming YouTube or Bilibili videos.
---

# Video Dub Skill

Use this skill when a user wants to turn a source video into a localized dubbed video with aligned subtitles.

This skill bundles the complete video_pipeline, so the pipeline code is included with the skill installation.

## What the pipeline does

Primary workflow:

1. Download the source video (via yt-dlp)
2. Optionally replace only the opening picture with a cover image
3. Extract mono 16k audio
4. Transcribe with Whisper
5. Clean English blocks, correct proper nouns, and translate
6. Generate TTS
7. Retime the video to match the dub
8. Export aligned SRT files without burning subtitles

The main controller is `video_pipeline/scripts/quick_deliver.py`.

## Supported modes

- **Forward localization**: English video to Chinese dubbed video
- **Reverse localization**: Chinese video to English dubbed video

## Requirements

### Environment variables (at least one required)

| Variable | Required | Description |
|----------|----------|-------------|
| `DEEPSEEK_API_KEY` | Yes* | DeepSeek API key for translation. *Required if using default translation path. |
| `YTDLP_COOKIES_FILE` | No | Path to YouTube cookies.txt for reliable downloads |
| `NODE_OPTIONS` | No | Set to `--max-old-space-size=4096` if YouTube shows JavaScript challenges |

### Optional TTS providers (no API key needed for default)

| Provider | Env Variable | Required |
|----------|--------------|----------|
| Edge TTS (default) | `TTS_PROVIDER=edge` | No |
| VolcEngine | `TTS_PROVIDER=volcengine` + API key | No |
| Azure | `TTS_PROVIDER=azure` + API key | No |
| Windows SAPI | `TTS_PROVIDER=windows_sapi` | No |

### Translation provider

The default translation uses DeepSeek API. To use a different provider, edit `video_pipeline/scripts/services/deepseek_translator.py` and replace the base URL with your preferred API (e.g., OpenAI, Anthropic, Grok, etc.). The translation interface is standardized, so any LLM API that supports chat completions can be substituted.

### System dependencies (must be installed)

- **Python 3.10+**
- **ffmpeg** and **ffprobe** (must be in PATH)
- **node** (for yt-dlp's JavaScript runtime)

### Python packages

```
pip install -r video_pipeline/requirements.txt
```

Key packages: yt-dlp, openai-whisper, torch, ffmpeg-python, edge-tts

## Default settings

- Whisper model: `small`
- TTS provider: `edge` (no API key needed)
- Edge voice: `zh-CN-YunjianNeural`
- Translation: DeepSeek API
- Retiming padding: `0.05s`
- Final subtitle target: `*_zh_retimed_v4_final.srt`

For reverse localization, reasonable English voice: `en-US-GuyNeural`

## Proper Noun Glossary

The enrichment stage automatically applies a local glossary before translation.

Use it to normalize:

- place names
- people and organizations
- recurring technical or military terms

Recommended format:

```json
{
  "terms": [
    { "canonical": "Kyiv" },
    {
      "canonical": "Armed Forces of the Russian Federation",
      "aliases": [
        "armed force of the Russian Federation",
        "Amodovvoso-Durasian Federation"
      ],
      "min_similarity": 0.72
    }
  ]
}
```

Rules:

- `canonical` is required.
- `aliases` is optional.
- If `aliases` is omitted, the canonical term still participates in fuzzy matching.
- `min_similarity` is optional.
- The glossary is stored in the pipeline bundle and does not require a separate manual step when the main controller is used.

## Running the pipeline

```powershell
# Install dependencies first
pip install -r video_pipeline/requirements.txt

# Set required environment variables
$env:DEEPSEEK_API_KEY="your_deepseek_api_key"  # Required for translation

# Optional: for reliable YouTube downloads
$env:YTDLP_COOKIES_FILE="path\to\youtube_cookies.txt"
$env:NODE_OPTIONS="--max-old-space-size=4096"

# Run the pipeline
cd <skill_root>\video_pipeline
python .\scripts\quick_deliver.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

To rebuild an already processed video:

```powershell
python .\scripts\quick_deliver.py "https://www.youtube.com/watch?v=VIDEO_ID" --refresh-tts
```

## Expected outputs

After a successful forward run:

- `video_pipeline/data/output/*_zh_retimed_v4.mp4` - final dubbed video
- `video_pipeline/data/subtitles/*_zh_retimed_v4_final.srt` - final subtitle file

Optional outputs:

- `video_pipeline/data/output/*_zh_male.mp4`
- `video_pipeline/data/subtitles/*_zh.srt`
- `video_pipeline/data/subtitles/*_zh_retimed_v4.srt`
- `video_pipeline/data/structured/*.json`
- `video_pipeline/data/state/debug/*_en_blocks.json`

## Agent guidance

When an agent runs this skill:

1. Validate the input URL (YouTube or Bilibili)
2. Set required environment variables (`DEEPSEEK_API_KEY` for translation)
3. Ensure system dependencies are installed (ffmpeg, node, Python 3.10+)
4. Run `quick_deliver.py` from the `video_pipeline` subdirectory
5. Return the final video and subtitle paths
6. If the user asks for partial reruns, rebuild only the requested stage when possible

## Known limitations

- YouTube downloads may require cookies file if encountering bot detection
- Video processing requires significant disk space for intermediate files
- Default TTS (Edge) requires no API key but an internet connection

## Security notes

This skill uses common patterns that may trigger automated security scanners:

- **`subprocess`**: Used to call ffmpeg, ffprobe, and yt-dlp for video processing. These are legitimate system utilities.
- **`os.getenv("DEEPSEEK_API_KEY")`**: API key is read from environment variables only, never hardcoded.
- **`decode()`**: Audio/video data is decoded for processing, not for malicious purposes.

These are standard practices for video processing pipelines and do not indicate any malicious behavior. The code does not:

- Transmit data to unauthorized endpoints
- Download or execute remote code
- Store or exfiltrate credentials

If your security scanner blocks this skill, you can verify by reviewing the source code in `video_pipeline/scripts/`.

## Packaging notes

This skill is published with the pipeline code bundled in the `video_pipeline/` subdirectory.

The bundle excludes generated outputs and caches (data/raw/, data/audio/, data/tts/, data/output/, data/state/, etc.).

To rebuild the release bundle from source:

```powershell
.\scripts\package_release.ps1 -SourceRoot "D:\video_pipeline" -DestinationRoot "<skill_destination>"
```
