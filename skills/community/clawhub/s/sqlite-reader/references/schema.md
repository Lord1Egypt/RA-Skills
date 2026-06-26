# SQLite Schema Reference

## Common OpenClaw Tables

### sessions table
- `id`: TEXT (primary key)
- `created_at`: INTEGER (timestamp)
- `updated_at`: INTEGER (timestamp)
- `model`: TEXT
- `context_tokens`: INTEGER
- `total_tokens`: INTEGER
- `system_sent`: BOOLEAN
- `aborted_last_run`: BOOLEAN
- `last_channel`: TEXT
- `last_to`: TEXT
- `transcript_path`: TEXT

### messages table
- `id`: TEXT
- `session_id`: TEXT (foreign key to sessions.id)
- `role`: TEXT (assistant/user/system)
- `content`: TEXT (JSON)
- `api`: TEXT
- `provider`: TEXT
- `model`: TEXT
- `stop_reason`: TEXT
- `timestamp`: INTEGER

### users table
- `id`: TEXT (primary key)
- `name`: TEXT
- `email`: TEXT
- `created_at`: INTEGER
- `last_active`: INTEGER

## PRAGMA Commands

- `PRAGMA table_info(table_name)`: Get column info
- `PRAGMA index_list(table_name)`: Get indexes
- `PRAGMA foreign_key_list(table_name)`: Get foreign keys
- `PRAGMA database_list`: List attached databases
- `PRAGMA journal_mode`: Get journal mode