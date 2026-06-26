# Organization Research Notes

## Observed pattern from established skills

### 1. self-improving-agent
Observed structure:
- `SKILL.md`
- `references/`
- `scripts/`
- `assets/`
- dedicated runtime/workspace data directory: `.learnings/`

Important pattern:
- The skill explains the methodology.
- The persistent data does **not** live inside generic docs only.
- It uses a dedicated top-level directory for ongoing structured data.

### 2. autonomous-skill
Observed structure:
- `SKILL.md`
- `scripts/`
- `templates/`
- dedicated runtime/workspace data directory: `.autonomous/<task-name>/`

Important pattern:
- The skill defines the workflow.
- Task data is isolated in a dedicated directory.
- Multiple runs can coexist without polluting shared areas.

## Design implication for source-research

`source-research` should follow the same high-level pattern:

1. **Skill package** stores methodology, references, templates, and helper scripts.
2. **Workspace data** should live in a dedicated directory, not scattered through generic docs.
3. Generic docs may hold high-level framework notes, but canonical source-research results should live under a dedicated tree.

## Recommended dedicated workspace directory

Use a dedicated top-level directory such as:
- `.source-research/`

Recommended structure:

```text
.source-research/
  README.md
  source-pools/
    index.md
    <pool-name>.md
  acquisition/
    <pool-name>.md
  filtering/
    <pool-name>.md
  high-quality-sources/
    index.md
    <pool-name>.md
  high-quality-information/
    index.md
    <pool-name>.md
  rejections/
    index.md
    <pool-name>.md
  programs/
    README.md
```

## Why this is better

This structure cleanly separates:
- source pool definitions;
- acquisition methods/programs;
- filtering methods/programs;
- filtered high-quality sources;
- high-quality information from those sources;
- rejection conclusions;
- engineering assets.

It also avoids polluting:
- general docs;
- broad methodology directories;
- unrelated project notes.
