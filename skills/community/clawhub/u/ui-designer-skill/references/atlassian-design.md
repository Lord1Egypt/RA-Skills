# Atlassian Design System

Collaborative design system for Jira, Confluence, Trello, Bitbucket.

## Design Principles

- **Bold, Optimistic, Practical**: Confident, positive, task-focused
- **Approachable**: Plain language, clear hierarchy, forgiving errors
- **Trustworthy**: Predictable patterns, consistent behavior, professional

## Color System

| Type | Name | Hex | Usage |
|------|------|-----|-------|
| Primary | Blue 500 | #0052CC | Actions, links, brand |
| Hover | Blue 600 | #0747A6 | Interactive hover |
| Success | Green | #00875A | Success states |
| Warning | Yellow | #FFAB00 | Warning states |
| Error | Red | #DE350B | Error states |
| Info | Blue 400 | #0065FF | Info messages |

### Neutrals
N0-N900: #FFFFFF → #091E42 (14 shades)

## Typography

| Scale | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| Heading XXL | 35px | 500 | 40px | Major sections |
| Heading XL | 29px | 500 | 32px | Page titles |
| Heading L | 24px | 500 | 28px | Section headers |
| Heading M | 20px | 500 | 24px | Subsections |
| Heading S | 16px | 600 | 20px | Card titles |
| Body | 14px | 400 | 20px | Main content |
| Caption | 12px | 400 | 16px | Labels, hints |

**Font:** -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif

## Spacing

**Base unit:** 8px  
**Scale:** 2px, 4px, 6px, 8px, 12px, 16px, 24px, 32px, 40px, 48px  
**Tokens:** space-025 (2px), space-100 (8px), space-200 (16px), space-300 (24px)

## Shadows

```css
raised: 0 1px 1px rgba(9,30,66,0.25), 0 0 1px rgba(9,30,66,0.31)
overflow: 0 4px 8px -2px rgba(9,30,66,0.25), 0 0 1px rgba(9,30,66,0.31)
overlay: 0 8px 12px -4px rgba(9,30,66,0.25), 0 0 1px rgba(9,30,66,0.31)
```

## Border Radius

Small: 3px | Default: 3px | Large: 8px | Circle: 50%

## Quick Examples

### Button
```html
<!-- Primary -->
<button class="px-4 h-8 bg-[#0052CC] hover:bg-[#0747A6] text-white text-sm rounded-sm">
  Create issue
</button>
```

### Input
```html
<input class="w-full h-10 px-2 bg-[#FAFBFC] border-2 border-[#DFE1E6] 
  hover:border-[#B3BAC5] focus:border-[#0052CC] rounded-sm text-sm"/>
```

### Card
```html
<div class="p-4 bg-white border border-[#DFE1E6] rounded-sm 
  shadow-[0_1px_1px_rgba(9,30,66,0.25)]">
  Card content
</div>
```

Full component library: `assets/components/atlassian-*.md`

## Grid System

8-column responsive grid | Gutter: 32px default, 16px small screens

## Accessibility

- **WCAG 2.1 AA**: 4.5:1 contrast minimum
- **Focus**: 2px solid ring, #0065FF
- **Keyboard**: All components navigable
- **Touch**: 44px minimum target

## Tailwind Config

```js
colors: {
  atlassian: {
    blue: { 500: '#0052CC', 600: '#0747A6' },
    neutral: { 0: '#FFFFFF', 800: '#172B4D', 900: '#091E42' },
    success: '#00875A', warning: '#FFAB00', error: '#DE350B'
  }
},
spacing: { '0.5': '2px', '1.5': '6px' },
boxShadow: {
  'atlassian-raised': '0 1px 1px rgba(9,30,66,0.25), 0 0 1px rgba(9,30,66,0.31)'
}
```

## Reference

**Full components:** `assets/components/atlassian-components.md`  
**Official:** https://atlassian.design
