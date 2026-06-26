---
name: snapdom
description: DOM capture engine that can export any DOM subtree as SVG, PNG, JPG, WebP, Canvas, or Blob, supporting inline styles, fonts, background images, pseudo-elements, and Shadow DOM.
---

# snapdom — DOM Capture Engine

## Use Cases

Use this skill when users request to take a screenshot of a web page element, DOM node, or HTML fragment, export it as an image, generate a web page snapshot, or convert any DOM element to an image/Canvas.

## Installation

NPM:
```bash
npm i @zumer/snapdom
```

CDN (script tag):
```html
<script src="https://unpkg.com/@zumer/snapdom/dist/snapdom.js"></script>
```

## Quick Start

### Shortcuts (One-off export)
```js
import { snapdom } from '@zumer/snapdom';

// Export a DOM element as PNG
const png = await snapdom.toPng(document.querySelector('#card'));
document.body.appendChild(png);

// Other formats
const blob = await snapdom.toBlob(document.querySelector('#card'));
const svgImg = await snapdom.toSvg(document.querySelector('#card'));
```

### Reusable Capture (Clone once, export multiple times)
```js
const result = await snapdom(document.querySelector('#card'));
const png = await result.toPng();
const jpg = await result.toJpg({ quality: 0.92 });
await result.download({ format: 'jpg', filename: 'card.jpg' });
```

## Common Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `scale` | number | 1 | Output scale multiplier |
| `width` / `height` | number | - | Force output dimensions |
| `quality` | number | 1 | JPG/WebP quality 0~1 |
| `backgroundColor` | string | `"#fff"` | Background color for JPG/WebP |
| `embedFonts` | boolean | false | Embed non-icon fonts |
| `useProxy` | string | `''` | CORS proxy URL |
| `exclude` | string[] | - | CSS selectors to exclude |
| `filter` | function | - | Filter function `(el) => boolean` |
| `debug` | boolean | false | Output silent errors to console.warn |

### Examples
```js
// High-definition screenshot (2x)
await snapdom.toPng(el, { scale: 2 });

// CORS cross-origin images
await snapdom.toPng(el, { useProxy: 'https://proxy.corsfix.com/?' });

// Exclude elements
await snapdom.toPng(el, { exclude: ['.cookie-banner', '.tooltip'] });

// Filter out display:none elements
await snapdom.toPng(document.body, {
  filter: el => window.getComputedStyle(el).display !== 'none'
});
```

## xbrowser Integration

When capturing in a **xbrowser** environment, SnapDOM must be run through the browser's execution context. Recommended pattern:

```js
// After an xbrowser snapshot, execute in the page via evaluate
await browser.evaluate(async (selector) => {
  const { snapdom } = window._snapdom || await import('https://unpkg.com/@zumer/snapdom/dist/snapdom.mjs');
  const el = document.querySelector(selector);
  if (!el) throw new Error(`Element not found: ${selector}`);
  const result = await snapdom(el, { scale: 2, embedFonts: true });
  const dataUrl = await result.toPng();
  return dataUrl;
}, selector);
```

See [references/api_reference.md](references/api_reference.md) for detailed API documentation and full options list.

## Plugins

Install official plugins:
```bash
npm install @zumer/snapdom-plugins
```

Register and use:
```js
import { snapdom } from '@zumer/snapdom';
import { filter, timestampOverlay } from '@zumer/snapdom-plugins';

snapdom.plugins(
  [filter, { preset: 'grayscale' }],
  [timestampOverlay, { position: 'bottom-right' }]
);

const out = await snapdom(element);
const png = await out.toPng();
```

Plugin lifecycle hooks: `beforeSnap` → `beforeClone` → `afterClone` → `beforeRender` → `afterRender` → `beforeExport` → `afterExport`.

Example Reference [assets/demo.html](assets/demo.html)。