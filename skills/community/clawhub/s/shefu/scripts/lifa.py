#!/usr/bin/env python3
"""历法模块 —— 年月日干支、月建、日建计算
纯 Python 标准库，零外部依赖。精度满足六爻纳甲和梅花易数起卦需求。
"""

import json
from datetime import datetime, date

# 天干地支
TGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
GANZHI_60 = [f"{TGAN[i % 10]}{DZHI[i % 12]}" for i in range(60)]

# 地支五行
DZHI_WX = {"子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火",
           "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"}

# ── 节气月建映射 ──
# 月建以节气为准：寅月始于立春，卯月始于惊蛰……
# 使用近似公历日期（±1天精度，对起卦足够）
MONTH_BRANCH_SOLAR = [
    # (节气起始日 M-D, 月建)
    ("01-06", "丑"),  # 小寒
    ("02-04", "寅"),  # 立春
    ("03-06", "卯"),  # 惊蛰
    ("04-05", "辰"),  # 清明
    ("05-06", "巳"),  # 立夏
    ("06-06", "午"),  # 芒种
    ("07-07", "未"),  # 小暑
    ("08-07", "申"),  # 立秋
    ("09-08", "酉"),  # 白露
    ("10-08", "戌"),  # 寒露
    ("11-07", "亥"),  # 立冬
    ("12-07", "子"),  # 大雪
]

# ── 干支计算 ──

def year_ganzhi(year: int) -> str:
    """公历年 → 年干支（以立春为界，此处用简化公式）"""
    gan = TGAN[(year - 4) % 10]
    zhi = DZHI[(year - 4) % 12]
    return f"{gan}{zhi}"


def month_zhi(dt: datetime = None) -> str:
    """公历日期 → 月建地支（以节气为准）"""
    if dt is None:
        dt = datetime.now()
    md = dt.strftime("%m-%d")
    current_zhi = "子"  # fallback
    for solar_start, zhi in MONTH_BRANCH_SOLAR:
        if md >= solar_start:
            current_zhi = zhi
    # 处理 1月1日-1月5日还在丑月的情况
    if md < "01-06":
        current_zhi = "丑"
    return current_zhi


def month_gan(month_zhi_val: str, year_gan: str) -> str:
    """月建地支 + 年天干 → 月干（五虎遁）
    甲己之年丙作首，乙庚之岁戊为头，
    丙辛必定寻庚起，丁壬壬位顺行流，
    若问戊癸何方发，甲寅之上好追求。
    """
    yg = year_gan
    start_map = {"甲": "丙", "己": "丙", "乙": "戊", "庚": "戊",
                 "丙": "庚", "辛": "庚", "丁": "壬", "壬": "壬",
                 "戊": "甲", "癸": "甲"}
    start_gan = start_map.get(yg, "甲")
    zhi_idx = DZHI.index(month_zhi_val)
    gan_idx = (TGAN.index(start_gan) + zhi_idx) % 10
    # 月干支从寅月开始
    # 寅月=正月，寅在DZHI索引为2
    yin_idx = 2
    offset = (zhi_idx - yin_idx) % 12
    gan_idx = (TGAN.index(start_gan) + offset) % 10
    return f"{TGAN[gan_idx]}{month_zhi_val}"


def day_ganzhi(dt: datetime = None) -> str:
    """公历日期 → 日干支
    以 2026-01-01 = 乙巳日 为基准（日干支序号 41）
    """
    if dt is None:
        dt = datetime.now()
    ref = date(2026, 1, 1)
    delta = (dt.date() - ref).days
    idx = (41 + delta) % 60  # 乙巳 = 第41位（0-index: 41）
    return GANZHI_60[idx]


def day_gan(dt: datetime = None) -> str:
    """公历日期 → 日干"""
    gz = day_ganzhi(dt)
    return gz[0]


def day_zhi(dt: datetime = None) -> str:
    """公历日期 → 日支"""
    gz = day_ganzhi(dt)
    return gz[1]


def now_ganzhi():
    """获取当前时间的完整干支信息"""
    now = datetime.now()
    ygz = year_ganzhi(now.year)
    yg = ygz[0]
    mzhi = month_zhi(now)
    mgz = month_gan(mzhi, yg)
    dgz = day_ganzhi(now)
    dg = dgz[0]
    dzhi_val = dgz[1]
    return {
        "公历": now.strftime("%Y-%m-%d %H:%M"),
        "年干支": ygz,
        "年干": yg,
        "年支": ygz[1],
        "月建": mzhi,
        "月干支": mgz,
        "月建五行": DZHI_WX[mzhi],
        "日干支": dgz,
        "日干": dg,
        "日支": dzhi_val,
        "日建五行": DZHI_WX[dzhi_val],
    }


# ── CLI ──

def main():
    import sys
    if sys.stdout.encoding != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")
    result = now_ganzhi()
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
