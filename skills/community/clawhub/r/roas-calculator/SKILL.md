---
name: roas-calculator
description: Evaluate ad ROAS against ecommerce margin reality, not just attributed revenue. Use when teams need a fast scale/hold/cut decision on paid traffic.
---

# ROAS Calculator (Ads)

ROAS 看起来高，不代表这笔广告真的值得放大。

## 先交互，再计算

这个 skill 不应该一上来就直接给结果。

开始时先问清楚：
1. 你想用什么口径看 ROAS？
   - 平台归因收入？
   - 扣退款后的净收入？
   - 扣掉折扣后的有效收入？
2. 你们平时怎么计算 break-even ROAS？
3. 你是想用你们现有口径，还是让我给一个推荐的电商计算框架？
4. 是否要把履约、客服、创意成本、渠道费算进去？

如果用户没有成熟口径，先给推荐框架，再让用户确认。

## Python script guidance

当用户提供了结构化数字后：
- 生成 Python 脚本做计算
- 先展示假设和公式
- 再输出结果
- 最后返回可复用脚本

如果数字不完整：
- 不要硬算
- 继续追问缺失变量
- 或给出推荐默认值并等待用户确认

## 解决的问题

很多团队看到广告回收就会加预算，但忽略了：
- 折扣、退款、物流和手续费会侵蚀可保留收入；
- 平台归因很好看，不等于真实利润好看；
- 一条广告 ROAS 够不够，不是看行业平均，而是看你的 unit economics。

这个 skill 的目标是：
**把 ROAS 放回真实电商利润语境里，给出 scale / hold / cut 的判断。**

## 何时使用

- 准备放大预算前；
- 广告表现看起来不错，但利润不确定；
- 团队需要统一 break-even ROAS 口径。

## 输入要求

- 广告花费
- 归因收入
- 毛利 / 成本结构
- 折扣与优惠
- 退款率 / 退货影响
- 可选：渠道费、创意成本、客服成本

## 工作流

1. 明确用户采用的 ROAS 与利润口径。
2. 计算名义 ROAS。
3. 根据利润结构估算 break-even ROAS。
4. 根据退款和折扣校正有效收入。
5. 给出是否可放量的建议。
6. 输出可复用 Python 脚本。

## 输出格式

1. 假设表
2. ROAS 结果
3. Break-even 对照
4. 建议动作
5. Python 脚本

## 质量标准

- 不只汇报 ROAS 数字，要解释够不够。
- 明确指出归因和真实利润的差距。
- 输出要能直接支持预算决策。
- 清楚标注估算项。
- 未确认口径前不要假装精确。

## 资源

参考 `references/output-template.md`。
