#!/usr/bin/env python3
"""
Timestamp Toolkit - Convert between timestamp and datetime formats
"""

import argparse
import json
import sys
from datetime import datetime, timezone
import re

def parse_datetime(input_str: str) -> datetime:
    """Parse datetime from various formats"""
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S.%f",
        "%Y-%m-%dT%H:%M:%S.%fZ",
        "%Y-%m-%d",
        "%Y/%m/%d %H:%M:%S",
        "%Y/%m/%d",
        "%Y年%m月%d日 %H:%M:%S",
        "%Y年%m月%d日",
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(input_str, fmt)
        except ValueError:
            continue
    
    raise ValueError(f"Unable to parse datetime: {input_str}")

def get_now(tz: str = "local", unit: str = "s") -> dict:
    """Get current timestamp"""
    try:
        if tz == "utc":
            now = datetime.now(timezone.utc)
        else:
            now = datetime.now()
        
        timestamp = now.timestamp()
        if unit == "ms":
            timestamp = int(timestamp * 1000)
        else:
            timestamp = int(timestamp)
        
        return {
            "success": True,
            "timestamp": timestamp,
            "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
            "iso": now.isoformat(),
            "unit": unit,
            "timezone": tz
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def to_datetime(input_str: str, tz: str = "local", unit: str = "s") -> dict:
    """Convert timestamp to datetime"""
    try:
        # Parse timestamp
        timestamp = float(input_str)
        
        # Convert milliseconds to seconds if needed
        if unit == "ms":
            timestamp = timestamp / 1000
        
        # Create datetime
        if tz == "utc":
            dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        else:
            dt = datetime.fromtimestamp(timestamp)
        
        return {
            "success": True,
            "timestamp": int(timestamp) if unit == "s" else int(timestamp * 1000),
            "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "iso": dt.isoformat(),
            "date": dt.strftime("%Y-%m-%d"),
            "time": dt.strftime("%H:%M:%S"),
            "unit": unit,
            "timezone": tz
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def to_timestamp(input_str: str, tz: str = "local", unit: str = "s") -> dict:
    """Convert datetime to timestamp"""
    try:
        dt = parse_datetime(input_str)
        
        timestamp = dt.timestamp()
        if unit == "ms":
            timestamp = int(timestamp * 1000)
        else:
            timestamp = int(timestamp)
        
        return {
            "success": True,
            "timestamp": timestamp,
            "datetime": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "unit": unit
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def format_datetime(input_str: str, output_format: str = "%Y-%m-%d %H:%M:%S") -> dict:
    """Format datetime string"""
    try:
        # Try parsing as timestamp first
        try:
            timestamp = float(input_str)
            dt = datetime.fromtimestamp(timestamp)
        except ValueError:
            # Parse as datetime string
            dt = parse_datetime(input_str)
        
        formatted = dt.strftime(output_format)
        
        return {
            "success": True,
            "input": input_str,
            "output": formatted,
            "format": output_format
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def time_diff(input1: str, input2: str = None) -> dict:
    """Calculate time difference"""
    try:
        # Parse first input
        try:
            ts1 = float(input1)
            dt1 = datetime.fromtimestamp(ts1)
        except ValueError:
            dt1 = parse_datetime(input1)
        
        # Parse second input (default to now)
        if input2:
            try:
                ts2 = float(input2)
                dt2 = datetime.fromtimestamp(ts2)
            except ValueError:
                dt2 = parse_datetime(input2)
        else:
            dt2 = datetime.now()
        
        diff = dt2 - dt1
        total_seconds = int(diff.total_seconds())
        
        days = abs(total_seconds) // 86400
        hours = (abs(total_seconds) % 86400) // 3600
        minutes = (abs(total_seconds) % 3600) // 60
        seconds = abs(total_seconds) % 60
        
        direction = "future" if total_seconds < 0 else "past"
        
        # Human readable
        if days > 0:
            human = f"{days}天{hours}小时"
        elif hours > 0:
            human = f"{hours}小时{minutes}分钟"
        elif minutes > 0:
            human = f"{minutes}分钟{seconds}秒"
        else:
            human = f"{seconds}秒"
        
        if direction == "future":
            human = f"{human}后"
        else:
            human = f"{human}前"
        
        return {
            "success": True,
            "datetime1": dt1.strftime("%Y-%m-%d %H:%M:%S"),
            "datetime2": dt2.strftime("%Y-%m-%d %H:%M:%S"),
            "total_seconds": total_seconds,
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
            "direction": direction,
            "human": human
        }
    except Exception as e:
        return {"success": False, "error": str(e)}

def main():
    parser = argparse.ArgumentParser(
        description='Timestamp Toolkit - Convert between timestamp and datetime'
    )
    parser.add_argument(
        'action',
        choices=['now', 'to-datetime', 'to-timestamp', 'format', 'diff'],
        help='Action to perform'
    )
    parser.add_argument(
        '--input', '-i',
        help='Input timestamp or datetime'
    )
    parser.add_argument(
        '--input2', '-i2',
        help='Second input for diff action'
    )
    parser.add_argument(
        '--format', '-f',
        default='%Y-%m-%d %H:%M:%S',
        help='Output format (default: %%Y-%%m-%%d %%H:%%M:%%S)'
    )
    parser.add_argument(
        '--tz',
        default='local',
        help='Timezone (local, utc, or timezone name)'
    )
    parser.add_argument(
        '--unit', '-u',
        choices=['s', 'ms'],
        default='s',
        help='Timestamp unit: s=seconds, ms=milliseconds (default: s)'
    )

    args = parser.parse_args()

    # Execute action
    if args.action == 'now':
        result = get_now(args.tz, args.unit)
    elif args.action == 'to-datetime':
        if not args.input:
            result = {"success": False, "error": "Missing --input parameter"}
        else:
            result = to_datetime(args.input, args.tz, args.unit)
    elif args.action == 'to-timestamp':
        if not args.input:
            result = {"success": False, "error": "Missing --input parameter"}
        else:
            result = to_timestamp(args.input, args.tz, args.unit)
    elif args.action == 'format':
        if not args.input:
            result = {"success": False, "error": "Missing --input parameter"}
        else:
            result = format_datetime(args.input, args.format)
    elif args.action == 'diff':
        if not args.input:
            result = {"success": False, "error": "Missing --input parameter"}
        else:
            result = time_diff(args.input, args.input2)
    else:
        result = {"success": False, "error": f"Unknown action: {args.action}"}

    # Output result
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result.get('success') else 1)

if __name__ == '__main__':
    main()
