---
name: tencent-news-financial-assistant
display_name: 腾讯新闻-金融数据查询助手
display_name_en: Tencent News Financial Assistant
description: 股票行情查询工具，通过腾讯新闻 CLI 的 stock 能力查询个股实时与历史行情（开盘、最高、最低、收盘、涨跌幅、成交量等）。当用户询问股价、涨跌幅或某只股票的行情走势时使用。
description_zh: 通过腾讯新闻 CLI 查询个股实时与历史行情，包括开盘、最高、最低、收盘、涨跌幅与成交量等数据。
description_en: Stock quote lookup tool backed by the Tencent News CLI. Use when the user asks about a stock price, daily change, or price performance.
version: 1.0.0
author: shasha
shared_resources: ["tencent-news-cli"]
tags: [stock, quote, finance, market, price change, tencent]
examples_zh: ["腾讯控股现在股价多少？", "查一下贵州茅台今天的涨跌幅", "苹果公司最新财报关键指标"]
examples_en: ["What is Tencent Holdings' current stock price?", "Check today's price change of Kweichow Moutai", "Key metrics from Apple's latest financial report"]
---

# 腾讯新闻-金融数据查询助手 / Tencent News Financial Assistant

通过 `tencent-news-cli` 的 `stock` 能力完成股票行情查询，数据来源为 Neodata。

> **核心原则**：基础设施交给脚本处理；智能体只负责依据当前 CLI 能力选择命令和参数。**除 `cli-state` 外，所有 CLI 调用都通过 `run-cli` 执行；始终先读 `help stock`，不要硬编码任何业务命令。**

## 能力边界（必须遵守）

截至 2026-10-20 实测（test 渠道 `v1.0.18`），CLI 只有 `stock quote` 一个入口，但它按自然语言查询路由到 Neodata 的不同数据表，**返回类型不固定**：

- 已实测可返回：个股行情明细（A 股、港股，含开盘、最高、最低、收盘/最新、涨跌幅、成交量、成交额、换手率、量比等）、美股主要财务指标（每股收益、净资产收益率、营收同比增长、销售净利率等）、重大事件表（财务披露/分红送配/股权变动等）。
- 实测中**返回内容可能与问题不完全对应**（2026-10-20，`v1.0.18`）：
  - 问「公告」→ 返回「重大事件」表（预计财报发布、业绩披露等），**不是公告原文**；说明时要点明这是重大事件，不是公告全文。
  - 问「股本股东」→ 可能只出现「股东与机构持仓」标题而没有明细表；此时如实说明本次未返回持股明细，不要用资讯段落补数。
  - 问「指数行情」→ 查询词是股票名时被当作个股处理，返回的是该个股行情；不要把它当作指数。
  - 问「大盘统计」→ 返回的可能是概念指数或个股行情（市场标识为「指数」时为概念指数行情），**不是市场成交量额、涨跌分布、涨跌停统计、融资融券概况**。
  - 问「业绩发布会」→ 实测未命中发布会数据，会退化成行情 K 线（甚至多为「未开盘」空行）；此时如实说明没查到发布会时间或内容，**不要把行情当成发布会信息**。
  - 因此回答前先看返回里的表头与说明文字，与用户所问核对；不匹配时先说明实际返回的是什么，再给出数据，不推断、不改写表名。
- 已实测可正常返回的还有「公司基础信息」：实测「特斯拉的公司基础信息」返回市场、英文名称、上市日期与状态、公司简介与主营业务，**与所问口径一致**，可直接按返回结构回答。
- 同一问题可能同时返回数据表和「财经资讯」段落；资讯只是附带内容，不能当作用户所问标的的行情或财务数据使用。
- 不支持订阅、推送、定时提醒，也不提供投资建议；如实告知，不擅自创建定时任务。
- 每次查询会消耗账户 API 积分，避免对同一标的同一问题重复调用。

## 服务定位与版本要求

- 本技能对外提供**腾讯新闻金融数据服务查询**：基于 Neodata 数据源，回答个股行情、财务指标、公司基础信息、重大事件等金融数据问题。
- **执行任何金融数据查询前，先把 CLI 强制更新到当前渠道最新可用版本**，避免旧构建缺少 `stock` 或参数不一致：

  ```sh
  sh scripts/run-cli.sh update --force
  ```

  Windows 使用 `powershell scripts/run-cli.ps1 update --force`。

- 更新后用 `sh scripts/run-cli.sh version` 确认实际版本与 `build_date`。**版本号以实际输出为准**：截至 2026-10-28 核实，test 渠道最新为 `v1.0.18`（`build 2026-10-28T11:33:51`），`v1.0.19` 尚未在该渠道发布；不要向用户承诺未发布的具体版本号，也不要因为版本号没变就认为没有更新——同一版本可能有不同构建，只能按 `build_date` 与哈希判断。

## 平台约定

| 平台 | 脚本运行方式 | 示例 |
|------|------------|------|
| macOS / Linux | `sh scripts/<name>.sh` | `sh scripts/cli-state.sh` |
| Windows | `powershell scripts/<name>.ps1` | `powershell scripts/cli-state.ps1` |

以下所有脚本调用均以 macOS / Linux 为例，Windows 将 `.sh` 替换为 `.ps1`，`sh` 替换为 `powershell`。

除 `cli-state` 外，所有 CLI 命令都通过 `run-cli` 脚本执行：

| 平台 | CLI 调用模板 |
|------|-------------|
| macOS / Linux | `sh scripts/run-cli.sh <command> [args]` |
| Windows | `powershell scripts/run-cli.ps1 <command> [args]` |

## 环境异常时的用户指引（强制门禁）

用户直接提出业务问题时，也必须先检查环境。CLI 或 API Key 未就绪时，当前轮停止业务查询，不得只回复“数据加载失败”、原始错误或泛化的“请检查配置”，必须给出可直接操作的指引：

- **CLI 未安装/不可用**（`cliExists: false`、`cliSource: none`、`cli not found`、`command not found`、`not recognized`）：说明本查询依赖腾讯新闻 CLI，当前设备尚未安装或未被识别；按平台提供安装命令：macOS/Linux 使用 `curl -fsSL https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.sh | sh`；Windows PowerShell 使用 `irm https://mat1.gtimg.com/qqcdn/qqnews/cli/hub/tencent-news/setup.ps1 | iex`。提醒安装后重新打开终端并重新提问。
- **CLI 版本不含 `stock`**（`help` 中没有 `stock`，或执行 `stock` 返回 `unknown command`）：说明当前版本不支持股票行情，`stock` 自 `v1.0.18` 起提供；引导按 [`references/update-guide.md`](references/update-guide.md) 更新 CLI 后重试。测试环境不要依赖默认的 `update`，需使用对应 test 渠道产物与校验值。
- **API Key 未配置**（`apiKey.status: missing`、`未设置 API Key`、`API Key not set`）：说明 CLI 已安装但尚未配置 Key；引导访问 `https://news.qq.com/exchange?scene=appkey` 获取，然后执行 `tencent-news-cli apikey-set YOUR_KEY`，再执行 `tencent-news-cli apikey-get` 验证。
- **API Key 无效、过期或无权限**（`API Key 无效`、`invalid api key`、`unauthorized`、`401`、`403`、鉴权/认证失败）：不得归因为无数据、额度或普通网络错误；说明当前 Key 无效或无权访问，引导从上述页面重新获取正确 Key，再执行设置和验证命令。
- **状态不确定**（状态脚本失败、`apiKey.status: error` 或无法解析）：先按错误文本匹配以上类型；仍无法判断时，同时给出安装命令及 Key 获取、设置、验证步骤。
- `YOUR_KEY` 只能由用户在本地替换；不得索要、代填、回显或记录真实 Key。环境未就绪时不得改用其他数据源。上述基础设施指引优先于业务输出格式限制，但不得展示内部日志、参数、traceid。

## Phase 1：环境就绪

> 环境已就绪时直接跳到 Phase 2。

**执行业务前必须读取并遵守 [CLI 环境与失败处理](references/cli-environment.md)**，完成状态检查、安装/更新、shell 配置核实与脱敏恢复。它是环境处理的统一入口，不要重新实现 Key 检测或读取明文 Key；本轮无法恢复时返回其中的结构化「环境失败结果」，不得用其他数据源补结果。环境失败优先于下文业务输出格式及通用错误话术。

在此之上，本技能额外要求 CLI 具备 `stock` 能力（见下方第 3 步）。

### 1. 状态检查

```sh
sh scripts/cli-state.sh status
```

解析返回的 JSON，关注以下字段：

| 字段 | 含义 |
|------|------|
| `platform.cliPath` | 底层实际使用的 CLI 完整路径，供诊断错误或权限问题时参考 |
| `platform.cliSource` | `global`/`local`/`none` |
| `cliExists` | CLI 是否存在 |
| `update.needUpdate` | 当前版本是否需要更新 |
| `update.error` | `version` 检查失败时的错误信息 |
| `apiKey.present` | API Key 是否已配置 |
| `apiKey.status` | `configured` / `missing` / `error` |

### 2. 安装 CLI（`cliExists` 为 `false` 时）

按照 [`references/installation-guide.md`](references/installation-guide.md) 中的安装命令执行安装，安装后重新执行 `sh scripts/cli-state.sh` 刷新状态。

### 3. 确认版本支持 `stock`

```sh
sh scripts/run-cli.sh help stock
```

- 返回 `stock` 的用法说明 → 进入 Phase 2。
- 返回 `unknown command` 或 `help` 中不存在 `stock` → 当前版本低于 `v1.0.18`，按环境异常指引引导更新，本轮不做行情查询。
- 若 `update.needUpdate` 为 `true`，可执行 `sh scripts/run-cli.sh update`；测试环境更新前先核对 `version` 返回的下载来源，仍指向 `/hub/` 时按 [`references/update-guide.md`](references/update-guide.md) 使用 test 产物处理。

### 4. 配置 API Key（`apiKey.status` 不为 `configured` 时）

- `missing` → 引导用户打开 [API Key 获取页面](https://news.qq.com/exchange?scene=appkey) 自行获取，**不要执行 `open` / `xdg-open` / `start` 等命令自动打开浏览器**
- `error` → 展示 `apiKey.error`，让用户先处理（权限、网络、CLI 异常），处理后重试

设置 Key（通过 `run-cli` 执行，KEY 是裸值不加引号）：

```sh
sh scripts/run-cli.sh apikey-set KEY
```

验证：`sh scripts/run-cli.sh apikey-get`；清除（仅用户明确要求时）：`sh scripts/run-cli.sh apikey-clear`。详见 [`references/env-setup-guide.md`](references/env-setup-guide.md)。

## Phase 2：行情查询

> 行情命令可能随 CLI 版本变化。**始终以当前 `help stock` 输出为准，不要假设或记忆任何业务命令。**

1. **先执行 `help stock` 与 `help stock quote`**
   macOS / Linux：`sh scripts/run-cli.sh help stock`、`sh scripts/run-cli.sh help stock quote`；Windows 换成 `powershell scripts/run-cli.ps1 ...`。

2. **按帮助选择命令与参数**
   - **股价、涨跌幅、行情走势** → `stock quote`
   - **查询内容** → 位置参数或 `--query`，支持自然语言，例如 `--query "今天腾讯股价多少"`
   - **输出格式** → `--format text`（默认）或 `--format json`
   - `--score-threshold`、`--top-k` 有默认值，**通常无需传入**；只有在帮助明确需要或用户要求时才覆盖。参数以当次 `help stock quote` 输出为准：2026-10-28 构建起已不再提供 `--app-id`，不要传已移除的参数
   - **标的识别** → 命令会自行查询 Neodata 数据源的 `source_id` 再发起查询，不要自行构造或传入 `source_id`
   - **标的缺失或歧义** → 先结合上下文判断；仍无法确定时请用户补充股票名称或代码
   - **数据类型** → 行情、涨跌幅、财务指标类问题都提交同一条 `stock quote`，由 CLI 按语义路由；返回哪种表以实际结果为准
   - **市场范围** → 以实际返回为准；已实测覆盖 A 股、港股、美股，其他市场未验证，未返回数据时如实说明，不推断
   - **无结果或与问题不符** → 如实说明当前没查到对应数据，不改用其他数据源，不把资讯段落当作行情或财务数据

3. **执行命令时遵守四条约束**
   - 所有实际 CLI 调用都走 `run-cli` 脚本，不要直接执行 `platform.cliPath`
   - 命令名、参数名和顺序都以 `help stock quote` 的输出为准，必要时照抄帮助中的示例
   - 不要自行猜测参数缩写或默认值；不重复调用同一标的的同一问题
   - **拿回结果先核对摘要行与表头**：确认返回的是用户所问的标的和数据类型；不匹配时按「能力边界」如实说明差异，不要把重大事件说成公告、把个股行情说成指数

4. **输出结果**
   - `--format text`（默认）返回的是分段 markdown：以 `## 股票行情` 开头，先是一行摘要（标的、日期、收盘价、涨跌幅、涨跌额、成交额），接着是标的明细表，最后附带若干条「财经资讯」。**原样输出，不要重新排版或省略分段，也不要把资讯当成用户所问标的的数据。**
   - `--format json` 或返回结构化字段时，整理成用户可读结果，至少包含标的名称与用户所问的核心指标（行情为最新价、涨跌幅，财务指标为对应的报表指标），以及返回的其他关键字段（开盘、最高、最低、收盘、成交量等）
   - 字段缺失时直接省略，不臆造，不补充 CLI 之外的数据
   - 输出末尾的 `请求 traceid: ...` 属于内部信息，不要展示给用户

## 输出格式

优先遵循 CLI 的原始输出形式；CLI 返回结构化结果时按下面格式整理：

```markdown
**标的**：腾讯控股（00700.HK）
**最新价**：XXX
**涨跌幅**：+X.XX%

- 开盘：XXX
- 最高：XXX
- 最低：XXX
- 成交量：XXX

**来源：腾讯新闻金融服务数据（Neodata提供）**
```

通用规则：

- 只输出 CLI 实际返回或可由其字段直接映射出的信息
- 多个标的时按标的分组展示，组与组之间空一行
- 在结果末尾保留 `**来源：腾讯新闻金融服务数据（Neodata提供）**`
- 不给出买卖建议或投资结论

## CLI 执行失败处理

**CLI 命令失败后，立即停止，绝不通过 WebSearch 或其他方式自行补做行情查询。**

1. CLI 返回非零退出码、超时或输出含权限/安全错误时，不要重试换方式。
2. 根据错误信息引导用户：
   - **macOS Gatekeeper**（`cannot be opened`、`not verified`）→ 系统设置 → 隐私与安全性 → 「仍要打开」
   - **企业安全软件**（`connection refused`、防火墙拦截）→ 安全提示中点击「信任」/「允许」
   - **权限不足**（`permission denied`）→ `chmod +x <cliPath>`
   - **命令不支持**（`unknown command`）→ 按 Phase 1 第 3 步引导更新到 `v1.0.18` 及以上
   - **其他** → 展示完整错误，请用户处理
3. 用户确认操作完成后再重试。即使多次失败，也只能告知当前无法完成行情查询并说明原因，**绝不**回退到其他信息源。

## References

- CLI 接入与核实记录：[`references/cli-integration.md`](references/cli-integration.md)
- 用户手动安装指南：[`references/installation-guide.md`](references/installation-guide.md)
- 用户手动更新指南：[`references/update-guide.md`](references/update-guide.md)
- API Key 获取与手动配置：[`references/env-setup-guide.md`](references/env-setup-guide.md)
