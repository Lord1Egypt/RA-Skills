---
name: unified-task-ledger
displayName: unified-task-ledger
slug: unified-task-ledger
author: 诺声(Logos)@SynomosAI
copyright: SynomosAI
version: 1.0.1
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Task
description: 统一任务账本，用于回答「派出去的任务现在什么状态」「批量派单怎么统一收口」这类问题
tags:
- 诺声
- AI技能
- SynomosAI
- nomos-standard-v1
- unified-task-ledger
agent_created: true
category: 任务管理
updated: 2026-08-28
fingerprint: FP-MX-062DFAD0BBC6
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
- 统一任务账本
- 双通道派单
- task ledger
brand: SynomosAI
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 诺声(Logos)@SynomosAI. Copyright: SynomosAI. License: MIT.'
ambassador: 诺声
trigger_keywords:
- unified
- task
- ledger
---

派出去的任务各有各的下场：有的完成没人验收，有的卡住没人知道，有的派了两次。统一任务账本只做一件事：**所有任务进同一本账，状态可查、去向可追、收口有人认**。

### 账本四字段

| 字段 | 内容 | 缺了会怎样 |
|---|---|---|
| 单号 | 唯一编号，追加不改 | 重派、漏派无从对账 |
| 单据 | 派什么：目标 + 验收判据 | 「做完了」与「做好了」扯皮 |
| 归属 | 谁接的单，owner 唯一 | 无主任务永远沉底 |
| 状态 | 待接 / 进行中 / 待验收 / 关闭 | 批量派单后没法统一收口 |

### 派单收口流程

1. 开单：四字段填齐才允许入账——没 owner 的单当场打回；
2. 认领：owner 显式接单，账本记接单时间；
3. 升级：owner 扛不动时按升级链上报，账本记录「试过什么、为何不行」；
4. 收口：验收判据满足才允许关闭；关闭时附产出物位置，账不记虚功。

## 纪律

- **一单一账**：同一件事不在两个渠道各记一本；
- 追加式：状态变化记新条目，不改历史——对账靠流水不靠记忆；
- 账实一致：账上说进行中，实际已停的，发现即修正并注明原因。

## 常见问题

**问：任务只有一句话，也要走四字段吗？**
轻量单可以一句话入账，但单号和归属两个字段不许省——这两项缺了，收口必然出问题。

---

© 2026 SynomosAI · 署名：诺声(Logos)@SynomosAI · 本技能包以 MIT 许可按「原样」提供，不附任何担保（SynomosAI 未申请实体注册、未申请商标注册；LGD 理论文本不在本许可范围内，保留所有权利）。

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
