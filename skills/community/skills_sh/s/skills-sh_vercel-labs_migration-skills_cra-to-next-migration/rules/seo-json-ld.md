---
title: Add Structured Data (JSON-LD)
impact: MEDIUM
impactDescription: Rich search results
tags: seo, json-ld, structured-data
---

## Add Structured Data (JSON-LD)

Add JSON-LD structured data for rich search results in Google.

**CRA with react-helmet (before):**

```tsx
<Helmet>
  <script type="application/ld+json">
    {JSON.stringify({
      "@context": "https://schema.org",
      "@type": "Article",
      "headline": "Article Title",
      "author": {
        "@type": "Person",
        "name": "Author Name"
      }
    })}
  </script>
</Helmet>
```

**Next.js Pattern (after):**

```tsx
// app/blog/[slug]/page.tsx
export default async function BlogPost({ params }) {
  const post = await fetchPost(params.slug)

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    description: post.excerpt,
    image: post.coverImage,
    datePublished: post.publishedAt,
    dateModified: post.updatedAt,
    author: {
      '@type': 'Person',
      name: post.author.name,
    },
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <article>
        <h1>{post.title}</h1>
        {/* ... */}
      </article>
    </>
  )
}
```

**Common schema types:**

```tsx
// Organization
const orgJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: 'Company Name',
  url: 'https://example.com',
  logo: 'https://example.com/logo.png',
}

// Product
const productJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Product',
  name: 'Product Name',
  image: 'https://example.com/product.jpg',
  offers: {
    '@type': 'Offer',
    price: '29.99',
    priceCurrency: 'USD',
  },
}

// BreadcrumbList
const breadcrumbJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: [
    { '@type': 'ListItem', position: 1, name: 'Home', item: 'https://example.com' },
    { '@type': 'ListItem', position: 2, name: 'Blog', item: 'https://example.com/blog' },
  ],
}
```
