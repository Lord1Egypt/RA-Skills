#!/usr/bin/env python3
"""
时间解析 CLI 工具
计算 publishTimeFrom/publishTimeTo 毫秒时间戳

用法:
    python3 parse_time_cli.py
    python3 parse_time_cli.py --from "2026-03-25 00:00:00" --to "2026-03-31 23:59:59"
    python3 parse_time_cli.py --days 7
    python3 parse_time_cli.py --format 1774233538071
"""

import argparse
import sys
import time
from datetime import datetime
from typing import Dict, Any, Optional, Union


# 默认时间范围（7天）
DEFAULT_DAYS = 7


def parse_datetime(dt_str: str) -> int:
    """
    解析日期时间字符串，返回毫秒时间戳
    
    Args:
        dt_str: 日期时间字符串，格式 "yyyy-mm-dd HH:MM:SS" 或 "yyyy-mm-dd"
        
    Returns:
        毫秒时间戳
    """
    if not dt_str:
        return int(time.time() * 1000)
    
    dt_str = dt_str.strip()
    
    # 尝试多种格式
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d %H:%M",
        "%Y/%m/%d",
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(dt_str, fmt)
            return int(dt.timestamp() * 1000)
        except ValueError:
            continue
    
    raise ValueError(f"无法解析日期时间: {dt_str}，请使用格式 'yyyy-mm-dd HH:MM:SS'")


def calculate_publish_time(
    time_from: Optional[Union[str, int]] = None,
    time_to: Optional[Union[str, int]] = None
) -> Dict[str, Any]:
    """
    计算 publishTimeFrom 和 publishTimeTo
    
    Args:
        time_from: 开始时间
            - 字符串格式: "yyyy-mm-dd HH:MM:SS"
            - 整数格式: 毫秒时间戳
            - 不传: 默认为 time_to 往前推7天
        time_to: 结束时间
            - 字符串格式: "yyyy-mm-dd HH:MM:SS"
            - 整数格式: 毫秒时间戳
            - 不传: 默认为当前时间
        
    Returns:
        {
            "publishTimeFrom": 毫秒时间戳,
            "publishTimeTo": 毫秒时间戳
        }
    """
    # 处理结束时间
    if time_to is None:
        publish_time_to = int(time.time() * 1000)
    elif isinstance(time_to, str):
        publish_time_to = parse_datetime(time_to)
    else:
        publish_time_to = int(time_to)
    
    # 处理开始时间
    if time_from is None:
        # 默认往前推7天
        publish_time_from = publish_time_to - (DEFAULT_DAYS * 24 * 60 * 60 * 1000)
    elif isinstance(time_from, str):
        publish_time_from = parse_datetime(time_from)
    else:
        publish_time_from = int(time_from)
    
    return {
        "publishTimeFrom": publish_time_from,
        "publishTimeTo": publish_time_to
    }


def format_timestamp(ts: int) -> str:
    """将毫秒时间戳格式化为日期时间字符串"""
    dt = datetime.fromtimestamp(ts / 1000)
    return dt.strftime("%Y-%m-%d %H:%M:%S")


def main():
    parser = argparse.ArgumentParser(
        description='计算发布时间范围（毫秒时间戳）',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s                                    # 默认最近7天
  %(prog)s --from "2026-03-25 00:00:00"       # 指定开始时间，结束时间为当前
  %(prog)s --to "2026-03-31 23:59:59"         # 指定结束时间，开始时间往前推7天
  %(prog)s --from "2026-03-25" --to "2026-03-31"  # 指定日期范围
  %(prog)s --days 3                         # 最近3天
  %(prog)s --format 1774233538071           # 将毫秒时间戳转为可读格式
        """
    )
    
    parser.add_argument('--from', dest='time_from', help='开始时间 (格式: yyyy-mm-dd HH:MM:SS 或 yyyy-mm-dd)')
    parser.add_argument('--to', dest='time_to', help='结束时间 (格式: yyyy-mm-dd HH:MM:SS 或 yyyy-mm-dd)，默认当前时间')
    parser.add_argument('--days', type=int, help='最近N天（与--from互斥）')
    parser.add_argument('--format', dest='format_ts', help='将毫秒时间戳转为可读格式')
    
    args = parser.parse_args()
    
    # 格式化时间戳模式
    if args.format_ts:
        try:
            ts = int(args.format_ts)
            readable = format_timestamp(ts)
            print(f"毫秒时间戳: {ts}")
            print(f"可读格式: {readable}")
            return
        except ValueError as e:
            print(f"错误: 无效的时间戳 - {e}", file=sys.stderr)
            sys.exit(1)
    
    # 计算时间范围
    try:
        if args.days and not args.time_from:
            # 使用days参数
            if args.time_to:
                time_to = parse_datetime(args.time_to)
            else:
                time_to = int(time.time() * 1000)
            
            time_from = time_to - (args.days * 24 * 60 * 60 * 1000)
            result = {
                "publishTimeFrom": time_from,
                "publishTimeTo": time_to
            }
        else:
            # 使用from/to参数
            result = calculate_publish_time(
                time_from=args.time_from,
                time_to=args.time_to
            )
        
        # 输出结果
        print("{")
        print(f'  "publishTimeFrom": {result["publishTimeFrom"]},')
        print(f'  "publishTimeTo": {result["publishTimeTo"]}')
        print("}")
        print()
        print("时间范围:")
        print(f"  开始: {format_timestamp(result['publishTimeFrom'])}")
        print(f"  结束: {format_timestamp(result['publishTimeTo'])}")
        
    except ValueError as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
