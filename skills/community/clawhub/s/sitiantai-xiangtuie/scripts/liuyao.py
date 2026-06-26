"""
liuyao.py — 六爻排盘引擎（司天监象推演系统）

合并：dizhi.py + guagong.py + wangshuai.py + main.py 核心
移除交互CLI，保留纯API接口
依赖：calendar.py 提供精算干支
"""

from datetime import datetime,date
from typing import Dict,List,Tuple,Optional,Any

# 核心旺衰评分引擎（开源版：月建旺相休囚死 + 日建七效应）
from .wangshuai_score import seasonal_status as _get_seasonal_status
from .wangshuai_score import calculate_strength as _calculate_yao_strength
from .wangshuai_score import batch_calculate_strength as _batch_calculate_strength

# ══════════════════════════════════════════════════════════
# 常量与配置 (dizhi + main 合并)
# ══════════════════════════════════════════════════════════

GAN_ORDER = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
ZHI_ORDER = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

BRANCH_WUXING = {
    "子":"水","丑":"土","寅":"木","卯":"木","辰":"土","巳":"火",
    "午":"火","未":"土","申":"金","酉":"金","戌":"土","亥":"水",
}

LIUSHOU = ["青龙","朱雀","勾陈","螣蛇","白虎","玄武"]

# 六神起法：按日干（传统京房规则）
# 甲乙→青龙, 丙丁→朱雀, 戊→勾陈, 己→螣蛇, 庚辛→白虎, 壬癸→玄武
GAN_TO_LIUSHOU = {
    "甲": 0, "乙": 0,
    "丙": 1, "丁": 1,
    "戊": 2,
    "己": 3,
    "庚": 4, "辛": 4,
    "壬": 5, "癸": 5,
}

# ══════════════════════════════════════════════════════════
# 纳甲地支（六爻核心数据，严格按传统京房纳甲体系）
# ══════════════════════════════════════════════════════════
# 内卦纳甲（初爻→三爻，从下往上）
NAJIA_INNER = {
    "乾宫": ["子", "寅", "辰"],
    "坤宫": ["未", "巳", "卯"],
    "震宫": ["子", "寅", "辰"],
    "巽宫": ["丑", "亥", "酉"],
    "坎宫": ["寅", "辰", "午"],
    "离宫": ["卯", "丑", "亥"],
    "艮宫": ["辰", "午", "申"],
    "兑宫": ["巳", "卯", "丑"],
}
# 外卦纳甲（四爻→上爻，从下往上）
NAJIA_OUTER = {
    "乾宫": ["午", "申", "戌"],
    "坤宫": ["丑", "亥", "酉"],
    "震宫": ["午", "申", "戌"],
    "巽宫": ["未", "巳", "卯"],
    "坎宫": ["申", "戌", "子"],
    "离宫": ["酉", "未", "巳"],
    "艮宫": ["戌", "子", "寅"],
    "兑宫": ["亥", "酉", "未"],
}

# 卦宫五行（六亲计算以本卦宫五行为"我"）
PALACE_WUXING = {
    "乾宫": "金", "坤宫": "土", "震宫": "木", "巽宫": "木",
    "坎宫": "水", "离宫": "火", "艮宫": "土", "兑宫": "金",
}

XUN_START = ["甲子","甲戌","甲申","甲午","甲辰","甲寅"]
XUN_END   = ["癸酉","癸未","癸巳","癸卯","癸丑","癸亥"]
XUN_KONG_MAP = {
    "甲子": ["戌","亥"],"甲戌": ["申","酉"],"甲申": ["午","未"],
    "甲午": ["辰","巳"],"甲辰": ["寅","卯"],"甲寅": ["子","丑"],
}


# Trigram (3-bit tuple, _hex_to_binary 输出: 1=阳,0=阴) → 纳甲宫名 lookup
# 索引顺序：初爻,二爻,三爻（从下往上）
TRIGRAM_TO_NAJIA = {
    (1,1,1): "乾宫",  # 乾(阳阳阳)
    (1,1,0): "兑宫",  # 兑(阳阳阴)
    (1,0,1): "离宫",  # 离(阳阴阳)
    (1,0,0): "震宫",  # 震(阳阴阴)
    (0,1,1): "巽宫",  # 巽(阴阳阳)
    (0,1,0): "坎宫",  # 坎(阴阳阴)
    (0,0,1): "艮宫",  # 艮(阴阴阳)
    (0,0,0): "坤宫",  # 坤(阴阴阴)
}

# ══════════════════════════════════════════════════════════
# 64卦宫位查找表 (guagong.py 内联)
# ══════════════════════════════════════════════════════════

HEXAGRAMS = {
    "1,1,1,1,1,1":{"宫名":"乾宫","世爻索引":5,"应爻索引":2,"卦类型":"本宫卦","卦名":"乾为天"},
    "0,1,1,1,1,1":{"宫名":"乾宫","世爻索引":0,"应爻索引":3,"卦类型":"一世卦","卦名":"天风姤"},
    "0,0,1,1,1,1":{"宫名":"乾宫","世爻索引":1,"应爻索引":4,"卦类型":"二世卦","卦名":"天山遯"},
    "0,0,0,1,1,1":{"宫名":"乾宫","世爻索引":2,"应爻索引":5,"卦类型":"三世卦","卦名":"天地否"},
    "0,0,0,0,1,1":{"宫名":"乾宫","世爻索引":3,"应爻索引":0,"卦类型":"四世卦","卦名":"风地观"},
    "0,0,0,0,0,1":{"宫名":"乾宫","世爻索引":4,"应爻索引":1,"卦类型":"五世卦","卦名":"山地剥"},
    "0,0,0,1,0,1":{"宫名":"乾宫","世爻索引":3,"应爻索引":0,"卦类型":"游魂卦","卦名":"火地晋"},
    "1,1,1,1,0,1":{"宫名":"乾宫","世爻索引":2,"应爻索引":5,"卦类型":"归魂卦","卦名":"火天大有"},
    "0,0,0,0,0,0":{"宫名":"坤宫","世爻索引":5,"应爻索引":2,"卦类型":"本宫卦","卦名":"坤为地"},
    "1,0,0,0,0,0":{"宫名":"坤宫","世爻索引":0,"应爻索引":3,"卦类型":"一世卦","卦名":"地雷复"},
    "1,1,0,0,0,0":{"宫名":"坤宫","世爻索引":1,"应爻索引":4,"卦类型":"二世卦","卦名":"地泽临"},
    "1,1,1,0,0,0":{"宫名":"坤宫","世爻索引":2,"应爻索引":5,"卦类型":"三世卦","卦名":"地天泰"},
    "1,1,1,1,0,0":{"宫名":"坤宫","世爻索引":3,"应爻索引":0,"卦类型":"四世卦","卦名":"雷天大壮"},
    "1,1,1,1,1,0":{"宫名":"坤宫","世爻索引":4,"应爻索引":1,"卦类型":"五世卦","卦名":"泽天夬"},
    "1,1,1,0,1,0":{"宫名":"坤宫","世爻索引":3,"应爻索引":0,"卦类型":"游魂卦","卦名":"水天需"},
    "0,0,0,0,1,0":{"宫名":"坤宫","世爻索引":2,"应爻索引":5,"卦类型":"归魂卦","卦名":"水地比"},
    "0,1,0,0,1,0":{"宫名":"坎宫","世爻索引":5,"应爻索引":2,"卦类型":"本宫卦","卦名":"坎为水"},
    "1,1,0,0,1,0":{"宫名":"坎宫","世爻索引":0,"应爻索引":3,"卦类型":"一世卦","卦名":"水泽节"},
    "1,0,0,0,1,0":{"宫名":"坎宫","世爻索引":1,"应爻索引":4,"卦类型":"二世卦","卦名":"水雷屯"},
    "1,0,1,0,1,0":{"宫名":"坎宫","世爻索引":2,"应爻索引":5,"卦类型":"三世卦","卦名":"水火既济"},
    "1,0,1,1,1,0":{"宫名":"坎宫","世爻索引":3,"应爻索引":0,"卦类型":"四世卦","卦名":"泽火革"},
    "1,0,1,1,0,0":{"宫名":"坎宫","世爻索引":4,"应爻索引":1,"卦类型":"五世卦","卦名":"雷火丰"},
    "1,0,1,0,0,0":{"宫名":"坎宫","世爻索引":3,"应爻索引":0,"卦类型":"游魂卦","卦名":"地火明夷"},
    "0,1,0,0,0,0":{"宫名":"坎宫","世爻索引":2,"应爻索引":5,"卦类型":"归魂卦","卦名":"地水师"},
    "1,0,1,1,0,1":{"宫名":"离宫","世爻索引":5,"应爻索引":2,"卦类型":"本宫卦","卦名":"离为火"},
    "0,0,1,1,0,1":{"宫名":"离宫","世爻索引":0,"应爻索引":3,"卦类型":"一世卦","卦名":"火山旅"},
    "0,1,1,1,0,1":{"宫名":"离宫","世爻索引":1,"应爻索引":4,"卦类型":"二世卦","卦名":"火风鼎"},
    "0,1,0,1,0,1":{"宫名":"离宫","世爻索引":2,"应爻索引":5,"卦类型":"三世卦","卦名":"火水未济"},
    "0,1,0,0,0,1":{"宫名":"离宫","世爻索引":3,"应爻索引":0,"卦类型":"四世卦","卦名":"山水蒙"},
    "0,1,0,0,1,1":{"宫名":"离宫","世爻索引":4,"应爻索引":1,"卦类型":"五世卦","卦名":"风水涣"},
    "0,1,0,1,1,1":{"宫名":"离宫","世爻索引":3,"应爻索引":0,"卦类型":"游魂卦","卦名":"天水讼"},
    "1,0,1,1,1,1":{"宫名":"离宫","世爻索引":2,"应爻索引":5,"卦类型":"归魂卦","卦名":"天火同人"},
    "1,0,0,1,0,0":{"宫名":"震宫","世爻索引":5,"应爻索引":2,"卦类型":"本宫卦","卦名":"震为雷"},
    "0,0,0,1,0,0":{"宫名":"震宫","世爻索引":0,"应爻索引":3,"卦类型":"一世卦","卦名":"雷地豫"},
    "0,1,0,1,0,0":{"宫名":"震宫","世爻索引":1,"应爻索引":4,"卦类型":"二世卦","卦名":"雷水解"},
    "0,1,1,1,0,0":{"宫名":"震宫","世爻索引":2,"应爻索引":5,"卦类型":"三世卦","卦名":"雷风恒"},
    "0,1,1,0,0,0":{"宫名":"震宫","世爻索引":3,"应爻索引":0,"卦类型":"四世卦","卦名":"地风升"},
    "0,1,1,0,1,0":{"宫名":"震宫","世爻索引":4,"应爻索引":1,"卦类型":"五世卦","卦名":"水风井"},
    "0,1,1,1,1,0":{"宫名":"震宫","世爻索引":3,"应爻索引":0,"卦类型":"游魂卦","卦名":"泽风大过"},
    "1,0,0,1,1,0":{"宫名":"震宫","世爻索引":2,"应爻索引":5,"卦类型":"归魂卦","卦名":"泽雷随"},
    "0,1,1,0,1,1":{"宫名":"巽宫","世爻索引":5,"应爻索引":2,"卦类型":"本宫卦","卦名":"巽为风"},
    "1,1,1,0,1,1":{"宫名":"巽宫","世爻索引":0,"应爻索引":3,"卦类型":"一世卦","卦名":"风天小畜"},
    "1,0,1,0,1,1":{"宫名":"巽宫","世爻索引":1,"应爻索引":4,"卦类型":"二世卦","卦名":"风火家人"},
    "1,0,0,0,1,1":{"宫名":"巽宫","世爻索引":2,"应爻索引":5,"卦类型":"三世卦","卦名":"风雷益"},
    "1,0,0,1,1,1":{"宫名":"巽宫","世爻索引":3,"应爻索引":0,"卦类型":"四世卦","卦名":"天雷无妄"},
    "1,0,0,1,0,1":{"宫名":"巽宫","世爻索引":4,"应爻索引":1,"卦类型":"五世卦","卦名":"火雷噬嗑"},
    "1,0,0,0,0,1":{"宫名":"巽宫","世爻索引":3,"应爻索引":0,"卦类型":"游魂卦","卦名":"山雷颐"},
    "0,1,1,0,0,1":{"宫名":"巽宫","世爻索引":2,"应爻索引":5,"卦类型":"归魂卦","卦名":"山风蛊"},
    "0,0,1,0,0,1":{"宫名":"艮宫","世爻索引":5,"应爻索引":2,"卦类型":"本宫卦","卦名":"艮为山"},
    "1,0,1,0,0,1":{"宫名":"艮宫","世爻索引":0,"应爻索引":3,"卦类型":"一世卦","卦名":"山火贲"},
    "1,1,1,0,0,1":{"宫名":"艮宫","世爻索引":1,"应爻索引":4,"卦类型":"二世卦","卦名":"山天大畜"},
    "1,1,0,0,0,1":{"宫名":"艮宫","世爻索引":2,"应爻索引":5,"卦类型":"三世卦","卦名":"山泽损"},
    "1,1,0,1,0,1":{"宫名":"艮宫","世爻索引":3,"应爻索引":0,"卦类型":"四世卦","卦名":"火泽睽"},
    "1,1,0,1,1,1":{"宫名":"艮宫","世爻索引":4,"应爻索引":1,"卦类型":"五世卦","卦名":"天泽履"},
    "1,1,0,0,1,1":{"宫名":"艮宫","世爻索引":3,"应爻索引":0,"卦类型":"游魂卦","卦名":"风泽中孚"},
    "0,0,1,0,1,1":{"宫名":"艮宫","世爻索引":2,"应爻索引":5,"卦类型":"归魂卦","卦名":"风山渐"},
    "1,1,0,1,1,0":{"宫名":"兑宫","世爻索引":5,"应爻索引":2,"卦类型":"本宫卦","卦名":"兑为泽"},
    "0,1,0,1,1,0":{"宫名":"兑宫","世爻索引":0,"应爻索引":3,"卦类型":"一世卦","卦名":"泽水困"},
    "0,0,0,1,1,0":{"宫名":"兑宫","世爻索引":1,"应爻索引":4,"卦类型":"二世卦","卦名":"泽地萃"},
    "0,0,1,1,1,0":{"宫名":"兑宫","世爻索引":2,"应爻索引":5,"卦类型":"三世卦","卦名":"泽山咸"},
    "0,0,1,0,1,0":{"宫名":"兑宫","世爻索引":3,"应爻索引":0,"卦类型":"四世卦","卦名":"水山蹇"},
    "0,0,1,0,0,0":{"宫名":"兑宫","世爻索引":4,"应爻索引":1,"卦类型":"五世卦","卦名":"地山谦"},
    "0,0,1,1,0,0":{"宫名":"兑宫","世爻索引":3,"应爻索引":0,"卦类型":"游魂卦","卦名":"雷山小过"},
    "1,1,0,1,0,0":{"宫名":"兑宫","世爻索引":2,"应爻索引":5,"卦类型":"归魂卦","卦名":"雷泽归妹"},
}


def _hex_to_binary(hexagram: List[int]) -> List[int]:
    """Convert 1-4 encoding to 0-1 binary.
    编码约定: 1=少阴, 2=少阳, 3=老阳(动), 4=老阴(动)
    输出约定: 1=阳爻, 0=阴爻（与 HEXAGRAMS key 一致）
    """
    return [1 if x in [2,3] else 0 for x in hexagram]


def get_hexagram_palace(hexagram: List[int]) -> dict:
    binary = _hex_to_binary(hexagram)
    key = ",".join(str(x) for x in binary)
    return HEXAGRAMS.get(key, {"宫名":"未知","卦名":"未知","卦类型":"未知","世爻索引":0,"应爻索引":3})


# ══════════════════════════════════════════════════════════
# 旺衰计算模块 (wangshuai.py 内联)
# ══════════════════════════════════════════════════════════

CONFLICT_BRANCH = {"子":"午","午":"子","丑":"未","未":"丑","寅":"申","申":"寅",
                    "卯":"酉","酉":"卯","辰":"戌","戌":"辰","巳":"亥","亥":"巳"}
COMBINE_BRANCH  = {"子":"丑","丑":"子","寅":"亥","亥":"寅","卯":"戌","戌":"卯",
                    "辰":"酉","酉":"辰","巳":"申","申":"巳","午":"未","未":"午"}
TOMB_BRANCH     = {"木":"未","火":"戌","金":"丑","水":"辰","土":["辰","戌","丑","未"]}
GENERATE_WUXING = {"木":"火","火":"土","土":"金","金":"水","水":"木"}
CONQUER_WUXING  = {"木":"土","土":"水","水":"火","火":"金","金":"木"}
IMPERIAL_WANG   = {"木":"卯","火":"午","金":"酉","水":"子","土":["辰","戌","丑","未"]}
EXTINCTION      = {"木":"申","火":"亥","金":"寅","水":"巳","土":"亥"}

# 三刑 / 六害
SANXING_BRANCH  = {"寅":"巳","巳":"申","申":"寅","丑":"戌","戌":"未","未":"丑","子":"卯","卯":"子"}
LIUHAI_BRANCH   = {"子":"未","未":"子","丑":"午","午":"丑","寅":"巳","巳":"寅","卯":"辰","辰":"卯","申":"亥","亥":"申","酉":"戌","戌":"酉"}

# ═══════ 旺衰评分移到 protected/wangshuai_score（保护层） ═══════


# ══════════════════════════════════════════════════════════
# 辅助计算函数
# ══════════════════════════════════════════════════════════

def _get_day_stem(year: int, month: int, day: int) -> str:
    base = date(1900,1,1); target = date(year,month,day)
    return GAN_ORDER[(6+(target-base).days)%10]


def _get_xunkong(day_ganzhi: str) -> List[str]:
    """计算旬空（修正版）。用60甲子循环位置精确匹配"""
    dg = day_ganzhi[0]; dz = day_ganzhi[1]
    # 在60甲子循环中查找位置（甲子=0, ..., 癸亥=59）
    idx = None
    for p in range(60):
        if GAN_ORDER[p % 10] == dg and ZHI_ORDER[p % 12] == dz:
            idx = p; break
    if idx is None:
        return ["", ""]
    # 旬的起始甲日位置，空亡=旬用10地支后剩余2个
    xun_start = (idx // 10) * 10
    empty_1 = (xun_start % 12 + 10) % 12
    empty_2 = (xun_start % 12 + 11) % 12
    return [ZHI_ORDER[empty_1], ZHI_ORDER[empty_2]]


def _get_liqin(wo_wx: str, target_wx: str) -> str:
    if not wo_wx or not target_wx: return ""
    if target_wx == wo_wx: return "兄弟"
    if GENERATE_WUXING.get(target_wx)==wo_wx: return "父母"
    if GENERATE_WUXING.get(wo_wx)==target_wx: return "子孙"
    if CONQUER_WUXING.get(target_wx)==wo_wx: return "官鬼"
    return "妻财"


def _get_liushou_order(day_stem: str) -> List[str]:
    """六神起法：按日干（京房传统规则）
    甲乙青龙、丙丁朱雀、戊勾陈、己螣蛇、庚辛白虎、壬癸玄武
    """
    idx = GAN_TO_LIUSHOU.get(day_stem, 0)
    return [LIUSHOU[(idx+i)%6] for i in range(6)]


def _generate_changed_hexagram(original: List[int]) -> List[int]:
    """变卦：老阳(3)→少阴(1), 老阴(4)→少阳(2)"""
    changed = []
    for line in original:
        if line==3: changed.append(1)   # 老阳→少阴
        elif line==4: changed.append(2)  # 老阴→少阳
        else: changed.append(line)
    if changed==original:
        for i in range(len(changed)):
            if original[i]==3: changed[i]=1; break
            elif original[i]==4: changed[i]=2; break
    return changed


def _check_additional_tomb(original_hexagram, original_branch,
                           changed_branch, strengths, is_original=True):
    moving_indices = [i for i,line in enumerate(original_hexagram) if line in [3,4]]
    for i in range(6):
        yw = BRANCH_WUXING[original_branch[i] if is_original else changed_branch[i]]
        tb = TOMB_BRANCH[yw]
        if not isinstance(tb,list): tb = [tb]
        if is_original and original_hexagram[i] not in [3,4]:
            for idx in moving_indices:
                if original_branch[idx] in tb:
                    strengths[i]["status"].append(f"入{['初','二','三','四','五','上'][idx]}爻墓")
        if is_original and original_hexagram[i] in [3,4]:
            if changed_branch and i<len(changed_branch):
                if changed_branch[i] in tb: strengths[i]["status"].append("入变爻墓")
        if not is_original and i in moving_indices:
            if original_branch[i] in tb: strengths[i]["status"].append("入本位动爻墓")
    return strengths


def _check_huitou(original_branch, changed_branch, moving_indices, changed_strength):
    for i in moving_indices:
        ow = BRANCH_WUXING[original_branch[i]]
        cw = BRANCH_WUXING[changed_branch[i]]
        if GENERATE_WUXING.get(cw)==ow: changed_strength[i]["status"].append("回头生")
        if CONQUER_WUXING.get(cw)==ow: changed_strength[i]["status"].append("回头克")
    return changed_strength


# ══════════════════════════════════════════════════════════
# 排盘入口
# ══════════════════════════════════════════════════════════

def arrange_hexagram(original_hexagram: List[int], time: datetime,
                     reason: str = "") -> Dict[str,Any]:
    """六爻完整排盘。输入：卦象编码[1=少阴,2=少阳,3=纯阳动,4=纯阴动]×6,
    时间datetime, 原因str → 返回dict含所有排盘数据"""

    positions = ["初爻","二爻","三爻","四爻","五爻","上爻"]
    line_names = {1:"少阴",2:"少阳",3:"老阳",4:"老阴"}
    line_symbols = {1:"-- --",2:"-----",3:"----- ○",4:"-- -- ×"}

    # 日干支 (优先用 calendar.py 精算)
    try:
        from calendar import calculate_bazi
        bz = calculate_bazi(time)
        day_ganzhi = bz["day"]
        hour_branch = bz["time"][1]
        month_branch = bz["month"][1]
        year_branch = bz["year"][1]
    except ImportError:
        day_ganzhi = _get_day_stem(time.year,time.month,time.day)+ZHI_ORDER[(time.date()-date(1900,1,1)).days%12]
        year_branch = ZHI_ORDER[(time.year-1900)%12]
        # simplified month/hour
        month_branch = ZHI_ORDER[(time.month+1)%12]
        hour_branch = ZHI_ORDER[((time.hour+1)//2)%12]

    day_branch = day_ganzhi[1]
    xunkong = _get_xunkong(day_ganzhi)
    day_stem = day_ganzhi[0]
    liushou_order = _get_liushou_order(day_stem)

    # 卦宫信息
    orig_info = get_hexagram_palace(original_hexagram)
    palace = orig_info["宫名"]; hex_name = orig_info["卦名"]
    # 纳甲：下卦取内卦纳甲，上卦取外卦纳甲
    orig_binary = _hex_to_binary(original_hexagram)
    lower_tri = tuple(orig_binary[0:3])
    upper_tri = tuple(orig_binary[3:6])
    lower_palace = TRIGRAM_TO_NAJIA.get(lower_tri, "乾宫")
    upper_palace = TRIGRAM_TO_NAJIA.get(upper_tri, "乾宫")
    orig_branch = NAJIA_INNER.get(lower_palace, NAJIA_INNER["乾宫"]) + \
                  NAJIA_OUTER.get(upper_palace, NAJIA_OUTER["乾宫"])
    shi_idx = orig_info["世爻索引"]; ying_idx = orig_info["应爻索引"]

    # 变卦
    has_moving = any(line in [3,4] for line in original_hexagram)
    changed_hex = _generate_changed_hexagram(original_hexagram) if has_moving else None
    changed_info = get_hexagram_palace(changed_hex) if has_moving and changed_hex else None
    # 变卦纳甲：同规则
    if has_moving and changed_info:
        ch_binary = _hex_to_binary(changed_hex)
        ch_lower_tri = tuple(ch_binary[0:3])
        ch_upper_tri = tuple(ch_binary[3:6])
        ch_lower_palace = TRIGRAM_TO_NAJIA.get(ch_lower_tri, "乾宫")
        ch_upper_palace = TRIGRAM_TO_NAJIA.get(ch_upper_tri, "乾宫")
        changed_branch = NAJIA_INNER.get(ch_lower_palace, NAJIA_INNER["乾宫"]) + \
                         NAJIA_OUTER.get(ch_upper_palace, NAJIA_OUTER["乾宫"])
    else:
        changed_branch = None

    # 六亲以本卦宫五行为"我"（传统六爻标准排法）
    palace_wx = PALACE_WUXING.get(palace, "金")
    is_moving = [line in [3,4] for line in original_hexagram]
    moving_indices = [i for i,m in enumerate(is_moving) if m]

    # 旺衰
    orig_strength = _batch_calculate_strength(orig_branch,month_branch,day_branch,
                                               changed_branch,is_moving)
    orig_strength = _check_additional_tomb(original_hexagram,orig_branch,
                                            changed_branch,orig_strength,True)

    changed_strength = None
    if has_moving and changed_hex and changed_branch:
        changed_strength = _batch_calculate_strength(changed_branch,month_branch,day_branch)
        changed_strength = _check_additional_tomb(original_hexagram,orig_branch,
                                                   changed_branch,changed_strength,False)
        changed_strength = _check_huitou(orig_branch,changed_branch,moving_indices,changed_strength)

    # 构建输出
    lines = []
    for i in range(5,-1,-1):
        lv = original_hexagram[i]; beast = liushou_order[i]
        br = orig_branch[i]; wx = BRANCH_WUXING[br]
        lq = _get_liqin(palace_wx,wx); st = orig_strength[i]
        shiying = "世" if i==shi_idx else ("应" if i==ying_idx else "-")
        lines.append({
            "爻位":positions[i],"卦象":line_names[lv],
            "地支":br,"五行":wx,"六亲":lq,"六兽":beast,
            "世应":shiying,"旺衰得分":st["score"],"状态":st["status"],
        })

    changed_lines = []
    if has_moving and changed_hex and changed_strength and changed_info:
        ch_shi = changed_info["世爻索引"]
        for i in range(5,-1,-1):
            lv = changed_hex[i]; beast = liushou_order[i]
            br = changed_branch[i]; wx = BRANCH_WUXING[br]
            lq = _get_liqin(palace_wx,wx); st = changed_strength[i]
            shiying = "世" if i==ch_shi else ("应" if i==(ch_shi+3)%6 else "-")
            changed_lines.append({
                "爻位":positions[i],"卦象":line_names[lv],
                "地支":br,"五行":wx,"六亲":lq,"六兽":beast,
                "世应":shiying,"旺衰得分":st["score"],"状态":st["status"],
            })

    return {
        "时间":time.isoformat(),
        "原因":reason,
        "年月日时":f"{year_branch} {month_branch} {day_branch} {hour_branch}",
        "日干支":day_ganzhi,"旬空":xunkong,
        "本卦":{"宫":palace,"名":hex_name,"类型":orig_info["卦类型"],
                "世爻":shi_idx,"应爻":ying_idx,"爻":lines},
        "变卦":None if not has_moving else {
            "宫":changed_info["宫名"],"名":changed_info["卦名"],
            "类型":changed_info["卦类型"],"爻":changed_lines,
            "动爻":moving_indices,
        },
        "动爻":moving_indices,
    }


# ══════════════════════════════════════════════════════════
# 卦名输入函数（v0.3.0 新增）
# ══════════════════════════════════════════════════════════

# 六十四卦名 → 二进制映射
_HEXAGRAM_BINARY_MAP = {}


def _init_hexagram_map():
    """初始化六十四卦名→二进制映射表"""
    if _HEXAGRAM_BINARY_MAP:
        return
    try:
        from scripts.meihua import BA_GUA, get_bian_gua_name
        from scripts.qigua import TRIGRAM_BINARY
    except ImportError:
        return

    # 遍历所有8×8=64卦组合，建立卦名→二进制映射
    for up_name in ["乾","兑","离","震","巽","坎","艮","坤"]:
        for down_name in ["乾","兑","离","震","巽","坎","艮","坤"]:
            name = get_bian_gua_name(up_name, down_name)
            # 二进制：下卦3位 + 上卦3位（从初爻到上爻）
            down_bin = TRIGRAM_BINARY.get(down_name, [0,0,0])
            up_bin = TRIGRAM_BINARY.get(up_name, [0,0,0])
            _HEXAGRAM_BINARY_MAP[name] = down_bin + up_bin

    # 兼容别名
    _HEXAGRAM_BINARY_MAP["乾为天"] = _HEXAGRAM_BINARY_MAP.get("乾为天", [1,1,1,1,1,1])
    _HEXAGRAM_BINARY_MAP["坤为地"] = _HEXAGRAM_BINARY_MAP.get("坤为地", [0,0,0,0,0,0])


def get_hexagram_binary(hexagram_name: str) -> List[int]:
    """卦名 → 六爻二进制列表（阳=1, 阴=0），从初爻到上爻"""
    _init_hexagram_map()

    # 去除可能的"→"或"之"后的变卦部分
    name = hexagram_name.split("→")[0].split("之")[0].strip()

    if name in _HEXAGRAM_BINARY_MAP:
        return _HEXAGRAM_BINARY_MAP[name]

    raise ValueError(f"未知卦名：{name}")


def binary_to_hexagram_encoding(binary: List[int]) -> List[int]:
    """
    六爻二进制列表 → 六爻编码。
    二进制: 1=阳, 0=阴（从初爻到上爻）
    编码: 1=少阴, 2=少阳
    """
    return [2 if b == 1 else 1 for b in binary]


def deduce_moving_lines(ben_binary: List[int], bian_binary: List[int]) -> List[int]:
    """
    对比本卦和变卦二进制，推算动爻位置。
    返回: 动爻索引列表（0-based，0=初爻, 5=上爻）
    """
    moving = []
    for i in range(6):
        if ben_binary[i] != bian_binary[i]:
            moving.append(i)
    return moving


def arrange_hexagram_by_name(ben_name: str, bian_name: Optional[str] = None,
                              time: Optional[datetime] = None,
                              reason: str = "") -> Dict:
    """
    卦名一键排盘。
    参数:
        ben_name: 本卦名（如"风天小畜"）
        bian_name: 变卦名（可选，如"风泽中孚"）
        time: 时间（默认当前）
        reason: 原因
    返回: arrange_hexagram 完整输出
    """
    if time is None:
        from datetime import datetime as dt
        time = dt.now()

    # 本卦二进制 → 编码
    ben_binary = get_hexagram_binary(ben_name)
    ben_encoding = binary_to_hexagram_encoding(ben_binary)

    # 如果有变卦，推算动爻并标记
    if bian_name:
        bian_binary = get_hexagram_binary(bian_name)
        moving_indices = deduce_moving_lines(ben_binary, bian_binary)
        for idx in moving_indices:
            # 编码索引：0=初爻, 5=上爻
            enc_idx = idx
            if 0 <= enc_idx < 6:
                if ben_encoding[enc_idx] == 2:  # 少阳→老阳(动)
                    ben_encoding[enc_idx] = 3
                elif ben_encoding[enc_idx] == 1:  # 少阴→老阴(动)
                    ben_encoding[enc_idx] = 4

    return arrange_hexagram(ben_encoding, time, reason)