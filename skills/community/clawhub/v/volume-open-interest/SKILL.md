---
name: volume-open-interest
description: |
  当用户要用量能（交易量）与持仓兴趣来验证价格信号、判断趋势健康度，或理解胀爆/抛售高潮、交易商分类报告（COT）等时激活。
  核心是"价格第一、量能第二"，量能只是验证价格的旁证。
  不适用于：单纯画价格线（转 trend-tools）、摆动指数超买超卖（转 oscillators-contrarian）。
  关键 trigger 词：成交量验证、持仓兴趣、量价背离、突破量能、胀爆、抛售高潮、COT、交易商分类报告。

  Activate when the user wants to use volume and open interest to confirm price signals, judge trend health, or understand blowoffs/selling climaxes and the COT (commitments of traders) report. The core is "price first, volume second" - volume is only corroborating evidence.
  Not applicable: simply drawing price lines (-> trend-tools), oscillator overbought/oversold (-> oscillators-contrarian).
  Key trigger words: volume confirmation, open interest, volume-price divergence, breakout volume, blowoff, selling climax, COT, trader classification report.

source_book: 《期货市场技术分析》 约翰·墨菲
source_chapter: 第七章 交易量和持仓兴趣
tags: [volume, open-interest, confirmation, blowoff, cot]
related_skills:
  - slug: trend-tools
    relation: composes-with
  - slug: oscillators-contrarian
    relation: composes-with
---

# 量能验证：交易量 / 持仓兴趣

## R — 原文 (Reading)

> "价格、交易量、持仓兴趣三者之中，价格是最主要的，量能与持仓兴趣是次要的验证指标。"
> "在牛市中，不同寻常的高额持仓兴趣……是危险信号。"
> "胀爆（价格急冲+交易量增+持仓兴趣骤降）与抛售高潮（价格骤坠+交易量重+持仓兴趣降）警告大规模平仓、趋势将突变。"
>
> — 约翰·墨菲，第七章 交易量和持仓兴趣

---

## I — 方法论骨架 (Interpretation)

量能是价格的"证人"——它不预言，只确认。用法：

1. **权重 5/3/2**：价格第一，交易量第二，持仓兴趣第三。**量能只验证价格信号，绝不喧宾夺主**。
2. **量价配合**：健康趋势中，价涨量增、价跌量缩；反向调整量萎缩。背离（价涨量缩）是趋势衰竭警告。
3. **持仓兴趣四条规则**：价涨持仓增=新多强劲；价涨持仓减=空头回补（脆弱上涨）；价跌持仓增=新空强劲；价跌持仓减=多头离场。用来判断资金流入/流出。
4. **必须用总额**：只用全市场总交易量/总持仓兴趣，不用单合约（有到期失真）。
5. **季节性修正**：持仓兴趣随合约换月/作物年度波动，比较前先剔除季节。
6. **胀爆 / 抛售高潮**：趋势末端量能+持仓骤变，是能量耗尽、反转将至的警告。
7. **交易商分类报告（COT）**：商业套保者 vs 投机大众的持仓结构——商业净空+投机净多常是顶部先兆。

---

## A1 — 书中的应用 (Past Application)

### 案例 1：1980 商品见顶，高持仓兴趣预警
- **问题**：大顶怎么提前察觉？
- **方法论的使用**：1980 年底商品创纪录持仓兴趣，是顶部危险早期警告，随后五年下跌。
- **结论**：持仓兴趣异常高=拥挤交易，警惕反转。
- **结果**：验证持仓兴趣顶部的预警价值。

### 案例 2：1985 豆粕 COT 顶部先兆
- **问题**：如何用持仓结构判断顶部？
- **方法论的使用**：1985-01-18 豆粕商业净空庞大、投机净多庞大 → 即将下跌。
- **结论**：商业套保者反向持仓是相反意见式顶部信号。
- **结果**：豆粕此后下跌验证。

---

## A2 — 触发场景 (Future Trigger) ★

### 用户会在什么情境下需要这个 skill?
1. 问"放量上涨/缩量下跌意味着什么"。
2. 问"持仓兴趣增加是不是看好"。
3. 看到暴涨暴跌伴随天量，问"是不是到头了"（胀爆/抛售高潮）。
4. 问"COT/交易商分类报告怎么看"。

### 语言信号
- "成交量验证、量价背离"
- "持仓兴趣增加/减少说明什么"
- "胀爆、抛售高潮"
- "COT、交易商分类报告"

### 与相邻 skill 的区分
- 与 `trend-tools` 的区别：trend-tools 是价格线/位，本 skill 是量能验证维度。
- 与 `oscillators-contrarian` 的区别：本 skill 是真实成交量/持仓，osc 是数学摆动指标+情绪。

---

## E — 可执行步骤 (Execution)

1. **看价格信号先行**：先有价格信号（突破/形态），再用本 skill 验证。
   - 完成标准：不单独凭量能下方向结论。
2. **判量价配合**：上涨放量/下跌缩量=健康；背离=警告。
   - 完成标准：明确量价是否同向。
3. **读持仓兴趣**：用四条规则判断资金流入/流出，做季节性修正、用总额。
   - 完成标准：得出"新多/空回补/新空/多离场"之一。
4. **查极端量能**：出现胀爆/抛售高潮或异常高持仓 → 预警反转。
   - 完成标准：标记危险信号。判停：若极端量能出现，降低顺势加码意愿。

---

## B — 边界 (Boundary) ★

### 不要在以下情况使用此 skill
- 用户只问价格线/支撑阻挡 → 转 trend-tools。
- 用户问 RSI 超买超卖 → 转 oscillators-contrarian。

### 作者在书中警告的失败模式
- **期货量能不如股市**（ce17）：结算延迟、涨跌停扭曲 OBV，期货中量价权重应下调，不可照搬股市。
- **牛市异常高持仓是危险**（ce16）：拥挤交易，一旦转向易踩踏。
- **胀爆/抛售高潮处顺势加码**（ce15）：此处应警惕反转而非加仓。

### 作者的盲点 / 时代局限
- 1986 年无实时 COT/算法；现代 COT 数据更及时，但"商业 vs 投机"解读逻辑不变。

### 容易混淆的邻近方法论
- 持仓兴趣（存量）≠ 交易量（流量），混用会误读突破有效性（见 glossary g01）。

---

## 相关 skills
- composes-with: trend-tools
- composes-with: oscillators-contrarian

---

## 审计信息
- **验证通过**: V1 ✓ / V2 ✓ / V3 ✓
- **测试通过率**: 100% (6/6, Stage4 盲测)
- **蒸馏时间**: 2026-08-03
