#!/usr/bin/env python3
"""YZL-AIoT 云智联 AIoT 设备管理交互技能 v1.1.0

基于新版 API (2026-06-15):
  Base: https://open.yzlkj.com
  路径以 /open/ 开头
"""

import json
import os
import sys
import http.client
import time
from datetime import datetime, timedelta
import urllib.request
from urllib.parse import urlencode
from collections import defaultdict

# ============================================================
# 请求频率限制配置（来自新版文档）
# ============================================================
RATE_LIMITS = {
    "device_all": {"max": 10, "window": 10},      # 10次/10秒
    "device_list": {"max": 5, "window": 10},       # 5次/10秒
    "device": {"max": 10, "window": 10},           # 10次/10秒
    "history": {"max": 2, "window": 10},           # 2次/10秒
    "command_send": {"max": 2, "window": 5},       # 2次/5秒
    "command_detail": {"max": 2, "window": 5},     # 2次/5秒
    "command_list": {"max": 2, "window": 10},      # 2次/10秒
    "ping": {"max": 10, "window": 10},             # 10次/10秒
}

# ============================================================
# 版本 & 技能信息
# ============================================================
LOCAL_VERSION = "1.1.0"
SKILL_SLUG = "yzl-aiot"
CLAWHUB_REGISTRY = "https://clawhub.ai"
VERSION_CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".version_cache.json")
VERSION_CACHE_TTL = 12 * 3600


def _get_skill_dir():
    return os.path.dirname(os.path.abspath(__file__))


def _read_meta_version():
    meta_path = os.path.join(_get_skill_dir(), "_meta.json")
    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
        return meta.get("version", LOCAL_VERSION)
    except (FileNotFoundError, json.JSONDecodeError):
        return LOCAL_VERSION


def _load_version_cache():
    try:
        with open(VERSION_CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_version_cache(cache):
    try:
        with open(VERSION_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def _parse_version(ver_str):
    try:
        parts = ver_str.split("-")[0].split(".")
        return tuple(int(p) for p in parts)
    except (ValueError, IndexError):
        return (0, 0, 0)


def check_latest_version(force=False):
    """检查 ClawHub 上是否有新版本。"""
    local_ver = _read_meta_version()
    result = {
        "has_update": False,
        "local_version": local_ver,
        "latest_version": local_ver,
        "latest_all": local_ver,
        "error": None,
        "cached": False,
    }

    if not force:
        cache = _load_version_cache()
        cached_result = cache.get("result")
        cached_at = cache.get("cached_at", 0)
        if cached_result and (time.time() - cached_at) < VERSION_CACHE_TTL:
            cached_result["cached"] = True
            return cached_result

    url = f"{CLAWHUB_REGISTRY}/api/v1/skills/{SKILL_SLUG}"
    try:
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": f"yzl-aiot/{LOCAL_VERSION}"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        tags = data.get("skill", {}).get("tags", {})
        latest_tag = tags.get("latest", "")

        if latest_tag:
            result["latest_all"] = latest_tag
            if any(x in latest_tag.lower() for x in ["test", "beta", "alpha", "rc"]):
                stable_ver = data.get("latestVersion", {}).get("version", latest_tag)
                result["latest_version"] = stable_ver
            else:
                result["latest_version"] = latest_tag
        else:
            stable_ver = data.get("latestVersion", {}).get("version", local_ver)
            result["latest_version"] = stable_ver
            result["latest_all"] = stable_ver

        local_tuple = _parse_version(local_ver)
        remote_tuple = _parse_version(result["latest_version"])
        if remote_tuple > local_tuple:
            result["has_update"] = True

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
        cache = _load_version_cache()
        cached_result = cache.get("result")
        if cached_result:
            cached_result["cached"] = True
            cached_result["error"] = f"网络检查失败({e})，使用上次缓存结果"
            return cached_result

    return result


def format_update_message(version_info):
    if version_info.get("error") and not version_info.get("cached"):
        return ""
    if not version_info.get("has_update"):
        return ""

    local_v = version_info["local_version"]
    latest_v = version_info["latest_version"]
    return (
        f"\n{'=' * 50}\n"
        f"📢 技能版本更新提醒\n"
        f"{'=' * 50}\n"
        f"当前版本: v{local_v}\n"
        f"最新版本: v{latest_v}\n\n"
        f"请使用以下命令更新：\n"
        f"  clawhub update {SKILL_SLUG}\n"
        f"  或: clawhub update {SKILL_SLUG} --version {latest_v}\n"
        f"{'=' * 50}\n"
    )


def cmd_check_update():
    """手动检查版本更新"""
    print(f"📡 正在检查 {SKILL_SLUG} 版本更新...")
    print(f"   本地版本: v{LOCAL_VERSION}")
    version_info = check_latest_version(force=True)
    if version_info.get("error"):
        print(f"\n❌ 检测失败: {version_info['error']}")
        return
    print(f"   远程最新: v{version_info['latest_version']}")
    if version_info.get("has_update"):
        print(f"\n🎉 发现新版本!")
        print(f"   当前: v{version_info['local_version']}")
        print(f"   最新: v{version_info['latest_version']}")
        print(f"\n更新方法：")
        print(f"   clawhub update {SKILL_SLUG}")
    else:
        print(f"\n✅ 已是最新版本")


# ============================================================
# API 基础配置
# ============================================================
request_times = defaultdict(list)


def check_rate_limit(endpoint_key):
    """检查并等待频率限制"""
    now = time.time()
    limit = RATE_LIMITS.get(endpoint_key, {"max": 10, "window": 10})
    request_times[endpoint_key] = [
        t for t in request_times[endpoint_key]
        if now - t < limit["window"]
    ]
    if len(request_times[endpoint_key]) >= limit["max"]:
        oldest = request_times[endpoint_key][0]
        wait_time = limit["window"] - (now - oldest) + 0.1
        if wait_time > 0:
            return wait_time
    request_times[endpoint_key].append(now)
    return 0


API_KEY = os.environ.get("YZLIOT_API_KEY")
BASE_URL = "https://open.yzlkj.com"

# ============================================================
# 新版 API 路径 (2026-06-15 更新)
# 所有路径都以 /open/ 开头
# ============================================================
API_PATHS = {
    "ping": "/open/ping",
    "device_all": "/open/device/all",          # GET /open/device/all
    "device_list": "/open/device/list",         # GET /open/device/list?SkipCount&MaxResultCount&Filter
    "device": "/open/device/",                  # GET /open/device/{id}  (path param)
    "history": "/open/history",                 # GET /open/history?facilityId&StartTime&EndTime&MaxCount
    "command_send": "/open/command/send",       # POST /open/command/send
    "command_list": "/open/command/list",       # GET /open/command/list?DeviceId&SkipCount&MaxResultCount
    "command_detail": "/open/command/",         # GET /open/command/{id}  (path param)
}

# 支持的设备型号前缀（用于 cmd_smart 自动识别）
DEVICE_MODEL_SENSORS = ["YZLSTM1", "STMCBL", "STMCS1"]
DEVICE_MODEL_VALVES = ["WA1CB1", "WANCD1"]
DEVICE_MODEL_LEVEL = ["YZLWP01"]


def make_request(endpoint, method="GET", data=None, rate_key=None, query_params=None):
    """通用 API 请求

    Args:
        endpoint: API 路径（已包含路径参数）
        method: HTTP 方法
        data: POST 请求体 (dict)
        rate_key: 频率限制标识（自动推断）
        query_params: 查询参数字典（用于 GET 请求）
    """
    if not API_KEY:
        return {"error": "请先设置环境变量 YZLIOT_API_KEY"}

    # 确定 rate_key
    if not rate_key:
        if "/device/all" in endpoint:
            rate_key = "device_all"
        elif "/device/list" in endpoint:
            rate_key = "device_list"
        elif "/device/" in endpoint:
            rate_key = "device"
        elif "/history" in endpoint:
            rate_key = "history"
        elif "/command/send" in endpoint:
            rate_key = "command_send"
        elif "/command/list" in endpoint:
            rate_key = "command_list"
        elif "/command/" in endpoint:
            rate_key = "command_detail"
        elif "/ping" in endpoint:
            rate_key = "ping"
        else:
            rate_key = "device_all"

    # 频率限制
    wait_time = check_rate_limit(rate_key)
    if wait_time > 0:
        time.sleep(wait_time)

    # 构建完整路径
    path = endpoint
    if query_params:
        sep = "&" if "?" in path else "?"
        path = f"{path}{sep}{urlencode(query_params)}"

    host = BASE_URL.replace("https://", "").replace("http://", "")
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
        return result
    except Exception as e:
        return {"error": str(e)}


# ============================================================
# 命令函数
# ============================================================

def cmd_ping():
    result = make_request(API_PATHS["ping"])
    if result.get("code") == 0:
        return f"✅ 连接成功！服务器响应: {result.get('data')}"
    return f"❌ 错误: {result}"


def cmd_all():
    """获取所有设备（简易信息，不含设施集）"""
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


def cmd_list(skip=0, max_count=20, filter_text=""):
    """分页获取设备列表（含设施集）"""
    query_params = {"SkipCount": skip, "MaxResultCount": min(max_count, 50)}
    if filter_text:
        query_params["Filter"] = filter_text

    result = make_request(API_PATHS["device_list"], query_params=query_params)
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
    """获取设备详情 — 新版: GET /open/device/{id}"""
    if not device_id:
        return "❌ 请指定设备ID"

    endpoint = f"{API_PATHS['device']}{device_id}"
    result = make_request(endpoint)
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
    """获取设施值历史 — 新版: GET /open/history?facilityId=&StartTime=&EndTime=&MaxCount=

    日期格式: 2026-03-07 00:01:59
    """
    if not facility_id:
        return "❌ 请指定设施ID\n获取方法：先使用 device <设备ID> 查看设备详情，找到对应设施的 id 字段"

    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    start_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
    end_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

    query_params = {
        "facilityId": facility_id,
        "StartTime": start_str,
        "EndTime": end_str,
        "MaxCount": "3000"  # 文档上限 3000
    }

    result = make_request(API_PATHS["history"], query_params=query_params)
    if result.get("code") != 0:
        return f"❌ 错误: {result}"

    data = result.get("data", {})
    values = data.get("values", [])
    if not values:
        return "📭 无历史数据"

    daily = defaultdict(list)
    for v in values:
        day = v['time'][:10]
        try:
            daily[day].append(float(v['value']))
        except (ValueError, TypeError):
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
    """获取设备所有设施的历史数据"""
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

    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    start_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
    end_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

    output = [f"📈 {dev.get('name', device_id)} 近{days}天历史数据", "=" * 50]

    for f in facilities:
        facility_id = f.get("id")
        facility_name = f.get("name", f.get("key", ""))
        if not facility_id:
            continue

        query_params = {
            "facilityId": facility_id,
            "StartTime": start_str,
            "EndTime": end_str,
            "MaxCount": "3000"
        }
        result = make_request(API_PATHS["history"], query_params=query_params)
        if result.get("code") != 0:
            continue

        data = result.get("data", {})
        values = data.get("values", [])
        if not values:
            continue

        daily = defaultdict(list)
        for v in values:
            day = v['time'][:10]
            try:
                daily[day].append(float(v['value']))
            except (ValueError, TypeError):
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
    """发送控制指令（新版 waitTimeout 范围 5~20 秒）"""
    if not device_id:
        return "❌ 请指定设备ID"
    if not cmd_type:
        return "❌ 请指定指令类型"

    try:
        parsed = json.loads(args) if isinstance(args, str) else args
        if isinstance(parsed, dict):
            args_list = [json.dumps(parsed)]
        elif isinstance(parsed, list):
            args_list = parsed
        else:
            args_list = [str(parsed)]
    except json.JSONDecodeError:
        args_list = [args]

    # 限制 waitTimeout 在新版范围内 (5~20)
    wait_timeout = max(5, min(20, wait_timeout))

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
    """获取设备指令列表"""
    if not device_id:
        return "❌ 请指定设备ID"

    query_params = {"DeviceId": device_id, "SkipCount": skip, "MaxResultCount": max_count}
    result = make_request(API_PATHS["command_list"], query_params=query_params)
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
    """获取指令详情 — 新版: GET /open/command/{id}"""
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
    """智能命令 — 根据用户意图自动识别设备并执行操作

    注意: 新版 /open/device/all 返回简易信息（不含设施集），
          如需获取温湿度/开关状态，会走 /open/device/{id} 补查详情。
    """
    result = make_request(API_PATHS["device_all"])
    if result.get("code") != 0:
        return f"❌ 获取设备列表失败: {result}"

    devices = result.get("data", {}).get("items", [])
    if not devices:
        return "📭 未找到设备"

    # 按型号分类
    sensor_devices = []
    valve_devices = []
    level_devices = []

    for dev in devices:
        device_id = dev.get("id", "")
        model_prefix = device_id.split("-")[0] if "-" in device_id else ""
        if model_prefix in DEVICE_MODEL_SENSORS:
            sensor_devices.append(dev)
        elif model_prefix in DEVICE_MODEL_VALVES:
            valve_devices.append(dev)
        elif model_prefix in DEVICE_MODEL_LEVEL:
            level_devices.append(dev)

    action_lower = action.lower() if action else ""

    def _get_device_detail(dev):
        """补查设备详情以获取设施数据"""
        did = dev.get("id")
        if not did:
            return {}
        ep = f"{API_PATHS['device']}{did}"
        r = make_request(ep)
        if r.get("code") == 0:
            return r.get("data", {})
        return {}

    # 意图：获取传感器数据（土壤温湿度）
    if any(k in action for k in ["传感器", "土壤", "湿度", "温度", "查看"]):
        if "液位" in action:
            if not level_devices:
                return "❌ 未找到液位传感器"
            output = ["🌊 液位传感器数据", "=" * 40]
            for dev in level_devices:
                detail = _get_device_detail(dev)
                facilities = detail.get("facilitys", [])
                yw = "-"
                for f in facilities:
                    if f.get("key") == "yw":
                        yw = f.get("value", "-")
                output.append(f"📡 {dev.get('name', '液位传感器')}")
                output.append(f"   状态: {dev.get('status', 'Unknown')} | 液位: {yw}")
            return "\n".join(output)
        else:
            if not sensor_devices:
                return "❌ 未找到土壤温湿度云传感器"
            output = ["🌱 土壤温湿度云传感器", "=" * 40]
            for dev in sensor_devices:
                detail = _get_device_detail(dev)
                facilities = detail.get("facilitys", [])
                wd = sf = "-"
                for f in facilities:
                    key = f.get("key", "")
                    value = f.get("value", "-")
                    if key == "wd":
                        wd = value
                    elif key == "sf":
                        sf = value
                output.append(f"📡 {dev.get('name', '土壤传感器')}")
                output.append(f"   状态: {dev.get('status', 'Unknown')} | 温度: {wd}°C | 湿度: {sf}%")
            return "\n".join(output)

    # 意图：获取液位
    if "液位" in action:
        if not level_devices:
            return "❌ 未找到液位传感器"
        output = ["🌊 液位传感器数据", "=" * 40]
        for dev in level_devices:
            detail = _get_device_detail(dev)
            facilities = detail.get("facilitys", [])
            yw = "-"
            for f in facilities:
                if f.get("key") == "yw":
                    yw = f.get("value", "-")
            output.append(f"📡 {dev.get('name', '液位传感器')}")
            output.append(f"   状态: {dev.get('status', 'Unknown')} | 液位: {yw}")
        return "\n".join(output)

    # 意图：打开电磁阀
    if "开" in action and any(k in action for k in ["电磁阀", "水阀", "阀"]):
        if not valve_devices:
            return "❌ 未找到远程电磁阀设备"
        valve = valve_devices[0]
        device_id = valve.get("id")
        detail = _get_device_detail(valve)
        facilities = detail.get("facilitys", [])
        current_status = "0"
        for f in facilities:
            if f.get("key") == "kk1":
                current_status = f.get("value", "0")
        if current_status == "1":
            return "🚿 远程电磁阀 已处于开启状态"
        result = cmd_send(device_id, "SetFac", [device_id, "kk1", "1"])
        return f"✅ 已开启远程电磁阀" if "✅" in result else f"❌ 开启失败: {result}"

    # 意图：关闭电磁阀
    if "关" in action and any(k in action for k in ["电磁阀", "水阀", "阀"]):
        if not valve_devices:
            return "❌ 未找到远程电磁阀设备"
        valve = valve_devices[0]
        device_id = valve.get("id")
        detail = _get_device_detail(valve)
        facilities = detail.get("facilitys", [])
        current_status = "0"
        for f in facilities:
            if f.get("key") == "kk1":
                current_status = f.get("value", "0")
        if current_status == "0":
            return "🚿 远程电磁阀 已处于关闭状态"
        result = cmd_send(device_id, "SetFac", [device_id, "kk1", "0"])
        return f"✅ 已关闭远程电磁阀" if "✅" in result else f"❌ 关闭失败: {result}"

    return """📖 支持的命令：
  • "获取传感器数据" / "查看传感器" - 获取土壤温湿度数据
  • "获取液位" / "液位数据" - 获取液位传感器数据
  • "打开电磁阀" / "开启水阀" - 开启远程电磁阀
  • "关闭电磁阀" / "关闭水阀" - 关闭远程电磁阀
  • "所有设备" - 查看所有设备"""


def main():
    args = sys.argv[1:]

    # check-update 不需要 API Key
    if args and args[0].lower() == "check-update":
        cmd_check_update()
        return

    if not API_KEY:
        print("❌ 请先设置环境变量 YZLIOT_API_KEY")
        print("")
        print("获取 API Key：")
        print("1. 打开微信小程序「云智联YZL」")
        print("2. 进入「我的」→「开放接口」")
        print("3. 创建或复制您的 API Token")
        print("")
        print("设置方法：")
        print('  export YZLIOT_API_KEY="你的APIKEY"')
        sys.exit(1)

    _update_msg = ""
    version_info = check_latest_version(force=False)
    if version_info.get("has_update"):
        _update_msg = format_update_message(version_info)

    # 不带参数，默认获取所有设备
    if not args:
        print(cmd_all())
        if _update_msg:
            print(_update_msg)
        return

    cmd = args[0].lower()

    # 自然语言命令
    if len(args) == 1 and (any('\u4e00' <= c <= '\u9fff' for c in args[0]) or args[0] in ["传感器", "电磁阀", "水阀", "打开", "关闭"]):
        print(cmd_smart(args[0]))
        if _update_msg:
            print(_update_msg)
        return

    if cmd == "ping":
        print(cmd_ping())
    elif cmd == "all":
        print(cmd_all())
    elif cmd == "list":
        print(cmd_list())
    elif cmd == "device":
        print(cmd_device(args[1] if len(args) > 1 else ""))
    elif cmd == "history":
        print(cmd_history(args[1] if len(args) > 1 else "", int(args[2]) if len(args) > 2 else 5))
    elif cmd == "device-history":
        device_id = args[1] if len(args) > 1 else ""
        days = int(args[2]) if len(args) > 2 else 5
        print(cmd_device_history(device_id, days))
    elif cmd == "send":
        device_id = args[1] if len(args) > 1 else ""
        cmd_type = args[2] if len(args) > 2 else ""
        cmd_args = args[3] if len(args) > 3 else "{}"
        print(cmd_send(device_id, cmd_type, cmd_args))
    elif cmd == "cmd-list":
        print(cmd_command_list(args[1] if len(args) > 1 else ""))
    elif cmd == "cmd-detail":
        print(cmd_command_detail(args[1] if len(args) > 1 else ""))
    else:
        print(f"❌ 未知命令: {cmd}")
        print("命令: ping, all, list, device <ID>, history <设施ID> [天数], device-history <设备ID> [天数], send <设备ID> <类型> [参数], cmd-list <设备ID>, cmd-detail <指令ID>, check-update")

    if _update_msg:
        print(_update_msg)


if __name__ == "__main__":
    main()
