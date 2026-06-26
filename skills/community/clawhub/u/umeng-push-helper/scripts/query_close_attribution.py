#!/usr/bin/env python3
"""
友盟推送助手 - 关闭归因分析
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
    """
    发送 POST 请求到友盟 API
    
    Args:
        url: API URL
        data: 请求数据字典
    
    Returns:
        解析后的 JSON 响应
    """
    cookie = load_cookie()
    if not cookie:
        print("ERROR: 未找到 Cookie，请先登录并保存 Cookie", file=sys.stderr)
        sys.exit(1)
    
    # 提取 ctoken 用于 x-csrf-token 头
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
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8') if e.fp else ''
        return {
            'success': False,
            'error': f'HTTP {e.code}',
            'message': error_body
        }
    except urllib.error.URLError as e:
        return {
            'success': False,
            'error': '网络错误',
            'message': str(e.reason)
        }
    except Exception as e:
        return {
            'success': False,
            'error': '未知错误',
            'message': str(e)
        }

def query_user_preference(appkey, date_type):
    """查询用户偏好分析"""
    url = ANALYSIS_INTERFACES['userPreference']['url']
    data = {
        "appkey": appkey,
        "datetype": date_type
    }
    
    result = make_request(url, data)
    return result

def query_push_frequency(appkey, date_type):
    """查询推送频次分析"""
    url = ANALYSIS_INTERFACES['pushFrequency']['url']
    data = {
        "appkey": appkey,
        "datetype": date_type
    }
    
    result = make_request(url, data)
    return result

def query_push_message(appkey, date_type):
    """查询通知内容分析"""
    url = ANALYSIS_INTERFACES['pushMessage']['url']
    data = {
        "appkey": appkey,
        "datetype": date_type
    }
    
    result = make_request(url, data)
    return result

def query_device_dimension(appkey, date_type):
    """查询设备维度分析"""
    url = ANALYSIS_INTERFACES['deviceDimension']['url']
    data = {
        "appkey": appkey,
        "datetype": date_type
    }
    
    result = make_request(url, data)
    return result

def display_user_preference(result, date_type):
    """展示用户偏好分析结果"""
    print("\n" + "=" * 80)
    print(f"👤 用户偏好分析 ({DATE_TYPES.get(date_type, date_type)})")
    print("=" * 80)
    
    if not result.get('status'):
        print(f"❌ 查询失败：{result.get('msg', '未知错误')}")
        return None
    
    data = result.get('data', {})
    
    # 解析关闭敏感度数据
    close_sensitivity = data.get('closeSensitivity', {})
    
    if close_sensitivity:
        # 1. 持续打开通知栏权限用户的敏感度分布
        open_duration = close_sensitivity.get('open_duration', [])
        if open_duration:
            print("\n【持续打开通知栏权限用户的敏感度分布】")
            print("-" * 80)
            
            for i, item in enumerate(open_duration, 1):
                name = item.get('name', 'N/A')
                value = item.get('value')  # 可能为 null
                ratio = item.get('ratioData', 0) or 0
                percentage = ratio * 100 if ratio <= 1 else ratio
                
                bar_length = int(percentage / 2)
                bar = "█" * bar_length + "░" * (50 - bar_length)
                
                # 如果 value 为 null，只显示百分比
                if value is not None:
                    print(f"{i}. {name:<20} {value:>10,}  {percentage:>6.2f}% |{bar}|")
                else:
                    print(f"{i}. {name:<20} {percentage:>6.2f}% |{bar}|")
            
            print("-" * 80)
        
        # 2. 新增关闭设备用户的敏感度分布
        close_new = close_sensitivity.get('close_new', [])
        if close_new:
            print("\n【新增关闭设备用户的敏感度分布】")
            print("-" * 80)
            
            for i, item in enumerate(close_new, 1):
                name = item.get('name', 'N/A')
                value = item.get('value')  # 可能为 null
                ratio = item.get('ratioData', 0) or 0
                percentage = ratio * 100 if ratio <= 1 else ratio
                
                bar_length = int(percentage / 2)
                bar = "█" * bar_length + "░" * (50 - bar_length)
                
                # 如果 value 为 null，只显示百分比
                if value is not None:
                    print(f"{i}. {name:<20} {value:>10,}  {percentage:>6.2f}% |{bar}|")
                else:
                    print(f"{i}. {name:<20} {percentage:>6.2f}% |{bar}|")
            
            print("-" * 80)
        
        # 显示建议
        suggestion = close_sensitivity.get('suggestion', '')
        if suggestion:
            print(f"\n💡 建议：{suggestion}")
    
    # 解析关闭时长分布
    to_close_duration = data.get('toCloseDuration', {})
    if to_close_duration:
        total = to_close_duration.get('total', 0)
        print(f"\n【关闭时间分布】(总计：{total:,})")
        print("-" * 80)
        
        duration_data = to_close_duration.get('data', [])
        for i, item in enumerate(duration_data[:7], 1):  # 只显示前 7 项
            name = item.get('name', 'N/A')
            value = item.get('value', 0) or 0
            ratio = item.get('ratioData', 0) or 0
            percentage = ratio * 100 if ratio <= 1 else ratio
            
            bar_length = int(percentage / 2)
            bar = "█" * bar_length + "░" * (50 - bar_length)
            
            print(f"{i}. {name:<15} {value:>10,}  {percentage:>6.2f}% |{bar}|")
        
        print("-" * 80)
    
    return data

def display_push_frequency(result, date_type):
    """展示推送频次分析结果"""
    print("\n" + "=" * 80)
    print(f"📱 推送频次分析 ({DATE_TYPES.get(date_type, date_type)})")
    print("=" * 80)
    
    if not result.get('status'):
        print(f"❌ 查询失败：{result.get('msg', '未知错误')}")
        return
    
    data = result.get('data', {})
    
    # 解析频次数据
    if isinstance(data, dict) and 'list' in data:
        items = data['list']
        
        print("\n【推送频次与关闭关系】")
        print("-" * 80)
        
        for i, item in enumerate(items, 1):
            name = item.get('name', 'N/A')
            value = item.get('value', 0)
            percentage = item.get('percentage', 0)
            
            bar_length = int(percentage / 2)
            bar = "█" * bar_length + "░" * (50 - bar_length)
            
            print(f"{i}. {name:<25} {value:>10}  {percentage:>6.2f}% |{bar}|")
        
        print("-" * 80)
    
    return data

def display_push_message(result, date_type):
    """展示通知内容分析结果（表格形式）"""
    print("\n" + "=" * 80)
    print(f"📝 通知内容分析 ({DATE_TYPES.get(date_type, date_type)})")
    print("=" * 80)
    
    if not result.get('status'):
        print(f"❌ 查询失败：{result.get('msg', '未知错误')}")
        return None
    
    data = result.get('data', {})
    
    # 以表格形式展示 - data 可能是 list 或包含 list 的 dict
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict) and 'list' in data:
        items = data['list']
    
    if len(items) > 0:
        print("\n【不同通知类型的关闭情况】")
        print("-" * 160)
        print(f"{'序号':<4} {'任务描述':<50} {'目标人群':<10} {'发送时间':<18} {'通知标题':<15} {'通知内容':<30} {'点击数':>8} {'关闭数':>8} {'效果比':>10} {'消息 ID':<25}")
        print("-" * 160)
        
        for i, item in enumerate(items[:20], 1):  # 只显示前 20 条
            description = item.get('description', 'N/A')[:48] + '..' if len(item.get('description', '')) > 48 else item.get('description', 'N/A')
            target = item.get('target', 'N/A')
            push_time = item.get('pushTime', 'N/A')
            title = item.get('title', 'N/A')
            text = item.get('text', '')[:28] + '...' if len(item.get('text', '')) > 28 else item.get('text', '')
            click_num = item.get('clickNum', 0)
            close_num = item.get('closeNum', 0)
            effect_ratio = item.get('effectRatio', 0)
            msg_id = item.get('msgId', 'N/A')
            
            print(f"{i:<4} {description:<50} {target:<10} {push_time:<18} {title:<15} {text:<30} {click_num:>8,} {close_num:>8,} {effect_ratio:>9.1f}% {msg_id:<25}")
        
        print("-" * 160)
        if len(items) > 20:
            print(f"... 还有 {len(items) - 20} 条数据未显示")
    else:
        print("\n⚠️  暂无通知内容分析数据（该应用可能未产生相关数据）")
    
    return data

def display_device_dimension(result, date_type):
    """展示设备维度分析结果"""
    print("\n" + "=" * 80)
    print(f"📲 设备维度分析 ({DATE_TYPES.get(date_type, date_type)})")
    print("=" * 80)
    
    if not result.get('status'):
        print(f"❌ 查询失败：{result.get('msg', '未知错误')}")
        return None
    
    data = result.get('data', {})
    
    # 检查是否有数据 - 数据可能是多个维度的字典
    has_data = False
    if isinstance(data, dict):
        # 检查是否有任何一个维度有数据
        for key in ['appVersion', 'osVersion', 'brandVersion', 'deviceModel']:
            if key in data and isinstance(data[key], list) and len(data[key]) > 0:
                has_data = True
                break
    
    if has_data:
        # 解析各个维度数据
        dimensions = {
            'brandVersion': '📱 手机品牌分布',
            'osVersion': '💻 OS 版本分布',
            'appVersion': '📦 应用版本分布',
            'deviceModel': '🔧 设备型号分布'
        }
        
        for dim_key, dim_name in dimensions.items():
            if dim_key in data and isinstance(data[dim_key], list) and len(data[dim_key]) > 0:
                items = data[dim_key]
                
                # 过滤出 addClose 类型的数据（新增关闭）
                close_items = [item for item in items if item.get('type') == 'addClose']
                
                if close_items:
                    print(f"\n【{dim_name}】(新增关闭设备)")
                    print("-" * 100)
                    print(f"{'序号':<4} {'名称':<25} {'关闭数':>12} {'占比':>10} {'趋势':>30}")
                    print("-" * 100)
                    
                    # 按关闭数排序
                    close_items.sort(key=lambda x: x.get('value', 0), reverse=True)
                    
                    total_close = sum(item.get('value', 0) for item in close_items)
                    
                    for i, item in enumerate(close_items[:15], 1):  # 只显示前 15 条
                        name = item.get('name', 'N/A')  # 直接使用接口返回的名称
                        value = item.get('value', 0)
                        ratio = item.get('ratioData', 0) or 0
                        percentage = ratio * 100 if ratio <= 1 else ratio
                        
                        # 计算占关闭总数的比例
                        close_percentage = (value / total_close * 100) if total_close > 0 else 0
                        
                        bar_length = int(close_percentage / 2)
                        bar = "█" * bar_length + "░" * (50 - bar_length)
                        
                        # 趋势箭头
                        trend = "⬆️" if close_percentage > 10 else "➡️" if close_percentage > 5 else "⬇️"
                        
                        print(f"{i:<4} {name:<25} {value:>12,} {close_percentage:>9.2f}% {trend:>30}")
                    
                    print("-" * 100)
                    if len(close_items) > 15:
                        print(f"... 还有 {len(close_items) - 15} 个{dim_name.split()[1]}未显示")
    else:
        print("\n⚠️  暂无设备维度分析数据（该应用可能未产生相关数据）")
    
    return data

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
        print("  # 查询近 7 日数据（默认）")
        print("  python scripts/query_close_attribution.py EXAMPLE_APPKEY_005")
        print("")
        print("  # 查询昨日数据")
        print("  python scripts/query_close_attribution.py EXAMPLE_APPKEY_005 1d")
        print("")
        print("  # 查询近 7 日数据")
        print("  python scripts/query_close_attribution.py EXAMPLE_APPKEY_005 7d")
        sys.exit(1)
    
    appkey = sys.argv[1]
    date_type = sys.argv[2] if len(sys.argv) > 2 else "7d"
    
    # 验证日期类型
    if date_type not in DATE_TYPES:
        print(f"ERROR: 无效的日期类型 '{date_type}'，仅支持：1d, 7d", file=sys.stderr)
        sys.exit(1)
    
    print("=" * 80)
    print("🔍 友盟推送 - 关闭归因分析")
    print("=" * 80)
    print(f"应用 Key   : {appkey}")
    print(f"时间范围   : {DATE_TYPES.get(date_type, date_type)}")
    print("=" * 80)
    
    # 依次调用四个接口
    all_results = {}
    
    # 1. 用户偏好分析
    print(f"\n{ANALYSIS_INTERFACES['userPreference']['icon']} 正在查询 {ANALYSIS_INTERFACES['userPreference']['name']}...")
    result = query_user_preference(appkey, date_type)
    if result.get('status'):
        print(f"✅ {ANALYSIS_INTERFACES['userPreference']['name']} 查询成功")
        all_results['userPreference'] = result
        display_user_preference(result, date_type)
    else:
        print(f"❌ {ANALYSIS_INTERFACES['userPreference']['name']} 查询失败：{result.get('msg', '未知错误')}")
    
    # 2. 推送频次分析
    print(f"\n{ANALYSIS_INTERFACES['pushFrequency']['icon']} 正在查询 {ANALYSIS_INTERFACES['pushFrequency']['name']}...")
    result = query_push_frequency(appkey, date_type)
    if result.get('status'):
        print(f"✅ {ANALYSIS_INTERFACES['pushFrequency']['name']} 查询成功")
        all_results['pushFrequency'] = result
        display_push_frequency(result, date_type)
    else:
        print(f"❌ {ANALYSIS_INTERFACES['pushFrequency']['name']} 查询失败：{result.get('msg', '未知错误')}")
    
    # 3. 通知内容分析
    print(f"\n{ANALYSIS_INTERFACES['pushMessage']['icon']} 正在查询 {ANALYSIS_INTERFACES['pushMessage']['name']}...")
    result = query_push_message(appkey, date_type)
    if result.get('status'):
        print(f"✅ {ANALYSIS_INTERFACES['pushMessage']['name']} 查询成功")
        all_results['pushMessage'] = result
        display_push_message(result, date_type)
    else:
        print(f"❌ {ANALYSIS_INTERFACES['pushMessage']['name']} 查询失败：{result.get('msg', '未知错误')}")
    
    # 4. 设备维度分析
    print(f"\n{ANALYSIS_INTERFACES['deviceDimension']['icon']} 正在查询 {ANALYSIS_INTERFACES['deviceDimension']['name']}...")
    result = query_device_dimension(appkey, date_type)
    if result.get('status'):
        print(f"✅ {ANALYSIS_INTERFACES['deviceDimension']['name']} 查询成功")
        all_results['deviceDimension'] = result
        display_device_dimension(result, date_type)
    else:
        print(f"❌ {ANALYSIS_INTERFACES['deviceDimension']['name']} 查询失败：{result.get('msg', '未知错误')}")
    
    print("\n" + "=" * 80)
    print("✅ 分析完成")
    print("=" * 80 + "\n")

if __name__ == "__main__":
    main()
