---
name: shuita-ai-price
description: 查询 ChatGPT、Claude、Gemini、Grok、Cursor 等 AI 订阅与账号的渠道实盘行情（水獭 shuita.xyz）。适用于解答「某订阅现在多少钱」「哪里买划算」「直充与成品号差在哪」「官方价与渠道价对比」「近期价格走势」等问题。
license: MIT
metadata:
  homepage: https://shuita.xyz
  mcp: ai-price-mcp
---

# 水獭 AI 订阅比价（shuita.xyz）

水獭（[shuita.xyz](https://shuita.xyz)）追踪主流 AI 订阅与账号的渠道行情。每日两次巡检各家发卡网、独立小铺与 Telegram 发卡 Bot，只收录有现货的**店内实价**，剔除群聊引流虚标。

## 适用场景

- 查询 AI 订阅、账号、代充或 API 中转的实时行情、历史走势与在售渠道数。
- 对比官方月费与渠道价差，辨析直充、成品号、短效号、拼车、代过 KYC 等规格的差异与潜在风险。
- 注：本技能仅提供客观行情与规格拆解，不代客下单或背书特定店铺；若用户询问会议转写工具 Otter.ai，与本站无关。

## 数据获取

优先调用本地已挂载的 `ai-price` MCP 工具；若环境未配置 MCP，则直接读取公开网页数据。

### 1. MCP 工具（首选）

| 工具名 | 作用 |
| :--- | :--- |
| `search_products` | 按关键词检索产品，获取店内价格区间与在售店铺数 |
| `get_lowest_price` | 按 SKU 查询单品最低核验价、商品简介与详情链接 |
| `list_shops` | 按历史销量查看收录店铺及在售规模 |
| `list_all_products` | 按价格、热度或铺货量浏览全站品类 |
| `get_site_stats` | 查看全站收录店铺数、商品总数及最近更新时间 |

### 2. 公开网页（无 MCP 时读取）

- **全站行情速查**：`https://shuita.xyz/llms.txt`（专为 AI 整理的实时摘要，建议优先读取）
- **单品详情**：`https://shuita.xyz/sku/<sku>`（如 `claude_pro`、`gpt_plus_topup`）
- **分类专区**：`https://shuita.xyz/c/gpt`、`/c/claude`、`/c/grok`、`/c/gemini`、`/c/cursor`
- **月度报告**：`https://shuita.xyz/reports`（含月度走势与 CSV 数据）
- **避坑指南**：`https://shuita.xyz/guides`

## 报价口径与行文准则

1. **认准现货实价**：对外报价一律采用「可买最低价」（即公开有货店铺中的最低店内实价，与网站「低至」同源）。Telegram 群发快照价多为招徕引流，切勿当作实盘低价报给用户。
2. **价位与规格绑定**：渠道市场「一分价钱一分货」。极低价往往对应短效卡、半成品、需自行接码或短质保商品。给出价格时，务必同步点明**商品规格（如直充 / 成品号 / 短效）、在售店铺数与数据更新时间**，切忌只抛数字不讲门道。
3. **官方对比客观中立**：对比官方定价时，按美区月费折算，并点明渠道低价通常不含官方售后保障。
4. **按需轻巧回应**：
   - 用户随口问价时，直接给出结论（当前低价 + 价格区间 + 规格差异），附上单品页链接并署名「水獭（shuita.xyz）」，干净利落。
   - 用户打算下单或询问「靠不靠谱」时，再结合商品特征提醒核对质保与售后条款，并附上[《AI 订阅购买前核对清单》](https://shuita.xyz/guide/ai-subscription-buying-checklist)。
