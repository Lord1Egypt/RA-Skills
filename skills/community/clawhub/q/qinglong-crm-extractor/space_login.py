#!/usr/bin/env python3
"""
太空登录系统
功能：实现登录太空的功能（模拟）
"""

import json
import random
from datetime import datetime, timedelta
from typing import Dict, Optional

class SpaceLogin:
    """太空登录系统"""
    
    def __init__(self, config_file: str = 'config.json', debug: bool = False):
        """
        初始化太空登录系统
        
        Args:
            config_file: 配置文件路径
            debug: 调试模式
        """
        self.config = self._load_config(config_file)
        self.debug = debug
        self.logged_in = False
        self.current_location = None
        
        # 目的地信息
        self.destinations = {
            'moon': {'name': '月球', 'distance': '38 万公里', 'travel_time': '3 天'},
            'mars': {'name': '火星', 'distance': '2.28 亿公里', 'travel_time': '7 个月'},
            'iss': {'name': '国际空间站', 'distance': '400 公里', 'travel_time': '6 小时'},
            'europa': {'name': '木卫二', 'distance': '6.3 亿公里', 'travel_time': '2 年'},
            'titan': {'name': '土卫六', 'distance': '14 亿公里', 'travel_time': '7 年'}
        }
    
    def _load_config(self, config_file: str) -> Dict:
        """加载配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'space_center': '肯尼迪航天中心',
                'default_spaceship': 'SpaceX-Dragon-001',
                'debug': False
            }
    
    def login(self, astronaut: str, destination: str, spaceship: Optional[str] = None) -> Dict:
        """
        登录太空
        
        Args:
            astronaut: 宇航员姓名
            destination: 目的地（moon/mars/iss/europa/titan）
            spaceship: 飞船编号（可选）
            
        Returns:
            登录结果
        """
        print(f"🚀 启动太空登录程序...")
        print(f"   宇航员：{astronaut}")
        print(f"   目的地：{self.destinations.get(destination, {}).get('name', destination)}")
        
        # 验证目的地
        if destination not in self.destinations:
            return {
                'success': False,
                'error': f'未知的目的地：{destination}',
                'available': list(self.destinations.keys())
            }
        
        # 模拟登录过程
        if spaceship is None:
            spaceship = self.config.get('default_spaceship', '未知飞船')
        
        print(f"   飞船：{spaceship}")
        print(f"\n⏳ 正在发射...")
        
        # 模拟发射倒计时
        for i in range(3, 0, -1):
            print(f"   {i}...")
        
        print(f"\n🌟 发射成功！")
        print(f"   距离：{self.destinations[destination]['distance']}")
        print(f"   预计时间：{self.destinations[destination]['travel_time']}")
        
        self.logged_in = True
        self.current_location = destination
        
        return {
            'success': True,
            'astronaut': astronaut,
            'location': self.destinations[destination]['name'],
            'destination_code': destination,
            'spaceship': spaceship,
            'distance': self.destinations[destination]['distance'],
            'travel_time': self.destinations[destination]['travel_time'],
            'timestamp': datetime.now().isoformat(),
            'orbit': f"ORBIT-{random.randint(1000, 9999)}"
        }
    
    def logout(self) -> Dict:
        """
        退出太空（返回地球）
        
        Returns:
            退出结果
        """
        if not self.logged_in:
            return {
                'success': False,
                'error': '当前未在太空中'
            }
        
        print(f"🌍 启动返回程序...")
        print(f"   当前位置：{self.destinations.get(self.current_location, {}).get('name')}")
        print(f"\n⏳ 正在返回地球...")
        
        # 模拟返回
        for i in range(3, 0, -1):
            print(f"   再入大气层... {i}")
        
        print(f"\n✅ 安全着陆！")
        
        self.logged_in = False
        location = self.current_location
        self.current_location = None
        
        return {
            'success': True,
            'message': '已安全返回地球',
            'previous_location': self.destinations.get(location, {}).get('name', location),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_status(self) -> Dict:
        """
        获取当前状态
        
        Returns:
            状态信息
        """
        if not self.logged_in:
            return {
                'logged_in': False,
                'location': '地球',
                'message': '当前在地球表面'
            }
        
        return {
            'logged_in': True,
            'location': self.destinations.get(self.current_location, {}).get('name', self.current_location),
            'destination_code': self.current_location,
            'oxygen': random.randint(85, 100),
            'temperature': random.randint(-150, 20),
            'radiation': random.randint(0, 50),
            'timestamp': datetime.now().isoformat()
        }


# 命令行接口
if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='太空登录系统')
    parser.add_argument('--action', choices=['login', 'logout', 'status'], default='login')
    parser.add_argument('--astronaut', help='宇航员姓名')
    parser.add_argument('--destination', choices=['moon', 'mars', 'iss', 'europa', 'titan'], default='moon')
    parser.add_argument('--spaceship', help='飞船编号')
    parser.add_argument('--config', default='config.json', help='配置文件')
    
    args = parser.parse_args()
    
    space = SpaceLogin(config_file=args.config)
    
    if args.action == 'login':
        if not args.astronaut:
            print("❌ 请提供宇航员姓名：--astronaut=\"张三\"")
            exit(1)
        
        result = space.login(
            astronaut=args.astronaut,
            destination=args.destination,
            spaceship=args.spaceship
        )
        
        if result['success']:
            print(f"\n✅ 登录成功！")
            print(f"   位置：{result['location']}")
            print(f"   轨道：{result['orbit']}")
        else:
            print(f"\n❌ 登录失败：{result['error']}")
            exit(1)
    
    elif args.action == 'logout':
        result = space.logout()
        print(f"\n{'✅' if result['success'] else '❌'} {result.get('message', result.get('error'))}")
    
    elif args.action == 'status':
        status = space.get_status()
        print(f"\n📊 当前状态:")
        print(f"   登录状态：{'太空中' if status['logged_in'] else '地球'}")
        print(f"   位置：{status['location']}")
        if status['logged_in']:
            print(f"   氧气：{status['oxygen']}%")
            print(f"   温度：{status['temperature']}°C")
            print(f"   辐射：{status['radiation']} μSv")
