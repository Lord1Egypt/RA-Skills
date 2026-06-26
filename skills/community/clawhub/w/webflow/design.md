# Webflow Design Patterns

## Responsive Breakpoints

Webflow breakpoints cascade DOWN. Changes on desktop affect all smaller breakpoints unless overridden.

**Order of work:**
1. Desktop first (base styles)
2. Tablet (991px and down)
3. Mobile landscape (767px and down)
4. Mobile portrait (478px and down)

**Common trap:** Making mobile-only changes on desktop. Always check which breakpoint you're on.

## Class Naming

**Use semantic naming:**
- `hero-section`, `hero-heading`, `hero-cta` ✓
- `div-block-47`, `heading-23-copy` ✗

**Combo classes for variants:**
- Base: `button`
- Variants: `button is-large`, `button is-secondary`

**Never rename auto-generated classes in production.** Create new ones and apply them.

## Layout Patterns

### Flexbox vs Grid
- **Flexbox:** 1-dimensional layouts (nav items, card rows)
- **Grid:** 2-dimensional layouts (gallery, dashboard sections)

### Common Grid Setups
```
12-column layout: 1fr repeat(12, minmax(0, 90px)) 1fr
Auto-fit cards: repeat(auto-fit, minmax(280px, 1fr))
```

## Interactions

**Keep animations under 400ms.** Anything longer feels slow.

**Staggered animations:**
- Set delay increment (0.1s works for most)
- Apply to collection items or sibling elements

**Scroll-triggered:**
- Use "While scrolling in view" for parallax
- Use "Scroll into view" for reveal animations
- Set offset 10-20% to trigger before element is centered

## Figma to Webflow

1. Match Figma's auto-layout → Webflow flexbox settings
2. Export images at 2x for retina
3. Use design tokens (colors, fonts) in Figma → create matching Webflow variables
4. Copy text styles: font-size, line-height, letter-spacing exactly

**Don't auto-import.** Manual class assignment keeps code clean.
