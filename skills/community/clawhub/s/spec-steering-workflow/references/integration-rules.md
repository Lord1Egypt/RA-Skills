# Integration Rules

## Default Position

This skill should work alone. Other skills are optional enhancements, not dependencies.

## With self-improving-agent

Use `.learnings/` for:
- mistakes
- corrections
- recurring lessons

Do not use `.learnings/` as the live state source for a spec. Current execution state still belongs in:
- `specs/`
- `steering/`

## With ontology

Ontology may be used as a derived index for:
- cross-spec relationships
- searchable task graphs
- long-lived entity links

Do not let ontology overwrite spec state. `specs/` remains the source of truth.

## With Proactive Agent

Not recommended for MVP because:
- both systems define state files
- both systems define recovery behavior
- both systems increase token load

If used together, prefer this priority:
1. `specs/` and `steering/` for execution state
2. `.learnings/` for experience logs
3. ontology for derived indexing

## Conflict Rule

When multiple systems disagree, prefer the execution protocol:
- `meta.json`
- `tasks.md`
- `handoff.md`
