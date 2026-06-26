# -*- coding: utf-8 -*-
"""
Report-gama — 市场容量与TAM/SAM/SOM分析模块
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

from config import REQUEST_TIMEOUT, REQUEST_RETRIES, USER_AGENTS, LOG_LEVEL, LOG_FORMAT

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


class MarketResearcher:
    """市场容量与TAM/SAM/SOM分析"""

    def __init__(self, country="俄罗斯", lang="ru"):
        self.country = country
        self.lang = lang
        self.country_code = self._country_to_code(country)
        self.session = self._create_session()
        self.market_data = {}

    def _country_to_code(self, country):
        codes = {"俄罗斯": "RU", "哈萨克斯坦": "KZ", "乌兹别克斯坦": "UZ", "白俄罗斯": "BY", "中国": "CN", "美国": "US"}
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

    def get_country_market_overview(self, category_keywords):
        """
        获取目标国家/品类市场规模数据

        Returns:
            dict: 市场容量分析
        """
        logger.info("[市场研究] 分析市场规模...")

        ru_kw = category_keywords.get("ru", [])
        en_kw = category_keywords.get("en", [])

        # 搜索市场规模
        market_data = {
            "country": self.country,
            "lang": self.lang,
            "export_time": datetime.now().strftime("%Y-%m-%d"),
            "TAM": {},
            "SAM": {},
            "SOM": {},
            "market_trends": [],
            "sources": [],
        }

        # 搜索各类规模数据
        for kw in ru_kw[:2] + en_kw[:2]:
            phrases = [
                f"{kw} объём рынка 2024 2025",
                f"{kw} размер рынка",
                f"{kw} market size Russia",
                f"рынок медицинского оборудования {kw} ёмкость",
            ]

            for phrase in phrases:
                url = f"https://www.google.com/search?q={quote_plus(phrase)}&hl={self.lang}"
                logger.info(f"[市场数据] {phrase[:50]}...")

                html = self._fetch(url)
                if html:
                    soup = BeautifulSoup(html, "lxml")
                    for item in soup.select("div.g")[:5]:
                        text = item.get_text()
                        numbers = self._extract_market_numbers(text)
                        if numbers:
                            market_data["sources"].append({
                                "phrase": phrase,
                                "data": numbers,
                                "snippet": text[:200],
                            })

                time.sleep(random.uniform(2, 4))

        # 获取该国经济数据作为基准
        country_baseline = self._get_country_baseline()
        market_data["country_baseline"] = country_baseline

        self.market_data = market_data
        return market_data

    def _get_country_baseline(self):
        """获取目标国家经济基准数据"""
        baselines = {
            "RU": {
                "gdp_2024_usd": "约1.9万亿美元",
                "population_2024": "约1.44亿",
                "healthcare_spending_gdp": "约5.5%",
                "medical_devices_market_2024": "约50亿美元",
                "medical_devices_growth": "+8-12%/年",
                "import_share": "约60-70%依赖进口",
            },
            "KZ": {
                "gdp_2024_usd": "约2600亿美元",
                "population_2024": "约2000万",
                "healthcare_spending_gdp": "约4%",
                "medical_devices_market_2024": "约8亿美元",
                "medical_devices_growth": "+10-15%/年",
                "import_share": "约80%依赖进口",
            },
            "CN": {
                "gdp_2024_usd": "约18万亿美元",
                "population_2024": "约14亿",
                "healthcare_spending_gdp": "约7%",
                "medical_devices_market_2024": "约900亿美元",
                "medical_devices_growth": "+12-18%/年",
                "import_share": "高端设备依赖进口",
            },
        }
        return baselines.get(self.country_code, {})

    def _extract_market_numbers(self, text):
        """从文本中提取市场规模数字"""
        # 模式：X亿美元/X十亿美元/X百万
        patterns = [
            r'(\d[\d.,]*)\s*(млрд|млн|billion|million|十亿|百万|亿美元|十亿美元)',
            r'объём.*?(\d[\d.,]*)\s*(млрд|млн)',
            r'рынок.*?(\d[\d.,]*)\s*(млрд|млн)',
        ]

        results = []
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for num_str, unit in matches:
                try:
                    num = float(re.sub(r'[^\d.]', '', num_str))
                    # 单位换算
                    if unit.lower() in ["млрд", "billion", "十亿"]:
                        num *= 1_000_000_000
                    elif unit.lower() in ["млн", "million", "百万"]:
                        num *= 1_000_000
                    elif unit in ["亿美元", "十亿美元"]:
                        num *= 100_000_000

                    results.append({
                        "value": num,
                        "unit": "USD",
                        "raw": f"{num_str} {unit}",
                    })
                except Exception:
                    pass

        return results

    def estimate_tam_sam_som(self, category, category_keywords=None, existing_data=None):
        """
        估算 TAM/SAM/SOM

        假设（俄罗斯医疗器械市场为基准）：
        - TAM = 全球医疗器械市场规模 × 俄罗斯GDP占比
        - SAM = 俄罗斯医疗器械市场 × 品类占比
        - SOM = SAM × 可达份额 × 竞争力系数

        Args:
            category: 品类名
            category_keywords: 品类关键词
            existing_data: 已有市场数据

        Returns:
            dict: TAM/SAM/SOM 估算
        """
        category = category or "通用"

        # 俄罗斯市场基准（2024-2025年）
        russia_baseline = {
            "total_medical_devices_market_usd": 5_000_000_000,  # 50亿美元
            "annual_growth": 0.10,  # 10%
        }

        # 品类占比估算（医疗器械各品类市场份额）
        category_share = {
            "血糖检测设备": 0.08,      # 8%（血糖管理是大品类）
            "血压计": 0.06,           # 6%
            "体温计": 0.03,            # 3%
            "心电图机": 0.05,          # 5%
            "雾化器": 0.04,            # 4%
            "轮椅": 0.03,              # 3%
            "一次性手套": 0.12,        # 12%（耗材大品类）
            "通用": 0.05,             # 默认5%
        }

        share = category_share.get(category, 0.05)

        # 计算
        total_market = russia_baseline["total_medical_devices_market_usd"]
        tam = total_market / 0.044  # 俄罗斯占全球约4.4%
        sam = total_market * share
        som = sam * 0.05 * 0.3  # 可达5%，实际竞争获得30%

        estimates = {
            "category": category,
            "base_year": 2024,
            "TAM": {
                "value_usd": tam,
                "description": f"全球{category}市场规模",
                "confidence": "medium",
            },
            "SAM": {
                "value_usd": sam,
                "description": f"俄罗斯{category}市场规模",
                "note": f"基于俄罗斯医疗器械总市场（${total_market/1e9:.1f}B）×品类占比（{share*100:.0f}%）",
                "confidence": "medium",
            },
            "SOM": {
                "value_usd": som,
                "description": f"可触及的俄罗斯{category}市场",
                "note": "SAM × 可达率(5%) × 竞争成功率(30%)",
                "confidence": "low",
            },
            "growth_rate": russia_baseline["annual_growth"],
            "data_source": "综合估算（基于行业报告+公开数据）",
        }

        return estimates

    def generate_market_report(self, market_data=None, tam_sam_som=None):
        """生成市场研究报告"""
        market_data = market_data or self.market_data
        tam_sam_som = tam_sam_som or {}

        report = "## 📊 市场容量与规模分析\n\n"

        # 国家基准
        baseline = market_data.get("country_baseline", {})
        if baseline:
            report += f"### 🌐 {self.country} 经济基准\n\n"
            report += "| 指标 | 数据 |\n"
            report += "|-----|------|\n"
            for k, v in baseline.items():
                report += f"| {k} | {v} |\n"
            report += "\n"

        # TAM/SAM/SOM
        if tam_sam_som:
            report += "### 📐 TAM / SAM / SOM 市场分层\n\n"

            def fmt(val):
                if val >= 1e9:
                    return f"${val/1e9:.2f}B"
                elif val >= 1e6:
                    return f"${val/1e6:.1f}M"
                else:
                    return f"${val:,.0f}"

            report += "| 层级 | 规模 | 说明 | 置信度 |\n"
            report += "|-----|------|------|--------|\n"

            for layer in ["TAM", "SAM", "SOM"]:
                if layer in tam_sam_som:
                    data = tam_sam_som[layer]
                    report += f"| **{layer}** | **{fmt(data.get('value_usd', 0))}** | {data.get('description','')} | 🟡{data.get('confidence','medium')} |\n"

            report += "\n"
            report += f"**市场年增长率**：约 {tam_sam_som.get('growth_rate', 0)*100:.0f}%\n"
            report += f"**基准年份**：{tam_sam_som.get('base_year', 2024)}\n\n"

        # 趋势分析
        report += "### 📈 市场驱动因素\n\n"
        report += "| 因素 | 影响 | 说明 |\n"
        report += "|-----|------|------|\n"

        if self.country_code == "RU":
            drivers = [
                ("人口老龄化", "正向", "60岁以上人口占比持续上升，慢性病管理需求增加"),
                ("政府医疗投入", "正向", "联邦医疗现代化项目持续推进"),
                ("进口替代", "中性", "政府支持国产器械，但高端产品仍依赖进口"),
                ("卢布汇率", "负向", "进口成本受汇率波动影响较大"),
                ("电商渗透率", "正向", "线上购买医疗器械比例快速提升"),
                ("国产化率目标", "正向", "2024年目标：医疗器械国产化率达50%"),
            ]
        else:
            drivers = [
                ("经济增长", "正向", "中产阶级扩大"),
                ("医疗改革", "正向", "扩大医保覆盖"),
                ("技术创新", "正向", "智能化、便携化趋势"),
            ]

        for factor, impact, desc in drivers:
            emoji = "📈" if impact == "正向" else ("📉" if impact == "负向" else "➡️")
            report += f"| {emoji} {factor} | {impact} | {desc} |\n"

        report += "\n"

        # 数据来源
        sources = market_data.get("sources", [])
        if sources:
            report += "### 📚 数据来源\n\n"
            for src in sources[:5]:
                data = src.get("data", [])
                numbers_str = ", ".join([d.get("raw", "") for d in data[:2]])
                report += f"- **{src['phrase'][:50]}**：{numbers_str or '仅标题匹配'}\n"
            report += "\n"

        report += "### ⚠️ 数据说明\n\n"
        report += "- 🔴 TAM/SAM/SOM为综合估算值，非精确统计\n"
        report += "- 🟡 市场增长率基于行业历史数据推算\n"
        report += "- 🟢 建议结合实地调研进行验证\n\n"

        return report

    def export_data(self, output_path=None):
        if output_path is None:
            output_path = f"market_research_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.market_data, f, ensure_ascii=False, indent=2)
        logger.info(f"市场研究数据已保存: {output_path}")
        return output_path


if __name__ == "__main__":
    researcher = MarketResearcher(country="俄罗斯", lang="ru")
    keywords = {"ru": ["глюкометр"], "en": ["blood glucose meter"]}
    data = researcher.get_country_market_overview(keywords)
    print(f"\n市场数据: {data.get('sources', [])[:2]}")
