# Image Overlay & Text-on-Image Rules

Two rules that govern any poster where text sits on top of an image — full-bleed background, large photo well with title bar, or generated/AI image with text overlay.

## Rule 1 — Selection first, mask only if selection fails

The default editorial-magazine answer is **no mask**. Real magazine covers (Kinfolk, Cereal, Apartamento, Monocle) almost never lay a uniform black gradient over a hero photo. They rely on **photo selection + composition** so text lands in a quiet zone naturally.

Apply the steps in order. Stop at the first one that passes.

### Step 1 — Photo selection (the main lever)

Before picking a mask, verify the photo qualifies for full-bleed treatment. Both tests must pass:

**Quiet-zone test**: at least one band of ≥30% canvas (full width × ≥30% height, or full height × ≥30% width) is low-detail / low-contrast / uniform. Examples: out-of-focus background, deep shade, fog, calm water, plain sky, blurred grass. This band is where the title will land.

**Light test**: the photo carries atmospheric / restrained light — overcast, dawn fog, golden hour, forest understory, film softness, dusk silhouette. Reject high-saturation noon shots, on-camera flash, generic stock cheerfulness.

If either test fails, **the photo is wrong for M16**. Fall back to M01 (split-layout cover with photo in a frame), or shoot/source again.

### Step 2 — Compose without a mask first

Place the title inside the qualified quiet zone. Run the thumbnail contrast check (Step 4). If it reads clean, ship as-is.

A no-mask cover signals craft. A heavily masked cover signals "we couldn't find the right photo." Try Step 2 every time before reaching for Step 3.

### Step 3 — Localized, image-toned tint (fallback only)

Only when Step 2 fails the contrast check. Three rules:

1. **Localized, not full-canvas.** Tint only the title region. Use `radial-gradient` centered on the title block, or a one-sided linear gradient that fades to fully transparent past the title. Never `inset: 0` over the whole image with a uniform alpha curve.

2. **Image-toned, not black.** Sample a dark tone already in the photo and use it as the tint color. Forest → deep moss `#1a2818`. Dusk → tea-rose dusk `#4a2638`. Snow → cool grey-blue `#2a3438`. Pure black `#000` reads as "annotation layer," not "atmospheric depth."

3. **Soft, not opaque.** Peak alpha 0.15-0.30 in the title region, falling to 0 outside. If you need >0.40 to read, the photo failed Step 1 — go back.

```css
/* Example: title in lower-left, image-toned soft tint */
.hero-bleed::after {
  content: "";
  position: absolute; inset: 0;
  background: radial-gradient(
    60% 45% at 25% 80%,
    rgba(26, 40, 24, 0.28) 0%,
    rgba(26, 40, 24, 0.0) 100%);
  pointer-events: none;
}
```

### Step 4 — Thumbnail contrast check (always)

Whether or not you applied a tint:
- Render the PNG, downscale to 360px wide, and look
- Title strokes must be legible without zoom
- If title looks like it's "fighting" the photo → swap photo or shift title to a different quiet zone, **not** strengthen the mask

### Banned

- Uniform full-canvas vertical falloff (`rgba(0,0,0,.55) → .10 → .10 → .80`). That is game-key-art treatment, not editorial
- Pure black mask color. Always image-toned
- Flat black/white rectangle behind text
- `mix-blend-mode: difference` for readability
- `img { opacity: .6 }` — kills the photo's depth
- Reaching for Step 3 before honestly attempting Step 1 with a better photo

---

## Rule 2 — Place text away from subject / face zones

Posters in 旅行/游戏/影视/穿搭/美食 frequently use a real photo as the hero. The photo has a subject — a face, a hand, a product, a peak. Text that overlaps the subject reads as graffiti, not editorial.

### Subject zone discovery

Before designing the title position on a hero photo, look at the image and observe:

1. Where is the **primary subject's face / focal feature**?
2. Where is the **edge of the subject's silhouette**?
3. Where is the **largest open / low-detail area**?

Record the answers as a comment in the HTML next to the hero block:

```html
<!-- subject map (SpaceX cover hero):
     rocket launch flame: 50% x 60% y, occupies ~30% of frame
     smoke cloud: lower 40% of frame
     safe text zone: top band (0-25% y) and upper-left corner
-->
```

### Safe-zone placement rules

Given the subject map, place text in this order of preference:

1. **Above + below** the subject (kicker top, title bottom). 90% of full-bleed covers should do this
2. **One side** — if subject occupies one vertical column, text fills the opposite column
3. **Diagonal corner** — only when subject is in one corner and opposite corner is genuinely empty. Rare

**Never place display titles across the face.** A 88px Chinese title cutting through a person's eyes is destructive even with a mask.

### Composition discipline (editorial look)

- **Asymmetric placement.** Titles offset to one side / one corner read more confident than dead-centered
- **Generous negative space.** Title should occupy ≤40% of the canvas
- **Title in one quiet zone, only one.** Splitting the title into two zones (top + bottom) is fine; splitting into three is busy
- **Title never overlaps the subject silhouette.** If the only safe placement requires crossing the subject's edge, switch modes

### Crop guards

| Subject location in raw image | Recommended `object-position` for 3:4 crop |
|------------------------------|---------------------------------------------|
| Face/focus in upper third | `center 25%` |
| Face/focus in middle third | `center center` |
| Face/focus in lower third | `center 70%` |
| Wide landscape, no single subject | `center 35%` |
| Vertical portrait, full body | `center top` |

---

## Checklist before delivery

Run this for every poster that has text touching an image:

- [ ] Photo passes quiet-zone test AND light test
- [ ] Tried no-mask composition first. Tint only added if contrast check failed
- [ ] If tinted: localized, image-toned color (not pure black), peak alpha ≤ 0.30
- [ ] No full-canvas vertical falloff present
- [ ] Subject map documented as a comment near the hero block
- [ ] No display title (≥72px) overlaps a face/hand/key product feature/subject silhouette
- [ ] Title occupies ≤40% of canvas. Asymmetric placement preferred
- [ ] `object-position` chosen intentionally, not left at default
- [ ] Thumbnail test passed (downscale to 360px wide; title still legible)
