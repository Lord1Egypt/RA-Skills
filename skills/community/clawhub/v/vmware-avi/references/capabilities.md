# VMware AVI Capabilities

All 28 MCP tools exposed by `vmware-avi mcp` (v1.5.15+; legacy entry point: `vmware-avi-mcp`), organized by category.

## Version Compatibility

### AVI Controller (NSX ALB)

| Controller Version | Support Level | Notes |
|--------------------|--------------|-------|
| AVI 30.x | ✅ Full | All 28 tools verified. avisdk `<31.0` upper bound. |
| AVI 22.1.x | ✅ Full | All analytics endpoint quirks fixed in v1.5.11 — `vs_analytics` uses POST `/analytics/metrics/collection` with `metric_requests[]`; `pool_list` uses `/virtualservice-inventory` to expose K8S-managed pool groups; SE→VS mapping reconstructed from `vip_summary[].service_engine[]`. |
| AVI < 22.1 | ⚠ Untested | avisdk may load but analytics/inventory endpoints differ. Not in CI. |

### VCF (VMware Cloud Foundation)

| VCF Version | Bundled AVI / NSX ALB | Support |
|-------------|-----------------------|---------|
| VCF 9.1 | NSX ALB (avisdk >=22.1,<31.0 covers it) | ✅ Full (declared v1.5.23) |
| VCF 9.0 | NSX ALB (avisdk >=22.1,<31.0 covers it) | ✅ Full (declared v1.5.23) |
| VCF 5.x | AVI 22.x | ✅ Full |

### Runtime

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | ≥ 3.11 | `requires-python` bumped from 3.10 to 3.11 in v1.5.19 (regression eval uses `tomllib`). |
| avisdk | ≥ 22.1, < 31.0 | Auto-installed. Range chosen so VCF 9.x bundled AVI is covered without forcing a major SDK jump. |
| kubernetes (Python) | ≥ 28.0 | Required only for AKO mode. |
| kubectl | any recent | Required only for AKO operations. |
| helm | ≥ 3.x | Required only for AKO config show/diff/upgrade. |

### MCP Transport

| Mode | Status | Recommended |
|------|--------|-------------|
| `vmware-avi mcp` (CLI subcommand, stdio) | ✅ Full | ✅ v1.5.15+ default — no PyPI re-resolve, works behind corporate TLS proxies. |
| `vmware-avi-mcp` (legacy console script, stdio) | ✅ Full | Kept for backward compatibility with pre-1.5.15 configs. |
| `python -m mcp_server` (stdio, via `__main__.py`) | ✅ Full | Container/Smithery deployments only — not for end-user CLI install. Added v1.5.22. |
| `uvx --from vmware-avi vmware-avi-mcp` | ⚠ Fallback | Re-resolves PyPI on each launch; fails behind corporate TLS proxies (踩坑 #25). Use `UV_NATIVE_TLS=true` workaround. |

## Automation Level Reference

Each operation is classified by autonomy level per the Enterprise Harness Engineering framework:

| Level | Meaning | Agent autonomy | Examples in this skill |
|:-:|---|---|---|
| **L1** | Read-only, raw data | Always auto-run | `vs_list`, `vs_status`, `pool_members`, `pool_status`, `controller_status`, `analytics_metrics` queries, AKO/AMKO inventory |
| **L2** | Read + analysis / recommendation | Always auto-run | traffic distribution analysis, health score correlation, pool member ratio summaries, analytics-driven anomaly detection |
| **L3** | Single write — user must approve | Only after explicit confirmation; destructive ops require double-confirm + `--dry-run` | `vs_toggle` (disable), `pool_member_enable`/`disable`, AKO `restart`/`upgrade`, `force_resync`, AMKO operations |
| **L4** | Multi-step plan / apply workflow | Plan generation auto; apply gated by user approval | *(roadmap — VS deployment plans, blue/green pool member rotations)* |
| **L5** | Auto-remediation from learned pattern | Pattern library only; requires `risk:low` + `reversible:true` + `repeatable:true` | *(roadmap — candidates: stale pool member drain, AKO controller reconnect)* |

**Notes**:
- L1/L2 tools are always safe for agents to call without confirmation.
- L3 tools always pass through the `@vmware_tool` decorator: connection check → policy check → audit log → double-confirm.
- AKO Kubernetes operations affect ingress/service routing — even "low-risk" restarts can briefly interrupt traffic; treat as L3 with explicit user approval.

## Traditional Mode — AVI Controller (13 tools)

### Virtual Service (3)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `vs_list` | List all Virtual Services on the active controller | `controller` (string, optional) | Low | No |
| `vs_status` | Show detailed status of a single VS (VIP, health score, pool binding, enabled state) | `name` (string, **required**) | Low | No |
| `vs_toggle` | Enable or disable a Virtual Service | `name` (string, **required**), `enable` (boolean, **required**) | Medium | Yes (disable) |

### Pool Member (4)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `pool_list` | Discover pools on the Controller, with VS bindings (uses `/virtualservice-inventory` to include K8S-managed pool groups) | `vs_filter` (string, optional) | Low | No |
| `pool_members` | List all members of a pool with health status and ratio | `pool` (string, **required**) | Low | No |
| `pool_member_enable` | Enable a pool member (restore traffic after maintenance) | `pool` (string, **required**), `server` (string, **required**) | Low | No |
| `pool_member_disable` | Disable a pool member with graceful connection drain | `pool` (string, **required**), `server` (string, **required**) | Medium | Yes |

### SSL Certificate (2)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `ssl_list` | List all SSL/TLS certificates on the controller | *(none)* | Low | No |
| `ssl_expiry_check` | Check certificates expiring within N days, with VS mapping | `days` (integer, default: 30) | Low | No |

### Analytics (2)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `vs_analytics` | Show VS metrics: L4 bandwidth/connections (`l4_client.avg_bandwidth`, `avg_complete_conns`, `avg_new_established_conns`) + L7 client transaction latency (`l7_client.avg_client_txn_latency`), response errors, total responses | `vs_name` (string, **required**) | Low | No |
| `vs_error_logs` | Show recent request error logs for a VS (HTTP status ≥ 400, filter `ge(response_code,400)`) | `vs_name` (string, **required**), `since` (string, default: `"1h"`) | Low | No |

### Service Engine (2)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `se_list` | List all Service Engines: name, mgmt IP, operational status, SE group (via `serviceengine-inventory`, config + runtime merged) | *(none)* | Low | No |
| `se_health` | Check SE health: per-SE operational status + connected-VS counts (placement map from `virtualservice-inventory`) | *(none)* | Low | No |

## AKO Mode — Kubernetes (17 tools)

### AKO Pod Ops (4)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `ako_status` | Check AKO pod status (phase, restart count, readiness) | `context` (string, optional) | Low | No |
| `ako_logs` | View AKO pod logs (tail mode) | `tail` (integer, default: 100), `since` (string, optional) | Low | No |
| `ako_restart` | Restart AKO pod by deleting it (its StatefulSet recreates it) | `context` (string, optional) | High | Yes |
| `ako_version` | Show AKO container image tag and Helm chart version | `context` (string, optional) | Low | No |

### AKO Config (3)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `ako_config_show` | Show current AKO Helm values (values.yaml snapshot; release auto-discovered via `helm list` — official installs use `--generate-name`) | *(none)* | Low | No |
| `ako_config_diff` | Show diff between running values and the official Broadcom OCI chart (`oci://projects.packages.broadcom.com/ako/helm-charts/ako`) | *(none)* | Low | No |
| `ako_config_upgrade` | Helm upgrade the discovered AKO release from the official Broadcom OCI chart with `--reuse-values` (defaults to dry-run) | `dry_run` (boolean, default: `true`) | High | Yes |

### Ingress Diagnostics (3)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `ako_ingress_check` | Validate Ingress annotations against AKO expectations in a namespace | `namespace` (string, **required**) | Low | No |
| `ako_ingress_map` | Show full Ingress-to-VS mapping across all namespaces | *(none)* | Low | No |
| `ako_ingress_diagnose` | Diagnose why a specific Ingress has no corresponding VS on the Controller | `name` (string, **required**), `namespace` (string, default: `"default"`) | Low | No |

### Sync Diagnostics (3)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `ako_sync_status` | Check overall K8s-to-Controller sync health | *(none)* | Low | No |
| `ako_sync_diff` | Show objects present in K8s but missing on Controller, and vice versa | *(none)* | Low | No |
| `ako_sync_force` | Force AKO to re-reconcile all K8s objects against the Controller | *(none)* | Medium | Yes |

### Multi-cluster (2)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `ako_clusters` | List all K8s clusters with AKO deployed | *(none)* | Low | No |
| `ako_amko_status` | Show AMKO (Avi Multi-cluster Kubernetes Operator) GSLB status | *(none)* | Low | No |

## Risk Level Definitions

| Level | Meaning | Examples |
|-------|---------|---------|
| **Low** | Read-only query, no state change | `vs_list`, `ssl_expiry_check`, `ako_logs` |
| **Medium** | State change affecting traffic flow, but recoverable | `vs_toggle` (disable), `pool_member_disable`, `ako_sync_force` |
| **High** | Disruptive operation affecting running services or deployments | `ako_restart`, `ako_config_upgrade` |

## Tool Counts by Risk Level

| Risk | Count | Tools |
|------|:-----:|-------|
| Low | 23 | All read-only tools + `vs_toggle` (enable), `pool_member_enable` |
| Medium | 4 | `vs_toggle` (disable), `pool_member_disable`, `ako_sync_force`, `pool_member_enable` contextually |
| High | 3 | `ako_restart`, `ako_config_upgrade` (when `dry_run=false`), `vs_toggle` (disable on critical VS) |

> Note: `vs_toggle` with `enable=true` is Low risk. With `enable=false` it is Medium risk and requires confirmation. Similarly, `ako_config_upgrade` with `dry_run=true` is Low risk (preview only); with `dry_run=false` it becomes High risk.

## Audit Coverage

All 28 tools are wrapped with `@vmware_tool` from vmware-policy, which provides:

- **Pre-execution**: Policy rule check against `~/.vmware/rules.yaml` (deny rules, maintenance windows)
- **Post-execution**: Audit log entry written to `~/.vmware/audit.db` (SQLite WAL mode)
- **Input sanitization**: All AVI API response text processed through `_sanitize()` (truncation + control character cleanup)

## Traditional vs AKO Mode Requirements

| Requirement | Traditional Mode | AKO Mode |
|-------------|:----------------:|:--------:|
| AVI Controller access | Required | Optional (for sync tools) |
| avisdk Python package | Required | Not required |
| kubectl in PATH | Not required | Required |
| helm in PATH | Not required | Required (for config operations) |
| kubeconfig | Not required | Required |
| kubernetes Python package | Not required | Required |
