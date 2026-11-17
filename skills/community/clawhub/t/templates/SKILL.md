---
name: read-figma-design
description: Read Figma design context from Multica issue figma_urls without Figma MCP.
---

# Read Figma Design

Use this skill when a Multica issue contains non-empty `figma_urls`.

This is a pure skill. The scripts do all deterministic work: token handling, Figma REST reads, screenshots, node expansion, style extraction, Code Connect clues, and artifact writing.

## Required Workflow

Run from this skill root before repairing UI code:

```bash
node scripts/read-figma-context.mjs \
  --issue-json <repair-repo>/.multica/tmp/<issue-id>.json \
  --out <repair-repo>/.multica/figma-context \
  --repo <repair-repo>
```

For a single URL:

```bash
node scripts/read-figma-context.mjs \
  --url "https://www.figma.com/design/<fileKey>/<fileName>?node-id=<node-id>" \
  --out <repair-repo>/.multica/figma-context \
  --repo <repair-repo>
```

For a direct smoke or manual URL:

```bash
node scripts/read-figma-context.mjs \
  --url "https://www.figma.com/design/<fileKey>/<fileName>?node-id=<node-id>" \
  --out <repair-repo>/.multica/figma-context \
  --repo <repair-repo>
```

Then read, in this order:

1. `summary.md`
2. `manifest.json`
3. `urls/<ordinal>/design-properties.json`
4. `urls/<ordinal>/code-connect.json`
5. `urls/<ordinal>/screenshots/`
6. `urls/<ordinal>/css-hints.css`

Validate artifacts manually when needed:

```bash
node scripts/validate-artifact.mjs <artifact-run-dir>
```

Offline diagnostics:

```bash
node scripts/read-figma-context.mjs --help
node scripts/read-figma-context.mjs --version
```

Both commands run without reading credentials or network.
`--help` runs without reading credentials or network.
`--version` runs without reading credentials or network.

Run a real API smoke before declaring this skill usable in a new environment:

```bash
node scripts/smoke-figma-context.mjs \
  --url "https://www.figma.com/design/VSfJU5zJ10wSdeMu2vk1Ar/New-workflow_Sensitive-Industry--Configuration_Age-Gating?node-id=6127-21193" \
  --out <repair-repo>/.multica/figma-context \
  --repo <repair-repo> \
  --env-file ../../.env
```

## Hard Rules

- Do not guess design intent from the URL alone.
- Read the generated artifacts before changing UI code.
- Cite the Figma URL, canonical node id, and artifact path in the repair notes.
- If parsing or Figma reading fails, report the stable error code and do not claim the design was used.
- Code Connect is best effort by default; do not turn `unavailable` into `unmapped`.
- Prefer local design-system components and tokens before custom CSS.
- Do not expose tokens in logs, comments, artifacts, or repair notes.
- Do not commit `.multica/figma-context/` or `.multica/tmp/`.
