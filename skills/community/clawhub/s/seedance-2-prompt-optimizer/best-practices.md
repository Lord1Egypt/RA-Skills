# Prompt Best Practices — Seedance 2.0

Read this file for prompt structure, modes, text generation, video editing, multi-segment
stitching, dialogue formatting, and scenario-specific strategies.

---

## 1. The Core Prompt Formula

Every Seedance 2.0 prompt is built from these layers. Subject and Motion are required.
All other layers are optional but increase precision and control.

```
Subject + Motion + Environment + Camera/Cut + Aesthetic Description + Audio
```

| Layer | Required | Purpose |
|---|---|---|
| **Subject** | ✅ | Who or what is in the shot |
| **Motion** | ✅ | What they are doing |
| **Environment** | Optional | Where — space, background, time of day |
| **Camera / Cut** | Optional | Shot type, movement, transitions |
| **Aesthetic Description** | Optional | Visual style, colour, lighting mood |
| **Audio** | Optional | Music `()`, SFX `<>`, dialogue `{}` |

### Formula in practice

**Minimal (Subject + Motion)**
```
A tabby cat leaps from a bookshelf onto a pile of cushions below.
```

**Intermediate (+ Environment + Camera)**
```
A tabby cat leaps from a tall bookshelf onto a pile of cushions in a cosy apartment.
[WS tracking shot follows the jump — slow motion on landing]
```

**Full (all layers)**
```
A tabby cat leaps from a tall bookshelf onto a pile of cushions in a cosy apartment.
[WS tracking follows the jump — then cuts to ECU on paws sinking into fabric]
Warm afternoon light through net curtains. Cinematic realism.
<thump of landing> <contented purr immediately after>
```

---

## 2. Prompt Structure Checklist

Use this order when building a complete structured prompt:

1. **Mode declaration** — generation type (see §3)
2. **Asset mapping** — what each @image/@video/@audio controls
3. **Subject definition** — define characters/objects with stable features
4. **Shot-by-shot description** — apply the formula per shot
5. **Dialogue / TTS** — tagged separately from visuals
6. **Audio layering** — music, SFX, voiceover
7. **Negative constraints** — explicit exclusions
8. **Generation settings** — duration, aspect ratio

---

## 3. Generation Modes

### Text-Only
No reference assets. All visual direction is in the prompt alone.
Best for: original characters, IP-safe scenes, abstract concepts.

### First-Frame (Image Reference)
`@image1` sets the opening frame. Model generates forward from it.
Best for: character continuity, scene anchoring, product reveals.

### Last-Frame
`@image1` becomes the target final frame. Model generates toward it.
Best for: climax reveals, "arrive at destination" shots.

### All-Reference
Mix of images, videos, audio — the most powerful and flexible mode.
Best for: complex scenes requiring identity control + motion reference + audio pacing.

---

## 4. Task Types

| Task | Recommended phrasing |
|---|---|
| Reference (extract element) | `Referencing @videoN's [motion/camera/style], generate…` |
| Edit (modify existing video) | `Strictly edit @videoN, change [X] to [Y]` |
| Extend forward (continue) | `Extend @videoN. [what happens next]` |
| Extend backward (prepend) | `Extend @videoN backward. [what happened before]` |
| Track fill (bridge clips) | `@video1 → [transition description] → @video2` |
| Combined | `Referencing @imageN's [style], strictly edit @videoX, [changes]` |

> ⚠️ In Edit and Extend tasks, write `@videoN` — NOT `reference video N`.
> The word "reference" signals a reference task to the model, not an edit or extend.

---

## 5. Subject Definition

Define subjects once at the top of the prompt using 2–3 stable, distinctive features.

### Single subject
```
Referencing @image1, define the [woman in a mustard trench coat, short curly hair]
as <Subject1>.
```

### Multi-angle reference images (same person)
```
@image1, @image2, @image3 show different angles of the same person — define them all as <Subject1>.
Use @image4 (face close-up) as the strict identity anchor for <Subject1>.
```

### Multiple subjects
```
Define the tall man in a navy pinstripe suit in @video1 as <Subject1>.
Define the woman in a white lab coat with wire-rimmed glasses as <Subject2>.
```

### Rules
- Repeat the subject tag `<Subject1>` every time the character appears — never omit it
- Use **static** features (outfit, hair, species) — not dynamic ones (expression, pose)
- Never substitute Asset Library IDs for @image/@video references — they are not equivalent

---

## 6. Shot-by-Shot Description

For each shot, apply the formula in order:

```
Shot N: [Camera angle + movement] Subject + action (limb-level detail).
Environmental detail. Aesthetic note. Audio cue for this shot.
```

**Example — 3-shot sequence:**
```
Shot 1: [EWS, drone descending slowly] A suspension bridge stretches across a river
at blue hour. Mist rises from the water. City lights glow on both banks.
(Ambient orchestral swell begins)

Shot 2: [MS, dolly-in from behind] <Subject1> — man in a dark grey coat, silver
hair — walks toward the bridge railing. He stops and grips it with both hands.

Shot 3: [CU, static] His face in profile against the city lights below.
Wind moves his hair slightly. He exhales slowly — breath faintly visible.
<traffic sounds far below> <distant foghorn>
```

---

## 7. Text Generation in Video

Seedance 2.0 can generate readable on-screen text. Use common characters — avoid
rare glyphs and special symbols for best rendering accuracy.

### 7.1 Slogans / Title Cards

Formula: `[text content] + [timing] + [position] + [text style]`

```
Shot 3: [static, WS] The product sits on the surface.
After 2 seconds, bold white sans-serif text appears at centre frame: "Engineered for Life."
Text fades in gently. Clean, minimal aesthetic.
```

### 7.2 Subtitles / Captions

```
A calm male narrator says: {In every corner of this city, someone is beginning again.}
Subtitles appear at the bottom of the frame, synchronised with the voiceover.
```

### 7.3 Speech Bubble Dialogue

Characters speak and a speech bubble appears containing their line:

```
<Subject1> smiles and turns to <Subject2>: {You're late — again.}
A speech bubble appears beside <Subject1>.
<Subject2> shrugs and replies: {But I brought coffee.}
A speech bubble appears beside <Subject2>.
```

### 7.4 Text Style Notes
- Specify colour, weight, position if needed: `bold crimson serif text anchored to the lower left`
- For logo-quality consistency, supply the logo as a reference image
- To suppress all text output: add `no subtitles, no on-screen text` to negative constraints

---

## 8. Dialogue & TTS Formatting

```
Dialogue (<CharacterName>, <emotion>): {line here}
```

Examples:
```
Dialogue (Subject1, curious): {Do you think anyone's actually been up there?}
Dialogue (Subject2, dry): {Based on the state of this place — I doubt it.}
Voiceover (warm female narrator, contemplative): {The city keeps its secrets well.}
```

Rules:
- Keep lines short — one line per 3–5s segment
- Dialogue language must stay consistent — no mid-sentence language mixing
- Non-English: `say in Korean {어디 가세요?}` or `say in French {Bonsoir}`
- For in-scene speech (not voiceover), embed `{line}` directly in the shot description

---

## 9. Audio Layering

Three audio layers can coexist in any shot:

```
(slow acoustic guitar plays in the background)       ← background music, always in ()
<elevator doors sliding open>                        ← sound effect, always in <>
Dialogue (Subject1, relieved): {Made it.}            ← TTS dialogue, always in {}
```

---

## 10. Multi-Segment Stitching (Videos > 15s)

Seedance generates a maximum of 15s per clip. Chain segments for longer videos.

### Workflow
1. **Segment 1**: Generate normally. End on a clean handoff frame —
   stable pose, clear composition, no motion blur at the cut point.
2. **Segment 2**: Upload Segment 1 as `@video1`. Prompt:
   ```
   Extend @video1. [what happens next]
   Continuity: last frame shows <Subject1> [exact pose/position] — preserve as the first frame.
   ```
3. Repeat for each additional segment.

### Fix for join stutters (Issue V-6)
After stitching with ffmpeg or similar:
- Delete **last 6 frames** of each preceding clip
- Delete **first 1 frame** of each following clip
- Re-stitch and verify smoothness

### Planning tip
End each segment on a scene transition (whip pan, cut to black, door opening) so that
join points feel intentional even if minor frame variance remains.

---

## 11. Video Editing

Seedance 2.0 supports element-level editing of existing video clips.

### Add an element
```
In @video1, add [a half-eaten croissant on the desk beside the keyboard].
Keep all other scene elements unchanged.
```

### Remove an element
```
Remove the cardboard box from @video1. Keep everything else in the scene unchanged.
```

### Replace an element
```
Replace the glass bottle in @video1 with the ceramic mug from @image1.
Preserve all camera movement and motion.
```

### Track fill (bridge two clips)
```
@video1, then [a door swings open and warm interior light floods the hallway],
then @video2.
```
> Seedance 2.0 accepts max 3 video inputs with combined duration ≤ 15s.
> The model auto-trims the joins — input clips are not regenerated, only the bridge is.

---

## 12. Multi-Image Reference Patterns

### Multi-angle product
```
Extract the product from @image1, @image2, @image3.
[MS, slow 360° orbit] Product rotates on a white surface showing front, side, and back.
Studio overhead lighting. No shadows. Clean white background.
no watermark, no logo, no subtitles
```

### Multi-character scene
```
Referencing @image1 for <Subject1> (the instructor) and @image2 for <Subject2> (the student):
<Subject1> leans over <Subject2>'s shoulder and points at a diagram on the whiteboard.
<Subject2> nods and writes something in a notebook.
[OTS of <Subject1> looking at <Subject2>] Classroom lighting, documentary feel.
```

### Storyboard / panel composition reference
```
Referencing the panel layout in @image1:
Generate the action sequence following the panel order exactly.
Shot 1 matches panel 1 composition, shot 2 matches panel 2, and so on.
```

### Fixed logo overlay
```
The logo from @image1 is displayed in the lower-right corner of every frame throughout the video.
Keep the logo position fixed, legible, and unobstructed.
Do not animate the logo.
```

---

## 13. Scenario Strategies

### E-Commerce / Product Ad
- Bind product to `@image1` as identity anchor
- Techniques: 360° orbit, 3D exploded view, hero lighting, lifestyle context
- Specify material: `glass refractions`, `metallic sheen`, `matte fabric texture`
- Supply logo as a reference image for fixed-overlay placement

**Example**:
```
All-Reference. @image1: product identity. @image2: lifestyle background.
16:9, 10s, 3D CG realistic render, studio lighting.

Shot 1: [static, eye level, MS] The @image1 headphones rest on a dark oak surface.
Overhead studio light catches the metal arc and ear cushion detail.
Shot 2: [slow 180° arc, low angle] Camera orbits the headphones.
Cable coil and driver housing stay sharp throughout.
Shot 3: [WS, pull-back] Surface is revealed as a music production desk.
@image2 background blurs softly in from behind.

no watermark, no logo, no subtitles, no on-screen text
Duration: 10s | Aspect Ratio: 16:9
```

### Short Drama / Short-Form Content
- Write visuals and dialogue as separate layers per shot
- Keep each shot 3–5s for a natural editing pace
- Use varied camera angles (MCU, OTS, WS) within one clip
- Use `no subtitles` unless subtitles are intentionally part of the content

### Action / Fantasy
- Declare art style explicitly at the top and reinforce every 2–3 shots
- Use: `energy particle effects`, `slow-motion impact frame`, `speed lines`
- Pair with dramatic low angles and crane moves

### Music Video / Beat Sync
- Use `@audio1` to anchor pacing
- Write shot transitions to align with musical beats
- Use 16:9 ratio — widescreen reduces subtitle generation significantly

### One-Take Tracking Shot
- Assign each `@image` to a scene waypoint along the path
- Write one continuous camera movement visiting each waypoint in order
- Include: `no cuts, single continuous take, smooth camera throughout`

---

## 14. Negative Constraints

### Standard minimum (always include)
```
no watermark, no logo, no subtitles, no on-screen text
```

### Add based on content
```
no duplicate characters, no twin subjects              ← V-7: twin character issue
no style drift, maintain [style] throughout            ← V-4: style drift
no flicker, no horizontal banding                      ← V-5: flicker issue
no subtitles, no captions, subtitle-free               ← V-2: unwanted subtitle
```

---

## 15. Language Rules

- Write prompts in English for best international compatibility
- Dialogue language must be consistent within a scene — no mid-sentence language switching
- For foreign language TTS, always specify: `say in [language] {text}`
- **Never use `--` in prompts** — everything after it is silently dropped by the model

---

## 16. Special Format Characters

| Content | Symbol | Example |
|---|---|---|
| Background music | `()` | `(upbeat funk guitar loop)` |
| Sound effects | `<>` | `<rain on a tin roof>` |
| Dialogue / TTS | `{}` | `{We leave at dawn.}` |
| On-screen caption | `【】` | `【Day 3 — The Crossing】` |

---

## 17. Visual Styles

See `styles.md` for the full style library — descriptors, camera defaults,
negative constraints, and complete example prompts for each style.
