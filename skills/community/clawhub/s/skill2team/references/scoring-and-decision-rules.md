# Scoring and Decision Rules

## Signals

- High risk: serious consequence if wrong.
- High data dependency: facts, numbers, sources, or source conflicts are central.
- High iteration: missing information and repeated revisions are common.
- High specialization: multiple professional perspectives are needed.
- High governance: independent review, blocking acceptance, auditability, credentials, or side-effect control is required.
- High architecture/workflow separation need: the system has both durable role relationships and nontrivial runtime control flow.

## Agent count recommendations

Skill2Team defaults to **5-6 top-level agents** for nontrivial teams.

| Situation | Suggested top-level agents | Required rationale |
|---|---|---|
| Simple, low-risk, low-data, low-iteration work | 2-4 | Explain which roles are safely consolidated and why no independent gate is lost. |
| Nontrivial or normal professional workflow | 5-6 | Normal rationale: accountable roles, gates, and skill ownership are clear. |
| High data/risk/iteration, multiple domains, or hard isolation | 7-8 | Strong rationale: name the exact requirement, risk if consolidated, and consolidation check. |
| Very broad or regulated separation | >8 | User must explicitly need hard isolation or broad domain separation; include a consolidation plan. |

## Must-separate triggers

- Data critical or sources conflict → Data Collector separate from Evidence Verifier, or one combined Source/Evidence role plus a separate Acceptance Reviewer if the team must stay within 5-6.
- Delivery risk high → Producer/Executor separate from Independent Acceptance Reviewer.
- Tool side effects high → Executor separate from Execution Approver.
- Runtime credentials or workspace isolation required → separate runtime agents only where isolation is material.
- Complex flow with shared state, reruns, or resume → Orchestrator/State owner must be explicit.

## Architecture/workflow rule

- Agent Architecture Map chooses role topology and accountability.
- Workflow Orchestration Map chooses runtime nodes, edges, branches, loops, gates, and waits.
- Control-Flow & Resume Contract chooses artifact state, invalidation, rerun, checkpoint, and recovery policy.

## Platform rule

Runtime target should not change logical accountability, but it changes artifacts, invocation rules, registration state, and isolation guarantees.
