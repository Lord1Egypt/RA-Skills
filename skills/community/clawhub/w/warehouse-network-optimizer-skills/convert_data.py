#!/usr/bin/env python3
"""
数据转换脚本 - 将Excel数据转换为JSON格式
用法: python3 convert_data.py --trunk <干线Excel> --distribution <共配Excel>

依赖: pip install pandas openpyxl

⚠️ 智能单位检测：
  1. 优先从表头/备注读取单位标识
  2. 根据数据特征（速度计算）自动推断
  3. 无法确定时提示用户
"""

import pandas as pd
import json
import re
import argparse
import os


def detect_time_unit(df, efficiency_col=12, distance_col=6):
    """
    智能检测时效单位（小时/天）
    
    检测策略：
    1. 搜索表头、备注中是否包含"小时"、"天"、"h"、"d"等标识
    2. 根据速度计算推断（合理速度约30-80km/h）
    """
    # 策略1: 搜索表头中的单位标识
    for row_idx in range(min(5, len(df))):
        for col_idx in range(len(df.columns)):
            val = str(df.iloc[row_idx, col_idx]).lower()
            if '小时' in val or 'h' in val or 'hr' in val:
                print(f'  [检测] 表头发现小时标识: {val}')
                return 'hours'
            if ('天' in val and '每' not in val) or val in ['d', 'day']:
                print(f'  [检测] 表头发现天标识: {val}')
                return 'days'
    
    # 策略2: 搜索"在途时效"附近列是否有单位
    for col_idx in range(max(0, efficiency_col-2), min(len(df.columns), efficiency_col+3)):
        for row_idx in range(min(5, len(df))):
            val = str(df.iloc[row_idx, col_idx]).lower()
            if '小时' in val or 'h' in val:
                print(f'  [检测] 时效列附近发现小时标识: {val}')
                return 'hours'
    
    # 策略3: 根据速度计算推断
    print('  [检测] 尝试根据速度计算推断单位...')
    speeds_hours = []
    speeds_days = []
    
    for idx in range(3, min(20, len(df))):
        distance = df.iloc[idx, distance_col]
        efficiency = df.iloc[idx, efficiency_col]
        if pd.isna(distance) or pd.isna(efficiency):
            continue
        try:
            dist = float(distance)
            eff = float(efficiency)
            if eff > 0 and dist > 0:
                speed_per_hour = dist / eff  # 如果efficiency是小时
                speed_per_day = dist / eff    # 如果efficiency是天
                speeds_hours.append(speed_per_hour)
                speeds_days.append(speed_per_day)
        except:
            continue
    
    if speeds_hours and speeds_days:
        avg_speed_hour = sum(speeds_hours) / len(speeds_hours)
        avg_speed_day = sum(speeds_days) / len(speeds_days)
        
        print(f'  [检测] 如果是小时: 平均速度 = {avg_speed_hour:.1f} km/h')
        print(f'  [检测] 如果是天:   平均速度 = {avg_speed_day:.1f} km/天')
        
        # 判断哪个更合理
        # 干线运输合理速度: 30-80 km/h（考虑堵车、装卸等）
        # 如果是天: 应该 > 500 km/天 才合理
        if 20 < avg_speed_hour < 100:
            print(f'  [检测] 推断结果: 小时 ✅ (速度 {avg_speed_hour:.1f} km/h 合理)')
            return 'hours'
        elif avg_speed_day > 300:
            print(f'  [检测] 推断结果: 天 ✅ (速度 {avg_speed_day:.1f} km/天 合理)')
            return 'days'
        else:
            print(f'  [检测] 两种都有可能，请人工确认')
            # 默认假设为小时（从业务角度更常见）
            return 'hours'
    
    # 默认返回小时
    print('  [检测] 无法确定，默认假设为小时')
    return 'hours'


def convert_trunk_lines(excel_path):
    """转换干线数据"""
    print(f'转换干线数据: {excel_path}')
    df = pd.read_excel(excel_path, header=None)
    
    warehouse_map = {
        '合肥': 1, '南京': 2, '郑州': 3, '杭州': 4, '济南': 5,
        '上海': 6, '西安': 7, '天津': 8, '沈阳': 9, '武汉': 10,
        '长沙': 11, '北京': 12, '成都': 13, '石家庄': 14, '乌鲁木齐': 15,
        '太原': 16, '哈尔滨': 17, '泉州': 18, '南昌': 19, '兰州': 20,
        '广州': 21, '鹿邑': 22, '长春': 23
    }
    
    # ⭐ 智能检测单位
    print('检测时效单位...')
    time_unit = detect_time_unit(df)
    
    def convert_shipping_days(s):
        if pd.isna(s): return '1,2,3,4,5,6,7'
        s = str(s).replace(' ', '')
        days = []
        if '周一' in s or '一' in s: days.append(1)
        if '周二' in s or '二' in s: days.append(2)
        if '周三' in s or '三' in s: days.append(3)
        if '周四' in s or '四' in s: days.append(4)
        if '周五' in s or '五' in s: days.append(5)
        if '周六' in s or '六' in s: days.append(6)
        if '周日' in s or '七' in s: days.append(7)
        return ','.join(map(str, sorted(set(days)))) if days else '1,2,3,4,5,6,7'
    
    def convert_efficiency(s):
        """转换时效值"""
        if pd.isna(s): return 1.0
        try:
            value = float(s)
            if time_unit == 'hours':
                return round(value / 24, 3)  # 小时转天
            else:
                return value  # 已经是天
        except:
            return 1.0
    
    records = []
    for idx, row in df.iterrows():
        if idx < 3: continue
        from_wh = str(row[3]).strip() if pd.notna(row[3]) else None
        to_wh = str(row[4]).strip() if pd.notna(row[4]) else None
        if not from_wh or not to_wh: continue
        
        from_id = warehouse_map.get(from_wh, 99)
        to_id = warehouse_map.get(to_wh, 99)
        hours = float(row[12]) if pd.notna(row[12]) else 24
        
        records.append({
            'id': len(records) + 1,
            'from_house_id': from_id,
            'from_house_name': f'{from_wh}仓',
            'to_house_id': to_id,
            'to_house_name': f'{to_wh}仓',
            'line_name': f'{from_wh}-{to_wh}',
            'distance': int(row[6]) if pd.notna(row[6]) else 0,
            'efficiency_original': hours,  # 原始值
            'efficiency': convert_efficiency(row[12]),  # 转换后
            'time_unit': time_unit,  # ⭐ 记录检测到的单位
            'shipping_days': convert_shipping_days(row[7]),
            'transport_mode': str(row[1]) if pd.notna(row[1]) else '单程',
            'line_type': '调拨'
        })
    
    return {'trunk_lines': records, 'time_unit': time_unit}


def convert_distribution_cycles(excel_path):
    """转换共配数据"""
    print(f'转换共配数据: {excel_path}')
    xlsx = pd.ExcelFile(excel_path)
    
    warehouse_map = {
        '长沙': '长沙仓', '济南': '济南仓', '沈阳': '沈阳仓', '武汉': '武汉仓',
        '西安': '西安仓', '南昌': '南昌仓', '天津': '天津仓', '太原': '太原仓',
        '广州': '广州仓', '北京': '北京仓', '合肥': '合肥仓', '郑州': '郑州仓',
        '石家庄': '石家庄仓', '哈尔滨': '哈尔滨仓', '南京': '南京仓', '杭州': '杭州仓',
        '上海': '上海仓', '泉州': '泉州仓', '兰州': '兰州仓', '成都': '成都仓'
    }
    
    weekday_map = {'周一': 1, '周二': 2, '周三': 3, '周四': 4, '周五': 5, '周六': 6, '周日': 7}
    
    def convert_efficiency(s):
        if pd.isna(s): return 1
        nums = re.findall(r'\d+', str(s))
        return int(nums[0]) if nums else 1
    
    all_records = []
    
    for sheet in xlsx.sheet_names:
        df = pd.read_excel(xlsx, sheet_name=sheet, header=None)
        warehouse_name = warehouse_map.get(sheet, f'{sheet}仓')
        
        header_row, monday_col = None, None
        for idx in range(min(5, len(df))):
            for col in range(len(df.columns)):
                if str(df.iloc[idx, col]).strip() == '周一':
                    header_row, monday_col = idx, col
                    break
            if monday_col: break
        
        if monday_col is None: continue
        
        eff_col = monday_col - 2
        current_province, current_city = None, None
        
        for idx in range(header_row + 1, len(df)):
            row = df.iloc[idx]
            if pd.notna(row[0]) and str(row[0]).strip():
                current_province = str(row[0]).strip()
            if pd.notna(row[1]) and str(row[1]).strip():
                current_city = str(row[1]).strip()
            if current_province is None or current_city is None: continue
            
            area = str(row[2]).strip() if pd.notna(row[2]) else '全区域'
            efficiency = convert_efficiency(row[eff_col]) if eff_col < len(row) else 1
            
            shipping_dates = []
            for offset, name in enumerate(['周一', '周二', '周三', '周四', '周五', '周六', '周日']):
                col = monday_col + offset
                if col < len(row) and pd.notna(row[col]):
                    val = str(row[col]).strip()
                    if val and val not in ['NaN'] and ('周' in val or val in ['√', 'V', 'v', 'Y', 'y']):
                        shipping_dates.append(weekday_map[name])
            
            if shipping_dates:
                all_records.append({
                    'start_house_name': warehouse_name,
                    'province_name': current_province,
                    'city_name': current_city,
                    'area_name': area,
                    'efficiency': efficiency,
                    'shipping_date': ','.join(map(str, sorted(set(shipping_dates))))
                })
    
    return {'distribution_cycles': all_records}


def main():
    parser = argparse.ArgumentParser(description='数据转换工具')
    parser.add_argument('--trunk', help='干线数据Excel文件')
    parser.add_argument('--distribution', help='共配数据Excel文件（多Sheet）')
    parser.add_argument('--output-dir', default='.', help='输出目录')
    args = parser.parse_args()
    
    if args.trunk:
        data = convert_trunk_lines(args.trunk)
        time_unit = data.pop('time_unit')  # 单独记录单位
        output_path = os.path.join(args.output_dir, 'trunk_lines.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f'✅ 干线数据已保存: {output_path} ({len(data["trunk_lines"])} 条)')
        print(f'⚠️ 检测到的时效单位: {time_unit}')
        if time_unit == 'hours':
            print('   已自动转换为天（÷24）')
    
    if args.distribution:
        data = convert_distribution_cycles(args.distribution)
        output_path = os.path.join(args.output_dir, 'distribution_cycles.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f'✅ 共配数据已保存: {output_path} ({len(data["distribution_cycles"])} 条)')
    
    if not args.trunk and not args.distribution:
        print('请指定 --trunk 或 --distribution 参数')


if __name__ == '__main__':
    main()
