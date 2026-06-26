# Workflow notes (YouTube no-subtitle)

Goal: Summarize the latest video even when YouTube timedtext/subtitles are empty.

Preferred local pipeline:

1) Install deps (once)
- `brew install yt-dlp ffmpeg`
- `python3 -m venv .venv && source .venv/bin/activate && pip install faster-whisper`

2) Run script
- `python3 scripts/youtube_asr_summarize.py --url <youtube-url> --out <outdir>`

3) Deliver
- Send `summary.md` content as WhatsApp-friendly bullets
- Attach 1-3 frames from `<outdir>/frames/frame_*.jpg`

Tips:
- Use `--model small` for speed on CPU; `medium` for accuracy.
- ASR may contain homophone errors; treat numbers/names carefully.
