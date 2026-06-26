# -*- coding: utf-8 -*-
"""
Report-gama — 广告投放渠道与价格研究模块
估算各渠道CPM/CPC价格，分析竞品广告策略
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


class AdResearcher:
    """广告投放渠道与价格研究"""

    def __init__(self, country="俄罗斯", lang="ru"):
        self.country = country
        self.lang = lang
        self.country_code = self._country_to_code(country)
        self.session = self._create_session()
        self.ad_data = {}

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

    def get_channel_overview(self, category_keywords):
        """
        获取广告渠道总览

        Returns:
            dict: 各渠道的CPM/CPC估算价格
        """
        logger.info("[广告研究] 获取广告渠道信息...")

        channels = self._get_russian_channels() if self.country_code == "RU" else self._get_generic_channels()

        ad_data = {
            "country": self.country,
            "category": category_keywords,
            "export_time": datetime.now().isoformat(),
            "channels": channels,
        }

        self.ad_data = ad_data
        return channels

    def _get_russian_channels(self):
        """俄罗斯主要广告渠道"""
        return {
            "yandex_direct": {
                "name": "Yandex.Direct",
                "name_cn": "Yandex.Direct（俄罗斯最大搜索引擎广告）",
                "platform_type": "搜索引擎广告（SEA）",
                "reach": "俄罗斯 ~95% 互联网用户",
                "cpm_range_rub": "80–400",
                "cpc_range_rub": "5–50",
                "min_budget_rub": "10,000/月",
                "payment_model": "CPC/CPМ/CPV",
                "audience_targeting": "地理位置/兴趣/重定向",
                "medical_category": "医疗类需额外审核（需提供资质证明）",
                "registration": "需注册Yandex账户，可企业资质开户",
                "key_advantage": "覆盖俄罗斯用户搜索意图，转化率高",
                "competition_level": "中高",
                "estimated_monthly_cost": "50,000–500,000 RUB（起量阶段）",
            },
            "vk_ads": {
                "name": "VK Реклама",
                "name_cn": "VK广告（原VKontakte，俄罗斯社交媒体）",
                "platform_type": "社交媒体广告",
                "reach": "俄罗斯 ~80 МАУ（月活）",
                "cpm_range_rub": "50–200",
                "cpc_range_rub": "3–20",
                "min_budget_rub": "5,000/月",
                "payment_model": "CPC/CPМ",
                "audience_targeting": "用户画像/兴趣/行为",
                "medical_category": "需审核，可能限制处方药/医疗器械",
                "registration": "VK广告后台注册",
                "key_advantage": "社交属性强，适合品牌曝光+口碑",
                "competition_level": "中",
                "estimated_monthly_cost": "30,000–300,000 RUB",
            },
            "my_target": {
                "name": "MyTarget",
                "name_cn": "MyTarget（Mail.ru系广告平台）",
                "platform_type": "跨平台广告网络",
                "reach": "俄罗斯 ~90 МАУ",
                "cpm_range_rub": "30–120",
                "cpc_range_rub": "2–15",
                "min_budget_rub": "5,000/月",
                "payment_model": "CPC/CPM",
                "audience_targeting": "Mail.ru/OK用户画像",
                "medical_category": "同VK限制",
                "registration": "my.com账户",
                "key_advantage": "价格较低，适合中小品牌",
                "competition_level": "低-中",
                "estimated_monthly_cost": "20,000–200,000 RUB",
            },
            "google_ads_ru": {
                "name": "Google Ads（俄罗斯）",
                "name_cn": "Google Ads（受限于部分服务暂停）",
                "platform_type": "搜索引擎+展示广告",
                "reach": "俄罗斯部分用户（2022年后部分受限）",
                "cpm_range_rub": "60–300（受限制）",
                "cpc_range_rub": "5–40（受限制）",
                "min_budget_rub": "15,000/月",
                "payment_model": "CPC/CPM",
                "audience_targeting": "搜索意图/兴趣",
                "medical_category": "高度受限（2022年后）",
                "registration": "需境外账户",
                "key_advantage": "仍是部分用户习惯，但主要已被Yandex替代",
                "competition_level": "下降",
                "estimated_monthly_cost": "可用但不稳定",
            },
            "wildberries_ads": {
                "name": "Wildberries Реклама",
                "name_cn": "Wildberries站内广告（俄罗斯最大电商）",
                "platform_type": "电商站内广告",
                "reach": "Wildberries月活买家",
                "cpm_range_rub": "100–500（按展示计）",
                "cpc_range_rub": "10–80（按点击计）",
                "min_budget_rub": "10,000/月",
                "payment_model": "CPC/CPM",
                "audience_targeting": "商品品类/搜索词",
                "medical_category": "允许，但需资质证明",
                "registration": "WB卖家后台",
                "key_advantage": "高购买意向用户，直接转化",
                "competition_level": "高",
                "estimated_monthly_cost": "50,000–1,000,000 RUB（视品类竞争）",
            },
            "ozon_ads": {
                "name": "Ozon Промо",
                "name_cn": "Ozon站内推广",
                "platform_type": "电商站内广告",
                "reach": "Ozon月活买家",
                "cpm_range_rub": "80–400",
                "cpc_range_rub": "8–60",
                "min_budget_rub": "10,000/月",
                "payment_model": "CPC/CPM",
                "audience_targeting": "品类/搜索",
                "medical_category": "允许，需资质",
                "registration": "Ozon卖家后台",
                "key_advantage": "仅次于Wildberries的电商流量",
                "competition_level": "中高",
                "estimated_monthly_cost": "50,000–800,000 RUB",
            },
        }

    def _get_generic_channels(self):
        """通用广告渠道（非俄罗斯）"""
        return {
            "google_ads": {
                "name": "Google Ads",
                "name_cn": "Google Ads",
                "platform_type": "搜索引擎+展示广告",
                "cpm_range_usd": "2–10",
                "cpc_range_usd": "0.5–5",
                "key_advantage": "全球覆盖，精准投放",
            },
            "meta_ads": {
                "name": "Meta Ads",
                "name_cn": "Meta（Facebook/Instagram）广告",
                "platform_type": "社交媒体广告",
                "cpm_range_usd": "5–15",
                "cpc_range_usd": "0.5–3",
                "key_advantage": "强大用户画像，高互动",
            },
        }

    def estimate_campaign_budget(self, category_keywords, daily_cpc_targets=100):
        """
        估算广告投放预算

        Args:
            category_keywords: 品类关键词
            daily_cpc_targets: 目标每日点击数

        Returns:
            dict: 预算估算
        """
        channels = self.ad_data.get("channels", {})

        estimates = {}
        for channel_key, channel in channels.items():
            cpc_str = channel.get("cpc_range_rub", channel.get("cpc_range_usd", ""))
            match = re.search(r'(\d+)[–-](\d+)', cpc_str)
            if match:
                low_cpc, high_cpc = int(match.group(1)), int(match.group(2))
                avg_cpc = (low_cpc + high_cpc) / 2

                estimates[channel_key] = {
                    "channel_name": channel.get("name", ""),
                    "avg_cpc": avg_cpc,
                    "daily_budget": avg_cpc * daily_cpc_targets,
                    "monthly_budget": avg_cpc * daily_cpc_targets * 30,
                    "monthly_reach_estimate": daily_cpc_targets * 30 * 10,  # 估算CTR=10%
                }

        return estimates

    def research_competitor_ads(self, category_keywords, brand_keywords=None):
        """
        研究竞品广告投放情况
        通过搜索广告结果推断竞品广告活动
        """
        logger.info("[广告研究] 研究竞品广告策略...")

        competitors_ads = []
        ru_kw = category_keywords.get("ru", [])
        brand_kw = brand_keywords or []

        for kw in (ru_kw[:3] + brand_kw[:5]):
            # 搜索广告展示
            url = f"https://yandex.ru/search/?text={quote_plus(kw + ' купить')}"
            logger.info(f"[竞品广告] {kw[:30]}...")

            html = self._fetch(url)
            if html:
                soup = BeautifulSoup(html, "lxml")
                # Yandex广告通常有特定class
                for ad in soup.select("[class*='adv'], [class*='OrganicWithPromoOffer']")[:5]:
                    title = ad.get_text(strip=True)[:100]
                    if title:
                        competitors_ads.append({
                            "keyword": kw,
                            "ad_text": title,
                            "platform": "Yandex.Search",
                            "date": datetime.now().strftime("%Y-%m-%d"),
                        })

            time.sleep(random.uniform(2, 4))

        return competitors_ads

    def generate_ad_report(self, channels=None, competitor_ads=None, budget_estimates=None):
        """生成广告投放分析报告"""
        channels = channels or self.ad_data.get("channels", {})
        budget_estimates = budget_estimates or {}

        report = "## 📢 广告投放渠道与价格分析\n\n"
        report += f"_数据采集时间：{datetime.now().strftime('%Y-%m-%d')}_\n\n"

        if not channels:
            return report + "（暂无广告数据）\n\n"

        # 渠道总览表
        report += "### 📡 主要广告渠道总览\n\n"
        report += "| 渠道 | 类型 | 覆盖 | CPC区间 | CPM区间 | 最低预算/月 | 竞争程度 |\n"
        report += "|-----|------|------|---------|---------|-----------|--------|\n"

        for ch_key, ch in channels.items():
            name = ch.get("name", "")
            ptype = ch.get("platform_type", "")
            reach = ch.get("reach", "")
            cpc = ch.get("cpc_range_rub", ch.get("cpc_range_usd", ""))
            cpm = ch.get("cpm_range_rub", ch.get("cpm_range_usd", ""))
            min_budget = ch.get("min_budget_rub", ch.get("min_budget_usd", ""))
            competition = ch.get("competition_level", "")

            report += f"| {name} | {ptype} | {reach} | {cpc} | {cpm} | {min_budget} | {competition} |\n"

        report += "\n"

        # 预算估算
        if budget_estimates:
            report += "### 💰 推荐广告预算方案\n\n"
            report += "| 渠道 | 建议CPC | 日预算 | 月预算 | 预计月曝光 |\n"
            report += "|-----|---------|--------|--------|---------|\n"
            for ch_key, est in budget_estimates.items():
                ch_name = est.get("channel_name", ch_key)
                avg_cpc = est.get("avg_cpc", 0)
                daily = est.get("daily_budget", 0)
                monthly = est.get("monthly_budget", 0)
                reach = est.get("monthly_reach_estimate", 0)
                currency = "RUB"
                report += f"| {ch_name} | {avg_cpc:.0f} {currency} | {daily:,.0f} {currency} | {monthly:,.0f} {currency} | ~{reach:,} |\n"
            report += "\n"

        # 渠道特点对比
        report += "### 🎯 渠道选择建议\n\n"
        report += "| 目标 | 推荐渠道 | 理由 |\n"
        report += "|-----|---------|------|\n"
        report += "| 搜索意图转化 | Yandex.Direct | 用户主动搜索，转化率高 |\n"
        report += "| 品牌曝光 | VK/MyTarget | 覆盖广，社交信任度高 |\n"
        report += "| 直接电商销售 | Wildberries/Ozon站内广告 | 高购买意向人群 |\n"
        report += "| 重定向 | Yandex.Direct + VK | 触达已有兴趣用户 |\n"
        report += "\n"

        # 竞品广告
        if competitor_ads:
            report += "### 🏢 竞品广告动态\n\n"
            seen = set()
            for ad in competitor_ads[:20]:
                key = ad.get("ad_text", "")[:50]
                if key not in seen:
                    seen.add(key)
                    report += f"- [{ad.get('platform')}] **{ad.get('ad_text', '')}** (关键词: {ad.get('keyword', '')}) \n"

            report += "\n"

        # 医疗类广告注意事项
        if self.country_code == "RU":
            report += "### ⚠️ 俄罗斯医疗器械广告合规提示\n\n"
            report += "1. **Росздравнадзор资质**：医疗器械广告须具备相应注册证明\n"
            report += "2. **禁止内容**：不得声称「最好」「唯一」等绝对化用语\n"
            report += "3. **审核周期**：Yandex.Direct医疗类广告审核通常3-5个工作日\n"
            report += "4. **关键词限制**：部分医疗词汇需额外资质认证\n"
            report += "5. **数据留存**：广告数据需保存至少2年以备监管审查\n\n"

        report += "### 💡 投放策略建议\n\n"
        report += "- **起步策略**：先在Yandex.Direct做关键词广告，积累数据\n"
        report += "- **电商联动**：Wildberries广告与Yandex广告协同，形成搜索→购买的闭环\n"
        report += "- **预算分配**：建议 60% 搜索广告 + 30% 电商站内 + 10% 社媒\n"
        report += "- **A/B测试**：持续测试不同广告文案，优化CTR\n"
        report += "- **季节性**：医疗器械在换季、节假日（ Новый год、23 февраля）需求较高\n"

        return report

    def export_data(self, output_path=None):
        if output_path is None:
            output_path = f"ad_research_{datetime.now().strftime('%Y%m%d')}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.ad_data, f, ensure_ascii=False, indent=2)
        logger.info(f"广告研究数据已保存: {output_path}")
        return output_path


if __name__ == "__main__":
    researcher = AdResearcher(country="俄罗斯", lang="ru")
    keywords = {"ru": ["глюкометр", "измеритель глюкозы"], "en": ["blood glucose meter"]}
    channels = researcher.get_channel_overview(keywords)
    print(f"\n获取了 {len(channels)} 个广告渠道:")
    for ch in channels:
        print(f"  {channels[ch]['name']}: CPC {channels[ch].get('cpc_range_rub','N/A')}")
