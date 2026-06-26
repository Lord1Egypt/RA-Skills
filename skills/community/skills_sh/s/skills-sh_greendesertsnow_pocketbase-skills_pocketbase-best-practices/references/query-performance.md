# Query Performance

**Impact: HIGH**

Pagination strategies, relation expansion, field selection, batch operations, and N+1 query prevention.

---

## 1. Use Back-Relations for Inverse Lookups

**Impact: HIGH (Fetch related records without separate queries)**

Back-relations allow you to expand records that reference the current record, enabling inverse lookups in a single request. Use the `collectionName_via_fieldName` syntax.

**Incorrect (manual inverse lookup):**

```javascript
// Fetching a user, then their posts separately
async function getUserWithPosts(userId) {
  const user = await pb.collection('users').getOne(userId);

  // Extra request for posts
  const posts = await pb.collection('posts').getList(1, 100, {
    filter: pb.filter('author = {:userId}', { userId })
  });

  return { ...user, posts: posts.items };
}
// 2 API calls

// Fetching a post, then its comments
async function getPostWithComments(postId) {
  const post = await pb.collection('posts').getOne(postId);
  const comments = await pb.collection('comments').getFullList({
    filter: pb.filter('post = {:postId}', { postId }),
    expand: 'author'
  });

  return { ...post, comments };
}
// 2 API calls
```

**Correct (using back-relation expand):**

```javascript
// Expand posts that reference this user
// posts collection has: author (relation to users)
async function getUserWithPosts(userId) {
  const user = await pb.collection('users').getOne(userId, {
    expand: 'posts_via_author'  // collectionName_via_fieldName
  });

  console.log('User:', user.name);
  console.log('Posts:', user.expand?.posts_via_author);
  return user;
}
// 1 API call!

// Expand comments that reference this post
// comments collection has: post (relation to posts)
async function getPostWithComments(postId) {
  const post = await pb.collection('posts').getOne(postId, {
    expand: 'comments_via_post,comments_via_post.author'
  });

  const comments = post.expand?.comments_via_post || [];
  comments.forEach(comment => {
    console.log(`${comment.expand?.author?.name}: ${comment.content}`);
  });

  return post;
}
// 1 API call with nested expansion!

// Multiple back-relations
async function getUserWithAllContent(userId) {
  const user = await pb.collection('users').getOne(userId, {
    expand: 'posts_via_author,comments_via_author,likes_via_user'
  });

  return {
    user,
    posts: user.expand?.posts_via_author || [],
    comments: user.expand?.comments_via_author || [],
    likes: user.expand?.likes_via_user || []
  };
}
```

**Back-relation syntax:**

```
{referencing_collection}_via_{relation_field}

Examples:
- posts_via_author      -> posts where author = current record
- comments_via_post     -> comments where post = current record
- order_items_via_order -> order_items where order = current record
- team_members_via_team -> team_members where team = current record
```

**Nested back-relations:**

```javascript
// Get user with posts and each post's comments
const user = await pb.collection('users').getOne(userId, {
  expand: 'posts_via_author.comments_via_post'
});

// Access nested data
const posts = user.expand?.posts_via_author || [];
posts.forEach(post => {
  console.log('Post:', post.title);
  const comments = post.expand?.comments_via_post || [];
  comments.forEach(c => console.log('  Comment:', c.content));
});
```

**Important considerations:**

```javascript
// Back-relations always return arrays, even if the relation field
// is marked as single (maxSelect: 1)

// Limited to 1000 records per back-relation
// For more, use separate paginated query
const user = await pb.collection('users').getOne(userId, {
  expand: 'posts_via_author'
});
// If user has 1500 posts, only first 1000 are included

// For large datasets, use paginated approach
async function getUserPostsPaginated(userId, page = 1) {
  return pb.collection('posts').getList(page, 50, {
    filter: pb.filter('author = {:userId}', { userId }),
    sort: '-created'
  });
}
```

**Use in list queries:**

```javascript
// Get all users with their post counts
// (Use view collection for actual counts)
const users = await pb.collection('users').getList(1, 20, {
  expand: 'posts_via_author'
});

users.items.forEach(user => {
  const postCount = user.expand?.posts_via_author?.length || 0;
  console.log(`${user.name}: ${postCount} posts`);
});
```

**When to use back-relations vs separate queries:**

| Scenario | Approach |
|----------|----------|
| < 1000 related records | Back-relation expand |
| Need pagination | Separate query with filter |
| Need sorting/filtering | Separate query |
| Just need count | View collection |
| Display in list | Back-relation (if small) |

Reference: [PocketBase Back-Relations](https://pocketbase.io/docs/working-with-relations/#back-relation-expand)

## 2. Use Batch Operations for Multiple Writes

**Impact: HIGH (Atomic transactions, 10x fewer API calls, consistent state)**

Batch operations combine multiple create/update/delete operations into a single atomic transaction. This ensures consistency and dramatically reduces API calls.

**Incorrect (individual requests):**

```javascript
// Creating multiple records individually
async function createOrderWithItems(order, items) {
  // If any fails, partial data remains!
  const createdOrder = await pb.collection('orders').create(order);

  for (const item of items) {
    await pb.collection('order_items').create({
      ...item,
      order: createdOrder.id
    });
  }
  // 1 + N API calls, not atomic
}

// Updating multiple records
async function updatePrices(products) {
  for (const product of products) {
    await pb.collection('products').update(product.id, {
      price: product.newPrice
    });
  }
  // N API calls, some might fail leaving inconsistent state
}

// Mixed operations
async function transferFunds(fromId, toId, amount) {
  // NOT ATOMIC - can leave invalid state!
  await pb.collection('accounts').update(fromId, { 'balance-': amount });
  // If this fails, money disappears!
  await pb.collection('accounts').update(toId, { 'balance+': amount });
}
```

**Correct (using batch operations):**

```javascript
// Atomic batch create
async function createOrderWithItems(order, items) {
  const batch = pb.createBatch();

  // Pre-generate order ID so items can reference it in the same batch
  // PocketBase accepts custom IDs (15-char alphanumeric)
  const orderId = crypto.randomUUID().replaceAll('-', '').slice(0, 15);

  // Queue order creation with known ID
  batch.collection('orders').create({ ...order, id: orderId });

  // Queue all items referencing the pre-generated order ID
  items.forEach(item => {
    batch.collection('order_items').create({
      ...item,
      order: orderId
    });
  });

  // Execute atomically
  const results = await batch.send();
  // All succeed or all fail together

  return {
    order: results[0],
    items: results.slice(1)
  };
}

// Batch updates
async function updatePrices(products) {
  const batch = pb.createBatch();

  products.forEach(product => {
    batch.collection('products').update(product.id, {
      price: product.newPrice
    });
  });

  const results = await batch.send();
  // 1 API call, atomic
  return results;
}

// Batch upsert (create or update)
async function syncProducts(products) {
  const batch = pb.createBatch();

  products.forEach(product => {
    batch.collection('products').upsert({
      id: product.sku,  // Use SKU as ID for upsert matching
      name: product.name,
      price: product.price,
      stock: product.stock
    });
  });

  return batch.send();
}

// Mixed operations in transaction
// NOTE: Batch operations respect API rules per-operation, but ensure your
// business logic validates inputs (e.g., sufficient balance) server-side
// via hooks or API rules to prevent unauthorized transfers.
async function transferFunds(fromId, toId, amount) {
  const batch = pb.createBatch();

  batch.collection('accounts').update(fromId, { 'balance-': amount });
  batch.collection('accounts').update(toId, { 'balance+': amount });

  // Create audit record
  batch.collection('transfers').create({
    from: fromId,
    to: toId,
    amount,
    timestamp: new Date()
  });

  // All three operations atomic
  const [fromAccount, toAccount, transfer] = await batch.send();
  return { fromAccount, toAccount, transfer };
}

// Batch delete
async function deletePostWithComments(postId) {
  // First get comment IDs
  const comments = await pb.collection('comments').getFullList({
    filter: pb.filter('post = {:postId}', { postId }),
    fields: 'id'
  });

  const batch = pb.createBatch();

  // Queue all deletions
  comments.forEach(comment => {
    batch.collection('comments').delete(comment.id);
  });
  batch.collection('posts').delete(postId);

  await batch.send();
  // Post and all comments deleted atomically
}
```

**Batch operation limits:**
- **Must be enabled first** in Dashboard > Settings > Application (disabled by default; returns 403 otherwise)
- Operations execute in a single database transaction
- All succeed or all rollback
- Respects API rules for each operation
- Configurable limits: `maxRequests`, `timeout`, and `maxBodySize` (set in Dashboard)
- **Avoid large file uploads** in batches over slow networks -- they block the entire transaction
- Avoid custom hooks that call slow external APIs within batch operations

**When to use batch:**

| Scenario | Use Batch? |
|----------|-----------|
| Creating parent + children | Yes |
| Bulk import/update | Yes |
| Financial transactions | Yes |
| Single record operations | No |
| Independent operations | Optional |

Reference: [PocketBase Batch API](https://pocketbase.io/docs/api-records/#batch-operations)

## 3. Expand Relations Efficiently

**Impact: HIGH (Eliminates N+1 queries, reduces API calls by 90%+)**

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

## 4. Select Only Required Fields

**Impact: MEDIUM (Reduces payload size, improves response time)**

Use the `fields` parameter to request only the data you need. This reduces bandwidth and can improve query performance, especially with large text or file fields.

**Incorrect (fetching everything):**

```javascript
// Fetching all fields when only a few are needed
const posts = await pb.collection('posts').getList(1, 20);
// Returns: id, title, content (10KB), thumbnail, author, tags, created, updated...

// Only displaying titles in a list
posts.items.forEach(post => {
  renderListItem(post.title);  // Only using title!
});
// Wasted bandwidth on content, thumbnail URLs, etc.

// Fetching user data with large profile fields
const users = await pb.collection('users').getFullList();
// Includes: avatar (file), bio (text), settings (json)...
// When you only need names for a dropdown
```

**Correct (selecting specific fields):**

```javascript
// Select only needed fields
const posts = await pb.collection('posts').getList(1, 20, {
  fields: 'id,title,created'
});
// Returns only: { id, title, created }

// For a dropdown/autocomplete
const users = await pb.collection('users').getFullList({
  fields: 'id,name,avatar'
});

// Include expanded relation fields
const posts = await pb.collection('posts').getList(1, 20, {
  expand: 'author',
  fields: 'id,title,expand.author.name,expand.author.avatar'
});
// Returns: { id, title, expand: { author: { name, avatar } } }

// Wildcard for all direct fields, specific for expand
const posts = await pb.collection('posts').getList(1, 20, {
  expand: 'author,category',
  fields: '*,expand.author.name,expand.category.name'
});
// All post fields + only name from expanded relations
```

**Using excerpt modifier:**

```javascript
// Get truncated text content
const posts = await pb.collection('posts').getList(1, 20, {
  fields: 'id,title,content:excerpt(200,true)'
});
// content is truncated to 200 chars with "..." appended

// Multiple excerpts
const posts = await pb.collection('posts').getList(1, 20, {
  fields: 'id,title:excerpt(50),content:excerpt(150,true)'
});

// Excerpt syntax: field:excerpt(maxLength, withEllipsis?)
// - maxLength: maximum characters
// - withEllipsis: append "..." if truncated (default: false)
```

**Common field selection patterns:**

```javascript
// List view - minimal data
const listFields = 'id,title,thumbnail,author,created';

// Card view - slightly more
const cardFields = 'id,title,content:excerpt(200,true),thumbnail,author,created';

// Detail view - most fields
const detailFields = '*,expand.author.name,expand.author.avatar';

// Autocomplete - just id and display text
const autocompleteFields = 'id,name';

// Table export - specific columns
const exportFields = 'id,email,name,created,status';

// Usage
async function getPostsList() {
  return pb.collection('posts').getList(1, 20, {
    fields: listFields,
    expand: 'author'
  });
}
```

**Performance impact:**

| Field Type | Impact of Selecting |
|------------|-------------------|
| text/editor | High (can be large) |
| file | Medium (URLs generated) |
| json | Medium (can be large) |
| relation | Low (just IDs) |
| number/bool | Low |

**Note:** Field selection happens after data is fetched from database, so it primarily saves bandwidth, not database queries. For database-level optimization, ensure proper indexes.

Reference: [PocketBase Fields Parameter](https://pocketbase.io/docs/api-records/#fields)

## 5. Use getFirstListItem for Single Record Lookups

**Impact: MEDIUM (Cleaner code, automatic error handling for not found)**

Use `getFirstListItem()` when you need to find a single record by a field value other than ID. It's cleaner than `getList()` with limit 1 and provides proper error handling.

**Incorrect (manual single-record lookup):**

```javascript
// Using getList with limit 1 - verbose
async function findUserByEmail(email) {
  const result = await pb.collection('users').getList(1, 1, {
    filter: pb.filter('email = {:email}', { email })
  });

  if (result.items.length === 0) {
    throw new Error('User not found');
  }

  return result.items[0];
}

// Using getFullList then filtering - wasteful
async function findUserByUsername(username) {
  const users = await pb.collection('users').getFullList({
    filter: pb.filter('username = {:username}', { username })
  });
  return users[0];  // Might be undefined!
}

// Fetching by ID when you have a different identifier
async function findProductBySku(sku) {
  // Wrong: getOne expects the record ID
  const product = await pb.collection('products').getOne(sku);  // Fails!
}
```

**Correct (using getFirstListItem):**

```javascript
// Clean single-record lookup by any field
async function findUserByEmail(email) {
  try {
    const user = await pb.collection('users').getFirstListItem(
      pb.filter('email = {:email}', { email })
    );
    return user;
  } catch (error) {
    if (error.status === 404) {
      return null;  // Not found
    }
    throw error;
  }
}

// Lookup by unique field
async function findProductBySku(sku) {
  return pb.collection('products').getFirstListItem(
    pb.filter('sku = {:sku}', { sku })
  );
}

// Lookup with expand
async function findOrderByNumber(orderNumber) {
  return pb.collection('orders').getFirstListItem(
    pb.filter('orderNumber = {:num}', { num: orderNumber }),
    { expand: 'customer,items' }
  );
}

// Complex filter conditions
async function findActiveSubscription(userId) {
  return pb.collection('subscriptions').getFirstListItem(
    pb.filter(
      'user = {:userId} && status = "active" && expiresAt > @now',
      { userId }
    )
  );
}

// With field selection
async function getUserIdByEmail(email) {
  const user = await pb.collection('users').getFirstListItem(
    pb.filter('email = {:email}', { email }),
    { fields: 'id' }
  );
  return user.id;
}
```

**Comparison with getOne:**

```javascript
// getOne - fetch by record ID
const post = await pb.collection('posts').getOne('abc123');

// getFirstListItem - fetch by any filter (use pb.filter for safe binding)
const post = await pb.collection('posts').getFirstListItem(
  pb.filter('slug = {:slug}', { slug: 'hello-world' })
);
const user = await pb.collection('users').getFirstListItem(
  pb.filter('username = {:name}', { name: 'john' })
);
const order = await pb.collection('orders').getFirstListItem(
  pb.filter('orderNumber = {:num}', { num: 12345 })
);
```

**Error handling:**

```javascript
// getFirstListItem throws 404 if no match found
try {
  const user = await pb.collection('users').getFirstListItem(
    pb.filter('email = {:email}', { email })
  );
  return user;
} catch (error) {
  if (error.status === 404) {
    // No matching record - handle appropriately
    return null;
  }
  // Other error (network, auth, etc.)
  throw error;
}

// Wrapper function for optional lookup
async function findFirst(collection, filter, options = {}) {
  try {
    return await pb.collection(collection).getFirstListItem(filter, options);
  } catch (error) {
    if (error.status === 404) return null;
    throw error;
  }
}

// Usage
const user = await findFirst('users', pb.filter('email = {:e}', { e: email }));
if (!user) {
  console.log('User not found');
}
```

**When to use each method:**

| Method | Use When |
|--------|----------|
| `getOne(id)` | You have the record ID |
| `getFirstListItem(filter)` | Finding by unique field (email, slug, sku) |
| `getList(1, 1, { filter })` | Need pagination metadata |
| `getFullList({ filter })` | Expecting multiple results |

Reference: [PocketBase Records API](https://pocketbase.io/docs/api-records/)

## 6. Prevent N+1 Query Problems

**Impact: HIGH (Reduces API calls from N+1 to 1-2, dramatically faster page loads)**

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

## 7. Use Efficient Pagination Strategies

**Impact: HIGH (10-100x faster list queries on large collections)**

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

