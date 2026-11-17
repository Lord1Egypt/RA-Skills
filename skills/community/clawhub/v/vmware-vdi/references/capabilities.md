# vmware-vdi — Capabilities

27 MCP tools (16 read / 11 write) over the Horizon 8 Connection Server REST API. Every tool accepts an
optional `target`. Typical response tokens are estimates for a small estate; lists paginate at 50.

`list_entitlements` accepts the documented single `EntitlementInfo` object and paginated principal rows.
SID-only objects have an empty principal name and type `UNKNOWN`; malformed responses report unreadable
entitlements instead of an empty list. The pool's own `id` is never interpreted as a principal SID.

## Monitoring (6 read)
| Tool | R/W | Returns | ~tokens |
|------|:---:|---------|:------:|
| `get_vdi_health_summary` | R | session totals by state, problem-machine count, pool enabled/disabled | 80–200 |
| `list_vdi_sessions` | R | id, user, type, state, protocol, pool_id, machine_id, start_time (filter user/pool/state) | 60–500 |
| `get_vdi_session` | R | one session's projection | 40–100 |
| `list_vdi_machines` | R | id, name, pool_id, state, user, agent_version, base_image (filter pool/state) | 60–500 |
| `get_vdi_machine` | R | one machine's projection | 40–100 |
| `list_vdi_events` | R | time, severity, type, module, user, machine, message (filter severity) | 100–600 |

## Statistics (2 read)
| Tool | R/W | Returns | ~tokens |
|------|:---:|---------|:------:|
| `get_vdi_session_stats` | R | current concurrent, by-state, by-protocol, top pools | 80–200 |
| `get_desktop_pool_utilization` | R | per-pool total/available/in-use/error + utilization % | 80–300 |

## Management (7 read / 2 write)
| Tool | R/W | Notes | ~tokens |
|------|:---:|-------|:------:|
| `list_desktop_pools` / `get_desktop_pool` | R | pools: type, enabled, assignment | 60–300 |
| `list_farms` | R | RDS farms: type, enabled, server count | 40–200 |
| `list_app_pools` | R | published apps: farm, enabled, executable | 40–300 |
| `list_entitlements` | R | AD principals entitled to a pool | 40–300 |
| `list_vdi_images` | R | instant-clone base VMs + snapshots | 60–400 |
| `search_ad_users` | R | resolve AD name → SID (for `add_entitlement`) | 40–200 |
| `set_desktop_pool_enabled` | W | enable/disable pool (idempotent, preview) | 40–120 |
| `add_entitlement` / `remove_entitlement` | W | grant/revoke pool access by SID (preview) | 40–120 |

## Ops actions (6 write) — help-desk
| Tool | R/W | Risk | Blast radius |
|------|:---:|:----:|--------------|
| `send_vdi_session_message` | W | low | informational, no disruption |
| `disconnect_vdi_session` | W | medium | one session, state preserved |
| `logoff_vdi_session` | W | high | kicks the user (profile write-back) |
| `set_vdi_machine_maintenance` | W | medium | drains a machine (no new sessions) |
| `reset_vdi_machine` | W | high | hard reset — user loses unsaved state |
| `remove_vdi_machine` | W | high | removes from pool; deletes VM for instant clones |

## Tasks (1 read / 2 write)
| Tool | R/W | Notes |
|------|:---:|-------|
| `get_vdi_task_status` | R | pool-scoped task status/progress (or all tasks for the pool) |
| `push_desktop_pool_image` | W | **critical** — apply pending image; recreates EVERY desktop; preview states affected desktops + in-session users |
| `cancel_vdi_task` | W | cancel a running pool task (applied work is not rolled back) |

**Confirmation gate (MCP)**: every write above except `send_vdi_session_message` takes `confirm`
(default `false`). Without it the tool returns `{"action": "preview", "blast_radius": {...}, "hint": ...}`
and changes nothing; with it the response carries the same `blast_radius`. The older per-tool keys
(`would_affect`, `would_set`, `would_cancel`, `would_entitle`, `would_unentitle`) are still returned and
are removed in the next minor release. What each blast radius measures, and what refuses `confirm=true`
when it cannot be read:

| Tool | `blast_radius` | Refused when unreadable |
|------|----------------|-------------------------|
| `reset_vdi_machine` / `set_vdi_machine_maintenance` / `remove_vdi_machine` | machine count, ids, names, states, assigned users, pool ids; `assignment_unread` lists machines whose row has no `user`/`assigned_user` field (not read ≠ nobody assigned; reported, not refused) | a machine's `state` |
| `logoff_vdi_session` / `disconnect_vdi_session` | session count, ids, affected users | a session's user |
| `cancel_vdi_task` | task type, state, progress (read via the task GET) | task type or state |
| `set_desktop_pool_enabled` | pool id/name/type, current and new enabled state | the current enabled flag |
| `push_desktop_pool_image` | pool id/name, affected desktops + ids, `unattributed_desktops` (+ ids: machines that name no pool, so the desktop count is a lower bound), in-session count/users, occupancy | occupancy (override: `acknowledge_unknown_occupancy`); machines with no pool id (no override) |
| `add_entitlement` / `remove_entitlement` | pool id/name, principal ids, already entitled / newly entitled, or losing access / not entitled (a list-shaped entitlement answer is read across every page) | the pool's current entitlements |

**Beta note (踩坑 #36)**: REST endpoints are verified against the official Horizon Server API operation
index. GET-response *field names* are defensive (`.get()` with fallbacks) and pending validation against a
live Connection Server — a mismatch yields empty results, not a crash. First real-Horizon use should
confirm the `session`/`machine`/`pool` projections and the `apply-image` / entitlement bodies.

## Maintenance safety boundary

After a write timeout or gateway error, inspect the Horizon target before retrying: the write may already have happened. Automatic transient retries apply only to GET reads; explicit authentication recovery is separate.
