# video_pipeline

`video_pipeline` is a local Windows-first pipeline for YouTube video localization.

Current primary workflow:

1. Download a YouTube video
2. Optionally replace the intro with the channel cover image
3. Extract mono 16k audio
4. Transcribe English subtitles with Whisper
5. Translate and normalize Chinese subtitle blocks
6. Generate Chinese TTS
7. Retime the video to fit the Chinese dub
8. Export the final retimed video and aligned SRT

The main entry point is [`scripts/quick_deliver.py`](D:\video_pipeline\scripts\quick_deliver.py).

## Main Command

Recommended command:

```powershell
cd D:\video_pipeline
python .\scripts\quick_deliver.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Force-regenerate the translation, TTS, dubbed media, retimed media, and SRT files for the same video:

```powershell
cd D:\video_pipeline
python .\scripts\quick_deliver.py "https://www.youtube.com/watch?v=VIDEO_ID" --refresh-tts
```

## Final Deliverables

The main deliverables are:

- `data/output/*_zh_retimed_v4.mp4`
- `data/subtitles/*_zh_retimed_v4_final.srt`

Additional outputs:

- `data/output/*_zh_male.mp4`
- `data/subtitles/*_zh.srt`
- `data/subtitles/*_zh_retimed_v4.srt`

`quick_deliver.py` automatically:

- exports SRT without burning subtitles into the video
- rewrites `*_zh_retimed_v4.srt` from the latest retime plan
- copies a cache-safe `*_zh_retimed_v4_final.srt`
- prints stage timing in seconds

## Agent Runbook

If an agent runs this project, use this as the default procedure:

1. Set required environment variables in the current PowerShell session
2. Run `scripts/quick_deliver.py`
3. Return these paths:
   - `*_zh_retimed_v4.mp4`
   - `*_zh_retimed_v4_final.srt`
   - optionally `*_zh_male.mp4`

Recommended command template:

```powershell
cd D:\video_pipeline
$env:DEEPSEEK_API_KEY="your_deepseek_api_key"
$env:YTDLP_COOKIES_FILE="E:\视频下载\www.youtube.com_cookies.txt"
$env:NODE_OPTIONS="--max-old-space-size=4096"
python .\scripts\quick_deliver.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

If the agent needs to rebuild a previously processed video:

```powershell
cd D:\video_pipeline
$env:DEEPSEEK_API_KEY="your_deepseek_api_key"
$env:YTDLP_COOKIES_FILE="E:\视频下载\www.youtube.com_cookies.txt"
$env:NODE_OPTIONS="--max-old-space-size=4096"
python .\scripts\quick_deliver.py "https://www.youtube.com/watch?v=VIDEO_ID" --refresh-tts
```

## Recent Changes For Agents

Use this section as the current operating summary before running the pipeline:

- Main controller: [`scripts/quick_deliver.py`](D:\video_pipeline\scripts\quick_deliver.py)
- Default Whisper model: `small`
- Default TTS provider: `edge`
- Default Edge voice: `zh-CN-YunjianNeural`
- Retiming padding between sentences: `0.05s`
- Final subtitle target for editors: `*_zh_retimed_v4_final.srt`

Important behavior changes:

- `prepare_video.py` now replaces only the first `intro_seconds` of the picture, while keeping the original audio.
- Cover replacement is channel-config driven; only explicitly enabled channels should use it.
- Opening-line override now prefers matching the English opening up to the `so let's start` style boundary, and only falls back to replacing the first translated sentence if no boundary is found.
- Proper noun correction is glossary-driven through `data/proper_nouns.json`; `aliases` are optional.
- English blocks are for translation quality only; the final structured JSON is Chinese-side only.
- `data/state/debug/*_en_blocks.json` is the best file to inspect when English segmentation looks odd.
- `--refresh-tts` should be used when the user wants regenerated dubbed audio, retimed media, and subtitles for an already processed video.

## Environment

Required:

- Windows
- Python 3.10+
- `ffmpeg` in `PATH`
- `node` in `PATH`
- DeepSeek API access

Recommended:

- `cookies.txt` for YouTube downloads that trigger sign-in / bot checks
- enough free disk space for raw videos, processed videos, TTS chunks, and retimed outputs

Install:

```powershell
cd D:\video_pipeline
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Quick checks:

```powershell
ffmpeg -version
node -v
python -V
```

## Environment Variables

Required in the current shell:

```powershell
$env:DEEPSEEK_API_KEY="your_deepseek_api_key"
```

Recommended for YouTube reliability:

```powershell
$env:YTDLP_COOKIES_FILE="E:\视频下载\www.youtube.com_cookies.txt"
$env:NODE_OPTIONS="--max-old-space-size=4096"
```

Current default TTS is Edge. No TTS API key is required for the default path.

Optional TTS overrides:

```powershell
$env:TTS_PROVIDER="edge"
$env:EDGE_TTS_VOICE="zh-CN-YunjianNeural"
```

Optional alternate providers:

- `TTS_PROVIDER=volcengine`
- `TTS_PROVIDER=azure`
- `TTS_PROVIDER=windows_sapi`

Check current values:

```powershell
echo $env:DEEPSEEK_API_KEY
echo $env:YTDLP_COOKIES_FILE
echo $env:NODE_OPTIONS
echo $env:TTS_PROVIDER
echo $env:EDGE_TTS_VOICE
```

Persist as user-level environment variables if needed:

```powershell
[System.Environment]::SetEnvironmentVariable("DEEPSEEK_API_KEY", "your_deepseek_api_key", "User")
[System.Environment]::SetEnvironmentVariable("YTDLP_COOKIES_FILE", "E:\视频下载\www.youtube.com_cookies.txt", "User")
[System.Environment]::SetEnvironmentVariable("NODE_OPTIONS", "--max-old-space-size=4096", "User")
[System.Environment]::SetEnvironmentVariable("TTS_PROVIDER", "edge", "User")
[System.Environment]::SetEnvironmentVariable("EDGE_TTS_VOICE", "zh-CN-YunjianNeural", "User")
```

After setting user-level variables, open a new PowerShell window before running the pipeline.

## Current Defaults

These are the defaults an agent should assume unless channel rules override them:

- main entry point: `scripts/quick_deliver.py`
- default TTS provider: `edge`
- default Edge voice: `zh-CN-YunjianNeural`
- retime sentence padding: `0.05s`
- final subtitle import target: `*_zh_retimed_v4_final.srt`

## Directory Structure

```text
video_pipeline/
  data/
    raw/                 # downloaded source videos
    covers/              # downloaded YouTube covers
    processed/           # intro-replaced videos
    audio/               # extracted wav files
    subs/                # Whisper English subtitle JSON
    structured/          # final Chinese structured JSON
    tts/                 # per-segment TTS audio
    dubbed_audio/        # merged Chinese audio tracks
    subtitles/           # exported SRT files
    output/              # final mp4 outputs
    state/
      archive.txt        # yt-dlp download archive
      debug/             # debug files such as english blocks
      retime_plans/      # video retime plans
      temp/              # temporary assets such as resized covers
      video_meta/        # per-video metadata snapshots
    channel_rules.json   # channel-specific rules
    proper_nouns.json    # local proper noun correction glossary
  scripts/
    quick_deliver.py
    download.py
    prepare_video.py
    extract_audio.py
    transcribe.py
    enrich_subtitles.py
    dub_video.py
    retime_video.py
    add_subtitles.py
    services/
  requirements.txt
  README.md
```

## Channel Rules

Rule file:

- `data/channel_rules.json`

Per-channel overrides can control:

- whether to download the cover image
- whether to replace the intro with the cover
- intro replacement seconds
- TTS voice
- whether to inject the fixed Chinese intro line

Only explicitly configured channels should use cover replacement.

## Proper Noun Correction

Local proper noun correction happens before translation.

Glossary file:

- `data/proper_nouns.json`

Supported format:

```json
{
  "terms": [
    { "canonical": "Kyiv" },
    {
      "canonical": "Armed Forces of the Russian Federation",
      "aliases": [
        "armed force of the Russian Federation"
      ],
      "min_similarity": 0.72
    }
  ]
}
```

Notes:

- `canonical` is required
- `aliases` is optional
- the system can match close Whisper misspellings against the glossary
- use this file to normalize place names, organizations, and recurring military terms

## Subtitle And Translation Notes

Current design:

- English blocks are optimized for translation, not for final subtitle display
- final Chinese blocks are the single source of truth for:
  - Chinese SRT
  - TTS input
  - retime planning

Debug file for English translation blocks:

- `data/state/debug/*_en_blocks.json`

Final structured JSON intentionally keeps only Chinese-side fields:

- `start`
- `end`
- `zh`
- `tts_text`
- `tts_file`
- `tts_duration`

## Troubleshooting

If YouTube says `Sign in to confirm you’re not a bot`:

- set `YTDLP_COOKIES_FILE`
- make sure the cookies file is valid

If download fails during the JavaScript challenge:

- set `NODE_OPTIONS=--max-old-space-size=4096`

If prepare-video fails on large videos:

- rerun after the failure
- the current pipeline already resizes large cover images before intro replacement

If you need to rebuild outputs for a completed video:

- rerun with `--refresh-tts`

If an editor imports an old subtitle by mistake:

- use `*_zh_retimed_v4_final.srt`

## Other Scripts

`quick_deliver.py` is the only recommended controller entry point.

The other scripts remain available for debugging or partial reruns:

- `download.py`
- `prepare_video.py`
- `extract_audio.py`
- `transcribe.py`
- `enrich_subtitles.py`
- `dub_video.py`
- `retime_video.py`
- `add_subtitles.py`

Old controller / rescue scripts have been removed and should not be reintroduced.

## Resume Behavior

The pipeline supports basic resume behavior:

- `yt-dlp` skips already archived downloads through `data/state/archive.txt`
- existing audio, subtitle, structured JSON, TTS, and output media are reused when present
- `--refresh-tts` clears delivery-stage artifacts for the current video and rebuilds them
