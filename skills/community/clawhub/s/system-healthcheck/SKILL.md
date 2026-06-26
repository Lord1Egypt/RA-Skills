---
name: system-healthcheck
description: Three-tier system health monitoring (L1/L2/L3) with heartbeat mechanism. Zero external dependencies, i18n support, console output only.
version: 1.0.0
author: "@个贷资产团队"
tags: [monitoring, healthcheck, cron, devops, i18n]
dependencies: []
config_required: true
platforms: [linux, macos]
license: MIT
---

# system-healthcheck

**Three-tier system health monitoring for OpenClaw**

[English](README.md) | [简体中文](README.zh-CN.md)

---

## Features

- **L1 Fast Check** (<200ms): Definition file existence check
- **L2 Hourly Check** (<5s): System resources, services, logs
- **L3 Daily Audit** (<60s): Comprehensive system audit
- **Heartbeat Mechanism**: Quiet when healthy, alert on issues
- **i18n Support**: Auto-detect language (en/zh-CN)
- **Zero External Dependencies**: Works out of the box

---

## Installation

```bash
clawhub install system-healthcheck
```

Or manually:

```bash
git clone https://github.com/your-username/system-healthcheck.git ~/.openclaw/skills/system-healthcheck
```

---

## Quick Start

### 1. L1 Fast Check (Manual)

```bash
cd ~/.openclaw/skills/system-healthcheck
python scripts/l1_fast_check.py
```

### 2. L2 Hourly Check (Manual)

```bash
python scripts/l2_hourly_check.py
```

### 3. Setup Crontab

```bash
cat templates/crontab_example.txt
# Copy and edit crontab
crontab -e
```

### 4. Heartbeat Check

```bash
python scripts/heartbeat.py
```

---

## Configuration

Edit `config/default_config.yaml`:

```yaml
# Internationalization
i18n:
  auto_detect: true  # Auto-detect system language
  # locale: zh-CN    # Or specify manually

# Thresholds
thresholds:
  disk_warning: 80      # Disk warning (%)
  disk_critical: 95     # Disk critical (%)
  memory_warning_mb: 500  # Memory warning (MB)
  log_size_mb: 100      # Log size warning (MB)

# Heartbeat
heartbeat:
  enabled: true
  work_hours_start: 9
  work_hours_end: 18
  quiet_on_ok: true  # Silent when all OK
```

---

## Output Examples

### L2 Hourly Check

```
🦞 System Health Check · 2026-03-23 09:00:00

✅ Disk Usage: 45% (threshold: 80%)
✅ Memory Usage: 1.2GB / 8GB
✅ Cron Service: Running
✅ OpenClaw Gateway: Healthy
✅ Log Files: 12MB

━━━━━━━━━━━━━━━━━━━━━━━━
✅ All checks passed
Duration: 1.2s
```

### Heartbeat (All OK)

```
HEARTBEAT_OK
```

### Heartbeat (Issues Detected)

```
🦞 Heartbeat Check · 2026-03-23 14:30:00

⚠️ Disk Usage: 85% (exceeds 80%)
✅ Memory Usage: 2.1GB / 8GB
...
```

---

## Scripts

| Script | Purpose | Frequency |
|--------|---------|-----------|
| `l1_fast_check.py` | Definition files check | Before conversations |
| `l2_hourly_check.py` | System health check | Hourly (cron) |
| `l3_daily_audit.py` | Comprehensive audit | Daily 08:00 (cron) |
| `heartbeat.py` | Work-hours heartbeat | Every 30min (cron) |

---

## CLI Options

```bash
# JSON output
python scripts/l2_hourly_check.py --json

# Quiet mode (exit code only)
python scripts/l2_hourly_check.py --quiet

# Force output (heartbeat)
python scripts/heartbeat.py --force
```

---

## Exit Codes

- `0`: All checks passed
- `1`: One or more checks failed

---

## Internationalization

Supported languages:
- `en` - English
- `zh-CN` - 简体中文

Auto-detected from system locale. Override with:

```bash
export OPENCLAW_LOCALE=zh-CN
python scripts/l2_hourly_check.py
```

---

## Requirements

- Python 3.8+
- Linux or macOS
- No external dependencies (optional: `rich` for colorful output, `pyyaml` for config)

---

## License

MIT

---

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.

---

## Changelog

### v1.0.0 (2026-03-23)
- Initial release
- L1/L2/L3 checks
- Heartbeat mechanism
- i18n support (en/zh-CN)
