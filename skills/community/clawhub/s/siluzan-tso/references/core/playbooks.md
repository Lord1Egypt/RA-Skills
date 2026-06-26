# 工作流目录 · 分析 / 报告类（P1–P9）

> **范围**：CLI 拉数 → 脚本读盘 → Agent 撰稿 → 交付的报告/分析任务。操作/管理类见 `references/core/workflows.md`（W1–W12）。
>
> **通用纪律统一见 `references/core/agent-conventions.md`**（加载纪律、数据处理协议「摘要 → outline → 脚本读 JSON」、时间范围反问、币种分表、交付前自检），各卡片**不再重复**，只写任务特有步骤。每张卡片结构统一：`触发 / 必读 / 步骤 / 交付与确认`。

| 编号  | 业务                   | 一句话                                 |
| ----- | ---------------------- | -------------------------------------- |
| P1    | 单账户投放画像         | 单户拉数 + 诊断画像                    |
| P2    | 多账户余额扫描         | 续航不足/充值预警巡检                  |
| P3    | 多账户投放画像汇总     | accounts-digest 多户对比表             |
| P4    | Google 账户周期报告    | 默认 8 维周期汇总                      |
| P4-FB | Meta/Facebook 周期报告 | facebook-analysis 5–7 维，默认 HTML    |
| P5    | 多账户多维度批处理     | google-analysis-batch，禁外层 for-loop |
| P6    | OKKI 周报              | 固定模板多 Sheet xlsx                  |
| P7    | Google 询盘分析        | 严格 3 个月 8 Sheet xlsx               |
| P8    | 网站诊断               | website-diagnosis，默认 HTML           |
| P9    | 战略市场分析           | market-analysis，默认 HTML             |

---

## P1 · 单账户投放画像

- **触发**：对单个 Google 账户做投放画像/诊断/健康检查。
- **必读**：`analytics/account-analytics.md`；诊断报告加 `references/report-templates/google-ads-diagnosis.md` + `references/report-templates/google-account-diagnosis-report.md`。
- **步骤**：
  1. 确认统计区间（规则见 conventions §五）。
  2. `list-accounts -m Google -k <mediaCustomerId> --json-out ./snap-p1`（取 `currencyCode`）。
  3. `stats -m Google -a <mediaCustomerId> --start <S> --end <D> --json-out ./snap-p1`。
  4. `google-analysis -a <mediaCustomerId> --start <S> --end <D> --sections overview,campaigns,devices,geographic,keywords,daily-metrics --json-out ./snap-p1`（诊断须含 `daily-metrics` 按日趋势）。
  5. **outline 门禁**：对**每个** section Read 其 `<section>-<accountId>_*.outline.txt`（一批并行读全）确认字段树后再写脚本——字段名以 outline 为准，**禁止**凭模板/通用命名直接写（详见 conventions §三 outline 门禁）。
  6. 脚本读盘 → 撰写报告：每模块除表格外须有「分析 + 建议」；每日趋势金额/CPA 2 位小数。
- **交付/确认**：按 conventions §七 自检后交付。

---

## P2 · 多账户余额扫描

- **触发**：多账户余额续航不足、充值预警、僵尸账户巡检。
- **必读**：`accounts/accounts.md`（§ balance-scan）。
- **步骤**：
  1. 全量巡检：`balance-scan -m <媒体> --threshold-days 7 --json-out ./snap-p2`（可选 `--min-balance 100` / `--target-days 60`）。
  2. 已知子集：`balance-scan -m <媒体> -a id1,id2,id3 --json-out ./snap-p2-subset`（跳过翻页）。
- **交付/确认**：按 `remainingDays` 升序；`hitReason="none"` 表示未触阈值；消耗过低的僵尸账户不纳入预警。**禁止**逐账户 `balance`。

---

## P3 · 多账户投放画像汇总

- **触发**：多账户消耗/点击/转化/CTR/CPC/CPA 汇总对比表、跨账户巡检。
- **必读**：`accounts/accounts.md`（§ accounts-digest）。
- **步骤**：
  1. 确认时间范围后执行 `accounts-digest -m <媒体> -a id1,id2,... --start <S> --end <D> --json-out ./snap-p3`（全量则省略 `-a`）。
  2. 基于落盘 `data.items` 与 `meta.totals` 生成报告，**不要**再逐账户 `stats`。
- **交付/确认**：表格覆盖用户请求的**每一个** ID（未返回的占一行标注「未返回」）。

---

## P4 · Google 账户周期报告

- **触发**：Google 账户某区间的周期/月度/季度汇总报告；或用户列出 Sheet/章节要 **Excel**（非 OKKI / 询盘）。
- **必读**：`references/report-templates/google-period-report.md` + `analytics/account-analytics.md`；**要 Excel** 加 `references/report-templates/google-period-report-excel.md`（全文）。
- **步骤**：
  1. **账户核验**：`list-accounts -m Google -k <mediaCustomerId> --json-out <dir>`；无记录则停止并告知用户。
  2. 确认时间范围；区间 > 3 个月时分段（季度/月）。
  3. **拉数**：用户已指定 Sheet/维度 → 只拉对应 `--sections`（见 `google-period-report-excel.md` 映射表）；未指定 → 按 `google-period-report.md` 默认 8 维，并可并行追问可选追加。
  4. **门禁**：对每个 section Read `<section>-<accountId>_*.outline.txt` 后再写脚本。
  5. 脚本读盘写产物：默认 **HTML**（`report-template*.html` 版式参考）；用户要 **Excel** → Agent 脚本写 xlsx（**禁止**宿主第三方 xlsx Skill；**无** CLI excel 子命令）。
  6. 默认 HTML 报告须含：账户概览、投放趋势、Top 关键词/系列/地区分布、优化建议；用户定制 Excel 以用户 Sheet 清单为准。
- **交付/确认**：按 conventions §七 自检；`accountId` 须与用户给的 `mediaCustomerId` 一致。

> 用户用「OKKI 周报」固定话术 → 改走 **P6**，不按默认 8 维追问。

---

## P4-FB · Meta/Facebook 账户周期报告

- **触发**：Meta/Facebook 账户周期/月报/周报或诊断报告。
- **必读**：`references/report-templates/meta-period-report.md` + `assets/meta-period-report-rules.md`（内容丰富度必读）+ `analytics/facebook-analysis-guide.md`；要 Excel 加 `references/report-templates/meta-period-report-excel.md`。
- **默认交付**：**HTML**（`facebook-analysis render`）；用户明确要 Excel 时 Agent 脚本写 xlsx（步骤 1–3 不变，不调 `render`）。
- **步骤**：
  1. `list-accounts -m MetaAd -k <mediaCustomerId> --json-out ./snap-fb` 确认账户与 `currencyCode`。
  2. 确认 `--start` / `--end`（>3 个月可分段）。
  3. **拉数**（默认 5 维，要创意加 `creative`）：`facebook-analysis -a <id> --start <S> --end <D> --json-out ./snap-fb --sections overview,ad-sets,platform,country,audience`。
  4. **分析**：脚本读落盘 JSON 聚合（见 `facebook-analysis-guide.md`）。
  5. **写 JSON**：按 `meta-period-report-rules.md` 落盘 `meta-period-report.json`（`narrative` 4 条建议各 ≥150 字 + `supplementaryRecommendations` 7 维 + HTML 必填扩展）；无按日/关键词等写「接口未提供」，**禁止编造**。
  6. **交付**：`facebook-analysis render --data ./meta-period-report.json --snapshot-dir ./snap-fb --out ./meta-period-report.html`。
- **交付/确认**：按 conventions §七 自检。诊断场景改用 `references/report-templates/meta-account-diagnosis-report.md`，拉数省略 `--sections` 拉全 7 维。

---

## P5 · 多账户多维度批处理

- **触发**：账户数 ≥ 2 且需拉取 ≥ 2 个 google-analysis 维度。**禁止**外层 for-loop。
- **必读**：`analytics/google-analysis-batch.md` + `analytics/account-analytics.md`；可选 `core/subagent-orchestration.md`。
- **入口选择**：全量 → 省略 `-a`；2~10 子集 → `google-analysis -a id1,id2,...`；≥10 子集或需 resume → `google-analysis-batch run -a id1,id2,...`。
- **步骤**：
  1. （可选）Read `subagent-orchestration.md` § P5 决定执行模式。
  2. 确认时间范围 + 维度（默认 `campaigns,geographic,keywords`）。
  3. 执行（推荐全量省略 `-a`）：
     ```bash
     siluzan-tso google-analysis-batch run --start <S> --end <D> \
       --sections campaigns,geographic,keywords \
       --account-concurrency 4 --section-concurrency 6 \
       --min-spend 1 --keyword-limit 1000 --json-out ./snap-p5
     ```
  4. **中断只能 resume**：`google-analysis-batch resume --json-out ./snap-p5 --run-id <runId>`；只读进度用 `status`。
  5. **outline 门禁（消费产物前）**：每个维度 Read 其一份 `results/<accountId>/<section>-<accountId>.outline.txt`（同维度多账户同结构，读其一即可代表该维度；一批并行把所有维度 outline 读全）确认字段树后再写聚合脚本，**禁止**凭模板字段名直接写（详见 conventions §三 outline 门禁 + `analytics/google-analysis-batch.md` §产物消费）。
- **交付/确认**：**禁止**重新 `run` 续跑；401 → 整批终止，重登录后 `resume`。

---

## P6 · OKKI 周报

- **触发**：话术含 `使用 okki 周报模板` / `OKKI 周报` / `okki 周报`，且指向 Google 账户 + 日期区间。
- **必读**：`references/report-templates/okki-weekly-google-client.md`（**全文**）+ `analytics/account-analytics.md`；可选 `core/subagent-orchestration.md`。
- **步骤**：
  1. （可选）Read `subagent-orchestration.md` § P6 决定是否分阶段委派。
  2. 确认 `mediaCustomerId` 与 `--start` / `--end`。
  3. 同一 `--json-out` 目录执行模板命令组合：`stats`、`balance`、`google-analysis --sections overview,campaigns,keywords,search-terms,campaign-device,campaign-geo-matched`。
  4. 脚本读盘 → 交付话术 + 多 Sheet `.xlsx`（无 CLI 写表命令）。
- **交付/确认**：**不**按 P4 默认 8 维追加；金额读 `*Yuan` 字段。

---

## P7 · Google 账户询盘分析

- **触发**：话术含 `Google 账户询盘分析` / `分析 XXX Google 账号的询盘效果`，或同时含「询盘 + 账户 + Google」。
- **必读**：`references/report-templates/google-inquiry-analysis.md`（**全文**）+ `analytics/account-analytics.md` + `analytics/geo-continents.json`；可选 `core/subagent-orchestration.md`。
- **时间窗口强约束**：**严格 3 个月** = 分析月份 + 向前 2 个完整自然月，**禁止**扩展到 7 个月。
- **步骤**：
  1. （可选）Read `subagent-orchestration.md` § P7。
  2. 询盘资料入场：用户附文件 → 解析落盘 `./snap-inquiry/inquiries.json`；仅给账户 ID → 反问账户 + 分析月份并贴字段清单，**禁止编造询盘数据**。
  3. CLI 拉数（同一目录）：`list-accounts`、`google-analysis --sections campaigns,keywords,search-terms,campaign-geo`，并按月拉 `m1/m2/m3` 的 `campaigns,geographic`。
  4. 脚本聚合计算 8 Sheet 数据；国家→大洲映射读 `geo-continents.json`，**禁止**硬编码国家名。
- **交付/确认**：必产 8 Sheet xlsx（版式见模板），**只能**由 Agent 脚本生成，**禁止**假设 `… excel` 子命令存在。

---

## P8 · 网站诊断

- **触发**：对某 URL 做网站/落地页诊断、投放前网站评分，或话术含「网站诊断」「落地页质量」（**非** Google 账户 `AdvertisingDiagnosis`）。
- **必读**：`analytics/website-diagnosis-guide.md` + `assets/website-diagnosis-rules.md` + `references/report-templates/website-diagnosis-report.md`。
- **默认交付**：**HTML**（`website-diagnosis render`）；**禁止**仅 Markdown 摘要或纯 JSON 充当终稿。
- **步骤**：
  1. 确认完整 URL（`https://` 可省略，CLI 自动补全）。
  2. 采集：`website-diagnosis collect --url <url> --json-out ./snap-web`。
  3. 按 `website-diagnosis-rules.md` 脚本落盘 `diagnosis.json`（与 tso_agent `getWebsiteDiagnosisData` 同结构：6 模块、29 子项、`ratingId`、`coreIssuesIds`）。
  4. 出 HTML：`website-diagnosis render --data ./diagnosis.json --collect ./snap-web/<collect>.json --out ./snap-web/website-diagnosis-report.html`。
- **交付/确认**：交付 HTML 路径；Lighthouse 缺失时在 HTML 中说明；仅需历史 ARIT 分时用 `website-diagnosis search --ids <websiteDiagnoseId>`。

---

## P9 · 战略市场分析

- **触发**：话术含「市场分析」「行业分析」「战略市场报告」「KA 市场报告」，或对某客户/行业做竞品/GTM 战略分析（**非** `google-analysis`、**非** 网站诊断）。
- **必读**：`analytics/market-analysis-guide.md` + `assets/market-analysis-rules.md`（原始业务维度清单）+ `references/report-templates/market-analysis-report.md`。
- **默认交付**：**HTML**（`market-analysis render`）。
- **步骤**：
  1. 确认客户信息（客户名称/网站/行业/核心产品至少一项）；`targetMarket` 默认「全球」、`timeRange` 默认「近12个月」（未给须写明）。
  2. 采集：`market-analysis collect --customer-name "<name>" --website <url> --industry "<industry>" --core-products "<products>" --target-market "<market>" --time-range "<range>" --json-out ./snap-market`。
  3. 按 `market-analysis-rules.md` 维度表**逐章 WebSearch** 撰写，脚本落盘 `./snap-market/market-report.json`。
  4. 渲染：`market-analysis render --data ./snap-market/market-report.json --out ./snap-market/market-analysis-report.html`；报缺项时**只补缺失维度**后重写 JSON。
- **交付/确认**：交付 HTML 路径并说明需联网加载 CDN。
