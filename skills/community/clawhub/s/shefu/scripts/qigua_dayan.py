#!/usr/bin/env python3
"""大衍筮法起卦模块
模拟蓍草占筮：49根蓍草，四营三变成一爻，十八变成一卦。
输出本卦、变卦、动爻信息。
"""

import json
import random
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
import lifa

DB_PATH = os.path.join(BASE_DIR, "..", "data", "guaci_db.json")

BAGUA_PIC = {"乾": "☰", "兑": "☱", "离": "☲", "震": "☳", "巽": "☴", "坎": "☵", "艮": "☶", "坤": "☷"}
BAGUA_WUXING = {"乾": "金", "兑": "金", "离": "火", "震": "木", "巽": "木", "坎": "水", "艮": "土", "坤": "土"}


def load_gua_db():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def find_gua_by_yao(yao, db):
    """根据六爻数组查找卦名，yao[0]=初爻, yao[5]=上爻"""
    for name, info in db.items():
        if info.get("yao") == yao:
            return name
    return None


def dayan_one_line(random_obj=None):
    """
    大衍筮法成卦：四营三变成一爻。
    返回 (value, yao, moving)
    value: 6(老阴)/7(少阳)/8(少阴)/9(老阳)
    yao: 0(阴)/1(阳)
    moving: True(动爻)/False(静爻)
    """
    if random_obj is None:
        random_obj = random

    stalks = 49  # 大衍之数五十，其用四十有九

    for _ in range(3):  # 三变
        # 分二：随意分为左右两堆
        split = random_obj.randint(1, stalks - 1)
        left = split
        right = stalks - split

        # 挂一：从右边取1根夹在指间
        right -= 1

        # 揲四：左右分别以4根为一组数，取余数
        left_rem = left % 4
        if left_rem == 0:
            left_rem = 4
        right_rem = right % 4
        if right_rem == 0:
            right_rem = 4

        # 归奇：余数 + 挂一
        removed = 1 + left_rem + right_rem
        stalks -= removed

    value = stalks // 4  # 6, 7, 8, 9

    if value == 6:
        return value, 0, True   # 老阴 → 阴爻，动
    elif value == 7:
        return value, 1, False  # 少阳 → 阳爻，静
    elif value == 8:
        return value, 0, False  # 少阴 → 阴爻，静
    elif value == 9:
        return value, 1, True   # 老阳 → 阳爻，动


def dayan_qigua(seed=None):
    """
    完整大衍筮法起卦：十八变 → 六爻 → 本卦 + 变卦。
    返回 dict。
    """
    if seed is not None:
        rng = random.Random(seed)
    else:
        rng = random

    lines = []
    for pos in range(1, 7):  # 初爻(1) → 上爻(6)
        value, yao, moving = dayan_one_line(rng)
        lines.append({
            "pos": pos,
            "value": value,       # 6/7/8/9
            "yao": yao,           # 0阴/1阳
            "moving": moving,     # 动爻?
            "changed_yao": yao if not moving else (1 - yao),
        })

    # 本卦六爻：[初,二,三,四,五,上]
    ben_yao = [l["yao"] for l in lines]
    # 变卦六爻
    bian_yao = [l["changed_yao"] for l in lines]

    # 动爻位置
    dong_yao = [l["pos"] for l in lines if l["moving"]]

    db = load_gua_db()

    ben_gua_name = find_gua_by_yao(ben_yao, db)
    bian_gua_name = find_gua_by_yao(bian_yao, db) if dong_yao else None

    # 卦名
    gua_info = db.get(ben_gua_name, {})
    shang_yao = gua_info.get("shang", "?")
    xia_yao = gua_info.get("xia", "?")
    wuxing = gua_info.get("wuxing", "?")

    # 历法（当前时间）
    li = lifa.now_ganzhi()
    year_gz = li.get("年干支", "")
    month_gz = li.get("月干支", "")
    day_gz = li.get("日干支", "")
    month_zhi = li.get("月建", "")
    day_zhi = li.get("日支", "")

    # 上下卦五行
    shang_wx = BAGUA_WUXING.get(shang_yao, "?")
    xia_wx = BAGUA_WUXING.get(xia_yao, "?")

    result = {
        "method": "大衍筮法",
        "method_desc": "四营十八变·蓍草模拟",
        "lines": lines,
        "ben_gua": {
            "name": ben_gua_name,
            "yao": ben_yao,
            "shang": shang_yao,
            "xia": xia_yao,
            "wuxing": wuxing,
            "shang_pic": BAGUA_PIC.get(shang_yao, "?"),
            "xia_pic": BAGUA_PIC.get(xia_yao, "?"),
        },
        "dong_yao": dong_yao,
        "jia_li": {
            "year": year_gz,
            "month": month_gz,
            "day": day_gz,
            "month_zhi": month_zhi,
            "day_zhi": day_zhi,
        },
    }

    if bian_gua_name:
        bian_info = db.get(bian_gua_name, {})
        result["bian_gua"] = {
            "name": bian_gua_name,
            "yao": bian_yao,
            "shang": bian_info.get("shang", "?"),
            "xia": bian_info.get("xia", "?"),
            "wuxing": bian_info.get("wuxing", "?"),
            "shang_pic": BAGUA_PIC.get(bian_info.get("shang", "?"), "?"),
            "xia_pic": BAGUA_PIC.get(bian_info.get("xia", "?"), "?"),
        }
    else:
        result["bian_gua"] = None

    return result


def format_output(result):
    """格式化输出为可读中文"""
    ben = result["ben_gua"]
    dong = result["dong_yao"]
    jia = result["jia_li"]
    lines = result["lines"]

    # 爻位标签
    pos_names = {1: "初", 2: "二", 3: "三", 4: "四", 5: "五", 6: "上"}

    output = []
    output.append("=" * 50)
    output.append(f"起卦方式：{result['method']}（{result['method_desc']}）")
    output.append(f"历法参照：{jia['year']}年 {jia['month']}月 {jia['day']}日")
    output.append("-" * 50)
    output.append(f"本卦：{ben['name']}  {ben['shang_pic']}{ben['xia_pic']}")
    output.append(f"  上卦 {ben['shang']}({ben['shang_pic']}) / 下卦 {ben['xia']}({ben['xia_pic']})")

    if result["bian_gua"]:
        bian = result["bian_gua"]
        output.append(f"变卦：{bian['name']}  {bian['shang_pic']}{bian['xia_pic']}")
        output.append(f"  上卦 {bian['shang']}({bian['shang_pic']}) / 下卦 {bian['xia']}({bian['xia_pic']})")

    output.append(f"动爻：{'、'.join(f'第{d}爻' for d in dong) if dong else '无（静卦）'}")
    output.append("-" * 50)
    output.append("爻位详情（从初到上）：")
    for l in lines:
        pos = l["pos"]
        v = l["value"]
        symbol = {6: "老阴 - - ×", 7: "少阳 ━━━", 8: "少阴 - -", 9: "老阳 ━━━ ○"}[v]
        status = "→ 动爻" if l["moving"] else "静爻"
        output.append(f"  {pos_names[pos]}爻（第{pos}位）: {symbol}  {status}")

    output.append("=" * 50)
    return "\n".join(output)


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

    import argparse
    parser = argparse.ArgumentParser(description="大衍筮法起卦")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("--seed", type=int, default=None, help="随机种子（调试用）")
    args = parser.parse_args()

    seed = args.seed if args.seed is not None else None
    result = dayan_qigua(seed=seed)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(format_output(result))


if __name__ == "__main__":
    main()
