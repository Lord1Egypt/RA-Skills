---
name: recruiting-resume-screening
description: Use when reviewing one or more Chinese-language resumes against a JD, batch-ranking candidates, identifying red flags and follow-up interview questions, or re-screening a prior candidate batch. Triggers include 发简历给我筛、根据 JD 评估候选人、批量简历筛选、给候选人排序、找出简历疑点、生成面试必问题、根据面试反馈复核排序、重新评估之前那批简历 等。
---

# 简历筛选

## Overview

按岗位 JD（或岗位标准包）对候选人做多维度评估，识别疑点与矛盾，给出排序与面试问题。

**Core principle: 看证据，不看关键词。**

简历出现关键词 ≠ 真的做过 ≠ 做深；必须看项目证据和个人贡献。

## When to Use

- 用户发送一份或多份简历 PDF 要求筛选。
- 用户要求"根据 JD 评估这个候选人"。
- 用户要求"对比这几个候选人"并给排序。
- 用户要求"找出简历里的疑点 / 风险点"。
- 用户要求"生成面试必问题"。
- 用户要求"重新评估之前那批简历"。

如果任务覆盖 JD + 筛选 + 面评的完整流程，先加载 [[recruiting-skillset]]。

## Prerequisites

- 已有岗位 JD 或岗位标准包；没有则先从 JD 抽取核心要求。
- 简历文件已在本地或可获取。
- 本机可用 PDF 提取后端（任一即可，越多越好）：`fitz` (PyMuPDF) / `pdfplumber` / `pdfminer.six`。
- 已了解招聘上下文：团队现状、业务阶段、用人风格。

## Workflow

### Step 1 — 获取并提取简历文本

**不要默认单跑 `pdfplumber`**。中文简历 PDF 常有页边跟踪串、竖排装饰字、隐藏文本层，单一后端不可靠。

推荐命令（脚本见 `scripts/resume_pdf_extract.py`）：

```bash
# 单份 PDF
python3 scripts/resume_pdf_extract.py /path/to/resume.pdf --output-dir /tmp/resume_extract_one

# 批量 PDF / 一个目录
python3 scripts/resume_pdf_extract.py /path/to/resume_dir --output-dir /tmp/resume_extract_batch
```

脚本会：

1. 分别尝试可用的 PDF 后端（`fitz` / `pdfplumber` / `pdfminer.six`）。
2. 做 Unicode 归一化、空白折叠、跟踪串 / 碎片行清洗。
3. 计算 `score / chars / lines / keyword_hits / quality`。
4. 选择分数最高的文本作为正式筛选输入。
5. 输出 `summary.json`、每份 PDF 对应的最佳 `.txt`、Markdown 索引表。

详见 [pdf-extraction.md](pdf-extraction.md)。

### Step 2 — 批量简历必须先做质量分层

用户一次性发送多份简历时**不要直接逐份硬读**。先做一轮 triage，把能直接评估和需要补核的简历分开。详见 [batch-screening.md](batch-screening.md)。

质量分层建议：

- `high`：`chars >= 2600` 且 `lines >= 55` 且 `score >= 65`
- `medium`：`chars >= 1600` 且 `lines >= 35` 且 `score >= 35`
- `low`：低于阈值，标记"待补核"，不阻塞整批交付

### Step 3 — 五维评估 + 疑点识别

每位候选人，从五个维度逐一评估，每维度 ★~★★★★★：

1. 专业匹配度（Skill Fit）
2. 履历稳定性（Career Stability）
3. 潜在风险（Risk Assessment）
4. 抗压与自驱（Resilience & Drive）
5. 团队适配（Team Fit）

完整维度定义与打分依据见 [five-dimension-rubric.md](five-dimension-rubric.md)。

逐条审读简历，主动发现疑点。完整疑点清单（时间类 / 内容类 / 逻辑类 / 行为类）见 [red-flags-catalog.md](red-flags-catalog.md)。每个疑点标注严重程度：

- 🔴 需面试必问
- 🟡 需关注
- 🟢 可能正常

### Step 4 — 综合评级

| 评级 | 含义 | 条件 |
| --- | --- | --- |
| ⭐⭐⭐ **强推** | 直通面试 | 专业匹配度 ≥ 4★ 且无重大风险，总得分 ≥ 20/25 |
| ⭐⭐ **推荐** | 进入面试 | 专业匹配度 ≥ 3★，总得分 ≥ 15/25 |
| ⭐ **待定** | 需电话筛选 | 有亮点但存在明显短板或风险 |
| ❌ **不推荐** | 不进入面试 | 专业匹配度 < 3★ 或存在不可接受风险 |

### Step 5 — 输出评估报告

每人一份**个人评估卡** + 整批**汇总排序表**。模板见 [output-templates.md](output-templates.md)。

### Step 6 — 面试反馈复核（可选）

用户补充技术一面 / HR 二面 / 用人经理初评后，做一次"去偏见复核"：

- 把面试反馈与简历原文逐项对照，区分"有证据支撑"和"主观印象"。
- "能力更强 / 更弱 / 成长性更好"这类结论，若没有具体案例支撑，标记为证据不足。
- 自动化、性能、AI 提效等容易被泛化的能力，默认按"接触过"处理，除非有明确独立负责证据。
- 优先检查时间线、工作年限、离职原因、薪资诉求等是否前后矛盾。

必须输出：总体结论（含排序调整）、逐人可疑点（🔴🟡🟢）、对已有面评的修正建议、终面追问（每人 ≥ 5 个 + 横向必问）、可选《终面准备说明》。

## Red Lines（一票否决）

以下情况直接 ❌ 不推荐，无论其他维度多强：

1. 简历造假或严重夸大（有明确证据）。
2. 方向完全不相关且无转型意愿。
3. 平均在职时间 < 8 个月且无合理解释。
4. 薪酬预期超出岗位预算 50% 以上。

## Anti-Patterns（严格禁止）

| 反模式 | 后果 | 正确做法 |
| --- | --- | --- |
| 凭记忆输出评估结论 | 凭印象漂移 | 必须先提取文本 → 五维评估 → 评级 |
| 复用旧会话结论 | 标准漂移、错过更新 | 重新提取、重新评估 |
| 省略个人评估卡 | 用户无法追溯结论 | 每人必须有完整评估卡 |
| 无文件评估 | 凭空编造 | 找不到简历必须告知用户并请求 |
| "看起来像做了"，3 行总结 | 失真 | 完整执行五维 + 疑点 + 面试题 |
| 把内部过程混入正式报告 | 干扰决策 | 文本提取索引、清洗日志只作内部材料 |
| 全员都给推荐 | 排序失去意义 | 敢下不推荐 / 待定 |

## Self-Check

输出前逐项确认：

- [ ] 每位候选人都提取了简历文本？
- [ ] 每人都有五维 ★ 评分？
- [ ] 每人都有疑点清单（🔴🟡🟢）？
- [ ] 每人都有 3 个面试必问题？
- [ ] 输出了汇总排序表？
- [ ] 评级引用了简历中具体内容作为证据？
- [ ] 不同结论的候选人在排序中区分开？
- [ ] 报告里没有混入提取脚本明细、清洗日志等过程性内容？

## Output Discipline

- Markdown 格式，适合飞书 / Notion 粘贴。
- 中文输出。
- **最终面向用户的报告只保留与筛选决策直接相关的内容**：个人评估卡、汇总排序、亮点、风险、疑点、面试问题、必要的待补核说明。
- **不要输出与筛选无关的过程性版块**：文本提取质量索引、backend/score/chars/lines 统计、清洗日志等只作内部工作材料，除非用户明确要求。
- 评估结论要有理有据，引用简历中具体内容作为证据。
- 不回避矛盾——候选人某方面强但另一方面有风险，两面都写。

## Feedback Loop

完成筛选后主动询问用户：

1. 评级是否准确？哪些人评高了 / 评低了？
2. 是否遗漏了重要评估维度？
3. 面试后的实际表现与评估是否一致？

用户反馈 → 更新本 Skill 的评估标准。新发现的风险模式 → 补充到 [red-flags-catalog.md](red-flags-catalog.md)。重大变更 → 写入 [EVOLUTION.md](EVOLUTION.md)。

## See Also

- [five-dimension-rubric.md](five-dimension-rubric.md) — 五维评估完整定义。
- [red-flags-catalog.md](red-flags-catalog.md) — 疑点完整清单。
- [output-templates.md](output-templates.md) — 评估卡 / 排序表 / 复核报告模板。
- [batch-screening.md](batch-screening.md) — 批量筛选纪律。
- [pdf-extraction.md](pdf-extraction.md) — PDF 提取与多后端 triage。
- [scripts/resume_pdf_extract.py](scripts/resume_pdf_extract.py) — 多后端 PDF 提取脚本。
- [EVOLUTION.md](EVOLUTION.md) — 演化日志。
- 总控流程：[[recruiting-skillset]]；面评：[[interview-evaluation]]。
