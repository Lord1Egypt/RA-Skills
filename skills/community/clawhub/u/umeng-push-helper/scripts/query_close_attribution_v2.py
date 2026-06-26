#!/usr/bin/env python3
"""
友盟推送助手 - 关闭归因分析（修复版）
调用 upush.umeng.com API 查询应用关闭归因数据
包括：用户偏好分析、推送频次分析、通知内容分析、设备维度分析
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

COOKIE_FILE = os.path.expanduser("~/.qoderwork/skills/umeng-push-helper/cookie.txt")
SCRIPT_DIR = Path(__file__).parent

# 支持的日期类型
DATE_TYPES = {
    "1d": "昨日",
    "7d": "近 7 日"
}

# 分析接口定义
ANALYSIS_INTERFACES = {
    "userPreference": {
        "name": "用户偏好分析",
        "url": "https://upush.umeng.com/hsf/dataStatistic/userPreferenceAnalyzer",
        "icon": "👤"
    },
    "pushFrequency": {
        "name": "推送频次分析",
        "url": "https://upush.umeng.com/hsf/dataStatistic/pushFrequencyAnalyzer",
        "icon": "📱"
    },
    "pushMessage": {
        "name": "通知内容分析",
        "url": "https://upush.umeng.com/hsf/dataStatistic/pushMessageAnalyzer",
        "icon": "📝"
    },
    "deviceDimension": {
        "name": "设备维度分析",
        "url": "https://upush.umeng.com/hsf/dataStatistic/deviceDimensionAnalyzer",
        "icon": "📲"
    }
}

def load_cookie():
    """从文件加载 Cookie"""
    if not os.path.exists(COOKIE_FILE):
        return None
    with open(COOKIE_FILE, 'r') as f:
        return f.read().strip()

def extract_ctoken(cookie):
    """从 Cookie 字符串中提取 ctoken 值"""
    for item in cookie.split(';'):
        item = item.strip()
        if item.startswith('ctoken='):
            return item.split('=', 1)[1]
    return None

def make_request(url, data):
    """发送 POST 请求到友盟 API"""
    cookie = load_cookie()
    if not cookie:
        print("ERROR: 未找到 Cookie，请先登录并保存 Cookie", file=sys.stderr)
        sys.exit(1)
    
    ctoken = extract_ctoken(cookie)
    
    headers = {
        "Content-Type": "application/json;charset=UTF-8",
        "Cookie": cookie,
        "x-csrf-token": ctoken if ctoken else ""
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
            
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def query_and_display(interface_key, appkey, date_type):
    """查询并显示单个维度的数据"""
    interface = ANALYSIS_INTERFACES[interface_key]
    
    print(f"\n{interface['icon']} 正在查询 {interface['name']}...")
    
    url = interface['url']
    data = {
        "appkey": appkey,
        "datetype": date_type
    }
    
    result = make_request(url, data)
    
    if result.get('status'):
        print(f"✅ {interface['name']} 查询成功")
        display_data(interface_key, result, date_type)
        return result
    else:
        print(f"❌ {interface['name']} 查询失败：{result.get('msg', '未知错误')}")
        return None

def display_data(interface_key, result, date_type):
    """根据接口类型显示数据"""
    data = result.get('data', {})
    
    if interface_key == 'userPreference':
        # 用户偏好分析
        close_sensitivity = data.get('closeSensitivity', {})
        
        if close_sensitivity:
            print("\n【关闭敏感度分布】")
            print("-" * 80)
            
            open_duration = close_sensitivity.get('open_duration', [])
            for item in open_duration:
                name = item.get('name', 'N/A')
                ratio = item.get('ratioData', 0) or 0
                percentage = ratio * 100 if ratio <= 1 else ratio
                
                bar_length = int(percentage / 2)
                bar = "█" * bar_length + "░" * (50 - bar_length)
                
                print(f"{name:<20} {percentage:>6.2f}% |{bar}|")
            
            suggestion = close_sensitivity.get('suggestion', '')
            if suggestion:
                print(f"\n💡 建议：{suggestion}")
        
        to_close_duration = data.get('toCloseDuration', {})
        if to_close_duration:
            total = to_close_duration.get('total', 0)
            print(f"\n【关闭时间分布】(总计：{total:,})")
            print("-" * 80)
            
            duration_data = to_close_duration.get('data', [])[:7]
            for item in duration_data:
                name = item.get('name', 'N/A')
                value = item.get('value', 0) or 0
                ratio = item.get('ratioData', 0) or 0
                percentage = ratio * 100 if ratio <= 1 else ratio
                
                bar_length = int(percentage / 2)
                bar = "█" * bar_length + "░" * (50 - bar_length)
                
                print(f"{name:<15} {value:>10,}  {percentage:>6.2f}% |{bar}|")
    
    elif interface_key == 'pushFrequency':
        # 推送频次分析
        req_distribution = data.get('reqDistribution', {})
        
        if req_distribution:
            total = req_distribution.get('total', 0)
            print(f"\n【推送频次分布】(总计：{total:,})")
            print("-" * 80)
            
            freq_data = req_distribution.get('data', [])
            for item in freq_data:
                name = item.get('name', 'N/A')
                value = item.get('value', 0) or 0
                ratio = item.get('ratioData', 0) or 0
                percentage = ratio * 100 if ratio <= 1 else ratio
                
                bar_length = int(percentage / 2)
                bar = "█" * bar_length + "░" * (50 - bar_length)
                
                print(f"{name:<20} {value:>10,}  {percentage:>6.2f}% |{bar}|")
            
            suggestion = req_distribution.get('suggestion', '')
            if suggestion:
                print(f"\n💡 建议：{suggestion}")
    
    elif interface_key == 'pushMessage':
        # 通知内容分析
        msg_types = data.get('msgTypes', {})
        
        if msg_types:
            print("\n【通知类型分布】")
            print("-" * 80)
            
            type_data = msg_types.get('data', [])
            for item in type_data:
                name = item.get('name', 'N/A')
                ratio = item.get('ratioData', 0) or 0
                percentage = ratio * 100 if ratio <= 1 else ratio
                
                bar_length = int(percentage / 2)
                bar = "█" * bar_length + "░" * (50 - bar_length)
                
                print(f"{name:<30} {percentage:>6.2f}% |{bar}|")
    
    elif interface_key == 'deviceDimension':
        # 设备维度分析
        device_dist = data.get('deviceDistribution', {})
        
        if device_dist:
            print("\n【设备类型分布】")
            print("-" * 80)
            
            dev_data = device_dist.get('data', [])
            for item in dev_data:
                name = item.get('name', 'N/A')
                ratio = item.get('ratioData', 0) or 0
                percentage = ratio * 100 if ratio <= 1 else ratio
                
                bar_length = int(percentage / 2)
                bar = "█" * bar_length + "░" * (50 - bar_length)
                
                print(f"{name:<25} {percentage:>6.2f}% |{bar}|")

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法：python scripts/query_close_attribution.py <appkey> [date_type]")
        print("")
        print("参数说明:")
        print("  appkey     - 应用的唯一标识（必填）")
        print("  date_type  - 日期类型：1d(昨日) 或 7d(近 7 日)，默认 7d")
        print("")
        print("示例:")
        print("  python scripts/query_close_attribution.py EXAMPLE_APPKEY_005")
        print("  python scripts/query_close_attribution.py EXAMPLE_APPKEY_005 1d")
        sys.exit(1)
    
    appkey = sys.argv[1]
    date_type = sys.argv[2] if len(sys.argv) > 2 else "7d"
    
    if date_type not in DATE_TYPES:
        print(f"ERROR: 无效的日期类型 '{date_type}'，仅支持：1d, 7d", file=sys.stderr)
        sys.exit(1)
    
    print("=" * 80)
    print("🔍 友盟推送 - 关闭归因分析")
    print("=" * 80)
    print(f"应用 Key   : {appkey}")
    print(f"时间范围   : {DATE_TYPES.get(date_type, date_type)}")
    print("=" * 80)
    
    # 依次查询四个维度
    results = {}
    
    for key in ['userPreference', 'pushFrequency', 'pushMessage', 'deviceDimension']:
        result = query_and_display(key, appkey, date_type)
        if result:
            results[key] = result
    
    print("\n" + "=" * 80)
    print("✅ 分析完成")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
