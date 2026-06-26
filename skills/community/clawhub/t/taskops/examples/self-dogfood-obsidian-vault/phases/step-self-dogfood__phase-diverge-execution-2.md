---
graphTaskEntityType: "phase"
graphTaskId: "phase-diverge-execution-2"
projectId: "dogfood-phase1-project"
stepId: "step-self-dogfood"
phaseType: "diverge"
status: "done"
rootNodeId: "phase-diverge-execution-2-root"
---

# Phase phase-diverge-execution-2

- project: [[projects/dogfood-phase1-project|Dogfood TaskOps on its own repo]]
- step: [[steps/step-self-dogfood|step-self-dogfood]]
- phaseType: `diverge`
- status: `done`
- description: Build a richer self-dogfood example run
- rootNode: [[nodes/step-self-dogfood__phase-diverge-execution-2__phase-diverge-execution-2-root|phase-diverge-execution-2-root]]

## Nodes
- [[nodes/step-self-dogfood__phase-diverge-execution-2__phase-diverge-execution-2-root|phase-diverge-execution-2-root]] [root] status=`done` — Root
- [[nodes/step-self-dogfood__phase-diverge-execution-2__node-build-self-dogfood-example|node-build-self-dogfood-example]] [work] status=`done` — Build the self-dogfood example

## Node edges
- [[nodes/step-self-dogfood__phase-diverge-execution-2__phase-diverge-execution-2-root|phase-diverge-execution-2-root]] -[flow]-> [[nodes/step-self-dogfood__phase-diverge-execution-2__node-build-self-dogfood-example|node-build-self-dogfood-example]]
