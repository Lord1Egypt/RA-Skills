#!/usr/bin/env python3
"""
Tencent Cloud MPS Usage Statistics Query Script

Features:
  Query MPS media processing usage information within a specified time range, with support for filtering by task type
  and region.
  Data from the last 365 days can be queried, with a maximum span of 90 days per query.

Supported Task Types (--type parameter):
  Transcode         Transcoding
  Enhance           Enhancement
  AIAnalysis        Intelligent Analysis
  AIRecognition     Intelligent Recognition
  AIReview          Content Review
  Snapshot          Screenshot
  AnimatedGraphics  Animated Image
  AiQualityControl  Quality Control
  Evaluation        Video Evaluation
  ImageProcess      Image Processing
  AddBlindWatermark Add Basic Copyright Digital Watermark
  AIGC              AIGC (Image/Video Generation)

Supported Regions (--region parameter):
  ap-guangzhou (default), ap-hongkong, ap-singapore,
  na-siliconvalley, eu-frankfurt, etc.

Usage:
  # Query transcoding usage for the last 7 days (default)
  python scripts/mps_usage.py

  # Query a specific date range
  python scripts/mps_usage.py --start 2024-01-01 --end 2024-01-31

  # Query multiple task types
  python scripts/mps_usage.py --type Transcode Enhance AIGC

  # Query specific regions
  python scripts/mps_usage.py --region ap-guangzhou ap-hongkong

  # Output in JSON format (convenient for programmatic processing)
  python scripts/mps_usage.py --json

  # Query all types for the last 30 days
  python scripts/mps_usage.py --days 30 --all-types
"""

import sys
from mps_auto_upgrade import check_sdk_version
import os
import json
import argparse
from datetime import datetime, timedelta, timezone

# ── Load environment variables (aligned with other scripts) ──
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)
try:
    from mps_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False

check_sdk_version()
try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.mps.v20190612 import mps_client, models
except ImportError:
    print("❌ Missing dependency, please run: pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)

# All supported task types
ALL_TASK_TYPES = [
    "Transcode", "Enhance", "AIAnalysis", "AIRecognition",
    "AIReview", "Snapshot", "AnimatedGraphics", "AiQualityControl",
    "Evaluation", "ImageProcess", "AddBlindWatermark",
    "AddNagraWatermark", "ExtractBlindWatermark", "AIGC",
]

# Task type display names (AvUnderstand belongs to AIAnalysis, not a standalone type)
TYPE_NAMES = {
    "Transcode":              "Transcoding",
    "Enhance":                "Enhancement",
    "AIAnalysis":             "Intelligent Analysis (incl. Large Model Audio/Video Understanding AvUnderstand)",
    "AIRecognition":          "Intelligent Recognition",
    "AIReview":               "Content Review",
    "Snapshot":               "Screenshot",
    "AnimatedGraphics":       "Animated Image",
    "AiQualityControl":       "Quality Control",
    "Evaluation":             "Video Evaluation",
    "ImageProcess":           "Image Processing",
    "AddBlindWatermark":      "Add Basic Copyright Digital Watermark",
    "AddNagraWatermark":      "Add NAGRA Digital Watermark",
    "ExtractBlindWatermark":  "Extract Basic Copyright Digital Watermark",
    "AIGC":                   "AIGC (Image/Video Generation)",
}


def get_credentials():
    """Get Tencent Cloud credentials from environment variables.
    If missing, try to auto-load from system files and retry."""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
    if not secret_id or not secret_key:
        # Try to auto-load from system environment files
        if _LOAD_ENV_AVAILABLE:
            print("[load_env] Environment variables not set, trying to auto-load from system files...", file=sys.stderr)
            _ensure_env_loaded(verbose=True)
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
        if not secret_id or not secret_key:
            if _LOAD_ENV_AVAILABLE:
                from mps_load_env import _print_setup_hint
                _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
            else:
                print(
                    "\n❌ Please configure environment variables TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY.\n"  # NOCA:line-too-long(error message readability)
                    "Add these variables to /etc/environment, ~/.profile, etc.\n",
                    file=sys.stderr,
                )
            sys.exit(1)
    return credential.Credential(secret_id, secret_key)


def to_iso8601(date_str: str) -> str:
    """Convert YYYY-MM-DD to ISO 8601 format (+08:00)"""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.strftime("%Y-%m-%dT00:00:00+08:00")


def query_usage(
    start_time: str,
    end_time: str,
    types: list = None,
    regions: list = None,
    region: str = "ap-guangzhou",
    dry_run: bool = False,
    raise_on_error: bool = False,
) -> dict:
    """
    Call the DescribeUsageData API to query usage
    Returns the raw API response data
    raise_on_error=True raises exceptions instead of sys.exit (for batch fault-tolerance scenarios)
    """
    cred = get_credentials()
    http_profile = HttpProfile()
    http_profile.endpoint = os.environ.get("TENCENTCLOUD_MPS_ENDPOINT", "mps.tencentcloudapi.com")
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    client = mps_client.MpsClient(cred, region, client_profile)

    req = models.DescribeUsageDataRequest()
    req.StartTime = to_iso8601(start_time)
    req.EndTime = to_iso8601(end_time)

    if types:
        req.Types = types
    if regions:
        req.ProcessRegions = regions

    if dry_run:
        print("[dry-run] Request parameters:")
        print(f"  StartTime: {req.StartTime}")
        print(f"  EndTime:   {req.EndTime}")
        print(f"  Types:     {types or 'Default (Transcode)'}")
        print(f"  Regions:   {regions or '[ap-guangzhou]'}")
        return {}

    try:
        resp = client.DescribeUsageData(req)
        return json.loads(resp.to_json_string())
    except TencentCloudSDKException as e:
        if raise_on_error:
            raise
        print(f"❌ API call failed: {e}", file=sys.stderr)
        sys.exit(1)


def format_usage(usage_seconds: int, task_type: str) -> str:
    """Format usage value (transcoding types use minutes, AIGC types use count)"""
    aigc_types = {"AIGC", "AIAnalysis", "AIRecognition", "AIReview",
                  "AiQualityControl", "Evaluation", "AddBlindWatermark",
                  "AddNagraWatermark", "ExtractBlindWatermark"}
    if task_type in aigc_types:
        return f"{usage_seconds} times"
    # Transcoding/Enhancement/Image Processing etc.: Usage unit is seconds
    minutes = usage_seconds / 60
    if minutes >= 60:
        return f"{minutes/60:.2f} hours ({minutes:.1f} minutes)"
    return f"{minutes:.2f} minutes"


def print_report(data: dict, output_json: bool = False):
    """Format and output usage report"""
    if output_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    task_data_list = data.get("Data", [])
    if not task_data_list:
        print("📊 Query result is empty (no usage data in this time period)")
        return

    print("\n" + "═" * 60)
    print("  📊 MPS Media Processing Usage Report")
    print("═" * 60)

    for task_data in task_data_list:
        task_type = task_data.get("TaskType", "Unknown")
        type_name = TYPE_NAMES.get(task_type, task_type)
        summary = task_data.get("Summary", [])
        details = task_data.get("Details", [])

        # Summary statistics
        total_count = sum(s.get("Count", 0) for s in summary)
        total_usage = sum(s.get("Usage", 0) for s in summary)

        print(f"\n▶ {task_type} — {type_name}")
        print(f"  Total calls: {total_count:,}")
        print(f"  Total usage: {format_usage(total_usage, task_type)}")

        # Daily breakdown
        if summary:
            print(f"  {'Date':<22} {'Count':>8} {'Usage':>20}")
            print(f"  {'-'*22} {'-'*8} {'-'*20}")
            for s in summary:
                date = s.get("Time", "")[:10]
                count = s.get("Count", 0)
                usage = s.get("Usage", 0)
                usage_str = format_usage(usage, task_type)
                print(f"  {date:<22} {count:>8,} {usage_str:>20}")

        # Specification breakdown
        if details:
            print(f"\n  Specification breakdown:")
            for detail in details:
                spec = detail.get("Specification", "")
                spec_data = detail.get("Data", [])
                spec_count = sum(d.get("Count", 0) for d in spec_data)
                spec_usage = sum(d.get("Usage", 0) for d in spec_data)
                if spec_count > 0:
                    print(f"    {spec:<35} {spec_count:>8,} times  {format_usage(spec_usage, task_type)}")

    print("\n" + "═" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Query MPS Media Processing Usage Statistics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Time parameters
    time_group = parser.add_mutually_exclusive_group()
    time_group.add_argument("--days", type=int, default=7,
                            help="Query the last N days (default: 7, max: 90)")
    time_group.add_argument("--start", metavar="YYYY-MM-DD",
                            help="Start date (use with --end)")
    parser.add_argument("--end", metavar="YYYY-MM-DD",
                        help="End date (default: today)")

    # Type parameters
    type_group = parser.add_mutually_exclusive_group()
    type_group.add_argument("--type", nargs="+", choices=ALL_TASK_TYPES,
                            metavar="TYPE", dest="types",
                            help="Task types to query (multiple allowed), default: Transcode")
    type_group.add_argument("--all-types", action="store_true",
                            help="Query all task types")

    # Region parameters
    parser.add_argument("--region", nargs="+", dest="process_regions",
                        metavar="REGION",
                        help="Processing regions (multiple allowed), default: ap-guangzhou")

    # Output parameters
    parser.add_argument("--json", action="store_true",
                        help="Output raw data in JSON format")
    parser.add_argument("--dry-run", action="store_true",
                        help="Only print request parameters, do not make actual API call")

    args = parser.parse_args()

    # ── Calculate time range ──
    today = datetime.now(tz=timezone(timedelta(hours=8))).strftime("%Y-%m-%d")

    if args.start:
        start_date = args.start
        end_date = args.end or today
    else:
        days = min(args.days, 90)
        end_date = today
        start_dt = datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=days - 1)
        start_date = start_dt.strftime("%Y-%m-%d")

    # ── Determine task types ──
    if args.all_types:
        types = ALL_TASK_TYPES
    elif args.types:
        types = args.types
    else:
        types = None  # Default: API returns Transcode

    print(f"🔍 Query period: {start_date} ~ {end_date}")
    print(f"📋 Task types: {', '.join(types) if types else 'Default (Transcode)'}")
    print(f"🌏 Processing regions: {', '.join(args.process_regions) if args.process_regions else 'ap-guangzhou'}")

    # ── Call API ──
    if args.all_types:
        # --all-types mode: query each type individually with fault tolerance
        all_data = []
        failed_types = []
        for t in types:
            try:
                data = query_usage(
                    start_time=start_date,
                    end_time=end_date,
                    types=[t],
                    regions=args.process_regions,
                    dry_run=args.dry_run,
                    raise_on_error=True,
                )
                if not args.dry_run:
                    task_list = data.get("Data", [])
                    if task_list:
                        all_data.extend(task_list)
            except TencentCloudSDKException as e:
                print(f"  ⚠️  {t} query failed: {e}", file=sys.stderr)
                failed_types.append(t)

        if failed_types:
            print(f"\n⚠️  The following types failed to query (may not be supported or lack permissions): {', '.join(failed_types)}", file=sys.stderr)  # NOCA:line-too-long(content cannot be shortened)

        if not args.dry_run:
            merged = {"Data": all_data}
            print_report(merged, output_json=args.json)
    else:
        data = query_usage(
            start_time=start_date,
            end_time=end_date,
            types=types,
            regions=args.process_regions,
            dry_run=args.dry_run,
        )

        if not args.dry_run:
            print_report(data, output_json=args.json)


if __name__ == "__main__":
    main()
