#!/usr/bin/env python3
"""
x402 wire helpers: read and write x402 v1 AND v2 payment messages. Standard library only.

Why this file exists
--------------------
x402 v2 moved the payment request into a `PAYMENT-REQUIRED` response header, the buyer's payment
into a `PAYMENT-SIGNATURE` request header, renamed `maxAmountRequired` to `amount`, and names
networks by CAIP-2 (`eip155:8453`, `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp`). Our servers answer
both versions during the v1 sunset window. This module is the one place the payment scripts learn
which version to speak, so every script follows the same rules:

- Use v2 only when the 402 carries a valid `PAYMENT-REQUIRED` header with an option we can pay.
  Otherwise use v1 exactly as before (JSON body, `X-Payment` header, base64 JSON).
- `X402_WIRE=v1` in the environment forces v1.
- The signed inner payload is the same in v1 and v2 (EVM EIP-3009 authorization, or a Solana
  transaction), so the existing signers are reused unchanged.
- The v2 payment echoes the chosen `accepts` entry UNCHANGED as `accepted`, plus the 402's
  `resource` and `extensions`.
- Amounts are canonical integer strings of atomic units. Never floats.
- Solana ids and addresses are compared and emitted exactly (base58 is case-sensitive). An unknown
  network is never paid and never defaults to Base.
- After a payment is sent, a 202, a 5xx or a timeout is PENDING, not failed: never sign a second
  payment for it. Resend the same header, or stop and check.

The same file ships in the `singularity` / `x402-layer` and `x402-compute` skills. Keep the copies
identical. Encodings are tested byte-for-byte against the official `@x402/core` 2.32.0 encoder.
"""

import base64
import binascii
import json
import os
import re
from typing import Any, Dict, Optional, Tuple

HEADER_PAYMENT_REQUIRED = "PAYMENT-REQUIRED"
HEADER_PAYMENT_SIGNATURE = "PAYMENT-SIGNATURE"
HEADER_PAYMENT_RESPONSE = "PAYMENT-RESPONSE"
HEADER_X_PAYMENT = "X-Payment"
HEADER_X_PAYMENT_RESPONSE = "X-PAYMENT-RESPONSE"

# A PAYMENT-REQUIRED header lists a few offers plus optional schemas; anything near this is not one.
MAX_HEADER_CHARS = 64 * 1024

# Our v1 network name <-> CAIP-2, EXACT case. Mirrors packages/x402-kit KIT_NETWORKS.
NETWORKS = (
    ("base", "eip155:8453", "evm"),
    ("solana", "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp", "svm"),
    ("robinhood", "eip155:4663", "evm"),
    ("megaeth", "eip155:4326", "evm"),
    ("arc", "eip155:5042", "evm"),
    ("arc-testnet", "eip155:5042002", "evm"),
    ("base-sepolia", "eip155:84532", "evm"),
    ("solana-devnet", "solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1", "svm"),
)

_CANONICAL_UINT = re.compile(r"^(0|[1-9][0-9]{0,77})$")
_BASE64 = re.compile(r"^[A-Za-z0-9+/]*={0,2}$")

# Keys this module adds to a challenge dict. Scripts never send these anywhere.
WIRE_KEY = "_x402_wire"
REQUIRED_KEY = "_x402_payment_required"
ACCEPTED_KEY = "_x402_accepted"


def network_name(raw: Any) -> Optional[str]:
    """v1 name for a v1 name (any case) or an EXACT CAIP-2 id. Unknown -> None."""
    if not isinstance(raw, str):
        return None
    value = raw.strip()
    if not value:
        return None
    if ":" in value:
        for name, caip2, _kind in NETWORKS:
            if caip2 == value:
                return name
        return None
    lower = value.lower()
    for name, _caip2, _kind in NETWORKS:
        if name == lower:
            return name
    return None


def network_kind(raw: Any) -> Optional[str]:
    name = network_name(raw)
    for n, _caip2, kind in NETWORKS:
        if n == name:
            return kind
    return None


def caip2_for(raw: Any) -> Optional[str]:
    name = network_name(raw)
    for n, caip2, _kind in NETWORKS:
        if n == name:
            return caip2
    return None


def same_address(kind: str, a: Any, b: Any) -> bool:
    """EVM hex addresses compare case-insensitively; everything else (Solana) exactly."""
    if not isinstance(a, str) or not isinstance(b, str):
        return False
    x, y = a.strip(), b.strip()
    if not x or not y:
        return False
    hex_re = re.compile(r"^0x[0-9a-fA-F]{40}$")
    if kind == "evm" and hex_re.match(x) and hex_re.match(y):
        return x.lower() == y.lower()
    return x == y


def parse_atomic(value: Any) -> Optional[int]:
    """Canonical non-negative integer string of atomic units -> int. Anything else -> None."""
    if not isinstance(value, str) or not _CANONICAL_UINT.match(value):
        return None
    number = int(value)
    return number if number < (1 << 256) else None


def wire_forced_v1() -> bool:
    return (os.getenv("X402_WIRE") or "").strip().lower() == "v1"


def encode_header(obj: Dict[str, Any]) -> str:
    """base64(JSON) exactly as JavaScript's JSON.stringify + base64 of the UTF-8 bytes."""
    text = json.dumps(obj, separators=(",", ":"), ensure_ascii=False)
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def decode_header(value: Any) -> Optional[Dict[str, Any]]:
    """base64(JSON object) -> dict. Anything else -> None (never raises)."""
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text or len(text) > MAX_HEADER_CHARS or not _BASE64.match(text):
        return None
    try:
        raw = base64.b64decode(text + "=" * (-len(text) % 4), validate=True)
        parsed = json.loads(raw.decode("utf-8"))
    except (binascii.Error, ValueError, UnicodeDecodeError):
        return None
    return parsed if isinstance(parsed, dict) else None


def parse_payment_required(value: Any) -> Optional[Dict[str, Any]]:
    """A valid v2 PaymentRequired (x402Version 2, non-empty accepts list of objects) or None."""
    decoded = decode_header(value)
    if decoded is None or decoded.get("x402Version") != 2:
        return None
    accepts = decoded.get("accepts")
    if not isinstance(accepts, list) or not accepts or not all(isinstance(a, dict) for a in accepts):
        return None
    return decoded


def _v1_view(entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """A v2 `accepts` entry seen with the v1 field names the scripts already read.

    The original entry rides along under ACCEPTED_KEY and is what gets echoed back, unchanged.
    Entries we cannot pay safely are dropped: not `exact`, an unknown or wrongly-cased network,
    a non-integer amount, or a missing payee / asset.
    """
    if entry.get("scheme") != "exact":
        return None
    raw_network = entry.get("network")
    if not isinstance(raw_network, str) or ":" not in raw_network:
        return None
    name = network_name(raw_network)
    if name is None:
        return None
    amount = entry.get("amount")
    if parse_atomic(amount) is None:
        return None
    pay_to = entry.get("payTo")
    asset = entry.get("asset")
    if not isinstance(pay_to, str) or not pay_to.strip() or not isinstance(asset, str) or not asset.strip():
        return None
    extra = entry.get("extra")
    view = {
        "scheme": "exact",
        "network": name,
        "maxAmountRequired": amount,
        "amount": amount,
        "payTo": pay_to,
        "asset": asset,
        "extra": extra if isinstance(extra, dict) else {},
        ACCEPTED_KEY: entry,
    }
    if isinstance(entry.get("maxTimeoutSeconds"), int):
        view["maxTimeoutSeconds"] = entry["maxTimeoutSeconds"]
    return view


def _response_json(response: Any) -> Dict[str, Any]:
    try:
        body = response.json()
    except Exception:
        return {}
    return body if isinstance(body, dict) else {}


def read_challenge(response: Any) -> Dict[str, Any]:
    """Read a 402 response. Header first (v2), v1 JSON body as the fallback.

    Returns the v1 JSON body as a dict (so existing fields such as `singularity`, `package` or
    `extensions` still work), with `accepts` replaced by v1-shaped views of the v2 offers when v2
    is used. `challenge[WIRE_KEY]` is "v2" or "v1".
    """
    body = _response_json(response)
    payment_required = None
    if not wire_forced_v1():
        headers = getattr(response, "headers", None) or {}
        payment_required = parse_payment_required(headers.get(HEADER_PAYMENT_REQUIRED))

    if payment_required is not None:
        options = [v for v in (_v1_view(e) for e in payment_required["accepts"]) if v is not None]
        if options:
            challenge = dict(body)
            challenge["accepts"] = options
            challenge[WIRE_KEY] = "v2"
            challenge[REQUIRED_KEY] = payment_required
            if "extensions" not in challenge and isinstance(payment_required.get("extensions"), dict):
                challenge["extensions"] = payment_required["extensions"]
            return challenge

    challenge = dict(body)
    challenge[WIRE_KEY] = "v1"
    return challenge


def uses_v2(challenge: Dict[str, Any], option: Dict[str, Any]) -> bool:
    return (
        not wire_forced_v1()
        and challenge.get(WIRE_KEY) == "v2"
        and isinstance(challenge.get(REQUIRED_KEY), dict)
        and isinstance(option.get(ACCEPTED_KEY), dict)
    )


def v2_payment_header(challenge: Dict[str, Any], option: Dict[str, Any], inner: Dict[str, Any]) -> Tuple[str, str]:
    """(PAYMENT-SIGNATURE, base64 JSON) for the chosen v2 option and a signed inner payload."""
    if not uses_v2(challenge, option):
        raise ValueError("v2_payment_header needs a v2 challenge and one of its options")
    required = challenge[REQUIRED_KEY]
    envelope: Dict[str, Any] = {"x402Version": 2}
    if isinstance(required.get("resource"), dict):
        envelope["resource"] = required["resource"]
    envelope["accepted"] = option[ACCEPTED_KEY]
    envelope["payload"] = inner
    if isinstance(required.get("extensions"), dict):
        envelope["extensions"] = required["extensions"]
    return HEADER_PAYMENT_SIGNATURE, encode_header(envelope)


def read_payment_response(response: Any) -> Optional[Dict[str, Any]]:
    """Settlement result from PAYMENT-RESPONSE (v2) or X-PAYMENT-RESPONSE (v1), if present."""
    headers = getattr(response, "headers", None) or {}
    for name in (HEADER_PAYMENT_RESPONSE, HEADER_X_PAYMENT_RESPONSE):
        decoded = decode_header(headers.get(name))
        if decoded is not None:
            return decoded
    return None


def is_ambiguous_status(status_code: Any) -> bool:
    """After a payment was SENT: 202 (settling) and any 5xx may mean the money moved."""
    return isinstance(status_code, int) and (status_code == 202 or status_code >= 500)


def pending_result(status_code: Optional[int] = None, detail: Any = None) -> Dict[str, Any]:
    """The answer to give when a sent payment's outcome is unknown. Never 'failed'."""
    result: Dict[str, Any] = {
        "pending": True,
        "status": status_code,
        "error": "Payment outcome not confirmed yet. The payment may have gone through.",
        "next_step": (
            "Do NOT sign or pay again. Retry later with the same payment header, "
            "or check your wallet history and the seller before paying again."
        ),
    }
    if detail:
        result["detail"] = str(detail)[:500]
    return result
