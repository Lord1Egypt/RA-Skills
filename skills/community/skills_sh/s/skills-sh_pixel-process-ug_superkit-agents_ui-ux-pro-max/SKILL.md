---
name: ui-ux-pro-max
description: >
  Use when the user needs full UI/UX design intelligence — styles, palettes, fonts, UX guidelines,
  chart selection, and accessible, performant implementation across any supported stack. Triggers:
  user says "design", "UI", "UX", "color palette", "typography", "accessibility", "responsive design",
  "chart type", "style guide", building any user-facing interface.
---

# UI/UX Pro Max

## Overview

A comprehensive UI/UX design intelligence system that combines visual design expertise with engineering rigor. This skill provides opinionated, production-ready guidance covering style selection, color palettes, typography, UX heuristics, data visualization, and multi-stack implementation. Every recommendation is filtered through a strict priority hierarchy that ensures accessibility and performance are never sacrificed for aesthetics.

## Phase 1: Requirements Gathering

1. Identify the product type and target audience
2. Determine platform(s) (web, mobile, desktop)
3. Assess existing brand guidelines or design system
4. Define accessibility requirements
5. Set performance budgets

**STOP — Confirm requirements with user before making design recommendations.**

### Priority Hierarchy (Non-Negotiable Order)

Do NOT skip or reorder these priorities. Accessibility always comes first.

1. **Accessibility** — WCAG 2.1 AA minimum, AAA preferred
   - Contrast ratio: 4.5:1 for normal text, 3:1 for large text
   - Keyboard navigation: all interactive elements focusable, visible focus ring
   - ARIA labels on all non-text controls
   - Screen reader announcements for dynamic content
   - Reduced motion: respect `prefers-reduced-motion`
2. **Touch Targets** — 44x44px minimum (Apple HIG / WCAG 2.5.5)
   - Spacing between targets: minimum 8px
   - Clickable area may exceed visual bounds via padding
3. **Performance**
   - Images: WebP with AVIF fallback, lazy loading below fold
   - CLS < 0.1, LCP < 2.5s, FID < 100ms
   - Font loading: `font-display: swap`, preload critical fonts
   - Bundle: code-split routes, tree-shake unused components
4. **Style** — Applied only after 1-3 are satisfied
5. **Layout** — Composition and spacing applied last

## Phase 2: Style Selection

**STOP — Present style recommendation with rationale before proceeding to implementation.**

### Style Selection Decision Table

| Context | Recommended Styles | Why |
|---|---|---|
| SaaS Dashboard | Minimalism, Swiss, Material 3 | Clean, data-focused, professional |
| Portfolio | Brutalism, Maximalism, Glassmorphism | Expressive, memorable |
| E-commerce | Clean, Material 3, Swiss | Trust, clarity, conversion |
| Mobile App | Material 3, Neumorphism, Minimalism | Native feel, thumb-friendly |
| Landing Page | Glassmorphism, Neo-Brutalism, Japandi | Visual impact, hero focus |
| Enterprise/B2B | Swiss Design, Minimalism | Authority, information density |
| Creative Agency | Maximalism, Brutalism, Cyberpunk | Uniqueness, portfolio showcase |
| Health/Wellness | Japandi, Minimalism | Calming, trustworthy |
| Finance | Swiss, Material 3 | Conservative, professional |
| Kids/Family | Claymorphism, Maximalism | Playful, engaging |

### Style Reference (Key Categories)

**Glass and Transparency:**
- Glassmorphism: `backdrop-filter: blur(10px)`, semi-transparent backgrounds, subtle border
- Frosted Glass: heavier blur (20px+), lower opacity, works on busy backgrounds
- Acrylic (Fluent Design): noise texture overlay + blur

**Minimal and Clean:**
- Minimalism: maximum whitespace, single accent color, limited element count
- Swiss Design: grid-based, Helvetica/Grotesk, asymmetric balance
- Japandi: warm neutrals, organic shapes, hidden complexity

**Bold and Expressive:**
- Brutalism: raw, exposed structure, system fonts, harsh borders, no border-radius
- Neo-Brutalism: brutalism + bright accent colors + drop shadows
- Maximalism: layered textures, mixed fonts, dense information

**Depth and Dimension:**
- Neumorphism: soft inner/outer shadows on same-color backgrounds
- Material Design 3: elevation tokens, tonal surfaces, dynamic color
- Claymorphism: inflated 3D look, pastel colors, inner shadows

**Dark and Moody:**
- Dark Mode: OLED-safe (#000 backgrounds), muted primaries, reduced brightness
- Cyberpunk: neon on dark, glitch effects, monospace accents
- Noir: high contrast, grayscale with single accent

## Phase 3: Color and Typography

**STOP — Present palette and font pairing for approval before building components.**

### Color Palette Selection Rules

| Palette Category | Product Types | Characteristics |
|---|---|---|
| SaaS/B2B (24 palettes) | Dashboards, admin tools | Professional blues, teals, slates |
| E-commerce (20 palettes) | Shops, marketplaces | Warm, trust-building ambers, greens |
| Health/Wellness (18 palettes) | Health apps, meditation | Calming greens, soft blues, lavender |
| Finance (15 palettes) | Banking, trading | Deep blues, golds, conservative neutrals |
| Creative (22 palettes) | Portfolios, agencies | Bold, saturated, unexpected combos |
| Social (16 palettes) | Communities, social apps | Vibrant, energetic, gradient-friendly |
| Education (14 palettes) | Learning, courses | Friendly, approachable, moderate saturation |
| Enterprise (12 palettes) | Corporate tools | Muted, authoritative, high-contrast |
| Kids/Family (10 palettes) | Children's apps | Bright primaries, rounded, playful |
| Luxury (10 palettes) | Premium brands | Black, gold, minimal, high whitespace |

### Color Token Rules

- Primary: brand identity color, used for CTAs and key actions
- Secondary: complementary, used for secondary actions and accents
- Neutral: gray scale for text, borders, backgrounds (minimum 9 shades)
- Semantic: success (#22C55E), warning (#F59E0B), error (#EF4444), info (#3B82F6)
- Always define as semantic tokens: `--color-action-primary`, not `--color-blue-500`

### Dark Mode Palette Rules

| Rule | Implementation |
|---|---|
| Do NOT invert colors | Remap to dark-appropriate equivalents |
| Reduce saturation 10-20% | Prevent eye strain on dark backgrounds |
| Elevation = lighter surface | Not shadow-based like light mode |
| Text hierarchy | #E2E8F0 (primary), #94A3B8 (secondary), #64748B (tertiary) |

### Font Pairings (Top 10)

| Pairing | Best For |
|---|---|
| Inter + Source Serif 4 | SaaS, dashboards |
| Geist + Geist Mono | Developer tools, technical |
| DM Sans + DM Serif Display | Marketing, editorial |
| Plus Jakarta Sans + Lora | Modern professional |
| Outfit + Newsreader | Creative agencies |
| Manrope + Bitter | Enterprise applications |
| Space Grotesk + Space Mono | Tech startups |
| Satoshi + Erode | Premium/luxury |
| General Sans + Gambetta | Editorial/publishing |
| Cabinet Grotesk + Zodiak | Bold branding |

### Typography Scale (Default)

```
--text-xs: 0.75rem / 1rem
--text-sm: 0.875rem / 1.25rem
--text-base: 1rem / 1.5rem
--text-lg: 1.125rem / 1.75rem
--text-xl: 1.25rem / 1.75rem
--text-2xl: 1.5rem / 2rem
--text-3xl: 1.875rem / 2.25rem
--text-4xl: 2.25rem / 2.5rem
```

## Phase 4: UX Guidelines Application

### Navigation Rules

1. Primary navigation: maximum 7 items (Miller's Law)
2. Current location always indicated (breadcrumb or active state)
3. Back button must always work as expected
4. Search available on every page for content-heavy apps

### Form Rules

5. Labels above inputs, never placeholder-only
6. Inline validation on blur, not on keystroke
7. Error messages: specific, actionable, adjacent to field
8. Auto-focus first field on page load
9. Submit button disabled until form valid (with explanation)
10. Progress indicator for multi-step forms

### Feedback Rules

11. Loading states for any action > 300ms
12. Skeleton screens over spinners for content loading
13. Toast notifications: auto-dismiss success (3s), persist errors
14. Tap feedback: 80-150ms response time
15. Optimistic UI for low-risk actions

### Content Layout Rules

16. F-pattern for text-heavy pages
17. Z-pattern for landing pages
18. Above-the-fold: value proposition + primary CTA
19. One primary CTA per viewport

### Mobile Rules

20. Bottom navigation for primary actions (thumb zone)
21. Pull-to-refresh for feed content
22. Swipe gestures with visual affordance

## Phase 5: Implementation

### Chart Type Selection Decision Table

| Data Relationship | Chart Types |
|---|---|
| Comparison | Bar, Grouped Bar, Lollipop, Dot Plot |
| Trend over Time | Line, Area, Sparkline, Step |
| Part-to-Whole | Pie (max 5 slices), Donut, Treemap, Stacked Bar |
| Distribution | Histogram, Box Plot, Violin, Density |
| Correlation | Scatter, Bubble, Heatmap |
| Flow/Process | Sankey, Funnel, Waterfall |
| Geographic | Choropleth, Dot Map, Cartogram |
| Hierarchical | Sunburst, Icicle |

### Supported Stacks

| Stack | Key Patterns |
|---|---|
| React | JSX components, hooks, CSS Modules / Tailwind |
| Next.js | App Router, Server Components, Image optimization |
| Vue | Composition API, `<script setup>`, Pinia |
| Svelte | Reactive declarations, transitions, SvelteKit |
| SwiftUI | Declarative views, ViewModifiers, @State/@Binding |
| React Native | Flexbox, Platform.select, SafeAreaView |
| Flutter | Widgets, Material/Cupertino, MediaQuery |
| Tailwind CSS | Utility-first, @apply sparingly, design tokens via config |
| shadcn/ui | Radix primitives, Tailwind variants, cn() utility |
| HTML/CSS | Semantic HTML5, CSS Grid/Flexbox, custom properties |

### Design Token Architecture

```
master.tokens.json    -> Primitive values (colors, spacing, fonts)
semantic.tokens.json  -> Mapped meanings (action-primary, surface-elevated)
component.tokens.json -> Component-specific (button-padding, card-radius)
overrides/
  brand-a.tokens.json -> Brand-specific overrides
  dark.tokens.json    -> Dark mode overrides
```

- Master tokens are read-only defaults
- Overrides are shallow-merged at runtime
- Component tokens reference semantic tokens only
- Never reference primitive tokens in components

## Quick Wins Checklist

- [ ] No emoji as icons — use Lucide React or Heroicons
- [ ] Tap feedback delay: 80-150ms
- [ ] Semantic color tokens (not raw hex values)
- [ ] 8dp spacing rhythm (4, 8, 12, 16, 24, 32, 48, 64)
- [ ] `prefers-color-scheme` media query for dark mode
- [ ] `prefers-reduced-motion` for animations
- [ ] `:focus-visible` instead of `:focus` for keyboard-only focus
- [ ] Image aspect ratios set to prevent CLS
- [ ] Font preloading for above-the-fold text
- [ ] `loading="lazy"` on below-fold images

## Anti-Patterns / Common Mistakes

| Anti-Pattern | Why It Is Wrong | What to Do Instead |
|---|---|---|
| `opacity` for disabled text | Kills readability | Use distinct disabled color token |
| Fixed pixel breakpoints only | Ignores component context | Use container queries for components |
| Hamburger menus on desktop | Hides primary navigation | Visible nav bar on desktop |
| Carousel for critical content | Most users see only first slide | Use static layout or accordion |
| Infinite scroll without URL persistence | Cannot share or return to position | Persist scroll position in URL |
| Modal on modal | Confusing, accessibility nightmare | Redesign to avoid nested modals |
| Auto-playing media | Annoying, accessibility violation | Require user interaction to play |
| Color as only differentiator | Color-blind users excluded | Add shape/pattern/text labels |
| Placeholder-only labels | Disappear on input, accessibility issue | Use visible labels above inputs |
| Raw hex values in components | Impossible to theme | Use semantic design tokens |

## Integration Points

| Skill | Integration |
|---|---|
| `ui-design-system` | Token architecture and component library |
| `canvas-design` | Data visualization and charts |
| `mobile-design` | Mobile-specific design patterns |
| `ux-researcher-designer` | User research informs design decisions |
| `artifacts-builder` | Standalone prototypes and demos |
| `senior-frontend` | Implementation of UI components |
| `accessibility` | WCAG compliance validation |

## Skill Type

**FLEXIBLE** — Follow the priority hierarchy (accessibility > touch > performance > style > layout). Style recommendations adapt to context. Accessibility and performance rules are strongly recommended and should not be deprioritized.
