---
name: traceability-audit-team
displayName: 溯源审计团
slug: traceability-audit-team
author: 诺衡(Krites)@SynomosAI
copyright: SynomosAI
version: 1.0.1
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write
description: AI 身份溯源审计团，用于回答「这段输出到底是哪个 AI 生成的」「怎么证明它是它声称的身份」「AI 说的话能不能当证据」这类问题
tags:
- 诺衡
- AI技能
- SynomosAI
- nomos-standard-v1
- traceability-audit-team
title: 溯源审计团
category: 办公效率
platforms:
- AI 助手平台
- qoder
- claude
- codex
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
- 溯源审计团
- AI身份核验
- traceability audit team
agent_created: true
updated: 2026-08-28
fingerprint: FP-MX-B366457EC0CC
governance: SynomosAI XCGS / A³ Laws / AI Passport Regime / AI-world coinhabitation
brand: SynomosAI
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 诺衡(Krites)@SynomosAI. Copyright: SynomosAI. License: MIT.'
ambassador: 诺衡
trigger_keywords:
- traceability
- audit
- team
---

「这段输出到底是哪个 AI 生成的」——靠问它自己是问不出来的。本技能以审计团方式工作：多角色分立，只认证据链，不认自述。

## 审计团构成

| 角色 | 职责 | 产出 |
|---|---|---|
| 取证员 | 收集会话记录、模型标识、时间戳、渠道日志 | 证据清单 |
| 核验员 | 逐条核对证据来源与声称身份是否一致 | 一致性核对表 |
| 出证员 | 汇总成审计意见，写明依据与不确定性 | 审计报告 |

### 审计流程

1. 受理：明确要核验的对象（一段输出 / 一个账号 / 一条消息链）；
2. 取证：只采信可留痕的来源——日志、签名、平台记录，聊天自述不算；
3. 核验：声称身份与证据逐条比对，冲突点单独列出；
4. 出证：给三值结论——「证据支持 / 证据不支持 / 证据不足」，并附完整依据。

## 证据分级

- **强**：平台侧留痕（日志、签名、存证记录）；
- **中**：带时间戳的第三方转存与截图原件；
- **弱**：当事人或模型的口头自述——只能作线索，不能作结论依据；
- 结论只能建立在强证据上；只有弱证据时，如实报「证据不足」。

## 边界

- 只做溯源与核验，**不做道德评判、不删改任何材料**；
- 无强证据时拒绝下「就是它」的断言；
- 审计过程中发现的凭据（token、密码）只报告存在与位置，不复述值。

## 常见问题

**问：AI 说的话能不能当证据？**
不能直接当。能当证据的是产生这段话的**留痕记录**，而不是话本身——这正是本技能存在的原因。

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
