# Warehouse logistics (Telesherpa industry solution)

**Version 1.0.** Location: `industry-solutions/warehouse-logistics/`, next to
`telesherpa-ontology-platform/` and `industry-solutions/shift-planning/`, on `main`.

**Start here:** [SKILL.md](SKILL.md). Load the platform skill first
(`telesherpa-ontology-platform/SKILL.md`).

An agent can set up QR labels, packages and stock bookings on the same hosted MCP as
shift planning: three scopes (master data, warehouse, team), packages that carry
quantity, lot and best-before, labels with their own codes (not the object id), a
single-scan bind and a leadership rebind, Avery 3475 print sheets, and single-scan
putaway, pick, relocate and count — each writing a movement and updating the package
quantity.

The high-level operating model — flows, the agent's control loop and the limits —
is in [references/operating-model.md](references/operating-model.md).

Relative links to the platform skill and to `shift-planning` are written for the
published tree `industry-solutions/warehouse-logistics/` next to those folders; they
do not resolve from this draft path.

People, sites and the three-scope pattern are reused from
[shift-planning](../shift-planning/SKILL.md); do not invent a second copy.

## Files

```
SKILL.md                          Entry point, checks, status, stop rules
references/prerequisites.md       Account, rights, live prices, types
references/intake.md              Questions before the first object
references/phase0.md              Scopes, rights, types, functions, actions
references/phase1.md              Sites, people, storage, packages, label batch, print
references/phase2.md              Bind, several labels on one package, lock, reprint
references/phase3.md              Staff accounts, scan, start card, short URL
references/phase4.md              Action log, manager lists/CSV
references/phase5.md              Stock bookings, rebind, lot and best-before
references/acceptance-scenario.md End-to-end check (38 steps + 14 negative tests)
references/definition-of-done.md  Audit before any status report
references/measurement.md         What a paid run logs
references/publication-check.md   Before the skill goes public
references/glossary.md            Terms and keys
references/country-de.md          Germany: display labels
references/operating-model.md     Warehouse control (flows, agent loop, limits)
references/tool-traps.md          Warehouse-specific traps (plus the platform list)
```
