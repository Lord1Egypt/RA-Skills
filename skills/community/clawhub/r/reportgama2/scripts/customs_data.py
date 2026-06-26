# -*- coding: utf-8 -*-
"""
Report-gama — 海关进出口数据模块
从 UN Comtrade、各国海关官网抓取进出口数量与金额数据
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


class CustomsData:
    """海关进出口数据采集"""

    def __init__(self, country="俄罗斯", lang="ru"):
        self.country = country
        self.lang = lang
        self.country_code = self._country_to_code(country)
        self.session = self._create_session()
        self.customs_data = {}

    def _country_to_code(self, country):
        codes = {"俄罗斯": "RU", "哈萨克斯坦": "KZ", "乌兹别克斯坦": "UZ", "白俄罗斯": "BY", "中国": "CN", "美国": "US"}
        return codes.get(country, "RU")

    def _create_session(self):
        session = requests.Session()
        session.headers.update({
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/json, text/html",
            "Accept-Language": f"{self.lang},en;q=0.5",
        })
        return session

    def _fetch(self, url, max_retries=REQUEST_RETRIES):
        for attempt in range(max_retries + 1):
            try:
                resp = self.session.get(url, timeout=REQUEST_TIMEOUT)
                if resp.status_code == 200:
                    return resp
                elif resp.status_code == 429:
                    time.sleep((attempt + 1) * 5)
            except Exception as e:
                logger.warning(f"请求失败: {e}")
                time.sleep(3)
        return None

    def get_hs_code(self, category):
        """获取品类对应的HS编码"""
        hs_map = {
            "血糖检测设备": {"primary": "902780", "alt": ["300190", "382200"], "description": "医疗分析仪器"},
            "血压计": {"primary": "901890", "alt": [], "description": "其他医疗仪器"},
            "体温计": {"primary": "902511", "alt": ["902519"], "description": "温度计"},
            "心电图机": {"primary": "901811", "alt": ["901812", "901819"], "description": "电气诊断仪器"},
            "雾化器": {"primary": "901920", "alt": [], "description": "呼吸器具"},
            "轮椅": {"primary": "8713", "alt": ["9402"], "description": "轮椅"},
            "一次性手套": {"primary": "401511", "alt": ["401519"], "description": "医疗用手套"},
            "通用": {"primary": "901890", "alt": [], "description": "其他医疗仪器"},
        }
        return hs_map.get(category, hs_map["通用"])

    def query_un_comtrade(self, hs_code, reporter_code="RU", years=None):
        """
        查询 UN Comtrade 数据库（免费公开API）

        Args:
            hs_code: HS编码
            reporter_code: 报告国代码
            years: 年份列表，默认最近5年

        Returns:
            dict: 进出口数据
        """
        years = years or [2021, 2022, 2023, 2024, 2025]
        logger.info(f"[UN Comtrade] 查询 HS:{hs_code} {reporter_code} {years}...")

        data = {
            "source": "UN Comtrade",
            "hs_code": hs_code,
            "reporter": reporter_code,
            "years": {},
        }

        # UN Comtrade API v1
        base_url = "https://comtradeapi.un.org/public/v1/preview/C/A/HS"

        for year in years:
            try:
                # 进口数据
                import_url = (
                    f"{base_url}/{year}/{reporter_code}/all?hsCode={hs_code}&partnerCode=WORLD"
                )
                resp = self._fetch(import_url)
                if resp and resp.status_code == 200:
                    try:
                        json_data = resp.json()
                        records = json_data.get("data", [])
                        if records:
                            rec = records[0]
                            data["years"][year] = {
                                "import_value_usd": rec.get("primaryValue", 0),
                                "import_qty": rec.get("netWgt", 0),
                                "import_qty_unit": "kg",
                                "cmd_desc": rec.get("cmdDesc", ""),
                            }
                    except json.JSONDecodeError:
                        pass
            except Exception as e:
                logger.warning(f"[UN Comtrade] {year} 失败: {e}")

            time.sleep(random.uniform(0.5, 1.5))

        return data

    def search_customs_from_web(self, hs_code, category_keywords, years=None):
        """
        通过网页搜索获取海关数据（当API不可用时的备选方案）

        Returns:
            dict: 估算的进出口数据
        """
        years = years or [2021, 2022, 2023, 2024, 2025]
        logger.info(f"[网页搜索] 海关数据 HS:{hs_code}...")

        ru_kw = category_keywords.get("ru", [])
        en_kw = category_keywords.get("en", [])

        search_phrases = []
        for kw in ru_kw[:2]:
            search_phrases.append(f"импорт {kw} объём {hs_code}")
            search_phrases.append(f"экспорт {kw} статистика {hs_code}")

        customs_data = {
            "source": "Web Research + Estimation",
            "hs_code": hs_code,
            "years": {},
            "note": "基于公开报道和贸易数据库的估算数据",
            "confidence": "medium",
        }

        # 搜索各年份数据
        for phrase in search_phrases[:6]:
            url = f"https://www.google.com/search?q={quote_plus(phrase)}&hl={self.lang}"
            logger.info(f"[海关数据] {phrase[:50]}...")

            resp = self._fetch(url)
            if resp:
                text = resp.text
                # 提取年份和数值
                for year in years:
                    # 模式1: "2024年 进口 1000万美元"
                    patterns = [
                        rf"{year}.*?(\d[\d.,]*)\s*(млн|тыс|百万|千万|万|USD|доллар)",
                        rf"(\d[\d.,]*)\s*(млн|тыс|百万|USD).*?{year}",
                        rf"импорт.*?{year}.*?(\d[\d.,]*)\s*(млн|тыс|USD)",
                    ]
                    for pattern in patterns:
                        matches = re.findall(pattern, text, re.IGNORECASE)
                        if matches:
                            for num_str, unit in matches:
                                try:
                                    num = float(re.sub(r'[^\d.]', '', num_str))
                                    if unit in ["млн", "百万"]:
                                        num *= 1_000_000
                                    elif unit in ["тыс", "千"]:
                                        num *= 1_000
                                    elif unit in ["万"]:
                                        num *= 10_000

                                    if year not in customs_data["years"]:
                                        customs_data["years"][year] = {}
                                    customs_data["years"][year]["import_value_usd"] = num
                                    customs_data["years"][year]["source_snippet"] = phrase
                                    break
                                except Exception:
                                    pass

            time.sleep(random.uniform(2, 4))

        return customs_data

    def estimate_market_size_from_customs(self, customs_data, hs_code, category):
        """
        基于海关数据估算市场规模

        Args:
            customs_data: 海关数据
            hs_code: HS编码
            category: 品类名

        Returns:
            dict: 市场规模估算
        """
        years_data = customs_data.get("years", {})

        if not years_data:
            return {
                "note": "海关数据暂不可得，无法估算",
                "confidence": "low",
            }

        latest_year = max(years_data.keys())
        latest_data = years_data[latest_year]

        # 从进口数据反推市场规模（假设进口占消费的30-60%）
        import_value = latest_data.get("import_value_usd", 0)

        if import_value > 0:
            # 粗估市场规模 = 进口额 / 进口占比
            market_size_low = import_value / 0.6  # 进口占60%
            market_size_high = import_value / 0.3  # 进口占30%

            return {
                "latest_year": latest_year,
                "import_value_usd": import_value,
                "estimated_market_size_usd_low": market_size_low,
                "estimated_market_size_usd_high": market_size_high,
                "estimated_market_size_usd_avg": (market_size_low + market_size_high) / 2,
                "growth_trend": self._calc_growth_trend(years_data),
                "confidence": "medium",
                "note": "基于UN Comtrade进口数据估算（假设进口占消费的30-60%）",
            }

        return {"note": "无法从海关数据估算市场规模", "confidence": "low"}

    def _calc_growth_trend(self, years_data):
        """计算进出口趋势"""
        if len(years_data) < 2:
            return "数据点不足"
        years = sorted(years_data.keys())
        values = [years_data[y].get("import_value_usd", 0) for y in years]
        values = [v for v in values if v > 0]
        if len(values) < 2:
            return "数据不足"
        growth = (values[-1] - values[0]) / values[0] * 100
        return f"{'+' if growth >= 0 else ''}{growth:.1f}%（{years[0]}-{years[-1]}）"

    def generate_customs_report(self, customs_data, market_estimate=None):
        """生成海关数据分析报告"""
        report = "## 🚢 海关进出口数据分析\n\n"
        report += f"_数据来源：{customs_data.get('source', 'Web Research')}_\n"
        report += f"_HS编码：{customs_data.get('hs_code', 'N/A')}_\n\n"

        years_data = customs_data.get("years", {})

        if not years_data:
            report += "### 📊 数据概况\n\n"
            report += "⚠️ **数据暂不可得**，原因可能包括：\n"
            report += "- UN Comtrade API 该品类数据未公开\n"
            report += "- 该品类跨多个HS编码，合并困难\n"
            report += "- 相关数据被归入更宽泛的分类\n\n"
            report += "**建议获取方式：**\n"
            report += "- 直接访问 [UN Comtrade](https://comtrade.un.org) 手动查询\n"
            report += "- 购买专业贸易数据库（Globeltradedata、Zauba等）\n"
            report += "- 联系各国海关总署申请统计数据\n\n"
            return report

        # 数据表
        years_sorted = sorted(years_data.keys(), reverse=True)
        currency = "USD"

        report += "### 📈 年度进口数据（单位：美元）\n\n"
        report += "| 年份 | 进口额（USD） | 数量（kg） | 备注 |\n"
        report += "|-----|-------------|-----------|------|\n"

        for year in years_sorted:
            d = years_data[year]
            val = d.get("import_value_usd", 0)
            qty = d.get("import_qty", 0)
            note = d.get("source_snippet", "")[:30] if d.get("source_snippet") else "—"
            if val:
                report += f"| {year} | **${val:,.0f}** | {qty:,.0f} | {note} |\n"
            else:
                report += f"| {year} | — | — | 暂无数据 |\n"

        report += "\n"

        # 趋势分析
        if len(years_sorted) >= 2:
            report += "### 📉 趋势分析\n\n"
            trend = self._calc_growth_trend(years_data)
            report += f"- **总体趋势**：{trend}\n"
            report += f"- **最新年份**：{years_sorted[0]}\n"

            values = [years_data[y].get("import_value_usd", 0) for y in years_sorted if years_data[y].get("import_value_usd")]
            if len(values) >= 2:
                report += f"- **进口额变化**：${values[0]:,.0f} → ${values[-1]:,.0f}\n"

            report += "\n"

        # 市场规模估算
        if market_estimate and market_estimate.get("confidence") != "low":
            report += "### 💹 市场规模估算\n\n"
            report += f"| 指标 | 数值 |\n"
            report += f"|------|------|\n"
            report += f"| 最新数据年份 | {market_estimate.get('latest_year', 'N/A')} |\n"
            report += f"| 进口额（USD） | ${market_estimate.get('import_value_usd', 0):,.0f} |\n"
            report += f"| 市场总规模（低端估算） | ${market_estimate.get('estimated_market_size_usd_low', 0):,.0f} |\n"
            report += f"| 市场总规模（高端估算） | ${market_estimate.get('estimated_market_size_usd_high', 0):,.0f} |\n"
            report += f"| 市场总规模（均值） | ${market_estimate.get('estimated_market_size_usd_avg', 0):,.0f} |\n"
            report += f"| 数据置信度 | 🟡 {market_estimate.get('confidence', 'unknown')} |\n"
            report += f"| 备注 | {market_estimate.get('note', '')} |\n"
            report += "\n"

        # 主要贸易国（估算）
        report += "### 🌍 主要贸易伙伴（俄罗斯医疗器械主要来源国）\n\n"
        report += "| 国家/地区 | 占比估算 | 主要品类 |\n"
        report += "|---------|---------|---------|\n"
        report += "| 🇨🇳 中国 | ~35% | 低端设备、电子体温计 |\n"
        report += "| 🇩🇪 德国 | ~20% | 高端设备、精密仪器 |\n"
        report += "| 🇺🇸 美国 | ~15% | 血糖仪、影像设备 |\n"
        report += "| 🇯🇵 日本 | ~10% | 精密设备、品牌器械 |\n"
        report += "| 🇰🇷 韩国 | ~8% | 消费级医疗器械 |\n"
        report += "| 其他 | ~12% | — |\n"
        report += "\n"
        report += "_注：以上为行业典型分布，非本品类精确数据_\n\n"

        # 获取建议
        report += "### 💡 数据获取建议\n\n"
        report += "如需更精确的海关数据，建议：\n"
        report += "1. 访问 [UN Comtrade](https://comtrade.un.org) 手动查询（免费，需注册）\n"
        report += "2. 使用 [OEC (Observatory of Economic Complexity)](https://oec.world/) 查询可视化贸易数据\n"
        report += "3. 购买专业数据库：Panjiva、ImportGenius、Datamyne 等\n"
        report += "4. 联系俄罗斯联邦海关总署（ФТС России）申请官方统计\n\n"

        return report

    def export_data(self, output_path=None):
        if output_path is None:
            output_path = f"customs_data_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.customs_data, f, ensure_ascii=False, indent=2)
        logger.info(f"海关数据已保存: {output_path}")
        return output_path


if __name__ == "__main__":
    customs = CustomsData(country="俄罗斯", lang="ru")
    keywords = {"ru": ["глюкометр"], "en": ["blood glucose meter"]}
    hs = customs.get_hs_code("血糖检测设备")
    data = customs.search_customs_from_web(hs["primary"], keywords, years=[2022, 2023, 2024])
    print(f"\n获取海关数据: {data.get('years', {})}")
