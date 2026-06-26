---
name: sf-express
version: 1.1.2
description: Use SF Express (顺丰速运) for shipment tracking, delivery anomaly triage, e-commerce seller/customer handoffs, shipping guidance, service-type comparison, outlet lookup, and delivery-time or fee estimation. Use when the user asks about 顺丰、顺丰单号查询、物流异常、包裹停滞、异常签收、寄快递、顺丰时效、顺丰运费、顺丰网点, or wants practical help understanding or managing an SF Express shipment. This skill may persist local user data for history and subscriptions when its runtime code is used.
---

# SF Express

## Overview

Use this skill to help users with common SF Express tasks such as tracking shipments, understanding service levels, estimating timing or fees, and preparing to send a parcel.

## Live Data and Demo Boundary

The bundled CLI must not fabricate live SF Express tracking.

- Real tracking requires a user-configured live endpoint through `SF_EXPRESS_TRACKING_ENDPOINT`.
- Remote live endpoints must use HTTPS; plain HTTP is accepted only for `127.0.0.1` or `localhost` development.
- If no endpoint is configured, `query` and `batch` fail safely instead of returning made-up logistics events.
- Demo data is still available for onboarding and tests, but only with `--mock`; every mock result is labelled `模拟演示数据（非真实物流）`.
- Do not describe mock output as live carrier data, proof of delivery, or an ETA.

Examples:

```bash
# Live endpoint path; endpoint may use {tracking_number} or a tracking_number query param
SF_EXPRESS_TRACKING_ENDPOINT="https://example.internal/sf/{tracking_number}" python3 sfexpress.py query SF1234567890

# Explicit demo path
python3 sfexpress.py query SF1234567890 --mock
```

## E-commerce Logistics Triage Workflow

For marketplace, merchant, or after-sales questions, start with triage before giving a recommendation:

1. Identify the actor: buyer, seller, customer-support agent, or operations owner.
2. Classify the latest tracking state:
   - **No first scan**: label created but not picked up.
   - **Line-haul stall**: no update after trunk departure or arrival.
   - **Transit delay**: moving but beyond the promised or typical window.
   - **Customs/security hold**: inspection, quarantine, or restricted-item review.
   - **Out for delivery risk**: repeated failed delivery or unreachable recipient.
   - **Abnormal signed**: signed by unknown person, wrong location, or user denies receipt.
   - **Return/reverse logistics**: package routed back to sender or after-sales address.
3. Give a buyer/seller handoff:
   - Buyer: what to check, what evidence to save, when to contact SF or the merchant.
   - Seller: order id, tracking id, promise window, refund/reship threshold, customer message draft.
4. State uncertainty. Do not promise arrival times unless live SF data or user-provided carrier data supports it.
5. Redact personal data in shared summaries: show partial phone/address/tracking details when possible.

Use this compact output for anomalies:

```text
Status: <normal | watch | delayed | abnormal | needs user action>
Evidence: <latest scan + timestamp + route>
Likely cause: <one or two cautious possibilities>
Next action: <buyer step / seller step>
Escalate if: <time threshold or status trigger>
```

## Local Persistence

When the local CLI/runtime code is used, this skill may create and persist local data under:

- `~/.openclaw/data/sf-express/sfexpress.db`
  - stores query history
  - stores shipment-subscription records
  - may store saved address records if those commands are implemented/used
- `~/.openclaw/data/sf-express/secure/`
  - stores encrypted local files used by the privacy/storage helper
- `~/.openclaw/data/sf-express/secure/.key`
  - stores a local encryption key file with mode `600`
- `~/.openclaw/data/sf-express/privacy_export.json`
  - may be created when the user runs privacy export

Only use persistence when it is necessary for the user's requested workflow. If the user asks about privacy, disclose these paths clearly.

## Privacy Controls

The local CLI supports privacy operations:

- `privacy info` — show local storage paths and stored-file info
- `privacy clear` — clear local SQLite history/subscription/address data, encrypted local files, and prior privacy exports
- `privacy export` — export local storage metadata to `privacy_export.json`

## Workflow

1. Determine the user's goal:
   - track an existing shipment
   - estimate fee or delivery time
   - compare service types
   - find a nearby outlet or locker
   - prepare shipment details
   - review or clear local history/subscriptions/privacy data
2. Ask for only the missing essentials, such as tracking number, route, package size, or urgency.
3. Give the most practical answer first.
4. If exact fee or timing cannot be confirmed, provide a cautious estimate and state assumptions.
5. If the task uses local runtime features that persist data, mention that local history/subscription/privacy files may be created under `~/.openclaw/data/sf-express/`.
6. Do not claim to complete real shipping actions unless live tools are available and confirmed.

---

## 🚀 First-Success Path

**30秒快速上手：两个常用场景**

### 场景 A：查快递
1. **告诉我单号** — 如 "SF1234567890"
2. **确认数据来源** — 真实端点、用户提供轨迹，或明确 `--mock` 演示
3. **获取物流状态** — 轨迹 + 谨慎 ETA + 异常分诊

> 示例："查一下顺丰单号 SF1234567890 到哪了"

### 场景 B：算运费
1. **告诉我出发地和目的地** + 物品重量/尺寸
2. **获取运费报价** — 含不同服务类型价格对比
3. **选择最合适的服务** — 标准/特快/即日

> 示例："从北京寄上海，2公斤文件，大概多少钱？"

---

## 📝 Sample Prompts

### 示例 1：快递单号查询
**用户输入：**
```
查一下顺丰单号 SF1234567890 的物流信息
```

**期望输出：**
```
📍 快递追踪：SF1234567890

数据来源：真实查询端点（或用户提供轨迹）
当前状态：正在派送中
预计到达：以顺丰实时页面/端点为准；当前建议按今天 18:00 前观察

📦 完整轨迹：
06-16 08:30 | 北京朝阳区CBD营业部 | 派送中
06-16 06:15 | 北京朝阳中转场 | 已到达
06-15 22:30 | 上海浦东集散中心 | 已发出
06-15 18:00 | 上海浦东新区营业部 | 已揽收

下一步：如需更改配送，请在顺丰官方渠道或派件员来电后由用户本人操作。
```

### 示例 2：运费估算
**用户输入：**
```
从广州寄到武汉，5公斤衣服，大概多少钱？顺丰标快和特快要多少钱？
```

**期望输出：**
```
💰 运费估算：广州 → 武汉（5kg）

顺丰标快（标准快递）：
- 预估 ¥36-42
- 预计 2-3 天到达

顺丰特快（时效优先）：
- 预估 ¥52-60
- 预计 1-2 天到达

💡 建议：
- 衣服非急用→标快性价比高
- 有易损物品→可选保价服务（保费 = 保价金额×0.1%）
- 精确价格以寄件时系统报价为准
```

### 示例 3：网点查询
**用户输入：**
```
帮我找找广州市天河区附近的顺丰网点
```

**期望输出：**
```
📍 广州市天河区顺丰网点

1️⃣ 天河营业部
   地址：天河区体育西路128号
   电话：020-3888xxxx
   营业时间：08:00-20:00

2️⃣ 珠江新城速运营业点
   地址：天河区珠江新城华夏路36号
   电话：020-3889xxxx
   营业时间：09:00-19:00

3️⃣ 天河东路自助柜
   地址：天河区天河东路66号小区门口
   类型：自助投递/取件 24小时

💡 附近还有 5 个丰巢快递柜可用
```

### 示例 4：服务类型对比
**用户输入：**
```
顺丰标快、特快、即日达有什么区别？寄文件选哪个？
```

**期望输出：**
```
📊 顺丰服务类型对比

| 服务类型 | 适用场景 | 省内 | 跨省 | 价格（1kg） |
|---------|---------|------|------|------------|
| 标快 | 常规寄件 | 1-2天 | 2-3天 | ¥12-18 |
| 特快 | 时效优先 | 次日 | 1-2天 | ¥22-28 |
| 即日达 | 当日必达 | 当天 | 部分城市 | ¥60-90+ |

✅ 寄文件推荐：标快
- 文件不易损坏，标快性价比最高
- 如有合同等重要文件，建议加**¥1保价服务**
- 文件类推荐用顺丰**文件封**（免费领取）
```

### 示例 5：寄件指南
**用户输入：**
```
我想寄一箱螃蟹到外省，顺丰能寄吗？要注意什么？
```

**期望输出：**
```
🦀 生鲜寄件指南（如螃蟹）

✅ 顺丰支持生鲜寄递，需注意：

📦 包装要求：
- 必须有保温箱/泡沫箱 + 冰袋
- 外部纸箱加固
- 标注"生鲜易腐"

💰 运费说明：
- 按实际重量计费 + 包装物料费（约¥5-15）
- 建议加购**生鲜保险**

⏰ 时效建议：
- 选顺丰特快（缩短在途时间）
- 避开周末/节假日高峰
- 尽量早寄、选上午时段揽收

⚠️ 注意：提前确认目的地城市可收生鲜快递
```

---

## 📋 Real Task Examples

| 场景 | 用户输入示例 | 技能输出要点 |
|------|-------------|-------------|
| **查快递** | "我买的东西寄出来了，SF9876543210到了没？" | 先确认真实端点/用户提供轨迹 → 显示轨迹和当前状态 → 给出谨慎 ETA 与异常分诊 |
| **算运费** | "深圳到北京寄10公斤书多少钱？" | 标快/特快价格对比 → 提示超重可能分段计费 → 建议打包方式省运费 |
| **找网点** | "附近哪里有顺丰可以寄快递？我在上海徐汇" | 列出附近营业部/服务点/自助柜 → 含地址电话营业时间 → 推荐最近最方便的 |
| **选服务** | "我要寄护照到美国，用顺丰国际怎么操作？" | 国际件服务介绍 → 所需材料清单 → 清关提示 → 预估时效（5-7工作日） |
| **寄特殊物品** | "我想寄几瓶白酒回家，顺丰给寄吗？" | 酒类寄递政策说明 → 包装要求 → 最大瓶数限制 → 保价建议 |
