"""
liuren.py — 大六壬排盘引擎（司天监象推演系统）
流程：起时→天地盘→四课→三传(九宗门)→旬遁→贵人→六亲→旺相
对接 calendar.py 八字节气计算。
"""

from __future__ import annotations
from datetime import datetime
from typing import Dict,List,Tuple,Optional

# ═══════════════════════════════════════════════
# 常量表（独立副本，不依赖 calendar.py）
# ═══════════════════════════════════════════════

TIAN_GAN = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
DI_ZHI  = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

GAN_WUXING   = [1,1,4,4,2,2,0,0,3,3]
ZHI_WUXING   = [3,2,1,1,2,4,4,2,0,0,2,3]
GAN_YINYANG  = [1,0,1,0,1,0,1,0,1,0]
ZHI_YINYANG  = [1,0,1,0,1,0,1,0,1,0,1,0]

JI_GONG = [2,4,5,7,5,7,8,10,11,1]

TIAN_JIANG  = ["贵人","螣蛇","朱雀","六合","勾陈","青龙","天空","白虎","太常","玄武","太阴","天后"]
YUE_JIANG   = [1,0,11,10,9,8,7,6,5,4,3,2]
ZHONG_QI    = ["冬至","大寒","雨水","春分","谷雨","小满",
               "夏至","大暑","处暑","秋分","霜降","小雪"]
LIU_QIN_NAMES = {1:"妻财",-1:"官鬼",2:"子孙",-2:"父母",0:"兄弟"}

_WANG_XIANG = {
    11:(1,4),10:(1,4),9:(1,4), 8:(4,2),7:(4,2),6:(4,2),
    5:(0,3),4:(0,3),3:(0,3), 2:(3,1),1:(3,1),0:(3,1),
}


# ═══════════════════════════════════════════════
# 生克关系
# ═══════════════════════════════════════════════

def sheng_ke(a: int, b: int) -> int:
    ke = {0:1,1:2,2:3,3:4,4:0}
    sh = {0:3,3:1,1:4,4:2,2:0}
    if ke.get(a)==b: return 1
    if ke.get(b)==a: return -1
    if sh.get(a)==b: return 2
    if sh.get(b)==a: return -2
    return 0


# ═══════════════════════════════════════════════
# 月将计算
# ═══════════════════════════════════════════════

def get_yue_jiang(dt: datetime) -> int:
    """获取月将。swisseph恒星制→fallback节气表。
    Returns: 地支索引 子=0...亥=11
    """
    try:
        import swisseph as swe
        y,m,d = dt.year,dt.month,dt.day
        h = dt.hour+dt.minute/60.0+dt.second/3600.0
        jd = swe.julday(y,m,d,h,swe.GREG_CAL)
        base_jd = swe.julday(1300,1,1,0.0,swe.GREG_CAL)
        swe.set_sid_mode(swe.SIDM_FAGAN_BRADLEY,0,0)
        ayan = (swe.get_ayanamsa_ut(jd)-swe.get_ayanamsa_ut(base_jd)+4.0)
        sun_trop = swe.calc_ut(jd,swe.SUN,swe.FLG_SWIEPH)[0][0]%360.0
        sun_sid = (sun_trop-ayan)%360.0
        palace = int(sun_sid/30.0)%12
        return [10,9,8,7,6,5,4,3,2,1,0,11][palace]
    except ImportError:
        pass

    # Fallback: 中气→月将
    try:
        from scripts.calendar import find_jieqi_in_year
    except ImportError:
        from calendar import find_jieqi_in_year

    all_jq = {}
    for y in [dt.year-1,dt.year,dt.year+1]:
        for n,t in find_jieqi_in_year(y).items():
            if n in ZHONG_QI: all_jq[n]=t
    sorted_jq = sorted(all_jq.items(),key=lambda x:x[1])
    prev = None
    for n,t in sorted_jq:
        if t <= dt: prev = n
    if prev and prev in ZHONG_QI:
        return YUE_JIANG[ZHONG_QI.index(prev)]
    return 0


# ═══════════════════════════════════════════════
# 天地盘 + 四课
# ═══════════════════════════════════════════════

def tian_di_pan(shi_zhi: int, yue_jiang: int) -> List[int]:
    first = yue_jiang-shi_zhi if shi_zhi<=yue_jiang else yue_jiang+12-shi_zhi
    return [(first+i)%12 for i in range(12)]


def si_ke(ri_gan: int, ri_zhi: int, tp: List[int]) -> List[int]:
    gong = JI_GONG[ri_gan]
    k1sh = tp[gong]; k2sh = tp[k1sh]
    k3sh = tp[ri_zhi]; k4sh = tp[k3sh]
    return [ri_gan,k1sh,k1sh,k2sh,ri_zhi,k3sh,k3sh,k4sh]


# ═══════════════════════════════════════════════
# 九宗门 — 三传
# ═══════════════════════════════════════════════

def _try_zei_ke(sk,tp,zei,ke) -> Optional[Tuple[List[int],str]]:
    if len(zei)==1:
        chu = sk[zei[0]*2+1]
        nm = "重审" if ZHI_YINYANG[sk[zei[0]*2+2]]==0 else "始入"
        return ([chu,tp[chu],tp[tp[chu]]],nm)
    if len(ke)==1 and len(zei)==0:
        chu = sk[ke[0]*2+1]
        return ([chu,tp[chu],tp[tp[chu]]],"元首")
    return None


def _try_bi_yong(sk,tp,zei,ke,rg) -> Optional[Tuple[List[int],str]]:
    zk = zei if len(zei)>=2 else ke
    bi = [sk[i*2+1] for i in zk if ZHI_YINYANG[sk[i*2+1]]==GAN_YINYANG[rg]]
    if len(bi)==1:
        chu = bi[0]
        return ([chu,tp[chu],tp[tp[chu]]],"比用")
    return None


def _try_she_hai(sk,tp,zei,ke,rg) -> Optional[Tuple[List[int],str]]:
    zk = zei if len(zei)>=2 else ke
    if not zk: return None
    scores = [(sk[i*2+1]-rg)%12 for i in zk]
    chu = sk[zk[scores.index(max(scores))]*2+1]
    return ([chu,tp[chu],tp[tp[chu]]],"涉害")


def _try_mao_xing(sk,tp,rg,rz) -> Optional[Tuple[List[int],str]]:
    chu = sk[5] if GAN_YINYANG[rg]==1 else sk[3]
    return ([chu,tp[chu],tp[tp[chu]]],"昴星")


def _try_fu_yin(sk,tp,rg) -> Tuple[List[int],str]:
    chu = tp[rg] if GAN_YINYANG[rg]==1 else tp[rg-10 if rg>=10 else 0]
    return ([chu,tp[chu],tp[tp[chu]]],"伏吟")


def _try_fan_yin(sk,tp,rg) -> Tuple[List[int],str]:
    return ([tp[rg],tp[tp[rg]],tp[tp[tp[rg]]]],"反吟")


def get_san_chuan(sk: List[int], tp: List[int], rg: int, rz: int) -> Tuple[List[int],str]:
    wx = [GAN_WUXING[sk[0]]]+[ZHI_WUXING[v] for v in sk[1:]]
    sr = [sheng_ke(wx[i],wx[i+1]) for i in range(0,len(wx),2)]
    zei = [i for i,v in enumerate(sr) if v==1]
    ke  = [i for i,v in enumerate(sr) if v==-1]

    # 贼克
    r = _try_zei_ke(sk,tp,zei,ke)
    if r: return r
    # 比用
    if len(zei)>1 or len(ke)>1:
        r = _try_bi_yong(sk,tp,zei,ke,rg)
        if r: return r
    # 涉害
    if len(zei)>=2 or len(ke)>=2:
        r = _try_she_hai(sk,tp,zei,ke,rg)
        if r: return r
    # 昴星
    if len(zei)==0 and len(ke)==0:
        r = _try_mao_xing(sk,tp,rg,rz)
        if r: return r
    # 伏吟/反吟
    if tp[0]==0: return _try_fu_yin(sk,tp,rg)
    if tp[1]==0: return _try_fan_yin(sk,tp,rg)

    chu = sk[1]
    return ([chu,tp[chu],tp[tp[chu]]],"通用")


# ═══════════════════════════════════════════════
# 旬遁
# ═══════════════════════════════════════════════

def xun_dun(rg: int, rz: int, tp: List[int], sc: List[int]) -> Tuple[List[int],List[int]]:
    first_zhi = (rz-rg)%12
    dun_first = (tp[0]+first_zhi)%12
    dg = [(dun_first+i)%10 for i in range(12)]
    sd = []
    for s in sc:
        for i,t in enumerate(tp):
            if t==s: sd.append(dg[i]); break
        else: sd.append(0)
    return dg,sd


# ═══════════════════════════════════════════════
# 贵人 + 六亲 + 旺相
# ═══════════════════════════════════════════════

def qi_gui_ren(rg: int, sz: int, tp: List[int]) -> List[int]:
    is_day = 3 <= sz <= 8
    gr_map = {0:(1,7),4:(1,7),6:(1,7),1:(0,8),5:(0,8),
              2:(11,9),3:(11,9),8:(5,3),9:(5,3),7:(6,2)}
    gr_zhi = gr_map.get(rg,(1,7))[0 if is_day else 1]
    gr_idx = tp.index(gr_zhi) if gr_zhi in tp else 0
    shun = not (5 <= gr_idx <= 10)
    jiang = [(gr_idx+(i if shun else -i))%12 for i in range(12)]
    return jiang


def get_liu_qin(ri_wx: int, sc: List[int]) -> List[str]:
    return [LIU_QIN_NAMES.get(sheng_ke(ri_wx,ZHI_WUXING[s]),"?") for s in sc]


def get_wang_xiang(yj: int) -> List[int]:
    wx = _WANG_XIANG.get(yj,(1,4))
    w,x = wx[0],wx[1]
    sh = {0:3,3:1,1:4,4:2,2:0}
    ke = {0:1,1:2,2:3,3:4,4:0}
    return [w,x,sh[w],sh[x],ke[w]]


# ═══════════════════════════════════════════════
# 统一入口
# ═══════════════════════════════════════════════

def compute_liuren(dt: datetime, lon: float=116.0, lat: float=40.0) -> Dict:
    """完整大六壬排盘。Returns dict 含四柱/月将/天地盘/四课/三传/遁干/天将/六亲/旺相/课名"""

    # 四柱
    try:
        from scripts.calendar import calculate_bazi
    except ImportError:
        from calendar import calculate_bazi
    bazi = calculate_bazi(dt,lon,lat)

    rg = TIAN_GAN.index(bazi["day"][0])
    rz = DI_ZHI.index(bazi["day"][1])
    sz = DI_ZHI.index(bazi["time"][1])

    yj = get_yue_jiang(dt)
    tp = tian_di_pan(sz,yj)
    sk = si_ke(rg,rz,tp)
    sc,kn = get_san_chuan(sk,tp,rg,rz)
    dg,sd = xun_dun(rg,rz,tp,sc)
    tj = qi_gui_ren(rg,sz,tp)
    lq = get_liu_qin(GAN_WUXING[rg],sc)
    wx = get_wang_xiang(yj)

    def zs(i): return DI_ZHI[i] if 0<=i<12 else "?"
    def gs(i): return TIAN_GAN[i] if 0<=i<10 else "?"

    return {
        "四柱": bazi,
        "月将": zs(yj),
        "天地盘": {"地盘":[zs(i) for i in range(12)],"天盘":[zs(i) for i in tp]},
        "四课": [gs(sk[0])]+[zs(i) for i in sk[1:]],
        "四课生克": [sheng_ke(GAN_WUXING[sk[0]],ZHI_WUXING[sk[1]]),
                     sheng_ke(ZHI_WUXING[sk[2]],ZHI_WUXING[sk[3]]),
                     sheng_ke(ZHI_WUXING[sk[4]],ZHI_WUXING[sk[5]]),
                     sheng_ke(ZHI_WUXING[sk[6]],ZHI_WUXING[sk[7]])],
        "三传": [zs(i) for i in sc],
        "三传遁干": [gs(i) for i in sd],
        "遁干": [gs(i) for i in dg],
        "天将": [TIAN_JIANG[i] for i in tj],
        "六亲": lq,
        "旺相": wx,
        "课名": kn,
    }