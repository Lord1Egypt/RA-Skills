# Routing Reference

> Source: https://vitepress.dev/guide/routing

## File-Based Routing

```
index.md                  -->  /index.html (accessible as /)
prologue.md               -->  /prologue.html
guide/index.md            -->  /guide/index.html (accessible as /guide/)
guide/getting-started.md  -->  /guide/getting-started.html
```

## Root and Source Directory

**Project Root:** Where `.vitepress/` directory lives.

**Source Directory:** Where Markdown files live (default: same as root, configured via `srcDir`).

## Linking

```md
<!-- Relative, recommended -->
[Getting Started](./getting-started)
[Guide](../guide/getting-started)

<!-- Avoid -->
[Getting Started](./getting-started.md)
```

## Clean URLs

Enable in config: `cleanUrls: true`

Requires server support to serve `/foo.html` when visiting `/foo`.

Server configurations:
- **Netlify/GitHub Pages:** Support by default
- **Vercel:** Enable in `vercel.json`

## Rewrites

```typescript
export default {
  rewrites: {
    'packages/:pkg/src/:slug*': ':pkg/:slug*'
  }
}
```

Or use function:

```typescript
rewrites(id) {
  return id.replace(/^packages\/([^/]+)\/src\//, '$1/')
}
```

## Dynamic Routes

### File Structure

```
packages/
├─ [pkg].md           # route template
└─ [pkg].paths.js     # paths loader
```

### paths.js

```javascript
export default {
  paths() {
    return [
      { params: { pkg: 'foo' }},
      { params: { pkg: 'bar' }}
    ]
  }
}
```

### TypeScript with defineRoutes

```typescript
import { defineRoutes } from 'vitepress'

export default defineRoutes({
  watch: ['../data/**/*.json'],
  async paths() {
    return [{ params: { pkg: 'foo' }}]
  },
  async transformPageData(pageData) {
    pageData.title = `${pageData.title} · Packages`
  }
})
```

### Multiple Params

```javascript
// [pkg]-[version].md + [pkg]-[version].paths.js
paths: () => [
  { params: { pkg: 'foo', version: '1.0.0' }},
  { params: { pkg: 'foo', version: '2.0.0' }}
]
```

### Dynamic Paths from Data

```javascript
import fs from 'fs'

export default {
  watch: ['./data/*.json'],
  paths(watchedFiles) {
    return watchedFiles.map(file => ({
      params: { slug: parseFile(file).slug }
    }))
  }
}
```

### Accessing Params

```md
# {{ $params.pkg }}
```

```vue
<script setup>
import { useData } from 'vitepress'
const { params } = useData()
</script>
```

### Raw Content

```javascript
return {
  params: { id: post.id },
  content: post.content  // raw Markdown/HTML
}
```

```md
<!-- @content -->
```
