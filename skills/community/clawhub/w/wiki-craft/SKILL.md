---
name: wikicraft
description: >
  Bootstrap and maintain a personal LLM Wiki — a persistent, compounding knowledge base
  of interlinked markdown pages that the LLM writes and maintains. Use when the user wants
  to build a knowledge base from scratch, ingest a new source into an existing wiki, query
  accumulated knowledge, or audit the wiki for gaps and contradictions.
  Triggers: "start a wiki", "build a knowledge base", "ingest this", "add to wiki",
  "what does the wiki say", "lint the wiki", "audit the wiki", "summarize this for the wiki".
license: Apache-2.0
metadata:
  author: Bruno VU
  version: "1.0.0"
  category: knowledge-management
  domain: personal-wiki
allowed-tools: Read Write Edit Bash
---

# LLM Wiki

Build and maintain a **persistent, compounding knowledge base** of interlinked markdown
files. The LLM writes and maintains the wiki. The human curates sources, asks questions,
and guides the analysis.

This is not RAG. Instead of re-deriving knowledge at query time, the LLM incrementally
builds a structured wiki that grows richer with every source added and every question
asked. Cross-references are pre-built. Contradictions are already flagged. Synthesis
already reflects everything ingested.

---

## First run — bootstrap

If `wiki/index.md` does **not** exist, the wiki is uninitialized. Ask the user:

1. **What is this wiki for?** (domain, topic, purpose)
2. **Where is the root directory?** (defaults to current working directory)
3. **What kinds of sources will you add?** (articles, PDFs, transcripts, notes…)
4. **How hands-on do you want to be during ingest?** (discuss first vs. batch silently)

Then:

1. Create `raw/` and `wiki/` directories.
2. Create `wiki/index.md` with a `# Wiki Index` heading and empty page sections.
3. Create `wiki/log.md` with a `# Log` heading.
4. Confirm the setup to the user and show them the directory layout.

---

## Directory structure

```
{root}/
  raw/          -- source documents (immutable — never modify)
  wiki/
    index.md    -- table of contents: every page with a one-line summary
    log.md      -- append-only chronological record of all operations
    *.md        -- generated pages (summaries, entities, concepts, etc.)
```

`raw/` is the user's domain. The LLM owns everything under `wiki/`.

---

## Ingest

When the user adds a source to `raw/` and asks you to process it:

1. **Read** the full source. Never modify anything in `raw/`.
2. **Discuss** key takeaways with the user before writing anything.
3. **Create a summary page** at `wiki/{source-name}.md`.
4. **Create or update concept, entity, and topic pages** for every major idea or entity
   the source touches. A single source typically touches 5–15 pages. That is normal.
5. **Add `[[wiki-links]]`** throughout every page you create or update. Links are the
   primary value of the wiki — connect aggressively.
6. **Note contradictions.** If new information disagrees with an existing claim, flag it
   on both pages: _(contradicts: [[other-page]])_
7. **Update `wiki/index.md`**: add new pages with one-line descriptions, keep sorted.
8. **Append to `wiki/log.md`**: date, source name, pages created, pages updated.

Do not write wiki pages before completing step 2.

---

## Query

When the user asks a question:

1. Read `wiki/index.md` first to find relevant pages.
2. Read those pages and synthesize an answer.
3. Cite specific wiki pages in your response.
4. If the answer is not in the wiki, say so clearly.
5. If the answer is valuable, offer to save it as a new wiki page.

Good answers should be filed back into the wiki so they compound over time. A comparison
you generated, an analysis, a connection the user discovered — these are valuable and
should not disappear into chat history.

**Output formats** — answers can take different forms depending on the question:

- Markdown page (default)
- Comparison table
- Marp slide deck (if the user has Marp)
- Matplotlib chart (for numeric data)
- Any format the user requests

---

## Lint / audit

When the user asks you to lint or audit the wiki:

- **Contradictions** — claims on different pages that disagree.
- **Orphan pages** — pages with no inbound `[[links]]` from other pages.
- **Missing pages** — concepts referenced in links that have no corresponding file.
- **Stale claims** — facts that newer sources have superseded.
- **Format violations** — pages that do not follow `templates/page.md`.
- **Missing citations** — factual claims with no `(source: ...)` reference.
- **Data gaps** — concepts that are mentioned but thin; suggest new sources to find.

Report findings as a numbered list, each with a suggested fix. Offer to apply fixes.

---

## Index format (`wiki/index.md`)

```markdown
# Wiki Index

## Summary pages
- [[source-name]] — one-line description

## Entity pages
- [[entity-name]] — one-line description

## Concept pages
- [[concept-name]] — one-line description
```

Keep entries sorted within each section.

---

## Log format (`wiki/log.md`)

Append one block per operation. Never edit existing entries.

```markdown
## [YYYY-MM-DD] ingest | Source Title

- Created: [[page-a]], [[page-b]]
- Updated: [[page-c]], [[page-d]]
- Notes: any notable contradictions, gaps, or decisions
```

The `## [YYYY-MM-DD]` prefix makes the log greppable:
`grep "^## \[" wiki/log.md | tail -5`

---

## Page format

Follow `templates/page.md`. Every page must have:

```markdown
# Page Title

**Summary**: One to two sentences.

**Sources**: Raw source files this page draws from.

**Last updated**: YYYY-MM-DD

---

Content with [[wiki-links]] throughout.

## Related pages

- [[page]]
```

- File names: lowercase, hyphens, `.md` (e.g. `machine-learning.md`)
- Every factual claim: `(source: filename.ext)`
- Contradictions: _(contradicts: [[page-name]])_
- Unsourced claims: _(needs verification)_

---

## Optional tooling

These are not required but mentioned in case the user wants them:

| Tool | Purpose |
|------|---------|
| [qmd](https://github.com/tobi/qmd) | Local search over wiki pages — BM25/vector hybrid, MCP server + CLI |
| Obsidian | Markdown editor with graph view, backlinks, Dataview, Marp plugin |
| Obsidian Web Clipper | Browser extension to clip articles to markdown |
| Marp | Markdown → slide decks; useful for presenting wiki synthesis |
| Dataview | Obsidian plugin — queries over YAML frontmatter in wiki pages |
| git | Version history and branching for the wiki directory |

---

## Rules

- **Never modify anything in `raw/`.**
- Always update `wiki/index.md` and `wiki/log.md` after every change.
- When uncertain how to categorize something, ask the user before writing.
- Write in plain language. The wiki is for the user, not for demonstration.
- Do not create wiki pages for things that belong in `raw/` (raw sources stay raw).
- Links are the primary value. Connect aggressively. A page with no outbound links
  is a missed opportunity.
