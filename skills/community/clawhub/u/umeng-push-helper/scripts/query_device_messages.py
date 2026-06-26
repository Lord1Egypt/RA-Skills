#!/usr/bin/env python3
"""
友盟推送助手 - 根据设备查询消息列表
调用 upush.umeng.com API 查询指定设备在指定日期范围内的所有推送消息
"""

import json
import os
import sys
import urllib.request
from datetime import datetime

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
        print(f"ERROR: HTTP 错误 {e.code}", file=sys.stderr)
        print(f"详情：{e.reason}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"ERROR: 网络错误", file=sys.stderr)
        print(f"详情：{e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

def query_device_messages(appkey, device_token, start_date, end_date, page=1, page_size=50):
    """
    查询设备消息列表
    
    Args:
        appkey: 应用 key
        device_token: 设备 token
        start_date: 开始日期 (yyyy-MM-dd)
        end_date: 结束日期 (yyyy-MM-dd)
        page: 页码，默认 1
        page_size: 每页数量，默认 50
    """
    url = "https://upush.umeng.com/hsf/setting/deviceMessage"
    data = {
        "appkey": appkey,
        "deviceToken": device_token,
        "startDate": start_date,
        "endDate": end_date,
        "page": page,
        "pageSize": page_size
    }
    
    print(f"\n{'='*100}")
    print(f"📱 友盟推送 - 设备消息列表查询")
    print(f"{'='*100}")
    print(f"应用 Key     : {appkey}")
    print(f"设备 Token   : {device_token}")
    print(f"日期范围    : {start_date} 至 {end_date}")
    print(f"页码        : {page}")
    print(f"每页数量    : {page_size}")
    print(f"{'='*100}\n")
    
    print(f"接口：{url}")
    print(f"请求参数:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    result = make_request(url, data)
    
    print(f"\n返回结果:")
    if result.get('status'):
        data_result = result.get('data', {})
        total = data_result.get('total', 0)
        curr_page = data_result.get('currPage', page)
        messages = data_result.get('list', [])
        
        print(f"\n✅ 共查询到 {total} 条消息\n")
        
        if not messages:
            print("暂无数据")
            return
        
        # 显示消息列表
        print(f"{'序号':<6} {'消息 ID':<25} {'标题':<20} {'发送时间':<20} {'状态':<12} {'通道':<10}")
        print(f"{'-'*100}")
        
        for i, msg in enumerate(messages, 1):
            msg_id_item = msg.get('msgId', 'N/A')[:22]
            
            # 从 digest 中解析标题
            title = 'N/A'
            try:
                digest = json.loads(msg.get('digest', '{}'))
                body = digest.get('body', {})
                title = body.get('title', 'N/A') or 'N/A'
            except:
                title = 'N/A'
            
            send_time = msg.get('startTime', 'N/A')
            status = msg.get('status', 'N/A')
            channel = msg.get('channel', 'N/A')
            
            print(f"{i:<6} {msg_id_item:<25} {title:<20} {send_time:<20} {status:<12} {channel:<10}")
        
        print(f"\n{'='*100}")
        print(f"本页显示 {len(messages)} 条消息（第 {(page-1)*page_size+1}-{(page-1)*page_size+len(messages)} 条）")
        
        # 计算总页数
        total_pages = (total + page_size - 1) // page_size if total > 0 else 1
        print(f"总页数：{total_pages}")
        
        if page < total_pages:
            print(f"下一页：python scripts/query_device_messages.py {appkey} {device_token} {start_date} {end_date} --page {page + 1}")
        else:
            print("已是最后一页")
        
        if page > 1:
            print(f"上一页：python scripts/query_device_messages.py {appkey} {device_token} {start_date} {end_date} --page {page - 1}")
        
        print(f"{'='*100}\n")
    else:
        print(f"查询失败：{result.get('msg', '未知错误')}")
        print(json.dumps(result, indent=2, ensure_ascii=False))

def main():
    """主函数"""
    if len(sys.argv) < 5:
        print("\n" + "="*100)
        print("友盟推送 - 设备消息列表查询工具")
        print("="*100)
        print("\n📱 功能说明：")
        print("   根据设备 token 查询指定日期范围内的所有推送消息列表")
        print("\n🔧 用法：python scripts/query_device_messages.py <appkey> <device_token> <start_date> <end_date> [选项]")
        print("\n示例:")
        print("  # 查询今天的所有推送")
        print("  python scripts/query_device_messages.py <appkey> <device_token> 2026-04-01 2026-04-01")
        print("\n  # 查询指定日期范围")
        print("  python scripts/query_device_messages.py <appkey> <device_token> 2026-04-01 2026-04-02")
        print("\n  # 查询第 2 页")
        print("  python scripts/query_device_messages.py <appkey> <device_token> 2026-04-01 2026-04-01 --page 2")
        print("\n  # 自定义每页数量")
        print("  python scripts/query_device_messages.py <appkey> <device_token> 2026-04-01 2026-04-01 --page-size 100")
        print("\n参数说明:")
        print("  appkey       - 应用的唯一标识")
        print("  device_token - 设备的推送 token")
        print("  start_date   - 开始日期，格式：yyyy-MM-dd")
        print("  end_date     - 结束日期，格式：yyyy-MM-dd")
        print("\n选项:")
        print("  --page PAGE        页码，默认 1")
        print("  --page-size SIZE   每页数量，默认 50（最大 100）")
        print("="*100 + "\n")
        sys.exit(1)
    
    # 解析位置参数
    appkey = sys.argv[1]
    device_token = sys.argv[2]
    start_date = sys.argv[3]
    end_date = sys.argv[4]
    
    # 解析选项参数
    page = 1
    page_size = 50
    
    args = sys.argv[5:]
    i = 0
    while i < len(args):
        if args[i] == '--page' and i + 1 < len(args):
            try:
                page = int(args[i + 1])
                if page < 1:
                    print("ERROR: 页码必须 >= 1", file=sys.stderr)
                    sys.exit(1)
            except ValueError:
                print(f"ERROR: 无效的页码：{args[i + 1]}", file=sys.stderr)
                sys.exit(1)
            i += 2
        elif args[i] == '--page-size' and i + 1 < len(args):
            try:
                page_size = int(args[i + 1])
                if page_size < 1 or page_size > 100:
                    print("ERROR: 每页数量必须在 1-100 之间", file=sys.stderr)
                    sys.exit(1)
            except ValueError:
                print(f"ERROR: 无效的每页数量：{args[i + 1]}", file=sys.stderr)
                sys.exit(1)
            i += 2
        else:
            print(f"ERROR: 无效参数：{args[i]}", file=sys.stderr)
            sys.exit(1)
    
    query_device_messages(appkey, device_token, start_date, end_date, page, page_size)

if __name__ == "__main__":
    main()
