---
title: Select Only Required Fields
impact: MEDIUM
impactDescription: Reduces payload size, improves response time
tags: query, fields, performance, bandwidth
---

## Select Only Required Fields

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
