"""
Registry metadata fetchers for npm, PyPI, and crates.io.
Returns a normalized dict or None if the package doesn't exist.
"""

from __future__ import annotations

import json
import urllib.request
import urllib.error
from datetime import datetime, timezone


def _fetch_json(url: str) -> dict | None:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "openclaw/0.1"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            return json.loads(resp.read())
    except Exception:
        return None


def _days_since(iso: str) -> int | None:
    """Return days since an ISO 8601 date string, or None if unparseable."""
    try:
        # Handle both 'Z' and '+00:00' suffixes
        ts = iso.replace("Z", "+00:00")
        dt = datetime.fromisoformat(ts)
        return (datetime.now(timezone.utc) - dt).days
    except Exception:
        return None


def get_npm_meta(name: str) -> dict | None:
    data = _fetch_json(f"https://registry.npmjs.org/{name}")
    if not data or "error" in data:
        return None

    time_data = data.get("time", {})
    created = time_data.get("created")
    # Latest published version
    dist_tags = data.get("dist-tags", {})
    latest = dist_tags.get("latest")
    latest_time = time_data.get(latest) if latest else None

    # Check for install scripts in latest version
    has_install_script = False
    if latest:
        version_data = data.get("versions", {}).get(latest, {})
        scripts = version_data.get("scripts", {})
        has_install_script = bool(scripts.get("preinstall") or scripts.get("postinstall") or scripts.get("install"))

    age_days = _days_since(created) if created else None
    latest_age_days = _days_since(latest_time) if latest_time else age_days

    return {
        "ecosystem": "npm",
        "name": name,
        "age_days": age_days,
        "latest_version_age_days": latest_age_days,
        "weekly_downloads": None,  # would need separate API call
        "has_install_script": has_install_script,
        "similar_to": None,  # populated by typosquat checker
    }


def get_pypi_meta(name: str) -> dict | None:
    data = _fetch_json(f"https://pypi.org/pypi/{name}/json")
    if not data:
        return None

    info = data.get("info", {})
    releases = data.get("releases", {})

    # Find the earliest release date across all versions
    earliest = None
    for version, files in releases.items():
        for f in files:
            upload_time = f.get("upload_time_iso_8601") or f.get("upload_time")
            if upload_time:
                dt = upload_time.replace("Z", "+00:00")
                if earliest is None or dt < earliest:
                    earliest = dt

    age_days = _days_since(earliest) if earliest else None

    return {
        "ecosystem": "pypi",
        "name": name,
        "age_days": age_days,
        "latest_version_age_days": None,
        "weekly_downloads": None,
        "has_install_script": False,  # PyPI doesn't expose this cleanly
        "similar_to": None,
    }


def get_crates_meta(name: str) -> dict | None:
    data = _fetch_json(f"https://crates.io/api/v1/crates/{name}")
    if not data or "crate" not in data:
        return None

    crate = data["crate"]
    created = crate.get("created_at")
    age_days = _days_since(created) if created else None

    return {
        "ecosystem": "crates",
        "name": name,
        "age_days": age_days,
        "latest_version_age_days": None,
        "weekly_downloads": crate.get("recent_downloads"),
        "has_install_script": False,
        "similar_to": None,
    }


def get_package_meta(name: str, ecosystem: str) -> dict | None:
    if ecosystem == "npm":
        return get_npm_meta(name)
    elif ecosystem == "pypi":
        return get_pypi_meta(name)
    elif ecosystem == "crates":
        return get_crates_meta(name)
    return None
