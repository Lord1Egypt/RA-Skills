# Design System Quick Reference — 2026 Edition

Complete reference for building token-based, OKLCH-powered, Liquid-Glass design systems.
Use during Step 3 of the Atom of Thought process and as a CSS copy-paste library.

---

## 1. OKLCH Color System (2026 Standard)

OKLCH is now the mandatory color format. Advantages over HSL:
- **Perceptual uniformity:** equal lightness values look equally bright across all hues
- **Relative colors:** `oklch(from var(--primary) calc(l + 0.2) c h)`
- **Better gradients:** no hue shifts between stops
- **Wide gamut:** accesses P3 colors not possible with HSL

### OKLCH Quick Reference

```
oklch(L C H)
L = lightness 0%–100% (perceptually uniform)
C = chroma    0–0.4    (0 = gray, 0.4 = max vivid)
H = hue       0–360    (same as HSL hue)
```

### Complete Token Blueprints

**Dark — AI/SaaS (Indigo Primary):**
```css
:root {
  --bg:          oklch(8%  0.020 265);
  --surface:     oklch(12% 0.020 265);
  --surface-up:  oklch(16% 0.020 265);
  --fg:          oklch(96% 0.010 95);
  --fg-muted:    oklch(65% 0.010 265);
  --fg-dim:      oklch(45% 0.010 265);
  --primary:     oklch(62% 0.210 285);   /* vivid indigo */
  --primary-up:  oklch(68% 0.210 285);
  --ok:          oklch(62% 0.180 155);
  --warn:        oklch(75% 0.190 65);
  --err:         oklch(62% 0.220 25);
  --border:      oklch(22% 0.015 265);
  --border-faint:oklch(15% 0.010 265);
}
```

**Dark — Developer/Terminal (Green Primary):**
```css
:root {
  --bg:       oklch(7%  0.015 155);
  --surface:  oklch(11% 0.015 155);
  --fg:       oklch(94% 0.008 120);
  --primary:  oklch(68% 0.200 155);   /* terminal green */
}
```

**Dark — Agency/Creative (Warm Copper):**
```css
:root {
  --bg:       oklch(9%  0.018 50);
  --surface:  oklch(13% 0.018 50);
  --fg:       oklch(95% 0.008 80);
  --primary:  oklch(65% 0.160 55);   /* warm copper/amber */
}
```

**Light — Fintech (Professional Blue):**
```css
:root {
  --bg:       oklch(98% 0.005 265);
  --surface:  oklch(100% 0 0);
  --fg:       oklch(18% 0.030 265);
  --fg-muted: oklch(52% 0.015 265);
  --primary:  oklch(48% 0.190 265);  /* deep professional blue */
  --ok:       oklch(48% 0.180 155);
  --err:      oklch(52% 0.220 25);
  --border:   oklch(88% 0.010 265);
}
```

**Light — Wellness/Organic (Sage Green):**
```css
:root {
  --bg:       oklch(97% 0.008 155);
  --surface:  oklch(100% 0 0);
  --fg:       oklch(22% 0.020 155);
  --fg-muted: oklch(55% 0.012 155);
  --primary:  oklch(52% 0.140 155);  /* sage green */
  --accent:   oklch(72% 0.130 60);   /* warm peach */
  --border:   oklch(86% 0.010 155);
}
```

### Relative Colors & Color-Mix (2026)

```css
/* Lighten/darken primary without extra tokens */
--primary-light: oklch(from var(--primary) calc(l + 0.20) c h);
--primary-dim:   oklch(from var(--primary) calc(l - 0.15) c h);

/* Mix colors */
--primary-tint: color-mix(in oklch, var(--primary) 12%, var(--bg));
--glow-color:   color-mix(in oklch, var(--primary) 30%, transparent);

/* Alpha variant — use / for opacity */
--primary-10: oklch(from var(--primary) l c h / 0.10);
--primary-20: oklch(from var(--primary) l c h / 0.20);
```

### Dopamine Palette (Lifestyle / Youth Brands)

```css
/* High-energy, vivid — Y2K inspired, vibrant */
--dopamine-pink:    oklch(72% 0.280 345);
--dopamine-orange:  oklch(75% 0.250 45);
--dopamine-yellow:  oklch(88% 0.200 95);
--dopamine-green:   oklch(72% 0.240 155);
--dopamine-blue:    oklch(65% 0.240 255);
/* Use on: lifestyle brands, beauty, youth apps, social */
/* Never on: fintech, healthcare, enterprise */
```

---

## 2. Typography Systems — 2026

### Font Pairings

| Heading | Body | Vibe | Best For |
|---------|------|------|----------|
| Inter (variable) | Inter | AI Minimalism | AI tools, Perplexity-style SaaS |
| Geist Sans | Geist Mono | Developer-grade | Dev tools, CLIs, code products |
| Cabinet Grotesk | Satoshi | Bold startup | Landing pages, startup SaaS |
| Clash Display | General Sans | Kinetic editorial | Portfolios, creative agencies |
| Space Grotesk | DM Sans | Geometric tech | API products, fintech |
| Playfair Display | Satoshi | Luxury editorial | Agencies, luxury brands |
| JetBrains Mono | Inter | Technical mono | Dev tools, terminal aesthetic |
| Sora | Nunito Sans | Friendly | Wellness, education, consumer |

### Type Scale (Major Third, 1.250)

| Level | Size | Weight | Line Height | Tracking | Use |
|-------|------|--------|-------------|----------|-----|
| Display | clamp(3rem, 1rem+5vw, 7rem) | 800 | 0.92 | -0.045em | Hero headlines |
| H1 | clamp(2.25rem, 1rem+3vw, 4rem) | 700 | 1.05 | -0.030em | Page titles |
| H2 | clamp(1.75rem, 1rem+2vw, 2.75rem) | 650 | 1.15 | -0.020em | Section heads |
| H3 | clamp(1.25rem, 1rem+1vw, 1.75rem) | 600 | 1.25 | -0.010em | Card titles |
| Body | 16–18px | 400 | 1.65 | 0 | Paragraphs |
| Small | 14px | 400 | 1.55 | +0.010em | Secondary |
| Caption | 12px | 500 | 1.45 | +0.020em | Labels, badges |

### Variable Font Axes

```css
/* Inter Variable — precise weight control */
.headline {
  font-family: 'Inter', sans-serif;
  font-variation-settings: 'wght' 820;  /* between 800-900 */
  font-optical-sizing: auto;
}

/* Cabinet Grotesk with tighter optical size */
.display {
  font-family: 'Cabinet Grotesk', sans-serif;
  font-variation-settings: 'wght' 800;
  font-feature-settings: 'kern' 1, 'liga' 1, 'ss01' 1;
}
```

### Kinetic Typography (2026 Trend)

```css
/* Scroll-responsive headline */
.kinetic-headline {
  animation: text-reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 40%;
}
@keyframes text-reveal {
  from { opacity: 0; clip-path: inset(0 100% 0 0); }
  to   { opacity: 1; clip-path: inset(0 0% 0 0); }
}

/* Cursor-responsive headline (JS required) */
.magnetic-text {
  transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
}
```

---

## 3. Liquid Glass System — 2026

### Dark Theme (Standard)

```css
.liquid-glass {
  background: linear-gradient(
    135deg,
    oklch(100% 0 0 / 0.08) 0%,
    oklch(100% 0 0 / 0.02) 100%
  );
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid oklch(100% 0 0 / 0.12);
  box-shadow:
    inset 0 1px 0 oklch(100% 0 0 / 0.15),
    inset 0 -1px 0 oklch(0% 0 0 / 0.08),
    0 8px 32px oklch(0% 0 0 / 0.30),
    0 0 0 1px oklch(100% 0 0 / 0.04);
  border-radius: var(--r);
  transition: border-color var(--dur-base) var(--ease-out),
              box-shadow var(--dur-base) var(--ease-out);
}
.liquid-glass:hover {
  border-color: oklch(100% 0 0 / 0.18);
  box-shadow:
    inset 0 1px 0 oklch(100% 0 0 / 0.20),
    0 12px 40px oklch(0% 0 0 / 0.35),
    0 0 0 1px oklch(100% 0 0 / 0.06);
}
```

### Light Theme

```css
.liquid-glass-light {
  background: oklch(100% 0 0 / 0.82);
  backdrop-filter: blur(24px) saturate(160%);
  border: 1px solid oklch(0% 0 0 / 0.07);
  box-shadow:
    0 1px 3px oklch(0% 0 0 / 0.05),
    0 8px 24px oklch(0% 0 0 / 0.04),
    inset 0 1px 0 oklch(100% 0 0 / 0.95);
}
```

### Warm Agency Tint

```css
.liquid-glass-warm {
  background: linear-gradient(
    135deg,
    oklch(85% 0.08 55 / 0.08) 0%,
    oklch(85% 0.08 55 / 0.01) 100%
  );
  backdrop-filter: blur(20px) saturate(150%);
  border: 1px solid oklch(85% 0.08 55 / 0.14);
  box-shadow: inset 0 1px 0 oklch(85% 0.08 55 / 0.12), 0 8px 32px oklch(0% 0 0 / 0.40);
}
```

### Tailwind Shorthand

```html
<!-- Dark liquid glass -->
<div class="bg-white/5 backdrop-blur-2xl saturate-150 border border-white/10
            shadow-[inset_0_1px_0_oklch(100%_0_0/0.15),0_8px_32px_oklch(0%_0_0/0.3)]
            rounded-xl hover:border-white/[0.18] transition-all duration-250">

<!-- Featured/accent card -->
<div class="backdrop-blur-2xl saturate-150 rounded-2xl
            [background:linear-gradient(135deg,oklch(62%_0.21_285/0.10),oklch(62%_0.21_285/0.03))]
            [border:1px_solid_oklch(62%_0.21_285/0.22)]
            [box-shadow:0_0_32px_oklch(62%_0.21_285/0.15)]">
```

---

## 4. 2026 CSS Native Features

### Scroll-Driven Animations

```css
/* Viewport reveal — replaces Intersection Observer */
.section-reveal {
  animation: fade-up linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 30%;
}

/* Full-page scroll progress bar */
.progress { animation: shrink-x linear; animation-timeline: scroll(root); }
@keyframes shrink-x { to { transform: scaleX(1); } }

/* Sticky header shadow on scroll */
@container scroll-state(stuck) {
  .sticky-nav { box-shadow: 0 2px 20px oklch(0% 0 0 / 0.15); }
}

/* Parallax layer */
.hero-bg {
  animation: parallax linear;
  animation-timeline: scroll(root block);
  animation-range: 0% 100%;
}
@keyframes parallax { to { transform: translateY(-80px); } }
```

### `@starting-style` — Flash-Free Enters (Baseline 2025)

```css
/* Modal enter */
.modal { opacity: 1; transform: scale(1); transition: opacity 200ms, transform 200ms; }
@starting-style { .modal { opacity: 0; transform: scale(0.95); } }

/* Toast / notification */
.toast { opacity: 1; transform: translateY(0); transition: all 300ms; }
@starting-style { .toast { opacity: 0; transform: translateY(16px); } }

/* Dropdown */
.dropdown { opacity: 1; transform: translateY(0) scaleY(1); transform-origin: top; transition: all 200ms; }
@starting-style { .dropdown { opacity: 0; transform: translateY(-8px) scaleY(0.96); } }
```

### CSS Anchor Positioning (Baseline 2025+)

```css
/* Tooltip that repositions automatically */
.trigger   { anchor-name: --tip-trigger; }
.tooltip   {
  position: fixed;
  position-anchor: --tip-trigger;
  inset-area: top;
  margin-bottom: 8px;
  position-try-fallbacks: --bottom, --left, --right;
  max-width: 200px;
}
@position-try --bottom { inset-area: bottom; margin-bottom: 0; margin-top: 8px; }
@position-try --left   { inset-area: left;   margin-bottom: 0; margin-right: 8px; }
@position-try --right  { inset-area: right;  margin-bottom: 0; margin-left: 8px;  }
```

### `sibling-index()` — CSS Stagger (Chrome 2026)

```css
/* Staggered animations without JavaScript */
.stagger-item {
  animation: fade-up var(--dur-slow) var(--ease-expo) both;
  animation-delay: calc(sibling-index() * 60ms);
  animation-timeline: view();
  animation-range: entry 0% cover 30%;
}
```

### View Transitions API

```css
/* Cross-document — 2 lines */
@view-transition { navigation: auto; }

/* Element-level morph */
.hero-image { view-transition-name: hero-image; }
.detail-image { view-transition-name: hero-image; } /* same name = morph */

/* Custom transition timing */
::view-transition-old(root) { animation-duration: 400ms; animation-timing-function: ease-in; }
::view-transition-new(root) { animation-duration: 400ms; animation-timing-function: ease-out; }
```

### CSS `if()` — Adaptive Styles (2026)

```css
/* Conditional transition duration */
.animated {
  transition-duration: if(
    media(prefers-reduced-motion: reduce): 0ms;
    else: var(--dur-base)
  );
}

/* Conditional size */
.btn {
  padding: if(
    container(min-width >= 640px): 0.75rem 1.5rem;
    else: 0.5rem 1rem
  );
}
```

### CSS Grid Lanes / Masonry (Baseline 2026)

```css
/* Native masonry — no JS library */
.masonry {
  display: grid-lanes;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

/* Traditional masonry (Safari + Chrome) */
.masonry-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: masonry;
  gap: 1rem;
}
```

---

## 5. Neo-Brutalism Recipes (2026)

Use for: agencies, creative portfolios, subculture brands — NOT for fintech or enterprise.

```css
/* Neo-brutalist card */
.brutal-card {
  background: oklch(97% 0.005 90);  /* near-white warm */
  border: 2px solid oklch(10% 0.01 0);  /* stark black border */
  box-shadow: 4px 4px 0 oklch(10% 0.01 0);  /* offset shadow — no blur */
  border-radius: 0;  /* no radius — intentional */
  transition: transform 100ms ease, box-shadow 100ms ease;
}
.brutal-card:hover {
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0 oklch(10% 0.01 0);
}

/* Neo-brutalist button */
.brutal-btn {
  background: oklch(85% 0.25 85);   /* bold yellow */
  border: 2px solid oklch(10% 0 0);
  box-shadow: 3px 3px 0 oklch(10% 0 0);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-radius: 0;
}
```

---

## 6. Gradient & Glow Recipes

### OKLCH Gradient Text

```css
.gradient-text {
  background: linear-gradient(
    135deg,
    var(--primary) 0%,
    oklch(from var(--primary) l c calc(h + 40)) 50%,
    oklch(from var(--primary) l c calc(h + 80)) 100%
  );
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
```

### Hero Background Recipes

```css
/* Deep space AI/SaaS */
.hero-ai {
  background:
    radial-gradient(ellipse at 50% 0%, oklch(62% 0.21 285 / 0.15) 0%, transparent 60%),
    radial-gradient(ellipse at 80% 70%, oklch(62% 0.21 285 / 0.06) 0%, transparent 50%),
    var(--bg);
}

/* Warm agency */
.hero-agency {
  background:
    radial-gradient(ellipse at 25% 20%, oklch(65% 0.16 55 / 0.10) 0%, transparent 50%),
    var(--bg);
}

/* Developer terminal */
.hero-dev {
  background:
    radial-gradient(ellipse at 50% 30%, oklch(68% 0.20 155 / 0.07) 0%, transparent 55%),
    linear-gradient(180deg, var(--bg) 0%, oklch(10% 0.015 155) 100%);
}

/* Animated mesh gradient */
.mesh-bg {
  background:
    radial-gradient(at 40% 20%, oklch(62% 0.21 285 / 0.15) 0px, transparent 50%),
    radial-gradient(at 80% 0%, oklch(65% 0.18 305 / 0.10) 0px, transparent 50%),
    radial-gradient(at 0% 50%, oklch(55% 0.20 250 / 0.08) 0px, transparent 50%),
    var(--bg);
  animation: mesh-shift 20s ease-in-out infinite alternate;
}
```

### Glow Effects

```css
/* Button glow */
.btn-glow {
  box-shadow: 0 0 24px oklch(from var(--primary) l c h / 0.40),
              0 0 48px oklch(from var(--primary) l c h / 0.15);
}

/* Card edge glow (featured pricing) */
.card-featured {
  box-shadow:
    0 0 30px oklch(from var(--primary) l c h / 0.20),
    0 8px 32px oklch(0% 0 0 / 0.25);
  border-color: oklch(from var(--primary) l c h / 0.30);
}
```

---

## 7. Grain / Noise Texture

```css
/* Global grain overlay — add to body or :root */
body::after {
  content: '';
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 9999;
  opacity: 0.035;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
/* Use opacity 0.025–0.045. Higher = more visible, lower = subtle warmth */
```

---

## 8. Logo Marquee — Full Implementation

```css
@keyframes marquee { from { transform: translateX(0) } to { transform: translateX(-50%) } }
@keyframes marquee-rev { from { transform: translateX(-50%) } to { transform: translateX(0) } }
.animate-marquee     { animation: marquee 24s linear infinite; }
.animate-marquee-rev { animation: marquee-rev 24s linear infinite; }
.marquee-fade        {
  mask-image: linear-gradient(to right, transparent 0%, black 12%, black 88%, transparent 100%);
}
.animate-marquee:hover { animation-play-state: paused; }
```

```jsx
// React
function Marquee({ items, speed = 24, reverse = false }) {
  return (
    <div className="overflow-hidden marquee-fade py-4">
      <div className={`flex gap-8 whitespace-nowrap ${reverse ? 'animate-marquee-rev' : 'animate-marquee'}`}
           style={{ animationDuration: `${speed}s` }}>
        {[...items, ...items].map((item, i) => (
          <div key={i} className="liquid-glass rounded-full px-5 py-2 shrink-0 text-fg/55 text-sm font-medium">
            {item}
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## 9. Spacing & Responsive Scales

### 4px Spacing Scale

```
4px  (1)  — icon-label gap
8px  (2)  — inline elements
12px (3)  — button internal padding
16px (4)  — standard content gap
24px (6)  — card internal padding
32px (8)  — between card groups
40px (10) — between subsections
48px (12) — section padding (mobile)
64px (16) — section padding (tablet)
80px (20) — section padding (desktop)
96px (24) — generous section padding
128px(32) — hero/feature padding
```

### Responsive Patterns

| Pattern | Desktop | Tablet | Mobile |
|---------|---------|--------|--------|
| Grid columns | 4 | 2 | 1 |
| Section padding | 96–128px | 64–80px | 48–64px |
| Display type | 80–120px | 56–72px | 40–52px |
| Card padding | 32–40px | 24–32px | 20–24px |
| Nav | Full | Full | Hamburger |
| Sidebar | Visible | Collapsible | Drawer |

---

## 10. Accessibility Tokens (WCAG 2.1 AA)

```css
/* Verify contrast: text on background */
/* Body text: min 4.5:1. Large text (18px+ bold, 24px+): min 3:1 */
/* Focus ring: min 3:1 against adjacent colors */
:root {
  --focus-ring: 0 0 0 3px oklch(62% 0.21 285 / 0.5);
}
*:focus-visible {
  outline: none;
  box-shadow: var(--focus-ring);
}

/* Skip link for keyboard users */
.skip-link {
  position: absolute;
  top: -100%;
  left: 1rem;
  background: var(--surface);
  padding: 0.5rem 1rem;
  z-index: 9999;
  border-radius: var(--r);
}
.skip-link:focus { top: 1rem; }
```
