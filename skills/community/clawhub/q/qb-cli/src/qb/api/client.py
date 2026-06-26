"""QuickBooks Online API client with auto-refresh and structured errors."""

import httpx
from typing import Optional, Any

from qb.auth.tokens import TokenManager, AuthNotConfiguredError

SANDBOX_BASE = "https://sandbox-quickbooks.api.intuit.com"
PRODUCTION_BASE = "https://quickbooks.api.intuit.com"
API_VERSION = "v3"
MINOR_VERSION = "75"


class QBApiError(Exception):
    """Structured error from QuickBooks API."""

    def __init__(
        self,
        status_code: int,
        message: str,
        detail: str = "",
        intuit_tid: str = "",
    ):
        self.status_code = status_code
        self.message = message
        self.detail = detail
        self.intuit_tid = intuit_tid
        super().__init__(f"[{status_code}] {message}")

    @classmethod
    def from_response(cls, response: httpx.Response) -> "QBApiError":
        """Parse a QuickBooks error response."""
        intuit_tid = response.headers.get("intuit_tid", "")
        try:
            body = response.json()
            fault = body.get("Fault", {})
            errors = fault.get("Error", [{}])
            error = errors[0] if errors else {}
            return cls(
                status_code=response.status_code,
                message=error.get("Message", response.reason_phrase or "Unknown error"),
                detail=error.get("Detail", ""),
                intuit_tid=intuit_tid,
            )
        except Exception:
            return cls(
                status_code=response.status_code,
                message=response.text[:500] if response.text else "Unknown error",
                intuit_tid=intuit_tid,
            )


class QBClient:
    """HTTP client for QuickBooks Online API.

    Handles authentication, auto-refresh on 401, and URL construction.
    """

    def __init__(
        self,
        token_manager: TokenManager,
        client_id: str,
        client_secret: str,
        environment: Optional[str] = None,
        verbose: bool = False,
    ):
        self.token_manager = token_manager
        self.client_id = client_id
        self.client_secret = client_secret
        self._environment = environment
        self.verbose = verbose

    @property
    def base_url(self) -> str:
        env = self._environment or self.token_manager.environment
        if env == "production":
            return PRODUCTION_BASE
        return SANDBOX_BASE

    @property
    def realm_id(self) -> str:
        return self.token_manager.realm_id

    def _url(self, path: str) -> str:
        """Build full API URL."""
        return f"{self.base_url}/{API_VERSION}/company/{self.realm_id}/{path}"

    def _headers(self, access_token: str) -> dict:
        return {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    def _request(
        self,
        method: str,
        path: str,
        params: Optional[dict] = None,
        json_body: Optional[dict] = None,
        retry_on_401: bool = True,
    ) -> dict:
        """Make an API request with auto-refresh on 401."""
        access_token = self.token_manager.get_access_token(
            self.client_id, self.client_secret
        )

        # Always include minorversion
        params = dict(params) if params else {}
        params.setdefault("minorversion", MINOR_VERSION)

        url = self._url(path)

        if self.verbose:
            import sys
            print(f"[HTTP] {method} {url}", file=sys.stderr)
            if params:
                print(f"[HTTP] params={params}", file=sys.stderr)

        response = httpx.request(
            method,
            url,
            headers=self._headers(access_token),
            params=params,
            json=json_body,
            timeout=30.0,
        )

        if self.verbose:
            import sys
            print(f"[HTTP] {response.status_code} ({len(response.content)} bytes)", file=sys.stderr)

        if response.status_code == 401 and retry_on_401:
            # Token expired mid-flight — clear cache to force refresh on retry
            self.token_manager.clear_cache()
            return self._request(
                method, path, params, json_body, retry_on_401=False
            )

        if response.status_code >= 400:
            raise QBApiError.from_response(response)

        # Some endpoints return empty body on success (e.g., send invoice)
        if not response.content:
            return {"success": True}

        return response.json()

    def get(self, path: str, params: Optional[dict] = None) -> dict:
        """HTTP GET request."""
        return self._request("GET", path, params=params)

    def post(
        self,
        path: str,
        body: Optional[dict] = None,
        params: Optional[dict] = None,
    ) -> dict:
        """HTTP POST request."""
        return self._request("POST", path, params=params, json_body=body)

    def query(self, sql: str, max_results: int = 100) -> dict:
        """Execute a QuickBooks query (SQL-like)."""
        if "MAXRESULTS" not in sql.upper():
            sql = f"{sql} MAXRESULTS {max_results}"
        return self.get("query", params={"query": sql})
