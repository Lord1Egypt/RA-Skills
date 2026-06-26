---
name: price-analysis
description: 当用户需要了解价格区间、分析价格趋势、获取议价建议或进行成本核算时触发
version: 1.0.0
tools_required:
  - price_database
  - market_trend_analyzer
  - negotiation_advisor
---

# 价格分析技能 (Price Analysis)

## 触发条件

以下场景自动触发价格分析技能：
- 用户点击商品详情页的价格区间展示
- 用户询问"这个价格能便宜吗"
- 用户想要"砍价"，请求谈判策略
- 成本核算和利润计算
- 批量采购的价格方案咨询
- 价格变动通知和预警

## 执行步骤

### Step 1: 价格数据获取
```
1. 查询该商品的历史报价记录
2. 获取当前市场价格区间
3. 收集同规格竞品价格
4. 汇总采购商的采购记录
```

### Step 2: 价格结构分析
```
FOB价格 = 出厂价 + 包装费 + 验货费 + 装柜费
CIF价格 = FOB + 海运费 + 保险费 + 港口杂费
电商成本 = 采购价 + 国内运费 + 关税 + 平台佣金 + 头程物流
```

### Step 3: 区间分析
```
1. 计算价格区间: [最低价, 市场价, 最高价]
2. 识别价格分布:
   - 低价区: < P25 (价格洼地)
   - 中价区: P25-P75 (合理区间)
   - 高价区: > P75 (溢价区)
3. 计算当前价格的百分位排名
```

### Step 4: 趋势分析
```
1. 分析30/60/90天价格走势
2. 识别价格拐点和异常波动
3. 判断趋势: 上涨/平稳/下跌
4. 预测未来1-2周趋势
```

### Step 5: 议价策略生成
```
1. 分析供应商价格空间
2. 识别议价切入点
3. 生成具体谈判话术
4. 设定目标价格和底线
```

## 输出格式

### 价格分析响应
```json
{
  "success": true,
  "skill": "price-analysis",
  "data": {
    "product_info": {
      "product_id": "WP2024001234",
      "product_name": "智能LED发光瑜伽垫",
      "specification": "8mm加厚，防滑，LED灯可充电"
    },
    "price_analysis": {
      "current_price": {
        "fob_yiwu": 12.50,
        "moq": 50,
        "currency": "USD"
      },
      "price_range": {
        "lowest": 10.20,
        "market": 12.00,
        "highest": 15.80,
        "unit": "USD"
      },
      "percentile": 62,
      "assessment": "当前价格处于市场中等偏上水平"
      },
    "cost_breakdown": {
      "factory_cost": 8.50,
      "packaging": 0.80,
      "inspection": 0.20,
      "loading": 0.30,
      "fob_yiwu": 9.80,
      "profit_margin_supplier": "21.6%"
    },
    "trend_analysis": {
      "period_30d": {
        "change": "+3.2%",
        "trend": "slight_up",
        "reason": "原材料涨价"
      },
      "period_90d": {
        "change": "-1.5%",
        "trend": "stable"
      },
      "forecast": {
        "direction": "stable",
        "confidence": 0.75,
        "outlook": "未来2周价格预计持稳"
      }
    },
    "quantity_discount": {
      "tiers": [
        {"moq": 50, "price": 12.50},
        {"moq": 200, "price": 11.80, "discount": "5.6%"},
        {"moq": 500, "price": 11.20, "discount": "10.4%"},
        {"moq": 1000, "price": 10.50, "discount": "16%"}
      ]
    }
  },
  "confidence": 0.88
}
```

### 议价建议响应
```json
{
  "success": true,
  "skill": "price-analysis",
  "data": {
    "negotiation_advisor": {
      "target_price": 11.00,
      "bottom_line": 10.50,
      "current_price": 12.50,
      "negotiation_room": "11.8%",
      "difficulty": "medium"
    },
    "strategies": [
      {
        "approach": "量价挂钩",
        "action": "承诺月度订单200件，争取价格降至11.80",
        "script": "如果我们每月稳定下单200件，能否给我们11.80的单价？",
        "expected_success": 0.85
      },
      {
        "approach": "竞品比较",
        "action": "提及同类供应商报价11.20，请其匹配",
        "script": "我们有另一家供应商报了11.20的价，您这边能匹配吗？",
        "expected_success": 0.60
      },
      {
        "approach": "长期合作",
        "action": "表达长期合作意向，换取优惠",
        "script": "我们计划长期合作，第一年预计采购5000件，能否给个长期合作价？",
        "expected_success": 0.70
      }
    ],
    "pro_tips": [
      "建议先从较小订单开始谈，成功后再扩大",
      "避免在订单旺季议价，成功率较低",
      "强调付款及时性作为谈判筹码"
    ]
  }
}
```

### 成本核算响应
```json
{
  "success": true,
  "skill": "price-analysis",
  "data": {
    "product": "智能LED发光瑜伽垫",
    "order_quantity": 500,
    "unit_price": 11.20,
    "cost_breakdown": {
      "fob_yiwu": 5600.00,
      "domestic_freight": 150.00,
      "inspection_fee": 100.00,
      "customs_clearance": 80.00,
      "sea_freight_20gp": 450.00,
      "destination_port_charges": 120.00,
      "cif_total": 6500.00,
      "duty_rate": 0.07,
      "import_duty": 455.00,
      "total_cost": 6955.00,
      "cost_per_unit": 13.91
    },
    "selling_price_recommendation": {
      "amazon_fees": {
        "referral_fee_rate": 0.15,
        "fulfillment_fee": 3.50
      },
      "recommended_prices": {
        "retail_price": 29.99,
        "profit_margin": "28.5%",
        "break_even": 18.50
      }
    }
  }
}
```

## 异常处理

### 异常1: 价格数据不足
```
判断: 历史报价<5条 或 供应商<3家
处理:
  1. 标注"数据样本不足，分析结果仅供参考"
  2. 提供价格范围而非精确分析
  3. 建议用户多获取几家报价
```

### 异常2: 价格异常波动
```
判断: 30天波动>20% 或 趋势异常
处理:
  1. 识别并标注异常点
  2. 尝试分析波动原因(原材料/汇率/政策)
  3. 提示用户关注风险
  4. 提高置信度标注
```

### 异常3: 议价空间有限
```
判断: 当前价格已接近成本底线
处理:
  1. 诚实告知议价空间较小
  2. 建议从其他维度争取优惠(交期/付款/服务)
  3. 提供替代方案(降低配置/换供应商)
```

## 示例

### 示例1: 商品价格查询
```
用户: "这款LED瑜伽垫现在什么价位？"
系统:
  1. 查询市场价格区间
  2. 计算百分位排名
  3. 分析趋势走向
  4. 输出完整价格分析报告
```

### 示例2: 批量询价
```
用户: "我要1000个，能便宜多少？"
系统:
  1. 查询阶梯价格表
  2. 计算折扣幅度
  3. 与供应商协商可能
  4. 输出最优报价方案
```

### 示例3: 砍价请求
```
用户: "太贵了，帮我砍砍价"
系统:
  1. 分析当前议价空间
  2. 生成3套谈判策略
  3. 提供具体话术建议
  4. 评估成功概率
```

### 示例4: 成本利润计算
```
用户: "算算我卖这个能赚多少"
系统:
  1. 收集采购和物流成本
  2. 计算各项费用
  3. 推荐售价区间
  4. 输出利润分析报告
```
