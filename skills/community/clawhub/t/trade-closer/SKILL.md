---
name: trade-closer
version: 1.0.0
description: B2B外贸开发信生成技能 - 3种邮件模板 + A/B主题行测试 + 多语言支持
metadata:
  openclaw:
    requires:
      bins:
        - curl
    emoji: ✉️
---

# Trade Closer - B2B外贸开发信生成

## 功能
- 3种邮件模板（直接型/故事型/价值型）
- A/B主题行测试（5个变体）
- 多语言支持（en/es/fr/de）
- 7天触达计划自动生成
- 邮件预览+A/B对比可视化

## 触发条件

当用户需要：
- 为客户生成开发信
- 撰写外贸邮件
- 创建A/B测试主题行
- 制定邮件触达计划

## 使用方法

### 基本用法

```
用户: 为Ferguson生成一封开发信
技能: 调用trade-closer生成个性化邮件
```

### 参数配置

```javascript
{
  company: "Ferguson",
  template: "direct",    // direct | story | value
  language: "en",       // en | es | fr | de
  subjectVariants: 5     // A/B测试数量
}
```

## 邮件模板

### 直接型 (Direct)
适用于已了解竞品的客户，开门见山直击要点

### 故事型 (Story)
适用于决策链长的客户，通过案例建立信任

### 价值型 (Value)
适用于注重ROI的采购者，数据驱动说服

## 7天触达计划

| Day | 内容 | 目的 |
|-----|------|------|
| 1 | 首次邮件 | 引起注意 |
| 2 | 价值内容 | 提供干货 |
| 4 | 案例分享 | 社会证明 |
| 6 | 限时优惠 | 紧迫感 |
| 7 | 最后提醒 | 促使行动 |

## 闭环生态

Trade Closer 是外贸获客4技能闭环的第三环：
- **trade-hunter** 🔍 → 客户发现
- **trade-qualifier** 📊 → 客户筛选
- **trade-closer** ✉️ → 开发信生成
- **trade-dashboard** 📈 → 数据看板
