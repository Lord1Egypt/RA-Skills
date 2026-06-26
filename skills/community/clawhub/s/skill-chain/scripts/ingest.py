#!/usr/bin/env python3
"""
SkillChain ingest: discover local skills and populate the graph.

Usage:
    python3 scripts/ingest.py scan                          # auto-discover skills
    python3 scripts/ingest.py scan --dirs <dir1> <dir2>     # scan specific dirs
    python3 scripts/ingest.py status                        # show graph summary
    python3 scripts/ingest.py reset                         # clear graph
"""

import argparse
import ast
import json
import re
import ssl
import sys
import urllib.request
import subprocess
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Stdlib module name set (for AST import filtering)
# ---------------------------------------------------------------------------

def _get_stdlib_names() -> frozenset:
    try:
        return frozenset(sys.stdlib_module_names)  # Python 3.10+
    except AttributeError:
        pass
    return frozenset({
        "os", "sys", "re", "json", "math", "io", "abc", "ast", "argparse",
        "collections", "copy", "csv", "datetime", "decimal", "email", "enum",
        "functools", "glob", "hashlib", "http", "importlib", "inspect", "itertools",
        "logging", "operator", "pathlib", "pickle", "platform", "pprint", "queue",
        "random", "shutil", "signal", "socket", "sqlite3", "ssl", "stat", "string",
        "struct", "subprocess", "tempfile", "textwrap", "threading", "time", "traceback",
        "typing", "unittest", "urllib", "uuid", "warnings", "weakref", "xml", "zipfile",
        "zlib", "base64", "binascii", "builtins", "calendar", "cmath", "cmd", "code",
        "codecs", "codeop", "compileall", "concurrent", "configparser", "contextlib",
        "contextvars", "ctypes", "dataclasses", "dbm", "difflib", "dis", "doctest",
        "encodings", "filecmp", "fileinput", "fnmatch", "fractions", "ftplib", "gc",
        "getopt", "getpass", "gettext", "grp", "gzip", "heapq", "hmac", "html",
        "idlelib", "imaplib", "imghdr", "keyword", "linecache", "locale", "lzma",
        "mailbox", "marshal", "mimetypes", "mmap", "multiprocessing", "netrc",
        "numbers", "opcode", "optparse", "pkgutil", "poplib", "posix", "posixpath",
        "profile", "pstats", "pty", "pwd", "py_compile", "pyclbr", "pydoc",
        "readline", "reprlib", "resource", "runpy", "sched", "secrets", "select",
        "selectors", "shelve", "shlex", "site", "smtplib", "socketserver",
        "statistics", "stringprep", "symtable", "sysconfig", "syslog", "tabnanny",
        "tarfile", "telnetlib", "termios", "test", "token", "tokenize", "tomllib",
        "trace", "tracemalloc", "tty", "turtle", "types", "unicodedata", "venv",
        "wave", "wsgiref", "xdrlib", "xmlrpc", "zipapp", "zipimport", "_thread",
    })

_STDLIB = _get_stdlib_names()

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SKILL_CHAIN_ROOT = Path(__file__).resolve().parent.parent
GRAPH_PATH = str(SKILL_CHAIN_ROOT / "memory" / "skillchain" / "graph.jsonl")
SCHEMA_PATH = str(SKILL_CHAIN_ROOT / "schema" / "skillchain.yaml")

# Reuse ontology.py for graph operations (sibling skill)
_ONTOLOGY_SCRIPT = Path(__file__).resolve().parent.parent.parent / "ontology" / "scripts" / "ontology.py"
if _ONTOLOGY_SCRIPT.exists():
    sys.path.insert(0, str(_ONTOLOGY_SCRIPT.parent))

try:
    from ontology import (
        load_graph,
        create_entity,
        create_relation,
        update_entity,
        append_op,
        generate_id,
    )
    _ONTOLOGY_OK = True
except ImportError:
    _ONTOLOGY_OK = False

# ---------------------------------------------------------------------------
# Default scan roots
# ---------------------------------------------------------------------------

DEFAULT_SCAN_ROOTS = [
    "~/.openclaw/skills",
    "~/.openclaw/extensions",
    "/Applications/OpenClaw.app/Contents/Resources/skills",
]

# ---------------------------------------------------------------------------
# Category keyword map  (text → category slug)
# ---------------------------------------------------------------------------

CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "crypto-finance":      ["crypto", "trading", "finance", "exchange", "market",
                            "portfolio", "binance", "gate", "stock", "blockchain",
                            "defi", "wallet", "token", "futures", "forex", "invest"],
    "media-creation":      ["video", "audio", "image", "music", "photo", "voice",
                            "screenshot", "diagram", "slide", "audiobook", "canvas",
                            "design", "animation", "subtitle", "transcript"],
    "communication":       ["email", "wechat", "lark", "qq", "telegram", "slack",
                            "message", "chat", "feishu", "dingtalk", "whatsapp",
                            "gmail", "mail", "sender", "notification"],
    "data-analysis":       ["data", "analysis", "report", "dashboard", "chart",
                            "analytics", "sql", "database", "spreadsheet", "excel",
                            "csv", "bitable", "tableau"],
    "web-automation":      ["browser", "playwright", "selenium", "scraper", "crawl",
                            "search", "web", "url", "http", "fetch", "spider"],
    "productivity":        ["memory", "task", "note", "calendar", "reminder",
                            "schedule", "planner", "brain", "knowledge", "ontology",
                            "second brain", "notion", "obsidian"],
    "development":         ["code", "github", "kubernetes", "k8s", "docker", "mcp",
                            "api", "developer", "git", "debug", "ci", "deploy",
                            "refactor", "test", "lint", "build"],
    "ai-models":           ["llm", "gemini", "qwen", "gpt", "openai", "model",
                            "vision", "generation", "embedding", "inference",
                            "claude", "mistral", "siliconflow"],
    "automation":          ["automation", "bot", "auto", "workflow", "recipe",
                            "scheduler", "trigger", "pipeline", "rpa"],
    "research":            ["research", "medical", "scientific", "paper", "literature",
                            "ncbi", "pubmed", "scholar", "biomedical", "clinical"],
    "iot-hardware":        ["device", "iot", "sensor", "hardware", "camera",
                            "ezviz", "ninebot", "robot", "control", "capture"],
    "security":            ["security", "antivirus", "auth", "credential", "safe",
                            "privacy", "encrypt", "vulnerability", "scan", "malware"],
}

# ---------------------------------------------------------------------------
# Ontology fallback (if ontology skill is not installed)
# ---------------------------------------------------------------------------

def _load_graph_fallback(path: str) -> tuple[dict, list]:
    entities: dict = {}
    relations: list = []
    p = Path(path)
    if not p.exists():
        return entities, relations
    with open(p) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            op = rec.get("op")
            if op == "create":
                e = rec["entity"]
                entities[e["id"]] = e
            elif op == "update":
                eid = rec["id"]
                if eid in entities:
                    entities[eid]["properties"].update(rec.get("properties", {}))
                    entities[eid]["updated"] = rec.get("timestamp")
            elif op == "delete":
                entities.pop(rec["id"], None)
            elif op == "relate":
                relations.append({
                    "from": rec["from"], "rel": rec["rel"],
                    "to": rec["to"], "properties": rec.get("properties", {})
                })
    return entities, relations


def _append_op_fallback(path: str, record: dict) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "a") as f:
        f.write(json.dumps(record) + "\n")


def _generate_id_fallback(type_name: str) -> str:
    import uuid
    return f"{type_name.lower()[:4]}_{uuid.uuid4().hex[:8]}"


def _create_entity_fallback(type_name: str, props: dict, graph_path: str,
                             entity_id: str | None = None) -> dict:
    eid = entity_id or _generate_id_fallback(type_name)
    ts = datetime.now(timezone.utc).isoformat()
    entity = {"id": eid, "type": type_name, "properties": props,
               "created": ts, "updated": ts}
    _append_op_fallback(graph_path, {"op": "create", "entity": entity, "timestamp": ts})
    return entity


def _create_relation_fallback(from_id: str, rel: str, to_id: str,
                               props: dict, graph_path: str) -> None:
    ts = datetime.now(timezone.utc).isoformat()
    _append_op_fallback(graph_path, {
        "op": "relate", "from": from_id, "rel": rel,
        "to": to_id, "properties": props, "timestamp": ts,
    })


# Choose implementation
if _ONTOLOGY_OK:
    _load   = load_graph
    _mkent  = create_entity
    _mkrel  = create_relation
    _upd    = update_entity
else:
    _load   = _load_graph_fallback
    _mkent  = _create_entity_fallback
    _mkrel  = _create_relation_fallback
    _upd    = None  # not used in ingest


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not m:
        return {}
    try:
        import yaml
        return yaml.safe_load(m.group(1)) or {}
    except Exception:
        pass
    # Minimal fallback: key: value lines
    result = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            result[k.strip()] = v.strip()
    return result


def _parse_allowed_tools(value) -> list[dict]:
    """Parse allowed-tools field into [{tool, pattern}] list.

    Handles both string and list forms:
      - "Bash(agent-browser:*)"
      - ["Bash(agent-browser:*)", "mcp__toolname"]
    """
    if not value:
        return []
    items = [value] if isinstance(value, str) else list(value)
    result = []
    for item in items:
        item = str(item).strip()
        m = re.match(r"^([A-Za-z0-9_\-]+)\((.+)\)$", item)
        if m:
            result.append({"tool": m.group(1), "pattern": m.group(2)})
        elif item:
            result.append({"tool": item, "pattern": "*"})
    return result


def _parse_requires_bins(metadata) -> list[str]:
    """Extract metadata.requires.bins list from skill metadata field."""
    if not metadata or not isinstance(metadata, dict):
        return []
    for key in metadata.values():
        if isinstance(key, dict):
            bins = key.get("requires", {}).get("bins", [])
            if isinstance(bins, list):
                return [str(b) for b in bins]
    return []


def parse_skill_md(path: Path) -> dict:
    """Extract name, description, license, allowed_tools, requires_bins, read_when from SKILL.md."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {}
    fm = _parse_frontmatter(text)
    return {
        "name":          fm.get("name", path.parent.name),
        "description":   fm.get("description", ""),
        "license":       fm.get("license", None),
        "allowed_tools": _parse_allowed_tools(fm.get("allowed-tools")),
        "requires_bins": _parse_requires_bins(fm.get("metadata")),
        "read_when":     fm.get("read_when") or [],
        "raw":           text,
    }


def _parse_pyproject_data(data: dict, add_fn) -> None:
    """Extract deps from a parsed pyproject.toml dict (PEP 621 + Poetry)."""
    # PEP 621 / Hatch / Flit: [project] dependencies = ["pkg>=x"]
    for dep in data.get("project", {}).get("dependencies", []):
        if isinstance(dep, str):
            name = re.split(r"[>=<!~\[\s;@]", dep)[0].strip().lower()
            if name:
                add_fn(name, dep, "pyproject.toml")
    # Poetry: [tool.poetry.dependencies] = {pkg = "^x"}
    poetry_deps = data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    for pkg_name, spec in poetry_deps.items():
        n = pkg_name.strip().lower()
        if n in ("python", ""):
            continue
        spec_str = spec if isinstance(spec, str) else (spec.get("version", "*") if isinstance(spec, dict) else str(spec))
        add_fn(n, f"{pkg_name}{spec_str}", "pyproject.toml[poetry]")
    # uv / PDM optional-dependencies
    for group_deps in data.get("project", {}).get("optional-dependencies", {}).values():
        for dep in group_deps:
            if isinstance(dep, str):
                name = re.split(r"[>=<!~\[\s;@]", dep)[0].strip().lower()
                if name:
                    add_fn(name, dep, "pyproject.toml[optional]")


def _parse_pyproject_regex(text: str, add_fn) -> None:
    """Pure-regex fallback when no TOML library is available."""
    # PEP 621: dependencies = [ ... ]
    m = re.search(r'\[project\].*?^dependencies\s*=\s*\[(.*?)\]', text, re.DOTALL | re.MULTILINE)
    if m:
        for grp in re.findall(r'"([^"]+)"|\'([^\']+)\'', m.group(1)):
            raw = grp[0] or grp[1]
            name = re.split(r"[>=<!~\[\s;@]", raw)[0].strip().lower()
            if name:
                add_fn(name, raw, "pyproject.toml")
    # Poetry: [tool.poetry.dependencies]
    m2 = re.search(r'\[tool\.poetry\.dependencies\](.*?)(?=^\[|\Z)', text, re.DOTALL | re.MULTILINE)
    if m2:
        for line in m2.group(1).splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            m3 = re.match(r'^([A-Za-z0-9_\-\.]+)\s*=\s*(.+)', line)
            if m3:
                n = m3.group(1).strip().lower()
                if n == "python":
                    continue
                add_fn(n, f"{m3.group(1)}{m3.group(2).strip()}", "pyproject.toml[poetry]")


def _parse_pyproject_toml(text: str, add_fn) -> None:
    """Parse pyproject.toml: try tomllib/tomli, fall back to regex."""
    for mod in ("tomllib", "tomli"):
        try:
            lib = __import__(mod)
            data = lib.loads(text)
            _parse_pyproject_data(data, add_fn)
            return
        except (ImportError, Exception):
            pass
    _parse_pyproject_regex(text, add_fn)


def _parse_pipfile(text: str, add_fn) -> None:
    """Parse Pipfile [packages] and [dev-packages] sections (INI-like)."""
    in_packages = False
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line in ("[packages]", "[dev-packages]"):
            in_packages = True
            continue
        if line.startswith("["):
            in_packages = False
            continue
        if in_packages:
            m = re.match(r'^([A-Za-z0-9_\-\.]+)\s*=\s*(.+)', line)
            if m:
                n = m.group(1).strip().lower()
                spec = m.group(2).strip().strip('"\'')
                if n not in ("python", ""):
                    add_fn(n, f"{m.group(1)}{spec}", "Pipfile")


def parse_requirements(skill_dir: Path) -> list[dict]:
    """Return [{name, ecosystem, spec, source}] for all declared packages.

    Sources checked (in order):
      - requirements.txt  (pypi)
      - pyproject.toml    (pypi, PEP 621 + Poetry + optional-deps)
      - Pipfile           (pypi)
      - package.json      (npm, dependencies + devDependencies + peerDependencies)
    """
    pkgs: list[dict] = []
    seen: set[str] = set()

    def _add(name: str, spec: str, source: str = "") -> None:
        n = name.strip().lower()
        if n and n not in seen:
            seen.add(n)
            entry: dict = {"name": n, "ecosystem": "pypi", "spec": spec}
            if source:
                entry["source"] = source
            pkgs.append(entry)

    def _add_npm(name: str, source: str = "") -> None:
        n = name.strip().lower()
        if n and n not in seen:
            seen.add(n)
            entry: dict = {"name": n, "ecosystem": "npm", "spec": name}
            if source:
                entry["source"] = source
            pkgs.append(entry)

    # 1. requirements.txt
    for req_file in skill_dir.rglob("requirements.txt"):
        try:
            for raw_line in req_file.read_text(errors="replace").splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#") or line.startswith("-"):
                    continue
                name = re.split(r"[>=<!~\[\s;]", line)[0].strip().lower()
                _add(name, line, "requirements.txt")
        except Exception:
            pass

    # 2. pyproject.toml (PEP 621, Poetry, uv/PDM optional-deps)
    for pp in skill_dir.rglob("pyproject.toml"):
        try:
            _parse_pyproject_toml(pp.read_text(errors="replace"), _add)
        except Exception:
            pass

    # 3. Pipfile
    for pf in skill_dir.rglob("Pipfile"):
        try:
            _parse_pipfile(pf.read_text(errors="replace"), _add)
        except Exception:
            pass

    # 4. package.json (npm)
    for pkg_file in skill_dir.rglob("package.json"):
        try:
            data = json.loads(pkg_file.read_text(errors="replace"))
            for section in ("dependencies", "devDependencies", "peerDependencies"):
                for pkg_name in data.get(section, {}):
                    _add_npm(pkg_name, "package.json")
        except Exception:
            pass

    return pkgs


def scan_python_imports(skill_dir: Path) -> list[dict]:
    """Scan *.py files via AST and extract third-party top-level imports.

    Returns [{name, ecosystem, spec, source}] for packages not already in the
    stdlib.  These are 'implicit' deps — useful when requirements.txt is absent
    or incomplete.
    """
    found: dict[str, str] = {}  # module_name -> first file that imported it
    for py_file in skill_dir.rglob("*.py"):
        try:
            tree = ast.parse(py_file.read_text(errors="replace"), filename=str(py_file))
        except SyntaxError:
            continue
        rel = py_file.relative_to(skill_dir) if py_file.is_relative_to(skill_dir) else py_file
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    top = alias.name.split(".")[0]
                    if top and top not in _STDLIB and not top.startswith("_"):
                        found.setdefault(top, str(rel))
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.level == 0:
                    top = node.module.split(".")[0]
                    if top and top not in _STDLIB and not top.startswith("_"):
                        found.setdefault(top, str(rel))
    return [
        {"name": n.lower(), "ecosystem": "pypi", "spec": n, "source": f"import:{src}"}
        for n, src in found.items()
    ]


def detect_tools(skill_dir: Path, skill_text: str) -> list[dict]:
    """Detect tools from SKILL.md content, file structure, and script imports."""
    tools = []
    seen: set[str] = set()
    text = skill_text.lower()

    def _add(name: str, kind: str, desc: str = "") -> None:
        if name not in seen:
            seen.add(name)
            tools.append({"name": name, "kind": kind, "description": desc})

    # Browser automation
    if "playwright" in text or "patchright" in text:
        _add("playwright", "playwright", "Browser automation (Playwright/Patchright)")
    if "selenium" in text or "webdriver" in text:
        _add("selenium", "browser", "Browser automation (Selenium)")
    if "puppeteer" in text:
        _add("puppeteer", "browser", "Browser automation (Puppeteer)")

    # MCP
    if re.search(r"\bmcp\b.{0,40}(server|tool|call)", text) or "fastmcp" in text:
        _add("mcp-tools", "mcp", "Model Context Protocol tools")

    # Media / A/V
    if "ffmpeg" in text:
        _add("ffmpeg", "cli", "Video/audio processing (FFmpeg)")
    if re.search(r"\bimagemagick\b|convert\.exe", text):
        _add("imagemagick", "cli", "Image processing (ImageMagick)")

    # Databases
    if "sqlite" in text:
        _add("sqlite", "db", "Local SQLite database")
    if re.search(r"postgres|postgresql", text):
        _add("postgres", "db", "PostgreSQL database")
    if re.search(r"\bmysql\b", text):
        _add("mysql", "db", "MySQL database")
    if re.search(r"\bmongodb\b|\bpymongo\b", text):
        _add("mongodb", "db", "MongoDB database")
    if re.search(r"\bredis\b", text):
        _add("redis", "db", "Redis key-value store")

    # Version control / DevOps
    if re.search(r"\bgit\b.{0,30}(commit|clone|push|branch|diff)", text):
        _add("git", "cli", "Git version control")
    if re.search(r"\bdocker\b", text):
        _add("docker", "cli", "Docker container runtime")
    if re.search(r"\bkubernetes\b|\bkubectl\b|\bk8s\b", text):
        _add("kubectl", "cli", "Kubernetes CLI")

    # Network / HTTP tools
    if re.search(r"\bcurl\b", text):
        _add("curl", "cli", "HTTP client (curl)")

    # Document processing
    if re.search(r"\bpandoc\b", text):
        _add("pandoc", "cli", "Universal document converter (Pandoc)")
    if re.search(r"\blibreoffice\b", text):
        _add("libreoffice", "cli", "LibreOffice document processing")

    # Node / npm runtime
    if re.search(r"\bnpx\b|\bnode\b.{0,20}(run|exec|script)", text):
        _add("node", "runtime", "Node.js runtime / npx")

    # Shell scripts / Python scripts
    if (skill_dir / "scripts").is_dir():
        _add("scripts", "python_script", "Local Python helper scripts")
    if any(skill_dir.rglob("*.sh")):
        _add("shell-scripts", "shell", "Local shell scripts")

    # Makefile
    if (skill_dir / "Makefile").exists():
        _add("make", "cli", "GNU Make build tool")

    return tools


def detect_skill_deps(skill_text: str, known_slugs: set[str]) -> list[str]:
    """Find references to other known skill slugs in SKILL.md."""
    deps = []
    for slug in known_slugs:
        # Match slug as a word in the text (not own name)
        if re.search(r"\b" + re.escape(slug) + r"\b", skill_text, re.IGNORECASE):
            deps.append(slug)
    return deps


def infer_categories(name: str, description: str) -> list[str]:
    text = (name + " " + description).lower()
    cats = [cat for cat, kws in CATEGORY_KEYWORDS.items() if any(kw in text for kw in kws)]
    return cats or ["uncategorized"]


def read_local_meta(skill_dir: Path) -> dict:
    meta: dict = {}
    for candidate in [skill_dir / "_meta.json",
                      skill_dir / ".clawhub" / "origin.json"]:
        if candidate.exists():
            try:
                data = json.loads(candidate.read_text())
                meta.setdefault("slug", data.get("slug", ""))
                meta.setdefault("version", data.get("version") or data.get("installedVersion", ""))
                meta.setdefault("registry", data.get("registry", "clawhub"))
                if "publishedAt" in data:
                    meta["published_at"] = data["publishedAt"]
            except Exception:
                pass
    return meta


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def is_skill_dir(path: Path) -> bool:
    try:
        return (path / "SKILL.md").exists()
    except PermissionError:
        return False


def find_skill_dirs(roots: list[str]) -> list[Path]:
    found: list[Path] = []
    seen: set[Path] = set()

    def _add(p: Path) -> None:
        try:
            r = p.resolve()
        except Exception:
            return
        if r not in seen:
            seen.add(r)
            found.append(p)

    for root_str in roots:
        root = Path(root_str).expanduser()
        if not root.exists():
            continue
        if is_skill_dir(root):
            _add(root)
            continue
        try:
            children = list(root.iterdir())
        except PermissionError:
            continue
        for child in children:
            if not child.is_dir():
                continue
            if is_skill_dir(child):
                _add(child)
            else:
                # One more level (e.g. skills-main/skills/*/SKILL.md)
                try:
                    for grandchild in child.iterdir():
                        if not grandchild.is_dir():
                            continue
                        if is_skill_dir(grandchild):
                            _add(grandchild)
                        # Special-case ~/.openclaw/extensions/<plugin>/skills/* pattern
                        elif grandchild.name == "skills":
                            try:
                                for gg in grandchild.iterdir():
                                    if gg.is_dir() and is_skill_dir(gg):
                                        _add(gg)
                            except PermissionError:
                                pass
                except PermissionError:
                    pass

    return found


# ---------------------------------------------------------------------------
# Graph upsert helpers
# ---------------------------------------------------------------------------

def _existing_id(entities: dict, type_name: str, key: str, value: str) -> str | None:
    for e in entities.values():
        if e["type"] == type_name and e["properties"].get(key) == value:
            return e["id"]
    return None


def upsert_skill(entities: dict, slug: str, props: dict) -> str:
    eid = _existing_id(entities, "Skill", "slug", slug)
    if eid:
        ts = datetime.now(timezone.utc).isoformat()
        rec = {"op": "update", "id": eid, "properties": props, "timestamp": ts}
        _append_op_fallback(GRAPH_PATH, rec) if not _ONTOLOGY_OK else \
            __import__("ontology").append_op(GRAPH_PATH, rec)
        entities[eid]["properties"].update(props)
        return eid
    entity = _mkent("Skill", {**props, "slug": slug}, GRAPH_PATH)
    entities[entity["id"]] = entity
    return entity["id"]


def upsert_category(entities: dict, name: str) -> str:
    eid = _existing_id(entities, "SkillCategory", "name", name)
    if eid:
        return eid
    entity = _mkent("SkillCategory", {"name": name}, GRAPH_PATH)
    entities[entity["id"]] = entity
    return entity["id"]


def upsert_tool(entities: dict, name: str, kind: str, desc: str) -> str:
    eid = _existing_id(entities, "Tool", "name", name)
    if eid:
        return eid
    entity = _mkent("Tool", {"name": name, "kind": kind, "description": desc}, GRAPH_PATH)
    entities[entity["id"]] = entity
    return entity["id"]


def upsert_package(entities: dict, name: str, ecosystem: str, spec: str,
                   source: str = "") -> str:
    eid = _existing_id(entities, "SoftwarePackage", "name", name)
    if eid:
        return eid
    props: dict = {"name": name, "ecosystem": ecosystem, "spec": spec}
    if source:
        props["source"] = source
    entity = _mkent("SoftwarePackage", props, GRAPH_PATH)
    entities[entity["id"]] = entity
    return entity["id"]


def relation_exists(relations: list, from_id: str, rel: str, to_id: str) -> bool:
    return any(r["from"] == from_id and r["rel"] == rel and r["to"] == to_id
               for r in relations)


def add_rel(entities: dict, relations: list,
            from_id: str, rel: str, to_id: str) -> None:
    if not relation_exists(relations, from_id, rel, to_id):
        _mkrel(from_id, rel, to_id, {}, GRAPH_PATH)
        relations.append({"from": from_id, "rel": rel, "to": to_id, "properties": {}})


def add_rel_with_props(entities: dict, relations: list,
                       from_id: str, rel: str, to_id: str, props: dict) -> None:
    if not relation_exists(relations, from_id, rel, to_id):
        _mkrel(from_id, rel, to_id, props, GRAPH_PATH)
        relations.append({"from": from_id, "rel": rel, "to": to_id, "properties": props})


# ---------------------------------------------------------------------------
# Online enrichment
# ---------------------------------------------------------------------------

def _clawhub_get(path: str, retries: int = 3) -> dict | None:
    import time
    ctx = ssl.create_default_context()
    req = urllib.request.Request(
        f"https://clawhub.ai/api/v1/{path}",
        headers={"Accept": "application/json"},
    )
    for attempt in range(retries):
        try:
            resp = urllib.request.urlopen(req, timeout=12, context=ctx)
            return json.loads(resp.read())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                wait = 2 ** (attempt + 1)
                time.sleep(wait)
                continue
            return None
        except Exception:
            return None
    return None


def enrich_online(entities: dict, relations: list) -> None:
    import time
    skills = [e for e in entities.values() if e["type"] == "Skill"]
    enriched = 0
    for skill in skills:
        slug = skill["properties"].get("slug") or skill["properties"].get("name", "")
        if not slug:
            continue
        data = _clawhub_get(f"skills/{slug}")
        if not data:
            continue
        s = data.get("skill", {})
        lv = data.get("latestVersion", {})
        owner = data.get("owner", {})
        mod = data.get("moderation") or {}
        stats = s.get("stats", {})

        updates: dict = {}
        if stats.get("stars") is not None:
            updates["stars"] = stats["stars"]
        if stats.get("downloads") is not None:
            updates["downloads"] = stats["downloads"]
        if stats.get("installsCurrent") is not None:
            updates["installs_current"] = stats["installsCurrent"]
        if owner.get("handle"):
            updates["owner_handle"] = owner["handle"]
        if lv.get("license"):
            updates.setdefault("license", lv["license"])
        if mod.get("verdict"):
            updates["moderation"] = mod["verdict"]

        if updates:
            ts = datetime.now(timezone.utc).isoformat()
            rec = {"op": "update", "id": skill["id"], "properties": updates, "timestamp": ts}
            _append_op_fallback(GRAPH_PATH, rec)
            skill["properties"].update(updates)
            enriched += 1
            print(f"    ✓ {slug} — stars:{updates.get('stars','?')} dl:{updates.get('downloads','?')}")

        time.sleep(0.4)  # stay within clawhub rate limits

    print(f"\n  Enriched {enriched}/{len(skills)} skills with online metadata.")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_scan(dirs: list[str]) -> None:
    Path(GRAPH_PATH).parent.mkdir(parents=True, exist_ok=True)
    entities, relations = _load(GRAPH_PATH)

    # Build effective scan roots:
    # - user-provided or DEFAULT_SCAN_ROOTS
    # - plus project-local ./skills (when this skill lives inside a project)
    # - plus global npm root: $(npm root -g)/openclaw/skills (when available)
    effective_dirs: list[str] = list(dirs)

    # Project-level skills directory: <project_root>/skills
    try:
        project_root = SKILL_CHAIN_ROOT.parent.parent.parent
        project_skills = project_root / "skills"
        if project_skills.exists():
            effective_dirs.append(str(project_skills))
    except Exception:
        pass

    # Global npm skills directory: $(npm root -g)/openclaw/skills
    try:
        proc = subprocess.run(
            ["npm", "root", "-g"],
            capture_output=True,
            text=True,
            timeout=3,
        )
        if proc.returncode == 0:
            npm_root = Path(proc.stdout.strip())
            global_skills = npm_root / "openclaw" / "skills"
            if global_skills.exists():
                effective_dirs.append(str(global_skills))
    except Exception:
        pass

    skill_dirs = find_skill_dirs(effective_dirs)
    if not skill_dirs:
        print("No skill directories found. Try --dirs <path>.")
        return

    print(f"Found {len(skill_dirs)} skill director{'y' if len(skill_dirs)==1 else 'ies'}.")

    # First pass: collect all slugs/names for cross-reference dep detection
    all_slugs: set[str] = set()
    parsed: list[tuple[Path, dict, dict]] = []
    for sd in skill_dirs:
        sm = parse_skill_md(sd / "SKILL.md")
        lm = read_local_meta(sd)
        slug = lm.get("slug") or sm.get("name", sd.name)
        all_slugs.add(slug)
        parsed.append((sd, sm, lm))

    # Second pass: ingest
    for sd, sm, lm in parsed:
        slug = lm.get("slug") or sm.get("name", sd.name)
        name = sm.get("name", slug)
        desc = sm.get("description", "")
        raw  = sm.get("raw", "")

        print(f"  → {slug}")

        props: dict = {
            "name":       name,
            "source":     "clawhub" if lm.get("registry") else "local",
            "status":     "active",
            "version":    lm.get("version", ""),
            "license":    sm.get("license") or "",
            "local_path": str(sd.resolve()),
            "last_scanned": datetime.now(timezone.utc).isoformat(),
        }
        if desc:
            props["description"] = desc[:500]

        skill_id = upsert_skill(entities, slug, props)

        # Categories
        for cat_name in infer_categories(name, desc):
            cat_id = upsert_category(entities, cat_name)
            add_rel(entities, relations, skill_id, "belongs_to_category", cat_id)

        # Tools
        for tool_info in detect_tools(sd, raw):
            tool_id = upsert_tool(entities, tool_info["name"],
                                  tool_info["kind"], tool_info.get("description", ""))
            add_rel(entities, relations, skill_id, "uses_tool", tool_id)

        # allowed-tools → invoked_via relations (e.g. Bash(agent-browser:*))
        for at in sm.get("allowed_tools", []):
            t_name = at["tool"]
            t_kind = "shell" if t_name.lower() in ("bash", "sh", "zsh") else "mcp"
            t_id = upsert_tool(entities, t_name, t_kind,
                               f"Invocation channel declared in allowed-tools")
            add_rel_with_props(entities, relations, skill_id, "invoked_via", t_id,
                               {"pattern": at.get("pattern", "*")})

        # metadata.requires.bins → requires_tool relations (e.g. node, npm, git)
        for bin_name in sm.get("requires_bins", []):
            t_id = upsert_tool(entities, bin_name, "cli-runtime",
                               f"Required binary declared in metadata.requires.bins")
            add_rel(entities, relations, skill_id, "requires_tool", t_id)

        # Store read_when count as a skill property (helps health scoring)
        rw = sm.get("read_when", [])
        if rw:
            ts = datetime.now(timezone.utc).isoformat()
            _append_op_fallback(GRAPH_PATH, {
                "op": "update", "id": skill_id,
                "properties": {"read_when_count": len(rw)},
                "timestamp": ts,
            })
            entities[skill_id]["properties"]["read_when_count"] = len(rw)

        # Declared packages (requirements.txt, pyproject.toml, Pipfile, package.json)
        declared_names: set[str] = set()
        for pkg in parse_requirements(sd):
            pkg_id = upsert_package(entities, pkg["name"], pkg["ecosystem"],
                                    pkg["spec"], pkg.get("source", ""))
            add_rel(entities, relations, skill_id, "requires_package", pkg_id)
            declared_names.add(pkg["name"])

        # Implicit packages from AST import scanning (not already declared)
        for pkg in scan_python_imports(sd):
            if pkg["name"] not in declared_names:
                pkg_id = upsert_package(entities, pkg["name"], pkg["ecosystem"],
                                        pkg["spec"], pkg.get("source", ""))
                add_rel(entities, relations, skill_id, "requires_package", pkg_id)

        # Skill-to-skill deps (other skills referenced in SKILL.md)
        other_slugs = all_slugs - {slug}
        for dep_slug in detect_skill_deps(raw, other_slugs):
            dep_id = _existing_id(entities, "Skill", "slug", dep_slug)
            if dep_id:
                add_rel(entities, relations, skill_id, "depends_on_skill", dep_id)

    total_skills = sum(1 for e in entities.values() if e["type"] == "Skill")
    total_pkgs   = sum(1 for e in entities.values() if e["type"] == "SoftwarePackage")
    print(f"\nGraph: {total_skills} skills, {total_pkgs} packages, {len(relations)} relations.")
    print(f"Stored in: {GRAPH_PATH}")


def cmd_enrich() -> None:
    print("Enriching with clawhub online metadata...")
    entities, relations = _load(GRAPH_PATH)
    if not entities:
        print("  Graph is empty — run `scan` first.")
        return
    enrich_online(entities, relations)


def cmd_status() -> None:
    entities, relations = _load(GRAPH_PATH)
    by_type: dict[str, int] = {}
    for e in entities.values():
        by_type[e["type"]] = by_type.get(e["type"], 0) + 1
    by_rel: dict[str, int] = {}
    for r in relations:
        by_rel[r["rel"]] = by_rel.get(r["rel"], 0) + 1

    print("=== SkillChain Graph Status ===")
    for t, n in sorted(by_type.items()):
        print(f"  {t:<20} {n}")
    print(f"  {'Relations':<20} {len(relations)}")
    if by_rel:
        print("\nRelation breakdown:")
        for r, n in sorted(by_rel.items(), key=lambda x: -x[1]):
            print(f"  {r:<30} {n}")


def cmd_reset() -> None:
    p = Path(GRAPH_PATH)
    if p.exists():
        p.write_text("")
        print(f"Graph cleared: {GRAPH_PATH}")
    else:
        print("Graph file does not exist yet.")


def cmd_analyze_all(dirs: list[str]) -> None:
    """One-shot: reset → scan → health → overlaps → report (with insights)."""
    import subprocess as _sp
    import sys as _sys

    analyze = Path(__file__).resolve().parent / "analyze.py"

    print("=" * 60)
    print("Step 1/4  Reset & Scan")
    print("=" * 60)
    cmd_reset()
    cmd_scan(dirs)

    for step, subcmd in [("Step 2/4  Health check", "health"),
                         ("Step 3/4  Overlap analysis", "overlaps"),
                         ("Step 4/4  Full report", "report")]:
        print()
        print("=" * 60)
        print(step)
        print("=" * 60)
        _sp.run([_sys.executable, str(analyze), subcmd], check=False)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="SkillChain ingest")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_scan = sub.add_parser("scan", help="Scan local skill directories")
    p_scan.add_argument("--dirs", nargs="+", default=DEFAULT_SCAN_ROOTS,
                        help="Root directories to scan (default: common skill paths)")

    p_all = sub.add_parser("analyze-all",
                           help="One-shot: reset + scan + health + overlaps + report")
    p_all.add_argument("--dirs", nargs="+", default=DEFAULT_SCAN_ROOTS,
                       help="Root directories to scan (default: common skill paths)")

    sub.add_parser("enrich", help="Enrich graph with clawhub online metadata")
    sub.add_parser("status", help="Show graph summary")
    sub.add_parser("reset",  help="Clear the graph")

    args = parser.parse_args()

    if args.cmd == "scan":
        cmd_scan(args.dirs)
    elif args.cmd == "analyze-all":
        cmd_analyze_all(args.dirs)
    elif args.cmd == "enrich":
        cmd_enrich()
    elif args.cmd == "status":
        cmd_status()
    elif args.cmd == "reset":
        cmd_reset()


if __name__ == "__main__":
    main()
