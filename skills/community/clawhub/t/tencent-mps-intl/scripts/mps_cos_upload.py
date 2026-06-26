#!/usr/bin/env python3
"""
Tencent Cloud COS File Upload Script

Features:
  Uses the Tencent Cloud COS Python SDK to upload local files to a COS Bucket.

Usage:
  # Simplest usage (cos-input-key is omitted, automatically uses input/<filename>)
  python mps_cos_upload.py --local-file /path/to/local/file.mp4

  # Manually specify cos-input-key
  python mps_cos_upload.py --local-file /path/to/local/file.mp4 --cos-input-key input/video.mp4

  # Specify bucket and region (overrides environment variables)
  python mps_cos_upload.py --local-file /path/to/file.mp4 --cos-input-key input/video.mp4 \
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
        description="Tencent Cloud COS File Upload Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simplest usage (cos-input-key omitted, automatically uses input/<filename>)
  python mps_cos_upload.py --local-file ./video.mp4

  # Manually specify cos-input-key
  python mps_cos_upload.py --local-file ./video.mp4 --cos-input-key input/video.mp4

  # Specify bucket and region
  python mps_cos_upload.py --local-file ./video.mp4 --cos-input-key input/video.mp4 \\
      --bucket mybucket-125xxx --region ap-guangzhou
        """
    )

    parser.add_argument(
        "--local-file", "-f",
        required=True,
        help="Local file path (required)"
    )
    parser.add_argument(
        "--cos-input-key", "-k",
        default=None,
        help="COS object key (Key), e.g. input/video.mp4 (default: /input/<local filename>)"
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


def upload_file(local_file, cos_key, bucket, region, secret_id, secret_key, verbose=False):
    """
    Upload a file to COS

    Args:
        local_file: Local file path
        cos_key: COS object key
        bucket: COS Bucket name
        region: COS Bucket region
        secret_id: Tencent Cloud SecretId
        secret_key: Tencent Cloud SecretKey
        verbose: Whether to show detailed logs

    Returns:
        dict: Upload result, including ETag and URL
    """
    # Check if local file exists
    if not os.path.isfile(local_file):
        print(f"Error: Local file does not exist: {local_file}", file=sys.stderr)
        return None

    # Get file size
    file_size = os.path.getsize(local_file)
    if verbose:
        print(f"Local file: {local_file}")
        print(f"File size: {file_size / 1024 / 1024:.2f} MB")
        print(f"Target Bucket: {bucket}")
        print(f"Target Region: {region}")
        print(f"COS Key: {cos_key}")

    # Create COS client
    config = CosConfig(
        Region=region,
        SecretId=secret_id,
        SecretKey=secret_key
    )
    client = CosS3Client(config)

    # Upload file
    try:
        if verbose:
            print(f"Starting upload...")

        response = client.upload_file(
            Bucket=bucket,
            LocalFilePath=local_file,
            Key=cos_key,
            PartSize=10,  # Part size: 10 MB
            MAXThread=5,  # Maximum thread count
            EnableMD5=False
        )

        # Build file URL
        url = f"https://{bucket}.cos.{region}.myqcloud.com/{cos_key.lstrip('/')}"

        # Generate temporary access URL (pre-signed URL, valid for 1 hour)
        presigned_url = None
        try:
            presigned_url = client.get_presigned_url(
                Method='GET',
                Bucket=bucket,
                Key=cos_key,
                Expired=3600  # Valid for 1 hour
            )
            if verbose:
                print(f"Pre-signed URL generated (valid for 1 hour)")
        except Exception as e:  # NOCA:broad-except(CLI script needs to handle all exceptions)
            if verbose:
                print(f"Failed to generate pre-signed URL: {e}")

        result = {
            "ETag": response.get("ETag", ""),
            "Key": cos_key,
            "Bucket": bucket,
            "Region": region,
            "URL": url,
            "PresignedURL": presigned_url,
            "Size": file_size
        }

        if verbose:
            print(f"Upload successful!")
            print(f"ETag: {result['ETag']}")
            print(f"URL: {url}")

        return result

    except Exception as e:  # NOCA:broad-except(CLI script needs to handle all exceptions)
        print(f"Upload failed: {e}", file=sys.stderr)
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

    # If cos-key is not specified, default to /input/<local filename>
    cos_key = args.cos_input_key
    if not cos_key:
        cos_key = "input/" + os.path.basename(args.local_file)
        if args.verbose:
            print(f"--cos-input-key not specified, using default: {cos_key}")

    # Execute upload
    result = upload_file(
        local_file=args.local_file,
        cos_key=cos_key,
        bucket=bucket,
        region=region,
        secret_id=secret_id,
        secret_key=secret_key,
        verbose=args.verbose
    )

    if result:
        print("\n=== Upload Successful ===")
        print(f"File: {args.local_file}")
        print(f"Size: {result['Size'] / 1024 / 1024:.2f} MB")
        print(f"Bucket: {result['Bucket']}")
        print(f"Key: {result['Key']}")
        print(f"Permanent URL: {result['URL']}")
        if result.get('PresignedURL'):
            print(f"Temporary URL: {result['PresignedURL']}")
            print("\n=== AIGC Script Arguments (using temporary URL) ===")
            print(f"--image-url '{result['PresignedURL']}'")
        print("\n=== COS Path Format (for audio/video processing scripts) ===")
        print(f"--cos-input-bucket {result['Bucket']} --cos-input-region {result['Region']} --cos-input-key {result['Key']}")  # NOCA:line-too-long(content cannot be shortened)
        print("\n=== AIGC Image/Video Script Arguments (using COS path, recommended) ===")
        print(f"--image-cos-bucket {result['Bucket']} --image-cos-region {result['Region']} --image-cos-key {result['Key']}")  # NOCA:line-too-long(line cannot be shortened)
        print("\n=== AIGC Video Script Arguments (first frame image using COS path) ===")
        print(f"--image-cos-bucket {result['Bucket']} --image-cos-region {result['Region']} --image-cos-key {result['Key']}")  # NOCA:line-too-long(line cannot be shortened)
        return 0
    else:
        print("\n=== Upload Failed ===", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
