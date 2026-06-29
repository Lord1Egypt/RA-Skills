import argparse
import json
import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional, Tuple

# mPaaS MGS 网关配置
BASE_URL = "https://cn-hangzhou-mgs-gw.cloud.alipay.com/mgw.htm"
MGS_HEADERS = {
    "Content-Type": "application/json",
    "workspaceId": "prod",
    "AppId": "ALIPUB3C84031111512",
}

# Operation-Type
OP_TYPE_LIST = "com.alipay.ekytsaas.skill.device.list"
OP_TYPE_QUERY = "com.alipay.ekytsaas.skill.device.query"
OP_TYPE_TRIP_LIST = "com.alipay.ekytsaas.skill.device.tripList"

# 轨迹查询约束
MAX_QUERY_DAYS = 30
DEFAULT_QUERY_DAYS = 7

# 配置文件路径（与脚本同级的 ../config.json）
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json")


def load_config(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def read_config_from_default() -> Optional[Dict[str, Any]]:
    if os.path.exists(CONFIG_PATH):
        return load_config(CONFIG_PATH)
    return None


def save_config_to_default(cfg: Dict[str, Any]) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)


def resolve_api_key(cfg: Dict[str, Any], arg_api_key: Optional[str]) -> Optional[str]:
    if arg_api_key:
        return arg_api_key
    env_key = os.getenv("API_KEY")
    if env_key:
        return env_key
    cfg_key = cfg.get("apiKey") if isinstance(cfg, dict) else None
    if cfg_key:
        return cfg_key
    return None


def build_mgs_body(params: Dict[str, Any]) -> bytes:
    """构建 mPaaS MGS 网关请求体，外层用 _requestBody 包裹，整体为数组格式"""
    payload = [{"_requestBody": params}]
    return json.dumps(payload).encode("utf-8")


def http_request(
    method: str,
    url: str,
    headers: Dict[str, str],
    params: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    data = build_mgs_body(params) if params is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw_body = resp.read().decode("utf-8")
            if not raw_body:
                raise RuntimeError(f"Empty response from server (HTTP {resp.status})")
            try:
                return json.loads(raw_body)
            except json.JSONDecodeError as e:
                raise RuntimeError(f"Invalid JSON response: {raw_body[:500]}") from e
    except urllib.error.HTTPError as err:
        body = ""
        try:
            body = err.read().decode("utf-8")
        except Exception:
            pass
        raise RuntimeError(f"HTTP {err.code}: {body}") from err


def call_api(operation_type: str, params: Dict[str, Any]) -> Any:
    """调用 mPaaS MGS 网关接口"""
    headers = dict(MGS_HEADERS)
    headers["Operation-Type"] = operation_type
    result = http_request("POST", BASE_URL, headers=headers, params=params)

    if not result.get("success", False):
        code = result.get("resultCode", "UNKNOWN")
        msg = result.get("resultMessage", "No message")
        raise RuntimeError(f"API error: [{code}] {msg}")

    return result.get("data")


def list_devices(api_key: str) -> List[Dict[str, Any]]:
    """查询绑定的车辆列表"""
    return call_api(OP_TYPE_LIST, {"apiKey": api_key}) or []


def get_device_info(api_key: str, tuid: str) -> Dict[str, Any]:
    """查询车辆实时数据"""
    return call_api(OP_TYPE_QUERY, {"apiKey": api_key, "tuid": tuid}) or {}


def list_trips(api_key: str, tuid: str, start_time: int, end_time: int) -> Dict[str, Any]:
    """查询车辆历史骑行轨迹（单天）"""
    return call_api(OP_TYPE_TRIP_LIST, {
        "apiKey": api_key,
        "tuid": tuid,
        "startTime": start_time,
        "endTime": end_time,
    }) or {}


def split_time_range_by_day(start_ts: int, end_ts: int) -> List[Tuple[int, int]]:
    """将毫秒时间戳范围按天拆分，每天的 startTime 为当天 00:00:00.000，endTime 为次日 00:00:00.000

    Args:
        start_ts: 起始毫秒时间戳
        end_ts: 结束毫秒时间戳

    Returns:
        按天拆分的 [(day_start_ms, day_end_ms), ...] 列表
    """
    tz_cn = timezone(timedelta(hours=8))
    start_dt = datetime.fromtimestamp(start_ts / 1000, tz=tz_cn)
    end_dt = datetime.fromtimestamp(end_ts / 1000, tz=tz_cn)

    # 对齐到天的起始
    day_start = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    day_end = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    if day_end < end_dt:
        day_end += timedelta(days=1)

    ranges = []
    current = day_start
    while current < day_end:
        next_day = current + timedelta(days=1)
        ranges.append((
            int(current.timestamp() * 1000),
            int(next_day.timestamp() * 1000),
        ))
        current = next_day
    return ranges


def list_trips_concurrent(
    api_key: str, tuid: str, start_time: int, end_time: int
) -> Dict[str, Any]:
    """并发查询车辆历史骑行轨迹，按天拆分后并发请求，汇总结果

    Args:
        api_key: API Key
        tuid: 车辆中控号
        start_time: 起始毫秒时间戳
        end_time: 结束毫秒时间戳

    Returns:
        汇总后的 {"trips": [...], "totalCount": N}
    """
    day_ranges = split_time_range_by_day(start_time, end_time)
    all_trips = []

    def query_one(day_range: Tuple[int, int]) -> List[Dict[str, Any]]:
        day_start, day_end = day_range
        try:
            data = list_trips(api_key, tuid, day_start, day_end)
            return data.get("trips", [])
        except RuntimeError:
            return []

    with ThreadPoolExecutor(max_workers=min(len(day_ranges), 8)) as executor:
        futures = {executor.submit(query_one, r): r for r in day_ranges}
        for future in as_completed(futures):
            try:
                trips = future.result()
                all_trips.extend(trips)
            except Exception:
                pass

    # 按 startTime 排序
    all_trips.sort(key=lambda t: t.get("startTime", 0))
    return {"trips": all_trips, "totalCount": len(all_trips)}


def main():
    parser = argparse.ArgumentParser(description="极酷电动车查询工具")
    parser.add_argument("--api-key", default=None, help="API Key (sk_live_xxx)")
    parser.add_argument("--device-name", default=None, help="车辆名称（模糊匹配）")
    parser.add_argument("--device-tuid", default=None, help="车辆中控号 (TUID)")
    parser.add_argument("--start-time", type=int, default=None, help="轨迹查询开始时间（Unix时间戳，秒）")
    parser.add_argument("--end-time", type=int, default=None, help="轨迹查询结束时间（Unix时间戳，秒）")
    parser.add_argument("--days", type=int, default=DEFAULT_QUERY_DAYS,
                        help=f"查询最近N天的轨迹（默认{DEFAULT_QUERY_DAYS}天，最大{MAX_QUERY_DAYS}天）")
    parser.add_argument("--no-trips", action="store_true", help="仅查询车辆实时数据，不查询轨迹")
    args = parser.parse_args()

    # 加载配置
    cfg = {}
    cfg_from_default = read_config_from_default()
    if cfg_from_default:
        cfg.update(cfg_from_default)

    # 解析 API Key
    api_key = resolve_api_key(cfg, args.api_key)
    if not api_key:
        print(json.dumps({"error": "Missing API key. Set API_KEY or provide --api-key or config.json"}, ensure_ascii=False))
        sys.exit(2)

    # 保存解析后的 API Key 到配置
    cfg["apiKey"] = api_key
    save_config_to_default(cfg)

    # 查询车辆列表
    try:
        devices = list_devices(api_key)
    except RuntimeError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)

    if not devices:
        print(json.dumps({"error": "No devices found"}, ensure_ascii=False))
        sys.exit(2)

    # 选择车辆
    selected = None
    if args.device_tuid:
        for d in devices:
            if str(d.get("tuid")) == args.device_tuid:
                selected = d
                break
    elif args.device_name:
        for d in devices:
            name = d.get("model") or d.get("deviceName") or ""
            if args.device_name in name:
                selected = d
                break
    else:
        # 多设备时返回列表供选择
        if len(devices) > 1:
            print(json.dumps({"choose_device": devices}, ensure_ascii=False))
            sys.exit(3)
        selected = devices[0]

    if not selected:
        print(json.dumps({"error": "Device not found", "devices": devices}, ensure_ascii=False))
        sys.exit(4)

    tuid = str(selected.get("tuid"))

    # 查询车辆实时数据
    try:
        info = get_device_info(api_key, tuid)
    except RuntimeError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)

    # 合并列表信息和实时数据
    output = {
        "tuid": tuid,
        "model": selected.get("model"),
        "color": selected.get("color"),
        "frameNo": selected.get("frameNo"),
        "barCode": selected.get("barCode"),
        "location": info.get("location"),
        "locationAddress": info.get("locationAddress"),
        "runningStatus": info.get("runningStatus"),
        "speed": info.get("speed"),
        "powerStatus": info.get("powerStatus"),
        "rsrp": info.get("rsrp"),
        "locss": info.get("locss"),
        "totalMileage": info.get("totalMileage"),
        "batteryLevel": info.get("batteryLevel"),
        "enduranceMileage": info.get("enduranceMileage"),
        "lastLocationTime": info.get("lastLocationTime"),
    }

    # 查询历史轨迹
    if not args.no_trips:
        try:
            if args.start_time and args.end_time:
                # 用户显式指定了时间范围（秒级时间戳）
                start_ms = args.start_time * 1000
                end_ms = args.end_time * 1000
            else:
                # 默认查询最近 N 天
                days = min(args.days, MAX_QUERY_DAYS)
                tz_cn = timezone(timedelta(hours=8))
                now = datetime.now(tz=tz_cn)
                end_dt = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
                start_dt = end_dt - timedelta(days=days)
                start_ms = int(start_dt.timestamp() * 1000)
                end_ms = int(end_dt.timestamp() * 1000)

            trips_data = list_trips_concurrent(api_key, tuid, start_ms, end_ms)
            output["trips"] = trips_data.get("trips", [])
            output["tripCount"] = trips_data.get("totalCount", 0)
        except RuntimeError as e:
            print(json.dumps({"error": str(e)}, ensure_ascii=False))
            sys.exit(1)

    print(json.dumps(output, ensure_ascii=False))


if __name__ == "__main__":
    main()