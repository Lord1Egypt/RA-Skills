# Style Diff Notes — Reference vs v3 HTML

**Reference:** `style-target-care.png` (copied to `/workspace/ref-care.png`)  
**Candidate:** `care-knowledge-map-v3.png` / `care-knowledge-map-v3.html`  
**Verdict:** Layout skeleton is close; **gestalt still Soft UI / planner-app**, not hand-drawn study-poster. Style-guide failure modes still active.

---

## Ruthless visual gaps (concrete)

| Area | Reference | v3 still does |
|------|-----------|---------------|
| **Borders** | Thin, soft marker/watercolor edges; slight wobble; title often a soft color *wash*, not a hard frame | Thick **4.5px solid** CSS borders + dashed inner ring; perfect vector curves; reads as sticker UI chrome |
| **Hub color / frame** | Pale near-white / soft cream hub; yellow「核心词」capsule with sparkle energy; light, open center | Corn-yellow `#fff8dc` card + **heavy navy multi-border** (solid + dashed outer + inset) + offset shadow → framed Soft-UI badge |
| **Arrow weight** | Felt-tip marker: thick *and* irregular, pressure variation, imperfect heads | Uniform SVG `stroke-width: 6` Béziers + clean triangle heads — bold but **machine-smooth** |
| **Illustration rendering** | Outlined chibi *scenes* (ink outline, blush, props, action lines) as sticker mnemonics | Flat SVG “bean” characters / icon-ish props; under-inked, under-scenic, clipart scale |
| **Paper texture** | Light cream + subtle grain / watercolor paper | Darker tan `#f3e7c8` + loud **20px radial dot grid** (`#bba67a`) → bullet-journal Soft UI |
| **Title font energy** | High-bounce brush / whiteboard marker poster lettering | ZCOOL KuaiLe present but sits on Soft-UI chrome → flatter, less marker pressure / bounce |
| **Card shadows** | Flat on paper (depth via color/wash, not lift) | Hard offset `box-shadow: 6px 7px 0 rgba(...)` sticker shadows |
| **Spacing density** | Near-square packed poster; gutters filled with doodle energy | 16:9 with large empty grid-showing gutters; airy web-component spacing |
| **Bottom chain shape** | Organic cloud / paint-blob banner + soft watercolor capsules (fuzzy edges) | Navy Soft-UI bubble + perfectly bordered pastel capsules + thin `→` + offset shadows |

---

## Must-have visual rules (actionable for image generation)

- **Paper:** Light cream / off-white (`~#FEF8DC`–`#FFF9EF`), **subtle grain only**. No strong geometric dot/square grid. Feels like scanned sketchbook paper.
- **Overall vibe:** 手帐 / teacher whiteboard / doodle poster — **not** Soft UI, not planner app, not component library screenshot.
- **Hub:** Soft pale cream/yellow fill; thin imperfect outline (warm yellow-orange OR soft navy, not triple chrome). 「核心词」as bright yellow capsule with small sparkle/sunburst rays. Center must feel open and hand-drawn, not a product card.
- **Borders:** Medium felt-tip weight with **visible wobble / pressure variation**. Prefer single imperfect stroke or soft watercolor edge. Optional faint dashed *inner* notebook ruling — never thick double Soft-UI frames.
- **Title pills on cards:** Soft pastel **marker wash** or irregular capsule overlapping the border; fuzzy edges OK. Not perfect geometric pills with hard 3px outlines + sticker shadow.
- **Arrows:** Thick navy/blue **marker** curves; slight width jitter; simple open/felt arrowheads; not uniform SVG strokes.
- **Illustrations:** Cute chibi **character scenes** with clear dark outlines, soft flat color + light blush/shade, props tied to meaning (heart, dog, magnifying glass, book, shield). Large enough to be memory anchors — not tiny lineless beans.
- **Shadows:** Prefer none or ultra-soft paper contact. **Forbid** hard offset Soft-UI sticker shadows (`Npx Mpx 0 rgba`).
- **Title type:** High-energy handwritten Chinese (站酷快乐体 / 马善政 style) with bounce, optional squiggle underline / stars. Must dominate the top edge.
- **Cards:** Macaron pastel fills/edges (sky, mint, lavender, soft yellow). Slight 0.5–1.5° tilt OK. Dense but readable packing.
- **Bottom chain:** Start with **organic cloud / paint-blob / ribbon** slogan shape (rough brush edge). Follow with soft watercolor capsules (tint fills, soft edges) linked by short hand-drawn arrows — not a row of perfect outlined UI pills.
- **Color accents:** Target English phrases in vivid red or deep navy; keep body text dark navy/charcoal.

---

## Forbidden traits (what v3 still has)

- Loud **dot-grid** background on darker tan (planner / Soft UI tell).
- **Thick perfect geometric borders** (4–5px solid) + dashed outer rings + inset rings that read as product chrome.
- Hub as **navy multi-border Soft-UI card** with hard offset shadow (even if fill is yellow).
- Uniform **vector-perfect** thick arrows (no marker jitter).
- **Flat SVG bean / icon illustrations** instead of outlined chibi scenes.
- Hard **offset sticker shadows** on cards, hub, capsules (`box-shadow: Npx Mpx 0 …`).
- Title that looks like a **web font on a dashboard**, not a marker poster headline.
- **Sparse 16:9 component spacing** that exposes empty grid gutters.
- Bottom chain as **perfect bordered capsule strip** + thin text arrows + Soft-UI navy bubble (missing organic blob/cloud chain language).
- Any result that could be mistaken for a clean Soft UI / modern textbook App screen (style-guide hard fail).

---

## Image-gen prompt anchors (short)

`hand-drawn studygram poster, cream watercolor paper grain NO dot grid, pale yellow core-word hub with soft imperfect outline, thick wobbly navy marker arrows, macaron pastel cards with thin sketchy borders and soft wash title pills, outlined chibi character scene stickers, NO soft-UI shadows, organic paint-blob knowledge chain at bottom, high-energy handwritten Chinese title, dense packed notebook layout`

**Negative:** `soft UI, neumorphism, perfect geometric borders, hard drop shadow stickers, dot grid planner background, flat lineless icon beans, dashboard cards, thin vector spokes, sterile white UI`


## 已并入主 prompt（v1.2）

上方 Image-gen prompt anchors 已复制进 `templates/infographic-prompt.md` 正文，成图时不必再翻本文件；本文件仍作翻车对照。
