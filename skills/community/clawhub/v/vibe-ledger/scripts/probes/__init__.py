"""Deterministic checks over the project files.

Each probe module exposes NAME, APPLIES_TO (a set of stack names, or None for
every project) and run(root, stack) -> list[Finding]."""
from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

from common import iter_files, read_text
from redact import redact

SUPPORTED = {"nextjs", "vite", "react", "express", "supabase", "firebase"}
_DEPS = {"next": "nextjs", "vite": "vite", "react": "react", "express": "express",
         "@supabase/supabase-js": "supabase", "@supabase/ssr": "supabase",
         "firebase": "firebase", "firebase-admin": "firebase", "vue": "vue", "svelte": "svelte",
         "@sveltejs/kit": "sveltekit", "nuxt": "nuxt", "@remix-run/react": "remix", "astro": "astro"}
_PY_FILES = {"requirements.txt", "pyproject.toml", "Pipfile", "setup.cfg"}
_PY_STACKS = ("flask", "django", "fastapi", "streamlit")
_MARKER_FILES = {"go.mod": "go", "Gemfile": "rails", "composer.json": "php"}


@dataclass
class Finding:
    probe: str
    level: str
    path: str
    line: int
    snippet: str
    message: str
    implies: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


# Keys only a browser extension declares. A manifest with manifest_version but none of
# these (e.g. a component inside a headless Chrome that Remotion/Puppeteer download into
# the project) is not an extension of the project.
_EXTENSION_KEYS = {"background", "content_scripts", "action", "browser_action", "page_action",
                   "side_panel", "sidebar_action", "permissions", "host_permissions",
                   "optional_permissions", "optional_host_permissions", "options_page",
                   "options_ui", "devtools_page", "chrome_url_overrides",
                   "web_accessible_resources", "commands", "omnibox", "theme"}


def _is_extension(path) -> bool:
    try:
        data = json.loads(read_text(path))
    except json.JSONDecodeError:
        return False
    return isinstance(data, dict) and bool(_EXTENSION_KEYS & data.keys())


def detect_stack(root) -> dict:
    root = Path(root)
    found: set[str] = set()
    py_text = []
    for p in iter_files(root):
        if p.name == "package.json":
            try:
                data = json.loads(read_text(p))
            except json.JSONDecodeError:
                continue
            deps = {**(data.get("dependencies") or {}), **(data.get("devDependencies") or {})}
            found |= {stack for dep, stack in _DEPS.items() if dep in deps}
        elif p.name in _PY_FILES:
            py_text.append(read_text(p).lower())
        elif p.name in _MARKER_FILES:
            found.add(_MARKER_FILES[p.name])
        elif p.name in ("firebase.json", "firestore.rules", "storage.rules", "database.rules.json"):
            found.add("firebase")
        elif p.name == "manifest.json" and '"manifest_version"' in read_text(p) and _is_extension(p):
            found.add("chrome-extension")
    if (root / "supabase").is_dir():
        found.add("supabase")
    joined = " ".join(py_text)
    found |= {s for s in _PY_STACKS if re.search(rf"\b{s}\b", joined)}
    return {"stacks": sorted(found), "unsupported": sorted(found - SUPPORTED), "covered": bool(found & SUPPORTED)}


def _modules():
    from probes import (cors_wildcard, firebase_rules, paid_api_unauthed, routes,
                        secrets_exposed, supabase_rls)
    return [secrets_exposed, supabase_rls, firebase_rules, cors_wildcard, paid_api_unauthed, routes]


def run_all(root) -> dict:
    root = Path(root).resolve()
    stack = detect_stack(root)
    findings, ran, skipped = [], [], []
    for mod in _modules():
        if mod.APPLIES_TO is not None and not (mod.APPLIES_TO & set(stack["stacks"])):
            skipped.append({"probe": mod.NAME,
                            "reason": "not used by this project: " + ", ".join(sorted(mod.APPLIES_TO)),
                            "needs": sorted(mod.APPLIES_TO)})
            continue
        try:
            found = mod.run(root, stack)
        except Exception as exc:  # one broken probe must not hide the rest, but must show
            skipped.append({"probe": mod.NAME, "reason": f"crashed: {exc!r}"})
            continue
        ran.append(mod.NAME)
        findings.extend(found)
    out, seen = [], Counter()
    for f in findings:
        d = f.to_dict()
        d["snippet"] = redact(d["snippet"])  # probes.json is read by the model: never hand it a raw key
        base = f"{f.probe}:{f.path}:{f.line}"
        seen[base] += 1
        d["id"] = base if seen[base] == 1 else f"{base}#{seen[base]}"
        out.append(d)
    return {"stack": stack, "findings": out, "ran": ran, "skipped": skipped}
