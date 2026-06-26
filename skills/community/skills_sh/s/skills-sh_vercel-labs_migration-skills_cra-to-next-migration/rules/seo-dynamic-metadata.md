---
title: Generate Dynamic Metadata
impact: HIGH
impactDescription: SEO for dynamic pages
tags: seo, metadata, dynamic
---

## Generate Dynamic Metadata

Use `generateMetadata` function for pages with dynamic content (blog posts, products, etc.).

**CRA with react-helmet (before):**

```tsx
// src/pages/BlogPost.tsx
import { Helmet } from 'react-helmet'
import { useParams } from 'react-router-dom'
import { usePost } from '../hooks/usePost'

export default function BlogPost() {
  const { slug } = useParams()
  const { post, loading } = usePost(slug)

  if (loading) return <Loading />

  return (
    <>
      <Helmet>
        <title>{post.title} | Blog</title>
        <meta name="description" content={post.excerpt} />
      </Helmet>
      <article>{/* ... */}</article>
    </>
  )
}
```

**Next.js generateMetadata (after):**

```tsx
// app/blog/[slug]/page.tsx
import { Metadata } from 'next'

type Props = {
  params: { slug: string }
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await fetchPost(params.slug)

  return {
    title: `${post.title} | Blog`,
    description: post.excerpt,
    openGraph: {
      title: post.title,
      description: post.excerpt,
      images: [{ url: post.coverImage }],
    },
  }
}

export default async function BlogPost({ params }: Props) {
  const post = await fetchPost(params.slug)

  return (
    <article>
      <h1>{post.title}</h1>
      {/* ... */}
    </article>
  )
}
```

**With parent metadata:**

```tsx
export async function generateMetadata(
  { params }: Props,
  parent: ResolvingMetadata
): Promise<Metadata> {
  const post = await fetchPost(params.slug)
  const parentOpenGraph = (await parent).openGraph

  return {
    title: post.title,
    openGraph: {
      ...parentOpenGraph,
      images: [post.coverImage, ...parentOpenGraph?.images || []],
    },
  }
}
```
