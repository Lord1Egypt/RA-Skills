---
name: video-prompt-reverse-engineer
version: 3.1.0
emoji: "🎬"
description: "Reverse-engineer AI video prompts from any video or screenshot. Analyzes shot types, camera movements, lighting, color grading, and director style. Outputs structured prompts for Kling, Seedance, Runway, Veo, Sora, Pika, HappyHorse and more. Includes full reproduction workflow. Use when user provides a video link, screenshot, or description and wants to replicate its style."
---

# Auto Video Prompt Reverse Engineer v3.0

Advanced AI video prompt reverse engineering. Input video/screenshot/description → structured prompts + reproduction workflow.

## When This Skill Triggers

User provides any of:
- Video link (Bilibili, YouTube, TikTok, Xinpianchang, etc.)
- Video file or screenshot(s)
- Text description of a video's visual style
- Request to analyze, deconstruct, replicate, or reverse-engineer a video

## Analysis Rules — Every Shot Must Include

| Dimension | Required Analysis |
|---|---|
| Shot Type | ECU / CU / MCU / MS / MWS / WS / EWS |
| Camera Movement | Static / Pan / Tilt / Dolly / Tracking / Crane / Handheld / Orbit / Zoom / Speed Ramp / Snap Zoom / Whip Pan |
| Composition | Rule of thirds / Centered / Symmetrical / Leading lines / Dutch angle / Low angle / Over-shoulder |
| Lighting | Natural / Studio / Neon / Volumetric / Rim / Backlit / High-key / Low-key / Spotlight / Strobe / Muzzle flash |
| Color | Palette name, color temperature (warm/cool), contrast curve, saturation level |
| Subject Motion | Walking / Running / Dancing / Falling / Turning / Slow motion / Freeze frame |
| Depth of Field | Shallow / Deep / Rack focus |
| Texture | Film grain / CGI / Ultra realistic / Painted / Pixel art |
| Temporal | Normal speed / Slow motion / Time-lapse / Freeze frame |

## Style Identification Checklist

Must identify ALL that apply:
- **Director style**: Nolan, Villeneuve, Refn, Deakins, Wes Anderson, Snyder, etc.
- **Film genre**: Cyberpunk, Atomic Punk, Film Noir, Neo-western, Post-apocalyptic, etc.
- **Animation style**: Anime, cel-shaded, stop-motion, etc.
- **CG style**: Photoreal, stylized, low-poly, etc.
- **Commercial style**: Product hero, lifestyle, fashion, tech reveal
- **AI artifacts**: Temporal flicker, morphing faces, smooth physics, perfect lighting, etc.
- **Color grading**: Teal-orange, bleach bypass, film noir, vaporwave, golden hour, kodachrome, etc.
- **Lens style**: Anamorphic flare, tilt-shift, bokeh characteristics, focal length
- **Film stock**: Kodak Portra, Fuji Pro, Kodachrome, etc.

## Model Estimation

Identify likely AI model(s) used:
- **Kling**: Smooth motion, Chinese prompt friendly, good physics
- **Seedance (小云雀)**: Audio-visual sync, immersive short film mode, character consistency
- **Runway Gen-3**: Camera controls (Pan, Zoom, Roll), cinematic quality
- **Veo**: Advanced cinematographic natural language understanding
- **Sora**: Narrative prompts, long duration, complex physics
- **Pika**: Short clips, motion parameter control
- **SVD**: Image-to-video, motion_bucket_id control
- **Wan/CogVideoX**: Chinese-optimized, shorter clips
- **Midjourney/Flux**: Keyframe generation (not video)

## Prompt Reverse Engineering Template

For EACH shot, output:

### Shot XX
**Content:** [what's happening]  
**Camera Language:** [shot type + composition]  
**Motion:** [camera movement type]  
**Lighting:** [lighting setup]  
**Color:** [palette + temperature]  
**Material/Texture:** [film grain / CGI / realistic]  
**Subject Action:** [what the subject does]

`
Positive Prompt: [structured prompt: Subject + Action + Environment + Camera + Lighting + Color Grade + Style + Technical]
Negative Prompt: [what to exclude]
Camera Prompt: [lens focal length, movement, angle]
Style Prompt: [director reference, film stock, genre]
Lighting Prompt: [specific lighting setup]
Parameters: [aspect ratio, FPS, motion scale, CFG, model]
`

## Output Format

Use this structure for every analysis:

`
# Video Overall Style Analysis

## Video Type
- [Short film / Commercial / MV / Documentary / etc.]

## Overall Style
- [Atomic Punk + Post-apocalyptic Western / Cyberpunk / etc.]

## Director Reference
- [Most similar director(s) and why]

## Editing Rhythm
- [Slow build / Fast cuts / Montage / etc.]

## Estimated AI Model(s)
- [Primary model + supporting tools]

## AI Generation Artifacts Detected
- [List specific tells]

---

# Shot Breakdown

## Shot 01
[Full analysis per template above]

## Shot 02
[Continue for ALL key shots]

---

# Global Reverse-Engineered Prompts

## Global Style Prompt (applies to all shots)
`
[Master style anchor prompt]
`

## Global Negative Prompt
`
[What to always exclude]
`

## Global Camera Prompt
`
[Default lens, movement vocabulary, aspect ratio]
`

---

# Parameter Estimation

| Parameter | Value |
|---|---|
| Aspect Ratio | [e.g. 2.39:1] |
| FPS | [e.g. 24fps cinematic] |
| Lens Range | [e.g. 24mm-85mm] |
| LUT Style | [e.g. Bleach Bypass Warm] |
| Color Temperature | [e.g. 4500K warm] |
| Depth of Field | [e.g. Shallow f/1.4-2.8 for CU, Deep f/8-11 for WS] |
| Shutter Feel | [e.g. 180-degree shutter, 1/48s at 24fps] |
| Film Grain | [e.g. Medium, 35mm Tri-X 400 punch] |
| Primary Model | [e.g. Seedance 2.0] |
| Secondary Tools | [e.g. Midjourney for keyframes, DaVinci for grade] |

---

# Reproduction Workflow

1. **Keyframe Generation** → Midjourney / Flux → Generate character concept art + scene reference images
2. **Video Generation** → Choose based on style:
   - **Ads / Product / Tech**: HappyHorse (快马) — Best for advertising & futuristic tech style
   - **Narrative / Short Film**: Kling / Seedance / Runway → Text + reference image to video
   - **Creative / Art**: Veo / Sora → Complex cinematic scenes
   - **Quick iteration**: Pika / SVD → Short clips, rapid testing
3. **Director Method** → Write director-style prompts (WHY characters do things, not just WHAT)
4. **Audio Sync** → Seedance immersive mode for audio-visual sync / manual foley / HappyHorse dialogue support
5. **Color Grade** → DaVinci Resolve → Match LUT, cascade correction
6. **Enhance** → Topaz Video AI → Upscale + denoise + stabilize
7. **Compose** → Premiere / Final Cut → Edit, rhythm cuts, music sync
8. **Final Pass** → Film grain overlay, letterboxing, sound mix

### HappyHorse Prompt Optimization Rules

When generating HappyHorse prompts, apply these transformations:
- **Remove negatives**: Replace "no helmet" → "helmet removed, resting on metal stand beside"
- **Visual substitution**: Replace "back to camera" → describe what the back LOOKS LIKE (helmet top reflecting light, shoulder armor V-shape)
- **Three-level shot control**: [Shot type] + [Angle anchor] + [1-2 micro details]
- **Cinematic keywords**: Always append quality tags (cinematic quality, film grain, etc.)
- **Chinese content**: Write prompts in Chinese for best results
- **Prompt length**: 50-150 characters optimal; too long causes semantic drift
- **No dialogue by default**: Only add dialogue when user explicitly requests it
- **Dialogue duration estimation**: Slow speech ≈ 3-4 chars/sec, normal ≈ 5-6 chars/sec; always leave 1-2s buffer for transitions
`

## Pro Tips (from real creators)

- **Tell AI WHY, not just WHAT**: "Character presses hat down because wind might blow it off" > "Character presses hat"
- **Use non-human characters** to bypass uncanny valley (robots, pixels, masks)
- **Don't draw storyboards**: Use scene reference image + character image + text direction
- **Keep AI surprises**: When generation gives unexpected good results, fold them into narrative
- **Credit your models**: List all AI tools used, treat them as "cast and crew"
- **Multiple takes**: Generate 10-20 variations per shot, select the best action/rhythm

## References

See [references/model_params.md](references/model_params.md) for model parameters, lens focal lengths, and color grading keyword reference.