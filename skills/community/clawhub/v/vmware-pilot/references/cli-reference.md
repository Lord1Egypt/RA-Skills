# CLI Reference — vmware-pilot

The `vmware-pilot` CLI is a **launcher, not a second interface to workflows**. It starts the
MCP server and reports its version — nothing else. Every workflow operation (design, plan,
run, approve, rollback, cancel) is performed via MCP tool calls through an AI agent or MCP
client.

---

## Commands

| Command | Description |
|---------|-------------|
| `vmware-pilot mcp` | Start the MCP server on stdio transport |
| `vmware-pilot version` | Print the installed version |
| `vmware-pilot --help` | Show usage |

## MCP Server Launch

```bash
# Recommended: installed entry point, never touches the network
uv tool install vmware-pilot==2.5.1
vmware-pilot mcp

# Fallback: uvx re-resolves against PyPI each start and fails behind a
# TLS-inspecting corporate proxy — set UV_NATIVE_TLS=true if you must use it
uvx --from vmware-pilot==2.5.1 vmware-pilot-mcp
```

The server runs on **stdio** transport and exposes 13 MCP tools (4 read, 9 write).

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

#### create_workflow_from_template

Create a workflow from a built-in or custom template.

```
create_workflow_from_template(
    workflow_type="clone_and_test",
    params={target_vm: "db01", change_spec: {memory_mb: 32768}, snapshot_name: "pre-change"}
)
→ {workflow_id: "wf-...", steps: [...]}
```

Available types: `clone_and_test`, `incident_response`, `plan_and_approve`, `compliance_scan`,
`network_segment_setup`, `vks_cluster_deploy`, `rolling_restart`, `capacity_expansion`,
`disaster_recovery`, `patch_deployment`, `storage_expansion`, `baseline_capture`,
`baseline_audit`, `baseline_remediate`.

#### create_workflow

Create a custom workflow directly from a step list. Refused — nothing saved —
if any destructive or unclassifiable step has no `require_approval` step before
it; the error names each step and the gate to insert.

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

Explicit, best-effort undo — never runs on its own. Reverses, last first, only
the steps pilot recorded as `success`; on the MCP server the steps you performed
are `not_executed`, so undo them yourself with each step's `rollback_tool`.

```
rollback(workflow_id="wf-...")
→ {action: "preview", blast_radius: {would_roll_back: [...], left_in_place: [...], blockers: [], ...}}

rollback(workflow_id="wf-...", confirm=True)   # after the user has seen the preview
→ {action: "rolled_back", state: "failed", rollback_results: [...], blast_radius: {...}}
```

`cancel_workflow(workflow_id, reason, confirm=False)` works the same way: the
preview lists the executed steps that stay applied, the steps already handed to
you in `pending_dispatch` (`handed_out_to_caller` — cancel neither stops nor undoes
them) and the steps that would be skipped; `confirm=True` cancels.

Both refuse `confirm=True` while a step is in `unknown_effects` (left `running`
or `interrupted` when a Pilot process stopped mid-dispatch). Check in the target
system whether that step took effect, then re-run with
`acknowledge_unknown_effects=True`.

#### get_workflow_status

Query workflow state, diff report, and audit log.

```
get_workflow_status(workflow_id="wf-...")
→ {state: "completed", steps: [...], audit_log: [...]}
```

---

## Helper Scripts

### validate_workflow.py

Validate a custom YAML workflow template before use. It runs pilot's own
approval-gate check, so use the Python vmware-pilot is installed in:

```bash
"$(uv tool dir)/vmware-pilot/bin/python" scripts/validate_workflow.py ~/.vmware/workflows/my_workflow.yaml
```

Checks:
- Step structure has required fields
- **Error** (exit 1): a destructive or unclassifiable step with no `require_approval` before it — `create_workflow_from_template` would refuse the file
- Warning: skills or tools not in the catalog

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
    tool: power_off_vm
    params:
      vm_name: "{{vm_name}}"
    rollback_tool: power_on_vm
    rollback_params:
      vm_name: "{{vm_name}}"
```

Place in `~/.vmware/workflows/` with `.yaml` extension. Hot-reloaded without restart.
