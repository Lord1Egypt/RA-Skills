---
graphTaskEntityType: "phase"
graphTaskId: "phase-verify-surface-1"
projectId: "dogfood-phase1-project"
stepId: "step-self-dogfood"
phaseType: "verify"
status: "done"
rootNodeId: "phase-verify-surface-1-root"
---

# Phase phase-verify-surface-1

- project: [[projects/dogfood-phase1-project|Dogfood TaskOps on its own repo]]
- step: [[steps/step-self-dogfood|step-self-dogfood]]
- phaseType: `verify`
- status: `done`
- description: Confirm the current contract is usable for live dogfooding
- rootNode: [[nodes/step-self-dogfood__phase-verify-surface-1__phase-verify-surface-1-root|phase-verify-surface-1-root]]

## Nodes
- [[nodes/step-self-dogfood__phase-verify-surface-1__phase-verify-surface-1-root|phase-verify-surface-1-root]] [root] status=`done` — Root
- [[nodes/step-self-dogfood__phase-verify-surface-1__node-verify-phase1-usable|node-verify-phase1-usable]] [work] status=`done` — Verify the Phase 1 surface is usable

## Node edges
- [[nodes/step-self-dogfood__phase-verify-surface-1__phase-verify-surface-1-root|phase-verify-surface-1-root]] -[flow]-> [[nodes/step-self-dogfood__phase-verify-surface-1__node-verify-phase1-usable|node-verify-phase1-usable]]
