---
name: word-deliverable
description: Turn financial-services outputs into a polished Word deliverable. Use when the user wants an IC memo, customer memo, internal note, diligence summary, or banker-ready .docx built from this plugin's analysis.
---

<!-- Derived from anthropics/financial-services-plugins under Apache-2.0. Modified by AIGroup for OpenClaw compatibility and banker workflow packaging. Not an official Anthropic release. -->


# Word Deliverable

Use this skill when the user wants a Word document as the final output surface for work produced by this plugin.

## Best-fit cases

- Customer memo after `customer-analysis-pack`
- Investment committee memo after `datapack-builder`
- Diligence note after `comps-analysis`, `dcf-model`, or `lbo-model`
- Internal banking brief assembled from multiple plugin outputs

## CN target pre-flight (MANDATORY when target is a Chinese-market entity)

For any CN/大陆 target (A股 / 港股中概 / 非上市内资), follow the same raw-data → provenance → analysis.md chain that `cn-client-investigation` enforces for PPT:

- The `.docx` memo MUST source every hard number from `<deliverable-dir>/analysis.md` or `<deliverable-dir>/data-provenance.md`. Do not re-derive numbers inside the docx generator.
- After the docx is written, run `validate-delivery.py` — its Gate 2c (`docx_data_audit.py`) scans the memo text and cross-checks every hard number against the provenance table. Missing rows = FAIL; block delivery.
- If a convenient machine-readable lookup helps the generator, run `extract_deck_numbers.py <deliverable_dir>` once to emit `deck-numbers.json`; memo generation code can import that instead of re-typing numbers from analysis.md.
- Cite `raw-data/{ts_code}-*.json` MCP snapshots in the memo's footnote if the memo includes banker-grade numbers (parallels PPT's Phase 3.5 requirement).

For non-CN targets, skip this pre-flight and use the generic routing below.

## Tooling preference

Prefer the bundled MiniMax-derived Word skill shipped inside this plugin:

- `minimax-docx`

Prefer `aigroup-mdtoword-mcp__markdown_to_docx` as the next routing layer for standard banker memo generation, markdown-to-Word conversion, and table-preserving `.docx` packaging.

If neither of those paths is available for any reason, fall back to the standard `docx` workflow already available in the environment.

This plugin now vendors the MiniMax DOCX skill as a convenience layer and treats `aigroup-mdtoword-mcp` as a first-class companion path for Word output. If the host already has a compatible Word / DOCX skill installed, that is also fine, but a separate MiniMax install should no longer be required for Word output after this plugin is installed.

Do not try to detect host skills by shelling out with `which`, PATH checks, or executable-name probes. These office capabilities may exist as host-routed skills even when no same-named binary is present in the shell.

Treat skill availability as a routing preference, not a shell-command discovery task.

The core rule is:

- author the document as a real `.docx`
- keep tables and headings structured
- do not stop at markdown if the user explicitly asked for Word

Preferred routing order:

1. `minimax-docx` for higher-fidelity Word generation and template-sensitive deliverables
2. `aigroup-mdtoword-mcp__markdown_to_docx` for stable banker memo and report packaging from markdown or structured content
3. environment `docx` fallback only when neither of the above is clearly available

## Workflow

### Step 1: Gather source material

Use existing outputs from this plugin first:

- `customer-analysis-pack`
- `datapack-builder`
- `comps-analysis`
- `competitive-analysis`
- `dcf-model`
- `lbo-model`
- `process-letter`

If the user already has markdown, Excel, PPT, or notes, treat them as input material rather than rewriting from scratch.

### Step 2: Choose document type

Pick the smallest document that matches the ask:

- memo
- briefing note
- IC summary
- diligence note
- board-ready written appendix

Clarify audience and tone only if needed for structure.

### Step 3: Build the `.docx`

Default structure:

```markdown
# Title
## Executive Summary
## Company Overview / Situation
## Analysis
## Risks
## Recommendation / Next Steps
## Appendix
```

Requirements:

- real section headings
- clean tables instead of pasted ASCII blocks
- explicit source notes where numbers matter
- banker-readable prose, not placeholder text
- if the content is already in markdown or tabular form, strongly prefer `aigroup-mdtoword-mcp` over manual copy/paste into ad hoc Word flows
- do not block on shell-based MiniMax detection if the host already routed you into this skill successfully

### Step 4: Keep the file lineage clean

If data came from an Excel model or analysis pack, say so in the document or delivery note.

If the user also wants a PDF, finish the Word file first, then hand off to `pdf-deliverable`.

## Output standard

Deliver:

1. a `.docx`
2. a short summary of what the document contains
3. any open assumptions or numbers still requiring verification

## Quality checklist

- the final artifact is a real `.docx`, not markdown renamed by hand
- headings and tables are readable in Word
- numbers match the underlying plugin output
- the narrative is concise and banker-usable
- no fake citations or placeholder sections remain
