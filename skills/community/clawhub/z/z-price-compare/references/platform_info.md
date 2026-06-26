# Platform Information Reference (Safe Mode)

This file contains general information about major Chinese e-commerce platforms.
**All information is publicly available and does not involve any scraping techniques.**

---

## Platform Overview

### 🟦 JD.com (京东)
- **Website**: `https://www.jd.com`
- **Main URL Pattern**: `https://item.jd.com/1000xxxxx.html`
- **Characteristics**: 
  - Self-operated (自营) items have highest trust
  - Fast delivery (often next-day)
  - Strong customer service
- **Best For**: Electronics, high-value items, urgent purchases
- **Note**: Some prices require login to view

### 🔴 Taobao (淘宝)  
- **Website**: `https://www.taobao.com`
- **Main URL Pattern**: `https://detail.tmall.com/item.htm?id=xxxxx`
- **Characteristics**:
  - Largest product variety
  - Mix of C2C and B2C sellers
  - Price varies significantly by seller
- **Best For**: Unique items, fashion, household goods
- **Note**: Quality varies widely between sellers

### 🟧 Tmall (天猫)
- **Website**: `https://www.tmall.com`
- **Main URL Pattern**: `https://detail.tmall.com/item.htm?id=xxxxx`
- **Characteristics**:
  - Official brand flagship stores only
  - Higher prices but guaranteed authenticity
  - Better return policies
- **Best For**: Brand-name products, gifts
- **Note**: Most reliable for authentic products

### 🟢 Pinduoduo (拼多多)
- **Website**: `https://www.pinduoduo.com`
- **Mobile URL**: `https://mobile.yangkeduo.com`
- **Characteristics**:
  - Group buying discounts
  - "Billions Subsidy" (百亿补贴) program
  - Lowest prices generally
- **Best For**: Budget-conscious shopping, daily items
- **Note**: Verify seller credentials for expensive items

### ⚪ 1688
- **Website**: `https://www.1688.com`
- **Characteristics**:
  - Wholesale/B2B platform
  - Factory direct prices
  - Minimum order quantities common
- **Best For**: Bulk purchasing, resellers
- **Note**: Not optimized for single-item retail

### 🟣 Suning (苏宁易购)
- **Website**: `https://www.suning.com`
- **Characteristics**:
  - Home appliances specialization
  - Online-offline integrated
  - Installation services included
- **Best For**: Large appliances, electronics
- **Note**: Good for items needing installation

### 🟡 Yiwugou (义乌购)
- **Website**: `https://www.yiwugou.com`
- **Characteristics**:
  - Small commodities focus
  - Direct from Yiwu wholesale market
  - Very low unit prices
- **Best For**: Small items, craft supplies, accessories
- **Note**: Check quality carefully for higher-priced items

### 🔴 Vipshop (唯品会)
- **Website**: `https://www.vipshop.com`
- **Characteristics**:
  - Flash sales and time-limited offers
  - Brand clearance focus
  - Deep discounts on seasonal items
- **Best For**: Clothing, shoes, bags at discount
- **Note**: Limited stock, act fast on good deals

---

## Search Query Patterns

When using web_search to find products:

```
# General search
"商品名称 site:jd.com"
"商品名称 site:tmall.com"

# Multiple platforms
"商品名称 site:jd.com OR site:tmall.com OR site:pdd.com"

# With price constraint
"商品名称 site:jd.com ¥500-1000"

# Specific model
"华为 MateBook 14 2024 site:jd.com"
```

---

## Trust Indicators

When reviewing search results, look for:

| Indicator | What It Means |
|-----------|---------------|
| 自营 (Self-operated) | Platform guarantees authenticity |
| 官方旗舰店 (Flagship Store) | Official brand store |
| 百亿补贴 (Billions Subsidy) | Platform-backed discount program |
| XX万 + 销量 | High sales volume (indicates popularity) |
| XX% 好评率 | High positive rating percentage |

---

## Safety Guidelines

✅ **DO:**
- Use search results as initial research
- Verify final prices on official platforms
- Click through to official sites before purchasing
- Look for trust indicators in search snippets
- Accept that search data may be slightly outdated

❌ **DON'T:**
- Treat search snippets as authoritative final prices
- Share collected pricing data commercially
- Attempt to bypass login requirements
- Assume all displayed products are currently in stock

---

## Alternative Data Sources

For commercial use or more accurate data, consider official APIs:

| Platform | Program | Description |
|----------|---------|-------------|
| JD | 京东联盟 | Affiliate program with API access |
| Alibaba/Tmall | 阿里妈妈 | Marketing and data services |
| Pinduoduo | 多多进宝 | Promotion program with API |

These provide legitimate, compliant access to pricing and product data.

---

_This reference is for educational purposes only. All information is gathered from public sources and does not involve any technical extraction methods._
