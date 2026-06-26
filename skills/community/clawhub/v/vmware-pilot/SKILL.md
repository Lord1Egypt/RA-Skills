---
name: vmware-pilot
description: >
  Use this skill whenever the user wants to design, execute, or manage complex multi-step VMware workflows with human approval and automatic rollback.
  Pilot is the orchestration brain — it breaks down a user's goal into steps across multiple VMware skills (aiops, monitor, nsx, aria, vks, storage, avi), adds approval gates before destructive operations, and rolls back automatically if anything fails.
  Always use vmware-pilot for: "clone and test before applying to production", "VMware incident response with checkpoints", "investigate alert root cause", "set up VMware infrastructure using multiple skills", "VMware rolling restart with health checks", "baseline capture and drift detection", "rolling maintenance with AVI drain", "AKO-aware app deployment", or any VMware workflow needing approval gates or rollback.
  15 built-in templates + custom YAML + AI-designed workflows from 185 available tools across 8 skills.
  For single VM operations use vmware-aiops, for read-only queries use vmware-monitor, for load balancer operations use vmware-avi.
installer:
  kind: uv
  package: vmware-pilot
allowed-tools: [Bash]
metadata: {"openclaw":{"requires":{"env":["VMWARE_PILOT_CONFIG"],"bins":["vmware-pilot-mcp"]},"primaryEnv":"VMWARE_PILOT_CONFIG","homepage":"https://github.com/zw008/VMware-Pilot","emoji":"🧭","os":["macos","linux"]}}
compatibility: >
  vmware-policy auto-installed as Python dependency (provides @vmware_tool decorator and audit logging). All workflow operations audited to ~/.vmware/audit.db.
  No direct vCenter/NSX credentials: Pilot is an orchestration layer that delegates to companion skills (aiops, monitor, nsx, etc.) which handle their own auth.
  Approval gates: Workflows pause for human review before destructive steps. Rollback automatically reverses completed steps on failure.
  State persistence: SQLite-backed workflow state survives restarts. No webhooks, no outbound network calls.
  Transitive dependencies: Only vmware-policy (audit/policy). No post-install scripts or background services.
---

# VMware Pilot

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware" is a trademark of Broadcom. Source code is publicly auditable at [github.com/zw008/VMware-Pilot](https://github.com/zw008/VMware-Pilot) under the MIT license.

Multi-step workflow orchestration for VMware MCP skills — design, approve, execute, rollback.

**Companion Skills**: [vmware-aiops](../vmware-aiops/SKILL.md) (VM operations) | [vmware-monitor](../vmware-monitor/SKILL.md) (monitoring) | [vmware-nsx](../vmware-nsx/SKILL.md) (networking) | [vmware-aria](../vmware-aria/SKILL.md) (metrics/alerts) | [vmware-avi](../vmware-avi/SKILL.md) (load balancing/AKO)

## What This Skill Does

| Capability | Description |
|---|---|
| Workflow Design | Natural language goal → AI designs steps from 8 skills' 185 tools |
| Approval Gates | Pause execution for human review before destructive operations |
| State Persistence | SQLite-backed, survives restarts, supports resume from checkpoint |
| Rollback | Reverse completed steps in order if workflow fails |
| Custom Templates | Save workflows as YAML for reuse, hot-reload without restart |
| Compliance Scans | Read-only health/capacity/anomaly checks across skills |

## Quick Install

```bash
pip install vmware-pilot
# or
uvx --from vmware-pilot vmware-pilot-mcp
```

## When to Use This Skill

| Scenario | Use Pilot? | Why |
|---|---|---|
| "Clone VM, test, then apply to prod" | Yes | Multi-step + approval |
| "Power on a VM" | No, use aiops | Single operation |
| "Set up app network + firewall + VMs" | Yes | Cross-skill orchestration |
| "Check cluster health" | No, use monitor/aria | Single read-only query |
| "Diagnose and fix an alert" | Yes | incident_response template |
| "Run compliance check" | Yes | compliance_scan template |
| "Drain server, patch, restore traffic" | Yes | Cross-skill: avi drain + aiops patch |
| "Deploy app with AKO ingress" | Yes | Cross-skill: aiops + vks + avi |
| "Check pool member health" | No, use avi | Single read-only query |

## Related Skills — Skill Routing

| User Intent | Recommended Skill |
|---|---|
| VM lifecycle (power, clone, deploy) | **vmware-aiops** (`uv tool install vmware-aiops`) |
| Read-only monitoring | **vmware-monitor** (`uv tool install vmware-monitor`) |
| NSX networking (segments, gateways, NAT) | **vmware-nsx** (`uv tool install vmware-nsx-mgmt`) |
| NSX security (DFW, groups) | **vmware-nsx-security** (`uv tool install vmware-nsx-security`) |
| Aria metrics/alerts/capacity | **vmware-aria** (`uv tool install vmware-aria`) |
| Tanzu Kubernetes (Supervisor/TKC) | **vmware-vks** (`uv tool install vmware-vks`) |
| Storage (iSCSI, vSAN, datastores) | **vmware-storage** (`uv tool install vmware-storage`) |
| Load balancing, VS, pool, AKO | **vmware-avi** (`uv tool install vmware-avi`) |
| Audit log query | **vmware-policy** (`vmware-audit` CLI) |
| **Multi-step orchestration** | **vmware-pilot** (this skill) |

## Common Workflows

### 1. Design a Custom Workflow (Interactive)

```
User: "I need to set up a new app environment with networking and VMs"

AI calls: get_skill_catalog()          → see available tools
AI calls: design_workflow(goal="...")   → create draft
AI calls: update_draft(id, steps=[...]) → fill in steps
User reviews and confirms
AI calls: confirm_draft(id, save_as_template=True)
AI calls: run_workflow(id)             → execute with approval gates
```

### 2. Clone-and-Test (Built-in Template)

```
AI calls: plan_workflow("clone_and_test", {
    target_vm: "db01",
    change_spec: {memory_mb: 32768},
    target: "vcenter-prod"
})
AI calls: run_workflow(workflow_id)
→ Clone → Apply → Monitor → [Approval Gate] → Commit → Cleanup
```

### 3. Batch Operations with Approval

```
AI calls: plan_workflow("plan_and_approve", {
    operations: [
        {action: "power_off", vm_name: "db01"},
        {action: "revert_snapshot", vm_name: "db01", snapshot_name: "baseline"},
        {action: "power_on", vm_name: "db01"}
    ]
})
→ Create Plan → [Approval Gate] → Execute Plan (with auto-rollback on failure)
```

### 4. Rolling Maintenance with AVI Drain

Drain traffic from a pool member via AVI, patch the server, then restore traffic:

```
1. vmware-avi pool disable <pool> <server>     # drain traffic from pool member
2. vmware-avi analytics <vs>                    # verify drain complete (0 active connections)
3. vmware-aiops vm guest-exec <vm> --cmd "apt-get upgrade -y"   # patch the server
4. vmware-avi pool enable <pool> <server>       # restore traffic to pool member
5. vmware-avi pool members <pool>               # verify health status is green
```

### 5. AKO-Aware Application Deployment

Deploy a backend VM, create a K8s namespace, and wire up AKO Ingress to the AVI Controller:

```
1. vmware-aiops deploy ova <image> --name <vm>  # deploy backend VM
2. vmware-vks namespace create <ns>             # create K8s namespace
3. kubectl apply -f ingress.yaml                # create Ingress with AKO annotations
4. vmware-avi ako ingress check <ns>            # validate AKO annotations are correct
5. vmware-avi ako sync status                   # verify VS created on AVI Controller
```

## Dispatch Contract (Important)

**Pilot is a Dispatcher, not an Executor.** It generates plans, tracks state, gates on approvals — it does NOT call companion skills' MCP tools itself. The calling AI agent is responsible for invoking `vmware-aiops::vm_clone` etc. when pilot's `run_workflow` returns a step description.

This is intentional v2-style architecture: pilot's context stays small, state is always on disk, and there are no persistent agent threads. Full contract details: see [`references/integration-patterns.md`](references/integration-patterns.md#the-dispatch-contract).

## MCP Tools (13 — 4 read, 9 write/control)

| Category | Tool | Risk | Description |
|---|---|---|---|
| **Discovery** | `get_skill_catalog` | low | Available skills and tools for design |
| | `list_workflows` | low | Built-in + custom templates |
| **Design** | `design_workflow` | low | Natural language → draft |
| | `update_draft` | medium | Edit draft steps |
| | `confirm_draft` | medium | Finalize draft → ready to execute |
| **Execute** | `plan_workflow` | medium | Create from template |
| | `create_workflow` | medium | One-step custom creation |
| | `review_workflow` | low | Structural sanity check before execution (approved \| needs_revision) |
| | `run_workflow` | medium | Execute next checkpoint (agent dispatches each step) |
| **Control** | `approve` | high | Human approval to continue |
| | `cancel_workflow` | high | Cancel a workflow (approval rejected / unsafe) → terminal CANCELLED, can't be run |
| | `rollback` | high | Reverse completed steps |
| | `get_workflow_status` | low | State + audit log |

## Built-in Templates (15)

The five most-used:

| Template | Steps | Approval | Skills Used |
|---|---|---|---|
| `clone_and_test` | 6 | Yes | aiops + monitor |
| `incident_response` | 4 | Yes | monitor + aiops |
| `investigate_alert` | 4 / 8 | Yes | monitor + aria (parallel-group gather + 4-criteria checkpoint, optional `deep_dive`) |
| `plan_and_approve` | 3 | Yes | aiops |
| `compliance_scan` | 3 | No | monitor + aria |

Full list: `clone_and_test`, `incident_response`, `investigate_alert`, `plan_and_approve`, `compliance_scan`, `network_segment_setup`, `vks_cluster_deploy`, `rolling_restart`, `capacity_expansion`, `disaster_recovery`, `patch_deployment`, `storage_expansion`, `baseline_capture`, `baseline_audit`, `baseline_remediate`. See `references/templates.md` for full details.

## Custom Templates

Drop YAML files in `~/.vmware/workflows/` — pilot auto-loads them.

```yaml
# ~/.vmware/workflows/restart_cluster.yaml
name: restart_cluster
description: Rolling restart of database cluster
steps:
  - action: check_health
    skill: monitor
    tool: get_alarms
    params:
      target: "{{target}}"
  - action: stop_replica
    skill: aiops
    tool: vm_power_off
    params:
      vm_name: "{{replica_vm}}"
    rollback_tool: vm_power_on
    rollback_params:
      vm_name: "{{replica_vm}}"
  - action: require_approval
    skill: pilot
    tool: approve
    params:
      message: "Replica stopped. Proceed?"
  - action: restart_primary
    skill: aiops
    tool: vm_power_off
    params:
      vm_name: "{{primary_vm}}"
```

## Usage Mode

| Scenario | Recommended | Why |
|----------|:-----------:|-----|
| Local/small models (Ollama, Qwen) | **MCP** | Structured JSON I/O for multi-step state |
| Cloud models (Claude, GPT-4o) | **MCP** | Design mode needs structured tool calls |
| CI/CD pipeline orchestration | **MCP** | Programmatic plan/approve/run cycle |
| Quick template listing | **CLI** | `vmware-pilot-mcp` is MCP-only; use MCP client |

> Note: vmware-pilot is MCP-only (no standalone CLI). All interactions go through MCP tool calls.
> Other skills in the family (aiops, monitor, avi, etc.) offer both CLI and MCP modes.

## CLI Quick Reference

vmware-pilot is an MCP-only server (no standalone CLI binary). Interact via MCP tool calls:

```bash
# Start the MCP server
uvx --from vmware-pilot vmware-pilot-mcp

# Validate a custom workflow YAML before loading
python3 scripts/validate_workflow.py ~/.vmware/workflows/my_workflow.yaml

# List available tools across all skills (design helper)
python3 scripts/list_available_tools.py          # all skills
python3 scripts/list_available_tools.py aiops    # specific skill
python3 scripts/list_available_tools.py --json   # JSON output

# View audit logs (via vmware-policy)
vmware-audit log --last 20
vmware-audit log --status denied
```

> Full CLI reference for companion skills: see `references/cli-reference.md`

## Troubleshooting

### Workflow stuck in "awaiting_approval"
Call `approve(workflow_id)` with the correct workflow ID to continue, or `rollback(workflow_id)` to abort. If the MCP session was lost, reconnect and call `get_workflow_status(workflow_id)` to see the current state -- workflows persist in SQLite and survive restarts.

### "Unknown workflow type" error from plan_workflow
The template name is case-sensitive. Use `list_workflows()` to see all available built-in and custom template names. Custom templates must be valid YAML in `~/.vmware/workflows/`.

### Custom YAML template not appearing
1. Verify the file is in `~/.vmware/workflows/` with a `.yaml` extension
2. Check YAML syntax -- run `python3 scripts/validate_workflow.py <path>` to validate
3. Template names must be unique -- a custom template cannot shadow a built-in name

### Rollback fails on some steps
Not all steps are reversible. Steps without `rollback_tool` defined are skipped during rollback. Pilot uses best-effort rollback: if one rollback step fails, it continues with remaining steps and reports which succeeded and which failed.

### "Workflow cannot be run" state error
A workflow can only be run from `pending` or `running` states. If it is in `draft`, call `confirm_draft()` first. If it is in `completed` or `failed`, create a new workflow -- completed workflows cannot be re-run.

### vmware-policy dependency missing
Pilot requires `vmware-policy` for the `@vmware_tool` decorator and audit logging. It is declared as a dependency in `pyproject.toml` and should install automatically. If missing, run `pip install vmware-policy` or reinstall pilot.

## Setup

No vCenter credentials needed — pilot orchestrates other skills that handle connections.

```json
{
  "mcpServers": {
    "vmware-pilot": {
      "command": "uvx",
      "args": ["--from", "vmware-pilot", "vmware-pilot-mcp"]
    }
  }
}
```

## Audit & Safety

All operations are automatically audited via vmware-policy (`@vmware_tool` decorator):
- Every tool call logged to `~/.vmware/audit.db` (SQLite, framework-agnostic)
- Policy rules enforced via `~/.vmware/rules.yaml` (deny rules, maintenance windows, risk levels)
- Risk classification: each tool tagged as low/medium/high/critical
- View recent operations: `vmware-audit log --last 20`
- View denied operations: `vmware-audit log --status denied`

vmware-policy is automatically installed as a dependency — no manual setup needed.

## License

MIT
