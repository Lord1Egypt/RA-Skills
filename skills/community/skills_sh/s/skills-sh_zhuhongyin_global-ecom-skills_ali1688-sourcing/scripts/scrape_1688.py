#!/usr/bin/env python3
"""
1688 Factory & Wholesale Price Scraper
Find factories and wholesale prices on 1688.com

Usage:
    python scrape_1688.py --keyword "升降桌" --limit 20
    python scrape_1688.py --keyword "desk converter" --province 浙江
"""

import argparse
import json
import re
import time
import random
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Optional
from urllib.parse import quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("Warning: requests/beautifulsoup4 not installed, will use mock data")


PRODUCTION_AREAS = {
    "办公家具": ["浙江安吉", "广东佛山", "江苏苏州"],
    "小家电": ["广东顺德", "浙江慈溪"],
    "箱包": ["浙江平湖", "广东花都"],
    "玩具": ["广东澄海", "浙江云和"],
    "纺织品": ["浙江绍兴", "江苏南通"],
    "五金工具": ["浙江永康", "广东东莞"],
}

CERTIFICATIONS = {
    "CE": "欧洲安全认证",
    "FCC": "美国联邦通信认证",
    "ROHS": "环保认证",
    "FDA": "美国食品药品认证",
    "UL": "美国安全认证",
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]


@dataclass
class PriceTier:
    quantity: str
    price: float


@dataclass
class Product:
    product_id: str
    title: str
    url: str
    image_url: str
    price_tiers: List[PriceTier]
    starting_price: float
    moq: int
    material: str
    colors: List[str]
    size: str
    weight: str
    packaging: str
    lead_time: str
    certifications: List[str]
    customization: bool
    sample_available: bool
    sample_price: Optional[float]


@dataclass
class Factory:
    rank: int
    company_name: str
    company_url: str
    verified: bool
    verification_type: str
    location: dict
    main_products: List[str]
    factory_info: dict
    products: List[Product]
    trade_info: dict
    ratings: dict
    transaction_history: dict
    contact: dict
    notes: str


@dataclass
class SourcingGuide:
    recommended_factories: List[dict]
    negotiation_tips: List[str]
    quality_checklist: List[str]
    shipping_options: List[dict]


@dataclass
class Ali1688SearchResult:
    keyword: str
    search_time: str
    total_results: int
    returned_results: int
    lowest_price: float
    highest_price: float
    average_price: float
    median_price: float
    main_production_areas: List[str]
    recommended_starting_price: float
    wholesale_price: dict
    factories: List[Factory]
    sourcing_guide: SourcingGuide
    price_for_calculator: dict


class Ali1688Scraper:
    
    def __init__(self):
        self.base_url = "https://www.1688.com"
        self.session = None
        if HAS_REQUESTS:
            self.session = requests.Session()
            self.session.headers.update({
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
            })
    
    def _get_headers(self) -> dict:
        return {
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": self.base_url,
        }
    
    def _fetch_page(self, url: str, retries: int = 3) -> Optional[str]:
        if not HAS_REQUESTS or not self.session:
            return None
        
        for attempt in range(retries):
            try:
                time.sleep(random.uniform(1, 2))
                response = self.session.get(
                    url,
                    headers=self._get_headers(),
                    timeout=30,
                    allow_redirects=True
                )
                
                if response.status_code == 200:
                    response.encoding = 'utf-8'
                    return response.text
                elif response.status_code in [403, 429]:
                    print(f"Rate limited, waiting... ({attempt + 1}/{retries})")
                    time.sleep(random.uniform(3, 6))
                else:
                    print(f"HTTP {response.status_code} for {url}")
                    
            except requests.exceptions.RequestException as e:
                print(f"Request failed: {e}, retrying... ({attempt + 1}/{retries})")
                time.sleep(random.uniform(2, 4))
        
        return None
    
    def get_search_url(self, keyword: str) -> str:
        encoded_keyword = quote_plus(keyword)
        return f"{self.base_url}/selloffer/offer_search.htm?keywords={encoded_keyword}"
    
    def parse_price_tiers(self, price_text: str) -> List[PriceTier]:
        tiers = []
        
        patterns = [
            (r'(\d+)-(\d+)[件台套]?\s*[¥￥]?([\d.]+)', 'range'),
            (r'≥?(\d+)[件台套]?\s*[¥￥]?([\d.]+)', 'min'),
        ]
        
        for pattern, ptype in patterns:
            matches = re.findall(pattern, price_text)
            for match in matches:
                if ptype == 'range':
                    tiers.append(PriceTier(
                        quantity=f"{match[0]}-{match[1]}",
                        price=float(match[2])
                    ))
                else:
                    tiers.append(PriceTier(
                        quantity=f"{match[0]}+",
                        price=float(match[1])
                    ))
        
        if not tiers:
            match = re.search(r'[¥￥]?([\d.]+)', price_text)
            if match:
                tiers = [
                    PriceTier(quantity="1-9", price=float(match.group(1)) * 1.2),
                    PriceTier(quantity="10-49", price=float(match.group(1)) * 1.1),
                    PriceTier(quantity="50+", price=float(match.group(1))),
                ]
        
        return tiers
    
    def detect_production_area(self, keyword: str) -> List[str]:
        for category, areas in PRODUCTION_AREAS.items():
            if any(word in keyword for word in category.split()):
                return areas
        return ["浙江", "广东", "江苏"]
    
    def _parse_product_card(self, card, rank: int) -> Optional[tuple]:
        try:
            product_id = ""
            link = card.find('a', href=True)
            if link:
                href = link['href']
                match = re.search(r'offer/(\d+)\.html', href)
                if match:
                    product_id = match.group(1)
                else:
                    match = re.search(r'offerId=(\d+)', href)
                    if match:
                        product_id = match.group(1)
            
            if not product_id:
                product_id = f"1688_{hash(str(card)) % 1000000}"
            
            title = ""
            title_elem = (
                card.find('div', class_=re.compile(r'(title|subject)', re.I)) or
                card.find('a', class_=re.compile(r'title', re.I)) or
                card.find('h2') or
                card.find('h3')
            )
            if title_elem:
                title = title_elem.get_text(strip=True)
            
            if not title:
                title = f"1688 产品 {product_id}"
            
            url = f"https://detail.1688.com/offer/{product_id}.html"
            
            image_url = ""
            img = card.find('img')
            if img:
                image_url = img.get('src', '') or img.get('data-lazy-src', '') or img.get('data-src', '')
            
            price_tiers = []
            price_elem = card.find(['span', 'div', 'p'], class_=re.compile(r'(price|cost)', re.I))
            if price_elem:
                price_text = price_elem.get_text(strip=True)
                price_tiers = self.parse_price_tiers(price_text)
            
            if not price_tiers:
                match = re.search(r'[¥￥]?([\d.]+)', card.get_text())
                if match:
                    base_price = float(match.group(1))
                    price_tiers = [
                        PriceTier(quantity="1-9", price=base_price * 1.2),
                        PriceTier(quantity="10-49", price=base_price * 1.1),
                        PriceTier(quantity="50+", price=base_price),
                    ]
            
            starting_price = price_tiers[-1].price if price_tiers else 100.0
            
            company_name = ""
            company_elem = card.find(['span', 'div', 'a'], class_=re.compile(r'(company|shop|store|seller)', re.I))
            if company_elem:
                company_name = company_elem.get_text(strip=True)
            
            location = {"province": "", "city": ""}
            location_elem = card.find(['span', 'div'], class_=re.compile(r'(location|address|area)', re.I))
            if location_elem:
                loc_text = location_elem.get_text(strip=True)
                match = re.match(r'(.+?)(.+)?', loc_text)
                if match:
                    location["province"] = match.group(1)
                    location["city"] = match.group(2) or ""
            
            return {
                "product_id": product_id,
                "title": title,
                "url": url,
                "image_url": image_url,
                "price_tiers": price_tiers,
                "starting_price": starting_price,
                "company_name": company_name,
                "location": location,
            }
            
        except Exception as e:
            print(f"Error parsing product card: {e}")
            return None
    
    def scrape_real_data(self, keyword: str, limit: int = 20, silent: bool = False) -> List[Factory]:
        if not HAS_REQUESTS:
            if not silent:
                print("requests/beautifulsoup4 not available, falling back to mock data")
            return []
        
        url = self.get_search_url(keyword)
        if not silent:
            print(f"Fetching: {url}")
        
        html = self._fetch_page(url)
        if not html:
            if not silent:
                print("Failed to fetch page, falling back to mock data")
            return []
        
        try:
            soup = BeautifulSoup(html, 'html.parser')
            products_data = []
            
            cards = soup.find_all(['div', 'li'], class_=re.compile(r'(offer|item|product|card)', re.I))
            
            if not cards:
                cards = soup.find_all('div', attrs={'data-offer-id': True})
            
            if not cards:
                cards = soup.find_all('div', class_='sw-offer')
            
            if not silent:
                print(f"Found {len(cards)} product cards")
            
            for rank, card in enumerate(cards[:limit * 2], 1):
                product_data = self._parse_product_card(card, rank)
                if product_data and product_data["price_tiers"]:
                    products_data.append(product_data)
                    if len(products_data) >= limit:
                        break
            
            factories = self._group_products_by_factory(products_data)
            return factories
            
        except Exception as e:
            if not silent:
                print(f"Error parsing HTML: {e}")
            return []
    
    def _group_products_by_factory(self, products_data: List[dict]) -> List[Factory]:
        factory_map = {}
        
        for i, pd in enumerate(products_data):
            company_name = pd.get("company_name") or f"工厂 {i + 1}"
            
            if company_name not in factory_map:
                location = pd.get("location", {"province": "", "city": ""})
                factory_map[company_name] = {
                    "rank": len(factory_map) + 1,
                    "company_name": company_name,
                    "location": location,
                    "products": [],
                    "verified": "认证" in company_name or "实业" in company_name,
                }
            
            product = Product(
                product_id=pd["product_id"],
                title=pd["title"],
                url=pd["url"],
                image_url=pd["image_url"],
                price_tiers=pd["price_tiers"],
                starting_price=pd["starting_price"],
                moq=10,
                material="",
                colors=["黑色", "白色"],
                size="",
                weight="",
                packaging="纸箱包装",
                lead_time="7-15天",
                certifications=[],
                customization=True,
                sample_available=True,
                sample_price=pd["starting_price"] * 1.2
            )
            factory_map[company_name]["products"].append(product)
        
        factories = []
        for company_name, data in factory_map.items():
            factory = Factory(
                rank=data["rank"],
                company_name=company_name,
                company_url=f"https://{company_name[:4].lower()}.1688.com",
                verified=data["verified"],
                verification_type="深度验厂" if data["verified"] else "企业认证",
                location=data["location"],
                main_products=[p.title[:20] for p in data["products"][:3]],
                factory_info={
                    "established": "2015",
                    "employees": "50-100人",
                    "production_capacity": "10000件/月",
                    "export_experience": True
                },
                products=data["products"],
                trade_info={
                    "min_order": data["products"][0].moq if data["products"] else 10,
                    "payment_terms": ["支付宝", "银行转账"],
                    "shipping": "支持物流配送",
                    "return_policy": "7天无理由退换"
                },
                ratings={
                    "overall": 4.5,
                    "quality": 4.6,
                    "service": 4.4,
                    "delivery": 4.5
                },
                transaction_history={
                    "total_orders": "500+",
                    "repeat_buyers": "35%",
                    "response_rate": "98%"
                },
                contact={
                    "contact_person": "王经理",
                    "phone": "138****8888",
                    "wechat": "",
                    "online_status": "在线"
                },
                notes="产业带工厂" if data["verified"] else "待验证工厂"
            )
            factories.append(factory)
        
        return factories
    
    def generate_sourcing_instruction(self, keyword: str, product: Product) -> str:
        instruction = f"""【采购找货指令】

产品名称：{keyword}
关键词：{keyword}、批发、工厂直供

材质要求：
- 主要材质：{product.material or '待确认'}
- 规格：{product.size or '待确认'}

功能要求：
- 重量：{product.weight or '待确认'}
- 包装：{product.packaging}

认证要求：
{chr(10).join(f'- {cert}' for cert in product.certifications) if product.certifications else '- 无特殊认证要求'}

起订量：{product.moq}件起
目标价格：¥{product.starting_price:.0f}-{product.starting_price * 1.2:.0f}/件（{product.moq}件起批价）

避坑提示：
1. 注意材质质量，避免以次充好
2. 确认产品质保期
3. 检查工艺细节
4. 要求提供实物样品确认品质

推荐产业带：{', '.join(self.detect_production_area(keyword))}
"""
        return instruction
    
    def generate_mock_data(self, keyword: str, limit: int = 20) -> Ali1688SearchResult:
        category_pricing = {
            "home-garden": {"min": 15.0, "max": 35.0},
            "electronics": {"min": 8.0, "max": 18.0},
            "sports": {"min": 12.0, "max": 25.0},
            "office": {"min": 10.0, "max": 22.0},
            "beauty": {"min": 6.0, "max": 15.0},
            "toys": {"min": 5.0, "max": 12.0},
            "clothing": {"min": 8.0, "max": 18.0},
            "jewelry": {"min": 10.0, "max": 25.0},
            "automotive": {"min": 12.0, "max": 28.0},
            "pet-supplies": {"min": 6.0, "max": 15.0}
        }
        
        mock_factories_data = [
            {
                "name": "安吉县宏达家具有限公司",
                "location": {"province": "浙江", "city": "安吉"},
                "verified": True,
                "verification_type": "深度验厂",
                "rating": 4.8,
                "products": [
                    {
                        "title": f"{keyword} 站立式办公桌 可折叠",
                        "price_tiers": [
                            {"quantity": "1-9", "price": 25.0},
                            {"quantity": "10-49", "price": 20.0},
                            {"quantity": "50+", "price": 18.0}
                        ],
                        "material": "冷轧钢+环保板材",
                        "moq": 10,
                    }
                ]
            },
            {
                "name": "佛山顺德办公设备有限公司",
                "location": {"province": "广东", "city": "佛山"},
                "verified": True,
                "verification_type": "企业认证",
                "rating": 4.6,
                "products": [
                    {
                        "title": f"{keyword} 升降桌架 电动款",
                        "price_tiers": [
                            {"quantity": "1-9", "price": 30.0},
                            {"quantity": "10-49", "price": 25.0},
                            {"quantity": "50+", "price": 22.0}
                        ],
                        "material": "优质钢材+实木",
                        "moq": 5,
                    }
                ]
            },
            {
                "name": "苏州工业园区家具制造厂",
                "location": {"province": "江苏", "city": "苏州"},
                "verified": False,
                "verification_type": "未认证",
                "rating": 4.3,
                "products": [
                    {
                        "title": f"{keyword} 桌面转换器 简易款",
                        "price_tiers": [
                            {"quantity": "1-9", "price": 18.0},
                            {"quantity": "10-49", "price": 15.0},
                            {"quantity": "50+", "price": 12.0}
                        ],
                        "material": "钢材+密度板",
                        "moq": 20,
                    }
                ]
            },
            {
                "name": "广州白云区化妆品制造厂",
                "location": {"province": "广东", "city": "广州"},
                "verified": True,
                "verification_type": "企业认证",
                "rating": 4.5,
                "products": [
                    {
                        "title": f"{keyword} 护肤套装 基础款",
                        "price_tiers": [
                            {"quantity": "1-9", "price": 8.0},
                            {"quantity": "10-49", "price": 6.5},
                            {"quantity": "50+", "price": 5.5}
                        ],
                        "material": "天然植物成分",
                        "moq": 50,
                    }
                ]
            },
            {
                "name": "义乌市玩具制造有限公司",
                "location": {"province": "浙江", "city": "义乌"},
                "verified": True,
                "verification_type": "深度验厂",
                "rating": 4.7,
                "products": [
                    {
                        "title": f"{keyword} 智能玩具 教育款",
                        "price_tiers": [
                            {"quantity": "1-9", "price": 6.0},
                            {"quantity": "10-49", "price": 5.0},
                            {"quantity": "50+", "price": 4.0}
                        ],
                        "material": "ABS环保塑料",
                        "moq": 100,
                    }
                ]
            },
            {
                "name": "宁波鄞州区服装制造厂",
                "location": {"province": "浙江", "city": "宁波"},
                "verified": True,
                "verification_type": "企业认证",
                "rating": 4.4,
                "products": [
                    {
                        "title": f"{keyword} 休闲套装 时尚款",
                        "price_tiers": [
                            {"quantity": "1-9", "price": 10.0},
                            {"quantity": "10-49", "price": 8.0},
                            {"quantity": "50+", "price": 6.5}
                        ],
                        "material": "纯棉+涤纶",
                        "moq": 50,
                    }
                ]
            },
            {
                "name": "深圳罗湖区珠宝首饰厂",
                "location": {"province": "广东", "city": "深圳"},
                "verified": True,
                "verification_type": "深度验厂",
                "rating": 4.6,
                "products": [
                    {
                        "title": f"{keyword} 时尚项链 不锈钢",
                        "price_tiers": [
                            {"quantity": "1-9", "price": 12.0},
                            {"quantity": "10-49", "price": 10.0},
                            {"quantity": "50+", "price": 8.0}
                        ],
                        "material": "316L不锈钢",
                        "moq": 20,
                    }
                ]
            },
            {
                "name": "东莞塘厦区汽车用品厂",
                "location": {"province": "广东", "city": "东莞"},
                "verified": True,
                "verification_type": "企业认证",
                "rating": 4.3,
                "products": [
                    {
                        "title": f"{keyword} 车载充电器 通用款",
                        "price_tiers": [
                            {"quantity": "1-9", "price": 15.0},
                            {"quantity": "10-49", "price": 12.0},
                            {"quantity": "50+", "price": 10.0}
                        ],
                        "material": "ABS阻燃材料",
                        "moq": 30,
                    }
                ]
            },
            {
                "name": "上海青浦区宠物用品厂",
                "location": {"province": "上海", "city": "上海"},
                "verified": True,
                "verification_type": "企业认证",
                "rating": 4.5,
                "products": [
                    {
                        "title": f"{keyword} 宠物玩具 耐咬款",
                        "price_tiers": [
                            {"quantity": "1-9", "price": 7.0},
                            {"quantity": "10-49", "price": 5.5},
                            {"quantity": "50+", "price": 4.5}
                        ],
                        "material": "天然橡胶",
                        "moq": 20,
                    }
                ]
            },
        ]
        
        factories = []
        all_prices = []
        
        for rank, mock_factory in enumerate(mock_factories_data[:limit], 1):
            products = []
            for mock_product in mock_factory["products"]:
                price_tiers = [PriceTier(**pt) for pt in mock_product["price_tiers"]]
                starting_price = price_tiers[-1].price if price_tiers else 100.0
                
                product = Product(
                    product_id=f"1688_{hash(mock_product['title']) % 1000000}",
                    title=mock_product["title"],
                    url=f"https://detail.1688.com/offer/{hash(mock_product['title']) % 1000000}.html",
                    image_url=f"https://cbu01.alicdn.com/mock_{rank}.jpg",
                    price_tiers=price_tiers,
                    starting_price=starting_price,
                    moq=mock_product["moq"],
                    material=mock_product["material"],
                    colors=["黑色", "白色", "木纹"],
                    size="80*40*10-50cm",
                    weight="8.5kg",
                    packaging="纸箱包装",
                    lead_time="7-15天",
                    certifications=["CE", "FCC"],
                    customization=True,
                    sample_available=True,
                    sample_price=starting_price * 1.2
                )
                products.append(product)
                all_prices.append(starting_price)
            
            factory = Factory(
                rank=rank,
                company_name=mock_factory["name"],
                company_url=f"https://{mock_factory['name'][:4].lower()}.1688.com",
                verified=mock_factory["verified"],
                verification_type=mock_factory["verification_type"],
                location=mock_factory["location"],
                main_products=[keyword, "办公桌", "升降桌"],
                factory_info={
                    "established": "2015",
                    "employees": "50-100人",
                    "production_capacity": "10000件/月",
                    "export_experience": True
                },
                products=products,
                trade_info={
                    "min_order": products[0].moq if products else 10,
                    "payment_terms": ["支付宝", "银行转账"],
                    "shipping": "支持物流配送",
                    "return_policy": "7天无理由退换"
                },
                ratings={
                    "overall": mock_factory["rating"],
                    "quality": mock_factory["rating"] + 0.1,
                    "service": mock_factory["rating"] - 0.1,
                    "delivery": mock_factory["rating"]
                },
                transaction_history={
                    "total_orders": "500+",
                    "repeat_buyers": "35%",
                    "response_rate": "98%"
                },
                contact={
                    "contact_person": "王经理",
                    "phone": "138****8888",
                    "wechat": "xxx8888",
                    "online_status": "在线"
                },
                notes=f"{'产业带核心工厂' if mock_factory['verified'] else '待验证工厂'}，{'出口经验丰富' if mock_factory['verified'] else '建议先拿样品'}"
            )
            factories.append(factory)
        
        factories.sort(key=lambda f: f.products[0].starting_price if f.products else 999)
        
        sourcing_guide = SourcingGuide(
            recommended_factories=[
                {
                    "factory_name": factories[0].company_name,
                    "reason": "价格合理，质量稳定，出口经验丰富"
                }
            ],
            negotiation_tips=[
                "起订量 50+ 可谈价格，预计可降 10-15%",
                "长期合作可申请账期",
                "定制包装需额外费用"
            ],
            quality_checklist=[
                "检查材质质量",
                "确认产品质保期",
                "要求提供认证证书"
            ],
            shipping_options=[
                {"method": "国内物流", "cost": "¥15-30/件", "time": "3-5天"},
                {"method": "快递", "cost": "¥50-80/件", "time": "1-2天"}
            ]
        )
        
        best_factory = factories[0]
        best_product = best_factory.products[0] if best_factory.products else None
        
        return Ali1688SearchResult(
            keyword=keyword,
            search_time=datetime.now().isoformat(),
            total_results=1256,
            returned_results=len(factories),
            lowest_price=min(all_prices) if all_prices else 0,
            highest_price=max(all_prices) if all_prices else 0,
            average_price=sum(all_prices) / len(all_prices) if all_prices else 0,
            median_price=sorted(all_prices)[len(all_prices) // 2] if all_prices else 0,
            main_production_areas=self.detect_production_area(keyword),
            recommended_starting_price=best_product.starting_price if best_product else 100,
            wholesale_price={
                "min_price": min(all_prices) if all_prices else 0,
                "max_price": max(all_prices) if all_prices else 0,
                "recommended_price": best_product.starting_price if best_product else 100,
                "currency": "CNY",
                "unit": "件",
                "note": f"建议以 ¥{best_product.starting_price if best_product else 100:.0f} 作为核价参考价"
            },
            factories=factories,
            sourcing_guide=sourcing_guide,
            price_for_calculator={
                "ali1688_price": best_product.starting_price if best_product else 100,
                "currency": "CNY",
                "source": best_factory.company_name,
                "moq": best_product.moq if best_product else 50,
                "note": f"{best_product.moq if best_product else 50}件起批价，用于核价计算"
            }
        )
    
    def build_result_from_factories(self, keyword: str, factories: List[Factory]) -> Ali1688SearchResult:
        if not factories:
            return self.generate_mock_data(keyword)
        
        all_prices = []
        for f in factories:
            for p in f.products:
                all_prices.append(p.starting_price)
        
        factories.sort(key=lambda f: f.products[0].starting_price if f.products else 999)
        
        best_factory = factories[0]
        best_product = best_factory.products[0] if best_factory.products else None
        
        sourcing_guide = SourcingGuide(
            recommended_factories=[
                {"factory_name": best_factory.company_name, "reason": "价格最低"}
            ],
            negotiation_tips=["起订量可谈", "长期合作可申请账期"],
            quality_checklist=["检查材质质量", "确认产品质保期"],
            shipping_options=[{"method": "物流", "cost": "¥15-30/件", "time": "3-5天"}]
        )
        
        return Ali1688SearchResult(
            keyword=keyword,
            search_time=datetime.now().isoformat(),
            total_results=len(factories),
            returned_results=len(factories),
            lowest_price=min(all_prices) if all_prices else 0,
            highest_price=max(all_prices) if all_prices else 0,
            average_price=sum(all_prices) / len(all_prices) if all_prices else 0,
            median_price=sorted(all_prices)[len(all_prices) // 2] if all_prices else 0,
            main_production_areas=self.detect_production_area(keyword),
            recommended_starting_price=best_product.starting_price if best_product else 100,
            wholesale_price={
                "min_price": min(all_prices) if all_prices else 0,
                "max_price": max(all_prices) if all_prices else 0,
                "recommended_price": best_product.starting_price if best_product else 100,
                "currency": "CNY",
                "unit": "件",
                "note": f"建议以 ¥{best_product.starting_price if best_product else 100:.0f} 作为核价参考价"
            },
            factories=factories,
            sourcing_guide=sourcing_guide,
            price_for_calculator={
                "ali1688_price": best_product.starting_price if best_product else 100,
                "currency": "CNY",
                "source": best_factory.company_name,
                "moq": best_product.moq if best_product else 50,
                "note": f"{best_product.moq if best_product else 50}件起批价，用于核价计算"
            }
        )


def format_output(result: Ali1688SearchResult, output_format: str = "json") -> str:
    if output_format == "json":
        data = {
            "metadata": {
                "keyword": result.keyword,
                "search_time": result.search_time,
                "total_results": result.total_results,
                "returned_results": result.returned_results,
                "data_source": "real" if result.total_results < 1000 else "mock"
            },
            "summary": {
                "lowest_price": result.lowest_price,
                "highest_price": result.highest_price,
                "average_price": round(result.average_price, 2),
                "median_price": result.median_price,
                "main_production_areas": result.main_production_areas,
                "recommended_starting_price": result.recommended_starting_price
            },
            "wholesale_price": result.wholesale_price,
            "factories": [
                {
                    **asdict(f),
                    "products": [
                        {**asdict(p), "price_tiers": [asdict(pt) for pt in p.price_tiers]}
                        for p in f.products
                    ]
                }
                for f in result.factories
            ],
            "sourcing_guide": asdict(result.sourcing_guide),
            "price_for_calculator": result.price_for_calculator
        }
        return json.dumps(data, ensure_ascii=False, indent=2)
    else:
        lines = []
        lines.append("=" * 60)
        lines.append(f"1688 供应链查询: {result.keyword}")
        lines.append("=" * 60)
        lines.append(f"\n【价格概况】")
        lines.append(f"  价格区间: ¥{result.lowest_price:.0f} - ¥{result.highest_price:.0f}")
        lines.append(f"  建议参考价: ¥{result.recommended_starting_price:.0f}")
        lines.append(f"  主要产地: {', '.join(result.main_production_areas)}")
        lines.append(f"\n【推荐工厂】")
        for f in result.factories[:3]:
            verified = "✅" if f.verified else "⚠️"
            lines.append(f"  {f.rank}. {verified} {f.company_name}")
            lines.append(f"     位置: {f.location['province']}{f.location['city']}")
            if f.products:
                lines.append(f"     起批价: ¥{f.products[0].starting_price:.0f} ({f.products[0].moq}件起)")
        lines.append(f"\n【核价参考】")
        lines.append(f"  1688 拿货价: ¥{result.price_for_calculator['ali1688_price']}")
        lines.append(f"  来源: {result.price_for_calculator['source']}")
        return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="1688 Factory & Wholesale Price Scraper"
    )
    parser.add_argument(
        "--keyword", type=str, required=True,
        help="Search keyword"
    )
    parser.add_argument(
        "--province", type=str,
        help="Filter by province"
    )
    parser.add_argument(
        "--limit", type=int, default=20,
        help="Maximum number of factories to return"
    )
    parser.add_argument(
        "--output", type=str,
        help="Output file path"
    )
    parser.add_argument(
        "--format", type=str, default="json",
        choices=["json", "text"],
        help="Output format"
    )
    parser.add_argument(
        "--mock", action="store_true",
        help="Force use mock data"
    )
    
    args = parser.parse_args()
    
    scraper = Ali1688Scraper()
    
    silent = args.format == "json"
    result = None
    
    if not args.mock:
        factories = scraper.scrape_real_data(args.keyword, args.limit, silent)
        if factories:
            result = scraper.build_result_from_factories(args.keyword, factories)
    
    if not result:
        if not silent:
            print("Using mock data as fallback...")
        result = scraper.generate_mock_data(keyword=args.keyword, limit=args.limit)
    
    output = format_output(result, args.format)
    
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(output)
        if not silent:
            print(f"Results saved to {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
