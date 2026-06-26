---
name: workspace-db
description: Workspace Documentation and Tree Database Manager. SQLite-based indexing for all documentation, files, and directory structures with CSV/JSON export capabilities.
---

# Workspace Database Manager

Hybrid database solution for OpenClaw workspace documentation and file indexing.

## Features

- **docs.db**: Documentation index (256+ documents, skills, symlinks)
- **tree.db**: Directory tree structures (152+ entries)
- **Auto-Export**: CSV and JSON formats
- **Git-Ready**: Skill structure for easy publishing

## Database Schema

### docs.db
```sql
documents: id, name, path, category, description, type, has_symlink, symlink_path, last_update
skills: id, name, version, status, description, path
symlinks: id, name, target, source_path, description
categories: id, name, description, priority
```

### tree.db
```sql
tree_entries: id, root_path, relative_path, name, type, depth, parent_path, size
tree_scans: id, root_path, max_depth, total_files, total_dirs, total_symlinks
```

## Scripts

| Script | Purpose |
|--------|---------|
| `db_manager.py` | Initialize and populate docs.db |
| `tree_indexer.py` | Scan directories with tree command |
| `update_docs_db.py` | Re-scan all documentations |

## Usage

```bash
# Initialize databases
python3 scripts/db_manager.py

# Index tree structures
python3 scripts/tree_indexer.py

# Update documentation index
python3 scripts/update_docs_db.py

# Query databases
sqlite3 db/docs.db "SELECT * FROM documents WHERE category='websearch'"
sqlite3 db/tree.db "SELECT * FROM tree_entries WHERE type='symlink'"
```

## Exports

Auto-generated in workspace root:
- `db_documents.csv/json`
- `db_skills.csv/json`
- `db_symlinks.csv/json`
- `export_tree_*.csv`

## Installation

```bash
clawhub install workspace-db
```

## Requirements

- Python 3.8+
- SQLite3
- tree command (optional, for indexing)
