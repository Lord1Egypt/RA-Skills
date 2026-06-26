import base64
import hashlib
import hmac
import json
import os
import time
from pathlib import Path
from typing import Optional


APPROVAL_SECRET_ENV = "SKILL_FORGE_APPROVAL_SECRET"
DEFAULT_TTL_SECONDS = 30 * 60


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64url_decode(text: str) -> bytes:
    padding = "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text + padding)


def hash_skill_dir(path: Path) -> str:
    path = path.expanduser().resolve()
    if not path.exists():
        return "missing"
    hasher = hashlib.sha256()
    if path.is_file():
        hasher.update(b"file\0")
        hasher.update(path.name.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(path.read_bytes())
        return hasher.hexdigest()
    for entry in sorted(p for p in path.rglob("*") if p.is_file()):
        rel = entry.relative_to(path).as_posix().encode("utf-8")
        hasher.update(rel)
        hasher.update(b"\0")
        hasher.update(entry.read_bytes())
        hasher.update(b"\0")
    return hasher.hexdigest()


def derive_secret(bot_token: Optional[str]) -> bytes:
    explicit = os.getenv(APPROVAL_SECRET_ENV)
    if explicit:
        return hashlib.sha256(explicit.encode("utf-8")).digest()
    if bot_token:
        return hashlib.sha256(("skill-forge-approval:" + bot_token).encode("utf-8")).digest()
    raise RuntimeError(
        f"approval secret unavailable: set {APPROVAL_SECRET_ENV} or provide a bot token"
    )


def issue_token(claims: dict, secret: bytes, ttl_seconds: int = DEFAULT_TTL_SECONDS) -> str:
    payload = dict(claims)
    issued = int(payload.get("issued_at") or time.time())
    payload["issued_at"] = issued
    payload.setdefault("expires_at", issued + ttl_seconds)
    body = _b64url_encode(
        json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    )
    signature = hmac.new(secret, body.encode("ascii"), hashlib.sha256).digest()
    return f"{body}.{_b64url_encode(signature)}"


def verify_token(token: str, secret: bytes, expected: dict, now: Optional[int] = None) -> tuple:
    if not token or "." not in token:
        return False, "malformed-token", {}
    body, signature = token.rsplit(".", 1)
    try:
        provided_sig = _b64url_decode(signature)
    except Exception:
        return False, "malformed-signature", {}
    expected_sig = hmac.new(secret, body.encode("ascii"), hashlib.sha256).digest()
    if not hmac.compare_digest(expected_sig, provided_sig):
        return False, "bad-signature", {}
    try:
        claims = json.loads(_b64url_decode(body).decode("utf-8"))
    except Exception:
        return False, "malformed-claims", {}
    current = now if now is not None else int(time.time())
    if int(claims.get("expires_at", 0)) < current:
        return False, "expired", claims
    for key, value in expected.items():
        if claims.get(key) != value:
            return False, f"claim-mismatch:{key}", claims
    return True, "ok", claims
