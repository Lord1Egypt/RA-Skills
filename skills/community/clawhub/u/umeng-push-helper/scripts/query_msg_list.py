#!/usr/bin/env python3
"""
友盟推送助手 - 获取消息列表
调用 upush.umeng.com API 获取指定应用的消息列表
支持分页和日期范围筛选
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

def query_msg_list(appkey, page=1, page_size=15, start_time="", end_time="", production_mode=True, display_type=0, description=""):
    """
    获取消息列表
    
    Args:
        appkey: 应用的唯一标识
        page: 页码，默认 1
        page_size: 每页条数，固定 15
        start_time: 开始时间，格式 yyyy-MM-dd
        end_time: 结束时间，格式 yyyy-MM-dd
        production_mode: 是否生产模式，默认 True
        display_type: 展示类型，默认 0
        description: 任务描述筛选
    """
    cookie = load_cookie()
    if not cookie:
        print("ERROR: 未找到 Cookie，请先登录并保存 Cookie", file=sys.stderr)
        sys.exit(1)
    
    url = "https://upush.umeng.com/hsf/push/getMsgList"
    
    # 计算默认时间范围：如果未提供，则 start_time 为当前时间往前推 15 天，end_time 为当天
    if not end_time:
        end_time = datetime.now().strftime("%Y-%m-%d")
    if not start_time:
        start_time = (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d")
    
    data = {
        "appkey": appkey,
        "productionMode": production_mode,
        "displayType": display_type,
        "description": description,
        "timeSelectorType": 1,
        "startTime": start_time,
        "endTime": end_time,
        "appGroup": False,
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

def display_msg_list(result, appkey, start_time, end_time, page, page_size):
    """展示消息列表 - 明细表格模式 + 逐条详情"""
    print("\n" + "=" * 260)
    print(f"📨 友盟推送 - 消息列表（任务粒度）")
    print("=" * 260)
    print(f"应用 Key   : {appkey}")
    print(f"时间范围   : {start_time} ~ {end_time}")
    print("=" * 260)
    
    if not result.get('status'):
        print(f"\n❌ 查询失败：{result.get('msg', '未知错误')}")
        return None
    
    data = result.get('data', {})
    
    total = data.get('total', 0)
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    curr_page = data.get('pageIndex', page)
    
    msg_list = data.get('msgSketchVOList', [])
    
    print(f"\n📊 共有 {total} 条数据，共 {total_pages} 页，当前第 {curr_page} 页")
    print("=" * 260)
    
    if not msg_list:
        print("\n⚠️  该时间范围内暂无消息数据")
        return data
    
    # 第一部分：汇总表
    print("\n【汇总表格】")
    header = (
        f"{'序号':>4} | "
        f"{'任务描述':<20} | "
        f"{'目标人群':<10} | "
        f"{'发送时间':<19} | "
        f"{'计划发送':>12} | "
        f"{'有效设备':>12} | "
        f"{'实际发送':>12} | "
        f"{'消息送达':>12} | "
        f"{'送达率':>8} | "
        f"{'消息展示':>12} | "
        f"{'展示率':>8} | "
        f"{'消息点击':>10} | "
        f"{'送达点击率':>10} | "
        f"{'展示点击率':>10} | "
        f"{'消息忽略':>10} | "
        f"{'忽略率':>8}"
    )
    print(header)
    print("-" * 260)
    
    for i, msg in enumerate(msg_list, (page - 1) * page_size + 1):
        description_raw = msg.get('description') or msg.get('title') or ''
        description = description_raw[:20]
        target = msg.get('target', 'N/A')[:10]
        send_time = msg.get('pushTime', 'N/A')
        
        def parse_num(val):
            if val is None:
                return 0
            if isinstance(val, str):
                return int(val.replace(',', ''))
            return val
        
        total_count = parse_num(msg.get('totalCount', 0))
        valid_devices = parse_num(msg.get('acceptCount', 0))
        actual_send = parse_num(msg.get('sentCount', 0))
        arrive_cnt = parse_num(msg.get('arriveCount', 0))
        show_cnt = parse_num(msg.get('showCount', 0))
        click_cnt = parse_num(msg.get('clickCount', 0))
        ignore_cnt = parse_num(msg.get('ignoreCount', 0))
        
        arrive_rate = msg.get('arriveRate', '')
        show_rate = msg.get('showRate', '')
        click_rate = msg.get('clickRate', '')
        click_rate_on_show = msg.get('clickRateOnShow', '')
        ignore_rate = msg.get('ignoreRate', '')
        
        row = (
            f"{i:>4} | "
            f"{description:<20} | "
            f"{target:<10} | "
            f"{send_time:<19} | "
            f"{total_count:>12,} | "
            f"{valid_devices:>12,} | "
            f"{actual_send:>12,} | "
            f"{arrive_cnt:>12,} | "
            f"{arrive_rate:>8} | "
            f"{show_cnt:>12,} | "
            f"{show_rate:>8} | "
            f"{click_cnt:>10,} | "
            f"{str(click_rate):>10} | "
            f"{str(click_rate_on_show):>10} | "
            f"{ignore_cnt:>10,} | "
            f"{ignore_rate:>8}"
        )
        print(row)
    
    print("-" * 260)
    
    # 第二部分：逐条明细详情
    print("\n【明细详情 - 逐条展示】")
    print("=" * 260)
    
    for i, msg in enumerate(msg_list, (page - 1) * page_size + 1):
        def parse_num(val):
            if val is None:
                return 0
            if isinstance(val, str):
                return int(val.replace(',', ''))
            return val
        
        description = msg.get('description') or msg.get('title') or ''
        target = msg.get('target', 'N/A')
        create_time = msg.get('createTime', 'N/A')
        send_time = msg.get('pushTime', 'N/A')
        
        total_count = parse_num(msg.get('totalCount', 0))
        valid_devices = parse_num(msg.get('acceptCount', 0))
        actual_send = parse_num(msg.get('sentCount', 0))
        arrive_cnt = parse_num(msg.get('arriveCount', 0))
        show_cnt = parse_num(msg.get('showCount', 0))
        click_cnt = parse_num(msg.get('clickCount', 0))
        ignore_cnt = parse_num(msg.get('ignoreCount', 0))
        
        arrive_rate = msg.get('arriveRate', '')
        show_rate = msg.get('showRate', '')
        click_rate = msg.get('clickRate', '')
        click_rate_on_show = msg.get('clickRateOnShow', '')
        ignore_rate = msg.get('ignoreRate', '')
        
        # 获取其他可能的字段
        status = msg.get('status', 'N/A')
        msg_id = msg.get('msgId', 'N/A')
        push_type = msg.get('type', 'N/A')
        production_mode_val = msg.get('productionMode', 'N/A')
        display_type_val = msg.get('displayType', 'N/A')
        app_group = msg.get('appGroup', 'N/A')
        
        print(f"\n--- 第 {i} 条消息明细 ---")
        print(f"  任务描述     : {description}")
        print(f"  目标人群     : {target}")
        print(f"  消息 ID      : {msg_id}")
        print(f"  推送类型     : {push_type}")
        print(f"  推送状态     : {status}")
        print(f"  创建时间     : {create_time}")
        print(f"  发送时间     : {send_time}")
        print(f"  ─────────────────────────────────────────")
        print(f"  计划发送     : {total_count:,}")
        print(f"  有效设备     : {valid_devices:,}")
        print(f"  实际发送     : {actual_send:,}")
        print(f"  ─────────────────────────────────────────")
        print(f"  消息送达     : {arrive_cnt:,}")
        if arrive_rate:
            print(f"  送达率       : {arrive_rate}")
        print(f"  消息展示     : {show_cnt:,}")
        if show_rate:
            print(f"  展示率       : {show_rate}")
        print(f"  消息点击     : {click_cnt:,}")
        if click_rate:
            print(f"  送达点击率   : {click_rate}")
        if click_rate_on_show:
            print(f"  展示点击率   : {click_rate_on_show}")
        print(f"  消息忽略     : {ignore_cnt:,}")
        if ignore_rate:
            print(f"  忽略率       : {ignore_rate}")
        print("=" * 260)
    
    # 分页导航
    print(f"\n📄 分页信息：")
    print(f"   当前页：{curr_page} / {total_pages}")
    
    if curr_page > 1:
        print(f"   上一页：python scripts/query_msg_list.py {appkey} --page {curr_page - 1}")
    else:
        print(f"   上一页：已是第一页")
    
    if curr_page < total_pages:
        print(f"   下一页：python scripts/query_msg_list.py {appkey} --page {curr_page + 1}")
    else:
        print(f"   下一页：已是最后一页")
    
    print("=" * 260)
    
    return data

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
    """展示 API 单播统计记录 - 明细表格模式 + 逐条详情"""
    print("\n" + "=" * 200)
    print(f"📡 API 单播统计记录")
    print("=" * 200)
    print(f"应用 Key   : {appkey}")
    print("=" * 200)
    
    if not result.get('status'):
        print(f"\n❌ 查询失败：{result.get('msg', '未知错误')}")
        return None
    
    data = result.get('data', {})
    
    total = data.get('total', 0)
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    curr_page = data.get('pageIndex', page)
    
    stat_list = data.get('list', [])
    
    print(f"\n📊 共有 {total} 条数据，共 {total_pages} 页，当前第 {curr_page} 页")
    print("=" * 200)
    
    if not stat_list:
        print("\n⚠️  暂无 API 单播统计记录")
        return data
    
    # 第一部分：汇总表
    print("\n【汇总表格】")
    header = (
        f"{'序号':>4} | "
        f"{'日期':<12} | "
        f"{'有效设备':>12} | "
        f"{'实际发送':>12} | "
        f"{'消息送达':>12} | "
        f"{'送达率':>8} | "
        f"{'消息展示':>12} | "
        f"{'展示率':>8} | "
        f"{'消息点击':>10} | "
        f"{'送达点击率':>10} | "
        f"{'展示点击率':>10} | "
        f"{'消息忽略':>10} | "
        f"{'忽略率':>8}"
    )
    print(header)
    print("-" * 200)
    
    for i, stat in enumerate(stat_list, (page - 1) * page_size + 1):
        date = stat.get('date', 'N/A')
        
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
        click_rate_on_show = stat.get('clickRateOnShow', '')
        ignore_count = parse_num(stat.get('ignoreCount', 0))
        ignore_rate = stat.get('ignoreRate', '')
        
        row = (
            f"{i:>4} | "
            f"{date:<12} | "
            f"{accept_count:>12,} | "
            f"{sent_count:>12,} | "
            f"{arrive_count:>12,} | "
            f"{arrive_rate:>8} | "
            f"{show_count:>12,} | "
            f"{show_rate:>8} | "
            f"{click_count:>10,} | "
            f"{str(click_rate):>10} | "
            f"{str(click_rate_on_show):>10} | "
            f"{ignore_count:>10,} | "
            f"{ignore_rate:>8}"
        )
        print(row)
    
    print("-" * 200)
    
    # 第二部分：逐条明细详情
    print("\n【明细详情 - 逐条展示】")
    print("=" * 200)
    
    for i, stat in enumerate(stat_list, (page - 1) * page_size + 1):
        def parse_num(val):
            if val is None:
                return 0
            if isinstance(val, str):
                return int(val.replace(',', ''))
            return val
        
        date = stat.get('date', 'N/A')
        accept_count = parse_num(stat.get('acceptCount', 0))
        sent_count = parse_num(stat.get('sentCount', 0))
        arrive_count = parse_num(stat.get('arriveCount', 0))
        arrive_rate = stat.get('arriveRate', '')
        show_count = parse_num(stat.get('showCount', 0))
        show_rate = stat.get('showRate', '')
        click_count = parse_num(stat.get('clickCount', 0))
        click_rate = stat.get('clickRate', '')
        click_rate_on_show = stat.get('clickRateOnShow', '')
        ignore_count = parse_num(stat.get('ignoreCount', 0))
        ignore_rate = stat.get('ignoreRate', '')
        
        print(f"\n--- 第 {i} 条 API 单播统计明细 ---")
        print(f"  日期         : {date}")
        print(f"  ─────────────────────────────────────────")
        print(f"  有效设备     : {accept_count:,}")
        print(f"  实际发送     : {sent_count:,}")
        print(f"  ─────────────────────────────────────────")
        print(f"  消息送达     : {arrive_count:,}")
        if arrive_rate:
            print(f"  送达率       : {arrive_rate}")
        print(f"  消息展示     : {show_count:,}")
        if show_rate:
            print(f"  展示率       : {show_rate}")
        print(f"  消息点击     : {click_count:,}")
        if click_rate:
            print(f"  送达点击率   : {click_rate}")
        if click_rate_on_show:
            print(f"  展示点击率   : {click_rate_on_show}")
        print(f"  消息忽略     : {ignore_count:,}")
        if ignore_rate:
            print(f"  忽略率       : {ignore_rate}")
        print("=" * 200)
    
    # 分页导航
    print(f"\n📄 分页信息：")
    print(f"   当前页：{curr_page} / {total_pages}")
    
    if curr_page > 1:
        print(f"   上一页：python scripts/query_msg_list.py {appkey} --api-page {curr_page - 1}")
    else:
        print(f"   上一页：已是第一页")
    
    if curr_page < total_pages:
        print(f"   下一页：python scripts/query_msg_list.py {appkey} --api-page {curr_page + 1}")
    else:
        print(f"   下一页：已是最后一页")
    
    print("=" * 200)
    
    return data

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法：python scripts/query_msg_list.py <appkey> [options]")
        print("")
        print("参数说明:")
        print("  appkey              - 应用的唯一标识（必填）")
        print("  --page PAGE         - 任务列表页码，默认 1")
        print("  --api-page PAGE     - API 单播统计页码，默认 1")
        print("  --start DATE        - 开始时间，格式 yyyy-MM-dd，默认当前时间往前推 15 天")
        print("  --end DATE          - 结束时间，格式 yyyy-MM-dd，默认当天")
        print("  --desc DESC         - 任务描述筛选")
        print("  --display-type TYPE - 展示类型，默认 0")
        print("  --production BOOL   - 是否生产模式，默认 true")
        print("")
        print("示例:")
        print("  # 查询默认时间范围（近 15 天）的消息列表")
        print("  python scripts/query_msg_list.py EXAMPLE_APPKEY_006")
        print("")
        print("  # 查询指定时间范围的消息列表")
        print("  python scripts/query_msg_list.py EXAMPLE_APPKEY_006 --start 2026-03-20 --end 2026-04-03")
        print("")
        print("  # 查询任务列表第 2 页")
        print("  python scripts/query_msg_list.py EXAMPLE_APPKEY_006 --page 2")
        print("")
        print("  # 查询 API 单播统计第 2 页")
        print("  python scripts/query_msg_list.py EXAMPLE_APPKEY_006 --api-page 2")
        sys.exit(1)
    
    appkey = sys.argv[1]
    
    # 解析可选参数
    page = 1
    api_page = 1
    start_time = ""
    end_time = ""
    description = ""
    display_type = 0
    production_mode = True
    
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--page' and i + 1 < len(sys.argv):
            try:
                page = int(sys.argv[i + 1])
                if page < 1:
                    print("ERROR: 页码必须 >= 1", file=sys.stderr)
                    sys.exit(1)
            except ValueError:
                print(f"ERROR: 无效的任务列表页码：{sys.argv[i + 1]}", file=sys.stderr)
                sys.exit(1)
            i += 2
        elif sys.argv[i] == '--api-page' and i + 1 < len(sys.argv):
            try:
                api_page = int(sys.argv[i + 1])
                if api_page < 1:
                    print("ERROR: API 单播统计页码必须 >= 1", file=sys.stderr)
                    sys.exit(1)
            except ValueError:
                print(f"ERROR: 无效的 API 单播统计页码：{sys.argv[i + 1]}", file=sys.stderr)
                sys.exit(1)
            i += 2
        elif sys.argv[i] == '--start' and i + 1 < len(sys.argv):
            start_time = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--end' and i + 1 < len(sys.argv):
            end_time = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--desc' and i + 1 < len(sys.argv):
            description = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == '--display-type' and i + 1 < len(sys.argv):
            try:
                display_type = int(sys.argv[i + 1])
            except ValueError:
                print(f"ERROR: 无效的展示类型：{sys.argv[i + 1]}", file=sys.stderr)
                sys.exit(1)
            i += 2
        elif sys.argv[i] == '--production' and i + 1 < len(sys.argv):
            production_mode = sys.argv[i + 1].lower() in ('true', '1', 'yes')
            i += 2
        else:
            print(f"ERROR: 未知参数：{sys.argv[i]}", file=sys.stderr)
            sys.exit(1)
    
    # 计算实际使用的时间范围（用于显示）
    if not end_time:
        end_time = datetime.now().strftime("%Y-%m-%d")
    if not start_time:
        start_time = (datetime.now() - timedelta(days=15)).strftime("%Y-%m-%d")
    
    # 1. 查询任务粒度的消息列表
    print("\n" + "=" * 160)
    print(f"📨 友盟推送 - 消息列表（任务粒度）")
    print("=" * 160)
    print(f"应用 Key   : {appkey}")
    print(f"时间范围   : {start_time} ~ {end_time}")
    print("=" * 160)
    
    msg_result = query_msg_list(
        appkey=appkey,
        page=page,
        page_size=15,
        start_time=start_time,
        end_time=end_time,
        production_mode=production_mode,
        display_type=display_type,
        description=description
    )
    
    display_msg_list(msg_result, appkey, start_time, end_time, page, 15)
    
    # 2. 查询 API 单播统计记录
    api_result = query_api_statistics(
        appkey=appkey,
        page=api_page,
        page_size=15
    )
    
    display_api_statistics(api_result, appkey, api_page, 15)

if __name__ == "__main__":
    main()
