---
name: walter-competitor
version: 2.0.0
description: "亚马逊竞品流量攻防智能分析。自动发现竞品、分析流量结构、识别弱点、生成攻击矩阵。无需手动提供ASIN，全自动竞品情报获取。"
---

# 亚马逊竞品流量攻防智能分析

## 核心能力

```
自动发现竞品 → 流量结构分析 → 弱点挖掘 → 攻击矩阵生成
全自动情报获取 → 智能攻防策略 → 可执行投放方案
```

## 用户交互（极简）

### 输入（2个参数）

```yaml
必需:
  keyword: "women active shorts"  # 品类关键词
  my_price: 32.0                  # 我的产品售价

可选:
  my_margin: 0.30                 # 毛利率（默认30%）
```

### 输出

```
竞品流量攻防完整方案
├── 竞品情报（自动发现Top 5）
├── 流量结构分析
├── 关键词攻防矩阵
├── 竞品弱点地图
├── 攻击矩阵（P0/P1/P2）
└── 预算与ROI方案
```

## 分析流程

### Step 1: 自动发现竞品（30秒）

系统自动：

```python
# 1. 获取竞品列表
competitors = data_layer.get_competitor_lookup(keyword)

# 2. 筛选Top 5（按销量/相关性）
top_competitors = filter_top_competitors(competitors, n=5)

# 3. 并行获取详细情报
with ThreadPoolExecutor(max_workers=5) as executor:
    for asin in top_competitors:
        executor.submit(data_layer.get_complete_competitor_intelligence, asin)
```

**输出示例**：

```
[Auto-Discover Competitors] 30 seconds

Found 5 core competitors for "women active shorts":

1. ASIN: B071WV2SRC (CRZ YOGA)
   Sales: ~3,200/month | Price: $28.99 | Rating: 4.5
   Traffic Keywords: 15 | Weakness: No brand ads [WARNING]

2. ASIN: B08KHQY9DV (BALEAF)
   Sales: ~2,800/month | Price: $25.99 | Rating: 4.2
   Traffic Keywords: 22 | Weakness: Low rating, many bad reviews [WARNING]

3. ASIN: B0CBCWHC6P (New Brand)
   Sales: ~1,500/month | Price: $32.99 | Rating: 4.6
   Traffic Keywords: 8 | Weakness: Few keywords, under-promoted [WARNING]

[View Details] [Adjust Range] [Add Custom ASIN]
```

### Step 2: 流量结构全景（1分钟）

分析每个竞品的流量来源：

```
[Traffic Structure Analysis]

                    CompA    CompB    CompC    Market Avg
Organic Search  ████████ 45%    ██████ 35%   ████ 20%    35%
SP Ads          ████ 20%        ████████ 40%  ██ 10%     25%
Brand Ads       ██ 10%          ████ 20%     █ 5%        12%
Video Ads       █ 5%            ██ 10%       █ 5%        7%
AC Recommended  ████ 15%        ████ 15%     ████████ 50% 18%
Other           ███ 5%          ██ 5%        ██ 10%      8%

Insights:
• CompA: Relies on organic, low ad spend → Opportunity: Increase ads to steal traffic
• CompB: SP ads 40% → Learn their keyword strategy
• CompC: AC 50% → High conversion, focus target
```

### Step 3: 关键词攻防矩阵（2分钟）

```
[Keyword Battle Matrix] Top 50 Keywords

High-Value Attack Targets (Competitors have but weak coverage):
┌─────────────────────┬──────────┬────────┬─────────┬──────────┐
│ Keyword             │ Volume   │ CompA  │ CompB   │ Action   │
├─────────────────────┼──────────┼────────┼─────────┼──────────┤
│ quick dry shorts    │ 12,500   │ [P3]   │ [X]     │ [ATTACK] │
│ athletic shorts women│ 8,900   │ [P5]   │ [P8]    │ [ATTACK] │
│ yoga shorts pocket  │ 5,600    │ [X]    │ [X]     │ [ATTACK] │
│ running shorts 5 inch│ 4,200   │ [P12]  │ [X]     │ [ATTACK] │
└─────────────────────┴──────────┴────────┴─────────┴──────────┘

Your Advantage Keywords (No competitor coverage):
• "anti-chafe shorts" - Volume 2,100, no competitors [CHECK]
• "high waist workout" - Volume 1,800, only 1 competitor [CHECK]

Defensive Keywords (Your core words to protect):
• "women active shorts" - All competitors bidding [WARNING]
```

### Step 4: CPA/ACOS Analysis（自动计算）

```
[Ad ROI Calculation] Based on your price $32, margin 30%

Target CPA: $9.6 (Price × Margin)

Keyword Bidding Recommendations:
┌─────────────────────┬────────┬────────┬────────┬────────┐
│ Keyword             │ Bid    │ Est.CVR│ Est.CPA│ P&L    │
├─────────────────────┼────────┼────────┼────────┼────────┤
│ quick dry shorts    │ $1.80  │ 8%     │ $22.5  │ [LOSS] │
│ athletic shorts     │ $1.20  │ 12%    │ $10.0  │ [LOW]  │
│ yoga shorts pocket  │ $0.90  │ 15%    │ $6.0   │ [PROFIT]│
│ workout shorts      │ $1.50  │ 10%    │ $15.0  │ [LOSS] │
└─────────────────────┴────────┴────────┴────────┴────────┘

Traffic Light System:
[GREEN]  Profit: 3 keywords, scale up
[YELLOW] Marginal: 5 keywords, optimize conversion
[RED]    Loss: 2 keywords, pause or reduce bid
```

### Step 5: 竞品弱点挖掘（1分钟）

```
[Competitor Weakness Map]

Competitor A (B071WV2SRC - CRZ YOGA):
├─ Traffic: Only 15 keywords, no brand ads
├─ Rating: 4.5, but 18% reviews mention "pilling"
├─ Price: $28.99, reduced 3 times recently (price war)
└─ VOC: Users complain "pockets too small"
[Attack Strategy] Emphasize "anti-pilling" + "large pockets"

Competitor B (B08KHQY9DV - BALEAF):
├─ Traffic: Over-relies on SP ads (40%), weak organic
├─ Rating: 4.2, 12% return rate (industry avg 8%)
├─ Product: Thin fabric, see-through issues
└─ Service: Slow support, poor review handling
[Attack Strategy] Emphasize "quality" + "service", steal dissatisfied users

Competitor C (B0CBCWHC6P - New Brand):
├─ Traffic: Only 8 keywords, severely under-promoted
├─ Strength: 4.6 rating, good product but unknown
└─ Opportunity: Copy their successful keywords
[Attack Strategy] Learn their path, increase promotion
```

### Step 6: 攻击矩阵生成（核心输出）

```
[Traffic Battle Plan]

═══════════════════════════════════════════════════════════════
P0 - Execute Immediately (High ROI, Quick Results)
═══════════════════════════════════════════════════════════════

Target 1: Steal CompA's "quick dry shorts" traffic
├─ Action: SP exact match, bid $1.50
├─ Budget: $50/day
├─ Expected: 30 clicks/day, 3 conversions
├─ ROI: +25%
└─ Timeline: Launch now

Target 2: Capture CompB's lost customers
├─ Action: Brand defense ads, keyword "BALEAF alternative"
├─ Budget: $30/day
├─ Expected: 15 clicks/day, 2 conversions
├─ ROI: +40% (high-quality competitor users)
└─ Timeline: Launch now

Target 3: Capture empty keyword "yoga shorts pocket"
├─ Action: SP+SB simultaneous bidding
├─ Budget: $40/day
├─ Expected: 25 clicks/day, 4 conversions
├─ ROI: +35%
└─ Timeline: Launch now

P0 Total Budget: $120/day
P0 Expected Return: +9 orders/day, $288 ad sales, $43 profit

═══════════════════════════════════════════════════════════════
P1 - Short-term (1-2 Weeks)
═══════════════════════════════════════════════════════════════

Target 1: Improve organic ranking
├─ Action: Optimize listing keywords, add "anti-chafe" differentiation
├─ Budget: $0 (optimization cost)
└─ Timeline: Complete this week

Target 2: Video ad test
├─ Action: SBV video ad, show "anti-pilling test"
├─ Budget: $60/day test
└─ Timeline: Launch within 2 weeks

═══════════════════════════════════════════════════════════════
P2 - Long-term Layout (1 Month)
═══════════════════════════════════════════════════════════════

Target 1: Brand defense
├─ Action: Bid on your own brand keywords
├─ Budget: $20/day
└─ Timeline: Within 1 month

Target 2: Related traffic
├─ Action: Target complementary products (yoga mats, sports bras)
├─ Budget: $40/day
└─ Timeline: Within 1 month
```

### Step 7: 预算与ROI方案

```
[Ad Budget Plans]

Conservative Plan (Daily $120):
├─ P0 Attack: $120/day
├─ Expected Daily Orders: +9
├─ Expected Daily Sales: $288
├─ Expected Daily Profit: $43
└─ Payback: Immediate

Standard Plan (Daily $200):
├─ P0 Attack: $120/day
├─ P1 Test: $60/day
├─ P2 Layout: $20/day
├─ Expected Daily Orders: +15
├─ Expected Daily Sales: $480
├─ Expected Daily Profit: $62
└─ Payback: Immediate

Aggressive Plan (Daily $350):
├─ P0 Attack: $150/day (increased)
├─ P1 Test: $100/day (multi-keyword)
├─ P2 Layout: $100/day (fast positioning)
├─ Expected Daily Orders: +28
├─ Expected Daily Sales: $896
├─ Expected Daily Profit: $98
└─ Risk: Monitor ACOS closely

[Recommendation] Start with conservative, scale up after ROI validation
```

## 技术实现

### 竞品自动发现算法

```python
def auto_discover_competitors(keyword: str, n: int = 5) -> List[str]:
    """Auto-discover core competitors"""
    # 1. Get competitor list
    result = data_layer.get_competitor_lookup(keyword)
    competitors = result.get("data", {}).get("items", [])
    
    # 2. Score and rank
    scored_competitors = []
    for comp in competitors:
        score = 0
        score += comp.get("monthlySales", 0) * 0.4
        score += comp.get("relevanceScore", 0) * 0.3
        score += comp.get("ratings", 0) * 0.0001 * 0.2
        price_diff = abs(comp.get("price", 0) - my_price)
        score += max(0, (50 - price_diff)) * 0.1
        scored_competitors.append((comp["asin"], score))
    
    # 3. Return Top N
    scored_competitors.sort(key=lambda x: x[1], reverse=True)
    return [asin for asin, _ in scored_competitors[:n]]
```

### 弱点挖掘算法

```python
def mine_weaknesses(competitor_data: dict) -> List[dict]:
    """Mine competitor weaknesses"""
    weaknesses = []
    
    # Traffic weakness
    traffic = competitor_data.get("traffic_analysis", {})
    if traffic.get("total_traffic_keywords", 0) < 20:
        weaknesses.append({
            "type": "low_traffic_diversity",
            "severity": "high",
            "description": f"Only {traffic['total_traffic_keywords']} traffic keywords",
            "attack_opportunity": "Capture their missing keywords"
        })
    
    # VOC weakness
    voc = competitor_data.get("voc_analysis", {})
    pain_points = voc.get("pain_points", [])
    if len(pain_points) > 5:
        top_pain = pain_points[0]
        weaknesses.append({
            "type": "voc_pain_point",
            "severity": "high",
            "description": top_pain["theme"],
            "attack_opportunity": f"Emphasize '{top_pain['theme']}' solution"
        })
    
    return weaknesses
```

## 依赖

- `unified_data_layer_v2.py` - 统一数据层
- `sellersprite_mcp.py` - MCP客户端
- SellerSprite API access

## 版本

V2 - 2026-04-12
- Added auto-competitor discovery
- Implemented traffic structure analysis
- Added keyword battle matrix
- Generated P0/P1/P2 attack plans
