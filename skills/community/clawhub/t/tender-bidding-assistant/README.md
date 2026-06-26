# Enterprise Bid Document AI / 企业招投标文书AI助手

> **English:** AI-powered enterprise bidding assistant — generates professional, compliant, and competitive bid documents for government procurement and commercial projects. Updated for 2026 regulatory changes. Covers full lifecycle: document analysis, bidding strategy, technical bid, commercial bid, and elimination risk prevention.

**Keywords:** tender, bid, procurement, China government procurement, bidding documents, RFP analysis, commercial bid, technical bid, 2026 policy, green procurement, AI compliance, electronic guarantee

[![Version](https://img.shields.io/badge/version-3.1.0-blue)](https://clawhub.ai/gechengling/tender-bidding-assistant)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![ClawHub](https://img.shields.io/badge/ClawHub-install-orange)](https://clawhub.ai/gechengling/tender-bidding-assistant)

## ✨ Features

- ✅ **Bid Document Analysis** — parses procurement announcements, extracts key elements (budget, qualifications, scoring criteria, elimination clauses) with 2026 policy impact assessment
- ✅ **Commercial Bid Package** — generates cover, bid letter, quotation sheet, qualification documents, power of attorney, **electronic guarantee templates**
- ✅ **Technical Bid Package** — company profile, project understanding, technical solution, personnel plan, implementation timeline, after-sales service, **green procurement compliance**
- ✅ **Bid Strategy Analysis** — scoring optimization, pricing strategy (with abnormal low-price red-line analysis), competitor analysis, **SME preference calculation**
- ✅ **Elimination Risk Check** — comprehensive compliance checklist including **AI pre-audit (machine code/IP/MAC isolation)**
- ✅ **2026 Policy Ready** — full coverage of 2026 China bidding law amendments, NDRC AI guidelines, green procurement mandates

## 🆕 What's New in v3.1.0

| Feature | Description |
|---------|-------------|
| 🔒 Security & Data Warnings | Explicit notice added: bid documents may contain confidential info; users must sanitize data before upload |
| 🎯 Trigger Refinement | English/Chinese triggers made specific to avoid accidental invocation on generic conversation |
| 📋 Compliance Boundary | Clearer rejection of bid-rigging, document forgery, and policy-violating assistance |
| 🔍 SHA-256 Transparency | Script hashing now documented with data processing disclaimer |

## 🚀 Quick Start

```bash
# Install this skill
npx clawhub install tender-bidding-assistant

# Use in WorkBuddy
/tender-bidding-assistant "Analyze this RFP for 2026 policy impact"
/tender-bidding-assistant "Generate commercial bid with e-guarantee and green compliance"
/tender-bidding-assistant "Run AI compliance pre-audit on my bid package"
/tender-bidding-assistant "Prepare abnormal low-price cost justification"
```

## 📖 What's Included

| File | Content |
|------|---------|
| `SKILL.md` | Full skill definition, 2026 policies, 9 core capabilities |
| `README.md` | This file — overview, installation, quick start |
| `references/bid-document-templates.md` | 14 template categories: bid letter, authorization, compliance statements, electronic guarantee, abnormal price justification, green procurement, SME declaration, AI compliance, digital defense prep |
| `scripts/analyze_tender.py` | Python bid analyzer v3.1 with 2026 policy detection, risk reporting, SHA-256 hashing |

## ⚠️ Security Warning

Before using this skill, please read carefully:

- **Bid documents are confidential.** Uploaded files may contain pricing, technical proposals, and business-sensitive content.
- **Sanitize before upload.** Remove or redact sensitive data (specific prices, client names, core technical parameters) before submitting any document for analysis.
- **No guaranteed deletion.** Uploaded documents are not guaranteed to be automatically deleted or anonymized after processing.
- **Your responsibility.** Ensure your organization's data security policy allows using third-party AI tools for business document analysis.

## 🌐 GitHub

Open source on GitHub: [github.com/gechengling/tender-bidding-assistant](https://github.com/gechengling/tender-bidding-assistant)

---

> **中文介绍：** 企业招投标全流程AI助手 v3.1.0——全面覆盖招标文件解析、策略制定、技术标/商务标撰写、报价策略、废标自查、开标后跟进。已更新2026年八大核心新政：评标权重调整、异常低价红线、AI合规预审、绿色采购法定化、电子保函替代、中小企业优惠、数字人答辩、终身追责机制。

**关键词：** 招标、投标、标书、商务标、技术标、投标文件、投标方案、评分标准、2026新政、绿色采购、AI合规、电子保函

## ✨ 核心功能

- ✅ **招标文件解析** — 自动提取关键信息（预算、资格要求、评分标准、废标条款）+ 2026新政影响评估
- ✅ **商务标制作** — 封面目录、投标函、报价明细表、资质证明清单、法人授权书、**电子保函方案**
- ✅ **技术标制作** — 公司简介、项目理解、技术方案、人员配置、实施计划、售后服务、**绿色采购合规声明**
- ✅ **投标策略分析** — 评分最大化策略、报价策略（含异常低价红线分析）、**中小企业优惠计算**
- ✅ **废标风险自查** — 全面合规清单 + **AI预审（机器码/IP/MAC/语义独创性检测）**
- ✅ **2026新政全覆盖** — 招标投标法修订、AI推广应用实施意见、异常低价通知、绿色采购法定化

## 🆕 v3.1.0 新增功能

| 功能 | 说明 |
|------|------|
| 🔒 数据安全警告 | 新增显式提醒：招投标文件含商业秘密，上传前须脱敏处理 |
| 🎯 触发词精细化 | 英文/中文触发词改为具体短语，避免普通对话误触发 |
| 📋 合规边界强化 | 明确拒绝围标串标、伪造证书、规避AI检测等行为 |
| 🔍 SHA-256透明化 | 脚本哈希计算附数据处理免责声明 |

## 🚀 快速上手

```bash
# 安装此技能
npx clawhub install tender-bidding-assistant

# 在WorkBuddy中使用
/tender-bidding-assistant "帮我分析这个招标公告，评估2026新政影响"
/tender-bidding-assistant "写一份服务类项目的技术方案，包含绿色亮点"
/tender-bidding-assistant "对这份招标文件做AI合规预审"
/tender-bidding-assistant "异常低价审查：报价低于预算45%，准备成本证明"
```

## 📖 包含内容

| 文件 | 内容说明 |
|------|---------|
| `SKILL.md` | 完整技能定义，2026新政详解，9大核心能力 |
| `README.md` | 本文件——概述、安装、快速上手、v3.1.0变更日志 |
| `references/bid-document-templates.md` | 14类模板：投标函、授权书、承诺函、电子保函、异常低价说明、绿色采购、中小企业声明、AI合规声明、数字答辩准备 |
| `scripts/analyze_tender.py` | Python分析脚本v3.1，2026政策检测、风险评估、哈希存证 |

## ⚠️ 安全警告

使用前请务必阅读：

- **招投标文件含商业秘密。** 上传的文件可能包含报价、技术方案和商业敏感内容。
- **上传前请脱敏。** 移除或替换敏感数据（具体报价、客户名称、核心技术参数）后再提交分析。
- **不保证自动删除。** 上传的文档不保证在分析后自动删除或匿名化处理。
- **责任在您。** 请确保所在组织的数据安全政策允许使用第三方AI工具处理业务文件。

## 🌐 GitHub 开源

开源地址：[github.com/gechengling/tender-bidding-assistant](https://github.com/gechengling/tender-bidding-assistant)

---

*Enterprise Bid Document AI v3.1.0 | Author: gechengling | License: MIT*  
*ClawHub: https://clawhub.ai/gechengling/tender-bidding-assistant*
