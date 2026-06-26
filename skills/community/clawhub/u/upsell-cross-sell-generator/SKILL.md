---
name: upsell-cross-sell-generator
description: Generate upsell and cross-sell ideas for ecommerce funnels based on product fit, timing, and margin logic. Use when teams want more relevant order expansion offers.
---

# Upsell Cross Sell Generator

加购不是乱推商品，而是在对的时机给出更顺的下一步。

## 解决的问题

很多 upsell / cross-sell 模块的问题是：
- 推荐看起来随机；
- 用户还没理解主商品，就被迫加购；
- 明明有关联商品，但没有按购买阶段放对位置；
- 提高了客单价，却伤害了转化率。

这个 skill 的目标是：
**根据商品关系、购买阶段和利润逻辑，生成更自然的 upsell / cross-sell 方案。**

## 何时使用

- 想提升客单价；
- 想优化 PDP / cart / checkout / post-purchase 的推荐模块；
- 想减少“乱推荐”造成的干扰感。

## 输入要求

- 核心商品
- 可搭配商品列表
- 价格与利润信息
- 用户当前所处阶段（浏览 / 下单 / 购买后）
- 可选：库存、促销规则、平台限制

## 工作流

1. 判断哪些商品适合做 upsell，哪些适合做 cross-sell。
2. 匹配不同阶段的推荐位置。
3. 检查推荐是否有清晰的购买理由。
4. 输出简短的话术和 placement 建议。

## 输出格式

1. 推荐项列表
2. Placement 建议
3. 推荐理由
4. 风险提示

## 质量标准

- 推荐必须和主商品有明确关系。
- 位置建议要符合用户当前阶段。
- 不让推荐显得硬推销。
- 输出要可直接进商品页或购物车模块。

## 资源

参考 `references/output-template.md`。
