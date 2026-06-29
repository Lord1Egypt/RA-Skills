---
name: xpeng-monitor
description: |
  小鹏汽车综合数据监控工具，持续集成各市场、各维度的数据。
  XPeng comprehensive data monitor, aggregating metrics across markets and dimensions.

  目前已支持（其他数据持续补充中）：
  - 【中国市场】各车型配置版本的交付周期（单位：周）
  - 【欧洲市场】纯电动车（BEV）日更交付/上牌销量，支持最近 12 个月环比对比

  Currently supported (more data to be added):
  - China: vehicle model delivery lead time / wait time in weeks
  - Europe: BEV daily registration/delivery volume with 12-month MoM comparison

  当用户提到以下任何场景时，都应使用此 Skill：

  **中国市场交付周期：**
  - "小鹏交付周期"、"小鹏交付时间"、"小鹏提车周期"、"小鹏提车时间"、"小鹏交付监控"、"小鹏交付周期监控"
  - "小鹏购车要等多久"、"小鹏订车到提车要多久"、"小鹏什么时候能提车"、"小鹏等车多久"
  - "小鹏G6交付多久"、"小鹏GX交付周期"、"G7等几周"、"小鹏M03多久能到"、"P7+提车时间"
  - "查询小鹏车型交付"、"小鹏各配置交付周期"、"小鹏交付数据"
  - 小鹏具体车型名称：G6、G9、GX、G7、P7、P7+、M03、X9、F30 等结合交付/提车/等车话题
  - XPeng delivery time, XPeng delivery lead time, XPeng delivery wait, XPeng wait time, XPeng delivery period, XPeng delivery estimate, XPeng delivery weeks, XPeng delivery schedule
  - When will my XPeng be delivered, XPeng how long to deliver

  **欧洲市场交付销量：**
  - "小鹏欧洲销量"、"小鹏欧洲交付"、"小鹏欧洲上牌"、"小鹏海外销量"、"小鹏欧洲数据"
  - "XPeng欧洲销量"、"XPeng欧洲交付"、"XPeng Europe delivery"、"XPeng Europe sales"
  - "小鹏欧洲市场"、"小鹏出海"、"XPeng EU"、"XPeng海外"
  - "小鹏欧洲纯电动"、"小鹏BEV"、"XPeng registrations"、"XPeng European market data"
  - XPeng Europe registrations, XPeng EU sales, XPeng European market data, XPeng BEV Europe

  **通用入口：**
  - "/xpeng-monitor"

  **隐式命中规则：**
  - 当用户询问小鹏汽车某个/某些车型的交付等待时间、提车周期、订车到交付需要多久时，即使没有明确说"交付周期"，也使用此 Skill
  - 当用户询问小鹏在欧洲的销量、交付数据、上牌量、市场份额时，也使用此 Skill
  - When a user asks about XPeng vehicle delivery time, wait time, or lead time for any model, even without explicitly saying "delivery", use this Skill
  - When a user asks about XPeng Europe delivery/sales/registration volume or market share, use this Skill
---

# 小鹏汽车综合数据监控 Skill

## 目标

本 Skill 用于获取小鹏汽车的综合数据，持续集成各市场、各维度的指标。目前已包含以下两大模块（其他数据待补充）：

- **第一部分 · 中国市场交付周期**：查询指定小鹏车型各配置版本的交付周期信息（单位：**周**）。数据来源：小鹏官方商城 API（`store.xiaopeng.com`）。
- **第二部分 · 欧洲市场纯电动车日更数据**：监控 XPENG 在欧洲披露日更数据国家的 BEV 每日上牌/交付销量，输出最近 12 个月的日更明细与环比对比。数据来源：eu-evs.com。

所有网络请求通过 `scripts/` 目录下的 Node.js 脚本执行（`node <script>.js`），不使用 Python、curl 或其他方式。脚本目录：`scripts/`（相对于 skill 根目录）。

## 执行前先确定命中功能

收到用户问题后，**先根据用户问题和上下文判断需要命中的功能列表，再根据命中的功能列表获取对应的数据**。不要无差别地执行所有脚本。

功能命中规则：

| 功能 | 命中条件（满足任一即可） |
|------|----------------------|
| **第一部分 · 中国交付周期** | 用户提到交付周期、交付时间、提车周期、提车时间、等几周、交付等待、订车到提车、中国/国内交付等；或指定了具体车型（如 G6、GX、M03、P7）并询问交付相关话题 |
| **第二部分 · 欧洲日更数据** | 用户提到欧洲销量、欧洲交付、欧洲上牌、海外销量、BEV 注册量、XPeng Europe、EU sales 等；或询问小鹏在海外/欧洲的市场表现 |

- 如果只命中一个功能，直接执行对应部分的流程。
- 如果同时命中两个功能（如"小鹏国内交付周期和欧洲销量怎么样"），分别执行两个部分的流程，各自独立获取数据后汇总展示。
- 如果无法确定命中哪个功能，使用 AskUserQuestion 询问用户想查看哪类数据。

---

## 全局执行铁律（适用于所有数据获取）

以下规则优先级最高，凌驾于各部分的具体流程之上，任何阶段都必须遵守：

1. **所有 HTTP 请求一律通过 `scripts/` 下的 Node.js 脚本发起**，严禁使用 curl、Python、WebFetch、WebSearch、Bash 直接拼接 URL 或任何其他方式直接请求数据源。数据源的反爬策略、登录态、cookie 管理全部封装在脚本内，绕过脚本会导致 bot 检测触发、账号被封或拿到不一致的数据。
2. **脚本失败只能"重跑同一脚本"或"把错误原样上报"**，不得改用替代手段。即脚本返回 `ERROR|...` 或非零退出码时，允许间隔片刻后重跑同一脚本（最多 2~3 次）；重跑仍失败则将错误信息转述给用户并停止，**不得**临时起意用 curl/WebFetch/Python 重新请求。
3. **瞬时网络错误脚本已内置重试**（socket hang up、ECONNRESET、连接超时等会在脚本内部退避重试 3 次），agent 不需要、也不应该对瞬时网络错误自行编排重试逻辑；只有当脚本输出明确的 `ERROR|...` 时才需要 agent 介入。
4. **判断脚本是否可用，只看 stdout**：正常数据、`LOGIN_REQUIRED`、`ERROR|...` 都在 stdout。不要因为 stderr 有输出或退出码非零就认定脚本不可用。

---

# 第一部分：中国市场交付周期数据

## 脚本列表

| 脚本文件 | 用途 | 用法 |
|---------|------|------|
| `fetch_car_series.js` | 获取全部车型列表 | `node fetch_car_series.js` |
| `fetch_car_versions.js` | 获取指定车型的配置版本列表 | `node fetch_car_versions.js <carSeriesCode>` |
| `fetch_delivery_period.js` | 查询指定配置的交付周期 | 见下方详细说明 |

## fetch_delivery_period.js 用法

该脚本根据车型类型使用不同的 API 策略：

| 模式 | 用法 | 适用车型 | 输出格式 |
|------|------|---------|---------|
| Case 1 单版本 | `node fetch_delivery_period.js <carVersionCode> <carSeriesCode>` | GX、M03、P7 系列 | `OK\|min\|max\|carName` |
| Case 2 单版本 | `node fetch_delivery_period.js <carVersionCode> <carSeriesCode>` | 其他车型 | `OK\|min\|max\|carName` |
| Case 2 批量 | `node fetch_delivery_period.js <carSeriesCode> --all` | 其他车型（推荐） | `versionCode\|OK\|min\|max\|carName`（每行一个版本） |

脚本自动根据 carSeriesCode 判断使用 Case 1 还是 Case 2。

## 流程步骤

### 步骤一：获取全部车型列表

运行 `scripts/fetch_car_series.js`，解析输出获取全部车型列表。

输出格式（每行一个）：`序号|carSeriesCode|carSeriesName`

### 步骤二：识别用户想监控的车型

根据用户的问题识别用户想要监控哪几个（一个或多个）`carSeriesCode`。匹配时支持用户说车型名称（如"G6"）或完整名称（如"2026款G6"），做模糊匹配。

如果用户没有提供具体车型，或提供的车型名无法匹配，则使用 AskUserQuestion 工具展示全部车型列表并让用户选择：

> | 序号 | carSeriesCode | carSeriesName |
> |------|--------------|---------------|
> | 1    | GX           | GX            |
> | 2    | M03_2026     | M03           |
> | ...  | ...          | ...           |
>
> 请告诉我您想查询哪些车型的交付周期？可以提供车型名称或序号，支持多个（如：1,3,5 或 GX,G7）。

### 步骤三：获取每个车型的配置版本列表

针对用户选中的每个 `carSeriesCode`，运行 `scripts/fetch_car_versions.js <carSeriesCode>`。

输出格式（每行一个）：`carVersionCode|carVersionName`

### 步骤四：查询每个配置版本的交付周期

根据车型是否为 GX/M03/P7 系列，使用不同的查询方式。脚本会根据 `carSeriesCode` 自动判断。

#### Case 1：GX/M03/P7 系列车型

针对每个 `carVersionCode`，运行：
```
node scripts/fetch_delivery_period.js <carVersionCode> <carSeriesCode>
```

**脚本内部逻辑：**
1. 请求 `listSpecGroupAndSpecList?carVersionSn=${carVersionCode}` 获取可选配置规格列表
2. 遍历每个配置组，在 `specList` 中找到 `isDefault=1` 的默认规格，收集其 `carSpecificationCode`
3. 组成排序后的 `carSpecificationCode` 列表，作为该车型的默认配置规格（列表可以为空，表示无默认选中配置）
4. 请求 `listCarInfoList?carVersionSn=${carVersionCode}` 获取 SKU 列表
5. 对每个 SKU，提取其 `specList` 中所有 `specCode` 组成列表并排序
6. 找到 `specCode` 列表与默认配置列表完全匹配的 SKU（应唯一）
7. 输出该 SKU 的 `minDeliveryPeriod`、`maxDeliveryPeriod` 和 `carName`

输出格式：`OK|minDeliveryPeriod|maxDeliveryPeriod|carName` 或 `NO_DATA|0|0|` 或 `ERROR|0|0|`

#### Case 2：其他车型

**推荐方式（批量查询）：** 运行一次即可获取该车型所有版本的交付周期：
```
node scripts/fetch_delivery_period.js <carSeriesCode> --all
```

**脚本内部逻辑：**
1. 请求 `allInOne?carSeriesSn=${carSeriesCode}` 获取全部数据
2. 从响应中提取 `carSpecGroupVoMap`（配置规格）和 `carInfoVoMap`（SKU 信息），两者均以 `carVersionCode` 为 key
3. 对每个 `carVersionCode`：
   - 从 `carSpecGroupVoMap` 中找到默认配置规格（同 Case 1 的匹配逻辑）
   - 从 `carInfoVoMap` 中找到匹配的 SKU
   - 输出该版本的交付周期

输出格式（每行一个版本）：`carVersionCode|OK|minDeliveryPeriod|maxDeliveryPeriod|carName` 或 `carVersionCode|NO_DATA|0|0|`

**备选方式（单版本查询）：** 也可按版本逐一查询：
```
node scripts/fetch_delivery_period.js <carVersionCode> <carSeriesCode>
```
输出格式同 Case 1：`OK|minDeliveryPeriod|maxDeliveryPeriod|carName` 或 `NO_DATA|0|0|` 或 `ERROR|0|0|`

#### 如何选择 Case

脚本自动判断，规则如下：
- **Case 1**：`carSeriesCode` 以 `GX`、`M03`、`P7`（不区分大小写）开头
- **Case 2**：其他所有车型

### 步骤五：输出结果

以表格形式输出每个车型下的交付周期。脚本输出中最后一个 `|` 后的字段即为 `carName`，**必须将完整的 carName 原样输出到表格的"车辆名称"列，不得省略或截断**。

| 车型 | 配置版本 | 车辆名称 | 最短交付周期 | 最长交付周期 |
|------|---------|---------|------------|------------|
| GX   | 1585 四驱 Max | GX 1585 四驱 Max 仰望绿 | 4周 | 6周 |
| GX   | 665 Max | GX 665 Max 星云白 | 6周 | 8周 |

## 执行约束

1. **严格遵守流程**：按步骤一至步骤五顺序执行，不跳过任何步骤。
2. **单位为周**：交付周期单位是**周**，不要理解为"天"或做任何转换。
3. **默认配置匹配**：交付周期取默认配置规格对应 SKU 的数据，不是取 SKU 列表第一个元素。
4. **统一使用 Node.js 脚本**：所有请求通过 `scripts/` 下的脚本执行，不使用 curl 或 Python。
5. **Case 2 优先批量**：对于非 GX/M03/P7 车型，优先使用 `--all` 模式一次获取全部版本，减少 API 请求次数。
6. **容错**：某个车型请求失败时，输出该车型查询失败，继续查询其他车型，不中断整个流程。
7. **完整输出 carName**：脚本输出的最后一个字段是 `carName`，输出表格时必须将其完整填入"车辆名称"列，不得省略、截断或简写。

## 异常处理

| 异常场景 | 处理方式 |
|---------|---------|
| 脚本执行报错（socket hang up / 网络错误 / 非零退出码） | **先重跑同一脚本 2~3 次**（间隔片刻）；仍失败则将错误转述给用户并停止。严禁改用 curl/Python/WebFetch 等替代方式（见「全局执行铁律」）|
| navigationBar API 请求失败 | 报告网络错误，无法继续 |
| 用户提供的车型不在列表中 | 提示用户重新选择，展示完整列表 |
| 配置页 HTML 中未找到版本信息 | 该车型输出"暂无配置信息" |
| listSpecGroupAndSpecList / allInOne API 返回失败 | 该配置输出"查询失败"，继续其他配置 |
| listCarInfoList API 返回空 data | 该配置输出"N/A" |
| 默认配置未匹配到任何 SKU | 该配置输出"N/A" |
| listCarInfoList API 请求失败 | 该配置输出"查询失败"，继续其他配置 |

---

# 第二部分：欧洲市场纯电动车日更数据

## 数据来源

eu-evs.com（欧洲纯电动车 BEV 注册量数据）。

**重要范围说明：** ALL_DAILY 视图仅汇总**披露日更数据的少数欧洲国家**（并非全欧洲）。也就是说，本 Skill 输出的欧洲销量数据只覆盖这些日更国家，不能代表 XPeng 在整个欧洲市场的全貌，也不应直接解读为「欧洲总销量」。

URL 模板：`https://eu-evs.com/brands/XPENG/ALL_DAILY/Models-Daily/Year/${year}`

页面返回 HTML 表格（id=`latestDateTable`），包含每个日期各车型的注册量。

## 脚本列表

| 脚本文件 | 用途 | 用法 |
|---------|------|------|
| `xpeng_eu_daily.js` | 获取最近 12 个月每日各车型交付销量明细，支持 JSON 和 markdown 报告两种输出 | `node xpeng_eu_daily.js [year] [--report] [--email <email> --password <password>]` |

## xpeng_eu_daily.js 说明

获取指定年份的数据，自动找到最新日期，从最新月开始往前取满 12 个月，返回每个月每个日期的各车型明细和日汇总。

**用法**：
```
node scripts/xpeng_eu_daily.js [year]                  # 输出 JSON（含 daily/monthly_full/monthly_partial）
node scripts/xpeng_eu_daily.js [year] --report         # 输出 markdown 报告（①②③ 表格，默认入口）
node scripts/xpeng_eu_daily.js [year] --email <email> --password <password>
```
- `year` 可选，默认当前年份
- `--report` 输出 3 个 markdown 表格（月度环比 / 全月总销量 / 车型明细），供 LLM 直接展示并附加 ④ 综合分析；**默认入口优先用此模式**
- `--email` / `--password` 可选，用于登录 eu-evs.com（见下方登录流程）

**跨年处理（自动）**：12 个月通常跨越两个自然年（如最新月为 2026-06，则范围为 2025-07 至 2026-06），脚本自动获取所需年份并合并。

**登录态与 bot 检测**：eu-evs.com 对未登录 / 被判定为 bot / 会话失效的请求会 302 重定向到各种页面（已观察到 `/bots`、`/login`、`/onlyNamed` 等，后续可能继续变化）。由于成功的数据请求固定返回 200，脚本对数据页的**任何 302** 都视为需要登录，不再枚举重定向目标。处理逻辑如下：
1. 首先尝试直接请求数据页（复用 `scripts/.eu-session.json` 中已保存的会话）
2. 如果被拦截（302）且未提供凭据，向 **stdout** 输出 `LOGIN_REQUIRED`（退出码 2）
3. 如果提供了 `--email` 和 `--password`，自动执行登录流程（GET /login 获取 CSRF token → POST /login 提交凭据），登录后自动重试
4. 登录成功后，会话 cookie 保存到 `scripts/.eu-session.json`，后续运行自动复用
5. 初始取数和跨年取数两个阶段共用同一套拦截处理；已登录过则不重复登录

**JSON 模式输出格式**（不加 `--report` 时，stdout 输出单行紧凑 JSON）：

```json
{
  "meta": {
    "latest_date": "YYYY-MM-DD",        // 最新数据日期
    "latest_day": D,                     // 最新日期是几号（PARTIAL 截止日）
    "partial_range": "1-D",              // PARTIAL 对比范围
    "models": ["车型1", ...],            // 基准车型列表（车型名可能含逗号如 "P7,P7I"）
    "months": ["YYYY-MM", ...]           // 12 个月，正序（最旧在前）
  },
  "daily": [                             // 每日明细，每个日期一个对象
    {"date":"YYYY-MM-DD","month":"YYYY-MM","sales":{"车型1":N,...},"total":N},
    ...
  ],
  "monthly_full": [                      // 全月汇总（该月所有有数据日期累加）
    {"month":"YYYY-MM","days":N,"sales":{...},"total":N},
    ...
  ],
  "monthly_partial": [                   // 同范围汇总（仅 day ≤ latest_day，跨月公平对比用）
    {"month":"YYYY-MM","days":N,"range":"1-D","sales":{...},"total":N},
    ...
  ]
}
```

**关键说明**：
- **车型用 JSON 键**：通过 `sales.G6`、`sales["P7,P7I"]` 访问，彻底避免列错位。
- **预汇总已内置**：`monthly_partial` 直接给出每月 1-D 范围累加，做环比无需手动累加；`monthly_full` 用于全月对比；`daily` 用于单日/趋势分析。
- **跨年车型对齐**：以输入年份的车型列表（`meta.models`）为基准，跨年数据中缺失车型补 0，新增车型仅当出现在基准列表中才显示。

## 流程步骤

### 步骤一：运行 daily 脚本（默认 `--report` 模式）

默认运行 `node scripts/xpeng_eu_daily.js --report`（当前年份），直接获取 ①②③ 三个 markdown 表格。如果用户指定了年份（如"查看 2025 年数据"），传入年份参数：`node scripts/xpeng_eu_daily.js 2025 --report`。

**何时用 JSON 模式（不加 `--report`）**：用户有非默认需求（某车型长期趋势、单日异常定位、工作日/周末分析、同比对比等），需要基于 `daily` / `monthly_full` 灵活计算时，去掉 `--report` 运行获取 JSON。

### 步骤一·补充：处理 LOGIN_REQUIRED（必须检测）

**检测规则（强制）**：每次运行 `xpeng_eu_daily.js` 后，**必须检查 stdout 是否包含 `LOGIN_REQUIRED`**。这是脚本要求 agent 介入获取凭据的唯一信号，**不得当成普通错误直接结束**，必须走下面的询问流程。

信号特征：
- 出现在 **stdout**（不是 stderr，不要只看 stderr 或退出码）
- 退出码为 2（仅作辅助，以 stdout 字符串为准）
- 可能在初始取数阶段或跨年取数阶段出现，任意阶段出现都同样处理

触发场景：eu-evs.com 将数据页请求 302 重定向到其他页面（`/bots`、`/login`、`/onlyNamed` 等），都意味着需要登录。脚本对数据页的任何 302 都视为需要登录。

处理步骤：

1. 使用 AskUserQuestion 询问用户的 eu-evs.com 账号邮箱和密码，并在提示中明确告知用户：
   - **凭据用途与隐私承诺**：邮箱和密码**仅用于本次登录 eu-evs.com**，不会上传到任何第三方或其他服务器，请放心提供。
   - **注册安全建议**：如尚未注册，建议在 eu-evs.com 注册时**不要使用自己的常用密码**，可使用独立的临时密码，避免主密码泄露风险。
2. 如果用户反馈尚未注册，告知用户前往 https://eu-evs.com/register 注册（再次提醒不要使用常用密码），注册完成后提供邮箱和密码
3. 拿到凭据后重新运行脚本，追加 `--email <email> --password <password>` 参数
4. 登录成功后会话会自动保存（`.eu-session.json`），后续运行无需再传凭据

> 兼容兜底：若脚本输出 `ERROR|BOT_BLOCKED_year_*` 或其他含 `BLOCKED` 字样的错误，也按 `LOGIN_REQUIRED` 同样流程处理。

### 步骤一·补充二：处理其他异常（原样上报）

脚本的所有信号（正常数据、`LOGIN_REQUIRED`、`ERROR|...`）**统一输出到 stdout**。运行脚本后，按以下优先级判断：

1. **stdout 包含 `LOGIN_REQUIRED`** → 走上方「处理 LOGIN_REQUIRED」流程，询问账密。
2. **stdout 包含 `ERROR|LOGIN_FAILED`**（凭据错误）→ 告知用户邮箱或密码不正确，重新获取凭据后用 `--email`/`--password` 重试。
3. **stdout 包含其他 `ERROR|...`**（如 `ERROR|HTTP_503_year_2026`、`ERROR|PARSE_FAILED_year_2025`、`ERROR|no_data_for_year_2025`、`ERROR|CSRF_TOKEN_NOT_FOUND` 等）→ **将 `|` 后的具体错误信息原样转述给用户**，说明当前无法获取数据及原因，不要静默吞掉，也不要自行臆造原因。例如：
   - `ERROR|HTTP_503_year_2026` → 「eu-evs.com 返回 503，服务暂时不可用，建议稍后重试」
   - `ERROR|PARSE_FAILED_year_2025` → 「2025 年数据页面结构解析失败，数据源可能已变更」
   - `ERROR|no_data_for_year_2025` → 「2025 年暂无数据」

判断顺序很重要：先确认是否为 `LOGIN_REQUIRED`，再确认是否为 `LOGIN_FAILED`，最后才是其他 `ERROR`。

脚本返回数据后，按以下规则完成展示与分析。

### 步骤二：展示 ①②③ 表格 + 生成 ④ 综合分析

#### ①②③ 表格：原样展示脚本输出

**输出必须包含范围说明：** 在展示 ①②③ 表格前后，需明确注明「以下数据仅覆盖披露日更数据的少数欧洲国家，并非 XPeng 全欧洲总销量」。该说明是必填项，不得省略，以免误导用户将数据解读为欧洲整体销量。

`--report` 模式输出的 3 个 markdown 表格（① 月度环比对比 / ② 全月总销量 / ③ 各车型销量明细）**已由脚本预计算并格式化完成，LLM 原样展示即可，不要重新计算或改写表格数据**。

脚本内部已处理：
- 环比变化量与百分比的 +/- 符号、四舍五入（保留 1 位小数）、分母为 0 标 N/A
- 当前月"月未结束"的标注
- 车型顺序按 `meta.models` 固定，0 值保留

#### ④ 综合分析：LLM 生成 4 条核心洞察

基于 ①②③ 表格的数据，输出 **4 条核心洞察**，建议覆盖以下维度：

1. **整体趋势**：当前月环比方向与幅度，是否延续上月走势
2. **主力车型**：销量最高的 1–2 个车型及其贡献率、环比表现
3. **异动车型**：环比变化最显著的车型（新投放放量、大幅增长或下滑）
4. **结构性变化**：新车型出现、产品组合迁移、市场份额相关的信号

分析必须**具体引用数字**（如「G6 当前月 535 辆，环比 +19.2%，贡献增量的 X%」），避免空泛描述。

### 步骤三：按需扩展（JSON 模式）

当用户需求超出默认 4 模块时，运行无 `--report` 版本获取 JSON，根据下表选择数据层级灵活计算：

| 需求 | 使用数据 |
|------|---------|
| 月度环比（1-D 同范围） | `monthly_partial` |
| 月度全月对比 | `monthly_full` |
| 某车型长期趋势 | `monthly_full[].sales.<车型>` 或 `monthly_partial[].sales.<车型>` |
| 同比/季度对比 | 基于 `monthly_full` 或 `monthly_partial` 灵活组合 |
| 单日异常定位 | `daily`（含每日每个车型明细） |
| 工作日 vs 周末分析 | `daily`（从 `date` 推导星期） |

## 执行约束

1. **默认入口用 `--report`，不要手动计算 ①②③**：`--report` 模式输出的 3 个表格已由脚本完成所有计算与格式化（环比变化量、百分比、车型对齐、"月未结束"标注），LLM 原样展示即可，**不要重新计算或改写表格数据**。只有步骤三的按需扩展场景才需要从 JSON 手动计算，此时优先用 `monthly_partial`/`monthly_full`，不要从 `daily` 累加。
2. **PARTIAL 才是公平对比**：最新月尚未结束，必须用「1 号到最新日」的数据与历史月同范围对比（即 `monthly_partial`），不能用全月数据（`monthly_full`）对比。
3. **日销量可为 0 或缺失**：部分日期（如周末）可能没有数据，`daily` 数组中不会出现这些日期，这是正常现象；`monthly_full`/`monthly_partial` 的 `days` 字段反映实际有数据的天数。
4. **车型可能变化**：不同年份车型列表可能不同（如 2026 年新增 M03、P7+、X9、F30），脚本已自动对齐，展示时以 `meta.models` 为准。
5. **单位为辆**：数值为注册量（辆），不是百分比或份额。
6. **百分比计算**：分母为 0 时不计算百分比，标注为 N/A。

## 异常处理

**总则**：脚本所有信号（正常数据、`LOGIN_REQUIRED`、`ERROR|...`）**统一输出到 stdout**，agent 只需检查 stdout 即可判断后续动作，无需看 stderr 或退出码。判断优先级：`LOGIN_REQUIRED` → `LOGIN_FAILED` → 瞬时网络错误 → 其他 `ERROR` → 正常数据。遇到任何失败都**只能重跑脚本或上报错误**，不得改用 curl/Python/WebFetch 等替代方式（见「全局执行铁律」）。

| stdout 信号 | 含义 | 处理方式 |
|---------|------|---------|
| `LOGIN_REQUIRED` | 数据页返回 302（未登录 / bot 拦截 / 会话失效，重定向到 `/bots`、`/login`、`/onlyNamed` 等） | **必须**使用 AskUserQuestion 询问 eu-evs.com 账号密码；未注册则引导到 https://eu-evs.com/register 注册；拿到凭据后用 `--email`/`--password` 重新运行。不得当成错误直接结束 |
| `ERROR|LOGIN_FAILED` | 邮箱或密码不正确 | 告知用户凭据错误，重新获取凭据后用 `--email`/`--password` 重试 |
| `ERROR|BOT_BLOCKED_year_*` 或其他含 `BLOCKED` | 拦截信号兼容兜底 | 同 `LOGIN_REQUIRED` 流程 |
| `ERROR|HTTP_<code>_year_<y>` | eu-evs.com 返回非预期状态码 | 将状态码和年份原样转述给用户；5xx 建议稍后重试，4xx 说明请求有问题 |
| `ERROR|PARSE_FAILED_year_<y>` | HTML 表格解析失败 | 告知用户 `<y>` 年数据页面结构解析失败，数据源可能已变更 |
| `ERROR|no_data_for_year_<y>` | 指定年份无数据 | 提示用户该年份暂无数据，建议换一年 |
| `ERROR|CSRF_TOKEN_NOT_FOUND` | 登录页结构变更，取不到 token | 告知用户数据源登录页结构可能已变更 |
| `ERROR|LOGIN_HTTP_<code>` | 登录接口异常 | 将状态码原样转述给用户 |
| `ERROR|socket hang up` / `ERROR|connect ECONNRESET...` / `ERROR|ETIMEDOUT` 等瞬时网络错误 | 脚本内部已退避重试 3 次仍未恢复（网络抖动、服务端瞬断） | **重跑同一脚本 2~3 次**（间隔 5~10 秒）；仍失败则将错误转述给用户、说明疑似网络波动并稍后再试。**不得**改用 curl/WebFetch/Python 等替代方式 |
| 其他 `ERROR|<msg>` | 未列举的异常 | **将 `|` 后的信息原样转述给用户**，不要静默吞掉，不要臆造原因 |
| 会话过期（已保存 session 失效） | 脚本会再次输出 `LOGIN_REQUIRED` | 重新走登录流程 |
| 最新月无数据（月初第一天） | 输出结果可能为空 | 提示用户数据尚未更新 |
