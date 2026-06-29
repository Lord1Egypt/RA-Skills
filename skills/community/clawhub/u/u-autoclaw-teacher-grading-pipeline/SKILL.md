---
name: teacher-grading-pipeline
description: Design or implement a bilingual lightweight teacher grading pipeline for K12 paper exams and homework. Use when the user discusses or asks to build workflows involving scanners, document cameras, mobile scanning apps, RFID/QR divider pages, teacher-provided answer keys, AI OCR/vision APIs, dual-provider verification, local deterministic scoring, teacher/student memory archives, Excel/Web/PDF reports, printable feedback, or HermesDesktop/OpenClaw skills for grading, marking, reviewing, exam analysis, wrong-question collection, and class learning analytics. 设计或实现中小学纸质试卷/作业批改流水线：高拍仪/扫描仪/手机扫描、RFID/二维码分隔页、教师标准答案、大厂 OCR/视觉接口、双接口校验、本地判分、教师与学生记忆库、成绩表、Web 可视化、PDF 打印报告、错题归集和班级学情分析。
---

# Teacher Grading Pipeline / 教师批改流水线

Brand context / 品牌归属：U-AutoClaw Portable Intelligent Data Warehouse / U-AutoClaw 便携式智能数据仓，www.wboke.com

## Publishing Notes / 发布说明

This skill is an orchestration and design skill. It does not include API keys, student data, teacher data, or proprietary provider credentials. When implementing a real system, users must configure their own OCR/AI provider credentials and comply with local privacy, school, and vendor policies.

本技能是流程编排和实现指南，不内置任何 API 密钥、学生数据、教师数据或第三方服务商凭证。真实落地时，用户需要自行注册并配置 OCR/AI 服务商接口，同时遵守当地隐私、学校和服务商政策。

This skill can be published as part of the U-AutoClaw Portable Intelligent Data Warehouse education workflow collection. Public references should credit: U-AutoClaw 便携式智能数据仓, www.wboke.com.

本技能可作为 U-AutoClaw 便携式智能数据仓教育工作流能力的一部分发布。公开展示时请标注：U-AutoClaw 便携式智能数据仓，www.wboke.com。

## Core Posture / 核心定位

Build a lightweight orchestration skill, not a full self-built marking engine. Prefer existing high-quality OCR, document parsing, and AI grading APIs. Keep HermesDesktop responsible for workflow, grouping, local scoring, review queues, memory, exports, and reporting.

构建轻量级批改流程编排能力，而不是从零自研完整阅卷引擎。优先组合成熟 OCR、文档解析和 AI 批改接口。HermesDesktop/OpenClaw 负责流程、分组、本地判分、异常审核、记忆沉淀、导出和报表。

Position it as a practical education workflow for U-AutoClaw Portable Intelligent Data Warehouse: local capture, local organization, cloud/provider adapters when users opt in, and structured outputs teachers can keep.

可将其定位为 U-AutoClaw 便携式智能数据仓的教育工作流：本地采集、本地归档、用户选择后接入云端/大厂接口，并生成教师可长期留存的结构化成果。

Default scope:

- K12, especially primary and middle school.
- Standard-answer-based grading first.
- Objective and semi-objective questions first: choice, true/false, fill-in, numeric answers, oral arithmetic, final-answer checks.
- Avoid fully automatic subjective grading unless the user explicitly accepts review risk.
- Require teacher-provided answer keys before scoring.

默认范围：

- 中小学，尤其是小学和初中。
- 先做有标准答案的批改。
- 优先做选择、判断、填空、数字答案、口算、最终答案核对。
- 主观题不默认全自动批改，除非用户明确接受审核风险。
- 判分前必须先有教师提供的标准答案。

## Recommended Workflow / 推荐流程

Use this pipeline unless the user gives a stronger local pattern:

1. Ingest scans from a scanner, document camera, phone scanning app, watched folder, or manual upload.
2. Group pages by student using RFID/QR/divider-page rules.
3. Extract page metadata, student identity, answers, and question structure through one or more providers.
4. Normalize answers locally.
5. Compare extracted answers against the teacher answer key with deterministic rules.
6. Cross-check providers when high reliability is requested.
7. Send uncertain items to a teacher review queue.
8. Generate formatted Excel score sheets, local Web dashboard, PDFs, per-student printable evaluation reports, wrong-question lists, and class analytics.
9. Update teacher memory and student learning archives separately.

中文流程：

1. 从扫描仪、高拍仪、手机扫描 App、监听文件夹或手动上传导入试卷。
2. 通过 RFID、二维码、条码或分隔页规则按学生分组。
3. 调用一个或多个 OCR/AI 服务提取学生身份、页面信息、作答内容和题目结构。
4. 本地标准化答案。
5. 按教师标准答案进行本地确定性判分。
6. 高可靠模式下做双接口交叉校验。
7. 不确定项进入教师人工审核队列。
8. 生成格式化 Excel 成绩单、本地 Web 仪表盘、PDF、学生个人打印报告、错题列表和班级学情分析。
9. 分别更新教师记忆库和学生成长档案。

## Identity And Page Grouping / 身份识别与分卷

Treat student identity as a first-class problem. Do not rely on AI guessing from mixed pages when a deterministic marker can exist.

Priority order:

1. RFID student tag or card.
2. QR/barcode divider page.
3. Divider-page OCR fields: name, student ID, class, exam name.
4. Name/student-number area on the paper.
5. Handwriting and student-answer continuity as auxiliary evidence.
6. Manual review.

For batch scanning, prefer one divider page before each student:

```text
Name
Student ID
Class
Exam Name
QR/barcode or RFID binding
```

When the QR/barcode/RFID value changes, start a new student packet. Put following pages into that packet until the next identity marker appears. If no marker is found, use handwriting and answer continuity only as a secondary confidence signal.

Never use printed question text as a similarity signal for student grouping. Strip or ignore printed regions and compare only handwriting zones, fill-in zones, answer boxes, and fill bubbles.

中文规则：

- 学生身份识别优先于答案识别。
- 每个学生前放一张分隔页，或使用 RFID/二维码/条码绑定学生。
- RFID、二维码或条码发生变化时，视为新学生试卷开始。
- 后续页面归入当前学生，直到下一个身份标记出现。
- 印刷题干不能作为学生雷同率或分卷依据。
- 只把手写区、填涂区、答题区作为辅助连续性判断。

## Provider Strategy / 服务商策略

Expose providers at the same level and let the user configure credentials on first use:

- Tencent Cloud question grading / education OCR.
- Baidu intelligent homework grading / education OCR.
- Alibaba education OCR / paper splitting / formula OCR.
- Mathpix or formula-specific OCR for math-heavy papers.
- General vision models for page understanding and JSON extraction.
- Local OCR such as PaddleOCR as fallback or privacy mode.

Support modes:

```text
Fast mode: one provider only.
Stable mode: primary provider plus low-confidence or sampled backup.
High-reliability mode: two providers for all pages/questions.
```

When using two providers, compare at question level before accepting results. Auto-accept only when answers, correctness, score, and confidence are within configured thresholds. Otherwise send to teacher review.

中文策略：

- 多个服务商同层级提供，不默认绑定单一厂商。
- 首次调用时由用户选择服务商并配置自己的 API Key/Secret。
- 支持快速模式、稳定模式和高可靠模式。
- 高可靠模式可把同一页面或题目提交给两个厂商，结果一致或差异在阈值内才自动写入成绩。
- 超出阈值、置信度低或两个接口冲突时，进入人工审核。

## Data Boundaries / 数据边界

Keep input, working data, output, and long-term memory separate.

Recommended top-level layout:

```text
data/
  input/
  working/
  output/
  memory/
  templates/
```

Preserve original images/PDFs as evidence. Use JSON for machine-readable state. Use Markdown for human-readable summaries and AI context. Use Excel/PDF/HTML for final delivery. Use TXT only as raw OCR cache when useful.

Never mix teacher memory with student memory.

Teacher memory captures:

- Identity and teaching context.
- Common phrases and feedback style.
- Historical comments and viewpoints.
- Rubrics, scoring preferences, and parent-communication tone.
- Civilized, encouraging, reminder-style report phrasing for different subjects and grades.

Student memory captures:

- Identity, class, and roster metadata.
- Exam history, wrong questions, scores, and knowledge points.
- Ability curves, recurring mistakes, handwriting/answer habits.
- Teacher review corrections and learning-profile updates.

## Review And Trust / 审核与可信度

Design for "first two runs are calibration, later runs are automation":

```text
Run 1: teacher verifies almost everything; learn templates, answer formats, roster, provider behavior, and teacher style.
Run 2: teacher verifies anomalies; harden thresholds, templates, and comments.
Run 3+: automatic batch processing with exception review.
```

Always keep an exception queue for:

- Unknown or duplicated student identity.
- Missing, duplicate, or out-of-order pages.
- Provider disagreement.
- Low OCR confidence.
- Answer-key mismatch.
- Score differences above threshold.
- Suspected folded-page, duplex, or scan-quality issues.

Every final score should be traceable to the original image, provider result, normalized answer, answer key, rule, and any teacher correction.

中文原则：

- 前两次使用主要用于校准试卷模板、教师风格、学生名单、接口阈值和常见错误。
- 第三次以后尽量自动批量处理，只把异常项交给老师。
- 每一个最终得分都要能追溯到原图、接口结果、标准答案、判分规则和教师修改记录。

## Student Evaluation Reports / 学生个人评估报告

When generating per-student reports, write according to the student's grade, subject, and learning stage. Use civilized, encouraging, reminder-style language. Never use insulting, humiliating, sarcastic, discriminatory, or overly harsh wording.

Each report should include:

- Student identity and exam metadata.
- Total score and question-level correctness.
- Which questions were right and wrong.
- Why each wrong question may have been wrong, based on answer evidence and knowledge points.
- Key lost-score points and mastered points.
- Short, actionable improvement suggestions.
- Teacher-style comments adapted from teacher memory.
- Optional color visualizations for color printers.

Use formatted tables for score sheets, question-level results, wrong-question lists, and knowledge-point summaries. Do not output long unstructured text when a table is more readable. Prefer PDF/HTML templates that print cleanly on A4. Support black-and-white fallback, but design charts, highlights, and section labels so a color printer can produce clearer reports.

中文要求：

- 每个学生可生成一份单独的试卷评估报告。
- 报告要按年级、学科和学生身份写，语气文明、鼓励、提醒、具体。
- 严禁羞辱、讽刺、歧视、粗暴否定或不文明用语。
- 成绩、题目、错题、知识点尽量表格化。
- 支持 A4 PDF/HTML 打印，优先适配彩色打印机，同时兼容黑白打印。
- 可展示错题截图、原卷裁剪图、扣分原因和提升建议。

## References / 参考

Load [references/design.md](references/design.md) when designing architecture, schemas, folder layouts, or implementation plans for this grading pipeline.

需要设计架构、数据结构、文件夹、报表模板或实现计划时，读取 [references/design.md](references/design.md)。

