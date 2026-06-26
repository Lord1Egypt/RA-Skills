# Style: Maple Cartoon (MapleStory-inspired cartoon pixel)

One of two style options for msw-painter. Choose this style for **characters, NPCs, monsters, and any sprite that should feel cute / illustrated / storybook-like**. For icons, tiles, and simple UI blocks where a clear retro look is desirable, prefer the [Chunky Pixel style](style-chunky-pixel.md).

The Maple Cartoon style is **higher-resolution pixel art** with **rich stepped shading**, **colored outlines (selout)**, and **selective anti-aliasing** on silhouette edges. The result reads as "painted / cartoon" rather than "retro 8-bit", while still being made of discrete pixels on a grid.

## Core principles

- **Higher logical grid** — typical working grid is 32×32 to 128×128 (vs 16×16 for chunky). This gives room for facial features, shading, and selout pixels. See the "Maple cartoon working grid" table in [size-guide.md](size-guide.md).
- **Rich stepped shading** — 4–6 color levels per surface (base + 2 darker + 2 lighter + optional rim light), still stepped (no gradient API), just with more steps than chunky.
- **Selout (colored outlines)** — outlines are NOT pure black. Use a desaturated, darker version of the adjacent fill color so the outline blends with each surface.
- **Selective anti-aliasing** — on silhouette edges and curved outlines, place a single intermediate-color pixel between two contrasting colors to soften the staircase. **Only on silhouettes**, never on internal shading.
- **Saturated pastel palette** — warm, slightly desaturated colors. Avoid pure primaries (`#FF0000`, `#00FF00`). Prefer `#E85A4F`, `#7BC96B` etc.
- **Grid alignment is still mandatory** — no fractional coordinates, no curve APIs, no gradient APIs.

## Pixel art implementation per medium

### SVG

```xml
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="100%" height="100%"
     style="image-rendering: pixelated; image-rendering: crisp-edges;">
  <!-- Base fill -->
  <rect x="20" y="16" width="24" height="20" fill="#F4C8A8"/>
  <!-- Selout outline (darker version of base) -->
  <rect x="19" y="16" width="1" height="20" fill="#8B5A3C"/>
  <!-- Soft AA pixel on a diagonal edge (intermediate color between outline and base) -->
  <rect x="19" y="15" width="1" height="1" fill="#B98060"/>
</svg>
```

### HTML5 Canvas

```javascript
// `c` and `ctx` are auto-exposed by render.cjs (imageSmoothingEnabled = false already).
const GRID = 64;
const s = c.width / GRID;
const px = (x, y, color) => { ctx.fillStyle = color; ctx.fillRect(x * s, y * s, s, s); };

// Base
for (let x = 20; x < 44; x++) for (let y = 16; y < 36; y++) px(x, y, '#F4C8A8');
// Selout outline column
for (let y = 16; y < 36; y++) px(19, y, '#8B5A3C');
// Soft AA corner pixel
px(19, 15, '#B98060');
```

### HTML

HTML is rarely the right choice for cartoon pixel art. Prefer SVG or Canvas. If you must use HTML, render each pixel as a tiny absolutely-positioned `<div>`, but the code becomes verbose quickly.

## Color palette

### Recommended palette feel

- **Warm and slightly desaturated.** Think children's book illustration, not neon arcade.
- **Hues**: salmon (`#E85A4F`), peach (`#F4C8A8`), butter (`#FFE08A`), sage (`#A8D5A0`), sky (`#A8D8E8`), lavender (`#C8B4E8`), cocoa (`#8B5A3C`).
- **Avoid**: pure `#000000`, pure `#FFFFFF`, fully saturated primaries.

### Per-surface shading recipe (4–6 levels)

For each surface (e.g. the body of a slime), prepare a small ramp:

| Level | Role | Recipe from base |
|-------|------|------------------|
| 0 | Deep shadow | base − 40% lightness, +5% saturation |
| 1 | Mid shadow | base − 20% lightness |
| 2 | **Base** | the primary fill color |
| 3 | Mid highlight | base + 15% lightness |
| 4 | Top highlight | base + 30% lightness, slight hue shift toward yellow |
| 5 | Rim light (optional) | base + 40% lightness, used as 1px line on the dark side |

Example for a green slime with base `#7BC96B`:
- Deep shadow: `#3F7A3A`
- Mid shadow: `#5BA853`
- Base: `#7BC96B`
- Mid highlight: `#A5DC95`
- Top highlight: `#D4F0C2`
- Rim light: `#EAFADE`

Apply each level in shrinking bands, **2–4 px wide each**, following the form of the surface.

## Selout (colored outline) recipe

Pure black outlines (`#000000`) make the sprite feel harsh and "retro-comic". MapleStory-style sprites use a **darker, slightly desaturated version of the adjacent fill color** as the 1-pixel outline.

Rule of thumb: outline color = base color with **lightness − 40~50%**, **saturation similar or slightly lower**.

| Surface base | Selout outline |
|--------------|----------------|
| Skin `#F4C8A8` | `#8B5A3C` (warm dark brown) |
| Green leaf `#7BC96B` | `#2F5A2A` (forest green) |
| Red cloth `#E85A4F` | `#7A2A20` (dark wine) |
| Blue water `#5AA8E8` | `#1E4A7A` (deep navy) |
| Yellow metal `#F4D060` | `#8A6A20` (bronze) |

When two outlined surfaces meet (e.g. skin meets shirt), use the **darker of the two surfaces' outlines** at the boundary, OR omit the outline entirely and rely on the color contrast.

## Selective anti-aliasing (selout AA)

On a diagonal or curved silhouette, a hard outline reads as a staircase. Place a **single intermediate-color pixel** at the inside corner of each step to soften it visually.

```
. . . O O O .         . . . O O O .
. . O X X X .         . . a X X X .       a = AA pixel
. O X X X X .   →     . a X X X X .       (color between O and X)
O X X X X X .         a X X X X X .
```

The AA color is mixed roughly halfway between the outline (`O`) and the inner fill (`X`). For `O = #8B5A3C` and `X = #F4C8A8`, a reasonable AA value is `#B98060`.

**Strict rules**:
- AA pixels ONLY on the silhouette (outer edge of the sprite, or the boundary between sprite and transparent background).
- NEVER use AA on internal shading boundaries. Internal shading stays stepped.
- Use 1 AA pixel per step at most. Stacking AA pixels turns the sprite mushy.

## Dithering (allowed sparingly)

For large soft surfaces (sky, water, a big shield) where stepped bands look too obvious, use a **2×2 checkerboard dither** to blend two adjacent levels.

```
Level A . Level A .            (checker pattern between
. Level B . Level B             level A and level B)
Level A . Level A .
. Level B . Level B
```

Constraints:
- Use only between two adjacent ramp levels (e.g. base ↔ mid highlight). Never across more than one step.
- Use only on large flat fields (≥ 8×8 px of dithered area). Tiny details should stay stepped.
- Never use dithering on a character's face or any detail-critical area.

## Character proportions (SD / chibi)

MapleStory-style characters are **2 to 3 heads tall** (super-deformed / chibi proportions).

| Total height | Head | Torso | Legs |
|--------------|------|-------|------|
| 64 px (2.5-head) | 26 px | 18 px | 20 px |
| 96 px (3-head)   | 32 px | 28 px | 36 px |
| 128 px (3-head)  | 42 px | 38 px | 48 px |

### Face features

- **Eyes**: large, round, **3–5 px wide**. Place them in the upper third of the face, spaced apart by roughly 1 eye-width. Add a 1-px white highlight inside each pupil.
- **Nose**: 1-px dot, or omit entirely on smaller sprites.
- **Mouth**: 2–3 px wide, 1 px tall, often a simple horizontal line or a tiny "v" / "u".
- **Cheek blush**: 1–2 px of soft pink (`#F4A8B8`) just below the eyes. Optional but very on-tone.
- **Outline of the head**: full selout in warm dark brown (`#8B5A3C`) — never black.

### Hair

- Solid block of base color + 1 highlight band on top + 1 shadow band underneath.
- A few **1-px flyaway strands** silhouetted against the background sell the cartoon look.

## Forbidden (still applies)

- **Curve APIs**: `arc()`, `arcTo()`, `bezierCurveTo()`, `quadraticCurveTo()` — round shapes must be made by placing pixels directly. (Selective AA softens visual roundness without using these.)
- **Soft effect APIs**: `box-shadow`, `filter: blur()`, `filter: drop-shadow()` — depth must come from manual stepped shading.
- **Gradient APIs**: `createLinearGradient()`, `createRadialGradient()`, CSS `linear-gradient()`/`radial-gradient()` — gradients must come from stepped bands and optional 2×2 dithering.
- **Fractional coordinates**: `fillRect(10.5, 20.3, ...)` — breaks grid alignment.
- **Pure black outlines** (`#000000`) — use selout.
- **Heavy AA / interior AA** — AA only at the silhouette, max 1 pixel per step.

## Drawing round shapes manually

Use the chunky midpoint circle as a starting silhouette, then add **1 selout AA pixel at each corner step**.

Example: a 12×12 cartoon-style circle.

```
. . . O O O O O O . . .
. . O X X X X X X O . .
. O X X X X X X X X O .
O X X X X X X X X X X O
O X X X X X X X X X X O
O X X X X X X X X X X O
O X X X X X X X X X X O
O X X X X X X X X X X O
O X X X X X X X X X X O
. O X X X X X X X X O .
. . O X X X X X X O . .
. . . O O O O O O . . .
```

Then sprinkle 1 AA pixel (mixture color between `O` and `X`) at each `.` cell that touches both `O` and `X` diagonally. This single tweak transforms a chunky circle into a soft cartoon button.

## Common reusable accents

| Accent | Purpose | Recipe |
|--------|---------|--------|
| Cheek blush | Cuteness on faces | 1–2 px soft pink (`#F4A8B8`) under eyes |
| Eye highlight | Liveliness | 1 px white inside each pupil, upper-left |
| Rim light | Form definition | 1 px lightest-ramp color on the dark side of the silhouette |
| Specular highlight | Glossy materials | 2–3 px cluster of lightest-ramp on metal/gem |
| Drop shadow on ground | Grounded look (only when entity sits on a tile) | 4–6 px oval of dark gray with 50% alpha, centered under feet |
