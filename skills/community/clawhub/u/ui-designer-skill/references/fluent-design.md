# Fluent Design System (Microsoft)

Light, depth, motion, material, and scale for intuitive experiences.

## Design Principles

- **Light**: Strategic illumination draws attention, reveals hierarchy
- **Depth**: Z-layering establishes relationships and importance
- **Motion**: Purposeful animation provides feedback (300-500ms)
- **Material**: Acrylic/Mica surfaces create tactile depth
- **Scale**: Adaptive layouts from mobile to desktop (40px min touch)

## Color System

| Type | Hex | Usage |
|------|-----|-------|
| Primary Blue | #0078D4 | Actions, links |
| Dark Blue | #005A9E | Hover states |
| Light Blue | #50E6FF | Accents |
| Success | #107C10 | Success states |
| Warning | #FFC83D | Warnings |
| Error | #D13438 | Errors |

### Neutrals
Gray 10-180: #FAF9F8 → #11100F (18 shades)

## Typography

| Scale | Size | Weight | Usage |
|-------|------|--------|-------|
| Heading Large | 46px | 600 | Hero titles |
| Heading | 28px | 600 | Page titles |
| Subheading | 20px | 600 | Sections |
| Body Large | 18px | 400 | Prominent text |
| Body | 14px | 400 | Content |
| Caption | 12px | 400 | Labels |

**Font:** 'Segoe UI Variable', 'Segoe UI', -apple-system, sans-serif

## Spacing

**Base:** 4px | **Scale:** 4, 8, 12, 16, 20, 24, 28, 32, 36, 40

## Shadows (Elevation)

```css
shadow-2: 0 0.3px 0.9px rgba(0,0,0,0.1), 0 1.6px 3.6px rgba(0,0,0,0.13)
shadow-4: 0 1.2px 3.6px rgba(0,0,0,0.11), 0 6.4px 14.4px rgba(0,0,0,0.13)
shadow-8: 0 3.2px 7.2px rgba(0,0,0,0.13), 0 12.8px 28.8px rgba(0,0,0,0.11)
```

## Border Radius

Small: 2px | Medium: 4px | Large: 8px | XL: 12px | Circle: 9999px

## Acrylic Material

```css
background: rgba(252,252,252,0.7);
backdrop-filter: blur(30px) saturate(125%);
border: 1px solid rgba(0,0,0,0.05);
```

## Quick Examples

### Button
```html
<button class="px-5 py-2.5 bg-[#0078D4] hover:bg-[#005A9E] text-white 
  rounded shadow-[0_0.3px_0.9px_rgba(0,0,0,0.1)] active:scale-[0.98]">
  Primary
</button>
```

### Card with Acrylic
```html
<div class="p-6 bg-white/70 backdrop-blur-[30px] backdrop-saturate-125 
  rounded-lg border border-black/5">
  Acrylic card
</div>
```

Full components: `assets/components/fluent-*.md`

## Accessibility

- **WCAG 2.1 AA**: 4.5:1 minimum
- **Focus**: 2px solid #0078D4, offset 2px
- **Motion**: Respect prefers-reduced-motion

## Tailwind Config

```js
colors: { fluent: { blue: '#0078D4', gray: { 10: '#FAF9F8', 160: '#292827' }}},
boxShadow: { 'fluent-2': '0 0.3px 0.9px rgba(0,0,0,0.1), 0 1.6px 3.6px rgba(0,0,0,0.13)' },
backdropBlur: { 'fluent': '30px' }
```

## Reference

**Components:** `assets/components/fluent-components.md`  
**Official:** https://fluent2.microsoft.design
