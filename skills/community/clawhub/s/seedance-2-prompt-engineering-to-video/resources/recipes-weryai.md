# Seedance 2.0 prompt recipes (WeryAI edition)

Production-ready **English prompt blocks** plus **WeryAI** execution hints. Full CLI fields: **[WERYAI_VIDEO_API.md](WERYAI_VIDEO_API.md)**.

**How to use:** Draft the **Final Prompt** (and constraints) below → map stills to **`image` / `images` / `first_frame` / `last_frame`** → run **`submit-*`** after user confirmation per [SKILL.md](../SKILL.md).

**Legend:** Recipes inherited from JiMeng-style docs may mention **`@video1` / `@audio1`**. On WeryAI, **replace with prose** and/or **key-frame `https` URLs** (see each recipe’s **WeryAI** box).

---

## A) Cinematic adventure (10s)

**WeryAI:** `submit-text` **or** `submit-multi-image` if the user supplies hero / environment stills (≤3 URLs). Optional **`generate_audio: true`** for ambience described in prompt.

**Suggested JSON (text-only):**

- `model`: `SEEDANCE_2_0`
- `duration`: `10`, `aspect_ratio`: `9:16`, `resolution`: `720p`

```text
Mode: Text-only (or map user stills: image1 = hero anchor, image2 = optional environment)
Assets Mapping:
- (If images) Reference 1: hero appearance and wardrobe lock
- (If images) Reference 2: optional environment color and material cues
- (No @video) Describe camera rhythm in prose: slow dolly out, follow shot, crane up

Final Prompt:
9:16 vertical, 10s, fantasy adventure cinematic, cel-shading blended with watercolor, cool blue-green palette with warm highlights.
0-3s: hero wakes in a dim ancient chamber; faint glowing runes pulse on wet stone walls; slow dolly out.
3-7s: hero walks to giant rune door and touches circular mechanism; energy ripples activate runes in sequence; heavy door opens into bright light; follow shot.
7-10s: reveal vast world from cliff edge with floating islands and distant glowing ruins; crane up + pullback for scale.
Audio: water-drop echoes and low temple resonance at start; layered activation tones at rune trigger; deep rumble on door opening; orchestral swell on world reveal; wind ambience to end.
Visual control: coherent lighting, physically plausible movement, stable identity.

Constraints (inside prompt — no API negative_prompt):
no watermark, no logo, no subtitles, no on-screen text.
```

---

## B) Continue / extend a previous clip (conceptual “Extend @video1”)

**WeryAI:** There is **no** separate “extend video URL” field in this skill’s flow. Use **`submit-image`** (or **`first_frame` + optional `last_frame`**) with an **`https`** **last-frame still** from the prior clip, plus a continuation **`prompt`**.

**Suggested JSON:**

- `image`: `<https last frame of previous segment>`
- `duration`: `5`–`15` (new segment only)
- Describe: “Seamless continuation, same identity, outfit, lighting, lens feel, no jump cut.”

```text
Mode: Continuation from reference still
Assets Mapping:
- Reference still: exact end state of previous segment (composition, pose, lighting)

Final Prompt:
Continue seamlessly from the reference frame. Preserve character identity, outfit, camera direction, and lighting from the prior shot.
0-2s: continue motion without a jump cut; micro-overlap action from the still.
2-5s: (adjust to chosen duration) one escalation beat then resolve naturally.
Camera: match prior lens feel and movement vocabulary (e.g., same tracking speed class).
Audio: continue ambience; subtle swell only if appropriate.

Constraints:
no watermark, no logo.
```

---

## C) Replace performer / character (JiMeng “Replace in @video1”)

**WeryAI:** Best-effort: **`submit-multi-image`** or **`image` + `last_image`** when the user provides **base plate / pose reference** + **new identity still**—**or** a **single** identity still with a strong “replace subject while keeping motion” prompt. Results depend on model behavior; set user expectations.

**Suggested JSON:** `images`: `[ baseFrameOrKeyPose, newIdentityStill ]` (order per **[WERYAI_VIDEO_API.md](WERYAI_VIDEO_API.md)** multi-image convention) + detailed **`prompt`**.

```text
Mode: Directed edit from references
Assets Mapping:
- Reference A: composition, pose, and scene lighting to preserve
- Reference B: replacement character identity, wardrobe shape, palette

Final Prompt:
Replace the main subject with the identity from the second reference while preserving the scene layout, approximate pose silhouette, timing of actions, and camera path described below.
Maintain clean edge continuity and stable face/body proportions; no extra limbs; no identity flicker.
(Add explicit beat timing for your chosen duration.)

Constraints:
no watermark, no logo, no on-screen text.
```

---

## D) IP-safe original creature battle (text-only, 10s)

**WeryAI:** `submit-text`, `duration`: `10`, `aspect_ratio`: `9:16`.

```text
Mode: Text-only generation
Assets Mapping:
- none

Final Prompt:
vertical 9:16, 10s, family-friendly original cartoon fantasy duel in a sunset forest clearing, vibrant cinematic lighting, expressive faces, smooth animation, high detail
Creature A: a tiny storm-rabbit with glowing cyan antlers and soft cloud-like fur, emits harmless spark particles
Creature B: a mini lava-iguana with crystal scales, ember freckles, and a floating flame orb above its tail
0-3s: dramatic stare-down, swirling leaves, warm sun rays through trees, slow push-in
3-7s: playful high-speed exchange, zigzag spark sprint versus curved ember spin, dynamic tracking camera, readable motion, clean silhouettes
7-10s: both land safely, smile, and perform a friendly team pose on two rocks under a glowing orange-pink sky, uplifting finish

Constraints:
no existing franchise characters, no brand references, no logos, no watermark, no subtitles, no on-screen text, no violence, no injuries
```

---

## E) IP-safe sci-fi hero (text-only, 10s)

**WeryAI:** `submit-text`.

```text
Mode: Text-only generation
Assets Mapping:
- none

Final Prompt:
vertical 9:16, duration 10s, original sci-fi hero short, cinematic city atmosphere after rain, reflective glass towers, cool blue and silver palette, family-friendly action tone, custom powered exo-suit with smooth ceramic panels, hex-light energy core, magnetic boots, forearm thrusters, expressive body language, polished animation quality
Main character nickname: Alloy Sentinel
Support character nickname: Orbit Mentor
0-3s: Alloy Sentinel stands on a high rooftop, suit systems boot sequence, hex-core pulses softly, vapor vents from shoulder ports, camera rises from boots to helmet in a dramatic reveal
3-7s: controlled flight through narrow skyline corridor, short lateral boosts, spiral climb around a tower, Orbit Mentor appears as a distant ally drone giving guidance lights, dynamic tracking camera, readable motion, crisp reflections
7-10s: Alloy Sentinel lands safely on a skybridge, energy core shifts from bright to calm glow, Orbit Mentor drone hovers at shoulder height, both face sunrise over the city, hopeful heroic ending

Constraints:
no Marvel, no Iron Man, no Tony Stark, no Avengers, no arc reactor, no franchise references, no logos, no recognizable character likeness, no watermark, no subtitles, no on-screen text
```

---

## F) Toy / figure dance (reference still, 10s)

**WeryAI:** `submit-image` with **`image`**: toy photo URL; **de-brand** in **`prompt`**.

```text
Mode: Single reference still
Assets Mapping:
- Reference still: proportions, colors, outfit silhouette only — strip all brand language from prompt

Final Prompt:
9:16 vertical, 10s, stylized toy dance animation in a clean studio set, one original vinyl-style art figure performing an upbeat hip-hop routine, playful and family-friendly tone, smooth animation, clean silhouette readability, soft cinematic lighting, simple gradient backdrop, energetic music-video framing
0-3s: figure enters center frame in a neutral stance, subtle head nod and shoulder groove, camera slow push-in from full-body to medium shot
3-7s: main dance combo with clear toy-friendly movement, side step, heel-toe shuffle, arm wave, chest bounce, controlled half-turn, rhythmic camera drift, stable limb motion
7-10s: final combo, short forward glide, hand-point to camera, confident freeze pose, slight camera tilt and gentle punch-in for final beat

Constraints:
no real person likeness, no celebrity likeness, no branded toy names, no logos, no trademark symbols, no text on clothing, no watermark, no subtitles, no violent gestures, no broken joints, no extra limbs, no deformed hands, no flicker, no blur, no face distortion
```

---

## G) Music beat-sync montage (12s)

**WeryAI:** `duration`: `12` is valid (integer 5–15). **No `@audio1` URL**—encode cuts and accents as **time ranges**. Optional **`generate_audio: true`** for generic rhythmic SFX (no copyrighted tracks).

**If user supplies storyboard stills:** `submit-multi-image` with ≤3 URLs; montage language must fit **one coherent clip** (not true multi-shot edit unless model interprets as style).

```text
Mode: Text-led beat sync (optional ≤3 stills for look)
Assets Mapping:
- (Optional) Stills: define color grade anchors or subject variants — describe order in prompt

Final Prompt:
9:16 vertical, 12s, high-energy montage rhythm without naming copyrighted music.
0-4s: quick punch-in cuts on implied downbeats; establish primary visual motif.
4-8s: alternate medium and close shots with kinetic transitions on every ~1s accent.
8-12s: crescendo with strongest motif, then clean landing frame; hold final pose 0.5s.
Maintain consistent color grade and readable composition.

Constraints:
no watermark, no logo.
```

---

## H) Product showcase / e-commerce ad (10s)

**WeryAI:** `submit-image` with product **`image`**; `aspect_ratio`: `16:9` if user wants widescreen (supported).

```text
Mode: Product identity anchor
Assets Mapping:
- Reference still: product front-facing hero photo

Final Prompt:
16:9 widescreen, 10s, 3D product showcase, studio lighting with soft gradient backdrop, cinematic product commercial tone
0-3s: product rotates 360° at medium speed, clean reflections on surface, hero key light from upper-left
3-7s: product pauses, then splits into three sections in a 3D exploded view, each part floats apart with subtle particle trails, smooth transition
7-10s: parts rapidly reassemble with satisfying snap motion, final hero shot with brand-neutral backdrop glow, slight camera push-in for impact
Material rendering: accurate surface finish, glass reflections, metallic sheen where applicable

Constraints:
no watermark, no logo overlay, no text overlay, no price tags, no competitor branding, no distorted proportions
```

---

## I) Short drama with dialogue (15s)

**WeryAI:** `submit-text` **or** `submit-multi-image` if character stills exist (≤2–3). `duration`: `15`.

```text
Mode: Text (optional character stills)
Assets Mapping:
- Optional still A: Character A appearance lock
- Optional still B: Character B appearance lock

Final Prompt:
9:16 vertical, 15s, cinematic short drama, indoor office, warm tungsten with cool window backlight, shallow depth of field, emotionally charged atmosphere
0-5s: close-up of Character A at a desk, tense expression, hands gripping a document
Dialogue (Character A, cold and firm): "The deal is off. I'm done."
Sound: ambient office hum, paper rustling
6-10s: medium two-shot, Character B steps forward reaching out, camera dollies slowly right, tension in body language
Dialogue (Character B, desperate): "You can't just walk away — not after everything."
Sound: footstep on hard floor, subtle dramatic underscore rising
11-15s: Character A stands, turns away toward window, silhouette against city lights, holds document then drops it, pages flutter to floor, camera slow push-in on profile
Sound: paper hitting floor, score resolves to silence, faint city ambience

Constraints:
no watermark, no subtitles, no on-screen text, no jump cuts, no shaky cam
```

---

## J) One-take long shot with multi-image waypoints (15s)

**WeryAI:** `submit-multi-image`, `images`: ≤3 URLs. If the user has **four** locations, **merge** two into one reference or **split** into two segments.

```text
Mode: Multi-image waypoints (max 3 stills on SEEDANCE_2_0)
Assets Mapping:
- Image 1: protagonist opening composition / wardrobe
- Image 2: mid-path environment or blocking beat
- Image 3: destination exterior or final framing anchor

Final Prompt:
16:9 widescreen, 15s, espionage thriller style, continuous one-take tracking shot, no cuts, rainy evening, neon-reflected wet streets, suspenseful atmosphere
Opening matches reference 1: protagonist in a dark coat walks forward, camera follows from the front at full-body framing
0-5s: steady front-tracking, occasional passersby obscure the subject, rain droplets on lens edge, shallow depth of field on subject
6-10s: protagonist turns a corner matching reference 2’s architecture, camera pans to follow; a mysterious figure matching reference 3 lurks at the corner edge watching
11-15s: camera continues forward; protagonist approaches and enters the building facade consistent with reference 3; door closes; camera holds on entrance; rain intensifies
Single continuous camera movement throughout, no cuts, no montage

Constraints:
no watermark, no subtitles, no on-screen text, no jump cuts, no freeze frames
```

---

## K) Multi-segment long video (>15s, 30s example)

**WeryAI:** Two separate **`submit-*`** calls. After segment 1, user (or pipeline) provides **`https`** still of **handoff frame** for segment 2 **`image`**.

### Segment 1 (0–15s) — `submit-text`

```text
## Long video plan
Total target: ~30s
Segments: 2
Aspect ratio: 16:9

### Segment 1
Mode: Text-only
Assets Mapping: none

Final Prompt:
16:9 widescreen, 15s, fantasy cinematic, aerial establishing energy
0-5s: top-down view of swirling cloud sea over mountain peaks, camera slowly pushes down through cloud layer
6-10s: reveal a sword master on a cliff edge, back to camera, robes billowing, dark energy rising on the horizon
11-15s: sword master slowly turns to face camera, draws glowing blade, eyes determined, low voice: "It begins.", hold clean front-facing medium composition

Constraints:
no watermark, no on-screen text

Handoff frame (for your planning): sword master facing camera, medium shot, glowing blade drawn, mountain backdrop, storm clouds ahead
```

### Segment 2 (15–30s) — `submit-image`

- **`image`:** `https` of segment 1 **last frame** (must match handoff).
- **`duration`:** `15`

```text
### Segment 2
Mode: Continuation from handoff still
Assets Mapping:
- Reference still: segment 1 handoff frame (exact pose, lighting, wardrobe)

Final Prompt:
Continue seamlessly from the reference frame; preserve identity, outfit, blade glow, storm light, and camera lens feel.
0-5s: shadow forms emerge from clouds and surge forward; sword master leaps to meet them
6-10s: dynamic aerial combat, blade trails cut through shadow forms that dissolve into ash, orbiting tracking camera
11-15s: sword master lands, sheathes blade, residual golden particles drift, slow push-in on profile against clearing sky, wind ambience to end

Constraints:
no watermark, no on-screen text
```

---

## Quick recipe picker

| User goal | Start here | Typical `submit-*` |
|-----------|------------|---------------------|
| Epic fantasy / adventure | A | `submit-text` or multi-image |
| Continue last shot | B | `submit-image` |
| Swap character in scene | C | `submit-multi-image` |
| Original creatures / heroes | D, E | `submit-text` |
| Toy dance | F | `submit-image` |
| Fast montage feel | G | `submit-text` |
| Product ad | H | `submit-image` |
| Dialogue scene | I | `submit-text` / multi-image |
| One-take chase | J | `submit-multi-image` |
| 30s+ story | K | two calls: text then image |
