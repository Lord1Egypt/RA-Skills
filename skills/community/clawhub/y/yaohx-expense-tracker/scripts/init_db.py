#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记账数据库初始化脚本
创建 categories.json 分类文件和 expenses/ 消费记录目录
"""

import json
import os
import sys
from datetime import datetime

# 工作区根目录（脚本所在目录的上级）
WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 默认消费分类
DEFAULT_CATEGORIES = {
    "categories": [
        {"name": "餐饮", "icon": "🍜", "description": "三餐、外卖、零食、饮料、咖啡等"},
        {"name": "交通", "icon": "🚗", "description": "打车、公交、地铁、加油、停车、共享单车"},
        {"name": "购物", "icon": "🛒", "description": "日用品、数码产品、服饰、网购等"},
        {"name": "居住", "icon": "🏠", "description": "房租、房贷、水电燃气、物业、维修"},
        {"name": "娱乐", "icon": "🎮", "description": "电影、KTV、游戏、旅游、景点门票"},
        {"name": "医疗", "icon": "💊", "description": "挂号、药品、体检、治疗"},
        {"name": "通讯", "icon": "📱", "description": "话费、流量、宽带"},
        {"name": "服饰", "icon": "👗", "description": "衣服、鞋帽、饰品、箱包"},
        {"name": "教育", "icon": "📚", "description": "培训、书籍、文具、课程"},
        {"name": "其他", "icon": "📦", "description": "未归类的其他消费"}
    ]
}


def init_categories():
    """创建 categories.json 文件"""
    categories_path = os.path.join(WORKSPACE, "categories.json")

    if os.path.exists(categories_path):
        print(f"[跳过] categories.json 已存在: {categories_path}")
        # 读取并验证
        with open(categories_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        print(f"[信息] 当前已有 {len(data.get('categories', []))} 个分类")
        return False

    with open(categories_path, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CATEGORIES, f, ensure_ascii=False, indent=2)
    print(f"[创建] categories.json 已创建: {categories_path}")
    return True


def init_expenses_dir():
    """创建 expenses/ 目录和当前月份的消费记录文件"""
    expenses_dir = os.path.join(WORKSPACE, "expenses")
    if not os.path.exists(expenses_dir):
        os.makedirs(expenses_dir)
        print(f"[创建] expenses/ 目录已创建: {expenses_dir}")
    else:
        print(f"[跳过] expenses/ 目录已存在: {expenses_dir}")

    # 创建当前月份的空消费记录文件
    now = datetime.now()
    month_str = now.strftime("%Y%m")
    expense_file = os.path.join(expenses_dir, f"expenses-{month_str}.json")

    if os.path.exists(expense_file):
        print(f"[跳过] {month_str} 月消费记录文件已存在: {expense_file}")
        return False

    initial_data = {
        "expenses": [],
        "last_updated": now.strftime("%Y/%m/%d %H:%M:%S"),
        "monthly_summaries": {}
    }

    with open(expense_file, "w", encoding="utf-8") as f:
        json.dump(initial_data, f, ensure_ascii=False, indent=2)
    print(f"[创建] {month_str} 月消费记录文件已创建: {expense_file}")
    return True


def main():
    print("=" * 50)
    print("  记账助手 - 数据库初始化")
    print("=" * 50)
    print(f"工作区: {WORKSPACE}")
    print()

    init_categories()
    print()
    init_expenses_dir()
    print()

    print("=" * 50)
    print("  初始化完成！")
    print("=" * 50)


if __name__ == "__main__":
    main()
