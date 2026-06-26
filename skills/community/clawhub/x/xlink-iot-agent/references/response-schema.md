# Xlink API Response Schemas

## Standard Response Format

Xlink API responses follow two formats depending on the endpoint:

### Standard Format (most endpoints)

```json
{
  "msg": "OK",
  "code": 200,
  "status": 200,
  "data": { ... }
}
```

### Simplified Format (some endpoints)

```json
{
  "count": 100,
  "list": [ ... ]
}
```

Some endpoints return a simplified “data object” directly (no `code/status/msg/data` wrapper), for example:

```json
{
  "thing_id": "45281011",
  "code": "200",
  "msg": "ok",
  "output": {},
  "command_id": "0ajskjska092"
}
```

## Error Response

```json
{
  "msg": "Error message",
  "code": 4001002,
  "status": 400,
  "error": {
    "msg": "Detailed error",
    "code": 4001002
  },
  "data": null
}
```

## API Response Schemas

### Device Overview (`/v3/device-service/devices/overview`)

```json
{
  "msg": "OK",
  "code": 200,
  "status": 200,
  "data": {
    "total": 120034,
    "online": 87433,
    "activated": 110223,
    "online_rate": 0.72,
    "activated_rate": 0.91
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `total` | int | Total devices |
| `online` | int | Online count |
| `activated` | int | Activated count |
| `online_rate` | float | Online rate (0-1) |
| `activated_rate` | float | Activated rate (0-1) |

### Device List (`/v2/devices/def-filter/aggregates`)

```json
{
  "count": 7823,
  "list": [
    {
      "device": {
        "id": 1696499516,
        "name": "变压器 0111",
        "mac": "725DCAB04F86",
        "product_id": "160042bc328303e9160042bc3283f605",
        "is_active": true,
        "create_time": "2020-01-11T11:34:32.662Z"
      },
      "online": {
        "is_online": false
      },
      "vdevice": {
        "last_login": "2025-09-23T11:57:23.753Z",
        "online_count": 45291063
      }
    }
  ]
}
```

This endpoint is documented as a simplified response (no wrapper).

### Device Latest Attributes (`/v2/device-shadow/device-attribute-query`)

```json
{
  "msg": "OK",
  "code": 200,
  "status": 200,
  "data": {
    "count": 1,
    "tmls": {
      "16a8b0d3133f000116a8b0d3133fc801": [
        {
          "index": 0,
          "field_name": {"cn": "温度", "en": "temperature"},
          "type": {"type": "float"},
          "symbol": "℃"
        }
      ]
    },
    "list": [
      {
        "device_id": 938245653,
        "product_id": "16a8b0d3133f000116a8b0d3133fc801",
        "is_online": true,
        "last_login": "2026-02-11T15:00:55.903Z",
        "last_update": "2026-02-11T15:06:08.921Z",
        "online_count": 127,
        "conn_prot": 2,
        "attributes": [
          {"index": 0, "field": "temperature", "value": 1.0, "time": 1770793568921}
        ]
      }
    ]
  }
}
```

### Device Alert Statistics (`/v3/alert/statistics`)

```json
{
  "msg": "OK",
  "code": 200,
  "status": 200,
  "data": {
    "list": [
      {
        "time": "2026-02-11T07:00:00.000",
        "added_alert_num": 231,
        "history_alert_num": 8433,
        "device_alert_num": 182,
        "device_alert_rate": 0.01
      }
    ]
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `time` | String | Timestamp (ISO 8601) |
| `added_alert_num` | int | New alerts |
| `history_alert_num` | int | Total alerts |
| `device_alert_num` | int | Device alerts |
| `device_alert_rate` | float | Alert rate (0-1) |

### Alert Overview (`/v3/alert/overview`)

```json
{
  "msg": "OK",
  "code": 200,
  "status": 200,
  "data": {
    "added_alert_num": 0,
    "history_alert_num": 143,
    "device_alert_num": 112,
    "device_alert_rate": 0.014316758276875879
  }
}
```

### Device Statistics Trend (`/v3/device-service/devices/statistics`)

```json
{
  "msg": "OK",
  "code": 200,
  "status": 200,
  "data": {
    "list": [
      {
        "time": "2026-02-11T07:00:00.000Z",
        "total": 120034,
        "online": 87433,
        "activated": 110223,
        "online_rate": 0.72,
        "activated_rate": 0.91
      }
    ]
  }
}
```

### Device Attribute History (`/v2/snapshot/device-attribute`)

```json
{
  "count": 150,
  "tml": [
    {
      "index": 0,
      "field_name": { "cn": "温度", "en": "temperature" },
      "type": { "type": "float" },
      "symbol": "℃"
    }
  ],
  "list": [
    {
      "0": 25.5,
      "id": "snapshot-xxx",
      "device_id": 1000,
      "snapshot_date": "2015-10-09T08:15:40.843Z",
      "rule_id": "rule-001"
    }
  ]
}
```

### Event Instances (`/v2/service/events/all-instances`)

```json
{
  "status": 200,
  "code": 200,
  "msg": "OK",
  "data": {
    "count": 53536,
    "list": [
      {
        "id": "69b130d838cb6c0038e90f57",
        "application": "VideoSecurity",
        "storage_time": "2026-03-11T17:07:37.146Z",
        "base": {
          "status": 1,
          "name": "人员离岗",
          "desc": "【AI】12-3-B 区南门门卫发生人员离岗",
          "create_time": "2026-03-11T17:07:37.116Z",
          "process_time": null,
          "device_id": "device-xxx",
          "device_name": "广州保利罗兰",
          "device_mac": "725DCAB04F86",
          "project_id": "proj-xxx",
          "project_name": "项目 A",
          "processed_way": -1,
          "priority": 2,
          "classification_id": "class-xxx",
          "rank_id": "rank-xxx"
        }
      }
    ]
  }
}
```

| Status | Description |
|--------|-------------|
| `1` | Pending (待处理) |
| `2` | Processing (处理中) |
| `3` | Processed (已处理) |

| Processed Way | Description |
|---------------|-------------|
| `-1` | Unprocessed (未处理) |
| `1` | Device Debug (设备调试) |
| `2` | Real Fault (真实故障) |
| `3` | False Alarm (误报) |
| `4` | Other (其他) |
| `5` | Transfer to Work Order (转工单) |
| `6` | Suppressed (抑制) |
| `7` | Auto Recovered (自动恢复) |

### Device Control (`/v2/device-shadow/service_invoke`)

```json
{
  "thing_id": "45281011",
  "code": "200",
  "msg": "ok",
  "output": {},
  "command_id": "0ajskjska092"
}
```

This endpoint is documented as a simplified response (direct data object).

| Code | Description |
|------|-------------|
| `200` | Success - device responded |
| `202` | Device offline - command not sent |
| `408` | Connection closed - device sleeping |
| `503` | Control failed - no response |

## Common Error Codes

| Code | Description |
|------|-------------|
| `200` | Success |
| `4001001` | Bad request |
| `4001002` | Missing required field |
| `4031003` | Invalid access token |
| `4041001` | Resource not found |
| `40428001` | Device not found |
| `40428009` | Product thing model not defined |
| `40075001` | Command cache write QPS limit |
| `40075004` | Command cache TTL exceeded |
| `429` | Rate limit exceeded |
| `500` | Internal server error |

## Pagination

List endpoints support pagination:

- `offset` - Pagination offset (default: 0)
- `limit` - Page size (varies by endpoint, typically 10-100)

Example:
```json
{
  "offset": 0,
  "limit": 20
}
```

## Time Format

All timestamps use ISO 8601 format:

```
2026-02-11T15:00:55.903Z
yyyy-MM-dd'T'HH:mm:ss.SSS'Z'
```
