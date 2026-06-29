"""
骰子操作函数库
"""
import random
import re

def roll_d20(advantage=None):
    """
    投 d20 骰子
    
    参数:
        advantage: None=普通, 'adv'=优势, 'dis'=劣势
    
    返回:
        dict: {"result": int, "detail": str, "type": str}
    """
    if advantage == 'adv':
        r1 = random.randint(1, 20)
        r2 = random.randint(1, 20)
        result = max(r1, r2)
        detail = f"d20优势: {r1}, {r2} → 取高 {result}"
    elif advantage == 'dis':
        r1 = random.randint(1, 20)
        r2 = random.randint(1, 20)
        result = min(r1, r2)
        detail = f"d20劣势: {r1}, {r2} → 取低 {result}"
    else:
        result = random.randint(1, 20)
        detail = f"d20: {result}"
    
    return {"result": result, "detail": detail, "type": "d20"}


def roll_dice(dice_spec):
    """
    投指定骰子，如 d6、d8、d12
    
    参数:
        dice_spec: str - "d6", "d8", "d12" 等
    
    返回:
        int: 骰子结果
    """
    sides = int(dice_spec.replace('d', ''))
    return random.randint(1, sides)


def rolling(expr):
    """
    通用骰子表达式求值
    
    支持格式:
        - "d20+5"
        - "3d6+2"
        - "2d8+4"
        - "d20" (普通)
        - "d20优势" / "d20劣势"
    
    参数:
        expr: str - 骰子表达式
    
    返回:
        dict: {"result": int, "detail": str, "rolls": list}
    """
    expr = expr.strip()
    
    # 处理优势/劣势
    advantage = None
    if '优势' in expr:
        advantage = 'adv'
        expr = expr.replace('优势', '').strip()
    elif '劣势' in expr:
        advantage = 'dis'
        expr = expr.replace('劣势', '').strip()
    
    if expr == 'd20':
        r = roll_d20(advantage)
        return {"result": r["result"], "detail": r["detail"], "rolls": [r["result"]]}
    
    # 匹配 "XdY+Z" 或 "XdY-Z" 格式
    match = re.match(r'^(\d*)d(\d+)([+-]\d+)?$', expr)
    if match:
        num = int(match.group(1)) if match.group(1) else 1
        sides = int(match.group(2))
        mod = int(match.group(3)) if match.group(3) else 0
        
        rolls = [random.randint(1, sides) for _ in range(num)]
        total = sum(rolls) + mod
        detail = f"{num}d{sides}: {'+'.join(map(str, rolls))} = {sum(rolls)}"
        if mod:
            detail += f" {'+' if mod > 0 else '-'} {abs(mod)} = {total}"
        
        return {"result": total, "detail": detail, "rolls": rolls}
    
    raise ValueError(f"无法解析骰子表达式: {expr}")


def roll_stat():
    """
    投角色属性值（4d6 去最低）
    
    返回:
        int: 属性值（3-18）
    """
    rolls = [random.randint(1, 6) for _ in range(4)]
    rolls.sort()
    return sum(rolls[1:])  # 去掉最低的一个
