# Capabilities — vmware-pilot

## MCP Tools (11)

| # | Tool | Risk | Category | Description |
|---|------|------|----------|-------------|
| 1 | `get_skill_catalog` | low | Discovery | List all available skills and tools for workflow design |
| 2 | `list_workflows` | low | Discovery | List built-in + custom templates and active workflows |
| 3 | `design_workflow` | low | Design | Natural language goal → draft workflow for review |
| 4 | `update_draft` | medium | Design | Edit draft workflow steps, name, or description |
| 5 | `confirm_draft` | medium | Design | Finalize draft → state changes to PENDING |
| 6 | `plan_workflow` | medium | Execute | Create workflow from built-in/custom template |
| 7 | `create_workflow` | medium | Execute | Create custom workflow from step list |
| 8 | `run_workflow` | medium | Execute | Execute workflow, pauses at approval gates |
| 9 | `approve` | high | Control | Human approval to continue past approval gate |
| 10 | `rollback` | high | Control | Reverse completed steps in reverse order |
| 11 | `get_workflow_status` | low | Control | Query workflow state, audit log, diff report |

---

## Built-in Templates (14)

| # | Template | Steps | Approval | Skills Used | Risk |
|---|----------|-------|----------|-------------|------|
| 1 | `clone_and_test` | 6 | Yes | aiops, monitor | Medium |
| 2 | `incident_response` | 4 | Yes | monitor, aiops | Medium |
| 3 | `plan_and_approve` | 3 | Yes | aiops | High |
| 4 | `compliance_scan` | 3 | No | monitor, aria | Low |
| 5 | `network_segment_setup` | 2-6 | Yes | nsx, nsx-security | Medium |
| 6 | `vks_cluster_deploy` | 4 | Yes | vks | Medium |
| 7 | `rolling_restart` | 2+3n | Yes | aiops, monitor | Medium |
| 8 | `capacity_expansion` | 5 | Yes | aria, aiops, monitor | Medium |
| 9 | `disaster_recovery` | 5 | Yes | aiops, monitor, nsx | High |
| 10 | `patch_deployment` | 1+3n | Yes | aiops, monitor | Medium |
| 11 | `storage_expansion` | 6 | Yes | storage | Medium |
| 12 | `baseline_capture` | 1-5 | No | monitor, nsx, storage | Low |
| 13 | `baseline_audit` | 2-5 | No | monitor, nsx, storage, aria | Low |
| 14 | `baseline_remediate` | 3+n | Yes | varies | High |

---

## Orchestrated Skills (8)

Pilot does not call VMware APIs directly. It delegates to these skills:

| Skill | Package | Tools | Domain |
|-------|---------|:-----:|--------|
| vmware-aiops | `vmware-aiops` | 34 | VM lifecycle, deployment, guest ops, clusters |
| vmware-monitor | `vmware-monitor` | 7 | Read-only inventory, alarms, events |
| vmware-nsx | `vmware-nsx-mgmt` | 32 | NSX segments, gateways, NAT, routing, IPAM |
| vmware-nsx-security | `vmware-nsx-security` | 20 | DFW policies/rules, security groups, traceflow |
| vmware-aria | `vmware-aria` | 27 | Aria Ops metrics, alerts, capacity, anomalies |
| vmware-vks | `vmware-vks` | 20 | Tanzu Supervisor, Namespaces, TKC clusters |
| vmware-storage | `vmware-storage` | 11 | Datastores, iSCSI, vSAN |
| vmware-avi | `vmware-avi` | 29 | AVI load balancing, pool members, AKO K8s ops |

**Total**: 185 tools across 8 skills (+ 11 pilot tools + 5 harness tools = 201 tools)

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
Pause execution for human review before destructive operations. Workflows can have multiple approval gates. Each gate requires an explicit `approve()` call to continue.

### Automatic Rollback
When a step fails, pilot offers to reverse all completed steps that have `rollback_tool` defined. Rollback executes in reverse order (last completed step first). Best-effort: if one rollback fails, remaining rollbacks still execute.

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
