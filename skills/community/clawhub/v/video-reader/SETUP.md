# VideoARM First-Run Setup

This guide runs once. After completion, `~/.videoarm/.installed` is created and skipped on future use.

## Welcome Message

Print this to the user before starting configuration. Translate to match the user's conversation language if not English:

---

**🎬 VideoARM — Agentic Video Question Answering**

VideoARM is a tool-driven video understanding system. It downloads videos, extracts visual frames and audio transcripts, then uses AI reasoning to answer questions about video content.

**What it can do:**
- Answer questions about any YouTube or local video
- Analyze visual scenes and spoken dialogue
- Handle multiple-choice and open-ended questions
- Auto-detect video language for transcription

**How it works:**
1. Downloads the video (YouTube, Bilibili, or local file)
2. Extracts key frames for visual analysis
3. Transcribes audio using Whisper (language auto-detected)
4. Combines visual + audio evidence to answer your question

Let's get you set up — just 2 quick questions.

---

## Step 1: Check Dependencies

Run `videoarm-doctor`. All ✅ → continue. Any ❌ → tell user what to install and stop.

## Step 2: Configure `.env`

If `<skill-path>/.env` does not exist, copy from `.env.example`.

Language is auto-detected — no configuration needed.

Ask questions **one at a time**:

### 1. Proxy
> "Do you need a network proxy to download videos? (Required in some regions for YouTube/Bilibili access)"
> - If yes → "What's your proxy address? (e.g. `http://127.0.0.1:7890`)"
> - If no → leave `HTTPS_PROXY` commented out

### 2. Transcription Model
> "Which local Whisper model would you like to use?"
> - `base` (default) — fast, good accuracy, low memory
> - `small` — better for accented or non-English speech
> - `medium` — high accuracy, slower
> - `large-v3` — best accuracy, requires more RAM
>
> "Press enter to use the default (`base`)."

## Step 3: Verify

Run `videoarm-doctor` once more to confirm everything is ready.

## Step 4: Mark Complete

```bash
mkdir -p ~/.videoarm && touch ~/.videoarm/.installed
```

Tell the user: "✅ VideoARM is ready! Send me a video link + question and I'll analyze it for you."
