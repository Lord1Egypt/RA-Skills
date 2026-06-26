# Plan Flow

Steps for `--plan` mode:

1. Detect language and suggest theme (see `references/theme-routing.md`).
2. Classify `report_class`; optionally add `archetype` only when the report clearly matches `brief`, `research`, `comparison`, or `update`.
3. For `regular-lumen` or periodic keywords, load `references/regular-report-content-rules.md`.
4. Generate `.report.md` with complete frontmatter, 3-5 useful sections, source-faithful structure, and placeholders only where data is missing.
5. Use real visual anchors only. Never use placeholder-only KPI/chart blocks; prefer callout, timeline, diagram, table, or prose scan anchors.
6. KPI values must be short, real quantitative values. If the source has no actual metric, do not render a KPI card; explanations and status words belong in prose, badges, callouts, or tables.
7. Use `theme_overrides` only for a small content-tone color hint; do not create a new design system in the IR.
8. Save as `report-<slug>.report.md`.
9. Tell the user the IR path, placeholder fields, suggested theme, and render command.
10. Stop. Do not generate HTML in `--plan` mode.

## Narrative Rhythm

`lead-block`, `section-quote`, and `action-grid` are optional prose upgrades. `claim -> explanation -> scan anchor` is a cadence, not a quota. If uncertain, keep normal paragraphs and add one clearer scan anchor instead of forcing a cadence block. Do not add more than one of `lead-block` / `section-quote` / `action-grid` by default inside the same section unless the source material clearly warrants it.
