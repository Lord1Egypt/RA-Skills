#!/usr/bin/env python3
"""
Tencent Cloud VOD AIGC API Token Management Tool

Purpose: Manage API Tokens (APIKeys) required for the VOD AIGC text generation API.
Tokens have no expiration time; after creation, allow approximately 1 minute for gateway synchronization.
Each user can have at most 50 Tokens.

Subcommands:
  create   Create a new Token
  delete   Delete a specified Token
  list     Query the Token list
  usage    Query AIGC usage statistics (Video/Image/Text)

Usage examples:
  python scripts/vod_aigc_token.py create
  python scripts/vod_aigc_token.py list
  python scripts/vod_aigc_token.py delete --api-token <api_token>
  python scripts/vod_aigc_token.py usage --type Text --start 2026-03-01 --end 2026-03-19
  python scripts/vod_aigc_token.py usage --type Video --start 2026-03-01 --end 2026-03-19
"""

import argparse
import json
import os
import re
import sys

# tencentcloud SDK version check
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vod_auto_upgrade import check_sdk_version

# Soft dependency: vod_load_env is used as a fallback to load credentials from ~/.env etc. when env vars are missing
try:
    from vod_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
    def _ensure_env_loaded(**kwargs):
        return False

check_sdk_version()

try:
    from tencentcloud.common import credential
    from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
    from tencentcloud.vod.v20180717 import vod_client, models
except ImportError:
    print("❌ Missing dependencies, please install first: pip install tencentcloud-sdk-python", file=sys.stderr)
    sys.exit(1)

DEFAULT_REGION = "ap-guangzhou"


def get_client(region: str = DEFAULT_REGION):
    """Create a VOD client"""
    secret_id = os.environ.get("TENCENTCLOUD_SECRET_ID", "")
    secret_key = os.environ.get("TENCENTCLOUD_SECRET_KEY", "")
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
    cred = credential.Credential(secret_id, secret_key)
    return vod_client.VodClient(cred, region)


# ─────────────────────────────────────────────
# Token Management API
# ─────────────────────────────────────────────

def create_token(client, sub_app_id: int = None) -> dict:
    """
    Create an AIGC API Token.
    Tokens have no expiration time; after creation, allow approximately 1 minute for gateway synchronization.
    """
    req = models.CreateAigcApiTokenRequest()
    if sub_app_id:
        req.SubAppId = sub_app_id
    resp = client.CreateAigcApiToken(req)
    return json.loads(resp.to_json_string())


def delete_token(client, api_token: str, sub_app_id: int = None) -> None:
    """
    Delete an AIGC API Token.
    After deletion, allow a brief period (approximately 1 minute) for the gateway to invalidate it.

    Args:
        api_token: The API Token string to delete (not the TokenId)
        sub_app_id: VOD sub-application ID (required for users who activated after December 2023)
    """
    req = models.DeleteAigcApiTokenRequest()
    req.ApiToken = api_token
    if sub_app_id:
        req.SubAppId = sub_app_id
    client.DeleteAigcApiToken(req)


def list_tokens(client, sub_app_id: int = None) -> dict:
    """Query the AIGC API Token list"""
    req = models.DescribeAigcApiTokensRequest()
    if sub_app_id:
        req.SubAppId = sub_app_id
    resp = client.DescribeAigcApiTokens(req)
    return json.loads(resp.to_json_string())


def describe_aigc_usage(
    client,
    start_time: str,
    end_time: str,
    aigc_type: str,
    sub_app_id: int = None,
) -> dict:
    """
    Query AIGC usage statistics.
    aigc_type: Video | Image | Text
    start_time/end_time: ISO format, e.g. 2026-03-01T00:00:00+08:00
    """
    req = models.DescribeAigcUsageDataRequest()
    req.StartTime = start_time
    req.EndTime   = end_time
    req.AigcType  = aigc_type
    if sub_app_id:
        req.SubAppId = sub_app_id
    resp = client.DescribeAigcUsageData(req)
    return json.loads(resp.to_json_string())


# ─────────────────────────────────────────────
# Output Formatting
# ─────────────────────────────────────────────

# Candidate dotenv file paths (consistent with vod_load_env._ENV_FILES; only dotenv-style files are scanned)
_ALL_ENV_FILES = [
    os.path.expanduser("~/.env"),
    os.path.join(os.getcwd(), ".env"),
]

_TOKEN_KEY = "TENCENTCLOUD_VOD_AIGC_TOKEN"
_DEFAULT_ENV_FILE = os.path.expanduser("~/.env")


def _update_token_in_file(filepath: str, token: str) -> bool:
    """
    Update or append TENCENTCLOUD_VOD_AIGC_TOKEN in the specified file.
    If the line already exists in the file, replace it; otherwise append.
    Returns True on success.
    """
    try:
        lines = []
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()

        new_lines = []
        found = False
        for line in lines:
            stripped = line.strip()
            # Match KEY=... or export KEY=... format
            if re.match(rf"""^\s*(?:export\s+)?{_TOKEN_KEY}\s*=""", stripped):
                new_lines.append(f'export {_TOKEN_KEY}="{token}"\n')
                found = True
            else:
                new_lines.append(line)

        if not found:
            # Ensure a newline at the end of the file before appending
            if new_lines and not new_lines[-1].endswith("\n"):
                new_lines.append("\n")
            new_lines.append(f'export {_TOKEN_KEY}="{token}"\n')

        with open(filepath, "w", encoding="utf-8") as f:
            f.writelines(new_lines)
        return True
    except Exception as e:
        print(f"⚠️  Failed to write to {filepath}: {e}", file=sys.stderr)
        return False


def find_token_in_env_files() -> list:
    """
    Scan all candidate config files and return a list of file paths containing TENCENTCLOUD_VOD_AIGC_TOKEN.
    """
    found_files = []
    token_re = re.compile(rf"""^\s*(?:export\s+)?{_TOKEN_KEY}\s*=""")
    for filepath in _ALL_ENV_FILES:
        if not os.path.isfile(filepath):
            continue
        try:
            with open(filepath, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    if token_re.match(line):
                        found_files.append(filepath)
                        break
        except (OSError, IOError):
            pass
    return found_files


def save_token_to_env(token: str) -> list:
    """
    Write the Token to environment variable config files.
    Strategy:
      1. Scan all candidate files and update all files that already contain TENCENTCLOUD_VOD_AIGC_TOKEN.
      2. If none of the files contain the variable, write only to ~/.env.
    Returns: list of file paths successfully written to.
    """
    target_files = find_token_in_env_files()

    if not target_files:
        # No files have the config, default to writing to ~/.env
        target_files = [_DEFAULT_ENV_FILE]

    written = []
    for filepath in target_files:
        if _update_token_in_file(filepath, token):
            written.append(filepath)

    return written


def print_token_created(data: dict, as_json: bool = False):
    """Print the creation result"""
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    sep = "=" * 60
    print(f"\n{sep}")
    print("✅ AIGC API Token created successfully")
    print("─" * 60)
    # API response field is Api Token (no TokenId)
    token_id = data.get("TokenId", data.get("ApiTokenId", "-"))
    token    = data.get("ApiToken", data.get("Token", "-"))
    print(f"  Token ID : {token_id}")
    print(f"  Token    : {token}")
    print()
    # Automatically write to environment variable config files
    if token and token != "-":
        written_files = save_token_to_env(token)
        if written_files:
            for f in written_files:
                print(f"💾 Automatically written to {f} (TENCENTCLOUD_VOD_AIGC_TOKEN)")
    print()
    print("⚠️  Notes:")
    print("  1. Tokens have no expiration time — keep them secure")
    print("  2. After creation, allow approximately 1 minute for gateway synchronization before use")
    print("  3. Each user can have at most 50 Tokens")
    print(f"{sep}\n")


def print_token_list(data: dict, as_json: bool = False):
    """Print the Token list"""
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    sep = "=" * 60
    # API returns Api Tokens (string array) or Aigc Api Token Set (object array); compatible with both formats
    raw_tokens = data.get("ApiTokens") or data.get("AigcApiTokenSet") or []
    total  = len(raw_tokens)
    print(f"\n{sep}")
    print(f"AIGC API Token List (total: {total})")
    print("─" * 60)
    if not raw_tokens:
        print("  No Tokens found. Use the create subcommand to create one.")
    else:
        for i, t in enumerate(raw_tokens, 1):
            if isinstance(t, str):
                # Api Tokens format: string array
                masked = t[:8] + "..." + t[-4:] if len(t) > 12 else t
                print(f"  [{i}] Token : {masked}")
            else:
                # Aigc Api Token Set format: object array
                token_id    = t.get("TokenId", "-")
                token       = t.get("Token", "-")
                create_time = t.get("CreateTime", "-")
                print(f"  [{i}] Token ID    : {token_id}")
                print(f"      Token       : {token}")
                print(f"      Created At  : {create_time}")
            print()
    print(f"{sep}\n")


def print_usage_data(data: dict, aigc_type: str, as_json: bool = False):
    """Print AIGC usage statistics"""
    if as_json:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    sep = "=" * 60
    dataset = data.get("AigcUsageDataSet", [])
    print(f"\n{sep}")
    print(f"AIGC Usage Statistics (Type: {aigc_type})")
    print("─" * 60)
    if not dataset:
        print("  No usage data available")
    else:
        total_count = 0
        total_usage = 0
        for spec_item in dataset:
            spec = spec_item.get("Specification", "-")
            rows = spec_item.get("DataSet", [])
            spec_count = sum(r.get("Count", 0) for r in rows)
            spec_usage = sum(r.get("Usage", 0) for r in rows)
            if spec_count == 0 and spec_usage == 0:
                continue
            print(f"  Specification: {spec}")
            print(f"  {'Date':<30} {'Tasks':>8} {'Usage':>10}")
            print(f"  {'─'*30} {'─'*8} {'─'*10}")
            for row in rows:
                t   = row.get("Time", "-")[:10]  # Take only the date portion
                cnt = row.get("Count", 0)
                usg = row.get("Usage", 0)
                if cnt > 0 or usg > 0:
                    print(f"  {t:<30} {cnt:>8} {usg:>10}")
            print(f"  {'Subtotal':<30} {spec_count:>8} {spec_usage:>10}")
            print()
            total_count += spec_count
            total_usage += spec_usage
        print("─" * 60)
        print(f"  {'Total':<30} {total_count:>8} {total_usage:>10}")
    print(f"{sep}\n")


# ─────────────────────────────────────────────
# CLI Entry Point
# ─────────────────────────────────────────────

def build_parser():
    parser = argparse.ArgumentParser(
        description="Tencent Cloud VOD AIGC API Token Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--region", default=DEFAULT_REGION,
                        help=f"Region (default: {DEFAULT_REGION})")
    parser.add_argument("--sub-app-id", type=int,
                        default=int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None,
                        help="VOD sub-application ID (required for users who activated after December 2023; can also be set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)")
    parser.add_argument("--json", action="store_true", dest="json_output",
                        help="Output in JSON format")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print parameter preview only, do not call the API")

    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    _sub_app_id_kwargs = dict(
        type=int,
        default=None,
        help="VOD sub-application ID (can also be placed in the global argument position or set via environment variable TENCENTCLOUD_VOD_SUB_APP_ID)",
    )

    # ── create ──
    p_create = subparsers.add_parser("create", help="Create a new AIGC API Token")
    p_create.add_argument("--sub-app-id", **_sub_app_id_kwargs)

    # ── delete ──
    p_delete = subparsers.add_parser("delete", help="Delete a specified AIGC API Token")
    p_delete.add_argument("--api-token", required=True,
                          help="The API Token string to delete (obtain via the list subcommand)")
    p_delete.add_argument("--sub-app-id", **_sub_app_id_kwargs)

    # ── list ──
    p_list = subparsers.add_parser("list", help="Query all AIGC API Tokens")
    p_list.add_argument("--sub-app-id", **_sub_app_id_kwargs)

    # ── usage ──
    p_usage = subparsers.add_parser("usage", help="Query AIGC usage statistics (Video/Image/Text)")
    p_usage.add_argument("--sub-app-id", **_sub_app_id_kwargs)
    p_usage.add_argument(
        "--type", "-t",
        dest="aigc_type",
        choices=["Video", "Image", "Text"],
        required=True,
        help="AIGC type: Video, Image, or Text",
    )
    p_usage.add_argument(
        "--start",
        default=None,
        help="Start date in YYYY-MM-DD or full ISO format (e.g. 2026-03-01); defaults to 30 days ago",
    )
    p_usage.add_argument(
        "--end",
        default=None,
        help="End date in YYYY-MM-DD or full ISO format (e.g. 2026-03-19); defaults to today",
    )

    return parser


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Merge sub-app-id: subcommand level takes priority, then global, then environment variable
    sub_app_id = getattr(args, "sub_app_id", None) or int(os.environ.get("TENCENTCLOUD_VOD_SUB_APP_ID", 0)) or None

    if args.dry_run:
        print("🔍 dry-run parameter preview:")
        print(f"  command    = {args.command}")
        print(f"  region     = {args.region}")
        if sub_app_id:
            print(f"  sub-app-id = {sub_app_id}")
        if args.command == "delete":
            print(f"  api-token  = {args.api_token}")
        if args.command == "usage":
            from datetime import datetime, timedelta
            today = datetime.now()
            default_start = (today - timedelta(days=30)).strftime("%Y-%m-%d")
            default_end = today.strftime("%Y-%m-%d")
            print(f"  type       = {args.aigc_type}")
            print(f"  start      = {args.start or default_start} (default: 30 days ago)" if not args.start else f"  start      = {args.start}")
            print(f"  end        = {args.end or default_end} (default: today)" if not args.end else f"  end        = {args.end}")
        return

    client = get_client(args.region)

    # In --json mode, progress info goes to stderr to avoid polluting JSON stdout
    _out = sys.stderr if args.json_output else sys.stdout

    try:
        if args.command == "create":
            # Check if a Token already exists in environment variables
            existing_token = os.environ.get("TENCENTCLOUD_VOD_AIGC_TOKEN", "").strip()
            if existing_token:
                masked = existing_token[:8] + "..." + existing_token[-4:] if len(existing_token) > 12 else existing_token[:4] + "..."
                print(f"⚠️  An existing AIGC Token was detected in environment variables: {masked}", file=_out)
                # Scan which files contain the config
                files_with_token = find_token_in_env_files()
                if files_with_token:
                    print("   The following config files contain TENCENTCLOUD_VOD_AIGC_TOKEN and will all be updated after creation:", file=_out)
                    for f in files_with_token:
                        print(f"     • {f}", file=_out)
                else:
                    print(f"   The new Token will be written to {_DEFAULT_ENV_FILE}", file=_out)
                try:
                    answer = input("   Continue creating a new Token? [y/N] ").strip().lower()
                except (EOFError, KeyboardInterrupt):
                    answer = "n"
                if answer not in ("y", "yes"):
                    print("⏭️  Cancelled. Existing Token retained.", file=_out)
                    sys.exit(0)
            print("🚀 Creating AIGC API Token...", file=_out)
            data = create_token(client, sub_app_id=sub_app_id)
            print_token_created(data, as_json=args.json_output)

        elif args.command == "delete":
            print(f"🗑️  Deleting Token: {args.api_token}", file=_out)
            delete_token(client, api_token=args.api_token, sub_app_id=sub_app_id)
            print(f"✅ Token {args.api_token} has been deleted (gateway invalidation takes approximately 1 minute)", file=_out)

        elif args.command == "list":
            print("🔍 Querying AIGC API Token list...", file=_out)
            data = list_tokens(client, sub_app_id=sub_app_id)
            print_token_list(data, as_json=args.json_output)

        elif args.command == "usage":
            # Date format compatibility: if only YYYY-MM-DD is provided, auto-complete to ISO format
            def to_iso(date_str: str, is_end: bool = False) -> str:
                if "T" not in date_str:
                    suffix = "T23:59:59+08:00" if is_end else "T00:00:00+08:00"
                    return date_str + suffix
                return date_str

            # Defaults: start = 30 days ago, end = today
            from datetime import datetime, timedelta
            today = datetime.now()
            default_start = (today - timedelta(days=30)).strftime("%Y-%m-%d")
            default_end = today.strftime("%Y-%m-%d")

            start_iso = to_iso(args.start or default_start, is_end=False)
            end_iso   = to_iso(args.end or default_end, is_end=True)
            print(f"🔍 Querying AIGC usage statistics | Type: {args.aigc_type} | {start_iso} ~ {end_iso}", file=_out)
            data = describe_aigc_usage(
                client,
                start_time=start_iso,
                end_time=end_iso,
                aigc_type=args.aigc_type,
                sub_app_id=sub_app_id,
            )
            print_usage_data(data, aigc_type=args.aigc_type, as_json=args.json_output)

    except TencentCloudSDKException as e:
        print(f"❌ API call failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
