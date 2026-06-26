# Capabilities

## Automation Level Reference

Each operation is classified by autonomy level per the Enterprise Harness Engineering framework. **vmware-aria is heavily L1/L2 (20 read / 7 write)** — primarily a monitoring and analysis skill.

| Level | Meaning | Agent autonomy | Examples in this skill |
|:-:|---|---|---|
| **L1** | Read-only, raw data | Always auto-run | `list_resources`, `get_resource`, `get_resource_metrics`, `list_alerts`, `get_alert`, `list_alert_definitions`, capacity / badge queries |
| **L2** | Read + analysis / recommendation | Always auto-run | anomaly counts, top-N consumer ranking, capacity trend forecasting, rightsizing recommendations |
| **L3** | Single write — user must approve | Only after explicit confirmation | `acknowledge_alert` (via takeownership action), `cancel_alert`, `create_alert_definition`, `set_alert_definition_state`, `delete_alert_definition`, `generate_report`, `delete_report` *(the only writes; all auditable)* |
| **L4** | Multi-step plan / apply workflow | *N/A currently* | — *(no multi-step orchestration; Aria is observe/analyze, not configure)* |
| **L5** | Auto-remediation from learned pattern | Pattern library only; requires `risk:low` + `reversible:true` + `repeatable:true` | *(roadmap — candidates: auto-acknowledge known-noisy alerts, auto-cancel resolved-by-event alerts)* |

**Notes**:
- L1/L2 tools are always safe for agents to call without confirmation.
- L3 alert-state writes pass through the `@vmware_tool` decorator: connection check → policy check → audit log. Cancel is irreversible by Aria API design and treated as a destructive operation.
- For VM/host operations see [vmware-aiops](https://github.com/zw008/VMware-AIops); Aria recommendations are advisory, not actuating.

## What vmware-aria Can Do

### Resource Monitoring

- **List any resource type**: VirtualMachine, HostSystem, ClusterComputeResource, Datastore, Datacenter, ResourcePool
- **Filter by name**: substring match across any resource list
- **Get resource details**: health, risk, and efficiency badges plus all identifiers
- **Fetch metric time series**: any metric key with configurable time window and rollup (AVG/MAX/MIN)
- **Find top consumers**: rank VMs or hosts by CPU, memory, disk, or network usage

### Alert Management

- **List active or all alerts**: filter by criticality (INFORMATION/WARNING/IMMEDIATE/CRITICAL) or resource. Alerts carry the resource ID only (the Alert model has no resource name) — resolve names via `get_resource`
- **Inspect alert details**: contributing (triggered) symptoms from the dedicated contributingsymptoms endpoint, plus timeline. Recommendations are attached to the alert definition, not the alert
- **Acknowledge alerts**: mark as seen without closing (control state → ACKNOWLEDGED)
- **Cancel alerts**: permanently dismiss (status → CANCELLED)
- **Browse alert definitions**: the templates that define when alerts fire

### Capacity Planning

- **Cluster capacity overview**: group-level remaining-capacity percentage plus per-dimension (cpu/mem/diskspace) headroom and days-until-full (the percentage metric only exists at group level)
- **Remaining capacity**: how much more CPU, memory, disk can be added before hitting limits
- **Time remaining**: predicted days until each capacity dimension is exhausted (based on trend)
- **Rightsizing recommendations**: identify over-provisioned VMs (reclaim resources) and under-provisioned VMs (prevent degradation)

### Anomaly Detection

- **List anomalies**: per-resource Total Anomalies counts (`System Attributes|total_alarms` metric — active symptoms, events, and DT violations on the object and its children), optionally scoped to one resource. The UI's anomalous-metrics list is not part of the public API
- **Risk badge**: composite risk score (0–100) from the resource's `badges[]` array — predicts likelihood of future problems; for contributing causes inspect the resource's active alerts

### Platform Health

- **Aria health check**: node status (ONLINE / OFFLINE) — a per-service breakdown is not exposed by the public API
- **Collector group status**: list collector groups (member IDs) enriched with each collector's name, UP/DOWN state, and local flag

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
| Manage Aria adapter instances | Not supported (UI required) |

---

## Aria Operations API Coverage

All requests carry `Authorization: vRealizeOpsToken <token>`.

| Endpoint | Used For |
|----------|---------|
| `POST /suite-api/api/auth/token/acquire` | Token authentication |
| `POST /suite-api/api/auth/token/release` | Token release on close (no body; token identified by the Authorization header) |
| `GET /suite-api/api/resources` | list_resources (also candidate listing for topn / anomaly / rightsizing scans) |
| `GET /suite-api/api/resources/{id}` | get_resource, get_resource_health, get_resource_riskbadge (badges come from the `badges[]` array — there are no `/badge/*` endpoints) |
| `POST /suite-api/api/resources/{id}/stats/query` | get_resource_metrics |
| `GET /suite-api/api/resources/stats/topn` | get_top_consumers (resourceId list capped at 100) |
| `GET /suite-api/api/resources/{id}/stats/latest` | capacity tools (OnlineCapacityAnalytics keys), list_anomalies (`System Attributes\|total_alarms`) |
| `POST /suite-api/api/alerts/query` | list_alerts (server-side status/criticality/resource filtering) |
| `GET /suite-api/api/alerts/{id}` | get_alert |
| `GET /suite-api/api/alerts/contributingsymptoms?id={alertId}` | get_alert (triggered symptoms) |
| `POST /suite-api/api/alerts?action=takeownership` | acknowledge_alert |
| `POST /suite-api/api/alerts?action=cancel` | cancel_alert |
| `GET /suite-api/api/alertdefinitions` | list_alert_definitions |
| `POST /suite-api/api/alertdefinitions` | create_alert_definition |
| `PUT /suite-api/api/alertdefinitions/{id}/enable` (or `/disable`) | set_alert_definition_state |
| `DELETE /suite-api/api/alertdefinitions/{id}` | delete_alert_definition |
| `GET /suite-api/api/symptomdefinitions` | list_symptom_definitions (filter param is `resourceKind`) |
| `GET /suite-api/api/reportdefinitions` | list_report_definitions (`subject` is an array of resource-kind strings) |
| `POST /suite-api/api/reports` | generate_report (requires at least one resource UUID) |
| `GET /suite-api/api/reports` / `GET /suite-api/api/reports/{id}` | list_reports / get_report (timestamp field is `completionTime`; definition filter and limit applied client-side) |
| `DELETE /suite-api/api/reports/{id}` | delete_report |
| `GET /suite-api/api/deployment/node/status` | get_aria_health, is_alive |
| `GET /suite-api/api/collectorgroups` + `GET /suite-api/api/collectors` | list_collector_groups (groups carry member IDs; details enriched from /collectors) |

---

## Aria Operations / VCF Operations Version Compatibility

| Feature | Minimum Version |
|---------|----------------|
| VCF Operations 9.1 (VCF 9.1) | ✅ Full — Aria Operations rebranded as VCF Operations in VCF 9. |
| VCF Operations 9.0 (VCF 9.0) | ✅ Full — suite-api endpoints unchanged. |
| Token authentication | 6.6+ |
| Resource metrics stats query | 6.7+ |
| Rightsizing recommendations | 7.0+ |
| Anomaly detection | 7.5+ |
| Suite API v2 paths used | 8.0+ |

**Recommended**: Aria Operations 8.x (vROps 8.x). All endpoints verified against Aria Operations 8.6.
