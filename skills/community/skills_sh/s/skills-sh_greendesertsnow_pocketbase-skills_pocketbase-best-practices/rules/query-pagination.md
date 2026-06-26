---
title: Use Efficient Pagination Strategies
impact: HIGH
impactDescription: 10-100x faster list queries on large collections
tags: query, pagination, performance, lists
---

## Use Efficient Pagination Strategies

Pagination impacts performance significantly. Use `skipTotal` for large datasets, cursor-based pagination for infinite scroll, and appropriate page sizes.

**Incorrect (inefficient pagination):**

```javascript
// Fetching all records - memory and performance disaster
const allPosts = await pb.collection('posts').getFullList();
// Downloads entire table, crashes on large datasets

// Default pagination without skipTotal
const posts = await pb.collection('posts').getList(100, 20);
// COUNT(*) runs on every request - slow on large tables

// Using offset for infinite scroll
async function loadMore(page) {
  // As page increases, offset queries get slower
  return pb.collection('posts').getList(page, 20);
  // Page 1000: skips 19,980 rows before returning 20
}
```

**Correct (optimized pagination):**

```javascript
// Use skipTotal for better performance on large collections
const posts = await pb.collection('posts').getList(1, 20, {
  skipTotal: true,  // Skip COUNT(*) query
  sort: '-created'
});
// Returns items without totalItems/totalPages (faster)

// Cursor-based pagination for infinite scroll
async function loadMorePosts(lastCreated = null) {
  const filter = lastCreated
    ? pb.filter('created < {:cursor}', { cursor: lastCreated })
    : '';

  const result = await pb.collection('posts').getList(1, 20, {
    filter,
    sort: '-created',
    skipTotal: true
  });

  // Next cursor is the last item's created date
  const nextCursor = result.items.length > 0
    ? result.items[result.items.length - 1].created
    : null;

  return { items: result.items, nextCursor };
}

// Usage for infinite scroll
let cursor = null;
async function loadNextPage() {
  const { items, nextCursor } = await loadMorePosts(cursor);
  cursor = nextCursor;
  appendToList(items);
}

// Batched fetching when you need all records
async function getAllPostsEfficiently() {
  const allPosts = [];
  let page = 1;
  const perPage = 1000;  // Larger batches = fewer requests (max 1000 per API limit)

  while (true) {
    const result = await pb.collection('posts').getList(page, perPage, {
      skipTotal: true
    });

    allPosts.push(...result.items);

    if (result.items.length < perPage) {
      break;  // No more records
    }
    page++;
  }

  return allPosts;
}

// Or use getFullList with batch option
const allPosts = await pb.collection('posts').getFullList({
  batch: 1000,  // Records per request (default 1000 since JS SDK v0.26.6; max 1000)
  sort: '-created'
});
```

**Choose the right approach:**

| Use Case | Approach |
|----------|----------|
| Standard list with page numbers | `getList()` with page/perPage |
| Large dataset, no total needed | `getList()` with `skipTotal: true` |
| Infinite scroll | Cursor-based with `skipTotal: true` |
| Export all data | `getFullList()` with batch size |
| First N records only | `getList(1, N, { skipTotal: true })` |

**Performance tips:**
- Use `skipTotal: true` unless you need page count
- Keep `perPage` reasonable (20-100 for UI, up to 1000 for batch exports)
- Index fields used in sort and filter
- Cursor pagination scales better than offset

Reference: [PocketBase Records API](https://pocketbase.io/docs/api-records/)
