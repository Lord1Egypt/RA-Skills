# SQLite Client API Reference

## open() Configuration Parameters

```typescript
const db = await open({
  filename: string,   // File path, ':memory:' for anonymous in-memory database, '' for anonymous disk database
  mode?: number,      // sqlite3.OPEN_READONLY | OPEN_READWRITE | OPEN_CREATE, default READWRITE | CREATE
  driver: any         // sqlite3.Database or compatible driver
})
```

### Custom Driver

Any library conforming to the sqlite3 API can be used as a driver:

```js
const sqlite3Offline = require('sqlite3-offline-next')
const db = await open({
  filename: './data.db',
  driver: sqlite3Offline.Database
})
```

### Opening Multiple Databases

```js
const [db1, db2] = await Promise.all([
  open({ filename: './db1.db', driver: sqlite3.Database }),
  open({ filename: './db2.db', driver: sqlite3.Database })
])
```

## Database Methods

### db.get(sql, [...params])

Returns the first matching row, or `undefined` if no match.

```js
const row = await db.get('SELECT * FROM users WHERE id = ?', 1)
const row2 = await db.get('SELECT * FROM users WHERE id = ?', [1])
const row3 = await db.get('SELECT * FROM users WHERE id = :id', { ':id': 1 })
```

### db.all(sql, [...params])

Returns an array of all matching rows.

```js
const rows = await db.all('SELECT * FROM users LIMIT ?', [100])
```

### db.run(sql, [...params])

Executes a write operation, returning `{ lastID, changes, stmt }`.

```js
const { lastID, changes } = await db.run('INSERT INTO users (name) VALUES (?)', 'Alice')
const { changes: updated } = await db.run('UPDATE users SET name = ? WHERE id = ?', 'Bob', 1)
```

### db.exec(sql)

Executes multiple SQL statements (no return value). Suitable for creating tables, batch inserts, etc.

```js
await db.exec(`
  CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT);
  INSERT INTO users (name) VALUES ('Alice');
  INSERT INTO users (name) VALUES ('Bob');
`)
```

### db.each(sql, [...params], callback)

Processes rows one by one with a callback. `callback(err, row)` is triggered once per row; the Promise resolves to the total row count.

```js
const count = await db.each('SELECT * FROM users', [], (err, row) => {
  if (err) throw err
  console.log(row)
})
console.log(`Processed ${count} rows`)
```

### db.prepare(sql, [...params])

Creates a prepared statement, returning a Statement object.

```js
const stmt = await db.prepare('INSERT INTO users (name) VALUES (?)')
await stmt.run('Alice')
await stmt.run('Bob')
await stmt.finalize()
```

### db.migrate(config)

Runs SQL migration files.

```js
await db.migrate({
  force?: boolean,            // Force rollback and re-run latest migration
  table?: string,             // Migration record table name, default 'migrations'
  migrationsPath?: string     // Migration directory, default cwd + '/migrations'
})
```

### db.close()

Closes the database connection.

```js
await db.close()
```

### db.getDatabaseInstance()

Gets the underlying sqlite3 driver instance for calling unwrapped methods.

```js
const rawDb = db.getDatabaseInstance()
```

## Statement Methods

### stmt.run([...params])

Executes the prepared statement, returning the same structure as `db.run()`.

### stmt.get([...params])

Returns the first matching row.

### stmt.all([...params])

Returns all matching rows.

### stmt.bind([...params])

Binds parameters to an already prepared statement.

```js
const stmt = await db.prepare('SELECT * FROM users WHERE id = ? AND name = ?')
await stmt.bind([1, 'Alice'])
const row = await stmt.get()
```

### stmt.finalize()

Releases prepared statement resources. **Must be called** to prevent memory leaks.

### stmt.getStatementInstance()

Gets the underlying sqlite3 Statement instance.

## Compatibility with sql-template-strings

```js
const SQL = require('sql-template-strings')

const book = 'harry potter'
const data = await db.all(SQL`SELECT * FROM books WHERE name = ${book}`)
```

## TypeScript Generics

```typescript
interface User { id: number; name: string; email: string }

const row = await db.get<User>('SELECT * FROM users WHERE id = ?', 1)
// row: User | undefined

const rows = await db.all<User[]>('SELECT * FROM users')
// rows: User[]
```

## Common PRAGMAs

```js
await db.exec('PRAGMA journal_mode=WAL')      // Optimize for concurrent writes
await db.exec('PRAGMA foreign_keys=ON')       // Enable foreign key constraints
await db.exec('PRAGMA busy_timeout=5000')     // Lock wait timeout in ms
const info = await db.all('PRAGMA table_info(users)')  // Table schema
const indexList = await db.all('PRAGMA index_list(users)')  // Index list
```

## FAQ

### SQLITE_BUSY Error

Multiple writers conflicting. Solutions:
1. Set `PRAGMA busy_timeout=5000`
2. Use WAL mode `PRAGMA journal_mode=WAL`
3. Serialize write operations

### Database File Locked

Ensure all `db` connections are closed after use with `await db.close()`. For long-running processes, consider using a connection pool pattern.

### Performance Optimization

- Wrap batch inserts in a transaction using `db.exec()`:
  ```js
  await db.exec('BEGIN')
  for (const item of items) {
    await db.run('INSERT INTO tbl VALUES (?, ?)', item.a, item.b)
  }
  await db.exec('COMMIT')
  ```
- Use `db.each()` to process large datasets row by row, avoiding loading everything into memory
- Use prepared statements `db.prepare()` for frequently executed queries