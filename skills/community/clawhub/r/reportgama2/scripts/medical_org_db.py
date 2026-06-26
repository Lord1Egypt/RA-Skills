# -*- coding: utf-8 -*-
"""
Report-gama — 俄罗斯医疗机构分布数据库
数据来源：rosminzdrav.ru、rmis.ru、各联邦主体卫生部门目录、网页搜索
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
    LOG_LEVEL, LOG_FORMAT, OUTPUT_DIR
)

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# 输出目录
MEDICAL_ORGS_OUTPUT_DIR = os.path.join(OUTPUT_DIR, "medical_orgs")
os.makedirs(MEDICAL_ORGS_OUTPUT_DIR, exist_ok=True)


# ============================================================================
# 俄联邦85个联邦主体完整列表（含联邦区划分）
# ============================================================================
RUSSIAN_FEDERAL_SUBJECTS = {
    "Центральный федеральный округ": [
        "Белгородская область", "Брянская область", "Владимирская область",
        "Воронежская область", "Ивановская область", "Калужская область",
        "Костромская область", "Курская область", "Липецкая область",
        "Московская область", "Орловская область", "Рязанская область",
        "Смоленская область", "Тамбовская область", "Тверская область",
        "Тульская область", "Ярославская область", "Москва",
    ],
    "Северо-Западный федеральный округ": [
        "Республика Карелия", "Республика Коми", "Архангельская область",
        "Ненецкий автономный округ", "Вологодская область",
        "Калининградская область", "Ленинградская область",
        "Мурманская область", "Новгородская область", "Псковская область",
        "Санкт-Петербург",
    ],
    "Южный федеральный округ": [
        "Республика Адыгея", "Республика Калмыкия", "Краснодарский край",
        "Астраханская область", "Волгоградская область", "Ростовская область",
        "Севастополь",
    ],
    "Северо-Кавказский федеральный округ": [
        "Республика Дагестан", "Республика Ингушетия",
        "Кабардино-Балкарская Республика", "Карачаево-Черкесская Республика",
        "Республика Северная Осетия — Алания",
        "Ставропольский край", "Чеченская Республика",
    ],
    "Приволжский федеральный округ": [
        "Республика Башкортостан", "Республика Марий Эл",
        "Республика Мордовия", "Республика Татарстан", "Удмуртская Республика",
        "Чувашская Республика", "Пермский край", "Кировская область",
        "Нижегородская область", "Оренбургская область", "Пензенская область",
        "Самарская область", "Саратовская область", "Ульяновская область",
    ],
    "Уральский федеральный округ": [
        "Курганская область", "Свердловская область", "Тюменская область",
        "Ханты-Мансийский автономный округ — Югра",
        "Ямало-Ненецкий автономный округ", "Челябинская область",
    ],
    "Сибирский федеральный округ": [
        "Республика Алтай", "Республика Бурятия", "Республика Тыва",
        "Республика Хакасия", "Алтайский край", "Забайкальский край",
        "Красноярский край", "Иркутская область", "Кемеровская область",
        "Новосибирская область", "Омская область", "Томская область",
    ],
    "Дальневосточный федеральный округ": [
        "Республика Саха (Якутия)", "Камчатский край", "Приморский край",
        "Хабаровский край", "Амурская область", "Магаданская область",
        "Сахалинская область", "Еврейская автономная область",
        "Чукотский автономный округ",
    ],
    # Крымский федеральный округ (合并到 Южный)
    "Крымский федеральный округ": [
        "Республика Крым", "Севастополь",
    ],
}

# 展平为单层 dict
ALL_FEDERAL_SUBJECTS = {}
for district, subjects in RUSSIAN_FEDERAL_SUBJECTS.items():
    for subj in subjects:
        # 修正字符串拼接问题
        subj_clean = subj.strip().strip('"')
        ALL_FEDERAL_SUBJECTS[subj_clean] = district

# 快速查找表（名称简写 → 全称）
SUBJECT_ALIASES = {
    "москва": "Москва",
    "мос": "Москва",
    "спб": "Санкт-Петербург",
    "питер": "Санкт-Петербург",
    "мособласть": "Московская область",
    "московская": "Московская область",
    "краснодарский": "Краснодарский край",
    "краснодар": "Краснодарский край",
    "татарстан": "Республика Татарстан",
    "казань": "Республика Татарстан",
    "свердловская": "Свердловская область",
    "екатеринбург": "Свердловская область",
    "ростовская": "Ростовская область",
    "ростов": "Ростовская область",
    "новосибирская": "Новосибирская область",
    "новосибирск": "Новосибирская область",
    "челябинская": "Челябинская область",
    "челябинск": "Челябинская область",
    "самарская": "Самарская область",
    "самара": "Самарская область",
    "нижегородская": "Нижегородская область",
    "нижний": "Нижегородская область",
    "воронежская": "Воронежская область",
    "воронеж": "Воронежская область",
    "пермская": "Пермский край",
    "пермь": "Пермский край",
}


# ============================================================================
# 机构类型定义
# ============================================================================
ORG_TYPES = {
    "больница": {
        "name_ru": "Больница",
        "name_cn": "医院",
        "search_kws": ["больница", "госпиталь", "стационар"],
    },
    "поликлиника": {
        "name_ru": "Поликлиника",
        "name_cn": "诊所/门诊部",
        "search_kws": ["поликлиника", "амбулатория", "клиника"],
    },
    "специализированный_центр": {
        "name_ru": "Специализированный центр",
        "name_cn": "专科中心",
        "search_kws": ["центр", "специализированный центр", "медицинский центр"],
    },
    "диагностический_центр": {
        "name_ru": "Диагностический центр",
        "name_cn": "诊断中心",
        "search_kws": ["диагностический центр", "лаборатория", "диагностика"],
    },
    "аптека": {
        "name_ru": "Аптека",
        "name_cn": "药房",
        "search_kws": ["аптека", "аптечный пункт", "аптечная сеть"],
    },
    "реабилитационный_центр": {
        "name_ru": "Реабилитационный центр",
        "name_cn": "康复中心",
        "search_kws": ["реабилитационный центр", "реабилитация"],
    },
    "гериатрический_центр": {
        "name_ru": "Гериатрический центр",
        "name_cn": "老年医学中心",
        "search_kws": ["гериатрический", "гериатрия", "пансионат для пожилых"],
    },
    "скорая_помощь": {
        "name_ru": "Станция скорой медицинской помощи",
        "name_cn": "急救站",
        "search_kws": ["скорая помощь", "станция скорой"],
    },
}

# 品类关键词 → 相关机构类型映射
CATEGORY_TO_ORG_TYPES = {
    "血糖检测设备": ["больница", "поликлиника", "диагностический_центр", "аптека"],
    "血压计": ["больница", "поликлиника", "диагностический_центр"],
    "体温计": ["больница", "поликлиника"],
    "心电图机": ["больница", "диагностический_центр", "специализированный_центр"],
    "雾化器": ["больница", "поликлиника", "специализированный_центр"],
    "轮椅": ["реабилитационный_центр", "гериатрический_центр", "больница"],
    "一次性手套": ["больница", "поликлиника", "аптека"],
    "医疗器械": list(ORG_TYPES.keys()),
}


# ============================================================================
# 估算参数（基于公开数据）
# ============================================================================
REGION_HEALTHCARE_PARAMS = {
    # 区域 → {医院密度, 诊所密度, 每医院床位均数, 每诊所日门诊量}
    "Москва": {"hospitals_per_100k": 3.2, "clinics_per_100k": 18, "avg_beds": 450, "outpatient_per_day": 800},
    "Санкт-Петербург": {"hospitals_per_100k": 3.5, "clinics_per_100k": 16, "avg_beds": 380, "outpatient_per_day": 650},
    "Московская область": {"hospitals_per_100k": 2.4, "clinics_per_100k": 12, "avg_beds": 320, "outpatient_per_day": 500},
    "Краснодарский край": {"hospitals_per_100k": 3.8, "clinics_per_100k": 14, "avg_beds": 290, "outpatient_per_day": 480},
    "Республика Татарстан": {"hospitals_per_100k": 3.2, "clinics_per_100k": 13, "avg_beds": 310, "outpatient_per_day": 520},
    "Свердловская область": {"hospitals_per_100k": 3.0, "clinics_per_100k": 11, "avg_beds": 340, "outpatient_per_day": 550},
    "DEFAULT": {"hospitals_per_100k": 3.5, "clinics_per_100k": 10, "avg_beds": 250, "outpatient_per_day": 400},
}

REGION_POPULATION = {
    "Москва": 13_000_000, "Санкт-Петербург": 5_600_000,
    "Московская область": 7_800_000, "Краснодарский край": 5_800_000,
    "Республика Татарстан": 3_900_000, "Свердловская область": 4_200_000,
    "Ростовская область": 4_200_000, "Республика Башкортостан": 4_000_000,
    "Нижегородская область": 3_200_000, "Челябинская область": 3_500_000,
    "Самарская область": 3_200_000, "Новосибирская область": 2_800_000,
    "DEFAULT": 2_000_000,
}


class MedicalOrgDatabase:
    """俄罗斯医疗机构分布数据库"""

    def __init__(self, country="俄罗斯", lang="ru"):
        self.country = country
        self.lang = lang
        self.session = self._create_session()
        self.orgs_data = []
        self.distribution_cache = {}

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

    def _normalize_region(self, region_input):
        """将区域输入规范化为标准名称"""
        if region_input in ALL_FEDERAL_SUBJECTS:
            return region_input
        # 别名查找
        key = region_input.lower().strip()
        if key in SUBJECT_ALIASES:
            return SUBJECT_ALIASES[key]
        # 模糊匹配
        for name in ALL_FEDERAL_SUBJECTS:
            if region_input.lower() in name.lower():
                return name
        return region_input

    def _get_regional_data(self, region):
        """从网络获取某区域医疗机构数据"""
        region = self._normalize_region(region)
        results = []

        # 数据源1: rosminzdrav.ru 医疗机构目录
        search_queries = [
            f"{region} медицинские организации список",
            f"{region} больницы и поликлиники",
            f"site:rosminzdrav.ru {region} медицинские организации",
        ]

        for query in search_queries[:2]:
            url = f"https://yandex.ru/search/?text={quote_plus(query)}&lr=213"
            logger.info(f"[机构数据] 搜索: {query[:60]}...")
            html = self._fetch(url)
            if html:
                results.extend(self._parse_org_results(html, region))
            time.sleep(random.uniform(1.5, 3))

        return results

    def _parse_org_results(self, html, region):
        """解析搜索结果中的医疗机构信息"""
        soup = BeautifulSoup(html, "lxml")
        orgs = []

        for item in soup.select("li.serp-item, div.organic")[:10]:
            try:
                title_elem = item.select_one("h2 a") or item.select_one(".OrganicTitle a")
                if not title_elem:
                    continue

                name = title_elem.get_text(strip=True)
                url = title_elem.get("href", "")

                # 判断机构类型
                org_type = self._classify_org_type(name)

                # 提取地址（如果有）
                address_elem = item.select_one(".OrganicTextContentSpan") or item.select_one("div.snippet-tex")
                address = ""
                if address_elem:
                    addr_text = address_elem.get_text(strip=True)
                    addr_match = re.search(r"г\.\s*[А-Яа-яё\s]+.*?(?:ул\.|пр\.|ш\.)[^,]+", addr_text)
                    if addr_match:
                        address = addr_match.group(0)[:200]

                orgs.append({
                    "name": name[:200],
                    "type": org_type,
                    "address": address,
                    "region": region,
                    "district": ALL_FEDERAL_SUBJECTS.get(region, ""),
                    "beds": None,  # 网页搜索一般不提供床位数
                    "contact": "",
                    "source": url[:300] if url else "",
                    "fetch_time": datetime.now().isoformat(),
                })
            except Exception as e:
                logger.debug(f"解析条目失败: {e}")
                continue

        return orgs

    def _classify_org_type(self, name):
        """根据机构名称自动分类"""
        name_lower = name.lower()
        if any(kw in name_lower for kw in ["больница", "госпиталь", "клиническая"]):
            return "больница"
        elif any(kw in name_lower for kw in ["поликлиника", "амбулатория"]):
            return "поликлиника"
        elif any(kw in name_lower for kw in ["диагностический", "диагностика", "лаборатория"]):
            return "диагностический_центр"
        elif any(kw in name_lower for kw in ["аптека", "аптечный"]):
            return "аптека"
        elif any(kw in name_lower for kw in ["реабилитац"]):
            return "реабилитационный_центр"
        elif any(kw in name_lower for kw in ["гериатрич"]):
            return "гериатрический_центр"
        elif any(kw in name_lower for kw in ["скорая"]):
            return "скорая_помощь"
        elif any(kw in name_lower for kw in ["центр", "институт"]):
            return "специализированный_центр"
        return "специализированный_центр"

    def get_medical_orgs_by_region(self, region, force_refresh=False):
        """
        按联邦主体获取医疗机构列表

        Args:
            region: 联邦主体名称（如 "Москва", "Краснодарский край"）
            force_refresh: 是否强制刷新

        Returns:
            list: 医疗机构字典列表
        """
        region = self._normalize_region(region)
        cache_key = f"region_{region}"

        if not force_refresh and cache_key in self.distribution_cache:
            logger.info(f"[医疗机构] 使用缓存: {region}")
            return self.distribution_cache[cache_key]

        logger.info(f"[医疗机构] 获取 {region} 的医疗机构数据...")

        # 尝试从本地缓存读取
        cache_path = os.path.join(MEDICAL_ORGS_OUTPUT_DIR, f"orgs_{region.replace(' ', '_')}.json")
        if os.path.exists(cache_path) and not force_refresh:
            try:
                with open(cache_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data:
                    self.distribution_cache[cache_key] = data
                    return data
            except Exception:
                pass

        # 从网络获取
        orgs = self._get_regional_data(region)

        # 若无结果，生成估算数据（基于区域参数模型）
        if not orgs:
            logger.info(f"[医疗机构] 网络数据为空，为 {region} 生成估算机构列表...")
            orgs = self._generate_estimated_orgs(region)

        # 补充区域级别机构（主要医院名称）
        if len(orgs) < 5:
            orgs.extend(self._get_major_hospitals(region))

        self.distribution_cache[cache_key] = orgs
        self.orgs_data = orgs

        # 保存到本地
        self._save_to_file(orgs, region)

        return orgs

    def get_medical_orgs_by_type(self, org_type, region=None):
        """
        按机构类型获取医疗机构列表

        Args:
            org_type: 机构类型键（如 "больница", "аптека"）
            region: 可选，限定区域

        Returns:
            list: 医疗机构字典列表
        """
        logger.info(f"[医疗机构] 按类型筛选: {org_type}" + (f"（{region}）" if region else ""))

        all_orgs = []
        regions_to_search = [region] if region else list(ALL_FEDERAL_SUBJECTS.keys())[:10]

        for reg in regions_to_search:
            reg = self._normalize_region(reg)
            cache_key = f"region_{reg}"
            if cache_key in self.distribution_cache:
                orgs = self.distribution_cache[cache_key]
            else:
                orgs = self.get_medical_orgs_by_region(reg)
            all_orgs.extend(orgs)

        # 按类型过滤
        filtered = [o for o in all_orgs if o.get("type") == org_type]

        logger.info(f"[医疗机构] 找到 {org_type} 类型机构: {len(filtered)} 个")
        return filtered

    def get_org_distribution_by_region(self, category, top_n=20):
        """
        按区域统计某品类相关机构分布

        Args:
            category: 品类名称（如 "血糖检测设备"）
            top_n: 返回前N个区域

        Returns:
            dict: {region: count}
        """
        logger.info(f"[医疗机构] 统计品类 '{category}' 在各区域的机构分布...")

        category = category or "医疗器械"
        relevant_types = CATEGORY_TO_ORG_TYPES.get(category, CATEGORY_TO_ORG_TYPES["医疗器械"])

        distribution = {}
        major_regions = list(ALL_FEDERAL_SUBJECTS.keys())[:top_n]

        for region in major_regions:
            region = self._normalize_region(region)
            cache_key = f"region_{region}"
            if cache_key not in self.distribution_cache:
                self.get_medical_orgs_by_region(region)

            orgs = self.distribution_cache.get(cache_key, [])
            count = sum(1 for o in orgs if o.get("type") in relevant_types)
            if count > 0:
                distribution[region] = count

        # 按数量排序
        distribution = dict(sorted(distribution.items(), key=lambda x: x[1], reverse=True))
        self.distribution_cache["category_distribution"] = distribution
        return distribution

    def get_market_capacity(self, org_type, region):
        """
        估算某区域某类机构的市场容量

        Args:
            org_type: 机构类型
            region: 联邦主体名称

        Returns:
            dict: 市场容量估算
        """
        region = self._normalize_region(region)
        params = REGION_HEALTHCARE_PARAMS.get(region, REGION_HEALTHCARE_PARAMS["DEFAULT"])
        population = REGION_POPULATION.get(region, REGION_POPULATION["DEFAULT"])

        # 估算机构数量
        if org_type in ["больница"]:
            density = params["hospitals_per_100k"]
        elif org_type in ["поликлиника"]:
            density = params["clinics_per_100k"]
        elif org_type in ["аптека"]:
            density = params["clinics_per_100k"] * 2.5  # 药房密度通常是诊所的2.5倍
        elif org_type in ["диагностический_центр"]:
            density = params["hospitals_per_100k"] * 0.5
        elif org_type in ["реабилитационный_центр"]:
            density = params["hospitals_per_100k"] * 0.3
        else:
            density = params["hospitals_per_100k"]

        estimated_count = int(population / 100_000 * density)

        # 估算市场容量（设备需求）
        # 假设每家医院年均采购10-50万卢布设备，诊所年均5-15万
        if org_type == "больница":
            avg_annual_per_org_rub = 350_000  # 35万卢布
            avg_beds = params["avg_beds"]
        elif org_type == "поликлиника":
            avg_annual_per_org_rub = 100_000
            avg_beds = 0
        elif org_type == "аптека":
            avg_annual_per_org_rub = 50_000
            avg_beds = 0
        else:
            avg_annual_per_org_rub = 150_000
            avg_beds = 0

        total_capacity_rub = estimated_count * avg_annual_per_org_rub

        capacity = {
            "region": region,
            "org_type": org_type,
            "estimated_org_count": estimated_count,
            "population": population,
            "annual_market_capacity_rub": total_capacity_rub,
            "annual_market_capacity_usd": round(total_capacity_rub / 90, 0),  # 假设1USD=90RUB
            "avg_beds_per_org": params.get("avg_beds", 0) if org_type == "больница" else 0,
            "avg_annual_per_org_rub": avg_annual_per_org_rub,
            "unit": "RUB",
            "confidence": "medium",
            "note": "基于区域人口密度和机构配置标准估算，实际数据请参考rosminzdrav.ru官方统计",
            "estimate_date": datetime.now().strftime("%Y-%m-%d"),
        }
        return capacity

    def search_medical_orgs(self, keyword, region=None):
        """
        搜索特定医疗机构

        Args:
            keyword: 搜索关键词（如机构名称关键字、科室名、城市名）
            region: 限定区域

        Returns:
            list: 匹配机构列表
        """
        logger.info(f"[医疗机构] 搜索关键词: {keyword}" + (f" 限定区域: {region}" if region else ""))

        # 网络搜索
        query = keyword
        if region:
            query = f"{self._normalize_region(region)} {keyword}"
        query += " медицинская организация"

        url = f"https://yandex.ru/search/?text={quote_plus(query)}&lr=213"
        html = self._fetch(url)
        orgs = []
        if html:
            orgs = self._parse_org_results(html, region or "未指定区域")

        # 同时搜索本地已缓存数据
        local_matches = []
        for cache_key, cached_orgs in self.distribution_cache.items():
            if cache_key.startswith("region_"):
                for org in cached_orgs:
                    if keyword.lower() in org.get("name", "").lower():
                        local_matches.append(org)

        # 合并去重
        seen = set()
        combined = []
        for o in orgs + local_matches:
            if o["name"] not in seen:
                seen.add(o["name"])
                combined.append(o)

        logger.info(f"[医疗机构] 找到 {len(combined)} 个匹配结果")
        return combined

    def _generate_estimated_orgs(self, region):
        """当无网络数据时，基于统计参数生成估算机构列表"""
        params = REGION_HEALTHCARE_PARAMS.get(region, REGION_HEALTHCARE_PARAMS["DEFAULT"])
        population = REGION_POPULATION.get(region, REGION_POPULATION["DEFAULT"])

        hospitals_count = int(population / 100_000 * params["hospitals_per_100k"])
        clinics_count = int(population / 100_000 * params["clinics_per_100k"])

        orgs = []
        type_weights = [
            ("больница", min(hospitals_count, 10)),
            ("поликлиника", min(clinics_count, 20)),
            ("диагностический_центр", min(int(clinics_count * 0.3), 8)),
            ("аптека", min(int(clinics_count * 2.5), 30)),
            ("скорая_помощь", min(int(population / 500_000) + 1, 5)),
        ]

        for org_type, count in type_weights:
            for i in range(count):
                org_name = f"{ORG_TYPES[org_type]['name_ru']} №{i+1} ({region})"
                orgs.append({
                    "name": org_name,
                    "type": org_type,
                    "address": f"{region}",
                    "region": region,
                    "district": ALL_FEDERAL_SUBJECTS.get(region, ""),
                    "beds": params["avg_beds"] if org_type == "больница" else None,
                    "contact": "",
                    "source": "估算数据（基于区域医疗配置标准）",
                    "fetch_time": datetime.now().isoformat(),
                    "is_estimated": True,
                })

        return orgs

    def _get_major_hospitals(self, region):
        """获取主要医院名称（通过搜索）"""
        query = f"{region} крупные больницы названия"
        url = f"https://yandex.ru/search/?text={quote_plus(query)}&lr=213"
        html = self._fetch(url)
        if not html:
            return []

        soup = BeautifulSoup(html, "lxml")
        hospitals = []
        for item in soup.select("li.serp-item, div.organic")[:5]:
            title_elem = item.select_one("h2 a")
            if title_elem:
                name = title_elem.get_text(strip=True)
                if "больница" in name.lower() or "госпиталь" in name.lower():
                    hospitals.append({
                        "name": name[:200],
                        "type": "больница",
                        "address": region,
                        "region": region,
                        "district": ALL_FEDERAL_SUBJECTS.get(region, ""),
                        "beds": REGION_HEALTHCARE_PARAMS.get(region, REGION_HEALTHCARE_PARAMS["DEFAULT"])["avg_beds"],
                        "contact": "",
                        "source": title_elem.get("href", "")[:300],
                        "fetch_time": datetime.now().isoformat(),
                    })
        return hospitals

    def _save_to_file(self, orgs, region):
        """保存机构数据到文件"""
        timestamp = datetime.now().strftime("%Y%m%d")
        safe_region = region.replace(" ", "_").replace("—", "-")
        filename = f"medical_orgs_{safe_region}_{timestamp}.json"
        filepath = os.path.join(MEDICAL_ORGS_OUTPUT_DIR, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump({
                    "region": region,
                    "fetch_time": datetime.now().isoformat(),
                    "total_count": len(orgs),
                    "orgs": orgs,
                }, f, ensure_ascii=False, indent=2)
            logger.info(f"[医疗机构] 数据已保存: {filepath}")
        except Exception as e:
            logger.warning(f"[医疗机构] 保存失败: {e}")

    def export_all_regions(self):
        """导出所有区域机构数据"""
        all_data = {}
        for region in list(ALL_FEDERAL_SUBJECTS.keys())[:20]:
            orgs = self.get_medical_orgs_by_region(region)
            all_data[region] = orgs

        timestamp = datetime.now().strftime("%Y%m%d")
        filepath = os.path.join(MEDICAL_ORGS_OUTPUT_DIR, f"all_regions_{timestamp}.json")

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "export_time": datetime.now().isoformat(),
                "total_regions": len(all_data),
                "regions": all_data,
            }, f, ensure_ascii=False, indent=2)

        logger.info(f"[医疗机构] 全区域数据已导出: {filepath}")
        return filepath

    def generate_distribution_report(self, category=None):
        """生成机构分布报告"""
        category = category or "医疗器械"
        distribution = self.get_org_distribution_by_region(category, top_n=20)

        report = f"## 🏥 俄罗斯医疗机构分布报告\n\n"
        report += f"**品类**: {category}\n"
        report += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"

        if not distribution:
            report += "_暂无数据_"
            return report

        report += "| 联邦主体 | 机构数量 | 估算市场容量(万卢布) |\n"
        report += "|---------|---------|-------------------|\n"

        for region, count in list(distribution.items())[:15]:
            params = REGION_HEALTHCARE_PARAMS.get(region, REGION_HEALTHCARE_PARAMS["DEFAULT"])
            capacity = int(count * params["avg_beds"] / 10) if count > 0 else count * 10
            report += f"| {region} | {count} | ~{capacity} |\n"

        report += "\n**数据说明**：\n"
        report += "- 🔴 网络数据有限时使用区域医疗配置标准估算\n"
        report += "- 🟡 精确数据请参考 rosminzdrav.ru 官方医疗机构目录\n"
        report += "- 🟢 可联系区域卫生部门获取最新数据\n"

        return report


# ============================================================================
# 快捷函数
# ============================================================================
def get_medical_orgs_by_region(region, **kwargs):
    db = MedicalOrgDatabase()
    return db.get_medical_orgs_by_region(region, **kwargs)


def get_medical_orgs_by_type(org_type, region=None, **kwargs):
    db = MedicalOrgDatabase()
    return db.get_medical_orgs_by_type(org_type, region=region, **kwargs)


def get_org_distribution_by_region(category, top_n=20, **kwargs):
    db = MedicalOrgDatabase()
    return db.get_org_distribution_by_region(category, top_n=top_n, **kwargs)


def get_market_capacity(org_type, region, **kwargs):
    db = MedicalOrgDatabase()
    return db.get_market_capacity(org_type, region, **kwargs)


def search_medical_orgs(keyword, region=None, **kwargs):
    db = MedicalOrgDatabase()
    return db.search_medical_orgs(keyword, region=region, **kwargs)


# ============================================================================
# 测试
# ============================================================================
if __name__ == "__main__":
    db = MedicalOrgDatabase()

    print("=== 测试：莫斯科医疗机构 ===")
    orgs = db.get_medical_orgs_by_region("Москва")
    print(f"获取到 {len(orgs)} 个机构")
    for o in orgs[:3]:
        print(f"  [{o['type']}] {o['name']}")

    print("\n=== 测试：市场容量估算 ===")
    cap = db.get_market_capacity("больница", "Москва")
    print(f"医院市场容量: {cap['annual_market_capacity_rub']:,.0f} RUB")

    print("\n=== 测试：品类区域分布 ===")
    dist = db.get_org_distribution_by_region("血糖检测设备", top_n=5)
    for reg, cnt in dist.items():
        print(f"  {reg}: {cnt}")
