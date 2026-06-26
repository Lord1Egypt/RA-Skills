# Docyrus Query & Formula Guide

## Table of Contents

1. [Query Payload Structure](#query-payload-structure)
2. [Columns](#columns)
3. [Filters](#filters)
4. [Filter Operators Reference](#filter-operators-reference)
5. [Order By](#order-by)
6. [Pagination](#pagination)
7. [Calculations (Aggregations)](#calculations)
8. [Formulas — Simple](#formulas--simple)
9. [Formulas — Block (AST)](#formulas--block-ast)
10. [Formulas — Subquery](#formulas--subquery)
11. [Block Kinds Reference](#block-kinds-reference)
12. [Child Queries](#child-queries)
13. [Pivot](#pivot)
14. [Expand](#expand)
15. [Allowed Functions](#allowed-functions)
16. [Allowed Cast Types](#allowed-cast-types)
17. [Complete Examples](#complete-examples)

---

## Query Payload Structure

Data source items are fetched via GET with a query payload:

```
GET /v1/apps/{appSlug}/data-sources/{slug}/items
```

The payload (`ZodSelectQueryPayload`) supports:

```typescript
interface ISelectQueryParams {
  columns?: string | null                    // comma-separated column names
  filters?: IQueryFilterGroup | null         // nested AND/OR filter groups
  filterKeyword?: string | null              // full-text search
  orderBy?: string | object | object[]       // sorting
  limit?: number                             // default: 100
  offset?: number                            // default: 0
  fullCount?: boolean                        // return total count
  calculations?: ICalculationRule[] | null   // aggregations
  formulas?: Record<string, IFormula> | null // computed virtual columns
  childQueries?: Record<string, IChildQuery> | null
  pivot?: { matrix, hideEmptyRows?, orderBy?, limit? } | null
  expand?: string[] | null                   // expand relation/user/enum fields
  expandTypes?: ('user' | 'enum' | 'relation')[] | null
  distinctColumns?: string[] | null
  queryMode?: 'OLTP' | 'OLAP' | 'EXPORT'
  recordId?: string | null                   // fetch single record by ID
}
```

**Critical**: Always send `columns`. Without it, only `id` is returned.

---

## Columns

**Type**: comma-separated string (server) or array (client interceptor converts).

### Basic Selection
```
"columns": "task_name, created_on, record_owner"
```

### Aliasing with `:`
```
"columns": "ra:related_account"
→ { "ra": { "id": "uuid", "name": "account name" } }
```

### Relation Expansion with `()`
```
"columns": "task_name, related_account(name:account_name, phone:account_phone)"
→ { "task_name": "...", "related_account": { "name": "...", "phone": "..." } }
```

### Spread with `...` (flatten to root)
```
"columns": "task_name, ...related_account(account_name, phone:account_phone)"
→ { "task_name": "...", "account_name": "...", "phone": "..." }
```

### Functions with `@`
```
"columns": "...related_account(an:account_name@upper)"
→ { "an": "ACCOUNT NAME" }
```

### Date Grouping Formulas

| Formula | Description |
|---------|-------------|
| `hours_of_today@field` | Group by hour for today |
| `days_of_week@field` | Group by day for current week |
| `days_of_month@field` | Group by day for current month |
| `weeks_of_month@field` | Group by week for current month |
| `months_of_year@field` | Group by month (YYYY-MM) |
| `quarters_of_year@field` | Group by quarter (YYYY-Q) |

### to_char Formatting
```
"columns": "day:to_char[DD/MM/YYYY]@created_on"
```

---

## Filters

Recursive group structure:

```typescript
interface IQueryFilterGroup {
  rules: (IQueryFilterRule | IQueryFilterGroup)[]
  combinator?: 'and' | 'or'  // default: 'and'
  not?: boolean               // negate entire group
}

interface IQueryFilterRule {
  field?: string
  operator: string
  value?: any
  filterType?: string | null  // NUMERIC, ALPHA, BOOL, DATE, DATETIME, RELATION, OWNER, etc.
}
```

### Basic AND
```json
{
  "filters": {
    "combinator": "and",
    "rules": [
      { "field": "task_status", "operator": "=", "value": 1 },
      { "field": "priority", "operator": ">=", "value": 3 }
    ]
  }
}
```

### Nested AND + OR
```json
{
  "filters": {
    "combinator": "and",
    "rules": [
      { "field": "created_on", "operator": "between", "value": ["2025-10-01", "2025-11-01"] },
      {
        "combinator": "or",
        "rules": [
          { "field": "email", "operator": "empty" },
          { "field": "phone", "operator": "not empty" }
        ]
      }
    ]
  }
}
```

### Filter by Related Record's Field
```json
{ "field": "rel_client/account_status", "operator": "=", "value": 2 }
```

### Negated Group
```json
{ "combinator": "and", "not": true, "rules": [{ "field": "status", "operator": "=", "value": "archived" }] }
```

---

## Filter Operators Reference

### Comparison
`=`, `!=`, `<>`, `>`, `<`, `>=`, `<=`, `between` (value: `[min, max]`)

### Text
`like` (with `%` wildcards), `not like`, `starts with`, `ends with`

### Collection
`in` (array), `not in` (array), `exists`, `contains any` (array), `contains all` (array), `not contains`

### Null/Empty
`is`, `is not`, `empty`, `not empty`, `null`, `not null`

### Boolean
`true`, `false`

### User-Related (no value)
`active_user`, `not_active_user`, `in_active_user_scope`, `not_in_active_user_scope`, `in_role`, `not_in_role`, `in_team`, `not_in_team`, `in_active_user_team`, `not_in_active_user_team`, `in_unit`, `not_in_unit`, `in_sub_unit`, `not_in_sub_unit`, `shared_to_me`, `contains_active_user`, `not_contains_active_user`, `contains_member_of_active_user_team`

### Date Shortcuts (no value)
`today`, `tomorrow`, `yesterday`, `last_7_days`, `last_15_days`, `last_30_days`, `last_60_days`, `last_90_days`, `last_120_days`, `next_7_days`, `next_15_days`, `next_30_days`, `next_60_days`, `next_90_days`, `next_120_days`, `last_week`, `this_week`, `next_week`, `last_month`, `this_month`, `next_month`, `before_today`, `after_today`, `last_year`, `this_year`, `next_year`, `first_quarter`, `second_quarter`, `third_quarter`, `fourth_quarter`, `last_3_months`, `last_6_months`

### Dynamic Date (value = number)
`x_days_ago`, `x_days_later`, `before_last_x_days`, `in_last_x_days`, `after_last_x_days`, `in_next_x_days`

---

## Order By

```json
// String
{ "orderBy": "created_on DESC" }

// Multi-column string
{ "orderBy": "firstname ASC, lastname DESC" }

// Object
{ "orderBy": { "field": "created_on", "direction": "desc" } }

// Array
{ "orderBy": [{ "field": "status", "direction": "asc" }, { "field": "created_on", "direction": "desc" }] }

// Related field
{ "orderBy": "relation_field(field_name DESC), id ASC" }
```

---

## Pagination

```json
{ "limit": 25, "offset": 50, "fullCount": true }
```
Returns records 51–75. `fullCount: true` adds total count to response.

---

## Calculations

Aggregations. Selected `columns` become GROUP BY fields.

```typescript
interface ICalculationRule {
  func: 'count' | 'sum' | 'avg' | 'min' | 'max' | 'jsonb_agg' | 'json_agg' | 'array_agg'
  field: string       // 'id' for count, actual field for sum/avg/etc.
  name?: string       // result column alias
  isDistinct?: boolean
  minValue?: number   // only aggregate values > this
  maxValue?: number   // only aggregate values < this
  numberType?: 'bigint' | 'int' | 'decimal'
}
```

### Count per Group
```json
{
  "columns": "record_owner(name)",
  "calculations": [{ "field": "id", "func": "count", "name": "task_count" }],
  "filters": { "rules": [{ "field": "task_status", "operator": "=", "value": 1 }] }
}
```

### Multiple Aggregations
```json
{
  "columns": "category",
  "calculations": [
    { "field": "id", "func": "count", "name": "total" },
    { "field": "amount", "func": "sum", "name": "totalAmount" },
    { "field": "amount", "func": "avg", "name": "avgAmount" },
    { "field": "amount", "func": "min", "name": "minAmount" },
    { "field": "amount", "func": "max", "name": "maxAmount" }
  ]
}
```

---

## Formulas — Simple

Single-depth function call. Column refs use `{column_name}` syntax.

```json
{
  "columns": "id, name, formatted_date, full_name",
  "formulas": {
    "formatted_date": { "func": "to_char", "args": ["{created_on}", "DD/MM/YYYY"] },
    "full_name": { "func": "concat", "args": ["{first_name}", " ", "{last_name}"] },
    "upper_name": { "func": "upper", "args": ["{name}"] }
  }
}
```

**Rule**: Formula key must appear in `columns`.

---

## Formulas — Block (AST)

Composable expression tree. One root block in `inputs` array.

```json
{
  "columns": "id, name, my_formula",
  "formulas": {
    "my_formula": {
      "inputs": [{ "kind": "...", ... }]
    }
  }
}
```

### Math Example: `quantity * unit_price`
```json
{
  "formulas": {
    "line_total": {
      "inputs": [{
        "kind": "math", "op": "*",
        "inputs": [
          { "kind": "column", "name": "quantity" },
          { "kind": "column", "name": "unit_price" }
        ]
      }]
    }
  }
}
```

### CASE Example: Categorize by Amount
```json
{
  "formulas": {
    "tier": {
      "inputs": [{
        "kind": "case",
        "cases": [
          { "when": { "kind": "compare", "op": ">=", "left": { "kind": "column", "name": "amount" }, "right": { "kind": "literal", "literal": 100000 } }, "then": { "kind": "literal", "literal": "Enterprise" } },
          { "when": { "kind": "compare", "op": ">=", "left": { "kind": "column", "name": "amount" }, "right": { "kind": "literal", "literal": 25000 } }, "then": { "kind": "literal", "literal": "Mid-Market" } }
        ],
        "else": { "kind": "literal", "literal": "SMB" }
      }]
    }
  }
}
```

---

## Formulas — Subquery

Correlated subquery against a child data source.

```json
{
  "columns": "id, name, active_deals",
  "formulas": {
    "active_deals": {
      "from": "crm_deal",
      "with": "account",
      "filters": { "rules": [{ "field": "stage", "operator": "!=", "value": "lost" }] },
      "inputs": [{ "kind": "aggregate", "name": "count", "inputs": [] }]
    }
  }
}
```

- `from`: child table slug in `appSlug_tableSlug` format
- `with`: child field referencing parent `id` (string) or multi-field join (object)
- `filters`: optional WHERE on child table

### Multi-Field Join
```json
{ "with": { "child_field1": "parent_field1", "child_field2": "parent_field2" } }
```

### Compatibility Wrapper
Can also use `expression` key:
```json
{ "formulas": { "count": { "expression": { "from": "...", "with": "...", "inputs": [...] } } } }
```

---

## Block Kinds Reference

Every block has `kind` discriminator. Optional: `tz` (timezone), `cast` (type cast).

| Kind | Purpose | Key Props |
|------|---------|-----------|
| `literal` | Static value | `literal: string \| number \| boolean \| null \| array` |
| `column` | Table column ref | `name: string \| string[]` |
| `builtin` | SQL constant | `name: 'current_date' \| 'current_time' \| 'current_timestamp' \| 'now'` |
| `function` | Whitelisted SQL fn | `name: string, inputs?: block[]` |
| `math` | Arithmetic | `op: '+' \| '-' \| '*' \| '/' \| '%', inputs: block[]` (min 2) |
| `compare` | Comparison | `op: '=' \| '!=' \| '>' \| '<' \| '>=' \| '<=' \| 'like' \| 'ilike' \| 'in' \| 'not in', left: block, right: block` |
| `boolean` | Logical | `op: 'and' \| 'or' \| 'not', inputs: block[]` |
| `case` | Conditional | `cases: [{ when: block, then: block }], else?: block` |
| `aggregate` | Aggregate fn | `name: 'count' \| 'sum' \| 'avg' \| 'min' \| 'max' \| ..., distinct?: boolean, inputs: block[]` |
| `extract` | Date part | `part: 'year' \| 'month' \| 'day' \| 'hour' \| 'minute' \| 'second', inputs: [block]` |

### Type Casting
```json
{ "kind": "column", "name": "price", "cast": "decimal" }
```
→ SQL: `("t0"."price")::decimal`

### Timezone
```json
{ "kind": "function", "name": "now", "tz": "UTC" }
```
→ SQL: `now() at time zone 'UTC'`

---

## Child Queries

Fetch child records as nested JSON arrays per parent row.

```json
{
  "columns": "id, name, recent_orders",
  "childQueries": {
    "recent_orders": {
      "from": "shop_order_item",
      "using": "product",
      "columns": "order_date, quantity, total_price",
      "orderBy": "order_date DESC",
      "limit": 5,
      "filters": { "rules": [{ "field": "order_date", "operator": "last_30_days" }] }
    }
  }
}
```

**Rules:**
- Key (e.g. `recent_orders`) must appear in parent `columns`
- `from`: `appSlug_slug` format
- `using`: field in **child** DS referencing parent's `id`
- Supports full query params: `columns`, `filters`, `calculations`, `orderBy`, `limit`

---

## Pivot

Cross-tab matrix queries with date range series.

```json
{
  "columns": "...order_status(status:name)",
  "pivot": {
    "matrix": [
      {
        "using": "created_on",
        "columns": "day:to_char[DD/MM/YYYY]@created_on",
        "dateRange": { "interval": "day", "min": "2025-09-01T00:00:00Z", "max": "2025-09-30T23:59:59Z" },
        "spread": true
      },
      {
        "using": "record_owner",
        "columns": "userName:name",
        "spread": true
      }
    ],
    "hideEmptyRows": false,
    "orderBy": "day ASC",
    "limit": 1000
  },
  "calculations": [
    { "field": "id", "func": "count", "name": "total" },
    { "field": "amount", "func": "sum", "name": "totalSold" }
  ]
}
```

Date range intervals: `day`, `week`, `month`, `year`, `hour`, `minute`, `second`

---

## Expand

Return full objects for relation/user/enum fields:

```json
{ "expand": ["record_owner", "related_account", "status"] }
```

---

## Allowed Functions

**String**: `length`, `lower`, `upper`, `substr`, `replace`, `concat`, `trim`, `ltrim`, `rtrim`, `btrim`, `split_part`, `initcap`, `reverse`, `strpos`, `lpad`, `rpad`

**Number**: `abs`, `ceil`, `floor`, `round`, `sqrt`, `power`, `mod`, `greatest`, `least`, `trunc`, `gcd`, `lcm`, `exp`, `ln`, `log`, `sign`

**Date/Time**: `now`, `age`, `date_part`, `date_trunc`, `extract`, `to_timestamp`, `to_char`, `to_date`, `to_time`, `make_date`, `make_time`, `make_timestamp`

**Utility**: `coalesce`

**JSON**: `jsonb_array_length`, `jsonb_extract_path`, `jsonb_extract_path_text`, `jsonb_build_object`, `json_build_object`, `jsonb_agg`, `json_agg`, `array_agg`

---

## Allowed Cast Types

`int`, `int[]`, `int2`, `int4`, `int8`, `bigint`, `real`, `float`, `float4`, `float8`, `numeric`, `double`, `decimal`, `money`, `timestamp`, `timestamptz`, `date`, `time`, `interval`, `bool`, `boolean`, `uuid`, `text` (and array variants)

---

## Complete Examples

### Full-Featured Query
```json
{
  "columns": "id, task_name, ...record_owner(owner_name:name), ...related_account(account_name:name)",
  "filters": {
    "combinator": "and",
    "rules": [
      { "field": "task_status", "operator": "in", "value": [1, 2] },
      { "field": "due_date", "operator": "in_next_x_days", "value": 7 },
      { "field": "record_owner", "operator": "in_active_user_team" }
    ]
  },
  "orderBy": "due_date ASC",
  "limit": 50,
  "fullCount": true
}
```

### Monthly Sales Report
```json
{
  "columns": "months_of_year@created_on, ...category(cat:name)",
  "calculations": [
    { "field": "id", "func": "count", "name": "order_count" },
    { "field": "total_amount", "func": "sum", "name": "revenue" },
    { "field": "total_amount", "func": "avg", "name": "avg_order" }
  ],
  "filters": { "rules": [
    { "field": "created_on", "operator": "this_year" },
    { "field": "order_status", "operator": "!=", "value": "cancelled" }
  ]},
  "orderBy": "months_of_year@created_on ASC"
}
```

### Computed Columns + Subquery
```json
{
  "columns": "id, name, profit_margin, active_deals",
  "formulas": {
    "profit_margin": {
      "inputs": [{
        "kind": "math", "op": "*",
        "inputs": [
          { "kind": "math", "op": "/", "inputs": [
            { "kind": "math", "op": "-", "inputs": [
              { "kind": "column", "name": "revenue" },
              { "kind": "column", "name": "cost" }
            ]},
            { "kind": "column", "name": "revenue", "cast": "decimal" }
          ]},
          { "kind": "literal", "literal": 100 }
        ]
      }]
    },
    "active_deals": {
      "from": "crm_deal", "with": "account",
      "filters": { "rules": [{ "field": "stage", "operator": "!=", "value": "lost" }, { "field": "stage", "operator": "!=", "value": "won" }] },
      "inputs": [{ "kind": "aggregate", "name": "count", "inputs": [] }]
    }
  },
  "orderBy": "profit_margin DESC",
  "limit": 20
}
```

### Customers with Nested Orders
```json
{
  "columns": "id, name, email, recent_orders, open_tickets",
  "childQueries": {
    "recent_orders": {
      "from": "shop_order", "using": "customer",
      "columns": "id, order_date, total_amount, ...status(status_label:name)",
      "orderBy": "order_date DESC", "limit": 10,
      "filters": { "rules": [{ "field": "order_date", "operator": "last_90_days" }] }
    },
    "open_tickets": {
      "from": "support_ticket", "using": "customer",
      "columns": "id, subject, priority, created_on",
      "orderBy": "created_on DESC", "limit": 5,
      "filters": { "rules": [{ "field": "status", "operator": "!=", "value": "closed" }] }
    }
  },
  "limit": 25
}
```
