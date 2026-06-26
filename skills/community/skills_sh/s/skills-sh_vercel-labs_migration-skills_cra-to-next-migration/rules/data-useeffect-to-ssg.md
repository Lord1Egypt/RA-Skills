---
title: Convert useEffect to getStaticProps (Pages Router)
impact: HIGH
impactDescription: Static generation for Pages Router
tags: data-fetching, ssg, getStaticProps, pages-router
---

## Convert useEffect to getStaticProps (Pages Router)

For static content that doesn't change often, use `getStaticProps` to fetch data at build time.

**CRA Pattern (before):**

```tsx
// src/pages/Blog.tsx
import { useState, useEffect } from 'react'

export default function Blog() {
  const [posts, setPosts] = useState([])

  useEffect(() => {
    fetch('/api/posts')
      .then(res => res.json())
      .then(setPosts)
  }, [])

  return <PostList posts={posts} />
}
```

**Next.js Pages Router (after):**

```tsx
// pages/blog.tsx
import { GetStaticProps } from 'next'

interface Props {
  posts: Post[]
}

export default function Blog({ posts }: Props) {
  return <PostList posts={posts} />
}

export const getStaticProps: GetStaticProps<Props> = async () => {
  const res = await fetch('https://api.example.com/posts')
  const posts = await res.json()

  return {
    props: {
      posts,
    },
    revalidate: 3600, // Regenerate every hour (ISR)
  }
}
```

**With dynamic routes:**

```tsx
// pages/blog/[slug].tsx
import { GetStaticProps, GetStaticPaths } from 'next'

export const getStaticPaths: GetStaticPaths = async () => {
  const res = await fetch('https://api.example.com/posts')
  const posts = await res.json()

  return {
    paths: posts.map(post => ({ params: { slug: post.slug } })),
    fallback: 'blocking', // or false, or true
  }
}

export const getStaticProps: GetStaticProps = async ({ params }) => {
  const res = await fetch(`https://api.example.com/posts/${params.slug}`)
  const post = await res.json()

  return {
    props: { post },
    revalidate: 60,
  }
}
```

**When to use:**
- Content doesn't change frequently
- Same content for all users
- SEO is important
- Performance is critical

For App Router, use `fetch()` with caching options in Server Components instead.
