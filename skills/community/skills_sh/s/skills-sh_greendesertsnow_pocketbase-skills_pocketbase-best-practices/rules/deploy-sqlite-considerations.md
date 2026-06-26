---
title: Optimize SQLite for Production
impact: LOW-MEDIUM
impactDescription: Better performance and reliability for SQLite database
tags: production, sqlite, database, performance
---

## Optimize SQLite for Production

PocketBase uses SQLite with optimized defaults. Understanding its characteristics helps optimize performance and avoid common pitfalls. PocketBase uses two separate databases: `data.db` (application data) and `auxiliary.db` (logs and ephemeral data), which reduces write contention.

**Incorrect (ignoring SQLite characteristics):**

```javascript
// Heavy concurrent writes - SQLite bottleneck
async function bulkInsert(items) {
  // Parallel writes cause lock contention
  await Promise.all(items.map(item =>
    pb.collection('items').create(item)
  ));
}

// Not using transactions for batch operations
async function updateMany(items) {
  for (const item of items) {
    await pb.collection('items').update(item.id, item);
  }
  // Each write is a separate transaction - slow!
}

// Large text fields without consideration
const schema = [{
  name: 'content',
  type: 'text'  // Could be megabytes - affects all queries
}];
```

**Correct (SQLite-optimized patterns):**

```javascript
// Use batch operations for multiple writes
async function bulkInsert(items) {
  const batch = pb.createBatch();
  items.forEach(item => {
    batch.collection('items').create(item);
  });
  await batch.send();  // Single transaction, much faster
}

// Batch updates
async function updateMany(items) {
  const batch = pb.createBatch();
  items.forEach(item => {
    batch.collection('items').update(item.id, item);
  });
  await batch.send();
}

// For very large batches, chunk them
async function bulkInsertLarge(items, chunkSize = 100) {
  for (let i = 0; i < items.length; i += chunkSize) {
    const chunk = items.slice(i, i + chunkSize);
    const batch = pb.createBatch();
    chunk.forEach(item => batch.collection('items').create(item));
    await batch.send();
  }
}
```

**Schema considerations:**

```javascript
// Separate large content into dedicated collection
const postsSchema = [
  { name: 'title', type: 'text' },
  { name: 'summary', type: 'text', options: { maxLength: 500 } },
  { name: 'author', type: 'relation' }
  // Content in separate collection
];

const postContentsSchema = [
  { name: 'post', type: 'relation', required: true },
  { name: 'content', type: 'editor' }  // Large HTML content
];

// Fetch content only when needed
async function getPostList() {
  return pb.collection('posts').getList(1, 20);  // Fast, no content
}

async function getPostWithContent(id) {
  const post = await pb.collection('posts').getOne(id);
  const content = await pb.collection('post_contents').getFirstListItem(
    pb.filter('post = {:id}', { id })
  );
  return { ...post, content: content.content };
}
```

**PocketBase default PRAGMA settings:**

PocketBase already configures optimal SQLite settings. You do not need to set these manually unless using a custom SQLite driver:

```sql
PRAGMA busy_timeout       = 10000;  -- Wait 10s for locks instead of failing immediately
PRAGMA journal_mode       = WAL;    -- Write-Ahead Logging: concurrent reads during writes
PRAGMA journal_size_limit = 200000000;  -- Limit WAL file to ~200MB
PRAGMA synchronous        = NORMAL; -- Balanced durability/performance (safe with WAL)
PRAGMA foreign_keys       = ON;     -- Enforce relation integrity
PRAGMA temp_store         = MEMORY; -- Temp tables in memory (faster sorts/joins)
PRAGMA cache_size         = -32000; -- 32MB page cache
```

WAL mode is the most impactful setting -- it allows multiple concurrent readers while a single writer is active, which is critical for PocketBase's concurrent API request handling.

**Index optimization:**

```sql
-- Create indexes for commonly filtered/sorted fields
CREATE INDEX idx_posts_author ON posts(author);
CREATE INDEX idx_posts_created ON posts(created DESC);
CREATE INDEX idx_posts_status_created ON posts(status, created DESC);

-- Verify indexes are being used
EXPLAIN QUERY PLAN
SELECT * FROM posts WHERE author = 'xxx' ORDER BY created DESC;
-- Should show: "USING INDEX idx_posts_author"
```

**SQLite limitations and workarounds:**

| Limitation | Workaround |
|------------|------------|
| Single writer | Use batch operations, queue writes |
| No full-text by default | Use view collections with FTS5 |
| File-based | SSD storage, avoid network mounts |
| Memory for large queries | Pagination, limit result sizes |

**Performance monitoring:**

```javascript
// Monitor slow queries via hooks (requires custom PocketBase build)
// Or use SQLite's built-in profiling

// From sqlite3 CLI:
// .timer on
// SELECT * FROM posts WHERE author = 'xxx';
// Run Time: real 0.003 user 0.002 sys 0.001

// Check database size
// ls -lh pb_data/data.db

// Vacuum to reclaim space after deletes
// sqlite3 pb_data/data.db "VACUUM;"
```

**When to consider alternatives:**

Consider migrating from single PocketBase if:
- Write throughput consistently > 1000/sec needed
- Database size > 100GB
- Complex transactions across tables
- Multi-region deployment required

**Custom SQLite driver (advanced):**

PocketBase supports custom SQLite drivers via `DBConnect`. The CGO driver (`mattn/go-sqlite3`) can offer better performance for some workloads and enables extensions like ICU and FTS5. This requires a custom PocketBase build:

```go
// main.go (custom PocketBase build with CGO driver)
package main

import (
    "github.com/pocketbase/dbx"
    "github.com/pocketbase/pocketbase"
    _ "github.com/mattn/go-sqlite3"  // CGO SQLite driver
)

func main() {
    app := pocketbase.NewWithConfig(pocketbase.Config{
        // Called twice: once for data.db, once for auxiliary.db
        DBConnect: func(dbPath string) (*dbx.DB, error) {
            return dbx.Open("sqlite3", dbPath)
        },
    })

    if err := app.Start(); err != nil {
        panic(err)
    }
}
// Build with: CGO_ENABLED=1 go build
```

Note: CGO requires C compiler toolchain and cannot be cross-compiled as easily as pure Go.

**Scaling options:**
1. **Read replicas**: Litestream for SQLite replication
2. **Sharding**: Multiple PocketBase instances by tenant/feature
3. **Caching**: Redis/Memcached for read-heavy loads
4. **Alternative backend**: If requirements exceed SQLite, evaluate PostgreSQL-based frameworks

Reference: [PocketBase Going to Production](https://pocketbase.io/docs/going-to-production/)
