# SurrealQL Reference

This is the comprehensive SurrealQL language reference for SurrealDB v3. SurrealQL is a SQL-like query language designed for SurrealDB's multi-model architecture, supporting document, graph, relational, vector, time-series, geospatial, and full-text search operations in a single language.

---

## Statements

### CREATE

Creates one or more records in a table.

```surql
-- Create a record with a random ID
CREATE person CONTENT {
    name: 'Tobie',
    age: 33,
    email: 'tobie@surrealdb.com'
};

-- Create a record with a specific ID
CREATE person:tobie SET
    name = 'Tobie',
    age = 33;

-- Create with a UUID-based ID
CREATE person:uuid() SET name = 'Jane';

-- Create with a ULID-based ID
CREATE person:ulid() SET name = 'John';

-- Create multiple records
CREATE person CONTENT [
    { name: 'Alice', age: 28 },
    { name: 'Bob', age: 35 }
];

-- Create with RETURN clause
CREATE person SET name = 'Eve' RETURN id, name;

-- Create with RETURN NONE (no output)
CREATE person SET name = 'Frank' RETURN NONE;

-- Create with RETURN BEFORE / AFTER / DIFF
CREATE person SET name = 'Grace' RETURN AFTER;
```

### SELECT

Retrieves records from one or more tables.

```surql
-- Select all fields from a table
SELECT * FROM person;

-- Select specific fields
SELECT name, age FROM person;

-- Select with alias
SELECT name AS full_name, math::floor(age) AS years FROM person;

-- Conditional filtering
SELECT * FROM person WHERE age > 30 AND name != 'Tobie';

-- Ordering results
SELECT * FROM person ORDER BY age DESC;

-- Limit and pagination
SELECT * FROM person LIMIT 10 START 20;

-- Grouping with aggregation
SELECT country, count() AS total FROM person GROUP BY country;

-- Nested field access
SELECT name.first, address.city FROM person;

-- Array filtering within records
SELECT emails[WHERE active = true] FROM person;

-- Select with value keyword (returns flat array)
SELECT VALUE name FROM person;

-- Select from specific record
SELECT * FROM person:tobie;

-- Select with FETCH to resolve record links
SELECT *, author.name FROM article FETCH author;

-- Select with SPLIT to unnest arrays
SELECT * FROM person SPLIT emails;

-- Select with TIMEOUT
SELECT * FROM person TIMEOUT 5s;

-- Select with PARALLEL execution
SELECT * FROM person PARALLEL;

-- Analyze query plan: either as a clause on SELECT
SELECT * FROM person WHERE age > 30 EXPLAIN;
-- or as a standalone statement (v3 form)
EXPLAIN SELECT * FROM person WHERE age > 30;
EXPLAIN ANALYZE SELECT * FROM person WHERE age > 30;
EXPLAIN FORMAT JSON SELECT * FROM person WHERE age > 30;

-- Subquery in SELECT
SELECT *, (SELECT count() FROM ->wrote->article GROUP ALL) AS article_count FROM person;
```

### UPDATE

Modifies existing records.

```surql
-- Update all records in a table
UPDATE person SET active = true;

-- Update a specific record
UPDATE person:tobie SET age = 34;

-- Merge data into a record
UPDATE person:tobie MERGE {
    settings: { theme: 'dark', lang: 'en' }
};

-- Update with CONTENT (replaces entire record)
UPDATE person:tobie CONTENT {
    name: 'Tobie',
    age: 34,
    active: true
};

-- Conditional update
UPDATE person SET verified = true WHERE age >= 18;

-- Update with RETURN clause
UPDATE person:tobie SET age = 35 RETURN DIFF;
UPDATE person:tobie SET age = 36 RETURN BEFORE;
UPDATE person:tobie SET age = 37 RETURN AFTER;

-- Increment / decrement numeric fields
UPDATE person:tobie SET age += 1;
UPDATE product:widget SET stock -= 5;

-- Append to an array
UPDATE person:tobie SET tags += 'admin';

-- Remove from an array
UPDATE person:tobie SET tags -= 'guest';
```

### DELETE

Removes records from tables.

```surql
-- Delete all records in a table
DELETE person;

-- Delete a specific record
DELETE person:tobie;

-- Conditional delete
DELETE person WHERE active = false;

-- Delete with RETURN
DELETE person:tobie RETURN BEFORE;

-- Delete with TIMEOUT
DELETE person WHERE last_login < time::now() - 1y TIMEOUT 30s;
```

### UPSERT

Creates a record if it does not exist, or updates it if it does.

```surql
-- Upsert a specific record
UPSERT person:tobie SET
    name = 'Tobie',
    age = 34,
    updated_at = time::now();

-- Upsert with CONTENT
UPSERT person:tobie CONTENT {
    name: 'Tobie',
    age: 34,
    company: 'SurrealDB'
};

-- Upsert with MERGE
UPSERT person:tobie MERGE {
    last_seen: time::now()
};
```

### INSERT

Inserts records, supporting bulk operations and ON DUPLICATE KEY UPDATE.

```surql
-- Insert a single record
INSERT INTO person {
    id: person:tobie,
    name: 'Tobie',
    age: 33
};

-- Bulk insert
INSERT INTO person [
    { name: 'Alice', age: 28 },
    { name: 'Bob', age: 35 },
    { name: 'Charlie', age: 42 }
];

-- Insert with ON DUPLICATE KEY UPDATE (upsert behavior)
INSERT INTO person {
    id: person:tobie,
    name: 'Tobie',
    age: 34
} ON DUPLICATE KEY UPDATE age = $input.age;

-- INSERT IGNORE: skip on conflict instead of error
-- (Silently ignores records that violate unique constraints)
```

### RELATE

Creates graph edges (relationships) between records.

```surql
-- Create a basic relationship
RELATE person:tobie->wrote->article:surreal;

-- Create a relationship with properties (SET syntax)
RELATE person:tobie->bought->product:laptop SET
    quantity = 1,
    price = 1299.99,
    purchased_at = time::now();

-- Create a relationship with CONTENT
RELATE person:alice->follows->person:bob CONTENT {
    since: time::now(),
    notifications: true
};

-- Relate multiple records at once
RELATE person:tobie->knows->[person:alice, person:bob, person:charlie];

-- Relate with a specific edge ID
RELATE person:tobie->wrote->article:surreal SET
    id = wrote:first_article;

-- Return the created edge
RELATE person:tobie->likes->post:123 RETURN AFTER;
```

### DEFINE NAMESPACE

Defines a namespace, the top-level organizational unit.

```surql
DEFINE NAMESPACE myapp;

-- With OVERWRITE
DEFINE NAMESPACE OVERWRITE myapp;

-- With IF NOT EXISTS
DEFINE NAMESPACE IF NOT EXISTS myapp;

-- With COMMENT
DEFINE NAMESPACE myapp COMMENT 'Production namespace';
```

### DEFINE DATABASE

Defines a database within a namespace.

```surql
DEFINE DATABASE mydb;

DEFINE DATABASE OVERWRITE mydb;

DEFINE DATABASE IF NOT EXISTS mydb;

DEFINE DATABASE mydb COMMENT 'Main application database';
```

### DEFINE TABLE

Defines a table with schema enforcement, type, permissions, and other options.

```surql
-- Schemaless table (default: any fields allowed)
DEFINE TABLE article SCHEMALESS;

-- Schemafull table (only defined fields allowed)
DEFINE TABLE person SCHEMAFULL;

-- Table with TYPE NORMAL (standard document table)
DEFINE TABLE person TYPE NORMAL SCHEMAFULL;

-- Table with TYPE ANY (can hold documents and be used as graph edges)
DEFINE TABLE flexible TYPE ANY SCHEMALESS;

-- Table with TYPE RELATION (graph edge table)
DEFINE TABLE wrote TYPE RELATION IN person OUT article;

-- Relation table with ENFORCED (strict in/out types)
DEFINE TABLE purchased TYPE RELATION IN person OUT product ENFORCED;

-- Relation table with FROM/TO syntax (aliases for IN/OUT)
DEFINE TABLE likes TYPE RELATION FROM person TO post;

-- Drop table: deletes records immediately upon write, useful for write-only audit logs
DEFINE TABLE events DROP;

-- Computed table view (auto-updated projection)
DEFINE TABLE person_by_age AS
    SELECT age, count() AS total
    FROM person
    GROUP BY age;

-- Table with changefeed
DEFINE TABLE orders CHANGEFEED 7d;

-- Table with changefeed including original data
DEFINE TABLE orders CHANGEFEED 30d INCLUDE ORIGINAL;

-- Table with permissions
DEFINE TABLE post SCHEMALESS
    PERMISSIONS
        FOR select FULL
        FOR create WHERE $auth.id != NONE
        FOR update WHERE author = $auth.id
        FOR delete WHERE author = $auth.id OR $auth.role = 'admin';

-- Table with COMMENT
DEFINE TABLE person SCHEMAFULL COMMENT 'Stores user profiles';
```

### DEFINE FIELD

Defines a field on a table with type constraints, defaults, assertions, and permissions.

```surql
-- Basic typed field
DEFINE FIELD name ON TABLE person TYPE string;

-- Numeric field
DEFINE FIELD age ON TABLE person TYPE int;

-- Optional field (can be null)
DEFINE FIELD nickname ON TABLE person TYPE option<string>;

-- Field with default value
DEFINE FIELD created_at ON TABLE person TYPE datetime DEFAULT time::now();

-- Field with VALUE (set on every create/update)
DEFINE FIELD updated_at ON TABLE person VALUE time::now();

-- Computed field (read-only, derived from other fields)
DEFINE FIELD full_name ON TABLE person VALUE string::concat(name.first, ' ', name.last);

-- READONLY field (cannot be changed after creation)
DEFINE FIELD created_at ON TABLE person TYPE datetime VALUE time::now() READONLY;

-- Field with ASSERT (validation constraint)
DEFINE FIELD email ON TABLE person TYPE string
    ASSERT string::is_email($value);

-- Field with range assertion
DEFINE FIELD age ON TABLE person TYPE int
    ASSERT $value >= 0 AND $value <= 150;

-- Record link field
DEFINE FIELD author ON TABLE article TYPE record<person>;

-- Array field with inner type
DEFINE FIELD tags ON TABLE article TYPE array<string>;

-- Set field (unique elements)
DEFINE FIELD categories ON TABLE article TYPE set<string>;

-- Nested object field
DEFINE FIELD address ON TABLE person TYPE object;
DEFINE FIELD address.street ON TABLE person TYPE string;
DEFINE FIELD address.city ON TABLE person TYPE string;
DEFINE FIELD address.zip ON TABLE person TYPE string;

-- Array of records
DEFINE FIELD reviewers ON TABLE article TYPE array<record<person>>;

-- Field with FLEXIBLE type (accepts any type, stores as-is)
DEFINE FIELD metadata ON TABLE article FLEXIBLE TYPE object;

-- Field with permissions
DEFINE FIELD email ON TABLE person TYPE string
    PERMISSIONS
        FOR select WHERE $auth.id = id OR $auth.role = 'admin'
        FOR update WHERE $auth.id = id;

-- Overwrite existing field definition
DEFINE FIELD OVERWRITE name ON TABLE person TYPE string;

-- IF NOT EXISTS
DEFINE FIELD IF NOT EXISTS name ON TABLE person TYPE string;

-- Geometry field
DEFINE FIELD location ON TABLE place TYPE geometry<point>;

-- Vector embedding field
DEFINE FIELD embedding ON TABLE document TYPE array<float> DEFAULT [];

-- Duration field
DEFINE FIELD duration ON TABLE event TYPE duration;

-- Decimal field (precise numeric)
DEFINE FIELD price ON TABLE product TYPE decimal;

-- Bytes field
DEFINE FIELD payload ON TABLE message TYPE bytes;

-- UUID field
DEFINE FIELD session_id ON TABLE session TYPE uuid;

-- Enum-like pattern using ASSERT
DEFINE FIELD status ON TABLE order TYPE string
    ASSERT $value IN ['pending', 'processing', 'shipped', 'delivered', 'cancelled'];
```

### DEFINE INDEX

Creates indexes for query optimization, uniqueness, full-text search, and vector similarity search.

```surql
-- Standard index
DEFINE INDEX age_idx ON TABLE person COLUMNS age;

-- Unique index
DEFINE INDEX email_idx ON TABLE person COLUMNS email UNIQUE;

-- Composite index
DEFINE INDEX name_age_idx ON TABLE person COLUMNS name, age;

-- Full-text search index with analyzer
DEFINE INDEX content_search ON TABLE article COLUMNS content
    FULLTEXT ANALYZER ascii BM25;

-- Full-text search with BM25 tuning
DEFINE INDEX content_search ON TABLE article COLUMNS content
    FULLTEXT ANALYZER ascii BM25(1.2, 0.75);

-- Full-text search with highlights enabled
DEFINE INDEX content_search ON TABLE article COLUMNS content
    FULLTEXT ANALYZER ascii BM25 HIGHLIGHTS;

-- HNSW vector index (for approximate nearest neighbor search)
DEFINE INDEX embedding_idx ON TABLE document FIELDS embedding
    HNSW DIMENSION 1536 DIST COSINE;

-- HNSW with tuning parameters
DEFINE INDEX embedding_idx ON TABLE document FIELDS embedding
    HNSW DIMENSION 3072
    DIST COSINE
    TYPE F32
    EFC 150
    M 12;

-- HNSW is the only documented vector index type in SurrealDB v3.
-- (The MTREE index keyword that earlier rule revisions documented
-- does not exist in the current upstream `DEFINE INDEX` grammar;
-- see https://surrealdb.com/docs/surrealql/statements/define/indexes.)
-- For brute-force kNN without an index, use the `<|K,METRIC|>`
-- operator (e.g. `vector <|2,EUCLIDEAN|> $query`).

-- Overwrite existing index
DEFINE INDEX OVERWRITE email_idx ON TABLE person COLUMNS email UNIQUE;

-- Idempotent definition — does nothing if the index already exists.
DEFINE INDEX IF NOT EXISTS email_idx ON TABLE person COLUMNS email UNIQUE;

-- CONCURRENTLY — build the index in the background without blocking
-- writes. Recommended for large indexes (HNSW, FULLTEXT) in
-- production. Monitor progress via INFO FOR INDEX (see rules/
-- performance.md §"Concurrent Index Builds").
DEFINE INDEX idx_embedding ON TABLE document
    FIELDS embedding HNSW DIMENSION 1536 DIST COSINE
    CONCURRENTLY;

-- Rebuild an index
REBUILD INDEX email_idx ON TABLE person;

-- Rebuild all indexes on a table
REBUILD INDEX ON TABLE person;
```

**HNSW distance metrics**: `COSINE`, `EUCLIDEAN`, `MANHATTAN`, `CHEBYSHEV`, `HAMMING`, `JACCARD`, `MINKOWSKI`, `PEARSON`.

**HNSW parameters**:
- `DIMENSION` -- Number of dimensions in the vector (required)
- `DIST` -- Distance metric (default: `EUCLIDEAN` — see
  `surrealdb/core/src/sql/statements/define/index.rs`, where the
  parser initialises `let mut distance = Distance::Euclidean;` and
  `Distance` derives `#[default]` on `Euclidean`. For text
  embeddings normalised to unit length, override to `DIST COSINE`
  explicitly.)
- `TYPE` -- Element type: `F32`, `F64`, `I16`, `I32`, `I64` (default: `F32`)
- `EFC` -- Size of dynamic candidate list during construction (default: 150)
- `M` -- Max number of connections per node per layer (default: 12)

### DEFINE ACCESS

Defines authentication and authorization access methods.

```surql
-- Record-based access (signup/signin for end users)
DEFINE ACCESS account ON DATABASE TYPE RECORD
    SIGNUP ( CREATE user SET email = $email, pass = crypto::argon2::generate($pass) )
    SIGNIN ( SELECT * FROM user WHERE email = $email AND crypto::argon2::compare(pass, $pass) )
    DURATION FOR TOKEN 15m, FOR SESSION 12h;

-- JWT access (external identity provider).
-- `TYPE JWT` accepts BOTH `DURATION FOR TOKEN` and `DURATION FOR
-- SESSION` (verified against parser tests stmt.rs:560/764/825).
-- Semantics depend on issuer-key presence: with `WITH ISSUER KEY`,
-- SurrealDB issues tokens and FOR TOKEN controls their lifetime;
-- for verification-only JWT (no issuer), the parser accepts FOR
-- TOKEN but the external issuer's `exp` claim is authoritative.
-- See rules/security.md §"JWT-Based Authentication" for the full
-- callout. Symmetric algorithms (HS256/HS384/HS512) auto-populate
-- the issuer with the same key — they are NOT verification-only.
DEFINE ACCESS token_auth ON DATABASE TYPE JWT
    ALGORITHM HS256 KEY 'your-secret-key-here'
    DURATION FOR TOKEN 1h, FOR SESSION 12h;

-- JWT with JWKS URL (for OAuth/OIDC providers)
DEFINE ACCESS oauth ON DATABASE TYPE JWT
    URL 'https://auth.example.com/.well-known/jwks.json'
    DURATION FOR SESSION 24h;

-- WITH ISSUER KEY is valid on BOTH standalone `TYPE JWT` and inside
-- a RECORD-access `WITH JWT` block (verified against parser test
-- stmt.rs:466 — `TYPE JWT ALGORITHM EDDSA KEY "foo" WITH ISSUER KEY
-- "bar"` parses to `JwtAccessIssue { alg: EdDSA, key: "bar" }`).
-- The actual upstream constraint is that the issuer algorithm must
-- match the verification algorithm (per stmt.rs:619 unwrap_err()),
-- not that the clause is scope-restricted. The example below shows
-- the RECORD-WITH-JWT pattern; the same `WITH ISSUER KEY` clause
-- also composes with standalone `TYPE JWT` definitions.
DEFINE ACCESS account ON DATABASE TYPE RECORD
    SIGNUP ( CREATE user SET email = $email, pass = crypto::argon2::generate($pass) )
    SIGNIN ( SELECT * FROM user WHERE email = $email AND crypto::argon2::compare(pass, $pass) )
    WITH JWT ALGORITHM RS256 KEY '-----BEGIN PUBLIC KEY-----...'
    WITH ISSUER KEY '-----BEGIN PRIVATE KEY-----...';

-- Overwrite and IF NOT EXISTS
DEFINE ACCESS OVERWRITE account ON DATABASE TYPE RECORD
    SIGNUP ( CREATE user SET email = $email, pass = crypto::argon2::generate($pass) )
    SIGNIN ( SELECT * FROM user WHERE email = $email AND crypto::argon2::compare(pass, $pass) );

DEFINE ACCESS IF NOT EXISTS account ON DATABASE TYPE RECORD
    SIGNUP ( CREATE user SET email = $email, pass = crypto::argon2::generate($pass) )
    SIGNIN ( SELECT * FROM user WHERE email = $email AND crypto::argon2::compare(pass, $pass) );

-- Bearer-token access (API keys, service-to-service tokens, refresh
-- tokens). TYPE BEARER issues opaque tokens via the ACCESS ... GRANT
-- statement and binds each token to either a USER (system user) or
-- a RECORD (e.g. one record per integration partner).
DEFINE ACCESS service_tokens ON DATABASE TYPE BEARER FOR USER
    DURATION FOR GRANT 30d, FOR TOKEN 1h, FOR SESSION 12h;

DEFINE ACCESS partner_tokens ON DATABASE TYPE BEARER FOR RECORD
    AUTHENTICATE {
        IF $auth.id THEN RETURN $auth ELSE THROW "no auth record" END
    }
    DURATION FOR GRANT 90d, FOR TOKEN 1h, FOR SESSION 24h;

-- Issue a bearer token under the access method (note the unquoted
-- user identifier — `FOR USER` takes an identifier, not a string).
ACCESS service_tokens GRANT FOR USER ci_runner;
```

`TYPE BEARER` accepts `DURATION FOR GRANT` (how long the issued
token remains usable), `DURATION FOR TOKEN`, and `DURATION FOR
SESSION`. It accepts `FOR USER` to bind the token to a system user
or `FOR RECORD` to bind it to a specific record (the latter
optionally accepts an `AUTHENTICATE` clause to validate the record
on each use — verified against the upstream `TYPE BEARER FOR [USER
| RECORD] [AUTHENTICATE @expression]` grammar; AUTHENTICATE is not
required, e.g. `DEFINE ACCESS api ON DATABASE TYPE BEARER FOR
RECORD DURATION FOR GRANT 10d;` is valid on its own).

### DEFINE ANALYZER

Defines text analyzers for full-text search indexes.

```surql
-- Basic analyzer with tokenizer and filters
DEFINE ANALYZER ascii TOKENIZERS blank, class FILTERS ascii, lowercase;

-- Snowball stemming analyzer for English
DEFINE ANALYZER english TOKENIZERS blank, class FILTERS ascii, snowball(english);

-- N-gram analyzer for autocomplete
DEFINE ANALYZER autocomplete TOKENIZERS blank FILTERS lowercase, ngram(2, 10);

-- Edge N-gram analyzer (prefix matching)
DEFINE ANALYZER prefix_search TOKENIZERS blank FILTERS lowercase, edgengram(1, 15);

-- Camel case tokenizer (splits camelCase words)
DEFINE ANALYZER code_search TOKENIZERS camel, blank FILTERS lowercase;

-- Custom multilingual analyzer
DEFINE ANALYZER multilingual TOKENIZERS blank, class FILTERS lowercase;
```

**Tokenizers**: `blank` (whitespace), `class` (character class boundaries), `camel` (camelCase split), `punct` (punctuation).

**Filters**: `ascii` (ASCII folding), `lowercase`, `uppercase`, `snowball(language)` (stemming), `ngram(min, max)`, `edgengram(min, max)`.

### DEFINE EVENT

Defines table events that trigger on record changes.

```surql
-- Event that fires on creation
DEFINE EVENT new_user ON TABLE user WHEN $event = "CREATE" THEN {
    CREATE log SET
        action = 'user_created',
        user = $after.id,
        timestamp = time::now();
};

-- Event that fires on update
DEFINE EVENT profile_change ON TABLE user WHEN $event = "UPDATE" THEN {
    CREATE audit_log SET
        table = 'user',
        record = $after.id,
        before = $before,
        after = $after,
        changed_at = time::now();
};

-- Event that fires on delete
DEFINE EVENT user_deleted ON TABLE user WHEN $event = "DELETE" THEN {
    -- Clean up related data
    DELETE session WHERE user = $before.id;
};

-- Event with conditional trigger
DEFINE EVENT stock_alert ON TABLE product
    WHEN $event = "UPDATE" AND $after.stock < 10
    THEN {
        CREATE notification SET
            type = 'low_stock',
            product = $after.id,
            stock = $after.stock;
    };

-- Event that sends HTTP webhook
DEFINE EVENT webhook ON TABLE order WHEN $event = "CREATE" THEN {
    http::post('https://hooks.example.com/orders', {
        order_id: $after.id,
        total: $after.total
    });
};
```

**Event variables**: `$event` (CREATE, UPDATE, DELETE), `$before` (record state before change), `$after` (record state after change).

### DEFINE FUNCTION

Defines reusable custom functions.

```surql
-- Simple function
DEFINE FUNCTION fn::greet($name: string) {
    RETURN string::concat('Hello, ', $name, '!');
};

-- Function with multiple parameters and return type
DEFINE FUNCTION fn::calculate_tax($amount: decimal, $rate: decimal) {
    RETURN $amount * $rate;
};

-- Function that queries the database
DEFINE FUNCTION fn::get_user_orders($user_id: record<person>) {
    RETURN SELECT * FROM order WHERE customer = $user_id ORDER BY created_at DESC;
};

-- Function with complex logic
DEFINE FUNCTION fn::full_name($person: record<person>) {
    LET $p = (SELECT name FROM ONLY $person);
    RETURN string::concat($p.name.first, ' ', $p.name.last);
};

-- Recursive-capable function
DEFINE FUNCTION fn::factorial($n: int) {
    IF $n <= 1 {
        RETURN 1;
    };
    RETURN $n * fn::factorial($n - 1);
};

-- Overwrite existing function
DEFINE FUNCTION OVERWRITE fn::greet($name: string) {
    RETURN string::concat('Hi, ', $name, '!');
};
```

### DEFINE MODULE

Defines WASM (WebAssembly) extension modules. New in SurrealDB v3. Allows extending SurrealDB with custom logic compiled to WASM.

```surql
-- Define a WASM module from a file
DEFINE MODULE my_module;

-- Modules provide custom functions that become available
-- as module::function_name() after loading
```

### DEFINE BUCKET

Defines file/object storage buckets. New in SurrealDB v3. Provides built-in file storage capabilities within SurrealDB.

```surql
-- Define a file storage bucket
DEFINE BUCKET images;

-- Define a bucket with configuration
DEFINE BUCKET documents COMMENT 'Document storage for user uploads';
```

### DEFINE USER

Defines system users with scoped access.

```surql
-- Root-level user (full system access)
DEFINE USER root_admin ON ROOT PASSWORD 'strong-password-here' ROLES OWNER;

-- Namespace-level user
DEFINE USER ns_admin ON NAMESPACE PASSWORD 'ns-password' ROLES OWNER;

-- Database-level user
DEFINE USER db_editor ON DATABASE PASSWORD 'db-password' ROLES EDITOR;

-- Database viewer
DEFINE USER db_viewer ON DATABASE PASSWORD 'viewer-password' ROLES VIEWER;

-- User with password hash (pre-hashed)
DEFINE USER admin ON ROOT PASSHASH '$argon2id$...' ROLES OWNER;

-- User with COMMENT
DEFINE USER admin ON DATABASE PASSWORD 'secret' ROLES OWNER
    COMMENT 'Primary database administrator';
```

**Roles**: `OWNER` (full access), `EDITOR` (read/write), `VIEWER` (read-only).

### DEFINE PARAM

Defines global parameters accessible across queries.

```surql
-- Define a parameter
DEFINE PARAM $app_name VALUE 'My Application';

-- Define a numeric parameter
DEFINE PARAM $max_results VALUE 100;

-- Define an object parameter
DEFINE PARAM $config VALUE {
    theme: 'dark',
    lang: 'en',
    version: 3
};

-- Use a defined parameter in queries
SELECT * FROM person LIMIT $max_results;
```

### DEFINE SEQUENCE

Defines an auto-incrementing sequence for generating sequential numeric IDs.

```surql
-- Define a sequence with defaults
DEFINE SEQUENCE order_seq;

-- Define with custom start and batch size
DEFINE SEQUENCE invoice_seq START 1000 BATCH 50;

-- Use OVERWRITE to redefine
DEFINE SEQUENCE OVERWRITE order_seq START 1 BATCH 100;

-- Use IF NOT EXISTS
DEFINE SEQUENCE IF NOT EXISTS order_seq;
```

Syntax: `DEFINE SEQUENCE [ OVERWRITE | IF NOT EXISTS ] @name [ BATCH @batch ] [ START @start ]`

### USE

Switches the active namespace and/or database.

```surql
-- Switch namespace
USE NS myapp;

-- Switch database
USE DB production;

-- Switch both
USE NS myapp DB production;
```

### INFO FOR

Returns schema information about the system, namespace, database, or table.

```surql
-- System-level info
INFO FOR ROOT;

-- Namespace-level info
INFO FOR NAMESPACE;
-- or
INFO FOR NS;

-- Database-level info
INFO FOR DATABASE;
-- or
INFO FOR DB;

-- Table-level info
INFO FOR TABLE person;
-- or
INFO FOR TABLE person STRUCTURE;
```

### LET

Binds values to variables for use in subsequent statements.

```surql
-- Bind a simple value
LET $name = 'Tobie';

-- Bind a query result
LET $adults = (SELECT * FROM person WHERE age >= 18);

-- Bind a computed value
LET $now = time::now();

-- Use variables in subsequent queries
LET $user = (CREATE person SET name = $name);
RELATE $user->wrote->article:first;
```

### BEGIN / COMMIT / CANCEL (Transactions)

Groups multiple statements into atomic transactions.

```surql
-- Basic transaction
BEGIN TRANSACTION;
    CREATE account:alice SET balance = 1000;
    CREATE account:bob SET balance = 500;
COMMIT TRANSACTION;

-- Transaction with transfer logic
BEGIN TRANSACTION;
    UPDATE account:alice SET balance -= 100;
    UPDATE account:bob SET balance += 100;
    CREATE transfer SET
        from = account:alice,
        to = account:bob,
        amount = 100,
        timestamp = time::now();
COMMIT TRANSACTION;

-- Cancel a transaction (rollback)
BEGIN TRANSACTION;
    UPDATE account:alice SET balance -= 10000;
    -- Oops, insufficient funds -- rollback
CANCEL TRANSACTION;
```

### RETURN

Returns a value from a block or function.

```surql
-- Return from a block
{
    LET $x = 10;
    LET $y = 20;
    RETURN $x + $y;
};

-- Return in function context
DEFINE FUNCTION fn::add($a: int, $b: int) {
    RETURN $a + $b;
};
```

### THROW

Throws a custom error, halting execution.

```surql
-- Throw a string error
THROW 'Something went wrong';

-- Throw conditionally
IF $balance < 0 {
    THROW 'Insufficient funds';
};

-- Throw with dynamic message
THROW string::concat('User ', $id, ' not found');
```

### SLEEP

Pauses execution for a specified duration. Primarily useful for testing.

```surql
SLEEP 1s;
SLEEP 500ms;
SLEEP 2m;
```

### IF / ELSE

Conditional branching.

```surql
-- Basic if/else
IF $age >= 18 {
    RETURN 'adult';
} ELSE {
    RETURN 'minor';
};

-- If/else if/else
IF $score >= 90 {
    RETURN 'A';
} ELSE IF $score >= 80 {
    RETURN 'B';
} ELSE IF $score >= 70 {
    RETURN 'C';
} ELSE {
    RETURN 'F';
};

-- If as an expression (inline)
LET $label = IF $active { 'Active' } ELSE { 'Inactive' };

-- If in UPDATE
UPDATE person SET status = IF age >= 18 { 'adult' } ELSE { 'minor' };
```

### FOR

Iterates over arrays or query results.

```surql
-- Iterate over an array
FOR $name IN ['Alice', 'Bob', 'Charlie'] {
    CREATE person SET name = $name;
};

-- Iterate over query results
FOR $user IN (SELECT * FROM person WHERE active = true) {
    UPDATE $user.id SET last_check = time::now();
};

-- Nested loops
FOR $i IN [1, 2, 3] {
    FOR $j IN ['a', 'b'] {
        CREATE item SET num = $i, letter = $j;
    };
};
```

### BREAK / CONTINUE

Controls loop execution flow.

```surql
-- Break out of a loop
FOR $item IN (SELECT * FROM product ORDER BY price ASC) {
    IF $item.price > 100 {
        BREAK;
    };
    UPDATE $item.id SET featured = true;
};

-- Skip iteration with CONTINUE
FOR $user IN (SELECT * FROM person) {
    IF $user.role = 'bot' {
        CONTINUE;
    };
    CREATE notification SET user = $user.id, message = 'System update';
};
```

### REMOVE

Removes schema definitions and data.

```surql
-- Remove a table and all its data
REMOVE TABLE person;

-- Remove a field definition
REMOVE FIELD email ON TABLE person;

-- Remove an index
REMOVE INDEX email_idx ON TABLE person;

-- Remove a namespace
REMOVE NAMESPACE myapp;

-- Remove a database
REMOVE DATABASE mydb;

-- Remove an event
REMOVE EVENT new_user ON TABLE user;

-- Remove a function
REMOVE FUNCTION fn::greet;

-- Remove a param
REMOVE PARAM $max_results;

-- Remove an analyzer
REMOVE ANALYZER english;

-- Remove an access method
REMOVE ACCESS account ON DATABASE;

-- Remove a user
REMOVE USER admin ON DATABASE;

-- Remove a module
REMOVE MODULE my_module;

-- Remove a bucket
REMOVE BUCKET images;
```

### ALTER

Modifies an existing schema object in-place.

**SurrealDB v3.1.0+** extends `ALTER` to every `DEFINE` counterpart:
`EVENT`, `PARAM`, `BUCKET`, `ANALYZER`, `FUNCTION`, `USER`, `ACCESS`,
`CONFIG`, and `API`, in addition to the seven targets available since v3.0.5
(verified against `core/src/syn/parser/stmt/alter.rs` at v3.0.5):
`ALTER SYSTEM`, `ALTER NAMESPACE`, `ALTER DATABASE`, `ALTER TABLE`,
`ALTER INDEX`, `ALTER FIELD`, `ALTER SEQUENCE`.

> **v3.0.5 boundary (still relevant on older servers).** On v3.0.5 only,
> `ALTER EVENT`, `ALTER PARAM`, `ALTER BUCKET`, `ALTER ANALYZER`,
> `ALTER FUNCTION`, `ALTER USER`, `ALTER ACCESS`, `ALTER CONFIG`, and
> `ALTER API` do **not** parse. Use `REMOVE` + `DEFINE` on 3.0.x, or upgrade
> to **v3.1.4+** for full ALTER coverage.

v3.1 ALTER constraints (from [Release 3.1](https://surrealdb.com/releases/3.1)):

- `ALTER PARAM` does not support `DROP VALUE` (a param without a value is meaningless).
- `ALTER EVENT` uses `DROP ASYNC` to revert to synchronous mode.
- `ALTER ACCESS` does not allow changing the access type (record / JWT / bearer).
- Resource names and table targets accept bound parameters, matching `DEFINE` / `REMOVE`.

```surql
-- v3.1+ examples (require SurrealDB 3.1.0+)
ALTER EVENT notify_user ON TABLE person DROP ASYNC;
ALTER PARAM app_version SET VALUE '2.0.0';
ALTER ACCESS user_auth SET DURATION FOR TOKEN 1h;
ALTER CONFIG GRAPHQL SET TABLES AUTO;
REMOVE CONFIG IF EXISTS GRAPHQL;

-- value::expect (v3.1.0+) — assert in method chains
SELECT value::expect($value, |$v| $v > 0, 'must be positive') FROM data;
```

Use `ALTER` when you need to change an attribute of an existing
definition without losing the object's history or dropping
dependent objects (which a `REMOVE` + `DEFINE` cycle would do).

```surql
-- ALTER SYSTEM — set or drop the global query timeout, run a global
-- compaction.
ALTER SYSTEM COMPACT;
ALTER SYSTEM QUERY_TIMEOUT 30s;
ALTER SYSTEM DROP QUERY_TIMEOUT;

-- ALTER NAMESPACE / ALTER DATABASE — primarily for COMPACT.
ALTER NAMESPACE COMPACT;
ALTER DATABASE COMPACT;

-- ALTER TABLE — change an existing table's attributes without
-- dropping the table or its data. Supports COMPACT, SET/DROP
-- COMMENT, SET/DROP CHANGEFEED, schema-mode toggle (SCHEMAFULL /
-- SCHEMALESS), TYPE switch (NORMAL / RELATION / ANY), and
-- PERMISSIONS rewriting.
ALTER TABLE person COMPACT;
ALTER TABLE person COMMENT 'User accounts';
ALTER TABLE person DROP COMMENT;
ALTER TABLE person CHANGEFEED 7d;
ALTER TABLE person DROP CHANGEFEED;
ALTER TABLE person SCHEMAFULL;
ALTER TABLE wrote TYPE RELATION FROM person TO article;
ALTER TABLE person PERMISSIONS FOR select WHERE id = $auth.id;

-- ALTER INDEX — supports IF EXISTS, PREPARE REMOVE (decommission an
-- index before removal), COMMENT '…' / DROP COMMENT. There is NO
-- COMPACT clause on ALTER INDEX in v3.0.5 (verified against
-- core/src/syn/parser/stmt/alter.rs lines 311-347 and the
-- AlterIndexStatement struct in core/src/sql/statements/alter/
-- index.rs — the struct carries `prepare_remove: bool` and
-- `comment: AlterKind<String>`, no `compact` field).
ALTER INDEX email_idx ON TABLE person PREPARE REMOVE;
ALTER INDEX email_idx ON TABLE person COMMENT 'Lookup by email';
ALTER INDEX email_idx ON TABLE person DROP COMMENT;
ALTER INDEX IF EXISTS optional_idx ON TABLE person PREPARE REMOVE;

-- ALTER FIELD — change an existing field's DEFAULT, ASSERT,
-- VALUE, READONLY, or PERMISSIONS without dropping the field.
ALTER FIELD email ON TABLE person DEFAULT 'unknown@example.com';
ALTER FIELD age ON TABLE person ASSERT $value >= 0;

-- ALTER SEQUENCE — change the sequence TIMEOUT (or clear it with
-- TIMEOUT NONE). There is NO RESTART clause on ALTER SEQUENCE in
-- v3.0.5 (verified against core/src/syn/parser/stmt/alter.rs lines
-- 1220-1243 and AlterSequenceStatement which carries only `name`,
-- `if_exists`, `timeout`).
ALTER SEQUENCE order_no TIMEOUT 5s;
ALTER SEQUENCE order_no TIMEOUT NONE;
ALTER SEQUENCE IF EXISTS optional_seq TIMEOUT 30s;
```

### REBUILD INDEX

Rebuilds indexes, useful after bulk data operations.

```surql
-- Rebuild a specific index
REBUILD INDEX email_idx ON TABLE person;

-- Rebuild all indexes on a table
REBUILD INDEX ON TABLE person;
```

### LIVE SELECT

Creates real-time subscriptions that push changes as they happen.

```surql
-- Live query on an entire table
LIVE SELECT * FROM person;

-- Live query with filtering
LIVE SELECT * FROM person WHERE age > 18;

-- Live query with DIFF (returns only changed fields)
LIVE SELECT DIFF FROM person;

-- Live query on specific fields
LIVE SELECT name, email FROM person;

-- Live query on a specific record
LIVE SELECT * FROM person:tobie;
```

Live queries return a UUID that can be used to cancel the subscription with `KILL`.

### KILL

Cancels an active live query.

```surql
-- Kill a live query by its UUID
KILL '1a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d';

-- Typically used with the UUID returned by LIVE SELECT
LET $live_id = (LIVE SELECT * FROM person);
-- ... later ...
KILL $live_id;
```

### SHOW CHANGES FOR TABLE

Retrieves the change feed for a table (requires CHANGEFEED to be enabled on the table).

```surql
-- Show all changes since a timestamp
SHOW CHANGES FOR TABLE orders SINCE '2026-01-01T00:00:00Z';

-- Show limited changes
SHOW CHANGES FOR TABLE orders SINCE '2026-01-01T00:00:00Z' LIMIT 100;
```

### VERSION Clause (Time-Travel Queries)

When running on the SurrealKV storage engine, you can query historical data at a specific point in time.

```surql
-- Query data as it existed at a specific time
SELECT * FROM person VERSION d'2026-01-15T12:00:00Z';

-- Time-travel with filtering
SELECT * FROM person WHERE active = true VERSION d'2025-12-01T00:00:00Z';
```

---

## Data Types

### Primitive Types

| Type | Description | Example |
|------|-------------|---------|
| `string` | UTF-8 text | `'hello'`, `"world"` |
| `int` | 64-bit signed integer | `42`, `-7` |
| `float` | 64-bit IEEE 754 floating point | `3.14`, `-0.5` |
| `decimal` | Arbitrary-precision decimal | `19.99dec`, `<decimal> 19.99` |
| `bool` | Boolean | `true`, `false` |
| `datetime` | ISO 8601 date and time | `d'2026-02-19T10:30:00Z'` |
| `duration` | Time duration | `1h30m`, `7d`, `500ms` |
| `bytes` | Binary data | `<bytes> "base64data"` |
| `uuid` | UUID value | `u'550e8400-e29b-41d4-a716-446655440000'` |
| `null` | Explicit null value | `null` |
| `none` | Absence of a value | `NONE` |
| `any` | Any type (no constraint) | -- |

### Complex Types

| Type | Description | Example |
|------|-------------|---------|
| `object` | Key-value map | `{ name: 'Tobie', age: 33 }` |
| `array` | Ordered list | `[1, 2, 3]` |
| `array<T>` | Typed array | `array<string>`, `array<int>` |
| `set` | Unique ordered list | -- |
| `set<T>` | Typed unique set | `set<string>` |
| `option<T>` | Nullable typed field | `option<string>` |
| `record` | Record link (any table) | `person:tobie` |
| `record<T>` | Record link (specific table) | `record<person>` |

### Geometry Types

| Type | Description |
|------|-------------|
| `geometry<point>` | GeoJSON Point |
| `geometry<line>` | GeoJSON LineString |
| `geometry<polygon>` | GeoJSON Polygon |
| `geometry<multipoint>` | GeoJSON MultiPoint |
| `geometry<multiline>` | GeoJSON MultiLineString |
| `geometry<multipolygon>` | GeoJSON MultiPolygon |
| `geometry<collection>` | GeoJSON GeometryCollection |

```surql
-- Geometry point (longitude, latitude)
CREATE place SET location = (-73.935242, 40.730610);

-- GeoJSON format
CREATE place SET location = {
    type: 'Point',
    coordinates: [-73.935242, 40.730610]
};

-- Polygon
CREATE zone SET area = {
    type: 'Polygon',
    coordinates: [[
        [-73.98, 40.75],
        [-73.97, 40.75],
        [-73.97, 40.76],
        [-73.98, 40.76],
        [-73.98, 40.75]
    ]]
};
```

### Record IDs

Record IDs are first-class citizens in SurrealDB, uniquely identifying every record.

```surql
-- String-based ID
person:tobie

-- Integer-based ID
person:100

-- UUID-based ID (auto-generated)
person:uuid()

-- ULID-based ID (time-sortable, auto-generated)
person:ulid()

-- Random ID
person:rand()

-- Complex/compound ID (using arrays or objects)
temperature:['London', d'2026-02-19T10:00:00Z']
city:[36.775, -122.4194]

-- Object-based compound ID
person:{ first: 'Tobie', last: 'Morgan' }
```

### Duration Literals

```surql
-- Duration components
1ns    -- nanoseconds
1us    -- microseconds
1ms    -- milliseconds
1s     -- seconds
1m     -- minutes
1h     -- hours
1d     -- days
1w     -- weeks
1y     -- years

-- Compound durations
1h30m
2d12h
1y6m3d
```

### Casting

Explicit type conversion using angle bracket syntax.

```surql
-- Cast to int
<int> '42'
<int> 3.14

-- Cast to float
<float> 42
<float> '3.14'

-- Cast to string
<string> 42
<string> true

-- Cast to bool
<bool> 'true'
<bool> 1

-- Cast to datetime
<datetime> '2026-02-19T10:00:00Z'

-- Cast to decimal
<decimal> 19.99
<decimal> '19.99'

-- Cast to duration
<duration> '1h30m'

-- Cast to record
<record> 'person:tobie'
```

---

## Operators

### Arithmetic Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `+` | Addition | `1 + 2` returns `3` |
| `-` | Subtraction | `5 - 3` returns `2` |
| `*` | Multiplication | `4 * 3` returns `12` |
| `/` | Division | `10 / 3` returns `3` |
| `**` | Exponentiation | `2 ** 8` returns `256` |
| `%` | Modulo | `10 % 3` returns `1` |

### Comparison Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Equals (loosely) | `1 = 1` |
| `!=` | Not equals | `1 != 2` |
| `==` | Exact equals (strict type) | `1 == 1` |
| `?=` | Any equals (for arrays) | `[1,2,3] ?= 2` |
| `*=` | All equals (for arrays) | `[1,1,1] *= 1` |
| `~` | Fuzzy match | `'hello' ~ 'helo'` |
| `!~` | Not fuzzy match | `'hello' !~ 'world'` |
| `?~` | Any fuzzy match | -- |
| `*~` | All fuzzy match | -- |
| `<` | Less than | `1 < 2` |
| `>` | Greater than | `2 > 1` |
| `<=` | Less than or equal | `1 <= 1` |
| `>=` | Greater than or equal | `2 >= 2` |

### Logical Operators

| Operator | Description |
|----------|-------------|
| `AND` / `&&` | Logical AND |
| `OR` / `\|\|` | Logical OR |
| `NOT` / `!` | Logical NOT |
| `!!` | Truthiness coercion (double-not) |

### Containment Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `CONTAINS` | Value contains | `[1,2,3] CONTAINS 2` |
| `CONTAINSNOT` | Value does not contain | `[1,2,3] CONTAINSNOT 4` |
| `CONTAINSALL` | Contains all values | `[1,2,3] CONTAINSALL [1,2]` |
| `CONTAINSANY` | Contains any value | `[1,2,3] CONTAINSANY [2,4]` |
| `CONTAINSNONE` | Contains none of | `[1,2,3] CONTAINSNONE [4,5]` |

### Membership Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `IN` | Value is in | `2 IN [1,2,3]` |
| `NOT IN` | Value is not in | `4 NOT IN [1,2,3]` |
| `INSIDE` | Same as IN | `2 INSIDE [1,2,3]` |
| `NOTINSIDE` | Same as NOT IN | `4 NOTINSIDE [1,2,3]` |
| `ALLINSIDE` | All values are in | `[1,2] ALLINSIDE [1,2,3]` |
| `ANYINSIDE` | Any value is in | `[2,4] ANYINSIDE [1,2,3]` |
| `NONEINSIDE` | None of the values are in | `[4,5] NONEINSIDE [1,2,3]` |

### Pattern Matching

Fuzzy matching uses the `~`, `!~`, `?~`, and `*~` operators documented
in the [Comparison Operators](#comparison-operators) table above.
Full-text search uses the `@@` / `@N@` `MATCHES` operators documented
in the [Search Functions](#search-functions) section. KNN vector
search uses the `<|K|>` / `<|K,DIST|>` / `<|K,EF|>` operators
documented in the [Vector Functions](#vector-functions) and `DEFINE
INDEX HNSW` sections. There is no separate "LIKE" operator in v3 —
that pre-v2 keyword was removed.

### Geometry Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `OUTSIDE` | Geometry containment check (left is outside right) | `point OUTSIDE polygon` |
| `INTERSECTS` | Geometry intersection check | `polygon_a INTERSECTS polygon_b` |

### Other Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `??` | Null coalescing | `$val ?? 'default'` |
| `?:` | Ternary | `$active ? 'yes' : 'no'` |
| `..` | Range | `1..10` |

---

## Functions

### String Functions

```surql
string::concat('hello', ' ', 'world')       -- 'hello world'
string::contains('SurrealDB', 'real')        -- true
string::starts_with('SurrealDB', 'Surreal')  -- true
string::ends_with('SurrealDB', 'DB')         -- true
string::len('hello')                         -- 5
string::lowercase('HELLO')                   -- 'hello'
string::uppercase('hello')                   -- 'HELLO'
string::trim('  hello  ')                    -- 'hello'
string::split('a,b,c', ',')                 -- ['a', 'b', 'c']
string::join(', ', 'a', 'b', 'c')           -- 'a, b, c'
string::slug('Hello World!')                 -- 'hello-world'
string::replace('hello world', 'world', 'DB') -- 'hello DB'
string::reverse('hello')                     -- 'olleh'
string::repeat('ab', 3)                      -- 'ababab'
string::slice('SurrealDB', 0, 7)             -- 'Surreal'

-- Validation functions
string::is_alphanum('abc123')               -- true
string::is_alpha('abc')                     -- true
string::is_ascii('hello')                   -- true
string::is_datetime('2026-01-01T00:00:00Z') -- true
string::is_domain('surrealdb.com')          -- true
string::is_email('tobie@surrealdb.com')     -- true
string::is_hexadecimal('ff00ab')            -- true
string::is_ip('192.168.1.1')               -- true
string::is_ipv4('192.168.1.1')             -- true
string::is_ipv6('::1')                      -- true
string::is_latitude('51.5074')              -- true
string::is_longitude('-0.1278')             -- true
string::is_numeric('12345')                 -- true
string::is_semver('1.2.3')                  -- true
string::is_url('https://surrealdb.com')     -- true
string::is_uuid('550e8400-e29b-41d4-a716-446655440000') -- true

-- Method syntax (on string values)
'hello world'.uppercase()                    -- 'HELLO WORLD'
'a,b,c'.split(',')                           -- ['a', 'b', 'c']
```

### Array Functions

```surql
array::add([1, 2], 3)                       -- [1, 2, 3] (no duplicates)
array::all([true, true, true])               -- true
array::any([false, true, false])             -- true
array::append([1, 2], 3)                     -- [1, 2, 3]
array::at([1, 2, 3], 1)                      -- 2
array::boolean_and([true, false], [true, true]) -- [true, false]
array::boolean_or([true, false], [false, true]) -- [true, true]
array::boolean_not([true, false])            -- [false, true]
array::boolean_xor([true, false], [false, true]) -- [true, true]
array::combine([1, 2], [3, 4])              -- [[1,3],[1,4],[2,3],[2,4]]
array::complement([1,2,3,4], [2,4])          -- [1, 3]    (relative complement: A \ B)
array::concat([1, 2], [3, 4])               -- [1, 2, 3, 4]
array::clump([1,2,3,4,5], 2)                -- [[1,2],[3,4],[5]]
-- array::difference is the SYMMETRIC difference (A △ B) with multiset
-- pairing: equal elements pair off and are dropped, unmatched elements
-- from BOTH inputs survive. For unique-element arrays this is exactly
-- the symmetric difference. (Source: core/src/val/array.rs:310-323.)
-- For relative complement A \ B use `array::complement` above.
array::difference([1,2,3], [2,3,4])          -- [1, 4]   (NOT [1] — both unmatched halves)
array::difference([1,1,2], [1,3])            -- [1, 2, 3]  (multiset pairing)
array::distinct([1, 2, 2, 3, 3])             -- [1, 2, 3]
array::find([1, 2, 3], 2)                    -- 2
array::find_index([1, 2, 3], 2)              -- 1
array::first([1, 2, 3])                      -- 1
array::flatten([[1, 2], [3, 4]])             -- [1, 2, 3, 4]
array::group([1,2,3,1,2])                    -- [1, 2, 3]
array::insert([1, 3], 2, 1)                  -- [1, 2, 3]
array::intersect([1,2,3], [2,3,4])           -- [2, 3]
array::join([1, 2, 3], ', ')                 -- '1, 2, 3'
array::last([1, 2, 3])                       -- 3
array::len([1, 2, 3])                        -- 3
array::logical_and([1, 0], [0, 1])           -- [0, 0]
array::logical_or([1, 0], [0, 1])            -- [1, 1]
array::logical_xor([1, 0], [0, 1])           -- [1, 1]
array::max([3, 1, 2])                        -- 3
array::min([3, 1, 2])                        -- 1
array::pop([1, 2, 3])                        -- [1, 2]
array::push([1, 2], 3)                       -- [1, 2, 3]
array::remove([1, 2, 3], 1)                  -- [1, 3]
array::reverse([1, 2, 3])                    -- [3, 2, 1]
array::shuffle([1, 2, 3])                    -- randomly shuffled
array::slice([1, 2, 3, 4], 1, 2)             -- [2, 3]
array::sort([3, 1, 2])                       -- [1, 2, 3]
array::sort::asc([3, 1, 2])                  -- [1, 2, 3]
array::sort::desc([3, 1, 2])                 -- [3, 2, 1]
array::transpose([[1,2],[3,4]])              -- [[1,3],[2,4]]
array::union([1, 2], [2, 3])                 -- [1, 2, 3]
array::windows([1,2,3,4], 2)                 -- [[1,2],[2,3],[3,4]]

-- Method syntax
[1, 2, 3].len()                              -- 3
[1, 2, 2, 3].distinct()                      -- [1, 2, 3]
[[1, 2], [3, 4]].flatten()                   -- [1, 2, 3, 4]
[3, 1, 2].sort()                             -- [1, 2, 3]
```

### Math Functions

```surql
math::abs(-42)                               -- 42
math::ceil(3.2)                              -- 4
math::floor(3.8)                             -- 3
math::round(3.5)                             -- 4
math::sqrt(16)                               -- 4.0
math::pow(2, 10)                             -- 1024
math::log(100, 10)                           -- 2.0
math::max([1, 5, 3])                         -- 5
math::min([1, 5, 3])                         -- 1
math::mean([1, 2, 3, 4, 5])                  -- 3
math::median([1, 2, 3, 4, 5])               -- 3
math::sum([1, 2, 3, 4, 5])                   -- 15
math::product([2, 3, 4])                     -- 24
math::fixed(3.14159, 2)                      -- 3.14
math::clamp(15, 0, 10)                       -- 10
math::lerp(0, 10, 0.5)                       -- 5.0
math::spread([1, 5, 3])                      -- 4
math::variance([1, 2, 3, 4, 5])             -- 2.0
math::stddev([1, 2, 3, 4, 5])               -- ~1.414
math::nearestrank([1, 2, 3, 4, 5], 75)      -- 4
math::percentile([1, 2, 3, 4, 5], 50)       -- 3.0
math::interquartile([1, 2, 3, 4, 5])        -- 2.0
math::midhinge([1, 2, 3, 4, 5])             -- 3.0
math::trimean([1, 2, 3, 4, 5])              -- 3.0
math::mode([1, 2, 2, 3])                    -- 2
math::bottom([5, 1, 3, 2, 4], 3)            -- [1, 2, 3]
math::top([5, 1, 3, 2, 4], 3)               -- [3, 4, 5]

-- Constants
math::pi                                     -- 3.14159...
math::e                                      -- 2.71828...
math::tau                                    -- 6.28318...
math::inf                                    -- Infinity
math::neg_inf                                -- -Infinity
```

### Time Functions

```surql
time::now()                                  -- current UTC datetime
time::day(d'2026-02-19T10:00:00Z')          -- 19
time::hour(d'2026-02-19T10:30:00Z')         -- 10
time::minute(d'2026-02-19T10:30:00Z')       -- 30
time::second(d'2026-02-19T10:30:45Z')       -- 45
time::month(d'2026-02-19T10:00:00Z')        -- 2
time::year(d'2026-02-19T10:00:00Z')         -- 2026
time::wday(d'2026-02-19T10:00:00Z')         -- day of week (0=Sunday)
time::yday(d'2026-02-19T10:00:00Z')         -- day of year
time::week(d'2026-02-19T10:00:00Z')         -- ISO week number
time::unix(d'2026-02-19T10:00:00Z')         -- Unix timestamp (seconds)

-- Formatting
time::format(time::now(), '%Y-%m-%d')        -- '2026-02-19'

-- Grouping (truncate to period)
time::group(d'2026-02-19T10:30:45Z', 'hour') -- d'2026-02-19T10:00:00Z'
time::group(d'2026-02-19T10:30:45Z', 'day')  -- d'2026-02-19T00:00:00Z'
time::group(d'2026-02-19T10:30:45Z', 'month') -- d'2026-02-01T00:00:00Z'

-- Rounding
time::floor(d'2026-02-19T10:30:45Z', 1h)    -- d'2026-02-19T10:00:00Z'

-- Component setters (datetime → datetime; v3.0.2+).
-- Each function takes a datetime and an integer for the targeted
-- component and returns a new datetime with that component replaced.
time::set_year(d'2026-02-19T10:00:00Z', 2030)        -- d'2030-02-19T10:00:00Z'
time::set_month(d'2026-02-19T10:00:00Z', 12)         -- d'2026-12-19T10:00:00Z'
time::set_day(d'2026-02-19T10:00:00Z', 1)            -- d'2026-02-01T10:00:00Z'
time::set_hour(d'2026-02-19T10:00:00Z', 23)          -- d'2026-02-19T23:00:00Z'
time::set_minute(d'2026-02-19T10:00:00Z', 45)        -- d'2026-02-19T10:45:00Z'
time::set_second(d'2026-02-19T10:00:00Z', 30)        -- d'2026-02-19T10:00:30Z'
time::set_nanosecond(d'2026-02-19T10:00:00Z', 500000000)
                                                      -- d'2026-02-19T10:00:00.500Z'
time::ceil(d'2026-02-19T10:30:45Z', 1h)     -- d'2026-02-19T11:00:00Z'
time::round(d'2026-02-19T10:30:45Z', 1h)    -- d'2026-02-19T11:00:00Z'

-- From Unix timestamp
time::from_micros(1708344000000000)
time::from_millis(1708344000000)
time::from_nanos(1708344000000000000)
time::from_secs(1708344000)
time::from_unix(1708344000)

-- Timezone
time::timezone()                             -- server timezone
```

### Duration Functions

```surql
duration::days(90h)                          -- 3 (number of complete days)
duration::hours(2d12h)                       -- 60 (total hours)
duration::micros(1s)                         -- 1000000
duration::millis(1s)                         -- 1000
duration::mins(2h30m)                        -- 150
duration::nanos(1ms)                         -- 1000000
duration::secs(1h30m)                        -- 5400

-- From components
duration::from::days(7)                      -- 7d
duration::from::hours(24)                    -- 1d
duration::from::micros(1000000)              -- 1s
duration::from::millis(1000)                 -- 1s
duration::from::mins(60)                     -- 1h
duration::from::nanos(1000000000)            -- 1s
duration::from::secs(3600)                   -- 1h
```

### Type Functions

```surql
-- Type checking
type::is::array([1, 2])                     -- true
type::is::bool(true)                         -- true
type::is::bytes(<bytes> 'data')              -- true
type::is::datetime(time::now())              -- true
type::is::decimal(19.99dec)                  -- true
type::is::duration(1h)                       -- true
type::is::float(3.14)                        -- true
type::is::geometry((-73.9, 40.7))            -- true
type::is::int(42)                            -- true
type::is::null(null)                         -- true
type::is::none(NONE)                         -- true
type::is::number(42)                         -- true
type::is::object({ a: 1 })                  -- true
type::is::point((-73.9, 40.7))              -- true
type::is::record(person:tobie)               -- true
type::is::string('hello')                    -- true
type::is::uuid(rand::uuid())                 -- true

-- Type construction
type::thing('person', 'tobie')               -- person:tobie
type::field('name')                          -- field reference
type::fields(['name', 'age'])                -- field references
type::record('person', 'tobie')              -- person:tobie
```

### Crypto Functions

```surql
-- Hashing
crypto::md5('hello')
crypto::sha1('hello')
crypto::sha256('hello')
crypto::sha512('hello')

-- Password hashing (use for auth)
crypto::argon2::generate('MyPassword')
crypto::argon2::compare($hash, 'MyPassword')

crypto::bcrypt::generate('MyPassword')
crypto::bcrypt::compare($hash, 'MyPassword')

crypto::scrypt::generate('MyPassword')
crypto::scrypt::compare($hash, 'MyPassword')
```

### Geo Functions

```surql
-- Distance between two points (meters)
geo::distance((-0.04, 51.55), (30.46, -17.86))

-- Area of a polygon (square meters)
geo::area({
    type: 'Polygon',
    coordinates: [[
        [-73.98, 40.75], [-73.97, 40.75],
        [-73.97, 40.76], [-73.98, 40.76],
        [-73.98, 40.75]
    ]]
})

-- Bearing between two points (degrees)
geo::bearing((-0.04, 51.55), (30.46, -17.86))

-- Centroid of a geometry
geo::centroid({
    type: 'Polygon',
    coordinates: [[
        [0, 0], [10, 0], [10, 10], [0, 10], [0, 0]
    ]]
})

-- Geohash encoding/decoding
geo::hash::encode((-0.04, 51.55))              -- geohash string
geo::hash::encode((-0.04, 51.55), 6)           -- with precision
geo::hash::decode('gcpuuz')                     -- geometry point
```

### HTTP Functions

Make outbound HTTP requests (requires network capability to be enabled).

```surql
-- GET request
http::get('https://api.example.com/data')

-- GET with headers
http::get('https://api.example.com/data', {
    'Authorization': 'Bearer token123'
})

-- POST request with body
http::post('https://api.example.com/data', {
    name: 'Tobie',
    email: 'tobie@surrealdb.com'
})

-- POST with custom headers
http::post('https://api.example.com/data', { name: 'Tobie' }, {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer token123'
})

-- PUT request
http::put('https://api.example.com/data/1', { name: 'Updated' })

-- PATCH request
http::patch('https://api.example.com/data/1', { age: 34 })

-- DELETE request
http::delete('https://api.example.com/data/1')

-- HEAD request
http::head('https://api.example.com/data')
```

### Meta / Record Functions

```surql
-- Extract the ID portion of a record ID
meta::id(person:tobie)                       -- 'tobie'
record::id(person:tobie)                     -- 'tobie'

-- Extract the table name from a record ID
meta::tb(person:tobie)                       -- 'person'
record::tb(person:tobie)                     -- 'person'
record::table(person:tobie)                  -- 'person'
```

### Parse Functions

```surql
-- Email parsing
parse::email::host('tobie@surrealdb.com')    -- 'surrealdb.com'
parse::email::user('tobie@surrealdb.com')    -- 'tobie'

-- URL parsing
parse::url::domain('https://surrealdb.com/docs')  -- 'surrealdb.com'
parse::url::host('https://surrealdb.com:8000')     -- 'surrealdb.com'
parse::url::path('https://surrealdb.com/docs')     -- '/docs'
parse::url::port('https://surrealdb.com:8000')     -- 8000
parse::url::query('https://example.com?a=1&b=2')   -- 'a=1&b=2'
parse::url::scheme('https://surrealdb.com')        -- 'https'
parse::url::fragment('https://example.com#section') -- 'section'
```

### Rand Functions

```surql
rand()                                       -- random float between 0 and 1
rand::bool()                                 -- random boolean
rand::enum('one', 'two', 'three')            -- random choice from values
rand::float()                                -- random float
rand::float(1.0, 100.0)                      -- random float in range
rand::guid()                                 -- random GUID string
rand::guid(20)                               -- random GUID of specific length
rand::int()                                  -- random integer
rand::int(1, 100)                            -- random integer in range
rand::string()                               -- random string
rand::string(10)                             -- random string of length
rand::string(5, 15)                          -- random string of length range
rand::time()                                 -- random datetime
rand::time(d'2020-01-01', d'2026-12-31')     -- random datetime in range
rand::uuid()                                 -- random UUID v7
rand::uuid::v4()                             -- random UUID v4
rand::uuid::v7()                             -- random UUID v7
rand::ulid()                                 -- random ULID
```

### Session Functions

Verified against v3.0.5 `core/src/fnc/session.rs`. There are EIGHT
session functions, not six — `session::ac` (access method name) and
`session::rd` (record-access record reference) are documented here
for the first time alongside the existing six.

```surql
session::ac()                                -- current access method name (auth)
session::db()                                -- current database name
session::id()                                -- current session ID
session::ip()                                -- client IP address
session::ns()                                -- current namespace name
session::origin()                            -- request origin
session::rd()                                -- record-access record reference
                                             --   (e.g. user:tobie when signed in
                                             --    via DEFINE ACCESS ... FOR RECORD)
session::token()                             -- current auth token claims
```

Each function reads from the in-memory `session` value on the
`FrozenContext` and returns `NONE` if the corresponding field is
unset. `session::ac` returns the access-method name as set during
authentication (the `AC` field on `paths::AC`); `session::rd`
returns the authenticated record (the `RD` field on `paths::RD`).
Both are particularly useful inside `DEFINE ACCESS ... PERMISSIONS`
and `DEFINE TABLE ... PERMISSIONS` clauses.

### Object Functions

```surql
object::entries({ a: 1, b: 2 })             -- [['a', 1], ['b', 2]]
object::from_entries([['a', 1], ['b', 2]])   -- { a: 1, b: 2 }
object::keys({ a: 1, b: 2 })                -- ['a', 'b']
object::len({ a: 1, b: 2 })                 -- 2
object::values({ a: 1, b: 2 })              -- [1, 2]
```

### Count Function

```surql
-- Count all records
SELECT count() FROM person GROUP ALL;

-- Count with condition
SELECT count() AS total FROM person WHERE active = true GROUP ALL;

-- Count values (non-null)
count([1, null, 2, null, 3])                 -- 3
```

### Vector Functions

```surql
-- Arithmetic operations
vector::add([1, 2, 3], [4, 5, 6])           -- [5, 7, 9]
vector::subtract([4, 5, 6], [1, 2, 3])      -- [3, 3, 3]
vector::multiply([1, 2, 3], [4, 5, 6])      -- [4, 10, 18]
vector::divide([4, 10, 18], [4, 5, 6])      -- [1, 2, 3]

-- Geometric operations
vector::angle([1, 0], [0, 1])               -- angle in radians
vector::cross([1, 0, 0], [0, 1, 0])         -- [0, 0, 1]
vector::dot([1, 2, 3], [4, 5, 6])           -- 32
vector::magnitude([3, 4])                    -- 5.0
vector::normalize([3, 4])                    -- [0.6, 0.8]
vector::project([3, 4], [1, 0])             -- projection vector
vector::scale([1, 2, 3], 2.0)               -- [2, 4, 6] (scalar multiply)

-- Distance functions (lower = closer; positive metrics)
-- Verified against v3.0.5 vector function registry: cosine, jaccard,
-- and pearson are NOT exposed under `vector::distance::*` — they live
-- only under `vector::similarity::*` below. See the similarity block.
vector::distance::chebyshev([1, 2], [4, 6])     -- 4
vector::distance::euclidean([1, 2], [4, 6])      -- 5.0
vector::distance::hamming([1, 0, 1], [1, 1, 0])  -- 2
vector::distance::manhattan([1, 2], [4, 6])      -- 7
vector::distance::minkowski([1, 2], [4, 6], 3)   -- minkowski with p=3
-- vector::distance::knn is NOT a standalone callable distance
-- function. It is a context-only function that reads the current
-- HNSW-index iteration result and accepts an optional 0-indexed
-- KNN reference (default 0). It cannot be called with a `(vec_a,
-- vec_b, k)` form. Source: `core/src/fnc/vector.rs:87-103`.
-- Use the brute-force `<|K,DIST|>` operator (see "KNN Operators"
-- below) for ad-hoc nearest-neighbour computation; use
-- `vector::distance::knn(@idx)` only inside a SELECT that scans
-- the HNSW index it refers to.

-- vector::distance::mahalanobis exists as a registered function
-- with a 2-argument signature (`Vec<Number>, Vec<Number>`), but
-- in v3.0.5 it ALWAYS returns `Error::Unimplemented` at runtime.
-- Source: `core/src/fnc/vector.rs:105-108`. There is no covariance-
-- matrix argument. Do NOT call this function in production until
-- it ships an implementation. Equivalent guidance:
--   vector::distance::mahalanobis([1, 2], [3, 4]) -- ERRORS in v3.0.5

-- Similarity functions (higher = more similar)
-- For cosine / jaccard / pearson, the upstream function lives ONLY
-- under `vector::similarity::*`. To get a "distance"-shaped value
-- (lower = closer), compute `1 - vector::similarity::cosine(...)`,
-- and similarly for jaccard / pearson.
vector::similarity::cosine([1, 2], [3, 4])       -- cosine similarity
vector::similarity::jaccard([1, 2, 3], [2, 3, 4]) -- jaccard similarity
vector::similarity::pearson([1, 2, 3], [4, 5, 6]) -- pearson similarity
-- vector::similarity::spearman is registered with a 2-argument
-- signature but ALWAYS returns `Error::Unimplemented` at runtime
-- in v3.0.5. Source: `core/src/fnc/vector.rs:140-143`. Do NOT call
-- it in production until it ships an implementation.
--   vector::similarity::spearman([1, 2, 3], [4, 5, 6]) -- ERRORS in v3.0.5
```

### Search Functions

Used in full-text search queries with `FULLTEXT ANALYZER` indexes.

```surql
-- Highlight matching terms
SELECT search::highlight('<b>', '</b>', 1) AS highlighted
FROM article
WHERE content @1@ 'SurrealDB';

-- Get offsets of matching terms
SELECT search::offsets(1) AS offsets
FROM article
WHERE content @1@ 'SurrealDB';

-- Get BM25 score
SELECT search::score(1) AS score
FROM article
WHERE content @1@ 'SurrealDB'
ORDER BY score DESC;
```

The `@N@` operator is the match operator for full-text search, where `N` is the index reference number used with `search::score()`, `search::highlight()`, and `search::offsets()`.

```surql
-- search::analyze(analyzer_name: string, text: string) -> array<string>
-- Run a defined analyzer over a string and return the resulting
-- token stream. Useful for previewing tokenization rules without
-- having to index a document.
DEFINE ANALYZER blog TOKENIZERS class FILTERS lowercase, snowball(english);
search::analyze('blog', 'The Quick brown FOXES')
                                              -- ['quick', 'brown', 'fox']

-- search::rrf(results: array, limit: int, rrf_constant?: int=60) -> array
-- Reciprocal Rank Fusion. Combines multiple ranked result lists
-- into a single ranked list using the standard RRF formula
-- `1 / (k + rank)` where `k` is `rrf_constant` (default 60) and
-- `rank` is 1-based. Each result list MUST contain objects with
-- an `id` field; documents are merged by id across lists.
LET $vec = SELECT id, embedding FROM doc WHERE embedding <|10|> $q;
LET $ft  = SELECT id, ft_score FROM doc WHERE content @1@ 'surrealdb';
RETURN search::rrf([$vec, $ft], 10);          -- top 10 fused
RETURN search::rrf([$vec, $ft], 10, 30);      -- with k=30 (sharper)

-- search::linear(results: array, weights: array<number>, limit: int,
--                norm: 'minmax' | 'zscore') -> array
-- Linear-combination fusion with per-list weights and normalization.
-- `weights.len()` MUST equal `results.len()`. Score extraction
-- priority per document: `distance` (transformed via 1/(1+d)),
-- `ft_score`, `score`, then rank-based fallback `1/(1+rank)`.
RETURN search::linear([$vec, $ft], [2.0, 1.0], 10, 'minmax');
RETURN search::linear([$vec, $ft], [1.0, 1.0], 10, 'zscore');
```

`search::rrf` rejects `limit < 1` and `rrf_constant < 0` with
`InvalidFunctionArguments`. `search::linear` rejects mismatched
array lengths, non-numeric weights, and any `norm` value other than
the two listed.

### Value Functions

```surql
-- Compute JSON Merge Patch diff between two values
value::diff({ a: 1, b: 2 }, { a: 1, b: 3 })  -- returns diff

-- Apply a JSON Merge Patch to a value
value::patch({ a: 1, b: 2 }, [{ op: 'replace', path: '/b', value: 3 }])
```

### Encoding Functions

Verified against v3.0.5 `core/src/fnc/encoding.rs`. The `encoding::*`
namespace exposes exactly four functions: two for Base64 and two for
CBOR. Nothing else (no hex / urlencoding / base32 / etc.).

```surql
-- Base64 (RFC 4648 standard alphabet)
-- encoding::base64::encode(bytes, padded?: bool=false) -> string
-- The optional second argument controls padding. Default is NO padding
-- (`STANDARD_NO_PAD`). Pass `true` to emit standard padded base64.
encoding::base64::encode(<bytes> 'hello')         -- 'aGVsbG8'      (no padding)
encoding::base64::encode(<bytes> 'hello', true)   -- 'aGVsbG8='     (padded)

-- encoding::base64::decode(string) -> bytes
-- Decoding is padding-INSENSITIVE: it accepts both padded and unpadded
-- input (`DecodePaddingMode::Indifferent`). Returns a `bytes` value.
encoding::base64::decode('aGVsbG8')               -- <bytes> 'hello'
encoding::base64::decode('aGVsbG8=')              -- <bytes> 'hello' (also OK)

-- CBOR (RFC 8949) round-trip via SurrealDB's public-value bridge.
-- encoding::cbor::encode(value) -> bytes
-- encoding::cbor::decode(bytes) -> value
-- Useful for binary serialization of arbitrary SurrealQL values
-- (records, datetimes, durations, decimals all supported via CBOR
-- tags). Errors on values that cannot be represented as a public
-- value (e.g. closures).
encoding::cbor::encode({ a: 1, b: [2, 3] })       -- <bytes> ...
encoding::cbor::decode(encoding::cbor::encode({ a: 1 }))  -- { a: 1 }
```

`encoding::base32`, `encoding::base64url`, `encoding::hex`,
`encoding::url`, `encoding::json`, and any other format are NOT
registered in v3.0.5. Only `base64` and `cbor` exist.

### Bytes Functions

Verified against v3.0.5 `core/src/fnc/bytes.rs`. The `bytes::*`
namespace exposes exactly ONE function in v3.0.5 — do NOT assume
the namespace mirrors `string::*`.

```surql
-- bytes::len(bytes) -> int
-- Number of raw bytes in a `bytes` value (NOT the string length —
-- the input is bytes, not a string).
bytes::len(<bytes> 'hello')                  -- 5
bytes::len(encoding::base64::decode('aGVsbG8'))  -- 5
```

`bytes::concat`, `bytes::slice`, `bytes::at`, `bytes::reverse`, and
any other transform are NOT registered in v3.0.5. Use `encoding::*`
for format conversions and `string::*` after decoding for textual
manipulation.

### Set Functions

Verified against v3.0.5 `core/src/fnc/set.rs` (396 LOC). The `set::*`
namespace operates on the first-class `Set` value (constructed via
`<set> [...]` cast or via SET fields in tables) and provides
mathematical-set semantics that DIFFER from `array::*` in three
important ways:

1. **`set::difference(A, B)` is the SYMMETRIC difference (A △ B)**,
   NOT `A \ B`. Use `set::complement(A, B)` for the relative
   complement (`A \ B`). The `array::*` namespace uses the SAME
   convention: `array::difference` is also the symmetric difference
   (with multiset-pairing semantics for duplicates — see the array
   section above), and `array::complement(A, B)` is the relative
   complement `A \ B`. So in both namespaces the function named
   `difference` means **A △ B**, contrary to the common
   informal-English reading of "difference" as `A \ B`. Source:
   `core/src/fnc/set.rs:68-76` (set), `core/src/val/array.rs:289-323`
   (array).
2. Sets are stored in `BTreeSet<Value>` (Rust standard-library
   BTree), so iteration / positional access is in **`Value::Ord`
   sort order**, not insertion order. `at`, `first`, `last`,
   `slice`, and the closure-based traversal functions all visit
   elements in this `Value::Ord` order. The ordering is determined
   by the cross-type `Value` comparator defined upstream (numbers
   before strings before arrays, etc.), not a SurrealDB-specific
   custom ordering.
3. Closure-based methods (`all`, `any`, `filter`, `find`, `fold`,
   `map`, `reduce`) iterate in sorted order and the closure receives
   one element at a time (or `(accum, val)` for fold/reduce).

```surql
-- Construction
<set> [1, 2, 2, 3]                           -- {1, 2, 3} (deduped on cast)

-- Membership and size
set::contains(<set>[1, 2, 3], 2)             -- true
set::len(<set>[1, 2, 3])                     -- 3
set::is_empty(<set>[])                       -- true

-- Mutating returns (the original set is not modified; result is new)
set::add(<set>[1, 2], 3)                     -- {1, 2, 3}
set::add(<set>[1, 2], [3, 4])                -- {1, 2, 3, 4} (array spread-insert)
set::add(<set>[1, 2], <set>[3, 4])           -- {1, 2, 3, 4} (set spread-insert)
set::remove(<set>[1, 2, 3], 2)               -- {1, 3}
set::remove(<set>[1, 2, 3], [1, 2])          -- {3}            (array spread-remove)

-- Set algebra
set::union(<set>[1, 2], <set>[2, 3])         -- {1, 2, 3}     (A ∪ B)
set::intersect(<set>[1, 2, 3], <set>[2, 3, 4]) -- {2, 3}      (A ∩ B)
set::difference(<set>[1, 2, 3], <set>[2, 3, 4]) -- {1, 4}     (A △ B — SYMMETRIC)
set::complement(<set>[1, 2, 3], <set>[2, 3]) -- {1}           (A \ B — RELATIVE)

-- Element access (BTree order)
set::first(<set>[3, 1, 2])                   -- 1             (minimum)
set::last(<set>[3, 1, 2])                    -- 3             (maximum)
set::at(<set>[1, 2, 3], 0)                   -- 1
set::at(<set>[1, 2, 3], -1)                  -- 3             (negative = from end)
set::min(<set>[3, 1, 2])                     -- 1
set::max(<set>[3, 1, 2])                     -- 3

-- Slicing (positional, BTree order)
-- set::slice(set, start_or_range?, end?) -> set
-- Three forms: no args (returns whole set), single int (start..),
-- start+end (start..end exclusive), or a Range value.
set::slice(<set>[1, 2, 3, 4, 5])             -- {1, 2, 3, 4, 5}
set::slice(<set>[1, 2, 3, 4, 5], 1)          -- {2, 3, 4, 5}
set::slice(<set>[1, 2, 3, 4, 5], 1, 3)       -- {2, 3}        (1..3 exclusive)
set::slice(<set>[1, 2, 3, 4, 5], -2)         -- {4, 5}        (negative supported)

-- Flattening + serialization
set::flatten(<set>[<set>[1, 2], <set>[3]])   -- {1, 2, 3}
set::join(<set>['a', 'b', 'c'], ', ')        -- 'a, b, c'

-- Closure-based traversal (async — closure invoked per element)
-- These are the seven async ones; they accept either a closure or a
-- plain value (which is matched for equality in `all`/`any`/`filter`/
-- `find`).
set::all(<set>[1, 2, 3], |$x| $x > 0)        -- true
set::any(<set>[1, 2, 3], |$x| $x > 2)        -- true
set::filter(<set>[1, 2, 3, 4], |$x| $x % 2 = 0)  -- {2, 4}
set::find(<set>[1, 2, 3], |$x| $x > 1)       -- 2
set::map(<set>[1, 2, 3], |$x| $x * 2)        -- {2, 4, 6}
set::fold(<set>[1, 2, 3], 0, |$acc, $x| $acc + $x)  -- 6
set::reduce(<set>[1, 2, 3], |$acc, $x| $acc + $x)   -- 6 (uses first elem as init)
```

NOT exposed under `set::*` in v3.0.5: `set::sort` (sets are already
ordered), `set::distinct` (sets are already deduplicated),
`set::reverse`, `set::concat`, `set::sample`, and the symmetric
`set::is_subset` / `set::is_superset` predicates. Use `array::*`
casts or boolean checks via `set::intersect` / `set::complement`
for the missing predicates.

### Sequence Functions

Verified against v3.0.5 `core/src/fnc/sequence.rs`. The `sequence::*`
namespace exposes exactly ONE function in v3.0.5 — sequences are
created with `DEFINE SEQUENCE` and read with this single function.

```surql
-- Create a sequence (DDL, not part of the function namespace)
DEFINE SEQUENCE invoice_no START 1000 BATCH 100 TIMEOUT 5s;

-- sequence::nextval(name: string) -> int
-- Returns the next value for the named sequence. Atomic and
-- monotonically increasing within a sequence. Errors if the
-- sequence is undefined or the namespace/database is invalid.
sequence::nextval('invoice_no')              -- 1000
sequence::nextval('invoice_no')              -- 1001
```

`sequence::reset`, `sequence::current`, `sequence::peek` are NOT
registered in v3.0.5. Use `REMOVE SEQUENCE name; DEFINE SEQUENCE
name START n;` to reset (which renumbers from `n`). There is no
non-mutating "peek the next value without consuming" function.

### Schema Functions

Verified against v3.0.5 `core/src/fnc/schema.rs`. The `schema::*`
namespace exposes exactly ONE function in v3.0.5. Schema introspection
is otherwise done via `INFO FOR DB`, `INFO FOR TABLE name`, and
`INFO FOR USER name`.

```surql
-- schema::table::exists(name: string) -> bool
-- Returns true if a table with the given name is defined in the
-- current database. Requires Action::View permission on the table
-- resource (will error under restrictive access).
schema::table::exists('person')              -- true | false

-- Idiomatic guard before DEFINE
IF !schema::table::exists('audit_log') THEN
    DEFINE TABLE audit_log SCHEMAFULL;
END;
```

`schema::table::list`, `schema::field::*`, `schema::index::*`,
`schema::namespace::*`, `schema::database::*`, and any other
`schema::*` predicates are NOT registered in v3.0.5. Use `INFO FOR
DB` (returns objects keyed by definition kind) or query the
`information_schema`-style virtual catalogs through `INFO` for
broader introspection.

### File Functions (Experimental — `Files` capability required)

Verified against v3.0.5 `core/src/fnc/file.rs` (232 LOC). All 13
functions in the `file::*` namespace are gated behind the experimental
`Files` capability. The registry split is:
- 2 sync inspectors at `core/src/fnc/mod.rs:239-240`
  (`file::bucket`, `file::key`)
- 11 async I/O functions at `core/src/fnc/mod.rs:602-612`
  (`put`, `put_if_not_exists`, `get`, `head`, `delete`, `copy`,
  `copy_if_not_exists`, `rename`, `rename_if_not_exists`, `exists`,
  `list`)

Every row carries the `exp(Files)` macro prefix, meaning the
capability check resolves at function-DISPATCH time (not at
SurrealQL parse time): if the `Files` capability is disabled, the
call parses successfully but errors when the dispatcher reaches the
gated row in `core/src/fnc/mod.rs:114-133`. Start the server with
`--allow-experimental Files` (or equivalent config) to enable these
functions. DO NOT rely on them in production until Files moves out
of experimental.

```surql
-- File values bind a bucket + key. Construct via DEFINE BUCKET first.
-- READONLY is a bare flag (no boolean operand) per the parser at
-- core/src/syn/parser/stmt/define.rs:1378-1380. Omit it for a
-- writable bucket; include it for read-only.
DEFINE BUCKET assets BACKEND "memory";

-- Bind a file pointer (does NOT read; resolves bucket+key).
LET $f = <file> "assets:/avatars/tobie.png";

-- Inspect the binding (these two are sync, capability still required)
file::bucket($f)                             -- 'assets'
file::key($f)                                -- '/avatars/tobie.png'

-- Read / write
file::put($f, <bytes> 'PNG-bytes-here')      -- NONE on success
-- *_if_not_exists is a NO-OP when the destination key already
-- exists — it does NOT error. Source: core/src/buc/controller.rs
-- comments at lines 97-103 ("If the key already exists, the
-- operation is a no-op").
file::put_if_not_exists($f, <bytes> '...')   -- NONE (no-op if key exists)
file::get($f)                                -- <bytes> ... or NONE
-- head() returns { updated, size, file } when present, NONE otherwise.
-- Source: core/src/buc/store/mod.rs:35-52 (ObjectMeta -> object value
-- has fields `updated: datetime`, `size: int`, `file: file`). NO
-- `etag` field exists in v3.0.5.
file::head($f)                               -- { updated, size, file } or NONE
file::exists($f)                             -- true | false
file::delete($f)                             -- NONE
file::list('assets', { prefix: '/avatars/' }) -- [{ updated, size, file }, ...]

-- Copy / rename
-- Destination can be a string (key relative to source bucket) or
-- another file value (cross-bucket). The *_if_not_exists variants
-- are NO-OPS when the destination already exists (same convention
-- as put_if_not_exists; source: core/src/buc/controller.rs:181-216).
file::copy($f, '/avatars/backup-tobie.png')  -- NONE
file::copy($f, <file> "archive:/backups/tobie.png")  -- cross-bucket
file::copy_if_not_exists($f, '/avatars/backup-tobie.png')   -- NONE (no-op)
file::rename($f, '/avatars/tobie-new.png')   -- NONE (within same bucket)
file::rename_if_not_exists($f, '/avatars/tobie-new.png')    -- NONE (no-op)
```

Signature reference (verified against `core/src/fnc/file.rs`):

| Function | Args | Returns |
|---|---|---|
| `file::bucket` / `file::key` | `(file)` | string |
| `file::put` / `file::put_if_not_exists` | `(file, value)` (value coerced via accept_payload) | NONE |
| `file::get` | `(file)` | bytes \| NONE |
| `file::head` | `(file)` | `{ updated, size, file }` \| NONE |
| `file::exists` | `(file)` | bool |
| `file::delete` | `(file)` | NONE |
| `file::list` | `(bucket: string, options?: object)` | array<object> |
| `file::copy` / `file::copy_if_not_exists` | `(src: file, dst: string \| file)` | NONE |
| `file::rename` / `file::rename_if_not_exists` | `(src: file, target: string)` | NONE |

Notable asymmetries:
- `file::list` is the ONLY function that takes a STRING bucket name
  (not a `file` value) AND an options object.
- `file::copy` / `file::copy_if_not_exists` are the ONLY functions
  whose destination can be EITHER a string (relative key in the
  source bucket) OR a `file` value (cross-bucket).
- `file::rename` / `file::rename_if_not_exists` only accept a STRING
  target — there is no cross-bucket rename. Use `file::copy` +
  `file::delete` instead.

`file::move` does NOT exist — use `file::rename` (intra-bucket) or
`file::copy` followed by `file::delete` (cross-bucket).

### API Functions

Verified against v3.0.5 `core/src/fnc/api/{mod,req,res}.rs`. The
`api::*` namespace exposes 7 functions, but they split into two
distinct usage modes:

1. **Callable from regular SurrealQL** — `api::invoke` only.
2. **Middleware-only** — `api::req::body`, `api::res::body`,
   `api::res::status`, `api::res::header`, `api::res::headers`,
   `api::timeout`. These take a `next` closure as one of their
   arguments and are designed to compose inside a
   `DEFINE API ... MIDDLEWARE` chain. Calling them outside that
   context fails with an arity / type error — the implicit `req`
   and `next` arguments supplied by the middleware runtime are
   not available, so the call is rejected before any side effect.

```surql
-- ============================================
-- 1. Callable: api::invoke
-- ============================================

-- api::invoke(path: string, req?: object) -> object
-- Calls a defined API endpoint internally (server-side dispatch,
-- no HTTP round-trip). Path MUST start with '/'. The optional
-- request object's input fields (per core/src/api/request.rs:14-23).
-- All caller-supplied fields are forwarded to the matched route's
-- handler as the SurrealQL `$request` value (see
-- core/src/api/invocation.rs:198-220), with TWO exceptions:
-- - `request_id` is OVERWRITTEN by `api::invoke` with a freshly
--   generated UUID (core/src/fnc/api/mod.rs:66-68) — passing your
--   own value has no effect.
-- - `params` is OVERWRITTEN with the values extracted from path
--   matching (core/src/fnc/api/mod.rs:92-95).
-- Caller-supplied `context` IS forwarded into the handler as
-- `$request.context`; the strip at core/src/fnc/api/mod.rs:101-106
-- only removes `context` from the RESPONSE object before
-- `api::invoke` returns, not from the request before the handler
-- sees it. Schema:
--   { method:  'get' | 'post' | 'put' | 'patch' | 'delete' | 'trace',
--             -- NOTE: 'head' is NOT a valid ApiMethod variant in
--             -- v3.0.5; the enum includes 'trace' instead. Source:
--             -- core/src/catalog/schema/api.rs:111-126.
--     headers: { string: string },
--     body:    <any>,
--     query:   { string: string },   -- query-string parameters
--     params:  { string: string },   -- OVERWRITTEN by path matching
--                                    -- when the route matches; on
--                                    -- unmatched paths the request
--                                    -- short-circuits to NotFound so
--                                    -- caller-supplied params are
--                                    -- never observable in any
--                                    -- handler. (fnc/api/mod.rs:92-95)
--     context: { ... }               -- forwarded as $request.context
--                                    -- to the matched handler;
--                                    -- stripped from the RESPONSE
--                                    -- object before api::invoke
--                                    -- returns (fnc/api/mod.rs:101-106)
--   }
-- (`request_id` is also a struct field but is unconditionally
-- overwritten with a fresh UUID — do not pass it.)
-- Defaults: GET, Content-Type + Accept set to native SurrealDB
-- format if absent. Returns the response object with `context`
-- stripped. Returns a NotFound-shaped response if no matching
-- definition.

api::invoke('/users/123');                                  -- GET
api::invoke('/users/123', { method: 'get' });
api::invoke('/users', {
    method: 'post',
    body: { name: 'Tobie', age: 33 }
});

-- ============================================
-- 2. Middleware-only (used inside DEFINE API ... MIDDLEWARE)
-- ============================================

-- api::req::body(strategy?) — parse the request body in place.
-- Strategies: 'auto' (default; sniff Content-Type), 'json', 'cbor',
-- 'flatbuffers', 'plain' (UTF-8 string), 'bytes' (raw, no parse),
-- 'native' (SurrealDB native).
DEFINE API "/users"
    FOR post
        MIDDLEWARE api::req::body('json')
        THEN { RETURN { status: 201, body: { name: $request.body.name } }; };

-- api::res::body(strategy?) — serialize the response body.
-- Same strategy set; 'auto' negotiates from Accept header.
DEFINE API "/data"
    FOR get
        MIDDLEWARE api::res::body('cbor')
        THEN { RETURN { status: 200, body: { hello: 'world' } }; };

-- api::res::status(code: int) — set status code (must be 100..=599).
DEFINE API "/not-found"
    FOR get
        MIDDLEWARE api::res::status(404)
        THEN { RETURN { body: { error: 'gone' } }; };

-- api::res::header(name: string, value?: string) — set or remove a
-- single response header. To REMOVE a header, OMIT the second
-- argument (one-arg form). The function signature uses
-- `Optional<String>`, whose `Optional<T>` resolves to `None` ONLY
-- when the argument is absent (core/src/fnc/args.rs:81-97).
-- Passing an explicit `NONE` value as the second argument is
-- rejected as a type error: `NONE` cannot coerce to `String` via
-- the `String` FromArg path. Use `api::res::headers` (the map form
-- below) when you need to mix sets and removes in one call — its
-- value type is `Option<String>`, so a `NONE` map value DOES
-- remove that header.
DEFINE API "/cors"
    FOR get
        MIDDLEWARE api::res::header('Access-Control-Allow-Origin', '*')
        THEN { RETURN { status: 200, body: {} }; };

-- Remove a header by omitting the value argument:
DEFINE API "/strip-server"
    FOR get
        MIDDLEWARE api::res::header('Server')   -- one arg = remove
        THEN { RETURN { status: 200, body: {} }; };

-- api::res::headers(map: { string: string|NONE }) — batch set/remove.
-- The map's value type is `Option<String>` (core/src/fnc/api/res.rs:184),
-- so `NONE` here DOES remove the header (different from
-- `api::res::header`'s second arg semantics). More efficient than
-- chaining api::res::header for many headers.
DEFINE API "/secure"
    FOR get
        MIDDLEWARE api::res::headers({
            'X-Frame-Options': 'DENY',
            'X-Content-Type-Options': 'nosniff',
            'Server': NONE,                  -- removes the Server header
        })
        THEN { RETURN { status: 200, body: {} }; };

-- api::timeout(duration) — abort request processing after duration.
DEFINE API "/slow"
    FOR get
        MIDDLEWARE api::timeout(5s)
        THEN { RETURN { status: 200, body: 'done' }; };
```

Argument-shape notes:
- `api::invoke` is a regular async function — its `req` arg is a
  PUBLIC `ApiRequest` object converted via `FromPublic`. Enum-style
  values like `method` derive from `ApiMethod` with
  `#[surreal(untagged, lowercase)]` (source:
  `core/src/catalog/schema/api.rs:111-126`); the derive matches the
  input string against the variant name LOWERCASED, so the input
  must itself be lowercase. `'GET'` and `'Get'` are NOT accepted —
  use `'get'`, `'post'`, etc.
- Direct calls to the middleware functions outside a
  `DEFINE API ... MIDDLEWARE` chain do not produce undefined
  behaviour — they fail with an arity / type error when the
  required implicit `(req, next)` arguments are missing or do not
  coerce. The middleware functions all take `(req, next, ...args)`
  and invoke `next.invoke(...)` to continue the chain. Their first
  visible argument in the SurrealQL call is the strategy / status /
  header — `req` and `next` are bound implicitly by the
  `DEFINE API ... MIDDLEWARE` runtime.
- `api::res::status` validates the code via `StatusCode::from_u16`
  and rejects any value outside `100..=599` with
  `ApiError::InvalidStatusCode`.

### Sleep Function

Verified against v3.0.5 `core/src/fnc/sleep.rs`. Registered as the
TOP-LEVEL function name `"sleep"` in `core/src/fnc/mod.rs:639` —
NOT under any namespace. Do NOT call it as `session::sleep`,
`time::sleep`, or `system::sleep`; those names are unregistered and
will fail with "function not found".

```surql
-- sleep(dur: duration) -> NONE
-- Pause execution for the given duration. The actual sleep is
-- clamped by the surrounding query / transaction timeout — if the
-- context timeout is shorter than `dur`, sleep returns when the
-- context timeout elapses, NOT after the full requested duration.
sleep(100ms)                                 -- pause 100ms, return NONE
sleep(2s)                                    -- pause 2 seconds

-- Useful for rate-limit testing, deterministic backoff, or
-- exercising TIMEOUT clauses. The function itself returns `Ok(NONE)`
-- after the (possibly clamped) wait — see core/src/fnc/sleep.rs:7-19.
-- The surrounding TIMEOUT clause is what surfaces a timeout error to
-- the client.
--
-- IMPORTANT: `RETURN` does NOT accept a `TIMEOUT` clause — its parser
-- only consumes the expression and an optional `FETCH`
-- (core/src/syn/parser/stmt/mod.rs:566-575). Attach `TIMEOUT` to a
-- statement that actually parses it (`SELECT`, `CREATE`, `UPDATE`,
-- `DELETE`, `RELATE`, `INSERT`, etc.):
CREATE timeout_probe SET slept = sleep(10s) TIMEOUT 1s;
-- After ~1s the surrounding TIMEOUT fires and the client receives a
-- timeout-shaped error rather than a created `timeout_probe` row.
-- (Sleep itself does not return an error; the TIMEOUT clause does.)
-- Source: core/src/syn/parser/stmt/create.rs:8-22 +
-- core/src/syn/parser/stmt/mod.rs:566-575.
```

The sleep is implemented via `tokio::time::sleep` (or
`wasmtimer::tokio::sleep` on wasm builds), so it does NOT block the
async runtime — other concurrent queries proceed normally.

---

## Subqueries and Expressions

### Subqueries

Any SurrealQL query can be used as a subquery within another query.

```surql
-- Subquery in WHERE clause
SELECT * FROM article
WHERE author IN (SELECT VALUE id FROM person WHERE role = 'editor');

-- Subquery in field projection
SELECT *,
    (SELECT VALUE count() FROM ->wrote->article GROUP ALL) AS article_count
FROM person;

-- Subquery in LET
LET $recent_articles = (
    SELECT * FROM article
    WHERE created_at > time::now() - 7d
    ORDER BY created_at DESC
    LIMIT 10
);
```

### Record Links

Records can directly link to other records using record IDs.

```surql
-- Create a record with a link
CREATE article SET
    title = 'Introduction to SurrealDB',
    author = person:tobie;

-- Query through the link
SELECT title, author.name FROM article;

-- Deep link traversal
SELECT title, author.company.name FROM article;
```

### Graph Traversal

Navigate graph relationships using arrow operators.

```surql
-- Forward traversal (outgoing edges)
SELECT ->wrote->article FROM person:tobie;

-- Backward traversal (incoming edges)
SELECT <-wrote<-person FROM article:surreal;

-- Multi-hop traversal
SELECT ->knows->person->wrote->article FROM person:tobie;

-- Bidirectional traversal
SELECT <->knows<->person FROM person:tobie;

-- Traversal with filtering
SELECT ->bought->product WHERE price > 100 FROM person:tobie;

-- Traversal with field selection
SELECT ->wrote->article.title FROM person:tobie;

-- Access edge properties during traversal
SELECT ->bought.quantity, ->bought->product.name FROM person:tobie;

-- Recursive traversal (ancestry)
-- Get parents
SELECT ->child_of->person FROM person:1;
-- Get grandparents
SELECT ->child_of->person->child_of->person FROM person:1;
-- All ancestors (variable depth)
SELECT ->child_of->person.* FROM person:1;
```

### Deferred Computation: Computed Fields, Closures, JS Functions

The `<future> { … }` expression syntax does NOT exist in v3.0.5
(verified against the v3.0.5 `Value` enum in `core/src/val/mod.rs`,
the `Kind` enum in `core/src/sql/kind.rs`, the lexer keyword set,
and the expression parser — none recognise `FUTURE` as a token, and
no `Future` variant exists in either enum). Earlier SurrealDB
versions did expose a `<future>` form; in v3 the use cases are
covered by three other features:

- **Computed fields** via `DEFINE FIELD … VALUE @expression` (see
  the [DEFINE FIELD](#define-field) section above) — re-evaluates
  the expression on every read of the record. This is the direct
  successor to v1/v2 `<future>` for "deferred computation on read".

  ```surql
  -- Recomputed on every SELECT — no value stored on disk.
  DEFINE FIELD age_display ON TABLE person
      VALUE string::concat(<string> age, ' years old');

  CREATE person SET name = 'Tobie', age = 33;
  -- SELECT age_display FROM person → 'Tobie' record returns
  -- 'age_display: "33 years old"' computed on read.
  ```

- **Closures** via the `|$args| body` syntax — first-class function
  values you can store on records, pass as parameters, or invoke
  on demand. Closure parameters are `$`-prefixed identifiers (bare
  identifiers in SurrealQL bind to field references, not local
  variables) and the closure body uses standard expression syntax
  with `RETURN` for the result.

  ```surql
  LET $double = |$n: number| $n * 2;
  RETURN $double(21);   -- 42
  ```

- **Embedded JavaScript** via `function() { … }` (see the
  [Embedded JavaScript](#embedded-javascript) section) — for
  computation that does not fit SurrealQL's expression surface.

### Parameters

Variables prefixed with `$` used in queries.

```surql
-- User-defined parameters (via LET or API)
LET $name = 'Tobie';
SELECT * FROM person WHERE name = $name;

-- System parameters
$auth     -- Current authenticated user record
$session  -- Current session data
$token    -- Current JWT token claims
$before   -- Record state before event (in events/live queries)
$after    -- Record state after event (in events/live queries)
$value    -- Current field value (in ASSERT/VALUE expressions)
$this     -- Current record (in field expressions)
$parent   -- Parent record (in subqueries)
$event    -- Event type string: 'CREATE', 'UPDATE', 'DELETE' (in events)
$input    -- Input data (in ON DUPLICATE KEY UPDATE)
```

### Embedded JavaScript

SurrealDB supports inline JavaScript functions for complex logic.

```surql
-- Inline JavaScript function
CREATE person SET
    name = 'Tobie',
    name_slug = function() {
        return arguments[0].name.toLowerCase().replace(/\s+/g, '-');
    };

-- JavaScript in function definitions
DEFINE FUNCTION fn::slugify($text: string) {
    RETURN function($text) {
        return arguments[0].toLowerCase()
            .replace(/[^\w\s-]/g, '')
            .replace(/\s+/g, '-');
    };
};
```

---

## Idioms and Patterns

### Record ID Syntax

```surql
-- Table:ID is the universal record identifier
person:tobie                 -- string ID
person:100                   -- numeric ID
person:uuid()                -- auto UUID
person:ulid()                -- auto ULID
person:rand()                -- auto random

-- Compound IDs
temperature:['London', '2026-02-19']    -- array compound key
user_session:{user: 'tobie', device: 'laptop'}  -- object compound key
```

### Destructuring and Nested Access

```surql
-- Access nested fields
SELECT name.first, name.last FROM person;

-- Access array elements
SELECT tags[0] FROM article;

-- Filter within arrays
SELECT emails[WHERE verified = true] FROM person;

-- Optional access for nullable record-link fields uses `.?` (period
-- before question-mark), not the JS-style `?.`. Verify against
-- https://surrealdb.com/docs/surrealql/idioms before relying on it.
SELECT spouse.?.name FROM person;
```

### Computed Table Views

```surql
-- Auto-updated aggregate view
DEFINE TABLE monthly_sales AS
    SELECT
        time::group(created_at, 'month') AS month,
        count() AS order_count,
        math::sum(total) AS revenue
    FROM order
    GROUP BY time::group(created_at, 'month');

-- Query the view like a regular table
SELECT * FROM monthly_sales ORDER BY month DESC;
```

### Changefeeds

```surql
-- Enable changefeed on a table
DEFINE TABLE orders CHANGEFEED 7d;

-- Read changes since a timestamp
SHOW CHANGES FOR TABLE orders SINCE '2026-02-01T00:00:00Z';

-- Changefeed with original data (for CDC patterns)
DEFINE TABLE orders CHANGEFEED 30d INCLUDE ORIGINAL;
```

---

## Best Practices

### SCHEMAFULL vs SCHEMALESS

- Use **SCHEMAFULL** when data integrity is paramount, for tables with well-known structures, user-facing data, and financial records. Every field must be defined before use. Provides compile-time-like safety for your data.
- Use **SCHEMALESS** for rapid prototyping, flexible metadata, log/event data, and when the schema is evolving frequently. Fields can be added without prior definition.
- Use **TYPE ANY** when a table may serve as both a normal document table and a graph edge table. Uncommon but useful in flexible schemas.
- Use **TYPE RELATION** for dedicated graph edge tables. Always specify `IN` and `OUT` types, and use `ENFORCED` to prevent edges from connecting incorrect record types.

### Transaction Patterns

```surql
-- Always wrap multi-step mutations in transactions
BEGIN TRANSACTION;
    LET $order = (CREATE order SET
        customer = $customer_id,
        total = $total,
        status = 'pending'
    );
    FOR $item IN $items {
        RELATE $order->contains->$item.product SET
            quantity = $item.qty,
            price = $item.price;
    };
    UPDATE customer:$customer_id SET last_order = time::now();
COMMIT TRANSACTION;
```

### Index Strategy

- Create indexes for fields used in `WHERE` clauses
- Use `UNIQUE` indexes for natural keys (email, username)
- Use full-text search indexes (`FULLTEXT ANALYZER`) for text search rather than substring matching
- Use HNSW indexes for vector similarity search (faster, approximate)
- For brute-force exact kNN without an index, use the `<|K,METRIC|>` operator (e.g. `vector <|2,EUCLIDEAN|> $query`)
- Composite indexes should list the most selective column first
- Avoid over-indexing: each index adds write overhead
- Use `EXPLAIN` to verify index usage in queries

### Query Optimization

- Use `SELECT VALUE` when you need a flat array of single values
- Use `FETCH` to resolve record links in a single query instead of multiple round trips
- Use `LIMIT` and `START` for pagination
- Prefer `PARALLEL` for large table scans
- Use `TIMEOUT` to prevent runaway queries
- Use computed table views for frequently-accessed aggregations
- Use record links instead of JOIN-style subqueries when possible
- Pre-filter with indexes, then apply complex logic in application code when needed

### Common Pitfalls

- Record IDs are case-sensitive: `person:Tobie` and `person:tobie` are different records
- `=` is a loose comparison; use `==` for strict type-matching comparison
- `CONTENT` replaces the entire record; use `MERGE` or `SET` for partial updates
- `array::add` prevents duplicates; `array::append` does not
- Datetime literals require the `d'...'` prefix: `d'2026-01-01T00:00:00Z'`
- Duration values do not use quotes: `1h30m` not `'1h30m'`
- `NONE` and `null` are distinct: `NONE` means "field absent", `null` means "field present with null value"
- `option<T>` allows `NONE` (field absent); it does not allow arbitrary types
- `RETURN NONE` suppresses output; omitting `RETURN` returns the affected records by default
- `DELETE table` deletes all records; `REMOVE TABLE table` removes the table definition entirely
- Graph edges created with `RELATE` are themselves records in a table; they can be queried directly
- Indexes cannot be created on computed fields (enforced since v3.0.1)
- Durations can be multiplied/divided by numbers and incremented/decremented (since v3.0.1)

---

## v3.0.1 Patch Notes (2026-02-24)

Key fixes and changes in SurrealDB v3.0.1:

- **Duration arithmetic**: Durations can now be multiplied and divided by numbers, and incremented/decremented like numbers (`1h * 2` = `2h`, `30m + 15m` = `45m`)
- **Computed field index prevention**: Creating indexes on computed fields is now correctly rejected (prevents silent index corruption)
- **Record ID dereference fix**: Record IDs are now properly dereferenced when a field is computed on them
- **Error serialization fix**: Error objects are correctly serialized across all protocols
- **GraphQL string enum fix**: String enum literals now work correctly in GraphQL queries
- **Root user permission fix**: Permission check conditions for root users are now evaluated correctly
- **Parallel index compaction**: Index compaction now runs in parallel across distinct indexes (performance improvement)
- **WASM compatibility**: Improved compatibility for embedded WASM deployments
- **RouterFactory trait**: New `RouterFactory` trait exposed for embedders to compose custom HTTP routers (advanced)

## v3.0.2 Patch Notes (2026-03-03)

Key fixes and changes in SurrealDB v3.0.2:

- **Non-existent record returns None** (#6978): `SELECT` on a record that does not exist now returns `NONE` instead of a confusing error. Code that catches errors on missing records should be updated to check for `NONE` instead.
- **Bind parameter resolution in MATCHES** (#6961): Bind parameters now correctly resolve in the `MATCHES (@N@)` operator and `search::score()` function
- **Datetime setter functions** (#6981): New functions to set individual parts of datetimes (year, month, day, hour, etc.)
- **Configurable CORS allow list** (#6998): `--allow-origins` flag now supports multiple origins for production CORS configuration
- **`--tables-exclude` flag** (#6999): New `surreal export --tables-exclude` flag to exclude specific tables from exports
- **Compound unique index fix** (#7002): Fixed compound unique indexing for multi-field unique constraints
- **DELETE live event permission fix** (#6992): Permission checks now correctly apply to DELETE events in live queries
- **DEFINE FUNCTION parsing fix** (#6987): Fixed parsing of `DEFINE FUNCTION` when loading from disk
- **Transaction timeout enforcement** (#6975): Transaction timeout is now correctly enforced for all queries
- **RecordIdKeyType::Object serialization** (#6977): Fixed serialization error for object-typed record ID keys
- **IndexAppending write-write conflicts** (#6982): Fixed write-write conflicts on `ip` keys during index appending
- **Executor optimizations** (#6995): New executor bug fixes and performance optimizations
- **SurrealValue for LinkedList/HashSet** (#6968): SDK embedders can now use `SurrealValue` with `LinkedList` and `HashSet` types

## v3.0.5 Patch Notes (2026-03-27)

Key fixes and changes in SurrealDB v3.0.5:

- **`REMOVE CONFIG` support** (#7108): configuration objects can now be removed through standard DDL instead of manual cleanup paths
- **`ALTER` coverage expanded** (#7126): `ALTER` support now applies across the statement surface instead of a narrow subset
- **Planner pushdown improvements** (#7076): plan-time resolution and `LIMIT` pushdown reduce wasted record scans in more query shapes
- **`$parent` fixes**: multiple fixes landed for `$parent` resolution in nested and edge-oriented queries
- **Computed field stability** (#7142, #7202): computed fields now evaluate more consistently in write and query paths
- **Edge query ordering fixes** (#7193, #7194): `ORDER BY` and related planning on edge-table queries behave correctly again
- **`encoding::*` registry verified (#7197)**: The v3.0.5
  `core/src/fnc/mod.rs` registry (lines 242-245) exposes exactly
  four `encoding::*` functions: `encoding::base64::{encode,decode}`
  and `encoding::cbor::{encode,decode}`. There is NO callable
  `encoding::json::*` function namespace in v3.0.5. Earlier wording
  in this section that said "encoding::json restored" was a
  v1.4.x-era doc fabrication. Cross-reference: see `### Encoding
  Functions` above for the full registered surface. Correction
  landed in v1.6.1 after a 4-WAY adversarial review pass.
- **GraphQL literal fields** (#7109): schema generation now supports literal fields in GraphQL mappings
- **Axum router support for embedders** (#7097): embedding use cases have an official axum router path
- **Validation input from stdin** (#7235): CLI validation flows now accept stdin input cleanly
- **Auth limits with `ALTER` fixed** (#7233): access-control edge cases introduced by broader `ALTER` support were corrected
- **Parser v3 work merged** (#6938): parser infrastructure continues moving toward the v3 line and unblocks later syntax work

### v3.1.4 Patch Notes (2026-06-10)

See `rules/gotchas.md` for a cross-domain gotcha catalog and
`rules/deployment.md` for the 3.0→3.1 upgrade guide. Key items:

- **Security:** array element-level SELECT permission leak fixed (GHSA-8rw6-p7m8-63jp)
- **Query:** `type::field('id') = record:…` uses record-id point lookup
- **Graph:** inline edge filters fixed in 3.1.3; `$parent` and single-scan traversals in 3.1.0
- **Vector:** DiskANN index type (64-bit only); same `<|K, EF|>` operator as HNSW
- **MCP:** built-in `surreal mcp` and HTTP `/mcp` (v3.1.0+)
- **ALTER:** full DEFINE counterparts (v3.1.0+); seven-target limit on v3.0.5 only

Full release notes: [surrealdb.com/releases/3.1](https://surrealdb.com/releases/3.1)
