---
title: Clear, Action-Oriented Title (e.g., "Use Cursor-Based Pagination for Large Lists")
impact: MEDIUM
impactDescription: Brief description of performance/security impact
tags: relevant, comma-separated, tags
---

## [Rule Title]

[1-2 sentence explanation of the problem and why it matters. Focus on impact.]

**Incorrect (describe the problem):**

```javascript
// Comment explaining what makes this problematic
const result = await pb.collection('posts').getList();
// Problem explanation
```

**Correct (describe the solution):**

```javascript
// Comment explaining why this is better
const result = await pb.collection('posts').getList(1, 20, {
  filter: 'published = true',
  sort: '-created'
});
// Benefit explanation
```

[Optional: Additional context, edge cases, or trade-offs]

Reference: [PocketBase Docs](https://pocketbase.io/docs/)
