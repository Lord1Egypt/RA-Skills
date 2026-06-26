---
name: xlink-iot-agent
description: Xlink IoT Agent - Query IoT devices and events via Xlink Gateway API. Provides device overview, device list, event instance queries, and alert statistics. Use when managing IoT devices and monitoring events on the XLink IoT platform.
version: 0.1.0
metadata:
  openclaw:
    requires:
      env:
        - XLINK_APP_ID
        - XLINK_APP_SECRET
        - XLINK_API_GROUP
    primaryEnv: XLINK_APP_ID
---

# Xlink IoT Agent

Control and query IoT devices and events on the XLink IoT platform via GatewayAppClient with signature-based authentication.

## When to Use

### ✅ Use This Skill When

- Querying device status and statistics on XLink IoT platform
- Monitoring device alerts and events
- Batch querying device attributes (latest values or historical data)
- Remote control of IoT devices (invoking thing model services)
- Filtering device data by project/product

### ❌ Do Not Use This Skill For

- Other IoT platforms (AWS IoT, Azure IoT, Alibaba Cloud IoT, etc.)
- Direct local device control (not via XLink IoT platform)
- Historical weather data or severe weather alerts (use weather skill)
- Non-IoT related device management tasks

---

## Quick Start

### 1. Set Environment Variables

```bash
export XLINK_BASE_URL="https://api-gw.xlink.cn"
export XLINK_APP_ID="your-app-id"
export XLINK_APP_SECRET="your-app-secret"
export XLINK_API_GROUP="your-group-id"
```

### 2. Run Commands

```bash
cd /path/to/xlink-iot-agent

# Device overview
python scripts/xlink_api.py overview

# Pending events
python scripts/xlink_api.py event-instances --status 1 --limit 20

# Alert statistics (last 24 hours)
python scripts/xlink_api.py alert-statistics

# Device control
python scripts/xlink_api.py device-control \
  --thing-id 10299402 \
  --service device_attribute_set_service \
  --input '{"PowerSwitch":true}'
```

---

## Core Commands

| Command | Function | Example |
|------|------|------|
| `overview` | Device overview statistics | `python scripts/xlink_api.py overview` |
| `device-list` | Device list query | `python scripts/xlink_api.py device-list --limit 20` |
| `device-trend` | Device statistics trend | `python scripts/xlink_api.py device-trend --start-time "2026-03-17T00:00" --end-time "2026-03-24T23:59"` |
| `device-history` | Device attribute history snapshots | `python scripts/xlink_api.py device-history --device-ids 300513220,501548135` |
| `device-latest` | Device latest attributes | `python scripts/xlink_api.py device-latest --device-ids 300513220,501548135` |
| `device-control` | Device control | `python scripts/xlink_api.py device-control --thing-id 10299402 --service device_attribute_set_service --input '{"PowerSwitch":true}'` |
| `alert-overview` | Alert overview | `python scripts/xlink_api.py alert-overview` |
| `alert-statistics` | Alert time-series statistics | `python scripts/xlink_api.py alert-statistics --interval hour` |
| `event-instances` | Event instance query | `python scripts/xlink_api.py event-instances --status 1 --limit 20` |

---

## Common Query Examples

### Device Overview

```bash
python scripts/xlink_api.py overview
```

Output:
```
==================================================
📊 XLINK Device Overview
==================================================

   📱 Total Devices:    7823
   🟢 Online:           143 (1.8%)
   ✅ Activated:        6756 (86.4%)
   ⚫ Offline:          7680
   ⏸️  Not Activated:   1067
```

### Pending Events

```bash
python scripts/xlink_api.py event-instances --status 1 --limit 20
```

### Alert Overview

```bash
python scripts/xlink_api.py alert-overview
```

### Device List (with Filtering)

```bash
# Filter by project
python scripts/xlink_api.py device-list \
  --query '{"logic":"AND","device":{"project_id":{"$eq":"XJA1JJAJA"}}}' \
  --limit 20

# JSON output
python scripts/xlink_api.py device-list --limit 20 --json
```

### Device Control

```bash
# Set attributes
python scripts/xlink_api.py device-control \
  --thing-id 10299402 \
  --service device_attribute_set_service \
  --input '{"ColorTemperature": 8}'

# With command cache (10 minutes)
python scripts/xlink_api.py device-control \
  --thing-id 10299402 \
  --service device_attribute_set_service \
  --input '{"Brightness": 100}' \
  --ttl 600
```

**Control Response Codes:**
| Code | Description |
|------|-------------|
| `200` | ✅ Success - device responded |
| `202` | ⏸️ Device offline - command not sent |
| `408` | ⚠️ Connection closed - device sleeping |
| `503` | ❌ Control failed |

---

## Python API

```python
import sys
sys.path.insert(0, "scripts")
from xlink_api import XlinkIoTClient

# Initialize (reads from environment variables)
client = XlinkIoTClient()

# Device overview
overview = client.get_device_overview(project_id="ab582")

# Device list
devices = client.get_device_list(limit=50)

# Alert statistics
alerts = client.get_alert_statistics(interval="hour")

# Event instances
events = client.get_event_instances(status=[1], limit=20)

# Device control
result = client.control_device(
    thing_id="10299402",
    service="device_attribute_set_service",
    input_params={"PowerSwitch": True}
)
```

---

## Detailed Documentation

Complete CLI command reference, parameter descriptions, and API documentation:

- [`references/cli-reference.md`](references/cli-reference.md) - Complete CLI command reference
- [`references/api-auth.md`](references/api-auth.md) - Authentication mechanism and security
- [`references/api-doc.md`](references/api-doc.md) - Complete API documentation
- [`references/response-schema.md`](references/response-schema.md) - Response format definitions

---

## Error Handling

| Status | Description | Solution |
|------|------|----------|
| `401 Unauthorized` | Invalid credentials | Check App ID/Secret |
| `403 Forbidden` | Access denied | Verify Group ID and permissions |
| `404 Not Found` | Resource not found | Check endpoint path or resource ID |
| `429 Too Many Requests` | Rate limited | Implement exponential backoff retry |
| `500 Server Error` | Server error | Retry later |

---

## Best Practices

1. **Use pagination** - For large datasets, use `--offset` and `--limit`
2. **Filter early** - Apply filters (status, device, time) to reduce data transfer
3. **Cache results** - Device status changes infrequently; cache for 30-60 seconds
4. **Handle rate limits** - Implement exponential backoff for 429 errors
5. **JSON output for scripting** - Use `--json` for programmatic parsing
6. **Debug mode** - Use `--debug` for troubleshooting
