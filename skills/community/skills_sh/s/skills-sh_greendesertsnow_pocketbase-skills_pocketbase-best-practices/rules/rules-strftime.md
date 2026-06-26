---
title: Use strftime() for Date Arithmetic in Filter Expressions
impact: MEDIUM
impactDescription: strftime() (added in v0.36) replaces brittle string prefix comparisons on datetime fields
tags: filter, strftime, datetime, rules, v0.36
---

## Use strftime() for Date Arithmetic in Filter Expressions

PocketBase v0.36 added the `strftime()` function to the filter expression grammar. It maps directly to SQLite's [strftime](https://sqlite.org/lang_datefunc.html) and is the correct way to bucket, compare, or extract parts of a datetime field. Before v0.36 people worked around this with `~` (substring) matches against the ISO string; those workarounds are fragile (they break at midnight UTC, ignore timezones, and can't handle ranges).

**Incorrect (substring match on the ISO datetime string):**

```javascript
// ❌ "matches anything whose ISO string contains 2026-04-08" - breaks as soon
//    as your DB stores sub-second precision or you cross a month boundary
const todayPrefix = new Date().toISOString().slice(0, 10);
const results = await pb.collection("orders").getList(1, 50, {
    filter: `created ~ "${todayPrefix}"`, // ❌
});
```

**Correct (strftime with named format specifiers):**

```javascript
// "all orders created today (UTC)"
const results = await pb.collection("orders").getList(1, 50, {
    filter: `strftime('%Y-%m-%d', created) = strftime('%Y-%m-%d', @now)`,
});

// "all orders from March 2026"
await pb.collection("orders").getList(1, 50, {
    filter: `strftime('%Y-%m', created) = "2026-03"`,
});

// "orders created this hour"
await pb.collection("orders").getList(1, 50, {
    filter: `strftime('%Y-%m-%d %H', created) = strftime('%Y-%m-%d %H', @now)`,
});
```

```javascript
// Same function is available inside API rules:
//   collection "orders" - List rule:
//      @request.auth.id != "" &&
//      user = @request.auth.id &&
//      strftime('%Y-%m-%d', created) = strftime('%Y-%m-%d', @now)
```

**Common format specifiers:**

| Specifier | Meaning |
|---|---|
| `%Y` | 4-digit year |
| `%m` | month (01-12) |
| `%d` | day of month (01-31) |
| `%H` | hour (00-23) |
| `%M` | minute (00-59) |
| `%S` | second (00-59) |
| `%W` | ISO week (00-53) |
| `%j` | day of year (001-366) |
| `%w` | day of week (0=Sunday) |

**Other filter functions worth knowing:**

| Function | Use |
|---|---|
| `strftime(fmt, datetime)` | Format/extract datetime parts (v0.36+) |
| `length(field)` | Count elements in a multi-value field (file, relation, select) |
| `each(field, expr)` | Iterate over multi-value fields: `each(tags, ? ~ "urgent")` |
| `issetIf(field, val)` | Conditional presence check used in complex rules |

Reference: [Filter Syntax - Functions](https://pocketbase.io/docs/api-rules-and-filters/#filters) · [v0.36.0 release](https://github.com/pocketbase/pocketbase/releases/tag/v0.36.0)
