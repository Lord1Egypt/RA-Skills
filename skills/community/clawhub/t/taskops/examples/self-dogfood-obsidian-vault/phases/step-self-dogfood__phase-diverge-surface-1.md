---
graphTaskEntityType: "phase"
graphTaskId: "phase-diverge-surface-1"
projectId: "dogfood-phase1-project"
stepId: "step-self-dogfood"
phaseType: "diverge"
status: "done"
rootNodeId: "phase-diverge-surface-1-root"
---

# Phase phase-diverge-surface-1

- project: [[projects/dogfood-phase1-project|Dogfood TaskOps on its own repo]]
- step: [[steps/step-self-dogfood|step-self-dogfood]]
- phaseType: `diverge`
- status: `done`
- description: Read the frozen Phase 1 contract surfaces
- rootNode: [[nodes/step-self-dogfood__phase-diverge-surface-1__phase-diverge-surface-1-root|phase-diverge-surface-1-root]]

## Nodes
- [[nodes/step-self-dogfood__phase-diverge-surface-1__phase-diverge-surface-1-root|phase-diverge-surface-1-root]] [root] status=`done` — Root
- [[nodes/step-self-dogfood__phase-diverge-surface-1__node-read-phase1-spec|node-read-phase1-spec]] [work] status=`done` — Read the Phase 1 spec
- [[nodes/step-self-dogfood__phase-diverge-surface-1__node-read-cli-surface|node-read-cli-surface]] [work] status=`done` — Read the CLI reference

## Node edges
- [[nodes/step-self-dogfood__phase-diverge-surface-1__phase-diverge-surface-1-root|phase-diverge-surface-1-root]] -[flow]-> [[nodes/step-self-dogfood__phase-diverge-surface-1__node-read-phase1-spec|node-read-phase1-spec]]
- [[nodes/step-self-dogfood__phase-diverge-surface-1__node-read-phase1-spec|node-read-phase1-spec]] -[dependency]-> [[nodes/step-self-dogfood__phase-diverge-surface-1__node-read-cli-surface|node-read-cli-surface]]
