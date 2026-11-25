#!/usr/bin/env python3
"""space-duck — responder brain fallback chain (0.9.7 [RESP-D]).

When the primary reply brain (the local ``claude`` CLI) cannot run — missing
binary, non-zero exit (e.g. "organisation access to Claude Code is disabled"),
timeout, or empty output — ``peck_responder`` falls back to an ordered list of
OpenAI-compatible chat-completions endpoints so an inbound peck still gets a
reply instead of a silent drop.

Egress is OWNER-CONSENTED ONLY. A fallback brain URL is NEVER read from an
inbound peck — only from ``~/.space-duck/config.json`` or the environment.
Three ordered sources:

  1. explicit   — config ``responder_fallback`` {base_url, model, api_key_env}
                  and/or env SPACEDUCK_RESPONDER_FALLBACK_URL / _MODEL /
                  _KEY_ENV. ``api_key_env`` is the NAME of an env var holding
                  the key; ``api_key_file`` is an alternative path to a 0600
                  key file (same custody pattern as the kimi-relay proxy
                  secret). Owner-set base_url, any host, http(s) only.
  2. kimi-relay — auto-detected when ``~/.kimi-code/credentials/proxy_secret``
                  exists: the sibling space-duck-kimi-relay localhost proxy at
                  http://127.0.0.1:<port>/v1 (default 8471; override via
                  SPACEDUCK_RESPONDER_KIMI_PORT or config
                  ``responder_kimi_relay_port``). LOOPBACK ONLY.
  3. openai     — when OPENAI_API_KEY is set: https://api.openai.com/v1,
                  model from SPACEDUCK_RESPONDER_FALLBACK_MODEL or the
                  documented default ``gpt-4o-mini``.

stdlib urllib only. No key literal is ever logged or returned in an error
string (errors carry only the HTTP status or the exception class name).
Reasoning / ``<think>`` content is stripped from replies.
"""
import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

HOME = Path.home()
# Sibling skill: space-duck-kimi-relay writes this 0600 bearer secret file when
# its local proxy is set up. Its presence is our auto-detect signal.
KIMI_SECRET = HOME / '.kimi-code' / 'credentials' / 'proxy_secret'

_THINK_RE = re.compile(r'<think>.*?</think>', re.DOTALL | re.IGNORECASE)
_DEFAULT_OPENAI_MODEL = 'gpt-4o-mini'
_DEFAULT_KIMI_MODEL = 'k3'          # kimi membership model (relay probe uses k3)
_LOOPBACK = {'127.0.0.1', 'localhost', '::1'}


def _host(url):
    try:
        return (urlparse(url or '').hostname or '').lower()
    except Exception:
        return ''


def _endpoint(base_url):
    """Normalise an OpenAI-compatible base to the chat-completions URL.
    Convention: base ends at ``/v1`` (matches the kimi-relay serve banner);
    we append ``/chat/completions`` unless it is already present."""
    b = (base_url or '').strip().rstrip('/')
    if b.endswith('/chat/completions'):
        return b
    return b + '/chat/completions'


def _read_key_file(path):
    try:
        return Path(os.path.expanduser(str(path))).read_text().strip()
    except Exception:
        return ''


def resolve_fallbacks(cfg):
    """Return the ordered list of usable fallback specs. Never raises.

    Each spec: ``{name, url, model, key}``. Secrets are resolved here (from the
    env-var NAME or a key file) but must never be logged by callers.
    """
    cfg = cfg or {}
    specs = []

    # 1. explicit owner config / env ────────────────────────────────────────
    rf = cfg.get('responder_fallback')
    rf = rf if isinstance(rf, dict) else {}
    base = (os.environ.get('SPACEDUCK_RESPONDER_FALLBACK_URL')
            or rf.get('base_url') or '').strip()
    if base and (base.startswith('http://') or base.startswith('https://')) \
            and _host(base):
        model = (os.environ.get('SPACEDUCK_RESPONDER_FALLBACK_MODEL')
                 or rf.get('model') or _DEFAULT_OPENAI_MODEL)
        key = ''
        key_env = (os.environ.get('SPACEDUCK_RESPONDER_FALLBACK_KEY_ENV')
                   or rf.get('api_key_env') or '')
        if key_env:
            key = os.environ.get(key_env, '')
        if not key and rf.get('api_key_file'):
            key = _read_key_file(rf['api_key_file'])
        specs.append({'name': 'config', 'url': _endpoint(base),
                      'model': model, 'key': key})

    # 2. kimi-relay auto-detect (loopback only) ─────────────────────────────
    if KIMI_SECRET.exists():
        secret = _read_key_file(str(KIMI_SECRET))
        raw_port = (os.environ.get('SPACEDUCK_RESPONDER_KIMI_PORT')
                    or str(cfg.get('responder_kimi_relay_port') or 8471))
        try:
            port = str(int(str(raw_port).strip()))
        except Exception:
            port = '8471'
        url = _endpoint(f'http://127.0.0.1:{port}/v1')
        if _host(url) in _LOOPBACK:
            model = (os.environ.get('SPACEDUCK_RESPONDER_KIMI_MODEL')
                     or cfg.get('responder_kimi_relay_model') or _DEFAULT_KIMI_MODEL)
            specs.append({'name': 'kimi-relay', 'url': url,
                          'model': model, 'key': secret})

    # 3. openai (pay-per-token) ─────────────────────────────────────────────
    okey = os.environ.get('OPENAI_API_KEY', '')
    if okey:
        model = (os.environ.get('SPACEDUCK_RESPONDER_FALLBACK_MODEL')
                 or _DEFAULT_OPENAI_MODEL)
        specs.append({'name': 'openai',
                      'url': _endpoint('https://api.openai.com/v1'),
                      'model': model, 'key': okey})
    return specs


def _egress_ok(spec):
    """Per-source host allowlist. ``config`` is owner-consented (any http(s)
    host); ``kimi-relay`` must be loopback; ``openai`` must be the official
    API host. Fail-closed on anything else."""
    name = spec.get('name')
    url = spec.get('url') or ''
    if name == 'config':
        return url.startswith('http://') or url.startswith('https://')
    if name == 'kimi-relay':
        return _host(url) in _LOOPBACK
    if name == 'openai':
        return _host(url) == 'api.openai.com'
    return False


def _extract_content(data):
    """Pull assistant text from an OpenAI-compatible chat.completion, ignoring
    any separate reasoning field and stripping inline ``<think>`` blocks."""
    try:
        choices = data.get('choices') or []
        if not choices:
            return ''
        msg = choices[0].get('message') or {}
        content = msg.get('content') or ''
        if isinstance(content, list):   # content-parts shape
            content = ''.join(
                p.get('text', '') if isinstance(p, dict) else str(p)
                for p in content)
        return _THINK_RE.sub('', content or '').strip()
    except Exception:
        return ''


def call(spec, sys_framing, prompt, timeout=90):
    """Invoke one fallback brain. Returns ``(text, '')`` on success or
    ``('', err)`` on failure. ``err`` never contains the API key — only an
    HTTP status token or the exception class name."""
    if not _egress_ok(spec):
        return '', 'egress-blocked'
    body = json.dumps({
        'model': spec.get('model'),
        'messages': [
            {'role': 'system', 'content': sys_framing},
            {'role': 'user', 'content': prompt},
        ],
        'stream': False,
    }).encode()
    # No custom User-Agent: openrouter.ai's Cloudflare tier 403-blocks
    # requests whose UA contains the skill name (proven 2026-09-26), while
    # urllib's default passes. Let urllib send its own UA.
    headers = {'Content-Type': 'application/json'}
    if spec.get('key'):
        headers['Authorization'] = 'Bearer ' + spec['key']
    req = urllib.request.Request(spec['url'], data=body, headers=headers,
                                 method='POST')
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read() or b'{}')
    except urllib.error.HTTPError as e:
        return '', f'http_{e.code}'
    except Exception as e:
        return '', f'transport:{type(e).__name__}'
    text = _extract_content(data)
    if not text.strip():
        return '', 'empty'
    return text, ''


if __name__ == '__main__':
    # Offline self-check: source resolution precedence + egress guard, no
    # network. (Full behavioural coverage lives in coordination/rig_skill_096.py.)
    import tempfile
    os.environ.pop('OPENAI_API_KEY', None)
    os.environ['SPACEDUCK_RESPONDER_FALLBACK_URL'] = 'https://proxy.example/v1'
    os.environ['SPACEDUCK_RESPONDER_FALLBACK_KEY_ENV'] = 'MY_KEY'
    os.environ['MY_KEY'] = 'sekret-value'
    s = resolve_fallbacks({})
    assert s and s[0]['name'] == 'config', s
    assert s[0]['url'] == 'https://proxy.example/v1/chat/completions', s[0]
    assert s[0]['key'] == 'sekret-value', 'key from env-var NAME'
    assert _egress_ok(s[0])
    assert not _egress_ok({'name': 'kimi-relay', 'url': 'http://1.2.3.4/v1/chat/completions'})
    assert _egress_ok({'name': 'kimi-relay', 'url': 'http://127.0.0.1:8471/v1/chat/completions'})
    assert _egress_ok({'name': 'openai', 'url': 'https://api.openai.com/v1/chat/completions'})
    assert not _egress_ok({'name': 'openai', 'url': 'https://evil.example/v1/chat/completions'})
    assert _extract_content({'choices': [{'message': {'content': '<think>x</think>hi'}}]}) == 'hi'
    print('OK _brain_fallback self-check')
