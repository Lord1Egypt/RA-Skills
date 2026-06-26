#!/usr/bin/env python3
"""Timestamp Tool - Unix timestamp converter."""

import argparse
import datetime
import sys
import time


def parse_offset(offset_str: str) -> datetime.timedelta:
    """Parse offset string like '1 day', '2 hours'."""
    parts = offset_str.strip().split()
    if len(parts) != 2:
        raise ValueError("Invalid offset format. Use: '1 day', '2 hours', etc.")
    
    value = int(parts[0])
    unit = parts[1].lower()
    
    if 'second' in unit or 'sec' in unit:
        return datetime.timedelta(seconds=value)
    elif 'minute' in unit or 'min' in unit:
        return datetime.timedelta(minutes=value)
    elif 'hour' in unit or 'hr' in unit:
        return datetime.timedelta(hours=value)
    elif 'day' in unit:
        return datetime.timedelta(days=value)
    elif 'week' in unit:
        return datetime.timedelta(weeks=value)
    elif 'month' in unit:
        return datetime.timedelta(days=value * 30)
    elif 'year' in unit:
        return datetime.timedelta(days=value * 365)
    else:
        raise ValueError(f"Unknown time unit: {unit}")


def main():
    parser = argparse.ArgumentParser(description='Timestamp converter')
    parser.add_argument('--now', action='store_true', help='Current timestamp')
    parser.add_argument('--to-human', type=int, metavar='TIMESTAMP', help='Convert to date')
    parser.add_argument('--to-unix', metavar='DATE', help='Convert date to timestamp')
    parser.add_argument('--add', metavar='OFFSET', help='Add time (e.g., "1 day")')
    parser.add_argument('--subtract', metavar='OFFSET', help='Subtract time')
    parser.add_argument('--format', default='%Y-%m-%d %H:%M:%S', help='Output format')
    parser.add_argument('--utc', action='store_true', help='Use UTC')
    
    args = parser.parse_args()
    
    try:
        # Determine base time
        if args.now or (not args.to_human and not args.to_unix):
            base_time = datetime.datetime.now(datetime.timezone.utc if args.utc else None)
        elif args.to_human:
            ts = args.to_human
            if args.utc:
                base_time = datetime.datetime.utcfromtimestamp(ts)
            else:
                base_time = datetime.datetime.fromtimestamp(ts)
        elif args.to_unix:
            base_time = datetime.datetime.strptime(args.to_unix, '%Y-%m-%d %H:%M:%S')
            if not args.utc:
                # Assume local time
                base_time = base_time.replace(tzinfo=datetime.timezone.utc).astimezone()
        else:
            base_time = datetime.datetime.now(datetime.timezone.utc if args.utc else None)
        
        # Apply offset
        if args.add:
            offset = parse_offset(args.add)
            base_time += offset
        elif args.subtract:
            offset = parse_offset(args.subtract)
            base_time -= offset
        
        # Output
        print(base_time.strftime(args.format))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
