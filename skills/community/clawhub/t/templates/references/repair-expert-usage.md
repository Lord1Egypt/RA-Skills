# Repair Expert Usage

Use this skill before UI repair when issue JSON contains a non-empty `figma_urls` array.

Workflow:

1. Export issue JSON from the repair environment.
2. From this skill root, run `node scripts/read-figma-context.mjs`.
3. Read `summary.md`, `manifest.json`, `design-properties.json`, `code-connect.json`, and screenshots.
4. Search the repair repo for matching design-system components and existing style tokens.
5. Repair code.
6. In the repair note, report the Figma URL, canonical node id, `runDirRelative` or `manifest.runDir`, and any failed or partial URL reads.

Do not:

- Guess design intent from the URL alone.
- Claim Code Connect exists unless `code-connect.json` proves it.
- Commit `.multica/figma-context/`, `.multica/tmp/`, screenshots, raw JSON, or temporary issue JSON.
- Write a machine-specific absolute command path into reusable instructions.
- Use local absolute `runDir` as a reusable artifact reference when `runDirRelative` or `manifest.runDir` is available.
