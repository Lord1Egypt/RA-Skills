#!/usr/bin/env python3
"""
TripClaw 行程导入脚本
将行程数据导入到 TripClaw 应用
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from typing import Optional, Dict, Any

# API 配置
API_BASE_URL = "https://api.tripclaws.com"
API_ENDPOINT = "/v1/trips/import"
DEFAULT_TIMEOUT = 30


def get_api_key() -> str:
    """从环境变量获取 API Key"""
    api_key = os.environ.get("TRIPCLAW_API_KEY", "")
    if not api_key:
        print("错误: 未设置 TRIPCLAW_API_KEY 环境变量", file=sys.stderr)
        print("请设置: export TRIPCLAW_API_KEY='your-api-key'", file=sys.stderr)
        sys.exit(1)
    return api_key


def validate_trip_data(data: Dict[str, Any]) -> list:
    """验证行程数据，返回错误列表"""
    errors = []
    
    # 必填字段检查
    if not data.get("name"):
        errors.append("缺少必填字段: name")
    if not data.get("startDate"):
        errors.append("缺少必填字段: startDate")
    if not data.get("endDate"):
        errors.append("缺少必填字段: endDate")
    
    # 途经点检查
    waypoints = data.get("waypoints", [])
    if not waypoints:
        errors.append("waypoints 数组不能为空，至少需要一个途经点")
    else:
        for i, wp in enumerate(waypoints):
            if not wp.get("name"):
                errors.append(f"waypoint[{i}] 缺少 name 字段")
            if not wp.get("type"):
                errors.append(f"waypoint[{i}] 缺少 type 字段")
    
    # 日期格式检查
    import re
    date_pattern = r"^\d{4}-\d{2}-\d{2}$"
    if data.get("startDate") and not re.match(date_pattern, data["startDate"]):
        errors.append("startDate 格式错误，应为 YYYY-MM-DD")
    if data.get("endDate") and not re.match(date_pattern, data["endDate"]):
        errors.append("endDate 格式错误，应为 YYYY-MM-DD")
    
    return errors


def import_trip(api_key: str, trip_data: Dict[str, Any], timeout: int = DEFAULT_TIMEOUT) -> Dict[str, Any]:
    """
    调用 TripClaw API 导入行程
    
    Args:
        api_key: TripClaw API Key
        trip_data: 行程数据字典
        timeout: 请求超时时间（秒）
    
    Returns:
        API 响应数据
    
    Raises:
        Exception: API 调用失败时抛出
    """
    url = f"{API_BASE_URL}{API_ENDPOINT}"
    
    # 构建请求
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    body = json.dumps(trip_data, ensure_ascii=False).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=body,
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            response_data = response.read().decode("utf-8")
            return json.loads(response_data)
    
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else ""
        try:
            error_json = json.loads(error_body)
            error_msg = error_json.get("error", {}).get("message", error_body)
        except json.JSONDecodeError:
            error_msg = error_body or str(e)
        
        raise Exception(f"API 错误 ({e.code}): {error_msg}")
    
    except urllib.error.URLError as e:
        raise Exception(f"网络错误: {e.reason}")
    
    except json.JSONDecodeError as e:
        raise Exception(f"响应解析错误: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="将行程数据导入到 TripClaw",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从文件导入
  python3 import_trip.py --file trip.json
  
  # 从标准输入导入
  cat trip.json | python3 import_trip.py --stdin
  
  # 直接传入 JSON 数据
  python3 import_trip.py --data '{"name":"测试行程",...}'
  
  # 指定 API Key（覆盖环境变量）
  python3 import_trip.py --api-key "your-key" --file trip.json
"""
    )
    
    # 数据输入选项（互斥）
    data_group = parser.add_mutually_exclusive_group(required=True)
    data_group.add_argument(
        "--file", "-f",
        type=str,
        help="行程数据 JSON 文件路径"
    )
    data_group.add_argument(
        "--data", "-d",
        type=str,
        help="直接传入行程 JSON 数据字符串"
    )
    data_group.add_argument(
        "--stdin",
        action="store_true",
        help="从标准输入读取 JSON 数据"
    )
    
    # API Key 选项
    parser.add_argument(
        "--api-key", "-k",
        type=str,
        help="TripClaw API Key（未指定则从 TRIPCLAW_API_KEY 环境变量读取）"
    )
    
    # 其他选项
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"请求超时时间（秒），默认 {DEFAULT_TIMEOUT}"
    )
    
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="仅验证数据格式，不实际导入"
    )
    
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="静默模式，仅输出结果 JSON"
    )
    
    args = parser.parse_args()
    
    # 获取 API Key
    api_key = args.api_key or get_api_key()
    
    # 读取行程数据
    try:
        if args.file:
            with open(args.file, "r", encoding="utf-8") as f:
                trip_data = json.load(f)
        elif args.stdin:
            trip_data = json.load(sys.stdin)
        else:
            trip_data = json.loads(args.data)
    except FileNotFoundError:
        print(f"错误: 文件不存在: {args.file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"错误: JSON 解析失败: {e}", file=sys.stderr)
        sys.exit(1)
    
    # 验证数据
    errors = validate_trip_data(trip_data)
    if errors:
        print("数据验证失败:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        sys.exit(1)
    
    if not args.quiet:
        print(f"行程数据验证通过: {trip_data.get('name', '未命名')}")
    
    # 仅验证模式
    if args.validate_only:
        print("验证成功，未执行导入")
        sys.exit(0)
    
    # 执行导入
    try:
        if not args.quiet:
            print("正在导入到 TripClaw...")
        
        result = import_trip(api_key, trip_data, args.timeout)
        
        # 输出结果
        print(json.dumps(result, ensure_ascii=False, indent=2 if not args.quiet else None))
        
        if result.get("success") and not args.quiet:
            data = result.get("data", {})
            print(f"\n✅ 导入成功!")
            print(f"   行程 ID: {data.get('tripId')}")
            print(f"   途经点数: {data.get('waypointCount')}")
            print(f"   活动数: {data.get('activityCount')}")
            if data.get("shareUrl"):
                print(f"   分享链接: {data.get('shareUrl')}")
        
        sys.exit(0 if result.get("success") else 1)
    
    except Exception as e:
        print(f"导入失败: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()