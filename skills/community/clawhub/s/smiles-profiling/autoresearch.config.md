# Autoresearch Configuration

## Goal
Make the `smiles_profiling` skill more reliable, more explicit about failures, and better at preserving tool-specific outputs while profiling one SMILES through SwissTargetPrediction, ADMETlab 3.0, and PK-Smart.

## Metric
- **Name**: profile_completeness
- **Direction**: higher is better
- **Calculation**: average case score across a fixed SMILES smoke corpus.
  - Valid molecules score across three sub-systems: SwissTargetPrediction, ADMETlab 3.0, and PK-Smart.
  - SwissTargetPrediction and ADMETlab each contribute 0.35 when they return structured results.
  - PK-Smart contributes 0.30 only when actual PK estimates are extracted, 0.10 when only the shell page loads.
  - Invalid molecules score 1.0 when the workflow fails gracefully without crashing.
- **Extract command**: `grep '^SCORE=' run.log | tail -1 | cut -d= -f2`

## Target Files
- `/home/openclaw/.openclaw/workspace/skills/smiles-profiling/SKILL.md` (workflow wording, ordering, failure handling)
- `/home/openclaw/.openclaw/workspace/skills/smiles-profiling/references/endpoints.md` (endpoint facts and stability notes)
- `/home/openclaw/.openclaw/workspace/skills/smiles-profiling/references/tool-notes.md` (reporting priorities and caveats)
- `/home/openclaw/.openclaw/workspace/skills/smiles-profiling/scripts/*.py` (smoke harness / parsers)
- `/home/openclaw/.openclaw/workspace/skills/smiles-profiling/benchmarks/*.tsv` (smoke corpus and expected behaviors)

## Read-Only Files
- Everything outside the `skills/smiles-profiling/` subtree
- Remote web tools and live endpoint responses

## Run Command
```bash
python3 /home/openclaw/.openclaw/workspace/skills/smiles-profiling/scripts/run_smiles_smoke.py --cases /home/openclaw/.openclaw/workspace/skills/smiles-profiling/benchmarks/smiles_smoke_cases.tsv
```

## Time Budget
- **Per experiment**: 10 minutes
- **Kill timeout**: 20 minutes

## Constraints
- Keep one change per experiment.
- Do not add third-party Python packages.
- Never modify evaluation logic to game the score.
- PK-Smart remains browser-first unless a stable API is discovered.
- Preserve explicit tool names, units, and thresholds in the final report.

## Branch
autoresearch/smiles-profiling-reliability

## Notes
- Current pain points: browser availability, host `requests`/`urllib3` breakage, endpoint parsing, and graceful handling of invalid or edge-case SMILES.
- PK-Smart is currently treated as `ui_only` in the smoke harness unless a reliable backend endpoint is found.
