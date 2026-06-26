# Memory Template - Turkey

Create `~/turkey/memory.md` with this structure:

```markdown
# Turkey Trip Memory

## Status
status: ongoing
version: 1.0.0
last: YYYY-MM-DD
integration: pending | complete | paused | never_ask

## Trip Snapshot
- Dates:
- Duration:
- Arrival and departure airports:
- Travelers:
- Kids:
- Mobility notes:

## Route Direction
- Main cluster: [Istanbul / Cappadocia-Central / Aegean-West / Mediterranean / Black Sea-East / Southeast]
- Confirmed bases:
- Open route questions:
- Domestic flight tolerance: [low / medium / high]
- Driving comfort: [none / local only / road-trip ready]

## Preferences
- Trip style:
- Budget:
- Pace:
- Food priorities:
- Archaeology priorities:
- Beach priorities:
- Nightlife priorities:

## Conditions
- Entry status: [visa-free / e-Visa / consular visa / unknown]
- Heat tolerance:
- Wind sensitivity:
- Conservative-context sensitivity:
- Must-see places:
- Must-avoid:

## Bookings and Deadlines
| Item | Needed by | Status | Notes |
|------|-----------|--------|-------|
| Entry docs | | | |
| Domestic flights | | | |
| Hotels | | | |
| Balloon or tours | | | |
| Car rental | | | |
| Museum/site tickets | | | |

## Working Plan
- Current route draft:
- Backup plan:
- Last-night protection:

## Notes
- Durable observations only.
```

## Status Values

| Value | Meaning | Behavior |
|-------|---------|----------|
| `ongoing` | still learning trip shape | ask only high-impact follow-ups |
| `complete` | core context is stable | act quickly from saved defaults |
| `paused` | memory use paused | do not expand without need |
| `never_ask` | no setup prompts wanted | avoid future setup questions |

## Key Principles

- Save route logic and constraints, not casual travel chatter.
- Keep volatile booking details in the table, not scattered notes.
- Replace stale assumptions when airport, visa, or domestic-flight choices become fixed.
- Preserve region choice because it determines transport, seasonality, and budget.
