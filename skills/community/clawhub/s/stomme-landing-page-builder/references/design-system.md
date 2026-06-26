# Design System Reference — Premium Landing Pages

Extracted from the polytrader.ai production landing page. Adapt colors to brand; keep the structural patterns.
Supports dual light/dark themes with auto browser detection, manual toggle, and localStorage persistence.

## CSS Custom Properties

Every value goes through a custom property. Never hardcode colors or spacing.
Dark theme in `:root` (default). Light theme overrides in `[data-theme="light"]`.

```css
:root {
  /* Background layers — dark premium */
  --bg-primary: #0a0a0c;
  --bg-secondary: #121216;
  --bg-tertiary: #1a1a1f;
  --bg-card: rgba(255, 255, 255, 0.04);
  --bg-card-hover: rgba(255, 255, 255, 0.08);
  --bg-elevated: rgba(255, 255, 255, 0.06);

  /* Borders — subtle, rgba-based */
  --border-subtle: rgba(255, 255, 255, 0.08);
  --border-medium: rgba(255, 255, 255, 0.12);
  --border-focus: rgba(var(--accent-rgb), 0.4);

  /* Glass effect */
  --glass-bg: rgba(15, 16, 18, 0.8);
  --glass-border: rgba(255, 255, 255, 0.06);

  /* Text — high contrast on dark */
  --text-primary: #fafafa;
  --text-secondary: #a0a0a8;
  --text-muted: #606068;

  /* Accent — replace with brand color */
  --accent: #e4b45c;          /* PolyTrader: gold. Stomme: use brand amber/gold */
  --accent-bright: #f0c96e;
  --accent-soft: rgba(228, 180, 92, 0.12);
  --accent-glow: rgba(228, 180, 92, 0.2);
  --accent-rgb: 228, 180, 92; /* For rgba() usage */

  /* Button text — dark on gold gradient button in dark mode */
  --btn-primary-text: #0a0a0c;

  /* Semantic */
  --green: #10b981;
  --red: #f43f5e;
  --blue: #3b82f6;

  /* Gradients */
  --gradient-accent: linear-gradient(135deg, var(--accent-bright) 0%, var(--accent) 50%, color-mix(in srgb, var(--accent), #000 15%) 100%);
  --gradient-card: linear-gradient(145deg, rgba(255,255,255,0.035) 0%, rgba(255,255,255,0.01) 100%);
  --gradient-hero-ambient: radial-gradient(ellipse 60% 50% at 50% 0%, var(--accent-soft) 0%, transparent 60%);

  /* Body ambient background — through variable so it switches with theme */
  --body-bg-gradient:
    radial-gradient(circle at top left, var(--accent-soft), transparent 24rem),
    radial-gradient(circle at 82% 16%, rgba(var(--accent-rgb), 0.08), transparent 22rem),
    linear-gradient(180deg, var(--bg-secondary), var(--bg-primary));

  /* Typography */
  --font-heading: 'Plus Jakarta Sans', 'SF Pro Display', system-ui, sans-serif;
  --font-body: 'Plus Jakarta Sans', 'SF Pro Text', system-ui, sans-serif;
  --font-mono: 'DM Mono', 'JetBrains Mono', monospace;

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;
  --space-3xl: 64px;
  --space-4xl: 96px;

  /* Radius */
  --radius-sm: 10px;
  --radius-md: 20px;
  --radius-lg: 28px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-card: 0 24px 64px rgba(0, 0, 0, 0.22);
  --shadow-button: 0 18px 50px var(--accent-glow);

  /* Max widths */
  --max-width: 1160px;
  --max-width-narrow: 720px;

  /* Theme toggle icon visibility */
  --theme-icon-sun: block;
  --theme-icon-moon: none;

  color-scheme: dark;
}
```

## Light Theme Overrides

Override only what changes — structure, spacing, radius, fonts stay the same.
Light mode: warm birch/parchment bg, deep navy text, slightly deepened accent for contrast.

```css
[data-theme="light"] {
  --bg-primary: #f7f3ed;
  --bg-secondary: #efe9e0;
  --bg-tertiary: #e6dfd5;
  --bg-card: rgba(0, 0, 0, 0.03);
  --bg-card-hover: rgba(0, 0, 0, 0.06);
  --bg-elevated: rgba(0, 0, 0, 0.04);

  --border-subtle: rgba(0, 0, 0, 0.08);
  --border-medium: rgba(0, 0, 0, 0.12);
  --border-focus: rgba(var(--accent-rgb), 0.35);

  --glass-bg: rgba(247, 243, 237, 0.85);
  --glass-border: rgba(0, 0, 0, 0.06);

  --text-primary: #0d1b2a;
  --text-secondary: #4a4540;
  --text-muted: #8a8580;

  /* Accent deepened for readability on light bg */
  --accent: #b8872e;
  --accent-bright: #d4a24c;
  --accent-soft: rgba(184, 135, 46, 0.1);
  --accent-glow: rgba(184, 135, 46, 0.15);
  --accent-rgb: 184, 135, 46;

  /* White text on gold gradient button in light mode */
  --btn-primary-text: #ffffff;

  --gradient-accent: linear-gradient(135deg, var(--accent-bright) 0%, var(--accent) 50%, color-mix(in srgb, var(--accent), #000 10%) 100%);
  --gradient-card: linear-gradient(145deg, rgba(0,0,0,0.02) 0%, rgba(0,0,0,0.005) 100%);
  --gradient-hero-ambient: radial-gradient(ellipse 60% 50% at 50% 0%, var(--accent-soft) 0%, transparent 60%);

  --body-bg-gradient:
    radial-gradient(circle at top left, var(--accent-soft), transparent 24rem),
    radial-gradient(circle at 82% 16%, rgba(var(--accent-rgb), 0.05), transparent 22rem),
    linear-gradient(180deg, var(--bg-secondary), var(--bg-primary));

  --shadow-card: 0 24px 64px rgba(0, 0, 0, 0.06);
  --shadow-button: 0 18px 50px var(--accent-glow);

  --theme-icon-sun: none;
  --theme-icon-moon: block;

  color-scheme: light;
}
```

## Glass Morphism

The signature component. Used for cards, nav, feature boxes.

```css
.glass {
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.03), rgba(255, 255, 255, 0.01)),
    var(--glass-bg);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border: 1px solid var(--glass-border);
  border-radius: var(--radius-lg);
  box-shadow:
    inset 0 1px 0 0 rgba(255, 255, 255, 0.06),
    var(--shadow-card);
}
```

## Premium Panel (Lux Panel)

Elevated glass with accent gradient glow. Used for featured pricing, hero pricing card.

```css
.lux-panel {
  position: relative;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.04), rgba(255, 255, 255, 0.015)),
    var(--glass-bg);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  border: 1px solid rgba(var(--accent-rgb), 0.18);
  border-radius: var(--radius-lg);
  box-shadow:
    inset 0 1px 0 0 rgba(255, 255, 255, 0.06),
    0 0 80px -20px var(--accent-soft),
    var(--shadow-card);
  overflow: hidden;
}

.lux-panel::before {
  content: '';
  position: absolute;
  inset: -1px;
  border-radius: inherit;
  background: linear-gradient(135deg, rgba(var(--accent-rgb), 0.08) 0%, transparent 50%);
  pointer-events: none;
  z-index: 0;
}
```

## Ambient Page Background

Uses `--body-bg-gradient` variable so it switches automatically with theme.

```css
body {
  background: var(--body-bg-gradient);
  background-attachment: fixed;
  color: var(--text-primary);
  font-family: var(--font-body);
  -webkit-font-smoothing: antialiased;
  transition: background 300ms ease, color 300ms ease;
}
```

## Theme Toggle Button

Sun/moon toggle in the nav bar. Icon visibility driven by CSS variables — no JS class toggling needed.

```css
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  padding: 0;
  background: var(--bg-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-full);
  color: var(--text-secondary);
  cursor: pointer;
  transition: color 200ms ease, background 200ms ease, border-color 200ms ease;
  flex-shrink: 0;
}

.theme-toggle:hover {
  color: var(--text-primary);
  background: var(--bg-card-hover);
  border-color: var(--border-medium);
}

.theme-toggle svg { width: 18px; height: 18px; }
.theme-toggle .icon-sun { display: var(--theme-icon-sun); }
.theme-toggle .icon-moon { display: var(--theme-icon-moon); }
```

### HTML (in nav, before hamburger toggle)
```html
<button class="theme-toggle" aria-label="Toggle light/dark theme" title="Toggle theme">
  <svg class="icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>
  <svg class="icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1111.21 3 7 7 0 0021 12.79z"/></svg>
</button>
```

## Flash Prevention

Add this blocking inline script inside `<head>`, before CSS loads. Reads stored preference or detects OS setting. Prevents the wrong theme from rendering even for one frame.

```html
<script>
  (function(){
    var t = localStorage.getItem('stomme-theme');
    if (!t) t = window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
    if (t === 'light') document.documentElement.setAttribute('data-theme', 'light');
  })();
</script>
```

Replace `'stomme-theme'` with an appropriate brand-specific key (e.g. `'mysite-theme'`).

## Theme Toggle JS

Add to `main.js`:

```js
function initTheme() {
  const toggle = document.querySelector('.theme-toggle');
  if (!toggle) return;

  const KEY = 'stomme-theme'; // match the key in the head script

  function getEffectiveTheme() {
    const stored = localStorage.getItem(KEY);
    if (stored) return stored;
    return window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark';
  }

  function applyTheme(theme) {
    if (theme === 'light') {
      document.documentElement.setAttribute('data-theme', 'light');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }
  }

  toggle.addEventListener('click', () => {
    const next = getEffectiveTheme() === 'dark' ? 'light' : 'dark';
    localStorage.setItem(KEY, next);
    applyTheme(next);
  });

  // Respect OS changes when user hasn't manually set preference
  window.matchMedia('(prefers-color-scheme: light)').addEventListener('change', e => {
    if (!localStorage.getItem(KEY)) {
      applyTheme(e.matches ? 'light' : 'dark');
    }
  });
}
```

Call `initTheme()` in the DOMContentLoaded handler.

## Smooth Theme Transitions

Add transitions on key themed elements so the switch isn't jarring:

```css
.glass,
.lux-panel,
.nav-bar,
h1, h2, h3, h4, p, a, span,
.section-kicker,
.btn-secondary {
  transition: color 300ms ease, background 300ms ease, border-color 300ms ease, box-shadow 300ms ease;
}
```

## Typography

```css
h1, h2, h3, h4 {
  font-family: var(--font-heading);
  font-weight: 700;
  color: var(--text-primary);
}

h1 {
  font-size: clamp(2.2rem, 9.4vw, 4.1rem);
  line-height: 1.04;
  letter-spacing: -0.055em;
}

h2 {
  font-size: clamp(2rem, 5vw, 2.55rem);
  line-height: 1.12;
  letter-spacing: -0.035em;
}

h3 {
  font-size: clamp(1.15rem, 2.5vw, 1.45rem);
  line-height: 1.16;
  letter-spacing: -0.025em;
}

p {
  color: var(--text-secondary);
  line-height: 1.75;
  max-width: 65ch;
}

/* Section kicker — small uppercase label above headings */
.section-kicker {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.6875rem;   /* 11px */
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.18em;
  color: var(--accent);
  opacity: 0.8;
}
```

## Buttons

```css
/* Primary — gradient with glow */
.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 0.875rem 1.75rem;
  font-family: var(--font-heading);
  font-size: 0.875rem;
  font-weight: 700;
  color: var(--btn-primary-text);
  background: var(--gradient-accent);
  border: none;
  border-radius: var(--radius-full);
  box-shadow: var(--shadow-button);
  cursor: pointer;
  transition: transform 200ms ease;
  text-decoration: none;
}

.btn-primary:hover {
  transform: translateY(-2px);
}

/* Secondary outline */
.btn-secondary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 0.875rem 1.5rem;
  font-family: var(--font-heading);
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--text-primary);
  background: transparent;
  border: 2px solid var(--border-medium);
  border-radius: var(--radius-full);
  cursor: pointer;
  transition: background-color 200ms ease, border-color 200ms ease;
  text-decoration: none;
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--text-primary);
}
```

## Sticky Nav

Includes theme toggle button between links and hamburger.

```css
nav {
  position: sticky;
  top: 0;
  z-index: 30;
  margin-bottom: var(--space-lg);
}

.nav-bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-full);
  border: 1px solid var(--border-subtle);
  background: var(--glass-bg);
  backdrop-filter: blur(18px);
  -webkit-backdrop-filter: blur(18px);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.18);
}

.nav-brand {
  font-family: var(--font-heading);
  font-weight: 700;
  font-size: 1rem;
  color: var(--text-primary);
  letter-spacing: -0.03em;
}

.nav-links a {
  font-size: 0.875rem;
  color: var(--text-secondary);
  text-decoration: none;
  transition: color 200ms ease;
}

.nav-links a:hover {
  color: var(--text-primary);
}
```

### Nav HTML structure
```html
<nav role="navigation" aria-label="Main navigation">
  <div class="nav-bar">
    <a href="/" class="nav-brand">brand</a>
    <ul class="nav-links">
      <li><a href="#features">Features</a></li>
      <li><a href="/pricing.html">Pricing</a></li>
      <li><a href="..." class="btn-primary nav-cta">Get started</a></li>
    </ul>
    <!-- Theme toggle: place BEFORE hamburger toggle -->
    <button class="theme-toggle" aria-label="Toggle theme">...</button>
    <button class="nav-toggle" aria-label="Toggle menu">...</button>
  </div>
</nav>
```

## Section Layout Patterns

### Hero
- Full-width, centered text
- h1 with tight tracking, p with max-width 44rem
- Two CTAs side by side (primary gradient + secondary outline)
- Below: glass card grid with 3 trust/value signals (icon + title + desc)

### How It Works
- Section kicker + h2 + intro paragraph
- 2-column grid: left has numbered glass cards (01, 02...), right has lux-panel feature highlight
- Number badges: 44px circles, bg-elevated, bold text

### Pricing
- Section kicker + h2 + intro
- 3-column grid (or 2 + sidebar): tier cards as glass panels
- Featured tier: lux-panel with ring-2 accent highlight
- Checklist items with ✓ icon in accent-green

### FAQ
- Section kicker + h2
- 2-column grid of glass cards
- h3 question + p answer per card

### Footer
- border-top separator
- 2-column: brand + tagline left, nav links right
- Bottom row: legal entity + privacy/terms links
- Minimal, no decoration

## Interactions

```css
/* Card hover lift */
.glass:hover,
.card:hover {
  transform: translateY(-2px);
  transition: transform 200ms ease;
}

/* Selected state — pricing */
.tier-card.selected {
  outline: 2px solid var(--accent);
  outline-offset: -2px;
}
```

## Responsive Breakpoints

```css
/* Tablet */
@media (max-width: 1024px) {
  .grid-3 { grid-template-columns: 1fr; }
  .grid-2 { grid-template-columns: 1fr; }
}

/* Mobile */
@media (max-width: 640px) {
  h1 { font-size: 2.2rem; }
  .nav-links { display: none; }
  /* Show hamburger */
}
```

## Separated Copy Pattern

All text content lives in js/copy.js:

```js
const COPY = {
  nav: { brand: 'stomme.ai', features: 'Features', pricing: 'Pricing' },
  hero: {
    headline: 'Your personal AI agent.\nOn your Mac. Without the complexity.',
    subtitle: '...',
    ctaPrimary: 'Get started — 50% off your first month',
    ctaSecondary: 'See how it works',
  },
  // ... all sections
};
export default COPY;
```

Then in HTML, reference via data attributes or JS hydration:
```html
<h1 data-copy="hero.headline"></h1>
<script type="module">
  import COPY from '/js/copy.js';
  document.querySelectorAll('[data-copy]').forEach(el => {
    const keys = el.dataset.copy.split('.');
    let val = COPY;
    for (const k of keys) val = val[k];
    el.textContent = val;
  });
</script>
```

## Google Fonts Loading

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
```

## Cloudflare Pages Files

### _headers
```
/*
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  X-XSS-Protection: 1; mode=block
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()

/css/*
  Cache-Control: public, max-age=31536000, immutable

/js/*
  Cache-Control: public, max-age=31536000, immutable

/img/*
  Cache-Control: public, max-age=31536000, immutable
```

### _redirects
```
/home    /    301
/index   /    301
```
