---
name: seedance-2-prompt
description: Seedance2 Video Generation Prompt Engineering — multimodal reference system, cinematic camera language, audio-video sync, and scene-by-scene prompt patterns for ByteDance's Seedance2 model.
license: MIT
---

# Seedance2 Prompt Engineering Skill

This skill, created by coopeai.com, provides comprehensive guidelines and prompt engineering patterns for writing professional video generation prompts for ByteDance's **Seedance2** model, optimized for cinematic creators, brand video producers, and social media content designers.

---

## 1. Seedance2 Model Specifications Reference

### 1.1 Model Variants

| Variant | Best For |
|---------|----------|
| **Standard T2V** | Text-to-video, highest fidelity, full scene generation |
| **Standard I2V** | Image-to-video, first/last frame anchoring, character consistency |
| **Standard Video Edit** | Targeted clip editing — swap characters, change actions, modify storylines |
| **Standard Video Extend** | Extend an existing clip with new continuous shots |
| **Fast T2V / I2V / Edit / Extend** | Same capabilities, lower latency for real-time workflows |
| **Turbo variants** | Lowest latency, suitable for prototyping and iterative drafting |

### 1.2 Multimodal Input Limits

| Input Type | Limit | Notes |
|------------|-------|-------|
| Images | Up to **9 images** | Characters, style refs, first/last frames |
| Videos | Up to **3 videos**, max 15s total | Motion, camera work, editing rhythm |
| Audio | Up to **3 MP3 files**, max 15s total | Music, SFX, dialogue sync |
| Total files | **12 files** per generation | Prioritize highest-impact inputs |

### 1.3 Output Specifications

- **Duration:** 4–15 seconds (user-selectable per generation)
- **Resolution:** Native 480p and 720p output
- **Audio:** Native joint generation — sound effects, music, and ambient audio are baked in, not layered in post
- **Architecture:** Dual-Branch Diffusion Transformer generating video and audio simultaneously

### 1.4 Content Guardrails

Seedance2 enforces **pre-generation restrictions** (not post-generation filtering):
- No real people's likenesses without authorization
- No copyrighted characters or brand identities
- No harmful, deceptive, or dangerous content
- All outputs carry **C2PA watermarking** for content authenticity

---

## 2. @ Mention System — Asset Reference Syntax

Seedance2's most powerful feature is its **@ mention system**, which lets you explicitly assign each uploaded asset a specific role in the generation.

### 2.1 Core Syntax

```
@Image1, @Image2 ... @Image9    — uploaded image files (numbered by upload order)
@Video1, @Video2, @Video3       — uploaded video clips
@Audio1, @Audio2, @Audio3       — uploaded audio files
```

### 2.2 Reference Patterns

| Goal | Prompt Pattern |
|------|---------------|
| Anchor the first frame | `Use @Image1 as the first frame` |
| Anchor the last frame | `End on @Image2 as the final frame` |
| Copy camera movement | `Follow @Video1's camera movements exactly` |
| Copy motion choreography | `Reference @Video1 for the fight choreography` |
| Set background music | `Use @Audio1 as the background music` |
| Sync cuts to a beat | `Cut @Image1 through @Image6 to the rhythm of @Video1` |
| Swap character in a clip | `Replace the woman in @Video1 with @Image1` |
| Extend a clip | `Extend @Video1 by 8 seconds` |
| Apply fisheye style | `Apply @Video1's fisheye lens effect to the new scene` |
| Combine location + character | `Character from @Image1, location from @Image2, camera from @Video1` |

### 2.3 @ Mention Rules

1. **Be explicit about role** — always state what each asset contributes (style, motion, character, audio). Ambiguous mentions are resolved by the model but may not match your intent.
2. **Number order matters** — @Image1 is the first uploaded file, @Image2 the second. Double-check order before running.
3. **Edit vs. reference** — if modifying a clip, say "edit @Video1 to...". If using it as a style source, say "reference @Video1 for...".
4. **Match duration on extends** — when extending a clip, set generation length to the added duration (e.g., extend by 8s → generate 8s, not 15s).

---

## 3. Prompt Engineering Best Practices

### 3.1 Scene Structure Formula

Write prompts in this order for best results:

```
[Subject + Action] + [Environment + Atmosphere] + [Camera Language] + [Motion & Pacing] + [Audio Direction] + [Duration Hint]
```

### 3.2 Camera Language Vocabulary

Seedance2 responds well to professional cinematography terms. Use these instead of vague descriptions:

| Technique | Prompt Keyword |
|-----------|---------------|
| Slow push-in | `slow dolly push toward the subject` |
| Orbit / arc shot | `orbital camera arc around the subject` |
| Tracking shot | `continuous tracking shot following the subject` |
| Hitchcock zoom | `Hitchcock zoom as the character is startled` |
| Crane up | `camera cranes up to reveal the skyline` |
| Handheld | `handheld naturalistic camera movement` |
| Static locked-off | `static locked-off wide shot` |
| Dutch angle | `slight Dutch angle, tension-building` |
| POV | `first-person POV shot` |

### 3.3 Motion & Pacing Descriptors

| Pacing | Prompt Example |
|--------|---------------|
| Slow, elegant | `slow graceful movement, each step deliberate` |
| Energetic, kinetic | `fast-paced dynamic motion, high energy` |
| Frozen moment | `time-freeze effect, subject in mid-air` |
| Beat-synced | `cuts timed to the drum beat of @Audio1` |
| Continuous flow | `one unbroken tracking shot, no cuts` |

### 3.4 Lighting & Atmosphere

Always describe the lighting source, direction, and quality — not just the mood:

- **Good:** `"warm golden hour sunlight raking from the left, long soft shadows on the concrete"` 
- **Bad:** `"good lighting, warm feel"`

Common lighting setups:

| Look | Prompt |
|------|--------|
| Golden hour | `warm golden hour sunlight, low angle, long shadows` |
| Night neon | `neon-lit street, cyan and magenta reflections on wet pavement` |
| Studio clean | `soft studio softbox lighting, neutral background, no shadows` |
| Dramatic chiaroscuro | `high contrast chiaroscuro, single hard key light, deep shadows` |
| Overcast natural | `soft diffused overcast daylight, flat even illumination` |

### 3.5 Audio Direction

Since Seedance2 generates audio natively, include audio intent in your prompt:

- `"ambient city sounds, distant traffic, subtle wind"` 
- `"score builds gradually, tension rising with the camera push"`
- `"crisp footsteps on gravel, no music, environmental sound only"`
- `"use @Audio1 as the soundtrack, sync the edit cuts to its rhythm"`

---

## 4. Use Case Scenarios & Prompt Examples

### Scenario 1: Cinematic Short — Single Character Scene

**Goal:** A character-driven narrative moment with strong emotional impact.

#### Prompt Template:
> [Character description] is [action] in [environment]. The camera [camera movement], capturing [emotional detail]. [Lighting setup]. [Audio direction]. [Duration].

#### Example (Homecoming):
> A tired office worker in a rumpled suit drags his briefcase through the front door of a dimly lit apartment. The camera slowly dolly-pushes toward his face as he hears his daughter's laughter from the next room — his expression shifts from exhaustion to warmth. Warm practical lamp light, deep shadows in the hallway. Ambient sound: creaking door, distant children's laughter. 8 seconds.

---

### Scenario 2: Beat-Synced Brand Video — Multi-Image Montage

**Goal:** Cut a series of product or lifestyle images to a music track rhythm.

#### Prompt Template:
> Cut @Image1 through @Image[N] in sequence, timed to the keyframe positions and rhythm of @Audio1. Each image holds for [X] beats. [Transition style]. [Overall visual mood].

#### Example (Fashion Drop):
> Cut @Image1 through @Image7 in sequence, timed to the drum hits and rhythm of @Audio1. Each image holds for 2 beats then cuts sharp. Flash cuts between garments, high contrast, bold direct lighting. Ending freeze on @Image7 for 1 second. 10 seconds.

---

### Scenario 3: Character Consistency — Multi-Shot Narrative

**Goal:** Maintain a consistent character across multiple scenes using image references.

#### Prompt Template:
> Character @Image1 [scene 1 action]. Then [scene 2 action]. Finally [scene 3 action]. Consistent character appearance throughout. [Camera style]. [Tone].

#### Example:
> Character @Image1 wakes up and stretches in a sunlit bedroom. Then walks into the kitchen and pours coffee, glancing out the window at a rainy street. Finally sits at a wooden desk and opens a laptop, a small smile on her face. Continuous warm morning light throughout. Handheld naturalistic camera. Intimate, quiet tone. 12 seconds.

---

### Scenario 4: Camera Work Replication

**Goal:** Apply complex camera choreography from a reference video to a new scene.

#### Prompt Template:
> New scene: [describe subject and environment]. Camera movement references @Video1 — replicate its [specific technique]. [Lighting]. [Audio].

#### Example (Hitchcock Zoom):
> A woman stands at the end of a long, narrow library corridor. Replicate @Video1's Hitchcock zoom technique as she turns to face the camera — the background rapidly recedes while she stays in sharp focus. Cold fluorescent lighting, slight green cast. Eerie ambient hum. 6 seconds.

---

### Scenario 5: Video Extension — Continuous Scene Development

**Goal:** Extend an existing clip into a longer continuous sequence.

#### Prompt Template:
> Extend @Video1 by [X] seconds. Continue from where the clip ends: [describe next action/event]. Maintain consistent [lighting / character / environment]. [New audio direction if needed].

#### Example:
> Extend @Video1 by 10 seconds. Continue from where the runner exits the corridor — she bursts through a rooftop door into open air, skids to a stop at the edge, and looks out over the city at sunset. Consistent handheld energy. Cut from indoor fluorescent to warm golden sunset lighting. Swelling orchestral score continues from @Audio1. 10 seconds.

---

### Scenario 6: Video Editing — Character or Action Swap

**Goal:** Modify a specific element in an existing video clip while keeping everything else intact.

#### Prompt Template:
> Edit @Video1: replace [original element] with [new element from @Image1 or description]. Keep [everything else] unchanged.

#### Example:
> Edit @Video1: replace the man walking across the bridge with @Image1 (a woman in a red coat). Keep the bridge environment, lighting, rain, and camera movement completely unchanged. Match her walking pace and stride to the original. 7 seconds.

---

## 5. Multi-Turn Editing Guidelines

Seedance2 supports iterative refinement. Use these patterns for multi-turn conversations:

1. **Isolating changes:**
   - *Vague:* "Make it more cinematic"
   - *Precise:* "Keep the subject and environment exactly as generated. Add a slow dolly push toward the subject's face and shift the lighting to a warmer golden tone."

2. **Adjusting pacing:**
   - *Vague:* "Slower"
   - *Precise:* "Reduce the overall motion speed by roughly half. The camera movement should ease in rather than start at full speed."

3. **Audio adjustments:**
   - *Vague:* "Better music"
   - *Precise:* "Replace the current background score with @Audio2. Keep all environmental sound effects — only swap the music layer."

4. **Extending selectively:**
   - *Vague:* "Make it longer"
   - *Precise:* "Extend @Video1 by 6 seconds. After the door closes, hold on the empty hallway for 2 seconds, then slowly push toward the window as light fades."

5. **Preserving consistency:**
   - Always mention which elements must stay identical: `"Keep the character's appearance, the room's lighting, and the camera angle identical to @Video1. Only change the season visible through the window from summer to winter."`
