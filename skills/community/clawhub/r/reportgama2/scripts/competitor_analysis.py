# -*- coding: utf-8 -*-
"""
Report-gama — 竞争对手深度分析模块
分析目标品类主要竞争者：品牌、产品线、价格、市场份额、渠道策略
"""

import random
import time
import logging
import re
import json
from datetime import datetime
from urllib.parse import quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"[ERROR] 缺少必需依赖: {e}")
    print("请运行: pip install requests beautifulsoup4 lxml")
    raise SystemExit(1)

from config import ECOMMERCE_PLATFORMS, REQUEST_TIMEOUT, REQUEST_RETRIES, USER_AGENTS, LOG_LEVEL, LOG_FORMAT

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class CompetitorAnalyzer:
    """竞争对手深度分析"""

    def __init__(self, country="俄罗斯", lang="ru"):
        self.country = country
        self.lang = lang
        self.country_code = self._country_to_code(country)
        self.session = self._create_session()
        self.competitors = []

    def _country_to_code(self, country):
        codes = {"俄罗斯": "RU", "哈萨克斯坦": "KZ", "中国": "CN", "美国": "US"}
        return codes.get(country, "RU")

    def _create_session(self):
        session = requests.Session()
        session.headers.update({
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": f"{self.lang},en;q=0.5",
        })
        return session

    def _fetch(self, url, max_retries=REQUEST_RETRIES):
        for attempt in range(max_retries + 1):
            try:
                resp = self.session.get(url, timeout=REQUEST_TIMEOUT)
                if resp.status_code == 200:
                    return resp.text
                elif resp.status_code == 429:
                    time.sleep((attempt + 1) * 5)
            except Exception as e:
                logger.warning(f"请求失败: {e}")
                time.sleep(3)
        return None

    def analyze_from_search(self, category_keywords, brand_keywords=None):
        """
        从搜索结果中分析竞争格局

        Args:
            category_keywords: 品类关键词
            brand_keywords: 已知品牌关键词列表

        Returns:
            list: 竞争者信息列表
        """
        logger.info("[竞争分析] 开始分析竞争格局...")
        brand_keywords = brand_keywords or []

        # 搜索竞争者
        ru_kw = category_keywords.get("ru", [])
        en_kw = category_keywords.get("en", [])

        # 搜索品牌榜单
        brand_search_results = self._search_brand_rankings(ru_kw + en_kw)

        # 搜索市场份额数据
        market_share = self._search_market_share(ru_kw + en_kw)

        # 从电商平台获取TOP品牌
        top_brands = self._get_top_brands_from_ecommerce(ru_kw)

        # 合并分析
        competitors = self._build_competitor_matrix(
            brand_search_results, market_share, top_brands, brand_keywords
        )

        logger.info(f"[竞争分析] 分析了 {len(competitors)} 个竞争者")
        self.competitors = competitors
        return competitors

    def _search_brand_rankings(self, keywords):
        """搜索品牌排行榜"""
        results = []
        for kw in keywords[:5]:
            url = f"https://www.google.com/search?q={quote_plus(kw + ' рейтинг брендов')}&hl={self.lang}"
            logger.info(f"[品牌排行] {kw[:30]}...")
            html = self._fetch(url)
            if html:
                soup = BeautifulSoup(html, "lxml")
                # 提取搜索结果中的品牌提及
                text = soup.get_text()
                # 寻找品牌词
                for line in text.split('\n'):
                    if any(brand in line for brand in [" Abbott", "Roche", "Omron", "Johnson", "Medtronic", "Samsung", "Xiaomi"]):
                        results.append({"text": line.strip(), "keyword": kw, "type": "brand_mention"})
            time.sleep(random.uniform(2, 4))
        return results

    def _search_market_share(self, keywords):
        """搜索市场份额数据"""
        data = []
        for kw in keywords[:3]:
            url = f"https://www.google.com/search?q={quote_plus(kw + ' доля рынка 2024 2025')}&hl={self.lang}"
            logger.info(f"[市场份额] {kw[:30]}...")
            html = self._fetch(url)
            if html:
                soup = BeautifulSoup(html, "lxml")
                for item in soup.select("div.g")[:5]:
                    text = item.get_text()
                    if any(w in text for w in ["доля", "рынок", "%", "市场份额", "market share"]):
                        title = item.select_one("h3")
                        data.append({
                            "title": title.get_text(strip=True) if title else "",
                            "snippet": text[:300],
                            "keyword": kw,
                            "type": "market_share"
                        })
            time.sleep(random.uniform(2, 4))
        return data

    def _get_top_brands_from_ecommerce(self, ru_keywords):
        """从电商平台获取TOP品牌"""
        top_brands = {}
        platforms = ["wildberries", "ozon", "yandex_market"]

        for platform_key in platforms:
            platform = ECOMMERCE_PLATFORMS.get(platform_key)
            if not platform:
                continue

            for kw in ru_keywords[:2]:
                try:
                    url = platform["search_url"].format(keyword=quote_plus(kw))
                    logger.info(f"[电商品牌] {platform['name']}: {kw[:30]}...")
                    html = self._fetch(url)
                    if html:
                        soup = BeautifulSoup(html, "lxml")
                        # 提取商品中的品牌名
                        for item in soup.select("[class*='product'], [class*='goods'], [class*='card']")[:20]:
                            text = item.get_text()
                            # 尝试提取品牌名（通常在商品名前）
                            if text and len(text) > 10:
                                parts = text.split()
                                if len(parts) > 1:
                                    brand = parts[0]
                                    if brand and brand[0].isupper():
                                        top_brands[brand] = top_brands.get(brand, 0) + 1
                    time.sleep(random.uniform(1.5, 3))
                except Exception as e:
                    logger.warning(f"[{platform['name']}] 失败: {e}")

        # 按出现频次排序
        sorted_brands = sorted(top_brands.items(), key=lambda x: x[1], reverse=True)
        return [{"brand": b, "mentions": c} for b, c in sorted_brands[:20]]

    def _build_competitor_matrix(self, brand_results, share_results, top_brands, known_brands):
        """构建竞争者矩阵"""
        competitors = []

        # 从TOP品牌构建基础竞争者
        seen = set()
        for item in top_brands:
            brand = item["brand"]
            if brand in seen or len(brand) < 3:
                continue
            seen.add(brand)
            competitors.append({
                "brand": brand,
                "origin": self._estimate_brand_origin(brand),
                "position": "unknown",
                "price_segment": "unknown",
                "channel": "unknown",
                "data_source": "ecommerce",
                "confidence": "medium",
                "mentions": item.get("mentions", 0),
            })

        # 添加已知品牌
        for brand in known_brands:
            if brand not in seen:
                seen.add(brand)
                competitors.append({
                    "brand": brand,
                    "origin": self._estimate_brand_origin(brand),
                    "position": self._estimate_position(brand),
                    "price_segment": self._estimate_price_segment(brand),
                    "channel": "医院/零售/电商",
                    "data_source": "known",
                    "confidence": "high",
                    "mentions": 0,
                })

        return competitors

    def _estimate_brand_origin(self, brand):
        """估算品牌来源国"""
        brand_lower = brand.lower()
        russian_brands = ["элта", "сателлит", "омрон", "ittle doctor", "b.well", "армед"]
        chinese_brands = ["xiaomi", "cettua", "yzed", "beurer"]
        if any(rb in brand_lower for rb in russian_brands):
            return "🇷🇺 俄罗斯/本地"
        elif any(cb in brand_lower for cb in chinese_brands):
            return "🇨🇳 中国"
        return "🌐 跨国品牌"

    def _estimate_position(self, brand):
        """估算品牌市场定位"""
        brand_lower = brand.lower()
        premium = ["abbott", "roche", "medtronic", "philips", "ge healthcare"]
        mid = ["omron", "microlife", "bayer", "的一"]
        if any(p in brand_lower for p in premium):
            return "高端"
        elif any(p in brand_lower for p in mid):
            return "中端"
        return "大众/低端"

    def _estimate_price_segment(self, brand):
        """估算价格段"""
        brand_lower = brand.lower()
        premium = ["abbott", "roche", "medtronic", "philips"]
        if any(p in brand_lower for p in premium):
            return "高价位（>3000 RUB）"
        return "中低价位（<3000 RUB）"

    def generate_competitor_report(self, competitors=None):
        """生成竞争分析报告"""
        competitors = competitors or self.competitors
        if not competitors:
            return "## 🏢 竞争格局分析\n\n（暂无数据）"

        report = "## 🏢 竞争格局分析\n\n"

        # 按定位分组
        by_position = {}
        for c in competitors:
            pos = c.get("position", "unknown")
            if pos not in by_position:
                by_position[pos] = []
            by_position[pos].append(c)

        report += f"_共分析 {len(competitors)} 个主要竞争者_\n\n"

        for position, comps in by_position.items():
            report += f"### 🔹 {position} 定位（{len(comps)} 个品牌）\n\n"
            report += "| 品牌 | 来源 | 价格段 | 主要渠道 | 可信度 | 备注 |\n"
            report += "|-----|------|--------|---------|--------|------|\n"
            for c in comps[:10]:
                brand = c.get("brand", "")
                origin = c.get("origin", "")
                price = c.get("price_segment", "")
                channel = c.get("channel", "")
                conf = c.get("confidence", "")
                report += f"| {brand} | {origin} | {price} | {channel} | 🟡{conf} | {c.get('data_source', '')} |\n"
            report += "\n"

        # 市场份额估算
        report += "### 📊 市场份额估算（基于搜索/电商数据推算）\n\n"
        report += "| 品牌 | 估算份额 | 定位 | 备注 |\n"
        report += "|-----|---------|------|------|\n"

        # 按mentions估算份额
        total = sum(c.get("mentions", 1) for c in competitors)
        if total == 0:
            total = len(competitors)

        for c in sorted(competitors, key=lambda x: x.get("mentions", 0), reverse=True)[:10]:
            share = (c.get("mentions", 1) / total * 100) if total > 0 else 0
            report += f"| {c['brand']} | ~{share:.1f}% | {c.get('position','')} | {c.get('data_source','')} |\n"

        report += "\n_⚠️ 以上份额为基于电商搜索数据的估算，非官方统计_\n\n"

        # 进入建议
        report += "### 💡 竞争策略建议\n\n"
        report += "- 高端市场由Abbott/Roche等国际品牌主导，准入门槛高\n"
        report += "- 中端市场（2000-4000 RUB）竞争激烈，需差异化竞争\n"
        report += "- 大众/低端市场价格敏感，适合走量\n"
        report += "- 建议关注Wildberries/Ozon等电商平台的TOP榜单寻找市场空白\n"

        return report

    def export_competitor_matrix(self, output_path=None):
        """导出竞争者矩阵为JSON"""
        if output_path is None:
            output_path = f"competitor_matrix_{datetime.now().strftime('%Y%m%d')}.json"
        data = {
            "export_time": datetime.now().isoformat(),
            "country": self.country,
            "total_competitors": len(self.competitors),
            "competitors": self.competitors,
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"竞争者矩阵已保存: {output_path}")
        return output_path


if __name__ == "__main__":
    analyzer = CompetitorAnalyzer(country="俄罗斯", lang="ru")
    keywords = {"ru": ["глюкометр", "измеритель глюкозы"], "en": ["blood glucose meter"]}
    brands = ["Abbott", "Roche", "Omron", "Johnson & Johnson", "Medtronic", "Элта", "Сателлит"]
    competitors = analyzer.analyze_from_search(keywords, brand_keywords=brands)
    print(f"\n分析了 {len(competitors)} 个竞争者:")
    for c in competitors[:5]:
        print(f"  {c['brand']} | {c['origin']} | {c['position']} | {c['price_segment']}")
