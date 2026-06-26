# MySQL to Go Type Mappings

## Common MySQL Types to Go Types

| MySQL Type | Go Type | Notes |
|------------|---------|-------|
| `TINYINT` | `int8` | Signed: -128 to 127 |
| `TINYINT UNSIGNED` | `uint8` | 0 to 255 |
| `SMALLINT` | `int16` | |
| `SMALLINT UNSIGNED` | `uint16` | |
| `INT` / `INTEGER` | `int` | |
| `INT UNSIGNED` | `uint` | |
| `BIGINT` | `int64` | |
| `BIGINT UNSIGNED` | `uint64` | |
| `FLOAT` | `float32` | |
| `DOUBLE` | `float64` | |
| `DECIMAL` / `NUMERIC` | `float64` | Or use custom type for precision |
| `BIT` | `bool` | BIT(1) |
| `BIT(1-64)` | `uint64` | For > 1 bit |

## String Types

| MySQL Type | Go Type | Notes |
|------------|---------|-------|
| `CHAR` | `string` | Fixed length |
| `VARCHAR` | `string` | Variable length |
| `TEXT` | `string` | |
| `TINYTEXT` | `string` | |
| `MEDIUMTEXT` | `string` | |
| `LONGTEXT` | `string` | |
| `ENUM` | `string` | Or custom enum type |

## Date/Time Types

| MySQL Type | Go Type | Notes |
|------------|---------|-------|
| `DATE` | `time.Time` | |
| `DATETIME` | `time.Time` | |
| `TIMESTAMP` | `time.Time` | |
| `TIME` | `time.Time` | |
| `YEAR` | `int` | |

## Binary Types

| MySQL Type | Go Type | Notes |
|------------|---------|-------|
| `BINARY` | `[]byte` | Fixed length |
| `VARBINARY` | `[]byte` | Variable length |
| `BLOB` | `[]byte` | |
| `TINYBLOB` | `[]byte` | |
| `MEDIUMBLOB` | `[]byte` | |
| `LONGBLOB` | `[]byte` | |

## JSON Types

| MySQL Type | Go Type | Notes |
|------------|---------|-------|
| `JSON` | `string` | Or `json.RawMessage` |

## Special Handling

### NULL Columns
- For nullable columns, use pointer types: `*int`, `*string`, `*time.Time`
- Xorm `nullable` option should be set

### Primary Key
- Add xorm tag: `pk`
- Auto increment: `pk autoincr`

### Unique Columns
- Add xorm tag: `unique`

### Default Values
- Add xorm tag: `default 'value'`

### Indexes
- Add xorm tag: `index`
- Composite index: `index idx_name`

## Column Name Conversion

MySQL `snake_case` column names are converted to Go `CamelCase` field names:
- `user_name` → `UserName`
- `created_at` → `CreatedAt`
- `id` → `ID` (special case)
- `url` → `URL` (special case)
- `user_id` → `UserID`

Common acronyms should be uppercase:
- `id` → `ID`
- `url` → `URL`
- `uri` → `URI`
- `http` → `HTTP`
- `https` → `HTTPS`
- `api_key` → `APIKey`
- `ip_address` → `IPAddress`
