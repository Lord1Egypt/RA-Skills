---
name: video-to-markdown
description: Analyze any YouTube, Facebook, or Instagram video URL and generate a comprehensive Markdown reference document by combining AI vision analysis of extracted frames with full video transcription. Use this skill when a user shares a video URL and wants a summary, notes, breakdown, or reference document from it. Triggers on "analyze this video", "summarize this video", "break down this video", "create notes from this video", "watch this video and explain it", "video to markdown", "pull notes from this", or any request to extract knowledge from a video. Also triggers automatically when a user pastes a YouTube, Instagram, or Facebook URL and asks what it's about or wants to understand its content — even without explicit keywords. Especially valuable for educational content, trading tutorials, technical demos, or any video where charts, diagrams, and on-screen visuals tell a different story than the narration alone.
---

# video-to-markdown

Extracts key frames + transcript from a video, sends both to Claude vision, and produces a structured Markdown document that captures everything the video teaches — including what's shown on screen but not fully explained verbally.

## Quick reference

```
python scripts/video_analyzer.py "<URL>" [--output DIR] [--max-frames N] [--cookies FILE] [--whisper]
```

Output: a `.md` file in the output directory.

---

## Step-by-step

### 1. Get the URL

Confirm the video URL from the user. Supported: YouTube, Facebook, Instagram (and most other sites yt-dlp handles).

### 2. Check dependencies

Run the preflight check:

```bash
ffmpeg -version && yt-dlp --version && python3 -c "import anthropic, PIL; print('deps OK')"
```

If anything fails:

```bash
bash scripts/setup.sh
```

Also confirm `ANTHROPIC_API_KEY` is set:

```bash
echo $ANTHROPIC_API_KEY
```

If not set:
```bash
export ANTHROPIC_API_KEY=your_key_here
```

### 3. Run the analyzer

**Standard (YouTube, captions available):**
```bash
python scripts/video_analyzer.py "<URL>" --output ./output
```

**Trading / chart-heavy content (more frames, Whisper for accuracy):**
```bash
python scripts/video_analyzer.py "<URL>" --max-frames 80 --whisper --output ./output
```

**Talking-head / lecture (fewer frames, captions sufficient):**
```bash
python scripts/video_analyzer.py "<URL>" --max-frames 20 --output ./output
```

**Facebook or Instagram (cookies required):**
```bash
python scripts/video_analyzer.py "<URL>" --cookies /path/to/cookies.txt --output ./output
```

**Maximum quality (Opus model + large Whisper + more frames):**
```bash
python scripts/video_analyzer.py "<URL>" \
  --model claude-opus-4-20250514 \
  --whisper --whisper-model large-v3 \
  --max-frames 80 \
  --output ./output
```

### 4. Read and present the output

The script prints the output file path as its last line. Read it and present the contents to the user:

```bash
cat ./output/<filename>.md
```

---

## Flag reference

| Flag | Default | When to change |
|---|---|---|
| `--max-frames` | 50 | Lower (20–30) for talking-head; higher (60–80) for dense charts |
| `--whisper` | off | Use when no captions exist, or for jargon-heavy content |
| `--whisper-model` | base | `large-v3` for highest accuracy (slower, more RAM) |
| `--cookies` | none | Required for Facebook/Instagram; sometimes YouTube |
| `--model` | claude-sonnet-4-20250514 | `claude-opus-4-20250514` for complex visual analysis |
| `--output` | current dir | Set to a specific notes folder |

---

## Cost estimates (claude-sonnet-4-20250514)

| Video length | Frames | Approx. cost |
|---|---|---|
| 10 min | ~20 | ~$0.08 |
| 30 min | ~50 | ~$0.20 |
| 60 min | ~80 | ~$0.35 |

Use `--model claude-haiku-4-5-20251001` for ~5× lower cost when analysis quality is less critical.

---

## Platform-specific notes

See `references/platforms.md` for full detail on cookie setup for Facebook and Instagram.

Quick summary:
- **YouTube**: works without auth on residential IPs; needs cookies on cloud IPs
- **Instagram**: requires cookies; behavior is intermittent even with valid cookies
- **Facebook**: requires cookies **and** browser impersonation (handled automatically)

Cookie source: Firefox only (Chrome cookies encrypted since v127). Export from logged-in session on same IP you're running from.

---

## Output format

Each run produces a `.md` file with:

**YAML frontmatter:**
- Source URL, platform, title
- Analysis timestamp, frames analyzed, transcript source, model used

**Document body:**
- Overview
- Visual Content Summary
- Section Breakdown (said vs. shown per topic)
- Key Visuals Explained
- Key Takeaways
- Terms & Concepts
- Visual–Narration Gaps ← the section that makes this worth doing

---

## Troubleshooting

**"No frames extracted"** → Check ffmpeg is installed and the video downloaded to the temp dir. Try `--max-frames 10` on a short public YouTube video first.

**"No captions found" (and no Whisper)** → Normal for non-captioned videos. Install faster-whisper and add `--whisper`, or the analysis continues from frames alone.

**Facebook "Cannot parse data"** → Cookies may be stale or from a different IP. Re-export from Firefox immediately before use, same network.

**Instagram fails with cookies** → Intermittent. Wait a few minutes and retry. Try a different account if it persists.

**Output is too short / missing visuals** → Increase `--max-frames` or upgrade to `--model claude-opus-4-20250514`.

**High cost** → Reduce `--max-frames` to 20–30. Talking-head content rarely needs more than 20 frames.
