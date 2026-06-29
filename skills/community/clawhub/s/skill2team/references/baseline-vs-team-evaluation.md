# Baseline-vs-Team Evaluation

A team architecture is not automatically better than a strong original skill. Skill2Team should compare them before recommending replacement.

## Process

1. Record execution path. Default to `direct-skill`; run meta-team execution preflight only when `meta-team-first` is selected. If Codex meta-team activation/fan-out is unavailable, state `meta-team-first blocked`, provide the reason and recovery, and stop instead of evaluating under the meta-team-first label.
2. Build representative tasks.
3. Run or reconstruct the original skill/workflow baseline.
4. Run or simulate the candidate team with the recorded execution path and fan-out status when applicable.
5. Score both on correctness, completeness, evidence quality, risk control, decision usefulness, clarity, traceability, maintainability, reuse, workflow alignment, platform fit, latency, cost, and user satisfaction.
6. Diagnose regressions.
7. Revise, hybridize, or stop.

## Common regressions

| Regression | Likely cause | Fix |
|---|---|---|
| Team is slower with no quality gain | too many agents or gates | merge roles or add fast path |
| Context is lost | weak handoff | improve artifact contracts |
| Team drifts from original skill | workflow not extracted | rebuild workflow migration map |
| Platform export does not run | wrong runtime assumption | regenerate target adapter |
| Original writing style is better | composer lost useful baseline behavior | preserve original as composer skill |

## Replacement rule

Use full replacement only if the team wins on priority metrics or ties while clearly improving risk, traceability, maintainability, or reuse. Otherwise keep baseline, run team in shadow mode, or use hybrid routing.
