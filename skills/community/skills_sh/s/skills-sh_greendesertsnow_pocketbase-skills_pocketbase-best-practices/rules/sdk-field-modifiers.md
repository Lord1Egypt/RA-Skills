---
title: Use Field Modifiers for Incremental Updates
impact: HIGH
impactDescription: Atomic updates, prevents race conditions, cleaner code
tags: sdk, modifiers, relations, files, numbers, atomic
---

## Use Field Modifiers for Incremental Updates

PocketBase supports `+` and `-` modifiers for incrementing numbers, appending/removing relation IDs, and managing file arrays without replacing the entire value.

**Incorrect (read-modify-write pattern):**

```javascript
// Race condition: two users adding tags simultaneously
async function addTag(postId, newTagId) {
  const post = await pb.collection('posts').getOne(postId);
  const currentTags = post.tags || [];

  // Another user might have added a tag in between!
  await pb.collection('posts').update(postId, {
    tags: [...currentTags, newTagId]  // Might overwrite the other user's tag
  });
}

// Inefficient for incrementing counters
async function incrementViews(postId) {
  const post = await pb.collection('posts').getOne(postId);
  await pb.collection('posts').update(postId, {
    views: post.views + 1  // Extra read, race condition
  });
}
```

**Correct (using field modifiers):**

```javascript
// Atomic relation append with + modifier
async function addTag(postId, newTagId) {
  await pb.collection('posts').update(postId, {
    'tags+': newTagId  // Appends to existing tags atomically
  });
}

// Append multiple relations
async function addTags(postId, tagIds) {
  await pb.collection('posts').update(postId, {
    'tags+': tagIds  // Appends array of IDs
  });
}

// Prepend relations (+ prefix)
async function prependTag(postId, tagId) {
  await pb.collection('posts').update(postId, {
    '+tags': tagId  // Prepends to start of array
  });
}

// Remove relations with - modifier
async function removeTag(postId, tagId) {
  await pb.collection('posts').update(postId, {
    'tags-': tagId  // Removes specific tag
  });
}

// Remove multiple relations
async function removeTags(postId, tagIds) {
  await pb.collection('posts').update(postId, {
    'tags-': tagIds  // Removes all specified tags
  });
}

// Atomic number increment
async function incrementViews(postId) {
  await pb.collection('posts').update(postId, {
    'views+': 1  // Atomic increment, no race condition
  });
}

// Atomic number decrement
async function decrementStock(productId, quantity) {
  await pb.collection('products').update(productId, {
    'stock-': quantity  // Atomic decrement
  });
}

// File append (for multi-file fields)
async function addImage(albumId, newImage) {
  await pb.collection('albums').update(albumId, {
    'images+': newImage  // Appends new file to existing
  });
}

// File removal
async function removeImage(albumId, filename) {
  await pb.collection('albums').update(albumId, {
    'images-': filename  // Removes specific file by name
  });
}

// Combined modifiers in single update
async function updatePost(postId, data) {
  await pb.collection('posts').update(postId, {
    title: data.title,        // Replace field
    'views+': 1,              // Increment number
    'tags+': data.newTagId,   // Append relation
    'tags-': data.oldTagId,   // Remove relation
    'images+': data.newImage  // Append file
  });
}
```

**Modifier reference:**

| Modifier | Field Types | Description |
|----------|-------------|-------------|
| `field+` or `+field` | relation, file | Append/prepend to array |
| `field-` | relation, file | Remove from array |
| `field+` | number | Increment by value |
| `field-` | number | Decrement by value |

**Benefits:**
- **Atomic**: No read-modify-write race conditions
- **Efficient**: Single request, no extra read needed
- **Clean**: Expresses intent clearly

**Note:** Modifiers only work with `update()`, not `create()`.

Reference: [PocketBase Relations](https://pocketbase.io/docs/working-with-relations/)
