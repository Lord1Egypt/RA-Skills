#!/home/linuxbrew/.linuxbrew/bin/python3.10
# -*- coding: utf-8 -*-
"""
select-super-stock 缓存包装器
交易时间使用 AKShare 实时数据，非交易时间使用缓存
"""

import sys
import os
import subprocess
from datetime import datetime

# 导入缓存工具
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '_shared'))
from cache_utils import StockDataCache, check_trading_status

SCRIPT_DIR = os.path.dirname(__file__)
CACHE_DIR = os.path.join(SCRIPT_DIR, '.cache')
ORIGINAL_SCRIPT = os.path.join(SCRIPT_DIR, 'stock_analyzer_orig.py')

# 初始化缓存
cache = StockDataCache(CACHE_DIR, cache_max_age_hours=24)

def main():
    print("=" * 60)
    print("📊 优质股票筛选专家")
    print("=" * 60)
    print()
    
    # 检查交易状态
    status = check_trading_status()
    print(f"📅 当前时间：{status['current_time']}")
    print(f"📆 星期：{status['weekday']}")
    print(f"💼 交易时间：{'是' if status['is_trading_time'] else '否'}")
    
    if not status['is_trading_time']:
        print(f"⏰ 下次交易：{status['next_trading_time']}")
    
    print()
    
    # 判断是否使用缓存
    use_cache = cache.should_use_cache()
    
    if use_cache:
        print("📦 非交易时间，使用缓存数据...")
        print()
        
        # 从缓存加载并显示
        cached_data = cache.load()
        if cached_data:
            print("=" * 60)
            print("📝 缓存数据报告")
            print("=" * 60)
            print()
            print(cached_data.get('report', '无缓存报告'))
            return
    else:
        print("🔍 交易时间，获取实时数据...")
        print()
    
    # 运行原始脚本获取实时数据
    print("=" * 60)
    print("🚀 执行分析...")
    print("=" * 60)
    print()
    
    result = subprocess.run(
        [sys.executable, ORIGINAL_SCRIPT] + sys.argv[1:],
        capture_output=True,
        text=True
    )
    
    output = result.stdout + result.stderr
    
    # 保存缓存
    if result.returncode == 0:
        cache.save({
            'report': output,
            'symbol': sys.argv[1] if len(sys.argv) > 1 else 'N/A'
        })
    
    # 输出结果
    print(output)
    
    if result.returncode != 0:
        print(f"\n❌ 脚本执行失败 (退出码：{result.returncode})")
        sys.exit(result.returncode)


if __name__ == '__main__':
    main()
