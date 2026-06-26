---
name: reelsmith
description: Create short-form vertical video packages, preview reels, narrated reels, and AI-video workflows from ideas, articles, updates, or source material. Use when the user wants a topic turned into a short-form video concept, hook, script, scene-by-scene plan, on-screen text, caption, cover concept, approval-ready reel package, rough vertical preview video, narrated reel, or an LTX-powered AI video option for Facebook Reels and similar social formats.
---

# Reelsmith

## Overview

Use this skill to turn a topic into a **Facebook Reels-ready content package**.
The output should feel like a practical creator workflow, not just a block of text.

Treat the core unit as:
- hook
- short script
- scene breakdown
- on-screen text
- caption
- visual plan
- approval before posting or production

## Core Workflow

1. Identify the topic and goal.
   - Accept sports updates, news summaries, explainers, product demos, quick opinions, event recaps, or promotional ideas.
   - Figure out whether the reel should:
     - inform
     - react
     - explain
     - promote
     - recap

2. Identify the target style.
   - Common modes:
     - informative
     - energetic
     - professional
     - punchy
     - promotional
   - If the user does not specify, default to **informative + engaging**.

3. Decide the reel length.
   - Default to **30-45 seconds**.
   - Shorter is usually better unless the topic clearly needs more room.

4. Write a strong hook.
   - The first line should make the viewer care immediately.
   - Prefer clarity over empty hype.
   - Hooks should sound natural when spoken aloud.

5. Build the short-form script.
   - Keep sentences short and speakable.
   - Avoid overloading the reel with too many facts.
   - Focus on the strongest 2-4 points only.

6. Break the script into scenes.
   - Each scene should have:
     - what is being said
     - what is shown
     - optional on-screen text
   - Prefer 4-7 scenes for a normal reel.

7. Add packaging elements.
   - Include:
     - caption
     - light hashtag suggestions
     - cover/thumbnail concept
     - optional visual prompt ideas

8. Keep it approval-first.
   - Do not assume the user wants to publish immediately.
   - Present the reel package clearly so it can be reviewed, revised, or later turned into a produced video.

## Output Format

Unless the user asks for something else, use this structure:

**Reel concept:** [one-line concept]
**Tone:** [tone]
**Length:** [estimated seconds]

**Hook**
[hook]

**Script**
[full short-form script]

**Scene breakdown**
1. [scene 1 visual + spoken line + on-screen text]
2. [scene 2 visual + spoken line + on-screen text]
3. [scene 3 visual + spoken line + on-screen text]

**Caption**
[caption]

**Hashtags**
[list]

**Cover concept**
[headline + visual direction]

**Approval status**
Awaiting user approval before production or publishing

## Writing Rules

- Optimize for spoken clarity.
- Write in a way that sounds natural aloud.
- Keep hooks sharp.
- Avoid bloated intros.
- Avoid stuffing too many facts into a short reel.
- Prefer memorable structure over exhaustive detail.

## Reel-Specific Guidance

- Strong reel openings usually happen in the first 1-2 lines.
- Good reels often work best when they answer one clear question.
- If the topic is dense, simplify instead of cramming.
- If the user wants more depth, create a series or a longer script rather than overpacking one reel.

## Visual Guidance

If the user wants visuals, offer:
- scene image concepts
- thumbnail/cover concept
- on-screen headline text
- optional B-roll ideas

Do not assume full video automation exists yet. In v1, focus on producing a strong reel package that could later be recorded, edited, or automated.

## Preview Generation

There are now two preview paths:

### 1. Text-card preview
A simple preview path can use `scripts/make_reel_preview.py` to turn scene text into a rough vertical MP4 preview. This is for pacing and structure review, not final polished production.

Example flow:
1. save scene text into a file with one scene per paragraph
2. run:

```bash
python3 scripts/make_reel_preview.py --title "My Reel" --scenes-file scenes.txt --output preview.mp4
```

### 2. Visual scene preview
For a less slideshow-like reel, use `scripts/make_visual_reel_preview.py` with scene JSON that points to per-scene background images. This keeps the old workflow intact while allowing a more video-like look with motion backgrounds and lighter text overlay.

Scene JSON shape:

```json
[
  {"bg": "/path/to/image1.png", "title": "Main title", "subtitle": "Short support line", "duration": 5.0},
  {"bg": "/path/to/image2.png", "title": "Next beat", "subtitle": "Another short line", "duration": 5.0}
]
```

Run:

```bash
python3 scripts/make_visual_reel_preview.py --scenes-json scenes.json --output preview.mp4
```

## Voiceover-Ready Workflow

The next production layer can add narration audio, then mux it with the preview video.

Current helpers:
- `scripts/openai_tts.py`
- `scripts/mux_reel_audio.py`

Example flow:
1. generate narration audio with OpenAI TTS

```bash
python3 scripts/openai_tts.py --text "Your reel narration" --style energetic --output narration.mp3
```

2. mux it with the preview video

```bash
python3 scripts/mux_reel_audio.py --video preview.mp4 --audio narration.mp3 --output preview-with-audio.mp4
```

Expected env var:
- `OPENAI_API_KEY`

Current voice style presets:
- `default`
- `calm`
- `professional`
- `energetic`
- `confident`
- `broadcast`

For sports and fast-moving updates, prefer:
- `energetic`
- `broadcast`
- `confident`

This keeps voiceover modular: script generation, preview assembly, narration generation, then final mux.

## LTX Video Backend (Optional)

For a true AI-generated video option, Reelsmith can also use LTX via API instead of the local ffmpeg preview path.

Current helper:
- `scripts/ltx_text_to_video.py`

Example:

```bash
python3 scripts/ltx_text_to_video.py \
  --prompt "A cinematic vertical sports video showing a high-stakes college basketball showdown, dramatic arena lighting, crowd energy, and bold camera movement" \
  --duration 8 \
  --resolution 1080x1920 \
  --output ltx-video.mp4
```

Expected env var:
- `LTX_API_KEY`

Recommended starting defaults:
- model: `ltx-2-3-fast`
- resolution: `1080x1920`
- duration: `8` or `10`

Use LTX mode when the user wants a reel to feel like a generated video instead of a slide-based preview.

## Suggested Next Steps

After generating a reel package, offer one useful next step such as:
- "Want a punchier hook?"
- "Want this turned into a 20-second version?"
- "Want a matching cover image?"
- "Want a rough preview video?"
- "Want this adapted for YouTube Shorts too?"
