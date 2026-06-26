# Security Model

The router delegates to two sub-skills (datetime and scheduling) based on user intent. All tools share the same MCP server binary and security model.

## Content Sanitization

All user-provided text (event summaries, descriptions) passes through a prompt injection firewall before reaching the calendar API:

- **Event summary** — checked for injection patterns
- **Event description** — checked for injection patterns
- **Rejected content** — returns an error asking the user to rephrase

This prevents malicious content from being written to calendars via AI agents. The firewall runs locally inside the MCP server process.

## Filesystem Containment

The MCP binary reads and writes only `~/.config/temporal-cortex/`:

| File | Purpose | Created By |
|------|---------|-----------|
| `credentials.json` | OAuth tokens for calendar providers | Setup wizard / auth command |
| `config.json` | Timezone, week start, provider labels | Setup wizard / configure script |

No other filesystem paths are accessed. Verifiable by:
- Inspecting the [open-source Rust code](https://github.com/temporal-cortex/mcp)
- Running under Docker where the volume mount is the only writable path

## Network Scope

| Layer | Tools | Network Access |
|-------|-------|---------------|
| Layer 0 (discovery) | `resolve_identity` | **Platform API** (`api.temporal-cortex.com`) — resolves email to Temporal Link slug. Only available in Platform Mode. |
| Layer 1 (datetime) | `get_temporal_context`, `resolve_datetime`, `convert_timezone`, `compute_duration`, `adjust_timestamp` | **None** — pure local computation |
| Layers 2-3 (calendar ops) | `list_calendars`, `list_events`, `find_free_slots`, `check_availability`, `expand_rrule`, `get_availability`, `book_slot` | **Calendar provider APIs only** (`googleapis.com`, `graph.microsoft.com`, or CalDAV) |
| Layers 3-4 (Platform scheduling) | `query_public_availability`, `request_booking` | **Platform API** (`api.temporal-cortex.com`) — cross-user scheduling. Only available in Platform Mode. |

Scheduling tools connect only to your configured providers:
- Google Calendar: `googleapis.com`
- Microsoft Outlook: `graph.microsoft.com`
- CalDAV: your configured server endpoint

**Local Mode (default):** No calls to Temporal Cortex servers. No telemetry. All network traffic goes exclusively to your configured calendar providers.

**Platform Mode:** Three additional tools (`resolve_identity`, `query_public_availability`, `request_booking`) call `api.temporal-cortex.com` to support cross-user scheduling via Temporal Links. No credential data is included in these calls — only the email or slug being resolved. All other tools behave identically to Local Mode.

## Tool Annotations

Only `book_slot` and `request_booking` modify external state. All other tools (13/15) are read-only and idempotent — safe to retry without side effects.

| Tool | `readOnlyHint` | `destructiveHint` | `idempotentHint` | `openWorldHint` |
|------|---------------|-------------------|-------------------|-----------------|
| `book_slot` | `false` | `false` | `false` | `true` |
| `request_booking` | `false` | `false` | `false` | `true` |

- **readOnlyHint: false** — both tools create calendar events
- **destructiveHint: false** — never deletes or overwrites existing events
- **idempotentHint: false** — calling either tool twice creates two events
- **openWorldHint: true** — makes external API calls to calendar providers

## Two-Phase Commit (book_slot)

The `book_slot` tool uses Two-Phase Commit (2PC) to guarantee conflict-free booking:

1. **LOCK** — Acquire exclusive lock on the time slot
2. **VERIFY** — Check for overlapping events and active locks
3. **WRITE** — Create event in the calendar provider
4. **RELEASE** — Release the exclusive lock

If any step fails, the lock is released and the booking is aborted. No partial writes.

`request_booking` follows the same protocol when booking on behalf of an external attendee via a Temporal Link.
