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
7. Aria node type / deployment info
8. MCP server module importable

---

## Resource Commands

### `vmware-aria resource list`

List resources by kind.

```
vmware-aria resource list [OPTIONS]

Options:
  --kind -k TEXT    Resource kind [default: VirtualMachine]
                    Values: VirtualMachine, HostSystem, ClusterComputeResource,
                            Datastore, Datacenter, ResourcePool
  --limit -n INT    Max results [default: 50]
  --name TEXT       Filter by name substring (case-insensitive)
  --target -t TEXT  Target name
```

**Output**: Table with Name, ID, Health (color + score), Status.

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
  --target -t TEXT     Target name
```

**Common metric keys**:
- `cpu|usage_average` — CPU utilization percentage
- `mem|usage_average` — Memory utilization percentage
- `cpu|demand_average` — CPU demand (MHz)
- `mem|workload` — Memory workload
- `disk|usage_average` — Disk I/O usage
- `net|usage_average` — Network usage

**Output**: JSON keyed by metric, each containing list of `{timestamp_ms, value}` points.

### `vmware-aria resource health`

Get health badge for a resource.

```
vmware-aria resource health <resource-id> [OPTIONS]
```

**Output**: JSON with health score (0–100), color, description.

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
  --target -t TEXT          Target name
```

### `vmware-aria alert get`

Get full alert details with contributing (triggered) symptoms. Recommendations are attached to the alert definition, not the alert. Alerts carry the resource ID only — resolve names via `vmware-aria resource get <id>`.

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

Cancel (dismiss) an alert.

```
vmware-aria alert cancel <alert-id> [OPTIONS]

Options:
  --yes -y          Skip confirmation prompt
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

**Output**: Table with VM name, recommended CPU, and recommended memory (from the `OnlineCapacityAnalytics|{cpu,mem}|recommendedSize` metrics).

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

### `vmware-aria anomaly risk`

Get risk badge score for a resource.

```
vmware-aria anomaly risk <resource-id> [OPTIONS]
```

**Output**: JSON with risk score (0–100) and color (from the resource's `badges[]` array). For contributing causes, inspect the resource's active alerts.

---

## Health Commands

### `vmware-aria health status`

Check Aria Operations platform health.

```
vmware-aria health status [OPTIONS]
```

**Output**: Console summary (ONLINE / OFFLINE) plus optional details. A per-service breakdown is not exposed by the public API.

### `vmware-aria health collectors`

List collector groups and member status.

```
vmware-aria health collectors [OPTIONS]
```

**Output**: Per-group tables listing collector ID, name, state (UP/DOWN), and local flag (marks the built-in collector on the Aria node).

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

```
vmware-aria report delete <report-id> [OPTIONS]

Options:
  --yes -y          Skip confirmation prompt
  --target -t TEXT  Target name
```

**Audit logged**: yes.

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (API failure, auth failure, validation error) |
| 2 | Usage error (invalid arguments) |

`vmware-aria doctor` exits 0 if all checks pass, 1 if any fail.
