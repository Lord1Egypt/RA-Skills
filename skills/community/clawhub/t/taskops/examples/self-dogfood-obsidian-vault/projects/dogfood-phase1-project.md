---
graphTaskEntityType: "project"
graphTaskId: "dogfood-phase1-project"
status: "done"
---

# Dogfood TaskOps on its own repo

- projectId: `dogfood-phase1-project`
- status: `done`
- goal: Prove the Phase 1 TaskOps contract is usable on a small real workflow
- description: A richer self-dogfood run that exercises repeated phases, step edges, direct statuses, and expected-vs-actual records

## Steps
- [[steps/step-self-dogfood|step-self-dogfood]] [implementation] status=`done`
- [[steps/step-followups|step-followups]] [review] status=`done`

## Step edges
- [[steps/step-self-dogfood|step-self-dogfood]] -> [[steps/step-followups|step-followups]]
