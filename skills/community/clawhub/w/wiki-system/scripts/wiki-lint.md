# Wiki Lint

You are running a wiki health check.

## Instructions

1. Read `WIKI-SCHEMA.md` for rules.
2. Read `memory/wiki/index.md` for the full page catalog.
3. If no pages exist yet, reply `WIKI_LINT_OK (empty wiki)`.
4. For each page listed in the index:
   a. Read the page file from `memory/wiki/`.
   b. **Frontmatter check:** Verify all required fields are present (title, domain, created, updated, sources, tags, confidence, status).
   c. **Stale check:** If `updated` is older than 30 days, set `status: stale` in frontmatter.
   d. **Broken links:** Check all `[[wikilinks]]` resolve to actual files in `memory/wiki/`.
   e. **Orphan check:** If no other wiki page links to this page, flag as orphan.
   f. **Contradiction scan:** Look for claims that directly contradict claims in other pages.
5. Check index.md is in sync with actual files on disk:
   - No phantom entries (listed but file missing)
   - No unlisted pages (file exists but not in index)
6. Trim `memory/wiki/log.md` entries older than 90 days.
7. Archive pages where `status: stale` AND `updated` older than 90 days:
   - Set `status: archived` in frontmatter
   - Remove from active index table
   - Add to an "Archived" section at bottom of index
8. Update index.md stats and orphan list.
9. Append lint results to `memory/wiki/log.md`.

## Output

Report format:
```
Wiki Lint Report
- Pages checked: N
- Stale pages flagged: N (list)
- Broken links: N (list)
- Orphan pages: N (list)
- Contradictions found: N (list)
- Log entries trimmed: N
- Pages archived: N
```

If everything is clean, reply `WIKI_LINT_OK`.
