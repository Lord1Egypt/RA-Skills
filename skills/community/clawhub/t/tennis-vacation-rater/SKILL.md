---
name: tennis-travel-rater-v2
description: Evaluate tennis vacation destinations with structured scoring across transportation, accommodation, weather, and court facilities. Use when users ask about tennis travel destinations, court recommendations, tennis vacation planning, comparing tennis resorts, or assessing tennis tourism spots.
---

# Tennis Travel Rater

Evaluate tennis vacation destinations with structured scoring and recommendations.

## Data Sources

This skill uses web search to collect flight price information. No external tools or installations are required.

## Quick Start

1. Extract destination info from user input
2. Confirm departure city (ask if not provided, default to Shanghai)
3. Ask user preferences (optional, use default weights if skipped)
4. Collect data for each dimension
5. Calculate weighted scores
6. Generate report using template

## Scoring Dimensions

| Dimension | Weight | Key Metrics |
|-----------|--------|-------------|
| Transportation | 25% | Flight price, frequency, ground transport |
| Accommodation | 25% | Hotel price, rating, proximity to courts |
| Weather | 20% | Temperature, precipitation, best season |
| Facilities | 30% | Court quality, fees, coaching availability |

**Custom Weights**: If user has preferences, adjust weights as follows:
- **If user selects 2 priorities**: 35% / 35% / 15% / 15% for top 2 and bottom 2
- **If user selects 1 priority only**: 35% / 21.7% / 21.7% / 21.6% (priority gets 35%, others equally split remaining 65%)
- **If user selects no preference**: Use default 25% / 25% / 25% / 25%

### Dimension Details

**Transportation (交通可达性)**
- Flight price: Round-trip cost from origin
- Frequency: Daily/weekly flights, flexibility
- Ground transport: Airport to court/hotel convenience

**Accommodation (住宿条件)**
- Hotel price: Mid-range average per night
- Court-proximity: Walking distance or shuttle available
- Rating: Booking/TripAdvisor scores

**Weather (天气适宜度)**
- Temperature: 15-28C optimal for outdoor tennis
- Precipitation: Rain probability impact
- Sunlight: Playable hours per day
- Best season: Recommended months

**Facilities (球场质量)**
- Court types: Hard/clay/grass count and quality
- Fees: Hourly rental rates
- Amenities: Locker room, shower, racket rental
- Coaching: Pro coach availability and rates

## Destination Types

| Type | Characteristics | Best For |
|------|-----------------|----------|
|  Training | Pro facilities, intensive atmosphere | Serious players |
|  Resort | Leisure vibe, integrated vacation | Families/friends |
|  Scenic | Unique views, Instagram-worthy | Short trips |
|  Urban | City center, trendy | Business travelers |

## Workflow

### Step 1: Gather Information

Extract from user input:
- Destination name (city/resort/court) - 从文字或链接中提取
- Travel dates/season
- Departure city
- Any links provided (Xiaohongshu, Instagram, etc.)

**信息收集原则：**
- 链接访问失败不阻塞流程
- 从用户消息文字中提取目的地（如"富士山" 确定为"静冈"或"山梨"）
- 缺失信息先使用默认值，同时询问用户确认

#### Link Access Protocol

**When user provides a link (e.g., Xiaohongshu, Instagram)**:

1. **Extract destination from user message text first**
   - Parse destination from message content (e.g., "富士山人生球场"  Japan Shizuoka/Yamanashi)
   - This is the primary source - never rely solely on link access

2. **Optionally attempt to access the link** (non-blocking, 10s timeout)
   - Use WebFetch or browser automation
   - If successful  supplement with additional details
   - If failed  continue with text-extracted information

3. **Confirm with user if information is unclear**
   - Ask: "Detected you want to visit [destination]. Is this correct?"
   - Get confirmation before proceeding

4. **Never block on link failure**
   - Link access is supplementary only
   - Always proceed with text-extracted information
   - Missing details can be filled via user questions

**If departure city unknown**: Ask user or default to Shanghai (note in report).

### Step 2: User Preferences (Optional)

Ask: "What's most important to you? (Choose up to 2)"
- Flight convenience
- Hotel quality
- Weather
- Court facilities

If skipped, use default 25% weights.

### Step 3: Data Collection

| Dimension | Data Source | Fallback |
|-----------|-------------|----------|
| Flights | **flyai CLI** (if installed) for real-time prices | WebSearch for reference prices |
| Hotels | Booking, TripAdvisor | WebSearch |
| Weather | Historical climate data | - |
| Courts | Built-in database, web search | - |

**注意**：如果 flyai CLI 未安装，将使用 WebSearch 获取参考价格，并在报告中标注数据来源。

#### Flight Search

**Priority: Use flyai CLI for real-time prices if available**

**Step 1: Check if flyai is installed**
```bash
which flyai
```

**Step 2: If installed, query real-time flight prices**
```bash
flyai search-flight \
  --origin "出发城市" \
  --destination "目的地" \
  --dep-date-start YYYY-MM-DD \
  --dep-date-end YYYY-MM-DD \
  --back-date-start YYYY-MM-DD \
  --back-date-end YYYY-MM-DD \
  --sort-type 3
```

**Step 3: Parse results**
- Round-trip total price (for scoring)
- Top 3 cheapest options (for report)
- jumpUrl (booking link)

**Fallback: If flyai is not installed**

Use **WebSearch** to get reference prices:
- Search query: `[出发城市]到[目的地]机票价格`
- Label as "网络参考价（非实时）"
- Note in report: "Install flyai CLI for real-time prices: `npm install -g @fly-ai/flyai-cli`"

**Data Source Labels:**
| Label | Condition | Scoring Impact |
|-------|-----------|----------------|
| flyai实时 | flyai CLI executed successfully | Full score |
| 网络参考 | WebSearch used (flyai not installed) | -1 point (max 8/10) |
| 待补充 | All methods failed | Max 5/10 |

** Rules:**
- Never invent flight prices
- Always label data source clearly

### Step 4: Scoring

Each dimension scored 0-10:
- 9-10: Excellent
- 7-8: Good
- 5-6: Average
- <5: Poor

**Final Score** = (dimension_score  weight)

### Step 5: Report Generation

Use [report-template.md](references/report-template.md) for full template.

For single destination: Use single-destination template
For multiple destinations: Use comparison template

## Report Structure

```markdown
#  Tennis Travel Rating Report
## [Destination]

> **一句话总结**：[简洁概括目的地核心优势和注意事项]

### Overall Score: [X.X]/10
**Rating**: [Highly Recommended/Recommended/etc.]
**Type**: [Training/Resort/Scenic/Urban]

### Dimension Scores
| Dimension | Score | Weight | Key Metric | 数据来源 |
|-----------|-------|--------|------------|----------|
| Transportation | X.X/10 | XX% | 往返机票 X,XXX起 | flyai实时/网络参考/待补充 |
| Accommodation | X.X/10 | XX% | XXX/晚 | Booking/Agoda/携程 |
| Weather | X.X/10 | XX% | 最佳季节: X-X月 | 历史气候数据 |
| Facilities | X.X/10 | XX% | 场地费 XXX/小时 | 酒店官网/实地调查 |

**数据来源标注说明：**
- **flyai实时**：使用Bash工具执行flyai命令获取的实时价格
- **网络参考价**：通过WebSearch获取的参考价格（非实时）
- **待补充**：无法获取数据，需要用户自行查询

### 1 交通可达性 (X.X/10)

**航班信息**
- 往返机票 X,XXX起
- 航空公司、转机情况等

**地面交通**
- 机场酒店/球场：约X小时车程
- [ 查看谷歌地图路线](https://www.google.com/maps/dir/机场名称/酒店或球场名称)

### 2 住宿条件 (X.X/10)

**酒店概况**
- **酒店名称**: [酒店名]
- **位置**: [具体位置描述]
- [ 在谷歌地图上查看](https://www.google.com/maps/search/酒店名+城市)
- 价格、评分等信息

### 3 天气适宜度 (X.X/10)

**最佳季节**: X-X月
- 温度、降水等分析

### 4 球场质量 (X.X/10)

**球场设施**
- **球场名称**: [球场名]
- **位置**: [具体位置描述]
- [ 在谷歌地图上查看](https://www.google.com/maps/search/球场名+城市)
- 场地类型、费用、预订方式等

### Highlights
- [Top strength]
- [Key consideration]
- [Best for: target audience]

### Budget Estimate (X天X晚)
| Item | Cost (参考价) |
|------|---------------|
| 往返机票 | X,XXX |
| 住宿 (X晚) | X,XXX |
| 球场费用 | XXX |
| 餐饮及其他 | X,XXX |
| **总计** | **X,XXX** |

*Generated: [Date] | Sources: [List]*
```

### Report Footer - Price Monitoring (REQUIRED)

**ALWAYS include this section at the end of every report:**

```markdown
---

###  价格查询建议

由于您的出行时间较灵活 / 距离计划出行还有[X天]，建议先查询当前机票价格：

**我可以为您提供**：
- 一次性查询 [出发地]  [目的地] 的当前航班价格
- 根据查询结果给出购票建议
- 推荐最佳购票时机

**需要我帮您查询当前价格吗？** 请告诉我您的预算上限（如：往返机票 X,XXX以内）。
```

**触发条件**（满足任一即需添加）：
1. 用户没有设置具体出行日期
2. 计划出行时间距离今天 >15天

**如果用户同意监控**：
1. 询问：出发城市、目的地、偏好月份、预算上限
2. **手动价格检查**：在当前会话中使用 WebSearch 或 flyai CLI 查询当前价格
3. **提供建议**：根据查询结果给出购票建议，但不创建自动监控任务
4. 确认已提供价格信息

**如果用户拒绝**：正常结束，无需进一步操作

**注意**：本 skill 不创建自动后台监控任务。如需持续监控，请手动定期查询。

## Built-in Database

Quick reference for popular destinations:

**Asia**: Sanya Haitang Bay, Shanghai Qizhong, Tokyo Ariake, Bali
**Europe**: Roland Garros, Wimbledon, Monte Carlo, Barcelona
**Americas**: Indian Wells, Miami, Cancun
**Oceania**: Melbourne Park, Gold Coast

For full database, see [destinations.md](references/destinations.md).

## Key Principles

1. **No data, no output** - Mark missing data as "待补充"
2. **Label all prices** as "参考价" (reference only)
3. **Highlight data sources** for transparency
4. **Never invent** flight prices, hotel ratings, or any destination details
5. **Link fails  Ask user** - When cannot access user-provided links, always ask for direct input instead of guessing

## Anti-Hallucination Checklist

Before generating report, verify:
- [ ] **航班价格**：来自flyai实时查询（Bash工具），或已标记为"待补充/网络参考价"
- [ ] **未使用WebSearch冒充flyai**：没有用网络搜索价格冒充实时查询结果
- [ ] All ratings are from real platforms or marked "待补充"
- [ ] No information invented when link access failed
- [ ] User provided destination name (not guessed from failed link)
- [ ] Data sources clearly labeled in report

### 航班数据专项核查

**必须确认：**
-  已检查 flyai CLI 是否可用
-  如可用，已使用 Bash 工具执行 flyai 命令
-  如不可用，已使用 WebSearch 获取参考价格
-  交通维度评分基于实际获取的价格数据
-  数据来源已清晰标注（flyai实时/网络参考/待补充）

## Price Monitoring Guide (MANDATORY)

### When to Include

**MUST include price monitoring section in EVERY report when:**
- User has not set specific travel dates, OR
- Travel date is >15 days away from today

### Where to Include

**ALWAYS add at the END of the report**, after the budget estimate section:

```markdown
---

###  价格查询建议

由于您的出行时间较灵活 / 距离计划出行还有[X天]，建议先查询当前机票价格：

**我可以为您提供**：
- 一次性查询 [出发地]  [目的地] 的当前航班价格
- 根据查询结果给出购票建议
- 推荐最佳购票时机

**需要我帮您查询当前价格吗？** 请告诉我您的预算上限（如：往返机票 X,XXX以内）。
```

### If User Agrees

1. Ask for details:
   - Departure city (confirm)
   - Destination (confirm)
   - Preferred travel months
   - Budget limit for round-trip flights

2. **Perform immediate price check** (no automatic monitoring):
   - Use WebSearch or flyai CLI to check current prices
   - Compare with user's budget
   - Provide booking recommendation based on current data

3. Confirm to user:
   ```markdown
    **价格查询完成**
   
   - 路线：[出发地]  [目的地]
   - 当前价格：[价格]
   - 您的预算：[预算]
   - 建议：[立即预订/继续观望]
   
   **注意**：此为一次性查询。如需持续关注，请定期手动查询或使用专业价格监控工具。
   ```

### If User Declines

Continue normally, no further action needed.

## Examples

**Example 1 - Basic query (flyai installed)**:
Input: "Evaluate Sanya for tennis trip from Shanghai in April"
Workflow:
1. Ask departure city  Shanghai
2. Ask preferences  User selects "Weather" and "Facilities"
3. **Check if flyai is installed**  Yes
4. **Query real-time flights**:
   ```bash
   flyai search-flight --origin "上海" --destination "三亚" --dep-date-start 2025-04-01 --dep-date-end 2025-04-07 --back-date-start 2025-04-05 --back-date-end 2025-04-12 --sort-type 3
   ```
5. Parse price (1,580)  Score transportation dimension
6. Search hotels, weather, court info
7. Generate report with weights: Weather 35%, Facilities 35%, Transportation 15%, Accommodation 15%
Output: Full report with 8.2/10 score (transportation based on flyai real-time price)

**Example 1b - flyai not installed**:
Input: "Evaluate Sanya for tennis trip from Shanghai in April"
Workflow:
1-2. Same as above
3. **Check if flyai is installed**  No
4. **Use WebSearch fallback**:
   - Search: "上海到三亚机票价格"
   - Get reference price: 1,200-2,000
   - Label as "网络参考价（非实时）"
5. Score transportation dimension (max 8/10 due to reference data)
6. Continue with other data collection
7. Generate report with note: "Install flyai CLI for real-time prices"
Output: Report with reference prices and installation suggestion

**Example 2 - Comparison**:
Input: "Compare Sanya vs Bali for tennis vacation"
Output: Side-by-side comparison with recommendation

**Example 3 - Custom weights (single priority)**:
Input: "I care most about flight convenience"
Workflow:
1. User selects only 1 priority: "Transportation"
2. Weights: Transportation 35%, Accommodation 21.7%, Weather 21.7%, Facilities 21.6%
3. Check flyai availability  Query flights if installed, else use WebSearch
4. Score transportation based on available data source
Output: Report with Transportation 35%, others equally split

**Example 4 - User provides Xiaohongshu link**:
Input: "我想去这里打球：96 【富士山人生球场！...】https://www.xiaohongshu.com/..."
Workflow:
1. **Extract destination from text first**:
   - Parse "富士山人生球场"  Japan Shizuoka/Yamanashi region
   - Text extraction is primary - link access is optional
2. **Optionally attempt link access**  Failed (Xiaohongshu anti-scraping)
   - Continue with text-extracted information
3. **Confirm with user**: "Detected you want to visit a court near Mt. Fuji (Shizuoka area). Default departure city: Shanghai. Is this correct?"
4. After user confirms, **check flyai availability**:
   - If installed  Query real-time flights
   - If not installed  Use WebSearch for reference prices
5. Generate report with clear data source labels
Output: Complete report with transportation data (source clearly labeled)
