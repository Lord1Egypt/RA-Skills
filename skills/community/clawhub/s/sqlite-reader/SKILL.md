---
name: sqlite-reader
description: Read and query SQLite database files. Use when user wants to inspect or extract data from .sqlite files, especially OpenClaw's main.sqlite memory database. Supports basic SELECT queries, table listing, and schema inspection.
---

# SQLite Reader Skill

## Quick Start

To read a SQLite file:
1. Use `read_sqlite` tool (not yet implemented - need to create script first)
2. Or use the provided Python script in scripts/read_sqlite.py

## Available Tools

Currently no direct tool exists, but I'll create a Python script that can:
- List all tables in the database
- Show table schema
- Execute SELECT queries
- Export data to CSV/JSON

## Usage Examples

### List all tables
```python
python scripts/read_sqlite.py --list-tables C:\path\to\database.sqlite
```

### Show table schema
```python
python scripts/read_sqlite.py --schema C:\path\to\database.sqlite users
```

### Execute SELECT query
```python
python scripts/read_sqlite.py --query "SELECT * FROM sessions LIMIT 5" C:\path\to\database.sqlite
```

## Implementation Plan

I need to create:
1. `scripts/read_sqlite.py` - Python script for SQLite operations
2. `references/schema.md` - SQLite schema reference