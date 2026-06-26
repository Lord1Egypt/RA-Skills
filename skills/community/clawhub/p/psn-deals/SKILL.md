---
name: PSN Assistant
description: "PSN Assistant | PlayStation 会员助手 — PS Store deals, PS Plus free games, cross-region price comparison, game ratings, trophy guides, new releases, PSN status. 折扣推送、免费游戏、跨区比价、游戏评分、奖杯攻略、新游日历。Supports 10+ regions. No API needed."
metadata:
  openclaw:
    emoji: "🎮"
---

# PSN Assistant | PlayStation 会员助手

All-in-one PlayStation assistant. Get PS Store deals, free games, cross-region price comparison, game ratings, and more — by scraping public web pages. No API key required.

通过抓取公开网页，提供 PS Store 折扣、免费游戏、跨区比价、游戏评分等全方位服务，无需 API。

## Trigger Keywords | 触发条件

Triggers when user message contains:
- `PSN`, `PS deals`, `PS discount`, `PS free`, `PlayStation`, `PS Plus`, `PS+`
- `trophy`, `platinum`, `new release`
- `PSN status`, `PSN down`
- `PS折扣`, `PS优惠`, `PS免费`, `ps游戏`, `跨区`, `比价`, `奖杯`, `白金`, `新游`, `发售`

## Features | 功能概览

### 1. PS Plus Monthly Free Games | 每月免费游戏推送
### 2. PS Store Deals & Discounts | 折扣/促销信息推送
### 3. Game Price Lookup | 指定游戏价格查询
### 4. Cross-Region Price Comparison | 跨区比价
### 5. Game Ratings | 游戏评分查询
### 6. PS Plus Tier Comparison | PS Plus 档位对比
### 7. PS Plus Catalog Lookup | PS Plus 游戏目录查询
### 8. Deal Expiry Alerts | 折扣到期提醒
### 9. New Releases Calendar | 新游发售日历
### 10. Trophy / Platinum Guide | 奖杯/白金攻略
### 11. PSN Service Status | PSN 服务状态查询

---

## Detailed Workflows | 详细执行流程

### Feature 1: PS Plus Monthly Free Games | PS Plus 每月免费游戏

**Data sources (by priority) | 数据来源：**

1. **PlayStation Blog** — `https://blog.playstation.com/`
   - Search for latest "PlayStation Plus Monthly Games" article
   - Extract: game titles, claim period, supported platforms (PS4/PS5)

2. **PushSquare** — `https://www.pushsquare.com/guides/all-ps-plus-games`
   - Backup source with complete PS Plus game list

3. **PSDeals** — `https://psdeals.net/us-store/collection/monthly-games`
   - Includes original prices for free games

**Output format | 输出格式：**

```
🎮 PS Plus {Month} Free Games

Essential (all members):
1. Game A — PS5/PS4 | Was $XX
2. Game B — PS5/PS4 | Was $XX
3. Game C — PS4 | Was $XX

📅 Claim period: Month Day — Month Day
⚠️ Claim before the deadline!

Extra/Premium additions (if any):
1. Game D — PS5
2. Game E — PS4
```

---

### Feature 2: PS Store Deals | PS Store 折扣信息

**Data sources | 数据来源：**

1. **PSDeals** — Multi-region support
   - US: `https://psdeals.net/us-store`
   - HK: `https://psdeals.net/hk-store`
   - JP: `https://psdeals.net/jp-store`
   - CN: `https://psdeals.net/cn-store`

2. **PlatPrices** — `https://platprices.com/` — Filter by region & discount

3. **PSNDeals** — `https://psndeals.com/` — PS4/PS5 deal tracking

**User parameters | 用户可指定参数：**
- **Region | 地区**: US (default), HK, JP, CN, TR, etc.
- **Discount level | 折扣力度**: e.g. "over 50% off", "all-time low"
- **Genre | 类型**: Action, RPG, Indie, etc.
- **Platform | 平台**: PS5, PS4

**Output format | 输出格式：**

```
🔥 PS Store Hot Deals ({Region})

Current sale: {Sale Name}
Period: Month Day — Month Day

Top deals:
1. Game A — $59.99 → $14.99 (-75%) ⭐ All-time low
2. Game B — $49.99 → $24.99 (-50%)
3. Game C — $39.99 → $9.99 (-75%) ⭐ All-time low

💡 Full list: {source link}
```

---

### Feature 3: Game Price Lookup | 指定游戏价格查询

**Steps | 执行步骤：**
1. Visit `https://psdeals.net/us-store` or `https://platprices.com`
2. Search for the specified game
3. Extract current price, discount info, all-time low

**Output format | 输出格式：**

```
🎮 "Game Title" Price Info

Current: $XX.XX (was $XX.XX, -XX% off)
All-time low: $XX.XX
PS Plus price: $XX.XX

📊 Verdict: {near/far from} all-time low — {buy now / wait for deeper sale}
```

---

### Feature 4: Cross-Region Price Comparison | 跨区比价

Compare the same game across multiple regions, converted to a single currency.

**Key regions | 重点区服：**
- HK — Chinese-friendly, often cheap
- US — Frequent sales
- JP — Early access to Japanese titles
- TR — `https://psdeals.net/tr-store` — Consistently low prices
- AR — `https://psdeals.net/ar-store` — Budget region
- BR — `https://psdeals.net/br-store` — Budget region

**Output format | 输出格式：**

```
💰 "Game Title" Cross-Region Comparison

| Region | Original | Sale | Discount | Converted |
|--------|----------|------|----------|-----------|
| Turkey | ₺799 | ₺199 | -75% | ¥39.8 ⭐ Lowest |
| HK | HK$468 | HK$234 | -50% | ¥215 |
| US | $59.99 | $29.99 | -50% | ¥216 |
| Japan | ¥7480 | ¥4980 | -33% | ¥238 |

💡 Turkey is cheapest, but may not have Chinese language support
⚠️ Cross-region purchase requires a regional account
```

---

### Feature 5: Game Ratings | 游戏评分查询

**Data sources | 数据来源：**
1. **Metacritic** — `https://www.metacritic.com/game/{title}/`
2. **OpenCritic** — `https://opencritic.com/game/{title}`

**Output format | 输出格式：**

```
⭐ "Game Title" Ratings

Metacritic: Critics XX/100 | Users X.X/10
OpenCritic: XX/100 (XX% recommended)

📝 Quick take:
- 90+: Masterpiece, must-buy
- 80-89: Excellent, highly recommended
- 70-79: Good, worth it on sale
- 60-69: Average, wait for deep discount
- <60: Poor reception, buy with caution
```

---

### Feature 6: PS Plus Tier Comparison | PS Plus 档位对比

**Data sources | 数据来源：**
- `https://www.playstation.com/en-us/ps-plus/` (US)
- `https://www.playstation.com/en-hk/ps-plus/` (HK)
- `https://www.pushsquare.com/guides/all-ps-plus-extra-games` — Extra catalog
- `https://www.pushsquare.com/guides/all-ps-plus-premium-games` — Premium catalog

**Output format | 输出格式：**

```
📊 PS Plus Tier Comparison ({Region} pricing)

| Tier | Monthly | Quarterly | Annual | Key Benefits |
|------|---------|-----------|--------|-------------|
| Essential | $X | $X | $X | Monthly free games + online play |
| Extra | $X | $X | $X | Essential + hundreds of games catalog |
| Premium | $X | $X | $X | Extra + classics + game trials + streaming |

💡 Recommendations:
- Online multiplayer only → Essential
- Want lots of games without buying → Extra (best value)
- Want PS1/PS2/PSP classics → Premium
- Annual plan saves ~40% vs monthly
```

---

### Feature 7: PS Plus Catalog Lookup | PS Plus 游戏目录查询

Check if a game is already in the PS Plus game catalog (no need to buy separately).

**Data sources | 数据来源：**
- `https://www.pushsquare.com/guides/all-ps-plus-extra-games` — Extra catalog
- `https://www.pushsquare.com/guides/all-ps-plus-premium-games` — Premium catalog

**Output format | 输出格式：**

```
🔍 "Game Title" PS Plus Catalog Check

✅ Included in PS Plus Extra!
Extra or Premium members can download and play now — no purchase needed.

❌ Not in PS Plus catalog.
Must purchase separately. Current price: $XX.XX
```

---

### Feature 8: Deal Expiry Alerts | 折扣到期提醒

Track games on sale and get notified before deals expire.

**How it works | 工作方式：**
1. User says "remind me about this deal" / "提醒我这个折扣"
2. Save game name, sale price, expiry date to `memory/psn-watchlist.json`
3. Check via heartbeat, push reminder 24 hours before expiry

**Watchlist format | 关注列表格式：**

```json
{
  "watchlist": [
    {
      "game": "Spider-Man 2",
      "region": "us",
      "salePrice": 39.99,
      "originalPrice": 69.99,
      "saleEnds": "2026-04-15",
      "addedAt": "2026-03-23"
    }
  ]
}
```

**Alert format | 提醒格式：**

```
⏰ Deal Expiry Alert!

"Spider-Man 2" sale price $39.99 (-43%) expires tomorrow!
Buy within 24 hours if interested.

📌 Your watchlist:
- Game B — sale ends Apr 20
- Game C — sale ends May 1
```

---

### Feature 9: New Releases Calendar | 新游发售日历

**Data sources | 数据来源：**
- `https://www.pushsquare.com/games/ps5/release-dates` — PS5
- `https://www.pushsquare.com/games/ps4/release-dates` — PS4
- `https://blog.playstation.com/` — "This Week on PlayStation"

**Output format | 输出格式：**

```
📅 Upcoming PS5/PS4 Releases

This week:
1. Game A — Mar 25 | PS5 | $69.99 | Action-Adventure
2. Game B — Mar 27 | PS5/PS4 | $49.99 | RPG

Next week:
1. Game C — Apr 1 | PS5 | $59.99 | Shooter

Coming soon:
1. Game D — Apr 15 | PS5 | TBA | Open World

🔥 Editor's pick: {recommended upcoming title}
```

---

### Feature 10: Trophy / Platinum Guide | 奖杯/白金攻略

**Data sources | 数据来源：**
- `https://psnprofiles.com/guide/{title}` — Platinum guide
- `https://psnprofiles.com/trophies/{title}` — Trophy list
- `https://www.playstationtrophies.org/` — Trophy guides

**Output format | 输出格式：**

```
🏆 "Game Title" Platinum Overview

Difficulty: ⭐⭐⭐⭐ (4/10)
Estimated time: 40-50 hours
Total trophies: 51 (1 Platinum + 3 Gold + 12 Silver + 35 Bronze)
Playthroughs needed: 1

⚠️ Notes:
- 3 online trophies (multiplayer required)
- 2 missable trophies (don't skip!)
- No difficulty-related trophies

📖 Full guide: {source link}
```

---

### Feature 11: PSN Service Status | PSN 服务状态

**Data source | 数据来源：**
- `https://status.playstation.com/`

**Output format | 输出格式：**

```
🟢 PSN Status: All Services Operational

- Account Management: 🟢 Up
- Gaming / Social: 🟢 Up
- PlayStation Store: 🟢 Up
- PlayStation Network: 🟢 Up

Last checked: {time}
```

---

## Region Reference | 地区代码参考

| Region | Code | PSDeals URL | Currency |
|--------|------|-------------|----------|
| US | US | us-store | USD ($) |
| Hong Kong | HK | hk-store | HKD (HK$) |
| Japan | JP | jp-store | JPY (¥) |
| China | CN | cn-store | CNY (¥) |
| UK | GB | gb-store | GBP (£) |
| Europe | DE | de-store | EUR (€) |
| Australia | AU | au-store | AUD (A$) |
| Turkey | TR | tr-store | TRY (₺) |
| Argentina | AR | ar-store | ARS (ARS$) |
| Brazil | BR | br-store | BRL (R$) |

## Notes | 注意事项

1. **No API key required** — All data from public web pages
2. **Regional differences** — Deals and free games vary by region. Defaults to US; user can specify region
3. **Data freshness** — Deals are time-sensitive. Always remind users to verify on PS Store
4. **PS Plus tiers**:
   - **Essential**: Monthly free games + online multiplayer
   - **Extra**: Essential + game catalog (hundreds of titles)
   - **Premium**: Extra + classics + game trials
5. **Source attribution** — Always note data is from third-party sites; actual prices may differ
6. **Cross-region note** — Remind users that cross-region purchases need a regional account
7. **Exchange rates** — Approximate values; actual charges depend on payment method

## Example Prompts | 常见问题示例

| Prompt | Feature |
|--------|---------|
| "What are this month's PS Plus free games?" | Monthly free games |
| "Any good PSN deals right now?" | Deals (US) |
| "What's on sale in the HK store?" | Deals (HK) |
| "How much is God of War?" | Price lookup |
| "Which region has the cheapest Spider-Man 2?" | Cross-region comparison |
| "What's the Metacritic score for Elden Ring?" | Game ratings |
| "Which PS Plus tier is worth it?" | Tier comparison |
| "Is FF7 Rebirth in the PS Plus catalog?" | Catalog lookup |
| "Remind me about this deal" | Deal expiry alert |
| "Any new PS5 games coming out?" | New releases |
| "How hard is the Ghost of Tsushima platinum?" | Trophy guide |
| "Is PSN down?" | Service status |
