#!/usr/bin/env python3
"""
Bootstrap cross-signing from Beeper recovery key.

Steps:
  1. Read recovery key from ~/.secrets/beeper-recovery-key.txt
  2. Decode Matrix-style recovery key → 32-byte seed
  3. Derive secret storage key via HKDF-SHA256 (empty info)
  4. Verify MAC against m.secret_storage.key.<default>
  5. Download + decrypt secrets:
       - m.cross_signing.self_signing  (signs devices)
       - m.cross_signing.user_signing  (signs other users)
       - m.cross_signing.master         (root of trust)
  6. Sign our device bbctl_G7BAIUUU with the self_signing private key
  7. POST /keys/signatures/upload with the new signature
  8. Verify: re-query /keys/query, device should now have 2 signatures

Reference: Matrix spec §11.6 + synapse source.
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import nacl.signing
import nacl.encoding
import unpaddedbase64
from canonicaljson import encode_canonical_json
from Crypto.Cipher import AES
from Crypto.Hash import HMAC as pyHMAC, SHA256 as pySHA256

SECRETS_DIR = Path.home() / ".secrets"
RECOVERY_FILE = SECRETS_DIR / "beeper-recovery-key.txt"
BBCTL_CFG = Path.home() / ".config" / "bbctl" / "config.json"


def load_bbctl():
    data = json.loads(BBCTL_CFG.read_text())
    env = data["environments"]["prod"]
    return {
        "token": env["access_token"],
        "user_id": f"@{env['username']}:beeper.com",
        "homeserver": f"https://matrix.beeper.com/_hungryserv/{env['username']}",
        "device_id": data.get("device_id", ""),
    }


def api(method, path, creds, body=None):
    url = creds["homeserver"] + path
    headers = {"Authorization": f"Bearer {creds['token']}"}
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


# --- Matrix recovery key decoding --------------------------------------------

def decode_recovery_key(key_str: str) -> bytes:
    """Matrix recovery key format: base58 with OLM_RECOVERY_KEY_PREFIX (0x8B, 0x01)
    followed by 32 bytes seed and XOR parity byte.

    Spec: https://spec.matrix.org/v1.11/client-server-api/#recovery-key

    The visible format is groups of 4 base58 chars. We strip whitespace.
    """
    stripped = "".join(key_str.split())
    # Base58 decode (Bitcoin alphabet)
    ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    num = 0
    for c in stripped:
        idx = ALPHABET.index(c)
        num = num * 58 + idx
    # Convert to bytes (big-endian)
    raw = num.to_bytes((num.bit_length() + 7) // 8 or 1, "big")
    # Re-add leading zero bytes (each '1' in base58 represents a zero byte)
    n_leading = len(stripped) - len(stripped.lstrip("1"))
    raw = b"\x00" * n_leading + raw

    # Should be: 2-byte prefix (0x8B 0x01) + 32-byte seed + 1-byte parity
    if len(raw) != 35:
        raise ValueError(f"Unexpected decoded length {len(raw)} (expected 35)")
    if raw[0] != 0x8B or raw[1] != 0x01:
        raise ValueError(f"Bad prefix: {raw[:2].hex()}")
    # Parity check: XOR of all bytes should be 0
    parity = 0
    for b in raw:
        parity ^= b
    if parity != 0:
        raise ValueError("Parity check failed — recovery key corrupted")
    return raw[2:34]  # 32-byte seed


# --- Secret storage decryption -----------------------------------------------

def derive_ssss_keys(seed: bytes, name: str) -> tuple[bytes, bytes]:
    """Derive AES + HMAC keys from the SSSS master seed using HKDF-SHA256.

    Per Matrix spec, for an account data type like 'm.cross_signing.self_signing':
      - salt = b'\\0' * 32
      - info = name
      - output = 64 bytes = AES key (32) + HMAC key (32)
    """
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives import hashes

    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=64,
        salt=b"\x00" * 32,
        info=name.encode(),
    )
    derived = hkdf.derive(seed)
    return derived[:32], derived[32:]


def verify_default_key_mac(seed: bytes, key_meta: dict) -> bool:
    """Verify recovery key is correct using the MAC in m.secret_storage.key.<id>.

    The MAC is computed on a 32-byte zero plaintext encrypted with AES-CTR
    (using iv from the key metadata and an empty `name` info).
    """
    aes_key, hmac_key = derive_ssss_keys(seed, "")
    iv = unpaddedbase64.decode_base64(key_meta["iv"])
    zero = b"\x00" * 32
    cipher = AES.new(aes_key, AES.MODE_CTR, initial_value=iv, nonce=b"")
    ct = cipher.encrypt(zero)
    expected_mac = unpaddedbase64.decode_base64(key_meta["mac"])
    h = pyHMAC.new(hmac_key, digestmod=pySHA256)
    h.update(ct)
    actual_mac = h.digest()
    return hmac.compare_digest(expected_mac, actual_mac)


def decrypt_secret(seed: bytes, name: str, encrypted: dict, key_id: str) -> bytes:
    """Decrypt an SSSS secret stored under account data type `name`.

    encrypted is the full content, e.g.:
      {"encrypted": {"<key_id>": {"iv":..., "ciphertext":..., "mac":...}}}
    """
    payload = encrypted["encrypted"][key_id]
    aes_key, hmac_key = derive_ssss_keys(seed, name)
    iv = unpaddedbase64.decode_base64(payload["iv"])
    ct = unpaddedbase64.decode_base64(payload["ciphertext"])
    mac_expected = unpaddedbase64.decode_base64(payload["mac"])

    # Verify MAC
    h = pyHMAC.new(hmac_key, digestmod=pySHA256)
    h.update(ct)
    if not hmac.compare_digest(h.digest(), mac_expected):
        raise ValueError(f"MAC verification failed for {name}")

    cipher = AES.new(aes_key, AES.MODE_CTR, initial_value=iv, nonce=b"")
    pt = cipher.decrypt(ct)
    # Matrix stores the secret as a base64 string (of the raw ed25519 seed)
    return pt


# --- Cross-signing signing ---------------------------------------------------

def sign_device(device_keys: dict, self_signing_seed: bytes, our_user: str) -> str:
    """Compute an ed25519 signature of the canonical JSON of device_keys,
    using the self-signing private seed.

    Returns base64-encoded signature.
    """
    # Canonical JSON excludes 'signatures' and 'unsigned' fields
    signable = {k: v for k, v in device_keys.items() if k not in ("signatures", "unsigned")}
    raw = encode_canonical_json(signable)

    signing_key = nacl.signing.SigningKey(self_signing_seed)
    sig = signing_key.sign(raw).signature
    return unpaddedbase64.encode_base64(sig)


def ssk_public_key(self_signing_seed: bytes) -> str:
    signing_key = nacl.signing.SigningKey(self_signing_seed)
    verify_key = signing_key.verify_key
    return unpaddedbase64.encode_base64(bytes(verify_key))


# --- Main --------------------------------------------------------------------

def main() -> int:
    creds = load_bbctl()
    print(f"User: {creds['user_id']}")
    print(f"Our device: {creds['device_id']}")
    print()

    # Step 1-2: decode recovery key
    if not RECOVERY_FILE.exists():
        print(f"Recovery key file missing: {RECOVERY_FILE}", file=sys.stderr)
        return 1
    key_str = RECOVERY_FILE.read_text().strip()
    try:
        seed = decode_recovery_key(key_str)
    except Exception as e:
        print(f"Failed to decode recovery key: {e}", file=sys.stderr)
        return 1
    print(f"✓ Recovery key decoded ({len(seed)} bytes)")

    # Step 3-4: verify MAC
    default_key_info = api("GET", "/_matrix/client/v3/user/"
                           f"{urllib.parse.quote(creds['user_id'])}"
                           "/account_data/m.secret_storage.default_key", creds)
    key_id = default_key_info["key"]
    key_meta = api("GET", "/_matrix/client/v3/user/"
                   f"{urllib.parse.quote(creds['user_id'])}"
                   f"/account_data/m.secret_storage.key.{key_id}", creds)
    print(f"✓ Default SSSS key id: {key_id}")
    if not verify_default_key_mac(seed, key_meta):
        print("❌ Recovery key does not match the MAC. Wrong key?", file=sys.stderr)
        return 1
    print("✓ Recovery key MAC verified — it's the correct key.")

    # Step 5: decrypt cross-signing secrets
    secrets = {}
    for name in ("m.cross_signing.master",
                 "m.cross_signing.self_signing",
                 "m.cross_signing.user_signing"):
        data = api("GET",
                   "/_matrix/client/v3/user/"
                   f"{urllib.parse.quote(creds['user_id'])}"
                   f"/account_data/{name}", creds)
        pt = decrypt_secret(seed, name, data, key_id)
        # pt is base64-encoded seed (ed25519 32 bytes)
        seed_b = unpaddedbase64.decode_base64(pt.decode("ascii").strip())
        if len(seed_b) != 32:
            raise ValueError(f"{name}: expected 32-byte seed, got {len(seed_b)}")
        secrets[name] = seed_b
        print(f"✓ Decrypted {name}")

    self_signing_seed = secrets["m.cross_signing.self_signing"]
    expected_ssk_pub = ssk_public_key(self_signing_seed)
    print(f"  self-signing public key: ed25519:{expected_ssk_pub}")

    # Sanity: compare with published self-signing key
    keys_resp = api("POST", "/_matrix/client/v3/keys/query", creds,
                    {"device_keys": {creds["user_id"]: []}})
    published_ssk = keys_resp.get("self_signing_keys", {}).get(creds["user_id"], {})
    published_pub = next(iter(published_ssk.get("keys", {}).values()), None)
    if published_pub != expected_ssk_pub:
        print(f"❌ self-signing key mismatch:\n  expected {expected_ssk_pub}\n  published {published_pub}",
              file=sys.stderr)
        return 1
    print("✓ Self-signing public key matches the published one.")

    # Step 6-7: sign our device
    our_device = keys_resp["device_keys"][creds["user_id"]][creds["device_id"]]
    print(f"\nSigning device {creds['device_id']}…")
    sig_b64 = sign_device(our_device, self_signing_seed, creds["user_id"])
    print(f"  signature: {sig_b64[:40]}…")

    # Build updated device_keys with the new signature
    signed_device = json.loads(json.dumps(our_device))  # deep copy
    sigs = signed_device.setdefault("signatures", {}).setdefault(creds["user_id"], {})
    sigs[f"ed25519:{expected_ssk_pub}"] = sig_b64

    upload_body = {
        creds["user_id"]: {
            creds["device_id"]: signed_device
        }
    }
    resp = api("POST", "/_matrix/client/v3/keys/signatures/upload", creds, upload_body)
    failures = resp.get("failures", {})
    if failures:
        print(f"❌ upload had failures: {json.dumps(failures, indent=2)}", file=sys.stderr)
        return 1
    print("✓ Signature uploaded successfully.")

    # Step 8: verify
    print("\nVerifying…")
    keys_resp2 = api("POST", "/_matrix/client/v3/keys/query", creds,
                     {"device_keys": {creds["user_id"]: []}})
    final_device = keys_resp2["device_keys"][creds["user_id"]][creds["device_id"]]
    sig_keys = list(final_device.get("signatures", {}).get(creds["user_id"], {}).keys())
    print(f"  signature keys on our device: {sig_keys}")
    if f"ed25519:{expected_ssk_pub}" in sig_keys:
        print("\n🎉 SUCCESS — device is now cross-signed. Bridge should accept our messages.")
        return 0
    else:
        print("\n⚠ Signature uploaded but not visible on device yet. Try again in a moment.",
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
