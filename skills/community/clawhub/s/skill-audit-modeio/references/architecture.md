# skill-audit Architecture

## Goal

Provide a deterministic, static, evidence-backed repository audit workflow for pre-install screening of skills, plugins, and agent repositories.

## Layout

```text
skill-audit/
  SKILL.md
  pyproject.toml
  scripts/
    skill_safety_assessment.py
    run_repo_set.py
  modeio_skill_audit/
    cli/
      skill_safety_assessment.py
    skill_safety/
      collector.py
      engine.py
      prompt_payload.py
      repo_intel.py
      scoring.py
      validation.py
      scanners/
        capability.py
        execution.py
        prompt.py
        secret.py
        supply_chain.py
  references/
    architecture.md
    prompt-contract.md
    output-contract.md
    benchmarking.md
    repo_sets/
      fresh_holdout_repos.json
      fresh_sourcepack_repos.json
  tests/
    test_skill_safety_assessment.py
    test_skill_safety_precheck.py
```

## Boundaries

- `scripts/skill_safety_assessment.py` is the repo-local wrapper for the audit CLI.
- `modeio_skill_audit/cli/skill_safety_assessment.py` owns argparse and command routing.
- `modeio_skill_audit/skill_safety/engine.py` owns orchestration and final report assembly.
- `collector.py` owns file discovery, filtering, and scan-surface classification.
- `scanners/*` own domain-specific findings.
- `repo_intel.py` owns the GitHub OSINT precheck layer.
- `prompt_payload.py` and `validation.py` own model-assist support without changing the deterministic scan baseline.
- `scripts/run_repo_set.py` is the repeatable batch benchmark runner for maintainers, not the normal published skill flow.
- `tests/` and benchmark assets stay out of the ClawHub upload surface.

## Pipeline

1. Resolve the target repository path.
2. Run GitHub OSINT precheck when the target is a GitHub repo.
3. Collect scan-eligible files and classify prompt, executable, capability, and supply surfaces.
4. Run deterministic scanners and produce findings with stable evidence IDs.
5. Compute coverage, scoring, and suggested decision.
6. Optionally generate prompt payload, validate model output, or merge adjudication results.
