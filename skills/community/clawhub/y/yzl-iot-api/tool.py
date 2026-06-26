#!/usr/bin/env python3
"""云智联 IoT 设备管理工具"""

import json
import os
import sys
import http.client
import time
from datetime import datetime, timedelta
import urllib.request
from urllib.parse import urlencode
from collections import defaultdict

# 请求频率限制配置
RATE_LIMITS = {
    "device_all": {"max": 10, "window": 10},      # 10次/10秒
    "device_list": {"max": 5, "window": 10},    # 5次/10秒
    "device": {"max": 10, "window": 10},         # 10次/10秒
    "history": {"max": 2, "window": 10},         # 2次/10秒
    "command_send": {"max": 2, "window": 5},      # 2次/5秒
    "command_detail": {"max": 2, "window": 5},    # 2次/5秒
    "command_list": {"max": 2, "window": 10},     # 2次/10秒
    "ping": {"max": 10, "window": 10},           # 10次/10秒
}

# ============================================================
# 版本自动更新检测（v1.5.0+）
# ============================================================

# 当前本地版本
LOCAL_VERSION = "1.5.0"

# 技能 slug（与 ClawHub 注册表一致）
SKILL_SLUG = "yzl-iot-api"

# ============================================================
# 停止维护通知 — 引导用户迁移到 YZL-AIoT
# ============================================================

DEPRECATION_NOTICE = (
    "\n"
    f"{'!' * 50}\n"
    f"⛔ yzl-iot-api 已停止维护\n"
    f"{'!' * 50}\n"
    f"此版本 (v{LOCAL_VERSION}) 为 yzl-iot-api 最终版。\n"
    f"后续将不再更新和维护。\n"
    f"\n"
    f"🚚 请迁移至新技能 YZL-AIoT，功能更强，持续更新：\n"
    f"   clawhub install yzl-aiot\n"
    f"\n"
    f"安装后卸载旧技能：\n"
    f"   clawhub uninstall yzl-iot-api\n"
    f"{'!' * 50}\n"
)

# ClawHub Registry API（无需登录即可查询公开技能信息）
CLAWHUB_REGISTRY = "https://clawhub.ai"

# 版本检测缓存文件（避免每次调用都请求网络）
VERSION_CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".version_cache.json")

# 缓存有效期（秒）：默认 12 小时
VERSION_CACHE_TTL = 12 * 3600


def _get_skill_dir():
    """获取当前技能目录"""
    return os.path.dirname(os.path.abspath(__file__))


def _read_meta_version():
    """从 _meta.json 读取本地版本号"""
    meta_path = os.path.join(_get_skill_dir(), "_meta.json")
    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        return meta.get("version", LOCAL_VERSION)
    except (FileNotFoundError, json.JSONDecodeError):
        return LOCAL_VERSION


def _load_version_cache():
    """读取版本检测缓存"""
    try:
        with open(VERSION_CACHE_FILE, "r", encoding="utf-8") as f:
            cache = json.load(f)
        return cache
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_version_cache(cache):
    """写入版本检测缓存"""
    try:
        with open(VERSION_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass  # 缓存写入失败不阻塞主流程


def _parse_version(ver_str):
    """将版本号字符串解析为可比较的元组，如 '1.4.0' -> (1, 4, 0)"""
    try:
        # 去除 - 后面的后缀（如 1.4.1-testpublish 视为 1.4.1）
        parts = ver_str.split("-")[0].split(".")
        return tuple(int(p) for p in parts)
    except (ValueError, IndexError):
        return (0, 0, 0)


def check_latest_version(force=False):
    """
    检查 ClawHub 上是否有新版本。
    
    Args:
        force: 是否强制忽略缓存重新检查
    
    Returns:
        dict: {
            "has_update": bool,
            "local_version": str,
            "latest_version": str,
            "latest_all": str,
            "error": str | None,
            "cached": bool
        }
    """
    local_ver = _read_meta_version()
    result = {
        "has_update": False,
        "local_version": local_ver,
        "latest_version": local_ver,
        "latest_all": local_ver,
        "error": None,
        "cached": False,
    }

    # 检查缓存（除非 force=True）
    if not force:
        cache = _load_version_cache()
        cached_result = cache.get("result")
        cached_at = cache.get("cached_at", 0)
        if cached_result and (time.time() - cached_at) < VERSION_CACHE_TTL:
            cached_result["cached"] = True
            return cached_result

    # 查询 ClawHub registry API
    url = f"{CLAWHUB_REGISTRY}/api/v1/skills/{SKILL_SLUG}"
    try:
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": "yzl-iot-api/1.5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        # 从 tags 中获取 latest 标签对应的版本
        tags = data.get("skill", {}).get("tags", {})
        latest_tag = tags.get("latest", "")
        
        if latest_tag:
            result["latest_all"] = latest_tag
            # 如果 latest 标签含 test/beta/alpha，则尝试寻找其他稳定版
            if any(x in latest_tag.lower() for x in ["test", "beta", "alpha", "rc"]):
                stable_ver = data.get("latestVersion", {}).get("version", latest_tag)
                result["latest_version"] = stable_ver
            else:
                result["latest_version"] = latest_tag
        else:
            stable_ver = data.get("latestVersion", {}).get("version", local_ver)
            result["latest_version"] = stable_ver
            result["latest_all"] = stable_ver

        # 比较版本号
        local_tuple = _parse_version(local_ver)
        remote_tuple = _parse_version(result["latest_version"])
        
        if remote_tuple > local_tuple:
            result["has_update"] = True

        # 写入缓存
        _save_version_cache({
            "result": {
                "has_update": result["has_update"],
                "local_version": local_ver,
                "latest_version": result["latest_version"],
                "latest_all": result["latest_all"],
                "error": None,
                "cached": False,
            },
            "cached_at": time.time()
        })

    except Exception as e:
        result["error"] = str(e)
        # 有错误时尝试使用已有的缓存
        cache = _load_version_cache()
        cached_result = cache.get("result")
        if cached_result:
            cached_result["cached"] = True
            cached_result["error"] = f"网络检查失败({e})，使用上次缓存结果"
            return cached_result

    return result


def format_update_message(version_info):
    """格式化版本更新提醒消息"""
    if version_info.get("error") and not version_info.get("cached"):
        return ""  # 无法检测时静默处理
    
    if not version_info.get("has_update"):
        return ""
    
    local_v = version_info["local_version"]
    latest_v = version_info["latest_version"]
    
    msg = (
        f"\n"
        f"{'=' * 50}\n"
        f"📢 技能版本更新提醒\n"
        f"{'=' * 50}\n"
        f"当前版本: v{local_v}\n"
        f"最新版本: v{latest_v}\n"
        f"\n"
        f"⚠️ 注意：yzl-iot-api 已停止维护\n"
        f"请迁移至 YZL-AIoT：\n"
        f"  clawhub install yzl-aiot\n"
        f"{'=' * 50}\n"
    )
    return msg


def cmd_check_update():
    """手动检查版本更新"""
    print(f"📡 正在检查 {SKILL_SLUG} 版本更新...")
    print(f"   本地版本: v{LOCAL_VERSION}")
    
    version_info = check_latest_version(force=True)
    
    if version_info.get("error"):
        print(f"\n❌ 检测失败: {version_info['error']}")
    else:
        print(f"   远程最新: v{version_info['latest_version']}")
    
    print(DEPRECATION_NOTICE)


# ============================================================
# 请求频率限制
# ============================================================

request_times = defaultdict(list)

def check_rate_limit(endpoint_key):
    """检查并等待频率限制
    
    Args:
        endpoint_key: 接口标识（如 device_all, command_send 等）
    
    Returns:
        需要等待的秒数（如果需要）
    """
    now = time.time()
    limit = RATE_LIMITS.get(endpoint_key, {"max": 10, "window": 10})
    
    # 清理过期的记录
    request_times[endpoint_key] = [
        t for t in request_times[endpoint_key] 
        if now - t < limit["window"]
    ]
    
    # 检查是否超过限制
    if len(request_times[endpoint_key]) >= limit["max"]:
        oldest = request_times[endpoint_key][0]
        wait_time = limit["window"] - (now - oldest) + 0.1
        if wait_time > 0:
            return wait_time
    
    # 记录本次请求时间
    request_times[endpoint_key].append(now)
    return 0

API_KEY = os.environ.get("YZLIOT_API_KEY")
BASE_URL = "https://open.yzlkj.com"

# 支持的设备（便于快速引用）
KNOWN_DEVICES = {
    "土壤温湿度云传感器": "YZLSTM1-0000001454",
    "远程电磁阀": "WA1CB1-0000000007",
}

API_PATHS = {
    "ping": "/openv1/ping",
    "device_all": "/openv1/deviceList",  # 正确路径
    "device_list": "/openv1/deviceList",
    "device": "/openv1/device?id=",
    "history": "/openv1/history",
    "command_send": "/open/command/send",  # POST 方式
    "command_list": "/openv1/command/list",
    "command_detail": "/openv1/command/detail",
}

def make_request(endpoint, method="GET", data=None, rate_key=None):
    if not API_KEY:
        return {"error": "请先设置环境变量 YZLIOT_API_KEY"}
    
    # 根据 endpoint 自动确定 rate_key
    if not rate_key:
        if "device/all" in endpoint or "deviceList" in endpoint:
            rate_key = "device_all" if "device/all" in endpoint else "device_list"
        elif "device?id=" in endpoint:
            rate_key = "device"
        elif "history" in endpoint:
            rate_key = "history"
        elif "command/send" in endpoint:
            rate_key = "command_send"
        elif "command/detail" in endpoint:
            rate_key = "command_detail"
        elif "command/list" in endpoint:
            rate_key = "command_list"
        elif "ping" in endpoint:
            rate_key = "ping"
        else:
            rate_key = "device_all"  # 默认
    
    # 检查频率限制
    wait_time = check_rate_limit(rate_key)
    if wait_time > 0:
        # 自动等待
        time.sleep(wait_time)
    
    # 提取路径和查询参数
    if "?" in endpoint:
        path, query = endpoint.split("?", 1)
        path = f"{path}?{query}"
    else:
        path = endpoint
    
    # 移除 BASE_URL 中的协议
    host = BASE_URL.replace("https://", "").replace("http://", "")
    
    # 使用 dict 格式的 headers
    headers = {
        "YZLIOT-APIKEY": API_KEY,
        "Content-Type": "application/json"
    }
    
    body = json.dumps(data) if data else None
    
    try:
        conn = http.client.HTTPSConnection(host, timeout=15)
        conn.request(method, path, body, headers)
        response = conn.getresponse()
        result = json.loads(response.read().decode("utf-8"))
        conn.close()
        
        # 遇到频率限制(429)或权限问题(403)时返回错误，由调用者决定是否重试
        return result
    except Exception as e:
        return {"error": str(e)}

def cmd_ping():
    result = make_request(API_PATHS["ping"])
    if result.get("code") == 0:
        return f"✅ 连接成功！服务器响应: {result.get('data')}"
    return f"❌ 错误: {result}"

def cmd_all():
    result = make_request(API_PATHS["device_all"])
    if result.get("code") != 0:
        return f"❌ 错误: {result}"
    
    items = result.get("data", {}).get("items", [])
    if not items:
        return "📭 未找到设备"
    
    output = [f"📋 设备列表 (共 {len(items)} 台)"]
    for i, dev in enumerate(items, 1):
        output.append(f"{i}. {dev.get('name', 'N/A')} - {dev.get('status', 'N/A')}")
    return "\n".join(output)

def cmd_list(skip=0, max_count=20):
    params = {"SkipCount": skip, "MaxResultCount": max_count}
    endpoint = API_PATHS["device_list"] + "?" + urlencode(params)
    result = make_request(endpoint)
    
    if result.get("code") != 0:
        return f"❌ 错误: {result}"
    
    items = result.get("data", {}).get("items", [])
    total = result.get("data", {}).get("totalCount", 0)
    
    if not items:
        return "📭 未找到设备"
    
    output = [f"📋 设备列表 (共 {total} 台)"]
    for i, dev in enumerate(items, 1):
        output.append(f"{i}. {dev.get('name', 'N/A')} - {dev.get('status', 'N/A')}")
    return "\n".join(output)

def cmd_device(device_id):
    if not device_id:
        return "❌ 请指定设备ID"
    
    endpoint = f"{API_PATHS['device']}{device_id}"
    result = make_request(endpoint, method="GET")
    
    if result.get("code") != 0:
        return f"❌ 错误: {result}"
    
    dev = result.get("data", {})
    output = [f"📱 {dev.get('name', 'N/A')}", f"状态: {dev.get('status', 'N/A')}"]
    
    facilities = dev.get("facilitys", [])
    if facilities:
        output.append("📊 设施数据:")
        for f in facilities:
            output.append(f"  • {f.get('key', 'N/A')}: {f.get('value', 'N/A')}")
    
    return "\n".join(output)

def cmd_history(facility_id, days=5):
    """获取历史数据
    
    Args:
        facility_id: 设施ID（从 device 命令的设施数据中获取，key 为 id 字段）
        days: 查询天数（默认5天）
    """
    if not facility_id:
        return "❌ 请指定设施ID\n获取方法：先使用 device <设备ID> 查看设备详情，找到对应设施的 id 字段"
    
    # 计算时间范围
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    start_str = start_time.strftime('%Y-%m-%dT%H:%M:%S')
    end_str = end_time.strftime('%Y-%m-%dT%H:%M:%S')
    
    # GET + Body 方式 (facilityId 在 query 参数中)
    body = {
        "startTime": start_str,
        "endTime": end_str,
        "maxCount": 500
    }
    
    # facilityId 作为 query 参数
    endpoint = f"{API_PATHS['history']}?facilityId={facility_id}"
    result = make_request(endpoint, method="GET", data=body)
    
    if result.get("code") != 0:
        return f"❌ 错误: {result}"
    
    data = result.get("data", {})
    if "statusCode" in data:
        return f"❌ API错误: statusCode={data.get('statusCode')}"
    
    values = data.get("values", [])
    if not values:
        return "📭 无历史数据"
    
    # 按日期分组统计
    from collections import defaultdict
    daily = defaultdict(list)
    for v in values:
        day = v['time'][:10]
        try:
            daily[day].append(float(v['value']))
        except:
            pass
    
    output = [f"📈 历史数据 (共 {len(values)} 条，近{days}天)", "=" * 40]
    
    for day in sorted(daily.keys()):
        nums = daily[day]
        avg = sum(nums) / len(nums)
        min_v = min(nums)
        max_v = max(nums)
        output.append(f"{day}: 最低{min_v:.1f} / 平均{avg:.1f} / 最高{max_v:.1f} ({len(nums)}条)")
    
    return "\n".join(output)

def cmd_device_history(device_id, days=5):
    """获取设备所有设施的历史数据
    
    Args:
        device_id: 设备ID
        days: 查询天数（默认5天）
    """
    if not device_id:
        return "❌ 请指定设备ID"
    
    # 先获取设备详情
    endpoint = f"{API_PATHS['device']}{device_id}"
    result = make_request(endpoint)
    
    if result.get("code") != 0:
        return f"❌ 获取设备详情失败: {result}"
    
    dev = result.get("data", {})
    facilities = dev.get("facilitys", [])
    
    if not facilities:
        return "❌ 该设备没有设施数据"
    
    # 计算时间范围
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    start_str = start_time.strftime('%Y-%m-%dT%H:%M:%S')
    end_str = end_time.strftime('%Y-%m-%dT%H:%M:%S')
    
    body = {
        "startTime": start_str,
        "endTime": end_str,
        "maxCount": 500
    }
    
    output = [f"📈 {dev.get('name', device_id)} 近{days}天历史数据", "=" * 50]
    
    # 获取每个设施的历史数据
    for f in facilities:
        facility_id = f.get("id")
        facility_name = f.get("name", f.get("key", ""))
        
        if not facility_id:
            continue
        
        endpoint = f"{API_PATHS['history']}?facilityId={facility_id}"
        result = make_request(endpoint, method="GET", data=body)
        
        if result.get("code") != 0:
            continue
        
        data = result.get("data", {})
        values = data.get("values", [])
        
        if not values:
            continue
        
        # 统计
        from collections import defaultdict
        daily = defaultdict(list)
        for v in values:
            day = v['time'][:10]
            try:
                daily[day].append(float(v['value']))
            except:
                pass
        
        if daily:
            output.append(f"\n📊 {facility_name}:")
            for day in sorted(daily.keys()):
                nums = daily[day]
                avg = sum(nums) / len(nums)
                min_v = min(nums)
                max_v = max(nums)
                output.append(f"  {day}: {min_v:.1f} ~ {avg:.1f} ~ {max_v:.1f}")
    
    return "\n".join(output)

def cmd_send(device_id, cmd_type, args="{}", wait_confirm=True, wait_timeout=10):
    """发送控制指令
    
    Args:
        device_id: 设备ID
        cmd_type: 指令类型 (GetFac/SetFac/Upfs/Custom)
        args: 指令参数 (JSON 字符串或数组)
        wait_confirm: 是否等待确认
        wait_timeout: 等待超时时间(秒)
    """
    if not device_id:
        return "❌ 请指定设备ID"
    if not cmd_type:
        return "❌ 请指定指令类型"
    
    # args 可以是数组或对象
    try:
        if isinstance(args, str):
            # 尝试解析为JSON
            parsed = json.loads(args)
            # 如果是对象，转为数组格式
            if isinstance(parsed, dict):
                args_list = [json.dumps(parsed)]  # 转为 ["{\"key\":\"value\"}"]
            elif isinstance(parsed, list):
                args_list = parsed
            else:
                args_list = [str(parsed)]
        else:
            args_list = args
    except json.JSONDecodeError:
        # 如果不是JSON，直接作为字符串
        args_list = [args]
    
    body = {
        "deviceId": device_id,
        "type": cmd_type,
        "args": args_list,
        "waitConfirm": wait_confirm,
        "waitTimeout": wait_timeout
    }
    
    result = make_request(API_PATHS["command_send"], method="POST", data=body)
    
    if result.get("code") != 0:
        return f"❌ 发送失败: {result}"
    
    data = result.get("data", {})
    return f"✅ 指令已发送: {json.dumps(data, ensure_ascii=False)}"

def cmd_command_list(device_id, skip=0, max_count=20):
    """获取设备支持的指令列表
    
    Args:
        device_id: 设备ID
        skip: 跳过数量
        max_count: 最大数量
    """
    if not device_id:
        return "❌ 请指定设备ID"
    
    # 注意：文档显示是 DeviceId (大写D)
    params = {"DeviceId": device_id, "SkipCount": skip, "MaxResultCount": max_count}
    endpoint = API_PATHS["command_list"] + "?" + urlencode(params)
    result = make_request(endpoint)
    
    if result.get("code") != 0:
        return f"❌ 获取失败: {result}"
    
    items = result.get("data", {}).get("items", [])
    total = result.get("data", {}).get("totalCount", 0)
    
    if not items:
        return "📭 暂无指令记录"
    
    output = [f"📋 指令列表 (共 {total} 条)"]
    for i, cmd in enumerate(items, 1):
        output.append(f"{i}. {cmd.get('type', 'N/A')} | 状态: {cmd.get('status', 'N/A')}")
        output.append(f"   时间: {cmd.get('creationTime', 'N/A')}")
    
    return "\n".join(output)

def cmd_command_detail(command_id):
    """获取指令详情
    
    Args:
        command_id: 指令ID
    """
    if not command_id:
        return "❌ 请指定指令ID"
    
    endpoint = f"{API_PATHS['command_detail']}{command_id}"
    result = make_request(endpoint)
    
    if result.get("code") != 0:
        return f"❌ 获取失败: {result}"
    
    cmd = result.get("data", {})
    output = [f"📋 指令详情", "=" * 40]
    output.append(f"ID: {cmd.get('id', 'N/A')}")
    output.append(f"设备ID: {cmd.get('deviceId', 'N/A')}")
    output.append(f"类型: {cmd.get('type', 'N/A')}")
    output.append(f"状态: {cmd.get('status', 'N/A')}")
    output.append(f"创建时间: {cmd.get('creationTime', 'N/A')}")
    
    args = cmd.get('args', [])
    if args:
        output.append(f"参数: {args}")
    
    return "\n".join(output)

def cmd_smart(action=""):
    """智能命令 - 根据用户意图自动识别设备并执行操作
    
    Args:
        action: 用户意图（如"获取传感器数据"、"打开电磁阀"等）
    """
    # 获取设备列表
    result = make_request(API_PATHS["device_all"])
    if result.get("code") != 0:
        return f"❌ 获取设备列表失败: {result}"
    
    devices = result.get("data", {}).get("items", [])
    if not devices:
        return "📭 未找到设备"
    
    # 按型号分类设备
    # 土壤温湿度云传感器: YZLSTM1, STMCBL, STMCS1
    sensor_devices = []
    # 远程电磁阀: WA1CB1, WANCD1
    valve_devices = []
    # 低功耗液位传感器: YZLWP01
    level_devices = []
    
    for dev in devices:
        device_id = dev.get("id", "")
        model_prefix = device_id.split("-")[0] if "-" in device_id else ""
        
        if model_prefix in ["YZLSTM1", "STMCBL", "STMCS1"]:
            sensor_devices.append(dev)
        elif model_prefix in ["WA1CB1", "WANCD1"]:
            valve_devices.append(dev)
        elif model_prefix == "YZLWP01":
            level_devices.append(dev)
    
    # 解析用户意图
    action_lower = action.lower() if action else ""
    
    # 意图：获取传感器数据（土壤温湿度）
    if "传感器" in action or "土壤" in action or "湿度" in action or "温度" in action or "查看" in action:
        if "液位" in action:
            # 液位传感器
            if not level_devices:
                return "❌ 未找到液位传感器"
            
            output = ["🌊 液位传感器数据", "=" * 40]
            for dev in level_devices:
                name = dev.get("name", dev.get("id"))
                status = dev.get("status", "Unknown")
                facilities = dev.get("facilitys", [])
                
                # 获取液位数据 (key: yw)
                yw = "-"
                for f in facilities:
                    key = f.get("key", "")
                    value = f.get("value", "-")
                    if key == "yw":
                        yw = value
                
                output.append(f"📡 液位传感器")
                output.append(f"   状态: {status} | 液位: {yw}")
            
            return "\n".join(output)
        else:
            # 土壤温湿度传感器
            if not sensor_devices:
                return "❌ 未找到土壤温湿度云传感器"
            
            output = ["🌱 土壤温湿度云传感器", "=" * 40]
            for dev in sensor_devices:
                name = dev.get("name", dev.get("id"))
                status = dev.get("status", "Unknown")
                facilities = dev.get("facilitys", [])
                
                # 获取温湿度 (key: wd=温度, sf=湿度)
                wd = sf = "-"
                for f in facilities:
                    key = f.get("key", "")
                    value = f.get("value", "-")
                    if key == "wd":
                        wd = value
                    elif key == "sf":
                        sf = value
                
                output.append(f"📡 土壤温湿度云传感器")
                output.append(f"   状态: {status} | 温度: {wd}°C | 湿度: {sf}%")
            
            return "\n".join(output)
    
    # 意图：获取液位数据
    if "液位" in action:
        if not level_devices:
            return "❌ 未找到液位传感器"
        
        output = ["🌊 液位传感器数据", "=" * 40]
        for dev in level_devices:
            name = dev.get("name", dev.get("id"))
            status = dev.get("status", "Unknown")
            facilities = dev.get("facilitys", [])
            
            # 获取液位数据 (key: yw)
            yw = "-"
            for f in facilities:
                key = f.get("key", "")
                value = f.get("value", "-")
                if key == "yw":
                    yw = value
            
            output.append(f"📡 液位传感器")
            output.append(f"   状态: {status} | 液位: {yw}")
        
        return "\n".join(output)
    
    # 意图：打开/开启电磁阀
    elif "开" in action and ("电磁阀" in action or "水阀" in action or "阀" in action):
        if not valve_devices:
            return "❌ 未找到远程电磁阀设备"
        
        valve = valve_devices[0]
        device_id = valve.get("id")
        
        # 获取当前状态
        facilities = valve.get("facilitys", [])
        current_status = "0"
        for f in facilities:
            if f.get("key") == "kk1":
                current_status = f.get("value", "0")
        
        if current_status == "1":
            return f"🚿 远程电磁阀 已处于开启状态"
        
        # 发送开启指令
        result = cmd_send(device_id, "SetFac", [device_id, "kk1", "1"])
        if "✅" in result:
            return f"✅ 已开启远程电磁阀"
        else:
            return f"❌ 开启失败: {result}"
    
    # 意图：关闭电磁阀
    elif "关" in action and ("电磁阀" in action or "水阀" in action or "阀" in action):
        if not valve_devices:
            return "❌ 未找到远程电磁阀设备"
        
        valve = valve_devices[0]
        device_id = valve.get("id")
        
        # 获取当前状态
        facilities = valve.get("facilitys", [])
        current_status = "0"
        for f in facilities:
            if f.get("key") == "kk1":
                current_status = f.get("value", "0")
        
        if current_status == "0":
            return f"🚿 远程电磁阀 已处于关闭状态"
        
        # 发送关闭指令
        result = cmd_send(device_id, "SetFac", [device_id, "kk1", "0"])
        if "✅" in result:
            return f"✅ 已关闭远程电磁阀"
        else:
            return f"❌ 关闭失败: {result}"
    
    # 无法识别意图，显示帮助
    return """📖 支持的命令：
  • "获取传感器数据" / "查看传感器" - 获取土壤温湿度数据
  • "获取液位" / "液位数据" - 获取液位传感器数据
  • "打开电磁阀" / "开启水阀" - 开启远程电磁阀
  • "关闭电磁阀" / "关闭水阀" - 关闭远程电磁阀
  • "所有设备" - 查看所有设备"""


def main():
    args = sys.argv[1:]
    
    # check-update 不需要 API Key，单独处理
    if args and args[0].lower() == "check-update":
        cmd_check_update()
        return
    
    if not API_KEY:
        print("❌ 请先设置环境变量 YZLIOT_API_KEY")
        print("")
        print("获取 API Key：")
        print("1. 打开微信小程序「云智联YZL」")
        print("2. 进入「我的」→「开放接口」")
        print("3. 复制您的 API Token")
        print("")
        print("设置方法：")
        print('  export YZLIOT_API_KEY="您的API密钥"')
        sys.exit(1)
    
    args = sys.argv[1:]
    
    # 不带参数时，默认获取所有设备数据
    if not args:
        print(cmd_all())
        _version_checked = True
        if _update_msg:
            print(_update_msg)
        print(DEPRECATION_NOTICE)
        return
    
    cmd = args[0].lower()
    
    # 处理自然语言命令（仅当第一个参数是中文或特定关键词时）
    if len(args) == 1 and (any('\u4e00' <= c <= '\u9fff' for c in args[0]) or args[0] in ["传感器", "电磁阀", "水阀", "打开", "关闭"]):
        print(cmd_smart(args[0]))
        _version_checked = True
        if _update_msg:
            print(_update_msg)
        print(DEPRECATION_NOTICE)
        return
    
    if cmd == "ping":
        print(cmd_ping())
        _version_checked = True
    elif cmd == "all":
        print(cmd_all())
        _version_checked = True
    elif cmd == "list":
        print(cmd_list())
        _version_checked = True
    elif cmd == "device":
        print(cmd_device(args[1] if len(args) > 1 else ""))
        _version_checked = True
    elif cmd == "history":
        print(cmd_history(args[1] if len(args) > 1 else "", int(args[2]) if len(args) > 2 else 5))
        _version_checked = True
    elif cmd == "device-history":
        # device-history <设备ID> [天数]
        device_id = args[1] if len(args) > 1 else ""
        days = int(args[2]) if len(args) > 2 else 5
        print(cmd_device_history(device_id, days))
        _version_checked = True
    elif cmd == "send":
        # send <设备ID> <指令类型> [参数]
        device_id = args[1] if len(args) > 1 else ""
        cmd_type = args[2] if len(args) > 2 else ""
        cmd_args = args[3] if len(args) > 3 else "{}"
        print(cmd_send(device_id, cmd_type, cmd_args))
        _version_checked = True
    elif cmd == "cmd-list":
        # cmd-list <设备ID>
        print(cmd_command_list(args[1] if len(args) > 1 else ""))
        _version_checked = True
    elif cmd == "cmd-detail":
        # cmd-detail <指令ID>
        print(cmd_command_detail(args[1] if len(args) > 1 else ""))
        _version_checked = True
    else:
        print(f"❌ 未知命令: {cmd}")
        print("命令: ping, all, list, device <ID>, history <设施ID> [天数], device-history <设备ID> [天数], send <设备ID> <类型> [参数], cmd-list <设备ID>, cmd-detail <指令ID>, check-update")
    
    # 执行后输出版本更新提醒（排除已单独处理的 check-update）
    if _version_checked:
        if _update_msg:
            print(_update_msg)
        # 停止维护通知（check-update 已单独显示）
        print(DEPRECATION_NOTICE)


if __name__ == "__main__":
    # 启动时静默检测版本更新
    _version_checked = False
    _update_msg = ""
    version_info = check_latest_version(force=False)
    if version_info.get("has_update"):
        _update_msg = format_update_message(version_info)
    main()