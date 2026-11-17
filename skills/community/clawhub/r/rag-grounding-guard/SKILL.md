---
name: rag-grounding-guard
display_name: RAG事实溯源校验（Grounding Guard）
display_name_en: "RAG Grounding Guard"
description: >-
  Verify RAG answers are grounded: per-claim support coverage against retrieved sources, with unsupported claims flagged before the answer ships.

  当用户说『RAG回答胡说八道/编造』『引用对不对』『回答有依据吗』『检索到的资料支撑不了结论』，或要给 RAG/检索增强回答做事实校验时使用。校验每条声明在检索来源里是否有支撑（ grounding 覆盖率），未覆盖的声明标红为幻觉风险，并要求来源带出处（有籍）。可运行脚本（grounding_check 校验器）。理论根基：LGD 三律之有籍(引用溯源)+有证(防幻觉可核验)。触发词：RAG校验、grounding、事实溯源、防幻觉、引用核查、检索支撑、hallucination、回答有依据吗。
version: 1.1.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
agent_created: true
author: 诺声(Logos)@SynomosAI
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, WebSearch
category: AI工程方法
platforms: [windows, macos, linux]
platform_compatibility: [windows, macos, linux]
read_when:
  - RAG/检索增强的回答出现编造或张冠李戴
  - 要核对 AI 声明是否有检索来源支撑
  - 上线一个知识库问答前做事实校验
  - 用户问「你这话有依据吗」
tags: [RAG校验, grounding, 事实溯源, 防幻觉, 引用核查, 有籍]
slug: rag-grounding-guard
title: RAG事实溯源校验（Grounding Guard）
copyright: SynomosAI
description_zh: "当用户说『RAG回答胡说八道/编造』『引用对不对』『回答有依据吗』『检索到的资料支撑不了结论』，或要给 RAG/检索增强回答做事实校验时使用。校验每条声明在检索来源里是否有支撑（ grounding 覆盖率），未覆盖的声明标红为幻觉风险，并要求来源带出处（有籍）。可运行脚本（grounding_check 校验器）。理论根基：LGD 三律之有籍(引用溯源)+有证(防幻觉可核验)。触发词：RAG校验、grounding、事实溯源、防幻觉、引用核查、检索支撑、hallucination、回答有依据吗。"
description_en: "Verify RAG answers are grounded: per-claim support coverage against retrieved sources, with unsupported claims flagged before the answer ships."
classification:
  skillhub: ["security-compliance"]
  iso_25010: ["Security"]
risk_tier: medium
risk_rationale: "门禁批量补丁默认 medium（内部约定：本 skill 设计为中等风险）：调用 API/读写文件/本地执行，最小权限，密钥走 Secret；若实际涉对外代执行(push/发布/发送/上架)须人工复评，改 high 并走负责人批准。"
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/grounding_check.py
  runtime: python3
  call_pattern: args
input_schema:
  claims:
    type: string
    description: "claims"
    required: true
  sources:
    type: string
    description: "sources"
    required: true
output_schema:
  stdout: 结构化 JSON IR（含 result / rc / error_code / warnings）
  exit_code: rc=0 正常 / rc=1 告警或从严推定 / rc=2 输入不足或非法
capabilities:
  - rag
  - grounding
  - verification
permissions:
  network: true
  filesystem: true
  subprocess: false
  scope: project-dir-only   # 只处理调用者指定目录；外发需人逐次确认，无预设接收端
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.1.1: Bilingual rewrite (full EN+ZH, English first); 1.0.0: initial upload (USK v3)"
---

> 凡自治之物 · LGD 治理学 · 创造术家族 ｜ 评测协议：skill-quality-gate

## English

### When to use
- When users question the truthfulness of RAG answers, or the input contains suspected hallucination keywords such as "fabricated" or "nonsense".
- When concrete conclusions drawn from retrieval results must be fact-checked, in line with the LGD registered/evidenced principles.
- In high-risk decision scenarios or when producing traceable reports, answers must carry supporting source citations.

### Usage
Call the core script `grounding_check.py` and specify the check target and sources via command-line arguments:
```bash
python grounding_check.py --target <claim-to-check> --source <retrieval-store ID or URL> --mode lgd_grounding
```
- `--target`: the specific factual statement or answer segment to verify.
- `--source`: the retrieved knowledge index, URL or related context data.
- `--mode`: validation mode; `lgd_grounding` recommended (LGD Three-Law grounding).

### Workflow
1. Extract the key factual claims from the current RAG answer into a list of statements to check.
2. Semantically match claims against retrieved sources and compute the grounding coverage.
3. Run `grounding_check.py` to produce the internal verification result per LGD rules.
4. The script flags unsupported claims as high risk, warning "hallucination risk" in red.
5. The system automatically requires unsupported conclusions to carry source links, ensuring every answer is traceable.
6. Aggregate the analysis into a final credibility assessment with evidence-based correction suggestions.

### Evidence & safety statement
- Evidence: TBD (no evaluation / badge link yet; update here once produced)
- Version: 1.1.1
- Safety: no independent security scan has been performed (TBD); the conclusion is pending and no endorsement is given until it is completed.

## 中文

### 何时用
- 当用户质疑 RAG 回答内容的真实性，或输入包含“编造”、“胡说八道”等疑似幻觉关键词时。
- 需要对检索结果中的具体结论进行事实核验，确保符合 LGD 三律之“有籍”与“有证”。
- 在涉及高风险决策或需要生成可追溯报告的场景中，要求答案附带出处链接支撑。

### 用法
调用核心脚本文件 `grounding_check.py`，通过命令行参数指定校验对象与来源：
```bash
python grounding_check.py --target <待校验的文本声明> --source <检索库 ID 或 URL> --mode lgd_grounding
```
- `--target`: 输入需要核查的具体事实陈述或回答片段。
- `--source`: 提供检索到的知识文档索引、URL 或相关上下文数据。
- `--mode`: 指定验证模式，推荐使用 `lgd_grounding`（LGD 三律 grounding）。

### 流程
1. 提取当前 RAG 回答中的关键事实声明，形成待校验文本列表。
2. 将待校验声明与检索来源进行语义匹配，计算接地覆盖率（Grounding Coverage）。
3. 执行 `grounding_check.py` 脚本，依据 LGD 三律规则生成内部校验结果。
4. 脚本输出中标记未覆盖的声明为高风险，并以红色文本警示“幻觉风险”。
5. 系统自动要求未支撑结论附带来源链接，确保每一条回答“有籍可查”。
6. 汇总分析结果，输出最终的可信度评估报告及基于证据的修正建议。

### 证据与安全声明

- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.1.1
- 安全：未做独立安全扫描（TBD），结论待补；补全前不作推荐背书。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/rag-grounding-guard
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/rag-grounding-guard/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。

---

## Data handling / 数据处理边界

- 默认不向任何外部地址发送数据：扫描结果、报告、命中明细一律只写本地或只打印到当前会话。
- 如需外发（告警、工单、邮件、IM），必须由人先明确指定接收方，并在每次发送前逐次确认；本技能不预设、也不硬编码任何接收端。
- 只处理调用者明确指定的目标路径，不遍历无关目录，不跟随符号链接，不读取目标之外的凭据文件。
- 命中内容在输出时按需脱敏，避免把敏感原值写进日志或对话记录。
