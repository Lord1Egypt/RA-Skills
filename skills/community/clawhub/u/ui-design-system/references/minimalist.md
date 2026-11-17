# Minimalist — Premium Utilitarian UI

> Clean editorial-style interfaces. Warm monochrome palette, typographic contrast, flat bento grids, muted pastels. No gradients, no heavy shadows.

---

## Protocol Overview

**Name:** Premium Utilitarian Minimalism & Editorial UI

**Description:** Advanced frontend engineering directive for generating highly refined, ultra-minimalist, "document-style" web interfaces analogous to top-tier workspace platforms (Notion, Linear). Strictly enforces:
- High-contrast warm monochrome palette
- Bespoke typographic hierarchies
- Meticulous structural macro-whitespace
- Bento-grid layouts
- Ultra-flat component architecture with deliberate muted pastel accents

---

## Absolute Negative Constraints (Banned Elements)

### Typography Bans
- DO NOT use "Inter", "Roboto", or "Open Sans" typefaces
- DO NOT use generic placeholder names like "John Doe", "Acme Corp", or "Lorem Ipsum"

### Icon Bans
- DO NOT use generic thin-line icon libraries like "Lucide", "Feather", or standard "Heroicons"

### Shadow Bans
- DO NOT use Tailwind's default heavy drop shadows (`shadow-md`, `shadow-lg`, `shadow-xl`)
- Shadows must be practically non-existent or heavily customized (ultra-diffuse, opacity < 0.05)

### Color Bans
- DO NOT use primary colored backgrounds for large elements (no bright blue, green, or red hero sections)
- DO NOT use gradients, neon colors, or 3D glassmorphism (beyond subtle navbar blurs)

### Shape Bans
- DO NOT use `rounded-full` (pill shapes) for large containers, cards, or primary buttons

### Content Bans
- DO NOT use emojis anywhere in code, markup, text content, headings, or alt text
- DO NOT use AI copywriting clichés: "Elevate", "Seamless", "Unleash", "Next-Gen", "Game-changer", "Delve"

---

## Typographic Architecture

The interface relies on extreme typographic contrast and premium font selection.

### Font Stack

| Role | Font Family |
|------|-------------|
| **Primary Sans (Body, UI, Buttons)** | `SF Pro Display`, `Geist Sans`, `Helvetica Neue`, `Switzer`, sans-serif |
| **Editorial Serif (Hero Headings & Quotes)** | `Lyon Text`, `Newsreader`, `Playfair Display`, `Instrument Serif`, serif |
| **Monospace (Code, Keystrokes, Meta-data)** | `Geist Mono`, `SF Mono`, `JetBrains Mono`, monospace |

### Typography Parameters

- **Serif Headings:** Tight tracking (`letter-spacing: -0.02em` to `-0.04em`), tight line-height (`1.1`)
- **Body Text:** Never absolute black (`#000000`). Use off-black/charcoal (`#111111` or `#2F3437`) with generous `line-height: 1.6`
- **Secondary Text:** Muted gray (`#787774`)

---

## Color Palette (Warm Monochrome + Spot Pastels)

Color is a scarce resource, utilized only for semantic meaning or subtle accents.

### Base Colors

| Role | Color |
|------|-------|
| Canvas / Background | Pure White `#FFFFFF` or Warm Bone `#F7F6F3` / `#FBFBFA` |
| Primary Surface (Cards) | `#FFFFFF` or `#F9F9F8` |
| Structural Borders / Dividers | Ultra-light gray `#EAEAEA` or `rgba(0,0,0,0.06)` |

### Accent Colors (Muted Pastels)

Exclusively for tags, inline code backgrounds, or subtle icon backgrounds.

| Accent | Background | Text |
|--------|------------|------|
| Pale Red | `#FDEBEC` | `#9F2F2D` |
| Pale Blue | `#E1F3FE` | `#1F6C9F` |
| Pale Green | `#EDF3EC` | `#346538` |
| Pale Yellow | `#FBF3DB` | `#956400` |

---

## Component Specifications

### Bento Box Feature Grids
- Asymmetrical CSS Grid layouts
- Cards: exactly `border: 1px solid #EAEAEA`
- Border-radius: crisp `8px` or `12px` maximum
- Internal padding: generous (`24px` to `40px`)

### Primary Call-To-Action (Buttons)
- Solid background `#111111`, text `#FFFFFF`
- Slight border-radius (`4px` to `6px`). No box-shadow
- Hover: subtle color shift to `#333333` or micro-scale `transform: scale(0.98)`

### Tags & Status Badges
- Pill-shaped (`border-radius: 9999px`)
- Very small typography (`text-xs`), uppercase with wide tracking (`letter-spacing: 0.05em`)
- Background: Muted Pastels defined above

### Accordions (FAQ)
- Strip all container boxes
- Separate items only with `border-bottom: 1px solid #EAEAEA`
- Clean, sharp `+` and `-` icon for toggle state

### Keystroke Micro-UIs
- Render shortcuts as physical keys using `<kbd>` tags
- `border: 1px solid #EAEAEA`, `border-radius: 4px`, `background: #F7F6F3`
- Use Monospace font

### Faux-OS Window Chrome
- When mocking up software, wrap in minimalist container with white top bar
- Three small, light gray circles (replicating macOS window controls)

---

## Iconography & Imagery

### System Icons
- Use **Phosphor Icons (Bold or Fill weights)** or **Radix UI Icons**
- Standardize stroke width across all icons

### Illustrations
- Monochromatic, rough continuous-line ink sketches on white background
- Single offset geometric shape filled with muted pastel color

### Photography
- High-quality, desaturated images with warm tone
- Apply subtle overlays (`opacity: 0.04` warm grain) to blend into monochrome palette
- Use `https://picsum.photos/seed/{context}/1200/800` when real assets unavailable

### Hero & Section Backgrounds
- Subtle full-width background imagery at very low opacity
- Soft radial light spots (`radial-gradient` with warm tones at `opacity: 0.03`)
- Minimal geometric line patterns to add depth without breaking clean aesthetic

---

## Subtle Motion & Micro-Animations

Motion should feel invisible — present but never distracting.

### Scroll Entry
- Elements fade in gently as they enter viewport
- `translateY(12px)` + `opacity: 0` resolving over `600ms` with `cubic-bezier(0.16, 1, 0.3, 1)`
- Use `IntersectionObserver`, never `window.addEventListener('scroll')`

### Hover States
- Cards: ultra-subtle shadow shift (`box-shadow` from `0 0 0` to `0 2px 8px rgba(0,0,0,0.04)` over `200ms`)
- Buttons: `scale(0.98)` on `:active`

### Staggered Reveals
- Lists and grid items enter with cascade delay (`animation-delay: calc(var(--index) * 80ms)`)
- Never mount everything at once

### Background Ambient Motion (Optional)
- Single, very slow-moving radial gradient blob (`animation-duration: 20s+`, `opacity: 0.02-0.04`)
- Applied to `position: fixed; pointer-events: none` layer
- Never on scrolling containers

### Performance
- Animate exclusively via `transform` and `opacity`
- No layout-triggering properties (`top`, `left`, `width`, `height`)
- Use `will-change: transform` sparingly

---

## Execution Protocol

1. Establish macro-whitespace first. Use massive vertical padding (`py-24` or `py-32`)
2. Constrain main typography content width to `max-w-4xl` or `max-w-5xl`
3. Apply custom typographic hierarchy and monochromatic color variables
4. Ensure every card, divider, and border adheres to `1px solid #EAEAEA` rule
5. Add scroll-entry animations to all major content blocks
6. Ensure sections have visual depth through imagery, ambient gradients, or subtle textures
7. Provide code reflecting high-end, uncluttered, editorial aesthetic

---

*Part of ui-styles skill v1.0.0 — adapted from taste-skill minimalist-skill*
