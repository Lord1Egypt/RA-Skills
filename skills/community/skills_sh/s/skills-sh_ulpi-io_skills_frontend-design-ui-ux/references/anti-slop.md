# Anti-AI-Slop Reference

Use this when committing to a direction (Step 2), locking the design language (Step 3), and running
the Pre-Flight gate (Step 6). These are the patterns that make a design instantly readable as "AI
generated." Ban them by default. A banned item is allowed ONLY if the brief explicitly asks for it
AND `DESIGN.md` justifies it.

## The slop test (apply at every gate)

> Could someone look at this and say "an AI made that" with no doubt? Then it failed.

Two passes:

- **First-order** — does it look generic for ANY product? (templated, characterless)
- **Second-order** — does it look like the generic LLM answer for THIS category? The category must not
  predict the aesthetic (a fintech app need not be blue; a creative brief need not be a serif).

## Aesthetic-direction menu (commit to ONE)

editorial / magazine · Swiss / grid · brutalist / raw · luxury / refined · playful / toy · technical /
utilitarian · organic / natural · maximalist · soft / pastel · industrial / signage · retro-futuristic.
Pick one and justify it from the brief. Bold-and-specific beats safe-and-averaged.

## Pattern vocabulary — reach past the default

When a layout reflex appears, pick a less-obvious pattern that still fits the brief. Concrete options
(not mandates), to give specific alternatives instead of the generic answer:

- **Hero:** split-asymmetric · full-bleed type · editorial cover · product-in-context · oversized
  numerals · horizontal-scroll intro. (Not centered-over-dark-mesh by default.)
- **Nav:** minimal top bar · sidebar rail · sticky contextual · command-palette-first · anchored section nav.
- **Sections:** 2-col zigzag · asymmetric grid · horizontal scroll · bento grid · ruled editorial
  columns · full-bleed alternating. (Not 3 equal cards.)
- **Cards / data:** list with dividers · table-first · stat strip · comparison matrix. Use cards only
  when elevation communicates real hierarchy; never nest them.
- **Motion:** one orchestrated page-load reveal · scroll-linked sticky stack · motivated hover changes.

Vary the pattern family across a long page — at least a few distinct families, never one block repeated.

## Fonts — banned as reflex defaults

- **Reflex "safe" defaults** as the PRIMARY face: Inter, Roboto, Arial, Helvetica, system-ui.
- **Reflex "characterful" defaults** (the model's go-to for "personality"): Fraunces, Playfair Display,
  Cormorant, Instrument Serif, Space Grotesk.
- Rule: pick type from the subject and **pair on a contrast axis** (serif+sans, geometric+humanist) or
  one family in multiple weights. "Creative brief ⇒ serif" is itself a tell — justify any serif.
- Reach-further pool (examples, not mandates): Geist, Satoshi, Neue Montreal, General Sans, Cabinet
  Grotesk, a characterful display paired with a quiet body and a utility/mono for data.

## Color — banned clichés

- The "AI purple/blue" glow and purple→blue gradients (the #1 tell).
- Cream / sand / beige default body backgrounds (`#F4F1EA` family). Token names like `--paper`,
  `--cream`, `--sand`, `--bone`, `--linen`, `--parchment` are tells in themselves.
- Gradient text as a shortcut for "premium."
- Single acid-green / vermilion accent on near-black as a reflex "bold" move.
- Rule: derive the palette per brief (`design-tokens-template.md`) — OKLCH, tinted neutrals, 60-30-10.

## Layout — banned patterns

- Three equal feature cards in a row → use a 2-col zigzag, asymmetric grid, or horizontal scroll.
- Centered hero over a dark mesh/gradient as the default hero.
- Left-text / right-image hero as the FIRST instinct (allowed, never the default).
- Nested cards (a card inside a card) — always wrong.
- Generic glassmorphism on everything.
- Eyebrow kickers + numbered section markers (`01 / 02 / 03`) unless the content truly is a sequence.
- Decorative status dots, fake "trusted by" rows, version labels in the hero, div-built fake screenshots.

## Copy — banned tells (copy is design)

- Buzzwords: elevate, unleash, seamless, next-gen, transformative, revolutionize, powerful solution.
- Fake names: John Doe, Jane Doe, Acme, Nexus, NovaCore, Flowbit.
- Fake-precise filler numbers: `99.99%`, `10x`, `50%` with no source — use specific real-feeling values or none.
- The **em-dash (—)** as a stylistic crutch — the single most common copy tell. Use a period or restructure.
- Rule: write from the user's side; keep action vocabulary consistent through a flow ("Publish" → "Published").

## Motion — banned

- Bounce / elastic easing as a default.
- Scattered infinite micro-animations everywhere.
- Motion with no reason. **Motion must be motivated** — if you can't state why in one sentence, cut it.
- Prefer one orchestrated moment (a staggered page-load reveal) over many small effects. Honor `prefers-reduced-motion`.

## When a reference uses a banned tell

Inspiration links (`inspiration-intake.md`) may use these. Do NOT inherit them. Take the DNA, drop the slop.
