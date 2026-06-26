---
name: sqlite-client
description: SQLite database operations. Use this skill when users need to create, read, query, or modify SQLite databases (.db files).
---

# SQLite Client

Use the `sqlite` (v5+) + `sqlite3` libraries to operate SQLite databases. All APIs return ES6 Promises and support async/await.

## Use Cases

- Creating SQLite databases and tables
- Executing SQL queries (SELECT/INSERT/UPDATE/DELETE)
- Database migrations
- Reading or analyzing the contents of .db files
- Importing/exporting data to/from SQLite
- Using in-memory databases for rapid prototyping

## Prerequisites

Before performing any database operations, ensure dependencies are installed in the project:

```bash
npm install sqlite3 sqlite
```

## Quick Start

### Opening a Database

```js
const sqlite3 = require('sqlite3')
const { open } = require('sqlite')

async function getDb() {
  return open({
    filename: './data.db',       // File path, or ':memory:' for in-memory database
    driver: sqlite3.Database
  })
}
```

### Using Cached Instances

```js
driver: sqlite3.cached.Database  // Reuse connections for the same file
```

### Closing the Database

```js
await db.close()
```

## Core Operations

### Creating Tables & Inserting Data

```js
await db.exec('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, email TEXT)')
await db.exec(`INSERT INTO users (name, email) VALUES ('Alice', 'alice@example.com')`)
```

### Querying a Single Row

```js
const row = await db.get('SELECT * FROM users WHERE id = ?', [1])
// row = { id: 1, name: 'Alice', email: 'alice@example.com' } or undefined
```

### Querying Multiple Rows

```js
const rows = await db.all('SELECT * FROM users WHERE name LIKE ?', ['%li%'])
// rows = [{ id: 1, name: 'Alice', ... }]
```

### Inserting a Row

```js
const result = await db.run('INSERT INTO users (name, email) VALUES (?, ?)', ['Bob', 'bob@example.com'])
// result.lastID → New row ID
// result.changes → Number of rows affected
```

### Updating / Deleting Rows

```js
const result = await db.run('UPDATE users SET name = ? WHERE id = ?', ['Bob Updated', 2])
// result.changes → Number of rows affected

await db.run('DELETE FROM users WHERE id = ?', [2])
```

### Named Parameters

```js
await db.get('SELECT * FROM users WHERE name = :name', { ':name': 'Alice' })
await db.run('INSERT INTO users (name, email) VALUES (:name, :email)', { ':name': 'Carol', ':email': 'carol@example.com' })
```

### Prepared Statements

```js
const stmt = await db.prepare('INSERT INTO users (name, email) VALUES (?, ?)')
await stmt.run('Dave', 'dave@example.com')
await stmt.run('Eve', 'eve@example.com')
await stmt.finalize()  // Must finalize after use
```

### Iterating Row by Row (each)

```js
const rowCount = await db.each(
  'SELECT * FROM users',
  [],
  (err, row) => {
    if (err) throw err
    console.log(row.name)
  }
)
// rowCount → Total number of rows processed
```

## Migrations

Create a `migrations/` folder in the project directory, name SQL files sequentially (e.g., `001-init.sql`), and then execute:

```js
await db.migrate({
  force: false,                    // true to rollback and reapply the latest migration
  table: 'migrations',             // Name of the migration record table
  migrationsPath: './migrations'   // Path to migration files
})
```

Example migration file `migrations/001-init.sql`:

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## Utility Functions

Common patterns for reading the contents of a `.db` file:

```js
// List all tables
const tables = await db.all("SELECT name FROM sqlite_master WHERE type='table'")

// Get table schema
const info = await db.all(`PRAGMA table_info(${tableName})`)

// Get row count
const { count } = await db.get(`SELECT COUNT(*) as count FROM ${tableName}`)
```

## Debugging

```js
const sqlite3 = require('sqlite3')
sqlite3.verbose()  // Enable verbose logging

db.on('trace', (sql) => {
  console.log('SQL:', sql)
})
```

## Notes

- The `db` object returned by `open()` wraps `sqlite3.Database`; all methods return Promises.
- `db.exec()` is used for executing multiple SQL statements (no return value); `db.run()` is for single write operations.
- Prepared statements must be `finalize()`d after use to prevent memory leaks.
- SQLite supports a maximum database file size of 281 TB, with a maximum row size of approximately 1 GB.
- For concurrent writes, use WAL mode: `await db.exec('PRAGMA journal_mode=WAL')`

## Advanced Reference

For detailed API documentation and more usage patterns, see [references/api.md](references/api.md).