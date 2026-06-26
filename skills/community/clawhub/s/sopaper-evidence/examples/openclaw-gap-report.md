# OpenClaw Experiment Gap Report Example

## Project

- Project: OpenClaw
- Paper type: system paper
- Scope date: 2026-03-11

## Current claim set

- OpenClaw addresses manipulation tasks with multiple system components
- OpenClaw can be positioned against recent robotics and embodied systems papers
- OpenClaw improves long-horizon manipulation performance over strong baselines

## Gap triage

| Gap ID | Severity | Category | Blocked claims | Why it matters | What resolves it | Owner | Next step |
| --- | --- | --- | --- | --- | --- | --- | --- |
| G01 | blocker | result provenance | quantitative improvement claims | There is no verified internal result table tied to named runs. | A reproducible table with run identifiers and metric definitions. | project team | Export the current best result table and attach run provenance. |
| G02 | blocker | baseline quality | outperforms baseline claims | The direct baseline set is not yet confirmed as fair under the same task and metric. | A validated direct-baseline matrix with scope notes. | paper lead | Review direct baselines against benchmark-fit and metric-fit rules. |
| G03 | major | ablation coverage | modular contribution claims | The system appears modular, but component-level evidence is still partial. | A minimal ablation set over perception, planning, and control components. | experiment owner | Define one must-run ablation per major subsystem. |
| G04 | major | real-world validation | generalization claims | It is not yet clear whether current evidence is simulation-only. | An explicit real-world section or a clear simulation-only limitation. | paper lead | Decide final positioning and draft limitations accordingly. |

## Benchmark-fit notes

- Benchmark: manipulation / long-horizon benchmark set
- Fit status: partial
- Risks: task definition and success criteria may not match exactly

## Baseline-set notes

- Direct baselines covered: partial
- Adjacent methods reviewed: yes
- Missing expected baselines: likely at least one stronger direct comparison

## Ablation notes

- Covered: partial architecture-level reasoning
- Missing: subsystem-specific ablations tied to measurable outcomes
- Nice to have: failure-mode and robustness analysis

## Writing impact

- Claims safe to draft now: scope, task framing, related work boundaries, evidence workflow
- Claims that must be narrowed: contribution novelty, system-level improvement framing
- Claims that must be removed until evidence improves: hard quantitative superiority claims
