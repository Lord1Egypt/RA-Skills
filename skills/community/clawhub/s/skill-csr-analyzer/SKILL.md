---
name: csr-analyzer
slug: csr-analyzer
displayName: "CSR分析技能"
description: "判断用户提供的文档是否属于汽车行业质量管理体系 IATF 16949 中的客户特定要求 (Customer-Specific Requirements, CSR)。直接触发词：判断CSR、客户特定要求、CSR审核、IATF CSR、CSR分析。语义触发：当用户消息中包含'客户要求'+'质量体系'、'OEM特殊要求'、'汽车客户额外要求'、'供应商质量手册'等组合时自动激活。文档分析触发：分析这份文档、帮我看看这份 配合文档附件上传时激活。This skill should be used when the user wants to determine whether a document contains IATF 16949 CSR content, or when uploading automotive quality documents for classification."
agent_created: true
version: "3.0.0"
---

# CSR Analyzer — IATF 16949 客户特定要求判断

## Overview

Analyze user-provided documents (PDF/Word/Excel/TXT) to determine which clauses — if any — qualify as Customer-Specific Requirements (CSR) under the IATF 16949 automotive quality management system. Output a structured, clause-by-clause judgment report with confidence scoring.

**能力边界（本技能不做以下事情）：**
- ❌ 不提供 IATF 16949 标准全文解读（仅判断 CSR 归属性）
- ❌ 不提供合规咨询或整改建议（仅做分类判断）
- ❌ 不替代第二方审核或客户官方 CSR 确认
- ❌ 不处理非汽车行业的质量管理体系文档（如 ISO 9001 通用要求、医疗器械 ISO 13485 等）
- ❌ 不从互联网检索 OEM CSR 文档（仅分析用户提供的文档）

## Trigger Detection

Activate this skill when the user's message matches any of the following patterns:

**Direct triggers (exact match or near-match):**
- `判断CSR` / `CSR审核` / `CSR分析` / `IATF CSR`
- `客户特定要求` / `客户特殊要求` / `顾客特定要求` / `顾客特殊要求`

**Semantic triggers (combination patterns):**
- "客户要求" + "质量体系" / "16949"
- "OEM特殊要求" / "OEM额外要求"
- "汽车客户" + "要求" / "手册" / "标准"
- "供应商质量手册" / "供应商要求手册"

**Document-analysis triggers (with attachment):**
- `分析这份文档` / `帮我看看这份` / `检查这个文件` (when an attachment is uploaded)
- Any file upload accompanied by automotive/quality-related context

**负面触发（以下情况不应激活本技能）：**
- 用户仅询问 IATF 16949 标准条款含义 → 用通用知识回答
- 用户要求编写质量管理体系文件 → 不属于 CSR 判断范畴
- 用户上传的文档明确与汽车行业无关（如食品、医疗、建筑） → 不激活

## Input Specification

| 属性 | 要求 |
|------|------|
| 支持格式 | PDF、DOCX、XLSX、TXT |
| 文件大小 | 单文件 ≤ 50MB；超出时提示用户拆分 |
| 语言 | 中文、英文、中英混合 |
| 文档类型 | OEM CSR 文件、供应商质量手册、质量协议、客户要求清单等 |
| 附件数量 | 单次分析 1 个文件；多文件时逐个处理 |

## Workflow

### Step 1: Receive, Parse, and Build Document TOC

- Accept PDF, DOCX, XLSX, or TXT files.
- Use appropriate tools (pdf skill for PDF, docx skill for Word, xlsx skill for Excel) to extract full text.
- For scanned PDFs (image-based), first attempt OCR extraction. If text is unextractable, report and ask the user for a text-accessible version.
- Preserve all clause/section numbering and structure during extraction.

**⚠️ 关键新增（解决 R4 结构未解析）：解析后必须先建立文档原生章节目录（TOC）。**
- 用正则/规则扫描全文，提取所有带编号的章节标题，例如：`第4章`、`§4.1`、`4.3`、`4.5.2`、`附件四`、`表1` 等。
- 输出一张 TOC 清单：`<原生编号> — <标题>`（如 `§4.4 — 特殊特性的识别及验证`）。
- 后续逐条分析**必须基于这张 TOC 遍历**，不得自由分段后声称"全覆盖"。
- 报告末尾的"覆盖率"自检须对照这张 TOC 勾选。

**异常处理：**
- **空文档或无可提取文本**：报告"文档内容为空或无法提取文本"，停止分析，建议用户检查文件。
- **超大文档（>50MB）**：提示用户拆分后重新上传，不强行处理。
- **不支持的格式**（如图片、压缩包）：明确告知不支持，列出支持的格式。
- **文本提取不完整**（如 PDF 部分页面为扫描件）：标注提取覆盖率，仅对已提取部分分析，未提取部分在报告中标注。

### Step 2: Pre-screening

Before detailed analysis, perform a quick pre-screen:

1. **Is the document from a known automotive OEM or Tier 1 supplier?**
   Check for company identifiers (logos, headers, footers, document properties).
   Reference `references/iatf16949_csr.md` for the known OEM list.

2. **Does the document reference IATF 16949 or ISO/TS 16949?**
   Search for keywords: "IATF 16949", "ISO/TS 16949", "16949", "质量管理体系".

3. **Does the document impose requirements beyond standard IATF 16949?**
   Look for language patterns: "in addition to", "shall also", "must also", "exceeds", "more stringent", "as a minimum", "at a minimum".

If all three pre-screening questions are negative, the document is unlikely to contain CSR — state this clearly and skip to summary.

**⚠️ 反幻觉红线（解决 R5 语言/幻觉）：预筛查中列出的每一个工具或术语（APQP / PPAP / FMEA / MSA / SPC / CMM …），都必须先在文档全文检索确认其字面出现。未检索到的术语严禁列入"行业特征/工具链"描述；若仅能推断"应有"，须标注"（推断，文档未明示）"。例如：文档未出现 MSA 一词，则不得写"全文贯穿 MSA"。**

**参考文件缺失处理：** 如果 `references/iatf16949_csr.md` 不存在或无法读取，不中断分析，改用内置的 IATF 16949 常见 CSR 条款知识进行判断，并在报告中注明"参考知识库未加载，基于通用知识判断"。

### Step 3: Clause-by-Clause Analysis

**⚠️ 关键新增（解决 R2 大词偏向）：先用下面的「条款识别清单」在文档中网罗候选条款，再逐条判断。模型不得只盯着 APQP/PPAP/PFMEA 等"明星工具"，操作层要求（CMM、封样、条形码、项目经理等）同样是 CSR。**

#### 条款识别清单（命中任一信号词即进入候选池）

| 类别 | 信号词 |
|------|--------|
| 核心工具 | APQP、PPAP、FMEA、PFMEA、DFMEA、控制计划、SPC、特殊特性、防错、遏制、**MSA（仅限文档实际出现时）** |
| 批准/认可 | OTS、样件、封样、留样、首件、工装样件、生产件批准、书面认可、事先批准 |
| 测量/检验 | CMM、三坐标、检具、量具、校验、校准、定期确认检验、全检、100%检验、早期遏制、过程能力、Cpk |
| 追溯/标识 | 条形码、永久标识、永久性标识、追溯性、批次、序列号、唯一标识 |
| 组织/人员 | 项目经理、质量负责人、管理者代表、副总经理、人员资质、培训、上岗 |
| 变更控制 | 变更、工程变更、设计变更、书面认可、事先批准、通知需方 |
| 分供方 | 分供方、外包、外协、二供、供应链、联合审核 |
| 指标/目标 | PPM、直通率、合格率、零缺陷、不良率、质量目标、质量指标 |
| 交付/文件 | 合格证、检验报告、发货清单、随货文件、质量记录、保存期 |
| 库存/物流 | 呆滞品、包装、运输、防护、储存、先进先出 |
| 审核 | 体系审核、过程审核、产品审核、二方审核、飞行检查、突击检查 |
| 不合格处置 | 不合格品、退货、挑选、返修、报废、永久性破坏、遏制 |

**对 TOC 中的每个条款，对照四个维度分析：**

| Dimension | Question | Indicators |
|-----------|----------|------------|
| **D1: IATF 16949 具体条款号引用** | 条款中是否出现 **具体条款号**（如 §8.3.4.4 / 第8.3.4.4条 / clause 8.3.4.4）？ | "Per IATF 16949 §X.X.X", "In addition to clause X.X.X", 交叉引用表 |
| **D2: 汽车客户来源** | 要求是否由汽车 OEM 或 Tier1 供应商发出？ | 文档中公司名、OEM 专用格式、供应商门户来源、笼统提及"IATF 16949 要求" |
| **D3: 超出标准** | 条款是否施加了超出 IATF 16949 的要求？ | "Shall also", "additionally", "exceeds", "more frequent than", "tighter than", "at minimum", 具体量化时限/频次/指标 |
| **D4: 强制性** | 要求是强制（shall/must）还是建议（should/may）？ | "Shall", "Must", "Required", "须", "应" vs. "Should", "Recommended", "May", "建议" |

**⚠️ D1 硬约束（解决 R1 口径漂移）：**
- **D1 = ✓ 当且仅当**条款中出现形如 `§X.X.X` / `第X.X.X条` / `clause X.X.X` / `8.3.4.4` 的**具体条款号引用**。
- 仅出现 "IATF 16949" / "按照 IATF 16949 要求" 等**笼统表述 → D1 必须为 ✗**（这些归 D2 支撑）。
- **反幻觉红线**：若全文无任何具体条款号，则所有条款 D1 一律 ✗，严禁因"明显属于 IATF 主题"而打 ✓。

**⚠️ §10 类"违约责任/赔偿"章节处理（解决 R3 一刀切）：**
- **排除单位 = 单条，不是整章。** 不得因章节标题含"违约/赔偿/罚则"而整体剔除。
- 逐条判断：若该条实质规定了**质量体系要求或质量指标**（如 PPM 指标表、不合格品的破坏性处置、随货文件要求、质量义务），**判为 CSR**；仅当该条纯粹是**金额罚则 / 申诉流程 / 争议解决**，才判为非 CSR。
- 同一段落里 CSR 条与非 CSR 条可并存。

**⚠️ 语言理解红线（解决 R5 读反）：**
- **析取词**："A 或 B" / "A 或者 B" = 满足任一即可。**严禁**读成"必须 A"或"非仅 A"。例：协议"通过 IATF 16949 或 ISO9001 认证" → 不得写成"必须通过 IATF 16949（非仅 ISO9001）"。
- **差异对比表"标准要求"列**：若不确定 IATF 16949 的具体要求/数值，填"待核实"或省略，**不得臆造**标准侧内容来衬托 CSR 侧。

### Step 4: Classification + Confidence Scoring

For each clause, assign one of three labels **and a confidence score (1-5)**:

- **属于 CSR** — At least D1+D3 or D2+D3 are positive, and D4 is mandatory.
  - 置信度 5：四个维度全部满足，依据明确
  - 置信度 4：三个维度满足，依据较明确

- **存疑 (Uncertain)** — Partial match on dimensions, insufficient information to confirm.
  - 置信度 3：两个维度满足，但缺少关键信息
  - 置信度 2：仅一个维度满足，信息不足

- **不属于 CSR** — Does not meet the CSR classification criteria.
  - 置信度 5：明确无 IATF 16949 关联且非汽车客户
  - 置信度 4：标准原文复述，无额外要求

**⚠️ 置信度为每条必填项**，不得留空。允许且预期存在"存疑"条目（见 Step 5）。

### Step 5: Quality Self-Check（强制、绑定执行，不得形式化）

在生成报告前，**逐项**执行以下自检，并将结果写入报告"质量自检结果"表：

1. **覆盖率检查（对照 Step 1 的 TOC）**：
   - 逐条核对 TOC 中每个条款是否已被分析。
   - 若未穷尽（如文档过长抽样），报告头部必须明确标注「本次为抽样覆盖，共分析 N / X 条，未覆盖：…」，**严禁**写"全覆盖"。
   - 勾选「已基于 TOC 遍历」或「已说明抽样范围」。

2. **一致性检查**：相似条款的判断结果是否一致？如有矛盾，复查并调整。

3. **依据完整性**：每条判断是否都有一句话依据？无依据的条目标记为"存疑"。

4. **D1 一致性**：全文中是否存在具体条款号？若不存在，确认所有 D1=✗。

5. **边界情况复核**：参考 `references/iatf16949_csr.md` 中的"判断中常见的边界情况"；重点复查「§10 类章节是否做了单条拆分」「操作层要求是否漏判」「析取词是否被误读」。

6. **存疑合理性**：若最终「0 存疑」，必须逐条说明为何每条都无可疑点；否则应重新审视边界条款，将至少模糊条目标为"存疑"。

### Step 6: Generate Report

Generate BOTH a complete markdown report file AND a summary in the conversation.

**6a. Write the full markdown report to a file:**

Create a file named `CSR-report-{文档简称}.md` in the current working directory. The file MUST contain the complete analysis with the following sections. Do NOT truncate or summarize — include every clause analyzed.

The report file structure:

```markdown
# CSR 判断报告

## 文档信息
- **文件名**：
- **文档类型**：
- **文档来源（OEM/供应商）**：
- **涉及 IATF 16949 版本**：
- **分析日期**：
- **覆盖说明**：全覆盖 / 抽样覆盖（共分析 N/X 条，未覆盖：…）

## 预筛查结果

| 筛查维度 | 结果 | 依据 |
|----------|------|------|
| 汽车行业客户来源 | ✓/✗ | 具体依据（所列工具/术语须已在文档检索确认） |
| IATF 16949 引用 | ✓/✗ | 具体依据 |
| 超出标准要求 | ✓/✗ | 具体依据 |

## 文档原生章节目录（TOC）
（列出解析得到的全部带编号条款，供覆盖率核对）

## 逐条判断

| 序号 | 协议原生条款号 | 条款摘要 | IATF 映射章节 | D1 | D2 | D3 | D4 | 判断结果 | 置信度 | 判断依据 |
|------|--------------|----------|--------------|----|----|----|----|----------|--------|----------|
| 1 | §4.4 | | §8.3 | ✗/✓ | ✓/✗ | ✓/✗ | 强制/建议 | 属于CSR/存疑/不属于CSR | 1-5 | 一句话依据 |

> 注意：「协议原生条款号」填文档自带编号（如 §4.4、§5.6.2、§7.7.3），「IATF 映射章节」填对应 IATF 16949 章节（如 §8.3、§8.5）。**两列不得混用**——协议 §5.1 不等于 IATF §5.1（领导作用）。

## 汇总统计

- **属于 CSR 条目**：N 条（其中置信度≥4：N条）
- **存疑条目**：N 条
- **非 CSR 条目**：N 条
- **平均置信度**：X.X / 5.0

### IATF 16949 章节分布

| 章节 | CSR 条目数 | 涉及条款 |
|------|:---------:|----------|
| §X.X | N | 条款摘要 |

### 关键差异点对比

| 维度 | IATF 16949 标准要求（不确定填"待核实"） | 本协议 CSR 要求 |
|------|----------------------------------------|-----------------|
| | | |

## 质量自检结果

| 检查项 | 结果 |
|--------|------|
| 覆盖率（已对照 TOC，或已说明抽样范围） | ✓/✗ |
| 一致性（相似条款判断一致） | ✓/✗ |
| 依据完整性（每条有依据） | ✓/✗ |
| D1 一致性（无条款号则全 ✗） | ✓/✗ |
| §10 类章节已单条拆分 | ✓/✗ |
| 存疑合理性（0 存疑须说明） | ✓/✗ |

## 结论

（一段总结性文字，描述文档的 CSR 特征和关键发现，包含整体置信度评价）
```

**6b. Output a brief summary in conversation:**

After writing the file, present a compact summary to the user: total clauses analyzed, CSR count, uncertain count, non-CSR count, average confidence, and the path to the report file. Use `present_files` to surface the report file to the user.

**CRITICAL**: Never skip the file writing step. The `.md` report file is the primary deliverable — the in-chat summary is secondary.

## Constraints

1. **ALWAYS write the full report to a `.md` file.** The report file is the primary deliverable. Never only output a summary in the conversation — the complete analysis must be persisted to disk. Use `present_files` to surface it to the user.
2. **Do not explain CSR definition or IATF 16949 background** unless the user explicitly asks. Execute judgment only.
3. **Output in Chinese** by default (user is a Chinese speaker). Keep format clean and structured.
4. **For scanned/image PDFs with no extractable text**: attempt basic OCR; if that fails, report the limitation and do not fabricate analysis.
5. **When uncertain**: use "存疑" rather than forcing a binary classification. The user can provide additional context.
6. **If the document is completely unrelated to automotive quality**: state this clearly and stop — do not force-fit clauses.
7. **Do not access the internet** to look up OEM CSR documents — analyze only what the user provides.
8. **Do not store or transmit document content** outside of the analysis session — no caching, no logging to external services.
9. **(R1) D1 硬约束**：无具体条款号引用则 D1 必须 ✗，不得放宽。
10. **(R2) 宽网罗**：必须使用「条款识别清单」网罗操作层要求，不得只判 APQP/PPAP/PFMEA。
11. **(R3) 单条拆分**："违约责任/赔偿"章节按单条判断，不得整章排除。
12. **(R5) 反幻觉**：① "A 或 B" 不得读成 "必须 A / 非仅 A"；② 预筛查/依据/差异表列出的工具术语须先在文档检索确认，未出现不得列入；③ 差异表"标准要求"列不确定则填"待核实"，不得臆造。
13. **(R6) 自检绑定**：置信度每条必填；覆盖率须对照 TOC；"0 存疑"须逐条说明。

## Trust & Safety Declaration

- **数据处理**：用户上传的文档仅在当前会话中分析，分析完成后不保留文档内容。报告文件仅包含分析结论，不包含原文完整复制。
- **权限边界**：本技能仅读取用户主动提供的文件，不主动访问文件系统其他位置，不执行网络请求。
- **安全红线**：本技能不执行任何脚本代码，不调用系统命令，不修改用户文件（仅创建分析报告文件）。
- **中文优先**：所有输出默认使用中文，符合国内用户使用习惯。

## Analysis Example

以下是一个完整的判断示例，展示本技能的输出标准：

> **输入条款**："根据 IATF 16949 第 8.3.4.4 条，供应商必须在产品批准过程中提交 Level 4 PPAP，且过程能力指数 Cpk 必须 ≥ 1.67（标准要求 Cpk ≥ 1.33）。"

| 维度 | 结果 | 依据 |
|------|------|------|
| D1: IATF 16949 引用 | ✓ | 明确引用 §8.3.4.4 |
| D2: 汽车客户来源 | ✓ | OEM 要求 |
| D3: 超出标准 | ✓ | Cpk≥1.67 vs 标准 1.33 |
| D4: 强制性 | ✓ | "必须" |
| **判断** | **属于 CSR** | 置信度 5/5 |

> **反例（D1 应为 ✗）**：条款"供方应按照 IATF 16949 要求建立质量管理体系"——仅笼统提及 IATF 16949，**无具体条款号**，D1 = ✗，由 D2 支撑。

更多示例见 `references/iatf16949_csr.md` 中的"CSR 判断示例"章节。

## References

- `references/iatf16949_csr.md` — IATF 16949 关键条款与常见 CSR 模式、主要 OEM 列表、判断示例、边界情况。
  - **加载时机**：当文档内容涉及不熟悉的 OEM 名称、异常条款结构、或需要核对 IATF 16949 标准要求时加载。
  - **搜索模式**：如需查找特定条款，使用 `grep -n "条款编号" references/iatf16949_csr.md`。

## Changelog

| 版本 | 日期 | 变更 |
|------|------|------|
| 3.0.0 | 2026-07-08 | 根因修复六处：R1 D1硬约束(无具体条款号必✗)、R2 增「条款识别清单」宽网罗操作层要求、R3 §10类章节改单条拆分、R4 Step1新增文档原生TOC遍历、R5 反幻觉(或/非仅误读、未现术语不得列入、标准侧待核实)、R6 自检绑定(置信度必填、覆盖率对照TOC、0存疑须说明)；报告模板增「协议原生条款号」「IATF映射章节」双列防止编号混淆 |
| 2.0.0 | 2026-07-04 | 按 TRACE 五维度全面升级：新增置信度评分、质量自检、异常处理、能力边界声明、Trust 安全声明、输入规范、分析示例 |
| 1.0.0 | 2026-06-XX | 初始版本：基础四维度分析框架 + 报告模板 |
