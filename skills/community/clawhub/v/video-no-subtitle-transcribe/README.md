# video-no-subtitle-transcribe 🎧

Fallback transcription for videos without subtitles: **download audio with yt-dlp + transcribe locally with faster-whisper**, output a full timestamped transcript.

When a video has no subtitles (creator disabled CC / auto-generated captions), use this skill to summarize its content anyway. **100% free, runs locally, no data leaves your machine.**

## Use Cases
- YouTube / Bilibili videos without subtitles ("Subtitles are disabled for this video")
- Subtitle endpoints blocked by YouTube rate-limiting / bot checks (429)
- Any site supported by yt-dlp, plus local audio/video files

## Dependencies
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (CTranslate2-accelerated OpenAI Whisper)
- ffmpeg
- whisper small model (auto-downloaded from ModelScope on first run, ~483MB)

```bash
pip install yt-dlp faster-whisper
# ffmpeg: apt install ffmpeg / brew install ffmpeg / choco install ffmpeg
```

## Usage

```bash
python3 scripts/transcribe_video.py "<VIDEO_URL_OR_LOCAL_FILE>" --lang zh --out transcript.txt
```

| Argument | Description | Default |
|----------|-------------|---------|
| `url` | Video URL or local audio/video file path | required |
| `--lang` | Language code (zh/en/ja...) | zh |
| `--out` | Output file path | transcript.txt |
| `--proxy` | Proxy URL (e.g. http://127.0.0.1:7890) | env var / OpenClaw config |

Output format: one line per segment, `[start-end seconds] text`

```
[2.0-4.0] Hello everyone, welcome to today's session
[7.2-13.6] Today we'll cover three topics, starting with project updates
```

## How It Works

1. **Download audio**: tries YouTube clients in order — `tv_embedded` → `android` → `ios` → default. `tv_embedded` bypasses YouTube's DRM/SABR experiments and bot checks.
2. **Transcribe locally**: faster-whisper small model, CPU int8 quantization, roughly 0.5–1x realtime (a 1-hour video takes ~30–60 min).
3. **Model management**: auto-downloads from ModelScope when missing/corrupt, verifies byte size (483546902) to prevent silent corruption.

## Browser Download Fallback

Only if every yt-dlp client attempt fails, use `https://youtube.iiilab.com/` in a browser to download the **YouTube** video's audio (preferred) or video file. Then pass the downloaded local file directly to the script:

```bash
python3 scripts/transcribe_video.py "<LOCAL_AUDIO_OR_VIDEO_FILE>" --lang zh --out transcript.txt
```

This third-party fallback submits the source URL to iiilab. Inform the user before using it for private, unlisted, sensitive, or client-owned videos. Stop and ask before proceeding if the site asks for login, CAPTCHA, payment, permissions, or other confirmation. Do not use this fallback for non-YouTube URLs.

## Pitfalls (important for maintainers)

- YouTube's default client gets 429 → must switch to `tv_embedded` etc.
- Model download: **ModelScope (CN mirror) is fast** (~1MB/s); HuggingFace direct is very slow from China (~90KB/s); hf-mirror's xet protocol **silently corrupts files**
- Model integrity: byte size must equal 483546902, otherwise whisper errors with `File model.bin is incomplete`
- Transcriptions may contain homophone typos (e.g. 在/再, 做/作) — normal for whisper small; restore by context when summarizing

## Companion Skill
Subtitle path (prefer this for videos that have subtitles — instant): [bilibili-youtube-watcher](https://clawhub.ai/donnycui/skills/bilibili-youtube-watcher) (yt-dlp based, supports YouTube + Bilibili)

## License
MIT
