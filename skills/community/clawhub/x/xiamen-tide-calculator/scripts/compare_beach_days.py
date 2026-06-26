#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
厦门赶海日期比较器
比较多日赶海评分，推荐最佳赶海日期（支持闰月）

版权信息：
    Copyright (c) 2026 柯英杰
    许可协议：MIT License
    
    作者：柯英杰
    创建日期：2026年4月2日
    最后更新：2026年4月3日
    
    GitHub: https://github.com/kingwingshome/xiamen-tide-calculator
    
免责声明：
    本程序基于厦门海域标准潮汐计算公式，仅供参考。实际潮汐时间可能受
    天气、气压、地形等因素影响。赶海活动存在风险，请务必注意安全。
    使用本程序进行赶海活动，用户需自行承担风险。
"""

import argparse
import sys
import zhdate
from datetime import datetime
from tide_calculator import calculate_tide, get_season_info, get_location_recommendation


def compare_beach_days(lunar_month, start_day, num_days=7, lunar_year=None):
    """
    比较多日赶海评分（支持闰月）

    参数:
        lunar_month: 农历月份
        start_day: 起始农历日期
        num_days: 比较天数
        lunar_year: 农历年（默认为当年）

    返回:
        按评分排序的日期列表
    """
    results = []

    if lunar_year is None:
        lunar_year = datetime.now().year

    for day_offset in range(num_days):
        lunar_day = start_day + day_offset

        # 检查日期是否有效
        if lunar_day > 30:
            break

        # 检查是否为闰月
        try:
            lunar_date = zhdate.ZhDate(lunar_year, lunar_month, lunar_day)
            is_leap = lunar_date.leap_month
        except:
            is_leap = False

        tide_info = calculate_tide(lunar_day, is_leap)

        results.append({
            'lunar_day': lunar_day,
            'lunar_month': lunar_month,
            'lunar_year': lunar_year,
            'is_leap_month': is_leap,
            'score': tide_info['beach_score'],
            'rating': tide_info['beach_rating'],
            'tide_size': tide_info['tide_size'],
            'beach_windows': tide_info['beach_windows'],
            'low1': tide_info['low1'],
            'low2': tide_info['low2']
        })

    # 按评分降序排序
    results.sort(key=lambda x: x['score'], reverse=True)

    return results


def format_comparison_output(results):
    """
    格式化多日比较输出（支持闰月）
    """
    output = []

    output.append(f"【未来{len(results)}天赶海推荐】")
    output.append("")

    # 分组显示
    strong_recommend = [r for r in results if r['rating'] == '强烈推荐']
    recommend = [r for r in results if r['rating'] == '推荐']
    average = [r for r in results if r['rating'] == '一般']
    not_recommend = [r for r in results if r['rating'] == '不推荐']

    if strong_recommend:
        output.append("🌟 强烈推荐：")
        for r in strong_recommend:
            season_name, _, season_desc = get_season_info()
            season_bonus = "1.0" if season_name in ['春季', '秋季'] else "0.7"
            score_reason = f"大潮 + 白天低潮 + {season_name}加成({season_bonus}分)"

            month_str = f"闰{r['lunar_month']}月" if r['is_leap_month'] else f"{r['lunar_month']}月"
            output.append(f"  - 农历{r['lunar_year']}年{month_str}{r['lunar_day']}日 - 评分：{r['score']}分")
            output.append(f"    理由：{score_reason}")
            output.append(f"    最佳赶海：{r['beach_windows'][0]}（窗口1）、{r['beach_windows'][1]}（窗口2）")
            output.append(f"    低潮时间：{r['low1']}、{r['low2']}")

            # 推荐地点
            locations = get_location_recommendation(r['tide_size'], r['is_leap_month'])
            output.append(f"    推荐地点：{locations[0]}")
            output.append("")

    if recommend:
        output.append("✅ 推荐：")
        for r in recommend:
            month_str = f"闰{r['lunar_month']}月" if r['is_leap_month'] else f"{r['lunar_month']}月"
            output.append(f"  - 农历{r['lunar_year']}年{month_str}{r['lunar_day']}日 - 评分：{r['score']}分")
            output.append(f"    理由：{r['tide_size']} + 时间窗口较好")
            output.append(f"    最佳赶海：{r['beach_windows'][0]}、{r['beach_windows'][1]}")
            output.append(f"    低潮时间：{r['low1']}、{r['low2']}")
            locations = get_location_recommendation(r['tide_size'], r['is_leap_month'])
            output.append(f"    推荐地点：{locations[0]}")
            output.append("")

    if average:
        output.append("⚠️ 一般：")
        for r in average:
            month_str = f"闰{r['lunar_month']}月" if r['is_leap_month'] else f"{r['lunar_month']}月"
            output.append(f"  - 农历{r['lunar_year']}年{month_str}{r['lunar_day']}日 - 评分：{r['score']}分")
            output.append(f"    理由：{r['tide_size']} + 条件一般")
            output.append(f"    最佳赶海：{r['beach_windows'][0]}、{r['beach_windows'][1]}")
            output.append(f"    低潮时间：{r['low1']}、{r['low2']}")
            output.append("")

    if not_recommend:
        output.append("❌ 不推荐：")
        for r in not_recommend:
            month_str = f"闰{r['lunar_month']}月" if r['is_leap_month'] else f"{r['lunar_month']}月"
            output.append(f"  - 农历{r['lunar_year']}年{month_str}{r['lunar_day']}日 - 评分：{r['score']}分")
            output.append(f"    理由：{r['tide_size']}，生物较少")
            output.append(f"    建议：等待大潮再赶海")
            output.append("")

    # 总结
    output.append("📊 总结：")
    best = results[0]
    month_str = f"闰{best['lunar_month']}月" if best['is_leap_month'] else f"{best['lunar_month']}月"
    output.append(f"  - 最佳赶海日期：农历{best['lunar_year']}年{month_str}{best['lunar_day']}日（{best['score']}分）")
    output.append(f"  - 强烈推荐天数：{len(strong_recommend)}天")
    output.append(f"  - 推荐天数：{len(recommend)}天")
    output.append(f"  - 一般天数：{len(average)}天")
    output.append(f"  - 不推荐天数：{len(not_recommend)}天")

    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(description='厦门赶海日期比较器')
    parser.add_argument('--lunar-month', type=int, required=True, help='农历月份（1-12）')
    parser.add_argument('--start-day', type=int, required=True, help='起始农历日期（1-30）')
    parser.add_argument('--days', type=int, default=7, help='比较天数，默认7天')

    args = parser.parse_args()

    if not 1 <= args.start_day <= 30:
        sys.stdout.reconfigure(encoding='utf-8')
        print("错误：起始农历日期必须在1-30之间")
        return 1

    if args.days < 1 or args.days > 30:
        sys.stdout.reconfigure(encoding='utf-8')
        print("错误：比较天数必须在1-30之间")
        return 1

    # 比较多日
    results = compare_beach_days(args.lunar_month, args.start_day, args.days)

    # 格式化输出
    output = format_comparison_output(results)
    sys.stdout.reconfigure(encoding='utf-8')
    print(output)

    return 0


if __name__ == '__main__':
    sys.exit(main())
