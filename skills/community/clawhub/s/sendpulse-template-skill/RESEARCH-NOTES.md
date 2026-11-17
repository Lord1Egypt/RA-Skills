# Research Notes — sendpulse-template-skill

Synthesized from a deep-research run (24 sources, ~120 extracted claims) plus analysis of the
existing `sendpulse-email-template` skill. Sources cited inline. This file is the evidence base
for the skill's architecture and content rules. Not shipped with the skill — internal working doc.

---

## 1. Agent Skills format — what is mandatory & portable

- **SKILL.md frontmatter: only `name` + `description` are mandatory.** `name` ≤ 64 chars, lowercase
  letters/numbers/hyphens, must match the parent directory name, cannot contain reserved words
  `anthropic`/`claude`. `description` ≤ 1024 chars, must state BOTH what the skill does AND when to
  use it, include trigger keywords, third person, no XML tags. Source: github.com/anthropics/skills,
  platform.claude.com/docs/.../agent-skills/best-practices. [confirmed 3-0]
- **Three-level progressive disclosure** (the core design principle):
  1. Metadata (~100 tokens: name+description) — always loaded for every skill at startup.
  2. SKILL.md body — loaded only when the skill activates. Keep **< 5000 tokens / < 500 lines**.
  3. Bundled resources (`scripts/`, `references/`, `assets/`) — loaded only on demand; scripts can
     even execute via bash without entering context. Source: anthropics/skills. [confirmed 3-0]
- **Standard directory layout:** `SKILL.md` + optional `scripts/` (executable code), `references/`
  (on-demand docs, small focused files), `assets/` (templates/images/data). Keep reference files
  **one level deep** from SKILL.md — Claude may only partially read (head -100) files referenced
  from other referenced files. Reference files > ~100–300 lines should open with a table of
  contents. Source: anthropics/skills, skill-creator. [confirmed 3-0]
- **Portability across Claude Code / Cursor / ChatGPT / etc.:** keep the core format minimal.
  The `compatibility` field (≤ 500 chars) — "Most skills do not need" it. `allowed-tools` is
  **experimental**, support varies between agents — a portable skill must NOT depend on it.
  Avoid Claude-only tool names in instructions (the old skill referenced `present_files`, which
  doesn't exist in Claude Code). Source: anthropics/skills. [confirmed 3-0]
- **`description` is the primary trigger.** Anthropic notes Claude tends to *under*-trigger skills,
  so descriptions should be "pushy" and enumerate concrete use cases + keywords. [from skill-creator]
- **Multi-domain pattern:** SKILL.md holds the workflow + variant-selection logic; one reference
  file per variant (e.g. per email type), so the model reads only the relevant file. [skill-creator]

## 2. Existing email skills — precedents

- **framix-team/skill-email-html-mjml** — built on **MJML 4.x as a "structural reliability
  framework"** (compiles to Outlook-safe nested tables, MSO ghost tables, VML, hybrid-fluid
  columns). Architecture: top-level SKILL.md + `compilation.md`, `mjml-reference.md`, a
  `components/` dir (head/layout/content/interactive/advanced) + `assets/examples/`. Workflow:
  gather reqs → infer type → announce layout → load only relevant component refs → generate MJML
  → compile w/ validation → deliver BOTH `.mjml` source and `.html`. [confirmed 3-0 on MJML rationale]
  - **Decision for us:** SendPulse needs an **HTML fragment** (no DOCTYPE/html/head/body), so we
    CANNOT ship MJML-compiled full documents. We keep the hand-authored table HTML approach from
    Vitya's `html-rules.md` (derived from 15 production SendPulse templates) but borrow framix's
    progressive-disclosure file split and "announce layout before coding" workflow step.
- **OneWave-AI/email-template-generator** — despite the name, generates *correspondence copy*
  (sales/support/apology emails), NOT coded HTML. Monolithic SKILL.md, no progressive disclosure.
  Not a precedent for HTML coding, but a reminder our `description` must disambiguate from copy-only
  tools. [from awesome-claude-skills]

## 3. Cross-client compatibility (caniemail.com, Litmus) — 2025–2026

- caniemail tracks ~307 HTML/CSS features across 25+ clients (the caniuse of email). Authoritative.
- **Apple Mail** macOS 287/307, iOS 282/305 — best; modern CSS mostly safe here only.
- **Outlook Windows desktop** ~59/306 (Windows Mail 62/299) — worst major client. Justifies
  table-based layout, MSO conditional comments, VML button/background fallbacks.
- **Gmail** desktop webmail 154/307; Gmail mobile apps iOS/Android ~111/307 — only ~half/third.
  Constrain CSS to the Gmail-safe subset for mobile.
- **Rule of thumb:** code to the *intersection* of Outlook-desktop + Gmail-mobile, progressively
  enhance for Apple Mail.

## 4. Dark mode

- ~35% of opens in dark mode (Litmus 2022, rising) — mainstream, not edge case.
- Three client behaviors: (a) **no change** to email rendering — Apple Mail, Gmail desktop, AOL,
  Yahoo; (b) **partial invert** (only light bgs flip) — Outlook.com, Outlook iOS/Android apps;
  (c) **full invert** (even dark bgs change) — Gmail iOS app, Outlook 2021 / Office 365 Windows.
- `@media (prefers-color-scheme: dark)` supported only in Apple Mail, iOS Mail, Outlook.com.
  Use `color-scheme` + `supported-color-schemes` meta. For Outlook-app image swap use proprietary
  `[data-ogsc]` selectors. Practical rule: pick colors that survive inversion; avoid pure-black/
  pure-white logos; add padding around transparent PNGs. Source: Litmus dark-mode guide.

## 5. Content craft (subject/preheader/CTA/A-B/UTM)

- Subject lines: front-load value, ~30–50 chars / ≤ 9 words for mobile, avoid spam triggers, one
  clear idea. Generate MULTIPLE variants for the user to choose (task requirement). [truelist]
- Preheader: 40–100 chars, complements (does not repeat) the subject. SendPulse uses a *visible*
  preheader bar (per html-rules), not a hidden span.
- CTA: one primary action, button ≥ 44px tap target, action-verb label, high contrast.
- A/B testing: change ONE variable at a time (subject vs CTA vs hero), need adequate sample,
  statistical significance before declaring a winner. Suggest A/B where list size justifies it. [salesforce]
- UTM: lowercase, consistent, no spaces; standard params source/medium/campaign(+term/content).
  Recommend a fixed naming convention file. Append to in-email links, never to unsubscribe. [utm.io]

## 6. Internationalization

- **RTL (Arabic/Hebrew):** set base direction in **markup** (`dir="rtl"`), NOT CSS — W3C says
  direction is semantic and must survive when CSS is stripped (email clients strip CSS).
  `dir="rtl"` at top level cascades; can be set per-table; on a table it reverses column order and
  right-aligns cells. Source: w3.org/International/questions/qa-html-dir. Caveat: Outlook/O365 RTL
  support is quirky (Litmus community threads) — test.
- **Non-latin scripts (CJK, Cyrillic):** charset UTF-8 (already in shell). Use system font stacks
  appropriate per script; don't force a latin web font on CJK. Keep ASCII-only in placehold.co text.
- **Locale:** localize date/number/currency formats and reading order, not just translate strings;
  mirror layout for RTL. Source: omnisend email-localization.

## 7. Design references / inspiration

- Best galleries of REAL production emails: **Really Good Emails** (has categories + some HTML),
  **Milled**, **Email Love**. Pinterest is design pins, not email HTML, and blocks automation.
- **Approach for the skill:** (a) curated in-skill style-direction library (minimal/editorial,
  bold promo, luxury serif, playful, dark premium…) so output isn't cookie-cutter; (b) user brings
  a screenshot/URL → multimodal analysis extracts palette/grid/type/mood → rebuild as valid email
  HTML; (c) point users to RGE/Milled/Email Love to pick a reference to send. No live scraping.

---

## Architecture decisions derived from the above

- Thin SKILL.md router (< 500 lines) = the **beginner quick path** end-to-end + mode detection +
  pointers. Everything deep lives in `references/` (expert path, loaded on demand).
- Reuse Vitya's `html-rules.md` (canonical, from 15 SendPulse templates) verbatim-ish as the HTML
  reference. Add new reference files for the task's new requirements.
- Mode detection (beginner vs expert) inferred from the request; both modes announced to the user.
- Portable: no `allowed-tools` dependence, no Claude-only tool names, generic "save the file +
  show the code block" output instructions.
