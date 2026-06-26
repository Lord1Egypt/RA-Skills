# Design Systems Pro — Advanced UI/UX Reference
> Learned from ui-ux-pro-max (xobi667) on ClawHub + distilled into actionable guidance

---

## 1. Color Palette by Product Type (96 product categories)

### Most Common Archetypes

| Product Type | Primary | CTA | Background | Notes |
|---|---|---|---|---|
| SaaS (General) | #2563EB (blue) | #F97316 (orange) | #F8FAFC | Trust blue + orange CTA contrast |
| Gaming / Cyberpunk | #7C3AED (purple) | #F43F5E (rose) | #0F0F23 | Neon purple + rose action |
| AI / Chatbot | #7C3AED (purple) | #06B6D4 (cyan) | #FAF5FF | AI purple + cyan interactions |
| Fintech / Crypto | #F59E0B (gold) | #8B5CF6 (purple) | #0F172A | Gold trust + purple tech |
| E-commerce Luxury | #1C1917 | #CA8A04 (gold) | #FAFAF9 | Premium black + gold accent |
| Healthcare | #0891B2 (cyan) | #059669 (green) | #ECFEFF | Calm cyan + health green |
| Creative Agency | #EC4899 (pink) | #06B6D4 (cyan) | #FDF2F8 | Bold pink + cyan accent |
| Video Streaming | #0F0F23 (black) | #E11D48 (red) | #000000 | Cinema dark + play red |
| Restaurant / Food | #DC2626 (red) | #CA8A04 (gold) | #FEF2F2 | Appetiting red + warm gold |
| Fitness / Gym | #F97316 (orange) | #22C55E (green) | #1F2937 | Energy orange + success green |

**Rule:** Primary color sets trust, CTA color creates urgency/action. They must have ≥7:1 contrast.

### Dark Background Products
Products that MUST use dark backgrounds: Gaming, Cyberpunk, Fintech, Video Streaming, Music Streaming, Developer Tools, Space Tech, Coding.

Products that MUST use light backgrounds: Healthcare, Education (kids), Restaurant, Wellness, Wedding.

---

## 2. Typography Pairings (50+ curated combinations)

### By Aesthetic

| Style | Heading | Body | Google Fonts Import |
|---|---|---|---|
| Tech Startup | Space Grotesk | DM Sans | `Space+Grotesk:wght@400;500;600;700&DM+Sans:wght@400;500;700` |
| Gaming / Esports | Russo One | Chakra Petch | `Russo+One&Chakra+Petch:wght@300;400;500;600;700` |
| Cyberpunk / HUD | Share Tech Mono | Fira Code | Monospace only — both mono |
| Pixel / Retro | Press Start 2P | VT323 | `Press+Start+2P&VT323` |
| Luxury / Fashion | Cormorant | Montserrat | `Cormorant:wght@400;500;600;700&Montserrat:wght@300;400;500` |
| Minimal Swiss | Inter | Inter | Single font — weight variations only |
| AI / Modern SaaS | Plus Jakarta Sans | Plus Jakarta Sans | Single font — versatile |
| Wellness / Calm | Lora | Raleway | Serif heading + elegant sans body |
| Developer Tool | JetBrains Mono | IBM Plex Sans | Mono heading + clean sans body |
| Editorial / News | Newsreader | Roboto | Serif editorial + readable body |
| Gen Z / Bold | Anton | Epilogue | Impact display + clean body |
| Crypto / Web3 | Orbitron | Exo 2 | Futuristic both |
| Kids / Education | Baloo 2 | Comic Neue | Fun, rounded |

**Chinese (Simplified):** `Noto Sans SC`
**Japanese:** `Noto Serif JP` (heading) + `Noto Sans JP` (body)

---

## 3. UI Style Systems (60+ documented styles)

### Most Relevant for Dark/Tech UI

#### Cyberpunk UI
- Background: `#0D0D0D`
- Colors: `#00FF00`, `#FF00FF`, `#00FFFF`
- Effects: Neon glow (`text-shadow: 0 0 10px`), glitch animation, CRT scanlines
- Font: monospace only
- CSS: `animation: glitch 0.3s`, `::before` scanlines with `repeating-linear-gradient`

#### Retro-Futurism (Synthwave)
- Background: `#1A1A2E`
- Colors: Neon Blue, Hot Pink #FF006E, Cyan #00FFFF
- Effects: CRT scanlines, neon glow, glitch on hover
- Era: 1980s inspired

#### Glassmorphism
- Background: `rgba(255,255,255,0.15)` over vibrant bg
- CSS: `backdrop-filter: blur(15px); border: 1px solid rgba(255,255,255,0.2);`
- Text must maintain 4.5:1 contrast over glass

#### Neubrutalism (2024 Trend)
- Borders: `3-4px solid #000`
- Shadows: `5px 5px 0 #000` (hard offset, no blur)
- Colors: High saturation primary colors
- No gradients, no border-radius (or minimal)
- Hover: `transform: translate(-4px, -4px)` + `box-shadow: 9px 9px 0 #000`

#### Bento Grid (Apple-style)
- Layout: `display: grid; grid-template-columns: repeat(4, 1fr); grid-auto-rows: 200px; gap: 16px;`
- Cards: `border-radius: 24px; background: #FFFFFF; box-shadow: 0 4px 6px rgba(0,0,0,0.05);`
- Hover: `transform: scale(1.02)`
- Background: `#F5F5F7`

#### Aurora / Gradient Mesh
- CSS: `background: conic-gradient(...)` or `radial-gradient` with multiple stops
- Animation: `background-position` shift `8-12s infinite`
- Text must have sufficient contrast — often needs dark overlay

---

## 4. UX Anti-Patterns — 99 Issues to Avoid

The following are HIGH SEVERITY issues (from 99-item database):

### Navigation
- No smooth scroll on anchor links → add `html { scroll-behavior: smooth; }`
- Fixed nav covering content → add `padding-top` equal to nav height
- No active state indicator → highlight current page/section
- No back button on mobile → preserve browser history

### Animation
- Animate more than 1-2 elements per view → animation overload, distraction
- Animations > 500ms → feels sluggish (use 150-300ms)
- No `prefers-reduced-motion` check → accessibility failure (HIGH SEVERITY)
- Continuous decorative animations → distracting
- Using `top/left/width/height` in animations → triggers expensive repaints, use `transform` instead

### Layout
- Z-index above 50 (arbitrary) → use scale: 10, 20, 30, 50
- `100vh` on mobile → use `min-h-dvh` instead (browser chrome issue)
- No space reserved for async content → layout shift (CLS)
- Multiple overlapping `position: fixed` elements → chaos

### Touch / Mobile
- Touch targets < 44×44px → HIGH SEVERITY
- Hover-only interactions → doesn't work on touch
- `tap delay` → add `touch-action: manipulation`
- Horizontal swipe conflicts with system gestures → avoid on main content

### Accessibility (ALL HIGH SEVERITY)
- Missing focus ring → `focus:ring-2 focus:ring-blue-500`
- Color as only indicator → add icons/text
- Missing alt text
- No form labels (placeholder only)
- No skip link for keyboard nav

### Forms
- Placeholder as label → use floating label or separate label
- No inline validation → validate on blur
- Wrong input type (text for email/phone) → use `type="email"`, `type="tel"`
- No password show/hide toggle
- No submission feedback

### Responsive
- Mobile body text < 16px → HIGH SEVERITY
- Missing viewport meta tag → HIGH SEVERITY
- No horizontal scroll prevention → `max-w-full overflow-x-hidden`
- Same small button sizes on mobile → increase touch targets

---

## 5. Pre-Delivery Checklist (40 items)

### Visual Quality
- [ ] No emojis as UI icons — use SVG (Heroicons/Lucide)
- [ ] All icons from consistent set (24×24 viewBox)
- [ ] Hover states don't shift layout (use `opacity`/`color`, not `margin`/`padding`)
- [ ] Use theme colors directly, not `var()` wrapper on Tailwind
- [ ] Brand logos verified from Simple Icons

### Interaction
- [ ] All clickable elements have `cursor-pointer`
- [ ] Hover: visual feedback (`150-300ms`)
- [ ] Active/press state present (`transform: scale(0.95)` or `translate`)
- [ ] Focus states visible (`focus:ring-2`)
- [ ] Loading buttons: disabled + spinner

### Light/Dark Mode
- [ ] Light mode text ≥ 4.5:1 contrast (body text)
- [ ] Glass/transparent elements visible in light mode (`bg-white/80`, not `/10`)
- [ ] Borders visible in both modes
- [ ] No `text-gray-400` for body text in light mode (use `#475569` minimum)

### Layout
- [ ] Floating elements have edge spacing (`top-4 left-4 right-4`)
- [ ] Content not hidden behind fixed navbar (add `padding-top`)
- [ ] Responsive at 375px / 768px / 1024px / 1440px
- [ ] No horizontal scroll on mobile

### Accessibility
- [ ] All images have alt text
- [ ] Form inputs have labels (not just placeholder)
- [ ] Color is not the only indicator
- [ ] `prefers-reduced-motion` respected
- [ ] Touch targets ≥ 44×44px

---

## 6. Landing Page Patterns (30 documented)

### By Conversion Goal

| Goal | Pattern | Key Elements |
|---|---|---|
| SaaS free trial | Hero + Features + CTA | Video demo center, sticky CTA, trust badges |
| E-commerce | Product Demo | Before/after slider, reviews, urgency |
| Lead generation | Lead Magnet + Form | ≤3 form fields, preview of lead magnet, instant value |
| Pricing page | Pricing + CTA | 3 tiers, popular badge, annual discount 20-30%, FAQ |
| Brand awareness | Storytelling-Driven | Scroll narrative, 5-7 chapters, emotional hooks |
| Event/Webinar | Event Landing | Countdown timer, speaker bio, limited seats |
| Launch/Waitlist | Waitlist Pattern | Countdown, email capture, social proof count |
| Community | Community/Forum | Member count, activity feed preview, low friction join |

### CTA Placement Rules
- Primary CTA: above fold always
- Secondary CTA: after testimonials/social proof
- Sticky CTA: in navbar on scroll past hero
- Never more than 2 CTA variants visible at once

---

## 7. Design System Tokens Template

```css
:root {
  /* Spacing (8px base unit) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-6: 24px;
  --space-8: 32px;
  --space-12: 48px;
  --space-16: 64px;

  /* Typography Scale (1.25 ratio) */
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;    /* minimum for body */
  --text-lg: 18px;
  --text-xl: 20px;
  --text-2xl: 24px;
  --text-3xl: 30px;
  --text-4xl: 36px;
  --text-5xl: 48px;
  --text-6xl: 60px;

  /* Border Radius */
  --radius-sm: 6px;
  --radius: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;    /* Bento/large cards */
  --radius-full: 9999px;

  /* Shadows / Elevation */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.1);
  --shadow: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-md: 0 10px 20px rgba(0,0,0,0.1);
  --shadow-lg: 0 20px 40px rgba(0,0,0,0.15);
  --shadow-glow: 0 0 30px rgba(var(--accent-rgb), 0.4);

  /* Z-Index Scale */
  --z-1: 10;
  --z-2: 20;
  --z-3: 30;
  --z-modal: 50;
  --z-toast: 100;

  /* Animation */
  --duration-fast: 150ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
  --ease-in: cubic-bezier(0.64, 0, 0.78, 0);
  --spring: cubic-bezier(0.34, 1.56, 0.64, 1);  /* bouncy */
}
```

---

## 8. Design Decision Framework

When choosing a UI style, ask 3 questions:

1. **Who is the user?** Age, tech savvy, context (mobile/desktop/TV)
2. **What is the industry?** Healthcare = accessible + calm. Gaming = immersive + dark. Finance = trust + professional.
3. **What is the goal?** Conversion = minimal distractions. Showcase = rich visual. Dashboard = information density.

### Quick Decision Table

| Industry | NEVER use | ALWAYS include |
|---|---|---|
| Healthcare / Medical | Neon colors, heavy animation | WCAG AAA, calm palette, 18px+ body text |
| Finance / Banking | Playful design, bright colors | Security badges, dark navy, trust signals |
| Gaming | Flat/minimal design | Dark mode, neon, 3D or glitch effects |
| Kids / Education | Dark mode, complex UX | Rounded shapes, bright pastels, large touch targets |
| SaaS B2B | Emoji icons, cluttered layout | Feature comparison, trust logos, demo CTA |
| E-commerce Luxury | Bright/vibrant palette | Premium black/gold, white space, elegance |

---

## Source
Learned from: `ui-ux-pro-max` by @xobi667 on ClawHub (MIT-0 license)
Data files: colors.csv (96 rows), typography.csv (57 rows), styles.csv (68 rows), ux-guidelines.csv (99 rows), landing.csv (30 rows), ui-reasoning.csv
