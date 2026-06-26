---
name: smart-price-monitor
description: >
  Monitor product prices, stock levels, and market data across any website or API, with intelligent
  alerts and trend analysis. Use this skill whenever the user wants to track prices, monitor deals,
  compare prices across stores, get notified about price drops, watch for restocks, track competitor
  pricing, monitor exchange rates, or build any kind of real-world data monitoring pipeline. Also
  triggers on: "price alert", "deal tracker", "price history", "price comparison", "stock alert",
  "restock notification", "market watch", "price scraping", "e-commerce monitoring", "competitor
  pricing", "price intelligence", "deal finder", "sale alert", "lowest price", "price trend".
  This is the go-to skill for any real-world data extraction and monitoring task.
---

# Smart Price & Deal Monitor

A comprehensive skill for monitoring real-world prices, deals, and market data with intelligent
alerting and trend analysis. Turns your AI agent into a vigilant price-watching assistant that
tracks changes, spots deals, and surfaces insights automatically.

## What This Skill Does

This skill enables three core workflows:

1. **Price Monitoring** — Track product prices across e-commerce sites and APIs over time
2. **Deal Detection** — Identify price drops, sales, and deals that match user criteria
3. **Market Intelligence** — Analyze pricing trends, competitor pricing, and market dynamics

## Quick Start

When the user asks to monitor a price or track a deal, follow this sequence:

1. Ask what they want to monitor (product URL, search term, or data source)
2. Set up the monitoring target configuration
3. Define alert thresholds (price drop %, absolute price target, restock)
4. Choose delivery method (file report, notification summary, or dashboard)
5. Run the first data collection to establish a baseline

## Core Workflow

### Step 1: Identify Monitoring Targets

Ask the user for one or more of:
- **Product URLs** — Direct links to products on any e-commerce site
- **Search queries** — "iPhone 16 Pro Max 256GB" across multiple retailers
- **API endpoints** — REST APIs that return pricing data (stocks, crypto, commodities)
- **Competitor pages** — Competitor product/pricing pages to watch

Store targets in a `monitors.json` configuration file:

```json
{
  "monitors": [
    {
      "id": "monitor-001",
      "name": "iPhone 16 Pro Max - Amazon",
      "type": "product_url",
      "source": "https://amazon.com/dp/B0EXAMPLE",
      "check_interval": "6h",
      "alert_rules": {
        "price_drop_pct": 5,
        "price_target": 899,
        "restock_alert": true
      },
      "history": []
    }
  ],
  "settings": {
    "currency": "USD",
    "timezone": "America/Los_Angeles",
    "report_format": "markdown"
  }
}
```

### Step 2: Data Collection

For each monitoring target, extract pricing data using the appropriate method:

**Web Scraping Approach** (for product URLs):
1. Fetch the page using available web tools (WebFetch, browser tools, or curl)
2. Parse the HTML/markdown to extract: current price, original price, availability, seller, ratings
3. Handle common anti-bot patterns: rotate user agents, respect robots.txt, add delays
4. Store extracted data with timestamp in the history array

**API Approach** (for structured data sources):
1. Call the API endpoint with appropriate headers
2. Parse JSON/XML response for price fields
3. Handle pagination if needed
4. Normalize data into standard format

**Search-Based Approach** (for price comparison):
1. Search for the product across multiple retailers
2. Extract prices from search results
3. Rank by price, factoring in shipping and seller reputation
4. Build a comparison table

### Step 3: Trend Analysis

After collecting data points over time, analyze trends:

- **Price Direction** — Is the price trending up, down, or stable?
- **Volatility** — How much does the price fluctuate? High volatility = wait for a dip
- **Seasonality** — Does this product follow seasonal pricing? (holidays, back-to-school, etc.)
- **Best Time to Buy** — Based on historical data, when is the optimal purchase window?
- **Deal Score** — Rate current price vs. historical average (0-100, where 100 = best deal ever)

Calculate a simple Deal Score:
```
deal_score = max(0, min(100, ((historical_avg - current_price) / historical_avg) * 200 + 50))
```

### Step 4: Alert Generation

Generate alerts when conditions are met:

**Alert Types:**
- `PRICE_DROP` — Price decreased by more than threshold percentage
- `TARGET_REACHED` — Price hit or fell below the user's target price
- `RESTOCK` — Previously out-of-stock item is now available
- `NEW_LOW` — All-time lowest price detected
- `DEAL_EXPIRING` — Sale or deal is ending soon
- `COMPETITOR_CHANGE` — Competitor changed their pricing

**Alert Format:**
```markdown
## Price Alert: [Product Name]

**Status:** PRICE_DROP
**Current Price:** $849.99 (was $999.99)
**Drop:** -15.0% ($150.00 savings)
**Deal Score:** 87/100
**Historical Low:** $829.99 (Black Friday 2025)
**Recommendation:** Strong buy — this is within 2% of the all-time low.

[Link to product](url)
```

### Step 5: Reporting

Generate reports in the user's preferred format:

**Daily Summary Report:**
- All monitored items with current prices
- Items with price changes in the last 24 hours
- Top deals (sorted by deal score)
- Items approaching target prices

**Trend Report (Weekly/Monthly):**
- Price charts showing trends for each item (ASCII or HTML)
- Average prices by category
- Best deals found this period
- Recommendations for when to buy vs. wait

**Comparison Report:**
- Side-by-side pricing across retailers
- Total savings potential
- Shipping cost comparison
- Seller reliability notes

## Data Storage

Store all monitoring data in a structured directory:

```
price-monitor-data/
├── monitors.json          # Active monitoring configurations
├── history/
│   ├── monitor-001.json   # Price history for each monitor
│   └── monitor-002.json
├── reports/
│   ├── daily-2026-04-06.md
│   └── weekly-2026-W14.md
└── alerts/
    └── alerts-2026-04-06.json
```

### History Entry Format

Each price check creates a history entry:

```json
{
  "timestamp": "2026-04-06T14:30:00Z",
  "price": 849.99,
  "original_price": 999.99,
  "currency": "USD",
  "in_stock": true,
  "seller": "Amazon",
  "shipping": "Free",
  "condition": "New",
  "coupon": null,
  "source_url": "https://..."
}
```

## Advanced Features

### Multi-Currency Support
When monitoring across regions, normalize prices to the user's preferred currency using
current exchange rates. Always show both the original and converted prices.

### Competitor Intelligence Mode
For business users monitoring competitor pricing:
1. Track competitor product catalog changes (new products, discontinued items)
2. Monitor pricing strategy shifts (frequent sales vs. everyday low price)
3. Generate competitive positioning reports
4. Alert on significant competitor price moves

### Deal Aggregation
Combine multiple data sources to find the best overall deal:
- Base price across retailers
- Available coupons and promo codes (search for "[product] coupon code [year]")
- Cashback opportunities
- Credit card rewards optimization
- Bundle deals and accessories

## Error Handling

- If a page fails to load, retry up to 3 times with exponential backoff
- If price extraction fails (page layout changed), flag the monitor as "needs attention"
- If an API returns errors, log the error and continue with other monitors
- Always validate extracted prices (not $0, not absurdly high, within 200% of last known price)
- If a product page returns 404, mark as "possibly discontinued" and alert user

## Integration Points

This skill works well with:
- **Scheduled tasks** — Set up recurring price checks using the schedule skill
- **Slack/Email** — Send alerts to Slack channels or email via connected MCPs
- **Spreadsheets** — Export price history to CSV/XLSX for further analysis
- **Dashboards** — Build HTML dashboards showing all monitored items

## Example Interactions

**Example 1: Simple Price Watch**
User: "Watch this laptop for me and let me know if it drops below $1200"
→ Set up a single product monitor with target price alert at $1200

**Example 2: Multi-Retailer Comparison**
User: "Find me the best deal on AirPods Pro 2 across all major retailers"
→ Search Amazon, Best Buy, Walmart, Target; build comparison table; set up ongoing monitoring

**Example 3: Competitor Pricing Analysis**
User: "Track how our competitor prices their SaaS plans and alert me when they change"
→ Set up multiple competitor page monitors; generate weekly competitive pricing report

**Example 4: Market Data Tracking**
User: "Monitor gold prices and alert me when it drops below $2000/oz"
→ Set up API-based monitor for commodity prices with threshold alert

## Korean Market Support (한국 시장 지원)

For Korean e-commerce monitoring:
- Supports Coupang, Naver Shopping, 11st, G-Market, Auction
- Korean Won (KRW) as base currency option
- Korean-language alert generation
- 네이버 최저가 비교 integration
- 쿠팡 로켓배송 availability tracking
