# 🗄️ Supabase Skill for OpenClaw

Connect to [Supabase](https://supabase.com) for database operations, vector search, and storage management.

## What it does

- **SQL queries** - run raw SQL against your Supabase Postgres database
- **CRUD operations** - insert, select, update, upsert, delete with filters
- **Vector search** - similarity search with pgvector and embeddings
- **Table management** - list tables, describe schemas, call stored procedures

## Quick start

### Install the skill

```bash
git clone https://github.com/mvanhorn/clawdbot-skill-supabase.git ~/.openclaw/skills/supabase
```

### Set up credentials

```bash
export SUPABASE_URL="https://yourproject.supabase.co"
export SUPABASE_SERVICE_KEY="eyJhbGciOiJIUzI1NiIs..."
```

### Example chat usage

- "Query the users table for active accounts"
- "Insert a new record into the posts table"
- "Search my documents for anything about authentication"
- "Show me the schema for the orders table"
- "Run this SQL: SELECT count(*) FROM events WHERE created_at > '2024-01-01'"

## Commands

| Command | What it does |
|---------|-------------|
| `query` | Run raw SQL |
| `select` | Query with filters (--eq, --gt, --lt, --like, --limit, --order) |
| `insert` | Insert one or more rows |
| `update` | Update rows matching filters |
| `upsert` | Insert or update |
| `delete` | Delete rows matching filters |
| `vector-search` | Similarity search via pgvector |
| `tables` | List all tables |
| `describe` | Show table schema |
| `rpc` | Call a stored procedure |

## How it works

Wraps the Supabase REST API and PostgREST with a shell script CLI. Uses the service role key (bypasses RLS). Vector search requires pgvector extension and a match function in your database. Embeddings default to OpenAI's text-embedding-ada-002 (1536 dimensions).

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SUPABASE_URL` | Yes | Project URL |
| `SUPABASE_SERVICE_KEY` | Yes | Service role key |
| `OPENAI_API_KEY` | No | For generating embeddings |
| `SUPABASE_ACCESS_TOKEN` | No | Management API token |

## License

MIT
