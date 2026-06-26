---
name: build-a-brand
description: >
  Build a complete brand identity and guidelines PDF from any input — an idea, an existing
  website, a list of reference brands, product photos, or "I want to rebrand X". Use when
  someone wants a brand identity but does NOT need a full commerce launch (no Shopify, no
  product listings, no social posting).
  Trigger phrases: "build me a brand", "make me a brand", "design a brand identity", "brand
  guidelines for [X]", "i want a brand book", "create a brand from scratch", "brand for [idea]",
  "i want a brand that feels like [X] + [Y]", "rebrand my [thing]", "visual identity for [thing]",
  "build-a-brand".
argument-hint: <idea-or-url-or-reference-brands> [photos=<paths-or-urls>] [refresh=<existing-brand>] [--quick] [--config <path>]
required-capabilities:
  - mcp__pika__generate_image
  - mcp__pika__remove_background
  - mcp__pika__html_to_pdf
  - mcp__pika__html_to_png
  - mcp__pika__analyze_media
  - mcp__pika__task_status
  - mcp__pika__upload_asset
---

# Build a Brand

Take any input — an idea, a website, a list of reference brands, product photos, or an existing brand to refresh — and produce a complete brand identity, ending in a 15-page brand guidelines PDF.

This is a standalone brand-building workflow focused on strategy, identity, design, and copy. Output is **one** brand guidelines PDF for the chosen identity.

## Full Workflow

### Stage 0 — Intake (empty-args menu)

If invoked with no input (no idea, no URL, no photos, no reference brands, and no relevant prior context in the conversation), print this menu verbatim as your full response and stop. Do not call any tool. Wait for the user's next message.

> **What are we branding?** Paste any of:
>
> - **An idea / description** — e.g. "a streetwear label for cat people"
> - **A website URL** — e.g. "rebrand my existing site at example.com"
> - **Product photos** — drop them in the chat
> - **Reference brands** — e.g. "I want something that feels like Aesop + Patagonia"
> - **An existing brand to refresh** — name + what's working / what isn't

If the user already dropped one of the above, skip the menu and proceed straight to Step 1.

### Stage 0.5 — Non-interactive fast lane

Use this path when the caller passes `--quick` or `--config <path>`, or when the
caller states they are running from CI, a subagent, a batch job, or any other
non-interactive harness.

This section has precedence over the interactive ask/wait instructions below.
When it applies, use this fast lane and do not fall through to the multi-turn
intake unless a required input is truly missing.

- `--config <path>` points to a JSON file that pre-bakes intake answers:
  `input`, `photos`, `reference_brands`, `audience`, `positioning`, `assets_to_keep`,
  `references`, `chosen_direction`, `chosen_identity`, and `export_kit`.
- `--quick` means use model judgment for all confirmation gates. Ask only if
  the original input is missing entirely; otherwise infer reasonable defaults,
  choose the strongest strategy direction and identity option, and continue.
- For `--quick` or `--config`, do not stop for confirmation at the deliverable
  preview, strategy-direction choice, identity-option choice, or brand-kit
  export gate. Record the assumption inline, then proceed.
- If a required asset is unavailable and cannot be inferred from the input,
  stop once with a single compact missing-fields list instead of starting a
  multi-turn Q&A loop.
- Do not deliver a condensed or partial brand output just because the caller is
  non-interactive or the run is short on wall-clock time. A condensed 6-page
  deck is not an acceptable substitute for the required 15-page guidelines.
  If the run is out of wall-clock budget, save a resumable checkpoint with the
  pages/assets already completed and stop; do not mark the workflow complete.

### Step 1 — Read the Input

Inputs vary. **Before asking any questions, open with a brief agenda** so the user knows what's coming:

```
here's how this works — 5 steps:
1. **Read the input** — i ask a few questions, you answer, i play back what i'm hearing
2. **Strategy directions** — 2-3 distinct positioning angles to choose from
3. **Identity options** — 3 full brand identities (name, colors, voice, brand board PDF preview) within your chosen direction
4. **Build the guidelines** — full 15-page brand book PDF for the chosen identity
5. **Export the brand kit** — once you're happy with the guidelines, i'll bundle a `brand.md` spec + logo assets (transparent PNG + PDF wrapper for every mark; SVG when vector-authored) in each brand color as a zip you can use anywhere

let's start. [questions follow]
```

Then ask 3-5 targeted questions in a single message. Adapt to the input type:

**If they dropped an idea / description:**
- What does this brand sell or do? (product / service / app / community / something else)
- Who is this for — describe the 2-3 audience segments this brand should serve, plus one vivid anchor persona inside the primary segment
- Why does this exist? what's broken about the alternatives, or what feeling are you trying to deliver?
- Do you have a name in mind, or is naming part of what you want help with?

**If they dropped a website / existing brand URL:**
- Are we refreshing this brand or rebuilding it from scratch?
- What's working about it today, and what isn't?
- Who's the current customer vs. who you wish were the customer?

**If they dropped product photos:**
- Ask how the product is made, who has bought or used it, price point, current sales/channel context, and any direction they already have in mind.
- Keep the output scoped to guidelines and a brand kit, not a commerce launch.

**If they dropped reference brands only ("I want a brand that feels like Aesop + Patagonia"):**
- What's the product, service, or thing this brand will be attached to?
- What about each reference brand specifically do you love? (the photography? the tone? the restraint?)
- Who buys this — describe the 2-3 audience segments this brand should serve, plus one vivid anchor persona inside the primary segment.
- Any constraints? (industry, regulation, location, price tier?)

**Always also ask (regardless of input type):**
- Do you have any existing brand assets you want to keep or incorporate? (Logo, wordmark, symbol, name, colors, fonts, photography, packaging — anything you don't want to lose.)
- Any specific references, inspirations, or moodboards you'd want this to draw from?

These two are essential — they prevent you from generating things the user already has, and they anchor the work in references the user actually likes. Always include them.

Keep it to a single message. Aim for 5-7 questions total (input-specific + the 2 universal), conversational not clinical. Wait for answers before proceeding.

**After answers**, analyze the input + answers together and read back:
- **Aesthetic territory**: what visual world does this live in?
- **Audience segments**: primary segment, secondary segment(s), and one vivid anchor persona inside the primary segment. Do not collapse the audience into one over-specific individual.
- **Positioning**: what's the wedge — what does this stand for that competitors don't?
- **Price tier / category fit**: where on the market shelf does this sit?
- **Story hook**: what's the emotional reason someone cares?
- **Assets being kept**: explicitly list what the user said they want to preserve (existing wordmark, name, colors, etc.)
- **References anchoring the work**: list the user-named inspirations.

**Then preview the deliverable and invite specific guidance** — before moving to brand directions, show the user what'll be in the final guidelines so they can flag anything to add, change, or call out:

```
here's what i'll build into the 15-page brand guidelines:

1. Cover (brand name, tagline, hero mood)
2. Strategy & positioning (primary/secondary audience segments + anchor persona)
3. Brand foundation (mission, values, story)
4. Logo (wordmark + symbol + variants)
5. Logo don'ts
6. Color palette
7. Typography
8. Icons (UI icon system + library guidance)
9. Voice & tone
10. Imagery rules (photography and/or illustration, adapted to brand medium)
11. Visual world / lifestyle imagery
12. Touchpoints (real photos showing the brand in use)
13. Brand applications (mockups: business card, app icon, favicon, etc.)
14. Digital + social
15. Do & don't

plus a brand kit zip at the end with: `brand.md` spec, logo assets (transparent PNG + PDF wrapper for every mark; SVG when vector-authored), design tokens (CSS / JSON / Tailwind), AI prompts (system prompt + task-specific starters), and the icon SVGs.

anything you want to add, change, call out specifically, or want me to handle differently? if not, i'll move on to brand directions.
```

Wait for response. Incorporate any specific user guidance (add a page, swap something, special focus on a particular section, exclude something) before moving to Step 2. This catches scope mismatches early — much cheaper than discovering them after the PDF is built.

### Step 2 — Present 2-3 Brand Directions

Based on your read, present 2-3 distinct brand directions. See `references/brand-directions.md` for structure.

Each direction must be a genuinely different business answer — not aesthetic variations. Differentiate on WHO and WHY, not WHAT.

Ask the user to pick one direction before proceeding.

### Step 3 — Generate 3 Brand Identity Options

Once they choose a direction, generate 3 complete brand identity options within that direction. See `references/brand-identity.md` for structure.

Each option includes: name + tagline, color palette, typography direction, voice & tone, logo concept, brand story, photography direction (product + lifestyle/mood), UI/website direction, example brands.

After presenting all 3 in text, **build a 3-page brand board PDF** (one page per option) so the user can see each identity before committing.

**Each option must include:**
- **Wordmark** in the brand's display font — use the user's existing wordmark if they have one they like; propose a new one if they need a logo or don't like their current one. A new wordmark must have custom letter treatment: adjusted spacing, ligature, cut, terminal, case, underline, or other ownable detail. It is not just a Google Font typed in a color.
- **Symbol/mark** — a standalone graphic that lives without the wordmark. Use the user's existing symbol if they have one they like; propose a new one otherwise. Even if the user keeps their wordmark, propose a symbol if they don't have one — favicons and app icons need a non-typographic mark. For new symbols, default to a generated PNG via `mcp__pika__generate_image` with `provider="gpt-image-2"` when visual quality, texture, detail, or originality matters. Ask for a clean isolated mark on transparent background, no baked-in letters, no watermark, no mockup, centered in a square. After generating, run the PNG through `mcp__pika__remove_background` with `mode="logo"` to guarantee a real transparent background before compositing it onto any colored or photo background — generated symbols often come back with a baked-in white background that becomes a white box at composite time. (Background removal strips only the outer background; design any interior negative space to be open at generation time, since the cleanup pass won't carve it out.) Use inline SVG only if the mark is intentionally simple, can be drawn cleanly by hand, and passes small-size QA. Must work at 16×16 AND 512×512.
- **Seal / badge** — if the option uses a seal, stamp, badge, or monogram, it must be readable and ownable at small and medium sizes. It cannot be a generic circular font lockup, clip-art crest, or low-contrast decorative filler.
- Tagline (8 words max)
- Voice sample with visible "VOICE" label (one quoted sentence, 14 words max)
- Compact board story (~35 words max, min 2 sentences)
- Lifestyle world description with visible "WORLD" label (~22 words max, min 1 full sentence)
- Lifestyle mood image (generated via gpt-image-2)
- 4-color palette with hex + role labels
- Display + body type specimens with named fonts

Brand board pages should look different enough that the user can tell which identity they are seeing before reading the labels. Don't use the same template recolored 3 times; each board's layout should embody the option's design philosophy. A magazine-cover option should look like a magazine cover (full-bleed photo, masthead-style); a soft consumer option should look like a homepage hero (rounded shapes, soft circles for swatches); an editorial option should look like a literary spread (huge italic centered, inset photo). See `references/brand-guidelines.md` "Brand Board Layout — Differentiate per Option" for examples.

If you can't physically tell which brand you're looking at *without* reading the labels — regenerate.

**Page size:** 1200×850px. Renderer: Pika MCP `mcp__pika__html_to_pdf` for PDF output and `mcp__pika__html_to_png` for PNG QA previews. Both use server-side Chromium; do not run local WeasyPrint or Chrome headless by default. The delivered PDF and QA PNGs must come from the MCP render path. If a local/sandbox/browser fallback is used for debugging, discard that output, rerender through MCP, and QA the final MCP PNGs. If the MCP and fallback renders disagree, fix the HTML/CSS; do not ship the fallback render.

**Board quality gate:** the 3-page preview must pass visual QA, not just render QA.

1. Inspect each PNG preview before sending the PDF. Fail ugly density, weak hierarchy, muddy one-note palette, unreadable small text, empty mockup/image slots, clipped text, and body copy or non-masthead text intersecting icons, swatches, seals, photos, phone mockups, or decorative rules. Also inspect the symbol at 16×16 and 512×512; if the small-size read is illegible, muddy, too generic, or collapses into noise, regenerate or simplify before delivery. Website/social/app mockups are optional on brand boards; do not add them unless they contain real content. If included, flat color rectangles count as empty placeholders unless the section is explicitly a palette specimen.
2. Run `mcp__pika__analyze_media` on each board PNG using the exact PASS/FAIL prompt in `references/brand-guidelines.md` "Full-Deck Visual QA" — its low-contrast clause is load-bearing (without it the model rates low-contrast text "legible" and PASSes a real defect). Ask about all issues listed above in addition to that prompt's checks. Masthead wordmark/tagline/issue metadata overlays on photos are allowed only when they use deliberate negative space or a contrast scrim and pass contrast QA as defined in `references/brand-guidelines.md` Rule 5. Body copy on images is still forbidden.
3. Handle tool state before interpreting the result. If `mcp__pika__analyze_media` returns `{task_id, status: "running"}`, poll `mcp__pika__task_status({task_id})` until terminal. Treat the QA as unavailable and halt with a manual-review warning if the tool is missing, raises `tool_not_found`, `provider_unavailable`, `unsupported_media_type`, `rate_limited`, `quota_exceeded`, `auth_error`, any HTTP 4xx/5xx error envelope, or a transport error, says it cannot analyze the image, or returns final text that does not match ``/^\s*[`*]{0,2}(PASS|FAIL)\b/``.
4. Interpret the result with that regex only. Fix every captured FAIL before delivery. If the captured result is PASS but the explanation lists a blocking collision, clipping, unreadable text, or missing required board content, treat it as FAIL. Do not proceed silently.

**Font rule:** fresh fonts per brand AND fonts must have character. Never default to Inter / Karla / Outfit / DM Sans / Lato — they have no point of view as a display face. Explore the full Google Fonts library. See `references/brand-guidelines.md` "Must Have Character — Don't Default to Safe Fonts" for approved high-character options by vibe (Fraunces, Instrument Serif, Bricolage Grotesque, Funnel Display, Bodoni Moda, Reddit Mono, etc.). For MCP rendering, use HTTPS font URLs or inline `data:font/...` sources; local `file://` font paths are not available server-side.

Do not build the full 15-page guidelines PDF until the user picks an option — that wastes time on rejected identities.

Present all 3 clearly. Ask the user to pick one, or mix elements from different options.

### Step 4 — Build the Full Brand Guidelines PDF

Once user confirms an identity, build the 15-page brand guidelines PDF.

**Page structure (15 pages; becomes 16 if hybrid imagery split):**

1. **Cover** — Brand name, tagline, hero mood image. Full-bleed.
2. **Strategy & Positioning** — Direction name. Positioning statement (one punchy sentence). Target audience system: primary segment, secondary segment(s), and one vivid anchor persona inside the primary segment. Do not describe only one over-specific customer. 3-4 reference brands with "borrow this" notes.
3. **Brand Foundation** — Mission. Brand values (3-5). The "why this exists" story (2-3 paragraphs of real copy in brand voice — not a template).
4. **Logo** — Primary mark + all variants (horizontal, icon-only, reversed), usage rules (on dark / on light / on color), logo mark explanation, clear space rule.
5. **Logo Don'ts** — Explicit misuse rendered in CSS: never stretch, never rotate, never wrong background, never recolor, never use drop shadow. Show each violation visually with a ✗ label.
6. **Color** — All swatches with hex + RGB + CMYK, primary pairings, accessibility/contrast note, never-do combinations. Full-bleed color columns, not swatches floating on white.
7. **Typography** — Full hierarchy (H1 through caption with exact px sizes), display/accent/body fonts, usage rules per context, type on color backgrounds, minimum sizes.
8. **Icons** — UI icon system: 8-12 essential icons (arrow-right, check, close, plus, settings, search, user, bell, menu, info, etc.) rendered in the brand's geometric style + stroke/corner/grid rules + library recommendation for icons beyond the set. See `references/brand-guidelines.md` "Icons Page — Structure & Rules" section.
9. **Voice & Tone** — Tone adjectives, copy examples by context (headline, body, button, error state, social caption), forbidden words/phrases. Show actual brand copy, not generic example copy.
10. **Imagery Rules** — adapts to the brand's medium. **Photography-led** → photography rules (subject/light/color/cast/texture/forbidden + 1 example photo). **Illustration-led** → illustration rules (style/color/line/character/composition/forbidden + 1 example illustration). **Hybrid** (both equally) → split into two pages, guidelines becomes 16 pages. See `references/brand-guidelines.md` "Imagery Rules Page — Adapts per Brand."
11. **Visual World** — Full-bleed 4-column grid of 4 images matching the brand's medium mix (all photos, all illustrations, or mixed). Cast must be racially diverse for any people-featuring images.
12. **Touchpoints — Real Photos** — A 2×2 grid of 4 REAL GENERATED PHOTOGRAPHS showing the brand in physical context. **Adapt to the brand type:**
    - **Physical product brand**: hang tag on garment, woven label macro, kraft mailer with tissue, flat lay of product + packaging
    - **Digital / app brand**: phone in hand showing the app, laptop on desk showing the site, sticker on water bottle, tote bag in a real scene
    - **Service brand**: business card in hand, branded notebook on desk, signage on a building, swag in context
    No CSS vector mockups on this page — without real generated photos the touchpoints look like a Figma exercise, not a brand. Real images prove the brand can survive contact with the physical world.
13. **Brand Applications — CSS Mockups** — CSS-rendered mockups of secondary applications, each labeled with specs: business card (with dimensions), social avatar (circle crop), sticker/app icon (rounded square), email signature, presentation cover slide. For product brands also include: hang tag spec, woven label spec, shopping bag spec.
14. **Digital / Social** — Website hero aesthetic (colors, fonts, layout feel), Instagram grid style (3×3 mockup with color palette + caption tone), story template (brand colors + logo placement), link-in-bio layout.
15. **Do & Don't** — 5 dos and 5 don'ts, brand-specific and actionable. Not generic ("do use the logo correctly") — brand-specific ("do leave a full em-dash of space around the wordmark in social posts; never crop our tagline mid-word").

Keep Page 2 (strategy) before Page 3 (foundation), and keep both before logo/color/type. Strategy frames every visual decision that follows.

Include every page in the structure. If the brand has no packaging, adapt the touchpoints page to the brand type instead of skipping it; the guidelines should still show how the identity survives in real contexts.

**Completion gate:** do not deliver a condensed or partial guidelines PDF. A
condensed 6-page deck, missing Visual World page, missing Touchpoints page, or
missing Brand Applications page is a failed checkpoint, not a final deliverable.
If time runs out, stop with a resumable checkpoint that lists completed pages,
missing pages, generated asset URLs, and the next render step. Do not present
the deck as done until all mandatory pages have rendered and passed QA.

All build rules in `references/brand-guidelines.md` apply: server-side Chromium render contract, explicit 1200×850 page dimensions, HTTPS/data-URI assets, no load-bearing text on generated images, no duplicate generated images across deck, text contrast thresholds on dark backgrounds, and mandatory pre-send QA previews for every page.

**Deliver as PDF.** `mcp__pika__html_to_pdf` returns a CDN `file_url`; give the user that URL. If exporting a local kit later, download that `file_url` into `~/Desktop/[brand-name]-brand-guidelines.pdf` or the kit folder as `brand-guidelines.pdf`. Do not use `mcp__pika__upload_asset` for PDFs; that tool still only accepts images/audio/video.

### Step 5 — Export the Brand Kit (after user confirms guidelines)

After delivering the 15-page guidelines PDF, **wait for explicit user confirmation** that they're happy with the brand. Don't auto-export — the kit codifies the final brand, so only build it once the brand is locked.

Then build a comprehensive brand kit zip that lets the user produce on-brand work anywhere — in Claude, GPT, Figma, with a designer, with a developer.

**Kit structure:**

```
[brand-name]-brand-kit.zip
├── brand.md                       # comprehensive machine-readable spec
├── brand-guidelines.pdf           # full 15-page guidelines PDF (the visual deliverable)
├── README.md                      # 1-page how-to-use guide
├── logo/
│   ├── symbol/                    # standalone mark, one set per color variant
│   │   ├── symbol-[color].png     # transparent background, 1024×1024+
│   │   ├── symbol-[color].svg     # only when vector-authored
│   │   └── symbol-[color].pdf     # vector PDF or raster PDF wrapper
│   ├── wordmark/                  # the brand name styled
│   │   └── wordmark-[color].{svg,png,pdf}
│   └── lockup/                    # symbol + wordmark together
│       ├── horizontal/
│       │   └── lockup-h-[color].{png,pdf} + svg when fully vector-authored
│       └── stacked/
│           └── lockup-s-[color].{png,pdf} + svg when fully vector-authored
├── icons/                         # the 12 UI icons from page 8 as SVGs
│   ├── arrow-right.svg
│   ├── check.svg
│   ├── close.svg
│   ├── plus.svg
│   ├── search.svg
│   ├── user.svg
│   ├── settings.svg
│   ├── bell.svg
│   ├── menu.svg
│   ├── info.svg
│   └── [+ any brand-specific icons]
├── fonts/                         # actual TTF font files (OFL-licensed Google Fonts)
│   ├── [display-font]-Variable.ttf
│   ├── [body-font]-Variable.ttf
│   └── README.md                  # license + install instructions
├── tokens/                        # design tokens for devs
│   ├── tokens.css                 # CSS custom properties — paste into :root
│   ├── tokens.json                # same content in JSON — for AI tools / CI
│   └── tailwind.config.snippet.js # paste into tailwind.config.js extend block
└── prompts/                       # AI prompts for downstream brand use
    ├── system-prompt.md           # paste at the top of a Claude/GPT thread for brand voice
    ├── tweet.md                   # task-specific starter: write a tweet
    ├── landing-hero.md            # task-specific starter: landing page hero copy
    ├── email.md                   # task-specific starter: marketing/transactional email
    ├── error-message.md           # task-specific starter: write a friendly error
    ├── photography.md             # task starter: generate brand-style photography (with cliché guardrails + brand-photography rules embedded)
    └── illustration.md            # task starter: generate brand-style illustration (only if the brand uses illustration as a medium)
```

**Color variants to export** (per logo): primary-on-light, primary-on-dark, neutral-on-light (ink), neutral-on-dark (cream), and one accent-on-color combination. Usually 4-5 color sets per logo type.

**brand.md** — see `references/brand-md-template.md` for the full structure. It must include:
- Quick reference block (name, tagline, primary color, fonts, voice in one scannable section)
- Positioning + audience segments
- Mission, values, story
- Voice & tone (adjectives, copy examples by context, forbidden words)
- Colors (table with hex / RGB / CMYK / Pantone / role)
- Typography (display + body + Google Fonts URLs + full hierarchy)
- Logo (wordmark description + symbol description + lockup specs + file list with paths)
- Photography rules
- Visual world description
- Touchpoint specs
- Do & don't list
- Reference brands with "borrow this" notes
- How-to-use section telling downstream tools/people how to apply the spec

**Asset generation pipeline:**
1. **Symbol master asset** — for new marks, prefer the generated PNG route: call `mcp__pika__generate_image` with `provider="gpt-image-2"` for a clean isolated mark on transparent background, centered, no text, no watermark, no mockup, no shadows. Use SVG only if the mark is deliberately simple and still reads at 16×16. Keep the best generated PNG as the source of truth when it is stronger than SVG.
2. **Logo SVGs** — write SVG variants for wordmarks, lockups, and any symbol that is actually vector-authored. Do not trace a rich generated PNG into a weak SVG just to satisfy a vector preference. For raster-generated symbols, note in `brand.md` that the symbol master is PNG.
3. **Logo PNGs** — export every symbol / wordmark / lockup as PNG on transparent background at `1024×1024+` for symbols and enough width for wordmarks. For SVG-derived assets, render SVG → PNG via `mcp__pika__html_to_png`: HTML wrapper with `<body style="margin:0;background:transparent;">` containing just the SVG, `raster_options.viewport_px:1024x1024`, `transparent_background:true` when available. For generated PNG symbols, preserve the original high-res transparent PNG and create color variants only when they remain crisp.
4. **Logo PDFs** — render SVG logo wrappers via `mcp__pika__html_to_pdf` when vector source exists. For raster-generated symbols, create a PDF wrapper that embeds the high-res PNG at full resolution and label it as raster-source in the README; do not pretend it is vector.
5. **Icon SVGs** — write each of the 12 icons as a standalone SVG with `stroke="currentColor"`, `viewBox="0 0 24 24"`, and the brand's chosen stroke weight + corner style applied consistently. See `references/brand-guidelines.md` "Icons Page — Structure & Rules" for which icons to include.
6. **Design tokens** — generate all three files from the brand spec:
    - `tokens.css` — `:root` block with `--color-*`, `--font-*`, `--font-size-*`, `--line-height-*`, `--space-*`, `--radius-*`, `--shadow-*` custom properties
    - `tokens.json` — same content as JSON object with sections: `color`, `font`, `fontSize`, `lineHeight`, `spacing`, `radius`, `shadow`
    - `tailwind.config.snippet.js` — JavaScript snippet to paste inside `module.exports.theme.extend` covering colors, fontFamily, fontSize, borderRadius, boxShadow
7. **AI prompts** — generate each prompt file with brand specifics interpolated:
    - `system-prompt.md` — a system prompt to paste at the top of any Claude/GPT thread. Includes: brand voice adjectives, forbidden words, copy rules, photography direction, color/font specs, sample voice examples. End with "Always apply this brand voice unless explicitly instructed otherwise."
    - `tweet.md` — task starter: max 280 chars, voice constraints, sample target tweets, then "Task: [USER FILLS IN]"
    - `landing-hero.md` — task starter: hero copy structure (headline + subheadline + CTA), brand voice rules, examples from the guidelines
    - `email.md` — task starter: email tone, subject line guidance, body structure, sign-off conventions
    - `error-message.md` — task starter: how the brand handles error/empty/loading states in voice (warm not robotic, specific not vague)
    - **`photography.md`** — task starter for generating brand-style photography (gpt-image-2 etc.). Must include: master prompt template tailored to the brand's photo direction (subject, light, color grade, cast diversity, texture); explicit "what to AVOID in the prompt" list (studio strobes, stock terms, glass coworking spaces, "engineers at laptops," "professional," "premium," etc.); banned cliché concepts list (hourglasses, lightbulbs, handshakes, network nodes, glowing brains, etc.); subject substitutes for "person doing X"; quality requirements (butter accent, diversity, film grain, documentary); explicit no-text guardrail string; note about never naming real publications.
    - **`illustration.md`** — only if the brand uses illustration as a medium. Task starter for generating brand-style illustrations. Master prompt template with strict palette + style rules (flat vector / line art / etc), banned elements (gradients, drop shadows, 3D, photographic textures), when to use illustration vs photography. Skip this file entirely if the brand has no illustration in its visual world.
8. **Brand fonts** — local export step. Download the actual font files from Google Fonts (or wherever the brand fonts live) and include in `fonts/`:
    - Variable font files when available: `[FontName]-Variable.ttf` (single file, supports all weights)
    - Or static weights at the levels the brand uses
    - GitHub mirror pattern: `https://github.com/google/fonts/raw/main/ofl/[fontname]/[FontName][wght].ttf`
    - Add a `fonts/README.md` noting the license (OFL is common, allows redistribution) + Google Fonts URL for online installation
9. **Brand guidelines PDF** — download the `html_to_pdf.file_url` from Step 4 into the kit as `brand-guidelines.pdf`. The kit is incomplete without it.
10. **README.md** — 1-page guide telling the user: what's in the kit, how to use brand.md with AI tools, which logo file for which context, where to install fonts (local TTFs or Google Fonts URLs), how to use the photography/illustration prompts.
11. **Zip everything**: `zip -r [brand]-brand-kit.zip brand.md brand-guidelines.pdf README.md logo/ icons/ fonts/ tokens/ prompts/`

**Brand-kit completion gate:** when the user confirms export, or when
`export_kit` is set in `--config`, the brand kit zip is a required deliverable.
Do not mark the brand kit complete until the zip exists and contains
`brand.md`, `brand-guidelines.pdf`, README, logo assets, icons, fonts, tokens,
and prompts. If any required file cannot be produced, stop with a resumable
checkpoint and list the missing files instead of shipping a partial zip.

**README.md** — 1-page guide telling the user:
- What's in the kit
- How to use `brand.md` with AI tools (paste into Claude/GPT to generate on-brand work)
- Which logo file to use for which context (web favicon → symbol PNG; print collateral → PDF; web header → wordmark SVG; etc.)
- Font installation links (Google Fonts URLs)

**Delivery:**
- Save zip to `~/Desktop/[brand-name]-brand-kit.zip` for local Mac users.
- If the environment cannot download fonts or write a local zip, do not ship a
  partial kit. Stop with a resumable blocked checkpoint that lists the
  completed artifacts (`file_url`, `brand.md`, tokens, logo assets), the missing
  files, and the exact filesystem/network blocker.
- Upload the completed zip to a CDN if needed.
- Tell the user what's in the completed zip and link to the `brand.md` so they can preview without unzipping.

## Key Principles

- **The input is the brief.** Don't ask for lengthy intake forms. Read what's in front of you and ask 3-5 precise questions.
- **Be specific about customers without narrowing the brand to one person.** Vague audiences = weak brands, but one hyper-specific individual can make the output unusably narrow. Define audience segments first: a primary segment, 1-2 secondary segments, and one anchor persona that makes the primary segment feel concrete.
- **3 options at each choice point.** Direction (step 2), then identity (step 3). Always 3.
- **Opinionated but collaborative.** Present your read confidently. They can push back.
- Generate actual copy — don't give templates with [BRACKETS]. Write real words in the brand voice.
- **All images must look real and crafted.** Generated lifestyle/touchpoint images need film grain, natural light, slight imperfections, editorial composition. Banned: perfect symmetry, gradient backgrounds, studio strobes, stock-photo energy, AI-smooth surfaces, floating objects on white. If it looks fake — regenerate.
- **Single deliverable.** One brand guidelines PDF. Not a press kit. Not a launch package. Not a social calendar. Just the brand.

---

## Brand Quality Standards

Every brand produced by this skill should meet the following standards. Generic output is a failure state because the deliverable is meant to guide real design decisions, not decorate a template.

### The Anti-Generic Test

Before delivering anything, ask: *Could this be a brand for literally anything else?* If yes — it's not done.

Strong brand = specific product/service + clear audience model + specific point of view. Weak brand = vibes + aesthetic mood board + empty tagline. Never deliver the second.

### Copy Standards

**What good brand copy sounds like:**
- It makes a specific claim: "Heavy wool. Made to last a decade." / "Built for one quiet hour a day."
- It has a point of view: "Not trend-led. Not mass-made."
- It can speak concretely to a reader inside a segment: "The app you reach for before checking your phone." This is copy style, not audience strategy; do not collapse the brand's audience model to only that reader.
- It creates tension or contrast: "Handmade. Overused. On purpose."
- It trusts the reader: no over-explaining, no "perfect for any occasion", no "cozy vibes"

**What bad brand copy sounds like:**
- "Crafted with love" / "Made with care" / "Designed with passion"
- "Perfect for any occasion" / "A timeless addition"
- "Quality you can feel" / "Designed to inspire"
- Generic taglines: "Where quality meets style" / "Wear your story"
- Hollow superlatives: "premium", "luxury", "elevated", "curated", "artisanal"
- Anything that could describe 500 other brands without changing a word

**Tagline test:** A great tagline could only belong to this brand. "Handmade. Overused. On purpose." is WORN's. "Just do it." is Nike's. If your tagline could appear on any random Etsy shop or Squarespace site without anyone noticing — rewrite it.

### Design Standards

**What editorial brand design looks like:**
- Strong typographic hierarchy — one thing is clearly the most important
- Color used with conviction — large fields, not accent dots
- Photography bleeds to edges — no floating images with shadow drops
- Scale contrast — one element dominates, others recede
- Pages feel designed, not assembled
- Whitespace is intentional, not default padding

**What generic brand design looks like:**
- Equal-sized boxes arranged in a grid
- Body copy the same size as everything else
- Centered everything
- White background with a few colored boxes
- Photos floating in white space with rounded corners
- Font specimens that say "Font Name Here" or "Sample Text"
- Color swatches that look like a paint store brochure

**Layout rule:** If a page could have been made in Canva or PowerPoint in 10 minutes — it's not good enough. Every page should require design decisions only someone with taste would make.

### Photography & Diversity Standards

Generated image sets featuring people should show racial diversity. This avoids defaulting every brand world to the same narrow cast.
- Default to a mixed cast across all 4+ lifestyle images: include Black, Asian, Latina, South Asian, Middle Eastern, or mixed-race subjects
- Vary body types, not just skin tone
- If only one person is shown, make a deliberate choice about who that person is — don't default to white/light-skinned
- Diversity is not a checkbox. It's a design choice that makes the brand more resonant and more honest

**Photography must feel found, not staged:**
- Real rooms with real lives in them (papers, plants, worn furniture)
- Imperfect light (window light, overcast, early morning)
- Film grain always — even a little
- Subjects not looking at camera unless it's a strong choice

### Deck / Guidelines Design Standards

- Typography must load. Use HTTPS font URLs or inline `data:font/...` sources in MCP-rendered HTML; local `file://` paths are not available to server-side Chromium. Always verify loaded fonts before signing off on a render. If fonts fall back to system defaults — the deck is broken, not deliverable.
- See `references/brand-guidelines.md` for the full MCP render contract and QA rules.
- Every page must have a clear visual hierarchy — one thing to look at first.
- Full-bleed photography pages should feel like magazine spreads, not slideshow slides.
- Color palette pages: full-bleed color columns, not swatches floating on white.
- Logo page: logo dramatically large, with clear variants, not timid or small.
- Voice page: show actual brand copy, not generic example copy.
- Touchpoints page: must include generated photographs of actual touchpoints — never CSS boxes.

Deliver the guidelines as one PDF, not as individual page images. Return the `mcp__pika__html_to_pdf` CDN URL and save a local copy when practical for the brand-kit zip.

### The Taste Check

Before delivering any brand output, ask yourself:
1. Would a 25-year-old with good taste want to buy from / use / work for this brand?
2. Does the copy sound like a real person wrote it?
3. Does the design look like a real designer made it?
4. Are the photos diverse and real-looking?
5. Is there a specific point of view — something this brand stands for that another brand doesn't?

If any answer is "not sure" — improve it before delivering. Strong and specific beats safe and generic every time.

---

## Load-bearing phrases

These are the anchors that keep this skill from drifting into generic brand-book output:

| Phrase | Where | Why load-bearing |
|---|---|---|
| `different business answer — not aesthetic variations` | Step 2 directions | Forces positioning variety before visual variety. |
| `fonts must have character` | Step 3 identity options | Prevents safe-font defaults from making every brand feel interchangeable. |
| `no load-bearing text on generated images` | Guidelines build rules | Keeps brand claims editable and legible in deterministic HTML/PDF. |
| `film grain, natural light, slight imperfections` | Image quality standards | Pushes lifestyle/touchpoint images away from stock-photo smoothness. |
| `Name a specific ethnicity per prompt` | Diverse-cast recovery | Fixes the model tendency toward all-white casts more reliably than generic diversity language. |

---

## Engine choice: gpt-image-2 (with caveats)

Default to `gpt-image-2` at `quality: "medium"` for all brand imagery. Why:
- Best instruction-following for cast-diversity prompts (nano-banana-pro tends to drift toward a white default unless heavily prompted).
- Strongest no-text guardrail adherence — critical for touchpoint shots (hang tag / woven label / sticker) where any baked-in text would ruin the mockup.
- Native 3:4 / 4:3 / 9:16 ratios crop cleanly on sharp subjects without weird stretching.

Avoid `nano-banana-pro` for this skill — it bakes magazine-cover-style text into product shots when prompts mention "editorial." 1K from gpt-image-2 is plenty for a 1200×850 PDF page; bump to gpt-image-2's 2K tier (or escalate to `seedream` for higher) only if a specific touchpoint genuinely needs print-tier resolution. (4K on gpt-image-2 is 16:9 / 9:16 only — this skill's 3:4 / 4:3 ratios route to `seedream` if 4K is required.)

## Runtime expectations

Tell the user the rough total up front — long stages without status updates feel broken.

| Stage | Time | Notes |
|---|---|---|
| Stage 0 → Step 1 (Q&A loop) | 5–15 min | User-paced; questions in one message |
| Step 2 (3 directions, text) | 1–2 min | Pure model output |
| Step 3 (3 identities + brand board PDF) | 5–7 min | 3 brand boards rendered via `mcp__pika__html_to_pdf` / `mcp__pika__html_to_png` QA |
| Step 4 image gen (8 photos via gpt-image-2 in 2 parallel batches of 4) | 8–12 min | The longest stage; each batch ≈ 4–6 min |
| Step 4 page build (15-page HTML + MCP render) | 2–5 min | `mcp__pika__html_to_pdf` async; `mcp__pika__html_to_png` previews for QA |
| Step 5 brand kit zip | 3–5 min | 4 colors × 3 logo types × 3 formats + 12 icons + tokens + fonts + prompts |

Total: ~25–45 min wall-clock excluding user response time.

---

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Fonts render as Times / Arial in the PDF | Font URL not reachable by server-side Chromium, or `@font-face` points to a local path | Use HTTPS raw font URLs or inline `data:font/...` sources; render a one-page `mcp__pika__html_to_png` preview before the full PDF |
| Generated image has baked-in magazine title or watermark | Prompt mentioned "magazine cover," "Vogue," "TIME," "Bloomberg," or any real publication | Strip publication names from prompt; append the verbatim no-text guardrail; regenerate. Describe visual qualities, not publications |
| Touchpoint / lifestyle photo shows only forehead / hand-only crop | 9:16 portrait source got cropped to a landscape cell | Regen with `aspect_ratio: "4:3"` or `"16:9"` to match the cell aspect, OR change the layout to a portrait cell |
| Page overflows the 850px ceiling | Headline > 60px combined with > 3 body paragraphs on the same page | Cut content, drop headline to 48px, or split across two pages. Re-render and verify with a screenshot |
| Board technically fits but looks ugly | Too much decorative styling, tiny text, muddy one-note palette, empty mockups, or weak hierarchy | Rewrite board copy to fit the budgets in `brand-identity.md`, remove decorative microtype, increase body text to 18px+, add negative space/contrast, and rerun PNG + visual QA |
| Text overlaps icons/swatches/seals/mockups | Decorative or absolute-positioned elements share the same reading area as copy | Give text a clean reading column/card, move graphics behind non-text areas only, and rerender. Passing `scrollHeight` is not enough if a sibling graphic occludes text |
| Brand board pages feel like recolored templates | Same template reused with palette swaps | Rebuild from `references/brand-guidelines.md` "Brand Board Layout — Differentiate per Option" — each board's layout must physically embody its design philosophy |
| Multi-page merge fails | Trying to stitch local page PDFs instead of using MCP | Prefer one `mcp__pika__html_to_pdf` call with native `@page`, or use `body_pages` + `shared_head` so the server merges pages |
| User picks a hybrid identity ("02's palette + 01's voice") | Skill assumes single-option pick | Build a hybrid spec brief before Step 4, confirm with user before rendering 15 pages |
| PDF upload to pika MCP returns "Unsupported file type" | `mcp__pika__upload_asset` allowlist is images/audio/video only — no PDFs | Don't use `mcp__pika__upload_asset` for PDFs. Use the `file_url` returned by `mcp__pika__html_to_pdf`; optionally save a local copy |
| Lifestyle grid all-white-cast despite diverse-cast rule | gpt-image-2 defaults to lighter skin tone when ethnicity isn't named explicitly per prompt | Name a specific ethnicity per prompt (Black, mixed-race East-Asian-and-white, East Asian, Latina, South Asian, Middle Eastern) — vary across the 4 grid prompts |
