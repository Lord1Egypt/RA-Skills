#!/usr/bin/env python3
"""
Import the Matrix key backup into the local Olm store.

Without this step, historical encrypted messages (Megolm group sessions)
stored in Beeper's server-side key backup are unreachable: the long-running
sync daemon only accumulates NEW sessions received via to_device after it
was started.

Flow:
  1. Load bbctl token + recovery key seed (32 bytes from base58 recovery key)
  2. Decrypt SSSS secret `m.megolm_backup.v1` → 32-byte Curve25519 private key
     of the backup
  3. Validate: derived public key matches the one in the active backup version
  4. GET /room_keys/version to pick the active version
  5. GET /room_keys/keys?version=X to download all encrypted room-key sessions
  6. For each session: decrypt with
     m.megolm_backup.v1.curve25519-aes-sha2 algorithm
       - ECDH: shared = X25519(backup_private, ephemeral_public)
       - HKDF-SHA256(info=""): 32 aes_key + 32 mac_key + 16 aes_iv
       - Wait, actually the spec: HKDF yields aes_key (32) || mac_key (32);
         the iv is transmitted in the ciphertext envelope? No — the spec
         splits 80 bytes: aes_key (32) + mac_key (32) + aes_iv (16).
         Let me re-check: per Matrix spec §11.2 / backup algorithm
         m.megolm_backup.v1.curve25519-aes-sha2:
           derived = HKDF(SHA-256, shared, salt=0*32, info="", len=80)
           aes_key = derived[0:32], mac_key = derived[32:64], aes_iv = derived[64:80]
           Then verify HMAC-SHA256(mac_key, ciphertext) == mac (truncated first 8 bytes)
           Then decrypt AES-256-CBC with pkcs7 padding? No — AES-CBC no padding,
           plaintext is JSON matching BackedUpRoomKey shape.
         Actually per spec: HMAC-SHA-256(mac_key, ciphertext)[:32] == mac
         and AES-256-CBC with plaintext padded with PKCS#7.
  7. Build Element-compatible export JSON and inject into the Olm store
     of the same client the daemon uses (~/.local/share/clawd-matrix/).

Reference:
  https://spec.matrix.org/v1.11/client-server-api/#backup-algorithm-mmegolm_backupv1curve25519-aes-sha2
"""
from __future__ import annotations

import argparse
import asyncio
import base64
import hmac
import json
import logging
import os
import sys
import urllib.parse
import urllib.request
from hashlib import sha256
from pathlib import Path

import unpaddedbase64
from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey,
    X25519PublicKey,
)
from cryptography.hazmat.primitives import serialization

from Crypto.Cipher import AES as PCAES
from Crypto.Hash import HMAC as pyHMAC, SHA256 as pySHA256

# Reuse SSSS decryption from bootstrap_crosssign
sys.path.insert(0, str(Path(__file__).parent))
from bootstrap_crosssign import (  # noqa: E402
    load_bbctl,
    decode_recovery_key,
    verify_default_key_mac,
    decrypt_secret,
    api,
)

# Silence nio noise
logging.getLogger("nio").setLevel(logging.ERROR)

RECOVERY_FILE = Path.home() / ".secrets" / "beeper-recovery-key.txt"


# --- Backup key handling -----------------------------------------------------

def fetch_ssss_key_id(creds) -> str:
    data = api("GET",
               "/_matrix/client/v3/user/"
               f"{urllib.parse.quote(creds['user_id'])}"
               "/account_data/m.secret_storage.default_key", creds)
    return data["key"]


def fetch_ssss_key_meta(creds, key_id: str) -> dict:
    return api("GET",
               "/_matrix/client/v3/user/"
               f"{urllib.parse.quote(creds['user_id'])}"
               f"/account_data/m.secret_storage.key.{key_id}", creds)


def fetch_backup_secret(creds) -> dict:
    return api("GET",
               "/_matrix/client/v3/user/"
               f"{urllib.parse.quote(creds['user_id'])}"
               "/account_data/m.megolm_backup.v1", creds)


def derive_backup_public_from_private(priv: bytes) -> str:
    """Derive unpadded-b64 Curve25519 public key from 32-byte private key."""
    sk = X25519PrivateKey.from_private_bytes(priv)
    pub_raw = sk.public_key().public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw,
    )
    return unpaddedbase64.encode_base64(pub_raw)


def backup_decrypt_session(
    backup_priv: bytes,
    session_data: dict,
) -> bytes:
    """Decrypt a single session_data entry per
    m.megolm_backup.v1.curve25519-aes-sha2.

    session_data = {"ephemeral": str, "ciphertext": str, "mac": str}
    Returns the JSON plaintext bytes (BackedUpRoomKey shape).
    """
    ephemeral_pub_raw = unpaddedbase64.decode_base64(session_data["ephemeral"])
    ciphertext = unpaddedbase64.decode_base64(session_data["ciphertext"])
    mac_expected = unpaddedbase64.decode_base64(session_data["mac"])

    # ECDH (x25519)
    sk = X25519PrivateKey.from_private_bytes(backup_priv)
    peer = X25519PublicKey.from_public_bytes(ephemeral_pub_raw)
    shared = sk.exchange(peer)

    # HKDF-SHA256 per vodozemac/libolm: salt = single 0x00 byte, info = empty,
    # output = 80 bytes split into aes_key(32) || mac_key(32) || aes_iv(16).
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=80,
        salt=b"\x00",
        info=b"",
    )
    derived = hkdf.derive(shared)
    aes_key = derived[:32]
    mac_key = derived[32:64]
    aes_iv = derived[64:80]

    # Known libolm/vodozemac bug: the MAC is computed on an EMPTY input,
    # not on the ciphertext, and truncated to 8 bytes.
    # See https://github.com/matrix-org/vodozemac/blob/main/src/pk_encryption.rs
    # ("BUG: This is a know issue, we check the MAC of an empty message...")
    h = pyHMAC.new(mac_key, digestmod=pySHA256)
    actual_mac = h.digest()
    if not hmac.compare_digest(actual_mac[:len(mac_expected)], mac_expected):
        raise ValueError(
            f"MAC mismatch on backup session "
            f"(got {actual_mac[:len(mac_expected)].hex()}, want {mac_expected.hex()})"
        )

    # AES-256-CBC decrypt with PKCS#7 unpadding
    cipher = Cipher(algorithms.AES(aes_key), modes.CBC(aes_iv))
    dec = cipher.decryptor()
    pt_padded = dec.update(ciphertext) + dec.finalize()
    unpadder = sym_padding.PKCS7(128).unpadder()
    pt = unpadder.update(pt_padded) + unpadder.finalize()
    return pt


# --- Fetch backup ------------------------------------------------------------

def fetch_backup_version(creds) -> dict:
    return api("GET", "/_matrix/client/v3/room_keys/version", creds)


def fetch_all_sessions(creds, version: str) -> dict:
    q = urllib.parse.quote(version)
    return api("GET",
               f"/_matrix/client/v3/room_keys/keys?version={q}",
               creds)


# --- Import into nio store ---------------------------------------------------

async def import_sessions_into_nio(element_export: list[dict]) -> int:
    """Take a list of Element-export-format session dicts and save them into
    the nio Olm store, so the client can decrypt historical events.

    Element export format entries look like:
      {
        "algorithm": "m.megolm.v1.aes-sha2",
        "room_id": "!xxx:server",
        "sender_key": "Curve25519PubB64",
        "session_id": "...",
        "session_key": "...",       # exported megolm key
        "sender_claimed_keys": {"ed25519": "Ed25519PubB64"},
        "forwarding_curve25519_key_chain": []
      }
    """
    from nio_client import make_client  # noqa: E402
    from nio.crypto.olm_machine import Olm

    client = await make_client()
    try:
        olm = client.olm
        if olm is None:
            print("ERROR: client.olm is None — e2ee not enabled?", file=sys.stderr)
            return 0

        imported = 0
        skipped = 0
        for s in element_export:
            if s.get("algorithm") != "m.megolm.v1.aes-sha2":
                skipped += 1
                continue
            session = Olm._import_group_session(
                s["session_key"],
                s["sender_claimed_keys"]["ed25519"],
                s["sender_key"],
                s["room_id"],
                s.get("forwarding_curve25519_key_chain", []),
            )
            if session is None:
                skipped += 1
                continue
            olm.save_inbound_group_session(session)
            imported += 1

        return imported
    finally:
        await client.close()


# --- Main --------------------------------------------------------------------

async def amain(args) -> int:
    creds = load_bbctl()
    print(f"User:       {creds['user_id']}")
    print(f"Device:     {creds['device_id']}")
    print(f"Homeserver: {creds['homeserver']}")
    print()

    # 1. Load recovery key
    if not RECOVERY_FILE.exists():
        print(f"Missing recovery key file: {RECOVERY_FILE}", file=sys.stderr)
        return 1
    seed = decode_recovery_key(RECOVERY_FILE.read_text().strip())
    print(f"✓ Recovery key decoded ({len(seed)} bytes)")

    # 2. Verify MAC of default key
    key_id = fetch_ssss_key_id(creds)
    key_meta = fetch_ssss_key_meta(creds, key_id)
    if not verify_default_key_mac(seed, key_meta):
        print("❌ Recovery key MAC mismatch — wrong key?", file=sys.stderr)
        return 1
    print(f"✓ Default SSSS key verified (id={key_id})")

    # 3. Decrypt m.megolm_backup.v1 SSSS secret → backup private key
    backup_enc = fetch_backup_secret(creds)
    backup_priv_b64 = decrypt_secret(
        seed, "m.megolm_backup.v1", backup_enc, key_id
    ).decode("ascii").strip()
    backup_priv = unpaddedbase64.decode_base64(backup_priv_b64)
    if len(backup_priv) != 32:
        print(f"❌ Unexpected backup priv length: {len(backup_priv)}", file=sys.stderr)
        return 1
    print(f"✓ Decrypted backup private key (32 bytes)")

    # 4. Fetch backup version and validate public key match
    version_info = fetch_backup_version(creds)
    version = version_info["version"]
    algo = version_info["algorithm"]
    expected_pub = version_info["auth_data"]["public_key"]
    if algo != "m.megolm_backup.v1.curve25519-aes-sha2":
        print(f"❌ Unsupported backup algorithm: {algo}", file=sys.stderr)
        return 1
    derived_pub = derive_backup_public_from_private(backup_priv)
    if derived_pub != expected_pub:
        print(f"❌ Public key mismatch:\n  expected {expected_pub}\n  derived  {derived_pub}",
              file=sys.stderr)
        return 1
    print(f"✓ Backup public key matches (version={version}, count={version_info['count']})")

    # 5. Download all sessions
    print("\nDownloading backup sessions...")
    all_data = fetch_all_sessions(creds, version)
    rooms = all_data.get("rooms", {})
    total_sessions = sum(len(r.get("sessions", {})) for r in rooms.values())
    print(f"  {len(rooms)} rooms, {total_sessions} sessions")

    # 6. Decrypt each session + build Element export entries
    print("\nDecrypting sessions...")
    element_export: list[dict] = []
    errors = 0
    for room_id, room_entry in rooms.items():
        for session_id, session_entry in room_entry.get("sessions", {}).items():
            sd = session_entry.get("session_data", {})
            try:
                pt_json = backup_decrypt_session(backup_priv, sd)
                payload = json.loads(pt_json)
                # BackedUpRoomKey: {algorithm, sender_key, session_key, sender_claimed_keys, forwarding_curve25519_key_chain}
                element_export.append({
                    "algorithm": payload["algorithm"],
                    "room_id": room_id,
                    "sender_key": payload["sender_key"],
                    "session_id": session_id,
                    "session_key": payload["session_key"],
                    "sender_claimed_keys": payload.get("sender_claimed_keys", {}),
                    "forwarding_curve25519_key_chain":
                        payload.get("forwarding_curve25519_key_chain", []),
                })
            except Exception as e:
                errors += 1
                if errors <= 3:
                    print(f"  [warn] decrypt {room_id[:20]} {session_id[:20]}: {e}",
                          file=sys.stderr)
    print(f"✓ Decrypted {len(element_export)}/{total_sessions} sessions"
          f" ({errors} errors)")

    if args.dump_export:
        outp = Path(args.dump_export)
        outp.write_text(json.dumps(element_export, indent=2))
        print(f"✓ Dumped Element-format JSON export to {outp}")

    if args.no_import:
        print("--no-import set, stopping before touching nio store.")
        return 0

    # 7. Import into nio Olm store
    print("\nImporting into nio Olm store...")
    imported = await import_sessions_into_nio(element_export)
    print(f"✓ Imported {imported} sessions into ~/.local/share/clawd-matrix/")

    print("\n🎉 Done. Restart the sync daemon to pick up the new sessions:")
    print("    systemctl --user restart clawd-beeper-sync")
    print("Then try: `nio_client.py history --room '!xxx:beeper.local' --limit 20`")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Import Matrix key backup into nio store")
    parser.add_argument("--dump-export", help="Also write Element-format JSON export to this path")
    parser.add_argument("--no-import", action="store_true",
                        help="Decrypt only, do not write to the nio Olm store")
    args = parser.parse_args()
    return asyncio.run(amain(args))


if __name__ == "__main__":
    sys.exit(main())
