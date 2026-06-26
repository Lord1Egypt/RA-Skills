---
name: retail-deal-goods-profile-analysis
description: |
  成交商品画像分析工具。分析成交商品的品类、价格带、颜色、包型、上市时间等特征分布及环比变化。
  
  核心能力：
  1. 品类分布（女包/男包/钱包/配饰占比）
  2. 价格带分布（主销价格带、高客单占比）
  3. 包型分布（手提/斜挎/双肩/托特等）
  4. 颜色分布（黑色系/棕色系/红色等）
  5. 上市时间分布（新品/当季/老款占比）
  6. 环比变化分析（本期vs上期特征变化）
  
  触发条件：
  - 用户询问商品画像（如"成交商品有什么特征"）
  - 用户分析品类结构（如"什么品类卖得好"）
  - 用户需要价格带分析（如"主销价格带是多少"）
---

# 成交商品特征分析 Skill

## 功能

分析成交商品的品类、价格带、颜色、包型、上市时间等特征分布及环比变化。

## 使用

```python
from analyze import analyze as deal_profile_analyze

result = deal_profile_analyze(
    store_id="416759_1714379448487",
    from_date="2026-03-01",
    to_date="2026-03-26",
    store_name="正义路60号店"
)
```

## API

- `analyze(store_id, from_date, to_date, store_name)` - 主分析函数

## 数据源

`/api/v1/store/dashboard/bi`

## 输出

- 品类特征分布及环比
- 价格带特征分布及环比
- 包型特征分布及环比
- 颜色特征分布及环比
- 上市时间特征分布及环比
- 综合分析结论
