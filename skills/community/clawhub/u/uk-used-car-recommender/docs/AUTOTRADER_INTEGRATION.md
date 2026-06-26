# AutoTrader Integration Guide

AutoTrader is the UK's largest and most professional used car trading platform, providing more detailed vehicle information and more accurate pricing data than Gumtree.

---

## 📊 Why Use AutoTrader?

### AutoTrader vs Gumtree

| Feature | AutoTrader | Gumtree |
|---------|-----------|---------|
| **Positioning** | Professional automotive platform | General classified ads |
| **Listing Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Price Accuracy** | Very accurate (with valuation) | Variable pricing |
| **Vehicle Information** | Complete specs + history | Basic parameters |
| **Dealers** | Many certified dealers | Mixed |
| **Search Filters** | Very detailed | Basic filtering |
| **Valuation Data** | ✅ Includes market valuation | ❌ None |
| **Rating System** | ✅ Retail Rating | ❌ None |

**Conclusion:** Dual-platform search provides the most comprehensive market data!

---

## 🚀 Quick Start

### Method 1: Using autotrader_scraper Library (Recommended) ⭐⭐⭐⭐⭐

**Installation:**
```bash
pip install autotrader_scraper
```

**Usage:**
```python
from cars.autotrader import search_autotrader

result = search_autotrader(
    make='Toyota',
    model='Yaris',
    postcode='SW1A1AA',  # London postcode
    radius=10,           # 10 mile radius
    max_price=10000,
    min_year=2016,
    limit=10
)

print(f"Found {result['total']} vehicles")
for car in result['items']:
    print(f"{car['title']} - {car['price_display']}")
```

---

### Method 2: Multi-Platform Search CLI

Search Gumtree + AutoTrader simultaneously:

```bash
python scripts/multi_platform_cli.py search \
  --make toyota \
  --model yaris \
  --postcode SW1A1AA \
  --max-price 10000 \
  --platforms gumtree,autotrader \
  --limit 10
```

**Example Output:**
```json
{
  "ok": true,
  "source": "multi_platform",
  "platforms": {
    "gumtree": {
      "ok": true,
      "total": 15
    },
    "autotrader": {
      "ok": true,
      "total": 23
    }
  },
  "total": 38,
  "items": [...]
}
```

---

## 📋 Search Parameter Comparison

### Gumtree Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--location` | City name or "uk" | `London`, `Manchester`, `uk` |
| `--distance` | Search radius (miles) | `10`, `20`, `50` |
| `--make` | Brand (lowercase) | `toyota`, `honda` |
| `--model` | Model (lowercase) | `yaris`, `civic` |
| `--max-price` | Maximum price | `10000` |
| `--fuel-type` | Fuel type | `petrol`, `hybrid_electric` |
| `--transmission` | Transmission | `manual`, `automatic` |

### AutoTrader Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--postcode` | UK postcode | `SW1A1AA`, `M1 1AE` |
| `--radius` | Search radius (miles) | `10`, `20`, `50` |
| `--make` | Brand (uppercase) | `TOYOTA`, `HONDA` |
| `--model` | Model (uppercase) | `YARIS`, `CIVIC` |
| `--max-price` | Maximum price | `10000` |
| `--min-year` | Earliest year | `2016` |
| `--max-year` | Latest year | `2020` |
| `--fuel-type` | Fuel type | `petrol`, `hybrid` |
| `--transmission` | Transmission | `manual`, `automatic` |

---

## 🎯 Integration with Data-Driven Recommendations

### Update Search Strategy

In the **Step 3: Execute Parallel Searches** section of `docs/DATA_DRIVEN_RECOMMENDATION.md`:

**Old Method (Gumtree only):**
```bash
python scripts/cli.py search \
  --make toyota --model yaris \
  --max-price 10000 --location London
```

**New Method (Dual-platform):**
```bash
python scripts/multi_platform_cli.py search \
  --make toyota --model yaris \
  --max-price 10000 \
  --postcode SW1A1AA \
  --platforms gumtree,autotrader
```

### Recommendation Output Example

```
🔍 Based on real-time London market research (2026-05-07)

Searched both Gumtree + AutoTrader platforms:

📊 Market Analysis Results:

**Toyota Yaris Hybrid**
- Gumtree: 45 for sale, average £9,200
- AutoTrader: 67 for sale, average £9,450
- Total: 112 for sale, combined average £9,350

**Honda Jazz**
- Gumtree: 23 for sale, average £8,800
- AutoTrader: 34 for sale, average £9,100
- Total: 57 for sale, combined average £8,980

---

【Recommended】Honda Jazz (2016-2019)
📊 Real Market Data (Dual-platform):
- ✓ 57 vehicles for sale (Gumtree 23 + AutoTrader 34)
- 💷 Combined price range: £6,995 - £9,950 (average £8,980)
- 📊 Price validation: Consistent across platforms, reliable data
- 🏪 Seller types: 70% Trade, 30% Private

⭐ Why recommended:
1. **Dual-platform validation** - Price data cross-validated, more reliable
2. **Abundant choices** - 57 for sale, wide selection
3. **Best value** - £1,020 below budget
4. **Legendary reliability** - What Car? ⭐⭐⭐⭐⭐

Here are 5 actual vehicles for sale (from both platforms):
[Display listings]
```

---

## 🛠️ Implementation Details

### Data Standardization

Both platforms return different data formats, requiring standardization:

```python
# Standardized output format
normalized_item = {
    "listing_id": ...,
    "title": ...,
    "price": int,
    "price_display": "£9,995",
    "location": ...,
    "url": ...,
    "year": "2019",
    "mileage": "57,000 miles",
    "fuel_type": "Petrol",
    "transmission": "Automatic",
    "seller_type": "Trade" / "Private",
    "image_url": ...,
    "source": "gumtree" / "autotrader",  # Source identifier
}
```

### Deduplication Strategy

The same vehicle may be listed on both platforms, requiring deduplication:

```python
def deduplicate_listings(items):
    """Deduplicate based on title, price, and mileage similarity"""
    unique_items = []
    seen = set()
    
    for item in items:
        # Generate fingerprint
        fingerprint = (
            item.get('title', '').lower(),
            item.get('price'),
            item.get('mileage')
        )
        
        if fingerprint not in seen:
            seen.add(fingerprint)
            unique_items.append(item)
    
    return unique_items
```

---

## 📈 Data Quality Comparison

### Gumtree Data Characteristics

**Advantages:**
- ✅ More private seller listings
- ✅ Potentially lower prices
- ✅ More local small dealers

**Disadvantages:**
- ⚠️ Information may be incomplete
- ⚠️ Price accuracy varies
- ⚠️ Some fake or outdated listings

### AutoTrader Data Characteristics

**Advantages:**
- ✅ Very detailed vehicle information
- ✅ High price accuracy
- ✅ Many certified dealers
- ✅ Includes valuation and rating data

**Disadvantages:**
- ⚠️ Prices usually slightly higher
- ⚠️ Fewer private seller listings

---

## 🎓 Best Practices

### 1. Application in Data-Driven Recommendations

```python
def generate_search_strategies(user_requirements):
    strategies = []
    
    for model in ["Toyota Yaris", "Honda Jazz", "Mazda 2"]:
        # Generate dual-platform search for each model
        strategies.append({
            "model": model,
            "platforms": ["gumtree", "autotrader"],
            "params": {
                "max_price": user_requirements["budget"],
                "postcode": user_requirements["postcode"],
                "location": user_requirements["city"]
            }
        })
    
    return strategies
```

### 2. Price Validation

```python
def verify_pricing(gumtree_avg, autotrader_avg):
    """Cross-validate price data"""
    
    if not gumtree_avg or not autotrader_avg:
        return "Single source, cannot validate"
    
    diff_percent = abs(gumtree_avg - autotrader_avg) / autotrader_avg * 100
    
    if diff_percent < 5:
        return "✅ Prices consistent, data reliable"
    elif diff_percent < 10:
        return "⚠️ Slight price difference (normal range)"
    else:
        return f"⚠️ Large price discrepancy ({diff_percent:.1f}%), requires further investigation"
```

### 3. Priority Ranking

```python
def calculate_score(item):
    score = 0
    
    # Source weighting
    if item['source'] == 'autotrader':
        score += 10  # AutoTrader has higher data quality
    
    # Seller type
    if item['seller_type'] == 'Trade':
        score += 5  # Dealers are more reliable
    
    # Price reasonableness
    # ... other scoring logic
    
    return score
```

---

## ⚠️ Cautions

### 1. API Limitations

- AutoTrader may have anti-scraping mechanisms
- Use reasonable request intervals (1-2 seconds)
- Don't make frequent large-volume requests

### 2. Dependency Management

```bash
# Basic dependencies (required)
pip install requests beautifulsoup4 lxml

# AutoTrader support (recommended)
pip install autotrader_scraper
```

If `autotrader_scraper` is not installed, will automatically fall back to backup scraper (limited features).

### 3. Postcode vs City Name

- **Gumtree** uses city names or "uk"
- **AutoTrader** uses UK postcodes

`multi_platform_cli.py` automatically converts:
```python
postcode "SW1A1AA" → location "London"  # For Gumtree
```

---

## 🔧 Troubleshooting

### Issue 1: autotrader_scraper Not Installed

**Error:**
```
ModuleNotFoundError: No module named 'autotrader_scraper'
```

**Solution:**
```bash
pip install autotrader_scraper
```

Or, the system will automatically use the backup scraper (data may be incomplete).

### Issue 2: AutoTrader Search Fails

**Possible Causes:**
- Network connection issues
- AutoTrader website structure changes
- Anti-scraping mechanisms

**Solutions:**
1. Check network connection
2. Update `autotrader_scraper` library
3. Use Gumtree only: `--platforms gumtree`

### Issue 3: Empty Search Results

**Check:**
- Is the postcode correct (UK postcode format)
- Are search conditions too strict
- Try expanding search radius

---

## 📚 Related Resources

**Official Resources:**
- [AutoTrader UK](https://www.autotrader.co.uk/)
- [AutoTrader Connect API](https://developers.autotrader.co.uk/api)

**Open Source Projects:**
- [autotrader_scraper](https://github.com/suhailidrees/autotrader_scraper)

**Related Documentation:**
- [DATA_DRIVEN_RECOMMENDATION.md](DATA_DRIVEN_RECOMMENDATION.md) - Data-driven recommendation methodology
- [GUMTREE_SEARCH.md](GUMTREE_SEARCH.md) - Gumtree search guide

---

## 🎯 Summary

**AutoTrader Integration Advantages:**
1. ✅ **More Comprehensive** - Covers the UK's two largest used car platforms
2. ✅ **More Accurate** - AutoTrader price data more reliable
3. ✅ **Complementary Validation** - Cross-validate prices and availability
4. ✅ **More Professional** - AutoTrader provides valuation and rating data

**Recommended Use Cases:**
- 🔥 **Data-driven recommendations** - Get most comprehensive market data
- 🔥 **Price validation** - Cross-validate price reasonableness
- 🔥 **Professional buyers** - Need detailed vehicle information and valuation data

**Get Started:**
```bash
# Install AutoTrader support
pip install autotrader_scraper

# Run dual-platform search
python scripts/multi_platform_cli.py search \
  --make toyota --model yaris \
  --postcode SW1A1AA \
  --max-price 10000 \
  --platforms gumtree,autotrader
```

---

*Last Updated: 2026-05-07*
