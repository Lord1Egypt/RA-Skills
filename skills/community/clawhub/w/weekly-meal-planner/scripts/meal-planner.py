#!/usr/bin/env python3
"""Meal Planner - Weekly menu generator"""

import argparse
import json
from datetime import datetime

# Simple meal database
MEALS = {
    "light": {
        "breakfast": ["白粥+咸菜", "豆浆+油条", "牛奶+面包", "鸡蛋+玉米", "小米粥+包子", "燕麦+水果", "馄饨"],
        "lunch": ["清蒸鱼+米饭", "白切鸡+蔬菜", "番茄炒蛋+米饭", "冬瓜汤+馒头", "蒸蛋+青菜", "豆腐汤+米饭", "凉拌黄瓜+粥"],
        "dinner": ["蔬菜沙拉", "蒸南瓜+小米粥", "清炒时蔬+米饭", "紫菜蛋花汤+馒头", "凉拌豆腐+粥", "蒸茄子+米饭", "白灼虾+蔬菜"]
    },
    "spicy": {
        "breakfast": ["辣肉面", "麻辣馄饨", "辣椒炒蛋+馒头", "酸辣粉", "香辣包子", "麻辣豆腐脑", "红油抄手"],
        "lunch": ["麻婆豆腐+米饭", "辣子鸡+米饭", "水煮鱼", "回锅肉+米饭", "麻辣香锅", "香辣虾+米饭", "剁椒鱼头+米饭"],
        "dinner": ["麻辣小龙虾", "香辣蟹", "口水鸡", "毛血旺", "干锅土豆", "香辣排骨", "麻辣火锅"]
    },
    "sweet": {
        "breakfast": ["红豆粥", "甜豆浆+油条", "牛奶+甜甜圈", "芝麻糊", "南瓜粥", "红枣银耳羹", "豆沙包"],
        "lunch": ["糖醋排骨+米饭", "可乐鸡翅+米饭", "蜜汁叉烧+米饭", "甜酸鱼+米饭", "红烧茄子+米饭", "糖醋里脊+米饭", "蜜汁鸡腿+米饭"],
        "dinner": ["银耳莲子汤", "红豆沙", "南瓜饼", "糖醋小排", "蜜汁烤翅", "甜玉米", "红枣粥"]
    },
    "balanced": {
        "breakfast": ["鸡蛋+牛奶+面包", "豆浆+包子+水果", "燕麦+酸奶+坚果", "粥+鸡蛋+蔬菜", "牛奶+麦片+水果", "豆腐脑+油条+豆浆", "鸡蛋饼+牛奶"],
        "lunch": ["荤素搭配套餐", "鸡肉+蔬菜+米饭", "鱼肉+豆腐+米饭", "牛肉+蔬菜+馒头", "猪肉+鸡蛋+米饭", "虾仁+蔬菜+米饭", "排骨+玉米+米饭"],
        "dinner": ["蔬菜+蛋白质+主食", "鱼+蔬菜+粥", "鸡+沙拉+面包", "豆腐+蔬菜+米饭", "蛋+蔬菜+馒头", "虾+蔬菜+粥", "肉+蔬菜+米饭"]
    }
}

# Estimated prices (yuan)
PRICES = {
    "白粥+咸菜": 3, "豆浆+油条": 5, "牛奶+面包": 8, "鸡蛋+玉米": 6, "小米粥+包子": 5, "燕麦+水果": 10, "馄饨": 8,
    "清蒸鱼+米饭": 25, "白切鸡+蔬菜": 20, "番茄炒蛋+米饭": 12, "冬瓜汤+馒头": 8, "蒸蛋+青菜": 10, "豆腐汤+米饭": 12, "凉拌黄瓜+粥": 6,
    "蔬菜沙拉": 15, "蒸南瓜+小米粥": 8, "清炒时蔬+米饭": 10, "紫菜蛋花汤+馒头": 6, "凉拌豆腐+粥": 5, "蒸茄子+米饭": 8, "白灼虾+蔬菜": 30,
    "辣肉面": 12, "麻辣馄饨": 10, "辣椒炒蛋+馒头": 8, "酸辣粉": 8, "香辣包子": 5, "麻辣豆腐脑": 6, "红油抄手": 10,
    "麻婆豆腐+米饭": 12, "辣子鸡+米饭": 20, "水煮鱼": 35, "回锅肉+米饭": 18, "麻辣香锅": 25, "香辣虾+米饭": 30, "剁椒鱼头+米饭": 28,
    "麻辣小龙虾": 50, "香辣蟹": 60, "口水鸡": 25, "毛血旺": 30, "干锅土豆": 15, "香辣排骨": 35, "麻辣火锅": 40,
    "红豆粥": 5, "甜豆浆+油条": 5, "牛奶+甜甜圈": 10, "芝麻糊": 6, "南瓜粥": 5, "红枣银耳羹": 8, "豆沙包": 4,
    "糖醋排骨+米饭": 25, "可乐鸡翅+米饭": 20, "蜜汁叉烧+米饭": 22, "甜酸鱼+米饭": 20, "红烧茄子+米饭": 12, "糖醋里脊+米饭": 18, "蜜汁鸡腿+米饭": 15,
    "银耳莲子汤": 8, "红豆沙": 6, "南瓜饼": 8, "糖醋小排": 20, "蜜汁烤翅": 18, "甜玉米": 4, "红枣粥": 5,
    "鸡蛋+牛奶+面包": 10, "豆浆+包子+水果": 8, "燕麦+酸奶+坚果": 12, "粥+鸡蛋+蔬菜": 8, "牛奶+麦片+水果": 10, "豆腐脑+油条+豆浆": 8, "鸡蛋饼+牛奶": 8,
    "荤素搭配套餐": 20, "鸡肉+蔬菜+米饭": 18, "鱼肉+豆腐+米饭": 22, "牛肉+蔬菜+馒头": 25, "猪肉+鸡蛋+米饭": 15, "虾仁+蔬菜+米饭": 28, "排骨+玉米+米饭": 25,
    "蔬菜+蛋白质+主食": 18, "鱼+蔬菜+粥": 20, "鸡+沙拉+面包": 18, "豆腐+蔬菜+米饭": 12, "蛋+蔬菜+馒头": 10, "虾+蔬菜+粥": 22, "肉+蔬菜+米饭": 18
}

def generate_menu(people, budget, taste):
    """Generate 7-day menu"""
    import random
    random.seed(42)  # For reproducible results
    
    meals = MEALS.get(taste, MEALS["balanced"])
    menu = []
    total_cost = 0
    
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    
    for i, day in enumerate(days):
        breakfast = meals["breakfast"][i % len(meals["breakfast"])]
        lunch = meals["lunch"][i % len(meals["lunch"])]
        dinner = meals["dinner"][i % len(meals["dinner"])]
        
        day_cost = (PRICES.get(breakfast, 10) + PRICES.get(lunch, 20) + PRICES.get(dinner, 20)) * people
        
        menu.append({
            "day": day,
            "breakfast": breakfast,
            "lunch": lunch,
            "dinner": dinner,
            "daily_cost": day_cost
        })
        total_cost += day_cost
    
    return menu, total_cost

def generate_shopping_list(menu):
    """Generate shopping list from menu"""
    items = {}
    for day in menu:
        for meal in [day["breakfast"], day["lunch"], day["dinner"]]:
            price = PRICES.get(meal, 15)
            if meal not in items:
                items[meal] = {"count": 1, "price": price}
            else:
                items[meal]["count"] += 1
    
    return items

def main():
    parser = argparse.ArgumentParser(description="Meal Planner")
    parser.add_argument("--people", type=int, required=True, help="Number of people")
    parser.add_argument("--budget", type=int, required=True, help="Daily budget per person")
    parser.add_argument("--taste", choices=["light", "spicy", "sweet", "balanced"], required=True)
    
    args = parser.parse_args()
    
    print("=" * 60)
    print(f"🍽️  一周菜单规划 ({args.taste}口味)")
    print("=" * 60)
    print(f"人数: {args.people}人 | 人均预算: {args.budget}元/天")
    print()
    
    menu, total_cost = generate_menu(args.people, args.budget, args.taste)
    
    # Print menu
    for day in menu:
        print(f"📅 {day['day']}")
        print(f"   🌅 早餐: {day['breakfast']}")
        print(f"   🌞 午餐: {day['lunch']}")
        print(f"   🌙 晚餐: {day['dinner']}")
        print(f"   💰 当日: {day['daily_cost']}元")
        print()
    
    # Shopping list
    shopping = generate_shopping_list(menu)
    print("=" * 60)
    print("🛒 买菜清单")
    print("=" * 60)
    
    list_total = 0
    for item, info in sorted(shopping.items()):
        subtotal = info["price"] * info["count"] * args.people
        list_total += subtotal
        print(f"   {item} x{info['count']} = {subtotal}元")
    
    print("-" * 60)
    print(f"💰 总预算: {args.budget * args.people * 7}元")
    print(f"💵 预计花费: {total_cost}元")
    print(f"📊 人均/天: {total_cost // 7 // args.people}元")
    
    if total_cost <= args.budget * args.people * 7:
        print(f"✅ 预算内")
    else:
        print(f"⚠️  超预算 {total_cost - args.budget * args.people * 7}元")
    
    # Save to file
    result = {
        "generated_at": datetime.now().isoformat(),
        "people": args.people,
        "budget_per_person": args.budget,
        "taste": args.taste,
        "menu": menu,
        "shopping_list": shopping,
        "total_cost": total_cost
    }
    
    with open("menu_plan.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 菜单已保存: menu_plan.json")

if __name__ == "__main__":
    main()
