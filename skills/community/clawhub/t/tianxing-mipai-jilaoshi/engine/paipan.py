"""排四柱 + 旬空（日柱旬空用于格局，分柱空亡用于六亲/风水读象）。

算法确定性、离线：
- 年柱：以立春为界（solar_time 节气计算）。
- 月柱：月界“节”定月支（solar_time）+ 五虎遁定月干。
- 日柱：儒略日 JDN，日干支序号 = (JDN + 49) % 60（锚点校验：1990-12-07=丙午42，2000-01-01=戊午54）。
- 时柱：真太阳时定日界/时支 + 五鼠遁定时干。
- 旬空：六甲旬空表；同时输出分柱空亡。
十神以日干为基准，地支按本气藏干计算。
"""
from __future__ import annotations

import solar_time as st

GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
GAN_WX = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]  # 木火土金水
BRANCH = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
BRANCH_WX = [4, 2, 0, 0, 2, 1, 1, 2, 3, 3, 2, 4]
BRANCH_PRIMARY = [9, 5, 0, 1, 4, 2, 3, 5, 6, 7, 4, 8]  # 本气天干 idx
# 六甲旬空：旬号(日干支序号//10) -> 空亡两支
KONGWANG = {0: ("戌", "亥"), 1: ("申", "酉"), 2: ("午", "未"),
             3: ("辰", "巳"), 4: ("寅", "卯"), 5: ("子", "丑")}


def gz_index(g: int, z: int) -> int:
    for n in range(60):
        if n % 10 == g and n % 12 == z:
            return n
    raise ValueError(f"invalid gan/zhi {g},{z}")


def shishen(day_idx: int, other_idx: int) -> str:
    if other_idx == day_idx:
        return "比肩"
    dw = GAN_WX[day_idx]
    ow = GAN_WX[other_idx]
    same = (day_idx % 2) == (other_idx % 2)
    if ow == dw:
        return "劫财"
    if (ow + 1) % 5 == dw:  # 生我
        return "正印" if not same else "偏印"
    if (dw + 1) % 5 == ow:  # 我生
        return "伤官" if not same else "食神"
    if (ow + 2) % 5 == dw:  # 克我
        return "正官" if not same else "七杀"
    if (dw + 2) % 5 == ow:  # 我克
        return "正财" if not same else "偏财"
    return "未知"


def _hour_branch(hour: int) -> int:
    return (hour + 1) // 2 % 12


def paipan(birth_dt, birth_place: str):
    """返回四柱排盘结果字典（确定性）。birth_dt 为公历 datetime（钟表时间）。"""
    y = birth_dt.year
    # 年柱：立春分界（birth_dt 为北京时间，须转 UTC 后与节气时刻比较）
    lichun_jd = st._solar_term_jd(y, 315.0)
    lichun_dt = st._jd_to_dt(lichun_jd)
    birth_utc = st.to_utc(birth_dt)
    year_for_pillar = y if birth_utc >= lichun_dt else y - 1
    year_idx = (year_for_pillar - 1984) % 60
    year_gan, year_zhi = year_idx % 10, year_idx % 12

    # 月柱：月支（节气）+ 五虎遁
    month_branch, jieqi_date = st.get_month_branch(birth_dt)
    yin_gan = (year_gan * 2 + 2) % 10
    month_gan = (yin_gan + ((month_branch - 2) % 12)) % 10

    # 真太阳时 -> 日界/时支
    true_dt, corr_min, matched = st.to_true_solar_time(birth_dt, birth_place)

    # 日柱
    jd = st._julian_day(true_dt)
    day_idx = (int(round(jd)) + 49) % 60
    day_gan, day_zhi = day_idx % 10, day_idx % 12

    # 时柱：五鼠遁
    hour_branch = _hour_branch(true_dt.hour)
    zi_gan = (day_gan * 2) % 10
    hour_gan = (zi_gan + hour_branch) % 10

    result = {
        "year": (year_gan, year_zhi),
        "month": (month_gan, month_branch),
        "day": (day_gan, day_zhi),
        "hour": (hour_gan, hour_branch),
    }

    def pillar_label(g, z):
        return GAN[g] + BRANCH[z]

    def pillar_shishen(g, z):
        return shishen(day_gan, g), shishen(day_gan, BRANCH_PRIMARY[z])

    out = {
        "four_pillars": {
            "year": {"gan": year_gan, "zhi": year_zhi, "label": pillar_label(*result["year"]),
                      "gan_shishen": pillar_shishen(*result["year"])[0],
                      "zhi_shishen": pillar_shishen(*result["year"])[1]},
            "month": {"gan": month_gan, "zhi": month_branch, "label": pillar_label(*result["month"]),
                       "gan_shishen": pillar_shishen(*result["month"])[0],
                       "zhi_shishen": pillar_shishen(*result["month"])[1]},
            "day": {"gan": day_gan, "zhi": day_zhi, "label": pillar_label(*result["day"]),
                     "gan_shishen": "日主", "zhi_shishen": pillar_shishen(*result["day"])[1]},
            "hour": {"gan": hour_gan, "zhi": hour_branch, "label": pillar_label(*result["hour"]),
                      "gan_shishen": pillar_shishen(*result["hour"])[0],
                      "zhi_shishen": pillar_shishen(*result["hour"])[1]},
        },
        "day_master": day_gan,
        "true_solar_time": true_dt.strftime("%Y-%m-%d %H:%M"),
        "solar_corr_min": round(corr_min, 2),
        "city_matched": matched,
        "jieqi_date": jieqi_date,
        "day_index": day_idx,
    }

    # 旬空：日柱旬空（格局用）
    out["kongwang_day_branch"] = KONGWANG[day_idx // 10]
    # 分柱空亡（六亲/风水读象用）
    out["kongwang_per_pillar"] = {}
    for pk, (g, z) in result.items():
        idx = gz_index(g, z)
        out["kongwang_per_pillar"][pk] = KONGWANG[idx // 10]
    return out
