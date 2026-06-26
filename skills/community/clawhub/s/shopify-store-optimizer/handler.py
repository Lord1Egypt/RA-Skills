#!/usr/bin/env python3
"""
Shopify Store Optimizer - handler.py
Generates store health diagnostic reports based on built-in templates and best-practice libraries.
No real-time API calls are made.
"""

import json
import re
import sys
from typing import Literal

# ─────────────────────────────────────────────
# BUILT-IN TEMPLATES & BEST-PRACTICE LIBRARIES
# ─────────────────────────────────────────────

CONVERSION_TIPS = [
    {
        "issue": "产品页缺少社会证明",
        "suggestion": "添加产品评价插件（Judge.me / Loox），在产品页展示星级评分和真实买家评价",
        "priority": "high",
        "effort_hours": 1,
        "apps": [
            {"name": "Judge.me Product Reviews", "price": "免费起步 / $9/月", "url": "https://judge.me/"},
            {"name": "Loox Reviews & Photos", "price": "$9.9/月", "url": "https://loox.io/"},
            {"name": "Ali Reviews", "price": "免费起步", "url": "https://alireviews.com/"},
        ],
    },
    {
        "issue": "CTA 按钮不够突出",
        "suggestion": "将 'Add to Cart' 按钮改为对比色（与背景形成高对比），增大尺寸，添加微动效",
        "priority": "high",
        "effort_hours": 0.5,
        "apps": [],
    },
    {
        "issue": "缺少信任标识",
        "suggestion": "在产品页和结算页添加安全支付徽章（SSL / Visa / Mastercard）、退款政策提示",
        "priority": "high",
        "effort_hours": 0.5,
        "apps": [
            {"name": "H Trust Badge", "price": "免费 / $5/月", "url": "https://h-trust-badge.com/"},
        ],
    },
    {
        "issue": "未展示库存/热销状态",
        "suggestion": "在产品卡片添加'仅剩 X 件'或'热销中'标签，制造紧迫感",
        "priority": "medium",
        "effort_hours": 0.5,
        "apps": [],
    },
    {
        "issue": "缺少 Urgency / FOMO 元素",
        "suggestion": "添加倒计时插件或'X 人正在查看此商品'浮动通知",
        "priority": "medium",
        "effort_hours": 1,
        "apps": [
            {"name": "Sales Pop Master", "price": "免费 / $9.9/月", "url": "https://sale-pop-master.com/"},
            {"name": "UFE: Urgency Fomo", "price": "$9.9/月", "url": "https://urgency-fomo.com/"},
        ],
    },
    {
        "issue": "结算流程过长",
        "suggestion": "启用 Shopify Checkout 优化，启用 Guest Checkout，减少必填字段",
        "priority": "high",
        "effort_hours": 1,
        "apps": [
            {"name": "Shopify Checkout Plus", "price": "$9/月", "url": "https://checkout-plus.com/"},
        ],
    },
    {
        "issue": "缺少 A/B 测试",
        "suggestion": "引入 Google Optimize 或 Shopify 内置的渠道测试数据，优化产品页文案和布局",
        "priority": "medium",
        "effort_hours": 2,
        "apps": [],
    },
]

SEO_TIPS = [
    {
        "issue": "产品 Meta Title / Description 缺失或重复",
        "suggestion": "为每个产品编写独特、含目标关键词的 Meta Title（50–60字符）和 Description（150–160字符）",
        "priority": "high",
        "effort_hours": 3,
        "apps": [
            {"name": "Plug in SEO", "price": "免费 / $9/月", "url": "https://plugineseo.com/"},
            {"name": "SEO Manager", "price": "$9/月", "url": "https://seomanager.app/"},
            {"name": "Smart SEO", "price": "免费起步", "url": "https://smartseo.app/"},
        ],
    },
    {
        "issue": "图片缺少 Alt 文本",
        "suggestion": "为所有产品图片添加描述性 Alt 文本，包含产品名和目标关键词",
        "priority": "high",
        "effort_hours": 2,
        "apps": [
            {"name": "AltText.ai", "price": "$9/月起", "url": "https://alttext.ai/"},
        ],
    },
    {
        "issue": "URL 结构未做关键词优化",
        "suggestion": "确保产品 URL 包含简短的产品名（而非随机 ID），例如 /products/organic-coffee-beans",
        "priority": "medium",
        "effort_hours": 1,
        "apps": [],
    },
    {
        "issue": "缺少 BLOG / 内容营销",
        "suggestion": "每周发布 1–2 篇与产品相关的博客文章，布局长尾关键词，提升自然流量",
        "priority": "medium",
        "effort_hours": 4,
        "apps": [
            {"name": "Shopify Blog+", "price": "免费", "url": "https://shopify.com/blog"},
        ],
    },
    {
        "issue": "未提交 sitemap.xml",
        "suggestion": "在 Shopify 后台 → 设置 → 搜索引擎主动提交 sitemap.xml 到 Google Search Console",
        "priority": "medium",
        "effort_hours": 0.5,
        "apps": [],
    },
    {
        "issue": "缺少结构化数据（Schema Markup）",
        "suggestion": "为产品页添加 Product Schema，包含价格、评分、库存状态，帮助搜索引擎理解页面内容",
        "priority": "medium",
        "effort_hours": 2,
        "apps": [
            {"name": "Schema Plus", "price": "$5/月", "url": "https://schema-plus.com/"},
        ],
    },
    {
        "issue": "页面加载速度慢",
        "suggestion": "压缩图片（WebP 格式）、启用_lazy load、精简主题代码、使用 CDN",
        "priority": "high",
        "effort_hours": 2,
        "apps": [
            {"name": "TinyIMG", "price": "免费 / $10/月", "url": "https://tinyimg.io/"},
            {"name": "Jetpack", "price": "免费 / $9/月", "url": "https://jetpack.com/"},
        ],
    },
]

UX_TIPS = [
    {
        "issue": "导航层级过深",
        "suggestion": "将重要页面控制在 2–3 次点击内可达；使用 Mega Menu 展示热门分类",
        "priority": "high",
        "effort_hours": 1,
        "apps": [
            {"name": "EA Store Sales", "price": "免费", "url": "https://ea-storesales.com/"},
        ],
    },
    {
        "issue": "缺少站点搜索功能",
        "suggestion": "启用 Shopify 内置搜索，并安装 Boost Commerce 优化搜索排序和过滤体验",
        "priority": "medium",
        "effort_hours": 1,
        "apps": [
            {"name": "Boost Commerce Search & Filter", "price": "$9.9/月", "url": "https://boostcommerce.net/"},
            {"name": "Searchanise", "price": "免费 / $9.9/月", "url": "https://searchanise.com/"},
        ],
    },
    {
        "issue": "移动端体验未优化",
        "suggestion": "使用 Google PageSpeed Insights 测试移动端，根据建议调整图片大小和主题布局",
        "priority": "high",
        "effort_hours": 2,
        "apps": [],
    },
    {
        "issue": "结账页体验差",
        "suggestion": "启用 Express Checkout（Shop Pay / Apple Pay / Google Pay），减少用户输入成本",
        "priority": "high",
        "effort_hours": 1,
        "apps": [
            {"name": "Shop Pay", "price": "免费", "url": "https://shopify.com/checkout"},
        ],
    },
    {
        "issue": "页面布局杂乱",
        "suggestion": "遵循 F 形阅读模式，重要信息（左上→右下）优先展示；留白充足，减少视觉噪音",
        "priority": "medium",
        "effort_hours": 2,
        "apps": [],
    },
    {
        "issue": "缺少 404 页面处理",
        "suggestion": "自定义 404 页面，引导用户返回首页或搜索，避免直接跳出",
        "priority": "low",
        "effort_hours": 0.5,
        "apps": [],
    },
]

APP_CATALOG = {
    "conversion": [
        {"name": "Judge.me Product Reviews", "price": "免费起步 / $9/月", "rationale": "安装量最大的评价插件，支持照片评价和邮件催评"},
        {"name": "Loox Reviews & Photos", "price": "$9.9/月", "rationale": "支持图片评价，自动收集社交媒体图片，有免费试用"},
        {"name": "Ali Reviews", "price": "免费起步", "rationale": "支持速卖通评价导入，免费计划功能完整"},
        {"name": "Sales Pop Master", "price": "免费 / $9.9/月", "rationale": "展示实时销售弹窗，制造紧迫感和社会证明"},
        {"name": "UFE: Urgency Fomo", "price": "$9.9/月", "rationale": "倒计时、库存紧迫感、多合一 urgency 工具"},
        {"name": "H Trust Badge", "price": "免费 / $5/月", "rationale": "在结算页展示支付安全徽章，提升信任度"},
        {"name": "Shop Pay", "price": "免费", "rationale": "Shopify 官方快速支付，转化率提升平均 1.7 倍"},
    ],
    "seo": [
        {"name": "Plug in SEO", "price": "免费 / $9/月", "rationale": "自动检测 100+ SEO 问题，覆盖元标签、死链、结构化数据"},
        {"name": "SEO Manager", "price": "$9/月", "rationale": "批量编辑 Meta 信息，支持 JSON-LD Schema，功能全面"},
        {"name": "Smart SEO", "price": "免费起步", "rationale": "自动生成 Meta 标签和 Alt 文本，适合多产品店铺"},
        {"name": "AltText.ai", "price": "$9/月起", "rationale": "AI 自动为图片生成 Alt 文本，大幅节省人工时间"},
        {"name": "TinyIMG", "price": "免费 / $10/月", "rationale": "自动压缩 Shopify 图片（WebP），提升页面加载速度"},
        {"name": "Schema Plus", "price": "$5/月", "rationale": "一键添加 Product / Review Schema，提升搜索展示效果"},
    ],
    "ux": [
        {"name": "Boost Commerce Search & Filter", "price": "$9.9/月", "rationale": "强大的搜索体验优化，支持过滤、同义词、拼写纠错"},
        {"name": "Searchanise", "price": "免费 / $9.9/月", "rationale": "即时搜索，支持多语言和个性化排序"},
        {"name": "Raja Theme Quick View", "price": "免费", "rationale": "无需打开产品页即可预览，适合产品多的店铺"},
        {"name": "EA Store Sales", "price": "免费", "rationale": "轻量 Mega Menu，优化大型店铺导航"},
    ],
}

CHECKLIST_CONVERSION = [
    "☐ 已安装产品评价插件并在产品页展示评分",
    "☐ 'Add to Cart' 按钮使用高对比色，尺寸≥ 44px",
    "☐ 信任标识（安全支付徽章）已展示在产品页和结算页",
    "☐ 已启用 Guest Checkout，减少结算步骤",
    "☐ 产品页展示库存数量或'热销'标签",
    "☐ 已启用至少一种快速支付（Shop Pay / Apple Pay）",
    "☐ 结算页说明退款政策（可放在 footer 或结算页侧栏）",
]

CHECKLIST_SEO = [
    "☐ 所有产品有独特的 Meta Title（50–60字符）",
    "☐ 所有产品有独特的 Meta Description（150–160字符）",
    "☐ 所有产品图片有描述性 Alt 文本",
    "☐ 产品 URL 包含可读产品名（不含随机 ID）",
    "☐ 已提交 sitemap.xml 到 Google Search Console",
    "☐ 页面加载速度（LCP）经 Google PageSpeed Insights 验证 < 2.5s",
    "☐ 已发布至少 5 篇与产品相关的博客文章",
    "☐ 已添加 Product Schema 结构化数据",
]

CHECKLIST_UX = [
    "☐ Google Mobile-Friendly Test 通过",
    "☐ 重要页面 3 次点击内可达",
    "☐ 启用 Shopify 内置搜索并测试结果相关性",
    "☐ 结算流程≤ 3 步（地址→运输→支付）",
    "☐ 自定义 404 页面已配置",
    "☐ 页面留白充足，无过度拥挤",
    "☐ 字体大小≥ 16px，正文可读性良好",
]

SCORE_THRESHOLDS = {
    "conversion": {"low": 0.5, "medium": 1.0, "high": 2.0},  # industry avg 1.4%-2.5%
    "seo": {"low": 0, "medium": 60, "high": 80},  # score 0-100
    "ux": {"low": 0, "medium": 60, "high": 80},
}

# ─────────────────────────────────────────────
# CORE DIAGNOSTIC ENGINE
# ─────────────────────────────────────────────

class DiagnosticEngine:
    def __init__(self, user_input: str):
        self.raw_input = user_input
        self.area = self._detect_area()
        self.conversion_rate = self._extract_conversion_rate()
        self.products_count = self._extract_products_count()
        self.traffic = self._extract_traffic()

    def _detect_area(self) -> str:
        text = self.raw_input.lower()
        if any(k in text for k in ["seo", "搜索", "meta", "关键词", "google", "排名", "流量", "网站速度"]):
            return "seo"
        if any(k in text for k in ["转化", "conversion", "订单", "销售", "购买", "cart", "checkout", "支付"]):
            return "conversion"
        if any(k in text for k in ["ux", "体验", "用户", "导航", "页面", "速度", "mobile", "移动"]):
            return "ux"
        return "all"

    def _extract_conversion_rate(self) -> float | None:
        m = re.search(r"转化[率\s]*[:：]?\s*([0-9.]+)\s*%", self.raw_input)
        if m:
            return float(m.group(1))
        m = re.search(r"conversion\s*rate\s*[:\-]?\s*([0-9.]+)\s*%", self.raw_input, re.I)
        if m:
            return float(m.group(1))
        m = re.search(r"([0-9.]+)\s*%", self.raw_input)
        if m and len(self.raw_input) < 200:
            return float(m.group(1))
        return None

    def _extract_products_count(self) -> int | None:
        m = re.search(r"(\d+)\s*个?\s*产品", self.raw_input)
        if m:
            return int(m.group(1))
        m = re.search(r"(\d+)\s*products?", self.raw_input, re.I)
        if m:
            return int(m.group(1))
        return None

    def _extract_traffic(self) -> int | None:
        m = re.search(r"月\s*访问[量是]*[:：]?\s*([0-9,]+)", self.raw_input)
        if m:
            return int(m.group(1).replace(",", ""))
        m = re.search(r"月\s*流量[:：]?\s*([0-9,]+)", self.raw_input)
        if m:
            return int(m.group(1).replace(",", ""))
        m = re.search(r"([0-9,]+)\s*(?:monthly|month)\s*(?:visits?|traffic)", self.raw_input, re.I)
        if m:
            return int(m.group(1).replace(",", ""))
        return None

    def _score_conversion(self) -> tuple[str, str]:
        cr = self.conversion_rate
        if cr is None:
            return "unknown", "🟡 中等（数据不足）"
        if cr < 1.0:
            return "low", "🔴 偏低"
        if cr < 1.5:
            return "medium", "🟡 中等"
        return "high", "🟢 良好"

    def _score_seo(self) -> tuple[str, str]:
        # No real API, return medium by default with advisory note
        return "medium", "🟡 中等（建议配合 Google Search Console 确认）"

    def _score_ux(self) -> tuple[str, str]:
        return "medium", "🟡 中等（建议用 Google PageSpeed Insights 自测）"

    def generate_report(self) -> str:
        area = self.area

        lines = [
            "## 🏪 Shopify 店铺健康度报告",
            "",
            "### 📊 整体健康度",
        ]

        if area == "all":
            cr_score, cr_label = self._score_conversion()
            seo_score, seo_label = self._score_seo()
            ux_score, ux_label = self._score_ux()

            # Overall
            scores = [cr_score, seo_score, ux_score]
            if "unknown" in scores:
                scores = [s for s in scores if s != "unknown"]
            if not scores:
                overall = "🟡 中等（信息不足，请提供更多店铺数据以获得精准诊断）"
            elif scores.count("low") >= 2:
                overall = "⚠️ 中等偏低（多个维度存在优化空间）"
            elif scores.count("high") >= 2:
                overall = "✅ 良好（店铺整体表现健康）"
            else:
                overall = "⚠️ 中等（有改善空间）"

            lines.append(overall)
            lines.append("")
            lines.append("| 诊断维度 | 健康评分 |")
            lines.append("|----------|----------|")
            lines.append(f"| 转化率 | {cr_label} |")
            lines.append(f"| SEO | {seo_label} |")
            lines.append(f"| 用户体验 | {ux_label} |")

        elif area == "conversion":
            cr_score, cr_label = self._score_conversion()
            lines.append(cr_label)
            if self.conversion_rate:
                lines.append(f"（当前值：{self.conversion_rate}%，行业均值 1.4%–2.5%）")

        elif area == "seo":
            seo_score, seo_label = self._score_seo()
            lines.append(seo_label)

        elif area == "ux":
            ux_score, ux_label = self._score_ux()
            lines.append(ux_label)

        lines.append("")
        lines.append("---")
        lines.append("")

        # ── Conversion Section ──
        if area in ("all", "conversion"):
            cr_score, cr_label = self._score_conversion()
            lines.extend([
                "### 1️⃣ 转化率分析 — 得分：" + cr_label,
                "",
            ])
            if self.conversion_rate and self.traffic:
                expected_low = self.traffic * 0.014
                expected_high = self.traffic * 0.025
                lines.extend([
                    f"**数据概览：**",
                    f"- 当前转化率：{self.conversion_rate}%",
                    f"- 月访问量：{self.traffic:,}",
                    f"- 预期月订单（行业均值）：{expected_low:.0f}–{expected_high:.0f}",
                    f"- 实际月订单（估算）：约 {self.traffic * self.conversion_rate / 100:.0f}",
                    "",
                ])
            elif self.conversion_rate:
                lines.append(f"**当前转化率：{self.conversion_rate}%**（行业均值 1.4%–2.5%）")

            lines.extend(["**转化率最佳实践检查清单：**"])
            for item in CHECKLIST_CONVERSION:
                lines.append(item)
            lines.append("")

            if cr_score in ("low", "medium", "unknown"):
                lines.append("**重点优化建议：**")
                for tip in CONVERSION_TIPS[:4]:
                    lines.append(f"- 🔸 **{tip['issue']}**：{tip['suggestion']}")
                    if tip["apps"]:
                        for app in tip["apps"][:2]:
                            lines.append(f"  - {app['name']}（{app['price']}）")
                lines.append("")

        # ── SEO Section ──
        if area in ("all", "seo"):
            lines.extend([
                "### 2️⃣ SEO 分析 — 得分：🟡 中等",
                "",
                "*提示：无实时 API 访问，建议配合 Google Search Console 和 Google PageSpeed Insights 获取真实数据。*",
                "",
                "**SEO 最佳实践检查清单：**",
            ])
            for item in CHECKLIST_SEO:
                lines.append(item)
            lines.append("")

            lines.append("**重点优化建议：**")
            for tip in SEO_TIPS[:4]:
                lines.append(f"- 🔸 **{tip['issue']}**：{tip['suggestion']}")
                if tip["apps"]:
                    for app in tip["apps"][:2]:
                        lines.append(f"  - {app['name']}（{app['price']}）")
            lines.append("")

        # ── UX Section ──
        if area in ("all", "ux"):
            lines.extend([
                "### 3️⃣ 用户体验分析 — 得分：🟡 中等",
                "",
                "*提示：建议使用 Google PageSpeed Insights（pagespeed.web.dev）实测移动端体验。*",
                "",
                "**用户体验最佳实践检查清单：**",
            ])
            for item in CHECKLIST_UX:
                lines.append(item)
            lines.append("")

            lines.append("**重点优化建议：**")
            for tip in UX_TIPS[:4]:
                lines.append(f"- 🔸 **{tip['issue']}**：{tip['suggestion']}")
                if tip["apps"]:
                    for app in tip["apps"][:2]:
                        lines.append(f"  - {app['name']}（{app['price']}）")
            lines.append("")

        # ── App Recommendations ──
        lines.extend([
            "### 🌐 推荐 App 汇总",
            "",
            "**转化率提升：**",
        ])
        for app in APP_CATALOG["conversion"][:4]:
            lines.append(f"- **{app['name']}** — {app['price']}  \n  {app['rationale']}")
        lines.append("")
        lines.append("**SEO 优化：**")
        for app in APP_CATALOG["seo"][:4]:
            lines.append(f"- **{app['name']}** — {app['price']}  \n  {app['rationale']}")
        lines.append("")
        lines.append("**用户体验：**")
        for app in APP_CATALOG["ux"][:3]:
            lines.append(f"- **{app['name']}** — {app['price']}  \n  {app['rationale']}")
        lines.append("")

        # ── Priority Action Items ──
        if area == "all":
            lines.extend([
                "### 📋 下一步行动清单（优先级排序）",
                "",
                "| 优先级 | 行动 | 预计时间 |",
                "|--------|------|---------|",
                "| 🔴 高 | 安装评价插件（Judge.me） | 1–2 小时 |",
                "| 🔴 高 | 优化产品页 Meta 信息 | 3–4 小时 |",
                "| 🟡 中 | 添加信任标识到结算页 | 30 分钟 |",
                "| 🟡 中 | 启用 SEO App 扫描问题 | 20 分钟 |",
                "| 🟢 低 | 优化导航和站点搜索 | 1–2 小时 |",
                "",
            ])

        lines.extend([
            "---",
            "",
            "*本报告基于 Shopify 最佳实践库生成，不涉及实时 API 调用。建议定期复检并结合 Google Analytics / Search Console 数据做最终判断。*",
        ])

        return "\n".join(lines)


# ─────────────────────────────────────────────
# HANDLER ENTRY POINT
# ─────────────────────────────────────────────

def handle(user_input: str) -> str:
    """
    Main handler. Takes a user query string and returns a markdown report.
    """
    engine = DiagnosticEngine(user_input)
    return engine.generate_report()


if __name__ == "__main__":
    # Self-test / demo mode
    print("=" * 60)
    print("Shopify Store Optimizer - Self Test")
    print("=" * 60)
    print()

    test_cases = [
        # Test 1: Full diagnostic
        "我的Shopify店有50个产品，月访问量3000，但转化率只有0.8%，帮我看看哪里有问题",
        # Test 2: SEO only
        "我的Shopify店SEO做得怎么样？",
        # Test 3: App recommendation
        "推荐一些能提高转化率的App",
        # Test 4: English input
        "My Shopify store has low conversion rate, what should I do?",
    ]

    for i, tc in enumerate(test_cases, 1):
        print(f"\n{'─' * 60}")
        print(f"[Test Case {i}]")
        print(f"Input: {tc}")
        print()
        result = handle(tc)
        print(result)
        print()

    print("=" * 60)
    print("All self-test cases completed.")
    print("=" * 60)
