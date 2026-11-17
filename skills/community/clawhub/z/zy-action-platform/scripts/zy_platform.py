#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
zy_platform.py — ZY Action Platform WorkBuddy skill client (pure standard library, zero third-party deps).

Call the REST API of a local or remote ZY Action Platform deployment from WorkBuddy
(or any terminal). Supports five products: aip(18080)/foundry(18081)/apollo(18082)/gotham(18083)/swift(18084).

Usage examples:
  python zy_platform.py health --product aip
  python zy_platform.py login --product foundry --username admin --dry-run     # preview normalized destination
  python zy_platform.py login --product foundry --username admin --password '******'
  python zy_platform.py logout --product foundry                               # remove cached token for this origin
  python zy_platform.py chat --product aip --query 'Top 5 sales by region'
  python zy_platform.py ontology-search --product foundry --query 'items below reorder point'
  python zy_platform.py search --product gotham --query 'orders'
  python zy_platform.py request --product foundry --method GET --path='metrics/catalog'
  python zy_platform.py request --product aip --method POST --path=chat --data '{"query":"..."}' \
      --allow-write                       # write methods need explicit consent, preview with --dry-run first
  python zy_platform.py verify-artifact --file ZY-Action-Platform_v2026.09.rar \
      --sha256 <SHA-256 from the official release page>   # verify installer before execution

Security contract (enforced by the script, not advisory):
  * Transport: every non-loopback destination must be https; remote plaintext http is
    always rejected. http is allowed only for 127.0.0.1/::1/localhost. Destinations are
    parsed with urllib.parse.urlsplit; --base-url carrying userinfo (user:pass@host),
    fragments (#) or query strings is rejected.
  * First contact with a non-loopback origin requires explicit --trust-host confirmation
    (recorded into the local trusted-origin list; revoke with logout --forget-host).
  * Token binding: cached tokens are strictly bound to the tuple
    scheme|host|port|product|api-root. When the current request origin differs from the
    cached origin, the token is NOT attached automatically; re-login or pass --token.
  * Redirects: cross-origin redirects are always blocked; same-origin redirects keep
    Authorization, cross-origin never carries it.
  * Before sending credentials: login/--dry-run prints the normalized destination first;
    the real login prints it to stderr as well.
  * Storage: tokens prefer the OS credential store (optional keyring module); otherwise
    fall back to ~/.workbuddy/zy_action_session.json (dir 0700 / file 0600 / atomic
    replacement via temp file / symlinks rejected / ownership verified on POSIX).
    Only the token and binding metadata are stored — no usernames. Expired entries are
    purged automatically on read/write.
  * Pass-through (request): GET/HEAD only by default; POST/PUT/PATCH/DELETE require
    explicit --allow-write; methods are restricted to a fixed set; paths go through a
    sensitive-segment denylist plus a read-only family allowlist (writes allowed only in
    chat / ontology/semantic-search); cached tokens are never attached automatically —
    use --with-token after explicit user consent (or pass --token). Approved write
    requests and login/logout are recorded to ~/.workbuddy/zy_action_audit.log
    (no credentials, no tokens).
  * Downloaded artifacts: always run verify-artifact (SHA-256) and verify the digital
    signature before executing an installer.

Conventions:
  * --base-url defaults to http://127.0.0.1:<product port>; a gateway form ending in
    "/v1" (e.g. http://127.0.0.1/aip-api/v1) is treated as the full API root, otherwise
    it is treated as the server root and /api/v1 is appended automatically.
  * Everything except health/login needs a login token; token priority: --token > local
    session cache.
  * Exit codes: 0 success / 1 argument error or local/security-policy refusal /
            2 network unreachable or timeout (including certificate failure) /
            3 HTTP error (4xx/5xx, non-401) / 4 auth failure (401, re-login) /
            5 business envelope code!=0.
  * No hardcoded accounts, passwords or keys; stdout prints JSON only, notices go to stderr.
"""

import argparse
import base64
import hashlib
import ipaddress
import json
import os
import posixpath
import re
import ssl
import stat
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:  # optional: OS credential store (Windows Credential Manager / macOS Keychain / Linux Secret Service)
    import keyring
except Exception:
    keyring = None

PRODUCTS = {
    "aip":     {"port": 18080, "name": "LightAIP NLQ data query"},
    "foundry": {"port": 18081, "name": "LightFoundry data integration/ontology"},
    "apollo":  {"port": 18082, "name": "LightApollo deployment platform"},
    "gotham":  {"port": 18083, "name": "LightGotham intelligence analysis"},
    "swift":   {"port": 18084, "name": "LightSwift onboard settlement"},
}

KEYRING_SERVICE = "zy-action-platform"
# Session directory: ~/.workbuddy by default; tests may isolate via ZY_WORKBUDDY_HOME
_SESSION_DIR_OVERRIDE = os.environ.get("ZY_WORKBUDDY_HOME")
SESSION_DIR = Path(_SESSION_DIR_OVERRIDE) if _SESSION_DIR_OVERRIDE \
    else Path.home() / ".workbuddy"
SESSION_FILE = SESSION_DIR / "zy_action_session.json"
AUDIT_FILE = SESSION_DIR / "zy_action_audit.log"
DEFAULT_TIMEOUT = 25
MAX_AGE_NO_EXP = 24 * 3600        # conservative max cache age when the login response has no exp claim
EXPIRY_SKEW = 30                  # treat tokens as expired 30s before their exp
MAX_BODY_BYTES = 20 * 1024 * 1024
AUDIT_MAX_BYTES = 2 * 1024 * 1024
USER_AGENT = "zy_platform/1.1.0"

# product -> curated subcommands (generic commands health/login/logout/me/request excluded)
ALLOW = {
    "aip":     {"datasource-list", "chat", "workflow-list", "workflow-run",
                "workflow-status", "workflow-cancel", "audit-list"},
    "foundry": {"datasource-list", "dataset-list", "dataset-preview",
                "ontology-objects", "ontology-search", "metric-list",
                "dashboard-list", "report-list"},
    "apollo":  {"apollo-docs", "desired-state-list", "deployment-list",
                "deployment-status", "drift-list", "bundle-list", "agent-list"},
    "gotham":  {"search", "graph-nodes", "graph-stats", "entity-list",
                "timeline-events", "map-features", "report-list"},
    "swift":   set(),
}

COMMAND_INTRO = {
    "health":             "check product health (public)",
    "login":              "log in and cache token (username/password; --dry-run to preview destination)",
    "logout":             "log out and securely remove cached tokens (--all; --forget-host revokes trusted origins)",
    "me":                 "return current logged-in user (AIP/Apollo)",
    "datasource-list":    "list datasources (AIP/Foundry)",
    "chat":               "NLQ natural-language data query (AIP)",
    "workflow-list":      "list automation workflows (AIP)",
    "workflow-run":       "run a workflow once (AIP, --workflow-id, optional --params)",
    "workflow-status":    "query execution result (AIP, --execution-id)",
    "workflow-cancel":    "cancel an execution (AIP, --execution-id)",
    "audit-list":         "audit logs (AIP admin)",
    "dataset-list":       "dataset list (Foundry)",
    "dataset-preview":    "dataset row preview (Foundry, --dataset-id)",
    "ontology-objects":   "ontology object types (Foundry)",
    "ontology-search":    "ontology semantic search (Foundry, --query)",
    "metric-list":        "metric list (Foundry)",
    "dashboard-list":     "dashboard list (Foundry)",
    "report-list":        "report list (Foundry/Gotham)",
    "search":             "global search (Gotham, --query)",
    "graph-nodes":        "knowledge-graph nodes (Gotham)",
    "graph-stats":        "graph statistics (Gotham)",
    "entity-list":        "multi-source resolved entities (Gotham)",
    "timeline-events":    "timeline events (Gotham)",
    "map-features":       "map features (Gotham)",
    "apollo-docs":        "Apollo API docs introspection (public)",
    "desired-state-list": "desired-state list (Apollo)",
    "deployment-list":    "deployment list (Apollo)",
    "deployment-status":  "deployment details (Apollo, --deployment-id)",
    "drift-list":         "drift events (Apollo)",
    "bundle-list":        "bundle artifact list (Apollo)",
    "agent-list":         "Spoke Agent node list (Apollo)",
    "request":            "read-only generic pass-through: --method GET/HEAD --path=datasets?limit=5; writes need --allow-write",
    "verify-artifact":    "verify downloaded artifact SHA-256: --file <path> --sha256 <official value>",
}

# business endpoints: method + path_template ({} placeholders filled from args)
ENDPOINTS = {
    "health":             ("GET",  "/health"),
    "login":              ("POST", "/api/v1/auth/login"),
    "me":                 ("GET",  "/api/v1/me"),
    "datasource-list":    ("GET",  "/api/v1/datasources"),
    "chat":               ("POST", "/api/v1/chat"),
    "workflow-list":      ("GET",  "/api/v1/workflows"),
    "workflow-run":       ("POST", "/api/v1/workflows/{workflow_id}/run"),
    "workflow-status":    ("GET",  "/api/v1/workflows/executions/{execution_id}"),
    "workflow-cancel":    ("POST", "/api/v1/workflows/executions/{execution_id}/cancel"),
    "audit-list":         ("GET",  "/api/v1/audit/logs"),
    "dataset-list":       ("GET",  "/api/v1/datasets"),
    "dataset-preview":    ("GET",  "/api/v1/datasets/{dataset_id}/preview"),
    "ontology-objects":   ("GET",  "/api/v1/ontology/objects"),
    "ontology-search":    ("POST", "/api/v1/ontology/semantic-search"),
    "metric-list":        ("GET",  "/api/v1/metrics"),
    "dashboard-list":     ("GET",  "/api/v1/dashboards"),
    "report-list":        ("GET",  "/api/v1/reports"),
    "search":             ("GET",  "/api/v1/search"),
    "graph-nodes":        ("GET",  "/api/v1/graph/nodes"),
    "graph-stats":        ("GET",  "/api/v1/graph/stats"),
    "entity-list":        ("GET",  "/api/v1/ingestion/entities"),
    "timeline-events":    ("GET",  "/api/v1/timeline/events"),
    "map-features":       ("GET",  "/api/v1/map/features"),
    "apollo-docs":        ("GET",  "/api/v1/docs"),
    "desired-state-list": ("GET",  "/api/v1/desired-states"),
    "deployment-list":    ("GET",  "/api/v1/deployments"),
    "deployment-status":  ("GET",  "/api/v1/deployments/{deployment_id}"),
    "drift-list":         ("GET",  "/api/v1/drift/events"),
    "bundle-list":        ("GET",  "/api/v1/bundles"),
    "agent-list":         ("GET",  "/api/v1/agents"),
}

PUBLIC_COMMANDS = {"health"}          # no token needed

# ---------------------------------------------------------------------------
# Pass-through (request) policy
# ---------------------------------------------------------------------------
ALLOWED_METHODS = ("GET", "HEAD", "POST", "PUT", "PATCH", "DELETE")
SAFE_METHODS = ("GET", "HEAD")
# sensitive/admin route segments (any path segment matching exactly → rejected, case-insensitive)
DENY_SEGMENTS = {
    "auth", "register", "password", "passwd", "users", "user", "admin",
    "administrator", "rbac", "roles", "permissions", "config", "settings",
    "license", "system", "database", "databases", "sql", "exec", "execute",
    "debug", "internal", "actuator", "tokens", "keys", "secrets", "sessions",
}
# read-only allowlist: any path segment matching → GET/HEAD allowed
READ_PASS_THROUGH_FAMILIES = {
    "datasets", "metrics", "ontology", "dashboards", "reports", "search",
    "graph", "timeline", "map", "entities", "ingestion", "workflows",
    "executions", "datasources", "deployments", "drift", "bundles", "agents",
    "desired-states", "docs", "audit", "catalog", "nexus", "charts", "sync",
    "events", "nodes", "stats", "features", "objects", "preview",
}
# write allowlist: only these first-segment families (other writes → use built-in commands)
WRITE_PASS_THROUGH_FAMILIES = {"chat", "ontology"}

# ---------------------------------------------------------------------------
# Origin parsing: scheme|host|port|product|api_path tuple
# ---------------------------------------------------------------------------
KNOWN_API_SUFFIXES = ("/aip-api/v1", "/apollo-api/v1", "/gotham-api/v1",
                      "/swift-api/v1", "/api/v1")


class _OriginError(Exception):
    """--base-url parse failure (converted to exit 1 when strict=True)."""


class Origin(object):
    __slots__ = ("scheme", "host", "port", "api_path", "product")

    def __init__(self, scheme, host, port, api_path, product):
        self.scheme = scheme
        self.host = host
        self.port = port
        self.api_path = api_path
        self.product = product

    @property
    def netloc(self):
        host = self.host
        if ":" in host:                      # IPv6 literal
            host = "[" + host + "]"
        default = 443 if self.scheme == "https" else 80
        if self.port != default:
            return "{}:{}".format(host, self.port)
        return host

    def api_root(self):
        return "{}://{}{}".format(self.scheme, self.netloc, self.api_path)

    def server_root(self):
        for s in KNOWN_API_SUFFIXES:
            if self.api_path.endswith(s):
                rest = self.api_path[: -len(s)]
                return "{}://{}{}".format(self.scheme, self.netloc, rest)
        return self.api_root()

    def key(self):
        return "|".join([self.scheme, self.host, str(self.port),
                         self.product, self.api_path])


def _is_loopback_host(host):
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return host == "localhost"


def parse_origin(raw, product, strict=True):
    """Parse --base-url into an Origin. With strict=False invalid input returns None (migration)."""
    try:
        return _parse_origin_impl(raw, product)
    except _OriginError as e:
        if strict:
            fail(1, str(e))
        return None


def _parse_origin_impl(raw, product):
    if raw is None or not str(raw).strip():
        return Origin("http", "127.0.0.1", PRODUCTS[product]["port"], "/api/v1", product)
    raw = str(raw).strip()
    if re.search(r"[\s\x00-\x1f\x7f]", raw):
        raise _OriginError("--base-url contains whitespace/control characters; refused.")
    parts = urllib.parse.urlsplit(raw)
    if parts.scheme not in ("http", "https"):
        raise _OriginError("--base-url must start with http:// or https:// (remote hosts must use https).")
    if parts.username is not None or parts.password is not None:
        raise _OriginError("security policy: --base-url must not carry userinfo (user:pass@host form).")
    if parts.fragment:
        raise _OriginError("security policy: --base-url must not contain a fragment (#).")
    if parts.query:
        raise _OriginError("security policy: --base-url must not contain a query string (?).")
    host = (parts.hostname or "").rstrip(".").lower()
    if not host:
        raise _OriginError("--base-url is missing a hostname.")
    try:
        port = parts.port
    except ValueError:
        raise _OriginError("--base-url has an invalid port.")
    if port is None:
        port = 443 if parts.scheme == "https" else 80
    path = urllib.parse.unquote(parts.path or "")
    norm = posixpath.normpath(path) if path else ""
    if norm in (".", "/"):
        norm = ""
    if norm and not norm.startswith("/"):
        norm = "/" + norm
    if ".." in norm.split("/") or "|" in norm or "\\" in norm:
        raise _OriginError("--base-url path is invalid (.., |, backslash not allowed).")
    loopback = _is_loopback_host(host)
    if parts.scheme == "http" and not loopback:
        raise _OriginError(
            "security policy: http is only allowed for loopback addresses "
            "(127.0.0.1/::1/localhost); remote host {} must use https.".format(host))
    if norm and any(norm == s or norm.endswith(s) for s in KNOWN_API_SUFFIXES):
        api_path = norm
    else:
        api_path = norm + "/api/v1"
    return Origin(parts.scheme, host, port, api_path, product)


def _origin_from_key(key):
    parts = key.split("|")
    if len(parts) != 5:
        return None
    scheme, host, port, product, api_path = parts
    if scheme not in ("http", "https") or not host or not port.isdigit():
        return None
    if product not in PRODUCTS or not api_path.startswith("/"):
        return None
    return Origin(scheme, host, int(port), api_path, product)


# ---------------------------------------------------------------------------
# Local storage: dir 0700 / file 0600 / atomic replace / no symlinks / owner check
# ---------------------------------------------------------------------------
def _reject_symlink(path, what):
    try:
        st = os.lstat(str(path))
    except OSError:
        return
    if stat.S_ISLNK(st.st_mode):
        fail(1, "security policy: {} is a symlink; refused ({}).".format(what, path))
    fattr = getattr(st, "st_file_attributes", 0)
    if fattr and (fattr & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)):
        fail(1, "security policy: {} is a reparse point (junction/symlink); refused ({}).".format(what, path))


def _enforce_owner(path, what):
    if os.name != "posix":
        return
    try:
        st = os.stat(str(path))
    except OSError:
        return
    if st.st_uid != os.getuid():
        fail(1, "security policy: {} is not owned by the current user; refused ({}).".format(what, path))


def _harden_perms(path, is_dir):
    """Best-effort permission tightening; on Windows use icacls to drop inheritance and keep only the current user."""
    try:
        os.chmod(str(path), 0o700 if is_dir else 0o600)
    except OSError:
        pass
    if os.name == "nt":
        user = os.environ.get("USERNAME") or ""
        if user:
            try:
                subprocess.run(["icacls", str(path), "/inheritance:r",
                                "/grant:r", user + ":F"],
                               capture_output=True, timeout=10)
            except Exception:
                pass


def _ensure_session_dir():
    try:
        SESSION_DIR.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        fail(1, "cannot create session directory {}: {}".format(SESSION_DIR, e))
    _reject_symlink(SESSION_DIR, "session directory")
    _enforce_owner(SESSION_DIR, "session directory")
    _harden_perms(SESSION_DIR, is_dir=True)


def _tighten_before_read(path):
    """Fix insecure permissions of existing files before read/write (tighten to 0600 if group/other bits set)."""
    try:
        mode = os.stat(str(path)).st_mode
    except OSError:
        return
    if mode & 0o077:
        _harden_perms(path, is_dir=False)


def _atomic_write_private(path, text):
    _ensure_session_dir()
    _reject_symlink(path, path.name)
    fd, tmp = tempfile.mkstemp(prefix=".zytmp-", dir=str(SESSION_DIR))
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            fd = None
            f.write(text)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, str(path))
        tmp = None
    finally:
        if fd is not None:
            try:
                os.close(fd)
            except OSError:
                pass
        if tmp is not None:
            try:
                os.unlink(tmp)
            except OSError:
                pass
    _harden_perms(path, is_dir=False)


# ---------------------------------------------------------------------------
# Session cache (v2): tokens bound to the origin tuple; expired purged; minimal data
# ---------------------------------------------------------------------------
def _jwt_expires_at(token):
    """Parse exp from the JWT payload; return None when unavailable."""
    try:
        part = token.split(".")[1]
        part += "=" * (-len(part) % 4)
        data = json.loads(base64.urlsafe_b64decode(part.encode("ascii")))
        exp = data.get("exp")
        if isinstance(exp, (int, float)) and exp > 0:
            return int(exp)
    except Exception:
        pass
    return None


def _keyring_set(key, token):
    if keyring is None:
        return False
    try:
        keyring.set_password(KEYRING_SERVICE, key, token)
        return True
    except Exception:
        return False


def _keyring_get(key):
    if keyring is None:
        return None
    try:
        return keyring.get_password(KEYRING_SERVICE, key)
    except Exception:
        return None


def _delete_keyring_secret(key):
    if keyring is None:
        return
    try:
        keyring.delete_password(KEYRING_SERVICE, key)
    except Exception:
        pass


def _migrate_v1(data):
    """Migrate the legacy format (product -> {token,username,base,time}); drop entries that cannot be safely verified."""
    tokens = {}
    now = int(time.time())
    for product, entry in (data or {}).items():
        if product not in PRODUCTS or not isinstance(entry, dict):
            continue
        token = entry.get("token")
        if not isinstance(token, str) or not token:
            continue
        origin = parse_origin(entry.get("base"), product, strict=False)
        if origin is None:      # remote plaintext http etc. cannot be verified safely → drop
            continue
        created = int(entry.get("time") or 0)
        exp = _jwt_expires_at(token) or (created + MAX_AGE_NO_EXP)
        if exp <= now + EXPIRY_SKEW:
            continue
        tokens[origin.key()] = {"token": token, "keyring": False,
                                "created_at": created, "expires_at": exp}
    if tokens:
        sys.stderr.write("[zy_platform] Legacy session cache detected; migrated to the new format "
                         "(tokens are strictly origin-bound, usernames are no longer stored).\n")
    return tokens


def load_store():
    store = {"version": 2, "tokens": {}, "trusted_origins": []}
    if not SESSION_FILE.exists():
        return store
    _reject_symlink(SESSION_FILE, "session file")
    _enforce_owner(SESSION_FILE, "session file")
    _tighten_before_read(SESSION_FILE)
    try:
        raw = SESSION_FILE.read_text(encoding="utf-8")
        data = json.loads(raw) if raw.strip() else {}
    except Exception:
        return store                     # do not overwrite a corrupted file; treat as empty
    if not isinstance(data, dict):
        return store
    now = int(time.time())
    changed = False
    tokens = data.get("tokens")
    if not isinstance(tokens, dict) and data:
        tokens = _migrate_v1(data)
        changed = True
    for key, entry in (tokens or {}).items():
        if not isinstance(key, str) or _origin_from_key(key) is None \
                or not isinstance(entry, dict):
            changed = True
            continue
        if not isinstance(entry.get("expires_at"), int) \
                or entry["expires_at"] <= now + EXPIRY_SKEW:
            _delete_keyring_secret(key)  # purge the credential-store secret along with the entry
            changed = True
            continue
        store["tokens"][key] = {
            "token": entry["token"] if isinstance(entry.get("token"), str) else None,
            "keyring": bool(entry.get("keyring")),
            "created_at": int(entry.get("created_at") or 0),
            "expires_at": entry["expires_at"],
        }
    trusted = data.get("trusted_origins")
    if isinstance(trusted, list):
        store["trusted_origins"] = [t for t in trusted
                                    if isinstance(t, str) and _origin_from_key(t)]
    if changed:
        try:
            save_store(store)
        except Exception:
            pass
    return store


def save_store(store):
    _atomic_write_private(SESSION_FILE,
                          json.dumps(store, ensure_ascii=False, indent=2))


def store_get_token(args, origin):
    """Token lookup for built-in commands: explicit --token > cache (strict origin-tuple binding)."""
    if args.token:
        return args.token
    if args.no_cache:
        return None
    store = load_store()
    key = origin.key()
    entry = store["tokens"].get(key)
    if entry:
        token = _keyring_get(key) if entry["keyring"] else entry["token"]
        if token:
            return token
        store["tokens"].pop(key, None)
        try:
            save_store(store)
        except Exception:
            pass
    other = [k for k, e in store["tokens"].items()
             if e.get("token") or e.get("keyring")]
    other = [k for k in other if _origin_from_key(k)
             and _origin_from_key(k).product == origin.product]
    if other:
        sys.stderr.write(
            "[zy_platform] security notice: the cached token is bound to a different origin ({}) "
            "than the requested one ({}); it will NOT be attached automatically. "
            "Re-login for this origin or pass --token explicitly.\n".format(
                ", ".join(other), key))
    return None


def store_set_token(origin, token):
    key = origin.key()
    now = int(time.time())
    exp = _jwt_expires_at(token) or (now + MAX_AGE_NO_EXP)
    entry = {"token": None, "keyring": False, "created_at": now, "expires_at": exp}
    if _keyring_set(key, token):
        entry["keyring"] = True
        storage = "keyring"
    else:
        entry["token"] = token
        storage = "file"
        sys.stderr.write(
            "[zy_platform] no usable OS credential store detected (install the python keyring "
            "module to enable); token stored in the hardened fallback file "
            "(dir 0700 / file 0600 / atomic replacement).\n")
    store = load_store()
    store["tokens"][key] = entry
    save_store(store)
    return {"storage": storage, "expires_at": exp, "expires_in": max(exp - now, 0)}


def store_clear(origin=None):
    """Remove cached tokens; origin=None clears all. Returns the number removed."""
    store = load_store()
    keys = list(store["tokens"]) if origin is None else \
        [origin.key()] if origin.key() in store["tokens"] else []
    for key in keys:
        _delete_keyring_secret(key)
        store["tokens"].pop(key, None)
    if keys:
        save_store(store)
    return len(keys)


def forget_host(origin):
    store = load_store()
    key = origin.key()
    if key in store["trusted_origins"]:
        store["trusted_origins"].remove(key)
        save_store(store)
        return 1
    return 0


def ensure_trusted(args, origin):
    """First contact with a non-loopback origin requires explicit --trust-host confirmation (loopback passes)."""
    if _is_loopback_host(origin.host):
        return
    store = load_store()
    if origin.key() in store["trusted_origins"]:
        return
    if getattr(args, "trust_host", False):
        store["trusted_origins"].append(origin.key())
        save_store(store)
        audit_event("trust-host", origin=origin.key())
        sys.stderr.write("[zy_platform] {} recorded into the local trusted-origin list (--trust-host); "
                         "revoke with logout --forget-host.\n".format(origin.api_root()))
        return
    fail(1, "security policy: first contact with the remote origin {} requires explicit confirmation. "
            "Show this normalized address to the user and, after informed consent, re-run with --trust-host; "
            "the origin will then be remembered locally.".format(origin.api_root()))


# ---------------------------------------------------------------------------
# Local audit log (no credentials, no tokens)
# ---------------------------------------------------------------------------
_SENSITIVE_KEY_RE = re.compile(
    r"pass(word|wd)?|secret|token|credential|api[_-]?key|authorization", re.I)


def _redact(obj):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if isinstance(k, str) and _SENSITIVE_KEY_RE.search(k):
                out[k] = "***"
            else:
                out[k] = _redact(v)
        return out
    if isinstance(obj, list):
        return [_redact(x) for x in obj]
    return obj


def audit_event(event, **fields):
    rec = {"ts": time.strftime("%Y-%m-%dT%H:%M:%S"), "event": event}
    rec.update(fields)
    try:
        _ensure_session_dir()
        _reject_symlink(AUDIT_FILE, "audit log")
        try:
            if AUDIT_FILE.stat().st_size > AUDIT_MAX_BYTES:
                os.replace(str(AUDIT_FILE), str(AUDIT_FILE) + ".1")
        except OSError:
            pass
        with open(str(AUDIT_FILE), "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        _harden_perms(AUDIT_FILE, is_dir=False)
    except Exception:
        pass                              # audit failure must not block the main flow


# ---------------------------------------------------------------------------
# HTTP: block cross-origin redirects; re-attach Authorization on same-origin hops only
# ---------------------------------------------------------------------------
class _CrossOriginRedirect(Exception):
    pass


class _StrictRedirectHandler(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        old = urllib.parse.urlsplit(req.full_url)
        new = urllib.parse.urlsplit(urllib.parse.urljoin(req.full_url, newurl))

        def norm(sp):
            if sp.scheme == "https":
                dport = 443
            elif sp.scheme == "http":
                dport = 80
            else:
                dport = None
            return (sp.scheme, (sp.hostname or "").rstrip(".").lower(),
                    sp.port or dport)

        if norm(new) != norm(old):
            raise _CrossOriginRedirect("{} -> {}".format(req.full_url, newurl))
        nreq = super().redirect_request(req, fp, code, msg, headers, newurl)
        if nreq is not None:
            auth = req.headers.get("Authorization")
            nreq.headers.pop("Authorization", None)
            if auth:                      # only same-origin redirects reach here
                nreq.add_header("Authorization", auth)
        return nreq


_OPENER = urllib.request.build_opener(_StrictRedirectHandler())


def _extract_message(obj):
    if isinstance(obj, dict):
        for k in ("message", "error", "detail", "msg", "trace"):
            if isinstance(obj.get(k), str) and obj[k]:
                return obj[k]
        data = obj.get("data")
        if isinstance(data, dict) and not data:
            return None
    return None


def http_call(method, url, payload=None, token=None, timeout=DEFAULT_TIMEOUT):
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ("http", "https") or parts.username \
            or parts.password or parts.fragment:
        fail(1, "security policy: invalid target URL ({}).".format(url))
    body = None
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, method=method)
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", USER_AGENT)
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with _OPENER.open(req, timeout=timeout) as resp:
            raw = resp.read(MAX_BODY_BYTES + 1).decode("utf-8", errors="replace")
            if len(raw.encode("utf-8", errors="replace")) > MAX_BODY_BYTES:
                fail(3, "response body exceeds the {}MB limit; refused to read.".format(
                    MAX_BODY_BYTES // (1024 * 1024)))
            obj = json.loads(raw) if raw.strip() else {}
            return resp.status, obj
    except _CrossOriginRedirect as e:
        fail(3, "security policy: cross-origin redirect blocked ({}). Contact the final address directly.".format(e))
    except urllib.error.HTTPError as e:
        raw = e.read(MAX_BODY_BYTES + 1).decode("utf-8", errors="replace")
        try:
            obj = json.loads(raw) if raw.strip() else {}
        except Exception:
            obj = {"error": raw[:200]}
        return e.code, obj
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        reason = getattr(e, "reason", None)
        cert_err = getattr(ssl, "SSLCertVerificationError", None)
        if cert_err is not None and isinstance(reason, cert_err):
            fail(2, "HTTPS certificate verification failed ({}): remote hosts must present a valid "
                    "certificate; self-signed/expired/mismatched certificates are rejected.".format(reason))
        fail(2, "network error, cannot reach {}: {}. Confirm the platform is running "
                "(launch 'Run ZY Action System' exe) and that --base-url/--product are correct.".format(url, e))
    except json.JSONDecodeError:
        fail(2, "response is not valid JSON: {}".format(url))
    return None, None  # unreachable


def emit(obj, args):
    kwargs = {"ensure_ascii": False}
    if args.pretty:
        kwargs["indent"] = 2
    print(json.dumps(obj, **kwargs))


def fail(rc, msg):
    print("[zy_platform] " + msg, file=sys.stderr)
    sys.exit(rc)


def check_business(obj, args):
    """Business envelope {code,message,data} check; bare JSON is treated as success."""
    if isinstance(obj, dict) and isinstance(obj.get("code"), int) and obj["code"] != 0:
        msg = _extract_message(obj) or "business failure (code=%s)" % obj["code"]
        fail(5, msg)
    return obj


def check_http(status, obj, args):
    if status == 401:
        fail(4, "auth failure (401): the login has expired; run the login command first (or check --token).")
    if 300 <= status < 400:
        fail(3, "unexpected redirect HTTP {} (this client only accepts same-origin redirects).".format(status))
    if status >= 400:
        msg = _extract_message(obj) or "HTTP {}".format(status)
        fail(3, "request failed HTTP {}: {}".format(status, msg))


# ---------------------------------------------------------------------------
# Command implementations
# ---------------------------------------------------------------------------
def run_health(args, product):
    origin = parse_origin(args.base_url, product)
    ensure_trusted(args, origin)
    status, obj = http_call("GET", origin.server_root() + "/health", timeout=args.timeout)
    check_http(status, obj, args)
    return obj


def run_login(args, product, dry_run=False):
    if not args.username or not args.password:
        fail(1, "login requires --username and --password. A fresh install seeds admin/admin1; "
                "self-registration is also available in the platform UI.")
    origin = parse_origin(args.base_url, product)
    login_url = origin.api_root() + "/auth/login"
    # show the normalized destination before sending credentials
    sys.stderr.write("[zy_platform] login destination (normalized): POST {}\n".format(login_url))
    if dry_run:
        return {"dry_run": True, "destination": login_url, "product": product,
                "note": "nothing sent, no credentials used. Show the destination to the user and, "
                        "after explicit consent, run again without --dry-run."}
    ensure_trusted(args, origin)
    status, obj = http_call("POST", login_url,
                            payload={"username": args.username,
                                     "password": args.password},
                            timeout=args.timeout)
    check_http(status, obj, args)
    token = None
    if isinstance(obj, dict):
        token = obj.get("token")                                 # AIP/Apollo/Gotham/Swift flat
        if token is None and isinstance(obj.get("data"), dict):  # Foundry {code,data:{token}}
            token = obj["data"].get("token")
    if not token:
        fail(5, "no token found in the login response; check the credentials or this product's login endpoint.")
    if args.no_cache:
        audit_event("login", product=product, origin=origin.key(),
                    status=status, storage="none")
        return {"login": "ok", "product": product, "username": args.username,
                "destination": origin.api_root(), "token_saved": False,
                "note": "--no-cache: token not cached for this session."}
    info = store_set_token(origin, token)
    audit_event("login", product=product, origin=origin.key(),
                status=status, storage=info["storage"])
    return {"login": "ok", "product": product, "username": args.username,
            "destination": origin.api_root(), "token_saved": True, **info}


def run_logout(args, product):
    if args.all:
        removed = store_clear(None)
        forgotten = 0
        if args.forget_host:
            store = load_store()
            forgotten = len(store["trusted_origins"])
            store["trusted_origins"] = []
            save_store(store)
        scope = "all origins"
    else:
        origin = parse_origin(args.base_url, product)
        removed = store_clear(origin)
        forgotten = forget_host(origin) if args.forget_host else 0
        scope = origin.key()
    audit_event("logout", product=product, scope=scope,
                removed=removed, hosts_forgotten=forgotten)
    return {"logout": "ok", "product": product, "scope": scope,
            "removed_tokens": removed, "forgotten_hosts": forgotten}


def run_verify_artifact(args):
    """SHA-256 verification of a downloaded artifact before execution (digest from a separate official channel)."""
    if not args.file:
        fail(1, "verify-artifact requires --file <path> and --sha256 <official expected value>.")
    path = Path(args.file)
    if not path.is_file():
        fail(1, "file not found: {}".format(path))
    h = hashlib.sha256()
    size = 0
    with open(str(path), "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
            size += len(chunk)
    digest = h.hexdigest()
    expected = re.sub(r"\s+", "", args.sha256 or "").lower()
    match = bool(expected) and digest == expected
    return {"file": str(path), "size": size, "sha256": digest,
            "expected_sha256": expected or None, "match": match,
            "note": "continue only when match=true; then verify the digital signature "
                    "(expected publisher: ZY Tech / zyinfo.pro) and confirm with the user before executing."}, \
           (0 if match else 1)


def _split_segments(path):
    p = path.split("?", 1)[0].split("#", 1)[0]
    return [seg for seg in p.split("/") if seg]


def _passthrough_check(method, path):
    segs = _split_segments(path)
    if not segs:
        fail(1, "pass-through path is empty.")
    denied = [s for s in segs if s.lower() in DENY_SEGMENTS]
    if denied:
        fail(1, "security policy: the pass-through path contains sensitive/admin route segments ({}); refused.".format(
            ", ".join(denied)))
    if segs[0].lower() == "health":
        return                                  # server-root /health
    families = {s.lower() for s in segs}
    if method in SAFE_METHODS:
        if not (families & READ_PASS_THROUGH_FAMILIES):
            fail(1, "security policy: the read-only pass-through path is not in the allowlist. Allowed families: {}.".format(
                ", ".join(sorted(READ_PASS_THROUGH_FAMILIES))))
    else:
        if segs[0].lower() not in WRITE_PASS_THROUGH_FAMILIES:
            fail(1, "security policy: pass-through writes are only allowed in the {} families "
                    "(e.g. chat, ontology/semantic-search); use built-in commands for other writes.".format(
                        ", ".join(sorted(WRITE_PASS_THROUGH_FAMILIES))))


def run_request(args, product, dry_run=False):
    if not args.method or not args.path:
        fail(1, "request requires --method and --path. Only GET/HEAD are allowed by default; "
                "POST/PUT/PATCH/DELETE need explicit --allow-write and should be previewed with --dry-run first.")
    method = args.method.strip().upper()
    if method not in ALLOWED_METHODS:
        fail(1, "--method only allows {} (arbitrary strings are not accepted).".format("/".join(ALLOWED_METHODS)))
    if method not in SAFE_METHODS and not args.allow_write:
        fail(1, "security policy: write method {} requires explicit --allow-write; preview the "
                "method/URL/body with --dry-run and confirm with the user first.".format(method))
    origin = parse_origin(args.base_url, product)
    path = args.path.strip().lstrip("/")
    if "|" in path or "\\" in path or re.search(r"[\x00-\x1f\x7f]", path):
        fail(1, "--path contains illegal characters.")
    if "#" in path:
        fail(1, "security policy: --path must not contain a fragment (#).")
    _passthrough_check(method, path)
    if path.startswith("health"):
        url = origin.server_root() + "/" + path
    else:
        url = origin.api_root() + "/" + path
    if args.query_str and "?" not in url:
        if "#" in args.query_str:
            fail(1, "security policy: --query-str must not contain a fragment (#).")
        url += "?" + args.query_str.lstrip("?")
    payload = None
    if args.data:
        try:
            payload = json.loads(args.data)
        except ValueError:
            fail(1, "--data must be a valid JSON string, e.g. '{\"query\":\"x\"}'.")
    # pass-through never attaches the cached token automatically; --with-token grants it
    # explicitly (origin binding still enforced) or pass --token explicitly
    token = args.token or (store_get_token(args, origin) if args.with_token else None)
    body_preview = _redact(payload) if payload is not None else None
    sys.stderr.write("[zy_platform] target request: {} {}\n".format(method, url))
    if body_preview is not None:
        sys.stderr.write("[zy_platform] body (sensitive fields masked): {}\n".format(
            json.dumps(body_preview, ensure_ascii=False)[:800]))
    if dry_run:
        return {"dry_run": True, "method": method, "url": url,
                "body": body_preview, "token_attached": bool(token),
                "note": "nothing sent. Show the method/URL/body to the user and only then "
                        "execute for real (write methods also need --allow-write)."}
    ensure_trusted(args, origin)
    if method not in SAFE_METHODS:
        audit_event("passthrough-write", method=method, url=url, product=product,
                    origin=origin.key(),
                    body=json.dumps(body_preview, ensure_ascii=False)[:1500]
                    if body_preview is not None else None)
    status, obj = http_call(method, url, payload=payload, token=token,
                            timeout=args.timeout)
    check_http(status, obj, args)
    if method not in SAFE_METHODS:
        audit_event("passthrough-write-result", method=method, url=url,
                    status=status)
    return obj


def _append_query(url, params):
    """Append non-empty query params to url. Param values are int/str."""
    qs = {k: v for k, v in params.items() if v is not None}
    if qs and "?" not in url:
        url += "?" + urllib.parse.urlencode(qs)
    return url


def _build_query(name, args):
    if name == "search":
        if not args.query:
            fail(1, "search requires --query (search keywords).")
        return {"q": args.query, "limit": args.limit}
    if name == "workflow-list":
        return {"page": args.page, "page_size": args.page_size}
    if name == "dataset-list":
        return {"limit": args.limit}
    if name == "dataset-preview":
        return {"limit": args.limit}
    if name == "audit-list":
        return {"page": args.page, "page_size": args.page_size}
    return {}


def run_command(name, args, product, origin):
    method, tmpl = ENDPOINTS[name]
    path = tmpl.format(workflow_id=args.workflow_id or "",
                       execution_id=args.execution_id or "",
                       dataset_id=args.dataset_id or "",
                       deployment_id=args.deployment_id or "")
    # ENDPOINTS templates carry the /api/v1 prefix; api_root already includes it.
    if path.startswith("/api/v1"):
        path = path[len("/api/v1"):]
    url = _append_query(origin.api_root() + path, _build_query(name, args))
    payload = None
    if method == "POST":
        if name == "chat":
            if not args.query:
                fail(1, "chat requires --query (a natural-language question).")
            payload = {"query": args.query}
        elif name == "workflow-run":
            if not args.workflow_id:
                fail(1, "workflow-run requires --workflow-id (run workflow-list first).")
            payload = {}
            if args.params:
                try:
                    payload = json.loads(args.params)
                except ValueError:
                    fail(1, "--params must be a valid JSON object, e.g. '{\"region\":\"east\"}'.")
        elif name == "ontology-search":
            if not args.query:
                fail(1, "ontology-search requires --query.")
            payload = {"query": args.query}
            if args.limit:
                payload["limit"] = args.limit
        elif name == "workflow-cancel":
            if not args.execution_id:
                fail(1, "workflow-cancel requires --execution-id.")
    token = None if name in PUBLIC_COMMANDS else store_get_token(args, origin)
    status, obj = http_call(method, url, payload=payload, token=token,
                            timeout=args.timeout)
    check_http(status, obj, args)
    return obj


def build_parser():
    p = argparse.ArgumentParser(
        prog="zy_platform.py",
        description="ZY Action Platform REST client (five products, security-hardened).",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("command", nargs="?", help="command: " + " / ".join(COMMAND_INTRO))
    p.add_argument("--product", choices=list(PRODUCTS), default="aip",
                   help="product: aip/foundry/apollo/gotham/swift (default aip)")
    p.add_argument("--base-url", default=None,
                   help="server address. Defaults to http://127.0.0.1:<product port>; "
                        "remote addresses must use https; gateway form https://host/aip-api/v1 accepted")
    p.add_argument("--username", default=None)
    p.add_argument("--password", default=None)
    p.add_argument("--token", default=None, help="explicit token (takes precedence over the session cache)")
    p.add_argument("--no-cache", action="store_true", help="do not read or write the local session cache")
    p.add_argument("--trust-host", action="store_true",
                   help="confirm and trust this remote origin (required on first contact with a "
                        "non-loopback origin, after informed user consent)")
    p.add_argument("--allow-write", action="store_true",
                   help="request: allow write methods (POST/PUT/PATCH/DELETE); confirm with the user first")
    p.add_argument("--with-token", action="store_true",
                   help="request: explicitly authorize attaching the cached same-origin token (not attached by default)")
    p.add_argument("--dry-run", action="store_true",
                   help="login/request: show the normalized target and body without sending")
    p.add_argument("--all", action="store_true", help="logout: clear every cached token")
    p.add_argument("--forget-host", action="store_true",
                   help="logout: also remove the current origin from the trusted-origin list")
    p.add_argument("--file", default=None, help="verify-artifact: file to verify")
    p.add_argument("--sha256", default=None,
                   help="verify-artifact: expected SHA-256 from the official release page")
    p.add_argument("--pretty", action="store_true", help="pretty-print JSON output")
    p.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT, help="request timeout in seconds")
    # business args
    p.add_argument("--query", default=None)
    p.add_argument("--limit", type=int, default=None, help="max rows to return (search/dataset etc.)")
    p.add_argument("--page", type=int, default=None)
    p.add_argument("--page-size", dest="page_size", type=int, default=None)
    p.add_argument("--workflow-id", default=None)
    p.add_argument("--execution-id", default=None)
    p.add_argument("--dataset-id", default=None)
    p.add_argument("--deployment-id", default=None)
    p.add_argument("--params", default=None)
    p.add_argument("--method", default=None)
    p.add_argument("--path", default=None,
                   help="request path relative to the API root; no leading /, e.g. datasets?limit=5")
    p.add_argument("--data", default=None, help="JSON request body for request")
    p.add_argument("--query-str", dest="query_str", default=None,
                   help="query string for request, e.g. 'limit=5&status=active'")
    p.add_argument("--list-commands", action="store_true", help="list all commands")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    if args.list_commands:
        for k, v in COMMAND_INTRO.items():
            print("{:<20} {}".format(k, v))
        return 0
    if not args.command:
        fail(1, "missing command. Use --list-commands or --help.")
    name = args.command
    product = args.product

    if name == "request":
        obj = run_request(args, product, dry_run=args.dry_run)
    elif name == "health":
        obj = run_health(args, product)
    elif name == "me":
        origin = parse_origin(args.base_url, product)
        ensure_trusted(args, origin)
        token = store_get_token(args, origin)
        status, obj = http_call("GET", origin.api_root() + "/me", token=token,
                                timeout=args.timeout)
        check_http(status, obj, args)
    elif name == "login":
        obj = run_login(args, product, dry_run=args.dry_run)
    elif name == "logout":
        obj = run_logout(args, product)
    elif name == "verify-artifact":
        obj, rc = run_verify_artifact(args)
        emit(obj, args)
        return rc
    else:
        if name not in ENDPOINTS:
            fail(1, "unknown command {}. Use --list-commands.".format(name))
        if name not in ALLOW[product]:
            ok_products = [pr for pr in ALLOW if name in ALLOW[pr]]
            fail(1, "command {} does not apply to product {}; applies to: {}.".format(
                name, product,
                ", ".join(ok_products) if ok_products else "none (generic commands only: health/login/logout/request)"))
        origin = parse_origin(args.base_url, product)
        ensure_trusted(args, origin)
        obj = run_command(name, args, product, origin)
    obj = check_business(obj, args)
    emit(obj, args)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
