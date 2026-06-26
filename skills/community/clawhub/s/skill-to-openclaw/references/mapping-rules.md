# Mapping Rules

## Goal

Translate a foreign or non-OpenClaw skill into an OpenClaw-compatible skill directory while preserving useful operational knowledge and preserving the source capability surface and source content as much as possible, while still dropping incompatible metadata.

## Portability

This mapping guide is meant to work across different machines and runtimes.

- Use the built-in vetting gate as the required baseline.
- External vetting helpers may be used only as optional supplemental aids.
- Do not rely on host-specific session concepts to complete the conversion.

## Source patterns

Common source patterns include:
- `.agents/skills/<name>/SKILL.md`
- single markdown skill files with sidecar docs
- Claude/Codex style skill folders
- mixed folders with `references/`, `scripts/`, `assets/`, or ad hoc docs

Do not rely on any one pattern.

## Metadata mapping

### Keep
- `name`
- `description`

### Remove or rewrite
- `allowed-tools`
- provider-specific capability declarations
- distribution-only packaging metadata
- non-OpenClaw runtime control metadata

## Content mapping

### Convert into `SKILL.md`
Keep:
- concise workflow instructions
- trigger guidance
- decision rules
- a clear capability map that preserves the source skill's major capability categories
- cautionary notes for sensitive or high-impact capabilities
- user-visible notes that explain flagged or sensitive capabilities without silently removing them
- references navigation

### Convert into `references/`
Move detailed materials such as:
- API references
- long examples
- domain notes
- schemas
- step-by-step deep dives
- source compatibility notes
- advanced capability details
- sensitive capability details that should remain available but not overload the main `SKILL.md`

### Keep scripts only when all are true
- they are understandable
- they passed vetting
- they add real value
- they fit the converted skill

If a script implementation is flagged, do not silently omit it during conversion. Report the issue in vetting output and follow the user-approved scope.

### Keep assets only when they are directly useful to the output

## Safety mapping

When security vetting reports risk:
- LOW: proceed normally
- MEDIUM: proceed only after flagged material is classified and annotated safely, and call out the remaining concern in the conversion summary
- HIGH: stop by default, unless the user explicitly asks for a salvage-only review or another narrower non-conversion review scope
- EXTREME: stop and report findings; do not proceed to conversion

Never silently preserve incompatible metadata such as unsupported frontmatter fields.

Do not silently drop a capability or flagged content merely because it is sensitive or risky. Report it during vetting, classify it clearly, and follow the user-approved scope during conversion.

## Output summary template

Use a short final summary with:
- source shape
- vetting result
- kept files
- rewritten files
- removed files
- remaining review concerns
