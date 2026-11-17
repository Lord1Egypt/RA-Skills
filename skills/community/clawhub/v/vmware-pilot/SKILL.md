---
name: vmware-pilot
description: >
  Use this skill whenever the user wants to design, execute, or manage complex multi-step VMware workflows with human approval gates and explicit, best-effort rollback.
  Pilot is the orchestration brain — it breaks a goal into steps across companion VMware skills (aiops, monitor, nsx, nsx-security, aria, vks, storage, avi), adds approval gates before destructive operations, and records per-step undo actions that run only when rollback is explicitly called, never automatically.
  Always use vmware-pilot for: "clone and test before applying to production", "VMware incident response with checkpoints", "investigate alert root cause", "VMware rolling restart with health checks", "baseline capture and drift detection", "rolling maintenance with AVI drain", or any VMware workflow needing approval gates or rollback.
  15 built-in templates + custom YAML + AI-designed workflows.
  Do NOT use for single-step work — use vmware-aiops for one VM action, vmware-monitor for read-only queries, vmware-avi for load balancer queries.
installer:
  kind: uv
  package: vmware-pilot
allowed-tools: [Bash]
metadata: {"openclaw":{"requires":{"anyBins":["vmware-pilot","uvx"]},"optional":{"env":["VMWARE_AUDIT_APPROVED_BY"]},"homepage":"https://github.com/vmware-skills/VMware-Pilot","emoji":"🧭","os":["macos","linux"]}}
compatibility: >
  vmware-policy auto-installed as Python dependency (provides @vmware_tool decorator and audit logging). All workflow operations audited to ~/.vmware/audit.db.
  No direct vCenter/NSX credentials: Pilot is an orchestration layer that delegates to companion skills (aiops, monitor, nsx, etc.) which handle their own auth.
  Approval gates: Workflows pause for human review before destructive steps; a custom workflow (YAML, create_workflow, or AI-designed) with a destructive or unclassifiable step not preceded by a gate is rejected, and force=True cannot override that. Rollback is never automatic: a failed step stops the workflow, and undo happens only when rollback is called; it is best-effort, and on the MCP server the calling agent performs each rollback_tool call itself.
  Pilot drives companion skills that change production (VM power, guest commands, network, storage, Kubernetes). Guest commands (run_vm_guest_command, upload_vm_guest_file, …) and credential-returning steps (vks issue_tkc_kubeconfig, issue_supervisor_kubeconfig) are gated like destructive ones.
  State persistence: SQLite-backed workflow state (~/.vmware/workflows.db, owner-only 0600 in a 0700 directory) survives restarts; secret-named params are masked before they are written. No webhooks, no outbound network calls.
  Transitive dependencies: Only vmware-policy (audit/policy). No post-install scripts or background services.
---

# VMware Pilot

> Self-test: [guide](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware" is a trademark of Broadcom. Source code is publicly auditable at [github.com/vmware-skills/VMware-Pilot](https://github.com/vmware-skills/VMware-Pilot) under the MIT license.

Multi-step workflow orchestration for VMware MCP skills — design, approve, execute, rollback.

**Companion Skills**: [vmware-aiops](../vmware-aiops/SKILL.md) (VM operations) | [vmware-monitor](../vmware-monitor/SKILL.md) (monitoring) | [vmware-nsx](../vmware-nsx/SKILL.md) (networking) | [vmware-aria](../vmware-aria/SKILL.md) (metrics/alerts) | [vmware-avi](../vmware-avi/SKILL.md) (load balancing/AKO)

## What This Skill Does

| Capability | Description |
|---|---|
| Workflow Design | Natural language goal → AI designs steps from the `get_skill_catalog` building-block list (101 curated tools across 13 skills) |
| Approval Gates | Pause execution for human review before destructive operations |
| State Persistence | SQLite-backed, survives restarts, supports resume from checkpoint |
| Rollback | Explicit, best-effort undo of completed steps in reverse order — never automatic (see Troubleshooting) |
| Custom Templates | Save workflows as YAML for reuse, hot-reload without restart |
| Compliance Scans | Read-only health/capacity/anomaly checks across skills |

## Quick Install

```bash
uv tool install vmware-pilot==2.5.1
vmware-pilot mcp          # start the MCP server (stdio)
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
AI calls: create_workflow_from_template("clone_and_test", {
    target_vm: "db01",
    change_spec: {memory_mb: 32768},
    snapshot_name: "pre-change",   # required: list_vm_snapshots (monitor)
    target: "vcenter-prod"
})
AI calls: run_workflow(workflow_id)
→ Clone (off) → Resize → Power on → Check → [Approval Gate] → Production → Power off staging
```

### 3. Batch Operations with Approval

```
AI calls: create_workflow_from_template("plan_and_approve", {
    operations: [
        {action: "power_off", vm_name: "db01"},
        {action: "revert_snapshot", vm_name: "db01", snapshot_name: "baseline"},
        {action: "power_on", vm_name: "db01"}
    ]
})
→ Create Plan → [Approval Gate] → Execute Plan
→ If the apply fails, nothing is undone automatically: ask the user, then call
  vmware-aiops rollback_vm_plan(plan_id) yourself
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

**Who executes steps depends on how pilot was started.**

- **`vmware-pilot mcp --dispatch`** (or `VMWARE_PILOT_DISPATCH=stdio`): pilot runs each step itself, in that skill's own MCP server (its policy, confirmation gate and audit apply), and stops at every approval gate — nothing after a gate runs before `approve`. Workflows reach `completed`. stdio only: refused with `--transport https`/`http`.
- **Default (no `--dispatch`): you do.** Every step is recorded `not_executed` and returned in `pending_dispatch`; perform them in order. At a gate, `approve` refuses while earlier steps are `not_executed` — show the user what they returned, then `approve(..., acknowledge_not_executed=True)`; they become `reported_done`. The workflow ends `dispatch_required`, never `completed`.

Without `--dispatch` this is the v2-style architecture: pilot's context stays small, state is always on disk, and there are no persistent agent threads. Full contract details: see [`references/integration-patterns.md`](references/integration-patterns.md#the-dispatch-contract).

**`get_skill_catalog` is a curated design aid, not a whitelist.** It surfaces 101 hand-picked building blocks across 13 skills — a deliberate subset of what those skills expose (aiops alone has 61 tools; the catalog lists 19). A step's `skill` handed to the calling agent may name any companion skill, including ones the catalog does not list; with `--dispatch` only catalog skills run (`pilot` is for approval gates). Use the catalog for inspiration; consult the target skill's own SKILL.md for its full tool surface.

## MCP Tools (13 — 4 read, 9 write/control)

| Category | Tool | Risk | Description |
|---|---|---|---|
| **Discovery** | `get_skill_catalog` | low | Available skills and tools for design |
| | `list_workflows` | low | Built-in + custom templates |
| **Design** | `design_workflow` | low | Natural language → draft |
| | `update_draft` | medium | Edit draft steps |
| | `confirm_draft` | medium | Finalize draft → ready to execute |
| **Execute** | `create_workflow_from_template` | medium | Create from template |
| | `create_workflow` | medium | One-step custom creation (rejected if a destructive step has no gate before it) |
| | `review_workflow` | low | Structural sanity check before execution (approved \| needs_revision) |
| | `run_workflow` | medium | Execute next checkpoint (agent dispatches each step) |
| **Control** | `approve` | high | Human approval to continue |
| | `cancel_workflow` | high | Cancel a workflow (approval rejected / unsafe) → terminal CANCELLED, can't be run. Previews unless `confirm=True` |
| | `rollback` | high | Explicit, best-effort undo; never runs on its own. Previews unless `confirm=True` |

**`rollback` and `cancel_workflow` preview by default.** Without `confirm=True` they return `blast_radius` (steps that would be undone, left applied, or skipped) and change nothing. Show it to the user; the user has not seen the preview yet, so do not set `confirm=True` on your own. They refuse when the state does not allow the transition, the record cannot be read, or a step was left `running`/`interrupted` (its effect is unknown: have the user check it in the target system, then pass `acknowledge_unknown_effects=True`).

**Template steps pass `confirm=True`.** Destructive companion tools preview unless called with `confirm=True`; in every built-in template such a step comes after an `approve` gate, so it carries `confirm=True` — dispatch it as listed. A step that only returned `action: preview` is recorded `failed`, not `success`.
| | `get_workflow_status` | low | State + audit log |

## Built-in Templates (15)

The five most-used:

| Template | Steps | Approval | Skills Used |
|---|---|---|---|
| `clone_and_test` | 7 (8 for a guest command) | Yes | aiops + monitor |
| `incident_response` | 4 | Yes | monitor + aiops |
| `investigate_alert` | 4 / 8 | Yes | monitor + aria (parallel-group gather + 4-criteria checkpoint, optional `deep_dive`) |
| `plan_and_approve` | 3 | Yes | aiops |
| `compliance_scan` | 3 | No | monitor + aria |

Full list: `clone_and_test`, `incident_response`, `investigate_alert`, `plan_and_approve`, `compliance_scan`, `network_segment_setup`, `vks_cluster_deploy`, `rolling_restart`, `capacity_expansion`, `disaster_recovery`, `patch_deployment`, `storage_expansion`, `baseline_capture`, `baseline_audit`, `baseline_remediate`. See `references/templates.md` for full details.

## Custom Templates

Drop YAML files in `~/.vmware/workflows/` — pilot auto-loads them.

**Approval gates are mandatory in custom workflows.** Every destructive step (the
skill catalog marks it high/critical risk, or its name says delete/remove/…) and
every step pilot cannot classify must have a `require_approval` step somewhere
before it. Otherwise `create_workflow_from_template`, `create_workflow` and `confirm_draft` refuse
the workflow and name the offending steps, `run_workflow` refuses it even with
`force=True`, and `scripts/validate_workflow.py` reports an error. Medium-risk
writes (`create_segment`, `power_on_vm`, …) do not require a gate.

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
  - action: require_approval        # required: the next step changes the estate
    skill: pilot
    tool: approve
    params:
      message: "Cluster healthy. Stop replica {{replica_vm}}?"
  - action: stop_replica
    skill: aiops
    tool: power_off_vm
    params:
      vm_name: "{{replica_vm}}"
    rollback_tool: power_on_vm
    rollback_params:
      vm_name: "{{replica_vm}}"
  - action: restart_primary
    skill: aiops
    tool: power_off_vm
    params:
      vm_name: "{{primary_vm}}"
```

## Usage Mode

| Scenario | Recommended | Why |
|----------|:-----------:|-----|
| Local/small models (Ollama, Qwen) | **MCP** | Structured JSON I/O for multi-step state |
| Cloud models (Claude, GPT-4o) | **MCP** | Design mode needs structured tool calls |
| CI/CD pipeline orchestration | **MCP** | Programmatic plan/approve/run cycle |
| Quick template listing | **MCP** | Call `list_workflows`; the CLI has no template commands |

> Note: every workflow operation — design, plan, run, approve, rollback — is MCP-only.
> The `vmware-pilot` CLI exists to launch the server and report its version, nothing more.
> Other skills in the family (aiops, monitor, avi, etc.) offer full CLI and MCP modes.

## CLI Quick Reference

The CLI is a launcher, not a second interface to workflows:

```bash
vmware-pilot mcp        # start the MCP server (stdio)
vmware-pilot version    # print installed version
vmware-pilot --help

# Validate a custom workflow YAML before loading (runs pilot's own gate check,
# so it needs the Python vmware-pilot is installed in)
"$(uv tool dir)/vmware-pilot/bin/python" scripts/validate_workflow.py ~/.vmware/workflows/my_workflow.yaml

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
Call `approve(workflow_id, approver=...)` with the correct workflow ID to continue, or `cancel_workflow(workflow_id)` if the approval is rejected (it previews first; call again with `confirm=True` once the user has seen it). If the MCP session was lost, reconnect and call `get_workflow_status(workflow_id)` to see the current state -- workflows persist in SQLite and survive restarts.

### "Unknown workflow type" error from create_workflow_from_template
The template name is case-sensitive. Use `list_workflows()` to see all available built-in and custom template names. Custom templates must be valid YAML in `~/.vmware/workflows/`.

### Custom YAML template not appearing
1. Verify the file is in `~/.vmware/workflows/` with a `.yaml` extension
2. Check YAML syntax -- run `scripts/validate_workflow.py <path>` with pilot's Python (see CLI Quick Reference)
3. A YAML file you drop in whose name matches a built-in replaces it (a warning is logged) -- rename it if that is not what you want. `create_workflow` and `confirm_draft` refuse to save a template under a built-in name
4. A file that lists but will not plan is missing an approval gate -- the `create_workflow_from_template` error names the step and the file

### Rollback did nothing, or fails on some steps
Rollback never happens on its own: a failed step leaves the workflow `failed` and stops. A bare `rollback(workflow_id)` only previews; `confirm=True` acts. It only reverses steps pilot recorded as `success`, and on the MCP server (no dispatcher) the steps you performed from `pending_dispatch` stay `not_executed` — so `rollback` there reverses nothing. Undo them yourself: call each performed step's `rollback_tool` with its `rollback_params`, last step first, after confirming with the user. Steps without a `rollback_tool` cannot be undone: rollback reports them `not_reversible`, and the preview lists steps handed to you that have none under `not_reversible_outside_pilot` — if you performed them (a clone, a production resize) they stay. An undo that does not remove what the step created is `partial` — a clone that was only powered off stays; delete it by hand. When pilot dispatches (`--dispatch`), rollback is best-effort: a failed undo does not stop the rest, and the result reports each one.

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
      "command": "vmware-pilot",
      "args": ["mcp"]
    }
  }
}
```

Add `"--dispatch"` to `args` to have pilot run the steps itself (each companion skill must be installed: `vmware-<skill>-mcp` on `PATH`).

> Fallback: `{"command": "uvx", "args": ["--from", "vmware-pilot==2.5.1", "vmware-pilot-mcp"]}` also
> works, but `uvx` re-resolves the package against PyPI on every start and fails behind a
> TLS-inspecting corporate proxy (`invalid peer certificate: UnknownIssuer`). The installed
> entry point above touches the network zero times; set `UV_NATIVE_TLS=true` if you must use `uvx`.

## Audit & Safety

All operations are automatically audited via vmware-policy (`@vmware_tool` decorator):
- Every tool call logged to `~/.vmware/audit.db` (SQLite, framework-agnostic)
- Policy rules enforced via `~/.vmware/rules.yaml` (deny rules, maintenance windows, risk levels)
- Risk classification: each tool tagged as low/medium/high/critical
- Environment scoping: policy rules can scope by environment (an optional label an opt-in `deny` rule may match), and skills with a config may declare `environment:` per target. Pilot has no targets of its own and registers no environment resolver, so its own calls are unlabeled (they match no environment-scoped rule) — its writes go to the local workflow DB, never to a VMware estate. Pilot's approval gate is a step in its own workflow: it pauses before the agent dispatches a destructive step, and the target skill then applies its own policy rules when the step runs
- View recent operations: `vmware-audit log --last 20`
- View denied operations: `vmware-audit log --status denied`
- Credential steps: `vks issue_tkc_kubeconfig` and `issue_supervisor_kubeconfig` return a live Supervisor token. Treat them as credential access, not read-only queries — never run one on your own initiative, keep it behind an approval gate (pilot gates both like a delete), write the kubeconfig to an owner-only file, and never print the token into chat or logs
- Local data is sensitive: `~/.vmware/workflows.db` (pilot keeps `~/.vmware` 0700 and the DB 0600) holds step params and companion-skill results, with secret-named params masked. Pilot never writes `~/.vmware/baselines/`; a baseline the agent saves there is an inventory of VMs, hosts, network segments, datastores and alarms — keep it owner-only and out of chat

vmware-policy is automatically installed as a dependency — no manual setup needed.

## License

MIT
