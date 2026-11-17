# Workflow Design Guide

## Core Concept: Pilot Breaks Down Goals into Multi-Skill Steps

When a user describes a goal, Pilot automatically:

1. **Identifies which skills are needed** (aiops, monitor, nsx, nsx-security, aria, vks, storage)
2. **Determines the correct step sequence** (pre-check -> action -> verify)
3. **Inserts approval gates** before destructive operations
4. **Adds rollback mappings** for reversible steps
5. **Persists state** so workflows survive restarts (SQLite-backed)

---

## Example: "Expand database cluster capacity"

### Without Pilot (user must orchestrate manually)

The user must know which skill has the right tool, call them in order, and remember to verify:

```
User calls aria   -> get_remaining_capacity   (must know aria has this)
User calls aria   -> list_rightsizing_recommendations  (must remember to check)
User calls monitor -> get_alarms              (must remember to verify no active issues)
User calls aiops  -> create_vm_plan           (must know parameters)
User calls aiops  -> apply_vm_plan            (must remember to apply)
User calls monitor -> get_alarms              (must verify no new alarms)
```

If anything fails, the user must manually figure out rollback.

### With Pilot (user just states the goal)

```
User: "Expand db01 to 32GB RAM"

Pilot creates workflow:
  Step 0: aria.get_remaining_capacity     -> check if capacity exists
  Step 1: aria.list_rightsizing            -> validate against recommendations
  Step 2: [APPROVAL GATE]                 -> user reviews and confirms
  Step 3: aiops.create_vm_plan            -> create the change plan
  Step 4: monitor.get_alarms              -> verify health after change

User reviews steps, approves at gate, Pilot completes execution.
On failure at Step 3 the workflow stops as `failed`; nothing is undone until
someone calls `rollback` (explicit, best-effort — see Error Handling in
integration-patterns.md).
```

---

## Workflow Step Structure

Each step in a workflow has these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `index` | int | Yes | Step position (0-based) |
| `action` | str | Yes | Human-readable name (e.g. "check_health", "clone_vm") |
| `skill` | str | Yes | Which VMware skill to invoke |
| `tool` | str | Yes | The specific MCP tool within that skill |
| `params` | dict | Yes | Tool parameters (passed directly to MCP tool) |
| `rollback_tool` | str | No | Tool to call if we need to undo this step |
| `rollback_params` | dict | No | Parameters for the rollback tool |
| `status` | str | Auto | pending / running / success / failed / skipped / rolled_back |

### Special step: Approval Gate

```yaml
- action: require_approval
  skill: pilot
  tool: approve
  params:
    message: "Changes ready. Proceed with production deployment?"
```

When the executor reaches an approval gate, it pauses the workflow and waits for
the user to call `approve(workflow_id)`. This is the mechanism that makes Pilot
safe for destructive operations.

---

## Available Skills and Key Tools

The **Risk** column is pilot's skill catalog (`get_skill_catalog`), which is what
the approval-gate check reads: a `high` step, a step whose name says
delete/remove/destroy/shutdown/drop/rollback/force_power_off, or a step whose
tool is not in the catalog must have a `require_approval` step before it in a
custom workflow, or pilot refuses the workflow. `medium` writes need no gate.

### aiops (VM Lifecycle and Operations)

| Tool | Risk | Use For |
|------|------|---------|
| `power_on_vm` | medium | Start a VM |
| `power_off_vm` | high | Stop a VM (graceful or force) |
| `deploy_linked_clone` | medium | Clone a VM from snapshot |
| `create_vm_plan` | medium | Create a batch operation plan |
| `apply_vm_plan` | medium | Execute a planned batch |
| `rollback_vm_plan` | medium | Undo a batch operation |
| `run_vm_guest_command` | high | Run command inside guest OS — as the account you name; gate it |
| `run_vm_guest_command_with_output` | high | Run command and capture output |
| `upload_vm_guest_file` | high | Upload file to guest OS |
| `provision_vm_guest` | high | Bootstrap a new VM |
| `batch_clone_vms` | medium | Clone multiple VMs at once |
| `restore_vm_clean_slate` | high | Revert VM to snapshot |
| `acknowledge_vcenter_alarm` | medium | Acknowledge an alarm |
| `reset_vcenter_alarm` | high | Clear triggered alarms — every one with the named alarm's status and entity type |
| `create_cluster` | medium | Create a new cluster |
| `deploy_vm_from_ova` | medium | Deploy from OVA |
| `deploy_vm_from_template` | medium | Deploy from template |

### monitor (Read-Only Monitoring)

| Tool | Risk | Use For |
|------|------|---------|
| `list_virtual_machines` | low | Inventory all VMs |
| `list_esxi_hosts` | low | Inventory all hosts |
| `list_all_datastores` | low | Inventory all datastores |
| `list_all_clusters` | low | Inventory all clusters |
| `get_alarms` | low | Check active alarms |
| `get_events` | low | Check recent events |
| `get_vm_info` | low | Detailed VM information |

### nsx (Networking)

| Tool | Risk | Use For |
|------|------|---------|
| `list_segments` | low | List network segments |
| `create_segment` | medium | Create overlay/VLAN segment |
| `delete_segment` | high | Remove a segment |
| `create_tier1_gateway` | medium | Create Tier-1 gateway |
| `create_nat_rule` | medium | Add NAT rule |
| `list_nat_rules` | low | List NAT rules |

### nsx-security (Firewall and Microsegmentation)

| Tool | Risk | Use For |
|------|------|---------|
| `list_dfw_policies` | low | List DFW policies |
| `create_dfw_policy` | medium | Create firewall policy |
| `create_dfw_rule` | medium | Add firewall rule |
| `delete_dfw_rule` | high | Remove firewall rule |
| `create_group` | medium | Create security group |
| `run_traceflow` | medium | Trace packet path |

### aria (Metrics, Alerts, Capacity)

| Tool | Risk | Use For |
|------|------|---------|
| `list_alerts` | low | List active alerts |
| `acknowledge_alert` | medium | Acknowledge an alert |
| `get_capacity_overview` | low | Overall capacity summary |
| `get_remaining_capacity` | low | Time/resource remaining |
| `get_time_remaining` | low | Days until capacity exhaustion |
| `list_anomalies` | low | Detected anomalies |
| `list_rightsizing_recommendations` | low | VM rightsizing suggestions |
| `generate_report` | not in catalog | Generate capacity report (unclassified, so it needs a gate before it) |

### vks (Tanzu Kubernetes)

| Tool | Risk | Use For |
|------|------|---------|
| `create_namespace` | medium | Create Supervisor Namespace |
| `delete_namespace` | high | Delete namespace |
| `create_tkc_cluster` | medium | Deploy TKC cluster |
| `scale_tkc_cluster` | medium | Scale worker nodes |
| `delete_tkc_cluster` | high | Delete TKC cluster |
| `issue_tkc_kubeconfig` | high | Returns a live Supervisor credential — gate it, write it to a file, never print it |
| `issue_supervisor_kubeconfig` | high | Same: a live Supervisor bearer token — gate it, write it to a file, never print it |

### storage (Datastores, iSCSI, vSAN)

| Tool | Risk | Use For |
|------|------|---------|
| `list_all_datastores` | low | List datastores |
| `enable_iscsi` | medium | Enable iSCSI adapter |
| `add_iscsi_target` | medium | Add iSCSI target |
| `rescan_storage` | medium | Rescan storage adapters |
| `get_vsan_health` | low | vSAN health check |
| `get_vsan_capacity` | low | vSAN capacity info |

---

## Designing Custom Workflows

### Method 1: YAML Templates

Drop a `.yaml` file in `~/.vmware/workflows/` and it is immediately available.
Supports `{{variable}}` placeholders that are filled from params at runtime.

```yaml
# ~/.vmware/workflows/restart_db_cluster.yaml
name: restart_db_cluster
description: Rolling restart of database cluster with health checks
steps:
  - action: check_health
    skill: monitor
    tool: get_alarms
    params:
      target: "{{target}}"

  - action: require_approval       # required: power_off_vm below is high risk
    skill: pilot
    tool: approve
    params:
      message: "Cluster healthy. Stop replica {{replica_vm}}?"

  - action: stop_replica
    skill: aiops
    tool: power_off_vm
    params:
      vm_name: "{{replica_vm}}"
      force: false
    rollback_tool: power_on_vm
    rollback_params:
      vm_name: "{{replica_vm}}"

  - action: require_approval
    skill: pilot
    tool: approve
    params:
      message: "Replica {{replica_vm}} stopped. Restart primary {{primary_vm}}?"

  - action: restart_primary
    skill: aiops
    tool: power_off_vm
    params:
      vm_name: "{{primary_vm}}"
      force: false
    rollback_tool: power_on_vm
    rollback_params:
      vm_name: "{{primary_vm}}"

  - action: start_primary
    skill: aiops
    tool: power_on_vm
    params:
      vm_name: "{{primary_vm}}"

  - action: start_replica
    skill: aiops
    tool: power_on_vm
    params:
      vm_name: "{{replica_vm}}"

  - action: verify
    skill: monitor
    tool: get_alarms
    params:
      target: "{{target}}"
```

Invoke it:
```
create_workflow_from_template("restart_db_cluster", {
    target: "vcenter1",
    replica_vm: "db02",
    primary_vm: "db01"
})
```

### Method 2: AI-Designed (`design_workflow`)

Describe your goal in natural language. The AI creates a draft that you review and edit.

```
User: "I need to migrate app01 to a new network segment with firewall rules"

AI calls: design_workflow(goal="Migrate app01 to new network segment with firewall rules")
AI returns: Draft workflow with steps from nsx, nsx-security, aiops, monitor
User reviews: Adjusts steps, adds/removes approval gates
AI calls: confirm_draft(draft_id, save_as_template=True)
AI calls: run_workflow(workflow_id)
```

### Method 3: Direct Creation (`create_workflow`)

Provide steps directly as JSON when you already know exactly what you want:

```
create_workflow(
    name="quick_snapshot_revert",
    steps=[
        {action: "pre_check", skill: "monitor", tool: "get_alarms", params: {target: "prod"}},
        {action: "require_approval", skill: "pilot", tool: "approve",
         params: {message: "Revert web01 to baseline?"}},
        {action: "revert", skill: "aiops", tool: "restore_vm_clean_slate",
         params: {vm_name: "web01", snapshot_name: "baseline", target: "prod"}},
        {action: "verify", skill: "monitor", tool: "get_vm_info",
         params: {vm_name: "web01", target: "prod"}},
    ]
)
```

---

## Workflow States

A workflow moves through these states:

```
DRAFT -> PENDING -> RUNNING -> AWAITING_APPROVAL -> RUNNING -> COMPLETED
                         |                                        |
                         +-> FAILED --(rollback)--> ROLLING_BACK  |
                         |                                        |
                         +-> BLOCKED_BY_POLICY                    |
                         |                                        |
                         +-> MONITORING ---> COMMITTING ----------+
```

| State | Meaning |
|-------|---------|
| `draft` | AI is still designing steps (editable) |
| `pending` | Finalized, ready to execute |
| `running` | Currently executing steps |
| `awaiting_approval` | Paused at an approval gate |
| `monitoring` | Watching for anomalies during test phase |
| `committing` | Applying tested changes to production |
| `rolling_back` | Undoing completed steps in reverse |
| `completed` | All steps finished successfully |
| `failed` | A step failed; nothing is undone until someone calls `rollback` |
| `blocked_by_policy` | Blocked by a policy check |

---

## Best Practices

### Step Design

1. **Always include a pre-check step** -- Start with `monitor.get_alarms` or `aria.list_anomalies` to verify the environment is healthy before making changes.

2. **Always include a post-verification step** -- End with a health check to confirm changes did not introduce issues.

3. **Place approval gates before destructive operations** -- Any step that modifies production (power off, delete, reconfigure) should have an approval gate before it.

4. **Define rollback for reversible steps** -- If a step can be undone (power off -> power on, create segment -> delete segment), always specify `rollback_tool` and `rollback_params`.

5. **Keep workflows under 15 steps** -- Longer workflows are harder to review and more likely to fail mid-execution. Split into multiple workflows if needed.

### Parameter Design

6. **Use `{{variable}}` placeholders in YAML templates** -- Makes templates reusable across different VMs, targets, and environments.

7. **Always include `target` parameter** -- Multi-vCenter setups require explicit target routing. Even single-vCenter setups benefit from explicit naming.

8. **Use descriptive approval messages** -- The message shown at an approval gate is the user's primary decision-making context. Include what was done, what will happen next, and any risks.

### Workflow Organization

9. **Save successful workflows as templates** -- Use `confirm_draft(id, save_as_template=True)` to save AI-designed workflows for reuse.

10. **Name templates by intent, not by tool** -- `restart_db_cluster` is better than `power_off_then_on`. The name should describe the goal, not the implementation.

11. **Group related steps** -- Keep all steps for one resource together (e.g., all steps for VM "db01" before moving to "db02" in a rolling restart).

12. **Test with `compliance_scan` first** -- Before running destructive workflows, run a compliance scan to verify the environment baseline.

---

## Validation

Before executing a workflow, validate it with the included script. It runs
pilot's own approval-gate check, so run it with the Python vmware-pilot is
installed in:

```bash
"$(uv tool dir)/vmware-pilot/bin/python" scripts/validate_workflow.py ~/.vmware/workflows/my_workflow.yaml
```

This checks:
- Step structure is valid (action / skill / tool present, params a mapping)
- **Approval gates (error)**: every destructive or unclassifiable step has a
  `require_approval` step before it — the same check `create_workflow_from_template`,
  `create_workflow`, `confirm_draft` and `run_workflow` enforce
- Skills and tools not in the catalog (warning — the catalog is a curated subset)
