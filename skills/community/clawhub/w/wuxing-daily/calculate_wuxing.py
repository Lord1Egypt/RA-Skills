#!/usr/bin/env python3
"""
五行命理计算器
根据生辰八字计算五行属性和命格分析
"""

from datetime import datetime
from typing import Dict, List, Tuple

# 天干
TIANGAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 地支
DIZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# 天干五行属性
TIANGAN_WUXING = {
    "甲": "木", "乙": "木",
    "丙": "火", "丁": "火",
    "戊": "土", "己": "土",
    "庚": "金", "辛": "金",
    "壬": "水", "癸": "水"
}

# 地支五行属性
DIZHI_WUXING = {
    "子": "水", "丑": "土", "寅": "木", "卯": "木",
    "辰": "土", "巳": "火", "午": "火", "未": "土",
    "申": "金", "酉": "金", "戌": "土", "亥": "水"
}

# 六十甲子纳音五行表
NAYIN_TABLE = {
    "甲子": "海中金", "乙丑": "海中金",
    "丙寅": "炉中火", "丁卯": "炉中火",
    "戊辰": "大林木", "己巳": "大林木",
    "庚午": "路旁土", "辛未": "路旁土",
    "壬申": "剑锋金", "癸酉": "剑锋金",
    "甲戌": "山头火", "乙亥": "山头火",
    "丙子": "涧下水", "丁丑": "涧下水",
    "戊寅": "城头土", "己卯": "城头土",
    "庚辰": "白蜡金", "辛巳": "白蜡金",
    "壬午": "杨柳木", "癸未": "杨柳木",
    "甲申": "泉中水", "乙酉": "泉中水",
    "丙戌": "屋上土", "丁亥": "屋上土",
    "戊子": "霹雳火", "己丑": "霹雳火",
    "庚寅": "松柏木", "辛卯": "松柏木",
    "壬辰": "长流水", "癸巳": "长流水",
    "甲午": "沙中金", "乙未": "沙中金",
    "丙申": "山下火", "丁酉": "山下火",
    "戊戌": "平地木", "己亥": "平地木",
    "庚子": "壁上土", "辛丑": "壁上土",
    "壬寅": "金箔金", "癸卯": "金箔金",
    "甲辰": "佛灯火", "乙巳": "佛灯火",
    "丙午": "天河水", "丁未": "天河水",
    "戊申": "大驿土", "己酉": "大驿土",
    "庚戌": "钗钏金", "辛亥": "钗钏金",
    "壬子": "桑柘木", "癸丑": "桑柘木",
    "甲寅": "大溪水", "乙卯": "大溪水",
    "丙辰": "沙中土", "丁巳": "沙中土",
    "戊午": "天上火", "己未": "天上火",
    "庚申": "石榴木", "辛酉": "石榴木",
    "壬戌": "大海水", "癸亥": "大海水"
}

# 时辰对应表（24小时制）
SHICHEN_MAP = {
    (23, 1): "子",
    (1, 3): "丑",
    (3, 5): "寅",
    (5, 7): "卯",
    (7, 9): "辰",
    (9, 11): "巳",
    (11, 13): "午",
    (13, 15): "未",
    (15, 17): "申",
    (17, 19): "酉",
    (19, 21): "戌",
    (21, 23): "亥"
}


def get_shichen(hour: int) -> str:
    """根据小时获取时辰"""
    for (start, end), sc in SHICHEN_MAP.items():
        if start <= hour < end or (start > end and (hour >= start or hour < end)):
            return sc
    return "子"


def get_year_ganzhi(year: int) -> Tuple[str, str]:
    """根据年份获取年柱天干地支"""
    # 1984年是甲子年
    offset = (year - 1984) % 60
    gan_index = offset % 10
    zhi_index = offset % 12
    return TIANGAN[gan_index], DIZHI[zhi_index]


def get_month_ganzhi(year_gan: str, month: int) -> Tuple[str, str]:
    """根据年干和月份获取月柱天干地支"""
    # 年上起月法
    # 甲己之年丙作首，乙庚之岁戊为头
    # 丙辛之岁寻庚上，丁壬壬位顺行流
    # 戊癸之年何方发，甲寅之上好追求
    
    year_start_map = {
        "甲": "丙", "己": "丙",
        "乙": "戊", "庚": "戊",
        "丙": "庚", "辛": "庚",
        "丁": "壬", "壬": "壬",
        "戊": "甲", "癸": "甲"
    }
    
    start_gan = year_start_map.get(year_gan, "丙")
    start_index = TIANGAN.index(start_gan)
    
    # 正月（农历一月）对应 start_gan
    gan_index = (start_index + month - 1) % 10
    zhi_index = (month + 1) % 12  # 正月建寅
    
    return TIANGAN[gan_index], DIZHI[zhi_index]


def get_day_ganzhi(year: int, month: int, day: int) -> Tuple[str, str]:
    """根据年月日获取日柱天干地支"""
    # 使用蔡勒公式计算，然后映射到干支
    # 已知：1989年12月12日是丙午日
    from datetime import date
    
    # 基准日期
    base_date = date(1989, 12, 12)
    base_gan_idx = TIANGAN.index("丙")
    base_zhi_idx = DIZHI.index("午")
    
    target_date = date(year, month, day)
    days_diff = (target_date - base_date).days
    
    gan_index = (base_gan_idx + days_diff) % 10
    zhi_index = (base_zhi_idx + days_diff) % 12
    
    return TIANGAN[gan_index], DIZHI[zhi_index]


def get_hour_ganzhi(day_gan: str, hour: int) -> Tuple[str, str]:
    """根据日干和小时获取时柱天干地支"""
    shichen = get_shichen(hour)
    zhi_index = DIZHI.index(shichen)
    
    # 日上起时法
    # 甲己还加甲，乙庚丙作初
    # 丙辛从戊起，丁壬庚子居
    # 戊癸何方发，壬子是真途
    
    day_start_map = {
        "甲": "甲", "己": "甲",
        "乙": "丙", "庚": "丙",
        "丙": "戊", "辛": "戊",
        "丁": "庚", "壬": "庚",
        "戊": "壬", "癸": "壬"
    }
    
    start_gan = day_start_map.get(day_gan, "甲")
    start_index = TIANGAN.index(start_gan)
    
    gan_index = (start_index + zhi_index) % 10
    
    return TIANGAN[gan_index], shichen


def calculate_wuxing_distribution(bazi: Dict[str, Tuple[str, str]]) -> Dict[str, int]:
    """计算八字中五行的分布情况"""
    wuxing_count = {"金": 0, "木": 0, "水": 0, "火": 0, "土": 0}
    
    for position, (gan, zhi) in bazi.items():
        # 天干五行
        wuxing_count[TIANGAN_WUXING[gan]] += 1
        # 地支五行
        wuxing_count[DIZHI_WUXING[zhi]] += 1
    
    return wuxing_count


def analyze_wuxing(wuxing_count: Dict[str, int]) -> Dict[str, any]:
    """分析五行旺衰和缺失"""
    total = sum(wuxing_count.values())
    average = total / 5
    
    analysis = {
        "counts": wuxing_count,
        "total": total,
        "strong": [],  # 偏旺
        "weak": [],    # 偏弱
        "missing": [], # 缺失
        "balanced": [] # 适中
    }
    
    for wx, count in wuxing_count.items():
        if count == 0:
            analysis["missing"].append(wx)
        elif count > average + 0.5:
            analysis["strong"].append(wx)
        elif count < average - 0.5:
            analysis["weak"].append(wx)
        else:
            analysis["balanced"].append(wx)
    
    return analysis


def get_xiyongshen(day_master: str, wuxing_analysis: Dict) -> List[str]:
    """根据日主和五行分析推算喜用神"""
    day_wuxing = TIANGAN_WUXING[day_master]
    
    # 简化的喜用神推算逻辑
    xiyongshen = []
    
    # 如果某五行过旺，需要泄或克
    if wuxing_analysis["strong"]:
        for wx in wuxing_analysis["strong"]:
            if wx == "木":
                xiyongshen.extend(["火", "金"])
            elif wx == "火":
                xiyongshen.extend(["土", "水"])
            elif wx == "土":
                xiyongshen.extend(["金", "木"])
            elif wx == "金":
                xiyongshen.extend(["水", "火"])
            elif wx == "水":
                xiyongshen.extend(["木", "土"])
    
    # 如果某五行缺失，需要补
    if wuxing_analysis["missing"]:
        xiyongshen.extend(wuxing_analysis["missing"])
    
    # 去重并保持顺序
    seen = set()
    result = []
    for x in xiyongshen:
        if x not in seen:
            seen.add(x)
            result.append(x)
    
    return result


def calculate_bazi(year: int, month: int, day: int, hour: int) -> Dict:
    """计算完整八字"""
    # 年柱
    year_gan, year_zhi = get_year_ganzhi(year)
    
    # 月柱（简化处理，假设输入的是农历月份）
    month_gan, month_zhi = get_month_ganzhi(year_gan, month)
    
    # 日柱
    day_gan, day_zhi = get_day_ganzhi(year, month, day)
    
    # 时柱
    hour_gan, hour_zhi = get_hour_ganzhi(day_gan, hour)
    
    bazi = {
        "年柱": (year_gan, year_zhi),
        "月柱": (month_gan, month_zhi),
        "日柱": (day_gan, day_zhi),
        "时柱": (hour_gan, hour_zhi)
    }
    
    # 计算纳音
    nayin_ganzhi = year_gan + year_zhi
    nayin = NAYIN_TABLE.get(nayin_ganzhi, "未知")
    
    # 五行分析
    wuxing_count = calculate_wuxing_distribution(bazi)
    wuxing_analysis = analyze_wuxing(wuxing_count)
    
    # 喜用神
    xiyongshen = get_xiyongshen(day_gan, wuxing_analysis)
    
    return {
        "bazi": bazi,
        "nayin": nayin,
        "day_master": day_gan,
        "wuxing_count": wuxing_count,
        "wuxing_analysis": wuxing_analysis,
        "xiyongshen": xiyongshen
    }


def format_bazi_result(result: Dict) -> str:
    """格式化八字分析结果"""
    bazi = result["bazi"]
    
    output = []
    output.append("=" * 40)
    output.append("五行命理分析报告")
    output.append("=" * 40)
    output.append("")
    
    # 八字
    output.append("【八字排盘】")
    for position, (gan, zhi) in bazi.items():
        output.append(f"  {position}：{gan}{zhi} ({TIANGAN_WUXING[gan]}{DIZHI_WUXING[zhi]})")
    output.append("")
    
    # 纳音
    output.append(f"【本命纳音】{result['nayin']}")
    output.append("")
    
    # 日主
    day_master = result["day_master"]
    output.append(f"【日主】{day_master} ({TIANGAN_WUXING[day_master]})")
    output.append("")
    
    # 五行分布
    output.append("【五行分布】")
    for wx, count in result["wuxing_count"].items():
        bar = "█" * count + "░" * (4 - count)
        output.append(f"  {wx}：{bar} ({count}个)")
    output.append("")
    
    # 五行分析
    analysis = result["wuxing_analysis"]
    output.append("【五行分析】")
    if analysis["strong"]:
        output.append(f"  偏旺：{', '.join(analysis['strong'])}")
    if analysis["weak"]:
        output.append(f"  偏弱：{', '.join(analysis['weak'])}")
    if analysis["missing"]:
        output.append(f"  缺失：{', '.join(analysis['missing'])}")
    if analysis["balanced"]:
        output.append(f"  适中：{', '.join(analysis['balanced'])}")
    output.append("")
    
    # 喜用神
    output.append(f"【喜用神】{', '.join(result['xiyongshen'])}")
    output.append("")
    
    # 性格特征（简化版）
    output.append("【性格特征】")
    day_wx = TIANGAN_WUXING[day_master]
    if day_wx == "金":
        output.append("  为人刚毅果断，重义气，有决断力")
    elif day_wx == "木":
        output.append("  为人仁慈正直，有同情心，善于规划")
    elif day_wx == "水":
        output.append("  为人聪明灵活，善于应变，有谋略")
    elif day_wx == "火":
        output.append("  为人热情开朗，积极向上，有领导力")
    elif day_wx == "土":
        output.append("  为人稳重踏实，诚信可靠，有包容心")
    output.append("")
    
    output.append("=" * 40)
    
    return "\n".join(output)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 5:
        print("用法: python calculate_wuxing.py <年> <月> <日> <时>")
        print("示例: python calculate_wuxing.py 1995 8 20 7")
        sys.exit(1)
    
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    day = int(sys.argv[3])
    hour = int(sys.argv[4])
    
    result = calculate_bazi(year, month, day, hour)
    print(format_bazi_result(result))
