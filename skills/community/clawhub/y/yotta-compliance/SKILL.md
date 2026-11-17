---
name: yotta-compliance
slug: yotta-compliance
version: 0.1.3
displayName: 合规条款审查·元规
summary: 本地、确定性的合规条款审查：规则包版本化，每条结论给出原文证据、命中规则与框架覆盖级别；零依赖，不构成法律意见。
description: '合规条款审查（元规）—— 对文本 / Markdown 做确定性合规条款审查：内置 PIPL 与数据出境基础规则包，逐条给出原文位置、命中规则、框架覆盖级别与来源条款；支持 Markdown / JSON 报告与 CI 闸门，零依赖本地运行，核心不联网、不调用模型，不构成法律意见。'
tags: [合规审查, 条款审查, 合同审查, 数据合规, 个人信息保护, PIPL, 数据出境, 证据链, 规则引擎, 离线, 隐私政策, compliance]
category: office-efficiency
license: MIT
homepage: https://github.com/YottaMeta/yotta-compliance
---
# 元规（yotta-compliance）

本地、确定性、可复算的合规条款审查技能。元规对文本或 Markdown 执行规则匹配、断言求值与证据抽取，
输出带**原文位置、命中规则、框架覆盖级别与来源条款**的审查报告。

可信契约：

- 每条风险结论必须回到原文证据、规则 id 和来源条款；
- 没有证据不输出风险结论；
- 同一输入得到同一结果（仅生成时间不同）；
- `mapping_only` 框架只做主题映射，不输出该框架的独立合规结论；
- 核心路径不调用 LLM、不联网，规则包只作为只读 JSON 数据。

## 何时使用

- 审查隐私政策、数据处理条款、个人信息处理规则等文本；
- 检查文本是否出现 PIPL 要求的告知、合法性依据、保存期限、单独同意、个人权利、影响评估等要素；
- 检查数据出境场景是否出现安全评估 / 标准合同 / 保护认证、单独同意、境外接收方告知、境内存储说明；
- 生成可复算的 Markdown / JSON 审查报告，作为人工复核的起点；
- 把达到指定严重度的条款缺口接入 CI 闸门。

**Do NOT trigger**：

- 不生成法律意见、不判断合同效力、不预测诉讼结果；
- 不替代律师、合规顾问或监管机构的判断；
- 不把 `mapping_only` 描述为“已审查该框架”；
- v0.1 不直接解析 PDF / docx，需先转成 UTF-8 文本或 Markdown；
- 不联网检索法条，不调用模型做语义裁决；
- 不自动修改合同或替用户签署、提交任何文件。

## 快速使用

Windows 使用 `python`，Linux / macOS 使用 `python3`。

```bash
# 审查一个文本 / Markdown 文件（默认装载 pipl + data-export）
python3 scripts/yotta_compliance.py review --input contract.md

# 只审查 PIPL 包
python3 scripts/yotta_compliance.py review --input contract.md --frameworks pipl

# 输出 JSON，并在达到 high 时返回退出码 1
python3 scripts/yotta_compliance.py review --input contract.md --format json --gate high --out report.json

# 从标准输入读取
python3 scripts/yotta_compliance.py review --stdin --frameworks pipl,data-export

# 规则包操作
python3 scripts/yotta_compliance.py rules list --framework pipl
python3 scripts/yotta_compliance.py rules show PIPL-NOTICE-001
python3 scripts/yotta_compliance.py rules validate --pack rules/pipl.json
```

报告默认写 stdout。只在显式提供 `--out` 时写文件，输出路径不得与输入文件相同，也不得写入规则包目录。

## 命令一览

| 命令 | 说明 |
|---|---|
| `review --input <file>` | 审查 UTF-8 `.txt` / `.md` / `.markdown` 文件 |
| `review --stdin` | 从标准输入读取文本 |
| `review --frameworks <list>` | 选择规则包，逗号分隔；缺省装载全部规则包 |
| `review --format md\|json` | 输出 Markdown（默认）或 JSON |
| `review --out <file>` | 写报告文件；缺省写 stdout |
| `review --gate <level>` | CI 闸门：`off` / `low` / `medium` / `high` / `critical` |
| `review --min-severity <level>` | 只输出达到该严重度的 finding；汇总计数仍保留全量 |
| `review --include-safe` | 在 JSON `summary.checked_rules` 与 Markdown 未覆盖范围中列出已检查未命中的规则 |
| `rules list` | 列出规则包与规则 |
| `rules show <rule_id>` | 查看单条规则的说明、建议、来源与测试用例 |
| `rules validate --pack <file>` | 校验规则包；不合规立即失败 |

## 退出码

| 退出码 | 含义 |
|---|---|
| 0 | 审查完成，未超过 gate |
| 1 | 审查完成，存在达到 gate 的 finding |
| 2 | 输入缺失、编码错误、路径不可用或超出输入上限 |
| 3 | 规则包缺失、schema 无效或重复 `rule_id` |
| 4 | CLI 用法错误 |

## 覆盖范围

当前正式规则包：

| 规则包 | 框架 | 覆盖级别 | 规则数 |
|---|---|---|---|
| `pipl` | PIPL | `baseline_review` | 11 |
| `data-export` | 数据出境 | `baseline_review` | 4 |

`GDPR` / `HIPAA` / `SOC2` / `PCI-DSS` / `ISO27001` / 等保 当前为 `mapping_only`：
只把基础规则映射到对应主题，不输出这些框架的独立合规结论。

完整规则清单、主题映射与明确未覆盖范围见 `references/coverage.md`。

## 报告包含什么

Markdown 报告固定包含七节：

1. 输入摘要（来源、大小、行数、SHA-256、规则包版本）；
2. 框架覆盖摘要（规则包、框架、覆盖级别、状态、规则数）；
3. 风险汇总；
4. 逐条发现（严重度、置信度、框架映射、原文证据、位置、规则说明、建议动作、规则来源）；
5. 未覆盖范围；
6. 人工复核清单；
7. 免责声明。

JSON 报告固定提供稳定机器契约：`schema_version` / `tool` / `tool_version` / `generated_at` /
`input` / `rule_packs` / `framework_coverage` / `summary` / `findings` / `review_items` / `disclaimer`。
字段语义与证据结构见 `references/report-format.md`。

示例（对一份缺少多项护栏的隐私说明运行默认规则包）：

```text
- 本次输出 11 条发现（全部 11 条）
- high：3 条
- medium：4 条
- low：4 条
- 已检查规则：15 条 ｜ 命中规则：13 条
```

实际结果取决于输入内容与所选规则包，示例数字不作为固定输出。

## 规则包与证据链

规则包是版本化 JSON 数据，包含 pack 元信息、条款类型词表、规则列表和可选的主题映射。
每条规则必须声明 `test_ids`，且正式规则在发布前必须配有正例、反例和边界例。

每条 finding 固定包含：

- `finding_id`、`rule_id`、`severity`、`confidence`；
- `framework_mapping`（基础框架与 `框架:mapping_only` 标签）；
- `evidence`（`matched_span` 带原文 quote 与起止行列；`document_scope` / `section_scope` 只给范围）；
- `rationale`、`remediation`、`source`。

规则编写、断言契约与验收要求见 `references/rule-authoring.md`。

## 已知局限（必须人工复核）

- **词形匹配，不是语义理解**：absence 规则只判断检索词是否出现；同义但词形不同的表述可能漏检。
- **文档级范围**：absence 的 `scope` 均为 `document`，任何位置出现检索词即视为已出现，不判断该表述是否适用于当前处理活动。
- **否定句不建模**：「不会对外提供」「未经同意不得处理」等否定表述仍会触发候选匹配，可能产生漏报。
- **只解析阿拉伯数字**：`保存期限：N年` 可解析；中文数字（如“三年”）不解析、不换算。
- **数据出境人数阈值未进入 v1**：需要单位感知的数值原语；相关阈值规则推迟到规则包 v2。
- **absence 类结论一律降低置信度**：medium / low 置信 finding 会进入人工复核清单，必须人工核验后才能采信。
- **不直接解析 PDF / docx**：请先用文档适配器转成 UTF-8 文本或 Markdown。

## 数据与安全边界

- 纯本地运行：不发送原文、证据或报告，不联网检索法条，不调用模型；
- 规则包是只读数据，不从规则正文执行代码；
- 输入上限 2 MiB；仅接受 UTF-8 文本；
- 除非显式设置 `--out`，报告只写 stdout；
- 输出路径不得与输入文件相同，也不得位于规则包目录内；
- 不缓存原文，不把合同内容写入日志。

## 使用范围与授权

- 只审查用户有权处理的文本；用户对输入来源与使用范围负责；
- 审查结果用于发现文本缺口并辅助人工复核，不构成法律意见；
- 不用于规避监管、伪造合规结论或对外声称“已通过某框架认证”；
- 引用规则来源时保留规则包中的条款号与链接，不凭记忆补写条款。

## 法律与红线

- 元规是**审查建议工具**，不是律师事务所、认证机构或监管机关；
- 规则命中只代表文本中出现了可观察现象，不代表真实业务未履行义务；
- 规则未命中不代表不存在风险；`mapping_only` 框架不得被解读为已完成合规审查；
- 使用本工具须遵守所在地法律法规与平台条款，最终判断由具备资质的专业人士作出。

## 家族协同

- **元信 yotta-verify**：规则包与技能发布前的确定性安全扫描；
- **元忆 yotta-memory**：仅在用户显式选择时保存报告摘要与规则包哈希，不自动保存合同原文；
- **元呈 yotta-present**：把审查结论呈现为报告或证据卡；
- **元安 yotta-security-audit**：审计规则包与文件读取面的安全风险；
- **元审 yotta-vetter**：自定义规则包安装前的来源与权限审查。

## 开发与校验

```bash
# 全量契约测试（技能目录内）
python3 scripts/test_yotta_compliance.py

# 规则包校验
python3 scripts/yotta_compliance.py rules validate --pack rules/pipl.json
python3 scripts/yotta_compliance.py rules validate --pack rules/data-export.json

# 语法检查
python3 -m py_compile scripts/yotta_compliance.py
```

## 参考文档

- `references/rule-authoring.md` — 规则包 schema、匹配原语、断言契约与规则验收；
- `references/report-format.md` — Markdown / JSON 报告契约、字段语义与退出码；
- `references/coverage.md` — 当前框架覆盖、规则清单、主题映射与明确未覆盖范围。

## 免责声明

本工具提供基于确定性规则的条款审查建议与证据链，不构成法律意见。
