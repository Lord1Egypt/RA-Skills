---
slug: sql-buddy
name: SQL Buddy / 自然语言 SQL 查询助手
version: 1.0.0
author: Golden Bean (coder)
category: Developer Tools
description: Convert natural language to SQL, explore database schemas, execute queries safely, and get optimization suggestions.
model: deepseek/deepseek-v4-flash
input_schema: schemas/input.schema.json
output_schema: schemas/output.schema.json
---

# SQL Buddy Skill

Convert natural language questions into SQL queries, explore database schemas, execute queries safely, and receive optimization advice. Supports SQLite, PostgreSQL, MySQL, and SQL Server.

## Core Capabilities

- **NL → SQL**: Translate Chinese/English descriptions into correct SQL
- **Schema Exploration**: Auto-discover tables, columns, types, and relationships
- **Safe Execution**: Read-only by default; DDL/DML requires explicit `--allow-write`
- **Query Optimization**: EXPLAIN plan analysis, index suggestions, performance warnings
- **Result Insight**: AI interpretation of query results (trends, anomalies)
- **Multi-Dialect**: SQLite / PostgreSQL / MySQL / MSSQL (⚠ MSSQL driver is a stub — requires pymssql)

## Security & Privacy

- Default `readonly: true` — all non-SELECT statements are intercepted
- Passwords never written to logs or history
- Connection configs stored locally at `~/.openclaw/data/sql-buddy/connections.json`
- LLM only receives table/column names and types, **never actual row data**
- Sensitive column names (`password_hash`, `secret`, `token`) are masked in schema context
- All user SQL parameters use parameterized queries (prepared statements)

## Usage

```
clawhub run sql-buddy --query "<natural language>" --connection <connection-string> [options]
```

### Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--query` | string | required | Natural language query (2-2000 chars) |
| `--connection` | string | `sqlite://./temp.db` | Connection string or JSON config |
| `--execute` | bool | false | Execute the generated SQL |
| `--explain` | bool | true | Show EXPLAIN plan |
| `--suggest-indexes` | bool | true | Suggest indexes |
| `--limit-rows` | int | 20 | Max rows to display |
| `--output-format` | enum | `table` | `table`, `json`, `csv`, `markdown` |
| `--show-schema` | bool | false | Show database schema first |
| `--direct-sql` | string | — | Skip NL→SQL, just analyze/optimize given SQL |
| `--allow-write` | bool | false | Allow INSERT/UPDATE/DELETE execution |
| `--language` | enum | `zh-CN` | `zh-CN`, `en-US` |

### Connection Format

```
sqlite:///path/to/database.db
postgresql://user:pass@host:5432/dbname
mysql://user:pass@host:3306/dbname
mssql://user:pass@host:1433/dbname
```

Or use environment variables: `DATABASE_URL` / `DB_PASSWORD`.

## Sample Prompts

### 1. Simple aggregating query (zero-config SQLite)
```text
clawhub run sql-buddy --query "最近7天注册了多少用户" \
  --connection sqlite://./app.db --execute
# → Generated SQL: SELECT COUNT(*) as new_users FROM users WHERE created_at >= DATE('now', '-7 days')
# → Result: 847 new users
```

### 2. Complex JOIN query
```text
clawhub run sql-buddy --query "每个品类上个月的销售额，按金额从高到低排序，同时显示商品数量" \
  --connection postgresql://localhost:5432/shop --execute
# → Multi-table JOIN with GROUP BY, ORDER BY, window functions
```

### 3. SQL optimization analysis
```text
clawhub run sql-buddy --direct-sql "SELECT * FROM orders JOIN users ON orders.user_id = users.id WHERE users.status = 'active'" \
  --explain --suggest-indexes
# → Full scan warning, index suggestions, optimized SQL rewrite
```

### 4. Schema exploration
```text
clawhub run sql-buddy --connection postgresql://localhost:5432/shop --show-schema
# → All tables with their columns, types, PKs, FKs, and comment hints
```

### 5. Billing analysis with result insight
```text
clawhub run sql-buddy --query "本月各区域销售额对比" \
  --connection postgresql://localhost:5432/shop --execute
# → SQL + results + AI insight: "华东区销售额环比下降15%，建议关注..."
```

## First-Success Path

```
Step 1: Install → clawhub install sql-buddy
Step 2: Connect to SQLite → clawhub run sql-buddy --query "有哪些表" --connection sqlite://./test.db
Step 3: See schema → auto-generated
Step 4: Query → clawhub run sql-buddy --query "每种状态有多少用户" --connection sqlite://./test.db --execute
Step 5: See aggregated result → "原来不用写SQL也能查数据!"
```

## Core Scripts

| File | Purpose |
|------|---------|
| `scripts/__init__.py` | Package init |
| `scripts/nl_parser.py` | Natural language → query intent extraction |
| `scripts/schema_explorer.py` | Schema discovery (tables, columns, FKs) |
| `scripts/sql_generator.py` | AI SQL generation with few-shot prompts |
| `scripts/sql_validator.py` | Syntax validation + dialect adaptation |
| `scripts/optimizer.py` | Execution plan analysis + index suggestions |
| `scripts/executor.py` | Safe query executor (read-only by default) |
| `scripts/connection_manager.py` | Connection pool + credential management |
| `scripts/result_formatter.py` | Format results as table / JSON / CSV |
| `scripts/insight_generator.py` | AI result interpretation |
| `scripts/security.py` | Password masking, SQL injection prevention |
| `scripts/drivers/` | Per-dialect driver adapters |
