---
name: smart-report
version: 1.4.0
display_name: 智能报告
display_name_en: Smart Report
description_zh: "将数据文件（CSV/TSV/TXT/XLSX/XLS/JSON）转化为单文件交互式 HTML 报告，内置 ECharts 可视化、自由叙事与硬证据链（事实台账 + 论点台账：每个论点强制声明论据，数字全部可溯源）；也可批量生成独立交互式图表 HTML（26 类图表、3 套主题）。当用户要求从数据文件撰写报告、周报/月报、分析文档、复盘或汇报材料，或提供数据文件要求出图时使用。"
description_en: "Data-to-report skill. Turns data files (CSV/TSV/TXT/XLSX/XLS/JSON) into single-file interactive HTML reports with ECharts visualizations, free-form narrative and a hard evidence chain (fact ledger + claims ledger: every claim must declare its evidence, every number stays traceable). Also batch-generates standalone interactive chart HTML files (26 chart types, 3 themes) via its chart CLI. Use when the user asks to write a report, weekly/monthly report, analysis document, review, or presentation material from data files, or provides data files asking for charts."
---

# Smart Report

> 将数据文件（CSV/Excel/JSON）转化为单文件 HTML 报告（可选导出 DOCX/PPTX 交付版）：**自由叙事 + 硬证据链**——章节结构由洞见驱动自由组织（方法论卡按需参考，非强制骨架），每个论点强制声明论据（claims 台账，assembler 程序校验），每个数字可溯源（facts 台账，支持占位符引用模式）。图表由内置引擎按需批量生成（26 类图表、3 套主题、沙箱 transform）。
> CLI 全参数、flags 语义、错误码表见 [REFERENCE.md](./references/REFERENCE.md)；积木定义、方法论卡查阅指引、report_spec/台账（facts + claims）规范、assembler 用法见 [REPORT.md](./references/REPORT.md)。

> **路径定位（MUST）**：脚本一律用**绝对路径**调用，禁止裸 `python` / 相对路径——命令执行的 cwd 是用户会话目录，不是本技能目录。在 smart-report-expert 专家包内，由 rui.md 的 Step 0 定位 skills 根目录 `$SKILLS` 与解释器 `$PY`，调用形如 `$PY "$SKILLS/smart-report/scripts/cli.py"`。独立使用时，先定位本 SKILL.md 所在目录的绝对路径记作 `$SKILL`，解释器按 `python3 → python → py` 探测、取 `-V` 通过且依赖齐全者记作 `$PY`。下文 `{skill_base}` 一律替换为 `$SKILL` 的绝对路径。

***

## Activation Triggers

* 用户提到「写报告」「周报/月报」「分析报告」「复盘」「汇报材料」「数据报告」「report」，或提供数据文件要求产出带图表的文档
* 仅要单独一张图（不要文档交付物）不是本技能的触发场景——引导用户使用图表类技能

***

## 方法论参考卡索引（按需查阅，非强制骨架）

报告结构**默认自由组装**：先理解数据、形成洞见、自由组织章节；**通用纪律卡恒读**，其余按触发键按需查阅，而非套用骨架。卡片是防错经验库，不是填空表单——不存在「必须匹配」「必须覆盖」。路由键必须是 Step 1 可从数据/意图中**探测**到的属性（数据形态或明确意图），不按行业关键词猜。

| 方法论卡 | 类型 | 触发键 |
|---------|------|--------|
| 通用纪律卡 | 恒读 | 无条件——每份报告动笔前核对（口径/叙事/诊断/周期纪律） |
| 简报卡 | 意图 | 用户要一页式/向上汇报/给领导看的材料 |
| 问卷数据卡 | 数据形态 | 低基数分类列、题号前缀列名、量表值域（1~5/1~7），或明示调研 |
| 目标对照卡 | 数据形态 | 目标/预算/成本列，给定目标值或对照期，或明示达成/复盘/ROI |

**卡片治理（新增卡准入）**：须同时满足 ① 有可探测触发键（数据形态或明确意图，非行业关键词）；② 携带通用纪律/引擎契约/B 表推不出的技术约定；③ 不能机器校验（能校验的进 plot_stats 输出）。行业知识（财务/人力/供应链等）**不预置卡片**——机器管行业无关的不变量（台账溯源、论点挂论据、数据不变量告警），LLM 管行业知识与报告结构。

**没有图数配额**：出多少张图由「论点是否需要图证」决定（见 Step 3），卡片中不含任何配额。

***

## 七步工作流（MUST 按序执行）

**Step 1 · 意图解析 + 理解数据**：确定报告类型、受众、数据文件、时间范围；先读数据（列名/量纲/行数/时间跨度），形成对数据的初步理解。数据文件不存在 MUST 先向用户索要，不得编造。不强制匹配模板——结构由接下来的洞见决定。

**Step 2 · 形成洞见 → 落盘洞见 → 自由组织大纲**：基于任务目标与数据理解形成分析主张，**每章一个洞见四元组，先落盘为 claims.json 雏形**（字段 `id`/`claim`/`evidence`/`section`/`type`，schema 见 REPORT.md 4.3）：
- **主张（claim）**：本章一句话结论
- **证据（evidence）**：支撑主张的数字/图（先占位，Step 4 补 ledger 事实 id 与含图章节 id）
- **为什么**：原因 / 机制
- **意味着什么**：影响 / 下步

据此自由组织章节。**恒读 `templates/通用纪律卡.md`**；其余卡片按触发键按需查阅（一页式汇报→简报卡；问卷形态→问卷数据卡；目标/复盘/ROI→目标对照卡）；数据不支持某分析时如实声明局限。纯文字论点不硬凑图；空洞章节自问是否并入相邻章。**洞见先于图存在**——先有主张，再在 Step 3 决定是否需要图证。

**Step 3 · 图表按需生成**（**唯一判据：该论点是否需要「数据可视化」来支撑/说服**——需要则出图，不需要则纯文字。选型由「结论类型 + 数据形态」查下方选型表决定，不因位于概览章而默认仪表盘。gauge/liquid 仅用于达成类单值结论；多 KPI 概览优先一张 bar 每柱一指标）：确定要出的图 → 一份 `charts.json` → 一次 CLI 调用（≥2 张图 MUST 批量，禁止逐张单图调用）：

```bash
python {skill_base}/scripts/cli.py data.xlsx --sheet "Sheet1" \
  --charts-file charts.json --theme default --output-dir ./sr_charts
```

`charts.json` 每项：`type`（必填）+ `title`/`subtitle`/`x_axis`/`y_axis`（字符串或数组）/`transform_code`/`annotation`/`label_col`/`color_by`/`sort`/`y_scale`/`label`/`width`/`height`/`target`/`x_name`/`y_name`/`series_name`/`series_names`。transform 含中文/引号 MUST 写 JSON 文件，不直接在 shell 传 `--charts`。`--theme` 与 spec.theme 一致。

**Step 4 · 建论据台账（ledger.json + claims.json 落盘）**：两份台账构成硬证据链，缺一不可：
- **事实台账 `ledger.json`（数字层）**：遍历 stdout 各图的 `plot_stats`/`data_preview` 提取关键数值写入（schema 见 REPORT.md），先用 `source_rows`/`plotted_rows`/`unique_entities` 对账聚合口径（是否漏去重、是否按行而非按实体统计）。**硬规则：正文/摘要/结论引用的每个数字必须先入台账再引用，禁止凭记忆写数**；派生数字（差值/占比变化）也入账。
- **论点台账 `claims.json`（主张层）**：由 Step 2 落盘的洞见雏形补全而来（不是事后另写）——`claim` 沿用洞见「主张」，`evidence` 补上 Step 3 生成的含图章节 id 与 Step 4 入账的 ledger 事实 id（schema 见 REPORT.md 4.3）。**硬规则：每个论点必须声明至少一个论据；论点文本中的数字必须已入事实台账；每节 narrative 的「主张」与对应 claim 的 `claim` 一致**——Step 6 由 assembler 程序校验（见 --claims）。
台账引用有两种模式（由 `--ledger-mode` 选择）：**scan**（默认，向后兼容——写死数字，assembler 扫描比对）与 **placeholder**（推荐——叙事中写 `{{台账id}}` 或 `{{台账id:,.1f}}`，assembler 替换并校验精度，杜绝漏检/误检）。新报告优先用 placeholder 模式。

**Step 5 · 逐章叙事（叙事 = 论证，不是图注）**：把 Step 2 落盘的每章洞见展开成自然语言叙事；Step 3 的 stdout `plot_stats`/`data_preview` 提供证据所需精确数值。每节 `narrative` 三层缺一不可：

1. **主张**：本节 claim 的一句话结论（即 Step 2 洞见的「主张」，与 claims.json 对应条目的 `claim` 一致）
2. **证据**：引用 ledger 事实 id / 图表（placeholder 模式写 `{{id}}`，scan 模式写台账数字）
3. **解释**：为什么 / 与什么对比 / 意味着什么 / 影响或下步

**`--annotation` 才负责「这张图」**（类型+覆盖范围+最显著事实+口径），在 Step 3 的 charts.json 里注入，**不写进 narrative**。**无需再跑 `--dry-run`**（Step 3 正式输出已带 plot_stats）。写作规则：**章节标题写结论**（主谓宾+数值，如「营收同比增长 23%」，数字取自台账）；**执行摘要最后写**（从各章结论汇总 3~5 句）。

**Step 6 · 组装**：写 `report_spec.json`（字段规范见 REPORT.md），调用 assembler：

```bash
# 基础 HTML（scan 模式，向后兼容）
python {skill_base}/scripts/report_assembler.py --spec report_spec.json \
  --charts-dir ./sr_charts --output ./sr_report/report.html \
  --ledger ledger.json --claims claims.json

# 推荐：placeholder 模式 + 论点全覆盖 + 多格式导出（html + docx + pptx）
python {skill_base}/scripts/report_assembler.py --spec report_spec.json \
  --charts-dir ./sr_charts --output ./sr_report/report.html \
  --ledger ledger.json --claims claims.json --claims-check coverage \
  --ledger-mode placeholder \
  --format html,docx,pptx
```

`--claims` 启用论点台账校验：论点缺论据、论据不可解析、论点数字未入账 → 报 5008 CLAIM_EVIDENCE_INVALID。`--claims-check basic`（默认）= 论点有论据 + 论据可定位 + 论点数字可溯源；`coverage` = basic + 每张图必须被至少一个论点引用（图→论点）+ 每段叙事（narrative 非空）必须被至少一个论点的 `section` 指向（叙事→论点，推荐）。注意：代码只做**形式校验**（论点挂了论据、论据真实可定位）；「论据是否真支撑论点」的**实质校验**是 LLM 职责——生成时自评并在交付语声明。
`--format` 接受 `html|docx|pptx` 逗号组合或 `all`，默认仅 `html`。docx/pptx 为**静态交付版**：图表经 Node SSR 渲染为 SVG 再光栅化 PNG 内嵌（需 Node ≥ 16 与 resvg-py；缺依赖时报 5007 并继续产出 HTML，不中断）。HTML 恒为主交付物；docx/pptx 按用户需求选用——用户只要网页/交互版 → 仅 html；要 Word 归档 → 加 docx；要汇报演示 → 加 pptx。用户未指定时默认仅 html，交付语中提示可选格式。

**Step 7 · 验收（机械可判定）**：
* ✅ assembler stdout 为 `{"report": {"success": true, ...}}` 且 `report_path` 指向的文件存在且非空
* ✅ spec 中每个 `chart_path` 的图表 HTML 存在且非空（assembler 已强制校验，缺失会报错）
* ✅ 正文关键数字 100% 可溯至 ledger.json（assembler `--ledger` 程序校验；scan 模式漏溯源报 5004 LEDGER_MISMATCH，placeholder 模式裸数字报 5005、未注册占位符报 5004，比 agent 自查更硬）
* ✅ 传 `--claims` 时论点台账校验通过（stdout 含 `claims` 统计：每个论点已声明论据、论据可解析、论点数字可溯源；coverage 模式下每张图都被论点引用、每段叙事都被论点 section 指向）
* ✅ `--format` 含 docx/pptx 时：stdout `exports` 列出的文件存在且非空；`export_errors` 中的格式须在交付语中说明原因（缺依赖属可降级，不算失败）
* ✅ `--format` 含 docx/pptx 且含 echarts 图表时：导出图片数 == 含图章节数（即 stdout 无 `export_errors.partial`；出现 `partial` 说明"导出图片数 < 含图章节数"，属"HTML 成功 + 导出部分失败"，须在交付语中点名缺失章节）
* ❌ 图表 CLI 或 assembler 失败 → 读 `error.details.suggestion`，修正后重试；**同一环节最多重试 2 次**
* 🛑 **仍失败（唯一必须的用户介入点）**：把 `code_name`、`suggestion`、已尝试的修复如实报告用户并给出建议，等待决策。不得静默改用自写脚本兜底。

***

## 图表规划知识（Step 3 直接依赖）

### 契约（6 条，MUST）

1. 列名解析后会被规范化：转小写、特殊字符→`_`（如 `总学时`→`总_学时`），中文保留；`--x-axis`/`--y-axis`/transform 必须引用规范化后的列名
2. transform 沙箱：可用变量仅 `df`/`pd`/`np`（`np.select`/`np.where` 可用），支持多语句（`;` 或换行分隔），必须产出名为 `result` 的 DataFrame；禁止 import/open/try/类定义（黑名单 + AST 白名单强制校验，违规返回带 `suggestion` 的错误）
3. pie/bar 等按「1 个分类列(name) + 1 个数值列(value)」读数据；分类频次图先 transform 聚合成 name/value 两列，再指定 `--x-axis name --y-axis value`
4. 成功时 stdout：`success`/`html_path`/`chart_type`/`title`/`source_rows`/`plotted_rows`/`unique_entities`/`data_rows`/`data_preview`（绘图数据前 10 行，口径校对用）/`annotation_source`/`plot_stats`（绘图数据完整统计摘要，写叙事用；26 类全覆盖）
5. 校对口径直接读 stdout 的 `data_preview` + `data_rows`，不要打开 HTML 搜数据——预览取自 transform 之后、渲染所用的同一份数据，即被绘制内容的真值
6. **聚合口径对账读 `source_rows` / `plotted_rows` / `unique_entities`**：`source_rows`=transform 前原始行数，`plotted_rows`=实际绘图行数，`unique_entities`=去重实体数（有 `--label-col` 取该列，否则取 x 列）。三者关系是"是否忘了去重"的机械判据：`plotted_rows == source_rows` 说明没聚合；各系列 value 之和等于 `source_rows` 而非 `unique_entities` 说明按行而非按实体统计

### 黄金示例

```bash
# 分类频次 → pie/bar（最高频）
--transform-code "result = df['类别列'].fillna('未标注').value_counts().rename_axis('name').reset_index(name='value')"

# 分组聚合 → bar
--transform-code "result = df.groupby('分组列')['数值列'].sum().rename_axis('name').reset_index(name='value')"

# 长→多系列（多列趋势）
--transform-code "result = df.pivot_table(index='<time>', columns='<category>', values='<value>', aggfunc='sum').reset_index()"
```

（gauge/liquid 想出"达成率"时必须补 `--target <目标值>`；缺它 `plot_stats.achievement` 为 `null`。环境自查用 `python {skill_base}/scripts/cli.py --doctor`。transform 含中文/引号时不要直接在 shell 传 `--charts`，写进 JSON 文件用 `--charts-file`。）

**口径陷阱**：聚合前想清楚「按数据行 vs 按去重实体」——统计实体属性先 `drop_duplicates`；生成后对照 `data_preview` + 对账三元组（`source_rows`/`plotted_rows`/`unique_entities`）检查（各行 value 之和等于原始行数而非实体数，就是忘了去重）。

### Chart Types 选型表（26 类）

选型前核对 Required Format；不匹配则用 transform 适配。heatmap/boxplot/radar 等多列图表，各列量纲差异大时先归一化（radar 各系列量级差 >10 倍时 CLI 会挂 advisory 告警；漏斗非逐级递减、散点小样本强相关、sankey 中间节点不守恒同样有 advisory——advisories 字段出现时 MUST 读并在叙事或 caveats 中回应，不得无视）。

| ID | Best For | Trigger Keywords | y_axis | Required Format |
|----|----------|------------------|:------:|-----------------|
| `line` | 时间趋势 | trend, 趋势, 变化, 走势 | 1~N | 1 时间列 + 1~N 数值列 |
| `bar` | 类目对比 | compare, 对比, 排名, 差异 | 1~N | 1 类目列 + 1~N 数值列 |
| `area` | 累计变化 | cumulative, 累计 | 1~N | 1 时间/类目列 + 1~N 数值列 |
| `pie` | 构成占比 | share, 占比, 构成, 比例 | 1 | 1 name + 1 value |
| `scatter` | 相关关系 | correlation, 相关, 关系 | 1 | 2 数值列 或 1+1 |
| `radar` | 多维对比 | multi-dimension, 多维, 综合, 雷达 | N | 1 指标列 + N 数值列 |
| `heatmap` | 交叉密度 | density, cross, 交叉, 矩阵, 热力 | N | 2 类目列 + 1 数值列 |
| `treemap` | 层级占比 | hierarchy, 层级, 嵌套 | 1 | 1 name + 1 value |
| `graph` | 实体关系 | relationship, 网络, 拓扑 | special | source + target (+value) |
| `boxplot` | 分布离群 | distribution, 分布, 离群 | N | N 数值列 |
| `waterfall` | 增量变化 | increment, 增量, 瀑布 | 1 | 1 类目 + 1 数值（增量） |
| `gauge` | KPI 进度 | progress, kpi, 进度, 达成 | 1 | 1 数值列（取均值） |
| `sankey` | 流向转移 | flow, 流向, 流量, 转移 | special | source + target + value |
| `funnel` | 转化率 | conversion, 转化, 漏斗, 流失 | 1 | 1 name + 1 value |
| `sunburst` | 单层占比 | proportion, sunburst, 旭日 | 1 | 1 name + 1 value |
| `wordcloud` | 词频关键词 | word frequency, 词频, 关键词, 词云 | 1 | 1 name + 1 value |
| `histogram` | 分布形态 | distribution, 分布, 直方图 | 1 | 1 数值列（`--x-axis` 或 `--y-axis` 均可，数值型 `--x-axis` 优先） |
| `stacked_bar` | 堆叠构成 | composition, stacked, 堆叠 | 1~N | 1 类目 + 1~N 数值 |
| `bubble` | 三变量相关 | bubble, 气泡, 三变量 | 2 | 2 数值 + 1 size |
| `pareto` | 二八分析 | pareto, 帕累托, 二八 | 1 | 1 类目 + 1 数值 |
| `combo` | 双轴组合 | dual-axis, 双轴, 组合 | 1~N | 1 类目 + 1 bar + 1~N line |
| `venn` | 集合交集 | overlap, 交集, 重叠, 韦恩 | 1 | 1 name + 1 value（交集行 `A∩B`，分隔符 ∩ & + × 与） |
| `mindmap` | 层级大纲 | mind map, 思维导图, 大纲 | 1 | 1 parent + 1 child |
| `orgchart` | 组织架构 | org chart, 组织架构, 层级 | 1 | 1 parent + 1 child |
| `liquid` | 百分比进度 | liquid, 水波, 进度, 完成率 | 1 | 1 数值列（取均值） |
| `spreadsheet` | 明细表格 | table, 明细, 清单, 表格 | N | 任意列（x/y 可选筛选列） |

> **`gauge`/`liquid` 要出"达成率"必须传 `--target <目标值>`**：`achievement` = mean ÷ target。不传时该字段为 `null`（自动推断的量程不是业务目标，比值无业务含义），且输出会挂 advisory。

scatter/bubble/boxplot 中未被 x/y 占用的字符串列自动作为身份列进 tooltip（`--label-col`）。

### Transform 常用模式

* 长转宽: `pivot_table`（见上）
* 宽转长: `result = df.melt(id_vars=['date'], var_name='name', value_name='value')`
* 过滤: `result = df[df['metric']=='revenue'][['category','value']].rename(columns={'category':'name'})`
* 重命名: `result = df.rename(columns={'来源':'source','去向':'target','金额':'value'})`
* 前向填充合并单元格: `result = df.ffill()`
* 瀑布增量: `tmp = df.copy(); tmp['delta'] = tmp['profit'].diff().fillna(tmp['profit'].iloc[0]); result = tmp[['month','delta']]`
* 重命名脏列名（`--header-row` 后仍剩 `score_a`/`unnamed_3` 等）: `result = df.rename(columns={'unnamed_0':'student_id','unnamed_1':'name','score_a':'homework_score','score_b':'exam_score'})`
* 合并子表头到单列名（f-string，沙箱已放行）: `result = df.rename(columns={c: f'{c}_score' for c in df.columns if c not in ['student_id','name']})`
* 不要原地修改 `df`（用 `df.copy()` 或链式操作）；原始数据已匹配目标格式时不传 transform

***

## Hard Constraints (MUST follow)

1. **MUST 走 CLI 工作流**（`cli.py` 批量出图 + `report_assembler.py` 组装），不要自写脚本替代
2. **报告结构自由组织，不强制匹配模板**：`templates/` 下 4 张方法论卡（通用纪律卡[恒读]/简报卡/问卷数据卡/目标对照卡）是防错经验库，按触发键查阅，不作为章节骨架，不存在图数配额
3. **脏表头 MUST 用 CLI flags**（`--skiprows N`/`--header-row N`/`--sheet`，语义见 REFERENCE.md）；N 由实际数据决定（先无 flags 跑一次看原始布局）。**注**：`--skiprows N` 与 `--header-row N` 是同一行为（都是"第 N 行作表头、其上行丢弃"），二选一即可，推荐统一用 `--header-row`
4. **列重命名/重塑/聚合 MUST 用 `--transform-code`**；解析层只解决"哪行是表头"
5. **轴名/系列名要改显示名，MUST 用 `--x-name`/`--y-name`/`--series-name(s)`，不要靠改列名**。改列名会同时改轴名和系列名（两者都绑定列名），副作用大且不可控。显示名才是唯一干净的入口：`--x-name` 改 x 轴、`--y-name` 改 y 轴、`--series-name`（单）或 `--series-names`（多，按可见系列顺序）改系列名。**26 类图表的系列名全部支持此入口**（heatmap/gauge/sankey/liquid 等亦不例外）；gauge/liquid 缺省系列名已用「列名」而非类型名（如「仪表盘」「水波图」），传 `--series-name` 即可覆盖。
6. **MUST report unsupported scenarios**: 不支持的场景（如嵌套 JSON 超 1 层、Word/PPT 之外的私有格式）先向用户说明并给建议，不得静默绕过；docx/pptx 导出缺可选依赖时如实报 5007 并交付 HTML，不伪装成功
7. **MUST NOT 硬编码绝对路径**；运行时解析路径（`{skill_base}` 相对）
8. **不要主动传 `--lang`**；CLI 自动跟随数据语言，仅当用户明确要求时才传
9. **数字 MUST 溯源台账**（见 Step 4 硬规则）；解读的每个数字都必须能在 `plot_stats`/`data_preview` 里找到出处；placeholder 模式下正文的数值一律写 `{{id}}`/`{{id:fmt}}` 引用，禁止手写数字（格式符须与台账精度一致，如 `{{total:,.1f}}`）
10. **论点 MUST 声明论据**：新报告 MUST 落盘 `claims.json` 并在组装时传 `--claims`（推荐 `--claims-check coverage`）；每个论点至少一个 evidence（ledger 事实 id 或含图章节 id），论点文本中的数字必须已入事实台账。代码只做形式校验，「论据是否真支撑论点」由你在生成时自评并在交付语声明
11. **执行摘要最后写**；`x_cardinality` 是去重个数，按 x 列语义表述（x 是「姓名」则说「59 名学生」而非「59 个类别」）
12. **MUST 附解读交付**：交付图表时必须附由 LLM 写的文字解读，并通过 `--annotation` 注入 HTML；成功输出里的 `annotation_source` 标明来源——`'user'`=你传的，`'default'`=代码用模板填充的（此时输出还会挂 advisory），交付前确认是 `'user'`
13. **MUST 显式传 `--output-dir`**，指向用户可见的目录（如 `./sr_charts`、桌面目录、当前工作目录下的显式子目录），默认值 `./smart_charts_output` 会随当前工作目录落盘，用户不易发现产物

***

## 默认策略（不向用户确认）

生成报告是廉价可逆动作（重生成秒级，零外部副作用）。章节组织（由洞见决定）、图表类型（按选型表）、取值口径（按列名/单位/数值范围推断）均由 agent 内部决定，不打断用户。

**事后审阅代替事前确认**：交付语中显式列出关键假设（章节组织思路、图表选型依据、聚合口径、论据链自评结论）。用户不同意任一假设，可一句话要求换结构/换口径/换类型重生成。

***

## Exit Criteria（机械可判定）

* ✅ **成功**: assembler stdout 为 `{"report": {"success": true, ...}}`，`report_path` 文件存在且非空，`--ledger` 校验通过（stdout 含 `ledger` 统计），传 `--claims` 时论点台账校验通过（stdout 含 `claims` 统计）→ 附交付语（关键假设清单 + 论据链自评声明）交付
* ℹ️ `--dry-run` 不算交付：`html_path` 为 null、不落盘，仅用于试错列名或试聚合脚本。写叙事不需要先跑它——Step 3 的批量正式输出已带 `plot_stats`
* ❌ **失败**: `success: false` 或 exit code 1 → 读 `error.details.suggestion`，修正后重试；同一环节最多重试 2 次
* 🛑 **仍失败（唯一必须的用户介入点）**: 如实报告 `code_name`/`suggestion`/已尝试修复，等待用户决策

***

## 指针

* **REPORT.md**：10 种积木定义、方法论卡查阅指引、report_spec 字段规范、事实台账（ledger.json）与论点台账（claims.json）schema 与校验规则、assembler 用法与错误码
* **REFERENCE.md**：CLI 全参数、flags 语义、错误码表、FAQ
* **templates/**：4 张方法论卡——通用纪律卡（恒读：口径/叙事/诊断/周期纪律）、简报卡（意图键）、问卷数据卡与目标对照卡（数据形态键）；防错经验库，按需查阅，非章节骨架
* **scripts/regression_check.py**：开发者端到端回归自测（引擎 26 类图表 + 沙箱逃逸 PoC + 多图/主题/语言/dry-run/annotation + P0/P1/P2 修复项 + 报告全链路 + 论点台账校验），用法 `python {skill_base}/scripts/regression_check.py`
