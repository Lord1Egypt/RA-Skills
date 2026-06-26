#!/usr/bin/env python3
"""
Amazon Movers & Shakers Data Scraper
支持多种数据源：卖家精灵 API、真实爬取、Mock 数据

Usage:
    # 使用卖家精灵 API（推荐）
    python scrape_amazon.py --source sellersprite --keyword "standing desk" --api-key YOUR_KEY
    
    # 真实爬取
    python scrape_amazon.py --source scrape --category home-garden --limit 20
    
    # Mock 数据
    python scrape_amazon.py --source mock --category home-garden --limit 20
    
    # 安装依赖
    python scrape_amazon.py --install-deps
"""

import argparse
import json
import re
import sys
import time
import random
import os
import subprocess
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional
from urllib.parse import quote_plus, urljoin


def install_dependencies():
    """安装所需依赖"""
    dependencies = ["requests", "beautifulsoup4"]
    print("正在安装依赖...")
    for dep in dependencies:
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", dep, "--quiet"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            print(f"  ✓ {dep}")
        except subprocess.CalledProcessError:
            print(f"  ✗ {dep} 安装失败")
    print("依赖安装完成，请重新运行脚本")
    sys.exit(0)


def check_dependencies():
    """检查依赖是否安装"""
    missing = []
    
    try:
        import requests
    except ImportError:
        missing.append("requests")
    
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        missing.append("beautifulsoup4")
    
    return missing


HAS_REQUESTS = False
HAS_BS4 = False

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    pass

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    pass


SELLERSPRITE_API_BASE = "https://api.sellersprite.com/v1"
SELLERSPRITE_MCP_BASE = "https://mcp.sellersprite.com"

AMAZON_SITES = {
    "us": {"domain": "amazon.com", "marketplace": "US"},
    "uk": {"domain": "amazon.co.uk", "marketplace": "UK"},
    "de": {"domain": "amazon.de", "marketplace": "DE"},
    "jp": {"domain": "amazon.co.jp", "marketplace": "JP"},
}

CATEGORY_URLS = {
    "home-garden": "/Best-Sellers-Home-Kitchen/zgbs/home-garden",
    "electronics": "/Best-Sellers-Electronics/zgbs/electronics",
    "sports": "/Best-Sellers-Sports-Outdoors/zgbs/sporting-goods",
    "office": "/Best-Sellers-Office-Products/zgbs/office-products",
    "beauty": "/Best-Sellers-Beauty/zgbs/beauty",
    "toys": "/Best-Sellers-Toys-Games/zgbs/toys-and-games",
    "clothing": "/Best-Sellers-Clothing/zgbs/apparel",
    "jewelry": "/Best-Sellers-Jewelry/zgbs/jewelry",
    "automotive": "/Best-Sellers-Automotive/zgbs/automotive",
    "pet-supplies": "/Best-Sellers-Pet-Supplies/zgbs/pet-supplies"
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]


@dataclass
class AmazonProduct:
    asins: str
    title: str
    url: str
    image_url: str
    price: Optional[float]
    price_display: str
    currency: str
    rating: Optional[float]
    review_count: Optional[int]
    rank: int
    rank_change: str
    prime: bool
    category_path: str
    suitable_for_temu: bool
    exclusion_reason: Optional[str]
    monthly_sales: Optional[int] = None
    monthly_revenue: Optional[float] = None
    search_volume: Optional[int] = None


class SellerSpriteAPI:
    """卖家精灵 API 客户端"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("SELLERSPRITE_API_KEY", "")
        self.base_url = SELLERSPRITE_API_BASE
        self.session = requests.Session() if HAS_REQUESTS else None
        
        if self.session:
            self.session.headers.update({
                "secret-key": self.api_key,
                "Content-Type": "application/json",
            })
    
    def _request(self, endpoint: str, params: dict = None) -> dict:
        if not HAS_REQUESTS or not self.api_key:
            return {"code": "ERROR", "message": "API key required or requests not installed"}
        
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.get(url, params=params, timeout=30)
            return response.json()
        except Exception as e:
            return {"code": "ERROR", "message": str(e)}
    
    def get_keyword_traffic(self, asin: str, marketplace: str = "US") -> dict:
        """获取关键词流量数据"""
        endpoint = f"/traffic/keyword/stat/{marketplace}/{asin}/"
        return self._request(endpoint)
    
    def get_product_info(self, asin: str, marketplace: str = "US") -> dict:
        """获取产品信息"""
        endpoint = f"/product/info/{marketplace}/{asin}/"
        return self._request(endpoint)
    
    def get_bestsellers(self, category_id: str, marketplace: str = "US", limit: int = 100) -> dict:
        """获取类目热销榜"""
        endpoint = f"/bestsellers/{marketplace}/{category_id}/"
        params = {"limit": limit}
        return self._request(endpoint, params)
    
    def search_products(self, keyword: str, marketplace: str = "US", page: int = 1) -> dict:
        """搜索产品"""
        endpoint = f"/search/{marketplace}/"
        params = {"keyword": keyword, "page": page}
        return self._request(endpoint, params)
    
    def get_market_trends(self, category_id: str, marketplace: str = "US") -> dict:
        """获取市场趋势"""
        endpoint = f"/market/trends/{marketplace}/{category_id}/"
        return self._request(endpoint)


class AmazonMoversShakersScraper:
    
    def __init__(self, site: str = "us", sellersprite_key: str = None):
        self.site = site
        self.site_info = AMAZON_SITES.get(site, AMAZON_SITES["us"])
        self.base_url = f"https://www.{self.site_info['domain']}"
        self.marketplace = self.site_info["marketplace"]
        
        self.sellersprite = None
        if sellersprite_key or os.environ.get("SELLERSPRITE_API_KEY"):
            self.sellersprite = SellerSpriteAPI(sellersprite_key)
        
        self.session = None
        if HAS_REQUESTS:
            self.session = requests.Session()
            self.session.headers.update({
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.5",
            })
    
    def _get_headers(self) -> dict:
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
    
    def fetch_sellersprite_data(self, keyword: str = None, category_id: str = None, limit: int = 20) -> List[AmazonProduct]:
        """使用卖家精灵 API 获取数据"""
        if not self.sellersprite:
            print("卖家精灵 API key 未配置，回退到其他数据源")
            return []
        
        products = []
        
        if keyword:
            result = self.sellersprite.search_products(keyword, self.marketplace)
            if result.get("code") == "OK":
                data = result.get("data", {}).get("products", [])
                for i, item in enumerate(data[:limit]):
                    product = self._parse_sellersprite_product(item, i + 1)
                    if product:
                        products.append(product)
        
        elif category_id:
            result = self.sellersprite.get_bestsellers(category_id, self.marketplace, limit)
            if result.get("code") == "OK":
                data = result.get("data", {}).get("products", [])
                for i, item in enumerate(data[:limit]):
                    product = self._parse_sellersprite_product(item, i + 1)
                    if product:
                        products.append(product)
        
        return products
    
    def _parse_sellersprite_product(self, item: dict, rank: int) -> Optional[AmazonProduct]:
        """解析卖家精灵 API 返回的产品数据"""
        try:
            asin = item.get("asin", "")
            title = item.get("title", "")
            price = item.get("price", 0)
            rating = item.get("rating", 0)
            review_count = item.get("review_count", 0)
            monthly_sales = item.get("monthly_sales")
            monthly_revenue = item.get("monthly_revenue")
            rank_change = item.get("rank_change", "+0")
            
            if not asin:
                return None
            
            return AmazonProduct(
                asins=asin,
                title=title,
                url=f"{self.base_url}/dp/{asin}",
                image_url=item.get("image_url", ""),
                price=price,
                price_display=f"${price:.2f}" if price else "",
                currency="USD",
                rating=rating,
                review_count=review_count,
                rank=rank,
                rank_change=f"+{rank_change}" if rank_change > 0 else str(rank_change),
                prime=item.get("prime", False),
                category_path=item.get("category", ""),
                suitable_for_temu=True,
                exclusion_reason=None,
                monthly_sales=monthly_sales,
                monthly_revenue=monthly_revenue,
                search_volume=item.get("search_volume"),
            )
        except Exception as e:
            print(f"解析卖家精灵数据失败: {e}")
            return None
    
    def scrape_real_data(self, category: str = None, limit: int = 20, silent: bool = False) -> List[AmazonProduct]:
        """真实爬取亚马逊数据"""
        if not HAS_REQUESTS or not HAS_BS4:
            if not silent:
                print("requests/beautifulsoup4 未安装，无法爬取")
            return []
        
        if category and category in CATEGORY_URLS:
            url = urljoin(self.base_url, CATEGORY_URLS[category])
        else:
            url = urljoin(self.base_url, "/Best-Sellers/zgbs")
        
        if not silent:
            print(f"爬取: {url}")
        
        try:
            time.sleep(random.uniform(1, 2))
            response = self.session.get(url, headers=self._get_headers(), timeout=30)
            
            if response.status_code != 200:
                if not silent:
                    print(f"HTTP {response.status_code}")
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            products = []
            
            cards = soup.find_all(['div', 'li'], id=re.compile(r'item|product', re.I))
            
            if not cards:
                cards = soup.find_all(['div', 'li'], class_=re.compile(r'(item|product|card|zg-item)', re.I))
            
            if not cards:
                cards = soup.select('[data-asin]')
            
            if not silent:
                print(f"找到 {len(cards)} 个候选元素")
            
            for rank, card in enumerate(cards[:limit * 3], 1):
                product = self._parse_html_product(card, rank)
                if product:
                    products.append(product)
                    if len(products) >= limit:
                        break
            
            if not silent:
                print(f"解析出 {len(products)} 个产品")
            return products
            
        except Exception as e:
            if not silent:
                print(f"爬取失败: {e}")
            return []
    
    def _parse_html_product(self, card, rank: int) -> Optional[AmazonProduct]:
        """解析 HTML 中的产品"""
        try:
            asin = card.get('data-asin') if card.get('data-asin') else None
            
            if not asin:
                link = card.find('a', href=True)
                if link:
                    match = re.search(r'/dp/([A-Z0-9]{10})', link['href'])
                    if match:
                        asin = match.group(1)
            
            if not asin:
                return None
            
            title = ""
            for selector in [
                lambda c: c.find('a', {'href': re.compile(r'/dp/')}),
                lambda c: c.find(['span', 'div'], class_=re.compile(r'(product-title|p13n-sc-truncated|title)', re.I)),
                lambda c: c.find('img', {'alt': True}),
            ]:
                title_elem = selector(card)
                if title_elem:
                    if title_elem.name == 'img':
                        title = title_elem.get('alt', '')
                    elif title_elem.name == 'a':
                        title = title_elem.get_text(strip=True) or title_elem.get('title', '')
                    else:
                        title = title_elem.get_text(strip=True)
                    if title and len(title) > 5:
                        break
            
            if not title:
                title = f"Amazon Product {asin}"
            
            price = None
            price_elem = card.find(['span', 'div'], class_=re.compile(r'price', re.I))
            if price_elem:
                match = re.search(r'\$([\d.]+)', price_elem.get_text())
                if match:
                    price = float(match.group(1))
            
            if not price:
                price_text = card.find(text=re.compile(r'\$\d+'))
                if price_text:
                    match = re.search(r'\$([\d.]+)', str(price_text))
                    if match:
                        price = float(match.group(1))
            
            rating = None
            rating_elem = card.find(['span', 'i'], class_=re.compile(r'(rating|star|a-icon-star)', re.I))
            if rating_elem:
                match = re.search(r'([\d.]+)', rating_elem.get_text())
                if match:
                    rating = float(match.group(1))
            
            if not rating:
                rating_elem = card.find('span', {'class': re.compile(r'a-icon-alt', re.I)})
                if rating_elem:
                    match = re.search(r'([\d.]+)', rating_elem.get_text())
                    if match:
                        rating = float(match.group(1))
            
            image_url = ""
            img = card.find('img')
            if img:
                image_url = img.get('src', '') or img.get('data-src', '')
            
            return AmazonProduct(
                asins=asin,
                title=title,
                url=f"{self.base_url}/dp/{asin}",
                image_url=image_url,
                price=price,
                price_display=f"${price:.2f}" if price else "",
                currency="USD",
                rating=rating,
                review_count=None,
                rank=rank,
                rank_change="+0",
                prime=False,
                category_path="",
                suitable_for_temu=True,
                exclusion_reason=None,
            )
        except:
            return None
    
    def generate_mock_data(self, category: str = "home-garden", limit: int = 20) -> List[AmazonProduct]:
        """生成 Mock 数据"""
        mock_products = [
            {"title": "Standing Desk Converter, Height Adjustable", "price": 89.99, "rating": 4.5, "review_count": 1256, "rank_change": "+256", "monthly_sales": 850},
            {"title": "Monitor Stand Riser with Storage", "price": 34.99, "rating": 4.3, "review_count": 892, "rank_change": "+189", "monthly_sales": 1200},
            {"title": "Desk Mat Large, PU Leather Pad", "price": 19.99, "rating": 4.6, "review_count": 2341, "rank_change": "+145", "monthly_sales": 2500},
            {"title": "Cable Management Box, Desktop Organizer", "price": 24.99, "rating": 4.4, "review_count": 567, "rank_change": "+98", "monthly_sales": 980},
            {"title": "Keyboard Tray Under Desk, Ergonomic", "price": 45.99, "rating": 4.2, "review_count": 423, "rank_change": "+87", "monthly_sales": 650},
            {"title": "Desk Shelf Organizer, Wooden Bookshelf", "price": 39.99, "rating": 4.7, "review_count": 1567, "rank_change": "+76", "monthly_sales": 890},
            {"title": "Laptop Stand Adjustable, Aluminum Riser", "price": 29.99, "rating": 4.5, "review_count": 3456, "rank_change": "+65", "monthly_sales": 1800},
            {"title": "Desk Drawer Organizer, Storage Cabinet", "price": 54.99, "rating": 4.1, "review_count": 234, "rank_change": "+54", "monthly_sales": 420},
            {"title": "Foot Rest Under Desk, Ergonomic Footrest", "price": 22.99, "rating": 4.4, "review_count": 876, "rank_change": "+43", "monthly_sales": 1100},
            {"title": "Desk Lamp with USB Charging Port, LED", "price": 32.99, "rating": 4.6, "review_count": 2134, "rank_change": "+32", "monthly_sales": 1500},
        ]
        
        products = []
        for i, mock in enumerate(mock_products[:limit]):
            asin = f"B0MOCK{i:04d}XYZ"
            products.append(AmazonProduct(
                asins=asin,
                title=mock["title"],
                url=f"{self.base_url}/dp/{asin}",
                image_url=f"https://m.media-amazon.com/images/I/mock{i}.jpg",
                price=mock["price"],
                price_display=f"${mock['price']:.2f}",
                currency="USD",
                rating=mock["rating"],
                review_count=mock["review_count"],
                rank=i + 1,
                rank_change=mock["rank_change"],
                prime=True,
                category_path="Home & Kitchen > Home Office Furniture",
                suitable_for_temu=True,
                exclusion_reason=None,
                monthly_sales=mock.get("monthly_sales"),
                monthly_revenue=mock.get("monthly_sales", 0) * mock["price"],
            ))
        
        return products
    
    def fetch_data(self, source: str = "auto", keyword: str = None, category: str = None, 
                   category_id: str = None, limit: int = 20, silent: bool = False) -> tuple:
        """
        获取数据的主方法
        
        Args:
            source: 数据源 (sellersprite/scrape/mock/auto)
            keyword: 搜索关键词
            category: 类目名称
            category_id: 卖家精灵类目ID
            limit: 返回数量
            silent: 是否静默模式（不打印调试信息）
        
        Returns:
            (products, data_source)
        """
        products = []
        # data_source = "mock"
        data_source = "auto"
        
        if source == "sellersprite" or (source == "auto" and self.sellersprite):
            if not silent:
                print("尝试使用卖家精灵 API...")
            products = self.fetch_sellersprite_data(keyword, category_id, limit)
            if products:
                data_source = "sellersprite"
                return products, data_source
            if not silent:
                print("卖家精灵 API 无数据，尝试其他数据源...")
        
        if source in ["scrape", "auto"] and not products:
            if not silent:
                print("尝试真实爬取...")
            products = self.scrape_real_data(category, limit, silent)
            if products:
                data_source = "scrape"
                return products, data_source
            if not silent:
                print("爬取失败，使用 Mock 数据...")
        
        if not silent:
            print("使用 Mock 数据...")
        products = self.generate_mock_data(category, limit)
        data_source = "mock"
        
        return products, data_source


def format_output(products: List[AmazonProduct], data_source: str, output_format: str = "json") -> str:
    if output_format == "json":
        return json.dumps({
            "metadata": {
                "site": "amazon.com",
                "scrape_time": datetime.now().isoformat(),
                "total_products": len(products),
                "data_source": data_source,
            },
            "products": [asdict(p) for p in products]
        }, ensure_ascii=False, indent=2)
    else:
        lines = ["=" * 60, f"亚马逊产品列表 (数据源: {data_source})", "=" * 60]
        for p in products:
            status = "✅" if p.suitable_for_temu else "❌"
            lines.append(f"\n{p.rank}. {status} {p.title[:50]}...")
            lines.append(f"   ASIN: {p.asins}")
            lines.append(f"   价格: {p.price_display}")
            lines.append(f"   评分: {p.rating} ({p.review_count} 评论)")
            if p.monthly_sales:
                lines.append(f"   月销量: {p.monthly_sales}")
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Amazon Movers & Shakers 数据获取")
    
    parser.add_argument("--source", choices=["sellersprite", "scrape", "mock", "auto"], 
                       default="auto", help="数据源选择")
    parser.add_argument("--api-key", help="卖家精灵 API Key")
    parser.add_argument("--keyword", help="搜索关键词")
    parser.add_argument("--category", default="home-garden", help="类目名称")
    parser.add_argument("--category-id", help="卖家精灵类目ID")
    parser.add_argument("--site", default="us", choices=list(AMAZON_SITES.keys()), help="站点")
    parser.add_argument("--limit", type=int, default=20, help="返回数量")
    parser.add_argument("--output", help="输出文件")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="输出格式")
    parser.add_argument("--install-deps", action="store_true", help="安装依赖并退出")
    
    args = parser.parse_args()
    
    if args.install_deps:
        install_dependencies()
        return
    
    missing_deps = check_dependencies()
    if missing_deps and args.source != "mock":
        print(f"缺少依赖: {', '.join(missing_deps)}")
        print("提示: 运行 'python scrape_amazon.py --install-deps' 安装依赖")
        print("或使用 --source mock 使用 Mock 数据")
        print("")
    
    scraper = AmazonMoversShakersScraper(args.site, args.api_key)
    products, data_source = scraper.fetch_data(
        source=args.source,
        keyword=args.keyword,
        category=args.category,
        category_id=args.category_id,
        limit=args.limit,
        silent=(args.format == "json")
    )
    
    output = format_output(products, data_source, args.format)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f"结果已保存到 {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
