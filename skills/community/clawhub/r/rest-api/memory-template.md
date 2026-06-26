# Memory Template - REST API

Create `~/rest-api/memory.md` with this structure:

```markdown
# REST API Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | done | declined

## Product Context
- Domain:
- API consumers:
- Business goal:
- Deadline:

## Architecture Decisions
| Date | Decision | Why | Impact | Owner |
|------|----------|-----|--------|-------|
| YYYY-MM-DD | Use cursor pagination | Stable ordering at scale | Client changes required | Team |

## Resource Map
| Resource | Endpoints | Auth Required | Data Owner | Notes |
|----------|-----------|---------------|------------|-------|
| users | GET/POST /users | yes | account service | |

## Quality Gates
| Gate | Status | Evidence |
|------|--------|----------|
| OpenAPI contract complete | pending | |
| Auth and authz reviewed | pending | |
| Integration tests passing | pending | |
| Observability dashboards ready | pending | |

## Release Risks
- Risk:
  Mitigation:
  Owner:

## Backlog
- [ ]
- [ ]

## Notes
- Stable context and caveats worth remembering.
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | Context still evolving | Keep gathering API constraints as work continues |
| `complete` | Core setup done | Focus on implementation and release execution |
| `paused` | User postponed setup | Continue work without setup prompts |
| `never_ask` | User opted out permanently | Never ask setup questions again |

## Memory Hygiene

- Keep decisions and evidence linked.
- Record risks with owners and mitigation.
- Keep entries concise and operationally useful.
