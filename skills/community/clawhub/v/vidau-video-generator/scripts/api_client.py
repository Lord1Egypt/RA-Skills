#!/usr/bin/env python3
"""
Vidau API client: sends HTTP requests and logs URL, method, params, and response to a file.
Log path is set by env VIDAU_API_LOG; default is ~/vidau_api.log so one log file is used regardless of cwd.
API Key is read from env VIDAU_API_KEY first; if unset, from OpenClaw config ~/.openclaw/openclaw.json skills.entries.vidau.
"""
import json
import os
from datetime import datetime
from typing import Optional
from typing import Optional, Tuple
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

LOG_PATH = os.environ.get("VIDAU_API_LOG", os.path.join(os.path.expanduser("~"), "vidau_api.log"))


def get_api_key() -> Optional[str]:
    """
    Get Vidau API Key: prefer env VIDAU_API_KEY; else read from OpenClaw config
    ~/.openclaw/openclaw.json skills.entries.vidau.apiKey or env.VIDAU_API_KEY.
    """
    key = os.environ.get("VIDAU_API_KEY")
    if key and key.strip():
        return key.strip()
    config_path = os.path.expanduser("~/.openclaw/openclaw.json")
    if not os.path.isfile(config_path):
        return None
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        entries = (cfg.get("skills") or {}).get("entries") or {}
        vidau = entries.get("vidau") or {}
        if isinstance(vidau.get("apiKey"), str) and vidau["apiKey"].strip():
            return vidau["apiKey"].strip()
        env = vidau.get("env") or {}
        key = env.get("VIDAU_API_KEY")
        if isinstance(key, str) and key.strip():
            return key.strip()
    except (OSError, json.JSONDecodeError, TypeError):
        pass
    return None


class APIError(Exception):
    """HTTP error with status code and response body for caller to log."""
    def __init__(self, message: str, status_code: int, body: str = ""):
        super().__init__(message)
        self.code = status_code
        self.body = body


def _write_log(
    method: str,
    url: str,
    params_or_body: Optional[str],
    response_status: Optional[int],
    response_body: str,
    error: Optional[str] = None,
) -> None:
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write("\n" + "=" * 60 + "\n")
            f.write(f"[{datetime.now().isoformat()}] API request\n")
            f.write("-" * 40 + "\n")
            f.write(f"URL:    {url}\n")
            f.write(f"Method: {method}\n")
            f.write(f"Params: {params_or_body or '(none)'}\n")
            f.write("-" * 40 + "\n")
            f.write(f"Status: {response_status}\n")
            if error:
                f.write(f"Error:  {error}\n")
            f.write(f"Body:   {response_body[:2000]}\n")
            if len(response_body) > 2000:
                f.write("...(truncated)\n")
            f.write("=" * 60 + "\n")
    except OSError:
        pass


def api_request(
    method: str,
    url: str,
    headers: Optional[dict] = None,
    data: Optional[bytes] = None,
    timeout: float = 30,
) -> Tuple[bytes, int]:
    """
    Send HTTP request and log URL, method, params, and response to the log file.
    Returns (response body bytes, HTTP status code).
    On HTTPError or URLError, logs first then re-raises.
    """
    params_str: Optional[str] = None
    if data:
        try:
            params_str = data.decode("utf-8")
        except Exception:
            params_str = "<binary>"

    try:
        req = Request(url, data=data, headers=headers or {}, method=method)
        with urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            status = getattr(resp, "status", 200)
            body_str = raw.decode("utf-8", errors="replace")
            _write_log(method, url, params_str, status, body_str)
            return raw, status
    except HTTPError as e:
        err_body = b""
        try:
            err_body = e.read()
        except Exception:
            pass
        body_str = err_body.decode("utf-8", errors="replace")
        _write_log(method, url, params_str, e.code, body_str, error=str(e.reason))
        raise APIError(str(e.reason), e.code, body_str) from e
    except URLError as e:
        _write_log(method, url, params_str, None, "", error=str(e.reason))
        raise
