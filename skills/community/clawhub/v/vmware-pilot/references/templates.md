# Built-in Templates Reference

vmware-pilot ships with 14 built-in workflow templates. Each template is a Python function
that generates a `Workflow` with pre-configured steps, approval gates, and rollback mappings.

---

## 1. clone_and_test

**Purpose**: Clone a VM, apply changes in staging, monitor, then await approval before applying to production. The safest way to test changes.

**Steps** (6):

| # | Action | Skill | Tool | Rollback |
|---|--------|-------|------|----------|
| 0 | Clone VM to staging | aiops | `deploy_linked_clone` | `vm_power_off` (staging) |
| 1 | Apply changes to staging | aiops | `vm_reconfigure` or `vm_guest_exec` | -- |
| 2 | Monitor staging health | monitor | `get_alarms` | -- |
| 3 | **APPROVAL GATE** | pilot | `approve` | -- |
| 4 | Apply changes to production | aiops | `vm_reconfigure` or `vm_guest_exec` | -- |
| 5 | Cleanup staging VM | aiops | `vm_power_off` | -- |

**Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `target_vm` | str | Yes | Production VM name to clone |
| `change_spec` | dict | Yes | Changes to apply (e.g. `{memory_mb: 32768, cpu: 4}`) |
| `monitor_minutes` | int | No | How long to monitor staging (default: 5) |
| `target` | str | No | vCenter target name |

**Example**:
```
plan_workflow("clone_and_test", {
    target_vm: "db01",
    change_spec: {memory_mb: 32768},
    target: "vcenter-prod"
})
```

---

## 2. incident_response

**Purpose**: Auto-diagnose and remediate an alert with human approval before taking action.

**Steps** (4):

| # | Action | Skill | Tool | Rollback |
|---|--------|-------|------|----------|
| 0 | Get alarm details | monitor | `get_alarms` | -- |
| 1 | Collect diagnostic events | monitor | `get_events` (critical, last 1h) | -- |
| 2 | **APPROVAL GATE** | pilot | `approve` | -- |
| 3 | Acknowledge alarm | aiops | `acknowledge_vcenter_alarm` | -- |

**Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `alert_entity` | str | Yes | Entity with the alert (VM/host name) |
| `alert_name` | str | Yes | Name of the alert/alarm |
| `target` | str | No | vCenter target name |

**Example**:
```
plan_workflow("incident_response", {
    alert_entity: "esxi-host-03",
    alert_name: "Host memory usage",
    target: "vcenter-prod"
})
```

---

## 3. plan_and_approve

**Purpose**: Wrap aiops batch operations with an approval gate. Bridge between aiops's single-skill batch operations and pilot's approval-gated workflows.

**Steps** (3):

| # | Action | Skill | Tool | Rollback |
|---|--------|-------|------|----------|
| 0 | Create batch plan | aiops | `vm_create_plan` | -- |
| 1 | **APPROVAL GATE** | pilot | `approve` | -- |
| 2 | Apply batch plan | aiops | `vm_apply_plan` | `vm_rollback_plan` |

**Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `operations` | list[dict] | Yes | List of operations for vm_create_plan |
| `target` | str | No | vCenter target name |
| `description` | str | No | Human-readable description |

**Supported operations**: `power_on`, `power_off`, `reset`, `clone`, `deploy_ova`, `deploy_template`, `linked_clone`, `create_snapshot`, `delete_snapshot`, `revert_snapshot`.

**Example**:
```
plan_workflow("plan_and_approve", {
    operations: [
        {action: "power_off", vm_name: "db01"},
        {action: "revert_snapshot", vm_name: "db01", snapshot_name: "baseline"},
        {action: "power_on", vm_name: "db01"}
    ],
    description: "Revert db01 to baseline"
})
```

---

## 4. compliance_scan

**Purpose**: Periodic read-only health scan across monitor and aria. No approval gate needed (all steps are non-destructive).

**Steps** (3, variable):

| # | Action | Skill | Tool | Rollback |
|---|--------|-------|------|----------|
| 0 | Check active alarms | monitor | `get_alarms` | -- |
| 1 | Check capacity remaining | aria | `get_capacity_overview` | -- |
| 2 | Check anomalies | aria | `list_anomalies` | -- |

**Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `target` | str | No | vCenter/Aria target name |
| `check_alarms` | bool | No | Include alarm check (default: True) |
| `check_capacity` | bool | No | Include capacity check (default: True) |

**Example**:
```
plan_workflow("compliance_scan", {target: "vcenter-prod"})
```

---

## 5. network_segment_setup

**Purpose**: Set up a complete application network: Tier-1 gateway + overlay segment + NAT + DFW firewall policy, with approval before finalization.

**Steps** (up to 6, depends on params):

| # | Action | Skill | Tool | Rollback |
|---|--------|-------|------|----------|
| 0 | Create Tier-1 gateway (if tier1_id) | nsx | `create_tier1_gateway` | `delete_tier1_gateway` |
| 1 | Create network segment | nsx | `create_segment` | `delete_segment` |
| 2 | Create NAT rule (if nat_source) | nsx | `create_nat_rule` | `delete_nat_rule` |
| 3 | Create DFW policy (if dfw_policy_id) | nsx-security | `create_dfw_policy` | `delete_dfw_policy` |
| 4 | **APPROVAL GATE** | pilot | `approve` | -- |
| 5 | Verify segments | nsx | `list_segments` | -- |

**Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `segment_id` | str | Yes | Segment identifier |
| `display_name` | str | Yes | Human-readable segment name |
| `subnet` | str | Yes | Subnet CIDR (e.g. "10.10.1.0/24") |
| `transport_zone_path` | str | Yes | NSX transport zone path |
| `tier1_id` | str | No | Tier-1 gateway ID (creates if provided) |
| `tier0_path` | str | No | Tier-0 gateway path for uplink |
| `nat_source` | str | No | NAT source network |
| `nat_translated` | str | No | NAT translated network |
| `dfw_policy_id` | str | No | DFW policy ID (creates if provided) |
| `target` | str | No | NSX target name |

**Example**:
```
plan_workflow("network_segment_setup", {
    segment_id: "app-frontend",
    display_name: "App Frontend Network",
    subnet: "10.10.1.0/24",
    transport_zone_path: "/infra/sites/default/enforcement-points/default/transport-zones/overlay-tz",
    tier1_id: "app-t1-gw",
    tier0_path: "/infra/tier-0s/t0-gateway",
    dfw_policy_id: "app-frontend-fw"
})
```

---

## 6. vks_cluster_deploy

**Purpose**: Deploy a complete VKS (vSphere with Tanzu) environment: create namespace, then deploy TKC cluster with approval gate.

**Steps** (4):

| # | Action | Skill | Tool | Rollback |
|---|--------|-------|------|----------|
| 0 | Create vSphere Namespace | vks | `create_namespace` | `delete_namespace` |
| 1 | **APPROVAL GATE** | pilot | `approve` | -- |
| 2 | Create TKC cluster | vks | `create_tkc_cluster` | `delete_tkc_cluster` |
| 3 | Verify cluster health | vks | `get_tkc_cluster` | -- |

**Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `namespace_name` | str | Yes | Namespace name |
| `cluster_id` | str | Yes | vSphere cluster ID for the namespace |
| `storage_policy` | str | Yes | Storage policy for the namespace |
| `tkc_name` | str | Yes | TKC cluster name |
| `k8s_version` | str | Yes | Kubernetes version (e.g. "v1.28.3") |
| `vm_class` | str | No | VM class for workers (default: "best-effort-medium") |
| `worker_count` | int | No | Number of workers (default: 3) |
| `target` | str | No | vCenter target name |

**Example**:
```
plan_workflow("vks_cluster_deploy", {
    namespace_name: "dev-team-a",
    cluster_id: "domain-c8",
    storage_policy: "vsan-default",
    tkc_name: "dev-cluster-01",
    k8s_version: "v1.28.3",
    worker_count: 3
})
```

---

## 7. rolling_restart

**Purpose**: Rolling restart of multiple VMs with health checks between each. Approval gate before starting.

**Steps** (2 + 3 per VM):

| # | Action | Skill | Tool | Rollback |
|---|--------|-------|------|----------|
| 0 | Pre-check health | monitor | `get_alarms` | -- |
| 1 | **APPROVAL GATE** | pilot | `approve` | -- |
| 2 | Power off VM_1 | aiops | `vm_power_off` | `vm_power_on` |
| 3 | Power on VM_1 | aiops | `vm_power_on` | -- |
| 4 | Health check VM_1 | monitor | `get_alarms` | -- |
| ... | (repeat for each VM) | | | |

**Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `vm_names` | list[str] | Yes | List of VM names to restart |
| `target` | str | No | vCenter target name |

**Example**:
```
plan_workflow("rolling_restart", {
    vm_names: ["web01", "web02", "web03"],
    target: "vcenter-prod"
})
```

---

## 8. capacity_expansion

**Purpose**: Expand VM resources (CPU/memory) with capacity checks and rightsizing validation before applying.

**Steps** (5):

| # | Action | Skill | Tool | Rollback |
|---|--------|-------|------|----------|
| 0 | Check remaining capacity | aria | `get_remaining_capacity` | -- |
| 1 | Check rightsizing recommendations | aria | `list_rightsizing_recommendations` | -- |
| 2 | **APPROVAL GATE** | pilot | `approve` | -- |
| 3 | Apply reconfiguration | aiops | `vm_create_plan` | -- |
| 4 | Verify health | monitor | `get_alarms` | -- |

**Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `vm_name` | str | Yes | VM to expand |
| `cpu` | int | No | New CPU count |
| `memory_mb` | int | No | New memory in MB |
| `target` | str | No | vCenter target name |

At least one of `cpu` or `memory_mb` must be provided.

**Example**:
```
plan_workflow("capacity_expansion", {
    vm_name: "db01",
    cpu: 8,
    memory_mb: 65536,
    target: "vcenter-prod"
})
```

---

## 9. disaster_recovery

**Purpose**: Revert a VM to a known-good snapshot and verify full stack health (VM, network, alarms). Approval gate first since this is destructive.

**Steps** (5):

| # | Action | Skill | Tool | Rollback |
|---|--------|-------|------|----------|
| 0 | **APPROVAL GATE** | pilot | `approve` | -- |
| 1 | Revert VM to snapshot | aiops | `vm_clean_slate` | -- |
| 2 | Verify VM is running | monitor | `vm_info` | -- |
| 3 | Verify network segments | nsx | `list_segments` | -- |
| 4 | Verify health (no new alarms) | monitor | `get_alarms` | -- |

**Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `vm_name` | str | Yes | VM to recover |
| `snapshot_name` | str | No | Snapshot to revert to (default: "baseline") |
| `target` | str | No | vCenter target name |

**Example**:
```
plan_workflow("disaster_recovery", {
    vm_name: "app-server-01",
    snapshot_name: "pre-upgrade",
    target: "vcenter-prod"
})
```

---

## 10. patch_deployment

**Purpose**: Rolling patch deployment: upload patch file, execute install, verify health -- one VM at a time. Approval gate before starting.

**Steps** (1 + 3 per VM):

| # | Action | Skill | Tool | Rollback |
|---|--------|-------|------|----------|
| 0 | **APPROVAL GATE** | pilot | `approve` | -- |
| 1 | Upload patch to VM_1 | aiops | `vm_guest_upload` | -- |
| 2 | Install patch on VM_1 | aiops | `vm_guest_exec_output` | -- |
| 3 | Verify health VM_1 | monitor | `get_alarms` | -- |
| ... | (repeat for each VM) | | | |

**Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `vm_names` | list[str] | Yes | VMs to patch |
| `patch_local_path` | str | Yes | Local path to patch file |
| `patch_guest_path` | str | Yes | Destination path inside guest OS |
| `install_command` | str | Yes | Command to run after upload (e.g. "rpm -Uvh /tmp/patch.rpm") |
| `username` | str | No | Guest OS username (default: "root") |
| `password` | str | No | Guest OS password |
| `target` | str | No | vCenter target name |

**Example**:
```
plan_workflow("patch_deployment", {
    vm_names: ["web01", "web02"],
    patch_local_path: "/tmp/security-patch-2026q1.rpm",
    patch_guest_path: "/tmp/security-patch-2026q1.rpm",
    install_command: "rpm -Uvh /tmp/security-patch-2026q1.rpm",
    username: "root",
    password: "...",
    target: "vcenter-prod"
})
```

---

## 11. storage_expansion

**Purpose**: Add iSCSI storage to a host: enable adapter, add target, rescan, verify new datastores.

**Steps** (6):

| # | Action | Skill | Tool | Rollback |
|---|--------|-------|------|----------|
| 0 | Check iSCSI status | storage | `storage_iscsi_status` | -- |
| 1 | Enable iSCSI adapter | storage | `storage_iscsi_enable` | -- |
| 2 | **APPROVAL GATE** | pilot | `approve` | -- |
| 3 | Add iSCSI target | storage | `storage_iscsi_add_target` | `storage_iscsi_remove_target` |
| 4 | Rescan storage | storage | `storage_rescan` | -- |
| 5 | Verify new datastores | storage | `list_all_datastores` | -- |

**Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `host_name` | str | Yes | ESXi host name |
| `iscsi_address` | str | Yes | iSCSI target IP address |
| `iscsi_port` | int | No | iSCSI port (default: 3260) |
| `target` | str | No | vCenter target name |

**Example**:
```
plan_workflow("storage_expansion", {
    host_name: "esxi-04",
    iscsi_address: "10.0.1.100",
    iscsi_port: 3260,
    target: "vcenter-prod"
})
```

---

## 12. baseline_capture

**Purpose**: Capture current infrastructure state as a JSON baseline snapshot. Used with `baseline_audit` and `baseline_remediate` for drift detection.

**Steps** (up to 5, depends on params):

| # | Action | Skill | Tool | Rollback |
|---|--------|-------|------|----------|
| 0 | Capture VM inventory | monitor | `list_virtual_machines` | -- |
| 1 | Capture host inventory | monitor | `list_esxi_hosts` | -- |
| 2 | Capture network segments | nsx | `list_segments` | -- |
| 3 | Capture datastores | storage | `list_all_datastores` | -- |
| 4 | Capture active alarms | monitor | `get_alarms` | -- |

All steps are read-only. No approval gate.

**Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `target` | str | No | vCenter target name |
| `include_vms` | bool | No | Capture VMs (default: True) |
| `include_hosts` | bool | No | Capture hosts (default: True) |
| `include_network` | bool | No | Capture NSX segments (default: True) |
| `include_storage` | bool | No | Capture datastores (default: True) |
| `include_alarms` | bool | No | Capture alarms (default: True) |
| `baseline_name` | str | No | Name for baseline (default: auto-generated timestamp) |

Baselines are saved to `~/.vmware/baselines/{name}.json`.

**Example**:
```
plan_workflow("baseline_capture", {
    target: "vcenter-prod",
    baseline_name: "pre-maintenance-2026q1"
})
```

---

## 13. baseline_audit

**Purpose**: Compare current infrastructure state against a saved baseline to detect configuration drift.

**Steps** (up to 5):

| # | Action | Skill | Tool | Rollback |
|---|--------|-------|------|----------|
| 0 | Current VM inventory | monitor | `list_virtual_machines` | -- |
| 1 | Current host inventory | monitor | `list_esxi_hosts` | -- |
| 2 | Current network segments | nsx | `list_segments` | -- |
| 3 | Current datastores | storage | `list_all_datastores` | -- |
| 4 | Check anomalies | aria | `list_anomalies` | -- |

All steps are read-only. No approval gate.

**Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `baseline_name` | str | No | Baseline to compare against (default: "latest") |
| `target` | str | No | vCenter target name |
| `include_vms` | bool | No | Audit VMs (default: True) |
| `include_hosts` | bool | No | Audit hosts (default: True) |
| `include_network` | bool | No | Audit NSX (default: True) |
| `include_storage` | bool | No | Audit storage (default: True) |

**Example**:
```
plan_workflow("baseline_audit", {
    baseline_name: "pre-maintenance-2026q1",
    target: "vcenter-prod"
})
```

---

## 14. baseline_remediate

**Purpose**: Fix configuration drifts detected by `baseline_audit`. Takes drift items and generates remediation steps with approval.

**Steps** (2 + N drift items + 1):

| # | Action | Skill | Tool | Rollback |
|---|--------|-------|------|----------|
| 0 | Pre-check alarms | monitor | `get_alarms` | -- |
| 1 | **APPROVAL GATE** | pilot | `approve` | -- |
| 2..N+1 | Fix drift item | (varies) | (varies) | (varies) |
| N+2 | Post-verify health | monitor | `get_alarms` | -- |

**Parameters**:

| Param | Type | Required | Description |
|-------|------|----------|-------------|
| `drift_items` | list[dict] | Yes | List of drift items from audit results |
| `target` | str | No | vCenter target name |

Each drift item dict:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | str | Yes | Remediation action name |
| `skill` | str | Yes | Skill to use |
| `tool` | str | Yes | Tool to call |
| `params` | dict | Yes | Tool parameters |
| `resource` | str | No | Resource name (for logging) |
| `rollback_tool` | str | No | Undo tool |
| `rollback_params` | dict | No | Undo parameters |

**Example**:
```
plan_workflow("baseline_remediate", {
    drift_items: [
        {
            resource: "web01",
            action: "fix_cpu",
            skill: "aiops",
            tool: "vm_create_plan",
            params: {operations: [{action: "reconfigure", vm_name: "web01", cpu: 4}]},
        },
        {
            resource: "app-segment",
            action: "recreate_segment",
            skill: "nsx",
            tool: "create_segment",
            params: {segment_id: "app-segment", display_name: "App Segment", ...},
            rollback_tool: "delete_segment",
            rollback_params: {segment_id: "app-segment"},
        }
    ],
    target: "vcenter-prod"
})
```

---

## Template Summary

| Template | Steps | Approval | Skills Used | Risk Level |
|----------|-------|----------|-------------|------------|
| `clone_and_test` | 6 | Yes | aiops, monitor | Medium |
| `incident_response` | 4 | Yes | monitor, aiops | Medium |
| `plan_and_approve` | 3 | Yes | aiops | High |
| `compliance_scan` | 3 | No | monitor, aria | Low |
| `network_segment_setup` | 2-6 | Yes | nsx, nsx-security | Medium |
| `vks_cluster_deploy` | 4 | Yes | vks | Medium |
| `rolling_restart` | 2+3n | Yes | aiops, monitor | Medium |
| `capacity_expansion` | 5 | Yes | aria, aiops, monitor | Medium |
| `disaster_recovery` | 5 | Yes | aiops, monitor, nsx | High |
| `patch_deployment` | 1+3n | Yes | aiops, monitor | Medium |
| `storage_expansion` | 6 | Yes | storage | Medium |
| `baseline_capture` | 1-5 | No | monitor, nsx, storage | Low |
| `baseline_audit` | 2-5 | No | monitor, nsx, storage, aria | Low |
| `baseline_remediate` | 3+n | Yes | varies | High |
