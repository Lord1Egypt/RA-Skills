# -*- coding: utf-8 -*-
"""
bazi.py - 八字四柱排盘（子平派，立春为界 / 节气换月）

依赖：lunar_python（仅用于精确 24 节气日期，天文部分）。
      该运行库需由部署方在运行环境中预先提供，本脚本不含安装指令。
      运行：python bazi.py --year 1990 --month 1 --day 1 --hour 12 --minute 0 --gender 男 --city 北京

说明：
  - 年柱：以「立春」为界（非春节）。
  - 月柱：以十二「节」换月（小寒->丑月 ... 立春->寅月 ...）。
  - 日柱：按公历日期 JD 公式推算（自洽，不依赖农历）。
  - 时柱：五鼠遁；默认「晚子时」（23:00-23:59 算次日），可用 --sect 0 切早子时。
  - 真太阳时：按出生城市经度校正，并扣回 1986-1991 大陆夏令时。
  - 大运：起运数 = 距最近「节」天数 / 3；阳年男/阴年女顺排，反之逆排。

仅作规则计算与推演参考，不可替代真人大师解读。
"""
import argparse
import sys
import math
import datetime

try:
    import lunar_python as L
except ImportError:
    sys.stderr.write(
        "ERROR: 运行环境缺少依赖 lunar_python。\n"
        "请由部署方在运行环境中预先提供该库后重试"
        "（本脚本不含安装指令）。\n"
    )
    sys.exit(2)

# ---------- 基础常量 ----------
GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
GAN_WX = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土",
          "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
ZHI_WX = {"子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
          "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"}
GAN_YINYANG = {"甲": "阳", "乙": "阴", "丙": "阳", "丁": "阴", "戊": "阳", "己": "阴",
               "庚": "阳", "辛": "阴", "壬": "阳", "癸": "阴"}
YANG_GAN = {"甲", "丙", "戊", "庚", "壬"}
# 五虎遁：年干 -> 正月(寅月)天干
WUHU = {"甲": "丙", "己": "丙", "乙": "戊", "庚": "戊", "丙": "庚", "辛": "庚",
        "丁": "壬", "壬": "壬", "戊": "甲", "癸": "甲"}
# 五鼠遁：日干 -> 子时天干
WUSHU = {"甲": "甲", "乙": "丙", "丙": "戊", "丁": "庚", "戊": "壬",
         "己": "甲", "庚": "丙", "辛": "戊", "壬": "庚", "癸": "壬"}
# 十二「节」-> 月支（寅月起正月）
JIE_LIST = [("立春", "寅"), ("惊蛰", "卯"), ("清明", "辰"), ("立夏", "巳"),
            ("芒种", "午"), ("小暑", "未"), ("立秋", "申"), ("白露", "酉"),
            ("寒露", "戌"), ("立冬", "亥"), ("大雪", "子"), ("小寒", "丑")]
# 六十甲子
GANZHI60 = [GAN[i % 10] + ZHI[i % 12] for i in range(60)]

# 城市经度表（东经为正），仅常用城市
CITY_LON = {
    "北京": 116.40, "上海": 121.47, "广州": 113.26, "深圳": 114.06, "成都": 104.07,
    "重庆": 106.55, "武汉": 114.30, "西安": 108.95, "杭州": 120.15, "南京": 118.78,
    "郑州": 113.65, "天津": 117.20, "沈阳": 123.43, "哈尔滨": 126.53, "济南": 117.00,
    "长沙": 112.94, "福州": 119.30, "厦门": 118.10, "昆明": 102.71, "贵阳": 106.71,
    "兰州": 103.83, "乌鲁木齐": 87.62, "拉萨": 91.11, "呼和浩特": 111.65, "南宁": 108.37,
    "海口": 110.35, "香港": 114.17, "澳门": 113.55, "台北": 121.56, "青岛": 120.33,
    "大连": 121.62, "宁波": 121.55, "苏州": 120.62, "太原": 112.55, "石家庄": 114.51,
    "合肥": 117.27, "南昌": 115.86, "长春": 125.32, "银川": 106.27, "西宁": 101.78,
}

# 大陆夏令时区间（时钟 +1h），需扣回标准时
DST_RANGES = [
    ("1986-05-04", "1986-09-14"), ("1987-04-12", "1987-09-13"),
    ("1988-04-10", "1988-09-11"), ("1989-04-16", "1989-09-10"),
    ("1990-04-15", "1990-09-16"), ("1991-04-14", "1991-09-15"),
]


# ---------- 干支数学 ----------
def gz_index(gz):
    return GANZHI60.index(gz)


def year_gz(year):
    """year 年之干支（甲子=0 对应公元4年）"""
    idx = (year - 4) % 60
    return GANZHI60[idx]


def jd_from_gregorian(y, m, d, hour_float):
    """公历 -> 儒略日（UT）"""
    if m <= 2:
        y -= 1
        m += 12
    a = y // 100
    b = 2 - a + a // 4
    jd = (math.floor(365.25 * (y + 4716))
          + math.floor(30.6001 * (m + 1))
          + d + b - 1524.5 + hour_float / 24.0)
    return jd


def day_gz_from_jd(jd):
    """日干支（甲子=0）。jd 取当日 12:00（午时，避开半日界）。
    标定：与 lunar_python(Solar->Lunar).getDay 全样本对齐，C=49。"""
    idx = int((jd + 49) % 60)
    return GANZHI60[idx]


def shishen(day_gan, other_gan):
    """other_干 相对 日干 的十神"""
    wd, wt = GAN_WX[day_gan], GAN_WX[other_gan]
    yd, yt = GAN_YINYANG[day_gan], GAN_YINYANG[other_gan]
    gen = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}      # 生
    ke = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}      # 克
    if wt == wd:
        return "比肩" if yt == yd else "劫财"
    if gen[wt] == wd:  # 他生我 -> 印
        return "偏印" if yt == yd else "正印"
    if gen[wd] == wt:  # 我生 -> 食伤
        return "食神" if yt == yd else "伤官"
    if ke[wd] == wt:  # 我克 -> 财
        return "偏财" if yt == yd else "正财"
    # 克我 -> 官杀
    return "七杀" if yt == yd else "正官"


def zhi_benqi(z):
    """地支本气天干（用于地支十神）"""
    return {"子": "癸", "丑": "己", "寅": "甲", "卯": "乙", "辰": "戊",
            "巳": "丙", "午": "丁", "未": "己", "申": "庚", "酉": "辛",
            "戌": "戊", "亥": "壬"}[z]


# ---------- 节气 ----------
def _solar_to_dt(s):
    """lunar_python.Solar -> datetime（北京时间）"""
    return datetime.datetime(s.getYear(), s.getMonth(), s.getDay(),
                             s.getHour(), s.getMinute(), s.getSecond())


def jieqi_dict(year):
    """返回 {节气名: datetime(北京时间)}，仅取十二「节」"""
    lunar = L.Lunar.fromYmdHms(year, 6, 1, 12, 0, 0)
    tbl = lunar.getJieQiTable()
    out = {}
    for name, dt in tbl.items():
        if name in [j[0] for j in JIE_LIST]:
            out[name] = _solar_to_dt(dt)
    return out


def jie_timeline(years):
    """返回排序的 [(datetime北京时间, 月支), ...] 覆盖给定年份的十二节"""
    items = []
    for y in years:
        d = jieqi_dict(y)
        for jname, zhi in JIE_LIST:
            if jname in d:
                items.append((d[jname], zhi))
    items.sort(key=lambda x: x[0])
    return items


# ---------- 真太阳时 ----------
def equation_of_time(dt_utc):
    """时差（分钟），NOAA 近似"""
    # 用 UTC 日期换算日角
    a = math.floor((14 - dt_utc.month) / 12)
    y = dt_utc.year + 4800 - a
    m = dt_utc.month + 12 * a - 3
    jdn = (dt_utc.day + math.floor((153 * m + 2) / 5) + 365 * y
           + math.floor(y / 4) - math.floor(y / 100) + math.floor(y / 400) - 32045)
    n = jdn - 2451545 + 0.0008  # 从 J2000 起算的天数(近似)
    b = math.radians(360.0 / 365.25 * n)
    eot = 229.18 * (0.000075 + 0.001868 * math.cos(b) - 0.032077 * math.sin(b)
                    - 0.014615 * math.cos(2 * b) - 0.040849 * math.sin(2 * b))
    return eot


def in_dst(y, m, d):
    bd = datetime.date(y, m, d)
    for s, e in DST_RANGES:
        if datetime.date.fromisoformat(s) <= bd <= datetime.date.fromisoformat(e):
            return True
    return False


def true_solar_correct(beijing_dt, lon, apply_dst):
    """北京时间(标准时) -> 真太阳时。返回 (corrected_dt, corrected_jd, notes)"""
    notes = []
    std = beijing_dt
    if apply_dst and in_dst(std.year, std.month, std.day):
        std = std - datetime.timedelta(hours=1)
        notes.append("已扣回夏令时 1 小时")
    # 经度差：地方平太阳时 = 标准时 + (lon - 120) * 4 分钟
    lon_offset_min = (lon - 120.0) * 4.0
    # 真太阳时 = 平太阳时 + 时差
    eot = equation_of_time(std)
    total_min = lon_offset_min + eot
    corrected = std + datetime.timedelta(minutes=total_min)
    if abs(lon_offset_min) > 0.5:
        notes.append("经度校正 %.2f 分（%s）" % (lon_offset_min, "东经" if lon >= 120 else "西经"))
        notes.append("时差 %.2f 分" % eot)
    # corrected_jd（用 corrected 当作当地时间推算 JD，用于节气比较需一致变换）
    jd = jd_from_gregorian(corrected.year, corrected.month, corrected.day,
                           corrected.hour + corrected.minute / 60.0 + corrected.second / 3600.0)
    return corrected, jd, notes


def jieqi_true_jd(beijing_dt, lon):
    """把节气的北京时间转化为与 birth 同帧的真太阳时 JD（仅用于比较先后）"""
    eot = equation_of_time(beijing_dt)
    lon_offset_min = (lon - 120.0) * 4.0
    jd = jd_from_gregorian(beijing_dt.year, beijing_dt.month, beijing_dt.day,
                           beijing_dt.hour + beijing_dt.minute / 60.0 + beijing_dt.second / 3600.0)
    return jd + (lon_offset_min + eot) / 1440.0


# ---------- 排盘 ----------
def compute_bazi(year, month, day, hour, minute, gender, city=None, lon=None,
                 sect=1, apply_dst=True):
    """返回结构化结果 dict"""
    assert gender in ("男", "女"), "gender must be 男/女"
    if city and city not in CITY_LON and lon is None:
        raise ValueError("未知城市 %s，请用 --lon 提供经度，或 --city 选内置城市" % city)
    if lon is None:
        lon = CITY_LON.get(city) if city else 120.0

    beijing_dt = datetime.datetime(year, month, day, hour, minute, 0)
    corrected, corr_jd, notes = true_solar_correct(beijing_dt, lon, apply_dst)
    cy, cm, cd = corrected.year, corrected.month, corrected.day
    chour_f = corrected.hour + corrected.minute / 60.0

    # 年柱：以立春为界
    # 取出生年前后年份的节气，找该年立春
    ybars = [cy - 1, cy, cy + 1]
    jt = jie_timeline(ybars)
    # 年柱以立春为界：取当年与上一年立春，按真太阳时帧比较
    lichun_this = jieqi_dict(cy).get("立春")
    lichun_prev = jieqi_dict(cy - 1).get("立春")
    # 出生真太阳时 JD 与立春同帧 JD 比较
    if lichun_this:
        lichun_jd = jieqi_true_jd(lichun_this, lon)
    else:
        lichun_jd = None
    if lichun_prev:
        lichun_prev_jd = jieqi_true_jd(lichun_prev, lon)
    else:
        lichun_prev_jd = None
    if lichun_jd is not None and corr_jd >= lichun_jd:
        year_used = cy
    elif lichun_prev_jd is not None and corr_jd >= lichun_prev_jd:
        year_used = cy - 1
    else:
        year_used = cy - 1
    yg = year_gz(year_used)
    y_gan, y_zhi = yg[0], yg[1]

    # 月柱：最近「节」<= 出生真太阳时
    # 先把出生真太阳时转为可比较的 JD（corr_jd 已同帧）
    best_zhi = None
    best_jd = None
    for jdt_beijing, zhi in jt:
        jj = jieqi_true_jd(jdt_beijing, lon)
        if jj <= corr_jd:
            if best_jd is None or jj > best_jd:
                best_jd = jj
                best_zhi = zhi
    if best_zhi is None:
        best_zhi = "子"  # fallback
    m_zhi = best_zhi
    # 月干：寅月(正月)干 = WUHU[年干]，按 月支 在 寅..丑 序列位置推进
    seq = [z for _, z in JIE_LIST]  # 寅卯辰巳午未申酉戌亥子丑
    p = seq.index(m_zhi)
    m_gan = GAN[(GAN.index(WUHU[y_gan]) + p) % 10]
    mg = m_gan + m_zhi

    # 日柱：晚子时(sect=1) 23:00-23:59 用次日日干；早子时(sect=0) 用当日
    day_for_gz = corrected
    if sect == 1 and 23 <= corrected.hour < 24:
        day_for_gz = corrected + datetime.timedelta(days=1)
    d_jd = jd_from_gregorian(day_for_gz.year, day_for_gz.month, day_for_gz.day, 12.0)
    dgz = day_gz_from_jd(d_jd)
    d_gan, d_zhi = dgz[0], dgz[1]

    # 时柱：时辰地支
    h = corrected.hour
    if h == 23 or (0 <= h < 1):
        zhi_h = "子"
    else:
        zhi_h = ZHI[(h + 1) // 2 % 12]
    # 时干：五鼠遁（用当日日干，晚子时用次日日干）
    s_gan = GAN[(GAN.index(WUSHU[d_gan]) + ZHI.index(zhi_h)) % 10]
    sg = s_gan + zhi_h

    # 五行 tally（四柱 8 字）
    wuxing_count = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
    for g in (y_gan, y_zhi, m_gan, m_zhi, d_gan, d_zhi, s_gan, zhi_h):
        wx = GAN_WX.get(g) or ZHI_WX.get(g)
        if wx:
            wuxing_count[wx] += 1

    # 十神（天干 + 地支本气，相对日主）
    pillars = {"年": yg, "月": mg, "日": dgz, "时": sg}
    shishen_map = {}
    for name, gz in pillars.items():
        tg, dz = gz[0], gz[1]
        ss_tg = shishen(d_gan, tg)
        ss_dz = shishen(d_gan, zhi_benqi(dz))
        shishen_map[name] = {"天干": tg, "天干十神": ss_tg,
                             "地支": dz, "地支本气十神": ss_dz}

    # 大运
    yang = y_gan in YANG_GAN
    forward = (yang and gender == "男") or ((not yang) and gender == "女")
    # 起运：顺排取下一个节，逆排取上一个节
    target_jd = None
    if forward:
        for jdt_beijing, _ in jt:
            jj = jieqi_true_jd(jdt_beijing, lon)
            if jj > corr_jd:
                target_jd = jj
                break
    else:
        for jdt_beijing, _ in reversed(jt):
            jj = jieqi_true_jd(jdt_beijing, lon)
            if jj < corr_jd:
                target_jd = jj
                break
    if target_jd is None:
        target_jd = corr_jd
    days_diff = abs(target_jd - corr_jd) * 1440.0 / 1440.0  # 天
    # JD 差即天数
    days_diff = abs(target_jd - corr_jd)
    start_age = days_diff / 3.0  # 三天为一岁
    m_idx = gz_index(mg)
    dayun = []
    for i in range(1, 11):
        if forward:
            g = GANZHI60[(m_idx + i) % 60]
        else:
            g = GANZHI60[(m_idx - i) % 60]
        age0 = start_age + (i - 1) * 10
        age1 = start_age + i * 10
        dayun.append({"运": i, "干支": g, "起运岁": round(age0, 1),
                      "交运岁": round(age1, 1), "起运年": year + int(age0)})

    result = {
        "输入": {"公历": "%04d-%02d-%02d %02d:%02d" % (year, month, day, hour, minute),
                 "性别": gender, "城市": city, "经度": round(lon, 2),
                 "早晚子时": "晚子时" if sect == 1 else "早子时"},
        "真太阳时校正": notes or ["未校（无城市/经度）"],
        "校正后时间": "%04d-%02d-%02d %02d:%02d" % (cy, cm, cd, corrected.hour, corrected.minute),
        "四柱": pillars,
        "日主": d_gan,
        "五行个数(四柱)": wuxing_count,
        "十神": shishen_map,
        "大运": {"顺逆": "顺排" if forward else "逆排",
                 "起运岁": round(start_age, 2),
                 "运程": dayun},
    }
    return result


def format_text(r):
    lines = []
    inp = r["输入"]
    lines.append("【八字排盘 · 子平派】")
    lines.append("输入：%s  性别：%s  城市：%s  经度：%s  %s"
                 % (inp["公历"], inp["性别"], inp["城市"], inp["经度"], inp["早晚子时"]))
    lines.append("真太阳时校正：%s" % "；".join(r["真太阳时校正"]))
    lines.append("校正后：%s" % r["校正后时间"])
    p = r["四柱"]
    lines.append("")
    lines.append("四柱：  年柱 %s    月柱 %s    日柱 %s    时柱 %s"
                 % (p["年"], p["月"], p["日"], p["时"]))
    lines.append("日主：%s" % r["日主"])
    wx = r["五行个数(四柱)"]
    lines.append("五行（四柱八字）：金%s 木%s 水%s 火%s 土%s"
                 % (wx["金"], wx["木"], wx["水"], wx["火"], wx["土"]))
    lines.append("")
    lines.append("十神（相对日主）：")
    for name in ("年", "月", "日", "时"):
        sm = r["十神"][name]
        if name == "日":
            lines.append("  %s柱 %s%s：日主" % (name, sm["天干"], sm["地支"]))
        else:
            lines.append("  %s柱 %s%s：天干[%s] 地支本气[%s]"
                         % (name, sm["天干"], sm["地支"], sm["天干十神"], sm["地支本气十神"]))
    lines.append("")
    du = r["大运"]
    lines.append("大运：%s  起运 %.2f 岁" % (du["顺逆"], du["起运岁"]))
    for d in du["运程"]:
        lines.append("  %2d运 %s  起 %s 岁 / 交 %s 岁（约 %d 年）"
                     % (d["运"], d["干支"], d["起运岁"], d["交运岁"], d["起运年"]))
    lines.append("")
    lines.append("（本结果为规则计算参考，最终洞察请结合处境或咨询真人大师）")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="八字四柱排盘（子平派）")
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("--month", type=int, required=True)
    ap.add_argument("--day", type=int, required=True)
    ap.add_argument("--hour", type=int, default=0)
    ap.add_argument("--minute", type=int, default=0)
    ap.add_argument("--gender", choices=["男", "女"], required=True)
    ap.add_argument("--city", default=None)
    ap.add_argument("--lon", type=float, default=None)
    ap.add_argument("--sect", type=int, default=1, choices=[0, 1],
                   help="0=早子时, 1=晚子时(默认)")
    ap.add_argument("--no-dst", action="store_true", help="不扣回夏令时")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()
    r = compute_bazi(args.year, args.month, args.day, args.hour, args.minute,
                     args.gender, city=args.city, lon=args.lon, sect=args.sect,
                     apply_dst=not args.no_dst)
    if args.json:
        import json
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(format_text(r))


if __name__ == "__main__":
    main()
