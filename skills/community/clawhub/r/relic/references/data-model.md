# Data model

Relic is published as a generic skill package. Private evolving user state lives in the configured vault path, not in the package tree.

## Vault files

- `manifest.json` — vault metadata
- `inbox.ndjson` — append-only observations
- `facets.json` — structured distilled facets
- `self-model.md` — narrative summary of the current self-model
- `voice.md` — language, tone, style, cadence
- `goals.md` — active and long-horizon goals
- `relationships.md` — important people, communities, entities
- `evolution/proposals/*.json` — candidate identity changes
- `snapshots/<timestamp>/...` — pre-apply snapshots
- `exports/*.md` — derived prompts and export artifacts

## Observation schema

Each `inbox.ndjson` line:

```json
{
  "id": "uuid-or-timestamp",
  "ts": "ISO-8601",
  "type": "fact|preference|value|tone|goal|memory|relationship|instruction|reflection",
  "source": "conversation|manual|import|derived",
  "text": "raw observation text",
  "tags": ["optional", "tags"],
  "confidence": 0.0,
  "meta": {}
}
```

## Distillation rules

- Keep facts separable from interpretations.
- Merge only semantically identical preferences or values.
- Preserve contradictions instead of over-flattening them.
- Filter malformed records and obvious tool/prompt noise before distillation.
- Keep `self-model.md` narrative and auditable, not transcript-shaped.

## Package boundary

The publishable package should contain only generic code, docs, handlers, and metadata.

Do not treat these as mutable runtime state:
- `SKILL.md`
- `README.md`
- `_meta.json`
- `.clawhub/origin.json`
- `scripts/`
- `references/`
- `hooks/`

All user-specific mutations belong in the configured vault only.
