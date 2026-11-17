# Worldview Versioning (P0 upgrade, v2.0)

A world that can change is a world that can break its own rules. Worldview
versioning gives the story's setting the same discipline as code: versioned,
diffable, and auditable.

## Worldview record structure

```yaml
worldview_id: "asea"
version: "1.3.0"
schema_version: 1
core_rules:            # immutable — change requires a new major version
  - "magic obeys conservation of energy"
  - "no resurrection"
  - "the sea breathes at the equinox"
derived_rules:         # can evolve within a major version
  - "guild charters expire every 7 years"
  - "sea-folk cannot lie in their native tongue"
canon:                 # narrative facts locked in
  - chapter: "c01"
    event: "the lighthouse falls"
timeline:              # event chain, append-only
  - {chapter: "c01", ts: "y1m3d12", event: "fall of lighthouse"}
  - {chapter: "c05", ts: "y1m4d02", event: "queen's decree"}
```

## Versioning rules

| Change | Version bump | Example |
|---|---|---|
| Core rule change | major (1.x → 2.0) | allowing resurrection |
| Derived rule change | minor (1.3 → 1.4) | extending guild charter to 10 years |
| Canon/timeline append | patch (1.3.0 → 1.3.1) | recording a new chapter event |

## Diff & audit

- Every chapter generates a **worldview diff** (`git diff`-style): rules touched,
  canon appended, contradictions flagged.
- A **contradiction** is any new event that violates a core rule → the story
  engine must reject or explicitly re-version the worldview.
- Keep the worldview file in version control (or the same repo as the story) so
  every revision is traceable.

## Procedure per chapter

1. Draft events.
2. Run contradiction check against core_rules + derived_rules.
3. On pass: append canon + timeline, bump patch.
4. On fail: either revise the event (preferred) or deliberate a rule change
   (major/minor bump with explicit rationale in the diff).
