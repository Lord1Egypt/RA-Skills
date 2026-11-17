"""Stable, collision-resistant local state paths for HaloArena clients."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from urllib import request
from urllib.parse import urlparse


STATE_OWNER_FILENAME = "state_owner.json"


class _NoAPIRedirect(request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # The Agent API has no redirect contract. Preserve the original HTTP
        # error/status without forwarding either authorization or secret bodies.
        return None


_API_OPENER = request.build_opener(_NoAPIRedirect())


def api_urlopen(req, *, timeout):
    return _API_OPENER.open(req, timeout=timeout)


def validated_api_base(api_base: str) -> str:
    value = normalized_arena_base(api_base)
    try:
        parsed = urlparse(value)
        valid = (
            bool(parsed.hostname)
            and parsed.username is None and parsed.password is None
            and not parsed.query and not parsed.fragment and not parsed.params
            and not any(character.isspace() or ord(character) < 32 for character in value)
            and "\\" not in value
            and (parsed.scheme == "https" or (
                parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "::1", "localhost"}
            ))
        )
        parsed.port  # Reject malformed/out-of-range ports before reading credentials.
    except ValueError:
        valid = False
    if not valid:
        raise ValueError("HaloArena API base must be an HTTPS URL without userinfo, query, or fragment (HTTP is allowed only on loopback).")
    return value


def normalized_arena_base(api_base: str) -> str:
    return str(api_base or "").strip().rstrip("/")


def arena_scope(api_base: str) -> str:
    normalized = normalized_arena_base(api_base)
    parsed = urlparse(normalized)
    identity = f"{parsed.scheme}-{parsed.netloc}" if parsed.netloc else normalized
    slug = re.sub(r"[^a-z0-9]+", "-", identity.lower()).strip("-") or "arena"
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:8]
    return f"{slug[:48]}-{digest}"


def namespaced_state_home(api_base: str, runtime_kind: str, *, root: Path) -> Path:
    return root / "instances" / arena_scope(api_base) / runtime_kind


def runtime_state_home(api_base: str, runtime_kind: str, *, root: Path) -> Path:
    """Resolve state while preserving the managed-runtime volume contract."""
    configured = str(os.environ.get("CLAWARENA_HOME") or "").strip()
    if configured:
        return Path(configured).expanduser()
    if (
        str(os.environ.get("CLAWARENA_RUNTIME_KIND") or "").strip() == runtime_kind
        and str(os.environ.get("CLAWARENA_RUNTIME_ID") or "").strip()
    ):
        # Existing managed OpenClaw images write their mounted credential to
        # ~/.clawarena/token. Keep that isolated container contract compatible
        # while self-hosted installs use arena-scoped state by default.
        return root
    return namespaced_state_home(api_base, runtime_kind, root=root)


def state_owner(api_base: str, runtime_kind: str) -> dict[str, object]:
    return {
        "schema_version": 1,
        "arena_base": normalized_arena_base(api_base),
        "runtime_kind": runtime_kind,
    }


def read_state_owner(home: Path) -> dict[str, object]:
    try:
        payload = json.loads((home / STATE_OWNER_FILENAME).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return payload if isinstance(payload, dict) else {}


def validate_state_owner(home: Path, api_base: str, runtime_kind: str) -> None:
    owner = read_state_owner(home)
    if not owner:
        return
    expected = state_owner(api_base, runtime_kind)
    if (
        owner.get("arena_base") != expected["arena_base"]
        or owner.get("runtime_kind") != expected["runtime_kind"]
    ):
        raise RuntimeError(
            f"HaloArena state directory {home} belongs to "
            f"{owner.get('runtime_kind') or 'another runtime'} at "
            f"{owner.get('arena_base') or 'another arena'}. Use its generated "
            "default path or choose a different explicit state directory."
        )


def state_owner_matches(home: Path, api_base: str, runtime_kind: str) -> bool:
    """Require positive local ownership evidence before migrating credentials."""
    owner = read_state_owner(home)
    expected = state_owner(api_base, runtime_kind)
    return bool(owner) and all(owner.get(key) == expected[key] for key in ("arena_base", "runtime_kind"))
