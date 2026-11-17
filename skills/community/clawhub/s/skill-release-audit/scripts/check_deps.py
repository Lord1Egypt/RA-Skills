#!/usr/bin/env python3
"""
Module 5: Dependency Declaration & Auto-Install
- Scan Python scripts for third-party imports
- Scan JS/TS for require/import
- Check shell for external binaries (jq, curl, gh, etc.)
- Compare against what's installed
- Auto-install missing Python deps (with user confirmation baked into main flow)
- Surface install commands for Node / bins
"""

import ast
import importlib.util
import re
import shutil
import subprocess
import sys
from pathlib import Path

from _common import split_frontmatter, find_sibling_skill_scripts
from i18n import t


def _as_str_list(val) -> list[str]:
    """Coerce a frontmatter value into a clean list of strings.

    Handles the yaml path (already a list) and the fallback path
    (an inline `[a, b]` string or a comma-separated string).
    """
    if val is None:
        return []
    if isinstance(val, dict):
        # Malformed declaration (e.g. `python:` written as a YAML map) — ignore
        # rather than stringify the dict into a junk "package name".
        return []
    if isinstance(val, (list, tuple)):
        return [str(x).strip().strip('"\'') for x in val if str(x).strip()]
    s = str(val).strip()
    if s.startswith("[") and s.endswith("]"):
        s = s[1:-1]
    return [x.strip().strip('"\'') for x in s.split(",") if x.strip()]

# ---------------------------------------------------------------------------
# Python standard library modules (rough list to avoid false positives)
# ---------------------------------------------------------------------------
STDLIB_MODULES = set(sys.stdlib_module_names) if hasattr(sys, "stdlib_module_names") else {
    "os", "sys", "re", "json", "pathlib", "subprocess", "typing", "collections",
    "itertools", "functools", "math", "datetime", "time", "random", "hashlib",
    "hmac", "base64", "urllib", "http", "email", "html", "xml", "csv", "io",
    "string", "struct", "copy", "pprint", "textwrap", "logging", "warnings",
    "contextlib", "abc", "enum", "dataclasses", "argparse", "configparser",
    "tempfile", "shutil", "glob", "fnmatch", "stat", "pwd", "grp", "signal",
    "traceback", "inspect", "types", "weakref", "gc", "platform", "socket",
    "ssl", "select", "threading", "multiprocessing", "asyncio", "concurrent",
    "queue", "unittest", "doctest", "ast", "dis", "token", "tokenize",
    "zipfile", "tarfile", "gzip", "bz2", "lzma", "zlib", "sqlite3",
    "pickle", "shelve", "marshal", "struct", "array", "mmap", "uuid",
    "secrets", "getpass", "locale", "codecs", "unicodedata", "difflib",
    "heapq", "bisect", "decimal", "fractions", "statistics", "cmath",
    "builtins", "__future__", "importlib", "pkgutil",
}

# Map common package names to their pip install names
PIP_INSTALL_MAP = {
    "yaml": "pyyaml",
    "cv2": "opencv-python",
    "PIL": "Pillow",
    "sklearn": "scikit-learn",
    "bs4": "beautifulsoup4",
    "dotenv": "python-dotenv",
    "dateutil": "python-dateutil",
    "jwt": "PyJWT",
    "Crypto": "pycryptodome",
    "OpenSSL": "pyOpenSSL",
    "serial": "pyserial",
    "usb": "pyusb",
    "magic": "python-magic",
    "toml": "toml",
    "tomli": "tomli",
    "tomllib": "tomllib",
    "aiofiles": "aiofiles",
    "httpx": "httpx",
    "requests": "requests",
    "aiohttp": "aiohttp",
    "fastapi": "fastapi",
    "pydantic": "pydantic",
    "click": "click",
    "rich": "rich",
    "typer": "typer",
    "tqdm": "tqdm",
    "numpy": "numpy",
    "pandas": "pandas",
    "matplotlib": "matplotlib",
}

# Common system binaries that skills might use
COMMON_BINS = {
    "jq", "curl", "wget", "gh", "git", "docker", "kubectl",
    "node", "npm", "npx", "bunx", "python3", "pip3",
    "ffmpeg", "convert", "pdftk", "pandoc",
}


# ---------------------------------------------------------------------------
# Extract Python imports
# ---------------------------------------------------------------------------

def extract_python_imports(script_path: Path) -> set[str]:
    """Return set of top-level module names imported in a Python file."""
    modules = set()
    try:
        source = script_path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except Exception:
        return modules

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                modules.add(node.module.split(".")[0])

    return modules


def is_installed(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None


def pip_package_name(module_name: str) -> str:
    return PIP_INSTALL_MAP.get(module_name, module_name)


# ---------------------------------------------------------------------------
# Node.js built-in modules (no install needed)
# ---------------------------------------------------------------------------
NODE_BUILTIN_MODULES = {
    "assert", "async_hooks", "buffer", "child_process", "cluster",
    "console", "constants", "crypto", "dgram", "diagnostics_channel",
    "dns", "domain", "events", "fs", "http", "http2", "https",
    "inspector", "module", "net", "os", "path", "perf_hooks",
    "process", "punycode", "querystring", "readline", "repl",
    "stream", "string_decoder", "sys", "timers", "tls", "trace_events",
    "tty", "url", "util", "v8", "vm", "wasi", "worker_threads", "zlib",
    # Node 18+ additions
    "node:fs", "node:path", "node:crypto", "node:http", "node:https",
    "node:os", "node:util", "node:stream", "node:buffer",
}


# ---------------------------------------------------------------------------
# Extract Node.js requires/imports
# ---------------------------------------------------------------------------

def extract_node_deps(script_path: Path) -> set[str]:
    deps = set()
    try:
        text = script_path.read_text(encoding="utf-8")
    except Exception:
        return deps

    # require('pkg') / require("pkg")
    for m in re.finditer(r"""require\s*\(\s*['"]([^'"./][^'"]*)['"]\s*\)""", text):
        deps.add(m.group(1).split("/")[0])  # handle scoped @org/pkg

    # import ... from 'pkg'
    for m in re.finditer(r"""import\s+.*?\s+from\s+['"]([^'"./][^'"]*)['"]\s*""", text):
        deps.add(m.group(1).split("/")[0])

    return deps


def check_node_dep_installed(pkg: str, script_path: Path) -> bool:
    """Check if a node module is in node_modules adjacent to script."""
    node_modules = script_path.parent / "node_modules" / pkg
    if node_modules.exists():
        return True
    # Also check workspace-level
    workspace_nm = Path.home() / ".openclaw" / "workspace" / "node_modules" / pkg
    return workspace_nm.exists()


# ---------------------------------------------------------------------------
# Extract shell binary dependencies
# ---------------------------------------------------------------------------

def extract_shell_bins(script_path: Path) -> set[str]:
    bins = set()
    try:
        text = script_path.read_text(encoding="utf-8")
    except Exception:
        return bins

    # command -v <bin> patterns
    for m in re.finditer(r'command\s+-v\s+(\w[\w-]*)', text):
        bins.add(m.group(1))

    # which <bin>
    for m in re.finditer(r'which\s+(\w[\w-]*)', text):
        bins.add(m.group(1))

    # Direct usage of known bins
    for b in COMMON_BINS:
        if re.search(rf'\b{re.escape(b)}\b', text):
            bins.add(b)

    return bins


# ---------------------------------------------------------------------------
# SKILL.md declared deps
# ---------------------------------------------------------------------------

def extract_declared_deps(skill_dir: Path) -> dict:
    """Parse frontmatter requires.bins / requires.python / python_optional / depends_on_skills from SKILL.md.

    支持字段：
      - bins / python: 必需的系统命令/Python 包
      - python_optional: 可选 Python 包（如某 executor 才需要的依赖）
      - depends_on_skills: 依赖的其它 skill（运行时按需下载安装，audit 不应把其 import 判为缺失）
    """
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return {}

    content = skill_md.read_text(encoding="utf-8")
    fm, fm_raw, _body = split_frontmatter(content)
    if not fm and not fm_raw:
        return {}

    declared: dict = {}

    # Preferred path: top-level keys parsed by split_frontmatter (yaml list when
    # PyYAML is present, inline `[a, b]` string on the fallback parser).
    field_keys = ["bins", "python", "python_optional", "depends_on_skills"]

    for key in field_keys:
        if key in fm:
            vals = _as_str_list(fm[key])
            if vals:
                declared[key] = vals

    # Fallback (only when the structured parse missed a key): match a TOP-LEVEL
    # `key: [ ... ]` line in the raw frontmatter. Anchored to column 0 (no leading
    # whitespace) so it does NOT accidentally pick up indented/nested lines or a
    # `key: [...]` substring buried inside a multi-line description block.
    for key in field_keys:
        if key in declared:
            continue
        m = re.search(rf'(?m)^{re.escape(key)}\s*:\s*\[([^\]]*)\]', fm_raw)
        if m:
            vals = _as_str_list(m.group(1))
            if vals:
                declared[key] = vals

    return declared


# ---------------------------------------------------------------------------
# Declaration-vs-code env check — delegated to _env_check classifier (v1.1)
#
# The old "reads env == must declare" logic moved to scripts/_env_check.py:
# per-access records → required/optional/runtime/ambient/test/review
# classification → per-finding-code profile severity. Contract lists live in
# config/env_contracts.json. Kept here: thin wrappers for backward compat.
# ---------------------------------------------------------------------------

sys.path.insert(0, str(Path(__file__).parent))
from _env_check import check_env_declarations  # noqa: E402


def extract_declared_env(skill_dir: Path) -> "set[str]":
    """Collect env vars declared in frontmatter under the ClawHub schema:
    metadata.openclaw.requires.env / primaryEnv / envVars[].name (aliases:
    metadata.clawdbot / metadata.clawdis).
    """
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return set()
    fm, _raw, _body = split_frontmatter(skill_md.read_text(encoding="utf-8"))
    declared: set[str] = set()

    meta = fm.get("metadata")
    if not isinstance(meta, dict):
        return declared
    for alias in ("openclaw", "clawdbot", "clawdis"):
        block = meta.get(alias)
        if not isinstance(block, dict):
            continue
        primary = block.get("primaryEnv")
        if isinstance(primary, str) and primary.strip():
            declared.add(primary.strip())
        req = block.get("requires")
        if isinstance(req, dict):
            for e in _as_str_list(req.get("env")):
                declared.add(e)
        env_vars = block.get("envVars")
        if isinstance(env_vars, list):
            for ev in env_vars:
                if isinstance(ev, dict) and isinstance(ev.get("name"), str):
                    declared.add(ev["name"].strip())
    return declared


def check_declaration_vs_code(skill_dir: Path, severity: str = "WARN",
                              profile: dict | None = None) -> "list[dict]":
    """Classified env declaration check (false-positive governance v1.1).

    Each visible finding becomes one issue with code/variable/location/reason
    — no more single aggregated WARN. `severity` is kept for backward
    compatibility (legacy declaration_vs_code profile key) and maps onto the
    ENV_REQUIRED_UNDECLARED code when the profile lacks per-code config.
    """
    declared = extract_declared_env(skill_dir)
    prof = dict(profile or {})
    if severity and severity.upper() not in ("OFF",):
        prof.setdefault("env_severity", {})
        # explicit --severity arg wins over profile only when the profile has
        # no per-code config of its own
        if "ENV_REQUIRED_UNDECLARED" not in prof["env_severity"]:
            prof["env_severity"]["ENV_REQUIRED_UNDECLARED"] = severity
    result = check_env_declarations(skill_dir, declared, prof)

    issues = []
    for fd in result["issues"]:
        msg = t("deps.env_finding",
                code=fd.get("code", ""), variable=fd.get("variable", ""),
                file=fd.get("file", ""), line=fd.get("line") or 0,
                access=fd.get("access", ""), reason=fd.get("reason", ""))
        issues.append({
            "file": fd["file"],
            "line": fd.get("line"),
            "message": msg,
            "severity": fd["severity"],
            "code": fd.get("code", ""),
            "variable": fd.get("variable", ""),
        })
    return issues


# ---------------------------------------------------------------------------
# Auto-install Python deps
# ---------------------------------------------------------------------------

def try_install_python_pkg(pkg_name: str, timeout: int = 60) -> tuple[bool, str]:
    """Attempt pip install. Returns (success, message)."""
    pip_name = pip_package_name(pkg_name)
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", pip_name, "--quiet"],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return False, t("deps.install_timeout", timeout=timeout)
    except Exception as e:
        return False, str(e)
    if result.returncode == 0:
        return True, t("deps.installed", pip=pip_name)
    else:
        err = result.stderr.strip().splitlines()[-1] if result.stderr.strip() else t("deps.unknown_error")
        return False, err


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

def run(skill_dir: Path, auto_install: bool = False, install_timeout: int = 60,
        profile: dict | None = None) -> dict:
    issues = []
    auto_installed = []
    install_failed = []

    scripts_dir = skill_dir / "scripts"
    all_python_deps: set[str] = set()
    all_node_deps: set[str] = set()
    all_bins: set[str] = set()
    node_scripts: list[Path] = []
    shell_scripts: list[Path] = []

    # 提前解析 frontmatter（含 python_optional / depends_on_skills），后面多处复用
    declared_for_filter = extract_declared_deps(skill_dir)

    # Local module names (scripts in the same directory — not third-party)
    local_modules: set[str] = set()
    if scripts_dir.exists():
        local_modules = {f.stem for f in scripts_dir.glob("*.py")}

    # 把 depends_on_skills 声明的兄弟 skill 的 scripts/ 顶层 .py 视为 local
    # （它们运行时会被自动下载安装 + 注入 sys.path，audit 不应判为缺失）
    dep_skills = declared_for_filter.get("depends_on_skills") or []
    if dep_skills:
        for dep in dep_skills:
            dep_scripts = find_sibling_skill_scripts(skill_dir, dep)
            if dep_scripts is not None:
                local_modules |= {f.stem for f in dep_scripts.glob("*.py")}
            # If the sibling skill isn't present locally (first-time audit), its
            # module names can't be scanned; we rely on python_optional / docs and
            # only WARN (never ERROR) — handled below.

    # python_optional：可选依赖不算缺失（缺失只给 INFO，不 ERROR/WARN）
    optional_modules: set[str] = set(declared_for_filter.get("python_optional") or [])

    if scripts_dir.exists():
        for script in scripts_dir.iterdir():
            if not script.is_file():
                continue
            if script.suffix == ".py":
                all_python_deps.update(extract_python_imports(script))
            elif script.suffix in {".js", ".ts", ".mjs", ".cjs"}:
                all_node_deps.update(extract_node_deps(script))
                node_scripts.append(script)
            elif script.suffix == ".sh":
                all_bins.update(extract_shell_bins(script))
                shell_scripts.append(script)

    # ----- Python deps -----
    third_party = {
        m for m in all_python_deps
        if m
        and m not in STDLIB_MODULES
        and m not in local_modules
        and not m.startswith("_")
    }
    # 拆分必需 vs 可选（optional）
    third_party_required = third_party - optional_modules
    third_party_optional_missing = (third_party & optional_modules)  # optional 且实际被 import 的

    for pkg in sorted(third_party_required):
        if not is_installed(pkg):
            if auto_install:
                ok, msg = try_install_python_pkg(pkg, timeout=install_timeout)
                if ok:
                    auto_installed.append(pkg)
                else:
                    install_failed.append((pkg, msg))
                    pip_name = pip_package_name(pkg)
                    # Install failure is a WARN, not ERROR: the dependency itself
                    # may be valid — the failure is usually an environment/network
                    # issue (offline registry, timeout) that shouldn't fail the audit.
                    issues.append({
                        "file": "scripts/",
                        "line": None,
                        "message": t("deps.py_install_failed", pkg=pkg, msg=msg, pip=pip_name),
                        "severity": "WARN",
                        "install_cmd": f"pip install {pip_name}",
                        "docs_url": f"https://pypi.org/project/{pip_name}/",
                    })
            else:
                pip_name = pip_package_name(pkg)
                issues.append({
                    "file": "scripts/",
                    "line": None,
                    "message": t("deps.py_missing", pkg=pkg),
                    "severity": "ERROR",
                    "install_cmd": f"pip install {pip_name}",
                })

    # python_optional 缺失只 INFO，不报 ERROR/WARN（这是声明意图：用户按场景手动装）
    for pkg in sorted(third_party_optional_missing):
        if not is_installed(pkg):
            pip_name = pip_package_name(pkg)
            issues.append({
                "file": "SKILL.md",
                "line": None,
                "message": t("deps.py_optional_missing", pkg=pkg, pip=pip_name),
                "severity": "INFO",
            })

    # ----- Node deps -----
    for pkg in sorted(all_node_deps):
        # Skip Node.js built-in modules
        bare = pkg.removeprefix("node:") if pkg.startswith("node:") else pkg
        if bare in NODE_BUILTIN_MODULES or pkg in NODE_BUILTIN_MODULES:
            continue
        if not check_node_dep_installed(pkg, scripts_dir / "placeholder"):
            issues.append({
                "file": "scripts/",
                "line": None,
                "message": t("deps.node_missing", pkg=pkg),
                "severity": "ERROR",
                "install_cmd": f"npm install {pkg}",
                "docs_url": f"https://www.npmjs.com/package/{pkg}",
            })

    # ----- System bins -----
    known_bins = all_bins & COMMON_BINS
    for b in sorted(known_bins):
        if not shutil.which(b):
            issues.append({
                "file": "scripts/",
                "line": None,
                "message": t("deps.bin_missing", b=b),
                "severity": "WARN",
                "install_cmd": _bin_install_hint(b),
            })

    # ----- SKILL.md declaration gap -----
    declared = declared_for_filter  # 复用上面的解析结果
    declared_py = set(declared.get("python", []))
    declared_py_optional = set(declared.get("python_optional", []))
    declared_bins = set(declared.get("bins", []))

    # 未声明 = 第三方 import - 必需声明 - 可选声明 - depends_on_skills 提供的模块
    # （depends_on_skills 兄弟 skill 的模块已加进 local_modules，third_party 已过滤掉，
    #  这里只需再减 optional 即可）
    undeclared_py = third_party - declared_py - declared_py_optional
    undeclared_bins = (known_bins & COMMON_BINS) - declared_bins

    if undeclared_py:
        issues.append({
            "file": "SKILL.md",
            "line": None,
            "message": t("deps.py_undeclared", pkgs=', '.join(sorted(undeclared_py))),
            "severity": "WARN",
        })

    if undeclared_bins:
        issues.append({
            "file": "SKILL.md",
            "line": None,
            "message": t("deps.bin_undeclared", bins=', '.join(sorted(undeclared_bins))),
            "severity": "WARN",
        })

    # ----- Declaration-vs-code env check (classified, profile-driven) -----
    decl_severity = (profile or {}).get("declaration_vs_code", "WARN")
    issues.extend(check_declaration_vs_code(skill_dir, severity=decl_severity,
                                            profile=profile))
    # Machine-readable evidence for JSON mode: classified hidden findings
    # (optional / runtime / ambient / review) ride along, never counted as WARN.
    try:
        from _env_check import check_env_declarations as _cec
        _decl_env = extract_declared_env(skill_dir)
        _env_full = _cec(skill_dir, _decl_env, profile or {})
        env_evidence = _env_full.get("evidence", [])
    except Exception:
        env_evidence = []

    errors = [i for i in issues if i["severity"] == "ERROR"]
    warnings = [i for i in issues if i["severity"] == "WARN"]

    result = {
        "module": t("module.deps"),
        "status": "FAIL" if errors else ("WARN" if warnings else "PASS"),
        "issues": issues,
        "auto_installed": auto_installed,
        "install_failed": [pkg for pkg, _ in install_failed],
    }
    if env_evidence:
        result["env_evidence"] = env_evidence
    return result


def _bin_install_hint(bin_name: str) -> str:
    hints = {
        "jq": "brew install jq  # 或 apt-get install jq",
        "curl": "brew install curl  # 或 apt-get install curl",
        "wget": "brew install wget  # 或 apt-get install wget",
        "gh": "brew install gh  # 或 https://cli.github.com",
        "git": "brew install git  # 或 apt-get install git",
        "docker": "https://docs.docker.com/get-docker/",
        "ffmpeg": "brew install ffmpeg  # 或 apt-get install ffmpeg",
        "node": "https://nodejs.org/",
        "npm": "随 Node.js 一起安装: https://nodejs.org/",
        "pandoc": "brew install pandoc  # 或 https://pandoc.org/installing.html",
    }
    return hints.get(bin_name, t("deps.install_hint_generic", bin=bin_name))
