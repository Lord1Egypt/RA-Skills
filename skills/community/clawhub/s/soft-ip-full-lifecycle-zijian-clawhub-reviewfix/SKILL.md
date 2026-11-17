---
name: "soft-ip-full-lifecycle-zijian"
version: "3.2.1"
description: >
  Software IP self-assessment: AI-delivered compliance review for Chinese software copyright applications. Performs material completeness check, source code documentation audit, user manual review, rights attribution verification, and registration readiness assessment. Payment verification via clawtip. Chinese-language service (中国软件著作权申报所需).
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

# soft-ip-full-lifecycle-zijian

**语言说明 / Language:** This skill is designed for Chinese software copyright compliance (中国软件著作权申报), and its user-facing interface is primarily in Chinese. Core metadata and technical documentation are in English for accessibility.

## 技能概述

软件知识产权全生命周期自检与合规审查服务。本技能通过 clawtip 完成支付验证后，**由 AI 模型在对话中**交付合规诊断和材料审查结果。

### 服务交付方式

本技能是 **AI 对话交付型** 服务：
- `create_order.py` — 创建本地订单文件（仅用于 clawtip 支付验证）
- 支付由 **clawtip** 官方钱包处理
- `service.py` — 验证支付凭证后，指示 AI 在对话中执行以下 5 项评估

### 5 项合规评估

| # | 评估项 | 说明 |
|---|--------|------|
| 1 | 材料完整性审查 | 对照软著登记要求逐项检查材料是否齐全 |
| 2 | 源代码文档审计 | 格式验证、页数检查、前/后30页完整性 |
| 3 | 用户手册合规检查 | 截图格式、功能描述完整性 |
| 4 | 权利归属验证 | 权属声明、合作协议框架检查 |
| 5 | 登记就绪评估 | 风险分级（阻塞性 / 建议性 / 参考性），修复建议 |

### 与 delivery-pro 的关系

| 维度 | zijian（本技能，诊断版） | delivery-pro（生成版） |
|------|------------------------|-----------------------|
| 用途 | 合规性诊断：识别缺失和问题 | 文档生成：填写全部 8 项申报材料 |
| 价格 | 190 UT (1.9 元) | 690 UT (6.9 元) |
| 输出 | 缺失清单 + 问题标注 + 风险评级 | 完整的可提交文档草稿 |
| 建议顺序 | 先运行：诊断问题，补充材料 | 后运行：基于完善的材料生成文档 |

---

## 环境变量配置

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `CLAWTIP_PAY_TO` | 是 | clawtip 商户收款地址 |
| `CLAWTIP_SM4_KEY` | 是 | SM4 加密密钥 |

> 以上环境变量仅用于 clawtip 支付凭证加密，不收集、不传输任何业务数据。

---

## 前置条件

```bash
openclaw skills install clawtip
```

---

## 🛒 第一阶段：创建订单

```bash
python3 scripts/create_order.py "<question>"
```

> 本地订单文件路径：`~/.openclaw/skills/orders/{indicator}/{order_no}.json`
> 包含字段：orderNo、amount、question。仅用于支付验证，不涉及任何审查材料。

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

## 🚀 第三阶段：合规审查

```bash
python3 scripts/service.py "<order_no>"
```

成功后，AI 模型将在对话中输出完整的合规评估报告。

---

## 数据处理说明

### 本地存储
| 文件 | 路径 | 内容 |
|------|------|------|
| 订单文件 | `~/.openclaw/skills/orders/{indicator}/{order_no}.json` | orderNo、amount、question、加密凭证 |

### 远程传输
本技能自身不发起任何远程 HTTP 请求。支付验证由 clawtip 官方钱包处理。

### 绝不收集或传输
源代码、申报文档、著作权人信息、公司信息或商业秘密。

---

## 版本历史

| Version | Date | Notes |
|:--------|:-----|:------|
| 3.2.1 | 2026-07-28 | Fix SkillSpector: inline file_utils/SM4; English error messages; service delivery spec; add permissions; justify Chinese locale |
| 3.2.0 | 2026-07-28 | Switch to official clawtip wallet |
| 3.1.34 | 2026-07-28 | Fix ClawHub audit |
| 3.1.33 | 2026-07-20 | Security review |
