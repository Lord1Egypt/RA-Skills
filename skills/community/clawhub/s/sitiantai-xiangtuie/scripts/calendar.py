"""
calendar.py — 历法计算模块（司天监象推演系统）
统一：历法转换 / 八字四柱 / 节气精算 / 旬空

源：calendar/lunar.py + calendar/bazi/pillars.py
依赖：swisseph, lunar_python
"""

from __future__ import annotations
from datetime import datetime,date,timedelta
from typing import Dict,Tuple

import swisseph as swe
from lunar_python import Solar,Lunar

# ═══════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════

TIAN_GAN = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
DI_ZHI  = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

GAN_WUXING = [1,1,4,4,2,2,0,0,3,3]
ZHI_WUXING = [3,2,1,1,2,4,4,2,0,0,2,3]

HOUR_TO_ZHI = [
    "子","丑","丑","寅","寅","卯","卯","辰","辰",
    "巳","巳","午","午","未","未","申","申","酉","酉",
    "戌","戌","亥","亥","子",
]

WU_HU_DUN = {"甲":"丙","己":"丙","乙":"戊","庚":"戊","丙":"庚","辛":"庚","丁":"壬","壬":"壬","戊":"甲","癸":"甲"}
WU_SHU_DUN = {"甲":"甲","己":"甲","乙":"丙","庚":"丙","丙":"戊","辛":"戊","丁":"庚","壬":"庚","戊":"壬","癸":"壬"}

JIE_QI_NAMES = [
    "立春","雨水","惊蛰","春分","清明","谷雨",
    "立夏","小满","芒种","夏至","小暑","大暑",
    "立秋","处暑","白露","秋分","寒露","霜降",
    "立冬","小雪","大雪","冬至","小寒","大寒",
]

JIE_QI_TO_MONTH_ZHI = {
    "立春":"寅","雨水":"寅","惊蛰":"卯","春分":"卯","清明":"辰","谷雨":"辰",
    "立夏":"巳","小满":"巳","芒种":"午","夏至":"午","小暑":"未","大暑":"未",
    "立秋":"申","处暑":"申","白露":"酉","秋分":"酉","寒露":"戌","霜降":"戌",
    "立冬":"亥","小雪":"亥","大雪":"子","冬至":"子","小寒":"丑","大寒":"丑",
}

XUN_KONG_MAP = {
    "甲子":("戌","亥"),"甲戌":("申","酉"),"甲申":("午","未"),
    "甲午":("辰","巳"),"甲辰":("寅","卯"),"甲寅":("子","丑"),
}

JIAZI_CYCLE = [TIAN_GAN[i%10]+DI_ZHI[i%12] for i in range(60)]


def shichen_from_hour(hour: int) -> str:
    return HOUR_TO_ZHI[hour]


# ═══════════════════════════════════════════
# 节气精算 (swisseph 二分法)
# ═══════════════════════════════════════════

def _julday(dt: datetime) -> float:
    return swe.julday(dt.year,dt.month,dt.day,
                      dt.hour+dt.minute/60.0+dt.second/3600.0)


def _sun_lon(jd: float) -> float:
    return swe.calc_ut(jd,swe.SUN,swe.FLG_SWIEPH)[0][0]%360.0


def _find_term(jd0: float,target: float,maxdays: float=40.0) -> float:
    jd = jd0
    prev = (_sun_lon(jd)-target)%360.0
    while jd < jd0+maxdays:
        jd += 1.0
        cur = (_sun_lon(jd)-target)%360.0
        if prev >= 180 and cur < 180: break
        prev = cur
    lo,hi = jd-1.0,jd
    for _ in range(60):
        mid = (lo+hi)/2.0
        if (_sun_lon(mid)-target)%360.0 < 180: hi = mid
        else: lo = mid
        if abs(hi-lo) < 1e-10: break
    return (lo+hi)/2.0


def find_jieqi_in_year(year: int) -> Dict[str,datetime]:
    terms = [(i*15+315)%360 for i in range(24)]
    approx = [
        (2,4),(2,19),(3,6),(3,21),(4,5),(4,20),(5,6),(5,21),
        (6,6),(6,21),(7,7),(7,23),(8,7),(8,23),(9,8),(9,23),
        (10,8),(10,23),(11,7),(11,22),(12,7),(12,22),(1,6),(1,20),
    ]
    out = {}
    for lon,(m,d) in zip(terms,approx):
        jd0 = swe.julday(year,m,max(1,d-15),0.0)
        jdt = _find_term(jd0,lon,40.0)
        y,m2,d2,h = swe.revjul(jdt)
        hi = int(h); mi = int((h-hi)*60); si = int(((h-hi)*60-mi)*60)
        out[JIE_QI_NAMES[len(out)]] = datetime(int(y),int(m2),int(d2),hi,mi,si)
    return out


def get_jieqi_before(dt: datetime) -> Tuple[str,datetime]:
    all_jq = []
    for y in [dt.year-1,dt.year,dt.year+1]:
        for n,t in find_jieqi_in_year(y).items():
            all_jq.append((t,n))
    best_n,best_t = None,None
    for t,n in all_jq:
        if t <= dt and (best_t is None or t > best_t):
            best_t,best_n = t,n
    return best_n,best_t


# ═══════════════════════════════════════════
# 八字四柱
# ═══════════════════════════════════════════

def calculate_bazi(dt: datetime, lon: float=116.0, lat: float=40.0) -> Dict[str,str]:
    tz = round(lon/15.0)
    ut = dt - timedelta(hours=tz)

    # 年柱
    yr = dt.year
    lc = find_jieqi_in_year(yr).get("立春")
    if lc and ut < lc: yr -= 1
    year = TIAN_GAN[(yr-4)%10]+DI_ZHI[(yr-4)%12]

    # 月柱
    jqn,_ = get_jieqi_before(ut)
    mz = JIE_QI_TO_MONTH_ZHI.get(jqn,"寅")
    fm = WU_HU_DUN.get(year[0],"丙")
    off = (DI_ZHI.index(mz)-DI_ZHI.index("寅"))%12
    month = TIAN_GAN[(TIAN_GAN.index(fm)+off)%10]+mz

    # 日柱 — 2026-04-23 丁卯 基准
    jd = swe.julday(dt.year,dt.month,dt.day,0.0)
    ref = swe.julday(2026,4,23,0.0)
    ref_idx = 3
    days = round(jd-ref)
    di = (ref_idx+days)%60
    if di < 0: di += 60
    day = TIAN_GAN[di%10]+DI_ZHI[di%12]

    # 时柱
    h = dt.hour
    if h == 23:
        nd = dt+timedelta(days=1)
        ndi = (ref_idx+round(swe.julday(nd.year,nd.month,nd.day,0.0)-ref))%60
        if ndi < 0: ndi += 60
        dg = TIAN_GAN[ndi%10]
    else:
        dg = day[0]
    tzhi = HOUR_TO_ZHI[h]
    fh = WU_SHU_DUN.get(dg,"甲")
    off2 = (DI_ZHI.index(tzhi)-DI_ZHI.index("子"))%12
    time = TIAN_GAN[(TIAN_GAN.index(fh)+off2)%10]+tzhi

    return {"year":year,"month":month,"day":day,"time":time}


# ═══════════════════════════════════════════
# 公历→农历
# ═══════════════════════════════════════════

def gregorian_to_lunar(dt: datetime) -> dict:
    s = Solar.fromYmd(dt.year,dt.month,dt.day)
    l = s.getLunar()
    rm = l.getMonth(); ileap = rm<0; lm = abs(rm)
    try: mg = l.getMonthInGanZhi()
    except: mg = ""
    try: dg = l.getDayInGanZhi()
    except: dg = ""
    return {
        "year":l.getYear(),"year_name":l.getYearInGanZhi(),
        "month":lm,"month_name":l.getMonthInChinese(),
        "day":l.getDay(),
        "day_name":l.getDayInChinese() if hasattr(l,"getDayInChinese") else str(l.getDay()),
        "is_leap_month":ileap,"leap_month":lm if ileap else 0,
        "zodiac":l.getYearShengXiao(),
        "month_ganzhi":mg,"day_ganzhi":dg,
    }


def get_today_lunar() -> dict:
    return gregorian_to_lunar(datetime.now())


# ═══════════════════════════════════════════
# 旬空
# ═══════════════════════════════════════════

def get_xunkong(day_stem: str, day_branch: str) -> Tuple[str,str]:
    gz = day_stem+day_branch
    if gz not in JIAZI_CYCLE: return ("戌","亥")
    idx = JIAZI_CYCLE.index(gz)
    return XUN_KONG_MAP.get(JIAZI_CYCLE[(idx//10)*10],("戌","亥"))


def get_xun_shou(day_stem: str, day_branch: str) -> str:
    gz = day_stem+day_branch
    if gz not in JIAZI_CYCLE: return "戊"
    idx = JIAZI_CYCLE.index(gz)
    return JIAZI_CYCLE[(idx//10)*10][0]