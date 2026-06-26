#!/usr/bin/env python3
"""
Upload files to UCloud US3 using Python SDK and get download URL.

Features:
    - Timestamp and MD5-based filename (format: YYYYMMDD_HHMMSS_md5.ext)
    - File size limit check
    - Signed download URL (7 days)
    - Direct URL output for easy sharing
"""

import sys
import os
import hashlib
from datetime import datetime

try:
    from ufile import filemanager, config
except ImportError:
    print("Installing ufile SDK...")
    os.system("pip3 install -q ufile")
    from ufile import filemanager, config

# Read from environment variables
PUBLIC_KEY = os.environ.get("US3_PUBLIC_KEY")
PRIVATE_KEY = os.environ.get("US3_PRIVATE_KEY")
BUCKET = os.environ.get("US3_BUCKET")

# Max file size (default 50MB)
MAX_FILE_SIZE_MB = int(os.environ.get("US3_MAX_FILE_SIZE_MB", "50"))
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Check required environment variables
if not PUBLIC_KEY or not PRIVATE_KEY or not BUCKET:
    print("Error: Missing required environment variables.")
    print()
    print("Please set the following environment variables:")
    print("  export US3_PUBLIC_KEY='your-public-key'")
    print("  export US3_PRIVATE_KEY='your-private-key'")
    print("  export US3_BUCKET='bucket-name.region.ufileos.com'  # or just 'bucket-name'")
    print("  export US3_ENDPOINT='cn-sh2.ufileos.com'  # optional if BUCKET is full domain")
    print("  export US3_MAX_FILE_SIZE_MB='50'  # optional, defaults to 50MB")
    sys.exit(1)

# Parse bucket configuration
# BUCKET can be either:
#   - Full domain: "bucket-name.region.ufileos.com"
#   - Just bucket name: "bucket-name" (requires US3_ENDPOINT)
if '.' in BUCKET:
    # Full domain format
    parts = BUCKET.split('.', 1)
    BUCKET_NAME = parts[0]
    ENDPOINT = parts[1]
else:
    # Just bucket name
    BUCKET_NAME = BUCKET
    ENDPOINT = os.environ.get("US3_ENDPOINT", "cn-sh2.ufileos.com")

# Set upload suffix to use the correct endpoint with dot separator
config.set_default(uploadsuffix="." + ENDPOINT, downloadsuffix="." + ENDPOINT)

if len(sys.argv) < 2:
    print("Usage: python3 upload_to_us3.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

if not os.path.exists(file_path):
    print(f"Error: File not found: {file_path}")
    sys.exit(1)

# Check file size
file_size = os.path.getsize(file_path)
if file_size > MAX_FILE_SIZE_BYTES:
    file_size_mb = file_size / (1024 * 1024)
    print(f"Error: File size ({file_size_mb:.2f}MB) exceeds maximum allowed size ({MAX_FILE_SIZE_MB}MB)")
    print()
    print("To increase the limit, set the environment variable:")
    print(f"  export US3_MAX_FILE_SIZE_MB='100'  # or your desired size in MB")
    sys.exit(1)

# Generate timestamp and MD5-based filename
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
original_filename = os.path.basename(file_path)
_, ext = os.path.splitext(original_filename)

# Calculate MD5 hash of file content (chunked reading for large files)
md5_hash = hashlib.md5()
with open(file_path, 'rb') as f:
    # Read file in 8KB chunks to avoid memory issues with large files
    for chunk in iter(lambda: f.read(8192), b''):
        md5_hash.update(chunk)
file_hash = md5_hash.hexdigest()

# Create remote filename: YYYYMMDD_HHMMSS_md5.ext
remote_name = f"{timestamp}_{file_hash}{ext}"

print(f"Uploading {os.path.basename(file_path)} to US3...")
print(f"  Bucket: {BUCKET_NAME}.{ENDPOINT}")
print(f"  Remote name: {remote_name}")
print(f"  File size: {file_size / (1024 * 1024):.2f}MB")
print()

handler = filemanager.FileManager(PUBLIC_KEY, PRIVATE_KEY)

ret, resp = handler.putfile(BUCKET_NAME, remote_name, file_path, None)

if resp.status_code == 200:
    print("✓ Upload successful!")
    print()

    # Generate private download URL with signature (expires in 7 days)
    private_url = handler.private_download_url(BUCKET_NAME, remote_name, expires=604800)

    # Add Content-Disposition to force download with original filename
    import urllib.parse
    original_filename = os.path.basename(file_path)
    content_disposition = urllib.parse.quote(f'attachment; filename="{original_filename}"')

    if '?' in private_url:
        download_url = f"{private_url}&response-content-disposition={content_disposition}"
    else:
        download_url = f"{private_url}?response-content-disposition={content_disposition}"

    print("📋 Download URL (valid for 7 days):")
    print(download_url)
    print()
    print("ℹ️  Note:")
    print("   - Click to download file directly (not preview)")
    print("   - URL contains authentication signature (required by US3)")
    print()
    print("━" * 60)
    print(f"📥 下载链接（7天内有效）：")
    print(download_url)
    print("━" * 60)
else:
    error_msg = resp.error if hasattr(resp, 'error') else resp.content
    print(f"✗ Upload failed: {resp.status_code} - {error_msg}")
    sys.exit(1)
