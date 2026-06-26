# Skeuomorphism

Design approach mimicking real-world objects using realistic textures, shadows, reflections, and dimensional details.

## Core Principles

- **Real-World Mimicry**: Digital elements imitate physical counterparts
- **Rich Detail**: Complex gradients, lighting, textures create authenticity
- **Depth & Dimension**: Layered elements create tangible 3D space
- **Material Authenticity**: Surfaces look and feel like real materials

## Color System

### Material Tones
| Material | Colors | Usage |
|----------|--------|-------|
| Leather | #3E2723, #5D4037, #8D6E63 | Dark to tan tones |
| Wood | #4E342E, #795548, #A1887F | Walnut to maple |
| Metal | #37474F, #546E7A, #90A4AE | Steel to chrome |
| Fabric | #1B5E20, #0D47A1, #880E4F | Green, navy, burgundy |

### Accent
Gold: #FFB300 | Copper: #BF360C | Bronze: #6D4C41 | Silver: #BDBDBD

## Typography

**Font:** 'Playfair Display', 'Futura', 'Avenir', 'Helvetica Neue', serif/sans-serif  
**Scale:** Display: 48px/700 | Large: 36px/600 | Heading: 28px/600 | Body: 16px/400

## Spacing

**Traditional:** 4, 8, 12, 16, 20, 24, 32, 40, 48, 64

## Border Radius

Realistic curves: Tight: 2px | Subtle: 4px | Medium: 8px | Rounded: 12px | Pill: 9999px

## Shadow & Lighting

### Raised Elements
```css
leather-btn: 0 1px 0 rgba(255,255,255,0.4) inset, 0 -1px 0 rgba(0,0,0,0.2) inset,
            0 4px 8px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2)
glossy-btn: 0 1px 3px rgba(0,0,0,0.12), inset 0 1px 0 rgba(255,255,255,0.5)
wood-panel: 0 2px 4px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.1)
```

### Inset/Pressed
```css
recessed: inset 0 2px 4px rgba(0,0,0,0.6), inset 0 1px 2px rgba(0,0,0,0.4),
         0 1px 0 rgba(255,255,255,0.1)
```

## Texture Effects

### Leather
```css
background: linear-gradient(135deg, #5D4037 0%, #3E2723 100%);
background-image: repeating-linear-gradient(45deg, transparent, transparent 2px, 
  rgba(0,0,0,.05) 2px, rgba(0,0,0,.05) 4px);
```

### Brushed Metal
```css
background: linear-gradient(180deg, #546E7A 0%, #37474F 100%);
background-image: repeating-linear-gradient(0deg, rgba(255,255,255,0) 0px,
  rgba(255,255,255,0.03) 1px, rgba(0,0,0,0.03) 2px, rgba(255,255,255,0) 3px);
```

Full texture library: `assets/textures/skeuomorphism-*.md`

## Quick Examples

### Leather Button
```html
<button class="px-6 py-3 rounded-lg text-white font-semibold relative overflow-hidden
  [background:linear-gradient(135deg,#5D4037_0%,#3E2723_100%)]
  shadow-[0_4px_8px_rgba(0,0,0,0.4),inset_0_1px_0_rgba(255,255,255,0.2)]">
  Leather
</button>
```

### Glossy Button
```html
<button class="px-6 py-3 rounded-full bg-gradient-to-b from-[#4CAF50] to-[#2E7D32]
  shadow-[0_4px_8px_rgba(0,0,0,0.3),inset_0_1px_0_rgba(255,255,255,0.4)]
  text-white font-semibold relative overflow-hidden
  before:content-[''] before:absolute before:top-0 before:left-0 before:right-0 before:h-1/2
  before:bg-gradient-to-b before:from-white/40 before:to-transparent before:rounded-t-full">
  Glossy
</button>
```

Full components: `assets/components/skeuomorphism-*.md`

## Accessibility

- **High Contrast**: Ensure 4.5:1 text contrast
- **Test Grayscale**: Verify hierarchy without color
- **Focus**: 3px solid #FFD700 outline, offset 2px
- **Semantic Colors**: Use for status indicators

## Best Practices

- Use sparingly (specific UI elements, not entire interfaces)
- Performance: Complex gradients/shadows can impact rendering
- Context: Best for creative, artistic, or nostalgic applications
- Commit to aesthetic throughout

## Tailwind Config

```js
colors: {
  leather: { dark: '#3E2723', medium: '#5D4037', tan: '#8D6E63' },
  wood: { walnut: '#4E342E', oak: '#795548', maple: '#A1887F' },
  metal: { steel: '#37474F', brushed: '#546E7A', chrome: '#90A4AE' }
}
```

## Reference

**Textures:** `assets/textures/skeuomorphism-textures.md`  
**Components:** `assets/components/skeuomorphism-components.md`
