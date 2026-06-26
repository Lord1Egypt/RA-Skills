#!/usr/bin/env python3
"""
友盟推送助手 - 获取 API 单播统计记录列表
调用 upush.umeng.com API 获取应用的 API 单播统计记录
支持分页查询
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime, timedelta

COOKIE_FILE = os.path.expanduser("~/.qoderwork/skills/umeng-push-helper/cookie.txt")

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

def query_api_statistics(appkey, page=1, page_size=15):
    """
    获取 API 单播统计记录列表
    
    Args:
        appkey: 应用的唯一标识
        page: 页码，默认 1
        page_size: 每页条数，固定 15
    """
    cookie = load_cookie()
    if not cookie:
        print("ERROR: 未找到 Cookie，请先登录并保存 Cookie", file=sys.stderr)
        sys.exit(1)
    
    url = "https://upush.umeng.com/hsf/dataStatistic/getApi"
    
    data = {
        "appkey": appkey,
        "pageIndex": page,
        "pageSize": page_size
    }
    
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
    except Exception as e:
        return {
            'success': False,
            'error': '未知错误',
            'message': str(e)
        }

def display_api_statistics(result, appkey, page, page_size):
    """展示 API 单播统计记录列表"""
    print("\n" + "=" * 140)
    print(f"📡 API 单播统计记录")
    print("=" * 140)
    print(f"应用 Key   : {appkey}")
    print("=" * 140)
    
    if not result.get('status'):
        print(f"\n❌ 查询失败：{result.get('msg', '未知错误')}")
        return None
    
    data = result.get('data', {})
    
    # 解析分页信息
    total = data.get('total', 0)
    # 计算总页数
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    curr_page = data.get('pageIndex', page)
    
    # 统计列表
    stat_list = data.get('list', [])
    
    print(f"\n📊 共有 {total} 条数据，共 {total_pages} 页，当前第 {curr_page} 页")
    print("-" * 140)
    
    if not stat_list:
        print("\n⚠️  暂无 API 单播统计记录")
        return data
    
    # 表头
    print(f"\n{'序号':<4} {'日期':<15} {'有效设备':>12} {'实际发送':>12} {'消息送达':>10} {'送达率':>8} {'消息展示':>10} {'展示率':>8} {'消息点击':>10} {'点击率':>8}")
    print("-" * 140)
    
    for i, stat in enumerate(stat_list, (page - 1) * page_size + 1):
        # 提取字段
        date = stat.get('date', 'N/A')
        
        # 数字字段 - 去除逗号
        def parse_num(val):
            if val is None:
                return 0
            if isinstance(val, str):
                return int(val.replace(',', ''))
            return val
        
        accept_count = parse_num(stat.get('acceptCount', 0))
        sent_count = parse_num(stat.get('sentCount', 0))
        arrive_count = parse_num(stat.get('arriveCount', 0))
        arrive_rate = stat.get('arriveRate', '')
        show_count = parse_num(stat.get('showCount', 0))
        show_rate = stat.get('showRate', '')
        click_count = parse_num(stat.get('clickCount', 0))
        click_rate = stat.get('clickRate', '')
        
        # 格式化输出
        print(f"{i:<4} {date:<15} {accept_count:>12,} {sent_count:>12,} {arrive_count:>10,} {arrive_rate:>8} {show_count:>10,} {show_rate:>8} {click_count:>10,} {click_rate:>8}")
    
    print("-" * 140)
    
    # 分页导航
    print(f"\n📄 分页信息：")
    print(f"   当前页：{curr_page} / {total_pages}")
    
    if curr_page > 1:
        print(f"   上一页：python scripts/query_api_statistics.py {appkey} --page {curr_page - 1}")
    else:
        print(f"   上一页：已是第一页")
    
    if curr_page < total_pages:
        print(f"   下一页：python scripts/query_api_statistics.py {appkey} --page {curr_page + 1}")
    else:
        print(f"   下一页：已是最后一页")
    
    print("=" * 140)
    
    return data

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法：python scripts/query_api_statistics.py <appkey> [options]")
        print("")
        print("参数说明:")
        print("  appkey      - 应用的唯一标识（必填）")
        print("  --page PAGE - 页码，默认 1")
        print("")
        print("示例:")
        print("  # 查询第 1 页（默认）")
        print("  python scripts/query_api_statistics.py EXAMPLE_APPKEY_006")
        print("")
        print("  # 查询第 2 页")
        print("  python scripts/query_api_statistics.py EXAMPLE_APPKEY_006 --page 2")
        sys.exit(1)
    
    appkey = sys.argv[1]
    
    # 解析可选参数
    page = 1
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--page' and i + 1 < len(sys.argv):
            try:
                page = int(sys.argv[i + 1])
                if page < 1:
                    print("ERROR: 页码必须 >= 1", file=sys.stderr)
                    sys.exit(1)
            except ValueError:
                print(f"ERROR: 无效的页码：{sys.argv[i + 1]}", file=sys.stderr)
                sys.exit(1)
            i += 2
        else:
            print(f"ERROR: 未知参数：{sys.argv[i]}", file=sys.stderr)
            sys.exit(1)
    
    # 查询 API 单播统计
    result = query_api_statistics(
        appkey=appkey,
        page=page,
        page_size=15
    )
    
    # 展示结果
    display_api_statistics(result, appkey, page, 15)

if __name__ == "__main__":
    main()
