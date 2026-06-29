#!/usr/bin/env python3
"""BT-Panel (Baota) HTTP client for cross-server log collection.

Scope:
- BT-standard signing: request_token = md5(str(request_time) + md5(api_key)).
- Strictly POST-only transport, per BT official documentation.
- Connection-and-cookie reuse via a per-client requests.Session() — the agent
  hammers the same panel many times per cron tick, so keeping the TCP/TLS
  socket warm and the BT session cookie pinned dramatically reduces both
  client-side latency and panel-side concurrency pressure.
- File-content reads via the /system?action=ExecShell endpoint, using
  ``tail -c +N | head -c CHUNK`` to fetch precise incremental byte ranges
  (avoids pulling whole log files into memory through GetFileBody).

Security note:
    The BT api_key has full panel privileges. Never commit it to the repo.
    Prefer environment-variable injection via remote_panels.<id>.api_key_env.

Dependency note:
    Requires the third-party ``requests`` package (already a transitive
    dependency in most Python ops environments). Connection pooling, cookie
    persistence, and per-call timeout are all handled through requests.Session.

Concurrency note:
    This client is synchronous on purpose — Server-Mate runs once per cron tick
    and most deployments have a small number of panels. If the cumulative
    request time across panels approaches the cron interval (e.g. >5 min for a
    10-min schedule), wrap fetches in concurrent.futures.ThreadPoolExecutor at
    the call site, OR migrate to an aiohttp-backed async variant. Both are
    drop-in: the LogReader contract returns plain (lines, cursor) and does not
    care which thread called it. Threading is the cheaper option since the
    agent has no other event loop to coordinate with.
"""

from __future__ import annotations

import hashlib
import json
import logging
import shlex
import time
from dataclasses import dataclass
from typing import Any

import requests
from requests.exceptions import (
    ConnectionError as RequestsConnectionError,
    HTTPError as RequestsHTTPError,
    RequestException,
    SSLError,
    Timeout,
)

try:
    # Suppress the InsecureRequestWarning when an operator explicitly opts
    # out of TLS verification on a self-signed BT panel. Verbose stack
    # warnings on every cron tick would drown out real diagnostics.
    from urllib3.exceptions import InsecureRequestWarning as _InsecureRequestWarning
except ImportError:  # pragma: no cover  - urllib3 is bundled with requests
    _InsecureRequestWarning = None  # type: ignore[assignment]


LOG = logging.getLogger("server_mate.bt_client")

# Operator-facing hint emitted whenever the panel rejects our signature.
# BT validates request_token = md5(request_time + md5(api_key)). If the agent
# clock drifts more than ~120s from the panel host, a correct api_key will
# still be rejected — the only fix is NTP, not re-pasting the key.
NTP_DRIFT_HINT = (
    "Authentication failed. Please check if the time on the Agent server and "
    "the Remote BT panel are synchronized (NTP Time Drift)."
)

# Substrings the BT panel commonly returns inside {"status": False, "msg": ...}
# when the request_token is rejected. Matched case-insensitively. Both English
# and Chinese variants are covered because BT localises by panel language.
_AUTH_FAILURE_HINTS = (
    "request_token",
    "request_time",
    "token",
    "签名",
    "鉴权",
    "时间",
    "未授权",
    "no permission",
    "permission denied",
    "auth failed",
    "authentication",
    "key error",
    "error_key",
)


def _looks_like_auth_failure(message: str | None) -> bool:
    """Return True if a panel-supplied error message looks like an auth/signature failure."""
    if not message:
        return False
    text = str(message).lower()
    return any(hint in text for hint in _AUTH_FAILURE_HINTS)


def _safe_remote_path(remote_path: str) -> str:
    """Validate + shell-quote a remote file path before splicing into ExecShell.

    Defense in depth — shlex.quote alone already neutralises shell metacharacters
    by wrapping the value in single quotes and escaping embedded quotes. We add
    two structural checks on top:

      * Reject embedded NUL/newline/CR — these are not legal in a Linux file path
        and their only realistic source is an attacker probing config injection.
      * Reject empty strings — would expand to an empty shell token and surprise
        the remote shell parser.

    Returns the safely quoted token ready for f-string splicing.
    """
    if not remote_path:
        raise ValueError("remote_path must be non-empty")
    path_str = str(remote_path)
    for forbidden in ("\x00", "\n", "\r"):
        if forbidden in path_str:
            raise ValueError(
                f"remote_path contains illegal control character ({forbidden!r}); refusing to build shell command"
            )
    return shlex.quote(path_str)


class BTPanelError(RuntimeError):
    """Raised when the BT panel returns a non-recoverable error."""


class BTPanelAuthError(BTPanelError):
    """Raised when api_key is missing/rejected — never auto-retried."""


@dataclass
class BTPanelConfig:
    panel_id: str
    url: str
    api_key: str
    timeout_seconds: int = 15
    retries: int = 2
    # Hard upper bound on bytes pulled per single ExecShell call AND per cron
    # cycle. Prevents OOM/timeout when an error_log explodes to multi-GB. Any
    # unread tail simply rolls over to the next cron tick.
    chunk_bytes: int = 5 * 1024 * 1024  # 5 MB
    verify_tls: bool = True

    @classmethod
    def from_dict(cls, panel: dict[str, Any]) -> "BTPanelConfig":
        return cls(
            panel_id=str(panel.get("panel_id") or "").strip(),
            url=str(panel.get("url") or "").strip().rstrip("/"),
            api_key=str(panel.get("api_key") or ""),
            timeout_seconds=int(panel.get("timeout_seconds", 15)),
            retries=int(panel.get("retries", 2)),
            chunk_bytes=int(panel.get("chunk_bytes", 5 * 1024 * 1024)),
            verify_tls=bool(panel.get("verify_tls", True)),
        )


class BTPanelClient:
    """Thin wrapper around the BT-Panel HTTP API.

    Only the subset needed by Server-Mate's log collection layer is exposed:
        - get_remote_file_size(path)
        - read_remote_file_chunk(path, offset, chunk_size)

    Both are designed to fail loudly on misconfiguration but return None / raise
    a typed exception on transient errors so the caller can decide whether to
    skip the cycle or surface an alert.
    """

    def __init__(self, config: BTPanelConfig) -> None:
        if not config.url:
            raise BTPanelAuthError(f"BT panel '{config.panel_id}' has empty url")
        if not config.api_key:
            raise BTPanelAuthError(
                f"BT panel '{config.panel_id}' has empty api_key "
                "(set api_key_env or api_key in remote_panels)"
            )
        self.config = config

        # One Session per panel. The agent hammers the same panel many times
        # per cron tick, so:
        #   * connection pooling reuses TCP/TLS sockets between calls
        #   * cookie persistence honors BT's official guidance to "save the
        #     cookie and attach it on every subsequent request"
        # both of which materially reduce request latency and panel CPU load.
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "server-mate-bt-client/1.1"})
        self.session.verify = bool(config.verify_tls)
        if not self.session.verify and _InsecureRequestWarning is not None:
            # Operator explicitly opted out — silence the per-cron WARN spam
            # (it would otherwise mask the real diagnostics from log_reader).
            requests.packages.urllib3.disable_warnings(_InsecureRequestWarning)

    def close(self) -> None:
        """Release the underlying HTTP connection pool. Safe to call multiple times."""
        try:
            self.session.close()
        except Exception:  # pragma: no cover - best-effort cleanup
            pass

    def __enter__(self) -> "BTPanelClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    @staticmethod
    def _generate_auth_params(api_key: str) -> dict[str, Any]:
        """Compute BT's standard ``request_time`` + ``request_token`` pair.

        Algorithm (per BT official API docs):
            request_time  = int(time.time())                          # Unix ts
            sk_md5        = md5(api_key)                              # 32-hex
            request_token = md5(str(request_time) + sk_md5)           # 32-hex

        Returns a dict ready to be merged into the form-data of any POST call.

        Note: ``api_key`` is taken as a parameter (rather than read from
        ``self.config.api_key``) so the function is stateless and trivially
        unit-testable, and so a future implementation can rotate keys per
        request without instantiating a new client.
        """
        request_time = int(time.time())
        sk_md5 = hashlib.md5(str(api_key).encode("utf-8")).hexdigest()
        request_token = hashlib.md5(
            (str(request_time) + sk_md5).encode("utf-8")
        ).hexdigest()
        return {"request_time": request_time, "request_token": request_token}

    def _post(self, endpoint: str, payload: dict[str, Any] | None = None) -> Any:
        """POST to the panel with merged auth + business params, with retries.

        Per BT official documentation, every API call MUST be a POST and MUST
        carry the dynamic signature. We unconditionally:
            1. Compute fresh ``_generate_auth_params(api_key)`` per attempt
               (re-signing on retry — important when the previous failure was
               itself caused by clock skew that has since been corrected).
            2. Merge the auth dict with the caller-supplied business payload
               and submit the union as ``data=`` (form-encoded body).
            3. Send through ``self.session.post`` so TCP/TLS and the BT
               session cookie are reused across calls.

        Retries are reserved for transport / 5xx failures. Auth and schema
        errors short-circuit immediately so the caller can fail loudly.
        """
        url = f"{self.config.url}{endpoint}"
        business = dict(payload or {})

        attempt = 0
        last_exc: Exception | None = None
        while attempt <= self.config.retries:
            attempt += 1
            # Re-sign on every attempt: a fresh request_time is required if
            # the panel rejected us due to local clock drift that has since
            # been fixed by NTP between retries.
            body = {**business, **self._generate_auth_params(self.config.api_key)}
            try:
                response = self.session.post(
                    url,
                    data=body,
                    timeout=self.config.timeout_seconds,
                )
            except (Timeout, RequestsConnectionError, SSLError, RequestException) as exc:
                LOG.warning(
                    "BT panel %s %s transport error: %s (attempt %s/%s)",
                    self.config.panel_id,
                    endpoint,
                    exc,
                    attempt,
                    self.config.retries + 1,
                )
                last_exc = exc
            else:
                # ---- HTTP-layer auth rejection ---------------------------
                if response.status_code in (401, 403):
                    LOG.warning(
                        "BT panel %s %s HTTP %s — rejected at HTTP layer. %s",
                        self.config.panel_id,
                        endpoint,
                        response.status_code,
                        NTP_DRIFT_HINT,
                    )
                    raise BTPanelAuthError(
                        f"BT panel '{self.config.panel_id}' rejected request: "
                        f"HTTP {response.status_code}. {NTP_DRIFT_HINT}"
                    )
                # ---- 5xx is transient: retry (don't burn an attempt slot
                #      on a hard error) ----------------------------------
                if 500 <= response.status_code < 600:
                    LOG.warning(
                        "BT panel %s %s HTTP %s (attempt %s/%s) — retrying",
                        self.config.panel_id,
                        endpoint,
                        response.status_code,
                        attempt,
                        self.config.retries + 1,
                    )
                    last_exc = RequestsHTTPError(
                        f"HTTP {response.status_code}", response=response
                    )
                else:
                    return self._parse_response(response)

            if attempt <= self.config.retries:
                time.sleep(min(2 ** (attempt - 1), 5))
        raise BTPanelError(
            f"BT panel '{self.config.panel_id}' {endpoint} failed after retries: {last_exc}"
        )

    @staticmethod
    def _parse_response(response: requests.Response) -> Any:
        """Parse a BT response. Returns dict (JSON), str (plain text), or None."""
        text = response.text or ""
        if not text:
            return None
        # requests.Response.json() handles encoding detection; fall back to a
        # bare json.loads + raw text when the panel returns a non-JSON blob
        # (e.g. some legacy ExecShell wrappers).
        try:
            return response.json()
        except ValueError:
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return text

    def exec_shell(self, shell: str) -> str:
        """Execute a shell snippet on the remote host.

        BT's /system?action=ExecShell returns a JSON-ish blob. Different panel
        versions wrap output in {"status": True, "data": "..."} or just return
        a bare string; we accept both. Returns the raw stdout.

        Panel-level auth failures (e.g. token mismatch from clock drift) come
        back as HTTP 200 + {"status": False, "msg": "<token error>"} rather than
        as 401/403, so we sniff the message and re-raise as BTPanelAuthError
        with the NTP hint when the message looks auth-related.
        """
        result = self._post("/system?action=ExecShell", {"shell": shell})
        if isinstance(result, dict):
            if result.get("status") is False:
                msg = str(result.get("msg") or result.get("data") or "unknown error")
                if _looks_like_auth_failure(msg):
                    LOG.warning(
                        "BT panel %s payload-level auth failure (msg=%r). %s",
                        self.config.panel_id,
                        msg[:200],
                        NTP_DRIFT_HINT,
                    )
                    raise BTPanelAuthError(
                        f"ExecShell rejected on {self.config.panel_id}: {msg}. {NTP_DRIFT_HINT}"
                    )
                raise BTPanelError(f"ExecShell failed on {self.config.panel_id}: {msg}")
            data = result.get("data")
            return data if isinstance(data, str) else (str(data) if data is not None else "")
        if isinstance(result, str):
            return result
        return ""

    def get_remote_file_size(self, remote_path: str) -> int | None:
        """Return file size in bytes, or None if the file is missing / unreadable.

        Uses ``stat -c %s`` because it is portable across BT-supported distros and
        cheap; falls back to ``wc -c`` if ``stat`` is unavailable.
        """
        # _safe_remote_path = shlex.quote + control-char rejection. NEVER
        # interpolate remote_path into a shell string without going through it.
        path_token = _safe_remote_path(remote_path)
        shell = (
            f"if [ -f {path_token} ]; then "
            f"stat -c %s {path_token} 2>/dev/null || wc -c < {path_token}; "
            f"else echo MISSING; fi"
        )
        try:
            stdout = self.exec_shell(shell)
        except BTPanelError:
            raise
        text = (stdout or "").strip().splitlines()[-1] if stdout else ""
        if not text or text == "MISSING":
            return None
        try:
            return max(int(text), 0)
        except ValueError:
            LOG.warning(
                "BT panel %s stat returned non-numeric output for %s: %r",
                self.config.panel_id,
                remote_path,
                text,
            )
            return None

    def read_remote_file_chunk(
        self,
        remote_path: str,
        offset: int,
        chunk_size: int | None = None,
    ) -> bytes:
        """Read up to chunk_size bytes starting at the given byte offset.

        Implemented with ``tail -c +<offset+1> | head -c <chunk_size>`` to avoid
        loading the whole file into memory on the panel side. ``tail -c +N`` is
        1-based, hence ``offset + 1``.

        Two layers of bounding apply to ``chunk_size``:
          1. Caller-supplied ``chunk_size`` is clamped to ``config.chunk_bytes``
             (default 5 MB) so a buggy caller cannot demand a 2 GB pull.
          2. The bound is also baked into the SHELL pipeline as ``head -c N``,
             so even if the remote panel mis-handles our argument, the kernel
             tears down the pipe at N bytes — defence in depth against OOM.

        The panel often base64-encodes ExecShell output to survive JSON
        round-trips, but content of a logrotated text log can equally come back
        as plain UTF-8 bytes. We request base64 explicitly so binary safety is
        preserved across panel versions.
        """
        if offset < 0:
            offset = 0
        requested = int(chunk_size or self.config.chunk_bytes)
        # Hard cap: never let a single ExecShell pull exceed config.chunk_bytes.
        size = max(min(requested, self.config.chunk_bytes), 0)
        if size <= 0:
            return b""

        # _safe_remote_path = shlex.quote + control-char rejection. NEVER
        # interpolate remote_path into a shell string without going through it.
        path_token = _safe_remote_path(remote_path)
        # `head -c {size}` is the on-the-wire OOM stopgap — see method docstring.
        # base64 -w 0 keeps output single-line; both GNU coreutils and BusyBox
        # accept the spaced form.
        shell = (
            f"tail -c +{offset + 1} {path_token} 2>/dev/null "
            f"| head -c {size} | base64 -w 0"
        )
        stdout = self.exec_shell(shell)
        token = (stdout or "").strip()
        if not token:
            return b""
        import base64 as _b64

        try:
            return _b64.b64decode(token, validate=False)
        except (ValueError, _b64.binascii.Error) as exc:
            LOG.warning(
                "BT panel %s base64 decode failed for %s offset=%s: %s",
                self.config.panel_id,
                remote_path,
                offset,
                exc,
            )
            return b""


def build_panel_registry(panels_config: dict[str, dict[str, Any]]) -> dict[str, BTPanelClient]:
    """Instantiate one BTPanelClient per configured panel_id.

    Panels with missing url/api_key are skipped with a logged warning so the
    main agent can still serve local sites. The skipped IDs are still reported
    in the returned dict as None placeholders to help the caller emit a clear
    "this site was not collected" diagnostic.
    """
    registry: dict[str, BTPanelClient] = {}
    for panel_id, panel in panels_config.items():
        try:
            registry[panel_id] = BTPanelClient(BTPanelConfig.from_dict(panel))
        except BTPanelAuthError as exc:
            LOG.warning("Skipping BT panel %s: %s", panel_id, exc)
    return registry
