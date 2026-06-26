---
name: text-to-svg
description: Generate logos, icons, illustrations and other vector graphics from natural language descriptions. Supports style directives (flat monochrome/gradient/stroke/rounded/minimal/tech). For design mockups, brand logos, UI icons, info illustrations.
---

# Text-to-SVG — Natural Language to SVG Vector Graphic Code

Convert natural language descriptions into runnable SVG vector graphic code.

## Workflow

1. **Parse requirements** — Identify objects, style, colors, dimensions from description
2. **Determine structure** — Choose appropriate SVG element composition (paths/shapes/text/gradients)
3. **Generate code** — Output complete code ready for embedding or saving as `.svg`
4. **Validate output** — Ensure correct SVG syntax, reasonable viewBox, well-balanced colors

## Output Specification

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 300" width="100%" height="100%">
  <!-- content -->
</svg>
```

- **Must include** `viewBox`, prefer square viewports (e.g., `100 100` or `400 400`)
- **Always declare** `xmlns` namespace
- **No external resources** (fonts/images), use built-in geometric shapes
- **Close all tags**, use self-closing tags for brevity `<circle/>` `<path/>`
- **Prefer hex colors** `#2C3E50` or named colors

## Style System

### Flat Monochrome
```svg
<rect x="20" y="20" width="60" height="60" rx="8" fill="#3498DB"/>
```
- No gradients, no shadows, solid fill
- Optional `rx/ry` for rounded corners
- Typical sizes: icons 24×24~64×64, logos 100×100~400×400

### Gradient
```svg
<defs>
  <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
    <stop offset="0%" stop-color="#667EEA"/>
    <stop offset="100%" stop-color="#764BA2"/>
  </linearGradient>
  <radialGradient id="g2" cx="50%" cy="50%" r="50%">
    <stop offset="0%" stop-color="#FF6B6B"/>
    <stop offset="100%" stop-color="#C0392B"/>
  </radialGradient>
</defs>
<circle cx="50" cy="50" r="40" fill="url(#g1)"/>
```

### Stroke Style
```svg
<circle cx="50" cy="50" r="40" fill="none" stroke="#2C3E50" stroke-width="3" stroke-linecap="round"/>
<path d="M20 20 L60 60" stroke="#E74C3C" stroke-width="4" stroke-linejoin="round"/>
```

### Minimal Lines
```svg
<path d="M10 50 Q 30 10, 50 50 T 90 50" fill="none" stroke="#333" stroke-width="2" stroke-linecap="round"/>
```

### Tech / Cyber
```svg
<rect x="10" y="10" width="80" height="80" rx="4" fill="#0a1628" stroke="#00d4ff" stroke-width="1"/>
<circle cx="50" cy="50" r="20" fill="none" stroke="#00d4ff" stroke-width="1" stroke-dasharray="3,3"/>
```

### 3D Skeuomorphic
```svg
<defs>
  <linearGradient id="shine" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0%" stop-color="#fff" stop-opacity=".3"/>
    <stop offset="100%" stop-color="#fff" stop-opacity="0"/>
  </linearGradient>
</defs>
<rect x="20" y="20" width="60" height="60" rx="12" fill="#E74C3C"/>
<rect x="20" y="20" width="60" height="30" rx="12" fill="url(#shine)"/>
```

## Common Palettes

```svg
<!-- Brand Blues -->
#3498DB #2980B9 #2C3E50 #1ABC9C
<!-- Warm Oranges -->
#E67E22 #F39C12 #D35400 #E74C3C
<!-- Natural Greens -->
#2ECC71 #27AE60 #16A085 #1ABC9C
<!-- Elegant Purples -->
#9B59B6 #8E44AD #6C3483 #5B2C6F
<!-- Neutrals -->
#2C3E50 #34495E #7F8C8D #BDC3C7 #ECF0F1
<!-- Gradient Combos -->
#667EEA→#764BA2  #F093FB→#F5576C  #4FACFE→#00F2FE
#43E97B→#38F9D7  #FA709A→#FEE140  #A18CD1→#FBC2EB
```

## Common Shape Reference

| Element | Tag | Key Attributes |
|---------|-----|----------------|
| Rectangle | `<rect>` | `x y width height rx ry` |
| Circle | `<circle>` | `cx cy r` |
| Ellipse | `<ellipse>` | `cx cy rx ry` |
| Line | `<line>` | `x1 y1 x2 y2` |
| Polygon | `<polygon>` | `points="x,y x,y ..."` |
| Path | `<path>` | `d="M...L...Q...C...Z"` |
| Text | `<text>` | `x y font-family font-size text-anchor` |
| Group | `<g>` | Wrap elements for unified transforms/styles |

## Path Commands

```
M x,y    — move to
L x,y    — line to
H x      — horizontal line
V y      — vertical line
Q cx,cy x,y         — quadratic bezier
C c1x,c1y c2x,c2y x,y  — cubic bezier
A rx,ry x-axis-rotation large-arc-flag sweep-flag x,y  — arc
Z        — close path
```

## Reference Files

| File | Content |
|------|---------|
| [references/templates.md](references/templates.md) | Logo/icon/illustration/UI component templates |
| [references/examples.md](references/examples.md) | Complete SVG examples in different styles |