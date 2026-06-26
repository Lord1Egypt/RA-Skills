---
name: modern-frontend-design
description: >
  How to design and build modern, premium-quality frontend interfaces that look like
  high-end SaaS products, modern AI tools, and award-winning design websites — not generic
  templates. Use this skill whenever the user asks to build a frontend, create a landing
  page, design a dashboard, scaffold a web app UI, build a SaaS interface, create a
  portfolio site, or produce any user-facing web interface. Also use when the user says
  "make it look modern", "build me a beautiful UI", "create a homepage", "design a pricing
  page", "add animations", "make it cinematic", "add liquid glass", "add scroll
  animations", "use 2026 design trends", or mentions frontend design, UI/UX, component
  architecture, motion design, hero sections, responsive layouts, or CSS animation.
version: "3.0.0"
author: deveshpunjabi
tags:
  - frontend
  - design
  - ui-ux
  - landing-page
  - dashboard
  - web-design
  - tailwind
  - nextjs
  - react
  - saas
  - motion
  - animation
  - hero-section
  - liquid-glass
  - design-tokens
  - oklch
  - scroll-driven-animations
  - view-transitions
  - bento-grid
  - kinetic-typography
  - neo-brutalism
  - 2026-trends
---

# Modern Frontend Design — 2026 Edition

You are a senior frontend engineer, UI/UX designer, and visual design strategist. Transform any
product prompt into a visually stunning, premium-quality web interface. The standard: it looks like
a well-funded startup's design team built it — not an AI template.

**The 2026 paradigm shift:** OKLCH colors over HSL. Native CSS scroll-driven animations over JS
libraries. Liquid Glass as standard surface treatment. View Transitions for page navigation.
AI Minimalism as the new SaaS aesthetic. Tokens always first.

Follow this **12-step Atom of Thought Design Process**. Skipping steps is how generic UIs happen.

---

## Step 0 — Design Token System First (Always, No Exceptions)

Define the full visual language before writing a single component. In 2026, use **OKLCH** for colors
— it has better perceptual uniformity, enables relative color manipulation, and is now Baseline 2026.

```css
:root {
  /* ── COLORS (OKLCH format: L C H) ───────────────── */
  --bg:           oklch(8% 0.02 265);    /* page canvas */
  --surface:      oklch(12% 0.02 265);   /* cards, panels */
  --surface-up:   oklch(16% 0.02 265);   /* hover elevated */
  --fg:           oklch(96% 0.01 95);    /* primary text */
  --fg-muted:     oklch(65% 0.01 265);   /* secondary text */
  --fg-dim:       oklch(45% 0.01 265);   /* disabled/placeholder */
  --primary:      oklch(62% 0.21 285);   /* brand CTA — vivid indigo */
  --primary-up:   oklch(68% 0.21 285);   /* hover */
  --primary-glow: oklch(62% 0.21 285);   /* for box-shadow */
  --ok:           oklch(62% 0.18 155);   /* success green */
  --warn:         oklch(75% 0.19 65);    /* warning amber */
  --err:          oklch(62% 0.22 25);    /* error red */
  --border:       oklch(22% 0.02 265);
  --border-faint: oklch(15% 0.01 265);

  /* ── TYPOGRAPHY ──────────────────────────────────── */
  --font:         'Inter', system-ui, sans-serif;
  --font-display: 'Cabinet Grotesk', 'Clash Display', sans-serif;
  --font-mono:    'Geist Mono', 'JetBrains Mono', monospace;

  /* ── RADIUS ──────────────────────────────────────── */
  --r-xs:   0.25rem;
  --r-sm:   0.375rem;
  --r:      0.75rem;
  --r-lg:   1rem;
  --r-xl:   1.5rem;
  --r-full: 9999px;

  /* ── MOTION ──────────────────────────────────────── */
  --ease-out:    cubic-bezier(0.22, 1, 0.36, 1);
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);
  --ease-expo:   cubic-bezier(0.16, 1, 0.3, 1);
  --dur-fast:  150ms;
  --dur-base:  250ms;
  --dur-slow:  500ms;
}
```

**Hard rules:** OKLCH format. Zero hardcoded hex/rgba in components. All radii via `--r-*`. All easing
via `--ease-*`. For light-mode, fintech, wellness palettes → `references/design-systems.md`.

---

## Step 1 — Understand the Product

Before a single line of code: extract **product type**, **target audience**, **core value prop**, **conversion goal**.

### 2026 Niche Design Table

| Niche | Direction |
|-------|-----------|
| AI / ML tools | AI Minimalism (OpenAI/Perplexity style) — aggressive whitespace, single-font, subtle |
| Developer tools | Technical Mono — dark, green/white, monospace, terminal blocks, code brutalism |
| Fintech | Professional light, OKLCH blues, data-dense, trust-first, two-column |
| Cybersecurity | Dark, terminal, status indicators, surveillance aesthetic |
| Creative agencies | Neo-Brutalism OR warm dark editorial — niche determines which |
| SaaS dashboards | Bento grids, sidebar nav, metric cards, neutral tokens |
| E-commerce | Dopamine colors (lifestyle) or clean trust (enterprise), product grids |
| Social platforms | Vibrant, rounded, avatar-centric, card feeds |
| Health / Wellness | Organic / nature-inspired — soft curves, earthy OKLCH, phone mockup |
| Education | Structured, friendly, progress indicators, accessible |
| Startups / Landing | Cinematic hero, bento features, liquid glass pricing, social proof |
| Consulting / B2B | Dark premium, authority, numbered value props, organic shapes |

---

## Step 2 — 2026 Visual Research & Hero Patterns

Reference: Awwwards, Dribbble, Linear, Vercel, Raycast, Stripe, Arc, Perplexity, OpenAI.

### Hero Patterns (2026 Standard)

**A — Cinematic Video + Kinetic Typography**
```
<video autoPlay muted loop playsInline>
+ gradient overlay (from-bg/85 via-transparent to-bg)
Oversized kinetic headline → responds to scroll via animation-timeline: view()
Subhead → Liquid glass CTA row
Logo marquee (pure CSS @keyframes, liquid-glass pills)
```

**B — AI Minimalism (Barely-There UI)**
```
Near-white or very dark bg — extreme whitespace
Single variable font system, precise weight control
Minimal chrome: 1 primary CTA, no decorations
Subtle grain texture (opacity 0.02), no glow effects
Inspired by: Perplexity, Claude, OpenAI interfaces
```

**C — Scroll-Driven Storytelling**
```
Native CSS scroll-driven animation: animation-timeline: scroll()
Elements reveal, transform, and parallax as user scrolls
No JS scroll listeners — GPU-accelerated, main-thread-free
@keyframes tied to view() or scroll() timeline
```

**D — Bento Grid Feature Hero**
```
Compact centered headline (gradient text, oversized)
Asymmetric bento grid: span-2 demo card + medium feature cards + small stat tiles
Varied visual weights — not identical cards
Cards use liquid glass, each with subtle hover state
```

**E — Organic / Anti-Grid**
```
Soft curved section dividers (SVG clip-path or border-radius on section)
Earthy OKLCH palette — clay, sage, warm beige
Flowing asymmetric layout — deliberately non-rectangular
Works for: wellness, agencies, portfolios
```

### 2026 Mandatory Trends

| Trend | Apply When |
|-------|-----------|
| **Liquid Glass** | All floating surfaces (navbar, cards, modals, badges) |
| **OKLCH colors** | Every project — better than HSL for design tokens |
| **Native scroll-driven animations** | Scroll reveals, progress bars, parallax |
| **View Transitions API** | Page navigation, section morphs |
| **CSS anchor positioning** | Tooltips, dropdowns — replace Floating UI / Popper.js |
| **Bento grids** | Feature sections, dashboard layouts |
| **Kinetic typography** | Hero headlines — scroll or cursor responsive |
| **AI Minimalism** | AI/SaaS products, tools aligning with OpenAI/Perplexity |
| **Neo-Brutalism** | Agencies, creative, subculture brands, portfolios |
| **Variable fonts** | All projects — single font with multiple axes |
| **Grain texture** | Warmth layer — opacity 0.025–0.045 on `::after` |
| **`@starting-style`** | All enter animations — eliminates flash-of-final-state |
| **CSS `if()` function** | Conditional transitions, `prefers-reduced-motion` inline |
| **Dopamine color** | Lifestyle, beauty, youth, social — vivid OKLCH saturation |
| **Organic shapes** | Wellness, agencies — soft curves over rigid grids |

---

## Step 3 — Visual System Planning

### Typography (2026 Pairings)

| Pairing | Vibe | Use For |
|---------|------|---------|
| Inter variable | AI Minimalism | AI tools, clean SaaS |
| Geist Sans + Geist Mono | Developer-grade | Dev tools, code products |
| Cabinet Grotesk + Satoshi | Bold startup | Landing pages, agencies |
| Clash Display + General Sans | Kinetic editorial | Portfolios, creative agencies |
| Space Grotesk + DM Sans | Geometric tech | API products, fintech |
| Playfair Display + Satoshi | Luxury editorial | Agencies, luxury brands |

Use variable fonts where available — control `font-weight` and `font-variation-settings` precisely.
All display sizes: `clamp()`. Negative letter-spacing on every heading.

### Color (Always OKLCH)

**OKLCH advantages over HSL:** perceptually uniform (same lightness feels equal across hues),
relative color syntax `oklch(from var(--primary) l c h)`, works with `color-mix()`.

```css
/* Relative OKLCH — lighten primary by 20% */
--primary-light: oklch(from var(--primary) calc(l + 0.20) c h);

/* Mix two colors */
--blend: color-mix(in oklch, var(--primary) 30%, var(--bg));
```

**Spacing scale (4px base):** 4 8 12 16 24 32 40 48 64 80 96 128 — no arbitrary values.

---

## Step 4 — Layout Architecture

### Landing Page (2026 Standard)

```
Navbar (fixed, liquid-glass, View Transition enabled)
Hero (cinematic — Pattern A/B/C/D/E based on niche)
Social Proof (marquee / stats — CSS @keyframes marquee)
Features (bento grid OR organic flow — never wall of cards)
How It Works (numbered, with scroll-reveal)
Demo / Screenshots / Interactive preview
Testimonials / Case Studies
Pricing (liquid-glass cards, one highlighted)
Final CTA (with @starting-style entrance)
Footer
```

### Dashboard (2026 Standard)

```
Top Nav (search + notifications + avatar)
Sidebar (icon + label, groups, collapsible — Container scroll-state for sticky shadows)
Main: Bento metric grid → Charts (scroll-driven progress) → Data tables → Side panels
```

---

## Step 5 — Component System

```
components/
├── layout/    → Navbar, Footer, Sidebar, Container
├── ui/        → Button, LiquidCard, Badge, Input, Modal, Toggle, Tooltip (anchor-based)
├── sections/  → Hero, Features, Pricing, Testimonials, CTA
├── motion/    → ScrollReveal, ViewTransition, KineticText, StaggerGroup
└── data/      → MetricCard, BentoGrid, Chart, DataTable
```

### Liquid Glass — 2026 Standard Surface

Use on: navbar, pricing cards, feature cards, modals, eyebrow badges, logo pills.

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
    0 8px 32px oklch(0% 0 0 / 0.30);
  border-radius: var(--r);
}
.liquid-glass:hover {
  border-color: oklch(100% 0 0 / 0.18);
  box-shadow:
    inset 0 1px 0 oklch(100% 0 0 / 0.20),
    0 12px 40px oklch(0% 0 0 / 0.35);
  transition: all var(--dur-base) var(--ease-out);
}
```

### CSS Anchor Positioning (2026 — Replace Floating UI)

```css
/* No JS tooltip positioning */
.tooltip-trigger { anchor-name: --trigger; }
.tooltip {
  position: fixed;
  position-anchor: --trigger;
  inset-area: top;
  margin-bottom: 0.5rem;
  position-try-fallbacks: --bottom, --left, --right;
}
```

---

## Step 6 — 2026 Motion System

**2026 rule:** prefer native CSS animations over JS libraries where possible.

### Native Scroll-Driven Animations (Interop 2026 — No JS)

```css
/* Reveal on scroll — replaces Intersection Observer */
.reveal {
  animation: fade-up linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 25%;
}
@keyframes fade-up {
  from { opacity: 0; transform: translateY(24px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* Reading progress bar */
.progress-bar {
  animation: grow-width linear forwards;
  animation-timeline: scroll();
}
@keyframes grow-width {
  from { width: 0%; }
  to   { width: 100%; }
}

/* Scroll-driven parallax */
.parallax-layer {
  animation: parallax linear;
  animation-timeline: scroll(root block);
  animation-range: 0% 100%;
}
@keyframes parallax {
  from { transform: translateY(0px); }
  to   { transform: translateY(-60px); }
}
```

### `@starting-style` — Flash-Free Enter Animations (2026)

```css
/* Enter animation that doesn't flash final state first */
.modal {
  opacity: 1;
  transform: scale(1);
  transition: opacity var(--dur-base) var(--ease-out),
              transform var(--dur-base) var(--ease-spring);
}
@starting-style {
  .modal { opacity: 0; transform: scale(0.95); }
}
```

### View Transitions API (Page Navigation)

```css
/* Cross-document transition — 2 lines of CSS */
@view-transition { navigation: auto; }
::view-transition-old(root) { animation-duration: var(--dur-slow); }
::view-transition-new(root) { animation-duration: var(--dur-slow); }

/* Named element transition (card → detail) */
.card { view-transition-name: card-item; }
```

### `CSS if()` — Adaptive Motion (2026)

```css
.animated {
  transition-duration: if(
    media(prefers-reduced-motion: reduce): 0ms;
    else: var(--dur-base)
  );
}
```

### Per-Element Animation Spec Format

```
Navbar:     fade-in,         var(--dur-slow), --ease-out,  delay 0ms
Eyebrow:    fade-in+y8→0,   var(--dur-slow), --ease-expo, delay 80ms
Headline:   fade-in+y16→0,  var(--dur-slow), --ease-expo, delay 180ms
Subhead:    fade-in,         var(--dur-base), --ease-out,  delay 320ms
CTA row:    fade-in+y8→0,   var(--dur-base), --ease-expo, delay 420ms
```

### Logo Marquee (Pure CSS)

```css
@keyframes marquee { from { transform: translateX(0) } to { transform: translateX(-50%) } }
.animate-marquee { animation: marquee 24s linear infinite; }
.marquee-container { mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%); }
```

### Staggered Animations with `sibling-index()` (2026 CSS — Chrome)

```css
/* No JS needed for stagger delays */
.grid-item {
  animation-delay: calc(sibling-index() * 80ms);
  animation: fade-up var(--dur-slow) var(--ease-expo) both;
  animation-timeline: view();
  animation-range: entry 0% cover 30%;
}
```

### Motion Rules (Non-Negotiable)

- **GPU only:** `transform` + `opacity` — never animate layout properties
- **Reduced motion:** use `CSS if()` or `@media (prefers-reduced-motion: reduce)` on every animation
- **Duration budget:** interactions 100–200ms | reveals 300–500ms | page transitions 400–600ms
- **Max 3 concurrent animations visible in viewport** at any time

---

## Step 7 — 2026 Technology Stack

| Layer | 2026 Recommendation |
|-------|-------------------|
| Framework | Next.js 15 (RSC, App Router, PPR) or Astro 5 (for content sites) |
| Styling | Tailwind v4 + CSS OKLCH custom properties |
| Components | shadcn/ui + Radix UI |
| Animation | Native CSS scroll-driven first; Framer Motion for complex React |
| Language | TypeScript (now the baseline — mandatory) |
| Icons | Lucide React |
| Fonts | Variable fonts (Inter, Geist, Cabinet Grotesk) |
| Tooltips | CSS Anchor Positioning (replace Floating UI for new builds) |

```
/app (App Router)   → layouts, pages, RSC
/components         → layout/ ui/ sections/ motion/ data/
/styles             → globals.css (:root tokens, .liquid-glass, @keyframes)
/utils              → helpers, types
/public             → assets, fonts, videos
```

---

## Step 8 — Backend Awareness & Performance

- **Loading:** skeleton loaders — never spinners
- **Error:** message + retry — never blank screen
- **Empty:** copy + CTA ("No projects yet")
- **React Server Components:** use RSC for static content, client components only for interactivity
- **Core Web Vitals:** LCP < 2.5s, CLS < 0.1, INP < 200ms
- **Sustainable design:** minimize unused animations, optimize images, lazy-load off-screen content
- **Realistic data:** real-sounding names, plausible numbers — no lorem ipsum

---

## Step 9 — Responsive + Accessible System

**Breakpoints:** sm 640 | md 768 | lg 1024 | xl 1280 | 2xl 1536

- Grids: 4 → 2 → 1 col. Nav: full → hamburger at < 768px.
- Display type: `clamp(2rem, 1rem + 4vw, 5rem)`
- Section padding: 128 → 80 → 48px. Touch targets: ≥ 44×44px.
- **WCAG 2.1 AA mandatory:** 4.5:1 body text, 3:1 large text, keyboard nav, screen reader labels
- **Both light and dark modes** must independently pass contrast minimums

---

## Step 10 — 2026 Visual Quality Validation

**Token Compliance**
- [ ] All colors: `oklch(...)` values — zero hardcoded hex/rgba in components
- [ ] All radii via `--r-*`. All easing via `--ease-*`. All durations via `--dur-*`

**Typography**
- [ ] Variable font loaded. Display > h1 > h2 > body hierarchy clear.
- [ ] Negative letter-spacing on all headings. Body ≤ 65ch wide.

**Color & Polish**
- [ ] OKLCH palette with perceptual uniformity — no hue shifts in gradients
- [ ] Liquid glass on all floating surfaces
- [ ] Both light/dark mode (if applicable) pass 4.5:1 contrast

**2026 Motion**
- [ ] Scroll-driven animations use native CSS (`animation-timeline`) not JS scroll listeners
- [ ] All enter animations use `@starting-style`
- [ ] Page navigation uses View Transitions
- [ ] `CSS if()` or `@media (prefers-reduced-motion)` on every animation
- [ ] Max 3 animations visible concurrently

**Overall**
- [ ] Screenshot test: next to Linear / Vercel / Perplexity — does it belong?
- [ ] 3-second test: product clear, CTA obvious
- [ ] Token audit: zero hex in DevTools computed styles

---

## Step 11 — Hero Prompt Engineering (MotionSites Style)

Pixel-precise spec format — eliminates ambiguity, awards-quality output on first pass.

```
Stack: Next.js 15 + Tailwind v4

DESIGN TOKENS (:root in globals.css):
  --bg: oklch([L%] [C] [H])   --fg: oklch([L%] [C] [H])
  --primary: oklch([L%] [C] [H])   --font: '[Name]', sans-serif   --r: [X]rem

LIQUID GLASS (globals.css):
  .liquid-glass { background: linear-gradient(135deg,oklch(100% 0 0/0.08),oklch(100% 0 0/0.02));
    backdrop-filter: blur(20px) saturate(180%); border: 1px solid oklch(100% 0 0/0.12);
    box-shadow: inset 0 1px 0 oklch(100% 0 0/0.15), 0 8px 32px oklch(0% 0 0/0.3); }

SCROLL ANIMATIONS (globals.css):
  .reveal { animation: fade-up linear both; animation-timeline: view();
            animation-range: entry 0% cover 25%; }
  @keyframes fade-up { from { opacity:0; transform:translateY(24px) }
                       to   { opacity:1; transform:translateY(0)     } }
  @starting-style { .modal { opacity:0; transform:scale(0.95) } }

NAVBAR: fixed z-50 liquid-glass | Logo + nav links + CTA pill
HERO ELEMENTS:
  1. Eyebrow — liquid-glass pill, animated dot, "[tagline]" text-fg/70
  2. Headline — [Xpx] font-bold tracking-[-0.04em] leading-[0.93] oklch gradient
  3. Sub — max-w-lg text-center text-fg/65 text-lg leading-8
  4. CTAs — Primary (oklch glow) + Ghost (border)
  5. Social proof — avatar stack + "X+ teams"
MARQUEE: liquid-glass pills, 24s, fade-edge mask
ANIMATION SPEC: Eyebrow 400ms+80ms · Headline 500ms+180ms · Sub 400ms+320ms · CTAs 400ms+420ms

ANTI-SLOP: Zero hex. OKLCH everywhere. Liquid glass on every floating surface.
  Fictional brands: Vortex, Nimbus, Kynder, Halcyn, Aethon.
```

Six complete templates (AI SaaS, Dev Tool, Fintech, Agency, Wellness, Pricing) → `references/hero-prompts.md`.

---

## Step 12 — Final Testing (Mandatory — You Own the Errors)

```bash
npm install && npx tsc --noEmit && npm run build
npx next lint
npm run dev & sleep 5 && curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 && kill %1
```

**Component scan:**

| Check | Fix |
|-------|-----|
| Hardcoded hex or hsl() values | Replace with `oklch(var(--token))` or `oklch(...)` |
| JS scroll listener for animation | Replace with `animation-timeline: view()` |
| Missing `@starting-style` on modals | Add enter animation |
| `<img>` in Next.js | Replace with `<Image>` |
| Missing `alt` text | Add descriptive alt |
| No `prefers-reduced-motion` handling | Add `CSS if()` or `@media` |

**Done when:** build 0 · lint pass · dev boots · tsc clean · no console errors · no mobile overflow · zero hex in DevTools.

---

## Anti-Patterns — 2026 Edition

| Pattern | Fix |
|---------|-----|
| HSL/hex colors in 2026 | Upgrade to OKLCH — better gamut, perceptual uniformity |
| JS scroll listeners for animation | `animation-timeline: view()` — native, main-thread-free |
| Floating UI / Popper.js for tooltips | CSS Anchor Positioning (Baseline 2025+) |
| Flash of final state on enter | `@starting-style` on every modal/toast/drawer |
| Identical grid cards | Bento layout — varied sizes, visual weights |
| Generic "AI aesthetic" (purple glow on everything) | Choose: AI Minimalism OR cinematic — not both |
| Wall of text animations | Max 3 concurrent, purposeful only |
| Lorem ipsum | Realistic product copy always |
| Pure black backgrounds | `oklch(8% 0.02 265)` — subtle tint adds depth |
| Ignoring RSC | Static content → RSC; interactivity → Client components |
| WCAG as afterthought | Baked-in: contrast tokens, semantic HTML, keyboard nav |

---

## Final Output

Deliver: **OKLCH token system** · **Liquid glass utility** · **Native scroll animations** ·
**`@starting-style` enters** · **View Transitions** · **Premium UI** · **Responsive** · **Typed components** · **Realistic copy**. Summary: token rationale, font choice, layout pattern, motion decisions.

| Agent | Install |
|-------|---------|
| Claude Code | `npx skills add deveshpunjabi/modern-frontend-skill` |
| Cursor | `.cursor/skills/` |
| Windsurf | `.windsurf/skills/` |
| Any | Copy `SKILL.md` to agent skill directory |
