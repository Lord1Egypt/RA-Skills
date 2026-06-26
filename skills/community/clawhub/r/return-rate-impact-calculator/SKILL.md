---
name: return-rate-impact-calculator
description: Calculate how return rate affects ecommerce profit, CAC tolerance, and operational risk. Use when teams need to see how refunds and reverse logistics change real margin.
---

# Return Rate Impact Calculator

退货率不是售后指标而已，它会直接吞掉利润、预算空间和增长判断。

## 先交互，再计算

开始时先问：
1. 你们要看的 return 是：
   - 退款率
   - 退货率
   - 退款+退货综合
2. 你们平时 return impact 的口径里包含哪些损失？
   - 收入回吐
   - 逆向物流
   - 包材
   - 二次销售损耗
   - 客服成本
3. 产品是否可以二次售卖？恢复率是多少？
4. 要沿用现有逻辑，还是让我给推荐框架？

## Python script guidance

当用户给出结构化输入后：
- 生成 Python 脚本计算退货影响
- 展示 revenue loss 与 extra cost loss
- 输出调整后利润与 CAC 容忍度
- 返回可复用脚本

## 解决的问题

很多团队会盯 GMV、ROAS、AOV，但忽略了一个事实：
- 退货率一高，营收并不等于可保留营收；
- 售后、逆向物流、二次包装和损耗会继续吃利润；
- 表面上投放还能跑，实际可承受的 CAC 已经变低。

这个 skill 的目标是：
**把 return rate 对利润和经营阈值的影响算清楚，避免用“未扣退货”的假象做决策。**

## 何时使用

- 某个 SKU 退款率明显偏高；
- 想知道高退货类目是否还能继续放量；
- 评估政策、文案、尺码说明、预期管理是否要调整。

## 输入要求

- 订单量 / 销售额
- 售价与毛利
- 当前退货率 / 退款率
- 逆向物流、处理费、二次销售损耗
- 退款政策与是否可二次售卖
- 可选：获客成本、仓储和额外客服成本

## 工作流

1. 明确 return impact 的口径。
2. 计算未考虑退货时的基础利润。
3. 计算退货带来的收入回吐和成本拖累。
4. 估算调整后的净利润与可承受 CAC。
5. 标记风险区间和优先修复动作。
6. 返回可复用 Python 脚本。

## 输出格式

1. 核心假设表
2. 退货影响拆解
3. 调整后利润 / 阈值
4. 风险提醒与建议动作
5. Python 脚本

## 质量标准

- 明确区分营收损失和额外成本损失。
- 输出对经营有用的阈值，而不只是一个百分比。
- 清楚说明哪些是假设值。
- 优先指出最值得修的环节。
- 未确认口径前不假装精确。

## 资源

参考 `references/output-template.md`。
