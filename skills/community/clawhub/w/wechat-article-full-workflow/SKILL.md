---
name: wechat-article-full-workflow
displayName: wechat-article-full-workflow
slug: wechat-article-full-workflow
author: 诺声(Logos)@SynomosAI
copyright: SynomosAI
version: 1.0.1
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep, Write, WebSearch
description: 微信公众号文章全流程：选题 → 标题 → 写作 → 排版 → 配图 → QA 自检 → 推送草稿 → 知识库存档，用于回答「公众号文章从零怎么做完」「排版老出问题怎么办」这类问题
tags:
- 诺声
- AI技能
- SynomosAI
- nomos-standard-v1
- wechat-article-full-workflow
agent_created: true
disable-model-invocation: true
category: 内容创作
updated: 2026-08-28
fingerprint: FP-MX-C30A66A35D98
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
- 公众号全流程
- 公众号发文
- WeChat article workflow
brand: SynomosAI
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 诺声(Logos)@SynomosAI. Copyright: SynomosAI. License: MIT.'
ambassador: 诺声
trigger_keywords:
- wechat
- article
- full
- workflow
---

公众号文章做不完，多半卡在中途换流程。本技能把全流程钉成八步流水线，每步有明确产出物，走完一步再走下一步。

## 八步流水线

1. **选题**：定主题与读者画像，产出一句「这篇解决读者什么问题」；
2. **标题**：出 3 版候选（悬念 / 数字 / 直给），选定 1 版、留 2 版备换；
3. **写作**：按大纲成稿，首段 100 字内给出继续读的理由；
4. **排版**：统一字号、行距、段距与强调色，样式不超过三套；
5. **配图**：封面 1 张 + 正文图按节配，无合适图就不硬配；
6. **QA 自检**：跑推送前自检清单（错别字、链接、数据、敏感词、权属信息）；
7. **推送草稿**：进草稿箱并生成预览，**不直接群发**——发出动作由你确认；
8. **存档**：定稿与封面归入知识库，记录选题来源便于复盘。

### 每步产出对照

| 步骤 | 产出物 | 完成判据 |
|---|---|---|
| 选题 | 一句话定位 | 你点头 |
| 标题 | 3 选 1 | 你选定 |
| 写作 | 全文初稿 | 覆盖大纲全部节点 |
| 排版 | 样式统一的稿件 | 三种样式内 |
| 配图 | 图位清单 | 无空图位 |
| QA | 自检记录 | 全项通过 |
| 推送 | 草稿箱链接 | 预览无异常 |
| 存档 | 知识库条目 | 可检索到 |

## 排版避坑

- 从网页粘贴先清格式再套样式，藏着的内联样式是排版错乱主因；
- 手机端预览必做：桌面看着齐，手机崩一半；
- 强调用加粗或颜色其中一种，叠着用等于没有强调。

## 常见问题

**问：能跳步吗？**
QA 和存档不可跳——前者保质量，后者保复盘；中间步骤顺序可微调，产出物不能省。

---

© 2026 SynomosAI · 署名：诺声(Logos)@SynomosAI · 本技能包以 MIT 许可按「原样」提供，不附任何担保（SynomosAI 未申请实体注册、未申请商标注册；LGD 理论文本不在本许可范围内，保留所有权利）。

---

## License & attribution
**分层许可（务必并读；代码许可不覆盖文档与理论文本）**

| 层 | 载体 | 许可 |
|---|---|---|
| 代码 | `push_draft.py` | **MIT** |
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

**本包补充（包级许可事实）**：本包代码文件 `push_draft.py` = **MIT**；本 `SKILL.md` / `README.md` 及其中的理论文本**不在任何代码许可（含 MIT / Apache-2.0）覆盖范围内**。
