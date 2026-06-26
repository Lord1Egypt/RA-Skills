# Example Memory Entry

This is an example of a memory `.md` file that the sync script (`sync_to_qdrant.py`) will chunk and embed into Qdrant.

## Format

Memory files are plain Markdown. No special frontmatter is required — the sync script uses the filename and section headings as metadata for retrieval context.

## Example: Daily log (`2026-01-15.md`)

```markdown
# 2026-01-15

## Postgres migration

Ran `ALTER TABLE memory_entries ADD COLUMN tags TEXT[]` on the `sysclaw_memory` database.
Migration succeeded. No downtime.

## Caddy reload

Reloaded Caddy after updating the reverse proxy for the new internal service.
Config validated with `caddy validate` before reload.

## Notes

- Qdrant was briefly unreachable at 14:30 — rebooted the container, resolved in 2 minutes
- TODO: add alerting for Qdrant downtime
```

## Example: Long-term fact (entry in `MEMORY.md`)

```markdown
## Infrastructure

- Proxmox cluster: 3 nodes (pve1, pve2, pve3)
- Internal DNS: Unbound on pfSense
- VLAN layout: 10.0.x.0/24 per zone (management, services, IoT)
- All services run as Docker containers under Portainer
```

## How the sync script handles these files

1. Reads the file and splits it into chunks (default: 400 tokens, 50 overlap)
2. Sends each chunk to the embedding endpoint (`EMBED_BASE_URL`)
3. Upserts vectors to the `{QDRANT_COLLECTION_PREFIX}_memory` collection
4. Records sync state in the `qdrant_sync_log` Postgres table

The `vector_search` tool queries this collection at runtime and returns the top-k most relevant chunks above the configured score threshold.
