#!/usr/bin/env python3
"""
友盟推送助手 - 概况统计查询
调用 upush.umeng.com API 查询应用概况统计数据
包括：应用概况、推送转换数据、厂商额度（仅安卓）
"""

import json
import os
import sys
import urllib.request
import urllib.error
import webbrowser
from datetime import datetime, timedelta
from pathlib import Path

COOKIE_FILE = os.path.expanduser("~/.qoderwork/skills/umeng-push-helper/cookie.txt")
SCRIPT_DIR = Path(__file__).parent
TEMPLATE_FILE = SCRIPT_DIR / "overview_stats_template.html"
OUTPUT_DIR = Path.home() / ".qoderwork" / "workspace" / "mnic36dybkkwfj9m" / "outputs"

# 支持的日期类型
DATE_TYPES = {
    "1d": "昨日",
    "3d": "近 3 日",
    "7d": "近 7 日"
}

# 消息类型
MSG_TYPES = {
    "notification": "通知栏消息",
    "message": "消息"
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
    except Exception as e:
        return {
            'success': False,
            'error': '未知错误',
            'message': str(e)
        }

def query_app_cnt(appkey):
    """查询应用概况统计"""
    url = "https://upush.umeng.com/hsf/overview/getAppCnt"
    data = {"appkey": appkey}
    
    result = make_request(url, data)
    return result

def query_transform_data(appkey, msg_type="notification", date_type="1d"):
    """查询推送转换数据"""
    url = "https://upush.umeng.com/hsf/overview/getTransformData"
    data = {
        "appkey": appkey,
        "msgType": msg_type,
        "dateType": date_type
    }
    
    result = make_request(url, data)
    return result

def query_third_quota(appkey):
    """查询第三方指标（厂商额度）"""
    url = "https://upush.umeng.com/hsf/overview/queryThirdQuota"
    data = {"appkey": appkey}
    
    result = make_request(url, data)
    return result

def display_app_cnt(result, appkey):
    """展示应用概况统计"""
    print("\n" + "=" * 80)
    print(f"📊 应用概况统计")
    print("=" * 80)
    
    if not result.get('status'):
        print(f"❌ 查询失败：{result.get('msg', '未知错误')}")
        return
    
    data = result.get('data', {})
    
    # 数据格式是 list，需要解析
    items = data.get('list', [])
    
    # 提取各指标
    active_users = 0
    arrive_users = 0
    uninstall_users = 0
    close_notify_users = 0
    
    for item in items:
        name = item.get('name', '')
        value = item.get('value', '0')
        # value 可能是字符串（带逗号）或数字
        if isinstance(value, str):
            value = int(value.replace(',', ''))
        
        if name == '活跃用户':
            active_users = value
        elif name == '送达用户':
            arrive_users = value
        elif name == '卸载用户':
            uninstall_users = value
        elif name == '关闭通知用户':
            close_notify_users = value
    
    print(f"\n应用 Key: {appkey}")
    print("-" * 80)
    print(f"{'指标':<25} {'数值':>20}")
    print("-" * 80)
    print(f"{'活跃用户':<25} {active_users:>20,}")
    print(f"{'送达用户':<25} {arrive_users:>20,}")
    print(f"{'卸载用户':<25} {uninstall_users:>20,}")
    print(f"{'关闭通知用户':<25} {close_notify_users:>20,}")
    print("-" * 80)
    
    return data

def display_transform_data(result, msg_type, date_type):
    """展示推送转换数据"""
    print("\n" + "=" * 80)
    print(f"📱 推送转换数据 ({MSG_TYPES.get(msg_type, msg_type)} - {DATE_TYPES.get(date_type, date_type)})")
    print("=" * 80)
    
    if not result.get('status'):
        print(f"❌ 查询失败：{result.get('msg', '未知错误')}")
        return
    
    data = result.get('data', {})
    
    # 数据格式是 list，需要解析
    items = data.get('list', [])
    
    # 提取各阶段数据
    stages = {}
    for item in items:
        name = item.get('name', '')
        value = item.get('value', 0)
        stage_type = item.get('type', '')
        stages[stage_type] = {'name': name, 'value': value}
    
    # 获取各阶段的值
    accept_val = stages.get('accept', {}).get('value', 0)
    sent_val = stages.get('sent', {}).get('value', 0)
    arrive_val = stages.get('arrive', {}).get('value', 0)
    show_val = stages.get('show', {}).get('value', 0)
    click_val = stages.get('click', {}).get('value', 0)
    
    # 计算各阶段比率
    sent_rate = (sent_val / accept_val * 100) if accept_val > 0 else 0
    arrive_rate = (arrive_val / sent_val * 100) if sent_val > 0 else 0
    show_rate = (show_val / arrive_val * 100) if arrive_val > 0 else 0
    click_rate = (click_val / show_val * 100) if show_val > 0 else 0
    
    print(f"\n{'阶段':<20} {'数量':>15} {'占上一阶段比率':>15}")
    print("-" * 60)
    print(f"{'有效设备':<20} {accept_val:>15,}")
    print(f"{'实际发送':<20} {sent_val:>15,} {sent_rate:>13.2f}%")
    print(f"{'消息送达':<20} {arrive_val:>15,} {arrive_rate:>13.2f}%")
    print(f"{'消息展示':<20} {show_val:>15,} {show_rate:>13.2f}%")
    print(f"{'消息点击':<20} {click_val:>15,} {click_rate:>13.2f}%")
    print("-" * 60)
    
    # 显示转化漏斗
    print(f"\n📊 转化漏斗:")
    max_bar = 50
    accept_bar = "█" * max_bar
    sent_bar = "█" * int(max_bar * sent_rate / 100)
    arrive_bar = "█" * int(max_bar * arrive_rate / 100)
    show_bar = "█" * int(max_bar * show_rate / 100)
    click_bar = "█" * int(max_bar * click_rate / 100)
    
    print(f"有效设备   {accept_bar} {accept_val:,}")
    print(f"实际发送   {sent_bar} {sent_val:,} ({sent_rate:.2f}%)")
    print(f"消息送达   {arrive_bar} {arrive_val:,} ({arrive_rate:.2f}%)")
    print(f"消息展示   {show_bar} {show_val:,} ({show_rate:.2f}%)")
    print(f"消息点击   {click_bar} {click_val:,} ({click_rate:.2f}%)")
    
    return data

def display_third_quota(result, appkey):
    """展示第三方指标（厂商额度）"""
    print("\n" + "=" * 80)
    print(f"🏭 厂商通道额度统计")
    print("=" * 80)
    
    if not result.get('status'):
        print(f"❌ 查询失败：{result.get('msg', '未知错误')}")
        return
    
    data = result.get('data', {})
    
    # 提取各厂商额度数据
    vendors = {
        'huawei': '华为',
        'xiaomi': '小米',
        'oppo': 'OPPO',
        'vivo': 'VIVO',
        'honor': '荣耀',
        'meizu': '魅族'
    }
    
    print(f"\n应用 Key: {appkey}")
    print("-" * 80)
    print(f"{'厂商':<15} {'剩余额度':>15} {'总额度':>15} {'使用率':>15}")
    print("-" * 80)
    
    has_data = False
    
    # OPPO 额度
    oppo_total = data.get('oppoTotalCount', 0) or 0
    oppo_remain = data.get('oppoRemainCount', 0) or 0
    if oppo_total > 0:
        has_data = True
        oppo_used = oppo_total - oppo_remain
        oppo_usage = (oppo_used / oppo_total * 100) if oppo_total > 0 else 0
        bar = "█" * int(oppo_usage / 2) + "░" * (50 - int(oppo_usage / 2))
        print(f"{'OPPO':<15} {oppo_remain:>15,} {oppo_total:>15,} {oppo_usage:>13.2f}% |{bar}|")
    
    # 小米额度
    xm_quota = data.get('xmQuotaCount', 0) or 0
    xm_acked = data.get('xmAckedCount', 0) or 0
    if xm_quota > 0:
        has_data = True
        xm_remain = xm_quota - xm_acked
        xm_usage = (xm_acked / xm_quota * 100) if xm_quota > 0 else 0
        bar = "█" * int(xm_usage / 2) + "░" * (50 - int(xm_usage / 2))
        print(f"{'小米':<15} {xm_remain:>15,} {xm_quota:>15,} {xm_usage:>13.2f}% |{bar}|")
    
    # vivo 额度 - vivoSysMsgCount 是系统消息总量，vivoMarketMsgCount 是运营消息总量
    vivo_sys = data.get('vivoSysMsgCount', 0) or 0
    vivo_market = data.get('vivoMarketMsgCount', 0) or 0
    if vivo_sys > 0 or vivo_market > 0:
        has_data = True
        print(f"{'VIVO':<15} {'系统:' + str(vivo_sys):>15} {'运营:' + str(vivo_market):>15}")
    
    if not has_data:
        print("暂无厂商额度数据")
    
    print("-" * 80)
    
    return data

def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法：python scripts/query_overview_stats.py <appkey> [date_type] [msg_type]")
        print("")
        print("参数说明:")
        print("  appkey     - 应用的唯一标识（必填）")
        print("  date_type  - 日期类型：1d(昨日), 3d(近 3 日), 7d(近 7 日)，默认 1d")
        print("  msg_type   - 消息类型：notification(通知栏消息), message(消息)，默认 notification")
        print("")
        print("示例:")
        print("  # 查询昨日数据（默认）")
        print("  python scripts/query_overview_stats.py EXAMPLE_APPKEY_005")
        print("")
        print("  # 查询近 7 日数据")
        print("  python scripts/query_overview_stats.py EXAMPLE_APPKEY_005 7d")
        print("")
        print("  # 查询消息类型的近 3 日数据")
        print("  python scripts/query_overview_stats.py EXAMPLE_APPKEY_005 3d message")
        print("")
        print("💡 提示：如果是安卓应用，会自动查询厂商额度数据")
        sys.exit(1)
    
    appkey = sys.argv[1]
    date_type = sys.argv[2] if len(sys.argv) > 2 else "1d"
    msg_type = sys.argv[3] if len(sys.argv) > 3 else "notification"
    
    # 验证日期类型
    if date_type not in DATE_TYPES:
        print(f"\n❌ 错误：无效的日期类型 '{date_type}'")
        print(f"\n✅ 支持的日期类型:")
        for key, name in DATE_TYPES.items():
            print(f"   {key} - {name}")
        print(f"\n示例：python scripts/query_overview_stats.py {appkey} 7d")
        sys.exit(1)
    
    # 验证消息类型
    if msg_type not in MSG_TYPES:
        print(f"\n❌ 错误：无效的消息类型 '{msg_type}'")
        print(f"\n✅ 支持的消息类型:")
        for key, name in MSG_TYPES.items():
            print(f"   {key} - {name}")
        print(f"\n示例：python scripts/query_overview_stats.py {appkey} {date_type} notification")
        sys.exit(1)
    
    print("=" * 80)
    print("📊 友盟推送 - 概况统计")
    print("=" * 80)
    print(f"应用 Key   : {appkey}")
    print(f"时间范围   : {DATE_TYPES.get(date_type, date_type)}")
    print(f"消息类型   : {MSG_TYPES.get(msg_type, msg_type)}")
    print("=" * 80)
    
    # 1. 查询应用概况
    print(f"\n📊 正在查询 应用概况...")
    app_cnt_result = query_app_cnt(appkey)
    if app_cnt_result.get('status'):
        print(f"✅ 应用概况 查询成功")
        app_cnt_data = display_app_cnt(app_cnt_result, appkey)
    else:
        print(f"❌ 应用概况 查询失败：{app_cnt_result.get('msg', '未知错误')}")
    
    # 2. 查询推送转换数据
    print(f"\n📱 正在查询 推送转换数据...")
    transform_result = query_transform_data(appkey, msg_type, date_type)
    if transform_result.get('status'):
        print(f"✅ 推送转换数据 查询成功")
        transform_data = display_transform_data(transform_result, msg_type, date_type)
    else:
        print(f"❌ 推送转换数据 查询失败：{transform_result.get('msg', '未知错误')}")
    
    # 3. 查询厂商额度（仅安卓）
    print(f"\n🏭 正在查询 厂商通道额度...")
    print(f"💡 提示：仅安卓应用需要查询此项")
    third_quota_result = query_third_quota(appkey)
    if third_quota_result.get('status'):
        print(f"✅ 厂商通道额度 查询成功")
        third_quota_data = display_third_quota(third_quota_result, appkey)
    else:
        print(f"❌ 厂商通道额度 查询失败：{third_quota_result.get('msg', '未知错误')}")
    
    print("\n" + "=" * 80)
    print("✅ 概况统计查询完成")
    print("=" * 80 + "\n")

def generate_html_report(app_cnt_data, transform_data, third_quota_data, appkey, msg_type, date_type):
    """生成 HTML 可视化报告"""
    
    # 读取模板
    if not TEMPLATE_FILE.exists():
        print(f"\n⚠️  警告：模板文件不存在：{TEMPLATE_FILE}")
        return None
    
    with open(TEMPLATE_FILE, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 准备数据
    data_script = f"""
    <script>
        // 注入数据
        window.appOverviewData = {json.dumps(app_cnt_data, ensure_ascii=False) if app_cnt_data else 'null'};
        window.transformData = {json.dumps(transform_data, ensure_ascii=False) if transform_data else 'null'};
        window.vendorData = {json.dumps(third_quota_data, ensure_ascii=False) if third_quota_data else 'null'};
        window.msgType = '{msg_type}';
        window.dateType = '{date_type}';
        
        // 更新应用 Key 显示
        document.addEventListener('DOMContentLoaded', function() {{
            const appkeyEl = document.getElementById('appkey');
            if (appkeyEl) {{
                appkeyEl.textContent = '{appkey}';
            }}
        }});
    </script>
    """
    
    # 将数据脚本插入到 template 的 script 之前
    html_content = html_content.replace(
        '<!-- 从 window 对象读取数据（由 Python 脚本注入） -->',
        data_script
    )
    
    # 确保输出目录存在
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"overview_stats_{appkey}_{timestamp}.html"
    
    # 写入文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return output_file

def open_html_report(file_path):
    """在浏览器中打开 HTML 报告"""
    if file_path and os.path.exists(file_path):
        try:
            webbrowser.open(f'file://{file_path}')
            print(f"\n🌐 已在浏览器中打开报告：{file_path}")
        except Exception as e:
            print(f"\n⚠️  无法自动打开浏览器：{e}")
            print(f"📄 报告文件位置：{file_path}")
    else:
        print(f"\n❌ 报告文件不存在：{file_path}")

if __name__ == "__main__":
    # 检查是否需要生成 HTML 报告
    generate_html = '--html' in sys.argv or '-h' in sys.argv
    
    if len(sys.argv) < 2 or (generate_html and len(sys.argv) < 3):
        print("使用方法：python scripts/query_overview_stats.py <appkey> [date_type] [msg_type] [--html]")
        print("")
        print("参数说明:")
        print("  appkey     - 应用的唯一标识（必填）")
        print("  date_type  - 日期类型：1d(昨日), 3d(近 3 日), 7d(近 7 日)，默认 1d")
        print("  msg_type   - 消息类型：notification(通知栏消息), message(消息)，默认 notification")
        print("  --html     - 生成 HTML 可视化报告（可选）")
        print("")
        print("示例:")
        print("  # 查询昨日数据（默认）")
        print("  python scripts/query_overview_stats.py EXAMPLE_APPKEY_005")
        print("")
        print("  # 查询并生成 HTML 报告")
        print("  python scripts/query_overview_stats.py EXAMPLE_APPKEY_005 --html")
        print("")
        print("  # 查询近 7 日数据并生成报告")
        print("  python scripts/query_overview_stats.py EXAMPLE_APPKEY_005 7d --html")
        print("")
        print("  # 查询消息类型的近 3 日数据")
        print("  python scripts/query_overview_stats.py EXAMPLE_APPKEY_005 3d message")
        print("")
        print("💡 提示：如果是安卓应用，会自动查询厂商额度数据")
        sys.exit(1)
    
    # 提取参数
    args = [arg for arg in sys.argv[1:] if not arg.startswith('--')]
    appkey = args[0]
    date_type = args[1] if len(args) > 1 else "1d"
    msg_type = args[2] if len(args) > 2 else "notification"
    
    # 验证日期类型
    if date_type not in DATE_TYPES:
        print(f"\n❌ 错误：无效的日期类型 '{date_type}'")
        print(f"\n✅ 支持的日期类型:")
        for key, name in DATE_TYPES.items():
            print(f"   {key} - {name}")
        print(f"\n示例：python scripts/query_overview_stats.py {appkey} 7d")
        sys.exit(1)
    
    # 验证消息类型
    if msg_type not in MSG_TYPES:
        print(f"\n❌ 错误：无效的消息类型 '{msg_type}'")
        print(f"\n✅ 支持的消息类型:")
        for key, name in MSG_TYPES.items():
            print(f"   {key} - {name}")
        print(f"\n示例：python scripts/query_overview_stats.py {appkey} {date_type} notification")
        sys.exit(1)
    
    print("=" * 80)
    print("📊 友盟推送 - 概况统计")
    print("=" * 80)
    print(f"应用 Key   : {appkey}")
    print(f"时间范围   : {DATE_TYPES.get(date_type, date_type)}")
    print(f"消息类型   : {MSG_TYPES.get(msg_type, msg_type)}")
    print("=" * 80)
    
    # 存储各 API 返回的数据
    app_cnt_data = None
    transform_data = None
    third_quota_data = None
    
    # 1. 查询应用概况
    print(f"\n📊 正在查询 应用概况...")
    app_cnt_result = query_app_cnt(appkey)
    if app_cnt_result.get('status'):
        print(f"✅ 应用概况 查询成功")
        app_cnt_data = display_app_cnt(app_cnt_result, appkey)
    else:
        print(f"❌ 应用概况 查询失败：{app_cnt_result.get('msg', '未知错误')}")
    
    # 2. 查询推送转换数据
    print(f"\n📱 正在查询 推送转换数据...")
    transform_result = query_transform_data(appkey, msg_type, date_type)
    if transform_result.get('status'):
        print(f"✅ 推送转换数据 查询成功")
        transform_data = display_transform_data(transform_result, msg_type, date_type)
    else:
        print(f"❌ 推送转换数据 查询失败：{transform_result.get('msg', '未知错误')}")
    
    # 3. 查询厂商额度（仅安卓）
    print(f"\n🏭 正在查询 厂商通道额度...")
    print(f"💡 提示：仅安卓应用需要查询此项")
    third_quota_result = query_third_quota(appkey)
    if third_quota_result.get('status'):
        print(f"✅ 厂商通道额度 查询成功")
        third_quota_data = display_third_quota(third_quota_result, appkey)
    else:
        print(f"❌ 厂商通道额度 查询失败：{third_quota_result.get('msg', '未知错误')}")
    
    print("\n" + "=" * 80)
    print("✅ 概况统计查询完成")
    print("=" * 80 + "\n")
    
    # 如果请求了 HTML 报告，则生成并打开
    if generate_html:
        print("\n📊 正在生成 HTML 可视化报告...")
        html_file = generate_html_report(
            app_cnt_data, 
            transform_data, 
            third_quota_data, 
            appkey, 
            msg_type, 
            date_type
        )
        if html_file:
            open_html_report(html_file)
