#!/usr/bin/env python3
"""
节假日数据更新工具
用于更新workday_calculator.py中的节假日数据
"""

import sys
import json
import re
from datetime import date, datetime

def load_current_holidays(script_path):
    """从脚本中加载当前的节假日数据"""
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取节假日数据
        holidays_2025 = extract_holidays(content, 2025)
        holidays_2026 = extract_holidays(content, 2026)
        extra_workdays_2025 = extract_extra_workdays(content, 2025)
        extra_workdays_2026 = extract_extra_workdays(content, 2026)
        
        return {
            'holidays_2025': holidays_2025,
            'holidays_2026': holidays_2026,
            'extra_workdays_2025': extra_workdays_2025,
            'extra_workdays_2026': extra_workdays_2026
        }
        
    except Exception as e:
        print(f"❌ 读取文件失败: {e}")
        return None

def extract_holidays(content, year):
    """从内容中提取指定年份的节假日"""
    pattern = rf'holidays_{year} = \[(.*?)\]'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return []
    
    holidays_text = match.group(1)
    dates = []
    
    # 提取date(YYYY, MM, DD)格式
    date_pattern = r'date\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)'
    for match in re.finditer(date_pattern, holidays_text):
        y, m, d = int(match.group(1)), int(match.group(2)), int(match.group(3))
        if y == year:
            dates.append(date(y, m, d))
    
    return dates

def extract_extra_workdays(content, year):
    """从内容中提取指定年份的调休工作日"""
    pattern = rf'extra_workdays_{year} = \[(.*?)\]'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return []
    
    workdays_text = match.group(1)
    dates = []
    
    # 提取date(YYYY, MM, DD)格式
    date_pattern = r'date\s*\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)'
    for match in re.finditer(date_pattern, workdays_text):
        y, m, d = int(match.group(1)), int(match.group(2)), int(match.group(3))
        if y == year:
            dates.append(date(y, m, d))
    
    return dates

def print_holiday_summary(holidays_data):
    """打印节假日数据摘要"""
    print("\n" + "="*60)
    print("📅 当前节假日数据摘要")
    print("="*60)
    
    for year in [2025, 2026]:
        holidays = holidays_data.get(f'holidays_{year}', [])
        extra_workdays = holidays_data.get(f'extra_workdays_{year}', [])
        
        print(f"\n🎉 {year}年节假日 ({len(holidays)}天):")
        holidays_by_month = {}
        for d in sorted(holidays):
            month = d.month
            if month not in holidays_by_month:
                holidays_by_month[month] = []
            holidays_by_month[month].append(d)
        
        for month in sorted(holidays_by_month.keys()):
            dates = holidays_by_month[month]
            date_str = ", ".join(f"{d.day}日" for d in dates)
            print(f"  {month}月: {date_str}")
        
        if extra_workdays:
            print(f"\n🏢 {year}年调休工作日 ({len(extra_workdays)}天):")
            for d in sorted(extra_workdays):
                print(f"  {d.strftime('%Y-%m-%d %A')}")

def add_holiday_interactive():
    """交互式添加节假日"""
    print("\n" + "="*60)
    print("➕ 添加节假日")
    print("="*60)
    
    try:
        year = input("年份 (例如: 2025): ").strip()
        if not year:
            print("❌ 年份不能为空")
            return None
        
        month = input("月份 (1-12): ").strip()
        if not month:
            print("❌ 月份不能为空")
            return None
        
        day = input("日期 (1-31): ").strip()
        if not day:
            print("❌ 日期不能为空")
            return None
        
        name = input("节假日名称 (可选): ").strip()
        
        holiday_date = date(int(year), int(month), int(day))
        
        print(f"\n✅ 添加的节假日: {holiday_date} ({name if name else '未命名'})")
        
        return {
            'date': holiday_date,
            'name': name,
            'year': int(year)
        }
        
    except ValueError as e:
        print(f"❌ 日期无效: {e}")
        return None
    except Exception as e:
        print(f"❌ 输入错误: {e}")
        return None

def add_extra_workday_interactive():
    """交互式添加调休工作日"""
    print("\n" + "="*60)
    print("➕ 添加调休工作日")
    print("="*60)
    
    try:
        year = input("年份 (例如: 2025): ").strip()
        if not year:
            print("❌ 年份不能为空")
            return None
        
        month = input("月份 (1-12): ").strip()
        if not month:
            print("❌ 月份不能为空")
            return None
        
        day = input("日期 (1-31): ").strip()
        if not day:
            print("❌ 日期不能为空")
            return None
        
        description = input("描述信息 (可选): ").strip()
        
        workday_date = date(int(year), int(month), int(day))
        
        print(f"\n✅ 添加的调休工作日: {workday_date} ({description if description else '无描述'})")
        
        return {
            'date': workday_date,
            'description': description,
            'year': int(year)
        }
        
    except ValueError as e:
        print(f"❌ 日期无效: {e}")
        return None
    except Exception as e:
        print(f"❌ 输入错误: {e}")
        return None

def generate_python_code(holidays_data):
    """生成Python代码"""
    
    print("\n" + "="*60)
    print("🐍 Python代码格式")
    print("="*60)
    
    for year in [2025, 2026]:
        holidays = sorted(holidays_data.get(f'holidays_{year}', []))
        extra_workdays = sorted(holidays_data.get(f'extra_workdays_{year}', []))
        
        print(f"\n# {year}年节假日")
        print(f"holidays_{year} = [")
        for d in holidays:
            print(f"    date({d.year}, {d.month}, {d.day}),")
        print("]")
        
        if extra_workdays:
            print(f"\n# {year}年调休工作日")
            print(f"extra_workdays_{year} = [")
            for d in extra_workdays:
                print(f"    date({d.year}, {d.month}, {d.day}),")
            print("]")

def search_holidays_online():
    """在线搜索节假日信息"""
    print("\n" + "="*60)
    print("🔍 在线搜索节假日信息")
    print("="*60)
    
    print("\n💡 建议访问以下网站获取最新信息：")
    print("1. 中国政府网 (www.gov.cn)")
    print("2. 国务院办公厅节假日安排通知")
    print("3. 百度百科节假日词条")
    print("4. 新华社官方网站")
    
    print("\n📋 常见节假日安排格式：")
    print("元旦：1月1日至3日放假调休，共3天")
    print("春节：2月15日至23日放假调休，共9天")
    print("清明节：4月4日至6日放假，共3天")
    print("劳动节：5月1日至5日放假调休，共5天")
    print("端午节：6月19日至21日放假，共3天")
    print("中秋节：9月25日至27日放假，共3天")
    print("国庆节：10月1日至7日放假调休，共7天")
    
    print("\n⚠️  注意：")
    print("- 请确保信息来源可靠")
    print("- 验证日期是否正确")
    print("- 注意调休工作日的安排")

def main():
    """主函数"""
    print("="*60)
    print("📅 节假日数据更新工具")
    print("="*60)
    
    script_path = "workday_calculator.py"
    
    # 加载当前数据
    holidays_data = load_current_holidays(script_path)
    if not holidays_data:
        print("❌ 无法加载当前节假日数据")
        return
    
    # 打印摘要
    print_holiday_summary(holidays_data)
    
    while True:
        print("\n" + "="*60)
        print("📋 功能菜单")
        print("="*60)
        print("1. 查看当前节假日数据")
        print("2. 添加节假日")
        print("3. 添加调休工作日")
        print("4. 在线搜索节假日信息")
        print("5. 生成Python代码")
        print("6. 退出")
        
        choice = input("\n请选择功能 (1-6): ").strip()
        
        if choice == '1':
            print_holiday_summary(holidays_data)
            
        elif choice == '2':
            holiday_info = add_holiday_interactive()
            if holiday_info:
                year = holiday_info['year']
                date_obj = holiday_info['date']
                key = f'holidays_{year}'
                
                if key not in holidays_data:
                    holidays_data[key] = []
                
                if date_obj not in holidays_data[key]:
                    holidays_data[key].append(date_obj)
                    holidays_data[key].sort()
                    print("✅ 节假日已添加")
                else:
                    print("⚠️  该日期已经是节假日")
            
        elif choice == '3':
            workday_info = add_extra_workday_interactive()
            if workday_info:
                year = workday_info['year']
                date_obj = workday_info['date']
                key = f'extra_workdays_{year}'
                
                if key not in holidays_data:
                    holidays_data[key] = []
                
                if date_obj not in holidays_data[key]:
                    holidays_data[key].append(date_obj)
                    holidays_data[key].sort()
                    print("✅ 调休工作日已添加")
                else:
                    print("⚠️  该日期已经是调休工作日")
            
        elif choice == '4':
            search_holidays_online()
            
        elif choice == '5':
            generate_python_code(holidays_data)
            
        elif choice == '6':
            print("\n👋 退出节假日数据更新工具")
            break
            
        else:
            print("❌ 无效选择，请重新输入")

if __name__ == "__main__":
    main()