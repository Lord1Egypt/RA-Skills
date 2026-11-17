#!/usr/bin/env python3
"""
Space Duck — Ed25519 signing-key setup / status / rotation for envelope v3.

INTENT: Generate a per-duck Ed25519 keypair on the owner's box, register the
        PUBLIC key with the Space Duck backend, and enable v3-signed pecks.
        The private key never leaves this machine (LANE-IS-IMMUTABLE
        doctrine — see docs/spec/BEAK-V3-ASYMMETRIC-IDENTITY.md §3.1).

CALLS:  POST <api>/beak/duck/sign-key/bootstrap  (X-Beak-Key auth)
        POST <api>/beak/duck/sign-key/rotate     (X-Beak-Key + old-key
                                                  attestation — [BEAK-V3-P2D])
        Space Duck's own backend only. No third-party hosts.

AUTH:   X-Beak-Key header from ~/.space-duck/config.json (chmod 600).
        The bootstrap endpoint is the ALREADY-PAIRED lane — it takes a
        first sign-key on a duck that has a beak_key but no live Cognito
        JWT (the Lane A common case). Autonomous rotation (v0.5.1) uses
        the same X-Beak-Key auth but ALSO requires an attestation
        envelope signed by the OLD private key so the server knows the
        current holder is asking. Owner has a 24 h window to revert from
        Mission Control if the rotate was theft-driven.

Files:
  ~/.space-duck/sign_key.hex  — 64 lowercase hex chars = 32 raw Ed25519
                                private-key bytes. Written 0600. NEVER
                                transmitted.
  ~/.space-duck/config.json   — updated with `sign_key_id` and
                                `envelope_v3: true` on successful setup.

Usage:
  python3 sign_key.py setup     # generate, register, wire config
  python3 sign_key.py status    # show local + registered state
  python3 sign_key.py rotate    # generate new keypair, attest with old key,
                                # rotate on server, replace local privkey atomically
"""
import argparse, hashlib, json, os, stat, sys, time, urllib.error, urllib.request
from pathlib import Path

CONFIG_DIR  = Path.home() / '.space-duck'
CONFIG_PATH = CONFIG_DIR / 'config.json'
SIGN_KEY_PATH = CONFIG_DIR / 'sign_key.hex'
DEFAULT_API = 'https://beak.spaceduckling.com'


def _load_config():
    if not CONFIG_PATH.exists():
        print('ERROR: No Space Duck config found. Run scripts/pair.py or scripts/setup.py first.')
        sys.exit(1)
    cfg = json.loads(CONFIG_PATH.read_text())
    from _apiguard import check_api_base  # [HARDEN-071]
    check_api_base(cfg)
    return cfg


def _save_config(cfg):
    CONFIG_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2))
    try:
        CONFIG_PATH.chmod(0o600)
    except OSError:
        pass


def _api_base(cfg):
    # Match send_peck.py's resolver: config wins, default to prod.
    return cfg.get('api_base', DEFAULT_API)


def _ensure_cryptography():
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey  # noqa: F401
    except ImportError:
        print('ERROR: v3 signing needs the `cryptography` package.')
        print('  Install with: pip install cryptography')
        sys.exit(1)


def _generate_keypair():
    _ensure_cryptography()
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives import serialization
    priv = Ed25519PrivateKey.generate()
    raw_priv = priv.private_bytes(
        serialization.Encoding.Raw,
        serialization.PrivateFormat.Raw,
        serialization.NoEncryption(),
    )
    raw_pub = priv.public_key().public_bytes(
        serialization.Encoding.Raw, serialization.PublicFormat.Raw)
    return raw_priv.hex(), raw_pub.hex()


def _write_sign_key(privkey_hex):
    CONFIG_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)
    # Write via a private temp then rename so we never leave a world-readable
    # window on the private key.
    tmp = SIGN_KEY_PATH.with_suffix('.hex.tmp')
    with open(tmp, 'w') as f:
        f.write(privkey_hex + '\n')
    try:
        os.chmod(tmp, 0o600)
    except OSError:
        pass
    os.replace(tmp, SIGN_KEY_PATH)


def _post_bootstrap(api, beak_key, pubkey_hex):
    body = json.dumps({'sign_pubkey': pubkey_hex}).encode()
    req = urllib.request.Request(
        f'{api}/beak/duck/sign-key/bootstrap',
        data=body, method='POST',
        headers={'Content-Type': 'application/json',
                 'X-Beak-Key': beak_key})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except Exception:
            return e.code, {'error': f'http_{e.code}'}
    except Exception as e:
        return 0, {'error': f'transport: {e}'}


# Import the shared envelope helper so status + future signing use the same
# derive_key_id / load_sign_key logic as send_peck.py. Sibling-dir import
# pattern mirrors send_peck.py's `sys.path.insert` recipe.
import pathlib as _pl
_script_dir = str(_pl.Path(__file__).resolve().parent)
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)
from _envelope import canonical_v3, derive_key_id, load_sign_key, sign_v3  # noqa: F401


def cmd_setup(args):
    """Generate a keypair (or reuse the one on disk) and bootstrap-register
    the pubkey with the backend. Idempotent — a re-run with the same on-disk
    key hits the 200 `already:true` branch on the server."""
    cfg = _load_config()
    api = _api_base(cfg)
    beak_key = cfg.get('beak_key', '')
    sdid = cfg.get('spaceduck_id', '')
    if not beak_key or not sdid:
        print('ERROR: config.json missing beak_key or spaceduck_id — repair pairing first.')
        sys.exit(1)

    # Reuse an existing on-disk key if present; regenerate only with --force.
    existing_priv, existing_pub, existing_kid = load_sign_key()
    if existing_priv and not args.force:
        print(f'🔑 Reusing existing sign key at {SIGN_KEY_PATH} (key_id={existing_kid})')
        priv_hex, pub_hex = existing_priv, existing_pub
    else:
        _ensure_cryptography()
        priv_hex, pub_hex = _generate_keypair()
        _write_sign_key(priv_hex)
        print(f'🔑 Generated new Ed25519 keypair — private key at {SIGN_KEY_PATH} (0600)')

    key_id = derive_key_id(pub_hex)
    print(f'   Public key:  {pub_hex[:16]}…  key_id={key_id}')
    print(f'📡 Registering with backend (POST /beak/duck/sign-key/bootstrap)...')
    status, resp = _post_bootstrap(api, beak_key, pub_hex)
    if status == 200:
        server_kid = resp.get('key_id', '')
        if server_kid and server_kid != key_id:
            print(f'⚠️  Server-derived key_id {server_kid} != local {key_id} — refusing to update config.')
            sys.exit(2)
        if resp.get('already'):
            print(f'✅ Already registered on this duck (key_id={server_kid}).')
        else:
            print(f'✅ Registered (key_id={server_kid}).')
        cfg['sign_key_id'] = server_kid or key_id
        cfg['envelope_v3'] = True
        _save_config(cfg)
        print(f'💾 Config updated: envelope_v3=true, sign_key_id={cfg["sign_key_id"]}')
        return 0
    if status == 409:
        current = resp.get('current_key_id', '')
        print('⚠️  A DIFFERENT sign_pubkey is already registered on this duck.')
        print(f'   current server key_id: {current}')
        print(f'   local key_id:          {key_id}')
        print()
        print('   Bootstrap is first-writer-wins (TOFU). To replace an existing key,')
        print('   an owner must sign in to Mission Control and rotate via:')
        print(f'     POST /beak/duck/{sdid}/sign-key/rotate')
        print('   (requires JWT + an attestation signed by the OLD key).')
        return 3
    if status == 403:
        print(f'❌ Backend refused (403): {resp.get("error", "invalid beak_key")}')
        print('   Check config.json beak_key; re-pair if it was rotated.')
        return 4
    print(f'❌ Bootstrap failed: HTTP {status} — {json.dumps(resp)[:220]}')
    return 1


def cmd_status(args):
    cfg = _load_config()
    priv_hex, pub_hex, key_id = load_sign_key()
    cfg_kid = cfg.get('sign_key_id', '')
    v3 = bool(cfg.get('envelope_v3'))
    print(f'sign_key.hex:   {"present" if priv_hex else "absent"}   ({SIGN_KEY_PATH})')
    if priv_hex:
        try:
            mode = stat.S_IMODE(os.stat(SIGN_KEY_PATH).st_mode)
            print(f'  perms:        {oct(mode)}  (want 0o600)')
        except OSError:
            pass
        print(f'  key_id:       {key_id}')
        print(f'  pubkey:       {pub_hex[:32]}…')
    print(f'config.sign_key_id:  {cfg_kid or "(unset)"}')
    print(f'config.envelope_v3:  {v3}')
    if priv_hex and cfg_kid and key_id != cfg_kid:
        print('⚠️  On-disk key_id does not match config.sign_key_id — '
              'run `sign_key.py setup` to re-sync (or investigate a rotate).')
    if priv_hex and not v3:
        print('ℹ️  A local sign key exists but envelope_v3 is not enabled in config. '
              'Run `sign_key.py setup` to register + enable.')
    return 0


def _post_box_rotate(api, beak_key, new_pubkey_hex, attestation_env, attestation_sig):
    """POST /beak/duck/sign-key/rotate — the [BEAK-V3-P2D] box-lane route.

    X-Beak-Key auth (no Cognito JWT) + attestation envelope signed by the
    CURRENT/OLD sign key. On 200 the server has installed the new pubkey and
    set a 24 h owner-revert window (sign_revert_until).
    """
    body = json.dumps({
        'sign_pubkey': new_pubkey_hex,
        'attestation': {'envelope': attestation_env, 'signature': attestation_sig},
    }).encode()
    req = urllib.request.Request(
        f'{api}/beak/duck/sign-key/rotate',
        data=body, method='POST',
        headers={'Content-Type': 'application/json',
                 'X-Beak-Key': beak_key})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except Exception:
            return e.code, {'error': f'http_{e.code}'}
    except Exception as e:
        return 0, {'error': f'transport: {e}'}


def cmd_rotate(args):
    """Autonomous box-lane rotate — 0.6.1 (marker [BEAK-V3-P2D]).

    Flow:
      1. Require: cryptography installed AND an existing on-disk sign key
         (the OLD private key that will sign the attestation).
      2. Generate a fresh Ed25519 keypair (the NEW key).
      3. Build a 10-field v3 canonical attestation envelope:
           intent='key_rotation', from_spaceduck_id=<own sdid>,
           message_hash=sha256(new_kid_hex_string), sender_key_id=<OLD kid>,
           timestamp=now, all other fields empty/default.
         Sign it with the OLD private key (sign_v3).
      4. POST to /beak/duck/sign-key/rotate (X-Beak-Key auth). On 200 the
         server has installed the new pubkey + set a 24 h owner-revert.
      5. ONLY after the server 200 do we atomically replace sign_key.hex
         with the new privkey (temp+os.replace, chmod 0600) and update
         config.sign_key_id. Any earlier failure leaves the local key file
         untouched — the OLD key stays live (and the server too, since the
         rotate never landed).

    Own-sdid resolution:
      - Config `spaceduck_id` (same key `pair.py` writes, same key
        `send_peck.py` reads) — see references above.
      - Optional CLI override: `--spaceduck-id`. Refuses to run without one.
    """
    cfg = _load_config()
    api = _api_base(cfg)
    beak_key = cfg.get('beak_key', '')
    sdid = (getattr(args, 'spaceduck_id', None) or cfg.get('spaceduck_id') or '').strip()
    if not beak_key:
        print('ERROR: config.json missing beak_key — repair pairing first.')
        return 1
    if not sdid:
        print('ERROR: no spaceduck_id in config.json — pass --spaceduck-id or re-pair.')
        return 1

    _ensure_cryptography()
    old_priv_hex, old_pub_hex, old_kid = load_sign_key()
    if not old_priv_hex:
        print(f'ERROR: no local sign key at {SIGN_KEY_PATH}.')
        print('       rotate requires the OLD key to sign the attestation.')
        print('       run `sign_key.py setup` first, or use Mission Control')
        print('       break-glass recovery if the OLD key is truly lost.')
        return 1

    # Generate the new keypair. We do NOT write it to disk yet — the write
    # is deferred until the server rotate confirms 200.
    new_priv_hex, new_pub_hex = _generate_keypair()
    new_kid = derive_key_id(new_pub_hex)
    print(f'🔑 Rotating sign key on {sdid}: old={old_kid} → new={new_kid}')

    # Build the attestation envelope. Message-hash is sha256 of the NEW
    # sender_key_id STRING (server: `hashlib.sha256(new_kid.encode()).hexdigest()`).
    now_ts = int(time.time())
    att_env = {
        'from_spaceduck_id': sdid,
        'to_spaceduck_id':   '',
        'conversation_id':   '',
        'turn_index':        0,
        'intent':            'key_rotation',
        'scopes_asserted':   [],
        'timestamp':         now_ts,
        'message_hash':      hashlib.sha256(new_kid.encode()).hexdigest(),
        'sender_key_id':     old_kid,
        'protocol_caps':     ['v3'],
    }
    try:
        att_sig = sign_v3(att_env, old_priv_hex)
    except Exception as _se:
        print(f'ERROR: attestation signing failed: {_se}')
        print(f'   local key file at {SIGN_KEY_PATH} untouched.')
        return 1

    print(f'📡 POST /beak/duck/sign-key/rotate (attestation signed by {old_kid})...')
    status, resp = _post_box_rotate(api, beak_key, new_pub_hex, att_env, att_sig)
    if status == 200:
        # Server accepted. Atomically install the new privkey; only THEN
        # update config so a partial failure never leaves config pointing
        # at a kid the on-disk key can't back.
        try:
            _write_sign_key(new_priv_hex)
        except Exception as _we:
            print(f'❌ CRITICAL: server rotated to {new_kid} but local key write failed: {_we}')
            print(f'   OLD key still at {SIGN_KEY_PATH}; use Mission Control revert within 24 h.')
            return 1
        cfg['sign_key_id'] = resp.get('sign_key_id') or new_kid
        cfg['envelope_v3'] = True
        _save_config(cfg)
        revert_until = int(resp.get('sign_revert_until', 0) or 0)
        overlap_until = int(resp.get('sign_prev_valid_until', 0) or 0)
        print(f'✅ Rotated: old={resp.get("sign_key_id_prev", old_kid)} → new={cfg["sign_key_id"]}')
        print(f'   Local private key updated at {SIGN_KEY_PATH} (0600).')
        if overlap_until:
            _ols = max(0, overlap_until - int(time.time()))
            print(f'   Verify-overlap: old pubkey stays valid ~{_ols}s (until {overlap_until}).')
        if revert_until:
            _rems = max(0, revert_until - int(time.time()))
            print(f'   Owner-revert window: {_rems // 3600}h remaining (until {revert_until}).')
            print(f'   To undo (owner-only): Mission Control → this duck → Revert last')
            print(f'   sign-key rotate, or POST /beak/duck/{sdid}/sign-key/rotate/revert.')
        return 0
    if status == 409 and (resp.get('error') == 'rotate_pending_window'):
        print('⚠️  Rotate blocked — a prior rotate on this duck is still owner-revocable.')
        _ru = int(resp.get('sign_revert_until', 0) or 0)
        if _ru:
            _rems = max(0, _ru - int(time.time()))
            print(f'   Revert window closes in {_rems // 3600}h {(_rems % 3600) // 60}m (unix {_ru}).')
        print('   Options: (a) owner reverts in Mission Control, then retry rotate;')
        print('            (b) wait for the window to expire, then retry rotate.')
        print(f'   Local key file at {SIGN_KEY_PATH} untouched — OLD key still active.')
        return 5
    if status == 401:
        print(f'❌ Backend refused (401): {resp.get("error", "auth")}')
        print(f'   Local key file at {SIGN_KEY_PATH} untouched.')
        return 4
    if status == 403:
        print(f'❌ Backend refused (403): {resp.get("error", "forbidden")}')
        _h = resp.get('hint', '')
        if _h:
            print(f'   hint: {_h}')
        print(f'   Local key file at {SIGN_KEY_PATH} untouched.')
        return 4
    if status == 404:
        print(f'❌ Rotate refused (404): {resp.get("error", "not_found")}')
        print(f'   Hint: {resp.get("hint","")}')
        print(f'   Local key file at {SIGN_KEY_PATH} untouched.')
        return 6
    if status == 410:
        print(f'❌ Duck revoked (410): {resp.get("error", "revoked")}')
        print(f'   Local key file at {SIGN_KEY_PATH} untouched.')
        return 7
    print(f'❌ Rotate failed: HTTP {status} — {json.dumps(resp)[:220]}')
    print(f'   Local key file at {SIGN_KEY_PATH} untouched.')
    return 1


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Manage the local Ed25519 signing key (envelope v3).')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p_setup = sub.add_parser('setup', help='Generate + register the sign key (idempotent).')
    p_setup.add_argument('--force', action='store_true',
                         help='Force-generate a fresh keypair even if one exists on disk. '
                              'Only useful when the server has NO key yet '
                              '(otherwise the bootstrap returns 409 — use rotate).')

    sub.add_parser('status', help='Show local + registered sign-key state.')
    p_rotate = sub.add_parser('rotate',
        help='Rotate the sign key autonomously — generate a new Ed25519 pair, '
             'attest with the OLD key, POST /beak/duck/sign-key/rotate, then '
             'atomically replace the local privkey. Owner has 24 h to revert.')
    p_rotate.add_argument('--spaceduck-id', dest='spaceduck_id', default=None,
        help='Override the config.spaceduck_id (rarely needed — normally read from config.json).')

    args = parser.parse_args()
    if args.cmd == 'setup':
        sys.exit(cmd_setup(args))
    if args.cmd == 'status':
        sys.exit(cmd_status(args))
    if args.cmd == 'rotate':
        sys.exit(cmd_rotate(args))
    parser.print_help()
    sys.exit(1)
