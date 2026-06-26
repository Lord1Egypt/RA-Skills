#!/usr/bin/env python3
"""盲盒旅行预算分配器（放松版）

根据总预算和天数，随机分配住宿、餐饮、交通、娱乐等各项花费。
支持输出 JSON 格式和人类可读格式。
支持预订跟踪功能。
"""

import random
import json
import sys
from typing import Dict, Union, List, Optional
from datetime import datetime


def allocate_budget(total_budget: float, days: int) -> Dict[str, Union[float, int, dict]]:
    """
    随机分配旅行预算
    
    Args:
        total_budget: 总预算（元）
        days: 游玩天数
    
    Returns:
        预算分配字典，包含各项预算金额和占比
    """
    # 生成随机比例（确保总和为 100%）
    accommodation_ratio = random.uniform(0.35, 0.45)
    food_ratio = random.uniform(0.20, 0.30)
    transport_ratio = random.uniform(0.15, 0.25)
    entertainment_ratio = 1 - accommodation_ratio - food_ratio - transport_ratio
    
    # 计算每日住宿预算（按天数 -1 晚计算）
    nights = days - 1 if days > 1 else 1
    per_night_budget = (total_budget * accommodation_ratio) / nights
    
    # 计算各项预算
    allocation = {
        'total_budget': total_budget,
        'days': days,
        'nights': nights,
        'accommodation': round(total_budget * accommodation_ratio, 2),
        'food': round(total_budget * food_ratio, 2),
        'transport': round(total_budget * transport_ratio, 2),
        'entertainment': round(total_budget * entertainment_ratio, 2),
        'per_day_total': round(total_budget / days, 2),
        'per_night_accommodation': round(per_night_budget, 2)
    }
    
    # 添加比例信息（百分比）
    allocation['ratios_percent'] = {
        'accommodation': round(accommodation_ratio * 100, 1),
        'food': round(food_ratio * 100, 1),
        'transport': round(transport_ratio * 100, 1),
        'entertainment': round(entertainment_ratio * 100, 1)
    }
    
    # 添加每日细分预算
    allocation['daily_breakdown'] = {
        'food_per_day': round(allocation['food'] / days, 2),
        'transport_per_day': round(allocation['transport'] / days, 2),
        'entertainment_per_day': round(allocation['entertainment'] / days, 2)
    }
    
    return allocation


class BookingTracker:
    """预订信息跟踪器"""
    
    def __init__(self):
        self.bookings = {
            'hotels': [],
            'transportation': [],
            'attractions': []
        }
    
    def add_hotel_booking(self, name: str, address: str, check_in: str, check_out: str, 
                         price_per_night: float, room_type: str, confirmation_number: str):
        """添加酒店预订"""
        self.bookings['hotels'].append({
            'name': name,
            'address': address,
            'check_in': check_in,
            'check_out': check_out,
            'price_per_night': price_per_night,
            'room_type': room_type,
            'confirmation_number': confirmation_number,
            'total_price': price_per_night * ((datetime.strptime(check_out, '%Y-%m-%d') - 
                                               datetime.strptime(check_in, '%Y-%m-%d')).days)
        })
    
    def add_transportation_booking(self, type: str, number: str, departure_time: str, 
                                   arrival_time: str, seat_class: str, price: float, 
                                   confirmation_number: str):
        """添加交通预订（返程）"""
        self.bookings['transportation'].append({
            'type': type,  # 'flight' or 'train'
            'number': number,
            'departure_time': departure_time,
            'arrival_time': arrival_time,
            'seat_class': seat_class,
            'price': price,
            'confirmation_number': confirmation_number
        })
    
    def add_attraction_booking(self, name: str, date: str, time_slot: str, 
                               price: float, status: str = '已预订'):
        """添加景点门票预订"""
        self.bookings['attractions'].append({
            'name': name,
            'date': date,
            'time_slot': time_slot,
            'price': price,
            'status': status
        })
    
    def get_total_booked(self) -> float:
        """计算已预订总额"""
        total = 0
        for hotel in self.bookings['hotels']:
            total += hotel['total_price']
        for transport in self.bookings['transportation']:
            total += transport['price']
        for attraction in self.bookings['attractions']:
            total += attraction['price']
        return total
    
    def generate_itinerary_summary(self) -> str:
        """生成行程摘要（用于行程表）"""
        lines = []
        lines.append("## 🎫 已确认预订信息\n")
        
        # 酒店
        if self.bookings['hotels']:
            lines.append("### 🏨 住宿")
            lines.append("| 日期 | 酒店名称 | 地址 | 房型 | 价格 | 确认号 |")
            lines.append("|------|---------|------|------|------|--------|")
            for hotel in self.bookings['hotels']:
                dates = f"{hotel['check_in']}-{hotel['check_out']}"
                lines.append(f"| {dates} | {hotel['name']} | {hotel['address']} | "
                           f"{hotel['room_type']} | {hotel['price_per_night']}元/晚 | "
                           f"{hotel['confirmation_number']} |")
            lines.append("")
        
        # 交通
        if self.bookings['transportation']:
            lines.append("### ✈️ 返程交通")
            lines.append("| 日期 | 班次 | 出发时间 | 到达时间 | 座位 | 价格 | 确认号 |")
            lines.append("|------|------|---------|---------|------|------|--------|")
            for transport in self.bookings['transportation']:
                icon = "✈️" if transport['type'] == 'flight' else "🚄"
                lines.append(f"| - | {icon} {transport['number']} | {transport['departure_time']} | "
                           f"{transport['arrival_time']} | {transport['seat_class']} | "
                           f"{transport['price']}元 | {transport['confirmation_number']} |")
            lines.append("")
        
        # 景点
        if self.bookings['attractions']:
            lines.append("### 🎟️ 景点门票")
            lines.append("| 日期 | 景点 | 时间 | 票价 | 状态 |")
            lines.append("|------|------|------|------|------|")
            for attraction in self.bookings['attractions']:
                lines.append(f"| {attraction['date']} | {attraction['name']} | "
                           f"{attraction['time_slot']} | {attraction['price']}元 | "
                           f"{attraction['status']} |")
            lines.append("")
        
        # 总计
        total = self.get_total_booked()
        lines.append(f"**已预订总额**：{total:.2f}元\n")
        
        return "\n".join(lines)


def format_budget_report(allocation: Dict) -> str:
    """
    格式化预算报告为人类可读文本
    
    Args:
        allocation: 预算分配字典
    
    Returns:
        格式化的预算报告文本
    """
    report = []
    report.append("=" * 60)
    report.append("🎁 盲盒旅行预算分配方案")
    report.append("=" * 60)
    report.append(f"总预算：¥{allocation['total_budget']:.2f}")
    report.append(f"游玩天数：{allocation['days']}天 {allocation['nights']}晚")
    report.append(f"日均预算：¥{allocation['per_day_total']:.2f}/天")
    report.append("")
    report.append("📊 预算分配明细")
    report.append("-" * 60)
    
    items = [
        ('🏨 住宿', allocation['accommodation'], allocation['ratios_percent']['accommodation']),
        ('🍜 餐饮', allocation['food'], allocation['ratios_percent']['food']),
        ('🚗 交通', allocation['transport'], allocation['ratios_percent']['transport']),
        ('🎢 娱乐', allocation['entertainment'], allocation['ratios_percent']['entertainment']),
    ]
    
    for name, amount, ratio in items:
        bar_length = int(ratio / 2)
        bar = '█' * bar_length + '░' * (50 - bar_length)
        report.append(f"{name:8} ¥{amount:>10.2f} ({ratio:5.1f}%) [{bar}]")
    
    report.append("")
    report.append("📅 每日预算参考")
    report.append("-" * 60)
    report.append(f"住宿：¥{allocation['per_night_accommodation']:.2f}/晚")
    report.append(f"餐饮：¥{allocation['daily_breakdown']['food_per_day']:.2f}/天")
    report.append(f"交通：¥{allocation['daily_breakdown']['transport_per_day']:.2f}/天")
    report.append(f"娱乐：¥{allocation['daily_breakdown']['entertainment_per_day']:.2f}/天")
    report.append("")
    report.append("=" * 60)
    report.append("💡 提示：这是随机分配的盲盒预算，实际花费可根据情况调整")
    report.append("=" * 60)
    
    return "\n".join(report)


def main():
    """命令行入口"""
    if len(sys.argv) < 3:
        print("使用方法:")
        print("  python budget_allocator.py <总预算> <天数> [输出格式]")
        print("")
        print("参数说明:")
        print("  总预算：数字，单位元（如 2000）")
        print("  天数：整数（如 3）")
        print("  输出格式：json 或 text（默认 text）")
        print("")
        print("示例:")
        print("  python budget_allocator.py 2000 3")
        print("  python budget_allocator.py 2000 3 json")
        sys.exit(1)
    
    try:
        total_budget = float(sys.argv[1])
        days = int(sys.argv[2])
        output_format = sys.argv[3] if len(sys.argv) > 3 else 'text'
    except ValueError as e:
        print(f"错误：参数格式不正确 - {e}")
        sys.exit(1)
    
    if total_budget <= 0:
        print("错误：预算必须是正数")
        sys.exit(1)
    
    if days < 1:
        print("错误：天数必须至少为 1")
        sys.exit(1)
    
    # 生成预算分配
    allocation = allocate_budget(total_budget, days)
    
    # 输出结果
    if output_format == 'json':
        print(json.dumps(allocation, indent=2, ensure_ascii=False))
    else:
        print(format_budget_report(allocation))


if __name__ == '__main__':
    main()
