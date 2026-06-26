# Markdown Extensions Reference

> Source: https://vitepress.dev/guide/markdown

## Header Anchors

Headers auto-get anchors. Custom anchor:

```md
# Custom anchors {#my-anchor}
```

## Links

### Internal Links

```md
[Home](/)
[foo heading](./#heading)
```

### External Links

Auto get `target="_blank" rel="noreferrer"`.

## Containers

### Info/Tip/Warning/Danger/Details

```md
::: info
This is an info box.
:::

::: tip
This is a tip.
:::

::: warning
This is a warning.
:::

::: danger
This is a dangerous warning.
:::

::: details
This is a details block.
:::
```

### Custom Title

```md
::: danger STOP
Danger zone, do not proceed
:::
```

### Details Open

```md
::: details Click me {open}
Content here
:::
```

## GitHub Alerts

```md
> [!NOTE]
> Note content here.

> [!TIP]
> Tip content here.

> [!IMPORTANT]
> Important content here.

> [!WARNING]
> Warning content here.

> [!CAUTION]
> Caution content here.
```

## Code Blocks

### Syntax Highlighting

````md
```js
const x = 1
```
````

Supported languages from Shiki.

### Line Highlighting

````md
```js{4}
export default {
  data() {
    return { msg: 'highlighted' }
  }
}
```
````

Ranges: `{5-8}`, single: `{4}`, mixed: `{4,7-10}`

### Focus

```md
```js
export default {
  data() {
    return { msg: 'Focused!' } // [!code focus]
  }
}
```
```

### Colored Diffs

```md
```js
return {
  msg: 'Removed' // [!code --]
  msg: 'Added'   // [!code ++]
}
```
```

### Errors/Warnings

```md
```js
msg: 'Error'   // [!code error]
msg: 'Warning' // [!code warning]
```
```

### Line Numbers

Config: `markdown: { lineNumbers: true }`

````md
```ts:line-numbers
const x = 1
```
````

Start from N: `ts:line-numbers=2`

## Import Code Snippets

```md
<<< @/snippets/file.js{2}

<!-- With VS Code region -->
<<< @/snippets/file.js#region-name

<!-- With language -->
<<< @/snippets/file.ts{c#}
```

## Code Groups

```md
::: code-group

```js [config.js]
const config = {}
```

```ts [config.ts]
const config: Config = {}
```

:::
```

## File Inclusion

```md
<!--@include: ./parts/basics.md-->
```

Line range: `{3,}`, `{,10}`, `{1,10}`

With header anchor: `<!--@include: ./file.md#section-name-->`

## Tables

```md
| Tables      |      Are      |  Cool |
|-------------|:-------------:|------:|
| col 3 is    | right-aligned | $1600 |
```

## Emoji

```md
:tada: :100:
```

## Table of Contents

```md
[[toc]]
```

## Math Equations

```bash
npm add -D markdown-it-mathjax3@^4
```

```typescript
markdown: { math: true }
```

```md
When $a \ne 0$, there are two solutions...

$$
x = {-b \pm \sqrt{b^2-4ac} \over 2a}
$$
```

## Image Lazy Loading

```typescript
markdown: { image: { lazyLoading: true } }
```

## raw Container

```md
::: raw
Wraps content in vp-raw class
:::
```

## Advanced Config

```typescript
markdown: {
  anchor: { permalink: markdownItAnchor.permalink.headerLink() },
  toc: { level: [1, 2] },
  config: (md) => { md.use(plugin) }
}
```
