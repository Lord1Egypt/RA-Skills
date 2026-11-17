"""真太阳时校正 + 节气（月界）计算。

全部为纯数学（Meeus 低精度太阳黄经 + 二分搜索），离线、确定性、无网络。
- 真太阳时 = 钟表时间（默认北京时）+ 经度差时差 + 均时差。
- 节气（月界“节”）用太阳黄经到达特定角度的时刻判定。

坐标系约定（务必遵守，否则会“把节气提前 8 小时生效”）：
- 出生钟表时间 birth_dt 一律视为**北京时间（UTC+8）**。
- _solar_term_jd / _jd_to_dt 返回的节气时刻是 **UTC**。
- 两者比较前必须先把 birth_dt 减去 8 小时转 UTC（用 to_utc()），禁止直接比较。
- 真太阳时只用于**定时辰 / 定日界**，不用于与节气时刻比较。
"""
from __future__ import annotations

import math
from datetime import datetime, timedelta

BEIJING_UTC_OFFSET = timedelta(hours=8)


def to_utc(birth_dt: datetime) -> datetime:
    """出生钟表时间（北京时间 UTC+8）→ UTC，用于与节气时刻（UTC）比较。"""
    return birth_dt - BEIJING_UTC_OFFSET

# 中国主要城市 / 地区中心经度（东经，度）。缺失时回退 120（北京时基准）并标注未校时差。
CITY_LONGITUDE = {
    "北京": 116.41, "上海": 121.47, "广州": 113.26, "深圳": 114.06, "天津": 117.20,
    "重庆": 106.55, "成都": 104.07, "杭州": 120.15, "南京": 118.78, "武汉": 114.31,
    "西安": 108.94, "苏州": 120.62, "郑州": 113.65, "长沙": 112.94, "沈阳": 123.43,
    "大连": 121.62, "青岛": 120.38, "济南": 117.00, "哈尔滨": 126.53, "长春": 125.32,
    "石家庄": 114.51, "太原": 112.55, "太谷": 112.55, "晋中": 112.74, "呼和浩特": 111.75, "合肥": 117.28, "福州": 119.30,
    "厦门": 118.09, "南昌": 115.86, "昆明": 102.83, "贵阳": 106.71, "南宁": 108.37,
    "海口": 110.20, "兰州": 103.83, "西宁": 101.78, "银川": 106.27, "乌鲁木齐": 87.62,
    "拉萨": 91.14, "东莞": 113.75, "佛山": 113.12, "宁波": 121.55, "无锡": 120.30,
    "温州": 120.70, "常州": 119.95, "徐州": 117.18, "唐山": 118.18, "保定": 115.46,
    "烟台": 121.39, "潍坊": 119.16, "洛阳": 112.45, "中山": 113.39, "惠州": 114.42,
    "珠海": 113.55, "汕头": 116.68, "揭阳": 116.37, "普宁": 116.17, "潮州": 116.63, "威海": 122.12, "大庆": 125.03, "鞍山": 122.99,
    # 用户案例相关
    "盂县": 113.37, "阳泉": 113.57, "平定": 113.62, "昔阳": 114.05, "寿阳": 113.16,
    # 湖南
    "衡阳": 112.57, "株洲": 113.13, "湘潭": 112.94, "岳阳": 113.13, "常德": 111.69,
    "郴州": 113.02, "邵阳": 111.47, "怀化": 109.96, "娄底": 111.99, "益阳": 112.35,
    "永州": 111.61, "张家界": 110.48, "湘西": 109.74,
    # 河南
    "南阳": 112.53, "信阳": 114.09, "开封": 114.31, "新乡": 113.93,
    "许昌": 113.85, "平顶山": 113.19, "驻马店": 114.02, "周口": 114.65,
    "商丘": 115.65, "安阳": 114.39, "焦作": 113.24, "濮阳": 115.03,
    "漯河": 114.02, "三门峡": 111.19, "鹤壁": 114.30, "济源": 112.60,
}

# 12 个“节”对应的太阳黄经（度）。索引 0=立春(寅月) ... 11=小寒(丑月)。
# 月支映射：0→寅(2) 1→卯(3) 2→辰(4) 3→巳(5) 4→午(6) 5→未(7)
#            6→申(8) 7→酉(9) 8→戌(10) 9→亥(11) 10→子(0) 11→丑(1)
JIE_LONGITUDE = [315, 345, 15, 45, 75, 105, 135, 165, 195, 225, 255, 285]
JIE_TO_BRANCH = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1]  # 寅..子..丑


def _julian_day(dt: datetime) -> float:
    """公历 datetime -> 儒略日（含小数）。"""
    y = dt.year
    m = dt.month
    d = dt.day + (dt.hour + dt.minute / 60.0 + dt.second / 3600.0) / 24.0
    if m <= 2:
        y -= 1
        m += 12
    a = y // 100
    b = 2 - a + a // 4
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + d + b - 1524.5


# 儒略日 ↔ datetime 以 2000-01-01 12:00 UTC（JD 2451545.0）为基准，避免手写反算取整错误
_JD_EPOCH = datetime(2000, 1, 1, 12, 0, 0)


def _jd_to_dt(jd: float) -> datetime:
    return _JD_EPOCH + timedelta(days=jd - 2451545.0)


def _sun_longitude(jd: float) -> float:
    """Meeus 低精度太阳黄经（度，0-360）。误差分钟级，足够判定月界。"""
    t = (jd - 2451545.0) / 36525.0
    l0 = 280.46646 + 36000.76983 * t + 0.0003032 * t * t
    m = 357.52911 + 35999.05029 * t - 0.0001537 * t * t
    mr = math.radians(m)
    c = (1.914602 - 0.004817 * t) * math.sin(mr)
    c += (0.019993 - 0.000101 * t) * math.sin(2 * mr)
    c += 0.000289 * math.sin(3 * mr)
    return (l0 + c) % 360.0


def _equation_of_time(jd: float) -> float:
    """均时差（分钟），低精度近似。"""
    dt = _jd_to_dt(jd)
    doy = dt.timetuple().tm_yday
    b = 360.0 / 365.24 * (doy - 81)
    br = math.radians(b)
    return 9.87 * math.sin(2 * br) - 7.53 * math.cos(br) - 1.5 * math.sin(br)


def resolve_longitude(birth_place: str):
    """从出生地解析经度，返回 (经度, 是否精确匹配)。"""
    for name, lng in CITY_LONGITUDE.items():
        if name in birth_place:
            return lng, True
    return 120.0, False


def solar_time_correction_minutes(birth_dt: datetime, birth_place: str):
    """返回 (经度差分钟, 均时差分钟, 是否精确匹配城市)。"""
    lng, matched = resolve_longitude(birth_place)
    jd = _julian_day(birth_dt)
    eot = _equation_of_time(jd)
    lng_diff = (lng - 120.0) * 4.0  # 每度 4 分钟
    return lng_diff, eot, matched


def to_true_solar_time(birth_dt: datetime, birth_place: str):
    """钟表时间（默认北京时）→ 真太阳时 datetime；返回 (true_dt, 校正分钟, 是否精确)。"""
    lng_diff, eot, matched = solar_time_correction_minutes(birth_dt, birth_place)
    total = lng_diff + eot
    true_dt = birth_dt + timedelta(minutes=total)
    return true_dt, total, matched


def _solar_term_jd(year: int, target_lon: float):
    """二分搜索 year 年内太阳黄经过 target_lon 的时刻（儒略日）。

    关键：用原始经度差（不归一化到 ±180），并以 |Δ|<180 排除 360° 回绕产生的假穿越。
    """
    lo = datetime(year, 1, 1)
    hi = datetime(year + 1, 1, 1)
    jd_lo = _julian_day(lo)
    jd_hi = _julian_day(hi)
    step = 0.5
    prev = _sun_longitude(jd_lo) - target_lon
    cur = jd_lo
    while cur < jd_hi:
        nxt = cur + step
        d = _sun_longitude(nxt) - target_lon
        if (prev <= 0 <= d or prev >= 0 >= d) and abs(d - prev) < 180:
            a, b = cur, nxt
            for _ in range(40):
                mid = (a + b) / 2
                dm = _sun_longitude(mid) - target_lon
                if abs(dm) < 1e-6:
                    return mid
                if dm * prev_sign(a, cur, target_lon) > 0:
                    a = mid
                else:
                    b = mid
            return (a + b) / 2
        prev = d
        cur = nxt
    return jd_hi


def prev_sign(a, b, target):
    da = _sun_longitude(a) - target
    da = ((da + 180) % 360) - 180
    return 1 if da >= 0 else -1


def get_month_branch(birth_dt: datetime):
    """返回生日所在月支序号（0=子..11=亥）与当月“节”的公历日期。

    月界用“节”（立春/惊蛰/.../大雪/小寒），以真太阳时前的公历生日判定即可
    （节气由天文决定，与真太阳时无关）。
    """
    y = birth_dt.year
    birth_utc = to_utc(birth_dt)  # 北京时间 → UTC，与节气时刻同坐标系
    # 收集跨年相关节：上一年全部 12 节 + 本年 12 节 + 下一年 12 节
    candidates = []
    for yr in (y - 1, y, y + 1):
        for idx, lon in enumerate(JIE_LONGITUDE):
            jd = _solar_term_jd(yr, lon)
            candidates.append((_jd_to_dt(jd), idx))
    candidates.sort(key=lambda x: x[0])
    chosen = candidates[0]
    for c in candidates:
        if c[0] <= birth_utc:
            chosen = c
        else:
            break
    idx = chosen[1]
    return JIE_TO_BRANCH[idx], chosen[0].date().isoformat()
