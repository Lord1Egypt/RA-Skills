---
title: Use Back-Relations for Inverse Lookups
impact: HIGH
impactDescription: Fetch related records without separate queries
tags: query, relations, back-relations, expand, inverse
---

## Use Back-Relations for Inverse Lookups

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
