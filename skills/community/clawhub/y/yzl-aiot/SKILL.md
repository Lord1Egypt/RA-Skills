---
name: yzl-aiot
description: "YZL-AIoT 云智联 AIoT 设备管理技能。Open API v2（文档更新 2026-07-25），路径以 /open/ 开头。一句话即可获取传感器数据、发送控制指令。⚠️ 请求频率必须低于平台限速，否则有封 IP 风险。激活语：云智联设备，钥匙是xxxxxx，帮我打开开关/获取数据"
homepage: https://github.com/yzlkj/yzl-aiot
metadata: { "openclaw": { "requires": { "bins": ["python"], "env": ["YZLIOT_API_KEY"] } } }
---

## ⚙️ 运行时要求

- **Python 3.6+**（仅使用 json, os, sys, http.client, time, collections 等标准库）
- **命令统一用 `python`**：本文档示例均为 `python tool.py ...`；若所在环境只有 `python3`（部分 Linux/macOS 较常见），把 `python` 换成 `python3` 即可，如 `python3 tool.py help`。
- **环境变量 `YZLIOT_API_KEY`** - 必需，请从「云智联YZL」微信小程序获取

## 🚨 请求频率限制与封 IP 风险（必读）

> 本节内容来自云智联开放接口《使用说明》（更新于 **2026-07-25**）的「限制」与「安全策略」。

**请求方必须确保每一个接口的请求频率都严格小于下表限制，并保证并发不超过 2。** 平台会对异常请求行为自动防护：

- **触发条件**：同一 IP 在短时间内频繁返回非 `0` 状态码（如 `400`、`401`、`403`、`429` 等）时，将被判定为错误请求。
- **封禁后果**：触发条件的 IP 将面临 **永久封禁**（仅封该来源 IP，影响该 IP 下所有调用）。
- **降险要求**：
  1. 调用频率必须低于限速，**不要**压线轮询（建议留出 20% 以上余量）；
  2. 失败重试必须使用**指数退避**（如 1s、2s、4s…），**禁止**在短时间内反复重试相同请求；
  3. 确保 `YZLIOT_API_KEY` 有效，避免因认证失败产生大量 `401`；
  4. 监控返回状态码，发现异常立即停止调用并排查。

### 接口限速表

| 接口 | 路径 | 限速 |
|------|------|------|
| 获取所有设备 | `GET /open/device/all` | 10 次 / 10 秒 |
| 获取设备列表（分页） | `GET /open/device/list` | 5 次 / 10 秒 |
| 获取设备详情 | `GET /open/device/{id}` | 10 次 / 10 秒 |
| 获取设施值历史 | `GET /open/history` | **6 次 / 30 秒** |
| 发送指令 | `POST /open/command/send` | 2 次 / 5 秒 |
| 获取指令详情 | `GET /open/command/{id}` | 2 次 / 5 秒 |
| 获取指令列表（分页） | `GET /open/command/list` | 2 次 / 10 秒 |
| 测试接口 | `GET /open/ping` | 10 次 / 10 秒 |

**并发限制：2**（同一 APIKEY 同时最多 2 个请求在途）

### 本技能内置的保护

- 本地按接口排队限速，请求前自动等待，避免超过平台阈值；
- **不做自动重试**（避免重试风暴触发封禁）；
- 连续 5 次返回非 `0` 状态码时自动中止本次运行并提示，防止持续刷出错误请求；
- 收到 `429` / `401` / `403` 时给出明确的降险提示。

## 🌱 YZL-AIoT 云智联 AIoT 设备管理

**一句话就能获取设备数据和发送控制指令！** 基于云智联开放接口 v2（文档更新 2026-07-25），所有 API 路径使用 `/open/` 前缀。

> 💡 如果你之前使用的是 `yzl-iot-api`，请迁移至此技能获取后续更新支持。

## ⚡ 快速使用

用户只需说：

- "获取传感器数据" → 自动获取所有土壤温湿度云传感器的温湿度
- "获取液位" / "液位数据" → 自动获取液位传感器的液位数据
- "打开电磁阀" / "开启水阀" → 开启远程电磁阀
- "关闭电磁阀" / "关闭水阀" → 关闭远程电磁阀

## 📋 支持的设备

### 土壤温湿度云传感器

| 型号前缀 | 说明 |
|----------|------|
| YZLSTM1 | 土壤温湿度云传感器标准款 |
| STMCBL | 土壤温湿度云传感器加长款 |
| STMCS1 | 土壤温湿度云传感器太阳能款 |

**获取数据：** 温度(wd)、湿度(sf)

### 远程电磁阀

| 型号前缀 | 说明 |
|----------|------|
| WA1CB1 | 远程电磁阀低功耗版本 |
| WANCD1 | 4G水阀（目前支持远程控制） |

**控制指令：** 通过 `kk1` 设施控制开(1)/关(0)。当前平台**支持远程控制的型号为 WANCD1**（远程控制水阀）。

### 低功耗液位传感器

| 型号前缀 | 说明 |
|----------|------|
| YZLWP01 | 低功耗液位传感器 |

**获取数据：** 液位(yw)

## 📖 自然语言示例

```
用户: "帮我看看传感器数据"
→ 返回所有土壤温湿度云传感器的温湿度

用户: "获取液位"
→ 返回液位传感器的液位数据

用户: "打开电磁阀"
→ 开启远程电磁阀

用户: "关闭水阀"
→ 关闭远程电磁阀
```

## 🔧 手动命令（可选）

如果需要更精细控制：

> 下列命令统一用 `python`；若环境只有 `python3`，把 `python` 换成 `python3` 即可（如 `python3 tool.py help`）。

```bash
# 获取所有设备（简易信息，不含设施集；可带轮询标记）
python tool.py all
python tool.py all --tag mytag

# 分页获取设备列表（含设施集，单页上限 200）
python tool.py list [跳过数量] [单页数量] [筛选词]

# 查看设备详情（路径参数）
python tool.py device WANCD1-0000000001

# 获取历史数据（设施ID，非设备ID；天数默认 5）
python tool.py history <设施ID> [天数]

# 获取设备全部设施的历史数据
python tool.py device-history <设备ID> [天数]

# 开启电磁阀（args 上限 5 个，waitTimeout 5~20 秒）
python tool.py send WANCD1-0000000001 SetFac '["WANCD1-0000000001","kk1","1"]'

# 关闭电磁阀
python tool.py send WANCD1-0000000001 SetFac '["WANCD1-0000000001","kk1","0"]'

# 指令记录
python tool.py cmd-list <设备ID>
python tool.py cmd-detail <指令ID>
```

## 🔄 自动版本更新检测 (v1.1.0+)

本技能内置自动版本更新检测功能。

### 工作方式

1. **自动检测**：每次运行工具时，静默向 ClawHub 查询最新版本
2. **缓存机制**：每 12 小时只检测一次，减少网络请求
3. **智能提醒**：检测到有新版本时，在命令输出结果末尾追加更新提醒
4. **离线容错**：网络不可用时使用上次缓存结果，不阻塞操作

### 手动检查更新

```bash
python tool.py check-update
```

### 更新方法

```bash
# 更新到最新稳定版
clawhub update yzl-aiot

# 或指定版本
clawhub update yzl-aiot --version 1.2.1
```

## 📡 API 接口参考（v2，文档更新 2026-07-25）

### 基础信息

| 项 | 值 |
|----|----|
| Base URL | `https://open.yzlkj.com` |
| 认证 | 请求头 `YZLIOT-APIKEY` |
| 响应包 | `{ "code": 0, "data": ..., "time": "..." }`，`code = 0` 表示成功 |
| 并发限制 | 2 |
| 在线文档 | https://cn6l1w4yn0.apifox.cn |

### 接口与参数

#### 1. 测试接口

`GET /open/ping` — 返回连接状态。

#### 2. 获取所有设备

`GET /open/device/all?PollingTag=`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `PollingTag` | string | 否 | 轮询标记 |

返回简易设备信息（**不含设施集**）：`id`、`name`、`model`、`status`、`latestMessageTime`、`latestModificationTime`。
需要设施数据时再用设备详情接口补查。

#### 3. 获取设备列表（分页）

`GET /open/device/list?Filter=&SkipCount=&MaxResultCount=`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `Filter` | string | 否 | 筛选 |
| `SkipCount` | integer | 否 | 跳过数量，配合 `MaxResultCount` 翻页 |
| `MaxResultCount` | integer | 否 | 单页最大数量，**上限 200** |

返回 `data.items[]`（含 `facilitys` 设施集）与 `data.totalCount`。

#### 4. 获取设备详情

`GET /open/device/{id}` — `id` 为设备 ID（路径参数）。返回设备完整信息，含 `facilitys` 设施集。

#### 5. 获取设施值历史

`GET /open/history?facilityId=&StartTime=&EndTime=&MaxCount=`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `facilityId` | string | 是 | **设施 ID**（`facilitys[].id`，不是设备 ID） |
| `StartTime` | string | 是 | 开始时间，格式 `2026-03-07 00:01:59` |
| `EndTime` | string | 是 | 结束时间，必须大于开始时间 |
| `MaxCount` | integer | 否 | 最大条数，**上限 3000** |

返回 `data`：`actual`、`total`、`firstTime`、`lastTime`、`values[]`（`valueId`、`value`、`time`）。

#### 6. 发送指令

`POST /open/command/send`，Body（`application/json`）：

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `deviceId` | string | 是 | 设备 ID（最长 32 字符） |
| `type` | string | 是 | 指令类型：`GetFac` / `SetFac` / `Upfs` / `Custom` |
| `args` | string[] | 否 | 指令参数，**最多 5 个** |
| `waitConfirm` | boolean | 否 | 是否等待设备确认 |
| `waitTimeout` | integer | 否 | 等待超时秒数，范围 **5~20** |

开关示例：

```json
{
  "deviceId": "WANCD1-0000000001",
  "type": "SetFac",
  "args": ["WANCD1-0000000001", "kk1", "1"],
  "waitConfirm": true,
  "waitTimeout": 15
}
```

- `kk1`：设施的 Key，需确保该设施是开关（`identifying = IoT.FAC.CTRL.SWITCH`）
- `1` 开启，`0` 关闭
- 当前支持远程控制的型号：`WANCD1`

返回：`{ "commandId": "...", "status": "Pending" }`

#### 7. 获取指令详情

`GET /open/command/{id}` — 返回 `id`、`deviceId`、`type`、`args`、`status`、`creationTime`。

#### 8. 获取指令列表（分页）

`GET /open/command/list?DeviceId=&SkipCount=&MaxResultCount=`

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `DeviceId` | string | 是 | 设备 ID |
| `SkipCount` | integer | 否 | 跳过数量 |
| `MaxResultCount` | integer | 否 | 单页最大数量 |

### 数据模型与枚举

| 枚举 | 取值 |
|------|------|
| `DeviceStatus` | `Online`、`Standby`、`Hibernate`、`Offline`、`Clean` |
| `CommandStatus` | `Pending`、`Sent`、`Failed`、`Completed`、`Cancelled`、`Rejected`、`Outtime`、`Outcount` |
| `CommandType` | `GetFac`、`SetFac`、`Upfs`、`Custom` |
| `FacilityValueType` | `Int`、`Decimal`、`String`、`Enum` |

**设施（facility）字段**：`id`、`name`、`key`、`valueType`、`value`、`valueUpdateTime`、`tags`、`identifying`

### 设备同步建议（来自官方《使用说明》）

1. 调用 `GET /open/device/all` 获取全部设备基础信息与 `latestModificationTime`；
2. 与本地记录比对，远端时间更新的设备才需要同步；
3. 对变更设备调用 `GET /open/device/{id}` 拉取详情（含设施集）；
4. 更新本地数据，完成增量同步。
5. 轮询间隔建议 **5 分钟 / 10 分钟 / 半小时**，按业务实时性调整；首次可先用 `/open/device/list` 分页拉全量。

> 注意：`/open/device/all` 与 `/open/device/{id}` 都有频率限制，批量补查详情时务必按限速排队，避免触发 429 与封 IP 策略。

### 状态码

| 码值 | 说明 |
|------|------|
| 0 | 成功 |
| 400 | 参数错误 |
| 401 | 未授权 / 无效 APIKey |
| 403 | 权限不足 |
| 429 | 请求频率超限 |
| 500 | 服务器错误 |

> 出现 `429` 说明已超过限速；出现 `401/403` 请先检查 APIKey 与权限。**务必停止高频重试**，否则可能被永久封 IP。

## 📞 联系与官网

- 电话：089836692518/18689850608
- 邮箱：yzlkj@yzlkj.com
- 官网：www.yzlkj.com

## 版本历史

### v1.2.1 (2026-10-18) — 命令示例统一为 python
- 🐍 **命令写法统一**：所有示例由 `python3 tool.py ...` 改为 `python tool.py ...`；并注明只有 `python3` 的环境（部分 Linux/macOS）把 `python` 换成 `python3` 即可
- 📦 **依赖声明同步**：`metadata.openclaw.requires.bins` 由 `["python3"]` 改为 `["python"]`
- 📝 **帮助文本同步**：`tool.py help` 的用法与示例、README、skill-card 同步改为 `python`
- ℹ️ 无接口、参数或行为变更，纯文档与提示文本修正（功能与 v1.2.0 完全一致）

### v1.2.0 (2026-10-17) — 对齐 2026-07-25 官方文档
- 🚨 **新增《请求频率限制与封 IP 风险》必读章节**：明确要求请求频率低于限速、并发 ≤2；同 IP 频繁返回非 0 状态码会被**永久封禁**；给出指数退避与监控要求
- ⚡ **历史数据限速更新**：`2 次/10 秒` → `6 次/30 秒`
- 📄 **设备列表上限更新**：`MaxResultCount` 上限 `50` → `200`
- 🔍 **获取所有设备**：新增 `PollingTag`（轮询标记）参数
- 🧩 **补充数据模型与枚举**：`DeviceStatus`、`CommandStatus`、`CommandType`、`FacilityValueType`
- 📝 **指令约束确认**：`args` 最多 5 个、`waitTimeout` 5~20 秒；当前支持远程控制型号 `WANCD1`
- 🛡️ **tool.py 安全性增强**：限速排队修正、错误码提示、连续 5 次非 0 自动中止（降低封 IP 风险），不做自动重试

### v1.1.0 (2026-06-18) — API v2 适配
- 🔄 **适配新版 API**：所有接口路径从 `/openv1/` 迁移至 `/open/`
- 🔧 **设备详情**：改用路径参数 `GET /open/device/{id}`
- 🔧 **指令详情**：改用路径参数 `GET /open/command/{id}`
- 🔧 **历史数据**：改为纯 Query 参数请求，日期格式更新
- ⚡ **发送指令**：超时范围调整至 5~20 秒
- 📝 **文档更新**：同步新版 API 接口参考

### v1.0.0 (2026-06-03) — 初始版本
- 🎉 从 yzl-iot-api 迁移，全新发布
- ✨ 自动版本更新检测
- ✨ 缓存机制：12 小时内不重复请求
- ✨ 离线容错：网络不可用时使用缓存结果
- 🔧 完整支持：设备列表、详情、历史数据、控制指令
- 🗣️ 自然语言命令（智能识别设备型号和执行意图）
