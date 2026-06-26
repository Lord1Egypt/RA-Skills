# Interface Contract

Use this file when building an agent-facing retrieval wrapper.

## Goal

Give agents one stable search entrypoint so they do not need to understand indexing internals.

## Recommended wrapper responsibilities

The wrapper should:
- accept a free-text query
- accept an agent id
- optionally accept a corpus id
- enforce allowlist rules
- return machine-friendly output
- fail clearly when access is denied or retrieval fails

The wrapper should not:
- expose raw implementation complexity to every caller
- let agents bypass corpus policy
- silently widen corpus scope

## Recommended CLI shape

```bash
node retrieval/scripts/workspace_search.mjs "weekly mock plan" --agent interview-trainer --json
```

Optional flags:
- `--corpus <id>`
- `--top-k <n>`
- `--semantic-k <n>`
- `--alpha <float>`
- `--json`
- `--text`

## Recommended JSON response

```json
{
  "query": "weekly mock plan",
  "agent": "interview-trainer",
  "corpus": null,
  "effectiveCorpora": ["workspace-core", "workspace-interview"],
  "topK": 5,
  "semanticK": 40,
  "alpha": 0.55,
  "results": [
    {
      "corpus": "workspace-interview",
      "path": "workspace-interview/plans/weekly-mock-plan.md",
      "title": "Weekly Mock Plan",
      "heading": "Current Recommendation",
      "startLine": 120,
      "endLine": 148,
      "snippet": "...",
      "scores": {
        "hybrid": 1.14,
        "semantic": 0.62,
        "lexical": 0.67,
        "ruleBoost": 0.50
      }
    }
  ]
}
```

## Error contract

Preferred failure modes:
- no corpora allowed for the agent
- requested corpus is not allowed
- index missing
- retrieval backend exits non-zero

Return a readable error message and non-zero exit status.

## Practical recommendation

Keep this wrapper as the compatibility layer even if the indexing backend changes later.
