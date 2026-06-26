---
name: schema-design-tooling
description: >-
  Best practices for Harper schema design, including core directives and GraphQL
  tooling configuration.
metadata:
  mode: generate
  sources:
    - reference/v5/database/schema.md#Overview
    - reference/v5/database/schema.md#Type Directives
    - reference/v5/database/schema.md#Field Directives
  sourceCommit: 4fe4c9c95e0974eaa77032f6f10e36fbd8ec64ac
  inputHash: 15b9c72decc1f05d
---

# Schema Design and GraphQL Tooling

Instructions for the agent to follow when designing Harper schemas, applying core directives, and configuring GraphQL tooling.

## When to Use

Apply this rule when creating or modifying Harper schema files, configuring `graphqlSchema` in `config.yaml`, or deciding which directives to apply to tables and fields. Use it any time a component needs tables, indexes, primary keys, or exported endpoints defined.

## How It Works

1. **Create a schema file** using standard GraphQL type definitions with Harper-specific directives. Name it (e.g., `schema.graphql`) and place it in your component directory.

2. **Register the schema** in the component's `config.yaml` using the `graphqlSchema` plugin:

   ```yaml
   graphqlSchema:
     files: 'schema.graphql'
   ```

   Both plugins and applications can specify schemas.

3. **Mark types as tables** with `@table`. The type name becomes the table name by default:

   ```graphql
   type Dog @table {
   	id: Long @primaryKey
   	name: String
   	breed: String
   	age: Int
   }
   ```

4. **Designate a primary key** with `@primaryKey` on exactly one field per type. Primary keys must be unique; duplicate-key inserts are rejected. If no primary key is provided on insert, Harper auto-generates one:
   - `String` or `ID` → UUID string
   - `Int`, `Long`, or `Any` → auto-incrementing integer

   Use `Long` or `Any` for auto-generated numeric keys; `Int` is 32-bit and may be insufficient for large tables.

5. **Add secondary indexes** with `@indexed` on any field that will be used for filtering in REST queries, SQL, or NoSQL operations:

   ```graphql
   type Breed @table {
   	id: Long @primaryKey
   	name: String @indexed
   }
   ```

   If the field value is an array, each element is individually indexed. Null values are indexed by default.

6. **Expose a table as an external endpoint** with `@export`. The optional `name` parameter sets the URL path segment:

   ```graphql
   type MyTable @table @export(name: "my-table") {
   	id: Long @primaryKey
   }
   ```

   Without `name`, the type name is used as the path segment.

7. **Configure `@table` arguments** as needed for database placement, expiration, eviction, and replication:

   | Argument       | Type      | Default                       | Description                                                   |
   | -------------- | --------- | ----------------------------- | ------------------------------------------------------------- |
   | `table`        | `String`  | type name                     | Override the table name                                       |
   | `database`     | `String`  | `"data"`                      | Database to place the table in                                |
   | `expiration`   | `Int`     | —                             | Seconds until a record goes stale                             |
   | `eviction`     | `Int`     | `0`                           | Additional seconds after `expiration` before physical removal |
   | `scanInterval` | `Int`     | `(expiration + eviction) / 4` | Seconds between eviction scans                                |
   | `replicate`    | `Boolean` | `true`                        | Enable replication of this table                              |

8. **Apply additional field directives** where needed:
   - `@createdTime` — auto-assigns Unix epoch milliseconds on record creation
   - `@updatedTime` — auto-assigns Unix epoch milliseconds on each update
   - `@embed(source: "fieldName", model: "modelName")` — computes an embedding vector on write; attribute type must be `[Float]`
   - `@hidden` — suppresses the field from MCP tool descriptors and OpenAPI documents (not an access-control mechanism)

9. **Restrict extra properties** with `@sealed` if records must not include properties beyond those declared:
   ```graphql
   type StrictRecord @table @sealed {
   	id: Long @primaryKey
   	name: String
   }
   ```

## Examples

**Minimal two-table schema:**

```graphql
type Dog @table {
	id: Long @primaryKey
	name: String
	breed: String
	age: Int
}

type Breed @table {
	id: Long @primaryKey
	name: String @indexed
}
```

**Table with expiration, eviction, and custom scan interval:**

```graphql
# Expire after 5 minutes, evict after 1 hour, scan every 10 minutes
type WeatherCache @table(expiration: 300, eviction: 3300, scanInterval: 600) {
	id: ID @primaryKey
	temperature: Float
}
```

**Exported table with timestamps and a hidden field:**

```graphql
type Customer @table @export(name: "customers") {
	id: Long @primaryKey
	name: String @indexed
	createdAt: Long @createdTime
	updatedAt: Long @updatedTime

	"""
	Internal — do not surface to external consumers.
	"""
	creditScore: Int @hidden
}
```

**Multiple `@table` argument combinations:**

```graphql
# Override table name
type Product @table(table: "products") {
	id: Long @primaryKey
}

# Place in a specific database
type Order @table(database: "commerce") {
	id: Long @primaryKey
}

# Auto-expire records after 1 hour
type Session @table(expiration: 3600) {
	id: Long @primaryKey
	userId: String
}

# Disable replication
type LocalRecord @table(replicate: false) {
	id: Long @primaryKey
	value: String
}

# Combine multiple arguments
type Event @table(database: "analytics", expiration: 86400) {
	id: Long @primaryKey
	name: String @indexed
}
```

## Notes

- All tables default to the `"data"` database. When designing plugins or applications, use unique database names to avoid table naming collisions.
- Schemas are flexible by default — records may include properties beyond those declared. Use `@sealed` to prevent this.
- `expiration` marks a record stale; `eviction` controls how long after expiration the record is physically removed. Eviction does not remove records from secondary indexes — Harper fetches the full record on demand if an evicted record matches a query.
- `scanInterval` is clock-aligned to the server's local timezone, not startup-aligned. The eviction schedule is deterministic across restarts.
- If replication is disabled on a table and later re-enabled, writes made during the disabled period are not replicated retroactively.
- `@hidden` (on types or fields) is a metadata-visibility directive only. Use `attribute_permissions` on roles to enforce data access control.
- Disabling replication (`replicate: false`) and re-enabling it later will not catch up on writes made while replication was disabled.
