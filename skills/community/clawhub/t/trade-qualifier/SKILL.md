---
name: trade-qualifier
version: 1.0.0
description: B2B外贸客户筛选技能 - 6维度深度评估 + A/B/C/D智能分级
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: 📊
---

# Trade Qualifier - B2B客户深度评分

## 功能
- 6维度深度评估（规模/匹配/采购力/信用/增长/风险）
- A/B/C/D智能分级
- 雷达图+漏斗可视化输出
- 支持自定义权重配置

## 触发条件

当用户需要：
- 对客户列表进行评分
- 筛选高价值目标客户
- 评估客户优先级
- 查看客户多维度分析

## 使用方法

### 基本用法

```
用户: 帮我评分这20家客户
技能: 调用trade-qualifier评估并返回分级结果
```

### 权重配置

```javascript
{
  weights: {
    scale: 0.20,      // 公司规模
    match: 0.25,      // 产品匹配
    purchasing: 0.20, // 采购力
    credit: 0.15,     // 信用评级
    growth: 0.15,     // 增长潜力
    risk: 0.05        // 合规风险
  }
}
```

## 输出格式

```json
{
  "success": true,
  "grades": {
    "A": { "count": 8, "minScore": 80, "companies": [...] },
    "B": { "count": 10, "minScore": 70, "companies": [...] },
    "C": { "count": 2, "minScore": 60, "companies": [...] },
    "D": { "count": 0, "minScore": 0, "companies": [] }
  }
}
```

## 闭环生态

Trade Qualifier 是外贸获客4技能闭环的第二环：
- **trade-hunter** 🔍 → 客户发现
- **trade-qualifier** 📊 → 客户筛选
- **trade-closer** ✉️ → 开发信生成
- **trade-dashboard** 📈 → 数据看板
