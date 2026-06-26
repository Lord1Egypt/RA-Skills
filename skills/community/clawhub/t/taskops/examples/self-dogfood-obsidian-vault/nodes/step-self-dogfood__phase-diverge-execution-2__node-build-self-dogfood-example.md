---
graphTaskEntityType: "node"
graphTaskId: "node-build-self-dogfood-example"
projectId: "dogfood-phase1-project"
stepId: "step-self-dogfood"
phaseId: "phase-diverge-execution-2"
nodeType: "work"
status: "done"
---

# Node node-build-self-dogfood-example

- project: [[projects/dogfood-phase1-project|Dogfood TaskOps on its own repo]]
- step: [[steps/step-self-dogfood|step-self-dogfood]]
- phase: [[phases/step-self-dogfood__phase-diverge-execution-2|phase-diverge-execution-2]]
- nodeType: `work`
- status: `done`
- title: Build the self-dogfood example
- description: Use the CLI to create a richer example that exercises repeated phases, step edges, and direct status updates

## Results
### Result `result-6b62dde9de`
- status: `done`
- at: `2026-04-24T02:43:12+00:00`
- expected: Exercise repeated phases, step edges, statuses, and result records in one real example
- actual: Built a richer self-dogfood run that uses repeated phases, a project-level step edge, explicit node edges, and direct status updates
- artifacts: examples/self-dogfood-project/graph.json, examples/self-dogfood-project/summary.md
