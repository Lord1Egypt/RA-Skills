# Video AI Models & Cinematography Reference

## Video Generation Models Parameters

### Seedance (小云雀) 2.0
- Resolution: 720p / 1080p
- Duration: 5s / 10s / immersive short film mode
- Key Feature: Audio-visual sync generation (gun shots, metal clashes, engine roars generated natively)
- Immersive Short Film Mode: Generates multi-shot sequences with coherent narrative
- Character Consistency: Strong character consistency across shots with reference images
- Chinese prompt: Supported and recommended for Chinese-themed content

### Kling (可灵)
- Resolution: 720p / 1080p
- Aspect Ratio: 16:9 / 9:16 / 1:1
- Duration: 5s / 10s
- Mode: Standard / High Quality / Pro
- Motion Scale: 0-100 (low=stable, high=dramatic)
- Creativity: 0-100
- Multi-Shot: Supports multi-angle generation from single keyframe
- Chinese prompt: Native support, better results for Chinese content

### Runway Gen-3 Alpha
- Resolution: 720p / 1080p
- Aspect Ratio: 16:9 / 9:16
- Duration: 4s / 10s / 16s
- Camera Controls: Pan Left/Right, Zoom In/Out, Roll
- CFG: 1-15
- Motion: 0-10

### Veo (Google)
- Resolution: 720p / 1080p
- Aspect Ratio: 16:9 / 9:16
- Duration: 4s-60s+
- Advanced cinematic natural language understanding
- Best for: Long-form narrative, complex camera directions

### Sora (OpenAI)
- Resolution: 720p / 1080p
- Aspect Ratio: 16:9 / 9:16 / 1:1
- Duration: 5s-20s
- Variations support
- Best for: Narrative prompts, complex physics, longer clips

### Pika
- Resolution: 720p / 1080p
- Aspect Ratio: 16:9 / 9:16 / 1:1
- Duration: 3s / 4s
- Camera: Pan / Zoom / Rotate
- Params: motion / guidance_scale
- Best for: Short clips, quick iterations

### Stable Video Diffusion (SVD)
- Resolution: 512x512 / 768x512
- Frames: 14 / 25
- Motion: motion_bucket_id (1-255)
- CFG: 1-15
- FPS: 6-12
- Best for: Image-to-video workflows, ComfyUI pipelines

### Wan Video / CogVideoX
- Resolution: 480p / 720p
- Aspect Ratio: 16:9 / 9:16 / 1:1
- Duration: 5s / 6s
- Chinese prompt: Optimized for Chinese
- Best for: Chinese content generation

### Higgsfield
- Resolution: Up to 4K
- Style: Cinematic, film-like quality
- Best for: Music videos, high-production-value shorts

### HappyHorse (快马) — Ad & Tech Video Specialist
- Supported Ratios: 16:9 / 9:16 / 1:1
- Duration: 5s / 10s (customizable)
- Resolution: 720P / 1080P
- **Best For**: Advertising (product showcase, brand promo, e-commerce, promotional animation), Tech style (futuristic, digital effects, cyberpunk, chip/data visualization)
- **NOT For**: Daily vlog, comedy/pet, story-driven drama
- Prompt Language: Chinese preferred; English also works
- Key Differentiator: Built-in audio support (dialogue, voiceover, BGM with prosody notation)

#### HappyHorse Prompt Template

**Basic (T2V)**:
`
Subject + Scene + Motion
`

**Advanced**:
`
Subject (appearance detail) + Scene (environment detail) + Motion (amplitude/rate/effect) + Aesthetic Control + Style
`

**Cinematic Narrative (short film)**:
`
Scene atmosphere + Subject detail + Emotion/narrative + Camera movement + Film aesthetic tags
`

**With Audio**:
`
Subject + Scene + Motion + Sound description (dialogue/SFX/BGM)
`

#### HappyHorse Aesthetic Control Keywords

| Category | Keywords |
|----------|----------|
| Quality | cinematic quality / 8K ultra realistic / film grain texture / 35mm film look |
| Lighting | golden hour lighting / shallow depth of field / rim light / volumetric / side backlight |
| Color | muted vintage color palette / warm color temperature / noir aesthetic |
| Detail | visible skin pores / hair strand detail / metal reflection / fabric wrinkles |
| Camera | push in / pull out / low angle / FPV / fixed shot / depth shift / one-take |

#### HappyHorse Audio Prosody Notation

| Symbol | Function | Example |
|--------|----------|---------|
| ， | 0.25s pause | 自然停顿 |
| 。 | 0.3-0.5s breath | 收尾 |
| …… | 0.5-2s hesitation | 犹豫、恐惧 |
| —— | 0.5-1s stretch | 强调、转折 |
| ~ | Warble/trail | 娇媚、轻俏 |
| ! | Burst | 愤怒、惊喜 |
| ? | Rising tone | 疑问 |
| ?? | Suppressed anger | 想发火又忍住 |
| !? or ?! | Shock + rise | 震惊、质问 |
| [pause Xs] | System pause | Timing control |
| [breathless] | Voice quality | 声带状态 |
| <sob> | SFX | 非语言声音 |

#### HappyHorse Prompt Optimization Rules

1. **No negative words** — describe what you WANT (except audio: "no dialogue" is OK)
2. **Visual substitution** — replace abstract actions with visible elements
3. **Three-level shot control** — Macro (shot type) → Meso (angle + anchor) → Micro (detail)
4. **Disambiguate** — replace vague terms with measurable characteristics
5. **Chinese prompts** — better for Chinese content on HappyHorse
6. **Length control** — 50-150 characters optimal; longer = semantic drift
7. **No dialogue by default** — only when user explicitly requests
8. **Duration estimation** — slow speech: 3-4 chars/sec; normal: 5-6 chars/sec; leave 1-2s buffer

---

## Lens Focal Length Reference

| Focal Length | View Angle | Common Use | Prompt Keywords |
|---|---|---|---|
| 14mm | Ultra wide 114deg | Epic landscapes, architecture | ultra wide angle, 14mm lens, dramatic perspective |
| 24mm | Wide 84deg | Establishing shots, environments | wide angle, 24mm lens, expansive vista |
| 35mm | Wide-normal 63deg | Environmental portraits, street | 35mm lens, natural perspective, street |
| 50mm | Normal 47deg | Documentary, natural feel | 50mm lens, natural perspective, documentary style |
| 85mm | Medium tele 29deg | Portrait close-ups, isolation | 85mm lens, shallow DOF, portrait, bokeh |
| 135mm | Telephoto 18deg | Compressed distance, portraits | 135mm lens, compressed perspective, separation |
| 200mm+ | Super tele 12deg | Distance, sports, wildlife | 200mm telephoto, extreme compression, isolated subject |

### Anamorphic Lens Keywords
- anamorphic lens, 2x squeeze, oval bokeh, horizontal lens flare, anamorphic stretch
- Common: 35mm anamorphic, 50mm anamorphic, 75mm anamorphic

---

## Camera Movement Keywords

| Movement | Prompt Keywords |
|---|---|
| Static | static shot, locked camera, fixed frame |
| Push In | push in, dolly in, slow zoom in, creeping forward |
| Pull Out | pull out, dolly out, zoom out, reveal |
| Tracking | tracking shot, lateral dolly, following shot |
| Crane | crane up, crane down, rising shot |
| Handheld | handheld, shaky cam, documentary feel |
| Orbit | orbit shot, 360 orbit, revolving camera |
| Pan | pan left, pan right, horizontal sweep |
| Tilt | tilt up, tilt down, vertical sweep |
| Whip Pan | whip pan, fast pan, swish pan |
| Speed Ramp | speed ramp, slow to fast, fast to slow |
| Snap Zoom | snap zoom, crash zoom, sudden zoom |
| Rack Focus | rack focus, shift focus, pull focus |
| Drone | drone shot, aerial, bird's eye view |
| Steadicam | steadicam, smooth tracking, stabilized |

---

## Color Grading Styles

| Style | Characteristics | Keywords |
|---|---|---|
| Teal & Orange | Cool shadows, warm highlights | teal and orange, cinematic color grade, blockbuster look |
| Bleach Bypass | Low saturation, high contrast | bleach bypass, desaturated, high contrast, Saving Private Ryan |
| Film Noir | B&W high contrast, hard shadows | film noir, high contrast black and white, hard shadows, chiaroscuro |
| Vaporwave | Pink-purple neon gradients | vaporwave, retro neon, pink purple gradient |
| Cyberpunk | Neon blue-purple, rain reflections | cyberpunk, neon lighting, rain, reflections, Blade Runner |
| Atomic Punk | Retro-futuristic, warm amber, rust | atomic punk, retro future, warm amber, rust, mid-century futurism |
| Golden Hour | Warm golden tones, soft | golden hour, warm tones, soft light, magic hour |
| Moonlight | Cool blue tones, cold | moonlight, cool blue tones, cold night, desaturated blue |
| Kodachrome | High saturation warm, vivid | kodachrome, vibrant warm colors, saturated reds and yellows |
| Pastel | Soft muted colors | pastel, soft muted, dreamy, light tones |
| Monochrome | Single color or B&W | monochrome, black and white, single color tint |
| Cross Process | Unusual color shifts, high contrast green shadows | cross processed, unusual color shift, high contrast green shadows |
| Film Emulation | 500T, 250D, Ektachrome | cinema film stock, 500T tungsten, 250D daylight, Ektachrome, Kodak Vision3 |

---

## Lighting Keywords

| Lighting Type | Keywords |
|---|---|
| Natural | natural light, available light, ambient |
| Studio 3-Point | three point lighting, key fill back, studio lit |
| Rembrandt | Rembrandt lighting, triangle under eye, dramatic |
| Rim/Backlight | rim light, backlight, edge lighting, silhouette |
| Volumetric | volumetric light, god rays, light beams, haze |
| Neon | neon lighting, colored neon, sign glow |
| Spotlight | single spotlight, dramatic spotlight, stage lighting |
| High-Key | bright even lighting, high key, commercial look |
| Low-Key | moody dark lighting, low key, dramatic shadows |
| Strobe | strobe lighting, flashing light, flicker |
| Muzzle Flash | muzzle flash, gunshot flash, weapon fire |

---

## Film Stock Emulation Keywords

| Stock | Look | Keywords |
|---|---|---|
| Kodak Vision3 500T | Warm tungsten, cinematic | 500T, Vision3, tungsten balanced, cinema film |
| Kodak Vision3 250D | Daylight, natural | 250D, daylight balanced, natural film |
| Kodak Portra 400 | Soft, pastel skin tones | Portra 400, soft pastel, portrait film |
| Kodak Portra 800 | Pushed, grainy, warm | Portra 800, pushed, grainy, warm tones |
| Fuji Pro 400H | Clean, pastel, green tones | Fuji Pro 400H, clean pastel, subtle green |
| Fuji Velvia 50 | Ultra saturated, vivid | Velvia 50, vivid saturated, saturated colors |
| Kodachrome 64 | Iconic warm vivid | Kodachrome, iconic warm vivid reds |
| Ilford HP5 | B&W, contrasty grain | Ilford HP5, black and white, contrasty grain |
| Cinestill 800T | Halations, neon glow | Cinestill 800T, halation, neon glow, tungsten |

---

## Director Style Quick Reference

| Director | Signature | Keywords |
|---|---|---|
| Denis Villeneuve | Vast landscapes, slow pacing, atmospheric | Villeneuve style, vast landscape, slow burn, atmospheric dread |
| Christopher Nolan | IMAX, practical effects, non-linear | Nolan style, IMAX, practical effects, non-linear |
| Wes Anderson | Symmetry, pastels, flat composition | Wes Anderson style, centered symmetry, pastel, flat framing |
| Roger Deakins | Natural light, silhouettes, long takes | Deakins cinematography, natural light, silhouettes, long takes |
| David Fincher | Dark, desaturated, precise camera | Fincher style, dark desaturated, precise camera movement |
| Nicolas Winding Refn | Neon, slow motion, violence | Refn style, neon lit, slow motion, atmospheric violence |
| Zack Snyder | Slow motion, desaturated, heroic | Snyder style, slow motion hero shot, desaturated, epic |
| Ridley Scott | Atmospheric, detailed, epic | Ridley Scott style, atmospheric, detailed world building, epic |
| Bong Joon-ho | Social commentary, genre-mixing, precise | Bong Joon-ho style, genre-mixing, social commentary |