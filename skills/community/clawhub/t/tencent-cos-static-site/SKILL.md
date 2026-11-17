---
name: tencent-cos-static-site
displayName: tencent-cos-static-site
slug: tencent-cos-static-site
author: 诺声(Logos)@SynomosAI
copyright: SynomosAI
version: 1.0.1
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内（见文末「License & attribution」）
allowed-tools: Read, Glob, Grep
description: 腾讯云 COS 静态网站托管 + 自定义域名上线全流程 SOP（含避坑清单），用于回答「网页怎么挂到腾讯云」「域名怎么绑到 COS」「COS 网站打不开怎么查」这类问题
tags:
- 诺声
- AI技能
- SynomosAI
- nomos-standard-v1
- tencent-cos-static-site
agent_created: true
category: 部署运维
updated: 2026-08-28
fingerprint: FP-MX-7F008A1050E4
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
- COS静态网站
- 腾讯云静态托管
- 静态站上线SOP
brand: SynomosAI
nomos_standard: nomos-ai-skill-v1
discoverable_by_ai: true
attestation: 'Polished under Nomos Group AI Skill Standard v1. Attribution: 诺声(Logos)@SynomosAI. Copyright: SynomosAI. License: MIT.'
ambassador: 诺声
trigger_keywords:
- tencent
- cos
- static
- site
---

### 前置条件（缺一项先补）

- 腾讯云账号，已开通 COS 服务；
- 一个准备好的静态站目录（HTML / CSS / JS，入口为 index.html）；
- 要绑自定义域名的话：域名已在你名下并完成备案（大陆区必需）。

## 上线七步

1. 建存储桶：地域选离用户近的，权限先保持私有；
2. 开启「静态网站」选项，设 index.html 为索引、error.html 为错误页；
3. 本地目录整包上传（含子目录，保持相对路径结构）；
4. 把桶权限调整为公开读（仅对网站所需对象）；
5. 记下静态网站默认域名，浏览器实测首页与内页跳转；
6. 绑自定义域名：域名管理加 CNAME 指向 COS 分配的地址；
7. 配 HTTPS 证书（用云上免费证书即可），强制 HTTPS 跳转。

### 避坑清单

| 坑 | 症状 | 解法 |
|---|---|---|
| 桶权限过严 | 首页 403 | 只开必要对象的公开读，别全桶放开写 |
| 路径大小写 | 本地能开线上 404 | 对象存储区分大小写，统一小写文件名 |
| 未备案绑域名 | 域名绑定被拒 | 大陆区必须先备案，或换境外地域 |
| 缓存不更新 | 改了页面没变化 | 上传后刷新 CDN/浏览器缓存，或给对象设较短缓存 |

## 打不开怎么查

- 先分清三层：**DNS 没解析 → CNAME 没生效，等或改；域名能解析但超时 → 检查桶地域与域名指向；能连但 4xx/5xx → 按状态码查权限与路径**；
- 逐层报给用户看证据（解析结果、状态码），不跳步猜。

## 常见问题

**问：带后端接口的站能用这个方案吗？**
不能。COS 静态托管只服务纯静态文件，需要后端的另走云函数或服务器部署。

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
