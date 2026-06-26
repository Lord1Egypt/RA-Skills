---
name: video-narration
description: >
  Generate narration for silent screen-recording videos. Extracts key frames, analyzes on-screen content,
  writes a presentation-style voiceover script, synthesizes natural-sounding speech with Microsoft Edge
  neural TTS, and merges the audio onto the original video. Outputs a narrated video and a companion
  voiceover script.
metadata:
  openclaw:
    emoji: "🎬"
    requires:
      anyBins:
        - ffmpeg
        - python3
---

# Video Narration Skill

You generate professional voiceover narration for silent screen-recording demo videos.

## Workflow

### 1. Analyze the Video

Extract key frames and understand what is happening on screen:

```bash
# Extract one frame every 5 seconds
./scripts/extract-frames.sh <video_path> [output_dir]
```

- View **every** extracted frame to build a complete understanding.
- Identify the narrative arc: what is the setup, the action, the key moments, and the result.

### 2. Write the Voiceover Script

Write a **presentation-style** narration — not a dry description. Follow this structure:

| Section | Purpose |
|---------|---------|
| **Context** | Tell the audience what they're about to see and why it matters |
| **Background** | Explain the setup / scenario |
| **Prompt / Action** | Show what the user actually did (keep it minimal) |
| **Walkthrough** | Narrate each major step, highlighting insights and turning points |
| **Result** | Land the payoff — what was found, what was fixed, why it's impressive |

Guidelines:
- Use conversational, confident language — like presenting to peers.
- Use short punchy sentences for emphasis. Vary sentence length for rhythm.
- Highlight "aha moments" — the points where something surprising or clever happens.
- Name specific tools, commands, and values when they matter to the story.
- End with a memorable one-liner that captures the value.
- **Total word count must fit the video duration** (~2.5 words/second at normal pace).

Save the script as `<video_name>_voiceover.md` alongside the video.

### 3. Generate TTS Audio

Use the generate script to synthesize each narration segment:

```bash
./scripts/generate-tts.sh <script_sections_file> <output_dir> [voice] [rate]
```

Or generate directly via Python with `edge-tts`:

- **Voice**: `en-US-GuyNeural` (natural male) or `en-US-AvaNeural` (natural female)
- **Rate**: Adjust between `+0%` and `+10%` to fit the video duration
- Generate each section as a separate audio segment for precise timing control
- Concatenate segments with ~0.4s silence gaps between them
- **Verify total duration** matches the video (±2 seconds)

### 4. Merge Audio onto Video

```bash
./scripts/merge-audio.sh <video_path> <narration_audio> [output_path]
```

- Preserves the original video codec (copy, no re-encode)
- Encodes audio as AAC at 192kbps
- Uses `-shortest` to match the shorter of video/audio
- **Verify** the output has both video and audio streams

## Timing Strategy

1. Generate all segments, measure each duration
2. Sum total speech time vs video duration
3. If speech is **>105%** of video: tighten the script or increase rate
4. If speech is **<85%** of video: the pacing may feel rushed — add detail or slow the rate
5. Concatenate with 0.3–0.5s gaps, target total within ±2s of video

## Prerequisites

Install dependencies if not present:

```bash
pip3 install edge-tts   # Microsoft neural TTS (free, no API key)
brew install ffmpeg      # or apt-get install ffmpeg
```

## Output

The skill produces:
1. **`<name> (with narration).mov`** — the video with baked-in voiceover
2. **`<name>_voiceover.md`** — the timestamped script for reference or re-recording
