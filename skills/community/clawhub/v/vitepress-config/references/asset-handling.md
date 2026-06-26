# Asset Handling

> Source: https://vitepress.dev/guide/asset-handling

## Referencing Static Assets

Reference assets using relative URLs:

```md
![An image](./image.png)
```

Assets are:
- Copied to output with hashed filenames
- Images <4kb base64 inlined
- Linked files (PDF, etc.) must go in `public` directory

## The Public Directory

Place files that don't need processing (robots.txt, favicons, PWA icons) in `<srcDir>/public/`:

```
docs/
├─ public/
│  ├─ robots.txt
│  └─ favicon.ico
└─ index.md
```

Reference with root absolute path: `/robots.txt`

## Base URL

```typescript
export default {
  base: '/bar/'  // for https://foo.github.io/bar/
}
```

Static references in markdown don't need updates. For dynamic paths in theme components:

```vue
<script setup>
import { withBase, useData } from 'vitepress'

const { theme } = useData()
</script>

<template>
  <img :src="withBase(theme.logoPath)" />
</template>
```

## withBase Helper

```typescript
withBase(path: string): string
```

Appends configured `base` to any URL path.
