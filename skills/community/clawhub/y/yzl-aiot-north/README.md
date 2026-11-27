# YZL-AIoT 北向（yzl-aiot-north）

> 云智联 AIoT 平台 `aiot.yzlkj.com` 的**北向接入**技能：把设备数据接进你的应用、后端、看板或数据管道。
> **只服务北向**；设备端固件用 `yzl-aiot-south`，开放平台 `open.yzlkj.com` 用 `yzl-open-api`。

**当前版本：v2.0.0**（自带接口库：一个接口一个方法）

## 平台边界

| 你的需求 | 用哪个技能 | 入口 / 协议 |
|---|---|---|
| 后端 / 看板 / Webhook / 历史与告警 | **本技能 `yzl-aiot-north`** | `aiot.yzlkj.com` REST、北向 MQTT、Bridge |
| MCU / 4G 模组固件接入 | `yzl-aiot-south` | TCP 41032 / UDP 40501 / MQTT 1883 |
| 开放平台 API Key 取数 / 开关水阀 | `yzl-open-api` | `open.yzlkj.com` Open API v2 |
| 不确定 | `yzl-aiot`（平台入口） | 负责分流 |

## 安装

```bash
clawhub install yzl-aiot-north
```

技能自带 `lib/`：`north_client.py`（Python 标准库）与 `north_client.mjs`（Node 原生 fetch），**不需要安装第三方包**。

## 认证

| 方式 | 变量 |
|---|---|
| JWT | `AIOT_TOKEN` |
| 账号密码 | `AIOT_ACCOUNT` + `AIOT_PASSWORD`（401 自动重登） |
| API Key | `AIOT_API_KEY`（`X-API-Key`） |

## 快速命令

```bash
python tool.py devices --limit 5          # 设备列表
python tool.py telemetry DEV-1            # 最新值
python tool.py history DEV-1 --keys temp,hum --limit 50
python tool.py command DEV-1 set sw 1     # 下发指令（写接口，3 倍配额）
python tool.py bridge --device DEV-1 --port 8080
python tool.py check-update               # 检查技能版本
```

> `tool.py` 是 SDK CLI 的包装：业务命令委托 `aiot_north`，本地命令为 `help` / `version` / `check-update`。

## 接口库

```python
import sys; sys.path.insert(0, "lib")
from north_client import NorthClient
c = NorthClient.from_env()
c.list_devices(max_results=5); c.telemetry("DEV-1")
```

```js
import { NorthClient } from "./lib/north_client.mjs";
const c = await NorthClient.fromEnv();
await c.listDevices({ maxResults: 5 });
```

完整对照见 `lib/README.md`。

## 示例

`examples/` 下有 Python 与 Node.js 两套可运行示例：

```bash
python examples/python/quickstart.py
python examples/python/bridge_webhook.py DEV-1
node examples/js/quickstart.mjs
node examples/js/bridge_webhook.mjs DEV-1
```

## 限频

**用户配额 = 基础配额 + 设备数 × 每台追加**（例：基础 60 + 100 台 × 10 = 1060 次/秒）；
**写接口（POST / PUT / DELETE）按 3 倍配额计**；超限 429。配额数据由接口返回，查询配额本身也受限速约束。
开放平台 `open.yzlkj.com` 的按接口限速与「封 IP」不适用于本平台。

## 文档

- 平台：https://aiot.yzlkj.com
- 协议与接口：技能自带 `docs/`（`01-北向接口说明.md`、`04-独立服务器与Webhook.md`、`05-故障排查.md`、`06-设施属性修改接口说明`）
- 桥接端点与 Webhook 签名见 `SKILL.md`

## 联系

- 电话：089836692518/18689850608
- 邮箱：yzlkj@yzlkj.com
- 官网：www.yzlkj.com
