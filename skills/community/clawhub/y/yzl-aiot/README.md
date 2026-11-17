# YZL-AIoT 技能

> 云智联科技（yzlkj）旗下 AIoT 开源组织核心项目。
> 专为通用智能体（AI Agent）设计的物联网设备管理技能：设备数据采集、历史数据查询、远程控制。

**当前版本：v1.2.1**（对齐云智联开放接口 2026-07-25 文档；v1.2.1 为命令写法修正）

## ⚠️ 重要：频率限制与封 IP 风险

请求方**必须确保请求频率低于平台限速，并保证并发不超过 2**。

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
| 🐙 GitHub（主站） | https://github.com/yzlkj/yzl-aiot |
| 🏠 Gitee（镜像） | https://gitee.com/yzl-aiot/yzl-aiot |
| 📦 ClawHub | clawhub → `yzl-aiot` |

## 安装 / 使用

1. 设置环境变量：

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
