# Result Trimming

Retrieval is useful only if the expanded context stays small and relevant.

## Default retrieval budget

- start with top 1-3 results
- inspect snippets first
- only fetch deeper content for 1-2 clearly relevant hits

## What to keep

Prefer keeping only:

- facts directly relevant to the current task
- the most recent explicit decision
- the specific prior conclusion that prevents repeated work

## What to avoid

Avoid:

- expanding every hit just because it matched
- loading entire project histories when only one fact is needed
- carrying forward stale or weakly related snippets

## Goal

Use retrieval to patch missing context, not to replace all reasoning with a large memory dump.
