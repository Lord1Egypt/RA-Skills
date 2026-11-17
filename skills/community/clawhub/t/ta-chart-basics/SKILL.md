---
name: ta-chart-basics
description: |
  当用户需要读懂或亲手绘制金融/期货图表、选择时间尺度（日/周/月/日内）、区分线图/点数图/单线图、
  或在算术刻度与对数刻度之间做选择、理解交易量/持仓兴趣如何在图上呈现时激活。
  不适用于：已会读图只想做买卖决策（转 trend-tools / 形态类 skill）、纯基本面分析。
  关键 trigger 词：怎么看K线/图表、蜡烛图、十字星、K线形态、日线周线月线、算术刻度对数刻度、如何作图。

  Activate when the user needs to read or draw financial/futures charts, choose time scale (daily/weekly/monthly/intraday), distinguish line/P&F/single-line charts, choose between arithmetic and logarithmic scales, or understand how volume/open-interest appear on charts.
  Not applicable: already able to read charts and only wants buy/sell decisions (-> trend-tools / pattern skills), pure fundamental analysis.
  Key trigger words: how to read candlestick/chart, candlestick, doji, K-line pattern, daily/weekly/monthly, arithmetic/log scale, how to plot.

source_book: 《期货市场技术分析》 约翰·墨菲
source_chapter: 第三章 图表简介
tags: [chart, line-chart, point-figure, scale, volume, foundation]
related_skills:
  - slug: ta-philosophy
    relation: depends-on
  - slug: trend-tools
    relation: composes-with
  - slug: point-figure
    relation: contrasts-with
---

# 图表基础：如何读图与作图

## R — 原文 (Reading)

> "在期货行业中，所有商业化图表的价格轴都是以算术刻度表示的，不过，在进行某些形式的分析，特别是在研究非常长期的趋势时，使用对数刻度图表可能更为便利。"
> "日线图的作法非常简易……竖直轴代表合约的价格，水平轴记录对应的时间项……在线段上从当日收市价格的位置向右引出一小截线头，日线图就画成了。"
>
> — 约翰·墨菲，第三章 图表简介

---

## I — 方法论骨架 (Interpretation)

技术分析的所有工具都建立在一张图之上。读懂图，是后续一切的前提。核心有四点：

1. **三类图表**：线图（竖直线段=当日最高-最低，右短线=收市价）最通用；单线图只连收市价，更简洁；点数图（P&F）忽略时间、只记价格转向，擅长显支撑阻挡。**线图是默认起点**。
2. **时间尺度可伸缩**：日线看 6–9 个月；周线/月线看长期主趋势（可回溯 5–20 年）；日内图（5 分钟/小时）用于精确择时。同一套原理在所有尺度通用。
3. **算术 vs 对数刻度**：算术刻度每单位等距（5→10 与 50→55 视觉相同）；对数刻度等距=等百分比（10→20 与 20→40 相同）。**长期趋势、价格跨度大时用对数**，短期用算术。
4. **量与持仓的画法**：交易量画在价格下方竖直线段（当日轻重）；持仓兴趣画成沿图下沿的实线（单边未平仓存量，非流量）。

读图顺序的铁律：**先长期后短期**（月→周→日→日内），不要拿长期图直接发交易指令。

---

## A1 — 书中的应用 (Past Application)

### 案例 1：从报纸数据补绘日线图
- **问题**：作者说明散户如何把《华尔街日报》期货版的数据变成可用图表。
- **方法论的使用**：报纸每行给出某合约的开/高/低/结算价与个别持仓兴趣；先画价格线段+收市短线，再把当日总交易量与总持仓兴趣画在下方。
- **结论**：每天不到半小时即可刷新整个投资组合的图表，把时间留给"研究图"而非"画新图"。
- **结果**：作者主张订阅商业化图表服务更划算、准确，但自绘也能完成。

### 案例 2：周线/月线纵览长期
- **问题**：日线只能看 6–9 个月，如何判断数年级主趋势？
- **方法论的使用**：把连续合约片断接续成连续周线/月线图，浓缩价格资料。
- **结论**：月线可覆盖 20 年以上，用于定主要趋势方向。
- **结果**：长期透视是全书"先宏观后微观"读图纪律的基石。

---

## A2 — 触发场景 (Future Trigger) ★

### 用户会在什么情境下需要这个 skill?
1. 刚接触技术分析，不知道"K线/线图怎么看、每个线段代表什么"。
2. 纠结"该看日线还是周线/月线"、或问"5分钟图怎么用"。
3. 在算术刻度与对数刻度之间不知如何选，或做长期分析时图看起来"失真"。
4. 想知道成交量、持仓兴趣在图上怎么画、代表什么。

### 语言信号（用户的话里出现这些就应激活）
- "这图怎么看 / 怎么画 K 线"
- "日线、周线、月线有什么区别，我该看哪个"
- "算术刻度和对数刻度选哪个"
- "成交量 / 持仓兴趣在图上怎么表示"

### 与相邻 skill 的区分
- 与 `ta-philosophy` 的区别：philosophy 讲"为什么信图表"，本 skill 讲"图表长什么样、怎么读"。
- 与 `trend-tools` 的区别：本 skill 只教"看图和选尺度"，不教支撑阻挡/趋势线等具体工具。

---

## E — 可执行步骤 (Execution)

1. **选图表类型**
   - 完成标准：确认用线图（默认）还是点数图（只看价格转向时用）。
2. **选时间尺度**
   - 完成标准：定主趋势用周/月线；定策略用日线；精确择时用日内图。**判停**：若用户只想定方向，停在周/月线即可，不继续下钻。
3. **选刻度**
   - 完成标准：短期/幅度小→算术；长期/跨度大→对数。
4. **叠加量能**
   - 完成标准：价格下方画出交易量线段、持仓兴趣实线，确认是"总额"而非单合约。

---

## B — 边界 (Boundary) ★

### 不要在以下情况使用此 skill
- 用户已会读图、只是要做买卖决策 → 转 trend-tools / reversal-patterns 等。
- 纯基本面/消息面分析 → 本 skill 不覆盖。

### 作者在书中警告的失败模式
- **长期图直接发交易指令**（ce18）：月/周线只定方向，不含精确入场点，越界到日内择时会过粗。
- **用单合约量能代替总额**（p23）：必须看全市场总交易量与总持仓兴趣，个别合约数据有到期失真。

### 作者的盲点 / 时代局限
- 书中图表均为纸媒手绘逻辑；现代软件已自动化，但"先长期后短期""用对数看长期"的原则不变。

### 容易混淆的邻近方法论
- 点数图（point-figure skill）是独立制图法，无时间轴；不要和线图混为一谈。

---

## 相关 skills
- depends-on: ta-philosophy
- composes-with: trend-tools
- contrasts-with: point-figure

---

## 审计信息
- **验证通过**: V1 ✓ / V2 ✓ / V3 ✓
- **测试通过率**: 100% (6/6, Stage4 盲测)
- **蒸馏时间**: 2026-08-03
