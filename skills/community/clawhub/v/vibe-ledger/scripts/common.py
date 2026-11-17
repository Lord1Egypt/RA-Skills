"""Shared helpers for vibe-ledger: paths, JSONL I/O, text normalisation,
project-file walking and the regexes several steps agree on."""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import unicodedata
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Iterator

__version__ = "1.0.0"

_WS = re.compile(r"\s+")


def norm_ws(text: str | None) -> str:
    """NFC-normalise and collapse every whitespace run to one space."""
    return _WS.sub(" ", unicodedata.normalize("NFC", text or "")).strip()


def slugify(name: str) -> str:
    s = re.sub(r"[^\w]+", "-", name).strip("-").lower()
    return s or "project"


def project_id(root) -> str:
    root = Path(root).resolve()
    digest = hashlib.sha1(str(root).encode("utf-8")).hexdigest()[:8]
    return f"{slugify(root.name)}-{digest}"


def home_dir() -> Path:
    env = os.environ.get("VIBE_LEDGER_HOME")
    return Path(env) if env else Path.home() / ".vibe-ledger"


def project_workdir(root) -> Path:
    return home_dir() / "projects" / project_id(root)


@lru_cache(maxsize=65536)
def _resolved(path: str) -> str:
    try:
        return str(Path(path).resolve())
    except OSError:
        return os.path.abspath(path)


def is_within(path, root) -> bool:
    """True when `path` is `root` or inside it, after resolving symlinks."""
    if not path or not root:
        return False
    p, r = _resolved(str(path)), _resolved(str(root))
    return p == r or p.startswith(r.rstrip(os.sep) + os.sep)


def rel(path, root) -> str:
    return Path(_resolved(str(path))).relative_to(_resolved(str(root))).as_posix()


def read_jsonl(path) -> Iterator[tuple[int, dict | None]]:
    """(line number, object) per non-empty line; object is None for a bad line."""
    with open(path, encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                yield lineno, None
                continue
            yield lineno, obj if isinstance(obj, dict) else None


def write_json(path, obj) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_jsonl(path, rows: Iterable[dict]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


SKIP_DIRS = {".git", "node_modules", ".next", "dist", "build", "out", ".venv", "venv",
             "__pycache__", ".turbo", ".vercel", ".cache", "coverage", ".svelte-kit",
             ".nuxt", "vendor", ".expo", ".idea", ".vscode",
             ".remotion"}  # Remotion's download cache (a whole headless Chrome), not the project's code
CODE_EXTS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".py", ".rb",
             ".go", ".php", ".sql", ".rules", ".json", ".html", ".toml", ".yaml", ".yml"}
SOURCE_EXTS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".py", ".rb",
               ".go", ".php", ".sql", ".rules", ".html", ".css"}
MAX_FILE_BYTES = 1_000_000


def iter_files(root, exts: set[str] | None = None) -> list[Path]:
    """Project files worth reading, sorted: skips dependency/build folders,
    symlinks, nested git checkouts (worktrees and clones inside the project — a
    subfolder with its own `.git` — are copies of other code, not this project)
    and files larger than MAX_FILE_BYTES."""
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(
            d for d in dirnames
            if d not in SKIP_DIRS
            and not os.path.islink(os.path.join(dirpath, d))
            and not os.path.lexists(os.path.join(dirpath, d, ".git")))
        for name in sorted(filenames):
            p = Path(dirpath) / name
            if exts is not None and p.suffix.lower() not in exts:
                continue
            try:
                if p.is_symlink() or p.stat().st_size > MAX_FILE_BYTES:
                    continue
            except OSError:
                continue
            out.append(p)
    return out


def read_text(path) -> str:
    return Path(path).read_text(encoding="utf-8", errors="replace")


def git_ls_files(root) -> list[str] | None:
    """Tracked files relative to `root`, or None when `root` is not in a git repo."""
    try:
        res = subprocess.run(["git", "-C", str(root), "ls-files", "-z"],
                             capture_output=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if res.returncode != 0:
        return None
    return [p for p in res.stdout.decode("utf-8", "replace").split("\0") if p]


def git_ignored(root, rel_paths: Iterable[str]) -> set[str]:
    """The paths (relative to `root`) git ignores — .gitignore, .git/info/exclude and the
    global excludes; tracked files never count. Empty when `root` is not in a git repo:
    the caller then keeps everything, which is the pre-git behaviour."""
    rel_paths = list(rel_paths)
    if not rel_paths:
        return set()
    try:
        res = subprocess.run(["git", "-C", str(root), "check-ignore", "-z", "--stdin"],
                             input="\0".join(rel_paths).encode("utf-8") + b"\0",
                             capture_output=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired):
        return set()
    # 0 = some ignored, 1 = none ignored, 128 = not a repo / fatal
    if res.returncode not in (0, 1):
        return set()
    return {p for p in res.stdout.decode("utf-8", "replace").split("\0") if p}


# A tool output that is an error even though the tool did not flag it.
ERROR_LINE = re.compile(
    r"(?im)^\s*(?:error|fatal|uncaught|unhandled)\b"
    r"|permission denied|violates row[- ]level security|failed to compile"
    r"|traceback \(most recent call last\)|npm err!"
    r"|status(?: code)?:? ?(?:401|403|500)\b|blocked by cors|cors policy"
)

# A user message reporting that something is broken.
USER_ERROR = re.compile(
    r"报错|错误|出错|还是不行|不行了|不工作|失败了|白屏|打不开"
    r"|still (?:not working|broken|failing)|doesn'?t work|not working|it'?s broken"
    r"|getting (?:an? )?error|\berror:|exception|traceback|blocked by|\bcors\b",
    re.I,
)

_CJK = re.compile(r"[぀-ヿ㐀-鿿가-힯]")
_LATIN = re.compile(r"[A-Za-z]")


def detect_lang(texts: Iterable[str]) -> str:
    """'zh' when at least as many user messages are mainly Chinese as English.
    A message counts as Chinese when 3 × its CJK characters ≥ its Latin letters. A message too short to tell
    ("push", "ok", "继续" — under 3 CJK characters and under 12 letters) does not vote: a Chinese-speaking user
    types "push" a lot, and those votes once turned a mostly Chinese project's report English."""
    zh = en = 0
    for text in texts:
        cjk, latin = len(_CJK.findall(text)), len(_LATIN.findall(text))
        if cjk < 3 and latin < 12:
            continue
        if cjk and cjk * 3 >= latin:
            zh += 1
        elif latin:
            en += 1
    return "zh" if zh and zh >= en else "en"
