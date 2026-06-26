#!/usr/bin/env python3
"""
友盟推送助手 - 查询单日 API 单播统计详情
调用多个接口获取指定日期的 API 单播统计数据
包括：发送漏斗、通道统计、失败原因、厂商集成情况
"""

import json
import os
import sys
import urllib.request
import urllib.error
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

def query_push_funnel(appkey, start_time):
    """查询消息发送漏斗"""
    url = "https://upush.umeng.com/hsf/dataStatistic/getUnicastPushMsgStat"
    data = {
        "appkey": appkey,
        "startTime": start_time
    }
    return make_request(url, data)

def query_channel_stats(appkey, start_time):
    """查询通道统计"""
    url = "https://upush.umeng.com/hsf/dataStatistic/getUnicastQuotaPushMsgStat"
    data = {
        "appkey": appkey,
        "startTime": start_time
    }
    return make_request(url, data)

def query_failure_reasons(appkey, ds):
    """查询失败原因"""
    url = "https://upush.umeng.com/hsf/push/getPushExpStatData"
    data = {
        "appkey": appkey,
        "isTask": False,
        "ds": ds,
        "isFree": False,
        "stage": "all",
        "channel": "all"
    }
    return make_request(url, data)

def query_channel_integration(appkey):
    """查询厂商通道集成情况"""
    url = "https://upush.umeng.com/hsf/setting/getChannelInfo"
    data = {
        "appkey": appkey
    }
    return make_request(url, data)

def display_push_funnel(result, date):
    """展示消息发送漏斗"""
    print("\n" + "=" * 80)
    print(f"📊 消息发送漏斗 ({date})")
    print("=" * 80)
    
    if not result.get('status'):
        print(f"❌ 查询失败：{result.get('msg', '未知错误')}")
        return None
    
    data = result.get('data', {})
    
    # 数据在 data.list 中
    funnel_list = data.get('list', [])
    
    if funnel_list:
        print(f"\n{'阶段':<20} {'数量':>15}")
        print("-" * 50)
        
        for item in funnel_list:
            name = item.get('name', 'N/A')
            value = item.get('value', 0) or 0
            
            # 格式化数字
            if isinstance(value, str):
                try:
                    value = int(value.replace(',', ''))
                except:
                    pass
            
            if isinstance(value, int):
                print(f"{name:<20} {value:>15,}")
            else:
                print(f"{name:<20} {str(value):>15}")
        
        print("-" * 50)
    else:
        print("\n⚠️  暂无漏斗数据")
    
    return data

def display_channel_stats(result, date):
    """展示通道统计"""
    print("\n" + "=" * 140)
    print(f"📡 通道统计 ({date})")
    print("=" * 140)
    
    if not result.get('status'):
        print(f"❌ 查询失败：{result.get('msg', '未知错误')}")
        return None
    
    data = result.get('data', {})
    stat_list = data.get('list', [])
    
    if not stat_list:
        print("\n⚠️  暂无通道统计数据")
        return data
    
    print(f"\n{'通道名称':<15} {'实际发送':>12} {'消息送达':>10} {'送达率':>8} {'消息展示':>10} {'展示率':>8} {'消息点击':>10} {'点击率':>8} {'展示点击率':>10} {'主要失败原因':<30}")
    print("-" * 140)
    
    for stat in stat_list:
        channel_name = stat.get('channelName', 'N/A')
        
        # 数字字段
        def parse_num(val):
            if val is None:
                return 0
            if isinstance(val, str):
                return int(val.replace(',', ''))
            return val
        
        sent_count = parse_num(stat.get('sentCount', 0))
        arrive_count = parse_num(stat.get('arriveCount', 0))
        arrive_rate = stat.get('arriveRate', '')
        show_count = parse_num(stat.get('showCount', 0))
        show_rate = stat.get('showRate', '')
        click_count = parse_num(stat.get('clickCount', 0))
        click_rate = stat.get('clickRate', '')
        click_rate_on_show = stat.get('clickRateOnShow', '')
        msg = stat.get('msg', '') or ''
        
        # 截断失败原因
        if len(msg) > 28:
            msg = msg[:28] + '...'
        
        print(f"{channel_name:<15} {sent_count:>12,} {arrive_count:>10,} {str(arrive_rate):>8} {show_count:>10,} {str(show_rate):>8} {click_count:>10,} {str(click_rate):>8} {str(click_rate_on_show):>10} {msg:<30}")
    
    print("-" * 140)
    
    return data

def display_failure_reasons(result, date, channel_stats_data=None):
    """展示失败原因"""
    print("\n" + "=" * 100)
    print(f"❌ 失败原因分析 ({date})")
    print("=" * 100)
    
    if not result.get('status'):
        print(f"❌ 查询失败：{result.get('msg', '未知错误')}")
        return None
    
    data = result.get('data', {})
    error_total = data.get('errorTotal', 0)
    error_list = data.get('errorData', [])
    
    print(f"\n总失败数：{error_total:,}")
    print("=" * 100)
    
    if not error_list:
        print("\n⚠️  暂无失败原因数据")
        return data
    
    # 展示主要失败原因（一级分类）
    print(f"\n【主要失败原因分类】")
    print(f"\n{'分类':<35} {'数量':>12} {'占失败比':>10}")
    print("-" * 65)
    
    # 收集详细数据用于后续建议
    failure_details = {}
    
    for item in error_list:
        name = item.get('name', 'N/A')
        num = item.get('num', 0) or 0
        rate = item.get('rate', 0) or 0
        percentage = rate * 100 if rate <= 1 else rate
        
        print(f"{name:<35} {num:>12,} {percentage:>9.2f}%")
        
        # 收集一级分类数据
        failure_details[name] = {'total': num, 'children': []}
        
        # 展示子原因（如果有）
        children = item.get('children', [])
        if children:
            for child in children:
                child_name = child.get('name', 'N/A')
                child_num = child.get('num', 0) or 0
                child_rate = child.get('rate', 0) or 0
                child_percentage = child_rate * 100 if child_rate <= 1 else child_rate
                
                # 截断原因
                if len(child_name) > 33:
                    child_name = child_name[:33] + '...'
                
                print(f"  └─ {child_name:<33} {child_num:>12,} {child_percentage:>9.2f}%")
                failure_details[name]['children'].append({
                    'name': child.get('name', 'N/A'),
                    'num': child_num
                })
    
    print("-" * 65)
    
    # 结合通道统计数据进行更详细的分析
    if channel_stats_data:
        print(f"\n【各通道失败详情】")
        print(f"\n{'通道':<12} {'发送量':>10} {'未送达':>10} {'未送达率':>10} {'主要失败原因':<40}")
        print("-" * 90)
        
        stat_list = channel_stats_data.get('list', [])
        
        def parse_num(val):
            if val is None:
                return 0
            if isinstance(val, str):
                try:
                    return int(val.replace(',', ''))
                except:
                    return 0
            return val
        
        for stat in stat_list:
            channel_name = stat.get('channelName', 'N/A')
            sent_count = parse_num(stat.get('sentCount', 0))
            arrive_count = parse_num(stat.get('arriveCount', 0))
            failed_count = sent_count - arrive_count
            fail_rate = (failed_count / sent_count * 100) if sent_count > 0 else 0
            main_fail_msg = stat.get('msg', '') or '无'
            
            # 截断失败原因
            if len(main_fail_msg) > 38:
                main_fail_msg = main_fail_msg[:38] + '...'
            
            print(f"{channel_name:<12} {sent_count:>10,} {failed_count:>10,} {fail_rate:>9.2f}% {main_fail_msg:<40}")
        
        print("-" * 90)
    
    return data


def generate_optimization_suggestions(funnel_data, channel_data, failure_data, integration_data):
    """基于多维度数据生成优化建议
    
    注意：仅基于实际返回数据给出有依据的建议，不编造没有信息来源的内容。
    """
    print("\n" + "=" * 100)
    print("💡 推送优化建议")
    print("=" * 100)
    
    suggestions = []
    
    # 1. 基于漏斗数据的建议 - 仅做数据陈述，不编造优化手段
    if funnel_data:
        funnel_list = funnel_data.get('list', [])
        sent = arrive = show = click = 0
        
        for item in funnel_list:
            name = item.get('name', '')
            value = item.get('value', 0) or 0
            if isinstance(value, str):
                try:
                    value = int(value.replace(',', ''))
                except:
                    value = 0
            
            if '发送' in name:
                sent = value
            elif '送达' in name:
                arrive = value
            elif '展示' in name:
                show = value
            elif '点击' in name:
                click = value
        
        # 送达率分析 - 仅陈述数据事实
        if sent > 0:
            arrive_rate = arrive / sent * 100
            lost_count = sent - arrive
            suggestions.append({
                'priority': '📊 数据概览',
                'title': '送达环节',
                'detail': f'实际发送 {sent:,} 条，送达 {arrive:,} 条，送达率 {arrive_rate:.2f}%，未送达 {lost_count:,} 条。具体失败原因见下方失败原因分析。'
            })
        
        # 展示率分析
        if arrive > 0:
            show_rate = show / arrive * 100
            lost_show = arrive - show
            suggestions.append({
                'priority': '📊 数据概览',
                'title': '展示环节',
                'detail': f'送达 {arrive:,} 条，展示 {show:,} 条，展示率 {show_rate:.2f}%，送达未展示 {lost_show:,} 条。可能原因包括通知权限关闭、厂商频控等。'
            })
        
        # 点击率分析
        if show > 0:
            click_rate = click / show * 100
            suggestions.append({
                'priority': '📊 数据概览',
                'title': '点击环节',
                'detail': f'展示 {show:,} 条，点击 {click:,} 条，点击率 {click_rate:.2f}%。'
            })
    
    # 2. 基于通道统计的建议 - 仅指出数据异常的通道
    if channel_data:
        stat_list = channel_data.get('list', [])
        
        for stat in stat_list:
            channel_name = stat.get('channelName', '')
            arrive_rate = stat.get('arriveRate', '')
            sent_count = stat.get('sentCount', 0) or 0
            msg = stat.get('msg', '') or ''
            
            # 魅族送达率为 0 的特殊情况 - 这是通道统计接口明确提示的
            if channel_name == '魅族' and arrive_rate == '0.00%':
                sent_val = sent_count
                if isinstance(sent_val, str):
                    try:
                        sent_val = int(sent_val.replace(',', ''))
                    except:
                        sent_val = 0
                
                suggestions.append({
                    'priority': '🔴 需处理',
                    'title': '魅族通道送达率为 0%',
                    'detail': f'魅族通道当天发送 {sent_val:,} 条消息，送达率为 0%。通道统计接口返回的主要失败原因为："{msg}"。'
                })
    
    # 3. 基于失败原因的建议 - 仅陈述失败原因数据，不编造解决方案
    if failure_data:
        error_list = failure_data.get('errorData', [])
        error_total = failure_data.get('errorTotal', 0)
        
        for item in error_list:
            name = item.get('name', '')
            num = item.get('num', 0) or 0
            
            if num <= 0:
                continue
            
            percentage = num / error_total * 100 if error_total > 0 else 0
            children = item.get('children', [])
            
            # 构建子原因描述
            children_desc = ''
            if children:
                # 按数量排序，取前3个
                top_children = sorted(children, key=lambda x: x.get('num', 0), reverse=True)[:3]
                children_parts = []
                for child in top_children:
                    child_name = child.get('name', '')
                    child_num = child.get('num', 0) or 0
                    children_parts.append(f'{child_name}（{child_num:,} 次）')
                children_desc = '，主要包括：' + '、'.join(children_parts)
            
            suggestions.append({
                'priority': '📊 失败原因',
                'title': f'{name}（{percentage:.1f}%）',
                'detail': f'共 {num:,} 次失败{children_desc}。'
            })
    
    # 4. 基于厂商集成情况的建议 - 仅陈述配置状态
    if integration_data:
        data = integration_data.get('data', {})
        
        # 魅族回执确认检查 - 这是接口明确返回的字段
        meizu_id = data.get('meizuId', '') or ''
        meizu_secret = data.get('meizuSecret', '') or ''
        meizu_confirmed = data.get('meizuCallbackUrlConfirmed')
        
        if meizu_id and meizu_secret and meizu_confirmed is False:
            suggestions.append({
                'priority': '⚠️  配置提示',
                'title': '魅族通道回执未确认',
                'detail': '魅族通道已填写 AppID 和 AppSecret，但 meizuCallbackUrlConfirmed 为 false。这会导致消息实际送达但无法统计到数据。'
            })
    
    # 输出建议
    if not suggestions:
        print("\n✅ 当前推送数据表现良好，暂无特别优化建议")
        return
    
    # 按优先级排序
    priority_order = {'🔴 需处理': 0, '⚠️  配置提示': 1, '📊 失败原因': 2, '📊 数据概览': 3}
    suggestions.sort(key=lambda x: priority_order.get(x['priority'], 99))
    
    for i, s in enumerate(suggestions, 1):
        print(f"\n【{i}】{s['priority']}")
        print(f"  📌 {s['title']}")
        print(f"  📋 {s['detail']}")
        print()

def display_channel_integration(result, appkey):
    """展示厂商通道集成情况"""
    print("\n" + "=" * 100)
    print(f"🔧 厂商通道集成情况")
    print("=" * 100)
    
    if not result.get('status'):
        print(f"❌ 查询失败：{result.get('msg', '未知错误')}")
        return None
    
    data = result.get('data', {})
    
    # 各厂商集成字段定义
    vendors = [
        {
            'key': 'huawei',
            'name': '华为',
            'fields': ['huaweiId', 'huaweiSecret'],
            'field_labels': {'huaweiId': 'AppID', 'huaweiSecret': 'AppSecret'}
        },
        {
            'key': 'xiaomi',
            'name': '小米',
            'fields': ['miSecret'],
            'field_labels': {'miSecret': 'AppSecret'}
        },
        {
            'key': 'oppo',
            'name': 'OPPO',
            'fields': ['oppoAppId', 'oppoSecret'],
            'field_labels': {'oppoAppId': 'AppID', 'oppoSecret': 'AppSecret'}
        },
        {
            'key': 'vivo',
            'name': 'VIVO',
            'fields': ['vivoAppId', 'vivoCallbackId'],
            'field_labels': {'vivoAppId': 'AppID', 'vivoCallbackId': 'CallbackID'}
        },
        {
            'key': 'meizu',
            'name': '魅族',
            'fields': ['meizuId', 'meizuSecret'],
            'field_labels': {'meizuId': 'AppID', 'meizuSecret': 'AppSecret'},
            'callback_confirmed_field': 'meizuCallbackUrlConfirmed'
        },
        {
            'key': 'honor',
            'name': '荣耀',
            'fields': ['honorAppId', 'honorClientId', 'honorClientSecret'],
            'field_labels': {'honorAppId': 'AppID', 'honorClientId': 'ClientID', 'honorClientSecret': 'ClientSecret'}
        },
    ]
    
    print(f"\n{'厂商':<10} {'AppID/ClientID':<35} {'AppSecret':<35} {'CallbackID':<20} {'状态':<15}")
    print("-" * 120)
    
    has_vivo_warning = False
    has_meizu_warning = False
    meizu_callback_confirmed = None
    
    for vendor in vendors:
        fields = vendor['fields']
        
        # 获取各字段值
        field_values = {}
        for field in fields:
            val = data.get(field, '') or ''
            field_values[field] = val
        
        # 判断是否全部字段都有值
        all_filled = all(field_values.get(f) for f in fields)
        any_filled = any(field_values.get(f) for f in fields)
        
        # 判断状态
        if all_filled:
            status = "✅ 已集成"
        elif any_filled:
            status = "⚠️  部分集成"
        else:
            status = "❌ 未集成"
        
        # vivo 特殊提示
        if vendor['key'] == 'vivo' and field_values.get('vivoAppId') and not field_values.get('vivoCallbackId'):
            has_vivo_warning = True
        
        # 魅族回执确认状态
        if vendor['key'] == 'meizu' and 'callback_confirmed_field' in vendor:
            callback_field = vendor['callback_confirmed_field']
            meizu_callback_confirmed = data.get(callback_field)
            # 如果填了 meizuId 和 meizuSecret，但 meizuCallbackUrlConfirmed 是 false
            if field_values.get('meizuId') and field_values.get('meizuSecret') and meizu_callback_confirmed is False:
                has_meizu_warning = True
        
        # 格式化显示
        app_id_val = field_values.get(fields[0], '-') or '-'
        secret_val = field_values.get(fields[-1] if len(fields) > 1 else fields[0], '-') or '-'
        callback_val = '-'
        
        # 对于有3个字段的厂商（荣耀），中间字段作为 ClientID
        if len(fields) == 3:
            app_id_val = field_values.get(fields[0], '-') or '-'
            secret_val = field_values.get(fields[2], '-') or '-'
            callback_val = field_values.get(fields[1], '-') or '-'
        
        # 对于小米只有1个字段
        if len(fields) == 1:
            app_id_val = '-'
            secret_val = field_values.get(fields[0], '-') or '-'
            callback_val = '-'
        
        # 截断显示
        def truncate(val, max_len=33):
            val = str(val) if val else '-'
            if len(val) > max_len:
                return val[:max_len] + '..'
            return val
        
        print(f"{vendor['name']:<10} {truncate(app_id_val):<35} {truncate(secret_val):<35} {truncate(callback_val):<20} {status:<15}")
    
    print("-" * 120)
    
    # vivo 提示
    if has_vivo_warning:
        print("\n💡 提示：接入 vivo 新回执，可以获得更详细的回执信息")
        print("   参考文档：https://dev.vivo.com.cn/documentCenter/doc/681")
    
    # 魅族回执确认提示
    if has_meizu_warning:
        print("\n⚠️  提示：由于魅族通道未确认配置回执，会导致有送达，但是统计不到的情况，建议配置")
    
    return data

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法：python scripts/query_daily_api_stats.py <appkey> <date>")
        print("")
        print("参数说明:")
        print("  appkey  - 应用的唯一标识（必填）")
        print("  date    - 查询日期，格式 yyyy-MM-dd 或 yyyyMMdd（必填）")
        print("")
        print("示例:")
        print("  # 查询 2026-04-07 的 API 单播统计详情")
        print("  python scripts/query_daily_api_stats.py EXAMPLE_APPKEY_006 2026-04-07")
        print("")
        print("  # 查询 20260407 的 API 单播统计详情")
        print("  python scripts/query_daily_api_stats.py EXAMPLE_APPKEY_006 20260407")
        sys.exit(1)
    
    appkey = sys.argv[1]
    date_str = sys.argv[2]
    
    # 解析日期格式
    try:
        if '-' in date_str:
            # yyyy-MM-dd 格式
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            start_time = date_obj.strftime("%Y-%m-%d")
            ds = date_obj.strftime("%Y%m%d")
        else:
            # yyyyMMdd 格式
            date_obj = datetime.strptime(date_str, "%Y%m%d")
            start_time = date_obj.strftime("%Y-%m-%d")
            ds = date_obj.strftime("%Y%m%d")
    except ValueError:
        print(f"ERROR: 无效的日期格式：{date_str}")
        print("支持的格式：yyyy-MM-dd 或 yyyyMMdd")
        sys.exit(1)
    
    print("=" * 100)
    print("📡 API 单播统计详情（单日）")
    print("=" * 100)
    print(f"应用 Key   : {appkey}")
    print(f"查询日期   : {start_time}")
    print("=" * 100)
    
    # 1. 查询消息发送漏斗
    print(f"\n📊 正在查询 消息发送漏斗...")
    funnel_result = query_push_funnel(appkey, start_time)
    funnel_data = None
    if funnel_result.get('status'):
        print(f"✅ 消息发送漏斗 查询成功")
        funnel_data = display_push_funnel(funnel_result, start_time)
    else:
        print(f"❌ 消息发送漏斗 查询失败：{funnel_result.get('msg', '未知错误')}")
    
    # 2. 查询通道统计
    print(f"\n📡 正在查询 通道统计...")
    channel_result = query_channel_stats(appkey, start_time)
    channel_data = None
    if channel_result.get('status'):
        print(f"✅ 通道统计 查询成功")
        channel_data = display_channel_stats(channel_result, start_time)
    else:
        print(f"❌ 通道统计 查询失败：{channel_result.get('msg', '未知错误')}")
    
    # 3. 查询失败原因
    print(f"\n❌ 正在查询 失败原因...")
    failure_result = query_failure_reasons(appkey, ds)
    failure_data = None
    if failure_result.get('status'):
        print(f"✅ 失败原因 查询成功")
        failure_data = display_failure_reasons(failure_result, start_time, channel_data)
    else:
        print(f"❌ 失败原因 查询失败：{failure_result.get('msg', '未知错误')}")
    
    # 4. 查询厂商通道集成情况
    print(f"\n🔧 正在查询 厂商通道集成情况...")
    integration_result = query_channel_integration(appkey)
    integration_data = None
    if integration_result.get('status'):
        print(f"✅ 厂商通道集成情况 查询成功")
        integration_data = display_channel_integration(integration_result, appkey)
    else:
        print(f"❌ 厂商通道集成情况 查询失败：{integration_result.get('msg', '未知错误')}")
    
    # 5. 生成优化建议
    print(f"\n💡 正在生成 优化建议...")
    generate_optimization_suggestions(funnel_data, channel_data, failure_data, integration_data)
    
    print("\n" + "=" * 100)
    print("✅ 查询完成")
    print("=" * 100 + "\n")

if __name__ == "__main__":
    main()
