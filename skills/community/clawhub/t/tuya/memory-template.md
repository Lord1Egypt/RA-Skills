# Memory Template - Tuya Smart

Create `~/tuya/memory.md` with this structure:

```markdown
# Tuya Smart Memory

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
- Project name and data center
- OpenAPI endpoint in use
- Account-linking model in use
- Risk mode (read-only, guarded writes, apply)

## Device Control Context
- Device groups and critical devices
- Known command codes and constraints
- Verification checks per device category

## Automation Constraints
- Rollout ordering and blast-radius limits
- Retry policy and stop conditions
- Rollback owner and rollback criteria

## Open Risks
- Auth/signing reliability risk
- Account-linking consistency risk
- Device state drift risk

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

Create `~/tuya/devices.md`:

```markdown
# Device Registry

## Device Name (device_id)
- Product category:
- Region:
- Capability codes:
- Safety classification:
- Last verified:
```

Create `~/tuya/incidents.md`:

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
- Record only Tuya-relevant context.
- Never store raw credentials or unrelated private data.
