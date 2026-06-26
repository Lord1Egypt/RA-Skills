---
name: social-video-distill
description: Distill public social-video and short-form media with AI-first delegation. Use when the user shares a YouTube, Facebook, Instagram, TikTok, X, or local clip and wants a fast transcript, summary, humor read, best line, caption ideas, or theme extraction. Prefer platform captions and browser AI such as Gemini or NotebookLM before local ASR; use local transcription only as a fallback when faster cloud/browser routes are unavailable.
---

# Social Video Distill

Distill short-form video without defaulting to local heavy lifting.

Prefer the fastest capable specialist first: existing captions, browser AI, then local fallback.

## Workflow Decision Tree

1. Clarify the output target.
   - Transcript only
   - Concise summary
   - Humor read / joke structure
   - Best line / key moment
   - Suggested caption or reply

2. Choose the lightest viable input path.
   - If the user already pasted a transcript: skip retrieval and distill directly.
   - If the platform likely exposes captions: use `scripts/extract_captions.sh` first.
   - If captions are missing but a browser AI session is available: use Gemini for distillation of any rough transcript, notes, or manually recovered dialogue.
   - If the task truly needs raw media and no better route exists: download media with `scripts/download_media.sh` and use a transcription fallback outside this skill.

3. Distill with browser AI before using local ASR when the goal is understanding rather than archival transcript quality.
   - Quick single-clip distillation: Gemini.
   - Multi-source/theme synthesis: NotebookLM.

4. Verify the result.
   - Separate direct transcript from inference.
   - If captions were unavailable and a rough transcript was used, say so.
   - Quote the strongest line exactly when possible.

## Quick Start

Install local helper runtimes once:

```bash
bash skills/social-video-distill/scripts/install_runtime.sh
```

Try captions first:

```bash
bash skills/social-video-distill/scripts/extract_captions.sh 'https://example.com/video'
```

Download media only when needed:

```bash
bash skills/social-video-distill/scripts/download_media.sh 'https://example.com/video'
```

Ask Gemini to distill a prepared transcript or notes file:

```bash
node skills/social-video-distill/scripts/ask_gemini_cdp.js \
  --prompt-file /absolute/path/to/prompt.txt
```

## Preferred Operating Pattern

### 1. Caption-first retrieval

Use `extract_captions.sh` before downloading full media.

Good fit:
- YouTube videos with manual or auto captions
- platforms where `yt-dlp` can expose subtitles without full download

If captions exist:
- clean the text lightly
- keep timestamps only if they help the task
- send the cleaned transcript to Gemini or distill directly

### 2. Browser-first distillation

Use Gemini when the job is:
- explain what this clip is saying
- summarize the point
- identify why it is funny
- extract the punchline
- draft a caption/reply

Use `scripts/ask_gemini_cdp.js` with a focused prompt file. Keep prompts short and task-specific.

If the user wants study-guide style synthesis across multiple clips or mixed sources, use NotebookLM instead of forcing Gemini into a long single-shot prompt.

### 3. Local fallback only when necessary

Use local ASR only when:
- captions are unavailable
- browser AI cannot access the content
- the user explicitly wants a transcript and not just a distillation

Do not lead with local Whisper/faster-whisper just because it is available.

## Output Guidance

Default to a compact result with these fields when helpful:
- **What it says**
- **What is directly supported**
- **What is inferred**
- **Best line**
- **Why it lands**

For humor requests, prefer:
1. premise
2. escalation/twist
3. punchline

For social reply requests, give 2-3 options max.

## When to Read References

- Read `references/prompts.md` for ready-to-use distillation prompts.
- Read `references/troubleshooting.md` when captions, CDP, or Gemini interaction fails.
