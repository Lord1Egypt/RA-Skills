# 工作流目录 · 分析 / 报告类（P1–P10）

> **范围**：CLI 拉数 → 脚本读盘 → Agent 撰稿 → 交付的报告/分析任务。操作/管理类见 `references/core/workflows.md`（W1–W12）。
> **通用纪律见 `references/core/agent-conventions.md`**（读盘、时间范围、币种、交付自检）；各卡片只写本任务步骤。卡片字段：`触发 / 必读 / 步骤 / 产物`。完整参数表见「必读」指向的命令文档。
> **用户模糊话术**（只说「报告/诊断/分析/检测/监测」、对象不清）：**必须先 Read `references/core/intent-routing.md`**，再读本节对应 P 卡片。
> **终稿语言**：按 conventions §14.6 判定 `zh` 或 `en`，写入 `meta.lang`，下面每条渲染 / 交付命令都带 `--lang <zh|en>`。

| 编号  | 业务                   | 一句话                                 |
| ----- | ---------------------- | -------------------------------------- |
| P1    | 单账户投放画像         | 单户拉数 + 诊断画像                    |
| P2    | 多账户余额扫描         | 续航不足/充值预警巡检                  |
| P3    | 多账户投放画像汇总     | accounts-digest 多户对比表             |
| P4    | Google 账户周期报告    | 默认 10 章周期汇总（含受众、否词）     |
| P4-FB | Meta/Facebook 周期报告 | facebook-analysis 默认 5 维，默认 HTML |
| P5    | 多账户多维度批处理     | google-analysis-batch，禁外层 for-loop |
| P6    | OKKI 周报              | 写 JSON → okki-render 出 5 Sheet xlsx  |
| P7    | Google 询盘分析        | 严格 3 个月 8 Sheet xlsx               |
| P8    | 网站诊断               | website-diagnosis，默认 HTML           |
| P9    | 战略市场分析           | market-analysis，默认 HTML             |
| P10   | Google 季度经营报告    | 复盘 + 下期规划 HTML（大族版式）       |

---

## P1 · 单账户投放画像

- **触发**：对单个 Google 账户做投放画像/诊断/健康检查。
- **必读**：`references/analytics/account-analytics.md`；诊断报告加 `report-templates/google-ads-diagnosis.md` + `report-templates/google-account-diagnosis-report.md`。
- **步骤**：
  1. 确认统计区间（规则见 conventions §五）。
  2. `list-accounts -m Google -k <mediaCustomerId> --json-out ./snap-p1`（取 `currencyCode`）。
  3. `stats -m Google -a <mediaCustomerId> --start <S> --end <D> --json-out ./snap-p1`。
  4. `google-ads-diagnosis collect -a <mediaCustomerId> --start <S> --end <D> --json-out ./snap-p1`（含对比周期 campaigns/geographic/keywords + `daily-metrics` 按日趋势；产出 `google-ads-diagnosis-collect.json`，**仅事实**）。部分维度失败（exit 2）时 collect 仍产出 JSON，**禁止**用 `--skip-fetch` 或脚本绕过 CLI 重映射快照。
  5. **outline 门禁**（若手写脚本读盘）：对**每个** section Read 其 `<section>-<accountId>_*.outline.txt` 确认字段树——字段名以 outline 为准。
  6. **Agent 撰写**：读 `google-ads-diagnosis-collect.json`（`reportData` + `agentBrief`）+ `google-ads-diagnosis.md`，填写全部 `analysis` / `suggestions` / `diagnosisOverview` / `summary` 等，保存 `google-ads-diagnosis.json`。
  7. **渲染终稿**：`google-ads-diagnosis render --data ./snap-p1/google-ads-diagnosis.json --out ./snap-p1/google-ads-diagnosis-report.html --lang <zh|en>`（模板与 MarkAI `GoogleAdsDiagnosisReport.html` 一致）。
- **产物**：HTML（`google-ads-diagnosis-report.html` 路径）；按 conventions §七 自检。

---

## P2 · 多账户余额扫描

- **触发**：多账户余额续航不足、充值预警、僵尸账户巡检。
- **必读**：`references/accounts/accounts-balance-stats.md`（§ balance-scan）。
- **反模式**：`meta.dataIssue` 非空或 exit 2 → 向用户说明数据异常（余额全 null / OAuth 失效），**禁止**当成「无预警命中」。
- **步骤**：
  1. 全量巡检：`balance-scan -m <媒体> --threshold-days 7 --json-out ./snap-p2 --lang <zh|en>`（可选 `--min-balance 100` / `--target-days 60`）。
  2. 已知子集：`balance-scan -m <媒体> -a id1,id2,id3 --json-out ./snap-p2-subset --lang <zh|en>`（跳过翻页）。
- **产物**：`data.items` 为全部已检查账户（按 `remainingDays` 升序）；预警筛 `hitReason !== "none"`；`hitReason="none"` 表示未触阈值；消耗过低的僵尸账户 `remainingDays` 为 null、不纳入预警。向用户贴 Markdown 表时单元格必须把 `|` 换成 `｜`（公司名常含 `|`）。**禁止**逐账户 `balance`。

---

## P3 · 多账户投放画像汇总

- **触发**：多账户消耗/点击/转化/CTR/CPC/CPA 汇总对比表、跨账户巡检；**转化成本监控 / 零转化 / 口语「零询盘」（无 CRM）**（见 `intent-routing.md` **§零·D**）。
- **必读**：`references/accounts/accounts-balance-stats.md`（§ accounts-digest）。
- **反模式**：
  - **有 CRM 询盘附件/字段表** → 改 **P7**，不要用本卡片。
  - **禁止**猜 `--period` / `--date-start`；只用 `--start`/`--end`（或 `--start-date`/`--end-date`）。
  - **禁止**发明 `cpa-risk-scan` / `cpa-scan`（拦截会提示改用本命令）。
  - `conversions`/`cpa` 为 null 时写「转化未返回」，**禁止**对 null 做 `>` 比较导致脚本崩溃。
  - **禁止**把 `meta.totals` 写成「全部账户」合计（`totalsScope=returned`，只合计命中行）。
  - **禁止**把 `ctr` 再 `.2%` / `*100`（已是百分数）。
  - **Google 四项巡检**（CPA、余额、零转化、无 Display/PMax，常带 MCC）：只跑下面这一条，**禁止**再逐户 `ad campaigns` / `google-analysis --sections campaign-types`，**禁止**把 `siluzan-tso` 写进脚本再 subprocess。
  - **D 组 / 「启用系列里有没有 PMax」/ 「启用但 7 天 0 展示」**：改用 `--with-enabled-campaigns`（步骤 1c）。提示词若写「先 list-accounts、digest --skip-balance、balance-scan -a 全部 ID、再逐户 ad campaigns」，**不要照做**。
- **步骤**：
  1. 确认时间范围后执行 `accounts-digest -m <媒体> -a id1,id2,... --start <S> --end <D> --json-out ./snap-p3 --lang <zh|en>`（全量则省略 `-a`）。指定 MCC 时加 `--login-customer-id <id>`，不要先 `list-accounts` 再把全部 ID 拼进 `-a`。
  1b. **要系列类型时**（仅 Google，含暂停的系列也算）：同一条命令加 `--with-campaign-types`。四项都要时**不要**再加 `--max-cpa` / `--zero-conversions`（那两个开关会丢掉其它行）。脚本读 `data.items`：`cpa`、`balance`、`spend`+`conversions`，以及 `hasDisplay` / `hasPmax`。只有 `campaignTypesStatus=ok` 且两项都为 false 才写入「无展示且无 PMax」；`error` / `skipped-no-spend` 另列。
  1c. **要启用中的 PMax，或启用但区间展示为 0 的系列**（D 组）：同一条命令加 `--with-enabled-campaigns`，**不要**加 `--skip-balance`，**不要**再跑 `balance-scan`（行上已有 `dailySpend`、`remainingDays`）。**不要**同时加 `--with-campaign-types`。脚本读 `hasEnabledPmax === false` 且 `enabledCampaignStatus=ok` 才算「启用系列里没有 PMax」；`zeroImpressionEnabled` 已排除 PMax 与 Display。`error` / `skipped-no-spend` 另列，禁止当成「无 PMax」。
  2. **高 CPA / 转化成本巡检**：`--max-cpa <n> --skip-balance`（CPA > n，或零转化且消耗已 > n）。读盘后**只把 `agentBrief.userDelivery` 原样发给用户**（无命中即「全部正常」句；有命中只贴表）。
  3. **零转化 / 零询盘巡检**（要全部空耗户，含小额）：加 `--zero-conversions`。
  4. 指定子集对比表：基于 `data.items`；**不要**再逐账户 `stats`。
- **产物**：巡检任务交付 `agentBrief.userDelivery`（或用户给的固定「全部正常」句）；对比表覆盖用户请求的**每一个** ID（未返回的占一行标注「未返回」）。Markdown 单元格须把 `|` 换成 `｜`。没有系列/关键词数据时**禁止**写暂停关键词、改落地页。**禁止**只落盘不说话。

---

## P4 · Google 账户周期报告

- **触发**：Google 账户某区间的周期**数据汇总**（只要花费/转化/10 章，或用户列出 Sheet 要 **Excel**）。非 OKKI / 询盘 / **非**客户版经营报告。
- **不是 P10**：出现「月度报告 / 月总结与规划 / 季度报告 / Q3 汇总 / Q4 规划 / 季度汇报 / 投放季报 / 客户版 / 大族模板 / 下月规划 / 效率+区域询盘+国家明细」→ **P10**（即使带「行业参考」也不改 P9）。
- **必读**：`report-templates/google-period-report.md` + `references/analytics/account-analytics.md`；**要 Excel** 加 `report-templates/google-period-report-excel.md`（全文）。
- **步骤**：
  1. **账户核验**：`list-accounts -m Google -k <mediaCustomerId> --json-out <dir>`；无记录则停止并告知用户。
  2. 确认时间范围；区间 > 3 个月时分段（季度/月）。
  3. **拉数**：用户已指定 Sheet/维度 → 只拉对应 `--sections`（见 `google-period-report-excel.md` 映射表）；未指定 → 按 `google-period-report.md` 默认 9 个拉数维（含 `audience`、`negative-keywords`），并可并行追问可选追加。终稿要「转化价值 / 单转化价值 / ROAS」的上期时，再按 excel 规格拉等长上期 `--sections campaigns` 后汇总，禁止把这三格留成「—」。关键词 / 搜索字词表用各自行的 `conversionsValue`（ROAS = 该值 / `spend`），不要用系列汇总值摊下去。
  4. **门禁**：对每个 section Read `<section>-<accountId>_*.outline.txt` 后再写脚本。
  5. 脚本读盘写 `google-period-report.json`（`meta` + `narrative`，`meta.lang` 跟本轮语言）；用户要 **Excel** → Agent 脚本写 xlsx（**禁止**宿主第三方 xlsx Skill；**无** CLI excel 子命令；表头跟 `meta.lang`）。
  6. 默认 HTML：`google-analysis render --data ./google-period-report.json --snapshot-dir ./snap-google --out ./google-period-report.html --lang <zh|en>`。须含账户概览、投放趋势、Top 关键词/系列/地区/受众分布、当前否词名单、优化建议。
- **产物**：按 conventions §七 自检；`accountId` 须与用户给的 `mediaCustomerId` 一致。HTML 封面按区间写成「季度」或「月度」，对不上则仍是「周期」。不要打开 HTML 改称呼。

> 用户用「OKKI 周报」固定话术 → 改走 **P6**，不按默认 10 章追问。
> 只要账户级按日 Excel（无多维章节）→ **P4-DAILY**。
> 用户要的是 **Demand Gen / 需求开发** 投放数据分析或汇总报告 → **P4-DG**，不要用本卡的 9 个拉数维。

---

## P4-DG · Demand Gen 投放数据分析汇总报告

- **触发**：Demand Gen / 需求开发 / 需求生成的投放数据分析、汇总报告、客户与运营共用版。只要 Excel 也走本卡。
- **不是**：创建或修改 Demand Gen（**W3**，`ad demand-gen` 写入）；也不是 Google 全账户周期报告（**P4**）。
- **必读**：`report-templates/demand-gen-analysis-report.md`。要 Excel 再读 `report-templates/demand-gen-analysis-report-excel.md`。
- **步骤**：
  1. `list-accounts -m Google -k <mediaCustomerId> --json-out ./snap-dg`。
  2. `google-analysis -a <id> --start … --end … --sections overview,campaigns,daily-metrics,devices,geographic,audience --json-out ./snap-dg`。系列只留 `channelTypeV2 = DEMAND_GEN`。
  3. `ad demand-gen list -a <id> --json-out ./snap-dg`，再对每个系列 `ad demand-gen report -a <id> --campaign-id <id> --start-date … --end-date … --json-out ./snap-dg`。
  4. 脚本读盘写 `demand-gen-analysis-report.json`。有效线索、商机、成交、业务 ROAS 用户没给就写 `未提供`。禁止抄模板演示数。
  5. 默认 HTML：`google-analysis demand-gen-render --data ./demand-gen-analysis-report.json --out ./demand-gen-analysis-report.html --lang <zh|en>`。
  6. 用户要 Excel：按 excel 纲要写 9 张表。**不要**用 `demand-gen-render` 代替 xlsx。
- **产物**：8 节 HTML，或 9 Sheet xlsx。`accountId` 与用户给的 ID 一致。

---

## P4-DAILY · 按日投放 Excel

- **触发**：按天导出 / 投放数据做成 Excel（非 Google/Meta 多维报告）。
- **必读**：`report-templates/stats-daily-excel.md`。
- **步骤**：核验账户 → `stats … --by-day --json-out` → 脚本写 xlsx。

---

## P4-FB · Meta/Facebook 账户周期报告

- **触发**：Meta/Facebook 账户周期/月报/周报或诊断报告。
- **必读**：`report-templates/meta-period-report.md` + `assets/meta-period-report-rules.md` + `references/analytics/facebook-analysis-guide.md`；要 Excel 加 `report-templates/meta-period-report-excel.md`。
- **默认产物**：**HTML**（`facebook-analysis render`）；用户要表格 / Excel 时 `render --format xlsx`。
- **步骤**：
  1. `list-accounts -m MetaAd -k <mediaCustomerId> --json-out ./snap-fb` 确认账户与 `currencyCode`。
  2. 确认 `--start` / `--end`（>3 个月可分段）。
  3. **拉数**（默认 5 维）：`facebook-analysis -a <id> --start <S> --end <D> --json-out ./snap-fb --sections overview,daily,country,campaigns,audience`。
  4. **分析**：脚本读落盘 JSON 聚合（见 `facebook-analysis-guide.md`）。
  5. **写 JSON**：按 `meta-period-report-rules.md` 落盘 `meta-period-report.json`（四问 + 3 张建议卡 + 各章 analysis/advice）；**禁止编造**数字。
  6. **交付**：`facebook-analysis render --data ./meta-period-report.json --snapshot-dir ./snap-fb --out ./meta-period-report.html --lang <zh|en>`；要表格加 `--format xlsx`。
- **产物**：按 conventions §七 自检。诊断场景改用 `report-templates/meta-account-diagnosis-report.md`，拉数省略 `--sections` 拉全量。

---

## P5 · 多账户多维度批处理

- **触发**：账户数 ≥ 2 且需拉取 ≥ 2 个 google-analysis 维度。**禁止**外层 for-loop。
- **必读**：`references/analytics/google-analysis-batch.md` + `references/analytics/account-analytics.md`；可选 `references/core/subagent-orchestration.md`。
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
  5. **outline 门禁（消费产物前）**：每个维度 Read 其一份 `results/<accountId>/<section>-<accountId>.outline.txt`（同维度多账户同结构，读其一即可代表该维度；一批并行把所有维度 outline 读全）确认字段树后再写聚合脚本，**禁止**凭模板字段名直接写（详见 conventions §三 outline 门禁 + `references/analytics/google-analysis-batch.md` §产物消费）。
- **产物**：**禁止**重新 `run` 续跑；401 → 整批终止，重登录后 `resume`。

---

## P6 · OKKI 周报

- **触发**：话术含 `使用 okki 周报模板` / `OKKI 周报` / `okki 周报`，且指向 Google 账户 + 日期区间。
- **必读**：`report-templates/okki-weekly-google-client.md`（**全文**）+ `references/analytics/account-analytics.md`；可选 `references/core/subagent-orchestration.md`。
- **步骤**：
  1. （可选）Read `subagent-orchestration.md` § P6 决定是否分阶段委派。
  2. `list-accounts -m Google -k <用户给的账户号>`（`928-780-1878` 可原样，CLI 去连字符）确认 `mediaCustomerId`；无 `-k` 的默认首页或 `itemCount < total` **禁止**判定未绑定。确认 `--start` / `--end`。
  3. 同一 `--json-out` 目录执行模板命令组合：`stats`、`balance`、`google-analysis --sections overview,campaigns,keywords,search-terms,campaign-device,geo-targeted`。
  4. 脚本读盘 → 只写 `okki-weekly-report.json` 的 `meta` + `narrative`（5 Sheet 表末分析 + 账户 Sheet 固定 5 维数据复盘；表为空也须写）。`deviceType` 是 `Desktop`/`Mobile`，禁止 `.get("DESKTOP")`，按大小写不敏感分类累加后再写设备金额。
  5. `google-analysis okki-render --data ./okki-weekly-report.json --snapshot-dir ./snap-okki --out <xlsx> --lang <zh|en>`。缺分析 / 缺 5 维复盘 / 缺 `campaign-device` 或 `geo-targeted` 会拒绝出文件；按 stderr 补 JSON 后重跑。**禁止** Agent 手写 xlsx。
  6. **话术收口**（用户本轮没换格式时，行首一个字都不能改）：先写一行 xlsx 路径，再贴一个代码块。块内从「您好，同步一下谷歌」起，依次是 `1、消耗：`、`2、展示点击：`、`3、点击率：`、`4、平均点击单价：`、`5、转化：`、`5.1`、`5.2`、`6、优化建议：` 与 ①②③ 各一行、`7、账户余额：`。只填当次数字。禁止合成一段，禁止改成「一、二、三、四」或「结论先行」。代码块外不要再写概览。用户**本轮**粘贴了新全文或点名改某一条，就按用户的来，只动被点名的行，仍然只发这一个代码块。填数规则见 `okki-weekly-google-client.md`。
- **产物**：`okki-render` 写出的 `.xlsx` 路径（缺文件 = 未完成）+ 上面这个代码块；**不**按 P4 默认 10 章追加。仅用户明确「只要话术 / 不要文件」时才省略 xlsx。

---

## P7 · Google 账户询盘分析

- **触发**：话术含 `Google 账户询盘分析` / `分析 XXX Google 账号的询盘效果`，或同时含「询盘 + 账户 + Google」。
- **必读**：`report-templates/google-inquiry-analysis.md`（**全文**）+ `references/analytics/account-analytics.md` + `references/analytics/geo-continents.json`；可选 `references/core/subagent-orchestration.md`。
- **时间窗口强约束**：**严格 3 个月** = 分析月份 + 向前 2 个完整自然月，**禁止**扩展到 7 个月。
- **步骤**：
  1. （可选）Read `subagent-orchestration.md` § P7。
  2. 询盘资料入场：用户附文件 → 先看一眼表头再落盘 `./snap-inquiry/inquiries.json`（列名接近即可）；仅给账户 ID → 反问账户 + 分析月份并贴字段清单，**禁止编造询盘数据**。
  3. CLI 拉数（同一目录）：`list-accounts`、`google-analysis --sections campaigns,keywords,search-terms,campaign-geo`，并按月拉 `m1/m2/m3` 的 `campaigns,geographic`。
  4. 脚本聚合计算 8 Sheet 数据；国家→大洲映射读 `geo-continents.json`，**禁止**硬编码国家名。
- **产物**：必产 8 Sheet xlsx（版式见模板），**只能**由 Agent 脚本生成，**禁止**假设 `… excel` 子命令存在。

---

## P8 · 网站诊断

- **触发**：对某 URL 做网站/落地页诊断、投放前网站评分；话术含「网站诊断/检测/监测/质量**报告**」「落地页报告」「官网体检」「**是否符合（Google）广告投放要求**」「**能不能投 / 适不适合投广告**」（**非** Google 账户诊断、**非** 行业报告、**非** 生成搜索广告方案）。同义词见 `intent-routing.md` §零 / §二 P8。
- **典型误路由**：用户说「诊断网站 https://… 是否符合 Google 广告投放要求」→ **仍是 P8**；须 `website-diagnosis collect --url …`，**禁止**因带「Google 广告」改走 W3，**禁止**只用 WebFetch/浏览器肉眼看页写结论。
- **必读**：`references/analytics/website-diagnosis-guide.md` + `assets/website-diagnosis-rules.md` + `report-templates/website-diagnosis-report.md`。
- **默认产物**：**HTML**（`website-diagnosis render`）；**禁止**仅 Markdown 摘要或纯 JSON 充当终稿。
- **步骤**：
  1. 确认完整 URL（`https://` 可省略，CLI 自动补全）。
  2. 采集：`website-diagnosis collect --url <url> --json-out ./snap-web`（落盘含 `signals` / `dataAvailability`；`--include-html` 仅增大落盘，不改 signals）。
  3. 脚手架：`website-diagnosis prepare --collect ./snap-web/<collect>.json`（Lighthouse 失败时 m2i1/m5i1 预填 Absent）。
  4. 按 `signals` + `website-diagnosis-rules.md` 补全 `needsAgent=true` 项，并写 `priorityPlan`（只根据本站未满分项，禁止套用固定行动清单）→ 落盘 `diagnosis.json`。
  5. 出 HTML：`website-diagnosis render --data ./diagnosis.json --collect ./snap-web/<collect>.json --out ./snap-web/website-diagnosis-report.html --lang <zh|en>`。
- **产物**：交付 HTML 路径；Lighthouse 缺失时性能项标「未测到」、禁止编造分；仅需历史 ARIT 分时用 `website-diagnosis search --ids <websiteDiagnoseId>`。

---

## P9 · 战略市场分析

- **触发**：话术含「市场分析」「**行业分析**」「**行业分析报告**」「生成/写一份 **XX 行业** 报告」（如「电商行业」「制造业」）、「战略市场报告」「KA 市场报告」，或对某客户/行业做竞品/GTM 战略分析（**非** `google-analysis`、**非** 网站诊断、**非** 账户周期 P4）。
- **典型误路由**：用户只说「帮我生成一份电商行业的行业分析报告」→ **仍是 P9**；须 `market-analysis collect --industry "电商" --json-out …`，**禁止**跳过 CLI 直接 WebSearch 写 Markdown。
- **必读**：`references/analytics/market-analysis-guide.md` + `assets/market-analysis-rules.md`（原始业务维度清单）+ `report-templates/market-analysis-report.md`。
- **默认产物**：**HTML**（`market-analysis render`）。
- **步骤**：
  1. 确认客户信息（客户名称/网站/行业/核心产品至少一项）；`targetMarket` 默认「全球」、`timeRange` 默认「近12个月」（未给须写明）。
  2. 采集：`market-analysis collect --customer-name "<name>" --website <url> --industry "<industry>" --core-products "<products>" --target-market "<market>" --time-range "<range>" --json-out ./snap-market`。**仅给行业时**可简化为 `--industry "电商" --json-out ./snap-market`（四选一至少一项即可）。
  3. 按 `market-analysis-rules.md` 维度表**逐章 WebSearch** 撰写，脚本落盘 `./snap-market/market-report.json`。
  4. 渲染：`market-analysis render --data ./snap-market/market-report.json --out ./snap-market/market-analysis-report.html --lang <zh|en>`；报缺项时**只补缺失维度**后重写 JSON。
- **产物**：交付 HTML 路径并说明需联网加载 CDN。

---

## P10 · Google 季度经营报告

- **触发**（命中越多越稳）：Google/谷歌广告 **月度报告**、**月总结与规划**、**季度报告**、**Q3 汇总**、**Q4 规划**、**季度汇报**、**投放季报**、客户版/对外、大族模板、下月规划；或要「效率 + 区域询盘 + 国家明细 + 规划」；或「结论→效率→结构→新探索→总结→Q4」。**不是** P1 诊断、**不是** P4「只要花费转化」的周期表。用户提「行业参考」仍走 P10，**禁止编造行业数**（本批无行业章）。
- **必读**：`report-templates/google-quarterly-report.md`；写 `narrative.plan` 前再 Read `report-templates/google-quarterly-plan.md`。
- **默认产物**：**HTML**（`google-quarterly render`）。
- **步骤**：
  1. 确认账户与区间：季度话术省略日期 → 上一完整自然季；**月度报告 / 下月规划** → 上一完整自然月（或用户指定月）作 `--start/--end`。
  2. **询盘未入场则先问再停**（话术见 `google-quarterly-report.md`「询盘入场」）。没有表格且用户未说「没有」时，**禁止** collect / 写 narrative / render。用户发来表 → 抽行落盘 `./snap-p10/inquiries.json` 再 `--inquiries`（**禁止**把 xlsx 原文件传给 collect）；用户说没有 → 询盘位留空（可选 `--inquiry-conversion`，须用户点名），**禁止编造**。
  3. `list-accounts -m Google -k <mediaCustomerId> --json-out ./snap-p10`（取户名、币种）。可与等询盘回复并行，但 collect 必须等询盘问完。
  4. `google-quarterly collect -a <id> --start <S> --end <D> --json-out ./snap-p10 --account-name "<名>"`（可选 `--keyword-seeds`）。新探索四类并行（视频 / PMax / 发现 / 展示）；视频用 Ads 视频报表，不拉频道订阅总数 / 来源饼 / 视频类型。
  5. 读 `google-quarterly-collect.json`，只写 `narrative` 到 `google-quarterly.json`（禁止改 kpis / monthly / planDefaults 数字）。
  6. 下期规划按 `google-quarterly-plan.md` 写九章。预算默认三档（维持本期 / +30% / +50%）+ 建议档月度 30/35/35，标「基于历史数据」，不是已批预算；CPA/询盘不外推；禁止自动调价/暂停指令。
  7. `google-quarterly render --data ./snap-p10/google-quarterly.json --out ./snap-p10/google-quarterly-report.html --lang <zh|en>`。
  8. **render 成功即停并交付**该 HTML。封面称呼已按区间写好：完整自然季是「季度」，从 1 号起的同一个月（含未过完的本月）是「月度」，其余是「本期」。**禁止**打开或修改 HTML，**禁止**再把「季度 / 月度」改一遍，**禁止**再 render，**禁止**未要求就转 PDF、截图或用视觉模型验收。
- **产物**：HTML 路径；新探索（视频 / PMax / 发现 / 展示）全无量则模板自动隐藏该章。
