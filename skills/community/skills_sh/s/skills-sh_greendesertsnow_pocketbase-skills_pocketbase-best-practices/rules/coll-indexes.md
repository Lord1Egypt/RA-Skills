---
title: Create Indexes for Frequently Filtered Fields
impact: CRITICAL
impactDescription: 10-100x faster queries on large collections
tags: collections, indexes, performance, query-optimization
---

## Create Indexes for Frequently Filtered Fields

PocketBase uses SQLite which benefits significantly from proper indexing. Queries filtering or sorting on unindexed fields perform full table scans.

**Incorrect (no indexes on filtered fields):**

```javascript
// Querying without indexes
const posts = await pb.collection('posts').getList(1, 20, {
  filter: 'author = "user123" && status = "published"',
  sort: '-publishedAt'
});
// Full table scan on large collections - very slow

// API rules also query without indexes
// listRule: "author = @request.auth.id"
// Every list request scans entire table
```

**Correct (indexed fields):**

```javascript
// Create collection with indexes via Admin UI or migration
// In PocketBase Admin: Collection > Indexes > Add Index

// Common index patterns:
// 1. Single field index for equality filters
//    CREATE INDEX idx_posts_author ON posts(author)

// 2. Composite index for multiple filters
//    CREATE INDEX idx_posts_author_status ON posts(author, status)

// 3. Index with sort field
//    CREATE INDEX idx_posts_status_published ON posts(status, publishedAt DESC)

// Queries now use indexes
const posts = await pb.collection('posts').getList(1, 20, {
  filter: 'author = "user123" && status = "published"',
  sort: '-publishedAt'
});
// Index scan - fast even with millions of records

// For unique constraints (e.g., slug)
// CREATE UNIQUE INDEX idx_posts_slug ON posts(slug)
```

**Index recommendations:**
- Fields used in `filter` expressions
- Fields used in `sort` parameters
- Fields used in API rules (`listRule`, `viewRule`, etc.)
- Relation fields (automatically indexed)
- Unique fields like slugs or codes

**Index considerations for SQLite:**
- Composite indexes work left-to-right (order matters)
- Too many indexes slow down writes
- Use `EXPLAIN QUERY PLAN` in SQL to verify index usage
- Partial indexes for filtered subsets

```sql
-- Check if index is used
EXPLAIN QUERY PLAN
SELECT * FROM posts WHERE author = 'user123' AND status = 'published';
-- Should show "USING INDEX" not "SCAN"
```

Reference: [SQLite Query Planning](https://www.sqlite.org/queryplanner.html)
