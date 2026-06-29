# Sample Generated Plan

Execution path: `direct-skill`; current-run fan-out status: `direct-skill-not-requested`.

The recommended design uses six top-level agents: Entry Coordinator, Source Mapper, Architecture Designer, Workflow Orchestrator / Producer, Independent Acceptance Reviewer, and Runtime Adapter.

## Agent Architecture Map

Coordinator + Specialists pattern. The architecture map defines accountability, routing, shared state, review authority, skill ownership, and runtime packaging ownership.

## Workflow Orchestration Map

Intake → source mapping → architecture design → workflow orchestration → independent review → package/register when requested. Branches, gates, reruns, human waits, checkpoints, and terminal boundaries are recorded separately from the architecture topology.

If the user explicitly selects `meta-team-first` with Target runtime codex, Skill2Team must run the fixed six-agent S2T meta-team through real registered Codex agents before producing the plan; otherwise it must stop with a blocker reason.
