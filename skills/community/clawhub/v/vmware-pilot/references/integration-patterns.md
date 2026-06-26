# Cross-Skill Integration Patterns

vmware-pilot orchestrates 7 VMware skills (156 tools) into coherent workflows.
This reference documents the most common integration patterns and when to use
Pilot vs. calling a skill directly.

---

## The Dispatch Contract

Pilot is a **Dispatcher**, not an **Executor**. This is a deliberate v2-style architecture (per the Enterprise Harness Engineering framework — see `docs/architecture-audit-2026-04-30.md`).

The contract:

1. **Pilot generates a plan** via `plan_workflow` or `design_workflow`. The plan is a sequence of `(skill, tool, params)` tuples plus approval gates and rollback metadata. State is persisted to SQLite.
2. **Pilot tracks state** via `run_workflow`, `approve`, `rollback`. Each call returns immediately on the next checkpoint — running, awaiting approval, completed, or failed.
3. **The calling AI agent dispatches each step**. After `run_workflow` returns a step description, the agent invokes the corresponding MCP tool on the target skill (e.g., `vmware-aiops::vm_clone`), captures the result, and reports back to pilot via the next state transition.

In other words: pilot is the brain, the AI agent is the hands. Pilot never reaches across the wire to call other skills' tools itself — its `dispatch` function defaults to a no-op.

### Why this matters

- **Context isolation**: each step runs in the agent's main loop, not inside pilot. Pilot's context stays small (~100 lines/turn).
- **No persistent agents**: there is no long-running pilot process that holds state in memory. State is always on disk.
- **Approval gates as state, not blocking calls**: when a workflow hits `require_approval`, pilot persists the state and returns. Resumption is a new MCP call (`approve`), not an unblocking signal to a paused thread.
- **Rollback is an explicit operation**: it doesn't happen automatically on agent crash or context loss. The user (or agent) must call `rollback` deliberately.

### What this means for agents using pilot

| Agent action | Correct pilot interaction |
|---|---|
| Start a multi-step task | Call `plan_workflow`; read returned plan; show to user |
| Execute the plan | Call `run_workflow`; for each pending step in the response, invoke the named skill+tool yourself; report progress to the user |
| Hit an approval gate | Tell the user; wait for explicit approval; call `approve` |
| Encounter a failure | Surface the error; ask the user whether to `rollback` |
| Need to know workflow state mid-execution | Call `get_workflow_status` (idempotent, safe) |

### What this means for skill authors

If you add a new template to pilot, your template's steps must reference (`skill`, `tool`) pairs that already exist on companion skills. Pilot does no validation of tool existence at plan time — that's the agent's job at dispatch time. To help agents catch typos early, consider adding a `--validate` flag to template authoring tools.

---

## Pattern 1: Monitor -> Diagnose -> Fix

Detect a problem, gather context, then remediate with approval.

```
monitor.get_alarms              -> Find active alarms
monitor.get_events              -> Gather diagnostic context (last 1h, critical)
aria.list_anomalies             -> Check for correlated anomalies
    [APPROVAL GATE]             -> Human reviews diagnosis
aiops.acknowledge_vcenter_alarm -> Acknowledge/clear the alarm
monitor.get_alarms              -> Verify alarm is resolved
```

**Built-in template**: `incident_response`

**When to use**: An alert fires and you want structured triage before taking action.
The approval gate ensures no one auto-acknowledges a real issue.

**Variations**:
- Add `aria.list_rightsizing_recommendations` if the alarm is resource-related
- Add `aiops.vm_power_off` / `vm_power_on` if restart is the remediation
- Add `nsx-security.run_traceflow` if the alarm is network-related

---

## Pattern 2: Check -> Change -> Verify

Validate capacity/health, make a change, confirm no regressions.

```
aria.get_remaining_capacity             -> Confirm capacity exists
aria.list_rightsizing_recommendations   -> Validate change is reasonable
    [APPROVAL GATE]                     -> Human confirms the plan
aiops.vm_create_plan                    -> Create batch operation plan
aiops.vm_apply_plan                     -> Execute the plan
monitor.get_alarms                      -> Verify no new alarms
```

**Built-in templates**: `capacity_expansion`, `plan_and_approve`

**When to use**: Any change to production VMs (resize, reconfigure, migrate).
The pre-check steps prevent expanding a VM when the cluster is already at capacity.

**Variations**:
- Replace `vm_create_plan` with direct `vm_power_on`/`vm_power_off` for simpler ops
- Add `storage.vsan_capacity` if the change involves disk expansion
- Chain with Pattern 4 (baseline) to detect drift after the change

---

## Pattern 3: Build -> Secure -> Deploy

Provision infrastructure, apply security policies, then deploy workloads.

```
nsx.create_tier1_gateway        -> Create network gateway
nsx.create_segment              -> Create network segment
nsx-security.create_group       -> Create security group for the segment
nsx-security.create_dfw_policy  -> Create firewall policy
nsx-security.create_dfw_rule    -> Add allow/deny rules
    [APPROVAL GATE]             -> Human reviews network + security setup
aiops.batch_clone_vms           -> Deploy VMs into the new segment
monitor.get_alarms              -> Verify deployment health
```

**Built-in template**: `network_segment_setup` (networking portion)

**When to use**: Setting up a new application environment from scratch.
This pattern ensures networking and security are in place before any VMs are deployed.

**Variations**:
- Add `vks.create_namespace` + `vks.create_tkc_cluster` instead of `batch_clone_vms` for Kubernetes workloads
- Add `nsx.create_nat_rule` for outbound SNAT
- Add `nsx-security.run_traceflow` as a post-deploy verification step

---

## Pattern 4: Capture -> Audit -> Remediate

Take a snapshot of current state, compare later, fix any drift.

```
Phase 1 - Capture (run once, save as baseline):
    monitor.list_virtual_machines   -> VM inventory + configs
    monitor.list_esxi_hosts         -> Host inventory
    nsx.list_segments               -> Network segments
    storage.list_all_datastores     -> Storage state
    monitor.get_alarms              -> Alarm state
    [Save to ~/.vmware/baselines/]

Phase 2 - Audit (run periodically):
    monitor.list_virtual_machines   -> Current VM state
    monitor.list_esxi_hosts         -> Current host state
    nsx.list_segments               -> Current network state
    storage.list_all_datastores     -> Current storage state
    aria.list_anomalies             -> Any new anomalies
    [Compare against saved baseline -> drift report]

Phase 3 - Remediate (if drift detected):
    monitor.get_alarms              -> Pre-check
        [APPROVAL GATE]             -> Human reviews drift items
    (skill).tool per drift item     -> Fix each drift
    monitor.get_alarms              -> Post-verify
```

**Built-in templates**: `baseline_capture`, `baseline_audit`, `baseline_remediate`

**When to use**: Change management and compliance. Capture a baseline before
maintenance windows, audit after changes, remediate any unintended drift.

**Variations**:
- Add `aria.get_capacity_overview` to the capture for capacity baselines
- Schedule `baseline_audit` as a daily or weekly automated check
- Filter audit to specific resource types (VMs only, network only, etc.)

---

## Pattern 5: Clone -> Test -> Approve -> Commit

Safe change deployment using a staging clone.

```
aiops.deploy_linked_clone       -> Clone production VM to staging
aiops.vm_reconfigure            -> Apply changes to staging clone
monitor.get_alarms              -> Monitor staging for issues
    [APPROVAL GATE]             -> Human verifies staging is healthy
aiops.vm_reconfigure            -> Apply same changes to production
aiops.vm_power_off              -> Cleanup staging clone
```

**Built-in template**: `clone_and_test`

**When to use**: High-risk configuration changes (memory resize, CPU change,
software upgrade) where you want to validate in staging first.

**Key benefit**: If staging shows problems, you reject at the approval gate
and production is never touched.

---

## Pattern 6: Rolling Operations

Apply changes to multiple VMs one at a time with health checks between each.

```
monitor.get_alarms              -> Pre-flight health check
    [APPROVAL GATE]             -> Human confirms VM list

For each VM:
    aiops.vm_power_off          -> Stop VM (graceful)
    aiops.vm_power_on           -> Start VM
    monitor.get_alarms          -> Verify health after restart
    [If alarms -> stop rolling, offer rollback]
```

**Built-in templates**: `rolling_restart`, `patch_deployment`

**When to use**: Any operation that must be applied to multiple VMs but cannot
be done simultaneously (database clusters, load-balanced web servers, etc.).

**Key benefit**: If one VM fails the health check after restart, the workflow
stops before touching remaining VMs. Rollback powers the failed VM back on.

---

## Pattern 7: Kubernetes Lifecycle

Provision a complete Tanzu Kubernetes environment.

```
vks.create_namespace            -> Create Supervisor Namespace with storage policy
    [APPROVAL GATE]             -> Human reviews namespace config
vks.create_tkc_cluster          -> Deploy TKC cluster
vks.get_tkc_cluster             -> Verify cluster is ready
vks.get_tkc_kubeconfig          -> Retrieve kubeconfig for access
```

**Built-in template**: `vks_cluster_deploy`

**When to use**: Developer onboarding, new project environments, test cluster
provisioning.

**Variations**:
- Add `vks.scale_tkc_cluster` for day-2 scaling operations
- Chain with Pattern 3 (Build -> Secure -> Deploy) for network-isolated clusters
- Add `nsx-security.create_group` + `create_dfw_rule` for cluster network policies

---

## Pattern 8: Storage Lifecycle

Add or expand storage on ESXi hosts.

```
storage.storage_iscsi_status    -> Check current iSCSI state
storage.storage_iscsi_enable    -> Enable adapter if needed
    [APPROVAL GATE]             -> Human confirms storage target
storage.storage_iscsi_add_target -> Add iSCSI target
storage.storage_rescan          -> Rescan HBAs
storage.list_all_datastores     -> Verify new datastores visible
```

**Built-in template**: `storage_expansion`

**When to use**: Adding SAN/NAS storage to hosts, expanding storage pools.

**Variations**:
- Add `storage.vsan_health` + `storage.vsan_capacity` for vSAN operations
- Chain with Pattern 2 for VM disk expansion after new storage is available

---

## When to Use Pilot vs. Direct Skill Call

| Scenario | Direct Skill | Use Pilot | Why |
|----------|:------------:|:---------:|-----|
| Power on a single VM | aiops | -- | Single operation, no approval needed |
| List active alarms | monitor | -- | Read-only query |
| Check VM details | monitor | -- | Read-only query |
| List network segments | nsx | -- | Read-only query |
| Check capacity | aria | -- | Read-only query |
| Get kubeconfig | vks | -- | Read-only query |
| Clone, test, approve, apply | -- | pilot | Multi-step with approval gate |
| Set up network + firewall + VMs | -- | pilot | Cross-skill orchestration |
| Incident diagnosis + remediation | -- | pilot | Needs approval before action |
| Rolling restart of 5 VMs | -- | pilot | Sequential with health checks |
| Deploy patches to cluster | -- | pilot | Rolling deployment with verification |
| Disaster recovery (snapshot revert) | -- | pilot | Destructive, needs approval |
| Add iSCSI storage + rescan | -- | pilot | Multi-step with verification |
| Baseline capture + audit | -- | pilot | Multi-skill data collection |
| Batch power off 10 VMs | either | pilot preferred | Approval gate adds safety |

### Rules of Thumb

1. **Single read-only query** -> Call the skill directly (monitor, aria, nsx, storage, vks)
2. **Single write operation on one resource** -> Call aiops directly (unless approval is required by policy)
3. **Multiple steps across skills** -> Use Pilot
4. **Destructive operation in production** -> Use Pilot (for the approval gate)
5. **Same operation on multiple resources** -> Use Pilot (for rolling execution + health checks)
6. **Need audit trail** -> Use Pilot (SQLite-persisted workflow log)

---

## Composing Patterns

Patterns can be chained sequentially:

```
1. baseline_capture (Pattern 4, Phase 1)    -> Save current state
2. network_segment_setup (Pattern 3)         -> Build new environment
3. clone_and_test (Pattern 5)                -> Test VM changes
4. baseline_audit (Pattern 4, Phase 2)       -> Verify no drift
```

This gives you a complete change management lifecycle:
- Capture state before changes
- Build infrastructure
- Test changes safely
- Audit for unintended side effects

---

## Error Handling

When a workflow step fails:

1. The step is marked `failed` with the error message
2. All remaining steps are marked `skipped`
3. The workflow state becomes `FAILED`
4. Pilot offers rollback for steps that have `rollback_tool` defined
5. Rollback executes in reverse order (last completed step first)
6. Steps without rollback are skipped during rollback

If rollback itself fails on one step, Pilot continues rolling back the remaining
steps (best-effort rollback) and reports which rollback steps succeeded or failed.
