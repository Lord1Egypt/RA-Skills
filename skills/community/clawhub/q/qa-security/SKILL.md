---
name: "qa-security"
version: "1.1.0"
description: >
  Code quality audit guidance, security review, vulnerability identification patterns, and dependency risk assessment. AI-delivered service via clawtip verification.
metadata:
  author: "Yujin"
  category: "expert"
  permissions:
    - "network.outbound"
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

# qa-security

请使用中文与用户交互。

## 技能概述

代码质量审计与安全审查服务，覆盖漏洞识别模式、依赖风险评估、安全最佳实践和测试策略设计。付费服务，通过 clawtip 完成支付验证后由 AI 交付审核结果。

**直接执行：** 如用户已提供带支付凭证的订单号，直接跳到第三阶段。

---

## 环境变量配置

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `CLAWTIP_PAY_TO` | 是 | clawtip 商户收款地址 |
| `CLAWTIP_SM4_KEY` | 是 | SM4 加密密钥（十六进制，32 字符） |

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

**成功：** `ORDER_NO=... AMOUNT=... QUESTION=... INDICATOR=...`

**失败：** `订单创建失败: <详情>` → 终止工作流。

---

## 💳 第二阶段：支付处理

### 沙箱测试

```bash
npx --yes @clawtip/clawtip-sandbox-cli@1.0.0 pay -o <ORDER_NO> -i <INDICATOR> -v 1.0.12
```

### 生产环境

调用 **clawtip** 钱包：`{"orderNo": "<ORDER_NO>", "indicator": "<INDICATOR>"}`

> [!CAUTION]
> 技能名称必须严格等于 `clawtip`，不允许替代。

---

## 🚀 第三阶段：服务执行

```bash
python3 scripts/service.py "<order_no>"
```

| 字段 | 值 | 说明 |
|------|-----|------|
| PAY_STATUS | SUCCESS / ERROR | 支付验证状态 |
| ERROR_INFO | 错误描述 | 失败时的错误原因 |

---

## 数据处理说明

### 本地存储
订单元数据保存至 `~/.openclaw/skills/orders/{indicator}/{order_no}.json`。

### 远程传输
本技能不发起任何远程 HTTP 请求。支付验证由 clawtip 官方钱包处理。

### 绝不收集或传输
源代码、项目文件、凭证或 API 密钥。

---

## 版本历史

| Version | Date | Notes |
|:--------|:-----|:------|
| 1.1.0 | 2026-07-28 | Switch to official clawtip wallet; remove api.ideaidea.com.cn |
| 1.0.24 | 2026-07-27 | Fix ClawHub audit |
| 1.0.1 | 2026-07-20 | Fix payment flow |
| 1.0.0 | 2026-07-19 | Initial release |
