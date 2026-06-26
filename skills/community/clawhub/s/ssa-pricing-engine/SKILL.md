---
name: pricing-engine
description: 动态定价引擎 — 根据 LME 铜价、数量阶梯、客户等级、实时汇率自动计算报价，集成 quotation-workflow 生成报价单
---

# pricing-engine

## Description

动态定价引擎 Skill，根据 LME 铜价、数量阶梯、客户等级（A/B/C/D）、实时汇率自动计算产品报价，并一键集成到 quotation-workflow 生成完整报价单。支持协议价覆盖（一客一价）、底价红线保护、历史报价记录。

适用场景：
- 收到询价时快速生成动态报价
- 批量报价单生成（多 SKU / 多客户）
- 查询历史报价记录和客户价格档案
- 铜价波动时快速重新报价

---

## Dependencies

| Skill | 说明 |
|-------|------|
| `quotation-workflow` | PDF/HTML/Excel 报价单生成（必须已安装并配置） |
| `copper-price-monitor` | 铜价数据源（输出文件供本 Skill 读取） |
| `customer-segmentation` | 客户等级数据（A/B/C/D）参考来源 |

---

## Environment Variables

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `DRY_RUN` | `false` | `true` 时使用模拟数据（铜价 9500 USD/吨，固定汇率），跳过 PDF 生成 |
| `PRICING_LOG` | `false` | `true` 时启用详细日志（写入 `logs/` 目录） |
| `COPPER_LOG` | `false` | `true` 时启用铜价适配层日志 |
| `CACHE_TTL_MS` | `14400000` | 汇率缓存时间（毫秒，默认 4 小时） |
| `PRICE_HISTORY_FILE` | `output/price-history.jsonl` | 自定义历史报价存储路径 |

---

## Directory Structure

```
pricing-engine/
├── SKILL.md
├── README.md
├── config/
│   ├── products-cost.json        # 产品基础成本表
│   ├── discount-rules.json       # 数量阶梯 + 客户等级折扣规则
│   ├── margin-rules.json         # 利润率目标 + 底价红线
│   └── customer-overrides.json   # 客户协议价覆盖（一客一价）
├── scripts/
│   ├── exchange-rate.js          # 汇率模块（4h 缓存 + 离线降级）
│   ├── copper-price-adapter.js   # 铜价适配层
│   ├── pricing-engine.js         # 核心定价引擎
│   ├── price-history.js          # 历史报价记录
│   └── quotation-integration.js  # 集成报价单工作流
├── cache/                        # 汇率缓存（自动生成）
├── data/                         # 内部数据（报价单编号计数器等）
├── logs/                         # 运行日志（PRICING_LOG=true 时写入）
└── output/                       # 生成报价单 + 历史记录 JSONL
```

---

## Scripts

### scripts/pricing-engine.js — 核心定价引擎

输入产品 SKU + 数量 + 客户等级 + 币种，输出含利润率的报价结果。
优先级：协议价（customer-overrides） > 公式定价。
低于底价红线时触发 Discord 通知并等待人工确认。

**CLI 用法：**
```bash
cd <pricing-engine-root>/scripts

# 单品报价（SKU 数量 客户等级 [币种]）
node pricing-engine.js quote HDMI-2.1-8K-2M 1000 B USD
node pricing-engine.js quote HDMI-2.1-8K-2M 5000 A CNY

# 批量报价（JSON 文件）
node pricing-engine.js batch /path/to/items.json

# 查询产品基础成本
node pricing-engine.js cost HDMI-2.1-8K-2M

# 列出所有产品
node pricing-engine.js products
```

**require() API：**
```js
const { calculatePrice, calculateBatch, getProductCost, listProducts } = require('./pricing-engine');

// 单品报价
const result = await calculatePrice('HDMI-2.1-8K-2M', 1000, 'B', 'USD');
// → { unitPrice, totalPrice, margin, discount, method, floorPriceWarning, ... }

// 批量报价
const batch = await calculateBatch([
  { sku: 'HDMI-2.1-8K-2M', quantity: 1000 },
  { sku: 'DP-1.4-4K-2M', quantity: 500 }
], 'B', 'USD');
```

**客户等级：** A（VIP）/ B（优质）/ C（标准）/ D（新客户）

---

### scripts/quotation-integration.js — 集成报价单工作流

定价引擎输出 → quotation-workflow 数据格式 → 自动生成 PDF/HTML 报价单。自动记录报价历史。

**CLI 用法：**
```bash
cd <pricing-engine-root>/scripts

# 生成完整报价单（含 PDF）
node quotation-integration.js generate \
  --customer CUST-001 \
  --name "Acme Corp" \
  --items '[{"sku":"HDMI-2.1-8K-2M","quantity":1000}]' \
  --currency USD \
  --grade B

# 仅预览价格（不生成 PDF）
node quotation-integration.js preview \
  --customer CUST-001 \
  --items '[{"sku":"HDMI-2.1-8K-2M","quantity":1000},{"sku":"DP-1.4-4K-2M","quantity":500}]' \
  --currency USD

# DRY_RUN 模式（模拟数据，不生成 PDF）
DRY_RUN=true node quotation-integration.js generate \
  --customer CUST-TEST \
  --name "Test Corp" \
  --items '[{"sku":"HDMI-2.1-8K-2M","quantity":1000}]' \
  --currency USD
```

**require() API：**
```js
const { generateQuotation, previewQuotation } = require('./quotation-integration');

// 生成完整报价单
const result = await generateQuotation({
  customerId: 'CUST-001',
  customerName: 'Acme Corp',
  customerGrade: 'B',
  currency: 'USD',
  items: [
    { sku: 'HDMI-2.1-8K-2M', quantity: 1000 },
    { sku: 'DP-1.4-4K-2M', quantity: 500 }
  ]
});
// → { quotationNo, outputPath, totalAmount, items, ... }

// 仅预览价格
const preview = await previewQuotation({ customerId, customerGrade, currency, items });
```

---

### scripts/exchange-rate.js — 汇率模块

对接 open.er-api.com 免费汇率 API，4h 缓存 + 离线降级（使用上次缓存值）。
支持 USD / EUR / GBP / CNY。

**CLI 用法：**
```bash
cd <pricing-engine-root>/scripts

# 查看当前所有汇率（base: USD）
node exchange-rate.js rates

# 查询特定汇率
node exchange-rate.js rate EUR
node exchange-rate.js rate CNY

# 汇率换算
node exchange-rate.js convert 100 USD CNY

# 强制刷新缓存
node exchange-rate.js refresh
```

**require() API：**
```js
const { getRate, convertAmount, getAllRates, refreshRates } = require('./exchange-rate');

const rate = await getRate('USD', 'CNY');       // → 7.25
const cny = await convertAmount(100, 'USD', 'CNY'); // → 725.0
```

---

### scripts/copper-price-adapter.js — 铜价适配层

读取 copper-price-monitor 的输出数据文件，计算各产品 SKU 的铜材料成本（USD）。薄适配层，不重复实现铜价抓取。

**CLI 用法：**
```bash
cd <pricing-engine-root>/scripts

# 查看最新铜价
node copper-price-adapter.js price

# 查看指定 SKU 的铜材料成本
node copper-price-adapter.js cost HDMI-2.1-8K-2M
node copper-price-adapter.js cost DP-1.4-4K-2M

# 查看所有产品铜成本
node copper-price-adapter.js cost-all

# 查看数据最后更新时间
node copper-price-adapter.js last-updated

# 强制刷新缓存
node copper-price-adapter.js refresh
```

**require() API：**
```js
const { getCopperPrice, getCopperCostForProduct, getCopperCostBatch, getLastUpdated } = require('./copper-price-adapter');

const { price, currency } = await getCopperPrice(); // → { price: 9500, currency: 'USD', source: ... }
const { copperWeight_kg, copperCost_usd } = await getCopperCostForProduct('HDMI-2.1-8K-2M');
```

---

### scripts/price-history.js — 历史报价记录

JSONL 追加存储，支持按客户/SKU/日期范围查询。每条记录自动生成唯一 ID（QH-YYYYMMDD-NNN）。

**CLI 用法：**
```bash
cd <pricing-engine-root>/scripts

# 手动记录一次报价
node price-history.js record '{"sku":"HDMI-2.1-8K-2M","quantity":1000,"unitPrice":4.46,"currency":"USD","customerId":"CUST-001"}'

# 查询全部历史（最近 10 条）
node price-history.js query --limit 10

# 按客户查询
node price-history.js query --customer CUST-001 --limit 20

# 按 SKU 查询（不区分大小写）
node price-history.js query --sku hdmi-2.1-8k-2m

# 按日期范围查询
node price-history.js query --from 2026-03-01 --to 2026-03-31
```

**require() API：**
```js
const { recordQuote, queryHistory } = require('./price-history');

const id = await recordQuote({ sku, quantity, unitPrice, currency, customerId, ... });
// → 'QH-20260325-001'

const history = await queryHistory({ customerId: 'CUST-001', limit: 10 });
```

---

## Config Files

### config/products-cost.json

产品基础成本表。每个 SKU 包含：
- `baseCost_usd`：基础成本（USD，不含铜价）
- `copperWeight_kg`：每件铜用量（kg），用于铜价联动计算
- `category`：产品分类（HDMI / DP / USB / LAN）
- `description`：产品描述

```json
{
  "products": [
    {
      "sku": "HDMI-2.1-8K-2M",
      "description": "HDMI 2.1 8K 2米",
      "category": "HDMI",
      "baseCost_usd": 2.50,
      "copperWeight_kg": 0.065
    }
  ]
}
```

### config/discount-rules.json

数量阶梯折扣 + 客户等级折扣规则。
- 数量阶梯：500 / 1000 / 5000 / 10000+
- 客户等级：A（VIP）/ B（优质）/ C（标准）/ D（新客户）
- 折扣上限：25%（防止过度折扣）

### config/margin-rules.json

利润率目标 + 底价红线。
- `targetMargin`：目标利润率（软性，供参考）
- `floorMargin`：底价红线（低于此利润率触发 Discord 通知 + 等待人工确认）
- 支持按产品分类设置不同规则

### config/customer-overrides.json

客户协议价覆盖（一客一价）。配置后该客户该 SKU 直接返回协议价，忽略公式定价。

```json
{
  "overrides": [
    {
      "customerId": "CUST-ACME-001",
      "sku": "HDMI-2.1-8K-2M",
      "unitPrice_usd": 6.80,
      "note": "年度合同价"
    }
  ]
}
```

---

## Quick Start

```bash
SKILL_DIR=<pricing-engine-root>
cd $SKILL_DIR/scripts

# 1. 测试模式（无需真实铜价/汇率数据）
DRY_RUN=true node pricing-engine.js quote HDMI-2.1-8K-2M 1000 B USD

# 2. 生成报价单
DRY_RUN=true node quotation-integration.js generate \
  --customer CUST-001 --name "Test Corp" \
  --items '[{"sku":"HDMI-2.1-8K-2M","quantity":1000}]' \
  --currency USD

# 3. 查看历史报价
node price-history.js query --limit 10
```

---

## Notes

- **底价红线触发**：价格低于 `margin-rules.json` 中配置的 `floorMargin` 时，不直接拒绝，而是记录 `pending_approval` 状态并发送 Discord 通知等待人工确认（外贸需要'亏本拿单'场景支持）。
- **离线降级**：汇率 API 不可用时自动使用上次缓存值，不影响报价流程。
- **DRY_RUN 模式**：所有模块均支持 `DRY_RUN=true`，使用模拟数据，适合测试和演示。
- **Phase 4 延后**：趋势分析功能（price-history