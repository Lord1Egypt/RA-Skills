---
name: svgjs
description: SVG.js — lightweight SVG manipulation & animation library. Zero dependencies, chainable API, full SVG spec coverage. Create/position/animate shapes (rect/circle/ellipse/line/polyline/polygon/path), text, images, groups, gradients, masks, patterns, text paths. 
---

# SVG.js

Zero-dependency SVG manipulation and animation. `npm install @svgdotjs/svg.js` or `import { SVG } from '@svgdotjs/svg.js'`

## Use Cases

Use when drawing SVG, animating vector graphics, building data visualizations, creating SVG-based UI components, or manipulating SVG DOM.

## Core API

**SVG()** — entry point for everything: create doc, get from DOM, create from fragment:
```js
const draw = SVG().addTo('body').size(300, 300)  // SVG doc MUST have explicit size()
const rect = SVG('#myRect')                       // get from DOM
const el = SVG('<circle>')                        // create from fragment
```

**Chainable** — every setter returns `this`:
```js
draw.rect(100, 100).fill('#f06').stroke({ width: 2, color: '#000' }).move(50, 50)

// .animate() starts animation chain, returns SVG.Runner (NOT the element)
rect.animate(1000).move(200, 200).fill('#0f0')
rect.animate({ duration: 2000, delay: 500, times: 3 }).rotate(45)
// Sequence: rect.animate().fill('#f03').animate().dmove(50, 50)
```

**Quick example**:
```js
import { SVG } from '@svgdotjs/svg.js'
const draw = SVG().addTo('body').size(400, 300)
draw.rect(100, 100).fill('#f06').move(50, 50)
draw.circle(50).fill('#0f0').center(200, 150)
draw.text('Hello').font({ family: 'Arial', size: 24 }).move(50, 200)
```

## Progressive References

- Shapes: rect/circle/ellipse/line/polyline/polygon/path → `references/shapes.md`
- Text, images, masks, gradients, patterns → `references/text-image.md`
- Positioning, sizing, attr, transforms, tree manipulation → `references/manipulating.md`
- Animation, Runner, Timeline, easing, controllers → `references/animating.md`
- Containers: groups, nested SVG, defs, symbols, links → `references/containers.md`
- Events, custom events, namespaces → `references/events.md`
- Import/export, extend, subclass → `references/utilities.md`
- Color, Matrix, Point, Box, List, PointArray, PathArray → `references/classes.md`

## Gotchas

1. **SVG doc must have explicit `size()`** — defaults to 0×0 without it
2. **`.animate()` returns Runner, not element** — chain `.animate()` again for sequencing
3. **Positioning works on ALL elements** — `rect.cx(50)` works though cx isn't native to rect
4. **Groups have no geometry** — no x/y/w/h; use `nested()` for positioned containers
5. **Text needs explicit newlines** — SVG has no flowing text; use `\n` or `tspan().newLine()`
6. **Path animation needs same command structure** — both paths must have identical M/C/S commands
7. **css() ≠ attr()** — `css()` sets inline styles, `attr()` sets SVG attributes
8. **First `SVG()` call creates invisible parser `<svg>`** — normal, documented in FAQ