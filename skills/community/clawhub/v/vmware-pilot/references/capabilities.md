# Capabilities — vmware-pilot

## MCP Tools (13 — 4 read, 9 write)

| # | Tool | Risk | Category | Description |
|---|------|------|----------|-------------|
| 1 | `get_skill_catalog` | low | Discovery | List all available skills and tools for workflow design |
| 2 | `list_workflows` | low | Discovery | List built-in + custom templates and active workflows |
| 3 | `design_workflow` | low | Design | Natural language goal → draft workflow for review |
| 4 | `update_draft` | medium | Design | Edit draft workflow steps, name, or description |
| 5 | `confirm_draft` | medium | Design | Finalize draft → state changes to PENDING |
| 6 | `create_workflow_from_template` | medium | Execute | Create workflow from built-in/custom template |
| 7 | `create_workflow` | medium | Execute | Create custom workflow from step list (refused if a destructive step has no approval gate before it) |
| 8 | `run_workflow` | medium | Execute | Execute workflow, pauses at approval gates |
| 9 | `approve` | high | Control | Human approval to continue past approval gate |
| 10 | `rollback` | high | Control | Explicit, best-effort undo of steps pilot recorded as succeeded, in reverse order — never automatic. Previews (`blast_radius`) unless `confirm=True` |
| 11 | `get_workflow_status` | low | Control | Query workflow state, audit log, diff report |
| 12 | `review_workflow` | low | Discovery | Sanity-check a planned workflow before anyone runs it |
| 13 | `cancel_workflow` | high | Control | Cancel a workflow — moves it to the terminal CANCELLED state. Previews (`blast_radius`) unless `confirm=True` |

---

## Built-in Templates (15)

| # | Template | Steps | Approval | Skills Used | Risk |
|---|----------|-------|----------|-------------|------|
| 1 | `clone_and_test` | 7-8 | Yes | aiops, monitor | Medium |
| 2 | `incident_response` | 4 | Yes | monitor, aiops | Medium |
| 3 | `plan_and_approve` | 3 | Yes | aiops | High |
| 4 | `compliance_scan` | 1-3 | No | monitor, aria | Low |
| 5 | `network_segment_setup` | 3-6 | Yes | nsx, nsx-security | Medium |
| 6 | `vks_cluster_deploy` | 5 | Yes | vks | Medium |
| 7 | `rolling_restart` | 2+3n | Yes | aiops, monitor | Medium |
| 8 | `capacity_expansion` | 5 | Yes | aria, aiops, monitor | Medium |
| 9 | `disaster_recovery` | 5 | Yes | aiops, monitor, nsx | High |
| 10 | `patch_deployment` | 1+3n | Yes | aiops, monitor | Medium |
| 11 | `storage_expansion` | 6 | Yes | storage | Medium |
| 12 | `baseline_capture` | 1-5 | No | monitor, nsx, storage | Low |
| 13 | `baseline_audit` | 1-5 | No | monitor, nsx, storage, aria | Low |
| 14 | `baseline_remediate` | 3+n | Yes | varies | High |
| 15 | `investigate_alert` | 4 (8 with `deep_dive`) | Checkpoint | monitor, aria | Low |

---

## Orchestrated Skills (13)

Pilot does not call VMware APIs directly. It delegates to these skills. Two different
numbers matter here, and they are not the same thing:

- **Skill tools** — everything that skill exposes over MCP, all callable by the agent
  when it dispatches a step.
- **In design catalog** — the hand-picked subset `get_skill_catalog` surfaces to the AI
  while it drafts a workflow. It is a curated starting point, not a whitelist: a step may
  name any skill, including ones absent from the catalog.

| Skill | Package | Skill tools | In design catalog | Domain |
|-------|---------|:-----------:|:-----------------:|--------|
| vmware-aiops | `vmware-aiops` | 61 | 19 | VM lifecycle, deployment, guest ops, clusters |
| vmware-monitor | `vmware-monitor` | 33 | 6 | Read-only inventory, alarms, events |
| vmware-nsx | `vmware-nsx-mgmt` | 33 | 8 | NSX segments, gateways, NAT, routing, IPAM |
| vmware-nsx-security | `vmware-nsx-security` | 22 | 7 | DFW policies/rules, security groups, traceflow |
| vmware-aria | `vmware-aria` | 46 | 7 | Aria Ops metrics, alerts, capacity, anomalies |
| vmware-vks | `vmware-vks` | 25 | 8 | Tanzu Supervisor, Namespaces, TKC clusters |
| vmware-storage | `vmware-storage` | 16 | 5 | Datastores, per-VM usage, iSCSI, vSAN, FC multipath |
| vmware-avi | `vmware-avi` | 28 | 13 | AVI load balancing, pool members, AKO K8s ops |
| vmware-debug | `vmware-debug` | 14 | 5 | Incident correlation, evidence-graded cases |
| vmware-harden | `vmware-harden` | 8 | 5 | Compliance baselines, violations, drift |
| vmware-log-insight | `vmware-log-insight` | 7 | 4 | Log search, aggregation, alerts |
| vmware-privateai | `vmware-privateai` | 20 | 5 | GPU hosts, vGPU profiles, utilisation |
| vmware-vdi | `vmware-vdi` | 27 | 9 | Horizon pools, sessions, machines, images |

**Totals**: 340 tools across the 13 companion skills; the design catalog covers 101 of them
across all 13. Pilot adds 13 orchestration tools of its own. The counts are checked against
the companion snapshot by `tests/eval/regression/test_catalog_covers_the_family.py`.

---

## Workflow States

```
DRAFT -> PENDING -> RUNNING -> AWAITING_APPROVAL -> RUNNING -> COMPLETED
                        |                                        |
                        +-> FAILED --(rollback)--> ROLLING_BACK  |
                        |                                        |
                        +-> BLOCKED_BY_POLICY                    |
                        |                                        |
                        +-> MONITORING ---> COMMITTING ----------+
```

| State | Description |
|-------|-------------|
| `draft` | AI is designing steps (editable via update_draft) |
| `pending` | Finalized, ready to execute via run_workflow |
| `running` | Currently executing steps sequentially |
| `awaiting_approval` | Paused at an approval gate |
| `monitoring` | Watching for anomalies during test phase |
| `committing` | Applying tested changes to production |
| `rolling_back` | Undoing completed steps in reverse order |
| `completed` | All steps finished successfully |
| `failed` | A step failed (rollback may be available) |
| `blocked_by_policy` | Blocked by vmware-policy rule |

---

## Key Features

### Approval Gates
Pause execution for human review before destructive operations. Workflows can have multiple approval gates. Each gate requires an explicit `approve()` call to continue. In a custom workflow (YAML, `create_workflow`, or AI-designed) every destructive or unclassifiable step, and every step whose params tell its tool to act whatever its risk tier — `confirm` / `confirmed` truthy in any spelling (`True`, `1`, `"yes"`), or a legacy `dry_run` passed falsy — must have a gate before it: otherwise pilot refuses to save, confirm, plan or run it, and `force=True` does not override that.

### Rollback (explicit, never automatic)
A failed step stops the workflow; nothing is reversed until someone calls `rollback`. It undoes, last first, only steps pilot recorded as `success` — on the MCP server (no dispatcher) that is none of the steps the agent performed, so the agent calls each step's `rollback_tool` itself. Best-effort: if one undo fails, the rest still run. Steps without a `rollback_tool` cannot be undone.

### Preview first: rollback and cancel_workflow
Both take `confirm: bool = False`. A bare call returns `{"action": "preview", "blast_radius": ...}` and changes nothing. `blast_radius` names the workflow (id, type, state), `state_after`, and — each as a count plus up to 16 steps — `would_roll_back` / `would_skip` (rollback entries carry each step's `rollback_tool` and `rollback_params`, secrets redacted), `left_in_place` (executed steps that stay applied: cancelling part-way leaves a half-applied change), `not_reversed_by_pilot` (rollback: steps the agent performed from `pending_dispatch` that have an undo to call), `not_reversible_outside_pilot` (rollback: handed-out steps with no undo — a clone, a production resize; read-only catalog tools left out), `handed_out_to_caller` (cancel: steps already in `pending_dispatch`, which cancel can neither stop nor undo), `unknown_effects` (steps interrupted mid-dispatch), plus `blockers` and `unmeasured`. `confirm=True` refuses when either list is non-empty: a state the transition is not allowed from, a step status Pilot does not recognise, a workflow record that cannot be read, or a step in `unknown_effects` (left `running`/`interrupted` by a Pilot process that stopped mid-dispatch). For the last, the refusal says what to check; after the user has checked in the target system whether each such step took effect, re-run with `acknowledge_unknown_effects=True` (default `False`). That acknowledgement covers only those steps — it lifts no blocker and no other unmeasured item.

### Companion tools that preview by default
Destructive companion tools take `confirm: bool = False` and return `action: preview` on a bare call. Built-in template steps (and their `rollback_params`) pass `confirm=True`, because in every built-in template they come after an `approve` gate (a test enforces it). `rollback_params` with `confirm: True` in any workflow, built-in or custom, run on a `rollback(confirm=True)` call without an approval step of their own: `rollback` is itself gated, and that `confirm=True` is the human decision taken after its preview listed every rollback step's tool and parameters; they no longer pass the deprecated `confirmed` / `dry_run`. A step or rollback whose result is a top-level `action: preview` is recorded `failed` ("step only previewed"), never `success`. `baseline_remediate` adds `confirm=True` to caller-supplied drift items for those tools and refuses items that already carry `confirm`, `confirmed` or `dry_run`.

### State Persistence
All workflow state is stored in SQLite at `~/.vmware/workflows.db` (WAL mode). Workflows survive MCP server restarts and can be resumed.

### Custom Templates
Drop YAML files in `~/.vmware/workflows/` for instant availability. Supports `{{variable}}` placeholders filled from params at runtime. Hot-reloaded without server restart.

### Interactive Design Mode
1. `design_workflow(goal)` creates a draft
2. `update_draft(id, steps)` edits the draft
3. `confirm_draft(id)` finalizes for execution
4. `run_workflow(id)` executes with approval gates

### Policy Integration
All operations audited via vmware-policy `@vmware_tool` decorator. Policy rules in `~/.vmware/rules.yaml` can deny operations based on maintenance windows, risk levels, or custom rules.
