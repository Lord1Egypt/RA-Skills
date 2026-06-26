# Video Learning Notes Reference

## Dependency expectations

- `yd-dlp-downloader` is responsible for authenticated/video-site downloads.
- `ffmpeg` and `ffprobe` are required for audio extraction, duration probing, scene detection, and screenshots.
- qwen-audio/STT should produce `transcript.srt` whenever timestamps are available.
- The Read tool should be used on extracted frame images to decide which screenshots are educationally useful.

## Frame selection heuristics

Prioritize slides, diagrams, formulas, charts, tables, code, UI operation screens, whiteboard content, and any timestamp where the visual content adds information missing from transcript text.

Avoid selecting frames that are blurry, duplicated, purely decorative, ads/intros/outros, or only show a speaker with no relevant visual information.
