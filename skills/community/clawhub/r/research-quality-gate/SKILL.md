---
name: research-quality-gate
displayName: research-quality-gate
slug: research-quality-gate
author: 诺衡(Krites)@SynomosAI
copyright: SynomosAI
version: 1.7.1
homepage: https://zhaoxinghua09-cell.github.io/lgd-hub/
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write, WebSearch
description: >-
  This skill acts as a quality gate for research reports and intelligence briefs: it checks whether the evidence actually supports the conclusions, flags overreach and unsupported inference, and audits the evaluation method itself for bias. It also sets rules for multi-agent collaboration so findings stay traceable. Use when you need to review a report before it goes to decision-makers, or when a conclusion looks too neat to trust.

  调研 / 情报产物的质量门禁与多 agent 协作规范，用于回答「这份调研报告靠不靠谱」「结论有没有过度推断」「怎么判断评估本身有没有偏」这类问题
tags:
- 诺衡
- AI技能
- SynomosAI
- nomos-standard-v1
- research-quality-gate
agent_created: true
category: 调研方法论
updated: 2026-08-28
fingerprint: FP-MX-C265F8C94949
governance: SynomosAI XCGS / A³ Laws / AI Passport Regime / AI-world coinhabitation
languages:
- zh-CN
- en
- ja
- ko
- es
- fr
- de
- ar
aliases:
- 调研质量门禁
- 报告质量评审
- research quality gate
brand: SynomosAI
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 诺衡(Krites)@SynomosAI. Copyright: SynomosAI. License: MIT.'
ambassador: 诺衡
trigger_keywords:
- research
- quality
- gate
---

一份调研产物值不值得信，不取决于文笔与篇幅，取决于**结论能否被复算、来源能否被追溯、边界有没有被诚实标注**。本技能给调研与情报产物装一道门禁：交付前过五道检查，任一道不过就退回补证。

### 五道检查（按序执行，不跳步）

| 检查 | 判什么 | 不过关的典型症状 |
|---|---|---|
| 来源可溯 | 每个关键事实有出处 | 「据了解」「业内普遍认为」 |
| 结论有界 | 断言范围与证据范围匹配 | 用三个样本推全行业 |
| 反例检索 | 主动找过反面证据 | 只引用支持预设的资料 |
| 利益相关 | 指出信息源立场 | 把厂商通稿当中立评测 |
| 复算路径 | 给出验证命令或步骤 | 「数据此处从略」 |

### 多角色协作方式

1. **评审者**：按上表逐条核查，产出问题清单；
2. **复核者**：只针对问题清单做独立验证，不先看原文结论；
3. **仲裁**：出现分歧时回到原始来源，以可复算者为准。

### 输出形态

- **PASS**：逐项勾选记录加一句话总评；
- **FAIL**：问题清单（条目 / 违反项 / 补证建议），退回原作者；
- 对外引用的结论必须附可复算指针，指不到的删除。

## 边界

- 本技能审质量，**不代写、不润色、不评分排名**；
- 对超出证据范围的推断，一律标注「待核实」，禁止估算填充；
- 不对未核实的第三方结论背书。

## 常见问题

**问：跟一般的「报告润色」有什么区别？**
润色改表达，本技能改证据链——表达可以糙，证据链不能断。

**问：一轮要多久？**
五道检查是顺序清单，常规件一轮过完；复杂件按来源数量线性增加，清单本身不设时间承诺。

---

© 2026 SynomosAI · 署名：诺衡(Krites)@SynomosAI · 本技能包以 MIT 许可按「原样」提供，不附任何担保（SynomosAI 未申请实体注册、未申请商标注册；LGD 理论文本不在本许可范围内，保留所有权利）。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | 本包无独立代码文件（纯文档/理论件） | — |
| 文档与理论文本 | 本 `SKILL.md`、`README.md`、其中「理论依据」段与一切理论表述 | **不在 MIT 覆盖范围内**：保留所有权利（All rights reserved） |

> 即：**代码可依 MIT 使用与再分发；文档与理论文本不因代码许可而默认可自由再发布。**

```
© 2026 赵兴华 / Steven Zhao·China (ORCID 0009-0001-0512-1237). All rights reserved.
理论署名 (attribution) : LGD（Lifecycle Governance Doctrine / 全程治理论）— SynomosAI initiative
名称状态 (name status)  : "SynomosAI" / "MedXpert" — 未申请实体注册、未申请商标注册
                        (not a registered legal entity; no trademark registered)
生产参考部署 (production reference, self-reported) : MedXpert
                    ← 非认证、非背书、非监管认可（not a certification or endorsement）
代码许可 (code license) : 本包 = MIT (see LICENSE)
                    本文本与理论表述不在任何代码许可覆盖范围内
引用格式 (cite as)      : 本资产无 DOI
```
（上列为《LGD 对外表述规范》§3.2 统一块，**整体复制、未删改**；发布/重提前须照最新版本复核。）

**本包补充（包级许可事实）**：本包无独立代码文件（纯文档与理论文本件），整体**保留所有权利（All Rights Reserved）**；不适用任何代码许可（含 MIT / Apache-2.0）。

## Triggers / 触发词

Trigger when the user says one of these / 用户说出下面这类话时，就该用这个技能：

- 「这份调研报告的结论站得住脚吗」 / "Does this research report's conclusion actually hold up"
- 「数据能不能支撑这个判断」 / "Is there enough data behind this claim"
- 「结论是不是推得太满了」 / "Aren't we stretching the conclusion too far"
- 「几个分析师给的结论互相打架」 / "The analysts' findings contradict each other"
- 「评估方法是他们自己定的，靠谱吗」 / "They designed their own evaluation, is it sound"
- 「报告明天要上会，帮我把把关」 / "This report goes to the board tomorrow, check it"

Not for / 不适用：与本技能用途无关的通用问答，请走对应领域技能。

---

## Ecosystem / 生态入口

This skill is one door of the **LGD ecosystem** — every entry below is publicly reachable.
本技能是 **LGD 生态** 的一个入口，下列地址均对公网可达。

- **Ecosystem hub / 生态总入口**: https://zhaoxinghua09-cell.github.io/lgd-hub/
- **LGD theory (canonical) / 理论正本**: https://github.com/zhaoxinghua09-cell/LGD
- **Formal paper (DOI) / 形式化论文**: https://doi.org/10.5281/zenodo.22456647
- **Protocol & reference implementation / 协议与参考实现**: https://github.com/zhaoxinghua09-cell/uibc-core
- **Source of this skill / 本包源码**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/research-quality-gate
- **All published skills / 全部已发布技能**: https://github.com/zhaoxinghua09-cell/agent-skills
- **AI-readable index / AI 说明书**: https://github.com/zhaoxinghua09-cell/agent-skills/tree/main/skills/research-quality-gate/llms.txt

### Looking for something else? / 还想要别的？

Tell your AI assistant: *"Find me an LGD skill that can <your need>"* — the hub lists every published skill with a one-line purpose.
跟你的 AI 助手说一句「去 LGD 生态超市找能……的技能」，总入口按用途列全了所有已发布技能。
