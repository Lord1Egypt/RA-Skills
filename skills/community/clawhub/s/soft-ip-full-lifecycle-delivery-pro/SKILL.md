---
name: "soft-ip-full-lifecycle-delivery-pro"
version: "1.3.1"
description: >
  Software copyright registration document drafting: AI generates all 8 application documents (application form, source code documentation, user manual, rights declaration, etc.) in conversation after clawtip payment verification. No source code, applicant info, or filing documents are uploaded.
metadata:
  author: "Yujin"
  category: "expert"
  permissions:
    - "credential.read"
    - "filesystem.read"
    - "filesystem.write"
  requires:
    - "clawtip"
  workflow:
    create_order:
      script: scripts/create_order.py
      args: ["{question}"]
      outputs: ["order_no", "amount", "indicator"]
    pay:
      requires: clawtip
      args: ["{order_no}", "{indicator}"]
    service:
      script: scripts/service.py
      args: ["{order_no}"]
---

# soft-ip-full-lifecycle-delivery-pro

## 技能概述

软件著作权申报材料全流程生成服务。本技能通过 clawtip 完成支付验证后，**由 AI 模型在对话中**逐份起草全部 8 项申报材料，用户只需描述软件功能即可。

### 服务交付方式

本技能是 **AI 对话交付型** 服务：
- `create_order.py` — 创建本地订单文件（仅用于 clawtip 支付验证）
- 支付由 **clawtip** 官方钱包处理
- `service.py` — 验证支付凭证后，指示 AI 在对话中输出完整申报材料草稿
- 实际的文档起草由 AI 模型在对话上下文中完成，不依赖外部脚本或模板库

### 8 项交付文档

| # | 文档 | 说明 |
|---|------|------|
| 1 | 软件著作权登记申请表 | 软件名称、版本号、分类号等标准化填写 |
| 2 | 软件说明书 | 功能描述、技术特点、运行环境 |
| 3 | 用户操作手册 | 安装指南、操作流程、界面说明 |
| 4 | 源程序代码文档 - 前30页 | 核心功能模块代码摘录 |
| 5 | 源程序代码文档 - 后30页 | 补充代码及关键算法 |
| 6 | 文档材料目录 | 全部提交文件的索引 |
| 7 | 权利归属证明 | 开发方声明、合作框架协议模板 |
| 8 | 申请材料汇总表 | 跨文档一致性检查清单 |

### 建议流程

1. 先使用 **soft-ip-full-lifecycle-zijian** 做材料合规性诊断
2. 材料补充完整后，使用本技能交付正式文档

---

## 环境变量配置

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `CLAWTIP_PAY_TO` | 是 | clawtip 商户收款地址（仅用于支付验证） |
| `CLAWTIP_SM4_KEY` | 是 | SM4 加密密钥（仅用于支付凭证加密） |

---

## 前置条件

```bash
openclaw skills install clawtip
```

---

## 🛒 第一阶段：创建订单

```bash
python3 scripts/create_order.py "<软件功能描述>"
```

> 本地订单文件路径：`~/.openclaw/skills/orders/{indicator}/{order_no}.json`
> 包含字段：orderNo、amount、question。仅用于支付验证。**不含任何申报材料或源代码。**

**成功：** `ORDER_NO=... AMOUNT=... QUESTION=... INDICATOR=...`
**失败：** `订单创建失败: <详情>` → 终止。

---

## 💳 第二阶段：支付处理

### 沙箱测试

```bash
npx --yes @clawtip/clawtip-sandbox-cli@1.0.0 pay -o <ORDER_NO> -i <INDICATOR> -v 1.0.12
```

### 生产环境

调用 **clawtip** 钱包：`{"orderNo": "<ORDER_NO>", "indicator": "<INDICATOR>"}`

---

## 🚀 第三阶段：文档生成

```bash
python3 scripts/service.py "<order_no>"
```

成功后，AI 模型将在对话中逐份输出全部 8 项申报材料的可编辑草稿。

---

## 数据处理说明

### 本地存储
| 文件 | 路径 | 内容 |
|------|------|------|
| 订单文件 | `~/.openclaw/skills/orders/{indicator}/{order_no}.json` | orderNo、amount、question、加密凭证 |

订单文件仅用于 clawtip 支付验证，不含任何申报材料。

### 远程传输
本技能自身不发起任何远程 HTTP 请求。支付验证由 clawtip 官方钱包处理。

### 绝不收集或传输
源代码、申报文档、著作权人信息、公司信息或商业秘密。

---

## 版本历史

| Version | Date | Notes |
|:--------|:-----|:------|
| 1.3.1 | 2026-07-28 | Fix SkillSpector findings: inline file_utils and SM4; document delivery specification in service.py |
| 1.3.23 | 2026-07-28 | Previous upload |
| 1.1.0 | 2026-07-20 | Restructured SKILL.md |
| 1.0.1 | 2026-07-20 | Fix payment flow |
