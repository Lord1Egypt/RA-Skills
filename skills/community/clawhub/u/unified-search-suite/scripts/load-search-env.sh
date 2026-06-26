#!/bin/bash
# Source this file to populate search-related env vars from, in order:
# 1) existing process env
# 2) ~/.openclaw/credentials/search.json
# 3) ~/.openclaw/openclaw.json (for existing local Tavily/Exa config)

set -euo pipefail

_eval_exports="$(python3 <<'PY'
import json, os, shlex
from pathlib import Path

out = {}

def set_if_missing(k, v):
    if not v:
        return
    if os.environ.get(k):
        return
    out[k] = str(v)

cred_path = Path.home() / '.openclaw' / 'credentials' / 'search.json'
if cred_path.exists():
    try:
        cred = json.loads(cred_path.read_text())
    except Exception:
        cred = {}
    exa = cred.get('exa')
    if isinstance(exa, dict):
        set_if_missing('EXA_API_KEY', exa.get('apiKey'))
        set_if_missing('EXA_API_BASE', exa.get('apiBase') or exa.get('apiUrl') or exa.get('baseUrl'))
    elif isinstance(exa, str):
        set_if_missing('EXA_API_KEY', exa)
    set_if_missing('EXA_API_BASE', cred.get('exaApiBase') or cred.get('exaApiUrl') or cred.get('exaBaseUrl'))
    set_if_missing('TAVILY_API_KEY', cred.get('tavily'))
    set_if_missing('TAVILY_API_BASE', cred.get('tavilyApiBase') or cred.get('tavilyApiUrl') or cred.get('tavilyBaseUrl'))
    grok = cred.get('grok') or {}
    if isinstance(grok, dict):
        set_if_missing('GROK_API_URL', grok.get('apiUrl'))
        set_if_missing('GROK_API_KEY', grok.get('apiKey'))
        set_if_missing('GROK_MODEL', grok.get('model'))
    tinyfish = cred.get('tinyfish') or {}
    if isinstance(tinyfish, dict):
        set_if_missing('TINYFISH_API_KEY', tinyfish.get('apiKey'))
        set_if_missing('TINYFISH_API_URL', tinyfish.get('apiUrl'))
    mineru = cred.get('mineru') or {}
    if isinstance(mineru, dict):
        set_if_missing('MINERU_TOKEN', mineru.get('token') or mineru.get('apiKey'))
        set_if_missing('MINERU_API_BASE', mineru.get('apiBase') or mineru.get('apiUrl') or mineru.get('baseUrl'))
    github = cred.get('github') or {}
    if isinstance(github, dict):
        set_if_missing('GITHUB_TOKEN', github.get('token'))

cfg_path = Path.home() / '.openclaw' / 'openclaw.json'
if cfg_path.exists():
    try:
        cfg = json.loads(cfg_path.read_text())
    except Exception:
        cfg = {}
    skills = (((cfg.get('skills') or {}).get('entries')) or {})
    tavily = skills.get('tavily') or {}
    exa = skills.get('exa-search') or {}
    set_if_missing('TAVILY_API_KEY', tavily.get('apiKey'))
    set_if_missing('EXA_API_KEY', exa.get('apiKey'))

if not os.environ.get('TAVILY_API_BASE'):
    tavily_key = out.get('TAVILY_API_KEY') or os.environ.get('TAVILY_API_KEY', '')
    if tavily_key.startswith('mysp-'):
        out['TAVILY_API_BASE'] = 'http://127.0.0.1:9874/api'

set_if_missing('OPENCLAW_WORKSPACE', str(Path.home() / 'clawd'))

for k, v in out.items():
    print(f'export {k}={shlex.quote(v)}')
PY
2>/dev/null)"

if [[ -n "${_eval_exports:-}" ]]; then
  eval "$_eval_exports"
fi
unset _eval_exports
