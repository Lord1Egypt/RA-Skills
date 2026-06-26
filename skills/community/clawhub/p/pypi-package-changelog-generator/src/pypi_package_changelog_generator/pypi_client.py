from __future__ import annotations

from typing import Any, Iterable
from urllib.parse import urlparse

from pypi_package_changelog_generator._http import (
    HttpClient,
    HttpTransport,
    HttpTransportError,
)


class PypiClientError(RuntimeError):
    def __init__(self, code: str, message: str, *, retryable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable


class PypiClient:
    def __init__(
        self, *, timeout: float = 30.0, transport: HttpTransport | None = None
    ) -> None:
        self._client = HttpClient(
            base_url="https://pypi.org/pypi",
            headers={"Accept": "application/json"},
            timeout=timeout,
            transport=transport,
            trust_env=True,
        )

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "PypiClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def get_project(self, package: str) -> dict[str, Any]:
        return self._get_json(f"/{package}/json")

    def get_release(self, package: str, version: str) -> dict[str, Any]:
        return self._get_json(f"/{package}/{version}/json")

    def download_bytes(self, url: str) -> bytes:
        try:
            response = self._client.get(url)
        except HttpTransportError as exc:
            raise PypiClientError(
                code="pypi_download_failed",
                message=f"Failed to download source archive from {url}.",
                retryable=True,
            ) from exc
        if response.status_code >= 400:
            raise PypiClientError(
                code="pypi_download_failed",
                message=f"Failed to download source archive from {url}.",
                retryable=True,
            )
        return response.content

    def find_sdist_url(self, release_payload: dict[str, Any]) -> str | None:
        for file_info in release_payload.get("urls", []):
            if file_info.get("packagetype") == "sdist":
                return file_info.get("url")
        return None

    def extract_repository_url(self, *payloads: dict[str, Any]) -> str | None:
        candidates: list[str] = []
        for payload in payloads:
            info = payload.get("info", {})
            project_urls = info.get("project_urls") or {}
            candidates.extend(project_urls.values())
            home_page = info.get("home_page")
            if home_page:
                candidates.append(home_page)

        for candidate in candidates:
            normalized = normalize_repository_url(candidate)
            if normalized:
                return normalized
        return None

    def _get_json(self, path: str) -> dict[str, Any]:
        try:
            response = self._client.get(path)
        except HttpTransportError as exc:
            raise PypiClientError(
                code="pypi_http_error",
                message=f"PyPI request failed for {path}.",
                retryable=True,
            ) from exc

        if response.status_code >= 400:
            status = response.status_code
            raise PypiClientError(
                code=f"pypi_http_{status}",
                message=f"PyPI request failed for {path} with HTTP {status}.",
                retryable=status >= 500,
            )
        return response.json()


def normalize_repository_url(candidate: str | None) -> str | None:
    if not candidate:
        return None
    text = candidate.strip()
    if text.startswith("git@github.com:"):
        text = text.replace("git@github.com:", "https://github.com/", 1)
    if text.endswith(".git"):
        text = text[:-4]
    parsed = urlparse(text)
    if parsed.scheme not in {"http", "https"}:
        return None
    if parsed.netloc.lower() != "github.com":
        return None
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return None
    owner, repo = parts[:2]
    return f"https://github.com/{owner}/{repo}"


def iter_project_urls(payloads: Iterable[dict[str, Any]]) -> list[str]:
    urls: list[str] = []
    for payload in payloads:
        info = payload.get("info", {})
        urls.extend((info.get("project_urls") or {}).values())
        if info.get("home_page"):
            urls.append(info["home_page"])
    return urls
