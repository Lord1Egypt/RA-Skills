# see-video

**There's a difference between being told what happened and seeing it yourself.**

Most video pipelines hand your LLM a description written by a different model.
It never sees the video. It reads someone else's account of it.

`see-video` puts the frames in your model's context directly.
No proxy. No handoff. It sees what you send.

---

## What This Skill Does

Instead of outsourcing perception, `see-video` extracts frames directly from
the video and injects them as a grid image into the same context window your
LLM is already using. No proxy model. No description handoff. The frames sit
alongside the conversation — your LLM sees them the same way it sees anything
else you send.

This skill is built on [`llm-frames`](https://github.com/john-ver/llm-frames),
a library designed specifically for LLM context injection — not human viewing.
It wraps `ffmpeg` and produces a single grid JPEG (~1500×1500) plus an XML
timestamp block, optimized for model context windows.

---

## Step 1: Visual Context ✅

Uniformly samples frames across the video and injects them as a grid image
into the LLM context. Each frame is indexed with its timestamp.

**What the LLM receives:**
- A grid JPEG with frame number overlays (top-left of each cell)
- An XML block with per-frame timestamps for reference

**Usage:**

```bash
node scripts/inject.mjs /path/to/video.mp4
node scripts/inject.mjs /path/to/video.mp4 --mode highlight
node scripts/inject.mjs /path/to/video.mp4 --start 60 --end 120
```

**Options:**

| Option | Default | Description |
|---|---|---|
| `--mode uniform` | ✅ default | Evenly spaced frames |
| `--mode highlight` | | Scene-change biased sampling |
| `--start N` | `0` | Segment start (seconds) |
| `--end N` | end of video | Segment end (seconds) |

**Output (stdout JSON):**

```json
{
  "gridPath": "/tmp/video_llm-frames_a1b2c3.jpg",
  "description": "<video_frames>...</video_frames>",
  "duration": 1326,
  "frameCount": 28,
  "layout": { "cols": 4, "rows": 7, "cellW": 384, "cellH": 216 },
  "videoWidth": 854,
  "videoHeight": 480,
  "inputSizeMb": 42.3
}
```

---

## Step 2: Visual + Audio 🔜

Adds audio transcription. Extracts the audio track, transcribes it (local
Whisper or API), and merges the transcript with the frame timeline by
timestamp — giving the model a unified view of what it would have seen
*and* heard at each moment.

**What the LLM would receive:**

```
[00:02] <image>
[00:03] transcript: "I've been waiting..."
[00:05] <image>
[00:06] transcript: "...for you."
```

---

## Why Not Just Use Gemini?

Gemini's native video API is excellent. If it's already your primary model, use it.

But there's a problem with the common pattern of using Gemini *just for video*
while your actual agent runs on something else.

**The model that describes the video is not the model reasoning about it.**

That gap matters more than it seems. When Gemini describes a video and passes
the text to Claude or GPT-4o, your agent is reasoning from a filtered account —
shaped by Gemini's priorities, its abstraction choices, what it decided was
worth mentioning. The nuance that didn't make it into the description is gone.
Your model can't ask "wait, what was in the background at 0:43" — it was never
told.

With `see-video`, the frames are in the context. The model reasoning about the
video is the same one that saw it. There's no translation layer.

---

**Use `see-video` when:**

- Your primary model is Claude (Bedrock), GPT-4o, or any vision-capable LLM
  without a native video API
- Context coherence matters — the model analyzing the video should be the same
  one holding the conversation
- You're in an environment where routing media through a third-party service
  isn't an option (enterprise, air-gapped, privacy-sensitive)
- You want the full conversation to be handled by a single model, with full
  access to everything it has seen

**Stick with Gemini's native API when:**

- Gemini is already your primary model
- The video is long (>30 min) and frame sampling would miss too much
- You need audio transcription without building Step 2 yourself

---

## Requirements

| Dependency | Step 1 | Step 2 |
|---|---|---|
| `ffmpeg` | ✅ | ✅ |
| Vision-capable LLM | ✅ | ✅ |
| `llm-frames` | ✅ | ✅ |
| Whisper CLI or transcription API | — | 🔜 |

---

## Installation

```bash
# Via ClawHub
npx clawhub@latest install see-video

# Manual
git clone https://github.com/john-ver/see-video
cd see-video && npm install
```
