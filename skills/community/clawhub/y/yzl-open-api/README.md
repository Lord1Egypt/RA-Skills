# YZL Open API（云智联开放接口）

> 云智联科技（yzlkj）**开放平台** `open.yzlkj.com` 的智能体技能：一句话取传感器数据、开 / 关设备。
> **本技能只覆盖 `open.yzlkj.com`**；`aiot.yzlkj.com` AIoT 平台请用 `yzl-aiot`（北向 `yzl-aiot-north` / 南向 `yzl-aiot-south`）。

**当前版本：v1.3.0**（由 `yzl-aiot` 更名而来，接口与 v1.2.1 完全一致）

## 平台边界

| 你的需求 | 用哪个技能 | 平台 / 入口 |
|---|---|---|
| 用 API Key 快速取数、开 / 关水阀 | **本技能 `yzl-open-api`** | `open.yzlkj.com` Open API v2 |
| 后端 / 看板 / Webhook / 历史数据接入 | `yzl-aiot-north` | `aiot.yzlkj.com` 北向 REST / MQTT / Bridge |
| MCU / 4G 模组固件接入 | `yzl-aiot-south` | `aiot.yzlkj.com` 南向 TCP 41032 / UDP 40501 / MQTT 1883 |
| 不确定用哪个 | `yzl-aiot`（平台总入口） | 负责分流 |

> 两个平台不是同一套系统：API Key、账号体系、数据模型都不同，不要混用。

## ⚠️ 重要：频率限制与封 IP 风险

请求方**必须确保请求频率低于平台限速，并保证并发不超过 2**。

**适用范围**：以下仅适用于 `open.yzlkj.com`。`aiot.yzlkj.com` 的限频主要针对北向 REST，按**用户配额** `基础配额 + 设备数 × 每台追加`（例：60 + 100 台 × 10 = 1060 次/秒；写接口 3 倍；配额数据由接口返回，查询也受限速约束），南向设备链路不走该配额。

| 接口 | 限速 |
|------|------|
| `GET /open/device/all` | 10 次 / 10 秒 |
| `GET /open/device/list` | 5 次 / 10 秒 |
| `GET /open/device/{id}` | 10 次 / 10 秒 |
| `GET /open/history` | 6 次 / 30 秒 |
| `POST /open/command/send` | 2 次 / 5 秒 |
| `GET /open/command/{id}` | 2 次 / 5 秒 |
| `GET /open/command/list` | 2 次 / 10 秒 |

- 并发限制：**2**
- 同一 IP 在短时间内频繁返回非 `0` 状态码（400/401/403/429 等）时，会被平台判定为异常请求并 **永久封禁该 IP**。
- 失败重试请使用**指数退避**（1s、2s、4s…），**切勿**在短时间内反复重试。
- 请确保 `YZLIOT_API_KEY` 有效，避免因认证失败产生大量 `401`。

本技能的 `tool.py` 已内置按接口排队限速、不做自动重试、连续 5 次非 0 响应自动中止等保护措施，但**调用方仍需自行控制整体调用节奏**。

## 仓库地址

| 平台 | 地址 |
|------|------|
| 🐙 GitHub | https://github.com/yzlkj/yzl-open-api |
| 🏠 Gitee | https://gitee.com/yzl-aiot/yzl-open-api |
| 📦 ClawHub | `yzl-open-api` |

## 安装 / 使用

```bash
clawhub install yzl-open-api
```

1. 设置环境变量（微信小程序「云智联YZL」→「我的」→「开放接口」获取）：

   ```bash
   export YZLIOT_API_KEY="你的APIKEY"
   ```

2. 常用命令（统一用 `python`；仅有 `python3` 的环境请把 `python` 换成 `python3`）：

   ```bash
   python tool.py all                  # 所有设备（简易信息）
   python tool.py device <设备ID>       # 设备详情
   python tool.py history <设施ID> 3    # 历史数据
   python tool.py send WANCD1-0000000001 SetFac '["WANCD1-0000000001","kk1","1"]'
   python tool.py help                 # 完整帮助
   ```

## 访问秘钥

- **环境变量** `YZLIOT_API_KEY` — 必需，请从「云智联YZL」微信小程序 →「我的」→「开放接口」获取

## 文档

- 在线接口文档：https://cn6l1w4yn0.apifox.cn
- 接口 Base URL：`https://open.yzlkj.com`
- 认证方式：请求头 `YZLIOT-APIKEY`

## 联系

- 电话：089836692518/18689850608
- 邮箱：yzlkj@yzlkj.com
- 官网：www.yzlkj.com
