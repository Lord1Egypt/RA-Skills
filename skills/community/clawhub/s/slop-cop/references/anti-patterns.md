# Anti-Patterns to Flag

Codified from real shipped bugs. These are the things that look fine in dev and break in prod. Flag any you spot in the asset itself, or in surrounding CSS/HTML context the user shares.

## Image-asset anti-patterns

### AI-hallucinated text shipped to prod  ⚠️ original sin
The single most common slop failure. AI image gens fill text regions with gibberish that looks like text at a glance ("EDIT AGGREE", "BANANN OF MEETING", scribbled approximations of letters). Always transcribe visible text verbatim and flag any non-word. **Automatic `KILL`.**

### Extra / melted / fused fingers
Six fingers, four fingers, a thumb on the wrong side, fingers melting into each other or into objects. **Automatic `KILL`** for anything shipping near a face or as a hero.

### Text overflow / card overlap
If CTA text spills outside a button/squircle, body copy runs under a dashboard card, or cards overlap unrelated content, the asset is not presentable. **Automatic `KILL`** for shipping graphics. This is not a polish issue; it is broken layout.

### Copy contradicts chart/data direction
If visible copy says "Cost per lead trending down" while the graph line is sideways or slightly upward, the visual evidence contradicts the claim. Same for "growth" copy paired with falling metrics, or any KPI/card/graph that tells a different story than its label. **Automatic `KILL`** for shipping creative unless the chart or copy is changed.

### Wrong aspect ratio used as full-bleed
A 1024×1024 square cropped to 1200×400 is not a banner — it's a banner-shaped piece of a square with the subject's head missing. Composition has to match aspect. **`FIX` only if the focal point survives the crop; otherwise `KILL`.**

### Visible watermarks / AI-tool tells
Midjourney corner, Adobe Firefly strip, leftover Getty overlay, "Made with DALL·E" stamps. **Automatic `KILL`** — even faint ones get noticed in compressed form.

### Mixed style without intent
Photoreal shark next to flat cartoon shark on the same page reads as a junk drawer. Flag style-mixing unless the site is intentionally collage-style.

## CSS / HTML anti-patterns (flag when you see surrounding code or the user describes the site)

### `-webkit-text-stroke` on multi-subpath glyphs
Letters with internal openings (A, B, D, O, P, Q, R, a, b, d, e, etc.) render visible seams along the inside of the stroke where subpaths join. Looks like a tear in the letter. Use SVG strokes or paint-order tricks instead.

### `background-size: 100% 100%` on horizon/wave dividers
Stretches the divider horizontally on ultrawide monitors (>2200px) into a smeared mess. Use `background-size: cover` with a sane aspect, or SVG with `preserveAspectRatio="none"` only on shapes that tolerate stretch (solid gradients, not detailed art).

### Pattern backgrounds at overlay opacity <0.7 behind body copy
Body text on a busy pattern with weak overlay is illegible. Bump overlay to ≥0.7 or move pattern out from under text.

### Missing `-webkit-backdrop-filter` prefix
Safari (still, in 2026) needs the prefix for backdrop blur. Without it, the glass effect just… isn't there on iOS. Always pair `backdrop-filter` with `-webkit-backdrop-filter`.

### No `prefers-reduced-motion` respect on animated bubbles/parallax
Auto-playing motion gives vestibular-disorder users a bad time and gets flagged by accessibility audits. Wrap motion in:
```css
@media (prefers-reduced-motion: no-preference) { /* motion */ }
```

### Hero text gradients without paint-order / letterpress fallback on Safari iOS
`background-clip: text` + gradient + stroke in Safari iOS can render with stroke ON TOP of fill, looking like outlined letters. Add `paint-order: stroke fill;` or provide a flat-color fallback via `@supports`.

### JPG used where PNG/WEBP transparency was needed
Logo with white-box background showing on a colored hero. Either re-export with alpha or convert. **`FIX`.**

### Hero `background-image` with no `min-height` and content shorter than image
Empty space under the fold because the bg image dictated height. Set `min-height` explicitly.

### `object-fit: cover` without `object-position`
Cover crops from the center by default. Faces and focal points get decapitated. Always pair with `object-position` when the subject isn't centered.

## Quick reference: hard-kill triggers

1. Hallucinated/gibberish text on a graphic.
2. Extra/melted/fused fingers or limbs.
3. Visible watermark or AI signature.
4. Major brand-palette clash with no recolor path.
5. Hero composition where the focal point doesn't survive the actual crop.
6. Text visibly overflowing outside its container or CTA shape.
7. Cards/buttons/graphs visibly overlapping unrelated content.
8. Copy contradicting visible chart/data/graph direction.
