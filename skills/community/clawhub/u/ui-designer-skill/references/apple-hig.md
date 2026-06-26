# Apple Human Interface Guidelines (HIG)

Design language for iOS, iPadOS, macOS, emphasizing clarity, deference, and depth.

## Design Principles

- **Clarity**: Legible text, precise icons, obvious functionality
- **Deference**: Content takes precedence over UI, subtle interfaces
- **Depth**: Visual layers, realistic motion enhance understanding

## Color System

| Type | Hex | Usage |
|------|-----|-------|
| iOS Blue | #007AFF | Primary actions |
| Green | #34C759 | Success |
| Red | #FF3B30 | Error/destructive |
| Orange | #FF9500 | Warnings |
| Purple | #AF52DE | Creative |
| Teal | #5AC8FA | Accents |

### Semantics
Label (Light): rgba(0,0,0,1.0) | Label (Dark): rgba(255,255,255,1.0)  
Secondary Label: 60% opacity | Background: #FFFFFF / #000000

## Typography

| Scale | Size | Weight | Usage |
|-------|------|--------|-------|
| Large Title | 34px | 400 | Hero |
| Title 1 | 28px | 400 | Major |
| Title 2 | 22px | 400 | Sections |
| Headline | 17px | 600 | Emphasized |
| Body | 17px | 400 | Content |
| Footnote | 13px | 400 | Details |
| Caption | 12px | 400 | Labels |

**Font:** -apple-system, 'SF Pro Text', 'SF Pro Display', sans-serif  
**Dynamic Type**: Text scales with user preferences

## Spacing

**Points:** 4pt, 8pt, 12pt, 16pt, 20pt, 24pt, 32pt, 44pt (min touch)

## Shadows

```css
subtle: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24)
medium: 0 3px 6px rgba(0,0,0,0.15), 0 2px 4px rgba(0,0,0,0.12)
high: 0 10px 20px rgba(0,0,0,0.15), 0 3px 6px rgba(0,0,0,0.10)
```

## Border Radius

Small: 8pt | Medium: 10pt | Large: 12pt | XL: 16pt | Continuous curve (proprietary)

## Vibrancy & Blur

```css
light-blur: backdrop-filter: blur(20px) saturate(180%); background: rgba(255,255,255,0.72);
dark-blur: backdrop-filter: blur(20px) saturate(180%); background: rgba(28,28,30,0.72);
```

## Quick Examples

### Button
```html
<button class="px-6 py-3 bg-[#007AFF] active:bg-[#0051D5] text-white 
  rounded-xl min-h-[44px] active:scale-[0.97]">
  Continue
</button>
```

### List Item
```html
<div class="px-4 py-3 min-h-[44px] bg-white border-b border-[#C7C7CC]/30 
  active:bg-[#D1D1D6]/50 flex items-center justify-between">
  Item
</div>
```

Full components: `assets/components/apple-*.md`

## Accessibility

- **Dynamic Type**: Support user text size preferences
- **VoiceOver**: All elements labeled, logical order
- **Touch Targets**: 44x44pt minimum
- **Color Contrast**: WCAG AA, test both light/dark modes

## Tailwind Config

```js
colors: {
  ios: {
    blue: '#007AFF', green: '#34C759', red: '#FF3B30',
    gray: { 1: '#8E8E93', 5: '#E5E5EA', 6: '#F2F2F7' }
  }
},
minHeight: { 'touch': '44px' }
```

## Reference

**Components:** `assets/components/apple-components.md`  
**Official:** https://developer.apple.com/design/human-interface-guidelines
