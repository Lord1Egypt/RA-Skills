---
active: true
description: "N-way cluster consolidation — produces one-fact-per-file output"
changelog: "v2 (2026-04-21): one-fact-per-file output; v1 (2026-04-16): initial single-merged-entry design"
variables:
  - cluster
---

You consolidate a cluster of 2-10 similar items (profiles or playbooks) that have accumulated over time.

## Core principle

**One fact per file.** Each output entry must contain exactly ONE atomic fact or preference (1-2 sentences). Do NOT combine unrelated facts into a single entry.

## Inputs

A cluster of items, each with: `id`, `path`, `content`. All items are the same type (all profiles OR all playbooks).

## Decision

- `keep_all` — the cluster items are already distinct single-fact entries with no redundancy. **Prefer this when items cover different topics.**
- `consolidate` — deduplicate, resolve contradictions, and split into individual facts.

If the cluster is already well-separated (each item covers a distinct topic with no overlap), return `keep_all` immediately.

### Contradiction handling

If items contradict on the same topic, keep the most recent version. Explain in `rationale`.

### Deduplication

If multiple items say the same thing in different words, keep one canonical version.

## Output schema

```json
{
  "action": "keep_all | consolidate",
  "facts": [
    {
      "slug": "kebab-case-topic",
      "body": "Single atomic fact, 1-2 sentences.",
      "source_ids": ["ids of items this fact was derived from"]
    }
  ],
  "ids_to_delete": ["ids of all original items that are being replaced"],
  "rationale": "2-3 sentences justifying the action"
}
```

For `keep_all`: `facts` is empty, `ids_to_delete` is empty.
For `consolidate`: `facts` contains one entry per distinct fact. `ids_to_delete` contains all original cluster IDs being replaced. Every original ID must appear in either `source_ids` of a fact or be explained in `rationale` as removed (contradiction/duplicate).

## Cluster

{cluster}
