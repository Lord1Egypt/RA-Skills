from __future__ import annotations

import json
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import ProxyHandler, Request, build_opener


@dataclass(frozen=True, slots=True)
class HttpRequest:
    method: str
    url: str
    headers: Mapping[str, str]

    @property
    def path(self) -> str:
        return urlsplit(self.url).path


@dataclass(slots=True)
class HttpResponse:
    status_code: int
    headers: dict[str, str]
    content: bytes
    url: str

    def json(self) -> Any:
        return json.loads(self.content.decode("utf-8"))


class HttpTransportError(RuntimeError):
    pass


type HttpTransport = Callable[[HttpRequest], HttpResponse]


class HttpClient:
    def __init__(
        self,
        *,
        base_url: str,
        headers: Mapping[str, str] | None = None,
        timeout: float = 30.0,
        transport: HttpTransport | None = None,
        trust_env: bool = True,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self.headers = dict(headers or {})
        self._timeout = timeout
        self._transport = transport
        self._trust_env = trust_env
        proxy_handler = ProxyHandler() if trust_env else ProxyHandler({})
        self._opener = build_opener(proxy_handler)

    def close(self) -> None:
        return None

    def get(
        self,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> HttpResponse:
        request = HttpRequest(
            method="GET",
            url=_append_query(_resolve_url(self._base_url, path), params),
            headers={**self.headers, **dict(headers or {})},
        )
        if self._transport is not None:
            return self._transport(request)

        urllib_request = Request(
            request.url,
            headers=dict(request.headers),
            method=request.method,
        )
        try:
            with self._opener.open(urllib_request, timeout=self._timeout) as response:
                return HttpResponse(
                    status_code=response.status,
                    headers=_normalize_headers(response.headers.items()),
                    content=response.read(),
                    url=response.geturl(),
                )
        except HTTPError as exc:
            return HttpResponse(
                status_code=exc.code,
                headers=_normalize_headers(exc.headers.items()),
                content=exc.read(),
                url=exc.geturl(),
            )
        except (URLError, OSError) as exc:
            raise HttpTransportError(str(exc)) from exc


def _resolve_url(base_url: str, path: str) -> str:
    if path.startswith("http://") or path.startswith("https://"):
        return path
    if path.startswith("/"):
        return f"{base_url}{path}"
    return f"{base_url}/{path}"


def _append_query(url: str, params: Mapping[str, Any] | None) -> str:
    if not params:
        return url

    split = urlsplit(url)
    query_pairs = parse_qsl(split.query, keep_blank_values=True)
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, list | tuple):
            query_pairs.extend((key, str(item)) for item in value)
            continue
        query_pairs.append((key, str(value)))
    return urlunsplit(
        (split.scheme, split.netloc, split.path, urlencode(query_pairs), split.fragment)
    )


def _normalize_headers(items: Any) -> dict[str, str]:
    return {str(key).lower(): str(value) for key, value in items}
