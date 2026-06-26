---
name: app-store-screens
description: >
  Generate 5–6 App Store screenshots in a given brand's aesthetic from a `brand.md`, raw
  product screenshots, or a public App Store listing fetched through Pika MCP. Story-driven
  (hook → value → features → proof → close), splashy, on-brand.
  Outputs 1290×2796 PNGs ready to drop into App Store Connect. Use when someone wants App Store /
  store listing assets — including: "make me app store screenshots", "design app store screens
  for [brand]", "I have a brand.md and screenshots, generate store assets", "screenshot set for
  app launch", "iOS store screens", "app store creative", "store listing visuals", "splashy app
  store screens", "app-store-screens".
argument-hint: <brand-md-or-brand-spec-or-app-store-url> [product-screenshots-or-figma-url] [reference=<url-or-path>] [count=5|6] [--quick] [--config <path>]
required-capabilities:
  - mcp__pika__analyze_media
  - mcp__pika__capture_website
  - mcp__pika__fetch_appstore_screens
  - mcp__pika__generate_image
  - mcp__pika__html_to_png
  - mcp__pika__upload_asset
---

# App Store Screens

Take a brand plus real product screens and produce a 5–6 screen App Store campaign at iPhone 6.9" size (1290×2796). The product screens can come from raw exports, Figma/source files, or a public App Store listing fetched through Pika MCP. Story-driven, splashy, strict to the brand.

This is a sister skill to `build-a-brand` — it consumes that skill's `brand.md` spec, but works equally well with any brand spec the user supplies.

## The deliverable

5 or 6 PNGs, numbered, saved to `~/Desktop/[app-name]-app-store-screens/` (or wherever the user prefers):

```
01_hook.png            ← biggest claim, works as a search-result thumbnail
02_value.png           ← the one thing the app does best
03_feature_a.png       ← specific capability
04_feature_b.png       ← another specific capability
05_proof.png           ← social proof, awards, "loved by", differentiator
06_close.png           ← optional 6th — closer / CTA / brand flourish
```

Plus a contact sheet (`_preview.png`) showing all 6 at a glance.

## Workflow

### Step 0 — Intake and style choice

If invoked with empty args and no usable brand/screenshot/demo context, print this menu verbatim and stop. Do not generate imagery or render HTML until the required inputs are present.

> **What App Store screenshot set should I make?** Required:
>
> - **Brand spec** — `brand.md` or equivalent brand notes with name, palette, fonts, voice, and imagery direction; or an App Store URL/app name if you want me to fetch the listing and draft the brand read first
> - **Raw product screenshots** — exported PNGs, a Figma/source file that can export them, a folder of screenshots, or an App Store URL/app name I can fetch with Pika MCP
> - **Or a fictional app demo brief** — only for launch demos/concepts where no real product exists; say `demo_mode: true` and provide what the fake app does
>
> Optional: reference App Store screenshot, moodboard, preferred screen count (5 or 6), output folder.

In interactive mode, if the user has supplied partial input, ask only for the missing required items and stop. If the non-interactive fast lane applies, use Step 0.5 instead. Required inputs:
- `brand.md` or an equivalent brand spec with name, palette, fonts, voice, and imagery direction; if the user gives an App Store URL and asks you to "help create it", fetch the listing first and draft an inferred brand spec from the listing/icon/screenshots for approval
- one product source: raw product screenshots, a Figma/source file that can export them, or an App Store URL/app name that can be fetched through Pika MCP
- for fictional launch demos only, `demo_mode: true` with `demo_brief` is an alternative to real product screenshots; use the Fictional app demo mode path below
- optional reference screenshot or moodboard if they want a specific App Store style

### Step 0.5 — Non-interactive fast lane

Use this path when the caller passes `--quick` or `--config <path>`, or when the
caller states they are running from CI, a subagent, a batch job, or any other
non-interactive harness.

This section has precedence over the interactive ask/wait instructions below.
When it applies, use this fast lane and do not fall through to the multi-turn
intake unless the required brand and either product screenshots or explicit demo
mode inputs are truly unavailable.

- `--config <path>` points to a JSON file with pre-baked choices: `brand_spec`,
  `product_screenshots`, `app_store_url`, `website_url`, `reference`, `style`,
  `screen_count`, `narrative_arc`, `demo_mode`, `demo_brief`, and
  `output_folder`.
- `--quick` means choose the default style unless a reference is supplied, infer
  the brand read from the provided brand spec or App Store listing, draft the
  5-6 screen arc yourself, and proceed.
- For `--quick` or `--config`, do not stop for confirmation at the style choice,
  brand-read playback, reference-rule playback, or 5-6 screen strategy pitch.
  Record assumptions inline and continue to design/render.
- If neither real product screenshots nor explicit `demo_mode: true` with
  `demo_brief` is available, stop once with a single compact missing-fields list
  instead of starting a multi-turn Q&A loop.

#### Fictional app demo mode

Use this only when the caller explicitly says this is a fictional app, fake app,
launch demo, concept demo, or passes `demo_mode: true` in config. Do not use demo mode for real products.

Demo mode is allowed to create representative UI mocks in the brand voice when no
real product screenshots exist, but the output must be labeled as demo-only
concept work, not production assets. Treat the invented screens as a storyboarded
QRT/demo artifact, not App Store Connect-ready evidence of a real product.

- Require a `demo_brief` or enough user-provided product concept detail to define
  the app's core job, audience, 3-5 features, and proof/CTA angle.
- Generate UI states that are internally consistent with that brief; do not imply
  real customers, real reviews, real metrics, or real integrations unless the
  prompt explicitly provides them.
- Add a demo-only disclosure in the delivery notes and contact sheet label:
  "Demo UI concept — not production assets and not real product screenshots."
- In non-interactive mode, proceed only if config sets `demo_mode: true` and
  provides `demo_brief`; otherwise stop with a compact missing-fields list.

In interactive mode, when the required inputs are present, open with a brief agenda and ask one upfront style question. This is the cheapest moment to learn whether the user wants the default or a specific reference. In the non-interactive fast lane, choose the default style unless `reference` or `style` is supplied, record that assumption inline, and continue.

```
here's how this works:
1. **Read your brand + screenshots** — i absorb the brand voice, palette, type, and figure out what the app actually does
2. **Strategy** — i pitch a 5–6 screen narrative arc (hook → value → features → proof → close) with headlines for each, before any design
3. **Design + generate** — i design each layout, composite at 1290×2796
4. **Preview** — i deliver the PNGs + a contact sheet so you can see the whole campaign at once

quick question before i start — **do you want the default style, or something specific?**

- **Default** — clean, restrained, screens shown untouched. Full-frame device, headline + sub above, solid brand-color backgrounds, brand-voice copy. Codified in `references/default-layout.md`. This is what i deliver well.
- **Something specific** — share a clear reference: a screenshot of an App Store page you love (Notion, Calm, Things, Headspace, anything), a figma file, a moodboard image. I'll study it, extract the compositional rules (device size + position, headline treatment, background, any signature flourishes), pitch back what i read before designing, then build the campaign — **with your brand's palette, fonts, voice, and photography style swapped in**. So if the reference uses an over-the-shoulder photo, i'll generate one in your brand's photo style (`gpt-image-2` accepts the reference as a style input). The reference dictates the composition; your brand dictates the look.

if you don't tell me, i'll go with default.
```

**Why no "jazzed up" auto-mode.** Doing rich/varied/dramatic compositions well requires visual-judgment calls (perspective, layering, typography hierarchy, color balance) that don't have a programmatic answer. When users want richness without a reference, my approximations tend to look amateur. Asking for a concrete reference lets me extract specific rules to replicate instead of inventing freely — and the user has a way to verify i'm aiming at the right thing.

Two downstream paths based on the answer:
- **Default** → follow `references/default-layout.md` end-to-end. Same composition skeleton on every screen; variety from color + content. This produces consistent, brand-disciplined work.
- **Replicate a reference** → study the reference, extract the rules, swap in the user's brand. See "Reference-driven path" below for the full process.

If the user can't or won't supply a reference but still wants more than default, push back gently — explain that without a reference you'll deliver default plus their brand color, and that's better than a guessing-game iteration loop. Don't invent a "jazzed" style on the fly.

### Step 1 — Read the brand and the product

#### App Store listing path

If the user supplies an `apps.apple.com` URL, numeric App Store app ID, or app-name search term as the product source, try Pika MCP `mcp__pika__fetch_appstore_screens` first because it is faster, more stable, and returns hosted screenshot/icon assets ready for later render steps:

```
fetch_appstore_screens(
  query: <app_store_url | numeric_app_id | search_term>,
  country: "us",
  max_screens: 10,
  include_icon: true
)
```

Use the returned `metadata`, `icon`, and `screenshots` as the product source. The returned screenshot `url` values are already Pika-hosted HTTPS assets and can be used directly in later `mcp__pika__html_to_png` stages.

If the user provided a country-specific App Store URL, preserve that storefront country when calling the tool when possible. If the country is unclear, default to `"us"` unless the user asked for another storefront.

If the MCP tool is unavailable, unauthenticated, or returns no screenshots, say what happened and then use the least fragile fallback available: other read/fetch tools, official App Store/iTunes metadata endpoints, or user-provided screenshots. Keep the fallback grounded in real listing assets; do not invent product UI.

Expected result shape:

```
{
  "app_url": "https://apps.apple.com/...",
  "metadata": { "name": "...", "subtitle": "...", "description": "...", "category": "...", "icon_url": "https://..." },
  "icon": { "url": "https://cdn.pika.art/...", "source_url": "https://is...mzstatic.com/...", "filename": "appstore-icon.png", "mime_type": "image/png", "width": 1024, "height": 1024 },
  "screenshots": [
    { "url": "https://cdn.pika.art/...", "source_url": "https://is...mzstatic.com/.../1290x2796bb.png", "filename": "appstore-screen-01.png", "mime_type": "image/png", "width": 1290, "height": 2796 }
  ],
  "count": 1
}
```

#### Thin App Store listing guardrail

After `mcp__pika__fetch_appstore_screens`, count usable screenshots that show real
product UI. If the listing returns fewer than 3 real product screenshots, treat it
as a thin App Store listing.

- Do not create a 5-6 screen campaign by hallucinating UI. Real product UI is the
  default requirement for device frames.
- Interactive mode: stop before strategy and offer two choices:
  1. **Website-capture path** — use `mcp__pika__capture_website` or supplied
     website/onboarding URLs to capture real product surfaces, then continue with
     those captures as product screenshots.
  2. **Real screenshot path** — ask for simulator exports, Figma frames, or other
     product UI captures before continuing.
  Do not offer synthesized device UI for real products. If the user explicitly
  pivots to a fictional launch/concept demo, route to Fictional app demo mode and
  require `demo_mode: true` with `demo_brief`.
- Non-interactive fast lane: prefer the website-capture path when `website_url`
  or an obvious product website is available. If there is no captureable product
  surface, stop once with a compact missing-fields list unless config explicitly
  sets `demo_mode: true` and provides `demo_brief`.

After fetching, infer only a draft brand read from the listing and visuals: app name, category, visible palette, likely type direction, voice from subtitle/description, and notable UI moments. In interactive mode, read it back as a provisional brand spec and ask the user to correct it before pitching the 5-6 screen arc. In the non-interactive fast lane, record it as the provisional brand spec and continue.

#### Reference-driven path: how to apply the user's brand to the reference's style

The reference describes WHAT THE LAYOUT/STYLE LOOKS LIKE. The brand describes WHAT COLORS/FONTS/VOICE/PHOTOGRAPHY TO USE. The skill's job is to combine them: replicate the reference's visual structure, but render it with the user's brand. Two things to extract from the reference, two from the brand:

**From the reference, extract structural rules:**
- Device size (as % of canvas) and tilt angle
- Headline treatment (size, position, color logic — accent on key word? tinted bg pill?)
- Background treatment (solid color, photo, gradient, abstract elements)
- Hero imagery pattern (hand holding phone, over-the-shoulder, real subject breaking out of phone, 3D objects floating, etc.)
- Callout / pull-out pattern (speech bubbles with arrows, floating cards, polaroid frames, etc.)
- Repetition rules: same layout every screen, or varied per slot?

**From the brand, apply specifics:**
- Palette (substitute brand colors wherever the reference uses solid color blocks)
- Fonts (substitute brand display + body fonts everywhere the reference uses type)
- Voice (rewrite all headlines/subs in brand voice — don't copy the reference's words)
- Photography direction (any generated imagery follows the brand's photo rules — for DeltaStream that's documentary 35mm, golden hour, real apartments, butter accent in every frame, real cast diversity)
- Mood (warm vs. clinical, playful vs. expert, etc.)

**For generated hero imagery: pass the reference as `reference_images` to `gpt-image-2`.** The tool supports up to 16 reference images. Use this when the reference uses a distinctive photo composition (hand-holding-phone, over-the-shoulder, person breaking out of screen, 3D character emerging). Combine with the brand's photography rules in the prompt:

```
Reference: [user's reference photo — e.g., insect app's hand-holding-phone with butterfly]

Prompt: "In the EXACT composition and lighting style of the reference image — hand
holding a phone at the same angle and scale — but render the subject and scene
per [BRAND] photography rules: documentary 35mm, golden hour window light, real
apartment, butter-yellow ceramic mug visible, mid-30s mixed-race cast, 35mm film
grain. Vertical 9:16 portrait."
```

This is how you get the reference's STYLE without copying its CONTENT. The hand+phone composition transfers; the lighting/cast/setting comes from the brand.

**Pitch the extracted rules back before designing in interactive mode.** Write them out as a short bullet list ("device 75% canvas tilted -8°, headline-on-yellow-pill above device, over-the-shoulder hero, ink callouts with curved arrows") and confirm with the user that you read the reference correctly. In the non-interactive fast lane, record the extracted rules inline and continue. Then build all 6 screens applying those rules consistently. Don't deviate mid-campaign.

Then actually read:

- **`brand.md`** — extract: brand name, tagline, palette (with hex), display font + body font, voice adjectives, voice examples, forbidden words, photography/illustration direction, mood words. If the file is a different format (PDF, plain notes), parse what's there and ask about gaps in interactive mode. In the non-interactive fast lane, record reasonable assumptions for non-critical gaps — don't invent a brand.
- **Product screenshots** — open each one and form an honest mental model: *what does this app actually do?* Note the core UI patterns (feed, chat, canvas, list, map, etc.), the primary action surface, and any "wow moment" screens (a generative result, a beautiful state, a unique interaction).
- If you can use `mcp__pika__analyze_media` to inspect screenshots without loading them as images, do — it's faster for a quick scan.

**Then read back what you found** (3-5 lines, conversational):

```
ok — reading [brand name]: [tagline]. palette: [colors]. voice: [adjectives]. the app looks like
it does [X] — i see [specific UI cue 1] and [specific UI cue 2]. the standout screen is [screen
N] because [reason]. correct me where i'm wrong, otherwise i'll pitch the 6-screen arc.
```

Interactive mode: wait for confirmation before pitching strategy. Catches misreads cheaply. In the non-interactive fast lane, treat the brand read as provisional, record the assumption inline, and continue to the strategy.

### Step 2 — Pitch the 6-screen strategy

Before designing anything, write out the narrative arc as plain text. Each screen needs:

- **Role** (hook / value / feature / proof / close)
- **Headline** (5–8 words, in brand voice — see "Copy" below)
- **Optional subhead** (one short line)
- **Layout archetype** (see below — name it, don't draw it yet)
- **Which raw screenshot it features** (filename) — or "none, full-bleed typography"

Present it like:

```
**Screen 1 — HOOK**
Headline: "Sleep like you mean it."
Sub: (none — let the headline carry)
Layout: full-bleed UI with bold typography overlay
Featured screenshot: home_screen.png

**Screen 2 — VALUE**
Headline: "One tap. Then quiet."
...
```

Interactive mode: ask the user to sign off on the arc before you generate or composite anything. Iterate on copy here — it's the cheapest moment to fix it. In the non-interactive fast lane, generate from the configured or inferred arc without stopping for signoff.

### Step 3 — Generate brand-world imagery

For any screen that calls for splashy background/hero imagery, generate it with `mcp__pika__generate_image`.

**Defaults that work for App Store splash:**
- `provider: gpt-image-2`
- `quality: medium` for finished screenshots; `low` only when the user explicitly wants fast iteration
- `aspect_ratio: 9:16` for full-bleed backgrounds (matches the iPhone canvas)
- 1K is the default. If a screen genuinely needs higher res (e.g. a hyper-detailed background that gets blown up), bump `gpt-image-2` to its 2K/4K tier (9:16 backgrounds support both) or escalate to `seedream` — surface the tradeoff and ask first

**Prompt structure for brand-world imagery:**
1. Subject + composition ("a wide cinematic shot of a single ceramic mug on weathered oak…")
2. Brand palette as named colors ("limited to ink black #0E0E10, oat #F5F0E6, and a single accent of rust #C84B2F")
3. Light + mood ("soft overcast window light, slight film grain, documentary feel")
4. Negative cues ("no text, no logos, no people unless specified, no stock-photo gloss")
5. Aspect for 9:16 backgrounds: "vertical composition with negative space in upper third for headline"

**Reserve upper third for the headline.** Tell the image model where the type will go so it leaves room.

Keep generated image URLs as HTTPS/CDN URLs for server-side rendering. If the user provides local product screenshots or background images, upload them with `mcp__pika__upload_asset` first and use the returned `public_url`; `mcp__pika__html_to_png` cannot read local `file://` paths.

### Step 4 — Composite each screen at 1290×2796

Write one HTML stage per screen, then render to PNG via Pika MCP `mcp__pika__html_to_png`. See `references/render-pipeline.md` for:
- The exact `mcp__pika__html_to_png` request shape
- Server-side asset/font rules
- Safe-zone guides
- Common gotchas (font loading, retina text sharpness, mid-curve crop)

Each HTML stage should be exactly 1290×2796px. Use `@font-face` with HTTPS raw font URLs or inline `data:font/...` sources. Local brand-kit font files must be exposed through a public HTTPS URL or inlined; `mcp__pika__upload_asset` does not accept font mime types.

After each render, run a pre-delivery QA pass before accepting the PNG. Use
`mcp__pika__analyze_media` on the rendered image and inspect the authored HTML
positions when available. Reject and rerender any screen whose text block
bounding boxes put load-bearing headline, eyebrow, subhead, CTA, or product UI
outside the safe content area documented in `references/render-pipeline.md`.

### Step 5 — Build the contact sheet + deliver

Once all 6 PNGs render cleanly:

1. Build a `_preview.png` contact sheet with `mcp__pika__html_to_png` — 6 thumbnails in a 3×2 grid at ~25% size, on a neutral background, labeled by role.
2. Present the contact sheet URL plus each individual screenshot `file_url`. If you also saved local copies, include those local paths separately.
3. Ask: anything to revise? Common revisions are copy tweaks (cheap) or layout swaps (medium) or new imagery (most expensive).

Do not report the screenshot set complete until `_preview.png` exists and is
included in the delivery. If the contact sheet render fails, fix the sheet HTML
or rerender the missing PNGs first; do not deliver only the individual PNGs and
call the campaign finished.

## The 5 layout archetypes

Use one per screen. **Don't stack devices.** One bold idea per screen.

See `references/layout-archetypes.md` for full CSS skeletons and visual examples. Quick reference:

1. **Floating device** — tilted phone on a splash background. The workhorse. Best for value/feature screens.
2. **Full-bleed UI** — phone canvas fills the frame; typography overlays at top or bottom. Best for the hook.
3. **Side-by-side** — device on one side, generated lifestyle imagery on the other. Best for emotional features.
4. **Parallax stack** — phone in front, branded shape/imagery floating behind. Best for "wow moment" feature screens.
5. **Quote card** — big pulled quote with a small device tucked in a corner. Best for the proof screen.

## Copy — non-negotiable

App Store headlines are tested in a tiny window. They must:

- **Be 5–8 words.** Anything longer dies on a 6.1" phone in search results.
- **Echo the brand voice exactly.** If `brand.md` says voice is "dry, deadpan, never exclamatory," the headlines never end in `!`. If voice is "warm and a little teasing," the headlines have rhythm.
- **Make a claim, not a description.** "Sleep like you mean it" > "Track your sleep". "Built for one quiet hour a day" > "Productivity app".
- **First two screens work as standalone thumbnails.** Bigger type, clearest hook. App Store search shows the first 2-3 expanded; the rest only render if a user taps through.

**Banned (these are the App Store equivalent of "crafted with love"):**
- "Stay organized."
- "Your daily companion."
- "All-in-one [category]."
- "Designed to help you [verb]."
- "Track. Plan. Achieve."
- Anything with "seamlessly", "effortlessly", "powerful", "smart", "intelligent".

If the headline could appear on 500 other apps without anyone noticing — rewrite.

## Visual standards

- **The device is the hero — type is the caption.** On a 1290×2796 canvas, the device should be 1050–1150px wide (≈ 81–89% of canvas). Anything smaller looks timid. Headlines support the screen content; they don't compete with it.
- **Typography hierarchy.** One thing dominates per screen — usually the device. Headline 100–140px Funnel-Display-class; subhead 36–44px; visible difference in weight and size. (Past 150px the headline starts fighting the device for the eye.)
- **Skip SVG-stroke iPhone frames — they don't align with screenshot corners.** Stroke-based SVG bezels sit half-inside/half-outside their path, and the radius/Dynamic Island proportions never quite match a real iPhone. Prefer transparent screenshot exports from Figma/simulator or a real iPhone mockup PNG with a transparent cutout. If only rectangular source screenshots are available, use a consistent CSS `border-radius` + `overflow:hidden` wrapper and visually QA the corners. The old local `clean_phone_uniform()` PIL recipe is now a documented MCP gap, not a default dependency.
- **Pick one: bleed OR full-frame. Never mid-crop the bottom curve.** Default is full-frame (device top at y=580 with width=1000, so the rounded bottom corners sit fully inside the canvas with ~48px breathing room below). Bleed variant (device top ≥ 819) pushes the rounded bottom corners entirely past y=2796 — useful for hook screens that want drama. Anything in between produces a visible half-cut curve where the canvas slices through the rounded corner mid-arc; this is the failure mode the rule prevents.
- **Apple safe zones.** Strict safe-zone rule: load-bearing text and product UI must stay inside y=180..2616. The top and bottom 100px bands are never for critical content, and the extra 80px buffer keeps App Store chrome, search-result cropping, and text ascenders from crowding the edge. Decoration is fine; critical claim and readable app UI are not.
- **One bold device per screen.** Massive type *or* generated imagery *or* a quote — not all three. Splashy ≠ chaotic.
- **Color from the brand palette only.** No new colors invented for the screenshots. If the palette feels too restrictive, that's the brand's problem to solve, not yours.

## Sourcing the screens

The raw screens can come from anywhere — an App Store listing fetched through Pika MCP, a Figma frame, a Sketch export, a simulator screenshot, or local files. If the source is an App Store URL/app ID/app name, use the App Store listing path above. If the source is Figma and you have Figma MCP access:

- `get_screenshot(fileKey, nodeId)` returns the rendered PNG of a node. This works without needing the user to select anything in the Figma desktop app.
- For a strip-of-phones layout, prefer asking for individual phone exports. If only a strip is available, crop manually from the design source or use a future server-side crop/clean tool when exposed; don't make local PIL cropping a default dependency of this skill.
- The natural render is usually at logical-pixel size (e.g. 393×852 per iPhone 15 Pro phone). When you scale this to the default 1000px device width on the App Store canvas, the upscale is acceptable for non-pixel-critical content. For tighter fidelity, ask if there's a higher-resolution export.

## Quality bar

Before delivering, do the squint test:

1. **Squint at the contact sheet.** Can you tell the 6 screens apart at a glance? (Different headlines, different layouts, different focal weight.) If they look like 6 versions of the same screen — redesign.
2. **First-2-screens thumbnail test.** Crop screens 1 and 2 to 25% size. Is the headline still legible? Is the hook still clear? If you have to lean in, the type is too small.
3. **Brand-test.** Cover the device on each screen. Does the surrounding design still feel like the brand? (Color, type, mood, voice in headlines.) If not, the screenshot is generic.
4. **Anti-generic test** (same as build-a-brand): could these screens belong to literally any other app in this category? If yes — rewrite the copy and rework the focal hierarchy.
5. **Safe-zone audit.** Check every rendered PNG and reject and rerender any screen with load-bearing text or product UI outside the safe content area.

## Load-bearing phrases

These anchors keep the generated campaign legible and on-brand:

| Phrase | Where | Why load-bearing |
|---|---|---|
| `vertical composition with negative space in upper third for headline` | Brand-world image prompts | Leaves usable space for real App Store headline type instead of forcing text over busy imagery. |
| `The device is the hero — type is the caption` | Visual standards | Prevents poster-like screens where copy overwhelms the product UI. |
| `Apple safe zones` | Visual standards / render QA | Keeps critical claims clear of status-bar and App Store overlay areas. |
| `no text, no logos` | Generated background prompts | Avoids unusable generated typography; real copy is added in HTML. |
| `Pick one: bleed OR full-frame` | Device layout rule | Prevents the half-cut rounded-corner crop that looks like a rendering bug. |

## Engine choice: HTML-first render, gpt-image-2 only for brand-world imagery

The final screenshots should be deterministic HTML/CSS composites rendered through `mcp__pika__html_to_png`, because App Store copy, device masks, safe zones, and brand typography need exact control. Use `gpt-image-2` only for splash/background/brand-world imagery where generation adds visual richness; keep real product UI as screenshots. Bump `gpt-image-2` to its 2K/4K tier (or escalate to `seedream`) only when a specific generated background genuinely needs higher resolution than 1K.

## Runtime Expectations

Typical run time is 10-25 minutes, depending on how much user confirmation is needed:

| Step | Wall clock | Notes |
|---|---:|---|
| Intake + style choice | 1-5 min | User-paced if a reference is needed |
| Brand/screenshot read | 2-5 min | Includes visual inspection and feature mapping |
| Strategy pitch | 2-5 min | Best place to iterate copy cheaply |
| Image generation | 2-8 min | Only for backgrounds or reference-driven hero imagery |
| HTML composite + render | 5-10 min | Six 1290x2796 PNGs plus contact sheet |
| QA revisions | variable | Copy tweaks are cheap; new imagery is slower |

## Failure Modes

| Symptom | Cause | Fix |
|---|---|---|
| Screens look like six variants of the same layout | Default skeleton was repeated without enough content contrast | Reassign layout archetypes and rotate focal weight, color, and screenshot choice |
| Headlines are illegible in contact sheet | Type is too small for App Store thumbnail use | Increase headline size, shorten copy to 5-8 words, and rerender |
| Generated background contains text or fake UI | Prompt over-described brand/product specifics | Regenerate with a no-text/no-logo guardrail and reserve the real UI for screenshots |
| App Store listing has fewer than 3 usable screenshots | Thin App Store listing, often a companion app or early listing | Use the website-capture path, ask for real screenshots, or stop. For fictional launch-demo concepts only, use Fictional app demo mode with `demo_mode: true`, `demo_brief`, and the demo-only disclosure |
| Fictional app has no real product screenshots | Launch-demo concept needs representative UI, but production rules forbid hallucinated UI | Use Fictional app demo mode only with `demo_mode: true`, a concrete `demo_brief`, representative UI mocks, and a demo-only disclosure |
| Load-bearing text appears too close to the top or bottom edge | Safe-zone QA was skipped or checked only the rendered look, not text block bounding boxes | Reject and rerender with text block bounding boxes inside the strict safe-zone margin |
| Device corners look uneven | Source screenshot already contains background in the rounded corner area, or CSS radius does not match the source | Ask for transparent/high-res source exports, use a real mockup cutout, or apply one consistent CSS mask and visually QA. A server-side uniform corner cleaner is still a tool gap. |
| Brand feels generic after hiding the screenshots | Surrounding design ignores `brand.md` voice, palette, or imagery rules | Rebuild the screen shell from the brand spec before rerendering |
| Render is blurry or scaled | Stage dimensions or raster options are wrong | Verify 1290x2796 stage size and `mcp__pika__html_to_png` `viewport_px:1290x2796`, `device_scale:1` |

## When to push back on the user

- If they want a "jazzed up" version without supplying a reference → push back. Ask for a screenshot of an App Store page they love, a figma file, or a moodboard. Explain that without a reference, you'll deliver default plus their brand color, and that's better than guessing at "exciting." (This rule comes from real campaign work — auto-jazzing produced amateur output every time.)
- If they want a 10-screen campaign → push back. 5-6 is the sweet spot; more is fatigue.
- If the brand voice in `brand.md` is generic ("modern, friendly, intuitive") → flag it. You can still produce screens, but tell them the headlines will only be as distinctive as the voice spec. Offer to sharpen the voice first (it lives in `brand.md`'s Voice & Tone section).
- If they have no real product screenshots and did not explicitly request fictional app demo mode → don't invent UI. Ask for screenshots, website/onboarding capture targets, or explicit `demo_mode: true` with a concrete `demo_brief`.
- If they don't have a brand at all → don't proceed on vibes. Route them to `build-a-brand` first, or have them write at minimum: name, palette hexes, display font, body font, one-line voice description.

## References

- `references/default-layout.md` — **the visual system the skill produces when the user supplies no reference.** Read this first for any run. Codifies the headline-top + device-dominant + full-frame composition, color rotation, and squint-test checklist. This is what the skill delivers well.
- `references/layout-archetypes.md` — vocabulary list of layout patterns found in real App Store campaigns. Use only to analyze a user-supplied reference. Not a free-choice menu.
- `references/render-pipeline.md` — `mcp__pika__html_to_png` render request, server-side asset/font rules, safe-zone overlay, font-loading checklist, pre-delivery checklist.
