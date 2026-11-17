# Webstudio Styling

All styling is applied per-element through style rows bound to a style source. There
is **no cascade** - Webstudio styles are element-scoped, so you must apply every
needed property to every target instance.

## Generate style values with Webstudio's own parser (MANDATORY)

Never hand-write a style value object. Webstudio ships a CSS parser inside the app
container. Use it to produce every value so Webstudio accepts them:

```js
// Call Webstudio's css-data parser to produce a valid style value
const { parseCssValue } = require("/app/node_modules/.pnpm/@webstudio-is+css-data@file+packages+css-data_zod@4.4.3/node_modules/@webstudio-is/css-data/lib/index.js")
parseCssValue('display', 'flex')
```

`parseStyle(property, cssValue)` is a helper that calls that parser via
`docker compose exec app node -e ...` and memoizes identical calls. Never write a
style value object by hand.

```js
// Resolve the native "Base" breakpoint id from the loaded build's `breakpoints`
const bps = JSON.parse(load('breakpoints'))
const base = bps.find(b => b.label === 'Base').id

function S(iid, property, cssValue) {
  styles.push(styleDecl(base, iid + ':ws:style', property, cssValue))
}
S(elId, 'display', 'flex')
S(elId, 'backgroundColor', '#090D12')
S(elId, 'gridTemplateColumns', '1fr 1fr')   // parser produces the valid tuple
```

## Applying styles to an element

### 1. Create and bind a local style source

Each styled element needs a local style source bound in `styleSourceSelections`, or
the style will NOT apply:

```js
styleSources.push({ type: 'local', id: iid + ':ws:style' })
styleSourceSelections.push({ instanceId: iid, values: [iid + ':ws:style'] })
```

When editing an existing element, check whether it already has a selection and add
the local source to its `values` if missing (don't create a duplicate selection row).

### 2. Set properties

Add one row per property, keyed to the element's style source. Use the parser for
values. When re-styling an existing property, remove the old row first to avoid
duplicates:

```js
function S(iid, bp, property, cssValue) {
  styles = styles.filter(s => !(s.styleSourceId===iid+':ws:style' && s.breakpointId===bp && s.property===property))
  styles.push(styleDecl(bp, iid+':ws:style', property, cssValue))
}
```

## Design tokens

Create a token style source and apply it, or apply the same declarations to each
element's local source. Tokens are `styleSources` with `type:'token'`:

```js
styleSources.push({ type: 'token', id: 'tok-surface', name: 'surface' })
styles.push({ breakpointId, styleSourceId: 'tok-surface', property: 'backgroundColor', value: parsedColor })
```

Define your own site-wide palette as tokens (create them via the Style Panel's
Style Sources, or import from the Design Tokens format - see `design.md`).

## Responsive styles via breakpoints

Breakpoints have `{id, label, maxWidth}`. The `Base` breakpoint applies everywhere;
mobile breakpoints carry `maxWidth`. Write the same property to different breakpoint
ids on the same style source to make an element responsive.

Breakpoint ids are generated per-instance and are NOT universal - resolve them from
the loaded `breakpoints` column at runtime by label, don't hardcode them:

```js
const bps = JSON.parse(load('breakpoints'))
const bpById = {}; for (const b of bps) bpById[b.id] = b
// find by label
const base = bps.find(b => b.label === 'Base').id
```

Always resolve the "Base" breakpoint from the loaded `breakpoints` column - never
hardcode an id (they differ per instance). Always check ALL breakpoints, not just
Base - desktop can look fine while mobile is broken.

## Page and element scoping

- **Page-level defaults** (background, body font, text color) go on the page root
  instance (`page.rootInstanceId`).
- **Component styles** go on the specific instances.
- Because there's no cascade, apply every needed property to every target instance.

## Common style patterns

```js
// page root
addStyle(local(root.id), 'backgroundColor', color('#090D12'))
addStyle(local(root.id), 'minHeight', unit(100,'vh'))
addStyle(local(root.id), 'maxWidth', unit(1080))
addStyle(local(root.id), 'marginLeft', kw('auto'))
addStyle(local(root.id), 'marginRight', kw('auto'))

// typography
addStyle(local(h1.id), 'fontFamily', {type:'fontFamily', value:['Fraunces','Georgia','serif']})
addStyle(local(h1.id), 'fontSize', unit(54))
addStyle(local(h1.id), 'fontWeight', {type:'unit', unit:'number', value:520})
addStyle(local(h1.id), 'lineHeight', {type:'unit', unit:'number', value:1.05})

// link reset
addStyle(local(a.id), 'textDecorationLine', kw('none'))
addStyle(local(a.id), 'textTransform', kw('uppercase'))
addStyle(local(a.id), 'letterSpacing', {type:'unit', unit:'em', value:0.08})
```

## Styling HtmlEmbed content

HtmlEmbeds render raw HTML and cannot use native style rows. Put a `<style>` block
inside the embed's `code`. Site-wide fonts/imports go in a `<style>` HtmlEmbed on
each page body as the first child. HtmlEmbeds inside page bodies publish; global
root children do NOT publish (a known gotcha - see `publishing.md`).
