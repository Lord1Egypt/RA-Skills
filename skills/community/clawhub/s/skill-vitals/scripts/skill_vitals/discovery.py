"""Generic filesystem discovery and deterministic SKILL.md inventory records."""

import hashlib
import os
import re
import time
from pathlib import Path

from .adapters.claude import lookup_usage
from .adapters.workbuddy import workbuddy_skill_active
from .frontmatter import parse_frontmatter
from .security import security_scan
from .util import est_tokens, norm, safe_str


DOC_DIRS = {"references", "reference", "refs", "docs", "doc"}
REPO_META = {"readme.md", "license.md", "license", "changelog.md", "contributing.md",
             "code_of_conduct.md", "security.md", "notice.md", "authors.md"}
PLUGIN_PATH_RE = re.compile(r"/plugins/(cache|marketplaces)/([^/]+)/(.+?)/skills/")
PLUGIN_WRAPPER_DIRS = {"plugins", "external_plugins", "unknown", "skills"}
VERSION_SEGMENT_RE = re.compile(r"^v?\d+(?:\.\d+)*$")


def plugin_identity(path_n: str):
    """Extract ``(plugin, marketplace)`` from a plugin Skill path."""
    match = PLUGIN_PATH_RE.search(path_n + "/")
    if not match:
        return None, None
    marketplace = match.group(2)
    middle = [part for part in match.group(3).split("/")
              if part and part not in PLUGIN_WRAPPER_DIRS]
    while len(middle) > 1 and VERSION_SEGMENT_RE.match(middle[-1]):
        middle.pop()
    plugin = middle[-1] if middle else marketplace
    return plugin, marketplace


def classify(skill_dir: Path, host: str, home_n=None, cwd_n=None):
    """Return the precedence level, namespace, and plugin key for one Skill."""
    home_n = home_n if home_n is not None else norm(Path(os.path.expanduser("~")))
    cwd_n = cwd_n if cwd_n is not None else norm(Path.cwd())
    path_n = norm(skill_dir.resolve())
    plugin, marketplace = plugin_identity(path_n)
    if plugin:
        return "plugin", plugin, f"{plugin}@{marketplace}"
    if host == "openclaw":
        if "/workspace/skills" in path_n:
            return "workspace", None, None
        if "/plugin-skills/" in path_n:
            return "plugin", None, None
        if path_n.startswith(cwd_n + "/skills"):
            return "workspace", None, None
        if path_n.startswith(cwd_n + "/.agents/skills"):
            return "project", None, None
        if path_n.startswith(home_n + "/.agents/skills"):
            return "personal", None, None
        if path_n.startswith(home_n + "/.openclaw/skills"):
            return "managed", None, None
        if re.match(re.escape(home_n) + r"/\.open[^/]*/skills(?:/|$)", path_n):
            return "managed", None, None
    if host == "hermes":
        return (("personal", None, None) if
                path_n.startswith(home_n + "/.hermes/skills") else
                ("external", None, None))
    if host == "codex":
        return "personal", None, None
    if host == "workbuddy":
        if (path_n.startswith(cwd_n + "/.codebuddy/skills") or
                path_n.startswith(cwd_n + "/.workbuddy/skills")):
            return "project", None, None
        if path_n.startswith(home_n + "/.workbuddy/skills"):
            return "personal", None, None
        if "/.workbuddy/plugins/marketplaces/workbuddy-builtin/" in path_n:
            return "managed", None, None
        return "unknown", None, None
    if "/managed" in path_n or "/etc/" in path_n or "enterprise" in path_n:
        return "enterprise", None, None
    if path_n.startswith(home_n + "/.claude/skills"):
        return "personal", None, None
    if (path_n.startswith(cwd_n + "/.claude/skills") or
            norm(skill_dir).startswith(".claude/skills")):
        return "project", None, None
    return "unknown", None, None


def days_since(milliseconds, now=None):
    if not milliseconds:
        return None
    current = time.time() if now is None else now
    return round((current - milliseconds / 1000.0) / 86400.0, 1)


def scan_skill_dir(skill_dir: Path, host: str, enabled_plugins, usage, plugins_known,
                   source_meta=None, home_n=None, cwd_n=None, now=None):
    """Build one stable public Skill record from a directory."""
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return None
    try:
        raw = skill_file.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None

    fields, frontmatter_raw, body = parse_frontmatter(raw)
    level, namespace, plugin_key = classify(skill_dir, host, home_n, cwd_n)
    source_meta = source_meta or {}
    enabled_state, loaded_state, runtime_verified = None, None, False
    if host in ("codex", "openclaw", "hermes", "workbuddy", "custom"):
        loaded, reason = True, level if level != "unknown" else "explicit-root"
        if host == "workbuddy" and "/plugins/marketplaces/workbuddy-builtin/" in norm(skill_dir):
            reason = "workbuddy-builtin-marketplace-manifest"
    elif host == "claude-code" and level in ("personal", "project", "enterprise"):
        loaded, reason = True, level
    elif level == "plugin":
        if not plugins_known:
            loaded, reason = False, "plugin-state-unknown"
        elif plugin_key in (enabled_plugins or ()) or namespace in (enabled_plugins or ()):
            loaded, reason = True, "plugin-enabled"
        else:
            loaded, reason = False, "plugin-not-enabled"
    else:
        loaded, reason = False, "unknown-location"

    bundled, bundled_bytes = [], 0
    refs_tokens, refs_files = 0, 0
    corpus_files, corpus_bytes = 0, 0
    for path in sorted(skill_dir.rglob("*"), key=norm):
        if not path.is_file() or path.name == "SKILL.md":
            continue
        try:
            size = path.stat().st_size
        except OSError:
            size = 0
        bundled_bytes += size
        relative = norm(path.relative_to(skill_dir))
        bundled.append({"path": relative, "bytes": size})
        if path.suffix.lower() not in (".md", ".markdown"):
            continue
        parts = relative.split("/")
        if len(parts) == 1 and path.name.lower() in REPO_META:
            continue
        if len(parts) == 1 or parts[0].lower() in DOC_DIRS:
            try:
                refs_tokens += est_tokens(path.read_text(encoding="utf-8", errors="replace"))
                refs_files += 1
            except OSError:
                pass
        else:
            corpus_files += 1
            corpus_bytes += size

    name = safe_str(fields.get("name") or skill_dir.name)
    if host == "openclaw":
        configured = source_meta.get("skill_entries", {}).get(name)
        if isinstance(configured, dict) and configured.get("enabled") is False:
            enabled_state, loaded_state = False, False
            loaded, reason = False, "openclaw-config-disabled"
        elif isinstance(configured, dict) and configured.get("enabled") is True:
            enabled_state, loaded_state = True, None
            loaded, reason = False, "openclaw-config-enabled-runtime-unverified"
        else:
            enabled_state, loaded_state = None, None
            loaded, reason = False, "openclaw-discoverable-runtime-unverified"
    elif host == "workbuddy" and source_meta.get("workbuddy_package"):
        mode = source_meta.get("workbuddy_welcome_mode")
        if not workbuddy_skill_active(source_meta.get("workbuddy_legacy_name"), mode):
            loaded, reason = False, f"workbuddy-mode-filtered:{mode}"
            enabled_state, loaded_state = False, False
        else:
            reason = (f"workbuddy-builtin-active-mode:{mode}" if mode else
                      "workbuddy-builtin-mode-unknown")
            enabled_state, loaded_state = (True, None) if mode else (None, None)
    hits, last_ms, matched_key = lookup_usage(usage, name, namespace)

    try:
        born = min(skill_dir.stat().st_ctime, skill_file.stat().st_ctime)
    except OSError:
        born = skill_file.stat().st_mtime
    current = time.time() if now is None else now
    age_days = round((current - born) / 86400.0, 1)
    description = fields.get("description", "")
    core_tokens = est_tokens(body)
    return {
        "name": name,
        "dir_name": safe_str(skill_dir.name),
        "host": host,
        "host_family": "claude-code" if host.startswith("claude-code") else host,
        "level": level,
        "namespace": namespace,
        "plugin_key": plugin_key,
        "loaded": loaded,
        "loaded_reason": reason,
        "installed": True,
        "discoverable": True if host == "openclaw" else loaded,
        "enabled_state": enabled_state,
        "loaded_state": loaded_state,
        "runtime_verified": runtime_verified,
        "instance_id": source_meta.get("instance_id"),
        "instance_root": source_meta.get("instance_root"),
        "config_path": source_meta.get("config_path"),
        "root_kind": source_meta.get("root_kind"),
        "conflict_domain": (f"openclaw:{source_meta.get('instance_id')}"
                            if host == "openclaw" and source_meta.get("instance_id") else host),
        "path": norm(skill_dir),
        "content_hash": hashlib.sha256(raw.encode("utf-8")).hexdigest()[:12],
        "description": description,
        "description_chars": len(description),
        "tier1_tokens": est_tokens(frontmatter_raw),
        "tier2_tokens": core_tokens,
        "tier2_core_tokens": core_tokens,
        "tier2_refs_tokens": refs_tokens,
        "tier2_refs_files": refs_files,
        "tier2_max_tokens": core_tokens + refs_tokens,
        "body_lines": body.count("\n") + 1 if body else 0,
        "bundled_files": len(bundled),
        "bundled_bytes": bundled_bytes,
        "data_corpus_files": corpus_files,
        "data_corpus_bytes": corpus_bytes,
        "mtime": int(skill_file.stat().st_mtime),
        "installed_days_ago": age_days,
        "usage_count": hits,
        "last_used_days_ago": days_since(last_ms, current if now is not None else None),
        "usage_key_matched": matched_key,
        "has_name": bool(fields.get("name")),
        "has_description": bool(description),
        "security": security_scan(skill_dir, raw),
    }


def _root_path(root, home=None):
    if home is not None and isinstance(root, str) and root.startswith("~"):
        return Path(home) / root[1:].lstrip("/\\")
    return Path(os.path.expanduser(root))


def collect(roots, enabled_plugins, usage, plugins_known, home=None, cwd=None):
    """Traverse roots deterministically and return records, roots, and read failures."""
    found, scanned_roots, unreadable, seen = [], [], [], set()
    home_n = norm(Path(home)) if home is not None else norm(Path(os.path.expanduser("~")))
    cwd_n = norm(Path(cwd)) if cwd is not None else norm(Path.cwd())
    for item in roots:
        host, root = item[:2]
        source_meta = item[2] if len(item) > 2 else {}
        base = _root_path(root, home)
        try:
            key = norm(base.resolve())
        except OSError:
            key = norm(base)
        dedupe_key = (host, source_meta.get("instance_id"), key)
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        if not base.is_dir():
            continue
        scanned_roots.append({"host": host, "path": norm(base),
                              "instance_id": source_meta.get("instance_id"),
                              "root_kind": source_meta.get("root_kind")})
        skill_files = ([base / "SKILL.md"] if source_meta.get("only_direct") else
                       sorted(base.rglob("SKILL.md"), key=norm))
        for skill_file in skill_files:
            if not skill_file.is_file():
                continue
            record = scan_skill_dir(
                skill_file.parent, host, enabled_plugins, usage, plugins_known,
                source_meta, home_n=home_n, cwd_n=cwd_n)
            if record:
                found.append(record)
            elif skill_file.is_file():
                unreadable.append({
                    "name": skill_file.parent.name,
                    "path": norm(skill_file.parent),
                    "host": host,
                    "reason": "SKILL.md exists but cannot be read (permission or I/O error)",
                })
    return found, scanned_roots, unreadable
