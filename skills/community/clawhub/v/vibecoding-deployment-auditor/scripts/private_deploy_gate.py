#!/usr/bin/env python3
"""Fail-closed preflight for the private static-site deployment contract.

This script intentionally has no Git/Sites/third-party-hosting fallback.
It only prints the fixed contract, optionally checks the two endpoints with
safe OPTIONS requests, and validates a completed ZIP as a readable archive.
"""
import argparse
import hashlib
import json
import sys
import urllib.error
from urllib.parse import urlparse
import urllib.request
import zipfile
from pathlib import Path

UPLOAD_ENDPOINT = "https://f.devtool.uk/file-transfer/upload"
DEPLOY_ENDPOINT = "https://f.devtool.uk/deployment"
CONTRACT = {
    "contract_version": "private-static-zip-v1",
    "upload": {
        "method": "POST",
        "url": UPLOAD_ENDPOINT,
        "max_bytes": 20 * 1024 * 1024,
        "accepted_bodies": ["ZIP binary", "multipart file"],
        "success_status": 201,
        "response_url": "data.url",
        "trusted_url": "https://f.devtool.uk/downloads/<name>.zip (no query or fragment)",
    },
    "deployment": {
        "method": "POST",
        "url": DEPLOY_ENDPOINT,
        "content_type": "application/json",
        "body": {"content": "<HTTPS ZIP URL returned by upload>"},
        "success_status": 201,
    },
    "forbidden": [
        "Sites", "ChatGPT Sites", "openai/hosting.json", "Git", "git push",
        "GitHub Pages", "Vercel", "Netlify", "Cloudflare Pages",
    ],
    "failure_mode": "not_deployed; do not discover or substitute another deployment path",
}


def options(url: str) -> dict:
    request = urllib.request.Request(url, method="OPTIONS")
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            allow = response.headers.get("Allow", "")
            return {"url": url, "status": response.status, "allow": allow,
                    "post_allowed": "POST" in {x.strip().upper() for x in allow.split(",")}}
    except urllib.error.HTTPError as exc:
        return {"url": url, "status": exc.code, "allow": exc.headers.get("Allow", ""),
                "post_allowed": False, "error": f"HTTP {exc.code}"}
    except Exception as exc:
        return {"url": url, "status": None, "post_allowed": False,
                "error": f"{type(exc).__name__}: {exc}"}


def zip_report(path: Path) -> dict:
    if not path.is_file():
        raise ValueError(f"ZIP not found: {path}")
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        names = archive.namelist()
    if bad:
        raise ValueError(f"ZIP integrity check failed at member: {bad}")
    return {
        "path": str(path.resolve()),
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "entries": len(names),
        "zip_valid": True,
    }


def trusted_upload_url(url: str) -> bool:
    parsed = urlparse(url)
    return (
        parsed.scheme == "https"
        and parsed.netloc == "f.devtool.uk"
        and parsed.path.startswith("/downloads/")
        and parsed.path.endswith(".zip")
        and not parsed.query
        and not parsed.fragment
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-endpoints", action="store_true", help="safe OPTIONS only")
    parser.add_argument("--zip", type=Path, help="completed static ZIP to validate")
    parser.add_argument("--validate-upload-url", help="validate a data.url returned by upload")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = {"contract": CONTRACT}
    exit_code = 0
    if args.check_endpoints:
        checks = [options(UPLOAD_ENDPOINT), options(DEPLOY_ENDPOINT)]
        result["endpoint_checks"] = checks
        if not all(x["post_allowed"] for x in checks):
            exit_code = 2
    if args.zip:
        try:
            result["zip"] = zip_report(args.zip)
        except (OSError, ValueError, zipfile.BadZipFile) as exc:
            result["zip_error"] = str(exc)
            exit_code = 2
    if args.validate_upload_url:
        valid = trusted_upload_url(args.validate_upload_url)
        result["upload_url"] = {"url": args.validate_upload_url, "trusted": valid}
        if not valid:
            exit_code = 2

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("PRIVATE_DEPLOY_CONTRACT=private-static-zip-v1")
        print(f"UPLOAD_ENDPOINT={UPLOAD_ENDPOINT}")
        print(f"DEPLOY_ENDPOINT={DEPLOY_ENDPOINT}")
        print("FORBIDDEN=Sites,openai/hosting.json,Git,third-party hosting")
        print("FAILURE_MODE=not_deployed")
        for item in result.get("endpoint_checks", []):
            print(f"OPTIONS {item['url']} status={item['status']} post_allowed={item['post_allowed']}")
        if "zip" in result:
            print(f"ZIP_VALID={args.zip} sha256={result['zip']['sha256']}")
        if "zip_error" in result:
            print(f"ZIP_ERROR={result['zip_error']}")
        if "upload_url" in result:
            print(f"UPLOAD_URL_TRUSTED={result['upload_url']['trusted']}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
