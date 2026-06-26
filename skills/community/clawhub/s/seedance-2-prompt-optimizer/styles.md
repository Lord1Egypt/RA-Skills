# Visual Styles Reference — Seedance 2.0

Use this file when the user asks about visual style, art direction, or aesthetic descriptors.
Always declare the style explicitly in the prompt — the model can drift without reinforcement.

---

## How to Apply a Style in a Prompt

Style should appear in the **aesthetic description** layer of the standard formula:

```
Subject + Motion + Environment + Camera/Cut + Aesthetic Description + Audio
```

Place the style descriptor early and reinforce it at each shot boundary if the clip is long.

```
[style descriptor], [aspect ratio], [duration]s.
Shot 1: [camera] [subject] [action], maintain [style] throughout.
```

---

## Style Index

| Style | When to use |
|---|---|
| Cinematic Realism | Live-action drama, product ads, short films |
| Documentary | Handheld, authentic feel, journalism, nature |
| 2D Hand-drawn Animation | Storybooks, indie cartoons, whimsical content |
| 2D Japanese Anime | Manga adaptations, action, romance, slice-of-life |
| 3D CG Realistic | High-end product renders, architectural viz |
| 3D Chinese Fantasy CG | Xianxia, wuxia, mythological epics |
| 3D Western Animation | Family-friendly, Pixar-adjacent, comedy |
| Cyberpunk / Neon Sci-Fi | Futuristic city, tech dystopia, music video |
| Ink-Wash / Shuimò | Traditional East Asian art, poetry, nature |
| Lo-fi / Retro Film | Grainy nostalgia, 8mm, VHS, warm tones |
| Minimalist / Flat Design | App ads, explainer video, clean UI showcases |
| Dark Fantasy / Gothic | Horror-adjacent, moody, macabre, supernatural |
| Stop Motion | Tactile, handcrafted feel, artisanal brand |
| Watercolour Illustration | Soft, painterly, dreamlike, children's content |
| Ukiyo-e / Woodblock Print | Japanese heritage, bold outlines, flat colour |

---

## Style Profiles

---

### Cinematic Realism

**Character**: True-to-life lighting, film-grade colour grading, natural textures, physically plausible motion. Feels like a Hollywood or prestige streaming production.

**Key descriptors**:
- `cinematic realism`, `photorealistic`, `35mm film aesthetic`
- `natural ambient lighting`, `shallow depth of field`
- `film grain, anamorphic lens flare`
- `colour graded: teal-and-orange`, `desaturated cool tones`, `warm golden hour`

**Camera defaults**: Steadicam or handheld for drama; dolly/crane for epic moments.

**Negative constraints**: `no cartoon elements, no illustration style, no CG rendering`

**Example prompt**:
```
Cinematic realism, 16:9, 10s.
Shot 1: [WS, golden hour, dolly-in] A middle-aged man in a worn leather jacket
walks slowly along an empty pier toward the water's edge, hands in pockets.
Shot 2: [CU, static, eye level] He stops; wind lifts his collar.
He exhales — breath visible in cold air.
(Muted strings swell softly in the background)
no watermark, no logo, no subtitles, no CG elements
```

---

### Documentary

**Character**: Raw, handheld energy. Natural lighting favoured over studio setups. Subjects often look slightly off-camera. Feels observed rather than staged.

**Key descriptors**:
- `documentary style`, `observational camera`, `handheld with natural shake`
- `available light`, `vérité`, `unscripted feel`
- `muted colour palette`, `slightly underexposed shadows`

**Camera defaults**: Handheld, rack focus, reactive panning to follow subject movement.

**Negative constraints**: `no studio lighting, no posed acting, no CGI`

**Example prompt**:
```
Documentary style, 16:9, 8s.
Shot 1: [MS, handheld, natural shake] An elderly fisherman repairs a net on a wooden
dock at dawn. He works with practiced, unhurried movements. Camera observes from a distance.
Shot 2: [ECU, rack focus] His weathered hands pull the thread through a gap
in the mesh — then pull focus to the grey ocean behind him.
<waves lapping against dock posts>
no watermark, no subtitles, no artificial lighting
```

---

### 2D Hand-Drawn Animation

**Character**: Visible pencil or brush strokes, expressive line variation, slightly wobbly outlines. Feels artisanal and human-made. Colour may bleed slightly outside lines.

**Key descriptors**:
- `2D hand-drawn animation`, `pencil sketch style`, `traditional animation`
- `expressive line weight`, `hand-inked outlines`, `cel animation`
- `warm flat colours`, `subtle paper texture`, `watercolour wash backgrounds`

**Camera defaults**: Simple cuts and pans; avoid complex 3D camera moves.

**Negative constraints**: `no 3D rendering, no photorealism, no CG shading`

**Example prompt**:
```
2D hand-drawn animation, warm flat colours, pencil-inked outlines, 16:9, 8s.
Shot 1: [WS, static] A small fox kit sits at the edge of an autumn forest.
Leaves drift down in spiralling arcs. Background is a loose watercolour wash.
Shot 2: [MCU, gentle push-in] The fox tilts its head curiously.
Its eyes are large and expressive, outlined in thick ink.
(Soft plucked acoustic guitar plays quietly)
no 3D rendering, no photorealism
```

---

### 2D Japanese Anime

**Character**: Bold outlines, large expressive eyes, speed lines for motion, dramatic reaction expressions. Colour is vivid. Motion may use limited frames deliberately for stylistic effect.

**Key descriptors**:
- `2D Japanese anime style`, `manga aesthetic`, `cel-shaded animation`
- `bold black outlines`, `vivid saturated colours`
- `speed lines`, `dramatic reaction frames`, `sparkle effects`
- Sub-styles: `shōnen` (action-heavy), `shōjo` (soft, romantic), `slice-of-life` (calm, everyday)

**Camera defaults**: Dynamic cuts, whip pans, dramatic low angles for action; soft pans for romance.

**Negative constraints**: `no photorealism, no 3D CG rendering, no Western cartoon style`

**Example prompt**:
```
2D Japanese anime style, vivid colours, bold black outlines, 16:9, 10s.
Shot 1: [low angle, fast push-in] A teenage girl in a school uniform sprints
down a hallway, speed lines filling the frame. Her ribbon trails behind her.
Shot 2: [CU, dramatic] She skids to a stop — eyes wide, sparkling with determination.
Shot 3: [WS, static] She faces a closed gymnasium door, fists clenched.
(Upbeat rock guitar riff)
no photorealism, no 3D rendering, maintain anime style throughout
```

---

### 3D CG Realistic

**Character**: High polygon count, ray-traced lighting, physically based rendering (PBR). Looks like a high-end product render or architectural visualisation. Surfaces have realistic material response to light.

**Key descriptors**:
- `3D CG realistic render`, `photorealistic 3D`, `ray-traced lighting`
- `physically based rendering (PBR)`, `subsurface scattering`
- `studio HDRI lighting`, `4K texture detail`
- `glass refraction`, `metallic sheen`, `matte ceramic`, `velvet surface`

**Camera defaults**: Slow controlled moves; orbit shots work well for products.

**Negative constraints**: `no illustration style, no cartoon shading, no flat colour`

**Example prompt**:
```
3D CG realistic render, ray-traced studio lighting, 16:9, 8s.
Shot 1: [static, eye level, MCU] A glass perfume bottle sits on a white marble surface.
Studio rim lighting catches the curved glass — caustic light patterns fan across the marble.
Shot 2: [slow 180° arc, low angle] Camera orbits the bottle. Liquid inside shifts
with amber warmth. Reflection of the studio softbox visible in the glass.
no watermark, no illustration style, no flat colour, no subtitles
```

---

### 3D Chinese Fantasy CG (Xianxia / Wuxia)

**Character**: Epic scale, flowing robes, ethereal light effects, ink-wash sky backgrounds rendered in 3D. Characters have idealised proportions. Magic and qi energy visualised as coloured particle systems.

**Key descriptors**:
- `3D Chinese fantasy CG style`, `xianxia aesthetic`, `wuxia cinematics`
- `flowing silk robes in motion`, `qi energy particle effects`, `immortal cultivation`
- `ink-wash mountain backdrop in 3D`, `celestial palace`, `misty cliff edges`
- `jade green and crimson palette`, `golden divine light`

**Camera defaults**: Sweeping crane shots, dramatic low angles, slow-motion impact frames.

**Negative constraints**: `no photorealistic live action, no Western fantasy style, maintain 3D CG style`

**Example prompt**:
```
3D Chinese fantasy CG style, xianxia aesthetic, 16:9, 12s.
Shot 1: [crane shot rising] A young immortal in white silk robes stands on a floating
stone platform above the clouds. Her sleeves billow in wind. Ink-wash mountains
recede beneath her.
Shot 2: [low angle, slow push-in] She raises one hand — golden qi particles spiral
upward from her palm, coalescing into a radiant sphere.
Shot 3: [ECU] Her eyes open — irises glow amber.
<thunder rolls in the distance> (ethereal guqin melody)
no photorealism, no live action, maintain CG style throughout, no subtitles
```

---

### 3D Western Animation

**Character**: Rounded, expressive character models with exaggerated proportions. Clean, vibrant colour. Bright, even lighting. Comedic timing in motion. Think modern family-friendly CG film aesthetic.

**Key descriptors**:
- `3D Western animation style`, `Pixar-adjacent CG`, `family animation aesthetic`
- `rounded exaggerated proportions`, `bright saturated colours`
- `clean PBR shading`, `expressive facial rigs`, `squash-and-stretch motion`

**Camera defaults**: Smooth crane/dolly moves, wide angles for comedy, close-ups for emotion.

**Negative constraints**: `no anime style, no 2D flat animation, no photorealism`

**Example prompt**:
```
3D Western animation style, bright saturated colours, squash-and-stretch motion, 16:9, 8s.
Shot 1: [WS, low angle] A small round robot in a cosy kitchen reaches up to a counter
that is clearly too tall for it. It stretches comically, wheels spinning on the tiles.
Shot 2: [MCU] Its round eyes go wide in determination — then it rockets upward
on a burst of steam from its feet, slamming both hands on the counter.
Shot 3: [CU] It beams proudly at the camera.
(Upbeat tuba-and-strings comedy score)
no photorealism, no anime, maintain Western animation style
```

---

### Cyberpunk / Neon Sci-Fi

**Character**: Rain-wet streets reflecting neon signage, high contrast between deep shadows and vivid coloured light, dense layered urban environments, holographic overlays.

**Key descriptors**:
- `cyberpunk aesthetic`, `neon-lit dystopia`, `retrofuturistic sci-fi`
- `rain-wet reflective streets`, `neon purple and cyan rim lighting`
- `holographic projections`, `digital glitch overlays`
- `ultra-dense urban skyline`, `flying vehicles`, `corporate megastructures`

**Camera defaults**: Low angles, dramatic shadows, slow drone sweeps, close-ups with heavy atmospheric haze.

**Negative constraints**: `no pastoral scenes, no natural daylight, no clean environments`

**Example prompt**:
```
Cyberpunk neon sci-fi, rain-slicked streets, neon cyan and magenta palette, 16:9, 10s.
Shot 1: [drone aerial, descending] Camera descends through a canyon of skyscrapers.
Neon signage reflects in every rain-wet surface. Flying delivery drones weave between towers.
Shot 2: [low angle, looking up] A figure in a long reflective coat stands at a crosswalk.
Holographic ads cycle above — her face illuminated in shifting colour.
Shot 3: [MCU, static] She pulls up her hood and steps into the rain.
<rain on concrete> <distant neon sign buzzing> (synthesiser bass pulse)
no subtitles, no watermark, no daylight scenes
```

---

### Ink-Wash / Shuimò (水墨)

**Character**: Monochromatic or near-monochromatic palette inspired by traditional Chinese brush painting. Subjects bleed into wet paper texture. Negative space used expressively. Motion is slow and deliberate.

**Key descriptors**:
- `ink-wash style`, `shuimò aesthetic`, `Chinese brush painting`
- `black ink on rice paper`, `bleeding ink edges`, `expressive empty space`
- `muted grey-black palette with selective colour accent`
- `misty, atmospheric, contemplative`

**Camera defaults**: Slow pans, minimal movement; still shots preferred.

**Negative constraints**: `no vivid colours, no sharp outlines, no CG shading, no Western illustration`

**Example prompt**:
```
Ink-wash shuimò style, black ink on paper texture, selective red accent, 16:9, 8s.
Shot 1: [WS, very slow pan right] Sparse ink-brush pine trees emerge from white mist.
A single crane stands still in the middle ground — rendered in bold black strokes.
Shot 2: [MCU, static] The crane lifts one leg slowly, feathers detailed in fine hatched lines.
A single red sun disc sits in the upper corner — the only colour in the frame.
(Soft xiao flute plays a solitary melody)
no vivid colours, no CG rendering, maintain ink-wash aesthetic throughout
```

---

### Lo-fi / Retro Film

**Character**: Grain, light leaks, desaturated or cross-processed colour. Feels like archival footage, Super 8, or expired 35mm. Warmth and imperfection are aesthetic goals.

**Key descriptors**:
- `lo-fi aesthetic`, `Super 8 film grain`, `VHS tape texture`
- `heavy film grain overlay`, `light leak flares`, `colour cross-processing`
- `warm faded tones`, `vignette`, `slightly overexposed highlights`
- `retro 1970s colour grade`, `nostalgic`, `faded Kodak palette`

**Camera defaults**: Handheld, natural shake, occasional rack focus.

**Negative constraints**: `no clean digital look, no vivid saturation, no sharp crisp edges`

**Example prompt**:
```
Lo-fi Super 8 film aesthetic, heavy grain, warm faded palette, vignette, 16:9, 8s.
Shot 1: [MS, handheld] Two teenagers run through a summer garden — sprinkler arcing
across the frame. Image is slightly overexposed at the edges.
Shot 2: [ECU, rack focus] A bare foot splashes into a paddling pool.
Light leaks streak across the top of the frame.
(Soft lo-fi hip-hop beat, slightly off-speed)
no clean digital look, no sharp edges, maintain grain and warmth throughout
```

---

### Minimalist / Flat Design

**Character**: Solid colour fills, no gradients or shadows, geometric shapes, clean white or single-colour backgrounds. Motion is smooth and purposeful. Feels like an app explainer or modern brand ad.

**Key descriptors**:
- `flat design animation`, `minimalist style`, `clean vector aesthetic`
- `solid colour fills`, `no shadow or gradient`, `geometric shapes`
- `white or single-colour background`, `sans-serif typography`
- `smooth easing animation`, `2D motion graphics`

**Camera defaults**: Static camera; let the graphic elements animate rather than the camera move.

**Negative constraints**: `no photorealism, no 3D shading, no texture or grain, no complex backgrounds`

**Example prompt**:
```
Flat design animation, minimalist, solid colour fills, no gradients, 16:9, 8s.
Shot 1: [static, WS] On a clean white background, a simple blue circle expands
from the centre of the frame — a stylised head appears within it.
Shot 2: [static] From the circle, three geometric icons radiate outward:
a book, a lightbulb, a speech bubble — each animating in with a smooth pop.
Shot 3: [static] Text appears below the icons: clean sans-serif, black.
(Soft upbeat xylophone melody)
no photorealism, no 3D, no texture, no gradients
```

---

### Dark Fantasy / Gothic

**Character**: Desaturated palette with selective deep jewel tones. Heavy use of shadow. Candlelight, moonlight, and bioluminescence as light sources. Environments feel ancient and decaying. Creatures and characters have heightened, dramatic design.

**Key descriptors**:
- `dark fantasy aesthetic`, `gothic horror atmosphere`
- `desaturated palette with deep crimson and midnight blue accents`
- `candlelit dungeon`, `moonlit graveyard`, `haunted forest`
- `volumetric fog`, `dramatic chiaroscuro lighting`
- `crumbling stone architecture`, `twisted bare trees`

**Camera defaults**: Slow dolly, handheld for tension, sudden crash zoom.

**Negative constraints**: `no bright cheerful colours, no clean modern environments`

**Example prompt**:
```
Dark fantasy gothic aesthetic, desaturated palette, deep crimson accents,
heavy chiaroscuro lighting, 16:9, 10s.
Shot 1: [WS, slow dolly forward] A stone corridor lit only by wall-mounted torches.
Shadows lurch and twist. A hooded figure at the far end turns slowly toward camera.
Shot 2: [CU, low angle] The figure's face — half in shadow, eyes catching torch light.
Shot 3: [ECU] A gauntleted hand closes around a cracked obsidian amulet.
<stone grinding> <torch flame crackling> (low cello drone builds)
no bright colours, no modern settings, maintain gothic atmosphere throughout
```

---

### Stop Motion

**Character**: Slight motion jitter between frames, visible texture of physical materials (clay, felt, paper, wood). Deliberate, slightly imprecise movement that communicates craft. Light may shift subtly between frames.

**Key descriptors**:
- `stop motion animation`, `claymation`, `felt puppet animation`, `paper cut-out animation`
- `visible material texture`, `slight frame-to-frame jitter`
- `handcrafted imperfection`, `physical miniature set`
- `warm studio lighting on set`, `shallow depth of field`

**Negative constraints**: `no smooth CG animation, no photorealism, no digital polish`

**Example prompt**:
```
Stop motion claymation style, visible clay texture, warm studio lighting,
slight frame jitter, 16:9, 8s.
Shot 1: [WS, static] A small clay house sits on a miniature paper hill.
A clay figure with round hands pushes open the front door.
Shot 2: [MS, static] The figure steps onto the doorstep and looks up —
eyes are simple inset buttons that shift slightly with each frame.
Shot 3: [ECU] A clay hand reaches toward a paper flower.
(Gentle hand-clapping folk tune)
no smooth digital animation, no CG shading, maintain claymation imperfection
```

---

### Watercolour Illustration

**Character**: Soft painted edges, colour bleeding and blooming, visible brushstrokes, translucent layered washes. Backgrounds often loose and impressionistic; subjects more defined but still painterly.

**Key descriptors**:
- `watercolour illustration style`, `painted aesthetic`, `soft brushstroke edges`
- `colour bleeding and blooming`, `translucent layered washes`
- `loose impressionistic background`, `visible paper grain`
- `pastel palette`, `warm honey tones`, `cool lavender shadows`

**Camera defaults**: Gentle slow pans, soft push-ins.

**Negative constraints**: `no sharp digital edges, no photorealism, no flat vector design`

**Example prompt**:
```
Watercolour illustration style, soft bleeding edges, pastel palette,
visible paper grain, 16:9, 8s.
Shot 1: [WS, very slow pan] A painted forest path in autumn.
Leaves are loose watercolour washes of amber and gold — edges bleed into each other.
Shot 2: [MS, gentle push-in] A child in a red coat walks along the path.
Her figure is more defined; the background behind her remains impressionistic.
(Gentle piano, unhurried tempo)
no sharp edges, no photorealism, maintain watercolour softness throughout
```

---

### Ukiyo-e / Woodblock Print

**Character**: Bold flat outlines, no gradient fills, strong diagonal compositions, stylised waves or clouds as background elements. Colour palette is limited and deliberate. Feels like a moving woodblock print.

**Key descriptors**:
- `ukiyo-e woodblock print style`, `Japanese heritage aesthetic`
- `bold flat outlines`, `limited flat colour palette`
- `stylised wave patterns`, `diagonal cloud formations`
- `no gradient, no shadow — flat fill only`
- `indigo, vermillion, and ochre palette`

**Camera defaults**: Static or very slow pan only — aggressive camera motion conflicts with the style.

**Negative constraints**: `no gradients, no 3D shading, no photorealism, no Western illustration`

**Example prompt**:
```
Ukiyo-e woodblock print style, bold flat outlines, limited palette of indigo and vermillion,
no gradients, flat colour fills, 16:9, 8s.
Shot 1: [WS, static] A great stylised wave rises at the centre of the frame —
outlined in bold black, filled with flat indigo. A small vessel rides its crest.
Shot 2: [slow pan right] Mount Fuji appears at the right edge — flat white peak
against a pale ochre sky filled with diagonal cloud formations.
(Taiko drum rolls softly) <wind gusts>
no photorealism, no gradients, no 3D rendering, maintain flat woodblock aesthetic
```

---

## Style Combination Tips

Some styles can be layered for hybrid results:

| Combination | Descriptor example |
|---|---|
| Anime × Dark Fantasy | `2D anime style, dark fantasy palette, gothic atmosphere` |
| Ink-Wash × 3D CG | `3D CG render with ink-wash post-processing overlay` |
| Lo-fi × Documentary | `documentary style, Super 8 film grain, lo-fi colour` |
| Watercolour × Minimalist | `watercolour illustration, minimal composition, clean pastel fills` |
| Cyberpunk × Anime | `2D anime style, cyberpunk neon palette, rain-slicked urban setting` |

Always reinforce the combined style in each shot — hybrid styles are more prone to drift.

---

## Style × Common Issues

| Style | Most likely issue | Prevention |
|---|---|---|
| Any animation style | V-4 style drift to realism | Reinforce style name every shot |
| 9:16 ratio (any style) | V-2 subtitle generation | Switch to 16:9 or add "no subtitles" |
| Multi-character scenes | V-7 duplicate characters | Add "exactly one instance of each character" |
| Anime / 3D CG with multi-angle ref images | V-7 twin issue | Clarify all angles are the same character |
