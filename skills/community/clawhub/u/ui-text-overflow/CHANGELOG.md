# Changelog — ui-text-overflow

All notable changes to this skill are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and semantic versioning.

## v1.1.0 — 2026-10-08

- **Renamed** from `text-fit` to `ui-text-overflow` (Figma: `symphonia-text-fit` → `symphonia-text-overflow`).
  "Text fit" usually means scaling the font to fill a container, which this skill does not do;
  the new name also states that the skill audits user interface text.
- Descriptions now say that the skill checks text in user interface components.

## v1.0.0 — 2026-10-08

Initial draft. Seventh skill of the Typesetting Engine Skillset.

- Sibling comparison by line count, character budget, truncation with reachable full text,
  flexible containers, resilience check.
- Sources are platform requirements (Material Design 3, WCAG 2.2, Apple HIG) and Google Fonts
  Knowledge. No source was found that prescribes equal text lengths across cards; the skill says so
  and reports length differences as measurements.
- **Not yet verified:** the Figma line-count estimate (`height / line-height`) and the resilience
  check have not been run in a Figma file or in the Figma agent.
