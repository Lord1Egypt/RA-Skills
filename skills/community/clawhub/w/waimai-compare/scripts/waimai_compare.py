#!/usr/bin/env python3
"""
外卖比价 - 多平台价格对比与红包优惠券查询报告生成器
支持美团外卖、饿了么、京东、淘宝(折淘客/好单库)等平台
"""

import argparse
import json
import sys
import os
from datetime import datetime
from html import escape

# ============ 数据处理 ============

PLATFORM_META = {
    "美团外卖": {"icon": "🟡", "color": "#FFD700", "url": "https://www.meituan.com"},
    "饿了么": {"icon": "🔵", "color": "#0097FF", "url": "https://www.ele.me"},
    "京东外卖": {"icon": "🔴", "color": "#E4393C", "url": "https://www.jd.com"},
    "淘宝": {"icon": "🟠", "color": "#FF5000", "url": "https://www.taobao.com"},
    "京东": {"icon": "🔴", "color": "#E4393C", "url": "https://www.jd.com"},
    "拼多多": {"icon": "🟤", "color": "#E02E24", "url": "https://www.pinduoduo.com"},
}

CSS_TEMPLATE = """
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Microsoft YaHei', sans-serif;
        background: #f5f7fa; color: #333; line-height: 1.6; padding: 20px;
    }
    .container { max-width: 900px; margin: 0 auto; }
    .report-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; padding: 30px; border-radius: 16px; margin-bottom: 24px; text-align: center;
    }
    .report-header h1 { font-size: 28px; margin-bottom: 8px; }
    .report-header .meta { font-size: 14px; opacity: 0.85; }
    .report-header .meta span { margin: 0 12px; }
    .section {
        background: white; border-radius: 12px; padding: 24px; margin-bottom: 20px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    .section-title {
        font-size: 18px; font-weight: 600; margin-bottom: 16px;
        display: flex; align-items: center; gap: 8px;
    }
    .platform-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; }
    .platform-card {
        background: white; border: 2px solid #e8e8e8; border-radius: 12px;
        padding: 20px; transition: all 0.3s; position: relative;
    }
    .platform-card:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.12); }
    .platform-card.best-deal {
        border-color: #FFD700; background: linear-gradient(to bottom, #FFFDE7, white);
        box-shadow: 0 4px 16px rgba(255,215,0,0.3);
    }
    .best-badge {
        position: absolute; top: -12px; right: 16px;
        background: #FFD700; color: #333; font-size: 13px; font-weight: 600;
        padding: 4px 12px; border-radius: 12px; box-shadow: 0 2px 8px rgba(255,215,0,0.4);
    }
    .platform-header { display: flex; align-items: center; gap: 8px; margin-bottom: 12px; }
    .platform-icon { font-size: 24px; }
    .platform-name { font-size: 16px; font-weight: 600; }
    .platform-link { font-size: 12px; color: #667eea; margin-left: auto; text-decoration: none; }
    .platform-link:hover { text-decoration: underline; }
    .price-row { display: flex; gap: 16px; margin-bottom: 8px; }
    .price-item { flex: 1; }
    .price-item.total { background: #f0f4ff; padding: 4px 8px; border-radius: 8px; }
    .price-label { font-size: 12px; color: #888; margin-bottom: 2px; }
    .price-value { font-size: 20px; font-weight: 700; color: #333; }
    .price-value.original { color: #666; }
    .price-value.delivery { color: #888; font-size: 16px; }
    .price-value.saving { color: #E4393C; }
    .price-value.saving-amount { color: #E4393C; }
    .price-note { font-size: 12px; color: #888; margin-top: 8px; }
    .price-range { font-size: 12px; color: #aaa; margin-top: 4px; }
    .summary-box {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        color: #333; padding: 20px; border-radius: 12px; margin-bottom: 20px; text-align: center;
    }
    .summary-box .best-platform { font-size: 22px; font-weight: 700; margin-bottom: 4px; }
    .summary-box .best-price { font-size: 32px; font-weight: 800; color: #E4393C; }
    .summary-box .savings-text { font-size: 14px; color: #555; margin-top: 8px; }
    .coupon-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }
    .coupon-card {
        background: #fff8f0; border-radius: 10px; padding: 16px; transition: all 0.3s;
    }
    .coupon-card:hover { transform: translateY(-1px); box-shadow: 0 3px 10px rgba(0,0,0,0.1); }
    .coupon-header { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
    .coupon-icon { font-size: 20px; }
    .coupon-platform { font-size: 14px; font-weight: 600; }
    .coupon-type { font-size: 12px; background: #FF5000; color: white; padding: 2px 8px; border-radius: 4px; }
    .new-user-badge { font-size: 11px; background: #E4393C; color: white; padding: 2px 6px; border-radius: 4px; }
    .coupon-body { font-size: 13px; color: #555; }
    .coupon-amount { font-size: 22px; font-weight: 700; color: #E4393C; margin-bottom: 4px; }
    .coupon-threshold { color: #888; margin-bottom: 2px; }
    .coupon-validity { color: #888; margin-bottom: 2px; }
    .coupon-how { color: #667eea; }
    .radar-container { text-align: center; }
    #radarChart { max-width: 500px; margin: 0 auto; }
    .notes-list { padding-left: 20px; }
    .notes-list li { margin-bottom: 6px; color: #666; }
    .warning-box {
        background: #fff3cd; border: 1px solid #ffc107; border-radius: 8px;
        padding: 12px 16px; margin-top: 16px; font-size: 13px; color: #856404;
    }
    @media (max-width: 600px) {
        .platform-grid { grid-template-columns: 1fr; }
        .coupon-grid { grid-template-columns: 1fr; }
        .price-row { flex-wrap: wrap; }
    }
"""


def find_best_deal(prices):
    """找出最优组合（考虑优惠后最低价）"""
    best = None
    best_total = float("inf")
    for p in prices:
        total = p.get("estimated_total") or p.get("original_price") or float("inf")
        if isinstance(total, str):
            try:
                total = float(total.split("-")[0])
            except (ValueError, AttributeError):
                total = float("inf")
        if total < best_total:
            best_total = total
            best = p
    return best, best_total


def find_matching_coupon(prices, coupons):
    """为每个平台匹配可用优惠券"""
    result = {}
    for p in prices:
        platform = p.get("platform", "")
        result[platform] = [c for c in coupons if c.get("platform") == platform]
    return result


def parse_number(val, default=0):
    """安全地解析数字值"""
    if isinstance(val, (int, float)):
        return float(val)
    if isinstance(val, str):
        try:
            return float(val.split("-")[0].replace("满", "").replace("元", "").replace("¥", ""))
        except (ValueError, AttributeError):
            return default
    return default


def calculate_savings(prices, coupons_by_platform):
    """计算使用优惠券后的节省金额"""
    savings = {}
    for p in prices:
        platform = p.get("platform", "")
        original = parse_number(p.get("original_price"), 0)
        total_saving = 0
        for c in coupons_by_platform.get(platform, []):
            threshold = parse_number(c.get("threshold"), 0)
            amount = parse_number(c.get("amount"), 0)
            if original >= threshold:
                total_saving += amount
        savings[platform] = total_saving
    return savings


def generate_radar_scores(prices, coupons_by_platform):
    """生成各平台五维雷达评分（价格/配送/优惠/品质/便利）"""
    scores = {}
    for p in prices:
        platform = p.get("platform", "")
        original = parse_number(p.get("original_price"), 50)
        price_score = max(1, 10 - (original / 10))
        coupons = coupons_by_platform.get(platform, [])
        coupon_score = min(10, len(coupons) * 2 + sum(
            parse_number(c.get("amount"), 0) for c in coupons
        ) / 3)
        if platform in ["美团外卖", "饿了么", "京东外卖"]:
            delivery_score = 9
        else:
            delivery_score = 4
        if platform in ["京东外卖", "京东", "饿了么"]:
            quality_score = 8
        elif platform in ["美团外卖", "淘宝"]:
            quality_score = 7
        else:
            quality_score = 6
        if platform in ["美团外卖", "饿了么", "京东外卖"]:
            convenience_score = 9
        else:
            convenience_score = 6
        scores[platform] = {
            "价格": round(price_score, 1),
            "配送": round(delivery_score, 1),
            "优惠": round(coupon_score, 1),
            "品质": round(quality_score, 1),
            "便利": round(convenience_score, 1),
        }
    return scores


def format_price(value):
    """格式化价格显示"""
    if value is None or value == "N/A" or value == "":
        return "&mdash;"
    if isinstance(value, (int, float)):
        return "¥" + str(int(value))
    return "¥" + str(value)


def format_coupon_amount(amount):
    """格式化优惠券金额"""
    if isinstance(amount, (int, float)):
        return "¥" + str(int(amount))
    return str(amount) if amount else ""


def format_coupon_threshold(threshold):
    """格式化优惠券门槛"""
    if isinstance(threshold, (int, float)):
        return "满¥" + str(int(threshold)) + "可用"
    if isinstance(threshold, str):
        return threshold
    if threshold is None or threshold == 0:
        return "无门槛"
    return str(threshold)


def build_platform_card(p, best_deal, savings):
    """构建单个平台卡片HTML"""
    platform = escape(p.get("platform", ""))
    meta = PLATFORM_META.get(p.get("platform", ""), {"icon": "⚪", "color": "#999", "url": "#"})
    is_best = (p == best_deal)
    original_price = p.get("original_price", "N/A")
    typical_range = p.get("typical_range", "")
    delivery_fee = p.get("delivery_fee", "")
    estimated_total = p.get("estimated_total", "N/A")
    note = escape(p.get("note", ""))
    saving = savings.get(p.get("platform", ""), 0)

    best_badge = '<div class="best-badge">🏆 最优选择</div>' if is_best else ""
    best_class = " best-deal" if is_best else ""

    final_price_html = ""
    if isinstance(original_price, (int, float)) and saving > 0:
        final_price_html = (
            '<div class="price-row">'
            '<div class="price-item"><div class="price-label">优惠后</div>'
            '<div class="price-value saving">¥' + str(int(original_price - saving)) + '</div></div>'
            '<div class="price-item"><div class="price-label">可省</div>'
            '<div class="price-value saving-amount">¥' + str(int(saving)) + '</div></div>'
            '</div>'
        )

    note_html = '<div class="price-note">' + note + '</div>' if note else ""
    range_html = '<div class="price-range">常见价格区间：' + escape(str(typical_range)) + '</div>' if typical_range else ""

    return (
        '<div class="platform-card' + best_class + '">'
        + best_badge +
        '<div class="platform-header">'
        '<span class="platform-icon">' + meta["icon"] + '</span>'
        '<span class="platform-name">' + platform + '</span>'
        '<a href="' + meta["url"] + '" target="_blank" class="platform-link">前往 ↗</a>'
        '</div>'
        '<div class="price-row">'
        '<div class="price-item"><div class="price-label">原价</div>'
        '<div class="price-value original">' + format_price(original_price) + '</div></div>'
        '<div class="price-item"><div class="price-label">配送费</div>'
        '<div class="price-value delivery">' + format_price(delivery_fee) + '</div></div>'
        '<div class="price-item total"><div class="price-label">预估总计</div>'
        '<div class="price-value">' + format_price(estimated_total) + '</div></div>'
        '</div>'
        + final_price_html
        + note_html
        + range_html
        + '</div>'
    )


def build_coupon_card(c):
    """构建单个优惠券卡片HTML"""
    platform = escape(c.get("platform", ""))
    meta = PLATFORM_META.get(c.get("platform", ""), {"icon": "⚪", "color": "#999"})
    type_str = escape(c.get("type", "优惠券"))
    amount = c.get("amount", "")
    threshold = c.get("threshold", "")
    validity = escape(c.get("validity", ""))
    how_to_get = escape(c.get("how_to_get", ""))
    is_new_user = c.get("is_new_user_only", False)

    new_badge = '<span class="new-user-badge">限新用户</span>' if is_new_user else ""

    return (
        '<div class="coupon-card" style="border-left: 4px solid ' + meta["color"] + ';">'
        '<div class="coupon-header">'
        '<span class="coupon-icon">' + meta["icon"] + '</span>'
        '<span class="coupon-platform">' + platform + '</span>'
        '<span class="coupon-type">' + type_str + '</span>'
        + new_badge +
        '</div>'
        '<div class="coupon-body">'
        '<div class="coupon-amount">' + format_coupon_amount(amount) + '</div>'
        '<div class="coupon-threshold">' + format_coupon_threshold(threshold) + '</div>'
        '<div class="coupon-validity">有效期：' + validity + '</div>'
        '<div class="coupon-how">领取方式：' + how_to_get + '</div>'
        '</div>'
        '</div>'
    )


def generate_html_report(data, output_path):
    """生成交互式HTML可视化比价报告"""
    product = escape(data.get("product", "未知商品"))
    city = escape(data.get("city", ""))
    query_time = escape(data.get("query_time", datetime.now().strftime("%Y-%m-%d %H:%M")))
    prices = data.get("price_comparison", [])
    coupons = data.get("coupons", [])
    extra_notes = data.get("notes", [])

    # 数据处理
    best_deal, best_total = find_best_deal(prices)
    coupons_by_platform = find_matching_coupon(prices, coupons)
    savings = calculate_savings(prices, coupons_by_platform)
    radar_scores = generate_radar_scores(prices, coupons_by_platform)

    # 构建各部分HTML
    platform_cards_html = "\n".join(build_platform_card(p, best_deal, savings) for p in prices)
    coupon_cards_html = "\n".join(build_coupon_card(c) for c in coupons)
    notes_html = "\n".join("<li>" + escape(n) + "</li>" for n in extra_notes)

    # 最优推荐区域
    summary_html = ""
    if best_deal:
        best_platform = escape(best_deal.get("platform", "未知"))
        best_price_str = format_price(best_total)
        max_saving = max(savings.values()) if savings else 0
        summary_html = (
            '<div class="summary-box">'
            '<div class="best-platform">🏆 最优推荐：' + best_platform + '</div>'
            '<div class="best-price">' + best_price_str + '</div>'
            '<div class="savings-text">使用最优平台+可用优惠，预估可省 ¥' + str(int(max_saving)) + '</div>'
            '</div>'
        )

    # 优惠券区域
    coupon_section_html = ""
    if coupon_cards_html:
        coupon_section_html = (
            '<div class="section">'
            '<div class="section-title">🎫 红包 / 优惠券</div>'
            '<div class="coupon-grid">' + coupon_cards_html + '</div>'
            '</div>'
        )
    else:
        coupon_section_html = (
            '<div class="section">'
            '<div class="section-title">🎫 红包 / 优惠券</div>'
            '<p style="color:#888;text-align:center;padding:20px;">暂未找到可用优惠券，建议在各平台APP内查看最新优惠</p>'
            '</div>'
        )

    # 备注区域
    notes_section_html = ""
    if notes_html:
        notes_section_html = (
            '<div class="section">'
            '<div class="section-title">💡 备注</div>'
            '<ul class="notes-list">' + notes_html + '</ul>'
            '</div>'
        )

    # 雷达图JS数据
    radar_platforms = list(radar_scores.keys())
    radar_dimensions = ["价格", "配送", "优惠", "品质", "便利"]
    radar_platform_colors = {k: PLATFORM_META.get(k, {}).get("color", "#999") for k in radar_platforms}

    radar_js_parts = [
        "const platforms = " + json.dumps(radar_platforms, ensure_ascii=False) + ";",
        "const dimensions = " + json.dumps(radar_dimensions, ensure_ascii=False) + ";",
        "const scores = " + json.dumps(radar_scores, ensure_ascii=False) + ";",
        "const platformColors = " + json.dumps(radar_platform_colors, ensure_ascii=False) + ";",
        "",
        "const datasets = platforms.map((p, i) => ({",
        "    label: p,",
        "    data: dimensions.map(d => scores[p][d] || 0),",
        "    borderColor: platformColors[p] || '#999',",
        "    backgroundColor: (platformColors[p] || '#999') + '20',",
        "    borderWidth: 2,",
        "    pointRadius: 4,",
        "    pointBackgroundColor: platformColors[p] || '#999',",
        "}));",
        "",
        "new Chart(document.getElementById('radarChart'), {",
        "    type: 'radar',",
        "    data: { labels: dimensions, datasets: datasets },",
        "    options: {",
        "        responsive: true,",
        "        scales: {",
        "            r: {",
        "                beginAtZero: true,",
        "                max: 10,",
        "                ticks: { stepSize: 2, font: { size: 11 } },",
        "                pointLabels: { font: { size: 13 } }",
        "            }",
        "        },",
        "        plugins: {",
        "            legend: { position: 'bottom', labels: { font: { size: 13 }, padding: 16 } }",
        "        }",
        "    }",
        "});",
    ]
    radar_js = "\n".join(radar_js_parts)

    # 组装完整HTML
    html_parts = [
        '<!DOCTYPE html>',
        '<html lang="zh-CN">',
        '<head>',
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        '<title>' + product + ' - 多平台比价报告</title>',
        '<style>',
        CSS_TEMPLATE,
        '</style>',
        '<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>',
        '</head>',
        '<body>',
        '<div class="container">',
        # Header
        '<div class="report-header">',
        '<h1>' + product + ' 多平台比价报告</h1>',
        '<div class="meta">',
        '<span>📍 ' + (city or '参考价格') + '</span>',
        '<span>🕐 ' + query_time + '</span>',
        '<span>📊 ' + str(len(prices)) + '个平台</span>',
        '</div>',
        '</div>',
        # Summary
        summary_html,
        # Price comparison
        '<div class="section">',
        '<div class="section-title">📊 价格对比详情</div>',
        '<div class="platform-grid">',
        platform_cards_html,
        '</div>',
        '</div>',
        # Coupons
        coupon_section_html,
        # Radar
        '<div class="section">',
        '<div class="section-title">🎯 平台综合评分</div>',
        '<div class="radar-container">',
        '<canvas id="radarChart"></canvas>',
        '</div>',
        '</div>',
        # Notes
        notes_section_html,
        # Warning
        '<div class="warning-box">',
        '⚠️ 以上价格来自网络搜索汇总，仅供参考。实际价格受定位、时段、店铺等因素影响，请以各平台APP实时显示为准。红包优惠券的金额和门槛也可能随时变化。',
        '</div>',
        '</div>',
        # JS
        '<script>',
        radar_js,
        '</script>',
        '</body>',
        '</html>',
    ]

    html = "\n".join(html_parts)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path


# ============ CLI 入口 ============

def main():
    parser = argparse.ArgumentParser(description="外卖比价报告生成器")
    parser.add_argument("--data", required=True, help="结构化比价数据 JSON")
    parser.add_argument("--output", required=True, help="输出 HTML 文件路径")
    parser.add_argument("--data-file", help="从文件读取 JSON 数据（代替 --data）")

    args = parser.parse_args()

    if args.data_file:
        with open(args.data_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.loads(args.data)

    output_path = generate_html_report(data, args.output)
    print("报告已生成: " + output_path)
    return output_path


if __name__ == "__main__":
    main()
