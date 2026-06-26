#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
财务计算器 - 用于计算章节财务，确保返还倍率和余额准确
"""

import sys
import re


class FinanceCalculator:
    """财务计算器"""

    def __init__(self, initial_balance=0):
        self.initial_balance = initial_balance
        self.expenses = []  # 支出记录
        self.incomes = []   # 收入记录

    def add_expense(self, description, amount):
        """添加支出"""
        self.expenses.append({
            'description': description,
            'amount': amount
        })

    def add_income(self, description, amount, multiplier=1):
        """添加收入"""
        self.incomes.append({
            'description': description,
            'amount': amount,
            'multiplier': multiplier
        })

    def calculate(self):
        """计算财务"""
        total_expense = sum(e['amount'] for e in self.expenses)
        total_income = sum(i['amount'] for i in self.incomes)
        final_balance = self.initial_balance - total_expense + total_income

        return {
            'initial_balance': self.initial_balance,
            'total_expense': total_expense,
            'total_income': total_income,
            'final_balance': final_balance,
            'expenses': self.expenses,
            'incomes': self.incomes
        }

    def print_report(self):
        """打印财务报告"""
        result = self.calculate()

        print("=" * 60)
        print("财务计算报告")
        print("=" * 60)
        print(f"初始余额：{result['initial_balance']:,.2f} 元")
        print()

        # 支出明细
        print("支出记录：")
        for i, expense in enumerate(result['expenses'], 1):
            print(f"  {i}. {expense['description']}：{expense['amount']:,.2f} 元")
        print(f"支出合计：{result['total_expense']:,.2f} 元")
        print()

        # 收入明细
        print("收入记录：")
        for i, income in enumerate(result['incomes'], 1):
            multiplier_text = f"（{income['multiplier']}倍）" if income['multiplier'] > 1 else ""
            print(f"  {i}. {income['description']}{multiplier_text}：{income['amount']:,.2f} 元")
        print(f"收入合计：{result['total_income']:,.2f} 元")
        print()

        # 最终余额
        print("=" * 60)
        print(f"当前余额：{result['initial_balance']:,.2f} - {result['total_expense']:,.2f} + {result['total_income']:,.2f} = {result['final_balance']:,.2f} 元")
        print("=" * 60)


def parse_chapter_finance(file_path):
    """从章节文件中解析财务数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 提取初始余额
        initial_match = re.search(r'初始余额[：:]\s*([-\d,]+.?\d*)\s*元', content)
        initial_balance = float(initial_match.group(1).replace(',', '')) if initial_match else 0

        # 提取支出
        expenses = []
        expense_pattern = r'[-–—][：:]\s*(.+?)[：:]\s*([-\d,]+.?\d*)\s*元'
        for match in re.finditer(expense_pattern, content):
            description = match.group(1).strip()
            amount = float(match.group(2).replace(',', ''))
            if '合计' not in description and '支出' not in description:
                expenses.append((description, amount))

        # 提取收入
        incomes = []
        income_pattern = r'返还(\d+\.?\d*)元[（(](\d+)倍[）)]'
        for match in re.finditer(income_pattern, content):
            amount = float(match.group(1))
            multiplier = int(match.group(2))
            incomes.append((f"返还{amount}元", amount * multiplier, multiplier))

        return {
            'success': True,
            'initial_balance': initial_balance,
            'expenses': expenses,
            'incomes': incomes
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


def main():
    if len(sys.argv) < 2:
        print("用法: python finance_calculator.py <章节文件路径>")
        print("示例: python finance_calculator.py chapter-4_xxx.txt")
        print()
        print("或者使用交互模式:")
        print("  python finance_calculator.py --interactive")
        return

    if sys.argv[1] == '--interactive':
        # 交互模式
        print("=" * 60)
        print("财务计算器（交互模式）")
        print("=" * 60)

        initial_balance = float(input("请输入初始余额："))
        calc = FinanceCalculator(initial_balance)

        print("\n【添加支出】（输入空行结束）:")
        while True:
            description = input("支出描述：")
            if not description:
                break
            amount = float(input("金额（元）："))
            calc.add_expense(description, amount)

        print("\n【添加收入】（输入空行结束）:")
        while True:
            description = input("收入描述：")
            if not description:
                break
            amount = float(input("金额（元）："))
            multiplier = int(input("返还倍率（=无返还）: ") or "1")
            calc.add_income(description, amount, multiplier)

        calc.print_report()
        return

    # 从文件解析
    file_path = sys.argv[1]
    result = parse_chapter_finance(file_path)

    if not result.get('success'):
        print(f"解析失败: {result.get('error')}")
        return

    initial_balance = result['initial_balance']
    expenses = result['expenses']
    incomes = result['incomes']

    calc = FinanceCalculator(initial_balance)

    for description, amount in expenses:
        calc.add_expense(description, amount)

    for description, amount, multiplier in incomes:
        calc.add_income(description, amount, multiplier)

    calc.print_report()


if __name__ == '__main__':
    main()
