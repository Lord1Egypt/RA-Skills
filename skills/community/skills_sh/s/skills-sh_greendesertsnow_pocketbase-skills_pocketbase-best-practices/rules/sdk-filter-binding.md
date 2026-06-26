---
title: Use Safe Parameter Binding in Filters
impact: CRITICAL
impactDescription: Prevents injection attacks, handles special characters correctly
tags: sdk, filters, security, injection, parameters
---

## Use Safe Parameter Binding in Filters

Always use `pb.filter()` with parameter binding when constructing filters with user input. String concatenation is vulnerable to injection attacks.

**Incorrect (string concatenation - DANGEROUS):**

```javascript
// SQL/filter injection vulnerability!
async function searchPosts(userInput) {
  // User input: `test" || id != "` breaks out of string
  const posts = await pb.collection('posts').getList(1, 20, {
    filter: `title ~ "${userInput}"`  // VULNERABLE!
  });
  return posts;
}

// Even with escaping, easy to get wrong
async function searchByEmail(email) {
  const escaped = email.replace(/"/g, '\\"');  // Incomplete escaping
  const users = await pb.collection('users').getList(1, 1, {
    filter: `email = "${escaped}"`  // Still potentially vulnerable
  });
  return users;
}

// Template literals are just as dangerous
const filter = `status = "${status}" && author = "${authorId}"`;
```

**Correct (using pb.filter with parameters):**

```javascript
// Safe parameter binding
async function searchPosts(userInput) {
  const posts = await pb.collection('posts').getList(1, 20, {
    filter: pb.filter('title ~ {:search}', { search: userInput })
  });
  return posts;
}

// Multiple parameters
async function filterPosts(status, authorId, minViews) {
  const posts = await pb.collection('posts').getList(1, 20, {
    filter: pb.filter(
      'status = {:status} && author = {:author} && views >= {:views}',
      { status, author: authorId, views: minViews }
    )
  });
  return posts;
}

// Reusing parameters
async function searchBothFields(query) {
  const results = await pb.collection('posts').getList(1, 20, {
    filter: pb.filter(
      'title ~ {:q} || content ~ {:q}',
      { q: query }  // Same parameter used twice
    )
  });
  return results;
}

// Different parameter types
async function complexFilter(options) {
  const filter = pb.filter(
    'created > {:date} && active = {:active} && category = {:cat}',
    {
      date: new Date('2024-01-01'),  // Date objects handled correctly
      active: true,                    // Booleans
      cat: options.category            // Strings auto-escaped
    }
  );

  return pb.collection('posts').getList(1, 20, { filter });
}

// Null handling
async function filterWithOptional(category) {
  // Only include filter if value provided
  const filter = category
    ? pb.filter('category = {:cat}', { cat: category })
    : '';

  return pb.collection('posts').getList(1, 20, { filter });
}

// Building dynamic filters
async function dynamicSearch(filters) {
  const conditions = [];
  const params = {};

  if (filters.title) {
    conditions.push('title ~ {:title}');
    params.title = filters.title;
  }

  if (filters.author) {
    conditions.push('author = {:author}');
    params.author = filters.author;
  }

  if (filters.minDate) {
    conditions.push('created >= {:minDate}');
    params.minDate = filters.minDate;
  }

  const filter = conditions.length > 0
    ? pb.filter(conditions.join(' && '), params)
    : '';

  return pb.collection('posts').getList(1, 20, { filter });
}
```

**Supported parameter types:**

| Type | Example | Notes |
|------|---------|-------|
| string | `'hello'` | Auto-escaped, quotes handled |
| number | `123`, `45.67` | No quotes added |
| boolean | `true`, `false` | Converted correctly |
| Date | `new Date()` | Formatted for PocketBase |
| null | `null` | For null comparisons |
| other | `{...}` | JSON.stringify() applied |

**Server-side is especially critical:**

```javascript
// Server-side code (Node.js, Deno, etc.) MUST use binding
// because malicious users control the input directly

export async function searchHandler(req) {
  const userQuery = req.query.q;  // Untrusted input!

  // ALWAYS use pb.filter() on server
  const results = await pb.collection('posts').getList(1, 20, {
    filter: pb.filter('title ~ {:q}', { q: userQuery })
  });

  return results;
}
```

Reference: [PocketBase Filters](https://pocketbase.io/docs/api-rules-and-filters/)
