# Workflow

## Recommended pipeline

1. Run `scripts/source_hygiene.py` to classify the source mix.
2. Run `scripts/notability_score.py` to estimate article viability.
3. Draft or trim the article.
4. Run `scripts/coi_tone_lint.py` and `scripts/deletion_risk_check.py`.
5. Use `scripts/citation_normalizer.py` to clean weak citations.
6. If needed, use `scripts/coi_rewrite.py` on suspicious paragraphs.
7. Use `scripts/sandbox_publish.py --dry-run` first, then publish to sandbox.
8. For Wikidata, use `scripts/wikidata_helper.py` to prepare starter statements.

## Interpretation shortcuts

- **strong hygiene + plausible/strong notability + low/medium deletion risk** → good sandbox candidate
- **mixed hygiene + borderline notability** → improve sourcing before publish
- **weak hygiene or high deletion risk** → do not move toward mainspace
