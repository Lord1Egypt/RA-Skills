---
name: zhihu-aiops
description: Use this skill when working with the Zhihu AIOps / 智护运维平台, including asset management, CMDB discovery, monitoring, alarm dashboards, Categraf SNMP metrics in VictoriaMetrics, managed asset inspection reports, and adding OS monitoring assets. This first release provides reference-guided workflows and API documentation; executable CLI helpers will be added in a later version.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - ZHIHU_API_URL
        - ZHIHU_USER
        - ZHIHU_PASSWORD
        - VM_URL
      bins:
        - curl
        - python3
    primaryEnv: ZHIHU_API_URL
---

# Zhihu AIOps Skill

This skill provides workflows and API references for the 智护运维平台 / Zhihu AIOps platform.

Use it for:

- Querying platform assets, asset models, asset types, and managed devices.
- Creating operating-system monitoring assets after connectivity checks.
- Querying dashboard and alarm summaries.
- Working with CMDB / asset discovery scan tasks and scan results.
- Querying VictoriaMetrics and Categraf SNMP `snmp_*` metrics.
- Generating managed asset inspection reports.

## Configuration

Set these environment variables before calling platform APIs:

```bash
export ZHIHU_API_URL="http://zhihu-server:48080/admin-api"
export ZHIHU_USER="admin"
export ZHIHU_PASSWORD="your-password"
export VM_URL="http://zhihu-metric:9090"
```

Do not hard-code customer IPs, test-environment URLs, usernames, passwords, or API keys into prompts or generated scripts. Prefer environment variables.

## Core Workflow

1. Read the relevant reference file from `references/` based on the user's goal.
2. Login to the Zhihu platform before calling protected platform APIs.
3. Send `Authorization: Bearer <accessToken>` with platform requests unless the target environment expects the raw token format.
4. For managed assets, query asset models first when the model ID is unknown, then call `/cqt/asset-info/page` with the correct `modelId` and `modelCode`.
5. For SNMP/network/security/storage device metrics, use VictoriaMetrics `snmp_*` metrics collected by Categraf, not Zabbix.
6. For inspection reports, combine platform managed asset data with VictoriaMetrics/SNMP data only when realtime metric status is requested.

## Reference Map

- Asset center APIs: `references/api_asset.md`
- CMDB discovery APIs: `references/api_cmdb.md`
- Dashboard and alarm summary APIs: `references/api_dashboard.md`
- Monitor center APIs: `references/api_monitor.md`
- VictoriaMetrics APIs: `references/api_victoriametrics.md`
- Categraf SNMP metrics: `references/api_snmp_metrics.md`
- Add OS monitoring workflow: `references/add-os-monitor.md`
- Managed asset inspection workflow: `references/inspection-run.md`

## Common Tasks

### Query Managed Assets

Read `references/api_asset.md`. If the user asks for concrete assets rather than model definitions, use `/cqt/asset-info/page`. For known managed inspection models, use the model information in `references/inspection-run.md`.

### Generate Managed Asset Inspection Report

Read `references/inspection-run.md`, then query these categories as needed:

- Security device: `modelId=254`, `modelCode=securitydevice`
- Network device: `modelId=185`, `modelCode=networkdevice`
- Terminal device: `modelId=260`, `modelCode=terminaldevice`
- Storage device: `modelId=261`, `modelCode=storagedevice`
- Database: `modelId=183`, `modelCode=storagebase`
- Operating system: `modelId=195`, `modelCode=operatesystem`

### Query SNMP Metrics

Read `references/api_snmp_metrics.md`. Use `VM_URL` and VictoriaMetrics APIs:

- `/api/v1/series` for metric discovery.
- `/api/v1/query` for instant queries.
- `/api/v1/query_range` for trends.

Prefer `snmp_*` metrics for network devices, security devices, storage devices, switches, routers, firewalls, and other SNMP-managed assets.

### Add OS Monitoring

Read `references/add-os-monitor.md`. Required user inputs are target IP, port, username, password, and monitor name. Login first, resolve the operating-system model/items dynamically, test connectivity, then create the asset.

## Current Limitations

This first ClawHub package is documentation-first and registration-ready. It does not yet include a production CLI wrapper. When deterministic execution is required, implement scripts in `scripts/` in the next phase, for example:

```bash
python3 scripts/zhihu_cli.py login
python3 scripts/zhihu_cli.py asset-page --model-code networkdevice
python3 scripts/zhihu_cli.py inspect-managed-assets --scope all
python3 scripts/zhihu_cli.py snmp-discover
python3 scripts/zhihu_cli.py vm-query --query 'up'
```
