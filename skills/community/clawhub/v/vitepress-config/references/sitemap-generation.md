# Sitemap Generation

> Source: https://vitepress.dev/guide/sitemap-generation

VitePress has built-in sitemap generation.

## Enable

```typescript
export default {
  sitemap: {
    hostname: 'https://example.com'
  }
}
```

Enable `lastUpdated` for `<lastmod>` tags.

## Options

Powered by [`sitemap`](https://www.npmjs.com/package/sitemap) package:

```typescript
export default {
  sitemap: {
    hostname: 'https://example.com',
    lastmodDateOnly: false,
    // ... other sitemap package options
  }
}
```

## With base

```typescript
export default {
  base: '/my-site/',
  sitemap: {
    hostname: 'https://example.com/my-site/'
  }
}
```

## transformItems Hook

```typescript
export default {
  sitemap: {
    hostname: 'https://example.com',
    transformItems: (items) => {
      items.push({
        url: '/extra-page',
        changefreq: 'monthly',
        priority: 0.8
      })
      return items
    }
  }
}
```
