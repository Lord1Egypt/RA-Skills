#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
采购记录技能 - 主入口脚本
解析自然语言命令并调用记录功能
"""

import sys
import re


def parse_command(text):
    """
    解析命令：采购 [日期] [物品名称] [价格]
    
    示例输入："采购 0312 螺丝 3 元"
    返回：(date, name, price) -> ("0312", "螺丝", "3")
    """

    # 移除前缀 "采购"
    if not text.startswith("采购"):
        return None

    # 提取命令参数部分
    params = text[2:].strip()

    # 正则表达式匹配：日期 (4 位数字) + 名称 (任意内容) + 价格 (数字或数字 + 单位)
    pattern = r'^(\d{4})\s+(.+?)\s+(\d+\.?\d*)(?:元)?'
    match = re.match(pattern, params)

    if not match:
        return None

    date_str = match.group(1)
    name = match.group(2).strip()
    price_str = match.group(3)

    # 验证价格是否只包含数字（可能带小数点）
    if not re.match(r'^\d+\.?\d*$', price_str):
        return None

    return (date_str, name, price_str)


def main():
    """主入口"""
    if len(sys.argv) < 2:
        print("用法：python main.py \"采购 0312 螺丝 3 元\"")
        sys.exit(1)

    command = " ".join(sys.argv[1:])
    result = parse_command(command)

    if result is None:
        print("命令格式错误！")
        print("正确格式：采购 [日期] [物品名称] [价格]")
        print("示例：采购 0312 螺丝 3")
        sys.exit(1)

    date_str, name, price = result

    # 直接导入并调用 record.py 中的函数（避免 subprocess 的编码问题）
    from record import record_purchase

    try:
        record_purchase(date_str, name, price)
    except Exception as e:
        print("录入失败：" + str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
