# SQL Style Guide For SQL-to-BI

## Purpose
Define SQL conventions that improve parser stability and semantic inference quality.

## Preferred Patterns
- Alias every projected expression with `AS`.
- Use snake_case aliases for semantic matching.
- Keep one metric intent per expression when possible.
- Keep time bucketing explicit (`DATE(ts) AS dt`, `DATE_TRUNC('week', ts) AS week_start`).
- Keep filters in `WHERE` explicit and stable.
- For date filters, prefer explicit and parseable literals:
  - string: `'2024-01-31'`, `'2024/01/31'`, `'2024-01-31 12:00:00'`
  - integer date: `20240131`
  - unix timestamp integer: `1706659200` or `1706659200000`

## Metadata In sql.md
Use optional bullet metadata above each SQL block:
- `id`: Stable identifier for joining outputs.
- `datasource`: Source connector name.
- `chart`: `auto` or explicit chart type.
- `refresh`: e.g. `5m`, `1h`, `1d`.
- `filters`: comma-separated filter dimensions.

## Anti-Patterns
- `SELECT *` for BI cards.
- Ambiguous aliases like `value`, `count` without context.
- Mixing unrelated grains in one query.
- Hidden computed fields without alias.

## Recommendation
If one SQL block is too complex for one card, split it into dedicated card-level SQL blocks.
