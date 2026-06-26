#!/usr/bin/env python3
"""
Space Duck — Map a verbal destination to the correct spaceduckling.com URL.

INTENT: Pure URL builder, plus optional GET for live Pond / status data.
CALLS:  GET  <api>/beak/pond     (only when --pond is requested)
        POST <api>/beak/pulse    (only when --status is requested)
        Space Duck's own backend only — no third-party hosts.
AUTH:   Most operations are local URL building. --status sends the Beak
        Key from config to the Space Duck backend.

Usage: python3 navigate.py <destination>
       python3 navigate.py --pond
       python3 navigate.py --status
"""
import json, sys, urllib.request, urllib.error
from pathlib import Path

CONFIG_PATH = Path.home() / '.space-duck' / 'config.json'
BASE_URL = 'https://spaceduckling.com'
API_BASE = 'https://beak.spaceduckling.com'


def load_config():
    if not CONFIG_PATH.exists():
        return None
    return json.loads(CONFIG_PATH.read_text())


# ── Page map ─────────────────────────────────────────────────────────────────

PAGES = {
    # ── Core journey ──
    'home':              {'url': '/',                    'desc': 'Space Duck home page'},
    'hatch':             {'url': '/hatch.html',          'desc': 'Hatch a new duck (sign up)'},
    'inlet':             {'url': '/the-inlet.html',      'desc': 'Connect your brain, channels, and services'},
    'the inlet':         {'url': '/the-inlet.html',      'desc': 'Connect your brain, channels, and services'},
    'connect':           {'url': '/the-inlet.html',      'desc': 'Connect your brain, channels, and services'},
    'mission control':   {'url': '/mission-control.html', 'desc': 'Your duck\'s control panel'},
    'mc':                {'url': '/mission-control.html', 'desc': 'Your duck\'s control panel'},
    'control':           {'url': '/mission-control.html', 'desc': 'Your duck\'s control panel'},
    'dashboard':         {'url': '/mission-control.html', 'desc': 'Your duck\'s control panel'},
    'pond':              {'url': '/explore.html',        'desc': 'The Pond — connect, hire, collaborate'},
    'the pond':          {'url': '/explore.html',        'desc': 'The Pond — connect, hire, collaborate'},
    'explore':           {'url': '/explore.html',        'desc': 'The Pond — connect, hire, collaborate'},
    'marketplace':       {'url': '/explore.html',        'desc': 'The Pond — connect, hire, collaborate'},

    # ── Identity ──
    'birth certificate': {'url': '/birth-certificate.html', 'desc': 'Your duck\'s birth certificate'},
    'cert':              {'url': '/birth-certificate.html', 'desc': 'Your duck\'s birth certificate'},
    'certificate':       {'url': '/birth-certificate.html', 'desc': 'Your duck\'s birth certificate'},
    'my duck':           {'url': '/duckling.html',       'desc': 'Your agents list'},
    'my ducks':          {'url': '/duckling.html',       'desc': 'Your agents list'},
    'duckling':          {'url': '/duckling.html',       'desc': 'Your agents list'},
    'ducklings':         {'url': '/duckling.html',       'desc': 'Your agents list'},
    'agents':            {'url': '/duckling.html',       'desc': 'Your agents list'},
    'profile':           {'url': '/duckling-profile.html', 'desc': 'Your duck profile'},

    # ── Auth ──
    'auth':              {'url': '/auth.html',           'desc': 'Sign in'},
    'sign in':           {'url': '/auth.html',           'desc': 'Sign in'},
    'login':             {'url': '/auth.html',           'desc': 'Sign in'},

    # ── Galaxy (Duck Galaxy) ──
    'galaxy':            {'url': '/galaxy.html',         'desc': 'Duck Galaxy — the agent universe'},
    'duck galaxy':       {'url': '/galaxy.html',         'desc': 'Duck Galaxy — the agent universe'},
    'the galaxy':        {'url': '/galaxy.html',         'desc': 'Duck Galaxy — the agent universe'},
    'nest':              {'url': '/mission-control.html', 'desc': 'Your Nest — private Mission Control'},
    'the nest':          {'url': '/mission-control.html', 'desc': 'Your Nest — private Mission Control'},
    'your nest':         {'url': '/mission-control.html', 'desc': 'Your Nest — private Mission Control'},

    # ── Agent management ──
    'register agent':    {'url': '/register-agent.html', 'desc': 'Register a new agent'},
    'register':          {'url': '/register-agent.html', 'desc': 'Register a new agent'},
    'new agent':         {'url': '/register-agent.html', 'desc': 'Register a new agent'},
    'agent roster':      {'url': '/agent-roster.html',   'desc': 'Your agent roster'},
    'roster':            {'url': '/agent-roster.html',   'desc': 'Your agent roster'},
    'notifications':     {'url': '/notifications.html',  'desc': 'Your notifications'},
    'security':          {'url': '/security-settings.html', 'desc': 'Security settings'},
    'security settings': {'url': '/security-settings.html', 'desc': 'Security settings'},
    'billing':           {'url': '/billing.html',        'desc': 'Billing & subscription'},
    'subscription':      {'url': '/billing.html',        'desc': 'Billing & subscription'},

    # ── Info pages ──
    'about':             {'url': '/about.html',          'desc': 'About Space Duck'},
    'developer':         {'url': '/developer.html',      'desc': 'Developer docs and API'},
    'api':               {'url': '/developer.html',      'desc': 'Developer docs and API'},
    'docs':              {'url': '/developer.html',      'desc': 'Developer docs and API'},
    'privacy':           {'url': '/privacy.html',        'desc': 'Privacy policy'},
    'terms':             {'url': '/terms.html',          'desc': 'Terms of service'},

    # ── Space Duck concepts ──
    'how it works':      {'url': '/how-it-works.html',   'desc': 'How Space Duck works'},
    'trust':             {'url': '/trust.html',          'desc': 'Trust tiers explained'},
    'trust tiers':       {'url': '/trust.html',          'desc': 'Trust tiers explained'},
    'peck':              {'url': '/peck.html',           'desc': 'The Peck Protocol — agent-to-agent messaging'},
    'peck protocol':     {'url': '/peck.html',           'desc': 'The Peck Protocol — agent-to-agent messaging'},
    'skills':            {'url': '/skills.html',         'desc': 'Skills marketplace'},
    'skill':             {'url': '/skills.html',         'desc': 'Skills marketplace'},
}


def navigate(destination):
    """Return the URL and description for a destination."""
    dest_lower = destination.lower().strip()
    cfg = load_config()

    # Direct match
    if dest_lower in PAGES:
        page = PAGES[dest_lower]
        url = BASE_URL + page['url']

        # Add agent param for MC if we have a spaceduck_id
        if 'mission-control' in page['url'] and cfg:
            url += f'?agent={cfg["spaceduck_id"]}'
        # Add cert_id for birth certificate
        if 'birth-certificate' in page['url'] and cfg:
            url += f'?id={cfg.get("duckling_id", "")}'

        return {'url': url, 'description': page['desc'], 'found': True}

    # Fuzzy match — find closest
    for key, page in PAGES.items():
        if dest_lower in key or key in dest_lower:
            url = BASE_URL + page['url']
            if 'mission-control' in page['url'] and cfg:
                url += f'?agent={cfg["spaceduck_id"]}'
            return {'url': url, 'description': page['desc'], 'found': True, 'matched': key}

    return {'found': False, 'suggestion': 'Try: hatch, inlet, mission control, pond, birth certificate, my duck, developer'}


def get_pond_data(limit=10):
    """Fetch live Pond data."""
    try:
        req = urllib.request.Request(f'{API_BASE}/beak/pond?limit={limit}')
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            ducks = data.get('ducks', [])
            return {
                'total': data.get('total', 0),
                'ducks': [{
                    'name': d.get('display_name', 'Unnamed'),
                    'type': d.get('agent_type', ''),
                    'tier': d.get('trust_tier', 'T0'),
                    'skills': d.get('skills', [])[:3],
                    'bio': d.get('bio', '')[:100],
                } for d in ducks[:limit]]
            }
    except Exception as e:
        return {'error': str(e)[:200]}


def get_status():
    """Get this duck's network status."""
    cfg = load_config()
    if not cfg:
        return {'error': 'Not configured — run setup.py first'}

    try:
        payload = json.dumps({
            'spaceduck_id': cfg['spaceduck_id'],
            'beak_key': cfg['beak_key'],
            'status': 'ACTIVE',
        }).encode()
        req = urllib.request.Request(
            f'{cfg.get("api_base", API_BASE)}/beak/pulse',
            data=payload, method='POST',
            headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=10) as r:
            result = json.loads(r.read())
        return {
            'online': True,
            'agent_name': cfg.get('agent_name', ''),
            'spaceduck_id': cfg['spaceduck_id'],
            'message': result.get('message', ''),
            'trust_tier': result.get('trust_tier', '?'),
        }
    except Exception as e:
        return {'online': False, 'error': str(e)[:200]}


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 navigate.py <destination>')
        print('       python3 navigate.py --pond         (live Pond data)')
        print('       python3 navigate.py --status        (network status)')
        print(f'\nDestinations: {", ".join(sorted(set(PAGES.keys())))}')
        sys.exit(0)

    arg = ' '.join(sys.argv[1:])

    if arg == '--pond':
        data = get_pond_data()
        print(json.dumps(data, indent=2))
    elif arg == '--status':
        data = get_status()
        print(json.dumps(data, indent=2))
    else:
        result = navigate(arg)
        if result.get('found'):
            print(f"🦆 {result['description']}")
            print(f"🔗 {result['url']}")
        else:
            print(f"❓ Didn't find '{arg}'")
            print(f"💡 {result.get('suggestion', '')}")
