---
name: sql-to-go
description: Convert MySQL CREATE TABLE statements to Go structs with form, json, and xorm tags. Use when converting SQL DDL to Go struct definitions, generating ORM models from database schemas, or creating Go types from MySQL tables. Supports MySQL data type mapping, snake_case to CamelCase conversion, and automatic tag generation.
---

# SQL to Go Struct

## Quick Start

Convert a MySQL CREATE TABLE statement to a Go struct with tags:

1. Parse the CREATE TABLE statement to extract table name, columns, and constraints
2. Map each MySQL column type to corresponding Go type
3. Convert snake_case column names to CamelCase field names
4. Generate struct with `form`, `json`, and `xorm` tags

## Type Mapping

For complete MySQL to Go type mappings, see [type_mappings.md](references/type_mappings.md).

### Quick Reference

| MySQL | Go | Notes |
|-------|-----|-------|
| `INT` | `int` | |
| `BIGINT` | `int64` | |
| `VARCHAR` | `string` | |
| `TEXT` | `string` | |
| `DATETIME` | `time.Time` | |
| `TIMESTAMP` | `time.Time` | |
| `BOOL` / `BIT(1)` | `bool` | |
| `DECIMAL` | `float64` | Or custom type |

## Column Name Conversion

Convert `snake_case` to `CamelCase`:

```
user_name    → UserName
created_at   → CreatedAt
user_id      → UserID
api_key      → APIKey
is_active    → IsActive
```

Special cases - acronyms remain uppercase:
- `id` → `ID`
- `url` → `URL`
- `uri` → `URI`

## Tag Generation

Generate three tags for each field:

- **`form`**: HTTP form parameter name (snake_case)
- **`json`**: JSON field name (snake_case)
- **`xorm`**: XORM ORM column name and constraints

### XORM Tag Patterns

| Constraint | Tag |
|------------|-----|
| Primary key | `xorm:"pk"` |
| Auto increment | `xorm:"autoincr"` |
| Not null | `xorm:"not null"` |
| Unique | `xorm:"unique"` |
| Default value | `xorm:"default 'value'"` |
| Nullable | `xorm:"nullable"` |
| Index | `xorm:"index"` |
| Comment | `xorm:"comment 'text'"` |

Combine constraints: `xorm:"'user_id' pk autoincr"`

## Example

### Input

```sql
CREATE TABLE users (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL,
    age INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    bio TEXT
) COMMENT='User table';
```

### Output

```go
package models

import "time"

// User represents the users table
type User struct {
    ID        uint64    `form:"id" json:"id" xorm:"'id' pk autoincr"`
    Username  string    `form:"username" json:"username" xorm:"'username' unique not null"`
    Email     string    `form:"email" json:"email" xorm:"'email' not null"`
    Age       int       `form:"age" json:"age" xorm:"'age' default 0"`
    CreatedAt time.Time `form:"created_at" json:"created_at" xorm:"'created_at'"`
    IsActive  bool      `form:"is_active" json:"is_active" xorm:"'is_active' default true"`
    Bio       string    `form:"bio" json:"bio" xorm:"'bio'"`
}
```

## Workflow

1. **Extract table info**: Get table name, column definitions, constraints
2. **Apply type mappings**: See [type_mappings.md](references/type_mappings.md) for reference
3. **Generate field name**: Convert snake_case column to CamelCase
4. **Add tags**: Generate form/json/xorm tags based on column attributes
5. **Handle special cases**: Primary keys, indexes, defaults, comments

## Nullable Columns

For nullable columns (allows NULL), use pointer types:

```go
// MySQL: phone VARCHAR(20) NULL
Phone *string `form:"phone" json:"phone" xorm:"'phone' nullable"`
```

## Struct Comment

Use table comment as struct comment, or generate from table name:

```go
// User represents the users table
```
