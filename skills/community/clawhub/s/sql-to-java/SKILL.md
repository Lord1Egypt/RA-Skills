---
name: sql-to-java-entity
description: Convert MySQL CREATE TABLE statements to Java entity classes following framework conventions. Use when converting SQL DDL to Java entity definitions, generating ORM models from database schemas, or creating JPA/MyBatis-Plus entity classes from MySQL tables. Supports MySQL to Java type mapping, snake_case to camelCase conversion, and automatic annotation generation with MyBatis-Plus and JPA annotations.
---

# SQL to Java Entity

## Quick Start

Convert a MySQL CREATE TABLE statement to a Java entity class:

1. Parse the CREATE TABLE statement to extract table name, columns, and constraints
2. Map each MySQL column type to corresponding Java type
3. Convert snake_case column names to camelCase field names
4. Generate entity class with `@TableName`, `@TableId`, and JPA annotations
5. Generate getter/setter methods

## Configuration

Before generating the entity class, determine the following:

- **Package name**: Ask the user for the target package (e.g., `com.example.entity`)
- **Base class**: Ask if the entity should extend a base class
- **Annotation style**: Confirm whether to use MyBatis-Plus annotations (default) or JPA annotations

If the user doesn't specify, use sensible defaults based on the project context.

## Type Mapping

For complete MySQL to Java type mappings, see [type_mappings.md](references/type_mappings.md).

### Quick Reference

| MySQL | Java | Notes                   |
|-------|------|-------------------------|
| `INT` | `Integer` |                         |
| `BIGINT` | `Long` |                         |
| `VARCHAR` | `String` |                         |
| `TEXT` | `String` |                         |
| `DATETIME` | `LocalDateTime` | java.time.LocalDateTime |
| `TIMESTAMP` | `LocalDateTime` | java.time.LocalDateTime |
| `TINYINT(1)` | `Integer` |                         |
| `DECIMAL` | `BigDecimal` | java.math.BigDecimal |

## Column Name Conversion

Convert `snake_case` to `camelCase`:

```
user_name    → userName
created_at   → createdAt
user_id      → userId
is_active    → isActive
```

Class name conversion (PascalCase):
```
user_info    → UserInfo
order_detail → OrderDetail
```

## Annotation Generation

### MyBatis-Plus Annotations

| Constraint | Annotation |
|------------|-----------|
| Table name | `@TableName("table_name")` |
| Primary key | `@TableId(type = IdType.AUTO)` |
| Column name | `@TableField("column_name")` (only if different from field name) |
| Not mapped | `@TableField(exist = false)` |

### JPA Annotations (if needed)

| Constraint | Annotation |
|------------|-----------|
| Primary key | `@Id` |
| Auto increment | `@GeneratedValue(strategy = GenerationType.IDENTITY)` |
| Column name | `@Column(name = "column_name")` |
| Not null | `@Column(nullable = false)` |
| Unique | `@Column(unique = true)` |
| Length | `@Column(length = 50)` |

## Example

### Input

```sql
CREATE TABLE `user_info` (
    `id` bigint unsigned NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL,
    `age` int DEFAULT NULL,
    `email` varchar(100) NOT NULL,
    `salary` decimal(10,2) DEFAULT NULL,
    `description` text,
    `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
    `is_active` tinyint(1) DEFAULT '1',
    PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='User Table';
```

### Output

```java
package com.example.model;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@TableName("user_info")
public class UserInfo {

    @TableId(type = IdType.AUTO)
    private Long id;

    private String name;

    private Integer age;

    private String email;

    private BigDecimal salary;

    private String description;

    private LocalDateTime createdAt;

    private Integer isActive;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public BigDecimal getSalary() {
        return salary;
    }

    public void setSalary(BigDecimal salary) {
        this.salary = salary;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public LocalDateTime getCreatedAt() {
        return createdAt;
    }

    public void setCreatedAt(LocalDateTime createdAt) {
        this.createdAt = createdAt;
    }

    public Integer getIsActive() {
        return isActive;
    }

    public void setIsActive(Integer isActive) {
        this.isActive = isActive;
    }
}
```

## Workflow

1. **Extract table info**: Get table name, column definitions, constraints, comment
2. **Apply type mappings**: See [type_mappings.md](references/type_mappings.md) for reference
3. **Generate class name**: Convert snake_case table name to PascalCase
4. **Generate field names**: Convert snake_case columns to camelCase
5. **Add annotations**: Generate @TableName, @TableId, @TableField based on column attributes
6. **Generate getters/setters**: Create standard getter and setter methods
7. **Add imports**: Include necessary imports for types and annotations

## Package Structure

Entity classes should be placed in a package specified by the user. Common conventions:

- **Generic project**: `com.{company}.{module}.entity` or `com.{company}.{module}.model`

## Class Comment

Use table comment as class comment:
```java
/**
 * User Table
 */
@TableName("user_info")
public class UserInfo extends EntityBean {
}
```

## Base Class

The entity may extend a framework base class if required:

- **Framework**: May extend `BaseEntity`, `AbstractEntity`, or no base class


## Primary Key Strategy

| MySQL Column Definition | IdType |
|------------------------|--------|
| AUTO_INCREMENT | `IdType.AUTO` |
| Manual assignment | `IdType.INPUT` |
| UUID | `IdType.ASSIGN_UUID` |
| Snowflake algorithm | `IdType.ASSIGN_ID` |

## Nullable Columns

For nullable columns (allows NULL), use wrapper types:
- `Integer` instead of `int`
- `Long` instead of `long`
- `Boolean` instead of `boolean`

## Important Notes

1. Always use wrapper types (`Integer`, `Long`, `Boolean`) for nullable columns
2. Use `BigDecimal` for DECIMAL/NUMERIC types to maintain precision
3. Use `LocalDateTime` for DATETIME/TIMESTAMP types
4. Table name in `@TableName` should match the actual database table name exactly
5. The `id` field should use `IdType.AUTO` for auto-increment columns
6. Generate complete getter/setter methods for all fields
7. Follow framework conventions and package structure
