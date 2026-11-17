# -*- coding: utf-8 -*-
"""
meihua.py - 梅花易数起卦（先天八卦数）

依赖：lunar_python（仅用于公历->农历，以便"按时间起卦"取农历年月日时）。
      该运行库需由部署方在运行环境中预先提供，本脚本不含安装指令。

用法：
  # 按时间起卦（默认，取农历年月日时辰）
  python meihua.py --year 2024 --month 7 --day 3 --hour 14 --minute 30
  # 报数起卦
  python meihua.py --numbers 8 6
  # 随机起卦
  python meihua.py --random

规则：
  先天八卦数：乾1 兑2 離3 震4 巽5 坎6 艮7 坤8
  上卦 = (年+月+日) % 8 ；下卦 = (年+月+日+时) % 8 ；动爻 = (年+月+日+时) % 6
  （取农历：年取地支序数1-12，月取农历月数，日取农历日，时取时辰序数1-12）
  体用：动爻所在之卦为「用」，无动爻之卦为「体」。

仅作规则推演参考，最终判断请结合处境或咨询真人大师。
"""
import argparse
import sys
import datetime
import random

try:
    import lunar_python as L
except ImportError:
    sys.stderr.write(
        "ERROR: 运行环境缺少依赖 lunar_python。\n"
        "请由部署方在运行环境中预先提供该库后重试"
        "（本脚本不含安装指令）。\n"
    )
    sys.exit(2)

# 先天八卦
XIANTIAN = {1: "乾", 2: "兑", 3: "離", 4: "震", 5: "巽", 6: "坎", 7: "艮", 8: "坤"}
TRI_WX = {1: "金", 2: "金", 3: "火", 4: "木", 5: "木", 6: "水", 7: "土", 8: "土"}
ZHI_ORDER = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
ZHI_NUM = {z: i + 1 for i, z in enumerate(ZHI_ORDER)}  # 子1..亥12

# 卦数<->3位二进制（乾111..坤000）
NUM_BITS = {1: 0b111, 2: 0b110, 3: 0b101, 4: 0b100, 5: 0b011, 6: 0b010, 7: 0b001, 8: 0b000}
BITS_NUM = {v: k for k, v in NUM_BITS.items()}

# 六十四卦名 (上卦数, 下卦数) -> 卦名
GUA_NAME = {
    (1, 1): "乾为天", (1, 2): "天泽履", (1, 3): "天火同人", (1, 4): "天雷无妄",
    (1, 5): "天风姤", (1, 6): "天水讼", (1, 7): "天山遁", (1, 8): "天地否",
    (2, 1): "泽天夬", (2, 2): "兑为泽", (2, 3): "泽火革", (2, 4): "泽雷随",
    (2, 5): "泽风大过", (2, 6): "泽水困", (2, 7): "泽山咸", (2, 8): "泽地萃",
    (3, 1): "火天大有", (3, 2): "火泽睽", (3, 3): "离为火", (3, 4): "火雷噬嗑",
    (3, 5): "火风鼎", (3, 6): "火水未济", (3, 7): "火山旅", (3, 8): "火地晋",
    (4, 1): "雷天大壮", (4, 2): "雷泽归妹", (4, 3): "雷火丰", (4, 4): "震为雷",
    (4, 5): "雷风恒", (4, 6): "雷水解", (4, 7): "雷山小过", (4, 8): "雷地豫",
    (5, 1): "风天小畜", (5, 2): "风泽中孚", (5, 3): "风火家人", (5, 4): "风雷益",
    (5, 5): "巽为风", (5, 6): "风水涣", (5, 7): "风山渐", (5, 8): "风地观",
    (6, 1): "水天需", (6, 2): "水泽节", (6, 3): "水火既济", (6, 4): "水雷屯",
    (6, 5): "水风井", (6, 6): "坎为水", (6, 7): "水山蹇", (6, 8): "水地比",
    (7, 1): "山天大畜", (7, 2): "山泽损", (7, 3): "山火贲", (7, 4): "山雷颐",
    (7, 5): "山风蛊", (7, 6): "山水蒙", (7, 7): "艮为山", (7, 8): "山地剥",
    (8, 1): "地天泰", (8, 2): "地泽临", (8, 3): "地火明夷", (8, 4): "地雷复",
    (8, 5): "地风升", (8, 6): "地水师", (8, 7): "地山谦", (8, 8): "坤为地",
}
# 卦义（简版，一句）
GUA_YI = {
    "乾为天": "刚健中正，诸事亨通但忌傲。", "天泽履": "循礼而行则安，慎防失足。",
    "天火同人": "和同于人，合作得力。", "天雷无妄": "不妄动则吉，妄为招灾。",
    "天风姤": "不期而遇，防阴长侵阳。", "天水讼": "争讼之象，宜止宜和。",
    "天山遁": "退避以存身，适时而隐。", "天地否": "闭塞不通，待时而通。",
    "泽天夬": "决而能和，去小人宜果。", "兑为泽": "喜悦相说，口舌亦生。",
    "泽火革": "顺天应人，革故鼎新。", "泽雷随": "随时而动，从善得吉。",
    "泽风大过": "大过之时，独立不惧。", "泽水困": "困而学之，静守待变。",
    "泽山咸": "感应相通，婚恋和合。", "泽地萃": "荟萃聚集，用人聚财。",
    "火天大有": "富有大有，遏恶扬善。", "火泽睽": "乖离相违，求同存异。",
    "离为火": "光明附丽，柔顺得中。", "火雷噬嗑": "咬合去梗，难事可解。",
    "火风鼎": "鼎新取象，养贤致用。", "火水未济": "事未成终，慎防反复。",
    "火山旅": "行旅在外，不安则凶。", "火地晋": "进而显明，前途光明。",
    "雷天大壮": "阳刚壮盛，不可恃强。", "雷泽归妹": "归妹失正，行事有咎。",
    "雷火丰": "丰大盛极，宜守不宜满。", "震为雷": "震动惊惧，临危不乱。",
    "雷风恒": "恒久不已，守常得成。", "雷水解": "险难消解，舒缓解脱。",
    "雷山小过": "小者过越，宜下不宜上。", "雷地豫": "欢悦安逸，预则立。",
    "风天小畜": "小有蓄积，待时而发。", "风泽中孚": "诚信在中，心诚则灵。",
    "风火家人": "齐家有序，内和外用。", "风雷益": "损上益下，与时偕行。",
    "巽为风": "顺从而入，谦逊得利。", "风水涣": "涣散疏通，聚气散疑。",
    "风山渐": "循序渐进，渐入佳境。", "风地观": "观察省视，静观其变。",
    "水天需": "需待时机，饮食宴乐。", "水泽节": "节制有度，适可而止。",
    "水火既济": "事已成济，防败于终。", "水雷屯": "初生艰难，步步为营。",
    "水风井": "养而不穷，井养不穷。", "坎为水": "重险重重，维心亨通。",
    "水山蹇": "蹇难在前，止而思反。", "水地比": "亲比相辅，择善而从。",
    "山天大畜": "厚畜待发，止健笃实。", "山泽损": "损下益上，损益有节。",
    "山火贲": "文饰外观，质美需显。", "山雷颐": "颐养之道，慎言节食。",
    "山风蛊": "蛊坏待治，振弊出新。", "山水蒙": "启蒙发智，循序渐进。",
    "艮为山": "止而不动，安分守静。", "山地剥": "剥落侵蚀，防微杜渐。",
    "地天泰": "天地交泰，通泰安舒。", "地泽临": "临下亲民，渐进得位。",
    "地火明夷": "明入地中，韬光养晦。", "地雷复": "一阳来复，生机重启。",
    "地风升": "积小成高，柔顺上升。", "地水师": "兵众用师，纪律为先。",
    "地山谦": "谦尊而光，谦受益。", "坤为地": "厚德载物，顺承乎天。",
}


def bit_to_num(bits):
    return BITS_NUM[bits & 0b111]


def num_to_bits(n):
    return NUM_BITS[n]


def trigram_reverse(n):
    """先天卦反象：阴阳全反，数 = 9 - n"""
    return 9 - n


def time_to_yue_ri_shi(year, month, day, hour):
    """公历 -> 农历 年地支序数 / 月 / 日 / 时辰序数"""
    sol = L.Solar.fromYmdHms(year, month, day, hour, 0, 0)
    lun = L.Lunar.fromSolar(sol)
    year_zhi = lun.getYearZhi()           # 地支字
    ynum = ZHI_NUM.get(year_zhi, 1)
    mnum = abs(lun.getMonth())           # 农历月（闰月取绝对值）
    dnum = lun.getDay()                  # 农历日
    # 时辰：23-1子,1-3丑,...
    if hour == 23 or hour == 0:
        snum = 1
    else:
        snum = ZHI_NUM[ZHI_ORDER[(hour + 1) // 2 % 12]]
    return ynum, mnum, dnum, snum


def build_gua(up, down, dong):
    """由上下卦数、动爻(1-6)推本卦/变卦/互卦及体用"""
    # 本卦六爻（顶->底）
    ub = num_to_bits(up)
    db = num_to_bits(down)
    lines = [(ub >> 2) & 1, (ub >> 1) & 1, ub & 1, (db >> 2) & 1, (db >> 1) & 1, db & 1]
    # 动爻位置 p(1=初..6=上) -> 翻转 lines[6-p]
    p = dong
    lines2 = list(lines)
    lines2[6 - p] ^= 1
    # 变卦上下
    up2 = bit_to_num((lines2[0] << 2) | (lines2[1] << 1) | lines2[2])
    down2 = bit_to_num((lines2[3] << 2) | (lines2[4] << 1) | lines2[5])
    # 互卦：下互=二三四爻, 上互=三四五爻
    hu_down = bit_to_num((lines[1] << 2) | (lines[2] << 1) | lines[3])
    hu_up = bit_to_num((lines[2] << 2) | (lines[3] << 1) | lines[4])
    # 体用：动爻在下(1-3)=下卦为用；在上(4-6)=上卦为用
    if p <= 3:
        ti, yong = up, down        # 体=上(静), 用=下(动)
    else:
        ti, yong = down, up        # 体=下(静), 用=上(动)
    return {
        "本卦": (up, down), "变卦": (up2, down2), "互卦": (hu_up, hu_down),
        "动爻": p, "体": ti, "用": yong,
    }


def shenke(ti, yong):
    """体用生克判定（五行）"""
    tw = TRI_WX[ti]
    yw = TRI_WX[yong]
    gen = {"金": "水", "水": "木", "木": "火", "火": "土", "土": "金"}
    ke = {"金": "木", "木": "土", "土": "水", "水": "火", "火": "金"}
    if yw == tw:
        return "比和", "平（顺遂，宜守成）"
    if gen[yw] == tw:
        return "用生体", "吉（得外助，谋事易成）"
    if ke[tw] == yw:
        return "体克用", "吉（我克得住，有利可得）"
    if gen[tw] == yw:
        return "体生用", "耗（我泄于外，费力少功）"
    # 余下：用克体
    return "用克体", "凶（外克内，事多阻碍难成）"


YINGQI = {
    1: "应期近：当日或三日内。",
    2: "应期短：数日乃至一周内。",
    3: "应期中：旬月之间。",
    4: "应期月：一两月内。",
    5: "应期远：一季或更久。",
    6: "应期久：经年或长远。",
}


def meihua(year=None, month=None, day=None, hour=None, numbers=None, rand=False):
    if rand:
        a = random.randint(1, 99)
        b = random.randint(1, 99)
        up = (a - 1) % 8 + 1
        down = (b - 1) % 8 + 1
        dong = (a + b - 1) % 6 + 1
        method = "随机起卦（%d, %d）" % (a, b)
    elif numbers:
        a, b = numbers
        up = (a - 1) % 8 + 1
        down = (b - 1) % 8 + 1
        dong = (a + b - 1) % 6 + 1
        method = "报数法（%d, %d）" % (a, b)
    else:
        ynum, mnum, dnum, snum = time_to_yue_ri_shi(year, month, day, hour)
        s = ynum + mnum + dnum + snum
        up = (ynum + mnum + dnum - 1) % 8 + 1
        down = (s - 1) % 8 + 1
        dong = (s - 1) % 6 + 1
        method = "按时间起卦（农历 年%d 月%d 日%d 时%d）" % (ynum, mnum, dnum, snum)
    g = build_gua(up, down, dong)
    rel, verdict = shenke(g["体"], g["用"])
    return {
        "起卦方式": method,
        "本卦": "%s（上%s下%s）" % (GUA_NAME[g["本卦"]], XIANTIAN[up], XIANTIAN[down]),
        "变卦": "%s（上%s下%s）" % (GUA_NAME[g["变卦"]], XIANTIAN[g["变卦"][0]], XIANTIAN[g["变卦"][1]]),
        "互卦": "%s（上%s下%s）" % (GUA_NAME[g["互卦"]], XIANTIAN[g["互卦"][0]], XIANTIAN[g["互卦"][1]]),
        "动爻": g["动爻"],
        "体用": "体=%s(%s)  用=%s(%s)" % (XIANTIAN[g["体"]], TRI_WX[g["体"]], XIANTIAN[g["用"]], TRI_WX[g["用"]]),
        "生克": rel,
        "断语": verdict,
        "卦义": GUA_YI.get(GUA_NAME[g["本卦"]], ""),
        "应期": YINGQI[g["动爻"]],
    }


def format_text(r):
    lines = ["【梅花易数起卦】", "起卦：" + r["起卦方式"], ""]
    lines.append("本卦：" + r["本卦"])
    lines.append("  卦义：" + r["卦义"])
    lines.append("变卦：" + r["变卦"])
    lines.append("互卦：" + r["互卦"])
    lines.append("动爻：第 %d 爻" % r["动爻"])
    lines.append("体用：" + r["体用"])
    lines.append("生克：" + r["生克"] + " —— " + r["断语"])
    lines.append("应期：" + r["应期"])
    lines.append("")
    lines.append("结论：%s" % ("宜行（吉）" if r["生克"] in ("用生体", "体克用", "比和") else "缓/避（耗或凶）"))
    lines.append("（本结果为规则推演参考，最终洞察请结合处境或咨询真人大师）")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="梅花易数起卦")
    ap.add_argument("--year", type=int)
    ap.add_argument("--month", type=int)
    ap.add_argument("--hour", type=int, default=12)
    ap.add_argument("--minute", type=int, default=0)
    ap.add_argument("--day", type=int)
    ap.add_argument("--numbers", nargs=2, type=int, metavar=("A", "B"))
    ap.add_argument("--random", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.random:
        r = meihua(rand=True)
    elif args.numbers:
        r = meihua(numbers=tuple(args.numbers))
    else:
        if not (args.year and args.month and args.day):
            ap.error("需提供 --year --month --day，或 --numbers A B，或 --random")
        r = meihua(year=args.year, month=args.month, day=args.day, hour=args.hour)
    if args.json:
        import json
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(format_text(r))


if __name__ == "__main__":
    main()
