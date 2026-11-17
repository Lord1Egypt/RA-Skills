# Capabilities

## Automation Level Reference

Each operation is classified by autonomy level per the Enterprise Harness Engineering framework. **vmware-aria is heavily L1/L2 (36 read / 10 write)** — primarily a monitoring and analysis skill.

| Level | Meaning | Agent autonomy | Examples in this skill |
|:-:|---|---|---|
| **L1** | Read-only, raw data | Always auto-run | `list_resources`, `get_resource`, `get_resource_metrics`, `list_metric_keys`, `get_resource_properties`, `get_resource_relationships`, `list_alerts`, `get_alert`, `list_alert_definitions`, `list_alert_notes`, `list_maintenance_schedules`, `get_aria_node_resources`, `list_adapters`, `search_api_operations`, `get_api_path`, capacity / badge queries |
| **L2** | Read + analysis / recommendation | Always auto-run | `investigate_alert` (alert → confirmed affected resource), `get_alert_recommendations` (alert → definition state → prioritized recommendations), anomaly counts, top-N consumer ranking, capacity trend forecasting, rightsizing recommendations |
| **L3** | Single write — user must approve | Only after explicit confirmation | `acknowledge_alert` (via takeownership action), `cancel_alert`, `create_alert_definition`, `set_alert_definition_state`, `delete_alert_definition`, `generate_report`, `delete_report`, `start_resource_maintenance`, `end_resource_maintenance`, `add_alert_note` *(the only writes; all auditable. On MCP, `acknowledge_alert`, `cancel_alert`, `delete_alert_definition`, `delete_report`, `start_resource_maintenance` and `end_resource_maintenance` take `confirm` (default false): without `confirm=true` they return a `blast_radius` — what the call would change — and change nothing; `confirm=true` is refused when a blocker is found or a field the radius depends on could not be read. The old `confirmed` alias was removed in 2.4.2; a call that passes it is refused as an unknown argument. `add_alert_note` is low risk and has no gate — a note changes neither the alert nor monitoring; the CLI still asks once)* |
| **L4** | Multi-step plan / apply workflow | *N/A currently* | — *(no multi-step orchestration; Aria is observe/analyze, not configure)* |
| **L5** | Auto-remediation from learned pattern | Pattern library only; requires `risk:low` + `reversible:true` + `repeatable:true` | *(roadmap — candidates: auto-acknowledge known-noisy alerts, auto-cancel resolved-by-event alerts)* |

**Notes**:
- L1/L2 tools are always safe for agents to call without confirmation.
- L3 alert-state writes pass through the `@vmware_tool` decorator: connection check → policy check → audit log. Cancel is irreversible by Aria API design and treated as a destructive operation.
- For VM/host operations see [vmware-aiops](https://github.com/vmware-skills/VMware-AIops); Aria recommendations are advisory, not actuating.

## What vmware-aria Can Do

### Resource Monitoring

- **List any resource type**: VirtualMachine, HostSystem, ClusterComputeResource, Datastore, Datacenter, ResourcePool
- **Filter by name**: substring match across any resource list
- **Find objects that stopped reporting**: every row carries `aria_state` (Aria's lifecycle state — `STARTED` for a powered-off VM too) and `collection_status` (`DATA_RECEIVING`, `NO_DATA_RECEIVING`, …; null when not reported). `collection_status="NO_DATA_RECEIVING"` with `resource_kind="all"` lists the objects behind "Objects are not receiving data from adapter instance"; a filter that matches nothing returns a `note` naming the statuses seen
- **Get resource details**: health, risk, and efficiency badges plus all identifiers
- **Fetch metric time series**: any metric key with configurable time window, rollup (AVG, MAX, MIN, SUM, COUNT, LATEST) and resolution (`interval_type` MINUTES/HOURS/DAYS/WEEKS/MONTHS × `interval_quantity`; default one point per 5 minutes, so a month at DAYS/1 is about 30 points per key instead of about 8,600). `interval` in the result gives the resolution requested and, in `applied`, what Aria reports it used, with a `note` when they differ. With AVG the summary `max` is the highest average, not the peak: use MAX for peaks. Keys with no points are listed under `missing` with a reason (`not_collected_for_resource` with `similar_keys`, `no_data_in_window`, `resource_reports_no_stat_keys`, `undetermined` — also when stat-key rows are in an unrecognised form) instead of silently vanishing. `similar_keys` holds at most 10 keys, only ones `sanitize()` leaves unchanged and at most 200 characters long
- **Look up metric keys**: `list_metric_keys` lists the keys one resource actually reports, joined with its kind's definitions for name and unit. Each row's `definition` is `found`, `found_by_instance` (an instanced key such as `guestfilesystem:/boot|usage` joined to `guestfilesystem|usage`), `not_defined_for_kind` (also listed in `unjoined_keys`) or `not_read` (the definitions could not be read: `definitions_status: undetermined`, name and unit unknown, not absent). With `resource_kind` instead, it lists the keys the kind defines — a defined key is not collected on every resource. A nonexistent resource id is an HTTP 404 error, not an empty list
- **Read properties**: `get_resource_properties` — current `{name, value}` rows sorted by name (power state, `summary|parentHost`, configured CPU and memory, `config|extraConfig|*` flags), filtered by a name substring. Configuration facts, not time series
- **Walk relationships**: `get_resource_relationships` — related resources with `id`, `name`, `kind`, `adapter_kind` and `direction` (`parent` / `child` / `both` / `other`). `relationship_type` is exactly ALL, PARENT or CHILD; ANCESTOR and DESCENDANT are refused (Aria Operations 8.18.7 answers HTTP 400 for them), so walk PARENT one level at a time. With ALL, `direction` is null and `direction_note` says why when the PARENT/CHILD lists could not be read
- **Find top consumers**: rank VMs or hosts by a metric's last-hour average (`value`, 5-minute AVG rollup — what Aria ranks by, descending; `latest_value` is the most recent point). Resources with no data for the key are left out, not ranked at zero; `excluded_no_data` counts the ones the ranking listed with no points, and `hint` says when that shortened the list — when they took slots of a full `top_n`, the result is `truncated` and `hint` says to raise `top_n`

### Alert Management

- **List active or all alerts**: filter by criticality (INFORMATION/WARNING/IMMEDIATE/CRITICAL) or resource. The Alert model has no resource name, so each row's `resource_name` and `resource_kind` are resolved in one batched `/resources` lookup per page; `null` means unknown, and `resource_names_note` says how many could not be retrieved (a failed lookup, or an appliance that ignored the id filter), were not returned, or have no name in Aria Operations
- **Inspect alert details**: contributing (triggered) symptoms from the dedicated contributingsymptoms endpoint, plus timeline. A symptom that carries no name or severity (every symptom on Aria Operations 8.18.7) takes both from its symptom definition, fetched in one batched `/symptomdefinitions` lookup; `definition_lookup` and `symptom_definitions_note` say when that did not work, including symptoms with no definition id to look up. Each symptom also carries the object it is on (`resource_id`, `resource_name`, `resource_kind`, `stat_key`, and `condition` from the instance message): on 8.18.7 the contributing-symptom payload has no resource id, so it is read from the symptom instance in `/symptoms` — which ignores its `id` filter there, so the tool walks it and keys rows by id. That is what names the down services behind "vCenter app health is affected" (e.g. `mem`, `system`). On 8.18.7 the walk runs for every alert, not only vCenter app alerts: one request per 1,000 symptoms in the appliance (capped at 20,000 symptoms), stopping once all are found, plus one batched `/resources` lookup; `acknowledge_alert` / `cancel_alert` skip it for their before-state. `resource_lookup` and `symptom_resources_note` say when an object could not be read — an empty `resource_id` is then unknown, not absent. Times come as epoch ms and ISO-8601 UTC (`*_time_utc`). Recommendations are attached to the alert definition, not the alert
- **Investigate an alert end-to-end**: `investigate_alert` resolves an alert to its affected resource in one call — fetches the alert, reads `resourceId`, fetches that resource, confirms name and kind, and returns both UUIDs *explicitly labelled* plus a ready-to-use handoff naming the exact vmware-monitor tool and argument. Use it instead of chaining `get_alert` → `get_resource` by hand: the two UUIDs are different objects and a small model will otherwise swap them. An unresolvable resource degrades to a warning plus explicit nulls rather than losing the alert
- **Acknowledge alerts**: mark as seen without closing (control state → ACKNOWLEDGED)
- **Alert notes**: `list_alert_notes` returns an alert's notes (`note`, `type` USER / SYSTEM, `user_name`, `created_time_ms`); an unknown alert id is HTTP 404, and a set `notes_note` means the notes are unknown, not absent. `add_alert_note` records who is handling the alert or what was done — it does not change status or ownership (use `acknowledge_alert`), is not idempotent (two calls add two notes) and has no undo. `created: null` with `confirmation_note` means Aria did not confirm the note: run `list_alert_notes` before retrying
- **Alert recommendations**: `get_alert_recommendations` resolves the alert to its alert definition, uses the state whose severity matches the alert's criticality (else the definition's only state, else every state merged at each recommendation's highest priority, with a `note`), and returns the recommendations sorted by priority (lower is more important) with description and action. `status`: `found`; `partial` (some text could not be read — `description: null` is unknown, not blank); `none_defined` (`recommendations: []`); `unknown` (the definition could not be read — `recommendations: null`, never "no recommendations"). On Aria Operations 8.18.7 a CRITICAL vCenter-app alert returned 7 prioritized recommendations
- **Cancel alerts**: permanently dismiss (status → CANCELLED)
- **Browse alert definitions**: the templates that define when alerts fire

### Capacity Planning

- **Cluster capacity overview**: group-level remaining-capacity percentage plus per-dimension (cpu/mem/diskspace) headroom and days-until-full (the percentage metric only exists at group level)
- **Remaining capacity**: how much more CPU, memory, disk can be added before hitting limits
- **Time remaining**: predicted days until each capacity dimension is exhausted (based on trend)
- **Rightsizing recommendations**: identify over-provisioned VMs (reclaim resources) and under-provisioned VMs (prevent degradation). Raw recommendations are MHz / KB / GB (`recommended_units`); `recommended_vcpus` converts CPU with the VM's own MHz per vCPU. `cpu_direction` / `memory_direction` compare against the current configuration (memory within 1% is `right_sized`). Powered-off VMs and templates are listed but never `actionable`, nor is a VM whose power state or template flag is unknown. If the VM property read fails, the property-derived fields are null, no row is actionable, and `properties_note` names the failure. `caveats` flag engine disagreement and vendor minimum sizes before any reduction. `recommendation_range` gives the daily low and high of each recommendation over the last 7 days with `days_with_data`; a CPU or memory range wider than 5% of its high makes `recommendation_stable` false and the row not actionable. Null when no history came back; `history_note` names a failed history read

### Resource Maintenance

- **Start maintenance**: `start_resource_maintenance` stops Aria alerting on one resource and collecting its data. With `duration_minutes` (1–525600) or `end_time_ms` (epoch milliseconds, in the future) the resource is `MAINTAINED` for that window and returns to its prior state when it expires; pass one, not both. With neither it is `MAINTAINED_MANUAL` until ended. Returns `requested`, `before` / `after` state, `confirmed` (true / false / null — null means the after-state could not be read, which is unknown, not failure) and `note`. On MCP a call without `confirm=true` reads the resource and returns `blast_radius` (name, kind, adapter states, whether it is in maintenance, the requested window) without changing anything; `confirm=true` is refused when the resource is already in maintenance (starting again would replace that window) or its state is unknown. An impossible window is refused before connecting. Risk medium; audited with the before and after state; undo is `end_resource_maintenance`, recorded only when the resource was known not to be in maintenance before (so an undo never closes a window this call did not open)
- **End maintenance**: `end_resource_maintenance` refuses a resource known not to be in maintenance (an adapter reports a state such as `STARTED` or `STOPPED`). When the state is unknown — it cannot be read, or an adapter reports `UNKNOWN` / `NONE` — the MCP tool refuses too (its blast radius cannot be measured); the CLI proceeds and `before` says unknown. Without `confirm=true` the MCP tool returns the `blast_radius` and changes nothing. Risk medium, audited. Its undo, recorded only when the resource was known to be in maintenance, re-enters manual maintenance — the end of a timed window is not restored
- **Maintenance schedules**: `list_maintenance_schedules` — name, schedule type (ONCE / DAILY / WEEKLY / MONTHLY / YEARLY), recurrence, start hour and minute, duration in minutes, time zone, start and expiry. A schedule does not list its resources; pass `resource_id` for the schedules of one resource. A set `schedules_note` means the schedules are unknown, not absent

### Anomaly Detection

- **List anomalies**: per-resource Total Anomalies counts (`System Attributes|total_alarms` metric — active symptoms, events, and DT violations on the object and its children), optionally scoped to one resource. The UI's anomalous-metrics list is not part of the public API
- **Risk badge**: composite risk score (0–100) from the resource's `badges[]` array — predicts likelihood of future problems; for contributing causes inspect the resource's active alerts

### Platform Health

- **Aria health check**: `assessment` HEALTHY / DEGRADED / DOWN / UNKNOWN from the node status plus the per-service breakdown, and the product version and line (8.x / 9.x). The node reports OFFLINE whenever any one service is not running, so OFFLINE with some services OK is DEGRADED, not down. An ONLINE node whose per-service breakdown could not be read is HEALTHY with `details` saying no service was checked individually; a service in a state other than OK or ERROR makes it UNKNOWN unless DEGRADED. An unreadable version or service list is reported (`version_error` / `services_error`), not raised
- **Collector group status**: list collector groups (member IDs) enriched with each collector's name, UP/DOWN state, and local flag
- **Aria node resources**: `get_aria_node_resources` reads Aria's own self-monitoring objects (`vC-Ops-Node`, `vC-Ops-Watchdog`): per node memory (`mem|total`, `mem|used`, `mem|free`, `mem|actualFree`, `mem|actualUsed`), swap, heap overall and per component, and watchdog restarts per service. Each value has `latest`, `unit` (from Aria's statkey definitions, never assumed) and `window` min / avg / max / points over `window_hours` (1–720, default 24) of 5-minute averages. `memory_pressure.level` is an indicator: HIGH when actual free memory is below 10% of total, ELEVATED below 20%, NORMAL at 20% or more, UNKNOWN when the readings do not settle it. A key with no value is in the node's `missing` list (`not_reported` / `no_data` / `undetermined`), never zeroed; `watchdog_restarts: null` is unknown, not zero. On Aria Operations 8.18.7 after a memory upgrade the node read `mem|total` 15.61 GB (was 7.75), actual free 41%, pressure NORMAL, and 9 watchdog services with 0 restarts
- **Adapter collection state**: `list_adapters` — each adapter instance's kind, collector, monitoring interval, resources and metrics collected, last collected and last heartbeat with ages in seconds, its own message, and `stale`: true when the last collection is older than max(3 × monitoring interval, 15 minutes), false within that, null when the fields cannot support a verdict (`stale_basis` shows the arithmetic). Ages use the appliance clock from node status when it is available (`reference_clock`). An empty or unrecognised answer is an error, never "no adapters". A recent collection does not prove every object behind the adapter receives data. On Aria Operations 8.18.7 all 6 adapters were not stale

### Raw API (read-only escape hatch)

For a read no tool above covers (HLD §17 D-18). Prefer the dedicated tools: their results are shaped, paginated and explained.

- **`search_api_operations(query, limit=20)`**: searches the suite-api operation index shipped in the package (`vmware_aria/api_spec/`: vROps 8.6, 315 operations; VCF Operations 9.1, 504 operations plus the verified fleet subset). Every word must appear in method, path or summary; path matches rank first, then GET. Each row: `method`, `path` template, `summary`, `indexes` (`8.6` / `9.1`) and `callable_with_get_api_path` (true only for GET). `limit` 1–100. Contacts no appliance. Typical response: ~1,500 tokens at the default limit
- **`get_api_path(path, params=None, target=None)`**: one `GET` through the target's client (its token, retry and error translation). `path` must match a GET operation of the index with every `{name}` replaced by one segment (letters, digits, space, `- . _ ~ : @ + , =`). Refused before any request: other methods, unindexed paths, `..` / `.` / `//`, `?` or `#` in `path` (use `params`), URLs, percent-encoding, non-string `params`. A 9.x appliance (read from `/versions/current`) is held to the 9.1 index; on 8.x, or when the version cannot be read, a path in either index is accepted — the 8.6 index is the only 8.x specification held and 8.18 answers paths it lacks; a path the appliance does not have returns a 404 error. Every string in the answer is sanitized (control/format characters stripped, cut to 500 characters). Answers over 30,000 characters of JSON (about 8k tokens — one resource or one page of a list fits; an unpaged list, 1,000 rows by default, does not) return `truncated: true`, `original_size` and `body_text` (cut, not valid JSON): page with `params` such as `pageSize`. Audited like every call. The account's Aria roles still decide what it can read. Typical response: 500–8,000 tokens

---

## What vmware-aria Cannot Do

| Capability | Use Instead |
|-----------|-------------|
| Create / delete / power VMs | `vmware-aiops` |
| Configure NSX segments, gateways, NAT | `vmware-nsx` |
| NSX DFW / firewall rules | `vmware-nsx-security` |
| vSphere inventory (VMs, hosts, clusters) read-only | `vmware-monitor` |
| Storage: iSCSI, vSAN, datastores | `vmware-storage` |
| Tanzu Kubernetes cluster management | `vmware-vks` |
| Create alert definitions | Supported via `create_alert_definition` (from symptom definition IDs) |
| Configure dashboards | Not supported (UI required) |
| Manage Aria adapter instances | Not supported (UI required); `list_adapters` reads their collection state |

---

## Aria Operations API Coverage

All requests carry `Authorization: vRealizeOpsToken <token>`.

| Endpoint | Used For |
|----------|---------|
| `POST /suite-api/api/auth/token/acquire` | Token authentication |
| `POST /suite-api/api/auth/token/release` | Token release on close (no body; token identified by the Authorization header) |
| `GET /suite-api/api/resources` | list_resources (also candidate listing for topn / anomaly / rightsizing scans); list_alerts and get_alert symptom resource names (`resourceId` repeated, 100 per request); get_aria_node_resources (self-monitoring `vC-Ops-Node` / `vC-Ops-Watchdog` objects) |
| `GET /suite-api/api/resources/{id}` | get_resource, get_resource_health, get_resource_riskbadge (badges come from the `badges[]` array — there are no `/badge/*` endpoints), investigate_alert (resource-side leg), list_metric_keys (the resource's adapter and resource kind), start_resource_maintenance / end_resource_maintenance (blast radius, and state before and after, from `resourceStatusStates`), acknowledge_alert / cancel_alert (the alert's resource name, context only) |
| `POST /suite-api/api/resources/{id}/stats/query` | get_resource_metrics |
| `GET /suite-api/api/resources/{id}/statkeys` | get_resource_metrics (only when a requested key returned no points, to explain why); list_metric_keys (the keys a resource reports); get_aria_node_resources (the keys each node reports) |
| `GET /suite-api/api/adapterkinds/{adapterKind}/resourcekinds/{resourceKind}/statkeys` | list_metric_keys (key names and units); get_aria_node_resources (units for the self-monitoring kinds) |
| `GET /suite-api/api/resources/{id}/properties` | get_resource_properties; get_resource_health (`SERVICE\|STATUS`, service-kind objects only) |
| `GET /suite-api/api/resources/{id}/relationships` + `/relationships/{PARENT\|CHILD}` | get_resource_relationships (paged walk; with ALL the PARENT and CHILD lists label `direction`) |
| `GET /suite-api/api/resources/stats/latest` | get_aria_node_resources (latest values) |
| `POST /suite-api/api/resources/properties/latest/query` | list_rightsizing_recommendations (current vCPUs, memory, CPU speed, power state, template flag, product name) |
| `GET /suite-api/api/resources/stats/topn` | get_top_consumers (resourceId list capped at 100) |
| `GET /suite-api/api/resources/{id}/stats/latest` | get_capacity_overview, get_remaining_capacity, get_time_remaining (OnlineCapacityAnalytics keys) |
| `POST /suite-api/api/resources/stats/query` | list_rightsizing_recommendations (OnlineCapacityAnalytics recommendedSize keys), list_anomalies (`System Attributes\|total_alarms`) — one request for a resourceId array; get_aria_node_resources (window min / avg / max); get_resource_health (latest `SERVICE\|AVAILABILITY`, service-kind objects only) |
| `PUT /suite-api/api/resources/{id}/maintained` | start_resource_maintenance (window as the `duration` or `end` query parameter; neither = manual maintenance) |
| `DELETE /suite-api/api/resources/{id}/maintained` | end_resource_maintenance |
| `GET /suite-api/api/maintenanceschedules` | list_maintenance_schedules (paged; `resourceId` filter) |
| `POST /suite-api/api/alerts/query` | list_alerts (server-side status/criticality/resource filtering) |
| `GET /suite-api/api/alerts/{id}` | get_alert, investigate_alert (alert-side leg; no dedicated endpoint — the tool composes the two existing reads), get_alert_recommendations (the alert's definition id and criticality), acknowledge_alert / cancel_alert (blast radius) |
| `GET /suite-api/api/alerts/{id}/notes` | list_alert_notes (paged) |
| `POST /suite-api/api/alerts/{id}/notes` | add_alert_note (body `{"content": …}`) |
| `GET /suite-api/api/alertdefinitions/{id}` | get_alert_recommendations (states and their recommendation priorities), delete_alert_definition (blast radius) |
| `GET /suite-api/api/recommendations` | get_alert_recommendations (recommendation text; `id` repeated, 50 per request) |
| `GET /suite-api/api/alerts/contributingsymptoms?id={alertId}` | get_alert (triggered symptoms) |
| `GET /suite-api/api/symptoms` | get_alert / investigate_alert (the object each symptom is on — `resourceId`, `statKey`, `message` — when the contributing-symptom leaf carries none; 8.18.7 ignores the `id` filter, so pages are walked until every symptom is found or `pageInfo.totalCount` is reached — up to 20 requests; not used by acknowledge_alert / cancel_alert) |
| `POST /suite-api/api/alerts?action=takeownership` | acknowledge_alert |
| `POST /suite-api/api/alerts?action=cancel` | cancel_alert |
| `GET /suite-api/api/alertdefinitions` | list_alert_definitions |
| `POST /suite-api/api/alertdefinitions` | create_alert_definition |
| `PUT /suite-api/api/alertdefinitions/{id}/enable` (or `/disable`) | set_alert_definition_state |
| `DELETE /suite-api/api/alertdefinitions/{id}` | delete_alert_definition |
| `GET /suite-api/api/symptomdefinitions` | list_symptom_definitions (filter param is `resourceKind`); get_alert / investigate_alert symptom names and severities (`id` repeated, 50 per request) |
| `GET /suite-api/api/reportdefinitions` | list_report_definitions (`subject` is an array of resource-kind strings) |
| `POST /suite-api/api/reports` | generate_report (requires at least one resource UUID) |
| `GET /suite-api/api/reports` / `GET /suite-api/api/reports/{id}` | list_reports / get_report (timestamp field is `completionTime`; definition filter and limit applied client-side); delete_report (blast radius) |
| `DELETE /suite-api/api/reports/{id}` | delete_report |
| `GET /suite-api/api/deployment/node/status` | get_aria_health (a 503 is read as a status, not an error), is_alive, list_adapters (the appliance clock, `systemTime`, for collection ages) |
| `GET /suite-api/api/adapters` | list_adapters (unpaged) |
| `GET /suite-api/api/deployment/node/services/info` | get_aria_health, doctor (per-service health) |
| `GET /suite-api/api/versions/current` | get_aria_health, doctor "Aria version" row, and the version shown when a 9.0+ tool (list_fleet_*, list_findings, promql_query) is called on an older appliance |
| `GET /suite-api/api/collectorgroups` + `GET /suite-api/api/collectors` | list_collector_groups (groups carry member IDs; details enriched from /collectors) |
| Any `GET` in the shipped index (`vmware_aria/api_spec/`) | get_api_path (GET only; path must match an indexed GET operation) |

---

## List Result Envelope

Every list-returning tool wraps its rows in the family envelope
(`vmware_policy.paginated`) rather than returning a bare array, so an agent can
tell a complete answer from page one instead of guessing (VMware-AIops issue
#31). Keys: `items`, `returned`, `limit`, `total`, `truncated`, `hint` — always
all six, with explicit `null` where a value is unknown.

`total` is only populated where the suite-api genuinely reports a collection
size. It is never inferred:

| Tool | `total` source | Notes |
|------|---------------|-------|
| `list_resources` | `pageInfo.totalCount` on `GET /resources` | Suppressed under `name_filter` — that filter is client-side, so the server's count describes the unfiltered kind |
| `list_alert_definitions` | `pageInfo.totalCount` on `GET /alertdefinitions` | Suppressed under `name_filter` |
| `list_symptom_definitions` | `pageInfo.totalCount` on `GET /symptomdefinitions` | `resource_kind` is a server-side param, so it is reflected in the count; suppressed under `name_filter` |
| `list_report_definitions` | `pageInfo.totalCount` on `GET /reportdefinitions` | Suppressed under `name_filter` |
| `list_reports` | Count of matches from the unpaged `GET /reports` | The whole matching set is in hand, so the count is exact |
| `list_rightsizing_recommendations` | VM `pageInfo.totalCount` from the candidate `GET /resources` | One row per VM evaluated, so the count describes the same collection |
| `list_anomalies` | Count of flagged objects on a complete scan; VM `pageInfo.totalCount` when the scan hit its cap | Also carries `scanned`, `vm_total`, `scan_complete`. `limit` bounds the answer, not the scan. Only flagged VMs are returned, so a short list is not evidence of a clean environment |
| `list_alerts` | — | `POST /alerts/query` reports no count; a full page is conservatively flagged truncated |
| `get_top_consumers` | — | A top-N ranking is a slice of an unbounded set |
| `list_collector_groups` | — | `GET /collectorgroups` is unpaged and takes no limit, so `truncated` is always `false` |
| `list_adapters` | Count of matches from the unpaged `GET /adapters` | Exact; the `adapter_kind` filter is applied client-side and reflected in the count |
| `list_metric_keys` | Count of rows after `key_filter` from the unpaged statkeys read | Exact |
| `get_resource_properties` | Count of rows after `name_filter` from the unpaged `GET /resources/{id}/properties` | Exact |
| `get_resource_relationships` | Count of related resources from a complete walk of the paged relationships endpoint | `null` only when the walk hit its safety cap (`direction_note` says so) |
| `list_maintenance_schedules` | `pageInfo.totalCount` on `GET /maintenanceschedules` | `null` when the API reports no size; a set `schedules_note` means `items` is unknown, not empty |
| `list_alert_notes` | `pageInfo.totalCount` on `GET /alerts/{id}/notes` | `null` when the API reports no size; a set `notes_note` means `items` is unknown, not empty |

The six tools added above also return `next_offset`: pass it back as `offset`
and stop when it is `null`.

CLI commands unwrap `items` and print the rows; the envelope is the MCP/library
contract.

Reading rules for an agent:

- **Rows live under `items`.** An empty `items` with `returned: 0` means the query genuinely matched nothing — report that, not a tool failure.
- **`truncated: true` means more rows exist.** Never describe it as the complete set; say it is partial or re-query with a higher `limit` or a narrower filter, as `hint` says.
- **`truncated: false` means the answer is complete.**
- **`total: null` means the API reported no collection size**, so a page filled exactly to the limit is flagged truncated conservatively; a follow-up with a larger limit settles it.
- **`list_anomalies`**: `limit` bounds the answer, not the scan — the environment is ranked in full and the worst `limit` objects returned. Only VMs with a non-zero count are returned, so a short list is not evidence of a clean environment. With `scan_complete: true`, `total` is the number of anomalous objects; with `scan_complete: false` the scan hit its cap, `total` is the VM count, and a `note` says the ranking is partial.

---

## Aria Operations / VCF Operations Version Compatibility

| Feature | Minimum Version |
|---------|----------------|
| VCF Operations 9.1.1.0 | Recognized as the 9.x product family; no exact-release rejection. Judge each operation by its response and declared requirements; full live-tool coverage on this patch is not established. |
| VCF Operations 9.1 (VCF 9.1) | Dedicated tools use the bundled 9.1 API contracts where applicable; this is not proof of full live-tool coverage. PromQL uses the 9.1 VODAP service (base path inferred, not yet verified on real hardware). Aria Operations was rebranded VCF Operations in VCF 9. |
| VCF Operations 9.0 (VCF 9.0) | ✅ suite-api tools plus fleet certificates / passwords / domains and diagnostic findings |
| Aria Operations 8.x | ✅ suite-api tools. Fleet, findings and PromQL are 9.0+: on 8.x they return a "requires VCF Operations 9.0 or newer" error naming the version the appliance reports |
| Token authentication | 6.6+ |
| Resource metrics stats query | 6.7+ |
| Rightsizing recommendations | 7.0+ |
| Anomaly detection | 7.5+ |
| Suite API v2 paths used | 8.0+ |

Endpoints are checked against the vROps 8.6 and VCF Operations 9.1 API indexes in `vmware_aria/api_spec/`. Live-verified on Aria Operations 8.18.7 (2026-09): resources, metrics, alerts and symptoms, rightsizing, health, doctor, node resources, adapters, alert recommendations, and reads of maintenance schedules and alert notes (none existed).

## Maintenance safety boundary

After a write timeout or gateway error, inspect the target before retrying: the write may already have happened. Automatic transient retries apply only to GET reads; explicit authentication recovery is separate.
