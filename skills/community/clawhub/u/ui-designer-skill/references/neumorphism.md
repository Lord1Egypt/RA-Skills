# Neumorphism (Soft UI)

Minimalist design combining skeuomorphism and flat design, creating soft extruded shapes from backgrounds using subtle dual shadows.

## Core Principles

- **Background Unity**: Elements appear carved from or extruded out of background
- **Dual Shadow System**: Light (top-left) + Dark (bottom-right) shadows create depth
- **Subtle Contrast**: Low contrast, monochromatic or near-monochromatic palettes
- **Minimalist Forms**: Clean geometric shapes, large rounded corners

## Color System

### Light Theme
| Type | Hex | Usage |
|------|-----|-------|
| Background | #E0E5EC | Base surface |
| Light | #FFFFFF | Light shadow |
| Dark | #A3B1C6 | Dark shadow |
| Text Primary | #4A5568 | Body text |
| Accent Blue | #667EEA | Interactive |

### Dark Theme
Background: #2D3748 | Light: #4A5568 | Dark: #1A202C

## Typography

**Font:** 'Inter', 'SF Pro', -apple-system, system-ui, sans-serif  
**Scale:** Large: 32px/600 | Heading: 24px/600 | Body: 16px/400 | Small: 14px/400

## Spacing

**Base:** 8px | **Scale:** 4, 8, 12, 16, 24, 32, 40, 48, 64, 80

## Border Radius

Small: 8px | Medium: 12px | Large: 16px | XL: 24px | Circular: 50%

## Shadow System

### Convex (Raised)
```css
raised: 8px 8px 16px rgba(163,177,198,0.6), -8px -8px 16px rgba(255,255,255,0.5)
subtle: 4px 4px 8px rgba(163,177,198,0.4), -4px -4px 8px rgba(255,255,255,0.4)
```

### Concave (Pressed)
```css
pressed: inset 4px 4px 8px rgba(163,177,198,0.5), inset -4px -4px 8px rgba(255,255,255,0.5)
deep: inset 8px 8px 16px rgba(163,177,198,0.6), inset -8px -8px 16px rgba(255,255,255,0.5)
```

## Quick Examples

### Button
```html
<button class="px-8 py-3 bg-[#E0E5EC] text-[#4A5568] rounded-2xl
  shadow-[8px_8px_16px_rgba(163,177,198,0.6),-8px_-8px_16px_rgba(255,255,255,0.5)]
  active:shadow-[inset_4px_4px_8px_rgba(163,177,198,0.5)]">
  Button
</button>
```

### Input
```html
<input class="w-full px-4 py-3 bg-[#E0E5EC] rounded-xl
  shadow-[inset_4px_4px_8px_rgba(163,177,198,0.5),inset_-4px_-4px_8px_rgba(255,255,255,0.5)]"/>
```

### Card
```html
<div class="p-8 bg-[#E0E5EC] rounded-3xl
  shadow-[8px_8px_16px_rgba(163,177,198,0.6),-8px_-8px_16px_rgba(255,255,255,0.5)]">
  Card
</div>
```

Full components: `assets/components/neumorphism-*.md`

## Accessibility

⚠️ **Contrast Issues**: Neumorphism's low contrast can hurt accessibility
- **Text**: Ensure 4.5:1 contrast minimum (darker text colors)
- **Focus**: Add clear 2px solid #667EEA outline, offset 2px
- **Borders**: Consider adding subtle borders for better definition
- **Alternative**: Combine with color changes on interaction

## Best Practices

- Monochromatic palette (same color family)
- Large border radius (12px+)
- Subtle shadow intensity
- Limited use (hero sections, cards, not entire interfaces)
- Test accessibility tools

## Tailwind Config

```js
colors: {
  neu: { bg: '#E0E5EC', light: '#FFFFFF', dark: '#A3B1C6', text: '#4A5568', blue: '#667EEA' }
},
boxShadow: {
  'neu-raised': '8px 8px 16px rgba(163,177,198,0.6), -8px -8px 16px rgba(255,255,255,0.5)',
  'neu-pressed': 'inset 4px 4px 8px rgba(163,177,198,0.5), inset -4px -4px 8px rgba(255,255,255,0.5)'
}
```
