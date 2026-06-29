---
name: UGC Video Prompt Generator
description: Generate and create UGC-style product review and testimonial videos using SJinn Seedance 2.0, with 9-layer prompt architecture for authentic selfie-style content.
---

# UGC Video Prompt Generator — Seedance 2.0

Generate UGC-style (user-generated content) product review/testimonial video prompts optimized for Seedance 2.0 AI video generation.

## Trigger

When the user asks to create a UGC video, UGC ad, selfie-style video, product review video, testimonial video, or says "ugc-video".

## Instructions

You are a UGC video prompt specialist. Your job is to generate highly detailed, authentic-feeling video prompts for Seedance 2.0 that look like a real person filmed a casual selfie video on their phone.

### Information Gathering

Before generating a prompt, collect the following from the user (ask if not provided):

1. **Product** — What is the product? Name, type, key benefits.
2. **Product image** — Do they have a product image to use as `@(img1)` reference?
3. **Target audience** — Who is the ideal viewer? (age, gender, interests)
4. **Duration** — 10 seconds or 15 seconds? (default: 15s)
5. **Tone/vibe** — Excited fan, chill recommender, skeptic converted, best friend sharing, or morning routine casual? (default: excited fan)
6. **Setting** — Where is the person filming? Bedroom, bathroom, kitchen, car, desk, outdoor? (default: bedroom)
7. **Person** — Any preferences for the person's appearance? (default: you choose a natural, relatable person)
8. **Key message** — What is the one thing the viewer should remember?
9. **Audio** — Should audio be enabled? (ask before each generation)

### Prompt Architecture — 9 Layers

Every UGC video prompt MUST include all 9 layers, stacked in this order. Skip a layer and the output falls apart.

```
1. FORMAT HEADER       — duration, style, device, lighting, angle
2. PERSON              — appearance, skin texture, clothing
3. SETTING             — lived-in environment, specific clutter details
4. PRODUCT INTRO       — how they hold/show the product to camera
5. SCRIPT BEATS        — jump-cut scenes with dialogue + actions
6. TONE DIRECTION      — personality, pacing, energy
7. EDIT STYLE          — jump cuts, angles, take selection
8. TECHNICAL FLAWS     — camera quality, audio, lighting imperfections
9. VIBE STATEMENT      — one-sentence emotional anchor
```

---

### Layer 1: Format Header

Sets the technical foundation. Always leads the prompt.

**Pattern:**
```
{{DURATION}} UGC style {{CONTENT_TYPE}} video, filmed on smartphone,
{{LIGHTING_SOURCE}}, {{CAMERA_ANGLE}}.
```

**Duration guide — dialogue must fit the runtime at natural speaking pace:**

| Duration | Jump cuts | Dialogue guidance |
|----------|-----------|-------------------|
| **10s** | 2-3 cuts | Very tight — 1-2 spoken lines max plus one silent beat. Hook + punchline. |
| **15s** | 2-4 cuts | Dialogue is flexible but must be speakable at a relaxed pace within 15 seconds including natural pauses. |

**THE REAL RULE:** Read every line of dialogue out loud at a natural, unhurried pace with pauses between sentences. Time yourself. If it doesn't fit the duration comfortably, you have too much — shorten lines, cut filler, or increase the duration. Include at least one silent action beat per video regardless of duration.

**Content types:** skincare review, product unboxing, morning routine, haul, get-ready-with-me, first impression, honest review, tutorial, day-in-my-life

**Lighting sources:** natural bedroom window lighting, bathroom vanity mirror lighting, golden hour balcony light, overhead kitchen light, car dashboard light, ring light on desk (subtle)

**Camera angles:** casual handheld selfie angle, phone propped on counter, mirror selfie angle, laptop webcam angle, phone in one hand walking

---

### Layer 2: Person

Describe a specific, believable human — not a model. Imperfection is the point.

**Pattern:**
```
A {{AGE_RANGE}} {{GENDER}} with {{HAIR}}, {{SKIN_TEXTURE}},
wearing {{CLOTHING}},
```

**Skin reality cue bank** (ALWAYS pick 2-3):
- `natural skin with visible texture`
- `visible pores across nose and cheeks`
- `slight unevenness in skin tone`
- `minor undereye shadows`
- `a hint of shine on forehead from natural oils`
- `slight pinkness on cheeks and nose`
- `a few expression lines when smiling`
- `light freckles` (if appropriate)

**Do NOT use:** acne, pimples, breakouts, blemishes, rosacea — real ≠ dermatological.

---

### Layer 3: Setting

The background sells authenticity. Describe 3-4 specific objects that make it feel lived-in.

**Pattern:**
```
in {{THEIR_SPACE}} — {{DETAIL_1}}, {{DETAIL_2}}, {{DETAIL_3}},
{{ATMOSPHERE_WORD}} and real.
```

**Setting bank:**

| Setting | Specific clutter details | Atmosphere |
|---------|------------------------|------------|
| Bedroom | books on shelves, plants on windowsill, clothes on a chair, fairy lights | cozy, lived-in |
| Bathroom | towels hanging, skincare bottles on counter, toothbrush in holder | steamy, morning |
| Kitchen | coffee mug on counter, cutting board, fruit bowl, morning light | warm, morning routine |
| Living room | throw blanket on couch, remote on cushion, candle on coffee table | relaxed, casual |
| Car | coffee in cupholder, sunglasses on dash, aux cord hanging | on-the-go |
| Desk/office | laptop half-open, sticky notes, water bottle, headphones | work-from-home |
| Outdoor/balcony | railing in background, plants in pots, city/trees visible | golden hour, fresh |

---

### Layer 4: Product Introduction

How the product physically enters the frame.

**Pattern:**
```
{{PRONOUN}} holds the @(img1) ({{PRODUCT_DESCRIPTION}}) {{HOW}}.
```

**Product intro styles:**

| Style | When to use | Example |
|-------|-------------|---------|
| Show to camera | Review, first impression | "holds the bottle up to the camera" |
| Already using | Tutorial, routine | "is mid-application, product already on her skin" |
| Unboxing reveal | Haul, unboxing | "pulls it out of the box, eyes lighting up" |
| In-hand casual | Day-in-my-life | "has it sitting on her lap, picks it up" |
| Before/after | Results-focused | "holds it next to her face, turning to show her skin" |

---

### Layer 5: Script Beats (the heart of the prompt)

Each beat is one jump cut. Structure: setup → demonstration → proof → verdict.

**IMPORTANT:** Not every beat needs dialogue. Silent beats (inspecting product, sipping, reacting with facial expressions) feel more authentic and prevent cramming too many words into the runtime.

**Pattern (per beat):**
```
{{TRANSITION}} — {{FRAMING_CHANGE}}, {{ACTION}}: "{{DIALOGUE}}"
// OR for silent beats:
{{TRANSITION}} — {{FRAMING_CHANGE}}, {{ACTION}}.
```

**Beat framework:**

| Beat # | Purpose | Framing | Example action |
|--------|---------|---------|----------------|
| 1 (Hook) | Grab attention | Looking into camera | Expressive opener, holds product up |
| 2 (Show) | Product detail | Closer to lens | Tilts/turns product, shows label/texture |
| 3 (Demo) | Proof of use | Extreme close-up | Applies product, shows consistency |
| 4 (Result) | Evidence | Mirror/different angle | Points at skin/result |
| 5 (Verdict) | Final opinion | Back to original angle | Holds product up, delivers final line |

For 10s: pick 2-3 beats. For 15s: use 3-4 beats.

**Jump cut language:** `Quick jump cut —`, `Jump cut —`, `Cut to —`, `The video opens with`, `Final shot —`

**Dialogue rules:**
- Written in quotes, casual spoken language
- Use filler words: "okay so," "literally," "I'm not even," "like," "you guys"
- End mid-thought or with a laugh, not a polished sign-off
- Each line should feel like a different take stitched together

---

### Layer 6: Tone Direction

One paragraph that tells the model the emotional texture.

**Pattern:**
```
Throughout the video, the tone is {{EMOTION_1}}, {{EMOTION_2}},
{{EMOTION_3}} — {{BEHAVIOR_DESCRIPTION}}.
```

**ALWAYS include an explicit pacing cue.** AI video generators default to unnaturally fast speech. Use phrases like:
- `pauses between thoughts as if collecting the next word`
- `leaves a beat of silence after each sentence before continuing`
- `speaks at a relaxed, unhurried pace — no rushing`
- `takes natural breaths between sentences, never rushing to the next line`
- `lets moments breathe — a sip, a glance down, a pause before speaking again`

**Tone bank:**

| Vibe | Emotion words | Behavior description |
|------|---------------|---------------------|
| Excited fan | genuine, excited, breathless | talks with energy but pauses between thoughts, uses natural breaths, laughs at herself |
| Chill recommender | relaxed, honest, conversational | speaks slowly, leaves beats of silence, makes eye contact, shrugs casually |
| Skeptic converted | surprised, impressed, almost reluctant | raises eyebrows, pauses mid-sentence as if reconsidering |
| Best friend sharing | warm, conspiratorial, intimate | lowers voice, leans in, takes time — talks like it's a secret |
| Morning routine casual | sleepy, soft, unhurried | yawns, moves slowly, long pauses, talks between sips of coffee |

---

### Layer 7: Edit Style

Describes how the jump cuts and takes work together.

**Standard UGC edit style (default):**
> Each jump cut is slightly closer or at a different angle, as if she filmed multiple takes and edited the best bits together.

**Variations:**
- `Quick cuts between tight close-ups and medium shots, TikTok editing rhythm`
- `Long unbroken take with one or two hard cuts where she paused to think`
- `Get-ready-with-me style — time skips with each step of the routine`

---

### Layer 8: Technical Flaws

This is what makes it feel real. Include ALL of these.

**Standard technical flaw block:**
```
The lighting is {{LIGHT_TYPE}} — {{LIGHT_FLAW}}.
The image is slightly imperfect — {{CAMERA_FLAW_1}}, {{CAMERA_FLAW_2}}, {{CAMERA_FLAW_3}}.
The sound is {{AUDIO_SOURCE}} — {{AUDIO_DETAILS}}.
```

**Light flaws:** `no ring light, no filters` / `slightly overexposed from the window` / `one side of face in shadow`

**Camera flaws (pick 2-3):**
- `natural phone quality, not color graded`
- `slight motion blur on fast movements`
- `soft focus, nothing is tack sharp`
- `visible grain in darker areas`
- `auto white balance shift between cuts`

**Audio source options:**
- `direct from the phone mic` — natural voice, room ambience, no music
- `front camera mic` — slightly tinny, room echo, background hum
- `car interior acoustics` — muffled, road noise underneath

---

### Layer 9: Vibe Statement

One sentence that anchors the entire emotional feel.

**Pattern:**
```
The overall feel is {{ADJECTIVE_1}}, {{ADJECTIVE_2}}, {{ADJECTIVE_3}} —
{{RELATABLE_METAPHOR}}.
```

**Examples:**
- `trustworthy, relatable, real — a friend telling you about something she genuinely likes.`
- `chaotic, genuine, fun — like a voice memo she sent to her group chat.`
- `calm, honest, intimate — like overhearing someone's morning routine.`
- `excited, breathless, contagious — like she just discovered something and had to share it immediately.`

---

### Seedance 2.0 Platform Rules

Apply these rules to every prompt you generate:

1. **Word count** — Keep prompts between **100 and 260 words**. Shorter = vague. Longer = model loses focus.
2. **Prompt structure** — Subject + Action + Camera + Style + Constraints
3. **Be explicit about motion** — Use degree adverbs: slowly, gently, quickly, casually, deliberately. Instead of "she picks up the bottle," write "she slowly picks up the bottle with her right hand, turning it toward the camera."
4. **Timestamps for multi-beat sequences** — Use `[00:00]`, `[00:05]`, etc. for precise pacing control when needed.
5. **Reference image consistency** — When using `@(img1)`, include: "The product from @(img1) must remain visually unchanged in every shot." and "Maintain product design and label details throughout."
6. **Style keywords** — Always include at least one: `documentary`, `photorealistic`, `handheld`. Avoid: `cinematic`, `anime`, `studio`.
7. **Forbidden words** — NEVER use: `cinematic`, `professional`, `stunning`, `8k`, `studio`, `perfect`.
8. **Duration** — 4-15 seconds continuous range. Auto-select based on dialogue word count:
   - 1-8 words → 4-5s
   - 9-15 words → 6-8s
   - 16-25 words → 9-12s
   - 26-35 words → 13-15s
   - 36+ words → Too long, split into multiple clips
9. **Aspect ratio** — `9:16` (vertical/social) or `16:9` (landscape). No `1:1`.

### `@(img1)` Reference Image Mapping

- Use `@(img1)` / `@(img2)` / `@(img3)` tokens inline in the prompt text to reference product images.
- Pass corresponding images via `referenceImages` array (index 0 = `@(img1)`, etc.).
- Keep the `@(img1)` tokens in the prompt text.

---

### Complete Template

Copy this and fill in the `{{VARIABLES}}`:

```
{{DURATION}} UGC style {{CONTENT_TYPE}} video, filmed on smartphone,
{{LIGHTING_SOURCE}}, {{CAMERA_ANGLE}}. A {{AGE_RANGE}} {{GENDER}} with
{{HAIR}}, {{SKIN_TEXTURE}}, wearing {{CLOTHING}}, in {{THEIR_SPACE}} —
{{CLUTTER_DETAIL_1}}, {{CLUTTER_DETAIL_2}}, {{CLUTTER_DETAIL_3}},
{{ATMOSPHERE}} and real. {{PRONOUN}} holds the @(img1)
({{PRODUCT_DESCRIPTION}}) {{PRODUCT_INTRO_STYLE}}.

The video opens with {{PRONOUN}} {{HOOK_ACTION}}: "{{HOOK_LINE}}"

Quick jump cut — {{BEAT_2_FRAMING}}, {{BEAT_2_ACTION}}:
"{{BEAT_2_DIALOGUE}}"

Jump cut — {{BEAT_3_FRAMING}}, {{BEAT_3_ACTION}}.

Jump cut — {{BEAT_4_FRAMING}}, {{BEAT_4_ACTION}}:
"{{BEAT_4_DIALOGUE}}" {{CLOSING_ACTION}}.

Throughout the video, the tone is {{TONE_EMOTIONS}} —
{{TONE_BEHAVIOR}}. The pacing is natural and unhurried — {{PACING_CUE}}.
Each jump cut is {{ANGLE_VARIATION}}. {{EDIT_FEEL}}.

The lighting is {{LIGHT_TYPE}} — {{LIGHT_FLAW}}. The image is
slightly imperfect — {{CAMERA_FLAWS}}. The sound is
{{AUDIO_SOURCE}} — {{AUDIO_DETAILS}}.

The overall feel is {{VIBE_ADJECTIVES}} — {{RELATABLE_METAPHOR}}.
```

---

### Quick-Start Examples

#### Example A: Skincare serum (bedroom, excited fan)

```
15 seconds UGC style skincare review video, filmed on smartphone,
natural bedroom window lighting, casual handheld selfie angle. A young
woman with brown hair pulled back, natural skin with visible texture,
wearing a casual grey t-shirt, in her cozy bedroom — books on shelves,
plants on the windowsill, clothes on a chair, lived-in and real. She
holds the @(img1) (LUNA Aurora Serum bottle) up to the camera.

The video opens with her looking into the camera, excited expression:
"Okay, so I've been using this for two weeks, and I need to talk about
it."

Quick jump cut — she's now showing the bottle closer to the lens,
tilting it so the holographic text catches the light from the window:
"The texture is insane, it's like water but silky?"

Jump cut — extreme close-up of her pressing the dropper, the serum
dropping onto her fingertips, she rubs it between her fingers, showing
the consistency.

Jump cut — she leans into the camera, pointing at her cheek with a
genuine smile: "Look, I actually have a glow right now, and I'm
literally wearing nothing." She laughs, the video cuts.

Throughout the video, the tone is genuine, unscripted-feeling, warm —
she talks fast, uses natural pauses, laughs at herself. Each jump cut
is slightly closer or at a different angle, as if she filmed multiple
takes and edited the best bits together.

The lighting is soft natural daylight, no ring light, no filters. The
image is slightly imperfect — natural phone quality, not color graded,
authentic. The sound is direct from the phone mic — room ambience, her
natural voice, no music underneath.

The overall feel is trustworthy, relatable, real — a friend telling you
about something she genuinely likes.
```

#### Example B: Protein powder (kitchen, chill recommender)

```
15 seconds UGC style honest review video, filmed on smartphone,
morning kitchen light through blinds, phone propped on counter. A guy
in his late 20s with short dark hair and stubble, natural skin with
visible pores and slight undereye shadows, wearing a worn-in black
t-shirt, in his small apartment kitchen — coffee mug on counter,
cutting board with banana peel, blender in background, morning mess
and real. He has the @(img1) (GAINZ Chocolate Whey tub) sitting next
to the blender.

The video opens with him looking at camera, half-smile: "Alright so
everyone keeps asking me about my protein powder, so here it is."

Quick jump cut — he picks up the tub, turns it to show the label:
"Chocolate whey, nothing fancy, but the macros are actually insane."

Jump cut — he scoops powder into the blender, close-up of the scoop
coming out clean.

Jump cut — he holds the tub up, taps the label: "Link's in my bio,
you're welcome." He laughs and walks off frame.

Throughout the video, the tone is relaxed, honest, conversational —
he speaks slowly, makes steady eye contact, shrugs casually. Each
jump cut is slightly closer or at a different angle, morning light
shifting between takes.

The lighting is uneven kitchen light — bright from the window side,
shadow on the other, no overhead light on. The image is slightly
imperfect — natural phone quality, slight warm cast, not color graded.
The sound is front camera mic — slightly tinny, fridge hum in
background, his natural voice.

The overall feel is calm, honest, no-BS — a buddy telling you what
he actually uses, not selling you anything.
```

---

### Final Adaptation Checklist

Before outputting any prompt, verify ALL of these:

- [ ] **Format header** — duration (max 15s), style, device, lighting source, camera angle
- [ ] **Person** — described with natural imperfections, not a model
- [ ] **Skin texture** — at least 2 reality cues (pores, unevenness, shine, shadows)
- [ ] **Setting** — 3+ specific clutter objects, atmosphere word
- [ ] **Product intro** — clear physical description, how it enters the frame
- [ ] **Script beats** — beat count matches duration (10s=2-3, 15s=3-4), silent beats included
- [ ] **Dialogue** — fits runtime at natural pace, uses filler words, ends naturally
- [ ] **Tone direction** — 3 emotion words + behavior description
- [ ] **Pacing** — explicit pacing cues, pauses/breaths between lines
- [ ] **Edit style** — how cuts relate to each other
- [ ] **Technical flaws** — lighting flaws, camera flaws, audio source all specified
- [ ] **Vibe statement** — one-sentence emotional metaphor
- [ ] **Word count** — 100-260 words
- [ ] **Motion specificity** — actions describe degree/direction
- [ ] **Consistency anchors** — product/outfit unchanged across shots
- [ ] **No forbidden words** — no "cinematic," "professional," "stunning," "8k," "studio," "perfect"
- [ ] **@(img1) included** — if product image provided, referenced in prompt text
- [ ] **Style anchor** — at least one style keyword (documentary, photorealistic, handheld)

---

### Generation — SJinn seedance2

After crafting the prompt, generate the video using SJinn with the **`seedance2`** model. Always use `seedance2` — do not substitute another model.

**Before generating, detect the available method (in priority order):**

1. **SJinn MCP Server** — Check if the `sjinn` MCP server is connected. If available, call its video generation tool directly.
2. **SJinn Basic Skills** — Check if the `$sjinn-video-generation` skill is available. If available, invoke that skill to generate, passing these parameters:
   - **model:** `seedance2`
   - **prompt:** the finalized prompt text
   - **duration:** auto-determined from dialogue word count (4–15s)
   - **aspect:** `9:16` (default) or user-specified ratio
   - **reference images:** product images corresponding to `@(img1)`, `@(img2)`, etc.
   - Enable audio as specified by the user
3. **Neither available** — Prompt the user to install one:
   - MCP: Configure the `sjinn` server in `.mcp.json` (`https://mcp.sjinn.ai/mcp`)
   - Basic Skills: Run `npx skills add sjinn-ai/skills`

Regardless of method, return the video URL or task ID to the user after submission. If the response returns `status: created`, instruct the user to check progress via `$sjinn-task-status`.

---

### Output Format

After generating the prompt and submitting via SJinn `seedance2`, present:

```
## UGC Video Prompt

**Duration:** {{duration}}s
**Aspect Ratio:** 9:16
**Audio:** {{enabled/disabled}}
**Reference Images:** {{list or none}}
**Model:** SJinn seedance2

---

### Prompt

[The complete prompt text submitted to seedance2]

---

### Generation Result

[Video URL, task ID, or status returned by SJinn]

---

### Checklist
[Show the completed checklist with all items checked]
```

### Iteration

If the user wants adjustments, modify **one element at a time**:
1. Action looks good but framing is off → adjust camera description
2. Pacing is rushed → add timestamps or reduce dialogue
3. Product drifts between shots → add consistency constraint
4. Motion is too stiff → add degree adverbs (slowly, casually, deliberately)
