"""
osv_offline.py - OSV.dev offline vulnerability data package integration.

Merges OSV ecosystem exports (PyPI / npm) into the existing three-tier
offline cache so coverage jumps from the hardcoded 26-package table to the
full ecosystem, WITHOUT requiring any API key (zero-key gene preserved).

Design principles (per skill-security-checker dead rules):
  - Zero external API key: downloads OSV public exports over plain HTTPS.
  - Offline-first: scans read the compact local index; network is only used
    to (re)build the index when it is missing or older than MAX_AGE_DAYS.
  - Graceful degradation: any download/parse failure falls back to the
    existing OSV-API / NVD / local-26-entry chain in supply_chain.py.
  - Performance: the index is built once (periodic cache) and stored compact;
    per-scan lookups are pure in-memory dict reads.

Author: njskills@agent.qq.com
Version: 3.4.0
"""

import os
import re
import json
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# ============================================================
# Constants
# ============================================================

# OSV public per-ecosystem exports (no auth required).
OSV_EXPORT_URLS = {
    'pypi': 'https://osv-vulnerabilities.storage.googleapis.com/PyPI/all.json',
    'npm': 'https://osv-vulnerabilities.storage.googleapis.com/npm/all.json',
}

# How old the local index may be before a refresh is attempted (days).
MAX_AGE_DAYS = 7

# Compact index is stored OUTSIDE the repo (cache dir) so the skill package
# stays small and the forbidden-file-type rule is never violated.
def _index_cache_dir():
    base = Path.home() / '.workbuddy' / 'osv_offline_cache'
    base.mkdir(parents=True, exist_ok=True)
    return base


def _index_path(ecosystem):
    return _index_cache_dir() / f'osv_index_{ecosystem}.json'


# ============================================================
# Version comparison (PEP 440 / semver best-effort, zero-dep)
# ============================================================

_PRE_RELEASE_KEYS = {'a', 'b', 'rc', 'alpha', 'beta', 'pre', 'preview',
                     'c', 'dev', 'snapshot'}


def _split_prerelease(ver):
    """Return (release_str, prerelease_str_or_None).

    Handles both semver (`1.2.0-alpha`) and PEP 440 (`1.2.0a1`, `1.2.0rc1`)
    pre-release markers. A version WITH a pre-release is ordered LOWER than
    the same release without one.
    """
    ver = ver.strip().lower()
    # Strip local version (+xxx) and epoch (PEP 440 N!) — keep numeric compare simple.
    ver = re.split(r'[+!]', ver, maxsplit=1)[0]
    m = re.search(r'[._-]?(a|b|rc|c|alpha|beta|pre|preview|dev|snapshot)(?=\d|$)', ver)
    if m:
        cut = m.start()
        while cut > 0 and ver[cut - 1] in '._-':
            cut -= 1
        return ver[:cut], ver[cut:]
    return ver, None


def _parse_release(release):
    """Parse a dotted release string into a list of comparable parts."""
    parts = []
    for seg in release.split('.'):
        seg = seg.strip()
        if seg == '':
            parts.append(0)
            continue
        # Extract leading integer (handles '1', '12', '1.post2' loosely)
        m = re.match(r'(\d+)', seg)
        if m:
            parts.append(int(m.group(1)))
        else:
            # Non-numeric segment: keep as string for ordering
            parts.append(seg)
    return parts


def _parse_version_tuple(version):
    """Return (release_tuple, prerelease_flag) for ordering.

    A version WITH a pre-release is considered LOWER than the same release
    without one (semver / PEP 440 semantics).
    """
    if not version:
        return None
    release_str, pre = _split_prerelease(str(version))
    release = _parse_release(release_str)
    # Normalize length for comparison
    return release, pre is not None


def compare_versions(a, b):
    """Return -1 / 0 / 1 comparing two version strings, or None if undecidable."""
    ta = _parse_version_tuple(a)
    tb = _parse_version_tuple(b)
    if ta is None or tb is None:
        return None
    ra, pa = ta
    rb, pb = tb
    # Pad to equal length
    la = list(ra) + [0] * (max(len(ra), len(rb)) - len(ra))
    lb = list(rb) + [0] * (max(len(ra), len(rb)) - len(rb))
    # Compare release tuples element-wise
    for x, y in zip(la, lb):
        if isinstance(x, str) and isinstance(y, str):
            if x != y:
                return -1 if x < y else 1
        elif isinstance(x, str):
            return 1  # string > int (rare)
        elif isinstance(y, str):
            return -1
        else:
            if x != y:
                return -1 if x < y else 1
    # Release equal -> pre-release ordering
    if pa and not pb:
        return -1
    if not pa and pb:
        return 1
    return 0


def version_in_range(version, introduced, fixed, last_affected):
    """Check if `version` is affected by a range.

    Returns True / False, or None when the comparison is undecidable
    (caller then treats the package as a name-level potential hit).
    """
    if introduced is None and fixed is None and last_affected is None:
        return True
    ok = True
    if introduced is not None:
        c = compare_versions(version, introduced)
        if c is None:
            return None
        if c < 0:
            ok = False
    if fixed is not None:
        c = compare_versions(version, fixed)
        if c is None:
            return None
        if c >= 0:
            ok = False
    if last_affected is not None:
        c = compare_versions(version, last_affected)
        if c is None:
            return None
        if c > 0:
            ok = False
    return ok


# ============================================================
# Download + index build
# ============================================================

def _download_file(url, dest, timeout=60, max_bytes=None):
    """Stream-download `url` to `dest`. Returns True on success, False on failure.

    max_bytes guards against runaway downloads in constrained environments.
    """
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'skill-security-checker/3.4.0',
            'Accept': 'application/json',
        })
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            total = 0
            with open(dest, 'wb') as f:
                while True:
                    chunk = resp.read(1 << 20)  # 1 MB
                    if not chunk:
                        break
                    total += len(chunk)
                    if max_bytes and total > max_bytes:
                        return False
                    f.write(chunk)
        return True
    except Exception:
        return False


def _extract_ranges(affected):
    """Extract a list of normalized range dicts from one OSV `affected` entry."""
    out = []
    eco = affected.get('package', {}).get('ecosystem', '')
    name = affected.get('package', {}).get('name', '')
    for rng in affected.get('ranges', []):
        events = rng.get('events', [])
        introduced = None
        fixed = None
        last_affected = None
        for ev in events:
            if 'introduced' in ev:
                introduced = ev['introduced']
            if 'fixed' in ev:
                fixed = ev['fixed']
            if 'last_affected' in ev:
                last_affected = ev['last_affected']
        out.append({
            'ecosystem': eco,
            'introduced': introduced,
            'fixed': fixed,
            'last_affected': last_affected,
        })
    return name, out


def build_index_from_export(ecosystem, export_path):
    """Parse an OSV all.json export into a compact index.

    Returns: {pkg_name: [{'id': str, 'ranges': [...]}, ...]}
    """
    index = {}
    try:
        with open(export_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception:
        return index
    entries = data if isinstance(data, list) else data.get('vulns', [])
    wanted_eco = ecosystem.lower()
    for vuln in entries:
        vid = vuln.get('id') or vuln.get('aliases', [''])[0]
        if not vid:
            continue
        for affected in vuln.get('affected', []):
            pkg_eco = (affected.get('package', {}) or {}).get('ecosystem', '').lower()
            if pkg_eco and pkg_eco != wanted_eco:
                continue
            name, ranges = _extract_ranges(affected)
            if not name:
                continue
            norm = _normalize_pkg(name)
            index.setdefault(norm, []).append({
                'id': vid,
                'ranges': ranges,
            })
    return index


def _normalize_pkg(name):
    return re.sub(r'[-_.]+', '-', name.lower()).strip('-')


def ensure_osv_index(ecosystem, force=False, timeout=60, max_bytes=None):
    """Ensure a fresh compact index exists. Returns index path or None.

    - If a fresh (<= MAX_AGE_DAYS) index exists and force is False, reuse it.
    - Otherwise attempt to download the OSV export, build the compact index,
      and persist it. Any failure returns the existing index if present,
      else None (caller degrades to API/NVD/local).
    """
    eco = ecosystem.lower()
    if eco not in OSV_EXPORT_URLS:
        return None
    p = _index_path(eco)
    # Reuse if fresh
    if not force and p.exists():
        try:
            meta = json.loads(p.read_text(encoding='utf-8')).get('_meta', {})
            ts = meta.get('indexed_at_ts', 0)
            if time.time() - ts < MAX_AGE_DAYS * 86400:
                return p
        except Exception:
            pass
    # Attempt refresh
    url = OSV_EXPORT_URLS[eco]
    tmp = _index_cache_dir() / f'_dl_{eco}.json'
    ok = _download_file(url, tmp, timeout=timeout, max_bytes=max_bytes)
    if ok:
        try:
            index = build_index_from_export(eco, tmp)
            payload = {
                '_meta': {
                    'ecosystem': eco,
                    'indexed_at': datetime.now().isoformat(),
                    'indexed_at_ts': time.time(),
                    'source': 'osv-offline-export',
                    'package_count': len(index),
                },
                'index': index,
            }
            p.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
        except Exception:
            pass
        finally:
            try:
                tmp.unlink()
            except Exception:
                pass
    if p.exists():
        return p
    return None


def load_osv_index(ecosystem):
    """Load the compact index from cache. Returns (index_dict, meta) or (None, None)."""
    p = _index_path(ecosystem.lower())
    if not p.exists():
        return None, None
    try:
        data = json.loads(p.read_text(encoding='utf-8'))
        return data.get('index', {}), data.get('_meta', {})
    except Exception:
        return None, None


def get_index_timestamp(ecosystem):
    """Return the ISO timestamp the index was built, or None."""
    _, meta = load_osv_index(ecosystem)
    if meta:
        return meta.get('indexed_at')
    return None


def osv_index_known_packages(ecosystem):
    """Return the set of normalized package names present in the offline index.

    Used by the scanner to skip the name-level fallback for packages the index
    already judged safe (avoids re-introducing false positives from the legacy
    local-26-entry table).
    """
    index, _ = load_osv_index(ecosystem)
    if not index:
        return set()
    return set(index.keys())


# ============================================================
# Version-range aware query
# ============================================================

def query_osv_index(packages_with_versions, ecosystem):
    """Query the offline index with version ranges.

    packages_with_versions: list of (name, exact_version_or_None, approx_bool)
    Returns: {name: [{'id': str, 'match_level': 'exact'|'name',
                      'approx': bool}, ...]}
    """
    index, _ = load_osv_index(ecosystem)
    results = {}
    if not index:
        return results
    for name, version, approx in packages_with_versions:
        norm = _normalize_pkg(name)
        vulns = index.get(norm)
        if not vulns:
            continue
        hits = []
        for v in vulns:
            vid = v.get('id')
            ranges = v.get('ranges', [])
            if not version:
                # No concrete version -> name-level potential hit only
                hits.append({'id': vid, 'match_level': 'name', 'approx': bool(approx)})
                continue
            matched = False
            uncertain = False
            for rng in ranges:
                res = version_in_range(version, rng.get('introduced'),
                                       rng.get('fixed'), rng.get('last_affected'))
                if res is True:
                    matched = True
                    break
                if res is None:
                    uncertain = True
            if matched:
                hits.append({'id': vid, 'match_level': 'exact', 'approx': bool(approx)})
            elif uncertain:
                hits.append({'id': vid, 'match_level': 'name', 'approx': bool(approx)})
        if hits:
            results[name] = hits
    return results


if __name__ == '__main__':
    # Manual index build (offline-first). Pass ecosystem as argv[1].
    import sys
    eco = sys.argv[1] if len(sys.argv) > 1 else 'pypi'
    path = ensure_osv_index(eco, force=True)
    if path:
        _, meta = load_osv_index(eco)
        print(f"Index ready: {path} ({meta.get('package_count')} packages, "
              f"indexed_at={meta.get('indexed_at')})")
    else:
        print(f"Failed to build index for {eco}")
