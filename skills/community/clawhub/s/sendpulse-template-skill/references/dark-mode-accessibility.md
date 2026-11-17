# Dark Mode, Accessibility & Cross-Client Safety

> Read this for dark-mode handling, accessibility, and which HTML/CSS is safe across clients.
> Data: caniemail.com (~307 features tracked across 25+ clients), Litmus dark-mode & rendering guides.

## Table of Contents
1. Cross-client reality (code to the intersection)
2. Dark mode (≈35% of opens)
3. Accessibility
4. Pre-send checklist

---

## 1. Cross-client reality — code to the intersection

caniemail.com feature support (approximate, per client):
- **Apple Mail** macOS ~287/307, iOS ~282/305 — best; modern CSS mostly safe **here only**.
- **Gmail** desktop webmail ~154/307; Gmail mobile apps ~111/307 — about half / a third.
- **Outlook Windows desktop** ~59/306 — worst major client (uses Word's rendering engine).

**Rule:** code to the *intersection* of Outlook-desktop + Gmail-mobile; progressively enhance for
Apple Mail. Concretely this is exactly why the skill uses:
- Table-based layout (no flex/grid/float), inline styles, 6-digit hex.
- MSO conditional comments + VML for Outlook backgrounds/buttons.
- A bulletproof CSS-table button instead of styled `<div>`/`<a>` blocks.
- `<table class="separator">` rows for spacing instead of `margin`.
- Pixel widths on columns; single-column reflow on mobile via the media query in the shell.

When tempted by a fancy CSS feature, assume Outlook & Gmail-app **don't** support it and provide a
graceful fallback (e.g. square corners where `border-radius` is ignored).

## 2. Dark mode — ~35% of opens, treat as mainstream

Clients fall into **three behaviors**:
1. **No change** to email rendering — Apple Mail, Gmail desktop, AOL, Yahoo. (Your colors stay.)
2. **Partial invert** — only light backgrounds flip dark, dark text flips light — Outlook.com,
   Outlook iOS/Android apps.
3. **Full invert** — even already-dark backgrounds change — Gmail iOS app, Outlook 2021 / Office 365
   on Windows.

**`@media (prefers-color-scheme: dark)`** is supported only in Apple Mail, iOS Mail, Outlook.com —
so dark-specific styles **cannot** be relied on universally. For Outlook-app image swaps use the
proprietary `[data-ogsc]` / `[data-ogsb]` attribute selectors.

**Practical, client-agnostic rules (do these by default):**
- Add the meta hints in the shell head area:
  ```html
  <meta name="color-scheme" content="light dark">
  <meta name="supported-color-schemes" content="light dark">
  ```
- Pick colors that **survive inversion**: avoid pure white (`#ffffff`) and pure black (`#000000`)
  as the only contrast pair — near-white/near-black behave better.
- **Logos & icons:** don't use pure-black logos on transparent PNG (vanish on dark). Add a small
  white/light padding plate behind transparent logos, or use a PNG with a safe background.
- Don't rely on background images to carry text contrast.
- For brand-critical color blocks, wrap them so partial-invert clients keep them readable.
- Optional enhancement (Apple/iOS/Outlook.com only): supply dark-mode overrides via the media query,
  but never depend on them for legibility.

## 3. Accessibility

- **Semantic order:** content reads top-to-bottom in source order (table layout already does this).
- **Alt text** on every `<img>` (empty `alt=""` only for purely decorative images).
- **Color contrast** ≥ 4.5:1 for body text, ≥ 3:1 for large text (check both light & dark).
- **Real text, not images of text** — keeps it readable, translatable, and screen-reader friendly.
- **Link text is meaningful** ("track your order", not "click here").
- **Font size** ≥ 14px body, ≥ 16px on mobile is comfortable.
- **`role="presentation"`** on layout tables (suppresses table semantics for screen readers).
- **Language attribute** on the wrapper (`lang="..."`) helps screen readers pronounce correctly.
- Don't convey meaning by color alone (e.g. "items in red") — add a label.

## 4. Pre-send checklist

- [ ] Renders in Outlook desktop (tables, VML button/bg, square-corner fallback)
- [ ] Renders in Gmail app (no unsupported CSS, no `<style>`-only critical layout)
- [ ] Readable in dark mode (no vanished logo, contrast holds under invert)
- [ ] All images have alt text; not an all-image email
- [ ] Single-column reflow works on mobile
- [ ] Contrast ratios pass; body ≥ 14px
- [ ] Unsubscribe + physical address present
