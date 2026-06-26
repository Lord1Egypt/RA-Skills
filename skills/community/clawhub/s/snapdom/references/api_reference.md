# SnapDOM API Reference

## Installation and Import

```js
// npm
import { snapdom, preCache } from '@zumer/snapdom';

// CDN ESM
import { snapdom } from 'https://unpkg.com/@zumer/snapdom/dist/snapdom.mjs';
```

## Core API

### `snapdom(el, options?)` → Capture result object

```js
const result = await snapdom(document.querySelector('#card'));
// result.url       — data URL
// result.toRaw()   → string (raw SVG string)
// result.toSvg()   → Promise<HTMLImageElement>
// result.toCanvas()→ Promise<HTMLCanvasElement>
// result.toBlob()  → Promise<Blob>
// result.toPng()    → Promise<HTMLImageElement>
// result.toJpg()   → Promise<HTMLImageElement>
// result.toWebp()  → Promise<HTMLImageElement>
// result.download() → Promise<void>
```

### Shortcut Methods

```js
await snapdom.toPng(el, options?);
await snapdom.toJpg(el, { quality: 0.92 });
await snapdom.toWebp(el, { quality: 0.85 });
await snapdom.toBlob(el, { type: 'jpeg' });
await snapdom.toSvg(el);
await snapdom.download(el, { format: 'jpg', filename: 'output.jpg' });
```

## Full Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `debug` | boolean | `false` | Output silent errors to console.warn |
| `fast` | boolean | `true` | Skip idle delays for faster capture |
| `scale` | number | `1` | Scale multiplier |
| `dpr` | number | `devicePixelRatio` | Device pixel ratio |
| `width` | number | - | Force width |
| `height` | number | - | Force height |
| `backgroundColor` | string | `"#fff"` | Background color |
| `quality` | number | `1` | JPG/WebP quality 0~1 |
| `useProxy` | string | `''` | CORS proxy URL |
| `embedFonts` | boolean | `false` | Embed non-icon fonts |
| `localFonts` | array | `[]` | Local font definitions |
| `iconFonts` | string/RegExp/array | `[]` | Icon font matchers |
| `excludeFonts` | object | `{}` | Exclude fonts |
| `exclude` | string[] | - | CSS selectors to exclude |
| `excludeMode` | `"hide"`/`"remove"` | `"hide"` | Exclude mode |
| `filter` | function | - | Filter predicate |
| `filterMode` | `"hide"`/`"remove"` | `"hide"` | Filter mode |
| `cache` | string | `"soft"` | Cache mode |
| `placeholders` | boolean | `true` | Show placeholders |
| `fallbackURL` | string/function | - | Fallback for failed image loads |
| `outerTransforms` | boolean | `true` | Preserve outer transforms |
| `outerShadows` | boolean | `false` | Preserve shadow overflow |
| `safariWarmupAttempts` | number | `3` | Safari warmup attempts |

### Dimension Priority

1. `scale` takes precedence over `width`/`height`
2. Provide only `width` → height scales proportionally
3. Provide both `width` + `height` → force dimensions (may distort)

### Cache Modes

| Mode | Description |
|------|-------------|
| `"disabled"` | No caching |
| `"soft"` | Clear session cache (default) |
| `"auto"` | Minimal cleanup |
| `"full"` | Preserve all caches |

## Pre-caching

```js
import { preCache } from '@zumer/snapdom';

await preCache({
  root: document.body,
  embedFonts: true,
  useProxy: 'https://proxy.corsfix.com/?'
});
```

## Capture Flow

```
DOM Element → Clone → Styles & Pseudo → Images & Backgrounds
→ Fonts → SVG foreignObject → data:image/svg+xml
→ toPng / toSvg / toBlob / download
```

Plugin hook order: `beforeSnap` → `beforeClone` → `afterClone` → `beforeRender` → `afterRender` → `beforeExport` → `afterExport` → `afterSnap`.

## Limitations

- External images must be CORS-accessible (use `useProxy` to handle)
- Safari WebP falls back to PNG
- Custom scrollbar styles only take effect when the element is not scrolled