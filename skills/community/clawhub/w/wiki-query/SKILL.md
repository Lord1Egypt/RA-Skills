---
name: wiki-query
description: Answer questions from a persistent markdown knowledge wiki and file durable results back into the wiki when useful. Use when a user asks a question against an existing personal or team wiki, wants synthesis across topic, concept, entity, source, or analysis pages, needs citations grounded in the wiki, or wants high-value query results saved as reusable analysis pages instead of disappearing into chat history. Best for Obsidian-friendly, plain markdown, or git-backed wikis that accumulate knowledge over time.
---

# Wiki Query

Answer questions from a markdown knowledge wiki by reading the wiki first, synthesizing across relevant pages, and saving durable results back into the wiki when they will be useful later.

## Query workflow

1. Read `index.md` first when available
2. Identify the most relevant topic, concept, entity, source, and analysis pages
3. Synthesize from the wiki before falling back to raw source files
4. Distinguish direct support, synthesis, and uncertainty
5. Cite the relevant wiki pages and, when useful, the supporting source pages
6. Decide whether the result should be saved as a durable analysis page
7. If a new page is created, update `index.md`
8. If the wiki tracks query history, append a concise entry to `log.md`

## Query principles

Prefer answers that clearly separate:
- facts directly supported by source-backed wiki pages
- synthesis across multiple pages
- speculation, ambiguity, or unresolved questions

Do not present a smooth answer if the wiki evidence is mixed. Surface disagreement and missing evidence explicitly.

## When to save the answer

Save the result back into the wiki when it has durable value, such as:
- a comparison that would be expensive to redo
- a synthesis across many pages or sources
- a decision memo or recommendation the user may revisit
- a new framing that should influence related topic or entity pages

Do not save trivial one-off answers.

## Typical outputs

For a normal wiki query, deliver:
- a concise answer grounded in the wiki
- citations to the relevant wiki pages
- a reusable analysis page when justified
- any related `index.md` or `log.md` updates

## Quality bar

A good wiki query should:
- reduce future repeated work
- preserve traceability back to the wiki
- make uncertainty visible
- improve the wiki when the result is worth keeping

## References

Read `references/query-patterns.md` for analysis-page templates and filing heuristics.
