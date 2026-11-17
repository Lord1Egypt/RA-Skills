# VMware AVI Capabilities

All 28 MCP tools exposed by `vmware-avi mcp` (v1.5.15+; legacy entry point: `vmware-avi-mcp`), organized by category.

## Version Compatibility

### AVI Controller (NSX ALB)

| Controller Version | Support Level | Notes |
|--------------------|--------------|-------|
| AVI 30.x | ✅ Full | All 28 tools verified. avisdk `<31.0` upper bound. |
| AVI 22.1.x | ✅ Full | All analytics endpoint quirks fixed in v1.5.11 — `get_virtual_service_analytics` uses POST `/analytics/metrics/collection` with `metric_requests[]`; `list_lb_pools` uses `/virtualservice-inventory` to expose K8S-managed pool groups; SE→VS mapping reconstructed from `vip_summary[].service_engine[]`. |
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
| `python -m vmware_avi.mcp_server` (stdio, via `__main__.py`) | ✅ Full | Docker image `CMD` only — not for end-user CLI install, and no longer used by `smithery.yaml` (which now calls the `vmware-avi mcp` entry point). Added v1.5.22. |
| `uvx --from vmware-avi==2.5.2 vmware-avi-mcp` | ⚠ Fallback | Re-resolves PyPI on each launch; fails behind corporate TLS proxies (踩坑 #25). Use `UV_NATIVE_TLS=true` workaround. |

## Automation Level Reference

Each operation is classified by autonomy level per the Enterprise Harness Engineering framework:

| Level | Meaning | Agent autonomy | Examples in this skill |
|:-:|---|---|---|
| **L1** | Read-only, raw data | Always auto-run | `list_virtual_services`, `get_virtual_service_status`, `list_lb_pools`, `list_lb_pool_members`, `list_service_engines`, `get_service_engine_health`, `get_virtual_service_analytics` queries, AKO/AMKO inventory (`get_ako_status`, `list_ako_clusters`, `get_ako_amko_status`) |
| **L2** | Read + analysis / recommendation | Always auto-run | traffic distribution analysis, health score correlation, pool member ratio summaries, analytics-driven anomaly detection |
| **L3** | Single write — user must approve | Only after explicit confirmation. MCP: `set_virtual_service_enabled`, `disable_lb_pool_member`, `restart_ako`, `upgrade_ako_config`, `force_ako_sync` return a `blast_radius` preview unless `confirm=true`; CLI: double-confirm + `--dry-run` | `set_virtual_service_enabled`, `enable_lb_pool_member`/`disable_lb_pool_member`, `restart_ako`, `upgrade_ako_config`, `force_ako_sync` |
| **L4** | Multi-step plan / apply workflow | Plan generation auto; apply gated by user approval | *(roadmap — VS deployment plans, blue/green pool member rotations)* |
| **L5** | Auto-remediation from learned pattern | Pattern library only; requires `risk:low` + `reversible:true` + `repeatable:true` | *(roadmap — candidates: stale pool member drain, AKO controller reconnect)* |

> Classification comes from each tool's `[READ]`/`[WRITE]` docstring marker,
> not from this table — see the README.

**Notes**:
- L1/L2 are infrastructure reads under the configured account; Policy, RBAC and audit still apply. Read access may reveal sensitive inventory.
- L3 tools always pass through the `@vmware_tool` decorator: connection check → policy check → audit log. The five gated tools then measure their blast radius; without `confirm=true` they stop there, and with it they refuse on a blocker or an unreadable field.
- AKO Kubernetes operations affect ingress/service routing — even "low-risk" restarts can briefly interrupt traffic; treat as L3 with explicit user approval.

## Traditional Mode — AVI Controller (13 tools)

### Virtual Service (3)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `list_virtual_services` | List all Virtual Services on the active controller | `controller` (string, optional) | Low | No |
| `get_virtual_service_status` | Show detailed status of a single VS (VIP, health score, pool binding, enabled state) | `name` (string, **required**) | Low | No |
| `set_virtual_service_enabled` | Enable or disable a Virtual Service. Returns `blast_radius` (VS, uuid, current state, VIPs, pools and member counts); previews unless `confirm=true` | `name` (string, **required**), `enable` (boolean, **required**), `confirm` (boolean, default `false`) | Medium | Yes (both directions) |

### Pool Member (4)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `list_lb_pools` | Discover pools on the Controller, with VS bindings (uses `/virtualservice-inventory` to include K8S-managed pool groups) | `vs_filter` (string, optional) | Low | No |
| `list_lb_pool_members` | List all members of a pool with health status and ratio | `pool` (string, **required**) | Low | No |
| `enable_lb_pool_member` | Enable a pool member (restore traffic after maintenance) | `pool` (string, **required**), `server` (string, **required**) | Low | No |
| `disable_lb_pool_member` | Disable a pool member with graceful connection drain. Returns `blast_radius` (pool, member, enabled members before/after); refuses the pool's only enabled member | `pool` (string, **required**), `server` (string, **required**), `confirm` (boolean, default `false`) | Medium | Yes |

### SSL Certificate (2)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `list_ssl_certs` | List all SSL/TLS certificates on the controller | *(none)* | Low | No |
| `check_ssl_cert_expiry` | Check certificates expiring within N days, with VS mapping | `days` (integer, default: 30) | Low | No |

### Analytics (2)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `get_virtual_service_analytics` | Show VS metrics: L4 bandwidth/connections (`l4_client.avg_bandwidth`, `avg_complete_conns`, `avg_new_established_conns`) + L7 client transaction latency (`l7_client.avg_client_txn_latency`), response errors, total responses | `vs_name` (string, **required**) | Low | No |
| `get_virtual_service_error_logs` | Show recent request error logs for a VS (HTTP status ≥ 400, filter `ge(response_code,400)`) | `vs_name` (string, **required**), `since` (string, default: `"1h"`) | Low | No |

### Service Engine (2)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `list_service_engines` | List all Service Engines: name, mgmt IP, operational status, SE group (via `serviceengine-inventory`, config + runtime merged) | *(none)* | Low | No |
| `get_service_engine_health` | Check SE health: per-SE operational status + connected-VS counts (placement map from `virtualservice-inventory`) | *(none)* | Low | No |

## AKO Mode — Kubernetes (15 tools)

### AKO Pod Ops (4)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `get_ako_status` | Check AKO pod status (phase, restart count, readiness) | `context` (string, optional) | Low | No |
| `get_ako_logs` | View AKO pod logs (tail mode) | `tail` (integer, default: 100), `since` (string, optional) | Low | No |
| `restart_ako` | Restart AKO pod by deleting it (its StatefulSet recreates it). Returns `blast_radius` (pod, uid, phase, Ingresses); the delete is pinned to the measured uid | `context` (string, optional), `confirm` (boolean, default `false`) | High | Yes |
| `get_ako_version` | Show AKO container image tag and Helm chart version | `context` (string, optional) | Low | No |

### AKO Config (3)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `get_ako_config` | Show current AKO Helm values (values.yaml snapshot; release auto-discovered via `helm list` — official installs use `--generate-name`) | *(none)* | Low | No |
| `diff_ako_config` | Preview the pending Helm change, running the same command `upgrade_ako_config` does (`--reuse-values` included) so the diff describes the actual upgrade rather than the chart's defaults. Chart: `oci://projects.packages.broadcom.com/ako/helm-charts/ako` | `chart_version` (optional — empty resolves to registry latest, which can move between calls) | Low | No |
| `upgrade_ako_config` | Helm upgrade the discovered AKO release from the official Broadcom OCI chart with `--reuse-values`. Without `confirm=true` returns `blast_radius` (release, chart now → chart to, status) plus the `helm upgrade --dry-run` output | `confirm` (boolean, default `false`), `chart_version` (optional) | High | Yes |

### Ingress Diagnostics (3)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `check_ako_ingress` | Validate Ingress annotations against AKO expectations in a namespace | `namespace` (string, **required**) | Low | No |
| `list_ako_ingresses` | Show full Ingress-to-VS mapping across all namespaces | *(none)* | Low | No |
| `diagnose_ako_ingress` | Diagnose why a specific Ingress has no corresponding VS on the Controller | `name` (string, **required**), `namespace` (string, default: `"default"`) | Low | No |

### Sync Diagnostics (3)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `get_ako_sync_status` | Check overall K8s-to-Controller sync health | *(none)* | Low | No |
| `diff_ako_sync` | Show objects present in K8s but missing on Controller, and vice versa | *(none)* | Low | No |
| `force_ako_sync` | Force AKO to re-reconcile all K8s objects against the Controller (deletes the AKO pod). Returns `blast_radius` like `restart_ako` | `context` (string, optional), `confirm` (boolean, default `false`) | Medium | Yes |

### Multi-cluster (2)

| Tool | Description | Parameters | Risk | Confirm |
|------|-------------|------------|:----:|:-------:|
| `list_ako_clusters` | List every K8s context and whether AKO runs there (unreadable ones say so) | *(none)* | Low | No |
| `get_ako_amko_status` | Show AMKO (Avi Multi-cluster Kubernetes Operator) GSLB status | *(none)* | Low | No |

## Risk Level Definitions

| Level | Meaning | Examples |
|-------|---------|---------|
| **Low** | Read-only query, no state change | `list_virtual_services`, `check_ssl_cert_expiry`, `get_ako_logs` |
| **Medium** | State change affecting traffic flow, but recoverable | `set_virtual_service_enabled` (disable), `disable_lb_pool_member`, `force_ako_sync` |
| **High** | Disruptive operation affecting running services or deployments | `restart_ako`, `upgrade_ako_config` |

## Tool Counts by Risk Level

Each tool is counted exactly once, at its default (worst-case) risk level, so the
three rows sum to the full tool surface:

| Risk | Count | Tools |
|------|:-----:|-------|
| Low | 23 | All 22 read-only tools + `enable_lb_pool_member` (a write, but it only restores traffic) |
| Medium | 3 | `set_virtual_service_enabled`, `disable_lb_pool_member`, `force_ako_sync` |
| High | 2 | `restart_ako`, `upgrade_ako_config` |

**Total: 23 + 3 + 2 = 28.**

> Note: risk is contextual for two tools, but each is listed only once above, at its
> higher level. `set_virtual_service_enabled` with `enable=true` is effectively Low risk; with
> `enable=false` it is Medium (and High against a critical VS), so it is counted as
> Medium. `upgrade_ako_config` without `confirm=true` is Low risk (preview only); with
> `confirm=true` it is High, so it is counted as High.

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
