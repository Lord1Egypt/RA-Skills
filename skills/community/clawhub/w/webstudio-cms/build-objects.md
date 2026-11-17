# Webstudio Build Objects

The entire site is a tree of `instances` (the element tree) plus the styles, props,
pages, and breakpoints that reference them. This file documents the exact object
shapes Webstudio stores and how to construct them programmatically.

## The element tree (`instances`)

Each node is an `instance` (element) or a child reference:

```js
// element
{ type: 'instance', id: '<22-char-id>', component, tag, children: [...] }

// child references
{ type: 'text', value: 'literal text' }   // text content
{ type: 'id',   value: '<instanceId>' }    // nested element
```

`tag` is the HTML tag (`div`, `h1`, `p`, `a`, `section`, etc.). `component` is the
Webstudio component name. A leaf text node is `{type:'text', value}`.

## The build helper patterns

The supported way to construct a build is to assemble the native objects yourself
(full source patterns are in `database.md` for load/commit and `styling.md` for
style values). The shapes Webstudio expects are:

```js
// element
{ type: 'instance', id: '<22-char-id>', component, tag, children: [...] }
// child refs
{ type: 'text', value: 'literal text' }
{ type: 'id', value: '<instanceId>' }
// style source binding (see styling.md)
styleSources.push({ type: 'local', id: iid + ':ws:style' })
styleSourceSelections.push({ instanceId: iid, values: [iid + ':ws:style'] })
// style row
{ breakpointId, styleSourceId, property, value }
// prop
{ id: iid + ':' + name, instanceId, name, type, value }
```

IDs must be Webstudio-style (alphanumeric, no `:` or `-_`). Use a random alphanumeric
string of ~22 chars; don't reuse one id across elements.

Helpers:
- `uid(n)` - random Webstudio-style id (alphanumeric, no `:` or `-_`)
- `inst(component, tag, children)` - an element node
- `textChild(value)` / `idChild(value)` - child references
- `color(hex)` - a valid color style value
- `unit(value, unit)` - a length/number style value (`unit(54)`, `unit(100,'vh')`)
- `kw(value)` - a keyword style value
- `prop(instanceId, name, type, value)` - an element prop
- `Build` class - assembles instances/styleSources/styles/props/pages and tracks by id

## Pages

Pages live in `pages`:

```js
pages.pages.push({
  id, name, title: JSON.stringify(title), rootInstanceId, path, meta: {},
})
pages.folders[0].children.push(id)
```

- `homePageId` - the root folder id
- `rootFolderId` = `'root'`, and `folders = [{id:'root', name:'Root', slug:'', children:[...]}]`
- Each page's `rootInstanceId` points at the top `body`/`Body` instance of that page.

The page root is where page-level defaults (background, body font, text color) go.

## Props

Element props carry attributes/behaviour (href, src, aria-label, etc.):

```js
{ id: '<instanceId>:<name>', instanceId, name, type, value }
```

Common prop `type` values include `string`, `number`, `boolean`. Use `prop()` from
the lib to build them. Props are NOT styles - don't put visual styling here.

## styleSources / styleSourceSelections

Each styled element needs a LOCAL style source bound to it, or styles won't apply:

```js
styleSources.push({ type: 'local', id: iid + ':ws:style' })
styleSourceSelections.push({ instanceId: iid, values: [iid + ':ws:style'] })
```

Token style sources (`type:'token'`) are named, reusable style groups (design
tokens). See `styling.md` for token usage.

## styles

One row per (breakpoint, style source, property):

```js
{ breakpointId, styleSourceId, property, value }
```

`value` must come from Webstudio's css-data parser - never hand-write it (see
`styling.md`).

## breakpoints

```js
{ id, label, maxWidth? }
```

`Base` applies everywhere (this instance's Base breakpoint id). Mobile breakpoints carry
`maxWidth`. Write the same property to different breakpoint ids on the same style
source to make an element responsive.

## dataSources / resources (advanced)

These are for variables and server resources (e.g. forms, external data fetches).
For standard pages they stay `[]` and can be left untouched. `marketplaceProduct`
stays `{}`, `projectSettings` stays at its default. Don't overwrite these columns
unless you're actually using them - and if you load them, write them back unchanged.

## Constructing a brand-new page vs editing

- **Edit existing:** load the build columns, locate elements by walking the tree
  (see `database.md`), mutate, write back ALL loaded columns.
- **New page:** build the instance tree with `Build`, add the page to `pages.pages`,
  bind style sources, write back.

Either way, follow the load/commit pattern in `database.md` and never write a
partial column set.
