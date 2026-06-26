#!/usr/bin/env python3
"""六爻纳甲起卦模块
铜钱摇卦 → 装卦 → 纳甲 → 六亲 → 世应 → 六神
"""

import json
import sys
import os
import random
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
import lifa

GUACI_PATH = os.path.join(BASE_DIR, "..", "data", "guaci_db.json")
NAJIA_PATH = os.path.join(BASE_DIR, "..", "data", "najia_table.json")

# 八卦三爻：[下,中,上] 1=阳 0=阴
BAGUA_YAO = {
    "乾": [1, 1, 1], "兑": [1, 1, 0], "离": [1, 0, 1], "震": [1, 0, 0],
    "巽": [0, 1, 1], "坎": [0, 1, 0], "艮": [0, 0, 1], "坤": [0, 0, 0],
}
BAGUA_PIC = {"乾": "☰", "兑": "☱", "离": "☲", "震": "☳", "巽": "☴", "坎": "☵", "艮": "☶", "坤": "☷"}

# 六神固定顺序（复用 lifa 中的天干列表）
LIUSHEN_ORDER = ["青龙", "朱雀", "勾陈", "腾蛇", "白虎", "玄武"]
LIUSHEN_START = {
    "甲": 0, "乙": 0, "丙": 1, "丁": 1, "戊": 2, "己": 3,
    "庚": 4, "辛": 4, "壬": 5, "癸": 5,
}

# 五行生克（用于六亲计算）
WX_SHENG = {"水": "木", "木": "火", "火": "土", "土": "金", "金": "水"}
WX_KE = {"水": "火", "火": "金", "金": "木", "木": "土", "土": "水"}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def yao_to_gua(three_yao):
    rev = {tuple(v): k for k, v in BAGUA_YAO.items()}
    return rev.get(tuple(three_yao), "?")


def find_gua_by_yao(guaci_db, yao_list):
    """六爻→卦名"""
    for name, info in guaci_db.items():
        if info["yao"] == yao_list:
            return name, info
    return None, None


def toss_coins():
    """模拟三枚铜钱摇卦
    规则：一个背(单背)=少阳, 两个背(双背)=少阴, 三个背(三背)=老阳(动), 三个字(三字)=老阴(动)
    返回: {'value': '老阴'/'少阴'/'少阳'/'老阳', 'yao': 0/1, 'changing': bool, 'coins': [正/反, ...]}
    """
    coins = [random.choice(["正", "反"]) for _ in range(3)]
    backs = sum(1 for c in coins if c == "反")
    if backs == 0:  # 三字（三正）→ 老阴（阴气极盛，物极必反）
        return {"value": "老阴", "yao": 0, "changing": True, "coins": coins, "bei": 0}
    elif backs == 1:  # 单背 → 少阳（一阳为贵）
        return {"value": "少阳", "yao": 1, "changing": False, "coins": coins, "bei": 1}
    elif backs == 2:  # 双背 → 少阴（一阴为贵）
        return {"value": "少阴", "yao": 0, "changing": False, "coins": coins, "bei": 2}
    else:  # backs == 3, 三背 → 老阳（阳气极盛，物极必反）
        return {"value": "老阳", "yao": 1, "changing": True, "coins": coins, "bei": 3}


def toss_hexagram():
    """摇六次得卦"""
    lines = []
    for i in range(1, 7):
        result = toss_coins()
        result["position"] = i
        lines.append(result)
    return lines


def get_najia_for_gua(najia_db, gua_info):
    """为非纯卦装纳甲
    下卦取纯卦的内卦纳甲，上卦取纯卦的外卦纳甲
    """
    xia_gua = gua_info["xia"]
    shang_gua = gua_info["shang"]
    inner = najia_db["八纯卦纳甲"][xia_gua]["内卦"]
    outer = najia_db["八纯卦纳甲"][shang_gua]["外卦"]
    return inner + outer


def calc_liuqin(gua_wuxing, yao_dizhi_wx):
    """六亲判定"""
    if gua_wuxing == yao_dizhi_wx:
        return "兄弟"
    if WX_SHENG.get(gua_wuxing) == yao_dizhi_wx:
        return "子孙"
    if WX_KE.get(gua_wuxing) == yao_dizhi_wx:
        return "妻财"
    if WX_SHENG.get(yao_dizhi_wx) == gua_wuxing:
        return "父母"
    if WX_KE.get(yao_dizhi_wx) == gua_wuxing:
        return "官鬼"
    return "?"


def get_liushen(day_gan):
    """根据日干获取六神排列(从初爻到上爻)"""
    start_idx = LIUSHEN_START.get(day_gan, 0)
    result = []
    for i in range(6):
        result.append(LIUSHEN_ORDER[(start_idx + i) % 6])
    return result


def yao_to_diagram(yao_val, changing=False):
    """爻的图符"""
    sym = "━━━" if yao_val == 1 else "━ ━"
    return sym + (" ○" if (changing and yao_val == 1) else " ×" if (changing and yao_val == 0) else "")


def get_calendar_info():
    """从 lifa 模块获取完整干支历法信息"""
    return lifa.now_ganzhi()


def run_liuyao(lines=None, day_gan=None):
    """主入口：六爻纳甲起卦
    lines: 6个 toss_coins() 的结果列表，默认自动摇卦
    """
    guaci_db = load_json(GUACI_PATH)
    najia_db = load_json(NAJIA_PATH)

    if lines is None:
        lines = toss_hexagram()

    cal = get_calendar_info()
    if day_gan is None:
        day_gan = cal["日干"]
    day_zhi = cal["日支"]
    day_ganzhi = cal["日干支"]
    month_zhi = cal["月建"]
    month_ganzhi = cal["月干支"]
    year_ganzhi = cal["年干支"]

    # 构建本卦和变卦
    ben_yao = [line["yao"] for line in lines]  # [初,二,三,四,五,上]
    bian_yao = []
    changing_positions = []
    for line in lines:
        if line["changing"]:
            changing_positions.append(line["position"])
            bian_yao.append(1 - line["yao"])
        else:
            bian_yao.append(line["yao"])

    ben_gua_name, ben_gua_info = find_gua_by_yao(guaci_db, ben_yao)
    bian_gua_name, bian_gua_info = find_gua_by_yao(guaci_db, bian_yao)

    if ben_gua_name is None:
        return {"error": f"未匹配到本卦: {ben_yao}"}
    if bian_gua_name is None:
        return {"error": f"未匹配到变卦: {bian_yao}"}

    # 纳甲装爻
    najia_lines = get_najia_for_gua(najia_db, ben_gua_info)

    # 六神
    liushen = get_liushen(day_gan)

    # 世应
    shi_pos = ben_gua_info["shi"]
    ying_pos = ben_gua_info["ying"]

    # 构建每爻完整信息
    yao_detail = []
    for i, line in enumerate(lines):
        pos = i + 1
        najia = najia_lines[i]
        dizhi_wx = najia["五行"]
        liuqin = calc_liuqin(ben_gua_info["wuxing"], dizhi_wx)
        yao_detail.append({
            "爻位": pos,
            "阴阳": "—" if line["yao"] == 1 else "- -",
            "卦画": yao_to_diagram(line["yao"], line["changing"]),
            "摇卦结果": line["value"],
            "铜钱": "".join(line["coins"]),
            "纳甲": najia["干支"],
            "天干": najia["天干"],
            "地支": najia["地支"],
            "地支五行": dizhi_wx,
            "六亲": liuqin,
            "六神": liushen[i],
            "世应": "世" if pos == shi_pos else "应" if pos == ying_pos else "",
            "动变": "动" if line["changing"] else "",
        })

    # 变卦爻信息
    if bian_gua_info:
        bian_najia = get_najia_for_gua(najia_db, bian_gua_info)
        for i in range(6):
            if (i + 1) in changing_positions:
                bn = bian_najia[i]
                yao_detail[i]["变爻"] = {
                    "变卦": bian_gua_name,
                    "变纳甲": bn["干支"],
                    "变地支": bn["地支"],
                    "变五行": bn["五行"],
                    "变六亲": calc_liuqin(ben_gua_info["wuxing"], bn["五行"]),
                }

    result = {
        "占卜时间": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "年干支": year_ganzhi,
        "月建": month_zhi,
        "月干支": month_ganzhi,
        "月建五行": cal["月建五行"],
        "日干支": day_ganzhi,
        "日干": day_gan,
        "日支": day_zhi,
        "日建五行": cal["日建五行"],
        "本卦": {
            "name": ben_gua_name,
            "palace": ben_gua_info["palace"],
            "wuxing": ben_gua_info["wuxing"],
            "shang": ben_gua_info["shang"],
            "xia": ben_gua_info["xia"],
            "上卦图": BAGUA_PIC[ben_gua_info["shang"]],
            "下卦图": BAGUA_PIC[ben_gua_info["xia"]],
            "shi": shi_pos,
            "ying": ying_pos,
        },
        "变卦": {
            "name": bian_gua_name,
            "palace": bian_gua_info["palace"],
            "wuxing": bian_gua_info["wuxing"],
            "shang": bian_gua_info["shang"],
            "xia": bian_gua_info["xia"],
            "上卦图": BAGUA_PIC[bian_gua_info["shang"]],
            "下卦图": BAGUA_PIC[bian_gua_info["xia"]],
        },
        "动爻": changing_positions,
        "爻位详情": yao_detail,
    }
    return result


def main():
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
    import argparse
    parser = argparse.ArgumentParser(description="六爻纳甲起卦")
    parser.add_argument("--lines", type=str, default=None,
                        help="手动输入6爻铜钱结果，格式: '正正反,正反反,...' (6组，逗号分隔)")
    parser.add_argument("--day-gan", type=str, default=None, help="日干 (甲-癸)")
    args = parser.parse_args()

    if args.lines:
        line_strs = args.lines.split(",")
        lines = []
        for s in line_strs:
            s = s.strip()
            backs = s.count("反")
            if backs == 0:  # 三字 → 老阴
                lines.append({"value": "老阴", "yao": 0, "changing": True, "coins": list(s), "bei": 0, "position": len(lines) + 1})
            elif backs == 1:  # 单背 → 少阳
                lines.append({"value": "少阳", "yao": 1, "changing": False, "coins": list(s), "bei": 1, "position": len(lines) + 1})
            elif backs == 2:  # 双背 → 少阴
                lines.append({"value": "少阴", "yao": 0, "changing": False, "coins": list(s), "bei": 2, "position": len(lines) + 1})
            else:  # 三背 → 老阳
                lines.append({"value": "老阳", "yao": 1, "changing": True, "coins": list(s), "bei": 3, "position": len(lines) + 1})
        result = run_liuyao(lines=lines, day_gan=args.day_gan)
    else:
        result = run_liuyao(day_gan=args.day_gan)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
