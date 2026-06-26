#!/usr/bin/env python3
"""
友盟推送助手 - 单条消息详情查询
根据 appkey 和 msg_id 查询单条推送消息的完整详情，包括：
1. 消息基本信息和参数（getMsgInfo）
2. 推送统计漏斗（getMsgData）
3. 失败原因分析（getPushExpStatData）
4. 厂商通道集成状态（getChannelInfo，仅 Android）
5. 分通道送达统计（getMsgStatChannelData，仅 Android）
"""

import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime

COOKIE_FILE = os.path.expanduser("~/.qoderwork/skills/umeng-push-helper/cookie.txt")
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "outputs")

# 厂商通道显示名称映射
CHANNEL_NAME_MAP = {
    "accs": "友盟通道",
    "huawei": "华为",
    "xiaomi": "小米",
    "oppo": "OPPO",
    "vivo": "VIVO",
    "honor": "荣耀",
    "meizu": "魅族",
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


def is_api_unicast(msg_id):
    """
    检测 msg_id 是否为 API 单播消息。
    规则：以 uu/ul/ua 开头，且倒数第二位是 0。
    """
    if len(msg_id) < 2:
        return False

    prefix = msg_id[:2].lower()
    if prefix not in ("uu", "ul", "ua"):
        return False

    if msg_id[-2] != '0':
        return False

    return True


def get_app_platform(appkey):
    """从 home/listAll 接口获取应用平台类型"""
    url = "https://upush.umeng.com/hsf/home/listAll"
    data = {
        "appkey": "",
        "platform": "all",
        "page": 1,
        "perPage": 15,
        "hasPush": 0,
        "appName": "",
        "yearQuotaSts": 0
    }

    result = make_request(url, data)
    if result.get('status'):
        app_list = result.get('data', {}).get('appList', [])
        for app in app_list:
            if app.get('appkey') == appkey:
                return app.get('platform', '').lower()
    return None


def call_get_msg_info(appkey, msg_id):
    """接口 1：获取消息基本信息"""
    url = "https://upush.umeng.com/hsf/push/getMsgInfo"
    data = {"appkey": appkey, "taskId": msg_id}
    return make_request(url, data)


def call_get_msg_data(appkey, msg_id):
    """接口 2：获取推送统计指标"""
    url = "https://upush.umeng.com/hsf/push/getMsgData"
    data = {"appkey": appkey, "taskId": msg_id}
    return make_request(url, data)


def call_get_push_exp_stat(appkey, msg_id):
    """接口 3：获取失败分析数据"""
    url = "https://upush.umeng.com/hsf/push/getPushExpStatData"
    data = {
        "appkey": appkey,
        "isTask": True,
        "msgId": msg_id,
        "isFree": False,
        "stage": "all",
        "channel": "all"
    }
    return make_request(url, data)


def call_get_channel_info(appkey):
    """接口 4：获取厂商通道集成状态（仅 Android）"""
    url = "https://upush.umeng.com/hsf/setting/getChannelInfo"
    data = {"appkey": appkey}
    return make_request(url, data)


def call_get_msg_stat_channel(appkey, msg_id):
    """接口 5：获取分通道送达统计（仅 Android）"""
    url = "https://upush.umeng.com/hsf/push/getMsgStatChannelData"
    data = {"appkey": appkey, "taskId": msg_id}
    return make_request(url, data)


def parse_num(val):
    """安全解析数字"""
    if val is None:
        return 0
    if isinstance(val, str):
        try:
            return int(val.replace(',', ''))
        except (ValueError, TypeError):
            return 0
    return val


def make_bar(value, max_value, width=50):
    """生成文本条形图"""
    if max_value == 0:
        filled = 0
    else:
        filled = int(value / max_value * width)
    filled = max(0, min(filled, width))
    empty = width - filled
    return '\u2588' * filled + '\u2591' * empty


def display_msg_info(result, appkey, msg_id):
    """展示消息基本信息"""
    print("\n" + "=" * 260)
    print(f"\U0001f4e8 友盟推送 - 单条消息详情")
    print("=" * 260)
    print(f"应用 Key   : {appkey}")
    print(f"消息 ID    : {msg_id}")
    print("=" * 260)

    data = result.get('data', {})

    print(f"\n\u3010消息基本信息\u3011")
    print("-" * 260)

    # 提取常见字段
    fields = [
        ('任务描述', data.get('description') or data.get('title') or ''),
        ('推送类型', data.get('type') or data.get('pushType') or ''),
        ('目标人群', data.get('target') or ''),
        ('生产模式', '是' if data.get('productionMode') else '否'),
        ('发送时间', data.get('pushTime') or data.get('sendTime') or ''),
        ('创建时间', data.get('createTime') or ''),
        ('状态', data.get('status') or ''),
        ('应用类型', data.get('platform') or ''),
    ]

    for label, value in fields:
        if value:
            print(f"  {label:<12} : {value}")

    # channelActivity 特别提示
    channel_activity = data.get('channelActivity')
    print(f"  {'厂商通道配置':<12} : {'已配置' if channel_activity else '未配置（仅能在线通道下发）'}")

    # 显示完整的 channelActivity 内容（如果有）
    if channel_activity:
        if isinstance(channel_activity, dict):
            print(f"  {'通道详情':<12} :")
            for k, v in channel_activity.items():
                ch_name = CHANNEL_NAME_MAP.get(k, k)
                print(f"               {ch_name}: {v}")
        else:
            print(f"  {'通道详情':<12} : {channel_activity}")

    print("-" * 260)


def display_msg_data(result):
    """展示推送统计漏斗"""
    data = result.get('data', {})
    if not data:
        print(f"\n\u26a0\ufe0f  暂无统计数据")
        return

    # 尝试从多种可能的字段名中获取数据
    # 有些接口返回列表，有些返回对象
    if isinstance(data, list) and len(data) > 0:
        data = data[0]

    total_count = parse_num(data.get('totalCount') or data.get('pushCnt') or 0)
    sent_count = parse_num(data.get('sentCount') or data.get('pushCnt') or total_count)
    arrive_count = parse_num(data.get('arriveCount') or data.get('arriveCnt') or 0)
    show_count = parse_num(data.get('showCount') or data.get('showCnt') or 0)
    click_count = parse_num(data.get('clickCount') or data.get('clickCnt') or 0)
    ignore_count = parse_num(data.get('ignoreCount') or data.get('ignoreCnt') or 0)

    # 计算各阶段比率
    arrive_rate = f"{arrive_count / sent_count * 100:.2f}%" if sent_count > 0 else "N/A"
    show_rate = f"{show_count / arrive_count * 100:.2f}%" if arrive_count > 0 else "N/A"
    click_rate = f"{click_count / arrive_count * 100:.2f}%" if arrive_count > 0 else "N/A"
    click_rate_show = f"{click_count / show_count * 100:.2f}%" if show_count > 0 else "N/A"
    ignore_rate = f"{ignore_count / arrive_count * 100:.2f}%" if arrive_count > 0 else "N/A"

    max_val = max(total_count, sent_count, arrive_count, show_count, click_count, ignore_count, 1)

    print(f"\n\u3010推送统计漏斗\u3011")
    print("-" * 260)
    print(f"{'阶段':<12} {'数量':>15} {'比率':>12} {'可视化'}")
    print("-" * 260)

    rows = [
        ('计划发送', total_count, '100.00%'),
        ('实际发送', sent_count, f"{sent_count / total_count * 100:.2f}%" if total_count > 0 else "N/A"),
        ('消息送达', arrive_count, arrive_rate),
        ('消息展示', show_count, show_rate),
        ('消息点击', click_count, click_rate),
        ('消息忽略', ignore_count, ignore_rate),
    ]

    for label, value, rate in rows:
        bar = make_bar(value, max_val)
        print(f"{label:<12} {value:>15,} {rate:>12} {bar}")

    print("-" * 260)

    # 额外展示送达点击率和展示点击率
    print(f"\n  送达点击率（点击/送达）: {click_rate}")
    print(f"  展示点击率（点击/展示）: {click_rate_show}")
    print("-" * 260)


def display_exp_stat(result):
    """展示失败原因分析"""
    data = result.get('data', {})
    if not data:
        print(f"\n\u26a0\ufe0f  暂无失败分析数据")
        return

    print(f"\n\u3010失败原因分析\u3011")
    print("-" * 260)

    # 尝试解析不同格式的数据
    # 格式 1：列表
    if isinstance(data, list):
        items = data
    # 格式 2：对象中包含 list 或 dataList
    elif isinstance(data, dict):
        items = data.get('list') or data.get('dataList') or data.get('items') or []
        if not items and isinstance(items, list) is False:
            # 可能是直接的对象数据，按 key-value 展示
            print(f"\n  数据内容:")
            for k, v in data.items():
                print(f"    {k}: {v}")
            print("-" * 260)
            return
    else:
        print(f"\n  数据格式未知: {json.dumps(data, ensure_ascii=False, indent=2)}")
        print("-" * 260)
        return

    if not items:
        print(f"\n  暂无失败记录")
        print("-" * 260)
        return

    # 表头
    header = f"{'序号':>4} | {'阶段':<15} | {'通道':<15} | {'原因':<30} | {'数量':>10} | {'占比':>8}"
    print(header)
    print("-" * 260)

    total = sum(parse_num(item.get('count') or item.get('num') or item.get('cnt') or 0) for item in items)

    for i, item in enumerate(items, 1):
        stage = item.get('stage') or item.get('phase') or ''
        channel = item.get('channel') or ''
        reason = item.get('reason') or item.get('cause') or item.get('errorMsg') or ''
        count = parse_num(item.get('count') or item.get('num') or item.get('cnt') or 0)
        ratio = f"{count / total * 100:.2f}%" if total > 0 else "N/A"

        ch_name = CHANNEL_NAME_MAP.get(channel, channel)
        print(f"{i:>4} | {stage:<15} | {ch_name:<15} | {reason:<30} | {count:>10,} | {ratio:>8}")

    print("-" * 260)


def display_channel_info(result, appkey, channel_activity=None):
    """展示厂商通道集成状态"""
    data = result.get('data', {})
    if not data:
        print(f"\n\u26a0\ufe0f  暂无通道集成信息")
        return

    print(f"\n\u3010厂商通道集成状态\u3011")
    print("-" * 260)

    # getChannelInfo 返回的是扁平 key-value 对象，需要提取各厂商通道信息
    # 定义厂商通道的关键字段映射
    vendor_configs = [
        ('huawei', '华为', ['huaweiId', 'huaweiSecret', 'huaweiCallbackId']),
        ('xiaomi', '小米', ['miId', 'miSecret']),
        ('oppo', 'OPPO', ['oppoAppId', 'oppoSecret']),
        ('vivo', 'VIVO', ['vivoAppId', 'vivoAppkey', 'vivoSecret', 'vivoCallbackId']),
        ('honor', '荣耀', ['honorAppId', 'honorClientId', 'honorClientSecret']),
        ('meizu', '魅族', ['meizuId', 'meizuSecret', 'meizuCallbackUrlConfirmed']),
        ('fcm', 'FCM', ['fcmSecret']),
    ]

    header = f"{'序号':>4} | {'通道名称':<12} | {'集成状态':<12} | {'配置状态':<12} | {'说明'}"
    print(header)
    print("-" * 260)

    warnings = []
    not_configured = []

    for i, (vendor_key, vendor_name, fields) in enumerate(vendor_configs, 1):
        # 检查是否至少有一个字段有值
        has_config = any(data.get(f, '') for f in fields)
        # 检查关键字段是否有有效值（非空字符串）
        key_fields_have_value = any(data.get(f) and data.get(f) not in ('', False, 'false') for f in fields[:2])

        integrated_str = '已集成' if has_config else '未集成'
        config_str = '已配置' if key_fields_have_value else '未配置'

        # 生成说明
        desc_parts = []
        for f in fields[:2]:
            val = data.get(f, '')
            if val and val not in ('', False, 'false'):
                display_val = str(val)[:20] + '...' if len(str(val)) > 20 else str(val)
                desc_parts.append(f"{f}={display_val}")
            else:
                desc_parts.append(f"{f}=空")
        desc = '; '.join(desc_parts)

        print(f"{i:>4} | {vendor_name:<12} | {integrated_str:<12} | {config_str:<12} | {desc}")

        if not has_config:
            warnings.append(vendor_name)
        elif not key_fields_have_value:
            not_configured.append(vendor_name)

    print("-" * 260)

    # 检查 channelActivity
    ch_activity = data.get('channelActivity', '') or channel_activity
    if ch_activity:
        if isinstance(ch_activity, dict) and len(ch_activity) > 0:
            active_channels = list(ch_activity.keys())
            active_names = [CHANNEL_NAME_MAP.get(c, c) for c in active_channels]
            print(f"\n  已激活的厂商通道 (channelActivity): {', '.join(active_names)}")
        else:
            print(f"\n  厂商通道配置 (channelActivity): {ch_activity}")
    else:
        print(f"\n  \u26a0\ufe0f  channelActivity 未配置")

    if warnings:
        print(f"\n  \u26a0\ufe0f  以下厂商通道未集成（无配置信息），将无法通过对应通道下发推送：")
        for w in warnings:
            print(f"     - {w}")

    if not_configured:
        print(f"\n  \u26a0\ufe0f  以下厂商通道已集成但关键字段未配置：")
        for w in not_configured:
            print(f"     - {w}")

    if not ch_activity:
        print(f"\n  \u274c  channelActivity 未配置，厂商通道无法使用，只能依赖应用活跃时通过在线通道下发。")
        print(f"     建议：在友盟后台 → 应用配置 → 推送渠道 → 配置 channelActivity 字段")

    print("-" * 260)


def display_channel_stats(result):
    """展示分通道送达统计（含失败原因解析）"""
    data = result.get('data', {})
    if not data:
        print(f"\n\u26a0\ufe0f  暂无分通道统计数据")
        return

    print(f"\n\u3010分通道送达统计\u3011")
    print("-" * 260)

    # 解析数据
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        items = data.get('list') or data.get('dataList') or data.get('items') or []
        # 如果是 dict of dicts
        if not items and data:
            for k, v in data.items():
                if isinstance(v, dict):
                    v['channel'] = k
                    items.append(v)

    if not items:
        print(f"\n  暂无分通道统计记录")
        print("-" * 260)
        return

    header = (
        f"{'序号':>4} | "
        f"{'通道':<12} | "
        f"{'发送':>10} | "
        f"{'送达':>10} | "
        f"{'送达率':>8} | "
        f"{'展示':>10} | "
        f"{'展示率':>8} | "
        f"{'点击':>8} | "
        f"{'送达点击率':>10}"
    )
    print(header)
    print("-" * 260)

    # 收集各通道的失败原因，用于汇总分析
    error_summary = []

    for i, item in enumerate(items, 1):
        channel = item.get('channel') or item.get('channelName') or ''
        ch_name = CHANNEL_NAME_MAP.get(channel, channel)

        sent = parse_num(item.get('sentCount') or item.get('sendCount') or item.get('sent') or 0)
        arrive = parse_num(item.get('arriveCount') or item.get('arrive') or 0)
        show = parse_num(item.get('showCount') or item.get('show') or 0)
        click = parse_num(item.get('clickCount') or item.get('click') or 0)

        arrive_rate = item.get('arriveRate') or (f"{arrive / sent * 100:.2f}%" if sent > 0 else "N/A")
        show_rate = item.get('showRate') or (f"{show / arrive * 100:.2f}%" if arrive > 0 else "N/A")
        click_rate = item.get('clickRate') or (f"{click / arrive * 100:.2f}%" if arrive > 0 else "N/A")

        print(
            f"{i:>4} | "
            f"{ch_name:<12} | "
            f"{sent:>10,} | "
            f"{arrive:>10,} | "
            f"{str(arrive_rate):>8} | "
            f"{show:>10,} | "
            f"{str(show_rate):>8} | "
            f"{click:>8,} | "
            f"{str(click_rate):>10}"
        )

        # 解析 error 字段
        error_raw = item.get('error', '')
        if error_raw:
            error_text, error_count = parse_error_field(error_raw)
            failed_count = sent - arrive if sent > 0 else 0
            error_summary.append({
                'channel': ch_name,
                'error_text': error_text,
                'error_count': error_count,
                'failed_count': failed_count,
                'sent': sent,
                'arrive': arrive,
            })

    print("-" * 260)

    # 展示各通道失败原因汇总
    if error_summary:
        print(f"\n\u3010各通道失败原因分析\u3011")
        print("-" * 260)
        for err in error_summary:
            if err['sent'] == 0:
                # 发送数为 0，说明完全未下发
                print(f"  {err['channel']}：发送数 0，未下发")
                print(f"    失败原因：{err['error_text']}（影响 {err['error_count']:,} 个）")
            elif err['arrive'] == 0:
                # 发送了但全部失败
                print(f"  {err['channel']}：发送 {err['sent']:,}，送达 0，全部失败")
                print(f"    失败原因：{err['error_text']}（影响 {err['error_count']:,} 个）")
            else:
                # 部分成功
                failed = err['sent'] - err['arrive']
                print(f"  {err['channel']}：发送 {err['sent']:,}，送达 {err['arrive']:,}，失败 {failed:,}")
                print(f"    失败原因：{err['error_text']}（影响 {err['error_count']:,} 个）")
        print("-" * 260)


def parse_error_field(error_raw):
    """
    解析 error 字段，提取失败原因和影响数量
    格式如："华为资讯营销类消息频次限制84455个"
    返回：(原因文本, 数量)
    """
    import re
    # 匹配末尾的数字 + "个"
    match = re.search(r'(\d+)个$', error_raw)
    if match:
        count = int(match.group(1))
        # 去掉末尾的数量部分，得到原因文本
        text = re.sub(r'\d+个$', '', error_raw).strip()
        return text, count
    return error_raw, 0


def generate_html_report(all_data, appkey, msg_id, is_android):
    """生成 HTML 可视化报告"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"msg_detail_{msg_id}_{timestamp}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # 准备数据
    msg_info = all_data.get('msgInfo', {})
    msg_data = all_data.get('msgData', {})
    exp_stat = all_data.get('expStat', {})
    channel_info = all_data.get('channelInfo', {})
    channel_stats = all_data.get('channelStats', {})

    # 处理 msg_data 可能是列表
    if isinstance(msg_data, list) and len(msg_data) > 0:
        msg_data = msg_data[0]

    data_json = json.dumps({
        'msgInfo': msg_info,
        'msgData': msg_data,
        'expStat': exp_stat,
        'channelInfo': channel_info,
        'channelStats': channel_stats,
        'isAndroid': is_android,
        'appkey': appkey,
        'msgId': msg_id,
    }, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>单条消息详情 - {msg_id}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 40px 20px;
}}
.container {{ max-width: 1200px; margin: 0 auto; }}
.header {{
    background: rgba(255,255,255,0.95);
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}}
.header h1 {{ color: #333; font-size: 24px; margin-bottom: 8px; }}
.header .meta {{ color: #666; font-size: 14px; }}
.header .meta span {{ margin-right: 24px; }}
.card {{
    background: rgba(255,255,255,0.95);
    border-radius: 16px;
    padding: 24px 32px;
    margin-bottom: 24px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}}
.card h2 {{ color: #333; font-size: 18px; margin-bottom: 16px; padding-bottom: 12px; border-bottom: 2px solid #667eea; }}
.info-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; }}
.info-item {{ background: #f8f9ff; padding: 16px; border-radius: 8px; }}
.info-item .label {{ color: #888; font-size: 12px; margin-bottom: 4px; }}
.info-item .value {{ color: #333; font-size: 16px; font-weight: 500; word-break: break-all; }}
.stat-row {{ display: flex; align-items: center; margin-bottom: 12px; }}
.stat-row .label {{ width: 80px; color: #666; font-size: 14px; }}
.stat-row .value {{ width: 120px; text-align: right; color: #333; font-size: 14px; font-weight: 500; }}
.stat-row .bar-container {{ flex: 1; margin: 0 12px; height: 24px; background: #eee; border-radius: 4px; overflow: hidden; }}
.stat-row .bar {{ height: 100%; background: linear-gradient(90deg, #667eea, #764ba2); border-radius: 4px; transition: width 0.5s; }}
.stat-row .rate {{ width: 80px; text-align: right; color: #667eea; font-size: 14px; font-weight: 500; }}
table {{ width: 100%; border-collapse: collapse; }}
th {{ background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; padding: 12px; text-align: left; font-size: 14px; }}
td {{ padding: 10px 12px; border-bottom: 1px solid #eee; font-size: 14px; }}
tr:hover {{ background: #f8f9ff; }}
.chart-container {{ position: relative; height: 300px; margin: 16px 0; }}
.channel-status {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 12px; }}
.ch-card {{ padding: 16px; border-radius: 8px; text-align: center; }}
.ch-card.integrated {{ background: #e8f5e9; }}
.ch-card.not-integrated {{ background: #ffebee; }}
.ch-card .name {{ font-size: 16px; font-weight: 500; margin-bottom: 8px; }}
.ch-card .status {{ font-size: 12px; color: #666; }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>\U0001f4e8 单条消息详情</h1>
        <div class="meta">
            <span>应用 Key: <strong id="appkey"></strong></span>
            <span>消息 ID: <strong id="msgId"></strong></span>
        </div>
    </div>

    <div class="card">
        <h2>\U0001f4cb 消息基本信息</h2>
        <div class="info-grid" id="infoGrid"></div>
    </div>

    <div class="card">
        <h2>\U0001f4ca 推送统计漏斗</h2>
        <div id="funnelStats"></div>
        <div class="chart-container"><canvas id="funnelChart"></canvas></div>
    </div>

    <div class="card">
        <h2>\U0001f50d 失败原因分析</h2>
        <div id="expStatContent"></div>
        <div class="chart-container"><canvas id="expChart"></canvas></div>
    </div>

    <div class="card" id="channelInfoCard" style="display:none;">
        <h2>\U0001f527 厂商通道集成状态</h2>
        <div class="channel-status" id="channelStatus"></div>
    </div>

    <div class="card" id="channelStatsCard" style="display:none;">
        <h2>\U0001f4e1 分通道送达统计</h2>
        <div id="channelStatsTable"></div>
        <div class="chart-container"><canvas id="channelChart"></canvas></div>
    </div>
</div>

<script>
const channelNameMap = {{
    "accs": "友盟通道", "huawei": "华为", "xiaomi": "小米",
    "oppo": "OPPO", "vivo": "VIVO", "honor": "荣耀", "meizu": "魅族"
}};

const data = {data_json};

function getChName(ch) {{ return channelNameMap[ch] || ch; }}

document.getElementById('appkey').textContent = data.appkey;
document.getElementById('msgId').textContent = data.msgId;

// 消息基本信息
const infoGrid = document.getElementById('infoGrid');
const infoFields = [
    ['任务描述', data.msgInfo.description || data.msgInfo.title || ''],
    ['推送类型', data.msgInfo.type || data.msgInfo.pushType || ''],
    ['目标人群', data.msgInfo.target || ''],
    ['生产模式', data.msgInfo.productionMode ? '是' : '否'],
    ['发送时间', data.msgInfo.pushTime || data.msgInfo.sendTime || ''],
    ['创建时间', data.msgInfo.createTime || ''],
    ['状态', data.msgInfo.status || ''],
    ['厂商通道配置', data.msgInfo.channelActivity ? '已配置' : '未配置'],
];
infoFields.forEach(([label, value]) => {{
    if (value) {{
        const div = document.createElement('div');
        div.className = 'info-item';
        div.innerHTML = `<div class="label">${{label}}</div><div class="value">${{value}}</div>`;
        infoGrid.appendChild(div);
    }}
}});

// 推送统计漏斗
function parseNum(v) {{ if (v == null) return 0; return typeof v === 'string' ? parseInt(v.replace(/,/g,'')) || 0 : v; }}

const md = Array.isArray(data.msgData) ? (data.msgData[0] || {{}}) : (data.msgData || {{}});
const funnelSteps = [
    ['计划发送', parseNum(md.totalCount || md.pushCnt)],
    ['实际发送', parseNum(md.sentCount || md.pushCnt || md.totalCount)],
    ['消息送达', parseNum(md.arriveCount || md.arriveCnt)],
    ['消息展示', parseNum(md.showCount || md.showCnt)],
    ['消息点击', parseNum(md.clickCount || md.clickCnt)],
    ['消息忽略', parseNum(md.ignoreCount || md.ignoreCnt)],
]];
const maxVal = Math.max(...funnelSteps.map(s => s[1]), 1);
const funnelEl = document.getElementById('funnelStats');
funnelSteps.forEach(([label, value]) => {{
    const pct = (value / maxVal * 100).toFixed(1);
    const rate = value > 0 ? '' : '';
    funnelEl.innerHTML += `<div class="stat-row">
        <div class="label">${{label}}</div>
        <div class="bar-container"><div class="bar" style="width:${{pct}}%"></div></div>
        <div class="value">${{value.toLocaleString()}}</div>
    </div>`;
}});

// 漏斗图
new Chart(document.getElementById('funnelChart'), {{
    type: 'bar',
    data: {{
        labels: funnelSteps.map(s => s[0]),
        datasets: [{{
            label: '数量',
            data: funnelSteps.map(s => s[1]),
            backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe'],
            borderRadius: 8,
        }}]
    }},
    options: {{
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ display: false }} }},
        scales: {{ x: {{ beginAtZero: true }} }}
    }}
}});

// 失败原因分析
const expStat = data.expStat;
let expItems = [];
if (Array.isArray(expStat)) {{ expItems = expStat; }}
else if (expStat && typeof expStat === 'object') {{
    expItems = expStat.list || expStat.dataList || expStat.items || [];
    if (expItems.length === 0 && !Array.isArray(expItems)) {{
        document.getElementById('expStatContent').innerHTML = `<p>数据: ${{JSON.stringify(expStat)}}</p>`;
    }}
}}
if (expItems.length > 0) {{
    const total = expItems.reduce((sum, item) => sum + parseNum(item.count || item.num || item.cnt || 0), 0);
    // 表格
    let html = '<table><thead><tr><th>阶段</th><th>通道</th><th>原因</th><th>数量</th><th>占比</th></tr></thead><tbody>';
    expItems.forEach(item => {{
        const count = parseNum(item.count || item.num || item.cnt || 0);
        const ratio = total > 0 ? (count / total * 100).toFixed(2) + '%' : 'N/A';
        html += `<tr><td>${{item.stage || item.phase || ''}}</td><td>${{getChName(item.channel || '')}}</td><td>${{item.reason || item.cause || item.errorMsg || ''}}</td><td>${{count.toLocaleString()}}</td><td>${{ratio}}</td></tr>`;
    }});
    html += '</tbody></table>';
    document.getElementById('expStatContent').innerHTML = html;

    // 饼图
    new Chart(document.getElementById('expChart'), {{
        type: 'doughnut',
        data: {{
            labels: expItems.map(item => (item.stage || '') + ' - ' + getChName(item.channel || '')),
            datasets: [{{
                data: expItems.map(item => parseNum(item.count || item.num || item.cnt || 0)),
                backgroundColor: ['#667eea', '#764ba2', '#f093fb', '#f5576c', '#4facfe', '#00f2fe', '#43e97b', '#fa709a'],
            }}]
        }},
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{ legend: {{ position: 'right' }} }}
        }}
    }});
}} else {{
    document.getElementById('expStatContent').innerHTML = '<p>暂无失败分析数据</p>';
    document.getElementById('expChart').parentElement.style.display = 'none';
}}

// 厂商通道集成状态
if (data.isAndroid) {{
    const ciCard = document.getElementById('channelInfoCard');
    const csCard = document.getElementById('channelStatsCard');
    ciCard.style.display = 'block';
    csCard.style.display = 'block';

    // 通道集成状态
    let chList = [];
    const ci = data.channelInfo;
    if (Array.isArray(ci)) {{ chList = ci; }}
    else if (ci && typeof ci === 'object') {{
        chList = ci.list || ci.channelList || ci.channels || [];
        if (chList.length === 0 && !Array.isArray(chList)) {{
            for (const k in ci) {{
                if (typeof ci[k] === 'object') {{ ci[k].name = k; chList.push(ci[k]); }}
                else {{ chList.push({{name: k, integrated: ci[k], enabled: ci[k]}}); }}
            }}
        }}
    }}

    const statusEl = document.getElementById('channelStatus');
    if (chList.length > 0) {{
        chList.forEach(ch => {{
            const name = ch.name || ch.channelName || ch.channel || '';
            const integrated = ch.integrated || ch.isEnabled || ch.enabled || ch.status;
            const isInt = integrated && ![0, '0', 'false', false].includes(integrated);
            statusEl.innerHTML += `<div class="ch-card ${{isInt ? 'integrated' : 'not-integrated'}}">
                <div class="name">${{getChName(name)}}</div>
                <div class="status">${{isInt ? '\u2705 已集成' : '\u274c 未集成'}}</div>
            </div>`;
        }});
    }}

    // 分通道统计
    let csItems = [];
    const cs = data.channelStats;
    if (Array.isArray(cs)) {{ csItems = cs; }}
    else if (cs && typeof cs === 'object') {{
        csItems = cs.list || cs.dataList || cs.items || [];
        if (csItems.length === 0 && !Array.isArray(csItems)) {{
            for (const k in cs) {{
                if (typeof cs[k] === 'object') {{ cs[k].channel = k; csItems.push(cs[k]); }}
            }}
        }}
    }}

    if (csItems.length > 0) {{
        let tblHtml = '<table><thead><tr><th>通道</th><th>发送</th><th>送达</th><th>送达率</th><th>展示</th><th>展示率</th><th>点击</th><th>送达点击率</th></tr></thead><tbody>';
        const chLabels = [], chSent = [], chArrive = [], chShow = [], chClick = [];
        csItems.forEach(item => {{
            const ch = getChName(item.channel || item.channelName || '');
            const sent = parseNum(item.sentCount || item.sendCount || item.sent || 0);
            const arrive = parseNum(item.arriveCount || item.arrive || 0);
            const show = parseNum(item.showCount || item.show || 0);
            const click = parseNum(item.clickCount || item.click || 0);
            const ar = item.arriveRate || (sent > 0 ? (arrive / sent * 100).toFixed(2) + '%' : 'N/A');
            const sr = item.showRate || (arrive > 0 ? (show / arrive * 100).toFixed(2) + '%' : 'N/A');
            const cr = item.clickRate || (arrive > 0 ? (click / arrive * 100).toFixed(2) + '%' : 'N/A');
            tblHtml += `<tr><td>${{ch}}</td><td>${{sent.toLocaleString()}}</td><td>${{arrive.toLocaleString()}}</td><td>${{ar}}</td><td>${{show.toLocaleString()}}</td><td>${{sr}}</td><td>${{click.toLocaleString()}}</td><td>${{cr}}</td></tr>`;
            chLabels.push(ch);
            chSent.push(sent);
            chArrive.push(arrive);
            chShow.push(show);
            chClick.push(click);
        }});
        tblHtml += '</tbody></table>';
        document.getElementById('channelStatsTable').innerHTML = tblHtml;

        new Chart(document.getElementById('channelChart'), {{
            type: 'bar',
            data: {{
                labels: chLabels,
                datasets: [
                    {{ label: '发送', data: chSent, backgroundColor: '#667eea' }},
                    {{ label: '送达', data: chArrive, backgroundColor: '#764ba2' }},
                    {{ label: '展示', data: chShow, backgroundColor: '#f093fb' }},
                    {{ label: '点击', data: chClick, backgroundColor: '#f5576c' }},
                ]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                plugins: {{ legend: {{ position: 'top' }} }},
                scales: {{ y: {{ beginAtZero: true }} }}
            }}
        }});
    }}
}}
</script>
</body>
</html>
"""

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)

    return filepath


def open_html_report(filepath):
    """在浏览器中打开 HTML 报告"""
    try:
        import subprocess
        import platform
        if platform.system() == 'Darwin':
            subprocess.run(['open', filepath], check=True)
        elif platform.system() == 'Windows':
            subprocess.run(['start', filepath], shell=True, check=True)
        else:
            subprocess.run(['xdg-open', filepath], check=True)
        print(f"\n\U0001f310 已在浏览器中打开报告")
    except Exception:
        print(f"\n\U0001f4c4 报告已生成: {filepath}")
        print(f"   请在浏览器中打开: file://{filepath}")


def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("使用方法：python scripts/query_msg_detail.py <appkey> <msg_id> [--html]")
        print("")
        print("参数说明:")
        print("  appkey    - 应用的唯一标识（必填）")
        print("  msg_id    - 消息 ID（必填）")
        print("  --html    - 生成 HTML 可视化报告（可选）")
        print("")
        print("示例:")
        print("  python scripts/query_msg_detail.py EXAMPLE_APPKEY_005 abcdefg12345678901234")
        print("  python scripts/query_msg_detail.py EXAMPLE_APPKEY_005 abcdefg12345678901234 --html")
        print("")
        print("注意: API 单播消息（以 uu/ul/ua 开头且倒数第二位是 0）不支持查询单条消息明细")
        sys.exit(1)

    appkey = sys.argv[1]
    msg_id = sys.argv[2]
    generate_html = '--html' in sys.argv

    # 1. API 单播检测
    if is_api_unicast(msg_id):
        print("\n" + "=" * 260)
        print(f"\u26a0\ufe0f  警告：该消息为 API 单播消息（msg_id: {msg_id}）")
        print("=" * 260)
        print(f"\nAPI 单播消息不支持单条消息详情查询。")
        print(f"请使用 query_msg_list.py --api-page 1 查看 API 单播统计数据。")
        sys.exit(0)

    print(f"\n{'=' * 260}")
    print(f"\U0001f50d 友盟推送 - 单条消息详情查询")
    print(f"{'=' * 260}")
    print(f"应用 Key   : {appkey}")
    print(f"消息 ID    : {msg_id}")
    print(f"{'=' * 260}")

    # 2. 接口 1：getMsgInfo（必须成功）
    print(f"\n\u3010步骤 1/5\u3011 查询消息基本信息...")
    msg_info_result = call_get_msg_info(appkey, msg_id)

    if not msg_info_result.get('status'):
        print(f"\n\u274c 查询失败：{msg_info_result.get('msg', msg_info_result.get('error', '未知错误'))}")
        if msg_info_result.get('message'):
            print(f"   详细信息：{msg_info_result['message'][:200]}")
        sys.exit(1)

    print(f"\u2705 消息基本信息查询成功")
    display_msg_info(msg_info_result, appkey, msg_id)

    # 3. 平台检测
    msg_info_data = msg_info_result.get('data', {})
    platform = (msg_info_data.get('platform') or '').lower()
    if not platform:
        print(f"\n\u3010平台检测\u3011 从消息信息中未获取到平台类型，尝试从应用列表获取...")
        platform = get_app_platform(appkey) or 'unknown'
        print(f"   应用平台: {platform}")
    is_android = (platform == 'android')

    # 4. 接口 2：getMsgData
    print(f"\n\u3010步骤 2/5\u3011 查询推送统计数据...")
    msg_data_result = call_get_msg_data(appkey, msg_id)
    if msg_data_result.get('status'):
        print(f"\u2705 推送统计查询成功")
        display_msg_data(msg_data_result)
    else:
        print(f"\u26a0\ufe0f  推送统计查询失败：{msg_data_result.get('msg', '未知错误')}")

    # 5. 接口 3：getPushExpStatData
    print(f"\n\u3010步骤 3/5\u3011 查询失败分析数据...")
    exp_stat_result = call_get_push_exp_stat(appkey, msg_id)
    if exp_stat_result.get('status'):
        print(f"\u2705 失败分析查询成功")
        display_exp_stat(exp_stat_result)
    else:
        print(f"\u26a0\ufe0f  失败分析查询失败：{exp_stat_result.get('msg', '未知错误')}")

    # 6. Android 专属接口
    channel_info_result = {}
    channel_stat_result = {}
    if is_android:
        # 接口 4：getChannelInfo
        print(f"\n\u3010步骤 4/5\u3011 查询厂商通道集成状态...")
        channel_info_result = call_get_channel_info(appkey)
        if channel_info_result.get('status'):
            print(f"\u2705 通道集成状态查询成功")
            channel_activity = msg_info_data.get('channelActivity')
            display_channel_info(channel_info_result, appkey, channel_activity)
        else:
            print(f"\u26a0\ufe0f  通道集成状态查询失败：{channel_info_result.get('msg', '未知错误')}")

        # 接口 5：getMsgStatChannelData
        print(f"\n\u3010步骤 5/5\u3011 查询分通道送达统计...")
        channel_stat_result = call_get_msg_stat_channel(appkey, msg_id)
        if channel_stat_result.get('status'):
            print(f"\u2705 分通道统计查询成功")
            display_channel_stats(channel_stat_result)
        else:
            print(f"\u26a0\ufe0f  分通道统计查询失败：{channel_stat_result.get('msg', '未知错误')}")
    else:
        print(f"\n\u3010步骤 4/5\u3011 跳过（非 Android 应用）")
        print(f"\u3010步骤 5/5\u3011 跳过（非 Android 应用）")

    # 7. HTML 报告
    if generate_html:
        print(f"\n\u3010生成 HTML 报告\u3011")
        all_data = {
            'msgInfo': msg_info_data,
            'msgData': msg_data_result.get('data', {}) if msg_data_result.get('status') else {},
            'expStat': exp_stat_result.get('data', {}) if exp_stat_result.get('status') else {},
            'channelInfo': channel_info_result.get('data', {}) if is_android and channel_info_result.get('status') else {},
            'channelStats': channel_stat_result.get('data', {}) if is_android and channel_stat_result.get('status') else {},
        }
        html_file = generate_html_report(all_data, appkey, msg_id, is_android)
        if html_file:
            open_html_report(html_file)

    print(f"\n{'=' * 260}")
    print(f"\u2705 查询完成")
    print(f"{'=' * 260}")


if __name__ == "__main__":
    main()
