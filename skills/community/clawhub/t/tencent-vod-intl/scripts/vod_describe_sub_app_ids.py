#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VOD Sub-Application List Query Script
"""

import os
import sys
import json
import argparse

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from vod_auto_upgrade import check_sdk_version


try:
    from vod_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
    def _ensure_env_loaded(**kwargs):
        return False

try:
    from tencentcloud.common import credential
    from tencentcloud.common.profile.client_profile import ClientProfile
    from tencentcloud.common.profile.http_profile import HttpProfile
    from tencentcloud.vod.v20180717 import vod_client, models
except ImportError:
    print("Error: Please install the Tencent Cloud SDK first: pip install tencentcloud-sdk-python")
    sys.exit(1)


DEFAULT_REGION = "ap-guangzhou"
MAX_LIMIT = 200


def get_credential():
    """Get Tencent Cloud credentials"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")

    if not secret_id or not secret_key:
        # Fallback: try to load credentials from ~/.env etc.
        if _LOAD_ENV_AVAILABLE:
            print("[load_env] Environment variables not set, attempting to load from dotenv files...", file=sys.stderr)
            _ensure_env_loaded(verbose=True)
            secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID")
            secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY")
        if not secret_id or not secret_key:
            if _LOAD_ENV_AVAILABLE:
                from vod_load_env import _print_setup_hint
                _print_setup_hint(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
            else:
                print("Error: Please set environment variables TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY", file=sys.stderr)
            sys.exit(1)

    return credential.Credential(secret_id, secret_key)


def get_client(region=DEFAULT_REGION):
    """Get VOD client"""
    cred = get_credential()
    http_profile = HttpProfile()
    http_profile.endpoint = "vod.tencentcloudapi.com"
    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile
    return vod_client.VodClient(cred, region, client_profile)


def normalize_tags(tag_args):
    """Parse tag arguments KEY=VALUE into the structure required by the API"""
    if not tag_args:
        return []

    tags = []
    for raw_tag in tag_args:
        if "=" not in raw_tag:
            print(f"Error: Invalid tag argument format: {raw_tag}, please use KEY=VALUE format")
            sys.exit(1)

        tag_key, tag_value = raw_tag.split("=", 1)
        tag_key = tag_key.strip()
        tag_value = tag_value.strip()

        if not tag_key:
            print(f"Error: Tag key cannot be empty: {raw_tag}")
            sys.exit(1)

        tags.append({
            "TagKey": tag_key,
            "TagValue": tag_value,
        })

    return tags


def validate_args(args):
    """Validate pagination parameters"""
    if args.offset is not None and args.offset < 0:
        print("Error: --offset cannot be less than 0")
        sys.exit(1)

    if args.limit is not None and not 1 <= args.limit <= MAX_LIMIT:
        print(f"Error: --limit must be between 1 and {MAX_LIMIT}")
        sys.exit(1)


def build_request_payload(args):
    """Build request parameters"""
    validate_args(args)

    payload = {}

    if args.name:
        payload["Name"] = args.name

    tags = normalize_tags(args.tag)
    if tags:
        payload["Tags"] = tags

    if args.offset is not None:
        payload["Offset"] = args.offset

    if args.limit is not None:
        payload["Limit"] = args.limit

    return payload


def build_request(args):
    """Build SDK request object"""
    payload = build_request_payload(args)
    req = models.DescribeSubAppIdsRequest()
    req.from_json_string(json.dumps(payload, ensure_ascii=False))
    return req, payload


def format_tags(tags):
    """Format tag output"""
    if not tags:
        return "None"
    return ", ".join(
        f"{tag.get('TagKey', '')}={tag.get('TagValue', '')}"
        for tag in tags
    )


def format_regions(regions):
    """Format region output"""
    if not regions:
        return "None"
    return ", ".join(regions)


def print_human_readable(result, printer=print):
    """Print result in human-readable format"""
    total_count = result.get("TotalCount", 0)
    sub_app_list = result.get("SubAppIdInfoSet", [])
    request_id = result.get("RequestId", "N/A")

    printer("Query completed!")
    printer(f"Applications returned this time: {len(sub_app_list)}")
    printer(f"Total applications: {total_count}")
    printer(f"RequestId: {request_id}")

    if not sub_app_list:
        printer("No sub-applications found matching the criteria.")
        return

    for index, item in enumerate(sub_app_list, start=1):
        printer(f"\n[{index}] SubAppId: {item.get('SubAppId', 'N/A')}")
        printer(f"  Name: {item.get('SubAppIdName') or item.get('Name') or 'N/A'}")
        printer(f"  Description: {item.get('Description') or 'N/A'}")
        printer(f"  Status: {item.get('Status') or 'N/A'}")
        printer(f"  Mode: {item.get('Mode') or 'N/A'}")
        printer(f"  Created At: {item.get('CreateTime') or 'N/A'}")
        printer(f"  Storage Regions: {format_regions(item.get('StorageRegions'))}")
        printer(f"  Tags: {format_tags(item.get('Tags'))}")


def describe_sub_app_ids(args, client=None, printer=print):
    """Query sub-application list"""
    req, payload = build_request(args)

    if args.dry_run:
        printer("[DRY RUN] Request parameters:")
        printer(json.dumps(payload, indent=2, ensure_ascii=False))
        return payload

    if client is None:
        client = get_client(args.region)

    try:
        resp = client.DescribeSubAppIds(req)
        result = json.loads(resp.to_json_string())

        if args.json:
            printer(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print_human_readable(result, printer=printer)

        return result
    except Exception as e:
        printer(f"Query failed: {e}")
        sys.exit(1)


def create_parser():
    """Create command-line argument parser"""
    parser = argparse.ArgumentParser(
        description="VOD Sub-Application List Query Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Query all sub-applications
  python vod_describe_sub_app_ids.py

  # Filter by application name
  python vod_describe_sub_app_ids.py --name MyAppName

  # Filter by tags
  python vod_describe_sub_app_ids.py --tag env=prod --tag team=media

  # Paginated query with JSON output
  python vod_describe_sub_app_ids.py --offset 0 --limit 20 --json
        """,
    )

    parser.add_argument("--name", help="Filter by application name")
    parser.add_argument(
        "--tag",
        action="append",
        help="Filter by tag, format KEY=VALUE, can be specified multiple times",
    )
    parser.add_argument("--offset", type=int, help="Pagination start offset, default 0")
    parser.add_argument("--limit", type=int, help="Number of results to return, range 1-200")
    parser.add_argument("--region", default=DEFAULT_REGION, help="Region")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--dry-run", action="store_true", help="Preview request parameters")

    return parser


def main():
    check_sdk_version()
    parser = create_parser()
    args = parser.parse_args()
    describe_sub_app_ids(args)


if __name__ == "__main__":
    main()