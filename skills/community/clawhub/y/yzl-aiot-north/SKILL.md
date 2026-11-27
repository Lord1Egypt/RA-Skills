---
name: yzl-aiot-north
description: "YZL-AIoT 北向接入技能（yzl-aiot-north，平台 aiot.yzlkj.com）。用 Python 或 JavaScript/Node.js 把平台设备数据接进自己的应用、后端、独立服务器、看板、Webhook 或数据管道：JWT/API-Key 认证、设备/实时值/历史/聚合/指令/告警 REST、北向 MQTT 订阅、REST 轮询的 HTTP/Webhook 桥（Bridge）；也覆盖型号设施的查询与单设施属性修改（PATCH /open/product/{id}/metric/{key}：access 改 rw 才能下发指令、改 dataType/label/visible）。Use when integrating 云智联 AIoT northbound data, or when the user wants to change one facility/metric property（让测点可控制、改数据类型、隐藏测点、清理自动添加的设施）, or mentions 北向、数据桥、webhook 推送、历史数据接入、告警接入、MQTT 订阅。"
---

> 🧭 **平台边界**：本技能只服务 `aiot.yzlkj.com` 北向（应用侧）。
> 设备端固件 → `yzl-aiot-south`；平台总入口 → `yzl-aiot`；开放平台 `open.yzlkj.com` → `yzl-open-api`（不是同一套系统）。
> 北向 REST 与南向设备链路（TCP 41032 / UDP 40501 / MQTT 1883）是两条链路，认证、限流都不同。

## ⚙️ 运行时要求

- **Python ≥ 3.8 / Node.js ≥ 18**：直接用 `lib/north_client.py`（标准库）或 `lib/north_client.mjs`（原生 fetch），**无需安装 SDK 或第三方包**
- **凭证**（三选一，见「认证」）：`AIOT_TOKEN` / `AIOT_ACCOUNT`+`AIOT_PASSWORD` / `AIOT_API_KEY`
- 不把账号、密码、token 写进代码或仓库

## 🚦 限频（只针对北向 REST）

- **用户配额 = 基础配额 + 设备数 × 每台追加**（例：基础 60 + 100 台 × 10 = **1060 次/秒**，具体数值以账号页面为准，`rate_config` 可热调）
- **写接口（POST / PUT / DELETE）按 3 倍配额计**；超限返回 `429`
- 配额数据由接口返回，**查询配额本身也受限速约束**
- 轮询 N 台设备时 `interval` 至少 N 秒，或改用北向 MQTT / Bridge 事件
- 开放平台 `open.yzlkj.com` 的按接口限速、并发 2、非 0 返回封 IP **不适用于本平台**

## 🌱 YZL-AIoT 北向（aiot.yzlkj.com）

**一句话：把平台里的设备数据，安全地接进你自己的系统。**

覆盖：设备、实时值、历史、聚合、指令、告警、型号；可下发 `set` / `get`；可订阅北向 MQTT；可用内置 Bridge 起一个只读 HTTP + Webhook 数据桥。

## ⚡ 快速使用

| 用户说 | 做法 |
|---|---|
| “把设备数据接进我的后端 / 看板” | 用 `NorthClient` 拉设备与实时值，或起 `NorthBridge` |
| “历史数据 / 曲线” | `devices.history(id, keys=[...], limit=...)`，或 `/events` |
| “告警接到我们的系统” | `alarms.list()`，或 Bridge → Webhook |
| “让这个测点能下发指令” | 改该测点 `access=rw`（见「单设施属性修改」） |
| “订阅 MQTT” | 确认有平台分配的北向 MQTT 独立凭证，再用 `NorthMQTT` |

## 🔑 认证

优先级（从高到低）：

| 方式 | 变量 | 说明 |
|---|---|---|
| JWT | `AIOT_TOKEN` | `Authorization: Bearer <token>`，最直接 |
| 账号密码 | `AIOT_ACCOUNT` + `AIOT_PASSWORD` | 自动登录，`401` 自动重登 |
| 平台 API Key | `AIOT_API_KEY` | 请求头 `X-API-Key`；本账号实测单独使用可能返回空数据 |

平台登录：

```http
POST https://aiot.yzlkj.com/auth/login
{"account":"用户名或手机号","password":"密码"}
```

> 浏览器前端不要持有 JWT / API Key；只访问你自己的后端或 Bridge。

## 🐍 Python 用法

```python
from aiot_north import NorthClient, normalize_telemetry

client = NorthClient.from_env()          # AIOT_TOKEN 或 AIOT_ACCOUNT/PASSWORD
devices = client.devices.list(max_results=20)
record = normalize_telemetry(client.devices.telemetry(devices["items"][0]["id"]))
print(record["deviceId"], record["values"], record["online"])

history = client.devices.history("DEV-1", keys=["temp"], limit=100)
client.devices.command("DEV-1", "set", ["sw", "1"])
```

Bridge（只读 HTTP + Webhook）：

```python
from aiot_north import NorthClient
from aiot_north.bridge import BridgeConfig, NorthBridge

bridge = NorthBridge(NorthClient.from_env(), BridgeConfig(
    device_ids=["DEV-1"], port=8080, interval=5,
    webhook_url="https://app.example.com/aiot/events",
    webhook_secret="...",
))
bridge.start(block=True)
```

CLI：

```bash
aiot-north whoami | devices | telemetry <id> | history <id> --keys temp,hum --limit 20 | bridge --device <id> --port 8080
```

## 🟨 JavaScript 用法

```js
import { NorthClient, normalizeTelemetry } from "aiot-north";

const client = await NorthClient.fromEnv();
const devices = await client.devices.list({ maxResults: 20 });
const record = normalizeTelemetry(await client.devices.telemetry(devices.items[0].id));
console.log(record.deviceId, record.values, record.online);

await client.devices.command("DEV-1", "set", ["sw", "1"]);
```

Bridge：

```js
import { NorthBridge, NorthClient } from "aiot-north";
const bridge = new NorthBridge(await NorthClient.fromEnv(), {
  deviceIds: ["DEV-1"], port: 8080, interval: 5,
  webhookUrl: process.env.AIOT_WEBHOOK_URL,
  webhookSecret: process.env.AIOT_WEBHOOK_SECRET,
});
await bridge.start();
```

CLI：`node src/cli.js whoami | devices | telemetry <id> | bridge --device <id> --port 8080`

## 📋 常用接口与方法

| 需求 | Python | JS |
|---|---|---|
| 登录 | `client.login()` | `client.login()` |
| 当前用户 | `client.profile()` | `client.profile()` |
| 账号概览 | `client.account()` | `client.account()` |
| 设备列表 | `client.devices.list()` | `client.devices.list()` |
| 设备详情 | `client.devices.get(id)` | `client.devices.get(id)` |
| 最新值 | `client.devices.telemetry(id)` | `client.devices.telemetry(id)` |
| 历史 | `client.devices.history(id, keys=..., limit=...)` | `client.devices.history(id, {keys, limit})` |
| 聚合 | `client.devices.aggregate(...)` | `client.devices.aggregate(...)` |
| 下发指令 | `client.devices.command(id, "set", ["sw","1"])` | `client.devices.command(id, "set", ["sw","1"])` |
| 指令列表 | `client.commands.list(...)` | `client.commands.list(...)` |
| 告警 | `client.alarms.list(...)` | `client.alarms.list(...)` |
| 型号 | `client.products.list()` | `client.products.list()` |
| 改单个设施属性 | `client.request("PATCH", path, body={...})` | `client.request("PATCH", path, { body })` |
| 网关端口 | `client.gateway_ports()` | `client.gatewayPorts()` |
| 参数归一化 | `normalize_telemetry` / `parse_device_payload` | 同名 |

## 🏗️ Bridge 与 Webhook

```
GET  /health
GET  /devices
GET  /devices/{id}/latest
GET  /devices/{id}/history?limit=100
GET  /events?since=<seq>&limit=100
GET  /metrics
POST /commands/{id}       # 需 allowCommand / --allow-command，默认关闭
```

Webhook 头：

```
X-AIoT-Event: telemetry
X-AIoT-Signature: sha256=<HMAC-SHA256(raw body, secret)>
```

校验必须用**原始 body**：Python `hmac.compare_digest`，Node `crypto.timingSafeEqual`。

## 🧩 单设施（测点）属性修改

平台原来只能 `PUT /open/product/{id}` 整表覆盖（漏一项就丢一个设施），2026-11-21 起支持单点改：

```http
PATCH /open/product/{型号ID}/metric/{设施key}
Authorization: Bearer <token>
Content-Type: application/json

{"dataType":"enum","access":"r","label":"浮球1(高/低)"}
```

Body 全部可选，只传要改的字段：

| 字段 | 取值 | 作用 |
|---|---|---|
| `dataType` | `int` / `decimal` / `text` / `enum` | 数据类型，影响平台解析、前端控件与曲线形态 |
| `access` | `rw` / `r` / `none` | `rw`=可查询+可下发指令；`r`=仅查询；`none`=仅上报 |
| `label` | 任意字符串 | 显示名称 |
| `unit` | 任意字符串 | 单位 |
| `visible` | `true` / `false` | 前端是否显示（不删数据） |

响应带 `before` / `after` 快照：

```json
{"code":0,"msg":"ok","data":{"product":"RSTICQ","key":"in1",
 "before":{"dataType":"int","access":"none","visible":true,"label":"输入1(浮球1)","unit":""},
 "after":{"dataType":"enum","access":"r","visible":true,"label":"输入1(浮球1)","unit":""}}}
```

批量改就循环调用，一次一个 key（接口本身是单设施的）。

## 📡 接口参考

| 项 | 值 |
|---|---|
| Base URL | `https://aiot.yzlkj.com` |
| 认证 | `Authorization: Bearer <JWT>` / `X-API-Key` |
| 设备列表 | `GET /open/device/list` |
| 设备详情 | `GET /open/device/{id}`（`metrics` 为 `{key: label}`，逐测点属性在 `metricMeta`） |
| 型号列表 | `GET /open/product/list`（`metrics[]` 含 `key/label/unit/dataType/access/visible`） |
| 单测点修改 | `PATCH /open/product/{id}/metric/{key}` |
| 测点语义配置 | `PUT /open/product/{id}/metrics-config` |
| 清理自动设施 | `POST /open/product/{id}/clean-metrics` |
| 告警列表 | `GET /open/alarm/list` |
| 状态码 | `429` 限流；`401` 未授权；`400` 参数错误；`404` 型号/key 不存在 |

## ⚠️ 常见坑（实测）

- **`access=rw` 只代表平台放控件，不代表设备认指令**：固件不支持时下发会超时/失败。
- `dataType` 与 IoTDB 序列类型绑定：序列类型首次写入即固定，`text` 序列写数字会失败；改 `dataType` 只影响解析与展示，不改已存数据。
- `visible=false` 不删数据，采集照旧，只是前端不显示。
- 设备上报了型号未定义的测点，平台会自动加设施：`autoAdd: true` + `addedAt`，默认 `decimal` + `access=none`；PATCH 改过任一属性后标记清除。
- 改完立即生效（服务端清型号缓存），不用重启。
- 本环境 `GET /open/product/{id}`（单型号详情）**实测 404**；取型号详情用 `GET /open/product/list` 再按 `id` 过滤。
- 非创建者且非管理员 PATCH 返回 `400`；型号或 key 不存在返回 `404`。
- 北向 MQTT 1883 需要**独立凭证**；用户 JWT、API Key、设备密码实测都会被拒。没有凭证就用 REST Bridge。
- `/open/device/list` 对 owner/admin 会返回 `password` / `bindCode`；SDK 默认脱敏，必须显式 `include_secrets` 才返回明文。
- `/open/alarm/list` 的 `pageSize` 可能被忽略，一次返回大量数据，业务侧自行截断。
- 时间字符串按平台本地时间（Asia/Shanghai）理解；Bridge 的 `receivedAt` 是 UTC ISO。
- 事件按 `ts` + `values` 变化触发；同一 `ts` 不重复推。

## ✅ 验证流程

1. `aiot-north whoami` 能通；
2. 设备列表非空；
3. `telemetry <id>` 有值；
4. Bridge `/health` 的 `lastPoll` 正常、`errorCount=0`；
5. `GET /events?since=0` 有事件；
6. 配了 Webhook：确认 2xx 且签名校验通过；
7. 改设施属性后：`GET /open/product/list` 能看到新的 `access`/`dataType`，再下一发 `get`/`set` 确认闭环。

## 🔐 安全

- 不在前端 / 仓库硬编码 token、密码、API Key、设备密码。
- Bridge 公网部署加 TLS + 鉴权/白名单；`--allow-command` 默认关闭。
- 不记录 `Authorization`、`X-API-Key`、`password`。
- Webhook secret 用环境变量；校验签名并防重放/去重。

## 🧰 接口库（一个接口一个方法）

| 文件 | 语言 | 说明 |
|---|---|---|
| `lib/north_client.py` | Python（标准库） | `NorthClient`，每个 REST 接口一个方法 |
| `lib/north_client.mjs` | Node.js（原生 fetch） | 同名方法（camelCase） |
| `lib/README.md` | — | 接口 ↔ 方法 ↔ CLI 对照表 |

```python
import sys; sys.path.insert(0, "lib")
from north_client import NorthClient
c = NorthClient.from_env()
c.list_devices(max_results=5)
c.telemetry("DEV-1")
```

## 📁 示例（Python / Node.js）

| 文件 | 场景 |
|---|---|
| `examples/python/quickstart.py` | 设备列表 → 最新值 → 历史 |
| `examples/python/bridge_webhook.py` | 只读 Bridge + Webhook |
| `examples/js/quickstart.mjs` | 同上（Node.js ESM） |
| `examples/js/bridge_webhook.mjs` | 同上（Node.js ESM） |

运行方式与依赖见 `examples/README.md`。

## 📁 本地资源

客户端与文档都随技能打包：`lib/north_client.py`、`lib/north_client.mjs`、`docs/`（01 北向接口说明、04 独立服务器与 Webhook、05 故障排查、06 设施属性修改）。不需要外部 SDK。

## 📞 联系与官网

- 电话：089836692518/18689850608
- 邮箱：yzlkj@yzlkj.com
- 官网：www.yzlkj.com

## 版本历史

### v2.0.0 (2026-11-27) — 自带接口库（一个接口一个方法）
- 🧰 新增 `lib/north_client.py`（标准库）与 `lib/north_client.mjs`（原生 fetch），覆盖全部北向 REST 接口
- 🖥️ `tool.py` 改为调用本技能自带库，不再依赖外部 SDK
- 🧪 新增 `tests/`：本地 mock + 25 项 Python 自测、12 项 JS 自测（离线）

### v1.3.0 (2026-11-27) — 增加 Python / Node.js 示例
- 📁 新增 `examples/`：Python 与 Node.js 各两例（quickstart、Bridge + Webhook）
- 📝 SKILL / README 增加示例入口

### v1.2.0 (2026-11-27) — 文档重写 + 命令行工具
- 📝 SKILL.md 按 `yzl-open-api` 结构重写
- 🧰 新增 `tool.py`：包装 SDK CLI（devices / telemetry / history / command / bridge），并提供 `help` / `version` / `check-update`
- 📄 补齐 README / CHANGELOG / skill-card / _meta / sync.sh

### v1.1.0 (2026-11-24) — 补单设施属性修改
- 🧩 新增 `PATCH /open/product/{id}/metric/{key}` 用法与 before/after 说明
- 🕳️ 补充实测坑：单型号 GET 404、`autoAdd`、`access=rw` 的真实含义

### v1.0.0 — 北向首版
- 🐍🟨 Python / Node 客户端、CLI、Bridge / Webhook、北向 MQTT
- 🔑 三级认证（JWT → 账号密码 → API Key）

> 2026-11-27：技能更名 `aiot-north` → `yzl-aiot-north`（内容不变）。
