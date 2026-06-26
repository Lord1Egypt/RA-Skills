---
name: safety-kb-query
description: "安全生产法规知识库查询工具。当用户需要查标准是否存在、搜索法规、对比标准清单、查看条款内容、统计知识库规模、检查数据质量时使用。触发词：查知识库、搜法规、标准存在吗、对比标准、查条款、KB查询、safety-review、法规检索、标准时效、数据质量检查"
version: "1.0.0"
author: WorkBuddy Agent
license: MIT
tags:
  - safety
  - regulation
  - knowledge-base
  - sqlite
  - compliance
  - mining-safety
---

# Safety KB Query — 安全生产法规知识库查询工具

## Overview

This skill provides **unified, schema-adaptive query access** to the `safety-review` knowledge base (SQLite database). It eliminates the need to manually write connection scripts, guess field names, or handle encoding issues every time.

**Database location**: `~/.openclaw-autoclaw/skills/safety-review/db/knowledge.db`

## When to Use This Skill

- User asks about whether a standard/regulation exists in the knowledge base
- User needs to search for regulations by keyword, number, or title
- User wants to compare a list of standards against what's in the database (gap analysis)
- User needs to view clause content of a specific regulation
- User requests statistics or health checks on the knowledge base
- Any task involving the `safety-review` SQLite database

**Trigger phrases (Chinese)**: 查知识库、搜法规、标准有没有、对比标准、查条款、数据质量、法规检索

## How to Use

### Prerequisites

1. Detect available Python command first:
   ```bash
   python --version
   ```
   Use `python` or `python3` based on availability.

2. The knowledge base path defaults to:
   ```
   C:\Users\13503\.openclaw-autoclaw\skills\safety-review\db\knowledge.db
   ```
   Override via environment variable `KB_PATH` if needed.

### Core Commands

All commands are executed via `scripts/kb_query.py`. Output is **JSON** for programmatic consumption.

#### 1. Search Regulations (`search`)

Find regulations matching a keyword across multiple fields.

```bash
python scripts/kb_query.py search <keyword> [--mode fuzzy|exact] [--limit N]
```

| Parameter | Description | Default |
|-----------|-------------|---------|
| `keyword` | Search term (standard number, title fragment, etc.) | Required |
| `--mode` | `fuzzy` (LIKE match) or `exact` (equality) | `fuzzy` |
| `--limit` | Maximum results | `20` |

**Example scenarios:**
- "看看 GB16423 有没有" → `search GB16423`
- "搜一下紧急避险相关的" → `search 紧急避险`
- "精确查找 AQ/T 2033-2023" → `search "AQ/T 2033-2023" --mode exact`

#### 2. Check Standard Existence (`check`) ⭐ **Most Useful**

Given a list of standards, report which exist and which are missing — **the primary gap analysis tool**.

```bash
python scripts/kb_query.py check <standard1> <standard2> <standard3> ...
```

**Output fields per result:**
- `found`: boolean
- `id`: regulation ID (if found)
- `document_number`: stored document number
- `title`: regulation title (truncated)
- `status`: current status
- `text_length`: character count of full_text
- `clause_count`: number of associated clauses

**Example:**
```bash
python scripts/kb_query.py check "GB 16423" "AQ/T 2033" "AQ 2034" "国发[2010]23号"
```

#### 3. Regulation Details (`info`)

Get comprehensive info about a specific regulation by ID.

```bash
python scripts/kb_query.py info <regulation_id>
```

Returns all columns from `regulations` table + clause count + linked `std_registry` entry (if any).

#### 4. Query Clauses (`clauses`)

Retrieve clauses of a regulation, with optional filtering.

```bash
python scripts/kb_query.py clauses <regulation_id> [--filter <keyword>]
```

#### 5. Database Statistics (`stats`)

Overview of knowledge base contents.

```bash
python scripts/kb_query.py stats
```

Returns: total regulations, total clauses, total books, status breakdown, domain distribution.

#### 6. Schema Inspection (`schema`)

Auto-detect and print table structures (useful when DB schema changes).

```bash
python scripts/kb_query.py schema
```

#### 7. Data Quality Check (`conflicts`) ⭐ **Important**

Detect potential data quality issues:

- **Empty content**: Regulations with NULL or very short full_text (<100 chars)
- **No clauses**: Regulations without any associated clause records
- **Title/doc_no mismatch**: Document number suggests a topic but title doesn't match (e.g., ID:94 containing "粮油加工" instead of mining safety content)

```bash
python scripts/kb_query.py conflicts
```

## Workflow Integration

### Typical Gap Analysis Workflow (for courseware/training materials)

When user provides a document that references standards and asks "which ones are missing":

1. **Extract referenced standards** from the user's document
2. **Run `check` command** with the extracted list
3. **Present results** as a table showing: ✅ Found / ❌ Missing / ⚠️ Data Issue
4. If data issues found, run `conflicts` for deeper analysis
5. Recommend next steps (import missing ones via `safety-kb-import`)

### Typical Search Workflow

1. Run `search` with user's keywords
2. If results found, use `info` to get details on relevant entries
3. If user needs clause-level detail, use `clauses`
4. Present findings in readable format (table, summary)

## Known Limitations

- **Read-only**: This skill only queries; use `safety-kb-import` for writing
- **Encoding**: Script uses UTF-8 output; ensure terminal supports it
- **Fuzzy search performance**: On large databases (>2000 records), LIKE queries may be slower; use `--mode exact` when possible
- **Clause truncation**: `clauses` command truncates content to 200 chars for readability; use `info` to get full text

## Relationship with Other Skills

| Skill | Role |
|-------|------|
| `safety-kb-query` (this one) | **Query/read** operations only |
| `safety-kb-import` | Import/write new regulations into the database |
| `standard-update-courseware` | Update training courseware based on standard changes |

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `Database not found` | Wrong path or DB moved | Check `DEFAULT_DB_PATH` or set `KB_PATH` env var |
| `no such column` | DB schema changed | Run `schema` command to see actual columns |
| Empty search results | Keyword too specific or not in DB | Try `--mode fuzzy` with shorter keywords |
| Garbled output | Terminal encoding issue | Pipe output through `chcp 65001` (Windows) or redirect to file |

## Version History

- **1.0.0** (2026-04-25): Initial release with 7 commands (search, check, info, clauses, stats, schema, conflicts)
