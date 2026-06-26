#!/usr/bin/env python3
"""Puzle Reading Client SDK

Provides a Python interface to Puzle's reading analysis platform.
Supports creating readings from URLs, HTML content, and local files,
plus semantic search and listing.

Requirements: requests (pip install requests)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import requests

# Token storage location: ~/.config/puzle/config.json
CONFIG_DIR = Path.home() / ".config" / "puzle"
CONFIG_FILE = CONFIG_DIR / "config.json"
BASE_URL = "https://read-web.puzle.com.cn/api/v1"


class PuzleAPIError(Exception):
    """API returned a non-200 application code.

    Note: The Puzle backend always returns HTTP 200. Errors are indicated
    by the ``code`` field in the JSON body (e.g. 401_002 for invalid token).
    """

    def __init__(self, code: int, msg: str) -> None:
        self.code = code
        self.msg = msg
        super().__init__(f"PuzleAPIError({code}): {msg}")


class PuzleTimeoutError(Exception):
    """Polling timed out waiting for reading to complete."""


@dataclass
class ReadingResult:
    """Lightweight result returned immediately after creating a reading."""

    reading_id: int
    resource_type: str  # "link" | "file"
    status: str
    task_id: int
    web_url: str  # e.g. "https://read.puzle.com.cn/read/42?type=link&task_id=100"
    puzle_id: int | None = None


class PuzleReadingClient:
    """Client for the Puzle Reading API.

    Token is loaded exclusively from ``~/.config/puzle/config.json``.
    Use ``exchange_device_code(code)`` to authorize — the token is never
    exposed to callers or stored in environment variables.

    If no token is found, raises ``ValueError``.
    """

    def __init__(self) -> None:
        token = self._load_token()
        if not token:
            raise ValueError(
                "No Puzle token found. "
                "Run PuzleReadingClient.exchange_device_code(code) to authorize."
            )
        self._base_url = BASE_URL
        self._web_host = self._base_url.split("/api/")[0]
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }
        )

    # ------------------------------------------------------------------
    # Token management
    # ------------------------------------------------------------------

    @staticmethod
    def _save_token(token: str) -> Path:
        """Save token to ~/.config/puzle/config.json. Internal use only."""
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        config: dict[str, str] = {}
        if CONFIG_FILE.exists():
            try:
                config = json.loads(CONFIG_FILE.read_text())
            except (json.JSONDecodeError, OSError):
                config = {}
        config["token"] = token
        CONFIG_FILE.write_text(json.dumps(config, indent=2))
        CONFIG_FILE.chmod(0o600)  # owner-only read/write
        return CONFIG_FILE

    @staticmethod
    def _load_token() -> str | None:
        """Load token from config file. Internal use only."""
        config = PuzleReadingClient._load_config()
        return config.get("token")

    @staticmethod
    def _load_config() -> dict[str, str]:
        if CONFIG_FILE.exists():
            try:
                return json.loads(CONFIG_FILE.read_text())
            except (json.JSONDecodeError, OSError):
                pass
        return {}

    @staticmethod
    def token_is_configured() -> bool:
        """Check whether a token is available in the config file."""
        return PuzleReadingClient._load_token() is not None

    @staticmethod
    def exchange_device_code(code: str) -> None:
        """Exchange a device authorization code for a token and save it.

        The user obtains the code from https://read-web.puzle.com.cn/device-auth.
        This method exchanges it for a token via the server and saves it to the
        config file. The token is never returned or exposed to callers.

        Args:
            code: The device authorization code from the user.

        Raises:
            PuzleAPIError: If the exchange request fails.
        """
        url = f"{BASE_URL}/auth/device/token"
        resp = requests.post(url, json={"code": code})
        if not resp.ok:
            raise PuzleAPIError(code=resp.status_code, msg=resp.text)
        body: dict[str, Any] = resp.json()
        if body.get("code", 200) != 200:
            raise PuzleAPIError(code=body["code"], msg=body.get("msg", "Unknown error"))
        token: str = body["data"]["access_token"]
        PuzleReadingClient._save_token(token)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        """Send an HTTP request and return parsed JSON. Raises PuzleAPIError on failure.

        The Puzle backend always returns HTTP 200. Errors are indicated by
        the ``code`` field in the response body (200 = success, anything else
        is an error). The error message is in the ``msg`` field.
        """
        url = f"{self._base_url}{path}"
        resp = self._session.request(method, url, **kwargs)
        if not resp.ok:
            # Network / reverse-proxy level error (not from Puzle backend)
            raise PuzleAPIError(code=resp.status_code, msg=resp.text)
        body: dict[str, Any] = resp.json()
        if body.get("code", 200) != 200:
            raise PuzleAPIError(code=body["code"], msg=body.get("msg", "Unknown error"))
        return body

    def _to_reading_result(self, item: dict[str, Any]) -> ReadingResult:
        reading_id = item["id"]
        resource_type = item["resource_type"]
        task_id = item["task_id"]
        return ReadingResult(
            reading_id=reading_id,
            resource_type=resource_type,
            status=item["status"],
            task_id=task_id,
            web_url=f"{self._web_host}/read/{reading_id}?type={resource_type}&task_id={task_id}",
            puzle_id=item.get("puzle_id"),
        )

    # ------------------------------------------------------------------
    # Create readings
    # ------------------------------------------------------------------

    def create_reading_from_url(self, url: str) -> ReadingResult:
        """Create a reading from a URL.

        Processing is async — call ``wait_for_reading()`` to get the full content.
        """
        data = self._request("POST", "/reading/link", json={"url": url})
        return self._to_reading_result(data["data"])

    def create_reading_from_html(
        self,
        url: str,
        title: str,
        content: str,
        text_content: str,
        *,
        excerpt: str | None = None,
        byline: str | None = None,
        site_name: str | None = None,
        published_time: str | None = None,
    ) -> ReadingResult:
        """Create a reading from pre-fetched HTML content.

        Internally performs two API calls:
        1. Save content to obtain a link_id
        2. Create a reading with that link_id

        This skips the fetching phase, so processing is faster than URL-based creation.
        """
        # Step 1: save content
        payload: dict[str, Any] = {
            "url": url,
            "title": title,
            "content": content,
            "text_content": text_content,
        }
        for key, value in [
            ("excerpt", excerpt),
            ("byline", byline),
            ("site_name", site_name),
            ("published_time", published_time),
        ]:
            if value is not None:
                payload[key] = value

        save_data = self._request("POST", "/link/save-content", json=payload)
        link_id = save_data["data"]["id"]

        # Step 2: create reading from saved link
        data = self._request("POST", "/reading/link", json={"link_id": link_id})
        return self._to_reading_result(data["data"])

    def create_reading_from_file(self, file_path: str) -> ReadingResult:
        """Create a reading from a local file.

        Internally performs three steps:
        1. Request a pre-signed upload URL from the server
        2. Upload file binary to S3
        3. Create a reading from the uploaded file

        Supported file types: PDF, TXT, MD, CSV, JPG, PNG, WebP, GIF, MP3, WAV
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        file_bytes = path.read_bytes()
        content_hash = hashlib.md5(file_bytes).hexdigest()
        file_size = len(file_bytes)
        filename = path.name

        # Step 1: get pre-signed upload URL
        upload_data = self._request(
            "POST",
            "/file/upload-url",
            json={
                "filename": filename,
                "content_hash": content_hash,
                "file_size_bytes": file_size,
            },
        )
        upload_info = upload_data["data"]
        upload_url: str = upload_info["upload_url"]
        file_key: str = upload_info["file_key"]

        # Step 2: upload binary to S3
        put_resp = requests.put(
            upload_url,
            data=file_bytes,
            headers={"Content-Type": "application/octet-stream"},
        )
        if not put_resp.ok:
            raise PuzleAPIError(
                code=put_resp.status_code,
                msg=f"S3 upload failed: {put_resp.text}",
            )

        # Step 3: create reading from uploaded file
        data = self._request(
            "POST",
            "/reading/file/from-upload",
            json={
                "file_key": file_key,
                "filename": filename,
                "content_hash": content_hash,
            },
        )
        return self._to_reading_result(data["data"])

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def get_reading_detail(self, reading_id: int, resource_type: str) -> dict[str, Any]:
        """Get full reading detail including content (when status is done).

        Routes to the correct endpoint based on resource_type:
        - "link" → GET /reading/link/{id}
        - "file" → GET /reading/file/{id}
        """
        if resource_type == "link":
            return self._request("GET", f"/reading/link/{reading_id}")
        elif resource_type == "file":
            return self._request("GET", f"/reading/file/{reading_id}")
        else:
            raise ValueError(f"Unknown resource_type: {resource_type!r}. Expected 'link' or 'file'.")

    def wait_for_reading(
        self,
        reading_id: int,
        resource_type: str,
        *,
        poll_interval: float = 3.0,
        timeout: float = 120.0,
    ) -> dict[str, Any]:
        """Poll until reading processing completes.

        Returns the full detail dict when status becomes "done".
        Raises PuzleAPIError if status becomes "fail".
        Raises PuzleTimeoutError if timeout is exceeded.
        """
        start = time.monotonic()
        while True:
            detail = self.get_reading_detail(reading_id, resource_type)
            status = detail["data"]["status"]
            if status == "done":
                return detail
            if status == "fail":
                raise PuzleAPIError(
                    code=500,
                    msg=f"Reading {reading_id} processing failed",
                )
            elapsed = time.monotonic() - start
            if elapsed > timeout:
                raise PuzleTimeoutError(
                    f"Reading {reading_id} did not complete within {timeout}s (last status: {status})"
                )
            time.sleep(poll_interval)

    def list_readings(self, page: int = 1, page_size: int = 10) -> dict[str, Any]:
        """List readings with pagination.

        Returns a mixed list of link and file readings, sorted by last_modify_time desc.
        """
        return self._request(
            "GET",
            "/reading/items",
            params={"page": page, "page_size": page_size},
        )

    def search(
        self,
        query: str,
        *,
        reading_ids: list[int] | None = None,
        top_k: int = 5,
    ) -> dict[str, Any]:
        """RAG semantic search across readings.

        Args:
            query: Natural language search query.
            reading_ids: Optional list of reading IDs to restrict search scope.
            top_k: Maximum number of results to return (default 5).

        Returns dict with items containing: reading_id, reading_title,
        resource_type, chunk_text, score.
        """
        payload: dict[str, Any] = {"query": query, "top_k": top_k}
        if reading_ids is not None:
            payload["reading_ids"] = reading_ids
        return self._request("POST", "/reading/search", json=payload)


# ======================================================================
# CLI
# ======================================================================


def _print_json(data: dict[str, Any] | list[Any]) -> None:
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _print_reading_result(result: ReadingResult) -> None:
    _print_json(asdict(result))


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="puzle_reading",
        description="Puzle Reading CLI — save articles, upload files, and search your reading library.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # auth ---------------------------------------------------------------
    p_auth = sub.add_parser(
        "auth",
        help="Authorize via device code (open https://read-web.puzle.com.cn/device-auth to get a code)",
    )
    p_auth.add_argument("code", help="Device authorization code from the web page")

    # status -------------------------------------------------------------
    sub.add_parser("status", help="Check whether a valid token is configured")

    # save-url -----------------------------------------------------------
    p_url = sub.add_parser("save-url", help="Create a reading from a URL")
    p_url.add_argument("url", help="Web article URL to save")

    # save-file ----------------------------------------------------------
    p_file = sub.add_parser(
        "save-file",
        help="Create a reading from a local file (PDF, TXT, MD, CSV, JPG, PNG, WebP, GIF, MP3, WAV)",
    )
    p_file.add_argument("path", help="Path to the local file")

    # save-html ----------------------------------------------------------
    p_html = sub.add_parser(
        "save-html",
        help="Create a reading from pre-fetched HTML content (skips server-side fetching)",
    )
    p_html.add_argument("--url", required=True, help="Original URL of the article")
    p_html.add_argument("--title", required=True, help="Article title")
    p_html.add_argument(
        "--content",
        required=True,
        help='Body HTML string, or "@path" to read from a file',
    )
    p_html.add_argument(
        "--text-content",
        required=True,
        help='Plain text version, or "@path" to read from a file',
    )
    p_html.add_argument("--excerpt", help="Short excerpt (optional)")
    p_html.add_argument("--byline", help="Author name (optional)")
    p_html.add_argument("--site-name", help="Site name (optional)")
    p_html.add_argument("--published-time", help="Published time ISO string (optional)")

    # list ---------------------------------------------------------------
    p_list = sub.add_parser("list", help="List readings in your library")
    p_list.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    p_list.add_argument("--page-size", type=int, default=10, help="Items per page (default: 10, max: 100)")

    # detail -------------------------------------------------------------
    p_detail = sub.add_parser("detail", help="Get full detail of a reading")
    p_detail.add_argument("reading_id", type=int, help="Reading ID")
    p_detail.add_argument("resource_type", choices=["link", "file"], help="Resource type")

    # wait ---------------------------------------------------------------
    p_wait = sub.add_parser("wait", help="Wait for a reading to finish processing, then print detail")
    p_wait.add_argument("reading_id", type=int, help="Reading ID")
    p_wait.add_argument("resource_type", choices=["link", "file"], help="Resource type")
    p_wait.add_argument("--timeout", type=float, default=120.0, help="Max seconds to wait (default: 120)")
    p_wait.add_argument("--interval", type=float, default=3.0, help="Poll interval in seconds (default: 3)")

    # search -------------------------------------------------------------
    p_search = sub.add_parser("search", help="Semantic search across your readings")
    p_search.add_argument("query", help="Natural language search query")
    p_search.add_argument("--top-k", type=int, default=5, help="Max results to return (default: 5)")
    p_search.add_argument("--reading-ids", help="Comma-separated reading IDs to restrict scope (optional)")

    return parser


def _resolve_file_arg(value: str) -> str:
    """If value starts with '@', read content from that file path; otherwise return as-is."""
    if value.startswith("@"):
        return Path(value[1:]).expanduser().read_text()
    return value


def _cmd_auth(args: argparse.Namespace) -> None:
    PuzleReadingClient.exchange_device_code(args.code)
    print("Authorized successfully. Token saved to ~/.config/puzle/config.json")  # noqa: T201


def _cmd_status(_args: argparse.Namespace) -> None:
    if PuzleReadingClient.token_is_configured():
        print("Token is configured.")  # noqa: T201
    else:
        print("No token found. Run: puzle_reading auth <code>")  # noqa: T201
        sys.exit(1)


def _cmd_save_url(args: argparse.Namespace) -> None:
    _print_reading_result(PuzleReadingClient().create_reading_from_url(args.url))


def _cmd_save_file(args: argparse.Namespace) -> None:
    _print_reading_result(PuzleReadingClient().create_reading_from_file(args.path))


def _cmd_save_html(args: argparse.Namespace) -> None:
    result = PuzleReadingClient().create_reading_from_html(
        url=args.url,
        title=args.title,
        content=_resolve_file_arg(args.content),
        text_content=_resolve_file_arg(args.text_content),
        excerpt=args.excerpt,
        byline=args.byline,
        site_name=args.site_name,
        published_time=args.published_time,
    )
    _print_reading_result(result)


def _cmd_list(args: argparse.Namespace) -> None:
    _print_json(PuzleReadingClient().list_readings(page=args.page, page_size=args.page_size))


def _cmd_detail(args: argparse.Namespace) -> None:
    _print_json(PuzleReadingClient().get_reading_detail(args.reading_id, args.resource_type))


def _cmd_wait(args: argparse.Namespace) -> None:
    data = PuzleReadingClient().wait_for_reading(
        args.reading_id, args.resource_type, poll_interval=args.interval, timeout=args.timeout,
    )
    _print_json(data)


def _cmd_search(args: argparse.Namespace) -> None:
    reading_ids: list[int] | None = None
    if args.reading_ids:
        reading_ids = [int(x.strip()) for x in args.reading_ids.split(",")]
    _print_json(PuzleReadingClient().search(args.query, reading_ids=reading_ids, top_k=args.top_k))


_COMMANDS: dict[str, Any] = {
    "auth": _cmd_auth,
    "status": _cmd_status,
    "save-url": _cmd_save_url,
    "save-file": _cmd_save_file,
    "save-html": _cmd_save_html,
    "list": _cmd_list,
    "detail": _cmd_detail,
    "wait": _cmd_wait,
    "search": _cmd_search,
}


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    try:
        _COMMANDS[args.command](args)
    except PuzleAPIError as e:
        print(f"Error: {e}", file=sys.stderr)  # noqa: T201
        sys.exit(1)
    except PuzleTimeoutError as e:
        print(f"Timeout: {e}", file=sys.stderr)  # noqa: T201
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)  # noqa: T201
        sys.exit(1)


if __name__ == "__main__":
    main()
