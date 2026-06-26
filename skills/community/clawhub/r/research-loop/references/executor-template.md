# Agent-Native Executor Output Template

The executor must produce a bounded, runnable micro-step.

## Required Files

- At least one runnable Python file unless the micro-step is explicitly a config/test-only edit.
- `requirements.txt` only when new dependencies are required.
- Optional `docs/agentic_research/<cycle_id>/...` notes for protocol context.
- `executor_manifest.json` written via the CLI helper.

## Manifest Shape

```json
{
  "cycle_id": "20260411_120451",
  "generated_at": "2026-04-11T12:04:51Z",
  "status": "completed",
  "mode": "agent_native_executor",
  "source": "agent_native_exec",
  "selected_micro_step": {"title": "..."},
  "summary": "What changed and why this is the next smallest useful step.",
  "limitations": ["What this step still does not prove."],
  "next_probe": "The next smallest follow-up probe.",
  "protocol_hygiene": {
    "repo_positioning": "clean | drift_detected | not_checked",
    "empirical_evidence_level": "none | structural_supported | synthetic_supported | empirical_supported",
    "reproducibility_dirty_diff_checked": true,
    "ci_coverage_note": "What confirm scripts or dirty-diff checks were added or left missing.",
    "venue_framing_status": "none | scouting_only | packaging_ready | premature",
    "naming_boundary_note": "Any misleading names fixed or explicitly deferred.",
    "contamination_check_strength": "none | weak_smoke_test | strong_artifact_scan"
  },
  "innovation_frontier": {
    "asset_bound_reading": "What the current repo assets genuinely support.",
    "asset_fixation_risk": "Where the selected step may be trapped by current incomplete assets.",
    "frontier_gap": "What missing external idea, benchmark axis, or mechanism this step keeps visible.",
    "step_mode": "repair | exploit | explore | bridge",
    "blank_slate_counterplan_ref": "Path or note for the counterplan considered before this step.",
    "next_exploration_probe": "Smallest safe idea-expanding probe after this step."
  },
  "generated_files": [
    {
      "destination": "source_repo",
      "repo_path": "scripts/run_pilot.py",
      "local_path": "/absolute/path/under/source_changes/scripts/run_pilot.py",
      "purpose": "Minimal executable experiment script"
    }
  ],
  "claim_rule": "No empirical claim is supported unless tied to generated runnable evidence."
}
```

## Rules

1. Keep one micro-step per cycle.
2. Read the target repo before writing.
3. Write into the `source_changes/` repo-root mirror, not directly into the source clone.
4. Prefer deterministic offline checks over secret-dependent API calls.
5. Do not require `OLLAMA_API_KEY`.
6. If a model call is optional, make it explicit and document the fallback.
7. If the selected micro-step touches reproducibility, run the relevant script and then check for a dirty git diff in tracked artifacts.
8. If the repo has no empirical model-output results, do not create manuscript packaging or venue-specific submission assets; create topic, benchmark, or protocol assets instead.
9. If a check is only a weak smoke test, label it weak in the manifest and docs.
10. Do not only repair or package inherited assets for multiple consecutive cycles; if the repo is asset-poor or toy-only, create a bounded exploration probe or design bridge that can expand the research hypothesis space.
11. Never mark an exploratory probe as empirical support until it produces real model-output or checkable experimental artifacts.
