---
name: vmware-avi
description: >
  Use this skill whenever the user mentions load balancing, ingress, virtual services, pool members, AVI, NSX ALB, AKO, or application delivery.
  Also trigger when the user mentions AKO ingress troubleshooting in a Tanzu/vSphere environment.
  Do NOT trigger when the user explicitly asks to set up or configure nginx/HAProxy/Traefik from scratch — those are not AVI tasks.
  Directly handles: virtual service listing and enable/disable, pool member management (drain/enable traffic), SSL certificate expiry checks,
  analytics and error logs, service engine health, AKO pod troubleshooting, AKO Helm config management, Ingress annotation validation,
  K8s-to-Controller sync diagnostics, and multi-cluster AKO overview.
  Always use this skill for any "virtual service", "pool member", "AKO status", "AKO logs", "ingress diagnose", "ssl expiry",
  "load balancer", "NSX ALB", "AVI controller", "AKO sync", "ingress", or "负载均衡" task.
  For VM lifecycle use vmware-aiops, for NSX networking use vmware-nsx, for K8s cluster lifecycle (Supervisor/TKC) use vmware-vks.
installer:
  kind: uv
  package: vmware-avi
argument-hint: "[vs-name, ako command, or describe your task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"env":["VMWARE_AVI_CONFIG"],"bins":["vmware-avi"],"config":["~/.vmware-avi/config.yaml","~/.vmware-avi/.env"]},"optional":{"env":["VMWARE_<CONTROLLER>_PASSWORD","KUBECONFIG"],"bins":["vmware-policy","kubectl"]},"primaryEnv":"VMWARE_AVI_CONFIG","homepage":"https://github.com/zw008/VMware-AVI","emoji":"🔀","os":["macos","linux"]}}
compatibility: >
  vmware-policy auto-installed as Python dependency (provides @vmware_tool decorator and audit logging). All write operations audited to ~/.vmware/audit.db.
  AVI Controller operations require avisdk and a per-controller password env var in ~/.vmware-avi/.env following the pattern <CONTROLLER_NAME_UPPER>_PASSWORD (e.g., controller "prod-avi" → PROD_AVI_PASSWORD).
  AKO operations require kubectl and a valid kubeconfig (default ~/.kube/config or KUBECONFIG env var). Kubeconfig is read-only — this skill does not modify kubeconfig files.
---

# VMware AVI

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by VMware, Inc. or Broadcom Inc.** "VMware", "NSX", and "AVI" are trademarks of Broadcom. Source code is publicly auditable at [github.com/zw008/VMware-AVI](https://github.com/zw008/VMware-AVI) under the MIT license.

AVI (NSX Advanced Load Balancer) application delivery and AKO Kubernetes operations — 28 MCP tools.

> **Dual mode**: Traditional AVI Controller management + AKO K8s operations in one skill.
> **Family**: [vmware-aiops](https://github.com/zw008/VMware-AIops) (VM lifecycle), [vmware-monitor](https://github.com/zw008/VMware-Monitor) (inventory/health), [vmware-storage](https://github.com/zw008/VMware-Storage) (iSCSI/vSAN), [vmware-vks](https://github.com/zw008/VMware-VKS) (Tanzu Kubernetes), [vmware-nsx](https://github.com/zw008/VMware-NSX) (NSX networking), [vmware-nsx-security](https://github.com/zw008/VMware-NSX-Security) (DFW/firewall), [vmware-aria](https://github.com/zw008/VMware-Aria) (metrics/alerts/capacity), [vmware-harden](https://github.com/zw008/VMware-Harden) (compliance baselines).
> | [vmware-pilot](../vmware-pilot/SKILL.md) (workflow orchestration) | [vmware-policy](../vmware-policy/SKILL.md) (audit/policy)

## What This Skill Does

| Category | Tools | Count |
|----------|-------|:-----:|
| **Virtual Service** | list, status, enable/disable | 3 |
| **Pool Member** | pool discovery, member list, enable/disable member (drain/restore traffic) | 4 |
| **SSL Certificate** | list, expiry check | 2 |
| **Analytics** | VS metrics overview, request error logs | 2 |
| **Service Engine** | list, health check | 2 |
| **AKO Pod Ops** | status, logs, restart, version info | 4 |
| **AKO Config** | values.yaml view, Helm diff, Helm upgrade | 3 |
| **Ingress Diagnostics** | annotation validation, VS mapping, error diagnosis, fix recommendation | 4 |
| **Sync Diagnostics** | K8s-Controller comparison, inconsistency list, force resync | 3 |
| **Multi-cluster** | cluster list, cross-cluster AKO overview, AMKO status | 3 |

## Quick Install

```bash
uv tool install vmware-avi
vmware-avi doctor            # checks Controller connectivity + kubeconfig + avisdk
```

## When to Use This Skill

- List, enable, or disable virtual services on AVI Controller
- Add, remove, drain, or restore pool members (maintenance windows, rolling deployments)
- Check SSL certificate expiry across all virtual services
- View VS analytics — throughput, latency, error rates, request logs
- Check service engine status (inventory-based) and per-SE VS placement counts
- Troubleshoot AKO pods — status, logs, restarts
- Manage AKO Helm configuration — view, diff, upgrade values.yaml
- Validate Ingress annotations and diagnose why a VS wasn't created as expected
- Detect sync drift between K8s resources and AVI Controller objects
- Get a cross-cluster view of AKO deployments and AMKO status

**Use companion skills for**:
- VM lifecycle, deployment, guest ops → `vmware-aiops`
- NSX segments, gateways, NAT → `vmware-nsx`
- DFW firewall rules, security groups → `vmware-nsx-security`
- K8s cluster lifecycle (Supervisor, TKC) → `vmware-vks`
- Read-only vSphere monitoring → `vmware-monitor`

## Related Skills — Skill Routing

| User Intent | Recommended Skill |
|-------------|------------------|
| Load balancer, VS, pool, AVI, ALB, AKO | **vmware-avi** ← this skill |
| VM lifecycle, deployment, guest ops | **vmware-aiops** (`uv tool install vmware-aiops`) |
| Read-only vSphere monitoring | **vmware-monitor** (`uv tool install vmware-monitor`) |
| Storage: iSCSI, vSAN, datastores | **vmware-storage** (`uv tool install vmware-storage`) |
| NSX networking: segments, gateways, NAT | **vmware-nsx** (`uv tool install vmware-nsx-mgmt`) |
| NSX security: DFW rules, security groups | **vmware-nsx-security** (`uv tool install vmware-nsx-security`) |
| Tanzu Kubernetes (Supervisor/TKC) | **vmware-vks** (`uv tool install vmware-vks`) |
| Aria Ops: metrics, alerts, capacity | **vmware-aria** (`uv tool install vmware-aria`) |
| Multi-step workflows with approval | **vmware-pilot** |
| Compliance baselines (CIS / 等保 / PCI-DSS), drift detection, LLM remediation advisor | **vmware-harden** (`uv tool install vmware-harden`) |
| Audit log query | **vmware-policy** (`vmware-audit` CLI) |

## Common Workflows

### Maintenance Window — Drain a Pool Member

**Pre-flight (judgment — affects live traffic)**:
- Capacity check: pool must have ≥ 2 healthy members. Disabling the only-other-healthy member is a self-DoS. Verify with `pool members my-pool` first.
- Connection persistence: if VS uses session persistence (cookie/source-IP), existing sessions stay pinned to the disabled member until they expire. "Drain" is not instant — 5-30 min depending on persistence TTL.
- Long-lived connections: WebSocket/streaming sessions can hold for hours. Decide upfront: hard-disconnect (faster, user-visible) or wait (slower, transparent).
- Observability: enable analytics on the VS BEFORE disabling — you need the baseline to detect degradation.

**Steps**:
1. `pool members my-pool` → confirm ≥ 2 healthy members and identify session persistence config
2. `pool disable my-pool <server-ip>` (graceful drain — new connections stop, existing finish)
3. `analytics my-vs --duration 15m` → watch active connection count to the drained member trend toward zero
4. Perform maintenance only after active connections = 0 (or you've decided to hard-disconnect)
5. `pool enable my-pool <server-ip>` → re-enable
6. **Verify** before declaring success: health monitor passes (typically 30-90 sec) AND new connections are landing on the member (analytics drill-down)

### AKO Ingress Not Creating VS

**Judgment**: this is a layered failure — figure out which layer broke before randomly probing. AKO is a controller; like all K8s controllers, the failure modes are: (a) controller down, (b) controller running but seeing wrong inputs, (c) controller acting but Avi rejecting outputs.

1. `ako status` → controller running, recent reconciles, no panic logs? If not, fix here first
2. `ako ingress check <namespace>` → required annotations present? Common miss: `kubernetes.io/ingress.class`, `aviinfrasetting.ako.vmware.com/name`
3. `ako sync status` → drift between K8s state and Avi state. Drift > a few minutes usually means controller error
4. `ako ingress diagnose <ingress-name>` → AKO's own diagnostic; often pinpoints the issue
5. If sync drifted: `ako sync diff` → review what's missing on Avi side. **Force resync only after** you understand why drift happened — blind resync masks bugs that will recur

### SSL Certificate Expiry Audit

**Judgment**: cert expiry is the most preventable outage in the LB world. Run this regularly, not reactively. The 30-day window is a minimum — for prod, set 60+ to allow renewal lead time.

1. `ssl expiry --days 60` → catch certs expiring within 60 days, not 30; enterprise renewal cycles take 2-4 weeks
2. Cross-reference VS mapping (in output) → identify which apps are at risk; some certs may be unused (orphans, candidates for cleanup)
3. **Decision**: certs marked `unused` (no VS) → propose deletion as part of audit; certs `in_use` → escalate to cert team with VS list and exact expiry date
4. Schedule a follow-up rescan post-renewal (not just rely on cert team confirming)

## Usage Mode

| Scenario | Recommended | Why |
|----------|:-----------:|-----|
| Local/small models (Ollama, Qwen) | **CLI** | ~2K tokens vs ~8K for MCP |
| Cloud models (Claude, GPT-4o) | Either | MCP gives structured JSON I/O |
| Automated pipelines | **MCP** | Type-safe parameters, structured output |
| AKO troubleshooting | **CLI** | Interactive log tailing, Helm diff output |

## MCP Tools (28 — 22 read, 6 write)

| Category | Tools | R/W |
|----------|-------|:---:|
| Virtual Service (3) | `vs_list`, `vs_status` | Read |
| | `vs_toggle` | Write |
| Pool Member (4) | `pool_list`, `pool_members` | Read |
| | `pool_member_enable`, `pool_member_disable` | Write |
| SSL Certificate (2) | `ssl_list`, `ssl_expiry_check` | Read |
| Analytics (2) | `vs_analytics`, `vs_error_logs` | Read |
| Service Engine (2) | `se_list`, `se_health` | Read |
| AKO Pod (4) | `ako_status`, `ako_logs`, `ako_version` | Read |
| | `ako_restart` | Write |
| AKO Config (3) | `ako_config_show`, `ako_config_diff` | Read |
| | `ako_config_upgrade` | Write |
| Ingress Diagnostics (3) | `ako_ingress_check`, `ako_ingress_map`, `ako_ingress_diagnose` | Read |
| Sync Diagnostics (3) | `ako_sync_status`, `ako_sync_diff` | Read |
| | `ako_sync_force` | Write |
| Multi-cluster (2) | `ako_clusters`, `ako_amko_status` | Read |

**Read/write split**: 22 tools are read-only, 6 modify state. Write tools require double confirmation and are audit-logged.

## CLI Quick Reference

```bash
# === Traditional Mode (AVI Controller) ===
vmware-avi vs list [--controller <name>]
vmware-avi vs status <vs-name>
vmware-avi vs enable <vs-name>
vmware-avi vs disable <vs-name>           # double-confirm

vmware-avi pool members <pool-name>
vmware-avi pool enable <pool> <server-ip>
vmware-avi pool disable <pool> <server-ip>  # double-confirm (graceful drain)

vmware-avi ssl list
vmware-avi ssl expiry [--days 30]

vmware-avi analytics <vs-name>
vmware-avi logs <vs-name> [--since 1h]

vmware-avi se list
vmware-avi se health

# === AKO Mode (K8s) ===
vmware-avi ako status [--context <k8s-context>]
vmware-avi ako logs [--tail 100] [--since 30m]
vmware-avi ako restart                    # double-confirm

vmware-avi ako config show
vmware-avi ako config diff
vmware-avi ako config upgrade             # double-confirm + --dry-run default

vmware-avi ako ingress check <namespace>
vmware-avi ako ingress map
vmware-avi ako ingress diagnose <ingress-name>

vmware-avi ako sync status
vmware-avi ako sync diff
vmware-avi ako sync force                 # double-confirm

vmware-avi ako clusters
vmware-avi ako amko status
```

> Full CLI reference: see `references/cli-reference.md`

## Troubleshooting

### "Controller unreachable" error
1. Run `vmware-avi doctor` to verify connectivity
2. Check if the controller address and port are correct in `~/.vmware-avi/config.yaml`
3. For self-signed certs: set `verify_ssl: false` in config.yaml (lab environments only)

### AKO Pod in CrashLoopBackOff
1. Check logs → `vmware-avi ako logs --tail 50`
2. Common causes: wrong controller IP in values.yaml, network policy blocking AKO→Controller, expired credentials
3. Fix config → `vmware-avi ako config show` to inspect, then `vmware-avi ako config upgrade` with corrected values (release auto-discovered — official installs use `--generate-name`; pulls the official Broadcom OCI chart `oci://projects.packages.broadcom.com/ako/helm-charts/ako`)

### Ingress created but no VS on Controller
1. Validate annotations → `vmware-avi ako ingress check <namespace>`
2. Check AKO logs for rejection reason → `vmware-avi ako logs --since 5m`
3. Run sync diff → `vmware-avi ako sync diff` to see if the object is stuck

### Pool member shows "down" after enable
Health monitor may still be failing. Check the actual health status on the Controller side — the member is enabled but unhealthy. Fix the backend service first, then the health status will auto-recover.

### SSL expiry check shows 0 certificates
Verify the controller connection has tenant-level access. Certificates are tenant-scoped in AVI — the configured user may only see certs in their tenant.

### AKO sync force has no effect
Force resync triggers AKO to re-reconcile all K8s objects. If the drift persists, the issue is likely in the K8s resource definition itself (bad annotation, missing secret). Use `vmware-avi ako ingress diagnose` to pinpoint the root cause.

## Setup

```bash
uv tool install vmware-avi
mkdir -p ~/.vmware-avi
vmware-avi init              # generates config.yaml and .env templates
chmod 600 ~/.vmware-avi/.env
vmware-avi doctor            # verify Controller + K8s connectivity
```

> All tools are automatically audited via vmware-policy. Audit logs: `vmware-audit log --last 20`

**Supported versions**: AVI Controller 22.1.x (analytics endpoint quirks fixed in v1.5.11) and 30.x. VCF 9.0 / 9.1 declared compatible (avisdk `>=22.1,<31.0` covers bundled AVI). Python 3.11+. Full table: `references/capabilities.md` → Version Compatibility.

> Full setup guide, security details, AI platform compatibility, and container/Smithery deployment: see `references/setup-guide.md`

## Audit & Safety

All operations are automatically audited via vmware-policy (`@vmware_tool` decorator):
- Every tool call logged to `~/.vmware/audit.db` (SQLite, framework-agnostic)
- Policy rules enforced via `~/.vmware/rules.yaml` (deny rules, maintenance windows, risk levels)
- Destructive operations (`vs_toggle` disable, `pool_member_disable`, `ako_restart`, `ako_config_upgrade`, `ako_sync_force`) require double confirmation
- `ako_config_upgrade` defaults to `--dry-run` mode — user must explicitly confirm to apply
- View recent operations: `vmware-audit log --last 20`

## License

MIT — [github.com/zw008/VMware-AVI](https://github.com/zw008/VMware-AVI)
