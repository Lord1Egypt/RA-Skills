#!/usr/bin/env python3
"""盲盒旅行规划器 - 独立体验版

无需 QoderWork，直接在命令行体验完整的盲盒旅行规划流程。
包含：历史记录管理、目的地推荐、行程生成、预订跟踪等功能。

使用方法:
    python blind_box_travel.py
"""

import json
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional

# 导入历史记录管理器
sys.path.insert(0, str(Path(__file__).parent))
from scripts.history_manager import HistoryManager


class BlindBoxTravel:
    """盲盒旅行规划器"""
    
    def __init__(self):
        self.history = HistoryManager()
        self.user_info = {}
        self.bookings = {
            'hotels': [],
            'transportation': [],
            'attractions': []
        }
        
        # 城市数据库（简化版，实际应该调用 API）
        self.city_database = {
            "上海": {
                "nearby": [
                    {"name": "南京", "time": "1h", "cost": 1800, "features": ["六朝古都", "中山陵", "夫子庙"]},
                    {"name": "扬州", "time": "1.5h", "cost": 1500, "features": ["淮扬美食", "瘦西湖", "烟花三月"]},
                    {"name": "绍兴", "time": "1h", "cost": 1300, "features": ["鲁迅故里", "江南水乡", "黄酒文化"]},
                    {"name": "无锡", "time": "30min", "cost": 1600, "features": ["太湖明珠", "鼋头渚", "灵山大佛"]},
                    {"name": "宁波", "time": "2h", "cost": 1700, "features": ["港口古城", "天一阁", "海鲜美食"]},
                ]
            },
            "杭州": {
                "nearby": [
                    {"name": "成都", "time": "2.5h✈️", "cost": 3500, "features": ["美食之都", "大熊猫", "宽窄巷子"]},
                    {"name": "厦门", "time": "1.5h✈️", "cost": 4000, "features": ["海上花园", "鼓浪屿", "海滨风光"]},
                    {"name": "西安", "time": "2h✈️", "cost": 3800, "features": ["十三朝古都", "兵马俑", "古城墙"]},
                    {"name": "桂林", "time": "2h✈️", "cost": 3200, "features": ["山水甲天下", "漓江", "象鼻山"]},
                    {"name": "青岛", "time": "2h✈️", "cost": 3600, "features": ["红瓦绿树", "栈桥", "八大关"]},
                    {"name": "长沙", "time": "4h🚄", "cost": 2800, "features": ["娱乐之都", "橘子洲", "岳麓山"]},
                ]
            },
            "北京": {
                "nearby": [
                    {"name": "西安", "time": "1.5h✈️", "cost": 3500, "features": ["十三朝古都", "兵马俑", "回民街"]},
                    {"name": "成都", "time": "2.5h✈️", "cost": 3800, "features": ["美食之都", "大熊猫", "火锅"]},
                    {"name": "青岛", "time": "3h🚄", "cost": 2500, "features": ["海滨城市", "啤酒节", "栈桥"]},
                ]
            },
            "广州": {
                "nearby": [
                    {"name": "厦门", "time": "1.5h✈️", "cost": 3200, "features": ["海上花园", "鼓浪屿", "沙茶面"]},
                    {"name": "桂林", "time": "1h✈️", "cost": 2800, "features": ["山水甲天下", "漓江", "阳朔"]},
                    {"name": "长沙", "time": "2.5h🚄", "cost": 2200, "features": ["娱乐之都", "湘菜", "橘子洲"]},
                ]
            }
        }
    
    def print_separator(self, char="=", length=60):
        """打印分隔线"""
        print(char * length)
    
    def collect_user_info(self):
        """收集用户信息"""
        print("\n🎲 欢迎使用盲盒旅行规划器！")
        self.print_separator()
        print("我很乐意为你安排一次说走就走的盲盒旅行！\n")
        
        # 1. 当前位置
        while True:
            city = input("请问你现在在哪个城市呢？ ").strip()
            if city:
                self.user_info['current_city'] = city
                break
            print("请输入有效的城市名称\n")
        
        # 2. 出发日期
        while True:
            date = input("\n请问你计划哪天出发呢？ (如 4 月 20 号/下周六) ").strip()
            if date:
                self.user_info['departure_date'] = date
                # 尝试解析日期
                try:
                    # 简单处理"4.27"格式
                    if '.' in date and len(date) <= 5:
                        month, day = map(int, date.split('.'))
                        parsed_date = datetime(2026, month, day)
                        self.user_info['parsed_date'] = parsed_date
                except:
                    pass
                break
            print("请输入有效的日期\n")
        
        # 3. 游玩天数
        while True:
            days = input("\n准备去玩几天呢？ (建议 2-5 天) ").strip()
            if days.isdigit() and 1 <= int(days) <= 10:
                self.user_info['days'] = int(days)
                break
            print("请输入有效的天数 (1-10)\n")
        
        # 4. 预算
        while True:
            budget = input("\n你的预算大概是多少呢？ (如 2000 元) ").strip()
            # 提取数字
            budget_num = ''.join(filter(str.isdigit, budget))
            if budget_num:
                self.user_info['budget'] = int(budget_num)
                break
            print("请输入有效的预算金额\n")
        
        print(f"\n✅ 收到！从{self.user_info['current_city']}出发，{self.user_info['departure_date']}出发，玩{self.user_info['days']}天，预算{self.user_info['budget']}元")
    
    def check_history(self):
        """查询历史记录"""
        print("\n📋 正在查询你的旅行历史记录...")
        
        visited = self.history.get_visited_cities()
        
        if visited:
            print(f"系统显示你之前去过：**{', '.join(visited)}**")
            print("这次我不会推荐这些地方，保证给你新奇的体验！✨\n")
        else:
            print("🎉 这是你第一次使用盲盒旅行服务，历史记录为空。")
            print("太棒了！这意味着所有城市都可以推荐，充满惊喜！✨\n")
    
    def recommend_destinations(self):
        """推荐目的地"""
        current_city = self.user_info['current_city']
        budget = self.user_info['budget']
        
        print(f"\n🔍 正在为你从{current_city}周边筛选适合的未去过城市...")
        
        # 获取候选城市
        nearby_cities = []
        for city, data in self.city_database.items():
            if city.lower() == current_city.lower():
                nearby_cities = data['nearby']
                break
        
        if not nearby_cities:
            # 如果没有匹配的城市，使用默认列表
            nearby_cities = [
                {"name": "成都", "time": "2-3h", "cost": 3500, "features": ["美食之都", "大熊猫", "宽窄巷子"]},
                {"name": "厦门", "time": "1.5h✈️", "cost": 4000, "features": ["海上花园", "鼓浪屿", "海滨风光"]},
                {"name": "西安", "time": "2h✈️", "cost": 3800, "features": ["十三朝古都", "兵马俑", "古城墙"]},
            ]
        
        # 过滤去过的城市
        visited = set(self.history.get_visited_cities())
        candidates = [c for c in nearby_cities if c['name'] not in visited]
        
        if not candidates:
            print("⚠️ 抱歉，周边推荐的城市你都去过了！")
            return None
        
        # 根据预算过滤
        affordable = [c for c in candidates if c['cost'] <= budget * 0.8]
        if affordable:
            candidates = affordable
        
        # 展示候选列表
        print("\n### 候选目的地")
        for i, city in enumerate(candidates[:6], 1):
            features = ', '.join(city['features'][:2])
            transport_icon = "✈️" if "✈️" in city['time'] else "🚄"
            print(f"{i}. **{city['name']}** - {features} ({transport_icon}{city['time']}, 预计花费{city['cost']}元)")
        
        print()
        
        # 随机选择
        selected = random.choice(candidates)
        
        print("🎲 现在我将从这些城市中随机选择一个作为你的目的地...")
        print("即将揭晓...")
        for i in range(3, 0, -1):
            print(f"{i}️⃣ ...")
            import time
            time.sleep(1)
        
        return selected
    
    def announce_destination(self, destination):
        """宣布目的地"""
        print("\n" + "=" * 60)
        print(f"🎁 盲盒揭晓！这次为你推荐的目的地是：**{destination['name']}**！")
        print("=" * 60)
        
        print(f"\n🌟 推荐理由:")
        print(f"- ✅ 你从未去过{destination['name']}")
        print(f"- ✅ {destination['features'][0]}")
        print(f"- ✅ 交通{destination['time']}直达，便利")
        print(f"- ✅ 预算范围内（预计{destination['cost']}元）")
        print(f"- ✅ 此时节气候宜人，适合旅行")
    
    def generate_itinerary(self, destination):
        """生成行程（简化版）"""
        city_name = destination['name']
        days = self.user_info['days']
        budget = self.user_info['budget']
        
        print(f"\n🏝️ 正在为你生成{city_name} {days}天的轻松行程...\n")
        
        # 预算分配
        accommodation = int(budget * 0.4)
        food = int(budget * 0.25)
        transport = int(budget * 0.25)
        entertainment = int(budget * 0.1)
        
        print("### 💰 预算分配（总预算{}元）".format(budget))
        print(f"| 类别 | 预算 | 占比 |")
        print(f"|------|------|------|")
        print(f"| 🏨 住宿 | {accommodation}元 | 40% |")
        print(f"| 🍜 餐饮 | {food}元 | 25% |")
        print(f"| ✈️ 交通 | {transport}元 | 25% |")
        print(f"| 🎢 娱乐 | {entertainment}元 | 10% |")
        
        print(f"\n### 📅 {days}天轻松行程安排")
        
        for day in range(1, days + 1):
            if day == 1:
                theme = "抵达 + 适应"
            elif day == days:
                theme = "返程"
            else:
                theme = "核心体验"
            
            print(f"\n#### 第{day}天【{theme}】")
            
            if day == 1:
                print("- 上午：抵达{city}，入住酒店".format(city=city_name))
                print("- 中午：当地特色午餐")
                print("- 下午：轻松漫步，适应环境")
                print("- 晚上：晚餐 + 自由活动")
            elif day == days:
                print("- 上午：最后一个景点")
                print("- 中午：告别午餐")
                print("- 下午：前往机场/车站，返程")
            else:
                print("- 上午：睡到自然醒，主要景点")
                print("- 中午：特色美食")
                print("- 下午：自由时间或轻松活动")
                print("- 晚上：晚餐推荐")
    
    def ask_booking(self):
        """询问是否预订"""
        print("\n" + "=" * 60)
        print("🎯 接下来怎么做？\n")
        print("A. 立即开始预订 - 我可以帮你查询酒店、交通等信息")
        print("B. 调整方案 - 换个城市/调整预算/修改行程")
        print("C. 先看看 - 保存方案，考虑一下再决定")
        
        choice = input("\n你的选择是？ (A/B/C) ").strip().upper()
        
        if choice == 'A':
            self.start_booking()
        elif choice == 'B':
            print("\n好的！你可以告诉我：")
            print("- '换个城市吧' - 重新随机选择")
            print("- '酒店太贵了' - 调整预算")
            print("- '行程太满' - 减少活动")
        elif choice == 'C':
            print("\n没问题！你可以随时再来找我～")
            print("祝你旅途愉快！✈️")
    
    def start_booking(self):
        """开始预订流程（简化演示）"""
        print("\n好的！让我们开始预订吧～\n")
        
        # 酒店预订
        print("### 🏨 第一步：预订酒店")
        print("推荐以下酒店:\n")
        print("1. 豪华型酒店 - 800 元/晚")
        print("2. 舒适型酒店 - 500 元/晚")
        print("3. 经济型酒店 - 300 元/晚")
        
        hotel_choice = input("\n你想预订哪家酒店？ (1/2/3) ").strip()
        if hotel_choice in ['1', '2', '3']:
            confirmation = input("请输入确认号（模拟，直接回车跳过）: ").strip() or "DEMO123"
            self.bookings['hotels'].append({
                'name': f"酒店{hotel_choice}",
                'confirmation': confirmation
            })
            print("✅ 酒店预订完成！\n")
        
        # 交通预订
        print("### ✈️ 第二步：预订往返交通")
        print("推荐航班/高铁:")
        print("1. 早班机 08:00 - 980 元")
        print("2. 午班机 14:00 - 850 元")
        print("3. 晚班机 18:00 - 920 元")
        
        transport_choice = input("\n你想预订哪一班？ (1/2/3) ").strip()
        if transport_choice in ['1', '2', '3']:
            confirmation = input("请输入确认号（模拟，直接回车跳过）: ").strip() or "FLIGHT456"
            self.bookings['transportation'].append({
                'name': f"航班{transport_choice}",
                'confirmation': confirmation
            })
            print("✅ 交通预订完成！\n")
        
        # 生成行程表
        self.generate_booking_summary()
    
    def generate_booking_summary(self):
        """生成预订总结"""
        print("\n" + "=" * 60)
        print("📋 预订总结")
        print("=" * 60)
        
        if self.bookings['hotels']:
            print("\n### 🏨 已预订酒店")
            for hotel in self.bookings['hotels']:
                print(f"- {hotel['name']} (确认号：{hotel['confirmation']})")
        
        if self.bookings['transportation']:
            print("\n### ✈️ 已预订交通")
            for transport in self.bookings['transportation']:
                print(f"- {transport['name']} (确认号：{transport['confirmation']})")
        
        print("\n✅ 所有预订已完成！")
        print("旅行结束后记得告诉我，我会帮你记录到历史中～\n")
    
    def save_to_history(self):
        """保存到历史记录"""
        print("\n🎉 欢迎回来！这次旅行玩得开心吗？")
        
        happy = input("开心吗？ (y/n) ").strip().lower()
        
        if happy == 'y':
            city = input("去的哪个城市呀？ ").strip()
            if city:
                date_str = datetime.now().strftime('%Y-%m-%d')
                self.history.add_visited_city(city, date_str, "盲盒旅行")
                print(f"✅ 已将{city}添加到你的旅行历史记录中！")
                print("下次为你推荐其他未去过的城市！\n")
        else:
            print("没关系，下次我会推荐更好的目的地！\n")
    
    def run(self):
        """运行完整流程"""
        try:
            # 1. 收集信息
            self.collect_user_info()
            
            # 2. 查询历史
            self.check_history()
            
            # 3. 推荐目的地
            destination = self.recommend_destinations()
            
            if not destination:
                return
            
            # 4. 宣布目的地
            self.announce_destination(destination)
            
            # 5. 生成行程
            self.generate_itinerary(destination)
            
            # 6. 询问预订
            self.ask_booking()
            
            # 7. 保存到历史（可选）
            save = input("\n旅行结束了吗？要记录到历史中吗？ (y/n) ").strip().lower()
            if save == 'y':
                self.save_to_history()
            
            print("\n感谢你使用盲盒旅行服务！期待下一次为你解锁新的目的地！✈️🎲\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 再见！祝你旅途愉快！\n")
            sys.exit(0)


def main():
    """主函数"""
    travel = BlindBoxTravel()
    travel.run()


if __name__ == '__main__':
    main()
