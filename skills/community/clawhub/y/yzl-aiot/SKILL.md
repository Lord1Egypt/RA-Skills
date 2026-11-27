---
name: yzl-aiot
description: "YZL-AIoT 平台入口（aiot.yzlkj.com）：南向设备接入与北向应用接入的总入口。用户说『加载 yzl-aiot』时，必须先加载本技能，再依次加载北向 `yzl-aiot-north` 与南向 `yzl-aiot-south` 两个技能；用户说『加载 yzl-aiot 北向 / 南向』时，只加载对应那个技能。开放平台 open.yzlkj.com 的 API Key 取数 / 开关请用 `yzl-open-api`。本技能只做平台总览、认证与分流，不直接提供接入代码细节。"
homepage: https://github.com/yzlkj/yzl-aiot
metadata: { "openclaw": { "requires": { "bins": ["python"] } } }
---

> 🧭 **平台边界**：本技能是 `aiot.yzlkj.com` 的总入口，只做分流与总览。
> 北向应用接入 → `yzl-aiot-north`；南向设备端固件 → `yzl-aiot-south`。
> 开放平台 `open.yzlkj.com`（API Key 取数 / 开关水阀）→ `yzl-open-api`，与本平台不是同一套系统。

## 🚦 加载规则（先执行，再回答）

| 用户说 | 你必须做的 |
|---|---|
| 「加载 yzl-aiot」「加载 YZL-AIoT 技能」 | 先加载本技能，**再依次加载 `yzl-aiot-north` 与 `yzl-aiot-south` 两个技能**（两个都要，不得用本页摘要代替） |
| 「加载 yzl-aiot 北向技能」 | **只**加载 `yzl-aiot-north` |
| 「加载 yzl-aiot 南向技能」 | **只**加载 `yzl-aiot-south` |
| 提到开放平台：液位 / 温湿度 / 水阀 / 「云智联YZL」小程序密钥 / open.yzlkj.com | 用 `yzl-open-api`（未安装就先 `clawhub install yzl-open-api`） |

- 用户只说「加载 yzl-aiot」而子技能未安装：先给安装命令（`clawhub install yzl-aiot-north`、`yzl-aiot-south`），不要编造接口细节。
- 已安装的子技能按名字加载即可（技能名来自 SKILL.md 的 `name`，与目录名无关）。
- 三个技能的分工见下表，**不要跨平台套用**。

## ⚙️ 运行时要求

- **Python 3.6+**（仅标准库）：本技能自带的 `tool.py` 用于环境自检与迁移引导。
- **不需要 API Key**：`status`、`migrate`、`check-update` 均可直接运行。
- 兼容层的开放平台命令才需要 `YZLIOT_API_KEY`（见「从 1.x 升级」）。

## 🌱 YZL-AIoT 平台（aiot.yzlkj.com）

**一句话：设备用南向连上来，应用用北向把数据接走。**

- 南向：`lgn` 登录、`facs` 实时上报、`hear` 心跳、下行 `set/get`、历史补传、OTA；
- 北向：设备 / 实时值 / 历史 / 聚合 / 指令 / 告警 REST，北向 MQTT 订阅，Bridge / Webhook；
- 测点（设施）属性可在平台上按需改：可控制、可查询、改类型、改显示名、隐藏。

## 🧭 三条线路

| 方向 | 技能 | 入口 / 协议 | 典型任务 |
|---|---|---|---|
| 北向 | `yzl-aiot-north` | `aiot.yzlkj.com` REST、北向 MQTT、Bridge / Webhook | 后端 / 看板 / 小程序 / 数据管道、历史与告警、改测点属性 |
| 南向 | `yzl-aiot-south` | TCP 41032、UDP 40501、MQTT 1883、OTA | MCU 固件、4G 模组、lwIP / W5500 移植 |
| 开放平台 | `yzl-open-api` | `open.yzlkj.com` Open API v2（API Key） | 快速取数、开关水阀 |

## ⚡ 快速使用

用户只需说：

- “把设备数据接进我的后端 / 看板” → 北向，给 Python / Node 示例；
- “给这块 MCU 写接入固件” → 南向，给 C SDK 集成步骤；
- “让这个测点可以下发指令” → 北向，改该测点 `access`；
- “看下昨天的液位历史” → 先判断平台：开放平台走 `yzl-open-api`，AIoT 平台走北向。

## 🏗️ 平台速览（细节在子技能里）

- **北向认证**：JWT（`POST /auth/login`）、账号密码自动登录、平台 API Key（`X-API-Key`）
- **北向数据**：设备列表 / 实时值 / 历史 / 聚合 / 指令 / 告警；测点属性用 `PATCH /open/product/{型号}/metric/{key}` 单点修改
- **南向链路**：设备号 + 密码 `lgn`、`facs` 上报、`hear` 心跳、`set` / `get` 回执、`facs_his` 补传、OTA
- **域名**：南向测试 `ciot.yzlkj.com`、生产 `siot.yzlkj.com`；北向统一 `aiot.yzlkj.com`
- **安全**：token、密码、API Key 只放环境变量，不写进代码或仓库

## 🚦 限频（只针对北向 REST）

- **用户配额 = 基础配额 + 设备数 × 每台追加**（例：基础 60 + 100 台 × 10 = **1060 次/秒**，具体数值以账号页面为准，`rate_config` 可热调）；
- **写接口（POST / PUT / DELETE）按 3 倍配额计**；超限返回 `429`；
- 配额数据由接口返回，**查询配额本身也受限速约束**；
- 南向设备链路（TCP / UDP / MQTT）**不走**这条 REST 配额；
- 开放平台 `open.yzlkj.com` 的按接口限速、并发 2、非 0 返回封 IP，**只属于 `yzl-open-api`**，不要套到本平台。

## 🔄 从 1.x 升级（2.0.0 说明）

- 2.0.0 起本技能拆为平台入口：北向 → `yzl-aiot-north`，南向 → `yzl-aiot-south`，开放平台 → `yzl-open-api`
- **兼容层**：本技能仍自带 1.x 的 `tool.py`（`all` / `send` / `history` 等），继续可用到 **3.0.0**；这些命令只对接 `open.yzlkj.com`
- **迁移**：`python tool.py migrate` 给出步骤；`python tool.py status` 查看环境与同族技能安装情况
- 3.0.0 将移除兼容层，定时脚本请提前迁移到 `yzl-open-api`

## 🔧 手动命令（可选）

```bash
python tool.py status        # 环境与技能安装情况（不需要 API Key）
python tool.py migrate       # 开放平台迁移引导（不需要 API Key）
python tool.py check-update  # 检查 yzl-aiot 自身版本
python tool.py all           # 兼容层：开放平台设备列表（需要 YZLIOT_API_KEY）
python tool.py send ...      # 兼容层：开放平台下发指令
```

## 📞 联系与官网

- 电话：089836692518/18689850608
- 邮箱：yzlkj@yzlkj.com
- 官网：www.yzlkj.com

## 版本历史

### v2.0.0 (2026-11-27) — 拆分为平台入口
- 🧭 **改为平台总入口**：不再承载开放平台接入细节，改为 `aiot.yzlkj.com` 的入口与分流
- 🧩 **三向拆分**：北向 `yzl-aiot-north`、南向 `yzl-aiot-south`、开放平台 `yzl-open-api`
- 🚦 **加载规则**：说「加载 yzl-aiot」时同时加载南北向；指定方向时只加载对应技能
- 🛡️ **兼容层**：保留 1.x 的 `tool.py`（开放平台命令）到 3.0.0，避免老用户脚本直接失效
- 🧰 **新增命令**：`status`、`migrate`（均可无 API Key 运行）
- 📏 **限速口径**：北向 REST 按用户配额（基础 + 设备数 × 每台追加，按秒计；写接口 3 倍）；开放平台限速只属于 `yzl-open-api`

> 2.0.0 之前，本技能是 `open.yzlkj.com` 的取数技能；该能力已整体迁至 `yzl-open-api`。
