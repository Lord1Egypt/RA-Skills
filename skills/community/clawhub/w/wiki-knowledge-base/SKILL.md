---
name: wiki-knowledge-base
description: Build and maintain a local Markdown-based knowledge wiki with Obsidian-style double-links. Inspired by Karpathy's "let's build" approach. Use when the user wants to create a personal knowledge base, wiki, or structured information repository from research articles, competitive analysis, or domain knowledge. Triggers on phrases like "build a wiki", "knowledge base", "knowledge graph", "organize research", "wiki maintenance", "wiki lint", or when working in a directory with wiki/concepts/entities structure.
---

# Wiki Knowledge Base

Build a local, Obsidian-compatible knowledge wiki from raw research materials. Uses a concept-entity-comparison-source architecture with double-link (`[[slug]]`) networking.

## Directory Structure

```
<project-root>/
├── raw/                  # Immutable source materials (read-only)
│   └── articles/         # Web articles, reports (Obsidian Web Clipper → Markdown)
├── wiki/                 # LLM-maintained knowledge pages
│   ├── index.md          # Master directory (update after every operation)
│   ├── log.md            # Append-only operation log
│   ├── concepts/         # Abstract concepts (AI Agent, MCP Protocol, ...)
│   ├── entities/         # Concrete products/companies/tools (Smithery, Cursor, ...)
│   ├── comparisons/      # Cross-entity analysis tables
│   └── sources/          # Structured summaries of raw/ materials
└── outputs/              # Generated reports, lint results
```

## Page Format

Every wiki page requires YAML frontmatter:

```yaml
---
title: Page Title
type: concept | entity | source-summary | comparison
sources:
  - raw/articles/filename.md
related:
  - "[[related-slug]]"
created: YYYY-MM-DD
updated: YYYY-MM-DD
confidence: high | medium | low
---
```

## Naming Conventions

- **File names**: kebab-case (`ai-agent.md`, `mcp-model-context-protocol.md`)
- **Double-links**: must use slug format `[[slug]]`, never Chinese text or PascalCase
- **Source references**: plain text path to `raw/` files in frontmatter

## Four Page Types

| Type | Purpose | Example |
|------|---------|---------|
| `concept` | Abstract domain knowledge, definitions, frameworks | AI Agent, MCP Protocol, Coding Agent |
| `entity` | Specific products, companies, tools with facts/data | Smithery, Cursor, Claude Code |
| `comparison` | Side-by-side analysis tables | MCP Platform Comparison |
| `source-summary` | Structured summary of a raw article |提炼 key findings from raw/ |

**Concept vs Entity**: concept = "what is X?" (category), entity = "what is Y specifically?" (instance). This avoids duplication—define once, link everywhere.

**Three-layer distillation**: `raw/` (full articles, 10k+ words) → `wiki/sources/` (summaries, ~500 words) → `wiki/concepts/ + wiki/entities/` (structured knowledge).

## Workflow: Ingest

When new materials arrive in `raw/`:

1. Read new files in `raw/`
2. Discuss key findings with user
3. Create `wiki/sources/<slug>.md` summary with proper frontmatter
4. Create or update related concept/entity pages, extracting information from the source
5. Update `wiki/index.md` with new entries
6. Append operation to `wiki/log.md`

## Workflow: Query

When answering questions from the wiki:

1. Read `wiki/index.md` to locate relevant pages
2. Read related concept/entity/comparison pages
3. Synthesize answer using `[[slug]]` citations
4. If answer has lasting value, propose saving as a new wiki page

## Workflow: Lint

Run health checks periodically (or when asked):

1. **Contradiction detection**: Find conflicting claims across pages (e.g., different numbers for same metric)
2. **Orphan detection**: Find pages with no inbound `[[double-link]]` from other pages (index.md doesn't count)
3. **Dangling links**: Find `[[links]]` pointing to non-existent files
4. **Ambiguous links**: Find links using Chinese/PascalCase instead of slug format
5. **Missing concepts**: Find entities mentioned in text but without their own page
6. **Content quality**: Flag pages with `confidence: low` or thin content (<100 words)
7. **Source coverage**: Check that concept/entity pages link back to their source summaries

Fix strategy:
- **Dangling links**: sed batch-replace to correct slug format
- **Ambiguous links**: replace with correct slug, or remove `[]` if too generic (e.g., `[[AI]]` → plain text)
- **Orphan source pages**: add `[[source-slug]]` in corresponding concept/entity page body
- **Contradictions**: verify against source pages, unify to source-of-truth data

Save lint report to `outputs/lint-YYYY-MM-DD.md`.

## Workflow: Git

After every operation batch:
```bash
git add -A && git commit -m "<type>: <description>"
```

Commit message format: `<type>: <description>` where type is `ingest`, `lint`, `fix`, `create`.
