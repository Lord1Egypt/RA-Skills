# Ops Playbooks — Troubleshooting Paths with vmware-aria

Each path below uses only commands this skill ships, in the order an operator would run them. Every read step was run against a live Aria Operations 8.18.7 appliance (2026-09-13); the examples quote what came back. The write steps — `alert note-add`, `alert acknowledge`, `maintenance start` and `maintenance end` — were not sent to it: they were run only with `--dry-run` or not at all, so what they return is described from the code and its tests, not observed. MCP tool names are in brackets where they differ from the command.

Quote any argument that contains `|` (`'cpu|readyPct'`) — a shell reads a bare `|` as a pipe.

For a root cause (not just a symptom), finish with [`investigation-protocol.md`](investigation-protocol.md).

---

## 1. Aria Operations itself reports DEGRADED or OFFLINE

**Question**: is the platform down, or is one service out while data still flows?

1. Assessment and the failed service → `vmware-aria health status` [`get_aria_health`]
   - `DEGRADED` = some services OK, some ERROR — not an outage. `DOWN` = no service OK. The node flag reads OFFLINE (HTTP 503) whenever any one service is not running, so OFFLINE alone proves nothing.
   - The version line tells you 8.x or 9.x; fleet, findings and PromQL only exist on 9.0+.
2. Is the node starved? → `vmware-aria health node --hours 24` [`get_aria_node_resources`]
   - `Memory pressure` is HIGH below 10% actual free, ELEVATED below 20%. Also read swap used, heap per component, and watchdog restarts per service.
   - Restarts of 0 with a service still failing means it is not crash-looping — it is stuck or misconfigured.
3. Is collection still working? → `vmware-aria health adapters` [`list_adapters`]
   - `Stale: yes` means the adapter's last collection is older than 3 intervals (at least 15 minutes).
4. Service-specific follow-up happens on the appliance (console or SSH), not through the API.

**Example**: `LOCATOR ERROR`, everything else OK → DEGRADED. `health node` showed 7.61 of 7.75 GB used and swap in use, so the VM was resized to 16 GB. Afterwards `health node` read 15.61 GB total, 41% actually free, pressure NORMAL, all watchdog restarts 0 — and LOCATOR was **still** in ERROR. Memory pressure was real but not the cause. The locator was in fact running (port 6061 listening, reachable by IP and by hostname, `locators=` matching the node IP, no "Could not contact any of the locators" in `analytics-*.log`), so the IP-change failure in Broadcom KB 404805 did not apply. What failed was the status check itself: `/storage/vcops/log/api.log` logged `GemfireLocatorStatusCheckVerifier` with `javax.net.ssl.SSLHandshakeException: No subject alternative DNS name matching aria-ops-01 found`. The check connects to the locator's JMX manager (port 1099, TLS 1.3 with client authentication) by the node's hostname, and the appliance certificate (`CN=vROps-slice-1`) lists only `localhost`, `127.0.0.1` and the node IP as Subject Alternative Names — so the handshake fails and the API sets the node OFFLINE while collection carries on. Check a node the same way: `grep -h -A1 "nested exception is:" /storage/vcops/log/api.log | sort | uniq -c`, then compare the certificate's SANs (`openssl s_client -connect 127.0.0.1:1099 </dev/null | openssl x509 -noout -ext subjectAltName`) with `hostname`. GemFire KB 439258 describes this handshake failure and its options (advertise a name that is on the certificate with `jmx-manager-hostname-for-clients`, or reissue the certificate); both change the appliance's configuration.

## 2. Triage a critical alert

**Question**: what is affected, why, and what does VMware recommend?

1. Open alerts → `vmware-aria alert list --criticality CRITICAL` [`list_alerts`] — rows carry the affected resource's name and ID (the MCP tool also returns its `resource_kind`; the CLI table has no kind column)
2. Symptoms → `vmware-aria alert get <alert-id>` [`get_alert`] — each symptom is named from its definition, with severity
3. Recommended actions → `vmware-aria alert recommendations <alert-id>` [`get_alert_recommendations`]
   - `status: found` lists them by priority; `none_defined` means the definition has none; `unknown` means they could not be read — not the same thing
4. The affected object → `vmware-aria resource get <resource-id>` [`get_resource`] (MCP [`investigate_alert`] does steps 2 and 4 in one call and labels the two UUIDs)
5. Where it sits → `vmware-aria resource relationships <resource-id> --type PARENT` [`get_resource_relationships`]
6. Record who is on it → `vmware-aria alert notes <alert-id>` [`list_alert_notes`], then `vmware-aria alert note-add <alert-id> "Investigating: …" --dry-run`, and again without `--dry-run` [`add_alert_note`, write]
7. When handled → `vmware-aria alert acknowledge <alert-id>` [`acknowledge_alert`, write]

**Example**: "vCenter app health is affected" (CRITICAL) — symptom "vCenter appliance health service is down" (CRITICAL); resource `vCenter-192.168.60.16`, kind `VC_APP`, health 25 (RED); parents "vCenter Health" and adapter instance "new VC"; 7 recommendations, priority 1 "Please check the Health Status of app"; no notes yet.

## 3. A VM is slow — find contention, not just consumption

1. Candidates → `vmware-aria resource top --metric 'cpu|usage_average' --top 10` [`get_top_consumers`]
   - `value` is the last-hour average Aria ranks by; resources with no data are left out, not ranked at zero
2. Contention on a candidate → `vmware-aria resource metrics <vm-id> --metrics 'cpu|readyPct,mem|balloonPct,mem|swapped_average' --hours 24` [`get_resource_metrics`]
   - CPU Ready >5% warning, >10% problem; balloon >0 = ESXi reclaiming memory; swapped >0 = severe
3. A busy VM with low Ready is healthy; a quiet VM with high Ready is starving. Confirm with the host's view before blaming the VM.

## 4. A metric comes back empty

1. Ask → `vmware-aria resource metrics <id> --metrics '<key>' --hours 1`
2. Read `missing[].reason` — never report it as zero:
   - `not_collected_for_resource` — this resource never reports the key; `similar_keys` lists keys from the same group
   - `no_data_in_window` — reported before, nothing in this window: widen `--hours`, then check `health adapters`
   - `undetermined` — the key list could not be read
3. Find the right key → `vmware-aria resource keys <id> --filter 'cpu|demand'` [`list_metric_keys`] — name and unit come from the kind's definitions

**Example**: `cpu|demand_average` → `not_collected_for_resource` on a VM. `resource keys --filter 'cpu|demand'` returns `cpu|demandPct` (CPU|Demand, %) and `cpu|demandmhz` (CPU|Demand, MHz).

## 5. Before resizing a VM

1. Candidates → `vmware-aria capacity rightsizing --limit 20` [`list_rightsizing_recommendations`]
   - Act only where `Act.` is yes; read every caveat under the table
   - A yellow `properties_note` means the property read failed — power state and current size are unknown, so nothing is actionable
2. Current facts → `vmware-aria resource properties <vm-id> --name powerState` and `--name hotadd` [`get_resource_properties`]
   - `config|extraConfig|mem_hotadd: false` means the change needs a power-off window
3. Check the vendor's minimum size before any reduction — appliances cannot be identified reliably from the API.
4. Make the change with vmware-aiops (this skill does not change VMs); wrap the window in maintenance (path 6).
5. Afterwards, re-read `capacity rightsizing` only once the analysis window reflects the new size.

**Example**: the Aria appliance VM had just been resized from 8 GB to 16 GB after memory pressure. The next `capacity rightsizing` still recommended 16.0 → 9.0 GiB with `Act.` yes — the engine's window was mostly pre-change data, and the VM is a vendor appliance. Following it would have undone the fix.

## 6. Planned maintenance on a monitored object

1. Existing windows → `vmware-aria maintenance schedules` [`list_maintenance_schedules`]
2. Preview → `vmware-aria maintenance start <resource-id> --duration 60 --dry-run` — prints `PUT /suite-api/api/resources/<id>/maintained?duration=60` without connecting
3. Start → the same without `--dry-run` [`start_resource_maintenance`, write, medium] — omit `--duration` and `--end` for indefinite maintenance
4. Do the work (for VM changes, vmware-aiops)
5. End → `vmware-aria maintenance end <resource-id>` [`end_resource_maintenance`, write, medium] — refused only when the resource is known not to be in maintenance; when its state is unknown (unreadable, or an adapter reports `UNKNOWN` / `NONE`) it proceeds

Both write commands confirm once (`--yes` skips) and are audited to `~/.vmware/audit.db`.
