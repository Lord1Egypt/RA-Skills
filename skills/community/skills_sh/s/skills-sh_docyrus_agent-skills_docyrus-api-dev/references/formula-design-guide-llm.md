# SQL Block Formula Reference

## Formula Types

Two block formula formats:

**Block Inline** — AST expression in SELECT: `{ alias?: string, inputs: IQueryFormulaBlock[] }`. Detected by `inputs` without `from`/`with`.

**Block Subquery** — correlated subquery on child table: `{ alias?, inputs, from: string, with: string | Record<string,string>, filters?: IQueryFilterGroup }`. Detected by `from`+`with`.

## Block Schema

Top-level requires exactly 1 element in `inputs[]`. Optional `alias` becomes SQL alias.

Every block has optional `tz?: string` (timezone) and `cast?: string` (type cast). Processing: compile → tz → cast.

## Block Kinds

### literal

`{ kind: "literal", literal: string|number|boolean|Date|null|Array }`

- Scalars → parameterized `$N`. Arrays → `($1, $2, ...)`.
- Inside `concat`/`concat_ws` parent: auto-casts (`::text`, `::boolean`, `::timestamptz`, `::jsonb`).

### column

`{ kind: "column", name: string|string[] }`

- Advanced DS: `"alias"."slug"`
- Simple DS custom fields: `"alias".data->>'<field-uuid>'` with auto-cast by field type:
  - number/money/duration(decimal≠false) → `::decimal`, (decimal=false) → `::int`
  - DB types jsonb/date/time/timestamptz/boolean/int* → `::<type>`, uuid[] → `::jsonb`
- Simple DS static/system fields (in `SIMPLE_STATIC_FIELD_SLUGS`): direct reference. Field not found → error.

### builtin

`{ kind: "builtin", name: "current_date"|"current_time"|"current_timestamp"|"now" }`

- Emitted as raw SQL. Other names → error.

### function

`{ kind: "function", name: string, inputs?: Block[] }`

- Validated against allowed functions whitelist. Inputs compiled recursively, joined by commas.
- **Gotcha:** Literal auto-cast only works inside `concat`/`concat_ws`. For `jsonb_build_object` and other functions, add explicit `"cast": "text"` to string literal blocks or Postgres will fail to determine parameter types.

### extract

`{ kind: "extract", part: "year"|"month"|"day"|"hour"|"minute"|"second", inputs: [Block] }`

- Exactly 1 input required.
- SQL: `extract(<part> from <expr>)`

### aggregate

`{ kind: "aggregate", name: "count"|"sum"|"avg"|"min"|"max"|"jsonb_agg"|"json_agg"|"array_agg", distinct?: boolean, inputs: Block[] }`

- `count` with empty or omitted inputs → `count(*)`. For count specifically, `inputs` is optional.
- `distinct` → `DISTINCT` keyword.

### math

`{ kind: "math", op: "+"|"-"|"*"|"/"|"%", inputs: Block[] }`

- Min 2 operands. Left-associative with parens: `((a op b) op c)`.

### case

`{ kind: "case", cases: [{when: Block, then: Block}], else?: Block }`

- Min 1 case required. `else` optional (defaults NULL).

### compare

`{ kind: "compare", op: "="|"!="|"<>"|">"|"<"|">="|"<="|"like"|"ilike"|"in"|"not in"|"not_in", left: Block, right: Block }`

- `in`/`not in`: `left in right`. `not_in` accepted as alias but prefer `"not in"` (with space).
- `ilike` auto-converted to `like` for MySQL dialect.

### boolean

`{ kind: "boolean", op: "and"|"or"|"not", inputs: Block[] }`

- `not`: exactly 1 input → `not (<expr>)`. `and`/`or`: min 2 → `((<a>) op (<b>))`.

## Subquery Details

- `from`: child table full slug (`appSlug_tableSlug`), matched via `dataSource.children`.
- `with` (string): child field joins to parent `id`. `with` (object): `{ childField: parentField }`.
- Simple child DS: table rewritten to `tenant_record`, fields use `data->>'uuid'` refs.
- Optional `filters` apply WHERE on child table.
- Child alias: `t0_child`. Parent alias: `t0`.

## Allowed Functions (Postgres)

**String**: length, lower, upper, substr, replace, concat, trim, ltrim, rtrim, btrim, split_part, initcap, reverse, strpos, lpad, rpad

**Number**: abs, ceil, floor, round, sqrt, power, mod, gcd, lcm, exp, ln, log, log10, log1p, pi, sign, width_bucket, trunc, greatest, least

**Date/Time**: now, age, clock_timestamp, date_part, date_trunc, extract, isfinite, justify_days, justify_hours, make_date, make_time, make_timestamp, make_timestamptz, timeofday, to_timestamp, to_char, to_date, to_time

**Utility**: coalesce

**JSON/JSONB**: jsonb_array_length, jsonb_extract_path, jsonb_extract_path_text, jsonb_object_keys, jsonb_build_object, json_build_object, jsonb_agg, json_agg, array_agg, array_to_json, row_to_json

**Aggregates**: count, sum, avg, min, max, jsonb_agg, json_agg, array_agg

## Cast Types

Allowed: int, int2, int4, int8, bigint, real, float, float4, float8, numeric, double, decimal, money, timestamp, timestamptz, date, time, interval, bool, boolean, uuid, text (+ array variants like `int[]`, `text[]`).

## Timezone

`tz` property: validated `/^[a-zA-Z0-9_]+$/`. SQL: `<expr> at time zone '<tz>'`. Column/function blocks omit outer parens.

## Validation Errors

| Condition | Error |
|---|---|
| Empty inputs | "Formula must have at least one input block" |
| >1 root input | "Multiple input blocks not yet supported" |
| Bad function | `Function "${name}" is not allowed for dialect "${dialect}"` |
| Bad aggregate | `Aggregate function "${name}" is not allowed` |
| Extract ≠1 input | "EXTRACT requires exactly one input expression" |
| Math <2 ops | "Math operations require at least 2 operands" |
| NOT ≠1 op | "NOT operation requires exactly one operand" |
| AND/OR <2 ops | "${OP} operation requires at least 2 operands" |
| CASE 0 whens | "CASE expression must have at least one WHEN clause" |
| Bad tz | "Unsupported timezone: ${tz}" |
| Bad builtin | "Unsupported formula function: ${name}" |

## SelectQueryBuilder Integration

1. Formulas in `ISelectQueryParams.formulas` as `Record<string, ISelectQueryFormula>`.
2. Column alias matching formula key → formula replaces column ref in SELECT.
3. Dispatch: `from`/`expression` → `buildBlockFormula()` (subquery), `inputs` only → `buildBlockFormula()` (inline).
4. Calculations with `func:"formula"` also route through `buildFormula()`.
5. `usedFormulas` set prevents duplicate application across SELECT and aggregations.
6. Subquery formulas trigger async `resolveChildDatasources()` before build.

## Examples

**Inline math** (balance / 100):

```json
{ "inputs": [{ "kind": "math", "op": "/", "inputs": [{ "kind": "column", "name": "balance" }, { "kind": "literal", "literal": 100 }] }] }
```

**Formatted date** (to_char):

```json
{ "inputs": [{ "kind": "function", "name": "to_char", "inputs": [{ "kind": "column", "name": "created_on" }, { "kind": "literal", "literal": "DD/MM/YYYY" }] }] }
```

**Subquery count**:

```json
{ "from": "app_child", "with": "parent_id", "inputs": [{ "kind": "aggregate", "name": "count", "inputs": [] }] }
```

**Subquery count with distinct**:

```json
{ "expression": { "from": "app_child_table", "with": "parent_field", "inputs": [{ "kind": "aggregate", "name": "count", "distinct": true, "inputs": [{ "kind": "column", "name": "id" }] }] } }
```

**Multi-field subquery join**:

```json
{ "from": "app_child", "with": { "child_field1": "parent_field1", "child_field2": "parent_field2" }, "inputs": [{ "kind": "aggregate", "name": "sum", "inputs": [{ "kind": "column", "name": "amount" }] }] }
```

**CASE with AND**:

```json
{ "inputs": [{ "kind": "case", "cases": [{ "when": { "kind": "boolean", "op": "and", "inputs": [{ "kind": "compare", "op": ">", "left": { "kind": "column", "name": "price" }, "right": { "kind": "literal", "literal": 100 } }, { "kind": "compare", "op": "ilike", "left": { "kind": "column", "name": "name" }, "right": { "kind": "literal", "literal": "%pro%" } }] }, "then": { "kind": "literal", "literal": "premium" } }], "else": { "kind": "literal", "literal": "standard" } }] }
```

**Multi-branch CASE** (tier assignment):

```json
{ "inputs": [{ "kind": "case", "cases": [{ "when": { "kind": "compare", "op": ">=", "left": { "kind": "column", "name": "revenue" }, "right": { "kind": "literal", "literal": 100000 } }, "then": { "kind": "literal", "literal": "enterprise" } }, { "when": { "kind": "compare", "op": ">=", "left": { "kind": "column", "name": "revenue" }, "right": { "kind": "literal", "literal": 10000 } }, "then": { "kind": "literal", "literal": "business" } }, { "when": { "kind": "compare", "op": ">=", "left": { "kind": "column", "name": "revenue" }, "right": { "kind": "literal", "literal": 1000 } }, "then": { "kind": "literal", "literal": "starter" } }], "else": { "kind": "literal", "literal": "free" } }] }
```

**Nested aggregate**: `round(sum(qty * price), 2)`:

```json
{ "alias": "total", "inputs": [{ "kind": "function", "name": "round", "inputs": [{ "kind": "aggregate", "name": "sum", "inputs": [{ "kind": "math", "op": "*", "inputs": [{ "kind": "column", "name": "qty" }, { "kind": "column", "name": "price" }] }] }, { "kind": "literal", "literal": 2 }] }] }
```

**Timezone**: `to_char(now() at time zone 'UTC', 'YYYY-MM-DD')`:

```json
{ "inputs": [{ "kind": "function", "name": "to_char", "inputs": [{ "kind": "function", "name": "now", "tz": "UTC" }, { "kind": "literal", "literal": "YYYY-MM-DD" }] }] }
```

**COALESCE** (null handling):

```json
{ "inputs": [{ "kind": "function", "name": "coalesce", "inputs": [{ "kind": "column", "name": "description" }, { "kind": "literal", "literal": "No description" }] }] }
```

**Subquery with filters** (count active children):

```json
{ "from": "app_child_table", "with": "parent_id", "filters": { "rules": [{ "field": "status", "operator": "=", "value": "active" }] }, "inputs": [{ "kind": "aggregate", "name": "count", "inputs": [] }] }
```

**String concatenation with initcap**:

```json
{ "inputs": [{ "kind": "function", "name": "initcap", "inputs": [{ "kind": "function", "name": "concat", "inputs": [{ "kind": "column", "name": "first_name" }, { "kind": "literal", "literal": " " }, { "kind": "column", "name": "last_name" }] }] }] }
```

**Percentage with cast**: `round(completed/total * 100, 2)`:

```json
{ "inputs": [{ "kind": "function", "name": "round", "inputs": [{ "kind": "math", "op": "*", "inputs": [{ "kind": "math", "op": "/", "inputs": [{ "kind": "column", "name": "completed_tasks", "cast": "decimal" }, { "kind": "function", "name": "greatest", "inputs": [{ "kind": "column", "name": "total_tasks", "cast": "decimal" }, { "kind": "literal", "literal": 1 }] }] }, { "kind": "literal", "literal": 100 }] }, { "kind": "literal", "literal": 2 }] }] }
```

**Days since created**: `date_part('day', age(now, created_on))::int`:

```json
{ "inputs": [{ "kind": "function", "name": "date_part", "inputs": [{ "kind": "literal", "literal": "day" }, { "kind": "function", "name": "age", "inputs": [{ "kind": "builtin", "name": "now" }, { "kind": "column", "name": "created_on" }] }], "cast": "int" }] }
```

**Boolean NOT with OR** (is_active = not archived or deleted):

```json
{ "inputs": [{ "kind": "boolean", "op": "not", "inputs": [{ "kind": "boolean", "op": "or", "inputs": [{ "kind": "compare", "op": "=", "left": { "kind": "column", "name": "is_archived" }, "right": { "kind": "literal", "literal": true } }, { "kind": "compare", "op": "=", "left": { "kind": "column", "name": "is_deleted" }, "right": { "kind": "literal", "literal": true } }] }] }] }
```

**Subquery sum with filters** (outstanding invoice amount):

```json
{ "from": "billing_invoice_line", "with": "invoice_id", "filters": { "combinator": "and", "rules": [{ "field": "status", "operator": "!=", "value": "paid", "filterType": "ALPHA" }, { "field": "amount", "operator": ">", "value": 0, "filterType": "NUMERIC" }] }, "inputs": [{ "kind": "function", "name": "coalesce", "inputs": [{ "kind": "aggregate", "name": "sum", "inputs": [{ "kind": "column", "name": "amount" }] }, { "kind": "literal", "literal": 0 }] }] }
```

**Extract year-month** (concat year + padded month):

```json
{ "inputs": [{ "kind": "function", "name": "concat", "inputs": [{ "kind": "extract", "part": "year", "inputs": [{ "kind": "column", "name": "created_on" }], "cast": "text" }, { "kind": "literal", "literal": "-" }, { "kind": "function", "name": "lpad", "inputs": [{ "kind": "extract", "part": "month", "inputs": [{ "kind": "column", "name": "created_on" }], "cast": "text" }, { "kind": "literal", "literal": 2 }, { "kind": "literal", "literal": "0" }] }] }] }
```

**JSONB extraction**:

```json
{ "inputs": [{ "kind": "function", "name": "jsonb_extract_path_text", "inputs": [{ "kind": "column", "name": "address" }, { "kind": "literal", "literal": "country" }] }] }
```

**Weighted average**: `sum(score * weight) / greatest(sum(weight), 1)`:

```json
{ "inputs": [{ "kind": "math", "op": "/", "inputs": [{ "kind": "aggregate", "name": "sum", "inputs": [{ "kind": "math", "op": "*", "inputs": [{ "kind": "column", "name": "score" }, { "kind": "column", "name": "weight" }] }] }, { "kind": "function", "name": "greatest", "inputs": [{ "kind": "aggregate", "name": "sum", "inputs": [{ "kind": "column", "name": "weight" }] }, { "kind": "literal", "literal": 1 }] }], "cast": "decimal" }] }
```

**Date truncation** (period grouping by month):

```json
{ "inputs": [{ "kind": "function", "name": "date_trunc", "inputs": [{ "kind": "literal", "literal": "month" }, { "kind": "column", "name": "order_date" }] }] }
```

**Multiple subquery formulas** (project with total + open task counts, using compat wrapper):

```json
{
  "columns": "id, name, total_tasks, open_tasks",
  "formulas": [
    {
      "key": "total_tasks",
      "expression": {
        "from": "base_task", "with": "project",
        "inputs": [{ "kind": "aggregate", "name": "count", "inputs": [{ "kind": "column", "name": "id" }] }]
      }
    },
    {
      "key": "open_tasks",
      "expression": {
        "from": "base_task", "with": "project",
        "inputs": [{ "kind": "aggregate", "name": "count", "inputs": [{ "kind": "column", "name": "id" }] }],
        "filters": { "rules": [{ "field": "status", "operator": "not_in", "value": ["<completed_uuid>", "<cancelled_uuid>"] }], "combinator": "and" }
      }
    }
  ]
}
```

→ Each formula produces a correlated subquery: `(SELECT count("t0_child"."id") FROM ... WHERE "t0_child"."project" = "t0"."id" [AND status filter])`. No GROUP BY needed.

**Combined aggregations via jsonb_build_object** (pack total + open counts into one JSON column, one subquery):

```json
{
  "key": "task_stats",
  "expression": {
    "from": "base_task", "with": "project",
    "inputs": [{
      "kind": "function", "name": "jsonb_build_object",
      "inputs": [
        { "kind": "literal", "literal": "total", "cast": "text" },
        { "kind": "aggregate", "name": "count", "inputs": [{ "kind": "column", "name": "id" }] },
        { "kind": "literal", "literal": "open", "cast": "text" },
        { "kind": "aggregate", "name": "count", "inputs": [{ "kind": "case", "cases": [{ "when": { "kind": "compare", "op": "not in", "left": { "kind": "column", "name": "status" }, "right": { "kind": "literal", "literal": ["<completed_uuid>", "<cancelled_uuid>"] } }, "then": { "kind": "column", "name": "id" } }] }] }
      ]
    }]
  }
}
```

→ Result: `{ "task_stats": { "total": 6, "open": 2 } }`. `count(CASE WHEN ... THEN id END)` skips NULLs (no `else`) to count conditionally. `"cast": "text"` on literal keys is **required** for `jsonb_build_object`.
