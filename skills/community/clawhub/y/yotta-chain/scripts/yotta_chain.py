#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""yotta-chain (yuan lian) - supply chain dependency validation engine.

Zero-dependency Python 3.8+ implementation (standard library only).

Scope (v0.1.2):
  - npm   : package.json + package-lock.json (v1/v2/v3) + npm-shrinkwrap.json + .npmrc
  - python: requirements*.txt + pyproject.toml (PEP 621 / poetry) + poetry.lock
            + Pipfile / Pipfile.lock
  - maven : pom.xml (basic: unpinned / SNAPSHOT / suspicious repository URLs)

Checks:
  - dependency confusion : registry config vs lockfile resolved URLs, mixed
    registries, suspicious (http / IP-literal / localhost) registry URLs,
    extra-index fallback mixing
  - lockfile consistency : manifest entry missing, range unsatisfied, root
    mismatch, dangling references, missing integrity, duplicate conflicts
  - hygiene              : missing lockfile, unpinned versions, SNAPSHOT
  - typosquat            : name resembles a popular package (edit distance)

No online CVE lookups; fully local and offline. SBOM-lite output is a
CycloneDX 1.5 JSON subset.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

VERSION = "0.1.7"

SEVERITY_ORDER = ["info", "low", "medium", "high"]
SEVERITY_RANK = {s: i for i, s in enumerate(SEVERITY_ORDER)}


class Finding:
    """A single validation finding."""

    __slots__ = ("rule", "severity", "file", "line", "package", "message", "detail", "ecosystem")

    def __init__(self, rule, severity, file, package, message, detail="", line=None, ecosystem=""):
        self.rule = rule
        self.severity = severity
        self.file = file
        self.line = line
        self.package = package
        self.message = message
        self.detail = detail
        self.ecosystem = ecosystem

    def to_dict(self):
        return {
            "rule": self.rule,
            "severity": self.severity,
            "file": self.file,
            "line": self.line,
            "package": self.package,
            "message": self.message,
            "detail": self.detail,
            "ecosystem": self.ecosystem,
        }


# --------------------------------------------------------------------------
# small text / url helpers
# --------------------------------------------------------------------------

def _read_text(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _url_host(url):
    """Return (scheme, host, port) for a registry/package URL, else None."""
    if not url:
        return None
    m = re.match(r"^(https?)://([^/:]+)(?::(\d+))?", url.strip())
    if not m:
        return None
    return m.group(1), m.group(2), m.group(3)


_IPV4_RE = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")


def _is_suspicious_url(url):
    """Return (bool, reason) for http://, IP-literal, localhost hosts."""
    if not url:
        return False, ""
    host = _url_host(url)
    if host is None:
        return False, ""
    scheme, h, _port = host
    if scheme != "https":
        return True, "非 HTTPS 的仓库地址（http://），传输与完整性易被篡改"
    if h in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
        return True, "仓库地址指向本机（%s），正常发布环境不应使用" % h
    if _IPV4_RE.match(h):
        return True, "仓库地址使用 IP 字面量（%s），建议改用域名并校验来源" % h
    return False, ""


def _norm_pkg(name):
    return (name or "").strip().lower()


# --------------------------------------------------------------------------
# Damerau-Levenshtein (for typosquat)
# --------------------------------------------------------------------------

def _damerau_levenshtein(a, b):
    """Return edit distance with adjacent transpositions (DL distance)."""
    la, lb = len(a), len(b)
    if abs(la - lb) > 2:
        return abs(la - lb) + 1
    d = [[0] * (lb + 1) for _ in range(la + 1)]
    for i in range(la + 1):
        d[i][0] = i
    for j in range(lb + 1):
        d[0][j] = j
    for i in range(1, la + 1):
        for j in range(1, lb + 1):
            cost = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(
                d[i - 1][j] + 1,
                d[i][j - 1] + 1,
                d[i - 1][j - 1] + cost,
            )
            if i > 1 and j > 1 and a[i - 1] == b[j - 2] and a[i - 2] == b[j - 1]:
                d[i][j] = min(d[i][j], d[i - 2][j - 2] + 1)
    return d[la][lb]


POPULAR_NPM = [
    "lodash", "express", "react", "request", "axios", "chalk", "commander",
    "debug", "dotenv", "eslint", "moment", "uuid", "yargs", "webpack",
    "typescript", "jest", "babel-core", "vue", "react-dom", "bluebird",
    "underscore", "minimist", "semver", "rimraf", "mkdirp", "glob", "async",
    "q", "inherits", "readable-stream", "string-width", "ansi-regex",
    "is-number", "isarray", "tslib", "core-js", "node-fetch", "fast-glob",
    "postcss", "autoprefixer", "esbuild", "rollup", "vite", "next", "gulp",
    "grunt", "webpack-cli", "cross-env", "concurrently", "nodemon",
    "prettier", "husky", "lint-staged", "js-yaml", "yaml", "fs-extra",
    "supports-color", "picocolors", "schema-utils", "serialize-javascript",
    "source-map", "path-exists", "p-limit", "safe-buffer", "util-deprecate",
    "brace-expansion", "balanced-match", "has-flag", "color-convert",
]

POPULAR_PYPI = [
    "requests", "urllib3", "flask", "django", "numpy", "pandas", "scipy",
    "pytest", "setuptools", "pip", "wheel", "cryptography", "pyyaml",
    "beautifulsoup4", "lxml", "jinja2", "sqlalchemy", "fastapi", "tornado",
    "aiohttp", "click", "tqdm", "matplotlib", "pillow", "six",
    "python-dateutil", "idna", "certifi", "charset-normalizer",
    "typing-extensions", "pydantic", "starlette", "uvicorn", "greenlet",
    "markupsafe", "packaging", "docutils", "sphinx", "celery", "redis",
    "boto3", "botocore", "kubernetes", "grpcio", "protobuf", "docker",
    "openpyxl", "xlsxwriter", "mypy", "black", "ruff", "coverage", "isort",
]


def find_typosquat(name, popular):
    """Return (legit_name, distance) if name resembles a popular package."""
    n = _norm_pkg(name)
    if not n or n in popular:
        return None
    best = None
    best_d = 99
    for p in popular:
        d = _damerau_levenshtein(n, p)
        if d < best_d:
            best_d = d
            best = p
        if best_d <= 1:
            break
    if best is not None and best_d <= 2 and abs(len(n) - len(best)) <= 2:
        return best, best_d
    # direct concatenation variant: name == popular without hyphen separators
    for p in popular:
        if n == p.replace("-", "") and len(p) >= 5:
            return p, 1
    return None


# --------------------------------------------------------------------------
# npm semver (subset sufficient for range checks)
# --------------------------------------------------------------------------

_RE_SEMVER = re.compile(
    r"^v?(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:-([0-9A-Za-z.-]+))?(?:\+[0-9A-Za-z.-]+)?$"
)


def parse_version(v):
    """Parse an npm-style version into (major, minor, patch, prerelease)."""
    if not v:
        return None
    m = _RE_SEMVER.match(v.strip())
    if not m:
        return None
    return (
        int(m.group(1)),
        int(m.group(2) or 0),
        int(m.group(3) or 0),
        m.group(4),
    )


def _pre_key(pre):
    if pre is None:
        return (1 << 30,)
    parts = []
    for p in pre.split("."):
        parts.append(int(p) if p.isdigit() else p)
    return tuple(parts)


def _ver_key(v):
    return (v[0], v[1], v[2], _pre_key(v[3]))


def _cmp_ver(a, b):
    if a is None or b is None:
        return 0
    ka, kb = _ver_key(a), _ver_key(b)
    return (ka > kb) - (ka < kb)


def _parse_ver_part(s):
    """Parse a version token that may be partial (1, 1.2, 1.2.x, *) or exact (1.2.3)."""
    s = s.strip().lower()
    if s in ("*", "x", "latest", ""):
        return "any", None
    if re.fullmatch(r"\d+", s):
        return "range", (int(s), None, None)
    if re.fullmatch(r"\d+\.\d+", s):
        mj, mn = s.split(".")
        return "range", (int(mj), int(mn), None)
    if re.fullmatch(r"\d+\.\d+\.\d+", s):
        return "exact", parse_version(s)
    m = re.fullmatch(r"(\d+)(?:\.(\d+))?\.(x|\*)", s)
    if m:
        mj = int(m.group(1))
        mn = int(m.group(2)) if m.group(2) else None
        return "range", (mj, mn, None)
    return "exact", parse_version(s)



def _cmp_partial(ver, part):
    """Compare version tuple against a partial (mj, mn, pt|None) tuple."""
    mj, mn, pt = part
    if ver[0] != mj:
        return (ver[0] > mj) - (ver[0] < mj)
    if mn is not None:
        if ver[1] != mn:
            return (ver[1] > mn) - (ver[1] < mn)
        if pt is not None and ver[2] != pt:
            return (ver[2] > pt) - (ver[2] < pt)
    return 0


def _lower_full(base):
    mj, mn, pt = base
    return (mj, mn if mn is not None else 0, pt if pt is not None else 0, None)


def _caret_upper(base):
    mj, mn, pt = base
    if mn is None:
        return (mj + 1, 0, 0)
    if mj > 0:
        return (mj + 1, 0, 0)
    if pt is None:
        return (0, mn + 1, 0)
    if mn > 0:
        return (0, mn + 1, 0)
    return (0, 0, pt + 1)


def _tilde_upper(base):
    mj, mn, _pt = base
    if mn is None:
        return (mj + 1, 0, 0)
    return (mj, mn + 1, 0)


def _semver_satisfies_one(ver, tok):
    """Satisfy a single comparator token (already expanded, no OR)."""
    tok = tok.strip()
    if not tok:
        return True
    m = re.match(r"^(>=|<=|>|<|=|~|\^)?\s*(.+)$", tok)
    op = m.group(1) or ""
    rest = m.group(2).strip()
    kind, base = _parse_ver_part(rest)
    if kind == "any":
        return True
    if kind == "range":
        # partial version: 1 / 1.2 / 1.x / 1.2.x
        if op == "^":
            return _cmp_ver(ver, _lower_full(base)) >= 0 and _cmp_partial(ver, _caret_upper(base)) < 0
        if op == "~":
            return _cmp_ver(ver, _lower_full(base)) >= 0 and _cmp_partial(ver, _tilde_upper(base)) < 0
        if op in ("", "="):
            return _cmp_partial(ver, base) == 0
        if op == ">=":
            return _cmp_ver(ver, _lower_full(base)) >= 0
        if op == ">":
            return _cmp_ver(ver, _lower_full(base)) > 0
        if op == "<=":
            return _cmp_partial(ver, base) <= 0
        if op == "<":
            return _cmp_partial(ver, base) < 0
        return _cmp_partial(ver, base) == 0
    if kind == "exact":
        if base is None:
            return False
        if op in ("", "="):
            return _cmp_ver(ver, base) == 0
        if op == ">=":
            return _cmp_ver(ver, base) >= 0
        if op == "<=":
            return _cmp_ver(ver, base) <= 0
        if op == ">":
            return _cmp_ver(ver, base) > 0
        if op == "<":
            return _cmp_ver(ver, base) < 0
        if op == "~":
            return _cmp_ver(ver, base) >= 0 and _cmp_partial(ver, _tilde_upper(base[:3])) < 0
        if op == "^":
            return _cmp_ver(ver, base) >= 0 and _cmp_partial(ver, _caret_upper(base[:3])) < 0
    return False



def semver_satisfies(version, range_str):
    """npm-style range satisfaction (^ ~ >= <= > < =, x-ranges, ||, hyphen)."""
    if version is None:
        return False
    ver = parse_version(version)
    if ver is None:
        return False
    range_str = (range_str or "").strip()
    if not range_str or range_str in ("*", "latest", "x", ""):
        return True
    for alt in range_str.split("||"):
        if _semver_satisfies_alt(ver, alt.strip()):
            return True
    return False


def _semver_satisfies_alt(ver, alt):
    # hyphen range: "1.2.3 - 2.3.4"
    m = re.match(r"^(\S+)\s+-\s+(\S+)$", alt)
    if m:
        lo = parse_version(m.group(1))
        hi = parse_version(m.group(2))
        if lo and hi:
            return _cmp_ver(ver, lo) >= 0 and _cmp_ver(ver, hi) <= 0
    toks = re.split(r"[\s,]+", alt)
    toks = [t for t in toks if t and t != "-"]
    if not toks:
        return True
    # npm rule: prerelease versions are excluded unless a comparator has
    # a prerelease on the same [major, minor, patch].
    if ver[3]:
        same = False
        for t in toks:
            mm = re.match(r"^(>=|<=|>|<|=|~|\^)?\s*(.+)$", t)
            rest = mm.group(2).strip() if mm else t
            b = parse_version(rest)
            if b and b[3] and b[0:3] == ver[0:3]:
                same = True
                break
        if not same:
            return False
    return all(_semver_satisfies_one(ver, t) for t in toks)


# --------------------------------------------------------------------------
# PEP 440 (python versions / specifiers, basic)
# --------------------------------------------------------------------------

_RE_PEP440 = re.compile(
    r"^v?(\d+)(?:\.(\d+))?(?:\.(\d+))?(?:\.(\d+))?"
    r"(?:(?:a|b|rc)(\d+))?(?:\.?(?:post|rev|r)(\d+))?"
    r"(?:\.?dev(\d+))?(?:\+[0-9A-Za-z.-]+)?$"
)


def parse_pep440(v):
    """Parse a PEP 440 version into (release, pre, post, dev)."""
    if not v:
        return None
    s = v.strip().lstrip("v")
    m = _RE_PEP440.match(s)
    if not m:
        return None
    rel = tuple(int(x or 0) for x in m.group(1, 2, 3, 4))
    pre = m.group(5)
    post = m.group(6)
    dev = m.group(7)
    return rel, pre, post, dev


def _pep_key(v):
    rel, pre, post, dev = v
    if dev is not None:
        return (rel, -3, int(dev), 0)
    if pre is not None:
        return (rel, -2, int(pre), 0)
    if post is not None:
        return (rel, 1, int(post), 0)
    return (rel, 0, 0, 0)


def _pep_cmp(a, b):
    if a is None or b is None:
        return 0
    ka, kb = _pep_key(a), _pep_key(b)
    return (ka > kb) - (ka < kb)


def _pep_match_operator(ver, op, rest):
    rest = rest.strip()
    if op == "==" and rest.endswith(".*"):
        prefix = rest[:-2].strip().lstrip("v")
        parts = [p for p in prefix.split(".") if p != ""]
        rel = ver[0]
        if len(parts) > len(rel):
            return False
        for i, p in enumerate(parts):
            if not p.isdigit() or int(p) != rel[i]:
                return False
        return True
    b = parse_pep440(rest)
    if b is None:
        return False
    c = _pep_cmp(ver, b)
    if op in ("==", ""):
        return c == 0
    if op == "!=":
        return c != 0
    if op == ">=":
        return c >= 0
    if op == "<=":
        return c <= 0
    if op == ">":
        return c > 0
    if op == "<":
        return c < 0
    if op == "~=":
        # compatible release: >= b, and first two segments equal
        rel = b[0]
        if len(rel) >= 2:
            return c >= 0 and rel[:2] == ver[0][:2]
        return c >= 0
    return False


def pep440_satisfies(version, spec):
    """PEP 440 specifier satisfaction (==,!=,<=,>=,<,>,~=,===, comma AND, || OR)."""
    ver = parse_pep440(version)
    if ver is None:
        return False
    spec = (spec or "").strip()
    if not spec:
        return True
    for alt in spec.split("||"):
        ok = True
        for part in alt.split(","):
            part = part.strip()
            if not part:
                continue
            m = re.match(r"^(===|==|!=|<=|>=|~=|>|<|\s*)(.+)$", part)
            op = (m.group(1) or "").strip()
            rest = m.group(2) if m else part
            if not _pep_match_operator(ver, op, rest):
                ok = False
                break
        if ok:
            return True
    return False


# --------------------------------------------------------------------------
# minimal TOML parser (subsets used by pyproject.toml / Pipfile / poetry.lock)
# --------------------------------------------------------------------------

def _find_eq_outside_string(line):
    in_str = False
    q = None
    for i, ch in enumerate(line):
        if in_str:
            if ch == q:
                in_str = False
        else:
            if ch in ('"', "'"):
                in_str = True
                q = ch
            elif ch == "=":
                return i
    return None


def _toml_unescape(s):
    out = []
    i = 0
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s):
            nxt = s[i + 1]
            mp = {"n": "\n", "t": "\t", "r": "\r", '"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f"}
            out.append(mp.get(nxt, nxt))
            i += 2
        else:
            out.append(ch)
            i += 1
    return "".join(out)


def _toml_string(s):
    s = s.strip()
    if s.startswith('"""') and s.endswith('"""') and len(s) >= 6:
        return _toml_unescape(s[3:-3].strip("\n"))
    if s.startswith("'''") and s.endswith("'''") and len(s) >= 6:
        return s[3:-3].strip("\n")
    if s.startswith('"') and s.endswith('"') and len(s) >= 2:
        return _toml_unescape(s[1:-1])
    if s.startswith("'") and s.endswith("'") and len(s) >= 2:
        return s[1:-1]
    return None


def _split_top_level(s, sep=","):
    """Split s on sep, respecting quotes and brackets."""
    parts = []
    depth = 0
    cur = []
    in_str = False
    q = None
    for ch in s:
        if in_str:
            cur.append(ch)
            if ch == q:
                in_str = False
            continue
        if ch in ('"', "'"):
            in_str = True
            q = ch
            cur.append(ch)
        elif ch in "[{":
            depth += 1
            cur.append(ch)
        elif ch in "]}":
            depth -= 1
            cur.append(ch)
        elif ch == sep and depth == 0:
            parts.append("".join(cur).strip())
            cur = []
        else:
            cur.append(ch)
    if cur:
        parts.append("".join(cur).strip())
    return [p for p in parts if p]


def _strip_toml_comment(s):
    """Strip a trailing inline TOML comment (# ...) that sits outside strings/brackets."""
    depth = 0
    in_str = False
    q = None
    i = 0
    while i < len(s) - 1:
        ch = s[i]
        if in_str:
            if ch == q:
                in_str = False
            i += 1
            continue
        if ch in ('"', "'"):
            in_str = True
            q = ch
        elif ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
        elif ch == "#" and depth == 0 and (i == 0 or s[i - 1] in " \t"):
            return s[:i].rstrip()
        i += 1
    return s


def _toml_value(s):
    s = _strip_toml_comment(s).strip()
    if not s:
        return None
    if s == "true":
        return True
    if s == "false":
        return False
    if s.startswith("["):
        return [_toml_value(x) for x in _split_top_level(s[1:-1].strip())]
    if s.startswith("{"):
        d = {}
        for pair in _split_top_level(s[1:-1].strip()):
            eq = _find_eq_outside_string(pair)
            if eq is None:
                continue
            k = _toml_key(pair[:eq].strip())
            d[".".join(k)] = _toml_value(pair[eq + 1:])
        return d
    st = _toml_string(s)
    if st is not None:
        return st
    if re.fullmatch(r"[+-]?\d+(_\d+)*", s):
        return int(s.replace("_", ""))
    if re.fullmatch(r"[+-]?(\d+_)*\d+\.\d+", s):
        return float(s.replace("_", ""))
    return s



def _toml_key(s):
    parts = []
    for p in _split_top_level(s, "."):
        st = _toml_string(p)
        parts.append(st if st is not None else p.strip())
    return parts


def _toml_nav(root, parts):
    """Navigate to the dict for a path, descending through array-of-tables lists."""
    cur = root
    for p in parts:
        nxt = cur.get(p)
        if isinstance(nxt, list):
            if not nxt:
                return None
            cur = nxt[-1]
            continue
        if not isinstance(nxt, dict):
            nxt = {}
            cur[p] = nxt
        cur = nxt
    return cur


def _toml_table(root, parts):
    return _toml_nav(root, parts)


def _toml_set(root, parts, value):
    cur = _toml_nav(root, parts[:-1])
    if cur is not None:
        cur[parts[-1]] = value



def _toml_aot(root, parts):
    """Return the next dict for an array-of-tables header, appending when needed."""
    cur = root
    for p in parts[:-1]:
        nxt = cur.get(p)
        if not isinstance(nxt, dict):
            nxt = {}
            cur[p] = nxt
        cur = nxt
    arr = cur.get(parts[-1])
    if not isinstance(arr, list):
        arr = []
        cur[parts[-1]] = arr
    d = {}
    arr.append(d)
    return d


def _bracket_depth(s):
    depth = 0
    in_str = False
    q = None
    for ch in s:
        if in_str:
            if ch == q:
                in_str = False
            continue
        if ch in ('"', "'"):
            in_str = True
            q = ch
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
    return depth


def _toml_needs_more(text, lines, i, n):
    """Whether a value continues on the following lines."""
    for q in ('"""', "'''"):
        if text.startswith(q):
            return q not in text[3:]
    if text.startswith("["):
        return _bracket_depth(text) > 0
    if text.startswith("{"):
        return _bracket_depth(text) > 0
    return False


def parse_toml(text):
    """Parse a TOML document (subset) into nested dict/list structures.

    Supports tables, arrays of tables, dotted keys, basic/literal/triple-quoted
    strings, arrays (multi-line), inline tables and inline comments - the
    subset used by pyproject.toml / Pipfile / poetry.lock.
    """
    root = {}
    cur = root
    lines = (text or "").lstrip("\ufeff").splitlines()
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        s = line.strip()
        if not s or s.startswith("#"):
            i += 1
            continue
        if s.startswith("[[") and s.endswith("]]"):
            cur = _toml_aot(root, _toml_key(s[2:-2].strip()))
            i += 1
            continue
        if s.startswith("[") and s.endswith("]"):
            cur = _toml_table(root, _toml_key(s[1:-1].strip()))
            i += 1
            continue
        eq = _find_eq_outside_string(line)
        if eq is None:
            i += 1
            continue
        key = _toml_key(line[:eq].strip())
        val_text = line[eq + 1:].strip()
        while _toml_needs_more(val_text, lines, i, n):
            i += 1
            if i >= n:
                break
            val_text += "\n" + lines[i]
        val = _toml_value(val_text.strip())
        _toml_set(cur, key, val)
        i += 1
    return root


# --------------------------------------------------------------------------
# npm ecosystem
# --------------------------------------------------------------------------

PUBLIC_NPM_HOSTS = ("registry.npmjs.org", "registry.yarnpkg.com")


def _scope_of(name):
    if name.startswith("@"):
        return name.split("/")[0].lstrip("@")
    return None


def parse_npmrc(text):
    """Parse .npmrc into {"registry": url|None, "scopes": {scope: url}}."""
    cfg = {"registry": None, "scopes": {}}
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line or line.startswith(("#", ";")):
            continue
        if "=" not in line:
            continue
        k, _, v = line.partition("=")
        k = k.strip()
        v = re.sub(r"\s+[#;].*$", "", v).strip()
        if k == "registry":
            cfg["registry"] = v or None
        elif k.startswith("@") and k.endswith(":registry"):
            cfg["scopes"][k[1:-9]] = v or None
    return cfg


def parse_package_json(text):
    try:
        d = json.loads(text or "{}")
        return d if isinstance(d, dict) else {}
    except Exception:
        return {}


def _lock_pkg_name(key):
    if not key:
        return ""
    idx = key.rfind("node_modules/")
    if idx >= 0:
        return key[idx + len("node_modules/"):]
    return key


def _v1_name(key):
    if key.startswith("@"):
        slash = key.find("/")
        at = key.find("@", slash)
        return key if at == -1 else key[:at]
    return key.split("@")[0]


def _descriptor_name_version(descriptor):
    """Split an npm descriptor such as @scope/pkg@1.2.3 or lodash@^4."""
    s = str(descriptor or "").strip().strip("\"'")
    if not s:
        return None, None
    if s.startswith("@"):
        slash = s.find("/")
        at = s.find("@", slash + 1) if slash >= 0 else -1
        if at > slash:
            return s[:at], s[at + 1:].split("(", 1)[0]
    at = s.rfind("@")
    if at > 0:
        return s[:at], s[at + 1:].split("(", 1)[0]
    return s, None


def _jsonc_load(text):
    """Parse the JSONC-like bun text lockfile without third-party modules."""
    cleaned = re.sub(r"(?m)^\s*//.*$", "", text or "")
    cleaned = re.sub(r",(\s*[}\]])", r"\1", cleaned)
    return json.loads(cleaned)


def parse_yarn_lock(text):
    """Parse the name/version/resolved/integrity subset of yarn.lock."""
    packages = {}
    current = None
    for raw in (text or "").splitlines():
        if raw and not raw.startswith((" ", "\t", "#")) and raw.rstrip().endswith(":"):
            descriptor_text = raw.rstrip()[:-1]
            current = None
            for item in descriptor_text.split(","):
                name, _ = _descriptor_name_version(item)
                if not name:
                    continue
                current = name
                packages.setdefault(name, [])
                break
            continue
        if current is None:
            continue
        m = re.match(r"^\s+version\s+\"?([^\"\s]+)\"?\s*$", raw)
        if m:
            entry = {"version": m.group(1), "resolved": None, "integrity": None,
                     "dev": False, "optional": False, "deps": {}, "key": current}
            packages.setdefault(current, []).append(entry)
            continue
        if not packages.get(current):
            continue
        entry = packages[current][-1]
        m = re.match(r"^\s+resolved\s+\"?([^\"\s]+)\"?\s*$", raw)
        if m:
            entry["resolved"] = m.group(1)
            continue
        m = re.match(r"^\s+integrity\s+\"?([^\"\s]+)\"?\s*$", raw)
        if m:
            entry["integrity"] = m.group(1)
    return {"lockfileVersion": None, "root": {}, "packages": packages}


def _pnpm_key_name_version(key):
    s = str(key or "").strip().strip("\"'").split("(", 1)[0]
    if not s:
        return None, None
    if s.startswith("/"):
        s = s[1:]
    if s.startswith("@"):
        slash = s.find("/")
        at = s.rfind("@")
        if slash >= 0 and at > slash:
            return s[:at], s[at + 1:]
        if slash >= 0:
            name, _, version = s.rpartition("/")
            return (name, version) if version else (None, None)
        return None, None
    if "@" in s:
        name, _, version = s.rpartition("@")
        return (name, version) if name and version else (None, None)
    if "/" in s:
        name, _, version = s.rpartition("/")
        return (name, version) if name and version else (None, None)
    return None, None


def parse_pnpm_lock(text):
    """Parse common pnpm-lock.yaml package keys without a YAML dependency."""
    packages = {}
    current = None
    in_packages = False
    lock_version = None
    for raw in (text or "").splitlines():
        m = re.match(r"^lockfileVersion:\s*['\"]?([^'\"\s]+)", raw)
        if m:
            try:
                lock_version = int(float(m.group(1)))
            except ValueError:
                lock_version = m.group(1)
            continue
        if re.match(r"^packages:\s*$", raw):
            in_packages = True
            continue
        if in_packages and raw and not raw.startswith((" ", "\t")):
            in_packages = False
            current = None
            continue
        if not in_packages:
            continue
        m = re.match(r"^\s{2}(['\"]?)(.+?)\1:\s*$", raw)
        if m:
            name, version = _pnpm_key_name_version(m.group(2))
            if name and version and version[:1].isdigit():
                current = name
                packages.setdefault(name, []).append({
                    "version": version, "resolved": None, "integrity": None,
                    "dev": False, "optional": False, "deps": {}, "key": m.group(2),
                })
            else:
                current = None
            continue
        if current and packages.get(current):
            m = re.search(r"integrity:\s*([^,}\s]+)", raw)
            if m:
                packages[current][-1]["integrity"] = m.group(1).strip("\"'")
    return {"lockfileVersion": lock_version, "root": {}, "packages": packages}


def parse_bun_lock(text):
    """Parse bun.lock (JSONC-like text). bun.lockb is intentionally unsupported."""
    try:
        data = _jsonc_load(text)
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    packages = {}
    for key, ent in (data.get("packages") or {}).items():
        name = None
        version = None
        integrity = None
        if isinstance(ent, list) and ent:
            name, version = _descriptor_name_version(ent[0])
            integrity = ent[3] if len(ent) > 3 else None
        elif isinstance(ent, dict):
            name = ent.get("name") or key
            version = ent.get("version")
            integrity = ent.get("integrity")
        if not name:
            name = key
        packages.setdefault(name, []).append({
            "version": str(version) if version else None,
            "resolved": None, "integrity": integrity,
            "dev": False, "optional": False, "deps": {}, "key": key,
        })
    workspace = (data.get("workspaces") or {}).get("") or {}
    root = {
        "name": workspace.get("name") or data.get("name"),
        "version": workspace.get("version") or data.get("version"),
    }
    return {"lockfileVersion": data.get("lockfileVersion"), "root": root, "packages": packages}


def _select_npm_lockfile(base, pj):
    manager = str(pj.get("packageManager") or "").split("@", 1)[0].lower()
    by_manager = {
        "npm": ("package-lock.json", "npm-shrinkwrap.json"),
        "yarn": ("yarn.lock",),
        "pnpm": ("pnpm-lock.yaml",),
        "bun": ("bun.lock", "bun.lockb"),
    }
    candidates = list(by_manager.get(manager, ()))
    for name in ("package-lock.json", "npm-shrinkwrap.json", "yarn.lock",
                 "pnpm-lock.yaml", "bun.lock", "bun.lockb"):
        if name not in candidates:
            candidates.append(name)
    for name in candidates:
        path = base / name
        if path.is_file():
            return path
    return None


def parse_package_lock(text):
    """Parse package-lock.json / npm-shrinkwrap.json.

    Returns {"lockfileVersion", "root", "packages": {name: [entry,...]}} or None.
    """
    try:
        data = json.loads(text or "{}")
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    lv = data.get("lockfileVersion")
    root = {
        "name": data.get("name"),
        "version": data.get("version"),
        "deps": data.get("dependencies") or {},
    }
    packages = {}
    if isinstance(lv, int) and lv >= 2:
        for key, ent in (data.get("packages") or {}).items():
            if not isinstance(ent, dict):
                continue
            name = _lock_pkg_name(key)
            if not name:
                continue
            deps = {}
            for dk in ("dependencies", "optionalDependencies", "peerDependencies"):
                for dn, dv in (ent.get(dk) or {}).items():
                    deps.setdefault(dn, dv)
            packages.setdefault(name, []).append({
                "version": ent.get("version"),
                "resolved": ent.get("resolved"),
                "integrity": ent.get("integrity"),
                "dev": bool(ent.get("dev") or ent.get("devOptional")),
                "optional": bool(ent.get("optional")),
                "deps": deps,
                "key": key,
            })
    else:
        for key, ent in (data.get("dependencies") or {}).items():
            if not isinstance(ent, dict):
                continue
            name = _v1_name(key)
            packages.setdefault(name, []).append({
                "version": ent.get("version"),
                "resolved": ent.get("resolved"),
                "integrity": ent.get("integrity"),
                "dev": bool(ent.get("dev")),
                "optional": bool(ent.get("optional")),
                "deps": dict(ent.get("requires") or {}),
                "key": key,
            })
    return {"lockfileVersion": lv, "root": root, "packages": packages}


def check_npm(project_dir, findings, sbom_pkgs):
    """Check the npm ecosystem in project_dir. Returns True if npm detected."""
    base = Path(project_dir)
    pj_path = base / "package.json"
    if not pj_path.exists():
        return False
    pj = parse_package_json(_read_text(pj_path))
    if not pj:
        return False

    manifest_deps = {}
    for group in ("dependencies", "devDependencies", "optionalDependencies", "peerDependencies"):
        d = pj.get(group) or {}
        if isinstance(d, dict):
            for n, r in d.items():
                manifest_deps.setdefault(n, {"range": r, "group": group})

    npmrc = parse_npmrc(_read_text(base / ".npmrc"))
    pub_cfg = pj.get("publishConfig") or {}
    if isinstance(pub_cfg, dict) and pub_cfg.get("registry"):
        npmrc["registry"] = npmrc["registry"] or pub_cfg["registry"]

    lock_path = _select_npm_lockfile(base, pj)
    if lock_path is None:
        if manifest_deps:
            findings.append(Finding(
                "missing_lockfile", "medium", "package.json", None,
                "缺少锁文件（支持 package-lock.json / npm-shrinkwrap.json / yarn.lock / pnpm-lock.yaml / bun.lock）",
                "依赖版本未锁定，安装结果不可复现；建议按项目包管理器提交对应锁文件", ecosystem="npm"))
    else:
        lock = None
        if lock_path.name == "bun.lockb":
            findings.append(Finding(
                "lockfile_parse_unsupported", "info", lock_path.name, None,
                "检测到 bun.lockb，但二进制锁文件本版本不做深度解析",
                "已按锁文件存在处理，不误报 missing_lockfile；需要深度一致性校验时请改用 bun.lock 文本锁文件", ecosystem="npm"))
        elif lock_path.name in ("package-lock.json", "npm-shrinkwrap.json"):
            lock = parse_package_lock(_read_text(lock_path))
        elif lock_path.name == "yarn.lock":
            lock = parse_yarn_lock(_read_text(lock_path))
        elif lock_path.name == "pnpm-lock.yaml":
            lock = parse_pnpm_lock(_read_text(lock_path))
        elif lock_path.name == "bun.lock":
            lock = parse_bun_lock(_read_text(lock_path))
        if lock is None and lock_path.name != "bun.lockb":
            findings.append(Finding(
                "lockfile_parse_error", "medium", lock_path.name, None,
                "锁文件解析失败（结构异常或格式不受支持）",
                "请用对应包管理器重新生成锁文件", ecosystem="npm"))
        else:
            if lock is not None:
                _check_npm_lock(base, lock_path, lock, pj, manifest_deps, npmrc, findings, sbom_pkgs)

    for name, info in manifest_deps.items():
        rng = (info["range"] or "").strip()
        if rng in ("", "*", "latest", "x"):
            findings.append(Finding(
                "unpinned", "low", "package.json", name,
                "依赖 %s 未固定版本（%s），每次安装可能拉到不同版本" % (name, rng or "未指定"),
                "建议给出 ^/~/精确版本并提交锁文件", ecosystem="npm"))
        if "/" not in name:
            ts = find_typosquat(name, POPULAR_NPM)
            if ts:
                findings.append(Finding(
                    "typosquat", "low", "package.json", name,
                    "依赖名 %s 与知名包 %s 高度相似（编辑距离 %d），请核对是否为拼写仿冒" % (name, ts[0], ts[1]),
                    "typosquat 是供应链投毒常见手法，发布前请人工确认包名与来源", ecosystem="npm"))
    return True


def _check_npm_lock(base, lock_path, lock, pj, manifest_deps, npmrc, findings, sbom_pkgs):
    lv = lock["lockfileVersion"]
    lock_name = lock["root"].get("name")
    lock_version = lock["root"].get("version")
    pj_name = pj.get("name")
    if pj_name and lock_name and lock_name != pj_name:
        findings.append(Finding(
            "lockfile_root_mismatch", "medium", lock_path.name, lock_name,
            "锁文件根包名 %s 与 package.json name %s 不一致" % (lock_name, pj_name),
            "锁文件与清单不对应，可能是复制或生成错误", ecosystem="npm"))
    if pj.get("version") and lock_version and str(lock_version) != str(pj.get("version")):
        findings.append(Finding(
            "lockfile_root_mismatch", "medium", lock_path.name, lock_name or "",
            "锁文件根版本 %s 与 package.json version %s 不一致" % (lock_version, pj.get("version")),
            "锁文件与清单不对应，请重新生成", ecosystem="npm"))

    packages = lock["packages"]

    for name, info in manifest_deps.items():
        entries = packages.get(name)
        if not entries:
            findings.append(Finding(
                "lockfile_missing_entry", "high", lock_path.name, name,
                "package.json 声明了 %s@%s，但锁文件中没有该包" % (name, info["range"]),
                "锁文件过期或手工改动，运行 npm install 重新生成", ecosystem="npm"))
            continue
        matched = any(e.get("version") and semver_satisfies(e["version"], info["range"])
                      for e in entries)
        if not matched:
            versions = ", ".join(sorted({str(e.get("version")) for e in entries if e.get("version")}))
            findings.append(Finding(
                "lockfile_range_unsatisfied", "high", lock_path.name, name,
                "锁文件中 %s 的版本（%s）不满足 package.json 声明范围 %s" % (name, versions or "无版本", info["range"]),
                "声明与锁定不一致，安装可能拉取意外版本", ecosystem="npm"))

    all_names = set(packages.keys())
    for name, entries in packages.items():
        for e in entries:
            for dn in e["deps"]:
                if dn not in all_names:
                    findings.append(Finding(
                        "lockfile_dangling_ref", "high", lock_path.name, name,
                        "锁文件里 %s 依赖的 %s 不存在于锁文件包列表" % (name, dn),
                        "依赖图断裂，安装可能失败或行为异常", ecosystem="npm"))

    if lv is not None and lv >= 2:
        for name, entries in packages.items():
            for e in entries:
                if e.get("version") and not e.get("integrity"):
                    res = e.get("resolved") or ""
                    if "github.com" in res or res.startswith("file:") or "git+" in res:
                        continue
                    findings.append(Finding(
                        "lockfile_integrity_missing", "medium", lock_path.name, name,
                        "锁文件中 %s@%s 缺少 integrity 校验值" % (name, e.get("version")),
                        "缺少完整性校验，安装无法防篡改", ecosystem="npm"))

    for name, entries in packages.items():
        sig = {}
        for e in entries:
            if not e.get("version"):
                continue
            key = (name, e["version"])
            s = (e.get("resolved"), e.get("integrity"))
            if key in sig and sig[key] != s:
                findings.append(Finding(
                    "lockfile_duplicate_conflict", "high", lock_path.name, name,
                    "锁文件中 %s@%s 存在多个不同来源（resolved/integrity 不一致）" % (name, e["version"]),
                    "同一版本解析到不同 tarball，存在被替换风险", ecosystem="npm"))
                break
            sig[key] = s

    # registry / dependency-confusion signals
    cfg_default_host = None
    if npmrc.get("registry"):
        cfg_default_host = _url_host(npmrc["registry"])
    host_by_name = {}
    for name, entries in packages.items():
        for e in entries:
            h = _url_host(e.get("resolved"))
            if h:
                host_by_name.setdefault(name, set()).add(h[1])

    for name, hosts in host_by_name.items():
        if len(hosts) > 1:
            findings.append(Finding(
                "confusion_mixed_registry", "high", lock_path.name, name,
                "包 %s 被解析自多个不同仓库主机：%s" % (name, ", ".join(sorted(hosts))),
                "同一依赖来源不一致，可能是依赖混淆或镜像污染", ecosystem="npm"))
        scope = _scope_of(name)
        scope_cfg = npmrc["scopes"].get(scope) if scope else None
        for h in sorted(hosts):
            if scope_cfg:
                sc_host = _url_host(scope_cfg)
                if sc_host and h != sc_host[1]:
                    findings.append(Finding(
                        "confusion_scope_registry", "high", lock_path.name, name,
                        "作用域 %s 在 .npmrc 配置了私有仓库 %s，但 %s 实际解析自公共仓库 %s" % (scope, scope_cfg, name, h),
                        "私有包名可能被公共仓库同名抢占（依赖混淆）", ecosystem="npm"))
            if cfg_default_host and cfg_default_host[1] != h and h in PUBLIC_NPM_HOSTS and not scope_cfg:
                findings.append(Finding(
                    "confusion_registry_mismatch", "medium", lock_path.name, name,
                    "项目配置了默认仓库 %s，但 %s 实际解析自公共仓库 %s" % (npmrc["registry"], name, h),
                    "配置与锁定来源不一致，私有包名可能被公共仓库抢占（依赖混淆）", ecosystem="npm"))

    for name, entries in packages.items():
        seen = set()
        for e in entries:
            res = e.get("resolved")
            if not res or res in seen:
                continue
            seen.add(res)
            suspicious, reason = _is_suspicious_url(res)
            if suspicious:
                findings.append(Finding(
                    "confusion_suspicious_registry", "medium", lock_path.name, name,
                    "包 %s 的解析地址可疑：%s（%s）" % (name, res, reason),
                    "请核对仓库地址来源", ecosystem="npm"))

    # collect SBOM packages
    for name, entries in packages.items():
        for e in entries:
            scope = "optional" if (e.get("dev") or e.get("optional")) else "required"
            sbom_pkgs.append({
                "ecosystem": "npm",
                "name": name,
                "version": e.get("version") or "",
                "resolved": e.get("resolved") or "",
                "integrity": e.get("integrity") or "",
                "scope": scope,
                "direct": name in manifest_deps,
                "deps": sorted(e["deps"].keys()),
            })
    return True


# --------------------------------------------------------------------------
# python ecosystem
# --------------------------------------------------------------------------

_RE_PEP508 = re.compile(r"^([A-Za-z0-9][A-Za-z0-9._-]*)(?:\[[^]]*\])?\s*([^;]*)$")


def _pep508_split(d):
    if not isinstance(d, str):
        return (str(d), "")
    m = _RE_PEP508.match(d.strip())
    if not m:
        return (d.strip(), "")
    return (m.group(1), m.group(2).strip())


def parse_requirements(text, base_dir=None, depth=0, out=None):
    """Parse requirements.txt content.

    Returns {"packages": {name: {"spec", "has_hash"}}, "index": url|None,
    "extra": [url,...]}. Follows -r includes (bounded depth).
    """
    out = out if out is not None else {"packages": {}, "index": None, "extra": []}
    if depth > 5:
        return out
    for raw in (text or "").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        low = line.lower()
        if low.startswith("--index-url") or low.startswith("-i "):
            parts = line.split(None, 1)
            if len(parts) > 1:
                out["index"] = parts[1].strip().split()[0]
            continue
        if low.startswith("--extra-index-url"):
            parts = line.split(None, 1)
            if len(parts) > 1:
                out["extra"].append(parts[1].strip().split()[0])
            continue
        if low.startswith("-r ") or low.startswith("--requirement "):
            parts = line.split(None, 1)
            if len(parts) > 1 and base_dir:
                sub = parts[1].strip().split()[0]
                parse_requirements(_read_text(Path(base_dir) / sub), Path(base_dir), depth + 1, out)
            continue
        if (low.startswith("-e ") or line.startswith("git+") or line.startswith("hg+")
                or line.startswith("svn+") or line.startswith("http://") or line.startswith("https://")):
            continue
        name_spec = line.partition(";")[0].strip()
        if not name_spec:
            continue
        m = _RE_PEP508.match(name_spec)
        if not m:
            continue
        name = m.group(1)
        spec = m.group(2).strip()
        has_hash = "--hash" in line
        spec = re.sub(r"\s+--hash=[^\s]+", "", spec).strip()
        out["packages"].setdefault(name, {"spec": spec, "has_hash": has_hash})
    return out


def pyproject_deps(py):
    """Return (project_deps, poetry_deps) lists of (name, spec)."""
    proj_deps = []
    poetry_deps = []
    proj = py.get("project") or {}
    for d in (proj.get("dependencies") or []):
        proj_deps.append(_pep508_split(d))
    opt = proj.get("optional-dependencies") or {}
    if isinstance(opt, dict):
        for lst in opt.values():
            if isinstance(lst, list):
                for d in lst:
                    proj_deps.append(_pep508_split(d))
    tool = py.get("tool") or {}
    poetry = tool.get("poetry") or {}
    pdep = poetry.get("dependencies") or {}
    if isinstance(pdep, dict):
        for name, spec in pdep.items():
            if name == "python":
                continue
            if isinstance(spec, dict):
                spec = spec.get("version", "*")
            poetry_deps.append((name, str(spec or "*")))
    g = poetry.get("dev-dependencies") or {}
    if isinstance(g, dict):
        for name, spec in g.items():
            poetry_deps.append((name, str(spec) if not isinstance(spec, dict) else "*"))
    for gname, gdata in (poetry.get("group") or {}).items():
        if isinstance(gdata, dict):
            for name, spec in (gdata.get("dependencies") or {}).items():
                poetry_deps.append((name, str(spec) if not isinstance(spec, dict) else "*"))
    return proj_deps, poetry_deps


def poetry_sources(py):
    out = []
    tool = py.get("tool") or {}
    poetry = tool.get("poetry") or {}
    srcs = poetry.get("source") or []
    if isinstance(srcs, dict):
        srcs = [srcs]
    for s in srcs:
        if isinstance(s, dict):
            out.append({
                "name": s.get("name"),
                "url": s.get("url"),
                "default": bool(s.get("default")),
                "secondary": bool(s.get("secondary")),
            })
    return out


def _pip_index_urls(py):
    """Collect index URLs from [tool.pip.index] / [[tool.pip.index]] / [tool.uv]."""
    urls = []
    tool = py.get("tool") or {}
    for tname in ("pip", "uv"):
        sec = tool.get(tname) or {}
        idx = sec.get("index")
        items = idx if isinstance(idx, list) else ([idx] if idx else [])
        for it in items:
            if isinstance(it, dict) and it.get("url"):
                urls.append(it["url"])
        if isinstance(sec, dict) and sec.get("index-url"):
            urls.append(sec["index-url"])
    return urls


def check_python(project_dir, findings, sbom_pkgs):
    """Check the python ecosystem. Returns True if python detected."""
    base = Path(project_dir)
    touched = False

    for rf in sorted(base.glob("requirements*.txt")):
        touched = True
        parsed = parse_requirements(_read_text(rf), base_dir=rf.parent)
        for name, info in parsed["packages"].items():
            spec = info["spec"]
            if not spec or spec in ("*", ""):
                findings.append(Finding(
                    "unpinned", "low", rf.name, name,
                    "依赖 %s 未固定版本（%s），每次安装可能拉到不同版本" % (name, spec or "未指定"),
                    "建议给出 ==/>= 等约束并配合锁文件（pip-tools / poetry / pipenv）", ecosystem="python"))
            ts = find_typosquat(name, POPULAR_PYPI)
            if ts:
                findings.append(Finding(
                    "typosquat", "low", rf.name, name,
                    "依赖名 %s 与知名包 %s 高度相似（编辑距离 %d），请核对是否为拼写仿冒" % (name, ts[0], ts[1]),
                    "typosquat 是供应链投毒常见手法，发布前请人工确认包名与来源", ecosystem="python"))
        idx = parsed["index"]
        extras = parsed["extra"]
        if idx and extras:
            findings.append(Finding(
                "confusion_extra_index", "medium", rf.name, None,
                "同时配置了主仓库 %s 与 extra-index %s，公共仓库成为回退源，私有包名可能被公共仓库同名抢占（依赖混淆）" % (idx, ", ".join(extras)),
                "依赖混淆高危配置：建议仅使用单一可信仓库并锁定私有包名", ecosystem="python"))
        for url in ([idx] if idx else []) + extras:
            suspicious, reason = _is_suspicious_url(url)
            if suspicious:
                findings.append(Finding(
                    "confusion_suspicious_registry", "medium", rf.name, None,
                    "索引地址可疑：%s（%s）" % (url, reason),
                    "请核对仓库地址来源", ecosystem="python"))

    pp_path = base / "pyproject.toml"
    if pp_path.exists():
        touched = True
        py = parse_toml(_read_text(pp_path))
        proj_deps, poetry_deps = pyproject_deps(py)
        declared = proj_deps + poetry_deps
        poetry_lock_path = base / "poetry.lock"
        uv_lock_path = base / "uv.lock"
        lock_path = None
        lock_kind = None
        if poetry_deps and poetry_lock_path.exists():
            lock_path, lock_kind = poetry_lock_path, "poetry"
        elif uv_lock_path.exists():
            lock_path, lock_kind = uv_lock_path, "uv"
        elif poetry_lock_path.exists():
            lock_path, lock_kind = poetry_lock_path, "poetry"
        lock = parse_toml(_read_text(lock_path)) if lock_path is not None else None
        if declared and lock_path is None:
            findings.append(Finding(
                "missing_lockfile", "medium", "pyproject.toml", None,
                "pyproject.toml 声明了 %d 个依赖但没有 poetry.lock / uv.lock" % len(declared),
                "依赖版本未锁定，安装结果不可复现；请按所用工具提交 poetry.lock 或 uv.lock", ecosystem="python"))
        elif lock is not None:
            if lock_kind == "poetry":
                _check_poetry_lock(lock, declared, findings, sbom_pkgs)
            else:
                _check_uv_lock(lock, declared, findings, sbom_pkgs)
        for src in poetry_sources(py):
            url = src.get("url")
            if not url:
                continue
            suspicious, reason = _is_suspicious_url(url)
            if suspicious:
                findings.append(Finding(
                    "confusion_suspicious_registry", "medium", "pyproject.toml", None,
                    "poetry 源 %s 地址可疑：%s（%s）" % (src.get("name") or "?", url, reason),
                    "请核对仓库地址来源", ecosystem="python"))
            if src.get("secondary") and "pypi.org" not in url:
                findings.append(Finding(
                    "confusion_extra_index", "medium", "pyproject.toml", None,
                    "poetry 源 %s（%s）标记为 secondary，公共 PyPI 仍是回退源，私有包名存在依赖混淆风险" % (src.get("name") or "?", url),
                    "依赖混淆高危配置：建议把私有源设为 default 并禁用公共回退", ecosystem="python"))
        for url in _pip_index_urls(py):
            suspicious, reason = _is_suspicious_url(url)
            if suspicious:
                findings.append(Finding(
                    "confusion_suspicious_registry", "medium", "pyproject.toml", None,
                    "索引地址可疑：%s（%s）" % (url, reason),
                    "请核对仓库地址来源", ecosystem="python"))

    if check_pipfile(project_dir, findings, sbom_pkgs):
        touched = True
    return touched


def _check_poetry_lock(lock, declared, findings, sbom_pkgs):
    pkgs = {}
    for p in (lock.get("package") or []):
        if isinstance(p, dict) and p.get("name"):
            pkgs[p["name"]] = p
    for name, spec in declared:
        p = pkgs.get(name)
        if p is None:
            findings.append(Finding(
                "lockfile_missing_entry", "high", "poetry.lock", name,
                "pyproject.toml 声明了 %s（%s），但 poetry.lock 中没有该包" % (name, spec),
                "锁文件过期或手工改动，运行 poetry lock 重新生成", ecosystem="python"))
            continue
        ver = p.get("version")
        if ver and not pep440_satisfies(ver, spec):
            findings.append(Finding(
                "lockfile_range_unsatisfied", "high", "poetry.lock", name,
                "poetry.lock 中 %s=%s 不满足 pyproject.toml 声明 %s" % (name, ver, spec),
                "声明与锁定不一致，安装可能拉取意外版本", ecosystem="python"))
    for name, p in pkgs.items():
        for dn in (p.get("dependencies") or {}):
            if dn not in pkgs:
                findings.append(Finding(
                    "lockfile_dangling_ref", "high", "poetry.lock", name,
                    "poetry.lock 里 %s 依赖的 %s 不存在于锁文件包列表" % (name, dn),
                    "依赖图断裂，安装可能失败或行为异常", ecosystem="python"))
        files = p.get("files") or []
        if not files:
            findings.append(Finding(
                "lockfile_integrity_missing", "medium", "poetry.lock", name,
                "poetry.lock 中 %s 缺少文件哈希（files 为空）" % name,
                "缺少完整性校验，安装无法防篡改", ecosystem="python"))
        sbom_pkgs.append({
            "ecosystem": "python",
            "name": name,
            "version": str(p.get("version") or ""),
            "resolved": "",
            "integrity": (files[0].get("hash") if files and isinstance(files[0], dict) else "") or "",
            "scope": "optional" if p.get("optional") else "required",
            "direct": name in dict(declared),
            "deps": sorted((p.get("dependencies") or {}).keys()),
        })


def _python_dep_name(spec):
    s = str(spec or "").strip().strip("\"'")
    if " @ " in s:
        return s.split(" @ ", 1)[0].strip()
    if ";" in s:
        s = s.split(";", 1)[0].strip()
    return re.split(r"[<>=!~\[\s]", s, 1)[0].strip()


def _check_uv_lock(lock, declared, findings, sbom_pkgs):
    pkgs = {}
    for p in (lock.get("package") or []):
        if isinstance(p, dict) and p.get("name"):
            pkgs[p["name"]] = p
    for name, spec in declared:
        p = pkgs.get(name)
        if p is None:
            findings.append(Finding(
                "lockfile_missing_entry", "high", "uv.lock", name,
                "pyproject.toml 声明了 %s（%s），但 uv.lock 中没有该包" % (name, spec),
                "锁文件过期或手工改动，运行 uv lock 重新生成", ecosystem="python"))
            continue
        ver = str(p.get("version") or "")
        if ver and spec not in ("", "*") and not pep440_satisfies(ver, spec):
            findings.append(Finding(
                "lockfile_range_unsatisfied", "high", "uv.lock", name,
                "uv.lock 中 %s=%s 不满足 pyproject.toml 声明 %s" % (name, ver, spec),
                "声明与锁定不一致，安装可能拉取意外版本", ecosystem="python"))
    for name, p in pkgs.items():
        deps = p.get("dependencies") or []
        dep_names = []
        if isinstance(deps, dict):
            dep_names = list(deps.keys())
        elif isinstance(deps, list):
            dep_names = [_python_dep_name(x) for x in deps if _python_dep_name(x)]
        for dn in dep_names:
            if dn not in pkgs:
                findings.append(Finding(
                    "lockfile_dangling_ref", "high", "uv.lock", name,
                    "uv.lock 里 %s 依赖的 %s 不存在于锁文件包列表" % (name, dn),
                    "依赖图断裂，安装可能失败或行为异常", ecosystem="python"))
        sbom_pkgs.append({
            "ecosystem": "python",
            "name": name,
            "version": str(p.get("version") or ""),
            "resolved": "",
            "integrity": "",
            "scope": "optional" if p.get("optional") else "required",
            "direct": name in dict(declared),
            "deps": dep_names,
        })


def check_pipfile(project_dir, findings, sbom_pkgs):
    base = Path(project_dir)
    pf = base / "Pipfile"
    if not pf.exists():
        return False
    doc = parse_toml(_read_text(pf))
    packages = {}
    for grp in ("packages", "dev-packages"):
        d = doc.get(grp) or {}
        if isinstance(d, dict):
            for name, spec in d.items():
                if isinstance(spec, dict):
                    spec = spec.get("version", "*")
                packages.setdefault(name, {"spec": str(spec or "*"), "group": grp})
    sources = doc.get("source") or []
    if isinstance(sources, dict):
        sources = [sources]
    lock_path = base / "Pipfile.lock"
    lock = None
    if lock_path.exists():
        try:
            lock = json.loads(_read_text(lock_path))
        except Exception:
            lock = None
    if packages and lock is None:
        findings.append(Finding(
            "missing_lockfile", "medium", "Pipfile", None,
            "Pipfile 声明了 %d 个依赖但没有 Pipfile.lock" % len(packages),
            "依赖版本未锁定，安装结果不可复现；建议 pipenv lock 并提交 Pipfile.lock", ecosystem="python"))
    elif lock is not None:
        entries = {}
        for grp in ("default", "develop"):
            d = lock.get(grp) or {}
            if isinstance(d, dict):
                for name, ent in d.items():
                    if isinstance(ent, dict):
                        entries.setdefault(name, ent)
        for name, info in packages.items():
            ent = entries.get(name)
            if ent is None:
                findings.append(Finding(
                    "lockfile_missing_entry", "high", "Pipfile.lock", name,
                    "Pipfile 声明了 %s（%s），但 Pipfile.lock 中没有该包" % (name, info["spec"]),
                    "锁文件过期或手工改动，运行 pipenv lock 重新生成", ecosystem="python"))
                continue
            ver = str(ent.get("version") or "").lstrip("==")
            if ver and info["spec"] not in ("*", "") and not pep440_satisfies(ver, info["spec"]):
                findings.append(Finding(
                    "lockfile_range_unsatisfied", "high", "Pipfile.lock", name,
                    "Pipfile.lock 中 %s=%s 不满足 Pipfile 声明 %s" % (name, ver, info["spec"]),
                    "声明与锁定不一致，安装可能拉取意外版本", ecosystem="python"))
            hashes = ent.get("hashes") or []
            if not hashes:
                findings.append(Finding(
                    "lockfile_integrity_missing", "medium", "Pipfile.lock", name,
                    "Pipfile.lock 中 %s 缺少 hashes 校验" % name,
                    "缺少完整性校验，安装无法防篡改", ecosystem="python"))
            sbom_pkgs.append({
                "ecosystem": "python",
                "name": name,
                "version": ver,
                "resolved": "",
                "integrity": (hashes[0] if hashes else ""),
                "scope": "optional" if info["group"] == "dev-packages" else "required",
                "direct": True,
                "deps": [],
            })
    pypi_urls = [str(s.get("url")) for s in sources if s.get("url") and "pypi.org" in str(s.get("url"))]
    private_urls = [str(s.get("url")) for s in sources if s.get("url") and "pypi.org" not in str(s.get("url"))]
    if pypi_urls and private_urls:
        findings.append(Finding(
            "confusion_extra_index", "medium", "Pipfile", None,
            "Pipfile 同时配置了公共 PyPI 与私有源（%s），私有包名存在依赖混淆风险" % ", ".join(private_urls),
            "依赖混淆高危配置：建议仅使用单一可信源并锁定私有包名", ecosystem="python"))
    for src in sources:
        url = src.get("url")
        if not url:
            continue
        suspicious, reason = _is_suspicious_url(url)
        if suspicious:
            findings.append(Finding(
                "confusion_suspicious_registry", "medium", "Pipfile", None,
                "源地址可疑：%s（%s）" % (url, reason),
                "请核对仓库地址来源", ecosystem="python"))
    return True


# --------------------------------------------------------------------------
# maven ecosystem (basic)
# --------------------------------------------------------------------------

def check_maven(project_dir, findings, sbom_pkgs):
    base = Path(project_dir)
    pom = base / "pom.xml"
    if not pom.exists():
        return False
    import xml.etree.ElementTree as ET

    def local(tag):
        return tag.rsplit("}", 1)[-1]

    def child(el, name):
        for c in el:
            if local(c.tag) == name:
                return c
        return None

    def children(el, name):
        return [c for c in el if local(c.tag) == name]

    try:
        root = ET.fromstring(_read_text(pom))
    except Exception:
        findings.append(Finding(
            "lockfile_parse_error", "medium", "pom.xml", None,
            "pom.xml 解析失败（XML 不合法）",
            "请修复 pom.xml 格式", ecosystem="maven"))
        return True

    props = {}
    pe = child(root, "properties")
    if pe is not None:
        for c in pe:
            props[local(c.tag)] = (c.text or "").strip()

    managed = {}
    dm = child(root, "dependencyManagement")
    if dm is not None:
        dme = child(dm, "dependencies")
        if dme is not None:
            for d in children(dme, "dependency"):
                g = child(d, "groupId")
                a = child(d, "artifactId")
                v = child(d, "version")
                if g is not None and a is not None:
                    managed[(g.text or "").strip(), (a.text or "").strip()] = (v.text or "").strip() if v is not None else None

    deps = []
    deps_el = child(root, "dependencies")
    if deps_el is not None:
        for d in children(deps_el, "dependency"):
            g = child(d, "groupId")
            a = child(d, "artifactId")
            v = child(d, "version")
            sc = child(d, "scope")
            ga = ((g.text or "").strip(), (a.text or "").strip())
            ver = (v.text or "").strip() if v is not None else None
            if ver and ver.startswith("$" + "{"):
                ver = props.get(ver[2:-1])
            if not ver:
                ver = managed.get(ga)
            scope = (sc.text or "").strip() if sc is not None else "compile"
            deps.append({"group": ga[0], "artifact": ga[1], "version": ver, "scope": scope})

    for d in deps:
        key = "%s:%s" % (d["group"], d["artifact"])
        if not d["version"]:
            findings.append(Finding(
                "unpinned", "medium", "pom.xml", key,
                "依赖 %s 未固定版本（未声明 <version> 且不在 dependencyManagement）" % key,
                "版本浮动可能被替换为恶意版本，建议显式固定", ecosystem="maven"))
        elif d["version"].endswith("-SNAPSHOT"):
            findings.append(Finding(
                "snapshot", "low", "pom.xml", key,
                "依赖 %s 使用 SNAPSHOT 版本 %s" % (key, d["version"]),
                "SNAPSHOT 版本可变，发布物不应依赖", ecosystem="maven"))
        sbom_pkgs.append({
            "ecosystem": "maven",
            "name": key,
            "version": d["version"] or "",
            "resolved": "",
            "integrity": "",
            "scope": "optional" if d["scope"] not in ("compile", "runtime") else "required",
            "direct": True,
            "deps": [],
        })

    rep_el = child(root, "repositories")
    if rep_el is not None:
        for r in children(rep_el, "repository"):
            u = child(r, "url")
            if u is not None and (u.text or "").strip():
                url = u.text.strip()
                suspicious, reason = _is_suspicious_url(url)
                if suspicious:
                    findings.append(Finding(
                        "confusion_suspicious_registry", "medium", "pom.xml", None,
                        "仓库地址可疑：%s（%s）" % (url, reason),
                        "请核对仓库地址来源", ecosystem="maven"))
    return True


# --------------------------------------------------------------------------
# SBOM-lite (CycloneDX 1.5 subset)
# --------------------------------------------------------------------------

def _purl(ecosystem, name, version):
    if ecosystem == "npm":
        n = name
        if n.startswith("@"):
            n = "%40" + n[1:]
        return ("pkg:npm/%s@%s" % (n, version)) if version else ("pkg:npm/%s" % n)
    if ecosystem == "python":
        return ("pkg:pypi/%s@%s" % (name, version)) if version else ("pkg:pypi/%s" % name)
    if ecosystem == "maven" and ":" in name:
        g, a = name.split(":", 1)
        return ("pkg:maven/%s/%s@%s" % (g, a, version)) if version else ("pkg:maven/%s/%s" % (g, a))
    return ("pkg:generic/%s@%s" % (name, version)) if version else ("pkg:generic/%s" % name)


def build_sbom(sbom_pkgs, include_dev=True, root_component=None):
    """Build a CycloneDX 1.5 subset JSON from collected packages."""
    seen = set()
    uniq = []
    for p in sbom_pkgs:
        key = (p["ecosystem"], p["name"], p["version"], p.get("resolved", ""))
        if key in seen:
            continue
        seen.add(key)
        uniq.append(p)
    if not include_dev:
        uniq = [p for p in uniq if p.get("scope") != "optional"]

    name_purl = {}
    for p in uniq:
        npk = (p["ecosystem"], p["name"])
        if npk not in name_purl:
            name_purl[npk] = _purl(p["ecosystem"], p["name"], p["version"])

    components = []
    for p in sorted(uniq, key=lambda x: (x["ecosystem"], x["name"].lower(), x["version"])):
        props = []
        if p.get("resolved"):
            props.append({"name": "yotta-chain:resolved", "value": p["resolved"]})
        if p.get("integrity"):
            props.append({"name": "yotta-chain:integrity", "value": p["integrity"]})
        if p.get("direct"):
            props.append({"name": "yotta-chain:direct", "value": "true"})
        components.append({
            "type": "library",
            "name": p["name"],
            "version": p["version"],
            "scope": p.get("scope", "required"),
            "purl": _purl(p["ecosystem"], p["name"], p["version"]),
            "properties": props,
        })

    dependencies = []
    if root_component and root_component.get("name"):
        root_ref = _purl(root_component.get("ecosystem", "generic"), root_component["name"], root_component.get("version") or "")
        direct_refs = sorted({
            _purl(p["ecosystem"], p["name"], p["version"])
            for p in uniq if p.get("direct")
        })
        dependencies.append({"ref": root_ref, "dependsOn": direct_refs})
    for p in uniq:
        purl = _purl(p["ecosystem"], p["name"], p["version"])
        refs = []
        for dn in p.get("deps") or []:
            target = name_purl.get((p["ecosystem"], dn))
            if target and target != purl:
                refs.append(target)
        dependencies.append({"ref": purl, "dependsOn": sorted(set(refs))})

    bom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "version": 1,
        "serialNumber": "urn:uuid:" + _uuid(),
        "metadata": {
            "timestamp": _now_iso(),
            "tools": [{"vendor": "YottaMeta", "name": "yotta-chain", "version": VERSION}],
        },
        "components": components,
        "dependencies": dependencies,
    }
    if root_component and root_component.get("name"):
        bom["metadata"]["component"] = {
            "type": "application",
            "name": root_component["name"],
            "version": root_component.get("version") or "",
        }
    return bom


def _uuid():
    import uuid
    return str(uuid.uuid4())


def _now_iso():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def render_sbom_text(bom):
    lines = ["元链 yotta-chain — SBOM-lite（CycloneDX 1.5 子集）"]
    meta = bom.get("metadata", {})
    comp = meta.get("component") or {}
    if comp:
        lines.append("项目：%s %s" % (comp.get("name"), comp.get("version")))
    lines.append("")
    lines.append("%-10s %-32s %-18s %-6s %s" % ("生态", "包名", "版本", "直接", "来源"))
    lines.append("-" * 100)
    for c in bom.get("components", []):
        props = {p["name"]: p["value"] for p in c.get("properties", [])}
        direct = "是" if props.get("yotta-chain:direct") == "true" else "否"
        resolved = props.get("yotta-chain:resolved", "")
        if len(resolved) > 64:
            resolved = resolved[:61] + "..."
        purl = c.get("purl", "")
        eco = "npm" if "pkg:npm" in purl else ("pypi" if "pkg:pypi" in purl else ("maven" if "pkg:maven" in purl else "?"))
        lines.append("%-10s %-32s %-18s %-6s %s" % (eco, c.get("name", ""), c.get("version", ""), direct, resolved))
    lines.append("")
    lines.append("组件数：%d" % len(bom.get("components", [])))
    return "\n".join(lines)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------

def _csv_escape(v):
    s = str(v)
    if any(c in s for c in ',"\n\r'):
        return '"' + s.replace('"', '""') + '"'
    return s


def _scanned_files(base, eco):
    """Return the input files relevant to the detected ecosystems."""
    out = []
    if "npm" in eco:
        out.append("package.json")
        pj = parse_package_json(_read_text(base / "package.json")) or {}
        lock = _select_npm_lockfile(base, pj)
        if lock is not None:
            out.append(lock.name)
        if (base / ".npmrc").is_file():
            out.append(".npmrc")
    if "python" in eco:
        for path in sorted(base.glob("requirements*.txt")):
            out.append(path.name)
        for name in ("pyproject.toml", "poetry.lock", "uv.lock",
                     "Pipfile", "Pipfile.lock"):
            if (base / name).is_file():
                out.append(name)
    if "maven" in eco and (base / "pom.xml").is_file():
        out.append("pom.xml")
    return sorted(set(out))


def _collect(project_dir, findings, sbom_pkgs, root_component, scanned_files=None):
    """Run all ecosystem checks; returns sorted ecosystem list."""
    base = Path(project_dir)
    eco = []
    if check_npm(project_dir, findings, sbom_pkgs):
        eco.append("npm")
        pj = parse_package_json(_read_text(base / "package.json"))
        if pj.get("name"):
            root_component.update({"ecosystem": "npm", "name": pj["name"], "version": str(pj.get("version") or "")})
    if check_python(project_dir, findings, sbom_pkgs):
        eco.append("python")
        py = parse_toml(_read_text(base / "pyproject.toml"))
        proj = py.get("project") or {}
        if proj.get("name"):
            root_component.update({"ecosystem": "python", "name": proj["name"], "version": str(proj.get("version") or "")})
    if check_maven(project_dir, findings, sbom_pkgs):
        eco.append("maven")
    if scanned_files is not None:
        scanned_files.extend(_scanned_files(base, eco))
    return eco


def cmd_scan(args):
    base = Path(args.path)
    if not base.is_dir():
        print("错误：路径不存在或不是目录：%s" % base, file=sys.stderr)
        return 4
    findings = []
    sbom_pkgs = []
    root_component = {}
    scanned_files = []
    eco = _collect(args.path, findings, sbom_pkgs, root_component, scanned_files=scanned_files)
    if not eco:
        print("错误：%s 下未发现支持的依赖清单/锁文件（package.json / requirements*.txt / pyproject.toml / Pipfile / pom.xml）" % base, file=sys.stderr)
        return 4

    min_rank = SEVERITY_RANK.get(args.level, 0)
    shown = [f for f in findings if SEVERITY_RANK.get(f.severity, 0) >= min_rank]
    shown.sort(key=lambda f: (SEVERITY_RANK.get(f.severity, 0), f.rule, f.package or ""))
    gate_rank = SEVERITY_RANK.get(args.gate, 0)
    gate_hits = [f for f in findings if SEVERITY_RANK.get(f.severity, 0) >= gate_rank]

    if args.format == "json":
        out = {
            "tool": "yotta-chain",
            "version": VERSION,
            "project": str(base),
            "ecosystems": eco,
            "scannedFiles": sorted(set(scanned_files)),
            "files": sorted({f.file for f in findings}),
            "summary": {s: sum(1 for f in findings if f.severity == s) for s in SEVERITY_ORDER},
            "findings": [f.to_dict() for f in shown],
        }
        text = json.dumps(out, ensure_ascii=False, indent=2)
    elif args.format == "csv":
        lines = ["rule,severity,ecosystem,file,line,package,message,detail"]
        for f in shown:
            ln = f.line if f.line is not None else ""
            lines.append(",".join(_csv_escape(x) for x in (
                f.rule, f.severity, f.ecosystem, f.file, ln, f.package or "", f.message, f.detail)))
        text = "\n".join(lines)
    else:
        lines = ["元链 yotta-chain %s — 供应链依赖校验" % VERSION]
        lines.append("项目：%s   生态：%s" % (base, ", ".join(eco)))
        if scanned_files:
            lines.append("输入文件：%s" % ", ".join(sorted(set(scanned_files))))
        if not shown:
            lines.append("未发现 %s 及以上风险项" % args.level)
        for s in SEVERITY_ORDER:
            for f in [x for x in shown if x.severity == s]:
                loc = ("%s:%s" % (f.file, f.line)) if f.line is not None else f.file
                pkg = (" %s" % f.package) if f.package else ""
                lines.append("[%s] %s%s  (%s)" % (s, f.rule, pkg, loc))
                lines.append("    %s" % f.message)
                if f.detail:
                    lines.append("    → %s" % f.detail)
        lines.append("")
        counts = ", ".join("%s %d" % (s, sum(1 for f in findings if f.severity == s)) for s in SEVERITY_ORDER)
        lines.append("共 %d 项（%s）；达到 gate=%s 的有 %d 项" % (len(findings), counts, args.gate, len(gate_hits)))
        text = "\n".join(lines)

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print("报告已写入 %s" % args.output)
    else:
        print(text)
    return 1 if gate_hits else 0


def cmd_sbom(args):
    base = Path(args.path)
    if not base.is_dir():
        print("错误：路径不存在或不是目录：%s" % base, file=sys.stderr)
        return 4
    findings = []
    sbom_pkgs = []
    root_component = {}
    eco = _collect(args.path, findings, sbom_pkgs, root_component)
    if not eco:
        print("错误：%s 下未发现支持的依赖清单/锁文件" % base, file=sys.stderr)
        return 4
    bom = build_sbom(sbom_pkgs, include_dev=not args.exclude_dev, root_component=root_component)
    if args.format == "text":
        text = render_sbom_text(bom)
    else:
        text = json.dumps(bom, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
        print("SBOM 已写入 %s" % args.output)
    else:
        print(text)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="yotta-chain",
        description="元链 yotta-chain — 供应链依赖校验引擎（零依赖 / 纯本地 / 不做在线 CVE）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_scan = sub.add_parser("scan", help="扫描依赖混淆 / lockfile 一致性 / 缺失锁文件 / typo-squat")
    p_scan.add_argument("--path", default=".", help="项目目录（默认当前目录）")
    p_scan.add_argument("--format", choices=["text", "json", "csv"], default="text", help="输出格式")
    p_scan.add_argument("--level", choices=SEVERITY_ORDER, default="info", help="只显示 >= 该级别的发现")
    p_scan.add_argument("--gate", choices=SEVERITY_ORDER, default="info", help="达到该级别即退出码 1（CI 用）")
    p_scan.add_argument("--output", "-o", default=None, help="写入文件")
    p_scan.set_defaults(func=cmd_scan)

    p_sbom = sub.add_parser("sbom", help="生成 SBOM-lite（CycloneDX 1.5 子集 JSON）")
    p_sbom.add_argument("--path", default=".")
    p_sbom.add_argument("--format", choices=["cyclonedx", "text"], default="cyclonedx")
    p_sbom.add_argument("--exclude-dev", action="store_true", help="不包含 dev/optional 依赖")
    p_sbom.add_argument("--output", "-o", default=None)
    p_sbom.set_defaults(func=cmd_sbom)

    p_ver = sub.add_parser("version", help="显示版本")
    p_ver.set_defaults(func=lambda a: (print(VERSION) or 0))

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
