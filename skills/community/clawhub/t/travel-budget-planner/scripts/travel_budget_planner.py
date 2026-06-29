#!/usr/bin/env python3
"""旅行预算规划师 - Travel Budget Planner
根据目的地、出行天数、出行风格估算旅行预算，提供费用分解和省钱建议
纯本地数据，无需外部API
"""
import json
import sys
from datetime import datetime

# ========== 目地消费数据库 ==========
# 每个目的地含：日均住宿/餐饮/交通/景点/杂费（按穷游/经济/舒适/豪华 四档）

DESTINATIONS = {
    # ===== 亚洲 =====
    "东京": {
        "country": "日本", "currency": "JPY", "rate": 4.8,
        "budget": {
            "穷游":   {"住宿": 150, "餐饮": 100, "交通": 60, "景点": 30, "杂费": 30},
            "经济":   {"住宿": 400, "餐饮": 200, "交通": 80, "景点": 50, "杂费": 50},
            "舒适":   {"住宿": 800, "餐饮": 400, "交通": 100, "景点": 80, "杂费": 80},
            "豪华":   {"住宿": 2000, "餐饮": 800, "交通": 200, "景点": 150, "杂费": 200},
        },
        "tips": ["买72小时地铁通票省交通费", "便利店早餐300日元搞定", "免税率10%，消费满5000日元可退税"],
    },
    "大阪": {
        "country": "日本", "currency": "JPY", "rate": 4.8,
        "budget": {
            "穷游":   {"住宿": 120, "餐饮": 80, "交通": 50, "景点": 20, "杂费": 25},
            "经济":   {"住宿": 350, "餐饮": 150, "交通": 70, "景点": 40, "杂费": 40},
            "舒适":   {"住宿": 700, "餐饮": 350, "交通": 90, "景点": 70, "杂费": 70},
            "豪华":   {"住宿": 1800, "餐饮": 700, "交通": 180, "景点": 130, "杂费": 180},
        },
        "tips": ["大阪周游卡含28个景点免费", "道顿堀小吃比东京便宜20%", "黑门市场可现场吃海鲜"],
    },
    "首尔": {
        "country": "韩国", "currency": "KRW", "rate": 195,
        "budget": {
            "穷游":   {"住宿": 100, "餐饮": 80, "交通": 30, "景点": 15, "杂费": 20},
            "经济":   {"住宿": 300, "餐饮": 150, "交通": 50, "景点": 30, "杂费": 40},
            "舒适":   {"住宿": 600, "餐饮": 300, "交通": 80, "景点": 60, "杂费": 60},
            "豪华":   {"住宿": 1500, "餐饮": 600, "交通": 150, "景点": 120, "杂费": 150},
        },
        "tips": ["T-money交通卡地铁公交通用", "明洞换汇汇率最好", "免税店购物满3万韩元可退税"],
    },
    "曼谷": {
        "country": "泰国", "currency": "THB", "rate": 4.5,
        "budget": {
            "穷游":   {"住宿": 50, "餐饮": 40, "交通": 15, "景点": 10, "杂费": 10},
            "经济":   {"住宿": 150, "餐饮": 80, "交通": 30, "景点": 20, "杂费": 25},
            "舒适":   {"住宿": 400, "餐饮": 200, "交通": 60, "景点": 40, "杂费": 50},
            "豪华":   {"住宿": 1200, "餐饮": 500, "交通": 150, "景点": 100, "杂费": 150},
        },
        "tips": ["BTS一日通票140泰铢无限乘", "街头小吃30-50泰铢一餐", "大皇宫等景点提前网上购票"],
    },
    "新加坡": {
        "country": "新加坡", "currency": "SGD", "rate": 5.4,
        "budget": {
            "穷游":   {"住宿": 200, "餐饮": 80, "交通": 20, "景点": 15, "杂费": 15},
            "经济":   {"住宿": 500, "餐饮": 200, "交通": 40, "景点": 30, "杂费": 30},
            "舒适":   {"住宿": 1000, "餐饮": 400, "交通": 70, "景点": 60, "杂费": 60},
            "豪华":   {"住宿": 2500, "餐饮": 800, "交通": 150, "景点": 120, "杂费": 150},
        },
        "tips": ["新加坡游客通行卡含公共交通", "小贩中心3-5新币一餐", "GST 9%，部分商店可退税"],
    },
    "巴厘岛": {
        "country": "印尼", "currency": "IDR", "rate": 0.00045,
        "budget": {
            "穷游":   {"住宿": 60, "餐饮": 30, "交通": 20, "景点": 5, "杂费": 10},
            "经济":   {"住宿": 200, "餐饮": 80, "交通": 50, "景点": 15, "杂费": 25},
            "舒适":   {"住宿": 500, "餐饮": 200, "交通": 100, "景点": 30, "杂费": 50},
            "豪华":   {"住宿": 1500, "餐饮": 500, "交通": 200, "景点": 80, "杂费": 120},
        },
        "tips": ["租摩托车最划算日均50元", "乌布和库塔物价差30%", "砍价是常态，先从6折开始"],
    },
    "吉隆坡": {
        "country": "马来西亚", "currency": "MYR", "rate": 1.55,
        "budget": {
            "穷游":   {"住宿": 50, "餐饮": 30, "交通": 10, "景点": 5, "杂费": 10},
            "经济":   {"住宿": 150, "餐饮": 60, "交通": 25, "景点": 15, "杂费": 20},
            "舒适":   {"住宿": 400, "餐饮": 150, "交通": 50, "景点": 30, "杂费": 40},
            "豪华":   {"住宿": 1000, "餐饮": 400, "交通": 120, "景点": 80, "杂费": 100},
        },
        "tips": ["吉隆坡消费东南亚最低之一", "Grab打车比出租便宜50%", "双子塔免费但需提前预约"],
    },

    # ===== 中国热门 =====
    "三亚": {
        "country": "中国", "currency": "CNY", "rate": 1,
        "budget": {
            "穷游":   {"住宿": 80, "餐饮": 50, "交通": 20, "景点": 10, "杂费": 15},
            "经济":   {"住宿": 250, "餐饮": 100, "交通": 40, "景点": 30, "杂费": 30},
            "舒适":   {"住宿": 600, "餐饮": 200, "交通": 80, "景点": 50, "杂费": 50},
            "豪华":   {"住宿": 2000, "餐饮": 500, "交通": 200, "景点": 100, "杂费": 150},
        },
        "tips": ["淡季5-9月酒店价格减半", "海鲜去第一市场自买加工", "免税店每人每年10万额度"],
    },
    "成都": {
        "country": "中国", "currency": "CNY", "rate": 1,
        "budget": {
            "穷游":   {"住宿": 60, "餐饮": 40, "交通": 15, "景点": 5, "杂费": 10},
            "经济":   {"住宿": 180, "餐饮": 80, "交通": 30, "景点": 20, "杂费": 25},
            "舒适":   {"住宿": 400, "餐饮": 150, "交通": 50, "景点": 40, "杂费": 40},
            "豪华":   {"住宿": 1000, "餐饮": 400, "交通": 120, "景点": 80, "杂费": 100},
        },
        "tips": ["成都消费一线城市最低", "火锅人均60-80元", "大熊猫基地早上7:30人最少"],
    },
    "丽江": {
        "country": "中国", "currency": "CNY", "rate": 1,
        "budget": {
            "穷游":   {"住宿": 50, "餐饮": 30, "交通": 15, "景点": 5, "杂费": 10},
            "经济":   {"住宿": 150, "餐饮": 60, "交通": 30, "景点": 15, "杂费": 20},
            "舒适":   {"住宿": 400, "餐饮": 120, "交通": 60, "景点": 30, "杂费": 40},
            "豪华":   {"住宿": 1200, "餐饮": 300, "交通": 150, "景点": 60, "杂费": 100},
        },
        "tips": ["束河比大研古城安静且便宜", "淡季11-3月住宿打3折", "玉龙雪山提前一天买票"],
    },
    "厦门": {
        "country": "中国", "currency": "CNY", "rate": 1,
        "budget": {
            "穷游":   {"住宿": 70, "餐饮": 40, "交通": 15, "景点": 5, "杂费": 10},
            "经济":   {"住宿": 200, "餐饮": 80, "交通": 30, "景点": 20, "杂费": 25},
            "舒适":   {"住宿": 500, "餐饮": 150, "交通": 50, "景点": 40, "杂费": 40},
            "豪华":   {"住宿": 1200, "餐饮": 400, "交通": 120, "景点": 80, "杂费": 100},
        },
        "tips": ["鼓浪屿船票提前3天买", "曾厝垵民宿淡季100出头", "海鲜8月禁渔期价格高"],
    },

    # ===== 欧洲 =====
    "巴黎": {
        "country": "法国", "currency": "EUR", "rate": 7.8,
        "budget": {
            "穷游":   {"住宿": 200, "餐饮": 150, "交通": 30, "景点": 20, "杂费": 20},
            "经济":   {"住宿": 500, "餐饮": 300, "交通": 60, "景点": 40, "杂费": 40},
            "舒适":   {"住宿": 1200, "餐饮": 600, "交通": 100, "景点": 80, "杂费": 80},
            "豪华":   {"住宿": 3000, "餐饮": 1200, "交通": 200, "景点": 150, "杂费": 200},
        },
        "tips": ["巴黎博物馆通票2日62欧含60+博物馆", "地铁10次票比单次便宜40%", "超市买法棍+奶酪=3欧午餐"],
    },
    "伦敦": {
        "country": "英国", "currency": "GBP", "rate": 9.2,
        "budget": {
            "穷游":   {"住宿": 250, "餐饮": 150, "交通": 40, "景点": 15, "杂费": 20},
            "经济":   {"住宿": 600, "餐饮": 300, "交通": 60, "景点": 30, "杂费": 40},
            "舒适":   {"住宿": 1500, "餐饮": 600, "交通": 100, "景点": 60, "杂费": 80},
            "豪华":   {"住宿": 4000, "餐饮": 1200, "交通": 200, "景点": 120, "杂费": 200},
        },
        "tips": ["伦敦最贵城市之一", "Oyster卡每日封顶7.5英镑", "大英博物馆/国家美术馆免费"],
    },
    "罗马": {
        "country": "意大利", "currency": "EUR", "rate": 7.8,
        "budget": {
            "穷游":   {"住宿": 150, "餐饮": 120, "交通": 20, "景点": 15, "杂费": 15},
            "经济":   {"住宿": 400, "餐饮": 250, "交通": 40, "景点": 30, "杂费": 35},
            "舒适":   {"住宿": 1000, "餐饮": 500, "交通": 80, "景点": 60, "杂费": 60},
            "豪华":   {"住宿": 2500, "餐饮": 1000, "交通": 180, "景点": 120, "杂费": 150},
        },
        "tips": ["罗马Pass含交通+2个景点", "自来水可直饮，带水瓶省钱", "意式早餐3欧：咖啡+可颂"],
    },

    # ===== 北美 =====
    "纽约": {
        "country": "美国", "currency": "USD", "rate": 7.2,
        "budget": {
            "穷游":   {"住宿": 300, "餐饮": 200, "交通": 40, "景点": 15, "杂费": 20},
            "经济":   {"住宿": 800, "餐饮": 400, "交通": 60, "景点": 30, "杂费": 40},
            "舒适":   {"住宿": 2000, "餐饮": 800, "交通": 100, "景点": 60, "杂费": 80},
            "豪华":   {"住宿": 5000, "餐饮": 2000, "交通": 200, "景点": 120, "杂费": 200},
        },
        "tips": ["纽约消费全美最高", "地铁7日通票33美元", "博物馆建议捐赠入场(MoMA除外)"],
    },
    "洛杉矶": {
        "country": "美国", "currency": "USD", "rate": 7.2,
        "budget": {
            "穷游":   {"住宿": 250, "餐饮": 150, "交通": 50, "景点": 15, "杂费": 20},
            "经济":   {"住宿": 600, "餐饮": 300, "交通": 80, "景点": 30, "杂费": 35},
            "舒适":   {"住宿": 1500, "餐饮": 600, "交通": 120, "景点": 60, "杂费": 60},
            "豪华":   {"住宿": 4000, "餐饮": 1500, "交通": 200, "景点": 120, "杂费": 150},
        },
        "tips": ["租车比打车划算", "环球影城工作日票便宜30%", "In-N-Out汉堡5美元吃到饱"],
    },

    # ===== 大洋洲 =====
    "悉尼": {
        "country": "澳大利亚", "currency": "AUD", "rate": 4.8,
        "budget": {
            "穷游":   {"住宿": 200, "餐饮": 120, "交通": 30, "景点": 15, "杂费": 20},
            "经济":   {"住宿": 500, "餐饮": 250, "交通": 50, "景点": 30, "杂费": 35},
            "舒适":   {"住宿": 1200, "餐饮": 500, "交通": 80, "景点": 60, "杂费": 60},
            "豪华":   {"住宿": 3000, "餐饮": 1000, "交通": 180, "景点": 120, "杂费": 150},
        },
        "tips": ["Opal卡周日封顶2.8澳元", "鱼市场比餐厅便宜50%", "蓝山国家公园免费"],
    },

    # ===== 中东 =====
    "迪拜": {
        "country": "阿联酋", "currency": "AED", "rate": 1.95,
        "budget": {
            "穷游":   {"住宿": 200, "餐饮": 80, "交通": 20, "景点": 15, "杂费": 15},
            "经济":   {"住宿": 500, "餐饮": 200, "交通": 50, "景点": 30, "杂费": 30},
            "舒适":   {"住宿": 1500, "餐饮": 500, "交通": 100, "景点": 60, "杂费": 60},
            "豪华":   {"住宿": 5000, "餐饮": 1500, "交通": 300, "景点": 200, "杂费": 200},
        },
        "tips": ["迪拜免税店全球最便宜之一", "Nol卡乘地铁/巴士通用", "斋月期间白天餐饮受限"],
    },
}

# 机票预估（人民币，单程，中国出发）
FLIGHT_ESTIMATE = {
    "日本": {"穷游": 800, "经济": 1500, "舒适": 3000, "豪华": 6000},
    "韩国": {"穷游": 600, "经济": 1200, "舒适": 2500, "豪华": 5000},
    "泰国": {"穷游": 500, "经济": 1000, "舒适": 2000, "豪华": 4000},
    "新加坡": {"穷游": 700, "经济": 1500, "舒适": 3000, "豪华": 6000},
    "印尼": {"穷游": 800, "经济": 1500, "舒适": 3000, "豪华": 5000},
    "马来西亚": {"穷游": 600, "经济": 1200, "舒适": 2500, "豪华": 5000},
    "法国": {"穷游": 2500, "经济": 4500, "舒适": 8000, "豪华": 15000},
    "英国": {"穷游": 2500, "经济": 5000, "舒适": 9000, "豪华": 18000},
    "意大利": {"穷游": 2500, "经济": 4500, "舒适": 8000, "豪华": 15000},
    "美国": {"穷游": 3000, "经济": 5500, "舒适": 10000, "豪华": 20000},
    "澳大利亚": {"穷游": 2000, "经济": 4000, "舒适": 7000, "豪华": 14000},
    "阿联酋": {"穷游": 2000, "经济": 4000, "舒适": 7000, "豪华": 12000},
    "中国": {"穷游": 300, "经济": 800, "舒适": 1500, "豪华": 3000},
}

# 签证费用预估（人民币）
VISA_COST = {
    "日本": 200, "韩国": 0, "泰国": 0, "新加坡": 0,
    "印尼": 0, "马来西亚": 0, "法国": 600, "英国": 1000,
    "意大利": 600, "美国": 1100, "澳大利亚": 1000, "阿联酋": 0, "中国": 0,
}


def cmd_plan(destination, days=5, style="经济", people=1, include_flight=True):
    """生成旅行预算规划"""
    if destination not in DESTINATIONS:
        # 模糊匹配
        matched = [d for d in DESTINATIONS if destination in d]
        if not matched:
            available = "、".join(sorted(DESTINATIONS.keys()))
            return json.dumps({
                "status": "error",
                "message": f"暂不支持「{destination}」，目前支持：{available}"
            }, ensure_ascii=False)
        destination = matched[0]

    dest = DESTINATIONS[destination]
    style = style if style in dest["budget"] else "经济"
    budget = dest["budget"][style]
    country = dest["country"]
    days = max(1, min(90, int(days)))
    people = max(1, min(10, int(people)))

    # 计算各项费用（人民币/天/人）
    daily_total = sum(budget.values())
    total_days = daily_total * days * people

    # 机票
    flight_cost = 0
    if include_flight and country in FLIGHT_ESTIMATE:
        flight_cost = FLIGHT_ESTIMATE[country].get(style, 0) * 2 * people  # 往返

    # 签证
    visa_cost = VISA_COST.get(country, 0) * people

    # 保险
    insurance_cost = 30 * days * people if country != "中国" else 5 * days * people

    # 总计
    total = total_days + flight_cost + visa_cost + insurance_cost

    # 构建输出
    output = f"💰 **{destination}旅行预算规划**\n\n"
    output += f"**出行信息**：{destination}（{country}） · {days}天 · {people}人 · {style}风格\n\n"
    output += "---\n\n"

    # 日均消费分解
    output += "## 📊 日均消费分解（人民币/人/天）\n\n"
    output += "| 项目 | 日均 | {0}天小计 |\n|------|------|------------|\n".format(days)
    for item, cost in budget.items():
        emoji = {"住宿": "🏨", "餐饮": "🍽️", "交通": "🚗", "景点": "🎫", "杂费": "📦"}.get(item, "📋")
        output += f"| {emoji} {item} | ¥{cost} | ¥{cost * days} |\n"
    output += f"| **日均合计** | **¥{daily_total}** | **¥{daily_total * days}** |\n\n"

    # 总预算汇总
    output += "## 💵 总预算汇总（人民币）\n\n"
    output += "| 项目 | 金额 |\n|------|------|\n"
    output += f"| 🏨 餐住行等({days}天×{people}人) | ¥{total_days:,} |\n"
    if flight_cost:
        output += f"| ✈️ 往返机票({people}人) | ¥{flight_cost:,} |\n"
    if visa_cost:
        output += f"| 📄 签证({people}人) | ¥{visa_cost:,} |\n"
    output += f"| 🛡️ 旅行保险({people}人) | ¥{insurance_cost:,} |\n"
    output += f"| **💰 预估总计** | **¥{total:,}** |\n"
    output += f"| **人均** | **¥{total // people:,}** |\n\n"

    # 对比其他风格
    output += "## 📈 不同风格对比（{0}天·{1}人·人均）\n\n".format(days, people)
    output += "| 风格 | 人均预算 | 说明 |\n|------|---------|------|\n"
    for s in ["穷游", "经济", "舒适", "豪华"]:
        if s in dest["budget"]:
            s_daily = sum(dest["budget"][s].values())
            s_flight = FLIGHT_ESTIMATE.get(country, {}).get(s, 0) * 2 if include_flight else 0
            s_visa = visa_cost
            s_insurance = insurance_cost
            s_total = (s_daily * days + s_flight + s_visa + s_insurance)
            desc = {"穷游": "青旅+街头小吃+公交", "经济": "经济酒店+普通餐厅+公共交通",
                    "舒适": "四星酒店+特色餐厅+打车", "豪华": "五星酒店+米其林+专车"}
            marker = " 👈" if s == style else ""
            output += f"| {s} | ¥{s_total:,}{marker} | {desc.get(s, '')} |\n"
    output += "\n"

    # 省钱建议
    if dest.get("tips"):
        output += "## 💡 省钱建议\n\n"
        for tip in dest["tips"]:
            output += f"- {tip}\n"
        output += "\n"

    output += "---\n📌 *以上为估算参考，实际费用受季节/汇率/个人消费习惯影响。机票价格波动大，建议提前1-2月关注。*\n"

    return output


def cmd_compare(destinations_str, days=5, style="经济"):
    """对比多个目的地的预算"""
    destinations = [d.strip() for d in destinations_str.split(",") if d.strip()]
    if not destinations:
        return json.dumps({"status": "error", "message": "请提供目的地列表，用逗号分隔，如 东京,首尔,曼谷"}, ensure_ascii=False)

    valid_dests = []
    for d in destinations:
        if d in DESTINATIONS:
            valid_dests.append(d)
        else:
            matched = [x for x in DESTINATIONS if d in x]
            if matched:
                valid_dests.append(matched[0])

    if not valid_dests:
        return json.dumps({"status": "error", "message": "没有匹配的目的地"}, ensure_ascii=False)

    style = style if style in ["穷游", "经济", "舒适", "豪华"] else "经济"
    days = max(1, min(90, int(days)))

    output = f"📊 **多目的地预算对比**（{days}天·{style}风格·1人）\n\n"
    output += "| 目的地 | 国家 | 日均 | 机票(往返) | 签证 | 总预算 |\n|--------|------|------|-----------|------|--------|\n"

    for d in valid_dests:
        dest = DESTINATIONS[d]
        budget = dest["budget"].get(style, dest["budget"]["经济"])
        daily = sum(budget.values())
        flight = FLIGHT_ESTIMATE.get(dest["country"], {}).get(style, 0) * 2
        visa = VISA_COST.get(dest["country"], 0)
        insurance = 30 * days if dest["country"] != "中国" else 5 * days
        total = daily * days + flight + visa + insurance
        output += f"| {d} | {dest['country']} | ¥{daily} | ¥{flight:,} | ¥{visa} | **¥{total:,}** |\n"

    output += "\n"

    # 排序推荐
    sorted_dests = []
    for d in valid_dests:
        dest = DESTINATIONS[d]
        budget = dest["budget"].get(style, dest["budget"]["经济"])
        daily = sum(budget.values())
        flight = FLIGHT_ESTIMATE.get(dest["country"], {}).get(style, 0) * 2
        visa = VISA_COST.get(dest["country"], 0)
        insurance = 30 * days if dest["country"] != "中国" else 5 * days
        total = daily * days + flight + visa + insurance
        sorted_dests.append((d, total))

    sorted_dests.sort(key=lambda x: x[1])
    output += f"🏆 **性价比排名**：{' > '.join([f'{d}(¥{t:,})' for d, t in sorted_dests])}\n"

    return output


# ========== 主入口 ==========
def main():
    if len(sys.argv) < 2:
        print(json.dumps({
            "status": "error",
            "message": "用法: travel_budget_planner.py <command> [args]\n命令: plan <目的地> [天数] [风格] [人数] | compare <目的地1,目的地2,...> [天数] [风格]"
        }, ensure_ascii=False))
        return

    command = sys.argv[1]

    if command == "plan":
        if len(sys.argv) < 3:
            print(json.dumps({"status": "error", "message": "请提供目的地"}, ensure_ascii=False))
            return
        dest = sys.argv[2]
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        style = sys.argv[4] if len(sys.argv) > 4 else "经济"
        people = int(sys.argv[5]) if len(sys.argv) > 5 else 1
        print(cmd_plan(dest, days, style, people))

    elif command == "compare":
        if len(sys.argv) < 3:
            print(json.dumps({"status": "error", "message": "请提供目的地列表，逗号分隔"}, ensure_ascii=False))
            return
        dests = sys.argv[2]
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        style = sys.argv[4] if len(sys.argv) > 4 else "经济"
        print(cmd_compare(dests, days, style))

    else:
        print(json.dumps({
            "status": "error",
            "message": f"未知命令: {command}\n支持: plan | compare"
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
