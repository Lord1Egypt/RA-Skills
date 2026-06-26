# Ant Design System

Enterprise-class UI design by Alibaba for natural, efficient experiences.

## Design Principles

- **Natural**: Inspired by nature's laws, familiar interactions
- **Certain**: Grounded decisions, clear hierarchy, predictable behavior
- **Meaningful**: Purpose-driven, task-focused, no waste
- **Growing**: Evolves with feedback, scalable architecture

## Color System

| Type | Hex | Usage |
|------|-----|-------|
| Ant Blue 6 | #1677FF | Primary actions |
| Blue 7 | #0958D9 | Hover |
| Blue 8 | #003EB3 | Active |
| Success | #52C41A | Success states |
| Warning | #FAAD14 | Warnings |
| Error | #FF4D4F | Errors |

### Neutrals
Gray 1-10: #FFFFFF → #262626 (10 shades)

## Typography

| Scale | Size | Weight | Usage |
|-------|------|--------|-------|
| H1 | 38px | 600 | Major headings |
| H2 | 30px | 600 | Page titles |
| H3 | 24px | 600 | Sections |
| Body | 14px | 400 | Content |
| Caption | 12px | 400 | Labels |

**Font:** -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif

## Spacing

**Base:** 8px | **Scale:** 4, 8, 12, 16, 24, 32, 40, 48, 64, 80

## Shadows

```css
hover: 0 2px 8px rgba(0,0,0,0.08)
card: 0 1px 2px rgba(0,0,0,0.03), 0 1px 6px -1px rgba(0,0,0,0.02)
dropdown: 0 6px 16px 0 rgba(0,0,0,0.08), 0 3px 6px -4px rgba(0,0,0,0.12)
```

## Border Radius

Small: 2px | Base: 6px | Large: 8px | Circle: 50%

## Grid System

12-column responsive | xs: <576px, sm: ≥576px, md: ≥768px, lg: ≥992px, xl: ≥1200px, xxl: ≥1600px

## Quick Examples

### Button
```html
<button class="px-4 h-8 bg-[#1677FF] hover:bg-[#4096FF] text-white 
  rounded-md shadow-[0_2px_0_rgba(5,145,255,0.1)]">
  Primary
</button>
```

### Card
```html
<div class="p-6 bg-white border border-[#F0F0F0] rounded-lg 
  shadow-[0_1px_2px_rgba(0,0,0,0.03)]">
  Card
</div>
```

Full components: `assets/components/ant-*.md`

## Accessibility

- **WCAG 2.1 AA**: 4.5:1 minimum
- **Focus**: 2px solid #1677FF, offset 2px
- **Keyboard**: Tab order follows visual hierarchy

## Tailwind Config

```js
colors: {
  ant: {
    blue: { 1: '#E6F4FF', 6: '#1677FF', 10: '#001D66' },
    gray: { 2: '#FAFAFA', 5: '#D9D9D9', 10: '#262626' }
  }
}
```

## Reference

**Components:** `assets/components/ant-components.md`  
**Official:** https://ant.design
