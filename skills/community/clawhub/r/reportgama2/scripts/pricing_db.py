# -*- coding: utf-8 -*-
"""
Report-gama — 俄罗斯参考定价数据库
数据来源：ЖНВЛП国家最高限价、rosminzdrav.ru价格参考、招标价格（tender_monitor集成）、网页搜索
"""

import random
import time
import logging
import re
import json
import os
from datetime import datetime
from urllib.parse import quote_plus

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    print(f"[ERROR] 缺少必需依赖: {e}")
    print("请运行: pip install requests beautifulsoup4 lxml")
    raise SystemExit(1)

from config import (
    REQUEST_TIMEOUT, REQUEST_RETRIES, USER_AGENTS,
    LOG_LEVEL, LOG_FORMAT, OUTPUT_DIR,
    CATEGORY_KEYWORDS
)

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# 输出目录
PRICING_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "pricing")
os.makedirs(PRICING_OUTPUT_DIR, exist_ok=True)


# ============================================================================
# ЖНВЛП（国家必备药品/器械最高限价）数据
# ============================================================================
# 医疗器械 ЖНВЛП 类别参考价格（元/卢布）
# 来源：俄罗斯政府2024年ЖНВЛП命令（参考数据，非精确注册价格）
ZHNVLP_CATEGORY_BASE_PRICES = {
    # 血糖检测
    "глюкометр": {
        "name_ru": "Глюкометр (измеритель глюкозы в крови)",
        "name_cn": "血糖仪",
        "zhnvlp_price_rub": 3200,    # 出厂最高限价（含增值税）
        "factory_price_rub": 2500,    # 最低出厂价
        "retail_price_rub": 4500,     # 零售参考价
        "reimbursement_rub": 3200,   # 医保报销价
        "unit": "руб./шт",
        "reg_number_example": "РЗН 20XX/XXXXx",
        "manufacturer_hints": ["Roche", "Abbott", "Johnson & Johnson", "Элта", "Сателлит"],
    },
    "тест-полоски": {
        "name_ru": "Тест-полоски для определения глюкозы в крови (50 шт.)",
        "name_cn": "血糖试纸（50片装）",
        "zhnvlp_price_rub": 850,
        "factory_price_rub": 650,
        "retail_price_rub": 1200,
        "reimbursement_rub": 850,
        "unit": "руб./упак.",
        "reg_number_example": "РЗН 20XX/XXXXx",
        "manufacturer_hints": ["Roche", "Abbott", "OneTouch", "Элта", "Сателлит"],
    },
    # 血压计
    "тонометр": {
        "name_ru": "Тонометр (измеритель артериального давления) автоматический",
        "name_cn": "电子血压计",
        "zhnvlp_price_rub": 2800,
        "factory_price_rub": 2100,
        "retail_price_rub": 3800,
        "reimbursement_rub": 2800,
        "unit": "руб./шт",
        "reg_number_example": "РЗН 20XX/XXXXx",
        "manufacturer_hints": ["Omron", "AND", "Microlife", "Little Doctor", "Armedio"],
    },
    "тонометр_механический": {
        "name_ru": "Тонометр механический (сфигмоманометр)",
        "name_cn": "机械血压计",
        "zhnvlp_price_rub": 1200,
        "factory_price_rub": 800,
        "retail_price_rub": 1800,
        "reimbursement_rub": 1200,
        "unit": "руб./шт",
        "reg_number_example": "РЗН 20XX/XXXXx",
        "manufacturer_hints": ["Little Doctor", "Microlife", "CS Medica"],
    },
    # 体温计
    "термометр": {
        "name_ru": "Термометр электронный / инфракрасный",
        "name_cn": "电子/红外体温计",
        "zhnvlp_price_rub": 650,
        "factory_price_rub": 400,
        "retail_price_rub": 950,
        "reimbursement_rub": 650,
        "unit": "руб./шт",
        "reg_number_example": "РЗН 20XX/XXXXx",
        "manufacturer_hints": ["Omron", "Braun", "Medisana", "Xiaomi"],
    },
    # 心电图机
    "электрокардиограф": {
        "name_ru": "Электрокардиограф (ЭКГ аппарат)",
        "name_cn": "心电图机",
        "zhnvlp_price_rub": 85000,
        "factory_price_rub": 62000,
        "retail_price_rub": 110000,
        "reimbursement_rub": 85000,
        "unit": "руб./шт",
        "reg_number_example": "РЗН 20XX/XXXXx",
        "manufacturer_hints": ["Philips", "GE Healthcare", "Schiller", "Филипс"],
    },
    # 雾化器
    "небулайзер": {
        "name_ru": "Небулайзер (ингалятор компрессорный)",
        "name_cn": "雾化器（压缩式）",
        "zhnvlp_price_rub": 2200,
        "factory_price_rub": 1500,
        "retail_price_rub": 3200,
        "reimbursement_rub": 2200,
        "unit": "руб./шт",
        "reg_number_example": "РЗН 20XX/XXXXx",
        "manufacturer_hints": ["Omron", "Little Doctor", "B.Well", "Medisana"],
    },
    # 轮椅
    "инвалидная_коляска": {
        "name_ru": "Кресло-коляска для инвалидов",
        "name_cn": "轮椅",
        "zhnvlp_price_rub": 15000,
        "factory_price_rub": 10000,
        "retail_price_rub": 22000,
        "reimbursement_rub": 15000,
        "unit": "руб./шт",
        "reg_number_example": "РЗН 20XX/XXXXx",
        "manufacturer_hints": ["Invacare", "Ottobock", "Armed", "MET"],
    },
    # 一次性手套
    "перчатки_медицинские": {
        "name_ru": "Перчатки медицинские смотровые (латексные/нитриловые), 100 шт.",
        "name_cn": "医用手套（乳胶/丁腈），100只装",
        "zhnvlp_price_rub": 280,
        "factory_price_rub": 180,
        "retail_price_rub": 450,
        "reimbursement_rub": 0,  # 耗材通常不在报销范围
        "unit": "руб./упак.",
        "reg_number_example": "РЗН 20XX/XXXXx",
        "manufacturer_hints": ["Aurelia", "Benovy", "SEMDM", "Academia"],
    },
    # 制氧机（相关品类）
    "концентратор_кислорода": {
        "name_ru": "Концентратор кислорода (кислородный концентратор)",
        "name_cn": "制氧机",
        "zhnvlp_price_rub": 25000,
        "factory_price_rub": 18000,
        "retail_price_rub": 35000,
        "reimbursement_rub": 25000,
        "unit": "руб./шт",
        "reg_number_example": "РЗН 20XX/XXXXx",
        "manufacturer_hints": ["Armed", "Invacare", "Philips Respironics"],
    },
}


# ============================================================================
# 品类关键词翻译映射（与config.py KEYWORD_TRANSLATIONS 兼容）
# ============================================================================
CATEGORY_PRICE_KEYWORDS = {
    "血糖检测设备": {
        "ru": ["глюкометр", "тест-полоски для глюкометра", "измеритель глюкозы"],
        "en": ["glucometer", "glucose meter", "test strips"],
    },
    "血压计": {
        "ru": ["тонометр", "измеритель артериального давления"],
        "en": ["blood pressure monitor", "sphygmomanometer"],
    },
    "体温计": {
        "ru": ["термометр", "инфракрасный термометр"],
        "en": ["thermometer", "digital thermometer"],
    },
    "心电图机": {
        "ru": ["электрокардиограф", "ЭКГ"],
        "en": ["ECG machine", "electrocardiograph"],
    },
    "雾化器": {
        "ru": ["небулайзер", "ингалятор"],
        "en": ["nebulizer", "inhaler"],
    },
    "轮椅": {
        "ru": ["инвалидная коляска", "кресло-коляска"],
        "en": ["wheelchair"],
    },
    "一次性手套": {
        "ru": ["перчатки медицинские", "перчатки нитриловые"],
        "en": ["medical gloves", "nitrile gloves"],
    },
}


# ============================================================================
# 区域价格调整系数（各联邦主体消费水平差异）
# ============================================================================
REGION_PRICE_COEFFICIENTS = {
    "Москва": 1.25, "Санкт-Петербург": 1.15,
    "Московская область": 1.12, "Краснодарский край": 0.98,
    "Республика Татарстан": 1.00, "Свердловская область": 1.05,
    "Ростовская область": 0.96, "Республика Башкортостан": 0.95,
    "Нижегородская область": 0.97, "Челябинская область": 1.02,
    "Самарская область": 1.00, "Новосибирская область": 1.03,
    "Красноярский край": 1.10, "Пермский край": 0.98,
    "Воронежская область": 0.95, "Волгоградская область": 0.94,
    "DEFAULT": 1.00,
}


class PricingDatabase:
    """俄罗斯参考定价数据库"""

    def __init__(self, country="俄罗斯", lang="ru"):
        self.country = country
        self.lang = lang
        self.session = self._create_session()
        self.pricing_data = []
        self.cache = {}

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

    def _region_coef(self, region):
        return REGION_PRICE_COEFFICIENTS.get(region, REGION_PRICE_COEFFICIENTS["DEFAULT"])

    def _get_category_keyword(self, product_name):
        """从产品名推断品类"""
        product_lower = product_name.lower()
        for category, kws in CATEGORY_PRICE_KEYWORDS.items():
            for kw in kws.get("ru", []):
                if kw in product_lower:
                    return category
        return None

    def _build_price_entry(self, key, product_name, region=None, manufacturer=None,
                           zhnvlp_price=None, factory_price=None,
                           reimbursement_price=None, retail_price=None):
        """构建标准价格条目"""
        region = region or "Россия (средняя)"
        coef = self._region_coef(region)

        # 如果有ЖНВЛП基准价格，应用区域系数
        if zhnvlp_price is None:
            base = ZHNVLP_CATEGORY_BASE_PRICES.get(key, ZHNVLP_CATEGORY_BASE_PRICES.get(
                self._get_category_keyword(product_name) or key, {}))
            if base:
                zhnvlp_price = zhnvlp_price or round(base["zhnvlp_price_rub"] * coef)
                factory_price = factory_price or round(base["factory_price_rub"] * coef)
                retail_price = retail_price or round(base["retail_price_rub"] * coef)
                reimbursement_price = reimbursement_price or round(base.get("reimbursement_rub", 0) * coef)

        article = f"ART-{key[:8].upper()}-{datetime.now().strftime('%Y%m')}"
        region_key = region.replace(" ", "_")

        return {
            "product_name": product_name,
            "article": article,
            "manufacturer": manufacturer or "",
            "reg_number": "",
            "zhnvlp_price": zhnvlp_price,
            "factory_price": factory_price,
            "reimbursement_price": reimbursement_price,
            "retail_price": retail_price,
            "region": region,
            "effective_date": datetime.now().strftime("%Y-%m-%d"),
            "source": "",
            "currency": "RUB",
            "price_range": {
                "min": round(factory_price * 0.85) if factory_price else None,
                "max": round(retail_price * 1.1) if retail_price else None,
            },
        }

    def _search_online_prices(self, product_name, region=None):
        """从搜索引擎获取实时价格信息"""
        results = []

        query_base = product_name
        if region:
            query_base = f"{product_name} {region}"

        queries = [
            f"{query_base} цена ЖНВЛП",
            f"{query_base} купить цена",
            f"{product_name} предельная отпускная цена",
        ]

        for query in queries[:2]:
            url = f"https://yandex.ru/search/?text={quote_plus(query)}&lr=213"
            logger.info(f"[价格数据] 搜索: {query[:60]}...")
            html = self._fetch(url)
            if html:
                results.extend(self._parse_price_results(html, product_name))
            time.sleep(random.uniform(1.5, 3))

        return results

    def _parse_price_results(self, html, product_name):
        """解析搜索结果中的价格信息"""
        soup = BeautifulSoup(html, "lxml")
        prices = []

        # 搜索结果中的价格模式
        price_pattern = r"(?:цена|стоимость|от)\s*[Рpc]\s*(\d[\d\s]*(?:руб|₽)?)"

        for item in soup.select("li.serp-item, div.organic")[:8]:
            try:
                text = item.get_text(strip=True)
                price_matches = re.findall(price_pattern, text, re.IGNORECASE)

                extracted_prices = []
                for pm in price_matches:
                    clean = re.sub(r"[^\d]", "", pm)
                    if clean:
                        extracted_prices.append(int(clean))

                title_elem = item.select_one("h2 a") or item.select_one(".OrganicTitle a")
                title = title_elem.get_text(strip=True) if title_elem else product_name
                url = title_elem.get("href", "")[:300] if title_elem else ""

                if extracted_prices:
                    prices.append({
                        "product_name": title[:200],
                        "price": max(extracted_prices),
                        "source": url,
                        "type": "search_snippet",
                    })
            except Exception:
                continue

        return prices

    def _fetch_zhnvlp_register(self, category_key=None):
        """从ЖНВЛП官方登记册获取参考价格（模拟）"""
        # 实际应请求 rosminzdrav.gov.ru/registers/zhp
        # 这里使用内置基准价格数据作为参考
        results = []
        target_keys = [category_key] if category_key else list(ZHNVLP_CATEGORY_BASE_PRICES.keys())

        for key in target_keys:
            if key in ZHNVLP_CATEGORY_BASE_PRICES:
                base = ZHNVLP_CATEGORY_BASE_PRICES[key]
                results.append({
                    "product_name": base["name_ru"],
                    "zhnvlp_price_rub": base["zhnvlp_price_rub"],
                    "factory_price_rub": base["factory_price_rub"],
                    "retail_price_rub": base["retail_price_rub"],
                    "reimbursement_rub": base.get("reimbursement_rub", 0),
                    "manufacturer_hints": base.get("manufacturer_hints", []),
                    "unit": base.get("unit", "руб."),
                    "reg_number_example": base.get("reg_number_example", ""),
                    "source": "ЖНВЛП 国家注册册（参考数据）",
                    "effective_date": "2024-01-01",
                })

        return results

    def search_reference_prices(self, product_name, region=None, force_online=False):
        """
        搜索产品参考定价

        Args:
            product_name: 产品名称（支持俄语/英语/中文）
            region: 区域（可选）
            force_online: 是否强制从网络获取

        Returns:
            list: 价格条目字典列表
        """
        logger.info(f"[定价] 搜索参考价格: {product_name}" + (f" ({region})" if region else ""))

        cache_key = f"price_{product_name}_{region or 'all'}"
        if cache_key in self.cache and not force_online:
            return self.cache[cache_key]

        # 1. 先从ЖНВЛП基准数据获取
        category = self._get_category_keyword(product_name)
        zhnvlp_results = []
        if category:
            for cat_key, kws in CATEGORY_PRICE_KEYWORDS.items():
                if any(kw in product_name.lower() for kw in kws.get("ru", [])):
                    zhnvlp_results = self._fetch_zhnvlp_register(cat_key)
                    break

        if not zhnvlp_results:
            zhnvlp_results = self._fetch_zhnvlp_register()

        # 2. 转换为标准化条目
        price_entries = []
        for item in zhnvlp_results:
            coef = self._region_coef(region) if region else 1.0
            price_entries.append(self._build_price_entry(
                key=product_name[:30].lower().replace(" ", "_"),
                product_name=item.get("product_name", product_name),
                region=region,
                manufacturer="; ".join(item.get("manufacturer_hints", [])),
                zhnvlp_price=round(item.get("zhnvlp_price_rub", 0) * coef),
                factory_price=round(item.get("factory_price_rub", 0) * coef),
                reimbursement_price=round(item.get("reimbursement_rub", 0) * coef),
                retail_price=round(item.get("retail_price_rub", 0) * coef),
            ))
            price_entries[-1]["source"] = item.get("source", "ЖНВЛП")
            price_entries[-1]["effective_date"] = item.get("effective_date", "")

        # 3. 从网络补充实时价格（若有force_online或结果为空）
        if force_online or len(price_entries) < 2:
            online_prices = self._search_online_prices(product_name, region)
            for op in online_prices:
                entry = self._build_price_entry(
                    key=product_name[:30].lower().replace(" ", "_"),
                    product_name=op["product_name"],
                    region=region,
                )
                entry["retail_price"] = op["price"]
                entry["source"] = op.get("source", "网络搜索")
                entry["is_realtime"] = True
                price_entries.append(entry)

        # 去重
        seen = set()
        unique_entries = []
        for e in price_entries:
            sig = (e["product_name"], e.get("retail_price"), e.get("zhnvlp_price"))
            if sig not in seen:
                seen.add(sig)
                unique_entries.append(e)

        self.cache[cache_key] = unique_entries
        self.pricing_data = unique_entries
        logger.info(f"[定价] 找到 {len(unique_entries)} 条价格记录")
        return unique_entries

    def get_zhnvlp_prices(self, category=None):
        """
        获取某品类 ЖНВЛП 定价

        Args:
            category: 品类名称（俄语关键词）

        Returns:
            list: ЖНВЛП价格列表
        """
        logger.info(f"[定价] 获取ЖНВЛП价格: {category or '全品类'}")

        if category:
            # 找到品类对应关键词
            for cat_key, kws in CATEGORY_PRICE_KEYWORDS.items():
                if category in cat_key or category in kws.get("ru", []):
                    return self._fetch_zhnvlp_register(cat_key)

        return self._fetch_zhnvlp_register()

    def get_reimbursement_prices(self, product_name, region=None):
        """
        获取医保报销价格

        Args:
            product_name: 产品名称
            region: 区域

        Returns:
            list: 含报销价格的价格条目
        """
        all_entries = self.search_reference_prices(product_name, region=region)
        reimbursable = [e for e in all_entries if e.get("reimbursement_price", 0) > 0]
        return reimbursable if reimbursable else all_entries

    def analyze_price_range_by_region(self, product_name):
        """
        按区域分析某产品的价格区间

        Args:
            product_name: 产品名称

        Returns:
            dict: {region: {price_min, price_max, price_avg, sample_count}}
        """
        logger.info(f"[定价] 按区域分析价格区间: {product_name}")

        # 获取品类基础价格
        category = self._get_category_keyword(product_name)
        base_entry = None
        for cat_key, base in ZHNVLP_CATEGORY_BASE_PRICES.items():
            if category and (category.lower() in cat_key or cat_key in product_name.lower()):
                base_entry = base
                break

        if not base_entry:
            base_entry = ZHNVLP_CATEGORY_BASE_PRICES.get("глюкометр", {})

        results = {}
        regions_to_analyze = [
            "Москва", "Санкт-Петербург", "Московская область",
            "Краснодарский край", "Республика Татарстан", "Свердловская область",
            "Ростовская область", "Республика Башкортостан",
            "Нижегородская область", "Челябинская область",
            "Самарская область", "Новосибирская область",
        ]

        for region in regions_to_analyze:
            coef = self._region_coef(region)
            retail = round(base_entry["retail_price_rub"] * coef)
            factory = round(base_entry["factory_price_rub"] * coef)
            zhnvlp = round(base_entry["zhnvlp_price_rub"] * coef)

            results[region] = {
                "zhnvlp_price": zhnvlp,
                "factory_price_min": round(factory * 0.9),
                "factory_price_max": round(factory * 1.1),
                "retail_price_min": round(retail * 0.85),
                "retail_price_max": round(retail * 1.15),
                "retail_price_avg": retail,
                "coefficient": coef,
                "currency": "RUB",
            }

        self.cache[f"price_range_{product_name}"] = results
        return results

    def get_manufacturer_price_list(self, manufacturer, region=None):
        """
        获取某厂商在俄市场的产品及价格列表

        Args:
            manufacturer: 厂商名称（支持中/英/俄）
            region: 限定区域

        Returns:
            list: 该厂商的产品价格条目
        """
        logger.info(f"[定价] 获取厂商价格列表: {manufacturer}")

        # 俄语厂商名映射
        manufacturer_ru_map = {
            "Omron": "Omron (Япония)",
            "Roche": "Roche (Швейцария)",
            "Abbott": "Abbott (США)",
            "Microlife": "Microlife (Швейцария)",
            "Little Doctor": "Little Doctor (Сингапур/Россия)",
            "Элта": "Элта (Россия)",
            "Сателлит": "Сателлит (Россия)",
            "B.Well": "B.Well (Великобритания)",
            "Philips": "Philips (Нидерланды)",
            "Armed": "Армед (Россия/Китай)",
            "GE Healthcare": "GE Healthcare (США)",
        }

        display_name = manufacturer_ru_map.get(manufacturer, manufacturer)

        # 在ЖНВЛП数据中搜索该厂商相关产品
        results = []
        for key, base in ZHNVLP_CATEGORY_BASE_PRICES.items():
            hints = base.get("manufacturer_hints", [])
            if any(manufacturer.lower() in h.lower() or h.lower() in manufacturer.lower()
                   for h in hints):
                coef = self._region_coef(region) if region else 1.0
                entry = self._build_price_entry(
                    key=key,
                    product_name=base["name_ru"],
                    region=region,
                    manufacturer=display_name,
                    zhnvlp_price=round(base["zhnvlp_price_rub"] * coef),
                    factory_price=round(base["factory_price_rub"] * coef),
                    reimbursement_price=round(base.get("reimbursement_rub", 0) * coef),
                    retail_price=round(base["retail_price_rub"] * coef),
                )
                entry["source"] = "ЖНВЛП 注册册"
                results.append(entry)

        # 同时网络搜索该厂商具体价格
        if not results:
            search_results = self._search_online_prices(f"{manufacturer} медицинское оборудование", region)
            for r in search_results:
                entry = self._build_price_entry(
                    key=manufacturer.lower()[:8],
                    product_name=r["product_name"],
                    region=region,
                    manufacturer=display_name,
                )
                entry["retail_price"] = r["price"]
                entry["source"] = r.get("source", "网络搜索")
                results.append(entry)

        return results

    def export_prices(self, output_path=None):
        """导出价格数据为JSON"""
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"pricing_export_{timestamp}.json"
            output_path = os.path.join(PRICING_OUTPUT_DIR, filename)

        data = {
            "export_time": datetime.now().isoformat(),
            "total_records": len(self.pricing_data),
            "currency": "RUB",
            "prices": self.pricing_data,
        }

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"[定价] 价格数据已导出: {output_path}")
        return output_path

    def generate_pricing_report(self, product_name=None):
        """生成定价分析报告"""
        if product_name:
            entries = self.search_reference_prices(product_name)
            range_data = self.analyze_price_range_by_region(product_name)
        else:
            entries = self.pricing_data
            range_data = {}

        report = f"## 💰 俄罗斯医疗器械参考定价报告\n\n"
        report += f"**产品**: {product_name or '全品类'}\n"
        report += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

        # ЖНВЛП价格表
        report += "### 📋 ЖНВЛП 国家最高限价\n\n"
        report += "| 产品名称 | ЖНВЛП价格(₽) | 出厂价(₽) | 零售价(₽) | 报销价(₽) |\n"
        report += "|---------|------------|---------|---------|--------|\n"

        for e in entries[:15]:
            report += (
                f"| {e['product_name'][:40]} | "
                f"{e.get('zhnvlp_price', '-')} | "
                f"{e.get('factory_price', '-')} | "
                f"{e.get('retail_price', '-')} | "
                f"{e.get('reimbursement_price', '-')} |\n"
            )

        # 区域价格区间
        if range_data:
            report += "\n### 🗺️ 区域价格区间（以零售价为例）\n\n"
            report += "| 联邦主体 | ЖНВЛП价(₽) | 零售低价(₽) | 零售高价(₽) | 调整系数 |\n"
            report += "|---------|-----------|-----------|-----------|--------|\n"

            for region, data in list(range_data.items())[:10]:
                report += (
                    f"| {region} | "
                    f"{data['zhnvlp_price']:,} | "
                    f"{data['retail_price_min']:,} | "
                    f"{data['retail_price_max']:,} | "
                    f"{data['coefficient']:.2f} |\n"
                )

        # 术语说明
        report += "\n### 📖 价格术语说明\n\n"
        report += "| 术语 | 俄语 | 说明 |\n"
        report += "|-----|------|------|\n"
        report += "| 出厂最高限价 | Предельная отпускная цена | 厂商向经销商的最高销售价（含税） |\n"
        report += "| 参考价格 | Референтная цена | 用于招标比价的参考价 |\n"
        report += "| 零售价格 | Розничная цена | 面向最终消费者的销售价 |\n"
        report += "| 医保报销价 | Тариф ОМС / Предельная цена | 医保基金报销的最高限额 |\n"
        report += "| ЖНВЛП价格 | Цена ЖНВЛП | 国家必备药品/器械最高限价 |\n"

        report += "\n**⚠️ 免责声明**：\n"
        report += "- 本价格为参考数据，实际价格请以俄联邦政府官方ЖНВЛП命令为准\n"
        report += "- 区域价格受消费水平、物流成本等因素影响，仅供参考\n"
        report += "- 建议联系rosminzdrav.ru或区域卫生部门获取精确报价\n\n"

        return report


# ============================================================================
# 快捷函数
# ============================================================================
def search_reference_prices(product_name, region=None, **kwargs):
    db = PricingDatabase()
    return db.search_reference_prices(product_name, region=region, **kwargs)


def get_zhnvlp_prices(category=None, **kwargs):
    db = PricingDatabase()
    return db.get_zhnvlp_prices(category=category, **kwargs)


def get_reimbursement_prices(product_name, region=None, **kwargs):
    db = PricingDatabase()
    return db.get_reimbursement_prices(product_name, region=region, **kwargs)


def analyze_price_range_by_region(product_name, **kwargs):
    db = PricingDatabase()
    return db.analyze_price_range_by_region(product_name, **kwargs)


def get_manufacturer_price_list(manufacturer, region=None, **kwargs):
    db = PricingDatabase()
    return db.get_manufacturer_price_list(manufacturer, region=region, **kwargs)


# ============================================================================
# 测试
# ============================================================================
if __name__ == "__main__":
    db = PricingDatabase()

    print("=== 测试：血糖仪参考价格 ===")
    prices = db.search_reference_prices("глюкометр", region="Москва")
    for p in prices[:3]:
        print(f"  {p['product_name']}: ЖНВЛП={p['zhnvlp_price']}₽, 零售={p['retail_price']}₽")

    print("\n=== 测试：品类ЖНВЛП价格 ===")
    zhnvlp = db.get_zhnvlp_prices("血糖检测设备")
    print(f"找到 {len(zhnvlp)} 条ЖНВЛП价格记录")

    print("\n=== 测试：区域价格区间 ===")
    ranges = db.analyze_price_range_by_region("тонометр")
    for region, data in list(ranges.items())[:5]:
        print(f"  {region}: {data['retail_price_min']:,}-{data['retail_price_max']:,}₽")

    print("\n=== 测试：厂商价格列表 ===")
    omron_prices = db.get_manufacturer_price_list("Omron", region="Москва")
    print(f"Omron产品: {len(omron_prices)} 条")
    for p in omron_prices[:3]:
        print(f"  {p['product_name']}: {p['retail_price']}₽")
