#!/usr/bin/env python3
"""
友盟推送助手 - 推送轨迹查询
调用 upush.umeng.com API 查询推送消息的完整轨迹
包括：消息生命周期、设备信息、请求内容、当天消息列表
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

def query_tool_life_cycle(appkey, device_token, msg_id):
    """
    步骤 1：查询消息生命周期
    
    Args:
        appkey: 应用 key
        device_token: 设备 token
        msg_id: 消息 ID
    """
    url = "https://upush.umeng.com/hsf/push/getToolLifeCycle"
    data = {
        "appkey": appkey,
        "deviceToken": device_token,
        "msgId": msg_id
    }
    
    print(f"\n{'='*80}")
    print(f"步骤 1：查询消息生命周期")
    print(f"{'='*80}")
    print(f"接口：{url}")
    print(f"请求参数:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    result = make_request(url, data)
    
    print(f"\n返回结果:")
    if result.get('status'):
        print(json.dumps(result.get('data', {}), indent=2, ensure_ascii=False))
    else:
        print(f"查询失败：{result.get('msg', '未知错误')}")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return result

def query_device_info(appkey, device_token, app_platform=None):
    """
    步骤 2：查询设备信息
    
    Args:
        appkey: 应用 key
        device_token: 设备 token
        app_platform: 应用平台 (android/ios/harmony)，用于判断是否检查 valid 字段
    """
    url = "https://upush.umeng.com/hsf/setting/getDeviceInfo"
    data = {
        "appkey": appkey,
        "deviceToken": device_token
    }
    
    print(f"\n{'='*80}")
    print(f"步骤 2：查询设备信息")
    print(f"{'='*80}")
    print(f"接口：{url}")
    print(f"请求参数:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    result = make_request(url, data)
    
    print(f"\n返回结果:")
    if result.get('status'):
        data_result = result.get('data', {})
        print(json.dumps(data_result, indent=2, ensure_ascii=False))
        
        # 检查是否为安卓/鸿蒙设备，并分析 thirdTokens 字段
        brand = data_result.get('brand', '').upper()
        is_android_or_harmony = brand in ['HUAWEI', 'XIAOMI', 'OPPO', 'VIVO', 'HONOR', 'MEIZU', 'ANDROID'] or brand == '' or app_platform in ['android', 'harmony']
        
        if is_android_or_harmony:
            third_tokens = data_result.get('thirdTokens', {})
            print(f"\n{'='*80}")
            print(f"🔍 安卓/鸿蒙设备厂商 Token 检查")
            print(f"{'='*80}")
            
            if not third_tokens:
                print(f"\n❌❌❌ 严重问题：未获取到任何厂商 Token ❌❌❌")
                print(f"\n【问题分析】")
                print(f"   - thirdTokens 字段为空，说明设备未成功注册任何厂商推送通道")
                print(f"   - 当设备离线时，推送将无法通过厂商通道下发")
                print(f"   - 这是导致消息无法送达的重要原因！\n")
                print(f"【可能原因】")
                print(f"   1. 客户端未集成对应厂商的推送 SDK")
                print(f"   2. 厂商推送配置不正确（如 AppKey、AppSecret 配置错误）")
                print(f"   3. 客户端初始化时未正确调用厂商通道注册方法")
                print(f"   4. 设备不支持该厂商推送（如模拟器、定制 ROM）\n")
                print(f"【解决方案】")
                print(f"   1. 检查客户端代码，确认已集成对应厂商的推送 SDK")
                print(f"   2. 在友盟后台配置正确的厂商推送凭证")
                print(f"      路径：友盟后台 → 应用配置 → 推送渠道 → 配置对应厂商")
                print(f"   3. 引导用户重启应用，重新注册推送")
                print(f"   4. 检查客户端日志，查看厂商通道初始化是否成功\n")
            else:
                # thirdTokens 不为空，显示详细内容
                print(f"\n✅ thirdTokens 字段包含内容:\n")
                
                # 常见厂商列表
                known_vendors = {
                    'huawei': '华为',
                    'xiaomi': '小米',
                    'oppo': 'OPPO',
                    'vivo': 'VIVO',
                    'honor': '荣耀',
                    'meizu': '魅族',
                    'fcm': 'FCM(Google)'
                }
                
                has_valid_token = False
                for vendor, token in third_tokens.items():
                    vendor_name = known_vendors.get(vendor.lower(), vendor)
                    if token and token.strip():
                        print(f"   ✅ {vendor_name}: {token[:20]}... (有效)")
                        has_valid_token = True
                    else:
                        print(f"   ⚠️  {vendor_name}: 空值或无效")
                
                if has_valid_token:
                    print(f"\n✅ 设备已成功注册厂商推送通道")
                    print(f"💡 如果仍无法收到消息，请检查：")
                    print(f"   1. 厂商后台配置的证书/凭证是否正确")
                    print(f"   2. 推送内容是否符合厂商规范")
                    print(f"   3. 设备通知权限是否开启")
                else:
                    print(f"\n⚠️  警告：虽然有 thirdTokens 字段，但所有厂商 token 均为空或无效")
                    print(f"💡 这可能导致离线推送失败\n")
                
                print(f"\n{'='*80}")
    else:
        print(f"查询失败：{result.get('msg', '未知错误')}")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return result

def query_tool_request_content(appkey, msg_id):
    """
    步骤 3：查询请求内容
    
    Args:
        appkey: 应用 key
        msg_id: 消息 ID
    """
    url = "https://upush.umeng.com/hsf/push/getToolRequestContent"
    data = {
        "appkey": appkey,
        "msgId": msg_id
    }
    
    print(f"\n{'='*80}")
    print(f"步骤 3：查询推送请求内容")
    print(f"{'='*80}")
    print(f"接口：{url}")
    print(f"请求参数:")
    print(json.dumps(data, indent=2, ensure_ascii=False))
    
    result = make_request(url, data)
    
    print(f"\n返回结果:")
    if result.get('status'):
        print(json.dumps(result.get('data', {}), indent=2, ensure_ascii=False))
    else:
        print(f"查询失败：{result.get('msg', '未知错误')}")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    
    return result

def extract_date_from_msg_id(msg_id):
    """
    从 msg_id 中提取日期
    msg_id 格式：前 7 位 + 13 位时间戳
    取第 8 位开始的 13 位数字作为时间戳
    
    Args:
        msg_id: 消息 ID
    
    Returns:
        yyyy-MM-dd 格式的日期字符串
    """
    try:
        # 从第 8 位开始（索引 7），取 13 位
        timestamp_str = msg_id[7:20]
        timestamp = int(timestamp_str)
        
        # 转换为 datetime
        dt = datetime.fromtimestamp(timestamp / 1000.0)
        
        # 格式化为 yyyy-MM-dd
        return dt.strftime('%Y-%m-%d')
    except Exception as e:
        print(f"⚠️  警告：无法从 msg_id 中解析日期：{e}")
        # 返回当前日期作为后备
        return datetime.now().strftime('%Y-%m-%d')

def query_device_messages(appkey, device_token, msg_id, life_cycle_result=None):
    """
    步骤 4：查询当天消息列表（分页获取所有记录）
    
    Args:
        appkey: 应用 key
        device_token: 设备 token
        msg_id: 目标消息 ID，用于解析日期和过滤
        life_cycle_result: 步骤 1 的返回结果，用于分析失败原因
    """
    # 从 msg_id 中提取日期
    target_date = extract_date_from_msg_id(msg_id)
    
    url = "https://upush.umeng.com/hsf/setting/deviceMessage"
    
    # 第一步：先查询总记录数
    first_page_data = {
        "appkey": appkey,
        "deviceToken": device_token,
        "startDate": target_date,
        "endDate": target_date,
        "page": 1,
        "pageSize": 50
    }
    
    print(f"\n{'='*80}")
    print(f"步骤 4：查询当天消息列表 ({target_date})")
    print(f"{'='*80}")
    print(f"接口：{url}")
    print(f"请求参数:")
    print(json.dumps(first_page_data, indent=2, ensure_ascii=False))
    
    # 获取第一页结果
    first_result = make_request(url, first_page_data)
    
    print(f"\n返回结果:")
    if not first_result.get('status'):
        print(f"查询失败：{first_result.get('msg', '未知错误')}")
        print(json.dumps(first_result, indent=2, ensure_ascii=False))
        return first_result
    
    # 解析第一页数据
    data_result = first_result.get('data', {})
    total = data_result.get('total', 0)
    messages = data_result.get('list', [])
    
    print(f"✅ 共查询到 {total} 条消息\n")
    
    # 如果有多页，继续获取剩余页面
    if total > 50:
        page_size = 50
        total_pages = (total + page_size - 1) // page_size
        print(f"📄 分 {total_pages} 页获取...\n")
        
        all_messages = messages.copy()
        
        for page in range(2, total_pages + 1):
            page_data = {
                "appkey": appkey,
                "deviceToken": device_token,
                "startDate": target_date,
                "endDate": target_date,
                "page": page,
                "pageSize": page_size
            }
            
            try:
                page_result = make_request(url, page_data)
                if page_result.get('status'):
                    page_messages = page_result.get('data', {}).get('list', [])
                    all_messages.extend(page_messages)
                    print(f"  ✅ 已获取第 {page}/{total_pages} 页 ({len(page_messages)} 条)")
                else:
                    print(f"  ⚠️  第 {page} 页获取失败：{page_result.get('msg', '未知错误')}")
            except Exception as e:
                print(f"  ⚠️  第 {page} 页获取失败：{e}")
        
        messages = all_messages
        print(f"\n✅ 已完成所有 {len(messages)} 条消息的获取\n")
    
    # 找到目标 msg_id 在列表中的位置
    target_index = -1
    for i, msg in enumerate(messages):
        if msg.get('msgId') == msg_id:
            target_index = i
            break
    
    # 显示所有消息，并标记目标消息
    if target_index >= 0:
        print(f"📋 消息列表（共 {len(messages)} 条，🎯 标记为目标消息）:\n")
        messages_to_show = messages
    else:
        print(f"⚠️  未找到目标 msg_id，显示所有 {len(messages)} 条消息:\n")
        messages_to_show = messages
    
    # 显示消息列表
    print(f"{'序号':<6} {'消息 ID':<25} {'标题':<20} {'发送时间':<20} {'状态':<12} {'通道':<10}")
    print(f"{'-'*100}")
    
    for i, msg in enumerate(messages_to_show, 1):
        msg_id_item = msg.get('msgId', 'N/A')[:22]
        # 从 digest 中解析标题
        title = 'N/A'
        try:
            digest = json.loads(msg.get('digest', '{}'))
            body = digest.get('body', {})
            title = body.get('title', 'N/A') or 'N/A'
        except:
            title = (msg.get('title', 'N/A') or 'N/A')[:18]
        
        send_time = msg.get('startTime', 'N/A')
        status = msg.get('status', 'N/A')
        channel = msg.get('channel', 'N/A')  # 新增：通道字段
        
        # 标记目标消息
        marker = "🎯" if msg.get('msgId') == msg_id else "  "
        
        print(f"{marker}{i:<5} {msg_id_item:<25} {title:<20} {send_time:<20} {status:<12} {channel:<10}")
    
    print(f"\n{'='*80}")
    
    # 分析限流原因：统计同通道成功消息数
    life_cycle_data = life_cycle_result.get('data', {}) if life_cycle_result else {}
    fail_stage = life_cycle_data.get('lifeCycle', {}).get('stageFailWithoutResend') if life_cycle_data else None
    fail_reason = fail_stage.get('extra', '') if fail_stage else ''
    
    if "单应用单设备限量" in fail_reason:
        analysis_result = analyze_channel_success_rate(messages, msg_id, fail_reason)
        
        if analysis_result:
            print(f"\n📊 限流原因分析（失败原因：单应用单设备限量）\n")
            print(f"目标消息通道：{analysis_result['target_channel']}")
            print(f"当天总消息数：{analysis_result['total_messages']} 条")
            print(f"通过 {analysis_result['target_channel']} 通道送达成功：{analysis_result['success_count']} 条\n")
            
            if analysis_result['success_count'] == 0:
                print(f"⚠️  警告：当天没有通过 {analysis_result['target_channel']} 通道送达成功的消息")
                print(f"💡 可能原因：device_token 已发生变化，当前使用的 token 可能不正确\n")
            elif analysis_result['success_count'] == 1:
                print(f"⚠️  警告：当天只有 1 条通过 {analysis_result['target_channel']} 通道送达成功的消息")
                print(f"💡 可能原因：device_token 可能发生了变化，导致限流策略误判\n")
                if analysis_result['success_messages']:
                    success_msg = analysis_result['success_messages'][0]
                    success_msg_id = success_msg.get('msgId', 'N/A')[:22]
                    success_time = success_msg.get('startTime', 'N/A')
                    digest = json.loads(success_msg.get('digest', '{}'))
                    title = digest.get('body', {}).get('title', 'N/A')
                    print(f"   唯一成功的消息：{success_msg_id} - {title} ({success_time})\n")
            else:
                print(f"✅ 当天有 {analysis_result['success_count']} 条通过该通道送达成功的消息")
                print(f"💡 说明 device_token 应该是正确的，限流可能是其他原因导致\n")
            
            print(f"{'='*80}")
    
    return first_result

def analyze_channel_success_rate(messages, target_msg_id, fail_reason):
    """
    分析通道成功率 - 当失败原因为"单应用单设备限量"时调用
    
    Args:
        messages: 当天所有消息列表
        target_msg_id: 目标消息 ID
        fail_reason: 失败原因
    
    Returns:
        dict: 统计结果
    """
    # 检查是否是限流错误
    if "单应用单设备限量" not in fail_reason:
        return None
    
    # 找到目标消息的通道
    target_channel = None
    for msg in messages:
        if msg.get('msgId') == target_msg_id:
            target_channel = msg.get('channel', 'unknown')
            break
    
    if not target_channel:
        return None
    
    # 统计当天通过该通道送达成功的消息数量
    success_count = 0
    success_messages = []
    
    for msg in messages:
        channel = msg.get('channel', 'unknown')
        status = msg.get('status', '')
        
        # 同一通道且状态为"送达成功"
        if channel == target_channel and '送达成功' in status:
            success_count += 1
            success_messages.append(msg)
    
    result = {
        'target_channel': target_channel,
        'success_count': success_count,
        'success_messages': success_messages,
        'total_messages': len(messages)
    }
    
    return result

def get_app_platform(appkey):
    """
    获取应用平台信息
    
    Args:
        appkey: 应用 key
    
    Returns:
        str: 平台类型 (android/ios/harmony)，未知时返回 None
    """
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
    
    try:
        result = make_request(url, data)
        if result.get('status'):
            app_list = result.get('data', {}).get('appList', [])
            for app in app_list:
                if app.get('appkey') == appkey:
                    platform = app.get('platform', '').lower()
                    return platform
        return None
    except Exception as e:
        print(f"⚠️  警告：获取应用平台信息失败：{e}")
        return None

def main():
    """主函数"""
    if len(sys.argv) < 4:
        print("\n" + "="*80)
        print("友盟推送消息排查工具")
        print("="*80)
        print("\n📱 适用场景：")
        print("   - 用户反馈收不到推送消息")
        print("   - 推送显示成功但用户未收到")
        print("   - 需要排查推送失败原因")
        print("\n🔧 用法：python scripts/query_push_trace.py <appkey> <device_token> <msg_id>")
        print("\n示例:")
        print("  python scripts/query_push_trace.py EXAMPLE_APPKEY_001 abc123xyz 1234567890abcdef")
        print("\n参数说明:")
        print("  appkey       - 应用的唯一标识")
        print("  device_token - 设备的推送 token（从设备日志或数据库中获取）")
        print("  msg_id       - 消息 ID（22 位，从推送记录中获取）")
        print("\n💡 如何获取这些参数？")
        print("  1. appkey: 运行 'python scripts/get_app_list.py' 查看应用列表")
        print("  2. device_token: 从客户端日志、数据库或友盟后台的设备管理中获取")
        print("  3. msg_id: 从友盟后台的推送记录中点击具体某条推送查看详情")
        print("="*80 + "\n")
        sys.exit(1)
    
    appkey = sys.argv[1]
    device_token = sys.argv[2]
    msg_id = sys.argv[3]
    
    print(f"\n{'='*80}")
    print(f"🔍 友盟推送消息排查")
    print(f"{'='*80}")
    print(f"应用 Key     : {appkey}")
    print(f"设备 Token   : {device_token}")
    print(f"消息 ID      : {msg_id}")
    print(f"{'='*80}")
    print(f"\n开始排查消息未收到的原因...")
    print(f"{'='*80}\n")
    
    # 获取应用平台信息
    print(f"📱 正在获取应用平台信息...")
    app_platform = get_app_platform(appkey)
    if app_platform:
        print(f"✅ 应用平台：{app_platform}")
        if app_platform == 'ios':
            print(f"ℹ️  iOS 应用将检查 valid 字段")
        else:
            print(f"ℹ️  {app_platform} 应用不检查 valid 字段")
    else:
        print(f"⚠️  无法获取应用平台信息，将自动判断")
    print()
    
    # 步骤 1：查询消息生命周期
    life_cycle_result = query_tool_life_cycle(appkey, device_token, msg_id)
    
    # 步骤 2：查询设备信息（传入 app_platform 用于判断是否检查 valid）
    device_info_result = query_device_info(appkey, device_token, app_platform)
    
    # 步骤 3：查询请求内容
    request_content_result = query_tool_request_content(appkey, msg_id)
    
    # 步骤 4：查询当天消息列表（传入 life_cycle_result 用于分析）
    device_messages_result = query_device_messages(appkey, device_token, msg_id, life_cycle_result)
    
    # 汇总分析
    print(f"\n{'='*80}")
    print(f"📊 排查结果汇总")
    print(f"{'='*80}")
    
    # 分析消息生命周期
    print(f"\n【消息状态分析】")
    if life_cycle_result.get('status') and life_cycle_result.get('data'):
        data = life_cycle_result['data']
        send_time = data.get('sendTime')
        arrive_time = data.get('arriveTime')
        click_time = data.get('clickTime')
        
        if send_time:
            print(f"✅ 消息已发送：{send_time}")
        else:
            print(f"❌ 消息未发送")
        
        if arrive_time:
            print(f"✅ 消息已到达设备：{arrive_time}")
        else:
            if send_time:
                print(f"⚠️  消息已发送但未到达")
        
        if click_time:
            print(f"✅ 用户已点击：{click_time}")
        else:
            if arrive_time:
                print(f"ℹ️  消息已到达但用户未点击")
    else:
        print(f"❌ 无法获取消息状态")
    
    # 分析设备信息
    print(f"\n【设备信息分析】")
    if device_info_result.get('status') and device_info_result.get('data'):
        data = device_info_result['data']
        device_model = data.get('deviceModel', '未知')
        os_version = data.get('osVersion', '未知')
        app_version = data.get('appVersion', '未知')
        push_channel = data.get('pushChannel', '未知')
        
        print(f"✅ 设备信息:")
        print(f"   - 设备型号：{device_model}")
        print(f"   - 系统版本：{os_version}")
        print(f"   - 应用版本：{app_version}")
        print(f"   - 推送通道：{push_channel}")
    else:
        print(f"❌ 无法获取设备信息")
    
    # 分析推送内容
    print(f"\n【推送内容分析】")
    if request_content_result.get('status') and request_content_result.get('data'):
        data = request_content_result['data']
        title = data.get('title', '未知')
        content = data.get('text', '未知')
        push_type = data.get('target', '未知')
        send_time = data.get('startTime', '未知')
        
        print(f"✅ 推送详情:")
        print(f"   - 标题：{title}")
        print(f"   - 内容：{content}")
        print(f"   - 目标类型：{push_type}")
        print(f"   - 发送时间：{send_time}")
    else:
        print(f"❌ 无法获取推送内容")
    
    # 显示问题列表
    print(f"\n{'='*80}")
    print(f"🔍 发现的问题")
    print(f"{'='*80}\n")
    
    issues = []
    
    if not life_cycle_result.get('status') or not life_cycle_result.get('data'):
        issues.append("1. 消息状态查询失败 - 请检查 msg_id 是否正确")
    
    if not device_info_result.get('status') or not device_info_result.get('data'):
        issues.append("2. 设备信息查询失败 - 请检查 device_token 是否正确")
    
    if life_cycle_result.get('status') and life_cycle_result.get('data'):
        lc_data = life_cycle_result['data']
        if not lc_data.get('sendTime'):
            issues.append("3. 消息未发送")
        elif not lc_data.get('arriveTime'):
            # 检查失败原因
            fail_stage = lc_data.get('lifeCycle', {}).get('stageFailWithoutResend')
            if fail_stage:
                fail_reason = fail_stage.get('extra', '未知原因')
                issues.append(f"4. 消息已发送但未到达 - 失败原因：{fail_reason}")
            else:
                issues.append("4. 消息已发送但未到达")
    
    if device_info_result.get('status') and device_info_result.get('data'):
        dev_data = device_info_result['data']
        if not dev_data.get('pushChannel') or dev_data.get('pushChannel') == 'unknown':
            issues.append("5. 推送通道异常")
        if not dev_data.get('online'):
            issues.append("6. 设备当前不在线")
        
        # 仅当应用平台为 iOS 时才检查 valid 字段
        is_ios_app = app_platform == 'ios'
        if is_ios_app and not dev_data.get('valid'):
            issues.append("7. 设备标识已失效 (iOS)")
        elif not is_ios_app:
            # 安卓/鸿蒙应用不检查 valid 字段，但可以显示提示信息
            pass
    
    if issues:
        for issue in issues:
            print(f"   ⚠️  {issue}")
        
        # 显示排查建议与参考资料（基于内置知识库）
        print(f"\n{'='*80}")
        print(f"📖 排查建议与解决方案")
        print(f"{'='*80}")
        
        # 根据问题类型提供针对性的建议
        has_channel_issue = any('不支持厂商' in str(issue) or '推送通道异常' in str(issue) for issue in issues)
        has_offline_issue = any('设备当前不在线' in str(issue) for issue in issues)
        has_arrive_issue = any('消息已发送但未到达' in str(issue) for issue in issues)
        
        if has_channel_issue or has_arrive_issue:
            print(f"\n🔍 针对「不支持厂商通道」的排查步骤:")
            print(f"\n1️⃣ 检查客户端是否上报三方 token")
            print(f"   - 出现「不支持厂商」提示，一般是客户端没有上报三方 token")
            print(f"   - 需要在客户端检查是否已生成厂商 token")
            print(f"   - 确认客户端已集成对应厂商的推送 SDK")
            
            print(f"\n2️⃣ 检查厂商配置是否正确")
            print(f"   - 登录友盟后台 → 【设置】→【应用配置】→【厂商配置】")
            print(f"   - 填写对应厂商的配置信息（华为/小米/OPPO/vivo/荣耀等）")
            print(f"   - 保存后等待 15 分钟再重新发送测试")
            
            print(f"\n3️⃣ 检查标题和内容是否超过厂商限制")
            print(f"   OPPO:")
            print(f"     • 标题：≤50 个字符（中英文及 emoji 均算 1 个字符）")
            print(f"     • 内容：标准样式≤50 字符，长文本≤128 字符，大图≤50 字符")
            print(f"   vivo:")
            print(f"     • 标题：≤40 个字符")
            print(f"     • 内容：≤100 个字符")
            print(f"   小米:")
            print(f"     • 标题：不允许空白，≤50 字符")
            print(f"     • 内容：不允许空白，≤128 字符")
            print(f"   华为/荣耀:")
            print(f"     • 参照小米的标准")
            
            print(f"\n4️⃣ 检查是否厂商超额")
            print(f"   各厂商对营销消息的限制:")
            print(f"   • 华为：新闻类 5 条/日，其他类 2 条/日")
            print(f"   • 小米：未接入公信/私信 1 条，新闻类 8 条，其他类 5 条")
            print(f"   • OPPO：新闻类 5 条，其他类 2 条")
            print(f"   • vivo：新闻类 5 条，其他类 2 条")
            print(f"   • 荣耀：新闻类 5 条，其他类 2 条")
            print(f"   💡 超过限制后，当天后续营销消息只能通过自有通道下发")
            
            print(f"\n5️⃣ 检查 channel_activity 配置")
            print(f"   • API 发送：必须填写 channel_activity 参数")
            print(f"   • 控制台发送：必须勾选「厂商下发参数」")
        
        if has_offline_issue:
            print(f"\n🔍 针对「设备离线」的排查步骤:")
            print(f"\n1️⃣ 确认设备网络状态")
            print(f"   - 检查设备是否连接 WiFi 或移动数据")
            print(f"   - 引导用户打开应用，让设备上线")
            
            print(f"\n2️⃣ 配置厂商通道（重要）")
            print(f"   - 当设备离线时，需要通过厂商通道下发推送")
            print(f"   - 如果 thirdTokens 为空，说明未注册厂商通道")
            print(f"   - 请参考上述「不支持厂商通道」的排查步骤")
            
            print(f"\n3️⃣ 使用测试消息功能")
            print(f"   • 华为：每应用每日可发 500 条测试消息（不受限）")
            print(f"   • 荣耀：每应用每日可发 1000 条测试消息（不受限）")
            print(f"   • vivo：需在 vivo 后台添加测试设备")
            print(f"   • 设置 production_mode=false 即可发送测试消息")
        
        # 提供厂商官方文档链接
        print(f"\n{'='*80}")
        print(f"🔗 各厂商错误码和回执码官方文档:")
        print(f"   • 华为：https://developer.huawei.com/consumer/cn/doc/HMSCore-Guides/message-restriction-description-0000001361648361")
        print(f"   • 小米：https://dev.mi.com/distribute/doc/details?pId=1656")
        print(f"   • OPPO: https://open.oppomobile.com/new/developmentDoc/info?id=13190")
        print(f"   • vivo: https://dev.vivo.com.cn/documentCenter/doc/695")
        print(f"   • 荣耀：https://developer.honor.com/cn/docs/11002/guides/notification-push-standards")
        
        print(f"\n{'='*80}")
        print(f"💡 如需进一步帮助，可提供具体的错误码或截图进行详细分析")
        print(f"{'='*80}")
    else:
        print(f"✅ 未发现明显问题")
    
    print(f"\n{'='*80}")
    print(f"排查完成")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    main()
