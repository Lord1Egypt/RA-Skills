# Single Video Ingest: Classification and Output Strategy

## Automatic content classification

When handling a single video, classify the content from the transcript first, then pick the output and screenshot strategy.

| Content Type | Classification Signals | Screenshot Strategy | Article Structure |
|------|------|------|------|
| Tutorial / hands-on demo | Sequential steps, code or UI changes | 5-15 frames, roughly one per step | Standard illustrated note |
| Review / deep analysis | Argument-driven, mostly voice-over | 8-12 frames, one per major concept | Sectioned note with images and quotes |
| Panel / discussion / meeting | Multiple speakers, topic turns | 5-8 frames, one per topic turn | Split by speaker or topic |
| Vlog / casual monologue | Loose narrative | 3-5 frames, use scene changes | Short summary structure |
| Podcast / audio-only | No useful visuals | 0 frames | Text-only summary |

## Platform-specific format selection

### Bilibili

- Run `-F` first because format IDs vary
- Non-premium access may not provide high-bitrate 1080p, so 720p is often safer
- Cookie-based login is commonly required

### YouTube

- `bestvideo[height<=720]+bestaudio/best[height<=720]` is usually the most stable choice
- Cookies are usually unnecessary
- Region-restricted videos may require a proxy

### Other platforms

- Run `-F` first
- Prefer a 720p `mp4` when available
- Most sites do not require cookies

## Subtitle acquisition priority

| Priority | Source | Handling |
|------|------|------|
| 1 | Platform-provided subtitles | Download `.srt`, then preprocess to plain text |
| 2 | No subtitles available | Transcribe with Whisper |
| 3 | External subtitle file already exists | Read and preprocess directly |

## Download failure recovery

1. Format unavailable: rerun `-F` and choose a different format ID
2. Bilibili `412`: refresh the cookie
3. YouTube region restriction: switch network route or fall back to `-f "best[height<=480]"`
4. Expired login state: export new cookies
5. Timeout: retry with a smaller format
