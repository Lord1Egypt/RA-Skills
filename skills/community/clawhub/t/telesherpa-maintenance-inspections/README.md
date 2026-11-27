# Maintenance and inspection deadlines (Telesherpa industry solution)

**Version 1.0.** Location: `industry-solutions/maintenance-inspections/`, next to
`telesherpa-ontology-platform/` and `industry-solutions/shift-planning/`.

**Start here:** [SKILL.md](SKILL.md). Load the platform skill first
(`telesherpa-ontology-platform/SKILL.md`).

An agent can set up recurring inspection duties and defect reports on the same
hosted MCP as shift planning: three scopes (master data, maintenance, team),
assets with open `serviceOrder` rows as the source of truth for each due date,
lists for overdue inspections, a 30-day window from `{today}` to `{today+30}`,
all open inspections (excluding defects) and open defects, start cards on the
team door, a form that records an inspection (result, note, photos, signature,
inspection date and optional next due date) and writes the next due date back
to the same open order, and a form that reports a defect on an asset.

The high-level operating model — flows, the agent's control loop and the limits —
is in [references/operating-model.md](references/operating-model.md).

People, sites and the three-scope pattern are reused from
[shift-planning](../shift-planning/SKILL.md); do not invent a second copy.

## Files

```
SKILL.md                          Entry point, checks, status, stop rules
references/prerequisites.md       Account, rights, live prices, types
references/intake.md              Questions before the first object
references/phase0.md              Scopes, rights, types, properties
references/phase1.md              Sites, people, assets, recurring service orders
references/phase2.md              Views, start cards, record inspection, report defect
references/acceptance-scenario.md End-to-end check (17 steps + 2 negative tests)
references/definition-of-done.md  Audit before any status report
references/measurement.md         What a paid run logs
references/publication-check.md   Before the skill goes public
references/glossary.md            Terms and keys
references/country-de.md          Germany: display labels
references/operating-model.md     Maintenance control (flows, agent loop, limits)
references/tool-traps.md          Solution-specific traps (plus the platform list)
```
