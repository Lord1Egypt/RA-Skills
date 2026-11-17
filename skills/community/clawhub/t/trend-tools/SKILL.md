---
name: trend-tools
description: |
  当用户要在图上识别并利用支撑与阻挡（含角色互换）、绘制/判定趋势线与管道线、用百分比回撤找加仓区、
  理解速度线/扇形原理、或识别价格跳空与反转日时激活。这是全书最高频、最落地的工具集。
  不适用于：判断宏观趋势层级（转 dow-theory-framework）、识别头肩等特定形态（转 reversal-patterns）。
  关键 trigger 词：支撑位阻力位、趋势线怎么画、跌破趋势线、50%回撤、跳空、反转日、扇形。

  Activate when the user wants to identify and use support & resistance (incl. role reversal), draw/judge trendlines and channels, use percentage retracement for add-zones, understand speed lines/fan principle, or identify price gaps and reversal days. This is the highest-frequency, most practical toolset in the book.
  Not applicable: judging macro trend hierarchy (-> dow-theory-framework), identifying specific patterns like head-and-shoulders (-> reversal-patterns).
  Key trigger words: support/resistance, how to draw trendline, break below trendline, 50% retracement, gap, reversal day, fan.

source_book: 《期货市场技术分析》 约翰·墨菲
source_chapter: 第四章 趋势的基本概念
tags: [support-resistance, trendline, channel, retracement, gap, reversal-day]
related_skills:
  - slug: dow-theory-framework
    relation: depends-on
  - slug: reversal-patterns
    relation: composes-with
  - slug: volume-open-interest
    relation: composes-with
---

# 趋势工具集：支撑阻挡 / 趋势线 / 回撤 / 跳空 / 反转日

## R — 原文 (Reading)

> "支撑水平被突破后，就演化为阻挡水平；阻挡被突破后，演化为支撑水平。"
> "在上升趋势中，我们沿着相继的依次抬高的低点作出一条直线……这条直线就是趋势线。"
> "市场通常按照一定的可预知的百分比例回撤——最熟悉的是 33%、50%、67%。"
>
> — 约翰·墨菲，第四章 趋势的基本概念

---

## I — 方法论骨架 (Interpretation)

这是把"趋势"从概念变成可操作价位的工具箱，六件套：

1. **支撑与阻挡**：前期密集成交区对后续价格形成"地板/天花板"。**角色互换**是核心反直觉机制——旧阻挡破位后变新支撑，旧支撑跌破后变新阻挡。触及次数越多、伴随成交量、时间跨度越长，越可靠。整数关（习惯数）天然云集挂单。
2. **趋势线**：连接依次抬高/降低的极点。被触及次数越多、坡度越平缓越可靠；**突破（配合 3% 或 2 天过滤）是趋势可能生变的早期信号**。
3. **管道线**：平行于趋势线连接反侧显著点，上轨常作价格目标。
4. **百分比回撤**：调整常回撤前波幅的 1/3~2/3，**50% 最关键**，用于找顺势加仓区。
5. **速度线 / 扇形**：第三条趋势线被破常标志反转；45°线（1×1）代表价时均衡。
6. **跳空与反转日**：跳空分突破/中继/衰竭/普通四类（衰竭=尾声预警）；反转日须"创新高/低+收市价回落/升破前收"，是单根 K 线预警，需后续确认。

---

## A1 — 书中的应用 (Past Application)

### 案例 1：活牛期货 35/56 阻挡转支撑
- **问题**：旧压制位突破后还有没有用？
- **方法论的使用**：活牛期货历史上 35、56 两个阻挡水平，向上突破后都转化为后续回撤的支撑。
- **结论**：**角色互换**规律在真实长期图表上成立。
- **结果**：验证了"旧阻挡=新支撑"的可操作性。

### 案例 2：黄金 400 整数关三次阻挡
- **问题**：整数关是不是真有支撑阻挡作用？
- **方法论的使用**：黄金 400 美元在熊市中三次阻挡上行，跌破后跌向 300 支撑区。
- **结论**：习惯数（整数关）是心理密集区，止损应挂在习惯数稍外。
- **结果**：支撑阻挡+习惯数的实战用法。

### 案例 3：糖/黄金在 2/3 回撤位转折
- **问题**：回撤到哪里算"到位"？
- **方法论的使用**：糖与黄金常在 2/3（66%）回撤位附近转折。
- **结论**：最大回撤 2/3 是强支撑/阻挡参考。
- **结果**：百分比回撤法落地。

---

## A2 — 触发场景 (Future Trigger) ★

### 用户会在什么情境下需要这个 skill?
1. 问"这个价位能不能买/是不是支撑位"。
2. 问"趋势线怎么画、跌破趋势线意味着什么"。
3. 问"回调到哪可以加仓"（回撤比例）。
4. 看到"跳空 / 某天反转"想知道含义。

### 语言信号
- "支撑位 / 阻力位 / 这个位置能不能买"
- "趋势线怎么画、跌破趋势线"
- "回调到 50% 能不能加仓"
- "跳空 / 反转日 / 扇形"

### 与相邻 skill 的区分
- 与 `dow-theory-framework` 的区别：dow 管"趋势层级与验证"，本 skill 管"具体画线价位"。
- 与 `reversal-patterns` 的区别：本 skill 是通用线/位工具，形态（头肩等）是特定图案，归 reversal。

---

## E — 可执行步骤 (Execution)

1. **标支撑阻挡**
   - 完成标准：找到近期密集成交区/前高前低，标出水平线并应用角色互换预期。
2. **画趋势线**
   - 完成标准：连接≥2 个极点，等第三点验证；用 3%/2 天过滤伪突破。
3. **算回撤区**
   - 完成标准：取前波幅的 1/3、1/2、2/3 作潜在加仓/目标区。
4. **判跳空/反转日类型**
   - 完成标准：区分突破/中继/衰竭；单日反转需收市确认，不单独判趋势终结。

---

## B — 边界 (Boundary) ★

### 不要在以下情况使用此 skill
- 用户问宏观牛熊层级 → 转 dow-theory-framework。
- 用户问头肩/双顶等完整图案 → 转 reversal-patterns。

### 作者在书中警告的失败模式
- **趋势线主观性**（ce08）：画法带主观，需至少三点验证，避免单点连线即下结论。
- **过滤器两难**（ce07）：过滤太小拉锯不减、太大错过初始动作，须匹配场景。
- **反转非突如其来**（ce09）：主要反转多酝酿，勿把单根 K 线当反转。

### 作者的盲点 / 时代局限
- 角色互换在高度操纵/流动性骤变时可能失效（见 ta-philosophy 边界）。

### 容易混淆的邻近方法论
- 反转日≠趋势反转：单日信号只是预警，须后续确认（区别于 reversal-patterns 的 completed 形态）。

---

## 相关 skills
- depends-on: dow-theory-framework
- composes-with: reversal-patterns
- composes-with: volume-open-interest

---

## 审计信息
- **验证通过**: V1 ✓ / V2 ✓ / V3 ✓
- **测试通过率**: 100% (6/6, Stage4 盲测)
- **蒸馏时间**: 2026-08-03
