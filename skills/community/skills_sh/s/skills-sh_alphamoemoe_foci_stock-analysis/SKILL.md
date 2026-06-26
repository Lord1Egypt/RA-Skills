---
name: stock-analysis
description: Generate a comprehensive sentiment analysis report for a single stock. Use when users want deep analysis of a specific ticker like NVDA, TSLA, or AAPL.
---

# Comprehensive Stock Analysis

Generate a complete sentiment analysis report for a single stock.

## Triggers

- "分析 NVDA"
- "NVDA 怎么样"
- "analyze TSLA"
- "what about AAPL"
- "帮我看看 AMD"
- `/stock-analysis NVDA`
- `/stock-analysis {ticker}`

## Arguments

- `ticker` - Stock ticker to analyze (required)

## Instructions

When the user wants a comprehensive analysis of a stock, follow these steps:

1. **Get Sentiment Data**
   Call `get_ticker_sentiment(ticker)` to get overall sentiment and breakdown by blogger.

2. **Search Related Viewpoints**
   Call `search_viewpoints(ticker)` to find all detailed opinions.

3. **Find Who Holds It**
   Call `get_blogger_positions` for bloggers who mentioned the stock to understand their conviction level.

4. **Compile Analysis**
   Create a comprehensive report covering:
   - Overall sentiment score
   - Bull vs bear breakdown
   - Key arguments from both sides
   - Notable bloggers with positions
   - Risk factors mentioned

5. **Present Results**
   Format the output as:

   ```
   ## TICKER 综合分析报告

   ### 情绪概览

   | 指标 | 数值 |
   |------|------|
   | 整体情绪 | 🟢 看涨 (X/10) |
   | 看涨博主 | X 位 |
   | 看跌博主 | X 位 |
   | 中性/观望 | X 位 |
   | 总提及次数 | XX |

   ### 多方观点 🐂

   **核心论点:**
   1. [论点1] — 博主A (XX万粉丝)
   2. [论点2] — 博主B
   3. [论点3] — 博主C

   **代表观点:**
   > "[详细观点引用]"
   > — 博主A, 2025-01-20

   ### 空方观点 🐻

   **核心论点:**
   1. [论点1] — 博主D
   2. [论点2] — 博主E

   **代表观点:**
   > "[详细观点引用]"
   > — 博主D, 2025-01-19

   ### 持仓博主

   | 博主 | 态度 | 持仓情况 |
   |------|------|----------|
   | 博主A | 看涨 | 重仓 |
   | 博主B | 观望 | 轻仓 |

   ### 风险提示 ⚠️

   - [风险1]: [描述]
   - [风险2]: [描述]

   ### 总结
   [客观总结各方观点，不做买卖建议]
   ```

## Tool Sequence

1. `get_ticker_sentiment(ticker)` → Get sentiment breakdown
2. `search_viewpoints(ticker)` → Get detailed viewpoints
3. `list_bloggers` → Get blogger info (if needed for context)
4. `get_blogger_positions(blogger)` → For key bloggers mentioning the stock
5. Compile comprehensive report

## Notes

- Present all viewpoints fairly, both bull and bear
- Include specific quotes when available
- Do NOT give buy/sell recommendations
- Highlight consensus and divergence
- Note the recency of viewpoints
