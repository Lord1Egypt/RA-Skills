---
name: trade-hunter
version: 1.0.0
description: B2B外贸客户发现技能 - 全球企业数据采集 + BOI评分初筛
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: 🔍
---

# Trade Hunter - B2B外贸客户发现

## 功能
- 全球B2B企业数据采集
- BOI(Business Opportunity Index)评分初筛
- 按行业/地区/营收精准筛选
- 一键生成客户发现报告+交互式地图可视化

## 触发条件

当用户需要：
- 寻找新的目标客户
- 搜索特定行业的企业
- 发现潜在B2B客户
- 获取客户联系信息
- 生成客户分布地图

## 使用方法

### 基本用法

```
用户: 帮我找美国花洒批发商
技能: 调用trade-hunter搜索并返回结果
```

### 高级参数

```javascript
{
  keywords: ["shower head", "bathroom fixtures"],  // 搜索关键词
  location: "USA",                                  // 地区
  revenueMin: "$10M",                               // 最小营收
  limit: 20,                                        // 返回数量
  includeContact: true                              // 是否包含联系方式
}
```

## 输出格式

```json
{
  "success": true,
  "data": [
    {
      "name": "公司名",
      "city": "城市",
      "state": "州",
      "industry": "行业",
      "revenue": "营收",
      "contact": "邮箱",
      "boiScore": 85
    }
  ],
  "summary": {
    "total": 20,
    "highValue": 8
  }
}
```

## 闭环生态

Trade Hunter 是外贸获客4技能闭环的第一环：
- **trade-hunter** 🔍 → 客户发现
- **trade-qualifier** 📊 → 客户筛选
- **trade-closer** ✉️ → 开发信生成
- **trade-dashboard** 📈 → 数据看板

## 注意事项

1. 数据来源为公开商业信息
2. 已进行PII脱敏处理
3. 遵守目标市场法规
