#!/usr/bin/env python3
"""支出统计计算脚本，读取数据做统计分析"""

import json
import argparse
import os
from collections import defaultdict
from datetime import datetime, timedelta, time as dt_time

from module import load_data


def filter_by_date(expenses, args):
    """按日期条件筛选"""
    if args.days:
        cutoff = datetime.combine(datetime.now() - timedelta(days=args.days - 1), dt_time.min).strftime('%Y-%m-%d')
        expenses = [e for e in expenses if e['date'] >= cutoff]
    elif args.from_date or args.to_date:
        if args.from_date:
            expenses = [e for e in expenses if e['date'] >= args.from_date]
        if args.to_date:
            expenses = [e for e in expenses if e['date'] <= args.to_date]
    elif not args.all:
        # 默认取最新月份
        latest = max(e['date'][:7] for e in expenses)
        expenses = [e for e in expenses if e['date'].startswith(latest)]
    return expenses


def filter_by_category(expenses, category):
    if category:
        expenses = [e for e in expenses if e['category'] == category]
    return expenses


def sort_expenses(expenses, sort_key):
    if sort_key == 'date':
        expenses = sorted(expenses, key=lambda x: x['date'])
    elif sort_key == 'date_desc':
        expenses = sorted(expenses, key=lambda x: x['date'], reverse=True)
    elif sort_key == 'amount':
        expenses = sorted(expenses, key=lambda x: x['amount'])
    elif sort_key == 'amount_desc':
        expenses = sorted(expenses, key=lambda x: x['amount'], reverse=True)
    return expenses


def get_date_range(expenses):
    """从记录中提取日期范围（不受排序影响）"""
    dates = sorted(set(e['date'] for e in expenses))
    if len(dates) > 1:
        return f"{dates[0]} ~ {dates[-1]}"
    return dates[0] if dates else ""


def format_summary(expenses, category=None, month=None):
    """简洁汇总模式"""
    if not expenses:
        print("没有匹配的记录")
        return

    total = sum(e['amount'] for e in expenses)
    by_cat = defaultdict(float)
    for e in expenses:
        by_cat[e['category']] += e['amount']

    date_range = get_date_range(expenses)
    label = category or '全部'
    month_label = month or expenses[0]['date'][:7]

    print(f"=== {month_label} {label}支出 ({date_range}) ===")
    print(f"共 {len(expenses)} 笔，合计 ¥{total:.2f}")

    if not category:
        print()
        for cat, amount in sorted(by_cat.items(), key=lambda x: x[1], reverse=True):
            pct = amount / total * 100 if total > 0 else 0
            print(f"  {cat}: ¥{amount:.2f} ({pct:.1f}%)")


def format_detail(expenses, category=None, month=None):
    """详细明细模式"""
    if not expenses:
        print("没有匹配的记录")
        return

    total = sum(e['amount'] for e in expenses)
    date_range = get_date_range(expenses)
    label = category or '全部'
    month_label = month or expenses[0]['date'][:7]

    print(f"=== {month_label} {label}支出 ({date_range}) ===")
    print(f"共 {len(expenses)} 笔，合计 ¥{total:.2f}")
    print()

    by_date = defaultdict(list)
    for e in expenses:
        by_date[e['date']].append(e)

    for date in sorted(by_date.keys()):
        day_total = sum(e['amount'] for e in by_date[date])
        print(f"📅 {date}  小计 ¥{day_total:.2f}")
        for e in by_date[date]:
            print(f"    {e['category']}  {e.get('description', '')}  ¥{e['amount']:.2f}")

    print()
    print(f"💰 合计: ¥{total:.2f}")


def format_json(expenses):
    """JSON输出模式"""
    print(json.dumps(expenses, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description='支出统计计算')
    parser.add_argument('--file', default='data/expenses.json', help='数据文件路径')
    parser.add_argument('--all', action='store_true', help='查询全量数据（不限月份）')
    parser.add_argument('--month', help='指定月份，格式 YYYY-MM')
    parser.add_argument('--from', dest='from_date', help='起始日期 YYYY-MM-DD')
    parser.add_argument('--to', dest='to_date', help='结束日期 YYYY-MM-DD')
    parser.add_argument('--days', type=int, help='最近N天')
    parser.add_argument('--category', help='分类名称（精确匹配）')
    parser.add_argument('--limit', type=int, help='返回记录条数')
    parser.add_argument('--sort', choices=['date', 'date_desc', 'amount', 'amount_desc'], default='date_desc', help='排序方式（默认按日期倒序）')
    parser.add_argument('--format', choices=['summary', 'detail', 'json'], default='summary', help='输出格式')

    args = parser.parse_args()

    expenses = load_data(args.file)
    if not expenses:
        print("暂无数据")
        return

    if args.month and args.days:
        import warnings
        warnings.warn('--month 和 --days 同时指定，将优先使用 --month', stacklevel=1)
    if args.month:
        try:
            datetime.strptime(args.month, '%Y-%m')
        except ValueError:
            print("月份格式应为 YYYY-MM")
            return
        expenses = [e for e in expenses if e['date'].startswith(args.month)]
    elif not args.all:
        expenses = filter_by_date(expenses, args)
    expenses = filter_by_category(expenses, args.category)
    expenses = sort_expenses(expenses, args.sort)

    if args.limit:
        expenses = expenses[:args.limit]

    if args.format == 'summary':
        format_summary(expenses, args.category, args.month)
    elif args.format == 'detail':
        format_detail(expenses, args.category, args.month)
    elif args.format == 'json':
        format_json(expenses)


if __name__ == '__main__':
    main()
