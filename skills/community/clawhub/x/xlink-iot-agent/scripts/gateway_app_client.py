import base64
import hashlib
import json
import os
import struct
import threading
import time
import urllib.parse
from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

try:
    import urllib3
    from urllib3.util.retry import Retry
    HAS_URLLIB3 = True
except ImportError:
    HAS_URLLIB3 = False
    import http.client
    import ssl


class StageType(str, Enum):
    RELEASE = "RELEASE"
    TEST = "TEST"
    PRE_RELEASE = "PRE_RELEASE"

    def stage(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class HttpResponse:
    code: int
    headers: dict[str, str]
    content: str

    @property
    def is_success(self) -> bool:
        return 200 <= self.code < 300

    def get_response_code(self) -> int:
        return self.code

    def get_content(self) -> str:
        return self.content

    def get_header(self, name: str) -> str | None:
        return self.headers.get(name)


class GatewayAppClientError(Exception):
    """Exception raised for HTTP and gateway client errors.

    Attributes:
        status: HTTP status code (0 if not available).
        response_body: Response body as string (empty string if not available).
    """

    def __init__(self, message: str, status: int = 0, response_body: str = ""):
        super().__init__(message)
        self.status = status
        self.response_body = response_body


class _ObjectIdGenerator:
    def __init__(self) -> None:
        self._random_five_bytes = os.urandom(5)
        self._counter = int.from_bytes(os.urandom(3), byteorder="big", signed=False)
        self._lock = threading.Lock()

    def next_hex(self) -> str:
        ts_seconds = int(time.time())
        with self._lock:
            counter = self._counter
            self._counter = (self._counter + 1) & 0xFFFFFF
        raw = (
            struct.pack(">I", ts_seconds)
            + self._random_five_bytes
            + counter.to_bytes(3, "big")
        )
        return raw.hex()


_REQUEST_ID_GENERATOR = _ObjectIdGenerator()


class GatewayAppClient:
    SYMBOL_LF = "\n"

    HEADER_GROUP = "Group"
    HEADER_STAGE = "Stage"
    HEADER_APP_ID = "App-ID"
    HEADER_SIGNATURE = "Signature"
    HEADER_TIMESTAMP = "Timestamp"
    HEADER_REQUEST_ID = "Request-ID"
    HEADER_CONTENT_MD5 = "Content-MD5"

    CONTENT_TYPE = "Content-Type"
    APPLICATION_JSON_UTF8_VALUE = "application/json;charset=UTF-8"

    CONNECT_TIMEOUT_S = 50.0
    SOCKET_TIMEOUT_S = 50.0

    # Retry configuration
    RETRY_TOTAL = 3
    RETRY_BACKOFF_FACTOR = 1
    RETRY_STATUS_FORCELIST = [429, 500, 502, 503, 504]

    def __init__(self, app_id: str, app_secret: str) -> None:
        self.app_id = app_id
        self.app_secret = app_secret

        if HAS_URLLIB3:
            retry_strategy = Retry(
                total=self.RETRY_TOTAL,
                backoff_factor=self.RETRY_BACKOFF_FACTOR,
                status_forcelist=self.RETRY_STATUS_FORCELIST,
            )
            self._http = urllib3.PoolManager(retries=retry_strategy)
        else:
            self._http = None

    def get(
        self,
        group: str,
        stage: StageType,
        url: str,
        host: str,
        header_map: dict[str, str] | None = None,
        param_map: Mapping[str, str] | None = None,
        connect_timeout_ms: int | None = None,
        socket_timeout_ms: int | None = None,
    ) -> HttpResponse:
        return self._request(
            method="GET",
            group=group,
            stage=stage,
            url=url,
            host=host,
            data=None,
            header_map=header_map,
            param_map=param_map,
            connect_timeout_ms=connect_timeout_ms,
            socket_timeout_ms=socket_timeout_ms,
        )

    def post(
        self,
        group: str,
        stage: StageType,
        url: str,
        host: str,
        data: str | bytes | Mapping[str, Any] | list[Any] | None,
        header_map: dict[str, str] | None = None,
        param_map: Mapping[str, str] | None = None,
        connect_timeout_ms: int | None = None,
        socket_timeout_ms: int | None = None,
    ) -> HttpResponse:
        return self._request(
            method="POST",
            group=group,
            stage=stage,
            url=url,
            host=host,
            data=data,
            header_map=header_map,
            param_map=param_map,
            connect_timeout_ms=connect_timeout_ms,
            socket_timeout_ms=socket_timeout_ms,
        )

    def put(
        self,
        group: str,
        stage: StageType,
        url: str,
        host: str,
        data: str | bytes | Mapping[str, Any] | list[Any] | None,
        header_map: dict[str, str] | None = None,
        param_map: Mapping[str, str] | None = None,
        connect_timeout_ms: int | None = None,
        socket_timeout_ms: int | None = None,
    ) -> HttpResponse:
        return self._request(
            method="PUT",
            group=group,
            stage=stage,
            url=url,
            host=host,
            data=data,
            header_map=header_map,
            param_map=param_map,
            connect_timeout_ms=connect_timeout_ms,
            socket_timeout_ms=socket_timeout_ms,
        )

    def delete(
        self,
        group: str,
        stage: StageType,
        url: str,
        host: str,
        header_map: dict[str, str] | None = None,
        param_map: Mapping[str, str] | None = None,
        connect_timeout_ms: int | None = None,
        socket_timeout_ms: int | None = None,
    ) -> HttpResponse:
        return self._request(
            method="DELETE",
            group=group,
            stage=stage,
            url=url,
            host=host,
            data=None,
            header_map=header_map,
            param_map=param_map,
            connect_timeout_ms=connect_timeout_ms,
            socket_timeout_ms=socket_timeout_ms,
        )

    def _build_request_id(self) -> str:
        return _REQUEST_ID_GENERATOR.next_hex()

    def _build_timestamp(self) -> str:
        return str(int(time.time() * 1000))

    def _build_full_path(self, url: str, param_map: Mapping[str, str] | None) -> str:
        if not param_map:
            return url
        parts: list[str] = []
        for key, value in param_map.items():
            parts.append(
                f"{key}={urllib.parse.quote_plus(str(value), encoding='utf-8')}"
            )
        return f"{url}?{'&'.join(parts)}"

    def _build_full_url(
        self, host: str, url: str, param_map: Mapping[str, str] | None
    ) -> str:
        if host.endswith("/") and not host.endswith("//"):
            host = host.rstrip("/")
        if url.startswith("/"):
            base = f"{host}{url}"
        else:
            base = f"{host}/{url}"
        if not param_map:
            return base
        return self._build_full_path(base, param_map)

    def _normalize_body(
        self, data: str | bytes | Mapping[str, Any] | list[Any] | None
    ) -> bytes | None:
        if data is None:
            return None
        if isinstance(data, bytes):
            return data
        if isinstance(data, str):
            return data.encode("utf-8")
        return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode(
            "utf-8"
        )

    def _signature(
        self, timestamp: str, request_id: str, full_path: str, body: bytes | None
    ) -> tuple[str, str | None]:
        content_md5 = None
        sign_parts = [self.app_id, self.app_secret, timestamp, request_id, full_path]
        if body is not None:
            content_md5 = base64.b64encode(hashlib.md5(body).digest()).decode("ascii")
            sign_parts.append(content_md5)
        sign_to_string = self.SYMBOL_LF.join(sign_parts)
        signature = base64.b64encode(
            hashlib.sha256(sign_to_string.encode("utf-8")).digest()
        ).decode("ascii")
        return signature, content_md5

    def _build_headers(
        self,
        group: str,
        timestamp: str,
        request_id: str,
        content_md5: str | None,
        signature: str,
        stage: StageType,
        extra_headers: dict[str, str] | None,
    ) -> dict[str, str]:
        headers: dict[str, str] = dict(extra_headers or {})
        headers[self.CONTENT_TYPE] = self.APPLICATION_JSON_UTF8_VALUE
        headers[self.HEADER_APP_ID] = self.app_id
        headers[self.HEADER_GROUP] = group
        headers[self.HEADER_STAGE] = stage.stage()
        headers[self.HEADER_TIMESTAMP] = timestamp
        headers[self.HEADER_REQUEST_ID] = request_id
        headers[self.HEADER_SIGNATURE] = signature
        if content_md5 is not None:
            headers[self.HEADER_CONTENT_MD5] = content_md5
        return headers

    def _timeout_seconds(
        self, connect_timeout_ms: int | None, socket_timeout_ms: int | None
    ) -> float:
        ct = (
            (connect_timeout_ms / 1000.0)
            if connect_timeout_ms
            else self.CONNECT_TIMEOUT_S
        )
        st = (
            (socket_timeout_ms / 1000.0) if socket_timeout_ms else self.SOCKET_TIMEOUT_S
        )
        return max(ct, st)

    def _request(
        self,
        method: str,
        group: str,
        stage: StageType,
        url: str,
        host: str,
        data: str | bytes | Mapping[str, Any] | list[Any] | None,
        header_map: dict[str, str] | None,
        param_map: Mapping[str, str] | None,
        connect_timeout_ms: int | None,
        socket_timeout_ms: int | None,
    ) -> HttpResponse:
        request_id = self._build_request_id()
        timestamp = self._build_timestamp()
        full_path = self._build_full_path(url, param_map)
        body = self._normalize_body(data)
        signature, content_md5 = self._signature(timestamp, request_id, full_path, body)
        headers = self._build_headers(
            group, timestamp, request_id, content_md5, signature, stage, header_map
        )
        full_url = self._build_full_url(host, url, param_map)
        timeout = self._timeout_seconds(connect_timeout_ms, socket_timeout_ms)

        try:
            if HAS_URLLIB3:
                resp = self._http.request(
                    method,
                    full_url,
                    body=body,
                    headers=headers,
                    timeout=timeout,
                )
                resp_headers = {k: v for k, v in resp.headers.items()}
                content = resp.data.decode("utf-8", errors="replace")

                if resp.status >= 400:
                    raise GatewayAppClientError(
                        f"HTTP {resp.status}: {content[:500]}",
                        status=resp.status,
                        response_body=content,
                    )

                return HttpResponse(code=resp.status, headers=resp_headers, content=content)
            else:
                # Fallback to http.client when urllib3 is not available
                parsed = urllib.parse.urlparse(full_url)
                conn_class = http.client.HTTPSConnection if parsed.scheme == 'https' else http.client.HTTPConnection
                conn = conn_class(parsed.netloc, timeout=timeout)
                try:
                    path = parsed.path + ('?' + parsed.query if parsed.query else '')
                    conn.request(method, path, body=body, headers=headers)
                    resp = conn.getresponse()
                    resp_headers = {k: v for k, v in resp.getheaders()}
                    content = resp.read().decode("utf-8", errors="replace")
                    
                    if resp.status >= 400:
                        raise GatewayAppClientError(
                            f"HTTP {resp.status}: {content[:500]}",
                            status=resp.status,
                            response_body=content,
                        )
                    
                    return HttpResponse(code=resp.status, headers=resp_headers, content=content)
                finally:
                    conn.close()

        except GatewayAppClientError:
            raise
        except Exception as e:
            raise GatewayAppClientError(
                f"{method} {full_url}: {e}",
                status=0,
                response_body="",
            ) from e
