---
name: umeng-cli-uapm
description: 友盟应用性能监控（U-APM）数据查询技能，支持通过 umeng-cli call 调用友盟 APM OpenAPI（apm.openapi.umeng.com）的 8 个只读查询接口，涵盖今日/历史稳定性、启动性能、网络性能、原生页面、H5 页面、分钟级网络与稳定性数据。当用户需要查询应用崩溃率、启动耗时、网络请求性能、页面加载性能或分钟级实时数据时使用。
metadata:
  requires:
    bins: ["umeng-cli"]
  cliHelp: "umeng-cli call --help"
  install: "npm install -g @umengfe/umeng-cli"
  homepage: "https://github.com/umeng/umeng-cli"
---

# 友盟应用性能监控（U-APM）数据查询技能

> `umeng-cli` 是友盟提供的命令行程序，所有操作通过执行 `umeng-cli call` 命令完成。

查询友盟应用性能监控（U-APM）的统计数据，包括稳定性（崩溃、ANR、卡顿）、启动性能、网络性能、原生页面性能、H5 页面性能、分钟级实时监控等，共 **8 个只读查询接口**。

> **埋点上报：** AI Agent 在阅读本 Skill 文档后，请执行以下命令进行调用埋点上报：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapm"}'
> ```
>
> **Appkey 维度打点：** 当本轮任务中出现 Appkey（即接口入参 `dataSourceId`）的输入操作时，在拿到该 Appkey 之后、发起首个业务 API 调用之前，再追加执行一次带 appkey 的打点：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapm", "appkey":"<输入的Appkey>"}'
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

## 鉴权方式

- **authType**: `aliyun-aksk`（ACS3-HMAC-SHA256 V3 签名，友盟 OpenAPI 标准鉴权）
- **baseUrl**: `https://apm.openapi.umeng.com`
- **API Version**: `2022-02-14`（可省略，umeng-cli 默认值）
- AK/SK 由 `umeng-cli login` 自动获取和注入，无需手动配置 `apiKey` / `apiSecurity`

### 登录状态检查

可以通过 `umeng-cli whoami` 查看当前登录状态和登录用户信息：

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

### 获取 dataSourceId（appKey）

U-APM 所有接口均以 `dataSourceId` 作为应用维度标识，其值等同于友盟统计后台中的 **appKey**。

**获取路径**：
1. 打开友盟官网：https://www.umeng.com/
2. 登录后进入对应应用的管理后台
3. 在「应用信息」或「集成设置」中复制 appKey
4. 将 appKey 作为 `dataSourceId` 传入 API 请求

> 服务端 API 是以**应用维度授权**的，在调用接口前，确保已经为应用添加了接口权限。详情参考友盟[访问凭证](https://devs.umeng.com/api/credentials)文档。

## 通用调用格式

```bash
umeng-cli call '{
  "name": "apm.<Action>",
  "api": {
    "method": "GET",
    "baseUrl": "https://apm.openapi.umeng.com",
    "endpoint": "<pathname>",
    "authType": "aliyun-aksk"
  }
}' '<参数JSON>'
```

- **Action 可省略**，自动从 `endpoint` 路径最后一段推导（首字母大写，例如 `/stat/getTodayStatTrend` → `GetTodayStatTrend`）
- **version 可省略**，默认 `2022-02-14`
- 本 Skill 的 8 个接口均为 `GET` 方法
- 参数 JSON 为空时传 `'{}'`

## 接口路由表

### 稳定性（崩溃 / ANR / 卡顿）

| Action | Endpoint | 功能 |
|--------|----------|------|
| `GetTodayStatTrend` | `/stat/getTodayStatTrend` | 今日小时粒度稳定性趋势 |
| `GetStatTrend` | `/stat/getStatTrend` | 历史按天稳定性趋势 |
| `GetErrorMinuteStatTrend` | `/stat/GetErrorMinuteStatTrend` | 分钟粒度稳定性趋势 |

### 性能（启动 / 网络 / 页面）

| Action | Endpoint | 功能 |
|--------|----------|------|
| `GetLaunchTrend` | `/stat/getLaunchTrend` | 启动性能趋势（按天/小时） |
| `GetNetworkTrend` | `/stat/getNetworkTrend` | 网络性能趋势（按天/小时） |
| `GetNativePageTrend` | `/stat/getNativePageTrend` | 原生页面性能趋势（按天/小时） |
| `GetH5PageTrend` | `/stat/getH5PageTrend` | H5 页面性能趋势（按天/小时） |
| `GetNetworkMinuteTrend` | `/stat/getNetworkMinuteTrend` | 分钟粒度网络趋势 |

> ⚠️ **注意 endpoint 大小写**：`GetErrorMinuteStatTrend` 的 endpoint 首字母为**大写 G**（`/stat/GetErrorMinuteStatTrend`），与其他 7 个接口的 `getXxx` 风格不同。此为友盟官方文档原文，API 大小写敏感，**切勿擅自改为小写**。

---

## 操作

### 1. 获取今日稳定性趋势 (GetTodayStatTrend)

获取今日**小时粒度**的实时稳定性统计数据，用于监控当日崩溃/ANR/卡顿走势。

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| dataSourceId | string | 是 | - | 数据源 ID（即 appKey） |
| type | integer | 是 | - | 异常类型枚举，见下文「稳定性类型枚举」 |
| appVersion | string | 否（可选） | 全部 | 指定 App 版本，不传则统计全部版本 |

**调用示例：**

```bash
# 查询今日全部崩溃的小时级趋势
umeng-cli call '{
  "name": "apm.GetTodayStatTrend",
  "api": {
    "method": "GET",
    "baseUrl": "https://apm.openapi.umeng.com",
    "endpoint": "/stat/getTodayStatTrend",
    "authType": "aliyun-aksk"
  }
}' '{"dataSourceId":"5fb6001a73749c24fd9cb356","type":0}'

# 查询今日 Java/iOS 崩溃的指定版本趋势
umeng-cli call '{"name":"apm.GetTodayStatTrend","api":{"method":"GET","baseUrl":"https://apm.openapi.umeng.com","endpoint":"/stat/getTodayStatTrend","authType":"aliyun-aksk"}}' '{"dataSourceId":"5fb6001a73749c24fd9cb356","type":1,"appVersion":"1.0.2"}'
```

**返回格式：**

```json
{
  "success": true,
  "code": 200,
  "msg": "succeed in handling request",
  "data": [
    {
      "timePoint": "13:00",
      "errorCount": 120,
      "errorRate": 17.24,
      "affectedUserCount": 56,
      "affectedUserRate": 10.21
    }
  ]
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | boolean | 调用是否成功 |
| `code` | long | 状态码（200 成功） |
| `msg` | string | 异常描述 |
| `data` | array | 数据数组（按小时聚合） |
| `data[].timePoint` | string | 统计时间段（小时，如 `13:00`） |
| `data[].errorCount` | long | 错误数 |
| `data[].errorRate` | double | 错误率（百分比） |
| `data[].affectedUserCount` | long | 影响用户数 |
| `data[].affectedUserRate` | double | 影响用户占比（百分比） |

---

### 2. 获取历史稳定性趋势 (GetStatTrend)

获取历史**按天**稳定性统计数据，用于分析周/月崩溃率走势。

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| dataSourceId | string | 是 | - | 数据源 ID（即 appKey） |
| type | integer | 是 | - | 异常类型枚举，见「稳定性类型枚举」 |
| startDate | string | 否（建议必传） | 友盟默认 | 起始日期，`yyyy-MM-dd` |
| endDate | string | 否（建议必传） | 友盟默认 | 结束日期，`yyyy-MM-dd`，与起始日期**间隔不超过 90 天** |
| appVersion | string | 否（可选） | 全部 | 指定 App 版本 |

> ⚠️ 若不传 `startDate`/`endDate`，友盟返回默认范围，具体行为**以 API 响应为准**，建议显式传入以避免歧义。

**调用示例：**

```bash
# 查询 2025-01-01 ~ 2025-01-07 全部崩溃趋势
umeng-cli call '{
  "name": "apm.GetStatTrend",
  "api": {
    "method": "GET",
    "baseUrl": "https://apm.openapi.umeng.com",
    "endpoint": "/stat/getStatTrend",
    "authType": "aliyun-aksk"
  }
}' '{"dataSourceId":"5fb6001a73749c24fd9cb356","type":0,"startDate":"2025-01-01","endDate":"2025-01-07"}'
```

**返回格式：**

```json
{
  "success": true,
  "code": 200,
  "msg": "succeed in handling request",
  "data": [
    {
      "timePoint": "2025-01-01",
      "errorCount": 120,
      "errorRate": 25.6,
      "affectedUserCount": 52,
      "affectedUserRate": 10.3
    }
  ]
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `data[].timePoint` | string | 统计日期（如 `2025-01-01`） |
| `data[].errorCount` | long | 错误数 |
| `data[].errorRate` | double | 错误率 |
| `data[].affectedUserCount` | long | 影响用户数 |
| `data[].affectedUserRate` | double | 影响用户占比 |

---

### 3. 获取启动性能趋势 (GetLaunchTrend)

获取**按天或按小时**粒度的启动性能统计，含首次启动/冷启动/热启动三类耗时。

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dataSourceId | string | 是 | 数据源 ID（即 appKey） |
| timeUnit | string | 是 | 时间粒度：`day`（按天） / `hour`（按小时，仅支持 1 天范围） |
| startDate | string | 是 | 起始日期 `yyyy-MM-dd`，距今不超过 90 天 |
| endDate | string | 是 | 结束日期 `yyyy-MM-dd`，与 startDate 间隔不超过 90 天 |
| appVersion | string | 否（可选） | 指定 App 版本 |

**调用示例：**

```bash
# 查询近 7 天按天启动性能
umeng-cli call '{
  "name": "apm.GetLaunchTrend",
  "api": {
    "method": "GET",
    "baseUrl": "https://apm.openapi.umeng.com",
    "endpoint": "/stat/getLaunchTrend",
    "authType": "aliyun-aksk"
  }
}' '{"dataSourceId":"5fb6001a73749c24fd9cb356","timeUnit":"day","startDate":"2025-01-01","endDate":"2025-01-07"}'

# 查询某一天按小时启动性能
umeng-cli call '{"name":"apm.GetLaunchTrend","api":{"method":"GET","baseUrl":"https://apm.openapi.umeng.com","endpoint":"/stat/getLaunchTrend","authType":"aliyun-aksk"}}' '{"dataSourceId":"5fb6001a73749c24fd9cb356","timeUnit":"hour","startDate":"2025-01-07","endDate":"2025-01-07","appVersion":"1.0.2"}'
```

**返回格式：**

```json
{
  "success": true,
  "code": 200,
  "msg": "succeed in handling request",
  "data": [
    {
      "timePoint": "2025-01-01",
      "firstLaunchCount": 2495,
      "firstLaunchDuration": 3740.5,
      "coldLaunchCount": 2495,
      "coldLaunchDuration": 3784.5,
      "hotLaunchCount": 2495,
      "hotLaunchDuration": 1400.5
    }
  ]
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `data[].timePoint` | string | 时间段（日期或小时，取决于 `timeUnit`） |
| `data[].firstLaunchCount` | long | 首次启动次数 |
| `data[].firstLaunchDuration` | double | 首次启动平均耗时（ms） |
| `data[].coldLaunchCount` | long | 冷启动次数 |
| `data[].coldLaunchDuration` | double | 冷启动平均耗时（ms） |
| `data[].hotLaunchCount` | long | 热启动次数 |
| `data[].hotLaunchDuration` | double | 热启动平均耗时（ms） |

---

### 4. 获取网络性能趋势 (GetNetworkTrend)

获取**按天或按小时**粒度的网络性能统计。

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dataSourceId | string | 是 | 数据源 ID（即 appKey） |
| timeUnit | string | 是 | `day` / `hour` |
| startDate | string | 是 | 起始日期 `yyyy-MM-dd` |
| endDate | string | 是 | 结束日期 `yyyy-MM-dd`，间隔 ≤ 90 天 |
| appVersion | string | 否（可选） | 指定 App 版本 |

**调用示例：**

```bash
umeng-cli call '{
  "name": "apm.GetNetworkTrend",
  "api": {
    "method": "GET",
    "baseUrl": "https://apm.openapi.umeng.com",
    "endpoint": "/stat/getNetworkTrend",
    "authType": "aliyun-aksk"
  }
}' '{"dataSourceId":"5fb6001a73749c24fd9cb356","timeUnit":"day","startDate":"2025-01-01","endDate":"2025-01-07"}'
```

**返回格式：**

```json
{
  "success": true,
  "code": 200,
  "msg": "succeed in handling request",
  "data": [
    {
      "timePoint": "2025-01-01",
      "avgResponseTime": 1654.51,
      "avgCost": 4402.8,
      "avgTransformBytes": 3299.43,
      "requestPerMinute": 1.61
    }
  ]
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `data[].timePoint` | string | 时间段（日期或小时） |
| `data[].avgResponseTime` | double | 全部域名平均响应时间（ms） |
| `data[].avgCost` | double | 全部域名平均总耗时（ms） |
| `data[].avgTransformBytes` | double | 全部域名平均传输字节数 |
| `data[].requestPerMinute` | double | 全部域名平均吞吐量（次/分钟） |

---

### 5. 获取原生页面性能趋势 (GetNativePageTrend)

获取**按天或按小时**粒度的原生页面（Activity/Fragment/ViewController）性能统计。

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dataSourceId | string | 是 | 数据源 ID（即 appKey） |
| timeUnit | string | 是 | `day` / `hour` |
| startDate | string | 是 | 起始日期 `yyyy-MM-dd` |
| endDate | string | 是 | 结束日期 `yyyy-MM-dd`，间隔 ≤ 90 天 |
| appVersion | string | 否（可选） | 指定 App 版本 |

**调用示例：**

```bash
umeng-cli call '{
  "name": "apm.GetNativePageTrend",
  "api": {
    "method": "GET",
    "baseUrl": "https://apm.openapi.umeng.com",
    "endpoint": "/stat/getNativePageTrend",
    "authType": "aliyun-aksk"
  }
}' '{"dataSourceId":"5fb6001a73749c24fd9cb356","timeUnit":"day","startDate":"2025-01-01","endDate":"2025-01-07"}'
```

**返回格式：**

```json
{
  "success": true,
  "code": 200,
  "msg": "succeed in handling request",
  "data": [
    {
      "timePoint": "2025-01-01",
      "avgLoadDuration": 75.9,
      "loadCnt": 2460,
      "slowLoadRate": 99.837,
      "crashRate": 37.317
    }
  ]
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `data[].timePoint` | string | 时间段 |
| `data[].avgLoadDuration` | double | 页面平均加载时长（ms） |
| `data[].loadCnt` | long | 页面加载样本量 |
| `data[].slowLoadRate` | double | 页面慢加载率（%） |
| `data[].crashRate` | double | 页面崩溃率（%） |

---

### 6. 获取 H5 页面性能趋势 (GetH5PageTrend)

获取**按天或按小时**粒度的 H5 页面性能统计。友盟返回的指标覆盖面较广（22 个字段），默认展示 5 个核心字段，完整字段见下表。

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dataSourceId | string | 是 | 数据源 ID（即 appKey） |
| timeUnit | string | 是 | `day` / `hour` |
| startDate | string | 是 | 起始日期 `yyyy-MM-dd` |
| endDate | string | 是 | 结束日期 `yyyy-MM-dd`，间隔 ≤ 90 天 |
| appVersion | string | 否（可选） | 指定 App 版本 |

**调用示例：**

```bash
umeng-cli call '{
  "name": "apm.GetH5PageTrend",
  "api": {
    "method": "GET",
    "baseUrl": "https://apm.openapi.umeng.com",
    "endpoint": "/stat/getH5PageTrend",
    "authType": "aliyun-aksk"
  }
}' '{"dataSourceId":"5fb6001a73749c24fd9cb356","timeUnit":"day","startDate":"2025-01-01","endDate":"2025-01-07"}'
```

**返回格式（节选核心字段）：**

```json
{
  "success": true,
  "code": 200,
  "msg": "succeed in handling request",
  "data": [
    {
      "timePoint": "2025-01-01",
      "dns": 50.16,
      "tcp": 150.18,
      "firstByte": 472.57,
      "domReady": 1881.96,
      "loadFinish": 4741.44
    }
  ]
}
```

**核心返回字段（推荐默认展示）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `data[].timePoint` | string | 时间段 |
| `data[].dns` | double | 平均 DNS 查询时间（ms） |
| `data[].tcp` | double | 平均 TCP 连接时间（ms） |
| `data[].firstByte` | double | 平均首字节时间（ms） |
| `data[].domReady` | double | 平均 DOM Ready 时间（ms） |
| `data[].loadFinish` | double | 平均页面完全加载时间（ms） |

**完整返回字段（共 22 个，按需取用）：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `data[].timePoint` | string | 时间段 |
| `data[].logCnt` | long | 样本量 |
| `data[].appCache` | double | 平均检查缓存时间（ms） |
| `data[].dns` | double | 平均 DNS 查询时间（ms） |
| `data[].tcp` | double | 平均 TCP 连接时间（ms） |
| `data[].ssl` | double | 平均 SSL 建连时间（ms） |
| `data[].ttfb` | double | 平均首字节响应时间（ms） |
| `data[].contentTrans` | double | 平均内容传输时间（ms） |
| `data[].analyzeDOM` | double | 平均 DOM 解析时间（ms） |
| `data[].loadResource` | double | 平均资源加载时间（ms） |
| `data[].loadEvent` | double | 平均事件加载时间（ms） |
| `data[].loadFinish` | double | 平均页面完全加载时间（ms） |
| `data[].firstByte` | double | 平均首字节时间（ms） |
| `data[].unload` | double | 平均卸载页面时间（ms） |
| `data[].redirect` | double | 平均重定向时间（ms） |
| `data[].domReady` | double | 平均 DOM Ready 时间（ms） |
| `data[].fp` | double | 平均首次绘制时间（ms） |
| `data[].fcp` | double | 平均首次内容绘制时间（ms） |
| `data[].tti` | double | 平均页面可交互时间（ms） |
| `data[].oneSecondRate` | double | 1 秒快开比 |
| `data[].twoSecondRate` | double | 2 秒快开比 |
| `data[].fiveSecondRate` | double | 5 秒慢开比 |

---

### 7. 获取分钟粒度网络趋势 (GetNetworkMinuteTrend)

获取**分钟粒度**实时网络统计数据，用于故障快速定位。

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dataSourceId | string | 是 | 数据源 ID（即 appKey） |
| startTime | string | 是 | 开始时间，精确到分钟，格式 `yyyy-MM-dd HH:mm`，**最多返回 startTime 后 10 分钟**的数据 |

> ⚠️ 此接口**没有 `type` 参数**（与分钟级稳定性接口不同）。

**调用示例：**

```bash
umeng-cli call '{
  "name": "apm.GetNetworkMinuteTrend",
  "api": {
    "method": "GET",
    "baseUrl": "https://apm.openapi.umeng.com",
    "endpoint": "/stat/getNetworkMinuteTrend",
    "authType": "aliyun-aksk"
  }
}' '{"dataSourceId":"5fb6001a73749c24fd9cb356","startTime":"2025-01-07 09:07"}'
```

**返回格式：**

```json
{
  "success": true,
  "code": 200,
  "msg": "succeed in handling request",
  "data": [
    {
      "timePoint": "2025-01-07 09:08",
      "requestCount": 1200,
      "errorCount": 120
    }
  ]
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `data[].timePoint` | string | 分钟粒度时间段 |
| `data[].requestCount` | long | 请求数量 |
| `data[].errorCount` | long | 错误数 |

---

### 8. 获取分钟粒度稳定性趋势 (GetErrorMinuteStatTrend)

获取**分钟粒度**实时稳定性统计，用于故障告警与快速定位崩溃高发时刻。

> ⚠️ **endpoint 首字母大写**：`/stat/GetErrorMinuteStatTrend`（G 为大写，与其他接口不一致但为友盟官方原文）。

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| dataSourceId | string | 是 | 数据源 ID（即 appKey） |
| type | integer | 是 | 异常类型枚举，见「稳定性类型枚举」 |
| startTime | string | 是 | 开始时间 `yyyy-MM-dd HH:mm`，最多返回后 10 分钟数据。当天 01 点前可查昨天；01 点后仅支持当天 |

**调用示例：**

```bash
umeng-cli call '{
  "name": "apm.GetErrorMinuteStatTrend",
  "api": {
    "method": "GET",
    "baseUrl": "https://apm.openapi.umeng.com",
    "endpoint": "/stat/GetErrorMinuteStatTrend",
    "authType": "aliyun-aksk"
  }
}' '{"dataSourceId":"5fb6001a73749c24fd9cb356","type":0,"startTime":"2025-01-07 09:07"}'
```

**返回格式：**

```json
{
  "success": true,
  "code": 200,
  "msg": "succeed in handling request",
  "data": [
    {
      "timePoint": "2025-01-07 09:08",
      "errorCount": 120,
      "launchCount": 1200
    }
  ]
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `data[].timePoint` | string | 分钟粒度时间段 |
| `data[].errorCount` | long | 错误数 |
| `data[].launchCount` | long | 启动次数 |

---

## 稳定性类型枚举（type 参数）

适用接口：`GetTodayStatTrend` / `GetStatTrend` / `GetErrorMinuteStatTrend`

| 值 | 含义 | 适用平台 |
|----|------|----------|
| `0` | 全部崩溃（默认推荐） | Android / iOS |
| `1` | Java/iOS 崩溃 | Android / iOS |
| `2` | Native 崩溃 | Android / iOS |
| `3` | ANR | 仅 Android |
| `4` | 自定义异常 | Android / iOS |
| `5` | 卡顿 | Android / iOS |

> `type` 为 **integer** 类型（不是 string），且为**必填**参数。

## 时间范围说明

| 场景 | 限制 |
|------|------|
| 按天/小时接口（`GetStatTrend` / `GetLaunchTrend` / `GetNetworkTrend` / `GetNativePageTrend` / `GetH5PageTrend`） | `startDate` 距今 ≤ 90 天，`endDate - startDate` ≤ 90 天 |
| 按小时粒度（`timeUnit=hour`） | 仅支持**单日**查询（`startDate == endDate`） |
| 分钟级接口（`GetNetworkMinuteTrend` / `GetErrorMinuteStatTrend`） | 最多返回 `startTime` 后 **10 分钟**数据 |
| 分钟级稳定性昨日查询 | 仅在**当天 01:00 之前**可查昨天；01:00 之后仅支持当天 |
| 今日接口（`GetTodayStatTrend`） | 仅当日小时粒度 |

## 典型工作流

### 场景 1：排查当日崩溃高发时段

```
1. GetTodayStatTrend (type=0)
   → 找出 errorRate / errorCount 最高的小时
2. GetErrorMinuteStatTrend (type=0, startTime=<异常小时开始>)
   → 定位到具体分钟，发现崩溃集中时刻
3. （可选）GetErrorMinuteStatTrend (type=1/2/3 逐类排查)
   → 定位崩溃类型（Java/Native/ANR）
```

### 场景 2：分析版本崩溃率对比

```
1. GetStatTrend (type=0, appVersion="1.0.1", startDate=近 7 天, endDate=近 7 天)
2. GetStatTrend (type=0, appVersion="1.0.2", startDate=近 7 天, endDate=近 7 天)
   → 对比两版本 errorRate / affectedUserRate
3. 如发现新版本异常升高：
   → GetStatTrend (type=1/2/3) 进一步按崩溃类型拆解
```

### 场景 3：分析启动性能与网络性能关联

```
1. GetLaunchTrend (timeUnit=day, startDate/endDate=近 7 天)
   → 观察 coldLaunchDuration 趋势
2. GetNetworkTrend (timeUnit=day, 相同日期)
   → 观察 avgResponseTime / avgCost 趋势
3. 若启动耗时与网络耗时同步升高 → 疑似启动期网络请求拖慢
   → 按 hour 粒度复查某天：
     GetLaunchTrend (timeUnit=hour, startDate=endDate=具体日期)
     GetNetworkTrend (timeUnit=hour, startDate=endDate=具体日期)
```

### 场景 4：H5 页面加载性能分析

```
1. GetH5PageTrend (timeUnit=day, startDate/endDate=近 7 天)
   → 核心字段：loadFinish / domReady / firstByte
2. 若 loadFinish 明显偏高：
   → 分析细分阶段（dns / tcp / ssl / ttfb / contentTrans / loadResource）
   → 定位瓶颈是 DNS / 建连 / 首字节 / 资源加载
3. 结合 oneSecondRate / twoSecondRate / fiveSecondRate 评估整体体验分布
```

## 边界条件与错误处理

- **未登录 / 登录态过期**：响应码非 200 或提示 `unauthorized`，执行 `umeng-cli login --no-qr`（AI Agent 以后台模式运行并将链接展示给用户）
- **参数校验错误**：检查 `type` 是否为 integer（不是 string）、日期格式是否为 `yyyy-MM-dd`、分钟时间是否为 `yyyy-MM-dd HH:mm`
- **90 天窗口越界**：按日期接口若 `startDate` 距今或 `endDate - startDate` 超过 90 天，会被拒绝
- **小时粒度跨天**：`timeUnit=hour` 时 `startDate` 必须等于 `endDate`，否则视为参数错误
- **分钟级接口时效**：`startTime` 必须是**最近时段**，过旧时间会无数据；稳定性接口跨天仅 01:00 前允许查昨天
- **应用未授权**：服务端 API 是应用维度授权的，未授权应用会返回错误码——需到友盟后台为该应用添加 U-APM 接口权限
- **data 为空数组**：代表该时段无任何上报，非错误

## 注意事项

- 本 Skill **仅限只读查询**，不包含符号表上传（`GetSymUploadParam` / `UploadSymbolFile` / `DeleteSymRecords`）与告警方案更新（`UpdateAlertPlan`），如需使用请参考 [umeng-cli/reference/openapi/uapm.md](../../../umeng-cli/reference/openapi/uapm.md)
- 所有接口均为 `GET` 方法
- `dataSourceId` 即友盟统计后台的 **appKey**，到 https://www.umeng.com/ 后台查询
- 同一调用可通过 `appVersion` 参数按版本过滤；不传则统计**全部版本**
- endpoint 大小写敏感，特别注意 `/stat/GetErrorMinuteStatTrend`（G 大写）和 `/stat/getH5PageTrend`（P 大写）
- 分钟级接口**单次返回最多 10 分钟**，若需更长时段需分段多次调用

## 快速参考

| Action | Endpoint | 必填参数 | 返回粒度 |
|--------|----------|----------|----------|
| `GetTodayStatTrend` | `/stat/getTodayStatTrend` | `dataSourceId` + `type` | 当日小时 |
| `GetStatTrend` | `/stat/getStatTrend` | `dataSourceId` + `type`（建议传日期） | 按天 |
| `GetLaunchTrend` | `/stat/getLaunchTrend` | `dataSourceId` + `timeUnit` + `startDate` + `endDate` | 按天/小时 |
| `GetNetworkTrend` | `/stat/getNetworkTrend` | `dataSourceId` + `timeUnit` + `startDate` + `endDate` | 按天/小时 |
| `GetNativePageTrend` | `/stat/getNativePageTrend` | `dataSourceId` + `timeUnit` + `startDate` + `endDate` | 按天/小时 |
| `GetH5PageTrend` | `/stat/getH5PageTrend` | `dataSourceId` + `timeUnit` + `startDate` + `endDate` | 按天/小时 |
| `GetNetworkMinuteTrend` | `/stat/getNetworkMinuteTrend` | `dataSourceId` + `startTime` | 分钟（最多 10 分钟） |
| `GetErrorMinuteStatTrend` | `/stat/GetErrorMinuteStatTrend` | `dataSourceId` + `type` + `startTime` | 分钟（最多 10 分钟） |
