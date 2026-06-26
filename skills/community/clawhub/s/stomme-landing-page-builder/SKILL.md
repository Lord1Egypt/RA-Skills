---
name: landing-page-builder
description: Build premium static landing pages with the Stomme/PolyTrader design system. Glass morphism, CSS custom properties, separated copy, responsive, Cloudflare Pages-ready. Use when building a website, landing page, marketing site, or product page. Produces static HTML/CSS/JS with no framework dependencies.
---

# Landing Page Builder

Build premium static landing pages using the proven design system from polytrader.ai.

## Stack
- Static HTML/CSS/JS — no frameworks, no build tools
- CSS custom properties for all theming
- Google Fonts via preconnect
- Cloudflare Pages deployment target

## Procedure

1. **Read content sources** — all copy must come from provided markdown files, never invented
2. **Read the design system reference** — `read references/design-system.md` for the full CSS pattern library
3. **Separate copy from layout** — define ALL text in a `js/copy.js` data file, reference from HTML via `data-copy` attributes or JS injection. This enables i18n later.
4. **Build pages** using the section patterns from the design system
5. **Include**: `_headers` (security headers), `_redirects`, `robots.txt`, `sitemap.xml`, `.gitignore`
6. **Generate validation scripts** — adapt `references/pre-push-check-template.sh` and `references/validate-live-template.js` for the specific site (selectors, locales, CSS vars). Place in `scripts/`. Set up `.githooks/pre-push`. Wire into CI workflow.
7. **Test**: open in browser at desktop AND mobile viewports. Run `bash scripts/pre-push-check.sh`. Verify theme toggle (3 full cycles), lang switcher (all locales), contrast on all interactive elements.
8. **Git init + commit** (hooks path set to `.githooks/`)
9. **Write BUILD-NOTES.md** with Cloudflare Pages deployment instructions

## Design System Principles

The reference file has the full implementation. Key principles:

- **Dual theme** — dark premium default + light mode. Auto-detects `prefers-color-scheme`, user toggle in nav, `localStorage` persistence, inline `<head>` script prevents flash
- **Glass morphism** — `.glass` cards with backdrop-filter, subtle borders, inset shadows — adapts to both themes
- **CSS custom properties** — every color, spacing value, and font through variables. Dark values in `:root`, light overrides in `[data-theme="light"]`
- **Gold/brand accent** — gradient CTAs, accent moments, section kickers. Slightly deepened in light mode for contrast
- **Ambient backgrounds** — layered radial-gradients for depth, NOT solid colors — both themes use them
- **Typography** — Google Fonts (Plus Jakarta Sans or similar geometric sans), tight tracking on headings (-0.035em), generous body line-height (1.75)
- **Interactions** — subtle translateY lifts on hover, gradient buttons with glow shadows
- **Theme toggle** — sun/moon SVG icons in nav, `localStorage` key for persistence, OS change listener

## Section Patterns (in order)

1. **Sticky nav** — frosted glass, pill shape or clean bar, brand + links + theme toggle + CTA
2. **Hero** — large headline, subheadline, dual CTAs (gradient primary + outline secondary), trust signals in glass card grid below
3. **Value proposition** — narrative text section explaining the core differentiator
4. **How it works** — numbered steps (01, 02, 03...) in glass cards, 2-column layout
5. **Features** — alternating layout (text left/visual right, then swap), glass cards
6. **Pricing** — tier cards with ring highlight on featured plan, checklist items with check icons
7. **FAQ** — 2-column glass card grid, question + answer
8. **Bottom CTA** — full-width banner, headline + CTA + supporting line
9. **Footer** — minimal, border-top, brand + links + legal

## Theme Architecture

Every page must include:

1. **Inline `<head>` script** (blocking, before CSS loads) — reads `localStorage` key, falls back to `prefers-color-scheme`, sets `data-theme="light"` on `<html>` if light
2. **`:root`** — dark theme variables (default)
3. **`[data-theme="light"]`** — light theme variable overrides
4. **`--body-bg-gradient`** variable — ambient background through a custom property so it switches with theme
5. **Theme toggle button** in nav with sun/moon SVG icons, visibility driven by CSS `--theme-icon-sun` / `--theme-icon-moon` variables
6. **JS in main.js** — `initTheme()` function: toggle click handler, `localStorage.setItem`, OS `change` listener (respects manual override)
7. **Smooth transitions** — 300ms ease on `color`, `background`, `border-color`, `box-shadow` for themed elements
8. **`--btn-primary-text`** — button text color variable (dark on dark theme where bg is gold, white on light theme)

## File Structure
```
site-root/
├── index.html
├── pricing.html
├── privacy.html
├── terms.html
├── 404.html
├── css/
│   └── style.css          # Full design system + page styles (dark + light themes)
├── js/
│   ├── copy.js            # ALL text content as exportable object
│   └── main.js            # Nav toggle, smooth scroll, theme toggle, minor interactions
├── img/
│   ├── favicon.svg
│   └── og-placeholder.png
├── _headers               # Cloudflare security headers
├── _redirects              # Cloudflare redirects
├── robots.txt
├── sitemap.xml
├── .gitignore
└── BUILD-NOTES.md
```

## Post-Build Validation (MANDATORY)

Every build **must** include a `scripts/` directory with two validation scripts. These are not optional — they are part of the deliverable, like _headers or sitemap.xml.

### 1. `scripts/pre-push-check.sh` — Static pre-push gate
Runs before every `git push` (via `.githooks/pre-push`). Checks:
- All `<script src>` and `<link href>` tags have cache-bust version params (`?v=HASH`)
- No hardcoded hex colors in style.css (all colors via CSS custom properties)
- copy.js and main.js parse without syntax errors
- `applyTheme()` is called on DOM load (not just on toggle click)
- CTA buttons have explicit color override (prevents inheritance from ancestor selectors like `.nav-links a`)
- No `removeAttribute('data-theme')` in any HTML file (must always set theme explicitly)
- Exit 1 on any failure — blocks the push

### 2. `scripts/validate-live.js` — Post-deploy browser validation
Runs in CI after every Cloudflare Pages deploy, using Playwright. Tests at **both** desktop (1440px) and mobile (375px) viewports:
- CSS custom properties resolve to non-empty values
- Contrast ratios on all interactive elements meet WCAG AA (4.5:1 normal text, 3.0:1 large)
- Theme toggle: 3 full cycles (6 clicks), verifies alternation and `localStorage` sync
- Language switcher: all locales produce non-empty hero text and correct `localStorage` value
- All `<script>` and `<link>` tags have version params
- No broken internal links (`href="#"`, empty, or undefined)
- Meta tags present: title, description, og:title

### 3. Git hook setup
```bash
mkdir -p .githooks
echo '#!/bin/bash' > .githooks/pre-push
echo 'bash "$(git rev-parse --show-toplevel)/scripts/pre-push-check.sh"' >> .githooks/pre-push
chmod +x .githooks/pre-push
git config core.hooksPath .githooks
```

### 4. CI workflow must include validation job
The GitHub Actions workflow must have a `validate` job that runs **after** the deploy job:
```yaml
validate:
  needs: deploy
  if: github.event_name == 'push' && github.ref == 'refs/heads/main'
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-node@v4
      with: { node-version: '22' }
    - name: Install Playwright
      run: npx playwright install chromium --with-deps
    - name: Wait for deploy propagation
      run: sleep 30
    - name: Run post-deploy validation
      run: node scripts/validate-live.js https://$DOMAIN
```

**Why this exists:** We shipped a grey-on-red CTA button and a broken theme toggle to production because we relied on visual review alone. Computed style checks catch what eyes miss. Mobile Safari caching broke deploys because we tested desktop only. These scripts encode every lesson into automated gates.

## Constraints
- No Tailwind, no Bootstrap, no React — hand-written CSS
- No external CDN for JS (except Google Fonts CSS)
- No analytics scripts (added separately later)
- No invented features — only what's in the content source files
- All file permissions 0o644 (static files, not secrets)
- Must pass Lighthouse performance >90
