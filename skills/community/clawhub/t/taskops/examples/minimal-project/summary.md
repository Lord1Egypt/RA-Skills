# Example TaskOps project

- projectId: `example-project`
- status: `pending`
- goal: Show a valid graph with a result record
- description: A minimal example project for the TaskOps skill
- steps: 1

## Steps
- `step-implementation` [implementation] status=`pending`
  - description: Implement simple state handling
  - phases: 2
    - phase `phase-diverge-1` [diverge] status=`pending`
      - description: Explore implementation options
      - nodes: 2
      - edges: 1
        - node `phase-diverge-1-root` [root] status=`pending` — Root
        - node `node-compare-state` [work] status=`done` — Compare state libraries
          - latestResult: `done` at 2026-04-23T16:52:53+00:00
          - expected: Choose a candidate state library
          - actual: Selected Zustand after comparing setup cost and complexity
          - notes: Good enough for the current scope
    - phase `phase-verify-1` [verify] status=`pending`
      - description: Verify the state management choice
      - nodes: 1
      - edges: 0
        - node `phase-verify-1-root` [root] status=`pending` — Root
  - phaseEdges:
    - `phase-diverge-1` -> `phase-verify-1`

## Step edges
- none
