#!/usr/bin/env python3
"""YZL-AIoT 云智联 AIoT 设备管理交互技能 v1.2.1

基于云智联开放接口（Open API v2，官方文档更新 2026-07-25）:
  Base: https://open.yzlkj.com
  路径以 /open/ 开头

⚠️ 重要：请求方必须确保请求频率低于平台限速，并保证并发不超过 2。
   同一 IP 在短时间内频繁返回非 0 状态码（400/401/403/429 等）会被平台
   判定为异常请求并【永久封禁该 IP】。本工具内置：
     - 按接口排队限速（请求前自动等待）
     - 不做任何自动重试（避免重试风暴）
     - 连续多次非 0 响应自动中止（降低封 IP 风险）

# ============================================================
# 请求频率限制配置（来自官方《使用说明》2026-07-25）
# ============================================================
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
# 请求频率限制配置（来自官方《使用说明》2026-07-25）
# 并发限制: 2（同一 APIKEY 同时最多 2 个请求在途）
# ============================================================
RATE_LIMITS = {
    "device_all": {"max": 10, "window": 10},       # 10次/10秒
    "device_list": {"max": 5, "window": 10},        # 5次/10秒
    "device": {"max": 10, "window": 10},            # 10次/10秒
    "history": {"max": 6, "window": 30},            # 6次/30秒
    "command_send": {"max": 2, "window": 5},        # 2次/5秒
    "command_detail": {"max": 2, "window": 5},      # 2次/5秒
    "command_list": {"max": 2, "window": 10},       # 2次/10秒
    "ping": {"max": 10, "window": 10},              # 10次/10秒
}

# 连续非 0 状态码保护上限：超过后自动中止，避免持续触发平台风控（封 IP）
MAX_CONSECUTIVE_ERRORS = 5

# ============================================================
# 版本 & 技能信息
# ============================================================
LOCAL_VERSION = "1.2.1"
SKILL_SLUG = "yzl-aiot"
CLAWHUB_REGISTRY = "https://clawhub.ai"
VERSION_CACHE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".version_cache.json")
VERSION_CACHE_TTL = 12 * 3600

DEVICE_STATUS_LABELS = {
    "Online": "在线",
    "Offline": "离线",
    "Standby": "待机",
    "Hibernate": "休眠",
}

COMMAND_STATUS_LABELS = {
    "Pending": "等待中",
    "Sent": "已发送",
    "Failed": "失败",
    "Completed": "已完成",
    "Cancelled": "已取消",
    "Rejected": "已拒绝",
    "Outtime": "超时",
    "Outcount": "超次数",
}

SAFETY_TIP = (
    "⚠️ 频率限制提醒：请确保请求频率低于平台限速（并发 ≤2）。\n"
    "   同一 IP 短时间内频繁返回非 0 状态码会被永久封禁，\n"
    "   失败请使用指数退避（1s/2s/4s…）重试，切勿高频重试。"
)


def _ensure_utf8_stdio():
    """Windows 控制台默认 GBK，输出 emoji/中文可能报 UnicodeEncodeError。

    统一将 stdout/stderr 切换为 UTF-8（失败时忽略），保证跨平台可运行。
    """
    for name in ("stdout", "stderr"):
        stream = getattr(sys, name, None)
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


_ensure_utf8_stdio()


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
_consecutive_errors = 0


def wait_for_rate_limit(endpoint_key):
    """按接口限速排队，返回实际等待秒数。

    注意：必须在请求【之前】调用，确保不会超过平台阈值。
    """
    limit = RATE_LIMITS.get(endpoint_key, {"max": 10, "window": 10})
    window, max_calls = limit["window"], limit["max"]
    total_wait = 0.0
    while True:
        now = time.time()
        recent = [t for t in request_times[endpoint_key] if now - t < window]
        request_times[endpoint_key] = recent
        if len(recent) < max_calls:
            request_times[endpoint_key].append(time.time())
            return total_wait
        wait = window - (now - recent[0]) + 0.05
        if wait <= 0:
            continue
        print(f"⏳ 本地限速等待 {wait:.1f} 秒（{endpoint_key}: {max_calls}次/{window}秒，避免触发封 IP 策略）",
              file=sys.stderr)
        time.sleep(wait)
        total_wait += wait


def _infer_rate_key(endpoint):
    if "/device/all" in endpoint:
        return "device_all"
    if "/device/list" in endpoint:
        return "device_list"
    if "/device/" in endpoint:
        return "device"
    if "/history" in endpoint:
        return "history"
    if "/command/send" in endpoint:
        return "command_send"
    if "/command/list" in endpoint:
        return "command_list"
    if "/command/" in endpoint:
        return "command_detail"
    if "/ping" in endpoint:
        return "ping"
    return "device_all"


def _track_api_result(result):
    """统计非 0 状态码；连续错误过多时中止，避免被封 IP。"""
    global _consecutive_errors
    code = result.get("code")
    if "error" in result or (code is not None and code != 0):
        _consecutive_errors += 1
    else:
        _consecutive_errors = 0
        return result

    if code == 429:
        print("🚫 平台返回 429：请求频率已超限！请降低调用频率，"
              "继续高频请求将触发封 IP 策略。", file=sys.stderr)
    elif code in (401, 403):
        print("🔑 认证/权限异常（%s）：请检查 YZLIOT_API_KEY 是否有效、是否有该设备权限。"
              "大量 401 会触发平台封 IP 策略。" % code, file=sys.stderr)

    if _consecutive_errors >= MAX_CONSECUTIVE_ERRORS:
        print(f"\n🛑 已连续 {_consecutive_errors} 次请求返回异常，自动中止本次运行。", file=sys.stderr)
        print(SAFETY_TIP, file=sys.stderr)
        sys.exit(2)
    return result


API_KEY = os.environ.get("YZLIOT_API_KEY")
BASE_URL = "https://open.yzlkj.com"

# ============================================================
# 新版 API 路径 (v2)
# 所有路径都以 /open/ 开头
# ============================================================
API_PATHS = {
    "ping": "/open/ping",
    "device_all": "/open/device/all",          # GET ?PollingTag=
    "device_list": "/open/device/list",         # GET ?SkipCount&MaxResultCount&Filter
    "device": "/open/device/",                  # GET /open/device/{id}  (path param)
    "history": "/open/history",                 # GET ?facilityId&StartTime&EndTime&MaxCount
    "command_send": "/open/command/send",       # POST
    "command_list": "/open/command/list",       # GET ?DeviceId&SkipCount&MaxResultCount
    "command_detail": "/open/command/",         # GET /open/command/{id}  (path param)
}

# 平台参数上限（来自官方文档）
MAX_DEVICE_LIST_PAGE = 200       # /open/device/list 的 MaxResultCount 上限
MAX_HISTORY_COUNT = 3000         # /open/history 的 MaxCount 上限
MAX_COMMAND_ARGS = 5             # /open/command/send 的 args 最多 5 个
WAIT_TIMEOUT_MIN, WAIT_TIMEOUT_MAX = 5, 20

# 支持的设备型号前缀（用于 cmd_smart 自动识别）
DEVICE_MODEL_SENSORS = ["YZLSTM1", "STMCBL", "STMCS1"]
DEVICE_MODEL_VALVES = ["WA1CB1", "WANCD1"]
DEVICE_MODEL_LEVEL = ["YZLWP01"]


def make_request(endpoint, method="GET", data=None, rate_key=None, query_params=None):
    """通用 API 请求（内置按接口限速，不做自动重试）

    Args:
        endpoint: API 路径（已包含路径参数）
        method: HTTP 方法
        data: POST 请求体 (dict)
        rate_key: 频率限制标识（自动推断）
        query_params: 查询参数字典（用于 GET 请求）
    """
    if not API_KEY:
        return {"error": "请先设置环境变量 YZLIOT_API_KEY"}

    if not rate_key:
        rate_key = _infer_rate_key(endpoint)

    # 请求前按限速排队
    wait_for_rate_limit(rate_key)

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
        raw = response.read().decode("utf-8")
        conn.close()
        try:
            result = json.loads(raw)
        except json.JSONDecodeError:
            return {"error": f"响应不是 JSON (HTTP {response.status}): {raw[:200]}"}
        return _track_api_result(result)
    except Exception as e:
        return _track_api_result({"error": str(e)})


# ============================================================
# 命令函数
# ============================================================

def cmd_ping():
    result = make_request(API_PATHS["ping"])
    if result.get("code") == 0:
        return f"✅ 连接成功！服务器响应: {result.get('data')}"
    return f"❌ 错误: {result}"


def _fmt_device_status(status):
    if not status:
        return "未知"
    return DEVICE_STATUS_LABELS.get(status, status)


def cmd_all(polling_tag=""):
    """获取所有设备（简易信息，不含设施集）"""
    query_params = {}
    if polling_tag:
        query_params["PollingTag"] = polling_tag

    result = make_request(API_PATHS["device_all"], query_params=query_params or None)
    if result.get("code") != 0:
        return f"❌ 错误: {result}"

    items = result.get("data", {}).get("items", [])
    if not items:
        return "📭 未找到设备"

    output = [f"📋 设备列表 (共 {len(items)} 台)"]
    for i, dev in enumerate(items, 1):
        name = dev.get("name") or "N/A"
        status = _fmt_device_status(dev.get("status"))
        model = dev.get("model") or "-"
        updated = dev.get("latestModificationTime") or "-"
        output.append(f"{i}. {name} [{model}] - {status} (最后修改: {updated})")
    return "\n".join(output)


def cmd_list(skip=0, max_count=20, filter_text=""):
    """分页获取设备列表（含设施集），单页上限 200"""
    max_count = int(max_count)
    max_count = max(1, min(max_count, MAX_DEVICE_LIST_PAGE))

    query_params = {"SkipCount": int(skip), "MaxResultCount": max_count}
    if filter_text:
        query_params["Filter"] = filter_text

    result = make_request(API_PATHS["device_list"], query_params=query_params)
    if result.get("code") != 0:
        return f"❌ 错误: {result}"

    items = result.get("data", {}).get("items", [])
    total = result.get("data", {}).get("totalCount", 0)

    if not items:
        return "📭 未找到设备"

    output = [f"📋 设备列表 (共 {total} 台，本页 {len(items)} 台)"]
    for i, dev in enumerate(items, 1):
        name = dev.get("name") or "N/A"
        status = _fmt_device_status(dev.get("status"))
        model = dev.get("model") or "-"
        facilities = dev.get("facilitys") or []
        keys = ", ".join(f.get("key", "") for f in facilities) or "-"
        output.append(f"{i}. {name} [{model}] - {status}")
        output.append(f"   设施: {keys}")
    return "\n".join(output)


def cmd_device(device_id):
    """获取设备详情 — GET /open/device/{id}"""
    if not device_id:
        return "❌ 请指定设备ID"

    endpoint = f"{API_PATHS['device']}{device_id}"
    result = make_request(endpoint)
    if result.get("code") != 0:
        return f"❌ 错误: {result}"

    dev = result.get("data", {})
    output = [
        f"📱 {dev.get('name', 'N/A')}",
        f"型号: {dev.get('model', 'N/A')} | 状态: {_fmt_device_status(dev.get('status'))}",
        f"最后修改: {dev.get('latestModificationTime', 'N/A')}",
    ]
    if dev.get("latestStatusTime"):
        output.append(f"最后状态时间: {dev.get('latestStatusTime')}")

    facilities = dev.get("facilitys", [])
    if facilities:
        output.append("📊 设施数据:")
        for f in facilities:
            output.append(f"  • {f.get('name', f.get('key', 'N/A'))} ({f.get('key', 'N/A')}): "
                          f"{f.get('value', 'N/A')} [{f.get('valueType', '')}]")
    else:
        output.append("📊 无设施数据")

    return "\n".join(output)


def _history_query(facility_id, days):
    end_time = datetime.now()
    start_time = end_time - timedelta(days=days)
    return {
        "facilityId": facility_id,
        "StartTime": start_time.strftime('%Y-%m-%d %H:%M:%S'),
        "EndTime": end_time.strftime('%Y-%m-%d %H:%M:%S'),
        "MaxCount": str(MAX_HISTORY_COUNT),
    }


def _daily_summary(values):
    """把 values 按天聚合为 (day, 最低, 平均, 最高, 条数)。"""
    daily = defaultdict(list)
    for v in values:
        t = v.get('time') or ""
        day = t[:10]
        try:
            daily[day].append(float(v.get('value')))
        except (ValueError, TypeError):
            pass
    rows = []
    for day in sorted(daily.keys()):
        nums = daily[day]
        rows.append((day, min(nums), sum(nums) / len(nums), max(nums), len(nums)))
    return rows


def cmd_history(facility_id, days=5):
    """获取设施值历史 — GET /open/history?facilityId=&StartTime=&EndTime=&MaxCount=

    日期格式: 2026-03-07 00:01:59
    """
    if not facility_id:
        return ("❌ 请指定设施ID\n"
                "获取方法：先使用 device <设备ID> 查看设备详情，找到对应设施的 id 字段")

    result = make_request(API_PATHS["history"], query_params=_history_query(facility_id, days))
    if result.get("code") != 0:
        return f"❌ 错误: {result}"

    data = result.get("data", {})
    values = data.get("values", [])
    if not values:
        return "📭 无历史数据"

    output = [f"📈 历史数据 (近{days}天，实际 {data.get('actual', len(values))}/{data.get('total', len(values))} 条)",
              "=" * 40]
    for day, min_v, avg, max_v, cnt in _daily_summary(values):
        output.append(f"{day}: 最低{min_v:.1f} / 平均{avg:.1f} / 最高{max_v:.1f} ({cnt}条)")

    return "\n".join(output)


def cmd_device_history(device_id, days=5):
    """获取设备所有设施的历史数据（注意：每个设施一次 /open/history 请求，受 6次/30秒 限制）"""
    if not device_id:
        return "❌ 请指定设备ID"

    endpoint = f"{API_PATHS['device']}{device_id}"
    result = make_request(endpoint)
    if result.get("code") != 0:
        return f"❌ 获取设备详情失败: {result}"

    dev = result.get("data", {})
    facilities = dev.get("facilitys", [])
    if not facilities:
        return "❌ 该设备没有设施数据"

    output = [f"📈 {dev.get('name', device_id)} 近{days}天历史数据", "=" * 50]

    for f in facilities:
        facility_id = f.get("id")
        facility_name = f.get("name", f.get("key", ""))
        if not facility_id:
            continue

        result = make_request(API_PATHS["history"], query_params=_history_query(facility_id, days))
        if result.get("code") != 0:
            continue

        values = result.get("data", {}).get("values", [])
        if not values:
            continue

        rows = _daily_summary(values)
        if rows:
            output.append(f"\n📊 {facility_name}:")
            for day, min_v, avg, max_v, cnt in rows:
                output.append(f"  {day}: {min_v:.1f} ~ {avg:.1f} ~ {max_v:.1f} ({cnt}条)")

    return "\n".join(output)


def _parse_args_list(args):
    try:
        parsed = json.loads(args) if isinstance(args, str) else args
        if isinstance(parsed, dict):
            return [json.dumps(parsed)]
        if isinstance(parsed, list):
            return [str(x) for x in parsed]
        return [str(parsed)]
    except json.JSONDecodeError:
        return [args]


def cmd_send(device_id, cmd_type, args="[]", wait_confirm=True, wait_timeout=10):
    """发送控制指令（args 最多 5 个；waitTimeout 范围 5~20 秒）"""
    if not device_id:
        return "❌ 请指定设备ID"
    if not cmd_type:
        return "❌ 请指定指令类型（SetFac / GetFac / Upfs / Custom）"

    args_list = _parse_args_list(args)
    if len(args_list) > MAX_COMMAND_ARGS:
        return (f"❌ 参数过多：args 最多 {MAX_COMMAND_ARGS} 个（当前 {len(args_list)} 个），"
                "平台会直接返回 400")

    wait_timeout = max(WAIT_TIMEOUT_MIN, min(WAIT_TIMEOUT_MAX, int(wait_timeout)))

    body = {
        "deviceId": device_id,
        "type": cmd_type,
        "args": args_list,
        "waitConfirm": bool(wait_confirm),
        "waitTimeout": wait_timeout
    }

    result = make_request(API_PATHS["command_send"], method="POST", data=body)
    if result.get("code") != 0:
        return f"❌ 发送失败: {result}"

    data = result.get("data", {}) or {}
    status = data.get("status")
    status_label = COMMAND_STATUS_LABELS.get(status, status) if status else "未知"
    return (f"✅ 指令已发送: commandId={data.get('commandId')}, "
            f"status={status}({status_label})")


def cmd_command_list(device_id, skip=0, max_count=20):
    """获取设备指令列表"""
    if not device_id:
        return "❌ 请指定设备ID"

    query_params = {"DeviceId": device_id, "SkipCount": int(skip), "MaxResultCount": int(max_count)}
    result = make_request(API_PATHS["command_list"], query_params=query_params)
    if result.get("code") != 0:
        return f"❌ 获取失败: {result}"

    items = result.get("data", {}).get("items", [])
    total = result.get("data", {}).get("totalCount", 0)
    if not items:
        return "📭 暂无指令记录"

    output = [f"📋 指令列表 (共 {total} 条)"]
    for i, cmd in enumerate(items, 1):
        status = cmd.get('status', 'N/A')
        output.append(f"{i}. {cmd.get('type', 'N/A')} | 状态: {status}"
                      f"({COMMAND_STATUS_LABELS.get(status, '')})")
        output.append(f"   时间: {cmd.get('creationTime', 'N/A')}")

    return "\n".join(output)


def cmd_command_detail(command_id):
    """获取指令详情 — GET /open/command/{id}"""
    if not command_id:
        return "❌ 请指定指令ID"

    endpoint = f"{API_PATHS['command_detail']}{command_id}"
    result = make_request(endpoint)
    if result.get("code") != 0:
        return f"❌ 获取失败: {result}"

    cmd = result.get("data", {})
    status = cmd.get('status', 'N/A')
    output = [f"📋 指令详情", "=" * 40]
    output.append(f"ID: {cmd.get('id', 'N/A')}")
    output.append(f"设备ID: {cmd.get('deviceId', 'N/A')}")
    output.append(f"类型: {cmd.get('type', 'N/A')}")
    output.append(f"状态: {status} ({COMMAND_STATUS_LABELS.get(status, '')})")
    output.append(f"创建时间: {cmd.get('creationTime', 'N/A')}")
    args = cmd.get('args', [])
    if args:
        output.append(f"参数: {args}")

    return "\n".join(output)


def cmd_smart(action=""):
    """智能命令 — 根据用户意图自动识别设备并执行操作

    注意: /open/device/all 返回简易信息（不含设施集），
          需要温湿度/开关状态时会走 /open/device/{id} 补查详情。
    """
    result = make_request(API_PATHS["device_all"])
    if result.get("code") != 0:
        return f"❌ 获取设备列表失败: {result}"

    devices = result.get("data", {}).get("items", [])
    if not devices:
        return "📭 未找到设备"

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

    def _get_device_detail(dev):
        """补查设备详情以获取设施数据"""
        did = dev.get("id")
        if not did:
            return {}
        r = make_request(f"{API_PATHS['device']}{did}")
        if r.get("code") == 0:
            return r.get("data", {})
        return {}

    def _facility_value(detail, key):
        for f in detail.get("facilitys", []):
            if f.get("key") == key:
                return f.get("value", "-")
        return "-"

    # 意图：获取液位
    if "液位" in action:
        if not level_devices:
            return "❌ 未找到液位传感器"
        output = ["🌊 液位传感器数据", "=" * 40]
        for dev in level_devices:
            detail = _get_device_detail(dev)
            output.append(f"📡 {dev.get('name', '液位传感器')}")
            output.append(f"   状态: {_fmt_device_status(dev.get('status'))} | "
                          f"液位: {_facility_value(detail, 'yw')}")
        return "\n".join(output)

    # 意图：获取传感器数据（土壤温湿度）
    if any(k in action for k in ["传感器", "土壤", "湿度", "温度", "查看"]):
        if not sensor_devices:
            return "❌ 未找到土壤温湿度云传感器"
        output = ["🌱 土壤温湿度云传感器", "=" * 40]
        for dev in sensor_devices:
            detail = _get_device_detail(dev)
            output.append(f"📡 {dev.get('name', '土壤传感器')}")
            output.append(f"   状态: {_fmt_device_status(dev.get('status'))} | "
                          f"温度: {_facility_value(detail, 'wd')}°C | "
                          f"湿度: {_facility_value(detail, 'sf')}%")
        return "\n".join(output)

    # 意图：打开电磁阀
    if "开" in action and any(k in action for k in ["电磁阀", "水阀", "阀"]):
        if not valve_devices:
            return "❌ 未找到远程电磁阀设备"
        valve = valve_devices[0]
        device_id = valve.get("id")
        detail = _get_device_detail(valve)
        if _facility_value(detail, "kk1") == "1":
            return "🚿 远程电磁阀 已处于开启状态"
        r = cmd_send(device_id, "SetFac", [device_id, "kk1", "1"])
        return "✅ 已开启远程电磁阀" if "✅" in r else f"❌ 开启失败: {r}"

    # 意图：关闭电磁阀
    if "关" in action and any(k in action for k in ["电磁阀", "水阀", "阀"]):
        if not valve_devices:
            return "❌ 未找到远程电磁阀设备"
        valve = valve_devices[0]
        device_id = valve.get("id")
        detail = _get_device_detail(valve)
        if _facility_value(detail, "kk1") == "0":
            return "🚿 远程电磁阀 已处于关闭状态"
        r = cmd_send(device_id, "SetFac", [device_id, "kk1", "0"])
        return "✅ 已关闭远程电磁阀" if "✅" in r else f"❌ 关闭失败: {r}"

    return """📖 支持的命令：
  • "获取传感器数据" / "查看传感器" - 获取土壤温湿度数据
  • "获取液位" / "液位数据" - 获取液位传感器数据
  • "打开电磁阀" / "开启水阀" - 开启远程电磁阀
  • "关闭电磁阀" / "关闭水阀" - 关闭远程电磁阀
  • "所有设备" - 查看所有设备"""


def print_help():
    print(f"""YZL-AIoT 云智联设备管理 v{LOCAL_VERSION}

用法:
  python tool.py <命令> [参数]
  （若环境只有 python3，把 python 换成 python3，如 python3 tool.py help）

命令:
  ping                              测试连接
  all [--tag 轮询标记]               获取所有设备（简易信息，不含设施集）
  list [跳过] [单页数量] [筛选词]     分页获取设备列表（含设施集，单页上限 200）
  device <设备ID>                    获取设备详情
  history <设施ID> [天数]            获取设施值历史（默认 5 天，单次上限 3000 条）
  device-history <设备ID> [天数]     获取设备全部设施的历史数据
  send <设备ID> <类型> [参数JSON]     发送指令（类型: SetFac/GetFac/Upfs/Custom）
  cmd-list <设备ID> [跳过] [数量]     获取设备指令列表
  cmd-detail <指令ID>                获取指令详情
  check-update                      检查技能版本更新
  help                              显示本帮助

示例:
  python tool.py all
  python tool.py list 0 50 水阀
  python tool.py device WANCD1-0000000001
  python tool.py history <设施ID> 3
  python tool.py send WANCD1-0000000001 SetFac '["WANCD1-0000000001","kk1","1"]'

⚠️ 频率限制（并发 ≤2，务必低于限速，否则有封 IP 风险）:
  /open/device/all      10次/10秒      /open/device/list      5次/10秒
  /open/device/{{id}}     10次/10秒      /open/history          6次/30秒
  /open/command/send     2次/5秒        /open/command/{{id}}     2次/5秒
  /open/command/list     2次/10秒
""")


def _need_api_key():
    if API_KEY:
        return False
    print("❌ 请先设置环境变量 YZLIOT_API_KEY")
    print("")
    print("获取 API Key：")
    print("1. 打开微信小程序「云智联YZL」")
    print("2. 进入「我的」→「开放接口」")
    print("3. 创建或复制您的 API Token")
    print("")
    print("设置方法：")
    print('  export YZLIOT_API_KEY="你的APIKEY"')
    return True


def main():
    args = sys.argv[1:]

    # check-update / help 不需要 API Key
    if args and args[0].lower() in ("check-update",):
        cmd_check_update()
        return
    if args and args[0].lower() in ("help", "-h", "--help"):
        print_help()
        return

    if _need_api_key():
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
    if len(args) == 1 and (any('\u4e00' <= c <= '\u9fff' for c in args[0])
                           or args[0] in ["传感器", "电磁阀", "水阀", "打开", "关闭"]):
        print(cmd_smart(args[0]))
        if _update_msg:
            print(_update_msg)
        return

    try:
        if cmd == "ping":
            print(cmd_ping())
        elif cmd == "all":
            tag = ""
            if len(args) > 2 and args[1] in ("--tag", "-t"):
                tag = args[2]
            elif len(args) > 1 and not args[1].startswith("-"):
                tag = args[1]
            print(cmd_all(tag))
        elif cmd == "list":
            skip = int(args[1]) if len(args) > 1 else 0
            max_count = int(args[2]) if len(args) > 2 else 20
            filter_text = args[3] if len(args) > 3 else ""
            print(cmd_list(skip, max_count, filter_text))
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
            cmd_args = args[3] if len(args) > 3 else "[]"
            print(cmd_send(device_id, cmd_type, cmd_args))
        elif cmd == "cmd-list":
            print(cmd_command_list(args[1] if len(args) > 1 else "",
                                   int(args[2]) if len(args) > 2 else 0,
                                   int(args[3]) if len(args) > 3 else 20))
        elif cmd == "cmd-detail":
            print(cmd_command_detail(args[1] if len(args) > 1 else ""))
        else:
            print(f"❌ 未知命令: {cmd}")
            print_help()
    except (ValueError, TypeError) as e:
        print(f"❌ 参数错误: {e}")
        print_help()

    if _update_msg:
        print(_update_msg)


if __name__ == "__main__":
    main()
