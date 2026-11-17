# CLI Reference

Complete reference for `vmware-aria` command-line interface.

## Global Options

All commands accept:
- `--target / -t <name>` — Target name from config (uses default if omitted)
- `--config / -c <path>` — Custom config file path

---

## `vmware-aria doctor`

Run pre-flight diagnostics.

```
vmware-aria doctor [OPTIONS]

Options:
  --skip-auth    Skip authentication check (only tests config + network)
  --config -c    Path to config file
```

**Checks performed**:
1. Config file exists at `~/.vmware-aria/config.yaml`
2. `.env` file permissions (warns if wider than 600)
3. Config parse succeeds (validates YAML and target structure)
4. Password env vars are set for each target
5. Network TCP connectivity to port 443 for each target
6. Aria Operations token acquisition (unless `--skip-auth`)
7. Aria version from `GET /versions/current`, e.g. `VMware Aria Operations 8.18.7 (8.x line, build 25423534)` (**WARN** `Not read: …` when it cannot be read — an unreadable version says nothing about whether the target works), and Aria platform health: PASS when HEALTHY, **WARN** when DEGRADED or UNKNOWN (the failed services are named), FAIL when DOWN. Only a failure to connect is an auth FAIL: an error after the token was acquired is a FAIL on the "Aria platform" row (`Checks did not complete: …`). The doctor disconnects from each target either way
8. MCP server module importable

Error details in the doctor table do not tell you to run the doctor again.

---

## Resource Commands

### `vmware-aria resource list`

List resources by kind.

```
vmware-aria resource list [OPTIONS]

Options:
  --kind -k TEXT             Resource kind [default: VirtualMachine]
                             Values: VirtualMachine, HostSystem, ClusterComputeResource,
                                     Datastore, Datacenter, ResourcePool, or all
  --limit -n INT             Max results [default: 50]
  --name TEXT                Filter by name substring (case-insensitive)
  --collection-status TEXT   Keep objects with this data-collection status,
                             e.g. NO_DATA_RECEIVING (case-insensitive)
  --target -t TEXT           Target name
```

**Output**: Table with Name (and Kind with `--kind all`), ID, Health (color + score), Aria state, and Collection.
**Aria state** is Aria's lifecycle state for the object — `STARTED` for a powered-off VM too, so it is not a power state.
**Collection** is whether data is arriving (`DATA_RECEIVING`, `NO_DATA_RECEIVING`, …; `—` when Aria reports none).
To find the objects behind "Objects are not receiving data from adapter instance", run
`vmware-aria resource list --kind all --collection-status NO_DATA_RECEIVING`.
If the filter matches nothing, a yellow line names the statuses the listing did contain.

### `vmware-aria resource get`

Get full resource details.

```
vmware-aria resource get <resource-id> [OPTIONS]

Arguments:
  resource-id  Resource UUID (required)

Options:
  --target -t TEXT  Target name
```

**Output**: JSON with all resource fields including health, risk, efficiency badges and identifiers.

### `vmware-aria resource metrics`

Fetch time-series metrics for a resource.

```
vmware-aria resource metrics <resource-id> [OPTIONS]

Arguments:
  resource-id  Resource UUID (required)

Options:
  --metrics -m TEXT    Comma-separated metric keys
                       [default: cpu|usage_average,mem|usage_average]
  --hours INT          History window in hours [default: 1]
  --summary            Per metric n/min/max/avg/p95/latest and change points, instead of every point
  --interval-type TEXT Span each point covers: MINUTES, HOURS, DAYS, WEEKS, MONTHS [default: MINUTES]
  --interval-quantity INT
                       Units of --interval-type per point, at least 1 [default: 5]
  --rollup TEXT        Value per point: AVG, MAX, MIN, SUM, COUNT, LATEST [default: AVG]
  --target -t TEXT     Target name
```

By default every point is one 5-minute sample, so a month is about 8,600 points per key. For long windows ask Aria to
aggregate: `--hours 720 --interval-type DAYS --interval-quantity 1` returns about 30 daily averages per key (`--rollup MAX`
for daily peaks; with AVG the summary `max` is the highest daily average, not the peak). The MCP tool takes the same
`interval_type`, `interval_quantity` and `rollup_type`. Any other interval type or rollup, or a quantity below 1, is an
error before connecting. `interval` in the output is the resolution requested; `applied` is what Aria reports it used
(`null` when no series carried a complete echo; `series_without_echo` counts those that did not), and `note` appears
only when a complete echo differs from the request.

**Common metric keys** (VirtualMachine names and units as Aria Operations 8.18.7 defines them; other resource kinds differ):
- `cpu|usage_average` — CPU|Usage (%)
- `mem|usage_average` — Memory|Usage (%)
- `cpu|demandmhz` — CPU|Demand (MHz)
- `mem|workload` — Memory|Workload (%)
- `disk|usage_average` — Physical Disk|Total Throughput (KBps) — a throughput, not a utilization percentage
- `net|usage_average` — Network|Usage Rate (KBps)

**Output**: JSON object:

```json
{
  "resource_id": "<uuid>",
  "window_begin_ms": 1757700000000,
  "window_end_ms": 1757703600000,
  "mode": "raw",
  "interval": {"type": "MINUTES", "quantity": 5, "rollup": "AVG",
               "applied": [{"type": "MINUTES", "quantity": 5, "rollup": "AVG"}], "series_without_echo": 0},
  "metrics": {"cpu|usage_average": [{"timestamp_ms": 1757700300000, "value": 3.2}]},
  "missing": [
    {"metric_key": "mem|usage_avg", "reason": "not_collected_for_resource",
     "detail": "...", "similar_keys": ["mem|usage_average", "..."]}
  ],
  "stat_keys_on_resource": 170
}
```

`metrics` holds only keys that returned at least one point. Every other requested key is in `missing`, with `reason`:
`not_collected_for_resource` (the resource never reports it; `similar_keys` lists up to 10 of its keys in the same group,
only keys that `sanitize()` leaves unchanged and that are at most 200 characters — when some were dropped, `detail` says
`N key(s) in the same group were omitted: they contain control characters or exceed 200 characters.`),
`no_data_in_window` (reported, but no points in the window), `resource_reports_no_stat_keys`, or `undetermined`
(the resource's stat-key list could not be read, or some of its rows are in an unrecognised form — `detail` then says
`N of M 'stat-key' rows in an unrecognised form`). `metric_key` is sanitized. `stat_keys_on_resource` is `null` unless something is missing.
A missing key is not a zero. (Before this change the output was a bare object keyed by metric.)

With `--summary` (MCP `summary=true`) `mode` is `summary` and `metrics` is replaced by `summary`: per key `n`, `min`,
`max`, `avg`, `p95`, `latest`, `first_timestamp_ms`, `latest_timestamp_ms`, `change_count`, `change_points` (each
`{timestamp_ms, from, to}` where the value differed from the point before — e.g. `badge|health` 100 → 25; at most 50,
the most recent kept, `change_points_truncated` says when more were dropped) and `non_numeric_points`. `missing` is
unchanged. A continuously varying metric such as CPU usage changes at almost every point, so read `change_count` there.
`p95` is the nearest-rank 95th percentile of the numeric points, an observed value. It is over the points as returned,
so with `--interval-type DAYS` it is the p95 of daily values, not of the 5-minute samples. With fewer than 20 numeric
points it is `null` and `p95_unavailable` says why.

### `vmware-aria resource health`

Get the health, risk and efficiency badges for a resource — and, for a service object, its service state.

```
vmware-aria resource health <resource-id> [OPTIONS]
```

**Output**: JSON with `name`, `kind`, and each badge's score (0–100) and color. The badges score the alerts attached to
that object, not a service's own state: on Aria Operations 8.18.7 the `mem` and `system` children of a vCenter app
object showed HEALTH GREEN 100 while `SERVICE|STATUS` was `orange` and `SERVICE|AVAILABILITY` was 0, because the alert is
raised on the parent. For a kind containing `SERVICE` (e.g. `VCENTER_APPLIANCE_HEALTH_SERVICES`) the output adds `service`:
`status` (`SERVICE|STATUS`, e.g. `green` / `orange`), `availability` (latest `SERVICE|AVAILABILITY` in the last hour),
`available` (`true` for 1, `false` for 0, `null` for anything else or nothing read), `read_errors` (why a value is
unknown) and `note`. `service` is `null` for other kinds.

### `vmware-aria resource top`

List top resource consumers by metric.

```
vmware-aria resource top [OPTIONS]

Options:
  --metric TEXT     Metric key to rank by [default: cpu|usage_average]
  --kind -k TEXT    Resource kind [default: VirtualMachine]
  --top -n INT      Number of top consumers [default: 10]
  --target -t TEXT  Target name
```

**Output**: Table with rank, name, value, unit. `value` is the average of the metric's points over the last hour (5-minute AVG rollup) — the number Aria Operations ranks by — and rows keep Aria's order, descending by `value`. The MCP tool `get_top_consumers` also returns `latest_value`, the most recent point. Resources with no data for the metric in the last hour are left out, not ranked at zero; `excluded_no_data` (MCP) counts the ones the ranking listed with no points. A yellow hint under the table says when that made the list shorter (or when no resources of that kind exist). When no-data rows took slots of a full `--top`, the result is marked truncated and the hint says to raise top_n.

### `vmware-aria resource keys`

List the metric keys a resource reports (with name and unit), or the keys a resource kind defines. Look keys up here before `resource metrics` or `resource top` instead of guessing.

```
vmware-aria resource keys [RESOURCE_ID] [OPTIONS]
vmware-aria resource keys <vm-id> --filter 'mem|'
vmware-aria resource keys --kind HostSystem --filter cpu

Arguments:
  RESOURCE_ID           Resource UUID; omit and pass --kind for a kind's definitions

Options:
  --kind -k TEXT        Resource kind, e.g. VirtualMachine
  --adapter-kind TEXT   Adapter kind for --kind [default: VMWARE]
  --filter -f TEXT      Substring of key or name, e.g. 'mem|'
  --limit -n INT        Page size, 1-500 [default: 100]
  --offset INT          Rows to skip; the next-page offset is printed below the table [default: 0]
  --target -t TEXT      Target name
  --config -c PATH      Config file path
```

Pass exactly one of RESOURCE_ID or `--kind`; both or neither is a usage error (exit 2).

**Output**: Table titled with the resource kind — Key, Name, Unit, and for a resource a Definition column: `found`, `found_by_instance` (an instanced key such as `guestfilesystem:/boot|usage` matched to `guestfilesystem|usage`), `not_defined_for_kind`, or `not_read` (the kind's definitions could not be read, so name and unit are unknown, not absent; a yellow note says why). A yellow line counts keys not defined for the kind. With `--kind` the table lists what the kind defines — a defined key is not collected on every resource. A nonexistent resource ID is an HTTP 404 error, not an empty table. The MCP tool `list_metric_keys` returns the envelope plus `source`, `resource_kind`, `adapter_kind`, `definitions_status` (`read` / `undetermined`), `definitions_note`, `unjoined_count`, `unjoined_keys` and `next_offset`.

### `vmware-aria resource properties`

List a resource's current properties (power state, parent host, extraConfig, ...).

```
vmware-aria resource properties <resource-id> [OPTIONS]
vmware-aria resource properties <vm-id> --name 'summary|'

Options:
  --name TEXT       Substring of the property name, e.g. 'summary|'
  --limit -n INT    Page size, 1-500 [default: 100]
  --offset INT      Rows to skip; the next-page offset is printed below the table [default: 0]
  --target -t TEXT  Target name
  --config -c PATH  Config file path
```

**Output**: Table of Name and Value, sorted by name — e.g. `summary|parentHost`, `summary|parentVcenter`, configured CPU and memory, `config|extraConfig|mem_hotadd`. These are current values; use `resource metrics` for time series. A failed or unrecognised read is an error, never an empty table; a missing resource is HTTP 404.

### `vmware-aria resource relationships`

List resources related to a resource (parents and children).

```
vmware-aria resource relationships <resource-id> [OPTIONS]
vmware-aria resource relationships <vm-id> --type PARENT

Options:
  --type TEXT       ALL, PARENT or CHILD [default: ALL]
  --limit -n INT    Page size, 1-500 [default: 100]
  --offset INT      Rows to skip; the next-page offset is printed below the table [default: 0]
  --target -t TEXT  Target name
  --config -c PATH  Config file path
```

**Output**: Table of Direction (`parent`, `child`, `both`, `other`, or `unknown`), Kind, Name, ID, sorted by kind and name. `--type` must be exactly `ALL`, `PARENT` or `CHILD` in upper case; `ANCESTOR` and `DESCENDANT` are refused (exit 2) — Aria Operations 8.18.7 answers HTTP 400 for them — so walk further by running the command again on a returned ID. With `ALL`, direction is `unknown` and a yellow note says why when the PARENT/CHILD lists could not be read. The MCP tool is `get_resource_relationships`.

---

## Alert Commands

### `vmware-aria alert list`

List alerts.

```
vmware-aria alert list [OPTIONS]

Options:
  --active / --all          Active alerts only vs all [default: active]
  --criticality TEXT        Filter: INFORMATION, WARNING, IMMEDIATE, CRITICAL
  --limit -n INT            Max results [default: 50]
  --json                    Print the result envelope as JSON instead of a table
  --target -t TEXT          Target name
```

**Output**: Table with ID, Name, Criticality, Status, Started (UTC), Resource (name), Resource ID. IDs are never
shortened. A terminal narrower than 160 columns cannot hold both UUID columns, so there each alert prints as a short
block instead (ID, criticality, status and start time; name; resource name and ID). `--json` prints every row field,
including the start and update times in ISO-8601 UTC (the fields ending `_time_utc`) beside the millisecond times.
The start-time field there is `start_time_utc`. Names and kinds come from one batched `GET /resources` lookup per page. A resource whose name could not be resolved prints as `?` — unknown, not "no resource" — and a yellow note under the table says how many could not be retrieved, were not returned (deleted or stale), or were returned with no name in Aria Operations. If the lookup answers with rows that were not requested (the appliance ignored the id filter), requested ids it left out count as could not be retrieved — retry — not as deleted.

### `vmware-aria alert get`

Get full alert details with contributing (triggered) symptoms. Recommendations are attached to the alert definition, not the alert. `get_alert` carries the resource ID only — resolve the name via `vmware-aria resource get <id>` or `alert list`.

Symptoms that carry no name or severity themselves (all of them on Aria Operations 8.18.7) take both from their symptom definition, fetched in one batched `GET /symptomdefinitions` lookup. Each symptom has `definition_lookup`: `resolved`, `not_needed`, `not_found`, `failed`, or `no_definition_id`. A `symptom_definitions_note` key appears when some did not resolve, or when symptoms carry no definition id to look a missing name or severity up by; an empty name there means unknown.

Each symptom also names the object it is on: `resource_id`, `resource_name`, `resource_kind`, `stat_key`, and
`condition` filled from the symptom instance's message (e.g. `HT not equal 0 != 1`). On 8.18.7 the contributing-symptom
payload carries no resource id, so it is read from the symptom instance in `GET /symptoms`; that endpoint ignores its
`id` filter there, so the tool walks the collection and keys rows by id. For "vCenter app health is affected" this names
the services that are down (e.g. `mem`, `system`).

Cost and scope: the walk runs for every alert whose symptoms carry no resource id — on 8.18.7 that is every alert,
not only vCenter app alerts. It costs one `GET /symptoms` per page of the appliance's whole symptom list (1,000 per
page; 78 symptoms on the lab = one request), stops as soon as every symptom is found, and is capped at 20,000
symptoms; plus one batched `GET /resources`. `alert acknowledge` and `alert cancel` read the alert for their
before-state without the walk. A page that fails keeps the symptoms found before it; a server that returns no total
count leaves the unfound ones `failed` (unknown), not `not_found`. `resource_lookup` is `not_needed`, `resolved`, `not_found` (every
page was read and the instance was not there), `failed` (the read failed or stopped early), `no_symptom_id`, or
`instance_names_no_resource`. A `symptom_resources_note` key appears when some could not be read — an empty
`resource_id` there is unknown, not absent.

The start, update and cancel times are each returned twice: as epoch milliseconds (the fields ending `_time_ms`) and
as ISO-8601 UTC (the fields ending `_time_utc`). The cancel time is `0` in milliseconds and `null` in UTC when the
alert was never cancelled.

```
vmware-aria alert get <alert-id> [OPTIONS]
```

### `vmware-aria alert acknowledge`

Acknowledge an alert (marks as seen, does not close it).

```
vmware-aria alert acknowledge <alert-id> [OPTIONS]

Options:
  --yes -y          Skip confirmation prompt
  --target -t TEXT  Target name
```

**Audit logged**: yes.

### `vmware-aria alert cancel`

Cancel (dismiss) an alert. **Asks twice** unless `--yes` is given.

```
vmware-aria alert cancel <alert-id> [OPTIONS]

Options:
  --yes -y          Skip both confirmation prompts
  --target -t TEXT  Target name
```

**Audit logged**: yes. Cancelled alerts will not re-trigger unless the underlying condition recurs.

### `vmware-aria alert definitions`

List alert definition templates.

```
vmware-aria alert definitions [OPTIONS]

Options:
  --name TEXT       Filter by name substring
  --limit -n INT    Max results [default: 50]
  --target -t TEXT  Target name
```

**Output**: Table with Name, Criticality (max severity across the definition's states), Resource Kind, Impact. Creating, enabling/disabling, and deleting alert definitions are MCP-only tools.

### `vmware-aria alert notes`

List the notes on an alert — who is handling it and what was done.

```
vmware-aria alert notes <alert-id> [OPTIONS]

Options:
  --limit -n INT    Page size, 1-500 [default: 50]
  --offset INT      Rows to skip; the next-page offset is printed below the table [default: 0]
  --target -t TEXT  Target name
  --config -c PATH  Config file path
```

**Output**: Table of Created (ms), Type (USER / SYSTEM), User, Note. An unknown alert ID is HTTP 404, not an empty table. A yellow note means Aria answered without a readable notes list: whether the alert has notes is unknown, not "no notes". The MCP tool `list_alert_notes` defaults to 100 rows.

### `vmware-aria alert note-add`

Add a note to an alert. It does not change the alert's status or ownership — use `alert acknowledge` for that. **Asks once** unless `--yes` is given.

```
vmware-aria alert note-add <alert-id> <text> [OPTIONS]
vmware-aria alert note-add <alert-id> "Taking this: rebooting esx-03" --dry-run

Options:
  --dry-run         Print the API call without executing it
  --yes -y          Skip the confirmation prompt
  --target -t TEXT  Target name
  --config -c PATH  Config file path
```

`--dry-run` prints the target and `POST /suite-api/api/alerts/<alert-id>/notes` with its body `{"content": "<text>"}`, and makes no connection. Empty text is refused (exit 2).

**Output**: JSON with `alert_id`, `action`, `created` (the stored note) and `confirmation_note`. When `created` is null Aria did not confirm the note — run `alert notes` before adding it again, because every call adds a note.

**Audit logged**: yes. Risk low; there is no undo for a note.

### `vmware-aria alert recommendations`

Show the prioritized recommendations for an alert, from its alert definition.

```
vmware-aria alert recommendations <alert-id> [OPTIONS]

Options:
  --target -t TEXT  Target name
  --config -c PATH  Config file path
```

**Output**: JSON with `alert_id`, `alert_name`, `criticality`, `alert_definition_id`, `alert_definition_name`, `state_severity`, `status`, `recommendations` (each: `id`, `priority` — lower is more important — `description`, `action`, `lookup`) and `note`. The alert's definition state whose severity matches the alert's criticality is used; otherwise the definition's only state; otherwise the recommendations of every state are merged at their highest priority, `state_severity` is null and `note` says so.

| `status` | Meaning |
|----------|---------|
| `found` | Every recommendation was read |
| `partial` | Some texts could not be read — ids and priorities are listed; `description: null` is unknown, not blank |
| `none_defined` | The definition defines none — `recommendations` is `[]` |
| `unknown` | The definition could not be read — `recommendations` is `null`; never report it as "no recommendations" |

An alert that cannot be read is an error. On Aria Operations 8.18.7 a CRITICAL vCenter-app alert returned 7 prioritized recommendations. The MCP tool is `get_alert_recommendations`.

---

## Capacity Commands

### `vmware-aria capacity overview`

Get a capacity overview for a cluster.

```
vmware-aria capacity overview <cluster-id> [OPTIONS]
```

**Output**: JSON with group-level `capacity_remaining_pct` plus per-dimension (cpu/mem/diskspace) `capacity_remaining` and `time_remaining_days`. The percentage metric exists only at group level. Values are None while capacity analytics warm up.

### `vmware-aria capacity remaining`

Get remaining capacity headroom for a cluster or host.

```
vmware-aria capacity remaining <resource-id> [OPTIONS]
```

**Output**: JSON with group-level `capacity_remaining_pct` and per-dimension `remaining_value` (absolute, unit per dimension e.g. MHz/KB).

### `vmware-aria capacity time-remaining`

Predict how many days until capacity is exhausted.

```
vmware-aria capacity time-remaining <resource-id> [OPTIONS]
```

**Output**: JSON with projected days per capacity dimension (None while capacity analytics have no data).

### `vmware-aria capacity rightsizing`

List VM rightsizing recommendations.

```
vmware-aria capacity rightsizing [OPTIONS]

Options:
  --resource-id TEXT   Scope to a specific VM UUID
  --limit -n INT       Max results [default: 20]
  --target -t TEXT     Target name
```

**Output**: Table with VM name, power state (`template` for templates), sizing status, `vCPU now→rec`, `Mem GiB now→rec`, `Disk GB`, and `Act.` (actionable), from the `OnlineCapacityAnalytics|{cpu,mem,diskspace}|recommendedSize` metrics. Status `reclaimable` means the engine publishes 0 for the VM — that is not a recommendation of zero; `none published` means the VM either needs no resizing or was never scored, which the appliance does not distinguish.

The raw recommendations are MHz (cpu), KB (memory) and GB (disk) — verified on Aria Operations 8.18.7. The table converts them: CPU MHz is divided by the VM's own MHz per vCPU (`cpu|speed` / `numCpu`) and rounded up — except that a result at most 0.01 vCPU (1% of one core's MHz) above a whole number of cores counts as that number, absorbing float noise between the engine's MHz and `cpu|speed`; a real fraction above that still rounds up (1.5 → 2). Memory is shown in GiB. Arrows mark direction against the current configuration: `↓` oversized, `↑` undersized, `=` right-sized. Memory within 1% of the configured size is right-sized. Disk has no direction.

`Act.` is `yes` only when the power state was read as `Powered On`, the template flag was read as false, and CPU or memory is off its recommendation; an unknown power state or template flag is never taken as running. Per-VM caveats print under the table: powered off, template, power state / template flag not published, a power state other than `Powered On`, current size not published, disagreement between `recommendedSize` and the engine's own `summary|oversized|*` / `summary|undersized|*` statistics, and — for every reduction — check the vendor minimum size first (appliances cannot be identified reliably from the API).

The MCP tool returns the same rows as JSON: `recommended_cpu` / `recommended_memory` / `recommended_diskspace` (raw), `recommended_units`, `sizing_status`, `current_vcpus`, `cpu_mhz_per_vcpu`, `recommended_vcpus`, `cpu_direction`, `current_memory_kb`, `memory_direction`, `power_state`, `is_template`, `product_name` (only when the VM publishes a vApp product), `aria_verdict`, `recommendation_range`, `recommendation_stable`, `actionable`, `caveats`, plus the top-level `properties_note` and `history_note`.

Whether a recommendation has settled: two more bulk queries read each VM's daily low and high of the three `recommendedSize` keys over the last 7 days (`recommendation_range`: `window_days`, `days_with_data`, and `cpu_mhz` / `memory_kb` / `diskspace_gb` as `[low, high]`). If CPU or memory ranged by more than 5% of its high, `recommendation_stable` is false, `Act.` is `no`, and a caveat prints the range — for example `recommendation not settled: memory ranged 8.0–32.0 GiB over the last 3 day(s) of history`. The appliance may hold fewer days than the window, which `days_with_data` says. With no history returned, `recommendation_stable` is null. If the history read fails, `history_note` names the failure (the CLI prints it in yellow), both fields are null, and `Act.` is decided without them.

If the bulk property read (`POST /resources/properties/latest/query`) fails, the rows still come back from the stats, but `power_state`, `is_template`, `current_vcpus`, `current_memory_kb`, `recommended_vcpus`, both directions and `product_name` are null — unknown, not unpublished — no row is actionable, and each row carries one caveat starting `VM properties could not be read`. `properties_note` (null when the read succeeded) names the failure — the HTTP status, or no HTTP response — and the CLI prints it in yellow under the table.

---

## Anomaly Commands

### `vmware-aria anomaly list`

List per-resource anomaly counts (`System Attributes|total_alarms` Total Anomalies metric — the public API does not expose the UI's anomalous-metrics list).

```
vmware-aria anomaly list [OPTIONS]

Options:
  --resource-id TEXT   Scope to a specific resource
  --limit -n INT       Max VMs to scan when listing [default: 20]
  --target -t TEXT     Target name
```

**Output**: Table with resource name (or ID) and anomaly count; without `--resource-id`, only resources with non-zero counts are shown, sorted descending.
Aria's key catalogue names `System Attributes|total_alarms` "Total Anomalies". It is not the alert count, which is a separate key, `System Attributes|total_alert_count` (verified on 8.18.7: vcsa read 5 anomalies with no alerts).

### `vmware-aria anomaly risk`

Get risk badge score for a resource.

```
vmware-aria anomaly risk <resource-id> [OPTIONS]
```

**Output**: JSON with risk score (0–100) and color (from the resource's `badges[]` array). For contributing causes, inspect the resource's active alerts.

---

## Health Commands

### `vmware-aria health status`

Check Aria Operations platform health: node, each service, and the release.

```
vmware-aria health status [OPTIONS]
```

**Output**: Console summary with the assessment, the node status, the version (e.g. `VMware Aria Operations 8.18.7 — 8.x line`, or `unknown (<version_error>)`), a per-service table (Service / Health / Details, from `GET /deployment/node/services/info`) or `Services: not read (<reason>)`, and details (always printed).

| Assessment | Meaning |
|------------|---------|
| `HEALTHY` | Node reports ONLINE and every listed service reports OK — or node reports ONLINE and the per-service breakdown was not read, in which case details say no service was checked individually |
| `DEGRADED` | At least one service OK and at least one ERROR — the platform still answers |
| `DOWN` | Every service reports ERROR |
| `UNKNOWN` | The observations do not settle it: node not ONLINE and the breakdown not read; a service reports a state other than OK or ERROR (and it is not DEGRADED); or node not ONLINE while every service reports OK |

A services reply with no service objects in it counts as not read.

The node status is OFFLINE (and `/deployment/node/status` answers HTTP 503) whenever any one service is not running, so OFFLINE alone is not an outage. On Aria Operations 8.18.7 a node with only `LOCATOR` not OK reads DEGRADED. The MCP tool `get_aria_health` returns `assessment`, `overall_status`, `healthy` (assessment is HEALTHY), `system_time_ms`, `services` (null when unreadable, with `services_error`), `services_not_ok`, `services_unrecognized`, `release_name`, `product_name`, `product_version`, `product_line`, `build_number`, `version_error`, and `details`. `details` is composed: the node status (with `(HTTP 503 at /deployment/node/status)` and the node's own details, up to 300 characters), the assessment in words, `Not OK: …` naming services in ERROR, and `services_error`. A version or service list that cannot be read — including a 2xx body that is not JSON — is reported in `version_error` / `services_error`, not raised; `release_name` and `product_name` are sanitized. A node-status failure other than HTTP 503 still raises.

### `vmware-aria health collectors`

List collector groups and member status.

```
vmware-aria health collectors [OPTIONS]
```

**Output**: Per-group tables listing collector ID, name, state (UP/DOWN), and local flag (marks the built-in collector on the Aria node).

### `vmware-aria health node`

Aria node memory, swap, heap and watchdog restarts, with a memory-pressure indicator. Use it when `health status` shows a service in ERROR or the Aria UI/API is slow.

```
vmware-aria health node [OPTIONS]
vmware-aria health node --hours 72 --json

Options:
  --hours INT       Window for min/avg/max, 1-720 hours [default: 24]
  --json            Print the full result as JSON
  --target -t TEXT  Target name
  --config -c PATH  Config file path
```

Reads Aria's own self-monitoring objects (`vC-Ops-Node`, `vC-Ops-Watchdog`).

**Output**: Per node — name and collection status; `Memory pressure: <level> — <basis>`; a table (Metric, Latest, Min, Avg, Max) of memory (`mem|total`, `mem|used`, `mem|free`, `mem|actualFree`, `mem|actualUsed`), swap (`swap|total`, `swap|used`, `swap|free`), heap (`heap|MaxHeapSize`, `heap|CurrentHeapSize`, `heap|CommittedMemory`, `heap|NodeHeapMemoryRemaining`) and committed heap per component, with units from Aria's own statkey definitions (on 8.18.7: GB for memory and swap, MB for the heap sizes, % for `heap|NodeHeapMemoryRemaining`); then the latest watchdog restarts per service, and a yellow `Missing <key>: <reason> — <detail>` line for each key with no value (`not_reported`, `no_data` or `undetermined` — never shown as zero). Min/avg/max are over 5-minute averages, so a shorter spike is smoothed. Watchdog restarts print `unknown — <why>` when they could not be read; yellow `units_error` / `latest_error` / `window_error` / `watchdog_error` lines name reads that failed.

Memory pressure is an indicator, not a diagnosis: HIGH when actual free memory (`mem|actualFree`) is below 10% of `mem|total`, ELEVATED below 20%, NORMAL at 20% or more, UNKNOWN when the readings do not settle it. On Aria Operations 8.18.7 after a memory upgrade the node read `mem|total` 15.61 GB (was 7.75), actual free 41%, NORMAL, and 9 watchdog services with 0 restarts. The MCP tool is `get_aria_node_resources` (`window_hours`).

### `vmware-aria health adapters`

Adapter instances, when each last collected, and whether that is stale. Use it for "Objects are not receiving data" or metrics that stopped updating.

```
vmware-aria health adapters [OPTIONS]
vmware-aria health adapters --kind VMWARE

Options:
  --kind TEXT       Adapter kind key, e.g. VMWARE (case-insensitive)
  --limit -n INT    Page size, 1-500 [default: 100]
  --offset INT      Rows to skip; the next-page offset is printed below the table [default: 0]
  --json            Print the full result as JSON
  --target -t TEXT  Target name
  --config -c PATH  Config file path
```

**Output**: Table titled with the clock the ages are measured on (`appliance` — the node status `systemTime` — or `local` when that cannot be read): Name, Kind, Last collected (seconds ago), Interval (minutes), Stale (yes / no / unknown), Resources, Metrics; then each adapter's own message. Stale means the last collection is older than max(3 × the adapter's monitoring interval, 15 minutes); unknown means the timestamp or interval is missing. When `--kind` matches nothing, the kinds present are printed. An empty or unrecognised `GET /adapters` answer is an error, not "no adapters" — every deployment runs a self-monitoring adapter. A recent last collection does not prove every object behind the adapter receives data. `--json` adds `id`, `resource_kind`, `collector_id`, `collector_group_id`, `last_heartbeat_ms` and its age, `stale_basis`, and envelope-level `stale_adapters`, `staleness_unknown` and `adapter_kinds_present`. On Aria Operations 8.18.7 all 6 adapters were not stale. The MCP tool is `list_adapters`.

---

## Report Commands

### `vmware-aria report definitions`

List available report definition templates.

```
vmware-aria report definitions [OPTIONS]

Options:
  --name TEXT       Filter by name substring
  --limit -n INT    Max results [default: 50]
  --target -t TEXT  Target name
```

**Output**: Table with Name, ID, Subject Type (resource kinds the template applies to), Owner.

### `vmware-aria report generate`

Trigger report generation from a definition template (async).

```
vmware-aria report generate <definition-id> --resources <id1,id2> [OPTIONS]

Options:
  --resources TEXT  Comma-separated resource UUIDs — at least one is required
                    (the Report API generates against a resource)
  --target -t TEXT  Target name
```

**Audit logged**: yes. Returns the queued `report_id`; poll with `report get`.

### `vmware-aria report list`

List generated reports.

```
vmware-aria report list [OPTIONS]

Options:
  --definition-id TEXT  Filter by definition UUID (applied client-side)
  --limit -n INT        Max results [default: 20]
  --target -t TEXT      Target name
```

### `vmware-aria report get`

Get status and download URLs for a generated report.

```
vmware-aria report get <report-id> [OPTIONS]
```

**Output**: Status; when `COMPLETED`, the PDF `download_url` and `csv_url`.

### `vmware-aria report delete`

Delete a generated report (the definition and schedules remain intact).
**Irreversible — asks twice** unless `--yes` is given.

```
vmware-aria report delete <report-id> [OPTIONS]

Options:
  --yes -y          Skip both confirmation prompts
  --target -t TEXT  Target name
```

**Audit logged**: yes.

---

## Maintenance Commands

Maintenance stops Aria alerting on a resource and collecting its data. `start` and `end` **ask once** unless `--yes` is given; `--dry-run` prints the API call and makes none — no connection, no request. Both are audited with the state before and after, and governed by vmware-policy under the MCP tool names `start_resource_maintenance` / `end_resource_maintenance` (risk medium).

### `vmware-aria maintenance start`

Put a resource in maintenance.

```
vmware-aria maintenance start <resource-id> [OPTIONS]
vmware-aria maintenance start <host-id> --duration 120
vmware-aria maintenance start <host-id> --duration 60 --dry-run
vmware-aria maintenance start <host-id> --end $(( ($(date +%s) + 7200) * 1000 ))

Arguments:
  resource-id  Resource UUID (from `vmware-aria resource list`) (required)

Options:
  --duration INT    Window length in minutes
  --end INT         Window end, epoch milliseconds
  --dry-run         Print the API call without executing it
  --yes -y          Skip the confirmation prompt
  --target -t TEXT  Target name
  --config -c PATH  Config file path
```

With `--duration` (1–525600 minutes) or `--end` (epoch **milliseconds**, in the future — the example above computes two hours from now in any POSIX shell; a fixed timestamp stops working once it passes) the resource is `MAINTAINED` for that window and returns to its prior state when it expires; give one, not both. With neither it enters manual maintenance (`MAINTAINED_MANUAL`) that lasts until `maintenance end` — easy to forget, so prefer a window. An invalid window is refused (exit 2) before anything is sent. `--dry-run` prints `PUT /suite-api/api/resources/<resource-id>/maintained` with the `duration` or `end` query parameter.

**Output**: JSON with `requested` (`mode` timed / manual, `duration_minutes`, `end_time_ms`), `before` and `after` (each: `name`, `kind`, `adapter_states`, `in_maintenance`, `maintenance_mode`, `note`, `read_error`), `confirmed` (true / false / null — null means the state could not be read afterwards, which is unknown, not failure) and `note`.

**Audit logged**: yes, with before and after state. Undo: `maintenance end`.

### `vmware-aria maintenance end`

Take a resource out of maintenance: Aria resumes alerting and collection.

```
vmware-aria maintenance end <resource-id> [OPTIONS]

Options:
  --dry-run         Print the API call without executing it
  --yes -y          Skip the confirmation prompt
  --target -t TEXT  Target name
  --config -c PATH  Config file path
```

Refused (exit 2) only when the resource is known not to be in maintenance — an adapter reports a state such as `STARTED` or `STOPPED`, so there is nothing to end. When the state is unknown (it cannot be read, or an adapter reports `UNKNOWN` / `NONE`) the call proceeds and `before` says unknown. `--dry-run` prints `DELETE /suite-api/api/resources/<resource-id>/maintained`.

**Output**: JSON with `before`, `after`, `confirmed` (true once the resource no longer reports maintenance, false when it still does, null when unknown) and `note`.

**Audit logged**: yes, with before and after state. The MCP undo (`start_resource_maintenance`) is recorded only when the resource was known to be in maintenance before; it re-enters manual maintenance — the end of a timed window is not restored.

### `vmware-aria maintenance schedules`

List maintenance schedules.

```
vmware-aria maintenance schedules [OPTIONS]

Options:
  --resource-id TEXT  Only schedules for this resource
  --limit -n INT      Page size, 1-500 [default: 50]
  --offset INT        Rows to skip; the next-page offset is printed below the table [default: 0]
  --target -t TEXT    Target name
  --config -c PATH    Config file path
```

**Output**: Table of Name, Type (ONCE / DAILY / WEEKLY / MONTHLY / YEARLY), Start (hour:minute and time zone), Duration (min), Recurrence, Expires (date, or `after N runs`), ID. A schedule does not list the resources it applies to — use `--resource-id`. A yellow note means the list could not be read: the schedules are unknown, not absent. The MCP tool `list_maintenance_schedules` defaults to 100 rows.

---

## Fleet Commands (VCF Operations 9.1)

Read-only fleet / diagnostics queries added for VCF Operations 9.1. The suite-api
*paths* are verified against the VCF 9.1 OpenAPI; the response *schemas* are read
defensively, and an unrecognised shape returns an empty result carrying a `note`
that the empty result is unconfirmed (never a silent "none"). The `promql`
sub-command reaches the real-time metrics (VODAP) service on a separate base
(`/data-query-service`) whose prefix is **INFERRED and not yet confirmed on real
hardware** — every result carries `base_path_confirmed: false`.

### `vmware-aria fleet certificates`

List certificate status/expiry across the VCF fleet.

```
vmware-aria fleet certificates [OPTIONS]

Options:
  --limit -n INT    Max rows (default 50)
  --target -t TEXT  Target name
```

### `vmware-aria fleet passwords`

List managed password-account status across the VCF fleet (read-only; does not rotate).

```
vmware-aria fleet passwords [OPTIONS]

Options:
  --limit -n INT    Max rows (default 50)
  --target -t TEXT  Target name
```

### `vmware-aria fleet domains`

List SDDC/workload domains behind one registered VCF integration. The integration
UUID comes from the Operations Integrations page.

```
vmware-aria fleet domains <integration-id> [OPTIONS]

Options:
  --limit -n INT    Max rows (default 50)
  --target -t TEXT  Target name
```

### `vmware-aria fleet findings`

List Operations diagnostic findings (not compliance — use vmware-harden for that).

```
vmware-aria fleet findings [OPTIONS]

Options:
  --severities TEXT  Comma-separated, e.g. CRITICAL,WARNING
  --categories TEXT  Comma-separated category filter
  --types TEXT       Comma-separated findingType filter
  --limit -n INT     Max rows (default 50)
  --target -t TEXT   Target name
```

### `vmware-aria fleet promql`

Run a real-time PromQL instant query against the VCF 9.1 VODAP service. Base path
INFERRED — confirm against a live appliance (`base_path_confirmed: false`).

```
vmware-aria fleet promql <query> [OPTIONS]

Options:
  --time TEXT       Evaluation timestamp (RFC3339 or Unix seconds)
  --source TEXT     Data-source id to scope the query
  --limit -n INT    Max result series (default 50)
  --target -t TEXT  Target name
```

---

## Raw API Commands (read-only escape hatch)

For reads no other command covers. The MCP tools are `search_api_operations` and `get_api_path`; both are audited under those names.

### `vmware-aria api search`

Search the suite-api operation index shipped with this skill (vROps 8.6 and VCF Operations 9.1). Contacts no appliance.

```
vmware-aria api search <query> [OPTIONS]
vmware-aria api search "resource properties"

Options:
  --limit -n INT    Operations to show, 1-100 [default: 20]
```

**Output**: Table of Method, Path, Indexes (`8.6`, `9.1`) and Summary; non-GET methods are dimmed — only GET paths can be read with `api get`.

### `vmware-aria api get`

GET one indexed suite-api path through the target's client and print the JSON answer.

```
vmware-aria api get <path> [OPTIONS]
vmware-aria api get /api/resources/<id>/properties
vmware-aria api get /api/alerts --param pageSize=20 --param page=0

Options:
  --param -p TEXT   Query parameter NAME=VALUE; repeatable
  --target -t TEXT  Target name
  --config -c PATH  Config file path
```

**Output**: `{path, operation, index, product_version, truncated, body}`. `path` must match a GET operation of the index with each `{name}` replaced by a value; other methods, unindexed paths, `..`, `//`, `?` or `#` in the path, URLs and percent-encoding are refused before connecting (exit 2). On a 9.x appliance only the 9.1 index applies; on 8.x, or when the version cannot be read, either index. Strings are sanitized and cut to 500 characters; over 30,000 characters of JSON the answer is `truncated: true` with `original_size` and `body_text` (cut, not valid JSON) — page with `--param pageSize=...`.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (API failure, auth failure, validation error) |
| 2 | Usage error (invalid arguments) |

`vmware-aria doctor` exits 0 if all checks pass, 1 if any fail. WARN rows do not fail.
