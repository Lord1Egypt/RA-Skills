# QMD Workflow

QMD is optional. Use normal Markdown search when the `qmd` binary is unavailable
or the workspace has no relevant collection.

## Safe discovery

Inspect available indexes:

```bash
qmd status
qmd collection list
```

Use lexical search for exact terms, identifiers, and filenames:

```bash
qmd search "authentication retry policy" -n 10
```

Use a structured query for conceptual overlap:

```bash
qmd query $'intent: Find existing guidance about retry policy; exclude raw incident transcripts.\nlex: authentication retry backoff policy\nvec: reusable rules for handling transient authentication failures'
```

Search results are leads. Retrieve full documents before comparing or editing:

```bash
qmd get "#abc123"
qmd multi-get "#abc123,#def456" --format md
```

Use `--full-path` only when a filesystem tool needs the underlying path:

```bash
qmd get "#abc123" --full-path
```

## Deduplication

Compare the candidate learning with retrieved rules for:

- same condition and action;
- narrower or broader scope;
- contradictions;
- existing ownership or authority; and
- links to prior evidence.

Update an existing record when it expresses the same rule. Create a distinct
entry only when its scope or resolution is materially different.

## Mutation boundaries

Searching and retrieval are read-only. The following mutate local state and
require user intent appropriate to setup or maintenance:

```bash
qmd collection add <path> --name <name>
qmd update
qmd embed
```

After an approved Markdown write, use `qmd update` when QMD indexes that path.
Use `qmd embed` only if semantic embeddings are part of the workspace workflow.
Never add a collection, alter masks, or rebuild embeddings merely to capture one
learning.

If model-backed queries fail, use `qmd search` with stronger lexical terms. Do
not change QMD configuration as an unrequested workaround.
