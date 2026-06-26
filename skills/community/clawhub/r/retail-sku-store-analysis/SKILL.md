---
name: retail-sku-store-analysis
description: |
  单SKU门店分析工具。分析单个商品在指定门店的销售表现、库存状态、导购贡献和AIoT转化数据。
  
  核心能力：
  1. SKU基础信息（名称、款号、颜色、包型、标准价、上市日期）
  2. 销售表现（销售额、销量、成交均价、贡献率、排名）
  3. 库存状态（当前库存、在架天数、绑定状态）
  4. 导购贡献（各导购销售额、销量、连带率、成交客户数）
  5. AIoT转化数据（试用次数、成交件数、转化率）
  
  触发条件：
  - 用户询问商品表现（如"心遥2卖得怎么样"）
  - 用户分析SKU数据（如"这个款库存还多吗"）
  - 用户需要导购贡献分析（如"谁卖了这款包"）
---

# 单SKU门店分析 Skill

分析单个商品在指定门店的销售表现、库存状态、导购贡献和AIoT转化数据。

## 使用方式

```python
import sys
sys.path.insert(0, '~/.openclaw/skills/sku-store-analysis')
import analyze as sku_analyze

# AIoT门店（获取完整数据）
result = sku_analyze.analyze(
    store_id="416759_1714379448487",
    goods_base_id="34311",
    from_date="2026-03-01",
    to_date="2026-03-26",
    store_name="正义路60号店",
    is_aiot_store=True
)

# 非AIoT门店（仅基础数据）
result = sku_analyze.analyze(
    store_id="416759_1714379448487",
    goods_base_id="34311",
    from_date="2026-03-01",
    to_date="2026-03-26",
    is_aiot_store=False
)
```

## API 端点

### 1. 基础数据（所有门店）
```
GET /api/v1/store/dashboard/bi/goods/detail
```

### 2. 导购表现数据（仅AIoT门店）
```
GET /api/v1/store/dashboard/bi/goods/performance
```

## 字段映射

### 基础数据字段
| API 字段 | Skill 字段 | 说明 |
|---------|-----------|------|
| `goodsBaseId` | `goods_base_id` | 商品基础ID |
| `goodsName` | `goods_info.name` | 商品名称 |
| `goodsModelCode` | `goods_info.model_code` | 款号 |
| `goodsColor` | `goods_info.color` | 颜色 |
| `goodsSize` | `goods_info.size` | 尺寸 |
| `goodsShape` | `goods_info.bag_type` | **包型** |
| `standardPrice` | `goods_info.standard_price` | 标准价 |
| `goodsLauchDate` | `goods_info.launch_date` | 上市日期 |
| `imageUrl` | `goods_info.image_url` | 图片URL |
| `dealAmount` | `metrics.sales.amount` | **统计周期内**销售额 |
| `dealAvgAmount` | `metrics.sales.avg_price` | **统计周期内**成交均价 |
| `qty` | `metrics.sales.qty` | **统计周期内**销量 |
| `giftQty` | `metrics.sales.gift_qty` | **统计周期内**赠品数量 |
| `contributeRate` | `metrics.sales.contribute_rate` | **占门店销售额百分比（已加%）** |
| `contributeRateFloat` | `metrics.sales.contribute_rate_float` | 贡献率原值 |
| `inventory` | `metrics.inventory.current` | **当前**库存 |
| `inStockDays` | `metrics.aiot.in_stock_days` | **AIoT在架天数**（系统记录） |
| `binding` | `metrics.aiot.binding_state` | **AIoT绑定状态（1=绑定，2=未绑定）** |
| `transFrequency` | `metrics.sales.lifetime_frequency` | **上市以来**成交频次 |
| `dealMoneyTotalRank` | `metrics.ranking.sales_rank` | 销售额排名 |
| `dealMoneyShareRank` | `metrics.ranking.share_rank` | 销售占比排名 |

### 导购表现字段（AIoT）
| API 字段 | Skill 字段 | 说明 |
|---------|-----------|------|
| `clerkName` | `metrics.clerks.list[].name` | 导购姓名 |
| `salesAmount` | `metrics.clerks.list[].sales_amount` | 销售额 |
| `salesPercentage` | `metrics.clerks.list[].sales_share` | 销售占比（%） |
| `effectiveOrderCount` | `metrics.clerks.list[].orders` | 订单数 |
| `effectiveQtyCount` | `metrics.clerks.list[].qty` | 销量 |
| `attachQtyRatio` | `metrics.clerks.list[].attach_ratio` | 连带率 |
| `transGroup` | `metrics.clerks.list[].trans_group` | 成交客户数 |
| `deepTrialGroup` | `metrics.clerks.list[].deep_trial_group` | 深度试用客户数 |
| `trialGroup` | `metrics.clerks.list[].trial_group` | 试用客户数 |
| `deepTrialTransRate` | `metrics.clerks.list[].deep_trial_trans_rate` | 深度试用转化率 |

### 新老客字段（AIoT）
| API 字段 | Skill 字段 | 说明 |
|---------|-----------|------|
| `isNewVip` | - | 1=新客, 2=老客 |
| `salesAmount` | `metrics.vips.new_vip/old_vip.sales_amount` | 销售额 |
| `salesPercentage` | `metrics.vips.new_vip/old_vip.sales_share` | 占比 |
| `effectiveQtyCount` | `metrics.vips.new_vip/old_vip.qty` | 销量 |

### AIoT表现字段（AIoT）
| API 字段 | Skill 字段 | 说明 |
|---------|-----------|------|
| `inStockDays` | `metrics.aiot_performance.in_stock_days` | **统计期间**SKU绑定信标在架天数 |
| `transGroup` | `metrics.aiot_performance.trans_group` | **绑定状态**成交的客户组数 |
| `deepTrialGroup` | `metrics.aiot_performance.deep_trial_group` | **绑定状态**深度试用的组数 = **意向客户组数** |
| `trialGroup` | `metrics.aiot_performance.trial_group` | **绑定状态**累计试用组数 = **潜在客户组数** |
| `deepTrialTransRate` | `metrics.aiot_performance.deep_trial_trans_rate` | **深度试用→成交转化率** |
| `sellThroughRate` | `metrics.aiot_performance.sell_through_rate` | 售罄率（已加%） |
| `sellThroughRateFloat` | `metrics.aiot_performance.sell_through_rate_float` | 售罄率原值 |
| `level` | `metrics.aiot_performance.level` | 等级 |

**售罄率公式：**
```
售罄率 = 1 - 期末库存 / (期初库存 + 期间增加库存)
```

## 分析维度

### 基础分析（所有门店）
- 销售指标：销售额、销量、成交均价、赠品、贡献占比、排名
- 价格指标：标准价、折扣率
- 库存指标：当前库存、库销比
- AIoT基础：绑定状态、在架天数（系统记录）
- 生命周期：上市以来成交频次

### AIoT增强分析（仅AIoT门店）
- **导购表现**：各导购销售贡献、集中度分析、零销售识别
- **新老客分布**：新客/老客购买占比
- **AIoT转化漏斗**：
  - 潜在客户（试用组数）
  - 意向客户（深度试用组数）
  - 成交客户（成交组数）
  - 深度试用→成交转化率
- **售罄率**：库存周转效率

## 诊断规则

| 发现 | 条件 |
|------|------|
| 🔴 库存断货 | 库存 = 0 |
| 🟡 库存偏低 | 库存 ≤ 2 |
| 🟡 库存积压 | 库存 > 销量×3 |
| 🟡 高折扣 | 折扣率 > 20% |
| ⚠️ AIoT未绑定 | binding = 2 |
| 📊 高频销售 | 成交频次 < 7天 |
| 💡 动销较慢 | 成交频次 > 30天 |
| 📊 销售冠军 | 排名第1 |
| 💡 老款商品 | 在架 > 180天 |
| ⚠️ 销售高度集中 | TOP3占比 > 80% |
| 💡 零销售导购 | 存在销售额=0的导购 |
| 📊 深度试用转化率高 | ≥ 50% |
| ⚠️ 深度试用转化率低 | < 20% |
| 📊 新客占比高 | > 50% |
| 📊 老客复购为主 | 老客占比 > 80% |
| 📊 售罄率高 | > 80% |

## 输出结构

```json
{
  "status": "ok",
  "subject_type": "sku_store",
  "store_id": "...",
  "goods_base_id": "...",
  "is_aiot_store": true,
  "goods_info": {
    "name": "...",
    "model_code": "...",
    "color": "...",
    "size": "...",
    "bag_type": "...",
    "standard_price": 1099,
    "launch_date": "2025/7/1",
    "aiot_binding": 1,
    "aiot_in_stock_days": 227
  },
  "core_metrics": {
    "sales": {...},
    "price": {...},
    "inventory": {...},
    "aiot": {...},
    "ranking": {...},
    "clerks": {...},
    "vips": {...},
    "aiot_performance": {
      "in_stock_days": 16,
      "trans_group": 4,
      "deep_trial_group": 11,
      "trial_group": 28,
      "deep_trial_trans_rate": 0.36,
      "sell_through_rate": "83.3",
      "sell_through_rate_float": 0.833333,
      "level": "--"
    }
  },
  "findings": [...],
  "recommendations": [...]
}
```

## Skill 路径
`~/.openclaw/skills/sku-store-analysis/`
