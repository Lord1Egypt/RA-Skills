"""SnapPwd zero-knowledge text-secret adapter."""

from __future__ import annotations

import base64
import re
from urllib.parse import urlsplit, urlunsplit

from secret_drop.errors import SecretDropError
from secret_drop.net import request_json

_BASE58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
_BASE58_MAP = {char: index for index, char in enumerate(_BASE58)}
_ID_RE = re.compile(r"^sp-[A-Za-z0-9_-]{4,256}$")


def matches(url: str) -> bool:
    parts = urlsplit(url)
    host = (parts.hostname or "").lower()
    return host == "snappwd.io" or host.endswith(".snappwd.io")


def _base58_decode(value: str) -> bytes:
    """Match the SnapPwd CLI decoder, including its leading-zero handling."""
    if not value:
        raise SecretDropError("SnapPwd URL has an invalid encryption key.")
    digits = [0]
    for char in value:
        mapped = _BASE58_MAP.get(char)
        if mapped is None:
            raise SecretDropError("SnapPwd URL has an invalid encryption key.")
        carry = mapped
        for index, digit in enumerate(digits):
            carry += digit * 58
            digits[index] = carry & 0xFF
            carry >>= 8
        while carry:
            digits.append(carry & 0xFF)
            carry >>= 8
    leading_ones = len(value) - len(value.lstrip("1"))
    decoded = bytearray(leading_ones + len(digits))
    for index, digit in enumerate(reversed(digits)):
        decoded[leading_ones + index] = digit
    return bytes(decoded)


def _decrypt(ciphertext_b64: str, key_text: str) -> str:
    try:
        from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    except ImportError as exc:
        raise SecretDropError(
            "SnapPwd support needs the 'cryptography' Python package. Install requirements.txt."
        ) from exc
    key = _base58_decode(key_text)
    if len(key) not in (16, 32):
        raise SecretDropError("SnapPwd encryption key has an unsupported length.")
    try:
        encrypted = base64.b64decode(ciphertext_b64, validate=True)
    except Exception as exc:
        raise SecretDropError("SnapPwd returned malformed ciphertext.") from exc
    if len(encrypted) < 12 + 16:
        raise SecretDropError("SnapPwd returned truncated ciphertext.")
    if encrypted[0] in (1, 2):
        iv, ciphertext = encrypted[1:13], encrypted[13:]
    else:
        iv, ciphertext = encrypted[:12], encrypted[12:]
    try:
        plaintext = AESGCM(key).decrypt(iv, ciphertext, None)
        return plaintext.decode("utf-8")
    except Exception as exc:
        raise SecretDropError("SnapPwd decryption failed.") from exc


def retrieve(url: str, *, allow_private: bool = False, api_base: str | None = None) -> str:
    parts = urlsplit(url)
    segments = [segment for segment in parts.path.split("/") if segment]
    try:
        idx = segments.index("g")
        secret_id = segments[idx + 1]
    except (ValueError, IndexError) as exc:
        raise SecretDropError("SnapPwd URL does not contain a secret id.") from exc
    if secret_id.startswith("spf-"):
        raise SecretDropError("SnapPwd file drops are not supported; use a text drop.")
    if not _ID_RE.fullmatch(secret_id):
        raise SecretDropError("SnapPwd secret id has an invalid shape.")
    key = parts.fragment
    if not key:
        raise SecretDropError("SnapPwd URL is missing its fragment encryption key.")
    if api_base:
        base = urlsplit(api_base.rstrip("/"))
        endpoint = urlunsplit((base.scheme, base.netloc, f"{base.path}/secrets/{secret_id}", "", ""))
    elif (parts.hostname or "").lower().endswith("snappwd.io"):
        endpoint = f"https://api.snappwd.io/v1/secrets/{secret_id}"
    else:
        endpoint = urlunsplit((parts.scheme, parts.netloc, f"/api/v1/secrets/{secret_id}", "", ""))
    _, payload, _ = request_json(endpoint, allow_private=allow_private)
    encrypted = payload.get("encryptedSecret") if payload else None
    if not isinstance(encrypted, str):
        raise SecretDropError("SnapPwd returned no encrypted text payload.")
    return _decrypt(encrypted, key)
