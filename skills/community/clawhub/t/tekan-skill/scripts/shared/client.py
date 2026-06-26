"""Reusable HTTP client for the Tekan API with auth and task polling."""

import os
import sys
import time
import webbrowser
from typing import Any, Optional

import requests

from .config import load_config


TEKAN_API_URL = "https://api.tekan.cn:443"
BASE_URL = "https://api.topview.ai"
RECHARGE_URL = "https://tekan.cn/subscription?action=recharge"

RESPONSE_CODES = {
    "200": "Success",
    "401": "Unauthorized, need to login again",
    "4000": "Request parameter error",
    "4001": "Request data format does not match",
    "4002": "Request digital signature does not match",
    "4003": "Required parameter cannot be null",
    "4004": "Resource not found",
    "4005": "Name duplicated",
    "4006": "Request refuse",
    "4007": "Exists unfinished task, please wait",
    "4100": "Credit not enough",
    "5000": "Internal server error, please report at https://tekan.cn with task type and taskId (e.g. 'avatar4 task failed, taskId: abc123')",
    "5001": "Feign invoke error",
    "5003": "Server is busy, please try again later",
    "5004": "I/O error occurred",
    "5005": "Unknown error occurred",
    "6001": "Security problem detect",
}


TEKAN_CREDIT_MULTIPLIER = 100

SHORT_URL_API = "https://api.tekan.cn:8097"
_SHORT_URL_DOMAIN_OLD = "https://api.topview.ai"


def shorten_url(long_url: str, uid: str = "", api_key: str = "") -> str:
    """Call the short-URL service; silently returns *long_url* on any failure.

    When *uid*/*api_key* are omitted the function tries to read them from the
    local credentials file so callers don't have to pass them explicitly.
    """
    if not uid or not api_key:
        try:
            from .config import _load_from_file
            creds = _load_from_file() or {}
            uid = uid or creds.get("uid", "")
            api_key = api_key or creds.get("api_key", "")
        except Exception:
            pass
    if not uid or not api_key:
        return long_url
    try:
        resp = requests.post(
            f"{SHORT_URL_API}/v1/short_url/generate",
            headers={
                "Topview-Uid": uid,
                "Authorization": f"Bearer {api_key}",
            },
            json={"longUrl": long_url},
            timeout=5,
        )
        resp.raise_for_status()
        result = resp.json().get("result", {})
        short = result.get("shortUrl", long_url)
        return short.replace(_SHORT_URL_DOMAIN_OLD, SHORT_URL_API)
    except Exception:
        return long_url


def to_tekan_credit(topview_credit) -> int:
    """Convert TopView credits to Tekan credits (×100, rounded to int)."""
    if topview_credit is None or topview_credit == "N/A":
        return 0
    return round(float(topview_credit) * TEKAN_CREDIT_MULTIPLIER)


def convert_result_credits(result: dict) -> dict:
    """Convert all credit fields in an API result dict to Tekan credits in-place."""
    for key in ("costCredit", "creditsCost"):
        if key in result and result[key] is not None:
            result[key] = to_tekan_credit(result[key])
    return result


class TopviewError(Exception):
    """Raised when the Topview API returns a non-200 response code."""

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")


class TopviewClient:
    """Authenticated HTTP client for Topview API endpoints.

    Usage::

        client = TopviewClient()
        resp = client.post("/v1/photo_avatar/task/submit", json={...})
        result = client.poll_task("/v1/photo_avatar/task/query", task_id)
    """

    def __init__(self, uid: Optional[str] = None, api_key: Optional[str] = None):
        if uid and api_key:
            self._uid = uid
            self._api_key = api_key
            self._access_token: Optional[str] = None
        else:
            cfg = load_config()
            self._uid = cfg["uid"]
            self._api_key = cfg["api_key"]
            self._access_token = cfg.get("access_token")

    @property
    def headers(self) -> dict:
        return {
            "Topview-Uid": self._uid,
            "Authorization": f"Bearer {self._api_key}",
        }

    @property
    def token_headers(self) -> dict:
        """Headers using OAuth access_token (for user/billing endpoints)."""
        token = self._access_token or self._api_key
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

    def shorten_url(self, long_url: str) -> str:
        """Shorten a URL using the short-URL service."""
        return shorten_url(long_url, self._uid, self._api_key)

    def _check(self, data: dict):
        code = str(data.get("code", ""))
        if code != "200":
            msg = data.get("message", RESPONSE_CODES.get(code, "Unknown error") + f", response: {data}")
            raise TopviewError(code, msg)
        if "result" in data:
            return data["result"]
        if "data" in data:
            return data["data"]
        return data

    def get(self, path: str, params: Optional[dict] = None, **kwargs) -> dict:
        url = f"{BASE_URL}{path}" if path.startswith("/") else path
        resp = requests.get(url, headers=self.headers, params=params, **kwargs)
        resp.raise_for_status()
        return self._check(resp.json())

    def post(self, path: str, json: Optional[dict] = None, **kwargs) -> dict:
        url = f"{BASE_URL}{path}" if path.startswith("/") else path
        resp = requests.post(url, headers=self.headers, json=json, **kwargs)
        resp.raise_for_status()
        return self._check(resp.json())

    def put(self, path: str, json: Optional[dict] = None, **kwargs) -> dict:
        url = f"{BASE_URL}{path}" if path.startswith("/") else path
        resp = requests.put(url, headers=self.headers, json=json, **kwargs)
        resp.raise_for_status()
        return self._check(resp.json())

    def delete(self, path: str, params: Optional[dict] = None, **kwargs) -> dict:
        url = f"{BASE_URL}{path}" if path.startswith("/") else path
        resp = requests.delete(url, headers=self.headers, params=params, **kwargs)
        resp.raise_for_status()
        return self._check(resp.json())

    def guard_credit(self, required: int = 0, task_name: str = "") -> int:
        """Fetch current quota and abort if credits are insufficient.

        When credits are insufficient, opens the recharge page in the
        browser (same pattern as auth.py login flow) and exits.

        Args:
            required: Tekan credits needed (already ×100). Pass 0 if unknown.
            task_name: Label for the log message.

        Returns:
            Current balance (Tekan credits).

        Raises:
            SystemExit: if balance is insufficient.
        """
        quota_path = "/user/benefit/tekan-video/quota"
        try:
            url = f"{TEKAN_API_URL}{quota_path}"
            resp = requests.get(url, headers=self.token_headers)
            resp.raise_for_status()
            result = self._check(resp.json())
            balance = int(result) if isinstance(result, (int, float)) else 0
        except Exception as e:
            print(f"Warning: failed to check credit balance: {e}", file=sys.stderr)
            return 0

        label = f" [{task_name}]" if task_name else ""
        insufficient = False

        if required > 0:
            print(
                f"Credit guard{label}: need {required}, have {balance}",
                file=sys.stderr,
            )
            if balance < required:
                insufficient = True
        elif balance <= 0:
            insufficient = True

        if insufficient:
            if required > 0:
                print(
                    f"\nInsufficient credits{label}: "
                    f"need {required}, have {balance}.",
                    file=sys.stderr,
                )
            else:
                print(
                    f"\nInsufficient credits{label}: balance is {balance}.",
                    file=sys.stderr,
                )

            recharge = self.shorten_url(RECHARGE_URL)
            print(
                f"\n  Recharge URL: {recharge}\n"
                f"\n  Please open the link above to top up your credits,\n"
                f"  then re-run the command.\n",
                file=sys.stderr,
            )
            try:
                webbrowser.open(recharge)
            except Exception:
                pass
            sys.exit(1)

        return balance

    def put_file(self, upload_url: str, file_path: str) -> None:
        """PUT a local file to a pre-signed S3 URL (no auth headers)."""
        with open(file_path, "rb") as f:
            resp = requests.put(upload_url, data=f)
        resp.raise_for_status()

    def poll_task(
        self,
        path: str,
        task_id: str,
        *,
        interval: float = 5.0,
        timeout: float = 600.0,
        verbose: bool = True,
    ) -> dict:
        """Poll a task endpoint until status is 'success' or 'failed'.

        Returns the result dict on success; raises TopviewError on failure.
        """
        start = time.time()
        while True:
            elapsed = time.time() - start
            if elapsed > timeout:
                raise TimeoutError(
                    f"Task {task_id} did not complete within {timeout}s"
                )

            result = self.get(path, params={"taskId": task_id})
            status = result.get("status", "").lower()

            if verbose:
                print(
                    f"  [{elapsed:.0f}s] status: {status}",
                    file=sys.stderr,
                )

            if status == "success":
                return result
            if status in ("failed", "fail"):
                raise TopviewError("TASK_FAILED", result.get("errorMsg", "Task failed"))

            time.sleep(interval)
