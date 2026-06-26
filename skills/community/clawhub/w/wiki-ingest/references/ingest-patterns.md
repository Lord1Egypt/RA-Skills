# Ingest Patterns

Use this file for concrete templates and heuristics during source ingestion.

## Source summary template

```markdown
# Source: <title>

## Summary
2-6 sentence summary.

## Key takeaways
- durable point
- durable point

## Entities and concepts
- [[Entity A]]
- [[Concept B]]

## Claims
- specific claim that can be checked later

## Open questions
- unresolved question

## Related wiki pages
- [[Topic Page]]

## Provenance
- Author:
- Date:
- URL or local path:
```
```

## Update decision heuristic

Before creating a page, check:
- does a page already exist for the same concept under a slightly different name
- would a section in an existing page be enough
- will this page likely be linked again in the future

If not, avoid creating the page.

## Contradiction pattern

```markdown
## Tensions and contradictions
- New source claims X
- Existing page or older source claims Y
- Best current interpretation: Z
- Confidence: low | medium | high
```
```

## Log entry pattern

```markdown
## [YYYY-MM-DD] ingest | <title>
- Created: [[Source: Title]]
- Updated: [[Topic A]], [[Entity B]]
- Notes: unresolved question about <claim>
```
```
