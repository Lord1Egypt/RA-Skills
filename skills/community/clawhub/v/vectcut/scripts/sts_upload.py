#!/usr/bin/env python3
"""STS Upload Script - Upload files to Aliyun OSS via STS credentials."""

import os
import sys
import json
import hmac
import base64
import hashlib
from urllib.parse import quote
from email.utils import formatdate
import requests

BASE_URL = "https://open.vectcut.com"
OSS_ENDPOINT = "oss-cn-hangzhou.aliyuncs.com"


def upload_file(file_path):
    jwt_token = os.getenv("VECTCUT_API_KEY")
    if not jwt_token:
        raise RuntimeError(
            "Environment variable VECTCUT_API_KEY is not set. "
            "Please call the vectcut-login skill first, then retry upload."
        )

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    auth_headers = {"Authorization": f"Bearer {jwt_token}", "Content-Type": "application/json"}

    # Step 1: Init
    print(f"[1/3] Initializing upload for {file_name} ({file_size} bytes)...")
    resp = requests.post(
        f"{BASE_URL}/sts/upload/init",
        headers=auth_headers,
        json={"file_name": file_name, "file_size_bytes": file_size},
        timeout=30,
    )
    body = resp.json()
    if resp.status_code != 200 or not body.get("success"):
        raise RuntimeError(f"upload/init failed: {resp.status_code}, {body}")

    creds = body["credentials"]
    object_key = body["object_key"]
    bucket_name = body["bucket_name"]

    # Step 2: Upload to OSS
    print("[2/3] Uploading to OSS...")
    gmt_date = formatdate(usegmt=True)
    content_type = "application/octet-stream"
    security_token = creds["SecurityToken"]

    string_to_sign = (
        f"PUT\n\n{content_type}\n{gmt_date}\n"
        f"x-oss-security-token:{security_token}\n"
        f"/{bucket_name}/{object_key}"
    )
    digest = hmac.new(
        creds["AccessKeySecret"].encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha1,
    ).digest()
    signature = base64.b64encode(digest).decode("utf-8")

    encoded_key = quote(object_key, safe="/-_.~")
    upload_url = f"https://{bucket_name}.{OSS_ENDPOINT}/{encoded_key}"
    oss_headers = {
        "Date": gmt_date,
        "Content-Type": content_type,
        "x-oss-security-token": security_token,
        "Authorization": f"OSS {creds['AccessKeyId']}:{signature}",
    }

    with open(file_path, "rb") as f:
        resp = requests.put(upload_url, headers=oss_headers, data=f, timeout=120)
    if resp.status_code not in (200, 201):
        raise RuntimeError(f"OSS upload failed: {resp.status_code}, {resp.text}")

    # Step 3: Complete
    print("[3/3] Completing upload...")
    resp = requests.post(
        f"{BASE_URL}/sts/upload/complete",
        headers=auth_headers,
        json={"object_key": object_key},
        timeout=30,
    )
    complete_body = resp.json()
    if resp.status_code != 200 or not complete_body.get("success"):
        raise RuntimeError(f"upload/complete failed: {resp.status_code}, {complete_body}")

    result = {
        "base_url": BASE_URL,
        "bucket_name": bucket_name,
        "local_file": file_path,
        "object_key": object_key,
        "file_size": file_size,
        "public_signed_url": complete_body.get("public_signed_url"),
    }
    print("Upload completed successfully!")
    return result


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python sts_upload.py <file_path>")
        sys.exit(1)

    try:
        result = upload_file(file_path=sys.argv[1])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except (RuntimeError, FileNotFoundError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
