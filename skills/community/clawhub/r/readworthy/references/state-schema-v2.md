# Readworthy state schema v2

## Location and ownership

Runtime state is private user data and lives outside the plugin. Resolve the directory with `scripts/state-path.mjs`; do not assume the installed skill is writable or persistent across updates.

The state directory contains:

- `state.json`: manifest and storage version.
- `profile.json`: topics, claims, preferences, reasoning lenses, and learning protocols.
- `index.json`: derived article lookup and A-item index.
- `articles/<article-id>.json`: one normalized record per unique article.
- `events.jsonl`: append-only feedback and revision events.
- `insights.json`: reusable cross-article insights.
- `backups/`: timestamped snapshots created before writes.

## Article record

Every article has this top-level shape:

```text
schema_version
id
metadata
content
analysis
  core_summary
  topics
  claims
  narrative
  decision_tradeoffs
  extras
assessment
  current
  history
feedback_ids
```

Required current fields include `metadata.title`, normalized `metadata.url`, `content.fingerprint_sha256`, arrays for topics, claims and decision tradeoffs, a current A/B/C/D recommendation, assessment history, and feedback ids.

## Claim knowledge

Each claim stores:

```json
{
  "prior_knowledge": "unknown | not_known | partially_known | known",
  "increment_type": "unknown | none | new_claim | new_context | new_evidence | new_framework | new_boundary | unsupported",
  "personal_value": "unknown | low | medium | high",
  "evidence_quality": "unknown | low | medium | high"
}
```

Do not infer broad mastery from exposure to one claim.

## Events

Each non-empty line in `events.jsonl` is an independent object containing:

- `schema_version: 2`
- `event_kind: feedback | revision`
- unique `id`
- `recorded_at`
- event-specific fields

Append corrections and point to affected article or assessment revisions. Never delete or rewrite an earlier event merely because the interpretation changed.

## Feedback protocol

`profile.json.protocols.implicit_acceptance` defaults to `disabled_until_explicit_opt_in`. Only change it after the user explicitly requests silence-based or next-request acceptance. Keep explicit feedback and Agent inference distinguishable.

## Write sequence

1. Initialize state if missing.
2. Back up state.
3. Edit durable source files or append events.
4. Rebuild the derived index after article changes.
5. Validate all state.
