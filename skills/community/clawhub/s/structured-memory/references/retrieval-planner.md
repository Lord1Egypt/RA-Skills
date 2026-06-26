# Retrieval Planner

## Default order

1. `MEMORY.md`
2. `projects/*.md`
3. `critical-facts/cards/` for execution-critical lookups about servers, services, paths, IDs, endpoints, or stable operational objects
4. `critical-facts/*.md` for raw fact scanning when the cards are missing or too sparse
5. `memory-index/by-date.json`
6. `memory-modules/` and `memory-entities/`
7. candidate daily memory files

## Query routing

### Rules or standing agreements
Check `MEMORY.md`, then project files, then `meta`.

### Project or object history
Check entity files first, then modules, then by-date index.

### Finance, legal, or organization questions
Filter by domain first, then module, then entity, then daily memory.

### Execution-critical lookups
Check in this order:
1. `critical-facts/cards/`
2. `critical-facts/*.md`
3. `projects/*.md`
4. daily memory only if needed for surrounding context

Trigger this path whenever the user asks about concrete operational facts such as servers, hosts, IPs, domains, URLs, endpoints, paths, repo locations, services, daemons, systemd units, gateways, or stable identifiers like open_id/chat_id/job id/run id/UUID.

### Unknown but clearly historical
Check top-level memory and project files first, then narrow with by-date index.
