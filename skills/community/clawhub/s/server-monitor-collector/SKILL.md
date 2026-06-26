---
name: server-monitor-collector
description: Collect server monitoring data (Zabbix / Prometheus / Alibaba / Tencent / Huawei Cloud), generate CSV/XLSX reports and send via email or Feishu.
triggers:
  - collect server monitoring data
  - server health report
  - host monitoring采集
  - zabbix prometheus monitoring
  - cloud CVM monitoring
  - server daily report cron
  - TC3-HMAC-SHA256 signature
homepage: https://clawhub.ai/skills
metadata:
  {
    "openclaw":
      {
        "emoji": "🖥️",
        "requires": { "bins": ["python3"], "env": ["ZABBIX_URL", "ZABBIX_USER", "ZABBIX_PASSWORD", "FEISHU_CHAT_ID", "HERMES_DIR", "ALIBABA_ACCESS_KEY_ID", "ALIBABA_ACCESS_KEY_SECRET", "ALIBABA_REGION", "TENCENT_SECRET_ID", "TENCENT_SECRET_KEY", "TENCENT_REGION", "HUAWEI_ACCESS_KEY", "HUAWEI_SECRET_KEY", "HUAWEI_REGION", "SMTP_HOST", "SMTP_PORT", "SMTP_FROM", "SMTP_TOKEN", "TARGET_EMAIL", "PROMETHEUS_URL"] },
        "install":
          [
            {
              "id": "scripts",
              "kind": "file",
              "src": "scripts/zabbix_cron.py",
              "label": "Main cron entry point (Zabbix + Cloud + Feishu + Email)"
            },
            {
              "id": "scripts-cloud",
              "kind": "file",
              "src": "scripts/cloud_monitor.py",
              "label": "Multi-cloud collector: Alibaba / Tencent / Huawei"
            },
            {
              "id": "scripts-standalone",
              "kind": "file",
              "src": "scripts/zabbix_monitor.py",
              "label": "Zabbix standalone collector + Excel report generator"
            },
            {
              "id": "scripts-mail",
              "kind": "file",
              "src": "scripts/send_zabbix_report.py",
              "label": "Standalone email sender"
            },
            {
              "id": "hermes-skill",
              "kind": "file",
              "src": "references/zabbix-config.md",
              "label": "Configure data sources in ~/.hermes/.env"
            },
            {
              "id": "cloud-config",
              "kind": "file",
              "src": "references/cloud-config.md",
              "label": "Cloud API credentials: Alibaba / Tencent / Huawei"
            },
            {
              "id": "notification-config",
              "kind": "file",
              "src": "references/notification-config.md",
              "label": "Feishu and email notification setup"
            }
          ]
      }
  }
---

# Server Monitor Collector

Collect server or cloud VM monitoring data, generate formatted Excel reports, and optionally send summaries via email or Feishu/Lark.

## Supported Data Sources

| Source | Auth | Notes |
|--------|------|-------|
| Zabbix | User/Pass or API Token | Host groups, memory, CPU, disk |
| Prometheus | URL only | PromQL queries |
| Alibaba Cloud CMS | AccessKey/SecretKey | ECS, RDS, SLB, EIP metrics |
| Tencent Cloud CAM | SecretID/Key | TC3-HMAC-SHA256 signature |
| Huawei Cloud IAM | AccessKey/SecretKey | IAM Token auth |

Data sources are **auto-detected** from `.env` — configure credentials for any combination and they will all be collected.

## Setup

### 1. Configure Environment

Create/edit `~/.hermes/.env`. Only configure the sources you need:

```bash
# --- Zabbix (pick one auth method) ---
ZABBIX_URL=https://zabbix.example.com/api_jsonrpc.php
ZABBIX_USER=Admin
ZABBIX_PASSWORD=your_password
# ZABBIX_TOKEN=your_api_token  # optional, takes priority over password

# --- Alibaba Cloud ---
ALIBABA_ACCESS_KEY_ID=your_key_id
ALIBABA_ACCESS_KEY_SECRET=your_secret
ALIBABA_REGION=cn-hangzhou
# ALIBABA_METRICS=CPUUtilization,MemoryUtilization,InternetInRate  # optional

# --- Tencent Cloud ---
TENCENT_SECRET_ID=your_secret_id
TENCENT_SECRET_KEY=your_secret_key
TENCENT_REGION=ap-shanghai

# --- Huawei Cloud ---
HUAWEI_ACCESS_KEY=your_access_key
HUAWEI_SECRET_KEY=your_secret_key
HUAWEI_REGION=cn-east-3

# --- Notifications ---
FEISHU_CHAT_ID=oc_xxxx         # optional
SMTP_HOST=smtp.example.com      # optional, omit to skip email
SMTP_PORT=465
SMTP_FROM=alarm@example.com
SMTP_TOKEN=your_token
TARGET_EMAIL=admin@example.com

# --- Report options ---
# TOPN: show top N hosts by memory+CPU score, 0=off (default: 50)
TOPN=50
```

### 2. Install Dependencies

**Zabbix / Prometheus** — no extra deps:
```bash
python3 zabbix_cron.py
```

**Alibaba Cloud** — needs SDK (use `uv` since venv has no pip):
```bash
uv run --with aliyun-python-sdk-core --with aliyun-python-sdk-cms \
  python3 cloud_monitor.py
```

**Tencent / Huawei** — pure Python, only `httpx` needed:
```bash
uv run --with httpx python3 cloud_monitor.py
```

### 3. Run Once (Manual Test)

```bash
python3 zabbix_cron.py
```

Expected output:
- `~/.hermes/cron/output/zabbix_monitor.csv`
- `~/.hermes/cron/output/zabbix_monitor.xlsx` (one sheet per host group + overview + TOP sheet)

### 4. Schedule Daily Report

```bash
hermes cron create \
  --name "Daily Server Health Report" \
  --script zabbix_cron.py \
  --schedule "30 9 * * *"
```

## Output Format

### CSV
- UTF-8-BOM encoding — opens correctly in Windows Excel without garbled characters
- Columns: `主机组`, `主机名`, `IP`, `内存可用(GB)`, `内存总量(GB)`, `内存占用率(%)`, `CPU占用率(%)`

### XLSX
- **总览** sheet: summary table with host group stats and alarm counts
- **Group sheets**: one per host group, sorted by memory usage descending
- **TOP50(内存+CPU)** sheet: top 50 hosts across all groups by combined memory+CPU score
- Cell coloring: `🔴 ≥80%` red, `🟠 ≥60%` orange, `🟡 ≥40%` yellow

## Auto-Detection Logic

Scripts detect which sources to use based on which env vars are set:

| Env var present | Data source used |
|----------------|-----------------|
| `ZABBIX_URL` | Zabbix API |
| `ALIBABA_ACCESS_KEY_ID` | Alibaba Cloud CMS (SDK) |
| `TENCENT_SECRET_ID` | Tencent Cloud CAM (TC3签名) |
| `HUAWEI_ACCESS_KEY` | Huawei Cloud IAM (Token) |
| `PROMETHEUS_URL` | Prometheus PromQL |

## Zabbix Host Group Exclusion

These groups are excluded by default (set in `EXCLUDE_GROUPS` in script):
- `Templates*` — template groups
- `Discovered hosts` — Zabbix auto-discovery

## Key Zabbix Item Keys

| Key | Description |
|-----|-------------|
| `vm.memory.size[available]` | Memory available (bytes) |
| `vm.memory.size[total]` | Memory total (bytes) |
| `system.cpu.util` | CPU utilization (%) |
| `vfs.fs.size[/,pused]` | Root disk usage (%) |

## Alarm Thresholds

| Metric | Warning | Alarm |
|--------|---------|-------|
| Memory usage | ≥40% yellow | ≥60% orange, ≥80% red |
| CPU usage | ≥40% yellow | ≥60% orange, ≥80% red |

## Feishu Message Format

Markdown card sent to `FEISHU_CHAT_ID` containing:
- Report timestamp, total hosts, group count
- Top 20 hosts with memory ≥60% or CPU ≥60%
- Color-coded: 🔴≥80%, 🟠≥60%, 🟡≥40%

## Email Format

- Subject: `服务器监控报告 YYYY-MM-DD HH:MM`
- Body: HTML summary matching the Feishu card
- Attachment: `zabbix_monitor.xlsx`

## References

- `references/zabbix-config.md` — Zabbix API details, item keys, auth options
- `references/notification-config.md` — Feishu and email SMTP setup, common providers
- `references/cloud-config.md` — Alibaba / Tencent / Huawei API endpoints, namespaces, SDK usage

## Guardrails

- **Never hardcode credentials** — always use `~/.hermes/.env`
- **Never print full credentials** in logs or chat
- **Never place scripts in web-accessible directories**
- If Zabbix host has no Agent — memory metrics show `N/A`, CPU still works
- Alibaba Cloud `MemoryUtilization` requires Cloud Monitor Agent installed on ECS instance
