"""Append-first local storage and bounded, opt-in HTTP with replayable responses."""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import socket
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .records import deduplicate

SECRET_KEYS = {"authorization", "key", "api_key", "apikey", "token", "access_token",
               "bearer_token", "password", "cookie", "secret", "client_secret"}
ALLOWED_HOSTS = {"www.googleapis.com", "youtube.googleapis.com", "api.x.com", "api.apify.com"}


class SourceError(Exception):
    def __init__(self, status, message, http_status=None, *, reason=None, raw=None):
        super().__init__(message)
        self.status, self.http_status, self.reason, self.raw = status, http_status, reason, raw


def require_env(name):
    if not isinstance(name, str) or not re.fullmatch(r"[A-Z][A-Z0-9_]*", name):
        raise SourceError("invalid-input", "Invalid credential variable name")
    value = os.environ.get(name, "").strip()
    if not value:
        raise SourceError("auth-failed", f"Set {name} in your environment before this source runs")
    return value


def now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _bytes(data):
    return json.dumps(data, ensure_ascii=False, sort_keys=True).encode("utf-8")


def _sanitize(value, secrets=()):
    if isinstance(value, dict):
        return {k: ("[REDACTED]" if k.lower() in SECRET_KEYS else _sanitize(v, secrets))
                for k, v in value.items()}
    if isinstance(value, list):
        return [_sanitize(v, secrets) for v in value]
    if isinstance(value, str):
        for secret in secrets:
            if secret:
                value = value.replace(secret, "[REDACTED]")
        return value
    return value


@dataclass
class Response:
    data: object
    raw: dict


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None  # Never forward credentials to a redirect target.


def http_transport(method, url, params, headers, json_body):
    if params:
        url += ("&" if "?" in url else "?") + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, data=_bytes(json_body) if json_body is not None else None,
                                 headers={"Accept": "application/json", "Content-Type": "application/json",
                                          "User-Agent": "Voice2Need/0.1", **(headers or {})}, method=method)
    try:
        response = urllib.request.build_opener(NoRedirect()).open(req, timeout=30)
    except urllib.error.HTTPError as exc:
        response = exc
    with response:
        raw = response.read()
        try:
            data = json.loads(raw)
        except (ValueError, UnicodeDecodeError):
            data = {"non_json_body": raw.decode("utf-8", "replace")}
        return response.code, data, dict(response.headers)


class Session:
    def __init__(self, run_dir, *, live=False, max_requests=100, max_units=None, transport=None):
        self.root = Path(run_dir).resolve()
        self.root.mkdir(parents=True, exist_ok=True)
        self.live, self.transport = live, transport
        if isinstance(max_requests, bool) or not isinstance(max_requests, int) or max_requests < 0:
            raise ValueError("max_requests must be a nonnegative integer")
        if max_units is not None and (isinstance(max_units, bool) or not isinstance(max_units, (int, float))
                                      or not math.isfinite(max_units) or max_units < 0):
            raise ValueError("max_units must be nonnegative")
        self.max_requests, self.max_units = max_requests, max_units
        self._lock = threading.RLock()
        self._request_locks = {}
        self.observation_gaps = []
        self.state = self.load_json("usage.json", {"requests": 0, "units": 0})

    def path(self, relative):
        p = (self.root / relative).resolve()
        if p == self.root or self.root not in p.parents:
            raise ValueError("Output must stay inside the run directory")
        return p

    def load_json(self, relative, default=None):
        p = self.path(relative)
        return json.loads(p.read_text()) if p.exists() else default

    def save_json(self, relative, data):
        if Path(relative).parts[0] in {"raw", "imports"}:
            raise ValueError("Raw files are immutable; use write_raw or import_raw")
        with self._lock:
            p = self.path(relative)
            p.parent.mkdir(parents=True, exist_ok=True)
            tmp = p.with_name(p.name + "." + uuid.uuid4().hex + ".tmp")
            with tmp.open("xb") as out:
                out.write(_bytes(data))
                out.flush()
                os.fsync(out.fileno())
            os.replace(tmp, p)

    def event(self, event):
        with self._lock:
            with self.path("events.jsonl").open("a", encoding="utf-8") as out:
                out.write(json.dumps({"at": now(), **event}, ensure_ascii=False) + "\n")
                out.flush()

    def write_raw(self, data, **metadata):
        payload = _bytes({"observed_at": now(), **metadata, "data": data})
        digest = hashlib.sha256(payload).hexdigest()
        relative = f"raw/{uuid.uuid4().hex}.json"
        p = self.path(relative)
        p.parent.mkdir(exist_ok=True)
        with p.open("xb") as out:
            out.write(payload)
            out.flush()
            os.fsync(out.fileno())
        return {"path": relative, "sha256": digest, "locator": "$.data"}

    def import_raw(self, filename):
        source = Path(filename)
        blob = source.read_bytes()
        digest = hashlib.sha256(blob).hexdigest()
        relative = f"imports/{digest}{source.suffix or '.bin'}"
        p = self.path(relative)
        p.parent.mkdir(exist_ok=True)
        if p.exists():
            if hashlib.sha256(p.read_bytes()).hexdigest() != digest:
                raise ValueError("Existing import hash mismatch")
        else:
            with p.open("xb") as out:
                out.write(blob)
                out.flush()
                os.fsync(out.fileno())
        return {"path": relative, "sha256": digest, "locator": "$"}

    def add_records(self, records):
        # One immutable observation segment per page. A crashed tail is never
        # appended to on resume, so it cannot corrupt later successfully read pages.
        with self._lock:
            p = self.path(f"observations/{time.time_ns():020d}-{uuid.uuid4().hex}.jsonl")
            p.parent.mkdir(exist_ok=True)
            with p.open("x", encoding="utf-8") as out:
                for record in records:
                    out.write(json.dumps(record, ensure_ascii=False) + "\n")
                out.flush()
                os.fsync(out.fileno())

    def records(self):
        records = []
        self.observation_gaps = []
        legacy = self.path("records.jsonl")
        paths = ([legacy] if legacy.exists() else []) + sorted(self.path("observations").glob("*.jsonl"))
        for p in paths:
            lines = p.read_bytes().splitlines()
            for i, line in enumerate(lines):
                if not line.strip():
                    continue
                try:
                    records.append(json.loads(line))
                except (ValueError, UnicodeDecodeError):
                    if i != len(lines) - 1:
                        raise ValueError(f"Invalid observation at {p.name}:{i + 1}")
                    self.observation_gaps.append({"status": "partial", "gap": "truncated-final-record",
                                                  "file": str(p.relative_to(self.root)), "line": i + 1})
        return deduplicate(records)

    def get_checkpoint(self, job_id):
        return self.load_json("checkpoints.json", {}).get(job_id, {})

    def checkpoint(self, job_id, state):
        with self._lock:
            states = self.load_json("checkpoints.json", {})
            states[job_id] = state
            self.save_json("checkpoints.json", states)

    def request(self, method, url, *, params=None, headers=None, json_body=None, units=1, cache=True):
        method = method.upper()
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS or parsed.query or parsed.username:
            raise SourceError("invalid-input", "Use a supported HTTPS API host and params for query values")
        if method not in {"GET", "POST"}:
            raise SourceError("invalid-input", "Unsupported request method")
        if not isinstance(units, (int, float)) or isinstance(units, bool) or not math.isfinite(units) or units < 0:
            raise SourceError("invalid-input", "Request units must be nonnegative")
        secrets = [str(v) for k, v in (params or {}).items() if k.lower() in SECRET_KEYS]
        for k, v in (headers or {}).items():
            if k.lower() in SECRET_KEYS:
                secrets += [str(v), str(v).removeprefix("Bearer ")]
        descriptor = {"method": method, "url": url, "params": _sanitize(params), "body": _sanitize(json_body)}
        fingerprint = hashlib.sha256(_bytes(descriptor)).hexdigest()
        with self._lock:
            lock = self._request_locks.setdefault(fingerprint, threading.RLock())
        with lock:
            cached = self.load_json(f"cache/{fingerprint}.json") if cache else None
            if cached:
                p = self.path(cached["path"])
                if hashlib.sha256(p.read_bytes()).hexdigest() != cached["sha256"]:
                    raise SourceError("provider-failed", "Cached raw response hash mismatch")
                return Response(json.loads(p.read_text())["data"], cached)
            pending_path = f"pending/{fingerprint}.json"
            if method == "POST" and self.load_json(pending_path):
                raise SourceError("provider-failed", "Previous POST outcome is indeterminate; inspect saved run before retrying")
            if not self.live and self.transport is None:
                raise SourceError("invalid-input", "Network is disabled; collection needs --live")
            with self._lock:
                if self.state["requests"] >= self.max_requests or (self.max_units is not None and
                         self.state["units"] + units > self.max_units):
                    raise SourceError("budget-exhausted", "Request/unit limit reached; saved data can be resumed")
                self.state["requests"] += 1
                self.state["units"] += units
                self.save_json("usage.json", self.state)
                if method == "POST":
                    self.save_json(pending_path, {"at": now(), "status": "indeterminate"})
            try:
                status, data, response_headers = (self.transport or http_transport)(method, url, params, headers, json_body)
            except (TimeoutError, socket.timeout, urllib.error.URLError, OSError):
                ref = self.write_raw({"transport_error": "timeout-or-connection-failure"}, request=descriptor)
                raise SourceError("timeout", "Request timed out or connection failed; inspect saved state", raw=ref) from None
            safe_data = _sanitize(data, secrets)
            raw = self.write_raw(safe_data, request=descriptor, http_status=status)
            self.event({"type": "request", "method": method, "host": parsed.hostname,
                        "http_status": status, "raw": raw, "units": units})
            if not 200 <= status < 300:
                reason = None
                if isinstance(safe_data, dict):
                    error = safe_data.get("error", {})
                    if isinstance(error, dict):
                        reason = next((r.get("reason") for r in error.get("errors", []) if isinstance(r, dict)), None)
                label = {401: "auth-failed", 402: "budget-exhausted", 403: "forbidden", 429: "rate-limited",
                         400: "invalid-input", 404: "provider-failed"}.get(status, "provider-failed")
                raise SourceError(label, f"Source returned HTTP {status}", status, reason=reason, raw=raw)
            if isinstance(data, dict) and "non_json_body" in data:
                raise SourceError("schema-drift", "Source returned non-JSON content", raw=raw)
            if cache:
                self.save_json(f"cache/{fingerprint}.json", raw)
            return Response(safe_data, raw)


def verify_raw(root, ref, *, cache=None):
    """Check copied bytes and JSON location, never fetch a URL during analysis."""
    root = Path(root).resolve()
    p = (root / ref["path"]).resolve()
    if root not in p.parents or not p.is_file():
        raise ValueError("Raw file is missing or outside run directory")
    key = (str(p), p.stat().st_mtime_ns, p.stat().st_size)
    saved = cache.get(key) if cache is not None else None
    if saved is None:
        blob = p.read_bytes()
        saved = (hashlib.sha256(blob).hexdigest(), json.loads(blob))
        if cache is not None:
            if len(cache) >= 16:
                cache.pop(next(iter(cache)))
            cache[key] = saved
    if saved[0] != ref["sha256"]:
        raise ValueError("Raw content hash mismatch")
    value = saved[1]
    locator = ref.get("locator", "$")
    if not locator.startswith("$"):
        raise ValueError("Raw locator must start with $")
    remaining = locator[1:]
    while remaining:
        token = re.match(r"^\.([A-Za-z_][A-Za-z0-9_-]*)|^\[(\d+)\]", remaining)
        if not token:
            raise ValueError("Unsupported raw locator")
        value = value[token.group(1)] if token.group(1) is not None else value[int(token.group(2))]
        remaining = remaining[token.end():]
    return value
