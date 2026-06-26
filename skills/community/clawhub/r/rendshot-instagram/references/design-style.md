# Instagram Visual Design Guide

## Aesthetic Categories

### 1. Clean Minimal — Best for: Business, tech, coaching
- White or light backgrounds
- 1-2 accent colors only
- Bold sans-serif typography
- Generous whitespace
- Flat icons or simple illustrations
- **Grid feel**: Airy, professional, cohesive

### 2. Bold & Graphic — Best for: Fitness, motivation, marketing
- High contrast (dark bg + neon/bright accents)
- Large uppercase text
- Geometric shapes, lines, frames
- Gradient overlays
- Strong visual hierarchy
- **Grid feel**: Energetic, attention-grabbing

### 3. Warm Editorial — Best for: Food, lifestyle, wellness
- Earth tones, warm palette
- Serif or mixed typography
- Photography-forward
- Soft overlays, rounded corners
- Editorial-quality compositions
- **Grid feel**: Inviting, aspirational

### 4. Moody & Dark — Best for: Photography, luxury, nightlife
- Dark backgrounds (near black)
- Desaturated or selectively colored
- Thin elegant fonts
- Minimal text overlay
- Rich textures
- **Grid feel**: Premium, cinematic

### 5. Playful & Colorful — Best for: Youth brands, creative, education
- Bright multi-color palettes
- Rounded sans-serif fonts
- Illustrated elements, doodles
- Gradient backgrounds
- Emoji and icon integration
- **Grid feel**: Fun, approachable, youthful

### 6. Brutalist / Anti-Design — Best for: Tech, art, Gen-Z audiences
- Raw typography, broken grids
- High contrast, clashing colors
- Intentional "ugly" aesthetic
- Monospace fonts, borders, stamps
- **Grid feel**: Edgy, unconventional

## Color Palettes by Niche

### Food & Beverage
- Primary: Terracotta `#C17652`, Cream `#FBF3EB`
- Accent: Olive `#6B7B3A`, Honey `#D4A54A`
- Background: Warm white `#FAF7F2`

### Fitness & Wellness
- Primary: Charcoal `#2D2D2D`, Electric green `#00E676`
- Accent: Orange `#FF6D00`, White `#FFFFFF`
- Background: Near black `#1A1A1A` or bright white

### Fashion & Beauty
- Primary: Black `#000000`, Blush `#F5C6C6`
- Accent: Gold `#C9A44A`, Deep red `#8B2252`
- Background: Off-white `#FAFAFA`

### Tech & SaaS
- Primary: Deep blue `#1A237E`, White `#FFFFFF`
- Accent: Cyan `#00BCD4`, Purple `#7C4DFF`
- Background: Dark `#0F1419` or light gray `#F5F5F7`

### Travel & Adventure
- Primary: Ocean `#1E88E5`, Sand `#D4C5A9`
- Accent: Sunset `#FF7043`, Forest `#2E7D32`
- Background: Sky `#E3F2FD` or white

### Education & Coaching
- Primary: Navy `#1A3A5C`, Bright yellow `#FFD600`
- Accent: Coral `#FF6B6B`, Teal `#26A69A`
- Background: Light `#FAFAFA` or soft blue `#E8EAF6`

## Typography Rules

### Feed Post (1080x1080)
- Title: 48-72px, bold, max 2 lines
- Subtitle: 28-36px, regular weight
- Body text: 24-28px (if needed, keep minimal)
- Safe margin: 80px from each edge

### Story (1080x1920)
- Title: 56-80px, bold, centered or top-aligned
- Body: 28-36px
- Keep text in the center 60% vertically (avoid system UI overlap at top/bottom)
- Safe zone: Top 120px + bottom 200px are system UI areas

### Carousel Slide
- Title: 48-64px, consistent across all slides
- Body: 24-32px
- Number/step: 80-120px (large visual anchor)
- Lock layout template after slide 1 for consistency

### Font Recommendations
- Sans-serif (modern): Inter, DM Sans, Plus Jakarta Sans, Poppins
- Sans-serif (bold): Montserrat, Bebas Neue, Oswald
- Serif (editorial): Playfair Display, DM Serif Display, Lora
- Mono (tech): JetBrains Mono, Space Mono, Fira Code
- Display (creative): Space Grotesk, Clash Display

## Layout Patterns

### Feed Post (1080x1080)
```
┌─────────────────┐
│                  │
│   TITLE TEXT     │  ← Top third: text hierarchy
│   Subtitle       │
│                  │
│   ┌──────────┐  │
│   │  VISUAL  │  │  ← Center: image, illustration, or icon
│   │  ELEMENT │  │
│   └──────────┘  │
│                  │
│   CTA / Tag      │  ← Bottom: subtle CTA
└─────────────────┘
```

### Story (1080x1920)
```
┌─────────────────┐
│  ⚠ System UI    │  ← 120px: avoid text here
│                  │
│   TITLE          │
│                  │
│   ┌──────────┐  │
│   │          │  │  ← Center: primary content
│   │  CONTENT │  │
│   │          │  │
│   └──────────┘  │
│                  │
│   CTA            │
│  ⚠ System UI    │  ← 200px: avoid text here
└─────────────────┘
```

### Carousel Slide
```
┌─────────────────┐
│  Step #          │  ← Large number anchor
│                  │
│  POINT TITLE     │  ← One key idea
│                  │
│  Supporting text  │  ← Brief explanation
│  or visual       │
│                  │
│  ─── page dot ── │  ← Visual pagination hint
└─────────────────┘
```

## Grid Aesthetic Principles

Instagram's profile grid is a 3-column layout. Plan for visual cohesion:

1. **Color consistency** — Stick to your palette across posts
2. **Alternating pattern** — Quote / photo / graphic rotation
3. **Row planning** — Every 3 posts should look good as a horizontal set
4. **Whitespace rhythm** — Mix busy and minimal posts
5. **Brand element** — Consistent logo placement or watermark style

## Design Anti-Patterns

1. **Text-only posts** — Low engagement unless styled graphically
2. **Stock photo generic** — Recognized instantly, undermines authenticity
3. **Inconsistent branding** — Random colors/fonts per post
4. **Over-designed** — Too many effects competing for attention
5. **Tiny text on stories** — Must be readable at phone-arm distance
6. **Ignoring safe zones** — Text hidden behind system UI
7. **Cluttered carousels** — More than one idea per slide
