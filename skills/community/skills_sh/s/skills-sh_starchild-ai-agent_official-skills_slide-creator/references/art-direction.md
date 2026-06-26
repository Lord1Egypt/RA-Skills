# Art Direction Reference

Detailed visual style vocabulary for building HTML slides.

---

## Style Taxonomy

### 1. Dark Tech Minimal
**Mood:** Bold, modern, premium  
**Industries:** SaaS, AI, developer tools, startups  
**Search keywords:** `"dark UI presentation" "dark minimal slide deck" site:dribbble.com`

```
Background:   #000 / #0a0a0a / #0d0d0d
Surface:      rgba(255,255,255,0.04) borders rgba(255,255,255,0.08)
Accent:       #3b82f6 (blue) / #10b981 (green) / #f59e0b (amber)
Text:         #fff / #e5e7eb / #9ca3af
Font:         Inter, Space Grotesk, JetBrains Mono (mono accents)
Radius:       6–12px
Glow:         radial-gradient(ellipse at top, rgba(accent,0.15) 0%, transparent 60%)
```

---

### 2. Light Clean Corporate
**Mood:** Trustworthy, professional, readable  
**Industries:** Finance, consulting, enterprise, legal  
**Search keywords:** `"clean white presentation" "corporate slide design" site:behance.net`

```
Background:   #fff / #f8fafc
Surface:      #f1f5f9 border #e2e8f0
Accent:       #1e40af (navy) / #0f766e (teal) / #7c3aed (violet)
Text:         #0f172a / #374151 / #6b7280
Font:         Inter, DM Sans, Plus Jakarta Sans
Radius:       4–8px
Shadow:       0 1px 3px rgba(0,0,0,0.08)
```

---

### 3. Bold Gradient
**Mood:** Creative, energetic, expressive  
**Industries:** Agencies, design studios, product launches, events  
**Search keywords:** `"gradient slide deck" "colorful presentation design" site:dribbble.com`

```
Background:   linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #0f172a 100%)
Surface:      rgba(255,255,255,0.08) borders rgba(255,255,255,0.12)
Accent:       #a855f7 / #ec4899 / #06b6d4 (vivid, high contrast)
Text:         #fff / rgba(255,255,255,0.7)
Font:         Outfit, Nunito, Sora
Radius:       12–20px
Effect:       blurred blobs (filter: blur(80px)) as background deco
```

---

### 4. Playful Illustration
**Mood:** Friendly, casual, approachable  
**Industries:** Education, consumer apps, HR/culture, NGO  
**Search keywords:** `"playful presentation design" "illustration slide deck" pastel`

```
Background:   #fffbf0 / #f0fdf4 / #fdf4ff (soft warm/cool pastels)
Surface:      #fff border #e9d5ff / #bbf7d0
Accent:       #f97316 (orange) / #8b5cf6 (violet) / #10b981 (green)
Text:         #1f2937 / #4b5563
Font:         Nunito, Poppins, Quicksand
Radius:       16–24px
Decoration:   wavy SVG dividers, rounded blobs, dashed borders
```

---

### 5. Newspaper / Editorial
**Mood:** Authoritative, journalistic, high-information  
**Industries:** Media, research, reports, policy  
**Search keywords:** `"editorial layout presentation" "newspaper style slide" typography`

```
Background:   #fafaf9 / #1c1917 (dark variant)
Surface:      ruled lines (border-bottom: 1px solid #e7e5e4), column grids
Accent:       #dc2626 (red) / #ca8a04 (amber) — used sparingly
Text:         #1c1917 / #57534e (body)
Font:         Playfair Display (headings), Source Serif 4 (body), mono for data
Radius:       0px (sharp, no rounding)
Layout:       multi-column grid, large pull quotes
```

---

### 6. Glassmorphism
**Mood:** Modern, layered, premium light  
**Industries:** Tech, fintech, luxury, mobile apps  
**Search keywords:** `"glassmorphism slide" "frosted glass UI presentation"`

```
Background:   linear-gradient(135deg, #667eea 0%, #764ba2 100%) or photo
Surface:      background: rgba(255,255,255,0.12); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.2)
Accent:       #fff (primary) / #f0f9ff (secondary)
Text:         #fff / rgba(255,255,255,0.8)
Font:         Inter, Figtree, Geist
Radius:       16–24px
Effect:       Multiple glass layers, subtle shadows
```

---

### 7. Monochrome Technical
**Mood:** Precise, systematic, data-first  
**Industries:** Engineering, research, academic, cybersecurity  
**Search keywords:** `"monochrome technical presentation" "data report slide design"`

```
Background:   #111827 / #030712
Surface:      #1f2937 border #374151
Accent:       #34d399 (terminal green) / #60a5fa (signal blue) — exactly one accent
Text:         #f9fafb / #9ca3af
Font:         JetBrains Mono, IBM Plex Mono (code/data), Inter (prose)
Radius:       2–4px
Layout:       dense, grid-aligned, data heavy
```

---

### 8. Warm Startup
**Mood:** Human, optimistic, narrative  
**Industries:** Consumer brands, D2C, social impact, storytelling  
**Search keywords:** `"warm brand presentation" "human centered slide deck" startup pitch`

```
Background:   #fff7ed / #fef3c7 / #1c1917 (dark variant)
Surface:      #fff border #fed7aa
Accent:       #ea580c (orange) / #16a34a (green) / #b45309 (amber)
Text:         #1c1917 / #78350f
Font:         Plus Jakarta Sans, Lora (serif headings), DM Sans
Radius:       8–16px
Photo style:  warm-toned, human subjects
```

---

## Industry → Style Quick Map

| Industry | Recommended style |
|----------|------------------|
| SaaS / Dev tools | Dark Tech Minimal or Monochrome Technical |
| Finance / Legal | Light Clean Corporate or Newspaper Editorial |
| Creative agency | Bold Gradient or Glassmorphism |
| Education / EdTech | Playful Illustration or Warm Startup |
| AI / Research | Monochrome Technical or Dark Tech Minimal |
| Consumer brand | Warm Startup or Playful Illustration |
| Healthcare | Light Clean Corporate |
| Crypto / Web3 | Dark Tech Minimal or Glassmorphism |
| Government / Policy | Newspaper Editorial or Light Clean Corporate |

---

## CSS Token Templates

Each style above maps directly to a CSS variables block. When building, open the
template for the chosen style and customize accent/font to match user's brand.

### Token structure (use in `<style>` or `styles.css`)

```css
:root {
  --bg-primary:   /* main slide bg */
  --bg-surface:   /* card/panel bg */
  --border-color: /* subtle dividers */
  --accent:       /* primary action color */
  --accent-muted: /* 15% opacity version */
  --text-primary: /* headings */
  --text-muted:   /* body/secondary */
  --radius:       /* border-radius */
  --font-head:    /* heading font */
  --font-body:    /* body font */
}
```

---

## Art Direction Conversation Guide

### 3 key questions to ask the user

1. **Audience & setting** — "Who is this deck for: investors, internal team, or a public keynote?"
2. **Mood keyword** — "How should the audience feel after viewing it? (authoritative / energetic / friendly / geeky-modern)"
3. **Brand constraint** — "Any brand colors, required fonts, or logo that must be included?"

### Search strategy

Use `web_search` with these patterns to find visual references:
- Style-specific: `"dark minimal presentation 2024" site:dribbble.com`
- Industry-specific: `"[industry] pitch deck design" OR "slide design inspiration"`
- Color-specific: `"[color palette name] UI deck slides"`

### Presenting options to user

Present exactly **3 style options**, each with:
- Style name + 1-line mood description
- 3 color hex swatches (bg / surface / accent)
- Font pairing
- Why it fits their content

### style-brief.md output template

```markdown
# Style Brief: [Project Name]

## Chosen Style: [Style Name]

### Color Palette
- Background: [hex]
- Surface: [hex]
- Accent: [hex]
- Text primary: [hex]
- Text muted: [hex]

### Typography
- Heading font: [name + Google Fonts URL]
- Body font: [name + Google Fonts URL]

### Visual Character
- Border radius: [px]
- Surface treatment: [description]
- Special effects: [glow / blur / grain / none]
- Layout density: [minimal / balanced / dense]

### Mood Reference
[1-2 sentence description of the visual feel]

### Search references found
- [URL or description 1]
- [URL or description 2]
```

---

## Extended Styles (Asian / Regional Aesthetics)

> Notes on references
> - If user provides reference images/screenshots, extract palette + spacing + shape language from images first.
> - If user provides web links, use `web_fetch` to read page content and infer tone/structure, then map into nearest style token template.
> - Avoid depending on remote CSS/source-code scraping; keep implementation template-driven.

---

### 9. HK Financial Blue-Gold
**Mood:** Authoritative, institutional, premium  
**Industries:** HKEX-listed companies, HK financial institutions, cross-border finance, Web3 in HK  
**Inspired by:** HKEX annual reports, DBS/Hang Seng brand decks

```
Background:   #0a1628 / #0d1f3c (deep navy)
Surface:      rgba(212,175,55,0.08) border rgba(212,175,55,0.25) (gold tint)
Accent:       #d4af37 (HKEX gold) / #c8a951 (warm gold)
Text:         #f5f0e8 (warm white) / #a89a7a (muted gold)
Font:         EB Garamond (headings, serif authority) + Inter (body)
Radius:       0–4px (sharp, institutional)
Effect:       thin gold horizontal rule as section divider, subtle grid texture
Logo spot:    top-right, 40px height
```

---

### 10. Ink & Paper (Ink-Wash Minimalism)
**Mood:** Cultural depth, elegant restraint, East-West hybrid  
**Industries:** Cultural events, luxury brand, art foundation, Chinese heritage organizations

```
Background:   #faf8f5 (warm paper) / #1a1a18 (ink black)
Surface:      #f0ede8 border #d4cfc8
Accent:       #c0392b (vermilion red) / #2c5f2e (pine green)
Text:         #1a1a18 / #5a5650
Font:         Noto Serif SC (Chinese headings) + Cormorant Garamond (English) + Noto Sans SC (body)
Radius:       0px
Effect:       thin brush-stroke SVG rule, asymmetric layout, generous white space
Layout:       right-aligned text blocks, large negative space
```

---

### 11. Singapore Tech Hub
**Mood:** Modern, multicultural, optimistic, government-confident  
**Industries:** GovTech, smart city, regional HQ, SEA startup

```
Background:   #fff / #f0f4f8
Surface:      #e8f0fe border #c5d5f5
Accent:       #e63946 (SG red) / #1d3557 (trusted blue)
Text:         #1d3557 / #457b9d
Font:         IBM Plex Sans (bilingual-safe, supports Chinese) + IBM Plex Mono (data)
Radius:       6–10px
Effect:       subtle diagonal stripe texture, clean card shadows
Note:         IBM Plex Sans covers Latin + Chinese glyphs natively
```

---

### 12. Crypto Neon Underground
**Mood:** Hype, community, degen, memetic energy  
**Industries:** NFT project, DeFi protocol, meme coin, crypto-native community

```
Background:   #000 / #050510
Surface:      #0d0d20 border rgba(0,255,200,0.2)
Accent:       #00ffcc (neon green) / #ff2d78 (hot pink) — use both freely
Text:         #fff / #b0fce9
Font:         Rajdhani / Exo 2 (headings) + Space Mono (data/addresses)
Radius:       4px
Effect:       animated scanline CSS, glitch text effect (CSS only), neon box-shadow
Layout:       asymmetric, rule-breaking, oversized numbers
```

---

### 13. Silicon Valley Product Minimal
**Mood:** Product-led, clean, confident, conversion-focused  
**Industries:** US B2B SaaS, developer tools, product launches, PLG companies

```
Background:   #f8fafc / #ffffff
Surface:      #ffffff border #e5e7eb
Accent:       #2563eb (product blue) / #14b8a6 (teal alt)
Text:         #0f172a / #475569
Font:         Inter (UI-safe) + Geist (headings optional)
Radius:       10–14px
Effect:       minimal cards, subtle shadow (0 8px 24px rgba(15,23,42,0.06))
Layout:       strong whitespace, tight hierarchy, KPI cards
```

---

### 14. YC / Stripe Investor Clean
**Mood:** Rational, credible, metrics-first, founder-friendly  
**Industries:** US/EU startup fundraising, seed-series A pitch decks

```
Background:   #ffffff / #f9fafb
Surface:      #f3f4f6 border #d1d5db
Accent:       #635bff (stripe violet) / #ff5a1f (yc orange, sparing)
Text:         #111827 / #6b7280
Font:         Inter + IBM Plex Sans
Radius:       6–10px
Effect:       no heavy decoration, straight lines, data tables + tiny charts
Layout:       investor narrative flow, one chart or one claim per slide
```

---

### 15. European Editorial Luxury
**Mood:** Premium, restrained, high-fashion editorial  
**Industries:** Luxury brands, fashion, design studios, cultural institutions

```
Background:   #f7f5f2 / #111111
Surface:      #ece8e1 border #d6d0c7
Accent:       #b08d57 (champagne gold) / #8c7355
Text:         #171717 / #5b5b5b
Font:         Canela/Playfair Display (headings) + Neue Haas/Inter (body fallback)
Radius:       0–4px
Effect:       thin rules, oversized serif titles, magazine-like whitespace
Layout:       asymmetric editorial grid, pull quotes, image-led sections
```

---

### 16. California Lifestyle Gradient
**Mood:** Optimistic, social, creator-economy friendly  
**Industries:** US consumer apps, DTC, creator tools, community products

```
Background:   linear-gradient(135deg, #fff7ed 0%, #ffe4e6 45%, #e0f2fe 100%)
Surface:      rgba(255,255,255,0.75) border rgba(255,255,255,0.9)
Accent:       #ff6b6b / #6366f1 / #06b6d4
Text:         #1f2937 / #6b7280
Font:         Sora (head) + Inter (body)
Radius:       14–24px
Effect:       soft blob gradients, friendly icons, rounded chips
Layout:       benefit-first, social proof blocks, CTA-heavy closing slide
```

---

## Updated Industry → Style Map

| Industry / Audience | Primary | Alternative |
|--------------------|---------|-------------|
| HKEX / HK Finance | HK Financial Blue-Gold | Light Clean Corporate |
| HK Web3 Conference | Dark Tech Minimal | Glassmorphism |
| Crypto community / NFT | Crypto Neon Underground | Dark Tech Minimal |
| CN Cultural / Heritage | Ink & Paper (Ink-Wash Minimalism) | Warm Startup |
| Singapore Government | Singapore Tech Hub | Light Clean Corporate |
| SEA Startup | Singapore Tech Hub | Bold Gradient |
| Pan-Asian Luxury | Ink & Paper (Ink-Wash Minimalism) | Glassmorphism |
| SaaS / Dev tools | Dark Tech Minimal | Monochrome Technical |
| Finance / Legal | Light Clean Corporate | Newspaper Editorial |
| Creative agency | Bold Gradient | Glassmorphism |
| Education / EdTech | Playful Illustration | Warm Startup |
| AI / Research | Monochrome Technical | Dark Tech Minimal |
| Consumer brand | Warm Startup | Playful Illustration |
| Healthcare | Light Clean Corporate | — |
| Government / Policy | Newspaper Editorial | Singapore Tech Hub |
| US Big Tech / B2B SaaS | Silicon Valley Product Minimal | Dark Tech Minimal |
| US/EU VC Fundraising | YC / Stripe Investor Clean | Light Clean Corporate |
| European Luxury / Fashion | European Editorial Luxury | Glassmorphism |
| US Consumer Growth / DTC | California Lifestyle Gradient | Warm Startup |

---

## Reference Extraction Protocol (from real-world testing)

> When a user provides a web URL as a style reference, follow these 7 rules to avoid misreading the style.
> These were discovered through trial-and-error (e.g. operaneon.com was misread as "neon" when it was actually warm brutalist).

### 7 Rules for URL Reference Extraction

1. **Ignore the brand name / domain name** — Never infer visual style from the product's industry or name. Example: "Neo" does NOT mean neon, "Opera" does NOT mean European luxury. The URL text is a red herring.

2. **Read copy tone & vocabulary** — The words used on the page reveal mood:
   - "surgical precision", "quiet confidence" → restrained, controlled
   - "unleash", "radically", "disrupt" → bold, aggressive
   - "crafted", "heritage", "timeless" → editorial, luxury
   - "fast", "simple", "built for" → product-led, SaaS

3. **Extract explicit color vocabulary** — Look for CSS keywords in the fetched text, or color names mentioned in body text / alt tags. Warm vs cool, light vs dark, muted vs saturated. The actual words on the page are more reliable than guessing.

4. **Infer layout density** — Count words per section:
   - Sparse (few words, large gaps) → editorial, luxury, confident
   - Dense (lots of info, tight spacing) → technical, functional, data-heavy

5. **Identify decorative motifs** — What visual elements are mentioned or implied:
   - Geometric shapes / grid lines → structural, brutalist
   - Soft gradients / blobs → lifestyle, friendly
   - Photography → editorial, human
   - Line art / icons → technical, clean
   - Typography-only → editorial, Swiss

6. **Find closest template + describe delta** — Don't generate from scratch. Match to the nearest template in art-direction.md, then describe what to change (e.g. "Style G but warmer, replace blue with burnt orange, add subtle grid lines").

7. **When uncertain, be conservative** — Under-promise the style match. Present 3 options:
   - Option A = your best interpretation of the reference
   - Option B = safer, cleaner variant
   - Option C = more experimental variant

---

## Style 17. Opera Warm Brutalist (extracted from operaneon.com)

**Mood:** Controlled tension, architectural precision, warm undertones  \n**Industries:** Architecture studios, design agencies, creative tech, European creative brands  \n**Extraction notes:** Dark background is warm deep gray/brown (NOT black), accent is burnt orange/amber (NOT neon), typography is large light-weight tight-tracking, decorative elements are thin lines + crosshairs (NOT glow effects).

```
Background:   #1a1814 / #252220 / #1c1a17 (warm dark gray-brown, NOT pure black)
Surface:      rgba(255,255,255,0.03) border rgba(255,255,255,0.06) — thin, minimal
Accent:       #e07a3a (burnt orange) / #c4622d (deep amber) — warm, NOT neon
Text:         #e8e4df (warm white) / #9a9490 (muted warm gray)
Font:         Space Grotesk / Helvetica Neue (headings) + Inter (body) — light weight, tight tracking
Radius:       0–2px (almost sharp, architectural)
Decorative:   thin grid lines, crosshair marks (+), oversized numbers, generous negative space
Layout:       editorial grid, asymmetric, content sparse but type-heavy
NOT:          neon glow, cyber effects, rainbow gradients, rounded cards
```

---

## Updated Industry → Style Map (with Style 17)

| Industry / Audience | Primary | Alternative |
|--------------------|---------|-------------|
| HKEX / HK Finance | HK Financial Blue-Gold | Light Clean Corporate |
| HK Web3 Conference | Dark Tech Minimal | Glassmorphism |
| Crypto community / NFT | Crypto Neon Underground | Dark Tech Minimal |
| CN Cultural / Heritage | Ink & Paper (Ink-Wash Minimalism) | Warm Startup |
| Singapore Government | Singapore Tech Hub | Light Clean Corporate |
| SEA Startup | Singapore Tech Hub | Bold Gradient |
| Pan-Asian Luxury | Ink & Paper (Ink-Wash Minimalism) | Glassmorphism |
| SaaS / Dev tools | Dark Tech Minimal | Monochrome Technical |
| Finance / Legal | Light Clean Corporate | Newspaper Editorial |
| Creative agency | Bold Gradient | Glassmorphism |
| Education / EdTech | Playful Illustration | Warm Startup |
| AI / Research | Monochrome Technical | Dark Tech Minimal |
| Consumer brand | Warm Startup | Playful Illustration |
| Healthcare | Light Clean Corporate | — |
| Government / Policy | Newspaper Editorial | Singapore Tech Hub |
| US Big Tech / B2B SaaS | Silicon Valley Product Minimal | Dark Tech Minimal |
| US/EU VC Fundraising | YC / Stripe Investor Clean | Light Clean Corporate |
| European Luxury / Fashion | European Editorial Luxury | Glassmorphism |
| US Consumer Growth / DTC | California Lifestyle Gradient | Warm Startup |
| Architecture / Design Studio | Opera Warm Brutalist | European Editorial Luxury |
| Creative Tech | Opera Warm Brutalist | Dark Tech Minimal |
