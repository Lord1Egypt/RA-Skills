# Wine Data Source Reference

This document provides detailed reference information for the data sources used by the Wine Info Search skill. Load this document when you need to understand API response structures, troubleshoot scraping issues, or extend the skill's capabilities.

## Data Source Status Summary (as of 2025-04)

| Source | Direct Access | WebFetch | Firecrawl | Status | Data Richness |
|--------|--------------|----------|-----------|--------|---------------|
| Wine-Searcher | ❌ 403 | ✅ Works | N/A | **Primary** | ★★★★★ Ratings, prices, vintages, tasting notes, critics |
| Vivino (Firecrawl) | ❌ Timeout (CN) | ❌ Timeout | ✅ Works | **Secondary (restored)** | ★★★★☆ Ratings, taste profile, grapes, food pairing |
| Wikipedia API | ✅ Works | N/A | N/A | **Tertiary (v1.5)** | ★★★☆☆ Wine & winery background, history |
| Open Food Facts | ⚠️ 503 (intermittent) | ⚠️ 503 | N/A | Supplementary | ★★☆☆☆ Basic metadata only (ABV, grape, image) |
| Vivino API | ❌ 403 Forbidden | N/A | N/A | **Deprecated** | N/A — blocked since 2025 |
| Vivino Web | ❌ Timeout (CN) | ❌ Timeout | N/A | **Deprecated** | N/A — blocked from China |

## 0.5. Wikipedia API (Tertiary Data Source — Wine & Winery Background, v1.5)

Wikipedia provides free, structured encyclopedic content about wines, wineries, and wine regions. The script uses the MediaWiki API to search and extract article summaries, providing background information that is not available from rating/price-focused sources.

### Configuration

No API key required. Both English and Chinese Wikipedia are accessible from China mainland.

### Wikipedia Search API

**Endpoint**: `GET https://en.wikipedia.org/w/api.php` (English) / `GET https://zh.wikipedia.org/w/api.php` (Chinese)

**Request Parameters**:
```
action=query
list=search
srsearch=<query>
srlimit=3
format=json
utf8=1
```

**Example**: `https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=Chateau+Lafite+Rothschild+wine&srlimit=3&format=json&utf8=1`

**Response**:
```json
{
  "query": {
    "search": [
      {
        "ns": 0,
        "title": "Château Lafite Rothschild",
        "pageid": 950914,
        "snippet": "Château Lafite Rothschild is a Premier Grand Cru Classé estate..."
      }
    ]
  }
}
```

### Wikipedia Extract API

**Endpoint**: `GET https://en.wikipedia.org/w/api.php`

**Request Parameters**:
```
action=query
titles=<article_title>
prop=extracts
exsentences=10
exintro=1
explaintext=1
format=json
utf8=1
```

**Example**: `https://en.wikipedia.org/w/api.php?action=query&titles=Ch%C3%A2teau+Lafite+Rothschild&prop=extracts&exsentences=10&exintro=1&explaintext=1&format=json&utf8=1`

**Response**:
```json
{
  "query": {
    "pages": {
      "950914": {
        "pageid": 950914,
        "ns": 0,
        "title": "Château Lafite Rothschild",
        "extract": "Château Lafite Rothschild is a wine estate in France..."
      }
    }
  }
}
```

### Data Available from Wikipedia

| Data Field | Description | Example |
|------------|-------------|---------|
| Wine background | Historical info about the wine | Origin, founding year, classification, notable events |
| Winery background | Info about the producer/estate | Founding, ownership, vineyard details, production methods |
| Region appellation | Geographic and legal classification | Bordeaux AOC, Pauillac appellation |
| Article URL | Link to full Wikipedia article | https://en.wikipedia.org/wiki/Château_Lafite_Rothschild |

### How the Script Uses Wikipedia

The script's `fetch_wine_background()` function uses a multi-strategy approach:

1. **Wine search**: Searches for `"<wine_name> wine"` or `"<query_en> wine"` on English Wikipedia first, then Chinese Wikipedia with `"<query_cn> 葡萄酒"`.
2. **Winery search**: Searches for `"<winery_name> winery"` on English Wikipedia, or `"<query_cn> 酒庄"` on Chinese Wikipedia.
3. **Filtering**: Skips disambiguation pages, lists, and non-wine-related articles by checking for wine keywords in snippets.
4. **Fallback**: If English Wikipedia returns no results, tries Chinese Wikipedia, and vice versa.
5. **Integration**: Background info is displayed in the new "🏛️ 酒款与酒庄背景" section, with links to full articles.

### Vintage Recommendations (v1.5)

The script enhances the existing vintage comparison data with recommendation labels:

| Rating Range | Label | Emoji | Description |
|-------------|-------|-------|-------------|
| ≥ 4.5 | 卓越 (Outstanding) | 🌟 | Exceptional vintage, highly recommended |
| 4.0 - 4.4 | 优秀 (Very Good) | ⭐ | Great vintage, recommended purchase |
| 3.5 - 3.9 | 良好 (Good) | 👍 | Good quality, worth trying |
| 3.0 - 3.4 | 一般 (Average) | 👌 | Average quality |
| < 3.0 | 不佳 (Below Average) | ⚠️ | Below average, not recommended |

**Confidence notes**:
- < 20 ratings: "(评价数较少)" — low confidence
- 20-99 ratings: "(评价数偏少)" — moderate confidence

**Buying advice**: When the user specifies a vintage year, the script compares it against the best vintages and provides specific recommendations.

## 0. Firecrawl → Vivino (Secondary Data Source, Restored Access)

Firecrawl is a web scraping service that provides US-based proxy IPs and JavaScript rendering. It enables access to Vivino from China, bypassing Vivino's IP blockade. This is the **recommended secondary data source** for China-based users.

### Configuration

| Method | How to Set |
|--------|-----------|
| Environment variable | `set FIRECRAWL_API_KEY=fc-xxxx` (Windows) / `export FIRECRAWL_API_KEY=fc-xxxx` (Linux/macOS) |
| Command-line argument | `python wine_search.py "拉菲" --firecrawl-key fc-xxxx` |

Free tier: **500 requests/month**. Register at [firecrawl.dev](https://firecrawl.dev).

### Firecrawl Scrape API

**Endpoint**: `POST https://api.firecrawl.dev/v1/scrape`

**Request Body**:
```json
{
  "url": "https://www.vivino.com/search/wines?q=Lafite+Legende",
  "formats": ["markdown"],
  "waitFor": 5000
}
```

**Headers**:
```
Content-Type: application/json
Authorization: Bearer fc-xxxx
```

**Response**:
```json
{
  "success": true,
  "data": {
    "markdown": "... (Vivino search results as markdown) ...",
    "metadata": {
      "title": "Search results for Lafite Legende - Vivino",
      "description": "...",
      "sourceURL": "https://www.vivino.com/search/wines?q=Lafite+Legende"
    }
  }
}
```

### Firecrawl Search API

**Endpoint**: `POST https://api.firecrawl.dev/v1/search`

**Request Body**:
```json
{
  "query": "Lafite Legende Bordeaux site:vivino.com",
  "limit": 5
}
```

**Response**:
```json
{
  "success": true,
  "data": [
    {
      "title": "Légende R Bordeaux Rouge - Vivino",
      "url": "https://www.vivino.com/wines/1138219",
      "description": "...",
      "markdown": "..."
    }
  ]
}
```

### Data Available from Vivino (via Firecrawl)

When scraping Vivino search pages via Firecrawl, the script parses the returned markdown to extract:

| Data Field | Description | Example |
|------------|-------------|---------|
| Wine name | Full wine name | "Les Légendes R Bordeaux Rouge" |
| Rating | Community rating (1-5) | 3.6 |
| Number of ratings | Rating count | 10,548 |
| Price | Reference price | $17.99 |
| Currency | Price currency | USD |
| Region | Wine region | Bordeaux |
| Country | Country of origin | France |
| Wine type | Red/White/Sparkling/etc. | Red wine |
| Wine ID | Vivino wine ID (for detail page) | 1138219 |
| Vintage year | Year if specified | 2020 |

When scraping Vivino detail pages, additionally available:

| Data Field | Description | Example |
|------------|-------------|---------|
| Grape varieties | With blending percentages | Cabernet Sauvignon 60%, Merlot 40% |
| Taste profile | Body/tannin/acidity/sweetness (1-5 scale) | body: 3, tannin: 3, acidity: 3, sweetness: 1 |
| Food pairing | Suggested food pairings | Beef, Lamb, Game |
| Description | Wine description | "A classic Bordeaux blend..." |
| Winery | Winery name | "Domaines Barons de Rothschild (Lafite)" |

### How the Script Uses Firecrawl

The script's cascading fallback strategy now starts with Firecrawl:

1. **`firecrawl_vivino_search(query, year, per_page)`** — Scrapes `vivino.com/search/wines?q=<query>` via Firecrawl. Parses the returned markdown using `_parse_vivino_markdown_search()` to extract wine results.

2. **`firecrawl_vivino_detail(wine_id)`** — Scrapes `vivino.com/wines/<wine_id>` via Firecrawl. Parses the returned markdown using `_parse_vivino_markdown_detail()` to extract grape varieties, taste profile, food pairing, and description.

3. If Firecrawl is not configured (no API key), the script skips to the next fallback (Vivino API, which returns 403).

### Markdown Parsing Strategies

The script uses two strategies to parse Vivino markdown:

**Strategy 1 (Block-based)**: Splits markdown into blocks (double-newline separated), then for each block:
- Looks for rating patterns (`\b[1-4]\.\d\b`)
- Looks for ratings count (`N ratings`)
- Looks for price (`$XX.XX`)
- Extracts wine name from the first substantial line
- Extracts region/country, wine type, wine ID from URL patterns

**Strategy 2 (Line-by-line)**: If Strategy 1 yields nothing, scans each line for:
- Rating values (1.0-5.0)
- Adjacent lines containing wine names
- Context window for price/ratings count

**Detail page parsing**: Looks for:
- Grape varieties with percentages (`Cabernet Sauvignon · 70%`)
- Taste profile keywords (`body`, `tannin`, `acidity`, `sweetness`)
- Food pairing sections
- Description sections
- Known grape names (29 varieties hardcoded)

## 1. Wine-Searcher (Primary Data Source via WebFetch)

Wine-Searcher is the most reliable external data source for wine information. Direct HTTP access returns 403, but WebFetch tool works reliably.

### Access Method

**URL Pattern**: `https://www.wine-searcher.com/find/{wine_name_with_plus}`

**Example**: `https://www.wine-searcher.com/find/lafite+rothschild+2018`

### Data Available from Wine-Searcher (via WebFetch)

Wine-Searcher provides extremely rich data including:

| Data Field | Description | Example |
|------------|-------------|---------|
| Wine name | Full wine name | "Chateau Lafite Rothschild" |
| Vintage | Year | 2018 |
| Region/Appellation | Wine region | Pauillac, Médoc, Bordeaux, France |
| Grape variety/blends | With percentages | "91% Cabernet Sauvignon, 8.5% Merlot, 0.5% Petit Verdot" |
| Style | Wine style | "Red - Savory and Classic" |
| Average price | Market reference price | $1,183 / 750ml (ex-tax) |
| Critic score | Aggregated critic rating | 98/100 |
| Number of critic reviews | Count | 19 |
| User rating | Community rating | 5/5 (39 ratings) |
| Food pairing | Suggested pairings | Beef and Venison |
| Drinking window | When to drink | 2025 - 2068 |
| Alcohol ABV | Alcohol content | 13.3 - 14.5% |
| Sweetness | Sweetness level | Dry |
| Maturation | Aging method | Oaked, French Oak |
| Winemaker | Winemaker name | Eric Kohler |
| Vintage comparison | Year × score × price table | Multiple decades of data |
| Critic reviews | Individual critic scores | Robert Parker 100/100, Wine Enthusiast 100/100, etc. |
| Producer tasting notes | Winery's own description | Detailed tasting notes |
| Merchant offers | Price listings by store | Multiple stores with prices |

### How to Use with WebFetch

The AI agent should use its WebFetch tool to visit Wine-Searcher URLs. The script outputs WebFetch-ready hints with URLs and extraction instructions.

```python
# WebFetch URL construction
query_en = "Lafite Rothschild 2018"
url = f"https://www.wine-searcher.com/find/{query_en.replace(' ', '+')}"
```

### Parsing Wine-Searcher Content

Key sections to extract from the returned markdown:

1. **Title area**: Wine name, vintage, region
2. **Price section**: "Avg Price (ex-tax) $X,XXX / 750ml"
3. **Ratings**: "X from N User Ratings" and "N / 100 N Critic Reviews"
4. **Details section**: Grape variety, ABV, food pairing, style, drinking window
5. **Vintage comparison table**: Year × Critic Score × Avg Price
6. **Critic reviews**: Individual critic names and scores

## 2. Open Food Facts API (Supplementary)

Open Food Facts is a free, public database of food products including wines. It provides basic metadata but limited rating/price data. Access may be intermittent (503 errors).

### Base URLs

| Endpoint | URL |
|----------|-----|
| Search | `https://world.openfoodfacts.org/cgi/search.pl?search_terms=<query>&search_tag=categories&page_size=<n>&json=1` |
| Product Detail | `https://world.openfoodfacts.org/api/v0/product/<barcode>.json` |

### Search Response Structure

```json
{
  "count": 42,
  "products": [
    {
      "code": "3017620422003",
      "product_name": "Château Lafite Rothschild",
      "product_name_en": "Château Lafite Rothschild",
      "brands": "Domaines Barons de Rothschild",
      "nutriments": {
        "alcohol_100g": 13.5
      },
      "grape_variety": "Cabernet Sauvignon, Merlot",
      "variety": "Cabernet Sauvignon, Merlot",
      "origin": "Pauillac, Bordeaux, France",
      "countries_tags": ["en:france"],
      "image_url": "https://...",
      "vintage": "2018"
    }
  ]
}
```

### Data Available from Open Food Facts

| Field | Description | Availability |
|-------|-------------|-------------|
| `product_name` / `product_name_en` | Wine name | ✅ Common |
| `brands` | Brand/winery | ✅ Common |
| `nutriments.alcohol_100g` | ABV (alcohol per 100g) | ⚠️ Occasional |
| `grape_variety` / `variety` | Grape variety | ⚠️ Occasional |
| `origin` | Region/origin | ⚠️ Occasional |
| `image_url` | Product image | ✅ Common |
| `vintage` | Vintage year | ⚠️ Rare |
| Rating/Price | Not available | ❌ N/A |
| Taste profile | Not available | ❌ N/A |

### API Behavior Notes

- **No authentication required** — Fully public API
- **Rate limiting** — May return 503 during high traffic
- **Data quality** — User-contributed, so wine data is often incomplete
- **No ratings/prices** — This is a food product database, not a wine-specific one

## 3. Vivino API (DEPRECATED — Blocked Since 2025)

> ⚠️ **Vivino public API is no longer accessible.** All endpoints return 403 Forbidden or 404 as of 2025.
> The script still attempts Vivino API calls as best-effort, but they will fail.
> This section is kept for reference only.

### Former Base URLs (Now 403/404)

| Endpoint | URL | Current Status |
|----------|-----|---------------|
| Search | `https://www.vivino.com/api/wines/search?q=<query>&per_page=<n>` | ❌ 403 Forbidden |
| Wine Detail | `https://www.vivino.com/api/wines/<wine_id>` | ❌ 403 Forbidden |
| Wine Vintages | `https://www.vivino.com/api/wines/<wine_id>/vintages` | ❌ 403 Forbidden |
| Web Search | `https://www.vivino.com/search/wines?q=<query>` | ❌ Timeout from China |
| api.vivino.com/search | `https://api.vivino.com/search?q=<query>` | ❌ 404 Not Found |
| api.vivino.com/wines/search | `https://api.vivino.com/wines/search?q=<query>` | ❌ 404 Not Found |

### Former Search Response Structure (For Reference Only)

```json
{
  "wines": [
    {
      "id": 12345,
      "name": "Château Lafite Rothschild",
      "winery": {
        "name": "Château Lafite Rothschild",
        "id": 678
      },
      "vintage": {
        "year": "2018"
      },
      "rating": {
        "average": 4.5,
        "ratings_count": 15234
      },
      "price": {
        "amount": 899.0,
        "currency": "USD"
      },
      "region": "Pauillac",
      "country": {
        "name": "France"
      },
      "wine_type": "red"
    }
  ]
}
```

### Former Wine Detail Response (For Reference Only)

```json
{
  "wine": {
    "id": 12345,
    "name": "Château Lafite Rothschild",
    "winery": { "name": "Château Lafite Rothschild", "id": 678 },
    "style": { "body": 4, "sweetness": 1, "tannin": 4, "acidity": 3 },
    "grape": [
      { "name": "Cabernet Sauvignon", "percentage": 70 },
      { "name": "Merlot", "percentage": 25 },
      { "name": "Cabernet Franc", "percentage": 5 }
    ],
    "food": [
      { "name": "Beef" },
      { "name": "Lamb" },
      { "name": "Game" }
    ],
    "description": "One of the most famous wines in the world...",
    "region": { "name": "Pauillac", "country": { "name": "France" } },
    "wine_type": "red",
    "rating": { "average": 4.5, "ratings_count": 15234 }
  }
}
```

**Style label mapping** (Chinese, still used for Wine-Searcher data display):

| Level | body | tannin | acidity | sweetness |
|-------|------|--------|---------|-----------|
| 1 | 轻盈 | 柔和 | 低酸 | 干型 |
| 2 | 较轻 | 较轻 | 较低 | 微甜 |
| 3 | 适中 | 适中 | 适中 | 半甜 |
| 4 | 醇厚 | 较强 | 较高 | 甜 |
| 5 | 厚重 | 强劲 | 高酸 | 极甜 |

## 2. WebFetch-Assisted Price Fetching

The script outputs WebFetch-ready price hints that the AI agent can use to fetch real-time prices. This approach is far more reliable than direct HTML scraping because WebFetch handles JavaScript rendering and anti-scraping measures.

### How It Works

1. `fetch_price_webfetch(query_cn, query_en)` generates a dict of platform hints, each containing:
   - `platform`: Platform name (e.g. "京东", "Wine-Searcher")
   - `url`: The search URL to fetch
   - `extraction_hint`: Instructions for what to extract from the page
   - `query_cn` / `query_en`: The search queries used

2. The AI agent should use its WebFetch tool to visit each URL and extract price data based on the hint.

3. If WebFetch is not available, the script also attempts direct scraping via `fetch_price_direct()` (legacy, low success rate).

### Supported Platforms for WebFetch

| Platform | URL Template | Extraction Hint |
|----------|-------------|----------------|
| 京东 | `https://search.jd.com/Search?keyword={q}&enc=utf-8` | Extract product name, ¥price, SKU link from search results |
| 天猫 | `https://list.tmall.com/search_product.htm?q={q}` | Extract product title, ¥price, shop link from search results |
| Wine-Searcher | `https://www.wine-searcher.com/find/{q_plus}` | Extract average price, price range, merchant offers |
| Vivino Shop | `https://www.vivino.com/search/wines?q={q}` | Extract wine name, rating, $price, purchase link |

### Legacy Direct Scraping (Low Success Rate)

The `fetch_price_direct(query, platform)` function attempts direct HTML scraping as a fallback:

**JD.com patterns**:
- `"p":"([\d.]+)"[^}]*"skuid":"(\d+)"` — modern JD JSON-in-HTML
- `data-price="([\d.]+)"[^>]*data-sku="(\d+)"` — classic data attributes
- Fallback: `class="gl-item"[^>]*data-sku="(\d+)"` — SKU ID only

**Wine-Searcher patterns**:
- `average[\s-]*price[^$]*\$([\d,.]+)` — average market price
- `from\s+\$([\d,.]+)` — starting price

**Limitations**: JD.com uses heavy JavaScript rendering; Wine-Searcher has anti-bot measures. Direct scraping fails more often than not.

## 3. Platform Link Generation

The script generates direct search links for the following platforms:

### Domestic Platforms (8)

| Platform | URL Template | Query Encoding |
|----------|-------------|---------------|
| 京东 | `https://search.jd.com/Search?keyword={q}&enc=utf-8` | UTF-8 |
| 天猫 | `https://list.tmall.com/search_product.htm?q={q}` | UTF-8 |
| 淘宝 | `https://s.taobao.com/search?q={q}` | UTF-8 |
| 苏宁易购 | `https://search.suning.com/{q}/` | UTF-8 |
| 拼多多 | `https://mobile.yangkeduo.com/search_result.html?search_key={q}` | UTF-8 |
| 1919吃喝 | `https://www.1919.cn/search/?keyword={q}` | UTF-8 |
| 也买酒 | `https://www.yesmywine.com/search/{q}.html` | UTF-8 |
| 酒仙网 | `https://www.jiuxian.com/search-{q}.html` | UTF-8 |

### International Platforms (8)

| Platform | URL Template | Query Encoding |
|----------|-------------|---------------|
| Vivino | `https://www.vivino.com/search/wines?q={q}` | UTF-8 |
| Vivino Shop | `https://www.vivino.com/search/wines?q={q}` | UTF-8 |
| Wine.com | `https://www.wine.com/v6/wines/?text={q}` | UTF-8 |
| Drizly | `https://drizly.com/search?q={q}` | UTF-8 |
| Total Wine | `https://www.totalwine.com/search/all?text={q}` | UTF-8 |
| Wine-Searcher | `https://www.wine-searcher.com/find/{q_with_plus}` | Plus-separated |
| Wine Spectator | `https://www.winespectator.com/search?search_type=wine&search_word={q}` | UTF-8 |
| CellarTracker | `https://www.cellartracker.com/list.asp?table=List&search={q}` | UTF-8 |
| Decántalo | `https://www.decantalo.com/uk/search?q={q}` | UTF-8 |

## 4. Troubleshooting

### "No results from any data source"
- The AI agent should use **WebFetch on Wine-Searcher** as the primary approach
- Try the alternative language (Chinese ↔ English) — the script auto-maps names
- Remove the series name to broaden the search
- Check if the brand name spelling is correct

### "Vivino API returns 403 Forbidden"
- This is **expected behavior** since 2025 — Vivino closed public API access
- The script still attempts Vivino as best-effort, then falls back to Wine-Searcher
- No fix needed; rely on Wine-Searcher via WebFetch instead

### "Open Food Facts returns 503"
- This is intermittent — the service may be temporarily overloaded
- Try again later, or rely on Wine-Searcher via WebFetch
- Open Food Facts only provides basic metadata (no ratings/prices)

### "Price scraping returns empty"
- Direct script HTTP access to Wine-Searcher and JD.com returns 403 Forbidden
- The AI agent should use **WebFetch** to visit these URLs instead
- The direct search links still work for manual price checking in a browser

### "SSL certificate errors"
- The script already disables SSL verification. If errors persist, it may be a network-level issue (corporate proxy, firewall, etc.)

### "Image OCR returns no text or garbled text"
- Ensure the image is clear and well-lit; blurry or dark photos yield poor OCR results
- For pytesseract, verify Tesseract-OCR is installed and `chi_sim` language data is available
- For easyocr, the first run downloads model files (~100MB); subsequent runs are faster
- If OCR quality is poor, try cropping the image to just the label area before searching
- As a last resort, the script falls back to filename-based hints

## 5. Bilingual Name Mapping

The script includes a `WINE_NAME_MAP` dictionary with 100+ entries mapping common Chinese wine names to English equivalents. This is used by `resolve_query_languages()` to automatically generate both `query_cn` and `query_en` for platform link generation and cross-language search retry.

### Mapping Categories

| Category | Examples |
|----------|---------|
| Famous Châteaux | 拉菲→Lafite, 木桐→Mouton, 玛歌→Margaux, 柏图斯→Pétrus |
| New World Wineries | 奔富→Penfolds, 作品一号→Opus One, 啸鹰→Screaming Eagle |
| Common Brands | 黄尾→Yellow Tail, 云雾之湾→Cloudy Bay, 蚝湾→Oyster Bay |
| Grape Varieties | 赤霞珠→Cabernet Sauvignon, 黑皮诺→Pinot Noir, 霞多丽→Chardonnay |
| Regions | 波尔多→Bordeaux, 纳帕谷→Napa Valley, 里奥哈→Rioja |
| Other Alcohol | 威士忌→Whisky, 干邑→Cognac, 麦卡伦→Macallan, 茅台→Moutai |

### How It Works

1. `resolve_query_languages(query)` detects if the query is Chinese or English
2. Looks up the query in `WINE_NAME_MAP` (CN→EN) or `_EN_TO_CN` (EN→CN)
3. Falls back to partial substring matching for compound queries (e.g. "奔富Bin 389" matches "奔富"→"Penfolds")
4. Returns `(query_cn, query_en)` — both may be the same if no mapping is found

### Extending the Map

To add new entries, edit `WINE_NAME_MAP` in `scripts/wine_search.py`:
```python
WINE_NAME_MAP["中文名"] = "English Name"
```
The reverse map `_EN_TO_CN` is auto-generated from `WINE_NAME_MAP`.

## 6. Health & Drinking Advice Module

The script includes a comprehensive health and drinking advice system.

### Age Group Definitions

| Group | Key | Age Range | Male Max (ml/day) | Female Max (ml/day) |
|-------|-----|-----------|-------------------|---------------------|
| 青年 | `young` | 18-35 | 250 | 150 |
| 中年 | `middle` | 36-55 | 200 | 120 |
| 中老年 | `senior` | 56-70 | 150 | 100 |
| 高龄 | `elderly` | 70+ | 100 | 75 |

### Supported Health Conditions (10)

| Key | Condition | Risk Level | Max (ml/serving) |
|-----|-----------|------------|-------------------|
| `hypertension` | 高血压 | 高 | 100 |
| `diabetes` | 糖尿病 | 中 | 120 |
| `gout` | 痛风 | 高 | 80 |
| `liver_disease` | 肝病/脂肪肝 | 极高 | 0 (戒酒) |
| `gastritis` | 胃炎/胃溃疡 | 中高 | 80 |
| `heart_disease` | 心脏病/冠心病 | 中 | 100 |
| `kidney_disease` | 肾病 | 中高 | 80 |
| `pregnancy` | 孕期/哺乳期 | 极高 | 0 (戒酒) |
| `medication` | 服用药物期间 | 极高 | 0 (戒酒) |
| `obesity` | 肥胖/减重 | 低 | 100 |

### ABV by Wine Type

| Type | Approximate ABV |
|------|----------------|
| Red | 13.5% |
| White | 12.0% |
| Sparkling | 12.0% |
| Rosé | 12.5% |
| Dessert | 10.0% |
| Fortified | 19.5% |

### Standard Drink Calculation

- 1 standard drink = 10g pure alcohol
- For wine: `grams_alcohol = ml × (ABV/100) × 0.789`
- Example: 150ml of 13.5% red wine = 150 × 0.135 × 0.789 = 15.98g ≈ 1.6 standard drinks

### Usage in Code

```python
# General advice for all age groups
format_health_advice(wine_type='red')

# Advice for specific age
format_health_advice(wine_type='red', user_age=40)

# Advice with health conditions
format_health_advice(wine_type='white', user_age=55, conditions=['hypertension', 'diabetes'])
```

## 7. Food Pairing Module

The script provides curated food pairing recommendations for 6 wine types, each with staple foods, main dishes, and pairing principles.

### Wine Type Pairing Summary

| Type | Staple Examples | Main Dish Examples | Principle |
|------|----------------|-------------------|-----------|
| Red | 牛排/烤肉, 意大利面 | 红烧牛肋排, 烤羊排, 蘑菇烩牛小排, 陈年奶酪 | Tannin + red meat protein; avoid fish/spicy |
| White | 米饭/白粥, 海鲜饭 | 清蒸鲈鱼, 白灼虾, 凯撒沙拉, 蒜香扇贝 | Acidity cuts fat + enhances seafood; avoid heavy red meat |
| Sparkling | 吐司/可颂, 寿司 | 生鱼片/寿司, 炸鱼薯条, 水果塔, 生蚝 | Bubbles cleanse palate; most versatile |
| Rosé | 法棍面包, 地中海沙拉 | 地中海沙拉, 烤大虾, 柠檬烤鸡, 塔帕斯 | Balanced red+white qualities; ideal for light meals |
| Dessert | 饼干/司康, 蛋糕 | 提拉米苏, 蓝莓奶酪蛋糕, 蓝纹奶酪, 苹果派 | Sweetness must match or exceed dessert |
| Fortified | 坚果拼盘, 巧克力 | 黑巧克力, 蓝纹奶酪, 烤坚果, 圣诞布丁 | High ABV + rich flavors; sip slowly |

### Usage in Code

```python
# Pairing with Vivino API food data
format_food_pairing(wine_type='red', vivino_food=[{'name': 'Beef'}, {'name': 'Lamb'}])

# Pairing without Vivino data (uses curated suggestions only)
format_food_pairing(wine_type='sparkling')
```
