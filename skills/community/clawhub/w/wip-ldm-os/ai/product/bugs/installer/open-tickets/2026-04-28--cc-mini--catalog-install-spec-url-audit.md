# Installer: catalog audit for install-spec URL field

**Date:** 2026-04-28
**Owner:** unassigned
**Status:** open
**Master plan:** [2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md](2026-04-28--cc-mini--installer-eight-interfaces-master-plan.md)

## What

Each `catalog.json` entry currently looks like:

```json
{
  "id": "memory-crystal",
  "name": "Memory Crystal",
  "npm": "@wipcomputer/memory-crystal",
  "repo": "wipcomputer/memory-crystal",
  "registryMatches": ["memory-crystal"],
  "cliMatches": ["crystal"],
  "recommended": true,
  "status": "stable"
}
```

There is no explicit field for the install-spec URL. The convention is implicit: `wip.computer/install/<id>.txt`. That works until we have a product whose slug differs from its install-spec URL, or a product that does not publish an install spec at all.

## Decision needed

Add an explicit `installSpec` field:

```json
{
  "id": "memory-crystal",
  "installSpec": "https://wip.computer/install/memory-crystal.txt"
}
```

If the field is missing, `ldm install` falls back to the implicit URL (`wip.computer/install/<id>.txt`). If the field is `null`, the product has no install spec (legacy or internal-only).

## Audit

- Walk every entry in `catalog.json`.
- For each, check whether `wip.computer/install/<id>.txt` returns 200.
- Produce a table: slug, has-spec, recommended-action.
- Add `installSpec` field to entries where the URL differs from the convention or is absent.

## Acceptance

- Catalog schema documents `installSpec` (string | null | omitted).
- Audit table is committed alongside the schema change.
- `ldm install` resolves the install spec URL via the field-or-convention rule and reports it during dry-run.

## Linked

- [Install spec URL publish pipeline](2026-04-28--cc-mini--install-spec-url-publish-pipeline.md) (this audit assumes that pipeline exists or will exist)
