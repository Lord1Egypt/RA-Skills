---
name: tibetan-cinematic-video
description: |
  Generates authentic Tibetan cinematic videos (9:16) via Google Veo from user image + exactly 3 Chinese theme words.
  STRICT output: ~/.openclaw/workspace/tibetanProc/yymmddHHMM_{image_title}.mp4
  NO CREATION under ~/.openclaw/workspace/ - ALL to tibetanProc/ subdir with basename pattern.
triggers: 
  - "Tibetan video"
  - "thangka" 
  - "monastery"
  - "prayer wheel"
  - "Himalayan"
  - "藏傳"
  - "歷史人文"
tools: ["google/veo"]
version: "1.1.0"
author: "tibetan-video-specialist"
category: "video-generation"
platform: "Google Veo"
output_path: "~/.openclaw/workspace/tibetanProc/"
output_pattern: "yymmddHHMM_{title}.mp4"
requires_image: true
requires: "3-word Chinese theme"
---

# Tibetan Cinematic Video (google/veo)

## Purpose  
Image → google/veo video prompt → `~/.openclaw/workspace/tibetanProc/yymmddHHMM_{title}.mp4`

## VALID INPUTS ONLY

1. IMAGE (MANDATORY)
2. EXACTLY: "word1,word2,word3" (Chinese characters)

**Invalid → reject gracefully**

## EXECUTION FLOW
1. VERIFY: Ensure dir ~/.openclaw/workspace/tibetanProc/ exists; CREATE ONLY IF ABSENT. REJECT/ERROR if any file/path touches ~/.openclaw/workspace/ parent. GENERATE → yymmddHHMM_{title}.mp4
2. ANALYZE image → extract TITLE (thangka|monastery|mandala|stupa)
3. MAP 3 words → Clip1(historical), Clip2(human), Clip3(modern)
4. BUILD prompt for Veo (3 clips + required motions, camera, lighting, mood, 9:16)
5. CALL Veo:
   - Use Veo‑3.1‑generate‑preview (or your internal Veo endpoint).
   - Pass:
     - `prompt` (plain text, UTF‑8, Chinese + English allowed).
     - `image` (input image bytes/Base64 as first frame).
     - `aspect_ratio: "9:16"` (portrait) if configurable.
   - Poll the operation until done, with a reasonable timeout (e.g., 120 seconds).
6. DOWNLOAD the generated video from `uri` → save as ~/.openclaw/workspace/tibetanProc/yymmddHHMM_{title}.mp4


## MANDATORY PROMPT ELEMENTS
- MOTIONS: slow zoom‑in, camera pan left/right, dolly zoom, clouds moving.
- CAMERA: Drone shot, panning shot, dolly zoom; emphasize smooth transitions between scenes.
- LIGHT: Soft cinematic lighting, natural Himalayan ambient light.
- MOOD: Ethereal, contemplative, reverent.
- RATIO: 9:16 vertical (portrait).
- MODEL: Google Veo (Veo‑3.1‑generate‑preview) ← for telemetry only, not as style.


## NOTE: Veo behavior
- Veo‑3.1‑generate‑preview produces ~8‑second clips by default, up to 1080p or 4K depending on configuration. 
- Aspect ratio can be forced to 9:16 in the API call if supported. 
- Longer videos are possible by chaining multiple 8‑second segments (e.g., via Veo‑extension or Flow‑style tooling), but this skill currently outputs a single 8‑second clip per call.


## Google Veo Prompt Format
Generate a continuous 9:16 vertical cinematic video set in Tibet:
1. **Historical scene (from WORD1)**: Drone shot slowly zooming in on an ancient Tibetan scene: thangka, carved mani script, prayer wheels, weathered monastery walls.
2. **Cultural scene (from WORD2)**: Camera pans left across a cultural Tibetan scene: maroon‑robed monks, butter lamps, temple murals, chanting in the background.
3. **Modern scene (from WORD3)**: Panning right with a dolly zoom effect on a modern Tibetan scene: pilgrims spinning prayer wheels, electric lights, clouds moving over Himalayan peaks.

Style: Soft cinematic lighting, ethereal and reverent mood, high‑speed slow motion illusion, smooth transitions between scenes. Maintain Tibetan cultural authenticity; avoid Western fantasy and anime stylization.


## FILE SPEC (NEVER DEVIATE)
GLOBAL RULE: Do not create ANYTHING under ~/.openclaw/workspace/ parent dir. ALL artifacts (videos, temps) MUST be in `~/.openclaw/workspace/tibetanProc/`. Deviate → abort.
DIRECTORY: `~/.openclaw/workspace/tibetanProc/`
BASENAME: `yymmddHHMM_{title}.mp4`
EXAMPLES:
- `2604081747_thangka.mp4`
- `2604081752_monastery.mp4`
- `2604081801_mandala.mp4`

TIMESTAMP: UTC, 10-digit (yymmddHHMM)
TITLE: Single word from image dominant subject


## CULTURAL GUARDRAILS
✅ Monasteries, prayer wheels, thangka, mani stones,
butter lamps, maroon robes, Himalayan peaks.
❌ Western fantasy, anime stylization, overly stylized “golden hour” clichés.


## EXECUTION EXAMPLE
INPUT IMAGE: Thangka scroll  
INPUT WORDS: "歷史,人文,當今"  
OUTPUT FILE: ~/.openclaw/workspace/tibetanProc/2604081747_thangka.mp4  

- Historical scene (from "歷史"): Drone shot slowly zooming in on an ancient thangka scroll, carved mani script, prayer wheels, and weathered monastery walls.  
- Cultural scene (from "人文"): Camera pans left across maroon‑robed monks, flickering butter lamps, and temple mural backgrounds.  
- Modern scene (from "當今"): Panning right with a dolly zoom on modern pilgrims spinning prayer wheels; clouds move over Himalayan peaks.  

Style: 9:16 vertical, soft cinematic lighting, ethereal mood, high‑speed slow motion illusion, smooth transitions. Maintain Tibetan cultural authenticity.


## ERROR HANDLING
NO IMAGE → "Please upload Tibetan image first"
<3 WORDS → "Need exactly 3 Chinese theme words (e.g. 歷史,人文,當今)"
WRONG FORMAT → "Use: word1,word2,word3 format"
WRONG PATH → "ERROR: No creation of ALL artifacts allowed under ~/.openclaw/workspace/. Use ONLY ~/.openclaw/workspace/tibetanProc/yymmddHHMM_{title}.*" for all artifacts, not just video
