"""TrendAI Vision One API client with auth, retry, and rate-limit handling."""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urlencode

REGIONS = {
    "us": "api.xdr.trendmicro.com",
    "eu": "api.eu.xdr.trendmicro.com",
    "jp": "api.xdr.trendmicro.co.jp",
    "sg": "api.sg.xdr.trendmicro.com",
    "au": "api.au.xdr.trendmicro.com",
    "in": "api.in.xdr.trendmicro.com",
    "mea": "api.mea.xdr.trendmicro.com",
}

MAX_RETRIES = 3
BACKOFF_BASE = 2  # seconds


class APIError(Exception):
    def __init__(self, status, message, body=None):
        self.status = status
        self.message = message
        self.body = body
        super().__init__(f"HTTP {status}: {message}")


class VisionOneClient:
    def __init__(self, api_key=None, region=None):
        self.api_key = api_key or os.environ.get("VISION_ONE_API_KEY", "")
        if not self.api_key:
            print(
                "ERROR: No API key provided\n"
                "EXPECTED: Set VISION_ONE_API_KEY environment variable\n"
                "EXAMPLE: export VISION_ONE_API_KEY='eyJ0eXAi...'",
                file=sys.stderr,
            )
            sys.exit(2)

        self.region = (region or os.environ.get("VISION_ONE_REGION", "us")).lower()
        if self.region not in REGIONS:
            valid = ", ".join(sorted(REGIONS))
            print(
                f"ERROR: Region '{self.region}' is not valid\n"
                f"EXPECTED: One of: {valid}\n"
                f"EXAMPLE: export VISION_ONE_REGION='us'",
                file=sys.stderr,
            )
            sys.exit(2)

        self.base_url = f"https://{REGIONS[self.region]}"

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json;charset=utf-8",
            "User-Agent": "OpenClaw-VisionOneTI/1.0",
        }

    def _request(self, method, path, params=None, body=None):
        url = f"{self.base_url}{path}"
        if params:
            # Filter out None values
            clean = {k: v for k, v in params.items() if v is not None}
            if clean:
                url += "?" + urlencode(clean)

        data = None
        if body is not None:
            data = json.dumps(body).encode("utf-8")

        req = urllib.request.Request(url, data=data, headers=self._headers(), method=method)

        last_err = None
        for attempt in range(MAX_RETRIES):
            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    raw = resp.read().decode("utf-8")
                    return json.loads(raw) if raw.strip() else {}
            except urllib.error.HTTPError as e:
                body_text = ""
                try:
                    body_text = e.read().decode("utf-8", errors="replace")
                except Exception:
                    pass

                if e.code == 429:
                    # Rate limited — backoff and retry
                    wait = BACKOFF_BASE ** (attempt + 1)
                    time.sleep(wait)
                    last_err = APIError(e.code, "Rate limited", body_text)
                    continue
                elif e.code >= 500:
                    # Server error — retry with backoff
                    wait = BACKOFF_BASE ** (attempt + 1)
                    time.sleep(wait)
                    last_err = APIError(e.code, "Server error", body_text)
                    continue
                elif e.code == 401:
                    raise APIError(
                        401,
                        "Authentication failed. Check your VISION_ONE_API_KEY and VISION_ONE_REGION.",
                        body_text,
                    )
                elif e.code == 403:
                    raise APIError(
                        403,
                        "Access denied. Your API key may lack permissions for this endpoint, "
                        "or the region may be incorrect.",
                        body_text,
                    )
                else:
                    raise APIError(e.code, f"Request failed: {body_text}", body_text)
            except urllib.error.URLError as e:
                wait = BACKOFF_BASE ** (attempt + 1)
                time.sleep(wait)
                last_err = APIError(0, f"Network error: {e.reason}")
                continue

        raise last_err

    def get(self, path, params=None):
        return self._request("GET", path, params=params)

    def post(self, path, body=None):
        return self._request("POST", path, body=body)
