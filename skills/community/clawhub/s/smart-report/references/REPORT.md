# REPORT.md — 积木 · 方法论卡 · report_spec · 事实/论点台账 · assembler

SKILL.md 之外的报告层完整规范。方法论卡细节在 `../templates/`（通用纪律卡[恒读]/简报卡/问卷数据卡/目标对照卡）。

***

## 1. 章节积木（B1~B10）

积木 = 叙事目标 + 首选图表 + 常用 transform + 写作要点。积木是**按需取材的知识卡**，不是大纲填空表——章节由洞见自由组织，需要某类分析（趋势/构成/漏斗/相关…）时查表选型防错。

| ID | 积木 | 叙事目标 | 首选图表 | 常用 transform | 写作要点 |
|----|------|----------|----------|----------------|----------|
| B1 | 指标概览 | 量化结果与达成 | 按结论定形态：达成单值→gauge/liquid（**必传 `--target`**，否则 achievement 为 null）；趋势→line（叠目标线）；结构→pareto/pie；排名→bar | mean/sum 聚合 | 先给绝对值再给相对值；达成类给目标基线 |
| B2 | 趋势走向 | 随时间怎么变 | line / area / combo | pivot_table 长转宽 | 指出方向、斜率变化点、峰值谷值及日期 |
| B3 | 结构构成 | 整体由什么组成 | pie / treemap / stacked_bar | groupby → name+value | Top1+Top2 占比必给；超 6 类先合并尾类 |
| B4 | 对比排名 | 谁多谁少差距多大 | bar / pareto | groupby + sort_values | 给头尾两端的具体差值，不只说"最高最低" |
| B5 | 分布形态 | 数据长什么样 | histogram / boxplot | 数值列直取 | 中心、离散、偏态、离群点四要素（数值直接引用 stdout：histogram 的 `bin_counts`/`peak_bin`，boxplot 的 `columns`） |
| B6 | 转化漏斗 | 流程在哪损耗 | funnel | 分阶段计数 | 逐级给转化率（直接引用 stdout `extra.conversion`），点出损耗最大的一级 |
| B7 | 相关关系 | X 与 Y 什么关系 | scatter / bubble | 双数值列 | 点出离群点身份（label-col）；相关系数引用 stdout `extra.correlation`（小样本告警见 advisories；相关≠因果的通用纪律见通用纪律卡·诊断） |
| B8 | 流向转移 | 从哪来到哪去 | sankey / graph | rename → source/target/value | 主流向前 3 条路径必给数值 |
| B9 | 明细清单 | 证据可查 | spreadsheet | 筛选 / TopN | 报告中的表格节；超 100 行先 TopN |
| B10 | 异常识别 | 哪里不对劲 | boxplot / line+标注 | diff / 阈值标记 | 先界定"何为异常"（口径），再列异常点 |

**降级通用规则**：数据不支持首选图表时，按 B6→B4（无阶段列）、B1→B4（无数值目标）、B7→B5（仅单数值列）方向降级；B1 有目标值但 headline 非单值结论时优选 B2（line 叠目标线），交付语声明。

***

## 2. 方法论卡查阅指引

**默认路径是自由组装**（无强制模板匹配）：先理解数据、形成洞见、自由组织章节；**通用纪律卡恒读**，其余按触发键（一页式汇报→简报卡；问卷形态→问卷数据卡；目标/复盘/ROI→目标对照卡）按需查阅核对防错清单，而非套用骨架。卡片不设固定章节顺序、不设图数配额，也不存在「必备章节」——是否采纳由论点需要决定。

何时查哪张卡：

1. 每份报告 → 恒读 **通用纪律卡**（口径/叙事/诊断/周期纪律）
2. 受众是领导且要求短（一页/简报）→ 查 **简报卡**（克制原则）
3. 数据形态：问卷/调研（低基数分类列、题号列、量表值域）→ **问卷数据卡**；目标/对照（目标、预算、成本列，或复盘/ROI）→ **目标对照卡**
4. 无命中形态 → 只用通用纪律卡即可，不硬凑领域卡

**输出语言**：方法论卡中的中文章节名（如「执行摘要」「分析一」）仅为语义示例，
实际报告的章节标题与叙事语言跟随用户语言（与 CLI `--lang` 自动跟随数据语言的行为一致）；
用户使用英文或其他语言时，不得照抄中文骨架标题。

***

## 3. report_spec.json 规范

Step 6 由 agent 写出，assembler 消费。用 `json.dumps(..., ensure_ascii=False)` 生成，不手写拼接。

```json
{
  "title": "结论式主标题（数字取自台账）",
  "subtitle": "口径 + 时间范围 + 数据来源",
  "theme": "default",
  "executive_summary": "3~5 句，最后写，从各章结论汇总；T8 用作核心结论",
  "sections": [
    {
      "id": "s1",
      "title": "结论式章节标题",
      "narrative": "论证式叙事（主张 + 证据引用 + 解释），数字占位符化或来自台账；\\n\\n 分段",
      "chart_path": "chart_01.html",
      "annotation": "图表下方说明文字（与 Step 5 注入图表的 --annotation 同源）"
    },
    { "id": "s2", "title": "无图章节", "narrative": "...", "chart_path": null }
  ],
  "appendix": {
    "methodology": "数据来源、清洗方法（transform 要点）、统计口径",
    "caveats": "数据局限、样本说明、未覆盖范围"
  }
}
```

placeholder 模式下（`--ledger-mode placeholder`），上例中所有数值字段改写占位符，例如：

```json
"title": "全年销售额{{total_sales:,.1f}}万元，{{top_region}}万元居首",
"narrative": "3月单月销售额即达{{peak_month:,.1f}}万元，环比{{mom_change:+.1f}}%。"
```

字段规则：

* `title`/`sections`（≥1 节，每节 `title` 必填）缺省 → `REPORT_SPEC_INVALID`
* `theme` 取 default/classic/dark，**必须与 Step 3 的 `--theme` 一致**
* `chart_path` 相对 `--charts-dir` 解析（也可绝对路径）；填 CLI stdout 返回的 `html_path` 文件名；`null` = 纯文字节
* `annotation` 可空；spreadsheet 图表节的 annotation 正常渲染
* `executive_summary`/`appendix` 可空（T8 模板附录可省，口径写脚注/章节内）
* `id` 会净化为锚点（非字母数字→`-`），建议直接用 `s1`/`s2`…；与目录联动

assembler 错误码：`5001 REPORT_SPEC_INVALID`（spec 缺字段/非法）· `5002 CHART_HTML_INVALID`（图表文件不可解析）· `5003 REPORT_ASSEMBLE_ERROR`（组装异常）· `5004 LEDGER_MISMATCH`（scan 模式数字未溯源 / placeholder 模式占位符未注册）· `5005 LEDGER_RAW_NUMBER`（placeholder 模式下出现裸数字）· `5006 EXPORT_SSR_FAILED`（Node SSR 图表静态化失败）· `5007 EXPORT_DEPENDENCY_MISSING`（docx/pptx 可选依赖缺失）· `5008 CLAIM_EVIDENCE_INVALID`（论点台账形式校验失败）。错误结构与 CLI 同构（`error`/`code`/`code_name`/`details.suggestion`），处理方式沿用 Exit Criteria。

组装产物结构：封面（title/subtitle/时间）→ 目录（锚点）→ 执行摘要 → 各章节（标题/叙事/图表/annotation）→ 附录 → 页脚。图表以 chartOption 提取方式内联（ECharts 只载一份，交互保留：tooltip/legend/dataZoom；单图页的改名面板与保存按钮不进报告）。

***

## 4. 台账体系：事实台账（ledger.json）+ 论点台账（claims.json）

Step 4 建、落盘；Step 6 由 assembler `--ledger` / `--claims` 程序校验；Step 7 验收。事实台账是报告唯一的数字来源；论点台账是报告的分析主张清单，每个论点强制声明论据，构成「论点 → 论据 → 事实」硬证据链。

```json
[
  {"id": "rev_h1", "metric": "总营收", "value": 2670, "unit": "万元",
   "source": "chart_01.plot_stats.sum", "sections": ["s1", "summary"]},
  {"id": "trend_h1", "metric": "涨跌幅", "value": 23.0, "unit": "%",
   "source": "chart_02.plot_stats.series[0].trend.delta_pct", "sections": ["s1", "summary"]}
]
```

* 字段：`id`（引用键）/ `metric` / `value`（数字或数字字符串，与文本同量纲：文本写"98.6%"则 value 为 98.6，写"2670 万元"则 value 为 2670）/ `unit` / `source`（图 + plot_stats 字段；手算标 `data_preview`）/ `sections`（引用位置，可省）
* 提取时机：Step 3 的批量 stdout（每图的 `plot_stats` + `data_preview`）。**入账前先用 `source_rows`/`plotted_rows`/`unique_entities` 对账聚合口径**——`plotted_rows == source_rows` 说明没聚合、各系列 value 之和等于 `source_rows` 而非 `unique_entities` 说明按行而非按实体统计，漏去重会直接暴露在三元组里
* 硬规则：正文/摘要/结论的每个数字先入台账再引用；多处引用从台账复制；派生数字（差值/占比变化）也入账

### 4.1 引用模式一：scan（默认，向后兼容）

正文直接写数字，assembler 全量扫描比对：

* **校验范围**（assembler 对 title/subtitle/摘要/章节标题/叙事/图注/附录全量扫描）：
  - 必须溯源：带小数的数字（98.6% / 17.1 个百分点 / 53.0）、>=100 的整数（2670 / 543 / 108）、紧邻 %/％/倍/个百分点的数字（37% / 2 倍）
  - 忽略：日期（2025-01 / 2025 年 / 6 月 / Q3）、图号（图 2）、章节引用（§1）、计数语境的纯小整数（<100 且非百分比形态，"3 个类别" / "Top 5"）
  - 容差：按文本显示位数四舍五入比对（文本 98.6 可命中台账 98.56）
  - 未溯源 → exit 1 + `5004 LEDGER_MISMATCH`（details.misses 列出数字/位置/上下文）；`--ledger-check warn` 可降级为仅警告
* 已知局限：扫描法存在语义盲区（整数百分比 37% 靠启发式识别、计数与统计数字边界靠规则推断），复杂表述可能漏检/误检

### 4.2 引用模式二：placeholder（推荐，根治校验盲区）

叙事中的数字一律写成占位符，由 assembler 替换：

* 语法：`{{台账id}}`（原样替换）或 `{{台账id:格式符}}`（Python format 规范，如 `{{total_sales:,.1f}}` → 18,858.9）
* 校验（替换后全量扫描，规则同 4.1 的必溯源清单，但无扫描盲区）：
  - 占位符 id 不在台账 → `5004`（details 列出未注册 id）
  - 格式符输出与台账值精度不符（如 `:,.0f` 截断 4561.8 → 4562）→ `5004`（精度守卫）
  - 替换后残留裸数字（未用占位符写的统计值）→ `5005 LEDGER_RAW_NUMBER`（details.misses 精确到字段）
  - 日期/图号/章节引用/计数语境小整数照常豁免
* 原则：**数值全部占位符化**（title/subtitle/executive_summary/sections 的 title/narrative/annotation/appendix）；规格写法示例见 SKILL.md Step 6
* 选择：新报告一律用 placeholder；scan 仅为兼容 1.0.x 存量 spec 保留

### 4.3 论点台账（claims.json 落盘）

`claims.json` 与 `ledger.json` 同在 Step 4 落盘，报告中每个分析论点一条记录。**它由 Step 2 的洞见雏形补全而来**（不是事后另写）：`claim` 即洞见的「主张」，`evidence` 补上 Step 3 的含图章节 id 与 Step 4 的 ledger 事实 id。因此 claim 是叙事骨架——每节 narrative 的「主张」必须与对应 claim 的 `claim` 一致。

```json
[
  {"id": "c1", "claim": "华东区营收下滑拖累整体",
   "evidence": ["rev_h1", "s3"], "section": "s3", "type": "结论"}
]
```

* 字段：`id`（唯一引用键）/ `claim`（论点主张文本，含数字时数字必须已入事实台账）/ `evidence`（论据 id 数组，至少 1 项）/ `section`（可选，论点所在章节 id）/ `type`（可选，如「结论」「发现」「建议」）
* **evidence 可引用三类 id**（assembler 程序解析）：
  - 事实 id：`ledger.json` 中的条目 id（如 `rev_h1`）
  - 含图章节 id：`report_spec.json` 中 `chart_path` 非空的章节 id（如 `s3`，该章节的图表即视觉论据）
  - 图表文件 stem：spec 引用的图表文件名去扩展名
* **形式校验（代码强制，机械可判定，`--claims` 启用）**：
  1. 每个 claim 必须声明至少一个 evidence → 缺则报 `5008 CLAIM_EVIDENCE_INVALID`
  2. 每个 evidence id 必须可解析（上述三类之一）→ 未注册报 `5008`（同现有 5004 的处理方式）
  3. claim 文本中的必溯源数字必须命中事实台账值（沿用 4.1/4.2 的数字识别与容差规则）
  4. `section` 若填写必须指向真实章节 id
* **`--claims-check coverage`（可选强制级）**：在 basic 之上补齐「章节 → 论点」两个方向的反向覆盖，构成「叙事/图 → 论点 → 论据」闭环：
  1. 每个含图章节被至少一个 claim 引用——「每张图都能被追溯到一个需要图证的论点」（violation：`uncovered_chart`）
  2. 每个含叙事（`narrative` 非空）的章节被至少一个 claim 的 `section` 指向——「每段叙事都能锚定到一个论点」（violation：`uncovered_narrative`）
* **边界（重要）**：代码只做形式校验（论点挂了论据、论据真实可定位）；**「论据是否真支撑论点」的实质校验是 LLM 职责**，生成时自评并在交付语声明
* HTML 报告自动附「附录·论点与论据」表（论点/论据/章节三列，与「关键数据溯源」表并列）

***

## 5. 报告写作规范（叙事层）

* **章节标题写结论**：主谓宾+数值（「营收同比增长 23%」），不用名词短语（「营收分析」）
* **报告主标题**：全文最重要的一条结论；时间范围/筛选条件/数据来源放 `subtitle`
* **执行摘要最后写**：从各章结论提炼 3~5 句，每句都要有台账出处
* **章节叙事 = 论证（三层缺一不可）**：① 主张（本节结论，即对应 claim 的 `claim` 文本）② 证据（引用 ledger 事实 id / 图表，数字占位符化）③ 解释（为什么 / 与什么对比 / 意味着什么 / 影响或下步）。**narrative 不写图注**——annotation 才说「这张图」（类型+覆盖范围+最显著事实+口径）；交付前确认每图 `annotation_source` 为 `'user'`（`'default'` 表示代码用模板填充，须补写解读重新生成）
* **结论与建议节**（T2/T3/T4/T5/T6）：建议必须由正文证据支撑，每条建议可指回某章
* 数字表述：`x_cardinality` 按语义表述；百分比给基数；大数用万/亿分位并保持全文一致

***

## 6. assembler 用法

```bash
# 基础：仅 HTML（scan 模式）
python {skill_base}/scripts/report_assembler.py \
  --spec report_spec.json \
  --charts-dir ./sr_charts \
  --output ./sr_report/report.html \
  --ledger ledger.json \
  --claims claims.json

# 推荐：placeholder 模式 + 论点全覆盖 + 多格式导出
python {skill_base}/scripts/report_assembler.py \
  --spec report_spec.json \
  --charts-dir ./sr_charts \
  --output ./sr_report/report.html \
  --ledger ledger.json \
  --claims claims.json --claims-check coverage \
  --ledger-mode placeholder \
  --format html,docx,pptx
```

* `--charts-dir`：spec 中相对 `chart_path` 的解析基准（默认 spec 同目录）
* `--ledger ledger.json`：启用数字溯源校验（推荐始终传入）；`--ledger-check warn` 降级为仅警告（scan 模式专用）
* `--claims claims.json`：启用论点台账形式校验（推荐新报告始终传入；规范见 4.3）
* `--claims-check basic|coverage`：论点校验级别（默认 basic = 论点有论据 + 论据可解析 + 论点数字可溯源；coverage = basic + 每张图必须被至少一个论点引用 + 每段叙事必须被至少一个论点的 section 指向）
* `--ledger-mode scan|placeholder`：台账引用模式（默认 scan；规范见 4.1/4.2，推荐 placeholder）
* `--format html|docx|pptx|all`：导出格式，逗号分隔（默认仅 html）。docx/pptx 为静态交付版：
  - 管线：图表 chartOption → Node SSR（`scripts/export_charts.js`，需 Node ≥ 16）渲染 SVG → `resvg-py` 光栅化 PNG → python-docx / python-pptx 组装（中文字体、原生表格、台账附录自动内嵌）
  - 依赖缺失（node/resvg-py/python-docx/python-pptx 任一）→ 该格式记入 stdout `export_errors`（错误码 5007），HTML 照常产出，不中断不伪装成功；依赖清单见 `requirements-optional.txt`
  - SSR 子进程整体失败 → `5006 EXPORT_SSR_FAILED`，同上降级
  - 中间产物（SVG/PNG/manifest）落 `--export-dir`（默认 `<output>_assets/`），便于复检
* `--export-dir`：自定义中间产物目录
* 校验通过时 stdout 报告对象含 `ledger` 统计：`{"checked": true, "mode": "scan|placeholder", "entries": N, "citations": M, "misses": 0}`；传 `--claims` 时另含 `claims` 统计：`{"checked": true, "mode": "basic|coverage", "claims": N, "evidence_refs": M, "uncovered_charts": 0, "uncovered_narratives": 0}`
* 成功 stdout：`{"report": {"success": true, "report_path": "...", "sections_count": N, "charts_count": M, "theme": "...", "formats": [...], "exports": {"docx": "..."}, "export_errors": {}, "ledger": {...}, "claims": {...}}}`
* HTML 产物单文件自包含（ECharts 内联），离线可开、可打印（print 样式已内置分页避免）；docx/pptx 为独立文件，与 HTML 同目录同名异扩展名
