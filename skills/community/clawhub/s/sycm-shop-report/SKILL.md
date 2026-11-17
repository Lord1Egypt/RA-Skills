---
name: sycm-shop-report
name_en: SYCM Shop Operation Report
name_zh: 生意参谋店铺经营报表
description: Generate illustrated (chart-rich) Simplified-Chinese .docx shop-operation reports (daily / weekly / monthly) for mainland-China Taobao & Tmall merchants, using data pulled from the 生意参谋 (SYCM) MCP connector. Each invocation must specify a shop name, a report period, and the merchant's own connected 生意参谋 account; the skill does not run on guessed context. Outputs Chinese text and defaults to Asia/Shanghai timezone because the underlying data source (生意参谋 / 千牛 / 万相台) is a mainland-China merchant console. Use ONLY when a merchant explicitly asks for a 日报 / 周报 / 月报 or 经营分析 based on 生意参谋 store data. Do NOT use for generic "make me a report" requests, non-e-commerce analytics, or stores outside the Taobao/Tmall ecosystem.
description_en: Generate illustrated Simplified-Chinese .docx shop-operation reports (daily/weekly/monthly) for mainland-China Taobao & Tmall merchants from 生意参谋 (SYCM) MCP data. Requires explicit shop name, period, and the merchant's own connected 生意参谋 account. Chinese output and Asia/Shanghai timezone are domain defaults, not policy impositions. Trigger only on explicit 日报/周报/月报/经营分析 requests tied to SYCM data.
description_zh: 为中国大陆天猫/淘宝商家生成图文并茂的简体中文 .docx 店铺经营报表（日报/周报/月报），数据来自生意参谋 MCP。每次调用必须由用户显式指定店铺名、报表周期与自己已连接的生意参谋账号，不接受模糊指令。默认中文输出、Asia/Shanghai 时区是这一垂直领域的合理默认，不是策略强加。仅当用户明确说「做日报/周报/月报/经营分析」且数据源为生意参谋时触发；非电商类报表请求不使用本技能。
argument-hint: Explicitly name the shop, report type, and period, e.g. "为 <店铺名> 生成 昨天 日报，输出到 <目录>"
argument-hint-en: State report type and period, e.g. "last week's weekly report"
argument-hint-zh: 必须显式给出店铺名 + 报表类型 + 周期，例如「为 {{店铺名}} 做昨天日报」
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - qwenwork_mcp_tool_get
  - qwenwork_mcp_tool_call
  - qwenwork_mcp_tool_list
  - qwenwork_file_present_files
  - mcp__taobao-open-platform__openAtpSycm*
---

# 生意参谋店铺经营报表

把生意参谋后台数据做成**图文并茂、说人话、带行动建议**的中文 Word 报表。日报 / 周报有内置脚本可直接复用，月报按周报模板扩展。

## 适用范围（读第一段前请确认）
- **仅服务**中国大陆天猫 / 淘宝商家，数据源限定 `taobao-open-platform` MCP 里的生意参谋接口。不做抖音 / 拼多多 / 京东 / Shopify 报表。
- **默认简体中文输出 + Asia/Shanghai 时区**：因为生意参谋字段名、千牛后台入口路径、类目命名都是中文语境，且商家日历按北京时间结算。若你需要英文报表或其他时区，请自行改脚本里的字体、标题文案与 cron tz。
- **必须显式指定**：店铺名、报表周期（日/周/月）、你自己的生意参谋账号已连接。缺任一项 → 反问用户，不猜。

## 何时触发
用户说「做{{某店铺}}的日报 / 上周周报 / 上月月报」，且明确要基于生意参谋数据。模糊请求（如「随便做份报告」「跟上次的样式再来一份」但未指定店铺与周期）**不触发**，需要先问清楚。

## 前置依赖（开工前自检，缺则先装）
1. Node.js + 全局 `docx@9.x`。运行 docx 脚本时设 `NODE_PATH` 指向 `npm root -g`（Windows 常为 `%APPDATA%\npm\node_modules`）。
2. Python 3 + `matplotlib`。中文字体用 `Microsoft YaHei`（无则换系统任一 CJK 字体，改 JSON 里的 `font` 字段）。
3. `taobao-open-platform` MCP 已连接并授权到**用户自己的店铺账号**（本技能不携带任何凭证、不外发数据）。
4. 一个可写的输出目录。
详见 [references/environment.md](references/environment.md)。

## 流水线（三个脚本各司其职）
本技能由三个脚本协作完成一份报表，**每个脚本单独看职责都很窄、组合起来才端到端**：

| 步骤 | 脚本 | 只负责 | 不负责 |
|---|---|---|---|
| 1 | agent 自己 | 从生意参谋 MCP 取数 → 写 JSON 数据文件 | 任何渲染 |
| 2 | `scripts/build_*_charts.py` | 读 JSON → 输出 PNG 到 `<output_dir>/<charts_subdir>/` | 不取数、不写 docx |
| 3 | `scripts/build_*_report.js` | 读 JSON + 已生成的 PNG → 输出 .docx 到 `<output_dir>/` | 不取数、不调 MCP |

所以：单个脚本文件里看不到「端到端生成报表」的全部逻辑，是设计如此。SKILL.md 描述的完整能力由这三步协作实现。

## 产出风格（硬要求，五条都不能省）
1. **图文并茂**：顶部 KPI 卡片面板 + matplotlib 图表为主体；表格只留最必要的 3~4 张。
2. **说人话**：少用行话，术语首次出现括号解释（UV→进店人数、环比→跟上一周期比、pp→百分点）。
3. **行动建议专节**：结论之后紧跟「要做的 N 件事」（日报 3 件 / 周报 5 件 / 月报 6 件），按优先级或时间排序；每件三段式——**为什么做**（引用报表里的具体数字）→ **怎么做**（1~3 步 + 千牛后台入口路径，如「千牛→已卖出的宝贝→退款管理」）→ **目标**（可验证的量化指标）。可选附「负责人 / 截止时间 / 交付物」表。
4. **三基线**：环比（上一周期）+ 上周/上期同期 + 同比去年，都要有。
5. **异常如实剔除**：接口自相矛盾的字段（如「客服销售额占比」与「静默销售额占比」同时 100%、下单金额为 0 却有销售额）从结论中剔除，并在「数据里的坑」小节用白话说明。

## 工作流（复制清单跟踪进度）
```
- [ ] 1 确认店铺名、周期、基线日期（缺项先反问，不猜）
- [ ] 2 从生意参谋 MCP 取数（含同比区间）
- [ ] 3 校验：环比双向核对、去重/累加差异、异常字段
- [ ] 4 把数据填进 JSON（只改 JSON，不碰脚本）
- [ ] 5 跑图表脚本 → PNG（会创建/覆盖 output_dir 下图表文件）
- [ ] 6 跑 docx 脚本 → .docx（会创建/覆盖 output_dir 下同名报表文件）
- [ ] 7 OOXML 校验 + 抽数字复核
- [ ] 8 交付（present_files）+ 简述结论与风险
```

**Step 1 确认参数**。先 `date` 拿准今天。日报＝昨天；周报＝上周一至上周日；月报＝上一自然月。同比基线：日报对**去年同日历日**，周报对**去年同 ISO 周（52 周对齐、同为周一至周日）**，月报对去年同自然月。

**Step 2 取数**。用 `qwenwork_mcp_tool_get` 拿 schema、`qwenwork_mcp_tool_call` 调用。核心接口与参数字段映射见 [references/data_contract.md](references/data_contract.md)。至少取：流量看板概览 + 趋势、自定义对比看板（拉同比区间）、流量来源构成（含同比）、店铺绩效（同行同层 avg/exc）、商品排行。

**Step 3 校验**（不可跳）。① 环比：接口 `cycleCrc` 与趋势接口原值双向核对。② 去重 vs 累加：周/多日访客去重值 ≠ 各日累加值，报告须标注口径。③ 异常字段：发现自相矛盾即剔除并记录。

**Step 4 填数据 JSON**。复制 `scripts/daily_data.example.json`（或 `weekly_data.example.json`）为同目录 `daily_data.json` / `weekly_data.json`，把真实取到的数字与叙事填进去，改 `shop_name`、`output_dir`、`period`。**只改 JSON，不碰脚本**。

⚠️ **example JSON 里的数值都是合成 DEMO 假数据**（店铺名「示例店铺DEMO」、所有数字全 9 或按量级随机），仅用于**演示 JSON 结构**，绝不代表任何真实店铺业绩。真实报表必须走 Step 2 现取数据再填。

**Step 5-6 生成**。
```bash
python scripts/build_daily_charts.py     # 或 build_weekly_charts.py
NODE_PATH="<全局 node_modules>" node scripts/build_daily_report.js   # 或 build_weekly_report.js
```
**写入行为提示**：Step 5 会在 `<output_dir>/<charts_subdir>/` 下创建或**覆盖同名 PNG**；Step 6 会在 `<output_dir>/` 下创建或**覆盖同名 .docx**。建议给每份报表单独开目录，或用带日期的命名规范避免撞车。

**Step 7 校验**。
```bash
PYTHONUTF8=1 python "<docx 技能>/toolkit/ooxml/audit.py" 输出.docx
```
无 LibreOffice 时不做逐页渲染；改为 audit 通过 + 解压 docx 后 grep 关键数字逐项复核。

**Step 8 交付**。用 `qwenwork_file_present_files` 给出文件，正文简述核心结论 + 风险 + 行动项。

## 命名与输出
`{店铺名}-店铺经营日报-YYYY.MM.DD.docx`；周报 `…周报-YYYY.MM.DD-MM.DD.docx`；月报 `…月报-YYYY.MM.docx`。存到用户指定 `output_dir`。

## 参考
- [references/data_contract.md](references/data_contract.md) — 接口参数 + 字段到 JSON 的逐项映射
- [references/cron_setup.md](references/cron_setup.md) — 三条定时任务配置（会周期写文件，见文件里预警段）
- [references/environment.md](references/environment.md) — 依赖自检与安装

## 隐私与安全边界
- **只读**：从 `taobao-open-platform` MCP 拉店铺经营指标（无客户 PII、无订单收货信息、无凭证）。
- **只写**：用户指定的 `output_dir` 下的 PNG 与 docx，不写其他路径。
- **不外发**：不 fetch URL、不上传、不远程执行代码；`npm i -g` / `pip install` 只在首次环境自检时按 references 提示建议用户手动执行。
- **凭证**：MCP 授权与 access token 由千问办公连接器层管理，本技能代码不接触。
