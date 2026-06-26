#!/usr/bin/env python3
"""
快速路径模块 - v1.0.0 (参考鸽子王架构)
用于简单查询的快速处理路径
"""

import re
import time
from typing import Dict, Optional, Tuple
from pathlib import Path
from datetime import datetime

# 简单查询模式
SIMPLE_PATTERNS = {
    # 状态查询
    r'^状态$|检查状态|健康检测': 'health_check',
    r'^记忆状态|记忆统计|记忆情况': 'memory_stats',
    r'^配置|查看配置|当前配置': 'config_show',
    
    # 简单读取
    r'^版本|版本号|v\d+\.\d+': 'version',
    r'^帮助|help|命令': 'help',
    
    # 列表查询
    r'^列表|列出|查看全部': 'list_all',
    
    # 时间查询
    r'^时间|现在几点': 'time_now',
}

# 缓存配置
FAST_CACHE_TTL = 60  # 快速缓存: 60秒


class FastPath:
    """快速路径处理器"""
    
    def __init__(self):
        self.cache = {}
        self.cache_time = {}
        self.stats = {
            'total': 0,
            'cache_hit': 0,
            'fast_path': 0,
        }
    
    def is_simple_query(self, query: str) -> Tuple[bool, str]:
        """判断是否是简单查询"""
        query = query.strip().lower()
        
        for pattern, handler in SIMPLE_PATTERNS.items():
            if re.search(pattern, query):
                return True, handler
        
        return False, ''
    
    def get_cache(self, key: str) -> Optional[Dict]:
        """获取缓存"""
        if key in self.cache:
            cache_time = self.cache_time.get(key, 0)
            if time.time() - cache_time < FAST_CACHE_TTL:
                self.stats['cache_hit'] += 1
                return self.cache[key]
            else:
                # 过期删除
                del self.cache[key]
                del self.cache_time[key]
        return None
    
    def set_cache(self, key: str, data: Dict):
        """设置缓存"""
        self.cache[key] = data
        self.cache_time[key] = time.time()
    
    def handle_fast_path(self, query: str, executor) -> Optional[Dict]:
        """处理快速路径"""
        self.stats['total'] += 1
        
        is_simple, handler_name = self.is_simple_query(query)
        if not is_simple:
            return None
        
        self.stats['fast_path'] += 1
        
        # 检查缓存
        cached = self.get_cache(handler_name)
        if cached:
            return cached
        
        # 执行处理
        handler = getattr(self, f'_handle_{handler_name}', None)
        if not handler:
            return None
        
        try:
            result = handler(executor)
            self.set_cache(handler_name, result)
            return result
        except Exception as e:
            return {'error': str(e), 'handler': handler_name}
    
    def _handle_health_check(self, executor) -> Dict:
        """处理健康检测"""
        return {
            'type': 'fast_path',
            'handler': 'health_check',
            'status': 'ok',
            'message': '系统运行正常'
        }
    
    def _handle_memory_stats(self, executor) -> Dict:
        """处理记忆统计"""
        return {
            'type': 'fast_path',
            'handler': 'memory_stats',
            'status': 'ok'
        }
    
    def _handle_config_show(self, executor) -> Dict:
        """处理配置显示"""
        return {
            'type': 'fast_path',
            'handler': 'config_show',
            'status': 'ok'
        }
    
    def _handle_version(self, executor) -> Dict:
        """处理版本查询"""
        return {
            'type': 'fast_path',
            'handler': 'version',
            'version': '3.9.0',
            'status': 'ok'
        }
    
    def _handle_time_now(self, executor) -> Dict:
        """处理时间查询"""
        now = datetime.now()
        return {
            'type': 'fast_path',
            'handler': 'time_now',
            'time': now.strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp': now.timestamp()
        }
    
    def get_stats(self) -> Dict:
        """获取统计"""
        cache_rate = (self.stats['cache_hit'] / max(self.stats['total'], 1)) * 100
        fast_rate = (self.stats['fast_path'] / max(self.stats['total'], 1)) * 100
        
        return {
            **self.stats,
            'cache_hit_rate': f'{cache_rate:.1f}%',
            'fast_path_rate': f'{fast_rate:.1f}%'
        }


if __name__ == '__main__':
    fast_path = FastPath()
    
    # 测试
    test_queries = [
        '状态',
        '检查状态',
        '记忆状态',
        '配置',
        '版本',
        '现在几点',
        '帮我写一段代码',  # 非简单查询
    ]
    
    print('=== 快速路径测试 ===\n')
    for q in test_queries:
        is_simple, handler = fast_path.is_simple_query(q)
        print(f'查询: {q}')
        print(f'  简单查询: {is_simple} ({handler})')
        print()
    
    print(f'统计: {fast_path.get_stats()}')
