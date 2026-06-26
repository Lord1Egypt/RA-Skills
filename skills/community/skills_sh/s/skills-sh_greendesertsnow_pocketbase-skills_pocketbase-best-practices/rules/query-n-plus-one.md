---
title: Prevent N+1 Query Problems
impact: HIGH
impactDescription: Reduces API calls from N+1 to 1-2, dramatically faster page loads
tags: query, performance, n-plus-one, optimization
---

## Prevent N+1 Query Problems

N+1 queries occur when you fetch a list of records, then make additional requests for each record's related data. This pattern causes severe performance issues at scale.

**Incorrect (N+1 patterns):**

```javascript
// Classic N+1: fetching related data in a loop
async function getPostsWithDetails() {
  const posts = await pb.collection('posts').getList(1, 20);  // 1 query

  for (const post of posts.items) {
    // N additional queries!
    post.author = await pb.collection('users').getOne(post.author);
    post.category = await pb.collection('categories').getOne(post.category);
  }
  // Total: 1 + 20 + 20 = 41 queries for 20 posts
}

// N+1 with Promise.all (faster but still N+1)
async function getPostsParallel() {
  const posts = await pb.collection('posts').getList(1, 20);

  await Promise.all(posts.items.map(async post => {
    post.author = await pb.collection('users').getOne(post.author);
  }));
  // Still 21 API calls, just parallel
}

// Hidden N+1 in rendering
function PostList({ posts }) {
  return posts.map(post => (
    <PostCard
      post={post}
      author={useAuthor(post.author)}  // Each triggers a fetch!
    />
  ));
}
```

**Correct (eliminate N+1):**

```javascript
// Solution 1: Use expand for relations
async function getPostsWithDetails() {
  const posts = await pb.collection('posts').getList(1, 20, {
    expand: 'author,category,tags'
  });

  // All data in one request
  posts.items.forEach(post => {
    console.log(post.expand?.author?.name);
    console.log(post.expand?.category?.name);
  });
  // Total: 1 query
}

// Solution 2: Batch fetch related records
async function getPostsWithAuthorsBatch() {
  const posts = await pb.collection('posts').getList(1, 20);

  // Collect unique author IDs
  const authorIds = [...new Set(posts.items.map(p => p.author))];

  // Single query for all authors (use pb.filter for safe binding)
  const filter = authorIds.map(id => pb.filter('id = {:id}', { id })).join(' || ');
  const authors = await pb.collection('users').getList(1, authorIds.length, {
    filter
  });

  // Create lookup map
  const authorMap = Object.fromEntries(
    authors.items.map(a => [a.id, a])
  );

  // Attach to posts
  posts.items.forEach(post => {
    post.authorData = authorMap[post.author];
  });
  // Total: 2 queries regardless of post count
}

// Solution 3: Use view collection for complex joins
// Create a view that joins posts with authors:
// SELECT p.*, u.name as author_name, u.avatar as author_avatar
// FROM posts p LEFT JOIN users u ON p.author = u.id

async function getPostsFromView() {
  const posts = await pb.collection('posts_with_authors').getList(1, 20);
  // Single query, data already joined
}

// Solution 4: Back-relations with expand
async function getUserWithPosts(userId) {
  const user = await pb.collection('users').getOne(userId, {
    expand: 'posts_via_author'  // All posts by this user
  });

  console.log('Posts by user:', user.expand?.posts_via_author);
  // 1 query gets user + all their posts
}
```

**Detecting N+1 in your code:**

```javascript
// Add request logging to detect N+1
let requestCount = 0;
pb.beforeSend = (url, options) => {
  requestCount++;
  console.log(`Request #${requestCount}: ${options.method} ${url}`);
  return { url, options };
};

// Monitor during development
async function loadPage() {
  requestCount = 0;
  await loadAllData();
  console.log(`Total requests: ${requestCount}`);
  // If this is >> number of records, you have N+1
}
```

**Prevention checklist:**
- [ ] Always use `expand` for displaying related data
- [ ] Never fetch related records in loops
- [ ] Batch fetch when expand isn't available
- [ ] Consider view collections for complex joins
- [ ] Monitor request counts during development

Reference: [PocketBase Expand](https://pocketbase.io/docs/api-records/#expand)
