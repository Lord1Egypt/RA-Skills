---
name: sendpulse-template-skill
description: >
  Generates production-ready, responsive HTML email templates for SendPulse campaigns, and guides
  uploading them and managing mailings via the SendPulse MCP server or API. Use this skill whenever
  the user wants to create, build, generate, design, code, or "верстать" an email template, HTML
  letter, email layout, newsletter, or campaign email — especially for SendPulse. Trigger on phrases
  like: "make an email", "create email template", "build a newsletter", "HTML email", "email layout",
  "зроби шаблон", "створи лист", "html шаблон розсилки", "зверстай лист", "сделай письмо",
  "шаблон рассылки", "сверстай email". Also trigger when the user names an email TYPE (welcome,
  promo/sale, newsletter/digest, transactional/order, reactivation, abandoned cart, educational)
  and asks to create it, even without the word "template". This skill codes HTML email layouts —
  it is NOT for writing plain business correspondence text. Works for users in any country and any
  language, and serves both beginners (fast, few questions) and expert marketers (deep control).
license: MIT
metadata:
  version: "1.5"
  homepage: https://github.com/sendpulse/sendpulse-skills/tree/main/sendpulse-template-skill
---

# SendPulse Email Template Generator

Produces a complete, responsive **HTML email document** ready to upload to SendPulse (*Upload a file*,
MCP, or API) or paste into the HTML editor. Works in any AI coding agent (Claude Code, Cursor, ChatGPT, etc.).

> **Output format:** a **complete HTML document** — `<!DOCTYPE html>`, `<html>`, `<head>` (meta tags +
> the `<style>` blocks), `<body>` (the layout). This matches SendPulse's own exported templates and
> the *Upload a file* path. (A body-only fragment — meta + `<style>` + layout `<div>`, no `<head>`/
> `<body>` — also works in the *Insert code* editor, but the full document is the default.) Full rules
> in [references/html-rules.md](references/html-rules.md) — **read it before writing any HTML.**

---

## How this skill thinks: two audiences, one workflow

**You don't need to prepare anything formal.** Just say what the email is for — the skill leads you
through the rest (email type → goal → style → content → the technical build) and asks only for what
it genuinely needs. It serves **two kinds of users** and adapts automatically, and always tells the
user which mode it picked and that the other mode exists.

| Mode | Who | Behavior |
|---|---|---|
| **Quick** (default) | Beginners, "just make me an email" | Max 3 questions, smart defaults, one good template fast. Proactively offers tips but never blocks. |
| **Pro** | Marketers who mention segments, UTM, A/B, brand guidelines, deliverability, dark mode, localization | Offers depth: subject-line variants, UTM scheme, A/B plan, i18n, analytics setup, brand profile. Loads reference files on demand. |

**Detecting the mode (infer, never interrogate):**
- Short / vague request, no marketing vocabulary → **Quick**. Example: *"make a promo email for a coffee shop sale."*
- Request mentions any of: brand guidelines, tone of voice, UTM, A/B test, segment, deliverability,
  dark mode, RTL/localization, analytics, "our colors/fonts", attaches a `brand-profile.md` → **Pro**.
- When unsure → start **Quick**, then add one line: *"I can also go deeper — subject-line variants,
  UTM tags, A/B plan, dark-mode and localization. Say 'pro mode' anytime."*

---

## Workflow

1. **Parse the request** — detect email TYPE, language, brand hints, content, any image URLs.
   Read [references/email-types.md](references/email-types.md) to pick the section set for the type.
2. **Pick the mode** (Quick vs Pro) per the table above and state it briefly.
3. **Clarify only what's missing** — see the Quick/Pro question sets below. Never re-ask what the
   user already gave. If a `brand-profile.md` is attached, read it and skip branding questions.
4. **Announce the layout** — one line listing the sections you'll build, in order. (Cheap, prevents
   rework — borrowed from the best email skills.)
5. **Read [references/html-rules.md](references/html-rules.md)** — always, before writing code.
6. **Assemble sections** using the type→sections map and the canonical HTML patterns.
7. **Generate the HTML fragment** — apply all rules strictly; use placehold.co for missing images.
8. **Generate 3 subject-line options + 1 preheader** (see [references/content-copywriting.md](references/content-copywriting.md)).
9. **Output** — save the `.html` file, show the full code block with paste instructions, and offer
   the relevant next steps (upload via MCP/API, analytics, A/B, variables) from the Pro add-ons.

---

## Quick mode — the fast path (beginners)

Ask **at most these three**, and only if not already answered:

1. **What's the email about?** (type + main message + the link the button should point to)
2. **Brand colors / logo?** — "If you have them, drop a HEX color or logo URL. If not, I'll pick a
   clean palette." (Never block on this.)
3. **Language?** — default to the language the user is writing in.

Then: announce layout → generate → deliver the HTML + 3 subject lines + paste instructions.
Default width **600px**. Use sensible defaults (see below). Offer — but don't force — one or two
high-value tips (e.g. *"want me to add UTM tags so you can track clicks?"*).

**Quick-mode defaults (apply silently when the user skips):**
- Width `600px`; Primary `#2D6CDF`, Accent `#FF5A00`; Page bg `#eeeeee`, Content bg `#ffffff`;
  Text `#333333`, Muted `#808080`; Font `Arial, "Helvetica Neue", Helvetica, sans-serif`.
- Always include: visible preheader bar, unsubscribe in footer, `{{unsubscribe_url}}`,
  `{{ec_es_email_sender_company}}`, `{{ec_es_email_sender_address}}`, `{{current_year}}`.
- Images: placehold.co color-matched to the palette (ASCII labels only).

---

## Pro mode — the deep path (expert marketers)

Offer these as a menu; let the user pick depth. Pull the matching reference file when they engage:

| Add-on | Reference file |
|---|---|
| Email type rules & section sets | [references/email-types.md](references/email-types.md) |
| Subject lines, preheader, CTA, humanized copy | [references/content-copywriting.md](references/content-copywriting.md) |
| Languages, RTL, CJK/Cyrillic, locale formats | [references/i18n.md](references/i18n.md) |
| Dark mode, accessibility, cross-client safety | [references/dark-mode-accessibility.md](references/dark-mode-accessibility.md) |
| Visual style directions & analyzing a reference | [references/style-directions.md](references/style-directions.md) |
| Variables, UTM, click/open analytics, A/B, unsubscribe | [references/variables-analytics.md](references/variables-analytics.md) |
| Upload the template via the SendPulse MCP server | [references/sendpulse-mcp.md](references/sendpulse-mcp.md) |
| Upload images & send via the SendPulse API | [references/sendpulse-api.md](references/sendpulse-api.md) |
| Reusable brand profile (colors, tone, socials, blocks) | [references/brand-profile.md](references/brand-profile.md) |

**Proactive Pro tips to surface while building** (mention what fits; don't dump all at once):
- Generate several subject-line variants so the user can choose or A/B test them.
- Propose a UTM scheme and add tags to in-email links (never to the unsubscribe link).
- Remind to enable click/open tracking in SendPulse campaign settings.
- Suggest personalization variables (`{{name}}`, custom variables) where they add value.
- Recommend pulling image URLs straight from the SendPulse File Manager (stable, fast CDN).
- Suggest an A/B test when the list is large enough to be meaningful.
- Offer to start a reusable `brand-profile.md` so future emails are one-click consistent.

---

## Template Types → Sections

Build only the sections relevant to the type. Full per-type guidance in
[references/email-types.md](references/email-types.md).

| Section | welcome | promo | newsletter | transactional | reactivation | trigger |
|---|---|---|---|---|---|---|
| Preheader bar | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Header + logo | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Hero image + headline | ✅ | ✅ | optional | ❌ | ✅ | ✅ |
| Intro / welcome text | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Features (3-col icons) | ✅ | optional | ❌ | ❌ | optional | ❌ |
| CTA button | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Product cards | ❌ | ✅ | optional | optional | optional | ✅ |
| Article digest blocks | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Order / transaction details | ❌ | ❌ | ❌ | ✅ | ❌ | optional |
| Social icons | optional | optional | ✅ | ❌ | optional | ❌ |
| Footer + unsubscribe | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## Core HTML patterns (summary — full spec in html-rules.md)

These are the load-bearing rules. **Always read [references/html-rules.md](references/html-rules.md)
for the complete, copy-pasteable patterns** (document shell, content block, button, spacer, footer).
**Reference examples** are in `assets/examples/` — `real-sendpulse-*.html` are real SendPulse
production templates (ground truth for exact markup); the others are clean teaching templates. Open
them on demand for full assembly — don't load them on every generation.

> **⚠️ IMPORTANT — responsiveness must NOT depend on media queries.** Email clients (the Gmail app
> especially) routinely strip `<style>` blocks, or fail to apply them unless they sit in `<head>` —
> and a SendPulse fragment's styles do not. So **build every responsive behavior (column stacking,
> fluid widths) on inline styles that survive stripping**: `display:inline-block` + `max-width` for
> columns, wrapped in `<!--[if mso]>` ghost-table cells for Outlook, plus a `width:100%; max-width:Npx`
> inline style on `bodyTable` so it shrinks to the viewport on its own. **Media queries are a
> progressive-enhancement layer only** (full-width buttons on phones, padding tweaks) — the layout
> must already be correct with every `<style>` block removed. Validate by deleting the `<style>`
> blocks and confirming the email still stacks to one column at phone width. Full pattern in
> [references/html-rules.md](references/html-rules.md) (§3).

- **Complete document** — `<!DOCTYPE html><html><head>` (meta tags + the two `<style>` blocks), then
  `<body>` with the wrapper `<div>` → `wrapper-table` (100%) → `bodyTable`. Make
  `bodyTable` fluid with an **inline** `width:100%; max-width:600px` (keep `width="600"` for Outlook)
  so it shrinks to the viewport even when the `<style>` is stripped — never rely on a media query
  alone to shrink it.
- **Tables for section structure; fluid-hybrid for columns.** No flexbox, grid, or float. Each
  visual section is a `<table width="100%">`. For multi-column rows, **do not** rely on
  media-query-only `<th class="tc responsive">` columns — they revert to the desktop layout in the
  Gmail app. Use the fluid hybrid: `display:inline-block` blocks with `width:100%; max-width:Npx`,
  wrapped in `<!--[if mso]>` ghost-table cells so Outlook keeps them side by side. They stack by
  themselves when the viewport is narrower than the column sum, with or without media queries.
- **Vary the layout to fit the content.** A single column is the default and most robust; use 2
  columns for paired products, 3 columns only for short icon/feature rows, and alternating
  image+text rows for storytelling. Don't force every email into a 3-column grid.
- **Each section is its own `<table width="100%">`** stacked in the body `<td>`.
- **Visible preheader bar** as the first section — never a `display:none` span.
- **CTA = CSS-table button** (no VML). Tap target ≥ 44px tall.
- **Button rows stack on mobile (media-query-free).** When two or more CTAs sit side by side, build
  the row as `display:inline-block` blocks with `max-width`, wrapped in `<!--[if mso]>` ghost-table
  cells for Outlook — so they reflow to one column on phones on their own, even with styles stripped.
  Give each button block a `padding-bottom` (~12px) so they never collide once stacked. Full snippet
  in [references/html-rules.md](references/html-rules.md).
- **Spacing via `<table class="separator">` rows**, never CSS `margin` between sections.
- **Pad content away from color boundaries.** Whenever two stacked sections have **different**
  background colors, content must not touch the seam where the color changes. Put real top **and**
  bottom padding (≥24px desktop / ≥16px mobile) **inside each colored section's own content `<td>`** —
  never leave a section cell with `padding-top:0` or `padding-bottom:0` against a differently colored
  neighbor (a button flush on the next section's background is the classic bug). A transparent
  `separator` row alone won't fix this, because it inherits one side's color; the breathing room has
  to live inside each section.
- **Inline styles**, 6-digit hex (`#ffffff`, not `#fff`), individual padding properties on `<td>`
  (never the `padding: 10px 20px` shorthand).
- **MSO conditional comments / VML** for Outlook backgrounds; plan square-corner fallback for radius.
- **Footer is mandatory** with `{{unsubscribe_url}}`.

---

## Image handling

**Prefer the brand's own real assets** — logo, product photos, hero — uploaded to the SendPulse File
Manager (see [references/sendpulse-api.md](references/sendpulse-api.md)). Placeholders are for drafts
only; replace them before sending. When images sit **side by side in a row, give them identical
dimensions** (crop beforehand) so the cards line up — email clients can't reliably crop on the fly.

When the user has **no** images yet, use **placehold.co** color-matched to the brand:

`https://placehold.co/{W}x{H}/{bg-hex}/{text-hex}/png?text={ASCII-Label}&font={font}`

- ASCII only in `text=` — no emoji/Unicode (★ ✓ → render broken). Use `LOGO`, `Hero`, `01`, `A`.
- Fonts: `montserrat`, `poppins`, `open-sans`, `roboto`, `lato`, `raleway`, etc.
- Feature icons (≤80px squares): short labels (`01`,`02`) + `border-radius:50%` for circles.

When the user gives real URLs, use them verbatim in `src`; keep dimensions as `width`/`height`.
**Recommend** uploading images to the SendPulse File Manager and using those URLs — see
[references/sendpulse-api.md](references/sendpulse-api.md) (resize/convert tips included there).

---

## SendPulse variables (most common — full list in variables-analytics.md)

| Variable | Use |
|---|---|
| `{{unsubscribe_url}}` | **Required** in every footer |
| `{{webversion}}` | "View online" link in the preheader |
| `{{current_year}}` | Footer copyright year |
| `{{ec_es_email_sender_company}}` | Company name in footer |
| `{{ec_es_email_sender_address}}` | Physical address in footer (legally required) |
| `{{name}}` | Subscriber first name (personalization) |

See [references/variables-analytics.md](references/variables-analytics.md) for custom variables,
fallback values, UTM conventions, analytics, and A/B testing.

---

## Critical anti-patterns (never do these)

- ❌ Mangling Outlook conditional comments by reformatting/prettifying — keep each `<!--[if …]>`
  opener on a single line (a Prettier-style line break inside `[if mso]` breaks ghost tables & VML).
  Never run an HTML formatter over a finished email template.
- ❌ Hidden `display:none` preheader — use the visible bar
- ❌ `padding: 10px 20px` shorthand on `<td>` — individual properties only
- ❌ VML buttons — CSS-table buttons only
- ❌ `margin` for section spacing — use `<table class="separator">`
- ❌ `display:flex`, `display:grid`, `float`, `<link>` stylesheets
- ❌ 3-digit hex in inline styles (`#fff` → `#ffffff`)
- ❌ Emoji/Unicode in placehold.co `?text=`
- ❌ Media-query-only responsiveness — e.g. `<th class="tc responsive">` columns that stack only via
  an `@media` rule, or a `bodyTable` that shrinks only via `@media`. These revert to the desktop
  layout in the Gmail app when styles are stripped. Build columns and fluid widths on inline styles
  (`display:inline-block` + `max-width`) + MSO ghost tables; treat `@media` as enhancement only.
- ❌ Setting base text direction via CSS for RTL — use the `dir` attribute in markup (see i18n.md)
- ❌ Relying on agent-specific tool names — keep output instructions generic for portability
- ❌ `<div>` for small badges / number circles / chips — SendPulse's mobile reset
  (`td,div{width:100%!important}`) stretches them into full-width bars. Use
  `<span style="display:inline-block; width:..; height:..">` instead (spans escape the reset).
- ❌ Centering a CTA button with `margin:auto`/`<center>` alone — it can left-clip on Gmail mobile.
  Add `align="center"` to the button `<table>` and keep horizontal padding comfortable but not so
  wide the button runs edge-to-edge on a phone.
- ❌ A row of side-by-side buttons that stays multi-column on mobile, or stacked buttons with no gap
  between them. Use the fluid hybrid (`inline-block` + `max-width` + MSO ghost tables) so the row
  reflows to one column on phones without a media query, and put `padding-bottom` on each button block
  so they don't fuse together once stacked.
- ❌ Letting content butt against the seam between two differently colored sections (e.g. a button or
  heading with `padding-top:0`/`padding-bottom:0` sitting flush on the neighbor's background). Always
  keep top/bottom padding inside each colored section's content cell.

> **Self-QA before delivering:**
> - Preview in the SendPulse editor, then **send a test to yourself** and open it on both desktop and
>   phone — that's the real cross-client check.
> - Verify: every image loads and is on-topic, columns stack cleanly on mobile, the CTA is centered
>   and easily tappable, and the footer has unsubscribe + sender address.
> - Service variables (`{{name}}`, `{{unsubscribe_url}}`, `{{webversion}}`) show placeholder *stubs*
>   in test sends — that's normal; they fill in on the real campaign. Don't mistake a stub for a bug.

---

## Output

1. **Save** the template as a `.html` file in the working folder.
2. **Show** the full HTML in a fenced ```html block for copy-paste.
3. **Give paste instructions:** "In SendPulse: Email → create a campaign → choose the template
   editor → switch to **HTML editor / code mode** → paste the code."
4. **For local images, offer the ZIP upload** (easiest manual path *with* images — no API, no File
   Manager URLs): New template → **Upload a file** → a `.zip` containing the HTML + all images **in
   the archive root** (no subfolders, ≤5MB), with image `src` as **bare filenames** (`src="hero.jpg"`),
   and tick **"Upload images to the server SendPulse"**. SendPulse hosts the images and rewrites the
   `src` to permanent URLs. Remote URLs (CDN/placeholders) can coexist. See
   [references/sendpulse-api.md](references/sendpulse-api.md). *(Verified working.)*
5. **Offer the next step:** upload automatically via the
   [MCP server](references/sendpulse-mcp.md) or [API](references/sendpulse-api.md) so the user
   doesn't copy-paste by hand, plus any relevant Pro add-ons (subject variants, UTM, A/B, analytics).
6. **Hand off what's out of scope:** running the campaign itself (address books, segments,
   scheduling, campaign analytics) → the **`sendpulse-email-skill`**; transactional sending
   triggered by app events → the **`sendpulse-smtp-skill`**. Recommend installing them if missing.

---

## Keeping this skill up to date

This skill is versioned (`metadata.version` above + the `VERSION` file). If you have web access,
you MAY check once per conversation when the skill is first used:

1. Fetch `https://raw.githubusercontent.com/sendpulse/sendpulse-skills/main/sendpulse-template-skill/VERSION`
2. Compare with the local version.
3. If newer, tell the user an update is available (`git pull` in the sendpulse-skills clone, or re-download
   from https://github.com/sendpulse/sendpulse-skills/tree/main/sendpulse-template-skill) — then continue with the current
   version.

Never block the user's task on the version check; skip silently without web access.
