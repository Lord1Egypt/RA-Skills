"""
meihua.py — 梅花易数排盘引擎（司天监象推演系统）

年月日时起卦法（优先 calendar.py 精算农历→fallback 简化）
含：互卦/变卦/错卦/综卦/体用
"""

from datetime import datetime
from typing import Dict,List,Tuple

# ═══════════════════════════════════════════
# 八卦名称
# ═══════════════════════════════════════════

# 注意：坤卦编号为 8（而非 0），避免模运算结果 0 导致 _GUA_HU 查表失败
BA_GUA = {1:"乾",2:"兑",3:"离",4:"震",5:"巽",6:"坎",7:"艮",8:"坤"}

# ═══════════════════════════════════════════
# 六十四卦互卦查找表 (caculate.py 原表)
# ═══════════════════════════════════════════

_GUA_HU = {
    11:["乾","乾","乾为天"],12:["巽","离","天泽履"],13:["乾","巽","天火同人"],
    14:["巽","艮","天雷无妄"],15:["乾","乾","天风姤"],16:["巽","离","天水讼"],
    17:["乾","巽","天山遯"],18:["巽","艮","天地否"],
    21:["乾","乾","泽天夬"],22:["巽","离","兑为泽"],23:["乾","巽","泽火革"],
    24:["巽","艮","泽雷随"],25:["乾","乾","泽风大过"],26:["巽","离","泽水困"],
    27:["乾","巽","泽山咸"],28:["巽","艮","泽地萃"],
    31:["兑","乾","火天大有"],32:["坎","离","火泽睽"],33:["兑","巽","离为火"],
    34:["坎","艮","火雷噬嗑"],35:["兑","乾","火风鼎"],36:["坎","离","火水未济"],
    37:["兑","巽","火山旅"],38:["坎","艮","火地晋"],
    41:["兑","乾","雷天大壮"],42:["坎","离","雷泽归妹"],43:["兑","巽","雷火丰"],
    44:["坎","艮","震为雷"],45:["兑","乾","雷风恒"],46:["坎","离","雷水解"],
    47:["兑","巽","雷山小过"],48:["坎","艮","雷地豫"],
    51:["离","兑","风天小畜"],52:["艮","震","风泽中孚"],53:["离","坎","风火家人"],
    54:["艮","坤","风雷益"],55:["离","兑","巽为风"],56:["艮","震","风水涣"],
    57:["离","坎","风山渐"],58:["艮","坤","风地观"],
    61:["离","兑","水天需"],62:["艮","震","水泽节"],63:["离","坎","水火既济"],
    64:["艮","坤","水雷屯"],65:["离","兑","水风井"],66:["艮","震","坎为水"],
    67:["离","坎","水山蹇"],68:["艮","坤","水地比"],
    71:["震","兑","山天大畜"],72:["坤","震","山泽损"],73:["震","坎","山火贲"],
    74:["坤","坤","山雷颐"],75:["震","兑","山风蛊"],76:["坤","震","山水蒙"],
    77:["震","坎","艮为山"],78:["坤","坤","山地剥"],
    81:["震","兑","地天泰"],82:["坤","震","地泽临"],83:["震","坎","地火明夷"],
    84:["坤","坤","地雷复"],85:["震","兑","地风升"],86:["坤","震","地水师"],
    87:["震","坎","地山谦"],88:["坤","坤","坤为地"],
}


# ═══════════════════════════════════════════
# 八卦变换 (错卦/综卦)
# ═══════════════════════════════════════════

# 八卦阴阳翻转（错卦）
_BAGUA_CUO = {"乾":"坤","坤":"乾","震":"巽","巽":"震","坎":"离","离":"坎","艮":"兑","兑":"艮"}

# 八卦倒转（综卦 — 只有这些反转后变化）
_BAGUA_ZONG = {"震":"艮","艮":"震","巽":"兑","兑":"巽"}
# 乾/坤/坎/离 综卦为自身


def get_cuo_gua(up: str, down: str) -> Tuple[str,str]:
    """错卦：所有阴阳反转"""
    return _BAGUA_CUO.get(up,up), _BAGUA_CUO.get(down,down)


def get_zong_gua(up: str, down: str) -> Tuple[str,str]:
    """综卦：卦倒转（上变下、下变上，同时内部翻转）"""
    new_up = _BAGUA_ZONG.get(down, down)
    new_down = _BAGUA_ZONG.get(up, up)
    return new_up, new_down


def get_hu_gua(up: str, down: str) -> Tuple[str,str,str]:
    """互卦：从六十四卦查找（上互/下互/卦名）"""
    up_num = {v:k for k,v in BA_GUA.items()}.get(up,1)
    down_num = {v:k for k,v in BA_GUA.items()}.get(down,1)
    key = up_num*10+down_num
    info = _GUA_HU.get(key, ["?","?","?卦"])
    return info[0], info[1], info[2]


def get_bian_gua_name(up: str, down: str) -> str:
    """查找卦名"""
    up_num = {v:k for k,v in BA_GUA.items()}.get(up,1)
    down_num = {v:k for k,v in BA_GUA.items()}.get(down,1)
    info = _GUA_HU.get(up_num*10+down_num)
    return info[2] if info else f"{up}{down}卦"


# ═══════════════════════════════════════════
# 变卦映射 (caculate.py dic_change)
# ═══════════════════════════════════════════

_DIC_CHANGE = {
    "乾":{1:"巽",2:"离",3:"兑"},"兑":{1:"坎",2:"震",3:"乾"},
    "离":{1:"艮",2:"乾",3:"震"},"震":{1:"坤",2:"兑",3:"离"},
    "巽":{1:"乾",2:"艮",3:"坎"},"坎":{1:"兑",2:"坤",3:"巽"},
    "艮":{1:"离",2:"巽",3:"坤"},"坤":{1:"震",2:"坎",3:"艮"},
}


# ═══════════════════════════════════════════
# 地支索引计算
# ═══════════════════════════════════════════

_ZHI2IDX = {"子":1,"丑":2,"寅":3,"卯":4,"辰":5,"巳":6,
            "午":7,"未":8,"申":9,"酉":10,"戌":11,"亥":12}

_HOUR2ZHI = {0:"子",1:"子",2:"丑",3:"丑",4:"寅",5:"寅",6:"卯",7:"卯",
             8:"辰",9:"辰",10:"巳",11:"巳",12:"午",13:"午",14:"未",15:"未",
             16:"申",17:"申",18:"酉",19:"酉",20:"戌",21:"戌",22:"亥",23:"亥"}


def _get_zhi_idx_from_ganzhi(ganzhi: str) -> int:
    zhi = ganzhi[1] if len(ganzhi)>=2 else ganzhi
    return _ZHI2IDX.get(zhi, 1)


# ═══════════════════════════════════════════
# 梅花易数年月日时起卦
# ═══════════════════════════════════════════

def compute_meihua(year: int, month: int, day: int, hour: int) -> Dict:
    """
    梅花易数年月日时起卦。
    优先 calendar.py 农历→fallback zhdate→fallback 简化计算。

    Returns 字典含:
    - 上卦/下卦/卦名
    - 体卦/用卦
    - 互卦 (上互/下互/互卦名)
    - 变卦 (变爻序号/变卦名)
    - 错卦/综卦
    """

    # 农历日期（优先精算 → fallback zhdate）
    lunar_year_zhi = lunar_month = lunar_day = lunar_hour_zhi = None
    try:
        from scripts.calendar import gregorian_to_lunar
        ln = gregorian_to_lunar(datetime(year,month,day))
        lunar_month = ln["month"]
        lunar_day = ln["day"]
        # 农历年地支：从年柱提取
        lunar_year_zhi = ln["year_name"][1] if ln.get("year_name") and len(ln["year_name"])>=2 else None
    except ImportError:
        pass

    if lunar_year_zhi is None or lunar_month is None:
        try:
            from zhdate import ZhDate
            lunar_dt = ZhDate.from_datetime(datetime(year,month,day))
            lunar_month = lunar_dt.lunar_month
            lunar_day = lunar_dt.lunar_day
            ch_words = lunar_dt.chinese()
            lunar_year_zhi = ch_words.split(" ")[1][1]
        except ImportError:
            # 最后 fallback：简化农历（用公历月日近似）
            lunar_month = month
            lunar_day = day
            lunar_year_zhi = "子"  # 占位

    if lunar_year_zhi is None:
        lunar_year_zhi = "子"

    # 时辰地支
    lunar_hour_zhi = _HOUR2ZHI.get(hour, "子")
    y_idx = _ZHI2IDX.get(lunar_year_zhi, 1)
    m_num = lunar_month
    d_num = lunar_day
    h_idx = _ZHI2IDX.get(lunar_hour_zhi, 1)

    # 上卦 = (年+月+日) % 8，结果 0 对应坤(8)
    up_num = (y_idx + m_num + d_num) % 8
    if up_num == 0: up_num = 8
    gua_up = BA_GUA.get(up_num, BA_GUA[1])

    # 下卦 = (年+月+日+时) % 8，结果 0 对应坤(8)
    down_num = (y_idx + m_num + d_num + h_idx) % 8
    if down_num == 0: down_num = 8
    gua_down = BA_GUA.get(down_num, BA_GUA[1])

    # 动爻 = (年+月+日+时) % 6
    change_line = (y_idx + m_num + d_num + h_idx) % 6
    if change_line == 0: change_line = 6

    # 体用（动爻≤3 用在下卦，>3 用在上卦）
    if change_line <= 3:
        gua_yong = gua_down
        gua_ti = gua_up
        # 变卦：下卦变
        gua_bian_down = _DIC_CHANGE[gua_down].get(change_line, gua_down)
        gua_bian_up = gua_up
    else:
        gua_yong = gua_up
        gua_ti = gua_down
        # 变卦：上卦变
        gua_bian_up = _DIC_CHANGE[gua_up].get(change_line-3, gua_up)
        gua_bian_down = gua_down

    # 互卦
    hu_up, hu_down, hu_name = get_hu_gua(gua_up, gua_down)

    # 错卦/综卦
    cuo_up, cuo_down = get_cuo_gua(gua_up, gua_down)
    zong_up, zong_down = get_zong_gua(gua_up, gua_down)

    # 卦名
    name = get_bian_gua_name(gua_up, gua_down)
    bian_name = get_bian_gua_name(gua_bian_up, gua_bian_down)
    cuo_name = get_bian_gua_name(cuo_up, cuo_down)
    zong_name = get_bian_gua_name(zong_up, zong_down)

    return {
        "时间":f"{year}-{month}-{day} {hour}:00",
        "农历":f"年支{lunar_year_zhi} 月{lunar_month} 日{lunar_day} 时{lunar_hour_zhi}",
        "上卦":gua_up,"下卦":gua_down,"卦名":name,
        "体卦":gua_ti,"用卦":gua_yong,
        "变爻":change_line,
        "变卦":{"上卦":gua_bian_up,"下卦":gua_bian_down,"卦名":bian_name},
        "互卦":{"上互":hu_up,"下互":hu_down,"卦名":hu_name},
        "错卦":{"上卦":cuo_up,"下卦":cuo_down,"卦名":cuo_name},
        "综卦":{"上卦":zong_up,"下卦":zong_down,"卦名":zong_name},
    }