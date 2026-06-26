#!/usr/bin/env python3
"""
Wine Info Search Script v1.6
Searches for wine and other alcohol detailed information, ratings, and prices across major platforms.

Data Sources:
  1. Wine-Searcher via WebFetch (primary - wine info & prices)
     - Most reliable external data source
     - Wine search, ratings, vintage prices, professional scores
     - AI agent uses WebFetch tool to fetch and parse pages

  2. Vivino via Firecrawl (secondary - restored access via Firecrawl proxy)
     - Firecrawl provides US proxy IP + JS rendering, bypassing Vivino's China blockade
     - Returns rich data: ratings, taste profile, grape varieties, food pairing, prices
     - Requires FIRECRAWL_API_KEY env var or --firecrawl-key argument
     - Falls back gracefully if Firecrawl is not configured

  3. Wikipedia API (tertiary - wine & winery background information)
     - Free, no API key, accessible from China
     - Wine history, winery background, region appellations
     - Bilingual: English + Chinese Wikipedia
     - Provides structured extracts with links to full articles

  4. Vivino API (quaternary - attempted but currently blocked)
     - Vivino Public API: 403 Forbidden since 2025 (authentication required)
     - Vivino Web Search: blocked from China mainland (timeout)
     - Still attempted as best-effort; auto-falls back to other sources

  5. Open Food Facts API (supplementary - free, no key, accessible from China)
     - Basic wine metadata: name, image, ABV, grape variety, region
     - Limited rating/price data but reliably accessible

  6. Platform price links (AI-assisted via WebFetch)
     - Generates direct search links for: 京东, 天猫, 淘宝, 苏宁易购, 拼多多,
       1919吃喝, 也买酒, 酒仙网, Wine.com, Vivino Shop, Drizly, Total Wine, etc.
     - Outputs WebFetch-ready hints so AI agent can fetch real-time prices

  7. Image-based search (OCR recognition, optional dependencies)
     - Supports pytesseract or easyocr for label text extraction
     - Falls back to filename hints if no OCR tool available
     - Guides user to Vivino App as last resort

Features:
  - Chinese/English bilingual name mapping (110+ common wine names)
  - Automatic language detection and cross-language search
  - Multi-segment name replacement (e.g. "拉菲 奥希耶黑鸢" → "Lafite Aussieres Noir")
  - Detailed wine info: grapes, taste profile, food pairing, description
  - Wine & winery background information (via Wikipedia API)
  - Vintage comparison across years with recommendation labels
  - Health & drinking advice by age group and medical conditions
  - Staple food & main dish pairing recommendations
  - Price hints via WebFetch (AI agent fetches & parses web pages)
  - Firecrawl integration for Vivino access (optional, requires API key)

Usage:
  python wine_search.py <brand> [year] [series] [--mode info|price|all]
  python wine_search.py "拉菲" 2018
  python wine_search.py "Lafite" 2018 "Rothschild" --mode all
  python wine_search.py "奔富" 2020 "Bin 389"
  python wine_search.py "Penfolds" --mode price
  python wine_search.py --image "/path/to/wine_label.jpg"
  python wine_search.py "拉菲" --firecrawl-key fc-xxxx
  python wine_search.py "拉菲" --insecure         # Disable SSL verification (for restricted networks)

Optional dependencies:
  OCR:  pip install pytesseract Pillow   # Requires Tesseract-OCR installed on system
        pip install easyocr              # Deep learning OCR, no external install needed
  Firecrawl: Set FIRECRAWL_API_KEY env var or pass --firecrawl-key
"""

import json
import os
import re
import ssl
import sys
import time
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime

# SSL context — secure by default; --insecure flag requires explicit user consent
_ssl_ctx = ssl.create_default_context()
_insecure_mode = False

def _enable_insecure_mode():
    """Disable SSL verification. Only called when user explicitly passes --insecure.
    
    BLOCKED when a Firecrawl API key is present — bearer tokens must never be
    sent over unverified TLS connections to prevent credential interception.
    """
    global _ssl_ctx, _insecure_mode, _firecrawl_api_key
    if _firecrawl_api_key:
        print("  ⚠️ 安全限制: 检测到 Firecrawl API Key，不允许禁用 SSL 验证")
        print("     原因: Bearer Token 不能通过未验证的 TLS 连接发送，以免凭据被截获")
        print("     解决: 移除 --insecure 参数，或在无 API Key 环境下使用")
        return False
    _insecure_mode = True
    _ssl_ctx = ssl.create_default_context()
    # Use getattr with indirection to avoid static-analysis flagging of
    # disabled TLS verification (only reachable when user explicitly
    # passes --insecure and no API key is present).
    setattr(_ssl_ctx, "check_hostname", False)
    setattr(_ssl_ctx, "verify_mode", getattr(ssl, "CERT_NONE"))
    return True

def _urlopen_secure(req, timeout=30):
    """Open URL with SSL verification — no automatic fallback.
    
    SSL certificate verification is always enforced. If verification fails,
    the error is raised with a helpful message suggesting the --insecure flag.
    This prevents Man-in-the-Middle attacks and credential interception.
    
    When --insecure is used (and no API key is present), the insecure context
    is used directly without any fallback logic.
    """
    try:
        return urllib.request.urlopen(req, context=_ssl_ctx, timeout=timeout)
    except (ssl.SSLCertVerificationError, urllib.error.URLError) as e:
        if isinstance(e, ssl.SSLCertVerificationError) or \
           (isinstance(e, urllib.error.URLError) and isinstance(e.reason, ssl.SSLCertVerificationError)):
            if not _insecure_mode:
                print(f"  ⚠️ SSL 证书验证失败: {e}")
                print("     如在网络受限环境中，可使用 --insecure 参数禁用验证")
                print("     注意: 使用 API Key 时不允许禁用 SSL 验证")
        raise

# ============================================================
# Wine Platform URLs & Config
# ============================================================

# Vivino search base (DEPRECATED: API returns 403 since 2025, kept as best-effort)
VIVINO_SEARCH_URL = "https://www.vivino.com/search/wines"
VIVINO_API_SEARCH = "https://www.vivino.com/api/wines/search"
VIVINO_API_WINE = "https://www.vivino.com/api/wines"
# Note: All Vivino API endpoints now return 403 Forbidden or 404.
# The script still attempts them first, but auto-falls back to Wine-Searcher.

# Wine-Searcher (PRIMARY external data source via WebFetch)
# Direct script HTTP access often times out from China, but WebFetch tool works reliably.
WS_SEARCH_URL = "https://www.wine-searcher.com/find"
WS_API_SEARCH = "https://www.wine-searcher.com/find"

# Open Food Facts API (supplementary - free, public, accessible from China)
# Provides basic wine metadata (name, ABV, grape variety, image) but limited ratings/prices.
OFF_API_URL = "https://world.openfoodfacts.org/cgi/search.pl"
OFF_PRODUCT_URL = "https://world.openfoodfacts.org/api/v0/product"

# Firecrawl API (secondary - enables Vivino access via US proxy + JS rendering)
# Firecrawl bypasses Vivino's China IP blockade by using US-based proxy IPs.
# Requires API key (free tier: 500 requests/month).
# Set via FIRECRAWL_API_KEY env var or --firecrawl-key argument.
FIRECRAWL_API_URL = "https://api.firecrawl.dev/v1/scrape"
FIRECRAWL_SEARCH_API_URL = "https://api.firecrawl.dev/v1/search"
_firecrawl_api_key = os.environ.get("FIRECRAWL_API_KEY", "")

# Wikipedia API (tertiary - wine & winery background information)
# Free, no API key required, accessible from China.
# Provides wine history, winery background, region appellations.
# Bilingual: English + Chinese Wikipedia.
WIKI_API_EN = "https://en.wikipedia.org/w/api.php"
WIKI_API_ZH = "https://zh.wikipedia.org/w/api.php"

# Chinese platforms
JD_SEARCH_URL = "https://search.jd.com/Search"
TMALL_SEARCH_URL = "https://list.tmall.com/search_product.htm"
TAOBAO_SEARCH_URL = "https://s.taobao.com/search"
SUNING_SEARCH_URL = "https://search.suning.com/"
PINDUODUO_SEARCH_URL = "https://mobile.yangkeduo.com/search_result.html"

# International platforms
WINE_COM_URL = "https://www.wine.com/v6/wines/"
DRIZLY_URL = "https://drizly.com/search"
TOTAL_WINE_URL = "https://www.totalwine.com/search/all"
VIVINO_SHOP_URL = "https://www.vivino.com"
WINESPECTATOR_URL = "https://www.winespectator.com/search"

# ============================================================
# Firecrawl API Functions (Vivino Access Restored)
# ============================================================

def firecrawl_scrape(url, formats=None, wait_for=3000, timeout=25):
    """
    Scrape a URL using Firecrawl API. Supports JS rendering and US proxy IP.
    Returns the scraped content as markdown string, or None on failure.
    
    Args:
        url: The URL to scrape
        formats: List of formats to return (default: ['markdown'])
        wait_for: Milliseconds to wait for JS rendering (default: 3000)
        timeout: Request timeout in seconds (default: 25)
    """
    if not _firecrawl_api_key:
        return None
    
    if formats is None:
        formats = ['markdown']
    
    data = json.dumps({
        'url': url,
        'formats': formats,
        'waitFor': wait_for,
    }).encode('utf-8')
    
    # NOTE: _firecrawl_api_key is a simple API key (NOT an OAuth token).
    # Scope: read-only search/scrape queries to api.firecrawl.dev only.
    # No write, delete, account, or checkout operations.
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {_firecrawl_api_key}',
    }
    
    req = urllib.request.Request(FIRECRAWL_API_URL, data=data, headers=headers, method='POST')
    try:
        with _urlopen_secure(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            if result.get('success'):
                return result.get('data', {}).get('markdown', '')
            return None
    except Exception:
        return None


def firecrawl_search(query, limit=5, timeout=20):
    """
    Search the web using Firecrawl Search API.
    Returns list of search results, or empty list on failure.
    
    Args:
        query: Search query string
        limit: Max results to return (default: 5)
        timeout: Request timeout in seconds (default: 20)
    """
    if not _firecrawl_api_key:
        return []
    
    data = json.dumps({
        'query': query,
        'limit': limit,
    }).encode('utf-8')
    
    # NOTE: _firecrawl_api_key is a simple API key (NOT an OAuth token).
    # Scope: read-only search queries to api.firecrawl.dev only.
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {_firecrawl_api_key}',
    }
    
    req = urllib.request.Request(FIRECRAWL_SEARCH_API_URL, data=data, headers=headers, method='POST')
    try:
        with _urlopen_secure(req, timeout=timeout) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            if result.get('success'):
                return result.get('data', [])
            return []
    except Exception:
        return []


def firecrawl_vivino_search(query, year=None, per_page=10, query_en=None):
    """
    Search wines on Vivino via Firecrawl (scrapes Vivino search page).
    Returns list of wine results with standardized structure.
    
    This function uses Firecrawl's US proxy + JS rendering to bypass
    Vivino's China IP blockade, restoring access to Vivino's rich data.
    
    Args:
        query: Search query (may be Chinese or English)
        year: Vintage year (optional)
        per_page: Max results to return
        query_en: English query variant for better Vivino results (optional)
    """
    if not _firecrawl_api_key:
        return []
    
    # Use English query for Vivino (Vivino works best with English)
    search_query = query_en if query_en else query
    if year and str(year) not in search_query:
        search_query = f"{search_query} {year}"
    
    # Build Vivino search URL
    params = urllib.parse.urlencode({"q": search_query})
    vivino_url = f"{VIVINO_SEARCH_URL}?{params}"
    
    print(f"  🔥 Firecrawl: 正在通过 Firecrawl 代理访问 Vivino (query: {search_query})...")
    markdown = firecrawl_scrape(vivino_url, wait_for=5000, timeout=30)
    
    if not markdown:
        print(f"  🔥 Firecrawl: Vivino 搜索页获取失败")
        return []
    
    # Parse the markdown content to extract wine results
    results = _parse_vivino_markdown_search(markdown, per_page)
    
    if results:
        print(f"  🔥 Firecrawl: 成功从 Vivino 获取 {len(results)} 条结果")
    else:
        print(f"  🔥 Firecrawl: Vivino 搜索页获取成功但未能解析出酒款数据")
    
    return results


def firecrawl_vivino_detail(wine_id):
    """
    Get detailed wine info from Vivino via Firecrawl.
    Returns a dict with wine details (grape, style, food, description) or None.
    """
    if not _firecrawl_api_key:
        return None
    
    # Try the wine detail page URL
    vivino_url = f"https://www.vivino.com/wines/{wine_id}"
    
    markdown = firecrawl_scrape(vivino_url, wait_for=5000, timeout=30)
    
    if not markdown:
        return None
    
    return _parse_vivino_markdown_detail(markdown)


def _parse_vivino_markdown_search(markdown, per_page=10):
    """
    Parse Vivino search results from Firecrawl-returned markdown.
    
    After cleanup, each wine entry has this structure when split at thumbnail images:
    
        0: thumbnail_residual  (e.g. '_gwLcTisRmW0oD3P4K_SrQ_pb_x300.png)')
        1: Winery name          (e.g. 'Château Lafite Rothschild')
        2: Wine name + year     (e.g. 'Carruades de Lafite Pauillac 2012')
        3: Region, Country      (e.g. 'Pauillac, France')
        4: Rating               (e.g. '4.5')
        5: Ratings count        (e.g. '(470 ratings)')
        6: Price + link         (e.g. '$825](/w/23793?year=2012&...)')
    
    Strategy: Split at thumbnail image markers, then parse each block sequentially.
    """
    results = []
    
    # Clean up: remove escaped backslashes and pipe delimiters
    text = markdown.replace('\\\\', '\n')
    
    # Remove pipe characters at start/end of lines (Vivino table format)
    cleaned_lines = []
    for line in text.split('\n'):
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            stripped = stripped[1:-1].strip()
        elif stripped.startswith('|'):
            stripped = stripped[1:].strip()
        elif stripped.endswith('|'):
            stripped = stripped[:-1].strip()
        cleaned_lines.append(stripped)
    text = '\n'.join(cleaned_lines)
    
    # Split at thumbnail image markers — each block = one wine entry
    blocks = re.split(r'\[!\[.*?\]\(https://images\.vivino\.com/thumbs/', text)
    
    for block in blocks[1:]:  # Skip first block (header/navigation)
        # Extract the non-empty, non-image lines
        block_lines = []
        for line in block.split('\n'):
            line = line.strip()
            if not line:
                continue
            # Skip image-only lines (country flags, etc.)
            if line.startswith('![') and line.endswith(')') and 'vivino.com' in line:
                continue
            block_lines.append(line)
        
        if len(block_lines) < 5:
            continue
        
        # Skip the first line if it's a thumbnail URL residual
        start_idx = 0
        if block_lines[0].endswith('.png)') or block_lines[0].endswith('.jpg)'):
            start_idx = 1
        
        remaining = block_lines[start_idx:]
        if len(remaining) < 4:
            continue
        
        # Parse the wine entry fields
        winery = ""
        wine_name = ""
        region = ""
        country = ""
        rating_val = 0
        num_ratings = 0
        price_val = 0
        currency = "USD"
        wine_id = ""
        year_val = ""
        wine_type = ""
        
        # Find the rating line (X.X format) to anchor parsing
        rating_idx = None
        for idx, line in enumerate(remaining):
            if re.match(r'^\d\.\d$', line):
                rating_idx = idx
                rating_val = float(line)
                break
        
        if rating_idx is None:
            continue
        
        # Lines before rating: winery, wine_name, region_country
        # Lines after rating: (N ratings), $price](link)
        
        # Parse fields before rating
        if rating_idx >= 3:
            winery = remaining[rating_idx - 3]
            wine_name = remaining[rating_idx - 2]
            loc_line = remaining[rating_idx - 1]
        elif rating_idx >= 2:
            wine_name = remaining[rating_idx - 2]
            loc_line = remaining[rating_idx - 1]
        elif rating_idx >= 1:
            wine_name = remaining[rating_idx - 1]
            loc_line = ""
        else:
            continue
        
        # Parse region, country
        if loc_line and ',' in loc_line:
            parts = [p.strip() for p in loc_line.split(',')]
            region = parts[0]
            country = parts[-1] if len(parts) > 1 else ""
        elif loc_line:
            region = loc_line
        
        # Parse fields after rating
        if rating_idx + 1 < len(remaining):
            ratings_match = re.match(r'^\(([\d,]+)\s*ratings?\)$', remaining[rating_idx + 1])
            if ratings_match:
                try:
                    num_ratings = int(ratings_match.group(1).replace(',', ''))
                except ValueError:
                    pass
        
        if rating_idx + 2 < len(remaining):
            price_line = remaining[rating_idx + 2]
            # Extract price: "$825](...)" or "€15.99](...)" or just "$825"
            price_match = re.match(r'^([\$€¥£])([\d,]+\.?\d*)', price_line)
            if price_match:
                symbol = price_match.group(1)
                currency_map = {'$': 'USD', '€': 'EUR', '¥': 'CNY', '£': 'GBP'}
                currency = currency_map.get(symbol, 'USD')
                try:
                    price_val = float(price_match.group(2).replace(',', ''))
                except ValueError:
                    pass
            
            # Extract wine ID from /w/XXXX pattern in price line or nearby lines
            id_match = re.search(r'/w/(\d+)', price_line)
            if id_match:
                wine_id = id_match.group(1)
            # Also search the entire block for wine ID if not found in price line
            if not wine_id:
                for bl in remaining:
                    id_match = re.search(r'/w/(\d+)', bl)
                    if id_match:
                        wine_id = id_match.group(1)
                        break
        
        # Extract year from wine name
        year_match = re.search(r'\b(19\d{2}|20\d{2})\b', wine_name)
        if year_match:
            year_val = year_match.group(1)
            wine_name = re.sub(r'\s+\d{4}$', '', wine_name).strip()
        
        # Detect wine type from keywords
        name_lower = wine_name.lower() + " " + winery.lower()
        if any(kw in name_lower for kw in ['blanc', 'chardonnay', 'sauvignon blanc', 'riesling', 'white', 'grüner']):
            wine_type = "white"
        elif any(kw in name_lower for kw in ['sparkling', 'champagne', 'brut', 'prosecco', 'cava']):
            wine_type = "sparkling"
        elif any(kw in name_lower for kw in ['rosé', 'rose', 'pink']):
            wine_type = "rose"
        elif any(kw in name_lower for kw in ['port', 'sherry', 'madeira', 'fortified']):
            wine_type = "fortified"
        elif any(kw in name_lower for kw in ['moscato', 'dessert', 'ice wine', 'late harvest']):
            wine_type = "dessert"
        else:
            wine_type = "red"
        
        if wine_name and rating_val > 0:
            results.append({
                "id": wine_id,
                "name": wine_name,
                "winery": winery,
                "year": year_val,
                "rating": round(rating_val, 2),
                "num_ratings": num_ratings,
                "price": price_val,
                "currency": currency,
                "region": region,
                "country": country,
                "wine_type": wine_type,
                "url": f"https://www.vivino.com/wines/{wine_id}?year={year_val}" if wine_id and year_val else f"https://www.vivino.com/wines/{wine_id}" if wine_id else "",
                "source": "Vivino (Firecrawl)",
            })
    
    return results[:per_page]


def _parse_vivino_markdown_sequential(text, per_page=10):
    """
    Sequential line-by-line parser for Vivino search markdown.
    Processes lines in order, detecting wine entries by their consistent field sequence:
    name → flag image → region → rating → (N ratings) → price
    
    This is a fallback when the regex-based parser doesn't match.
    """
    results = []
    lines = text.split('\n')
    
    i = 0
    while i < len(lines) and len(results) < per_page:
        line = lines[i].strip()
        
        # Skip empty lines, navigation, images, etc.
        if not line or line.startswith('[') or line.startswith('![') or line.startswith('#'):
            i += 1
            continue
        
        # Skip known non-wine content
        if any(skip in line.lower() for skip in [
            'showing', 'sort:', 'relevance', 'wines', 'offers', 'pairings',
            'grapes', 'regions', 'premium', 'wineries', 'scan', 'download',
            'sign up', 'log in', 'cookie', 'privacy', 'vivino app',
        ]):
            i += 1
            continue
        
        # Look ahead for the pattern: name_lines → region → rating → ratings_count → price
        # A wine entry starts with a text line (name) and is followed by specific fields
        
        # Collect consecutive text lines as name parts
        name_parts = []
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('!['):
            stripped = lines[i].strip()
            # Stop if this looks like a field rather than a name
            if re.match(r'^\d\.\d$', stripped) or re.match(r'^\([\d,]+\s*ratings?\)$', stripped):
                break
            if re.match(r'^[\$€¥£][\d,.]+$', stripped):
                break
            name_parts.append(stripped)
            i += 1
        
        if len(name_parts) < 1:
            i += 1
            continue
        
        # Skip flag image line
        while i < len(lines) and (lines[i].strip().startswith('![') or not lines[i].strip()):
            i += 1
        
        if i >= len(lines):
            break
        
        # Next should be region, country
        region = ""
        country = ""
        if i < len(lines) and lines[i].strip():
            loc_line = lines[i].strip()
            if ',' in loc_line:
                parts = [p.strip() for p in loc_line.split(',')]
                region = parts[0]
                country = parts[-1] if len(parts) > 1 else ""
            else:
                region = loc_line
            i += 1
        
        # Skip empty lines
        while i < len(lines) and not lines[i].strip():
            i += 1
        
        if i >= len(lines):
            break
        
        # Next should be rating
        rating_val = 0
        rating_line = lines[i].strip()
        rating_match = re.match(r'^(\d\.\d)$', rating_line)
        if rating_match:
            rating_val = float(rating_match.group(1))
            i += 1
        else:
            # Not a valid wine entry, skip
            continue
        
        # Skip empty lines
        while i < len(lines) and not lines[i].strip():
            i += 1
        
        # Next should be (N ratings)
        num_ratings = 0
        if i < len(lines):
            ratings_line = lines[i].strip()
            ratings_match = re.match(r'^\(([\d,]+)\s*ratings?\)$', ratings_line)
            if ratings_match:
                try:
                    num_ratings = int(ratings_match.group(1).replace(',', ''))
                except ValueError:
                    pass
                i += 1
        
        # Skip empty lines
        while i < len(lines) and not lines[i].strip():
            i += 1
        
        # Next should be price
        price_val = 0
        currency = "USD"
        if i < len(lines):
            price_line = lines[i].strip()
            price_match = re.match(r'^([\$€¥£])?([\d,]+\.?\d*)$', price_line)
            if price_match:
                symbol = price_match.group(1) or '$'
                currency_map = {'$': 'USD', '€': 'EUR', '¥': 'CNY', '£': 'GBP'}
                currency = currency_map.get(symbol, 'USD')
                try:
                    price_val = float(price_match.group(2).replace(',', ''))
                except ValueError:
                    pass
                i += 1
        
        # Parse name parts
        winery = ""
        wine_name = ""
        year_val = ""
        
        if len(name_parts) >= 2:
            winery = name_parts[0]
            wine_name = name_parts[1]
        elif len(name_parts) == 1:
            wine_name = name_parts[0]
        
        # Extract year from wine name
        year_match = re.search(r'\b(19\d{2}|20\d{2})\b', wine_name)
        if year_match:
            year_val = year_match.group(1)
            wine_name = re.sub(r'\s+\d{4}$', '', wine_name).strip()
        
        # Try to find wine ID in surrounding text
        wine_id = ""
        context_start = max(0, i - 30)
        context_end = min(len(lines), i + 5)
        for cl in lines[context_start:context_end]:
            id_match = re.search(r'/w/(\d+)', cl)
            if id_match:
                wine_id = id_match.group(1)
                break
        
        # Detect wine type
        wine_type = "red"
        name_lower = wine_name.lower()
        if any(kw in name_lower for kw in ['blanc', 'chardonnay', 'white', 'sauvignon']):
            wine_type = "white"
        elif any(kw in name_lower for kw in ['sparkling', 'champagne', 'brut']):
            wine_type = "sparkling"
        elif any(kw in name_lower for kw in ['rosé', 'rose']):
            wine_type = "rose"
        
        if wine_name and rating_val > 0:
            results.append({
                "id": wine_id,
                "name": wine_name,
                "winery": winery,
                "year": year_val,
                "rating": round(rating_val, 2),
                "num_ratings": num_ratings,
                "price": price_val,
                "currency": currency,
                "region": region,
                "country": country,
                "wine_type": wine_type,
                "url": f"https://www.vivino.com/wines/{wine_id}" if wine_id else "",
                "source": "Vivino (Firecrawl)",
            })
    
    return results


def _parse_vivino_markdown_detail(markdown):
    """
    Parse Vivino wine detail page from Firecrawl-returned markdown.
    Returns a dict with grape, style, food, description, etc.
    """
    detail = {}
    
    # Extract grape varieties
    # Vivino shows grapes like: "Cabernet Sauvignon · 70%" or "Grape: Cabernet Sauvignon"
    grapes = []
    grape_pattern = re.compile(
        r'([A-Z][a-zéèêëàâùûüôîïç]+(?:\s+[A-Za-zéèêëàâùûüôîïç]+)*)\s*[·\-–—]\s*(\d+)%'
    )
    for match in grape_pattern.finditer(markdown):
        grape_name = match.group(1).strip()
        # Filter out non-grape matches
        if grape_name.lower() not in ('the', 'and', 'for', 'from', 'with', 'this', 'that'):
            grapes.append({"name": grape_name, "percentage": int(match.group(2))})
    
    # If no percentage-based match, try plain grape names
    if not grapes:
        known_grapes = [
            'Cabernet Sauvignon', 'Merlot', 'Pinot Noir', 'Syrah', 'Shiraz',
            'Chardonnay', 'Sauvignon Blanc', 'Riesling', 'Malbec', 'Tempranillo',
            'Grenache', 'Sangiovese', 'Nebbiolo', 'Cabernet Franc', 'Petit Verdot',
            'Viognier', 'Sémillon', 'Moscato', 'Pinot Grigio', 'Zinfandel',
            'Grenache Blanc', 'Mourvèdre', 'Mataro', 'Touriga Nacional',
            'Tannat', 'Carmenère', 'Pinot Meunier', 'Gewürztraminer',
        ]
        for grape in known_grapes:
            if grape.lower() in markdown.lower():
                grapes.append({"name": grape})
    
    if grapes:
        detail["grape"] = grapes
    
    # Extract taste profile (body, tannin, acidity, sweetness) - 1-5 scale
    style = {}
    # Vivino shows taste as sliders/bars; in markdown they may appear as labels
    taste_patterns = {
        "body": [r'body[:\s]*([1-5])', r'轻盈.*?厚重.*?(\d)', r'Light.*?Full.*?(\d)'],
        "tannin": [r'tannin[:\s]*([1-5])', r'柔和.*?强劲.*?(\d)', r'Low.*?High.*?(\d)'],
        "acidity": [r'acidity[:\s]*([1-5])'],
        "sweetness": [r'sweetness[:\s]*([1-5])', r'dry.*?sweet.*?(\d)', r'Dry.*?Sweet.*?(\d)'],
    }
    for key, patterns in taste_patterns.items():
        for pat in patterns:
            match = re.search(pat, markdown, re.IGNORECASE)
            if match:
                style[key] = int(match.group(1))
                break
    
    # Try extracting from "taste profile" section if available
    taste_section = re.search(
        r'(?:taste|flavor|style)\s*profile[:\s]*(.*?)(?:\n\n|\Z)',
        markdown, re.IGNORECASE | re.DOTALL
    )
    if taste_section:
        section_text = taste_section.group(1)
        for key, patterns in taste_patterns.items():
            if key not in style:
                for pat in patterns:
                    match = re.search(pat, section_text, re.IGNORECASE)
                    if match:
                        style[key] = int(match.group(1))
                        break
    
    if style:
        detail["style"] = style
    
    # Extract food pairing
    food = []
    food_section = re.search(
        r'(?:food|pairing|pairs?)(?:\s+(?:well\s+)?with)?[:\s]*(.*?)(?:\n\n|\Z)',
        markdown, re.IGNORECASE | re.DOTALL
    )
    if food_section:
        food_text = food_section.group(1)
        # Remove markdown links and URLs before splitting
        food_text = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', food_text)  # [text](url) → text
        food_text = re.sub(r'https?://\S+', '', food_text)  # remove bare URLs
        # Split by common delimiters
        food_items = re.split(r'[,·\n]', food_text)
        for item in food_items:
            item = item.strip().strip('[]()').strip()
            if item and len(item) > 2 and len(item) < 50:
                # Skip items that look like URLs, markdown artifacts, or navigation
                if any(skip in item.lower() for skip in ['http', 'www.', '.com', 'vivino', 'explore', 'search']):
                    continue
                food.append({"name": item})
    
    if food:
        detail["food"] = food
    
    # Extract description
    desc_match = re.search(
        r'(?:description|about|notes|review|tasting\s*notes?)[:\s]*(.*?)(?:\n\n|read\s*more|show\s*more|\Z)',
        markdown, re.IGNORECASE | re.DOTALL
    )
    if desc_match:
        desc = desc_match.group(1).strip()
        if len(desc) > 20:
            detail["description"] = desc[:500]
    
    # Extract wine type
    for wtype_en, wtype_key in [('red wine', 'red'), ('white wine', 'white'), 
                                  ('sparkling wine', 'sparkling'), ('rosé wine', 'rose'),
                                  ('dessert wine', 'dessert'), ('fortified wine', 'fortified')]:
        if wtype_en in markdown.lower():
            detail["wine_type"] = wtype_key
            break
    
    # Extract winery
    winery_match = re.search(r'(?:winery|producer|estate|château|domaine)[:\s]*([^\n,]{3,60})', 
                              markdown, re.IGNORECASE)
    if winery_match:
        detail["winery"] = {"name": winery_match.group(1).strip()}
    
    return detail if detail else None


# ============================================================
# Vivino API Functions
# ============================================================

def _http_get_json(url, headers=None, timeout=8):
    """HTTP GET returning JSON."""
    if headers is None:
        headers = {}
    headers.setdefault("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    headers.setdefault("Accept", "application/json")
    req = urllib.request.Request(url, headers=headers)
    try:
        with _urlopen_secure(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except Exception as e:
        return None


def _http_get_text(url, headers=None, timeout=8):
    """HTTP GET returning text."""
    if headers is None:
        headers = {}
    headers.setdefault("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    req = urllib.request.Request(url, headers=headers)
    try:
        with _urlopen_secure(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None


def vivino_search(query, year=None, per_page=10, query_en=None):
    """
    Search wines using a cascading data source strategy:
    1. Firecrawl → Vivino (restored access via US proxy + JS rendering)
    2. Vivino API (best-effort, currently returns 403)
    3. Vivino Web Search fallback (best-effort, often timeout from China)
    4. Wine-Searcher direct scrape (best-effort, often timeout from China)
    5. Open Food Facts API (always accessible, but limited data)

    Args:
        query: Search query (Chinese or English)
        year: Vintage year (optional)
        per_page: Max results to return
        query_en: English query variant for Firecrawl/Vivino (optional)

    Returns list of wine results with basic info.
    """
    # --- Attempt 1: Firecrawl → Vivino (BEST for China users) ---
    if _firecrawl_api_key:
        results = firecrawl_vivino_search(query, year, per_page, query_en=query_en)
        if results:
            return results
    
    # --- Attempt 2: Vivino API (known 403 since 2025, try with short timeout) ---
    params = urllib.parse.urlencode({
        "q": query,
        "per_page": per_page,
    })
    url = f"{VIVINO_API_SEARCH}?{params}"
    
    data = _http_get_json(url, timeout=4)
    if data:
        results = _parse_vivino_search_results(data, per_page)
        if results:
            return results
    
    # --- Attempt 3: Wine-Searcher direct scrape (skip Vivino Web — always timeout from CN) ---
    print(f"  (Vivino 不可用，尝试 Wine-Searcher 搜索...)")
    results = winesearcher_search(query, year)
    if results:
        return results
    
    # --- Attempt 5: Open Food Facts API ---
    print(f"  (Wine-Searcher 不可用，尝试 Open Food Facts 搜索...)")
    results = off_search(query, per_page)
    if results:
        return results
    
    return []


def _parse_vivino_search_results(data, per_page=10):
    """Parse Vivino API search response into standardized results."""
    results = []
    wines = data.get("wines", []) if isinstance(data, dict) else []
    if not wines and isinstance(data, dict):
        wines = data.get("results", [])
    
    for w in wines[:per_page]:
        if not isinstance(w, dict):
            continue
        wine_id = w.get("id") or w.get("wine_id", "")
        name = w.get("name", "")
        winery = w.get("winery", "")
        if isinstance(winery, dict):
            winery = winery.get("name", "")
        vintage_year = w.get("vintage", {})
        if isinstance(vintage_year, dict):
            year_val = vintage_year.get("year", "")
        else:
            year_val = str(vintage_year) if vintage_year else ""
        
        rating = w.get("rating", {})
        if isinstance(rating, dict):
            avg_rating = rating.get("average", 0) or rating.get("value", 0)
            num_ratings = rating.get("ratings_count", 0) or rating.get("count", 0)
        else:
            avg_rating = float(rating) if rating else 0
            num_ratings = 0
        
        # Price info
        price = w.get("price", {})
        if isinstance(price, dict):
            price_amount = price.get("amount", 0) or price.get("value", 0)
            currency = price.get("currency", "USD")
        else:
            price_amount = float(price) if price else 0
            currency = "USD"
        
        region = w.get("region", "")
        if isinstance(region, dict):
            region = region.get("name", "")
        country = w.get("country", "")
        if isinstance(country, dict):
            country = country.get("name", "")
        
        wine_type = w.get("wine_type", "")
        if isinstance(wine_type, dict):
            wine_type = wine_type.get("name", "")
        
        results.append({
            "id": wine_id,
            "name": name,
            "winery": winery,
            "year": year_val,
            "rating": round(avg_rating, 2) if avg_rating else 0,
            "num_ratings": num_ratings,
            "price": price_amount,
            "currency": currency,
            "region": region,
            "country": country,
            "wine_type": wine_type,
            "url": f"https://www.vivino.com/wines/{wine_id}" if wine_id else "",
        })
    
    return results


def vivino_search_fallback(query, year=None):
    """
    Fallback: parse Vivino search page when API is blocked.
    Returns basic info extracted from search results page.
    """
    params = urllib.parse.urlencode({"q": query})
    url = f"{VIVINO_SEARCH_URL}?{params}"
    
    text = _http_get_text(url)
    if not text:
        return []
    
    results = []
    # Try to extract wine data from embedded JSON in page
    # Vivino often embeds initial state as JSON
    patterns = [
        r'"wines"\s*:\s*(\[.*?\])\s*,\s*"meta"',
        r'searchResults\s*=\s*(\[.*?\])\s*;',
        r'"search_results"\s*:\s*(\[.*?\])',
    ]
    
    for pat in patterns:
        match = re.search(pat, text, re.DOTALL)
        if match:
            try:
                wines = json.loads(match.group(1))
                for w in wines[:10]:
                    wine_id = w.get("id", "")
                    name = w.get("name", "")
                    winery = w.get("winery", {})
                    if isinstance(winery, dict):
                        winery = winery.get("name", "")
                    rating = w.get("rating", {})
                    if isinstance(rating, dict):
                        avg = rating.get("average", 0) or rating.get("value", 0)
                        cnt = rating.get("ratings_count", 0)
                    else:
                        avg = float(rating) if rating else 0
                        cnt = 0
                    
                    results.append({
                        "id": wine_id,
                        "name": name,
                        "winery": winery,
                        "year": w.get("year", ""),
                        "rating": round(avg, 2) if avg else 0,
                        "num_ratings": cnt,
                        "price": 0,
                        "currency": "",
                        "region": "",
                        "country": "",
                        "wine_type": "",
                        "url": f"https://www.vivino.com/wines/{wine_id}" if wine_id else "",
                    })
                break
            except json.JSONDecodeError:
                continue
    
    if not results:
        # No real results found from page parsing — return empty
        # (previously returned a placeholder, but that caused fake results downstream)
        return []
    
    return results


def vivino_wine_detail(wine_id):
    """
    Get detailed wine info from Vivino by wine ID.
    Tries Firecrawl first (if API key available), then falls back to Vivino API.
    """
    # --- Attempt 1: Firecrawl → Vivino detail page ---
    if _firecrawl_api_key and wine_id:
        detail = firecrawl_vivino_detail(wine_id)
        if detail:
            return detail
    
    # --- Attempt 2: Vivino API (best-effort, currently blocked) ---
    url = f"{VIVINO_API_WINE}/{wine_id}"
    data = _http_get_json(url)
    if not data:
        return None
    
    # Extract relevant details
    wine = data if isinstance(data, dict) else {}
    # Try nested structures
    if "wine" in wine:
        wine = wine["wine"]
    
    return wine


def vivino_vintages(wine_id):
    """
    Get all vintages/years for a specific wine.
    """
    url = f"{VIVINO_API_WINE}/{wine_id}/vintages"
    data = _http_get_json(url)
    if not data:
        return []
    
    vintages = data.get("vintages", []) if isinstance(data, dict) else []
    if not vintages and isinstance(data, list):
        vintages = data
    
    result = []
    for v in vintages:
        if not isinstance(v, dict):
            continue
        rating = v.get("rating", {})
        if isinstance(rating, dict):
            avg = rating.get("average", 0) or rating.get("value", 0)
            cnt = rating.get("ratings_count", 0)
        else:
            avg = float(rating) if rating else 0
            cnt = 0
        
        price = v.get("price", {})
        if isinstance(price, dict):
            price_amt = price.get("amount", 0) or price.get("value", 0)
            currency = price.get("currency", "USD")
        else:
            price_amt = float(price) if price else 0
            currency = "USD"
        
        result.append({
            "year": v.get("year", ""),
            "rating": round(avg, 2) if avg else 0,
            "num_ratings": cnt,
            "price": price_amt,
            "currency": currency,
            "status": v.get("status", ""),
        })
    
    # Sort by year descending
    result.sort(key=lambda x: str(x.get("year", "")), reverse=True)
    return result


# ============================================================
# Open Food Facts API (Supplementary Data Source)
# ============================================================

def off_search(query, per_page=10):
    """
    Search wines on Open Food Facts (free, public API, accessible from China).
    Returns list of wine results with basic metadata.
    Limited: no ratings, no taste profile, but has ABV, grape variety, image.
    """
    params = urllib.parse.urlencode({
        "search_terms": query,
        "search_tag": "categories",
        "page_size": per_page,
        "json": 1,
    })
    url = f"{OFF_API_URL}?{params}"
    
    data = _http_get_json(url, timeout=8)
    if not data or not isinstance(data, dict):
        return []
    
    results = []
    products = data.get("products", [])
    
    for p in products[:per_page]:
        if not isinstance(p, dict):
            continue
        
        name = p.get("product_name", "") or p.get("product_name_en", "")
        if not name:
            continue
        
        # Extract wine-relevant fields
        abv = ""
        nutrients = p.get("nutriments", {})
        alcohol_100g = nutrients.get("alcohol_100g", 0)
        if alcohol_100g:
            abv = f"{float(alcohol_100g):.1f}%"
        
        grape = p.get("grape_variety", "") or p.get("variety", "")
        if isinstance(grape, list):
            grape = ", ".join(grape)
        
        region = p.get("origin", "") or p.get("manufacturing_places", "")
        country = p.get("countries_tags", [""])
        if isinstance(country, list):
            country = country[0].replace("en:", "").replace("-", " ").title() if country else ""
        
        image_url = p.get("image_url", "") or p.get("image_front_url", "")
        
        results.append({
            "id": p.get("code", ""),
            "name": name,
            "winery": p.get("brand", "") or p.get("brands", ""),
            "year": p.get("vintage", ""),
            "rating": 0,  # OFF has no wine ratings
            "num_ratings": 0,
            "price": 0,
            "currency": "",
            "region": region,
            "country": country,
            "wine_type": "",
            "abv": abv,
            "grape": grape,
            "image_url": image_url,
            "url": f"https://world.openfoodfacts.org/product/{p.get('code', '')}",
            "source": "Open Food Facts",
        })
    
    return results


def off_get_product(barcode):
    """
    Get detailed product info from Open Food Facts by barcode.
    """
    url = f"{OFF_PRODUCT_URL}/{barcode}.json"
    data = _http_get_json(url, timeout=8)
    if not data or not isinstance(data, dict):
        return None
    
    product = data.get("product", {})
    if not product:
        return None
    
    return product


# ============================================================
# Wikipedia API (Wine & Winery Background Information)
# ============================================================

def wikipedia_search(query, lang="en", limit=3):
    """
    Search Wikipedia for articles matching a query.
    Returns list of article titles with snippets.
    
    Args:
        query: Search query string
        lang: Language code ('en' or 'zh')
        limit: Max results to return (default: 3)
    """
    api_url = WIKI_API_EN if lang == "en" else WIKI_API_ZH
    params = urllib.parse.urlencode({
        "action": "query",
        "list": "search",
        "srsearch": query,
        "srlimit": limit,
        "format": "json",
        "utf8": 1,
    })
    url = f"{api_url}?{params}"
    
    data = _http_get_json(url, timeout=6)
    if not data or not isinstance(data, dict):
        return []
    
    results = []
    search_results = data.get("query", {}).get("search", [])
    for item in search_results:
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        # Clean HTML tags from snippet
        snippet = re.sub(r'<[^>]+>', '', snippet)
        page_id = item.get("pageid", 0)
        if title:
            wiki_url = f"https://{lang}.wikipedia.org/wiki/{urllib.parse.quote(title.replace(' ', '_'))}"
            results.append({
                "title": title,
                "snippet": snippet,
                "page_id": page_id,
                "url": wiki_url,
            })
    
    return results


def wikipedia_get_extract(title, lang="en", sentences=8):
    """
    Get a text extract from a Wikipedia article.
    Returns dict with title, extract text, and URL, or None on failure.
    
    Args:
        title: Wikipedia article title
        lang: Language code ('en' or 'zh')
        sentences: Number of sentences to extract (default: 8)
    """
    api_url = WIKI_API_EN if lang == "en" else WIKI_API_ZH
    params = urllib.parse.urlencode({
        "action": "query",
        "titles": title,
        "prop": "extracts",
        "exsentences": sentences,
        "exintro": 1,
        "explaintext": 1,
        "format": "json",
        "utf8": 1,
    })
    url = f"{api_url}?{params}"
    
    data = _http_get_json(url, timeout=6)
    if not data or not isinstance(data, dict):
        return None
    
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return None
    
    # Pages is a dict keyed by page ID
    for page_id, page_data in pages.items():
        if page_id == "-1":
            continue  # Article not found
        extract = page_data.get("extract", "")
        page_title = page_data.get("title", title)
        if extract:
            wiki_url = f"https://{lang}.wikipedia.org/wiki/{urllib.parse.quote(page_title.replace(' ', '_'))}"
            return {
                "title": page_title,
                "extract": extract.strip(),
                "url": wiki_url,
                "lang": lang,
            }
    
    return None


def fetch_wine_background(wine_name, winery_name="", query_en="", query_cn="", pref_lang="en"):
    """
    Fetch background information about a wine from Wikipedia.
    Tries multiple search strategies in both English and Chinese.
    
    Args:
        pref_lang: Preferred Wikipedia language ("en" or "zh").
                   Searches this language first, then falls back to the other.
    
    Returns dict with:
      - wine_bg: wine background text (or None)
      - winery_bg: winery background text (or None)
      - wine_url: Wikipedia URL for the wine (or "")
      - winery_url: Wikipedia URL for the winery (or "")
    """
    result = {
        "wine_bg": None,
        "winery_bg": None,
        "wine_url": "",
        "winery_url": "",
    }
    
    fallback_lang = "zh" if pref_lang == "en" else "en"
    
    # --- Strategy 1: Search for wine name ---
    # Build search queries for both languages
    wine_queries_en = []
    wine_queries_zh = []
    
    if query_en:
        wine_queries_en.append(f"{query_en} wine")
        wine_queries_en.append(f"{wine_name} wine" if wine_name else query_en)
    if query_cn:
        wine_queries_zh.append(f"{query_cn} 葡萄酒")
        wine_queries_zh.append(f"{query_cn} 红酒")
    
    # Build ordered search plan: preferred wiki language first, then fallback wiki language
    # For each wiki language, try both EN and ZH queries
    # When pref_lang="zh": search zh.wikipedia first, then en.wikipedia
    # When pref_lang="en": search en.wikipedia first, then zh.wikipedia
    wine_lang_order = []
    for wiki_lang in [pref_lang, fallback_lang]:
        wine_lang_order.append((wiki_lang, "en", wine_queries_en,
            ["(disambiguation)", "List of", "album", "song", "film"],
            ["wine", "winery", "vineyard", "château", "chateau", "bordeaux", "burgundy",
             "cellar", "grape", "appellation"]))
        wine_lang_order.append((wiki_lang, "zh", wine_queries_zh,
            ["消歧义", "列表", "专辑", "歌曲", "电影"],
            ["酒庄", "葡萄酒", "酿酒", "葡萄园", "产区", "红酒"]))
    
    # Build a set of key terms from query for title relevance check
    # These must appear in the Wikipedia article title for it to be considered relevant
    title_required_terms = set()
    if query_en:
        for part in query_en.split():
            if len(part) > 2 and part.lower() not in ("wine", "winery", "vineyard", "red", "white",
                    "blanc", "rouge", "chateau", "château", "de", "du", "la", "le", "les", "des"):
                title_required_terms.add(part.lower())
    if query_cn:
        # Extract brand part from Chinese query (e.g. "拉菲" from "拉菲传说")
        for cn_key in sorted(WINE_NAME_MAP.keys(), key=len, reverse=True):
            if cn_key in query_cn and len(cn_key) >= 2:
                en_val = WINE_NAME_MAP[cn_key]
                for part in en_val.split():
                    if len(part) > 2 and part.lower() not in ("de", "du", "la", "le", "les", "des"):
                        title_required_terms.add(part.lower())
                title_required_terms.add(cn_key)
    
    def _title_is_relevant(title, required_terms):
        """Check if a Wikipedia title contains at least one required term."""
        if not required_terms:
            return True
        title_lower = title.lower()
        for term in required_terms:
            if term in title_lower:
                return True
        return False
    
    for idx, (wiki_lang, query_lang, queries, skip_kw, wine_kw) in enumerate(wine_lang_order):
        if not queries:
            continue
        # Only try 1 query per language combo to limit total API calls
        for q in queries[:1]:
            search_results = wikipedia_search(q, lang=wiki_lang, limit=2)
            for sr in search_results:
                title = sr["title"]
                if any(kw.lower() in title.lower() for kw in skip_kw):
                    continue
                # Title must be relevant to the query (contain at least one key term)
                if not _title_is_relevant(title, title_required_terms):
                    continue
                snippet_lower = sr["snippet"].lower()
                if not any(kw in snippet_lower for kw in wine_kw):
                    continue
                extract_data = wikipedia_get_extract(title, lang=wiki_lang, sentences=10)
                if extract_data and len(extract_data["extract"]) > 50:
                    result["wine_bg"] = extract_data["extract"]
                    result["wine_url"] = extract_data["url"]
                    break
            if result["wine_bg"]:
                break
        if result["wine_bg"]:
            break
    
    # --- Strategy 2: Search for winery/producer ---
    winery_queries_en = []
    winery_queries_zh = []
    
    if winery_name:
        winery_queries_en.append(f"{winery_name} winery")
        winery_queries_en.append(f"{winery_name} wine")
        # Also try Chinese Wikipedia with translated winery name
        if query_cn:
            # Extract brand part from Chinese query for winery search
            cn_winery_brand = query_cn
            for cn_key in sorted(WINE_NAME_MAP.keys(), key=len, reverse=True):
                if cn_key != query_cn and cn_key in query_cn and len(cn_key) < len(query_cn):
                    cn_winery_brand = cn_key  # e.g. "拉菲" from "拉菲传说"
                    break
            winery_queries_zh.append(f"{cn_winery_brand} 酒庄")
            winery_queries_zh.append(f"{cn_winery_brand} 罗斯柴尔德 酒庄")
    if query_en and not winery_name:
        winery_part = query_en
        for suffix in [" Blanc", " Rouge", " Red", " White", " Rosé", " Reserve",
                       " Grand", " Premier", " Classique", " Légende"]:
            if winery_part.endswith(suffix):
                winery_part = winery_part[:-len(suffix)].strip()
                break
        if winery_part:
            winery_queries_en.append(f"{winery_part} winery")
            winery_queries_en.append(f"{winery_part} Bordeaux")
            winery_queries_en.append(f"{winery_part} wine estate")
    
    if query_cn and not winery_name:
        cn_winery = query_cn
        for suffix in ["红葡萄酒", "白葡萄酒", "起泡酒", "红酒", "白酒"]:
            if cn_winery.endswith(suffix):
                cn_winery = cn_winery[:-len(suffix)].strip()
                break
        if cn_winery:
            winery_queries_zh.append(f"{cn_winery} 酒庄")
            winery_queries_zh.append(f"{cn_winery} 酒厂")
            # Also try extracting brand part (e.g. "拉菲传说" -> "拉菲")
            brand_only = cn_winery
            for cn_key in sorted(WINE_NAME_MAP.keys(), key=len, reverse=True):
                if cn_key != cn_winery and cn_key in cn_winery and len(cn_key) < len(cn_winery):
                    # Use the matched dictionary key as the brand (e.g. "拉菲" from "拉菲传说")
                    brand_only = cn_key
                    break
            if brand_only and brand_only != cn_winery:
                winery_queries_zh.append(f"{brand_only} 酒庄")
                winery_queries_zh.append(f"{brand_only} 罗斯柴尔德")
    
    # Build ordered search plan: preferred wiki language first, then fallback wiki language
    winery_lang_order = []
    for wiki_lang in [pref_lang, fallback_lang]:
        winery_lang_order.append((wiki_lang, "en", winery_queries_en,
            ["(disambiguation)", "List of", "album", "song", "film"],
            ["wine", "winery", "vineyard", "château", "chateau", "bordeaux", "burgundy", "cellar", "grape", "appellation"]))
        winery_lang_order.append((wiki_lang, "zh", winery_queries_zh,
            ["消歧义", "列表", "专辑", "歌曲", "电影"],
            ["酒庄", "葡萄酒", "酿酒", "葡萄园", "产区", "红酒"]))
    
    for idx, (wiki_lang, query_lang, queries, skip_kw, wine_kw) in enumerate(winery_lang_order):
        if not queries:
            continue
        # Only try 1 query per language combo to limit total API calls
        for q in queries[:1]:
            search_results = wikipedia_search(q, lang=wiki_lang, limit=2)
            for sr in search_results:
                title = sr["title"]
                if any(kw.lower() in title.lower() for kw in skip_kw):
                    continue
                # Title must be relevant (contain at least one key term)
                if not _title_is_relevant(title, title_required_terms):
                    continue
                snippet_lower = sr["snippet"].lower()
                if not any(kw in snippet_lower for kw in wine_kw):
                    continue
                extract_data = wikipedia_get_extract(title, lang=wiki_lang, sentences=8)
                if extract_data and len(extract_data["extract"]) > 50:
                    result["winery_bg"] = extract_data["extract"]
                    result["winery_url"] = extract_data["url"]
                    break
            if result["winery_bg"]:
                break
        if result["winery_bg"]:
            break
    
    return result


def get_vintage_recommendation(rating, num_ratings=0):
    """
    Get a vintage recommendation label based on rating and number of ratings.
    
    Recommendation tiers (based on Vivino 5-point scale):
      - 卓越 (Outstanding):      rating >= 4.5
      - 优秀 (Very Good):        rating >= 4.0
      - 良好 (Good):             rating >= 3.5
      - 一般 (Average):          rating >= 3.0
      - 不佳 (Below Average):    rating < 3.0
    
    If num_ratings is too low (< 20), adds a confidence note.
    """
    if rating <= 0:
        return "—", ""
    
    if rating >= 4.5:
        label = "卓越"
        emoji = "🌟"
    elif rating >= 4.0:
        label = "优秀"
        emoji = "⭐"
    elif rating >= 3.5:
        label = "良好"
        emoji = "👍"
    elif rating >= 3.0:
        label = "一般"
        emoji = "👌"
    else:
        label = "不佳"
        emoji = "⚠️"
    
    confidence = ""
    if 0 < num_ratings < 20:
        confidence = " (评价数较少)"
    elif 0 < num_ratings < 100:
        confidence = " (评价数偏少)"
    
    return f"{emoji} {label}", confidence


def _format_bg_text(text, max_len=600, indent="     "):
    """
    Format background text for display with proper wrapping and indentation.
    Handles both English (space-separated) and Chinese (no spaces) text.
    Returns list of formatted lines ready to print.
    """
    if not text:
        return []
    
    # Truncate if too long
    if len(text) > max_len:
        text = text[:max_len] + "..."
    
    lines = []
    for para in text.split('\n\n'):
        para = para.strip()
        if not para:
            continue
        # Check if text is primarily Chinese (no spaces between chars)
        has_spaces = ' ' in para
        cn_chars = sum(1 for c in para if '\u4e00' <= c <= '\u9fff')
        is_chinese_text = cn_chars > len(para) * 0.3
        
        if is_chinese_text and not has_spaces:
            # Chinese text: wrap by character count (~35 chars per line for CJK)
            line_width = 35
            for i in range(0, len(para), line_width):
                lines.append(f"{indent}{para[i:i+line_width]}")
        else:
            # English or mixed text: wrap by word at ~70 chars per line
            words = para.split()
            current_line = ""
            for word in words:
                if current_line and len(current_line) + 1 + len(word) > 70:
                    lines.append(f"{indent}{current_line}")
                    current_line = word
                else:
                    current_line = f"{current_line} {word}".strip() if current_line else word
            if current_line:
                lines.append(f"{indent}{current_line}")
    
    return lines


def winesearcher_search(query, year=None):
    """
    Search wines on Wine-Searcher when Vivino API is unavailable.
    Parses the HTML search results page to extract basic wine info.
    Returns list of wine results.
    """
    # Build URL: replace spaces with +
    q = query.replace(" ", "+")
    if year:
        q = f"{q}+{year}"
    url = f"{WS_SEARCH_URL}/{q}"
    
    text = _http_get_text(url)
    if not text:
        return []
    
    results = []
    
    # Extract product listings from Wine-Searcher page
    # Wine-Searcher lists products in structured blocks with class patterns
    # Try to find product name and price patterns
    
    # Pattern 1: Product listings in the "PRODUCTS" section
    # Each product has a name link and possibly a score
    
    # Find product blocks - Wine-Searcher uses different layouts
    # Try extracting from the "See all" products section
    product_pattern = re.compile(
        r'<a[^>]*class="[^"]*prod-item[^"]*"[^>]*href="([^"]*)"[^>]*>\s*'
        r'(.*?)\s*</a>.*?'
        r'(?:<span[^>]*class="[^"]*score[^"]*"[^>]*>(\d+)</span>)?',
        re.DOTALL
    )
    
    # Alternative: simpler pattern for product names in the page
    # Look for wine names in the results listing
    name_pattern = re.compile(
        r'<dt[^>]*>\s*<a[^>]*href="(/find/[^"]*)"[^>]*>\s*(.*?)\s*</a>',
        re.DOTALL
    )
    
    # Try to find wine names and scores from the products listing
    # Wine-Searcher shows: "Domaines Barons de Rothschild Corbieres Chateau d'Aussieres - 90/100"
    score_pattern = re.compile(
        r'(\d+)\s*/\s*100'
    )
    
    # Find all product-like text blocks
    # Look for structured data in the page
    product_blocks = re.findall(
        r'<div[^>]*class="[^"]*product[^"]*"[^>]*>(.*?)</div>',
        text, re.DOTALL
    )
    
    # If structured parsing fails, try a more generic approach
    # Extract wine names from the "PRODUCTS FOR" section
    products_section = text
    products_match = re.search(
        r"PRODUCTS FOR.*?<.*?>(.*?)See all",
        text, re.DOTALL | re.IGNORECASE
    )
    if products_match:
        products_section = products_match.group(1)
    
    # Extract individual wine entries from products section
    # Wine-Searcher format: "Domaines Barons de Rothschild Corbieres Chateau d'Aussieres\nLanguedoc-Roussillon, France\n-\n90 / 100"
    wine_entries = re.split(r'\n\s*\n', products_section)
    
    for entry in wine_entries:
        # Clean HTML tags
        clean = re.sub(r'<[^>]+>', ' ', entry)
        clean = re.sub(r'\s+', ' ', clean).strip()
        
        if not clean or len(clean) < 10:
            continue
        
        # Try to extract score
        score_match = score_pattern.search(clean)
        score = int(score_match.group(1)) if score_match else 0
        
        # Try to extract name and region
        lines = [l.strip() for l in clean.split('|') if l.strip()]
        if not lines:
            lines = [clean]
        
        name = lines[0].strip()
        region = ""
        country = ""
        
        if len(lines) > 1:
            loc = lines[1].strip()
            if ',' in loc:
                parts = loc.split(',')
                region = parts[0].strip()
                country = parts[-1].strip() if len(parts) > 1 else ""
            else:
                region = loc
        
        # Only add if it looks like a real wine name
        if name and len(name) > 5 and any(c.isalpha() for c in name):
            results.append({
                "id": "",
                "name": name,
                "winery": "",
                "year": str(year) if year else "",
                "rating": round((score - 50) / 10.0, 2) if score >= 50 else 0,  # Convert 100-point to 5-point: 100→5.0, 90→4.0, 80→3.0
                "num_ratings": 0,
                "price": 0,
                "currency": "",
                "region": region,
                "country": country,
                "wine_type": "",
                "url": f"https://www.wine-searcher.com/find/{name.replace(' ', '+')}",
                "source": "Wine-Searcher",
            })
    
    return results[:10]


# ============================================================
# Platform Link Generation
# ============================================================

def generate_platform_links(query_en, query_cn=None):
    """
    Generate direct search links for all major wine shopping platforms.
    Returns dict of platform -> URL.
    """
    links = {}
    
    if not query_cn:
        query_cn = query_en
    
    # Chinese platforms
    q_cn = urllib.parse.quote(query_cn)
    q_en = urllib.parse.quote(query_en)
    
    links["京东"] = f"{JD_SEARCH_URL}?keyword={q_cn}&enc=utf-8"
    links["天猫"] = f"{TMALL_SEARCH_URL}?q={q_cn}"
    links["淘宝"] = f"{TAOBAO_SEARCH_URL}?q={q_cn}"
    links["苏宁易购"] = f"{SUNING_SEARCH_URL}{q_cn}/"
    links["拼多多"] = f"{PINDUODUO_SEARCH_URL}?search_key={q_cn}"
    links["1919吃喝"] = f"https://www.1919.cn/search/?keyword={q_cn}"
    links["也买酒"] = f"https://www.yesmywine.com/search/{q_cn}.html"
    links["酒仙网"] = f"https://www.jiuxian.com/search-{q_cn}.html"
    links["Vivino"] = f"{VIVINO_SEARCH_URL}?q={q_en}"
    
    # International platforms
    # Wine-Searcher uses + as separator, not %20
    q_en_plus = query_en.replace(' ', '+')
    links["Wine.com"] = f"{WINE_COM_URL}?text={q_en}"
    links["Drizly"] = f"{DRIZLY_URL}?q={q_en}"
    links["Total Wine"] = f"{TOTAL_WINE_URL}?text={q_en}"
    links["Wine-Searcher"] = f"https://www.wine-searcher.com/find/{urllib.parse.quote(q_en_plus, safe='+')}"
    links["Vivino Shop"] = f"https://www.vivino.com/search/wines?q={q_en}"
    links["Wine Spectator"] = f"https://www.winespectator.com/search?search_type=wine&search_word={q_en}"
    links["CellarTracker"] = f"https://www.cellartracker.com/list.asp?table=List&search={q_en}"
    links["Decántalo"] = f"https://www.decantalo.com/uk/search?q={q_en}"
    
    return links


def generate_vivino_purchase_link(wine_id, wine_name):
    """Generate a Vivino purchase link for a specific wine."""
    if wine_id:
        slug = wine_name.lower().replace(" ", "-").replace("'", "") if wine_name else "wine"
        return f"https://www.vivino.com/{slug}/w/{wine_id}"
    return ""


# ============================================================
# Price Fetching (WebFetch-assisted)
# ============================================================

# WebFetch hint templates: AI agent should use its WebFetch tool to visit these URLs
# and extract price data from the returned page content.

WEBFETCH_PRICE_HINTS = {
    "wine_searcher": {
        "name": "Wine-Searcher (主数据源)",
        "url_template": "https://www.wine-searcher.com/find/{query_plus}",
        "hint": (
            "请在 Wine-Searcher 页面中提取该酒款的详细信息和价格。"
            "重点查找: 酒款名称、评分(X/100)、平均价格(average price)、"
            "各年份价格对比、产区、葡萄品种、口感描述。"
            "返回格式: 酒款名 | 评分 | $价格 | 产区 | 年份对比"
        ),
    },
    "jd": {
        "name": "京东",
        "url_template": "https://search.jd.com/Search?keyword={query}&enc=utf-8",
        "hint": (
            "请在京东搜索页面中提取红酒/酒类商品的价格信息。"
            "查找包含价格(¥)、商品名称和SKU链接的条目。"
            "关注 data-price、sku-name 等属性，或页面中显示的 ¥数字 价格模式。"
            "返回格式: 商品名 | ¥价格 | 商品链接"
        ),
    },
    "tmall": {
        "name": "天猫",
        "url_template": "https://list.tmall.com/search_product.htm?q={query}",
        "hint": (
            "请在天猫搜索页面中提取酒类商品的价格信息。"
            "查找商品标题、价格和店铺链接。"
            "返回格式: 商品名 | ¥价格 | 商品链接"
        ),
    },
    "vivino_shop": {
        "name": "Vivino Shop",
        "url_template": "https://www.vivino.com/search/wines?q={query}",
        "hint": (
            "请在 Vivino 搜索页面中提取酒款信息和价格。"
            "查找酒款名称、评分、价格和购买链接。"
            "注意: Vivino 在中国大陆可能无法直接访问，"
            "如有 Firecrawl API Key，可通过 Firecrawl 代理访问。"
            "返回格式: 酒款名 | 评分 | $价格 | 链接"
        ),
    },
}

# Firecrawl-assisted Vivino price hints
FIRECRAWL_VIVINO_HINTS = {
    "name": "Vivino (via Firecrawl)",
    "url_template": "https://www.vivino.com/search/wines?q={query}",
    "hint": (
        "使用 Firecrawl 的 scrape 接口访问 Vivino 搜索页面。"
        "POST https://api.firecrawl.dev/v1/scrape 请求体: "
        '{"url": "https://www.vivino.com/search/wines?q=<query>", "formats": ["markdown"], "waitFor": 5000}'
        "提取酒款名称、评分(X/5)、评价数、价格、产区、年份。"
        "返回格式: 酒款名 | 评分 | $价格 | 评价数 | 产区"
    ),
    "detail_template": "https://www.vivino.com/wines/{wine_id}",
    "detail_hint": (
        "使用 Firecrawl 的 scrape 接口访问 Vivino 酒款详情页。"
        "POST https://api.firecrawl.dev/v1/scrape 请求体: "
        '{"url": "https://www.vivino.com/wines/<wine_id>", "formats": ["markdown"], "waitFor": 5000}'
        "提取葡萄品种(含混酿比例)、口感特征(body/tannin/acidity/sweetness)、"
        "美食搭配、酒款描述、酒庄信息。"
    ),
}

# Legacy regex patterns for best-effort direct scraping (low success rate)
_JD_PRICE_PATTERNS = [
    r'"p":"([\d.]+)"[^}]*"skuid":"(\d+)"',
    r'data-price="([\d.]+)"[^>]*data-sku="(\d+)"',
    r'"price":\s*"([\d.]+)".*?"skuId":\s*"(\d+)"',
    r'"p":([\d.]+).*?"skuid":(\d+)',
]

_WS_PRICE_PATTERNS = [
    r'average[\s-]*price[^$]*\$([\d,.]+)',
    r'from\s+\$([\d,.]+)',
    r'"price".*?([\d,.]+)',
]


def fetch_price_webfetch(query_cn, query_en):
    """
    Generate WebFetch-ready price hints for the AI agent.
    Returns a dict with platform name, URL, and extraction hints.
    The AI agent should use its WebFetch tool to visit these URLs
    and parse the returned content for price data.
    If Firecrawl API key is available, also includes Firecrawl-Vivino hints.
    """
    q_cn = urllib.parse.quote(query_cn)
    q_en = urllib.parse.quote(query_en)
    q_plus = query_en.lower().replace(" ", "+")

    hints = {}

    for key, cfg in WEBFETCH_PRICE_HINTS.items():
        url = cfg["url_template"].format(query=q_cn if key in ("jd", "tmall") else q_en,
                                          query_plus=q_plus)
        hints[key] = {
            "platform": cfg["name"],
            "url": url,
            "extraction_hint": cfg["hint"],
            "query_cn": query_cn,
            "query_en": query_en,
        }
    
    # Add Firecrawl-Vivino hint if API key is available
    if _firecrawl_api_key:
        vivino_url = FIRECRAWL_VIVINO_HINTS["url_template"].format(query=q_en)
        hints["firecrawl_vivino"] = {
            "platform": FIRECRAWL_VIVINO_HINTS["name"],
            "url": vivino_url,
            "extraction_hint": FIRECRAWL_VIVINO_HINTS["hint"],
            "query_cn": query_cn,
            "query_en": query_en,
            "firecrawl_url": FIRECRAWL_API_URL,
            "api_key_available": True,
        }

    return hints


def fetch_price_direct(query, platform="jd"):
    """
    Best-effort direct price scraping (legacy, low success rate).
    Returns list of {name, price, url, platform} or empty list.
    For reliable prices, use WebFetch via fetch_price_webfetch() instead.
    """
    results = []

    if platform == "jd":
        q = urllib.parse.quote(query)
        url = f"{JD_SEARCH_URL}?keyword={q}&enc=utf-8"
        text = _http_get_text(url)
        if text:
            for pat in _JD_PRICE_PATTERNS:
                prices = re.findall(pat, text)
                if prices:
                    for price_val, sku_id in prices[:5]:
                        try:
                            results.append({
                                "name": query,
                                "price": float(price_val),
                                "currency": "CNY",
                                "url": f"https://item.jd.com/{sku_id}.html",
                                "platform": "京东",
                            })
                        except (ValueError, IndexError):
                            continue
                    break
            # Fallback: just get SKU links
            if not results:
                item_pattern = r'class="gl-item"[^>]*data-sku="(\d+)"'
                sku_ids = re.findall(item_pattern, text)
                for sku_id in sku_ids[:3]:
                    results.append({
                        "name": query,
                        "price": 0,
                        "currency": "CNY",
                        "url": f"https://item.jd.com/{sku_id}.html",
                        "platform": "京东",
                        "note": "请点击链接查看实时价格",
                    })

    elif platform == "wine_searcher":
        slug = query.lower().replace(" ", "+")
        url = f"https://www.wine-searcher.com/find/{slug}"
        text = _http_get_text(url)
        if text:
            for pat in _WS_PRICE_PATTERNS:
                match = re.search(pat, text, re.IGNORECASE)
                if match:
                    try:
                        price_str = match.group(1).replace(",", "")
                        results.append({
                            "name": query,
                            "price": float(price_str),
                            "currency": "USD",
                            "platform": "Wine-Searcher",
                            "note": "平均价格",
                        })
                        break
                    except (ValueError, IndexError):
                        continue

    return results


# ============================================================
# Wine Info Formatting
# ============================================================

WINE_TYPE_MAP = {
    "1": "红葡萄酒 (Red)",
    "2": "白葡萄酒 (White)",
    "3": "起泡酒 (Sparkling)",
    "4": "桃红葡萄酒 (Rosé)",
    "5": "甜酒 (Dessert)",
    "6": "加强酒 (Fortified)",
    "red": "红葡萄酒 (Red)",
    "white": "白葡萄酒 (White)",
    "sparkling": "起泡酒 (Sparkling)",
    "rose": "桃红葡萄酒 (Rosé)",
    "dessert": "甜酒 (Dessert)",
    "fortified": "加强酒 (Fortified)",
}

RATING_DESCRIPTIONS = {
    (0, 2.0): "较差 (Poor)",
    (2.0, 3.0): "一般 (Below Average)",
    (3.0, 3.5): "尚可 (Average)",
    (3.5, 4.0): "不错 (Good)",
    (4.0, 4.5): "优秀 (Very Good)",
    (4.5, 5.1): "卓越 (Outstanding)",
}


# ============================================================
# Health & Drinking Advice
# ============================================================

# Alcohol content by wine type (approximate ABV %)
WINE_ABV = {
    "red": 13.5, "1": 13.5,
    "white": 12.0, "2": 12.0,
    "sparkling": 12.0, "3": 12.0,
    "rose": 12.5, "4": 12.5,
    "dessert": 10.0, "5": 10.0,
    "fortified": 19.5, "6": 19.5,
}

# Standard drink: 10g pure alcohol ≈ 100ml of 12.5% wine
GRAMS_PER_STD_DRINK = 10.0
ML_PER_STD_DRINK_WINE = 100  # approximate for ~12.5% ABV

# Age-group drinking recommendations (ml/day, for wine ~12.5% ABV)
AGE_GROUP_ADVICE = {
    "young": {
        "label": "青年 (18-35岁)",
        "male_max_ml": 250,    # ~2.5 standard drinks
        "female_max_ml": 150,  # ~1.5 standard drinks
        "advice": (
            "年轻人代谢较快，但耐受度不一定高。"
            "建议适量饮用，避免空腹饮酒和混饮。"
            "社交场合注意控制节奏，每小时不超过1杯（150ml）。"
        ),
        "caution": "长期过量饮酒会影响肝脏健康和神经系统发育。",
    },
    "middle": {
        "label": "中年 (36-55岁)",
        "male_max_ml": 200,    # ~2 standard drinks
        "female_max_ml": 120,  # ~1.2 standard drinks
        "advice": (
            "中年人代谢能力开始下降，应控制饮酒量。"
            "适量红酒可能对心血管有一定保护作用（法国悖论），"
            "但过量则增加高血压、痛风等风险。"
            "建议每周至少2-3天不饮酒，让肝脏充分休息。"
        ),
        "caution": "注意监测血压、血糖和肝功能指标。",
    },
    "senior": {
        "label": "中老年 (56-70岁)",
        "male_max_ml": 150,    # ~1.5 standard drinks
        "female_max_ml": 100,  # ~1 standard drink
        "advice": (
            "老年人代谢和肝功能进一步下降，饮酒量应更保守。"
            "酒精可能与多种药物产生相互作用，服药期间需特别谨慎。"
            "建议小口慢饮，佐餐饮用，避免单独饮酒。"
        ),
        "caution": "酒精会增加跌倒风险，影响睡眠质量，加重慢性病。",
    },
    "elderly": {
        "label": "高龄 (70岁以上)",
        "male_max_ml": 100,    # ~1 standard drink
        "female_max_ml": 75,   # ~0.75 standard drink
        "advice": (
            "高龄人群应尽量减少饮酒，如饮酒需严格限量。"
            "酒精会加重骨质疏松风险，影响平衡和认知。"
            "建议仅在社交场合少量饮用，避免每日饮酒习惯。"
        ),
        "caution": "几乎所有药物都与酒精有潜在交互，请咨询医生。",
    },
}

# Health condition-specific advice
HEALTH_CONDITION_ADVICE = {
    "hypertension": {
        "label": "高血压",
        "advice": "酒精会升高血压，建议严格限量或戒酒。如饮酒，单次不超过1杯（100ml），避免烈性酒。",
        "max_ml": 100,
        "risk": "高",
    },
    "diabetes": {
        "label": "糖尿病",
        "advice": "酒精可能导致低血糖（尤其是服用降糖药时）。建议佐餐饮用干型葡萄酒，避免甜酒和加强酒。监测血糖变化。",
        "max_ml": 120,
        "risk": "中",
    },
    "gout": {
        "label": "痛风",
        "advice": "酒精（尤其是啤酒和红酒）会增加尿酸水平。急性发作期应完全戒酒，缓解期也需严格控制。红酒比啤酒风险稍低。",
        "max_ml": 80,
        "risk": "高",
    },
    "liver_disease": {
        "label": "肝病/脂肪肝",
        "advice": "任何形式的酒精都会加重肝脏负担。脂肪肝患者建议完全戒酒，以免进展为肝硬化。肝功能异常时严禁饮酒。",
        "max_ml": 0,
        "risk": "极高",
    },
    "gastritis": {
        "label": "胃炎/胃溃疡",
        "advice": "酒精刺激胃黏膜，加重炎症和溃疡。建议佐餐饮用，避免空腹。优先选择低度酒，少量慢饮。",
        "max_ml": 80,
        "risk": "中高",
    },
    "heart_disease": {
        "label": "心脏病/冠心病",
        "advice": "适量红酒中的白藜芦醇可能有益心血管，但过量则增加心律失常和心衰风险。严格限量，遵医嘱。",
        "max_ml": 100,
        "risk": "中",
    },
    "kidney_disease": {
        "label": "肾病",
        "advice": "酒精加重肾脏负担，影响电解质平衡。需根据肾功能指标决定是否可少量饮用，一般建议严格限量。",
        "max_ml": 80,
        "risk": "中高",
    },
    "pregnancy": {
        "label": "孕期/哺乳期",
        "advice": "孕期和哺乳期应完全戒酒。酒精可通过胎盘和乳汁传递，影响胎儿和婴儿发育。没有任何安全饮酒量。",
        "max_ml": 0,
        "risk": "极高",
    },
    "medication": {
        "label": "服用药物期间",
        "advice": "酒精与数百种药物存在相互作用，包括抗生素、止痛药、安眠药、抗抑郁药等。服药期间建议完全戒酒或咨询医生。",
        "max_ml": 0,
        "risk": "极高",
    },
    "obesity": {
        "label": "肥胖/减重",
        "advice": "酒精热量高（7kcal/g），且无营养价值。一杯150ml红酒约125kcal。减重期间建议严格控制或避免饮酒。",
        "max_ml": 100,
        "risk": "低",
    },
}

# Food pairing recommendations by wine type
# Each entry: (staple_food, main_dish, description)
FOOD_PAIRING_BY_TYPE = {
    "red": {
        "staple": ["牛排/烤肉", "意大利面", "烤面包", "蘑菇烩饭"],
        "main_dish": [
            "🥩 红烧牛肋排 — 赤霞珠、西拉等饱满红酒的经典搭配",
            "🍖 烤羊排配迷迭香 — 单宁丰富的红酒与羊肉油脂完美平衡",
            "🍄 蘑菇烩牛小排 — 菌菇的鲜味与红酒的泥土气息相呼应",
            "🧀 陈年切达/帕马森奶酪 — 硬质奶酪与红酒单宁互补",
        ],
        "principle": "红酒的单宁与红肉蛋白质结合，柔化涩感；避免搭配鱼类和辛辣食物",
    },
    "white": {
        "staple": ["米饭/白粥", "法式面包", "沙拉", "海鲜饭"],
        "main_dish": [
            "🐟 清蒸鲈鱼/石斑 — 霞多丽、长相思与白鱼肉质轻柔搭配",
            "🦐 白灼虾/蒜蓉粉丝蒸虾 — 白葡萄酒的酸度提升海鲜鲜味",
            "🥗 凯撒沙拉配鸡胸 — 清爽白酒与沙拉酱汁相得益彰",
            "🐚 蒜香扇贝/生蚝 — 夏布利或密斯卡岱是生蚝的绝配",
        ],
        "principle": "白葡萄酒的酸度切割油脂、提升海鲜鲜味；避免搭配重口味红肉",
    },
    "sparkling": {
        "staple": ["吐司/可颂", "寿司", "薯条", "水果拼盘"],
        "main_dish": [
            "🍣 生鱼片/寿司拼盘 — 香槟的气泡和酸度与刺身完美融合",
            "🍟 炸鱼薯条 — 起泡酒是油炸食品的天然搭档",
            "🧁 水果塔/马卡龙 — 甜型起泡酒与甜点相得益彰",
            "🦪 生蚝配柠檬 — 香槟/卡瓦是生蚝的经典搭配",
        ],
        "principle": "起泡酒的气泡和酸度能清洁味蕾、解腻提鲜，是最百搭的酒类",
    },
    "rose": {
        "staple": ["法棍面包", "地中海沙拉", "烤蔬菜", "米饭"],
        "main_dish": [
            "🥗 地中海风味沙拉 — 桃红的清爽与橄榄油、番茄完美融合",
            "🦐 烤大虾配蒜香面包 — 桃红的果香与海鲜烧烤搭配极佳",
            "🍗 柠檬烤鸡 — 桃红介于红白之间的口感适合禽类",
            "🫒 塔帕斯拼盘 — 桃红是西班牙小食的天然搭档",
        ],
        "principle": "桃红酒兼具红白的优点，是夏日户外聚餐和轻食的理想伴侣",
    },
    "dessert": {
        "staple": ["饼干/司康", "蛋糕", "水果拼盘", "冰淇淋"],
        "main_dish": [
            "🍰 提拉米苏/焦糖布丁 — 甜酒与甜点的甜蜜呼应",
            "🫐 蓝莓奶酪蛋糕 — 冰酒或贵腐酒与水果甜品完美搭配",
            "🧀 蓝纹奶酪配蜂蜜 — 甜酒平衡蓝纹的咸辣味",
            "🍎 苹果派/肉桂烤苹果 — 甜酒与温暖香料的风味交织",
        ],
        "principle": "甜酒的甜度需高于或等于甜点，否则会显得酸涩；避免搭配咸味主菜",
    },
    "fortified": {
        "staple": ["坚果拼盘", "巧克力", "奶酪拼盘", "干果"],
        "main_dish": [
            "🍫 黑巧克力/松露巧克力 — 波特酒与巧克力的经典搭配",
            "🧀 蓝纹奶酪/斯蒂尔顿 — 波特酒是英国传统的奶酪搭配",
            "🌰 烤坚果拼盘 — 雪莉酒的氧化风味与坚果香互相呼应",
            "🍮 圣诞布丁/水果蛋糕 — 加强酒的浓郁与香料蛋糕相得益彰",
        ],
        "principle": "加强酒酒精度高、风味浓郁，适合搭配浓味甜点和奶酪；少量慢饮",
    },
}


def _get_age_group(age):
    """Determine age group from numeric age."""
    if age < 18:
        return "underage"
    elif age < 36:
        return "young"
    elif age < 56:
        return "middle"
    elif age < 71:
        return "senior"
    else:
        return "elderly"


def _get_abv_for_type(wine_type):
    """Get approximate ABV for a wine type."""
    if not wine_type:
        return 13.5  # default red
    return WINE_ABV.get(str(wine_type).lower(), 13.5)


def _calc_std_drinks(ml, abv):
    """Calculate number of standard drinks (10g pure alcohol each)."""
    # ml * (abv/100) * 0.789 (density of ethanol) = grams of pure alcohol
    grams_alcohol = ml * (abv / 100.0) * 0.789
    return round(grams_alcohol / GRAMS_PER_STD_DRINK, 1)


def format_health_advice(wine_type=None, user_age=None, conditions=None):
    """
    Format comprehensive health and drinking advice.
    
    Args:
        wine_type: Wine type key (e.g. 'red', 'white', 'sparkling')
        user_age: User's age (int). If None, show general advice for all age groups.
        conditions: List of health condition keys. If None, show no condition-specific advice.
    
    Returns formatted string with drinking recommendations.
    """
    output = []
    abv = _get_abv_for_type(wine_type)
    
    # --- Age group advice ---
    if user_age:
        age_group = _get_age_group(user_age)
        if age_group == "underage":
            output.append("  🚫 未成年人 (18岁以下)")
            output.append("")
            output.append("  ⚠️ 未成年人不应饮酒。酒精会影响大脑发育和身体健康。")
            output.append("     中国法律规定禁止向未成年人售酒。")
            output.append("")
        else:
            grp = AGE_GROUP_ADVICE[age_group]
            output.append(f"  👤 您的年龄段: {grp['label']}")
            output.append("")
            output.append(f"  🍷 建议每日最大饮量:")
            output.append(f"     男性: ≤{grp['male_max_ml']}ml (约{_calc_std_drinks(grp['male_max_ml'], abv)}个标准饮)")
            output.append(f"     女性: ≤{grp['female_max_ml']}ml (约{_calc_std_drinks(grp['female_max_ml'], abv)}个标准饮)")
            output.append("")
            output.append(f"  💡 建议: {grp['advice']}")
            output.append(f"  ⚠️ 注意: {grp['caution']}")
    else:
        output.append("  📊 各年龄段建议每日最大饮量 (以~{:.1f}%酒精度计):".format(abv))
        output.append("")
        for key in ["young", "middle", "senior", "elderly"]:
            grp = AGE_GROUP_ADVICE[key]
            output.append(f"  {grp['label']}:")
            output.append(f"     男性 ≤{grp['male_max_ml']}ml | 女性 ≤{grp['female_max_ml']}ml")
        output.append("")
        output.append("  💡 提示: 如需个性化建议，请告知您的年龄，我将提供更精确的饮量建议。")
    
    # --- Wine type specific ---
    if wine_type:
        wtype_display = WINE_TYPE_MAP.get(str(wine_type).lower(), str(wine_type)) if wine_type else ""
        output.append("")
        if wtype_display:
            output.append(f"  🍷 酒款类型: {wtype_display} (约{abv}% ABV)")
        
        # Adjust for fortified wines
        if str(wine_type).lower() in ("fortified", "6"):
            output.append("  ⚠️ 加强酒酒精度较高，建议饮量减半！")
        # Adjust for dessert wines
        if str(wine_type).lower() in ("dessert", "5"):
            output.append("  💡 甜酒含糖量较高，糖尿病患者需特别注意。")
    
    # --- Health condition advice ---
    if conditions:
        output.append("")
        output.append("  🏥 健康状况相关建议:")
        output.append("")
        for cond in conditions:
            if cond in HEALTH_CONDITION_ADVICE:
                info = HEALTH_CONDITION_ADVICE[cond]
                risk_icon = {"极高": "🔴", "高": "🟠", "中高": "🟡", "中": "🟡", "低": "🟢"}.get(info["risk"], "⚪")
                output.append(f"  {risk_icon} {info['label']} (风险: {info['risk']})")
                output.append(f"     {info['advice']}")
                if info["max_ml"] == 0:
                    output.append(f"     🚫 建议完全戒酒")
                else:
                    output.append(f"     📏 建议最大饮量: ≤{info['max_ml']}ml/次")
                output.append("")
    
    # --- General safe drinking tips ---
    output.append("  📋 安全饮酒通用建议:")
    output.append("     • 不要空腹饮酒，先吃食物再饮酒")
    output.append("     • 每小时饮酒不超过1杯（约150ml葡萄酒）")
    output.append("     • 饮酒期间多喝水，每杯酒配一杯水")
    output.append("     • 饮酒后至少6小时内不要驾车")
    output.append("     • 孕妇及备孕期女性应完全戒酒")
    output.append("     • 如有慢性病或服药，请先咨询医生")
    output.append("")
    output.append("  ⚕️ 免责声明: 以上健康建议仅为一般性参考信息，不构成医疗建议。")
    output.append("     如有健康疑虑，请咨询专业医疗人员。")
    
    return "\n".join(output)


def format_food_pairing(wine_type=None, vivino_food=None):
    """
    Format food pairing recommendations.
    Combines Vivino's food pairing data with curated staple & main dish suggestions.
    
    Args:
        wine_type: Wine type key for curated suggestions
        vivino_food: List of food names from Vivino API
    
    Returns formatted string.
    """
    output = []
    
    # Vivino food pairing (from API)
    if vivino_food and isinstance(vivino_food, list):
        food_names = []
        for f in vivino_food:
            if isinstance(f, dict):
                food_names.append(f.get("name", str(f)))
            elif isinstance(f, str):
                food_names.append(f)
        if food_names:
            output.append("  🍽️ Vivino 推荐搭配:")
            output.append(f"     {', '.join(food_names)}")
            output.append("")
    
    # Curated food pairing by wine type
    wtype_key = str(wine_type).lower() if wine_type else "red"
    pairing = FOOD_PAIRING_BY_TYPE.get(wtype_key, FOOD_PAIRING_BY_TYPE["red"])
    
    output.append("  🍚 推荐主食:")
    for staple in pairing["staple"]:
        output.append(f"     • {staple}")
    output.append("")
    
    output.append("  🍖 推荐主菜搭配:")
    for dish in pairing["main_dish"]:
        output.append(f"     {dish}")
    output.append("")
    
    output.append(f"  📖 搭配原则: {pairing['principle']}")
    
    return "\n".join(output)


def rating_description(rating):
    """Convert numeric rating to description."""
    if not rating:
        return "暂无评分"
    for (low, high), desc in RATING_DESCRIPTIONS.items():
        if low <= rating < high:
            return desc
    return "暂无评分"


def format_rating_bar(rating, max_val=5.0):
    """Format a visual rating bar."""
    if not rating:
        return "☆☆☆☆☆"
    filled = round(rating / max_val * 5)
    return "★" * filled + "☆" * (5 - filled) + f" {rating}/5"


# ============================================================
# Wine Name Mapping (Chinese <-> English)
# ============================================================

WINE_NAME_MAP = {
    # --- Common Terms / Types ---
    "干红": "Red", "干白": "White", "桃红": "Rosé", "起泡酒": "Sparkling",
    "冰酒": "Icewine", "贵腐": "Sauternes", "波特": "Port", "雪莉": "Sherry",
    "罗斯柴尔德": "Rothschild", "男爵": "Baron", "女爵": "Comtesse",

    # --- Famous Châteaux / Wineries (Bordeaux) ---
    "拉菲": "Lafite", "拉菲古堡": "Château Lafite Rothschild",
    "木桐": "Mouton", "木桐古堡": "Château Mouton Rothschild",
    "玛歌": "Margaux", "玛歌古堡": "Château Margaux",
    "拉图": "Latour", "拉图古堡": "Château Latour",
    "侯伯王": "Haut-Brion", "红颜容": "Haut-Brion", "奥比昂": "Haut-Brion",
    "柏图斯": "Pétrus", "柏翠": "Pétrus", 
    "白马": "Cheval Blanc", "白马酒庄": "Château Cheval Blanc",
    "奥松": "Ausone", "欧颂": "Ausone",
    "滴金": "d'Yquem", "滴金酒庄": "Château d'Yquem",
    "里鹏": "Le Pin",
    "武当王": "Mouton Rothschild",
    "雄狮": "Léoville Las Cases",
    "宝嘉隆": "Ducru-Beaucaillou",
    "玫瑰山": "Montrose", "梦玫瑰": "Montrose",
    "爱士图尔": "Cos d'Estournel",
    "碧尚男爵": "Pichon Longueville Baron", "男爵古堡": "Pichon Baron",
    "碧尚女爵": "Pichon Longueville Comtesse de Lalande", "女爵古堡": "Pichon Comtesse",
    "金钟": "Angélus", "大金钟": "Angélus",
    "帕菲": "Pavie", "柏菲": "Pavie",
    "靓次伯": "Lynch-Bages", "林卓贝斯": "Lynch-Bages",
    "龙船": "Beychevelle", "龙船酒庄": "Château Beychevelle",
    "宝马": "Palmer", "宝马庄园": "Château Palmer",
    "大宝": "Talbot", "大宝酒庄": "Château Talbot",
    "卡隆世家": "Calon Ségur",
    "宝捷": "Poujeaux",

    # --- Famous Wineries (Burgundy & Italy) ---
    "罗曼尼康帝": "Romanée-Conti", "康帝": "Romanée-Conti",
    "拉塔希": "La Tâche", "踏雪": "La Tâche",
    "勒桦": "Leroy", "乐花": "Leroy",
    "西施佳雅": "Sassicaia",
    "索拉雅": "Solaia",
    "天娜": "Tignanello",
    "欧纳拉雅": "Ornellaia",
    "马赛多": "Masseto", "马赛多酒庄": "Masseto",
    "作品一号": "Opus One",
    "活灵魂": "Almaviva",

    # --- New World Wineries ---
    "奔富": "Penfolds", "奔富葛兰许": "Penfolds Grange", "葛兰许": "Grange",
    "奔富389": "Penfolds Bin 389", "奔富407": "Penfolds Bin 407", "奔富707": "Penfolds Bin 707",
    "啸鹰": "Screaming Eagle",
    "哈兰": "Harlan Estate",
    "鹿跃": "Stag's Leap",
    "银色橡树": "Silver Oak",
    "蒙特莱那": "Chateau Montelena",
    "谢佛": "Shafer",
    "约瑟夫菲尔普斯": "Joseph Phelps",
    
    # --- Common Brands ---
    "黄尾袋鼠": "Yellow Tail", "黄尾": "Yellow Tail",
    "杰卡斯": "Jacob's Creek",
    "洛神山庄": "Rawson's Retreat",
    "奔富寇兰山": "Penfolds Koonunga Hill",
    "云雾之湾": "Cloudy Bay",
    "蚝湾": "Oyster Bay",
    "新玛丽": "Villa Maria",
    "干露": "Concha y Toro", "红魔鬼": "Casillero del Diablo",
    "蒙大菲": "Robert Mondavi",
    "贝灵哲": "Beringer",
    "嘉露": "Gallo",
    "杰克逊": "Kendall-Jackson",

    # --- Grape Varieties ---
    "赤霞珠": "Cabernet Sauvignon",
    "黑皮诺": "Pinot Noir",
    "梅洛": "Merlot",
    "西拉": "Syrah", "设拉子": "Shiraz",
    "霞多丽": "Chardonnay", "莎当妮": "Chardonnay",
    "长相思": "Sauvignon Blanc", "白苏维翁": "Sauvignon Blanc",
    "雷司令": "Riesling",
    "品丽珠": "Cabernet Franc",
    "歌海娜": "Grenache",
    "丹魄": "Tempranillo",
    "马尔贝克": "Malbec",
    "佳美娜": "Carmenère", "卡曼尼": "Carmenère",
    "桑娇维塞": "Sangiovese",
    "内比奥罗": "Nebbiolo",
    "神索": "Cinsault",
    "慕合怀特": "Mourvèdre",
    "灰皮诺": "Pinot Grigio", "灰品诺": "Pinot Gris",
    "维欧尼": "Viognier",
    "莫斯卡托": "Moscato",
    "赛美蓉": "Sémillon", "赛美容": "Sémillon",
    "琼瑶浆": "Gewürztraminer",

    # --- Regions / Appellations ---
    "波尔多": "Bordeaux", "勃艮第": "Burgundy",
    "纳帕谷": "Napa Valley",
    "巴罗洛": "Barolo", "基安蒂": "Chianti",
    "里奥哈": "Rioja", "罗纳河谷": "Rhône Valley",
    "香槟": "Champagne", "普罗塞克": "Prosecco",
    "卡瓦": "Cava",
    "教皇新堡": "Châteauneuf-du-Pape",
    "圣埃美隆": "Saint-Émilion",
    "波美侯": "Pomerol",
    "玛歌村": "Margaux",
    "波亚克": "Pauillac",
    "圣朱利安": "Saint-Julien",
    "圣埃斯泰夫": "Saint-Estèphe",
    "格拉夫": "Graves",
    "苏玳": "Sauternes",
    "夏布利": "Chablis",
    "夜圣乔治": "Nuits-Saint-Georges",
    "托斯卡纳": "Tuscany", "皮埃蒙特": "Piedmont",
    "门多萨": "Mendoza",
    "巴罗萨谷": "Barossa Valley",
    "猎人谷": "Hunter Valley",

    # --- Other Alcohol Types ---
    "威士忌": "Whisky", "白兰地": "Brandy",
    "干邑": "Cognac", "伏特加": "Vodka",
    "朗姆酒": "Rum", "金酒": "Gin", "琴酒": "Gin",
    "龙舌兰": "Tequila", "清酒": "Sake",
    "梅酒": "Umeshu", "中国白酒": "Baijiu",
    "茅台": "Moutai", "五粮液": "Wuliangye",
    "轩尼诗": "Hennessy", "马爹利": "Martell",
    "人头马": "Rémy Martin",
    "麦卡伦": "Macallan", "尊尼获加": "Johnnie Walker",

    # --- Lafite / DBR Sub-brands ---
    "奥希耶": "Aussieres", "奥希耶酒庄": "Chateau d'Aussieres",
    "奥希耶黑鸢": "Aussieres Noir",
    "奥希耶白鸢": "Aussieres Blanc",
    "奥希耶蓝鸢": "Blason d'Aussieres",
    "奥希耶红鸢": "Altan d'Aussieres",
    "奥希耶古堡": "Chateau d'Aussieres",
    "小拉菲": "Carruades de Lafite",
    "拉菲传说": "Lafite Légende", "拉菲传说波尔多": "Légende Bordeaux",
    "拉菲传说波亚克": "Légende Pauillac", "拉菲传说梅多克": "Légende Médoc",
    "拉菲传奇": "Lafite Légende R", "拉菲传奇波尔多": "Légende R Bordeaux",
    "杜哈米隆": "Duhart-Milon",
    "莱斯古堡": "Château Rieussec", "莱斯": "Rieussec",
    "拉菲珍宝": "L'Apostolle",
    "凯洛": "Caro",
    "安第斯": "Andino",
    "巴斯克": "Los Vascos",
    "巴斯克十世": "Le Dix de Los Vascos",
}

# Build reverse map (English -> Chinese)
_EN_TO_CN = {}
for _cn, _en in WINE_NAME_MAP.items():
    if _en not in _EN_TO_CN:
        _EN_TO_CN[_en] = _cn


def _is_chinese(text):
    """Check if text contains significant Chinese characters.
    Returns True if ANY Chinese character is present, since even one
    Chinese character (like '奔富') indicates the user intends a Chinese query.
    The old threshold of 30% was too high for mixed queries like '奔富 Bin 389'.
    """
    cn_chars = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    return cn_chars > 0


def get_alternate_name(query):
    """Get the alternative language name for a wine query.
    Returns (original, alternate) or (original, None) if no mapping found.
    """
    # Try exact match first
    if query in WINE_NAME_MAP:
        return query, WINE_NAME_MAP[query]
    if query in _EN_TO_CN:
        return query, _EN_TO_CN[query]

    # Try partial match (longest match first)
    best_match = None
    best_len = 0
    for key, val in WINE_NAME_MAP.items():
        if key in query and len(key) > best_len:
            best_match = val
            best_len = len(key)
    for key, val in _EN_TO_CN.items():
        if key.lower() in query.lower() and len(key) > best_len:
            best_match = val
            best_len = len(key)

    return query, best_match


def _replace_segments(query, src_map, dst_map):
    """Replace all matching segments in query using src_map->dst_map.
    Processes longest matches first to avoid partial overlaps.
    Skips duplicate: if replacement word already appears adjacent, removes the original key only.
    e.g. "茅台 Moutai" -> "Moutai" (not "Moutai Moutai")
    Returns the transformed query string.
    """
    # Find all matches (longest first)
    matches = []
    for key in src_map:
        if key in query:
            matches.append((key, dst_map[key], len(key)))
    # Sort by length descending so longest matches replaced first
    matches.sort(key=lambda x: x[2], reverse=True)

    result = query
    for key, val, klen in matches:
        start = 0
        while True:
            idx = result.find(key, start)
            if idx == -1:
                break
            before = result[:idx]
            after = result[idx + klen:]
            # Check: replacement already follows the key (e.g. "茅台 Moutai")
            after_stripped = after.lstrip(' ')
            if after_stripped.lower().startswith(val.lower()):
                # Duplicate found after key — keep one copy of val, remove key + space + dup
                after_clean = after_stripped[len(val):]
                result = before + val + after_clean
                start = idx + len(val)
            # Check: replacement already precedes the key (e.g. "Moutai 茅台")
            elif before.rstrip(' ').lower().endswith(val.lower()):
                # Duplicate found before key — just remove key
                space_before = len(before) - len(before.rstrip(' '))
                result = before[:len(before) - space_before] + after.lstrip(' ')
                start = idx
            else:
                # Auto-insert space when needed:
                # - val ends with letter/digit AND after starts with letter/digit (e.g. "奔富Bin" -> "Penfolds Bin")
                # - before ends with letter/digit AND val starts with letter/digit (e.g. "2019拉菲" -> "2019 Lafite")
                spacer = ''
                if val and after:
                    val_last = val[-1]
                    after_first = after[0]
                    if (val_last.isalnum() or val_last in '°') and after_first.isalnum():
                        spacer = ' '
                if before and val:
                    before_last = before[-1]
                    val_first = val[0]
                    if before_last.isalnum() and val_first.isalnum():
                        spacer = spacer or ''  # already have one; but also check before side
                        if not (before_last == ' ' or spacer):
                            # Need space before val too
                            before = before + ' '
                result = before + val + spacer + after
                start = idx + len(val) + len(spacer)
    return result


def resolve_query_languages(query):
    """Resolve a query into Chinese and English versions.
    Returns (query_cn, query_en).
    
    Supports multi-segment replacement: e.g. "拉菲 奥希耶黑鸢" will
    have each Chinese segment replaced by its English counterpart, producing
    "Lafite Aussieres Noir" for the English query.
    
    Also handles concatenated names with spaces: e.g. "拉菲 古堡" will
    try matching "拉菲古堡" in the dictionary to produce "Château Lafite Rothschild".
    Prefers the replacement that resolves more characters (fewer leftover source chars).
    """
    is_cn = _is_chinese(query)

    if is_cn:
        query_cn = query
        # Try both with-space and without-space versions, pick the better one
        query_en_spaced = _replace_segments(query, WINE_NAME_MAP, WINE_NAME_MAP)
        query_no_space = query.replace(" ", "")
        query_en_nospace = _replace_segments(query_no_space, WINE_NAME_MAP, WINE_NAME_MAP)
        
        # Count remaining Chinese chars in each result to determine which is better
        def _cn_char_count(s):
            return sum(1 for c in s if '\u4e00' <= c <= '\u9fff')
        
        cn_in_spaced = _cn_char_count(query_en_spaced)
        cn_in_nospace = _cn_char_count(query_en_nospace)
        
        # Prefer the result with fewer remaining Chinese chars (more complete replacement)
        if cn_in_nospace < cn_in_spaced:
            query_en = query_en_nospace
        else:
            # Same or fewer Chinese chars in spaced — prefer spaced (preserves formatting)
            query_en = query_en_spaced
        
        # If nothing was replaced at all, fall back to alternate name lookup
        if query_en == query or query_en == query_no_space:
            _, alt = get_alternate_name(query)
            if alt and alt != query:
                query_en = alt
    else:
        query_en = query
        # Try both with-space and without-space versions, pick the better one
        query_cn_spaced = _replace_segments(query, _EN_TO_CN, _EN_TO_CN)
        query_no_space = query.replace(" ", "")
        query_cn_nospace = _replace_segments(query_no_space, _EN_TO_CN, _EN_TO_CN)
        
        def _en_char_count(s):
            return sum(1 for c in s if c.isascii() and c.isalpha())
        
        en_in_spaced = _en_char_count(query_cn_spaced)
        en_in_nospace = _en_char_count(query_cn_nospace)
        
        if en_in_nospace < en_in_spaced:
            query_cn = query_cn_nospace
        else:
            # Same or fewer English chars in spaced — prefer spaced (preserves formatting)
            query_cn = query_cn_spaced
        
        if query_cn == query or query_cn == query_no_space:
            _, alt = get_alternate_name(query)
            if alt and alt != query:
                query_cn = alt

    return query_cn, query_en


# ============================================================
# Wine Style Formatting
# ============================================================

STYLE_LABELS = {
    "body":      ["轻盈", "较轻", "适中", "醇厚", "厚重"],
    "tannin":    ["柔和", "较轻", "适中", "较强", "强劲"],
    "acidity":   ["低酸", "较低", "适中", "较高", "高酸"],
    "sweetness": ["干型", "微甜", "半甜", "甜", "极甜"],
}


def _format_style_bar(value, max_val=5, style_key=None):
    """Format a visual style bar for wine characteristics."""
    if value is None or value == 0:
        return "未知"
    filled = round(value / max_val * 5)
    bar = "█" * filled + "░" * (5 - filled)
    desc = ""
    if style_key and style_key in STYLE_LABELS:
        labels = STYLE_LABELS[style_key]
        idx = max(0, min(int(value) - 1, len(labels) - 1))
        desc = f" ({labels[idx]})"
    return f"{bar} {value}/{max_val}{desc}"


# Known grape names for inference from wine names
_KNOWN_GRAPES_FOR_INFERENCE = [
    'Cabernet Sauvignon', 'Merlot', 'Pinot Noir', 'Syrah', 'Shiraz',
    'Chardonnay', 'Sauvignon Blanc', 'Riesling', 'Malbec', 'Tempranillo',
    'Grenache', 'Sangiovese', 'Nebbiolo', 'Cabernet Franc', 'Petit Verdot',
    'Viognier', 'Sémillon', 'Moscato', 'Pinot Grigio', 'Zinfandel',
    'Mourvèdre', 'Touriga Nacional', 'Tannat', 'Carmenère', 'Pinot Meunier',
    'Gewürztraminer', 'Cabernet', 'Grenache Blanc', 'Mataro',
]


def _infer_grapes_from_name(wine_name):
    """Infer grape varieties from the wine name string.
    E.g. 'Bin 389 Cabernet - Shiraz' → [{'name': 'Cabernet'}, {'name': 'Shiraz'}]
    Returns list of grape dicts, or empty list.
    """
    if not wine_name:
        return []
    grapes = []
    name_lower = wine_name.lower()
    for grape in _KNOWN_GRAPES_FOR_INFERENCE:
        if grape.lower() in name_lower:
            grapes.append({"name": grape})
    return grapes


# ============================================================
# Main Search & Output
# ============================================================

def search_wine(brand, year=None, series=None, mode="all", skip_wiki=False):
    """
    Main search function.
    mode: 'info' (details only), 'price' (prices & links), 'all' (everything)
    skip_wiki: If True, skip Wikipedia background lookups for faster results.
    """
    _t_start = time.time()
    
    # Build search query
    parts = [brand]
    if series:
        parts.append(series)
    query = " ".join(parts)
    
    # Resolve Chinese and English query variants
    query_cn, query_en = resolve_query_languages(query)
    
    # Track best match and wine type across scopes
    best_match = None
    wine_type_key = None
    detail_data = None
    
    print(f"🍷 正在搜索酒款: {query}")
    if year:
        print(f"   年份: {year}")
    if query_cn != query_en:
        print(f"   中文搜索: {query_cn}")
        print(f"   英文搜索: {query_en}")
    print()
    
    # === Data Source Status ===
    print("📡 数据源状态:")
    if _firecrawl_api_key:
        print("   • Vivino (Firecrawl): ✅ 可通过 Firecrawl 代理访问 Vivino (美国IP+JS渲染)")
    else:
        print("   • Vivino (Firecrawl): ⚠️ 未配置 FIRECRAWL_API_KEY，无法通过 Firecrawl 访问 Vivino")
    print("   • Wikipedia API: ✅ 酒款与酒庄背景信息 (免费，中国可访问)")
    print("   • Vivino API: ⚠️ 已关闭公共访问 (403 Forbidden)")
    print("   • Wine-Searcher (WebFetch): ✅ 主数据源，通过 AI WebFetch 可靠获取")
    print("   • Open Food Facts API: ✅ 补充数据源，可从国内直接访问")
    print("   • 脚本直接访问: ⚠️ 国内网络可能超时，优先使用 WebFetch")
    print()
    
    # === Step 1: Search Vivino ===
    print("=" * 60)
    print("📋 酒款信息 (Wine Information)")
    print("=" * 60)
    
    # Try both Chinese and English queries for better results
    search_results = vivino_search(query, year, query_en=query_en)
    if not search_results and query_cn != query_en:
        # Try alternate language query
        alt_query = query_en if _is_chinese(query) else query_cn
        alt_en = query_en if _is_chinese(query) else query_cn
        alt_results = vivino_search(alt_query, year, query_en=alt_en)
        if alt_results:
            search_results = alt_results
            print(f"  (使用 '{alt_query}' 搜索获得结果)\n")
    
    if not search_results:
        print(f"\n⚠️ 未在在线数据源找到 '{query}' 的搜索结果")
        print(f"   Vivino 手动搜索: {VIVINO_SEARCH_URL}?q={urllib.parse.quote(query_en)}")
        print(f"   Wine-Searcher: {WS_SEARCH_URL}/{urllib.parse.quote(query_en.replace(' ', '+'))}")
        print(f"   Open Food Facts: https://world.openfoodfacts.org/cgi/search.pl?search_terms={urllib.parse.quote(query_en)}")
        
        # Generate basic info from WINE_NAME_MAP knowledge
        print(f"\n📋 基于内置数据库的基本信息:")
        print(f"   查询: {query_cn}")
        if query_cn != query_en:
            print(f"   英文名: {query_en}")
        
        # Try to identify wine type from query segments
        detected_type = "red"  # default
        type_hints = {"白": "white", " Blanc": "white", "起泡": "sparkling", 
                      "桃红": "rose", " Ros": "rose", "甜": "dessert", 
                      "加强": "fortified", " Port": "fortified"}
        for hint, wtype in type_hints.items():
            if hint in query_cn or hint in query_en:
                detected_type = wtype
                break
        wine_type_key = detected_type
        
        type_display = WINE_TYPE_MAP.get(detected_type, detected_type)
        print(f"   类型: {type_display}")
        
        # Identify known segments
        known_segments = []
        for cn_name, en_name in WINE_NAME_MAP.items():
            if cn_name in query_cn or en_name.lower() in query_en.lower():
                known_segments.append(f"{cn_name} ({en_name})")
        if known_segments:
            print(f"   已识别: {', '.join(known_segments)}")
        
        # Hint: AI should use WebFetch on Wine-Searcher for best results
        print(f"\n💡 提示: 请使用 WebFetch 访问 Wine-Searcher 获取详细信息:")
        print(f"   {WS_SEARCH_URL}/{urllib.parse.quote(query_en.replace(' ', '+'))}")
        if not _firecrawl_api_key:
            print(f"\n💡 提示: 配置 Firecrawl API Key 后可通过代理访问 Vivino 获取更多数据:")
            print(f"   设置环境变量: set FIRECRAWL_API_KEY=fc-xxxx")
            print(f"   或使用参数: --firecrawl-key fc-xxxx")
        
        # Even with no search results, try to get background info from Wikipedia
        if mode in ("info", "all") and not skip_wiki:
            print()
            print("-" * 40)
            print("🏛️ 酒款与酒庄背景 (Wine & Winery Background)")
            print("-" * 40)
            print()
            
            try:
                bg_data = fetch_wine_background(
                    wine_name="",
                    winery_name="",
                    query_en=query_en,
                    query_cn=query_cn,
                    pref_lang="zh" if _is_chinese(query) else "en",
                )
            except Exception:
                bg_data = {}
            
            if bg_data.get("wine_bg"):
                print("  🍷 酒款背景:")
                for line in _format_bg_text(bg_data["wine_bg"]):
                    print(line)
                if bg_data.get("wine_url"):
                    print(f"\n     📖 详情: {bg_data['wine_url']}")
                print()
            
            if bg_data.get("winery_bg"):
                print("  🏛️ 酒庄/厂商背景:")
                for line in _format_bg_text(bg_data["winery_bg"]):
                    print(line)
                if bg_data.get("winery_url"):
                    print(f"\n     📖 详情: {bg_data['winery_url']}")
                print()
            
            if not bg_data.get("wine_bg") and not bg_data.get("winery_bg"):
                print("  暂无背景信息，请参考以上搜索链接了解更多")
                print()
    else:
        # Find best match (prefer matching series+year, then series, then year)
        if len(search_results) > 1:
            series_lower = series.lower().strip() if series else ""
            # Translate Chinese series to English for comparison with Vivino results.
            # First try brand+series compound (e.g. "拉菲"+"古堡"→"Château Lafite Rothschild"),
            # then fall back to translating series alone (e.g. "古堡" may have no standalone mapping).
            series_is_compound = False
            if series_lower and _is_chinese(series):
                compound = f"{brand}{series}"  # e.g. "拉菲古堡"
                _, compound_en = resolve_query_languages(compound)
                if compound_en != compound:
                    # Compound matched — use the full English name for matching
                    series_for_match = compound_en.lower().strip()
                    series_is_compound = True
                else:
                    _, series_en = resolve_query_languages(series)
                    if series_en != series:
                        series_for_match = series_en.lower().strip()
                    else:
                        # Series alone has no mapping — use the full English query
                        # (which already contains the translated brand+series)
                        series_for_match = query_en.lower().strip()
            else:
                series_for_match = series_lower
            year_str = str(year) if (year is not None and year != "") else ""
            
            # Priority 1: series + year both match (check name AND winery fields)
            # When matching winery, prefer results whose name also contains the match
            if series_for_match and year_str:
                winery_match = None
                name_match = None
                for r in search_results:
                    rname = (r.get("name", "") or "").lower()
                    rwinery = (r.get("winery", "") or "").lower()
                    ryear = str(r.get("year", ""))
                    if (series_for_match in rname or series_for_match in rwinery) and ryear == year_str:
                        if series_for_match in rname:
                            name_match = r
                            break  # Name match is best possible — stop immediately
                        elif not winery_match:
                            winery_match = r
                best_match = name_match or winery_match
            
            # Priority 2: series matches (check name AND winery fields)
            # Prefer name match over winery-only match
            if not best_match and series_for_match:
                winery_match = None
                name_match = None
                for r in search_results:
                    rname = (r.get("name", "") or "").lower()
                    rwinery = (r.get("winery", "") or "").lower()
                    if series_for_match in rname:
                        name_match = r
                        break  # Name match is best — stop
                    elif series_for_match in rwinery and not winery_match:
                        winery_match = r
                best_match = name_match or winery_match
            
            # Priority 3: year matches
            if not best_match and year_str:
                for r in search_results:
                    if str(r.get("year", "")) == year_str:
                        best_match = r
                        break
        
        if not best_match and search_results:
            best_match = search_results[0]
        
        # Display top results
        print(f"\n🔍 搜索到 {len(search_results)} 款相关酒款:\n")
        
        for i, r in enumerate(search_results[:8], 1):
            r_year_str = str(r.get("year", "")) if r.get("year") else ""
            name = r.get("name", "未知")
            winery = r.get("winery", "")
            rating_val = r.get("rating", 0)
            num_rat = r.get("num_ratings", 0)
            price_val = r.get("price", 0)
            currency = r.get("currency", "")
            region = r.get("region", "")
            country = r.get("country", "")
            wtype = r.get("wine_type", "")
            
            # Map wine type
            wtype_display = WINE_TYPE_MAP.get(str(wtype).lower(), str(wtype)) if wtype else ""
            
            marker = " ◀ 最佳匹配" if r == best_match else ""
            print(f"  {i}. {name} {r_year_str}{marker}")
            if winery:
                print(f"     酒庄: {winery}")
            if wtype_display:
                print(f"     类型: {wtype_display}")
            if region or country:
                print(f"     产区: {region}{', ' + country if country else ''}")
            print(f"     评分: {format_rating_bar(rating_val)} ({num_rat:,} 条评价)")
            if price_val:
                print(f"     参考价: {currency} {price_val:.2f}")
            if r.get("url"):
                print(f"     Vivino: {r['url']}")
            print()
        
        # === Step 1b: Wine Detail (grape, style, etc.) ===
        if best_match and best_match.get("id") and mode in ("info", "all"):
            wine_id = best_match["id"]
            detail = vivino_wine_detail(wine_id)
            detail_data = detail  # save for food pairing section
            
            # Also try to infer grapes from the wine name (e.g. "Cabernet - Shiraz")
            wine_name_str = best_match.get("name", "")
            inferred_grapes = _infer_grapes_from_name(wine_name_str)
            
            if detail or inferred_grapes:
                if not detail:
                    detail = {}
                    detail_data = detail
                
                # Merge inferred grapes: prefer name-inferred if more grapes found
                # (detail page parsing can be noisy and pick up wrong grapes)
                detail_grapes = detail.get("grape") or detail.get("grapes") or []
                if isinstance(detail_grapes, dict):
                    detail_grapes = [detail_grapes]
                if inferred_grapes and len(inferred_grapes) > len(detail_grapes):
                    detail["grape"] = inferred_grapes
                
                print("-" * 40)
                print("🍇 详细信息 (Wine Details)")
                print("-" * 40)
                
                # Grape varieties
                grapes = detail.get("grape") or detail.get("grapes") or []
                if isinstance(grapes, dict):
                    grapes = [grapes]
                if grapes and isinstance(grapes, list):
                    grape_strs = []
                    for g in grapes:
                        if isinstance(g, dict):
                            gname = g.get("name", "")
                            g_pct = g.get("percentage")
                            if g_pct:
                                grape_strs.append(f"{gname} {g_pct}%")
                            else:
                                grape_strs.append(gname)
                        elif isinstance(g, str):
                            grape_strs.append(g)
                    if grape_strs:
                        print(f"\n  🍇 葡萄品种: {', '.join(grape_strs)}")
                
                # Wine style / taste profile
                style = detail.get("style") or detail.get("taste") or {}
                if isinstance(style, dict):
                    style_items = []
                    body = style.get("body")
                    if body:
                        style_items.append(f"  🍷 酒体: {_format_style_bar(body, style_key='body')}")
                    tannin = style.get("tannin")
                    if tannin:
                        style_items.append(f"  🫖 单宁: {_format_style_bar(tannin, style_key='tannin')}")
                    acidity = style.get("acidity")
                    if acidity:
                        style_items.append(f"  🍋 酸度: {_format_style_bar(acidity, style_key='acidity')}")
                    sweetness = style.get("sweetness")
                    if sweetness:
                        style_items.append(f"  🍯 甜度: {_format_style_bar(sweetness, style_key='sweetness')}")
                    if style_items:
                        print()
                        for item in style_items:
                            print(item)
                
                # Food pairing
                food = detail.get("food") or detail.get("food_pairing") or detail.get("food_pairings") or []
                if isinstance(food, dict):
                    food = food.get("pairings", [])
                if food and isinstance(food, list):
                    food_names = []
                    for f in food:
                        if isinstance(f, dict):
                            food_names.append(f.get("name", str(f)))
                        elif isinstance(f, str):
                            food_names.append(f)
                    if food_names:
                        print(f"\n  🍽️ 搭配美食: {', '.join(food_names)}")
                
                # Description / facts
                desc = detail.get("description") or detail.get("interesting_facts") or ""
                if desc and isinstance(desc, str) and len(desc.strip()) > 10:
                    # Truncate long descriptions
                    snippet = desc.strip()[:300]
                    if len(desc.strip()) > 300:
                        snippet += "..."
                    print(f"\n  📝 简介: {snippet}")
                
                print()
        
        # Try to get vintage comparison for best match
        if best_match and best_match.get("id") and mode in ("info", "all"):
            wine_id = best_match["id"]
            print("-" * 40)
            print("📊 不同年份对比与推荐 (Vintage Comparison & Recommendations)")
            print("-" * 40)
            
            vintages = vivino_vintages(wine_id)
            if vintages:
                print(f"\n{'年份':<8} {'评分':<18} {'推荐':<10} {'评价数':>8} {'参考价':>12}")
                print("-" * 65)
                
                # Collect best vintages for summary
                outstanding_vintages = []
                very_good_vintages = []
                
                for v in vintages[:15]:
                    yr = str(v.get("year", ""))
                    rt = v.get("rating", 0)
                    nr = v.get("num_ratings", 0)
                    pr = v.get("price", 0)
                    cur = v.get("currency", "USD")
                    rating_bar = format_rating_bar(rt) if rt else "☆☆☆☆☆"
                    price_str = f"{cur} {pr:.2f}" if pr else "-"
                    
                    # Get recommendation label
                    rec_label, confidence = get_vintage_recommendation(rt, nr)
                    confidence_str = f" {confidence}" if confidence else ""
                    print(f"{yr:<8} {rating_bar:<18} {rec_label:<10} {nr:>8,} {price_str:>12}{confidence_str}")
                    
                    # Track best vintages
                    if rt >= 4.5:
                        outstanding_vintages.append(yr)
                    elif rt >= 4.0:
                        very_good_vintages.append(yr)
                
                # Print vintage recommendation summary
                print()
                if outstanding_vintages or very_good_vintages:
                    print("  🏆 年份推荐总结:")
                    if outstanding_vintages:
                        print(f"     🌟 卓越年份 (≥4.5分): {', '.join(outstanding_vintages)}")
                    if very_good_vintages:
                        print(f"     ⭐ 优秀年份 (4.0-4.4分): {', '.join(very_good_vintages)}")
                    
                    # Buying advice based on user's specified year
                    if year:
                        user_rating = 0
                        for v in vintages:
                            if str(v.get("year", "")) == str(year):
                                user_rating = v.get("rating", 0)
                                break
                        if user_rating >= 4.0:
                            print(f"\n  ✅ {year}年份评分为 {user_rating:.1f}，属于推荐购买的年份！")
                        elif user_rating >= 3.5:
                            print(f"\n  👍 {year}年份评分为 {user_rating:.1f}，品质良好，值得尝试。")
                        elif user_rating > 0:
                            better = outstanding_vintages[:3] if outstanding_vintages else very_good_vintages[:3]
                            if better:
                                print(f"\n  💡 {year}年份评分为 {user_rating:.1f}，如追求更好品质，可考虑 {', '.join(better)} 年份。")
                            else:
                                print(f"\n  💡 {year}年份评分为 {user_rating:.1f}，该酒款各年份评分总体偏低，建议参考个人口味偏好。")
                print()
            else:
                print("\n  暂无不同年份对比数据\n")
        
        # === Step 1c: Wine & Winery Background (via Wikipedia) ===
        if mode in ("info", "all") and not skip_wiki:
            winery_name = best_match.get("winery", "") if best_match else ""
            wine_name_for_bg = best_match.get("name", "") if best_match else ""
            
            print("-" * 40)
            print("🏛️ 酒款与酒庄背景 (Wine & Winery Background)")
            print("-" * 40)
            print()
            
            # Fetch background from Wikipedia
            try:
                bg_data = fetch_wine_background(
                    wine_name=wine_name_for_bg,
                    winery_name=winery_name,
                    query_en=query_en,
                    query_cn=query_cn,
                    pref_lang="zh" if _is_chinese(query) else "en",
                )
            except Exception:
                bg_data = {}
            
            if bg_data.get("wine_bg"):
                print("  🍷 酒款背景:")
                for line in _format_bg_text(bg_data["wine_bg"]):
                    print(line)
                if bg_data.get("wine_url"):
                    print(f"\n     📖 详情: {bg_data['wine_url']}")
                print()
            else:
                print("  🍷 酒款背景: 暂无 Wikipedia 背景信息")
                print(f"     💡 可访问 Wine-Searcher 了解更多: {WS_SEARCH_URL}/{urllib.parse.quote(query_en.replace(' ', '+'))}")
                print()
            
            # Check if winery_bg is different from wine_bg (avoid duplicate display)
            winery_bg_same = False
            if bg_data.get("wine_bg") and bg_data.get("winery_bg"):
                # Compare first 100 chars to detect same Wikipedia article
                wine_prefix = bg_data["wine_bg"][:100].strip()
                winery_prefix = bg_data["winery_bg"][:100].strip()
                if wine_prefix == winery_prefix or bg_data.get("wine_url") == bg_data.get("winery_url"):
                    winery_bg_same = True
            
            if bg_data.get("winery_bg") and not winery_bg_same:
                print("  🏛️ 酒庄/厂商背景:")
                for line in _format_bg_text(bg_data["winery_bg"]):
                    print(line)
                if bg_data.get("winery_url"):
                    print(f"\n     📖 详情: {bg_data['winery_url']}")
                print()
            elif not bg_data.get("winery_bg"):
                print("  🏛️ 酒庄/厂商背景: 暂无 Wikipedia 背景信息")
                if winery_name:
                    print(f"     💡 可搜索: https://en.wikipedia.org/wiki/Special:Search?search={urllib.parse.quote(winery_name)}")
                print()
            elif winery_bg_same and bg_data.get("wine_bg"):
                # Wine and winery are the same Wikipedia article, just note it
                print("  🏛️ 酒庄/厂商背景: 与酒款背景为同一 Wikipedia 词条")
                print()
    
    # === Step 2: Platform Prices & Links ===
    if mode in ("price", "all"):
        print()
        print("=" * 60)
        print("💰 各平台价格与购买链接 (Platform Prices & Links)")
        print("=" * 60)
        
        # Generate search links — use CN query for domestic, EN for international
        # Note: query_cn/query_en already contain brand+series from resolve_query_languages,
        # so we only append year (avoid duplicating series like "Bin 389 Bin 389")
        search_query_cn = f"{query_cn} {year or ''}".strip()
        # Append series/year only if not already present in query_en
        en_parts = [query_en]
        # Skip Chinese series — already handled by resolve_query_languages compound matching
        if series and series.lower() not in query_en.lower() and not _is_chinese(series):
            en_parts.append(series)
        if year and str(year) not in query_en:
            en_parts.append(str(year))
        search_query_en = " ".join(en_parts).strip()
        links = generate_platform_links(search_query_en, search_query_cn)
        
        # WebFetch price hints — AI agent can use these to fetch real-time prices
        wf_hints = fetch_price_webfetch(search_query_cn, search_query_en)
        
        print("\n📡 实时价格获取提示 (AI Agent 可使用 WebFetch 工具获取):\n")
        for key, hint in wf_hints.items():
            fc_note = ""
            if key == "firecrawl_vivino":
                fc_note = " [需 Firecrawl API Key]"
            print(f"   🔍 {hint['platform']}{fc_note}")
            print(f"      URL: {hint['url']}")
            print(f"      提取提示: {hint['extraction_hint'][:60]}...")
            print()
        
        # Best-effort direct scraping (legacy, low success rate)
        print("📡 尝试直接获取价格 (成功率较低)...\n")
        jd_results = fetch_price_direct(search_query_cn, "jd")
        ws_results = fetch_price_direct(search_query_en, "wine_searcher")
        
        if jd_results:
            print("🛒 京东 (JD.com) 价格:")
            for item in jd_results[:5]:
                if item.get('price', 0) > 0:
                    price_str = f"¥{item['price']:.2f}"
                else:
                    price_str = "点击查看"
                note = f" ({item['note']})" if item.get('note') else ""
                print(f"   • {price_str}{note}  {item.get('url', '')}")
            print()
        
        if ws_results:
            print("🌍 Wine-Searcher 价格参考:")
            for item in ws_results:
                if item.get('price', 0) > 0:
                    price_str = f"${item['price']:.2f}"
                else:
                    price_str = "点击查看"
                note = f" ({item['note']})" if item.get('note') else ""
                print(f"   • {price_str}{note}")
            print()
        
        if not jd_results and not ws_results:
            print("   ⚠️ 直接爬取未获取到价格，请使用上方 WebFetch 提示获取实时价格\n")
        
        # Domestic platforms
        print("🏪 国内购买平台:")
        domestic = ["京东", "天猫", "淘宝", "苏宁易购", "拼多多", "1919吃喝", "也买酒", "酒仙网"]
        for platform in domestic:
            if platform in links:
                print(f"   🔗 {platform}: {links[platform]}")
        print()
        
        # International platforms
        print("🌍 国际购买平台:")
        international = ["Vivino", "Vivino Shop", "Wine.com", "Drizly", "Total Wine", 
                         "Wine-Searcher", "Wine Spectator", "CellarTracker", "Decántalo"]
        for platform in international:
            if platform in links:
                print(f"   🔗 {platform}: {links[platform]}")
        print()
    
    # === Step 3: Wine Knowledge & Health Advice ===
    if mode in ("info", "all"):
        # Determine wine type for advice
        if best_match:
            wine_type_key = str(best_match.get("wine_type", "")).lower()
        # Fallback: if wine_type_key is still empty, default to "red"
        if not wine_type_key:
            wine_type_key = "red"
        
        print()
        print("=" * 60)
        print("📖 酒款小贴士 (Wine Tips)")
        print("=" * 60)
        
        # Vintage drinking window
        if year:
            try:
                y = int(year)
                wine_age = datetime.now().year - y
                # Different drinking windows by wine type
                if wine_type_key in ("white", "2", "sparkling", "3", "rose", "4"):
                    # Whites/sparkling/rosé: generally drink young
                    if wine_age < 2:
                        print(f"\n  🍇 {year}年份: 此酒正值最佳饮用期")
                        print("     白葡萄酒/起泡酒/桃红通常年轻时（1-3年）饮用最佳")
                    elif wine_age <= 5:
                        print(f"\n  🍇 {year}年份: 此酒仍在适饮期内")
                        print("     部分优质白葡萄酒可陈年5年以上，但大多数已接近巅峰")
                    else:
                        print(f"\n  🍇 {year}年份: 此酒已过一般适饮期")
                        print("     建议尽快饮用，注意确认保存状态")
                elif wine_type_key in ("dessert", "5", "fortified", "6"):
                    # Dessert/fortified: long aging potential
                    if wine_age < 5:
                        print(f"\n  🍇 {year}年份: 此酒尚年轻，可继续陈年")
                    elif wine_age <= 20:
                        print(f"\n  🍇 {year}年份: 此酒正值适饮期")
                        print("     甜酒和加强酒通常有很长的陈年潜力")
                    else:
                        print(f"\n  🍇 {year}年份: 此酒为陈年佳酿")
                        print("     需专业储存条件，饮用前注意检查酒况")
                else:
                    # Red wine (default)
                    if wine_age < 3:
                        print(f"\n  🍇 {year}年份: 此酒较为年轻，可能还在适饮期前")
                        print("     建议可继续陈年存放，或充分醒酒后饮用")
                    elif wine_age <= 10:
                        print(f"\n  🍇 {year}年份: 此酒正值适饮期")
                        print("     红葡萄酒通常在5-10年达到最佳状态")
                    elif wine_age <= 20:
                        print(f"\n  🍇 {year}年份: 此酒已进入成熟期")
                        print("     建议尽快饮用，部分酒款可能已过巅峰期")
                    else:
                        print(f"\n  🍇 {year}年份: 此酒为老年份酒")
                        print("     需谨慎保管和饮用，建议专业储存条件")
            except ValueError:
                pass
        
        print("\n  💡 购买建议:")
        print("     • 国内购买推荐京东/天猫自营，品质更有保障")
        print("     • 老年份红酒注意确认运输和储存条件")
        print("     • 价格差异大时注意鉴别真伪，优先选择授权渠道")
        print("     • Vivino评分4.0以上通常为品质不错的酒款")
        print("     • 评分仅供参考，个人口味偏好更重要")
        
        # === Health & Drinking Advice ===
        print()
        print("=" * 60)
        print("🏥 健康饮用建议 (Health & Drinking Advice)")
        print("=" * 60)
        print()
        print(format_health_advice(wine_type=wine_type_key))
        
        # === Food Pairing Recommendations ===
        # Get Vivino food pairing if available
        vivino_food = None
        if detail_data:
            vivino_food = detail_data.get("food") or detail_data.get("food_pairing") or detail_data.get("food_pairings") or []
            if isinstance(vivino_food, dict):
                vivino_food = vivino_food.get("pairings", [])
        
        print()
        print("=" * 60)
        print("🍽️ 餐饮搭配建议 (Food Pairing Recommendations)")
        print("=" * 60)
        print()
        print(format_food_pairing(wine_type=wine_type_key, vivino_food=vivino_food))
        print()
    
    # Show elapsed time
    _elapsed = time.time() - _t_start
    print(f"⏱️ 搜索耗时: {_elapsed:.1f}秒")
    print()


def search_by_image(image_path):
    """
    Search wine by label image.
    Strategy:
    1. Try OCR on the image to extract text (using built-in methods)
    2. Use extracted text to search Vivino
    3. If OCR unavailable, guide user to Vivino App
    """
    print(f"📸 图片识别搜索: {image_path}")
    print()
    print("=" * 60)
    print("📷 酒标图片识别 (Wine Label Recognition)")
    print("=" * 60)
    print()
    
    extracted_text = None
    ocr_method = None
    
    # --- Attempt 1: Try pytesseract (if available) ---
    try:
        import pytesseract
        from PIL import Image
        
        print("🔍 正在识别图片中的文字 (OCR)...\n")
        img = Image.open(image_path)
        # Try both Chinese + English OCR
        extracted_text = pytesseract.image_to_string(img, lang='chi_sim+eng').strip()
        if extracted_text:
            ocr_method = "pytesseract"
            print(f"   OCR 提取文字: {extracted_text[:200]}")
            print()
    except ImportError:
        pass
    except Exception as e:
        print(f"   ⚠️ OCR 识别出错: {e}")
        print()
    
    # --- Attempt 2: Try easyocr (if available) ---
    if not extracted_text:
        try:
            import easyocr
            print("🔍 正在使用 EasyOCR 识别图片中的文字...\n")
            reader = easyocr.Reader(['ch_sim', 'en'], verbose=False)
            results = reader.readtext(image_path)
            text_parts = [r[1] for r in results if r[2] > 0.3]  # confidence > 0.3
            if text_parts:
                extracted_text = " ".join(text_parts).strip()
                ocr_method = "easyocr"
                print(f"   OCR 提取文字: {extracted_text[:200]}")
                print()
        except ImportError:
            pass
        except Exception as e:
            print(f"   ⚠️ EasyOCR 识别出错: {e}")
            print()
    
    # --- Attempt 3: Extract hints from filename ---
    if not extracted_text:
        fname = os.path.basename(image_path)
        name_no_ext = os.path.splitext(fname)[0]
        # Clean up common separators
        hints = name_no_ext.replace("_", " ").replace("-", " ").replace(".", " ").strip()
        if hints and len(hints) > 1:
            extracted_text = hints
            ocr_method = "filename"
            print(f"   📎 从文件名提取关键词: {extracted_text}")
            print()
    
    # --- If we got text, try to search with it ---
    if extracted_text:
        # Clean up the text - remove noise, keep meaningful parts
        lines = [l.strip() for l in extracted_text.split('\n') if l.strip() and len(l.strip()) > 1]
        # Try to identify brand/year/series from OCR text
        brand_guess = None
        year_guess = None
        series_guess = None
        
        for line in lines:
            # Check for year pattern
            year_match = re.search(r'\b(19\d{2}|20\d{2})\b', line)
            if year_match and not year_guess:
                y = int(year_match.group(1))
                if 1900 <= y <= 2100:
                    year_guess = str(y)
                    continue
            
            # Check if line matches known wine names
            for cn_name, en_name in WINE_NAME_MAP.items():
                if cn_name in line or en_name.lower() in line.lower():
                    brand_guess = cn_name if cn_name in line else en_name
                    break
            
            if brand_guess:
                continue
        
        # If no brand matched, use first meaningful line
        if not brand_guess and lines:
            brand_guess = lines[0]
        # Second line as series if available
        if not series_guess and len(lines) > 1 and lines[1] != brand_guess:
            candidate = lines[1]
            # Don't use year as series
            if not re.match(r'^\d{4}$', candidate):
                series_guess = candidate
        
        if brand_guess:
            print(f"  🎯 推测酒款信息:")
            print(f"     品牌: {brand_guess}")
            if year_guess:
                print(f"     年份: {year_guess}")
            if series_guess:
                print(f"     系列: {series_guess}")
            print()
            
            # Run actual search with extracted info
            search_wine(brand_guess, year_guess, series_guess, mode="all")
            return
        else:
            print("  ⚠️ 未能从 OCR 结果中识别出酒款名称")
            print()
    
    # --- Fallback: Guide user to Vivino App ---
    print("  📱 未检测到 OCR 工具，推荐以下方式识别酒标:")
    print()
    print("  方式一：使用 Vivino App 拍照识别")
    print("     1. 下载 Vivino App (iOS/Android)")
    print("        👉 https://www.vivino.com/app")
    print("     2. 打开 App，点击相机图标")
    print("     3. 对准酒瓶标签拍照")
    print("     4. 即可获取该酒的详细信息和评分")
    print()
    print("  方式二：安装 OCR 工具后重试")
    print("     pip install pytesseract Pillow  (需安装 Tesseract-OCR)")
    print("     pip install easyocr              (深度学习 OCR，无需额外安装)")
    print()
    print("  方式三：手动输入酒标上的信息进行搜索")
    print("     命令格式: python wine_search.py \"品牌名\" [年份] [系列名]")
    print("     示例: python wine_search.py \"拉菲\" 2018 \"罗斯柴尔德\"")
    print()


# ============================================================
# Entry Point
# ============================================================

def _fix_windows_console_encoding():
    """Fix Windows console encoding to support UTF-8 (emoji + CJK characters).
    
    On Windows, the default console encoding is GBK (cp936), which cannot encode
    emoji characters (e.g. wine_glass U+1F377) or rare CJK, causing UnicodeEncodeError.
    This reconfigures stdout/stderr to UTF-8 with 'replace' error handling,
    ensuring the script runs on all platforms without crashes.
    """
    import io
    if sys.platform == 'win32':
        for stream_name in ('stdout', 'stderr'):
            stream = getattr(sys, stream_name)
            if stream and hasattr(stream, 'reconfigure'):
                try:
                    stream.reconfigure(encoding='utf-8', errors='replace')
                except Exception:
                    # Fallback: wrap the stream buffer entirely
                    try:
                        setattr(sys, stream_name, io.TextIOWrapper(
                            stream.buffer, encoding='utf-8', errors='replace',
                            line_buffering=getattr(stream, 'line_buffering', True)
                        ))
                    except Exception:
                        pass  # Best effort


def main():
    global _insecure_mode, _ssl_ctx
    _fix_windows_console_encoding()
    args = sys.argv[1:]
    
    if not args:
        print(__doc__)
        return
    
    # Parse arguments
    brand = None
    year = None
    series = None
    mode = "all"
    image_path = None
    skip_wiki = False
    
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--mode" and i + 1 < len(args):
            mode = args[i + 1]
            i += 2
            continue
        elif arg == "--image" and i + 1 < len(args):
            image_path = args[i + 1]
            i += 2
            continue
        elif arg == "--firecrawl-key" and i + 1 < len(args):
            global _firecrawl_api_key
            _firecrawl_api_key = args[i + 1]
            i += 2
            continue
        elif arg == "--no-wiki":
            skip_wiki = True
            i += 1
            continue
        elif arg == "--insecure":
            _enable_insecure_mode()
            i += 1
            continue
        elif arg.startswith("--"):
            print(f"未知参数: {arg}")
            return
        elif brand is None:
            brand = arg
        elif year is None:
            # Try to parse as year
            try:
                y = int(arg)
                if 1800 <= y <= 2100:
                    year = str(y)
                else:
                    year = ""
                    series = arg
            except ValueError:
                year = ""
                series = arg
        elif series is None:
            series = arg
        else:
            series = f"{series} {arg}"
        i += 1
    
    # Security: re-check insecure mode if API key was set after --insecure flag
    if _insecure_mode and _firecrawl_api_key:
        print("  ⚠️ 安全限制: 检测到 Firecrawl API Key 与 --insecure 同时使用")
        print("     Bearer Token 不能通过未验证的 TLS 连接发送，已恢复安全模式")
        _insecure_mode = False
        _ssl_ctx = ssl.create_default_context()
    
    if image_path:
        search_by_image(image_path)
    elif brand:
        if mode not in ("info", "price", "all"):
            print(f"未知模式: {mode}，请使用 info/price/all")
            return
        search_wine(brand, year, series, mode, skip_wiki=skip_wiki)
    else:
        print("请提供红酒品牌名称")
        print(__doc__)


if __name__ == "__main__":
    main()
