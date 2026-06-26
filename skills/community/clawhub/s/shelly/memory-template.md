# Memory Template - Shelly

Create `~/shelly/memory.md` with this structure:

```markdown
# Shelly Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Activation Preferences
- When this skill should auto-activate
- When this skill should stay silent
- Proactive vs explicit-only behavior

## Environment Context
- Local segments and reachability assumptions
- Preferred control plane (local, cloud, mixed)
- MQTT broker role and boundaries
- Risk mode (read-only, guarded writes, apply)

## Device Control Context
- Device groups and critical devices
- Component ids and validated method patterns
- Verification checks per device class

## Automation Constraints
- Rollout ordering and blast-radius limits
- Retry policy and stop conditions
- Rollback owner and rollback criteria

## Open Risks
- Reachability and latency risk
- Identity and state consistency risk
- Credential and permission risk

## Notes
- Durable decisions and validated fixes

---
*Updated: YYYY-MM-DD*
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context still evolving | Keep learning environment and control patterns |
| `complete` | Stable operating context | Focus on execution and optimization |
| `paused` | User paused setup expansion | Use existing context and ask only if blocked |
| `never_ask` | User wants no setup prompts | Do not ask setup questions unless explicitly requested |

## File Templates

Create `~/shelly/devices.md`:

```markdown
# Device Registry

## Device Name (device_id)
- Model:
- Local IP:
- Components:
- High-impact actions:
- Last verified:
```

Create `~/shelly/incidents.md`:

```markdown
# Incident Log

## YYYY-MM-DD HH:MM - Incident
- Symptom:
- Scope affected:
- Root cause hypothesis:
- Mitigation:
- Verification:
```

## Key Principles

- Keep entries concise and operational.
- Record only Shelly-relevant context.
- Never store raw credentials or unrelated private data.
