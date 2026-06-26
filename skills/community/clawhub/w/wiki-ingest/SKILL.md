---
name: wiki-ingest
description: Ingest new source material into a persistent markdown knowledge wiki. Use when a user adds an article, note, transcript, report, paper, meeting summary, or other source and wants the agent to summarize it, extract entities and concepts, update existing wiki pages, create justified new pages, repair cross-links, update index and log files, and record contradictions or open questions. Best for Obsidian-friendly, plain markdown, or git-backed wikis that are maintained incrementally over time.
---

# Wiki Ingest

Ingest one source into an existing markdown knowledge wiki without turning the wiki into a junk drawer. Read the source, identify durable knowledge, update the right existing pages, and create new pages only when they are clearly warranted.

## Workflow

1. Read the source material
2. Identify core topics, entities, concepts, claims, dates, and open questions
3. Inspect the relevant wiki pages before creating new ones
4. Create or update a source summary page if the wiki uses source pages
5. Update affected topic, concept, entity, and analysis pages
6. Add or repair internal links
7. Update `index.md`
8. Append a concise ingest entry to `log.md`
9. Record contradictions, uncertainty, and follow-up questions explicitly

## Page creation rule

Create a new page only when at least one of these is true:
- the concept or entity is likely to recur
- the page can become a meaningful link hub
- the content would make an existing page too broad or noisy

Otherwise, update an existing page.

## Source handling

Treat source material as read-only.

Preserve the distinction between:
- what the source says
- what the wiki already believes
- what the current synthesis suggests after combining multiple sources

Do not silently flatten contradictions.

## Required outputs

For a normal ingest, produce:
- a source summary or source page update
- updates to relevant wiki pages
- an `index.md` update
- a `log.md` entry
- a short note on contradictions, ambiguity, or next questions

## Quality bar

A good ingest should:
- increase reuse of knowledge
- strengthen cross-links
- reduce future re-reading
- keep page scope clean
- avoid speculative overreach

## References

Read `references/ingest-patterns.md` for templates and examples.
