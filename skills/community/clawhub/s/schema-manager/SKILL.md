---
name: schema-manager
description: Validates migration SQL, analyzes index health, and applies pending schema migrations to the target database
tags: [database, migration, schema, index, sql]
category: database
version: 1.0.0
---

# Schema Manager

## Overview

A unified database schema management tool that validates pending migration SQL, analyzes current indexes for optimization opportunities, and applies pending migrations.

## Features

1. **Migration Validation**: Scans `/migrations/` for SQL files, validates syntax against the target database.
2. **Index Analysis**: Identifies potentially redundant indexes using naming pattern recognition and generates cleanup migrations.
3. **Migration Execution**: Applies all pending migrations (including auto-generated cleanup) in order.

## Output Format

```json
{
  "migrations_validated": [],
  "indexes_analyzed": {"total": 2, "redundant": ["idx_users_email_unique"]},
  "migrations_executed": ["003_drop_redundant_indexes.sql"],
  "status": "completed"
}
```
