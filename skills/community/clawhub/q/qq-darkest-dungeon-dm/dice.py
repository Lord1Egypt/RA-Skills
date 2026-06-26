# dice.py
import sys
import re
import random

def roll_dice(expression):
    # 移除空格
    expression = expression.replace(' ', '')
    # 按加号分割多组骰子
    parts = expression.split('+')
    
    total = 0
    details =[]
    
    for part in parts:
        if 'd' in part or 'D' in part:
            part = part.lower()
            try:
                count_str, sides_str = part.split('d')
                count = int(count_str) if count_str else 1
                sides = int(sides_str)
                
                rolls = [random.randint(1, sides) for _ in range(count)]
                part_total = sum(rolls)
                total += part_total
                details.append(f"{part}: {rolls} = {part_total}")
            except Exception:
                return f"❌ 无法解析骰子格式: {part}"
        else:
            try:
                mod = int(part)
                total += mod
                details.append(f"修正值: {mod}")
            except Exception:
                return f"❌ 无法解析修正值: {part}"
                
    return f"🎲 投掷[{expression}] -> 细节: {', '.join(details)} | 最终总值: {total}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python dice.py <公式> (例如: 1d20+5)")
        sys.exit(1)
    
    expr = sys.argv[1]
    print(roll_dice(expr))