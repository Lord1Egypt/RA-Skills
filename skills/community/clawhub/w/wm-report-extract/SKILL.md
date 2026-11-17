---
name: wm-report-extract
display_name: "财报提取 Financial Report Extractor"
version: 0.6.1
description: 财报 PDF（年报/半年报/季报，A 股 + 港股 IFRS）内容理解与按需可溯源提取。双轨转换（Docling FAST + PyMuPDF 有框线表格接管 + ACCURATE 报表页精修）→ 可提取性 meta → adapt-plan 提取剧本 → 全表 records 预提取 → materialize 分表 → 定型晋升 + 质量门（勾稽校验/数值存在性/quote 回验）→ review-extract 独立审核。每个数值带页码与原文 quote 溯源，无 quality.json / review.json 不得给下游。Standalone——`fetch --pdf-url` 无需任何 API key 即可全链路运行；可选接入 WinMale 平台启用 symbol 模式。Use when the user asks to extract or locate data in a financial report PDF (annual/semi-annual/quarterly), e.g. 货币资金、前十大股东、分红方案、全量核心数据、第 N 页内容。
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# 财报提取

对财报 PDF（年报/半年报/季报）做**内容理解**：先产出可提取性 meta 文件（这份财报有什么、在哪、质量如何），再**根据用户需求**做数据提取——要特定内容就提特定内容，要全量就全量提取。无预定义模式，需求驱动；每个提取值可溯源到 PDF 页码与原文。

## 何时使用

- 「从 XX 年报里提取货币资金、前十大股东」
- 「把这份年报的核心数据全量提取出来」
- 「XX 年报第 N 页说了什么」
- 「深入解读这家公司的年报，需要的数据都拿出来」

## 不要用本技能

| 用户说法 | 改用 |
|----------|------|
| 财报列表 / 最新年报 PDF 在哪 | 让用户提供 PDF 或公开直链（A 股可用巨潮资讯网 cninfo.com.cn） |
| 三表数字、关键指标（平台口径） | 用本技能全量提取；WinMale 平台用户另可用 wm-statements / wm-data |
| 本地没有 PDF 且无法下载 | 让用户提供文件或公开直链 |

## 依赖与预期

- 转换阶段需 `docling`+`pymupdf`（约 1-2GB，Python 3.10+，实测 docling 2.120.2 / PyMuPDF 1.24.14）；`scan/locate/cache` 无需。**解释器选择**：优先 `WM_REPORT_PYTHON` 指定的解释器，未设置时用 PATH 上的 `python3`；执行与依赖安装须用**同一个**已装 docling/pymupdf 的解释器，勿用 managed venv。
- 转换为双轨混合：Docling FAST 全档（版面/叙述/无框线表）+ PyMuPDF `find_tables` 接管有框线页表格（零幻觉、带单元格 bbox）+ ACCURATE 精修无框线报表页（约 10-24 页）。300 页年报约 **6-12 分钟**——**建议后台运行**；`--accurate` 可全档 ACCURATE（约 30-35 分钟，最高精度档）；sha256 缓存幂等，二次提取秒级命中。
- darwin 上默认 CPU（`--device cpu`），规避 MPS 内核崩溃。
- 本地已有 docling 模型缓存时**默认离线运行**（自动设 HF_HUB_OFFLINE，避免 HuggingFace revision 在线检查在网络波动时卡死转换；需更新模型时 `unset HF_HUB_OFFLINE TRANSFORMERS_OFFLINE`）。

## 七步流程（必须按序，产物落缓存可审计）

脚本门面（路径按已安装 pack，下同）：

```bash
python3 <skills_root>/wm-report-extract/scripts/wm_report.py <subcommand>
```

### ① 获取 + 转换（fetch / convert）

```bash
# 经 WinMale 平台查链接并下载（symbol 模式，可选；未接平台请用 --pdf-url 直链）
python3 …/wm_report.py fetch --symbol 601633 --filing-type annual [--report-date 2025-12-31]
# 或直链 / 本地路径
python3 …/wm_report.py fetch --pdf-url https://…/report.pdf
python3 …/wm_report.py convert <pdf路径|cache_id>   # 建议后台：耗时 8-20 分钟
```

产物：`report.md`（每个 PDF 页起始处 `<!-- page:N -->` 标记，表格已转 markdown，文本 NFKC 归一化）、`pages.json`（含每页竖线/横线统计）、`fitz_tables.json`（fitz 轨道表格的页内顺序与 bbox）、`convert_meta.json`。缓存 `~/.cache/wm-report-extract/{sha12}/`。

表格来源双轨仲裁（convert 内自动）：有框线页（竖线网格 + fitz 检出 ≥3 行）用 PyMuPDF 表格（数值全部来自页面文本，零幻觉，带 bbox）；无框线/三线表页用 Docling，其中报表页（资产负债/利润/现金流量表）自动 ACCURATE 精修；同页文本相似的纯文本表保留 docling 版（语义结构更好，fitz 版去重抑制）。`meta.json` 的 `tables[].track` 标注来源；跨页续表类型只从本合并链链头继承（防类型传染），同类型多条独立物理链各自成表不混源拼接（canonical 给结构分最高链）。

### ② 内容理解 meta（scan）

```bash
python3 …/wm_report.py scan <cache_id> --summary
```

`meta.json` 是后续一切的依据：

- `industry_hint`：行业探测（bank/automobile/…，特征词+置信度）→ 决定覆盖清单行业扩展组
- `document_profile`：`market/script/accounting/convert_health/novelty` 画像；低置信行业保持 `industry=null`
- `filing_kind`：`annual` / `q1` / `semi` / `q3` / `quarter` / `prospectus`
- `chapters` 章节树（正文锚点→目录回退）/ `sections` 子节锚点（`from_toc:true` 需复核）
- `tables[]` 全表 schema：headers/单位/期间列/科目样本/续表合并（`continued`）/类型——**类型是提示，headers 才是证据**
- `priority` 优先指引：按 coverage-checklist 通用层+行业层分组给出入口（结构性三表 > 特异签名表 > 锚点区间 > 关键词）
- `anomalies[]` 异常与降级（异常不中断，是处置依据，见下表）

| code | 处置 |
|------|------|
| `convert_failed` / `encrypted` / `convert_missing` | blocker：告知用户，建议解密/`--ocr`/`--accurate` 重转 |
| `low_text_page` | 该页可能是扫描图：值需跨页复核，必要时 `--ocr` 重转 |
| `table_fragment` | 碎表：改用正文键值对提取或相邻表拼接 |
| `chapters_from_toc` | 章节 page 为印刷页码与物理页有偏移，定位优先 `sections`/`tables`（物理页） |
| `missing_chapter_anchors` | 章节/目录均未解析出：用 `sections` + `locate` 定位 |
| `kangxi_compat` | quote 为 NFKC 归一化文本，与 PDF 原字符可能不同形 |
| `garbled` / `long_table` / `header_noise` / `table_type_unknown` | 复核、分段读、忽略版式噪声、读表头确认类型 |

### ②½ 方案适配（adapt-plan）

```bash
python3 …/wm_report.py adapt-plan <cache_id> [--result <result-...>]
```

产物：`result-*/adapt_plan.json`。以**报告正文**（章节/表标题/行标签）为最高优先级信号，行业组为先验：

- `observed_signals` / `promote_priority` / `expected_but_missing`：内容锚定覆盖与晋升顺序
- `coverage_groups`：先验 A–I + 行业 X 组（`industry=null` 时仅通用层）
- `q1/q3`：完整 MD&A 叙述标 `not_applicable`
- `low_text_page` / `garbled`：给出 `--ocr` / `--accurate` 建议

### ③ 全表 records 确定性预提取（extract-tables）——应提尽提的机制保证

```bash
python3 …/wm_report.py extract-tables <cache_id>          # → records.json（秒级）
python3 …/wm_report.py locate <cache_id> "存货" --records # 按科目行检索（含断词归一匹配）
```

`records.json`：每张表每个数据行 → `{table, page, type, row_label, label_norm, values[{value,period,header}], unit, headers}`。数百页年报产出数千条行级记录，**每条可溯源到表+页**。三表/摘要等已定型；续表自动继承类型；跨页续表已合并。

### ④ 结构化分表（materialize-tables）

```bash
python3 …/wm_report.py materialize-tables <cache_id> [--force]
```

产物：`result-{ts}/manifest.json + tables/*.json + gaps.json + promote_candidates.json`。Python 只做高置信定型；其余进 generic。表格数据必须优先消费分表文件。

### ⑤ Agent 定型晋升（type_promote）

读 `promote_candidates.json`（每张 generic 的 title/headers/前 8 行/`type_hint`/`filing_kind`），对照 coverage-checklist **分析意图** 决定是否晋升。只输出 `confidence=high` 的项：

```bash
python3 …/wm_report.py apply-promotions <cache_id> --file promotions.json [--result result-…]
```

- 按「这张表回答哪个分析问题」晋升，禁止写死品牌/公司名
- 混两类或低置信 → 保持 generic
- 季报不要硬升年报才有的组
- 同类型多张物理表：第一张用稳定 `table_id`，其余为 `{type}_p{page}_i{index}`，禁止静默合并

**规则化预晋升（0.6.1 起必跑，Agent 晋升的前置）**：行业 allowlist ∪ 跨业态邻接白名单
（hint 共现 ≥2，如煤电一体的 power_generation）内每 hint 取首个候选自动晋升，无总数上限：

```bash
python3 …/wm_report.py auto-promote <cache_id> [--result result-…]
```

### ⑤½ 叙述证据扫描（narrative-scan，0.6.1 起）

```bash
python3 …/wm_report.py narrative-scan <cache_id> [--result result-…]
```

- 通用 MD&A 4 项 + 各行业叙述/required_gaps 的 needles（`domain/narratives.py` 声明式）
- needle 命中 → 自动 `found`（quote+page，过 review 硬门回验）；未命中 → `agent_tasks/`
  证据包（章节区间/页码/excerpt/needles）——**程序不判 not_disclosed，留 Agent 终审**

### ⑤¾ Agent 闭环（agent_tasks 协议，0.6.1 起）

对 `agent_tasks/*.json` 的待办，Agent 读证据包后写 `agent_tasks_done/*.json`：

| 任务 | 输出 | 机器校验 |
|------|------|----------|
| `narrative_close`（叙述/gap 终态） | `found`（quote+page）/ `not_disclosed`（reason≥8字）/ `not_found` | quote 逐字在 report.md 且页码一致 |
| `qa_adjudication`（勾稽仲裁） | `rule_limitation`（附 rationale，标注保留不删）/ `real` | finding 必须存在于 quality.json |
| `industry_confirm`（行业确认） | 目录内 industry | industry 必须在 INDUSTRY_HINTS |

```bash
python3 …/wm_report.py agent-apply <cache_id> [--result result-…]   # 校验不过即拒（exit 1）
```

### ⑥ 质量门（qa-tables，给下游前必跑）

```bash
python3 …/wm_report.py qa-tables <cache_id> [--result result-…] [--verdicts qa-verdicts.json]
```

- Python：列错位、缺单位、垃圾表头
- Python v2 质量门（对照 PDF 原文）：
  - **勾稽校验**：资产=负债+权益恒等、合计=Σ分项（减:项为负、其中:项跳过）、期初+增减=期末、同比%用金额重算——失败记 `identity/subtotal/roll/yoy_mismatch`（degraded，不删行）
  - **数值存在性**：表内每个数字必须真实出现在溯源页 PDF 文本（`value_not_on_page`；超 30% 整表 demote）
  - **quote 回验**：行 quote 逐字（NFKC 归一化）存在于溯源页（`quote_unverified`）
- Agent：语义复核 typed 表（会议议程冒充激励表、利润变动原因冒充海外经营等）→ `demote` 或 `split`
- 产物 `quality.json`；**无此文件或未跑 QA，禁止把 typed 表交给分析角色**
- `status=fail` 表示发生过 `demote`/`split`；下游仍只消费 `verdict=pass` 的 typed 表；suspect 数值/quote 进 `gaps.json` 供复核

### ⑥½ 独立审核（review-extract）

```bash
python3 …/wm_report.py review-extract <cache_id> [--result <result-...>]
```

- 审核与提取角色分离：**审核不改表，只读产物打分**
- 硬门：`quality.json` 存在、叙述 `found` 必须有 quote+page、`required_gaps` 必须终态、quote 可回验、画像一致性、**年报/半年报三表定型**（`statement_signature_gap`）
- 软门：一季报/三季报三表缺一、demote/split、未 promote 的非噪声 `type_hint`
- QA：三表行标签须命中科目词；假利润表（公司名当 item）→ demote
- novelty / hard fail 时写 `derived/evolution_proposal.json`（含 `actions`、`missing_type_signatures`、`noise_type_hints`）；**只产 proposal，不自动改规则库**

### ⑥¾ HTML 阅览（render-html，可选）

```bash
python3 …/wm_report.py render-html <cache_id> [--result result-...] [--out report.html]
```

- 产物默认：`result-*/report.html`（单文件自包含，系统字体，可离线打开）
- **只嵌入 `quality.json` 中 `verdict=pass` 的表** + gaps / review / QA findings；只读，不在页面改数；typed 表展示 `variant` 徽标（primary/parent_company/summary/analysis/supplementary）
- 侧栏按覆盖组导航；三表切换；行点击展开 quote+页码抽屉

### ⑥⅞ 一键收口（close，auto-heal，0.6.1 起）

```bash
python3 …/wm_report.py close <cache_id> [--result result-...]
```

依序执行 auto-promote → narrative-scan → agent-apply（若 `agent_tasks_done/` 有产物）
→ qa-tables → review-extract，输出**最小待办清单**（`todo_tasks`）。禁止：静默改数字、
无 quote 的 found、跳过 quality.json。完整闭环见 `references/workflow.md` 的 auto-heal 节。

> 质量门不可取消。0.6.1 起 `close`（auto-heal）已落地：规则化 auto-promote + narrative-scan 叙述证据 + agent_tasks 协议闭环 + 再 qa/review，替代按公司手写 `close_*.py`，**不放宽硬门**。

### ⑦ 按用户需求制定方案 + 执行提取

固定覆盖按 coverage-checklist。清单外 / 定型表覆盖不到的项走 **个性化抽取**：

```bash
python3 …/wm_report.py resolve <cache_id> --need "合同负债" --need "存货" --write-fields
```

产物（L2 首选）：`result-{ts}/fields/<field_id>.json` + `result-{ts}/fields/_batch.json`，并回填 `result-{ts}/manifest.json -> catalog.fields[]`（提供可枚举的 FieldRecord 证据索引；每个数值带页码与 quote，可复核）。**0.6.0 起港股 IFRS 三大报表已可定型（简繁签名）；非报表港式表仍可空，convert + resolve 照跑。**

L2 传统备选（legacy）：`extract-query` 仍可用，但它把 `value` 留空给 Agent（禁止写入 PDF 之外数字），用于需要更复杂“切片级”语义时。

第三方（东财/现货网站）数字 **不得** 写入 adhoc.json——PDF 没有就是 `not_in_pdf`；研究包用 L3 Web 另记。

## 输出形态

- 给人：正文结论 + 关键数字表（每行带页码角标）+ 来源 footer。
- 给 Agent：`result-{ts}/manifest.json` + `adapt_plan.json` + `quality.json` + `review.json` + 仅 `verdict=pass` 的 `tables/*.json` + `narratives/*.json` + `gaps.json`。

## 禁止

- 无 `quality.json` 就把 typed 表交给下游分析。
- 把 Python `type_hint` 或未晋升的 generic 当成稳定 `table_id`。
- 全量提取时跳过 D_mda / C_segments，或把变动原因表只抽成金额。
- 把具体公司品牌名、口号写进 plan 或覆盖清单。
- 编造数值/页码；quote 必须逐字（NFKC 归一化后）来自该页。
- 用第三方数据源（东财/同花顺等）补 PDF 里没有的数——not_found 就是 not_found；不得写入 adhoc.json。
- macOS 上用 `--device mps`（Metal 内核崩溃）；默认 cpu。
- 港股报告：0.6.0 起三大报表签名/章节锚/行业词已简繁适配；仍定不出的表（港式非报表版式）**不要跳过 convert / locate / resolve**，改走 L2 个性化抽取。美股/英文报告：锚点库未适配，同样走 L2。

## 深入参考

| 需要 | 读 |
|------|----|
| 四步操作细节与故障排查 | [references/workflow.md](references/workflow.md) |
| 溯源契约、缺口复盘、derived 规则 | [references/provenance.md](references/provenance.md) |
| 全量提取覆盖清单 | [references/coverage-checklist.md](references/coverage-checklist.md) |
| 锚点/表格签名模式库（扩展指南） | [references/anchors.md](references/anchors.md) |
| 规则演进/新行业适配提案流程 | [references/adaptation.md](references/adaptation.md) |
| 请求/响应示例 | [examples/](examples/) |
