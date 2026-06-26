# Cross-Skill Workflows

vmware-harden produces compliance findings and Suggestions but never executes
remediations directly. Real changes go through `vmware-pilot`, which dispatches
to the right sibling skill (vmware-aiops, vmware-nsx-security, vmware-storage)
for the actual write.

## Workflow 1 — NTP drift remediation (host)

```
1. vmware-harden scan --target prod-vc --baseline cis-vmware-esxi-8.0-subset
   → finds host with ntp_enabled=false (cis-esxi-2.1.1)

2. vmware-harden advise --violation-id <vid>
   → Advisor calls Anthropic; produces Suggestion with execution_plan
     [{step:1, mcp_tool:"vmware_aiops.host_ntp_configure", params:{...}}]

3. vmware-harden apply --violation-id <vid>
   → harden submits Suggestion to PilotClient.submit_remediation()
   → pilot creates a Workflow with one step (skill="aiops", tool="host_ntp_configure")
   → pilot's DispatchFn invokes vmware-aiops MCP tool
   → vmware-aiops applies the change, audit row written via @vmware_tool

4. Subsequent vmware-harden scan
   → cis-esxi-2.1.1 no longer fires; drift event recorded showing
     ntp_enabled: false → true between snapshots
```

## Workflow 2 — DFW any/any anti-pattern remediation

```
1. vmware-harden scan --target prod-vc --baseline pci-dss-4.0-vmware
   → fires pci-r1-1 on a DFW rule with src=ANY/dst=ANY/action=allow

2. vmware-harden advise --all-critical
   → Suggestion proposes deleting or scoping the rule via vmware-nsx-security

3. vmware-harden apply --violation-id <vid>
   → human_review_required=true (scope/destructive); CLI prompts y/N
   → on approve, pilot dispatches to vmware-nsx-security.dfw_rule_delete
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

5. Apply approved suggestions; pilot orchestrates with audit logging

6. Re-scan after a maintenance window; drift page shows what changed
```

## Failure modes (cross-skill)

| Failure | Where it surfaces | Recovery |
|---------|-------------------|----------|
| sibling skill not installed | `harden apply` returns PilotSubmissionError | install with `uv tool install vmware-<sibling>` |
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
