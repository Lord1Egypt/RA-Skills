"""PIN-based authentication for YouOS web UI."""

from __future__ import annotations

import hashlib
import json
import secrets
import time
from pathlib import Path
from typing import Any

# Methods that mutate server state — these are the CSRF-relevant ones.
STATE_CHANGING_METHODS = frozenset({"POST", "PUT", "DELETE", "PATCH"})


def _get_sessions_path() -> Path:
    from app.core.settings import get_var_dir

    return get_var_dir() / "sessions.json"


SESSIONS_PATH = _get_sessions_path()
SESSION_MAX_AGE = 86400  # 24 hours


PBKDF2_ITERATIONS = 260000


def get_pin_hash(pin: str) -> str:
    """Hash a PIN using PBKDF2-HMAC-SHA256."""
    salt = secrets.token_hex(16)
    dk = hashlib.pbkdf2_hmac("sha256", pin.encode("utf-8"), bytes.fromhex(salt), PBKDF2_ITERATIONS)
    return f"pbkdf2:sha256:{PBKDF2_ITERATIONS}:{salt}:{dk.hex()}"


def verify_pin(pin: str, stored_hash: str) -> bool:
    """Verify a PIN against a stored hash.

    Supports both new PBKDF2 format and legacy SHA-256 (no ':' separator).
    """
    if ":" not in stored_hash:
        # Legacy SHA-256 format
        import warnings

        warnings.warn(
            "PIN stored in legacy SHA-256 format. Re-set your PIN to upgrade to PBKDF2.",
            DeprecationWarning,
            stacklevel=2,
        )
        legacy_hash = hashlib.sha256(pin.encode("utf-8")).hexdigest()
        return secrets.compare_digest(legacy_hash, stored_hash)

    # PBKDF2 format: pbkdf2:sha256:<iterations>:<salt_hex>:<hash_hex>
    parts = stored_hash.split(":")
    if len(parts) != 5 or parts[0] != "pbkdf2":
        return False
    _, algo, iterations_str, salt_hex, hash_hex = parts
    dk = hashlib.pbkdf2_hmac(algo, pin.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations_str))
    return secrets.compare_digest(dk.hex(), hash_hex)


def is_auth_enabled(config: dict[str, Any]) -> bool:
    """Check if PIN auth is enabled (non-empty pin hash in config)."""
    pin_value = config.get("server", {}).get("pin", "")
    return bool(pin_value)


def create_session_token() -> str:
    """Create a cryptographically secure session token."""
    return secrets.token_urlsafe(32)


def load_sessions(path: Path | None = None) -> dict[str, float]:
    """Load sessions from JSON file, prune expired tokens.

    Returns dict of {token: created_at_unix}.
    """
    if path is None:
        path = SESSIONS_PATH
    now = time.time()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {}
        # Prune expired
        return {tok: ts for tok, ts in data.items() if now - ts < SESSION_MAX_AGE}
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def save_sessions(sessions: dict[str, float], path: Path | None = None) -> None:
    """Write sessions dict to JSON file."""
    if path is None:
        path = SESSIONS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sessions), encoding="utf-8")


def persist_new_session(token: str, path: Path | None = None) -> None:
    """Add a new session token and persist to disk."""
    sessions = load_sessions(path)
    sessions[token] = time.time()
    save_sessions(sessions, path)


# ── API tokens (for the browser extension / non-cookie clients) ──────────
# The browser extension can't ride the SameSite=Lax session cookie cross-origin,
# so PIN-protected instances accept a long-lived API token via the
# `X-YouOS-Token` header instead. Tokens are stored hashed (same PBKDF2 as PINs)
# and compared in constant time.


def _get_api_tokens_path() -> Path:
    from app.core.settings import get_var_dir

    return get_var_dir() / "api_tokens.json"


def load_api_token_hashes(path: Path | None = None) -> list[str]:
    """Return stored API-token hashes; [] if none or the file is unreadable."""
    if path is None:
        path = _get_api_tokens_path()
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []
    if isinstance(data, list):
        return [str(h) for h in data]
    if isinstance(data, dict):
        return [str(h) for h in data.get("tokens", [])]
    return []


def add_api_token(path: Path | None = None) -> str:
    """Generate a new API token, persist its hash, and return the plaintext once."""
    if path is None:
        path = _get_api_tokens_path()
    token = secrets.token_urlsafe(32)
    hashes = load_api_token_hashes(path)
    hashes.append(get_pin_hash(token))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(hashes), encoding="utf-8")
    return token


def revoke_api_tokens(path: Path | None = None) -> int:
    """Delete all stored API tokens. Returns how many were removed."""
    if path is None:
        path = _get_api_tokens_path()
    count = len(load_api_token_hashes(path))
    if path.exists():
        path.write_text(json.dumps([]), encoding="utf-8")
    return count


def verify_api_token(token: str, path: Path | None = None) -> bool:
    """True if `token` matches any stored API-token hash."""
    if not token:
        return False
    return any(verify_pin(token, h) for h in load_api_token_hashes(path))


def _normalize_origin(origin: str) -> str:
    return origin.strip().rstrip("/")


def compute_allowed_origins(config: dict[str, Any]) -> set[str]:
    """Origins permitted for cookie-authenticated state-changing requests.

    The session cookie is the CSRF-prone credential — a malicious page can
    cause the browser to attach it to a cross-origin POST. We pin requests to
    the server's own origin(s):

    - ``http://127.0.0.1:<port>`` / ``http://localhost:<port>`` (the local web UI)
    - ``http://<configured_host>:<port>`` when ``server.host`` is non-loopback
      (e.g. LAN deployments)
    - ``https://<tailscale_hostname>.ts.net`` and ``http://...`` (Tailscale)
    - any literal origins under ``server.allowed_origins`` (escape hatch for
      reverse proxies, alternate-port test setups, etc.)

    API-token requests bypass this entirely — they're not CSRF-prone.
    """
    server_cfg = config.get("server", {}) if isinstance(config, dict) else {}
    port = int(server_cfg.get("port", 8901))
    host = server_cfg.get("host", "127.0.0.1") or "127.0.0.1"

    origins: set[str] = {
        f"http://127.0.0.1:{port}",
        f"http://localhost:{port}",
    }
    if host not in {"127.0.0.1", "localhost", "::1", "0.0.0.0", ""}:
        origins.add(f"http://{host}:{port}")

    tailscale = config.get("tailscale", {}) if isinstance(config, dict) else {}
    ts_host = (tailscale.get("hostname") or "").strip()
    if ts_host:
        origins.add(f"https://{ts_host}.ts.net")
        origins.add(f"http://{ts_host}.ts.net")

    extras = server_cfg.get("allowed_origins") or []
    if isinstance(extras, list):
        for entry in extras:
            if isinstance(entry, str) and entry.strip():
                origins.add(_normalize_origin(entry))

    return origins


def compute_token_allowed_origins(config: dict[str, Any]) -> set[str] | None:
    """Origins permitted for *token*-authenticated state-changing requests.

    Distinct from ``compute_allowed_origins`` (which guards the cookie auth
    path against CSRF). Token auth isn't CSRF-prone — the attacker would
    need to know the token to make the browser send it — but a compromised
    page that exfiltrated the token could otherwise reuse it from any
    origin. This narrows that surface: if the user configures
    ``server.token_allowed_origins``, token-authed state-changers must
    additionally carry an Origin in the set.

    Returns ``None`` when the allowlist is **not configured**, signalling
    "no extra check; preserve the historical token-authenticates-anywhere
    behaviour". Returning an empty set would mean "configured to allow no
    origins, block everything" which is almost certainly a foot-gun, so
    blank lists are also treated as not-configured.

    Browser extensions don't have a stable cross-install identifier (Chrome
    unpacked-ID depends on the dev directory; Firefox uses a per-install
    UUID, not the manifest's ``browser_specific_settings.gecko.id``), so
    we can't ship a default that "just works". The user reads their own
    extension's Origin out of the browser's network tab and adds it here.
    """
    server_cfg = config.get("server", {}) if isinstance(config, dict) else {}
    raw = server_cfg.get("token_allowed_origins")
    if not isinstance(raw, list):
        return None
    origins: set[str] = set()
    for entry in raw:
        if isinstance(entry, str) and entry.strip():
            origins.add(_normalize_origin(entry))
    if not origins:
        return None
    return origins


def token_request_origin_allowed(
    *,
    method: str,
    origin: str | None,
    allowed_origins: set[str] | None,
) -> bool:
    """Per-request decision for token-authenticated callers.

    Mirrors ``request_origin_allowed`` for the cookie path but with three
    differences:

    1. ``allowed_origins=None`` (allowlist not configured) → always allowed,
       preserving the historical token-authenticates-anywhere behaviour.
       Migrating instances aren't broken by deploying this code.
    2. No Referer fallback. Token clients (browser extensions, CLIs) are
       expected to always send Origin when state-changing; a missing Origin
       on a token POST against an allowlisted instance is treated as
       suspect, not silently allowed.
    3. ``Origin: null`` still rejected — same reasoning as the cookie path.
    """
    if method.upper() not in STATE_CHANGING_METHODS:
        return True
    if allowed_origins is None:
        return True
    if origin is None:
        return False
    normalized = _normalize_origin(origin)
    if normalized == "null" or not normalized:
        return False
    return normalized in allowed_origins


def request_origin_allowed(
    *,
    method: str,
    origin: str | None,
    referer: str | None,
    allowed_origins: set[str],
) -> bool:
    """True if the request may proceed under cookie auth.

    Only the state-changing methods are checked; GET/HEAD/OPTIONS are not
    targets of classic CSRF because the browser-attached session cookie can't
    be combined with a writable response in a meaningful way.

    On a state-changing request the ``Origin`` header is the primary signal;
    when it is absent (some same-origin POSTs from older clients, or
    server-to-server traffic) we fall back to ``Referer`` matching one of the
    allowed origins. ``Origin: null`` (sandboxed/file:// contexts) is treated
    as not-allowed — there is no legitimate same-origin request that needs it.
    """
    if method.upper() not in STATE_CHANGING_METHODS:
        return True

    if origin is not None:
        normalized = _normalize_origin(origin)
        if normalized == "null" or not normalized:
            return False
        return normalized in allowed_origins

    if referer:
        for allowed in allowed_origins:
            if referer == allowed or referer.startswith(allowed + "/"):
                return True

    return False


class LoginRateLimiter:
    """Simple rate limiter: 3 attempts then 60s lockout per IP."""

    def __init__(self, max_attempts: int = 3, lockout_seconds: int = 60):
        self.max_attempts = max_attempts
        self.lockout_seconds = lockout_seconds
        self._attempts: dict[str, list[float]] = {}

    def is_locked(self, client_ip: str) -> bool:
        attempts = self._attempts.get(client_ip, [])
        if len(attempts) < self.max_attempts:
            return False
        last_attempt = attempts[-1]
        return (time.time() - last_attempt) < self.lockout_seconds

    def record_attempt(self, client_ip: str) -> None:
        if client_ip not in self._attempts:
            self._attempts[client_ip] = []
        self._attempts[client_ip].append(time.time())
        # Keep only recent attempts
        cutoff = time.time() - self.lockout_seconds
        self._attempts[client_ip] = [t for t in self._attempts[client_ip] if t > cutoff]
        # Drop other IPs whose attempts have all aged out so the map stays bounded.
        for ip in [ip for ip, ts in self._attempts.items() if not ts or ts[-1] <= cutoff]:
            if ip != client_ip:
                del self._attempts[ip]

    def reset(self, client_ip: str) -> None:
        self._attempts.pop(client_ip, None)
