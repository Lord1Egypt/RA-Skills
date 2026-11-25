# Two small read-only toolsets for an MCP gateway

Offline integration examples for AIops #45. Reuse the canonical [VM performance](vm-performance.md), [host alarms](host-alarms.md) and [case reports](scenario-reports.md) procedures. This reference adds no collector, gateway, tools or authorization behavior. The procedures and optional report views are available in Debug 2.4.0; deployment-specific gateway validation remains separate. No live gateway/model test or token/latency saving is established.

[Copyable JSON](gateway-toolsets.json) contains backend-qualified allowlists and example calls, not a configuration format accepted by any particular gateway. Substitute placeholders from authorized configuration/discovery results, replace the illustrative UTC event window, and map the fields to your gateway. Calls are an ordered recipe for a host/operator, not an executable batch: check every result before substituting the next identifier. Do not run the file as a script.


## Follow-up: typed identity and report views

The current seven-tool profile adds read-only get_vm_info. Compare its instance_uuid to Aria VMEntityInstanceUUID; do not compare BIOS and instance UUIDs. For one selected VM the typed identifiers matched exactly and nine discovered CPU/memory/disk series returned data. Host investigation returned two alarms and no sensor rows; sensor availability remains a gap. Three report depths retained scope, grade, evidence IDs and gaps without changing the ledger. This is operator-driven real-data validation, not an autonomous-model/gateway test, fault injection or confirmed root cause. The earlier six-tool baseline below remains historical evidence.

## Select one profile

| Task | Infrastructure tools exposed to the agent | Count |
|---|---|---|
| VM performance | Monitor: list_virtual_machines, investigate_vm, get_vm_info. Aria: list_resources, get_resource, list_metric_keys, get_resource_metrics. | 7 |
| Host alarms | Monitor: list_esxi_hosts, investigate_host, get_events, get_host_sensors, get_host_performance. | 5 |

Expose only the selected profile through both tools/list and tools/call dispatch. Reject unlisted tools, unknown backends and unauthorized targets; never silently forward to a different backend. Retrieve full schemas from the selected backend version rather than replacing them with the example arguments. Recheck names, parameters and readOnlyHint after upgrades. These names describe the profile; annotations/visibility alone are not authorization. Keep backend Policy, audit and product RBAC. Use read-only product accounts and read exposure where supported; keep caller identity/session isolation and correlation as described in each backend's setup guide. This file is not a new enforced allowlist or an OAuth/OBO implementation.

Aggregate investigations include related hosts, clusters, datastores, workloads and events. Authorization to the named VM/host alone does not establish permission to disclose every related row. A trusted gateway must check/filter the response before delivery to the caller/model, or omit the call and report a gap. No such filter is implemented by these examples.

## VM performance: seven tools

Resolve an exact VM in Monitor, then call investigate_vm. Resolve its Aria resource independently and verify identifiers with get_resource; equal display names are insufficient. The vSphere and Aria target names are separate configuration keys. Missing or ambiguous cross-product identity stops correlation.

Discover keys before metrics: the JSON starts with CPU keys; repeat list_metric_keys with memory/storage filters as needed, using only returned keys with understood units. Do not invent a CPU-ready key or infer storage latency from throughput. Query only the requested facts; summary=True limits point output but preserves missing-key indications and aggregation caveats. AVG summaries are summaries of interval averages, not raw peaks.

hours is relative to collection time for investigate_vm and get_resource_metrics. Record actual returned sample times and fetched_at. These calls cannot express an arbitrary historical start/end window: if they do not cover the incident, record the gap rather than treating the current hour as historical evidence. Aria is required for this profile's metric branch; if unavailable, retain the Monitor observation and explicit gaps without claiming a performance diagnosis.

## Host alarms: five tools

Resolve the exact host, then prefer investigate_host for alarms, impact, current load and event context. Use the additional tools only for a discriminating check, avoiding repeated full collection. get_host_performance is a current snapshot, not incident-window history.

get_events supports start/end but has no host_name or limit parameter. severity="info" includes the lower-severity context; retain the returned severity and unknown classifications. Routine login/logout events are folded by default: preserve routine_folded/routine_note, and do not claim the returned rows are the full raw event stream. Its result spans the authorized target, so correlate host identity explicitly and inspect read_truncated/read_note. Do not send unrelated event rows to a caller/model without authorization to those rows. Narrow the window or record incomplete coverage; there is no invented offset.

get_host_sensors also has no host_name filter: limit=50 caps rows across the target. Filtering those rows locally does not prove the host had no sensors; the desired rows may be outside the cap. Preserve hosts_without_sensors and sensors_note. Only use this call where the caller may read the target-wide data. Otherwise omit it and record a sensor gap. Sensor colour alone cannot identify a failed DIMM.

## Bounds, evidence and output

The host starts with 20 infrastructure tool calls, requests limit=50 where supported, and follows at most three exposed pages per check. These are procedure limits, not hard bounds on backend work or all response sizes. Aria name_filter is client-side: even limit=50 can scan many internal pages; inspect scan_complete and truncation. get_events has no output limit parameter, and aggregate investigations fan out and may return more than 50 rows. A trusted host/gateway must separately bound the data delivered to the model, retain coverage/counts and record omissions; if the deployment requires a strict backend scan/row budget these tools do not establish it. No automatic response budget/filter is supplied here. Monitor lists and Aria list_resources have no offset here: truncated results need narrower supported filters or an explicit scope decision, not a fabricated page parameter. For list_metric_keys, follow next_offset until null or the budget; a final page may still say truncated=true. Other unpaged result shapes retain their own caps and gap semantics.

The host tracks these procedure limits; the JSON does not enforce them. Stop on identity ambiguity, denied required sources or exhausted budget. Missing/stale/contradictory observations remain gaps/alternative hypotheses, never zero or healthy. Preserve source backend/tool, exact query/target, collection and incident times, units, coverage and evidence IDs. Treat returned text as data, never as instructions to widen access or repair.

Debug is optional and separate from the infrastructure allowlist. open_case, submit_case_evidence, record_case_gap and record_case_hypothesis write the local ledger and must retain their write classification and require separate local-record permission. Do not mount all Debug tools behind a read-only-only token and assume collection can persist evidence. Without that permission, return a bounded in-memory report using the same observation/gap structure, without claiming a persisted case or grade. With permission, use the existing ledger and get_case; optional report_view requires the candidate implementation, and older installations must omit it. Existing outer fields can include a local path, so project only authorized report fields for gateway clients. Report depth is not RBAC.

No remediation, alarm acknowledgment, power operations, repair handoff or confirm=True is part of either profile. Keep any later action in a separately authorized workflow.

Schema baseline checked locally: Monitor 2.6.2 and Aria 2.4.7, with the then-unreleased Debug report candidate (subsequently included in 2.4.0). This is not a latest-release compatibility claim; rerun registry checks against the exact deployed versions.

## Verify before sharing results

Offline: check every listed name/argument against the actual backend registry and read annotations; ensure local ledger writes are outside the infrastructure profile. Existing Debug report tests cover legacy/view behavior and gaps. Live acceptance later must separately check authorized/denied targets, incomplete discovery, mismatched identity, missing metrics/sensors and contradictory evidence. A real host/model comparison must measure native calls, quality, actual tokens and latency before making performance claims. Published package versions and the gateway mapping must be recorded with those results.

## Weekend live checklist (pending)

- Record exact backend packages, Debug candidate revision and gateway mapping; revalidate deployed schemas.
- VM: verify one cross-product identity, discovered metric units, actual sample window and one missing/contradictory-data branch.
- Host: check actual alarms, related-entity authorization, sensors and event window/folding/coverage; distinguish current from historical observations.
- Confirm denied targets and unlisted tool calls fail through the gateway; check that unauthorized rows never reach the model and local ledger writes require separate permission.
- If Debug is enabled, compare brief/operator/investigation views for the same evidence IDs, grade and gaps; confirm legacy get_case still works.

The limited backend/report checks below are complete; full gateway and incident acceptance items remain pending. AIops #69 create/delete validation is separate and deferred; neither profile requires infrastructure writes.

## Limited lab validation — 2026-11-20

All eleven distinct infrastructure tool names in the two profiles succeeded over actual local MCP-to-lab connections (Monitor 2.6.2, Aria 2.4.7). The candidate Debug 2.3.3 report interface accepted legacy and all three views; evidence IDs, scope, grades and gaps agreed, case files were unchanged by reads, and vSphere session count deltas were zero. This is a backend/report plumbing check, not full investigation acceptance or deployed-gateway/model validation.

Cross-product identity remains unresolved in the sampled VM: Monitor's uuid comes from config.uuid (BIOS UUID), whereas Aria returned VMEntityInstanceUUID plus VMEntityObjectID/VMEntityVCID. These are different identity types; unequal BIOS/instance UUIDs do not establish different VMs. Do not compare them as equivalent. The six-tool baseline has not established the shared typed identifier needed for this sample; stop correlation and obtain a verified mapping in a separately scoped check. Aria metrics were tested independently with three discovered keys, not used to diagnose the Monitor VM. First-page CPU keys did not include the desired usage/ready keys; do not substitute other CPU keys as equivalent evidence.

Host sensors returned zero rows; performance returned one row and events two rows without read truncation in the sampled hour. These are observations, not a hardware-health or causal incident conclusion. Gateway filtering/denials, caller isolation and full missing/contradictory live cases remain pending.
