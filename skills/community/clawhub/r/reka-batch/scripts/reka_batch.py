#!/usr/bin/env python3
"""reka-batch: run large, non-urgent LLM jobs on Reka's Batch API at 50% of live rates.

Standard library only (Python 3.9+). Use it as a CLI or import it as a module.

  reka_batch.py make      --items items.csv --prompt prompt.txt --model glm5.3-flash --out requests.jsonl
  reka_batch.py validate  requests.jsonl
  reka_batch.py estimate  requests.jsonl --avg-output 300
  reka_batch.py submit    requests.jsonl --state-dir runs/tickets
  reka_batch.py status    --state-dir runs/tickets
  reka_batch.py wait      --state-dir runs/tickets [--notify-cmd '...']
  reka_batch.py collect   --state-dir runs/tickets
  reka_batch.py cancel    --state-dir runs/tickets
  reka_batch.py cleanup   --state-dir runs/tickets
  reka_batch.py list      [--files]

Environment:
  REKA_API_KEY   required for API calls; never printed or written to disk.
  REKA_BASE_URL  optional. https://api.reka.ai/v1 (default), another https://*.reka.ai
                 endpoint, or an http(s) loopback URL for local testing.

API reference: https://developer.reka.ai/batch/reference
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import secrets
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, Iterator, List, Optional, Tuple

__version__ = "0.1.0"
USER_AGENT = f"reka-batch/{__version__}"

DEFAULT_BASE_URL = "https://api.reka.ai/v1"
ENDPOINT = "/v1/chat/completions"
COMPLETION_WINDOW = "24h"

# Limits from https://developer.reka.ai/batch/reference
MAX_ROWS = 50_000
MAX_FILE_BYTES = 100_000_000
MAX_CUSTOM_ID = 512
MAX_METADATA_PAIRS = 16
MAX_METADATA_KEY = 64
MAX_METADATA_VALUE = 512
MAX_JSON_RESPONSE_BYTES = 8 * 1024 * 1024

TERMINAL_STATUSES = frozenset({"completed", "failed", "expired", "cancelled"})

# Live (synchronous) list prices, USD per million tokens. Batch bills 50% of these,
# including the cache-read rate. Reasoning tokens bill as output.
RATES_AS_OF = "2026-10-28"
RATES_SOURCE = "https://developer.reka.ai/pricing"
LIVE_RATES: Dict[str, Dict[str, float]] = {
    "glm5.3-flash": {"input": 0.15, "cached": 0.015, "output": 0.50},
    "qwen3.8-27b": {"input": 0.20, "cached": 0.05, "output": 2.50},
}
BATCH_FACTOR = 0.5

# Rough token heuristics for estimates only. Real counts come back in batch usage.
DEFAULT_CHARS_PER_TOKEN = 3.5
MESSAGE_OVERHEAD_TOKENS = 4
# Prefix caching, measured on the live Batch API (2026-10-28): a request gets no cache-read
# tokens below CACHE_MIN_TOKENS, and above it the cached prefix is the prompt rounded down to
# a CACHE_BLOCK_TOKENS boundary, minus one block. Same behaviour live and in batch.
CACHE_MIN_TOKENS = 1024
CACHE_BLOCK_TOKENS = 640
DEFAULT_MAX_OUTPUT_GUESS = 4096
LOW_MAX_TOKENS_FOR_REASONING = 1024

EXIT_OK, EXIT_ERROR, EXIT_USAGE, EXIT_INVALID, EXIT_TEMPFAIL = 0, 1, 2, 3, 75


# --------------------------------------------------------------------------- errors

class RekaBatchError(Exception):
    """Base error with a user-facing message."""

    exit_code = EXIT_ERROR


class ValidationFailed(RekaBatchError):
    exit_code = EXIT_INVALID

    def __init__(self, report: Dict[str, Any]):
        self.report = report
        first = "; ".join(f"line {e['line']}: {e['message']}" for e in report["errors"][:3])
        super().__init__(f"{len(report['errors'])} problem(s) in the request file: {first}")


class TransientError(RekaBatchError):
    """Network failure or timeout: the outcome of the call is unknown."""


class UploadUncertain(RekaBatchError):
    exit_code = EXIT_TEMPFAIL


class QueueFull(RekaBatchError):
    exit_code = EXIT_TEMPFAIL

    def __init__(self, retry_after: int):
        self.retry_after = retry_after
        super().__init__(
            f"Reka's batch queue is full (HTTP 429 batch_queue_full). Retry in about {retry_after}s; "
            "rerun the same submit command (the file is already uploaded) or pass --wait-queue."
        )


class RekaAPIError(RekaBatchError):
    def __init__(self, status: int, message: str, *, code: Optional[str] = None,
                 err_type: Optional[str] = None, retry_after: Optional[int] = None):
        self.status, self.code, self.err_type, self.retry_after = status, code, err_type, retry_after
        hint = {
            401: "check REKA_API_KEY",
            403: "the account may be out of credit, or the key cannot use batch",
            404: "wrong or deleted id, or owned by another account",
            409: "idempotency key reused with a different body, or file still in use",
        }.get(status)
        detail = f" ({hint})" if hint else ""
        super().__init__(f"HTTP {status}{' ' + code if code else ''}: {message}{detail}")


# --------------------------------------------------------------------------- utilities

def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def write_jsonl(rows: Iterable[Dict[str, Any]], path: Path) -> int:
    lines = [json.dumps(r, ensure_ascii=False, separators=(",", ":")) for r in rows]
    atomic_write_text(Path(path), "".join(line + "\n" for line in lines))
    return len(lines)


def read_jsonl(path: Path) -> Iterator[Tuple[int, Dict[str, Any]]]:
    with open(path, "r", encoding="utf-8") as fh:
        for lineno, line in enumerate(fh, 1):
            if line.strip():
                yield lineno, json.loads(line)


def fmt_int(n: float) -> str:
    return f"{int(round(n)):,}"


def fmt_tokens(n: float) -> str:
    if n >= 1e6:
        return f"{n / 1e6:.1f}M"
    if n >= 1e3:
        return f"{n / 1e3:.1f}k"
    return str(int(n))


def fmt_usd(x: float) -> str:
    return f"${x:,.4f}" if x < 0.01 else f"${x:,.2f}"


def fmt_duration(seconds: float) -> str:
    seconds = max(0, int(seconds))
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    return f"{h}h {m:02d}m" if h else (f"{m}m {s:02d}s" if m else f"{s}s")


def load_rates(path: Optional[str] = None) -> Dict[str, Dict[str, float]]:
    """Live rates, optionally overridden by a JSON file shaped like LIVE_RATES."""
    rates = {k: dict(v) for k, v in LIVE_RATES.items()}
    src = path or os.environ.get("REKA_BATCH_RATES")
    if src:
        with open(src, "r", encoding="utf-8") as fh:
            for model, r in json.load(fh).items():
                rates[model] = {"input": float(r["input"]), "cached": float(r.get("cached", r["input"])),
                                "output": float(r["output"])}
    return rates


# --------------------------------------------------------------------------- request building

def build_request(custom_id: str, model: str, messages: List[Dict[str, Any]], **params: Any) -> Dict[str, Any]:
    """One batch row: a Chat Completions body plus a custom_id. None-valued params are dropped."""
    body: Dict[str, Any] = {"model": model, "messages": messages}
    body.update({k: v for k, v in params.items() if v is not None})
    return {"custom_id": custom_id, "method": "POST", "url": ENDPOINT, "body": body}


_PLACEHOLDER = re.compile(r"\{\{\s*([A-Za-z0-9_.\-]+)\s*\}\}")


def render_template(template: str, item: Dict[str, Any]) -> str:
    """Replace {{field}} placeholders. Single braces are left alone, so JSON examples survive."""
    missing = sorted({m.group(1) for m in _PLACEHOLDER.finditer(template) if m.group(1) not in item})
    if missing:
        raise RekaBatchError(f"template placeholders with no matching field: {', '.join(missing)}")
    return _PLACEHOLDER.sub(lambda m: "" if item[m.group(1)] is None else str(item[m.group(1)]), template)


def read_items(path: Path) -> List[Dict[str, Any]]:
    if path.suffix.lower() in (".csv", ".tsv"):
        with open(path, newline="", encoding="utf-8-sig") as fh:
            return list(csv.DictReader(fh, delimiter="\t" if path.suffix.lower() == ".tsv" else ","))
    return [row for _, row in read_jsonl(path)]


def make_requests(items: List[Dict[str, Any]], *, prompt: str, model: str, system: Optional[str] = None,
                  id_field: Optional[str] = None, max_tokens: Optional[int] = None,
                  reasoning_effort: Optional[str] = None, json_mode: bool = False,
                  temperature: Optional[float] = None) -> List[Dict[str, Any]]:
    rows, seen = [], set()
    for i, item in enumerate(items):
        cid = str(item.get(id_field)) if id_field else f"row-{i:06d}"
        if id_field and (item.get(id_field) in (None, "")):
            raise RekaBatchError(f"item {i} has no value for id field {id_field!r}")
        if cid in seen:
            raise RekaBatchError(f"duplicate custom_id {cid!r} (item {i})")
        seen.add(cid)
        messages = ([{"role": "system", "content": system}] if system else []) + [
            {"role": "user", "content": render_template(prompt, item)}]
        rows.append(build_request(cid, model, messages, max_tokens=max_tokens, reasoning_effort=reasoning_effort,
                                  temperature=temperature,
                                  response_format={"type": "json_object"} if json_mode else None))
    return rows


# --------------------------------------------------------------------------- validation

def validate_file(path: Path, *, allow_unknown_model: bool = False,
                  known_models: Iterable[str] = LIVE_RATES.keys()) -> Dict[str, Any]:
    """Check a request file against the documented limits before anything is uploaded."""
    path = Path(path)
    errors: List[Dict[str, Any]] = []
    warnings: List[str] = []
    ids: set = set()
    models: Dict[str, int] = {}
    rows = 0
    reasoning_warned = 0
    size = path.stat().st_size

    def err(line: int, message: str) -> None:
        if len(errors) < 100:
            errors.append({"line": line, "message": message})

    if size > MAX_FILE_BYTES:
        err(0, f"file is {size:,} bytes; the limit is {MAX_FILE_BYTES:,}")
    try:
        fh = open(path, "r", encoding="utf-8")
    except OSError as exc:
        raise RekaBatchError(f"cannot read {path}: {exc}") from None
    with fh:
        for lineno, line in enumerate(fh, 1):
            if not line.strip():
                err(lineno, "blank line; use exactly one JSON request per line")
                continue
            rows += 1
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                err(lineno, f"not valid JSON ({exc.msg})")
                continue
            if not isinstance(row, dict):
                err(lineno, "each line must be a JSON object")
                continue
            cid = row.get("custom_id")
            if not isinstance(cid, str) or not cid:
                err(lineno, "custom_id must be a non-empty string")
            elif len(cid) > MAX_CUSTOM_ID:
                err(lineno, f"custom_id is {len(cid)} characters; the limit is {MAX_CUSTOM_ID}")
            elif cid in ids:
                err(lineno, f"duplicate custom_id {cid!r}")
            else:
                ids.add(cid)
            if row.get("method") != "POST":
                err(lineno, 'method must be "POST"')
            if row.get("url") != ENDPOINT:
                err(lineno, f'url must be "{ENDPOINT}"')
            body = row.get("body")
            if not isinstance(body, dict):
                err(lineno, "body must be a Chat Completions request object")
                continue
            model = body.get("model")
            if not isinstance(model, str) or not model:
                err(lineno, "body.model is required")
            else:
                models[model] = models.get(model, 0) + 1
                if model not in known_models and not allow_unknown_model:
                    err(lineno, f"model {model!r} is not offered for batch (use one of: "
                                f"{', '.join(sorted(known_models))}, or --allow-unknown-model)")
            msgs = body.get("messages")
            if not isinstance(msgs, list) or not msgs:
                err(lineno, "body.messages must be a non-empty list")
            if body.get("stream") is True:
                err(lineno, "stream: true is rejected by the Batch API")
            limit = body.get("max_tokens", body.get("max_completion_tokens"))
            if body.get("reasoning_effort") is None and isinstance(limit, int) and limit < LOW_MAX_TOKENS_FOR_REASONING:
                reasoning_warned += 1
    if rows == 0:
        err(0, "the file has no requests")
    if rows > MAX_ROWS:
        err(0, f"{rows:,} requests; the limit is {MAX_ROWS:,} per file (split it)")
    if len(models) > 1:
        err(0, f"one model per file; found {', '.join(f'{m} ({n})' for m, n in sorted(models.items()))}")
    if reasoning_warned:
        warnings.append(
            f"{reasoning_warned} row(s) set max_tokens < {LOW_MAX_TOKENS_FOR_REASONING} without reasoning_effort. "
            "These models think before answering, so thinking can use the whole budget and content comes back "
            'empty. Set "reasoning_effort": "none" for short answers, or raise max_tokens.')
    return {"path": str(path), "rows": rows, "bytes": size, "model": next(iter(models), None),
            "errors": errors, "warnings": warnings, "ok": not errors}


# --------------------------------------------------------------------------- estimation

def _message_text(msg: Dict[str, Any]) -> Tuple[str, int]:
    content, images = msg.get("content"), 0
    if isinstance(content, str):
        text = content
    elif isinstance(content, list):
        chunks = []
        for part in content:
            if isinstance(part, dict) and part.get("type") == "text":
                chunks.append(str(part.get("text", "")))
            elif isinstance(part, dict) and part.get("type") in ("image_url", "input_image", "image"):
                images += 1
        text = "".join(chunks)
    else:
        text = ""
    if msg.get("tool_calls"):
        text += json.dumps(msg["tool_calls"], sort_keys=True, separators=(",", ":"))
    return f"<{msg.get('role', '')}>\n{text}\n", images


def prompt_text(body: Dict[str, Any]) -> Tuple[str, int]:
    """The request as one string, in roughly the order a chat template renders it."""
    parts, images = [], 0
    for key in ("tools", "response_format"):
        if body.get(key):
            parts.append(json.dumps(body[key], sort_keys=True, separators=(",", ":")))
    for msg in body.get("messages") or []:
        text, n = _message_text(msg if isinstance(msg, dict) else {})
        parts.append(text)
        images += n
    return "".join(parts), images


def cost_usd(rates: Dict[str, float], *, uncached_in: float, cached_in: float, out: float,
             batch: bool) -> float:
    factor = BATCH_FACTOR if batch else 1.0
    return factor * (uncached_in * rates["input"] + cached_in * rates["cached"] + out * rates["output"]) / 1e6


def estimate_file(path: Path, *, avg_output: Optional[float] = None, chars_per_token: float = DEFAULT_CHARS_PER_TOKEN,
                  rates: Optional[Dict[str, Dict[str, float]]] = None) -> Dict[str, Any]:
    """Rough pre-flight cost: no-cache vs ideal-cache, live vs batch."""
    rates = rates or load_rates()
    prompts: List[str] = []
    in_tokens = 0.0
    max_out = 0.0
    images = 0
    model = None
    for _, row in read_jsonl(Path(path)):
        body = row.get("body") or {}
        model = model or body.get("model")
        text, n_img = prompt_text(body)
        prompts.append(text)
        images += n_img
        in_tokens += len(text) / chars_per_token + MESSAGE_OVERHEAD_TOKENS * len(body.get("messages") or [])
        limit = body.get("max_tokens", body.get("max_completion_tokens"))
        max_out += limit if isinstance(limit, int) and limit > 0 else DEFAULT_MAX_OUTPUT_GUESS
    n = len(prompts)
    if not n:
        raise RekaBatchError("the file has no requests")
    prefix = os.path.commonprefix(prompts) if n > 1 else ""
    prefix_tokens = len(prefix) / chars_per_token
    # A prefix only earns cache reads if it clears the minimum and the block rounding leaves
    # something behind; below that every row pays full input price.
    if prefix_tokens < CACHE_MIN_TOKENS:
        cacheable_per_row = 0.0
    else:
        cacheable_per_row = max(0.0, (int(prefix_tokens) // CACHE_BLOCK_TOKENS) * CACHE_BLOCK_TOKENS
                                - CACHE_BLOCK_TOKENS)
    cacheable = cacheable_per_row * (n - 1)
    if model not in rates:
        raise RekaBatchError(f"no rates for model {model!r}; pass --rates with a JSON price table")
    r = rates[model]
    scenarios = {}
    out_cases = {"expected": avg_output * n if avg_output else None, "worst": max_out}
    for label, out in out_cases.items():
        if out is None:
            continue
        scenarios[label] = {
            "output_tokens": out,
            "live_no_cache": cost_usd(r, uncached_in=in_tokens, cached_in=0, out=out, batch=False),
            "live_ideal_cache": cost_usd(r, uncached_in=in_tokens - cacheable, cached_in=cacheable, out=out, batch=False),
            "batch_no_cache": cost_usd(r, uncached_in=in_tokens, cached_in=0, out=out, batch=True),
            "batch_ideal_cache": cost_usd(r, uncached_in=in_tokens - cacheable, cached_in=cacheable, out=out, batch=True),
        }
    return {"path": str(path), "rows": n, "model": model, "input_tokens": in_tokens,
            "shared_prefix_tokens": prefix_tokens, "cacheable_tokens": cacheable, "images": images,
            "chars_per_token": chars_per_token, "scenarios": scenarios, "rates": r,
            "rates_as_of": RATES_AS_OF, "rates_source": RATES_SOURCE}


def format_estimate(est: Dict[str, Any]) -> str:
    lines = [f"{est['path']}: {fmt_int(est['rows'])} rows, model {est['model']}",
             f"Input  ~{fmt_tokens(est['input_tokens'])} tokens; shared prefix ~{fmt_tokens(est['shared_prefix_tokens'])}"
             f" per row (up to {fmt_tokens(est['cacheable_tokens'])} cacheable)"]
    for label, s in est["scenarios"].items():
        title = "Expected output" if label == "expected" else "Worst case (every row uses max_tokens)"
        lines += ["", f"{title}: ~{fmt_tokens(s['output_tokens'])} output tokens",
                  f"  {'':18}{'no cache hits':>15}{'ideal cache hits':>18}",
                  f"  {'Live (list price)':18}{fmt_usd(s['live_no_cache']):>15}{fmt_usd(s['live_ideal_cache']):>18}",
                  f"  {'Batch (50% off)':18}{fmt_usd(s['batch_no_cache']):>15}{fmt_usd(s['batch_ideal_cache']):>18}"]
    if "expected" not in est["scenarios"]:
        lines.append("\nPass --avg-output N (typical output tokens per row) for an expected figure.")
    notes = [f"~{est['chars_per_token']} characters per token"]
    if est["images"]:
        notes.append(f"{est['images']} image(s) not counted")
    if est["shared_prefix_tokens"] < CACHE_MIN_TOKENS:
        notes.append(f"prefix under {CACHE_MIN_TOKENS} tokens, so it gets no cache hits at all; "
                     f"move more shared text to the front to reach the cache-read rate")
    else:
        notes.append(f"prefix caching starts at {CACHE_MIN_TOKENS} tokens and rounds down to "
                     f"{CACHE_BLOCK_TOKENS}-token blocks, so the cached part can be smaller than the prefix")
    notes.append("reasoning tokens bill as output")
    lines += ["", "Rough estimate: " + "; ".join(notes) + ".",
              f"Rates as of {est['rates_as_of']}: {est['rates_source']}"]
    return "\n".join(lines)


# --------------------------------------------------------------------------- HTTP client

def resolve_base_url(value: Optional[str] = None) -> str:
    url = (value or os.environ.get("REKA_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
    parts = urllib.parse.urlsplit(url)
    if parts.username or parts.password or parts.query or parts.fragment:
        raise RekaBatchError("REKA_BASE_URL must not contain credentials, a query or a fragment")
    host = (parts.hostname or "").lower()
    if parts.scheme == "https" and (host == "reka.ai" or host.endswith(".reka.ai")):
        return url
    if parts.scheme in ("http", "https") and host in ("127.0.0.1", "localhost", "::1"):
        return url
    raise RekaBatchError("REKA_BASE_URL must be https://api.reka.ai/v1 (or another https://*.reka.ai "
                         "endpoint), or a loopback URL for local testing")


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Never follow a redirect: urllib would forward the Authorization header to the new host."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D401
        raise RekaAPIError(code, f"refusing to follow a redirect to {newurl} with the API key attached")


class BatchClient:
    """Thin client for /v1/files and /v1/batches."""

    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, timeout: float = 60.0,
                 sleep: Callable[[float], None] = time.sleep):
        key = api_key if api_key is not None else os.environ.get("REKA_API_KEY", "")
        if not key.strip():
            raise RekaBatchError("set REKA_API_KEY (get a key at https://developer.reka.ai/keys)")
        self._key = key.strip()
        self.base_url = resolve_base_url(base_url)
        self.timeout = timeout
        self._sleep = sleep
        self._opener = urllib.request.build_opener(_NoRedirect)

    def __repr__(self) -> str:  # never show the key
        return f"BatchClient(base_url={self.base_url!r})"

    # -- transport
    def _url(self, path: str, query: Optional[Dict[str, Any]] = None) -> str:
        path = path[3:] if path.startswith("/v1/") else path
        url = self.base_url + (path if path.startswith("/") else "/" + path)
        if query:
            q = {k: v for k, v in query.items() if v is not None}
            if q:
                url += "?" + urllib.parse.urlencode(q)
        return url

    def _send(self, method: str, url: str, *, data: Optional[bytes] = None,
              headers: Optional[Dict[str, str]] = None, stream_to: Optional[Path] = None) -> Any:
        hdrs = {"Authorization": f"Bearer {self._key}", "Accept": "application/json", "User-Agent": USER_AGENT}
        hdrs.update(headers or {})
        req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
        try:
            resp = self._opener.open(req, timeout=self.timeout)
        except urllib.error.HTTPError as exc:
            raise self._api_error(exc) from None
        except RekaAPIError:
            raise
        except (urllib.error.URLError, socket.timeout, TimeoutError, ConnectionError, OSError) as exc:
            reason = getattr(exc, "reason", exc)
            raise TransientError(f"{method} {urllib.parse.urlsplit(url).path}: {reason}") from None
        with resp:
            if stream_to is not None:
                stream_to.parent.mkdir(parents=True, exist_ok=True)
                tmp = stream_to.with_name(stream_to.name + ".part")
                with open(tmp, "wb") as fh:
                    shutil.copyfileobj(resp, fh, 1 << 20)
                os.replace(tmp, stream_to)
                return None
            raw = resp.read(MAX_JSON_RESPONSE_BYTES + 1)
        if len(raw) > MAX_JSON_RESPONSE_BYTES:
            raise RekaBatchError(f"response from {urllib.parse.urlsplit(url).path} is too large")
        try:
            return json.loads(raw.decode("utf-8")) if raw else {}
        except (UnicodeDecodeError, json.JSONDecodeError):
            raise RekaBatchError(f"malformed JSON from {urllib.parse.urlsplit(url).path}") from None

    @staticmethod
    def _api_error(exc: urllib.error.HTTPError) -> RekaAPIError:
        message, code, err_type = exc.reason or "request failed", None, None
        try:
            payload = json.loads(exc.read(64 * 1024).decode("utf-8"))
            e = payload.get("error", payload) if isinstance(payload, dict) else {}
            message = e.get("message") or message
            code, err_type = e.get("code"), e.get("type")
        except Exception:
            pass
        retry_after = None
        ra = exc.headers.get("Retry-After") if exc.headers else None
        if ra and str(ra).strip().isdigit():
            retry_after = int(str(ra).strip())
        return RekaAPIError(exc.code, str(message), code=code, err_type=err_type, retry_after=retry_after)

    def _with_retries(self, fn: Callable[[], Any], *, attempts: int = 4) -> Any:
        delay = 1.0
        for attempt in range(1, attempts + 1):
            try:
                return fn()
            except TransientError:
                if attempt == attempts:
                    raise
            except RekaAPIError as exc:
                if exc.status == 429 and exc.code == "batch_queue_full":
                    raise
                if not (exc.status >= 500 or exc.status == 429) or attempt == attempts:
                    raise
                if exc.retry_after:
                    delay = min(max(delay, exc.retry_after), 60)
            self._sleep(delay)
            delay = min(delay * 2, 30)
        raise AssertionError("unreachable")

    def _json(self, method: str, path: str, *, body: Optional[Dict[str, Any]] = None,
              query: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None,
              retry: bool = True) -> Dict[str, Any]:
        data = json.dumps(body).encode("utf-8") if body is not None else None
        hdrs = dict(headers or {})
        if data is not None:
            hdrs["Content-Type"] = "application/json"
        call = lambda: self._send(method, self._url(path, query), data=data, headers=hdrs)  # noqa: E731
        return self._with_retries(call) if retry else call()

    # -- files
    def upload_file(self, path: Path, filename: Optional[str] = None) -> Dict[str, Any]:
        """Upload a JSONL file with purpose=batch. Not retried: an upload has no idempotency key."""
        payload = Path(path).read_bytes()
        boundary = "reka-batch-" + secrets.token_hex(16)
        name = (filename or Path(path).name).replace('"', "")
        body = b"".join([
            f'--{boundary}\r\nContent-Disposition: form-data; name="purpose"\r\n\r\nbatch\r\n'.encode(),
            f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{name}"\r\n'
            f"Content-Type: application/jsonl\r\n\r\n".encode(),
            payload, f"\r\n--{boundary}--\r\n".encode()])
        return self._send("POST", self._url("/files"), data=body,
                          headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})

    def list_files(self, purpose: Optional[str] = "batch", limit: int = 100, order: str = "desc",
                   after: Optional[str] = None) -> Dict[str, Any]:
        return self._json("GET", "/files", query={"purpose": purpose, "limit": limit, "order": order, "after": after})

    def iter_files(self, purpose: Optional[str] = "batch", max_items: int = 1000) -> Iterator[Dict[str, Any]]:
        after, seen = None, 0
        while seen < max_items:
            page = self.list_files(purpose=purpose, limit=min(100, max_items - seen), after=after)
            data = page.get("data") or []
            for f in data:
                yield f
            seen += len(data)
            if not page.get("has_more") or not data:
                return
            after = page.get("last_id") or data[-1]["id"]

    def download_file(self, file_id: str, dest: Path) -> Path:
        self._with_retries(lambda: self._send("GET", self._url(f"/files/{file_id}/content"), stream_to=Path(dest)))
        return Path(dest)

    def delete_file(self, file_id: str) -> Dict[str, Any]:
        return self._json("DELETE", f"/files/{file_id}")

    # -- batches
    def create_batch(self, input_file_id: str, *, metadata: Optional[Dict[str, str]] = None,
                     idempotency_key: Optional[str] = None) -> Dict[str, Any]:
        body: Dict[str, Any] = {"input_file_id": input_file_id, "endpoint": ENDPOINT,
                                "completion_window": COMPLETION_WINDOW}
        if metadata:
            body["metadata"] = metadata
        headers = {"Idempotency-Key": idempotency_key} if idempotency_key else None
        # Safe to retry only because the idempotency key returns the original batch.
        return self._json("POST", "/batches", body=body, headers=headers, retry=bool(idempotency_key))

    def get_batch(self, batch_id: str) -> Dict[str, Any]:
        return self._json("GET", f"/batches/{batch_id}")

    def list_batches(self, limit: int = 20, after: Optional[str] = None) -> Dict[str, Any]:
        return self._json("GET", "/batches", query={"limit": limit, "after": after})

    def cancel_batch(self, batch_id: str) -> Dict[str, Any]:
        return self._json("POST", f"/batches/{batch_id}/cancel")


# --------------------------------------------------------------------------- run state

STATE_FILE = "state.json"
REQUESTS_FILE = "requests.jsonl"


def load_state(state_dir: Path) -> Dict[str, Any]:
    p = Path(state_dir) / STATE_FILE
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def save_state(state_dir: Path, state: Dict[str, Any]) -> None:
    atomic_write_text(Path(state_dir) / STATE_FILE, json.dumps(state, indent=2, sort_keys=True) + "\n")


def parse_metadata(pairs: Iterable[str]) -> Dict[str, str]:
    meta: Dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise RekaBatchError(f"metadata must be key=value, got {pair!r}")
        k, v = pair.split("=", 1)
        if not k or len(k) > MAX_METADATA_KEY or len(v) > MAX_METADATA_VALUE:
            raise RekaBatchError(f"metadata key 1-{MAX_METADATA_KEY} chars, value up to {MAX_METADATA_VALUE}")
        meta[k] = v
    if len(meta) > MAX_METADATA_PAIRS:
        raise RekaBatchError(f"at most {MAX_METADATA_PAIRS} metadata pairs")
    return meta


def _recover_upload(client: BatchClient, state: Dict[str, Any], state_dir: Path) -> Optional[str]:
    """Find an earlier upload of exactly this file (name, size, then content hash)."""
    for f in client.iter_files(purpose="batch", max_items=1000):
        if f.get("filename") != state["upload_filename"] or f.get("bytes") != state["input_bytes"]:
            continue
        probe = Path(state_dir) / "raw" / f"recovered-{f['id']}.jsonl"
        client.download_file(f["id"], probe)
        try:
            if sha256_file(probe) == state["input_sha256"]:
                return f["id"]
        finally:
            probe.unlink(missing_ok=True)
    return None


def submit(input_path: Path, state_dir: Path, *, client: BatchClient, metadata: Optional[Dict[str, str]] = None,
           wait_queue: bool = False, queue_timeout: float = 4 * 3600, reupload: bool = False,
           allow_unknown_model: bool = False, sleep: Callable[[float], None] = time.sleep) -> Dict[str, Any]:
    """Validate, upload once, create once. Safe to rerun with the same state dir after any failure."""
    input_path, state_dir = Path(input_path), Path(state_dir)
    report = validate_file(input_path, allow_unknown_model=allow_unknown_model)
    if not report["ok"]:
        raise ValidationFailed(report)
    for w in report["warnings"]:
        log(f"warning: {w}")
    digest = sha256_file(input_path)
    state = load_state(state_dir)
    if state.get("input_sha256") and state["input_sha256"] != digest:
        raise RekaBatchError(f"{state_dir} already tracks a different request file; use a new --state-dir")
    if state.get("batch_id"):
        log(f"Already submitted as {state['batch_id']}; checking its status.")
        return client.get_batch(state["batch_id"])
    if not state:
        state = {"version": 1, "nonce": secrets.token_hex(8), "input_sha256": digest,
                 "input_bytes": report["bytes"], "input_rows": report["rows"], "model": report["model"],
                 "base_url": client.base_url, "source": str(input_path.resolve())}
        state["upload_filename"] = f"{input_path.stem[:80]}-{state['nonce']}-{digest[:12]}.jsonl"
        state_dir.mkdir(parents=True, exist_ok=True)
        save_state(state_dir, state)
    local_copy = state_dir / REQUESTS_FILE
    if local_copy.resolve() != input_path.resolve():
        shutil.copyfile(input_path, local_copy)

    if not state.get("file_id"):
        if state.get("upload_uncertain") and not reupload:
            log("A previous upload's outcome is unknown; looking for it in your files…")
            found = _recover_upload(client, state, state_dir)
            if not found:
                raise UploadUncertain(
                    "The last upload may or may not have reached Reka, and no matching file was found. "
                    "Check `reka_batch.py list --files`, then rerun with --reupload to upload again.")
            log(f"Found the earlier upload: {found}")
            state.update(file_id=found, upload_uncertain=False)
            save_state(state_dir, state)
        else:
            state["upload_uncertain"] = True  # recorded first, so a crash mid-upload is detectable
            save_state(state_dir, state)
            log(f"Uploading {fmt_int(report['rows'])} requests ({report['bytes']:,} bytes)…")
            try:
                uploaded = client.upload_file(local_copy, filename=state["upload_filename"])
            except TransientError as exc:
                raise UploadUncertain(f"Upload outcome unknown ({exc}). Rerun the same command: it looks for "
                                      "the file before uploading again.") from None
            except RekaAPIError as exc:
                if exc.status >= 500:
                    raise UploadUncertain(f"Upload outcome unknown ({exc}). Rerun the same command.") from None
                state["upload_uncertain"] = False
                save_state(state_dir, state)
                raise
            state.update(file_id=uploaded["id"], upload_uncertain=False)
            save_state(state_dir, state)

    key = f"reka-batch-{state['nonce']}-{digest[:24]}"
    deadline = time.monotonic() + queue_timeout
    while True:
        try:
            batch = client.create_batch(state["file_id"], metadata=metadata, idempotency_key=key)
            break
        except RekaAPIError as exc:
            if exc.status == 429 and exc.code == "batch_queue_full":
                wait_s = exc.retry_after or 300
                if not wait_queue or time.monotonic() + wait_s > deadline:
                    raise QueueFull(wait_s) from None
                log(f"Batch queue full; retrying in {wait_s}s (same file, same idempotency key).")
                sleep(wait_s)
                continue
            raise
    state.update(batch_id=batch["id"], created_at=batch.get("created_at"), expires_at=batch.get("expires_at"))
    save_state(state_dir, state)
    return batch


# --------------------------------------------------------------------------- status, wait, collect

def batch_line(batch: Dict[str, Any], now: Optional[float] = None) -> str:
    now = now or time.time()
    c = batch.get("request_counts") or {}
    total, done, failed = c.get("total", 0), c.get("completed", 0), c.get("failed", 0)
    parts = [batch.get("id", "?"), batch.get("status", "?"), f"{fmt_int(done)}/{fmt_int(total)} done"]
    if failed:
        parts.append(f"{fmt_int(failed)} failed")
    if batch.get("created_at"):
        parts.append(f"started {fmt_duration(now - batch['created_at'])} ago")
    if batch.get("status") not in TERMINAL_STATUSES and batch.get("expires_at"):
        parts.append(f"window closes in {fmt_duration(batch['expires_at'] - now)}")
    return "  ".join(parts)


_SAFE = re.compile(r"^[A-Za-z0-9_.\-]{1,200}$")


def _notify(cmd: str, batch: Dict[str, Any], state_dir: Path) -> None:
    c = batch.get("request_counts") or {}
    env = dict(os.environ)
    env.pop("REKA_API_KEY", None)  # the hook never needs the key
    for name, value in (("RB_BATCH_ID", batch.get("id")), ("RB_STATUS", batch.get("status")),
                        ("RB_TOTAL", c.get("total", 0)), ("RB_COMPLETED", c.get("completed", 0)),
                        ("RB_FAILED", c.get("failed", 0))):
        s = str(value)
        env[name] = s if _SAFE.match(s) else "unknown"
    env["RB_STATE_DIR"] = str(Path(state_dir).resolve())
    try:
        subprocess.run(cmd, shell=True, env=env, timeout=60, check=False)  # the user's own command
    except subprocess.TimeoutExpired:
        log("warning: --notify-cmd timed out after 60s")


def wait(state_dir: Path, *, client: BatchClient, interval: float = 60.0, max_wait: float = 25 * 3600,
         notify_cmd: Optional[str] = None, sleep: Callable[[float], None] = time.sleep,
         on_update: Callable[[str], None] = log) -> Dict[str, Any]:
    state = _require_batch(state_dir)
    started, last_line, backoff = time.monotonic(), None, interval
    while True:
        try:
            batch = client.get_batch(state["batch_id"])
            backoff = interval
        except (TransientError, RekaAPIError) as exc:
            if isinstance(exc, RekaAPIError) and exc.status < 500 and exc.status != 429:
                raise
            on_update(f"status check failed ({exc}); retrying")
            backoff = min(backoff * 2, 15 * 60)
            sleep(backoff)
            continue
        line = batch_line(batch)
        status_key = (batch.get("status"), (batch.get("request_counts") or {}).get("completed"))
        if status_key != last_line:
            on_update(line)
            last_line = status_key
        if batch.get("status") in TERMINAL_STATUSES:
            if notify_cmd:
                _notify(notify_cmd, batch, state_dir)
            return batch
        if time.monotonic() - started > max_wait:
            raise RekaBatchError(f"still {batch.get('status')} after {fmt_duration(max_wait)}; rerun wait later")
        sleep(max(1.0, interval))


def _require_batch(state_dir: Path) -> Dict[str, Any]:
    state = load_state(state_dir)
    if not state.get("batch_id"):
        raise RekaBatchError(f"no submitted batch in {state_dir} (run submit first)")
    return state


def _parse_result_row(row: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {"custom_id": row.get("custom_id"), "ok": False}
    if row.get("error"):
        e = row["error"]
        out["error"] = {"code": e.get("code"), "message": e.get("message")}
        return out
    resp = row.get("response") or {}
    status = resp.get("status_code")
    body = resp.get("body") or {}
    out["status_code"] = status
    if status != 200:
        e = body.get("error") if isinstance(body, dict) else None
        out["error"] = {"code": (e or {}).get("code") or f"http_{status}", "message": (e or {}).get("message")}
        return out
    choice = (body.get("choices") or [{}])[0]
    msg = choice.get("message") or {}
    content = msg.get("content")
    out.update(finish_reason=choice.get("finish_reason"), usage=body.get("usage"), content=content)
    if msg.get("tool_calls"):
        out["tool_calls"] = msg["tool_calls"]
    if (content is None or (isinstance(content, str) and not content.strip())) and not msg.get("tool_calls"):
        out["error"] = {"code": "empty_content",
                        "message": f"finish_reason={choice.get('finish_reason')}; thinking may have used the "
                                   "max_tokens budget (raise max_tokens or set reasoning_effort)"}
        return out
    out["ok"] = True
    if choice.get("finish_reason") == "length":
        out["truncated"] = True
    return out


def usage_cost(batch: Dict[str, Any], rates: Optional[Dict[str, Dict[str, float]]] = None) -> Optional[Dict[str, Any]]:
    """Actual tokens from the batch object, priced at batch and at live rates."""
    usage = batch.get("usage") or {}
    model = batch.get("model")
    rates = rates or load_rates()
    if not usage or model not in rates:
        return None
    total_in = usage.get("input_tokens", 0) or 0
    cached = ((usage.get("input_tokens_details") or {}).get("cached_tokens", 0)) or 0
    out = usage.get("output_tokens", 0) or 0
    reasoning = ((usage.get("output_tokens_details") or {}).get("reasoning_tokens", 0)) or 0
    r = rates[model]
    batch_cost = cost_usd(r, uncached_in=total_in - cached, cached_in=cached, out=out, batch=True)
    live_cost = cost_usd(r, uncached_in=total_in - cached, cached_in=cached, out=out, batch=False)
    return {"model": model, "input_tokens": total_in, "cached_tokens": cached, "output_tokens": out,
            "reasoning_tokens": reasoning, "batch_cost_usd": round(batch_cost, 6),
            "live_equivalent_usd": round(live_cost, 6), "saved_usd": round(live_cost - batch_cost, 6),
            "rates_as_of": RATES_AS_OF}


def collect(state_dir: Path, *, client: BatchClient, bump_max_tokens: Optional[float] = None,
            rates: Optional[Dict[str, Dict[str, float]]] = None) -> Dict[str, Any]:
    """Download results, join them to the requests, write results/retry/summary files."""
    state_dir = Path(state_dir)
    state = _require_batch(state_dir)
    batch = client.get_batch(state["batch_id"])
    if batch.get("status") not in TERMINAL_STATUSES:
        raise RekaBatchError(f"batch is {batch.get('status')}; results appear once it finishes ({batch_line(batch)})")
    raw = state_dir / "raw"
    sources = []
    for key, name in (("output_file_id", "output.jsonl"), ("error_file_id", "errors.jsonl")):
        if batch.get(key):
            sources.append(client.download_file(batch[key], raw / name))

    requests: Dict[str, str] = {}
    order: List[str] = []
    with open(state_dir / REQUESTS_FILE, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                cid = json.loads(line)["custom_id"]
                requests[cid] = line.rstrip("\n")
                order.append(cid)

    results: Dict[str, Dict[str, Any]] = {}
    for src in sources:
        for _, row in read_jsonl(src):
            parsed = _parse_result_row(row)
            cid = parsed["custom_id"]
            if cid in requests and (cid not in results or parsed["ok"]):
                results[cid] = parsed
    for cid in order:
        results.setdefault(cid, {"custom_id": cid, "ok": False,
                                 "error": {"code": "missing", "message": "no result row came back"}})

    write_jsonl((results[cid] for cid in order), state_dir / "results.jsonl")
    retry_rows, codes = [], {}
    for cid in order:
        res = results[cid]
        if res["ok"]:
            continue
        code = (res.get("error") or {}).get("code") or "unknown"
        codes[code] = codes.get(code, 0) + 1
        req = json.loads(requests[cid])
        if bump_max_tokens and code == "empty_content":
            body = req["body"]
            cur = body.get("max_tokens") or LOW_MAX_TOKENS_FOR_REASONING
            body["max_tokens"] = int(max(LOW_MAX_TOKENS_FOR_REASONING, cur * bump_max_tokens))
        retry_rows.append(req)
    retry_path = state_dir / "retry.jsonl"
    if retry_rows:
        write_jsonl(retry_rows, retry_path)
    elif retry_path.exists():
        retry_path.unlink()

    ok = sum(1 for r in results.values() if r["ok"])
    summary = {"batch_id": batch["id"], "status": batch.get("status"), "model": batch.get("model"),
               "rows": len(order), "succeeded": ok, "failed": len(order) - ok,
               "truncated": sum(1 for r in results.values() if r.get("truncated")),
               "error_codes": codes, "results_file": str(state_dir / "results.jsonl"),
               "retry_file": str(retry_path) if retry_rows else None,
               "cost": usage_cost(batch, rates)}
    atomic_write_text(state_dir / "summary.json", json.dumps(summary, indent=2) + "\n")
    state.update(collected=True, output_file_id=batch.get("output_file_id"), error_file_id=batch.get("error_file_id"))
    save_state(state_dir, state)
    return summary


def format_summary(s: Dict[str, Any]) -> str:
    lines = [f"{s['batch_id']} {s['status']}: {fmt_int(s['succeeded'])}/{fmt_int(s['rows'])} rows succeeded"
             + (f", {fmt_int(s['failed'])} failed" if s["failed"] else "")
             + (f", {fmt_int(s['truncated'])} cut off at max_tokens" if s["truncated"] else "")]
    if s["error_codes"]:
        lines.append("Failures: " + ", ".join(f"{k} x{v}" for k, v in sorted(s["error_codes"].items())))
    c = s.get("cost")
    if c:
        lines.append(f"Tokens: {fmt_tokens(c['input_tokens'])} in ({fmt_tokens(c['cached_tokens'])} cached), "
                     f"{fmt_tokens(c['output_tokens'])} out ({fmt_tokens(c['reasoning_tokens'])} reasoning)")
        lines.append(f"Cost: {fmt_usd(c['batch_cost_usd'])} at batch rates "
                     f"(live would be {fmt_usd(c['live_equivalent_usd'])}; saved {fmt_usd(c['saved_usd'])})")
    lines.append(f"Results: {s['results_file']}")
    if s.get("retry_file"):
        lines.append(f"Retry file: {s['retry_file']} (read the error codes first; submit it with a new --state-dir)")
    return "\n".join(lines)


def cleanup(state_dir: Path, *, client: BatchClient, force: bool = False) -> List[str]:
    """Delete this run's input and result files from Reka (they otherwise stay up to 31 days)."""
    state = load_state(state_dir)
    if state.get("batch_id") and not state.get("collected") and not force:
        raise RekaBatchError("results not collected yet; run collect first (or pass --force)")
    if state.get("batch_id"):
        batch = client.get_batch(state["batch_id"])
        if batch.get("status") not in TERMINAL_STATUSES:
            raise RekaBatchError("the batch is still running; cancel it or wait before deleting its files")
        ids = [state.get("file_id"), batch.get("output_file_id"), batch.get("error_file_id")]
    else:
        ids = [state.get("file_id")]
    deleted = []
    for fid in [i for i in ids if i]:
        try:
            client.delete_file(fid)
            deleted.append(fid)
        except RekaAPIError as exc:
            if exc.status != 404:
                raise
    state["deleted_files"] = sorted(set(state.get("deleted_files", [])) | set(deleted))
    save_state(state_dir, state)
    return deleted


# --------------------------------------------------------------------------- CLI

def _client(args: argparse.Namespace) -> BatchClient:
    return BatchClient(base_url=getattr(args, "base_url", None))


def _emit(args: argparse.Namespace, data: Any, text: str) -> None:
    print(json.dumps(data, indent=2, default=str) if args.json else text)


def cmd_make(args: argparse.Namespace) -> int:
    items = read_items(Path(args.items))
    prompt = Path(args.prompt).read_text(encoding="utf-8")
    system = Path(args.system).read_text(encoding="utf-8") if args.system else None
    rows = make_requests(items, prompt=prompt, model=args.model, system=system, id_field=args.id_field,
                         max_tokens=args.max_tokens, reasoning_effort=args.reasoning, json_mode=args.json_mode,
                         temperature=args.temperature)
    n = write_jsonl(rows, Path(args.out))
    report = validate_file(Path(args.out), allow_unknown_model=args.allow_unknown_model)
    _emit(args, {"written": n, "out": args.out, "validation": report},
          f"Wrote {fmt_int(n)} requests to {args.out}" + "".join(f"\nwarning: {w}" for w in report["warnings"])
          + "".join(f"\nerror: line {e['line']}: {e['message']}" for e in report["errors"]))
    return EXIT_OK if report["ok"] else EXIT_INVALID


def cmd_validate(args: argparse.Namespace) -> int:
    r = validate_file(Path(args.file), allow_unknown_model=args.allow_unknown_model)
    text = (f"OK: {fmt_int(r['rows'])} requests, {r['bytes']:,} bytes, model {r['model']}" if r["ok"]
            else f"{len(r['errors'])} problem(s):" + "".join(f"\n  line {e['line']}: {e['message']}" for e in r["errors"]))
    text += "".join(f"\nwarning: {w}" for w in r["warnings"])
    _emit(args, r, text)
    return EXIT_OK if r["ok"] else EXIT_INVALID


def cmd_estimate(args: argparse.Namespace) -> int:
    est = estimate_file(Path(args.file), avg_output=args.avg_output, chars_per_token=args.chars_per_token,
                        rates=load_rates(args.rates))
    _emit(args, est, format_estimate(est))
    return EXIT_OK


def cmd_submit(args: argparse.Namespace) -> int:
    batch = submit(Path(args.file), Path(args.state_dir), client=_client(args),
                   metadata=parse_metadata(args.metadata or []), wait_queue=args.wait_queue,
                   reupload=args.reupload, allow_unknown_model=args.allow_unknown_model)
    text = (f"Submitted {batch['id']} ({batch.get('status')}). Results arrive within 24 hours"
            + (f", by {time.strftime('%Y-%m-%d %H:%M %Z', time.localtime(batch['expires_at']))}"
               if batch.get("expires_at") else "")
            + f".\nCheck:   {Path(sys.argv[0]).name} status --state-dir {args.state_dir}"
            + f"\nCollect: {Path(sys.argv[0]).name} collect --state-dir {args.state_dir}")
    _emit(args, batch, text)
    return EXIT_OK


def cmd_status(args: argparse.Namespace) -> int:
    client = _client(args)
    batch_id = args.batch_id or _require_batch(Path(args.state_dir))["batch_id"]
    batch = client.get_batch(batch_id)
    _emit(args, batch, batch_line(batch))
    return EXIT_OK


def cmd_wait(args: argparse.Namespace) -> int:
    batch = wait(Path(args.state_dir), client=_client(args), interval=args.interval,
                 max_wait=args.max_wait_hours * 3600, notify_cmd=args.notify_cmd)
    _emit(args, batch, batch_line(batch))
    return EXIT_OK


def cmd_collect(args: argparse.Namespace) -> int:
    s = collect(Path(args.state_dir), client=_client(args), bump_max_tokens=args.bump_max_tokens,
                rates=load_rates(args.rates))
    _emit(args, s, format_summary(s))
    return EXIT_OK


def cmd_cancel(args: argparse.Namespace) -> int:
    batch = _client(args).cancel_batch(_require_batch(Path(args.state_dir))["batch_id"])
    _emit(args, batch, batch_line(batch) + "\nRows already running finish; collect gets the finished ones.")
    return EXIT_OK


def cmd_cleanup(args: argparse.Namespace) -> int:
    deleted = cleanup(Path(args.state_dir), client=_client(args), force=args.force)
    _emit(args, {"deleted": deleted}, f"Deleted {len(deleted)} file(s) from Reka: {', '.join(deleted) or '-'}")
    return EXIT_OK


def cmd_list(args: argparse.Namespace) -> int:
    client = _client(args)
    if args.files:
        files = list(client.iter_files(purpose=None, max_items=args.limit))
        text = "\n".join(f"{f['id']}  {f.get('purpose', '?'):12} {f.get('bytes', 0):>12,}  {f.get('filename', '')}"
                         for f in files) or "No files."
        _emit(args, files, text)
    else:
        data = client.list_batches(limit=min(args.limit, 100)).get("data") or []
        _emit(args, data, "\n".join(batch_line(b) for b in data) or "No batches.")
    return EXIT_OK


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="reka_batch.py", description=__doc__.split("\n\n")[0])
    p.add_argument("--version", action="version", version=__version__)
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name: str, fn: Callable[[argparse.Namespace], int], help_: str, *, state: bool = False,
            file: bool = False, api: bool = False) -> argparse.ArgumentParser:
        sp = sub.add_parser(name, help=help_, description=help_)
        sp.set_defaults(fn=fn)
        sp.add_argument("--json", action="store_true", help="machine-readable output")
        if file:
            sp.add_argument("file", help="request file (JSONL)")
        if state:
            sp.add_argument("--state-dir", required=True, help="run folder holding state.json and results")
        if api:
            sp.add_argument("--base-url", help=argparse.SUPPRESS)
        return sp

    sp = add("make", cmd_make, "build a request file from a CSV/JSONL of items and a {{field}} prompt template")
    sp.add_argument("--items", required=True)
    sp.add_argument("--prompt", required=True, help="user prompt template file with {{field}} placeholders")
    sp.add_argument("--system", help="shared system prompt file (identical in every row, so it can be cached)")
    sp.add_argument("--model", required=True, help=f"batch model: {', '.join(sorted(LIVE_RATES))}")
    sp.add_argument("--id-field", help="item field to use as custom_id (default: row number)")
    sp.add_argument("--max-tokens", type=int)
    sp.add_argument("--reasoning", choices=["none", "minimal", "low", "medium", "high"],
                    help='sets reasoning_effort ("none" for short labels)')
    sp.add_argument("--json-mode", action="store_true", help='response_format {"type": "json_object"}')
    sp.add_argument("--temperature", type=float)
    sp.add_argument("--allow-unknown-model", action="store_true")
    sp.add_argument("--out", required=True)

    sp = add("validate", cmd_validate, "check a request file against the Batch API limits", file=True)
    sp.add_argument("--allow-unknown-model", action="store_true")

    sp = add("estimate", cmd_estimate, "rough cost: live vs batch, with and without cache hits", file=True)
    sp.add_argument("--avg-output", type=float, help="typical output tokens per row")
    sp.add_argument("--chars-per-token", type=float, default=DEFAULT_CHARS_PER_TOKEN)
    sp.add_argument("--rates", help="JSON price table overriding the built-in one")

    sp = add("submit", cmd_submit, "validate, upload and create the batch (safe to rerun)", file=True, state=True,
             api=True)
    sp.add_argument("--metadata", action="append", help="key=value, up to 16")
    sp.add_argument("--wait-queue", action="store_true", help="if the queue is full, wait and retry")
    sp.add_argument("--reupload", action="store_true", help="upload again after an uncertain upload")
    sp.add_argument("--allow-unknown-model", action="store_true")

    sp = add("status", cmd_status, "show a batch's status", api=True)
    g = sp.add_mutually_exclusive_group(required=True)
    g.add_argument("--state-dir")
    g.add_argument("--batch-id")

    sp = add("wait", cmd_wait, "poll until the batch finishes, then optionally run a notify command", state=True,
             api=True)
    sp.add_argument("--interval", type=float, default=60.0, help="seconds between checks (default 60)")
    sp.add_argument("--max-wait-hours", type=float, default=25.0)
    sp.add_argument("--notify-cmd", help="shell command run when done; gets RB_BATCH_ID, RB_STATUS, RB_TOTAL, "
                                         "RB_COMPLETED, RB_FAILED, RB_STATE_DIR (never the API key)")

    sp = add("collect", cmd_collect, "download results and write results.jsonl, retry.jsonl, summary.json",
             state=True, api=True)
    sp.add_argument("--bump-max-tokens", type=float, help="multiply max_tokens for empty_content rows in retry.jsonl")
    sp.add_argument("--rates", help="JSON price table overriding the built-in one")

    add("cancel", cmd_cancel, "cancel a running batch (finished rows are kept)", state=True, api=True)

    sp = add("cleanup", cmd_cleanup, "delete this run's files from Reka after collecting", state=True, api=True)
    sp.add_argument("--force", action="store_true")

    sp = add("list", cmd_list, "list recent batches (or --files)", api=True)
    sp.add_argument("--files", action="store_true")
    sp.add_argument("--limit", type=int, default=20)
    return p


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        return args.fn(args)
    except ValidationFailed as exc:
        if getattr(args, "json", False):
            print(json.dumps(exc.report, indent=2))
        log(f"error: {exc}")
        return exc.exit_code
    except RekaBatchError as exc:
        log(f"error: {exc}")
        return exc.exit_code
    except KeyboardInterrupt:
        log("interrupted; rerun the same command to resume")
        return 130


if __name__ == "__main__":
    sys.exit(main())
