# Text To Sql

[中文版](./README_zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0-blue)](SKILL.md)

> Converts natural language descriptions into syntactically correct SQL queries

## What Problem This Solves

Non-technical users know what data they want ("show me revenue by month for the top 10 customers") but can't write SQL. This skill bridges the gap — takes a schema + natural language request and produces a syntactically correct query with table aliases, proper JOINs, and GROUP BY.

**When triggered:** Database schema + natural language question + write SQL intent.

## Features

- **Schema-aware translation** — asks for table/column schema before writing queries (never invents column names)
- **Complete SQL coverage** — SELECT, WHERE, GROUP BY, ORDER BY, LIMIT, JOIN (INNER, LEFT, RIGHT), aggregate functions
- **Plain English explanation** — outputs both the query AND a one-line description of what it does
- **Multiple approach options** — `/alternatives` mode shows different JOIN strategies or subquery vs CTE approaches

## Quick Start

```bash
# Via ClawHub
clawhub install text-to-sql

# Or manually
cp -r text-to-sql ~/.openclaw/skills/
```

### Usage

```
/text-to-sql
```

Provide schema (table names + columns) and describe what data you want in English.

```
/text-to-sql/explain
```

Outputs query with inline comments explaining each clause — for learning purposes.

```
/text-to-sql/alternatives
```

Shows 2-3 different query approaches for the same question.

## Modes

| Mode | Description |
|------|-------------|
| `/text-to-sql` | Converts natural language to SQL query |
| `/text-to-sql/explain` | Query with inline comments explaining each clause |
| `/text-to-sql/alternatives` | 2-3 alternative query strategies |

## Examples

| Request | Query |
|---------|-------|
| Schema: `users(id, name)`, `orders(user_id, total)` | `SELECT u.name, SUM(o.total) FROM users u JOIN orders o ON u.id = o.user_id GROUP BY u.name` |
| "top 10 customers" | `ORDER BY total DESC LIMIT 10` added |
| "revenue by month" | `SELECT DATE_TRUNC('month', date), SUM(revenue) FROM orders GROUP BY 1` |
| No schema provided | Asks for schema first — doesn't guess column names |

## Directory Structure

```
text-to-sql/
├── SKILL.md
├── LICENSE
├── README.md
├── README_zh.md
├── CONTRIBUTING.md
├── .gitignore
├── references/       # SQL dialect cheat sheet, JOIN guide, intent mapping
└── tests/
```

## License

MIT License — see [LICENSE](LICENSE).