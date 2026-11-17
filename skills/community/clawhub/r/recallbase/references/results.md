# Result reference

Read this file when a RecallBase result contains unfamiliar fields or when an integration depends on the JSON contract.

## Envelope

Every CLI JSON response is one of:

- Success: `ok: true`, `meta`, and `data`
- Failure: `ok: false`, `meta`, and `error`

`meta.schemaVersion` is currently `1`. Warnings and source diagnostics can qualify an otherwise successful result.

## Query results

- `today`: `date`, a compact `summary`, `keySessions`, `continuationHints`, and `sourceCoverage`. Open the most relevant key sessions when the summary is too terse to support a useful answer.
- `search`: the normalized `query`, applied `filters`, ranked `results`, and `sourceCoverage`. Each result includes an `id`, `sourceId`, title, timestamps, snippet when available, score, and stable `uri`.
- `open`: conversation metadata, ordered `messages`, `rawEvidenceRefs`, and `diagnostics`.
- `sources`: per-source health, confidence, import time, counts, and diagnostics.

Message `text` is the main content. Optional `thinking` contains platform-visible reasoning and remains distinct from `text`. Optional `modelId`, `upstreamIds`, `attachments`, `citations`, and `media` are supporting context. Attachment and media URLs are sanitized and may omit token-like query details.

RecallBase imports are message-first. A healthy source can report `rawEvidence: 0`; judge coverage primarily from conversations, messages, health, and diagnostics.

## Useful filters

Narrow targeted searches when the user supplies the constraint:

```bash
rb search "<query>" --json --source <source-id>
rb search "<query>" --json --date YYYY-MM-DD
rb search "<query>" --json --limit <count>
```

Prefer a precise query containing distinctive nouns, exact errors, filenames, commands, or decision language. Broaden only after a narrow search fails.
