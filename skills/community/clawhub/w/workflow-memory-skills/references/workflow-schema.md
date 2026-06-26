# Workflow Schema

Use this reference when creating, editing, validating, or explaining workflow files for `work-style-memory`.

## Goals

The schema should support:

- matching similar future requests
- compiling a short execution brief for the agent
- powering a local editable UI

## Recommended File Format

Store one workflow per JSON file.

Recommended filename pattern:

- `slug.json`

Recommended top-level fields:

```json
{
  "id": "pr-review",
  "name": "PR Review",
  "summary": "Review pull requests with a risk-first pass and short final summary.",
  "match": {
    "keywords": ["pr", "review", "diff", "patch"]
  },
  "steps": [
    {
      "id": "fetch",
      "title": "Fetch change context",
      "instruction": "Load the PR, changed files, and recent comments."
    },
    {
      "id": "analyze",
      "title": "Inspect risk and regressions",
      "instruction": "Prioritize behavior changes, hidden coupling, and missing tests."
    },
    {
      "id": "respond",
      "title": "Draft review output",
      "instruction": "Present findings first, then open questions, then a short summary."
    }
  ],
  "tool_preferences": [
    {
      "tool": "github",
      "purpose": "Load PR metadata and comments"
    },
    {
      "tool": "git",
      "purpose": "Inspect diffs and local code context"
    }
  ],
  "version": 1
}
```

## Field Guidance

`id`

- Stable machine-friendly identifier.
- Lowercase kebab-case is recommended.

`name`

- Human-facing title shown in the UI.

`summary`

- One sentence describing the workflow's purpose.

`match`

- `keywords`: short lexical clues that should trigger the workflow

`steps`

- Keep each step short.
- Step ids should be generated automatically by the UI or save layer.
- The `instruction` field should guide execution, not dump a transcript.

`tool_preferences`

- Optional but useful for both matching and prompt compilation.

`version`

- Increment on schema or behavior changes.

## Matching Heuristics

Suggested scoring dimensions:

- keyword overlap
- tool overlap

A simple MVP scoring approach:

1. Start with keyword overlap.
2. Add weight for matching tools.
3. If multiple workflows are close, ask before choosing.

## Prompt Compilation

When turning a workflow into a prompt or execution brief, include:

- workflow name
- current user goal
- ordered steps
- preferred tools

Do not dump the entire JSON verbatim unless the user asks for raw data. Summarize it into a brief that is fast for the model to follow.

## Save And Update Policy

Create a new workflow when:

- the task pattern is new
- the steps are materially different from existing workflows
- the user explicitly wants a new variant

Update an existing workflow when:

- intent is the same
- only summary, keywords, steps, or tool preferences changed

## Local UI Requirements

The UI should be able to edit every top-level field above without hand-editing JSON. The UI should also show:

- last updated timestamp
