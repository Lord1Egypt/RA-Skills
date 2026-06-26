#!/usr/bin/env python3
"""
Tencent Cloud COS File Download Script

Features:
  Uses the Tencent Cloud COS Python SDK to download files from a COS Bucket to local.

Usage:
  # Simplest usage (local-file is omitted, automatically uses ./<cos-input-key filename>)
  python mps_cos_download.py --cos-input-key output/result.mp4

  # Manually specify local-file
  python mps_cos_download.py --cos-input-key output/result.mp4 --local-file ./result.mp4

  # Specify bucket and region (overrides environment variables)
  python mps_cos_download.py --cos-input-key output/result.mp4 --local-file ./result.mp4 \\
      --bucket mybucket-125xxx --region ap-guangzhou

Environment Variables:
  TENCENTCLOUD_SECRET_ID   - Tencent Cloud SecretId
  TENCENTCLOUD_SECRET_KEY  - Tencent Cloud SecretKey
  TENCENTCLOUD_COS_BUCKET  - COS Bucket name (e.g. mybucket-125xxx)
  TENCENTCLOUD_COS_REGION  - COS Bucket region (default: ap-guangzhou)
"""

import argparse
import os
import sys

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
    print("Error: Tencent Cloud COS SDK not installed. Please run: pip install cos-python-sdk-v5", file=sys.stderr)
    sys.exit(1)


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Tencent Cloud COS File Download Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simplest usage: omit --local-file, automatically saves as ./<filename>
  python mps_cos_download.py --cos-input-key output/result.mp4
  # Equivalent to: --local-file ./result.mp4

  # Manually specify local-file
  python mps_cos_download.py --cos-input-key output/result.mp4 --local-file ./result.mp4

  # Specify bucket and region
  python mps_cos_download.py --cos-input-key output/result.mp4 --local-file ./result.mp4 \\
      --bucket mybucket-125xxx --region ap-guangzhou
        """
    )

    parser.add_argument(
        "--cos-input-key", "-k",
        required=True,
        help="COS object key (Key), e.g. input/video.mp4 (required)"
    )
    parser.add_argument(
        "--local-file", "-f",
        default=None,
        help="Local save path (default: ./<cos-input-key filename>)"
    )
    parser.add_argument(
        "--bucket", "-b",
        default=None,
        help="COS Bucket name (default: uses env var TENCENTCLOUD_COS_BUCKET)"
    )
    parser.add_argument(
        "--region", "-r",
        default=None,
        help="COS Bucket region (default: uses env var TENCENTCLOUD_COS_REGION or ap-guangzhou)"
    )
    parser.add_argument(
        "--secret-id",
        default=None,
        help="Tencent Cloud SecretId (default: uses env var TENCENTCLOUD_SECRET_ID)"
    )
    parser.add_argument(
        "--secret-key",
        default=None,
        help="Tencent Cloud SecretKey (default: uses env var TENCENTCLOUD_SECRET_KEY)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed logs"
    )

    return parser.parse_args()


def download_file(cos_key, local_file, bucket, region, secret_id, secret_key, verbose=False):
    """
    Download a file from COS

    Args:
        cos_key: COS object key
        local_file: Local save path
        bucket: COS Bucket name
        region: COS Bucket region
        secret_id: Tencent Cloud SecretId
        secret_key: Tencent Cloud SecretKey
        verbose: Whether to show detailed logs

    Returns:
        dict: Download result, including file size and local path
    """
    # Create local directory (if it doesn't exist)
    local_dir = os.path.dirname(os.path.abspath(local_file))
    if local_dir and not os.path.exists(local_dir):
        os.makedirs(local_dir, exist_ok=True)
        if verbose:
            print(f"Created directory: {local_dir}")

    if verbose:
        print(f"Source Bucket: {bucket}")
        print(f"Source Region: {region}")
        print(f"COS Key: {cos_key}")
        print(f"Local save path: {local_file}")

    # Create COS client
    config = CosConfig(
        Region=region,
        SecretId=secret_id,
        SecretKey=secret_key
    )
    client = CosS3Client(config)

    # Download file
    try:
        if verbose:
            print(f"Starting download...")

        _response = client.download_file(
            Bucket=bucket,
            Key=cos_key.lstrip('/'),
            DestFilePath=local_file
        )

        # Get downloaded file size
        file_size = os.path.getsize(local_file)

        # Build file URL
        url = f"https://{bucket}.cos.{region}.myqcloud.com/{cos_key.lstrip('/')}"

        result = {
            "Key": cos_key,
            "Bucket": bucket,
            "Region": region,
            "LocalFile": local_file,
            "URL": url,
            "Size": file_size
        }

        if verbose:
            print(f"Download successful!")
            print(f"File size: {file_size / 1024 / 1024:.2f} MB")

        return result

    except Exception as e:  # NOCA:broad-except(CLI script needs to handle all exceptions)
        print(f"Download failed: {e}", file=sys.stderr)
        return None


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

    # Get configuration (command line args take priority, then environment variables)
    secret_id = args.secret_id or os.environ.get("TENCENTCLOUD_SECRET_ID")
    secret_key = args.secret_key or os.environ.get("TENCENTCLOUD_SECRET_KEY")
    bucket = args.bucket or os.environ.get("TENCENTCLOUD_COS_BUCKET")
    region = args.region or os.environ.get("TENCENTCLOUD_COS_REGION") or ""

    # Check required parameters
    if not secret_id or not secret_key:
        print("Error: Missing Tencent Cloud credentials. Please set TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY environment variables, or use --secret-id and --secret-key arguments.", file=sys.stderr)  # NOCA:line-too-long(content cannot be shortened)
        sys.exit(1)

    if not bucket:
        print("Error: Missing COS Bucket configuration. Please set TENCENTCLOUD_COS_BUCKET environment variable, or use --bucket argument.", file=sys.stderr)  # NOCA:line-too-long(content cannot be shortened)
        sys.exit(1)

    # If local-file is not specified, default to saving as the same filename in current directory
    local_file = args.local_file
    if not local_file:
        local_file = "./" + os.path.basename(args.cos_input_key)
        if args.verbose:
            print(f"--local-file not specified, using default: {local_file}")

    # Execute download
    result = download_file(
        cos_key=args.cos_input_key,
        local_file=local_file,
        bucket=bucket,
        region=region,
        secret_id=secret_id,
        secret_key=secret_key,
        verbose=args.verbose
    )

    if result:
        print("\n=== Download Successful ===")
        print(f"Bucket: {result['Bucket']}")
        print(f"Key: {result['Key']}")
        print(f"Local file: {result['LocalFile']}")
        print(f"Size: {result['Size'] / 1024 / 1024:.2f} MB")
        print(f"URL: {result['URL']}")
        return 0
    else:
        print("\n=== Download Failed ===", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
