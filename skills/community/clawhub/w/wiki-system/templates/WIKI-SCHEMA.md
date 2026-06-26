# Wiki Schema

## Purpose
LLM-maintained knowledge wiki. Structured markdown pages with cross-references,
sourced from raw documents and research. Follows Karpathy's three-layer pattern:
Raw Sources (immutable) -> Wiki (LLM-maintained) -> Schema (this file).

## Directory Layout
- **Raw sources:** `work/wiki-sources/` (immutable after ingest, not indexed)
- **Wiki pages:** `memory/wiki/{domain}-{topic}.md` (QMD-indexed automatically)
- **Index:** `memory/wiki/index.md` (catalog of all pages, <4000 tokens)
- **Log:** `memory/wiki/log.md` (append-only activity log)
- **Ingest queue:** `work/wiki-sources/ingestion-queue.md`

## Page Naming Convention
- Lowercase kebab-case with domain prefix: `{domain}-{topic}.md`
- Domains: `bio`, `vita`, `longevity`, `tech`, `ops`, `finance`, `people`
- Examples: `bio-akash-deal.md`, `longevity-senolytics.md`, `tech-openclaw-memory.md`

## Page Template (Frontmatter Required)

```yaml
---
title: "Page Title"
domain: bio|vita|longevity|tech|ops|finance|people
created: YYYY-MM-DD
updated: YYYY-MM-DD
sources:
  - work/wiki-sources/articles/source-name.md
  - "https://url-if-web-source"
tags: [tag1, tag2]
confidence: high|medium|low
status: active|stale|archived
---
```

After frontmatter, use this structure:

```markdown
# Page Title

## Summary
2-3 sentence overview.

## Key Claims
1. Claim with source attribution
2. ...

## Open Questions
- Unresolved questions related to this topic

## Related
- [[other-wiki-page]]
- [[another-page#specific-section]]
```

## Cross-Reference Format
- Use Obsidian-style wikilinks: `[[wiki-page-slug]]`
- For section links: `[[wiki-page-slug#section-heading]]`
- All links are relative within `memory/wiki/`
- When creating or updating a page, scan existing pages for cross-reference opportunities and add links in both directions

## Index Constraints
- `memory/wiki/index.md` must stay under ~4000 tokens
- Use compact table format: `| Slug | Title | Domain | Updated | Tags |`
- If page count exceeds 80, create domain sub-indices (`index-{domain}.md`) linked from main
- Never duplicate page content in the index -- titles and metadata only

## Log Format (memory/wiki/log.md)
- Append-only, most recent at bottom
- Format: `YYYY-MM-DD HH:MM | action | page | summary`
- Actions: `ingest`, `update`, `create`, `lint-fix`, `archive`, `merge`
- Trim entries older than 90 days during lint

## Operations

### Ingest
1. Check `work/wiki-sources/ingestion-queue.md` for pending items
2. Read each source from `work/wiki-sources/` (or fetch URL)
3. Extract key claims, facts, entities, relationships
4. Create or update wiki page(s) in `memory/wiki/`
5. Add cross-references to related existing pages (both directions)
6. Update `memory/wiki/index.md`
7. Append to `memory/wiki/log.md`
8. Mark source as processed in ingestion-queue.md
9. Max 3 sources per automated run. Pages should be 200-800 words.

### Query
1. Read `memory/wiki/index.md` to check if relevant pages exist
2. Use `memory_search` or read matched pages directly
3. Synthesize answer from wiki content, citing the wiki page
4. If answer reveals a knowledge gap, add entry to `work/wiki-sources/ingestion-queue.md`

### Lint
1. Check all wiki pages for:
   - Stale `updated` dates (>30 days) -> set `status: stale`
   - Broken `[[wikilinks]]` that don't resolve to actual files
   - Orphan pages (no inbound links from other wiki pages)
   - Contradictions between pages
   - Missing frontmatter fields
2. Fix what can be fixed automatically
3. Flag what needs human review
4. Archive pages with `status: stale` older than 90 days
5. Trim log entries older than 90 days
6. Update index stats and orphan list

## Exclusion Zones (wiki operations must NOT modify these)
- `MEMORY.md` -- owned by Dreaming deep phase (setup script adds a one-time reference, but wiki operations never modify it after that)
- `DREAMS.md` -- owned by Dreaming diary
- `memory/YYYY-MM-DD.md` -- owned by daily compaction
- `memory/dreaming/` -- owned by Dreaming reports
- `memory/projects/active/` -- owned by project workflows
- `memory/decisions.log` -- owned by decision tracking
- `memory/learnings.log` -- owned by learning tracking
