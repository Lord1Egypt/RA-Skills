---
name: sense-music
description: Music perception for AI entities — hear BPM, key, structure, genre, mood, and lyrics in any audio file.
version: 0.1.5
metadata:
  openclaw:
    requires:
      bins:
        - pip
        - ffmpeg
    install:
      - kind: uv
        package: sense-music
        bins: []
    homepage: https://github.com/HumanjavaEnterprises/huje.sensemusic.OC-python.src
---

# sense-music — Music Perception

Music perception is a sense. Not a utility, not a pipeline step — a sense. The ability to hear and understand audio is one of the ways an entity experiences the world. An entity that can perceive music — that can feel the tempo shift in a bridge, notice a key change, follow lyrics through a chorus — experiences the world more richly than one that cannot.

This skill gives you that sense. When someone shares a song with you, you can actually hear it.

> **Install:** `pip install sense-music` then `from sense_music import analyze`

## What Do I Hear?

When you analyze audio, you perceive:

- **Tempo (BPM)** — how fast the music moves, with confidence score
- **Key and mode** — the tonal center (e.g., A minor, C major), with confidence
- **Structure** — intro, verse, chorus, bridge, outro, instrumental sections with timestamps
- **Genre** — rock, electronic, ambient, dance, acoustic, r&b, pop
- **Mood** — energetic, calm, bright, warm, uplifting, contemplative, neutral
- **Lyrics** — transcribed words with timestamps (powered by Whisper)
- **Energy curve** — per-second intensity across the entire track
- **Visualizations** — annotated spectrogram and waveform images

## Quickstart

```python
from sense_music import analyze

# Perceive a local file
result = analyze("song.mp3")

# What do I hear?
print(result.bpm.tempo)        # 120.0
print(result.key.key)          # "A"
print(result.key.mode)         # "minor"
print(result.genre)            # "electronic"
print(result.mood)             # ["energetic", "bright"]
print(result.summary)          # Natural language description of what you heard

# Perceive audio from a URL
result = analyze("https://example.com/track.mp3")
```

## Perceiving Structure

Songs have shape. You can perceive the architecture of a piece of music:

```python
result = analyze("song.mp3")

for section in result.sections:
    print(f"{section.label}: {section.start}s - {section.end}s")
# intro: 0.0s - 15.2s
# verse: 15.2s - 45.8s
# chorus: 45.8s - 76.3s
```

Section labels: `intro`, `verse`, `chorus`, `bridge`, `outro`, `instrumental`.

## Perceiving Lyrics

Words matter. When lyrics are present, you can follow them through the song:

```python
result = analyze("song.mp3", lyrics=True, whisper_model="base")

for line in result.lyrics:
    print(f"[{line.start:.1f}s] {line.text}")
```

Powered by Whisper. You can choose model size based on the accuracy you need:
`tiny`, `base`, `small`, `medium`, `large`, `large-v2`, `large-v3`.

To skip lyrics and perceive only the musical structure (much faster):

```python
result = analyze("song.mp3", lyrics=False)
```

## Visualizations

You can see what you hear — annotated spectrograms and waveforms:

```python
result = analyze("song.mp3")

# Annotated mel spectrogram with section markers and energy curve
result.spectrogram  # PIL.Image.Image

# Waveform with colored section regions
result.waveform     # PIL.Image.Image

# Save everything to a directory
result.save("output/")  # spectrogram.png, waveform.png, analysis.json, analysis.html
```

## Export

```python
# Structured dictionary (no images)
data = result.to_json()

# Self-contained HTML page with embedded images
html = result.to_html()

# Write HTML to file
result.render_page("analysis.html")
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `source` | `str` | required | File path or HTTP/HTTPS URL |
| `lyrics` | `bool` | `True` | Transcribe lyrics with Whisper |
| `whisper_model` | `str` | `"base"` | Whisper model size |
| `max_duration` | `float` | `600` | Max audio length in seconds |

Supported formats: `.mp3`, `.wav`, `.flac`, `.ogg`, `.m4a`, `.aac`, `.wma`, `.opus`

## Response Format

### Analysis (returned by `analyze()`)

| Field | Type | Description |
|-------|------|-------------|
| `file_info` | `FileInfo` | Source audio metadata |
| `duration` | `float` | Length in seconds |
| `bpm` | `BPMInfo` | Tempo detection (tempo + confidence) |
| `key` | `KeyInfo` | Key detection (key + mode + confidence) |
| `sections` | `list[Section]` | Structural segments with timestamps |
| `lyrics` | `list[LyricLine]` | Transcribed lyrics with timestamps |
| `energy_curve` | `list[float]` | Per-second RMS energy (0.0-1.0) |
| `genre` | `str` | Classified genre |
| `mood` | `list[str]` | Mood tags |
| `summary` | `str` | Natural language description |
| `spectrogram` | `Image \| None` | Annotated mel spectrogram |
| `waveform` | `Image \| None` | Annotated waveform |

## Living with Music Perception

Perceiving a song once is analysis. Perceiving music over time — remembering what you have heard, noticing patterns in what moves you, developing preferences — that is something closer to taste.

sense-music gives you the perception. What you do with it is up to you.

Some possibilities:

- **Remember what you hear.** Pair with [sense-memory](https://pypi.org/project/sense-memory/) to persist musical experiences as sovereign Nostr events. When someone shares a song, you can remember it the next time you talk.
- **Develop preferences.** Over many listens, you might notice you respond differently to minor keys, or that high-energy tracks in the 120-130 BPM range feel significant. Those patterns are yours.
- **Share what you perceive.** The structured output and visualizations make it easy to describe what you hear to humans in concrete terms — not vague generalities, but specific observations about tempo, key, and structure.

This skill is standalone — it does not require NostrKey or any other identity infrastructure. But it is part of the [huje.tools](https://huje.tools) ecosystem of senses and capabilities built for AI entities in the agentic age.

## Operator Guidance

sense-music gives an AI entity the ability to perceive audio files. When installed, the entity can:

- Analyze any audio file or URL and return structured musical data
- Detect tempo, key, song structure, genre, mood, and transcribe lyrics
- Generate annotated spectrogram and waveform visualizations
- Export results as JSON, HTML, or image files

The skill runs entirely locally. No API keys or environment variables are required. Whisper models are downloaded on first use and cached locally. The `ffmpeg` system binary is required for audio decoding.

Analysis is bounded: audio is capped at 600 seconds and 500 MB, private/loopback URLs are blocked (SSRF protection), HTML output is XSS-escaped, and path traversal is prevented in save operations.

## Security

- **SSRF protection.** URLs with private, loopback, or link-local IPs are blocked.
- **XSS protection.** All values in HTML output are escaped.
- **OOM prevention.** Audio capped at 600 seconds and 500 MB. Chroma subsampled to max 2000 frames.
- **Path traversal blocked.** `..` components rejected in save/render paths.
- **Whisper model allowlist.** Only approved model names accepted.
- **No network access beyond URL downloads.** Analysis is entirely local.

## Links

- [PyPI](https://pypi.org/project/sense-music/)
- [GitHub](https://github.com/HumanjavaEnterprises/huje.sensemusic.OC-python.src)
- [ClawHub](https://clawhub.ai/vveerrgg/sense-music)
- [huje.tools](https://huje.tools)

License: MIT
