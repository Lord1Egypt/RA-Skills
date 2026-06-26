#!/home/linuxbrew/.linuxbrew/bin/python3.10
# -*- coding: utf-8 -*-
"""
通用缓存工具模块
为所有股票交易 skill 提供统一的缓存机制

功能：
- 交易时间自动检测
- 数据缓存/读取
- 缓存有效期管理
- 自动降级处理
"""

import os
import json
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class StockDataCache:
    """股票数据缓存管理器"""
    
    def __init__(self, cache_dir: str, cache_max_age_hours: int = 24):
        """
        初始化缓存管理器
        
        Args:
            cache_dir: 缓存目录路径
            cache_max_age_hours: 缓存最大有效期（小时）
        """
        self.cache_dir = cache_dir
        self.cache_max_age_hours = cache_max_age_hours
        self.cache_file = os.path.join(cache_dir, 'cache.json')
        
        # 确保缓存目录存在
        os.makedirs(cache_dir, exist_ok=True)
    
    def is_trading_time(self) -> bool:
        """
        判断当前是否为 A 股交易时间
        
        Returns:
            bool: True=交易时间，False=非交易时间
        """
        now = datetime.now()
        
        # 检查是否为工作日（周一=0 到 周五=4）
        if now.weekday() >= 5:  # 周六=5, 周日=6
            return False
        
        # 检查是否在交易时间段内
        # A 股交易时间：9:30-11:30, 13:00-15:00
        current_time = now.time()
        morning_start = datetime.strptime("09:30", "%H:%M").time()
        morning_end = datetime.strptime("11:30", "%H:%M").time()
        afternoon_start = datetime.strptime("13:00", "%H:%M").time()
        afternoon_end = datetime.strptime("15:30", "%H:%M").time()  # 延长到 15:30 用于盘后数据
        
        is_morning = morning_start <= current_time <= morning_end
        is_afternoon = afternoon_start <= current_time <= afternoon_end
        
        return is_morning or is_afternoon
    
    def should_use_cache(self) -> bool:
        """
        判断是否应该使用缓存
        
        Returns:
            bool: True=使用缓存，False=获取实时数据
        """
        # 如果是交易时间，不使用缓存（获取实时数据）
        if self.is_trading_time():
            return False
        
        # 非交易时间，检查是否有有效缓存
        return self.has_valid_cache()
    
    def has_valid_cache(self) -> bool:
        """
        检查是否有有效的缓存
        
        Returns:
            bool: True=有有效缓存，False=无缓存或缓存过期
        """
        if not os.path.exists(self.cache_file):
            return False
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查缓存时间
            cache_time_str = data.get('cache_time', '')
            if not cache_time_str:
                return False
            
            cache_time = datetime.fromisoformat(cache_time_str)
            age_hours = (datetime.now() - cache_time).total_seconds() / 3600
            
            return age_hours < self.cache_max_age_hours
        
        except Exception as e:
            print(f"⚠️ 缓存检查失败：{e}")
            return False
    
    def load(self) -> Optional[Dict[str, Any]]:
        """
        从缓存加载数据
        
        Returns:
            dict or None: 缓存数据，失败返回 None
        """
        if not os.path.exists(self.cache_file):
            return None
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 检查缓存是否过期
            cache_time_str = data.get('cache_time', '')
            if cache_time_str:
                cache_time = datetime.fromisoformat(cache_time_str)
                age_hours = (datetime.now() - cache_time).total_seconds() / 3600
                
                if age_hours < self.cache_max_age_hours:
                    print(f"✓ 使用缓存数据 (生成于 {cache_time.strftime('%Y-%m-%d %H:%M')}, {age_hours:.1f}小时前)")
                    return data
                else:
                    print(f"⚠️ 缓存已过期 ({age_hours:.1f}小时前)")
                    return None
            else:
                return None
        
        except Exception as e:
            print(f"⚠️ 缓存读取失败：{e}")
            return None
    
    def save(self, data: Dict[str, Any]) -> bool:
        """
        保存数据到缓存
        
        Args:
            data: 要缓存的数据
        
        Returns:
            bool: True=保存成功，False=保存失败
        """
        try:
            # 添加缓存时间戳
            data['cache_time'] = datetime.now().isoformat()
            data['cache_expire'] = (datetime.now() + timedelta(hours=self.cache_max_age_hours)).isoformat()
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print(f"✓ 数据已缓存到 {self.cache_file}")
            return True
        
        except Exception as e:
            print(f"⚠️ 缓存保存失败：{e}")
            return False
    
    def clear(self) -> bool:
        """
        清除缓存
        
        Returns:
            bool: True=清除成功，False=清除失败
        """
        try:
            if os.path.exists(self.cache_file):
                os.remove(self.cache_file)
                print("✓ 缓存已清除")
                return True
            else:
                print("ℹ️ 无缓存可清除")
                return True
        
        except Exception as e:
            print(f"⚠️ 缓存清除失败：{e}")
            return False
    
    def get_cache_info(self) -> Dict[str, Any]:
        """
        获取缓存信息
        
        Returns:
            dict: 缓存信息
        """
        info = {
            'exists': os.path.exists(self.cache_file),
            'valid': False,
            'cache_time': None,
            'age_hours': None,
            'expire_time': None
        }
        
        if info['exists']:
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                cache_time_str = data.get('cache_time', '')
                if cache_time_str:
                    cache_time = datetime.fromisoformat(cache_time_str)
                    info['cache_time'] = cache_time.strftime('%Y-%m-%d %H:%M:%S')
                    info['age_hours'] = round((datetime.now() - cache_time).total_seconds() / 3600, 1)
                    info['valid'] = info['age_hours'] < self.cache_max_age_hours
                
                expire_time_str = data.get('cache_expire', '')
                if expire_time_str:
                    info['expire_time'] = datetime.fromisoformat(expire_time_str).strftime('%Y-%m-%d %H:%M:%S')
            
            except Exception as e:
                info['error'] = str(e)
        
        return info


def check_trading_status() -> Dict[str, Any]:
    """
    检查当前交易状态
    
    Returns:
        dict: 交易状态信息
    """
    now = datetime.now()
    
    is_trading = now.weekday() < 5 and (
        datetime.strptime("09:30", "%H:%M").time() <= now.time() <= datetime.strptime("11:30", "%H:%M").time() or
        datetime.strptime("13:00", "%H:%M").time() <= now.time() <= datetime.strptime("15:30", "%H:%M").time()
    )
    
    status = {
        'current_time': now.strftime('%Y-%m-%d %H:%M:%S'),
        'weekday': now.strftime('%A'),
        'is_trading_day': now.weekday() < 5,
        'is_trading_time': is_trading,
        'next_trading_time': None
    }
    
    # 计算下次交易时间
    if not is_trading:
        if now.weekday() >= 5:  # 周末
            next_monday = now + timedelta(days=(7 - now.weekday()))
            next_trading = next_monday.replace(hour=9, minute=30, second=0, microsecond=0)
        else:  # 工作日非交易时间
            if now.time() < datetime.strptime("09:30", "%H:%M").time():
                next_trading = now.replace(hour=9, minute=30, second=0, microsecond=0)
            else:
                next_day = now + timedelta(days=1)
                if next_day.weekday() >= 5:
                    next_day += timedelta(days=(7 - next_day.weekday()))
                next_trading = next_day.replace(hour=9, minute=30, second=0, microsecond=0)
        
        status['next_trading_time'] = next_trading.strftime('%Y-%m-%d %H:%M:%S')
    
    return status


# 使用示例
if __name__ == '__main__':
    print("=" * 60)
    print("缓存工具模块 - 测试")
    print("=" * 60)
    print()
    
    # 检查交易状态
    status = check_trading_status()
    print("📅 当前时间:", status['current_time'])
    print("📆 星期:", status['weekday'])
    print("💼 是否交易日:", "是" if status['is_trading_day'] else "否")
    print("📊 是否交易时间:", "是" if status['is_trading_time'] else "否")
    
    if not status['is_trading_time']:
        print("⏰ 下次交易时间:", status['next_trading_time'])
    
    print()
    
    # 测试缓存
    cache = StockDataCache(cache_dir='./test_cache', cache_max_age_hours=24)
    
    print("📦 缓存信息:")
    info = cache.get_cache_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    
    print()
    print("🎯 是否使用缓存:", "是" if cache.should_use_cache() else "否")
