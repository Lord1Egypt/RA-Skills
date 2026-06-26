#!/usr/bin/env python3
"""Quick-generate a video via local dashboard-console API.

Flow:
1) Generate script: POST /video/script/gen
2) Create task:     POST /video/task/create
3) Poll state:      GET  /video/task/state?task_id=...

Auth:
- /video/task/create requires Authorization Bearer JWT (dashboard token)
- script/gen and task/state may not require auth in current code, but we still allow passing token.

Exit codes:
- 0 success
- 2 bad args
- 3 auth/login failed
- 4 request failed / generation failed / timeout
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, Optional, Tuple


DEFAULT_DASHBOARD_BASE_URL = "https://xiaonian.cc"
API_PREFIX = "/employee-console/dashboard/v2/api"


def _http_json(
    method: str,
    url: str,
    body: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout_s: int = 300,
) -> Dict[str, Any]:
    data = None
    req_headers = {"Content-Type": "application/json"}
    if headers:
        req_headers.update(headers)

    if body is not None:
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers=req_headers, method=method.upper())
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} {e.reason}: {raw}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error: {e}") from e


def _login(base_url: str, phone: str, password: str) -> str:
    url = base_url.rstrip("/") + API_PREFIX + "/auth/login"
    resp = _http_json("POST", url, {"phone": phone, "password": password}, timeout_s=60)
    token = resp.get("access_token")
    if not token:
        raise RuntimeError(f"Login failed: {resp}")
    return token


DEFAULT_TOKEN = "atk_ajhhuxTyHciMIxZQ_vt_boqVeG_zTr4Ix9REWuVBXSc"


def _get_token(base_url: str) -> Tuple[Optional[str], Optional[str]]:
    token = os.getenv("DASHBOARD_TOKEN") or DEFAULT_TOKEN
    if token:
        return token, "env:DASHBOARD_TOKEN"

    phone = os.getenv("DASHBOARD_PHONE")
    password = os.getenv("DASHBOARD_PASSWORD")
    if phone and password:
        token = _login(base_url, phone, password)
        return token, "login:DASHBOARD_PHONE+DASHBOARD_PASSWORD"

    return None, None


def _dashboard_ok(resp: Any) -> Tuple[bool, Any]:
    # Dashboard convention: {success: bool, data: ..., message: ...}
    if not isinstance(resp, dict):
        return True, resp
    if resp.get("success") is False:
        return False, resp
    return True, resp


def _download(url: str, out_path: str) -> None:
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=600) as resp:
        data = resp.read()
    with open(out_path, "wb") as f:
        f.write(data)


def main() -> int:
    ap = argparse.ArgumentParser(description="Dashboard video: quick generate final video")
    ap.add_argument("--base-url", default=os.getenv("DASHBOARD_BASE_URL", DEFAULT_DASHBOARD_BASE_URL), help="Dashboard base url")

    ap.add_argument("--request", required=True, help="User requirement / request_desc")
    ap.add_argument("--video-type", default="AUTO", help="Video type passed through to backend (string). Default AUTO")
    ap.add_argument("--duration", type=int, default=15, help="Duration seconds")
    ap.add_argument("--has-subtitle", action="store_true", default=True, help="Include subtitles (default on)")
    ap.add_argument("--no-subtitle", dest="has_subtitle", action="store_false", help="Disable subtitles")

    ap.add_argument("--orientation", default="portrait", choices=["portrait", "landscape"], help="portrait or landscape")
    ap.add_argument("--hd", action="store_true", help="Enable HD / upsample if supported")

    ap.add_argument("--image-url", default="", help="Optional BOS image URL to keep product consistent")

    ap.add_argument("--poll-interval", type=float, default=3.0, help="Seconds between polls")
    ap.add_argument("--timeout", type=int, default=3600, help="Total timeout seconds")

    ap.add_argument("--out", default="", help="Optional: download video to this path")
    ap.add_argument("--json", action="store_true", help="Print full JSON output")

    args = ap.parse_args()

    base_url = args.base_url.rstrip("/")
    api_base = base_url + API_PREFIX

    # token required for task/create
    token, _src = _get_token(base_url)
    if not token:
        sys.stderr.write("Missing auth. Set env DASHBOARD_TOKEN, or set DASHBOARD_PHONE + DASHBOARD_PASSWORD for login.\n")
        return 3

    headers_auth = {"Authorization": f"Bearer {token}"}

    # 1) script
    try:
        resp = _http_json(
            "POST",
            api_base + "/video/script/gen",
            body={
                "video_type": args.video_type,
                "request_desc": args.request,
                "duration": int(args.duration),
                "has_subtitle": bool(args.has_subtitle),
            },
            headers=headers_auth,
            timeout_s=300,
        )
        ok, payload = _dashboard_ok(resp)
        if not ok:
            raise RuntimeError(f"script/gen not successful: {payload}")
        data = payload.get("data") if isinstance(payload, dict) else None
        script = (data or {}).get("script") if isinstance(data, dict) else None
        if not script:
            raise RuntimeError(f"Unexpected script/gen response: {payload}")
    except Exception as e:
        sys.stderr.write(f"Script gen failed: {e}\n")
        return 4

    # 2) create task
    try:
        body = {
            "video_type": args.video_type,
            "request_desc": args.request,
            "script": script,
            "duration": int(args.duration),
            "image_file_path": (args.image_url or None),
            "orientation": args.orientation,
            "is_hd": bool(args.hd),
        }
        resp = _http_json("POST", api_base + "/video/task/create", body=body, headers=headers_auth, timeout_s=300)
        ok, payload = _dashboard_ok(resp)
        if not ok:
            raise RuntimeError(f"task/create not successful: {payload}")
        data = payload.get("data") if isinstance(payload, dict) else None
        task_id = (data or {}).get("task_id") if isinstance(data, dict) else None
        if not task_id:
            raise RuntimeError(f"Unexpected task/create response: {payload}")
        task_id = str(task_id)
    except Exception as e:
        sys.stderr.write(f"Create task failed: {e}\n")
        return 4

    # 3) poll state
    start = time.time()
    last_state: Dict[str, Any] = {}
    while True:
        if time.time() - start > int(args.timeout):
            sys.stderr.write(f"Timeout after {args.timeout}s. task_id={task_id}\n")
            return 4

        try:
            qs = urllib.parse.urlencode({"task_id": task_id})
            url = api_base + "/video/task/state?" + qs
            resp = _http_json("GET", url, headers=headers_auth, timeout_s=60)
            ok, payload = _dashboard_ok(resp)
            if not ok:
                raise RuntimeError(f"task/state not successful: {payload}")
            data = payload.get("data") if isinstance(payload, dict) else None
            if not isinstance(data, dict):
                raise RuntimeError(f"Unexpected task/state response: {payload}")
            last_state = data

            status = str(data.get("status") or "")
            if status == "completed":
                video_url = data.get("video_url")
                if not video_url:
                    raise RuntimeError(f"completed but missing video_url: {payload}")

                result: Dict[str, Any] = {
                    "state": "SUCCESS",
                    "task_id": task_id,
                    "video_url": video_url,
                    "script": script,
                    "status": status,
                    "progress": data.get("progress"),
                }

                if args.out:
                    _download(str(video_url), args.out)
                    result["downloaded_to"] = args.out

                if args.json:
                    print(json.dumps(result, ensure_ascii=False, indent=2))
                else:
                    slim = {k: result[k] for k in ["state", "task_id", "script", "video_url"] if k in result}
                    if args.out:
                        slim["downloaded_to"] = args.out
                    print(json.dumps(slim, ensure_ascii=False, indent=2))
                return 0

            if status == "failed":
                raise RuntimeError(f"Video task failed: {data.get('failed_reason')}")

        except Exception as e:
            sys.stderr.write(f"Poll failed: {e}\n")
            if last_state:
                sys.stderr.write(f"Last state: {json.dumps(last_state, ensure_ascii=False)}\n")
            return 4

        time.sleep(float(args.poll_interval))


if __name__ == "__main__":
    raise SystemExit(main())
