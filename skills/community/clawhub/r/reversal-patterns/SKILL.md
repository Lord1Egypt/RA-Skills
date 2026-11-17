---
name: reversal-patterns
description: |
  当用户在图上看到或怀疑头肩形、双重顶/底、三重顶/底、圆顶圆底、V 形等"价格图案"并想据此判断趋势反转时激活。
  重点是形态的"完成条件"（必须先有趋势 + 颈线/关键位突破 + 量能验证），而非看见类似形状就行动。
  不适用于：持续形态（转 continuation-patterns）、通用支撑阻挡线（转 trend-tools）。
  关键 trigger 词：头肩顶/底、双重顶双重底、三重顶、圆底、V形反转、形态完成、颈线突破。

  Activate when the user sees or suspects head-and-shoulders, double top/bottom, triple top/bottom, rounding, or V shapes on the chart and wants to judge trend reversal. Focus is on the "completion conditions" (must have a prior trend + neckline/key-level breakout + volume confirmation), not acting on a merely similar shape.
  Not applicable: continuation patterns (-> continuation-patterns), generic support/resistance (-> trend-tools).
  Key trigger words: head-and-shoulders top/bottom, double top/bottom, triple top, rounding bottom, V reversal, pattern completion, neckline breakout.

source_book: 《期货市场技术分析》 约翰·墨菲
source_chapter: 第五章 主要反转形态
tags: [head-and-shoulders, double-top, reversal, pattern, neckline]
related_skills:
  - slug: trend-tools
    relation: depends-on
  - slug: continuation-patterns
    relation: contrasts-with
  - slug: volume-open-interest
    relation: composes-with
---

# 主要反转形态：头肩 / 双重顶底 / 三重 / 圆底 / V 形

## R — 原文 (Reading)

> "头肩形是最著名、最可靠的主要反转形态，由左肩、头部、右肩及颈线组成；当价格跌破（升势中）或突破（跌势中）颈线，并伴以交易量验证，形态完成。"
> "双重顶这个术语被大大地滥用了……大多数潜在的双重顶演化得面目全非。"
> "V 形反转……极难判别。"
>
> — 约翰·墨菲，第五章 主要反转形态

---

## I — 方法论骨架 (Interpretation)

反转形态回答"趋势是不是到头了"。先掌握**共同要领**，再识别具体图案：

1. **共同要领（前置条件）**：①形态事前**必须已有明确趋势**；②需**趋势线/颈线突破**来确认；③**规模越大，后续动作越大**。没有这三条，看见类似形状也不算数。
2. **头肩形**（最可靠）：左肩—头—右肩，成交量随右肩递减；**颈线突破+回抽确认+放量**才算完成，目标位=头到颈线垂直距离投影。
3. **双重顶/底、三重顶/底**：前高/前低天然有阻挡，但"阻挡≠反转"；必须等颈线（中间谷/峰）被有效突破。三重比双重更可靠。
4. **圆底/圆顶**：罕见，圆底偏市场大底（作者经验）；演化缓慢。
5. **V 形**：无渐进过程，**极难用常规工具提前捕捉**，均线因滞后也无助；只能事后确认。

**纪律**：没有百发百中的形态（ce10）；流产形态（未完成即失效）要及时摆脱亏损头寸（ce19）。

---

## A1 — 书中的应用 (Past Application)

### 案例 1：小麦 1964–1972 头肩底
- **问题**：如何确认长期大底？
- **方法论的使用**：小麦构筑清晰头肩底，颈线突破后走出长期上涨。
- **结论**：头肩形态在长期图表上同样可靠，信号可用。
- **结果**：验证头肩底作为大级别底部反转。

### 案例 2：玉米/铜双重顶相距七年
- **问题**：双重顶只在短期出现吗？
- **方法论的使用**：玉米、铜的两个双重顶相隔达七年，长期图表依然成立。
- **结论**：反转形态不依赖时间尺度，勿因跨度大而忽视。
- **结果**：形态跨周期有效。

### 案例 3：圆底是市场底部（作者经验）
- **问题**：罕见形态怎么用？
- **方法论的使用**：作者凭经验指出圆底虽少，一旦出现常标示大底。
- **结论**：圆底偏底部识别，用于底端而非顶端。
- **结果**：补充经验性判别。

---

## A2 — 触发场景 (Future Trigger) ★

### 用户会在什么情境下需要这个 skill?
1. 图上出现疑似头肩/双顶，问"是不是要反转了、能不能反手"。
2. 问"双重顶是不是成立了"。
3. 问"形态完成没有、目标位到哪"。
4. 看到快速 V 形，问"是不是反转"。

### 语言信号
- "头肩顶/底、双重顶、三重顶"
- "这个形态是不是完成了 / 颈线突破了"
- "圆底、V形反转"
- "形态目标位怎么算"

### 与相邻 skill 的区分
- 与 `trend-tools` 的区别：trend-tools 是通用线/位，本 skill 是完整图案识别与完成判定。
- 与 `continuation-patterns` 的区别：本 skill 是"反转"（趋势掉头），continuation 是"中途歇脚继续原趋势"。

---

## E — 可执行步骤 (Execution)

1. **确认前置**：当前是否已有明确趋势？无趋势则形态无意义。
   - 完成标准：先有趋势 + 规模足够。
2. **识别图案**：判断是头肩/双顶/三重/圆底/V形哪种。
   - 完成标准：对照构件（肩/头/颈线或双峰/谷）。
3. **等突破确认**：必须颈线/关键位被**有效突破**（常伴放量）。
   - 完成标准：收市突破+回抽不破。判停：未突破前只观察，不下反转单。
4. **测算目标**：头肩用头-颈线垂直距离投影；双顶用形态高度。
   - 完成标准：给出至少一档目标位。

---

## B — 边界 (Boundary) ★

### 不要在以下情况使用此 skill
- 用户在看三角形/旗形等"中途歇脚"图案 → 转 continuation-patterns。
- 用户只问通用支撑位 → 转 trend-tools。

### 作者在书中警告的失败模式
- **双重顶被滥用**（ce11）：一见接近前高就喊双顶做空，多数继续新高；必须等颈线跌破。
- **无形态百发百中**（ce10）：形态是概率，流产形态要果断止损。
- **牛市陷阱**（ce12）：假突破追反被套，须收盘确认+量能过滤。
- **V 形极难判别**（ce13）：常规工具滞后，勿强求提前捕捉。

### 作者的盲点 / 时代局限
- 形态识别含主观；现代算法形态识别可辅助，但"完成判定"仍需人工确认。

### 容易混淆的邻近方法论
- 双顶的"前高阻挡"≠反转（ce11）；勿与 trend-tools 的普通阻挡混淆。

---

## 相关 skills
- depends-on: trend-tools
- contrasts-with: continuation-patterns
- composes-with: volume-open-interest

---

## 审计信息
- **验证通过**: V1 ✓ / V2 ✓ / V3 ✓
- **测试通过率**: 100% (6/6, Stage4 盲测)
- **蒸馏时间**: 2026-08-03
