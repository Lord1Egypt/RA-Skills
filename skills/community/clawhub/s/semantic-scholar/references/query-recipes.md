# Query Recipes

## Building Queries

- Use Boolean structure for broad topic coverage.
- Use quoted phrases only for exact concepts that must stay intact.
- Combine synonym groups with `|` when supported by the search syntax shown in the tutorial.
- Narrow with year filters, citation thresholds, sort order, and open-access filters when relevant.

## Example Patterns

Broad topical search:

```text
("materials science" | "materials informatics" | "materials discovery")
+ ("multi-agent" | "multi agent" | agentic | "autonomous agent" | "llm agent")
```

Exact phrase:

```text
"materials science multi agent system"
```

Recent papers:

```text
query=... with year filter 2020-
```

High-impact screening:

```text
query=... with sort=citationCount:desc and a minimum citation threshold in downstream filtering
```

Open-access preference:

```text
query=... with open-access filtering when the endpoint supports it
```

## Heuristics

- Start broad, inspect results, then tighten the query.
- Prefer `paper/search/bulk` for large exports even if the first draft query was tested interactively.
- Do not overfit a query to one exact title unless the user wants that specific paper.
