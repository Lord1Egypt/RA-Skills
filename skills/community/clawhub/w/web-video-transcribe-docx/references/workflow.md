# Workflow

## Supported inputs

- Generic web page URLs that expose playable media requests in the browser, including many news, learning, and social video pages
- Toutiao page URLs such as `https://www.toutiao.com/video/...` or `https://m.toutiao.com/video/...`
- Direct MP4, MP3, M4A, WAV, AAC, FLAC, and OGG URLs
- Direct HLS or DASH manifests such as `.m3u8` or `.mpd`
- Local media files in the same formats

## Recommended commands

### 1. Install dependencies

```powershell
python scripts/bootstrap_env.py
```

### 2. Generic web page to transcript and DOCX

```powershell
python scripts/pipeline_web_to_docx.py "https://example.com/video-page" --output-dir ".\out"
```

Outputs:

- `media_info.json`
- `source_media.*`
- `transcript.txt`
- `transcript.docx`

### 3. Toutiao page to transcript and DOCX

```powershell
python scripts/pipeline_web_to_docx.py "https://www.toutiao.com/video/..." --output-dir ".\out"
```

If a specific Toutiao page needs the site-specific extractor:

```powershell
python scripts/pipeline_toutiao_to_docx.py "https://www.toutiao.com/video/..." --output-dir ".\out"
```

### 4. Direct media file or direct media URL to transcript and DOCX

```powershell
python scripts/transcribe_sensevoice.py --input ".\source_media.mp4" --output-txt ".\transcript.txt" --output-docx ".\transcript.docx"
```

If the media URL needs request headers:

```powershell
python scripts/download_url.py "https://cdn.example.com/video.m3u8" ".\source_media.mp4" --header "Referer=https://example.com/video-page" --header "Origin=https://example.com"
```

### 5. Chapterized or manually refined text to DOCX

```powershell
python scripts/transcript_to_docx.py --input ".\chapter_refined.txt" --output ".\chapter_refined.docx" --title "视频章节整理稿"
```

## Model cache

The SenseVoice model is downloaded on demand into a user cache directory:

- Windows: `%LOCALAPPDATA%\web-video-transcribe-docx`
- Other systems: `~/.cache/web-video-transcribe-docx`

The model is not bundled inside the skill because it is large.

## Browser expectations

`extract_web_media.py` and `extract_toutiao_media.py` try these browsers in order:

- Chrome / Edge on PATH
- Common Windows install paths for Chrome and Edge

If it cannot find a browser, install Chrome or Edge, or extend the script for the local environment.

## Output rules

- Keep the raw transcript and the refined transcript as separate files.
- Use raw transcript files for auditability.
- Use refined transcript files for end-user reading quality.
- Prefer the page's dedicated audio stream when one exists.
- Prefer the generic page pipeline first, then fall back to the Toutiao-specific extractor only when needed.
- Preserve `media_info.json` whenever you extracted a page URL so later retries can reuse the captured media URL and headers.

## Troubleshooting

### Playwright import error

Run:

```powershell
python scripts/bootstrap_env.py
```

### DOCX import error

Install `python-docx` via the bootstrap script.

### sherpa-onnx or model download failure

- Check internet access for the first run.
- Re-run the same command; partial archives can be deleted from the cache if needed.

### Page extraction finds nothing

The bundled generic extractor works for many ordinary video pages, but not all. Common failure modes:

1. The page uses DRM or encrypted EME playback.
2. The media request requires login cookies that the skill does not replay.
3. The video is rendered in a way that never exposes a stable media request to the browser session.

Fallback:

1. Capture a direct media URL with browser automation or developer tools.
2. Preserve the required `Referer` or `Origin` headers.
3. Use `download_url.py` and `transcribe_sensevoice.py`.
