# Wiki Ingest

You are running a wiki ingestion cycle.

## Instructions

1. Read `WIKI-SCHEMA.md` for rules, structure, and constraints.
2. Read `work/wiki-sources/ingestion-queue.md` for pending items.
3. If the queue is empty, reply `NO_REPLY`.
4. For each pending source (max 3 per run):
   a. Read the source from `work/wiki-sources/` (or fetch URL if web source).
   b. Extract: key claims, facts, entities, relationships, dates.
   c. Check `memory/wiki/index.md` to see if an existing page covers the topic.
   d. If existing page: read it, update it (bump `updated` date, add new claims, add source to frontmatter sources list).
   e. If new topic: create new page in `memory/wiki/` using the template from WIKI-SCHEMA.md.
   f. Scan other wiki pages for cross-reference opportunities. Add `[[wikilinks]]` in both directions.
   g. Update `memory/wiki/index.md` (add/update row in table, bump stats).
   h. Append entry to `memory/wiki/log.md`.
   i. Mark source as processed in `work/wiki-sources/ingestion-queue.md` (move to Processed section with `[x]`).
5. Keep pages factual and concise. Each page should be 200-800 words.
6. Never modify files listed in Exclusion Zones (see WIKI-SCHEMA.md).
7. Use `confidence: high` only for claims with strong sourcing. Default to `medium`.

## Output

Report format:
```
Wiki Ingest Report
- Sources processed: N
- Pages created: N (list slugs)
- Pages updated: N (list slugs)
- Cross-references added: N
```

If nothing to process, reply `NO_REPLY`.
