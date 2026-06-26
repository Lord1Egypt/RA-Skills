---
title: Master Filter Expression Syntax
impact: CRITICAL
impactDescription: Enables complex access control and efficient querying
tags: api-rules, filters, syntax, operators, security
---

## Master Filter Expression Syntax

PocketBase filter expressions use a specific syntax for both API rules and client-side queries. Understanding operators and composition is essential.

**Incorrect (invalid filter syntax):**

```javascript
// Wrong operator syntax
const posts = await pb.collection('posts').getList(1, 20, {
  filter: 'status == "published"'  // Wrong: == instead of =
});

// Missing quotes around strings
const posts = await pb.collection('posts').getList(1, 20, {
  filter: 'status = published'  // Wrong: unquoted string
});

// Wrong boolean logic
const posts = await pb.collection('posts').getList(1, 20, {
  filter: 'status = "published" AND featured = true'  // Wrong: AND instead of &&
});
```

**Correct (proper filter syntax):**

```javascript
// Equality and comparison operators
const posts = await pb.collection('posts').getList(1, 20, {
  filter: 'status = "published"'           // Equals
});
filter: 'views != 0'                        // Not equals
filter: 'views > 100'                       // Greater than
filter: 'views >= 100'                      // Greater or equal
filter: 'price < 50.00'                     // Less than
filter: 'created <= "2024-01-01 00:00:00"'  // Less or equal

// String operators
filter: 'title ~ "hello"'   // Contains (case-insensitive)
filter: 'title !~ "spam"'   // Does not contain

// Logical operators
filter: 'status = "published" && featured = true'   // AND
filter: 'category = "news" || category = "blog"'    // OR
filter: '(status = "draft" || status = "review") && author = "abc"'  // Grouping

// Array/multi-value operators (for select, relation fields)
filter: 'tags ?= "featured"'    // Any tag equals "featured"
filter: 'tags ?~ "tech"'        // Any tag contains "tech"

// Null checks
filter: 'deletedAt = null'      // Is null
filter: 'avatar != null'        // Is not null

// Date comparisons
filter: 'created > "2024-01-01 00:00:00"'
filter: 'created >= @now'       // Current timestamp
filter: 'expires < @today'      // Start of today (UTC)
```

**Available operators:**

| Operator | Description |
|----------|-------------|
| `=` | Equal |
| `!=` | Not equal |
| `>` `>=` `<` `<=` | Comparison |
| `~` | Contains (LIKE %value%) |
| `!~` | Does not contain |
| `?=` `?!=` `?>` `?~` | Any element matches |
| `&&` | AND |
| `\|\|` | OR |
| `()` | Grouping |

**Date macros:**
- `@now` - Current UTC datetime
- `@today` - Start of today UTC
- `@month` - Start of current month UTC
- `@year` - Start of current year UTC

**Filter functions:**
- `strftime(fmt, datetime)` - Format/extract datetime parts (v0.36+). E.g. `strftime('%Y-%m', created) = "2026-03"`. See `rules-strftime.md` for the full format specifier list.
- `length(field)` - Element count of a multi-value field (file, relation, select). E.g. `length(tags) > 0`.
- `each(field, expr)` - Iterate a multi-value field: `each(tags, ? ~ "urgent")`.
- `issetIf(field, val)` - Conditional presence check for complex rules.

Reference: [PocketBase Filters](https://pocketbase.io/docs/api-rules-and-filters/#filters-syntax)
