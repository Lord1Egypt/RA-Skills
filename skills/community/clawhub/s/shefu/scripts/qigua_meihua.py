#!/usr/bin/env python3
"""梅花易数起卦模块
支持时间起卦和数字起卦，输出本卦/互卦/变卦/动爻/体用
"""

import json
import sys
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
import lifa

DB_PATH = os.path.join(BASE_DIR, "..", "data", "guaci_db.json")

# 先天八卦数（乾1兑2离3震4巽5坎6艮7坤8）
XIANTIAN = {1: "乾", 2: "兑", 3: "离", 4: "震", 5: "巽", 6: "坎", 7: "艮", 8: "坤"}
# 先天八卦三爻：从下爻到上爻，1=阳 0=阴
BAGUA_YAO = {
    "乾": [1, 1, 1],
    "兑": [1, 1, 0],
    "离": [1, 0, 1],
    "震": [1, 0, 0],
    "巽": [0, 1, 1],
    "坎": [0, 1, 0],
    "艮": [0, 0, 1],
    "坤": [0, 0, 0],
}
# 八卦名→先天数
BAGUA_NUM = {v: k for k, v in XIANTIAN.items()}

# 五行生克
WUXING_SHENGKE = {
    "金": {"生": "水", "克": "木", "被生": "土", "被克": "火"},
    "木": {"生": "火", "克": "土", "被生": "水", "被克": "金"},
    "水": {"生": "木", "克": "火", "被生": "金", "被克": "土"},
    "火": {"生": "土", "克": "金", "被生": "木", "被克": "水"},
    "土": {"生": "金", "克": "水", "被生": "火", "被克": "木"},
}

BAGUA_WUXING = {"乾": "金", "兑": "金", "离": "火", "震": "木", "巽": "木", "坎": "水", "艮": "土", "坤": "土"}

BAGUA_PIC = {"乾": "☰", "兑": "☱", "离": "☲", "震": "☳", "巽": "☴", "坎": "☵", "艮": "☶", "坤": "☷"}


def load_gua_db():
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def yao_pic(yang):
    return "━━━" if yang else "━ ━"


def bagua_from_num(n, offset=0):
    """数字 → 八卦"""
    r = n % 8
    return XIANTIAN[r if r != 0 else 8]


def dongyao_from_num(n):
    """数字 → 动爻 1-6"""
    r = n % 6
    return r if r != 0 else 6


def find_gua(guaci_db, shang, xia):
    """根据上下卦查找卦名"""
    for name, info in guaci_db.items():
        if info["shang"] == shang and info["xia"] == xia:
            return name, info
    return None, None


def calc_biangua(gua_info, dongyao):
    """计算变卦：动爻阴阳翻转"""
    yao = gua_info["yao"][:]
    yao[dongyao - 1] = 1 - yao[dongyao - 1]  # 翻转
    shang3 = yao[3:6]  # 四五六爻
    xia3 = yao[0:3]  # 一二三爻
    shang_name = yao_to_gua(shang3)
    xia_name = yao_to_gua(xia3)
    return shang_name, xia_name, yao


def yao_to_gua(three_yao):
    """三爻转八卦名"""
    rev = {tuple(v): k for k, v in BAGUA_YAO.items()}
    return rev.get(tuple(three_yao), "?")


def calc_hugua(ben_gua_name, ben_gua_info):
    """计算互卦：本卦二三四爻为下互，三四五爻为上互"""
    yao = ben_gua_info["yao"]
    xia_hu = yao[1:4]  # 二三四爻
    shang_hu = yao[2:5]  # 三四五爻
    return yao_to_gua(shang_hu), yao_to_gua(xia_hu)


def calc_tiyong(ben_gua_info, dongyao):
    """体用判定"""
    shang = ben_gua_info["shang"]
    xia = ben_gua_info["xia"]
    if dongyao in (4, 5, 6):  # 上卦动（四五六爻）
        ti = xia
        yong = shang
    else:  # 下卦动（一二三爻）
        ti = shang
        yong = xia
    return ti, yong


def tiyong_relation(ti, yong):
    """体用生克关系
    sk[ti] = {"生": 我生, "克": 我克, "被生": 生我, "被克": 克我}
    """
    ti_wx = BAGUA_WUXING[ti]
    yong_wx = BAGUA_WUXING[yong]
    sk = WUXING_SHENGKE[ti_wx]
    if ti_wx == yong_wx:
        return "体用比和", "体用同气，吉"
    elif yong_wx == sk["被生"]:  # 用生体（生我者为用）
        return "用生体", "用生体，事成顺遂"
    elif yong_wx == sk["生"]:    # 体生用（我生者为用）
        return "体生用", "体生用，泄气耗力"
    elif yong_wx == sk["克"]:    # 体克用（我克者为用）
        return "体克用", "体克用，需主动争取"
    elif yong_wx == sk["被克"]:  # 用克体（克我者为用）
        return "用克体", "用克体，事有阻碍"


def qigua_by_time(year=None, month=None, day=None, hour=None):
    """时间起卦（农历或公历均可，以数字运算）"""
    now = datetime.now()
    if year is None:
        year = now.year
    if month is None:
        month = now.month
    if day is None:
        day = now.day
    if hour is None:
        hour = now.hour
    # 年+月+日 → 上卦
    shang_sum = year + month + day
    shang_num = shang_sum % 8
    if shang_num == 0:
        shang_num = 8
    shang_gua = XIANTIAN[shang_num]
    # 年+月+日+时 → 下卦
    xia_sum = year + month + day + hour
    xia_num = xia_sum % 8
    if xia_num == 0:
        xia_num = 8
    xia_gua = XIANTIAN[xia_num]
    # 年+月+日+时 → 动爻
    dongyao = xia_sum % 6
    if dongyao == 0:
        dongyao = 6
    return shang_gua, xia_gua, dongyao


def qigua_by_numbers(*numbers):
    """数字起卦
    两数：数1为上卦，数2为下卦
    三数：数1为上卦，数2为下卦，数3为动爻
    """
    nums = list(numbers)
    shang_gua = bagua_from_num(nums[0])
    xia_gua = bagua_from_num(nums[1])
    dongyao = dongyao_from_num(nums[2]) if len(nums) >= 3 else dongyao_from_num(nums[0] + nums[1])
    return shang_gua, xia_gua, dongyao


def hexagram_view(yao_list, dongyao=None):
    """卦画字符表示"""
    lines = []
    for i in range(5, -1, -1):
        yang = yao_list[i]
        marker = ""
        if dongyao and (i + 1) == dongyao:
            marker = " ← 动" if yang else " ← 动"
        yang_symbol = "━━━" if yang else "━ ━"
        lines.append(f"  爻{i+1}: {yang_symbol}{marker}")
    return "\n".join(lines)


def run_meihua(method="time", **kwargs):
    """主入口"""
    guaci_db = load_gua_db()

    if method == "time":
        shang_gua, xia_gua, dongyao = qigua_by_time(
            kwargs.get("year"), kwargs.get("month"),
            kwargs.get("day"), kwargs.get("hour")
        )
        desc = "时间起卦"
    elif method == "number":
        numbers = kwargs.get("numbers", [])
        shang_gua, xia_gua, dongyao = qigua_by_numbers(*numbers)
        desc = f"数字起卦 ({', '.join(str(n) for n in numbers)})"
    else:
        raise ValueError(f"不支持的方法: {method}")

    # 本卦
    ben_gua_name, ben_gua_info = find_gua(guaci_db, shang_gua, xia_gua)
    if ben_gua_name is None:
        return {"error": f"未找到卦: 上{shang_gua} 下{xia_gua}"}

    # 互卦
    hugua_shang, hugua_xia = calc_hugua(ben_gua_name, ben_gua_info)
    hugua_name, hugua_info = find_gua(guaci_db, hugua_shang, hugua_xia)

    # 变卦
    bgua_shang, bgua_xia, bgua_yao = calc_biangua(ben_gua_info, dongyao)
    biangua_name, biangua_info = find_gua(guaci_db, bgua_shang, bgua_xia)

    # 体用
    ti, yong = calc_tiyong(ben_gua_info, dongyao)
    rel, rel_desc = tiyong_relation(ti, yong)

    result = {
        "method": desc,
        "历法": lifa.now_ganzhi(),
        "本卦": {
            "name": ben_gua_name,
            "shang": ben_gua_info["shang"],
            "xia": ben_gua_info["xia"],
            "wuxing": ben_gua_info["wuxing"],
            "yao": ben_gua_info["yao"],
            "上卦图": BAGUA_PIC[ben_gua_info["shang"]],
            "下卦图": BAGUA_PIC[ben_gua_info["xia"]],
        },
        "互卦": {
            "name": hugua_name or f"上{hugua_shang}下{hugua_xia}",
            "shang": hugua_shang,
            "xia": hugua_xia,
            "上卦图": BAGUA_PIC[hugua_shang],
            "下卦图": BAGUA_PIC[hugua_xia],
        },
        "变卦": {
            "name": biangua_name or f"上{bgua_shang}下{bgua_xia}",
            "shang": bgua_shang,
            "xia": bgua_xia,
            "wuxing": biangua_info["wuxing"] if biangua_info else "?",
            "yao": bgua_yao,
            "上卦图": BAGUA_PIC[bgua_shang],
            "下卦图": BAGUA_PIC[bgua_xia],
        },
        "动爻": dongyao,
        "体用": {
            "体": ti,
            "体五行": BAGUA_WUXING[ti],
            "用": yong,
            "用五行": BAGUA_WUXING[yong],
            "关系": rel,
            "说明": rel_desc,
            "体图": BAGUA_PIC[ti],
            "用图": BAGUA_PIC[yong],
        },
        "卦画": {
            "本卦": hexagram_view(ben_gua_info["yao"], dongyao),
            "互卦": hexagram_view(hugua_info["yao"]) if hugua_info else "N/A",
            "变卦": hexagram_view(bgua_yao),
        },
    }
    return result


def main():
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        print(json.dumps(run_meihua("time"), ensure_ascii=False, indent=2))
        return

    arg = sys.argv[1]
    if arg == "time":
        result = run_meihua("time")
    elif arg == "number":
        nums = [int(x) for x in sys.argv[2:]]
        result = run_meihua("number", numbers=nums)
    else:
        print(f"用法: python qigua_meihua.py [time|number <数1> <数2> [数3]]")
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
