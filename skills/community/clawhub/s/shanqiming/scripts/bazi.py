# -*- coding: utf-8 -*-
"""精确八字(四柱)计算 —— 基于儒略日(JDN)，适用于 1900-2100 年。
验证锚点: 1949-10-01 = 甲子日 (seq=0)。
用法:
  python bazi.py 2004 9 18
  python bazi.py 1977 8 3 6      # 最后一参数为小时(0-23)，给则算时柱
"""
import sys
from datetime import date

GAN = "甲乙丙丁戊己庚辛壬癸"
ZHI = "子丑寅卯辰巳午未申酉戌亥"

# 寿星公式 C 值表 (节气的"日"基准)，按世纪区分
C_20 = [6.11,20.84,4.6295,19.4599,6.3826,21.4155,5.59,20.888,6.318,21.86,
        6.5,22.2,7.928,23.65,8.35,23.95,8.44,23.822,9.098,24.218,8.218,23.08,7.9,22.6]
C_21 = [5.4055,20.12,3.87,18.73,5.63,20.646,4.81,20.1,5.52,21.04,
        5.678,21.37,7.108,22.83,7.5,23.13,7.646,23.042,8.318,23.438,7.438,22.36,7.18,21.94]

def solar_term_day(year, n):
    """第 n 个节气(0=小寒 ... 23=冬至)在 year 年的"日"(1-31)。精度±1天，近边界请人工复核。"""
    C = C_21 if year >= 2000 else C_20
    Y = year % 100
    D = int(Y * 0.2422 + C[n]) - int(Y / 4)
    return D

def jdn(y, m, d):
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - yy // 100 + yy // 400 - 32045

def day_ganzhi(y, m, d):
    seq = (jdn(y, m, d) + 49) % 60   # 0=甲子
    return GAN[seq % 10], ZHI[seq % 12], seq

# 节气索引 -> 月支(地支字符)
TERM_ZHI = {0:"丑", 2:"寅", 4:"卯", 6:"辰", 8:"巳", 10:"午", 12:"未",
            14:"申", 16:"酉", 18:"戌", 20:"亥", 22:"子"}

def month_zhi(y, m, d):
    """依据节气边界确定月支。"""
    bounds = []  # (date, zhi)
    for n, mon in [(0,1),(2,2),(4,3),(6,4),(8,5),(10,6),(12,7),(14,8),(16,9),(18,10),(20,11),(22,12)]:
        bounds.append((date(y, mon, solar_term_day(y, n)), TERM_ZHI[n]))
    # 下一年小寒 (丑月起点，处理12月之后)
    bounds.append((date(y+1, 1, solar_term_day(y+1, 0)), "丑"))
    cur = date(y, m, d)
    chosen = "丑"
    for bd, zhi in bounds:
        if bd <= cur:
            chosen = zhi
    return chosen

# 五虎遁: 年干 -> 寅月天干index
WUHU_BASE = {"甲":2,"己":2,"乙":4,"庚":4,"丙":6,"辛":6,"丁":8,"壬":8,"戊":0,"癸":0}
# 十二月支顺序(从寅起)
MONTH_ZHI_ORDER = ["寅","卯","辰","巳","午","未","申","酉","戌","亥","子","丑"]
# 五鼠遁: 日干 -> 子时天干index
WUSHU_BASE = {"甲":0,"己":0,"乙":2,"庚":2,"丙":4,"辛":4,"丁":6,"壬":6,"戊":8,"癸":8}
# 时辰顺序
SHICHEN_ORDER = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
SHICHEN_HOURS = {0:[23,0],1:[1,2],2:[3,4],3:[5,6],4:[7,8],5:[9,10],
                 6:[11,12],7:[13,14],8:[15,16],9:[17,18],10:[19,20],11:[21,22]}

def year_pillar(y, m, d):
    li_chun = date(y, 2, solar_term_day(y, 2))
    yp = y - 1 if date(y, m, d) < li_chun else y
    return GAN[(yp-4) % 10] + ZHI[(yp-4) % 12], yp

def month_pillar(y, m, d):
    yp = year_pillar(y, m, d)[1]
    yzhi = year_pillar(y, m, d)[0][0]  # 年干
    mz = month_zhi(y, m, d)
    base = WUHU_BASE[yzhi]
    off = MONTH_ZHI_ORDER.index(mz)
    mg = (base + off) % 10
    return GAN[mg] + mz

def day_pillar(y, m, d):
    g, z, _ = day_ganzhi(y, m, d)
    return g + z

def hour_pillar(y, m, d, hour):
    dg = day_pillar(y, m, d)[0]
    base = WUSHU_BASE[dg]
    sci = None
    for i, hrs in SHICHEN_HOURS.items():
        if hour in hrs:
            sci = i
            break
    if sci is None:
        sci = 0
    hg = (base + sci) % 10
    return GAN[hg] + SHICHEN_ORDER[sci]

def main():
    y, m, d = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    hour = int(sys.argv[4]) if len(sys.argv) > 4 else None
    yp = year_pillar(y, m, d)
    mp = month_pillar(y, m, d)
    dp = day_pillar(y, m, d)
    out = [f"年柱: {yp[0]}", f"月柱: {mp}", f"日柱: {dp} (日主 {dp[0]})"]
    if hour is not None:
        out.append(f"时柱: {hour_pillar(y, m, d, hour)}")
    print(" | ".join(out))

if __name__ == "__main__":
    main()
