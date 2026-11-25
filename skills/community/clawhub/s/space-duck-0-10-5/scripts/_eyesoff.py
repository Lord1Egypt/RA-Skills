#!/usr/bin/env python3
"""Eyes Off — end-to-end encrypted peck bodies ([EYES-OFF-P1],
docs/spec/PECK-E2EE-EYES-OFF.md).

Sealed-box v1: X25519 + XSalsa20-Poly1305 (libsodium crypto_box_seal via
PyNaCl). Encrypt/decrypt happen only on the duck's own box; the platform
stores ciphertext it cannot read. Metadata (sender/recipient/type/time)
stays plaintext so bond checks, rate caps, and approval gates keep working.

Key custody (mirrors the v3 sign_key.hex idiom in _envelope.py):
  ~/.space-duck/enc_key.hex  — 64 lowercase hex chars = 32 raw X25519
  private-key bytes, chmod 0600, NEVER leaves the box, never logged.
  The public key is registered to the duck's row as PEM SPKI
  (`enc_pubkey_pem`, scheme ENC_SCHEME below).

API:
  available()                  -> (bool, reason)  crypto deps present?
  ensure_enc_key()             -> (privkey_hex, pub_pem) generate+cache on first run
  load_enc_key()               -> (privkey_hex, pub_pem) or (None, None)
  pub_pem_from_priv(hex)       -> PEM SPKI str for the matching public key
  seal(plaintext, pem)         -> base64 ciphertext str (for recipient pem)
  unseal(ciphertext_b64)       -> plaintext str (with the local private key)

CLI:
  python3 _eyesoff.py setup    — generate key if missing, print pub PEM + status
  python3 _eyesoff.py status   — report key presence + crypto availability
  python3 _eyesoff.py register — setup + register the PUBLIC key with the
                                 platform (POST /beak/duck/<self>/enc-key,
                                 own beak key). For ducks paired before
                                 0.9.9 — pairing after [EYES-OFF-P1]
                                 registers automatically.

Fail-closed doctrine: when a connection has encryption ON, callers must
treat any error from seal()/unseal() as a hard stop — NEVER fall back to
sending plaintext. (Enforced again server-side from [EYES-OFF-P2].)
"""
import base64
import json
import sys
from pathlib import Path

ENC_KEY_PATH = Path.home() / '.space-duck' / 'enc_key.hex'
ENC_SCHEME = 'x25519-xsalsa20poly1305-sealedbox-v1'


def available():
    """Return (ok, reason). Both PyNaCl (sealed box) and cryptography (PEM
    SPKI encode/decode) are required; pure-python fallbacks are rejected by
    design (constant-time concerns — spec §3.3)."""
    try:
        import nacl.public  # noqa: F401
    except Exception:
        return False, 'PyNaCl not installed (pip install pynacl)'
    try:
        from cryptography.hazmat.primitives.asymmetric import x25519  # noqa: F401
    except Exception:
        return False, 'cryptography not installed (pip install cryptography)'
    return True, ''


def pub_pem_from_priv(privkey_hex):
    """PEM SPKI (-----BEGIN PUBLIC KEY-----) for the X25519 public key
    matching 32 raw private bytes given as 64 hex chars."""
    from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    priv = X25519PrivateKey.from_private_bytes(bytes.fromhex(privkey_hex))
    return priv.public_key().public_bytes(
        serialization.Encoding.PEM,
        serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode('ascii')


def _raw_pub_from_pem(pem_str):
    """32 raw X25519 public-key bytes from a PEM SPKI string."""
    from cryptography.hazmat.primitives.serialization import load_pem_public_key
    from cryptography.hazmat.primitives import serialization
    pub = load_pem_public_key(pem_str.encode('ascii'))
    return pub.public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw)


def load_enc_key():
    """Read ~/.space-duck/enc_key.hex -> (privkey_hex, pub_pem) or (None, None)."""
    if not ENC_KEY_PATH.exists():
        return None, None
    try:
        privkey_hex = ENC_KEY_PATH.read_text().strip().lower()
        if len(privkey_hex) != 64:
            return None, None
        bytes.fromhex(privkey_hex)
        return privkey_hex, pub_pem_from_priv(privkey_hex)
    except Exception:
        return None, None


def ensure_enc_key():
    """Return (privkey_hex, pub_pem) — generate + cache 0600 on first run."""
    privkey_hex, pub_pem = load_enc_key()
    if privkey_hex:
        return privkey_hex, pub_pem
    import os
    privkey_hex = os.urandom(32).hex()
    ENC_KEY_PATH.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    ENC_KEY_PATH.write_text(privkey_hex + '\n')
    ENC_KEY_PATH.chmod(0o600)
    return privkey_hex, pub_pem_from_priv(privkey_hex)


def seal(plaintext, recipient_pub_pem):
    """Sealed-box encrypt `plaintext` (str) to the recipient's PEM SPKI
    public key. Returns base64 ciphertext. Raises on any failure — callers
    must hard-stop, never downgrade to plaintext."""
    from nacl.public import PublicKey, SealedBox
    raw_pub = _raw_pub_from_pem(recipient_pub_pem)
    box = SealedBox(PublicKey(raw_pub))
    ct = box.encrypt(plaintext.encode('utf-8'))
    return base64.b64encode(bytes(ct)).decode('ascii')


def unseal(ciphertext_b64):
    """Sealed-box decrypt with the local private key. Returns plaintext str.
    Raises on missing key or MAC/key mismatch (e.g. peer encrypted to a
    rotated key) — callers surface the error, never guess."""
    from nacl.public import PrivateKey, SealedBox
    privkey_hex, _ = load_enc_key()
    if not privkey_hex:
        raise RuntimeError('no local enc key (~/.space-duck/enc_key.hex missing) '
                           '— run: python3 _eyesoff.py setup')
    box = SealedBox(PrivateKey(bytes.fromhex(privkey_hex)))
    pt = box.decrypt(base64.b64decode(ciphertext_b64))
    return pt.decode('utf-8')


def _cli():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'status'
    ok, reason = available()
    if cmd == 'setup':
        if not ok:
            print(json.dumps({'ok': False, 'error': f'crypto unavailable: {reason}'}))
            sys.exit(1)
        existed = ENC_KEY_PATH.exists()
        _, pub_pem = ensure_enc_key()
        print(json.dumps({
            'ok': True,
            'created': not existed,
            'enc_key_path': str(ENC_KEY_PATH),
            'enc_scheme': ENC_SCHEME,
            'enc_pubkey_pem': pub_pem,
        }, indent=2))
    elif cmd == 'status':
        privkey_hex, pub_pem = load_enc_key()
        print(json.dumps({
            'crypto_available': ok,
            'crypto_reason': reason,
            'enc_key_present': bool(privkey_hex),
            'enc_scheme': ENC_SCHEME,
            'enc_pubkey_pem': pub_pem or '',
        }, indent=2))
    elif cmd == 'register':
        # [EYES-OFF 0.9.10] Self-registration for ducks paired before the
        # enc key existed. Same endpoint pairing uses; authed with this
        # duck's OWN beak key (server rejects peer keys, [EYES-OFF-P2]).
        # Space Duck's own backend only — no third-party hosts.
        if not ok:
            print(json.dumps({'ok': False, 'error': f'crypto unavailable: {reason}'}))
            sys.exit(1)
        import urllib.request, urllib.error
        cfg_path = Path.home() / '.space-duck' / 'config.json'
        try:
            cfg = json.loads(cfg_path.read_text())
        except Exception as e:
            print(json.dumps({'ok': False, 'error': f'config unreadable: {e}'}))
            sys.exit(1)
        sdid = str(cfg.get('spaceduck_id', '')).strip().upper()
        beak_key = cfg.get('beak_key', '')
        api = str(cfg.get('api_base', '') or
                  'https://beak.spaceduckling.com').rstrip('/')
        if not sdid or not beak_key:
            print(json.dumps({'ok': False,
                              'error': 'spaceduck_id/beak_key missing from config'}))
            sys.exit(1)
        _, pub_pem = ensure_enc_key()
        req = urllib.request.Request(
            f'{api}/beak/duck/{sdid}/enc-key',
            data=json.dumps({'enc_pubkey_pem': pub_pem,
                             'enc_scheme': ENC_SCHEME}).encode(),
            headers={'Content-Type': 'application/json',
                     'X-Beak-Key': beak_key},
            method='POST',
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as r:
                resp = json.loads(r.read())
            print(json.dumps({'ok': True, 'spaceduck_id': sdid,
                              'enc_scheme': ENC_SCHEME,
                              'server': resp}, indent=2))
        except urllib.error.HTTPError as e:
            try:
                detail = json.loads(e.read())
            except Exception:
                detail = {}
            print(json.dumps({'ok': False, 'error': f'http_{e.code}',
                              'detail': detail}, indent=2))
            sys.exit(1)
        except Exception as e:
            print(json.dumps({'ok': False, 'error': str(e)[:160]}))
            sys.exit(1)
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == '__main__':
    _cli()
