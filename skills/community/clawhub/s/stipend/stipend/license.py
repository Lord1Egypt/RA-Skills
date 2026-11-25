"""Licence keys — verified offline, no phone-home, no account.

A licence is a short signed token. The package verifies it locally against a
public signer address baked in below. That means:

  * no licence server to call, so buying works even if stipend.sh is down
  * no account, no login, nothing to leak
  * the key cannot be forged without our private key
  * we cannot revoke one, which is a deliberate trade — a product that phones
    home to check permission is exactly what this whole thing is arguing against

Signing reuses the secp256k1 already present via eth-account. No new dependency
in a process that holds a private key.

Format:  STIPEND-<base64url(payload)>.<signature>
Payload: {"id": "<purchase id>", "at": <unix ts>, "tier": "paid"}
"""

import base64
import json
import os
import time

from .config import CONFIG_DIR, ensure_dirs

LICENSE_FILE = CONFIG_DIR / "license.key"
PREFIX = "STIPEND-"

# Public address of the licence signer. Verification only — the private key
# lives on the issuing server and never ships.
SIGNER_ADDRESS = os.environ.get(
    "STIPEND_LICENSE_SIGNER",
    "0xb12fb716b0D392979afe1480fBCFef56C0a3Ce6F",
)


class LicenseError(RuntimeError):
    pass


def _b64e(raw):
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def _b64d(text):
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def issue(purchase_id, private_key, tier="paid"):
    """Sign a licence. Runs on the issuing server only, never on a client."""
    from eth_account import Account
    from eth_account.messages import encode_defunct

    payload = json.dumps(
        {"id": str(purchase_id), "at": int(time.time()), "tier": tier},
        separators=(",", ":"), sort_keys=True,
    )
    body = _b64e(payload.encode())
    signed = Account.sign_message(encode_defunct(text=body), private_key=private_key)
    return f"{PREFIX}{body}.{signed.signature.hex()}"


def verify(key, signer=None):
    """Check a licence. Returns its payload, or raises LicenseError."""
    signer = (signer or SIGNER_ADDRESS).lower()
    if not key or not key.startswith(PREFIX):
        raise LicenseError("That does not look like a stipend licence key.")

    try:
        body, signature = key[len(PREFIX):].split(".", 1)
    except ValueError:
        raise LicenseError("Licence key is malformed — expected one '.' separator.")

    try:
        payload = json.loads(_b64d(body).decode())
    except Exception as e:
        raise LicenseError(f"Licence payload is unreadable: {e}") from e

    try:
        from eth_account import Account
        from eth_account.messages import encode_defunct
        recovered = Account.recover_message(
            encode_defunct(text=body),
            signature=signature if signature.startswith("0x") else "0x" + signature,
        )
    except ImportError as e:
        raise LicenseError("eth-account is required to verify a licence.") from e
    except Exception as e:
        raise LicenseError(f"Signature is not valid: {e}") from e

    if recovered.lower() != signer:
        raise LicenseError(
            "Licence was not signed by stipend. If you bought this, contact "
            "support rather than editing the key."
        )
    return payload


def install(key):
    """Store a verified licence. Refuses to store an invalid one."""
    payload = verify(key)
    ensure_dirs()
    LICENSE_FILE.write_text(key.strip(), encoding="utf-8")
    try:
        os.chmod(LICENSE_FILE, 0o600)
    except (OSError, NotImplementedError):
        pass
    return payload


def current():
    """The installed licence payload, or None. Never raises."""
    if not LICENSE_FILE.exists():
        return None
    try:
        return verify(LICENSE_FILE.read_text(encoding="utf-8").strip())
    except (LicenseError, OSError):
        return None


def is_paid():
    payload = current()
    return bool(payload and payload.get("tier") == "paid")


def require_paid(feature):
    """Gate a paid feature. Explains rather than just refusing."""
    if is_paid():
        return True
    raise LicenseError(
        f"{feature} is part of the paid tier ($39, one-off).\n"
        "The wallet, spending limits and x402 auto-pay stay free forever — this "
        "is the cost tracking that tells you whether an agent is worth running.\n"
        "  https://stipend.sh  ·  install a key with: stipend license add <key>"
    )
