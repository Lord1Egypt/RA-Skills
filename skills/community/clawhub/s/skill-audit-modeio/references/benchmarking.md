# skill-audit Benchmarking

## Runner

Use `scripts/run_repo_set.py` to evaluate a curated repo set without changing the target repos.

```bash
python3 scripts/run_repo_set.py \
  --repo-set references/repo_sets/fresh_holdout_repos.json \
  --repos-root /path/to/local/repo-cache
```

## Repo-set format

The repo-set manifest shape is unchanged:

- JSON array
- each item includes `repo` and `label`
- `label` is typically `safe` or `risky`

## Output

The runner reports:

- decision distribution by label
- precision / recall on `reject|caution` vs `approve`
- per-repo decision, risk score, and finding counts

## Interpretation

- Use the benchmark to compare policy or scanner changes, not to replace manual review.
- Treat missing local clones as setup gaps, not product behavior regressions.
- Keep holdout and sourcepack repo sets separate so tuning does not leak into evaluation.
