# VMware AVI CLI Reference

Complete command reference for the `vmware-avi` CLI (v1.4.0).

## Global Commands

| Command | Description | Flags |
|---------|-------------|-------|
| `vmware-avi doctor` | Run environment diagnostics (Controller connectivity, kubeconfig, SDK availability) | -- |
| `vmware-avi init` | Generate `config.yaml` and `.env` templates in `~/.vmware-avi/` | -- |
| `vmware-avi config` | Show current configuration (passwords masked) | -- |

## Virtual Service Commands (`vmware-avi vs`)

| Command | Description | Arguments / Flags |
|---------|-------------|-------------------|
| `vmware-avi vs list` | List all Virtual Services | `--controller <name>` (optional, use a specific controller) |
| `vmware-avi vs status <name>` | Show VS status details (VIP, health, pool binding) | `<name>` (required) |
| `vmware-avi vs enable <name>` | Enable a Virtual Service | `<name>` (required) |
| `vmware-avi vs disable <name>` | Disable a Virtual Service | `<name>` (required). **Double-confirm required.** |

## Pool Member Commands (`vmware-avi pool`)

| Command | Description | Arguments / Flags |
|---------|-------------|-------------------|
| `vmware-avi pool members <pool>` | List pool members and health status | `<pool>` (required) |
| `vmware-avi pool enable <pool> <server-ip>` | Enable a pool member (restore traffic) | `<pool>` (required), `<server-ip>` (required) |
| `vmware-avi pool disable <pool> <server-ip>` | Disable a pool member (graceful drain) | `<pool>` (required), `<server-ip>` (required). **Double-confirm required.** |

## SSL Certificate Commands (`vmware-avi ssl`)

| Command | Description | Arguments / Flags |
|---------|-------------|-------------------|
| `vmware-avi ssl list` | List all SSL certificates | -- |
| `vmware-avi ssl expiry` | Check certificates expiring within N days | `--days <N>` (default: 30) |

## Service Engine Commands (`vmware-avi se`)

| Command | Description | Arguments / Flags |
|---------|-------------|-------------------|
| `vmware-avi se list` | List all Service Engines: name, mgmt IP, operational status, SE group (status from the `serviceengine-inventory` endpoint, config + runtime merged) | -- |
| `vmware-avi se health` | Check Service Engine health: per-SE operational status + connected-VS counts (placement map from `virtualservice-inventory`) | -- |

## Analytics Commands

| Command | Description | Arguments / Flags |
|---------|-------------|-------------------|
| `vmware-avi analytics <vs-name>` | Show VS analytics: L4 bandwidth/connections + L7 client transaction latency (`l7_client.avg_client_txn_latency`), response errors, total responses | `<vs-name>` (required) |
| `vmware-avi logs <vs-name>` | Show VS request error logs (HTTP status ≥ 400, filter `ge(response_code,400)`) | `<vs-name>` (required), `--since <range>` (default: `1h`, e.g. `30m`, `2h`) |

## AKO Pod Commands (`vmware-avi ako`)

| Command | Description | Arguments / Flags |
|---------|-------------|-------------------|
| `vmware-avi ako status` | Check AKO pod status (Running, CrashLoopBackOff, etc.) | `--context <k8s-context>` (optional) |
| `vmware-avi ako logs` | View AKO pod logs | `--tail <N>` (default: 100), `--since <range>` (e.g. `30m`), `--context <k8s-context>` (optional) |
| `vmware-avi ako restart` | Restart AKO pod by deleting it (its StatefulSet recreates it) | `--context <k8s-context>` (optional). **Double-confirm required.** |
| `vmware-avi ako version` | Show AKO version info (image tag, Helm chart version) | `--context <k8s-context>` (optional) |

## AKO Config Commands (`vmware-avi ako config-*`)

| Command | Description | Arguments / Flags |
|---------|-------------|-------------------|
| `vmware-avi ako config-show` | Show current AKO Helm values.yaml (release auto-discovered via `helm list` — official installs use `--generate-name`) | -- |
| `vmware-avi ako config-diff` | Show pending Helm changes (diff against the official Broadcom OCI chart `oci://projects.packages.broadcom.com/ako/helm-charts/ako`) | -- |
| `vmware-avi ako config-upgrade` | Helm upgrade the discovered AKO release from the official Broadcom OCI chart with `--reuse-values` | `--dry-run` / `--no-dry-run` (default: `--dry-run`). **Double-confirm required for actual apply.** |

## AKO Ingress Commands (`vmware-avi ako ingress-*`)

| Command | Description | Arguments / Flags |
|---------|-------------|-------------------|
| `vmware-avi ako ingress-check <namespace>` | Validate Ingress annotations in a namespace | `<namespace>` (required) |
| `vmware-avi ako ingress-map` | Show Ingress to VS mapping across all namespaces | -- |
| `vmware-avi ako ingress-diagnose <name>` | Diagnose why an Ingress has no corresponding VS | `<name>` (required), `--namespace <ns>` (default: `default`) |

## AKO Sync Commands (`vmware-avi ako sync-*`)

| Command | Description | Arguments / Flags |
|---------|-------------|-------------------|
| `vmware-avi ako sync-status` | Check K8s-Controller sync status | -- |
| `vmware-avi ako sync-diff` | Show K8s-Controller inconsistencies (objects in K8s but not on Controller, or vice versa) | -- |
| `vmware-avi ako sync-force` | Force AKO to re-reconcile all K8s objects | **Double-confirm required.** |

## AKO Multi-cluster Commands (`vmware-avi ako`)

| Command | Description | Arguments / Flags |
|---------|-------------|-------------------|
| `vmware-avi ako clusters` | List all clusters with AKO deployed | -- |
| `vmware-avi ako amko-status` | Show AMKO (multi-cluster GSLB) status | -- |

## Destructive Operations Summary

The following commands require double confirmation before execution:

| Command | Risk | Reason |
|---------|------|--------|
| `vs disable` | Medium | Takes a VS offline, impacts client traffic |
| `pool disable` | Medium | Drains traffic from a pool member |
| `ako restart` | High | Restarts AKO pod, temporarily pauses K8s-Controller sync |
| `ako config-upgrade` | High | Modifies AKO Helm release, may change load-balancing behavior |
| `ako sync-force` | Medium | Forces full re-reconciliation, may cause brief churn |

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `VMWARE_AVI_CONFIG` | Override config file path (default: `~/.vmware-avi/config.yaml`) |
| `<CONTROLLER_NAME>_PASSWORD` | AVI Controller password (e.g. `PROD_AVI_PASSWORD`) |

## Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Failure (connectivity error, missing config, check failed) |
