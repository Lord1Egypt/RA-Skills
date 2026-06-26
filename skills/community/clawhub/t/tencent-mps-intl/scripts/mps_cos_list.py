#!/usr/bin/env python3
"""
Tencent Cloud COS File Listing Script

Features:
  Uses the Tencent Cloud COS Python SDK to list files in a specified Bucket, with support for path prefix filtering and
  filename search.

Usage:
  # List all files in the Bucket root directory (using bucket from environment variables)
  python mps_cos_list.py

  # List files under a specified path
  python mps_cos_list.py --prefix output/transcode/

  # Search for files by filename (fuzzy match)
  python mps_cos_list.py --search video

  # Exact match filename
  python mps_cos_list.py --search "result.mp4" --exact

  # Specify bucket and region
  python mps_cos_list.py --prefix input/ --bucket mybucket-125xxx --region ap-guangzhou

  # Limit the number of results
  python mps_cos_list.py --prefix output/ --limit 50

Environment Variables:
  TENCENTCLOUD_SECRET_ID   - Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  - Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET  - COS Bucket name (e.g., mybucket-125xxx)
  TENCENTCLOUD_COS_REGION  - COS Bucket region (default: ap-guangzhou)
"""

import argparse
import os
import sys
from datetime import datetime

# Load environment variable module (same directory)
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _SCRIPT_DIR)

try:
    from mps_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
try:
    from mps_load_env import ensure_env_loaded, check_required_vars, _print_setup_hint
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False

try:
    from qcloud_cos import CosConfig, CosS3Client
except ImportError:
    print("Error: Tencent Cloud COS SDK is not installed. Please run: pip install cos-python-sdk-v5", file=sys.stderr)
    sys.exit(1)


def parse_args():
    """Parse command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Tencent Cloud COS File Listing Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all files in the Bucket root directory
  python mps_cos_list.py

  # List files under a specified path
  python mps_cos_list.py --prefix output/transcode/

  # Fuzzy search for files with "video" in the filename
  python mps_cos_list.py --search video

  # Exact match filename "result.mp4"
  python mps_cos_list.py --search "result.mp4" --exact

  # List the first 50 files
  python mps_cos_list.py --prefix output/ --limit 50
        """
    )

    parser.add_argument(
        "--prefix", "-p",
        default="",
        help="Path prefix to filter files under a specified directory (e.g., output/transcode/)"
    )
    parser.add_argument(
        "--search", "-s",
        default=None,
        help="Filename search keyword, supports fuzzy matching"
    )
    parser.add_argument(
        "--exact",
        action="store_true",
        help="Exact match mode, only returns files with an exactly matching filename"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        default=1000,
        help="Maximum number of files to return (default: 1000, max: 1000)"
    )
    parser.add_argument(
        "--bucket", "-b",
        default=None,
        help="COS Bucket name (defaults to environment variable TENCENTCLOUD_COS_BUCKET)"
    )
    parser.add_argument(
        "--region", "-r",
        default=None,
        help="COS Bucket region (defaults to environment variable TENCENTCLOUD_COS_REGION or ap-guangzhou)"
    )
    parser.add_argument(
        "--secret-id",
        default=None,
        help="Tencent Cloud SecretId (defaults to environment variable TENCENTCLOUD_SECRET_ID)"
    )
    parser.add_argument(
        "--secret-key",
        default=None,
        help="Tencent Cloud SecretKey (defaults to environment variable TENCENTCLOUD_SECRET_KEY)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show verbose logs"
    )
    parser.add_argument(
        "--show-url",
        action="store_true",
        help="Show full file URLs"
    )

    return parser.parse_args()


def format_size(size_bytes):
    """Format file size"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / 1024 / 1024:.2f} MB"
    else:
        return f"{size_bytes / 1024 / 1024 / 1024:.2f} GB"


def format_time(time_str):
    """Format time string"""
    try:
        # COS returned time format: 2024-01-15T08:30:00.000Z
        dt = datetime.fromisoformat(time_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')  # NOCA:bare-except(intentional)
    except Exception:  # NOCA:broad-except(catch all for datetime parsing fallback)
        return time_str


def match_filename(key, search_term, exact=False):
    """
    Match filename

    Args:
        key: COS object key (full path)
        search_term: Search keyword
        exact: Whether to use exact matching

    Returns:
        bool: Whether it matches
    """
    if not search_term:
        return True

    # Get filename (strip path)
    filename = os.path.basename(key)

    if exact:
        return filename == search_term
    else:
        # Fuzzy match: filename contains search keyword (case-insensitive)
        return search_term.lower() in filename.lower()


def list_files(bucket, region, secret_id, secret_key, prefix="", search_term=None,
               exact=False, limit=1000, show_url=False, verbose=False):
    """
    List files in a COS Bucket

    Args:
        bucket: COS Bucket name
        region: COS Bucket region
        secret_id: Tencent Cloud SecretId
        secret_key: Tencent Cloud SecretKey
        prefix: Path prefix
        search_term: Filename search keyword
        exact: Whether to use exact matching
        limit: Maximum number of results
        show_url: Whether to show full URLs
        verbose: Whether to show verbose logs

    Returns:
        list: File list
    """
    # Create COS client
    config = CosConfig(
        Region=region,
        SecretId=secret_id,
        SecretKey=secret_key
    )
    client = CosS3Client(config)

    if verbose:
        print(f"Bucket: {bucket}")
        print(f"Region: {region}")
        print(f"Prefix: {prefix if prefix else '(root directory)'}")
        if search_term:
            match_type = "exact match" if exact else "fuzzy match"
            print(f"Search: {search_term} ({match_type})")
        print(f"Limit: up to {limit} files")
        print("-" * 60)

    # List files
    files = []
    marker = ""

    try:
        while len(files) < limit:
            # Each request returns at most 1000 items
            max_keys = min(1000, limit - len(files))

            response = client.list_objects(
                Bucket=bucket,
                Prefix=prefix,
                Marker=marker,
                MaxKeys=max_keys
            )

            # Get file list
            contents = response.get('Contents', [])

            for item in contents:
                key = item.get('Key', '')

                # Skip directories (keys ending with /)
                if key.endswith('/'):
                    continue

                # Filename match check
                if not match_filename(key, search_term, exact):
                    continue

                file_info = {
                    'Key': key,
                    'Size': int(item.get('Size', 0)),
                    'LastModified': item.get('LastModified', ''),
                    'ETag': item.get('ETag', '').strip('"'),
                }

                if show_url:
                    file_info['URL'] = f"https://{bucket}.cos.{region}.myqcloud.com/{key.lstrip('/')}"

                files.append(file_info)

                if len(files) >= limit:
                    break

            # Check if there are more files
            is_truncated = response.get('IsTruncated', 'false')
            if is_truncated == 'false' or is_truncated is False:
                break

            # Get the marker for the next page
            marker = response.get('NextMarker', '')
            if not marker:
                break

        return files

    except Exception as e:  # NOCA:broad-except(CLI script needs to handle all exceptions)
        print(f"Failed to list files: {e}", file=sys.stderr)
        return None


def print_files(files, show_url=False, bucket=None, region=None):
    """
    Print file list

    Args:
        files: File list
        show_url: Whether to show URLs
        bucket: Bucket name
        region: Region
    """
    if not files:
        print("No files found.")
        return

    print(f"\nFound {len(files)} file(s) in total\n")

    # Table header
    if show_url:
        print(f"{'No.':<6} {'Filename':<40} {'Size':<12} {'Modified':<20} {'URL'}")
        print("-" * 120)
    else:
        print(f"{'No.':<6} {'Filename':<50} {'Size':<12} {'Modified'}")
        print("-" * 90)

    # Print file info
    for idx, file in enumerate(files, 1):
        key = file['Key']
        filename = os.path.basename(key)
        size = format_size(file['Size'])
        last_modified = format_time(file['LastModified'])

        # Truncate filename to fit display
        display_name = filename[:38] + "..." if len(filename) > 40 else filename

        if show_url:
            url = file.get('URL', '')
            print(f"{idx:<6} {display_name:<40} {size:<12} {last_modified:<20} {url}")
        else:
            print(f"{idx:<6} {display_name:<50} {size:<12} {last_modified}")

    print()

    # Summary statistics
    total_size = sum(f['Size'] for f in files)
    print(f"Total size: {format_size(total_size)}")


def main():
    """Main function"""
    args = parse_args()

    # Load environment variables
    if _LOAD_ENV_AVAILABLE:
        loaded = ensure_env_loaded(verbose=args.verbose)
        if not loaded:
            missing = check_required_vars(["TENCENTCLOUD_SECRET_ID", "TENCENTCLOUD_SECRET_KEY"])
            _print_setup_hint(missing)
            sys.exit(1)

    # Get configuration (command-line arguments take priority, then environment variables)
    secret_id = args.secret_id or os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = args.secret_key or os.environ.get("TENCENTCLOUD_SECRET_KEY")
    bucket = args.bucket or os.environ.get("TENCENTCLOUD_COS_BUCKET")
    region = args.region or os.environ.get("TENCENTCLOUD_COS_REGION") or ""

    # Check required parameters
    if not secret_id or not secret_key:
        print("Error: Missing Tencent Cloud credential configuration. Please set the TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY environment variables, or use the --secret-id and --secret-key arguments.", file=sys.stderr)  # NOCA:line-too-long(line cannot be shortened)
        sys.exit(1)

    if not bucket:
        print("Error: Missing COS Bucket configuration. Please set the TENCENTCLOUD_COS_BUCKET environment variable, or use the --bucket argument.", file=sys.stderr)  # NOCA:line-too-long(line cannot be shortened)
        sys.exit(1)

    # Limit maximum number of results
    limit = min(args.limit, 1000)

    # List files
    files = list_files(
        bucket=bucket,
        region=region,
        secret_id=secret_id,
        secret_key=secret_key,
        prefix=args.prefix,
        search_term=args.search,
        exact=args.exact,
        limit=limit,
        show_url=args.show_url,
        verbose=args.verbose
    )

    if files is not None:
        print_files(files, show_url=args.show_url, bucket=bucket, region=region)
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
