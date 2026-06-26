#!/usr/bin/env python3
"""
Reliable SAP Business Accelerator Hub API spec downloader.

Uses environment-variable login with Playwright Chromium.
Downloads JSON/YAML/EDMX for one or more API IDs from authenticated Hub endpoints.
"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import re
import shutil
import sys
import time
from dataclasses import dataclass
from typing import Dict, List, Tuple


TYPE_TO_SUFFIX = {
    "JSON": "openapi.json",
    "YAML": "openapi.yaml",
    "EDMX": "odata.edmx",
}

DEFAULT_OUTPUT_DIR = "/usr/download"
DEFAULT_BROWSER = "chromium"
DEFAULT_PROFILE_DIR = "/tmp/pw_sap_download/chromium-user-data"


@dataclass
class DownloadResult:
    ok: bool
    output_file: str = ""
    bytes_written: int = 0
    error: str = ""
    endpoint: str = ""


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser()
    ap.add_argument("--api-id", action="append", default=[], help="Repeatable API ID")
    ap.add_argument("--api-id-file", help="Text file with one API ID per line", default=None)
    ap.add_argument("--types", default="JSON,YAML,EDMX", help="Comma-separated: JSON,YAML,EDMX")
    ap.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    ap.add_argument("--headful", action="store_true", help="Run browser with UI (default headless)")
    ap.add_argument("--retries", type=int, default=3)
    ap.add_argument("--timeout-seconds", type=int, default=60)
    ap.add_argument("--sleep-between-retries", type=float, default=1.5)
    ap.add_argument("--json-report", default="", help="Write full report to JSON file")
    ap.add_argument("--username-env", default="SAP_HUB_USERNAME")
    ap.add_argument("--password-env", default="SAP_HUB_PASSWORD")
    ap.add_argument("--probe-api-id", default="WAREHOUSEORDER_0001")
    return ap.parse_args()


def load_api_ids(args: argparse.Namespace) -> List[str]:
    ids = [x.strip() for x in args.api_id if x and x.strip()]
    if args.api_id_file:
        p = pathlib.Path(args.api_id_file)
        if not p.exists():
            raise SystemExit(f"--api-id-file not found: {p}")
        for line in p.read_text(encoding="utf-8", errors="ignore").splitlines():
            s = line.strip()
            if s and not s.startswith("#"):
                ids.append(s)
    deduped = []
    seen = set()
    for api_id in ids:
        if api_id not in seen:
            seen.add(api_id)
            deduped.append(api_id)
    if not deduped:
        raise SystemExit("No API IDs provided. Use --api-id or --api-id-file.")
    return deduped


def parse_types(raw: str) -> List[str]:
    parts = [x.strip().upper() for x in raw.split(",") if x.strip()]
    if not parts:
        raise SystemExit("No valid --types.")
    bad = [x for x in parts if x not in TYPE_TO_SUFFIX]
    if bad:
        raise SystemExit(f"Unsupported types: {bad}. Allowed: {list(TYPE_TO_SUFFIX)}")
    out = []
    seen = set()
    for x in parts:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def init_clean_profile(dst: str) -> None:
    dst_path = pathlib.Path(dst)
    if dst_path.exists():
        shutil.rmtree(dst_path)
    dst_path.mkdir(parents=True, exist_ok=True)


def is_login_or_html(text: str) -> bool:
    t = (text or "").strip().lower()
    if t.startswith("<!doctype html") or t.startswith("<html"):
        return True
    hints = [
        "accounts.sap.com/oauth2/authorize",
        "sign in",
        "sap business accelerator hub: sign in",
    ]
    return any(h in t for h in hints)


def validate_payload(payload_type: str, text: str) -> Tuple[bool, str]:
    if not text or len(text) < 20:
        return False, "empty_or_too_short"
    if is_login_or_html(text):
        return False, "html_login_page"

    if payload_type == "JSON":
        try:
            obj = json.loads(text)
        except Exception:
            return False, "invalid_json"
        if isinstance(obj, dict) and ("openapi" in obj or "swagger" in obj):
            return True, ""
        return False, "json_missing_openapi_or_swagger"

    if payload_type == "YAML":
        head = text[:400].lower()
        if "openapi:" in head or "swagger:" in head:
            return True, ""
        return False, "yaml_missing_openapi_or_swagger"

    if payload_type == "EDMX":
        head = text[:800].lower()
        if "<edmx:edmx" in head or ("<edmx" in head and "xmlns:edmx" in head):
            return True, ""
        if "<?xml" in head and "<edmx" in text.lower():
            return True, ""
        return False, "invalid_edmx_signature"

    return False, "unknown_type"


def endpoint_for(api_id: str, payload_type: str) -> str:
    return (
        "https://hub.sap.com/odata/1.0/catalog.svc/"
        f"APIContent.APIs('{api_id}')/$value?type={payload_type}&attachment=true"
    )


def ensure_hub_reachable(context) -> None:
    page = context.new_page()
    try:
        page.goto("https://hub.sap.com", wait_until="domcontentloaded", timeout=45000)
    finally:
        page.close()


def read_credentials(username_env: str, password_env: str) -> Tuple[str, str]:
    return (
        os.environ.get(username_env, "").strip(),
        os.environ.get(password_env, "").strip(),
    )


def probe_authenticated(context, probe_api_id: str, timeout_ms: int) -> Tuple[bool, str]:
    try:
        resp = context.request.get(endpoint_for(probe_api_id, "JSON"), timeout=timeout_ms)
        body = resp.text()
        if resp.status == 200 and not is_login_or_html(body):
            return True, ""
        if is_login_or_html(body):
            return False, "html_login_page"
        return False, f"http_{resp.status}"
    except Exception as e:  # noqa: BLE001
        return False, f"probe_exception:{e}"


def _first_locator(page, selectors: List[str]):
    for sel in selectors:
        loc = page.locator(sel).first
        try:
            if loc.count() > 0:
                return loc
        except Exception:
            continue
    return None


def try_auto_login(context, username: str, password: str, timeout_ms: int) -> Tuple[bool, str]:
    if not username or not password:
        return False, "missing_credentials"

    page = context.new_page()
    try:
        page.goto(
            "https://hub.sap.com/api/WAREHOUSEORDER_0001/overview",
            wait_until="domcontentloaded",
            timeout=timeout_ms,
        )
        page.wait_for_timeout(1200)

        # If not redirected to SAP ID login, try clicking login entry points.
        if "accounts.sap.com" not in page.url.lower():
            for sel in [
                "a[aria-label*='login' i]",
                "button[aria-label*='login' i]",
                "a[href*='accounts.sap.com']",
                "a[href*='oauth2/authorize']",
            ]:
                loc = page.locator(sel).first
                try:
                    if loc.count() > 0:
                        loc.click(timeout=3000)
                        page.wait_for_timeout(1200)
                        break
                except Exception:
                    continue

        # Handle popup login page if exists.
        if "accounts.sap.com" not in page.url.lower():
            for p in context.pages:
                try:
                    if "accounts.sap.com" in (p.url or "").lower():
                        page = p
                        break
                except Exception:
                    continue

        if "accounts.sap.com" not in page.url.lower():
            return False, "login_page_not_reached"

        user = _first_locator(
            page,
            [
                "input[type='email']",
                "input[autocomplete='username']",
                "input[placeholder*='Email' i]",
                "input[placeholder*='User ID' i]",
                "input[name*='user' i]",
            ],
        )
        pwd = _first_locator(
            page,
            [
                "input[type='password']",
                "input[autocomplete='current-password']",
                "input[name*='pass' i]",
            ],
        )
        if user is None or pwd is None:
            return False, "login_fields_not_found"

        user.fill(username, timeout=5000)
        pwd.fill(password, timeout=5000)

        btn = _first_locator(
            page,
            [
                "button:has-text('Continue')",
                "button:has-text('Sign In')",
                "button[type='submit']",
                "input[type='submit']",
            ],
        )
        if btn is None:
            return False, "submit_button_not_found"

        btn.click(timeout=6000)
        page.wait_for_timeout(3500)

        # MFA or additional challenge can still keep user on accounts.sap.com.
        if "accounts.sap.com" in page.url.lower():
            return False, "still_on_accounts_after_submit"

        return True, ""
    except Exception as e:  # noqa: BLE001
        return False, f"login_exception:{e}"
    finally:
        try:
            page.close()
        except Exception:
            pass


def download_one(context, out_dir: pathlib.Path, api_id: str, payload_type: str, retries: int, timeout_ms: int, sleep_s: float) -> DownloadResult:
    endpoint = endpoint_for(api_id, payload_type)
    suffix = TYPE_TO_SUFFIX[payload_type]
    out_file = out_dir / f"{api_id}_{suffix}"

    last_error = "unknown"
    for attempt in range(1, retries + 1):
        try:
            resp = context.request.get(endpoint, timeout=timeout_ms)
            status = resp.status
            body = resp.text()
            if status != 200:
                last_error = f"http_{status}"
            else:
                ok, reason = validate_payload(payload_type, body)
                if ok:
                    out_file.write_text(body, encoding="utf-8")
                    return DownloadResult(
                        ok=True,
                        output_file=str(out_file),
                        bytes_written=len(body.encode("utf-8")),
                        endpoint=endpoint,
                    )
                last_error = reason
        except Exception as e:  # noqa: BLE001
            last_error = f"exception:{e}"

        if attempt < retries:
            time.sleep(sleep_s * attempt)

    return DownloadResult(ok=False, error=last_error, endpoint=endpoint)


def main() -> int:
    args = parse_args()
    api_ids = load_api_ids(args)
    payload_types = parse_types(args.types)
    out_dir = pathlib.Path(os.path.expanduser(args.output_dir))
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except PermissionError as e:
        raise SystemExit(
            f"Cannot create output dir '{out_dir}' (permission denied). "
            "Create it first (for example: sudo mkdir -p /usr/download && sudo chown \"$USER\":staff /usr/download) "
            "or pass --output-dir to a writable path."
        ) from e

    profile_path = DEFAULT_PROFILE_DIR
    init_clean_profile(profile_path)
    timeout_ms = max(10, args.timeout_seconds) * 1000
    username, password = read_credentials(args.username_env, args.password_env)
    if not username or not password:
        raise SystemExit(
            f"Missing required credentials: set {args.username_env} and {args.password_env}."
        )

    try:
        from playwright.sync_api import sync_playwright
    except Exception as e:  # noqa: BLE001
        raise SystemExit(
            "Python Playwright is required. Install with:\n"
            "  python3 -m pip install playwright\n"
            "  python3 -m playwright install chromium\n"
            f"Import error: {e}"
        )

    report: Dict[str, Dict[str, Dict[str, object]]] = {}
    precheck: Dict[str, object] = {}

    with sync_playwright() as p:
        launch_kwargs = {
            "headless": not args.headful,
            "ignore_default_args": ["--use-mock-keychain", "--password-store=basic"],
        }
        context = p.chromium.launch_persistent_context(profile_path, **launch_kwargs)
        try:
            ensure_hub_reachable(context)
            login_ok, login_reason = try_auto_login(
                context=context,
                username=username,
                password=password,
                timeout_ms=timeout_ms,
            )
            if not login_ok:
                raise SystemExit(f"Automatic login failed: {login_reason}")
            probe_ok, probe_reason = probe_authenticated(context, args.probe_api_id, timeout_ms)

            precheck = {
                "auth_mode": "env",
                "browser": DEFAULT_BROWSER,
                "probe_api_id": args.probe_api_id,
                "authenticated": probe_ok,
                "reason": probe_reason,
                "username_env": args.username_env,
                "password_env": args.password_env,
                "username_present": bool(username),
                "password_present": bool(password),
            }

            for api_id in api_ids:
                report[api_id] = {}
                for payload_type in payload_types:
                    res = download_one(
                        context=context,
                        out_dir=out_dir,
                        api_id=api_id,
                        payload_type=payload_type,
                        retries=max(1, args.retries),
                        timeout_ms=timeout_ms,
                        sleep_s=max(0.0, args.sleep_between_retries),
                    )
                    report[api_id][payload_type] = {
                        "ok": res.ok,
                        "file": res.output_file,
                        "bytes": res.bytes_written,
                        "error": res.error,
                        "endpoint": res.endpoint,
                    }
        finally:
            context.close()

    failures = []
    for api_id, per_type in report.items():
        for payload_type, item in per_type.items():
            if not item["ok"]:
                failures.append((api_id, payload_type, item["error"]))

    hint = ""
    if failures:
        total_attempts = sum(len(x) for x in report.values())
        html_failures = sum(1 for _, _, err in failures if err == "html_login_page")
        if total_attempts > 0 and html_failures == len(failures) == total_attempts:
            hint = (
                "All downloads failed authentication or payload validation. "
                "Verify SAP_HUB_USERNAME/SAP_HUB_PASSWORD and retry."
            )

    summary = {
        "api_ids": api_ids,
        "types": payload_types,
        "output_dir": str(out_dir),
        "failures": failures,
        "hint": hint,
        "precheck": precheck,
        "report": report,
    }

    text = json.dumps(summary, ensure_ascii=False, indent=2)
    print(text)
    if args.json_report:
        pathlib.Path(args.json_report).write_text(text, encoding="utf-8")

    return 2 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
