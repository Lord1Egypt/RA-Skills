---
title: Expand Relations Efficiently
impact: HIGH
impactDescription: Eliminates N+1 queries, reduces API calls by 90%+
tags: query, relations, expand, joins, performance
---

## Expand Relations Efficiently

Use the `expand` parameter to fetch related records in a single request. This eliminates N+1 query problems and dramatically reduces API calls.

**Incorrect (N+1 queries):**

```javascript
// Fetching posts then authors separately - N+1 problem
async function getPostsWithAuthors() {
  const posts = await pb.collection('posts').getList(1, 20);

  // N additional requests for N posts!
  for (const post of posts.items) {
    post.authorData = await pb.collection('users').getOne(post.author);
  }

  return posts;
}
// 21 API calls for 20 posts!

// Even worse with multiple relations
async function getPostsWithAll() {
  const posts = await pb.collection('posts').getList(1, 20);

  for (const post of posts.items) {
    post.author = await pb.collection('users').getOne(post.author);
    post.category = await pb.collection('categories').getOne(post.category);
    post.tags = await Promise.all(
      post.tags.map(id => pb.collection('tags').getOne(id))
    );
  }
  // 60+ API calls!
}
```

**Correct (using expand):**

```javascript
// Single request with expanded relations
async function getPostsWithAuthors() {
  const posts = await pb.collection('posts').getList(1, 20, {
    expand: 'author'
  });

  // Access expanded data
  posts.items.forEach(post => {
    console.log('Author:', post.expand?.author?.name);
  });

  return posts;
}
// 1 API call!

// Multiple relations
async function getPostsWithAll() {
  const posts = await pb.collection('posts').getList(1, 20, {
    expand: 'author,category,tags'
  });

  posts.items.forEach(post => {
    console.log('Author:', post.expand?.author?.name);
    console.log('Category:', post.expand?.category?.name);
    console.log('Tags:', post.expand?.tags?.map(t => t.name));
  });
}
// Still just 1 API call!

// Nested expansion (up to 6 levels)
async function getPostsWithNestedData() {
  const posts = await pb.collection('posts').getList(1, 20, {
    expand: 'author.profile,category.parent,comments_via_post.author'
  });

  posts.items.forEach(post => {
    // Nested relations
    console.log('Author profile:', post.expand?.author?.expand?.profile);
    console.log('Parent category:', post.expand?.category?.expand?.parent);

    // Back-relations (comments that reference this post)
    console.log('Comments:', post.expand?.['comments_via_post']);
  });
}

// Back-relation expansion
// If comments collection has a 'post' relation field pointing to posts
async function getPostWithComments(postId) {
  const post = await pb.collection('posts').getOne(postId, {
    expand: 'comments_via_post,comments_via_post.author'
  });

  // Access comments that reference this post
  const comments = post.expand?.['comments_via_post'] || [];
  comments.forEach(comment => {
    console.log(`${comment.expand?.author?.name}: ${comment.text}`);
  });

  return post;
}
```

**Expand syntax:**

| Syntax | Description |
|--------|-------------|
| `expand: 'author'` | Single relation |
| `expand: 'author,tags'` | Multiple relations |
| `expand: 'author.profile'` | Nested relation (2 levels) |
| `expand: 'comments_via_post'` | Back-relation (records pointing to this) |

**Handling optional expand data:**

```javascript
// Always use optional chaining - expand may be undefined
const authorName = post.expand?.author?.name || 'Unknown';

// Type-safe access with TypeScript
interface Post {
  id: string;
  title: string;
  author: string;  // Relation ID
  expand?: {
    author?: User;
  };
}

const posts = await pb.collection('posts').getList<Post>(1, 20, {
  expand: 'author'
});
```

**Limitations:**
- Maximum 6 levels of nesting
- Respects API rules on expanded collections
- Large expansions may impact performance

Reference: [PocketBase Expand](https://pocketbase.io/docs/api-records/#expand)
