# Meta-Team Execution

Skill2Team has two execution paths: `direct-skill` and `meta-team-first`.

`meta-team-first` is a hard Codex multi-agent mode. It is **not** a sequential role-play mode.

## Mandatory Codex rule

When the user selects:

```text
Execution path: meta-team-first
Target runtime: codex
```

Skill2Team must first generate or reuse the fixed six-agent `s2t-meta` Codex meta-team package and make a manifest-scoped registration attempt before processing the requested route/delivery.

Codex desktop may not hot-load custom agents written to `.codex/config.toml` during the same running thread. Treat file installation and active-session invocation as separate checks. Do not describe the meta-team pass as a fallback run. Do not continue package or design work under the `meta-team-first` label unless one of these is true:

1. registered `s2t-meta-*` custom agents were actually invoked and handoff evidence exists; or
2. the active Codex session used real independent subagents for the fixed S2T work orders and records `current_run_fanout_status=real_session_subagents`.

The second path is allowed only as current-session fan-out evidence. It does not mark the registered `s2t-meta-*` team runnable and it must keep registered smoke-test status pending.

If the environment cannot expose or verify either registered Codex custom-agent handoff or real current-session subagent fan-out, stop and report:

```text
meta-team-first blocked
reason: <specific reason>
recovery: <how to register/activate the fixed s2t-meta Codex team, or rerun with Execution path: direct-skill>
```

The only permitted alternatives are:

1. complete the real Codex meta-team activation and continue through `s2t-meta-entry`; or
2. complete real current-session subagent fan-out using fixed S2T role work orders, record `real_session_subagents`, and keep registered `s2t-meta-*` smoke tests pending; or
3. stop with a blocker report; or
4. rerun only if the user explicitly changes the execution path to `direct-skill` or explicitly selects a non-Codex API-service follow-up.

## Execution log fields

| Field | Meaning |
|---|---|
| `selected_route` | `source-to-team`, `brief-to-team`, or `guided-to-team` |
| `delivery` | `design` or `package` |
| `architecture_method` | framework-neutral agent relationship graph by default |
| `model_invocation_policy` | OpenAI Codex default; direct model API calls only as explicitly labeled API-run role simulation or API-service follow-up |
| `execution_path` | `direct-skill` or `meta-team-first` |
| `meta_team_first_done` | `true` when registered `s2t-meta-*` agents ran, or when real current-session subagents executed the fixed S2T work orders and that status is explicit |
| `registered_meta_team_smoke_status` | `passed`, `pending_hot_reload_or_new_thread`, or `not_attempted` |
| `current_run_fanout_status` | `direct-skill-not-requested`, `real_subagents`, `real_session_subagents`, or `blocked_no_real_codex_meta_team` |
| `execution_mode` | `direct_skill`, `fanout`, `blocked`, or `artifact_only` |
| `blocked_reason` | Required when `execution_path=meta-team-first` and `current_run_fanout_status` is neither `real_subagents` nor `real_session_subagents` |
| `synthesis_owner` | `s2t-meta-entry` when registered custom-agent activation succeeds; `Skill2Team entry with real session subagents` when using current-session fan-out; otherwise `Skill2Team direct skill` |
| `independent_meta_team_audit_status` | `passed_with_evidence`, `pending_independent_audit`, or `blocked` |
| `design_package_conformance_status` | `passed` or `blocked` |
| `reexecution_required` | `true` when conformance or audit blocks package handoff |
| `reexecute_from` | Earliest responsible meta role or phase to rerun |

## Fixed S2T meta-team

| Registered agent id | Internal role | Responsibility |
|---|---|---|
| `s2t-meta-entry` | S2T Lead | Intake, route/delivery/execution-path selection, state tracking, work orders, synthesis |
| `s2t-meta-source-mapper` | Source Mapper | Asset inventory and original workflow extraction |
| `s2t-meta-architecture-designer` | Architecture Designer | Agent Architecture Map, role boundaries, skill allocation, count rationale |
| `s2t-meta-workflow-orchestrator` | Workflow Orchestrator | Workflow Orchestration Map, control-flow, handoffs, gates, rerun/resume |
| `s2t-meta-runtime-adapter` | Runtime Adapter | Codex package artifacts, agent profiles, manifests, invocation contracts, prompt rewrite, design-output archive and Codex-only package-end templates |
| `s2t-meta-evaluation-reviewer` | Quality Reviewer | Independent design/package conformance, runtime-instruction materialization, package-quality, risk, count-justification, and acceptance-gate audit |

Every fixed meta-team agent has a profile entry in `data/meta_team_contract.json`. When Skill2Team generates its own meta-team package, it must emit the same `agent-profiles.json`, `profiles/*.agent-profile.json`, and framework-neutral agent relationship architecture metadata used for target teams.

## Required activation protocol for `meta-team-first` + Codex

1. Load `data/meta_team_contract.json` and verify the fixed six meta-agent profiles.
2. Generate or reuse the fixed `s2t-meta` Codex package containing `.codex/agents/s2t-meta-*.toml`, profile files, architecture/workflow metadata, and the registration manifest.
3. Register the package into the active Codex project using manifest-scoped registration. Do not delete unrelated custom agents.
4. Verify `.codex/config.toml` enables multi-agent/fan-out and contains entries for all six `s2t-meta-*` agents.
5. Run or verify smoke evidence for `s2t-meta-entry` invocation, handoff to each specialist, reviewer gate blocking, and state/artifact handoff.
6. If step 5 fails with an activation-cache or hot-load symptom such as `agent type is currently not available`, do not keep retrying the same invocation. Record `registered_meta_team_smoke_status=pending_hot_reload_or_new_thread`, then either use real current-session subagents for fixed S2T work orders or stop with `meta-team-first blocked`.
7. Only after registered smoke checks pass, process the user's route through `s2t-meta-entry`. If using current-session subagents, process the route through fixed-role work orders and record that registered runtime smoke tests remain pending.
8. Run the independent reviewer work order before package handoff. The reviewer must receive source extraction artifacts, architecture/workflow maps, conformance contracts, runtime instruction conformance, local-resource allocation, and package artifacts. The reviewer must not be the producer of the artifact under review.

If any step fails and real current-session subagents are not available, stop with a blocker report instead of simulating the meta-team.

## Independent audit and re-execution

Generated meta-team packages and meta-team-first target-team packages must include `meta-team-audit.contract.json` and `docs/meta-team-audit-contract.md`.

The audit must inspect `source_derived_runtime_constraints`, `design-package-conformance.contract.json`, and `runtime-instruction-conformance.json` before package handoff.

If the reviewer finds missing source constraints, dropped human waits, missing startup settings, missing stage-internal deliverables, invalid local-resource allocation, weak role boundaries, missing package artifacts, or absent runtime instruction materialization, set `reexecution_required=true` and `reexecute_from` to the earliest responsible role:

- `s2t-meta-source-mapper` for missing source workflow, local resources, startup settings, or human-intervention inventory;
- `s2t-meta-workflow-orchestrator` for missing workflow nodes, edges, gates, checkpoints, deliverables, or source-derived runtime constraints;
- `s2t-meta-architecture-designer` for missing ownership, role boundaries, or profile responsibilities;
- `s2t-meta-runtime-adapter` for missing package files, manifests, runtime instructions, or conformance contracts.

The reviewer blocks or approves. It must not silently repair the producer's artifacts and then approve its own changes.

## Route work orders after real activation

| Route | Required meta-team work orders |
|---|---|
| `source-to-team` | `s2t-meta-entry` integrates and asks for human-interaction execution mode; Source Mapper inventories source assets, required user input nodes, and workflow; Architecture Designer creates Agent Architecture Map and count rationale; Workflow Orchestrator creates Workflow Orchestration Map and control-flow/resume contract; Runtime Adapter handles package/profile artifacts, entry-agent startup welcome, design-output archive, and Codex-only package-end templates; Quality Reviewer checks gates and count justification. |
| `brief-to-team` | `s2t-meta-entry` clarifies goal; Source Mapper treats brief as source; Architecture Designer proposes compact team; Workflow Orchestrator sketches runtime flow; Quality Reviewer checks risk and count. |
| `guided-to-team` | `s2t-meta-entry` asks concise questions; Architecture Designer separates architecture concerns; Workflow Orchestrator separates workflow concerns; Quality Reviewer checks risk and count; Runtime Adapter joins when package output is likely. |

## Delivery outputs after real activation

| Delivery | Meta-team output |
|---|---|
| `design` | Architecture map, workflow map, contracts, role cards, skill allocation, migration plan, and design quality gate. |
| `package` | Codex artifacts, profile artifacts, manifests, invocation contract, design intermediate results, `design-output.zip`, entry-agent startup welcome page, conformance contracts, runtime instruction conformance, meta-team audit contract, generated-agent list, usage guide, package release gate, and Codex-only package-end prompt templates. |

Package-after work is not a Skill2Team delivery. Package-end prompts must focus on Codex registration, smoke tests, registered entry-agent use, and current-session Codex fan-out. Non-Codex continuations belong to design output and design-output.zip.
