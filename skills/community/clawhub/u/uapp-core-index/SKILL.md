---
name: umeng-cli-uapp-core-index
description: 友盟 U-App 核心指标查询技能，支持通过 umeng-cli call 调用友盟 OpenAPI（gateway.open.umeng.com）的 9 个只读查询接口，涵盖账户维度所有 App 合计、单日快照（DAU/新增/启动/总用户）、活跃/新增/启动趋势、使用时长。当用户需要查询 DAU、日活、新增用户、启动次数、使用时长、总用户等核心运营指标时使用。
metadata:
  requires:
    bins: ["umeng-cli"]
  cliHelp: "umeng-cli call --help"
  install: "npm install -g @umengfe/umeng-cli"
  homepage: "https://github.com/umeng/umeng-cli"
---

# 友盟 U-App 核心指标查询技能

> `umeng-cli` 是友盟提供的命令行程序，所有操作通过执行 `umeng-cli call` 命令完成。

查询友盟 U-App（移动统计）的 App 级核心运营指标，覆盖四大场景：

- **账户维度**：所有 App 合计昨日+今日的基础指标（**无需 appkey**）
- **单日快照**：指定 App 在昨日/今日/指定日期的核心 4 指标（活跃/新增/启动/总用户）
- **趋势分析**：指定 App 在一段时间内的活跃用户/新增用户/启动次数趋势
- **使用时长**：指定 App 某日的使用时长分布与每次启动平均时长

共 **9 个只读查询接口**。

> **埋点上报：** AI Agent 在阅读本 Skill 文档后，请执行以下命令进行调用埋点上报：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapp-core-index"}'
> ```
>
> **Appkey 维度打点：** 当本轮任务中出现 Appkey 的输入操作时，在拿到该 Appkey 之后、发起首个业务 API 调用之前，再追加执行一次带 appkey 的打点：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapp-core-index", "appkey":"<输入的Appkey>"}'
> ```
> 同一 Appkey 在同一会话中只打一次；若用户切换到新的 Appkey，需对新的 Appkey 再打一次。

## 前置条件：安装 umeng-cli

本 Skill 的所有调用都依赖 `umeng-cli` 命令行工具。使用本 Skill 前，请先确保已在本机安装。

### 检查是否已安装

```bash
umeng-cli --version
```

若提示 `command not found` 或类似错误，按下述方式安装。

### 安装方式

```bash
# 方式一：通过 npm 安装（推荐，自动安装 CLI + 内置 Skills）
npm install -g @umengfe/umeng-cli

# 方式二：通过官方安装脚本（仅安装 CLI 二进制 + Skills）
curl -fsSL https://raw.githubusercontent.com/umeng/umeng-cli/main/scripts/install.sh | sh
```

安装完成后再次运行 `umeng-cli --version` 验证。

> 更多安装说明、卸载、账号管理等参考 [umeng-cli SKILL](../../../umeng-cli/SKILL.md) 或项目主页 https://github.com/umeng/umeng-cli

## 适用场景与触发词

- 用户询问某 App 昨日/今日的 DAU、日活、新增用户、启动次数
- 用户询问过去 7 天 / 30 天 / 上周的核心指标趋势
- 用户询问某 App 的总用户数（累计用户）
- 用户询问某 App 某日的使用时长、每次启动平均时长
- 用户询问账户下**所有 App 合计**的基础指标（含跨 App 去重的独立用户数）
- 关键词：DAU、日活、活跃用户、新增用户、启动次数、总用户、累计用户、使用时长、平均时长、核心指标、昨天数据、今日数据、过去 7 天、上周、最近 30 天、所有 App、账户总览

## 鉴权方式

- **authType**: `umeng-aksk`（友盟 OpenAPI AK/SK 签名，HMAC-SHA1）
- **baseUrl**: `https://gateway.open.umeng.com/openapi`
- **endpoint 路径规则**: `param2/1/com.umeng.uapp/<接口名>`
- AK/SK 由 `umeng-cli login` 自动获取并加密缓存，无需手动配置 `apiKey` / `apiSecurity`

### 登录状态检查

```bash
umeng-cli whoami
```

### 登录要求

当接口返回未登录或登录态过期时，需要执行 `umeng-cli login --no-qr` 进行登录。

**AI Agent 执行登录的正确方式：**

> `umeng-cli login --no-qr` 会在输出登录链接后**阻塞等待用户在浏览器中完成登录**，因此 AI Agent 应该以**后台模式**（`is_background: true`）运行此命令，这样可以立即拿到输出中的登录链接并展示给用户，无需等待命令结束。命令会在用户完成登录后自动退出并保存凭证。

如果终端不支持显示二维码（如 AI Agent 终端、SSH 远程终端等），可以使用 `--no-qr` 参数，仅输出可点击的登录链接：

```bash
umeng-cli login --no-qr

# 输出:
# 🔄 正在生成登录链接...
# ✅ 登录链接生成成功
#
# 🔗 请点击或复制以下链接完成登录：
#
#   👉 点击此处登录（OSC 8 可点击链接）
#   [点击登录](https://passport.umeng.com/login?redirectURL=...)
#   https://passport.umeng.com/login?redirectURL=...
#
# ⏳ 等待登录...
# ✅ 授权成功！
# ✅ 登录完成！
```

### 获取 appkey

除 `getAllAppData` 外，其余 8 个接口均以 `appkey` 作为应用维度标识。

**获取路径**：
1. 直接要求用户提供 `appkey`
2. 若用户不知道，引导至友盟官网 https://www.umeng.com/ 登录后在应用管理后台复制
3. （进阶）可调用同 namespace 的 `umeng.uapp.getAppList` 搜索获取

> ⚠️ `umeng.uapp.getAllAppData` **无需 appkey**（返回当前账户下所有 App 合计指标），是账户总览专用入口。

## 通用调用格式

```bash
umeng-cli call '{
  "name": "umeng.uapp.<接口名>",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.<接口名>",
    "authType": "umeng-aksk"
  }
}' '<参数JSON>'
```

- 本 Skill 的 9 个接口均为 `GET` 方法
- `endpoint` 路径遵循统一格式 `param2/1/com.umeng.uapp/<接口名>`
- 参数 JSON 为空时传 `'{}'`（适用于 `getAllAppData`）

## 核心 4 指标定义

`getDailyData` / `getYesterdayData` / `getTodayData` / `getTodayYesterdayData` 四个单日快照接口共享同一响应结构 `DailyDataInfo`，其中"**核心 4 指标**"指同时返回的以下四个字段：

| 字段名 | 中文含义 |
|--------|----------|
| `activityUsers` | 活跃用户数（DAU） |
| `newUsers` | 新增用户数 |
| `launches` | 启动次数 |
| `totalUsers` | 总用户数（累计） |

> 第 5 个字段 `payUsers`（游戏付费用户数）仅在游戏 SDK 有值，非游戏应用恒为 0，不列入核心 4 指标。

## 接口路由表

### 账户维度（无需 appkey）

| 接口 | Endpoint | 功能 |
|------|----------|------|
| `umeng.uapp.getAllAppData` | `param2/1/com.umeng.uapp/umeng.uapp.getAllAppData` | 所有 App 合计的昨日+今日基础指标 + 昨日独立去重 + totalUsers |

### 单日快照（应用级）

| 接口 | Endpoint | 功能 |
|------|----------|------|
| `umeng.uapp.getDailyData` | `param2/1/com.umeng.uapp/umeng.uapp.getDailyData` | 指定日期核心 4 指标（支持 channel/version 过滤） |
| `umeng.uapp.getYesterdayData` | `param2/1/com.umeng.uapp/umeng.uapp.getYesterdayData` | 昨日核心 4 指标（便捷） |
| `umeng.uapp.getTodayData` | `param2/1/com.umeng.uapp/umeng.uapp.getTodayData` | 今日核心 4 指标（数据延迟，通常次日完整） |
| `umeng.uapp.getTodayYesterdayData` | `param2/1/com.umeng.uapp/umeng.uapp.getTodayYesterdayData` | 今日+昨日同时返回核心 4 指标 |

### 趋势分析（应用级）

| 接口 | Endpoint | 功能 |
|------|----------|------|
| `umeng.uapp.getActiveUsers` | `param2/1/com.umeng.uapp/umeng.uapp.getActiveUsers` | 时间范围内活跃用户趋势（支持 daily/weekly/monthly/7day/30day） |
| `umeng.uapp.getNewUsers` | `param2/1/com.umeng.uapp/umeng.uapp.getNewUsers` | 时间范围内新增用户趋势（daily/weekly/monthly） |
| `umeng.uapp.getLaunches` | `param2/1/com.umeng.uapp/umeng.uapp.getLaunches` | 时间范围内启动次数趋势（daily/weekly/monthly） |

### 使用时长（应用级）

| 接口 | Endpoint | 功能 |
|------|----------|------|
| `umeng.uapp.getDurations` | `param2/1/com.umeng.uapp/umeng.uapp.getDurations` | 指定日期使用时长分布 + 每次启动平均时长 |

> 💡 **排序与 Top N 由客户端完成**：本 Skill 9 个接口均不提供服务端排序参数，排序与截断需客户端（LLM 侧）在响应数据上完成。

---

## 操作

### 1. 获取所有 App 合计数据 (getAllAppData)

获取当前登录账户下**所有 App** 昨日和今日的基础统计数据，**无需 appkey**，**无需任何参数**。

**参数说明：** 无参数。

**调用示例：**

```bash
umeng-cli call '{
  "name": "umeng.uapp.getAllAppData",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getAllAppData",
    "authType": "umeng-aksk"
  }
}' '{}'
```

**返回格式：**

```json
{
  "allAppData": [
    {
      "todayActivityUsers": 12500,
      "todayNewUsers": 480,
      "todayLaunches": 38000,
      "yesterdayActivityUsers": 25600,
      "yesterdayNewUsers": 920,
      "yesterdayLaunches": 78200,
      "yesterdayUniqNewUsers": 890,
      "yesterdayUniqActiveUsers": 24100,
      "totalUsers": 1560000
    }
  ]
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `allAppData[].todayActivityUsers` | integer | 今日活跃用户（所有 App 合计） |
| `allAppData[].todayNewUsers` | integer | 今日新增用户（所有 App 合计） |
| `allAppData[].todayLaunches` | integer | 今日启动次数（所有 App 合计） |
| `allAppData[].yesterdayActivityUsers` | integer | 昨日活跃用户（所有 App 合计） |
| `allAppData[].yesterdayNewUsers` | integer | 昨日新增用户（所有 App 合计） |
| `allAppData[].yesterdayLaunches` | integer | 昨日启动次数（所有 App 合计） |
| `allAppData[].yesterdayUniqNewUsers` | integer | 昨日独立新增用户数（**跨 App 去重**） |
| `allAppData[].yesterdayUniqActiveUsers` | integer | 昨日独立活跃用户数（**跨 App 去重**） |
| `allAppData[].totalUsers` | integer | 总用户数（所有 App 合计） |

> 💡 **唯一提供跨 App 去重的接口**：`yesterdayUniqNewUsers` / `yesterdayUniqActiveUsers` 两个字段在其他应用级接口中拿不到，适合"账户下所有 App 昨天一共有多少独立活跃用户"这类问题。

---

### 2. 获取指定日期统计数据 (getDailyData)

获取指定 App 在特定日期的核心 4 指标。支持按 `channel` 或 `version` 过滤。

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appkey | string | 是 | 应用 ID |
| date | string | 是 | 查询日期，格式 `yyyy-MM-dd` |
| version | string | 否 | 版本名称（仅一个，含特殊字符需 urlEncode） |
| channel | string | 否 | 渠道名称（仅一个，含特殊字符需 urlEncode） |

**调用示例：**

```bash
# 查询某 App 在 2026-04-27 的核心 4 指标
umeng-cli call '{
  "name": "umeng.uapp.getDailyData",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getDailyData",
    "authType": "umeng-aksk"
  }
}' '{"appkey":"你的appkey","date":"2026-04-27"}'

# 查询指定渠道在某日的核心 4 指标
umeng-cli call '{"name":"umeng.uapp.getDailyData","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.uapp/umeng.uapp.getDailyData","authType":"umeng-aksk"}}' '{"appkey":"你的appkey","date":"2026-04-27","channel":"App%20Store"}'
```

**返回格式：**

```json
{
  "dailyData": {
    "date": "2026-04-27",
    "activityUsers": 25600,
    "newUsers": 920,
    "launches": 78200,
    "totalUsers": 1560000,
    "payUsers": 0
  }
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `dailyData.date` | string | 统计日期 |
| `dailyData.activityUsers` | integer | 活跃用户数（DAU） |
| `dailyData.newUsers` | integer | 新增用户数 |
| `dailyData.launches` | integer | 启动次数 |
| `dailyData.totalUsers` | integer | 总用户数（累计） |
| `dailyData.payUsers` | integer | 游戏付费用户数（仅游戏 SDK） |

---

### 3. 获取昨日统计数据 (getYesterdayData)

获取指定 App 昨日的核心 4 指标。相当于 `getDailyData` + `date=昨日`，但无需传日期。

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appkey | string | 是 | 应用 ID |

**调用示例：**

```bash
umeng-cli call '{
  "name": "umeng.uapp.getYesterdayData",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getYesterdayData",
    "authType": "umeng-aksk"
  }
}' '{"appkey":"你的appkey"}'
```

**返回格式：**

```json
{
  "yesterdayData": {
    "date": "2026-04-27",
    "activityUsers": 25600,
    "newUsers": 920,
    "launches": 78200,
    "totalUsers": 1560000,
    "payUsers": 0
  }
}
```

**返回字段说明**：字段结构与 `getDailyData.dailyData` 一致，外层 key 为 `yesterdayData`。

---

### 4. 获取今日统计数据 (getTodayData)

获取指定 App 今日的核心 4 指标。**注意数据延迟**：今日数据通常次日才完整，盘中查询可能为 0 或偏低。

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appkey | string | 是 | 应用 ID |

**调用示例：**

```bash
umeng-cli call '{
  "name": "umeng.uapp.getTodayData",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getTodayData",
    "authType": "umeng-aksk"
  }
}' '{"appkey":"你的appkey"}'
```

**返回格式：**

```json
{
  "todayData": {
    "date": "2026-04-28",
    "activityUsers": 12500,
    "newUsers": 480,
    "launches": 38000,
    "totalUsers": 1560480,
    "payUsers": 0
  }
}
```

**返回字段说明**：字段结构与 `getDailyData.dailyData` 一致，外层 key 为 `todayData`。

> ⚠️ **今日数据延迟**：友盟数据存在同步延迟，今日数据通常次日才完整。若用户强调"准确数据"，建议改用 `getYesterdayData`。

---

### 5. 获取今日+昨日对比数据 (getTodayYesterdayData)

一次调用同时返回今日和昨日的核心 4 指标，适合对比场景。

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appkey | string | 是 | 应用 ID |

**调用示例：**

```bash
umeng-cli call '{
  "name": "umeng.uapp.getTodayYesterdayData",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getTodayYesterdayData",
    "authType": "umeng-aksk"
  }
}' '{"appkey":"你的appkey"}'
```

**返回格式：**

```json
{
  "todayData": {
    "date": "2026-04-28",
    "activityUsers": 12500,
    "newUsers": 480,
    "launches": 38000,
    "totalUsers": 1560480,
    "payUsers": 0
  },
  "yesterdayData": {
    "date": "2026-04-27",
    "activityUsers": 25600,
    "newUsers": 920,
    "launches": 78200,
    "totalUsers": 1560000,
    "payUsers": 0
  }
}
```

**返回字段说明**：两个子对象结构均与 `getDailyData.dailyData` 一致。

---

### 6. 获取活跃用户趋势 (getActiveUsers)

获取指定 App 某个时间范围内的活跃用户数趋势。

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| appkey | string | 是 | - | 应用 ID |
| startDate | string | 是 | - | 起始日期 `yyyy-MM-dd` |
| endDate | string | 是 | - | 截止日期 `yyyy-MM-dd` |
| periodType | string | 否 | `daily` | `daily` / `weekly` / `monthly` / **`7day`** / **`30day`**（仅本接口额外支持 7day/30day） |

> ⚠️ **返回条数限制**：
> - `periodType = daily / 7day / 30day` 时，返回结果上限 **60 条**
> - `periodType = weekly` 时，返回结果上限 **8 条**
> - `periodType = monthly` 时，返回结果上限 **3 条**
> - 实际以接口为准。

**调用示例：**

```bash
# 查询近 7 天每日活跃用户趋势
umeng-cli call '{
  "name": "umeng.uapp.getActiveUsers",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getActiveUsers",
    "authType": "umeng-aksk"
  }
}' '{"appkey":"你的appkey","startDate":"2026-04-21","endDate":"2026-04-27","periodType":"daily"}'
```

**返回格式：**

```json
{
  "activeUserInfo": [
    {
      "date": "2026-04-21",
      "value": 24800,
      "dailyValue": [],
      "hourValue": []
    }
  ]
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `activeUserInfo[].date` | string | 统计日期 |
| `activeUserInfo[].value` | integer | 无渠道/无版本按天、按周、按月汇总值 |
| `activeUserInfo[].dailyValue[]` | NameValue[] | 本接口不含 channel/version 参数，通常为空数组 |
| `activeUserInfo[].hourValue[]` | integer[] | 按小时查询时返回（本接口不使用） |

---

### 7. 获取新增用户趋势 (getNewUsers)

获取指定 App 某个时间范围内的新增用户数趋势。

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| appkey | string | 是 | - | 应用 ID |
| startDate | string | 是 | - | 起始日期 `yyyy-MM-dd` |
| endDate | string | 是 | - | 截止日期 `yyyy-MM-dd` |
| periodType | string | 否 | `daily` | `daily` / `weekly` / `monthly` |

> ⚠️ 本接口**不支持** `7day` / `30day`（仅 `getActiveUsers` 支持）。

**调用示例：**

```bash
umeng-cli call '{
  "name": "umeng.uapp.getNewUsers",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getNewUsers",
    "authType": "umeng-aksk"
  }
}' '{"appkey":"你的appkey","startDate":"2026-04-21","endDate":"2026-04-27","periodType":"daily"}'
```

**返回格式：**

```json
{
  "newUserInfo": [
    {
      "date": "2026-04-21",
      "value": 880,
      "dailyValue": [],
      "hourValue": []
    }
  ]
}
```

**返回字段说明**：结构与 `getActiveUsers` 的 `activeUserInfo[]` 一致，外层 key 为 `newUserInfo`。

---

### 8. 获取启动次数趋势 (getLaunches)

获取指定 App 某个时间范围内的启动次数趋势。

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| appkey | string | 是 | - | 应用 ID |
| startDate | string | 是 | - | 起始日期 `yyyy-MM-dd` |
| endDate | string | 是 | - | 截止日期 `yyyy-MM-dd` |
| periodType | string | 否 | `daily` | `daily` / `weekly` / `monthly` |

> ⚠️ 本接口**不支持** `7day` / `30day`。

**调用示例：**

```bash
umeng-cli call '{
  "name": "umeng.uapp.getLaunches",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getLaunches",
    "authType": "umeng-aksk"
  }
}' '{"appkey":"你的appkey","startDate":"2026-04-21","endDate":"2026-04-27","periodType":"daily"}'
```

**返回格式：**

```json
{
  "launchInfo": [
    {
      "date": "2026-04-21",
      "value": 75200,
      "dailyValue": [],
      "hourValue": []
    }
  ]
}
```

**返回字段说明**：结构与 `getActiveUsers` 的 `activeUserInfo[]` 一致，外层 key 为 `launchInfo`。

---

### 9. 获取使用时长 (getDurations)

获取指定 App 某日的使用时长分布 + 每次启动平均时长。支持按 `channel` 或 `version` 过滤。

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| appkey | string | 是 | - | 应用 ID |
| date | string | 是 | - | 查询日期 `yyyy-MM-dd` |
| statType | string | 否 | `daily` | `daily`（按天） / `daily_per_launch`（按次） |
| channel | string | 否 | - | 渠道名称（仅一个，含特殊字符需 urlEncode） |
| version | string | 否 | - | 版本名称（仅一个，含特殊字符需 urlEncode） |

**调用示例：**

```bash
# 查询某日总体使用时长分布
umeng-cli call '{
  "name": "umeng.uapp.getDurations",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getDurations",
    "authType": "umeng-aksk"
  }
}' '{"appkey":"你的appkey","date":"2026-04-27"}'

# 按每次启动统计
umeng-cli call '{"name":"umeng.uapp.getDurations","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.uapp/umeng.uapp.getDurations","authType":"umeng-aksk"}}' '{"appkey":"你的appkey","date":"2026-04-27","statType":"daily_per_launch"}'
```

**返回格式：**

```json
{
  "durationInfos": [
    {"name": "0-3", "value": 5800, "percent": 0.23},
    {"name": "4-10", "value": 4200, "percent": 0.17},
    {"name": "11-30", "value": 3800, "percent": 0.15}
  ],
  "average": 185.5
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `durationInfos[].name` | string | 时间区间（单位：秒） |
| `durationInfos[].value` | integer | 该区间内的启动次数 / 用户数 |
| `durationInfos[].percent` | double | 该区间占总量的比例 |
| `average` | double | **每次启动的平均使用时长** |

> 💡 **"平均使用时长"语义**：`average` 即"每次启动平均时长"，对应旧 skill 的 `duration` 指标。如需看分布，读 `durationInfos[]`。

---

## 公共枚举与约束

### periodType 枚举（三个趋势接口差异）

| 值 | getActiveUsers | getNewUsers | getLaunches | 说明 |
|----|:---:|:---:|:---:|------|
| `daily` | ✅ | ✅ | ✅ | 按日（默认） |
| `weekly` | ✅ | ✅ | ✅ | 按周 |
| `monthly` | ✅ | ✅ | ✅ | 按月 |
| `7day` | ✅ | ❌ | ❌ | **仅 getActiveUsers 支持** |
| `30day` | ✅ | ❌ | ❌ | **仅 getActiveUsers 支持** |

**返回条数上限**（`getActiveUsers` 官方明确）：

| periodType | 上限 |
|------------|------|
| `daily` / `7day` / `30day` | 60 条 |
| `weekly` | 8 条 |
| `monthly` | 3 条 |

> `getNewUsers` / `getLaunches` 官方未明确标注上限，跨度过大时请分段查询。

### 日期格式

- `date` / `startDate` / `endDate` 统一使用 `yyyy-MM-dd`
- 今日数据有延迟，建议查询"昨日及以前"

### channel / version 单值限制

- `getDailyData` 与 `getDurations` 的 `channel` / `version` **只接受单个值**
- 多值对比需多次调用后由客户端聚合
- 若需查看某渠道/版本的**趋势**（时间范围），改用 `umeng-cli-uapp-channel-version` skill 的 `ByChannelOrVersion` 系列接口

### urlEncode 规则

- 含空格、中文、特殊字符的渠道名/版本号需做 URL 编码（percent-encoding）
- 例：`App Store` → `App%20Store`；`华为` → `%E5%8D%8E%E4%B8%BA`
- 纯英文字母/数字/点号（如 `Umeng` / `3.5` / `1.0.0`）**无需**编码

### 分页

本 Skill 9 个接口均**不支持**分页参数。

## 时间范围换算参考

| 常用语义 | startDate | endDate | 说明 |
|----------|-----------|---------|------|
| `yesterday` | 昨天 | 昨天 | 或直接用 `getYesterdayData` |
| `today` | 今天 | 今天 | 或直接用 `getTodayData` |
| `today_yesterday` | — | — | 直接用 `getTodayYesterdayData`（一次返回两天） |
| `last_7_days` | 今天 - 7 | 昨天 | 过去 7 天（含昨天，不含今天） |
| `last_30_days` | 今天 - 30 | 昨天 | 过去 30 天 |
| `last_90_days` | 今天 - 90 | 昨天 | 过去 90 天 |
| `last_week` | 上周周一 | 上周周日 | 按日明细，客户端可再算日均 |
| 指定日期 | 用户给出 | 同 startDate | 单日查询，直接用 `getDailyData` |

## 典型工作流

### 场景 1：账户级所有 App 合计（无需 appkey）

```
需求："我账户下所有 App 昨天一共多少 DAU / 新增 / 启动？"
1. getAllAppData()   // 无需任何参数
2. 读取 allAppData[0] 的 yesterdayActivityUsers / yesterdayNewUsers / yesterdayLaunches
3. 如用户问"去重后独立活跃用户" → 读 yesterdayUniqActiveUsers / yesterdayUniqNewUsers
4. 如用户问"总用户数" → 读 totalUsers
```

### 场景 2：昨日核心 4 指标一览

```
需求："某 App 昨天 DAU 多少？新增多少？启动多少？"
1. getYesterdayData(appkey)   // 最简路径，无需日期
2. 从 yesterdayData 读 activityUsers / newUsers / launches / totalUsers
3. 用自然语言总结关键数字
```

### 场景 3：今日 vs 昨日对比

```
需求："某 App 今天和昨天 DAU 对比？"
1. getTodayYesterdayData(appkey)   // 一次返回两天
2. 对比 todayData.activityUsers 与 yesterdayData.activityUsers
3. 计算同比增减 → 输出"今日比昨日 ±X%"
4. 提醒："今日数据通常次日才完整，盘中数据仅供参考"
```

### 场景 4：过去 7/30 天 DAU 趋势

```
需求："某 App 过去 7 天 DAU 趋势？"
1. 计算 startDate = today - 7, endDate = yesterday
2. getActiveUsers(appkey, startDate, endDate, periodType=daily)
3. 读取 activeUserInfo[].value 按日期列出趋势
4. 指出最高点/最低点，总结整体走势（上升/下降/持平）
```

### 场景 5：过去 N 天新增 + 启动趋势

```
需求："某 App 过去 30 天新增用户和启动次数走势？"
1. 计算 startDate/endDate
2. 并行调用：
   - getNewUsers(appkey, startDate, endDate, periodType=daily)
   - getLaunches(appkey, startDate, endDate, periodType=daily)
3. 合并两组趋势数据，按日期对齐
4. 总结新增走势 + 启动走势，如二者背离则指出（如启动涨但新增跌 → 老用户活跃回升）
```

### 场景 6：指定日期核心 4 指标

```
需求："某 App 在 2026-04-15 这天的数据是多少？"
1. getDailyData(appkey, date=2026-04-15)
2. 从 dailyData 读 activityUsers / newUsers / launches / totalUsers
3. 若用户指定渠道或版本：加 channel/version 参数（单值，必要时 urlEncode）
```

### 场景 7：使用时长分析

```
需求："某 App 昨日使用时长怎样？"
1. getDurations(appkey, date=yesterday)
2. 优先输出 average（每次启动平均时长，核心指标）
3. 附：durationInfos 分布 Top 3 区间（例如 0-3 秒 / 4-10 秒 / 11-30 秒）
4. 如用户强调"每次启动" → 传 statType=daily_per_launch 再查一次
```

## 边界条件与错误处理

- **未说 appkey**：除 `getAllAppData` 外，先询问用户 appkey；若用户不知道，引导至友盟后台查询或用 `umeng.uapp.getAppList`
- **appkey 无效**：响应非成功，提示「找不到该应用，请确认 appkey 是否正确或是否已开通 U-App」
- **返回数据为空**：`dailyData` / `yesterdayData` 等字段为空代表该日期暂无数据，建议换近期日期
- **今日数据为 0 或极低**：说明友盟数据存在延迟，今日数据通常次日才完整，建议改查昨日
- **periodType 误用 7day/30day**：仅 `getActiveUsers` 支持，用在 `getNewUsers` / `getLaunches` 上会失败
- **日期跨度过大**：注意各 periodType 返回条数上限（daily/7day/30day≤60、weekly≤8、monthly≤3），超过需分段查询
- **channel / version 含特殊字符忘记 urlEncode**：可能返回空结果或签名错误，要求做 URL 编码
- **`getDurations` 的 `statType`**：默认 `daily`；用户强调"每次启动"时用 `daily_per_launch`
- **未登录 / 登录态过期**：执行 `umeng-cli login --no-qr`（AI Agent 以后台模式运行并将链接展示给用户）

## 典型问法 → 接口/参数映射

| 典型问法 | 接口 | 关键参数 |
|----------|------|----------|
| "我所有 App 昨天一共多少 DAU？" | `getAllAppData` | 无参数，读 `yesterdayActivityUsers` |
| "所有 App 昨天独立活跃用户？" | `getAllAppData` | 无参数，读 `yesterdayUniqActiveUsers` |
| "某 App 昨天 DAU 多少？" | `getYesterdayData` | `appkey`，读 `yesterdayData.activityUsers` |
| "某 App 今天 DAU 多少？" | `getTodayData` | `appkey`，读 `todayData.activityUsers` |
| "某 App 今天和昨天 DAU 对比？" | `getTodayYesterdayData` | `appkey` |
| "某 App 在 2026-04-15 的数据？" | `getDailyData` | `appkey` + `date=2026-04-15` |
| "App Store 渠道昨天 DAU？" | `getDailyData` | `appkey` + `date=yesterday` + `channel=App%20Store` |
| "过去 7 天 DAU 趋势？" | `getActiveUsers` | 近 7 天，`periodType=daily` |
| "过去 30 天新增用户趋势？" | `getNewUsers` | 近 30 天，`periodType=daily` |
| "上周日均启动次数？" | `getLaunches` | 上周周一~周日，`periodType=daily`，客户端算均值 |
| "最近 30 天使用时长变化？" | `getDurations`（多次，每日一次） | 逐日 `date` 调用，读 `average` |
| "某 App 昨日使用时长分布？" | `getDurations` | `appkey` + `date=yesterday` |
| "某 App 累计总用户数？" | `getYesterdayData` | 读 `yesterdayData.totalUsers` |

### 旧 skill 参数等价对照

旧 `uapp-core-index` 的自定义参数与新接口的等价关系：

| 旧参数组合 | 新接口调用 |
|------------|-----------|
| `--metric dau --range yesterday` | `getYesterdayData` 读 `activityUsers` |
| `--metric new_users --range last_7_days` | `getNewUsers` 近 7 天 daily |
| `--metric launches --range last_week` | `getLaunches` 上周周一~周日 daily |
| `--metric duration --range last_30_days` | `getDurations` 逐日调用，读 `average` |
| `--metric dau --range today_yesterday` | `getTodayYesterdayData` |
| `--metric dau --range 2026-03-25` | `getDailyData` + `date=2026-03-25` |

## 注意事项

- 本 Skill **仅限只读查询**，不包含 `umeng.uapp.createApp` / `umeng.uapp.event.create` 等写入接口
- 所有接口均为 `GET` 方法
- `appkey` 到友盟官网 https://www.umeng.com/ 应用管理后台查询（`getAllAppData` 除外）
- **核心 4 指标**：`activityUsers`（DAU） / `newUsers` / `launches` / `totalUsers`；`payUsers` 仅游戏 SDK 有值
- **今日数据延迟**：今日数据通常次日才完整，盘中查询仅供参考
- **`total_users` 只在单日快照可得**：4 个单日快照接口都直接返回；趋势类 3 个接口不含 `totalUsers`，如需总用户趋势需拼接多日快照
- **`getAllAppData` 独有能力**：唯一提供跨 App 去重的 `yesterdayUniqNewUsers` / `yesterdayUniqActiveUsers` 字段
- **`duration` 指标语义**：核心场景推 `getDurations.average`（每次启动平均时长），分布场景看 `durationInfos[]`
- **`periodType` 差异**：`7day` / `30day` 仅 `getActiveUsers` 支持
- **`channel` / `version` 单值**：`getDailyData` / `getDurations` 仅接受一个值，多值需多次调用；如需趋势请用 `umeng-cli-uapp-channel-version`
- **urlEncode**：含空格/中文/特殊字符的渠道与版本名需要 URL 编码

## 快速参考

| # | 接口 | Endpoint（相对 baseUrl） | 必填参数 | 可选参数 | 维度 |
|---|------|--------------------------|----------|----------|------|
| 1 | `umeng.uapp.getAllAppData` | `param2/1/com.umeng.uapp/umeng.uapp.getAllAppData` | **无** | — | 账户（所有 App 合计） |
| 2 | `umeng.uapp.getDailyData` | `param2/1/com.umeng.uapp/umeng.uapp.getDailyData` | `appkey` + `date` | `channel` / `version` | 应用单日 |
| 3 | `umeng.uapp.getYesterdayData` | `param2/1/com.umeng.uapp/umeng.uapp.getYesterdayData` | `appkey` | — | 应用昨日 |
| 4 | `umeng.uapp.getTodayData` | `param2/1/com.umeng.uapp/umeng.uapp.getTodayData` | `appkey` | — | 应用今日 |
| 5 | `umeng.uapp.getTodayYesterdayData` | `param2/1/com.umeng.uapp/umeng.uapp.getTodayYesterdayData` | `appkey` | — | 应用今+昨 |
| 6 | `umeng.uapp.getActiveUsers` | `param2/1/com.umeng.uapp/umeng.uapp.getActiveUsers` | `appkey` + `startDate` + `endDate` | `periodType`（含 7day/30day） | 应用趋势 |
| 7 | `umeng.uapp.getNewUsers` | `param2/1/com.umeng.uapp/umeng.uapp.getNewUsers` | `appkey` + `startDate` + `endDate` | `periodType` | 应用趋势 |
| 8 | `umeng.uapp.getLaunches` | `param2/1/com.umeng.uapp/umeng.uapp.getLaunches` | `appkey` + `startDate` + `endDate` | `periodType` | 应用趋势 |
| 9 | `umeng.uapp.getDurations` | `param2/1/com.umeng.uapp/umeng.uapp.getDurations` | `appkey` + `date` | `statType` / `channel` / `version` | 应用时长 |

> 完整 uapp namespace 其他接口（如 `getRetentions` / `getChannelData` / `event.*` 等）请参考 [umeng-cli/reference/openapi/uapp.md](../../../umeng-cli/reference/openapi/uapp.md)。
> 渠道/版本维度（对比、Top N、趋势）的专门查询请使用 [umeng-cli-uapp-channel-version](../umeng-cli-uapp-channel-version/SKILL.md)。
