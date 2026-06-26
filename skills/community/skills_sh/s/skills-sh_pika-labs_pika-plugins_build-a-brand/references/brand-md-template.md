# brand.md — Template Reference

This template defines the structure of the `brand.md` file delivered in Step 5's brand kit zip. It's a comprehensive, machine-readable brand spec that lets users (or downstream AI tools) produce on-brand work without needing the 15-page guidelines PDF.

## Why this format

`brand.md` is the brand's portable form. Paste it into Claude, GPT, or any LLM along with a task ("write a launch tweet," "design a landing page hero," "draft an email") and the AI can produce on-brand output without the user manually re-explaining the brand. The format is intentionally:
- **Scannable at the top** (Quick Reference block) so an AI doesn't have to read 200 lines before producing something.
- **Detailed below** so the AI can dig in when a task needs more specificity.
- **Markdown** so it renders in GitHub, Notion, Cursor, Claude artifacts, etc.

## Required sections (in this order)

1. Title + one-line description
2. Quick Reference (scannable top block)
3. Positioning
4. Target Customer
5. Mission
6. Values
7. Story (why we exist)
8. Voice & Tone
9. Colors
10. Typography
11. Logo
12. Icons
13. Imagery (Photography and/or Illustration)
14. Visual World
15. Touchpoints
16. Do & Don't
17. Reference Brands
18. Design Tokens (pointer to /tokens/ files)
19. AI Prompts (pointer to /prompts/ files)
20. How to Use This Spec

## Template

```markdown
# [Brand Name] — Brand Guide

> A complete brand spec. Paste this into Claude, GPT, or any AI tool along with a task to produce on-brand work. Or hand it to a designer or developer.

---

## Quick Reference

- **Name:** [Brand Name]
- **Tagline:** [Tagline]
- **One-line positioning:** [Positioning statement]
- **Primary color:** [Name] `#HEX`
- **Display font:** [Font name] (Google Fonts: [URL])
- **Body font:** [Font name] (Google Fonts: [URL])
- **Voice:** [3-4 adjectives separated by commas]
- **Logo symbol:** [One-line description — e.g. "outlined Δ delta with horizontal bar"]

---

## Positioning

[Positioning statement as a single declarative sentence.]

[1-2 paragraph expansion of what the brand stands for, what's different about it, what the wedge is.]

---

## Target Customer

[Customer name (real or representative), age, role.]

[2-3 sentence vivid description of who they are, what they care about, why they buy. Specific not demographic.]

---

## Mission

[Mission as a single sentence — the thing the brand exists to do.]

---

## Values

1. **[Value 1]** — [one-line explanation]
2. **[Value 2]** — [one-line explanation]
3. **[Value 3]** — [one-line explanation]
4. **[Value 4]** — [one-line explanation]
5. **[Value 5]** — [one-line explanation]

---

## Story — Why We Exist

[2-3 paragraphs of the brand's origin/why story, written in brand voice. This is the "about us" content — it should be real copy, ready to paste into a website.]

---

## Voice & Tone

**Adjectives:** [4 tone adjectives, comma-separated]

**How we sound:**
[1-2 sentences describing the voice.]

**Copy examples by context:**

| Context | Example |
|---|---|
| Headline | [Real example in brand voice] |
| Sub-headline | [Real example] |
| CTA button | [Real example — short, specific] |
| Error state | [Real example — warm not robotic] |
| Footer line | [Real example] |
| Social post | [Real example] |

**Words we never use:**
[Comma-separated list of forbidden words — usually marketing clichés the brand specifically avoids.]

---

## Colors

| Name | Hex | RGB | CMYK | Pantone | Role |
|---|---|---|---|---|---|
| [Name] | #HEXVAL | R, G, B | C, M, Y, K | XXX C | Primary |
| [Name] | #HEXVAL | R, G, B | C, M, Y, K | XXX C | Background |
| [Name] | #HEXVAL | R, G, B | C, M, Y, K | XXX C | Text |
| [Name] | #HEXVAL | R, G, B | C, M, Y, K | XXX C | Depth / accent |

**Primary pairings:** [Which colors go with which — e.g. "Primary on Background is the default; Primary on Text is for emphasis blocks."]

**Never:** [Color combos to avoid — e.g. "Never pair Primary with cool blues. Never tint Background gray."]

---

## Typography

**Display:** [Font name + weight], used for hero headlines at [size range]. [One-sentence note on its character.]
- Google Fonts: [URL]

**Body:** [Font name + weight], used for paragraph text at [size range].
- Google Fonts: [URL]

**Hierarchy:**

| Level | Font | Weight | Size | Line-height |
|---|---|---|---|---|
| Display | [Font] | [Weight] | 124–168px | 0.85–0.92 |
| H1 | [Font] | [Weight] | 64–72px | 0.92–0.95 |
| H2 | [Font] | [Weight] | 38–42px | 1.05–1.1 |
| H3 | [Font] | [Weight] | 22–24px | 1.15–1.2 |
| Body | [Font] | [Weight] | 16px | 1.45–1.55 |
| Caption | [Font] | [Weight] | 11px | 1.4, letter-spacing 0.28em uppercase |

**Pairing rules:** [Brief note — e.g. "Display font carries the brand. Body font supports it. Never use the display font for body or vice versa."]

---

## Logo

### Wordmark

[Description of the wordmark — typeface, treatment, custom touches, what it feels like.]

Files (in `logo/wordmark/`):
- `wordmark-[primary].svg/.png/.pdf` — for use on background color
- `wordmark-on-dark.svg/.png/.pdf` — for use on dark backgrounds
- [etc — list all variants]

### Symbol

[Description of the symbol/mark — shape, what it evokes, how it relates to the brand metaphor.]

Files (in `logo/symbol/`):
- `symbol-[primary].svg/.png/.pdf` — primary color on transparent
- `symbol-on-dark.svg/.png/.pdf` — reversed for dark backgrounds
- [etc]

### Lockup

[Description of how wordmark + symbol combine. Primary lockup (stacked or horizontal). Secondary lockups. When to use each.]

Files (in `logo/lockup/horizontal/` and `logo/lockup/stacked/`):
- [List variants]

**Clear space rule:** [Minimum space around the lockup — e.g. "Minimum one symbol-height of space on all sides."]

**Don'ts:** Don't stretch, rotate, recolor outside the palette, drop-shadow, or place on busy backgrounds.

---

## Icons

**Stroke weight:** [e.g. 1.5px / 2px / 3px]
**Corner radius:** [sharp / 2px / round]
**Line caps:** [butt / round / square]
**Style:** [outline / filled / mixed]
**Grid:** 24×24 base

**Set in this kit** (`/icons/`):
- arrow-right, arrow-down, check, close, plus, minus, search, user, settings, bell, menu, info
- [+ any brand-specific icons]

**For icons beyond this set:** Use [library name + weight] — e.g. "Phosphor Light" or "Lucide at 1.5px stroke."

Each icon SVG uses `stroke="currentColor"` so it adopts the surrounding text color in any application context.

---

## Imagery

Use this section's photography-OR-illustration block depending on the brand's medium. Delete whichever doesn't apply, or keep both if the brand is hybrid.

### Photography (if brand uses photography)

**Subject:** [Who/what is in the frame.]

**Light:** [Lighting style — direction, quality, time of day.]

**Color:** [Color grade direction.]

**Texture:** [Film, grain, composition guidance.]

**Forbidden:** [What this brand's photography never looks like — stock, studio, etc.]

**Cast diversity:** All lifestyle images featuring people must show racial diversity across the set. Vary body types. Default to mixed cast unless there's a deliberate reason for a single subject.

### Illustration (if brand uses illustration)

**Style:** [Flat vector / line art / geometric / 3D / hand-drawn / mixed. Be specific.]

**Color use:** [How brand colors apply — large fields vs accent dots, palette restraint per illustration.]

**Line / stroke:** [Stroke weight, corner radius, line caps. Or "no strokes, color fields only."]

**Character:** [Friendly / precise / playful / archival / geometric / organic. Match brand voice.]

**Composition:** [Asymmetric / centered, whitespace approach, framing rules.]

**Subject matter:** [What illustrations depict — scenes, objects, metaphors. Tied to the brand metaphor.]

**Forbidden:** [What kills the style — realistic detail in flat-vector brand, gradients, drop shadows, generic stock-illustration look, etc.]

**Reference brands' illustration style:** [2-3 brands whose illustration is close.]

---

## Visual World

[2-3 sentence description of the world the brand's imagery lives in — environments, time of day, mood, characters. Should paint a picture someone could art-direct a shoot from.]

---

## Touchpoints

The brand shows up on these surfaces. Each follows the rules above.

- **Web** — [hero treatment, color usage, typography rules]
- **Mobile app** — [UI palette and rules]
- **Social** — [tone, asset rules, posting cadence]
- **Print collateral** — [business cards, packaging, etc.]
- **Merch** — [stickers, mugs, totes, apparel]

---

## Do & Don't

**DO:**
- [Brand-specific do #1]
- [Brand-specific do #2]
- [Brand-specific do #3]
- [Brand-specific do #4]
- [Brand-specific do #5]

**DON'T:**
- [Brand-specific don't #1]
- [Brand-specific don't #2]
- [Brand-specific don't #3]
- [Brand-specific don't #4]
- [Brand-specific don't #5]

---

## Reference Brands

These brands share the territory. They're not competitors — they're cultural reference points the brand can borrow energy from.

- **[Brand]** — Borrow: [what to learn from them]
- **[Brand]** — Borrow: [what to learn from them]
- **[Brand]** — Borrow: [what to learn from them]
- **[Brand]** — Borrow: [what to learn from them]

---

## Design Tokens

Machine-readable versions of all visual tokens (colors, fonts, spacing, radius, shadow) live in the `/tokens/` directory:

- **`tokens/tokens.css`** — CSS custom properties. Drop the `:root { ... }` block into your stylesheet and reference as `var(--color-primary)`, `var(--font-display)`, etc.
- **`tokens/tokens.json`** — same content as JSON. Useful for AI tools, build pipelines, or any non-CSS context.
- **`tokens/tailwind.config.snippet.js`** — paste inside your `tailwind.config.js` `theme.extend` block. All brand tokens become Tailwind classes (`bg-primary`, `text-text`, `font-display`, `rounded-lg`, etc).

The token names match this spec — don't rename them or they'll fall out of sync with the rest of the brand documentation.

---

## AI Prompts

Pre-built prompts for common downstream tasks live in `/prompts/`:

**Copy prompts:**
- **`prompts/system-prompt.md`** — paste at the top of any Claude or GPT thread to prime the model on this brand's voice + visual identity. Then add your task below.
- **`prompts/tweet.md`** — task starter for writing tweets in brand voice
- **`prompts/landing-hero.md`** — task starter for landing page hero copy (headline + sub + CTA)
- **`prompts/email.md`** — task starter for marketing or transactional emails
- **`prompts/error-message.md`** — task starter for writing warm-but-specific error/empty/loading states

**Image prompts:**
- **`prompts/photography.md`** — task starter for generating brand photography via gpt-image-2 (or similar). Includes the brand's exact photo direction (subject / light / cast / texture), banned cliché concepts list, anti-stock guardrails, the no-text safeguard string, and subject substitutes for "person at laptop" defaults.
- **`prompts/illustration.md`** — *(only present if the brand uses illustration)* — task starter for generating brand illustrations. Includes the brand's illustration style rules, palette constraints, banned elements (gradients, drop shadows, etc.), and when to use illustration vs photography.

These prompts encode the brand voice rules from this spec into instructions the model will follow. Use them when you want consistent on-brand output without re-explaining the brand each time.

---

## How to Use This Spec

**With an AI tool (Claude, GPT, etc.):**
1. Paste `prompts/system-prompt.md` (or this whole `brand.md`) at the top of a new thread.
2. Add your task — "Write a launch tweet" / "Design a landing page hero" / "Draft an onboarding email."
3. Or use a specific task starter from `/prompts/` for the most consistent output.
4. Verify the output against the Do & Don't section before shipping.

**With a designer:**
- Hand them the `brand.md` + `/logo/` + `/icons/` directories. They have everything they need.

**With a developer:**
- Point them at `/tokens/` first. CSS variables / JSON / Tailwind config — pick whichever matches their stack.
- The icon SVGs in `/icons/` use `currentColor` for stroke so they inherit color from context.

**For self-checks:**
- Before delivering anything in this brand's voice, re-read the "Voice & Tone" section.
- Before delivering anything visual, re-read "Colors," "Typography," "Icons," and "Imagery."
- Always check the Do & Don't list last.

---

*Generated [DATE] by the build-a-brand skill. Update this file when the brand evolves.*
```

## Filling guidelines

- **Quick Reference** must be scannable in 5 seconds. Don't bloat it.
- **Voice copy examples** must be REAL on-brand sentences, not placeholders. Pull from the guidelines PDF's Voice & Tone page.
- **Colors table** needs Pantone if you have it; mark as "—" if not specified.
- **Typography Google Fonts URLs** must be the actual `https://fonts.google.com/specimen/[Name]` link, not the embed URL.
- **Logo file lists** must match exactly what's in the zip. If a variant doesn't exist, don't list it.
- **Reference brands** with "borrow this" notes — the same content as the guidelines page 2.
- **How to Use** — the most important section for downstream usability. Tell the user how to actually apply this spec.

## What NOT to include

- Don't include the full 15-page guidelines verbatim. The brand.md is the SPEC, not the manual. Keep it tight.
- Don't include marketing fluff. Every section should be either directly usable copy or actionable rules.
- Don't include build mechanics (WeasyPrint quirks, prompt templates, etc.). Those are skill-internal.
