# -*- coding: utf-8 -*-
"""
Report-gama 配置文件
"""

import os

# 技能根目录（自动推断）
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(BASE_DIR)

# 输出目录
OUTPUT_DIR = os.path.join(SKILL_DIR, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 数据存储
DATA_DIR = os.path.join(SKILL_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ============================================================
# 支持的国家配置
# ============================================================
COUNTRIES = {
    "俄罗斯": {
        "code": "RU",
        "lang": "ru",
        "lang_alt": "en",
        "currency": "RUB",
        "currency_symbol": "₽",
        "ecommerce": ["wildberries", "ozon", "yandex_market"],
        "ad_channels": ["yandex_direct", "google_ads"],
        "customs_source": "un_comtrade",
        "news_sources": ["yandex_news", "rbc", "medvestnik", "vademecum"],
        "search_engines": ["yandex", "google", "ddg"],
        "hs_region": "RU",
    },
    "哈萨克斯坦": {
        "code": "KZ",
        "lang": "ru",
        "lang_alt": "kk",
        "currency": "KZT",
        "currency_symbol": "₸",
        "ecommerce": ["wildberries_kz", "kaspi"],
        "ad_channels": ["yandex_direct"],
        "customs_source": "un_comtrade",
        "news_sources": ["yandex_news", "tengrinews"],
        "search_engines": ["yandex", "google"],
        "hs_region": "KZ",
    },
    "乌兹别克斯坦": {
        "code": "UZ",
        "lang": "uz",
        "lang_alt": "ru",
        "currency": "UZS",
        "currency_symbol": "so'm",
        "ecommerce": ["uzum", "olx_uz"],
        "ad_channels": ["yandex_direct"],
        "customs_source": "un_comtrade",
        "news_sources": ["yandex_news"],
        "search_engines": ["yandex", "google"],
        "hs_region": "UZ",
    },
    "白俄罗斯": {
        "code": "BY",
        "lang": "ru",
        "lang_alt": "be",
        "currency": "BYN",
        "currency_symbol": "Br",
        "ecommerce": ["wildberries_by", "21vek"],
        "ad_channels": ["yandex_direct"],
        "customs_source": "un_comtrade",
        "news_sources": ["yandex_news"],
        "search_engines": ["yandex", "google"],
        "hs_region": "BY",
    },
    "中国": {
        "code": "CN",
        "lang": "zh",
        "lang_alt": "en",
        "currency": "CNY",
        "currency_symbol": "¥",
        "ecommerce": ["taobao", "jd", "pinduoduo"],
        "ad_channels": ["baidu", "bytedance_ads"],
        "customs_source": "china_customs",
        "news_sources": ["baidu_news", "sina", "36kr"],
        "search_engines": ["baidu", "google", "sogou"],
        "hs_region": "CN",
    },
    "美国": {
        "code": "US",
        "lang": "en",
        "lang_alt": "es",
        "currency": "USD",
        "currency_symbol": "$",
        "ecommerce": ["amazon", "walmart"],
        "ad_channels": ["google_ads", "meta_ads"],
        "customs_source": "us_census",
        "news_sources": ["google_news", "reuters", "bbc"],
        "search_engines": ["google", "bing", "ddg"],
        "hs_region": "US",
    },
}

# ============================================================
# 默认品类关键词库（俄语/英语/中文 三语）
# ============================================================
CATEGORY_KEYWORDS = {
    "血糖检测设备": {
        "ru": ["глюкометр", "измеритель глюкозы в крови", "тест-полоски для глюкометра", "глюкометр купить"],
        "en": ["blood glucose meter", "glucometer", "blood glucose monitor", "glucose test strips"],
        "zh": ["血糖仪", "血糖检测仪", "血糖试纸"],
        "hs_code": "902780",
        "hs_code_alt": ["300190", "382200"],
        "brand_keywords": ["Accu-Chek", "OneTouch", "Contour", "FreeStyle", "Сателлит", "Элта", "Омелон"],
    },
    "血压计": {
        "ru": ["тонометр", "измеритель артериального давления", "автоматический тонометр", "механический тонометр"],
        "en": ["blood pressure monitor", "sphygmomanometer", "BP monitor", "digital blood pressure"],
        "zh": ["血压计", "血压监测仪", "电子血压计"],
        "hs_code": "901890",
        "brand_keywords": ["Omron", "AND", "Microlife", "Little Doctor", "Armedio", "Medisana"],
    },
    "体温计": {
        "ru": ["термометр", "инфракрасный термометр", "электронный термометр"],
        "en": ["thermometer", "digital thermometer", "infrared thermometer"],
        "zh": ["体温计", "额温枪", "红外体温计"],
        "hs_code": "902511",
        "brand_keywords": ["Omron", "Braun", "Medisana", "Xiaomi", "CET"],
    },
    "心电图机": {
        "ru": ["электрокардиограф", "ЭКГ аппарат", "монитор сердечного ритма"],
        "en": ["ECG machine", "electrocardiograph", "EKG device"],
        "zh": ["心电图机", "心电监护仪"],
        "hs_code": "901811",
        "brand_keywords": ["Philips", "GE Healthcare", "Mortara", "Schiller", "Филипс"],
    },
    "雾化器": {
        "ru": ["небулайзер", "ингалятор", "компрессорный небулайзер"],
        "en": ["nebulizer", "inhaler", "compressor nebulizer"],
        "zh": ["雾化器", "吸入器", "医用雾化机"],
        "hs_code": "901920",
        "brand_keywords": ["Omron", "MED121", "Little Doctor", "Flute", "B.Well"],
    },
    "轮椅": {
        "ru": ["инвалидная коляска", "кресло-коляска", "электрическая коляска"],
        "en": ["wheelchair", "electric wheelchair", "manual wheelchair"],
        "zh": ["轮椅", "电动轮椅"],
        "hs_code": "8713",
        "brand_keywords": ["Invacare", "Drive Medical", "Karma", "Ottobock"],
    },
    "一次性手套": {
        "ru": ["перчатки медицинские", "перчатки латексные", "перчатки нитриловые"],
        "en": ["medical gloves", "latex gloves", "nitrile gloves"],
        "zh": ["医用手套", "一次性手套", "乳胶手套"],
        "hs_code": "401511",
        "brand_keywords": ["Aurelia", "SEMDM", "Benovy", "Academia"],
    },
}

# 通用品类（未知品类使用）
DEFAULT_KEYWORDS = {
    "ru": ["товар", "продукция"],
    "en": ["product", "goods"],
    "zh": ["产品", "商品"],
}

# ============================================================
# 新闻来源配置
# ============================================================
NEWS_SOURCES = {
    "RU": {
        "government": [
            {"name": "Росздравнадзор", "url": "https://roszdravnadzor.gov.ru", "lang": "ru"},
            {"name": "Минздрав России", "url": "https://minzdrav.gov.ru", "lang": "ru"},
            {"name": "ФАС России", "url": "https://fas.gov.ru", "lang": "ru"},
        ],
        "industry": [
            {"name": "Медвестник", "url": "https://medvestnik.ru", "lang": "ru"},
            {"name": "Vademecum", "url": "https://vademec.ru", "lang": "ru"},
            {"name": "Pharmvestnik", "url": "https://pharmvestnik.ru", "lang": "ru"},
            {"name": "РБК", "url": "https://rbc.ru", "lang": "ru"},
            {"name": "Коммерсантъ", "url": "https://kommersant.ru", "lang": "ru"},
        ],
        "ecommerce_news": [
            {"name": "Oborot.ru", "url": "https://oborot.ru", "lang": "ru"},
        ],
    },
    "KZ": {
        "industry": [
            {"name": "Tengrinews", "url": "https://tengrinews.kz", "lang": "ru"},
            {"name": "Казахстанский портал", "url": "https://kapital.kz", "lang": "ru"},
        ],
    },
    "CN": {
        "industry": [
            {"name": "36Kr", "url": "https://36kr.com", "lang": "zh"},
            {"name": "虎嗅", "url": "https://huxiu.com", "lang": "zh"},
            {"name": "亿欧", "url": "https://iyiou.com", "lang": "zh"},
        ],
    },
}

# ============================================================
# 电商平台配置
# ============================================================
ECOMMERCE_PLATFORMS = {
    "wildberries": {
        "name": "Wildberries",
        "name_cn": "Wildberries（俄罗斯最大电商）",
        "country": "RU",
        "search_url": "https://www.wildberries.ru/catalog/0/search.aspx?search={keyword}",
        "search_url_alt": "https://www.wildberries.ru/catalog/0/search.aspx?sort=popular&query={keyword}",
        "lang": "ru",
    },
    "ozon": {
        "name": "Ozon",
        "name_cn": "Ozon（俄罗斯综合电商）",
        "country": "RU",
        "search_url": "https://www.ozon.ru/search/?text={keyword}",
        "lang": "ru",
    },
    "yandex_market": {
        "name": "Яндекс.Маркет",
        "name_cn": "Yandex.Маркет（俄罗斯比价平台）",
        "country": "RU",
        "search_url": "https://market.yandex.ru/search?text={keyword}",
        "lang": "ru",
    },
    "kaspi": {
        "name": "Kaspi.kz",
        "name_cn": "Kaspi（哈萨克斯坦电商）",
        "country": "KZ",
        "search_url": "https://kaspi.kz/shop/search/?text={keyword}",
        "lang": "ru",
    },
    "amazon": {
        "name": "Amazon",
        "name_cn": "Amazon（美国/全球电商）",
        "country": "US",
        "search_url": "https://www.amazon.com/s?k={keyword}",
        "lang": "en",
    },
    "jd": {
        "name": "京东",
        "name_cn": "京东",
        "country": "CN",
        "search_url": "https://search.jd.com/Search?keyword={keyword}",
        "lang": "zh",
    },
}

# ============================================================
# 搜索配置
# ============================================================
SEARCH_ENGINES = {
    "yandex": {
        "name": "Yandex",
        "base_url": "https://yandex.ru/search/?text={keyword}&lr={lr}&nd=1",
        "news_url": "https://news.search.yandex.ru/news?q={keyword}&lr={lr}",
        "lr_codes": {"RU": 213, "KZ": 163, "UZ": 10505, "BY": 14969, "US": 39},
    },
    "google": {
        "name": "Google",
        "base_url": "https://www.google.com/search?q={keyword}&hl={hl}&gl={gl}",
        "news_url": "https://news.google.com/search?q={keyword}&hl={hl}",
    },
    "baidu": {
        "name": "Baidu",
        "base_url": "https://www.baidu.com/s?wd={keyword}",
        "news_url": "https://news.baidu.com/ns?word={keyword}",
    },
    "ddg": {
        "name": "DuckDuckGo",
        "base_url": "https://duckduckgo.com/html/?q={keyword}",
        "news_url": "https://duckduckgo.com/html/?q={keyword}&ia=news",
    },
    "bing": {
        "name": "Bing",
        "base_url": "https://www.bing.com/search?q={keyword}",
        "news_url": "https://www.bing.com/news/search?q={keyword}",
    },
}

# ============================================================
# 海关数据配置
# ============================================================
CUSTOMS_CONFIG = {
    "un_comtrade": {
        "name": "UN Comtrade",
        "base_url": "https://comtradeapi.un.org/public/v1/preview/C/A/HS",
        "requires_auth": False,
    },
    "china_customs": {
        "name": "中国海关总署",
        "base_url": "http://www.customs.gov.cn",
    },
}

# ============================================================
# 报告生成配置
# ============================================================
REPORT_CONFIG = {
    "max_news_days": 30,
    "max_search_results_per_query": 20,
    "min_source_confidence": "medium",
    "chart_dpi": 150,
    "chart_width_inches": 10,
    "chart_height_inches": 6,
    "pdf_page_size": "A4",
}

# ============================================================
# 用户代理池
# ============================================================
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
]

# ============================================================
# 代理配置（可选）
# ============================================================
PROXY = os.environ.get("HTTP_PROXY", None)
HTTPS_PROXY = os.environ.get("HTTPS_PROXY", None)

# ============================================================
# 请求超时配置（秒）
# ============================================================
REQUEST_TIMEOUT = 15
REQUEST_RETRIES = 2

# ============================================================
# 日志配置
# ============================================================
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
