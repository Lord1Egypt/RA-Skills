# Skill: better-sqlite3 Guide for OpenClaw Agents

## Purpose

This skill teaches an agent how to use `better-sqlite3` as an embedded persistence layer.

Use this when the agent needs:

- Local structured memory
- Ledger-like storage
- Fast single-file database
- Search/query capability
- Aggregation/reporting
- Low-tool-call operations through a reusable utility wrapper

---

# Core Mental Model

SQLite is:

- One database = one `.db` file
- No server required
- SQL query engine inside process
- ACID compliant
- Supports:
  - CRUD
  - indexes
  - transactions
  - search
  - aggregate reporting

Node library:

`better-sqlite3`

is synchronous, fast, and ideal for agents.

---

# SECTION 1 — Installation

## Local Project Install

```bash
npm install better-sqlite3
```

---

## Global Install (for agent utilities)

```bash
npm install -g better-sqlite3
```

(Usually better practice is local project install.)

Verify:

```bash
npm list better-sqlite3
```

or

```bash
npm ls better-sqlite3
```

---

# SECTION 2 — Basic Connection

```javascript
const Database = require('better-sqlite3')

const db = new Database('memory.db')
```

Creates:

```text
memory.db
```

if missing.

---

## Recommended PRAGMA Setup

Always initialize:

```javascript
db.pragma('journal_mode = WAL')
db.pragma('foreign_keys = ON')
db.pragma('synchronous = NORMAL')
```

Recommended defaults.

---

# SECTION 3 — Table Creation

Example:

```javascript
db.exec(`
CREATE TABLE IF NOT EXISTS customers(
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT NOT NULL,
 city TEXT,
 balance REAL DEFAULT 0,
 created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
`)
```

---

# SECTION 4 — CRUD

---

## CREATE (Insert)

Pattern:

```javascript
const stmt=
db.prepare(`
INSERT INTO customers
(name,city,balance)
VALUES (?,?,?)
`)

stmt.run(
 'Daksh',
 'Bhuj',
 5000
)
```

---

## Insert Multiple

```javascript
const insert=db.prepare(`
INSERT INTO customers
(name,city,balance)
VALUES (?,?,?)
`)

const many=db.transaction((rows)=>{
 for (const r of rows){
   insert.run(
    r.name,
    r.city,
    r.balance
   )
 }
})

many([
 {name:'Daksh',city:'Bhuj',balance:5000},
 {name:'Rahul',city:'Surat',balance:3000}
])
```

Use transactions for bulk inserts.

---

## READ

Fetch one:

```javascript
let row=db.prepare(
'SELECT * FROM customers WHERE id=?'
).get(1)
```

---

Fetch many:

```javascript
let rows=db.prepare(
'SELECT * FROM customers'
).all()
```

---

Conditional:

```javascript
SELECT *
FROM customers
WHERE balance > 1000
```

---

## UPDATE

```javascript
db.prepare(`
UPDATE customers
SET balance=?
WHERE id=?
`).run(
7000,
1
)
```

---

Increment update:

```sql
UPDATE customers
SET balance=balance+500
WHERE id=1
```

Useful for ledger balances.

---

## DELETE

```javascript
db.prepare(`
DELETE FROM customers
WHERE id=?
`).run(1)
```

---

# SECTION 5 — SEARCH

---

## Exact Search

```sql
SELECT *
FROM customers
WHERE city='Bhuj'
```

---

## Partial Search

```sql
SELECT *
FROM customers
WHERE name LIKE '%Dak%'
```

---

## Multi-condition Search

```sql
SELECT *
FROM customers
WHERE city='Bhuj'
AND balance > 1000
```

---

## Ordering Search

```sql
SELECT *
FROM customers
ORDER BY balance DESC
```

---

## Pagination

```sql
SELECT *
FROM customers
LIMIT 10 OFFSET 20
```

---

## Full-text Search (FTS)

Create FTS index:

```sql
CREATE VIRTUAL TABLE notes
USING fts5(content)
```

Insert:

```sql
INSERT INTO notes(content)
VALUES ('Inventory adjusted')
```

Search:

```sql
SELECT *
FROM notes
WHERE notes MATCH 'inventory'
```

Useful for agent memory search.

---

## Indexes For Fast Search

```sql
CREATE INDEX idx_city
ON customers(city)
```

Very important.

---

# SECTION 6 — Aggregate Functions

---

## SUM

```sql
SELECT
SUM(balance)
FROM customers
```

Example:

total receivables.

---

## AVG

```sql
SELECT
AVG(balance)
FROM customers
```

---

## COUNT

```sql
SELECT
COUNT(*)
FROM customers
```

---

## MAX

```sql
SELECT MAX(balance)
FROM customers
```

---

## MIN

```sql
SELECT MIN(balance)
FROM customers
```

---

## GROUP BY Aggregates

City-wise balances:

```sql
SELECT
city,
SUM(balance)
FROM customers
GROUP BY city
```

---

Average by city:

```sql
SELECT
city,
AVG(balance)
FROM customers
GROUP BY city
```

---

Count by city:

```sql
SELECT
city,
COUNT(*)
FROM customers
GROUP BY city
```

---

## HAVING (aggregate filtering)

```sql
SELECT
city,
SUM(balance) total
FROM customers
GROUP BY city
HAVING total > 10000
```

Powerful reporting pattern.

---

# SECTION 7 — Transactions

Critical for accounting-like operations.

```javascript
const transfer=db.transaction(()=>{
  debit.run(...)
  credit.run(...)
})
transfer()
```

All-or-nothing.

---

# SECTION 8 — Utility Script (Single Exec Tool Wrapper)

Goal:

Minimize multiple agent tool calls.

Create:

```text
sqlite-util.js
```

---

## Utility Script

```javascript
const Database=require('better-sqlite3')
const db=new Database('memory.db')

db.pragma('journal_mode=WAL')

const cmd=process.argv[2]

if(cmd==='query'){
 const sql=process.argv[3]
 console.log(
  JSON.stringify(
   db.prepare(sql).all(),
   null,
   2
  )
 )
}

if(cmd==='exec'){
 const sql=process.argv[3]
 db.exec(sql)
 console.log('ok')
}

if(cmd==='insert_customer'){
 db.prepare(`
 INSERT INTO customers
(name,city,balance)
VALUES (?,?,?)
 `).run(
 process.argv[3],
 process.argv[4],
 process.argv[5]
 )
 console.log('inserted')
}

if(cmd==='sum_balance'){
 console.log(
  db.prepare(`
   SELECT SUM(balance) t
   FROM customers
  `).get().t
 )
}
```

---

# Invocation Examples

## Generic Query

```bash
node sqlite-util.js query \
"select * from customers"
```

---

## Execute SQL

```bash
node sqlite-util.js exec \
"update customers set balance=0"
```

---

## Insert

```bash
node sqlite-util.js insert_customer \
Daksh Bhuj 5000
```

---

## Aggregate

```bash
node sqlite-util.js sum_balance
```

---

This lets agent use one exec call for many operations.

Very efficient.

---

# SECTION 9 — Common Agent Patterns

---

## Key-value Memory Table

```sql
memory(
key TEXT PRIMARY KEY,
value TEXT
)
```

---

## Event Journal

```sql
events(
id,
event_type,
payload,
created_at
)
```

Append-only.

---

## Accounting Ledger

```sql
ledger(
id,
voucher_no,
account,
debit,
credit
)
```

---

# SECTION 10 — Safety Rules

Always:

- use parameterized queries

Good:

```javascript
WHERE id=?
```

Bad:

string concatenation.

Avoid injection.

---

Always use transactions for:

- transfers
- journal posting
- bulk operations

---

Add indexes on searched fields.

---

Backup:

```bash
cp memory.db memory-backup.db
```

Simple snapshot strategy.

---

# Section 11 — Useful Agent SQL Recipes

Total balance:

```sql
SELECT SUM(balance)
FROM customers
```

---

Top 5 balances:

```sql
SELECT *
FROM customers
ORDER BY balance DESC
LIMIT 5
```

---

Search keyword:

```sql
SELECT *
FROM customers
WHERE name LIKE '%Dak%'
```

---

Count records:

```sql
SELECT COUNT(*)
FROM customers
```

---

# Decision Guidance

Use SQLite instead of:

- JSON flat files
- CSV pseudo databases

when:

- data changes often
- search matters
- aggregates needed
- multiple operations per task
- ledger integrity matters

---

# Preferred Stack

Recommended:

- better-sqlite3
- WAL mode
- utility wrapper
- single exec tool calls

Ideal for OpenClaw skills.
