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
import json, argparse, sys, urllib.request, urllib.error
from pathlib import Path

CONFIG_DIR = Path.home() / '.space-duck'
CONFIG_PATH = CONFIG_DIR / 'config.json'
API_BASE = 'https://beak.spaceduckling.com'


def validate_beak_key(beak_key, spaceduck_id):
    """Validate the Beak Key by sending an identity peck to self."""
    payload = json.dumps({
        'sender_spaceduck_id': spaceduck_id,
        'target_spaceduck_id': spaceduck_id,
        'beak_key': beak_key,
        'peck_type': 'identity',
        'payload': {'message': 'key validation check'}
    }).encode()
    req = urllib.request.Request(
        f'{API_BASE}/beak/agent/message',
        data=payload, method='POST',
        headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            result = json.loads(r.read())
            return True, result
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:200]
        if e.code == 403:
            return False, {'error': 'Invalid Beak Key — check the value and Spaceduck ID'}
        elif e.code == 401:
            return False, {'error': 'No Beak Key provided'}
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
        valid, result = validate_beak_key(cfg['beak_key'], cfg['spaceduck_id'])
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
