#!/usr/bin/env python3
"""
计算时间区间内有多少个工作日的Python脚本
支持排除中国的节假日和调休安排
"""

import datetime
from datetime import date, timedelta
import argparse
import json
import os
import sys

class WorkdayCalculator:
    def __init__(self):
        # 定义周末（0=周一，6=周日）
        self.weekends = {5, 6}  # 周六和周日为周末
        
        # 定义中国的节假日（2025-2026年）
        self.holidays = self._load_holidays()
        
        # 定义调休工作日（本来是周末但需要上班）
        self.extra_workdays = self._load_extra_workdays()
    
    def _load_holidays(self):
        """加载节假日日期"""
        # 2025年节假日
        holidays_2025 = [
            # 元旦
            date(2025, 1, 1),
            # 春节
            date(2025, 1, 28), date(2025, 1, 29), date(2025, 1, 30),
            date(2025, 1, 31), date(2025, 2, 1), date(2025, 2, 2), date(2025, 2, 3),
            # 清明节
            date(2025, 4, 4), date(2025, 4, 5), date(2025, 4, 6),
            # 劳动节
            date(2025, 5, 1), date(2025, 5, 2), date(2025, 5, 3), date(2025, 5, 4), date(2025, 5, 5),
            # 端午节
            date(2025, 5, 31), date(2025, 6, 1), date(2025, 6, 2),
            # 中秋节
            date(2025, 10, 1), date(2025, 10, 2), date(2025, 10, 3),
            # 国庆节
            date(2025, 10, 4), date(2025, 10, 5), date(2025, 10, 6), date(2025, 10, 7),
        ]
        
        # 2026年节假日（根据国务院办公厅通知）
        holidays_2026 = [
            # 元旦：1月1日至3日
            date(2026, 1, 1), date(2026, 1, 2), date(2026, 1, 3),
            
            # 春节：2月15日至23日
            date(2026, 2, 15), date(2026, 2, 16), date(2026, 2, 17),
            date(2026, 2, 18), date(2026, 2, 19), date(2026, 2, 20),
            date(2026, 2, 21), date(2026, 2, 22), date(2026, 2, 23),
            
            # 清明节：4月4日至6日
            date(2026, 4, 4), date(2026, 4, 5), date(2026, 4, 6),
            
            # 劳动节：5月1日至5日
            date(2026, 5, 1), date(2026, 5, 2), date(2026, 5, 3),
            date(2026, 5, 4), date(2026, 5, 5),
            
            # 端午节：6月19日至21日
            date(2026, 6, 19), date(2026, 6, 20), date(2026, 6, 21),
            
            # 中秋节：9月25日至27日
            date(2026, 9, 25), date(2026, 9, 26), date(2026, 9, 27),
            
            # 国庆节：10月1日至7日
            date(2026, 10, 1), date(2026, 10, 2), date(2026, 10, 3),
            date(2026, 10, 4), date(2026, 10, 5), date(2026, 10, 6), date(2026, 10, 7),
        ]
        
        return set(holidays_2025 + holidays_2026)
    
    def _load_extra_workdays(self):
        """加载调休工作日"""
        # 2025年调休工作日
        extra_workdays_2025 = [
            date(2025, 2, 8),   # 春节调休
            date(2025, 2, 15),  # 春节调休
        ]
        
        # 2026年调休工作日
        extra_workdays_2026 = [
            # 春节调休
            date(2026, 2, 14), date(2026, 2, 28),
            
            # 元旦调休
            date(2026, 1, 4),
            
            # 劳动节调休
            date(2026, 4, 26), date(2026, 5, 9),
            
            # 国庆节调休
            date(2026, 9, 26), date(2026, 10, 10),
        ]
        
        return set(extra_workdays_2025 + extra_workdays_2026)
    
    def is_workday(self, day):
        """
        判断某一天是否为工作日
        
        Args:
            day: datetime.date对象
            
        Returns:
            bool: True表示工作日，False表示非工作日
        """
        # 如果是周末
        if day.weekday() in self.weekends:
            # 检查是否为调休工作日
            if day in self.extra_workdays:
                return True
            return False
        
        # 检查是否为节假日
        if day in self.holidays:
            return False
        
        return True
    
    def calculate_workdays(self, start_date, end_date):
        """
        计算两个日期之间的工作日数量
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            int: 工作日数量
        """
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        
        workday_count = 0
        current_date = start_date
        
        while current_date <= end_date:
            if self.is_workday(current_date):
                workday_count += 1
            current_date += timedelta(days=1)
        
        return workday_count
    
    def get_workday_details(self, start_date, end_date):
        """
        获取工作日的详细信息
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            dict: 包含工作日、节假日、周末等信息的字典
        """
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        
        workdays = []
        holidays = []
        weekends = []
        extra_workdays = []
        
        current_date = start_date
        
        while current_date <= end_date:
            is_weekend = current_date.weekday() in self.weekends
            
            if is_weekend:
                if current_date in self.extra_workdays:
                    extra_workdays.append(current_date)
                    workdays.append(current_date)
                else:
                    weekends.append(current_date)
            elif current_date in self.holidays:
                holidays.append(current_date)
            else:
                workdays.append(current_date)
            
            current_date += timedelta(days=1)
        
        return {
            'start_date': start_date,
            'end_date': end_date,
            'workdays': sorted(workdays),
            'holidays': sorted(holidays),
            'weekends': sorted(weekends),
            'extra_workdays': sorted(extra_workdays),
            'total_days': (end_date - start_date).days + 1,
            'workday_count': len(workdays)
        }
    
    def add_holiday(self, holiday_date, holiday_name=None):
        """
        添加节假日
        
        Args:
            holiday_date: 节假日日期
            holiday_name: 节假日名称（可选）
        """
        self.holidays.add(holiday_date)
        
    def remove_holiday(self, holiday_date):
        """
        移除节假日
        
        Args:
            holiday_date: 要移除的节假日日期
        """
        if holiday_date in self.holidays:
            self.holidays.remove(holiday_date)
    
    def add_extra_workday(self, workday_date, description=None):
        """
        添加调休工作日
        
        Args:
            workday_date: 调休工作日日期
            description: 描述信息（可选）
        """
        self.extra_workdays.add(workday_date)

def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description='计算时间区间内有多少个工作日',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s 2025-01-01 2025-01-31
  %(prog)s 2026-02-01 2026-02-28 --details
  %(prog)s 2025-03-01 2025-03-31 --details --export result.json
        """
    )
    
    parser.add_argument(
        'start_date',
        help='开始日期 (格式: YYYY-MM-DD)'
    )
    
    parser.add_argument(
        'end_date',
        help='结束日期 (格式: YYYY-MM-DD)'
    )
    
    parser.add_argument(
        '--details',
        action='store_true',
        help='显示详细信息（工作日、节假日、周末列表）'
    )
    
    parser.add_argument(
        '--export',
        help='导出结果到JSON文件'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Workday Calculator v1.0.0'
    )
    
    return parser.parse_args()

def format_date_list(dates, max_display=10):
    """格式化日期列表显示"""
    if not dates:
        return "无"
    
    if len(dates) <= max_display:
        return "\n".join(f"  {i+1}. {d.strftime('%Y-%m-%d %A')}" for i, d in enumerate(dates))
    else:
        first_part = "\n".join(f"  {i+1}. {d.strftime('%Y-%m-%d %A')}" for i, d in enumerate(dates[:max_display]))
        return f"{first_part}\n  ... 和 {len(dates) - max_display} 个更多日期"

def main():
    """主函数"""
    args = parse_args()
    
    try:
        start_date = datetime.datetime.strptime(args.start_date, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(args.end_date, '%Y-%m-%d').date()
    except ValueError as e:
        print(f"❌ 日期格式错误: {e}")
        print("💡 请使用 YYYY-MM-DD 格式，例如: 2025-01-01")
        sys.exit(1)
    
    # 创建计算器实例
    calculator = WorkdayCalculator()
    
    if args.details:
        # 获取详细信息
        details = calculator.get_workday_details(start_date, end_date)
        
        print("\n" + "="*60)
        print("📅 工作日计算详情")
        print("="*60)
        print(f"📌 时间区间: {start_date} 到 {end_date}")
        print(f"📊 总天数: {details['total_days']}")
        print(f"💼 工作日数量: {details['workday_count']}")
        print(f"🎉 节假日数量: {len(details['holidays'])}")
        print(f"🌴 周末数量: {len(details['weekends'])}")
        print(f"🏢 调休工作日数量: {len(details['extra_workdays'])}")
        
        if details['workdays']:
            print(f"\n💼 工作日列表 ({len(details['workdays'])}天):")
            print(format_date_list(details['workdays']))
        
        if details['holidays']:
            print(f"\n🎉 节假日列表 ({len(details['holidays'])}天):")
            print(format_date_list(details['holidays']))
        
        if details['extra_workdays']:
            print(f"\n🏢 调休工作日列表 ({len(details['extra_workdays'])}天):")
            print(format_date_list(details['extra_workdays']))
        
        # 导出到JSON文件
        if args.export:
            try:
                export_data = {
                    'start_date': details['start_date'].isoformat(),
                    'end_date': details['end_date'].isoformat(),
                    'workdays': [d.isoformat() for d in details['workdays']],
                    'holidays': [d.isoformat() for d in details['holidays']],
                    'weekends': [d.isoformat() for d in details['weekends']],
                    'extra_workdays': [d.isoformat() for d in details['extra_workdays']],
                    'total_days': details['total_days'],
                    'workday_count': details['workday_count'],
                    'generated_at': datetime.datetime.now().isoformat()
                }
                
                with open(args.export, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, ensure_ascii=False, indent=2)
                
                print(f"\n✅ 结果已导出到: {args.export}")
                
            except Exception as e:
                print(f"❌ 导出失败: {e}")
    
    else:
        # 简单计算
        workday_count = calculator.calculate_workdays(start_date, end_date)
        total_days = (end_date - start_date).days + 1
        
        print(f"\n📅 从 {start_date} 到 {end_date}:")
        print(f"📊 总天数: {total_days}")
        print(f"💼 工作日数量: {workday_count}")
        print(f"🎉 非工作日数量: {total_days - workday_count}")

if __name__ == "__main__":
    main()