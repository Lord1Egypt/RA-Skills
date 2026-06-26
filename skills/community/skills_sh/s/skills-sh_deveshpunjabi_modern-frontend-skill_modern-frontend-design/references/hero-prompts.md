# Hero Prompt Templates — 2026 Edition

Six production-ready, MotionSites-style hero templates. Each is pixel-precise:
OKLCH tokens, Liquid Glass utility, native CSS scroll animations, `@starting-style`, component anatomy.
Copy, fill brackets, paste into any AI coding agent. First-generation quality.

---

## Template 1 — AI SaaS (AI Minimalism, Dark, Video Background)

**Niche:** AI writing tools, ML platforms, LLM products, automation SaaS
**Vibe:** Perplexity × Linear — restrained, intelligent, single-font

```
Build a cinematic AI SaaS hero.
Stack: Next.js 15 + Tailwind v4 + Framer Motion

═══════════════════════════════════════
OKLCH DESIGN TOKENS (globals.css :root)
═══════════════════════════════════════
--bg:          oklch(8%  0.020 265);
--surface:     oklch(12% 0.020 265);
--surface-up:  oklch(16% 0.020 265);
--fg:          oklch(96% 0.010 95);
--fg-muted:    oklch(65% 0.010 265);
--fg-dim:      oklch(45% 0.010 265);
--primary:     oklch(62% 0.210 285);
--primary-up:  oklch(68% 0.210 285);
--border:      oklch(22% 0.015 265);
--font:        'Inter', system-ui, sans-serif;
--r:           0.75rem;
--ease-out:    cubic-bezier(0.22, 1, 0.36, 1);
--ease-expo:   cubic-bezier(0.16, 1, 0.30, 1);
--dur-base:    250ms;
--dur-slow:    500ms;

═══════════════════════════════════════
LIQUID GLASS UTILITY (globals.css)
═══════════════════════════════════════
.liquid-glass {
  background: linear-gradient(135deg, oklch(100% 0 0/0.08), oklch(100% 0 0/0.02));
  backdrop-filter: blur(20px) saturate(180%);
  -webkit-backdrop-filter: blur(20px) saturate(180%);
  border: 1px solid oklch(100% 0 0/0.12);
  box-shadow: inset 0 1px 0 oklch(100% 0 0/0.15), 0 8px 32px oklch(0% 0 0/0.3);
  border-radius: var(--r);
}

═══════════════════════════════════════
NATIVE CSS SCROLL + ENTER ANIMATIONS (globals.css)
═══════════════════════════════════════
.reveal {
  animation: fade-up linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 30%;
}
@keyframes fade-up { from { opacity:0; transform:translateY(24px) } to { opacity:1; transform:translateY(0) } }
@keyframes marquee { from { transform:translateX(0) } to { transform:translateX(-50%) } }
.animate-marquee { animation: marquee 24s linear infinite; }
.marquee-fade { mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%); }
@starting-style { .modal { opacity: 0; transform: scale(0.95); } }
@view-transition { navigation: auto; }

═══════════════════════════════════════
GRAIN OVERLAY (globals.css body::after)
═══════════════════════════════════════
opacity: 0.032; z-index: 9999; pointer-events: none; fixed inset-0;
background-image: SVG fractalNoise filter (see design-systems.md)

═══════════════════════════════════════
NAVBAR
═══════════════════════════════════════
Position: fixed top-0 z-50 w-full
Style: liquid-glass px-6 py-4 flex items-center justify-between
Left: liquid-glass icon (8×8 rounded-lg, primary gradient) + "Lumina" font-semibold var(--fg)
Center: ["Features", "Pricing", "Changelog", "Docs"] text-fg/60 text-sm gap-8 hidden md:flex
Right: ["Sign in" ghost sm] + ["Start free →" primary rounded-full px-4 py-2 text-sm
       box-shadow: 0 0 24px oklch(from var(--primary) l c h / 0.4)]
Bottom divider: h-px bg-gradient-to-r from-transparent via-fg/15 to-transparent

═══════════════════════════════════════
HERO SECTION
═══════════════════════════════════════
Layout: relative min-h-screen overflow-hidden flex flex-col

VIDEO BACKGROUND:
  <video autoPlay muted loop playsInline className="absolute inset-0 w-full h-full object-cover" />
  Overlay: absolute inset-0 bg-gradient-to-b from-bg/85 via-transparent to-bg
  Vignette: absolute inset-0 bg-[radial-gradient(ellipse_at_center,transparent_40%,oklch(8%_0.02_265/0.6)_100%)]

CONTENT: z-10 flex-1 flex flex-col items-center justify-center px-4 pt-24 pb-16 text-center

ELEMENTS (Framer Motion stagger, all ease-expo):
  1. Eyebrow badge (delay 0ms, 400ms)
     liquid-glass rounded-full px-4 py-1.5 inline-flex items-center gap-2 mb-8
     · Animated dot: w-2 h-2 rounded-full oklch(68% 0.2 155) animate-pulse
     · Text: "AI-Native Writing for Modern Teams" text-fg/70 text-sm font-medium

  2. Headline (delay 100ms, 550ms)
     font-bold tracking-[-0.045em] leading-[0.92]
     font-size: clamp(3.5rem, 1rem + 6vw, 7.5rem)
     Line 1: "Write smarter." oklch(var(--fg))
     Line 2: "Ship faster." — gradient: linear-gradient(135deg, var(--primary), oklch(62% 0.21 305))
     Apply gradient: bg-clip-text text-transparent

  3. Subheadline (delay 220ms, 400ms)
     max-w-lg mx-auto mt-6 text-fg/65 text-lg leading-[1.75]
     Content: realistic 1-sentence product description

  4. CTA row (delay 370ms, 400ms)
     flex items-center justify-center gap-3 mt-10
     Primary: "Start writing free" rounded-full px-8 py-3.5 font-semibold text-sm
              oklch bg-primary hover:bg-primary-up
              box-shadow: 0 0 24px oklch(62% 0.21 285 / 0.4), 0 0 48px oklch(62% 0.21 285 / 0.15)
     Ghost: "Watch the demo →" rounded-full px-8 py-3.5 text-sm
            border border-fg/15 text-fg/70 hover:border-fg/30

  5. Social proof (delay 470ms, 400ms)
     flex items-center justify-center gap-3 mt-10
     5 overlapping avatars (w-8 h-8 rounded-full gradient-primary) + "-3 ml offset"
     "Loved by 50,000+ writers" text-fg/50 text-sm
     ★★★★★ oklch(75% 0.19 65) text-xs

  6. Visual spacer h-24 (video breathing room)

═══════════════════════════════════════
LOGO MARQUEE
═══════════════════════════════════════
py-10 overflow-hidden marquee-fade
Left label: "Trusted by teams at" text-fg/35 text-xs tracking-widest uppercase
Brands (liquid-glass pills): Vortex, Nimbus, Kynder, Halcyn, Aethon, Solace, Driftly, Covalent

═══════════════════════════════════════
ANTI-SLOP
═══════════════════════════════════════
- Zero hardcoded hex. All colors oklch(var(--token)) or oklch(...) direct
- Liquid glass on: navbar, eyebrow, logo pills — nowhere else in hero
- Fictional brands only (believable, not generic)
- Grain overlay on body for warmth
- @starting-style on any modal/dialog triggered from hero
```

---

## Template 2 — Developer Tool (Technical Mono, Dark Green)

**Niche:** Observability, CLIs, APIs, DevOps, code editors
**Vibe:** Terminal × Linear — monospace, utilitarian, authoritative

```
Build a developer tool hero.
Stack: React + Vite + Tailwind

OKLCH TOKENS:
  --bg:      oklch(7%  0.015 155);   /* deep dark green-tinted */
  --surface: oklch(11% 0.015 155);
  --fg:      oklch(94% 0.008 120);
  --primary: oklch(68% 0.200 155);   /* terminal green */
  --font:    'JetBrains Mono', 'Fira Code', monospace;
  --r:       0.375rem;               /* sharp — dev tool aesthetic */

HERO ANATOMY:
  1. Navbar: transparent start | liquid-glass on scroll (Container scroll-state)
     Left: "> axiom" font-mono font-bold — ">" in primary
     Right: ["$ npm i axiom" copy-pill liquid-glass rounded] + ["Docs" ghost]

  2. Background: var(--bg) +
     Scanline texture: repeating-linear-gradient(0deg, transparent 2px, oklch(100% 0 0/0.01) 3px)
     Radial glow: radial-gradient(ellipse at 50% 35%, oklch(68% 0.20 155/0.07) 0%, transparent 55%)
     Dot grid: radial-gradient(oklch(100% 0 0/0.06) 1px, transparent 1px) 28px 28px

  3. Content: centered, text-center, pt-24
     Eyebrow: liquid-glass rounded px-3 py-1 font-mono text-xs primary "$ v3.1 now stable ↗"
     Headline: font-mono font-bold clamp(2.5rem,5vw,5.5rem) tracking-tight leading-[1.05]
               "Ship observability." / "Not complexity."
               "observability" = solid primary (NOT gradient — terminal auth)
     Sub: font-sans text-fg/60 text-lg max-w-md leading-8 mt-5
     CTAs: "Get started" primary + "Read the docs →" ghost — BOTH font-mono
     Terminal block (signature element):
       liquid-glass rounded-lg p-5 font-mono text-sm text-left max-w-md mx-auto mt-10
       Title bar: flex — 3 dots (err/warn/ok colors) + "~/your-project" centered text-fg/30
       Lines (stagger reveal 200ms each):
         $ npm install @axiom/client     ← text-fg/70
         ✓ Installed in 0.3s             ← oklch(68% 0.20 155)
         $ axiom init --project my-app   ← text-fg/70
         ✓ Connected. Streaming logs...  ← oklch(68% 0.20 155) + blinking cursor

  4. Logo marquee: fictional dev brands — Supabase, PlanetScale, Neon, Railway (fictional variants)
     Each: liquid-glass rounded px-3 py-1.5 font-mono text-xs text-fg/50

ANIMATIONS: Terminal lines stagger 250ms each. Cursor blink on last line (@keyframes blink).
RADIUS: --r: 0.375rem everywhere. No rounded-full. No soft UI.
```

---

## Template 3 — Fintech (Professional Light, Two-Column)

**Niche:** Expense tracking, payments, invoicing, banking SaaS
**Vibe:** Bloomberg × Linear — clean, data-dense, trust-first

```
Build a fintech SaaS hero.
Stack: Next.js 15 + Tailwind

OKLCH TOKENS (light mode):
  --bg:       oklch(98% 0.005 265);
  --surface:  oklch(100% 0 0);
  --fg:       oklch(18% 0.030 265);
  --fg-muted: oklch(52% 0.015 265);
  --primary:  oklch(48% 0.190 265);  /* deep professional blue */
  --ok:       oklch(48% 0.180 155);  /* positive delta */
  --err:      oklch(52% 0.220 25);   /* negative delta */
  --border:   oklch(88% 0.010 265);
  --r:        0.5rem;                /* conservative — enterprise */

HERO LAYOUT: two-column (left: text 55%, right: floating dashboard card 45%)

LEFT COLUMN:
  Trust badge: liquid-glass-light rounded-full px-3 py-1 inline-flex items-center gap-2 mb-6
    · Shield icon + "SOC 2 Type II · GDPR · PCI DSS" text-fg/70 text-sm
  Headline: text-fg font-bold clamp(2.25rem,4vw,4rem) tracking-[-0.028em] leading-[1.12]
            "Expense management built for serious teams."
            NO gradient — plain bold text signals trust
  Sub: text-fg/60 text-lg max-w-md leading-8 mt-4
  CTAs: "Request a demo" primary → "Start free trial" border-primary text-primary
  Trust row: flex items-center gap-6 mt-8
    · "256-bit encryption" · "99.99% uptime" · "Instant reconciliation"
    Each: checkmark oklch(48% 0.18 155) + label text-fg/55 text-sm

RIGHT COLUMN (floating card):
  liquid-glass-light rounded-2xl p-6 shadow-[0_20px_60px_oklch(0%_0_0/0.08)]
  Balance: "$284,931.40" text-4xl font-bold text-fg
  Delta: "+$12,430 (4.6% this month)" text-ok text-sm font-medium flex items-center gap-1
  Sparkline SVG: 5-point smooth curve, stroke=primary, fill=primary/10, animated draw on load
  3 transactions: company name + amount + category chip (oklch tinted pills)
  Category chips: oklch(48% 0.19 265 / 0.10) bg + oklch(48% 0.19 265) text

LOGO BAR: "Trusted by finance leaders at" — fictional enterprise logos grayscale (no color)
ANIMATIONS: Left content stagger 80ms. Dashboard card: fade-in + scale(0.97→1) 600ms ease-spring.
            Balance counter: count up 0→284,931, 1200ms ease-out. Sparkline stroke-dasharray draw.
```

---

## Template 4 — Creative Agency (Neo-Brutalism + Editorial)

**Niche:** Design studios, creative agencies, experimental portfolios
**Vibe:** Awwwards × Balenciaga — raw, editorial, intentionally bold

```
Build a creative agency hero.
Stack: React + Vite + Tailwind + GSAP

OKLCH TOKENS (warm dark):
  --bg:      oklch(9%  0.018 50);   /* warm near-black */
  --surface: oklch(13% 0.018 50);
  --fg:      oklch(95% 0.008 80);
  --primary: oklch(65% 0.160 55);   /* copper/amber */
  --font-display: 'Clash Display', 'Playfair Display', serif;
  --r: 0;                           /* zero radius — brutalist */

NAVBAR: transparent, px-8 py-6 | "FORMA" tracking-[0.35em] text-xs font-bold |
        ["Work", "About", "Journal"] right | No CTA button

HERO ANATOMY (full viewport):
  Background: var(--bg) + radial glow + grain overlay opacity-4
  Layout: asymmetric, NOT standard left-text right-image

  Row 1 (top-left, massive):
    "CREATIVE" font-display italic font-light text-fg/30
    size: clamp(5rem, 12vw, 14rem) leading-[0.88] tracking-[-0.03em]

  Row 2 (push-right, fills row):
    [small 80×110px image — warm tones, rounded-lg, inline element]
    "STUDIO" font-display font-black text-fg
    size: clamp(5rem, 12vw, 14rem) leading-[0.88] tracking-[-0.04em]

  Row 3 (split):
    Left: "SINCE 2019 · BARCELONA" text-fg/40 text-xs tracking-widest uppercase
    Right: "37 Projects Shipped" liquid-glass-warm rounded px-3 py-1 text-xs

  Divider: h-px bg-gradient-to-r from-transparent via-fg/20 to-transparent my-16

  Bottom two-col:
    Left: "We design brands people remember — and identities that outlive trends."
          font-sans text-fg/65 text-lg leading-[1.7] max-w-[32ch]
    Right: "scroll to explore ↓" text-fg/35 text-xs tracking-widest uppercase

Services row: ["Brand Identity" · "Web Design" · "Motion" · "Art Direction" · "3D"]
  text-fg/45 text-sm, "·" separators

ANIMATIONS (GSAP):
  Headline character reveal: SplitText on "CREATIVE" + "STUDIO", each char y:40→0 + opacity stagger
  Inline image: GSAP ScrollTrigger parallax (y: 0→-50px over 100vh scroll)
  Custom cursor: 32px circle, mix-blend-mode: difference, lag follow
```

---

## Template 5 — Wellness / Organic (Soft Light, Phone Mockup)

**Niche:** Sleep apps, fitness trackers, meditation, nutrition
**Vibe:** Calm × Apple Health — soft, natural, trustworthy

```
Build a wellness app hero.
Stack: React + Vite + Tailwind + Framer Motion

OKLCH TOKENS (soft sage light):
  --bg:      oklch(97% 0.008 155);
  --surface: oklch(100% 0 0);
  --fg:      oklch(22% 0.020 155);
  --fg-muted:oklch(55% 0.012 155);
  --primary: oklch(52% 0.140 155);   /* sage green */
  --accent:  oklch(72% 0.130 60);    /* warm peach */
  --border:  oklch(86% 0.010 155);
  --r:       1.25rem;                /* extra soft */

BACKGROUND BLOBS (CSS only, no JS):
  Two absolute radial-gradient circles:
  Blob 1: 550px at -8% top 30%, oklch(52% 0.14 155 / 0.13), filter blur(80px)
  Blob 2: 500px at 108% bottom 20%, oklch(72% 0.13 60 / 0.10), filter blur(80px)
  Both: animation: blob-float 9s ease-in-out infinite alternate
  @keyframes blob-float { from { transform: translateY(0) } to { transform: translateY(-28px) } }

HERO LAYOUT: two-column (left: text 52%, right: phone mockup 48%)

LEFT:
  Eyebrow: "🌿 2M+ people sleeping better" liquid-glass-light rounded-full px-4 py-2 text-sm mb-8
  Headline: font-bold clamp(2.5rem,4vw,4rem) leading-[1.15] text-fg
            "Sleep deeper." / "Feel lighter." / "Live better."
            "deeper" = text-primary (no gradient — wellness warmth)
  Sub: text-fg/60 text-lg leading-[1.8] max-w-md mt-5
  CTAs: "Start for free" primary rounded-full px-8 py-4 font-semibold |
        "Already a member? Sign in →" text-fg/55 text-sm font-medium

  App store row: App Store + Google Play (liquid-glass-light pills)
  Media logos: "Featured in:" Forbes, Wired, Women's Health — grayscale, small

RIGHT (phone mockup):
  375×750 rounded-[3.25rem] border border-fg/8 overflow-hidden
  liquid-glass-light shadow-[0_40px_100px_oklch(0%_0_0/0.08)]
  animation: phone-bob 5s ease-in-out infinite alternate
  @keyframes phone-bob { from { transform: translateY(0) } to { transform: translateY(-12px) } }
  Screen content:
    Gradient bg sage to white | "Sleep Score" label | "92/100" text-5xl font-bold text-primary
    Arc SVG (stroke-dasharray animated from 0 to 230, 1500ms ease-out, delay 600ms)
    "Tonight's Plan" section: bedtime, wake time, sleep goal
    Bottom ring progress: 3 rings (sleep, movement, mindfulness) — animated draw

ANIMATIONS: Blob float continuous | Phone bob continuous | Left content: Framer stagger 80ms
```

---

## Template 6 — SaaS Pricing Page (Liquid Glass, Interactive Toggle)

**Niche:** Any SaaS product pricing page
**Stack:** React + Vite + Tailwind + Framer Motion

```
OKLCH TOKENS (dark):
  --bg: oklch(6% 0.018 265); --surface: oklch(10% 0.018 265);
  --fg: oklch(95% 0.010 95); --primary: oklch(62% 0.210 285);

PAGE STRUCTURE:
  Header: centered, mb-20
    Eyebrow: liquid-glass pill "Pricing" text-xs tracking-widest uppercase mb-4
    Headline: "Simple, transparent pricing." clamp(2rem,4vw,3.75rem) font-bold tracking-tight
    Sub: text-fg/60 text-lg mt-4

  TOGGLE: liquid-glass rounded-full p-1.5 inline-flex mt-8
    "Monthly" pill: active = bg-primary text-white rounded-full px-6 py-2.5 text-sm font-medium
    "Yearly" pill: inactive = text-fg/55 text-sm px-6 py-2.5
    "Save 20%" badge on Yearly: oklch(75% 0.19 65) bg, absolute top-right of pill, text-[10px] font-bold

  CARDS (3-column grid, gap-6):
    Card 1 — Starter:
      liquid-glass rounded-2xl p-8
      Plan: "Starter" text-fg/70 font-medium | "$0" text-5xl font-bold
      8 feature items: checkmark oklch(62% 0.18 155) + label text-fg/65 text-sm
      CTA: border border-border rounded-xl py-3 text-sm text-fg/75 hover:border-fg/30

    Card 2 — Pro (FEATURED):
      Wrapper: p-px rounded-2xl bg-gradient-to-b from-primary/40 to-oklch(62%_0.21_305/0.15)
      Inner: oklch(12% 0.022 265) bg rounded-[calc(1rem-1px)] p-8
      "Most Popular" badge: absolute top-4 right-4, liquid-glass px-3 py-1 text-xs text-primary
      Price: Framer layoutId="price" — animates smoothly between monthly/yearly
      "Save $X/year" text: fade-in when yearly selected (AnimatePresence)
      12 feature items including "Everything in Starter +"
      CTA: bg-primary rounded-xl py-3 font-semibold
           box-shadow: 0 0 28px oklch(62% 0.21 285 / 0.4)

    Card 3 — Enterprise:
      liquid-glass rounded-2xl p-8
      Price: "Custom" text-5xl font-bold
      Features: "Custom contracts", "Dedicated SLA", "Onboarding team", "Private cloud"
      CTA: "Talk to sales →" text-primary text-sm font-semibold (no button bg)

  FAQ ACCORDION (below cards, mt-24):
    max-w-2xl mx-auto | liquid-glass rounded-2xl overflow-hidden | divide-y divide-border/50
    8 questions | AnimatePresence on expand/collapse | height: auto animation with layout
    Questions: billing, cancellation, team seats, security, integration, data export, uptime, support

PRICE ANIMATION: monthly=[0,29,custom] yearly=[0,24,custom]
  Use Framer Motion layoutId="price-value" on the dollar amount spans
  AnimatePresence for "Save $X" text below Pro price
```

---

## Brand Name Bank (Fictional — Always Use These)

**Tech/AI:** Vortex, Nimbus, Kynder, Halcyn, Aethon, Luminal, Zephyr, Quark, Axiom, Solace
**Enterprise:** Meridian, Clearpath, Vantara, Arclight, Nexus, Solvex, Covalent, Altos, Pinnacle
**Consumer:** Driftly, Bloom, Soften, Luma, Sage, Still, Grove, Halo, Soothe, Tender
**Finance:** Clearpath, Vantara, Meridian Group, Arclight, Nexus Capital, Solvex, Aurum

## Quick Start Checklist

Before submitting any hero prompt to an AI agent, verify:
- [ ] OKLCH tokens defined (not HSL, not hex)
- [ ] `.liquid-glass` utility included
- [ ] `@starting-style` for any dialogs/modals
- [ ] Native scroll animation (`animation-timeline`) not JS listeners
- [ ] `@view-transition { navigation: auto; }` included
- [ ] Grain overlay on body (opacity 0.025–0.045)
- [ ] Fictional but believable brand names (not "Company A")
- [ ] Realistic product copy (not lorem ipsum)
- [ ] Per-element animation timing specified (delay + duration + easing)
