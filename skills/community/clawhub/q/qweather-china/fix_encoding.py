#!/usr/bin/env python3
"""
修复qweather.py文件的编码问题
将所有print语句替换为safe_print
"""

import re
import os

def fix_print_statements(file_path):
    """修复文件中的print语句"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 替换print为safe_print
    # 匹配 print( 但不匹配 safe_print(
    pattern = r'(?<!safe_)print\('
    replacement = 'safe_print('
    
    new_content = re.sub(pattern, replacement, content)
    
    # 检查是否有变化
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"已修复 {file_path} 中的print语句")
        return True
    else:
        print(f"{file_path} 无需修复")
        return False

def fix_all_files():
    """修复所有Python文件"""
    files_to_fix = [
        'qweather.py',
        'openclaw_integration.py',
        'location_handler.py',
        'test_enhanced.py',
        'answer_tomorrow.py',
        'answer_simple.py',
        'check_tomorrow.py',
    ]
    
    fixed_count = 0
    for filename in files_to_fix:
        file_path = os.path.join(os.path.dirname(__file__), filename)
        if os.path.exists(file_path):
            if fix_print_statements(file_path):
                fixed_count += 1
    
    print(f"\n总共修复了 {fixed_count} 个文件")
    
    # 创建测试脚本
    create_test_script()
    
    return fixed_count

def create_test_script():
    """创建测试脚本"""
    test_script = '''#!/usr/bin/env python3
"""
测试跨平台兼容性
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from encoding_utils import setup_encoding, safe_print
from qweather import QWeatherClient

def test_cross_platform():
    """测试跨平台兼容性"""
    # 设置编码
    info = setup_encoding()
    
    safe_print("=" * 50)
    safe_print("qweather-china v1.1.1 跨平台兼容性测试")
    safe_print("=" * 50)
    
    safe_print(f"平台: {info['platform']}")
    safe_print(f"编码: {info['encoding']}")
    safe_print(f"Python版本: {info['python_version']}")
    
    safe_print("\n" + "=" * 50)
    safe_print("测试天气查询功能")
    safe_print("=" * 50)
    
    try:
        client = QWeatherClient()
        
        # 测试实时天气
        safe_print("\n1. 测试实时天气查询:")
        weather = client.get_weather_now("beijing")
        safe_print(f"🌤️ 北京当前天气")
        safe_print(f"🌡️ 温度: {weather.temp}°C")
        safe_print(f"💧 湿度: {weather.humidity}%")
        safe_print(f"🌬️ 风力: {weather.wind_scale}级 {weather.wind_dir}")
        
        # 测试天气预报
        safe_print("\n2. 测试天气预报:")
        forecasts = client.get_weather_forecast("beijing", 2)
        for i, forecast in enumerate(forecasts):
            day = "今天" if i == 0 else "明天"
            safe_print(f"\n📅 {day} ({forecast.fx_date}):")
            safe_print(f"☀️ 白天: {forecast.text_day}")
            safe_print(f"🌙 夜间: {forecast.text_night}")
            safe_print(f"🌡️ 温度: {forecast.temp_min}°C ~ {forecast.temp_max}°C")
        
        safe_print("\n" + "=" * 50)
        safe_print("✅ 跨平台兼容性测试通过！")
        safe_print("=" * 50)
        
        return True
        
    except Exception as e:
        safe_print(f"\n❌ 测试失败: {str(e)}")
        safe_print("=" * 50)
        return False

if __name__ == "__main__":
    success = test_cross_platform()
    sys.exit(0 if success else 1)
'''
    
    test_file = os.path.join(os.path.dirname(__file__), 'test_cross_platform.py')
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_script)
    
    print(f"已创建测试脚本: {test_file}")

if __name__ == "__main__":
    print("开始修复qweather-china技能的编码问题...")
    fix_all_files()
    print("\n修复完成！现在可以运行 test_cross_platform.py 进行测试。")