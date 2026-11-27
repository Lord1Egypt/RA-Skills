# 北向接口库（Python / Node.js）

技能自带、零第三方依赖，一个接口一个方法。加载技能后可直接 import：

```python
import sys; sys.path.insert(0, "lib")
from north_client import NorthClient
c = NorthClient.from_env()
c.list_devices(max_results=5)
```

```js
import { NorthClient } from "./lib/north_client.mjs";
const c = await NorthClient.fromEnv();
await c.listDevices({ maxResults: 5 });
```

## 认证

`AIOT_TOKEN`（JWT）｜`AIOT_ACCOUNT` + `AIOT_PASSWORD`（自动登录，401 自动重登）｜`AIOT_API_KEY`（`X-API-Key`）

## 接口 ↔ 方法对照

| 接口 | Python | JS | CLI |
|---|---|---|---|
| `POST /auth/login` | `login()` | `login()` | — |
| `GET /auth/profile` | `profile()` | `profile()` | `whoami` |
| `GET /open/account` | `account_summary()` | `accountSummary()` | `account` |
| `GET /open/device/list` | `list_devices()` | `listDevices()` | `devices` |
| `GET /open/device/{id}` | `get_device()` | `getDevice()` | `device` |
| `GET /open/device/stats` | `device_stats()` | `deviceStats()` | `stats` |
| `GET /open/device/{id}/telemetry` | `telemetry()` | `telemetry()` | `telemetry` |
| `GET /open/device/{id}/history` | `history()` | `history()` | `history` |
| `GET /open/device/{id}/aggregate` | `aggregate()` | `aggregate()` | `aggregate` |
| `GET /open/device/{id}/backfill-logs` | `backfill_logs()` | `backfillLogs()` | `backfill-logs` |
| `POST /open/device/{id}/command` | `send_command()` | `sendCommand()` | `command` |
| `GET /open/command/list` | `list_commands()` | `listCommands()` | `commands` |
| `GET /open/command/{id}` | `get_command()` | `getCommand()` | `command-detail` |
| `GET /open/alarm/list` | `list_alarms()` | `listAlarms()` | `alarms` |
| `GET /open/product/list` | `list_products()` / `find_product()` | `listProducts()` / `findProduct()` | `products` |
| `GET /open/gateway/ports` | `gateway_ports()` | `gatewayPorts()` | `ports` |
| `PATCH /open/product/{id}/metric/{key}` | `update_metric()` | `updateMetric()` | `metric` |
| `PUT /open/product/{id}/metrics-config` | `update_metrics_config()` | `updateMetricsConfig()` | `metrics-config` |
| `POST /open/product/{id}/clean-metrics` | `clean_metrics()` | `cleanMetrics()` | `clean-metrics` |

Python 还提供 `client.devices.* / commands.* / alarms.* / products.*` 兼容写法。

## 错误与限频

- 业务码非 0 抛 `NorthError(code, status, body)`；429 会附带限频提示。
- 用户配额 = 基础配额 + 设备数 × 每台追加（次/秒）；写接口（POST/PUT/DELETE）按 3 倍计。
- 查询配额本身也受限速约束；轮询多台设备时把间隔调大。

## 离线自测

```bash
python tests/test_north.py                     # 起 mock，跑 25 项
# JS：先起 mock，再跑
python tests/mock_north.py 18082
node tests/test_north.mjs http://127.0.0.1:18082
```
