#!/usr/bin/env python3
"""
Calculator script for accurate mathematical operations.
Supports: basic arithmetic, percentages, powers, roots, trigonometry, logarithms, 
equation solving, inequality solving, and provides detailed calculation steps.
"""

import sys
import json
import requests


def calculate(content: str, lan: str = None):
    """
    调用远程计算 API 进行数学计算
    
    Args:
        content: 要计算的表达式或方程
        lan: 语言参数（可选）
    
    Returns:
        list: 计算结果列表，出错时返回 None
    """
    # 构建 API URL
    if lan:
        url = f"https://xyst.yuanfudao.com/solar-calcbot/api/auto-solve?_productId=631&language={lan}"
    else:
        url = "https://xyst.yuanfudao.com/solar-calcbot/api/auto-solve?_productId=631"
    
    # 构建请求数据
    data = {
        'content': content
    }
    print(f'xy_calculator invoked: {data}')
    
    # 设置请求头
    headers = {
        'content-type': 'application/json;charset=UTF-8'
    }
    
    try:
        # 发送 POST 请求
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        
        # 解析响应并直接返回 answer_list
        result = response.json()
        answer_list = result.get('autoAnswerList', [])
        
        return answer_list
    except Exception as e:
        print(f"❌ 错误: {str(e)}", file=sys.stderr)
        return None


def main():
    if len(sys.argv) < 2:
        print("用法: calc.py '<表达式>' [语言]")
        print("\n注意: 输入必须是 LaTeX 格式")
        print("\n示例:")
        print("  基础计算:")
        print("    calc.py '2 + 3'")
        print("    calc.py '(2 + 3) \\times 4'")
        print("    calc.py '\\sqrt{144}'")
        print("    calc.py '\\sin(\\frac{\\pi}{2})'")
        print("\n  方程求解:")
        print("    calc.py '2x + 5 = 15'")
        print("    calc.py 'x^2 - 5x + 6 = 0'")
        print("\n  二元一次方程组:")
        print("    calc.py '\\begin{cases} x + y = 10 \\\\ x - y = 2 \\end{cases}'")
        print("    calc.py '\\begin{cases} 2x + 3y = 12 \\\\ x - y = 1 \\end{cases}'")
        print("\n  不等式求解:")
        print("    calc.py '2x + 5 > 15'")
        print("    calc.py 'x^2 - 4 \\geq 0'")
        print("\n  指定语言:")
        print("    calc.py '2 + 3' zh")
        print("    calc.py '2 + 3' en")
        sys.exit(1)
    
    # 获取表达式（第一个参数）
    content = sys.argv[1]
    
    # 获取语言参数（第二个参数，可选）
    lan = sys.argv[2] if len(sys.argv) > 2 else None
    
    # 执行计算并直接输出结果
    answer_list = calculate(content, lan)
    
    # 如果计算失败，返回非零退出码
    if answer_list is None:
        sys.exit(1)
    
    # 直接输出 JSON 格式的结果
    print(json.dumps(answer_list, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
