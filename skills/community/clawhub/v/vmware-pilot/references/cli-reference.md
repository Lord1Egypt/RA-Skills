# CLI Reference — vmware-pilot

vmware-pilot is an **MCP-only** server. It does not provide a standalone CLI binary.
All workflow operations are performed via MCP tool calls through an AI agent or MCP client.

---

## MCP Server Launch

```bash
# Recommended: via uvx (isolated environment)
uvx --from vmware-pilot vmware-pilot-mcp

# Alternative: via pip install
pip install vmware-pilot
vmware-pilot-mcp
```

The server runs on **stdio** transport and exposes 11 MCP tools.

---

## MCP Tool Reference

### Discovery Tools

#### get_skill_catalog

Get available skills and tools for workflow design.

```
get_skill_catalog()
→ {aiops: {tools: {...}}, monitor: {...}, nsx: {...}, ...}
```

#### list_workflows

List built-in and custom templates, plus active workflows.

```
list_workflows()
→ {templates: [...], active_workflows: [...]}
```

### Design Tools

#### design_workflow

Create a draft workflow from natural language description.

```
design_workflow(
    goal="Migrate app01 to new network with firewall",
    constraints="approval before destructive steps"
)
→ {workflow_id: "wf-...", state: "draft", next_step: "..."}
```

#### update_draft

Edit a draft workflow's name, description, or steps.

```
update_draft(
    workflow_id="wf-...",
    name="app_migration",
    steps=[{action: "...", skill: "...", tool: "...", params: {...}}]
)
→ {workflow_id: "wf-...", steps: [...]}
```

#### confirm_draft

Finalize a draft workflow for execution (DRAFT -> PENDING).

```
confirm_draft(
    workflow_id="wf-...",
    save_as_template=True
)
→ {workflow_id: "wf-...", state: "pending"}
```

### Execution Tools

#### plan_workflow

Create a workflow from a built-in or custom template.

```
plan_workflow(
    workflow_type="clone_and_test",
    params={target_vm: "db01", change_spec: {memory_mb: 32768}}
)
→ {workflow_id: "wf-...", steps: [...]}
```

Available types: `clone_and_test`, `incident_response`, `plan_and_approve`, `compliance_scan`,
`network_segment_setup`, `vks_cluster_deploy`, `rolling_restart`, `capacity_expansion`,
`disaster_recovery`, `patch_deployment`, `storage_expansion`, `baseline_capture`,
`baseline_audit`, `baseline_remediate`.

#### create_workflow

Create a custom workflow directly from a step list.

```
create_workflow(
    name="quick_restart",
    description="Restart with health check",
    steps=[...],
    save_as_template=False
)
→ {workflow_id: "wf-...", steps: [...]}
```

#### run_workflow

Execute a planned workflow. Pauses at approval gates.

```
run_workflow(workflow_id="wf-...")
→ {state: "awaiting_approval", current_step: {...}}
```

### Control Tools

#### approve

Human approval to continue past an approval gate.

```
approve(
    workflow_id="wf-...",
    approver="admin@example.com"
)
→ {state: "running", ...}
```

#### rollback

Abort and reverse completed steps in reverse order.

```
rollback(workflow_id="wf-...")
→ {state: "failed", rollback_results: [...]}
```

#### get_workflow_status

Query workflow state, diff report, and audit log.

```
get_workflow_status(workflow_id="wf-...")
→ {state: "completed", steps: [...], audit_log: [...]}
```

---

## Helper Scripts

### validate_workflow.py

Validate a custom YAML workflow template before use.

```bash
python3 scripts/validate_workflow.py ~/.vmware/workflows/my_workflow.yaml
```

Checks:
- All referenced skills exist in the catalog
- Tool names are recognized
- Approval gates are placed before destructive steps
- Step structure has required fields

### list_available_tools.py

Browse all available skills and tools for workflow design.

```bash
python3 scripts/list_available_tools.py          # All skills
python3 scripts/list_available_tools.py aiops    # Specific skill
python3 scripts/list_available_tools.py --json   # JSON output
```

---

## Audit Log (via vmware-policy)

```bash
vmware-audit log --last 20          # Recent operations
vmware-audit log --status denied    # Denied by policy
vmware-audit log --tool approve     # Filter by tool
```

---

## Custom Workflow YAML Format

```yaml
name: my_workflow
description: Human-readable description
steps:
  - action: check_health
    skill: monitor
    tool: get_alarms
    params:
      target: "{{target}}"

  - action: require_approval
    skill: pilot
    tool: approve
    params:
      message: "Proceed with changes?"

  - action: apply_change
    skill: aiops
    tool: vm_power_off
    params:
      vm_name: "{{vm_name}}"
    rollback_tool: vm_power_on
    rollback_params:
      vm_name: "{{vm_name}}"
```

Place in `~/.vmware/workflows/` with `.yaml` extension. Hot-reloaded without restart.
