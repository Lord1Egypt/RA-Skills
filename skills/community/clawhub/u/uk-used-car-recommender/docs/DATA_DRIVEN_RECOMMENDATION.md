# Data-Driven Recommendation Guide

## Overview

This document details how to implement used car recommendations based on real market data, rather than relying solely on the LLM's training knowledge.

---

## 🔄 Workflow Comparison

### ❌ Old Method: Pure Inference-Driven

```
User needs → LLM inference → Recommend models (based on training data)
                                  ↓
                            (May be outdated/inaccurate)
```

**Problems:**
- Information only up to training data cutoff date
- Prices may have changed significantly
- Recommended models may be scarce in market
- Lacks real market validation

---

### ✅ New Method: Data-Driven Reasoning

```
User needs → Generate search strategy → Fetch real data → Analyze + Reason → Recommend
                                                    ↓
                                        (Based on actual market conditions)
```

**Advantages:**
- ✅ Recommended models actually exist in the market
- ✅ Prices based on current actual listings
- ✅ Understand real supply situation
- ✅ Combine reliability knowledge + market reality

---

## 📋 Implementation Steps

### Step 1: Collect Key Information

**Required Information:**
- Budget (maximum price)
- Location (city name or "uk")

**Recommended to Collect:**
- Usage (commute/family/off-road, etc.)
- Preferences (brand, model, fuel type)
- Must-have requirements (automatic, ULEZ compliant, number of seats, etc.)

**Example Dialogue:**
```
Agent: To recommend actual vehicles for sale, I need your budget and location.
       What's your maximum budget? Which city?

User: £10,000, London

Agent: Great! What's the usage? Commute, family, or other?

User: Mainly commute, occasionally family

Agent: Any special requirements? Like automatic, fuel-efficient, or other preferences?

User: Automatic, fuel-efficient, good reliability

Agent: Got it! I'll now search for reliable automatic vehicles under £10,000 in London...
```

---

### Step 2: Generate Search Strategies

Based on requirements, build **3-5 different search queries**, covering:
- Different reliable brands/models
- Different fuel types (petrol, hybrid, diesel)
- Price ranges (leave some room)

**Example (Budget £10k, London, automatic, fuel-efficient):**

```python
strategies = [
    {
        "name": "Toyota Yaris Hybrid",
        "make": "toyota",
        "model": "yaris",
        "fuel_type": "hybrid_electric",
        "transmission": "automatic",
        "max_price": 10000,
        "location": "London",
        "year": "up_to_5",
        "sort": "price_lowest_first",
        "rationale": "Excellent fuel economy, Toyota reliability, CVT automatic"
    },
    {
        "name": "Honda Jazz",
        "make": "honda",
        "model": "jazz",
        "fuel_type": "petrol",
        "transmission": "automatic",
        "max_price": 10000,
        "location": "London",
        "year": "up_to_5",
        "sort": "price_lowest_first",
        "rationale": "Legendary reliability, flexible space, smooth CVT"
    },
    {
        "name": "Mazda 2",
        "make": "mazda",
        "model": "2",
        "fuel_type": "petrol",
        "transmission": "automatic",
        "max_price": 10000,
        "location": "London",
        "year": "up_to_5",
        "sort": "price_lowest_first",
        "rationale": "Driving pleasure, reliable, low failure rate"
    },
    {
        "name": "Hyundai i20",
        "make": "hyundai",
        "model": "i20",
        "fuel_type": "petrol",
        "transmission": "automatic",
        "max_price": 10000,
        "location": "London",
        "year": "up_to_5",
        "sort": "price_lowest_first",
        "rationale": "Good warranty, modern design, good value"
    },
    {
        "name": "Ford Fiesta (backup)",
        "make": "ford",
        "model": "fiesta",
        "fuel_type": "petrol",
        "transmission": "automatic",
        "max_price": 9500,  # Leave £500 room
        "location": "London",
        "year": "up_to_5",
        "sort": "price_lowest_first",
        "rationale": "Many market choices, but avoid 1.0 EcoBoost wet belt issues"
    }
]
```

---

### Step 3: Execute Parallel Searches

**Execute Gumtree CLI search for each strategy:**

```bash
# Strategy 1: Toyota Yaris Hybrid
python ~/.cursor/skills/uk-car-recommender/scripts/cli.py search \
  --make toyota --model yaris \
  --fuel-type hybrid_electric \
  --transmission automatic \
  --max-price 10000 \
  --location London \
  --year up_to_5 \
  --sort price_lowest_first \
  --limit 15

# Strategy 2: Honda Jazz
python ~/.cursor/skills/uk-car-recommender/scripts/cli.py search \
  --make honda --model jazz \
  --transmission automatic \
  --max-price 10000 \
  --location London \
  --year up_to_5 \
  --sort price_lowest_first \
  --limit 15

# ... other strategies
```

**Tip:** You can use the Shell tool to execute these commands sequentially or in parallel.

---

### Step 4: Parse and Analyze Results

**Extract from each search result:**

```python
# Pseudocode example
results_analysis = []

for strategy in strategies:
    search_result = execute_search(strategy)
    
    if search_result["ok"]:
        items = search_result["items"]
        
        # Calculate statistics
        analysis = {
            "model": strategy["name"],
            "total_found": len(items),
            "total_available": search_result.get("total_results", len(items)),
            "prices": [item.get("price") for item in items if item.get("price")],
            "years": [item.get("year") for item in items if item.get("year")],
            "mileages": [item.get("mileage") for item in items],
            "seller_types": [item.get("seller_type_display") for item in items],
            "avg_price": calculate_average_price(items),
            "price_range": (min_price, max_price),
            "trade_count": count_trade_sellers(items),
            "private_count": count_private_sellers(items),
            "sample_listings": items[:3],  # First 3 examples
            "search_url": search_result["search_url"]
        }
        
        results_analysis.append(analysis)
```

**Key Metrics:**
1. **Supply** - Number of available vehicles
2. **Price Distribution** - Minimum, maximum, average prices
3. **Condition** - Year and mileage ranges
4. **Seller Type** - Trade vs Private ratio

---

### Step 5: Ranking and Recommendations

**Comprehensive Scoring Formula:**

```python
def calculate_recommendation_score(analysis, user_requirements):
    score = 0
    
    # 1. Availability score (more is better)
    availability_score = min(analysis["total_found"] / 20, 1.0) * 30
    
    # 2. Price score (average price below budget is better)
    budget = user_requirements["max_budget"]
    price_buffer = budget - analysis["avg_price"]
    price_score = min(price_buffer / 2000, 1.0) * 25
    
    # 3. Reliability score (from training knowledge)
    reliability_score = get_reliability_rating(analysis["model"]) * 25
    
    # 4. Match score (meets user preferences)
    match_score = calculate_preference_match(analysis, user_requirements) * 20
    
    return score + availability_score + price_score + reliability_score + match_score

# Sort all models
ranked_recommendations = sorted(
    results_analysis,
    key=lambda x: calculate_recommendation_score(x, user_requirements),
    reverse=True
)
```

---

### Step 6: Present Recommendations

**Display Format:**

```markdown
🔍 Based on real-time London market research (2026-05-07)

Searched 5 reliable models, found 165 vehicles for sale:

---

📊 **Market Analysis Results:**

1. **Toyota Yaris Hybrid** - 45 for sale
   - Price range: £7,500 - £10,000 (average £9,200)
   - Typical condition: 2017-2020, 40k-65k miles
   - Sellers: 80% Trade, 20% Private

2. **Honda Jazz** - 23 for sale
   - Price range: £6,995 - £9,950 (average £8,800)
   - Typical condition: 2016-2019, 35k-60k miles
   - Sellers: 65% Trade, 35% Private

3. **Ford Fiesta** - 67 for sale
   - Price range: £6,000 - £9,500 (average £8,500)
   - Typical condition: 2016-2019, 40k-70k miles
   - Sellers: 70% Trade, 30% Private

4. **Mazda 2** - 18 for sale
   - Price range: £8,500 - £10,000 (average £9,500)
   - Typical condition: 2017-2020, 30k-55k miles
   - Sellers: 85% Trade, 15% Private

5. **Hyundai i20** - 12 for sale
   - Price range: £8,000 - £10,000 (average £9,100)
   - Typical condition: 2018-2020, 25k-50k miles
   - Sellers: 90% Trade, 10% Private

---

✨ **Recommendation Ranking (Comprehensive Score):**

### 【Top Choice】Honda Jazz (2016-2019)

📊 **Real Market Data:**
- ✓ 23 vehicles for sale
- 💷 Actual prices: £6,995 - £9,950 (average £8,800)
- 📅 Typical condition: 3-7 years old, 35k-60k miles
- 🏪 65% Trade sellers (most with warranty)

⭐ **Why Recommended:**
1. **Best Value** - Average price £8,800, £1,200 below budget, room to spare
2. **Legendary Reliability** - What Car? reliability rating ⭐⭐⭐⭐⭐
3. **Abundant Choices** - 23 for sale, won't struggle due to fierce competition
4. **Flexible Space** - Magic Seats, extremely high space utilization
5. **Low Running Costs** - Insurance group 7-12, VED £20-£165/year

⚠️ **Cautions:**
- Pre-2015 old model looks dated, recommend 2016+ facelift
- CVT automatic not fast-accelerating, but smooth enough for daily commute

🔗 **View actual listings:** [Gumtree search link]

---

### 【Runner-up】Toyota Yaris Hybrid (2017-2020)

📊 **Real Market Data:**
- ✓ 45 vehicles for sale (most choices)
- 💷 Actual prices: £7,500 - £10,000 (average £9,200)
- 📅 Typical condition: 4-7 years old, 40k-65k miles

⭐ **Why Recommended:**
1. **Most Choices** - Most abundant market supply, room for negotiation
2. **Excellent Fuel Economy** - Hybrid system, 60+ MPG city
3. **Toyota Reliability** - Mature hybrid technology, low failure rate
4. **ULEZ Free** - Free passage in London zero-emission zone

⚠️ **Cautions:**
- Average price £9,200, slightly higher than Jazz
- Rear space smaller than Jazz
- CVT transmission not suitable for aggressive driving

🔗 **View actual listings:** [Gumtree search link]

---

### 【Backup】Ford Fiesta (2016-2019)

📊 **Real Market Data:**
- ✓ 67 vehicles for sale (most choices)
- 💷 Actual prices: £6,000 - £9,500 (average £8,500)

⭐ **Advantages:** Most choices, low price

⚠️ **Important Warning:**
- **Avoid 2015-2019 1.0 EcoBoost three-cylinder engine** - High wet belt failure rate
- **Recommend 1.25L four-cylinder petrol version** - Reliable but slightly higher fuel consumption
- Need to carefully check if EcoBoost models had timing belt replaced

---

### 📋 Example Actual Listings (Honda Jazz Top 3)

**1. 2018 Honda Jazz 1.3 i-VTEC SE 5dr CVT**
- 💷 £8,495
- 📍 Stratford, London
- 📅 2018, 48,000 miles
- 🏪 Trade seller (with warranty)
- 🖼️ [View images]
- 🔗 [View details]

**2. 2017 Honda Jazz 1.3 i-VTEC EX 5dr**
- 💷 £7,995
- 📍 Hackney, London
- 📅 2017, 52,000 miles
- 🏪 Trade seller (with warranty)
- 🖼️ [View images]
- 🔗 [View details]

**3. 2019 Honda Jazz 1.3 i-VTEC SE Navi 5dr CVT**
- 💷 £9,750
- 📍 Barnet, London
- 📅 2019, 35,000 miles
- 🏪 Trade seller (1 year warranty)
- 🖼️ [View images]
- 🔗 [View details]

---

💡 **Next Step Suggestions:**
1. Review above actual listings, pick 3-5 of interest
2. Check MOT history (gov.uk/check-mot-history)
3. Run HPI check (£20-£40)
4. Arrange viewing and test drive
5. Prepare to negotiate (Trade sellers usually have £200-£500 negotiation room)

Need help analyzing MOT history for a specific vehicle or providing viewing checklist?
```

---

## 🎯 Key Principles

### 1. **Data First, Knowledge Assist**

- ✅ **First** see what's in the market
- ✅ **Then** use reliability knowledge to exclude bad options
- ✅ **Finally** recommend based on real supply and demand

### 2. **Transparent Data Sources**

- Clearly state "based on X actual vehicles for sale"
- Show search date
- Provide search links for user verification

### 3. **Combine Both Strengths**

**Real Data Provides:**
- Current prices
- Actual supply
- Market trends

**Training Knowledge Provides:**
- Reliability ratings
- Known issues
- Long-term value
- Insurance and tax information

### 4. **Graceful Degradation**

If unable to fetch real data (network issues, CLI errors):
1. Honestly inform user
2. Give guidance based on training knowledge
3. Suggest user manually search Gumtree/Auto Trader
4. Provide search URL templates

---

## 📊 Effectiveness Comparison Example

### Scenario: User budget £8,000, Manchester

#### ❌ Pure Inference Method:

```
Based on your budget, I recommend:
1. Ford Focus 1.6 (2014-2016) - £6k-£8k
2. Vauxhall Astra 1.4 (2013-2015) - £5k-£8k
3. Peugeot 308 (2014-2016) - £6k-£8k
```

**Problems:**
- Don't know how many actually for sale
- Price range may be outdated
- May recommend scarce models

#### ✅ Data-Driven Method:

```
Searched Manchester area under £8,000, results:

1. Ford Focus - Only found 8, most are high-mileage diesel versions (not recommended)
2. Vauxhall Astra - Found 15, but average mileage 78k, fair condition
3. Peugeot 308 - Only 3, insufficient choices

【Better Discovery】Actual search found:
- Honda Civic (2012-2015) - 23 for sale, average £7,200
- Toyota Auris (2013-2016) - 18 for sale, average £7,600
- Mazda 3 (2014-2016) - 12 for sale, average £7,800

Recommend: Honda Civic - Most choices, better reliability, more reasonable actual price
```

**Advantages:**
- ✅ Know real supply situation
- ✅ Avoid recommending scarce models
- ✅ Discover better actual options
- ✅ Provide current market prices

---

## 🛠️ Troubleshooting

### Issue 1: CLI Execution Fails

**Error:** `ModuleNotFoundError: No module named 'requests'`

**Solution:**
```bash
cd ~/.cursor/skills/uk-car-recommender
pip install -r requirements.txt
```

### Issue 2: Empty Search Results

**Possible Causes:**
- Search criteria too strict
- Indeed no matching vehicles in that area

**Solution:**
1. Relax conditions (raise budget cap, expand area, reduce filter conditions)
2. Try nationwide search `--location uk`
3. Adjust year/mileage limits

### Issue 3: JSON Parsing Error

**Solution:**
- Check if CLI output is valid JSON
- Look at error messages
- Confirm network connection is normal

### Issue 4: Search Too Slow

**Optimization:**
- Reduce number of search strategies (3 instead of 5)
- Lower `--limit` parameter (10 instead of 15)
- Avoid multiple searches in same conversation

---

## 📚 Related Documentation

- [GUMTREE_SEARCH.md](GUMTREE_SEARCH.md) - CLI detailed parameter documentation
- [WORKFLOW_GUIDE.md](WORKFLOW_GUIDE.md) - Complete car buying process
- [UK_MARKET_REFERENCE.md](UK_MARKET_REFERENCE.md) - Market reference data

---

## 🎓 Summary

**Core of Data-Driven Recommendations:**

1. **Always search first, then recommend** - Let the market tell you the answer
2. **Transparent data** - Tell users based on how many real vehicles
3. **Combine knowledge** - Use reliability knowledge to filter and rank
4. **Show evidence** - Provide actual listing samples
5. **Verifiable** - Give users search links to verify themselves

Such recommendations:
- ✅ More accurate (based on current market)
- ✅ More credible (supported by real data)
- ✅ More practical (recommended vehicles actually exist)
- ✅ More responsible (avoid misleading users)
