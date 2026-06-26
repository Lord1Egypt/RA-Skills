---
title: Generate sitemap.xml
impact: MEDIUM
impactDescription: Help search engines discover pages
tags: seo, sitemap, indexing
---

## Generate sitemap.xml

Generate a sitemap dynamically to help search engines discover and index your pages.

**CRA Pattern (before):**

```xml
<!-- public/sitemap.xml - manually maintained -->
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2024-01-01</lastmod>
  </url>
</urlset>
```

**Next.js Dynamic Sitemap (after):**

```tsx
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    {
      url: 'https://example.com',
      lastModified: new Date(),
      changeFrequency: 'yearly',
      priority: 1,
    },
    {
      url: 'https://example.com/about',
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: 'https://example.com/blog',
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.5,
    },
  ]
}
```

**With dynamic content:**

```tsx
// app/sitemap.ts
import { MetadataRoute } from 'next'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  // Fetch all blog posts
  const posts = await fetchAllPosts()

  const blogUrls = posts.map((post) => ({
    url: `https://example.com/blog/${post.slug}`,
    lastModified: new Date(post.updatedAt),
    changeFrequency: 'monthly' as const,
    priority: 0.7,
  }))

  // Fetch all products
  const products = await fetchAllProducts()

  const productUrls = products.map((product) => ({
    url: `https://example.com/products/${product.slug}`,
    lastModified: new Date(product.updatedAt),
    priority: 0.8,
  }))

  return [
    { url: 'https://example.com', priority: 1 },
    ...blogUrls,
    ...productUrls,
  ]
}
```

**Multiple sitemaps:**

```tsx
// app/sitemap/[id]/route.ts
// For large sites, generate multiple sitemaps
```

**Static sitemap files:**

You can also use a static `public/sitemap.xml` file like in CRA, but dynamic generation is recommended for maintainability.

```
public/
└── sitemap.xml    # Static file (works like CRA)
```

See also: `seo-robots.md` for robots.txt configuration.
