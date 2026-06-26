import hashlib
import hmac
import json
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests


class ZKEApiError(Exception):
    def __init__(self, code: Any, msg: str, payload: Optional[dict] = None):
        self.code = code
        self.msg = msg
        self.payload = payload or {}
        super().__init__(f"ZKE API Error {code}: {msg}")


class ZKEClient:
    def __init__(
        self,
        base_url: str,
        api_key: str = "",
        api_secret: str = "",
        recv_window: int = 5000,
        timeout: int = 15,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key or ""
        self.api_secret = api_secret or ""
        self.recv_window = recv_window
        self.timeout = timeout
        self.session = requests.Session()

    def _build_headers(
        self,
        signed: bool = False,
        ts: str = "",
        sign: str = "",
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json"
        }

        if signed and self.api_key:
            headers["X-CH-APIKEY"] = self.api_key
        if signed and ts:
            headers["X-CH-TS"] = ts
        if signed and sign:
            headers["X-CH-SIGN"] = sign

        if extra_headers:
            headers.update(extra_headers)

        return headers

    def _sign(
        self,
        ts: str,
        method: str,
        request_path: str,
        body_str: str = "",
    ) -> str:
        if not self.api_secret:
            return ""

        payload = f"{ts}{method.upper()}{request_path}{body_str}"
        return hmac.new(
            self.api_secret.encode("utf-8"),
            payload.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()

    def request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
        signed: bool = False,
        extra_headers: Optional[Dict[str, str]] = None,
    ) -> Any:
        method = method.upper()
        params = dict(params or {})
        body = dict(body or {})

        url = f"{self.base_url}{path}"

        # recvWindow is optional; only send when caller explicitly wants it
        # or when body/params already include it.
        query_str = urlencode(params) if params else ""
        request_path = path if not query_str else f"{path}?{query_str}"

        body_str = ""
        if method != "GET" and body:
            body_str = json.dumps(body, separators=(",", ":"), ensure_ascii=False)

        ts = ""
        sign = ""
        if signed:
            ts = str(int(time.time() * 1000))
            sign = self._sign(
                ts=ts,
                method=method,
                request_path=request_path,
                body_str=body_str if method != "GET" else "",
            )

        headers = self._build_headers(
            signed=signed,
            ts=ts,
            sign=sign,
            extra_headers=extra_headers,
        )

        resp = self.session.request(
            method=method,
            url=url,
            params=params if method == "GET" else None,
            data=body_str if method != "GET" else None,
            headers=headers,
            timeout=self.timeout,
        )

        text = resp.text.strip()

        try:
            data = resp.json()
        except Exception:
            raise RuntimeError(f"HTTP {resp.status_code} 返回非JSON: {text}")

        if isinstance(data, dict):
            code = data.get("code")
            msg = data.get("msg", "")

            if code is not None and str(code) not in ("0", "200"):
                raise ZKEApiError(code, msg, data)

        if resp.status_code >= 400:
            raise RuntimeError(f"HTTP {resp.status_code}: {text}")

        return data

    def explain_error(self, err: Exception) -> str:
        if isinstance(err, ZKEApiError):
            return f"ZKE API Error {err.code}: {err.msg}"
        return str(err)
