---
name: "ssq-analyzer"
version: "1.0.29"
description: >
  SSQ (Double Color Ball) lottery intelligent analysis: fetches official draw data from cwl.gov.cn, computes hot/cold statistics, frequency distributions, AC values, odd-even ratios, and zone distributions. Paid tier (3.9 yuan/run) delivers 5 recommended number sets via clawtip payment.
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
      outputs: ["order_no", "amount", "indicator"]
    pay:
      requires: clawtip
      args: ["{order_no}", "{indicator}"]
    service:
      script: scripts/service.py
      args: ["{order_no}"]
---

# ssq-analyzer

> The primary interaction language is Chinese. If the user prefers English or another language, the assistant should switch accordingly.

## 技能概述

本技能提供**双色球彩票智能分析服务**，从中国福利彩票官网（cwl.gov.cn）拉取最新开奖数据，进行冷热号统计、规律分析和号码推荐。

### 免费功能（无需支付，随时可用）

✅ **数据抓取与数据库管理** — 从 cwl.gov.cn 官方 API 自动拉取最新开奖数据，增量更新本地 SQLite 数据库

✅ **红球冷热属性统计** — 近 20 期热度排名（热号 ≥ 6 次、温号 3-5 次、冷号 < 3 次），逐球号遗漏期数和出现频率

✅ **蓝球统计** — 近 20 期蓝球出现次数、遗漏期数和热温冷属性分类

✅ **特征分布统计** — 奇偶比分布、AC 值分布（算术复杂度）、三区分布、和值统计

✅ **近 20 期原始开奖数据** — 完整展示最近 20 期的红球、蓝球和开奖日期

### 付费功能（3.9 元/次，通过 clawtip 验证后交付）

🔒 **备选蓝球推荐（4 枚）** — 基于冷号反弹概率、奇偶搭配、遗漏深度等多策略综合排序

🔒 **最终推荐号码（5 组）** — 每组 6 红球 + 1 蓝球，通过奇偶比、AC 值、三区分布、和值、连号、冷热配比等多维交叉过滤校验

> **免费用户无需创建订单或配置支付**。直接运行 `fetch_ssq.py` 和 `analyze_ssq.py` 即可获取完整统计分析。
> 推荐号码需要先创建订单，通过 clawtip 完成 3.9 元支付后，由 `service.py` 生成。

---

## 环境变量配置

仅当需要支付验证时使用（运行 `create_order.py` 时）：

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `CLAWTIP_PAY_TO` | 是 | clawtip 商户收款地址 |
| `CLAWTIP_SM4_KEY` | 是 | SM4 加密密钥 |

---

## 前置条件

如需支付功能，需安装 clawtip：

```bash
openclaw skills install clawtip
```

---

## 🚀 免费使用（无需支付）

直接运行以下命令即可获取完整统计分析：

**抓取最新数据：**
```bash
python3 scripts/fetch_ssq.py
```

**生成分析报告：**
```bash
python3 scripts/analyze_ssq.py
```

报告包含：红球冷热统计、蓝球统计、奇偶比/AC值/三区分布/和值等特征分析、近 20 期开奖数据。

---

## 🛒 第一阶段：创建订单（仅付费推荐需要）

如果用户需要推荐号码，先创建订单。

```bash
python3 scripts/create_order.py
```

**成功输出：** `ORDER_NO=... AMOUNT=... INDICATOR=...`

**失败：** `订单创建失败: <详情>` → 终止。

> 运行后会在本地创建订单文件：`~/.openclaw/skills/orders/{indicator}/{order_no}.json`
> 仅包含支付必要的元数据（orderNo、amount、slug、payTo、encrypted_data、description、resource_url）。
> **不收集、不存储任何用户咨询内容、开奖数据或个人身份信息。**

---

## 💳 第二阶段：支付处理

使用技能 **clawtip** 处理支付。

调用参数：
- `orderNo`：第一阶段的 ORDER_NO
- `indicator`：第一阶段的 INDICATOR

> ⚠️ 必须使用名称精确等于 `clawtip` 的技能。

---

## 🚀 第三阶段：服务执行（含付费推荐）

无论是否支付，先执行免费分析：

```bash
python3 scripts/service.py
```

如果有支付凭证，推荐号码会自动附加。

如果已支付，传入订单号：

```bash
python3 scripts/service.py "<order_no>"
```

---

## 数据流说明

### 网络请求

| 方向 | 目标 | 传输内容 | 频率 |
|------|------|----------|------|
| 出站 | `cwl.gov.cn` API | 公开开奖查询（无用户数据） | 按需（用户触发） |
| 出站 | clawtip 支付服务 | 仅技能标识符 slug（无彩票数据、无用户数据） | 仅创建订单时 |

### 本地存储

| 文件 | 路径 | 内容 |
|------|------|------|
| 开奖数据库 | `scripts/ssq_data.db` | 公开开奖号码，无用户数据 |
| 分析报告 | `scripts/最新分析结果.md` | 统计结果 + 推荐号码（如有支付） |
| 订单文件 | `~/.openclaw/skills/orders/{indicator}/{order_no}.json` | 仅支付元数据（orderNo、amount、slug、payTo、encrypted_data） |

> **隐私承诺**：本技能不收集、不存储、不传输任何用户个人信息、咨询内容或彩票数据。
> 订单文件包含的字段均为支付处理所需的系统生成数据，不含用户输入内容。

### 绝不收集或传输

- 用户咨询内容或问题描述
- 个人身份信息、设备信息
- 支付密码或钱包私钥
- 选号偏好或购买记录

---

## 分析流程

1. **数据抓取**（免费）：`fetch_ssq.py` → `cwl.gov.cn` → 本地 SQLite
2. **统计分析**（免费）：`analyze_ssq.py` → 本地生成分析报告（不含推荐号码）
3. **号码推荐**（付费）：`service.py` → 验证凭证 → 生成推荐号码

---

## ⚠️ 风险提示

> 本报告基于历史数据统计分析生成。彩票开奖为随机独立事件，任何分析方法均不能保证中奖。请理性购彩，量力而行。

> 本技能使用 SM4 国密算法仅用于 clawtip 支付流程中的凭证加密。不用于加密彩票数据、用户信息或通信内容。

---

## 版本历史

| Version | Date | Notes |
|:--------|:-----|:------|
| 1.0.29 | 2026-07-29 | 移除 question 参数和存储；移除 argparse；更新隐私说明为精确声明 |
| 1.0.27 | 2026-07-28 | Fix SkillSpector: remove old report with paid numbers; update docstring for credential fields |
| 1.0.26 | 2026-07-28 | Fix SkillSpector: subprocess→direct import; accurate storage disclosure; question field caution |
| 1.1.1 | 2026-07-28 | Fix SkillSpector findings: freemium enforcement, remove --recommend bypass, inline SM4, accurate data-flow disclosure |
| 1.1.0 | 2026-07-28 | Switch to official clawtip wallet; env-var config |
| 1.0.20 | 2026-07-20 | Freemium model |
| 1.0.1 | 2026-07-20 | Fix payment flow |
| 1.0.0 | 2026-07-19 | Initial release |
