"""
auth_middleware.py - Authentication & Authorization Module (V12)

Provides JWT token-based auth and API Key auth for the FastAPI server.

Core components:
  - AuthConfig        → configuration dataclass (jwt_secret, api_keys, expiry)
  - create_jwt_token  → generate signed JWT via HMAC-SHA256 (stdlib only)
  - verify_jwt_token  → verify JWT signature + expiry, return claims or None
  - verify_api_key    → lookup API key in config, return tenant info or None
  - AuthMiddleware    → pure-ASGI middleware, extracts + validates auth headers
  - require_permission→ FastAPI dependency for endpoint-level permission gating
  - get_tenant_context→ FastAPI dependency returning TenantContext from request
  - TenantAuth        → convenience wrapper for token creation

Usage:
  from agent_memory.auth_middleware import AuthConfig, AuthMiddleware, TenantAuth

  config = AuthConfig(
      jwt_secret="my-secret-key",
      api_keys={
          "<YOUR_API_KEY>": {"tenant_id": "tenant-1", "permissions": ["read", "write"]},
      },
  )

  auth = TenantAuth(config)
  token = auth.create_token("tenant-1", "agent-42", ["read", "write"])

  app.add_middleware(AuthMiddleware, config=config)

  @app.get("/protected")
  async def protected_route(ctx=Depends(get_tenant_context)):
      return {"tenant": ctx.tenant_id}
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import os
import secrets
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .tenant import TenantContext

logger = logging.getLogger(__name__)

# ── Constants ────────────────────────────────────────────

_JWT_HEADER = {"alg": "HS256", "typ": "JWT"}
_MAX_TOKEN_LENGTH = 8192
_API_KEY_HEADER = "x-api-key"

# ── Error Helpers ────────────────────────────────────────

_ERROR_AUTH_MISSING = {"error": {"code": "AUTH_MISSING", "message": "需要认证：请提供 Authorization: Bearer <token> 或 X-API-Key 请求头。"}}
_ERROR_AUTH_INVALID = {"error": {"code": "AUTH_INVALID", "message": "认证失败：令牌或 API Key 无效，请检查后重试"}}
_ERROR_TOKEN_EXPIRED = {"error": {"code": "TOKEN_EXPIRED", "message": "登录已过期，请重新获取访问令牌"}}
_ERROR_INSUFFICIENT_PERMISSIONS = {"error": {"code": "INSUFFICIENT_PERMISSIONS", "message": "权限不足：当前账户无法执行此操作，请联系管理员或升级套餐"}}
_ERROR_FORBIDDEN = {"error": {"code": "FORBIDDEN", "message": "访问被拒绝：您没有权限访问此资源"}}
_ERROR_RATE_LIMITED = "认证尝试过于频繁，请 {seconds} 秒后重试"


def _json_bytes(data: dict) -> bytes:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


# ── Brute-force protection ──────────────────────────────

class _AuthRateLimiter:
    """Track failed auth attempts per IP and enforce cooldowns."""

    _MAX_FAILURES = 5
    _WINDOW_SECONDS = 300.0   # 5 minutes
    _COOLDOWN_SECONDS = 30.0  # 30-second cooldown after threshold

    def __init__(self):
        self._failures: Dict[str, List[float]] = {}

    def record_failure(self, ip: str):
        now = time.time()
        attempts = self._failures.get(ip, [])
        attempts = [t for t in attempts if now - t < self._WINDOW_SECONDS]
        attempts.append(now)
        self._failures[ip] = attempts

    def record_success(self, ip: str):
        self._failures.pop(ip, None)

    def is_rate_limited(self, ip: str) -> bool:
        now = time.time()
        attempts = self._failures.get(ip, [])
        attempts = [t for t in attempts if now - t < self._WINDOW_SECONDS]
        self._failures[ip] = attempts
        if len(attempts) >= self._MAX_FAILURES:
            last_failure = attempts[-1]
            if now - last_failure < self._COOLDOWN_SECONDS:
                return True
            # Cooldown expired but still within window — allow retry, clear
            if now - attempts[0] >= self._WINDOW_SECONDS:
                self._failures.pop(ip, None)
        return False

    def get_retry_after(self, ip: str) -> Optional[int]:
        """Return seconds until the rate limit cooldown expires for this IP, or None."""
        now = time.time()
        attempts = self._failures.get(ip, [])
        attempts = [t for t in attempts if now - t < self._WINDOW_SECONDS]
        if len(attempts) >= self._MAX_FAILURES:
            last_failure = attempts[-1]
            remaining = int(self._COOLDOWN_SECONDS - (now - last_failure)) + 1
            if remaining > 0:
                return remaining
        return None


# ── Base64URL helpers ────────────────────────────────────

def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(s: str) -> bytes:
    rem = len(s) % 4
    if rem:
        s += "=" * (4 - rem)
    return base64.urlsafe_b64decode(s)


# ═══════════════════════════════════════════════════════════
# AuthConfig
# ═══════════════════════════════════════════════════════════

_DEFAULT_JWT_SECRET = secrets.token_hex(32)  # Runtime-generated per process; source code contains no actual secret


@dataclass
class AuthConfig:
    _jwt_secret_is_default: bool = field(init=False, repr=False, default=False)

    jwt_secret: str
    api_keys: Dict[str, Dict[str, Any]] = field(default_factory=dict)
    token_expiry_seconds: int = 3600

    def __post_init__(self):
        if self.jwt_secret == _DEFAULT_JWT_SECRET:
            self._jwt_secret_is_default = True
            env = os.environ.get("AGENT_MEMORY_ENV", "production").lower()
            if env in ("production", "prod", "staging"):
                raise ValueError(
                    "JWT secret must be changed from default in production/staging. "
                    "Set AGENT_MEMORY_JWT_SECRET environment variable."
                )
            logger.critical(
                "JWT_SECRET 为空或使用默认值! 这是不安全的! "
                "请设置环境变量 AGENT_MEMORY_JWT_SECRET 为至少32字符的随机字符串。"
            )
            allow_insecure = os.environ.get("AGENT_MEMORY_ALLOW_INSECURE", "").strip() in ("1", "true", "yes")
            is_test = os.environ.get("AGENT_MEMORY_ENV") == "test" or allow_insecure
            has_api_keys = bool(self.api_keys)
            if not is_test and has_api_keys:
                raise ValueError(
                    "FATAL: JWT_SECRET 为空或使用默认值，且已配置 API Keys 认证，拒绝启动! "
                    "请设置环境变量 AGENT_MEMORY_JWT_SECRET 为至少32字符的随机字符串。"
                    "如需在开发环境强制启动，请设置: AGENT_MEMORY_ALLOW_INSECURE=1"
                )
            logger.warning(
                "JWT_SECRET 正使用不安全默认值! "
                "请在启动前设置: export AGENT_MEMORY_JWT_SECRET=<random-64-char-string>"
            )
        else:
            self._jwt_secret_is_default = False
            if not self.jwt_secret:
                logger.critical(
                    "JWT_SECRET 为空! JWT 认证已禁用! "
                    "请设置环境变量 AGENT_MEMORY_JWT_SECRET 为至少32字符的随机字符串。"
                )

    def is_default_secret(self) -> bool:
        return self.jwt_secret == _DEFAULT_JWT_SECRET

    def validate_jwt_secret(self) -> bool:
        return not self._jwt_secret_is_default


# ═══════════════════════════════════════════════════════════
# JWT: create / verify
# ═══════════════════════════════════════════════════════════

def create_jwt_token(
    tenant_id: str,
    agent_id: str,
    permissions: List[str],
    secret: str,
    expiry_seconds: int = 3600,
) -> str:
    now = int(time.time())
    payload = {
        "tenant_id": tenant_id,
        "agent_id": agent_id,
        "permissions": permissions,
        "iat": now,
        "exp": now + expiry_seconds,
    }

    header_b64 = _b64url_encode(_json_bytes(_JWT_HEADER))
    payload_b64 = _b64url_encode(_json_bytes(payload))

    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    signature = hmac.new(
        secret.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()
    sig_b64 = _b64url_encode(signature)

    return f"{header_b64}.{payload_b64}.{sig_b64}"


def verify_jwt_token(token: str, secret: str) -> Optional[dict]:
    """Verify JWT token signature and expiry.

    Returns:
        dict with claims if valid,
        {"_expired": True} if token is expired (signature valid but expired),
        None if token is malformed or signature invalid.
    """
    if not secret:
        logger.warning("JWT verification failed: secret is empty")
        return None

    if not token or len(token) > _MAX_TOKEN_LENGTH:
        logger.warning("JWT verification failed: token missing or exceeds max length")
        return None

    parts = token.split(".")
    if len(parts) != 3:
        logger.warning("JWT verification failed: malformed token (not 3 parts)")
        return None

    header_b64, payload_b64, sig_b64 = parts

    signing_input = f"{header_b64}.{payload_b64}".encode("ascii")
    expected_sig = hmac.new(
        secret.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()

    try:
        provided_sig = _b64url_decode(sig_b64)
    except Exception as e:
        logger.warning("auth_middleware: %s", e)
        return None

    if not hmac.compare_digest(provided_sig, expected_sig):
        logger.warning("JWT verification failed: signature mismatch")
        return None

    try:
        payload_bytes = _b64url_decode(payload_b64)
        payload = json.loads(payload_bytes)
    except Exception as e:
        logger.warning("auth_middleware: %s", e)
        return None

    exp = payload.get("exp", 0)
    if time.time() > exp:
        logger.warning(
            f"JWT verification failed: token expired "
            f"(tenant_id={payload.get('tenant_id', '?')}, agent_id={payload.get('agent_id', '?')})"
        )
        return {"_expired": True}

    tenant_id = payload.get("tenant_id")
    agent_id = payload.get("agent_id")
    permissions = payload.get("permissions", [])

    if not tenant_id or not agent_id:
        logger.warning("JWT verification failed: missing tenant_id or agent_id in payload")
        return None

    if not isinstance(permissions, list):
        permissions = []

    return {
        "tenant_id": tenant_id,
        "agent_id": agent_id,
        "permissions": permissions,
        "iat": payload.get("iat"),
        "exp": exp,
    }


# ═══════════════════════════════════════════════════════════
# API Key verification
# ═══════════════════════════════════════════════════════════

def hash_api_key(api_key: str) -> str:
    """Generate SHA-256 hash of API key for secure storage and comparison.

    Args:
        api_key: The raw API key to hash.

    Returns:
        Hexadecimal string of the SHA-256 hash.
    """
    return hashlib.sha256(api_key.encode()).hexdigest()


def _is_hashed_key(key: str) -> bool:
    """Check if a key appears to be a SHA-256 hash (64 hex characters).

    Args:
        key: The key string to check.

    Returns:
        True if the key looks like a SHA-256 hash, False otherwise.
    """
    return len(key) == 64 and all(c in "0123456789abcdef" for c in key.lower())


def verify_api_key(api_key: str, config: AuthConfig) -> Optional[dict]:
    """Verify API key using time-constant comparison to prevent timing attacks.

    The config.api_keys dictionary should use SHA-256 hashes as keys for secure
    storage. For backward compatibility, plaintext keys are also supported
    (with a warning logged).

    Args:
        api_key: The raw API key provided by the client.
        config: The authentication configuration containing API key mappings.

    Returns:
        Dictionary with tenant_id, agent_id, and permissions if valid, None otherwise.
    """
    if not api_key or not config.api_keys:
        logger.warning("API Key verification failed: key missing or no keys configured")
        return None

    api_key_hash = hash_api_key(api_key)

    for stored_key, key_info in config.api_keys.items():
        if _is_hashed_key(stored_key):
            if hmac.compare_digest(api_key_hash, stored_key):
                tenant_id = key_info.get("tenant_id")
                permissions = key_info.get("permissions", [])

                if not tenant_id:
                    logger.warning("API Key verification failed: key entry missing tenant_id")
                    return None

                if not isinstance(permissions, list):
                    permissions = []

                return {
                    "tenant_id": tenant_id,
                    "agent_id": key_info.get("agent_id", "anonymous"),
                    "permissions": permissions,
                }
        else:
            logger.warning(
                "API Key storage uses plaintext (not hashed). "
                "Consider migrating to SHA-256 hashed keys for better security."
            )
            if hmac.compare_digest(api_key, stored_key):
                tenant_id = key_info.get("tenant_id")
                permissions = key_info.get("permissions", [])

                if not tenant_id:
                    logger.warning("API Key verification failed: key entry missing tenant_id")
                    return None

                if not isinstance(permissions, list):
                    permissions = []

                return {
                    "tenant_id": tenant_id,
                    "agent_id": key_info.get("agent_id", "agent-unknown"),
                    "permissions": permissions,
                }

    logger.warning("API Key verification failed: unknown key")
    return None


# ═══════════════════════════════════════════════════════════
# AuthMiddleware (ASGI-compatible)
# ═══════════════════════════════════════════════════════════

class AuthMiddleware:
    _rate_limiter = _AuthRateLimiter()

    def __init__(self, app, config: AuthConfig, exclude_paths: Optional[List[str]] = None):
        self.app = app
        self.config = config
        self._exclude_paths: frozenset = frozenset(exclude_paths or [])

    def _is_excluded(self, path: str) -> bool:
        for ep in self._exclude_paths:
            if path == ep or path.startswith(ep + "/"):
                return True
        return False

    def _get_client_ip(self, scope) -> str:
        # Check X-Forwarded-For header first (for reverse proxy scenarios)
        for key, val in scope.get("headers", []):
            if key == b"x-forwarded-for":
                forwarded = val.decode("latin-1").split(",")[0].strip()
                if forwarded:
                    return forwarded
        return scope.get("client", ("?", 0))[0]

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "").rstrip("/") or "/"

        if self._is_excluded(path):
            await self.app(scope, receive, send)
            return

        client_ip = self._get_client_ip(scope)

        # Brute-force rate limit check
        if self._rate_limiter.is_rate_limited(client_ip):
            retry_after = self._rate_limiter.get_retry_after(client_ip) or int(self._rate_limiter._COOLDOWN_SECONDS)
            error_body = {"error": {"code": "RATE_LIMITED", "message": _ERROR_RATE_LIMITED.format(seconds=retry_after)}}
            headers = [(b"content-type", b"application/json; charset=utf-8")]
            headers.append((b"retry-after", str(retry_after).encode("ascii")))
            await _send_json_with_headers(send, 429, error_body, headers)
            logger.warning("Auth rate-limited: ip=%s path=%s retry_after=%s", client_ip, path, retry_after)
            return

        request = _ASGIRequest(scope)

        auth_header = request.headers.get("authorization", "")
        api_key_header = request.headers.get(_API_KEY_HEADER, "")

        auth_info: Optional[dict] = None

        if auth_header.lower().startswith("bearer "):
            token = auth_header[7:].strip()
            auth_info = verify_jwt_token(token, self.config.jwt_secret)
            if auth_info is None:
                self._rate_limiter.record_failure(client_ip)
                await _send_json(send, 401, _ERROR_AUTH_INVALID)
                logger.warning(
                    f"Auth failure (JWT): path={path} "
                    f"client={client_ip}"
                )
                return
            if auth_info.get("_expired"):
                self._rate_limiter.record_failure(client_ip)
                await _send_json(send, 401, _ERROR_TOKEN_EXPIRED)
                logger.warning(
                    f"Auth failure (JWT expired): path={path} "
                    f"client={client_ip}"
                )
                return

        elif api_key_header:
            auth_info = verify_api_key(api_key_header, self.config)
            if auth_info is None:
                self._rate_limiter.record_failure(client_ip)
                await _send_json(send, 401, _ERROR_AUTH_INVALID)
                logger.warning(
                    f"Auth failure (API Key): path={path} "
                    f"client={client_ip}"
                )
                return

        else:
            await _send_json(send, 401, _ERROR_AUTH_MISSING)
            logger.warning(
                f"Auth failure (missing): path={path} "
                f"client={client_ip}"
            )
            return

        self._rate_limiter.record_success(client_ip)
        scope["_auth_tenant_id"] = auth_info["tenant_id"]
        scope["_auth_agent_id"] = auth_info["agent_id"]
        scope["_auth_permissions"] = auth_info["permissions"]

        await self.app(scope, receive, send)


class _ASGIRequest:
    __slots__ = ("_headers",)

    def __init__(self, scope):
        raw = scope.get("headers", [])
        self._headers: Dict[str, str] = {}
        for k, v in raw:
            key = k.decode("ascii").lower()
            if key in ("x-api-key", "authorization"):
                self._headers[key] = v.decode("utf-8", errors="replace")
            else:
                self._headers[key] = v.decode("latin-1")

    @property
    def headers(self) -> Dict[str, str]:
        return self._headers


async def _send_json(send, status_code: int, body: dict):
    content = json.dumps(body, ensure_ascii=False).encode("utf-8")
    await send({
        "type": "http.response.start",
        "status": status_code,
        "headers": [
            (b"content-type", b"application/json; charset=utf-8"),
            (b"content-length", str(len(content)).encode("ascii")),
        ],
    })
    await send({
        "type": "http.response.body",
        "body": content,
    })


async def _send_json_with_headers(send, status_code: int, body: dict, extra_headers: list):
    content = json.dumps(body, ensure_ascii=False).encode("utf-8")
    headers = list(extra_headers) + [(b"content-length", str(len(content)).encode("ascii"))]
    await send({
        "type": "http.response.start",
        "status": status_code,
        "headers": headers,
    })
    await send({
        "type": "http.response.body",
        "body": content,
    })


# ═══════════════════════════════════════════════════════════
# FastAPI Dependencies
# ═══════════════════════════════════════════════════════════

class _RequirePermission:
    def __init__(self, permission: str):
        self._permission = permission

    async def __call__(self, request):
        permissions: List[str] = getattr(request.state, "permissions", None)
        if permissions is None:
            permissions = request.scope.get("_auth_permissions", [])

        if self._permission not in permissions:
            logger.warning(
                f"Permission denied: required={self._permission} "
                f"tenant_id={getattr(request.state, 'tenant_id', '?')} "
                f"agent_id={getattr(request.state, 'agent_id', '?')} "
                f"permissions={permissions}"
            )
            from fastapi import HTTPException
            raise HTTPException(
                status_code=403,
                detail=_ERROR_INSUFFICIENT_PERMISSIONS,
            )

        return True


def require_permission(permission: str):
    from fastapi import Depends
    return Depends(_RequirePermission(permission))


class _TenantContextExtractor:
    async def __call__(self, request) -> TenantContext:
        tenant_id: str = getattr(request.state, "tenant_id", None)
        agent_id: str = getattr(request.state, "agent_id", None)
        permissions: List[str] = getattr(request.state, "permissions", None)

        if tenant_id is None:
            tenant_id = request.scope.get("_auth_tenant_id", "unknown")
        if agent_id is None:
            agent_id = request.scope.get("_auth_agent_id", "unknown")
        if permissions is None:
            permissions = request.scope.get("_auth_permissions", [])

        return TenantContext(
            tenant_id=tenant_id,
            agent_id=agent_id,
            permissions=list(permissions),
        )


def get_tenant_context(request=None):
    return _TenantContextExtractor()


# ═══════════════════════════════════════════════════════════
# FastAPI Middleware variant (for use with @app.middleware)
# ═══════════════════════════════════════════════════════════

class FastAPIAuthMiddleware:
    _rate_limiter = _AuthRateLimiter()

    def __init__(self, app, config: AuthConfig, exclude_paths: Optional[List[str]] = None):
        self.app = app
        self.config = config
        self._exclude_paths: frozenset = frozenset(exclude_paths or [])

    def _is_excluded(self, path: str) -> bool:
        for ep in self._exclude_paths:
            if path == ep or path.startswith(ep + "/"):
                return True
        return False

    def _get_client_ip(self, scope) -> str:
        # Check X-Forwarded-For header first (for reverse proxy scenarios)
        for key, val in scope.get("headers", []):
            if key == b"x-forwarded-for":
                forwarded = val.decode("latin-1").split(",")[0].strip()
                if forwarded:
                    return forwarded
        return scope.get("client", ("?", 0))[0]

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        from fastapi import Request
        from fastapi.responses import JSONResponse

        path = scope.get("path", "").rstrip("/") or "/"

        if self._is_excluded(path):
            await self.app(scope, receive, send)
            return

        client_ip = self._get_client_ip(scope)

        # Brute-force rate limit check
        if self._rate_limiter.is_rate_limited(client_ip):
            retry_after = self._rate_limiter.get_retry_after(client_ip) or int(self._rate_limiter._COOLDOWN_SECONDS)
            error_body = {"error": {"code": "RATE_LIMITED", "message": _ERROR_RATE_LIMITED.format(seconds=retry_after)}}
            response = JSONResponse(status_code=429, content=error_body)
            response.headers["Retry-After"] = str(retry_after)
            logger.warning("Auth rate-limited: ip=%s path=%s retry_after=%s", client_ip, path, retry_after)
            await response(scope, receive, send)
            return

        request = Request(scope, receive)

        auth_header = request.headers.get("authorization", "")
        api_key_header = request.headers.get(_API_KEY_HEADER, "")

        auth_info: Optional[dict] = None

        if auth_header.lower().startswith("bearer "):
            token = auth_header[7:].strip()
            auth_info = verify_jwt_token(token, self.config.jwt_secret)
            if auth_info is None:
                self._rate_limiter.record_failure(client_ip)
                response = JSONResponse(status_code=401, content=_ERROR_AUTH_INVALID)
                logger.warning(
                    f"Auth failure (JWT): path={path} "
                    f"client={client_ip}"
                )
                await response(scope, receive, send)
                return
            if auth_info.get("_expired"):
                self._rate_limiter.record_failure(client_ip)
                response = JSONResponse(status_code=401, content=_ERROR_TOKEN_EXPIRED)
                logger.warning(
                    f"Auth failure (JWT expired): path={path} "
                    f"client={client_ip}"
                )
                await response(scope, receive, send)
                return

        elif api_key_header:
            auth_info = verify_api_key(api_key_header, self.config)
            if auth_info is None:
                self._rate_limiter.record_failure(client_ip)
                response = JSONResponse(status_code=401, content=_ERROR_AUTH_INVALID)
                logger.warning(
                    f"Auth failure (API Key): path={path} "
                    f"client={client_ip}"
                )
                await response(scope, receive, send)
                return

        else:
            response = JSONResponse(status_code=401, content=_ERROR_AUTH_MISSING)
            logger.warning(
                f"Auth failure (missing): path={path} "
                f"client={client_ip}"
            )
            await response(scope, receive, send)
            return

        self._rate_limiter.record_success(client_ip)
        scope["_auth_tenant_id"] = auth_info["tenant_id"]
        scope["_auth_agent_id"] = auth_info["agent_id"]
        scope["_auth_permissions"] = auth_info["permissions"]

        request = Request(scope, receive)
        request.state.tenant_id = auth_info["tenant_id"]
        request.state.agent_id = auth_info["agent_id"]
        request.state.permissions = auth_info["permissions"]
        scope["_fastapi_request"] = request

        async def _wrapped_receive():
            return await receive()

        await self.app(scope, _wrapped_receive, send)


# ═══════════════════════════════════════════════════════════
# TenantAuth convenience wrapper
# ═══════════════════════════════════════════════════════════

class TenantAuth:
    def __init__(self, config: AuthConfig):
        self._config = config

    @property
    def config(self) -> AuthConfig:
        return self._config

    def create_token(
        self,
        tenant_id: str,
        agent_id: str,
        permissions: List[str],
        expiry_seconds: Optional[int] = None,
    ) -> str:
        return create_jwt_token(
            tenant_id=tenant_id,
            agent_id=agent_id,
            permissions=permissions,
            secret=self._config.jwt_secret,
            expiry_seconds=expiry_seconds if expiry_seconds is not None else self._config.token_expiry_seconds,
        )

    def verify_token(self, token: str) -> Optional[dict]:
        return verify_jwt_token(token, self._config.jwt_secret)

    def verify_key(self, api_key: str) -> Optional[dict]:
        return verify_api_key(api_key, self._config)
