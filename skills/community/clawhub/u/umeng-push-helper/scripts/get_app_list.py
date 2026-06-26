#!/usr/bin/env python3
"""
友盟推送助手 - 获取应用列表
调用 upush.umeng.com API 获取账号下的应用列表
支持分页功能，默认显示第 1 页
"""

import json
import os
import sys
import urllib.request
import urllib.error

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

def get_app_list(page=1):
    """
    获取应用列表
    
    Args:
        page: 页码，默认为 1
    """
    per_page = 15  # 固定每页 15 条记录
    
    cookie = load_cookie()
    if not cookie:
        print("ERROR: 未找到 Cookie，请先登录并保存 Cookie", file=sys.stderr)
        sys.exit(1)
    
    url = "https://upush.umeng.com/hsf/home/listAll"
    
    data = {
        "appkey": "",
        "platform": "all",
        "page": page,
        "perPage": per_page,
        "hasPush": 0,
        "appName": "",
        "yearQuotaSts": 0
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
            
            # 解析响应数据
            if 'data' in result and 'appList' in result['data']:
                app_list = result['data']['appList']
                
                # 从返回结果中解析分页信息
                total = result['data'].get('total', len(app_list))
                total_pages = result['data'].get('totalPage', 1)
                curr_page = result['data'].get('currPage', page)
                
                if not app_list:
                    print(f"\n提示：第 {page} 页暂无数据")
                    return
                
                # 输出分页信息
                print(f"\n{'='*120}")
                print(f"账号下共有 {total} 个应用，共分 {total_pages} 页，当前处于第 {curr_page} 页")
                print(f"{'='*120}\n")
                
                # 显示应用列表（表格形式）- 确保 appkey 完整显示
                print(f"{'序号':<4} {'appkey':<26} {'应用名称':<50} {'平台':<10} {'DAU':>12}")
                print(f"{'-'*120}")
                
                start_num = (page - 1) * per_page + 1
                for i, app in enumerate(app_list, start_num):
                    appkey = app.get('appkey', 'N/A')
                    app_name = app.get('appName', 'N/A')
                    platform = app.get('platform', 'N/A')
                    dau = app.get('dau', '0')
                    # 格式化 DAU，添加千位分隔符
                    try:
                        dau_formatted = f"{int(dau):,}" if dau and dau != '-' else dau
                    except (ValueError, TypeError):
                        dau_formatted = str(dau)
                    print(f"{i:<4} {appkey:<26} {app_name:<50} {platform:<10} {dau_formatted:>12}")
                
                # 输出分页提示
                print(f"\n{'='*120}")
                print(f"本页显示 {len(app_list)} 个应用（第 {start_num}-{start_num + len(app_list) - 1} 个）")
                
                if page < total_pages:
                    print(f"下一页：python scripts/get_app_list.py --page {page + 1}")
                else:
                    print("已是最后一页")
                
                if page > 1:
                    print(f"上一页：python scripts/get_app_list.py --page {page - 1}")
                
                print(f"{'='*120}\n")
            else:
                print("ERROR: 响应格式异常", file=sys.stderr)
                print(json.dumps(result, indent=2, ensure_ascii=False))
                sys.exit(1)
                
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

if __name__ == "__main__":
    # 解析命令行参数
    page = 1
    
    args = sys.argv[1:]
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
        else:
            # 兼容旧版本，直接传入页码数字
            try:
                page = int(args[i])
                if page < 1:
                    print("ERROR: 页码必须 >= 1", file=sys.stderr)
                    sys.exit(1)
            except ValueError:
                print(f"ERROR: 无效参数：{args[i]}", file=sys.stderr)
                print("用法：python scripts/get_app_list.py [--page PAGE]")
                print("示例:")
                print("  python scripts/get_app_list.py              # 显示第 1 页（默认）")
                print("  python scripts/get_app_list.py 2            # 显示第 2 页")
                print("  python scripts/get_app_list.py --page 3     # 显示第 3 页")
                sys.exit(1)
            i += 1
    
    get_app_list(page)
