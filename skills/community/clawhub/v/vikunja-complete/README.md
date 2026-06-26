# vikunja-complete

Production-grade Vikunja skill for LLM/agent workflows.

## What this provides

A deterministic CLI-backed skill with strong validation and operational safety:

- Core task ops: `health`, `list`, `create`, `update`, `move`, `complete`, `bulk-update`
- Collaboration ops: comments, labels, assignees
- Structure ops: views, buckets
- Integrations: webhooks
- V0.4 ops: attachments, relations, saved filters, notifications, subscriptions, tokens

## Install / Runtime Requirements

- `curl`
- `jq`
- Environment variables:
  - `VIKUNJA_URL`
  - `VIKUNJA_TOKEN`

## Skill entrypoint

- Skill spec: `skills/vikunja/SKILL.md`
- CLI script: `skills/vikunja/scripts/vikunja.sh`

## Quick start

```bash
export VIKUNJA_URL="https://your-vikunja-host"
export VIKUNJA_TOKEN="<token>"

./skills/vikunja/scripts/vikunja.sh health
./skills/vikunja/scripts/vikunja.sh list --limit 10
```

## Versioning

- Current version: `VERSION`
- Release history: `CHANGELOG.md`

