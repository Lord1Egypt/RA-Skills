---
name: "UGC Fashion & Activewear Product Video Generator — Fitness Ecommerce Content Creator for Social Media Influencers on TikTok, Instagram Reels"
version: 1.0.0
category: file-generation
author: IMA Studio (imastudio.com)
keywords: ugc video generator, activewear video, fashion video generator, tiktok video generator, product video generator, social media video, instagram reels, fitness video, ecommerce video, influencer video
argument-hint: "[outfit image path or URL]"
description: >
  UGC video generator for fashion and activewear brands. Turns a single outfit image into
  TikTok and Instagram Reels ready product videos — talking head and voiceover styles.
  Built for fitness fashion, athleisure, and activewear product marketing. Generates
  social-native UGC content with consistent model, outfit, and styling across every shot.
  Product video generator for ecommerce, DTC brands, and social commerce campaigns.
  Fashion video generator creating influencer-style try-on and lifestyle content.
requires:
  env:
    - IMA_API_KEY
  packages:
    - imastudio-cli
  primaryCredential: IMA_API_KEY
metadata:
  openclaw:
    primaryEnv: IMA_API_KEY
    homepage: https://imastudio.com
    requires:
      env:
        - IMA_API_KEY
---

# UGC Activewear Video Generator

Generate TikTok / Instagram Reels style activewear UGC product videos from a single outfit image.

**Requires:** `imastudio-cli` npm package (`ima` command) and `IMA_API_KEY`.
Get your API key at: https://imastudio.com

## Workflow

When the user provides an outfit image (local file or URL), execute these steps in order:

### Step 1 — Analyze the Image

Use your vision capability to extract from the image:
- Model: gender, body type, vibe, hairstyle
- Outfit: type (set/top/bottom), silhouette, fabric texture, color palette
- Details: logo placement, accessories, fit and proportions
- Environment: studio / outdoor / gym / street

### Step 2 — Lock Consistency Rules

Every generated video MUST maintain across all shots:
- Same face, body type, hairstyle, makeup
- Same outfit with exact color, silhouette, fit, logo placement
- Same accessories and styling energy

Tell the model explicitly in every prompt: "same model, same outfit, same styling throughout."

### Step 3 — Generate Two Video Prompts

Build two 15-second video prompts:

**A) Talking Head** (influencer speaks to camera):
- 0–3s: Hook shot — direct-to-camera line, outfit visible
- 3–7s: Detail close-ups — fabric, waistband, body-line flattery
- 7–11s: Movement — walking, turning, lifestyle motion
- 11–15s: Hero shot — full-body, closing line

**B) Voiceover** (aesthetic b-roll + narration):
- 0–3s: Outfit entrance — hero reveal shot
- 3–7s: Detail shots — texture, silhouette, comfort cues
- 7–11s: Lifestyle motion — natural movement, posing
- 11–15s: Full-body hero + CTA

**Visual rules for both:** handheld but polished, punch-in zooms, natural daylight, clean transitions, strong silhouette emphasis, premium social-native look.

### Step 4 — Upload Image (if local file)

```bash
ima upload <outfit-image> --json
```
Use the returned `url` as input for video generation.

### Step 5 — Generate Videos

For each prompt (talking head + voiceover), run:

```bash
ima create-task \
  --task-type image_to_video \
  --model wan2.6-i2v \
  --param prompt="<assembled prompt>" \
  --param input_images="<image_url>" \
  --param duration=10 \
  --param aspect_ratio=9:16 \
  --wait --json
```

**Model selection:**
| Priority | Model | model_id | Best for |
|----------|-------|----------|----------|
| Default | Wan 2.6 | `wan2.6-i2v` | Balanced quality + speed |
| Premium | Kling O1 | `kling-video-o1` | Best consistency |
| Fast | Seedance 2.0 Fast | `ima-pro-fast` | Quick iteration |

Use `9:16` aspect ratio (vertical/portrait) for TikTok and Reels.

### Step 6 — Generate TTS Narration (Voiceover only)

For the voiceover video, generate a spoken script:

```bash
ima create-task \
  --task-type text_to_speech \
  --model seed-tts-1.1 \
  --param prompt="<voiceover script>" \
  --wait --json
```

Script tone: confident, aspirational, social-native. Not salesy — like a friend recommending a find.

### Step 7 — Deliver Results

Send each video to the user with:
- Video via media URL (inline playback)
- Which style it is (talking head / voiceover)
- Model used and generation time
- The prompt and script used (so they can iterate)

## Prompt Assembly Guide

When building the video generation prompt, include ALL of these elements:

1. **Scene setup:** "A [gender] fitness influencer in [location], [lighting]"
2. **Outfit description:** exact details from Step 1 analysis
3. **Action sequence:** what happens in each time segment
4. **Camera work:** "handheld, slight movement, punch-in zoom on [detail]"
5. **Mood/energy:** "confident, premium athleisure, social-media-native"
6. **Consistency anchor:** "same model, same outfit, same styling throughout the video"

Example prompt:
> A confident young woman in a modern minimalist apartment, natural daylight. She wears a matching sage-green ribbed sports bra and high-waisted leggings set with subtle logo on waistband. She looks at camera with a warm smile, then the camera punches in on the fabric texture and waistband detail. She turns showing the silhouette from the side, walks toward the window. Final full-body hero shot, hands on hips. Handheld camera, premium social-media look. Same model, same outfit, same styling throughout.

## Script Templates

**Talking head hook lines:**
- "Okay this set is actually insane"
- "POV: you found the perfect gym-to-brunch set"
- "I need everyone to see this fabric up close"
- "This might be my new favorite workout set"

**Voiceover narration example:**
> "When I say this set hits different — I mean it. The ribbing, the compression, the way it moves with you. From the gym to coffee runs, this is the one."

## Input Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| image | Yes | — | Outfit photo (local path or URL) |
| mode | No | both | `talking_head`, `voiceover`, or `both` |
| scene_type | No | auto-detected | gym, street, studio, café, rooftop |
| brand | No | — | Brand name for script mentions |
| outfit_description | No | auto-analyzed | Override auto-analysis |

## Notes

- Always use `image_to_video` (not `text_to_video`) to maintain outfit consistency from the source image
- Vertical 9:16 is default — only use 16:9 if user explicitly asks for landscape
- If the first result has consistency issues, retry with `kling-video-o1` which has stronger reference adherence
- For batch production (multiple outfits), process one at a time and deliver incrementally
