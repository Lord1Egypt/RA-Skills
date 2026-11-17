#!/usr/bin/env python3
"""Batch upload images to WeChat permanent material library and replace HTML placeholders.

Usage:
    python upload_to_wechat.py <html_file> <images_dir> <mapping_json> [--config <config_json>]

mapping_json format:
[
    ["PLACEHOLDER_NAME", "image_filename.png"],
    ...
]

The script:
1. Obtains WeChat access_token
2. Uploads each image from images_dir via material/add_material
3. Replaces data-src="PLACEHOLDER_NAME" with src="https_cdn_url" in HTML
4. Saves updated HTML back
"""
import sys, os, json, io

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

import argparse
import requests


def get_credentials(config_path=None):
    """Get WeChat credentials."""
    app_id = os.environ.get("WECHAT_APP_ID") or os.environ.get("WECHAT_APPID")
    app_secret = os.environ.get("WECHAT_APP_SECRET") or os.environ.get("WECHAT_SECRET")

    if (not app_id or not app_secret) and config_path and os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        app_id = cfg.get("appid") or cfg.get("app_id", app_id)
        app_secret = cfg.get("secret") or cfg.get("app_secret", app_secret)

    if not app_id or not app_secret:
        import subprocess
        try:
            ps = subprocess.run(
                ['powershell', '-Command',
                 '[Environment]::GetEnvironmentVariable("WECHAT_APP_SECRET","User")'],
                capture_output=True, text=True, timeout=10
            )
            app_secret = ps.stdout.strip() or app_secret
            ps2 = subprocess.run(
                ['powershell', '-Command',
                 '[Environment]::GetEnvironmentVariable("WECHAT_APP_ID","User")'],
                capture_output=True, text=True, timeout=10
            )
            app_id = ps2.stdout.strip() or app_id
        except Exception:
            pass

    return app_id, app_secret


def get_access_token(app_id, app_secret):
    r = requests.post(
        "https://api.weixin.qq.com/cgi-bin/stable_token",
        json={"grant_type": "client_credential", "appid": app_id, "secret": app_secret},
        timeout=30
    )
    data = r.json()
    token = data.get("access_token", "")
    if not token:
        print(f"[ERROR] Token failed: {data}", file=sys.stderr)
        sys.exit(1)
    return token


def upload_image(token, filepath):
    """Upload one image. Returns (media_id, cdn_url)."""
    fname = os.path.basename(filepath)
    size = os.path.getsize(filepath)

    with open(filepath, 'rb') as f:
        r = requests.post(
            f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={token}&type=image",
            files={'media': (fname, f, 'image/png')},
            timeout=120
        )
    result = r.json()

    if 'media_id' not in result:
        print(f"  [FAIL] {result}", file=sys.stderr)
        return None, None

    cdn_url = result.get('url', '')
    # Ensure HTTPS
    if cdn_url.startswith('http://'):
        cdn_url = cdn_url.replace('http://', 'https://', 1)

    return result['media_id'], cdn_url


def main():
    parser = argparse.ArgumentParser(description="Upload images to WeChat and update HTML")
    parser.add_argument("html_file", help="Path to HTML article file with data-src placeholders")
    parser.add_argument("images_dir", help="Directory containing image files")
    parser.add_argument("mapping_file", help="JSON mapping file: [[placeholder, filename], ...]")
    parser.add_argument("--config", help="Path to JSON config with appid/secret", default=None)
    args = parser.parse_args()

    # Load mapping
    with open(args.mapping_file, 'r', encoding='utf-8') as f:
        mapping = json.load(f)
    print(f"[INFO] {len(mapping)} images to upload")

    # Get credentials
    app_id, app_secret = get_credentials(args.config)
    if not app_id or not app_secret:
        print("[ERROR] No WeChat credentials found", file=sys.stderr)
        sys.exit(1)

    token = get_access_token(app_id, app_secret)
    print(f"[OK] Token obtained: {token[:16]}...")

    # Upload images
    urls = {}
    for placeholder, fname in mapping:
        img_path = os.path.join(args.images_dir, fname)
        if not os.path.exists(img_path):
            print(f"[WARN] File not found: {img_path}, skipping {placeholder}", file=sys.stderr)
            continue

        print(f"[UPLOAD] {fname} -> {placeholder}")
        media_id, cdn_url = upload_image(token, img_path)

        if media_id:
            urls[placeholder] = (media_id, cdn_url)
            print(f"  [OK] {cdn_url[:70]}...")
        else:
            print(f"  [FAIL] Upload failed for {fname}", file=sys.stderr)
            sys.exit(1)

    # Read and update HTML
    with open(args.html_file, 'r', encoding='utf-8') as f:
        html = f.read()

    for placeholder, (media_id, cdn_url) in urls.items():
        html = html.replace(f'data-src="{placeholder}"', f'src="{cdn_url}"')

    with open(args.html_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"\n[DONE] {len(urls)} images uploaded, HTML updated: {args.html_file}")

    # Save url map for reference
    url_map_path = os.path.join(os.path.dirname(args.html_file), "image_urls.json")
    with open(url_map_path, 'w', encoding='utf-8') as f:
        json.dump({k: v[1] for k, v in urls.items()}, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
