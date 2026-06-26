#!/usr/bin/env python3
"""行程单生成器（放松版）

根据预订信息和初步行程安排，生成可打印的详细行程表。
支持 Markdown 和纯文本格式输出。
"""

import json
import sys
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class ItineraryGenerator:
    """行程单生成器"""
    
    def __init__(self, city: str, start_date: str, days: int, travelers: int = 1):
        self.city = city
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.days = days
        self.travelers = travelers
        self.bookings = {
            'hotels': [],
            'transportation': [],
            'attractions': []
        }
        self.daily_plans = []
    
    def add_hotel_booking(self, name: str, address: str, check_in: str, check_out: str,
                         price_per_night: float, room_type: str, confirmation_number: str,
                         phone: str = ''):
        """添加酒店预订信息"""
        self.bookings['hotels'].append({
            'name': name,
            'address': address,
            'check_in': check_in,
            'check_out': check_out,
            'price_per_night': price_per_night,
            'room_type': room_type,
            'confirmation_number': confirmation_number,
            'phone': phone
        })
    
    def add_transportation_booking(self, type: str, number: str, departure_time: str,
                                   arrival_time: str, seat_class: str, price: float,
                                   confirmation_number: str, from_station: str = '',
                                   to_station: str = ''):
        """添加交通预订信息"""
        self.bookings['transportation'].append({
            'type': type,  # 'flight' or 'train'
            'number': number,
            'departure_time': departure_time,
            'arrival_time': arrival_time,
            'seat_class': seat_class,
            'price': price,
            'confirmation_number': confirmation_number,
            'from_station': from_station,
            'to_station': to_station
        })
    
    def add_attraction_booking(self, name: str, date: str, time_slot: str,
                               price: float, status: str = '已预订'):
        """添加景点门票预订信息"""
        self.bookings['attractions'].append({
            'name': name,
            'date': date,
            'time_slot': time_slot,
            'price': price,
            'status': status
        })
    
    def add_daily_plan(self, day_index: int, date: str, day_name: str, theme: str,
                       activities: List[Dict]):
        """
        添加每日行程计划
        
        Args:
            day_index: 第几天（从 1 开始）
            date: 日期字符串（2026-04-15）
            day_name: 星期几（周三）
            theme: 当日主题（轻松适应/核心体验/返程）
            activities: 活动列表，每个活动包含：
                - time: 时间（如 "10:00"）
                - title: 活动标题
                - location: 地点
                - price: 价格
                - booked: 是否已预订
                - notes: 备注
        """
        self.daily_plans.append({
            'day_index': day_index,
            'date': date,
            'day_name': day_name,
            'theme': theme,
            'activities': activities
        })
    
    def generate_markdown(self, include_bookings: bool = True) -> str:
        """
        生成 Markdown 格式行程单
        
        Args:
            include_bookings: 是否包含已确认预订信息
        
        Returns:
            Markdown 格式的行程单
        """
        lines = []
        
        # 标题
        lines.append(f"# 📋 {self.city} 详细行程表")
        lines.append("")
        lines.append(f"*生成时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*")
        lines.append(f"*版本：v2.0（放松版）*")
        lines.append("")
        
        # 已确认预订信息
        if include_bookings and (self.bookings['hotels'] or self.bookings['transportation'] or 
                                  self.bookings['attractions']):
            lines.append("## 🎫 已确认预订信息")
            lines.append("")
            
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
                    station_info = ""
                    if transport.get('from_station'):
                        station_info = f"{transport['from_station']}→{transport.get('to_station', '')}"
                    lines.append(f"| - | {icon} {transport['number']} | {transport['departure_time']} | "
                               f"{transport['arrival_time']} | {transport['seat_class']} | "
                               f"{transport['price']}元 | {transport['confirmation_number']} |")
                if station_info:
                    lines.append(f"\n路线：{station_info}")
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
        
        # 完整行程安排
        lines.append("## 📅 完整行程安排")
        lines.append("")
        
        for plan in self.daily_plans:
            # 日期标题
            lines.append(f"### 第{plan['day_index']}天（{plan['date']} {plan['day_name']}）"
                        f"【{plan['theme']}】")
            lines.append("")
            
            # 当日活动
            for activity in plan['activities']:
                time_str = activity.get('time', '')
                title = activity.get('title', '')
                location = activity.get('location', '')
                price = activity.get('price', 0)
                booked = activity.get('booked', False)
                notes = activity.get('notes', '')
                
                # 时间
                if time_str:
                    lines.append(f"**🕐 {time_str}**")
                
                # 活动标题
                if title:
                    booking_icon = "✅ " if booked else ""
                    lines.append(f"- {booking_icon}{title}")
                
                # 地点
                if location:
                    lines.append(f"  - 📍 {location}")
                
                # 价格
                if price > 0:
                    lines.append(f"  - 💰 {price}元")
                    if booked:
                        lines.append(f"  - ✅ 已预订")
                
                # 备注
                if notes:
                    lines.append(f"  - 💡 {notes}")
                
                lines.append("")
            
            lines.append("---")
            lines.append("")
        
        # 紧急联系信息
        lines.append("## 📞 紧急联系信息")
        lines.append("")
        if self.bookings['hotels']:
            hotel = self.bookings['hotels'][0]
            if hotel.get('phone'):
                lines.append(f"- 酒店前台：{hotel['phone']}")
        lines.append(f"- 当地旅游热线：12301")
        lines.append(f"- 紧急求助：110 / 120")
        lines.append("")
        
        # 温馨提示
        lines.append("## 💡 温馨提示")
        lines.append("")
        lines.append("- 行程比较轻松，可根据实际情况自由调整")
        if self.bookings['transportation']:
            lines.append("- 请提前 30 分钟到达车站/机场")
        lines.append("- 随身携带身份证和预订确认信息")
        lines.append("- 保持手机畅通，便于接收通知")
        lines.append("")
        
        return "\n".join(lines)
    
    def generate_text_version(self) -> str:
        """生成纯文本版本（适合短信/微信发送）"""
        lines = []
        lines.append(f"【{self.city} 行程单】")
        lines.append(f"{self.start_date.strftime('%m.%d')}出发，共{self.days}天")
        lines.append("")
        
        # 关键预订
        if self.bookings['hotels']:
            hotel = self.bookings['hotels'][0]
            lines.append(f"🏨 {hotel['name']}")
            lines.append(f"   {hotel['check_in']}-{hotel['check_out']}入住")
            lines.append("")
        
        if self.bookings['transportation']:
            transport = self.bookings['transportation'][0]
            icon = "✈️" if transport['type'] == 'flight' else "🚄"
            lines.append(f"{icon} 返程：{transport['number']}")
            lines.append(f"   {transport['departure_time']}出发")
            lines.append("")
        
        # 每日亮点
        for plan in self.daily_plans:
            lines.append(f"D{plan['day_index']} ({plan['date']})：{plan['theme']}")
            # 只列出主要活动
            main_activities = [a for a in plan['activities'] if a.get('booked', False)]
            if main_activities:
                for act in main_activities:
                    lines.append(f"  • {act['time']} {act['title']}")
            else:
                lines.append(f"  • 自由活动为主")
        
        return "\n".join(lines)


def create_sample_itinerary() -> str:
    """创建示例行程单（用于测试）"""
    gen = ItineraryGenerator("杭州", "2026-04-15", 3)
    
    # 添加酒店预订
    gen.add_hotel_booking(
        name="全季酒店西湖店",
        address="杭州市上城区湖滨路 XX 号",
        check_in="2026-04-15",
        check_out="2026-04-17",
        price_per_night=380,
        room_type="高级大床房",
        confirmation_number="123456",
        phone="0571-88888888"
    )
    
    # 添加返程交通
    gen.add_transportation_booking(
        type="train",
        number="G1234",
        departure_time="15:30",
        arrival_time="20:45",
        seat_class="二等座",
        price=538,
        confirmation_number="654321",
        from_station="杭州东站",
        to_station="上海虹桥站"
    )
    
    # 添加景点门票
    gen.add_attraction_booking(
        name="灵隐寺",
        date="2026-04-16",
        time_slot="10:00-12:00",
        price=75,
        status="已预订"
    )
    
    # 添加每日行程
    gen.add_daily_plan(1, "2026-04-15", "周三", "轻松适应", [
        {'time': '10:00', 'title': '睡到自然醒，出门', 'location': '酒店出发'},
        {'time': '12:00', 'title': '午餐', 'location': '楼外楼', 'price': 80},
        {'time': '14:00', 'title': '西湖漫步', 'location': '断桥残雪→白堤', 'notes': '免费，随意走走停停'},
        {'time': '18:00', 'title': '晚餐', 'location': '外婆家', 'price': 60},
    ])
    
    gen.add_daily_plan(2, "2026-04-16", "周四", "核心体验", [
        {'time': '10:00', 'title': '灵隐寺参观', 'location': '灵隐寺', 'price': 75, 'booked': True},
        {'time': '12:00', 'title': '素斋午餐', 'location': '灵隐寺素斋馆', 'price': 40},
        {'time': '14:00', 'title': '自由时间', 'notes': '推荐龙井村品茶或回酒店休息'},
        {'time': '18:00', 'title': '晚餐', 'location': '绿茶餐厅', 'price': 70},
    ])
    
    gen.add_daily_plan(3, "2026-04-17", "周五", "返程", [
        {'time': '10:00', 'title': '退房，寄存行李', 'location': '酒店'},
        {'time': '11:00', 'title': '河坊街最后逛逛', 'location': '河坊街'},
        {'time': '12:00', 'title': '告别午餐', 'location': '知味观', 'price': 30},
        {'time': '13:30', 'title': '前往杭州东站', 'notes': '地铁 1 号线，约 30 分钟'},
        {'time': '15:30', 'title': 'G1234 次列车', 'location': '杭州东站', 'booked': True},
    ])
    
    return gen.generate_markdown()


def main():
    """命令行入口"""
    if len(sys.argv) > 1 and sys.argv[1] == '--sample':
        # 生成示例行程单
        print(create_sample_itinerary())
    else:
        print("使用方法:")
        print("  python itinerary_generator.py              # 显示帮助信息")
        print("  python itinerary_generator.py --sample     # 生成示例行程单")
        print("")
        print("程序说明:")
        print("  该脚本通常作为库使用，被主程序调用生成行程单")
        print("  --sample 参数用于测试和演示")


if __name__ == '__main__':
    main()
