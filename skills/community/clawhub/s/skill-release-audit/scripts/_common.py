#!/usr/bin/env python3
"""
Shared helpers for skill-release-audit check modules.

Internal-only module (prefixed with `_`) — not a standalone check.
Keeps file-classification logic in one place so check_logic.py and
check_edges.py agree on what counts as a bash script.
"""

import json
import os
import sys
from pathlib import Path

from i18n import t

# ---------------------------------------------------------------------------
# Target profiles (--target). Each profile tunes which checks fire and at what
# severity for a given publishing target. Profiles live in ../profiles/*.json.
# ---------------------------------------------------------------------------

_PROFILES_DIR = Path(__file__).resolve().parent.parent / "profiles"
DEFAULT_PROFILE = "generic"


def list_profiles() -> "list[str]":
    """Return available profile names (sorted), derived from profiles/*.json."""
    if not _PROFILES_DIR.is_dir():
        return [DEFAULT_PROFILE]
    return sorted(p.stem for p in _PROFILES_DIR.glob("*.json"))


def load_profile(name: "str | None") -> dict:
    """Load a target profile by name. Falls back to a built-in minimal generic
    profile if the file is missing or unreadable, so the auditor never crashes
    on a bad --target. Unknown names raise ValueError (caller reports nicely).
    """
    builtin_generic = {
        "name": "generic",
        "frontmatter": {"required": ["name", "description"], "version_severity": "INFO"},
        "files": {"require_readme": False, "require_license": False},
        "slug_regex": "^[a-z0-9][a-z0-9-]*$",
        "slug_max_len": None,
        "bundle_limit_mb": None,
        "declaration_vs_code": "WARN",
    }
    if not name:
        name = DEFAULT_PROFILE
    path = _PROFILES_DIR / f"{name}.json"
    if not path.is_file():
        if name == DEFAULT_PROFILE:
            return builtin_generic
        raise ValueError(
            f"unknown --target '{name}'. Available: {', '.join(list_profiles())}"
        )
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # A corrupt named profile must NOT silently degrade — the user thinks
        # they are validating against `name` but would get generic rules. Warn
        # to stderr (report-only; no fix command, per auditor design) and fall
        # back so the run still completes.
        print(t("cli.profile_corrupt", name=name), file=sys.stderr)
        return builtin_generic

# Candidate skills-root directory names across agent frameworks. Used to locate a
# sibling skill (for `depends_on_skills`) and to suggest a safe data directory,
# without hardcoding any single framework's layout.
_SKILLS_ROOT_CANDIDATES = (
    "~/.openclaw/skills",
    "~/.openclaw/workspace/skills",
    "~/.claude/skills",
    "~/.codex/skills",
    "~/.agents/skills",
)


def safe_data_dir_hint(skill_name: str = "<skill-name>") -> str:
    """Return a portable, human-readable path hint for where a skill should
    persist data (i.e. OUTSIDE its own directory, which is overwritten on update).

    Resolution order, first existing wins:
      1. $CLAWHUB_WORKDIR / $OPENCLAW_WORKSPACE (if set)
      2. ~/.openclaw/workspace
      3. ~/.local/share  (XDG-ish fallback, exists on most Linux/macOS)
      4. ~  (home dir, always present)

    Returns a string for messaging only — callers should not assume the dir
    exists. This avoids hardcoding the OpenClaw-specific path in user-facing tips
    so the auditor stays useful on Claude Code / Codex / plain GitHub checkouts.
    """
    for env_var in ("CLAWHUB_WORKDIR", "OPENCLAW_WORKSPACE"):
        val = os.environ.get(env_var)
        if val:
            return f"{val.rstrip('/')}/.skill-data/{skill_name}/"

    for base in ("~/.openclaw/workspace", "~/.local/share", "~"):
        if Path(base).expanduser().is_dir():
            return f"{base}/.skill-data/{skill_name}/"

    return f"~/.skill-data/{skill_name}/"


def find_sibling_skill_scripts(skill_dir: Path, dep_name: str) -> "Path | None":
    """Locate the `scripts/` dir of a sibling skill named `dep_name`.

    Checks the parent of `skill_dir` first (the common "all skills under one
    root" layout), then a set of well-known skills-root candidates. Returns the
    scripts Path if found, else None (the caller degrades gracefully — a missing
    sibling is not an error during a first-time audit).
    """
    candidates = [skill_dir.parent / dep_name / "scripts"]
    for root in _SKILLS_ROOT_CANDIDATES:
        candidates.append(Path(root).expanduser() / dep_name / "scripts")
    for c in candidates:
        if c.is_dir():
            return c
    return None


# Shebangs that identify a bash/sh script (extensionless files).
_BASH_SHEBANGS = (
    b"#!/bin/bash",
    b"#!/usr/bin/env bash",
    b"#!/bin/sh",
    b"#!/usr/bin/env sh",
)


def split_frontmatter(content: str) -> tuple[dict, str, str]:
    """Split SKILL.md content into (frontmatter_dict, frontmatter_raw, body).

    Prefers PyYAML (`yaml.safe_load`) for correct handling of multi-line values,
    lists and nested maps. Falls back to a tolerant hand-rolled `key: value`
    parser when PyYAML is unavailable (PyYAML is not in the stdlib).

    `frontmatter_dict` values may be str, list or dict (yaml path) or str only
    (fallback path). `frontmatter_raw` is the text between the `---` fences,
    useful for regex-based extraction that needs the original layout.
    """
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "", content.strip()

    fm_lines: list[str] = []
    body_start = len(lines)
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            body_start = i + 1
            break
        fm_lines.append(lines[i])

    fm_raw = "\n".join(fm_lines)
    body = "\n".join(lines[body_start:]).strip()

    fm: dict = {}
    try:
        import yaml  # type: ignore
        loaded = yaml.safe_load(fm_raw)
        if isinstance(loaded, dict):
            fm = loaded
        return fm, fm_raw, body
    except Exception:
        pass

    # Fallback: tolerant flat key:value parser (no external deps).
    # Inline JSON values (`key: {...}` / `key: [...]`) are JSON-decoded so that
    # nested structures (e.g. `metadata: {"openclaw": {...}}`) survive without
    # PyYAML. This keeps the fallback path consistent with the yaml path, which
    # matters for checks that read nested fields (e.g. declaration-vs-code reading
    # metadata.openclaw.requires.env). Without this, such values stay strings and
    # silently break those checks on environments lacking PyYAML.
    current_key = None
    for line in fm_lines:
        if line and not line[0].isspace() and ":" in line:
            k, _, v = line.partition(":")
            current_key = k.strip()
            v = v.strip()
            if v[:1] in "{[":
                try:
                    fm[current_key] = json.loads(v)
                    continue
                except Exception:
                    pass
            fm[current_key] = v
        elif line and line[0].isspace() and current_key:
            prev = fm.get(current_key, "")
            # Only fold continuation lines into plain string values; never clobber
            # an already-parsed dict/list.
            if isinstance(prev, str):
                fm[current_key] = (prev + "\n" + line.strip()).strip()

    return fm, fm_raw, body


def is_bash_script(path: Path) -> bool:
    """Return True if `path` is a bash/sh script.

    Matches by `.sh` suffix, or — for extensionless files — by a bash/sh
    shebang on the first line. A non-bash shebang (e.g. `#!/usr/bin/env python3`)
    is NOT treated as bash, so a Python launcher without an extension won't be
    handed to `bash -n`.
    """
    if not path.is_file():
        return False
    if path.suffix == ".sh":
        return True
    if path.suffix == "":
        try:
            if path.stat().st_size == 0:
                return False
            head = path.read_bytes()[:32]
        except Exception:
            return False
        return any(head.startswith(s) for s in _BASH_SHEBANGS)
    return False
