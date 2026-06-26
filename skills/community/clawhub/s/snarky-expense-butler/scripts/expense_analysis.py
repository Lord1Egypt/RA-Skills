#!/usr/bin/env python3
# 毒舌消费分析 — 像损友一样吐槽你的消费习惯

import json
import sys
import os
import datetime
from datetime import timedelta

DATA_FILE = os.environ.get('EXPENSE_DATA_FILE', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'expense_records.json'))

# 分类吐槽词典
CATEGORY_COMMENTS = {
    "餐饮": {
        "emoji": "🍔",
        "roast": "全是你在吃",
        "hint": "食堂不去非吃外卖",
        "save_tip": "能吃食堂的日子别点外卖，一天省15一个月省450"
    },
    "交通": {
        "emoji": "🚇",
        "roast": "腿是借的吗",
        "hint": "地铁能到就别打车",
        "save_tip": "多走两步，省钱又健身，一举两得"
    },
    "购物": {
        "emoji": "🛒",
        "roast": "又买买买了",
        "hint": "冷静一下，加入购物车先放三天",
        "save_tip": "购物车放三天，还想要的再买，能省一半冲动消费"
    },
    "娱乐": {
        "emoji": "🎮",
        "roast": "花钱找乐子的一把好手",
        "hint": "免费的快乐也不少",
        "save_tip": "看看免费展览、公园散步，快乐不用花钱"
    },
    "医疗": {
        "emoji": "💊",
        "roast": "身体是革命的本钱",
        "hint": "提前养生比事后治病便宜",
        "save_tip": "早睡早起少点外卖，就是最好的医保"
    },
    "教育": {
        "emoji": "📚",
        "roast": "投资自己没毛病",
        "hint": "别买了课不看",
        "save_tip": "先把手头的课学完再买新的"
    },
    "其他": {
        "emoji": "❓",
        "roast": "分类都懒得选",
        "hint": "记清楚点，不然月底一脸懵",
        "save_tip": "认真分类，搞清楚钱花哪了"
    }
}


def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ 消费记录文件不存在")
        sys.exit(1)
    except json.JSONDecodeError:
        print("❌ 消费记录文件格式错误")
        sys.exit(1)


def get_daily_budget(data):
    """获取日预算"""
    budget = data.get('settings', {}).get('budget', {})
    return budget.get('daily', 50)


def calc_category_totals(items):
    """计算分类汇总（正数退款减少，负数消费增加）"""
    category_totals = {}
    for item in items:
        cat = item['category']
        category_totals[cat] = round(category_totals.get(cat, 0) + (-item['amount']), 2)
    return category_totals


def analyze_roast(items, category_totals, total):
    """生成毒舌吐槽"""
    roasts = []

    if not category_totals:
        return roasts

    # 按金额排序分类
    sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
    top_cat, top_amount = sorted_cats[0]
    top_pct = round(top_amount / total * 100, 1) if total > 0 else 0

    # 大头消费吐槽
    if top_pct > 70:
        info = CATEGORY_COMMENTS.get(top_cat, CATEGORY_COMMENTS["其他"])
        # 找出该分类的明细来吐槽
        cat_items = [i for i in items if i['category'] == top_cat]
        detail_notes = [f"{i['note']} ¥{round(abs(i['amount']), 2)}" for i in cat_items if i.get('note')]
        if detail_notes:
            roasts.append(f"  → {' | '.join(detail_notes)}")
            roasts.append(f"  {info['hint']}，{info['roast']}")

    # 重复消费检测
    cat_count = {}
    for item in items:
        cat = item['category']
        cat_count[cat] = cat_count.get(cat, 0) + 1

    repeat_cats = [c for c, cnt in cat_count.items() if cnt >= 3]
    if repeat_cats:
        for rc in repeat_cats:
            cat_items = [i for i in items if i['category'] == rc]
            amounts = [abs(i['amount']) for i in cat_items]
            avg = round(sum(amounts) / len(amounts), 2)
            max_item = max(cat_items, key=lambda x: abs(x['amount']))
            min_item = min(cat_items, key=lambda x: abs(x['amount']))
            if abs(max_item['amount']) > abs(min_item['amount']) * 2:
                roasts.append(f"  💡 {rc}花了{len(cat_items)}次，从¥{round(abs(min_item['amount']), 2)}到¥{round(abs(max_item['amount']), 2)}，价格差两倍，你是真的不在乎性价比")

    # 退款检测（正数为退款）
    refunds = [i for i in items if i['amount'] > 0]
    if refunds:
        refund_total = sum(i['amount'] for i in refunds)
        roasts.append(f"  ↩️ 退款 ¥{round(abs(refund_total), 1)}，买了又退，你是在锻炼网购肌肉吗")

    return roasts


def generate_suggestions(category_totals, total, daily_budget):
    """生成优化建议"""
    suggestions = []

    if "餐饮" in category_totals:
        food_pct = round(category_totals["餐饮"] / total * 100, 1) if total > 0 else 0
        if food_pct > 60:
            suggestions.append("1. 吃占了大头，自己做饭或吃食堂，一周省100+")
        if category_totals["餐饮"] > daily_budget * 0.5:
            suggestions.append("2. 下午茶这玩意，戒一周省100+")

    if "购物" in category_totals and category_totals["购物"] > 30:
        suggestions.append("3. 购物车放三天，还想要的再买，能省一半冲动消费")

    if "交通" in category_totals:
        if category_totals["交通"] > 20:
            suggestions.append("4. 每天通勤¥8，办个月卡能省不少")

    if not suggestions:
        if total < daily_budget * 0.5:
            suggestions.append("1. 今天花得不多，继续保持！")
        else:
            suggestions.append("1. 看看有没有能优化的地方，积少成多")

    return suggestions


def analyze_date(date_str):
    """分析指定日期的消费"""
    data = load_data()
    daily_budget = get_daily_budget(data)

    # 找到当天记录
    today_record = None
    for record in data['records']:
        if record['date'] == date_str:
            today_record = record
            break

    if not today_record:
        print(f"📊 今日消费分析 ({date_str})")
        print("━━━━━━━━━━━━━━━━━━")
        print(f"今天还没有消费记录，省钱第一天！🎉")
        print(f"日预算: ¥{daily_budget}")
        return

    items = today_record['items']
    # 重新计算总额（正数退款减少，负数消费增加）
    total = round(sum(-item['amount'] for item in items), 2)

    # 分类汇总（退款减少，消费增加）
    category_totals = calc_category_totals(items)

    # 超支情况
    over = round(total - daily_budget, 2)
    if over > 0:
        status = f"超支: ¥{round(over, 1)} 🚨"
    elif over > -daily_budget * 0.2:
        status = f"还剩: ¥{round(abs(over), 1)} ⚠️"
    else:
        status = f"还剩: ¥{round(abs(over), 1)} ✅"

    # 输出
    print(f"📊 今日消费分析 ({date_str})")
    print("━━━━━━━━━━━━━━━━━━")
    print(f"今日花费: ¥{round(total, 1)} | 日预算: ¥{round(daily_budget, 1)} | {status}")
    print()

    # 最大开销
    if category_totals:
        sorted_cats = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        top_cat, top_amount = sorted_cats[0]
        top_pct = round(top_amount / total * 100, 0) if total > 0 else 0
        info = CATEGORY_COMMENTS.get(top_cat, CATEGORY_COMMENTS["其他"])

        print(f"💸 最大开销: {top_cat} ¥{abs(round(top_amount, 1))}（占{int(top_pct)}%）")

        # 分类明细
        print(f"{'🍔' if '餐饮' in category_totals else '📋'} 分类明细:")
        for cat, amount in sorted_cats:
            pct = round(amount / total * 100, 0) if total > 0 else 0
            cat_info = CATEGORY_COMMENTS.get(cat, CATEGORY_COMMENTS["其他"])
            print(f"  {cat_info['emoji']} {cat}: ¥{abs(round(amount, 1))} ({int(pct)}%) ← {cat_info['roast']}")
    else:
        print("📋 无有效消费分类（可能全部为退款）")

    print()

    # 毒舌吐槽
    roasts = analyze_roast(items, category_totals, total)
    for r in roasts:
        print(r)
    if roasts:
        print()

    # 优化建议
    print("💡 优化建议:")
    suggestions = generate_suggestions(category_totals, total, daily_budget)
    for s in suggestions:
        print(f"  {s}")
    print()

    # 今日判定
    if over > 0:
        print(f"📈 今日判定: 🔴 超支，明天长点心吧")
    elif over > -daily_budget * 0.1:
        print(f"📈 今日判定: 🟡 勉强及格，继续保持")
    else:
        print(f"📈 今日判定: 🟢 省钱小能手，值得表扬！")


def main():
    if len(sys.argv) < 2:
        print("📊 毒舌消费分析工具")
        print("用法: python3 expense_analysis.py <日期|today>")
        print()
        print("示例:")
        print("  python3 expense_analysis.py today")
        print("  python3 expense_analysis.py 2026-03-18")
        return

    arg = sys.argv[1]
    if arg == "today":
        date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        date_str = arg

    analyze_date(date_str)


if __name__ == "__main__":
    main()
