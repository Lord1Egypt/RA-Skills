"""
supply_chain.py - Supply chain risk analysis for skill-security-checker.

Runs as part of the audit pipeline (SecurityAuditor.scan_supply_chain()).
Offline-first: OSV.dev data-package index (full ecosystem) -> OSV API -> NVD
-> local 26-entry CVE DB. Lock-file parsing enables version-range matching.
Offline-capable detection (typo-squatting, dependency tree, license scan)
works without any API access.

Author: njskills@agent.qq.com
Version: 3.0.0
"""

import os
import re
import json
import time
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed

# OSV offline data package integration (v3.4.0). Degrades gracefully if missing.
try:
    from osv_offline import (ensure_osv_index, load_osv_index, query_osv_index,
                             get_index_timestamp, osv_index_known_packages)
    _OSV_OFFLINE_AVAILABLE = True
except Exception:
    _OSV_OFFLINE_AVAILABLE = False

# ============================================================
# Constants
# ============================================================

# Well-known packages used for typo-squatting detection.
TOP_PYTHON_PACKAGES = [
    'requests', 'numpy', 'pandas', 'matplotlib', 'scipy', 'scikit-learn',
    'tensorflow', 'torch', 'keras', 'django', 'flask', 'fastapi',
    'aiohttp', 'tornado', 'celery', 'sqlalchemy', 'alembic',
    'redis', 'pymongo', 'psycopg2', 'mysql-connector-python',
    'pillow', 'pyyaml', 'jinja2', 'werkzeug', 'click', 'tqdm',
    'pytest', 'coverage', 'mypy', 'black', 'isort', 'flake8',
    'sphinx', 'twine', 'setuptools', 'wheel', 'pip',
    'cryptography', 'pyjwt', 'oauth2client', 'httpx', 'urllib3',
    'grpcio', 'protobuf', 'beautifulsoup4', 'lxml', 'scrapy',
    'opencv-python', 'pyinstaller', 'nuitka', 'cython',
    'typing-extensions', 'packaging', 'importlib-metadata',
    'certifi', 'chardet', 'idna', 'charset-normalizer',
    'six', 'python-dateutil', 'decorator', 'attrs',
    'pytz', 'regex', 'msgpack', 'toml', 'colorama',
    'docutils', 'pygments', 'six', 'filelock',
    'virtualenv', 'distlib', 'platformdirs', 'pluggy',
    'pyparsing', 'jsonschema', 'pyrsistent', 'iniconfig',
]

TOP_NODE_PACKAGES = [
    'react', 'vue', 'angular', 'express', 'lodash', 'axios',
    'webpack', 'babel', 'jest', 'mocha', 'eslint', 'prettier',
    'typescript', 'gulp', 'grunt', 'socket.io', 'moment',
    'async', 'debug', 'ms', 'semver', 'chalk',
    'commander', 'glob', 'minimatch', 'globby',
    'rimraf', 'mkdirp', 'uuid', 'nanoid',
    'node-fetch', 'cross-fetch', 'isomorphic-fetch',
    'dotenv', 'config', 'cosmiconfig', 'js-yaml',
    'minimist', 'yargs', 'inquirer', 'enquirer',
    'webpack', 'rollup', 'esbuild', 'vite', 'parcel',
    'eslint', 'tslint', 'standard', 'xo',
    'husky', 'lint-staged', 'commitlint',
]

# Incompatible license mapping (project_license -> list of forbidden licenses)
LICENSE_INCOMPATIBLE = {
    'MIT': ['GPL-2.0', 'GPL-3.0', 'AGPL-3.0', 'SSPL-1.0'],
    'Apache-2.0': ['GPL-2.0', 'AGPL-3.0', 'SSPL-1.0'],
    'BSD-2-Clause': ['GPL-2.0', 'GPL-3.0', 'AGPL-3.0', 'SSPL-1.0'],
    'BSD-3-Clause': ['GPL-2.0', 'GPL-3.0', 'AGPL-3.0', 'SSPL-1.0'],
    'GPL-2.0': ['MIT', 'Apache-2.0', 'BSD-2-Clause', 'BSD-3-Clause', 'ISC'],
    'GPL-3.0': ['MIT', 'Apache-2.0', 'BSD-2-Clause', 'BSD-3-Clause', 'ISC'],
    'AGPL-3.0': ['MIT', 'Apache-2.0', 'BSD-2-Clause', 'BSD-3-Clause', 'ISC', 'GPL-2.0'],
}

# Obfuscation map used by typo-squatting (visual similarity)
CHAR_CONFUSION = {
    '0': 'o', 'o': '0',
    '1': 'l', 'l': '1',
    '5': 's', 's': '5',
    'rn': 'm', 'm': 'rn',
    'vv': 'w', 'w': 'vv',
    'cl': 'd', 'd': 'cl',
}

# ============================================================
# Data Structures
# ============================================================

class SupplyChainFinding:
    """One supply-chain risk finding (mirrors static ScanResult shape)."""
    def __init__(self, category, severity, message, suggestion, detail=None):
        self.category = category
        self.severity = severity
        self.file = '<supply-chain>'
        self.line = 0
        self.message = message
        self.pattern = 'supply_chain'
        self.suggestion = suggestion
        self.source = 'supply_chain'
        self.detail = detail or {}

    def to_dict(self):
        return {
            'category': self.category,
            'severity': self.severity,
            'file': self.file,
            'line': self.line,
            'message': self.message,
            'pattern': self.pattern,
            'suggestion': self.suggestion,
            'source': self.source,
            'detail': self.detail,
        }

# ============================================================
# Helpers
# ============================================================

def _levenshtein(a, b):
    """Classic Levenshtein distance."""
    if len(a) < len(b):
        return _levenshtein(b, a)
    if len(b) == 0:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a):
        curr = [i + 1]
        for j, cb in enumerate(b):
            insert = prev[j + 1] + 1
            delete = curr[j] + 1
            replace = prev[j] + (ca != cb)
            curr.append(min(insert, delete, replace))
        prev = curr
    return prev[-1]


def _normalize_pkg_name(name):
    """Normalize a package name for comparison."""
    return re.sub(r'[-_.]+', '-', name.lower()).strip('-')


def _get_cache_dir():
    """Return a writable cache directory (cross-platform)."""
    base = Path.home() / '.workbuddy' / 'supply_chain_cache'
    base.mkdir(parents=True, exist_ok=True)
    return base


def _cache_path(key):
    hashed = hashlib.md5(key.encode()).hexdigest()[:12]
    return _get_cache_dir() / f'{hashed}.json'


def _read_cache(key, ttl_hours):
    """Read cached data if present and fresh."""
    p = _cache_path(key)
    if not p.exists():
        return None
    try:
        data = json.loads(p.read_text(encoding='utf-8'))
        ts = data.get('_ts', 0)
        if time.time() - ts < ttl_hours * 3600:
            return data.get('payload')
    except Exception:
        pass
    return None


def _write_cache(key, payload):
    p = _cache_path(key)
    try:
        p.write_text(json.dumps({'_ts': time.time(), 'payload': payload},
                               ensure_ascii=False), encoding='utf-8')
    except Exception:
        pass


def _http_get_json(url, timeout=8):
    """HTTP GET returning parsed JSON, or None on failure (stdlib only)."""
    try:
        import urllib.request, urllib.error
        req = urllib.request.Request(url, headers={
            'User-Agent': 'skill-security-checker/3.0.0',
            'Accept': 'application/json',
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode('utf-8'))
    except Exception:
        return None


# ============================================================
# 1. Dependency Tree Parsing
# ============================================================

def parse_requirements_txt(content):
    """Parse requirements.txt content -> list of (name, version)."""
    deps = []
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('-'):
            continue
        # Strip extras and environment markers
        line = line.split(';')[0].strip()
        for sep in ['==', '>=', '<=', '~=', '!=']:
            if sep in line:
                name, _, ver = line.partition(sep)
                deps.append((name.strip(), ver.strip()))
                break
        else:
            deps.append((line, ''))
    return deps


def parse_package_json(content):
    """Parse package.json content -> list of (name, version)."""
    try:
        data = json.loads(content)
    except Exception:
        return []
    deps = []
    for section in ['dependencies', 'devDependencies', 'peerDependencies']:
        block = data.get(section, {})
        if isinstance(block, dict):
            for name, ver in block.items():
                deps.append((name, str(ver)))
    return deps


def parse_pyproject_toml(content):
    """Minimal TOML-ish parser for pyproject.toml [project] dependencies."""
    deps = []
    in_deps = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped == 'dependencies = [':
            in_deps = True
            continue
        if in_deps:
            if stripped == ']':
                in_deps = False
                continue
            m = re.match(r'\s*["\']([^"\']+)["\']\s*,?\s*', stripped)
            if m:
                dep = m.group(1)
                for sep in ['>=', '<=', '==', '~=', '!=', '>', '<', '=']:
                    if sep in dep:
                        name, _, ver = dep.partition(sep)
                        deps.append((name.strip(), ver.strip()))
                        break
                else:
                    deps.append((dep.strip(), ''))
    return deps


def parse_package_lock_json(content):
    """Parse package-lock.json (lockfileVersion 1/2/3) -> list of (name, version, transitive).

    Lock files contain the full resolved dependency tree, so versions are exact
    and the closure is known (approx=False).
    """
    try:
        data = json.loads(content)
    except Exception:
        return []
    records = []
    # lockfileVersion >= 2: 'packages' dict keyed by node_modules path
    packages = data.get('packages')
    if isinstance(packages, dict):
        for key, val in packages.items():
            if not isinstance(val, dict) or not key:
                continue
            name = key.split('node_modules/')[-1]
            if not name or '/' in name:
                continue
            ver = val.get('version')
            if ver:
                records.append((name, ver, True))
        if records:
            return records
    # lockfileVersion 1: nested 'dependencies' tree
    seen = {}

    def _walk(node):
        if not isinstance(node, dict):
            return
        for name, val in node.items():
            if not isinstance(val, dict):
                continue
            ver = val.get('version')
            if ver and name not in seen:
                seen[name] = (name, ver, True)
            _walk(val.get('dependencies', {}))

    _walk(data.get('dependencies', {}))
    return list(seen.values())


def parse_poetry_lock(content):
    """Parse poetry.lock [[package]] sections -> list of (name, version, transitive).

    Contains full transitive tree; exact + non-approx.
    """
    records = []
    blocks = re.split(r'\[\[package\]\]', content)
    for block in blocks[1:]:
        name = None
        ver = None
        for line in block.splitlines():
            m = re.match(r'\s*name\s*=\s*["\']([^"\']+)["\']', line)
            if m:
                name = m.group(1)
            m = re.match(r'\s*version\s*=\s*["\']([^"\']+)["\']', line)
            if m:
                ver = m.group(1)
            if name and ver:
                break
        if name and ver:
            records.append((name, ver, True))
    return records


def discover_dependency_records(skill_path):
    """Discover and parse all dependency manifests into rich records.

    Returns list of dicts:
      {name, version_spec, exact_version, approx, ecosystem, manifest, transitive}
    approx=True means the resolved version / full tree is unknown (no lock file),
    so version-range matching is approximate and flagged as such.
    """
    skill_path = Path(skill_path)
    records = []
    # (filename, parser, ecosystem, is_lock_file)
    candidates = [
        ('requirements.txt', parse_requirements_txt, 'pypi', False),
        ('package.json', parse_package_json, 'npm', False),
        ('pyproject.toml', parse_pyproject_toml, 'pypi', False),
        ('package-lock.json', parse_package_lock_json, 'npm', True),
        ('poetry.lock', parse_poetry_lock, 'pypi', True),
        ('Pipfile', None, 'pypi', False),  # Future
    ]
    for fname, parser, eco, is_lock in candidates:
        if parser is None:
            continue
        p = skill_path / fname
        if not p.exists():
            continue
        try:
            text = p.read_text(encoding='utf-8-sig')
        except Exception:
            continue
        parsed = parser(text)
        for item in parsed:
            if len(item) == 3:
                name, ver, _ = item
            else:
                name, ver = item[0], item[1]
            if is_lock:
                # Lock file: version is the resolved exact version, full tree known
                exact_version = ver
                approx = False
            else:
                # Constraint manifest: exact only when pinned; full tree unknown
                exact_version = ver if ver else None
                approx = True
            records.append({
                'name': name,
                'version_spec': ver,
                'exact_version': exact_version,
                'approx': approx,
                'ecosystem': eco,
                'manifest': fname,
                'transitive': is_lock,
            })
    return records


# ============================================================
# 2. Typo-Squatting Detection (offline, no API)
# ============================================================

def _confusion_candidates(name):
    """Generate visually-similar variants using the confusion map."""
    candidates = set()
    for src, dst in CHAR_CONFUSION.items():
        if src in name:
            candidates.add(name.replace(src, dst))
    return candidates


def detect_typo_squats(package_names):
    """Return list of (squatted_name, legitimate_name, distance)."""
    top_python = set(_normalize_pkg_name(n) for n in TOP_PYTHON_PACKAGES)
    top_node = set(_normalize_pkg_name(n) for n in TOP_NODE_PACKAGES)
    top_all = top_python | top_node
    findings = []
    seen = set()
    for name in package_names:
        norm = _normalize_pkg_name(name)
        if norm in top_all:
            continue
        # Quick pre-filter: only check if Levenshtein <= 2 against any top pkg.
        for legit in top_all:
            if abs(len(norm) - len(legit)) > 2:
                continue
            dist = _levenshtein(norm, legit)
            if dist <= 2 and dist > 0:
                key = tuple(sorted([norm, legit]))
                if key in seen:
                    continue
                seen.add(key)
                findings.append((name, legit, dist))
                break  # one match per candidate
        # Also check confusion-based variants.
        for cand in _confusion_candidates(norm):
            if cand in top_all:
                findings.append((name, cand, 0))
                break
    return findings


# ============================================================
# 3. Maintenance Status Assessment (with caching)
# ============================================================

def _check_pypi_status(package_name, ttl=24):
    """Fetch PyPI metadata for a package (cached)."""
    cache_key = f'pypi:{package_name}'
    cached = _read_cache(cache_key, ttl)
    if cached is not None:
        return cached
    data = _http_get_json(f'https://pypi.org/pypi/{package_name}/json')
    if data and 'info' in data:
        info = data['info']
        result = {
            'source': 'pypi',
            'name': package_name,
            'latest_version': info.get('version'),
            'last_release_date': _pypi_latest_date(data),
            'deprecated': info.get('classifiers', []) and any(
                'Development Status' in c and 'Inactive' in c
                for c in info.get('classifiers', [])
            ),
            'summary': (info.get('summary') or '')[:120],
        }
        _write_cache(cache_key, result)
        return result
    return None


def _pypi_latest_date(data):
    """Extract most recent release date from PyPI JSON."""
    try:
        releases = data.get('releases', {})
        dates = []
        for ver, files in releases.items():
            for f in files:
                d = f.get('upload_time')
                if d:
                    dates.append(d)
        return max(dates) if dates else None
    except Exception:
        return None


def _check_npm_status(package_name, ttl=24):
    """Fetch npm registry metadata (cached)."""
    cache_key = f'npm:{package_name}'
    cached = _read_cache(cache_key, ttl)
    if cached is not None:
        return cached
    data = _http_get_json(f'https://registry.npmjs.org/{package_name}')
    if data:
        latest = data.get('dist-tags', {}).get('latest')
        time_map = data.get('time', {})
        last_time = time_map.get(latest) or time_map.get('modified')
        result = {
            'source': 'npm',
            'name': package_name,
            'latest_version': latest,
            'last_release_date': last_time,
            'deprecated': bool(data.get(latest, {}).get('deprecated')) if latest else False,
        }
        _write_cache(cache_key, result)
        return result
    return None


def assess_maintenance(package_name, source='pypi', ttl=24):
    """Assess a single package's maintenance status."""
    if source == 'npm':
        return _check_npm_status(package_name, ttl)
    return _check_pypi_status(package_name, ttl)


# ============================================================
# 4. License Compliance
# ============================================================

SPDX_LICENSE_SPDX_IDS = [
    'MIT', 'Apache-2.0', 'BSD-2-Clause', 'BSD-3-Clause', 'ISC',
    'GPL-2.0', 'GPL-3.0', 'AGPL-3.0', 'LGPL-2.1', 'LGPL-3.0',
    'MPL-2.0', 'Unlicense', 'SSPL-1.0', 'Proprietary',
]


def _parse_spdx_from_classifier(classifier):
    """Extract SPDX id from a PyPI classifier string like 'License :: OSI Approved :: MIT'."""
    if '::' in classifier:
        parts = classifier.split('::')
        return parts[-1].strip()
    return ''


def get_pypi_license(package_name, ttl=72):
    """Get license info from PyPI."""
    cache_key = f'pypi_license:{package_name}'
    cached = _read_cache(cache_key, ttl)
    if cached is not None:
        return cached
    data = _http_get_json(f'https://pypi.org/pypi/{package_name}/json')
    if data and 'info' in data:
        info = data['info']
        license_str = (info.get('license') or '').strip()
        classifiers = info.get('classifiers', [])
        classifier_license = ''
        for c in classifiers:
            if 'License' in c and 'OSI Approved' in c:
                classifier_license = _parse_spdx_from_classifier(c)
                break
        result = {
            'license_field': license_str,
            'classifier_license': classifier_license,
            'combined': classifier_license or license_str,
        }
        _write_cache(cache_key, result)
        return result
    return None


def check_license_compatibility(dep_license, project_license):
    """Check if dep_license is compatible with project_license."""
    if not dep_license or not project_license:
        return True, 'unknown'
    dep_norm = dep_license.strip()
    proj_norm = project_license.strip()
    # Exact match = compatible
    if dep_norm.lower() == proj_norm.lower():
        return True, 'compatible'
    # Check known incompatibilities
    forbidden = LICENSE_INCOMPATIBLE.get(proj_norm, [])
    for fb in forbidden:
        if fb.lower() in dep_norm.lower():
            return False, fb
    return True, 'unknown'


# ============================================================
# 5. CVE Database (auto-pull with fallback)
# ============================================================

# Local fallback: manually curated 26-entry CVE DB (kept for offline mode)
LOCAL_KNOWN_VULN = {
    'requests': {'<2.32.0': 'CVE-2024-35195'},
    'urllib3': {'<2.2.0': 'CVE-2024-49769'},
    'flask': {'<3.0.0': 'CVE-2023-30861'},
    'django': {'<4.2.0': 'CVE-2023-43665'},
    'numpy': {'<1.22.0': 'CVE-2021-33430'},
    'pillow': {'<10.0.0': 'CVE-2023-44271'},
    'pyyaml': {'<6.0': 'CVE-2020-14343'},
    'jinja2': {'<3.1.0': 'CVE-2024-22851'},
    'cryptography': {'<42.0.0': 'CVE-2023-49083'},
    'aiohttp': {'<3.9.0': 'CVE-2023-47627'},
    'tqdm': {},
    'setuptools': {'<65.5.0': 'CVE-2022-40897'},
    'node-fetch': {'<2.6.7': 'CVE-2022-0235'},
    'minimist': {'<1.2.6': 'CVE-2021-44906'},
    'lodash': {'<4.17.21': 'CVE-2021-23337'},
    'axios': {'<0.21.1': 'CVE-2021-3749'},
    'express': {'<4.19.2': 'CVE-2024-29045'},
    'vue': {},
    'react': {},
    'webpack': {'<5.76.0': 'CVE-2023-28153'},
    'moment': {'<2.29.4': 'CVE-2022-31129'},
    'npm': {'<6.14.17': 'CVE-2022-29244'},
    'tough-cookie': {'<4.1.3': 'CVE-2023-26136'},
    'word-wrap': {'<1.2.4': 'CVE-2023-26115'},
    'protobuf': {'<3.19.5': 'CVE-2022-1941'},
    'eslint': {},
}


def _query_osv_batch(package_names, ecosystem):
    """Query OSV API for a batch of packages. Returns dict of pkg->vulns list."""
    if not package_names:
        return {}
    url = 'https://api.osv.dev/v1/query'
    results = {}
    # OSV recommends batch size <= 100; we chunk for safety.
    batch_size = 50
    for i in range(0, len(package_names), batch_size):
        batch = package_names[i:i+batch_size]
        payload = json.dumps([{
            'version': '*',
            'package': {'name': name, 'ecosystem': ecosystem}
        } for name in batch]).encode()
        try:
            import urllib.request, urllib.error
            req = urllib.request.Request(url, data=payload, headers={
                'Content-Type': 'application/json',
                'User-Agent': 'skill-security-checker/3.0.0',
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                for j, item in enumerate(data.get('results', [])):
                    pkg = batch[j] if j < len(batch) else None
                    if pkg and item.get('vulns'):
                        results[pkg] = item['vulns'][:5]  # Cap at 5 per pkg
        except Exception:
            break
        time.sleep(0.2)  # Rate limit friendliness
    return results


# CVE offline cache paths (7-day full + daily increment)
CVE_OFFLINE_CACHE_DIR = Path.home() / ".workbuddy" / "cve_cache"
CVE_OFFLINE_CACHE_DIR.mkdir(parents=True, exist_ok=True)
CVE_FULL_CACHE_PATH = CVE_OFFLINE_CACHE_DIR / "cve_full_cache.json"
CVE_INCREMENT_CACHE_PATH = CVE_OFFLINE_CACHE_DIR / "cve_increment_cache.json"
CVE_FULL_TTL_DAYS = 7


def _get_cve_offline_cache(package_names, ecosystem='pypi'):
    """Look up CVEs from offline cache (7-day full + daily increment)."""
    now = time.time()
    cves = {}

    # Check increment cache first (today's updates)
    if CVE_INCREMENT_CACHE_PATH.exists():
        try:
            inc_data = json.loads(CVE_INCREMENT_CACHE_PATH.read_text(encoding='utf-8'))
            inc_ts = inc_data.get('_ts', 0)
            # Increment valid for 24h
            if now - inc_ts < 86400:
                inc_entries = inc_data.get('entries', {})
                for pkg in package_names:
                    if pkg in inc_entries:
                        cves[pkg] = inc_entries[pkg]
        except Exception:
            pass

    # Check full cache (7-day)
    if CVE_FULL_CACHE_PATH.exists():
        try:
            full_data = json.loads(CVE_FULL_CACHE_PATH.read_text(encoding='utf-8'))
            full_ts = full_data.get('_ts', 0)
            if now - full_ts < CVE_FULL_TTL_DAYS * 86400:
                full_entries = full_data.get('entries', {})
                for pkg in package_names:
                    if pkg not in cves and pkg in full_entries:
                        cves[pkg] = full_entries[pkg]
        except Exception:
            pass

    return cves


def _update_cve_offline_cache(new_cve_data, mode='increment'):
    """Update offline cache with fresh CVE data."""
    try:
        if mode == 'increment' and CVE_INCREMENT_CACHE_PATH.exists():
            existing = json.loads(CVE_INCREMENT_CACHE_PATH.read_text(encoding='utf-8'))
            entries = existing.get('entries', {})
        else:
            entries = {}

        entries.update(new_cve_data)
        cache_data = {
            '_ts': time.time(),
            'entries': entries,
            'ecosystem': 'pypi',
            'updated': datetime.now().isoformat(),
        }
        target = CVE_INCREMENT_CACHE_PATH if mode == 'increment' else CVE_FULL_CACHE_PATH
        target.write_text(json.dumps(cache_data, ensure_ascii=False, indent=2), encoding='utf-8')
    except Exception:
        pass


def _query_nvd_single(package_name, ecosystem):
    """Fallback: NVD NIST API for a single package."""
    if ecosystem == 'npm':
        keyword = f'npm {package_name}'
    else:
        keyword = f'pypi {package_name}'
    url = f'https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={keyword}&resultsPerPage=5'
    data = _http_get_json(url)
    if data and data.get('vulnerabilities'):
        return [v['cve']['id'] for v in data['vulnerabilities'][:5]]
    return []


def query_cve_database(package_names, ecosystem='pypi'):
    """Query CVEs for a list of packages.
    
    Flow: offline cache (7-day full + daily increment) -> OSV batch -> NVD -> local.
    Fresh API results are written back to offline cache.
    """
    # 1. Try offline cache first
    cves = _get_cve_offline_cache(package_names, ecosystem)
    
    # 2. Filter packages still missing
    missing = [pkg for pkg in package_names if pkg not in cves]
    
    if not missing:
        return cves

    # 3. Try OSV batch for missing packages
    fresh_results = {}
    try:
        osv_results = _query_osv_batch(missing, ecosystem)
        for pkg, vulns in osv_results.items():
            cve_ids = [v.get('id') for v in vulns if v.get('id')]
            if cve_ids:
                cves[pkg] = cve_ids
                fresh_results[pkg] = cve_ids
    except Exception:
        osv_results = {}

    # 4. NVD fallback for any still missing
    still_missing = [pkg for pkg in missing if pkg not in cves]
    for pkg in still_missing:
        try:
            found = _query_nvd_single(pkg, ecosystem)
            if found:
                cves[pkg] = found
                fresh_results[pkg] = found
        except Exception:
            pass
        time.sleep(0.35)

    # 5. Local fallback for anything still missing
    for pkg in package_names:
        if pkg in cves:
            continue
        norm = _normalize_pkg_name(pkg)
        for local_pkg, vulns in LOCAL_KNOWN_VULN.items():
            if _normalize_pkg_name(local_pkg) == norm:
                local_cves = [v for v in vulns.values() if v]
                if local_cves:
                    cves[pkg] = local_cves
                    fresh_results[pkg] = local_cves
                break

    # 6. Write fresh results to offline cache
    if fresh_results:
        _update_cve_offline_cache(fresh_results, mode='increment')

    return cves


# ============================================================
# Main Pipeline
# ============================================================

def scan_supply_chain(skill_path, frontmatter=None, refresh_osv=False):
    """Run the full supply chain pipeline. Returns list of SupplyChainFinding.

    v3.4.0: vulnerability detection is offline-first via the OSV data package
    index (full ecosystem) with version-range matching; falls back to the
    OSV-API / NVD / local-26-entry chain for packages the index missed.
    """
    findings = []
    records = discover_dependency_records(skill_path)
    if not records:
        return findings

    # Group by ecosystem
    by_eco = {}
    for r in records:
        by_eco.setdefault(r['ecosystem'], []).append(r)

    all_package_names = set(r['name'] for r in records)
    pypi_names = [r['name'] for r in records if r['ecosystem'] == 'pypi']

    # 1. Typo-squatting detection (both ecosystems merged)
    squats = detect_typo_squats(list(all_package_names))
    for squatted, legit, dist in squats:
        findings.append(SupplyChainFinding(
            category='typo_squatting', severity='high',
            message=f'包名疑似钓鱼: "{squatted}" 与知名包 "{legit}" 高度相似 (距离={dist})',
            suggestion=f'确认 "{squatted}" 是否为可信来源；如非必要请替换为 "{legit}"',
            detail={'squatted': squatted, 'legitimate': legit, 'distance': dist},
        ))

    # 2. Vulnerability query (offline-first OSV index + fallback)
    resolved_cves = set()
    for eco, eco_records in by_eco.items():
        exact_map = {r['name']: r['exact_version'] for r in eco_records if r['exact_version']}
        osv_hits = {}
        if _OSV_OFFLINE_AVAILABLE:
            # Refresh index if stale (>7d) or forced; degrades silently on failure
            try:
                ensure_osv_index(eco, force=refresh_osv)
            except Exception:
                pass
            data_point = get_index_timestamp(eco) or 'unknown'
            pkgs_with_ver = [(r['name'], r['exact_version'], r['approx']) for r in eco_records]
            try:
                osv_hits = query_osv_index(pkgs_with_ver, eco)
            except Exception:
                osv_hits = {}
            for pkg, hits in osv_hits.items():
                for h in hits:
                    vid = h['id']
                    resolved_cves.add((pkg, vid))
                    ver = exact_map.get(pkg, '未知')
                    if h['match_level'] == 'exact':
                        severity = 'critical'
                        msg = f'依赖包 "{pkg}" (版本 {ver}) 命中已知漏洞: {vid}'
                    else:
                        note = '近似匹配' if h['approx'] else '无精确版本'
                        severity = 'medium'
                        msg = f'依赖包 "{pkg}" 存在潜在漏洞 {vid}（{note}，建议提供 lock 文件精确确认）'
                    findings.append(SupplyChainFinding(
                        category='known_cve', severity=severity,
                        message=msg,
                        suggestion=f'请升级 "{pkg}" 到安全版本，参考 {vid} 官方公告',
                        detail={'package': pkg, 'cve': vid,
                                'match_level': h['match_level'], 'approx': h['approx'],
                                'ecosystem': eco, 'data_point': data_point},
                    ))

        # Fallback: packages the offline index did not cover (network available).
        # Packages the index already knows (and judged safe) are excluded to avoid
        # re-introducing name-level false positives from the legacy local DB.
        known_safe = set()
        if _OSV_OFFLINE_AVAILABLE:
            try:
                known_safe = osv_index_known_packages(eco)
            except Exception:
                known_safe = set()
        unresolved = []
        for r in eco_records:
            norm = _normalize_pkg_name(r['name'])
            if r['name'] not in osv_hits and norm not in known_safe:
                unresolved.append(r['name'])
        unresolved = list(set(unresolved))
        if unresolved:
            try:
                cve_results = query_cve_database(list(unresolved), ecosystem=eco)
            except Exception:
                cve_results = {}
            for pkg, cves in cve_results.items():
                for cve_id in cves:
                    if (pkg, cve_id) in resolved_cves:
                        continue
                    resolved_cves.add((pkg, cve_id))
                    findings.append(SupplyChainFinding(
                        category='known_cve', severity='critical',
                        message=f'依赖包 "{pkg}" 存在已知 CVE: {cve_id}',
                        suggestion=f'请立即升级 "{pkg}" 到安全版本，参考 {cve_id} 官方公告',
                        detail={'package': pkg, 'cve': cve_id,
                                'match_level': 'name', 'approx': True,
                                'ecosystem': eco, 'data_point': 'api/nvd'},
                    ))

    # 3. Maintenance assessment (parallel, cached, rate-limited) - PyPI manifests
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {}
        for name in list(pypi_names)[:20]:  # Cap at 20 to be API-friendly
            fut = executor.submit(assess_maintenance, name, 'pypi', 24)
            futures[fut] = name
        for fut in as_completed(futures):
            pkg = futures[fut]
            try:
                status = fut.result()
                if status is None:
                    continue
                if status.get('deprecated'):
                    findings.append(SupplyChainFinding(
                        category='deprecated_package', severity='high',
                        message=f'依赖包 "{pkg}" 已被上游标记为弃用',
                        suggestion=f'请替换 "{pkg}" 为活跃维护的替代品',
                        detail=status,
                    ))
                last_date = status.get('last_release_date') or ''
                if last_date:
                    try:
                        dt = datetime.fromisoformat(last_date.replace('Z', '+00:00'))
                        age_days = (datetime.now() - dt.replace(tzinfo=None)).days
                        if age_days > 365 * 2:
                            findings.append(SupplyChainFinding(
                                category='unmaintained_package', severity='medium',
                                message=f'依赖包 "{pkg}" 已 {age_days // 365} 年未更新，可能为僵尸包',
                                suggestion=f'确认 "{pkg}" 是否仍在维护；如长期无更新请考虑替换',
                                detail={'age_days': age_days, 'last_release': last_date},
                            ))
                    except Exception:
                        pass
            except Exception:
                continue

    # 4. License compliance (parallel, cached) - PyPI manifests
    project_license = ''
    if frontmatter:
        project_license = frontmatter.get('license', '') or frontmatter.get('License', '')
    if project_license:
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {}
            for name in list(pypi_names)[:15]:  # Cap at 15 to be API-friendly
                fut = executor.submit(get_pypi_license, name, 72)
                futures[fut] = name
            for fut in as_completed(futures):
                pkg = futures[fut]
                try:
                    lic = fut.result()
                    if not lic:
                        continue
                    lic_str = lic.get('classifier_license') or lic.get('license_field') or ''
                    if not lic_str:
                        continue
                    ok, reason = check_license_compatibility(lic_str, project_license)
                    if not ok:
                        findings.append(SupplyChainFinding(
                            category='license_incompatible', severity='medium',
                            message=f'依赖包 "{pkg}" 许可证 "{lic_str}" 与项目 "{project_license}" 不兼容',
                            suggestion=f'替换为兼容许可证的依赖，或咨询法律团队确认使用合规性',
                            detail={'package': pkg, 'license': lic_str,
                                    'project_license': project_license, 'conflict': reason},
                        ))
                except Exception:
                    continue

    return findings
