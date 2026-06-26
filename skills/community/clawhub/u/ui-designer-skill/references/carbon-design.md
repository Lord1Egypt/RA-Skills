# Carbon Design System (IBM)

Enterprise design system emphasizing clarity, efficiency, and consistency.

## Design Principles

- **Clarity**: Clear visual hierarchy, purposeful typography
- **Efficiency**: Streamlined workflows, keyboard-first interactions
- **Consistency**: Unified patterns, reusable components
- **Inclusive**: WCAG 2.1 AA, keyboard navigation, screen readers

## Color System

| Type | Hex | Usage |
|------|-----|-------|
| Blue 60 | #0F62FE | Primary actions |
| Blue 70 | #0353E9 | Hover |
| Blue 80 | #002D9C | Active |
| Success | #24A148 | Success |
| Warning | #F1C21B | Warnings |
| Error | #DA1E28 | Errors |

### Neutrals
Gray 10-100: #F4F4F4 → #161616 (10 shades)

## Typography

| Scale | Size | Weight | Usage |
|-------|------|--------|-------|
| Heading 07 | 54px | 300 | Hero |
| Heading 04 | 28px | 400 | Page titles |
| Heading 03 | 20px | 400 | Sections |
| Body 02 | 16px | 400 | Content |
| Body 01 | 14px | 400 | Dense content |
| Label 01 | 12px | 400 | Labels |

**Font:** 'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif  
**Code:** 'IBM Plex Mono', 'Menlo', monospace

## Spacing

**Base:** 16px (1rem) | **Tokens:** 2px, 4px, 8px, 12px, 16px, 24px, 32px, 40px, 48px, 64px, 80px, 96px, 160px

## Shadows

```css
1: 0 1px 2px rgba(0,0,0,0.3)
2: 0 2px 6px rgba(0,0,0,0.3)
3: 0 4px 8px rgba(0,0,0,0.3)
4: 0 8px 16px rgba(0,0,0,0.3)
```

## Border & Radius

Width: 1px (default), 2px (focus) | Radius: 0px (default), 2-8px

## Grid System

16-column responsive | Small: <672px (4 col), Medium: 672-1056px (8 col), Large: 1056-1312px (16 col)

## Quick Examples

### Button
```html
<button class="px-4 h-12 bg-[#0F62FE] hover:bg-[#0353E9] text-white 
  border-2 border-transparent focus:border-white focus:ring-2">
  Primary
</button>
```

### Input
```html
<input class="w-full h-10 px-4 bg-[#F4F4F4] border-b-2 border-[#8D8D8D] 
  focus:bg-white focus:border-[#0F62FE] text-sm"/>
```

Full components: `assets/components/carbon-*.md`

## Accessibility

- **WCAG 2.1 AA**: 4.5:1 text, 3:1 interactive
- **Focus**: 2px solid #0F62FE, offset 2px
- **Keyboard**: Fully accessible

## Tailwind Config

```js
colors: {
  carbon: {
    blue: { 60: '#0F62FE', 70: '#0353E9', 80: '#002D9C' },
    gray: { 10: '#F4F4F4', 80: '#393939', 100: '#161616' }
  }
}
```

## Reference

**Components:** `assets/components/carbon-components.md`  
**Official:** https://carbondesignsystem.com
