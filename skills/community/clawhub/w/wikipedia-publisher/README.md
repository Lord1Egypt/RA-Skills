# wikipedia-publisher

A policy-safe OpenClaw skill for drafting, reviewing, de-risking, and publishing Wikipedia and Wikidata content.

## What it does

- prefers sandbox-first Wikipedia workflows
- scores notability / article viability
- flags promotional / COI-prone wording
- checks deletion-risk heuristics
- helps normalize citations and spot weak references
- supports Wikipedia article drafting, sandbox publishing, and basic Wikidata prep

## Contents

- `SKILL.md` — skill instructions and workflow
- `references/red-flags.md` — publishing risk checklist
- `references/workflow.md` — recommended script order
- `references/citation-guidelines.md` — citation cleanup guidance
- `scripts/source_hygiene.py` — citation classifier for independent vs primary/weak sources
- `scripts/notability_score.py` — rough article viability scorer
- `scripts/coi_tone_lint.py` — tone/source-risk linter for wiki drafts
- `scripts/deletion_risk_check.py` — heuristic rejection/deletion-risk checker
- `scripts/citation_fetch_enricher.py` — fetch live metadata from source URLs
- `scripts/citation_normalizer.py` — citation cleanup suggester
- `scripts/coi_rewrite.py` — neutral rewrite helper for PR-ish prose
- `scripts/sandbox_publish.py` — MediaWiki sandbox publishing helper
- `scripts/wikidata_helper.py` — starter statement generator for Wikidata
- `scripts/wiki_ref_utils.py` — shared citation parsing/classification helpers

## Quick test

```bash
./scripts/source_hygiene.py path/to/draft.wiki
./scripts/notability_score.py path/to/draft.wiki
./scripts/coi_tone_lint.py path/to/draft.wiki
./scripts/deletion_risk_check.py path/to/draft.wiki
./scripts/citation_fetch_enricher.py --draft path/to/draft.wiki --limit 3
./scripts/citation_normalizer.py path/to/draft.wiki
./scripts/coi_rewrite.py suspicious-paragraph.txt
./scripts/sandbox_publish.py --file draft.wiki --title "User:Example/Foo draft" --dry-run
./scripts/wikidata_helper.py --name "Foo" --instance-of organization --country "United Arab Emirates"
```

## Packaging

This repo contains the raw skill source. Package it with OpenClaw's skill tooling when needed.
