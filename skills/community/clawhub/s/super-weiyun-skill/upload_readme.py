#!/usr/bin/env python3
"""Upload README.md to Weiyun - interactive login + upload script."""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from weiyun_skills.login import qrcode_login, cookies_login, load_cookies
from weiyun_skills.client import WeiyunClient


def main():
    readme_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md")
    cookies_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cookies.json")

    if not os.path.isfile(readme_path):
        print(f"[ERROR] README.md not found at: {readme_path}")
        sys.exit(1)

    print("=" * 60)
    print("  Weiyun Skills - Upload README.md")
    print("=" * 60)
    print(f"  File: {readme_path}")
    print(f"  Size: {os.path.getsize(readme_path)} bytes")
    print()

    # Step 1: Check if already logged in
    saved = load_cookies(cookies_path)
    if saved and saved.get("cookies_str"):
        print("[*] Found saved cookies, verifying...")
        client = WeiyunClient(cookies_path=cookies_path)
        space = client.get_space_info()
        if space["success"]:
            print(f"[✓] Already logged in as: {saved.get('uin', 'unknown')}")
        else:
            print("[*] Saved cookies expired, need to re-login.")
            saved = {}

    # Step 2: Login if needed
    if not saved or not saved.get("cookies_str"):
        print()
        print("Choose login method:")
        print("  1) QR code scan (recommended)")
        print("  2) Paste cookies from browser")
        print()

        choice = input("Enter choice [1/2]: ").strip()

        if choice == "2":
            print()
            print("Steps to get cookies:")
            print("  1. Open https://www.weiyun.com in browser and login")
            print("  2. Press F12 -> Network tab -> click any request")
            print("  3. Copy the 'Cookie:' header value")
            print()
            cookies_str = input("Paste cookies here: ").strip()
            result = cookies_login(cookies_str, save_path=cookies_path)
        else:
            result = qrcode_login(save_path=cookies_path)

        if not result["success"]:
            print(f"\n[ERROR] Login failed: {result['message']}")
            sys.exit(1)

        print(f"\n[✓] Login successful! Cookies saved to: {cookies_path}")

    # Step 3: Upload README.md
    print()
    print("-" * 60)
    print("[*] Uploading README.md to Weiyun root directory...")
    print("-" * 60)

    client = WeiyunClient(cookies_path=cookies_path)
    result = client.upload_file(readme_path, "/README.md", overwrite=True)

    if result["success"]:
        data = result["data"]
        print()
        print("=" * 60)
        print("  ✅ Upload successful!")
        print(f"  📄 File: {data.get('name', 'README.md')}")
        print(f"  📦 Size: {data.get('size', 0)} bytes")
        print(f"  📂 Path: {data.get('remote_path', '/README.md')}")
        print(f"  🔑 MD5:  {data.get('md5', 'N/A')}")
        print(f"  🕐 Time: {data.get('uploaded_at', 'N/A')}")
        print("=" * 60)
    else:
        print(f"\n[ERROR] Upload failed: {result['message']}")
        print(f"  Error code: {result.get('error_code', 'UNKNOWN')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
