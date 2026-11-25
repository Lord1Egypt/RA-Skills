#!/usr/bin/env python3
"""
Space Duck — Configure this agent's identity and register as a peck listener.

INTENT: Save the user's Beak Key + duck IDs to ~/.space-duck/config.json,
        validate the key against the Space Duck backend, and (optionally)
        register a webhook URL so the agent can receive incoming pecks.
CALLS:  POST <api>/beak/agent/message  (validate the key by self-pinging)
        POST <api>/beak/pulse          (register the webhook)
        Space Duck's own backend only — no third-party hosts.
AUTH:   The Beak Key is what the user pastes in. It is written to
        ~/.space-duck/config.json with mode 0600 and used to identify
        this agent on the Space Duck network.

        Install-key rotation: if the pasted key is a one-time install
        key (`bk_OTP_…`), the backend swaps it for a long-lived
        `bk_LIVE_…` on first validate and returns the new key in
        `rotated_to`. setup() persists `rotated_to` (not the OTP) so
        the agent stays connected after the 10-minute OTP expiry.

Usage: python3 setup.py --beak-key bk_XXXX --spaceduck-id XXXXXXXX --duckling-id XXXXXXXX
       python3 setup.py --show
       python3 setup.py --validate   (test if Beak Key is valid)
"""
import hashlib, json, argparse, secrets, sys, time, urllib.request, urllib.error
from pathlib import Path

# Canonical envelope helper — same sibling module send_peck.py / chat.py sign
# with. setup.py may be invoked by absolute path (installers do), so the CWD is
# not the scripts dir; extend sys.path the same way send_peck.py does.
import pathlib as _pl
_script_dir = str(_pl.Path(__file__).resolve().parent)
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)
from _envelope import sign_v2 as _v2_sign

CONFIG_DIR = Path.home() / '.space-duck'
CONFIG_PATH = CONFIG_DIR / 'config.json'
API_BASE = 'https://beak.spaceduckling.com'


def validate_beak_key(beak_key, spaceduck_id, cfg=None):
    """Validate the Beak Key by sending a v2-SIGNED identity peck to self.

    The server (lambda_function.py, POST /beak/agent/message) rejects every
    unsigned peck with 403 "Unsigned peck rejected…", and 410s envelope v1
    outright (ENVELOPE_V1_SUNSET passed 2026-06-05). An unsigned/versionless
    probe therefore fails for perfectly good pairings, so this builds the same
    envelope v2 the real send paths build:

      canonical = json(sorted 8 fields, compact separators) via _envelope.canonical_v2
      signature = HMAC-SHA256(beak_key, canonical).hexdigest()  via _envelope.sign_v2

    Server counterparts: `_envelope_v2_canonical` / `_envelope_v2_sign` /
    `_envelope_v2_verify` (lambda_function.py:4728-4753) and the v2 verify
    branch that rebuilds the envelope from the request body. `message_hash` is
    recomputed server-side from the top-level `message`, so `message` must be a
    top-level field (the old code only sent `payload.message` — hashing '').

    Ordering that makes this a truthful test: the server compares the stored
    beak_key BEFORE checking the signature, so a WRONG key still yields
    403 {"error": "Invalid Beak Key"}. The bk_OTP_ swap-on-validate branch also
    runs before signature verification, so install-key rotation is unaffected.
    """
    message = 'key validation check'
    message_hash = hashlib.sha256(message.encode()).hexdigest()
    peck_id = 'peck_' + secrets.token_urlsafe(12)
    timestamp = int(time.time())
    # Self-peck, fresh conversation: conversation_id = peck_id, turn 0, no scopes.
    env_v2 = {
        'from_spaceduck_id': spaceduck_id,
        'to_spaceduck_id':   spaceduck_id,
        'conversation_id':   peck_id,
        'turn_index':        0,
        'intent':            'identity',
        'scopes_asserted':   [],
        'timestamp':         timestamp,
        'message_hash':      message_hash,
    }
    body_dict = {
        'envelope_version':    '2',
        'sender_spaceduck_id': spaceduck_id,
        'target_spaceduck_id': spaceduck_id,
        'message':             message,
        'message_hash':        message_hash,
        'peck_type':           'identity',
        'intent':              'identity',
        'peck_id':             peck_id,
        'conversation_id':     peck_id,
        'turn_index':          0,
        'scopes_asserted':     [],
        'timestamp':           timestamp,
        # Kept in the body (not only the X-Beak-Key header) because the
        # bk_OTP_ swap-on-validate branch reads body.beak_key first.
        'beak_key':            beak_key,
        'signature':           _v2_sign(env_v2, beak_key),
    }
    # v3-preferred, mirroring send_peck.py: ducks with `v2_sunset_enforced_at`
    # on their spaceducks row 410 every v2 envelope, so a v2-only probe
    # false-fails their perfectly good pairing. If a local Ed25519 sign key
    # exists, sign v3; any hiccup degrades byte-identically to the v2 body.
    if (cfg or {}).get('envelope_v3', True):
        try:
            from _envelope import load_sign_key as _load_sign_key, \
                sign_v3 as _v3_sign, derive_key_id as _v3_derive_kid  # noqa: F401
            _v3_priv, _v3_pub, _v3_kid_local = _load_sign_key()
            if _v3_priv:
                _v3_kid = (cfg or {}).get('sign_key_id') or _v3_kid_local
                _v3_env = dict(env_v2, sender_key_id=_v3_kid, protocol_caps=['v3'])
                body_dict.update({
                    'envelope_version': '3',
                    'sender_key_id':    _v3_kid,
                    'protocol_caps':    ['v3'],
                    'signature':        _v3_sign(_v3_env, _v3_priv),
                })
        except Exception as _v3_err:
            print(f'WARN: v3 envelope build failed ({_v3_err}); validating with v2.',
                  file=sys.stderr)
    payload = json.dumps(body_dict).encode()
    req = urllib.request.Request(
        f'{API_BASE}/beak/agent/message',
        data=payload, method='POST',
        headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            result = json.loads(r.read())
            return True, result
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        try:
            server_err = str(json.loads(body).get('error', '')).strip()
        except Exception:
            server_err = ''
        if e.code == 403:
            marker = (server_err or body).lower()
            # Defense in depth: an unsigned-peck rejection is a SKILL defect,
            # never evidence that the operator's key is wrong. Never launder it
            # into "Invalid Beak Key".
            if 'unsigned peck' in marker:
                return False, {'error': (
                    'Server rejected the validation peck as unsigned — your Beak Key '
                    'was never tested. This is a skill bug, not a bad key. '
                    'Update the skill (scripts/update.sh) and retry.')}
            if 'invalid beak key' in marker or 'invalid peck signature' in marker:
                return False, {'error': 'Invalid Beak Key — check the value and Spaceduck ID'}
            if 'sign_key_not_registered' in marker:
                # Local Ed25519 key exists but the server has no pubkey for
                # this duck (stale key from a previous pairing). Not a bad
                # beak key — the send paths would hit the same wall.
                return False, {'error': (
                    'Local sign key is not registered for this duck — run '
                    'python3 scripts/sign_key.py setup (or remove the stale '
                    '~/.space-duck/sign_key.hex) and retry.')}
            if server_err:
                # A real server verdict about something OTHER than the key
                # (birth certificate, grants, mute, …). Report it verbatim.
                return False, {'error': f'Rejected by server (403): {server_err}'}
            return False, {'error': f'Invalid Beak Key — check the value and Spaceduck ID (server said: {body})'}
        elif e.code == 401:
            return False, {'error': 'No Beak Key provided'}
        elif e.code == 410 and 'sunset' in (server_err or body).lower():
            # Envelope-version sunset (v1 global, or per-duck v2 opt-in) — the
            # key was never tested; the duck just requires a newer envelope.
            return False, {'error': (
                f'Server requires a newer envelope version ({server_err}) — your '
                'Beak Key was never tested. If this duck is v3-enforced, register '
                'a sign key (python3 scripts/sign_key.py setup) and retry.')}
        return False, {'error': f'HTTP {e.code}: {body}'}
    except Exception as e:
        return False, {'error': str(e)}


def pulse(spaceduck_id, beak_key, webhook_url=''):
    """Send a presence pulse so the directory flips this duck to ALIVE.

    /beak/pulse only updates last_seen + health_state — the webhook URL
    field is silently ignored by the backend (registration happens via a
    different code path). Field included for forward-compat only.
    """
    body = {
        'spaceduck_id': spaceduck_id,
        'beak_key': beak_key,
        'status': 'ACTIVE',
    }
    if webhook_url:
        body['openclaw_webhook_url'] = webhook_url
    payload = json.dumps(body).encode()
    req = urllib.request.Request(
        f'{API_BASE}/beak/pulse',
        data=payload, method='POST',
        headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return True, json.loads(r.read())
    except Exception as e:
        return False, {'error': str(e)[:200]}


def setup(beak_key, spaceduck_id, duckling_id, agent_name='Agent', webhook_url=''):
    CONFIG_DIR.mkdir(mode=0o700, parents=True, exist_ok=True)

    # Step 1: Validate the Beak Key
    print(f'🔑 Validating Beak Key...')
    valid, result = validate_beak_key(beak_key, spaceduck_id)
    if not valid:
        print(f'❌ Beak Key validation FAILED: {result.get("error", "unknown")}')
        print(f'   Check your Beak Key and Spaceduck ID, then try again.')
        sys.exit(1)
    print(f'✅ Beak Key valid!')

    # Step 1b: If backend swapped a one-time install key (bk_OTP_) for a
    # long-lived bk_LIVE_, persist the new key — not the expiring OTP.
    rotated_to = result.get('rotated_to') if isinstance(result, dict) else None
    if rotated_to and rotated_to != beak_key:
        print(f'🔄 Install key swapped for long-lived Beak Key — persisting {rotated_to[:12]}…')
        beak_key = rotated_to

    # Step 2: Save config
    config = {
        'beak_key': beak_key,
        'spaceduck_id': spaceduck_id,
        'duckling_id': duckling_id,
        'agent_name': agent_name,
        'api_base': API_BASE,
        'openclaw_webhook_url': webhook_url,
    }
    CONFIG_PATH.write_text(json.dumps(config, indent=2))
    CONFIG_PATH.chmod(0o600)
    print(f'💾 Config saved to {CONFIG_PATH}')

    # Step 3: Pulse so the directory flips this duck to ALIVE.
    # Validation alone proves the key works but doesn't update presence;
    # without this pulse, /ducks.html keeps showing "Connect your duck".
    print(f'💓 Sending presence pulse...')
    ok, pulse_result = pulse(spaceduck_id, beak_key, webhook_url)
    if ok:
        print(f'✅ Pulse sent — duck is ALIVE in the directory.')
    else:
        print(f'⚠️  Pulse failed: {pulse_result.get("error", "")}')
        print(f'   Identity saved locally, but duck won\'t show online until a pulse goes through.')
    if webhook_url:
        print(f'🔗 Webhook on file → {webhook_url}')

    print(f'\n🦆 Setup complete!')
    print(f'   Agent:        {agent_name}')
    print(f'   Spaceduck ID: {spaceduck_id}')
    print(f'   Duckling:     {duckling_id}')
    print(f'   Beak Key:     {beak_key[:10]}…')
    if webhook_url:
        print(f'   Webhook:      {webhook_url}')
    return config


def show():
    if not CONFIG_PATH.exists():
        print('No config found. Run setup.py --beak-key ... first.')
        return
    cfg = json.loads(CONFIG_PATH.read_text())
    print(f'Agent:        {cfg.get("agent_name")}')
    print(f'Spaceduck ID: {cfg.get("spaceduck_id")}')
    print(f'Duckling:     {cfg.get("duckling_id")}')
    print(f'Beak Key:     {cfg.get("beak_key","")[:10]}…')
    wh = cfg.get('openclaw_webhook_url', '')
    print(f'Webhook:      {wh or "(not set)"}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Set up Space Duck agent identity')
    parser.add_argument('--beak-key', required=False)
    parser.add_argument('--spaceduck-id', required=False)
    parser.add_argument('--duckling-id', required=False)
    parser.add_argument('--agent-name', default='Agent')
    parser.add_argument('--webhook-url', default='', help='OpenClaw webhook URL for receiving pecks')
    parser.add_argument('--show', action='store_true')
    parser.add_argument('--validate', action='store_true', help='Validate existing Beak Key')
    args = parser.parse_args()

    if args.show:
        show()
    elif args.validate:
        if not CONFIG_PATH.exists():
            print('No config found. Run setup.py --beak-key ... first.')
            sys.exit(1)
        cfg = json.loads(CONFIG_PATH.read_text())
        valid, result = validate_beak_key(cfg['beak_key'], cfg['spaceduck_id'], cfg=cfg)
        if valid:
            print(f'✅ Beak Key is valid for {cfg.get("agent_name")}')
        else:
            print(f'❌ Beak Key invalid: {result.get("error", "unknown")}')
    elif not args.beak_key or not args.spaceduck_id or not args.duckling_id:
        print('Usage: python3 setup.py --beak-key bk_XXX --spaceduck-id XXXX --duckling-id XXXX [--webhook-url URL]')
        print('       python3 setup.py --show')
        print('       python3 setup.py --validate')
        sys.exit(1)
    else:
        setup(args.beak_key, args.spaceduck_id, args.duckling_id, args.agent_name, args.webhook_url)
