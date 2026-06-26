# pricing-engine

> 动态定价引擎：铜价联动 × 数量阶梯 × 客户等级 × 汇率自动换算

## Overview

`pricing-engine` 是 Farreach Electronic 的核心定价模块，属于 Evolution 系统 Phase 3。它将材料成本（LME 铜价实时联动）、数量阶梯折扣、客户等级（A/B/C/D）、多币种汇率整合为一套自动化定价流程，并直接集成到 `quotation-workflow` 生成 PDF/HTML 报价单。

## Architecture

```
铜价数据 (copper-price-monitor)
        │
        ▼
 copper-price-adapter.js
        │
        ├──────────────────────────────────┐
        ▼                                  ▼
 exchange-rate.js              products-cost.json
 (4h 缓存 + 离线降级)          discount-rules.json
        │                      margin-rules.json
        │                      customer-overrides.json
        └──────────────┬───────────────────┘
                       ▼
              pricing-engine.js  ◄── 核心引擎
               (calculatePrice)
                       │
                       ├── price-history.js (记录)
                       ▼
         quotation-integration.js
                       │
                       ▼
           quotation-workflow (PDF/HTML/Excel)
```

## Pricing Logic

### 定价优先级
1. **协议价**（`customer-overrides.json`）：直接返回，忽略后续公式
2. **公式定价**：`(baseCost + copperCost) × (1 + targetMargin) × (1 - discount)`
3. **底价红线检查**：低于 `floorMargin` → `pending_approval` + Discord 通知

### 折扣规则
- **数量阶梯**：500 / 1000 / 5000 / 10000+ pcs
- **客户等级**：A（VIP，最大折扣）/ B / C / D（新客户，无折扣）
- **上限**：折扣不超过 25%（防过度折扣）

### 铜价联动
每个 SKU 配置 `copperWeight_kg`，铜材料成本 = `copperWeight × copperPrice`。铜价从 `copper-price-monitor` 输出文件读取，有缓存机制。

## File Reference

### Scripts

| 文件 | 大小 | 功能 |
|------|------|------|
| `scripts/pricing-engine.js` | 27KB | 核心定价引擎，集成所有模块 |
| `scripts/quotation-integration.js` | 30KB | 集成 quotation-workflow，生成报价单 |
| `scripts/copper-price-adapter.js` | 14KB | 铜价适配层，读取 copper-price-monitor 数据 |
| `scripts/exchange-rate.js` | 10KB | 汇率模块，open.er-api.com + 4h 缓存 |
| `scripts/price-history.js` | 11KB | 历史报价 JSONL 存储 + 查询 |

### Config Files

| 文件 | 说明 |
|------|------|
| `config/products-cost.json` | 产品 SKU 基础成本 + 铜用量系数 |
| `config/discount-rules.json` | 数量阶梯 + 客户等级折扣表 |
| `config/margin-rules.json` | 利润率目标 / 底价红线（按分类） |
| `config/customer-overrides.json` | 客户协议价（一客一价，优先级最高） |

## Usage Examples

### 快速报价
```bash
cd <pricing-engine-root>/scripts

# 单品报价
node pricing-engine.js quote HDMI-2.1-8K-2M 1000 B USD
# 输出：{ unitPrice: 4.46, totalPrice: 4460, margin: 0.1937, discount: 0.107, method: 'formula' }

# 查看所有 SKU
node pricing-engine.js products

# 查看某 SKU 铜成本
node pricing-engine.js cost HDMI-2.1-8K-2M
```

### 生成报价单
```bash
# DRY_RUN 测试（不生成真实 PDF）
DRY_RUN=true node quotation-integration.js generate \
  --customer CUST-001 --name "Acme Corp" \
  --items '[{"sku":"HDMI-2.1-8K-2M","quantity":1000},{"sku":"DP-1.4-4K-2M","quantity":500}]' \
  --currency USD --grade B

# 生产模式（生成真实 PDF）
node quotation-integration.js generate \
  --customer CUST-001 --name "Acme Corp" \
  --items '[{"sku":"HDMI-2.1-8K-2M","quantity":1000}]' \
  --currency USD --grade B
```

### 查询历史报价
```bash
# 按客户查询
node price-history.js query --customer CUST-001 --limit 20

# 按 SKU + 日期范围
node price-history.js query --sku HDMI-2.1-8K-2M --from 2026-03-01 --to 2026-03-31
```

### 汇率 & 铜价
```bash
# 查看当前汇率
node exchange-rate.js rates
node exchange-rate.js convert 100 USD CNY

# 查看铜价
node copper-price-adapter.js price
node copper-price-adapter.js cost-all   # 所有 SKU 铜成本
```

## Programmatic API

```js
const { calculatePrice, calculateBatch } = require('./scripts/pricing-engine');
const { generateQuotation, previewQuotation } = require('./scripts/quotation-integration');
const { recordQuote, queryHistory } = require('./scripts/price-history');
const { getRate, convertAmount } = require('./scripts/exchange-rate');
const { getCopperPrice, getCopperCostForProduct } = require('./scripts/copper-price-adapter');

// 单品报价
const result = await calculatePrice('HDMI-2.1-8K-2M', 1000, 'B', 'USD');
console.log(result.unitPrice, result.margin);

// 批量报价
const batch = await calculateBatch([
  { sku: 'HDMI-2.1-8K-2M', quantity: 1000 },
  { sku: 'DP-1.4-4K-2M', quantity: 500 }
], 'B', 'USD');

// 生成报价单
const quotation = await generateQuotation({
  customerId: 'CUST-001',
  customerName: 'Acme Corp',
  customerGrade: 'B',
  currency: 'USD',
  items: [{ sku: 'HDMI-2.1-8K-2M', quantity: 1000 }]
});
console.log(quotation.quotationNo, quotation.outputPath);
```

## Environment Variables

```bash
DRY_RUN=true          # 模拟模式：铜价 9500 USD/吨，固定汇率，跳过 PDF 生成
PRICING_LOG=true      # 启用详细日志（logs/ 目录）
COPPER_LOG=true       # 启用铜价适配层日志
CACHE_TTL_MS=14400000 # 汇率缓存时间（默认 4h）
PRICE_HISTORY_FILE=/path/to/custom.jsonl  # 自定义历史记录路径
```

## Integration Notes

### quotation-workflow 集成
`quotation-integration.js` 依赖 quotation-workflow 的以下脚本：
- `scripts/generate-all.sh`：生成完整报价单套件（PDF + HTML + Excel）
- `scripts/generate_quotation_html.py`：HTML 报价单生成

确保 quotation-workflow 已安装在：
`<quotation-workflow-root>/`

### copper-price-monitor 集成
copper-price-adapter 从 copper-price-monitor 的输出数据文件读取铜价。
如果 copper-price-monitor 未运行或数据过期，适配层会使用缓存值并记录警告。

### 底价红线处理流程
```
计算价格 → 检查利润率 → 低于 floorMargin
                                │
                                ▼
                    设置 status = pending_approval
                    发送 Discord 通知
                    等待人工确认（不自动拒绝）
                    确认后继续生成报价单
```

## Development

### 添加新 SKU
编辑 `config/products-cost.json`，添加：
```json
{
  "sku": "NEW-SKU-CODE",
  "description": "产品描述",
  "category": "HDMI",
  "baseCost_usd": 3.00,
  "copperWeight_kg": 0.08
}
```

### 添加客户协议价
编辑 `config/customer-overrides.json`，添加：
```json
{
  "customerId": "CUST-NEW-001",
  "sku": "HDMI-2.1-8K-2M",
  "unitPrice_usd": 5.50,
  "note": "2026 年度合同"
}
```

### 调整利润率规则
编辑 `config/margin-rules.json` 中对应分类的 `targetMargin` 和 `floorMargin`。

## Status

- **Phase**: 3
- **Status**: packaged
- **Completed Subtasks**: 6/6
- **Last Updated**: 2026-03-25

## Related Skills

- [`quotation-workflow`](../quotation-workflow/) — 报价单生成工作流
- [`copper-price-monitor`](../copper-price-monitor/) — LME 铜价监控
- [`customer-segmentation`](../customer-segmentation/) — 客户等级分类
