---
name: wechat-qa-checklist
displayName: wechat-qa-checklist
slug: wechat-qa-checklist
author: 诺衡(Krites)@SynomosAI
copyright: SynomosAI
version: 1.0.1
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep
description: 微信公众号文章推送前的强制自检清单，用于回答「推之前还要查什么」「上次那个坑别再踩」这类问题
tags:
- 诺衡
- AI技能
- SynomosAI
- nomos-standard-v1
- wechat-qa-checklist
metadata:
  openclaw:
    emoji: 📋
agent_created: true
disable-model-invocation: true
category: 内容创作
updated: 2026-08-28
fingerprint: FP-MX-94467824703E
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
- 公众号自检清单
- 推送前检查
- WeChat QA checklist
brand: SynomosAI
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 诺衡(Krites)@SynomosAI. Copyright: SynomosAI. License: MIT.'
ambassador: 诺衡
trigger_keywords:
- wechat
- qa
- checklist
---

推送前自检不是走过场：发出去的文章改不了，所以检查全部前置。本技能是一张强制清单——十项逐条过，任何一项不过就不推。

## 推送前十查

- **事实**：文中数字、日期、引用与来源核对过吗？
- **链接**：每个链接点过一遍吗？跳转目标是预期的吗？
- **错别字**：通读一遍了吗？（机器查 + 人读各一遍）
- **标题**：标题与内容一致吗？有没有标题党欺诈？
- **图片**：都加载正常吗？版权来源清楚吗？
- **权属**：署名、来源标注、转载授权在位吗？
- **敏感词**：平台规则词、行业敏感表述扫过吗？
- **排版**：手机端预览过吗？样式没崩吧？
- **合规**：有没有绝对化用语、无法兑现的承诺？
- **留档**：定稿与素材归档了吗？

### 一票否决项

下面任何一条命中，无论多急都不推：

- 事实错误或无法溯源的关键数据；
- 缺失权属与来源标注的转载内容；
- 绝对化用语（最、第一、百分之百有效等无依据表述）。

## 查出问题怎么处置

1. 记录：问题项 + 位置 + 建议改法；
2. 修正后**重跑全清单**——改一处常碰坏另一处；
3. 连续两轮仍有否决项，说明稿子没成熟，退回写作环节。

## 常见问题

**问：改一个错别字也要跑全清单吗？**
改动范围小可以只跑受影响项（比如改正文错字不影响链接与图片），但凡动了事实与数据，十项全跑。

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
