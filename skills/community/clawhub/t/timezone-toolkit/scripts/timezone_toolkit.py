#!/usr/bin/env python3
"""Timezone toolkit: convert times, show world clocks, find meeting times, list timezones.

No external dependencies — uses Python's built-in zoneinfo (3.9+) and datetime.
"""

import argparse
import sys
from datetime import datetime, timedelta

try:
    from zoneinfo import ZoneInfo, available_timezones
except ImportError:
    print("Error: Python 3.9+ required for zoneinfo module.", file=sys.stderr)
    sys.exit(1)


# Common timezone aliases
ALIASES = {
    "EST": "America/New_York",
    "EDT": "America/New_York",
    "CST": "America/Chicago",
    "CDT": "America/Chicago",
    "MST": "America/Denver",
    "MDT": "America/Denver",
    "PST": "America/Los_Angeles",
    "PDT": "America/Los_Angeles",
    "GMT": "Etc/GMT",
    "UTC": "UTC",
    "BST": "Europe/London",
    "CET": "Europe/Paris",
    "CEST": "Europe/Paris",
    "IST": "Asia/Kolkata",
    "JST": "Asia/Tokyo",
    "KST": "Asia/Seoul",
    "CST_CN": "Asia/Shanghai",
    "AEST": "Australia/Sydney",
    "AEDT": "Australia/Sydney",
    "NZST": "Pacific/Auckland",
    "NZDT": "Pacific/Auckland",
    "SGT": "Asia/Singapore",
    "HKT": "Asia/Hong_Kong",
    "BRT": "America/Sao_Paulo",
    "ART": "America/Argentina/Buenos_Aires",
}


def resolve_tz(name):
    """Resolve a timezone name or alias to a ZoneInfo object."""
    upper = name.upper()
    if upper in ALIASES:
        return ZoneInfo(ALIASES[upper])
    try:
        return ZoneInfo(name)
    except (KeyError, Exception):
        pass
    # Fuzzy search
    lower = name.lower()
    for tz in sorted(available_timezones()):
        if lower in tz.lower():
            return ZoneInfo(tz)
    print(f"Unknown timezone: '{name}'. Use 'list' to find valid names.", file=sys.stderr)
    sys.exit(1)


def parse_time(time_str):
    """Parse a time string into a datetime. Accepts various formats."""
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%dT%H:%M",
        "%H:%M:%S",
        "%H:%M",
        "%I:%M %p",
        "%I:%M%p",
        "%I %p",
        "%I%p",
    ]
    for fmt in formats:
        try:
            dt = datetime.strptime(time_str, fmt)
            # If no date part, use today
            if dt.year == 1900:
                now = datetime.now()
                dt = dt.replace(year=now.year, month=now.month, day=now.day)
            return dt
        except ValueError:
            continue
    # Try "now"
    if time_str.lower() == "now":
        return datetime.now()
    print(f"Cannot parse time: '{time_str}'. Use formats like '15:30', '3:30 PM', '2026-03-15 10:00'.", file=sys.stderr)
    sys.exit(1)


def cmd_convert(args):
    """Convert a time between timezones."""
    from_tz = resolve_tz(args.source)
    dt = parse_time(args.time)
    dt_src = dt.replace(tzinfo=from_tz)

    targets = args.targets
    if not targets:
        targets = ["UTC"]

    print(f"Source: {dt_src.strftime('%Y-%m-%d %H:%M:%S %Z')} ({from_tz})")
    print()
    for target in targets:
        to_tz = resolve_tz(target)
        dt_tgt = dt_src.astimezone(to_tz)
        print(f"  {str(to_tz):30s}  {dt_tgt.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    return 0


def cmd_now(args):
    """Show current time in one or more timezones."""
    now_utc = datetime.now(ZoneInfo("UTC"))
    zones = args.zones if args.zones else [
        "America/New_York", "America/Chicago", "America/Los_Angeles",
        "Europe/London", "Europe/Paris", "Asia/Tokyo", "Asia/Shanghai",
        "Australia/Sydney", "UTC",
    ]

    print(f"Current time ({now_utc.strftime('%Y-%m-%d %H:%M:%S UTC')})")
    print()
    for z in zones:
        tz = resolve_tz(z)
        local = now_utc.astimezone(tz)
        offset = local.strftime("%z")
        offset_str = f"UTC{offset[:3]}:{offset[3:]}"
        print(f"  {str(tz):30s}  {local.strftime('%Y-%m-%d %H:%M:%S %Z'):30s}  {offset_str}")
    return 0


def cmd_meeting(args):
    """Find overlapping work hours between timezones."""
    zones = [resolve_tz(z) for z in args.zones]
    start_hour = args.start or 9
    end_hour = args.end or 17

    now_utc = datetime.now(ZoneInfo("UTC"))
    today = now_utc.date()

    print(f"Finding overlap for work hours {start_hour:02d}:00-{end_hour:02d}:00")
    print(f"Zones: {', '.join(str(z) for z in zones)}")
    print()

    # For each UTC hour, check if it falls within work hours for all zones
    overlaps = []
    for h in range(24):
        utc_dt = datetime(today.year, today.month, today.day, h, 0, tzinfo=ZoneInfo("UTC"))
        all_ok = True
        local_times = []
        for tz in zones:
            local = utc_dt.astimezone(tz)
            local_h = local.hour
            if not (start_hour <= local_h < end_hour):
                all_ok = False
            local_times.append((tz, local))
        if all_ok:
            overlaps.append((h, local_times))

    if overlaps:
        print("Overlapping hours (UTC):")
        for utc_h, locals_ in overlaps:
            parts = []
            for tz, lt in locals_:
                parts.append(f"{str(tz).split('/')[-1]}={lt.strftime('%H:%M')}")
            print(f"  {utc_h:02d}:00 UTC  →  {', '.join(parts)}")
        print(f"\n{len(overlaps)} overlapping hour(s) found.")
    else:
        print("No overlapping work hours found. Consider adjusting --start/--end.")
    return 0


def cmd_list(args):
    """List available timezones."""
    zones = sorted(available_timezones())
    if args.filter:
        filt = args.filter.lower()
        zones = [z for z in zones if filt in z.lower()]
    for z in zones:
        print(z)
    print(f"\n{len(zones)} timezone(s).", file=sys.stderr)
    return 0


def cmd_offset(args):
    """Show UTC offset for a timezone."""
    tz = resolve_tz(args.zone)
    now = datetime.now(tz)
    offset = now.strftime("%z")
    offset_str = f"UTC{offset[:3]}:{offset[3:]}"
    dst = "DST active" if now.dst() and now.dst() != timedelta(0) else "Standard time"
    print(f"{tz}")
    print(f"  Current time:  {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    print(f"  UTC offset:    {offset_str}")
    print(f"  DST status:    {dst}")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Timezone toolkit: convert, compare, and plan across timezones",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  %(prog)s convert 15:30 --from EST --to PST JST UTC
  %(prog)s convert "3:30 PM" --from PST --to EST
  %(prog)s now                                  # World clock (defaults)
  %(prog)s now EST PST JST                      # Specific zones
  %(prog)s meeting EST PST JST                  # Find overlapping hours
  %(prog)s meeting EST IST --start 8 --end 18   # Custom work hours
  %(prog)s list --filter America                 # List matching timezones
  %(prog)s offset Asia/Tokyo                     # Show offset & DST info
""",
    )

    sub = parser.add_subparsers(dest="command", help="Command to run")

    # convert
    p_conv = sub.add_parser("convert", help="Convert time between timezones")
    p_conv.add_argument("time", help="Time to convert (e.g., '15:30', '3:30 PM', 'now')")
    p_conv.add_argument("--from", "-f", dest="source", required=True, help="Source timezone")
    p_conv.add_argument("--to", "-t", dest="targets", nargs="+", help="Target timezone(s)")

    # now
    p_now = sub.add_parser("now", help="Show current time in multiple timezones")
    p_now.add_argument("zones", nargs="*", help="Timezone names (default: major cities)")

    # meeting
    p_meet = sub.add_parser("meeting", help="Find overlapping work hours")
    p_meet.add_argument("zones", nargs="+", help="Timezone names for participants")
    p_meet.add_argument("--start", type=int, help="Work day start hour (default: 9)")
    p_meet.add_argument("--end", type=int, help="Work day end hour (default: 17)")

    # list
    p_list = sub.add_parser("list", help="List available timezones")
    p_list.add_argument("--filter", "-f", help="Filter by name")

    # offset
    p_off = sub.add_parser("offset", help="Show UTC offset and DST info")
    p_off.add_argument("zone", help="Timezone name")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return 0

    cmds = {
        "convert": cmd_convert,
        "now": cmd_now,
        "meeting": cmd_meeting,
        "list": cmd_list,
        "offset": cmd_offset,
    }
    return cmds[args.command](args)


if __name__ == "__main__":
    sys.exit(main() or 0)
