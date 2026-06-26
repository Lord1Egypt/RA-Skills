# MySQL to Java Type Mappings

## Numeric Types

| MySQL Type | Java Type | Notes |
|------------|-----------|-------|
| `TINYINT` | `Integer` | Signed: -128 to 127 |
| `TINYINT UNSIGNED` | `Integer` | 0 to 255 |
| `SMALLINT` | `Integer` | |
| `SMALLINT UNSIGNED` | `Integer` | |
| `INT` / `INTEGER` | `Integer` | |
| `INT UNSIGNED` | `Long` | To avoid overflow |
| `BIGINT` | `Long` | |
| `BIGINT UNSIGNED` | `Long` | May need BigInteger for very large values |
| `FLOAT` | `Float` | |
| `DOUBLE` | `Double` | |
| `DECIMAL` / `NUMERIC` | `BigDecimal` | Use for precision-critical values |

## String Types

| MySQL Type | Java Type | Notes |
|------------|-----------|-------|
| `CHAR` | `String` | Fixed length |
| `VARCHAR` | `String` | Variable length |
| `TEXT` | `String` | |
| `TINYTEXT` | `String` | |
| `MEDIUMTEXT` | `String` | |
| `LONGTEXT` | `String` | |
| `ENUM` | `String` | Or Java enum type |

## Date/Time Types

| MySQL Type | Java Type | Notes |
|------------|-----------|-------|
| `DATE` | `LocalDate` | Date only |
| `DATETIME` | `LocalDateTime` | Date and time |
| `TIMESTAMP` | `LocalDateTime` | Timestamp |
| `TIME` | `LocalTime` | Time only |
| `YEAR` | `Integer` | |

## Binary Types

| MySQL Type | Java Type | Notes |
|------------|-----------|-------|
| `BINARY` | `byte[]` | Fixed length |
| `VARBINARY` | `byte[]` | Variable length |
| `BLOB` | `byte[]` | Or `Blob` type |
| `TINYBLOB` | `byte[]` | |
| `MEDIUMBLOB` | `byte[]` | |
| `LONGBLOB` | `byte[]` | |

## Boolean Types

| MySQL Type | Java Type | Notes |
|------------|-----------|-------|
| `BIT(1)` | `Boolean` | |
| `TINYINT(1)` | `Integer` | 0/1 flag, not true boolean |
| `BOOLEAN` | `Boolean` | |

## JSON Types

| MySQL Type | Java Type | Notes |
|------------|-----------|-------|
| `JSON` | `String` | Or custom object with JSON parser |

## Special Handling

### NULL Columns
- For nullable columns, always use wrapper types: `Integer`, `Long`, `Boolean`, etc.
- Never use primitive types (`int`, `long`, `boolean`) for nullable columns
- This allows null values to be properly represented

### Primary Key
- Use `Long` or `Integer` based on the column type
- Add `@TableId` annotation with appropriate `IdType`
- Auto increment: `@TableId(type = IdType.AUTO)`
- Manual input: `@TableId(type = IdType.INPUT)`

### Decimal/Precision Types
- Always use `BigDecimal` for DECIMAL and NUMERIC types
- Never use `Double` or `Float` for monetary values
- Import: `java.math.BigDecimal`

### Date/Time Types
- Use Java 8 Time API: `LocalDateTime`, `LocalDate`, `LocalTime`
- Import from `java.time` package
- Avoid legacy `java.util.Date` and `java.sql.Timestamp`

## Column Name Conversion

MySQL `snake_case` column names are converted to Java `camelCase` field names:
- `user_name` → `userName`
- `created_at` → `createdAt`
- `id` → `id`
- `url` → `url`
- `user_id` → `userId`

Class names use `PascalCase`:
- `user_info` → `UserInfo`
- `order_detail` → `OrderDetail`
- `sys_user_role` → `SysUserRole`

## Common Imports

```java
// MyBatis-Plus annotations
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import com.baomidou.mybatisplus.annotation.TableField;

// Java types
import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.time.LocalDate;
import java.time.LocalTime;
```

## Type Selection Guidelines

1. **Use wrapper types** (`Integer`, `Long`, `Boolean`) for all fields that can be NULL
2. **Use `BigDecimal`** for any DECIMAL/NUMERIC type, especially for currency
3. **Use `LocalDateTime`** for DATETIME and TIMESTAMP columns
4. **Use `String`** for all text-based types (VARCHAR, TEXT, etc.)
5. **Use `byte[]`** for binary data (BLOB, BINARY, etc.)
6. **Consider `Long` for INT UNSIGNED** to prevent overflow issues
