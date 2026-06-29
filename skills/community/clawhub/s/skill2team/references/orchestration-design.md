# Orchestration Design

Skill2Team generates workflow orchestration as a first-class deliverable, but it must not mix workflow orchestration with agent architecture.

Workflow preservation is part of orchestration design: concrete source behavior must survive the migration into profile-based agents.

## Required separation

| Output | Purpose |
|---|---|
| Agent Architecture Map | Stable agent relationships, accountability, authority, shared state, context boundaries, skill ownership, and review relationships. |
| Workflow Orchestration Map | Runtime control-flow rules: sequence, branch, loop, gate, fan-out/fan-in, required user input node, human wait, checkpoint/resume, and terminal boundaries. |
| Control-Flow & Resume Contract | State, artifact lineage, invalidation, rerun, checkpoint, and recovery rules. |

## Agent Architecture Map fields

| Field | Meaning |
|---|---|
| Architecture pattern | coordinator/specialists, supervisor/worker, router/specialists, handoff chain, evidence ledger, reviewer-gated, team ReAct, or hybrid routing |
| Top-level agent count | Prefer 5-6; justify any other count |
| Roles and boundaries | responsibilities, non-responsibilities, authority, context visibility |
| Skill ownership | owned, shared, restricted, advisory, evidence-only, tool-only, or packaging-only skills |
| Gate ownership | who can block, approve, or request rerun |
| Shared state model | evidence ledger, artifact store, decision log, registry, or no shared state |
| Isolation model | same session, separate workspace, separate credentials, sandbox, or human separation |

## Workflow Orchestration Map fields

| Field | Meaning |
|---|---|
| Nodes | task, decision, gate, merge, required-user-input, human-wait, checkpoint, terminal |
| Edges | ordered, conditional, rerun, repair, resume, terminal |
| Source stage mappings | source stage id, target owner, migration action, preserved deliverables, handoff target |
| Stage-internal deliverables | named artifacts, candidate sets, prompt packages, registries, matrices, files, audit records, checkpoints, and closing prompts that must be produced before handoff |
| Required user input nodes | source-required settings, choices, approvals, no-auto-continue waits, and terminal/new-request decisions that must be asked or preserved |
| Human intervention points | user choice, approval, no-auto-continue wait, acceptance point, terminal boundary, default action, allowed user choices |
| Human intervention policy | preserve, convert to reviewer gate, auto-advance with audit, remove as redundant, plus recorded user overrides |
| Work request types | DataRequest, VerificationRequest, AnalysisRequest, CompositionRequest, RevisionRequest, AcceptanceRequest, ExecutionApprovalRequest, EvaluationRequest |
| Artifacts | CaseBrief, AssetInventory, WorkflowMap, ArchitectureMap, SkillCatalog, RoleCards, SkillMatrix, EvidenceLedger, DecisionLog, EvaluationReport |
| Handoff rules | required input, expected output, owner, next step, blocked condition |
| Gate rules | evidence gate, analysis gate, composition gate, execution approval gate, acceptance gate |
| Rerun triggers | new data, corrected fact, source conflict, user change, reviewer rejection, cost/latency issue |
| Stop conditions | target metrics met, user stops, budget reached, risks accepted, no meaningful improvement |
| Platform constraints | actual support for subagents, workspaces, tools, sandbox, memory, and registration |

## Blueprint examples

### Compact 5-agent design

```text
User → Entry Coordinator / Orchestrator
        ↓
Source Mapper → Architecture Designer → Workflow Orchestrator / Producer
        ↓
Independent Acceptance Reviewer → Delivery
```

### Governed 6-agent evidence-first design

```text
User → Entry Coordinator / Orchestrator
        ↓
Source/Data Mapper → Evidence Verifier → Evidence Ledger
        ↓
Domain Producer → Workflow Orchestrator / Composer
        ↓
Independent Acceptance Reviewer → Delivery
```

## Do-not-drift rule

The workflow orchestration must explain how each major original workflow stage maps to owners and handoffs. If it cannot explain the mapping, treat the design as speculative.

## No-summary-only rule

`source_workflow.summary` is not enough for a generated target team. For nontrivial source workflows, the Workflow Orchestration Map must include concrete `workflow_nodes`, `workflow_edges`, `stage_mappings`, `stage_internal_deliverables`, `user_input_nodes`, `human_intervention_points`, `gate_points`, and `checkpoint_resume_points`.

A human-wait edge does not replace the stage's own production duties. If a source stage must generate internal artifacts before asking the user to continue, the target workflow must model both the production node and the human-wait or selection edge.
