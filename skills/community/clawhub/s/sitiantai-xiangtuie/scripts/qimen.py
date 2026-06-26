"""
qimen.py — 奇门遁甲排盘引擎（司天监象推演系统）
合并：models.py + ju.py + pan.py + state.py
干支计算对接 calendar.py 精算。
"""

from dataclasses import dataclass,field
from datetime import datetime,timedelta
from enum import Enum
from typing import Dict,List,Tuple,Optional
import math

# ═══════════════════════════════════════════
# 常量与枚举 (models)
# ═══════════════════════════════════════════

class DunType(str,Enum): YANG="阳遁"; YIN="阴遁"

TIAN_GAN = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
DI_ZHI  = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
SAN_QI  = ["乙","丙","丁"]
YI_QI_SEQUENCE = ["戊","己","庚","辛","壬","癸","丁","丙","乙"]

JIU_XING = ["天蓬","天任","天冲","天辅","天英","天芮","天柱","天心","天禽"]
BA_MEN   = ["休门","生门","伤门","杜门","景门","死门","惊门","开门"]
BA_SHEN  = ["值符","螣蛇","太阴","六合","白虎","玄武","九地","九天"]

GONG_NUMBER = {1:"坎宫",2:"坤宫",3:"震宫",4:"巽宫",5:"中宫",6:"乾宫",7:"兑宫",8:"艮宫",9:"离宫"}
GONG_DIRECTION = {1:"北",2:"西南",3:"东",4:"东南",5:"中",6:"西北",7:"西",8:"东北",9:"南"}

XING_NUMBER = {"天蓬":1,"天芮":2,"天冲":3,"天辅":4,"天禽":5,"天心":6,"天柱":7,"天任":8,"天英":9}
NUMBER_XING = {v:k for k,v in XING_NUMBER.items()}

MEN_NUMBER  = {"休门":1,"死门":2,"伤门":3,"杜门":4,"开门":6,"惊门":7,"生门":8,"景门":9}
NUMBER_MEN  = {v:k for k,v in MEN_NUMBER.items()}

XING_ATTR = {
    "天蓬":{"五行":"水","吉凶":"凶"},"天任":{"五行":"土","吉凶":"吉"},
    "天冲":{"五行":"木","吉凶":"吉"},"天辅":{"五行":"木","吉凶":"吉"},
    "天英":{"五行":"火","吉凶":"中"},"天芮":{"五行":"土","吉凶":"凶"},
    "天柱":{"五行":"金","吉凶":"凶"},"天心":{"五行":"金","吉凶":"吉"},
    "天禽":{"五行":"土","吉凶":"吉"},
}
MEN_ATTR = {
    "休门":{"吉凶":"吉","五行":"水"},"生门":{"吉凶":"大吉","五行":"土"},
    "伤门":{"吉凶":"凶","五行":"木"},"杜门":{"吉凶":"凶","五行":"木"},
    "景门":{"吉凶":"中","五行":"火"},"死门":{"吉凶":"大凶","五行":"土"},
    "惊门":{"吉凶":"凶","五行":"金"},"开门":{"吉凶":"吉","五行":"金"},
}
SHEN_ATTR = {
    "值符":{"吉凶":"吉","五行":"土"},"螣蛇":{"吉凶":"凶","五行":"火"},
    "太阴":{"吉凶":"吉","五行":"金"},"六合":{"吉凶":"吉","五行":"木"},
    "白虎":{"吉凶":"凶","五行":"金"},"玄武":{"吉凶":"凶","五行":"水"},
    "九地":{"吉凶":"吉","五行":"土"},"九天":{"吉凶":"吉","五行":"金"},
}

YANG_DUN_JU = {
    "冬至":[1,7,4],"小寒":[2,8,5],"大寒":[3,9,6],"立春":[8,5,2],
    "雨水":[9,6,3],"惊蛰":[1,7,4],"春分":[3,9,6],"清明":[4,1,7],
    "谷雨":[5,2,8],"立夏":[4,1,7],"小满":[5,2,8],"芒种":[6,3,9],
}
YIN_DUN_JU = {
    "夏至":[9,3,6],"小暑":[8,2,5],"大暑":[7,1,4],"立秋":[2,5,8],
    "处暑":[1,4,7],"白露":[9,3,6],"秋分":[7,1,4],"寒露":[6,9,3],
    "霜降":[5,8,2],"立冬":[6,9,3],"小雪":[5,8,2],"大雪":[4,7,1],
}

JIAZI_CYCLE = [TIAN_GAN[i%10]+DI_ZHI[i%12] for i in range(60)]

XUN_SHOU = {"甲子":"戊","甲戌":"己","甲申":"庚","甲午":"辛","甲辰":"壬","甲寅":"癸"}
XUN_KONG_MAP = {"甲子":("戌","亥"),"甲戌":("申","酉"),"甲申":("午","未"),
                "甲午":("辰","巳"),"甲辰":("寅","卯"),"甲寅":("子","丑")}

SHICHEN_HOURS = {"子":(23,1),"丑":(1,3),"寅":(3,5),"卯":(5,7),"辰":(7,9),
                 "巳":(9,11),"午":(11,13),"未":(13,15),"申":(15,17),"酉":(17,19),
                 "戌":(19,21),"亥":(21,23)}

JIEQI_HUANGJING = {
    "小寒":285,"大寒":300,"立春":315,"雨水":330,"惊蛰":345,"春分":0,
    "清明":15,"谷雨":30,"立夏":45,"小满":60,"芒种":75,"夏至":90,
    "小暑":105,"大暑":120,"立秋":135,"处暑":150,"白露":165,"秋分":180,
    "寒露":195,"霜降":210,"立冬":225,"小雪":240,"大雪":255,"冬至":270,
}

YANG_DUN_JIEQI = ["冬至","小寒","大寒","立春","雨水","惊蛰","春分","清明","谷雨","立夏","小满","芒种"]
YIN_DUN_JIEQI  = ["夏至","小暑","大暑","立秋","处暑","白露","秋分","寒露","霜降","立冬","小雪","大雪"]


def hour_to_shichen(h: int) -> str:
    if h==23 or h==0: return "子"
    for z,(s,e) in SHICHEN_HOURS.items():
        if z=="子": continue
        if s<=h<e: return z
    return "子"


# ═══════════════════════════════════════════
# 节气计算 (简化，来自 ju.py)
# ═══════════════════════════════════════════

def _jd(dt: datetime) -> float:
    a = (14-dt.month)//12; y = dt.year+4800-a; m = dt.month+12*a-3
    jdn = dt.day+(153*m+2)//5+365*y+y//4-y//100+y//400-32045
    frac = (dt.hour-12)/24+dt.minute/1440+dt.second/86400
    return jdn+frac


def _solar_longitude(jd: float) -> float:
    n = jd-2451545.0
    L = (280.46646+36000.76983*(n/36525))%360
    g = math.radians((357.52911+35999.05029*(n/36525))%360)
    C = (1.914602-0.004817*(n/36525)-0.000014*(n/36525)**2)*math.sin(g)
    C += 0.019993*math.sin(2*g)+0.000289*math.sin(3*g)
    return (L+C)%360


def _find_jieqi_before_fast(dt: datetime) -> Tuple[str,datetime]:
    JIEQI_APPROX = [
        ("小寒",1,6),("大寒",1,20),("立春",2,4),("雨水",2,19),
        ("惊蛰",3,6),("春分",3,21),("清明",4,5),("谷雨",4,20),
        ("立夏",5,6),("小满",5,21),("芒种",6,6),("夏至",6,21),
        ("小暑",7,7),("大暑",7,23),("立秋",8,7),("处暑",8,23),
        ("白露",9,8),("秋分",9,23),("寒露",10,8),("霜降",10,23),
        ("立冬",11,7),("小雪",11,22),("大雪",12,7),("冬至",12,22),
    ]
    cand = []
    for n,m,d in JIEQI_APPROX:
        for yo in [-1,0,1]:
            try:
                t = datetime(dt.year+yo,m,d,0,0,0)
                if t <= dt: cand.append((n,t))
            except ValueError: pass
    if not cand: return "冬至",dt-timedelta(days=10)
    cand.sort(key=lambda x: dt-x[1])
    return cand[0]


# ═══════════════════════════════════════════
# 局数计算 (ju.py — 适配 calendar.bazi)
# ═══════════════════════════════════════════

def _calc_ganzhi_from_bazi(dt: datetime) -> Tuple[str,str,str,str]:
    """用精算 bazi 获取四柱（替换原 ju.py 的简化版）"""
    try:
        from scripts.calendar import calculate_bazi
    except ImportError:
        from calendar import calculate_bazi
    bz = calculate_bazi(dt)
    return bz["year"],bz["month"],bz["day"],bz["time"]


def _calc_xun_shou_kong(ri_zhu: str) -> Tuple[str,Tuple[str,str]]:
    if ri_zhu not in JIAZI_CYCLE: return "戊",("戌","亥")
    idx = JIAZI_CYCLE.index(ri_zhu)
    xs = JIAZI_CYCLE[(idx//10)*10]
    return XUN_SHOU.get(xs,"戊"),XUN_KONG_MAP.get(xs,("戌","亥"))


def _calc_yuan(dt: datetime, jieqi_dt: datetime) -> int:
    delta = (dt.date()-jieqi_dt.date()).days
    if delta<5: return 0
    elif delta<10: return 1
    else: return 2


def _calc_ju(dt: datetime) -> Tuple[DunType,int,str,str]:
    jn,jdt = _find_jieqi_before_fast(dt)
    if jn in YANG_DUN_JIEQI:
        dtype,ju_table = DunType.YANG,YANG_DUN_JU
    else:
        dtype,ju_table = DunType.YIN,YIN_DUN_JU
    yi = _calc_yuan(dt,jdt)
    yuan = ["上元","中元","下元"][yi]
    ju = ju_table.get(jn,[1,7,4])[yi]
    return dtype,ju,yuan,jn


# ═══════════════════════════════════════════
# 排盘引擎 (pan.py — 洛书旋转)
# ═══════════════════════════════════════════

YANG_PATH = [1,2,3,4,6,7,8,9]
YIN_PATH  = [9,8,7,6,4,3,2,1]


def _rotate(gong: int, steps: int, dun: DunType) -> int:
    seq = YANG_PATH if dun==DunType.YANG else YIN_PATH
    if gong not in seq: return gong
    return seq[(seq.index(gong)+steps)%len(seq)]


def _build_di_pan(ju: int, dun: DunType) -> Dict[int,str]:
    path = YANG_PATH if dun==DunType.YANG else YIN_PATH
    dp = {}
    if ju==5:
        for i,g in enumerate(path): dp[g] = YI_QI_SEQUENCE[(i+1)%9]
        dp[5] = "戊"
    else:
        si = path.index(ju) if ju in path else 0
        for i,g in enumerate(path): dp[g] = YI_QI_SEQUENCE[(i-si)%9]
        dp[5] = "戊"
    return dp


def _build_tian_pan(sg: str, dp: Dict[int,str], dun: DunType) -> Tuple[Dict[int,str],int]:
    zfg = next((g for g,p in dp.items() if p==sg),9)
    wug = next((g for g,p in dp.items() if p=="戊"),1)
    path = YANG_PATH if dun==DunType.YANG else YIN_PATH
    steps = (path.index(zfg)-path.index(wug))%8 if wug in path and zfg in path else 0
    tp = {}
    for g,gan in dp.items():
        if g==5: tp[5]=gan
        else: tp[_rotate(g,steps,dun)] = gan
    for g in range(1,10):
        if g not in tp: tp[g]="？"
    return tp,zfg


def _build_jiu_xing(ju: int, dun: DunType, zfg: int) -> Dict[int,str]:
    XING_BY_NUM = {1:"天蓬",2:"天芮",3:"天冲",4:"天辅",6:"天心",7:"天柱",8:"天任",9:"天英"}
    path = YANG_PATH if dun==DunType.YANG else YIN_PATH
    steps = 0
    if ju!=5 and zfg!=5 and ju in path and zfg in path:
        steps = (path.index(zfg)-path.index(ju))%8
    jx = {}
    for num,xing in XING_BY_NUM.items():
        if num in path: jx[path[(path.index(num)+steps)%8]] = xing
    jx[5] = "天禽"
    return jx


def _build_ba_men(ju: int, dun: DunType, zfg: int) -> Dict[int,str]:
    MEN_BY_NUM = {1:"休门",2:"死门",3:"伤门",4:"杜门",6:"开门",7:"惊门",8:"生门",9:"景门"}
    path = YANG_PATH if dun==DunType.YANG else YIN_PATH
    steps = 0
    if ju!=5 and zfg!=5 and ju in path and zfg in path:
        steps = (path.index(zfg)-path.index(ju))%8
    bm = {}
    for num,men in MEN_BY_NUM.items():
        if num in path: bm[path[(path.index(num)+steps)%8]] = men
    return bm


def _build_ba_shen(zfg: int, dun: DunType) -> Dict[int,str]:
    path = YANG_PATH if dun==DunType.YANG else YIN_PATH
    SHEN = ["值符","螣蛇","太阴","六合","白虎","玄武","九地","九天"]
    si = path.index(zfg) if zfg in path else 0
    bs = {}
    for i,g in enumerate(path): bs[g] = SHEN[(i-si)%8]
    return bs


# ═══════════════════════════════════════════
# QimenState (state.py)
# ═══════════════════════════════════════════

@dataclass
class QimenState:
    dt: datetime = field(default_factory=datetime.now)
    nian_zhu: str = ""; yue_zhu: str = ""; ri_zhu: str = ""; shi_zhu: str = ""
    jieqi: str = ""; dun_type: DunType = DunType.YANG; ju_shu: int = 1; yuan: str = "上元"
    zhi_fu_gong: int = 9; zhi_shi_gong: int = 9
    tian_pan: Dict[int,str] = field(default_factory=dict)
    di_pan: Dict[int,str] = field(default_factory=dict)
    jiu_xing: Dict[int,str] = field(default_factory=dict)
    ba_men: Dict[int,str] = field(default_factory=dict)
    ba_shen: Dict[int,str] = field(default_factory=dict)
    xun_kong: tuple = ("","")
    shi_gan: str = ""; ri_gan: str = ""

    def get_gong_info(self, gong: int) -> dict:
        x = self.jiu_xing.get(gong,""); m = self.ba_men.get(gong,""); s = self.ba_shen.get(gong,"")
        return {
            "宫位":GONG_NUMBER.get(gong,""),"方位":GONG_DIRECTION.get(gong,""),
            "天盘干":self.tian_pan.get(gong,""),"地盘干":self.di_pan.get(gong,""),
            "九星":x,"八门":m,"八神":s,
            "星吉凶":XING_ATTR.get(x,{}).get("吉凶","") if x else "",
            "门吉凶":MEN_ATTR.get(m,{}).get("吉凶","") if m in MEN_ATTR else "",
            "神吉凶":SHEN_ATTR.get(s,{}).get("吉凶","") if s in SHEN_ATTR else "",
        }

    def summary(self) -> str:
        return (f"{self.dun_type.value}第{self.ju_shu}局（{self.jieqi}·{self.yuan}）"
                f" | {self.dt.strftime('%Y-%m-%d %H:%M')}"
                f" | {self.nian_zhu}年 {self.yue_zhu}月 {self.ri_zhu}日 {self.shi_zhu}时")

    def to_dict(self) -> dict:
        return {
            "时间":self.dt.isoformat(),"年柱":self.nian_zhu,"月柱":self.yue_zhu,
            "日柱":self.ri_zhu,"时柱":self.shi_zhu,"节气":self.jieqi,
            "遁类型":self.dun_type.value,"局数":self.ju_shu,"元":self.yuan,
            "旬空":list(self.xun_kong),"值符宫":self.zhi_fu_gong,"值使宫":self.zhi_shi_gong,
            "天盘":{str(k):v for k,v in self.tian_pan.items()},
            "地盘":{str(k):v for k,v in self.di_pan.items()},
            "九星":{str(k):v for k,v in self.jiu_xing.items()},
            "八门":{str(k):v for k,v in self.ba_men.items()},
            "八神":{str(k):v for k,v in self.ba_shen.items()},
        }


# ═══════════════════════════════════════════
# 统一入口
# ═══════════════════════════════════════════

def compute_qimen(dt: datetime) -> QimenState:
    """完整奇门排盘。自动计算局数→地盘→天盘→九星→八门→八神"""
    nz,yz,rz,sz = _calc_ganzhi_from_bazi(dt)
    dun,ju,yuan,jq = _calc_ju(dt)
    xg,xk = _calc_xun_shou_kong(rz)
    sg,rg = sz[0],rz[0]

    dp = _build_di_pan(ju,dun)
    tp,zfg = _build_tian_pan(sg,dp,dun)
    jx = _build_jiu_xing(ju,dun,zfg)
    bm = _build_ba_men(ju,dun,zfg)
    bs = _build_ba_shen(zfg,dun)

    return QimenState(dt=dt,nian_zhu=nz,yue_zhu=yz,ri_zhu=rz,shi_zhu=sz,
                      jieqi=jq,dun_type=dun,ju_shu=ju,yuan=yuan,
                      zhi_fu_gong=zfg,zhi_shi_gong=zfg,
                      tian_pan=tp,di_pan=dp,jiu_xing=jx,ba_men=bm,ba_shen=bs,
                      xun_kong=xk,shi_gan=sg,ri_gan=rg)