# Shopify Polaris

Merchant-focused design system for e-commerce and admin interfaces.

## Design Principles

- **Fresh**: Modern, clean aesthetic that feels trustworthy
- **Efficient**: Optimize for merchant productivity and task completion
- **Considerate**: Thoughtful, inclusive design for all merchants
- **Trustworthy**: Reliable, predictable experiences merchants can depend on

## Color System

| Type | Hex | Usage |
|------|-----|-------|
| Teal (Brand) | #008060 | Actions, brand |
| Dark Teal | #004C3F | Hover |
| Interactive | #2C6ECB | Links, secondary actions |
| Critical | #D82C0D | Errors, destructive |
| Warning | #FFC453 | Warnings |
| Success | #008060 | Success |

### Neutrals
Sky: #F4F6F8 | Surface: #FFFFFF | Ink: #202223 | Border: #C9CCCF  
Text Subdued: #6D7175 | Text Disabled: #8C9196

## Typography

| Scale | Size | Weight | Usage |
|-------|------|--------|-------|
| Heading 2XL | 28px | 600 | Major sections |
| Heading XL | 24px | 600 | Page titles |
| Heading LG | 20px | 600 | Sections |
| Heading MD | 16px | 600 | Subsections |
| Body LG | 16px | 400 | Prominent |
| Body MD | 14px | 400 | Content |
| Body SM | 13px | 400 | Dense |

**Font:** -apple-system, 'San Francisco', 'Segoe UI', Roboto, sans-serif

## Spacing

**Base:** 4px (0.25rem) | **Scale:** 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80

## Shadows

```css
100: 0 1px 0 0 rgba(0,0,0,0.05)
200: 0 3px 6px -3px rgba(23,24,24,0.08), 0 8px 20px -4px rgba(23,24,24,0.12)
300: 0 4px 8px -2px rgba(23,24,24,0.08), 0 12px 32px -4px rgba(23,24,24,0.12)
```

## Border Radius

Small: 4px | Base: 8px | Large: 12px | Full: 9999px

## Quick Examples

### Button
```html
<button class="px-4 h-9 bg-[#008060] hover:bg-[#004C3F] text-white 
  rounded-lg shadow-[0_1px_0_0_rgba(0,0,0,0.05)]">
  Save
</button>
```

### Card
```html
<div class="p-5 bg-white border border-[#E1E3E5] rounded-lg 
  shadow-[0_1px_0_0_rgba(0,0,0,0.05)]">
  Card
</div>
```

Full components: `assets/components/polaris-*.md`

## Accessibility

- **WCAG 2.1 AA**: 4.5:1 text minimum
- **Focus**: 2px solid #008060, offset 2px
- **Keyboard**: All components accessible
- **Merchant-first**: Clear labels, helpful errors

## Tailwind Config

```js
colors: {
  polaris: {
    teal: '#008060',
    ink: '#202223',
    sky: '#F4F6F8',
    interactive: '#2C6ECB',
    critical: '#D82C0D'
  }
}
```

## Reference

**Components:** `assets/components/polaris-components.md`  
**Official:** https://polaris.shopify.com
