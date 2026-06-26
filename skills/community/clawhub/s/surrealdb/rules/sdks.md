# SurrealDB SDK Reference

This document covers SDK usage patterns for the officially documented SDKs
(Rust, JavaScript, Python, Go, Java, .NET, PHP) plus first-party or
SurrealDB-org SDK repos that are still pre-release or not fully documented
(C, Swift, Kotlin, Ruby). Each section states whether the package is published
and whether examples are verified against a release or only against upstream
source.

---

## JavaScript / TypeScript SDK

**Package**: `surrealdb` on npm
**Repository**: github.com/surrealdb/surrealdb.js

### Installation

```bash
npm install surrealdb

# For embedded Node.js engine
npm install @surrealdb/node

# For WASM browser engine
npm install @surrealdb/wasm
```

### Engine Options

The JS/TS SDK supports three distinct engines:

| Engine | Package | Use Case |
|--------|---------|----------|
| Remote (HTTP/WebSocket) | `surrealdb` | Client-server applications |
| Node.js embedded | `@surrealdb/node` | Server-side apps without separate DB process |
| WASM (browser) | `@surrealdb/wasm` | Browser-based applications, offline-first |

### Connection Patterns

```typescript
import { Surreal, RecordId, Table } from "surrealdb";

const db = new Surreal();

// --- Remote connections ---
// WebSocket (recommended for live queries and subscriptions)
await db.connect("wss://host:8000");

// HTTP (stateless, suitable for serverless)
await db.connect("https://host:8000");

// --- Embedded Node.js connections (requires @surrealdb/node) ---
// In-memory (data lost on process exit)
await db.connect("mem://");

// RocksDB persistent storage
await db.connect("rocksdb://path.db");

// SurrealKV persistent storage
await db.connect("surrealkv://path.db");

// SurrealKV with versioned storage (supports historical queries)
await db.connect("surrealkv+versioned://path.db");

// --- WASM browser connections (requires @surrealdb/wasm) ---
// In-memory
await db.connect("mem://");

// IndexedDB persistent storage (browser only)
await db.connect("indxdb://mydb");
```

### Authentication

```typescript
// Root-level authentication
await db.signin({
  username: "root",
  password: "root",
});

// Namespace-level authentication
await db.signin({
  namespace: "my_ns",
  username: "ns_user",
  password: "ns_pass",
});

// Database-level authentication
await db.signin({
  namespace: "my_ns",
  database: "my_db",
  username: "db_user",
  password: "db_pass",
});

// Record-level (scope) authentication
const token = await db.signin({
  namespace: "my_ns",
  database: "my_db",
  access: "user_access",
  variables: {
    email: "user@example.com",
    password: "user_pass",
  },
});

// Sign up a new record user
const token = await db.signup({
  namespace: "my_ns",
  database: "my_db",
  access: "user_access",
  variables: {
    email: "new@example.com",
    password: "new_pass",
    name: "New User",
  },
});

// Use an existing token
await db.authenticate(token);

// Invalidate the current session
await db.invalidate();
```

### Namespace and Database Selection

```typescript
await db.use({
  namespace: "my_ns",
  database: "my_db",
});

// Or set individually
await db.use({ namespace: "my_ns" });
await db.use({ database: "my_db" });
```

### CRUD Operations

```typescript
// --- Create ---
// Create with auto-generated ID
const person = await db.create("person", {
  name: "Alice",
  age: 30,
});

// Create with specific ID
const specific = await db.create(new RecordId("person", "alice"), {
  name: "Alice",
  age: 30,
});

// --- Select ---
// Select all records from a table
const allPeople = await db.select("person");

// Select a specific record
const alice = await db.select(new RecordId("person", "alice"));

// --- Update (full replacement) ---
// Replace all fields on a record
const updated = await db.update(new RecordId("person", "alice"), {
  name: "Alice Smith",
  age: 31,
  email: "alice@example.com",
});

// --- Merge (partial update) ---
// Update only specified fields, keep the rest
const merged = await db.merge(new RecordId("person", "alice"), {
  age: 32,
});

// --- Patch (JSON Patch operations) ---
const patched = await db.patch(new RecordId("person", "alice"), [
  { op: "replace", path: "/age", value: 33 },
  { op: "add", path: "/verified", value: true },
]);

// --- Delete ---
// Delete a specific record
await db.delete(new RecordId("person", "alice"));

// Delete all records in a table
await db.delete("person");
```

### Queries

```typescript
// Simple query
const results = await db.query("SELECT * FROM person WHERE age > 25");

// Parameterized query (prevents injection)
const results = await db.query(
  "SELECT * FROM person WHERE age > $min_age AND name = $name",
  {
    min_age: 25,
    name: "Alice",
  }
);

// Typed query results
interface Person {
  id: RecordId;
  name: string;
  age: number;
}

const [people] = await db.query<[Person[]]>(
  "SELECT * FROM person WHERE age > $min_age",
  { min_age: 25 }
);

// Multiple statements in one query
const [people, orders] = await db.query<[Person[], Order[]]>(`
  SELECT * FROM person WHERE active = true;
  SELECT * FROM order WHERE status = 'pending';
`);
```

### Live Queries

```typescript
// Subscribe to changes on a table
const stream = await db.live("person");

// Process events with async iteration
for await (const event of stream) {
  switch (event.action) {
    case "CREATE":
      console.log("New person:", event.result);
      break;
    case "UPDATE":
      console.log("Updated person:", event.result);
      break;
    case "DELETE":
      console.log("Deleted person:", event.result);
      break;
  }
}

// Live query with a filter
const stream = await db.live("person", {
  filter: "age > 25",
});

// Kill a live query
await db.kill(stream.id);
```

### RecordId Usage

```typescript
import { RecordId, Table } from "surrealdb";

// Create a RecordId
const id = new RecordId("person", "alice");
console.log(id.table);  // "person"
console.log(id.id);     // "alice"

// Numeric IDs
const numericId = new RecordId("person", 123);

// Complex IDs (arrays, objects)
const complexId = new RecordId("temperature", ["London", new Date()]);

// Table reference (for operations on all records)
const table = new Table("person");
```

### Error Handling

```typescript
import { Surreal, SurrealError, ConnectionError } from "surrealdb";

try {
  await db.connect("wss://host:8000");
  await db.signin({ username: "root", password: "root" });
} catch (error) {
  if (error instanceof ConnectionError) {
    console.error("Failed to connect:", error.message);
  } else if (error instanceof SurrealError) {
    console.error("SurrealDB error:", error.message);
  }
}
```

### Connection Lifecycle and Reconnection

```typescript
const db = new Surreal();

// Connect with event handlers
db.on("connected", () => console.log("Connected"));
db.on("disconnected", () => console.log("Disconnected"));
db.on("error", (err) => console.error("Error:", err));

await db.connect("wss://host:8000");

// Graceful shutdown
await db.close();
```

---

## JavaScript / TypeScript SDK v2 (GA -- recommended for new projects)

**Package**: `surrealdb` on npm (v2.0.3)
**Status**: General availability. Full SurrealDB 3.0.x support. Recommended for
new projects. The v1 API above is maintained but v2 is the future.

**v2.0.3 changes**:
- Export API supports the new server-side export options exposed by SurrealDB 3.0.5
- `BoundQuery` values can be interpolated directly into the `surql` template literal
- `patch` function signature corrected (#580)
- Includes the earlier v2.0.2 improvements for streamed import/export, blob import, and `StringRecordId` return normalization

The v2 SDK is a ground-up rewrite with an engine-based architecture, multi-session
support, client-side transactions, query builder patterns, streaming responses,
automatic token refresh, and full SurrealDB 3.0 compatibility.

**v2.0.0 GA highlights** (2026-02-25):
- Full SurrealDB 3.0.1 support (embedded WASM and Node engines updated)
- Engine-based architecture (createRemoteEngines, createNodeEngines, createWasmEngines)
- Multi-session support (newSession, forkSession, await using)
- Client-side transactions
- Automatic token refreshing with refresh token exchange
- Redesigned live query API with subscribe/async iteration
- Query builder pattern with chainable methods
- Expressions API (eq, ne, or, and, between, inside, raw, surql template tag)
- Diagnostics API for protocol-level inspection
- Codec visitor API for custom encode/decode
- User-defined API invocation (.api())
- Web Worker support via createWasmWorkerEngines with createWorker factory

### Installation

```bash
npm install surrealdb

# Embedded engines (published in sync with the SDK)
npm install @surrealdb/node
npm install @surrealdb/wasm
```

### Engine Architecture (v2)

The v2 SDK separates engines from the Surreal class. You compose engines
explicitly in the constructor.

```typescript
import { Surreal, createRemoteEngines } from "surrealdb";
import { createNodeEngines } from "@surrealdb/node";
import { createWasmEngines, createWasmWorkerEngines } from "@surrealdb/wasm";

// Remote only (HTTP + WebSocket)
const db = new Surreal({
  engines: createRemoteEngines(),
});

// Remote + embedded Node.js
const db = new Surreal({
  engines: {
    ...createRemoteEngines(),
    ...createNodeEngines(),
  },
});

// Remote + WASM (browser)
const db = new Surreal({
  engines: {
    ...createRemoteEngines(),
    ...createWasmEngines(),
  },
});

// WASM in a Web Worker (offloads DB ops from main thread)
// NOTE: beta.2+ requires createWorker factory for Vite compatibility
import WorkerAgent from "@surrealdb/wasm/worker?worker";

const db = new Surreal({
  engines: {
    ...createRemoteEngines(),
    ...createWasmWorkerEngines({
      createWorker: () => new WorkerAgent(),
    }),
  },
});
```

### Connection with Auto Token Refresh (v2)

```typescript
const db = new Surreal();

await db.connect("wss://host:8000", {
  namespace: "test",
  database: "test",
  renewAccess: true,  // auto-refresh expired tokens (default: true)
  authentication: {
    username: "root",
    password: "root",
  },
});

// Or use a callable for async/deferred auth
await db.connect("wss://host:8000", {
  namespace: "test",
  database: "test",
  authentication: () => ({
    username: "root",
    password: "root",
  }),
});
```

### Event Listeners (v2)

```typescript
// Type-safe event subscriptions (replaces v1 .on() pattern)
const unsub = db.subscribe("connected", () => {
  console.log("Connected");
});

// Cleanup
unsub();

// Access internal state
console.log(db.namespace);     // current namespace
console.log(db.database);      // current database
console.log(db.accessToken);   // current access token
console.log(db.refreshToken);  // current refresh token
console.log(db.params);        // defined connection params
```

### Multi-Session Support (v2)

```typescript
// Create an isolated session (own namespace, database, auth state)
const session = await db.newSession();
await session.signin({ username: "other_user", password: "pass" });
await session.use({ namespace: "other_ns", database: "other_db" });

// Fork a session (clone its state)
const forked = await session.forkSession();

// Close a session
await session.closeSession();

// Automatic cleanup with await using (TC39 Explicit Resource Management)
{
  await using session = await db.newSession();
  // session is automatically closed at end of scope
}
```

### Query Builder Pattern (v2)

v2 introduces chainable builder methods on all query functions. `update` and
`upsert` no longer take contents as a second argument; use `.content()`,
`.merge()`, `.replace()`, or `.patch()` instead.

```typescript
import { Table, RecordId } from "surrealdb";

const usersTable = new Table("users");

// Select with field selection and fetch
const record = await db.select(new RecordId("person", "alice"))
  .fields("age", "firstname", "lastname")
  .fetch("orders");

// Select with where filter
const active = await db.select(usersTable)
  .where(eq("active", true));

// Update with merge (v2 pattern)
await db.update(new RecordId("person", "alice")).merge({
  age: 32,
  verified: true,
});

// Update with content (full replace)
await db.update(new RecordId("person", "alice")).content({
  name: "Alice Smith",
  age: 32,
});

// Upsert with merge
await db.upsert(new RecordId("person", "bob")).merge({
  name: "Bob",
  active: true,
});
```

**IMPORTANT (v2 breaking change)**: Query functions no longer accept plain strings
as table names. You must use the `Table` class:

```typescript
// v1 (still works in v1 SDK)
await db.select("person");

// v2 (required)
await db.select(new Table("person"));
```

### Query Method Overhaul (v2)

```typescript
// Basic typed query
const [user] = await db.query<[User]>("SELECT * FROM user:foo");

// Collect specific result indexes from multi-statement queries
const [users, orders] = await db.query(
  "LET $u = SELECT * FROM user; LET $o = SELECT * FROM order; RETURN $u; RETURN $o"
).collect<[User[], Order[]]>(2, 3);

// Auto-jsonify results
const [products] = await db.query<[Product[]]>(
  "SELECT * FROM product"
).json();

// Get full response objects (including status, time, etc.)
const responses = await db.query<[Product[]]>(
  "SELECT * FROM product"
).responses();

// Stream responses (prepare for future per-record streaming)
const stream = db.query("SELECT * FROM large_table").stream();

for await (const frame of stream) {
  if (frame.isValue<Product>()) {
    console.log(frame.value);
  } else if (frame.isDone()) {
    console.log("Stats:", frame.stats);
  } else if (frame.isError()) {
    console.error(frame.error);
  }
}
```

### Expressions API (v2)

Compose dynamic, param-safe WHERE expressions:

```typescript
import { eq, ne, or, and, between, inside, raw, surql } from "surrealdb";

// Use with query builder .where()
await db.select(usersTable).where(eq("active", true));

// Compose complex expressions
await db.select(usersTable).where(
  or(
    eq("role", "admin"),
    and(
      eq("active", true),
      between("age", 18, 65)
    )
  )
);

// Use with surql template tag
const isActive = true;
await db.query(surql`SELECT * FROM users WHERE ${eq("active", isActive)}`);

// Raw expression insertion (use with caution)
await db.query(surql`SELECT * FROM users ${raw("WHERE active = true")}`);
```

### Redesigned Live Queries (v2)

```typescript
const live = await db.live(new Table("users"));

// Callback-based (action, result, recordId)
live.subscribe((action, result, record) => {
  console.log(action, result, record);
});

// Async iteration
for await (const { action, value } of live) {
  console.log(action, value);
}

// Kill the live query
live.kill();

// Attach to an existing live query ID
const [id] = await db.query("LIVE SELECT * FROM users");
const existing = await db.liveOf(id);
```

### User-Defined API Invocation (v2)

```typescript
// Call user-defined APIs registered in SurrealDB
const result = await db.api("my_custom_endpoint", {
  param1: "value",
});
```

### Diagnostics API (v2)

Intercept protocol-level communication for debugging:

```typescript
import { applyDiagnostics, createRemoteEngines } from "surrealdb";

const db = new Surreal({
  engines: applyDiagnostics(createRemoteEngines(), (event) => {
    // event: { type, key, phase, duration?, success?, result? }
    console.log(`[${event.type}] ${event.phase}`, event.duration);
  }),
});
```

Event types: `open`, `version`, `use`, `signin`, `query`, `reset`.
Each event has `before`, `progress` (queries only), and `after` phases.

### Codec Visitor API (v2)

Custom encode/decode processing for SurrealDB values:

```typescript
const db = new Surreal({
  codecOptions: {
    valueDecodeVisitor(value) {
      // Transform RecordIds, Dates, or custom types on decode
      return value;
    },
    valueEncodeVisitor(value) {
      // Transform values before sending to SurrealDB
      return value;
    },
  },
});
```

### Migration Guide: v1 to v2

| v1 Pattern | v2 Equivalent |
|------------|---------------|
| `new Surreal()` | `new Surreal({ engines: createRemoteEngines() })` |
| `db.connect("wss://...")` | Same, but with `authentication` option for auto-refresh |
| `db.on("connected", fn)` | `db.subscribe("connected", fn)` -- returns unsub function |
| `db.select("person")` | `db.select(new Table("person"))` |
| `db.update(id, data)` | `db.update(id).content(data)` or `.merge(data)` |
| `db.merge(id, data)` | `db.update(id).merge(data)` |
| `db.query(q).then(([r]) => ...)` | `db.query(q).collect<[T]>(0)` |
| `db.live("person")` then iterate | `db.live(new Table("person"))` then `.subscribe()` or `for await` |
| N/A | `db.newSession()` -- isolated sessions |
| N/A | `db.query(q).stream()` -- streaming responses |
| N/A | `db.api("endpoint")` -- user-defined APIs |
| N/A | `applyDiagnostics()` -- protocol inspection |

---

## Python SDK

**Package**: `surrealdb` on PyPI (v2.0.0 GA, released 2026-04-23)
**Repository**: github.com/surrealdb/surrealdb.py
**Status**: Stable for the published v2 package. Upstream `main` is already
tracking an unreleased v3.0.0 Python API (`846f5de6df41`, 2026-05-12); do not
write v3-only code unless you pin to that source commit or a future published
v3 release.

**v2.0.0 GA highlights** (2026-04-23, promoted from `v2.0.0-alpha.1`):
- SurrealDB 3.x feature support (#230)
- Python 3.9 dropped; minimum is now Python 3.10
- Structured error handling with typed error classes (#233)
- WebSocket session transaction ID bug fixed (#236)
- musl Linux wheel/binary support for Alpine and slim containers (#241)
- Pydantic Logfire instrumentation with README example (#229)
- README slimmed and developer docs moved to CONTRIBUTING.md (#243)
- Release-notification workflow added (#240, #244)

**Post-v2.0.0 upstream main (not on PyPI as of 2026-05-14)**:
- CRUD methods (`create`, `update`, `upsert`, `delete`, `insert`) move to an
  awaitable/lazy builder API with chainable `.content()`, `.merge()`,
  `.replace()`, `.patch()`, and `.relation()` clauses.
- `query()` now returns all statement results: a single value for one statement,
  or a tuple for multi-statement queries / transaction blocks. `query().into()`
  maps multi-result outputs onto dataclasses.
- `run(name, args)` exposes the `RUN` RPC.
- The old `db.merge(record, data)`, `db.patch(record, data)`, and
  `db.insert_relation(table, data)` forms are removed in the v3 API.
- Embedded engines were split into a separate optional package:
  `pip install surrealdb[embedded]` installs `surrealdb-embedded`; the base
  package is HTTP/WebSocket only. Without the extra, `mem://`, `file://`, and
  `surrealkv://` raise `UnsupportedEngineError`.
- Builder execution is intentionally idempotent and guarded against several
  injection/reconfiguration hazards, but sync-builder truthiness/comparison can
  still execute the pending RPC. Avoid idioms like `if db.query("DELETE ...")`;
  call `.execute()` explicitly for fire-and-forget operations.

### Installation

```bash
pip install surrealdb

# Unreleased-main v3 pattern once published:
# pip install "surrealdb[embedded]"
```

### Synchronous API

```python
from surrealdb import Surreal

# Context manager ensures clean connection lifecycle
with Surreal("ws://localhost:8000/rpc") as db:
    db.signin({"username": "root", "password": "root"})
    db.use("test", "test")

    # Create
    person = db.create("person", {"name": "Alice", "age": 30})

    # Create with specific ID
    db.create("person:alice", {"name": "Alice", "age": 30})

    # Select all
    people = db.select("person")

    # Select one
    alice = db.select("person:alice")

    # Update (full replace)
    db.update("person:alice", {"name": "Alice Smith", "age": 31})

    # Merge (partial update)
    db.merge("person:alice", {"age": 32})

    # Delete
    db.delete("person:alice")

    # Query with parameters
    result = db.query(
        "SELECT * FROM person WHERE age > $min_age",
        {"min_age": 25}
    )

    # Raw query
    result = db.query("SELECT * FROM person")
```

### Asynchronous API

```python
import asyncio
from surrealdb import AsyncSurreal

async def main():
    async with AsyncSurreal("ws://localhost:8000/rpc") as db:
        await db.signin({"username": "root", "password": "root"})
        await db.use("test", "test")

        # All CRUD operations are async
        person = await db.create("person", {"name": "Bob", "age": 25})
        people = await db.select("person")
        result = await db.query("SELECT * FROM person WHERE age > $min", {"min": 20})

asyncio.run(main())
```

### Embedded Connections

Published v2.0.0 includes embedded support in the main `surrealdb` package. The
unreleased v3 API splits embedded support into the optional
`surrealdb-embedded` package. In v3 main, base `surrealdb` installs no Rust
extension, and embedded URLs (`mem://`, `file://`, `surrealkv://`) fail with
install guidance unless the `[embedded]` extra is present.

```python
# In-memory (data lost when process exits)
async with AsyncSurreal("mem://") as db:
    await db.use("test", "test")
    await db.create("person", {"name": "Alice"})

# File-backed persistence
async with AsyncSurreal("file:///path/to/db") as db:
    await db.use("test", "test")
    await db.create("person", {"name": "Alice"})

# v3 main also wires SurrealKV through the embedded extra
async with AsyncSurreal("surrealkv://path/to/db") as db:
    await db.use("test", "test")
```

### Authentication Patterns

```python
# Root authentication
db.signin({"username": "root", "password": "root"})

# Namespace authentication
db.signin({
    "namespace": "my_ns",
    "username": "ns_user",
    "password": "ns_pass",
})

# Database authentication
db.signin({
    "namespace": "my_ns",
    "database": "my_db",
    "username": "db_user",
    "password": "db_pass",
})

# Record user authentication
token = db.signin({
    "namespace": "my_ns",
    "database": "my_db",
    "access": "user_access",
    "variables": {
        "email": "user@example.com",
        "password": "secret",
    },
})

# Sign up
token = db.signup({
    "namespace": "my_ns",
    "database": "my_db",
    "access": "user_access",
    "variables": {
        "email": "new@example.com",
        "password": "new_pass",
    },
})

# Token-based authentication
db.authenticate(token)
```

### Sessions and Transactions (WebSocket only)

```python
# Transactions are only available over WebSocket connections
with Surreal("ws://localhost:8000/rpc") as db:
    db.signin({"username": "root", "password": "root"})
    db.use("test", "test")

    # Run multiple statements atomically
    result = db.query("""
        BEGIN TRANSACTION;
        CREATE account:alice SET balance = 100;
        CREATE account:bob SET balance = 50;
        UPDATE account:alice SET balance -= 25;
        UPDATE account:bob SET balance += 25;
        COMMIT TRANSACTION;
    """)
```

### Pydantic and Dataclass Mapping

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Person:
    name: str
    age: int
    email: Optional[str] = None

# Query results can be mapped to dataclasses
result = db.query("SELECT * FROM person")
people = [Person(**record) for record in result]
```

### Pydantic Logfire Observability

The Python SDK integrates with Pydantic Logfire for tracing and observability of database operations. Refer to the Logfire documentation for setup details.

---

## Go SDK

**Package**: `github.com/surrealdb/surrealdb.go` (v1.4.0, released 2026-03-03; main HEAD `aef39d3`, 2026-04-30)
**Repository**: github.com/surrealdb/surrealdb.go

**v1.4.0 changes** (latest tagged release):
- SurrealDB v3 structured error handling: new `surrealdb.ServerError` type for extracting v3 error fields. Existing `RPCError` and `QueryError` continue to work for v2 compatibility.
- Identifier sanitization in restore to prevent SQL injection (#375)
- Added `models.Table` example for select operations (#379)

**Post-v1.4.0 main**: 8 commits since the v1.4.0 tag (no new release tag yet). Pin to `v1.4.0` for stability; review main HEAD if you need very recent fixes.

### Installation

```bash
go get github.com/surrealdb/surrealdb.go
```

### Connection

The Go SDK supports two connection engines per upstream `db.go`:
WebSocket and HTTP. **Embedded URL schemes (`mem://`, `surrealkv://`,
`rocksdb://`) are not supported** -- the previous documentation
that showed `surrealdb.New("mem://")` was wrong. The `New(url)` entry
point itself is also marked `Deprecated` in current upstream;
`FromEndpointURLString(ctx, url)` is the recommended replacement.

```go
package main

import (
    "context"
    surrealdb "github.com/surrealdb/surrealdb.go"
)

func main() {
    ctx := context.Background()

    // Preferred entry point (current API)
    db, err := surrealdb.FromEndpointURLString(ctx, "ws://localhost:8000")
    if err != nil {
        panic(err)
    }
    defer db.Close(ctx)  // Close takes ctx

    // HTTP works the same way
    // db, err = surrealdb.FromEndpointURLString(ctx, "http://localhost:8000")
}
```

### Authentication and namespace selection

`SignIn` capitalizes both letters; the method takes `ctx` first then
an `any`-typed credential payload (struct or map). `Use` takes
`ctx, ns, database`. Both return errors that must be checked.

```go
// Sign in -- SignIn (capital I), takes ctx + any-typed credential
_, err = db.SignIn(ctx, surrealdb.Auth{
    Username: "root",
    Password: "root",
})
if err != nil {
    panic(err)
}

// Select namespace and database
err = db.Use(ctx, "my_ns", "my_db")
if err != nil {
    panic(err)
}
```

### CRUD with Struct Mapping

```go
type Person struct {
    ID    string `json:"id,omitempty"`
    Name  string `json:"name"`
    Age   int    `json:"age"`
    Email string `json:"email,omitempty"`
}

// Create
person, err := surrealdb.Create[Person](db, ctx, "person", Person{
    Name: "Alice",
    Age:  30,
})

// Select all
people, err := surrealdb.Select[[]Person](db, ctx, "person")

// Select one
alice, err := surrealdb.Select[Person](db, ctx, "person:alice")

// Update (full replace)
updated, err := surrealdb.Update[Person](db, ctx, "person:alice", Person{
    Name:  "Alice Smith",
    Age:   31,
    Email: "alice@example.com",
})

// Merge (partial update)
merged, err := surrealdb.Merge[Person](db, ctx, "person:alice", map[string]interface{}{
    "age": 32,
})

// Delete
err = db.Delete(ctx, "person:alice")

// Query
results, err := surrealdb.Query[[]Person](db, ctx,
    "SELECT * FROM person WHERE age > $min_age",
    map[string]interface{}{"min_age": 25},
)
```

### Context-Based Operations

All Go SDK operations accept a `context.Context` parameter, enabling timeout control, cancellation propagation, and deadline management.

```go
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

people, err := surrealdb.Select[[]Person](db, ctx, "person")
if err != nil {
    // Handle timeout or cancellation
}
```

---

## Rust SDK

**Crate**: `surrealdb`
**Repository**: github.com/surrealdb/surrealdb

### Cargo.toml

```toml
[dependencies]
surrealdb = "3"
tokio = { version = "1", features = ["full"] }
serde = { version = "1", features = ["derive"] }
```

### Connection

```rust
use surrealdb::Surreal;
use surrealdb::engine::remote::ws::Ws;
use surrealdb::engine::remote::http::Http;
use surrealdb::engine::local::{Mem, RocksDb, SurrealKv};

// WebSocket
let db = Surreal::new::<Ws>("localhost:8000").await?;

// HTTP
let db = Surreal::new::<Http>("localhost:8000").await?;

// Embedded in-memory
let db = Surreal::new::<Mem>(()).await?;

// Embedded RocksDB
let db = Surreal::new::<RocksDb>("path.db").await?;

// Embedded SurrealKV
let db = Surreal::new::<SurrealKv>("path.db").await?;
```

### Authentication

```rust
use surrealdb::opt::auth::Root;

db.signin(Root {
    username: "root",
    password: "root",
}).await?;

db.use_ns("my_ns").use_db("my_db").await?;
```

### CRUD with Serde

```rust
use serde::{Deserialize, Serialize};
use surrealdb::RecordId;

#[derive(Debug, Serialize, Deserialize)]
struct Person {
    name: String,
    age: u32,
    email: Option<String>,
}

#[derive(Debug, Deserialize)]
struct Record {
    id: RecordId,
}

// Create
let created: Vec<Record> = db.create("person")
    .content(Person {
        name: "Alice".to_string(),
        age: 30,
        email: None,
    })
    .await?;

// Create with specific ID
let alice: Option<Record> = db.create(("person", "alice"))
    .content(Person {
        name: "Alice".to_string(),
        age: 30,
        email: None,
    })
    .await?;

// Select all
let people: Vec<Person> = db.select("person").await?;

// Select one
let alice: Option<Person> = db.select(("person", "alice")).await?;

// Update
let updated: Option<Person> = db.update(("person", "alice"))
    .content(Person {
        name: "Alice Smith".to_string(),
        age: 31,
        email: Some("alice@example.com".to_string()),
    })
    .await?;

// Merge
let merged: Option<Person> = db.update(("person", "alice"))
    .merge(serde_json::json!({ "age": 32 }))
    .await?;

// Delete
let _: Option<Person> = db.delete(("person", "alice")).await?;
```

### Queries

```rust
// Parameterized query
let mut result = db.query("SELECT * FROM person WHERE age > $min_age")
    .bind(("min_age", 25))
    .await?;

let people: Vec<Person> = result.take(0)?;

// Multiple statements
let mut result = db.query("SELECT * FROM person; SELECT * FROM order;").await?;
let people: Vec<Person> = result.take(0)?;
let orders: Vec<Order> = result.take(1)?;
```

### Live Queries

```rust
use surrealdb::Notification;
use futures::StreamExt;

let mut stream = db.select("person").live().await?;

while let Some(notification) = stream.next().await {
    let notification: Notification<Person> = notification?;
    match notification.action {
        Action::Create => println!("Created: {:?}", notification.data),
        Action::Update => println!("Updated: {:?}", notification.data),
        Action::Delete => println!("Deleted: {:?}", notification.data),
        _ => {}
    }
}
```

---

## Java SDK

> **v1.4.3 status note:** the v1.4.0 / v1.4.1 / v1.4.2 versions of
> this section pinned a non-existent Maven version (`3.0.0`) and
> documented an API surface (`db.connect("ws://...")`,
> `db.signin("root", "root")`, `db.use("ns", "db")`,
> `db.create("person", Map.of(...))`, `db.queryAsync(...)` returning
> `CompletableFuture<...>`) that did not match the actual upstream
> SDK. **Verified upstream on 2026-05-14** -- `repo1.maven.org`
> shows `latest=2.0.1` (last updated 2026-04-28); the API uses
> `Credential` typed objects and chained `useNs()` / `useDb()` calls;
> `queryAsync` and `CompletableFuture` do not appear in the source
> at all.

**Package**: `com.surrealdb:surrealdb` on Maven Central
**Verified version at v1.7.0 cut**: `2.1.1` (2026-06-10; previous
versions `0.1.0`, `0.2.0`, `0.2.1`, `1.0.0-beta.1`, `2.0.0-alpha.1`,
`2.0.0`, `2.0.1`)
**Repository**: `github.com/surrealdb/surrealdb.java`
**Java requirement**: JDK 8+ (verified for 8, 11, 17, 21, 25)
**Native architectures**: Linux ARM/x86_64, Windows x86_64,
macOS ARM/x86_64, Android Linux ARM/x86_64
**Status**: stable

### Maven dependency

```xml
<dependency>
    <groupId>com.surrealdb</groupId>
    <artifactId>surrealdb</artifactId>
    <version>2.1.1</version>
</dependency>
```

Gradle:

```groovy
ext {
    surrealdbVersion = "2.0.1"
}

dependencies {
    implementation "com.surrealdb:surrealdb:${surrealdbVersion}"
}
```

### Connection and authentication

The SDK supports both embedded ("memory") and remote connections.
Authentication takes a typed `Credential` object, not raw strings.

```java
import com.surrealdb.Surreal;
import com.surrealdb.RecordId;
import com.surrealdb.signin.RootCredential;
import com.surrealdb.signin.NamespaceCredential;
import com.surrealdb.signin.DatabaseCredential;

try (Surreal driver = new Surreal()) {
    // Embedded in-memory connection
    driver.connect("memory");

    // Or remote connection (URL scheme is the connection target;
    // verify against current upstream docs for HTTP/WS specifics)
    // driver.connect("ws://localhost:8000");

    // Namespace and database (chained, return NsDb)
    driver.useNs("test").useDb("test");

    // Authentication via typed Credential objects
    driver.signin(new RootCredential("root", "root"));
    // Or: driver.signin(new NamespaceCredential("ns_user", "ns_pass", "my_ns"));
    // Or: driver.signin(new DatabaseCredential("db_user", "db_pass", "my_ns", "my_db"));
}
```

### Typed CRUD with `Class<T>`

The Java SDK uses typed generics: pass a `Class<T>` to identify the
record type and let the SDK marshal between Java types and SurrealDB
records.

```java
static class Person {
    RecordId id;
    String firstName;
    String lastName;
    boolean marketing;

    public Person() {}  // default constructor required
    public Person(String firstName, String lastName, boolean marketing) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.marketing = marketing;
    }
}

// Create returns a List<T>
List<Person> created = driver.create(Person.class, "person",
    new Person("Alice", "Smith", true));

// Select returns an Iterator<T>
Iterator<Person> people = driver.select(Person.class, "person");
while (people.hasNext()) {
    System.out.println(people.next());
}
```

### Queries

The SDK exposes two query methods: `query(sql)` for parameter-free
SurrealQL and `queryBind(sql, params)` for parameterized statements.
There is **no** `queryAsync` and the SDK does **not** return a
`CompletableFuture` from query methods.

```java
// Parameter-free
driver.query("SELECT * FROM person");

// Parameterized
driver.queryBind(
    "SELECT * FROM person WHERE age > $min_age",
    Map.of("min_age", 25));
```

### Cross-references

- Upstream README: `https://github.com/surrealdb/surrealdb.java`
- Upstream Javadoc: `https://surrealdb.github.io/surrealdb.java/javadoc/`
- Upstream docs portal: `https://surrealdb.com/docs/integration/libraries/java`

---

## .NET SDK

**Package**: `SurrealDb.Net` on NuGet (latest verified: `0.10.2`, 2026-04-24)
**Repository**: github.com/surrealdb/surrealdb.net
**Status**: beta. Official README documents HTTP/WS remote connections,
embedded packages (`SurrealDb.Embedded.InMemory`, `.RocksDb`, `.SurrealKv`),
dependency injection, authentication, live queries, and client-side
transactions. API is pre-1.0 and may still change.

### Installation

```bash
dotnet add package SurrealDb.Net
```

### Basic Usage

```csharp
using SurrealDb.Net;
using SurrealDb.Net.Models;

// Create client
var db = new SurrealDbClient("ws://localhost:8000/rpc");
await db.SignIn(new RootAuth { Username = "root", Password = "root" });
await db.Use("my_ns", "my_db");

// Create
var person = await db.Create("person", new Person
{
    Name = "Alice",
    Age = 30
});

// Select all
var people = await db.Select<Person>("person");

// Query
var results = await db.Query(
    "SELECT * FROM person WHERE age > $min_age",
    new { min_age = 25 }
);

// Dispose
await db.DisposeAsync();
```

### Dependency Injection

```csharp
// In Startup.cs or Program.cs
var options = SurrealDbOptions
  .Create()
  .WithEndpoint("http://127.0.0.1:8000")
  .WithNamespace("my_ns")
  .WithDatabase("my_db")
  .WithUsername("root")
  .WithPassword("root")
  .Build();

builder.Services.AddSurreal(options);

// In a service or controller
public class PersonService
{
    private readonly ISurrealDbClient _db;

    public PersonService(ISurrealDbClient db)
    {
        _db = db;
    }

    public async Task<IEnumerable<Person>> GetPeople()
    {
        return await _db.Select<Person>("person");
    }
}
```

Lifetime boundary: `SurrealDbClient` is singleton-compatible; use
`SurrealDbSession` / `ISurrealDbSession` for scoped or transient DI.

### LINQ Integration

```csharp
// Query using LINQ-style expressions where supported
var adults = await db.Select<Person>("person")
    .Where(p => p.Age >= 18)
    .OrderBy(p => p.Name)
    .ToListAsync();
```

---

## PHP SDK

> **v1.4.3 status note:** the previous version of this section used
> `"username"` / `"password"` keys in `signin()` (verified upstream uses
> `"user"` / `"pass"`), did not capture the `signin()` token return
> value, used double-quoted SurrealQL strings (PHP would interpolate
> `$min_age`), and used string record-IDs everywhere where the
> canonical upstream API uses typed `RecordId::create()` and
> `Table::create()` objects. Rechecked 2026-05-14 against the upstream
> `surrealdb/surrealdb.php` README + `src/Surreal.php` source.

**Package**: `surrealdb/surrealdb.php` on Packagist
**Repository**: `github.com/surrealdb/surrealdb.php`

### Installation

```bash
composer require surrealdb/surrealdb.php
```

### Basic usage

```php
use Surreal\Surreal;
use Surreal\Cbor\Types\Record\RecordId;
use Surreal\Cbor\Types\Table;

$db = new Surreal();

// Connect via WebSocket
$db->connect("ws://localhost:8000/rpc");

// Authenticate -- keys are "user" / "pass" upstream (NOT
// "username" / "password"). The signin call returns a token.
$token = $db->signin([
    "user" => "root",
    "pass" => "root",
]);

$db->use(["namespace" => "my_ns", "database" => "my_db"]);

// Create -- prefer typed Table / RecordId objects per the upstream
// canonical API; string targets may work but are not the documented
// surface
$person = $db->create(Table::create("person"), [
    "name" => "Alice",
    "age" => 30,
]);

// Select
$people = $db->select(Table::create("person"));
$alice = $db->select(RecordId::create("person", "alice"));

// Query -- use SINGLE quotes around SurrealQL so PHP doesn't try to
// interpolate `$min_age` as a variable
$results = $db->query(
    'SELECT * FROM person WHERE age > $min_age',
    ["min_age" => 25]
);

// Update
$db->update(RecordId::create("person", "alice"), [
    "name" => "Alice Smith",
    "age" => 31,
]);

// Merge
$db->merge(RecordId::create("person", "alice"), ["age" => 32]);

// Delete
$db->delete(RecordId::create("person", "alice"));

// Close
$db->close();
```

---

## C SDK (`surrealdb.c`)

**Package**: source-only beta; no tagged release or package-registry artifact
verified at the v1.6.6 cut.
**Repository**: `github.com/surrealdb/surrealdb.c`
**Status**: beta / low-level FFI. The upstream README warns that a `cbindgen`
header-ordering issue can cause linking failures; use a published header or
manually reorder headers until upstream resolves it.

The C driver is backed by Rust crates (`surrealdb = 3.0.1`,
`surrealdb-core = 3.0.1`) and builds `staticlib` / `cdylib` outputs. It is a
systems-integration surface, not a general application SDK. Prefer the
language-native SDKs above unless you are embedding SurrealDB behind an FFI
boundary.

```c
#include "path/to/surrealdb.h"

sr_surreal_t *db;
sr_string_t err;

char *endpoint = "ws://localhost:8000";
/* or: char *endpoint = "surrealkv://database.skv"; */

if (sr_connect(&err, &db, endpoint) < 0) {
    printf("failed to connect: %s", err);
    return 1;
}

sr_surreal_disconnect(db);
```

Cross-reference the upstream README before using any API beyond connection and
disconnect; this skill does not yet document the full generated header.

---

## Swift SDK (`surrealdb.swift`)

> **v1.4.2 status note:** the v1.4.0 / v1.4.1 versions of this section
> documented an `iOS 16+ / macOS 13+ / tvOS 16+ / watchOS 9+ / visionOS 1+`
> deployment target, a `from: "1.0.0"` SwiftPM pin, a single
> `Surreal()` client class, a `SurrealKit` Swift bundling, and an API
> surface (`db.connect`, `db.signin(.root(...))`, `db.live(table: ...)`,
> `event.value()`, `event.recordID`, `db.on(.disconnected)`) that did
> not match the actual upstream package. **None of those claims survived
> direct upstream verification on 2026-05-14.** This file remains
> verified-only; full API documentation is deferred until the package
> publishes its first tag.

**Package**: `SurrealDB` (SwiftPM module name in upstream `Package.swift`)
**Repository**: `github.com/surrealdb/surrealdb.swift`
**Status (verified 2026-05-14)**: pre-release. **No git tags published**;
no version on Swift Package Index. The package compiles against
`swift-tools-version: 6.1`.
**Verified platform deployment targets** (from upstream `Package.swift`
on `main`): iOS 17+, macOS 14+, tvOS 17+, watchOS 10+, visionOS 1+.

> **Not bundled with SurrealKit.** SurrealKit is a separate Rust /
> TypeScript schema-management toolkit (`rules/surrealkit.md`) and
> contains zero Swift sources. Treat the SDK and the toolkit as two
> independent dependencies.

### Installation (development-only)

Because no version tag exists, you cannot use `from: "1.0.0"` or any
other version constraint. Pin to a specific commit on `main` for now:

```swift
// Package.swift
.package(
  url: "https://github.com/surrealdb/surrealdb.swift",
  branch: "main"
)
```

Add the `SurrealDB` product to your target dependencies. Update the
pin to a tagged release as soon as upstream publishes one.

### API surface

The actual API surface uses two `actor` clients (verified from
`Sources/SurrealDB/Runtime/Clients.swift`,
`Sources/SurrealDB/Protocols.swift`,
`Sources/SurrealDB/PublicTypes.swift`):

- `SurrealHTTPClient` (conforms to `SurrealQueryable`)
- `SurrealWebSocketClient` (conforms to `SurrealLiveQueryable`)

Both take an `endpoint: String` in their initializer and expose a
`connect()` method as a separate step. Auth uses a `SignInCredentials`
enum (`.root(username:password:)`, `.namespace(...)`, `.database(...)`,
`.accessVariables(...)`, `.accessBearer(...)`). CRUD methods take typed
`SurrealModel`-conforming values rather than table-name strings, and
the package exposes a freestanding macro DSL (`#select`, `#create`,
`#update`, `#delete`, `#live`) plus a `SurrealPredicate` predicate type.

> The exact method signatures, the macro arguments, and the embedded
> engine story (the upstream `Package.swift` does not currently declare
> a `surrealdb-core` FFI dependency) are deferred until the
> first tagged release lands. **Do not copy-paste API examples from
> any earlier version of this rule -- they were hallucinated.**

### Cross-references

- `rules/surrealkit.md` -- the Rust/TS schema toolkit (separate from this SDK)
- `rules/data-modeling.md` -- record IDs, schemafull tables
- Upstream: `https://github.com/surrealdb/surrealdb.swift`

---

## Kotlin SDK (`surrealdb.kotlin`)

> **v1.4.2 status note:** the v1.4.0 / v1.4.1 versions of this section
> documented Maven coordinates `com.surrealdb:surrealdb-kotlin:0.4.0`,
> a `Surreal()` client with `connect()` + typed `query<T>(...)`
> generics, embedded engine support (`db.connect("rocksdb://...")`,
> `db.connect("mem://")`), Kotlin Multiplatform JS / Native targets,
> coroutines `1.8.0` + Kotlin `2.0.0`, plus a `Java SDK strict superset`
> + `@JvmOverloads` interop story. **None of those survived direct
> upstream verification on 2026-05-14.** Shrunk here pending a rewrite
> once the package publishes a Maven Central release.

**Package**: not yet published. The repo's `gradle.properties` declares
`GROUP=com.surrealdb`, `VERSION_NAME=0.1.0-SNAPSHOT`. Maven Central has
**no** `com.surrealdb:surrealdb-kotlin` artifact as of 2026-05-14.
The Java SDK (`com.surrealdb:surrealdb` `2.0.1`) is a separate
artifact; consume that from Kotlin if you need a published JVM client
today.
**Repository**: `github.com/surrealdb/surrealdb.kotlin`
**Verified KMP targets** (from `build.gradle.kts`): `androidTarget()`,
`jvm()`, `iosX64()`, `iosArm64()`, `iosSimulatorArm64()`. **No JS, no
non-Apple Native target.**
**Verified dep versions** (`build.gradle.kts`): Kotlin `2.1.10`,
coroutines `1.10.1`, kotlinx-serialization `1.8.0`.

### API shape (verified, abbreviated)

The actual entry point is `SurrealClient(config: SurrealClientConfig)`
(verified from `SurrealClient.kt` and `SurrealClientConfig.kt`). The
config takes `httpEndpoint` and `wsEndpoint` strings; **there is no
embedded-engine support** in the current source. Base methods return
`JsonElement`:

```kotlin
suspend fun query(sql: String, vars: JsonObject? = null): JsonElement
suspend fun select(thing: String): JsonElement
suspend fun create(thing: String, data: JsonElement? = null): JsonElement
suspend fun update(thing: String, data: JsonElement? = null): JsonElement
suspend fun merge(thing: String, data: JsonElement? = null): JsonElement
suspend fun delete(thing: String): JsonElement
suspend fun live(query: String, vars: JsonObject? = null): LiveQuerySubscription
```

Each base method has a typed companion using a `reified` generic that
decodes the JSON to a `kotlinx.serialization`-compatible type:
`queryAs<T>`, `selectAs<T>`, `createAs<T>`, `insertAs<T>`,
`updateAs<T>`, `mergeAs<T>`, `patchAs<T>`, `deleteAs<T>`. There is
also a `decode<T>(element)` helper. Use the typed helpers when you
have a `@Serializable` data class, or stay on `JsonElement` for
opaque payloads.

Auth goes through a `SurrealAuthInput` sealed interface with
`SignIn(params: JsonObject)` and `Token(token: String)` variants --
there is no `Root` / `Database` data class as of 2026-05-14.

> **Do not copy-paste API examples from any earlier version of this
> rule.** Detailed usage is deferred until a tagged release.

### Cross-references

- `rules/sdks.md` (Java SDK section) -- the published JVM client today
- Upstream: `https://github.com/surrealdb/surrealdb.kotlin`

---

## Ruby SDK (`surrealdb.rb`)

> **v1.4.2 status note:** the v1.4.0 / v1.4.1 versions of this section
> documented Ruby 3.1+ support, a `gem "surrealdb", "~> 1.0"` pin, a
> `surrealdb-embedded` companion gem with FFI to `surrealdb-core`, a
> `surrealdb-rails` companion gem with `SurrealDB::Record` /
> ActiveRecord-shaped chains, an `access:` keyword-style auth variant,
> and a `live(...).each do |event|` enumerator-returning live-query
> shape.
>
> Verified upstream on 2026-05-14:
>
> - `surrealdb-rails` does **not** exist (rubygems.org 404; GitHub
>   `surrealdb/surrealdb-rails` repo 404). The `SurrealDB::Record`
>   class and the ActiveRecord-shaped chain examples were fabricated.
> - `surrealdb-embedded` **does** exist (RubyGems v0.7.0 published
>   2026-04-01 by SurrealDB authors). It provides embedded database
>   support (`mem://`, `surrealkv://`, `file://`) via FFI bindings to
>   `libsurrealdb_c` (not `surrealdb-core` as the v1.4.0 narrative
>   claimed). The v1.4.0 documented API for it was hallucinated; the
>   gem itself is real but its surface needs fresh verification.
> - The pinned `~> 1.0` does not exist -- the latest official release
>   is `0.7.0`.
>
> The main-gem shape below was rewritten on 2026-05-14 to match the
> actual `surrealdb` gem; `surrealdb-embedded` API documentation is
> deferred until a fresh upstream pass.

**Package**: `surrealdb` on RubyGems (verified)
**Verified version at v1.6.6 cut**: `0.7.0` (published 2026-04-01 by
SurrealDB authors)
**Repository**: `github.com/surrealdb/surrealdb.rb`
**Required Ruby**: `>= 3.2` (verified from `surrealdb.gemspec`)
**Documented at**: `https://surrealdb.com/docs/sdk/ruby`

### Installation

```ruby
# Gemfile
gem "surrealdb"  # current latest is 0.7.0; check rubygems.org before pinning
```

```bash
bundle install
```

### Connecting

The constructor takes the connection URL; `connect` is a separate
call:

```ruby
require "surrealdb"

db = SurrealDB::Client.new("ws://localhost:8000/rpc")
db.connect

# signin takes a positional Hash, not keyword args
db.signin({ "user" => "root", "pass" => "root" })
db.use("myapp", "production")
```

### CRUD

```ruby
db.create("person", { name: "Alice", age: 30 })
db.select("person")
db.update(SurrealDB::Thing.new("person", "alice"), { age: 31 })
db.delete("person:alice")
```

### Live queries

`live` returns a UUID (the live-query ID). Subscribe separately:

```ruby
live_id = db.live("person")  # returns a UUID string
db.subscribe(live_id) do |event|
  # event yields the change payload
end
# Later: db.kill(live_id)
```

> **Rails / ActiveRecord adapter:** there is no official adapter as of
> the v1.6.6 cut. Use the SDK directly from your Rails models if you
> need Rails integration.

### Cross-references

- `rules/sdks.md` (other SDKs) -- decision matrix
- Upstream: `https://github.com/surrealdb/surrealdb.rb`
- Upstream docs: `https://surrealdb.com/docs/sdk/ruby`

---

## SDK Selection Guide

> **v1.4.2 status note:** the v1.4.0 / v1.4.1 matrix made claims about
> Swift / Kotlin / Ruby capabilities (embedded engines, live-query
> shapes, mobile targets) that did not match the actual upstream
> packages. The matrix below is restricted to verified facts; rows
> for unreleased SDKs are marked accordingly.

### Decision Matrix

| Factor | JS/TS | Python | Go | Rust | Java | .NET | PHP | Swift | Kotlin | Ruby |
|--------|-------|--------|----|------|------|------|-----|-------|--------|------|
| Published release | Yes | Yes | Yes | Yes | Yes (beta) | Yes | Yes | **No (no tags)** | **No (SNAPSHOT)** | Yes (0.7.0) |
| Embedded engine | Yes | Yes (`mem://` / `file://`) | Yes | Yes | Yes (`memory` only) | Yes (`SurrealDb.Embedded.*` packages) | No | Unverified | No (HTTP/WS only in source) | Yes (`surrealdb-embedded` gem 0.7.0; FFI to `libsurrealdb_c`) |
| WebSocket | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes (actor client) | Yes | Yes |
| HTTP | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes (actor client) | Yes | Yes |
| Live queries | Yes | Yes | Yes | Yes | Limited | Limited | No | Yes (`AsyncStream`) | Yes (`LiveQuerySubscription`) | Yes (UUID + subscribe) |
| WASM (browser) | Yes | No | No | No | No | No | No | No | No | No |
| Async API | Yes | Yes | Yes | Yes | Yes | Yes | No | Yes (Swift Concurrency / actors) | Yes (coroutines) | Yes (`async` runtime) |
| Type safety | TS generics | Type hints | Generics | Strong | Generics | Generics | Weak | Macros + `SurrealModel` | `JsonElement` + `reified` decode helpers (`queryAs<T>`, `selectAs<T>`, ...) | Duck-typed |
| Mobile target | -- | -- | -- | -- | -- | -- | -- | iOS / iPadOS / macOS / tvOS / watchOS / visionOS | Android / iOS (KMP) | -- |

### When to Use Each SDK

- **JavaScript/TypeScript**: web apps, full-stack JS, browser (WASM), serverless, real-time apps.
- **Python**: data science, ML pipelines, scripting, backend APIs (FastAPI/Django), prototyping. Pair with `rules/langchain.md` for RAG.
- **Go**: microservices, high-concurrency servers, CLI tools, cloud-native applications.
- **Rust**: performance-critical apps, systems programming, embedded databases, Surrealism extensions (`rules/surrealism.md`).
- **Java**: enterprise apps, Spring Boot services, JVM codebases. The published Maven artifact today is `com.surrealdb:surrealdb 2.0.1` (verified via `repo1.maven.org/maven2/com/surrealdb/surrealdb/maven-metadata.xml`, last updated 2026-04-28). Supports embedded `memory` mode plus remote connections.
- **Kotlin**: as of 2026-05-14, **no Maven release**; consume the Java SDK from Kotlin until upstream publishes `surrealdb-kotlin`.
- **.NET**: ASP.NET, Windows services, C# codebases, Blazor.
- **PHP**: Laravel/Symfony, WordPress plugins, traditional web apps.
- **C**: FFI/system integration when a native binding is required. Beta, source-only, and currently affected by an upstream `cbindgen` header-ordering caveat.
- **Swift**: as of 2026-05-14, **no published tag**; pin `branch: "main"` only for development. SDK exists; tagged release pending.
- **Ruby**: gem `surrealdb` 0.7.0 published 2026-04-01. No Rails / ActiveRecord adapter at this time; use the SDK directly from Rails models if needed.

### Embedded vs Remote Trade-offs

**Embedded** (in-process database):
- No network latency
- Single-process deployment
- No separate database server to manage
- Limited to single-node (no distributed queries)
- Available in: JS/TS (Node.js, WASM), Python, Go, Rust. Other-language embedded support is unverified as of 2026-05-14.

**Remote** (HTTP/WebSocket to server):
- Shared database across instances
- Supports TiKV for distributed storage
- Independent scaling of compute and storage
- Network latency overhead
- Available in: All SDKs that have published releases.

### Performance characteristics

- **Rust SDK**: lowest overhead; direct library calls when embedded.
- **Go SDK**: efficient goroutine-based concurrency.
- **Node.js embedded**: V8 + native bindings; good for I/O-heavy workloads.
- **Python SDK**: GIL-bound; use async API for I/O-bound workloads.
- **Ruby SDK**: GVL-bound; use the async-runtime client and a connection pool for concurrent workloads.
- **WASM (browser)**: client-side; performance follows browser WASM runtime.
- **Swift / Kotlin SDKs**: pre-release; performance characteristics deferred until tagged releases.
