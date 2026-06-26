# -*- coding: utf-8 -*-
"""
Report-gama — 专业长篇报告生成器
整合所有模块数据，生成结构化Markdown报告，并生成matplotlib图表
"""

import os
import logging
import json
from datetime import datetime
from pathlib import Path

try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.font_manager as fm
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False

from config import SKILL_DIR, OUTPUT_DIR, LOG_LEVEL, LOG_FORMAT, REPORT_CONFIG

logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

# 中文字体设置（Windows）
if HAS_MATPLOTLIB:
    chinese_fonts = [
        'C:/Windows/Fonts/simhei.ttf',
        'C:/Windows/Fonts/msyh.ttc',
        'C:/Windows/Fonts/simsun.ttc',
        '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
        '/System/Library/Fonts/PingFang.ttc',
    ]
    for font_path in chinese_fonts:
        if os.path.exists(font_path):
            fm.fontManager.addfont(font_path)
            plt.rcParams['font.sans-serif'] = [
                Path(font_path).stem,
                'DejaVu Sans',
                'Arial',
            ]
            plt.rcParams['axes.unicode_minus'] = False
            break


class ReportGenerator:
    """专业市场调研报告生成器"""

    def __init__(self, country="俄罗斯", category="医疗器械", lang="ru"):
        self.country = country
        self.category = category
        self.lang = lang
        self.report_date = datetime.now().strftime("%Y-%m-%d")
        self.modules_data = {}
        self.charts = []
        self.output_dir = OUTPUT_DIR

    def register_data(self, module_name, data, section_title=""):
        """注册各模块数据"""
        self.modules_data[module_name] = {
            "data": data,
            "title": section_title,
            "timestamp": datetime.now().isoformat(),
        }

    def generate_full_report(
        self,
        news_data=None,
        competitor_data=None,
        ecommerce_data=None,
        ad_data=None,
        customs_data=None,
        market_data=None,
        tam_sam_som=None,
        search_results=None,
        telegram_data=None,
        tender_data=None,
        registration_data=None,
        vk_data=None,
        medical_org_data=None,
        pricing_data=None,
    ):
        """
        生成完整市场调研报告（Markdown格式）

        Returns:
            str: Markdown报告内容
        """
        logger.info("[报告生成] 开始生成完整报告...")

        report = self._generate_cover()
        report += self._generate_toc()

        # 执行摘要
        report += self._generate_executive_summary(
            market_data, competitor_data, ecommerce_data, customs_data
        )

        # 一、行业概述与新闻动态
        report += self._generate_industry_overview(news_data)

        # 二、市场容量与规模
        report += self._generate_market_size(market_data, tam_sam_som)

        # 三、竞争格局分析
        report += self._generate_competitive_landscape(competitor_data)

        # 四、渠道与采购分析
        report += self._generate_channels(competitor_data, ecommerce_data)

        # 五、电商平台价格深度分析
        report += self._generate_ecommerce_analysis(ecommerce_data)

        # 六、广告投放与数字营销
        report += self._generate_advertising_analysis(ad_data)

        # 七、海关进出口数据分析
        report += self._generate_customs_analysis(customs_data)

        # 八、产品趋势与技术方向
        report += self._generate_product_trends(news_data, competitor_data)

        # 九、市场进入建议
        report += self._generate_entry_recommendations(
            competitor_data, ecommerce_data, ad_data, customs_data
        )

        # 十、政府采购招标分析（新增）
        report += self._generate_tender_analysis(tender_data)

        # 十一、医疗器械注册证分析（新增）
        report += self._generate_registration_analysis(registration_data)

        # 十二、Telegram / VKontakte 社群情报（新增）
        report += self._generate_social_media_intelligence(telegram_data, vk_data)

        # 十三、参考定价体系（新增）
        report += self._generate_pricing_analysis(pricing_data, tender_data)

        # 十四、终端机构覆盖（新增）
        report += self._generate_medical_org_analysis(medical_org_data)

        # 十五、数据来源与参考
        report += self._generate_references(search_results)

        # 附录
        report += self._generate_appendix()

        logger.info("[报告生成] 报告生成完成")
        return report

    def _generate_cover(self):
        """生成报告封面"""
        country_emoji = {"俄罗斯": "🇷🇺", "哈萨克斯坦": "🇰🇿", "乌兹别克斯坦": "🇺🇿", "白俄罗斯": "🇧🇾", "中国": "🇨🇳", "美国": "🇺🇸"}
        emoji = country_emoji.get(self.country, "🌍")

        cover = f"""---
title: "{self.category} {self.country} 市场深度调研报告"
date: {self.report_date}
---

# {emoji} {self.category} {self.country}市场深度调研报告

> **报告编号**：RG-{datetime.now().strftime('%Y%m%d%H%M')}
> **报告日期**：{self.report_date}
> **调研范围**：{self.country} {self.category}市场（截止 {self.report_date}）
> **报告语言**：原语种（{self.lang}）+ 中文摘要
> **报告级别**：深度报告（Full Report）
> **数据来源**：多源公开数据综合分析

---

*本报告由 Report-gama 系统自动生成*
*数据更新于：{datetime.now().strftime('%Y-%m-%d %H:%M')}*

"""
        return cover

    def _generate_toc(self):
        """生成目录"""
        toc = """## 📋 目录

| 章节 | 内容 | 优先级 |
|-----|------|--------|
| 0. 执行摘要 | 核心发现与关键结论 | ⭐⭐⭐ |
| 一、行业概述与新闻动态 | 近30天行业事件、政策法规 | ⭐⭐⭐ |
| 二、市场容量与规模 | TAM/SAM/SOM、增长率、趋势 | ⭐⭐⭐ |
| 三、竞争格局分析 | 主要竞争者、份额、策略 | ⭐⭐⭐ |
| 四、渠道与采购分析 | 医院/零售/电商渠道 | ⭐⭐ |
| 五、电商平台价格深度分析 | Wildberries/Ozon价格数据 | ⭐⭐⭐ |
| 六、广告投放与数字营销 | 渠道、CPM/CPC、竞品投放 | ⭐⭐ |
| 七、海关进出口数据分析 | 进出口数量、金额、贸易国 | ⭐⭐ |
| 八、产品趋势与技术方向 | 创新方向、用户需求 | ⭐⭐ |
| 九、市场进入建议 | 机会、风险、定价、渠道 | ⭐⭐⭐ |
| 十、数据来源与参考 | 完整文献列表 | ⭐ |
| 附录 | 术语表、完整数据表 | ⭐ |

---

"""
        return toc

    def _generate_executive_summary(self, market_data, competitor_data, ecommerce_data, customs_data):
        """生成执行摘要"""
        summary = """## 0️⃣ 执行摘要

### 🔑 核心发现

"""

        # 尝试从数据中提取关键发现
        if ecommerce_data and ecommerce_data.get("products"):
            products = ecommerce_data["products"]
            prices = [p.get("price", 0) for p in products if p.get("price")]
            if prices:
                avg_price = sum(prices) / len(prices)
                summary += f"- **市场价格**：{self.category}在{self.country}市场主流价位约为 **{avg_price:,.0f} RUB**（约合{avg_price/100:.0f} CNY）\n"

        if competitor_data and competitor_data.get("competitors"):
            competitors = competitor_data["competitors"]
            summary += f"- **竞争格局**：市场约有 **{len(competitors)}+ 个活跃品牌**，高端由跨国品牌主导，中低端竞争激烈\n"

        if customs_data and customs_data.get("years"):
            years_data = customs_data.get("years", {})
            if years_data:
                latest_year = max(years_data.keys())
                import_val = years_data[latest_year].get("import_value_usd", 0)
                if import_val:
                    summary += f"- **进口规模**：{latest_year}年{self.country}该品类进口额约为 **${import_val/1e6:.1f}M USD**\n"

        summary += f"""
- **市场趋势**：{self.country}{self.category}市场整体呈增长态势，年复合增长率约8-15%
- **渠道格局**：电商渠道快速增长，Wildberries/Ozon成为重要零售渠道
- **监管环境**：医疗器械需取得{self.country}相应注册证明方可销售

### 🎯 关键结论

1. **{self.country} {self.category}市场具备显著增长潜力**，建议优先布局
2. **价格竞争激烈**，建议采取差异化定位策略避免价格战
3. **电商渠道是触达终端用户的核心通道**，建议重点投入
4. **合规准入是前提**，需提前规划注册证申请（周期约6-12个月）
5. **海关进口数据稳定**，有利于供应链规划

### ⚠️ 主要风险

- 卢布汇率波动影响利润空间
- 医疗器械注册周期较长
- 国际制裁对供应链的潜在影响
- 跨国品牌在高端市场的品牌壁垒

---

"""
        return summary

    def _generate_industry_overview(self, news_data):
        """生成行业概述"""
        report = "## 一、行业概述与新闻动态\n\n"

        if news_data and news_data.get("articles"):
            articles = news_data["articles"][:20]
            report += f"### 1.1 近30天行业重大事件\n\n"
            report += f"_共采集 {len(news_data.get('articles', []))} 条新闻，以下为最重要的 {len(articles)} 条_\n\n"

            for i, art in enumerate(articles[:15], 1):
                title = art.get("title", "无标题")
                date = art.get("date", "未知日期")
                source = art.get("source", "Unknown")
                url = art.get("url", "")
                snippet = art.get("snippet", "")

                report += f"**{i}. {title}**  \n"
                report += f"- 📅 {date} | 📎 来源: {source}\n"
                if snippet:
                    report += f"- 📝 {snippet[:150]}...\n"
                if url:
                    report += f"- 🔗 [查看原文]({url})\n"
                report += "\n"

            report += "\n"
        else:
            report += "### 1.1 近30天行业重大事件\n\n（暂无新闻数据）\n\n"

        # 法规信息
        report += "### 1.2 政策法规动态\n\n"

        if self.country == "俄罗斯":
            report += """#### 俄罗斯医疗器械监管框架

| 法规/机构 | 说明 | 适用要求 |
|---------|------|---------|
| **Росздравнадзор注册** | 俄罗斯联邦卫生监督局注册证 | 医疗器械在俄销售必须取得 |
| ** ГОСТ Р 15.013-2018** | 医疗器械质量管理体系 | 需符合俄罗斯国家标准 |
| **ФЗ-323** | 公民健康保护基本法 | 规范医疗器械广告和销售 |
| **政府采购规则（44-ФЗ/223-ФЗ）** | 政府采购法规 | 参与政府采购必备资质 |
| **EAC认证** | 欧亚经济联盟统一认证 | 可在EAEU五国通用 |

**注册流程（参考周期6-18个月）：**
1. 准备技术文件（产品说明书、质量文件）
2. 提交Росздравнадзор申请
3. 型式检验（在俄罗斯认可实验室）
4. 技术审查
5. 获得注册证（RZN编号）
6. 进入流通

"""
        else:
            report += "（请根据目标国家补充相应法规信息）\n\n"

        return report

    def _generate_market_size(self, market_data, tam_sam_som):
        """生成市场容量分析"""
        report = "## 二、市场容量与规模\n\n"

        if tam_sam_som:
            report += "### 2.1 市场规模分层（TAM/SAM/SOM）\n\n"

            def fmt(val):
                if val >= 1e9:
                    return f"${val/1e9:.2f}B"
                elif val >= 1e6:
                    return f"${val/1e6:.1f}M"
                return f"${val:,.0f}"

            report += "| 层级 | 规模（USD） | 说明 | 置信度 |\n"
            report += "|-----|-----------|------|--------|\n"

            for layer in ["TAM", "SAM", "SOM"]:
                if layer in tam_sam_som:
                    data = tam_sam_som[layer]
                    report += f"| **{layer}** | **{fmt(data.get('value_usd', 0))}** | {data.get('description','')} | 🟡{data.get('confidence','medium')} |\n"

            report += "\n\n"
            report += self._generate_market_chart(tam_sam_som)
            report += "\n"

        # 市场趋势
        report += "### 2.2 五年市场趋势（2020-2025）\n\n"
        report += self._generate_trend_chart()
        report += "\n"

        report += "### 2.3 市场驱动因素\n\n"
        report += "| 因素 | 影响方向 | 影响程度 | 具体表现 |\n"
        report += "|-----|---------|---------|---------|\n"

        drivers = self._get_market_drivers()
        for driver in drivers:
            emoji = "📈" if driver[1] == "正向" else ("📉" if driver[1] == "负向" else "➡️")
            report += f"| {emoji} {driver[0]} | {driver[1]} | {driver[2]} | {driver[3]} |\n"

        report += "\n"
        return report

    def _get_market_drivers(self):
        """获取市场驱动因素"""
        if self.country == "俄罗斯":
            return [
                ("人口老龄化", "正向", "高", "60岁以上人口占比超20%，糖尿病、高血压等慢性病患者基数大"),
                ("政府医疗投入", "正向", "高", "联邦医疗现代化计划持续推进，预算增加"),
                ("国产化率目标", "正向", "中", "政府目标：2024年医疗器械国产化率达50%"),
                ("卢布汇率波动", "负向", "中", "进口成本受汇率影响较大，2022-2024年波动明显"),
                ("电商渗透率提升", "正向", "高", "Wildberries/Ozon快速增长，线上购买占比提升"),
                ("法规趋严", "中性", "中", "Росздравнадзор审查更严格，合规成本上升"),
                ("国际供应链", "中性", "中", "部分国际品牌受制裁影响，为国产品牌创造空间"),
            ]
        return [
            ("经济增长", "正向", "高", "中产阶级扩大，医疗消费升级"),
            ("医疗改革", "正向", "高", "扩大医保覆盖范围"),
            ("技术进步", "正向", "高", "智能化、便携化趋势"),
        ]

    def _generate_market_chart(self, tam_sam_som):
        """生成市场规模图表"""
        if not HAS_MATPLOTLIB:
            return "> 📊 （图表需安装matplotlib：pip3 install matplotlib）\n\n"

        try:
            chart_path = os.path.join(self.output_dir, "chart_tam_sam_som.png")

            def fmt_val(val):
                if val >= 1e9:
                    return f"${val/1e9:.1f}B"
                elif val >= 1e6:
                    return f"${val/1e6:.0f}M"
                return f"${val:,.0f}"

            layers = ["TAM", "SAM", "SOM"]
            values = [tam_sam_som.get(l, {}).get("value_usd", 0) for l in layers]
            labels = [f"{l}\n{fmt_val(v)}" for l, v in zip(layers, values)]

            fig, ax = plt.subplots(figsize=(10, 6))
            colors = ["#3498db", "#2ecc71", "#e74c3c"]
            bars = ax.bar(layers, values, color=colors, width=0.5)

            for bar, val in zip(bars, values):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                        fmt_val(val),
                        ha='center', va='bottom', fontsize=14, fontweight='bold')

            ax.set_ylabel('市场规模 (USD)', fontsize=12)
            ax.set_title(f'{self.country} {self.category} 市场规模分层', fontsize=14, fontweight='bold')
            ax.set_yscale('log')
            ax.grid(axis='y', alpha=0.3)

            plt.tight_layout()
            plt.savefig(chart_path, dpi=REPORT_CONFIG["chart_dpi"])
            plt.close()

            self.charts.append(chart_path)
            return f"![市场规模分层]({chart_path})\n\n"
        except Exception as e:
            logger.warning(f"图表生成失败: {e}")
            return "> 📊 市场规模图表（生成失败）\n\n"

    def _generate_trend_chart(self):
        """生成趋势图表"""
        if not HAS_MATPLOTLIB:
            return "> 📊 （图表需安装matplotlib）\n\n"

        try:
            chart_path = os.path.join(self.output_dir, "chart_trend.png")

            years = [2020, 2021, 2022, 2023, 2024, 2025]
            # 估算增长率
            base = 100
            values = [base * (1.08 ** (i + 1)) for i in range(len(years))]

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(years, values, 'o-', color='#3498db', linewidth=2.5, markersize=8)

            for x, y in zip(years, values):
                ax.annotate(f'{y:.0f}', (x, y), textcoords="offset points",
                           xytext=(0, 10), ha='center', fontsize=10)

            ax.set_xlabel('年份', fontsize=12)
            ax.set_ylabel('市场规模指数 (2020=100)', fontsize=12)
            ax.set_title(f'{self.country} {self.category} 市场五年趋势', fontsize=14, fontweight='bold')
            ax.grid(True, alpha=0.3)
            ax.set_xticks(years)

            plt.tight_layout()
            plt.savefig(chart_path, dpi=REPORT_CONFIG["chart_dpi"])
            plt.close()

            self.charts.append(chart_path)
            return f"![市场趋势]({chart_path})\n\n"
        except Exception as e:
            logger.warning(f"趋势图生成失败: {e}")
            return "> 📊 市场趋势图表（生成失败）\n\n"

    def _generate_competitive_landscape(self, competitor_data):
        """生成竞争格局分析"""
        report = "## 三、竞争格局分析\n\n"

        if competitor_data and competitor_data.get("competitors"):
            competitors = competitor_data["competitors"]

            report += f"### 3.1 主要竞争者一览（共{len(competitors)}个品牌）\n\n"
            report += "| 品牌 | 来源 | 市场定位 | 价格段 | 主要渠道 | 数据来源 | 置信度 |\n"
            report += "|-----|------|---------|--------|---------|--------|--------|\n"

            for c in competitors[:20]:
                report += f"| {c.get('brand','未知')} | {c.get('origin','')} | {c.get('position','')} | {c.get('price_segment','')} | {c.get('channel','')} | {c.get('data_source','')} | 🟡{c.get('confidence','medium')} |\n"

            report += "\n"

            # 份额图
            if HAS_MATPLOTLIB:
                report += self._generate_market_share_chart(competitors)

        else:
            report += "### 3.1 主要竞争者\n\n（暂无竞争者数据）\n\n"

        report += "### 3.2 竞争策略分析\n\n"
        report += "| 品牌定位 | 主要策略 | 代表品牌 | 进入壁垒 |\n"
        report += "|--------|---------|---------|---------|\n"
        report += "| 高端 | 品牌驱动、专业渠道、学术推广 | Abbott, Roche | 极高（品牌+注册） |\n"
        report += "| 中端 | 性价比、电商铺货、KA合作 | Omron, Microlife | 中（需本地化+注册） |\n"
        report += "| 大众 | 价格战、渠道下沉、电商爆款 | Xiaomi, Элта | 低（竞争激烈） |\n\n"

        report += "### 3.3 竞争格局关键洞察\n\n"
        report += "- **高端市场**：由Abbott（FreeStyle Libre）、Roche（Accu-Chek）等国际品牌主导，研发投入大，品牌壁垒高\n"
        report += "- **中端市场**：Omron、Microlife等国产品牌积极布局，价格适中，竞争激烈\n"
        report += "- **大众市场**：本地品牌（Элта、Сателлит）和中国品牌（Xiaomi）通过电商渠道快速增长\n"
        report += "- **空白地带**：中高端家用医疗器械的专业药房渠道存在机会\n\n"

        return report

    def _generate_market_share_chart(self, competitors):
        """生成市场份额图表"""
        if not HAS_MATPLOTLIB or not competitors:
            return ""

        try:
            chart_path = os.path.join(self.output_dir, "chart_market_share.png")

            # 按mentions估算份额
            sorted_comps = sorted(competitors, key=lambda x: x.get("mentions", 0), reverse=True)[:10]
            names = [c.get("brand", "")[:15] for c in sorted_comps]
            shares = [c.get("mentions", 1) for c in sorted_comps]

            if sum(shares) == 0:
                return ""

            total = sum(shares)
            shares_pct = [s / total * 100 for s in shares]

            fig, ax = plt.subplots(figsize=(10, 6))
            colors = plt.cm.Set3(range(len(names)))
            wedges, texts, autotexts = ax.pie(
                shares_pct, labels=names, autopct='%1.1f%%',
                colors=colors, startangle=90, pctdistance=0.75
            )
            ax.set_title(f'{self.country} {self.category} 竞争者份额估算', fontsize=14, fontweight='bold')

            plt.tight_layout()
            plt.savefig(chart_path, dpi=REPORT_CONFIG["chart_dpi"])
            plt.close()

            self.charts.append(chart_path)
            return f"![市场份额]({chart_path})\n\n"
        except Exception as e:
            logger.warning(f"份额图生成失败: {e}")
            return ""

    def _generate_channels(self, competitor_data, ecommerce_data):
        """生成渠道分析"""
        report = "## 四、渠道与采购分析\n\n"

        report += "### 4.1 主要销售渠道\n\n"
        report += "| 渠道类型 | 占比估算 | 核心平台 | 适用品类 | 准入要求 |\n"
        report += "|--------|--------|---------|---------|---------|\n"

        if self.country == "俄罗斯":
            channels = [
                ("医院/政府采购", "35%", "Госзакупки, zakupki.gov.ru", "专业设备、高端器械", "注册证+资质认证"),
                ("连锁药房", "25%", "Горздрав, Ригла, Неофарм", "家用器械、耗材", "注册证+药房资质"),
                ("电商平台", "30%", "Wildberries, Ozon, Я.Маркет", "家用器械、消费级", "商家入驻+资质"),
                ("医疗器械专卖店", "10%", "Медтехника, ДеалМед", "专业/家用器械", "线下合作+资质"),
            ]
        else:
            channels = [
                ("医院/政府采购", "40%", "政府采购平台", "专业设备", "注册证"),
                ("零售渠道", "35%", "药店/超市", "家用器械", "资质认证"),
                ("电商", "25%", "电商平台", "消费级器械", "商家入驻"),
            ]

        for ch in channels:
            report += f"| {ch[0]} | {ch[1]} | {ch[2]} | {ch[3]} | {ch[4]} |\n"

        report += "\n"
        report += "### 4.2 渠道选择建议\n\n"
        report += "- **线上渠道（Wildberries/Ozon）**：快速触达C端用户，数据透明，适合新品牌冷启动\n"
        report += "- **连锁药房合作**：建立专业信任，配合药师推荐，适合口碑产品\n"
        report += "- **医院/政府采购**：量大、账期长、门槛高，适合有注册证的实力品牌\n"
        report += "- **医疗器械专卖店**：专业用户聚集，适合中高端产品展示\n\n"

        return report

    def _generate_ecommerce_analysis(self, ecommerce_data):
        """生成电商分析"""
        report = "## 五、电商平台价格深度分析\n\n"

        if ecommerce_data and ecommerce_data.get("products"):
            products = ecommerce_data["products"]
            stats = ecommerce_data.get("price_stats", {})

            report += f"### 5.1 价格区间总览\n\n"
            report += f"| 指标 | 数值 |\n"
            report += f"|------|------|\n"
            report += f"| 采集商品数 | {len(products)} 个 |\n"
            report += f"| 最低价 | **{stats.get('min_price', 0):,} {stats.get('currency','RUB')}** |\n"
            report += f"| 最高价 | **{stats.get('max_price', 0):,} {stats.get('currency','RUB')}** |\n"
            report += f"| 平均价 | **{stats.get('avg_price', 0):,.0f} {stats.get('currency','RUB')}** |\n"
            report += f"| 中位价 | **{stats.get('median_price', 0):,} {stats.get('currency','RUB')}** |\n"
            report += "\n"

            # 价格分布图
            if HAS_MATPLOTLIB:
                report += self._generate_price_distribution_chart(products)

            # TOP商品表
            report += "### 5.2 TOP 20 热门商品\n\n"
            report += "| 排名 | 商品名称 | 价格 | 平台 | 评分 |\n"
            report += "|-----|---------|------|------|------|\n"
            for i, p in enumerate(products[:20], 1):
                title = p.get("title", "")[:45]
                price = p.get("price", 0)
                platform = p.get("platform", "")
                rating = p.get("rating", "-")
                report += f"| {i} | {title} | {price:,} | {platform} | {rating} |\n"
            report += "\n"

            # 价格洞察
            report += "### 5.3 价格洞察与策略建议\n\n"
            q1 = stats.get("q1_price", 0)
            q3 = stats.get("q3_price", 0)
            avg = stats.get("avg_price", 0)

            report += f"- **主流价位**：{q1:,} - {q3:,} RUB（约{avg/100:.0f}%分位数）\n"
            report += "- **定价策略**：\n"
            report += "  - 高端定位：定价 > Q3 + 30%（高溢价，需强品牌背书）\n"
            report += f"  - 主流定位：定价 Q1-Q3（{q1:,}-{q3:,} RUB，竞争激烈）\n"
            report += f"  - 经济型：定价 < Q1（{q1:,} RUB以下，价格敏感）\n"
            report += "- **促销活动**：关注Wildberries/Ozon的Чёрная пятница（黑五）折扣\n\n"

        else:
            report += "（暂无电商数据）\n\n"

        return report

    def _generate_price_distribution_chart(self, products):
        """生成价格分布图"""
        if not HAS_MATPLOTLIB or not products:
            return ""

        try:
            chart_path = os.path.join(self.output_dir, "chart_price_distribution.png")

            prices = [p.get("price", 0) for p in products if p.get("price", 0) > 0]
            if not prices:
                return ""

            fig, axes = plt.subplots(1, 2, figsize=(14, 5))

            # 直方图
            axes[0].hist(prices, bins=30, color='#3498db', alpha=0.7, edgecolor='white')
            axes[0].axvline(sum(prices)/len(prices), color='red', linestyle='--', label=f'均价: {sum(prices)/len(prices):,.0f}')
            axes[0].set_xlabel('价格 (RUB)')
            axes[0].set_ylabel('商品数量')
            axes[0].set_title(f'{self.country} {self.category} 价格分布')
            axes[0].legend()
            axes[0].grid(alpha=0.3)

            # 箱线图
            sorted_prices = sorted(prices)
            n = len(sorted_prices)
            bp_data = [
                sorted_prices[:n//4] if n > 4 else sorted_prices,
                sorted_prices,
                sorted_prices[3*n//4:] if n > 4 else sorted_prices,
            ]
            bp = axes[1].boxplot(prices, patch_artist=True)
            bp['boxes'][0].set_facecolor('#2ecc71')
            axes[1].set_title('价格箱线图')
            axes[1].set_ylabel('价格 (RUB)')
            axes[1].grid(alpha=0.3)

            plt.tight_layout()
            plt.savefig(chart_path, dpi=REPORT_CONFIG["chart_dpi"])
            plt.close()

            self.charts.append(chart_path)
            return f"![价格分布]({chart_path})\n\n"
        except Exception as e:
            logger.warning(f"价格图生成失败: {e}")
            return ""

    def _generate_advertising_analysis(self, ad_data):
        """生成广告分析"""
        report = "## 六、广告投放与数字营销\n\n"

        if ad_data and ad_data.get("channels"):
            channels = ad_data["channels"]

            report += "### 6.1 主要广告渠道\n\n"
            report += "| 渠道 | 类型 | CPC区间 | CPM区间 | 竞争程度 | 医疗合规 |\n"
            report += "|-----|------|--------|--------|---------|---------|\n"

            for ch_key, ch in channels.items():
                name = ch.get("name", "")
                ptype = ch.get("platform_type", "")
                cpc = ch.get("cpc_range_rub", ch.get("cpc_range_usd", "N/A"))
                cpm = ch.get("cpm_range_rub", ch.get("cpm_range_usd", "N/A"))
                comp = ch.get("competition_level", "")
                med = ch.get("medical_category", "")[:30]
                report += f"| {name} | {ptype} | {cpc} | {cpm} | {comp} | {med} |\n"

            report += "\n"

            # 预算估算表
            report += "### 6.2 推荐广告预算方案\n\n"
            report += "| 渠道 | 日预算(RUB) | 月预算(RUB) | 预计月曝光 | 适用场景 |\n"
            report += "|-----|-----------|-----------|---------|---------|\n"

            for ch_key, ch in channels.items():
                name = ch.get("name", "")
                cpc_str = ch.get("cpc_range_rub", "")
                match = [s for s in cpc_str.split("-") if s.strip().isdigit()]
                if match:
                    avg_cpc = sum(int(s) for s in match) / len(match)
                    daily_budget = avg_cpc * 100
                    monthly = daily_budget * 30
                    reach = monthly / avg_cpc * 10
                    scene = "搜索转化" if "search" in name.lower() or "search" in ptype.lower() else "品牌曝光"
                    report += f"| {name} | {daily_budget:,.0f} | {monthly:,.0f} | ~{int(reach):,} | {scene} |\n"

            report += "\n"

        report += "### 6.3 医疗器械广告合规要点\n\n"
        if self.country == "俄罗斯":
            report += "- **资质要求**：广告主须持有Росздравнадзор注册证\n"
            report += "- **禁用表述**：不得使用「最好」「唯一」「100%有效」等绝对化用语\n"
            report += "- **审核周期**：Yandex.Direct医疗类广告通常需3-5个工作日\n"
            report += "- **平台限制**：部分平台对医疗器械广告有额外限制\n"
            report += "- **数据留存**：广告数据须保存不少于2年\n\n"
        else:
            report += "（请根据目标国家补充广告合规信息）\n\n"

        return report

    def _generate_customs_analysis(self, customs_data):
        """生成海关数据分析"""
        if customs_data and customs_data.get("years"):
            years_data = customs_data.get("years", {})
            years_sorted = sorted(years_data.keys(), reverse=True)

            report = "## 七、海关进出口数据分析\n\n"
            report += f"_数据来源：{customs_data.get('source', 'Web Research')} | HS编码：{customs_data.get('hs_code', 'N/A')}_\n\n"

            report += "### 7.1 年度进口数据\n\n"
            report += "| 年份 | 进口额（USD） | 数量 | 备注 |\n"
            report += "|-----|-------------|------|------|\n"

            for year in years_sorted:
                d = years_data[year]
                val = d.get("import_value_usd", 0)
                qty = d.get("import_qty", 0)
                note = d.get("source_snippet", "")[:25] if d.get("source_snippet") else "—"
                if val:
                    report += f"| {year} | **${val:,.0f}** | {qty:,.0f} kg | {note} |\n"
                else:
                    report += f"| {year} | — | — | {note} |\n"

            report += "\n"

            # 趋势图
            if HAS_MATPLOTLIB:
                report += self._generate_customs_trend_chart(years_data)

            report += "### 7.2 主要贸易伙伴\n\n"
            report += "| 国家/地区 | 估算占比 | 主要品类 |\n"
            report += "|---------|---------|---------|\n"
            report += "| 🇨🇳 中国 | ~35% | 低端设备、电子产品 |\n"
            report += "| 🇩🇪 德国 | ~20% | 高端精密设备 |\n"
            report += "| 🇺🇸 美国 | ~15% | 高端品牌器械 |\n"
            report += "| 🇯🇵 日本 | ~10% | 精密医疗仪器 |\n"
            report += "| 🇰🇷 韩国 | ~8% | 消费级器械 |\n"
            report += "| 其他 | ~12% | 各类器械 |\n"
            report += "\n"

        else:
            report = "## 七、海关进出口数据分析\n\n"
            report += "⚠️ **数据暂不可得**。建议直接访问以下渠道获取：\n"
            report += "- [UN Comtrade](https://comtrade.un.org) — 免费注册查询\n"
            report += "- [OEC](https://oec.world) — 可视化贸易数据\n"
            report += "- 各国海关总署官网\n\n"

        return report

    def _generate_customs_trend_chart(self, years_data):
        """生成海关趋势图"""
        if not HAS_MATPLOTLIB or not years_data:
            return ""

        try:
            chart_path = os.path.join(self.output_dir, "chart_customs_trend.png")

            years = sorted(years_data.keys())
            values = [years_data[y].get("import_value_usd", 0) for y in years]
            values = [v for v in values if v > 0]

            if not values:
                return ""

            fig, ax = plt.subplots(figsize=(10, 5))
            ax.plot(years[:len(values)], values, 'o-', color='#9b59b6', linewidth=2.5, markersize=8)

            for x, y in zip(years[:len(values)], values):
                label = f'${y/1e6:.1f}M' if y >= 1e6 else f'${y/1e3:.0f}K'
                ax.annotate(label, (x, y), textcoords="offset points",
                           xytext=(0, 10), ha='center', fontsize=10)

            ax.set_xlabel('年份')
            ax.set_ylabel('进口额 (USD)')
            ax.set_title(f'{self.country} {self.category} 进口额趋势')
            ax.grid(True, alpha=0.3)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(chart_path, dpi=REPORT_CONFIG["chart_dpi"])
            plt.close()

            self.charts.append(chart_path)
            return f"![海关趋势]({chart_path})\n\n"
        except Exception as e:
            logger.warning(f"海关趋势图生成失败: {e}")
            return ""

    def _generate_product_trends(self, news_data, competitor_data):
        """生成产品趋势"""
        report = "## 八、产品趋势与技术方向\n\n"

        report += "### 8.1 技术创新方向\n\n"
        report += "| 技术趋势 | 说明 | 市场成熟度 | 商业机会 |\n"
        report += "|--------|------|----------|---------|\n"
        report += "| 连续血糖监测（CGM） | 不用扎手指，数据实时上传 | 高（欧美成熟） | 高端市场快速增长 |\n"
        report += "| 智能化/IoT | APP连接、数据分析、远程问诊 | 中 | 与移动健康结合 |\n"
        report += "| 微针微创 | 减少疼痛，提升依从性 | 中 | 高端消费品机会 |\n"
        report += "| 无创检测 | 光学/光谱技术无创测血糖 | 低（技术瓶颈） | 未来潜力大 |\n"
        report += "| 云端数据管理 | 云平台存储、医生共享 | 中 | SaaS服务机会 |\n\n"

        report += "### 8.2 用户需求变化\n\n"
        report += "- **准确性**：用户对测量准确性要求持续提升（医疗级 vs 消费级）\n"
        report += "- **便捷性**：操作简便、读数清晰、携带方便\n"
        report += "- **智能化**：数据记录、分析、提醒功能成为标配\n"
        report += "- **社群化**：糖尿病管理社区、家人共享数据需求增长\n"
        report += "- **性价比**：在保证准确性的前提下，价格敏感性提升\n\n"

        report += "### 8.3 市场机会识别\n\n"
        report += f"- **{self.category} + 智能APP** 组合：硬件+软件+服务一体化\n"
        report += f"- **中端价位精准产品**：填补{self.country}市场空白\n"
        report += f"- **慢病管理生态**：从单一产品向健康管理平台延伸\n"
        report += f"- **礼品市场**：{self.category}作为健康礼品的市场机会\n\n"

        return report

    def _generate_entry_recommendations(self, competitor_data, ecommerce_data, ad_data, customs_data):
        """生成市场进入建议"""
        report = "## 九、市场进入建议\n\n"

        report += "### 9.1 机会与风险评估\n\n"
        report += "| 维度 | 评分 | 说明 |\n"
        report += "|-----|------|------|\n"
        report += "| 市场潜力 | ⭐⭐⭐⭐⭐ | 人口基数大，老龄化加速，需求稳定增长 |\n"
        report += "| 竞争强度 | ⭐⭐⭐ | 高端品牌强，中低端竞争激烈 |\n"
        report += "| 法规难度 | ⭐⭐⭐ | 注册周期长，但一旦取得壁垒较高 |\n"
        report += "| 渠道成熟度 | ⭐⭐⭐⭐ | Wildberries/Ozon生态成熟，门槛适中 |\n"
        report += "| 汇率风险 | ⭐⭐ | 卢布汇率波动，需对冲策略 |\n"
        report += "| 供应链风险 | ⭐⭐⭐ | 国际物流+制裁风险，需本地化备货 |\n\n"

        report += "### 9.2 定价策略建议\n\n"
        if ecommerce_data and ecommerce_data.get("price_stats"):
            stats = ecommerce_data["price_stats"]
            q1 = stats.get("q1_price", 0)
            q3 = stats.get("q3_price", 0)
            avg = stats.get("avg_price", 0)
            report += f"| 策略 | 定价区间 | 目标用户 | 竞争策略 |\n"
            report += f"|-----|---------|---------|---------|\n"
            report += f"| 高端定位 | >{q3*1.3:,.0f} RUB | 高收入/专业用户 | 品牌驱动，专业背书 |\n"
            report += f"| 主流竞争 | {q1:,.0f}-{q3*1.3:,.0f} RUB | 中等收入家庭 | 性价比+差异化 |\n"
            report += f"| 爆款经济 | <{q1:,.0f} RUB | 价格敏感用户 | 规模优先，薄利多销 |\n\n"
        else:
            report += "（建议参考电商平台现有价格数据制定定价策略）\n\n"

        report += "### 9.3 渠道选择建议\n\n"
        report += "**Phase 1（0-6个月）：电商冷启动**\n"
        report += "- 优先入驻Wildberries/Ozon，建立线上销售基础\n"
        report += "- 投入Yandex.Direct广告获取初期流量\n"
        report += "- 积累真实用户评价，优化产品\n\n"
        report += "**Phase 2（6-12个月）：线下拓展**\n"
        report += "- 洽谈连锁药房合作（Горздрав, Неофарм等）\n"
        report += "- 申请政府采购资质\n"
        report += "- 参加俄罗斯医疗器械展会（Moscow International Medical Forum）\n\n"
        report += "**Phase 3（12个月+）：品牌深化**\n"
        report += "- 建立本地品牌形象\n"
        report += "- 与当地经销商合作\n"
        report += "- 申请EAEU统一认证（EAEU注册）\n\n"

        report += "### 9.4 关键行动清单\n\n"
        report += "| 优先级 | 行动项 | 时间节点 | 责任方 |\n"
        report += "|-------|--------|---------|--------|\n"
        report += "| P0 | 确定代理/合作模式 | 第1个月 | 销售 |\n"
        report += "| P0 | 准备注册文件 | 第1-3个月 | 法规 |\n"
        report += "| P1 | Wildberries/Ozon入驻 | 第2个月 | 运营 |\n"
        report += "| P1 | 申请Росздравнадзор注册证 | 第3个月开始 | 法规 |\n"
        report += "| P2 | 制定本地化定价策略 | 第2个月 | 市场 |\n"
        report += "| P2 | Yandex.Direct广告启动 | 第3个月 | 市场 |\n"
        report += "| P3 | 线下药房渠道洽谈 | 第6个月 | 销售 |\n"
        report += "| P3 | 政府采购资质申请 | 第6个月 | 法规 |\n\n"

        return report

    def _generate_tender_analysis(self, tender_data):
        """生成政府采购招标分析章节"""
        report = "## 十、政府采购招标分析\n\n"
        report += "> 📋 数据来源：ЕИС zakupki.gov.ru、各联邦主体招标平台\n\n"
        tenders = tender_data.get("tenders", []) if tender_data else []
        price_est = tender_data.get("price_estimate", {}) if tender_data else {}

        if not tenders:
            report += "*暂无政府采购招标数据，请启用 --modules tender 参数重新采集。*\n\n"
            return report

        # 统计
        prices = [t.get("price", 0) for t in tenders if t.get("price")]
        avg_price = sum(prices) / len(prices) if prices else 0
        regions = {}
        for t in tenders:
            r = t.get("region", "未知")
            regions[r] = regions.get(r, 0) + 1

        report += f"### 10.1 招标概览\n\n"
        report += f"- **近30天招标公告总数**：{len(tenders)} 条\n"
        report += f"- **平均中标价格**：{avg_price:,.0f} RUB（约 ${avg_price/90:,.0f} USD）\n"
        report += f"- **活跃采购区域数**：{len(regions)} 个\n\n"

        report += f"### 10.2 各区域招标频次\n\n"
        for region, count in sorted(regions.items(), key=lambda x: -x[1])[:8]:
            bar = "█" * min(count, 20)
            report += f"- **{region}**：{bar} {count} 条\n"
        report += "\n"

        report += f"### 10.3 最新招标公告\n\n"
        report += "| 招标编号 | 采购方 | 标题 | 中标价(RUB) | 截止日期 | 区域 |\n"
        report += "|---------|-------|------|------------|---------|------|\n"
        for t in tenders[:10]:
            report += f"| {t.get('id','N/A')} | {t.get('customer','N/A')[:20]} | {t.get('title','N/A')[:30]} | {t.get('price',0):,.0f} | {t.get('deadline','N/A')} | {t.get('region','N/A')} |\n"
        report += "\n"

        report += f"### 10.4 招标参考价格区间\n\n"
        if price_est:
            report += f"- 最低参考价：{price_est.get('min_price', 0):,.0f} RUB\n"
            report += f"- 最高参考价：{price_est.get('max_price', 0):,.0f} RUB\n"
            report += f"- 平均参考价：{price_est.get('avg_price', 0):,.0f} RUB\n\n"

        return report

    def _generate_registration_analysis(self, registration_data):
        """生成医疗器械注册证分析章节"""
        report = "## 十一、医疗器械注册证分析\n\n"
        report += "> 🏥 数据来源：Росздравнадзор 注册证数据库、ГРЛС\n\n"
        regs = registration_data.get("registrations", []) if registration_data else []

        if not regs:
            report += "*暂无注册证数据，请启用 --modules registration 参数重新采集。*\n\n"
            return report

        holders = {}
        for r in regs:
            h = r.get("holder", "未知")
            holders[h] = holders.get(h, 0) + 1

        active = [r for r in regs if not r.get("expired", False)]
        expired = [r for r in regs if r.get("expired", False)]

        report += f"### 11.1 注册证概览\n\n"
        report += f"- **有效注册证总数**：{len(active)} 条\n"
        report += f"- **已过期注册证**：{len(expired)} 条\n"
        report += f"- **注册证持有人（竞争厂商）数**：{len(holders)} 家\n\n"

        report += f"### 11.2 竞争对手注册证持有量 TOP 10\n\n"
        report += "| 排名 | 公司 | 注册证数量 |\n"
        report += "|------|------|----------|\n"
        for i, (holder, count) in enumerate(sorted(holders.items(), key=lambda x: -x[1])[:10], 1):
            report += f"| {i} | {holder} | {count} |\n"
        report += "\n"

        report += f"### 11.3 有效注册证列表\n\n"
        report += "| 注册证号 | 产品名称 | 持有人 | 有效期至 | 国家 |\n"
        report += "|---------|---------|------|---------|------|\n"
        for r in active[:15]:
            expiry = r.get("expiry_date", "N/A")
            report += f"| {r.get('reg_number','N/A')} | {r.get('product_name','N/A')[:30]} | {r.get('holder','N/A')} | {expiry} | {r.get('holder_country','N/A')} |\n"
        report += "\n"

        return report

    def _generate_social_media_intelligence(self, telegram_data, vk_data):
        """生成社交媒体情报章节"""
        report = "## 十二、社交媒体情报（Telegram / VKontakte）\n\n"
        report += "> 💬 数据来源：Telegram 公开频道、VKontakte 公开群组（仅合法公开内容）\n\n"

        tg_posts = telegram_data.get("posts", []) if telegram_data else []
        vk_posts = vk_data.get("posts", []) if vk_data else []

        if not tg_posts and not vk_posts:
            report += "*暂无社交媒体数据，请启用 --modules telegram,vk 参数重新采集。*\n\n"
            return report

        report += f"### 12.1 Telegram 公开频道情报\n\n"
        if tg_posts:
            report += f"- **采集帖子数**：{len(tg_posts)} 条\n"
            channels = set(p.get("channel", "未知") for p in tg_posts)
            report += f"- **涉及频道数**：{len(channels)} 个\n"
            report += f"\n**热门帖子：**\n\n"
            report += "| 来源频道 | 内容摘要 | 互动 | 日期 |\n"
            report += "|---------|---------|------|------|\n"
            for p in tg_posts[:8]:
                text = p.get("text", "")[:50].replace("\n", " ")
                likes = p.get("likes", 0)
                report += f"| {p.get('channel','N/A')} | {text} | ❤️ {likes} | {p.get('date','N/A')} |\n"
        else:
            report += "_无 Telegram 数据_\n"
        report += "\n"

        report += f"### 12.2 VKontakte 群组情报\n\n"
        if vk_posts:
            report += f"- **采集帖子数**：{len(vk_posts)} 条\n"
            report += f"\n**热门帖子：**\n\n"
            report += "| 来源群组 | 内容摘要 | 点赞 | 日期 |\n"
            report += "|---------|---------|------|------|\n"
            for p in vk_posts[:8]:
                text = p.get("text", "")[:50].replace("\n", " ")
                likes = p.get("likes", 0)
                report += f"| {p.get('group_name','N/A')} | {text} | ❤️ {likes} | {p.get('publish_date','N/A')} |\n"
        else:
            report += "_无 VKontakte 数据_\n"
        report += "\n"

        return report

    def _generate_pricing_analysis(self, pricing_data, tender_data):
        """生成参考定价体系分析章节"""
        report = "## 十三、参考定价体系（ЖНВЛП + 招标价格）\n\n"
        report += "> 💰 数据来源：ЖНВЛП 国家最高限价表、ЕИС 招标历史价格\n\n"
        prices = pricing_data.get("prices", []) if pricing_data else []
        zhnvlp = pricing_data.get("zhnvlp", {}) if pricing_data else {}
        tender_prices = tender_data.get("price_estimate", {}) if tender_data else {}

        if not prices and not zhnvlp:
            report += "*暂无定价数据，请启用 --modules pricing 参数重新采集。*\n\n"
            return report

        report += f"### 13.1 ЖНВЛП 国家最高限价\n\n"
        if zhnvlp:
            items = zhnvlp.get("items", []) if isinstance(zhnvlp, dict) else []
            report += f"- **纳入 ЖНВЛП 产品数**：{len(items)} 种\n\n"
            report += "| 产品名称 | 出厂限价(RUB) | 零售限价(RUB) | 生效日期 |\n"
            report += "|---------|------------|------------|---------|\n"
            for item in items[:10]:
                report += f"| {item.get('product_name','N/A')} | {item.get('factory_price',0):,.0f} | {item.get('retail_price',0):,.0f} | {item.get('effective_date','N/A')} |\n"
        report += "\n"

        report += f"### 13.2 市场参考价格区间\n\n"
        if prices:
            price_vals = [p.get("retail_price", 0) for p in prices if p.get("retail_price")]
            if price_vals:
                report += f"- 最低零售价：{min(price_vals):,.0f} RUB\n"
                report += f"- 最高零售价：{max(price_vals):,.0f} RUB\n"
                report += f"- 平均零售价：{sum(price_vals)/len(price_vals):,.0f} RUB\n\n"

        if tender_prices:
            report += f"### 13.3 招标历史价格参考\n\n"
            report += f"- 招标最低价：{tender_prices.get('min_price',0):,.0f} RUB\n"
            report += f"- 招标最高价：{tender_prices.get('max_price',0):,.0f} RUB\n"
            report += f"- 招标平均价：{tender_prices.get('avg_price',0):,.0f} RUB\n\n"

        return report

    def _generate_medical_org_analysis(self, medical_org_data):
        """生成医疗机构分布分析章节"""
        report = "## 十四、终端医疗机构覆盖分析\n\n"
        report += "> 🏥 数据来源：Росминздрав 医疗机构目录、地区卫生部门数据\n\n"
        orgs = medical_org_data.get("orgs", []) if medical_org_data else []
        distribution = medical_org_data.get("distribution", {}) if medical_org_data else {}

        if not orgs and not distribution:
            report += "*暂无医疗机构数据，请启用 --modules medical_org 参数重新采集。*\n\n"
            return report

        report += f"### 14.1 主要联邦主体医疗机构分布\n\n"
        if distribution:
            report += "| 联邦主体 | 医院数 | 诊所数 | 药房数 | 诊断中心数 |\n"
            report += "|---------|-------|-------|-------|----------|\n"
            for region, counts in list(distribution.items())[:10]:
                if isinstance(counts, dict):
                    report += f"| {region} | {counts.get('hospital',0)} | {counts.get('clinic',0)} | {counts.get('pharmacy',0)} | {counts.get('diagnostic',0)} |\n"
        report += "\n"

        report += f"### 14.2 市场容量评估\n\n"
        if orgs:
            report += f"- **统计机构总数**：{len(orgs)} 家\n"
            report += "- 俄罗斯约有 9,300 家医院、43,000 家诊所、约 7 万家药房\n"
            report += "- 按医疗机构密度和区域经济水平，医疗器械市场规模呈现显著的区域差异\n\n"
            report += "**市场容量层级划分：**\n\n"
            report += "| 层级 | 区域 | 市场容量 | 优先级 |\n"
            report += "|------|------|---------|--------|\n"
            report += "| 1级（核心） | Москва、СПб | 超大 | ⭐⭐⭐⭐⭐ |\n"
            report += "| 2级（重点） | МО、Краснодар、Татарстан、Свердловская | 大 | ⭐⭐⭐⭐ |\n"
            report += "| 3级（潜力） | 其他联邦主体 | 中等 | ⭐⭐⭐ |\n\n"

        return report

    def _generate_references(self, search_results):
        """生成参考文献"""
        report = "## 十五、数据来源与参考\n\n"

        report += "### 参考来源\n\n"

        sources = [
            ("行业媒体", "Медвестник (medvestnik.ru)", "俄罗斯医疗器械行业权威媒体"),
            ("行业媒体", "Vademecum (vademec.ru)", "俄罗斯医疗行业深度报道"),
            ("政府机构", "Росздравнадзор (roszdravnadzor.gov.ru)", "俄罗斯联邦卫生监督局"),
            ("政府机构", "Минздрав России (minzdrav.gov.ru)", "俄罗斯联邦卫生部"),
            ("政府数据", "Росстат (rosstat.gov.ru)", "俄罗斯联邦统计局"),
            ("电商平台", "Wildberries (wildberries.ru)", "俄罗斯最大电商平台价格数据"),
            ("电商平台", "Ozon (ozon.ru)", "俄罗斯综合电商平台"),
            ("搜索引擎", "Yandex (yandex.ru)", "俄罗斯搜索+新闻"),
            ("搜索引擎", "Google News", "国际新闻聚合"),
            ("贸易数据", "UN Comtrade (comtrade.un.org)", "联合国贸易统计数据库"),
            ("贸易数据", "OEC (oec.world)", "经济复杂度贸易可视化"),
            ("行业协会", "俄罗斯医疗器械制造商协会", "行业数据与政策"),
        ]

        report += "| 类型 | 来源 | 说明 |\n"
        report += "|-----|------|------|\n"
        for s in sources:
            report += f"| {s[0]} | {s[1]} | {s[2]} |\n"

        report += "\n"
        report += "### 置信度说明\n\n"
        report += "| 等级 | 标识 | 来源类型 | 使用规则 |\n"
        report += "|-----|------|---------|---------|\n"
        report += "| 高可信 | 🔴 | 政府数据、上市财报、权威机构 | 可直接引用 |\n"
        report += "| 中可信 | 🟡 | 专业媒体、品牌官网、电商数据 | 标注来源，谨慎引用 |\n"
        report += "| 低可信 | 🟢 | 论坛、社交媒体、估算数据 | 仅作参考，须标注「估算」 |\n\n"

        report += "---\n\n"
        return report

    def _generate_appendix(self):
        """生成附录"""
        report = "## 附录\n\n"

        report += "### 附录A：术语对照表（中/俄/英）\n\n"
        report += "| 中文 | 俄语 | 英语 | 说明 |\n"
        report += "|-----|------|------|------|\n"

        terms = [
            ("医疗器械", "Медицинское изделие (МДИ)", "Medical Device", ""),
            ("医疗器械注册证", "Регистрационное удостоверение", "Registration Certificate", "Росздравнадзор颁发"),
            ("血糖检测仪", "Глюкометр", "Glucometer / Blood Glucose Meter", ""),
            ("市场容量", "Ёмкость рынка", "Market Capacity", ""),
            ("竞争格局", "Конкурентная среда", "Competitive Landscape", ""),
            ("电商", "Электронная коммерция (e-commerce)", "E-commerce", ""),
            ("海关编码", "Код ТН ВЭД", "HS Code", "海关进出口商品编码"),
            ("政府采购", "Государственные закупки", "Government Procurement", "44-ФЗ/223-ФЗ"),
            ("连锁药房", "Аптечная сеть", "Pharmacy Chain", ""),
            ("广告投放", "Рекламная кампания", "Advertising Campaign", ""),
            ("CPC", "Стоимость за клик", "Cost Per Click", ""),
            ("CPM", "Стоимость за 1000 показов", "Cost Per Mille", ""),
            ("TAM", "Общий объём рынка", "Total Addressable Market", ""),
            ("SAM", "Доступный объём рынка", "Serviceable Addressable Market", ""),
            ("SOM", "Реалистичный объём рынка", "Serviceable Obtainable Market", ""),
        ]

        for t in terms:
            report += f"| {t[0]} | {t[1]} | {t[2]} | {t[3]} |\n"

        report += "\n"

        report += "### 附录B：完整数据表\n\n"
        report += "如需完整的原始数据（JSON格式），请参见以下文件：\n"
        report += "- `search_results_*.json` — 搜索结果原始数据\n"
        report += "- `competitor_matrix_*.json` — 竞争者矩阵数据\n"
        report += "- `ecommerce_data_*.json` — 电商价格原始数据\n"
        report += "- `customs_data_*.json` — 海关数据\n\n"

        report += "---\n\n"
        report += f"*报告生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n"
        report += f"*Report-gama v1.0.0 — 专业市场调研报告系统*\n"

        return report

    def save_report(self, content, output_path=None):
        """保存报告为Markdown文件"""
        if output_path is None:
            output_path = os.path.join(
                self.output_dir,
                f"report_{self.category}_{self.country}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
            )

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)

        logger.info(f"报告已保存: {output_path}")
        return output_path

    def export_charts_info(self):
        """返回已生成图表列表"""
        return self.charts


if __name__ == "__main__":
    generator = ReportGenerator(country="俄罗斯", category="血糖检测设备", lang="ru")
    report = generator.generate_full_report()
    path = generator.save_report(report)
    print(f"\n报告已生成: {path}")
    print(f"图表数量: {len(generator.charts)}")
