# Project Architecture

ThoughtCodec is organized as a bilingual open-source skill library. Each skill has one stable folder, an English instruction file, and a Simplified Chinese instruction file.

## Directory Tree

```text
.
|-- .github/
|   |-- ISSUE_TEMPLATE/
|   |-- pull_request_template.md
|   `-- workflows/
|-- assets/
|   |-- logo.svg
|   |-- logo-mono.svg
|   |-- banner.svg
|   |-- social-preview.svg
|   `-- diagrams/
|-- catalog/
|   `-- skills.json
|-- docs/
|   |-- en/
|   `-- zh-CN/
|-- examples/
|-- scripts/
|-- skills/
|   |-- architecture-scaffolding/
|   |-- sop-instantiation/
|   |-- rule-prompt-optimizer/
|   |-- code-abstraction-encapsulation/
|   `-- personal-methodology-engine/
|-- README.md
|-- README.zh-CN.md
`-- LICENSE
```

## Skill Folder Pattern

```text
skills/<skill-id>/
|-- SKILL.md
|-- SKILL.zh-CN.md
`-- examples/
    `-- basic-usage.md
```

`SKILL.md` is the English primary version. `SKILL.zh-CN.md` is the Simplified Chinese version.
Skill-specific assets and references can be added when a skill actually needs them.

## Naming Rules

- Skill folders use lowercase kebab-case.
- Skill IDs must match the folder name and catalog entry.
- Public assets should use descriptive lowercase names.
- Chinese documentation should use `zh-CN` in the path or filename.

## Catalog Rules

Every published skill must be listed in `catalog/skills.json` with:

- `id`
- English and Chinese titles
- type: `decompression`, `compression`, or `loop`
- supported models
- English and Chinese descriptions
- English and Chinese file paths

## Visual Asset Rules

Project-level images live in `assets/`. Skill-specific visuals live in the relevant skill folder.

Required project visuals:

- `assets/logo.svg`
- `assets/logo-mono.svg`
- `assets/banner.svg`
- `assets/social-preview.svg`
- `assets/diagrams/architecture.svg`
- `assets/diagrams/decompression-compression.svg`
- `assets/diagrams/agentic-loop.svg`
