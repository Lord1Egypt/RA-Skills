#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消费记录写入脚本
接收 JSON 格式的消费记录，写入当月 expenses/expenses-YYYYMM.json 文件

用法:
    python3 record_expense.py '<JSON字符串>'

示例:
    python3 record_expense.py '{"date":"2026-06-01","time":"11:32:06","amount":25,"merchant":"某餐厅","category":"餐饮","payment_method":"微信支付","notes":"午餐","source":"手动输入"}'
"""

import json
import os
import sys
from datetime import datetime


def get_workspace():
    """获取 skill 根目录（expense-tracker 目录）"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_expense_file_path(workspace, year_month):
    """获取指定月份的消费记录文件路径"""
    expenses_dir = os.path.join(workspace, "expenses")
    return os.path.join(expenses_dir, f"expenses-{year_month}.json")


def ensure_expense_file(filepath):
    """确保消费记录文件存在，不存在则创建"""
    if not os.path.exists(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        initial = {
            "expenses": [],
            "last_updated": datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
            "monthly_summaries": {}
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(initial, f, ensure_ascii=False, indent=2)
    return filepath


def generate_id(date_str, existing_expenses):
    """生成消费记录 ID: YYYY-MM-DD-NNN"""
    # 统计当天已有记录数
    same_day_count = sum(1 for e in existing_expenses if e.get("date") == date_str)
    seq = same_day_count + 1
    return f"{date_str}-{seq:03d}"


def validate_category(workspace, category):
    """验证消费分类是否合法"""
    categories_path = os.path.join(workspace, "categories.json")
    if not os.path.exists(categories_path):
        # 如果分类文件不存在，接受任何分类
        return True

    with open(categories_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    valid_names = [c["name"] for c in data.get("categories", [])]
    if category not in valid_names:
        print(f"[警告] 分类 '{category}' 不在预设分类中，有效分类: {valid_names}", file=sys.stderr)
        return False
    return True


def record_expense(expense_data):
    """
    将消费记录写入当月文件

    expense_data 必须包含:
        - date: 日期 (YYYY-MM-DD)
        - amount: 金额 (数字)
        - merchant: 商家名称
        - category: 消费分类

    可选:
        - time: 时间 (HH:MM:SS)，默认当前时间
        - currency: 货币，默认 CNY
        - payment_method: 支付方式
        - notes: 备注
        - source: 数据来源
    """
    workspace = get_workspace()

    # 提取日期确定文件
    date_str = expense_data.get("date", datetime.now().strftime("%Y-%m-%d"))
    year_month = date_str[:7].replace("-", "")  # "2026-06" -> "202606"

    # 确保文件存在
    filepath = ensure_expense_file(get_expense_file_path(workspace, year_month))

    # 读取现有数据
    with open(filepath, "r", encoding="utf-8") as f:
        monthly_data = json.load(f)

    existing_expenses = monthly_data.get("expenses", [])

    # 验证分类
    category = expense_data.get("category", "其他")
    validate_category(workspace, category)

    # 生成 ID
    record_id = generate_id(date_str, existing_expenses)

    # 补全字段
    now = datetime.now()
    record = {
        "id": record_id,
        "date": date_str,
        "time": expense_data.get("time", now.strftime("%H:%M:%S")),
        "amount": float(expense_data["amount"]),
        "currency": expense_data.get("currency", "CNY"),
        "merchant": expense_data["merchant"],
        "category": category,
        "payment_method": expense_data.get("payment_method", ""),
        "notes": expense_data.get("notes", ""),
        "source": expense_data.get("source", "手动输入")
    }

    # 追加记录
    existing_expenses.append(record)
    monthly_data["expenses"] = existing_expenses
    monthly_data["last_updated"] = now.strftime("%Y/%m/%d %H:%M:%S")

    # 写回文件
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(monthly_data, f, ensure_ascii=False, indent=2)

    # 输出结果
    result = {
        "status": "success",
        "record": record,
        "monthly_total": sum(e["amount"] for e in existing_expenses),
        "monthly_count": len(existing_expenses)
    }
    return result


def main():
    if len(sys.argv) < 2:
        print("用法: python3 record_expense.py '<JSON字符串>'", file=sys.stderr)
        print("示例: python3 record_expense.py '{\"date\":\"2026-06-01\",\"amount\":25,\"merchant\":\"某餐厅\",\"category\":\"餐饮\"}'", file=sys.stderr)
        sys.exit(1)

    try:
        expense_data = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"[错误] JSON 解析失败: {e}", file=sys.stderr)
        sys.exit(1)

    result = record_expense(expense_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
