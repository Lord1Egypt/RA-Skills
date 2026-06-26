#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
奇门遁甲排盘工具
天工长老开发 v1.0.0

功能：根据时间计算奇门遁甲完整排盘
"""

import argparse
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# ============== 基础数据 ==============

# 八卦先天数
BAGUA_NUM = {
    '乾': 1, '兑': 2, '离': 3, '震': 4,
    '巽': 5, '坎': 6, '艮': 7, '坤': 8
}

# 八卦方位
BAGUA_DIR = {
    '乾': '西北', '兑': '西', '离': '南', '震': '东',
    '巽': '东南', '坎': '北', '艮': '东北', '坤': '西南'
}

# 九宫数
JIUGONG = {
    1: '坎', 2: '坤', 3: '震', 4: '巽',
    5: '中', 6: '乾', 7: '兑', 8: '艮', 9: '离'
}

# 八门
BA_MEN = ['休门', '生门', '伤门', '杜门', '景门', '死门', '惊门', '开门']

# 九星
BA_STAR = ['天蓬', '天芮', '天冲', '天辅', '天禽', '天心', '天柱', '天任', '天英']

# 八神
BA_SHEN = ['值符', '螣蛇', '太阴', '六合', '白虎', '玄武', '九地', '九天']

# 十天干
TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']

# 十二地支
DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

# 节气数据（近似值，用于快速计算）
JIEQI_DATA = {
    # 月令节气
    1: ('小寒', '大寒'),
    2: ('立春', '雨水'),
    3: ('惊蛰', '春分'),
    4: ('清明', '谷雨'),
    5: ('立夏', '小满'),
    6: ('芒种', '夏至'),
    7: ('小暑', '大暑'),
    8: ('立秋', '处暑'),
    9: ('白露', '秋分'),
    10: ('寒露', '霜降'),
    11: ('立冬', '小雪'),
    12: ('大雪', '冬至'),
}

# 阳遁节气（冬至后~芒种）
YANG_DUN_JIEQI = ['冬至', '小寒', '大寒', '立春', '雨水', '惊蛰', '春分', '清明', '谷雨', '立夏', '小满', '芒种']

# 阴遁节气（夏至后~大雪）
YIN_DUN_JIEQI = ['夏至', '小暑', '大暑', '立秋', '处暑', '白露', '秋分', '寒露', '霜降', '立冬', '小雪', '大雪']

# 六甲旬首
LIU_JIA = {
    '甲子': '戊', '甲戌': '己', '甲申': '庚',
    '甲午': '辛', '甲辰': '壬', '甲寅': '癸'
}

# ============== 工具函数 ==============

def get_jieqi(year: int, month: int, day: int) -> Tuple[str, str, bool]:
    """
    计算节气
    返回：(当前节气，下一节气，是否阳遁)
    """
    # 简化计算：根据月份和日期估算节气
    # 实际应用中应使用精确天文算法
    
    # 节气日期近似（每月 6-8 日和 21-23 日）
    if day >= 21 or (day >= 6 and month in [1, 4, 7, 10]):
        # 中气
        jieqi = JIEQI_DATA[month][1] if month <= 12 else JIEQI_DATA[1][1]
    else:
        # 节气
        jieqi = JIEQI_DATA[month][0]
    
    # 判断阴阳遁
    # 冬至后到芒种为阳遁，夏至后到大雪为阴遁
    yang_dun_months = [12, 1, 2, 3, 4, 5, 6]  # 冬至到芒种
    yin_dun_months = [6, 7, 8, 9, 10, 11, 12]  # 夏至到大雪
    
    is_yang_dun = month in yang_dun_months
    if month == 6:
        is_yang_dun = day < 21  # 夏至前阳遁，夏至后阴遁
    elif month == 12:
        is_yang_dun = day >= 21  # 冬至后阳遁
    
    return jieqi, is_yang_dun

def get_yun_type_and_ju(year: int, month: int, day: int, hour: int) -> Tuple[str, int]:
    """
    计算阴阳遁和局数
    返回：(阴阳遁字符串，局数)
    """
    jieqi, is_yang_dun = get_jieqi(year, month, day)
    
    # 简化局数计算（实际应精确到节气和时辰）
    # 这里使用日干支计算
    day_gan_zhi = get_day_gan_zhi(year, month, day)
    day_gan = day_gan_zhi[0]
    
    # 根据日干和节气确定局数
    # 简化算法：用日干序数
    gan_num = TIAN_GAN.index(day_gan) + 1
    
    if is_yang_dun:
        yun_type = f"阳遁"
        ju = (gan_num + month + day) % 9
        if ju == 0:
            ju = 9
    else:
        yun_type = f"阴遁"
        ju = 9 - ((gan_num + month + day) % 9)
        if ju == 0:
            ju = 9
    
    return yun_type, ju

def get_day_gan_zhi(year: int, month: int, day: int) -> str:
    """
    计算日干支（简化算法）
    """
    # 简化计算，实际应使用精确历法
    # 这里用一个基准日推算
    base_year, base_month, base_day = 2026, 1, 1
    base_gan_zhi = 0  # 2026 年 1 月 1 日为甲戌日
    
    # 计算天数差
    from datetime import timedelta
    base_date = datetime(base_year, base_month, base_day)
    target_date = datetime(year, month, day)
    days_diff = (target_date - base_date).days
    
    # 60 甲子循环
    gan_zhi_index = (base_gan_zhi + days_diff) % 60
    
    gan_index = gan_zhi_index % 10
    zhi_index = gan_zhi_index % 12
    
    return TIAN_GAN[gan_index] + DI_ZHI[zhi_index]

def get_hour_gan_zhi(day_gan: str, hour: int) -> str:
    """
    计算时干支
    五鼠遁：甲己还生甲，乙庚丙作初，丙辛从戊起，丁壬庚子居，戊癸何方发，壬子是真途
    """
    # 时辰地支（23-1 子，1-3 丑...）
    hour_zhi_index = ((hour + 1) % 24) // 2
    hour_zhi = DI_ZHI[hour_zhi_index]
    
    # 时干计算
    day_gan_index = TIAN_GAN.index(day_gan)
    
    # 五鼠遁公式
    gan_start = [0, 2, 4, 6, 8][day_gan_index % 5]  # 甲己 0, 乙庚 2, 丙辛 4, 丁壬 6, 戊癸 8
    hour_gan_index = (gan_start + hour_zhi_index) % 10
    
    return TIAN_GAN[hour_gan_index] + hour_zhi

def get_zhi_fu_zhi_shi(ju: int, is_yang_dun: bool) -> Tuple[str, str]:
    """
    计算值符和值使
    """
    # 简化计算
    # 值符：根据局数确定值使门，值符星随之
    zhi_shi_index = (ju - 1) % 8
    zhi_shi = BA_MEN[zhi_shi_index]
    
    # 值符星（与值使门对应）
    zhi_fu_index = zhi_shi_index % 9
    zhi_fu = BA_STAR[zhi_fu_index]
    
    return zhi_fu, zhi_shi

def pai_pan(ju: int, is_yang_dun: bool) -> Dict:
    """
    排九宫盘
    """
    # 简化排盘（实际奇门排盘非常复杂，涉及飞盘、转盘等）
    # 这里提供一个基础框架
    
    pan = {}
    
    # 九宫顺序（洛书顺序）
    gong_order = [4, 9, 2, 3, 5, 7, 8, 1, 6]  # 巽离坤 震中兑 艮坎乾
    
    # 八门排布（根据值使门顺/逆排）
    men_start = BA_MEN.index(get_zhi_fu_zhi_shi(ju, is_yang_dun)[1])
    
    for i, gong_num in enumerate(gong_order):
        gong_name = JIUGONG[gong_num]
        
        # 门
        men_index = (men_start + i) % 8 if is_yang_dun else (men_start - i) % 8
        men = BA_MEN[men_index]
        
        # 星
        star_index = (i + ju - 1) % 9
        star = BA_STAR[star_index]
        
        # 神
        shen_index = i % 8
        shen = BA_SHEN[shen_index]
        
        pan[gong_name] = {
            '门': men,
            '星': star,
            '神': shen
        }
    
    return pan

# ============== 主函数 ==============

def qimen_pan(date_str: Optional[str] = None, timestamp: Optional[int] = None) -> Dict:
    """
    奇门遁甲排盘主函数
    
    参数：
        date_str: 日期字符串 "YYYY-MM-DD HH:MM"
        timestamp: Unix 时间戳
    
    返回：
        排盘结果字典
    """
    # 解析时间
    if timestamp:
        dt = datetime.fromtimestamp(timestamp)
    elif date_str:
        dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    else:
        dt = datetime.now()
    
    year, month, day = dt.year, dt.month, dt.day
    hour = dt.hour
    
    # 计算四柱
    day_gan_zhi = get_day_gan_zhi(year, month, day)
    day_gan = day_gan_zhi[0]
    hour_gan_zhi = get_hour_gan_zhi(day_gan, hour)
    
    # 年柱（简化）
    year_gan_zhi = TIAN_GAN[(year - 4) % 10] + DI_ZHI[(year - 4) % 12]
    
    # 月柱（简化）
    month_gan_zhi = TIAN_GAN[(year - 4) % 10 * 2 + month] + DI_ZHI[month + 2]
    
    # 计算阴阳遁和局数
    yun_type, ju = get_yun_type_and_ju(year, month, day, hour)
    is_yang_dun = '阳' in yun_type
    
    # 值符值使
    zhi_fu, zhi_shi = get_zhi_fu_zhi_shi(ju, is_yang_dun)
    
    # 节气
    jieqi, _ = get_jieqi(year, month, day)
    
    # 排盘
    pan = pai_pan(ju, is_yang_dun)
    
    # 农历（简化显示）
    lunar_month = f"{'正二三四五六七八九十'[month-1]}月"
    lunar_day = f"{'初一初二初三初四初五初六初七初八初九初十十一十二十三十四十五十六十七十八十九二十廿一廿二廿三廿四廿五廿六廿七廿八廿九三十'[day-1]}"
    
    result = {
        '公历时间': f"{year}年{month}月{day}日 {hour}时{dt.minute}分",
        '农历时间': f"{year_gan_zhi}年 {lunar_month} {lunar_day} {hour_gan_zhi}时",
        '节气': jieqi,
        '阴阳遁': f"{yun_type}{ju}局",
        '值符': zhi_fu,
        '值使': zhi_shi,
        '四柱': {
            '年柱': year_gan_zhi,
            '月柱': month_gan_zhi,
            '日柱': day_gan_zhi,
            '时柱': hour_gan_zhi
        },
        '九宫落位': pan
    }
    
    return result

def format_output(result: Dict) -> str:
    """
    格式化输出
    """
    output = []
    output.append("【排盘结果】")
    output.append(f"- 公历时间：{result['公历时间']}")
    output.append(f"- 农历时间：{result['农历时间']}")
    output.append(f"- 节气：{result['节气']}")
    output.append(f"- 阴阳遁：{result['阴阳遁']}")
    output.append(f"- 值符：{result['值符']}")
    output.append(f"- 值使：{result['值使']}")
    output.append("")
    output.append("【四柱】")
    output.append(f"年柱：{result['四柱']['年柱']}  月柱：{result['四柱']['月柱']}  日柱：{result['四柱']['日柱']}  时柱：{result['四柱']['时柱']}")
    output.append("")
    output.append("【九宫落位】")
    output.append("┌─────────┬─────────┬─────────┐")
    
    # 上三宫
    for gong in ['巽', '离', '坤']:
        if gong in result['九宫落位']:
            p = result['九宫落位'][gong]
            output.append(f"│  {gong}四宫  │" if gong == '巽' else f"│  {gong}九宫  │" if gong == '离' else f"│  {gong}二宫  │")
            output.append(f"│  {p['门']:<6}│" if len(p['门']) <= 6 else f"│  {p['门']}│")
    output.append("├─────────┼─────────┼─────────┤")
    
    # 中三宫
    for gong in ['震', '中', '兑']:
        if gong in result['九宫落位']:
            p = result['九宫落位'][gong]
            output.append(f"│  {gong}三宫  │" if gong == '震' else f"│  ({gong}寄宫)│" if gong == '中' else f"│  {gong}七宫  │")
            output.append(f"│  {p['门']:<6}│" if gong != '中' else "│         │")
    output.append("├─────────┼─────────┼─────────┤")
    
    # 下三宫
    for gong in ['艮', '坎', '乾']:
        if gong in result['九宫落位']:
            p = result['九宫落位'][gong]
            output.append(f"│  {gong}八宫  │" if gong == '艮' else f"│  {gong}一宫  │" if gong == '坎' else f"│  {gong}六宫  │")
            output.append(f"│  {p['门']:<6}│" if len(p['门']) <= 6 else f"│  {p['门']}│")
    output.append("└─────────┴─────────┴─────────┘")
    
    output.append("")
    output.append("【用神参考】")
    output.append("- 财运：看生门、戊土")
    output.append("- 事业：看开门、官鬼")
    output.append("- 婚姻：看乙庚、六合")
    output.append("- 健康：看天芮、死门")
    
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description='奇门遁甲排盘工具')
    parser.add_argument('--date', '-d', type=str, help='日期时间 (YYYY-MM-DD HH:MM)')
    parser.add_argument('--timestamp', '-t', type=int, help='Unix 时间戳')
    parser.add_argument('--json', '-j', action='store_true', help='输出 JSON 格式')
    
    args = parser.parse_args()
    
    try:
        result = qimen_pan(args.date, args.timestamp)
        
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(format_output(result))
            
    except Exception as e:
        print(f"排盘错误：{e}")
        return 1
    
    return 0

if __name__ == '__main__':
    exit(main())
