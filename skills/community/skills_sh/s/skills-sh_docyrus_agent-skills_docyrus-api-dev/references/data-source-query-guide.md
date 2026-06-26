# Data Source Query Guide

Comprehensive reference for querying data sources using the `ZodSelectQueryPayload` schema. This document covers every parameter, operator, and feature with detailed examples.

---

## Table of Contents

1. [Overview](#overview)
2. [Query Payload Structure](#query-payload-structure)
3. [Common Parameters](#common-parameters)
4. [Columns](#columns)
5. [Filters](#filters)
6. [Filter Keyword](#filter-keyword)
7. [Order By](#order-by)
8. [Pagination (limit / offset)](#pagination)
9. [Calculations (Aggregations)](#calculations)
10. [Formulas](#formulas)
11. [Pivot](#pivot)
12. [Child Queries](#child-queries)
13. [Expand](#expand)
14. [Query Mode](#query-mode)
15. [Distinct Columns](#distinct-columns)
16. [Full Count](#full-count)
17. [Cursor-Based Sync](#cursor-based-sync)
18. [Filter Operators Reference](#filter-operators-reference)
19. [Allowed Functions Reference](#allowed-functions-reference)
20. [Allowed Aggregates Reference](#allowed-aggregates-reference)
21. [Allowed Cast Types](#allowed-cast-types)
22. [Complete Examples](#complete-examples)

---

## Overview

All data source reads go through a unified select query payload. The payload is validated by `ZodSelectQueryPayload` (defined in `libs/shared/src/database/schemas.ts`). It supports:

- **Column selection** with relation expansion, aliasing, spread, and functions
- **Filtering** with nested AND/OR groups, dozens of operators, and relation field filtering
- **Keyword search** via full-text search
- **Sorting** by one or more fields with direction
- **Pagination** with limit/offset
- **Aggregations** (count, sum, avg, min, max, etc.) with grouping
- **Formulas** — computed virtual columns (block/AST-based)
- **Pivot** — advanced cross-tab grouping with date range series and matrix CTEs
- **Child queries** — fetch related child records as nested JSON arrays
- **Field expansion** — automatically expand relation/user/enum fields

---

## Query Payload Structure

The full `ZodSelectQueryPayload` type:

```typescript
interface ISelectQueryParams {
  // --- Identity ---
  dataSourceId?: string | null;
  dataSourceFullSlug?: string | null;
  connectionId?: string | null;
  connectionAccountId?: string | null;
  parentRecord?: Record<string, any> | null;

  // --- Filtering ---
  filters?: IQueryFilterGroup | null;
  filterKeyword?: string | null;

  // --- Column Selection ---
  columns?: string | null;
  distinctColumns?: string[] | null;

  // --- Computed Columns ---
  formulas?: Record<string, ISelectQueryFormula> | null;

  // --- Aggregation ---
  calculations?: ISelectQueryCalculationRule[] | null;
  groupSummaries?: boolean;

  // --- Sorting ---
  orderBy?: string | ISelectQueryOrderBy | ISelectQueryOrderBy[];

  // --- Pagination ---
  limit?: number;   // default: 100
  offset?: number;  // default: 0

  // --- Expansion ---
  expandTypes?: ("user" | "enum" | "relation")[] | null;
  expand?: string[] | null;

  // --- Misc ---
  queryMode?: "OLTP" | "OLAP" | "EXPORT";
  fullCount?: boolean;
  cursorDateStart?: string | null;
  cursorDateEnd?: string | null;

  // --- Advanced ---
  childQueries?: ISelectQueryChildQueryParams[] | null;
  pivot?: {
    matrix: ISelectPivotMatrixQuery[];
    hideEmptyRows?: boolean;
    orderBy?: string | ISelectQueryOrderBy | ISelectQueryOrderBy[];
    limit?: number;
  } | null;
}
```

---

## Common Parameters

These parameters identify which data source to query.

| Parameter | Type | Description |
|---|---|---|
| `dataSourceId` | `string \| null` | UUID of the data source |
| `dataSourceFullSlug` | `string \| null` | Full slug in `appSlug_slug` format (e.g. `crm_account`) |
| `connectionId` | `string \| null` | Connection ID for external data sources |
| `connectionAccountId` | `string \| null` | Account ID for the connection |
| `parentRecord` | `object \| null` | Parent record context for relation/formula resolution |

> **Note:** You need either `dataSourceId` or `dataSourceFullSlug` to identify the target data source.

---

## Columns

**Parameter:** `columns` — `string | null`

Use a comma-separated list of field slugs to select specific columns.

### Rules

- Use `()` to select specific columns from a related record (`field-relation`, `field-select`, `field-userSelect` type fields).
- Use `...` (spread operator) to flatten related columns into the root object. **Always flatten related columns when fetching data for charts** to avoid object nesting and parsing overhead.
- Use `:` to alias a column. The alias goes on the left side (e.g. `tn:task_name`).
- Use `@` to apply a pre-defined function. **Always use with an alias** (e.g. `name:upper@account_name`).
- **Do not** use aggregation functions (count, sum, etc.) via `@` syntax — use `calculations` instead.

### Basic Selection

```
"columns": "task_name, created_on, record_owner"
```

### Aliasing with `:`

Use `:` to give a column an alias (shorter name in the result).

```
"columns": "ra:related_account"
```

**Result:**

```json
[
  {
    "ra": {
      "id": "uuid",
      "name": "account name"
    }
  }
]
```

### Relation Expansion with `()`

Use parentheses to select specific columns from a related record. Works with `field-relation`, `field-select`, and `field-userSelect` type fields.

```
"columns": "task_name, related_account(name:account_name, phone:account_phone)"
```

**Result:**

```json
[
  {
    "task_name": "Task Name",
    "related_account": {
      "name": "Account Name",
      "phone": "05556668899"
    }
  }
]
```

### Spread Operator `...`

Use the spread operator to flatten selected columns from a related record into the root object (no nesting).

```
"columns": "task_name, ...related_account(account_name, phone:account_phone)"
```

**Result:**

```json
[
  {
    "task_name": "Task Name",
    "account_name": "Account Name",
    "phone": "05556668899"
  }
]
```

### Functions with `@`

Use `@` to apply a pre-defined function to a column, specified as `<function>@<field>`.

```
"columns": "task_name, ...related_account(an:upper@account_name, ap:account_phone)"
```

**Result:**

```json
[
  {
    "task_name": "Task Name",
    "an": "ACCOUNT NAME",
    "ap": "05556668899"
  }
]
```

### Special Date/DateTime Formulas for Aggregations

Use the `@` symbol with special date formulas to format date intervals. These are typically used with a date interval filter to group data for a specific period. Values outside the current period are grouped as `"OLDER"` and `"UPCOMING"`.

**Format:** `<formula>@<date_or_datetime_field>`

| Formula | Description | Example |
| ------- | ----------- | ------- |
| `hours_of_today` | Groups by hour for today | `hours_of_today@created_on` |
| `days_of_week` | Groups by day for the current week | `days_of_week@created_on` |
| `days_of_month` | Groups by day for the current month | `days_of_month@created_on` |
| `weeks_of_month` | Groups by week number for the current month | `weeks_of_month@created_on` |
| `weeks_of_quarter` | Groups by week number for the current quarter | `weeks_of_quarter@created_on` |
| `months_of_quarter` | Groups by month for the current quarter | `months_of_quarter@created_on` |
| `months_of_year` | Groups by month for the current year (YYYY-MM) | `months_of_year@created_on` |
| `quarters_of_year` | Groups by quarter for the current year (YYYY-Q) | `quarters_of_year@created_on` |

### Column Syntax with `to_char` Function

Use `to_char` with brackets `[]` for date formatting:

```
"columns": "day:to_char[DD/MM/YYYY]@created_on"
```

This formats the `created_on` field as `DD/MM/YYYY` and aliases it as `day`.

---

## Filters

**Parameter:** `filters` — `IQueryFilterGroup | null`

Filters use a recursive group structure with combinators (`and` / `or`) and rules.

> **Tip:** If you are asked to find records that contain a specific string, prefer using `filterKeyword` instead of `filters` for that filter. `filterKeyword` performs full-text search across all searchable fields.

### Filter Group Structure

```typescript
interface IQueryFilterGroup {
  rules: (IQueryFilterRule | IQueryFilterGroup)[];
  combinator?: "and" | "or";  // default: "and"
  not?: boolean;               // negate the entire group
}

interface IQueryFilterRule {
  field?: string;
  operator: IFilterOperator;
  value?: any;
  filterType?: QueryFilterType | null;
}
```

### Filter Types (for value casting)

| FilterType | Use For |
|---|---|
| `NUMERIC` | Number fields |
| `ALPHA` | Text/string fields |
| `BOOL` | Boolean fields |
| `DATE` | Date fields |
| `TIME` | Time fields |
| `DATETIME` | DateTime fields |
| `MULTISELECT` | Multi-select fields |
| `LIST` | List fields |
| `RELATION` | Relation fields |
| `OWNER` | Owner/user fields |
| `FOLLOWER` | Follower fields |
| `APPROVAL` | Approval fields |

### Example: Basic AND Filter

```json
{
  "filters": {
    "combinator": "and",
    "rules": [
      {
        "field": "task_status",
        "operator": "=",
        "value": 1
      },
      {
        "field": "priority",
        "operator": ">=",
        "value": 3
      }
    ]
  }
}
```

### Example: Nested AND + OR

Filter records created between two dates, AND where either email is empty OR phone is not empty:

```json
{
  "filters": {
    "combinator": "and",
    "rules": [
      {
        "field": "created_on",
        "operator": "between",
        "value": ["2025-10-01", "2025-11-01"]
      },
      {
        "combinator": "or",
        "rules": [
          {
            "field": "email",
            "operator": "empty"
          },
          {
            "field": "phone",
            "operator": "not empty"
          }
        ]
      }
    ]
  }
}
```

### Example: Filtering by Related Record's Field (String Match)

Use `filterKeyword` when searching for a specific substring across all searchable fields:

```json
{
  "filterKeyword": "John",
  "columns": "id, name, email"
}
```

Alternatively, use `rel_{{relation_field_slug}}/{{field_slug}}` with `like` operator to filter by a specific related field:

```json
{
  "filters": {
    "combinator": "and",
    "rules": [
      {
        "field": "rel_client/name",
        "operator": "like",
        "value": "John"
      }
    ]
  }
}
```

### Example: Filtering by Related Record's Field

Use the `rel_{{relation_field_slug}}/{{field_slug}}` syntax to filter by a parent/related table's field:

```json
{
  "filters": {
    "combinator": "and",
    "rules": [
      {
        "field": "task_status",
        "operator": "in",
        "value": [1, 2, 3]
      },
      {
        "field": "rel_client/account_status",
        "operator": "=",
        "value": 2
      }
    ]
  }
}
```

### Example: Negated Filter Group

```json
{
  "filters": {
    "combinator": "and",
    "not": true,
    "rules": [
      {
        "field": "status",
        "operator": "=",
        "value": "archived"
      }
    ]
  }
}
```

### Example: Date Shortcut Operators

```json
{
  "filters": {
    "rules": [
      {
        "field": "created_on",
        "operator": "this_month"
      }
    ]
  }
}
```

### Example: User-Related Operators

```json
{
  "filters": {
    "rules": [
      {
        "field": "record_owner",
        "operator": "active_user"
      }
    ]
  }
}
```

### Example: X Days Operators

```json
{
  "filters": {
    "rules": [
      {
        "field": "due_date",
        "operator": "in_next_x_days",
        "value": 7
      }
    ]
  }
}
```

---

## Filter Keyword

**Parameter:** `filterKeyword` — `string | null`

Performs a full-text search across all searchable fields.

```json
{
  "filterKeyword": "John Doe",
  "columns": "id, name, email"
}
```

---

## Order By

**Parameter:** `orderBy` — `string | ISelectQueryOrderBy | ISelectQueryOrderBy[]`

Use comma-separated field and direction pairs to sort data.

### String Format

```json
{
  "orderBy": "created_on DESC"
}
```

Multiple fields:

```json
{
  "orderBy": "firstname ASC, lastname DESC"
}
```

### Object Format

```json
{
  "orderBy": {
    "field": "created_on",
    "direction": "desc"
  }
}
```

### Array Format

```json
{
  "orderBy": [
    { "field": "firstname", "direction": "asc" },
    { "field": "lastname", "direction": "desc" }
  ]
}
```

### Sorting by Related Field

Use parentheses to sort by a field of a related table:

```json
{
  "orderBy": "relation_field_slug(field_name DESC), id ASC"
}
```

---

## Pagination

### `limit`

**Type:** `number` (positive integer)
**Default:** `100`

Maximum number of records to return.

### `offset`

**Type:** `number` (non-negative integer)
**Default:** `0`

Number of records to skip for pagination.

### Example

```json
{
  "columns": "id, name",
  "limit": 25,
  "offset": 50,
  "orderBy": "created_on DESC"
}
```

This fetches records 51–75 (page 3 with 25 per page).

---

## Calculations

**Parameter:** `calculations` — `ISelectQueryCalculationRule[] | null`

Use calculations to group and aggregate data.

### Calculation Rule Structure

```typescript
interface ISelectQueryCalculationRule {
  func: string;        // "count" | "sum" | "avg" | "min" | "max" | "jsonb_agg" | "json_agg" | "array_agg"
  field: string;       // field/column to aggregate
  name?: string;       // alias for the result column
  isDistinct?: boolean; // aggregate unique values only (default: false)
  minValue?: number;   // aggregate values greater than this
  maxValue?: number;   // aggregate values less than this
  numberType?: "bigint" | "int" | "decimal"; // result number type
}
```

### Rules

- Always use the `id` field for counting records.
- Use the aggregated field's slug for other functions (sum, avg, etc.).
- Skip `numberType` unless it is specifically required.
- Use `name` to alias the calculation result column (keep it short).
- **Do not** use `distinctColumns` together with `calculations`. Prefer `calculations` to aggregate data.

### Example: Count per Group

Count open tasks per user:

```json
{
  "columns": "record_owner(name)",
  "calculations": [
    {
      "field": "id",
      "func": "count",
      "name": "count_of_open_tasks"
    }
  ],
  "filters": {
    "combinator": "and",
    "rules": [
      {
        "field": "task_status",
        "operator": "=",
        "value": 1
      }
    ]
  }
}
```

**Result:**

```json
[
  {
    "record_owner": {
      "name": "User Name"
    },
    "count_of_open_tasks": 10
  }
]
```

### Example: Distinct Count

Count unique emails:

```json
{
  "calculations": [
    {
      "field": "email",
      "func": "count",
      "name": "unique_emails",
      "isDistinct": true
    }
  ]
}
```

**Result:**

```json
[
  {
    "unique_emails": 10
  }
]
```

### Example: Multiple Aggregations

```json
{
  "columns": "category",
  "calculations": [
    {
      "field": "id",
      "func": "count",
      "name": "total"
    },
    {
      "field": "amount",
      "func": "sum",
      "name": "totalAmount"
    },
    {
      "field": "amount",
      "func": "avg",
      "name": "avgAmount"
    },
    {
      "field": "amount",
      "func": "min",
      "name": "minAmount"
    },
    {
      "field": "amount",
      "func": "max",
      "name": "maxAmount"
    }
  ]
}
```

### `groupSummaries`

**Type:** `boolean`
**Default:** `false`

When `true` and aggregation is used, includes group summary rows in the output.

---

## Formulas

**Parameter:** `formulas` — `Record<string, ISelectQueryFormula> | null`

Formulas are virtual computed columns injected into `SELECT` queries at build time. Keys are the formula names (used as column aliases), values are formula definitions.

There are two block formula formats:

### 1. Block Inline Formula

AST-based formula that compiles to an inline SQL expression. Uses a block tree with `kind` discriminator.

```typescript
interface IQueryBlockInlineFormulaSchema {
  alias?: string;
  inputs: IQueryFormulaBlock[];  // exactly 1 root block
}
```

**Example: Simple Division**

```json
{
  "columns": "id, name, basic_formula",
  "formulas": {
    "basic_formula": {
      "inputs": [{
        "kind": "math",
        "op": "/",
        "inputs": [
          { "kind": "column", "name": "balance" },
          { "kind": "literal", "literal": 100 }
        ]
      }]
    }
  }
}
```

> SQL: `("t0"."balance" / $1) as "basic_formula"`

### 2. Block Subquery Formula

Compiles to a correlated subquery against a child data source.

```typescript
interface IQueryBlockSubqueryFormulaSchema {
  alias?: string;
  inputs: IQueryFormulaBlock[];
  from: string;                           // child table full slug
  with: string | Record<string, string>;  // join condition(s)
  filters?: IQueryFilterGroup;
}
```

**Example: Count Child Records**

```json
{
  "columns": "id, name, children_count",
  "formulas": {
    "children_count": {
      "from": "app_child_table",
      "with": "parent_field",
      "inputs": [{
        "kind": "aggregate",
        "name": "count",
        "inputs": []
      }]
    }
  }
}
```

> SQL: `(SELECT count(*) FROM "schema"."child_table" AS "t0_child" WHERE "t0_child"."parent_field" = "t0"."id") AS "children_count"`

**Example: Subquery with Filters**

```json
{
  "formulas": {
    "active_children": {
      "from": "app_child_table",
      "with": "parent_id",
      "filters": {
        "rules": [
          { "field": "status", "operator": "=", "value": "active" }
        ]
      },
      "inputs": [{
        "kind": "aggregate",
        "name": "count",
        "inputs": []
      }]
    }
  }
}
```

**Example: Multi-Field Subquery Join**

```json
{
  "formulas": {
    "related_sum": {
      "from": "app_child",
      "with": {
        "child_field1": "parent_field1",
        "child_field2": "parent_field2"
      },
      "inputs": [{
        "kind": "aggregate",
        "name": "sum",
        "inputs": [{ "kind": "column", "name": "amount" }]
      }]
    }
  }
}
```

**Example: Compatibility Wrapper**

Block subquery formulas can also be wrapped under an `expression` key:

```json
{
  "formulas": {
    "children_count": {
      "from": "app_child_table",
      "with": "parent_field",
      "inputs": [{
        "kind": "aggregate",
        "name": "count",
        "distinct": true,
        "inputs": [{ "kind": "column", "name": "id" }]
      }]
    }
  }
}
```

### Block Formula Kinds Reference

Every block has a `kind` discriminator and optional `tz` (timezone) and `cast` (type cast) properties.

#### `literal` — Static Values

```json
{ "kind": "literal", "literal": "Hello World" }
{ "kind": "literal", "literal": 42 }
{ "kind": "literal", "literal": true }
{ "kind": "literal", "literal": null }
{ "kind": "literal", "literal": ["active", "pending", "approved"] }
```

#### `column` — Table Column Reference

```json
{ "kind": "column", "name": "fullname" }
{ "kind": "column", "name": ["col1", "col2"] }
```

#### `builtin` — SQL Constants

```json
{ "kind": "builtin", "name": "current_date" }
{ "kind": "builtin", "name": "now" }
```

Allowed values: `current_date`, `current_time`, `current_timestamp`, `now`

#### `function` — SQL Function Calls

```json
{
  "kind": "function",
  "name": "concat",
  "inputs": [
    { "kind": "literal", "literal": "Hello " },
    { "kind": "column", "name": "fullname" }
  ]
}
```

> Only whitelisted functions are allowed (see [Allowed Functions Reference](#allowed-functions-reference)).

#### `extract` — Date Part Extraction

```json
{
  "kind": "extract",
  "part": "month",
  "inputs": [{ "kind": "column", "name": "created_on" }]
}
```

> SQL: `extract(month from "t0"."created_on")`

Parts: `year`, `month`, `day`, `hour`, `minute`, `second`

#### `aggregate` — Aggregate Functions

```json
{ "kind": "aggregate", "name": "count", "inputs": [] }
```

> SQL: `count(*)`

```json
{
  "kind": "aggregate",
  "name": "count",
  "distinct": true,
  "inputs": [{ "kind": "column", "name": "product_code" }]
}
```

> SQL: `count(distinct "t0"."product_code")`

Allowed aggregates: `count`, `sum`, `avg`, `min`, `max`, `jsonb_agg`, `json_agg`, `array_agg`

#### `math` — Arithmetic Operations

```json
{
  "kind": "math",
  "op": "*",
  "inputs": [
    { "kind": "column", "name": "quantity" },
    { "kind": "column", "name": "unit_price" }
  ]
}
```

> SQL: `("t0"."quantity" * "t0"."unit_price")`

Operators: `+`, `-`, `*`, `/`, `%`
Requires at least 2 operands. For 3+: `((a op b) op c)`.

#### `case` — Conditional Expressions

```json
{
  "kind": "case",
  "cases": [{
    "when": {
      "kind": "compare",
      "op": ">",
      "left": { "kind": "column", "name": "price" },
      "right": { "kind": "literal", "literal": 100 }
    },
    "then": { "kind": "literal", "literal": "expensive" }
  }],
  "else": { "kind": "literal", "literal": "cheap" }
}
```

> SQL: `case when "t0"."price" > $1 then $2 else $3 end`

#### `compare` — Comparison Operations

```json
{
  "kind": "compare",
  "op": "in",
  "left": { "kind": "column", "name": "status" },
  "right": { "kind": "literal", "literal": ["active", "pending"] }
}
```

> SQL: `"t0"."status" in ($1, $2)`

Operators: `=`, `!=`, `<>`, `>`, `<`, `>=`, `<=`, `like`, `ilike`, `in`, `not in`, `not_in`

#### `boolean` — Logical Operations

```json
{
  "kind": "boolean",
  "op": "and",
  "inputs": [
    {
      "kind": "compare", "op": ">",
      "left": { "kind": "column", "name": "price" },
      "right": { "kind": "literal", "literal": 100 }
    },
    {
      "kind": "compare", "op": "ilike",
      "left": { "kind": "column", "name": "name" },
      "right": { "kind": "literal", "literal": "%pro%" }
    }
  ]
}
```

> SQL: `(("t0"."price" > $1) and ("t0"."name" ilike $2))`

Operators: `and`, `or`, `not`

### Block Formula: Type Casting

Any block can include a `cast` property:

```json
{ "kind": "column", "name": "price", "cast": "decimal" }
```

> SQL: `("t0"."price")::decimal`

### Block Formula: Timezone Handling

Any block can include a `tz` property:

```json
{ "kind": "function", "name": "now", "tz": "UTC" }
```

> SQL: `now() at time zone $1`

### Advanced Formula Examples

**Nested Functions with Aggregates:** Round the sum of (quantity × unit_price)

```json
{
  "formulas": {
    "rounded_total": {
      "alias": "rounded_total",
      "inputs": [{
        "kind": "function",
        "name": "round",
        "inputs": [
          {
            "kind": "aggregate",
            "name": "sum",
            "inputs": [{
              "kind": "math",
              "op": "*",
              "inputs": [
                { "kind": "column", "name": "quantity" },
                { "kind": "column", "name": "unit_price" }
              ]
            }]
          },
          { "kind": "literal", "literal": 2 }
        ]
      }]
    }
  }
}
```

> SQL: `round(sum(("t0"."quantity" * "t0"."unit_price")), $1) as "rounded_total"`

**CASE with Boolean Logic:** Categorize rows

```json
{
  "formulas": {
    "category": {
      "inputs": [{
        "kind": "case",
        "cases": [{
          "when": {
            "kind": "boolean",
            "op": "and",
            "inputs": [
              {
                "kind": "compare", "op": ">",
                "left": { "kind": "column", "name": "price" },
                "right": { "kind": "literal", "literal": 100 }
              },
              {
                "kind": "compare", "op": "ilike",
                "left": { "kind": "column", "name": "name" },
                "right": { "kind": "literal", "literal": "%pro%" }
              }
            ]
          },
          "then": { "kind": "literal", "literal": "premium" }
        }],
        "else": { "kind": "literal", "literal": "standard" }
      }]
    }
  }
}
```

**Null Handling with COALESCE:**

```json
{
  "formulas": {
    "safe_desc": {
      "inputs": [{
        "kind": "function",
        "name": "coalesce",
        "inputs": [
          { "kind": "column", "name": "description" },
          { "kind": "literal", "literal": "No description" }
        ]
      }]
    }
  }
}
```

**Timezone Conversion:**

```json
{
  "formulas": {
    "local_time": {
      "inputs": [{
        "kind": "function",
        "name": "to_char",
        "inputs": [
          { "kind": "function", "name": "now", "tz": "UTC" },
          { "kind": "literal", "literal": "YYYY-MM-DD HH24:MI:SS" }
        ]
      }]
    }
  }
}
```

> SQL: `to_char(now() at time zone $1, $2)`

---

## Pivot

**Parameter:** `pivot` — `{ matrix, hideEmptyRows?, orderBy?, limit? } | null`

Use `pivot` to perform advanced cross-tab grouping queries with aggregations. Each matrix object is executed as a CTE query. All CTEs are cross-joined to create a full matrix, then the main data is left-joined. This ensures all combinations appear in results, even when no matching records exist.

### Pivot Structure

```typescript
interface IPivot {
  matrix: ISelectPivotMatrixQuery[];
  hideEmptyRows?: boolean;
  orderBy?: string | ISelectQueryOrderBy | ISelectQueryOrderBy[];
  limit?: number;
}

interface ISelectPivotMatrixQuery {
  using: string;      // field in main query to join the CTE on
  columns: string;    // columns to select (supports alias, spread, functions)
  spread?: boolean;   // spread jsonb columns as separate columns
  filters?: IQueryFilterGroup;
  limit?: number;
  dateRange?: {
    interval: "day" | "week" | "month" | "year" | "hour" | "minute" | "second";
    increment?: number;   // number of intervals to increment (default: 1)
    min: string;          // minimum datetime value (ISO format)
    max: string;          // maximum datetime value (ISO format)
  };
}
```

### How Pivot Works

1. Each `matrix` entry generates a CTE (Common Table Expression):
   - If `dateRange` is provided, a date range series is generated
   - Otherwise, records are fetched from the related data source
2. All CTEs are cross-joined to create the full cartesian product (matrix)
3. The main query data is left-joined to the matrix
4. This ensures all combinations appear, even with zero matching records

### Example: Orders per Day, per User, per Status

```json
{
  "columns": "...order_status(orderStatus:name)",
  "pivot": {
    "matrix": [
      {
        "using": "created_on",
        "columns": "day:to_char[DD/MM/YYYY]@created_on",
        "dateRange": {
          "interval": "day",
          "min": "2025-09-01T00:00:00Z",
          "max": "2025-09-02T00:00:00Z"
        },
        "spread": true
      },
      {
        "using": "record_owner",
        "columns": "userName:name",
        "spread": true,
        "filters": {
          "combinator": "and",
          "rules": [
            {
              "field": "primary_role",
              "operator": "=",
              "value": "1cdefd30-9f6d-4c7e-94c9-5b8a7e1c9f31"
            }
          ]
        }
      }
    ]
  },
  "calculations": [
    {
      "field": "id",
      "func": "count",
      "name": "total"
    },
    {
      "field": "amount",
      "func": "sum",
      "name": "totalSold"
    }
  ]
}
```

**What each matrix entry does:**

1. **First matrix** (`using: "created_on"`): Creates a date range series from 2025-09-01 to 2025-09-02 with `day` intervals. Even if there are no orders on a given day, that day still appears in results.
2. **Second matrix** (`using: "record_owner"`): Fetches users filtered by role. Even if a user has no orders on a day, they still appear in the cross-join.

**Result:**

```json
[
  {
    "userName": "User 1",
    "orderStatus": 1,
    "day": "01/09/2025",
    "total": 10,
    "totalSold": 3000
  },
  {
    "userName": "User 2",
    "orderStatus": 5,
    "day": "01/09/2025",
    "total": 5,
    "totalSold": 1500
  },
  {
    "userName": "User 1",
    "orderStatus": 1,
    "day": "02/09/2025",
    "total": 10,
    "totalSold": 3000
  },
  {
    "userName": "User 2",
    "orderStatus": 3,
    "day": "02/09/2025",
    "total": 5,
    "totalSold": 1500
  }
]
```

### Date Range Intervals

| Interval | Description |
|---|---|
| `day` | Generate one row per day |
| `week` | Generate one row per week |
| `month` | Generate one row per month |
| `year` | Generate one row per year |
| `hour` | Generate one row per hour |
| `minute` | Generate one row per minute |
| `second` | Generate one row per second |

### Pivot Options

| Option | Type | Description |
|---|---|---|
| `hideEmptyRows` | `boolean` | Don't include rows where no matching data exists |
| `orderBy` | `string \| object \| array` | Sort the pivot results |
| `limit` | `number` | Maximum number of pivot result rows (default: 1000) |

---

## Child Queries

**Parameter:** `childQueries` — `ISelectQueryChildQueryParams[] | null`

Use `childQueries` to fetch related records from a child data source as a nested JSON array for each parent record. This is similar to a `LEFT JOIN` but returns results as an aggregated JSON array in a single column.

### Child Query Structure

```typescript
interface ISelectQueryChildQueryParams {
  alias: string;                    // alias for the child query
  from: string;                    // child data source slug in "appSlug_slug" format
  using: string;                   // field in the child DS that references the parent record
  columns?: string | null;         // comma-separated columns to select from child
  filters?: IQueryFilterGroup;     // optional filters on child records
  calculations?: ISelectQueryCalculationRule[]; // optional aggregations
  orderBy?: string | ISelectQueryOrderBy | ISelectQueryOrderBy[];
  limit?: number;                  // max child records per parent (default: 100)
}
```

### Example: Clients with Their Matters

```json
{
  "columns": "id, name, matters",
  "childQueries": [
    {
      "alias": "matters",
      "from": "attornaid_matter",
      "using": "client",
      "columns": "name",
      "filters": {
        "rules": [
          { "field": "created_on", "operator": "<", "value": "2025-12-01" }
        ]
      }
    }
  ]
}
```

**Result:**

```json
[
  {
    "id": "uuid",
    "name": "Client Name",
    "matters": [
      { "name": "Matter 1" },
      { "name": "Matter 2" }
    ]
  }
]
```

### Key Rules

- The child query key (e.g. `"matters"`) must also appear in the parent's `columns` string.
- `from` uses `appSlug_slug` format (e.g. `"attornaid_matter"`).
- `using` is the field in the **child** data source that references the parent record's `id`.
- All parent query parameters (`columns`, `filters`, `calculations`, `orderBy`, `limit`) are supported within child queries.

### Example: Products with Recent Orders (limited, sorted)

```json
{
  "columns": "id, product_name, recent_orders",
  "childQueries": [
    {
      "alias": "recent_orders",
      "from": "shop_order_item",
      "using": "product",
      "columns": "order_date, quantity, total_price",
      "orderBy": "order_date DESC",
      "limit": 5,
      "filters": {
        "rules": [
          { "field": "order_date", "operator": "last_30_days" }
        ]
      }
    }
  ]
}
```

### Example: Child Query with Aggregations

```json
{
  "columns": "id, name, order_stats",
  "childQueries": [
    {
      "alias": "order_stats",
      "from": "shop_order",
      "using": "customer",
      "calculations": [
        { "field": "id", "func": "count", "name": "total_orders" },
        { "field": "amount", "func": "sum", "name": "total_spent" }
      ]
    }
  ]
}
```

---

## Expand

### `expandTypes` (Deprecated)

**Type:** `("user" | "enum" | "relation")[] | null`

Automatically expand all columns of the specified field types. Replaced by `expand`.

```json
{
  "expandTypes": ["user", "relation"]
}
```

### `expand`

**Type:** `string[] | null`

List of specific field slugs to expand. Expanded fields return their full object representation instead of just the ID/value.

```json
{
  "expand": ["record_owner", "related_account", "status"]
}
```

---

## Query Mode

**Parameter:** `queryMode` — `"OLTP" | "OLAP" | "EXPORT"`
**Default:** `"OLTP"`

| Mode | Description |
|---|---|
| `OLTP` | Standard transactional queries. Default. Lower limits for interactive use. |
| `OLAP` | Analytical queries. Allows larger result sets. |
| `EXPORT` | Export mode. Highest limits for bulk data extraction. |

---

## Distinct Columns

**Parameter:** `distinctColumns` — `string[] | null`

List of columns to deduplicate results on. Use only for simple queries when you need exactly one deterministic row per group and the winner is defined by a simple `ORDER BY`.

> **Important:** Do **not** use `distinctColumns` together with `calculations`. Prefer `calculations` to aggregate data.

### Example: Last Invoice Date per Client

```json
{
  "columns": "...client(client_name:name), invoice_date",
  "distinctColumns": ["client"],
  "orderBy": "invoice_date DESC"
}
```

### Example: Deduplicate by Email

```json
{
  "columns": "email, name",
  "distinctColumns": ["email"]
}
```

---

## Full Count

**Parameter:** `fullCount` — `boolean`

When `true`, returns the total count of records matching the filters using a window function, alongside the paginated results.

```json
{
  "columns": "id, name",
  "limit": 10,
  "offset": 0,
  "fullCount": true
}
```

---

## Cursor-Based Sync

| Parameter | Type | Description |
|---|---|---|
| `cursorDateStart` | `string \| null` | ISO datetime cursor start for data sync |
| `cursorDateEnd` | `string \| null` | ISO datetime cursor end for data sync |

Used for incremental data synchronization, fetching only records modified within the cursor window.

```json
{
  "cursorDateStart": "2025-10-01T00:00:00Z",
  "cursorDateEnd": "2025-10-02T00:00:00Z"
}
```

---

## Filter Operators Reference

### Basic Comparison

| Operator | Description | Value Type |
|---|---|---|
| `=` | Equals | any |
| `!=` | Not equals | any |
| `<>` | Not equals (alias) | any |
| `>` | Greater than | number/date |
| `<` | Less than | number/date |
| `>=` | Greater than or equal | number/date |
| `<=` | Less than or equal | number/date |
| `between` | Between two values | `[min, max]` |

### Text Search

| Operator | Description | Value Type |
|---|---|---|
| `like` | Pattern match (case-sensitive) | string with `%` wildcards |
| `not like` | Negated pattern match | string with `%` wildcards |
| `starts with` | Starts with value | string |
| `ends with` | Ends with value | string |

### Collection

| Operator | Description | Value Type |
|---|---|---|
| `in` | Value is in list | array |
| `not in` | Value is not in list | array |
| `not_in` | Alias for `not in` | array |
| `exists` | Record exists | — |
| `contains any` | Contains any of the values | array |
| `contains all` | Contains all of the values | array |
| `not contains` | Does not contain | any |

### Null/Empty Checks

| Operator | Description | Value Type |
|---|---|---|
| `is` | Is value | any |
| `is not` | Is not value | any |
| `empty` | Field is empty/null | — |
| `not empty` | Field is not empty/null | — |
| `null` | Field is null | — |
| `not null` | Field is not null | — |

### Boolean

| Operator | Description | Value Type |
|---|---|---|
| `true` | Field is true | — |
| `false` | Field is false | — |

### User-Related

| Operator | Description |
|---|---|
| `active_user` | Field equals the current logged-in user |
| `not_active_user` | Field does not equal the current user |
| `in_active_user_scope` | Field is within active user's scope |
| `not_in_active_user_scope` | Field is outside active user's scope |
| `in_role` | User has specified role |
| `not_in_role` | User does not have specified role |
| `in_team` | User is in specified team |
| `not_in_team` | User is not in specified team |
| `in_active_user_team` | User is in active user's team |
| `not_in_active_user_team` | User is not in active user's team |
| `in_unit` | User is in specified org unit |
| `not_in_unit` | User is not in specified org unit |
| `in_sub_unit` | User is in sub-unit |
| `not_in_sub_unit` | User is not in sub-unit |

### Record Sharing

| Operator | Description |
|---|---|
| `shared_to_me` | Record is shared to the current user |

### Follower-Related

| Operator | Description |
|---|---|
| `contains_active_user` | Followers contain the active user |
| `not_contains_active_user` | Followers do not contain the active user |
| `contains_member_of_active_user_team` | Followers contain a member of active user's team |

### Date Shortcuts

| Operator | Description |
|---|---|
| `today` | Is today |
| `tomorrow` | Is tomorrow |
| `yesterday` | Is yesterday |
| `last_7_days` | Within last 7 days |
| `last_15_days` | Within last 15 days |
| `last_30_days` | Within last 30 days |
| `last_60_days` | Within last 60 days |
| `last_90_days` | Within last 90 days |
| `last_120_days` | Within last 120 days |
| `next_7_days` | Within next 7 days |
| `next_15_days` | Within next 15 days |
| `next_30_days` | Within next 30 days |
| `next_60_days` | Within next 60 days |
| `next_90_days` | Within next 90 days |
| `next_120_days` | Within next 120 days |
| `last_week` | During last week |
| `this_week` | During this week |
| `next_week` | During next week |
| `last_month` | During last month |
| `this_month` | During this month |
| `next_month` | During next month |
| `before_today` | Before today |
| `after_today` | After today |
| `last_year` | During last year |
| `this_year` | During this year |
| `next_year` | During next year |
| `first_quarter` | During Q1 of current year |
| `second_quarter` | During Q2 of current year |
| `third_quarter` | During Q3 of current year |
| `fourth_quarter` | During Q4 of current year |
| `last_3_months` | Within last 3 months |
| `last_6_months` | Within last 6 months |

### Dynamic Date Operators (require value)

| Operator | Value | Description |
|---|---|---|
| `x_days_ago` | number | Exactly X days ago |
| `x_days_later` | number | Exactly X days later |
| `before_last_x_days` | number | Before the last X days |
| `in_last_x_days` | number | Within the last X days |
| `after_last_x_days` | number | After the last X days |
| `in_next_x_days` | number | Within the next X days |

---

## Allowed Functions Reference

### Postgres Functions

| Category | Functions |
|---|---|
| **String** | `length`, `lower`, `upper`, `substr`, `replace`, `concat`, `trim`, `ltrim`, `rtrim`, `btrim`, `split_part`, `initcap`, `reverse`, `strpos`, `lpad`, `rpad` |
| **Number** | `abs`, `ceil`, `floor`, `round`, `sqrt`, `power`, `mod`, `gcd`, `lcm`, `exp`, `ln`, `log`, `log10`, `log1p`, `pi`, `sign`, `width_bucket`, `trunc`, `greatest`, `least` |
| **Date/Time** | `now`, `age`, `clock_timestamp`, `date_part`, `date_trunc`, `extract`, `isfinite`, `justify_days`, `justify_hours`, `make_date`, `make_time`, `make_timestamp`, `make_timestamptz`, `timeofday`, `to_timestamp`, `to_char`, `to_date`, `to_time` |
| **Utility** | `coalesce` |
| **JSON/JSONB** | `jsonb_array_length`, `jsonb_extract_path`, `jsonb_extract_path_text`, `jsonb_object_keys`, `jsonb_build_object`, `json_build_object`, `jsonb_agg`, `json_agg`, `array_agg`, `array_to_json`, `row_to_json` |
| **Internal** | `noselect`, `anyvalue` |

### Postgres Literals (used as raw SQL)

`current_date`, `current_time`, `current_timestamp`

---

## Allowed Aggregates Reference

Supported aggregate functions:

| Aggregate | Description |
|---|---|
| `count` | Count of rows/values |
| `sum` | Sum of values |
| `avg` | Average of values |
| `min` | Minimum value |
| `max` | Maximum value |
| `jsonb_agg` | Aggregate values as JSONB array |
| `json_agg` | Aggregate values as JSON array |
| `array_agg` | Aggregate values as PostgreSQL array |

---

## Allowed Cast Types

Valid types for the `cast` property in block formulas and `numberType` in calculations:

`int`, `int[]`, `int2`, `int2[]`, `int4`, `int4[]`, `int8`, `int8[]`, `bigint`, `bigint[]`, `real`, `real[]`, `float`, `float[]`, `float4`, `float4[]`, `float8`, `float8[]`, `numeric`, `numeric[]`, `double`, `double[]`, `decimal`, `decimal[]`, `money`, `money[]`, `timestamp`, `timestamp[]`, `timestamptz`, `timestamptz[]`, `date`, `date[]`, `time`, `time[]`, `interval`, `interval[]`, `bool`, `bool[]`, `boolean`, `boolean[]`, `uuid`, `uuid[]`, `text`, `text[]`

---

## Complete Examples

### Example 1: Full-Featured Select Query

Fetch tasks with filters, sorting, pagination, and relation expansion:

```json
{
  "dataSourceFullSlug": "crm_task",
  "columns": "id, task_name, ...record_owner(owner_name:name, owner_email:email), ...related_account(account_name:name)",
  "filters": {
    "combinator": "and",
    "rules": [
      { "field": "task_status", "operator": "in", "value": [1, 2] },
      { "field": "due_date", "operator": "in_next_x_days", "value": 7 },
      { "field": "record_owner", "operator": "in_active_user_team" }
    ]
  },
  "orderBy": "due_date ASC, task_name ASC",
  "limit": 50,
  "offset": 0,
  "fullCount": true
}
```

### Example 2: Aggregation Dashboard

Monthly sales report grouped by category:

```json
{
  "dataSourceFullSlug": "shop_order",
  "columns": "months_of_year@created_on, ...category(cat:name)",
  "calculations": [
    { "field": "id", "func": "count", "name": "order_count" },
    { "field": "total_amount", "func": "sum", "name": "revenue" },
    { "field": "total_amount", "func": "avg", "name": "avg_order" }
  ],
  "filters": {
    "rules": [
      { "field": "created_on", "operator": "this_year" },
      { "field": "order_status", "operator": "!=", "value": "cancelled" }
    ]
  },
  "orderBy": "months_of_year@created_on ASC"
}
```

### Example 3: Pivot — Weekly Sales by Salesperson

```json
{
  "dataSourceFullSlug": "shop_order",
  "columns": "...order_status(status_name:name)",
  "pivot": {
    "matrix": [
      {
        "using": "created_on",
        "columns": "week:to_char[IYYY-IW]@created_on",
        "dateRange": {
          "interval": "week",
          "min": "2025-01-01T00:00:00Z",
          "max": "2025-03-31T23:59:59Z"
        },
        "spread": true
      },
      {
        "using": "salesperson",
        "columns": "sp_name:name",
        "spread": true
      }
    ],
    "orderBy": "week ASC"
  },
  "calculations": [
    { "field": "id", "func": "count", "name": "deals" },
    { "field": "amount", "func": "sum", "name": "revenue" }
  ]
}
```

### Example 4: Child Queries — Customers with Orders and Tickets

```json
{
  "dataSourceFullSlug": "crm_customer",
  "columns": "id, name, email, recent_orders, open_tickets",
  "childQueries": [
    {
      "alias": "recent_orders",
      "from": "shop_order",
      "using": "customer",
      "columns": "id, order_date, total_amount, ...status(status_label:name)",
      "orderBy": "order_date DESC",
      "limit": 10,
      "filters": {
        "rules": [
          { "field": "order_date", "operator": "last_90_days" }
        ]
      }
    },
    {
      "alias": "open_tickets",
      "from": "support_ticket",
      "using": "customer",
      "columns": "id, subject, priority, created_on",
      "orderBy": "created_on DESC",
      "limit": 5,
      "filters": {
        "rules": [
          { "field": "status", "operator": "!=", "value": "closed" }
        ]
      }
    }
  ],
  "filters": {
    "rules": [
      { "field": "status", "operator": "=", "value": "active" }
    ]
  },
  "limit": 25
}
```

### Example 5: Formulas — Computed Columns with Subquery

Fetch accounts with an inline profit margin formula and a subquery counting active deals:

```json
{
  "dataSourceFullSlug": "crm_account",
  "columns": "id, name, profit_margin, active_deals",
  "formulas": {
    "profit_margin": {
      "inputs": [{
        "kind": "math",
        "op": "*",
        "inputs": [
          {
            "kind": "math",
            "op": "/",
            "inputs": [
              {
                "kind": "math",
                "op": "-",
                "inputs": [
                  { "kind": "column", "name": "revenue" },
                  { "kind": "column", "name": "cost" }
                ]
              },
              { "kind": "column", "name": "revenue", "cast": "decimal" }
            ]
          },
          { "kind": "literal", "literal": 100 }
        ]
      }]
    },
    "active_deals": {
      "from": "crm_deal",
      "with": "account",
      "filters": {
        "rules": [
          { "field": "stage", "operator": "!=", "value": "lost" },
          { "field": "stage", "operator": "!=", "value": "won" }
        ]
      },
      "inputs": [{
        "kind": "aggregate",
        "name": "count",
        "inputs": []
      }]
    }
  },
  "orderBy": "profit_margin DESC",
  "limit": 20
}
```

### Example 6: Combined Pivot + Calculations + Filters

Daily hourly breakdown of support tickets per agent for today:

```json
{
  "dataSourceFullSlug": "support_ticket",
  "columns": "...priority(priority_name:name)",
  "pivot": {
    "matrix": [
      {
        "using": "created_on",
        "columns": "hour:hours_of_today@created_on",
        "dateRange": {
          "interval": "hour",
          "min": "2025-10-15T00:00:00Z",
          "max": "2025-10-15T23:59:59Z"
        },
        "spread": true
      },
      {
        "using": "assigned_agent",
        "columns": "agent:name",
        "spread": true,
        "filters": {
          "rules": [
            { "field": "is_active", "operator": "true" }
          ]
        }
      }
    ],
    "hideEmptyRows": false
  },
  "calculations": [
    { "field": "id", "func": "count", "name": "ticket_count" }
  ],
  "filters": {
    "rules": [
      { "field": "created_on", "operator": "today" }
    ]
  }
}
```

### Example 7: Complex Nested Filters

```json
{
  "dataSourceFullSlug": "crm_deal",
  "columns": "id, name, amount, stage, record_owner(name)",
  "filters": {
    "combinator": "and",
    "rules": [
      {
        "field": "amount",
        "operator": ">",
        "value": 10000
      },
      {
        "combinator": "or",
        "rules": [
          {
            "combinator": "and",
            "rules": [
              { "field": "stage", "operator": "=", "value": "negotiation" },
              { "field": "created_on", "operator": "this_month" }
            ]
          },
          {
            "combinator": "and",
            "rules": [
              { "field": "stage", "operator": "=", "value": "proposal" },
              { "field": "record_owner", "operator": "active_user" }
            ]
          }
        ]
      },
      {
        "field": "rel_account/industry",
        "operator": "in",
        "value": ["technology", "finance", "healthcare"]
      }
    ]
  },
  "orderBy": "amount DESC",
  "limit": 100
}
```

### Example 8: CASE Formula with Multiple Conditions

```json
{
  "dataSourceFullSlug": "crm_deal",
  "columns": "id, name, amount, deal_tier",
  "formulas": {
    "deal_tier": {
      "inputs": [{
        "kind": "case",
        "cases": [
          {
            "when": {
              "kind": "compare", "op": ">=",
              "left": { "kind": "column", "name": "amount" },
              "right": { "kind": "literal", "literal": 100000 }
            },
            "then": { "kind": "literal", "literal": "Enterprise" }
          },
          {
            "when": {
              "kind": "compare", "op": ">=",
              "left": { "kind": "column", "name": "amount" },
              "right": { "kind": "literal", "literal": 25000 }
            },
            "then": { "kind": "literal", "literal": "Mid-Market" }
          },
          {
            "when": {
              "kind": "compare", "op": ">=",
              "left": { "kind": "column", "name": "amount" },
              "right": { "kind": "literal", "literal": 5000 }
            },
            "then": { "kind": "literal", "literal": "SMB" }
          }
        ],
        "else": { "kind": "literal", "literal": "Micro" }
      }]
    }
  }
}
```

### Example 9: Date Formatting with Block Formula

```json
{
  "dataSourceFullSlug": "crm_activity",
  "columns": "id, subject, formatted_date, formatted_time",
  "formulas": {
    "formatted_date": {
      "inputs": [{
        "kind": "function",
        "name": "to_char",
        "inputs": [
          { "kind": "column", "name": "created_on" },
          { "kind": "literal", "literal": "DD Mon YYYY" }
        ]
      }]
    },
    "formatted_time": {
      "inputs": [{
        "kind": "function",
        "name": "to_char",
        "inputs": [
          { "kind": "column", "name": "created_on" },
          { "kind": "literal", "literal": "HH24:MI" }
        ]
      }]
    }
  },
  "orderBy": "created_on DESC",
  "limit": 50
}
```

### Example 10: Distinct Count with Min/Max Bounds

```json
{
  "dataSourceFullSlug": "shop_order",
  "columns": "category",
  "calculations": [
    {
      "field": "id",
      "func": "count",
      "name": "total_orders"
    },
    {
      "field": "amount",
      "func": "sum",
      "name": "valid_revenue",
      "minValue": 0,
      "maxValue": 1000000
    },
    {
      "field": "amount",
      "func": "avg",
      "name": "avg_amount",
      "numberType": "decimal"
    },
    {
      "field": "product_code",
      "func": "count",
      "name": "unique_products",
      "isDistinct": true
    }
  ]
}
```
