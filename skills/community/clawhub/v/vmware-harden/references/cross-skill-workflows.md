# Cross-Skill Workflows

vmware-harden produces compliance findings and Suggestions. **It never changes a
VMware system, and it never runs a remediation.** Its MCP tools are all read-only.
The one hand-off point is the CLI-only `vmware-harden apply`: it saves the
Suggestion's plan as a **pending** `vmware-pilot` workflow (with an approval-gate
step) and stops. Nothing runs until someone drives that workflow through pilot
(`run_workflow`, then `approve` at the gate), and each step is then performed by
the sibling skill that owns the write (vmware-aiops, vmware-nsx-security,
vmware-storage), under that skill's own confirmation gate and audit.

The tool names below are illustrative: a Suggestion's `execution_plan` names
whatever tool the Advisor proposed, and pilot refuses a step whose tool its
skill does not have.

## Workflow 1 — NTP drift remediation (host)

```
1. vmware-harden scan --target prod-vc --baseline cis-vmware-esxi-8.0-subset
   → finds host with ntp_enabled=false (cis-esxi-2.1.1)

2. vmware-harden advise --violation-id <vid>
   → Advisor calls Anthropic; produces Suggestion with execution_plan
     [{step:1, mcp_tool:"<aiops host NTP tool>", params:{...}}]

3. vmware-harden apply --violation-id <vid> --pilot real
   → harden saves a PENDING pilot workflow (plan steps + approval gate)
   → prints the workflow id; nothing has run and nothing has changed

4. In vmware-pilot: run_workflow(<id>) → stops at the approval gate →
   approve(<id>) → the aiops step runs under aiops' own gate and audit

5. Subsequent vmware-harden scan
   → cis-esxi-2.1.1 no longer fires; drift event recorded showing
     ntp_enabled: false → true between snapshots
```

## Workflow 2 — DFW any/any anti-pattern remediation

```
1. vmware-harden scan --target prod-vc --baseline pci-dss-4.0-vmware
   → fires pci-r1-1 on a DFW rule with src=ANY/dst=ANY/action=allow

2. vmware-harden advise --all-critical
   → Suggestion proposes scoping (or deleting) the rule via vmware-nsx-security

3. vmware-harden apply --violation-id <vid> --pilot real
   → human_review_required=true (scope/destructive); CLI prompts y/N before
     it will even save the workflow
   → on yes, a PENDING pilot workflow is saved; nothing runs yet

4. In vmware-pilot: run_workflow → approval gate → approve → the
   nsx-security step runs (e.g. delete_dfw_rule, which previews its
   blast radius and needs confirm=True)
```

## Workflow 3 — 等保 2.0 audit lifecycle

```
1. Initial scan (collectors: host, vm, datastore, dfw_rule)
   vmware-harden scan --target prod-vc --baseline dengbao-2.0-level3-vmware

2. Web review for non-technical auditor
   vmware-harden web --port 8080
   → Summary radar / Violations table / Drift timeline

3. Generate suggestions for critical findings
   vmware-harden advise --all-critical

4. Manual review of each Suggestion's impact_prediction in the web panel

5. `vmware-harden apply --pilot real` for each approved suggestion saves a pending
   pilot workflow; run and approve each one in vmware-pilot, which logs every step

6. Re-scan after a maintenance window; drift page shows what changed
```

## Failure modes (cross-skill)

| Failure | Where it surfaces | Recovery |
|---------|-------------------|----------|
| sibling skill not installed | `harden apply` returns PilotSubmissionError | `uv tool install "vmware-harden[remediation]==1.20.0"` — installing the sibling on its own lands in a separate tool env harden cannot import from |
| sibling skill API drift | pilot dispatch fails mid-workflow | pilot's rollback runs; harden marks remediation as failed |
| baseline references unknown mcp_tool | harden advise produces Suggestion that pilot can't dispatch | edit baseline YAML's `remediation.mcp_tool` to a real tool name |
| harden Twin DB stale vs vCenter | re-run `harden scan --target ...` to refresh |

## Family awareness map

| Question | Skill |
|----------|-------|
| Is this VM compliant with 等保? | vmware-harden |
| Configure NTP on a host | vmware-aiops |
| Modify DFW rule | vmware-nsx-security |
| Encrypt a datastore | vmware-storage |
| Orchestrate multi-step change with approval | vmware-pilot (via harden apply) |
| Read-only inventory snapshot | vmware-monitor |
| Aria Operations metrics | vmware-aria |
