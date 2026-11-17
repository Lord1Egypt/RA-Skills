"""The project's file graph: which files import which, where the app starts, and
which notable outside services and data stores the code reaches.

Everything here is static text analysis; nothing is executed."""
from __future__ import annotations

import hashlib
import json
import os
import re
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

from common import git_ignored, is_within, iter_files, read_text, rel

JS_EXTS = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte")
PY_EXT = ".py"
HTML_EXT = ".html"
# an inline <script> (no src) with real code in it: the page's own logic, which a vibe-coded app often keeps there
INLINE_SCRIPT = re.compile(r"<script\b(?![^>]*\bsrc\s*=)(?![^>]*\btype\s*=\s*[\"']?(?:application/(?:ld\+)?json|text/template)\b)[^>]*>([\s\S]*?)</script>", re.I)
INLINE_MIN = 200  # characters: below this an inline script is a one-liner, not the page's logic
# a path the page's script names — fetch("/api/entries"), const url = '/api/export?month=', the same on
# http://localhost:3001 — that a server file
# also names as a string is how the page talks to it; asset paths (a stylesheet, an image) are not
PAGE_PATH = re.compile(r"""[`'"](?:https?://(?:localhost|127\.0\.0\.1)(?::\d+)?)?(/[A-Za-z][A-Za-z0-9_\-/.]*)(?=[`'"?#$])""")
ASSET_EXT = re.compile(r"\.(?:css|js|mjs|png|jpe?g|gif|svg|ico|webp|woff2?|ttf|html?|map)$", re.I)
RESOLVE_EXTS = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue", ".svelte")
TEST_FILE = re.compile(r"(?:^|/)(?:tests?|__tests__|spec|fixtures?)/|\.(?:test|spec)\.[a-z]+$")
CONFIG_FILE = re.compile(r"(?:^|/)(?:[^/]+\.config\.[a-z]+|\.eslintrc[^/]*|\.prettierrc[^/]*|jest\.setup\.[a-z]+"
                         r"|setupTests\.[a-z]+)$")
FOLDER_THRESHOLD = 80
FOLDER_MAX = 40  # a collapsed folder bigger than this is split one level further when it can be
EXPLAIN_MAX = 30
EXPLAIN_CHUNK = 8

_PY_LINE_COMMENT = re.compile(r"#[^\n]*")
JS_IMPORT = re.compile(
    r"""(?:^|[;\n}])[ \t]*(?:import|export)[ \t]+(?P<clause>[^'"`;]*?)[ \t]*\bfrom[ \t]*['"](?P<a>[^'"\n]+)['"]"""
    r"""|(?:^|[;\n}])[ \t]*import[ \t]*['"](?P<b>[^'"\n]+)['"]"""
    r"""|\bimport\(\s*['"](?P<c>[^'"\n]+)['"]\s*\)"""
    r"""|\brequire\(\s*['"](?P<d>[^'"\n]+)['"]\s*\)""")
PY_FROM = re.compile(r"^[ \t]*from[ \t]+(\.*)([\w.]*)[ \t]+import[ \t]+\(?([^\n#)]*)", re.M)
PY_IMPORT = re.compile(r"^[ \t]*import[ \t]+([\w.]+(?:[ \t]*,[ \t]*[\w.]+)*)", re.M)
_NAME = re.compile(r"[A-Za-z_$][\w$]*")
_NOT_NAMES = {"import", "export", "type", "as", "from", "default", "typeof"}


def _blank(m: re.Match) -> str:
    return re.sub(r"[^\n]", " ", m.group(0))


def _strip_js(text: str) -> str:
    """Blank // and /* */ comments, skipping string literals: a Chrome match pattern such as
    "*://*/*" holds both markers and must not swallow the code after it."""
    out, i, n = list(text), 0, len(text)
    while i < n:
        c = text[i]
        if c in "'\"`":
            j = i + 1
            while j < n and text[j] != c:
                if text[j] == "\\":
                    j += 1
                elif text[j] == "\n" and c != "`":
                    break  # an unterminated quote (an apostrophe in JSX text) ends with its line
                j += 1
            i = j + 1
        elif text.startswith("//", i):
            j = text.find("\n", i)
            j = n if j < 0 else j
            out[i:j] = " " * (j - i)
            i = j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j < 0 else j + 2
            out[i:j] = [ch if ch == "\n" else " " for ch in text[i:j]]
            i = j
        else:
            i += 1
    return "".join(out)


def strip_comments(text: str, lang: str) -> str:
    if lang == "py":
        return _PY_LINE_COMMENT.sub(_blank, text)
    return _strip_js(text)


def _line(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def js_imports(text: str) -> list[tuple[str, int, list[str]]]:
    clean = strip_comments(text, "js")
    out = []
    for m in JS_IMPORT.finditer(clean):
        key = next(k for k in ("a", "b", "c", "d") if m.group(k))
        names = [n for n in _NAME.findall(m.group("clause") or "") if n not in _NOT_NAMES][:12] if key == "a" else []
        start = m.start("clause") if key == "a" else m.start(key)  # the line where the statement starts
        out.append((m.group(key), _line(clean, start), names))
    return out


def py_imports(text: str) -> list[tuple[str, str, int, list[str]]]:
    clean = strip_comments(text, "py")
    found = []
    for m in PY_FROM.finditer(clean):
        names = [n.split(" as ")[0].strip() for n in m.group(3).split(",") if n.strip()]
        found.append((m.start(), (m.group(1), m.group(2), _line(clean, m.start(1)), [n for n in names if n != "*"])))
    for m in PY_IMPORT.finditer(clean):
        line = _line(clean, m.start(1))
        for i, mod in enumerate(x.strip() for x in m.group(1).split(",")):
            found.append((m.start() + i, ("", mod, line, [])))
    return [item for _, item in sorted(found, key=lambda f: f[0])]


def has_inline_code(html: str) -> bool:
    return sum(len(m.group(1).strip()) for m in INLINE_SCRIPT.finditer(html)) >= INLINE_MIN


def _in_inline_script(html: str, pos: int) -> bool:
    return any(m.start(1) <= pos < m.end(1) for m in INLINE_SCRIPT.finditer(html))


def page_fetch_edges(files: dict, texts: dict) -> list[tuple[str, str, int, list]]:
    """(page, server file, line, [path]) for each path a page's script fetches that a server file names as a string."""
    out = []
    servers = [f for f in sorted(files) if not f.endswith(HTML_EXT)]
    for page in sorted(f for f in files if f.endswith(HTML_EXT)):
        seen = set()
        for m in PAGE_PATH.finditer(texts[page]):
            path = m.group(1).rstrip("/")
            if len(path) < 2 or path in seen or ASSET_EXT.search(path) or not _in_inline_script(texts[page], m.start()):
                continue
            seen.add(path)
            lit = re.compile(r"""[`'"]""" + re.escape(path) + r"""(?:[`'"/?]|$)""")
            for srv in servers:
                if lit.search(texts[srv]):
                    out.append((page, srv, _line(texts[page], m.start()), [path]))
    return out


def collect_files(root) -> tuple[dict[str, Path], Counter]:
    root = Path(root).resolve()
    files: dict[str, Path] = {}
    excluded: Counter = Counter()
    found = {rel(p, root): p for p in iter_files(root, set(JS_EXTS) | {PY_EXT, HTML_EXT})}
    # a page counts as code only when it carries its own script; plain markup and templates stay out
    found = {r: p for r, p in found.items() if not r.endswith(HTML_EXT) or has_inline_code(read_text(p))}
    ignored = git_ignored(root, found)  # generated output, caches, local scratch
    for r, p in found.items():
        if r in ignored:
            excluded["ignored by git"] += 1
        elif TEST_FILE.search(r):
            excluded["tests"] += 1
        elif CONFIG_FILE.search(r):
            excluded["config"] += 1
        else:
            files[r] = p
    return files, excluded


def _strip_jsonc(text: str) -> str:
    out, i, n, in_str = [], 0, len(text), False
    while i < n:
        c = text[i]
        if in_str:
            out.append(c)
            if c == "\\" and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            in_str = c != '"'
            i += 1
            continue
        if c == '"':
            in_str = True
            out.append(c)
            i += 1
        elif text.startswith("//", i):
            j = text.find("\n", i)
            i = n if j < 0 else j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            i = n if j < 0 else j + 2
        else:
            out.append(c)
            i += 1
    return re.sub(r",(\s*[}\]])", r"\1", "".join(out))


def _norm(path: str) -> str:
    return PurePosixPath(os.path.normpath(path)).as_posix()


def _config_chain(path: Path, seen: set) -> list[tuple[Path, dict]]:
    """[(folder, compilerOptions)] from the farthest base config to `path`, following relative `extends`."""
    if path in seen or not path.is_file():
        return []
    seen.add(path)
    try:
        cfg = json.loads(_strip_jsonc(read_text(path)))
    except json.JSONDecodeError:
        return []
    if not isinstance(cfg, dict):
        return []
    chain: list[tuple[Path, dict]] = []
    ext = cfg.get("extends")
    for e in [ext] if isinstance(ext, str) else ext if isinstance(ext, list) else []:
        if isinstance(e, str) and e.startswith("."):  # a package name (@tsconfig/…) holds no project paths
            target = path.parent / e
            if not target.is_file() and target.suffix != ".json":
                target = target.with_name(target.name + ".json")
            chain += _config_chain(target.resolve(), seen)
    opts = cfg.get("compilerOptions")
    chain.append((path.parent, opts if isinstance(opts, dict) else {}))
    return chain


def _aliases_from(config: Path, root: Path) -> list[tuple[str, list[str], bool]]:
    """Aliases of one tsconfig/jsconfig, targets relative to the project root. As in TypeScript, a later config's
    `paths` replaces an earlier one's, and targets resolve against the effective baseUrl (or the config that
    defined `paths` when there is none)."""
    base_dir = paths_dir = None
    paths: dict = {}
    for folder, opts in _config_chain(config.resolve(), set()):
        if isinstance(opts.get("baseUrl"), str):
            base_dir = folder / opts["baseUrl"]
        if isinstance(opts.get("paths"), dict):
            paths, paths_dir = opts["paths"], folder
    anchor = base_dir or paths_dir
    out = []
    for key, targets in paths.items():
        wild = key.endswith("*")
        outs = []
        for t in targets if isinstance(targets, list) else []:
            if not isinstance(t, str):
                continue
            target = Path(os.path.normpath(anchor / (t[:-1] if t.endswith("*") else t)))
            if is_within(target, root):
                outs.append(rel(target, root) or ".")
        out.append((key[:-1] if wild else key, outs, wild))
    return sorted(out, key=lambda a: -len(a[0]))


def load_aliases(root) -> list[tuple[str, list[str], bool]]:
    """The project root's aliases (tsconfig.json, else jsconfig.json)."""
    root = Path(root).resolve()
    for name in ("tsconfig.json", "jsconfig.json"):
        if (root / name).is_file():
            return _aliases_from(root / name, root)
    return []


def alias_scopes(root) -> list[tuple[str, list]]:
    """[(folder, aliases)] for every tsconfig/jsconfig in the project, deepest folder first: in a monorepo each
    package's config applies to the files under it."""
    root = Path(root).resolve()
    found: dict[str, Path] = {}
    for p in iter_files(root, {".json"}):
        if p.name in ("tsconfig.json", "jsconfig.json"):
            folder = PurePosixPath(rel(p, root)).parent.as_posix()
            folder = "" if folder == "." else folder
            if folder not in found or p.name == "tsconfig.json":
                found[folder] = p
    scopes = [(folder, _aliases_from(p, root)) for folder, p in found.items()]
    return sorted(scopes, key=lambda sc: -len(sc[0]))


def aliases_for(path: str, scopes) -> list:
    for folder, aliases in scopes:
        if not folder or path.startswith(folder + "/"):
            return aliases
    return []


def _candidates(base: Path):
    yield base
    if base.suffix in (".js", ".jsx", ".mjs", ".cjs"):  # TS ESM writes "./util.js" for util.ts
        for ext in (".ts", ".tsx", ".mts", ".cts"):
            yield base.with_suffix(ext)
    for ext in RESOLVE_EXTS:
        yield base.with_name(base.name + ext)
    for ext in RESOLVE_EXTS:
        yield base / f"index{ext}"


def resolve_js(spec: str, src: str, root, aliases) -> tuple[str, str | None]:
    root = Path(root).resolve()
    spec = spec.split("?")[0]
    bases: list[Path] = []
    if spec.startswith("."):
        bases = [root / PurePosixPath(src).parent / spec]
    else:
        for prefix, targets, wild in aliases:
            if (wild and spec.startswith(prefix)) or (not wild and spec == prefix):
                rest = spec[len(prefix):] if wild else ""
                bases = [root / t / rest if rest else root / t for t in targets]
                break
        else:
            if spec.startswith("@/"):
                bases = [root / "src" / spec[2:], root / spec[2:]]
            elif spec.startswith("~/"):
                bases = [root / spec[2:]]
            elif spec.startswith("/"):
                bases = [root / spec[1:]]  # root-absolute, as Vite's index.html writes it
    if not bases:
        return "package", spec
    for base in bases:
        for cand in _candidates(base):
            if cand.is_file() and is_within(cand, root):
                return "file", rel(cand, root)
    return "missing", None


def resolve_py(dots: str, module: str, src: str, root) -> tuple[str, str | None]:
    root = Path(root).resolve()
    parts = [p for p in module.split(".") if p]
    if dots:
        base = root / PurePosixPath(src).parent
        for _ in range(len(dots) - 1):
            base = base.parent
        target = base.joinpath(*parts)
        cands = ([target.with_suffix(".py")] if parts else []) + [target / "__init__.py"]
        for cand in cands:
            if cand.is_file() and is_within(cand, root):
                return "file", rel(cand, root)
        return "missing", None
    # A script run directly has its own folder first on sys.path, so in a folder that is
    # not a package `import workshop` means the sibling workshop.py. Inside a package an
    # absolute import stays absolute.
    here = root / PurePosixPath(src).parent
    tops = [root, root / "src"]
    if here != root and not (here / "__init__.py").is_file():
        tops.insert(0, here)
    for top in tops:
        target = top.joinpath(*parts)
        for cand in (target.with_suffix(".py"), target / "__init__.py"):
            if cand.is_file():
                return "file", rel(cand, root)
    return "package", module


EXT_PACKAGES = {
    "openai": ("openai", "OpenAI API", "paid"),
    "@anthropic-ai/sdk": ("anthropic", "Anthropic API", "paid"),
    "@google/genai": ("google-ai", "Google AI API", "paid"),
    "@google/generative-ai": ("google-ai", "Google AI API", "paid"),
    "groq-sdk": ("groq", "Groq API", "paid"),
    "cohere-ai": ("cohere", "Cohere API", "paid"),
    "replicate": ("replicate", "Replicate API", "paid"),
    "elevenlabs": ("elevenlabs", "ElevenLabs API", "paid"),
    "@elevenlabs/elevenlabs-js": ("elevenlabs", "ElevenLabs API", "paid"),
    "stripe": ("stripe", "Stripe", "paid"),
    "twilio": ("twilio", "Twilio", "paid"),
    "resend": ("resend", "Resend", "paid"),
    "@supabase/supabase-js": ("supabase", "Supabase", "data"),
    "@supabase/ssr": ("supabase", "Supabase", "data"),
    "firebase": ("firebase", "Firebase", "data"),
    "firebase-admin": ("firebase", "Firebase", "data"),
    "@prisma/client": ("prisma", "Prisma database", "data"),
    "pg": ("postgres", "PostgreSQL", "data"),
    "mysql2": ("mysql", "MySQL", "data"),
    "mongoose": ("mongodb", "MongoDB", "data"),
    "redis": ("redis", "Redis", "data"),
    "ioredis": ("redis", "Redis", "data"),
}
PY_PACKAGES = {
    "openai": ("openai", "OpenAI API", "paid"),
    "anthropic": ("anthropic", "Anthropic API", "paid"),
    "stripe": ("stripe", "Stripe", "paid"),
    "twilio": ("twilio", "Twilio", "paid"),
    "supabase": ("supabase", "Supabase", "data"),
    "firebase_admin": ("firebase", "Firebase", "data"),
    "sqlite3": ("sqlite", "SQLite", "data"),
    "psycopg2": ("postgres", "PostgreSQL", "data"),
    "psycopg": ("postgres", "PostgreSQL", "data"),
    "pymongo": ("mongodb", "MongoDB", "data"),
    "redis": ("redis", "Redis", "data"),
    "sqlalchemy": ("sql", "SQL database", "data"),
}
EXT_URLS = [
    (re.compile(r"https?://api\.openai\.com"), ("openai", "OpenAI API", "paid")),
    (re.compile(r"https?://api\.anthropic\.com"), ("anthropic", "Anthropic API", "paid")),
    (re.compile(r"https?://api\.deepseek\.com"), ("deepseek", "DeepSeek API", "paid")),
    (re.compile(r"https?://generativelanguage\.googleapis\.com"), ("google-ai", "Google AI API", "paid")),
    (re.compile(r"https?://api\.stripe\.com"), ("stripe", "Stripe", "paid")),
    (re.compile(r"https?://api\.elevenlabs\.io"), ("elevenlabs", "ElevenLabs API", "paid")),
    (re.compile(r"https?://api\.minimaxi?\.(?:io|chat|com)"), ("minimax", "MiniMax API", "paid")),
    (re.compile(r"https?://api\.moonshot\.(?:cn|ai)"), ("moonshot", "Moonshot (Kimi) API", "paid")),
    (re.compile(r"https?://dashscope(?:-intl)?\.aliyuncs\.com"), ("dashscope", "Alibaba DashScope (Qwen) API", "paid")),
    (re.compile(r"https?://api\.groq\.com"), ("groq", "Groq API", "paid")),
    (re.compile(r"https?://api\.mistral\.ai"), ("mistral", "Mistral API", "paid")),
    (re.compile(r"https?://[\w-]+\.supabase\.co"), ("supabase", "Supabase", "data")),
]
STORAGE_APIS = [
    (re.compile(r"\blocalStorage\b"), ("local-storage", "localStorage", "data")),
    (re.compile(r"\bsessionStorage\b"), ("session-storage", "sessionStorage", "data")),
    (re.compile(r"\bindexedDB\.open\b"), ("indexeddb", "IndexedDB", "data")),
    (re.compile(r"\bchrome\.storage\.(?:local|session|sync)\b"), ("chrome-storage", "chrome.storage", "data")),
]
JS_EXPORTS = [
    re.compile(r"^[ \t]*export[ \t]+(?:default[ \t]+)?(?:async[ \t]+)?function\*?[ \t]*([A-Za-z_$][\w$]*)", re.M),
    re.compile(r"^[ \t]*export[ \t]+(?:declare[ \t]+)?(?:const|let|var|class|abstract[ \t]+class|interface|type|enum)"
               r"[ \t]+([A-Za-z_$][\w$]*)", re.M),
    re.compile(r"^[ \t]*export[ \t]+default[ \t]+class[ \t]+([A-Za-z_$][\w$]*)", re.M),
    re.compile(r"^[ \t]*(?:module\.)?exports\.([A-Za-z_$][\w$]*)[ \t]*=", re.M),
]
EXPORT_LIST = re.compile(r"^[ \t]*export[ \t]*\{([^}]*)\}(?![ \t]*from)", re.M)
MODULE_EXPORTS_OBJ = re.compile(r"module\.exports[ \t]*=[ \t]*\{([^}]*)\}")
PY_EXPORT = re.compile(r"^(?:async[ \t]+)?def[ \t]+([A-Za-z]\w*)|^class[ \t]+([A-Za-z]\w*)", re.M)
NEXT_ENTRY = re.compile(r"(?:^|/)app/(?:.+/)?(?:page|route)\.(?:t|j)sx?$"
                        r"|(?:^|/)pages/(?!_app\.|_document\.)(?:[^/]+/)*[^/]+\.(?:t|j)sx?$")
SCRIPT_SRC = re.compile(r"""<script\b[^>]*?\bsrc\s*=\s*["']([^"']+)["']""", re.I)
LISTEN = re.compile(r"\.listen\(")
PY_MAIN = re.compile(r"""^if\s+__name__\s*==\s*['"]__main__['"]\s*:""", re.M)


def _line_text(text: str, lineno: int) -> str:
    lines = text.splitlines()
    return lines[lineno - 1].strip()[:200] if 0 < lineno <= len(lines) else ""


def exports(text: str, lang: str) -> list[dict]:
    found: list[tuple[int, str]] = []
    src = text if lang == "py" else strip_comments(text, "js")
    if lang == "py":
        found = [(m.start(), m.group(1) or m.group(2)) for m in PY_EXPORT.finditer(src)]
    else:
        for rx in JS_EXPORTS:
            found += [(m.start(1), m.group(1)) for m in rx.finditer(src)]
        for rx, sep in ((EXPORT_LIST, " as "), (MODULE_EXPORTS_OBJ, ":")):
            for m in rx.finditer(src):
                for part in m.group(1).split(","):
                    if not part.strip():
                        continue
                    name = part.split(sep)[-1 if sep == " as " else 0].strip()
                    if _NAME.fullmatch(name) and name != "default":
                        found.append((m.start(1) + m.group(1).find(part), name))
    out, seen = [], set()
    for pos, name in sorted(found):
        if name not in seen:
            seen.add(name)
            out.append({"name": name, "line": _line(src, pos)})
    return out


def _load_json(path):
    path = Path(path)
    if not path.is_file():
        return None
    try:
        return json.loads(read_text(path))
    except json.JSONDecodeError:
        return None


def _html_scripts(root: Path, page: str) -> list[str]:
    html = root / _norm(page)
    if not html.is_file():
        return []
    out = []
    for src in SCRIPT_SRC.findall(read_text(html)):
        if re.match(r"^[a-z][a-z0-9+.-]*:", src, re.I) or src.startswith("//"):
            continue  # remote scripts are not project files
        target = root / src.lstrip("/") if src.startswith("/") else html.parent / src
        if target.is_file() and is_within(target, root):
            out.append(rel(target, root))
    return out


def _uses_next(root: Path, pkg) -> bool:
    """Next.js routing rules apply only to a Next.js project; a Vite app's src/pages/ is ordinary code."""
    if isinstance(pkg, dict):
        for key in ("dependencies", "devDependencies"):
            if isinstance(pkg.get(key), dict) and "next" in pkg[key]:
                return True
    return any(root.glob("next.config.*"))


def find_entries(root, files: dict, texts: dict | None = None) -> dict[str, str]:
    root = Path(root).resolve()
    texts = texts if texts is not None else {r: read_text(p) for r, p in files.items()}
    entries: dict[str, str] = {}

    def add(path, reason):
        if path and path in files and path not in entries:
            entries[path] = reason

    pkg = _load_json(root / "package.json")
    if _uses_next(root, pkg):
        for f in sorted(files):
            if NEXT_ENTRY.search(f):
                add(f, "next.js page or route")
    manifest = _load_json(root / "manifest.json")
    if isinstance(manifest, dict) and "manifest_version" in manifest:
        bg = manifest.get("background") or {}
        for s in [bg.get("service_worker"), *(bg.get("scripts") or [])]:
            if isinstance(s, str):
                add(_norm(s), "manifest background script")
        for cs in manifest.get("content_scripts") or []:
            for s in (cs.get("js") or []) if isinstance(cs, dict) else []:
                add(_norm(s), "manifest content script")
        pages = [("side panel", (manifest.get("side_panel") or {}).get("default_path")),
                 ("popup", (manifest.get("action") or {}).get("default_popup")
                  or (manifest.get("browser_action") or {}).get("default_popup")),
                 ("options page", manifest.get("options_page") or (manifest.get("options_ui") or {}).get("page")),
                 ("devtools page", manifest.get("devtools_page"))]
        for label, page in pages:
            if isinstance(page, str):
                for s in _html_scripts(root, page):
                    add(s, f"manifest {label} → {_norm(page)}")
    for html in ("index.html", "public/index.html"):
        for s in _html_scripts(root, html):
            add(s, f"{html} script")
    if isinstance(pkg, dict):
        if isinstance(pkg.get("main"), str):
            add(_norm(pkg["main"]), "package.json main")
        bins = pkg.get("bin")
        for b in [bins] if isinstance(bins, str) else list(bins.values()) if isinstance(bins, dict) else []:
            if isinstance(b, str):
                add(_norm(b), "package.json bin")
    for f in sorted(files):
        if f.endswith(HTML_EXT):
            add(f, "page with its own script")
        elif f.endswith(JS_EXTS) and LISTEN.search(texts[f]):
            add(f, "starts a server (.listen)")
        elif f.endswith(PY_EXT) and (PY_MAIN.search(texts[f]) or PurePosixPath(f).name in ("app.py", "main.py", "manage.py")):
            add(f, "python entry point")
    return entries


def edits_from_digest(recs, root) -> dict[str, dict]:
    root = Path(root).resolve()
    out: dict[str, dict] = {}
    for r in recs:
        if r.get("kind") != "edit":
            continue
        ts = r.get("ts") or ""
        for f in r.get("files", []):
            if not is_within(f, root):
                continue
            e = out.setdefault(rel(f, root), {"count": 0, "first": ts, "last": ts})
            e["count"] += 1
            if ts and (not e["first"] or ts < e["first"]):
                e["first"] = ts
            if ts > e["last"]:
                e["last"] = ts
    return out


def folder_groups(paths) -> list[dict]:
    """Group by the shallowest folder depth that splits the files into at least 3 groups. A group of more than
    FOLDER_MAX files is split one level further while it has subfolders to split into, so opening a folder never
    pours out a hundred cards when it need not. Files above a split, and groups of one file, stay single nodes."""
    dirs = {p: PurePosixPath(p).parent.parts for p in paths}
    for depth in range(1, max((len(d) for d in dirs.values()), default=0) + 1):
        groups: dict[str, list[str]] = defaultdict(list)
        for p, parts in dirs.items():
            if len(parts) >= depth:
                groups["/".join(parts[:depth])].append(p)
        if len(groups) < 3:
            continue
        kept, pending = [], list(groups.items())
        while pending:
            key, members = pending.pop()
            level = key.count("/") + 1
            below: dict[str, list[str]] = defaultdict(list)
            for p in members:
                if len(dirs[p]) > level:
                    below["/".join(dirs[p][:level + 1])].append(p)
            if len(members) > FOLDER_MAX and len(below) >= 2:
                pending += list(below.items())
            else:
                kept.append((key, members))
        return [{"id": k, "files": sorted(v)} for k, v in sorted(kept) if len(v) >= 2]
    return []


def _package_root(spec: str) -> str:
    parts = spec.split("/")
    return "/".join(parts[:2]) if spec.startswith("@") else parts[0]


def _add_edge(edges: dict, a: str, b: str, line: int, names) -> None:
    e = edges.get((a, b))
    if e is None:
        edges[(a, b)] = {"from": a, "to": b, "line": line, "names": list(names)}
    else:
        e["names"] += [n for n in names if n not in e["names"]]


def build(root, recs, probes) -> dict:
    root = Path(root).resolve()
    files, excluded = collect_files(root)
    texts = {r: read_text(p) for r, p in files.items()}
    scopes = alias_scopes(root)
    edges: dict = {}
    unresolved: list[dict] = []
    ext_info: dict[str, tuple] = {}
    ext_hits: dict[str, list] = {}
    file_ext: dict[tuple, int] = {}

    def hit(f, info, line):
        key = info[0]
        ext_info[key] = info
        ev = ext_hits.setdefault(key, [])
        if len(ev) < 3 and all(e["path"] != f for e in ev):
            ev.append({"path": f, "line": line, "snippet": _line_text(texts[f], line)})
        file_ext.setdefault((f, key), line)

    for f in sorted(files):
        lang = "py" if f.endswith(PY_EXT) else "js"
        if lang == "js":
            for spec, line, names in js_imports(texts[f]):
                kind, target = resolve_js(spec, f, root, aliases_for(f, scopes))
                if kind == "file":
                    if target in files and target != f:
                        _add_edge(edges, f, target, line, names)
                elif kind == "missing":
                    unresolved.append({"from": f, "spec": spec, "line": line})
                elif _package_root(spec) in EXT_PACKAGES:
                    hit(f, EXT_PACKAGES[_package_root(spec)], line)
        else:
            for dots, module, line, names in py_imports(texts[f]):
                targets = []
                if dots and not module:
                    targets = [t for k, t in (resolve_py(dots, n, f, root) for n in names) if k == "file"]
                    if not targets:
                        kind, target = resolve_py(dots, "", f, root)
                        if kind == "file":
                            targets = [target]
                        else:
                            unresolved.append({"from": f, "spec": dots, "line": line})
                else:
                    kind, target = resolve_py(dots, module, f, root)
                    if kind == "file":
                        targets = [target]
                    elif kind == "missing":
                        unresolved.append({"from": f, "spec": dots + module, "line": line})
                    elif module.split(".")[0] in PY_PACKAGES:
                        hit(f, PY_PACKAGES[module.split(".")[0]], line)
                for t in targets:
                    if t in files and t != f:
                        _add_edge(edges, f, t, line, names)
        clean = strip_comments(texts[f], lang)
        for rx, info in EXT_URLS + (STORAGE_APIS if lang == "js" else []):
            m = rx.search(clean)
            if m:
                hit(f, info, _line(clean, m.start()))
    for page, srv, line, names in page_fetch_edges(files, texts):
        _add_edge(edges, page, srv, line, names)
    for (f, key), line in sorted(file_ext.items()):
        _add_edge(edges, f, "ext:" + key, line, [])
    edge_list = sorted(edges.values(), key=lambda e: (e["from"], e["to"]))
    indeg = Counter(e["to"] for e in edge_list if not e["to"].startswith("ext:"))
    entries = find_entries(root, files, texts) or {f: "not imported by any file" for f in files if indeg[f] == 0}
    levels: dict[str, set] = defaultdict(set)
    for fd in probes.get("findings", []):
        levels[fd.get("path")].add(fd.get("level"))
    edits = edits_from_digest(recs, root)
    has_ext = {f for f, _key in file_ext}
    nodes = []
    for f in sorted(files):
        lv = levels.get(f, set())
        score = ((3 if f in entries else 0) + (3 if "certain" in lv else 1 if "hint" in lv else 0)
                 + min(indeg[f], 5) + (2 if f in has_ext else 0) + min((edits.get(f) or {}).get("count", 0) // 3, 3))
        parent = PurePosixPath(f).parent.as_posix()
        nodes.append({"id": f, "label": PurePosixPath(f).name, "folder": "" if parent == "." else parent,
                      "role": "entry" if f in entries else "logic", "lines": texts[f].count("\n") + 1,
                      "exports": exports(texts[f], "py" if f.endswith(PY_EXT) else "js"),
                      "score": score, "explain": False, "edits": edits.get(f),
                      "sha": hashlib.sha1(texts[f].encode("utf-8", "replace")).hexdigest()[:12]})  # for comparing runs
    # the score caps fan-in at 5, so a big project has many ties; break them by how many
    # files really depend on the file, then by how often it was edited — not by name
    def rank(n):
        return (-n["score"], -indeg[n["id"]], -((n["edits"] or {}).get("count", 0)), n["id"])
    ranked = sorted((n for n in nodes if n["score"] > 0), key=rank)
    # no one folder takes more than half the slots while other folders have candidates
    # (every script in a scripts/ folder is an entry and would otherwise fill them all);
    # slots nobody else can use go back to the ranking
    cap, per_folder, chosen = -(-EXPLAIN_MAX // 2), Counter(), []
    for n in ranked:
        if len(chosen) < EXPLAIN_MAX and per_folder[n["folder"]] < cap:
            chosen.append(n)
            per_folder[n["folder"]] += 1
    picked = {id(n) for n in chosen}
    chosen += [n for n in ranked if id(n) not in picked][:EXPLAIN_MAX - len(chosen)]
    for n in chosen:
        n["explain"] = True
    collapsed = len(nodes) > FOLDER_THRESHOLD
    return {"nodes": nodes,
            "externals": [{"id": "ext:" + k, "label": ext_info[k][1], "kind": ext_info[k][2], "evidence": ext_hits[k]}
                          for k in sorted(ext_info)],
            "edges": edge_list,
            "entries": [{"path": p, "reason": r} for p, r in sorted(entries.items())],
            "folders": folder_groups(sorted(files)) if collapsed else [],
            "collapsed": collapsed, "unresolved": unresolved, "excluded": dict(excluded),
            "languages": sorted({"py" if f.endswith(PY_EXT) else "js" for f in files})}


def explain_pack(g: dict, root, probes) -> str:
    import areas
    chosen = sorted((n for n in g["nodes"] if n["explain"]), key=lambda n: (-n["score"], n["id"]))
    uses, used_by = defaultdict(list), defaultdict(list)
    for e in g["edges"]:
        uses[e["from"]].append(e["to"])
        used_by[e["to"]].append(e["from"])
    labels = {x["id"]: x["label"] for x in g["externals"]}
    findings = defaultdict(list)
    for fd in probes.get("findings", []):
        findings[fd.get("path")].append(fd)
    lines = ["# vibe-ledger explain pack", "", f"Project: {root}", "",
             "Write `explain.json` for the files below as references/explain-guide.md describes. They are the most "
             "important files (entry points, files with findings, files many others use); every other file gets an "
             "automatic summary.", ""]
    groups = [chosen[i:i + EXPLAIN_CHUNK] for i in range(0, len(chosen), EXPLAIN_CHUNK)]
    if len(groups) > 1:
        lines += [f"There are {len(chosen)} files in {len(groups)} groups. Give each group to its own subagent (or do "
                  "them one by one); each group writes the parts file named in its heading, then run `vl.py merge`.", ""]
    for gi, group in enumerate(groups, 1):
        if len(groups) > 1:
            lines += [f"## Group {gi} → parts/explain_{gi:02d}.json", ""]
        for n in group:
            lines.append(f"### {n['id']}  (score {n['score']}, {n['role']}, {n['lines']} lines)")
            if n["exports"]:
                lines.append("- exports: " + ", ".join(f"{x['name']} (line {x['line']})" for x in n["exports"][:20]))
            if uses[n["id"]]:
                lines.append("- uses: " + ", ".join(labels.get(t, t) for t in uses[n["id"]]))
            if used_by[n["id"]]:
                lines.append("- used by: " + ", ".join(used_by[n["id"]]))
            for fd in findings.get(n["id"], []):
                lines.append(f"- check ({fd.get('level')}): {fd.get('message')} (line {fd.get('line')})")
            if n.get("edits"):
                lines.append(f"- changed in the conversations {n['edits']['count']} times")
            lines.append("")
    if not chosen:
        lines.append('_No file needs a detailed explanation; write `{"evidence": {}, "files": {}}`._')
        return "\n".join(lines) + "\n" + ("\n" + areas.pack_section(g, root) if g["nodes"] else "")
    where = ("in `explain.json` after `vl.py merge` (one writer for the whole project, not one per group)"
             if len(groups) > 1 else "in `explain.json`")
    lines += ["## Journeys", "",
              f"Also write 2–4 `journeys` {where}: something the user does (\"你点「分析」时\"), and the files it "
              "passes through in order, one plain sentence per step (references/explain-guide.md). Start from the "
              "entry points:", ""]
    lines += [f"- {e['path']} ({e['reason']})" for e in g["entries"]]
    return "\n".join(lines) + "\n\n" + areas.pack_section(g, root)
