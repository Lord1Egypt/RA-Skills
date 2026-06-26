#!/usr/bin/env python3

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any, Iterable


DEFAULT_BASE_URL = "https://api.tickflow.org"
DEFAULT_API_KEY_ENV = "TICKFLOW_API_KEY"
DEFAULT_TIMEOUT = 10.0
USER_AGENT = "tickflow-realtime-skill/1.0"


class TickFlowError(Exception):
    pass


class TickFlowAPIError(TickFlowError):
    def __init__(self, status: int, code: str | None, message: str, details: Any = None):
        self.status = status
        self.code = code
        self.message = message
        self.details = details
        super().__init__(self.__str__())

    def __str__(self) -> str:
        parts = [f"HTTP {self.status}"]
        if self.code:
            parts.append(self.code)
        parts.append(self.message)
        return " - ".join(parts)


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def die(message: str, exit_code: int = 1) -> "NoReturn":
    eprint(message)
    raise SystemExit(exit_code)


def parse_csv_arg(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def resolve_api_key() -> str:
    value = os.environ.get(DEFAULT_API_KEY_ENV)
    if value:
        return value

    raise TickFlowError(f"Missing API key. Export {DEFAULT_API_KEY_ENV} before running the script.")


def build_url(base_url: str, path: str, params: dict[str, Any] | None = None) -> str:
    base = base_url.rstrip("/")
    url = f"{base}{path}"
    if not params:
        return url

    filtered = {key: value for key, value in params.items() if value is not None}
    query = urllib.parse.urlencode(filtered, doseq=True)
    return f"{url}?{query}" if query else url


def request_json(
    method: str,
    path: str,
    api_key: str,
    *,
    base_url: str = DEFAULT_BASE_URL,
    params: dict[str, Any] | None = None,
    json_body: dict[str, Any] | None = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> Any:
    headers = {
        "Accept": "application/json",
        "User-Agent": USER_AGENT,
        "x-api-key": api_key,
    }
    data = None
    if json_body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(json_body).encode("utf-8")

    request = urllib.request.Request(
        build_url(base_url, path, params),
        method=method.upper(),
        headers=headers,
        data=data,
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        payload = exc.read().decode("utf-8", errors="replace")
        parsed = _safe_json_loads(payload)
        if isinstance(parsed, dict):
            raise TickFlowAPIError(exc.code, parsed.get("code"), parsed.get("message", payload), parsed.get("details"))
        raise TickFlowAPIError(exc.code, None, payload.strip() or "Request failed")
    except urllib.error.URLError as exc:
        raise TickFlowError(f"Network error: {exc.reason}") from exc

    parsed = _safe_json_loads(payload)
    if parsed is None:
        raise TickFlowError("Response is not valid JSON.")
    return parsed


def _safe_json_loads(text: str) -> Any:
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def ensure_dict(value: Any, *, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TickFlowError(f"{name} must be an object.")
    return value


def ensure_list(value: Any, *, name: str) -> list[Any]:
    if not isinstance(value, list):
        raise TickFlowError(f"{name} must be an array.")
    return value


def format_epoch_ms(value: Any) -> str:
    if value in (None, ""):
        return "-"
    try:
        dt = datetime.fromtimestamp(int(value) / 1000, tz=timezone.utc)
    except (TypeError, ValueError, OSError):
        return str(value)
    return dt.isoformat().replace("+00:00", "Z")


def format_number(value: Any, decimals: int = 2) -> str:
    if value is None:
        return "-"
    if isinstance(value, bool):
        return str(value)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        text = f"{value:.{decimals}f}"
        return text.rstrip("0").rstrip(".")
    return str(value)


def format_percent(value: Any, decimals: int = 2) -> str:
    if value is None:
        return "-"
    try:
        pct = float(value) * 100
    except (TypeError, ValueError):
        return str(value)
    return f"{pct:.{decimals}f}%"


def pad(value: Any, width: int) -> str:
    text = str(value)
    return text if len(text) >= width else text + (" " * (width - len(text)))


def render_table(rows: list[dict[str, Any]], columns: list[tuple[str, str]]) -> str:
    if not rows:
        return "No data returned."

    widths: dict[str, int] = {}
    for key, title in columns:
        widths[key] = len(title)
    for row in rows:
        for key, _ in columns:
            widths[key] = max(widths[key], len(str(row.get(key, "-"))))

    header = "  ".join(pad(title, widths[key]) for key, title in columns)
    divider = "  ".join("-" * widths[key] for key, _ in columns)
    body = []
    for row in rows:
        body.append("  ".join(pad(row.get(key, "-"), widths[key]) for key, _ in columns))
    return "\n".join([header, divider, *body])


def compact_kline_to_rows(data: dict[str, Any]) -> list[dict[str, Any]]:
    data = ensure_dict(data, name="kline data")
    timestamps = ensure_list(data.get("timestamp"), name="data.timestamp")
    row_count = len(timestamps)
    rows: list[dict[str, Any]] = []
    keys = [
        "timestamp",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "amount",
        "prev_close",
        "open_interest",
        "settlement_price",
    ]

    for index in range(row_count):
        row: dict[str, Any] = {}
        for key in keys:
            column = data.get(key)
            if column is None:
                continue
            if not isinstance(column, list):
                raise TickFlowError(f"data.{key} must be an array.")
            if len(column) != row_count:
                raise TickFlowError(f"data.{key} length does not match data.timestamp.")
            row[key] = column[index]
        rows.append(row)
    return rows


def to_pretty_json(value: Any, pretty: bool) -> str:
    if pretty:
        return json.dumps(value, indent=2, ensure_ascii=False)
    return json.dumps(value, ensure_ascii=False)


def join_csv(items: Iterable[str]) -> str:
    return ",".join(item for item in items if item)
