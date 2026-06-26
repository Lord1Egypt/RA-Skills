# Fallback Rules

Retrieval must not become a blocker.

## Fall back immediately when

- `memory_search` returns no useful hits
- the hits are obviously low-relevance or noisy
- the task turns out to be low-context after all
- `memory_search` is unavailable in the current environment
- the cost of chasing more context is higher than the likely benefit

## Fallback behavior

When falling back:

1. stop retrieval expansion
2. proceed with the original skill or workflow
3. avoid dragging weak snippets into the final reasoning

## Important principle

The point of retrieval is to reduce wasted context, not to force every task through an extra search step.
