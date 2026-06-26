#!/usr/bin/env python3
"""
Deploy a prepared site directory to Netlify as a zip upload.

Requires:
- NETLIFY_AUTH_TOKEN
- optional NETLIFY_SITE_ID for existing sites

Example:
  NETLIFY_AUTH_TOKEN=... \
  python3 scripts/netlify_zip_deploy.py ./site-output

If NETLIFY_SITE_ID is missing, the script can create a new site first and then
persist the returned non-secret site identifiers to `.website-manager/deploy.json`.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import time
import urllib.error
import urllib.request
import zipfile
from pathlib import Path


API_ROOT = "https://api.netlify.com/api/v1"
DEFAULT_SAVE_JSON = ".website-manager/deploy.json"


def build_zip(source_dir: Path) -> Path:
    tmp = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
    tmp.close()
    zip_path = Path(tmp.name)
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(source_dir.rglob("*")):
            if path.is_file():
                archive.write(path, path.relative_to(source_dir))
    return zip_path


def request(method: str, url: str, token: str, body: bytes | None = None, content_type: str | None = None) -> dict:
    headers = {"Authorization": f"Bearer {token}"}
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=60) as response:
        raw = response.read()
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))


def create_site(token: str, account_slug: str | None, site_name: str | None) -> dict:
    payload: dict = {}
    if site_name:
        payload["name"] = site_name
    url = f"{API_ROOT}/sites" if not account_slug else f"{API_ROOT}/{account_slug}/sites"
    return request("POST", url, token, json.dumps(payload).encode("utf-8"), "application/json")


def create_deploy(site_id: str, token: str, zip_bytes: bytes, draft: bool) -> dict:
    url = f"{API_ROOT}/sites/{site_id}/deploys"
    if draft:
        url += "?draft=true"
    return request("POST", url, token, zip_bytes, "application/zip")


def poll_deploy(deploy_id: str, token: str, timeout_seconds: int) -> dict:
    url = f"{API_ROOT}/deploys/{deploy_id}"
    deadline = time.time() + timeout_seconds
    while time.time() < deadline:
        payload = request("GET", url, token)
        state = payload.get("state")
        if state in {"ready", "error"}:
            return payload
        time.sleep(3)
    raise TimeoutError(f"Timed out waiting for deploy {deploy_id}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Deploy a site directory to Netlify as a zip upload.")
    parser.add_argument("site_dir", help="Built site directory to deploy")
    parser.add_argument("--draft", action="store_true", help="Create a draft deploy")
    parser.add_argument("--timeout", type=int, default=300, help="Polling timeout in seconds")
    parser.add_argument(
        "--save-json",
        default=DEFAULT_SAVE_JSON,
        help="Where to save the resulting non-secret Netlify IDs and URLs. Use '-' to disable.",
    )
    args = parser.parse_args()

    token = os.environ.get("NETLIFY_AUTH_TOKEN")
    site_id = os.environ.get("NETLIFY_SITE_ID")
    account_slug = os.environ.get("NETLIFY_ACCOUNT_SLUG")
    site_name = os.environ.get("NETLIFY_SITE_NAME")
    if not token or not site_id:
        if not token:
            print("ERROR: NETLIFY_AUTH_TOKEN must be set.", file=sys.stderr)
            return 2

    site_dir = Path(args.site_dir).resolve()
    if not site_dir.exists() or not site_dir.is_dir():
        print(f"ERROR: {site_dir} is not a directory.", file=sys.stderr)
        return 2

    zip_path = build_zip(site_dir)
    try:
        site_payload: dict | None = None
        if not site_id:
            site_payload = create_site(token, account_slug, site_name)
            site_id = site_payload.get("id")
            if not site_id:
                print("ERROR: Netlify did not return a site id.", file=sys.stderr)
                return 1
        zip_bytes = zip_path.read_bytes()
        deploy = create_deploy(site_id, token, zip_bytes, args.draft)
        deploy_id = deploy.get("id")
        if not deploy_id:
            print("ERROR: Netlify did not return a deploy id.", file=sys.stderr)
            return 1
        final = poll_deploy(deploy_id, token, args.timeout)
        state = final.get("state", "unknown")
        result = {
            "site_id": site_id,
            "site_name": (site_payload or {}).get("name"),
            "site_url": (site_payload or {}).get("url"),
            "deploy_id": deploy_id,
            "state": state,
            "deploy_url": final.get("deploy_url"),
            "ssl_url": final.get("ssl_url"),
        }
        if args.save_json != "-":
            save_path = Path(args.save_json)
            save_path.parent.mkdir(parents=True, exist_ok=True)
            save_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(result, indent=2))
        return 0 if state == "ready" else 1
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"HTTP ERROR {exc.code}: {detail}", file=sys.stderr)
        return 1
    finally:
        zip_path.unlink(missing_ok=True)


if __name__ == "__main__":
    raise SystemExit(main())
