---
name: undocs-blog
description: Create and manage blog posts in undocs documentation sites
---

# Blog Functionality

Undocs includes built-in blog functionality for publishing articles and updates.

## Blog Structure

Create blog posts in the `blog/` directory:

```
docs/
└── blog/
    ├── 0.index.md          # Blog index page
    ├── 1.initial-release.md
    ├── 2.second-release.md
    └── 3.new-blog.md
```

## Blog Index Page

Create `blog/0.index.md` to serve as the blog homepage:

```markdown
---
title: Blog
description: Latest updates and articles
---

# Blog

Welcome to our blog!
```

## Blog Posts

Each blog post is a markdown file in the `blog/` directory:

```markdown
---
title: Initial Release
description: Announcing the first release of our project
date: 2024-01-15
---

# Initial Release

Content of the blog post...
```

## Blog Layout

Blog posts use the `blog` layout automatically:

```typescript
definePageMeta({
  layout: "blog",
});
```

## Blog Post Metadata

Blog posts support standard frontmatter fields:

- `title`: Post title
- `description`: Post description/excerpt
- `date`: Publication date
- Standard Nuxt Content frontmatter fields

## Blog Index Display

The blog index page automatically displays all blog posts using Nuxt UI's `UBlogPosts` component:

```vue
<UBlogPosts class="mb-12 md:grid-cols-2 lg:grid-cols-3">
  <UBlogPost
    v-for="post in posts"
    :key="post._path"
    :post="post"
  />
</UBlogPosts>
```

## Blog Navigation

Blog is automatically excluded from main documentation navigation but can be accessed via:

- Direct URL: `/blog`
- Header navigation (if configured)
- Breadcrumbs

## Key Points

- Blog posts are stored in `blog/` directory
- Use `0.index.md` for the blog homepage
- Blog layout is applied automatically
- Posts are displayed in a grid layout
- Supports standard Nuxt Content frontmatter
- Blog is separate from main documentation navigation

<!--
Source references:
- https://github.com/unjs/undocs/tree/main/app/pages/blog
- https://github.com/unjs/undocs/tree/main/app/layouts/blog.vue
-->
