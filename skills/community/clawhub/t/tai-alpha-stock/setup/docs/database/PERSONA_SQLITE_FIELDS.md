# Persona and meta JSON (SQLite)

## `runs` table

| Column | Purpose |
|--------|---------|
| `persona_json` | Optional JSON: `persona_ids` used and embedded `score` snapshot |
| `meta_json` | Run metadata: `lang`, `audience`, `source_policy`, `market`, `persona_requested` |

Legacy databases receive these columns via migration on `init_db()`.

## Schema file

Consolidated DDL: [`../sql/schema/tai_alpha_schema_consolidated.sql`](../sql/schema/tai_alpha_schema_consolidated.sql).
