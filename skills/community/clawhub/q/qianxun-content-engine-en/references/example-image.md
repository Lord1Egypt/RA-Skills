# Deconstruction Example · Image post (jewelry recommendation)

> Illustrative example with **fictional brand and content** — used to teach the format. Real deconstructions should reference verifiable XHS data via `extract_xhs.py`.
> Used to demo: image-by-image deconstruction granularity, cultural-meaning hook analysis.

---

# AIC-EXAMPLE-002 | Vintage wisteria earrings (heritage gold jewelry post)

> Reference link: (illustrative — not a live URL)
> Deconstructed at: 2026-04-26 18:35
> Platform: Xiaohongshu
> Content type: image (image post)

## Metadata
- **Author**: {Heritage Goldsmith Brand}
- **Published**: 2026-XX-XX
- **Engagement**: 👍 N ｜ ⭐ N ｜ 💬 N ｜ 📤 N
- **note_id**: `{example-id}`

---

## I. Positioning

### 1. Content goal
Jewelry recommendation + cultural narrative

### 2. Target audience
Women drawn to vintage / heritage aesthetics, valuing cultural meaning and craft details. Long decision cycles, weight gold weight and craftsmanship, less concerned with "trends".
> Cross-reference `[[graph/audience/segments]]` (TBD: cultural-aesthetic jewelry consumer)

### 3. Viral theme
Uses "wisteria flower" as inspiration, fusing seasonal landscape with vintage-era romance to package a pair of gold earrings as "softness and grace settled from old time" — adds cultural depth rather than purely showing craft.

---

## II. Deconstruction

### 4. Reference content deconstruction

```
Image 0 (shoot setup explanation):
- Scene: outdoor courtyard or interior with heritage architecture elements (wooden door, lattice window, white walls)
- Props: aged wooden table, open thread-bound book or scroll as static base
- Lighting: soft side or rim light to highlight gold texture and brushed pattern, with shadow contrast

Image 1 (cover · static product show · wide):
- Composition: slight overhead, sharp focus on earrings
- Elements: open palm as stable visual plane, earrings centered
- Style: deep wood-grain background, blurred via shallow depth-of-field, side-back light creates rim around hand and earrings
- Role: typical static product shot — hand presence adds warmth and story over plain table placement

Image 2 (static product show · close-up):
- Composition: earrings at visual center
- Elements: hand as scale reference
- Style: background fully blurred to dark
- Role: from wide to close-up — let viewer "see clearly". Emphasizes craft details and material weight

Image 3 (worn show · portrait):
- Composition: only crop ear and partial side profile (typical Eastern aesthetic "negative space")
- Elements: model's posture natural and quiet, soft light on face and earrings
- Style: earrings are absolute visual focus
- Role: shifts from "object" to "person" — shows product-with-person relationship. Core is "atmosphere" and "imagination space"

Image 4 (symmetric hand composition):
- Composition: strict symmetry, hands hold earring pair on each side, mirror relationship
- Elements: tassel motion shown in even light
- Style: ceremonial, formal aesthetic
- Role: pure aesthetic shot — pursuing formal harmony
```

### 5. Style tags
`Heritage-modern` `Vintage-era` `Heritage-gold` `Original-design` `Vintage-romantic` `Literary`
> All in `[[graph/engine/style-tags]]` dictionary, no new tags

### 6. Scene tags
`Solid-dark backdrop / heritage wooden lattice / courtyard`

### 7. Emotion hook
**Core emotion**: Cultural + Aspiration

**Evidence**: Uses "wisteria flower" as cultural symbol, elevating "a pair of gold earrings" into "grace from a vintage-era courtyard". Cultural anchors (wisteria, heritage place, vintage era) attach "cultural identity" to wearing the product, evoking "I want to become this kind of person" rather than pure "I want to buy".

> Cross-references `[[graph/engine/hooks]]` "Cultural｜Symbolic meaning" — this case is high-quality verification of that pattern.

### 8. Comment keywords

> Source: `comments.json`, agent classifies semantically (no regex), each entry has raw-text evidence.
> Note: this example's comment data is illustrative (drawn from historical deconstruction notes), not live API data — for format reference only.

- **Asking price / weight / craft fee** (4 raw comments: "how much for this one" "what's the gold weight" "how is the craft fee calculated" "how much for the diamond") — high-AOV decision path; standard inquiry chain for jewelry buyers
- **Asking for physical store** (1 raw comment: "where's the physical store") — strong demand for gold-category: want to see materials in person + verify authenticity

> Overall: all comments are pre-conversion inquiries (no complaints), proving copy + visual hook landed; only missing piece is the purchase path. Recommendation: pin comment with weight / craft-fee / store-address trio.

---

## III. Copy

### 9. Reference voiceover
N/A (image post)

### 10. Reference voiceover logic analysis
N/A (image post) — see body copy logic in "Takeaways" below

### 11. Reference cover copy
No explicit cover text (cover relies on image visual itself)

### 12. Reference title
`Vintage-era wisteria-dream earrings`

### 13. Reference body copy
```
Wisteria sash and curtain, wind carries softened fragrance

Every spring, I want to record this lush season in {city}
Spring at the old gate, wisteria like a dream, draped over the eaves
As if walking through a series of ancient paintings

This pair of gold earrings is designed around wisteria
Tiny wisteria blossoms bloom at center
Surrounded by a circle of vine flowers on each side
Every petal hand-brushed with detailed lines
Light tassels gently sway below

Like softness and bone settled from old time
Carrying the grace of a {city} courtyard from the vintage era
Now held within the few inches of an ear
```

### 14. Reference hashtags
`#heritage-jewelry #original-design #boutique-design-earrings #gold-earrings #heritage-gold #vintage-era`

---

## IV. Takeaways

1. **Image-post "cover image = title"**: this post has no text cover — the first image itself is the hook (hand + earring + dark backdrop), carrying its own information. If your product visuals are strong enough, you can skip the big-text cover.
2. **Cultural anchors land deeper than USP**: zero mention of price, weight, or buying points across the entire post — all about "wisteria" "city" "vintage-era" "old time". Build "I want to become this kind of person" aspiration first; purchase decision follows naturally.
3. **Poetic open + prose-style body**: "Wisteria sash and curtain, wind carries softened fragrance" sets the tone first, switching reader from scroll-mode to read-mode. The rest is pace-easy prose, matching product tonality.
4. **4-image structure for jewelry posts**: wide → close-up (see craft) → portrait (build aspiration) → symmetric (formal aesthetic). Stable structure for "recommendation-style jewelry image posts" — reusable.
5. **High-intent comments don't come from "rush", they come from "cultural resonance + physical assurance"**: comments asking "price / weight / store" indicate users were moved by culture and now lack only "trust completion". CTA shouldn't be "rush" — it should be "address + hours + craft credentials".

---

## Graph writeback log

This deconstruction triggers the following graph updates:

1. ✅ `graph/engine/hooks.md` "Cultural｜Symbolic meaning" gets evidence: source AIC-EXAMPLE-002
2. ✅ `graph/platforms/xiaohongshu.md` "Image-post 4-frame formula" appended to platform formulas section
3. ⚠️ Pending human review: should `[[graph/audience/segments]]` add a "cultural-aesthetic jewelry consumer" segment?
