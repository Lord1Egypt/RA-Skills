# Career Knowledge Vault Workflow

Use this reference when the user wants a Karpathy-style LLM wiki, Obsidian vault, reusable career knowledge base, future resume optimization, or durable interview preparation memory.

## Purpose

The career vault is a derived Markdown knowledge layer. It helps future runs reuse verified project, technology, metric, interview-story, job-target, and disclosure knowledge without re-reading every raw document from scratch.

It does not replace:

- `source-inventory.md`
- `tool-usage-log.md`
- `evidence.md`
- `run-summary.md`
- final user review for sensitive details

Raw sources remain the source of truth. The vault compiles reusable synthesis with provenance back to evidence records.

## Directory Shape

```text
career-vault/
|-- AGENTS.md
|-- index.md
|-- log.md
|-- projects/
|-- technologies/
|-- metrics/
|-- interview-stories/
|-- job-targets/
|-- disclosure/
`-- raw-sources/
```

`AGENTS.md` is the schema and operating protocol. `index.md` is the content map. `log.md` is the chronological maintenance record.

## Build Workflow

1. Create or reuse structured `evidence.json` when available. If only `evidence.md` exists, build structured records manually or with `evidence_normalizer.py` patterns before running the vault builder.
2. Run:

```bash
python3 plugins/resume-intelligence/skills/resume-intelligence/scripts/build_career_vault.py resume-runs/<run>/evidence.json --output-dir resume-runs/<run>/career-vault --run-name "<target role or run>" --run-date YYYY-MM-DD
```

3. Run:

```bash
python3 plugins/resume-intelligence/skills/resume-intelligence/scripts/vault_lint.py resume-runs/<run>/career-vault
```

4. Save the lint output as `career-vault-lint.md` when the vault is part of a delivered run.
5. Mention the vault path in `run-summary.md`.

## Page Rules

Every durable page should have:

- YAML frontmatter.
- One-sentence summary near the top.
- Focused scope: one project, one technology, one metric family, one interview story, or one job target.
- Obsidian `[[links]]` to related project and technology pages.
- Evidence links or source context references.
- Disclosure status when private, enterprise, or low-confidence evidence is involved.

Do not copy raw private documents into the vault. Store source context IDs and evidence references instead.

## Query Workflow

When answering from the vault:

1. Read `career-vault/index.md`.
2. Read only the relevant linked pages.
3. Cite the page paths and source context references used.
4. If a needed page is stale, missing evidence links, or has disclosure risk, report that before using it for final resume wording.

## Maintenance Workflow

Update the vault when:

- A new run produces stronger evidence.
- The user confirms dates, metrics, ownership, or disclosure decisions.
- A new job target changes keyword priorities.
- A project or technology page becomes stale.
- A lint pass finds orphan pages or missing evidence links.

Append `log.md` for every ingest, lint pass, major rewrite, or user confirmation.

## Obsidian Use

Obsidian is optional. The vault is plain Markdown and works in Codex, Claude, Cursor, VS Code, or any editor. Obsidian is useful for backlinks, graph view, and manual review of `[[links]]`.

Recommended Obsidian habits:

- Open `career-vault/` as a vault.
- Start from `index.md`.
- Use graph view to inspect projects, technologies, and disclosure pages.
- Keep private vaults local unless the user explicitly approves syncing or sharing.

## Scaling

Start with plain Markdown, `index.md`, and `rg`. Add vector search or RAG only if the vault becomes too large for index-driven search. The default workflow should stay local, inspectable, and easy to version with git.
