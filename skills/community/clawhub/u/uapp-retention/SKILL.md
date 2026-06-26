---
name: umeng-cli-uapp-retention
description: 友盟 U-App 留存率查询技能，支持通过 umeng-cli call 调用友盟 OpenAPI（gateway.open.umeng.com）的 1 个只读留存接口，覆盖新增/活跃用户的次日/3日/7日/14日/30日留存率查询、版本与渠道维度的留存对比分析。当用户需要查询应用留存率、次日留存、7日留存、版本/渠道留存对比时使用。
metadata:
  requires:
    bins: ["umeng-cli"]
  cliHelp: "umeng-cli call --help"
  install: "npm install -g @umengfe/umeng-cli"
  homepage: "https://github.com/umeng/umeng-cli"
---

# 友盟 U-App 留存率查询技能

> `umeng-cli` 是友盟提供的命令行程序，所有操作通过执行 `umeng-cli call` 命令完成。

查询友盟 U-App（移动统计）的新增/活跃用户留存率，覆盖两类核心需求：

- **留存趋势**：某 App 在时间范围内每日新增/活跃用户的次日、3日、7日、14日、30日留存率
- **维度对比**：按版本或渠道过滤单维度留存；多版本/多渠道对比由客户端循环调用

共 **1 个只读查询接口**（`umeng.uapp.getRetentions`）。版本列表 / 渠道列表的枚举能力由 `umeng-cli-uapp-channel-version` 提供，本 Skill 不重复收纳。

> **埋点上报：** AI Agent 在阅读本 Skill 文档后，请执行以下命令进行调用埋点上报：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapp-retention"}'
> ```
>
> **Appkey 维度打点：** 当本轮任务中出现 Appkey 的输入操作时，在拿到该 Appkey 之后、发起首个业务 API 调用之前，再追加执行一次带 appkey 的打点：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapp-retention", "appkey":"<输入的Appkey>"}'
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

- 用户询问某 App 某时间段的次日/3日/7日/14日/30日留存率
- 用户询问某版本或某渠道的留存表现
- 用户请求多版本或多渠道的留存对比
- 用户询问活跃用户留存（非默认的新增用户留存）
- 关键词：留存、留存率、次日留存、7日留存、30日留存、留存趋势、版本留存、渠道留存、新增用户留存、活跃用户留存

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

本 Skill 的 1 个接口以 `appkey` 作为应用维度标识。

**获取路径**：
1. 直接要求用户提供 `appkey`
2. 若用户不知道，引导至友盟官网 https://www.umeng.com/ 登录后在应用管理后台复制
3. （进阶）调用同 namespace 的 `umeng.uapp.getAppList`，或使用 `uapp-assets` Skill 搜索

## 通用调用格式

```bash
umeng-cli call '{
  "name": "umeng.uapp.getRetentions",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getRetentions",
    "authType": "umeng-aksk"
  }
}' '<参数JSON>'
```

- 本 Skill 的接口为 `GET` 方法
- `endpoint` 路径遵循统一格式 `param2/1/com.umeng.uapp/<接口名>`
- 所有请求均需 `appkey`

## 核心概念

### retentionRate 数组索引表（本 Skill 文档核心）

`umeng.uapp.getRetentions` 的响应 `retentionInfo[].retentionRate` 是一个**定长数组**，每个元素分别对应**不同的留存窗口**（从安装/活跃之日向后的若干天）。索引映射如下：

| 留存窗口 | 自然语言 | `retentionRate` 数组索引 | 取值单位 |
|----------|----------|:---:|:---:|
| 次日留存 | "次日"、"1日" | `retentionRate[0]` | 小数（0~1） |
| 3日留存 | "3日"、"三日" | `retentionRate[1]` | 小数（0~1） |
| 7日留存 | "7日"、"一周"、"周留存" | `retentionRate[2]` | 小数（0~1） |
| 14日留存 | "14日"、"两周"、"双周留存" | `retentionRate[3]` | 小数（0~1） |
| 30日留存 | "30日"、"月留存" | `retentionRate[4]` | 小数（0~1） |

> ⚠️ **索引不是接口参数**：想看哪个留存窗口，是**客户端后处理**（对 `retentionRate[i]` 取值），不是通过请求参数过滤。一次调用返回所有 5 个窗口的留存值。

**提取示例（jq / LLM 侧）：**

```bash
# 取每日的次日留存
jq '.retentionInfo[] | {date, d1: .retentionRate[0]}'

# 取每日的 7 日留存
jq '.retentionInfo[] | {date, d7: .retentionRate[2]}'

# 同时拉出 1/7/30 日
jq '.retentionInfo[] | {date, d1: .retentionRate[0], d7: .retentionRate[2], d30: .retentionRate[4]}'
```

### type = newUser vs activeUser

| `type` | 含义 | `totalInstallUser` 字段含义 |
|--------|------|------------------------------|
| `newUser`（默认） | 新增用户留存率：当日新增用户在后续 N 天中回流的比例 | 当日**新增**用户数（作为留存基数） |
| `activeUser` | 活跃用户留存率：当日活跃用户在后续 N 天中再次活跃的比例 | 当日**安装**用户数（注意：即使 `type=activeUser`，该字段仍然是"当日安装用户数"，不是活跃用户基数） |

> ⚠️ **`totalInstallUser` 语义恒定**：无论 `type` 为 `newUser` 还是 `activeUser`，`totalInstallUser` 字段始终为「当日安装/新增用户数」。若要分析"活跃基数"，请使用 `umeng-cli-uapp-core-index` 的 `getActiveUsers` 接口。

## 接口路由表

| 接口 | Endpoint | 功能 |
|------|----------|------|
| `umeng.uapp.getRetentions` | `param2/1/com.umeng.uapp/umeng.uapp.getRetentions` | 获取 App 新增/活跃用户在时间范围内的留存率数据（含次日/3日/7日/14日/30日 5 个窗口） |

### 与本 skill 相邻能力的边界

| 能力 | 归属 Skill | 说明 |
|------|-----------|------|
| 枚举应用的**版本列表** | `umeng-cli-uapp-channel-version` 的 `umeng.uapp.getVersionData` | 本 Skill 不重复收纳；两处定义对应同一接口 |
| 枚举应用的**渠道列表** | `umeng-cli-uapp-channel-version` 的 `umeng.uapp.getChannelData` | 同上 |
| 活跃用户基数 / DAU | `umeng-cli-uapp-core-index` 的 `getActiveUsers` | `type=activeUser` 时的 `totalInstallUser` 非活跃基数 |
| 新增用户基数 | `umeng-cli-uapp-core-index` 的 `getNewUsers` | 留存分子/分母解释时若需独立查询新增基数可配合使用 |

---

## 操作

### 获取 App 留存率 (getRetentions)

获取指定 App 在时间范围内的**新增/活跃用户留存率**，一次返回次日/3日/7日/14日/30日 5 个窗口的留存值。

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| appkey | string | 是 | - | 应用 ID |
| startDate | string | 是 | - | 起始日期 `yyyy-MM-dd` |
| endDate | string | 是 | - | 截止日期 `yyyy-MM-dd` |
| periodType | string | 否 | `daily` | 聚合粒度：`daily` / `weekly` / `monthly` |
| channel | string | 否 | - | 渠道名称（**仅限单个**；含空格/中文需 urlEncode） |
| version | string | 否 | - | 版本名称（**仅限单个**；含空格/中文需 urlEncode） |
| type | string | 否 | `newUser` | 留存类型：`newUser`（新增用户留存）/ `activeUser`（活跃用户留存） |

**调用示例：**

```bash
# 基础：过去 7 天的新增用户留存（默认 daily 聚合）
umeng-cli call '{
  "name": "umeng.uapp.getRetentions",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getRetentions",
    "authType": "umeng-aksk"
  }
}' '{"appkey":"你的appkey","startDate":"2026-04-21","endDate":"2026-04-27"}'

# 活跃用户留存
umeng-cli call '{"name":"umeng.uapp.getRetentions","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.uapp/umeng.uapp.getRetentions","authType":"umeng-aksk"}}' '{"appkey":"你的appkey","startDate":"2026-04-21","endDate":"2026-04-27","type":"activeUser"}'

# 按版本过滤（版本号为纯数字 / 点号时无需编码）
umeng-cli call '{"name":"umeng.uapp.getRetentions","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.uapp/umeng.uapp.getRetentions","authType":"umeng-aksk"}}' '{"appkey":"你的appkey","startDate":"2026-04-21","endDate":"2026-04-27","version":"2.0.11001"}'

# 按渠道过滤（"App Store" 含空格，必须 urlEncode）
umeng-cli call '{"name":"umeng.uapp.getRetentions","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.uapp/umeng.uapp.getRetentions","authType":"umeng-aksk"}}' '{"appkey":"你的appkey","startDate":"2026-04-21","endDate":"2026-04-27","channel":"App%20Store"}'

# 按周聚合
umeng-cli call '{"name":"umeng.uapp.getRetentions","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.uapp/umeng.uapp.getRetentions","authType":"umeng-aksk"}}' '{"appkey":"你的appkey","startDate":"2026-02-01","endDate":"2026-04-27","periodType":"weekly"}'

# 中文渠道（华为）
umeng-cli call '{"name":"umeng.uapp.getRetentions","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.uapp/umeng.uapp.getRetentions","authType":"umeng-aksk"}}' '{"appkey":"你的appkey","startDate":"2026-04-21","endDate":"2026-04-27","channel":"%E5%8D%8E%E4%B8%BA"}'
```

**返回格式：**

```json
{
  "retentionInfo": [
    {
      "date": "2026-04-21",
      "totalInstallUser": 132,
      "retentionRate": [0.3561, 0.2727, 0.1462, 0.0914, 0.0619]
    },
    {
      "date": "2026-04-22",
      "totalInstallUser": 145,
      "retentionRate": [0.3890, 0.2870, 0.1580, 0.0960, 0.0680]
    }
  ]
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `retentionInfo[].date` | string | 统计日期（`periodType=weekly` 时为周起始日，`monthly` 时为月份） |
| `retentionInfo[].totalInstallUser` | integer | 当日（周/月）安装用户数，作为留存基数分母 |
| `retentionInfo[].retentionRate[]` | double[] | **定长 5 项留存率数组**，索引依次为 `[0]=次日, [1]=3日, [2]=7日, [3]=14日, [4]=30日`，单位为小数（需乘 100 换算成百分比） |

> 💡 **读数建议**：LLM 在向用户呈现留存率时，将小数 `0.3561` 换算为 `35.61%` 更易理解；当数组某项为 `null` / 空时，说明该窗口尚未到期（见下文「边界条件」）。

---

## 公共约束

### 日期格式与范围换算

- `startDate` / `endDate` 统一使用 `yyyy-MM-dd`
- 本 Skill **不提供 `--range yesterday/last_7_days/...` 语法糖**：客户端自行按当前日期换算，常用映射如下：

| 自然语言 | `startDate` | `endDate` |
|----------|-------------|-----------|
| 昨天 | `today - 1` | `today - 1` |
| 过去 7 天 | `today - 7` | `today - 1` |
| 过去 30 天 | `today - 30` | `today - 1` |
| 最近一个月 | `today - 30` | `today - 1` |
| 上周 | 上周一 | 上周日 |

### periodType 聚合

| 取值 | 说明 |
|------|------|
| `daily`（默认） | 每日一条记录，留存率按每日安装用户池计算 |
| `weekly` | 每周一条记录，`date` 为周起始日 |
| `monthly` | 每月一条记录 |

> 与 `umeng-cli-uapp-event` 的 7 个接口「全部不支持 `periodType`」形成对比，本接口**原生支持** `daily/weekly/monthly`。

### 分页

- **本 Skill 接口不支持分页**，一次调用即返回完整时间段的 `retentionInfo[]`
- 大时间窗口查询直接传 `startDate`/`endDate` 即可

### channel / version 过滤

- 均**仅限单个取值**；不支持传入多个用逗号/数组
- 多版本、多渠道对比 → 客户端循环多次调用（见「典型工作流」）
- 想枚举可用版本/渠道 → 使用 `umeng-cli-uapp-channel-version` 的 `getVersionData` / `getChannelData`

### urlEncode 规则

以下场景需要对值做 URL 编码（percent-encoding）：

- `channel`：含空格 / 中文 / 特殊字符
- `version`：一般纯数字 + 点号无需编码；但含字母组合或特殊后缀（如 `2.0-beta`）时建议编码

示例：

| 原值 | 编码后 |
|------|--------|
| `App Store` | `App%20Store` |
| `华为` | `%E5%8D%8E%E4%B8%BA` |
| `应用宝` | `%E5%BA%94%E7%94%A8%E5%AE%9D` |
| `2.0.11001` | `2.0.11001`（无需编码） |

### retentionRate 空值与"今日"规则

- 接口文档明示：「**不包含今日**」——留存率的分子需要"安装日之后第 N 天"实际发生，若 N 天尚未过去，对应索引位可能为 `null` / `0`
- 例如今天是 `2026-04-27`，查询 `date=2026-04-25` 的留存：
  - `retentionRate[0]`（次日，对应 `2026-04-26`）：**有值**
  - `retentionRate[1]`（3日，对应 `2026-04-28`）：**还未到期，通常为 null 或 0**
- LLM 在摘要时应避免把 `0` 误读为"留存率 0%"，需判断窗口是否已到期

### 返回数据为空的常见原因

- 时间范围过新（含今日）：留存数据需要相应留存天数后才能生成
- `version` / `channel` 拼写错误或大小写不匹配
- `version` / `channel` 含空格/中文但未做 urlEncode
- appkey 所属应用在该时间段内无新增/活跃用户

## 典型工作流

### 工作流 1：基础留存趋势（含索引抽取）

```
需求："过去 30 天的次日留存怎么样？"
1. 客户端计算 startDate = today - 30, endDate = today - 1
2. getRetentions(appkey, startDate, endDate)  ← 一次拿到 5 个窗口
3. 客户端对 retentionInfo[] 逐项取 retentionRate[0]（次日）
4. 汇总：日均次日留存率、最高/最低点、整体趋势
5. 可选：同一数组取 retentionRate[2]（7日）/ [4]（30日）并行展示
```

### 工作流 2：多留存窗口对比（同时间段 1/7/30 日）

```
需求："过去 30 天的 1日、7日、30日留存对比曲线"
1. getRetentions(appkey, last_30_days)  ← 仍是 1 次调用
2. 客户端对每个 retentionInfo[i]：
   - d1 = retentionRate[0]
   - d7 = retentionRate[2]
   - d30 = retentionRate[4]
3. 输出 3 条时间序列（同一 X 轴，3 条 Y 曲线）
4. 摘要：三窗口的均值与下降幅度（如 d1 35% → d7 14% → d30 6%）
5. 注意：越后期的窗口在末期天数上越可能 null（尚未到期）
```

### 工作流 3：版本留存对比（客户端并行循环）

```
需求："3.2 和 3.1 版本的次日留存对比"
1. （可选）先用 umeng-cli-uapp-channel-version 的 getVersionData 确认版本存在
2. 对每个版本 v in ["3.2", "3.1"]：
   - getRetentions(appkey, last_7_days, version=v)
3. 客户端汇总：
   - 对齐 retentionInfo[].date
   - 提取各自 retentionRate[0]
4. 输出对比：两条次日留存曲线；均值差异、峰值差异
5. 提醒：每个版本的 totalInstallUser 可能差异大，须在报告中标注基数
```

### 工作流 4：渠道留存对比（客户端并行循环）

```
需求："GooglePlay 和 AppStore 的 7日留存对比"
1. （可选）先用 umeng-cli-uapp-channel-version 的 getChannelData 确认渠道存在
2. 对每个渠道 c in ["GooglePlay", "App Store"]：
   - urlEncode(c) → "GooglePlay" / "App%20Store"
   - getRetentions(appkey, last_7_days, channel=<encoded>)
3. 对齐 date，提取 retentionRate[2]（7日）
4. 输出双渠道 7 日留存对比 + 基数（totalInstallUser）
5. 多渠道（≥3）场景同理，循环调用 N 次并合并
```

## 边界条件与错误处理

- **未说 appkey**：先询问；若用户不知道，引导至友盟后台查询或用 `uapp-assets` Skill
- **未说 App 名**：先询问，不要猜测；App 名无法匹配时提示「可用 uapp-assets 查询应用列表」
- **appkey 无效**：响应非成功，提示「找不到该应用，请确认 appkey 是否正确或是否已开通 U-App 统计」
- **查询今天/昨天留存**：说明留存数据需要相应留存天数后才能生成；次日留存至少要到"第二天才能计算"，建议 `last_7_days` 或更早的起始日，并在摘要中提示"末期天数的中长窗口尚未到期"
- **`retentionRate` 某项为 0 / null**：区分两种情况：
  - 该日留存窗口尚未到期（如今天查 30 日留存）→ 告知用户「尚未到期，暂无数据」
  - 该日确实留存为 0 → 按字面呈现
- **版本/渠道拼写错误**：响应返回空 `retentionInfo[]`；建议通过 `umeng-cli-uapp-channel-version` 查询可用列表
- **`type=activeUser` 时 `totalInstallUser` 字段**：仍是"当日安装用户数"，不是"当日活跃用户数"；若用户需要活跃用户留存的分母基数，请用 `umeng-cli-uapp-core-index` 的 `getActiveUsers` 另取
- **大时间范围 + periodType=daily**：一次返回可能上百条记录；客户端建议分段摘要而非全量堆叠
- **多版本/多渠道对比传了单参数**：本接口不支持 `versions`/`channels` 复数形式，也不支持逗号分隔；必须客户端循环
- **未登录 / 登录态过期**：执行 `umeng-cli login --no-qr`（AI Agent 以后台模式运行并将链接展示给用户）

## 典型问法 → 接口/参数映射

| 典型问法 | 调用 | 关键参数 & 客户端后处理 |
|----------|------|--------------------------|
| "昨天 DAU 的次日留存多少？" | `getRetentions` | `startDate`=`endDate`=昨天；取 `retentionRate[0]` |
| "过去 7 天的 7 日留存趋势？" | `getRetentions` | `last_7_days`；取 `retentionRate[2]` |
| "最近一个月的 30 日留存？" | `getRetentions` | `last_30_days`；取 `retentionRate[4]` |
| "活跃用户的次日留存？" | `getRetentions` | `type=activeUser`；取 `retentionRate[0]` |
| "按周看的 7 日留存趋势？" | `getRetentions` | `periodType=weekly` + 较长时间窗（如 last_90_days）；取 `retentionRate[2]` |
| "3.2 版本的次日留存？" | `getRetentions` | `version=3.2`；取 `retentionRate[0]` |
| "GooglePlay 渠道的 7 日留存？" | `getRetentions` | `channel=GooglePlay`；取 `retentionRate[2]` |
| "App Store 渠道的次日留存？" | `getRetentions` | `channel=App%20Store`（urlEncode）；取 `retentionRate[0]` |
| "3.2 版本在 GooglePlay 的次日留存？" | `getRetentions` | 同时传 `version` + `channel`；取 `retentionRate[0]` |
| "3.2 和 3.1 版本的次日留存对比？" | `getRetentions` × 2 | 客户端循环，每版本 1 次；对齐日期 |
| "GooglePlay 和 AppStore 的 7 日留存对比？" | `getRetentions` × 2 | 客户端循环，每渠道 1 次；对齐日期 |
| "1/7/30 日留存对比曲线" | `getRetentions` × 1 | 同一响应取 `retentionRate[0/2/4]` 三条曲线 |
| "有哪些版本？"（用于选留存筛选） | 指向 `umeng-cli-uapp-channel-version` | `getVersionData` |
| "有哪些渠道？"（用于选留存筛选） | 指向 `umeng-cli-uapp-channel-version` | `getChannelData` |

### 旧 skill 参数等价对照

旧 `uapp-retention` 的 CLI 参数与新接口的等价关系：

| 旧 CLI 参数组合 | 新接口调用 |
|-----------------|------------|
| `--retention-day 1` | 调 `getRetentions`，客户端取 `retentionRate[0]` |
| `--retention-day 3` | 客户端取 `retentionRate[1]` |
| `--retention-day 7` | 客户端取 `retentionRate[2]` |
| `--retention-day 14` | 客户端取 `retentionRate[3]` |
| `--retention-day 30` | 客户端取 `retentionRate[4]` |
| `--retention-type new`（默认） | `type=newUser` |
| `--retention-type active` | `type=activeUser` |
| `--period day/week/month` | `periodType=daily/weekly/monthly` |
| `--range yesterday` | 客户端换算 `startDate=endDate=today-1` |
| `--range last_7_days` | 客户端换算 `startDate=today-7, endDate=today-1` |
| `--range last_30_days` | 客户端换算 `startDate=today-30, endDate=today-1` |
| `--version "X"` | `version=X`（含空格/特殊字符先 urlEncode） |
| `--channel "X"` | `channel=X`（含空格/中文先 urlEncode） |
| `--list-versions` | 指向 `umeng-cli-uapp-channel-version` 的 `getVersionData`（本 Skill 不收纳） |
| `--list-channels` | 指向 `umeng-cli-uapp-channel-version` 的 `getChannelData` |
| `--compare-versions "3.2,3.1"` | 客户端循环：每版本调 1 次 `getRetentions`，对齐日期合并 |
| `--compare-channels "GooglePlay,AppStore"` | 客户端循环：每渠道调 1 次 `getRetentions`，对齐日期合并 |
| `--json` 输出 | `umeng-cli call` 原生输出即 JSON，无需额外开关 |
| `--app NAME` → `appkey` 解析 | 用户直接给 `appkey`，或通过 `uapp-assets` 搜索 |

## 注意事项

- 本 Skill **仅覆盖 1 个只读查询接口** `umeng.uapp.getRetentions`；不涉及任何写入或事件管理
- 接口为 `GET` 方法；`appkey` 到友盟官网 https://www.umeng.com/ 应用管理后台查询
- **核心概念**：留存窗口（次日/3日/7日/14日/30日）对应 `retentionRate[]` 数组索引 `[0/1/2/3/4]`，不是接口参数
- **`type` 仅两个取值**：`newUser`（默认）/ `activeUser`；其他字符串会被接口拒绝或返回默认
- **`periodType` 支持 `daily`/`weekly`/`monthly`**：与 `umeng-cli-uapp-event` 的 7 个接口「全部不支持 periodType」形成差异
- **`channel` / `version` 仅限单个**：多维度对比由客户端循环调用实现
- **urlEncode**：`channel` 含空格/中文必须编码；`version` 含特殊字符时建议编码
- **`totalInstallUser` 语义恒定**：无论 `type=newUser` 或 `activeUser`，均为"当日安装用户数"（非活跃基数）
- **"不含今日"与未到期窗口**：查询含今日或临近日期时，后段留存窗口可能为 `null` / `0`（尚未到期），LLM 摘要时需区分"尚未到期"与"真实为 0"
- **版本 / 渠道枚举**：去 `umeng-cli-uapp-channel-version` 用 `getVersionData` / `getChannelData`（本 Skill 不重复收纳）
- **响应体无 `page` / `totalPage`**：本接口不支持分页，单次调用返回完整区间

## 快速参考

| # | 接口 | Endpoint（相对 baseUrl） | 必填参数 | 可选参数 | 维度 |
|---|------|--------------------------|----------|----------|------|
| 1 | `umeng.uapp.getRetentions` | `param2/1/com.umeng.uapp/umeng.uapp.getRetentions` | `appkey` + `startDate` + `endDate` | `periodType`（daily/weekly/monthly）/ `channel`（单个）/ `version`（单个）/ `type`（newUser/activeUser） | 留存率（响应 `retentionRate[0/1/2/3/4]` 分别为 1/3/7/14/30 日留存） |

> 完整 uapp namespace 其他接口（如 `getActiveUsers` / `getNewUsers` / `getChannelData` 等）请参考 [umeng-cli/reference/openapi/uapp.md](../../../umeng-cli/reference/openapi/uapp.md)。
> 版本 / 渠道列表枚举请使用 [umeng-cli-uapp-channel-version](../umeng-cli-uapp-channel-version/SKILL.md)；核心指标查询请使用 [umeng-cli-uapp-core-index](../umeng-cli-uapp-core-index/SKILL.md)；自定义事件查询请使用 [umeng-cli-uapp-event](../umeng-cli-uapp-event/SKILL.md)。
