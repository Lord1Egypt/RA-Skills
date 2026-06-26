# Deconstruction Example · Video (founder-story type)

> This is an illustrative example showing what a complete video deconstruction card looks like. The brand and figures below are **fictional** — used purely to teach the format. Real deconstructions should reference verifiable XHS data via `extract_xhs.py`.
> Used to demo: deconstruction granularity for founder-story videos, how to write voiceover logic analysis, when to trigger graph writebacks.

---

# AIC-EXAMPLE-001 | 75-born woman opens 2000 m² heritage store in {City}

> Reference link: (illustrative — not a live URL)
> Deconstructed at: 2026-04-26 18:30
> Platform: Xiaohongshu
> Content type: video

## Metadata
- **Author**: {Brand} (@brand-handle)
- **Published**: 2026-XX-XX
- **Engagement**: 👍 N ｜ ⭐ N ｜ 💬 N ｜ 📤 N
- **note_id**: `{example-id}`

---

## I. Positioning

### 1. Content goal
Founder/store-personality video — build founder credibility / drive store visits

### 2. Target audience
30-45 y/o experienced women drawn to heritage aesthetics. Long decision cycles, value materials and ethos, easily moved by founder stories.
> If brand-aware mode: cross-reference `[[graph/audience/segments]]` segment A (independent aesthetic-driven women)

### 3. Viral theme
Uses a 75-born female founder's "25-year focus + 2000 m² flagship" contrast to convey reverence for traditional craft and uncompromising quality, anchoring brand trust.

---

## II. Deconstruction

### 4. Reference content deconstruction

```
0-2s ｜ Shot: medium
Visual: woman in heritage outfit and straw hat (founder "M") in spacious store, examining garments on rack. Refined interior with multiple heritage pieces displayed.
Camera: locked, soft natural light
Voiceover: "I have an unusual boss, named M."

3-7s ｜ Shot: medium / close
Visual: founder organizing items in different zones, more interior visible.
On-screen text: "Born in '77" "Opened a 2000 m² store in {neighborhood}" "heritage womenswear"
Voiceover: "Born in '77, but she opened a 2000 m² heritage life store in {neighborhood}."

8-14s ｜ Shot: close / extreme
Visual: founder in conversation with team or customer, hand gestures showing fabric and craftsmanship details.
On-screen text: "Make a piece that gives you presence" "clothes that last through time"
Voiceover: "I asked her why heritage. She said she wants to make clothes that give Chinese women presence — clothes that last."

15-24s ｜ Shot: close
Visual: founder personally inspects fabric, organizes display.
On-screen text: "From the weight of {fabric A}" "the texture of {fabric B} to every curve of the cut, she misses nothing" "personally vets samples, personally checks quality"
Voiceover: "From the weight of {fabric A}, the texture of {fabric B}, to every curve of the cut, she misses nothing — personally vets every sample, personally checks every piece."

25-34s ｜ Shot: wide / close
Visual: founder walking through store, touching fabrics, adjusting display.
On-screen text: "Open just two months" "she still walks the store every day" "looking, touching fabrics, adjusting displays"
Voiceover: "Open just two months, but she still walks the store every day — looking, touching fabrics, adjusting displays."

35-39s ｜ Shot: close / medium
Visual: founder talking with team, smiling. Ends on her back as she walks away.
On-screen text: "Get the details right, get the quality real" "to honor every trust"
Voiceover: "She says only by getting the details right and the quality real can she honor every trust — and her own 25 years dedicated to clothing."
```

### 5. Style tags
`Heritage-modern` `Founder-story` `Working-state` `Brand-values`
> Hits in `[[graph/engine/style-tags]]`: Heritage-modern, Craftsmanship, Restrained
> New tags this run: "Working-state", "Brand-values" (queue for Step 6 writeback)

### 6. Scene tags
`Store interior / heritage rack / founder in working scenes`

### 7. Emotion hook
**Core emotion**: Contrast｜Age × Achievement

**Evidence**: First 12 seconds drop two numbers — "75-born" + "2000 m²". The age/scale contrast creates an "unexpected" framing that hooks curiosity. Mid-section pivots to "craftsmanship focus" to build trust. Ending elevates to "25-year dedication" for emotional landing.

> Hits `[[graph/engine/hooks]]` "Contrast｜Age × Achievement" — this case is a high-quality verification of that pattern.

### 8. Comment keywords

> Source: `comments.json`, agent classifies semantically (no regex), each entry has raw-text evidence.

- **Asking contact / hours** (2 raw comments: "do you have a phone number, are you still open?" "your clothes look great, definitely visiting") — high-intent in-store inquiry, signal that founder-video has activated conversion intent
- **Aspirational expression** (1 raw comment: "definitely visiting") — user actively expressing intent to visit, signals brand values landed

> Overall: 3 of 4 comments are pre-conversion signals (contact / hours / store-visit intent). Founder credibility built successfully — no slogan-style CTA needed.

---

## III. Copy

### 9. Reference voiceover

```
I have an unusual boss, named M.

Born in '77, but she opened a 2000 m² heritage life store in {neighborhood}.

I asked her why heritage. She said she wants to make clothes that give
Chinese women presence — clothes that last.

From the weight of {fabric A}, the texture of {fabric B}, to every curve
of the cut, she misses nothing — personally vets every sample, personally
checks every piece.

Clothes follow people. They have to be comfortable, they have to feel right.

Open just two months, but she still walks the store every day — looking,
touching fabrics, adjusting displays.

She says only by being in the store can she really hear what women need.

She believes — get the details right, get the quality real — and you'll
honor every trust, and your own 25 years dedicated to clothing.
```

### 10. Reference voiceover logic analysis

**Layer 1 · Establish contrast and curiosity (0-12s)**
The opening throws two key numbers: "75-born" and "2000 m²". The age-vs-scale contrast immediately creates an "unusual founder" frame. This hook triggers curiosity — viewers want to know who this M person is and how she did this.

**Layer 2 · Convey craftsmanship and value (12-28s)**
After the curiosity hook, copy reveals the answer. "Wants to make clothes that give Chinese women presence" + "personally vets samples" details build a focused, professional craftsperson image. Conveys product core value — not just clothes, but quality, expertise, and care for women — building trust.

**Layer 3 · Land emotional resonance (28s-end)**
Rises from product to emotion. "Only by being in the store can she really hear what women need" lands the brand's "user-centered" ethos. This emotional connection lets target audience (independent, experienced women) move from "approving the product" to "identifying with the brand culture", completing the narrative elevation.

**Key design choices**:
- Contrast number opener — captures attention in 3 seconds
- Numbers + craft nouns ({fabric A} / {fabric B} / cut) — turns "craftsmanship" from adjective into verifiable detail
- Time anchor ("25 years") — turns "expertise" from claim into fact

### 11. Reference cover copy
`75-born woman opens 2000 m² heritage womenswear store in {neighborhood}`

### 12. Reference title
`Open a heritage flagship in {neighborhood} to serve`

### 13. Reference body copy
Pursuing service and expertise, refining true value-for-quality, bringing excellent products to you

### 14. Reference hashtags
`#heritage-flagship #premium-womenswear #downtown-discovery #shopping-trip`

---

## IV. Takeaways (dual-mode comparison — used to teach agents the difference between modes)

> ⚠️ This example **shows both** "objective" and "brand-aware" mode formats side-by-side. Real deconstruction outputs only one, picked by Step 0 graph state.

### Mode B · Objective (graph not populated)

Each bullet: **observation → inference → recommendation** (3 segments):

1. **Numeric contrast is the strongest hook in the first 3 seconds** (observation: this video uses 75-born + 2000 m² double-numbers) → (inference: specific numbers — age/scale/duration/identity — create contrast more attention-grabbing than adjectives) → (recommendation: founder-videos should embed at least 1 specific numeric contrast in first 3 seconds)
2. **Craftsmanship needs craft-noun carriers** (observation: this video uses "weight of {fabric A}, texture of {fabric B}, curve of cut") → (inference: physical nouns are 10x more credible than adjectives) → (recommendation: every "premium" claim should be replaced with 1-2 specific material/craft words)
3. **Emotional elevation belongs in the last 5 seconds** (observation: "honor 25 years dedication" lands in final 4 seconds) → (inference: build trust first, then land on "for whom we make this" to activate resonance) → (recommendation: elevation lines can't sit in the middle — must be in the last 1/8 of duration)
4. **Founder videos don't need slogan-style CTAs** (observation: comments organically include "phone number" and "definitely visiting") → (inference: when founder credibility is built, conversion comes naturally) → (recommendation: drop slogan CTAs; let the ending breathe with negative space)

### Mode A · Brand-aware (graph populated, illustrative configuration)

> Assumes `graph/brand/brand-story.md` contains specific founder background (e.g., "{N} years in {industry} / cross-disciplinary experience / N+ user-acquisition track record"); `graph/audience/segments.md` defines primary segment ("Segment A · 35+ aesthetics-driven independent women").

1. **Founder's "numeric contrast" can be reused directly** — when making our own founder video, open with "hard number + contrast identity" (e.g., "{N} years in {industry}, first cross-disciplinary venture in {Y}: {Z} result"), structurally analogous to M's 75-born × 2000 m²
2. **Category-specific "craft nouns" can substitute for {fabric A}/{fabric B}** — replace abstract adjectives with specific materials / processes / methodologies for our category (jewelry: "heritage gold / brushed metal / openwork"; software: "pipeline / nodes / orchestration")
3. **Segment A doesn't want promo CTAs — wants "trust completion"** — pinned comment should carry "craft / data / case studies" instead of "rush / limited"
4. **Reusable founder-video formula**: open 3s with hard-number contrast → middle shows specific methods/craft → end with "for whom" (one-sentence mission, anchoring brand-voice value-keywords)

---

**Root difference between modes**:
- **Objective mode** outputs "general methodology" — useful as a content-planning playbook
- **Brand-aware mode** outputs "an immediately executable next-content brief" — directly feeds into generate mode

The ROI of filling the graph is visible right here.

---

## Graph writeback log

This deconstruction triggers the following graph updates:

1. ✅ `graph/engine/hooks.md` "Contrast｜Age × Achievement" gets first-evidence supplement: source AIC-EXAMPLE-001
2. ✅ `graph/engine/style-tags.md` adds two new tags: "Working-state", "Brand-values"
3. ⚠️ Pending human review: should `graph/platforms/xiaohongshu.md` add a new "Founder + working-state" persona-video formula?
