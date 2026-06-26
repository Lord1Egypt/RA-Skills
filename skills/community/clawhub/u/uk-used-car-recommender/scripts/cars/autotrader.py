"""
AutoTrader UK 搜索实现

支持两种方式：
1. 使用 autotrader_scraper 库（推荐）
2. 使用自定义爬虫（备用）
"""

from __future__ import annotations

import json
import re
from typing import Any

# 检查是否安装了 autotrader_scraper
try:
    from autotrader_scraper import AutoTraderScraper
    HAS_AUTOTRADER_SCRAPER = True
except ImportError:
    HAS_AUTOTRADER_SCRAPER = False
    print("⚠️  autotrader_scraper 未安装。安装方式：pip install autotrader_scraper")

# 备用方案：使用 requests + BeautifulSoup
import requests
from bs4 import BeautifulSoup

_DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.9",
}


def build_autotrader_url(
    make: str | None = None,
    model: str | None = None,
    postcode: str | None = None,
    radius: int = 10,
    min_price: int | None = None,
    max_price: int | None = None,
    min_year: int | None = None,
    max_year: int | None = None,
    fuel_type: str | None = None,
    transmission: str | None = None,
    body_type: str | None = None,
    min_mileage: int | None = None,
    max_mileage: int | None = None,
    seller_type: str | None = None,
    sort: str = "relevance",
) -> str:
    """构建 AutoTrader 搜索 URL"""
    base_url = "https://www.autotrader.co.uk/car-search"
    
    params = []
    
    if postcode:
        params.append(f"postcode={postcode}")
    if radius:
        params.append(f"radius={radius}")
    if make:
        params.append(f"make={make.upper()}")
    if model:
        params.append(f"model={model.upper()}")
    if min_price:
        params.append(f"price-from={min_price}")
    if max_price:
        params.append(f"price-to={max_price}")
    if min_year:
        params.append(f"year-from={min_year}")
    if max_year:
        params.append(f"year-to={max_year}")
    if fuel_type:
        # 映射到 AutoTrader 参数
        fuel_map = {
            "petrol": "Petrol",
            "diesel": "Diesel",
            "electric": "Electric",
            "hybrid": "Hybrid"
        }
        params.append(f"fuel-type={fuel_map.get(fuel_type.lower(), fuel_type)}")
    if transmission:
        trans_map = {
            "manual": "Manual",
            "automatic": "Automatic"
        }
        params.append(f"transmission={trans_map.get(transmission.lower(), transmission)}")
    if body_type:
        params.append(f"body-type={body_type}")
    if min_mileage:
        params.append(f"minimum-mileage={min_mileage}")
    if max_mileage:
        params.append(f"maximum-mileage={max_mileage}")
    if seller_type:
        # "dealer" or "private"
        params.append(f"seller-type={seller_type}")
    
    # 排序选项
    sort_map = {
        "relevance": "relevance",
        "price_low": "price-asc",
        "price_high": "price-desc",
        "mileage_low": "mileage-asc",
        "distance": "distance",
        "year_new": "year-desc",
        "year_old": "year-asc"
    }
    params.append(f"sort={sort_map.get(sort, 'relevance')}")
    
    url = base_url + "?" + "&".join(params)
    return url


def search_autotrader_with_library(
    make: str | None = None,
    model: str | None = None,
    postcode: str = "SW1A1AA",  # 默认伦敦
    radius: int = 10,
    max_price: int | None = None,
    min_year: int | None = None,
    max_year: int | None = None,
    limit: int = 10,
) -> dict[str, Any]:
    """使用 autotrader_scraper 库搜索（推荐）"""
    
    if not HAS_AUTOTRADER_SCRAPER:
        return {
            "ok": False,
            "error": "autotrader_scraper 库未安装。请运行：pip install autotrader_scraper",
            "items": [],
            "total": 0,
        }
    
    try:
        scraper = AutoTraderScraper()
        
        results = scraper.search(
            make=make,
            model=model,
            postcode=postcode,
            radius=radius,
            price_to=max_price,
            year_from=min_year,
            year_to=max_year,
        )
        
        # 标准化输出格式（与 Gumtree 保持一致）
        normalized_items = []
        for car in results[:limit]:
            normalized_items.append({
                "listing_id": car.get("id"),
                "title": car.get("title"),
                "price": car.get("price"),
                "price_display": f"£{car.get('price'):,}" if car.get('price') else None,
                "location": car.get("location"),
                "url": car.get("url"),
                "year": car.get("year"),
                "mileage": car.get("mileage"),
                "fuel_type": car.get("fuel_type"),
                "transmission": car.get("transmission"),
                "body_type": car.get("body_type"),
                "engine_size": car.get("engine_size"),
                "seller_type": car.get("seller_type"),
                "image_url": car.get("image_url"),
                "source": "autotrader",
            })
        
        return {
            "ok": True,
            "source": "autotrader_scraper",
            "search_url": build_autotrader_url(
                make=make, model=model, postcode=postcode,
                radius=radius, max_price=max_price
            ),
            "total": len(results),
            "items": normalized_items,
        }
        
    except Exception as e:
        return {
            "ok": False,
            "error": f"AutoTrader 搜索失败: {str(e)}",
            "items": [],
            "total": 0,
        }


def search_autotrader_fallback(
    make: str | None = None,
    model: str | None = None,
    postcode: str = "SW1A1AA",
    radius: int = 10,
    max_price: int | None = None,
    limit: int = 10,
    timeout: int = 30,
) -> dict[str, Any]:
    """备用方案：使用 requests + BeautifulSoup 直接爬取"""
    
    url = build_autotrader_url(
        make=make,
        model=model,
        postcode=postcode,
        radius=radius,
        max_price=max_price,
    )
    
    try:
        session = requests.Session()
        session.headers.update(_DEFAULT_HEADERS)
        response = session.get(url, timeout=timeout)
        
        if response.status_code != 200:
            return {
                "ok": False,
                "error": f"HTTP {response.status_code}",
                "items": [],
                "total": 0,
                "search_url": url,
            }
        
        soup = BeautifulSoup(response.text, "lxml")
        
        # 提取列表（需要根据实际页面结构调整）
        listings = []
        
        # AutoTrader 使用 JSON-LD 或 data attributes
        # 这里是简化示例，实际需要根据页面结构调整
        cards = soup.find_all("article", class_=re.compile("product-card"))
        
        for card in cards[:limit]:
            listing = {
                "listing_id": None,
                "title": None,
                "price": None,
                "price_display": None,
                "location": None,
                "url": None,
                "year": None,
                "mileage": None,
                "source": "autotrader_fallback",
            }
            
            # 提取标题
            title_elem = card.find(class_=re.compile("title"))
            if title_elem:
                listing["title"] = title_elem.get_text(strip=True)
            
            # 提取价格
            price_elem = card.find(class_=re.compile("price"))
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                listing["price_display"] = price_text
                # 提取数字
                price_match = re.search(r"[\d,]+", price_text)
                if price_match:
                    listing["price"] = int(price_match.group().replace(",", ""))
            
            # 提取链接
            link_elem = card.find("a")
            if link_elem and link_elem.get("href"):
                href = link_elem["href"]
                if not href.startswith("http"):
                    href = f"https://www.autotrader.co.uk{href}"
                listing["url"] = href
            
            listings.append(listing)
        
        return {
            "ok": True,
            "source": "autotrader_fallback",
            "search_url": url,
            "total": len(listings),
            "items": listings,
            "warning": "使用备用爬虫，数据可能不完整。推荐安装 autotrader_scraper 库。"
        }
        
    except Exception as e:
        return {
            "ok": False,
            "error": f"AutoTrader 搜索失败: {str(e)}",
            "items": [],
            "total": 0,
            "search_url": url,
        }


def search_autotrader(
    make: str | None = None,
    model: str | None = None,
    postcode: str = "SW1A1AA",
    radius: int = 10,
    max_price: int | None = None,
    min_year: int | None = None,
    max_year: int | None = None,
    limit: int = 10,
) -> dict[str, Any]:
    """
    智能 AutoTrader 搜索：优先使用库，失败时回退到自定义爬虫
    """
    
    # 优先使用官方库
    if HAS_AUTOTRADER_SCRAPER:
        result = search_autotrader_with_library(
            make=make,
            model=model,
            postcode=postcode,
            radius=radius,
            max_price=max_price,
            min_year=min_year,
            max_year=max_year,
            limit=limit,
        )
        if result["ok"]:
            return result
    
    # 降级到自定义爬虫
    print("⚠️  使用备用爬虫方案...")
    return search_autotrader_fallback(
        make=make,
        model=model,
        postcode=postcode,
        radius=radius,
        max_price=max_price,
        limit=limit,
    )


# 测试代码
if __name__ == "__main__":
    # 测试搜索
    result = search_autotrader(
        make="Toyota",
        model="Yaris",
        postcode="SW1A1AA",
        radius=10,
        max_price=10000,
        min_year=2016,
        limit=5,
    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
