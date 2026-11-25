# Export-safe Remotion: what client-side rendering can draw

Subclip exports with Remotion's client-side renderer (`renderMediaOnWeb`, Remotion 4.0.530). It does not screenshot a browser: it re-draws each element onto a canvas from its computed styles, and anything it does not implement is silently missing from the exported video. The live preview is a real browser, so an unsupported style **looks right in preview and breaks only in export**. `validate_runtime_layer_source` warns with "Export can't draw this: …"; treat every such warning as an error to fix.

Source: <https://www.remotion.dev/docs/client-side-rendering/limitations>. Any CSS property not listed as supported below is unsupported.

## Supported

- **Layout:** `margin`, `left`/`top` positioning, `display`, `width`, `height`, `flex`, `flex-direction`, `overflow`, `object-fit`. Positions are measured with `getBoundingClientRect()`, so any layout that produces the right box works.
- **Transforms:** `transform` (2D and 3D functions), `transform-origin`, `translate`, `scale`, `rotate`, `opacity`, `backface-visibility`.
- **Backgrounds:** `background-color`, `background-clip` (including text clip), `background-image: linear-gradient(…)` with `background-size` / `background-position` in px or %.
- **Borders:** `border`, `border-style`, `border-color`, `border-width`, `border-radius` (including elliptical radii), `outline`.
- **Text:** `color`, `-webkit-text-fill-color`, `font-family`, `font-size`, `font-style`, `font-weight`, `line-height`, `letter-spacing`, `word-spacing`, `text-transform`, `text-rendering`, `font-variant-caps`, `font-kerning`, `text-shadow`, `-webkit-text-stroke(-color|-width)`, `paint-order`, the `direction` attribute. `font-stretch` is rounded to a named stretch.
- **Text decoration (partial):** solid, dotted, dashed, double and wavy underline / overline / line-through with `text-decoration-color` and `text-decoration-thickness`. Wavy lines are approximated; exact line positions may differ.
- **Shadows:** plain `box-shadow` (offset, blur, colour).
- **Masks:** `mask-image: linear-gradient(…)`; one raster `url()` (same-origin, `data:` or `blob:`) only with `mask-size: 100% 100%`, `mask-position: 0% 0%`, `mask-repeat: no-repeat` (alpha channel).
- **Filters:** `blur()`, `brightness()`, `contrast()`, `drop-shadow()`, `grayscale()`, `hue-rotate()`, `invert()`, `opacity()`, `saturate()`, `sepia()`, combined.
- **Clip path:** `polygon()`, `path()`, `circle()`, `ellipse()`, `inset()`.
- **Elements:** `<Video>` and `<Audio>` from `@remotion/media`, `<Img>` (including SVG data URIs), inline `<svg>` (drawn as an image, so SVG-internal gradients/filters/`url(#…)` work), `<Gif>`, `<Lottie>`, `<Rive>`, `<ThreeCanvas>`, `<SkiaCanvas>`.
- **Fonts in SVG text:** fonts from `@remotion/fonts` / `@remotion/google-fonts` are embedded for `<text>`, `<tspan>`, `<textPath>` when the font is chosen inside the SVG markup (inline style, `font-family` attribute, or a `<style>` inside the SVG).

## Not supported: never author these in a Remotion layer

| Don't use | What happens in export | Use instead |
| --- | --- | --- |
| `z-index` (any element) | Ignored; elements draw in DOM order, stacking contexts ignored | Order the JSX back to front; for layer-level order use the Subclip item's `zIndex`/`layerOrder` |
| `backdrop-filter` | Not drawn (no blur/frost) | A semi-opaque background colour, or a pre-blurred image |
| `mix-blend-mode`, `background-blend-mode` | Not drawn | Pre-mixed colours or an image |
| `radial-gradient`, `conic-gradient`, `repeating-*-gradient` | Not drawn | `linear-gradient`, layered linear gradients, an SVG `<radialGradient>` inside an `<svg>`, or an image |
| `background-image: url(…)` | Not drawn | An `<Img>` element sized with `object-fit` |
| `box-shadow` with `inset` or a spread radius | Inset not drawn, spread ignored | A border, an inner element, or `outline` |
| `object-position` | Ignored; media always centred | A wrapper with `overflow: hidden` and an offset child |
| `perspective`, `perspective-origin` | Not supported | 2D transforms, or `<ThreeCanvas>` for real 3D |
| `transform-style` | Always behaves as `preserve-3d` | Avoid relying on flat 3D children |
| `writing-mode` | Not supported | Rotate the text with `transform` |
| `corner-shape` | Not supported | `border-radius` |
| CSS `filter` / `clip-path` / `mask` with `url(#…)` | Not drawn | Filter functions above; clip-path shapes above |
| Cross-origin, SVG, multi-layer or luminance masks | Not drawn | A single same-origin/data alpha mask, or a linear-gradient mask |
| `<iframe>` | Not drawn | Render the content directly |
| `<OffthreadVideo>`, `<Html5Video>`, `<Html5Audio>` | Unsupported | `<Video>` / `<Audio>` from `@remotion/media` |
| `<AnimatedEmoji>` | Unsupported | `<Lottie>` |
| `<AnimatedImage>` | Only works when rendering in Chrome | `<Gif>` or `<Img>` |

Also avoid fonts loaded only through CSS `@font-face`, a Google Fonts CSS import or the `FontFace` API for SVG text: they are not embedded. Text inside `<foreignObject>` is not treated as SVG text.

## Checklist before saving a Remotion layer

1. `validate_runtime_layer_source` returns no "Export can't draw this" warnings.
2. Stacking is expressed by JSX order, never `z-index`.
3. Every gradient is `linear-gradient` (or lives inside an `<svg>`).
4. Images are `<Img>`, never CSS background images.
5. After saving, check a frame through the export path (or a short export) when the design relies on filters, masks, clip paths or text effects.
