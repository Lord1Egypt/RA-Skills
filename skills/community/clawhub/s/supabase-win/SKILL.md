---
name: supabase-query
description: Query Supabase cloud database via REST API using project ID and anon key. Use when the user needs to query their Supabase database, inspect table schemas, or retrieve data. Only supports read operations for security.
license: MIT
compatibility: Requires Python 3.x and Windows with PowerShell or CMD. No database drivers needed.
metadata:
  author: user
  version: "2.0"
---

# Supabase Query Skill

This skill allows AI agents to query Supabase cloud database via REST API using only project ID and anon key.

## Security Features

- **Cloud-native**: Uses Supabase REST API, no direct database connection
- **Read-only operations**: Only SELECT-style queries via HTTP GET
- **Row limit**: Maximum 200 rows returned per query
- **Timeout protection**: 30-second request timeout
- **Local config**: Credentials stored in local `.env` file (not in version control)

## Prerequisites

1. Python 3.x installed
2. Supabase project with API access enabled

## Setup

1. Copy `references/.env.example` to `references/.env`
2. Fill in your Supabase credentials in `references/.env`:
   - `SUPABASE_PROJECT_ID`: Your Supabase project ID (from project URL)
   - `SUPABASE_ANON_KEY`: Your anon/public API key (from Settings → API)

## Usage

Run the query script from the skill directory:

```bash
python scripts/query.py "users" --select "*" --limit 10
```

Or on Windows:

```batch
scripts\query.bat users --select "*" --limit 10
```

## Output Format

The script returns JSON:

```json
{
  "success": true,
  "table": "users",
  "rows": [...],
  "row_count": 10,
  "truncated": false
}
```

Error response:

```json
{
  "success": false,
  "error": "Error message here"
}
```

## Examples

### Query all columns
```bash
python scripts/query.py "users" --select "*" --limit 20
```

### Query specific columns with filter
```bash
python scripts/query.py "users" --select "id,name,email" --eq "status:active" --limit 10
```

### Query with ordering
```bash
python scripts/query.py "posts" --select "title,created_at" --order "created_at.desc" --limit 5
```

## Troubleshooting

- **"Config file not found"**: Create `references/.env` from the example file
- **"Connection failed"**: Check your project ID and anon key
- **"Table not found"**: Verify the table name and RLS policies
- **"Permission denied"**: Check if anon key has access to the table (RLS settings)
