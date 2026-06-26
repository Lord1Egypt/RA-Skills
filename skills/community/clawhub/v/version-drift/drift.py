#!/usr/bin/env python3
"""
Version Drift — Detect version drift across your infrastructure.

Usage:
    python3 drift.py check                  # table output (default)
    python3 drift.py check --json           # JSON output
    python3 drift.py check --markdown       # markdown table
    python3 drift.py check --only my-server # check one host only
    python3 drift.py check --config /path/to/config.yaml
"""

import json
import os
import re
import shlex
import ssl
import subprocess
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, urlencode
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

# ---------------------------------------------------------------------------
# Optional: pyyaml — falls back to JSON config if unavailable
# ---------------------------------------------------------------------------
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

SCRIPT_DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _ssl_ctx(verify=True):
    """Return an SSL context. Defaults to verified; pass verify=False for self-signed certs."""
    if verify:
        return ssl.create_default_context()
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def expand_env(value):
    """Recursively expand ${VAR} references in strings, dicts, and lists."""
    if isinstance(value, str):
        def _replace(m):
            return os.environ.get(m.group(1), m.group(0))
        return re.sub(r'\$\{([^}]+)\}', _replace, value)
    if isinstance(value, dict):
        return {k: expand_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [expand_env(v) for v in value]
    return value


def json_path_extract(data, path):
    """Extract a value from nested dicts using dot-notation (e.g. 'data.info.version')."""
    for key in path.split('.'):
        if isinstance(data, dict):
            data = data.get(key)
        elif isinstance(data, list) and key.isdigit():
            data = data[int(key)]
        else:
            return None
    return data


def http_get_json(url, headers=None, timeout=15, verify_ssl=True):
    """GET a URL and return parsed JSON."""
    req = Request(url)
    req.add_header('User-Agent', 'version-drift/1.0')
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    with urlopen(req, timeout=timeout, context=_ssl_ctx(verify=verify_ssl)) as resp:
        return json.loads(resp.read().decode())


def http_request(url, headers=None, timeout=15, verify_ssl=True, method='GET'):
    """HTTP request returning (status, headers, body bytes)."""
    req = Request(url, method=method)
    req.add_header('User-Agent', 'version-drift/1.3')
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    with urlopen(req, timeout=timeout, context=_ssl_ctx(verify=verify_ssl)) as resp:
        return resp.status, resp.headers, resp.read()


def run_local(cmd, timeout=30):
    """Run a shell command locally, return stdout stripped."""
    r = subprocess.run(
        ['sh', '-c', cmd], capture_output=True, text=True, timeout=timeout,
    )
    return r.stdout.strip()


def run_ssh(host, user, cmd, ssh_key=None, timeout=30, strict_host_key='accept-new'):
    """Run a command over SSH, return stdout stripped."""
    ssh_cmd = ['ssh', '-o', f'StrictHostKeyChecking={strict_host_key}', '-o', 'ConnectTimeout=10']
    if ssh_key:
        ssh_cmd += ['-i', os.path.expanduser(ssh_key)]
    ssh_cmd += [f'{user}@{host}', cmd]
    r = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=timeout)
    return r.stdout.strip()


def strip_v(version):
    """Strip leading 'v' or 'V' from version strings."""
    if version and version.lower().startswith('v'):
        return version[1:]
    return version


def is_prerelease(version):
    return bool(re.search(r'(?:^|[.\-+])(?:alpha|a|beta|b|rc|pre|preview|canary|nightly|dev)\d*', (version or '').lower()))

# ---------------------------------------------------------------------------
# Installed version fetchers
# ---------------------------------------------------------------------------

def get_installed_version(host_cfg, check_cfg):
    """Return the installed version string for a check."""
    host_type = host_cfg.get('type', 'local')
    installed = check_cfg.get('installed', '')

    # HTTP host with json_path
    if host_type == 'http':
        if isinstance(installed, dict) and 'json_path' in installed:
            url = host_cfg.get('url', '')
            headers = host_cfg.get('headers', {})
            verify = host_cfg.get('verify_ssl', True)
            data = http_get_json(url, headers, verify_ssl=verify)
            return str(json_path_extract(data, installed['json_path']) or '')
        # string command not meaningful for http hosts
        return ''

    # SSH host
    if host_type == 'ssh':
        return run_ssh(
            host_cfg['host'], host_cfg.get('user', 'root'),
            installed, ssh_key=host_cfg.get('ssh_key'),
            strict_host_key=host_cfg.get('strict_host_key', 'accept-new'),
        )

    # Local
    return run_local(installed)

# ---------------------------------------------------------------------------
# Latest version fetchers
# ---------------------------------------------------------------------------

def _github_headers():
    headers = {'Accept': 'application/vnd.github+json'}
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f'Bearer {token}'
    return headers


def get_latest_github(repo):
    url = f'https://api.github.com/repos/{repo}/releases/latest'
    data = http_get_json(url, headers=_github_headers())
    return strip_v(data.get('tag_name', ''))


def get_latest_gitlab(project, base_url='https://gitlab.com', token=None):
    """Latest GitLab release tag for a project path like group/name."""
    headers = {}
    if token:
        headers['PRIVATE-TOKEN'] = token
    url = f"{base_url.rstrip('/')}/api/v4/projects/{quote(project, safe='')}/releases?per_page=1&order_by=released_at&sort=desc"
    data = http_get_json(url, headers=headers)
    if isinstance(data, list) and data:
        return strip_v(data[0].get('tag_name', ''))
    return ''


def get_latest_gitea(repo, base_url, token=None):
    """Latest Gitea/Forgejo release tag for owner/name."""
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
    owner_repo = repo.strip('/').split('/', 1)
    if len(owner_repo) != 2:
        return ''
    owner, name = owner_repo
    url = f"{base_url.rstrip('/')}/api/v1/repos/{quote(owner)}/{quote(name)}/releases/latest"
    data = http_get_json(url, headers=headers)
    return strip_v(data.get('tag_name', ''))


def get_latest_npm(package):
    url = f'https://registry.npmjs.org/{package}/latest'
    data = http_get_json(url)
    return data.get('version', '')


def get_latest_pypi(package):
    url = f'https://pypi.org/pypi/{package}/json'
    data = http_get_json(url)
    return (data.get('info') or {}).get('version', '')


def get_latest_docker(repo, tag_regex=None, include_prerelease=False, pages=3):
    """Latest Docker Hub tag, preferring highest stable semver over last-pushed noise."""
    candidates = []
    pattern = re.compile(tag_regex) if tag_regex else None
    for page in range(1, max(1, int(pages)) + 1):
        url = f'https://hub.docker.com/v2/repositories/{repo}/tags?ordering=last_updated&page_size=100&page={page}'
        data = http_get_json(url)
        for tag in (data.get('results') or []):
            name = tag.get('name', '')
            if not name or name == 'latest':
                continue
            if pattern and not pattern.search(name):
                continue
            if not include_prerelease and is_prerelease(name):
                continue
            if parse_version_tuple(name) == (0,):
                continue
            candidates.append(name)
        if not data.get('next'):
            break
    if not candidates:
        return ''
    return sorted(candidates, key=version_sort_key, reverse=True)[0]


def _parse_www_authenticate(value):
    """Parse a Docker registry Bearer challenge header into a dict."""
    if not value or not value.lower().startswith('bearer '):
        return {}
    parts = {}
    for item in re.finditer(r'(\w+)="([^"]*)"', value[len('Bearer '):]):
        parts[item.group(1)] = item.group(2)
    return parts


def _normalise_oci_image(image, tag='latest'):
    """Return (registry, repository, reference) for Docker/OCI image refs."""
    ref = image
    if '@' in ref:
        ref, tag = ref.split('@', 1)
    elif ':' in ref.rsplit('/', 1)[-1]:
        ref, tag = ref.rsplit(':', 1)

    parts = ref.split('/')
    if len(parts) == 1:
        registry = 'registry-1.docker.io'
        repository = f'library/{parts[0]}'
    elif '.' in parts[0] or ':' in parts[0] or parts[0] == 'localhost':
        registry = parts[0]
        repository = '/'.join(parts[1:])
    else:
        registry = 'registry-1.docker.io'
        repository = ref
    return registry, repository, tag


def get_latest_oci(cfg):
    """Return the current digest for an OCI/Docker image tag from any v2 registry."""
    image = cfg.get('image') or cfg.get('repo')
    tag = cfg.get('tag', 'latest')
    verify = cfg.get('verify_ssl', True)
    if not image:
        return ''
    registry, repository, reference = _normalise_oci_image(image, tag)
    url = f'https://{registry}/v2/{repository}/manifests/{reference}'
    accept = ', '.join([
        'application/vnd.oci.image.index.v1+json',
        'application/vnd.oci.image.manifest.v1+json',
        'application/vnd.docker.distribution.manifest.list.v2+json',
        'application/vnd.docker.distribution.manifest.v2+json',
    ])
    headers = {'Accept': accept}
    username = cfg.get('username') or os.environ.get(cfg.get('username_env', ''))
    password = cfg.get('password') or os.environ.get(cfg.get('password_env', ''))
    if username and password:
        import base64
        token = base64.b64encode(f'{username}:{password}'.encode()).decode()
        headers['Authorization'] = f'Basic {token}'

    try:
        _, resp_headers, _ = http_request(url, headers=headers, method='HEAD', verify_ssl=verify)
    except HTTPError as e:
        if e.code != 401:
            raise
        challenge = _parse_www_authenticate(e.headers.get('WWW-Authenticate'))
        if not challenge:
            raise
        params = {'service': challenge.get('service'), 'scope': challenge.get('scope')}
        token_url = challenge['realm'] + '?' + urlencode({k: v for k, v in params.items() if v})
        token_data = http_get_json(token_url, verify_ssl=verify)
        headers['Authorization'] = f"Bearer {token_data.get('token') or token_data.get('access_token')}"
        _, resp_headers, _ = http_request(url, headers=headers, method='HEAD', verify_ssl=verify)

    digest = resp_headers.get('Docker-Content-Digest', '')
    if cfg.get('return', 'digest') == 'tag@digest':
        return f'{reference}@{digest}' if digest else reference
    return digest


def get_latest_http(cfg, verify_ssl=True):
    url = cfg.get('url', '')
    headers = cfg.get('headers', {})
    json_path = cfg.get('json_path', 'version')
    data = http_get_json(url, headers, verify_ssl=verify_ssl)
    return str(json_path_extract(data, json_path) or '')


def get_latest_version(latest_cfg, verify_ssl=True):
    """Return the latest version string for a check."""
    source = latest_cfg.get('source', '')
    if source == 'github':
        return get_latest_github(latest_cfg['repo'])
    if source == 'gitlab':
        token = latest_cfg.get('token') or os.environ.get(latest_cfg.get('token_env', ''))
        return get_latest_gitlab(latest_cfg['project'], latest_cfg.get('base_url', 'https://gitlab.com'), token=token)
    if source in ('gitea', 'forgejo'):
        token = latest_cfg.get('token') or os.environ.get(latest_cfg.get('token_env', ''))
        return get_latest_gitea(latest_cfg['repo'], latest_cfg['base_url'], token=token)
    if source == 'npm':
        return get_latest_npm(latest_cfg['package'])
    if source == 'pypi':
        return get_latest_pypi(latest_cfg['package'])
    if source == 'docker':
        return get_latest_docker(
            latest_cfg['repo'],
            tag_regex=latest_cfg.get('tag_regex'),
            include_prerelease=latest_cfg.get('include_prerelease', False),
            pages=latest_cfg.get('pages', 3),
        )
    if source in ('oci', 'registry'):
        latest_cfg = dict(latest_cfg)
        latest_cfg.setdefault('verify_ssl', verify_ssl)
        return get_latest_oci(latest_cfg)
    if source == 'http':
        return get_latest_http(latest_cfg, verify_ssl=verify_ssl)
    return ''

# ---------------------------------------------------------------------------
# Changelog / release notes fetchers
# ---------------------------------------------------------------------------

def get_github_releases_between(repo, installed, latest):
    """Fetch GitHub releases between installed and latest versions.
    Returns list of dicts: [{version, name, summary, url}] newest-first."""
    releases = []
    page = 1
    while page <= 5:  # cap at 5 pages (500 releases)
        url = f'https://api.github.com/repos/{repo}/releases?per_page=100&page={page}'
        try:
            data = http_get_json(url, headers=_github_headers())
        except Exception:
            break
        if not data:
            break
        for rel in data:
            tag = strip_v(rel.get('tag_name', ''))
            # Skip pre-releases and versions at or below installed
            if rel.get('prerelease') or rel.get('draft'):
                continue
            if compare_versions(tag, installed) <= 0:
                # We've gone past installed version, stop
                page = 999
                break
            body = rel.get('body') or ''
            summary = _summarize_body(body)
            releases.append({
                'version': tag,
                'name': rel.get('name') or tag,
                'summary': summary,
                'url': rel.get('html_url', ''),
            })
        page += 1
    return releases


def _summarize_body(body, max_lines=5, max_chars=300):
    """Extract a brief summary from release notes markdown."""
    if not body:
        return ''
    lines = []
    for line in body.split('\n'):
        line = line.strip()
        if not line:
            continue
        # Skip common noise
        if line.startswith('##') and any(w in line.lower() for w in ['contributor', 'full changelog', 'docker', 'sha256']):
            continue
        if line.startswith('**Full Changelog**') or line.startswith('https://github.com'):
            continue
        lines.append(line)
        if len(lines) >= max_lines:
            break
    text = '\n'.join(lines)
    if len(text) > max_chars:
        text = text[:max_chars].rsplit(' ', 1)[0] + '…'
    return text


def get_npm_changes(package, installed, latest):
    """Get npm package changelog summary. Returns list of version dicts."""
    try:
        url = f'https://registry.npmjs.org/{package}'
        data = http_get_json(url)
        repo_url = ''
        repo = (data.get('repository') or {})
        if isinstance(repo, dict):
            repo_url = repo.get('url', '')
        elif isinstance(repo, str):
            repo_url = repo
        m = re.search(r'github\.com[/:]([^/]+/[^/.]+)', repo_url)
        if m:
            return get_github_releases_between(m.group(1), installed, latest)
    except Exception:
        pass
    return []


def get_pypi_changes(package, installed, latest):
    """Get PyPI package changelog summary via GitHub if available."""
    try:
        url = f'https://pypi.org/pypi/{package}/json'
        data = http_get_json(url)
        info = data.get('info') or {}
        for field in ('project_urls', 'home_page', 'package_url'):
            urls = info.get(field) or {}
            if isinstance(urls, dict):
                for v in urls.values():
                    m = re.search(r'github\.com/([^/]+/[^/]+)', str(v))
                    if m:
                        return get_github_releases_between(m.group(1).rstrip('/'), installed, latest)
            elif isinstance(urls, str):
                m = re.search(r'github\.com/([^/]+/[^/]+)', urls)
                if m:
                    return get_github_releases_between(m.group(1).rstrip('/'), installed, latest)
    except Exception:
        pass
    return []


def fetch_changes(latest_cfg, installed, latest):
    """Fetch changelog/release notes between installed and latest.
    Returns list of dicts: [{version, name, summary, url}]."""
    source = latest_cfg.get('source', '')
    try:
        if source == 'github':
            return get_github_releases_between(latest_cfg['repo'], installed, latest)
        if source == 'npm':
            return get_npm_changes(latest_cfg['package'], installed, latest)
        if source == 'pypi':
            return get_pypi_changes(latest_cfg['package'], installed, latest)
    except Exception:
        pass
    return []

# ---------------------------------------------------------------------------
# Version comparison
# ---------------------------------------------------------------------------

def parse_version_tuple(v):
    """Parse a semver/calver-ish string into numeric parts.

    Handles prefixes and suffixes like v1.2.3, 2026.5.7-beta.1, node-22.14.0.
    Non-version words are ignored; prerelease ordering is handled by version_sort_key().
    """
    v = strip_v(str(v or '').strip())
    m = re.search(r'(\d+(?:\.\d+){0,5})', v)
    if not m:
        return (0,)
    parts = re.split(r'[.\-+]', m.group(1))
    result = []
    for p in parts:
        try:
            result.append(int(p))
        except ValueError:
            pass
    return tuple(result) or (0,)


def version_sort_key(v):
    """Sortable key where stable releases sort above prereleases with same numbers."""
    nums = parse_version_tuple(v)
    return (*nums, 0 if is_prerelease(v) else 1)


def compare_versions(a, b):
    """Return -1/0/1 for a < b, equal, a > b using semver/calver-ish rules."""
    av = list(parse_version_tuple(a))
    bv = list(parse_version_tuple(b))
    width = max(len(av), len(bv))
    av += [0] * (width - len(av))
    bv += [0] * (width - len(bv))
    if av < bv:
        return -1
    if av > bv:
        return 1
    # Same numeric version: stable is newer than prerelease.
    apre = is_prerelease(a)
    bpre = is_prerelease(b)
    if apre and not bpre:
        return -1
    if not apre and bpre:
        return 1
    return 0


def classify_drift(installed, latest):
    """Return ('current'|'minor'|'major'|'unknown', label)."""
    if not installed or not latest:
        return 'unknown', 'UNKNOWN'
    if installed == latest:
        return 'current', 'CURRENT'
    if str(installed).startswith('sha256:') or str(latest).startswith('sha256:'):
        return 'minor', 'DRIFT'
    iv = parse_version_tuple(installed)
    lv = parse_version_tuple(latest)
    if compare_versions(installed, latest) >= 0:
        return 'current', 'CURRENT'
    # major drift = first segment differs
    if len(iv) > 0 and len(lv) > 0 and iv[0] < lv[0]:
        return 'major', 'MAJOR DRIFT'
    return 'minor', 'DRIFT'


def describe_drift(installed, latest):
    """Return a human-readable description of what changed between versions."""
    iv = parse_version_tuple(installed)
    lv = parse_version_tuple(latest)

    parts = []
    if len(iv) >= 1 and len(lv) >= 1 and iv[0] != lv[0]:
        parts.append(f"major version bump ({iv[0]} → {lv[0]})")
    if len(iv) >= 2 and len(lv) >= 2 and iv[1] != lv[1]:
        diff = lv[1] - iv[1] if iv[0] == lv[0] else lv[1]
        parts.append(f"{diff} minor release{'s' if diff != 1 else ''}")
    if len(iv) >= 3 and len(lv) >= 3 and iv[0] == lv[0] and iv[1] == lv[1] and iv[2] != lv[2]:
        diff = lv[2] - iv[2]
        parts.append(f"{diff} patch{'es' if diff != 1 else ''}")

    if not parts:
        return f"{installed} → {latest}"
    return f"{installed} → {latest} ({', '.join(parts)})"

# ---------------------------------------------------------------------------
# State tracking
# ---------------------------------------------------------------------------

def load_state(path):
    try:
        with open(path) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_state(path, state):
    with open(path, 'w') as f:
        json.dump(state, f, indent=2)

# ---------------------------------------------------------------------------
# Main check logic
# ---------------------------------------------------------------------------

def run_checks(config, only_host=None, include_changes=False):
    """Run all checks, return list of result dicts."""
    results = []
    hosts = config.get('hosts', [])
    for host_cfg in hosts:
        host_name = host_cfg.get('name', 'unknown')
        if only_host and host_name != only_host:
            continue
        for check_cfg in host_cfg.get('checks', []):
            check_name = check_cfg.get('name', 'unknown')
            result = {
                'host': host_name,
                'check': check_name,
                'installed': None,
                'latest': None,
                'status': 'unknown',
                'label': 'UNKNOWN',
                'error': None,
            }
            # Installed
            try:
                result['installed'] = get_installed_version(host_cfg, check_cfg)
            except Exception as e:
                result['error'] = f'installed: {e}'

            # Latest
            try:
                verify = host_cfg.get('verify_ssl', True)
                result['latest'] = get_latest_version(check_cfg.get('latest', {}), verify_ssl=verify)
            except Exception as e:
                result['error'] = f'latest: {e}'

            if result['error']:
                result['status'] = 'error'
                result['label'] = 'ERROR'
            else:
                result['status'], result['label'] = classify_drift(
                    result['installed'], result['latest']
                )

            # Drift description
            if result['status'] in ('minor', 'major'):
                result['drift_description'] = describe_drift(
                    result['installed'], result['latest']
                )
            else:
                result['drift_description'] = None

            # Changelog
            result['changes'] = []
            if include_changes and result['status'] in ('minor', 'major'):
                try:
                    result['changes'] = fetch_changes(
                        check_cfg.get('latest', {}),
                        result['installed'], result['latest'],
                    )
                except Exception:
                    pass

            results.append(result)
    return results


def update_state(state, results):
    """Update state dict with drift timestamps. Returns updated state."""
    now = datetime.now(timezone.utc).isoformat()
    for r in results:
        key = f"{r['host']}/{r['check']}"
        prev = state.get(key, {})
        if r['status'] in ('minor', 'major'):
            if prev.get('status') in ('minor', 'major'):
                r['drifting_since'] = prev.get('drifting_since', now)
            else:
                r['drifting_since'] = now
            state[key] = {
                'status': r['status'],
                'installed': r['installed'],
                'latest': r['latest'],
                'drifting_since': r['drifting_since'],
                'last_checked': now,
            }
        else:
            r['drifting_since'] = None
            state[key] = {
                'status': r['status'],
                'installed': r['installed'],
                'latest': r['latest'],
                'drifting_since': None,
                'last_checked': now,
            }
    return state

# ---------------------------------------------------------------------------
# Output formatters
# ---------------------------------------------------------------------------

# ANSI colors (disabled when NO_COLOR is set or not a TTY)
_use_color = sys.stdout.isatty() and not os.environ.get('NO_COLOR')

def _c(code, text):
    if _use_color:
        return f'\033[{code}m{text}\033[0m'
    return text

GREEN = lambda t: _c('32', t)
YELLOW = lambda t: _c('33', t)
RED = lambda t: _c('31', t)
DIM = lambda t: _c('2', t)


def _status_display(r):
    label = r.get('label', 'UNKNOWN')
    since = r.get('drifting_since')
    suffix = ''
    if since and label in ('DRIFT', 'MAJOR DRIFT'):
        try:
            dt = datetime.fromisoformat(since)
            suffix = f' (since {dt.strftime("%Y-%m-%d")})'
        except Exception:
            pass

    if label == 'CURRENT':
        return GREEN(f'✅ {label}'), f'✅ {label}'
    if label == 'DRIFT':
        return YELLOW(f'⚠️  {label}{suffix}'), f'⚠️ {label}{suffix}'
    if label == 'MAJOR DRIFT':
        return RED(f'🔴 {label}{suffix}'), f'🔴 {label}{suffix}'
    if label == 'ERROR':
        return RED(f'❌ {label}'), f'❌ {label}'
    return DIM(f'❓ {label}'), f'❓ {label}'


def format_table(results):
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = [f'Version Drift Report — {now}', '']

    # Column widths
    hw = max((len(r['host']) for r in results), default=4)
    cw = max((len(r['check']) for r in results), default=5)
    iw = max((len(r.get('installed') or 'N/A') for r in results), default=9)
    lw = max((len(r.get('latest') or 'N/A') for r in results), default=6)
    hw = max(hw, 4); cw = max(cw, 5); iw = max(iw, 9); lw = max(lw, 6)

    header = f"{'Host':<{hw}}  {'Check':<{cw}}  {'Installed':<{iw}}  {'Latest':<{lw}}  Status"
    lines.append(header)
    lines.append('─' * (hw + cw + iw + lw + 30))

    current = 0
    total = len(results)
    for r in results:
        colored, _ = _status_display(r)
        inst = r.get('installed') or 'N/A'
        lat = r.get('latest') or 'N/A'
        if r.get('error'):
            inst = 'ERROR'
            lat = 'ERROR'
        line = f"{r['host']:<{hw}}  {r['check']:<{cw}}  {inst:<{iw}}  {lat:<{lw}}  {colored}"
        lines.append(line)
        if r.get('drift_description'):
            lines.append(f"  {'':>{hw}}  {'':>{cw}}  ↳ {DIM(r['drift_description'])}")
        if r.get('changes'):
            for ch in r['changes'][:5]:  # max 5 releases shown
                ver_str = f"  {'':>{hw}}  {'':>{cw}}    {ch['version']}"
                if ch.get('summary'):
                    first_line = ch['summary'].split('\n')[0][:80]
                    ver_str += f" — {DIM(first_line)}"
                lines.append(ver_str)
            if len(r.get('changes', [])) > 5:
                lines.append(f"  {'':>{hw}}  {'':>{cw}}    ... and {len(r['changes']) - 5} more releases")
        if r['status'] == 'current':
            current += 1

    drifting = total - current
    lines.append('')
    lines.append(f'Summary: {current}/{total} up to date, {drifting} drifting')
    return '\n'.join(lines)


def format_markdown(results):
    now = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    lines = [f'**Version Drift Report** — {now}', '']
    lines.append('| Host | Check | Installed | Latest | Status |')
    lines.append('|------|-------|-----------|--------|--------|')

    current = 0
    total = len(results)
    for r in results:
        _, plain = _status_display(r)
        inst = r.get('installed') or 'N/A'
        lat = r.get('latest') or 'N/A'
        if r.get('error'):
            inst = 'ERROR'
            lat = 'ERROR'
        lines.append(f'| {r["host"]} | {r["check"]} | {inst} | {lat} | {plain} |')
        if r['status'] == 'current':
            current += 1

    drifting = total - current
    lines.append('')
    lines.append(f'**Summary:** {current}/{total} up to date, {drifting} drifting')

    # Changelog details
    items_with_changes = [r for r in results if r.get('changes') or r.get('drift_description')]
    if items_with_changes:
        lines.append('')
        lines.append('### Changes')
        for r in items_with_changes:
            lines.append(f'')
            lines.append(f'**{r["host"]}/{r["check"]}** — {r.get("drift_description", "")}')
            if r.get('changes'):
                for ch in r['changes'][:8]:
                    summary_line = ''
                    if ch.get('summary'):
                        summary_line = f' — {ch["summary"].split(chr(10))[0][:100]}'
                    lines.append(f'- `{ch["version"]}`{summary_line}')
                if len(r.get('changes', [])) > 8:
                    lines.append(f'- *...and {len(r["changes"]) - 8} more releases*')

    return '\n'.join(lines)


def format_json(results):
    now = datetime.now(timezone.utc).isoformat()
    output = {
        'timestamp': now,
        'results': results,
        'summary': {
            'total': len(results),
            'current': sum(1 for r in results if r['status'] == 'current'),
            'drifting': sum(1 for r in results if r['status'] in ('minor', 'major')),
            'errors': sum(1 for r in results if r['status'] == 'error'),
            'changes_fetched': any(r.get('changes') for r in results),
        }
    }
    return json.dumps(output, indent=2)

# ---------------------------------------------------------------------------
# Config discovery helpers
# ---------------------------------------------------------------------------

def _iter_compose_images(path):
    """Yield (service, image) pairs from a Docker Compose file."""
    text = Path(path).read_text()
    if HAS_YAML:
        data = yaml.safe_load(text) or {}
        for service, cfg in (data.get('services') or {}).items():
            image = (cfg or {}).get('image')
            if image:
                yield service, str(image)
        return

    # Minimal fallback for simple compose files when PyYAML is unavailable.
    current = None
    for line in text.splitlines():
        m = re.match(r'^\s{2}([A-Za-z0-9_.-]+):\s*$', line)
        if m:
            current = m.group(1)
        m = re.match(r'^\s+image:\s*["\']?([^"\'#]+)', line)
        if current and m:
            yield current, m.group(1).strip()


def discover_compose(path, host_name='docker-host'):
    """Return a suggested config fragment for Docker Compose image digest checks."""
    checks = []
    for service, image in _iter_compose_images(path):
        registry, repo, ref = _normalise_oci_image(image)
        digest_cmd = (
            "docker inspect "
            f"$(docker compose ps -q {shlex.quote(service)}) "
            "--format '{{range .RepoDigests}}{{println .}}{{end}}' "
            "| head -1 | sed 's/.*@//'"
        )
        checks.append({
            'name': service,
            'installed': digest_cmd,
            'latest': {'source': 'oci', 'image': f'{registry}/{repo}', 'tag': ref, 'return': 'digest'},
        })
    return {'hosts': [{'name': host_name, 'type': 'local', 'checks': checks}]}

# ---------------------------------------------------------------------------
# Config loading
# ---------------------------------------------------------------------------

def load_config(path):
    path = Path(path)
    if not path.exists():
        print(f"Error: config file not found: {path}", file=sys.stderr)
        print(f"Hint: copy config.example.yaml to config.yaml and customize it.", file=sys.stderr)
        sys.exit(1)

    with open(path) as f:
        content = f.read()

    if HAS_YAML and path.suffix in ('.yaml', '.yml'):
        config = yaml.safe_load(content)
    else:
        config = json.loads(content)

    return expand_env(config)

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def print_usage():
    print(textwrap.dedent("""\
        Usage:
          python3 drift.py check [OPTIONS]
          python3 drift.py discover --compose docker-compose.yml [--host NAME]

        Check options:
          --config PATH    Config file path (default: config.yaml)
          --json           Output as JSON
          --markdown       Output as markdown table
          --only HOST      Check only this host
          --changes        Fetch changelogs for drifting items (slower)
          --no-state       Don't read/write state file
          -h, --help       Show this help

        Discover options:
          --compose PATH    Generate digest checks from Docker Compose images
          --host NAME       Host name to use in generated config

        Examples:
          python3 drift.py check
          python3 drift.py check --json
          python3 drift.py check --only my-server --markdown
          python3 drift.py discover --compose docker-compose.yml
    """))


def main():
    args = sys.argv[1:]

    if not args or args[0] in ('-h', '--help'):
        print_usage()
        sys.exit(0)

    if args[0] == 'discover':
        compose_path = None
        host_name = 'docker-host'
        i = 1
        while i < len(args):
            a = args[i]
            if a == '--compose' and i + 1 < len(args):
                compose_path = args[i + 1]; i += 2
            elif a == '--host' and i + 1 < len(args):
                host_name = args[i + 1]; i += 2
            elif a in ('-h', '--help'):
                print_usage(); sys.exit(0)
            else:
                print(f"Unknown option: {a}", file=sys.stderr)
                print_usage(); sys.exit(1)
        if not compose_path:
            print("Error: discover requires --compose PATH", file=sys.stderr)
            sys.exit(1)
        fragment = discover_compose(compose_path, host_name=host_name)
        if HAS_YAML:
            print(yaml.safe_dump(fragment, sort_keys=False))
        else:
            print(json.dumps(fragment, indent=2))
        sys.exit(0)

    if args[0] != 'check':
        print(f"Unknown command: {args[0]}", file=sys.stderr)
        print_usage()
        sys.exit(1)

    # Parse flags
    config_path = None
    output_fmt = None
    only_host = None
    no_state = False
    include_changes = False

    i = 1
    while i < len(args):
        a = args[i]
        if a == '--config' and i + 1 < len(args):
            config_path = args[i + 1]; i += 2
        elif a == '--json':
            output_fmt = 'json'; i += 1
        elif a == '--markdown':
            output_fmt = 'markdown'; i += 1
        elif a == '--only' and i + 1 < len(args):
            only_host = args[i + 1]; i += 2
        elif a == '--changes':
            include_changes = True; i += 1
        elif a == '--no-state':
            no_state = True; i += 1
        elif a in ('-h', '--help'):
            print_usage(); sys.exit(0)
        else:
            print(f"Unknown option: {a}", file=sys.stderr)
            print_usage(); sys.exit(1)

    # Resolve config path
    if not config_path:
        # Look next to script first, then cwd
        script_config = SCRIPT_DIR / 'config.yaml'
        if script_config.exists():
            config_path = str(script_config)
        else:
            config_path = 'config.yaml'

    config = load_config(config_path)

    # Determine output format
    if not output_fmt:
        output_fmt = (config.get('output') or {}).get('format', 'table')

    # State file
    state_file = (config.get('output') or {}).get('state_file', 'state.json')
    if not os.path.isabs(state_file):
        state_file = str(SCRIPT_DIR / state_file)

    state = {} if no_state else load_state(state_file)

    # Run checks
    results = run_checks(config, only_host=only_host, include_changes=include_changes)
    state = update_state(state, results)

    if not no_state:
        save_state(state_file, state)

    # Output
    if output_fmt == 'json':
        print(format_json(results))
    elif output_fmt == 'markdown':
        print(format_markdown(results))
    else:
        print(format_table(results))

    # Exit code: non-zero if any drift
    has_drift = any(r['status'] in ('minor', 'major') for r in results)
    has_error = any(r['status'] == 'error' for r in results)
    if has_error:
        sys.exit(2)
    if has_drift:
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
