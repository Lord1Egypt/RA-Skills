# vibe-ledger Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the vibe-ledger skill: read the Claude Code / Codex conversations that built a project plus its current code, turn the promises in them into a verified ledger, and render an offline HTML report with four diagrams.

**Architecture:** A pipeline of small stdlib-only Python scripts under `scripts/`, driven by one CLI (`scripts/vl.py`). Scripts find candidates, run deterministic probes and verify evidence; the agent (guided by `SKILL.md` + `references/`) writes `ledger.json`; the renderer draws only what passed verification.

**Tech Stack:** Python ≥ 3.11 standard library only at runtime; pytest for tests; headless Chrome (optional) for screenshots.

**Spec:** `docs/superpowers/specs/2026-10-09-vibe-ledger-design.md` — read it before starting any task.

## Global Constraints

- Runtime code uses the Python standard library only (Python ≥ 3.11). No f-string nests the same quote character inside `{}` (that needs 3.12).
- Nothing is sent over the network. Nothing is written inside the user's project folder.
- Intermediate files live in `~/.vibe-ledger/projects/<project-id>/runs/<timestamp>/` (overridable with `VIBE_LEDGER_HOME`). Project id = `slug(folder name)-<first 8 hex of SHA-1 of the resolved absolute path>`.
- Reports go to `~/Desktop`, else `~/Downloads`, else the run folder (`VIBE_LEDGER_OUT_DIR` or `--out-dir` override).
- Secrets are masked (prefix + `…` + last 4) in the digest, the archive and the report; the renderer refuses to write a report that still contains one.
- `~/.claude/settings.json` is changed only by `vl.py retention --set`, which SKILL.md tells the agent to run only after the user agrees.
- Constants (copied from the spec): reading-pack limit **120,000** characters; compromise window **20** digest records or the end of the next turn, whichever is earlier; tool-error text truncated to **2,000** characters; edit summaries to **1,500**; code-snippet tolerance **±3** lines; map shows at most **12** nodes; high-entropy secret = length ≥ **20** and Shannon entropy ≥ **3.5** bits/char.
- Five-question keys: `where_data`, `what_costs`, `who_can_see`, `what_breaks`, `open_debts`. Statuses: `kept`, `broken`, `partial`, `pending` (only for `deferred`), `unknown`. Promise types: `user_requirement`, `ai_claim`, `deferred`. Access subjects: `anonymous`, `signed_in` (other signed-in users), `owner`.
- Every CLI step prints the exact next command (`NEXT:`), with paths quoted by `shlex.quote`, runnable as printed.
- Git: stage named paths only (never `git add -A` / `git add .`); never push.

## Review Focus

1. **Many large real logs** — a user with hundreds of MB of `~/.claude/projects` logs from other projects: `start` must not parse files that never mention the project folder name. Test: `test_prefilter_skips_unrelated_files` (Task 3).
2. **Project path with spaces and Chinese characters** (`~/我的 应用`) — ids, run folders and every printed `NEXT:` command must still work. Test: `test_start_prints_runnable_next_commands_for_unusual_path` (Task 13).
3. **Quotes and files that differ only in invisible ways** — CRLF line endings in the code, NFD vs NFC Unicode in a quote. Expected: they still verify. Tests: `test_code_evidence_with_crlf_file`, `test_quote_matches_across_unicode_normalisation` (Task 8).
4. **Project that is not a git repository** — probes and the "unattributed files" list must degrade (no crash; fall back to walking files). Tests: `test_git_ls_files_returns_none_outside_git` (Task 1), `test_secrets_probe_without_git` (Task 5), `test_start_without_git` (Task 13).
5. **Symlinked paths** (`/tmp` vs `/private/tmp` on macOS) — a session recorded under the symlinked path still belongs to the project. Tests: `test_is_within_follows_symlinks` (Task 1), `test_symlinked_project_path` (Task 3).

## How this plan reads the spec

- The one-line answer under each of the five questions (spec §11.1 "两三句结论") is computed from verified data by `render.summaries`, not written by the model, so it cannot state anything unverified. The model's plain-language voice lives in each promise's `verdict_plain`, shown on the cards right below.
- Diagram E is its own developer-view section. The ledger format (spec §9.1) does not link a path to a promise, so ledger rows do not embed it.
- Probe messages are short English technical sentences; they appear only inside evidence. Everything a user reads first comes from `i18n.py` (zh/en) or from the model in the run's language.
- Run-folder contents and the `run.json` manifest are defined in Task 13.

## File Structure

```
vibe-ledger/
  SKILL.md                          agent-facing workflow (Task 14)
  README.md, LICENSE                (Task 16)
  pyproject.toml, .gitignore        pytest config only (Task 1)
  .claude-plugin/plugin.json        (Task 16)
  .claude-plugin/marketplace.json   (Task 16)
  references/
    extraction-guide.md  ledger-schema.md  five-questions.md  probes.md  candidates.md   (Task 14)
  scripts/
    common.py            paths, JSONL, normalisation, file walking, shared regexes, language detection, version (Task 1)
    redact.py            secret masking and detection (Task 1)
    sessions.py          Claude Code + Codex log parsing, project ownership, archive (Tasks 2–3)
    candidates.py        compromise / deferral / claim candidates, code TODOs, reading packs (Task 4)
    probes/__init__.py   Finding, stack detection, run_all (Task 5)
    probes/util.py       shared probe helpers (Task 5)
    probes/secrets_exposed.py  probes/supabase_rls.py   (Task 5)
    probes/firebase_rules.py   probes/cors_wildcard.py  probes/paid_api_unauthed.py  probes/routes.py  (Task 6)
    ledger.py            ledger constants, validate, merge (Task 7)
    verify.py            evidence checks and ledger verification (Tasks 8–9)
    ledger_report/__init__.py  bits.py  i18n.py  assets/report.css  assets/report.js  (Task 10)
    ledger_report/map_svg.py  ledger_report/access_html.py   (Task 11)
    ledger_report/timeline_svg.py  ledger_report/paths_svg.py (Task 12)
    render.py            page assembly, summaries, coverage, delivery (Task 10)
    shot.py              headless Chrome screenshots (Task 13)
    vl.py                CLI: start / merge / check / render / shot / retention (Task 13)
  tests/
    conftest.py  helpers/__init__.py  helpers/fake_logs.py
    test_common.py  test_redact.py  test_sessions_claude.py  test_sessions_codex.py  test_collect.py
    test_candidates.py  test_probes_stack_secrets_supabase.py  test_probes_other.py
    test_ledger.py  test_verify_evidence.py  test_verify_ledger.py
    test_render_page.py  test_render_map_access.py  test_render_timeline_paths.py
    test_cli.py  test_docs.py  test_packaging.py  test_e2e_deterministic.py
    fixtures/apps/{notes-supabase,habits-firebase,chat-express,clean-todos,flask-notes}/...
    fixtures/answers/*.json
    e2e/__init__.py  e2e/scenarios.py  e2e/prepare.py  e2e/score.py
```

Digest record (produced by `sessions.py`, read by everything after it) — a dict with keys:
`id` (str), `session` (thread id, str), `agent` (`"claude-code"`|`"codex"`), `ts` (ISO string from the log), `role` (`"user"`|`"assistant"`|`"agent"`|`"tool"`), `kind` (`"text"`|`"edit"`|`"command"`|`"error"`), `text` (str, masked), `files` (list of absolute path strings), `cwd` (str), `sidechain` (bool), `seq` (int, order in the thread), `turn` (int, user-turn number), `in_project` (True), and for edits optional `old` / `new` (str, masked, ≤ 1,500 chars).

---

### Task 1: Scaffold, `common.py`, `redact.py`

**Files:**
- Create: `pyproject.toml`, `.gitignore`, `tests/conftest.py`, `tests/helpers/__init__.py`
- Create: `scripts/common.py`, `scripts/redact.py`
- Test: `tests/test_common.py`, `tests/test_redact.py`

**Interfaces:**
- Consumes: nothing.
- Produces:
  - `common.__version__ = "0.1.0"`
  - `common.norm_ws(text: str) -> str`, `common.slugify(name: str) -> str`, `common.project_id(root) -> str`, `common.home_dir() -> Path`, `common.project_workdir(root) -> Path`
  - `common.is_within(path, root) -> bool`, `common.rel(path, root) -> str` (POSIX, relative to resolved root)
  - `common.read_jsonl(path) -> Iterator[tuple[int, dict | None]]`, `common.write_json(path, obj)`, `common.load_json(path)`, `common.write_jsonl(path, rows)`
  - `common.SKIP_DIRS`, `common.CODE_EXTS`, `common.SOURCE_EXTS`, `common.MAX_FILE_BYTES`, `common.iter_files(root, exts=None) -> list[Path]`, `common.read_text(path) -> str`, `common.git_ls_files(root) -> list[str] | None`
  - `common.ERROR_LINE`, `common.USER_ERROR` (compiled regexes), `common.detect_lang(texts) -> "zh" | "en"`
  - `redact.redact(text: str) -> str`, `redact.find_secrets(text: str) -> list[tuple[int, int, str]]`, `redact.shannon_entropy(s: str) -> float`, `redact.ELLIPSIS = "…"`

- [ ] **Step 1: Write the scaffold files**

`pyproject.toml`:
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q -p no:cacheprovider"
```

`.gitignore`:
```
__pycache__/
*.pyc
.pytest_cache/
```

`tests/conftest.py`:
```python
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))
```

`tests/helpers/__init__.py`: empty file.

- [ ] **Step 2: Write the failing tests**

`tests/test_common.py`:
```python
from pathlib import Path

import common


def test_norm_ws_collapses_and_nfc():
    assert common.norm_ws("  a\n\t b  ") == "a b"
    assert common.norm_ws("é") == "é"
    assert common.norm_ws(None) == ""


def test_project_id_is_stable_and_path_specific(tmp_path):
    a = tmp_path / "我的 应用"
    a.mkdir()
    b = tmp_path / "other" / "我的 应用"
    b.mkdir(parents=True)
    assert common.project_id(a) == common.project_id(a)
    assert common.project_id(a) != common.project_id(b)
    assert common.project_id(a).startswith("我的-应用-")


def test_workdir_honours_env(tmp_path, monkeypatch):
    monkeypatch.setenv("VIBE_LEDGER_HOME", str(tmp_path / "home"))
    app = tmp_path / "app"
    app.mkdir()
    assert common.project_workdir(app) == tmp_path / "home" / "projects" / common.project_id(app)


def test_is_within(tmp_path):
    root = tmp_path / "app"
    (root / "src").mkdir(parents=True)
    assert common.is_within(root / "src" / "x.ts", root)
    assert common.is_within(root, root)
    assert not common.is_within(tmp_path / "app2" / "x.ts", root)
    assert not common.is_within(tmp_path, root)
    assert not common.is_within("", root)


def test_is_within_follows_symlinks(tmp_path):
    real = tmp_path / "real"
    real.mkdir()
    link = tmp_path / "link"
    link.symlink_to(real)
    assert common.is_within(link / "a.ts", real)
    assert common.is_within(real / "a.ts", link)


def test_rel_is_posix_relative(tmp_path):
    (tmp_path / "a" / "b").mkdir(parents=True)
    assert common.rel(tmp_path / "a" / "b" / "c.ts", tmp_path) == "a/b/c.ts"


def test_read_jsonl_reports_bad_lines(tmp_path):
    f = tmp_path / "x.jsonl"
    f.write_text('{"a": 1}\nnot json\n\n[1, 2]\n{"b": 2}\n', encoding="utf-8")
    assert list(common.read_jsonl(f)) == [(1, {"a": 1}), (2, None), (4, None), (5, {"b": 2})]


def test_iter_files_skips_dependency_dirs_and_big_files(tmp_path):
    (tmp_path / "node_modules" / "x").mkdir(parents=True)
    (tmp_path / "node_modules" / "x" / "a.js").write_text("x")
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "b.ts").write_text("ok")
    (tmp_path / "src" / "big.js").write_bytes(b"a" * (common.MAX_FILE_BYTES + 1))
    assert [p.name for p in common.iter_files(tmp_path, {".js", ".ts"})] == ["b.ts"]


def test_detect_lang_votes_per_message():
    zh = ["帮我做一个记账应用", "只有我自己能看到",
          "Error: permission denied for table notes at line 3 of the migration"]
    assert common.detect_lang(zh) == "zh"
    assert common.detect_lang(["make me a habit tracker", "only I should see my data"]) == "en"
    assert common.detect_lang([]) == "en"


def test_git_ls_files_returns_none_outside_git(tmp_path):
    assert common.git_ls_files(tmp_path) is None


def test_error_patterns():
    assert common.ERROR_LINE.search("ready\nError: permission denied for table notes")
    assert common.ERROR_LINE.search("new row violates row-level security policy")
    assert not common.ERROR_LINE.search("compiled successfully in 2s")
    assert common.USER_ERROR.search("保存的时候报错了")
    assert common.USER_ERROR.search("Access to fetch has been blocked by CORS policy")
    assert not common.USER_ERROR.search("make the button blue")
```

`tests/test_redact.py`:
```python
import base64
import json

import redact

# Built by concatenation so this file never contains a contiguous secret.
OPENAI = "sk-proj-" + "Ab3dE5fG7hJ9kL1mN3pQ5rS7tU9vW1xY"
ANTHROPIC = "sk-ant-api03-" + "Zz9Yy8Xx7Ww6Vv5Uu4Tt3Ss2Rr1Qq0Pp"
STRIPE = "sk_live_" + "51Hq8kLmNoPqRsTuVwXy"
AWS = "AKIA" + "IOSFODNN7EXAMPLE"


def jwt(payload: dict) -> str:
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    return enc({"alg": "HS256", "typ": "JWT"}) + "." + enc(payload) + "." + "s1gnatureS1gnature"


def test_prefixed_secrets_are_masked_keeping_prefix_and_last4():
    for secret, prefix in ((OPENAI, "sk-proj-"), (ANTHROPIC, "sk-ant-"), (STRIPE, "sk_live_"), (AWS, "AKIA")):
        out = redact.redact(f"key is {secret} ok")
        assert secret not in out
        assert f"{prefix}…{secret[-4:]}" in out


def test_jwt_is_masked():
    token = jwt({"role": "service_role"})
    out = redact.redact(f"SUPABASE={token}")
    assert token not in out and "eyJ…" in out


def test_high_entropy_assignment_is_masked_low_entropy_is_not():
    assert "q8Zr2Lx9Vb4Nm7Kp3Wd6Ty1" not in redact.redact('API_TOKEN="q8Zr2Lx9Vb4Nm7Kp3Wd6Ty1"')
    plain = "PASSWORD_HINT=aaaaaaaaaaaaaaaaaaaaaaaa"
    assert redact.redact(plain) == plain


def test_private_key_block_is_replaced():
    block = "-----BEGIN RSA " + "PRIVATE KEY-----\nMIIBOgIBAAJBAKj34GkxFhD90vcNLYLInFEX6Ppy1tPf9Cnzj4p4WGeKLs1Pt8Qu\n-----END RSA " + "PRIVATE KEY-----"  # built in pieces: no key-shaped literal in the repo
    assert redact.redact(block) == "[PRIVATE KEY REDACTED]"


def test_masking_is_idempotent_and_leaves_nothing_detectable():
    text = f"{OPENAI} {ANTHROPIC} {STRIPE} {AWS} {jwt({'role': 'anon'})} API_TOKEN=q8Zr2Lx9Vb4Nm7Kp3Wd6Ty1"
    once = redact.redact(text)
    assert redact.redact(once) == once
    assert redact.find_secrets(once) == []
    assert len(redact.find_secrets(text)) >= 6


def test_prose_is_untouched():
    s = "skip the sk- prefix discussion; AKIA alone is fine"
    assert redact.redact(s) == s


def test_entropy():
    assert redact.shannon_entropy("") == 0.0
    assert redact.shannon_entropy("aaaa") == 0.0
    assert redact.shannon_entropy("abcd") == 2.0
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_common.py tests/test_redact.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'common'` / `'redact'`.

- [ ] **Step 4: Write `scripts/common.py`**

```python
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

__version__ = "0.1.0"

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
             ".nuxt", "vendor", ".expo", ".idea", ".vscode"}
CODE_EXTS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".py", ".rb",
             ".go", ".php", ".sql", ".rules", ".json", ".html", ".toml", ".yaml", ".yml"}
SOURCE_EXTS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".py", ".rb",
               ".go", ".php", ".sql", ".rules", ".html", ".css"}
MAX_FILE_BYTES = 1_000_000


def iter_files(root, exts: set[str] | None = None) -> list[Path]:
    """Project files worth reading, sorted: skips dependency/build folders,
    symlinks and files larger than MAX_FILE_BYTES."""
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames
                             if d not in SKIP_DIRS and not os.path.islink(os.path.join(dirpath, d)))
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
    A message counts as Chinese when 3 × its CJK characters ≥ its Latin letters."""
    zh = en = 0
    for text in texts:
        cjk, latin = len(_CJK.findall(text)), len(_LATIN.findall(text))
        if cjk and cjk * 3 >= latin:
            zh += 1
        elif latin:
            en += 1
    return "zh" if zh and zh >= en else "en"
```

- [ ] **Step 5: Write `scripts/redact.py`**

```python
"""Mask secrets before anything is stored or shown.

A masked secret keeps a recognisable prefix and its last four characters
(`sk-proj-…wXyZ`), so the report can say *which* key leaked without leaking
it again. Masking is idempotent: masked text never matches a pattern again."""
from __future__ import annotations

import math
import re
from collections import Counter

ELLIPSIS = "…"
MIN_ENTROPY = 3.5
MIN_LEN = 20

_PATTERNS: list[tuple[str, re.Pattern]] = [
    ("private_key", re.compile(
        r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.S)),
    ("anthropic", re.compile(r"(?P<p>sk-ant-)[A-Za-z0-9_\-]{20,}")),
    ("openai", re.compile(r"(?P<p>sk-(?:proj-)?)(?!ant-)[A-Za-z0-9_\-]{20,}")),
    ("stripe", re.compile(r"(?P<p>(?:sk|rk|pk)_(?:live|test)_)[A-Za-z0-9]{10,}")),
    ("aws", re.compile(r"(?P<p>AKIA)[0-9A-Z]{16}")),
    ("github", re.compile(r"(?P<p>ghp_|gho_|ghs_|github_pat_)[A-Za-z0-9_]{20,}")),
    ("slack", re.compile(r"(?P<p>xox[abposr]-)[A-Za-z0-9\-]{10,}")),
    ("jwt", re.compile(r"(?P<p>eyJ)[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}")),
]
_ASSIGN = re.compile(
    r"(?P<name>\b[A-Za-z_][A-Za-z0-9_]*(?:key|secret|token|password|passwd)[A-Za-z0-9_]*)"
    r"(?P<sep>\s*[:=]\s*[\"']?)(?P<val>[A-Za-z0-9+/_\-.=]{" + str(MIN_LEN) + r",})",
    re.I,
)


def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    n = len(s)
    return -sum(c / n * math.log2(c / n) for c in Counter(s).values())


def _mask(kind: str, m: re.Match) -> str:
    if kind == "private_key":
        return "[PRIVATE KEY REDACTED]"
    return f"{m.group('p')}{ELLIPSIS}{m.group(0)[-4:]}"


def find_secrets(text: str) -> list[tuple[int, int, str]]:
    """(start, end, kind) for every unmasked secret in `text`."""
    spans = []
    for kind, rx in _PATTERNS:
        spans += [(m.start(), m.end(), kind) for m in rx.finditer(text or "")]
    for m in _ASSIGN.finditer(text or ""):
        if shannon_entropy(m.group("val")) >= MIN_ENTROPY:
            spans.append((m.start("val"), m.end("val"), "assignment"))
    return sorted(set(spans))


def redact(text: str) -> str:
    if not text:
        return text or ""
    for kind, rx in _PATTERNS:
        text = rx.sub(lambda m, k=kind: _mask(k, m), text)

    def _assign(m: re.Match) -> str:
        val = m.group("val")
        if shannon_entropy(val) < MIN_ENTROPY:
            return m.group(0)
        return f"{m.group('name')}{m.group('sep')}{ELLIPSIS}{val[-4:]}"

    return _ASSIGN.sub(_assign, text)
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_common.py tests/test_redact.py`
Expected: PASS (all tests).

- [ ] **Step 7: Commit**

```bash
git add pyproject.toml .gitignore tests/conftest.py tests/helpers/__init__.py scripts/common.py scripts/redact.py tests/test_common.py tests/test_redact.py
git commit -m "feat: scaffold with shared helpers and secret masking"
```

---
### Task 2: Claude Code log parsing

**Files:**
- Create: `tests/helpers/fake_logs.py`
- Create: `scripts/sessions.py`
- Test: `tests/test_sessions_claude.py`

**Interfaces:**
- Consumes: `common.read_jsonl`, `common.ERROR_LINE` (Task 1).
- Produces:
  - `sessions.Stats` dataclass with fields `files_scanned, files_parsed, files_matched, threads, records, bad_lines, compact_summaries, skipped_sessions, archived_threads` (int), `ignored_types, by_agent` (Counter), `earliest, latest` (str), `warnings` (list[str]) and `to_dict() -> dict`.
  - `sessions.parse_claude_file(path, stats) -> list[dict]` — digest records **without** `seq`, `turn`, `in_project` (added in Task 3).
  - `sessions.TOOL_TEXT_LIMIT = 2000`, `sessions.EDIT_LIMIT = 1500`.
  - Test helper `helpers.fake_logs.ClaudeSession(cwd, session_id="sess-1", sidechain=False)` with methods `user(text, **extra) -> uuid`, `assistant_text(text) -> uuid`, `tool(name, inp, result, is_error=False) -> (tool_use_uuid, result_uuid)`, `edit(path, old, new)`, `write(path, content)`, `bash(cmd, output, is_error=False)`, `compact_summary(text)`, `raw(obj)`, `set_cwd(cwd)`, `save(projects_dir, agent_id=None) -> Path`.

Real Claude Code records (observed in Claude Code 2.x logs): one JSON object per line with `type` (`user`, `assistant`, and many bookkeeping types such as `attachment`, `file-history-snapshot`, `mode`), `uuid`, `sessionId`, `timestamp`, `cwd`, `isSidechain`, `message.content` (a string or a list of blocks: `text`, `tool_use` with `id/name/input`, `tool_result` with `tool_use_id/content/is_error`). Compaction summaries are `user` records with `isCompactSummary: true`. Command and notification wrappers are `user` strings starting with `<task-notification`, `<local-command-`, `<command-name>` etc.; skill injections carry `isMeta: true`. Sub-agent transcripts live at `projects/<dir>/<sessionId>/subagents/agent-<id>.jsonl`.

- [ ] **Step 1: Write the test helper**

`tests/helpers/fake_logs.py`:
```python
"""Builders for synthetic Claude Code and Codex session logs.

They mirror the record shapes seen in real logs (Claude Code 2.x,
Codex CLI 0.122–0.154); every value is invented."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

T0 = datetime(2026, 9, 12, 9, 0, tzinfo=timezone.utc)


def ts(minutes: int) -> str:
    return (T0 + timedelta(minutes=minutes)).isoformat().replace("+00:00", "Z")


class ClaudeSession:
    def __init__(self, cwd, session_id: str = "sess-1", sidechain: bool = False, start: int = 0):
        self.cwd, self.sid, self.sidechain = str(cwd), session_id, sidechain
        self.lines: list[dict] = []
        self.n = start

    def _base(self, typ: str) -> dict:
        self.n += 1
        return {"type": typ, "uuid": f"{self.sid}-u{self.n}", "parentUuid": None,
                "sessionId": self.sid, "timestamp": ts(self.n), "cwd": self.cwd,
                "isSidechain": self.sidechain, "userType": "external", "version": "2.1.0"}

    def user(self, text: str, **extra) -> str:
        d = self._base("user")
        d["message"] = {"role": "user", "content": text}
        d.update(extra)
        self.lines.append(d)
        return d["uuid"]

    def assistant_text(self, text: str) -> str:
        d = self._base("assistant")
        d["message"] = {"role": "assistant", "content": [{"type": "text", "text": text}]}
        self.lines.append(d)
        return d["uuid"]

    def tool(self, name: str, inp: dict, result: str, is_error: bool = False) -> tuple[str, str]:
        a = self._base("assistant")
        tool_id = f"toolu_{a['uuid']}"
        a["message"] = {"role": "assistant",
                        "content": [{"type": "tool_use", "id": tool_id, "name": name, "input": inp}]}
        self.lines.append(a)
        r = self._base("user")
        r["message"] = {"role": "user", "content": [
            {"type": "tool_result", "tool_use_id": tool_id, "content": result, "is_error": is_error}]}
        self.lines.append(r)
        return a["uuid"], r["uuid"]

    def edit(self, path, old: str, new: str) -> tuple[str, str]:
        return self.tool("Edit", {"file_path": str(path), "old_string": old, "new_string": new},
                         "The file has been updated.")

    def write(self, path, content: str) -> tuple[str, str]:
        return self.tool("Write", {"file_path": str(path), "content": content}, "File created successfully")

    def bash(self, cmd: str, output: str, is_error: bool = False) -> tuple[str, str]:
        return self.tool("Bash", {"command": cmd, "description": "run"}, output, is_error)

    def compact_summary(self, text: str) -> None:
        d = self._base("user")
        d["isCompactSummary"] = True
        d["message"] = {"role": "user", "content": text}
        self.lines.append(d)

    def raw(self, obj: dict) -> None:
        self.lines.append(obj)

    def set_cwd(self, cwd) -> None:
        self.cwd = str(cwd)

    def save(self, projects_dir, agent_id: str | None = None) -> Path:
        folder = Path(projects_dir) / ("-" + self.cwd.strip("/").replace("/", "-").replace(" ", "-"))
        path = (folder / self.sid / "subagents" / f"agent-{agent_id}.jsonl") if agent_id \
            else folder / f"{self.sid}.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in self.lines),
                        encoding="utf-8")
        return path
```

- [ ] **Step 2: Write the failing tests**

`tests/test_sessions_claude.py`:
```python
import sessions
from helpers.fake_logs import ClaudeSession


def parse(sess, tmp_path, **save_kw):
    f = sess.save(tmp_path / "projects", **save_kw)
    stats = sessions.Stats()
    return sessions.parse_claude_file(f, stats), stats


def test_user_assistant_edit_command_and_error(tmp_path):
    app = tmp_path / "app"
    s = ClaudeSession(app)
    s.user("只有我自己能看到我的笔记")
    s.assistant_text("好的，我会开启 RLS。")
    s.edit(app / "supabase/migrations/001.sql", "enable row level security", "disable row level security")
    s.bash("npx supabase db push", "Error: new row violates row-level security policy", is_error=True)
    s.bash("ls", "a.ts\nb.ts")
    s.tool("Read", {"file_path": str(app / "a.ts")}, "contents")
    recs, _ = parse(s, tmp_path)
    assert [(r["role"], r["kind"]) for r in recs] == [
        ("user", "text"), ("assistant", "text"), ("assistant", "edit"),
        ("assistant", "command"), ("tool", "error"), ("assistant", "command")]
    edit = recs[2]
    assert edit["old"] == "enable row level security"
    assert edit["new"] == "disable row level security"
    assert edit["files"] == [str(app / "supabase/migrations/001.sql")]
    assert recs[0]["agent"] == "claude-code" and recs[0]["session"] == "sess-1"
    assert recs[0]["ts"].startswith("2026-09-12T") and recs[0]["cwd"] == str(app)
    assert recs[0]["id"] == "sess-1-u1"


def test_bash_output_with_error_text_counts_as_error_without_flag(tmp_path):
    s = ClaudeSession(tmp_path / "app")
    s.bash("npm run dev", "ready\nError: permission denied for table notes")
    recs, _ = parse(s, tmp_path)
    assert [r["kind"] for r in recs] == ["command", "error"]


def test_error_text_is_truncated(tmp_path):
    s = ClaudeSession(tmp_path / "app")
    s.bash("x", "E" * 5000, is_error=True)
    recs, _ = parse(s, tmp_path)
    assert len(recs[1]["text"]) == sessions.TOOL_TEXT_LIMIT


def test_write_and_multiedit_are_edits(tmp_path):
    app = tmp_path / "app"
    s = ClaudeSession(app)
    s.write(app / "a.ts", "export const a = 1;")
    s.tool("MultiEdit", {"file_path": str(app / "b.ts"),
                         "edits": [{"old_string": "x", "new_string": "y"},
                                   {"old_string": "p", "new_string": "q"}]}, "ok")
    recs, _ = parse(s, tmp_path)
    assert [r["kind"] for r in recs] == ["edit", "edit"]
    assert recs[0]["new"] == "export const a = 1;" and recs[0]["old"] == ""
    assert recs[0]["text"].startswith("WRITE ")
    assert recs[1]["old"] == "x\np" and recs[1]["new"] == "y\nq"


def test_wrappers_meta_and_compact_summaries_are_not_user_words(tmp_path):
    s = ClaudeSession(tmp_path / "app")
    s.user("<task-notification>done</task-notification>")
    s.user("<command-name>/model</command-name>")
    s.user("skill text", isMeta=True)
    s.compact_summary("This session is being continued from a previous conversation...")
    s.user("real question")
    recs, stats = parse(s, tmp_path)
    assert [r["text"] for r in recs] == ["real question"]
    assert stats.compact_summaries == 1


def test_sidechain_prompts_are_agent_not_user(tmp_path):
    s = ClaudeSession(tmp_path / "app", sidechain=True)
    s.user("You are a reviewer. Check the code.")
    recs, _ = parse(s, tmp_path)
    assert recs[0]["role"] == "agent" and recs[0]["sidechain"] is True


def test_subagent_file_gets_its_own_thread(tmp_path):
    s = ClaudeSession(tmp_path / "app", session_id="sess-9")
    s.user("Review this")
    recs, _ = parse(s, tmp_path, agent_id="abc")
    assert recs[0]["session"] == "sess-9/agent-abc"
    assert recs[0]["role"] == "agent"


def test_bad_lines_and_other_types_are_counted(tmp_path):
    s = ClaudeSession(tmp_path / "app")
    s.raw({"type": "file-history-snapshot", "snapshot": {}})
    s.user("hi")
    f = s.save(tmp_path / "projects")
    with open(f, "a", encoding="utf-8") as fh:
        fh.write("{broken\n")
    stats = sessions.Stats()
    recs = sessions.parse_claude_file(f, stats)
    assert len(recs) == 1 and stats.bad_lines == 1
    assert stats.ignored_types["claude:file-history-snapshot"] == 1


def test_multi_block_message_gets_suffixed_ids(tmp_path):
    s = ClaudeSession(tmp_path / "app")
    s.raw({"type": "assistant", "uuid": "m1", "sessionId": "sess-1", "timestamp": "2026-09-12T09:00:00Z",
           "cwd": str(tmp_path / "app"),
           "message": {"role": "assistant", "content": [{"type": "text", "text": "one"},
                                                        {"type": "text", "text": "two"}]}})
    recs, _ = parse(s, tmp_path)
    assert [r["id"] for r in recs] == ["m1", "m1#1"]


def test_stats_to_dict_is_json_ready():
    st = sessions.Stats()
    st.ignored_types["claude:x"] += 2
    d = st.to_dict()
    assert d["ignored_types"] == {"claude:x": 2} and isinstance(d["by_agent"], dict)
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_sessions_claude.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'sessions'`.

- [ ] **Step 4: Write `scripts/sessions.py` (Claude Code part)**

```python
"""Find the Claude Code and Codex sessions that belong to a project and turn
them into a compact, masked digest the rest of the pipeline reads.

The model never reads raw logs: only the digest, through the reading packs."""
from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

from common import ERROR_LINE, read_jsonl

TOOL_TEXT_LIMIT = 2000
EDIT_LIMIT = 1500
EDIT_TOOLS = {"Edit", "MultiEdit", "Write", "NotebookEdit"}
COMMAND_TOOLS = {"Bash"}
WRAPPER_PREFIXES = ("<task-notification", "<local-command-", "<command-name>", "<command-message>",
                    "<command-args>", "<system-reminder>", "<bash-input>", "<bash-stdout>",
                    "<bash-stderr>")


@dataclass
class Stats:
    files_scanned: int = 0
    files_parsed: int = 0
    files_matched: int = 0
    threads: int = 0
    records: int = 0
    bad_lines: int = 0
    compact_summaries: int = 0
    skipped_sessions: int = 0
    archived_threads: int = 0
    ignored_types: Counter = field(default_factory=Counter)
    by_agent: Counter = field(default_factory=Counter)
    earliest: str = ""
    latest: str = ""
    warnings: list = field(default_factory=list)

    def to_dict(self) -> dict:
        d = dict(self.__dict__)
        d["ignored_types"] = dict(self.ignored_types)
        d["by_agent"] = dict(self.by_agent)
        d["warnings"] = list(self.warnings)
        return d


def _rec(role: str, kind: str, text: str, files=(), old: str | None = None, new: str | None = None) -> dict:
    r = {"role": role, "kind": kind, "text": text, "files": [f for f in files if f]}
    if old is not None:
        r["old"] = old[:EDIT_LIMIT]
    if new is not None:
        r["new"] = new[:EDIT_LIMIT]
    return r


def _content_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(b.get("text", "") for b in content
                         if isinstance(b, dict) and b.get("type") == "text")
    return ""


def _claude_edit(name: str, inp: dict) -> dict:
    path = inp.get("file_path") or inp.get("notebook_path") or ""
    if name == "Write":
        new = inp.get("content", "")
        return _rec("assistant", "edit", f"WRITE {path}\n{new}"[:EDIT_LIMIT], [path], old="", new=new)
    if name == "MultiEdit":
        edits = inp.get("edits") or []
        old = "\n".join(e.get("old_string", "") for e in edits)
        new = "\n".join(e.get("new_string", "") for e in edits)
    elif name == "NotebookEdit":
        old, new = "", inp.get("new_source", "")
    else:
        old, new = inp.get("old_string", ""), inp.get("new_string", "")
    text = f"EDIT {path}\n--- before\n{old}\n+++ after\n{new}"
    return _rec("assistant", "edit", text[:EDIT_LIMIT], [path], old=old, new=new)


def _claude_blocks(obj: dict, tool_names: dict) -> list[dict]:
    typ = obj.get("type")
    content = (obj.get("message") or {}).get("content")
    if isinstance(content, str):
        blocks = [{"type": "text", "text": content}]
    else:
        blocks = [b for b in (content or []) if isinstance(b, dict)]
    out = []
    for b in blocks:
        bt = b.get("type")
        if typ == "user" and bt == "text":
            text = b.get("text") or ""
            if obj.get("isMeta") or not text.strip() or text.lstrip().startswith(WRAPPER_PREFIXES):
                continue
            out.append(_rec("user", "text", text))
        elif typ == "user" and bt == "tool_result":
            text = _content_text(b.get("content"))
            name = tool_names.get(b.get("tool_use_id"), "")
            if b.get("is_error") or (name in COMMAND_TOOLS and ERROR_LINE.search(text)):
                out.append(_rec("tool", "error", text[:TOOL_TEXT_LIMIT]))
        elif typ == "assistant" and bt == "text" and (b.get("text") or "").strip():
            out.append(_rec("assistant", "text", b["text"]))
        elif typ == "assistant" and bt == "tool_use":
            name, inp = b.get("name", ""), b.get("input") or {}
            tool_names[b.get("id")] = name
            if name in EDIT_TOOLS:
                out.append(_claude_edit(name, inp))
            elif name in COMMAND_TOOLS:
                out.append(_rec("assistant", "command", str(inp.get("command", ""))[:TOOL_TEXT_LIMIT]))
    return out


def parse_claude_file(path, stats: Stats) -> list[dict]:
    """One Claude Code transcript file -> digest records of one thread."""
    path = Path(path)
    is_sub = "subagents" in path.parts
    records: list[dict] = []
    tool_names: dict = {}
    for lineno, obj in read_jsonl(path):
        if obj is None:
            stats.bad_lines += 1
            continue
        typ = obj.get("type")
        if typ not in ("user", "assistant"):
            stats.ignored_types[f"claude:{typ}"] += 1
            continue
        if obj.get("isCompactSummary"):
            stats.compact_summaries += 1
            continue
        session = obj.get("sessionId") or path.stem
        thread = f"{session}/{path.stem}" if is_sub else session
        uid = obj.get("uuid") or f"{path.name}:{lineno}"
        side = bool(obj.get("isSidechain")) or is_sub
        for k, r in enumerate(_claude_blocks(obj, tool_names)):
            if side and r["role"] == "user":
                r["role"] = "agent"
            r.update(id=uid if k == 0 else f"{uid}#{k}", session=thread, agent="claude-code",
                     ts=obj.get("timestamp", ""), cwd=obj.get("cwd") or "", sidechain=side)
            records.append(r)
    return records
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_sessions_claude.py`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add tests/helpers/fake_logs.py scripts/sessions.py tests/test_sessions_claude.py
git commit -m "feat: parse Claude Code transcripts into digest records"
```

---
### Task 3: Codex log parsing, project ownership, archive, `collect()`

**Files:**
- Modify: `tests/helpers/fake_logs.py` (append `CodexSession`)
- Modify: `scripts/sessions.py` (append the Codex parser and `collect`)
- Test: `tests/test_sessions_codex.py`, `tests/test_collect.py`

**Interfaces:**
- Consumes: `sessions.Stats`, `sessions._rec`, `sessions.parse_claude_file` (Task 2); `common.is_within`, `common.read_jsonl`, `common.write_jsonl`, `common.ERROR_LINE`; `redact.redact` (Task 1).
- Produces:
  - `sessions.parse_codex_file(path, stats) -> list[dict]`
  - `sessions.collect(root, claude_dir=None, codex_dir=None, archive_dir=None) -> tuple[list[dict], Stats]` — full digest records (with `seq`, `turn`, `in_project`), masked, only records that concern `root`, threads ordered by first timestamp.
  - `sessions.default_claude_dir() -> Path` (`$CLAUDE_CONFIG_DIR/projects`, else `~/.claude/projects`), `sessions.default_codex_dir() -> Path` (`$CODEX_HOME/sessions`, else `~/.codex/sessions`).
  - `sessions.load_archive(archive_dir) -> dict[str, list[dict]]`, `sessions.save_archive(archive_dir, threads: list[list[dict]])`.
  - Test helper `helpers.fake_logs.CodexSession(cwd, session_id="codex-1", source="cli", version="0.147.0")` with `user(text) -> lineno`, `agent(text)`, `update(path, diff)`, `add(path, content)`, `exec_end(cmd, output, exit_code=0, cwd=None)`, `item_command(cmd, output, exit_code=0, cwd=None)`, `item_filechange(changes)`, `apply_patch_call(patch)`, `function_exec(cmd, output)`, `custom_exec(cmd, output)`, `compacted()`, `set_cwd(cwd)`, `save(sessions_dir) -> Path`.

Real Codex records (observed across Codex CLI 0.122–0.154): `{"timestamp", "type", "payload"}`. `session_meta.payload` has `id`, `cwd`, `source` (a string such as `"cli"`/`"exec"`/`"vscode"`, or a dict `{"subagent": ...}`; `{"subagent": {"other": "guardian"}}` marks an auto-review session whose user message is *another* session's transcript — skip it). `turn_context.payload.cwd` updates the working folder. User and assistant words come from `event_msg` payloads of type `user_message` / `agent_message` (present in every version). File changes come from `event_msg/patch_apply_end` (`changes: {abs_path: {type: add|update|delete, content | unified_diff}}`), from `event_msg/item_completed` with `item.type == "FileChange"` (same `changes` shape, 0.147+), or — when neither exists — from `response_item/custom_tool_call` named `apply_patch` (`*** Add/Update/Delete File:` text, paths may be relative). Commands come from `item_completed` `CommandExecution` (`command` list, `cwd` as `file://…`, `exit_code` int or string, `aggregated_output`), else `event_msg/exec_command_end` (same fields), else `response_item/function_call` (`name: exec_command`, `arguments` JSON with `cmd`) or `custom_tool_call` named `exec` (JavaScript calling `tools.exec_command({"cmd": …})`), whose outputs (`function_call_output` / `custom_tool_call_output`) contain `Process exited with code N`. Compaction shows up as `compacted` or `event_msg/context_compacted`.

- [ ] **Step 1: Append the Codex builder to `tests/helpers/fake_logs.py`**

```python
class CodexSession:
    def __init__(self, cwd, session_id: str = "codex-1", source="cli", version: str = "0.147.0"):
        self.cwd, self.sid = str(cwd), session_id
        self.n = 0
        self.lines: list[dict] = [{"timestamp": ts(0), "type": "session_meta", "payload": {
            "id": session_id, "timestamp": ts(0), "cwd": self.cwd, "originator": "codex-tui",
            "cli_version": version, "source": source}}]

    def _ev(self, typ: str, payload: dict) -> int:
        self.n += 1
        self.lines.append({"timestamp": ts(self.n), "type": typ, "payload": payload})
        return len(self.lines)  # the 1-based line number in the saved file

    def set_cwd(self, cwd) -> None:
        self.cwd = str(cwd)

    def user(self, text: str) -> int:
        self._ev("turn_context", {"cwd": self.cwd})
        return self._ev("event_msg", {"type": "user_message", "message": text})

    def agent(self, text: str) -> int:
        return self._ev("event_msg", {"type": "agent_message", "message": text, "phase": "final_answer"})

    def update(self, path, diff: str) -> int:
        return self._ev("event_msg", {"type": "patch_apply_end", "call_id": f"c{self.n}", "success": True,
                                      "changes": {str(path): {"type": "update", "unified_diff": diff,
                                                              "move_path": None}}})

    def add(self, path, content: str) -> int:
        return self._ev("event_msg", {"type": "patch_apply_end", "call_id": f"c{self.n}", "success": True,
                                      "changes": {str(path): {"type": "add", "content": content}}})

    def exec_end(self, cmd: str, output: str, exit_code=0, cwd=None) -> int:
        return self._ev("event_msg", {"type": "exec_command_end", "call_id": f"c{self.n}",
                                      "command": ["/bin/zsh", "-lc", cmd], "cwd": str(cwd or self.cwd),
                                      "aggregated_output": output, "exit_code": exit_code,
                                      "status": "completed"})

    def item_command(self, cmd: str, output: str, exit_code=0, cwd=None) -> int:
        return self._ev("event_msg", {"type": "item_completed", "item": {
            "type": "CommandExecution", "id": f"exec-{self.n}", "command": ["/bin/zsh", "-lc", cmd],
            "cwd": "file://" + str(cwd or self.cwd), "aggregated_output": output,
            "exit_code": exit_code, "status": "completed" if str(exit_code) == "0" else "failed"}})

    def item_filechange(self, changes: dict) -> int:
        return self._ev("event_msg", {"type": "item_completed", "item": {
            "type": "FileChange", "id": f"fc-{self.n}", "changes": changes}})

    def apply_patch_call(self, patch: str) -> int:
        return self._ev("response_item", {"type": "custom_tool_call", "call_id": f"c{self.n}",
                                          "name": "apply_patch", "input": patch, "status": "completed"})

    def function_exec(self, cmd: str, output: str) -> int:
        call = f"call_{self.n}"
        self._ev("response_item", {"type": "function_call", "name": "exec_command", "call_id": call,
                                   "arguments": json.dumps({"cmd": cmd, "workdir": self.cwd})})
        return self._ev("response_item", {"type": "function_call_output", "call_id": call, "output": output})

    def custom_exec(self, cmd: str, output: str) -> int:
        call = f"call_{self.n}"
        js = "const r = await tools.exec_command(" + json.dumps({"cmd": cmd, "workdir": self.cwd}) + ");\ntext(r.output);\n"
        self._ev("response_item", {"type": "custom_tool_call", "name": "exec", "call_id": call, "input": js})
        return self._ev("response_item", {"type": "custom_tool_call_output", "call_id": call,
                                          "output": [{"type": "input_text", "text": output}]})

    def compacted(self) -> int:
        return self._ev("compacted", {"message": "summary"})

    def save(self, sessions_dir) -> Path:
        path = Path(sessions_dir) / "2026" / "09" / "12" / f"rollout-2026-09-12T09-00-00-{self.sid}.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in self.lines),
                        encoding="utf-8")
        return path
```

- [ ] **Step 2: Write the failing Codex tests**

`tests/test_sessions_codex.py`:
```python
import sessions
from helpers.fake_logs import CodexSession


def parse(sess, tmp_path):
    f = sess.save(tmp_path / "sessions")
    stats = sessions.Stats()
    return sessions.parse_codex_file(f, stats), stats, f


def test_text_patch_and_failed_exec(tmp_path):
    app = tmp_path / "app"
    s = CodexSession(app)
    ln_user = s.user("Each user should only see their own habits.")
    s.agent("For now I'm starting Firestore in test mode.")
    s.update(app / "firestore.rules", "@@ -1,2 +1,2 @@\n-allow read: if false;\n+allow read: if true;\n")
    s.add(app / "src/App.tsx", "export default function App() {}")
    s.exec_end("npm test", "1 failing", exit_code=1)
    recs, _, f = parse(s, tmp_path)
    assert [(r["role"], r["kind"]) for r in recs] == [
        ("user", "text"), ("assistant", "text"), ("assistant", "edit"), ("assistant", "edit"),
        ("assistant", "command"), ("tool", "error")]
    assert recs[0]["id"] == f"{f.name}:{ln_user}"
    assert recs[0]["session"] == "codex-1" and recs[0]["agent"] == "codex"
    assert recs[2]["old"] == "allow read: if false;" and recs[2]["new"] == "allow read: if true;"
    assert recs[3]["new"] == "export default function App() {}" and recs[3]["text"].startswith("WRITE ")
    assert recs[4]["text"] == "npm test"


def test_item_command_strips_file_url_and_reads_string_exit_code(tmp_path):
    app = tmp_path / "app"
    s = CodexSession(app, version="0.154.0")
    s.user("run it")
    s.item_command("npm run dev", "boom", exit_code="1", cwd=app / "web")
    recs, _, _ = parse(s, tmp_path)
    assert [r["kind"] for r in recs] == ["text", "command", "error"]
    assert recs[1]["cwd"] == str(app / "web")


def test_filechange_and_patch_end_for_the_same_change_count_once(tmp_path):
    app = tmp_path / "app"
    s = CodexSession(app)
    change = {str(app / "a.ts"): {"type": "add", "content": "x"}}
    s.user("go")
    s.add(app / "a.ts", "x")
    s.item_filechange(change)
    recs, _, _ = parse(s, tmp_path)
    assert [r["kind"] for r in recs] == ["text", "edit"]


def test_function_call_fallback_and_exit_code_in_output(tmp_path):
    s = CodexSession(tmp_path / "app", version="0.141.0")
    s.user("go")
    s.function_exec("supabase db push", "Chunk ID: 1\nProcess exited with code 1\nOutput:\npermission denied")
    recs, _, _ = parse(s, tmp_path)
    assert [r["kind"] for r in recs] == ["text", "command", "error"]
    assert recs[1]["text"] == "supabase db push"


def test_custom_exec_javascript_command(tmp_path):
    s = CodexSession(tmp_path / "app", version="0.154.0")
    s.user("go")
    s.custom_exec("sed -n '1,20p' a.ts", "Process exited with code 0\nOutput:\nfine")
    recs, _, _ = parse(s, tmp_path)
    assert [r["kind"] for r in recs] == ["text", "command"]
    assert recs[1]["text"] == "sed -n '1,20p' a.ts"


def test_apply_patch_call_used_when_no_patch_events_and_relative_paths_kept(tmp_path):
    s = CodexSession(tmp_path / "app")
    s.user("go")
    s.apply_patch_call("*** Begin Patch\n*** Add File: src/a.ts\n+export const a = 1;\n*** End Patch")
    recs, _, _ = parse(s, tmp_path)
    assert recs[1]["kind"] == "edit" and recs[1]["files"] == ["src/a.ts"]
    assert recs[1]["new"] == "export const a = 1;"


def test_guardian_sessions_are_skipped(tmp_path):
    s = CodexSession(tmp_path / "app", source={"subagent": {"other": "guardian"}})
    s.user("The following is the Codex agent history whose request action you are assessing ...")
    recs, stats, _ = parse(s, tmp_path)
    assert recs == [] and stats.skipped_sessions == 1


def test_spawned_subagent_prompt_is_agent(tmp_path):
    s = CodexSession(tmp_path / "app", source={"subagent": {"thread_spawn": {"parent_thread_id": "p", "depth": 1}}})
    s.user("You are a critic.")
    recs, _, _ = parse(s, tmp_path)
    assert recs[0]["role"] == "agent" and recs[0]["sidechain"] is True


def test_compaction_is_counted(tmp_path):
    s = CodexSession(tmp_path / "app")
    s.user("go")
    s.compacted()
    _, stats, _ = parse(s, tmp_path)
    assert stats.compact_summaries == 1
```

- [ ] **Step 3: Write the failing `collect` tests**

`tests/test_collect.py`:
```python
import json

import sessions
from helpers.fake_logs import ClaudeSession, CodexSession

OPENAI = "sk-proj-" + "Ab3dE5fG7hJ9kL1mN3pQ5rS7tU9vW1xY"


def run(app, tmp_path, archive=False):
    return sessions.collect(app, claude_dir=tmp_path / "projects", codex_dir=tmp_path / "sessions",
                            archive_dir=(tmp_path / "archive") if archive else None)


def test_collect_claims_sessions_by_cwd_and_edit_paths(tmp_path):
    app, other = tmp_path / "app", tmp_path / "other"
    app.mkdir()
    other.mkdir()
    a = ClaudeSession(app, "s-app")
    a.user("build the app")
    a.save(tmp_path / "projects")
    b = ClaudeSession(other, "s-other")
    b.user("unrelated app question")
    b.save(tmp_path / "projects")
    c = ClaudeSession(tmp_path, "s-home")
    c.user("fix the app from home")
    c.edit(app / "x.ts", "a", "b")
    c.save(tmp_path / "projects")
    recs, stats = run(app, tmp_path)
    assert {r["session"] for r in recs} == {"s-app", "s-home"}
    assert any(r["text"] == "fix the app from home" for r in recs)
    assert all(r["in_project"] for r in recs)
    assert stats.threads == 2 and stats.by_agent["claude-code"] == 2


def test_cwd_change_mid_session_keeps_only_project_records(tmp_path):
    app, other = tmp_path / "app", tmp_path / "other"
    app.mkdir()
    other.mkdir()
    s = ClaudeSession(app, "s1")
    s.user("app question")
    s.set_cwd(other)
    s.user("other question")
    s.save(tmp_path / "projects")
    recs, _ = run(app, tmp_path)
    assert [r["text"] for r in recs] == ["app question"]


def test_symlinked_project_path(tmp_path):
    real = tmp_path / "real" / "app"
    real.mkdir(parents=True)
    (tmp_path / "link").symlink_to(tmp_path / "real")
    s = ClaudeSession(tmp_path / "link" / "app", "s1")
    s.user("hello app")
    s.save(tmp_path / "projects")
    recs, _ = run(real, tmp_path)
    assert [r["text"] for r in recs] == ["hello app"]


def test_turns_and_seq(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    s = ClaudeSession(app, "s1")
    s.user("one")
    s.assistant_text("reply")
    s.user("two")
    s.save(tmp_path / "projects")
    recs, _ = run(app, tmp_path)
    assert [(r["seq"], r["turn"]) for r in recs] == [(0, 1), (1, 1), (2, 2)]


def test_codex_and_claude_threads_are_ordered_by_time(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    c = CodexSession(app, "x1")
    c.user("codex first")
    c.save(tmp_path / "sessions")
    s = ClaudeSession(app, "s1", start=100)
    s.user("claude later")
    s.save(tmp_path / "projects")
    recs, stats = run(app, tmp_path)
    assert [r["text"] for r in recs] == ["codex first", "claude later"]
    assert stats.by_agent == {"codex": 1, "claude-code": 1}
    assert stats.earliest < stats.latest


def test_relative_codex_patch_paths_resolve_against_cwd(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    s = CodexSession(app)
    s.user("go")
    s.apply_patch_call("*** Begin Patch\n*** Add File: src/a.ts\n+x\n*** End Patch")
    s.save(tmp_path / "sessions")
    recs, _ = run(app, tmp_path)
    assert recs[1]["files"] == [str(app / "src/a.ts")]


def test_digest_is_masked(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    s = ClaudeSession(app, "s1")
    s.user(f"my key is {OPENAI}")
    s.save(tmp_path / "projects")
    recs, _ = run(app, tmp_path)
    assert OPENAI not in recs[0]["text"] and "sk-proj-…" in recs[0]["text"]


def test_archive_keeps_threads_whose_logs_were_deleted(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    s = ClaudeSession(app, "s1")
    s.user(f"remember this {OPENAI}")
    f = s.save(tmp_path / "projects")
    run(app, tmp_path, archive=True)
    archived = list((tmp_path / "archive").glob("*.jsonl"))
    assert archived and OPENAI not in archived[0].read_text(encoding="utf-8")
    f.unlink()
    recs, stats = run(app, tmp_path, archive=True)
    assert [r["text"][:13] for r in recs] == ["remember this"]
    assert stats.archived_threads == 1


def test_prefilter_skips_unrelated_files(tmp_path):
    app = tmp_path / "myapp"
    app.mkdir()
    for i in range(3):
        u = ClaudeSession(tmp_path / f"elsewhere{i}", f"u{i}")
        u.user("nothing to see")
        u.save(tmp_path / "projects")
    s = ClaudeSession(app, "s1")
    s.user("hello")
    s.save(tmp_path / "projects")
    _, stats = run(app, tmp_path)
    assert stats.files_scanned == 4 and stats.files_parsed == 1 and stats.files_matched == 1


def test_prefilter_accepts_json_escaped_folder_names(tmp_path):
    app = tmp_path / "笔记"
    app.mkdir()
    f = tmp_path / "projects" / "x" / "s1.jsonl"
    f.parent.mkdir(parents=True)
    rec = {"type": "user", "uuid": "u1", "sessionId": "s1", "timestamp": "2026-09-12T09:00:00Z",
           "cwd": str(app), "message": {"role": "user", "content": "hello"}}
    f.write_text(json.dumps(rec) + "\n", encoding="utf-8")  # ensure_ascii=True escapes the folder name
    recs, _ = run(app, tmp_path)
    assert [r["text"] for r in recs] == ["hello"]


def test_unreadable_format_warns(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    f = tmp_path / "projects" / "x" / "weird.jsonl"
    f.parent.mkdir(parents=True)
    f.write_text(json.dumps({"type": "brand-new-format", "cwd": str(app), "body": "hi"}) + "\n", encoding="utf-8")
    recs, stats = run(app, tmp_path)
    assert recs == [] and any("format may have changed" in w for w in stats.warnings)


def test_missing_log_dirs_are_fine(tmp_path):
    app = tmp_path / "app"
    app.mkdir()
    recs, stats = sessions.collect(app, claude_dir=tmp_path / "nope", codex_dir=None)
    assert recs == [] and stats.files_scanned == 0
```

- [ ] **Step 4: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_sessions_codex.py tests/test_collect.py`
Expected: FAIL — `AttributeError: module 'sessions' has no attribute 'parse_codex_file'` (and `collect`).

- [ ] **Step 5: Append the Codex parser and `collect` to `scripts/sessions.py`**

Add these imports at the top of `scripts/sessions.py` (merge with the existing import block):
```python
import json
import os
import re

from common import ERROR_LINE, is_within, read_jsonl, write_jsonl
from redact import redact
```

Append:
```python
GUARDIAN_PREFIX = "The following is the Codex agent history whose request action you are assessing"
_PATCH_FILE = re.compile(r"^\*\*\* (Add|Update|Delete) File: (.+)$", re.M)
_JS_CMD = re.compile(r'"cmd"\s*:\s*"((?:[^"\\]|\\.)*)"')
_EXIT = re.compile(r"(?:Process exited with code|Exit code:?)\s*(-?\d+)")
_SHELL_FUNCTIONS = {"exec_command", "shell", "local_shell", "container.exec"}


def _strip_file_url(cwd) -> str:
    if isinstance(cwd, str) and cwd.startswith("file://"):
        return cwd[len("file://"):]
    return cwd or ""


def _exit_code(value) -> int | None:
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def _command_text(cmd) -> str:
    if isinstance(cmd, list):
        if len(cmd) >= 3 and cmd[1] in ("-lc", "-c"):
            return str(cmd[2])
        return " ".join(map(str, cmd))
    return str(cmd or "")


def _diff_sides(diff: str) -> tuple[str, str]:
    old, new = [], []
    for line in diff.splitlines():
        if line.startswith(("---", "+++", "@@", "***")):
            continue
        if line.startswith("-"):
            old.append(line[1:])
        elif line.startswith("+"):
            new.append(line[1:])
    return "\n".join(old), "\n".join(new)


def _change_rec(path: str, ch: dict) -> dict:
    kind = ch.get("type")
    if kind == "update":
        diff = ch.get("unified_diff") or ""
        old, new = _diff_sides(diff)
        text = f"EDIT {path}\n{diff}"
    elif kind == "add":
        old, new = "", ch.get("content") or ""
        text = f"WRITE {path}\n{new}"
    else:
        old, new = ch.get("content") or "", ""
        text = f"DELETE {path}"
    return _rec("assistant", "edit", text[:EDIT_LIMIT], [path], old=old, new=new)


def _changes(changes: dict, seen: set) -> list[dict]:
    out = []
    for path, ch in changes.items():
        if not isinstance(ch, dict):
            continue
        key = (path, ch.get("type"), ch.get("unified_diff") or ch.get("content") or "")
        if key in seen:
            continue
        seen.add(key)
        out.append(_change_rec(path, ch))
    return out


def _apply_patch_recs(patch: str) -> list[dict]:
    parts = _PATCH_FILE.split(patch)  # [before, op, path, body, op, path, body, ...]
    out = []
    for i in range(1, len(parts) - 2, 3):
        op, path, body = parts[i], parts[i + 1].strip(), parts[i + 2]
        old, new = _diff_sides(body)
        verb = "WRITE" if op == "Add" else op.upper()
        out.append(_rec("assistant", "edit", f"{verb} {path}\n{body.strip()}"[:EDIT_LIMIT], [path], old=old, new=new))
    return out


def _output_text(out) -> str:
    if isinstance(out, list):
        return "\n".join(str(b.get("text", "")) for b in out if isinstance(b, dict))
    if isinstance(out, str):
        try:
            j = json.loads(out)
        except json.JSONDecodeError:
            return out
        if isinstance(j, dict) and "output" in j:
            meta = j.get("metadata") if isinstance(j.get("metadata"), dict) else {}
            code = meta.get("exit_code")
            return str(j.get("output", "")) + (f"\nProcess exited with code {code}" if code is not None else "")
        return out
    return ""


def _fn_commands(p: dict) -> list[str]:
    name = p.get("name")
    if p.get("type") == "custom_tool_call" and name == "exec":
        out = []
        for m in _JS_CMD.finditer(p.get("input") or ""):
            try:
                out.append(json.loads('"' + m.group(1) + '"'))
            except json.JSONDecodeError:
                out.append(m.group(1))
        return out
    if p.get("type") == "function_call" and name in _SHELL_FUNCTIONS:
        try:
            args = json.loads(p.get("arguments") or "{}")
        except json.JSONDecodeError:
            return []
        cmd = args.get("cmd") or args.get("command") if isinstance(args, dict) else None
        return [_command_text(cmd)] if cmd else []
    return []


def _command_recs(p: dict, at_cwd: str) -> list[dict]:
    cwd = _strip_file_url(p.get("cwd")) or at_cwd
    out = [_rec("assistant", "command", _command_text(p.get("command"))[:TOOL_TEXT_LIMIT])]
    output = p.get("aggregated_output") or ((p.get("stdout") or "") + (p.get("stderr") or ""))
    code = _exit_code(p.get("exit_code"))
    if code not in (None, 0) or ERROR_LINE.search(output or ""):
        out.append(_rec("tool", "error", (output or f"exit code {code}")[:TOOL_TEXT_LIMIT]))
    for r in out:
        r["_cwd"] = cwd
    return out


def parse_codex_file(path, stats: Stats) -> list[dict]:
    """One Codex rollout file -> digest records of one thread ([] for skipped sessions)."""
    path = Path(path)
    session, cwd, side = path.stem, "", False
    events = []
    for lineno, obj in read_jsonl(path):
        if obj is None:
            stats.bad_lines += 1
            continue
        typ = obj.get("type")
        p = obj.get("payload") if isinstance(obj.get("payload"), dict) else {}
        if typ == "session_meta":
            session = p.get("id") or p.get("session_id") or session
            cwd = _strip_file_url(p.get("cwd")) or cwd
            src = p.get("source")
            if isinstance(src, dict) and "subagent" in src:
                sub = src["subagent"]
                if isinstance(sub, dict) and sub.get("other") == "guardian":
                    stats.skipped_sessions += 1
                    return []
                side = True
            continue
        if typ == "turn_context":
            cwd = _strip_file_url(p.get("cwd")) or cwd
            continue
        if typ == "compacted" or (typ == "event_msg" and p.get("type") == "context_compacted"):
            stats.compact_summaries += 1
            continue
        events.append((lineno, obj.get("timestamp", ""), cwd, typ, p))

    kinds = {(t, p.get("type")) for _, _, _, t, p in events}
    items = {p.get("item", {}).get("type") for _, _, _, t, p in events
             if t == "event_msg" and p.get("type") == "item_completed" and isinstance(p.get("item"), dict)}
    use_patch_end = ("event_msg", "patch_apply_end") in kinds
    use_filechange = "FileChange" in items
    use_patch_call = not (use_patch_end or use_filechange)
    use_item_cmd = "CommandExecution" in items
    use_exec_end = not use_item_cmd and ("event_msg", "exec_command_end") in kinds
    use_fn = not (use_item_cmd or use_exec_end)

    records: list[dict] = []
    seen: set = set()
    calls: dict = {}
    for lineno, ts, at_cwd, typ, p in events:
        pt = p.get("type")
        new: list[dict] = []
        if typ == "event_msg" and pt == "user_message":
            text = p.get("message") or ""
            if text.startswith(GUARDIAN_PREFIX):
                stats.skipped_sessions += 1
                return []
            if text.strip():
                new.append(_rec("agent" if side else "user", "text", text))
        elif typ == "event_msg" and pt == "agent_message":
            if (p.get("message") or "").strip():
                new.append(_rec("assistant", "text", p["message"]))
        elif typ == "event_msg" and pt == "patch_apply_end" and use_patch_end:
            new += _changes(p.get("changes") or {}, seen)
        elif typ == "event_msg" and pt == "item_completed" and isinstance(p.get("item"), dict):
            item = p["item"]
            if item.get("type") == "FileChange" and use_filechange:
                new += _changes(item.get("changes") or {}, seen)
            elif item.get("type") == "CommandExecution" and use_item_cmd:
                new += _command_recs(item, at_cwd)
        elif typ == "event_msg" and pt == "exec_command_end" and use_exec_end:
            new += _command_recs(p, at_cwd)
        elif typ == "response_item" and pt == "custom_tool_call" and p.get("name") == "apply_patch":
            if use_patch_call:
                new += _apply_patch_recs(p.get("input") or "")
        elif typ == "response_item" and use_fn and pt in ("function_call", "custom_tool_call"):
            cmds = _fn_commands(p)
            if cmds:
                calls[p.get("call_id")] = cmds
                new += [_rec("assistant", "command", c[:TOOL_TEXT_LIMIT]) for c in cmds]
        elif (typ == "response_item" and use_fn and pt in ("function_call_output", "custom_tool_call_output")
              and p.get("call_id") in calls):
            text = _output_text(p.get("output"))
            m = _EXIT.search(text)
            code = int(m.group(1)) if m else None
            if code not in (None, 0) or ERROR_LINE.search(text):
                new.append(_rec("tool", "error", text[:TOOL_TEXT_LIMIT]))
        else:
            stats.ignored_types[f"codex:{typ}/{pt}"] += 1
        for k, r in enumerate(new):
            r.update(id=f"{path.name}:{lineno}" if k == 0 else f"{path.name}:{lineno}#{k}",
                     session=session, agent="codex", ts=ts, cwd=r.pop("_cwd", at_cwd), sidechain=side)
            records.append(r)
    return records


def default_claude_dir() -> Path:
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "projects"


def default_codex_dir() -> Path:
    return Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex") / "sessions"


def _number(records: list[dict]) -> None:
    """Order within the thread, user-turn numbers, absolute file paths."""
    turn = 0
    for i, r in enumerate(records):
        if r["role"] == "user":
            turn += 1
        r["seq"], r["turn"] = i, turn
        cwd = r.get("cwd") or ""
        r["files"] = [f if Path(f).is_absolute() or not cwd else str(Path(cwd) / f) for f in r["files"]]


def _claim(records: list[dict], root: Path) -> list[dict]:
    """The records of one thread that concern `root`; [] when the thread never touches it."""
    touches = any(is_within(f, root) for r in records for f in r["files"])
    if not touches and not any(is_within(r["cwd"], root) for r in records if r["cwd"]):
        return []
    kept = []
    for r in records:
        cwd = r["cwd"]
        r["in_project"] = ((bool(cwd) and is_within(cwd, root))
                           or any(is_within(f, root) for f in r["files"])
                           or (touches and bool(cwd) and is_within(root, cwd)))
        if r["in_project"]:
            kept.append(r)
    return kept


def _archive_name(thread: str) -> str:
    return re.sub(r"[^\w.-]+", "__", thread) + ".jsonl"


def load_archive(archive_dir) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    base = Path(archive_dir)
    if not base.is_dir():
        return out
    for f in sorted(base.glob("*.jsonl")):
        recs = [obj for _, obj in read_jsonl(f) if obj]
        if recs:
            out[recs[0]["session"]] = recs
    return out


def save_archive(archive_dir, threads: list[list[dict]]) -> None:
    for recs in threads:
        if recs:
            write_jsonl(Path(archive_dir) / _archive_name(recs[0]["session"]), recs)


def _log_files(claude_dir, codex_dir):
    for agent, base in (("claude-code", claude_dir), ("codex", codex_dir)):
        if base and Path(base).is_dir():
            for f in sorted(Path(base).rglob("*.jsonl")):
                yield agent, f


def collect(root, claude_dir=None, codex_dir=None, archive_dir=None) -> tuple[list[dict], Stats]:
    root = Path(root).resolve()
    stats = Stats()
    threads: dict[str, list[dict]] = {}
    needles = {root.name, json.dumps(root.name)[1:-1]}  # raw and \u-escaped spellings
    for agent, f in _log_files(claude_dir, codex_dir):
        stats.files_scanned += 1
        try:
            raw = f.read_text(encoding="utf-8", errors="replace")
        except OSError as exc:
            stats.warnings.append(f"cannot read {f}: {exc}")
            continue
        if not any(n in raw for n in needles):
            continue  # cheap prefilter: a file that never names the folder cannot belong to it
        stats.files_parsed += 1
        skipped_before = stats.skipped_sessions
        recs = parse_claude_file(f, stats) if agent == "claude-code" else parse_codex_file(f, stats)
        if stats.skipped_sessions > skipped_before:
            continue
        if not any(r["kind"] == "text" for r in recs) and str(root) in raw:
            stats.warnings.append(f"{f.name}: mentions this project but no messages could be read; "
                                  "the log format may have changed")
        if not recs:
            continue
        _number(recs)
        kept = _claim(recs, root)
        if kept:
            stats.files_matched += 1
            threads.setdefault(kept[0]["session"], []).extend(kept)
    if archive_dir:
        for thread, recs in load_archive(archive_dir).items():
            if thread not in threads:
                threads[thread] = recs
                stats.archived_threads += 1
    ordered = sorted(threads.values(), key=lambda rs: min(r["ts"] for r in rs))
    out: list[dict] = []
    for recs in ordered:
        recs.sort(key=lambda r: (r["ts"], r["seq"]))
        for i, r in enumerate(recs):
            r["seq"] = i
            for key in ("text", "old", "new"):
                if key in r:
                    r[key] = redact(r[key])
        out.extend(recs)
    if archive_dir:
        save_archive(archive_dir, ordered)
    stats.threads, stats.records = len(ordered), len(out)
    stats.by_agent = Counter(rs[0]["agent"] for rs in ordered)
    stamps = [r["ts"] for r in out if r["ts"]]
    stats.earliest, stats.latest = (min(stamps), max(stamps)) if stamps else ("", "")
    return out, stats
```

Also update the existing `from common import ...` line in the Claude part so the module has a single import block (`ERROR_LINE, is_within, read_jsonl, write_jsonl`).

- [ ] **Step 6: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_sessions_claude.py tests/test_sessions_codex.py tests/test_collect.py`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add tests/helpers/fake_logs.py scripts/sessions.py tests/test_sessions_codex.py tests/test_collect.py
git commit -m "feat: parse Codex rollouts and collect a project's masked digest"
```

---
### Task 4: Candidates and reading packs

**Files:**
- Create: `scripts/candidates.py`
- Test: `tests/test_candidates.py`

**Interfaces:**
- Consumes: digest records (see File Structure); `common.USER_ERROR`, `common.iter_files`, `common.read_text`, `common.rel` (Task 1).
- Produces:
  - `candidates.WINDOW_MAX = 20`, `candidates.PACK_LIMIT = 120_000`, `candidates.RECORD_LIMIT = 4000`
  - `candidates.is_change(rec) -> bool`, `candidates.bypass_hints(rec) -> list[str]`
  - `candidates.find_compromises(recs) -> list[dict]` — each `{"id": "K1", "session", "turn", "error_id", "window_ids": [...], "change_ids": [...], "hints": [...], "priority": int}`
  - `candidates.find_deferrals(recs) -> list[dict]` — each `{"id": "D1", "msg_id", "session", "turn", "phrases": [...]}`
  - `candidates.find_claims(recs) -> list[dict]` — each `{"id": "A1", "msg_id", "session", "turn", "phrases": [...]}`
  - `candidates.scan_code_todos(root) -> list[dict]` — each `{"path", "line", "text"}`
  - `candidates.render_record(rec) -> str`
  - `candidates.build_packs(root, recs, comps, defs, claims, todos, limit=PACK_LIMIT) -> list[str]`
  - `candidates.run(root, recs, limit=PACK_LIMIT) -> dict` with keys `compromises, deferrals, claims, todos, packs_text, stats`

- [ ] **Step 1: Write the failing tests**

`tests/test_candidates.py`:
```python
import candidates


def rec(i, role, kind, text, turn, session="s1", **extra):
    r = {"id": f"r{i}", "session": session, "agent": "claude-code", "ts": f"2026-09-12T09:{i:02d}:00Z",
         "role": role, "kind": kind, "text": text, "files": [], "cwd": "/app", "sidechain": False,
         "seq": i, "turn": turn, "in_project": True}
    r.update(extra)
    return r


def edit(i, turn, old, new, path="/app/supabase/migrations/001.sql"):
    return rec(i, "assistant", "edit", f"EDIT {path}\n--- before\n{old}\n+++ after\n{new}", turn,
               files=[path], old=old, new=new)


def test_error_then_bypass_edit_is_a_candidate():
    recs = [rec(0, "user", "text", "save my notes", 1),
            rec(1, "tool", "error", "new row violates row-level security policy", 1),
            edit(2, 1, "alter table notes enable row level security;\ncreate policy p on notes using (auth.uid() = user_id);",
                 "alter table notes disable row level security;")]
    [c] = candidates.find_compromises(recs)
    assert c["id"] == "K1" and c["error_id"] == "r1" and c["change_ids"] == ["r2"]
    assert "rls_disabled" in c["hints"] and "removed_guard" in c["hints"]
    assert c["priority"] == len(c["hints"])


def test_user_reported_error_counts():
    recs = [rec(0, "user", "text", "保存的时候报错了", 1),
            edit(1, 1, "", "app.use(cors());", path="/app/server.js")]
    [c] = candidates.find_compromises(recs)
    assert c["error_id"] == "r0" and "cors_wildcard" in c["hints"]


def test_error_without_a_following_change_is_not_a_candidate():
    recs = [rec(0, "tool", "error", "Error: boom", 1), rec(1, "assistant", "text", "Let me look.", 1)]
    assert candidates.find_compromises(recs) == []


def test_window_stops_after_the_next_turn():
    recs = [rec(0, "tool", "error", "Error: boom", 1),
            rec(1, "user", "text", "ok", 2),
            rec(2, "user", "text", "now something else", 3),
            edit(3, 3, "a", "b")]
    assert candidates.find_compromises(recs) == []


def test_window_stops_after_twenty_records():
    recs = [rec(0, "tool", "error", "Error: boom", 1)]
    recs += [rec(i, "assistant", "text", "thinking", 1) for i in range(1, 22)]
    recs.append(edit(22, 1, "a", "b"))
    assert candidates.find_compromises(recs) == []


def test_overlapping_errors_merge_into_one_candidate():
    recs = [rec(0, "tool", "error", "Error: one", 1), rec(1, "tool", "error", "Error: two", 1),
            edit(2, 1, "a", "b")]
    assert len(candidates.find_compromises(recs)) == 1


def test_command_writes_count_as_changes_but_not_dev_null():
    assert candidates.is_change(rec(0, "assistant", "command", "cat > a.sql <<'EOF'\nselect 1;\nEOF", 1))
    assert candidates.is_change(rec(0, "assistant", "command", "sed -i '' 's/a/b/' x.ts", 1))
    assert not candidates.is_change(rec(0, "assistant", "command", "ls > /dev/null 2>&1", 1))
    assert not candidates.is_change(rec(0, "assistant", "command", "npm test", 1))


def test_bypass_hint_catalogue():
    def hints(new, old=""):
        return candidates.bypass_hints({"kind": "edit", "text": "", "old": old, "new": new})
    assert "policy_allows_all" in hints("create policy p on t for select using (true);")
    assert "type_check_silenced" in hints("// @ts-ignore\nconst x = y as any;")
    assert "verify_skipped" in hints("https.Agent({ rejectUnauthorized: false })")
    assert "service_role_used" in hints("createClient(url, process.env.SUPABASE_SERVICE_ROLE_KEY)")
    assert "empty_catch" in hints("try { go() } catch (e) {}")
    assert "mock_data" in hints("const notes = mockNotes;")
    assert "removed_guard" in hints("handler()", old="requireAuth(handler)")
    assert hints("const total = a + b;") == []


def test_deferrals_from_text_records():
    recs = [rec(0, "assistant", "text", "为了先跑起来，我暂时关闭 RLS，之后再补策略。", 1),
            rec(1, "assistant", "text", "For now I'm using test mode; lock it down before launch.", 1),
            rec(2, "assistant", "text", "All done.", 1),
            rec(3, "tool", "error", "temporary failure", 1)]
    found = candidates.find_deferrals(recs)
    assert [d["msg_id"] for d in found] == ["r0", "r1"]
    assert "暂时" in found[0]["phrases"] and "for now" in found[1]["phrases"]


def test_claims_are_the_last_ai_text_of_each_turn():
    recs = [rec(0, "user", "text", "add login", 1),
            rec(1, "assistant", "text", "I've added the login check.", 1),
            rec(2, "assistant", "text", "接口已经加了登录保护。", 1),
            rec(3, "user", "text", "thanks", 2),
            rec(4, "assistant", "text", "You're welcome.", 2)]
    found = candidates.find_claims(recs)
    assert [a["msg_id"] for a in found] == ["r2"]


def test_code_todos_only_in_comments(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "a.ts").write_text(
        'const PASSWORD = "admin123"; // hardcoded for now\n'
        '<input placeholder="Email" />\n'
        "# TODO: lock down\n"
        "/* 这里暂时写死 */\n", encoding="utf-8")
    found = candidates.scan_code_todos(tmp_path)
    assert [(t["path"], t["line"]) for t in found] == [("src/a.ts", 1), ("src/a.ts", 3), ("src/a.ts", 4)]


def test_single_small_pack_contains_every_user_message_and_ids(tmp_path):
    recs = [rec(0, "user", "text", "只有我自己能看到我的笔记", 1),
            rec(1, "tool", "error", "Error: violates row-level security", 1),
            edit(2, 1, "enable row level security", "disable row level security")]
    out = candidates.run(tmp_path, recs)
    assert len(out["packs_text"]) == 1
    pack = out["packs_text"][0]
    assert "[r0]" in pack and "只有我自己能看到我的笔记" in pack
    assert "Candidate K1" in pack and "[r2]" in pack
    assert out["stats"]["packs"] == 1 and out["stats"]["compromises"] == 1


def test_large_digest_splits_into_packs_under_the_limit(tmp_path):
    recs = []
    for turn in range(1, 41):
        recs.append(rec(turn, "user", "text", f"turn {turn} " + "x" * 900, turn))
    packs = candidates.build_packs(tmp_path, recs, [], [], [], [], limit=5000)
    assert len(packs) > 1
    joined = "".join(packs)
    assert all(f"[r{i}]" in joined for i in range(1, 41))
    assert all(len(p) <= 5000 + 1000 for p in packs)  # limit plus the fixed header


def test_long_record_is_truncated_with_a_marker():
    text = candidates.render_record(rec(0, "user", "text", "y" * (candidates.RECORD_LIMIT + 50), 1))
    assert "50 more characters not shown" in text


def test_empty_digest_still_makes_one_pack(tmp_path):
    out = candidates.run(tmp_path, [])
    assert len(out["packs_text"]) == 1 and "No conversation records" in out["packs_text"][0]
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_candidates.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'candidates'`.

- [ ] **Step 3: Write `scripts/candidates.py`**

```python
"""Find the moments in the digest worth the model's attention and write the
reading packs: the only conversation text the model reads.

Candidates are hints from simple rules; the model judges each one and the
verifier checks whatever it concludes."""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

from common import USER_ERROR, iter_files, read_text, rel

WINDOW_MAX = 20
PACK_LIMIT = 120_000
RECORD_LIMIT = 4000

WRITE_CMD = re.compile(
    r"sed\s+-i|>>?\s*(?!/dev/null)[\w./~\"'-]|\btee\b|<<-?\s*['\"]?\w+|\bpsql\b"
    r"|\bsupabase\s+(?:db|migration)|\bprisma\s+(?:migrate|db)|\bfirebase\s+deploy"
    r"|\b(?:mv|cp|rm)\s|writeFile|open\([^)]*['\"][wa]\+?['\"]"
)
BYPASS = [
    ("rls_disabled", re.compile(r"disable\s+row\s+level\s+security", re.I)),
    ("policy_allows_all", re.compile(r"(?:using|with\s+check)\s*\(\s*true\s*\)", re.I)),
    ("cors_wildcard", re.compile(r"""origin\s*:\s*['"]\*['"]|Access-Control-Allow-Origin['"]?\s*[:,]\s*['"]\*|\bcors\(\s*\)""", re.I)),
    ("type_check_silenced", re.compile(r"@ts-ignore|@ts-nocheck|eslint-disable|:\s*any\b|\bas\s+any\b|#\s*type:\s*ignore|#\s*noqa")),
    ("verify_skipped", re.compile(r"--no-verify|verify\s*=\s*False|rejectUnauthorized\s*:\s*false|NODE_TLS_REJECT_UNAUTHORIZED\s*=\s*['\"]?0|InsecureSkipVerify", re.I)),
    ("service_role_used", re.compile(r"service_role", re.I)),
    ("empty_catch", re.compile(r"catch\s*(?:\([^)]*\))?\s*\{\s*\}|except[^:\n]*:\s*\n?\s*pass\b")),
    ("mock_data", re.compile(r"\b(?:mock|fake|dummy|hardcoded?)\w*", re.I)),
    ("commented_out", re.compile(r"^\s*(?://|#)\s*(?:app\.use|await\s+\w*auth|if\s*\(\s*!?\s*\w*(?:user|session|auth))", re.I | re.M)),
]
GUARD_WORD = re.compile(r"\b(auth\w*|polic\w*|verif\w*|check\w*|validat\w*|permission\w*|require\w*)", re.I)
DEFER = re.compile(
    r"for now|temporar(?:y|ily)|placeholder|\bmock(?:ed)?\b|hard-?cod(?:e|ed)|\bstub(?:bed)?\b"
    r"|in production,? you(?:'ll)? (?:should|need|want)|quick fix|workaround"
    r"|before (?:launch|deploy\w*|going live|you ship)"
    r"|暂时|先这样|之后再|后续再|以后再|临时|写死|模拟数据|先跑起来|先不管|上线前",
    re.I,
)
CLAIM = re.compile(
    r"I(?:'ve| have) (?:added|implemented|set up|secured|protected|enabled|fixed|built|created)"
    r"|now (?:protected|secure|private|requires?|only)|\b(?:is|are) now\b"
    r"|已经|已(?:实现|添加|修复|完成|开启|加)|✅",
    re.I,
)
TODO = re.compile(
    r"(?:(?:^|\s)(?://|#|--)|/\*|<!--)[^\n]*?"
    r"(?:\b(?:TODO|FIXME|HACK|XXX|for now|temporar\w*|mock\w*|placeholder|hard-?coded?)\b|暂时|临时|写死)",
    re.I,
)
TODO_EXTS = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte", ".py", ".rb", ".go",
             ".php", ".sql", ".rules", ".html", ".css"}
ROLE = {"user": "USER", "assistant": "AI", "agent": "PARENT-AGENT", "tool": "TOOL-OUTPUT"}
HEADER = (
    "# vibe-ledger reading pack {k}/{n}\n\n"
    "Project: {root}\n\n"
    "Each record starts with `[ID]`. Use that ID as `msg_id`. Copy quotes character for character "
    "from the text under the header, and never quote across a \"not shown\" marker. Candidates are "
    "hints from simple rules, not findings: judge each one.\n\n"
)


def _by_session(recs: list[dict]) -> dict[str, list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for r in recs:
        groups[r["session"]].append(r)
    for g in groups.values():
        g.sort(key=lambda r: r["seq"])
    return groups


def is_change(r: dict) -> bool:
    return r["kind"] == "edit" or (r["kind"] == "command" and bool(WRITE_CMD.search(r["text"])))


def _is_error_signal(r: dict) -> bool:
    if r["kind"] == "error":
        return True
    return r["role"] == "user" and r["kind"] == "text" and bool(USER_ERROR.search(r["text"]))


def bypass_hints(r: dict) -> list[str]:
    new = r.get("new") if r.get("new") is not None else (r["text"] if r["kind"] == "command" else "")
    old = r.get("old") or ""
    hints = [name for name, rx in BYPASS if rx.search(new or "")]
    removed = ({m.group(1).lower() for m in GUARD_WORD.finditer(old)}
               - {m.group(1).lower() for m in GUARD_WORD.finditer(new or "")})
    if removed:
        hints.append("removed_guard")
    return hints


def find_compromises(recs: list[dict]) -> list[dict]:
    spans = []  # (session, list, start, end)
    for session, L in _by_session(recs).items():
        cur = None
        for i, r in enumerate(L):
            if not _is_error_signal(r):
                continue
            end = i
            for j in range(i + 1, min(i + WINDOW_MAX, len(L) - 1) + 1):
                if L[j]["turn"] > r["turn"] + 1:
                    break
                end = j
            if cur is not None and i <= cur[3]:
                cur[3] = max(cur[3], end)
                continue
            cur = [session, L, i, end]
            spans.append(cur)
    out = []
    for session, L, start, end in spans:
        window = L[start:end + 1]
        changes = [x for x in window[1:] if is_change(x)]
        if not changes:
            continue
        hints = sorted({h for x in changes for h in bypass_hints(x)})
        out.append({"id": f"K{len(out) + 1}", "session": session, "turn": L[start]["turn"],
                    "error_id": L[start]["id"], "window_ids": [x["id"] for x in window],
                    "change_ids": [x["id"] for x in changes], "hints": hints, "priority": len(hints)})
    return out


def find_deferrals(recs: list[dict]) -> list[dict]:
    out = []
    for r in recs:
        if r["kind"] != "text" or r["role"] not in ("user", "assistant"):
            continue
        phrases = sorted({m.group(0).lower() for m in DEFER.finditer(r["text"])})
        if phrases:
            out.append({"id": f"D{len(out) + 1}", "msg_id": r["id"], "session": r["session"],
                        "turn": r["turn"], "phrases": phrases})
    return out


def find_claims(recs: list[dict]) -> list[dict]:
    out = []
    for session, L in _by_session(recs).items():
        last: dict[int, dict] = {}
        for r in L:
            if r["role"] == "assistant" and r["kind"] == "text":
                last[r["turn"]] = r
        for turn in sorted(last):
            r = last[turn]
            phrases = sorted({m.group(0) for m in CLAIM.finditer(r["text"])})
            if phrases:
                out.append({"id": f"A{len(out) + 1}", "msg_id": r["id"], "session": session,
                            "turn": turn, "phrases": phrases})
    return out


def scan_code_todos(root) -> list[dict]:
    out = []
    for p in iter_files(root, TODO_EXTS):
        for i, line in enumerate(read_text(p).splitlines(), 1):
            if len(line) <= 500 and TODO.search(line):
                out.append({"path": rel(p, root), "line": i, "text": line.strip()[:200]})
    return out


def render_record(r: dict) -> str:
    text = r["text"]
    if len(text) > RECORD_LIMIT:
        hidden = len(text) - RECORD_LIMIT
        text = text[:RECORD_LIMIT] + f"\n…[{hidden} more characters not shown — do not quote past this point]"
    return f"#### [{r['id']}] {ROLE.get(r['role'], r['role'])} · {r['ts']} · {r['kind']}\n{text.rstrip()}\n"


def _units(recs, comps, defs, claims) -> list[str]:
    groups = _by_session(recs)
    index = {r["id"]: r for r in recs}
    by_turn: dict[tuple[str, int], list[str]] = defaultdict(list)
    for session, L in groups.items():
        for r in L:
            if r["role"] == "user" and r["kind"] == "text":
                by_turn[(session, r["turn"])].append(render_record(r))
    for c in comps:
        body = "".join(render_record(index[i]) for i in c["window_ids"])
        hints = ", ".join(c["hints"]) or "none"
        by_turn[(c["session"], c["turn"])].append(
            f"**Candidate {c['id']} — an error, then a change** (bypass hints: {hints})\n\n{body}")
    for d in defs:
        by_turn[(d["session"], d["turn"])].append(
            f"**Candidate {d['id']} — put off for later?** (matched: {', '.join(d['phrases'])})\n\n"
            + render_record(index[d["msg_id"]]))
    for a in claims:
        by_turn[(a["session"], a["turn"])].append(
            f"**Candidate {a['id']} — the AI says it did something** (matched: {', '.join(a['phrases'])})\n\n"
            + render_record(index[a["msg_id"]]))
    first_ts = {s: L[0]["ts"] for s, L in groups.items()}
    units = []
    for session, turn in sorted(by_turn, key=lambda k: (first_ts[k[0]], k[1])):
        agent = groups[session][0]["agent"]
        units.append(f"### Session {session} ({agent}) · turn {turn}\n\n" + "\n".join(by_turn[(session, turn)]))
    return units


def build_packs(root, recs, comps, defs, claims, todos, limit: int = PACK_LIMIT) -> list[str]:
    groups: list[list[str]] = []
    cur: list[str] = []
    size = 0
    for unit in _units(recs, comps, defs, claims):
        if cur and size + len(unit) > limit:
            groups.append(cur)
            cur, size = [], 0
        cur.append(unit)
        size += len(unit) + 1
    groups.append(cur)
    todo_text = ""
    if todos:
        todo_text = "\n## Code comments that put work off\n\n" + "".join(
            f"- {t['path']}:{t['line']} — {t['text']}\n" for t in todos)
    packs = []
    for k, units in enumerate(groups, 1):
        body = "\n".join(units) if units else "_No conversation records were found for this project._\n"
        packs.append(HEADER.format(k=k, n=len(groups), root=root) + body + (todo_text if k == 1 else ""))
    return packs


def run(root, recs: list[dict], limit: int = PACK_LIMIT) -> dict:
    comps, defs, claims = find_compromises(recs), find_deferrals(recs), find_claims(recs)
    todos = scan_code_todos(root)
    packs = build_packs(root, recs, comps, defs, claims, todos, limit)
    return {"compromises": comps, "deferrals": defs, "claims": claims, "todos": todos,
            "packs_text": packs,
            "stats": {"compromises": len(comps), "deferrals": len(defs), "claims": len(claims),
                      "todos": len(todos), "packs": len(packs), "pack_chars": [len(p) for p in packs]}}
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_candidates.py`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/candidates.py tests/test_candidates.py
git commit -m "feat: find error/deferral/claim candidates and write reading packs"
```

---
### Task 5: Probe framework, stack detection, `secrets_exposed`, `supabase_rls`

**Files:**
- Create: `scripts/probes/__init__.py`, `scripts/probes/util.py`, `scripts/probes/secrets_exposed.py`, `scripts/probes/supabase_rls.py`
- Create (stubs filled in Task 6): `scripts/probes/firebase_rules.py`, `scripts/probes/cors_wildcard.py`, `scripts/probes/paid_api_unauthed.py`, `scripts/probes/routes.py`
- Test: `tests/test_probes_stack_secrets_supabase.py`

**Interfaces:**
- Consumes: `common.iter_files`, `common.read_text`, `common.rel`, `common.git_ls_files`, `common.CODE_EXTS`; `redact.find_secrets` (Task 1).
- Produces:
  - `probes.Finding(probe, level, path, line, snippet, message, implies=[])` with `to_dict()`; `level` ∈ `certain | hint | fact`; `implies` items are `{"resource": str, "subject": "anonymous"|"signed_in"|"owner", "perm": "read"|"write", "value": "allow"|"deny"}` (`resource` may be `"*"` for all data).
  - `probes.SUPPORTED = {"nextjs", "vite", "react", "express", "supabase", "firebase"}`
  - `probes.detect_stack(root) -> {"stacks": [...], "unsupported": [...], "covered": bool}`
  - `probes.run_all(root) -> {"stack": {...}, "findings": [finding dict + "id"], "ran": [names], "skipped": [{"probe", "reason"}]}` — finding id = `"<probe>:<path>:<line>"`, suffixed `#2`, `#3` … on collision.
  - Each probe module: `NAME: str`, `APPLIES_TO: set[str] | None`, `run(root: Path, stack: dict) -> list[Finding]`.
  - `probes.util.CODE` (JS/TS-family extensions), `line_at(text, pos) -> int`, `line_text(text, lineno) -> str`, `first_code_line(text) -> tuple[int, str]`, `is_client_file(relpath, text, stacks) -> bool | None`, `local_imports(root, path, text) -> list[Path]`.

- [ ] **Step 1: Write the failing tests**

`tests/test_probes_stack_secrets_supabase.py`:
```python
import base64
import json
import subprocess

import probes
from probes import secrets_exposed, supabase_rls
from probes.util import is_client_file, local_imports

OPENAI = "sk-proj-" + "Ab3dE5fG7hJ9kL1mN3pQ5rS7tU9vW1xY"


def jwt(role):
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    return enc({"alg": "HS256"}) + "." + enc({"role": role, "iss": "supabase"}) + "." + "s1gnatureS1gnature"


def write(root, rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def test_detect_stack_from_package_json_and_files(tmp_path):
    write(tmp_path, "package.json", json.dumps({"dependencies": {"next": "15", "@supabase/supabase-js": "2"},
                                                "devDependencies": {"vite": "5"}}))
    write(tmp_path, "firestore.rules", "rules_version = '2';")
    write(tmp_path, "api/requirements.txt", "flask==3.0\n")
    st = probes.detect_stack(tmp_path)
    assert st["stacks"] == ["firebase", "flask", "nextjs", "supabase", "vite"]
    assert st["unsupported"] == ["flask"] and st["covered"] is True


def test_detect_stack_unknown_project(tmp_path):
    write(tmp_path, "main.go", "package main")
    write(tmp_path, "go.mod", "module x")
    st = probes.detect_stack(tmp_path)
    assert st == {"stacks": ["go"], "unsupported": ["go"], "covered": False}


def test_client_prefixed_secret_in_env_is_certain(tmp_path):
    write(tmp_path, ".env.local", f"NEXT_PUBLIC_SUPABASE_ANON_KEY={jwt('anon')}\nNEXT_PUBLIC_OPENAI_API_KEY={OPENAI}\n"
                                  "OPENAI_API_KEY_SERVER=fine-on-server\nVITE_ADMIN_SECRET=x\n")
    write(tmp_path, ".env.example", f"NEXT_PUBLIC_OPENAI_API_KEY={OPENAI}\n")
    found = secrets_exposed.run(tmp_path, {"stacks": ["nextjs"]})
    got = sorted((f.path, f.line, f.level) for f in found)
    assert got == [(".env.local", 2, "certain"), (".env.local", 4, "certain")]


def test_hardcoded_secret_in_code_but_not_anon_jwt(tmp_path):
    write(tmp_path, "src/ai.ts", f'const key = "{OPENAI}";\nconst anon = "{jwt("anon")}";\n'
                                 f'const admin = "{jwt("service_role")}";\n')
    found = secrets_exposed.run(tmp_path, {"stacks": []})
    assert sorted(f.line for f in found) == [1, 3]


def test_tracked_env_file_is_reported(tmp_path):
    write(tmp_path, ".env", "A=1\n")
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "add", ".env"], check=True)
    found = secrets_exposed.run(tmp_path, {"stacks": []})
    assert [(f.path, f.line, f.snippet) for f in found] == [(".env", 1, "A=1")]


def test_secrets_probe_without_git(tmp_path):
    write(tmp_path, "src/a.ts", "export const a = 1;\n")
    assert secrets_exposed.run(tmp_path, {"stacks": []}) == []


MIGRATION = """create table notes (
  id uuid primary key,
  user_id uuid not null
);

alter table notes disable row level security;

create table profiles (id uuid primary key);
alter table profiles enable row level security;
create policy "everyone reads" on profiles for select using (true);

create table todos (id bigint primary key);
"""


def test_supabase_rls_findings_and_implications(tmp_path):
    write(tmp_path, "supabase/migrations/001_init.sql", MIGRATION)
    write(tmp_path, "lib/db.ts", 'const r = await supabase.from("notes").select();\n'
                                 'const s = await supabase.from("payments").select();\n'
                                 'const b = Buffer.from("hello");\n')
    found = {(f.message.split(" ")[0], f.path, f.line): f for f in supabase_rls.run(tmp_path, {"stacks": ["supabase"]})}
    by_line = {(f.path, f.line): f for f in found.values()}
    off = by_line[("supabase/migrations/001_init.sql", 6)]
    assert off.level == "certain" and "notes" in off.message
    assert {"resource": "notes", "subject": "anonymous", "perm": "read", "value": "allow"} in off.implies
    pol = by_line[("supabase/migrations/001_init.sql", 10)]
    assert {(i["subject"], i["perm"]) for i in pol.implies} == {("anonymous", "read"), ("signed_in", "read")}
    never = by_line[("supabase/migrations/001_init.sql", 12)]
    assert "todos" in never.message and never.implies == []
    unknown = by_line[("lib/db.ts", 2)]
    assert unknown.level == "hint" and "payments" in unknown.message
    assert ("lib/db.ts", 3) not in by_line
    assert ("supabase/migrations/001_init.sql", 9) not in by_line  # profiles has RLS on


def test_service_role_in_client_code(tmp_path):
    write(tmp_path, "components/Admin.tsx", '"use client";\nconst k = process.env.NEXT_PUBLIC_SUPABASE_SERVICE_ROLE_KEY;\n')
    write(tmp_path, "app/api/admin/route.ts", "const k = process.env.SUPABASE_SERVICE_ROLE_KEY;\n")
    found = supabase_rls.run(tmp_path, {"stacks": ["supabase", "nextjs"]})
    assert [(f.path, f.line, f.level) for f in found] == [("components/Admin.tsx", 2, "certain")]


def test_is_client_file():
    assert is_client_file("app/page.tsx", '"use client";', ["nextjs"]) is True
    assert is_client_file("app/api/x/route.ts", "", ["nextjs"]) is False
    assert is_client_file("src/App.tsx", "", ["vite"]) is True
    assert is_client_file("lib/util.ts", "", ["nextjs"]) is None


def test_local_imports_resolve_relative_and_alias(tmp_path):
    write(tmp_path, "lib/ai.ts", "export {}")
    route = write(tmp_path, "app/api/chat/route.ts", 'import { ask } from "@/lib/ai";\nimport x from "../../util";\n')
    write(tmp_path, "app/util/index.ts", "export {}")
    got = sorted(p.relative_to(tmp_path.resolve()).as_posix() for p in local_imports(tmp_path, route, route.read_text()))
    assert got == ["app/util/index.ts", "lib/ai.ts"]


def test_run_all_ids_and_skips(tmp_path):
    write(tmp_path, "package.json", json.dumps({"dependencies": {"react": "18"}}))
    write(tmp_path, ".env", f"VITE_KEY={OPENAI}\nVITE_OTHER={OPENAI}\n")
    out = probes.run_all(tmp_path)
    assert "secrets_exposed" in out["ran"]
    assert any(s["probe"] == "supabase_rls" for s in out["skipped"])
    ids = [f["id"] for f in out["findings"]]
    assert len(ids) == len(set(ids))
    assert "secrets_exposed:.env:1" in ids


def test_a_crashing_probe_is_reported_not_hidden(tmp_path, monkeypatch):
    def boom(root, stack):
        raise RuntimeError("bad regex")
    monkeypatch.setattr(secrets_exposed, "run", boom)
    out = probes.run_all(tmp_path)
    assert {"probe": "secrets_exposed", "reason": "crashed: RuntimeError('bad regex')"} in out["skipped"]
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_probes_stack_secrets_supabase.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'probes'`.

- [ ] **Step 3: Write `scripts/probes/util.py`**

```python
"""Small helpers shared by the probes."""
from __future__ import annotations

import re
from pathlib import Path

CODE = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte"}
SERVER_MARKERS = ("api/", "server/", "/server", "supabase/functions", "scripts/", "migrations/",
                  ".server.", "middleware", "route.")
IMPORT = re.compile(r"""(?:from\s+|require\(\s*|import\(\s*)['"]([^'"]+)['"]""")
_EXTS = (".ts", ".tsx", ".js", ".jsx", ".mjs")


def line_at(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def line_text(text: str, lineno: int) -> str:
    lines = text.splitlines()
    return lines[lineno - 1].strip() if 0 < lineno <= len(lines) else ""


def first_code_line(text: str) -> tuple[int, str]:
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip():
            return i, line.strip()
    return 1, ""


def is_client_file(relpath: str, text: str, stacks) -> bool | None:
    """True: runs in the browser. False: server-only. None: cannot tell."""
    p = relpath.lower()
    if any(m in p for m in SERVER_MARKERS) or "'use server'" in text or '"use server"' in text:
        return False
    if "'use client'" in text or '"use client"' in text:
        return True
    if "vite" in stacks and p.startswith("src/"):
        return True
    parts = p.split("/")
    if "components" in parts or "public" in parts:
        return True
    return None


def local_imports(root, path, text: str) -> list[Path]:
    """Files inside the project that `path` imports (relative, `@/` or `~/` specifiers)."""
    root, path = Path(root).resolve(), Path(path).resolve()
    out = []
    for spec in IMPORT.findall(text):
        if spec.startswith("."):
            bases = [path.parent / spec]
        elif spec.startswith(("@/", "~/")):
            bases = [root / "src" / spec[2:], root / spec[2:]]
        else:
            continue
        for base in bases:
            cands = [base] + [base.with_name(base.name + e) for e in _EXTS] + [base / f"index{e}" for e in _EXTS]
            hit = next((c for c in cands if c.is_file()), None)
            if hit:
                out.append(hit.resolve())
                break
    return out
```

- [ ] **Step 4: Write `scripts/probes/__init__.py`**

```python
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
                            "reason": "not used by this project: " + ", ".join(sorted(mod.APPLIES_TO))})
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
        base = f"{f.probe}:{f.path}:{f.line}"
        seen[base] += 1
        d["id"] = base if seen[base] == 1 else f"{base}#{seen[base]}"
        out.append(d)
    return {"stack": stack, "findings": out, "ran": ran, "skipped": skipped}
```

- [ ] **Step 5: Write the four stub modules (filled in Task 6)**

Each of `scripts/probes/firebase_rules.py`, `cors_wildcard.py`, `paid_api_unauthed.py`, `routes.py` gets this content, with `NAME` set to the file's own stem and `APPLIES_TO` as listed (firebase_rules: `{"firebase"}`; cors_wildcard: `None`; paid_api_unauthed: `{"nextjs", "express"}`; routes: `{"nextjs", "express"}`):
```python
"""Filled in by Task 6."""
NAME = "firebase_rules"
APPLIES_TO = {"firebase"}


def run(root, stack):
    return []
```

- [ ] **Step 6: Write `scripts/probes/secrets_exposed.py`**

```python
"""Secrets that anyone can read: browser-exposed env vars, keys written in
the code, and env files committed to git."""
from __future__ import annotations

import base64
import json
import re
from pathlib import Path, PurePosixPath

from common import CODE_EXTS, git_ls_files, iter_files, read_text, rel
from probes import Finding
from probes.util import first_code_line, line_at, line_text
from redact import find_secrets

NAME = "secrets_exposed"
APPLIES_TO = None
CLIENT_PREFIXES = ("NEXT_PUBLIC_", "VITE_", "EXPO_PUBLIC_", "REACT_APP_")
SENSITIVE_NAME = re.compile(r"SECRET|SERVICE_ROLE|PRIVATE|PASSWORD", re.I)
ENV_LINE = re.compile(r"^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$")
EXAMPLE_SUFFIXES = (".example", ".sample", ".template", ".dist")


def jwt_role(token: str) -> str | None:
    try:
        payload = token.split(".")[1]
        payload += "=" * (-len(payload) % 4)
        return json.loads(base64.urlsafe_b64decode(payload)).get("role")
    except Exception:
        return None


def sensitive(kind: str, raw: str) -> bool:
    """Anon/publishable keys are designed to be public; everything else is not."""
    if kind == "jwt":
        return jwt_role(raw) == "service_role"
    if kind == "stripe":
        return not raw.startswith("pk_")
    return kind != "assignment"


def _is_env(name: str) -> bool:
    return name.startswith(".env") and not name.endswith(EXAMPLE_SUFFIXES)


def run(root, stack) -> list[Finding]:
    root = Path(root).resolve()
    out: list[Finding] = []
    for p in iter_files(root):
        if not _is_env(p.name):
            continue
        r = rel(p, root)
        for i, line in enumerate(read_text(p).splitlines(), 1):
            m = ENV_LINE.match(line)
            if not m:
                continue
            name, val = m.group(1), m.group(2).strip().strip("'\"")
            prefix = next((x for x in CLIENT_PREFIXES if name.startswith(x)), None)
            if not prefix or not val:
                continue
            secret = any(sensitive(k, val[s:e]) for s, e, k in find_secrets(val))
            if secret or SENSITIVE_NAME.search(name):
                out.append(Finding(NAME, "certain", r, i, line.strip(),
                                   f"{name} starts with {prefix}, so it is bundled into the browser code where anyone can read it"))
    for p in iter_files(root, CODE_EXTS):
        text = read_text(p)
        r = rel(p, root)
        for s, e, kind in find_secrets(text):
            if not sensitive(kind, text[s:e]):
                continue
            ln = line_at(text, s)
            out.append(Finding(NAME, "certain", r, ln, line_text(text, ln),
                               f"A {kind} secret is written directly in the code"))
    for t in git_ls_files(root) or []:
        f = root / t
        if _is_env(PurePosixPath(t).name) and f.is_file():
            ln, snip = first_code_line(read_text(f))
            out.append(Finding(NAME, "certain", t, ln, snip,
                               "This environment file is tracked by git; pushing the repository publishes it"))
    return out
```

- [ ] **Step 7: Write `scripts/probes/supabase_rls.py`**

```python
"""Supabase row level security as the migrations describe it."""
from __future__ import annotations

import re
from pathlib import Path

from common import iter_files, read_text, rel
from probes import Finding
from probes.util import CODE, is_client_file, line_at, line_text

NAME = "supabase_rls"
APPLIES_TO = {"supabase"}
_T = r"(?:\"?public\"?\.)?\"?(\w+)\"?"
CREATE = re.compile(rf"create\s+table\s+(?:if\s+not\s+exists\s+)?{_T}", re.I)
RLS = re.compile(rf"alter\s+table\s+(?:if\s+exists\s+)?(?:only\s+)?{_T}\s+(enable|disable)\s+row\s+level\s+security", re.I)
POLICY = re.compile(rf"create\s+policy\s+(?:\"[^\"]*\"|\w+)\s+on\s+{_T}(?P<body>[^;]*);", re.I | re.S)
ALLOWS_ALL = re.compile(r"(?:using|with\s+check)\s*\(\s*true\s*\)", re.I)
FROM_CALL = re.compile(r"(?:supabase\w*|client|db)\s*\.from\(\s*['\"`](\w+)['\"`]\s*\)", re.I)
SERVICE_ROLE = re.compile(r"service_role", re.I)
OPEN = ("anonymous", "signed_in")


def _implies(table: str, read: bool, write: bool, subjects) -> list[dict]:
    out = []
    for s in subjects:
        if read:
            out.append({"resource": table, "subject": s, "perm": "read", "value": "allow"})
        if write:
            out.append({"resource": table, "subject": s, "perm": "write", "value": "allow"})
    return out


def _sql_files(root: Path) -> list[Path]:
    out = []
    for p in iter_files(root, {".sql"}):
        parts = rel(p, root).split("/")
        if "supabase" in parts or "migrations" in parts:
            out.append(p)
    return sorted(out, key=lambda q: rel(q, root))


def run(root, stack) -> list[Finding]:
    root = Path(root).resolve()
    out: list[Finding] = []
    tables: dict[str, dict] = {}
    for p in _sql_files(root):
        text, r = read_text(p), rel(p, root)
        events = sorted([(m.start(), "create", m) for m in CREATE.finditer(text)]
                        + [(m.start(), "rls", m) for m in RLS.finditer(text)]
                        + [(m.start(), "policy", m) for m in POLICY.finditer(text)], key=lambda e: e[0])
        for pos, kind, m in events:
            name = m.group(1).lower()
            ln = line_at(text, pos)
            snip = line_text(text, ln)
            t = tables.setdefault(name, {"created": None, "rls": None})
            if kind == "create":
                t["created"] = t["created"] or (r, ln, snip)
            elif kind == "rls":
                t["rls"] = (m.group(2).lower(), r, ln, snip)
            elif ALLOWS_ALL.search(m.group("body")):
                body = m.group("body").lower()
                cmd = re.search(r"\bfor\s+(all|select|insert|update|delete)\b", body)
                cmd = cmd.group(1) if cmd else "all"
                role = re.search(r"\bto\s+(\w+)", body)
                role = role.group(1) if role else "public"
                subjects = ("signed_in",) if role == "authenticated" else OPEN
                read, write = cmd in ("all", "select"), cmd != "select"
                perms = "/".join(x for x, on in (("read", read), ("write", write)) if on)
                who = "signed-in users" if role == "authenticated" else "everyone"
                out.append(Finding(NAME, "certain", r, ln, snip,
                                   f"A policy on table {name} lets {who} {perms} every row (using true)",
                                   _implies(name, read, write, subjects)))
    for name, t in sorted(tables.items()):
        if t["rls"] and t["rls"][0] == "disable":
            _, r, ln, snip = t["rls"]
            out.append(Finding(NAME, "certain", r, ln, snip,
                               f"Row level security is switched off for table {name}: anyone with the public "
                               "anon key can read and change every row", _implies(name, True, True, OPEN)))
        elif t["created"] and not t["rls"]:
            r, ln, snip = t["created"]
            out.append(Finding(NAME, "certain", r, ln, snip,
                               f"Table {name} is created without enabling row level security in the migrations "
                               "(if it was switched on in the Supabase dashboard, that is not visible here)"))
    defined = set(tables)
    for p in iter_files(root, CODE):
        text, r = read_text(p), rel(p, root)
        for m in FROM_CALL.finditer(text):
            name = m.group(1).lower()
            if name not in defined:
                defined.add(name)
                ln = line_at(text, m.start(1))
                out.append(Finding(NAME, "hint", r, ln, line_text(text, ln),
                                   f"Table {name} is used here but not defined in the migrations, so its row level "
                                   "security cannot be checked"))
        m = SERVICE_ROLE.search(text)
        if m:
            client = is_client_file(r, text, stack.get("stacks", []))
            if client is not False:
                ln = line_at(text, m.start())
                out.append(Finding(NAME, "certain" if client else "hint", r, ln, line_text(text, ln),
                                   "The service_role key, which bypasses every access rule, is referenced in code "
                                   "that may run in the browser"))
    return out
```

- [ ] **Step 8: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_probes_stack_secrets_supabase.py`
Expected: PASS.

- [ ] **Step 9: Commit**

```bash
git add scripts/probes/__init__.py scripts/probes/util.py scripts/probes/secrets_exposed.py scripts/probes/supabase_rls.py scripts/probes/firebase_rules.py scripts/probes/cors_wildcard.py scripts/probes/paid_api_unauthed.py scripts/probes/routes.py tests/test_probes_stack_secrets_supabase.py
git commit -m "feat: probe framework with stack detection, secrets and Supabase RLS probes"
```

---
### Task 6: Probes `firebase_rules`, `cors_wildcard`, `paid_api_unauthed`, `routes`

**Files:**
- Modify (replace the Task 5 stubs): `scripts/probes/firebase_rules.py`, `scripts/probes/cors_wildcard.py`, `scripts/probes/paid_api_unauthed.py`, `scripts/probes/routes.py`
- Test: `tests/test_probes_other.py`

**Interfaces:**
- Consumes: `probes.Finding`, `probes.util.{CODE, line_at, line_text, first_code_line, local_imports}` (Task 5); `common.iter_files`, `common.read_text`, `common.rel`.
- Produces: the four probe modules with the `NAME` / `APPLIES_TO` / `run(root, stack)` contract. `routes` findings have `level="fact"` and `message` like `"POST /api/chat"`, `"PAGE /dashboard"`, `"API /api/hello"`.

- [ ] **Step 1: Write the failing tests**

`tests/test_probes_other.py`:
```python
from probes import cors_wildcard, firebase_rules, paid_api_unauthed, routes


def write(root, rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


TEST_MODE = """rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.time < timestamp.date(2026, 11, 1);
    }
  }
}
"""


def test_firebase_test_mode_and_if_true(tmp_path):
    write(tmp_path, "firestore.rules", TEST_MODE)
    write(tmp_path, "storage.rules", "service firebase.storage {\n  match /b/{bucket}/o {\n    allow read: if true;\n  }\n}\n")
    write(tmp_path, "database.rules.json", '{\n  "rules": {\n    ".read": true,\n    ".write": "auth != null"\n  }\n}\n')
    found = sorted(firebase_rules.run(tmp_path, {"stacks": ["firebase"]}), key=lambda f: (f.path, f.line))
    assert [(f.path, f.line) for f in found] == [("database.rules.json", 3), ("firestore.rules", 5), ("storage.rules", 3)]
    test_mode = found[1]
    assert "test-mode" in test_mode.message
    assert {(i["subject"], i["perm"]) for i in test_mode.implies} == {
        ("anonymous", "read"), ("anonymous", "write"), ("signed_in", "read"), ("signed_in", "write")}
    assert all(i["resource"] == "*" for i in test_mode.implies)
    assert {i["perm"] for i in found[2].implies} == {"read"}


def test_firebase_safe_rules_are_quiet(tmp_path):
    write(tmp_path, "firestore.rules", "allow read, write: if request.auth != null && request.auth.uid == userId;\n")
    assert firebase_rules.run(tmp_path, {"stacks": ["firebase"]}) == []


def test_cors_wildcard_variants(tmp_path):
    write(tmp_path, "server.js", "const cors = require('cors');\napp.use(cors());\n")
    write(tmp_path, "api/h.ts", "res.setHeader('Access-Control-Allow-Origin', '*');\nres.setHeader('Access-Control-Allow-Credentials', 'true');\n")
    write(tmp_path, "b.ts", "app.use(cors({ origin: 'https://mine.example' }));\n")
    found = sorted(cors_wildcard.run(tmp_path, {"stacks": []}), key=lambda f: f.path)
    assert [(f.path, f.line) for f in found] == [("api/h.ts", 1), ("server.js", 2)]
    assert "credentials" in found[0].message and "credentials" not in found[1].message


def test_paid_api_without_auth_direct_and_through_helper(tmp_path):
    write(tmp_path, "app/api/summarize/route.ts",
          'import OpenAI from "openai";\n\nexport async function POST(req: Request) {\n  return Response.json({});\n}\n')
    write(tmp_path, "lib/ai.ts", 'import Anthropic from "@anthropic-ai/sdk";\nexport const ask = () => 1;\n')
    write(tmp_path, "app/api/chat/route.ts",
          'import { ask } from "@/lib/ai";\nexport async function POST() { return ask(); }\n')
    write(tmp_path, "app/api/safe/route.ts",
          'import OpenAI from "openai";\nexport async function POST() {\n  const { data } = await supabase.auth.getUser();\n}\n')
    found = sorted(paid_api_unauthed.run(tmp_path, {"stacks": ["nextjs"]}), key=lambda f: f.path)
    assert [(f.path, f.line, f.level) for f in found] == [
        ("app/api/chat/route.ts", 2, "hint"), ("app/api/summarize/route.ts", 3, "hint")]
    assert "anthropic" in found[0].message and "openai" in found[1].message


def test_paid_api_express(tmp_path):
    write(tmp_path, "server.js", 'const OpenAI = require("openai");\nconst app = express();\n'
                                 'app.post("/api/chat", async (req, res) => {});\n')
    [f] = paid_api_unauthed.run(tmp_path, {"stacks": ["express"]})
    assert (f.path, f.line) == ("server.js", 3)


def test_routes_next_and_express(tmp_path):
    write(tmp_path, "app/(marketing)/about/page.tsx", "export default function About() {}\n")
    write(tmp_path, "app/api/chat/route.ts", "\nexport async function POST() {}\nexport const GET = () => 1;\n")
    write(tmp_path, "pages/api/hello.ts", "export default function handler() {}\n")
    write(tmp_path, "pages/_app.tsx", "export default function App() {}\n")
    write(tmp_path, "server.js", "router.get('/health', (req, res) => res.send('ok'));\n")
    msgs = sorted(f.message for f in routes.run(tmp_path, {"stacks": ["nextjs", "express"]}))
    assert msgs == ["API /api/hello", "GET /api/chat", "GET /health", "PAGE /about", "POST /api/chat"]
    assert all(f.level == "fact" and f.snippet for f in routes.run(tmp_path, {"stacks": ["nextjs", "express"]}))


def test_routes_ignore_pages_dir_outside_next(tmp_path):
    write(tmp_path, "src/pages/Home.tsx", "export default function Home() {}\n")
    assert routes.run(tmp_path, {"stacks": ["express"]}) == []
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_probes_other.py`
Expected: FAIL — assertions fail because the stubs return `[]`.

- [ ] **Step 3: Write `scripts/probes/firebase_rules.py`**

```python
"""Firebase security rules that let anyone in."""
from __future__ import annotations

import re
from pathlib import Path

from common import iter_files, read_text, rel
from probes import Finding
from probes.util import line_at, line_text

NAME = "firebase_rules"
APPLIES_TO = {"firebase"}
ALLOW_TRUE = re.compile(r"allow\s+([\w\s,]+?)\s*:\s*if\s+true\s*;", re.I)
TEST_MODE = re.compile(r"allow\s+([\w\s,]+?)\s*:\s*if\s+request\.time\s*<\s*timestamp\.date\(", re.I)
RTDB = re.compile(r"\"\.(read|write)\"\s*:\s*(?:true|\"true\")")
READ_OPS = {"read", "get", "list"}
WRITE_OPS = {"write", "create", "update", "delete"}


def _implies(ops: str) -> list[dict]:
    names = {o.strip().lower() for o in ops.split(",")}
    out = []
    for perm, group in (("read", READ_OPS), ("write", WRITE_OPS)):
        if names & group:
            out += [{"resource": "*", "subject": s, "perm": perm, "value": "allow"} for s in ("anonymous", "signed_in")]
    return out


def run(root, stack) -> list[Finding]:
    root = Path(root).resolve()
    out: list[Finding] = []
    for p in iter_files(root):
        if not (p.suffix == ".rules" or p.name == "database.rules.json"):
            continue
        text, r = read_text(p), rel(p, root)
        for rx, msg in ((ALLOW_TRUE, "This rule lets anyone {ops} (if true)"),
                        (TEST_MODE, "This is the test-mode rule: anyone can {ops} until the date in it")):
            for m in rx.finditer(text):
                ln = line_at(text, m.start())
                out.append(Finding(NAME, "certain", r, ln, line_text(text, ln),
                                   msg.format(ops=" ".join(m.group(1).split())), _implies(m.group(1))))
        for m in RTDB.finditer(text):
            ln = line_at(text, m.start())
            out.append(Finding(NAME, "certain", r, ln, line_text(text, ln),
                               f"This Realtime Database rule lets anyone {m.group(1)} everything", _implies(m.group(1))))
    return out
```

- [ ] **Step 4: Write `scripts/probes/cors_wildcard.py`**

```python
"""Servers that accept calls from every website."""
from __future__ import annotations

import re
from pathlib import Path

from common import iter_files, read_text, rel
from probes import Finding
from probes.util import CODE, line_at, line_text

NAME = "cors_wildcard"
APPLIES_TO = None
RULES = [
    (re.compile(r"""origin\s*:\s*['"]\*['"]"""), "CORS allows every website ('*') to call this server"),
    (re.compile(r"""Access-Control-Allow-Origin['"]?\s*[:,]\s*['"]\*['"]""", re.I),
     "The Access-Control-Allow-Origin header is '*', so every website can call this server"),
    (re.compile(r"\bcors\(\s*\)"), "cors() with no options allows every website to call this server"),
]
CREDENTIALS = re.compile(r"credentials\s*:\s*true|Access-Control-Allow-Credentials['\"]?\s*[:,]\s*['\"]?true", re.I)


def run(root, stack) -> list[Finding]:
    root = Path(root).resolve()
    out: list[Finding] = []
    for p in iter_files(root, CODE | {".py"}):
        text, r = read_text(p), rel(p, root)
        extra = ", and it also accepts the visitor's cookies and credentials" if CREDENTIALS.search(text) else ""
        for rx, msg in RULES:
            for m in rx.finditer(text):
                ln = line_at(text, m.start())
                out.append(Finding(NAME, "certain", r, ln, line_text(text, ln), msg + extra))
    return out
```

- [ ] **Step 5: Write `scripts/probes/paid_api_unauthed.py`**

```python
"""Server endpoints that spend money on a paid API with no login check in sight."""
from __future__ import annotations

import re
from pathlib import Path

from common import iter_files, read_text, rel
from probes import Finding
from probes.util import CODE, line_at, line_text, local_imports

NAME = "paid_api_unauthed"
APPLIES_TO = {"nextjs", "express"}
PAID = re.compile(
    r"""(?:from\s+|require\(\s*)['"](openai|@anthropic-ai/sdk|replicate|stripe|twilio|resend"""
    r"""|@google/generative-ai|@google/genai|groq-sdk|cohere-ai|elevenlabs|@elevenlabs/elevenlabs-js)['"]"""
    r"""|https://api\.(openai|anthropic|replicate|stripe|elevenlabs)\.(?:com|io)""")
AUTH = re.compile(
    r"getUser\(|getSession\(|getServerSession\(|\bauth\(\)|currentUser\(|verifyIdToken\(|jwt\.verify\("
    r"|requireAuth|isAuthenticated|withAuth|clerkClient|getAuth\(|req\.user\b|supabase\.auth\."
    r"|passport\.authenticate|ensureLoggedIn|authMiddleware", re.I)
NEXT_ROUTE = re.compile(r"(?:^|/)(?:app/(?:.+/)?route|pages/api/.+)\.(?:t|j)sx?$")
EXPRESS = re.compile(r"\b(?:app|router)\.(?:get|post|put|patch|delete|all)\(")
HANDLER = re.compile(
    r"export\s+(?:async\s+)?function\s+(?:GET|POST|PUT|PATCH|DELETE)\b"
    r"|export\s+const\s+(?:GET|POST|PUT|PATCH|DELETE)\b|export\s+default\s+(?:async\s+)?function"
    r"|\b(?:app|router)\.(?:get|post|put|patch|delete|all)\(|['\"]use server['\"]")


def _service(m: re.Match) -> str:
    name = next(g for g in m.groups() if g)
    return name.split("/")[-1].replace("@", "").replace("-sdk", "").replace("sdk", "").strip("-") or name


def run(root, stack) -> list[Finding]:
    root = Path(root).resolve()
    out: list[Finding] = []
    for p in iter_files(root, CODE):
        r, text = rel(p, root), read_text(p)
        is_endpoint = NEXT_ROUTE.search(r) or EXPRESS.search(text) or "use server" in text
        if not is_endpoint or AUTH.search(text):
            continue
        m = PAID.search(text)
        if not m:
            for dep in local_imports(root, p, text):
                m = PAID.search(read_text(dep))
                if m:
                    break
        if not m:
            continue
        h = HANDLER.search(text)
        ln = line_at(text, h.start()) if h else 1
        service = m.group(1) or m.group(2)
        label = "anthropic" if "anthropic" in service else _service(m)
        out.append(Finding(NAME, "hint", r, ln, line_text(text, ln),
                           f"This server endpoint calls a paid service ({label}) and no login check was found in the file"))
    return out
```

- [ ] **Step 6: Write `scripts/probes/routes.py`**

```python
"""The pages and API endpoints the project defines (facts for the app map and paths)."""
from __future__ import annotations

import re
from pathlib import Path

from common import iter_files, read_text, rel
from probes import Finding
from probes.util import CODE, first_code_line, line_at, line_text

NAME = "routes"
APPLIES_TO = {"nextjs", "express"}
APP_ROUTE = re.compile(r"(?:^|/)app/(?P<dir>(?:.+/)?)route\.(?:t|j)sx?$")
APP_PAGE = re.compile(r"(?:^|/)app/(?P<dir>(?:.+/)?)page\.(?:t|j)sx?$")
PAGES = re.compile(r"(?:^|/)pages/(?P<path>.+)\.(?:t|j)sx?$")
METHOD = re.compile(r"export\s+(?:async\s+)?(?:function|const)\s+(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)\b")
EXPRESS = re.compile(r"""\b(?:app|router)\.(get|post|put|patch|delete|all)\(\s*['"`]([^'"`]+)['"`]""")


def _url(directory: str) -> str:
    parts = [s for s in directory.strip("/").split("/") if s and not (s.startswith("(") and s.endswith(")"))]
    return "/" + "/".join(parts)


def run(root, stack) -> list[Finding]:
    root = Path(root).resolve()
    next_js = "nextjs" in stack.get("stacks", [])
    out: list[Finding] = []
    for p in iter_files(root, CODE):
        r, text = rel(p, root), read_text(p)
        if next_js and (m := APP_ROUTE.search(r)):
            for mm in METHOD.finditer(text):
                ln = line_at(text, mm.start())
                out.append(Finding(NAME, "fact", r, ln, line_text(text, ln), f"{mm.group(1)} {_url(m.group('dir'))}"))
            continue
        if next_js and (m := APP_PAGE.search(r)):
            ln, snip = first_code_line(text)
            out.append(Finding(NAME, "fact", r, ln, snip, f"PAGE {_url(m.group('dir'))}"))
            continue
        if next_js and (m := PAGES.search(r)):
            if r.split("/")[-1].startswith("_"):
                continue
            path = m.group("path")
            path = "" if path == "index" else path[:-len("/index")] if path.endswith("/index") else path
            kind = "API" if path == "api" or path.startswith("api/") else "PAGE"
            ln, snip = first_code_line(text)
            out.append(Finding(NAME, "fact", r, ln, snip, f"{kind} /{path}"))
            continue
        for mm in EXPRESS.finditer(text):
            ln = line_at(text, mm.start())
            out.append(Finding(NAME, "fact", r, ln, line_text(text, ln), f"{mm.group(1).upper()} {mm.group(2)}"))
    return out
```

- [ ] **Step 7: Run all probe tests**

Run: `python3 -m pytest tests/test_probes_other.py tests/test_probes_stack_secrets_supabase.py`
Expected: PASS.

- [ ] **Step 8: Commit**

```bash
git add scripts/probes/firebase_rules.py scripts/probes/cors_wildcard.py scripts/probes/paid_api_unauthed.py scripts/probes/routes.py tests/test_probes_other.py
git commit -m "feat: Firebase rules, CORS, paid-API and route probes"
```

---
### Task 7: Ledger format — `validate` and `merge`

**Files:**
- Create: `scripts/ledger.py`
- Test: `tests/test_ledger.py`

**Interfaces:**
- Consumes: `common.norm_ws` (Task 1).
- Produces:
  - Constants `STATUSES, TYPES, QUESTIONS, EVIDENCE_KINDS, LANES, NODE_KINDS, SUBJECTS, PERMS` (tuples, values exactly as in Global Constraints; `LANES = ("browser", "server", "storage")`; `NODE_KINDS = ("page", "route", "function", "database", "storage", "third_party", "client")`; `PERMS = ("allow", "deny", "unknown")`).
  - `ledger.LedgerError(problems: list[str])` with `.problems`.
  - `ledger.validate(led: dict) -> None` — raises `LedgerError` listing **every** problem. `map`, `access`, `paths`, `compromises` are optional (missing = empty); `evidence` and `promises` are required.
  - `ledger.normalise(led: dict) -> dict` — a copy with every optional section present (`map: {"nodes": [], "edges": []}`, `access: {"resources": []}`, `paths: []`, `compromises: []`).
  - `ledger.merge(parts: list[dict]) -> dict` — parts hold only `evidence`, `promises`, `compromises`; ids get a `p<N>_` prefix; a promise whose first source quote and type repeat an earlier one is dropped when the status agrees and kept with `conflict_with` on both sides when it does not; a part carrying non-empty `map`/`access`/`paths` is rejected.

Ledger shape (from spec §9.1): `evidence` is `{id: {kind: transcript, session, msg_id, quote} | {kind: code, path, line(int), snippet} | {kind: probe, finding_id}}`; each promise has `id, type, question, plain, source[transcript ids], status, verdict_plain, verdict_dev, evidence[ids], fix_prompt?`; each compromise has `id, error(transcript id), change[transcript ids], bypassed, still_present(bool), now[code/probe ids], breaks(promise id|null)`; `map.nodes[]` have `id, lane, kind, label, holds[], paid(bool), evidence[]`; `map.edges[]` have `from, to, carries, risk(str|null), evidence[]`; `access.resources[]` have `name, cells{subject: {read, write, evidence[]}}, required_by(promise id|null)`; `paths[]` have `action, steps[{label, evidence(one id), warning(str|null)}]`.

- [ ] **Step 1: Write the failing tests**

`tests/test_ledger.py`:
```python
import copy

import pytest

import ledger


def minimal():
    return {
        "evidence": {
            "E1": {"kind": "transcript", "session": "s1", "msg_id": "m1", "quote": "只有我自己能看到账目"},
            "E2": {"kind": "code", "path": "supabase/migrations/001.sql", "line": 6,
                   "snippet": "alter table notes disable row level security;"},
            "E3": {"kind": "probe", "finding_id": "supabase_rls:supabase/migrations/001.sql:6"},
            "E4": {"kind": "transcript", "session": "s1", "msg_id": "m2", "quote": "new row violates"},
            "E5": {"kind": "transcript", "session": "s1", "msg_id": "m3", "quote": "disable row level security"},
        },
        "promises": [{"id": "P1", "type": "user_requirement", "question": "who_can_see",
                      "plain": "只有我自己能看到账目", "source": ["E1"], "status": "broken",
                      "verdict_plain": "前门锁了，后窗开着", "verdict_dev": "RLS disabled on notes",
                      "evidence": ["E2", "E3"], "fix_prompt": "Re-enable RLS on notes and add an owner policy."}],
        "compromises": [{"id": "C1", "error": "E4", "change": ["E5"], "bypassed": "rls",
                         "still_present": True, "now": ["E2"], "breaks": "P1"}],
        "map": {"nodes": [{"id": "db", "lane": "storage", "kind": "database", "label": "Supabase",
                           "holds": ["notes"], "paid": False, "evidence": ["E2"]},
                          {"id": "web", "lane": "browser", "kind": "page", "label": "Home page",
                           "holds": [], "paid": False, "evidence": ["E2"]}],
                "edges": [{"from": "web", "to": "db", "carries": "notes", "risk": "anyone can read",
                           "evidence": ["E3"]}]},
        "access": {"resources": [{"name": "notes", "required_by": "P1", "cells": {
            "anonymous": {"read": "allow", "write": "allow", "evidence": ["E3"]},
            "owner": {"read": "allow", "write": "allow", "evidence": ["E2"]}}}]},
        "paths": [{"action": "Save a note", "steps": [{"label": "supabase.insert()", "evidence": "E2", "warning": None}]}],
    }


def test_minimal_ledger_is_valid():
    ledger.validate(minimal())


def test_optional_sections_may_be_missing():
    led = minimal()
    for key in ("map", "access", "paths", "compromises"):
        del led[key]
    led["promises"][0]["status"] = "unknown"
    ledger.validate(led)
    norm = ledger.normalise(led)
    assert norm["map"] == {"nodes": [], "edges": []} and norm["paths"] == [] and norm["compromises"] == []


@pytest.mark.parametrize("mutate, needle", [
    (lambda L: L["promises"][0].update(status="maybe"), "status"),
    (lambda L: L["promises"][0].update(type="wish"), "type"),
    (lambda L: L["promises"][0].update(question="vibes"), "question"),
    (lambda L: L["promises"][0].update(status="pending"), "pending is only for type deferred"),
    (lambda L: L["promises"][0].update(source=[]), "source must list"),
    (lambda L: L["promises"][0].update(source=["E2"]), "must be transcript"),
    (lambda L: L["promises"][0].update(evidence=["E99"]), "unknown evidence id E99"),
    (lambda L: L["promises"][0].pop("verdict_plain"), "missing verdict_plain"),
    (lambda L: L["promises"].append(copy.deepcopy(L["promises"][0])), "duplicated"),
    (lambda L: L["evidence"]["E2"].update(line="6"), "line must be an integer"),
    (lambda L: L["evidence"]["E1"].pop("quote"), "missing quote"),
    (lambda L: L["evidence"].update(E9={"kind": "rumour"}), "kind must be one of"),
    (lambda L: L["compromises"][0].update(breaks="P9"), "breaks"),
    (lambda L: L["compromises"][0].update(still_present="yes"), "still_present"),
    (lambda L: L["compromises"][0].update(now=["E1"]), "must be code or probe"),
    (lambda L: L["map"]["nodes"][0].update(lane="cloud"), "lane"),
    (lambda L: L["map"]["edges"][0].update(to="nowhere"), "unknown node"),
    (lambda L: L["access"]["resources"][0]["cells"].update(admin={"read": "allow", "write": "deny", "evidence": []}), "subject"),
    (lambda L: L["access"]["resources"][0]["cells"]["owner"].update(read="yes"), "read"),
    (lambda L: L["paths"][0]["steps"][0].update(evidence=["E2"]), "one evidence id"),
])
def test_each_problem_is_reported(mutate, needle):
    led = minimal()
    mutate(led)
    with pytest.raises(ledger.LedgerError) as exc:
        ledger.validate(led)
    assert any(needle in p for p in exc.value.problems), exc.value.problems


def test_all_problems_are_listed_at_once():
    led = minimal()
    led["promises"][0]["status"] = "maybe"
    led["map"]["nodes"][0]["lane"] = "cloud"
    with pytest.raises(ledger.LedgerError) as exc:
        ledger.validate(led)
    assert len(exc.value.problems) >= 2


def test_not_an_object():
    with pytest.raises(ledger.LedgerError):
        ledger.validate([])


def part(n_quote="只有我自己能看到账目", status="broken"):
    return {"evidence": {"E1": {"kind": "transcript", "session": "s", "msg_id": "m1", "quote": n_quote},
                         "E2": {"kind": "code", "path": "a.sql", "line": 1, "snippet": "x"}},
            "promises": [{"id": "P1", "type": "user_requirement", "question": "who_can_see", "plain": "p",
                          "source": ["E1"], "status": status, "verdict_plain": "v", "verdict_dev": "d",
                          "evidence": ["E2"]}],
            "compromises": []}


def test_merge_prefixes_ids_and_keeps_distinct_promises():
    out = ledger.merge([part("quote one"), part("quote two")])
    assert [p["id"] for p in out["promises"]] == ["p1_P1", "p2_P1"]
    assert set(out["evidence"]) == {"p1_E1", "p1_E2", "p2_E1", "p2_E2"}
    assert out["promises"][1]["source"] == ["p2_E1"]
    ledger.validate(out)


def test_merge_drops_exact_duplicates_and_flags_conflicts():
    same = ledger.merge([part(), part()])
    assert len(same["promises"]) == 1
    clash = ledger.merge([part(status="broken"), part(status="kept")])
    assert len(clash["promises"]) == 2
    assert clash["promises"][0]["conflict_with"] == ["p2_P1"]
    assert clash["promises"][1]["conflict_with"] == ["p1_P1"]


def test_merge_remaps_compromise_breaks_to_the_kept_duplicate():
    a, b = part(), part()
    b["evidence"]["E3"] = {"kind": "transcript", "session": "s", "msg_id": "m2", "quote": "error text"}
    b["compromises"] = [{"id": "C1", "error": "E3", "change": ["E1"], "bypassed": "rls",
                         "still_present": True, "now": ["E2"], "breaks": "P1"}]
    out = ledger.merge([a, b])
    assert out["compromises"][0]["breaks"] == "p1_P1" and out["compromises"][0]["id"] == "p2_C1"


def test_merge_rejects_code_sections_in_parts():
    p = part()
    p["map"] = {"nodes": [{"id": "x"}], "edges": []}
    with pytest.raises(ledger.LedgerError) as exc:
        ledger.merge([p])
    assert any("map/access/paths" in s for s in exc.value.problems)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_ledger.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'ledger'`.

- [ ] **Step 3: Write `scripts/ledger.py`**

```python
"""The ledger: the only contract between the model and the scripts."""
from __future__ import annotations

import copy

from common import norm_ws

STATUSES = ("kept", "broken", "partial", "pending", "unknown")
TYPES = ("user_requirement", "ai_claim", "deferred")
QUESTIONS = ("where_data", "what_costs", "who_can_see", "what_breaks", "open_debts")
EVIDENCE_KINDS = ("transcript", "code", "probe")
LANES = ("browser", "server", "storage")
NODE_KINDS = ("page", "route", "function", "database", "storage", "third_party", "client")
SUBJECTS = ("anonymous", "signed_in", "owner")
PERMS = ("allow", "deny", "unknown")
_EVIDENCE_FIELDS = {"transcript": ("session", "msg_id", "quote"), "code": ("path", "line", "snippet"),
                    "probe": ("finding_id",)}
_PROMISE_FIELDS = ("type", "question", "plain", "source", "status", "verdict_plain", "verdict_dev", "evidence")
_COMPROMISE_FIELDS = ("id", "error", "change", "bypassed", "still_present", "now")


class LedgerError(Exception):
    def __init__(self, problems: list[str]):
        super().__init__("\n".join(problems))
        self.problems = problems


def normalise(led: dict) -> dict:
    out = copy.deepcopy(led)
    out.setdefault("compromises", [])
    out.setdefault("map", {})
    out["map"].setdefault("nodes", [])
    out["map"].setdefault("edges", [])
    out.setdefault("access", {})
    out["access"].setdefault("resources", [])
    out.setdefault("paths", [])
    return out


def validate(led: dict) -> None:
    if not isinstance(led, dict):
        raise LedgerError(["the ledger must be a JSON object"])
    p: list[str] = []
    ev = led.get("evidence")
    if not isinstance(ev, dict):
        p.append("evidence: must be an object mapping ids to evidence")
        ev = {}
    for eid, e in ev.items():
        kind = e.get("kind") if isinstance(e, dict) else None
        if kind not in EVIDENCE_KINDS:
            p.append(f"evidence {eid}: kind must be one of {', '.join(EVIDENCE_KINDS)}")
            continue
        for f in _EVIDENCE_FIELDS[kind]:
            if f not in e:
                p.append(f"evidence {eid}: missing {f}")
        if kind == "code" and "line" in e and not isinstance(e["line"], int):
            p.append(f"evidence {eid}: line must be an integer")

    def refs(where: str, ids, kinds=None) -> None:
        if not isinstance(ids, list):
            p.append(f"{where}: must be a list of evidence ids")
            return
        for i in ids:
            if i not in ev:
                p.append(f"{where}: unknown evidence id {i}")
            elif kinds and ev[i].get("kind") not in kinds:
                p.append(f"{where}: evidence {i} must be {' or '.join(kinds)}")

    promises = led.get("promises")
    if not isinstance(promises, list):
        p.append("promises: must be a list")
        promises = []
    pids: set = set()
    for x in promises:
        pid = x.get("id")
        where = f"promise {pid}"
        if not pid or pid in pids:
            p.append(f"{where}: id missing or duplicated")
        pids.add(pid)
        for f in _PROMISE_FIELDS:
            if f not in x:
                p.append(f"{where}: missing {f}")
        if x.get("type") not in TYPES:
            p.append(f"{where}: type must be one of {', '.join(TYPES)}")
        if x.get("question") not in QUESTIONS:
            p.append(f"{where}: question must be one of {', '.join(QUESTIONS)}")
        if x.get("status") not in STATUSES:
            p.append(f"{where}: status must be one of {', '.join(STATUSES)}")
        if x.get("status") == "pending" and x.get("type") != "deferred":
            p.append(f"{where}: status pending is only for type deferred")
        if "source" in x and not x["source"]:
            p.append(f"{where}: source must list at least one transcript evidence id")
        refs(f"{where} source", x.get("source", []), ("transcript",))
        refs(f"{where} evidence", x.get("evidence", []))

    for c in led.get("compromises", []):
        where = f"compromise {c.get('id')}"
        for f in _COMPROMISE_FIELDS:
            if f not in c:
                p.append(f"{where}: missing {f}")
        refs(f"{where} error", [c["error"]] if c.get("error") else [], ("transcript",))
        refs(f"{where} change", c.get("change", []), ("transcript",))
        refs(f"{where} now", c.get("now", []), ("code", "probe"))
        if c.get("breaks") is not None and c.get("breaks") not in pids:
            p.append(f"{where}: breaks refers to unknown promise {c.get('breaks')}")
        if "still_present" in c and not isinstance(c["still_present"], bool):
            p.append(f"{where}: still_present must be true or false")

    m = led.get("map", {})
    nids: set = set()
    for n in m.get("nodes", []):
        where = f"map node {n.get('id')}"
        if not n.get("id") or n["id"] in nids:
            p.append(f"{where}: id missing or duplicated")
        nids.add(n.get("id"))
        if n.get("lane") not in LANES:
            p.append(f"{where}: lane must be one of {', '.join(LANES)}")
        if n.get("kind") not in NODE_KINDS:
            p.append(f"{where}: kind must be one of {', '.join(NODE_KINDS)}")
        if not n.get("label"):
            p.append(f"{where}: missing label")
        if not isinstance(n.get("paid", False), bool):
            p.append(f"{where}: paid must be true or false")
        refs(f"{where} evidence", n.get("evidence", []))
    for e in m.get("edges", []):
        where = f"map edge {e.get('from')}->{e.get('to')}"
        for end in ("from", "to"):
            if e.get(end) not in nids:
                p.append(f"{where}: unknown node {e.get(end)}")
        refs(f"{where} evidence", e.get("evidence", []))

    for r in led.get("access", {}).get("resources", []):
        where = f"access {r.get('name')}"
        if not r.get("name"):
            p.append(f"{where}: missing name")
        for subject, cell in (r.get("cells") or {}).items():
            if subject not in SUBJECTS:
                p.append(f"{where}: subject {subject} must be one of {', '.join(SUBJECTS)}")
                continue
            for perm in ("read", "write"):
                if cell.get(perm, "unknown") not in PERMS:
                    p.append(f"{where} {subject}: {perm} must be one of {', '.join(PERMS)}")
            refs(f"{where} {subject} evidence", cell.get("evidence", []))
        if r.get("required_by") is not None and r.get("required_by") not in pids:
            p.append(f"{where}: required_by refers to unknown promise {r.get('required_by')}")

    for path in led.get("paths", []):
        where = f"path {path.get('action')}"
        if not path.get("action"):
            p.append(f"{where}: missing action")
        for st in path.get("steps", []):
            if not st.get("label"):
                p.append(f"{where}: a step is missing its label")
            if not isinstance(st.get("evidence"), str):
                p.append(f"{where} step {st.get('label')}: evidence must be one evidence id")
            else:
                refs(f"{where} step {st.get('label')}", [st["evidence"]])

    if p:
        raise LedgerError(p)


def merge(parts: list[dict]) -> dict:
    """Combine chunk ledgers (promises + compromises only) into one ledger."""
    problems = [f"part {n}: map/access/paths belong in the main ledger, not in a part"
                for n, part in enumerate(parts, 1)
                if part.get("map", {}).get("nodes") or part.get("map", {}).get("edges")
                or part.get("access", {}).get("resources") or part.get("paths")]
    if problems:
        raise LedgerError(problems)
    out = normalise({"evidence": {}, "promises": []})
    seen: dict[tuple, dict] = {}
    for n, part in enumerate(parts, 1):
        validate(part)
        pre = f"p{n}_"
        ren = lambda i: pre + i
        for eid, e in part["evidence"].items():
            out["evidence"][ren(eid)] = copy.deepcopy(e)
        idmap: dict[str, str] = {}
        for x in part["promises"]:
            y = copy.deepcopy(x)
            y["id"] = ren(x["id"])
            y["source"] = [ren(i) for i in x["source"]]
            y["evidence"] = [ren(i) for i in x["evidence"]]
            key = (x["type"], norm_ws(part["evidence"][x["source"][0]]["quote"]))
            prev = seen.get(key)
            if prev is not None and prev["status"] == y["status"]:
                idmap[x["id"]] = prev["id"]
                continue
            if prev is not None:
                prev.setdefault("conflict_with", []).append(y["id"])
                y.setdefault("conflict_with", []).append(prev["id"])
            else:
                seen[key] = y
            idmap[x["id"]] = y["id"]
            out["promises"].append(y)
        for c in part.get("compromises", []):
            y = copy.deepcopy(c)
            y["id"] = ren(c["id"])
            y["error"] = ren(c["error"])
            y["change"] = [ren(i) for i in c["change"]]
            y["now"] = [ren(i) for i in c["now"]]
            y["breaks"] = idmap.get(c.get("breaks")) if c.get("breaks") else None
            out["compromises"].append(y)
    validate(out)
    return out
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_ledger.py`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/ledger.py tests/test_ledger.py
git commit -m "feat: ledger validation and chunk merging"
```

---
### Task 8: Evidence checks

**Files:**
- Create: `scripts/verify.py` (evidence functions; Task 9 adds ledger verification)
- Test: `tests/test_verify_evidence.py`

**Interfaces:**
- Consumes: `common.is_within`, `common.norm_ws`, `common.read_text`, `common.rel` (Task 1).
- Produces:
  - `verify.TOLERANCE = 3`, `verify.MIN_QUOTE = 4`
  - `verify.find_snippet_lines(lines: list[str], snippet: str) -> list[int]` — 1-based start lines of every place the whitespace-normalised snippet occurs (blank lines ignored; tries a window of k non-blank lines, then k+1).
  - `verify.check_transcript(e: dict, index: dict[str, dict]) -> dict` — `{"ok": True, "ts", "session", "role", "msg_kind"}` or `{"ok": False, "reason"}`.
  - `verify.check_code(e: dict, root) -> dict` — `{"ok": True, "path"(normalised), "line", "line_corrected": bool, "reason"?}` or `{"ok": False, "reason"}`.
  - `verify.check_probe(e: dict, findings: dict[str, dict], root) -> dict` — copies `probe, level, message, path, line, snippet` from the finding, then re-checks the snippet with `check_code`.

- [ ] **Step 1: Write the failing tests**

`tests/test_verify_evidence.py`:
```python
import unicodedata

import verify

INDEX = {"m1": {"id": "m1", "session": "s1", "ts": "2026-09-12T09:01:00Z", "role": "user", "kind": "text",
                "text": "帮我做一个笔记应用。只有我自己能看到我的笔记。\nThanks!"}}


def write(root, rel, text, newline="\n"):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.replace("\n", newline).encode("utf-8"))
    return p


def test_transcript_quote_found_and_timestamp_taken_from_digest():
    out = verify.check_transcript({"msg_id": "m1", "session": "wrong", "quote": "只有我自己能看到我的笔记",
                                   "ts": "1999-01-01"}, INDEX)
    assert out == {"ok": True, "ts": "2026-09-12T09:01:00Z", "session": "s1", "role": "user", "msg_kind": "text"}


def test_transcript_quote_whitespace_insensitive():
    assert verify.check_transcript({"msg_id": "m1", "quote": "我的笔记。 Thanks!"}, INDEX)["ok"]


def test_quote_matches_across_unicode_normalisation():
    index = {"m": {**INDEX["m1"], "text": unicodedata.normalize("NFC", "café is open")}}
    quote = unicodedata.normalize("NFD", "café is open")
    assert verify.check_transcript({"msg_id": "m", "quote": quote}, index)["ok"]


def test_transcript_failures():
    assert verify.check_transcript({"msg_id": "nope", "quote": "abcdef"}, INDEX)["reason"].startswith("message id not found")
    assert "shorter" in verify.check_transcript({"msg_id": "m1", "quote": "我的"}, INDEX)["reason"]
    assert "word for word" in verify.check_transcript({"msg_id": "m1", "quote": "我从来没说过这句话"}, INDEX)["reason"]


CODE = "line one\n\nconst a = 1;\nconst b = 2;\n\n\nconst c = 3;\nconst a = 1;\n"


def test_code_snippet_near_given_line(tmp_path):
    write(tmp_path, "src/x.ts", CODE)
    out = verify.check_code({"path": "src/x.ts", "line": 5, "snippet": "const b = 2;"}, tmp_path)
    assert out["ok"] and out["line"] == 4 and out["line_corrected"] is False and out["path"] == "src/x.ts"


def test_code_snippet_far_but_unique_is_corrected(tmp_path):
    write(tmp_path, "src/x.ts", CODE)
    out = verify.check_code({"path": "src/x.ts", "line": 40, "snippet": "const c = 3;"}, tmp_path)
    assert out["ok"] and out["line"] == 7 and out["line_corrected"] is True and "corrected" in out["reason"]


def test_code_snippet_repeated_far_away_fails(tmp_path):
    write(tmp_path, "src/x.ts", CODE)
    out = verify.check_code({"path": "src/x.ts", "line": 40, "snippet": "const a = 1;"}, tmp_path)
    assert not out["ok"] and "occurs 2 times" in out["reason"]


def test_multi_line_snippet_across_a_blank_line(tmp_path):
    write(tmp_path, "src/x.ts", CODE)
    out = verify.check_code({"path": "src/x.ts", "line": 4, "snippet": "const b = 2;\nconst c = 3;"}, tmp_path)
    assert out["ok"] and out["line"] == 4


def test_code_evidence_with_crlf_file(tmp_path):
    write(tmp_path, "a.sql", "create table t (id int);\nalter table t disable row level security;\n", newline="\r\n")
    assert verify.check_code({"path": "a.sql", "line": 2, "snippet": "alter table t disable row level security;"}, tmp_path)["ok"]


def test_code_failures(tmp_path):
    write(tmp_path, "a.ts", "x\n")
    outside = tmp_path.parent / "outside.ts"
    outside.write_text("x\n")
    assert verify.check_code({"path": "../outside.ts", "line": 1, "snippet": "x"}, tmp_path)["reason"] == "path is outside the project"
    assert verify.check_code({"path": str(outside), "line": 1, "snippet": "x"}, tmp_path)["reason"] == "path is outside the project"
    assert verify.check_code({"path": "missing.ts", "line": 1, "snippet": "x"}, tmp_path)["reason"] == "file not found"
    assert verify.check_code({"path": "a.ts", "line": 1, "snippet": "   "}, tmp_path)["reason"] == "snippet is empty"
    assert verify.check_code({"path": "a.ts", "line": 1, "snippet": "y"}, tmp_path)["reason"] == "snippet not found in the file"


def test_symlink_pointing_outside_is_rejected(tmp_path):
    secret = tmp_path.parent / "elsewhere.txt"
    secret.write_text("token\n")
    root = tmp_path / "app"
    root.mkdir()
    (root / "link.txt").symlink_to(secret)
    assert not verify.check_code({"path": "link.txt", "line": 1, "snippet": "token"}, root)["ok"]


def test_probe_evidence(tmp_path):
    write(tmp_path, "a.sql", "alter table t disable row level security;\n")
    finding = {"id": "supabase_rls:a.sql:1", "probe": "supabase_rls", "level": "certain", "path": "a.sql",
               "line": 1, "snippet": "alter table t disable row level security;", "message": "RLS off", "implies": []}
    good = verify.check_probe({"finding_id": finding["id"]}, {finding["id"]: finding}, tmp_path)
    assert good["ok"] and good["probe"] == "supabase_rls" and good["message"] == "RLS off"
    assert verify.check_probe({"finding_id": "nope"}, {}, tmp_path)["reason"] == "probe finding not found in probes.json"
    write(tmp_path, "a.sql", "alter table t enable row level security;\n")
    stale = verify.check_probe({"finding_id": finding["id"]}, {finding["id"]: finding}, tmp_path)
    assert not stale["ok"] and stale["reason"].startswith("the code changed since the probe ran")


def test_find_snippet_lines():
    lines = ["a b", "", "c", "a b"]
    assert verify.find_snippet_lines(lines, "a  b") == [1, 4]
    assert verify.find_snippet_lines(lines, "b\nc") == [1]
    assert verify.find_snippet_lines(lines, "") == []
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_verify_evidence.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'verify'`.

- [ ] **Step 3: Write `scripts/verify.py` (evidence part)**

```python
"""Check every piece of evidence in a ledger against the digest, the code and
the probes; downgrade or drop whatever cannot be shown to be true."""
from __future__ import annotations

import os
from pathlib import Path

from common import is_within, norm_ws, read_text, rel

TOLERANCE = 3
MIN_QUOTE = 4


def find_snippet_lines(lines: list[str], snippet: str) -> list[int]:
    target = norm_ws(snippet)
    if not target:
        return []
    rows = [(n, norm_ws(text)) for n, text in enumerate(lines, 1)]
    rows = [(n, text) for n, text in rows if text]
    k = max(1, sum(1 for line in snippet.splitlines() if line.strip()))
    for size in (k, k + 1):
        hits = [rows[i][0] for i in range(len(rows))
                if target in " ".join(text for _, text in rows[i:i + size])]
        if hits:
            return hits
    return []


def check_transcript(e: dict, index: dict) -> dict:
    rec = index.get(e.get("msg_id"))
    if rec is None:
        return {"ok": False, "reason": "message id not found in the conversation digest"}
    quote = norm_ws(e.get("quote", ""))
    if len(quote) < MIN_QUOTE:
        return {"ok": False, "reason": f"quote is shorter than {MIN_QUOTE} characters"}
    if quote not in norm_ws(rec["text"]):
        return {"ok": False, "reason": "quote is not in that message word for word"}
    return {"ok": True, "ts": rec["ts"], "session": rec["session"], "role": rec["role"], "msg_kind": rec["kind"]}


def check_code(e: dict, root) -> dict:
    root = Path(root).resolve()
    raw = str(e.get("path") or "")
    path = Path(raw) if os.path.isabs(raw) else root / raw
    if not raw or not is_within(path, root):
        return {"ok": False, "reason": "path is outside the project"}
    if not path.is_file():
        return {"ok": False, "reason": "file not found"}
    snippet = e.get("snippet") or ""
    if not norm_ws(snippet):
        return {"ok": False, "reason": "snippet is empty"}
    hits = find_snippet_lines(read_text(path).splitlines(), snippet)
    given = e.get("line") if isinstance(e.get("line"), int) else 0
    near = [n for n in hits if abs(n - given) <= TOLERANCE]
    base = {"path": rel(path, root)}
    if near:
        return {**base, "ok": True, "line": min(near, key=lambda n: abs(n - given)), "line_corrected": False}
    if len(hits) == 1:
        return {**base, "ok": True, "line": hits[0], "line_corrected": True,
                "reason": f"line corrected from {given} to {hits[0]}"}
    if hits:
        return {"ok": False, "reason": f"snippet occurs {len(hits)} times in the file and none is within "
                                       f"{TOLERANCE} lines of line {given}"}
    return {"ok": False, "reason": "snippet not found in the file"}


def check_probe(e: dict, findings: dict, root) -> dict:
    f = findings.get(e.get("finding_id"))
    if f is None:
        return {"ok": False, "reason": "probe finding not found in probes.json"}
    info = {k: f[k] for k in ("probe", "level", "message", "path", "line", "snippet")}
    code = check_code({"path": f["path"], "line": f["line"], "snippet": f["snippet"]}, root)
    if not code["ok"]:
        return {**info, "ok": False, "reason": "the code changed since the probe ran: " + code["reason"]}
    return {**info, "ok": True, "line": code["line"]}
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_verify_evidence.py`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/verify.py tests/test_verify_evidence.py
git commit -m "feat: verify transcript, code and probe evidence"
```

---
### Task 9: Ledger verification

**Files:**
- Modify: `scripts/verify.py` (append)
- Test: `tests/test_verify_ledger.py`

**Interfaces:**
- Consumes: `ledger.validate`, `ledger.normalise`, `ledger.SUBJECTS` (Task 7); `verify.check_transcript`, `check_code`, `check_probe` (Task 8).
- Produces:
  - `verify.verify_ledger(led: dict, index: dict[str, dict], root, probes: dict) -> dict` — raises `ledger.LedgerError` on a format problem; otherwise returns a new ledger where:
    - every evidence item gains `ok` (bool) and either the check's extra fields or `reason`;
    - promises whose sources all fail move to `rejected` (with `reason`); surviving promises keep only passing sources; a non-`unknown` status without a passing code/probe evidence becomes `unknown` with `downgraded_from` and `downgrade_reason`;
    - compromises whose error or every change fails move to `rejected`; `still_present: true` without passing code/probe evidence in `now` becomes `None` with `downgrade_reason`; `breaks` pointing at a rejected promise becomes `None`;
    - `map` becomes `{"nodes", "edges", "unverified_nodes", "unverified_edges"}` — a node/edge needs a passing code/probe evidence, and an edge also needs both ends verified;
    - access cells without passing code/probe evidence become `read = write = "unknown"` (originals kept in `claimed`); probe `implies` fill `unknown` cells (`from_probe: [finding ids]`) and contradict known ones (`conflicts: [{perm, probe, probe_says, ledger_says, message}]`); a resource named by a probe but absent from the ledger is added with `added_by_probe: True` (`"*"` resources are added only when the ledger has no resources);
    - path steps gain `unverified` (bool);
    - a `verification` summary: `{"evidence_total", "evidence_ok", "failed": [{"id", "reason"}], "downgraded", "rejected", "nodes_unverified", "edges_unverified", "cells_unknown", "conflicts"}`.
  - `verify.summary_lines(verified: dict) -> list[str]` — human-readable lines printed by `vl.py check`.

- [ ] **Step 1: Write the failing tests**

`tests/test_verify_ledger.py`:
```python
import pytest

import ledger
import verify

MIGRATION = "create table notes (id uuid);\n\nalter table notes disable row level security;\n"
INDEX = {
    "m1": {"id": "m1", "session": "s1", "ts": "2026-09-12T09:01:00Z", "role": "user", "kind": "text",
           "text": "只有我自己能看到我的笔记"},
    "m2": {"id": "m2", "session": "s1", "ts": "2026-09-12T09:05:00Z", "role": "tool", "kind": "error",
           "text": "new row violates row-level security policy"},
    "m3": {"id": "m3", "session": "s1", "ts": "2026-09-12T09:06:00Z", "role": "assistant", "kind": "edit",
           "text": "EDIT supabase/migrations/001.sql\n+++ after\nalter table notes disable row level security;"},
}
FINDING = {"id": "supabase_rls:supabase/migrations/001.sql:3", "probe": "supabase_rls", "level": "certain",
           "path": "supabase/migrations/001.sql", "line": 3,
           "snippet": "alter table notes disable row level security;", "message": "RLS is off for notes",
           "implies": [{"resource": "notes", "subject": "anonymous", "perm": "read", "value": "allow"},
                       {"resource": "notes", "subject": "anonymous", "perm": "write", "value": "allow"},
                       {"resource": "orders", "subject": "anonymous", "perm": "read", "value": "allow"}]}
PROBES = {"findings": [FINDING], "ran": ["supabase_rls"], "skipped": [], "stack": {}}


@pytest.fixture
def root(tmp_path):
    p = tmp_path / "supabase" / "migrations" / "001.sql"
    p.parent.mkdir(parents=True)
    p.write_text(MIGRATION, encoding="utf-8")
    return tmp_path


def base():
    return {
        "evidence": {
            "E1": {"kind": "transcript", "session": "s1", "msg_id": "m1", "quote": "只有我自己能看到我的笔记"},
            "E2": {"kind": "code", "path": "supabase/migrations/001.sql", "line": 3,
                   "snippet": "alter table notes disable row level security;"},
            "E3": {"kind": "probe", "finding_id": FINDING["id"]},
            "E4": {"kind": "transcript", "session": "s1", "msg_id": "m2", "quote": "violates row-level security"},
            "E5": {"kind": "transcript", "session": "s1", "msg_id": "m3", "quote": "disable row level security"},
            "FAKE_Q": {"kind": "transcript", "session": "s1", "msg_id": "m1", "quote": "我从来没说过这句话"},
            "FAKE_C": {"kind": "code", "path": "app/pay.ts", "line": 1, "snippet": "stripe.charge()"},
        },
        "promises": [
            {"id": "P1", "type": "user_requirement", "question": "who_can_see", "plain": "只有我能看到",
             "source": ["E1"], "status": "broken", "verdict_plain": "v", "verdict_dev": "d", "evidence": ["E2", "E3"]},
            {"id": "P2", "type": "user_requirement", "question": "what_costs", "plain": "made up",
             "source": ["FAKE_Q"], "status": "broken", "verdict_plain": "v", "verdict_dev": "d", "evidence": ["E2"]},
            {"id": "P3", "type": "ai_claim", "question": "what_costs", "plain": "claimed",
             "source": ["E1"], "status": "kept", "verdict_plain": "v", "verdict_dev": "d", "evidence": ["FAKE_C"]},
        ],
        "compromises": [
            {"id": "C1", "error": "E4", "change": ["E5"], "bypassed": "rls", "still_present": True,
             "now": ["E2"], "breaks": "P1"},
            {"id": "C2", "error": "E4", "change": ["E5"], "bypassed": "cors", "still_present": True,
             "now": ["FAKE_C"], "breaks": "P2"},
            {"id": "C3", "error": "FAKE_Q", "change": ["E5"], "bypassed": "x", "still_present": False,
             "now": [], "breaks": None},
        ],
        "map": {"nodes": [{"id": "db", "lane": "storage", "kind": "database", "label": "Supabase",
                           "holds": ["notes"], "paid": False, "evidence": ["E2"]},
                          {"id": "stripe", "lane": "storage", "kind": "third_party", "label": "Stripe",
                           "holds": [], "paid": True, "evidence": ["FAKE_C"]},
                          {"id": "web", "lane": "browser", "kind": "page", "label": "Home", "holds": [],
                           "paid": False, "evidence": ["E3"]}],
                "edges": [{"from": "web", "to": "db", "carries": "notes", "risk": None, "evidence": ["E2"]},
                          {"from": "web", "to": "stripe", "carries": "card", "risk": None, "evidence": ["E2"]}]},
        "access": {"resources": [{"name": "notes", "required_by": "P1", "cells": {
            "anonymous": {"read": "deny", "write": "unknown", "evidence": ["E2"]},
            "owner": {"read": "allow", "write": "allow", "evidence": ["FAKE_C"]}}}]},
        "paths": [{"action": "Save", "steps": [{"label": "insert", "evidence": "E2", "warning": None},
                                               {"label": "charge", "evidence": "FAKE_C", "warning": None}]}],
    }


def run(root, led=None):
    return verify.verify_ledger(led or base(), INDEX, root, PROBES)


def test_evidence_gets_ok_flags(root):
    out = run(root)
    ev = out["evidence"]
    assert ev["E1"]["ok"] and ev["E1"]["ts"] == "2026-09-12T09:01:00Z"
    assert ev["E3"]["ok"] and ev["E3"]["message"] == "RLS is off for notes"
    assert not ev["FAKE_Q"]["ok"] and not ev["FAKE_C"]["ok"]


def test_promises_rejected_downgraded_or_kept(root):
    out = run(root)
    ids = {p["id"]: p for p in out["promises"]}
    assert set(ids) == {"P1", "P3"}
    assert ids["P1"]["status"] == "broken"
    assert ids["P3"]["status"] == "unknown" and ids["P3"]["downgraded_from"] == "kept"
    assert [r["id"] for r in out["rejected"] if r["id"].startswith("P")] == ["P2"]


def test_compromises(root):
    out = run(root)
    comps = {c["id"]: c for c in out["compromises"]}
    assert comps["C1"]["still_present"] is True and comps["C1"]["breaks"] == "P1"
    assert comps["C2"]["still_present"] is None and comps["C2"]["breaks"] is None
    assert "C3" not in comps and any(r["id"] == "C3" for r in out["rejected"])


def test_map_draws_only_verified(root):
    m = run(root)["map"]
    assert [n["id"] for n in m["nodes"]] == ["db", "web"]
    assert [n["id"] for n in m["unverified_nodes"]] == ["stripe"]
    assert [(e["from"], e["to"]) for e in m["edges"]] == [("web", "db")]
    assert [(e["from"], e["to"]) for e in m["unverified_edges"]] == [("web", "stripe")]


def test_access_unknown_cells_probe_fill_and_conflicts(root):
    res = {r["name"]: r for r in run(root)["access"]["resources"]}
    notes = res["notes"]["cells"]
    assert notes["owner"]["read"] == "unknown" and notes["owner"]["claimed"] == {"read": "allow", "write": "allow"}
    assert notes["anonymous"]["read"] == "deny"
    assert notes["anonymous"]["conflicts"][0]["probe_says"] == "allow"
    assert notes["anonymous"]["write"] == "allow" and notes["anonymous"]["from_probe"] == [FINDING["id"]]
    assert res["orders"]["added_by_probe"] is True and res["orders"]["cells"]["anonymous"]["read"] == "allow"


def test_star_resource_added_only_when_ledger_has_none(root):
    probes = {"findings": [{**FINDING, "id": "fb", "path": "supabase/migrations/001.sql",
                            "implies": [{"resource": "*", "subject": "anonymous", "perm": "read", "value": "allow"}]}]}
    led = base()
    led["access"] = {"resources": []}
    out = verify.verify_ledger(led, INDEX, root, probes)
    assert [r["name"] for r in out["access"]["resources"]] == ["*"]
    out2 = verify.verify_ledger(base(), INDEX, root, probes)
    assert [r["name"] for r in out2["access"]["resources"]] == ["notes"]
    assert out2["access"]["resources"][0]["cells"]["anonymous"]["conflicts"]


def test_paths_mark_unverified_steps(root):
    steps = run(root)["paths"][0]["steps"]
    assert [s["unverified"] for s in steps] == [False, True]


def test_summary_counts_and_lines(root):
    out = run(root)
    v = out["verification"]
    assert v["evidence_total"] == 7 and v["evidence_ok"] == 5
    assert v["downgraded"] == 1 and v["rejected"] == 2 and v["nodes_unverified"] == 1 and v["conflicts"] == 1
    text = "\n".join(verify.summary_lines(out))
    assert "FAKE_C" in text and "file not found" in text


def test_format_error_raises(root):
    led = base()
    led["promises"][0]["status"] = "maybe"
    with pytest.raises(ledger.LedgerError):
        run(root, led)


def test_input_is_not_mutated(root):
    led = base()
    run(root, led)
    assert "ok" not in led["evidence"]["E1"]
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_verify_ledger.py`
Expected: FAIL — `AttributeError: module 'verify' has no attribute 'verify_ledger'`.

- [ ] **Step 3: Append to `scripts/verify.py`**

Add to the imports: `from ledger import normalise, validate`.

```python
STRONG = ("code", "probe")


def _check(e: dict, index: dict, root, findings: dict) -> dict:
    if e["kind"] == "transcript":
        return check_transcript(e, index)
    if e["kind"] == "code":
        return check_code(e, root)
    return check_probe(e, findings, root)


def _apply_probe_implications(resources: list[dict], findings: list[dict]) -> int:
    had_any = bool(resources)
    conflicts = 0
    for f in findings:
        for imp in f.get("implies") or []:
            name = imp["resource"]
            targets = [r for r in resources if r["name"] == name or name == "*"]
            if not targets:
                if name == "*" and had_any:
                    continue
                new = {"name": name, "cells": {}, "required_by": None, "added_by_probe": True}
                resources.append(new)
                targets = [new]
            for r in targets:
                cell = r["cells"].setdefault(imp["subject"], {"read": "unknown", "write": "unknown", "evidence": []})
                current = cell.get(imp["perm"], "unknown")
                if current == "unknown":
                    cell[imp["perm"]] = imp["value"]
                    if f["id"] not in cell.setdefault("from_probe", []):
                        cell["from_probe"].append(f["id"])
                elif current != imp["value"]:
                    cell.setdefault("conflicts", []).append({
                        "perm": imp["perm"], "probe": f["id"], "probe_says": imp["value"],
                        "ledger_says": current, "message": f["message"]})
                    conflicts += 1
    return conflicts


def verify_ledger(led: dict, index: dict, root, probes: dict) -> dict:
    validate(led)
    out = normalise(led)
    findings = {f["id"]: f for f in probes.get("findings", [])}
    ev = out["evidence"]
    for eid, e in ev.items():
        e.update(_check(e, index, root, findings))

    def ok(i) -> bool:
        return bool(ev.get(i, {}).get("ok"))

    def strong(ids) -> list:
        return [i for i in ids if ok(i) and ev[i]["kind"] in STRONG]

    rejected, kept, downgraded = [], [], 0
    for x in out["promises"]:
        if not any(ok(i) for i in x["source"]):
            rejected.append({**x, "reason": "none of its quotes could be found in the conversations"})
            continue
        x["source"] = [i for i in x["source"] if ok(i)]
        if x["status"] != "unknown" and not strong(x["evidence"]):
            x["downgraded_from"], x["status"] = x["status"], "unknown"
            x["downgrade_reason"] = "no code or probe evidence passed verification"
            downgraded += 1
        kept.append(x)
    out["promises"] = kept
    pids = {x["id"] for x in kept}

    comps = []
    for c in out["compromises"]:
        if not ok(c["error"]) or not any(ok(i) for i in c["change"]):
            rejected.append({**c, "reason": "its error or its change could not be found in the conversations"})
            continue
        if c["still_present"] and not strong(c["now"]):
            c["still_present"] = None
            c["downgrade_reason"] = "no code or probe evidence that it is still in the code"
        if c.get("breaks") not in pids:
            c["breaks"] = None
        comps.append(c)
    out["compromises"] = comps
    out["rejected"] = rejected

    nodes, bad_nodes = [], []
    for n in out["map"]["nodes"]:
        (nodes if strong(n.get("evidence", [])) else bad_nodes).append(n)
    good_ids = {n["id"] for n in nodes}
    edges, bad_edges = [], []
    for e in out["map"]["edges"]:
        drawn = e["from"] in good_ids and e["to"] in good_ids and strong(e.get("evidence", []))
        (edges if drawn else bad_edges).append(e)
    out["map"] = {"nodes": nodes, "edges": edges, "unverified_nodes": bad_nodes, "unverified_edges": bad_edges}

    resources = out["access"]["resources"]
    for r in resources:
        for cell in r["cells"].values():
            cell.setdefault("evidence", [])
            if not strong(cell["evidence"]):
                if cell.get("read", "unknown") != "unknown" or cell.get("write", "unknown") != "unknown":
                    cell["claimed"] = {"read": cell.get("read", "unknown"), "write": cell.get("write", "unknown")}
                cell["read"] = cell["write"] = "unknown"
            cell.setdefault("read", "unknown")
            cell.setdefault("write", "unknown")
        if r.get("required_by") not in pids:
            r["required_by"] = None
    conflicts = _apply_probe_implications(resources, list(findings.values()))

    for path in out["paths"]:
        for st in path["steps"]:
            st["unverified"] = not strong([st["evidence"]])

    failed = [{"id": k, "reason": e.get("reason", "")} for k, e in ev.items() if not e.get("ok")]
    out["verification"] = {
        "evidence_total": len(ev), "evidence_ok": len(ev) - len(failed), "failed": failed,
        "downgraded": downgraded, "rejected": len(rejected),
        "nodes_unverified": len(bad_nodes), "edges_unverified": len(bad_edges),
        "cells_unknown": sum(1 for r in resources for c in r["cells"].values()
                             for perm in ("read", "write") if c.get(perm) == "unknown"),
        "conflicts": conflicts,
    }
    return out


def summary_lines(verified: dict) -> list[str]:
    v = verified["verification"]
    ev = verified["evidence"]
    lines = [f"Evidence: {v['evidence_total']} checked, {v['evidence_ok']} passed, {len(v['failed'])} failed"]
    for f in v["failed"]:
        e = ev[f["id"]]
        where = (f"{e.get('path')}:{e.get('line')}" if e["kind"] in ("code", "probe")
                 else f"message {e.get('msg_id')}")
        lines.append(f"  ✗ {f['id']} ({e['kind']} {where}): {f['reason']}")
    counts = {s: 0 for s in ("kept", "broken", "partial", "pending", "unknown")}
    for p in verified["promises"]:
        counts[p["status"]] += 1
    lines.append("Promises: {} in the ledger (✅{kept} ❌{broken} ⚠{partial} ⏳{pending} ❓{unknown}), "
                 "{d} downgraded to ❓, {r} rejected".format(len(verified["promises"]), d=v["downgraded"],
                                                           r=v["rejected"], **counts))
    lines.append(f"Map: {len(verified['map']['nodes'])} nodes drawn, {v['nodes_unverified']} left off as unverified; "
                 f"Access: {v['cells_unknown']} cells unknown, {v['conflicts']} conflicts with probes")
    return lines
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_verify_evidence.py tests/test_verify_ledger.py`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/verify.py tests/test_verify_ledger.py
git commit -m "feat: verify a whole ledger, downgrade or drop what lacks evidence"
```

---
### Task 10: Report page — shared bits, strings, page assembly, delivery

**Files:**
- Create: `scripts/ledger_report/__init__.py` (empty), `scripts/ledger_report/bits.py`, `scripts/ledger_report/i18n.py`
- Create: `scripts/ledger_report/assets/report.css`, `scripts/ledger_report/assets/report.js`
- Create (stubs filled in Tasks 11–12): `scripts/ledger_report/map_svg.py`, `access_html.py`, `timeline_svg.py`, `paths_svg.py`
- Create: `scripts/render.py`
- Test: `tests/test_render_page.py`, `tests/helpers/verified.py`

**Interfaces:**
- Consumes: a verified ledger (Task 9 output shape), the run manifest (`run.json`, built in Task 13: keys `project_name`, `lang`, `sessions` = `Stats.to_dict()`, `unattributed` list, …), `probes.json` (Task 5); `redact.redact`, `redact.find_secrets`; `common.slugify`.
- Produces:
  - `ledger_report.bits`: `GLYPH` (status → emoji), `ORDER = ("broken", "partial", "pending", "unknown", "kept")`, `h(value) -> str` (mask then HTML-escape), `trunc(text, n) -> str`, `ht(value, n) -> str` (mask, then truncate, then escape — never truncate before masking), `fmt_date(ts) -> "YYYY-MM-DD HH:MM"`, `evidence_html(ids, evidence, lang) -> str`.
  - `ledger_report.i18n`: `STR = {"zh": {...}, "en": {...}}` (identical key sets), `t(lang, key, **kw) -> str`.
  - Diagram functions (stubs now): `map_svg.render_map(ledger, lang) -> str`, `access_html.render_access(ledger, lang) -> str`, `timeline_svg.render_timeline(ledger, lang, has_transcripts) -> str`, `paths_svg.render_paths(ledger, lang) -> str`.
  - `render.counts(ledger) -> dict[status, int]`, `render.summaries(ledger, lang) -> dict[question, str]`, `render.assert_no_secrets(doc: str) -> None` (raises `RuntimeError`), `render.render_html(ledger, run, probes, lang) -> str`, `render.deliver(html, run_dir, project_name, out_dir=None) -> Path`.
  - Test helper `helpers.verified.sample()` → a verified ledger dict, `helpers.verified.RUN`, `helpers.verified.PROBES`, `helpers.verified.OPENAI`.

- [ ] **Step 1: Write the shared test data**

`tests/helpers/verified.py`:
```python
"""A hand-built verified ledger (the shape verify.verify_ledger returns)."""
import copy

OPENAI = "sk-proj-" + "Ab3dE5fG7hJ9kL1mN3pQ5rS7tU9vW1xY"

_SAMPLE = {
    "evidence": {
        "E1": {"kind": "transcript", "session": "s1", "msg_id": "m1", "quote": "只有我自己能看到我的笔记",
               "ok": True, "ts": "2026-09-12T09:01:00Z", "role": "user", "msg_kind": "text"},
        "E2": {"kind": "code", "path": "supabase/migrations/001.sql", "line": 3,
               "snippet": "alter table notes disable row level security;", "ok": True, "line_corrected": False},
        "E3": {"kind": "probe", "finding_id": "secrets_exposed:.env.local:2", "ok": True, "probe": "secrets_exposed",
               "level": "certain", "path": ".env.local", "line": 2,
               "snippet": "NEXT_PUBLIC_OPENAI_API_KEY=" + OPENAI, "message": "bundled into the browser"},
        "E4": {"kind": "transcript", "session": "s1", "msg_id": "m4", "quote": "暂时先把 key 放前端",
               "ok": True, "ts": "2026-09-13T10:00:00Z", "role": "assistant", "msg_kind": "text"},
        "E5": {"kind": "transcript", "session": "s1", "msg_id": "m5", "quote": "violates row-level security",
               "ok": True, "ts": "2026-09-12T09:20:00Z", "role": "tool", "msg_kind": "error"},
        "E6": {"kind": "transcript", "session": "s1", "msg_id": "m6", "quote": "disable row level security",
               "ok": True, "ts": "2026-09-12T09:21:00Z", "role": "assistant", "msg_kind": "edit"},
        "E7": {"kind": "code", "path": "app/api/summarize/route.ts", "line": 3,
               "snippet": "export async function POST(req: Request) {", "ok": True, "line_corrected": True},
        "BAD": {"kind": "code", "path": "app/pay.ts", "line": 1, "snippet": "stripe()", "ok": False,
                "reason": "file not found"},
    },
    "promises": [
        {"id": "P1", "type": "user_requirement", "question": "who_can_see", "plain": "只有我自己能看到我的笔记",
         "source": ["E1"], "status": "broken", "verdict_plain": "前门锁了，后窗一直开着",
         "verdict_dev": "notes 表关闭了 RLS（supabase/migrations/001.sql:3）", "evidence": ["E2"],
         "fix_prompt": "Re-enable row level security on notes and add a policy using (auth.uid() = user_id)."},
        {"id": "P2", "type": "deferred", "question": "open_debts", "plain": "把 OpenAI key 移到服务端",
         "source": ["E4"], "status": "pending", "verdict_plain": "key 还在前端，任何人都能拿走",
         "verdict_dev": "NEXT_PUBLIC_OPENAI_API_KEY in .env.local", "evidence": ["E3"],
         "fix_prompt": "Rename NEXT_PUBLIC_OPENAI_API_KEY to OPENAI_API_KEY and read it only in route.ts."},
        {"id": "P3", "type": "ai_claim", "question": "what_costs", "plain": "接口已经加了登录保护",
         "source": ["E1"], "status": "unknown", "verdict_plain": "没找到能证明这一点的代码",
         "verdict_dev": "no auth check found", "evidence": ["BAD"], "downgraded_from": "kept",
         "downgrade_reason": "no code or probe evidence passed verification", "fix_prompt": "Add a login check."},
        {"id": "P4", "type": "user_requirement", "question": "where_data", "plain": "笔记要存到 Supabase",
         "source": ["E1"], "status": "kept", "verdict_plain": "笔记确实存在 Supabase 的 notes 表里",
         "verdict_dev": "supabase.from('notes')", "evidence": ["E2"]},
    ],
    "compromises": [{"id": "C1", "error": "E5", "change": ["E6"], "bypassed": "RLS", "still_present": True,
                     "now": ["E2"], "breaks": "P1"}],
    "rejected": [{"id": "P9", "plain": "made up", "reason": "none of its quotes could be found in the conversations"}],
    "map": {"nodes": [{"id": "web", "lane": "browser", "kind": "page", "label": "首页", "holds": [], "paid": False,
                       "evidence": ["E2"]},
                      {"id": "api", "lane": "server", "kind": "route", "label": "/api/summarize", "holds": [],
                       "paid": False, "evidence": ["E7"]},
                      {"id": "db", "lane": "storage", "kind": "database", "label": "Supabase", "holds": ["notes"],
                       "paid": False, "evidence": ["E2"]},
                      {"id": "ai", "lane": "storage", "kind": "third_party", "label": "OpenAI", "holds": [],
                       "paid": True, "evidence": ["E7"]}],
            "edges": [{"from": "web", "to": "db", "carries": "笔记", "risk": "陌生人也能读", "evidence": ["E2"]},
                      {"from": "web", "to": "api", "carries": "笔记内容", "risk": None, "evidence": ["E7"]},
                      {"from": "api", "to": "ai", "carries": "笔记内容", "risk": None, "evidence": ["E7"]}],
            "unverified_nodes": [{"id": "stripe", "lane": "storage", "kind": "third_party", "label": "Stripe",
                                  "holds": [], "paid": True, "evidence": ["BAD"]}],
            "unverified_edges": []},
    "access": {"resources": [
        {"name": "notes", "required_by": "P1", "cells": {
            "anonymous": {"read": "allow", "write": "allow", "evidence": ["E2"]},
            "signed_in": {"read": "allow", "write": "allow", "evidence": ["E2"]},
            "owner": {"read": "allow", "write": "allow", "evidence": ["E2"]}}},
        {"name": "profiles", "required_by": None, "cells": {
            "anonymous": {"read": "deny", "write": "deny", "evidence": ["E2"]},
            "owner": {"read": "allow", "write": "allow", "evidence": ["E2"]}}}]},
    "paths": [{"action": "点“AI 总结”", "steps": [
        {"label": "summarize()", "evidence": "E7", "warning": None, "unverified": False},
        {"label": "POST /api/summarize", "evidence": "E7", "warning": "没有登录检查", "unverified": False},
        {"label": "stripe.charge()", "evidence": "BAD", "warning": None, "unverified": True}]}],
    "verification": {"evidence_total": 8, "evidence_ok": 7, "failed": [{"id": "BAD", "reason": "file not found"}],
                     "downgraded": 1, "rejected": 1, "nodes_unverified": 1, "edges_unverified": 0,
                     "cells_unknown": 0, "conflicts": 0},
}

RUN = {"project_name": "notes", "lang": "zh", "unattributed": ["lib/legacy.ts"],
       "sessions": {"threads": 2, "records": 40, "earliest": "2026-09-12T09:00:00Z", "latest": "2026-09-13T11:00:00Z",
                    "by_agent": {"claude-code": 2}, "archived_threads": 1, "ignored_types": {"claude:mode": 3},
                    "bad_lines": 0, "warnings": ["x.jsonl: the log format may have changed"]}}
PROBES = {"ran": ["secrets_exposed", "supabase_rls"], "skipped": [{"probe": "firebase_rules", "reason": "not used"}],
          "stack": {"stacks": ["nextjs", "supabase", "flask"], "unsupported": ["flask"], "covered": True},
          "findings": []}


def sample():
    return copy.deepcopy(_SAMPLE)
```

- [ ] **Step 2: Write the failing tests**

`tests/test_render_page.py`:
```python
import re

import pytest

import render
from helpers.verified import OPENAI, PROBES, RUN, sample
from ledger_report import bits, i18n


def test_i18n_key_sets_match_and_t_formats():
    assert set(i18n.STR["zh"]) == set(i18n.STR["en"])
    assert i18n.t("zh", "ok_rows", n=3) == "其余 3 类数据（没发现问题）"
    assert i18n.t("fr", "today") == i18n.STR["en"]["today"]


def test_every_literal_key_used_in_the_report_code_exists():
    import pathlib
    scripts = pathlib.Path(__file__).resolve().parents[1] / "scripts"
    src = "".join(p.read_text(encoding="utf-8") for p in scripts.glob("**/*.py"))
    keys = set(re.findall(r"""\bt\(\s*lang\s*,\s*["']([a-z_]+)["']\s*[,)]""", src))
    assert keys and keys <= set(i18n.STR["en"]), keys - set(i18n.STR["en"])


def test_h_masks_then_escapes_and_ht_masks_before_truncating():
    assert bits.h(f"<b>{OPENAI}</b>") == f"&lt;b&gt;sk-proj-…{OPENAI[-4:]}&lt;/b&gt;"
    short = bits.ht(f"key: {OPENAI}", 20)
    assert "Ab3dE5fG7h" not in short and len(short) <= 20


def test_counts_and_summaries():
    led = sample()
    assert render.counts(led) == {"broken": 1, "partial": 0, "pending": 1, "unknown": 1, "kept": 1}
    s = render.summaries(led, "zh")
    assert s["where_data"] == "数据存放在：Supabase。数据还会发给：OpenAI。"
    assert s["what_costs"] == "会花钱的服务：OpenAI。"
    assert s["who_can_see"] == "2 类数据里，有 1 类陌生人能读到；0 处说法冲突。"
    assert s["what_breaks"] == "1 处“报错后的妥协”仍在代码里；1 条承诺没做到。"
    assert s["open_debts"] == "还欠着 1 件说过“以后再说”的事。"


def test_page_structure(monkeypatch):
    html = render.render_html(sample(), RUN, PROBES, "zh")
    assert html.startswith("<!doctype html>") and '<html lang="zh-CN">' in html
    assert "「notes」对账单" in html and "依据 2 段对话" in html
    assert html.index("没做到") < html.index("做到了")
    assert html.count('class="copy"') == 2  # broken + pending; not unknown, not kept
    assert 'class="verdict-dev dev-only"' in html
    assert "原结论“做到了”缺少能通过校验的证据" in html
    assert "没有覆盖的技术栈：flask" in html and "lib/legacy.ts" in html
    assert "file not found" in html and "made up" in html and "format may have changed" in html
    assert 'data-status="broken"' in html and 'data-filter="pending"' in html


def test_report_never_contains_a_raw_secret():
    html = render.render_html(sample(), RUN, PROBES, "zh")
    assert OPENAI not in html and f"sk-proj-…{OPENAI[-4:]}" in html
    assert render.find_secrets(html) == []


def test_assert_no_secrets_refuses():
    with pytest.raises(RuntimeError) as exc:
        render.assert_no_secrets(f"<p>{OPENAI}</p>")
    assert OPENAI not in str(exc.value)


def test_english_report_and_empty_ledger():
    led = sample()
    led["promises"], led["compromises"] = [], []
    led["map"] = {"nodes": [], "edges": [], "unverified_nodes": [], "unverified_edges": []}
    led["access"] = {"resources": []}
    led["paths"] = []
    run = {**RUN, "sessions": {**RUN["sessions"], "records": 0, "threads": 0}}
    html = render.render_html(led, run, PROBES, "en")
    assert '<html lang="en">' in html and "No conversations were found" in html
    assert "The ledger is empty" in html


def test_deliver_prefers_explicit_dir_then_falls_back(tmp_path, monkeypatch):
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    out = render.deliver("<p>x</p>", run_dir, "我的 应用", out_dir=tmp_path / "out")
    assert out.parent == tmp_path / "out" and out.name.startswith("vibe-ledger-我的-应用-")
    assert (run_dir / "report.html").exists()
    blocker = tmp_path / "not-a-dir"
    blocker.write_text("x")
    monkeypatch.setenv("HOME", str(tmp_path / "nohome"))
    fallback = render.deliver("<p>x</p>", run_dir, "app", out_dir=blocker)
    assert fallback == run_dir / "report.html"


def test_deliver_uses_env_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("VIBE_LEDGER_OUT_DIR", str(tmp_path / "env-out"))
    run_dir = tmp_path / "run"
    run_dir.mkdir()
    assert render.deliver("<p>x</p>", run_dir, "app").parent == tmp_path / "env-out"
```

- [ ] **Step 3: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_render_page.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'render'`.

- [ ] **Step 4: Write `scripts/ledger_report/bits.py`**

```python
"""Small pieces every part of the report uses. Everything that reaches the
page goes through h() or ht(): mask secrets first, then escape."""
from __future__ import annotations

from html import escape

from ledger_report.i18n import t
from redact import redact

GLYPH = {"kept": "✅", "broken": "❌", "partial": "⚠️", "pending": "⏳", "unknown": "❓"}
ORDER = ("broken", "partial", "pending", "unknown", "kept")


def h(value) -> str:
    return escape(redact("" if value is None else str(value)), quote=True)


def trunc(text, n: int) -> str:
    text = str(text)
    return text if len(text) <= n else text[: max(n - 1, 0)] + "…"


def ht(value, n: int) -> str:
    """Mask, then truncate, then escape: truncating first could cut a secret
    into a fragment too short to be recognised and masked."""
    return escape(trunc(redact("" if value is None else str(value)), n), quote=True)


def fmt_date(ts) -> str:
    ts = str(ts or "")
    return ts[:16].replace("T", " ")


def evidence_html(ids, evidence: dict, lang: str) -> str:
    items = []
    for i in ids:
        e = evidence.get(i)
        if not e:
            continue
        if e["kind"] == "transcript":
            who = t(lang, "said_by_user") if e.get("role") == "user" else t(lang, "said_by_ai")
            head = f'{h(t(lang, "transcript"))} · {h(who)} · {h(fmt_date(e.get("ts")))}'
            body = f'<blockquote>{ht(e.get("quote", ""), 600)}</blockquote>'
        elif e["kind"] == "code":
            fixed = f' · {h(t(lang, "line_corrected"))}' if e.get("line_corrected") else ""
            head = f'{h(t(lang, "code"))} · <code>{ht(e.get("path", ""), 80)}:{h(e.get("line", ""))}</code>{fixed}'
            body = f'<pre>{ht(e.get("snippet", ""), 800)}</pre>'
        else:
            head = (f'{h(t(lang, "probe"))} · <code>{ht(e.get("probe", ""), 40)}</code> · '
                    f'<code>{ht(e.get("path", ""), 80)}:{h(e.get("line", ""))}</code>')
            body = f'<p>{ht(e.get("message", ""), 300)}</p><pre>{ht(e.get("snippet", ""), 400)}</pre>'
        fail = "" if e.get("ok") else f'<p class="fail">✗ {ht(e.get("reason", ""), 200)}</p>'
        cls = "ev ok" if e.get("ok") else "ev failed"
        items.append(f'<li class="{cls}"><div class="ev-head">{head}</div>{body}{fail}</li>')
    if not items:
        return ""
    return (f'<details class="evidence"><summary>{h(t(lang, "evidence"))} ({len(items)})</summary>'
            f'<ul>{"".join(items)}</ul></details>')
```
- [ ] **Step 5: Write `scripts/ledger_report/i18n.py`**

```python
"""Every string the report shows, in Chinese and English (identical keys)."""
from __future__ import annotations

STR = {
    "zh": {
        "doc_title": "{name} 对账单", "title": "「{name}」对账单",
        "subtitle": "依据 {threads} 段对话（{start} 至 {end}）和当前代码生成",
        "subtitle_none": "没有找到对话记录，只核对了当前代码",
        "view_dev": "开发者视图", "view_plain": "大白话",
        "status_kept": "做到了", "status_broken": "没做到", "status_partial": "部分做到",
        "status_pending": "还欠着", "status_unknown": "查不到",
        "q_where_data": "数据存在哪", "q_what_costs": "什么操作会花钱", "q_who_can_see": "谁能看到",
        "q_what_breaks": "哪里最容易出事", "q_open_debts": "还欠着的“以后再说”",
        "sec_map": "① 数据存在哪 · 什么会花钱", "sec_access": "② 谁能看到",
        "sec_timeline": "③ 哪里最容易出事 · 还欠着的事", "sec_paths": "关键操作路径",
        "sec_ledger": "对账表", "sec_coverage": "这份报告没看到什么",
        "lane_browser": "浏览器", "lane_server": "你的服务器", "lane_storage": "存储与第三方服务",
        "legend_map": "💰 = 会花钱 · 红色 = 有风险",
        "subj_anonymous": "陌生人", "subj_anonymous_sub": "没登录",
        "subj_signed_in": "其他登录用户", "subj_signed_in_sub": "不是这条数据的主人",
        "subj_owner": "本人", "subj_owner_sub": "数据的主人",
        "perm_read": "读", "perm_write": "改", "allow": "能", "deny": "不能", "unknown": "?",
        "lane_you_said": "你说的", "lane_error": "报错", "lane_ai_changed": "AI 改的",
        "lane_deferred": "以后再说", "today": "今天",
        "still_present": "仍在代码里", "fixed": "已不在", "unclear": "不确定", "compromise": "妥协",
        "said_by_user": "你说的", "said_by_ai": "AI 说的", "said_on": "{who} · {date}",
        "evidence": "证据", "copy_fix": "复制修复指令", "copied": "已复制",
        "no_transcripts_timeline": "没找到对话记录，无法生成时间线。",
        "no_timeline_items": "对话里没有找到与这五个问题相关、又能核实的事件。",
        "no_database": "没有检测到数据库。", "no_map": "没能从代码里确认任何数据去向。",
        "no_paths": "没有可展示的操作路径。",
        "no_promises": "账本是空的：对话里没有找到与这五个问题相关、又能核实的承诺。",
        "other_nodes": "其他（图上放不下）：", "unverified_nodes": "未核实，没画进图里：",
        "ok_rows": "其余 {n} 类数据（没发现问题）",
        "probe_says": "检查脚本发现：{msg}", "conflict": "说法冲突", "filter_all": "全部",
        "col_status": "状态", "col_promise": "承诺", "col_who": "来源", "col_verdict": "结论",
        "sum_where": "数据存放在：{stores}。", "sum_where_none": "没有从代码里确认到数据存放的位置。",
        "sum_sent": "数据还会发给：{others}。",
        "sum_costs": "会花钱的服务：{paid}。", "sum_costs_none": "没有发现会按次收费的服务。",
        "sum_access": "{n} 类数据里，有 {anon} 类陌生人能读到；{conflicts} 处说法冲突。",
        "sum_breaks": "{comp} 处“报错后的妥协”仍在代码里；{broken} 条承诺没做到。",
        "sum_debts": "还欠着 {n} 件说过“以后再说”的事。",
        "cov_sessions": "读了 {claude} 段 Claude Code 对话、{codex} 段 Codex 对话。",
        "cov_archived": "其中 {n} 段来自之前的归档（原始记录已被清理）。",
        "cov_ignored": "跳过了 {n} 条与本报告无关的记录（系统记录、工具调用等）。",
        "cov_bad": "{n} 行记录损坏，无法读取。",
        "cov_unattributed": "{n} 个代码文件在对话里找不到改动记录（可能是手动改的、在别的工具里改的，或由命令生成）：",
        "cov_probes": "运行了这些检查：{ran}。", "cov_skipped": "跳过的检查：{skipped}。",
        "cov_unsupported": "没有覆盖的技术栈：{stacks}，这部分没有做确定性核验。",
        "cov_failed": "{n} 条证据没通过校验：", "cov_rejected": "{n} 条结论因为在对话里找不到出处而被拒：",
        "cov_warnings": "警告：", "cov_none": "无",
        "transcript": "对话", "code": "代码", "probe": "检查脚本", "line_corrected": "行号已更正",
        "downgraded": "原结论“{old}”缺少能通过校验的证据，已改为“查不到”。",
        "sep": "、", "colon": "：", "required": "要求：", "all_data": "所有数据",
        "unverified": "未核实", "more_items": "另有 {n} 项放不下，见下方对账表。",
    },
    "en": {
        "doc_title": "{name} ledger", "title": "{name}: promises vs. code",
        "subtitle": "Built from {threads} conversations ({start} to {end}) and the current code",
        "subtitle_none": "No conversations were found; only the current code was checked",
        "view_dev": "Developer view", "view_plain": "Plain view",
        "status_kept": "Kept", "status_broken": "Broken", "status_partial": "Partly kept",
        "status_pending": "Still owed", "status_unknown": "Can't tell",
        "q_where_data": "Where your data lives", "q_what_costs": "What costs money",
        "q_who_can_see": "Who can see it", "q_what_breaks": "Where it is most likely to break",
        "q_open_debts": "Things put off \"for later\"",
        "sec_map": "1 · Where data lives · what costs money", "sec_access": "2 · Who can see it",
        "sec_timeline": "3 · Where it may break · what is still owed", "sec_paths": "Key call paths",
        "sec_ledger": "The ledger", "sec_coverage": "What this report could not see",
        "lane_browser": "Browser", "lane_server": "Your server", "lane_storage": "Storage & outside services",
        "legend_map": "💰 = costs money · red = risk",
        "subj_anonymous": "Strangers", "subj_anonymous_sub": "not signed in",
        "subj_signed_in": "Other users", "subj_signed_in_sub": "signed in, not the owner",
        "subj_owner": "You", "subj_owner_sub": "the owner",
        "perm_read": "Read", "perm_write": "Change", "allow": "yes", "deny": "no", "unknown": "?",
        "lane_you_said": "You said", "lane_error": "Error", "lane_ai_changed": "AI changed",
        "lane_deferred": "For later", "today": "Today",
        "still_present": "still in the code", "fixed": "gone", "unclear": "unclear", "compromise": "Workaround",
        "said_by_user": "You said", "said_by_ai": "The AI said", "said_on": "{who} · {date}",
        "evidence": "Evidence", "copy_fix": "Copy the fix instruction", "copied": "Copied",
        "no_transcripts_timeline": "No conversations were found, so there is no timeline.",
        "no_timeline_items": "No verifiable event about the five questions was found in the conversations.",
        "no_database": "No database was detected.", "no_map": "No data flow could be confirmed from the code.",
        "no_paths": "No call paths to show.",
        "no_promises": "The ledger is empty: no promise about the five questions could be verified in the conversations.",
        "other_nodes": "Others (no room on the map): ", "unverified_nodes": "Unverified, left off the map: ",
        "ok_rows": "{n} more kinds of data (no problems found)",
        "probe_says": "a check found: {msg}", "conflict": "Conflicting answers", "filter_all": "All",
        "col_status": "Status", "col_promise": "Promise", "col_who": "Source", "col_verdict": "Verdict",
        "sum_where": "Data is stored in: {stores}.", "sum_where_none": "No storage could be confirmed from the code.",
        "sum_sent": "Data is also sent to: {others}.",
        "sum_costs": "Services that charge per use: {paid}.", "sum_costs_none": "No pay-per-use service was found.",
        "sum_access": "Of {n} kinds of data, strangers can read {anon}; {conflicts} conflicting answers.",
        "sum_breaks": "{comp} workarounds made after an error are still in the code; {broken} promises are broken.",
        "sum_debts": "{n} things put off \"for later\" are still owed.",
        "cov_sessions": "Read {claude} Claude Code and {codex} Codex conversations.",
        "cov_archived": "{n} of them came from an earlier archive (the original logs were deleted).",
        "cov_ignored": "Skipped {n} records unrelated to this report (bookkeeping, tool calls and similar).",
        "cov_bad": "{n} damaged lines could not be read.",
        "cov_unattributed": "{n} code files have no change in the conversations (edited by hand, in another tool, or generated by a command):",
        "cov_probes": "Checks that ran: {ran}.", "cov_skipped": "Checks skipped: {skipped}.",
        "cov_unsupported": "Not covered: {stacks}; those parts were not checked deterministically.",
        "cov_failed": "{n} pieces of evidence failed verification:",
        "cov_rejected": "{n} conclusions were rejected because their source could not be found:",
        "cov_warnings": "Warnings:", "cov_none": "none",
        "transcript": "Conversation", "code": "Code", "probe": "Check", "line_corrected": "line number corrected",
        "downgraded": "The original verdict \"{old}\" had no evidence that passed verification, so it now reads \"can't tell\".",
        "sep": ", ", "colon": ": ", "required": "Required: ", "all_data": "All data",
        "unverified": "unverified", "more_items": "{n} more items did not fit; see the ledger below.",
    },
}


def t(lang: str, key: str, **kw) -> str:
    text = STR.get(lang, STR["en"]).get(key, STR["en"][key])
    return text.format(**kw) if kw else text
```
- [ ] **Step 6: Write `scripts/ledger_report/assets/report.css`**

```css
:root{--bg:#f7f6f2;--fg:#1c1c1e;--muted:#5f5f66;--line:#dcd9cf;--card:#ffffff;--soft:#efede6;
  --ok:#14805a;--bad:#d12f3a;--warn:#b66d00;--pend:#6a45c0;--unk:#77777f;--accent:#1f5fd6;--paid:#9a6500}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#121214;--fg:#ececf0;--muted:#a6a6ae;
  --line:#2e2e34;--card:#1b1b1f;--soft:#232328;--ok:#3cc68a;--bad:#ff5c66;--warn:#f2a73b;--pend:#a88dff;
  --unk:#9a9aa3;--accent:#74a1ff;--paid:#e9b949}}
:root[data-theme=dark]{--bg:#121214;--fg:#ececf0;--muted:#a6a6ae;--line:#2e2e34;--card:#1b1b1f;--soft:#232328;
  --ok:#3cc68a;--bad:#ff5c66;--warn:#f2a73b;--pend:#a88dff;--unk:#9a9aa3;--accent:#74a1ff;--paid:#e9b949}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
  font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei",sans-serif;
  font-variant-numeric:lining-nums tabular-nums}
.wrap{max-width:1040px;margin:0 auto;padding:28px 16px 72px}
header h1{font-size:30px;line-height:1.2;margin:0 0 6px;letter-spacing:-.01em}
.sub{color:var(--muted);margin:0 0 14px}
.toggle{font:inherit;font-size:14px;padding:6px 14px;border-radius:999px;border:1px solid var(--line);
  background:var(--card);color:var(--fg);cursor:pointer}
body:not(.dev) .dev-only{display:none}
body.dev .plain-only{display:none}
.counts{display:flex;flex-wrap:wrap;gap:8px;margin:16px 0 0}
.count{display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:999px;background:var(--card);
  border:1.5px solid var(--line);font-weight:600;font-size:15px}
.count b{font-size:18px}
.s-broken{--c:var(--bad)}.s-partial{--c:var(--warn)}.s-pending{--c:var(--pend)}.s-unknown{--c:var(--unk)}.s-kept{--c:var(--ok)}
.count[class*=s-]{border-color:var(--c);color:var(--c)}
section{margin-top:44px}
h2{font-size:23px;margin:0 0 10px}
.summary{margin:0 0 8px}
.summary b{font-weight:650}
.diagram-wrap,.scroll-x,.matrix-wrap{overflow-x:auto;-webkit-overflow-scrolling:touch;border:1px solid var(--line);
  border-radius:14px;background:var(--card);padding:10px;margin:12px 0}
svg.diagram{display:block;width:100%;height:auto}
svg.map{min-width:720px}
svg.timeline{width:auto;max-width:none}
.empty{color:var(--muted);font-style:italic;padding:12px 0}
.note{color:var(--muted);font-size:14px}
.note.unverified{color:var(--warn)}
/* map */
.lane{fill:var(--soft)}.lane-title{fill:var(--muted);font-size:14px;font-weight:600}
.node rect{fill:var(--card);stroke:var(--line);stroke-width:1.5}.node.risky rect{stroke:var(--bad);stroke-width:2.5}
.node-label{fill:var(--fg);font-size:15px;font-weight:600}.node-sub{fill:var(--muted);font-size:12px}
.node-ref{fill:var(--accent);font-size:11px;font-family:ui-monospace,Menlo,monospace}
.paid{font-size:16px}
.edge{fill:none;stroke:var(--muted);stroke-width:1.6}.edge.risk{stroke:var(--bad);stroke-width:2.4}
.edge-label{fill:var(--muted);font-size:12px;paint-order:stroke;stroke:var(--card);stroke-width:5px;stroke-linejoin:round}
.edge-label.risk{fill:var(--bad);font-weight:600}
.arrowhead{fill:var(--muted)}.arrowhead.risk{fill:var(--bad)}
.legend{fill:var(--muted);font-size:12px}
/* access matrix */
table{border-collapse:collapse;width:100%}
.matrix th,.matrix td{border-bottom:1px solid var(--line);padding:10px;text-align:left;vertical-align:top}
.matrix thead th{font-size:14px}.matrix th small{display:block;color:var(--muted);font-weight:400;font-size:12px}
.matrix th .req{color:var(--muted)}.matrix th .req.bad{color:var(--bad)}
.cell{min-width:120px}.cell.frame{box-shadow:inset 0 0 0 2.5px var(--bad);border-radius:8px}
.perm{display:flex;gap:8px;font-size:14px}.perm span{color:var(--muted);min-width:2.5em}
.perm b.allow{color:var(--accent)}.perm b.deny{color:var(--muted);font-weight:500}.perm b.unknown{color:var(--unk)}
.conflict-note{color:var(--warn);font-size:13px;margin-top:4px}.probe-note{color:var(--muted);font-size:12px}
.ok-rows summary{cursor:pointer;color:var(--muted);margin:8px 0}
/* timeline */
.tl-band{fill:var(--soft)}.tl-lane{fill:var(--muted);font-size:13px;font-weight:600}
.tl-date{fill:var(--muted);font-size:12px}.tl-date.today{fill:var(--fg);font-weight:700}
.tl-today{fill:none;stroke:var(--line);stroke-dasharray:4 4}
.mk{fill:var(--c);stroke:var(--card);stroke-width:1.5}
.arc,.tl-link{fill:none;stroke:var(--c);stroke-width:1.6;opacity:.75}.tl-link{stroke-dasharray:3 3}
.tl-pill rect{fill:color-mix(in srgb,var(--c) 14%,var(--card));stroke:var(--c);stroke-width:1}
.tl-pill text{fill:var(--fg);font-size:12.5px}
/* paths */
.step rect{fill:var(--card);stroke:var(--line);stroke-width:1.5}.step.warn rect{stroke:var(--warn);stroke-width:2.2}
.step.unverified rect{stroke-dasharray:5 4}.step-label{fill:var(--fg);font-size:13px;font-weight:600}
.step-ref{fill:var(--accent);font-size:11px;font-family:ui-monospace,Menlo,monospace}
.step-warn{fill:var(--warn);font-size:12px}.step-unv{fill:var(--unk);font-size:11px}
.path-title{fill:var(--fg);font-size:14px;font-weight:700}.flow{fill:none;stroke:var(--muted);stroke-width:1.5}
/* cards */
.cards{display:grid;gap:12px;margin-top:12px}
.card{background:var(--card);border:1px solid var(--line);border-left:5px solid var(--c);border-radius:12px;padding:14px 16px}
.card-head{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:6px}
.pill{display:inline-block;padding:2px 10px;border-radius:999px;font-size:13px;font-weight:650;color:var(--c);
  background:color-mix(in srgb,var(--c) 13%,transparent)}
.origin{color:var(--muted);font-size:13px}
.promise{font-weight:650;margin:2px 0}.verdict{margin:2px 0}.verdict-dev{color:var(--muted);font-size:14px;margin:2px 0}
.copy{font:inherit;font-size:13px;margin-top:8px;padding:5px 12px;border-radius:8px;border:1px solid var(--accent);
  background:transparent;color:var(--accent);cursor:pointer}
details.evidence{margin-top:6px}details.evidence summary{cursor:pointer;color:var(--accent);font-size:13px}
.evidence ul{list-style:none;padding:0;margin:6px 0}.ev{border-top:1px dashed var(--line);padding:6px 0}
.ev-head{font-size:12.5px;color:var(--muted)}.ev.failed .ev-head{color:var(--bad)}
.ev blockquote{margin:4px 0;padding-left:10px;border-left:3px solid var(--line)}
.ev pre{white-space:pre-wrap;word-break:break-word;background:var(--soft);padding:6px 8px;border-radius:6px;
  font:12.5px/1.45 ui-monospace,Menlo,monospace;margin:4px 0}
.fail{color:var(--bad);font-size:13px;margin:2px 0}
code{font:0.92em ui-monospace,Menlo,monospace}
/* ledger table */
.filters{display:flex;flex-wrap:wrap;gap:6px;margin:8px 0}
.filter{font:inherit;font-size:13px;padding:4px 10px;border-radius:999px;border:1px solid var(--line);
  background:var(--card);color:var(--fg);cursor:pointer}.filter.on{border-color:var(--accent);color:var(--accent)}
.ledger th,.ledger td{border-bottom:1px solid var(--line);padding:9px 8px;text-align:left;vertical-align:top;font-size:14px}
/* coverage */
.coverage{padding-left:20px}.coverage li{margin:4px 0}.coverage .warn{color:var(--warn)}.coverage ul{padding-left:18px}
@media (max-width:600px){header h1{font-size:23px}h2{font-size:19px}.count{font-size:13px}.ledger td,.ledger th{font-size:13px}}
```

- [ ] **Step 7: Write `scripts/ledger_report/assets/report.js`**

```javascript
(function () {
  var root = document.documentElement;
  try {
    var q = new URLSearchParams(location.search);
    if (q.get("theme")) root.setAttribute("data-theme", q.get("theme"));
    if (q.get("view") === "dev") document.body.classList.add("dev");
  } catch (e) {}
  var toggle = document.getElementById("view-toggle");
  if (toggle) toggle.addEventListener("click", function () {
    var on = document.body.classList.toggle("dev");
    toggle.setAttribute("aria-pressed", on ? "true" : "false");
  });
  document.querySelectorAll("[data-filter]").forEach(function (b) {
    b.addEventListener("click", function () {
      var s = b.getAttribute("data-filter");
      document.querySelectorAll("[data-filter]").forEach(function (x) { x.classList.toggle("on", x === b); });
      document.querySelectorAll("tr[data-status]").forEach(function (r) {
        r.hidden = s !== "all" && r.getAttribute("data-status") !== s;
      });
    });
  });
  function done(b) { b.textContent = b.getAttribute("data-done"); }
  document.querySelectorAll("button.copy").forEach(function (b) {
    b.addEventListener("click", function () {
      var text = b.getAttribute("data-text");
      var fallback = function () {
        var a = document.createElement("textarea");
        a.value = text; document.body.appendChild(a); a.select();
        try { document.execCommand("copy"); done(b); } catch (e) {}
        a.remove();
      };
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(function () { done(b); }, fallback);
      else fallback();
    });
  });
})();
```

- [ ] **Step 8: Write the four diagram stubs (filled in Tasks 11–12)**

`scripts/ledger_report/map_svg.py`:
```python
"""Diagram A — filled in by Task 11."""
from ledger_report.bits import h
from ledger_report.i18n import t


def render_map(ledger, lang):
    return f'<p class="empty">{h(t(lang, "no_map"))}</p>'
```

`scripts/ledger_report/access_html.py`:
```python
"""Diagram B — filled in by Task 11."""
from ledger_report.bits import h
from ledger_report.i18n import t


def render_access(ledger, lang):
    return f'<p class="empty">{h(t(lang, "no_database"))}</p>'
```

`scripts/ledger_report/timeline_svg.py`:
```python
"""Diagram C — filled in by Task 12."""
from ledger_report.bits import h
from ledger_report.i18n import t


def render_timeline(ledger, lang, has_transcripts):
    return f'<p class="empty">{h(t(lang, "no_transcripts_timeline"))}</p>'
```

`scripts/ledger_report/paths_svg.py`:
```python
"""Diagram E — filled in by Task 12."""
from ledger_report.bits import h
from ledger_report.i18n import t


def render_paths(ledger, lang):
    return f'<p class="empty">{h(t(lang, "no_paths"))}</p>'
```

- [ ] **Step 9: Write `scripts/render.py`**

```python
"""Render the verified ledger as one self-contained, offline HTML page."""
from __future__ import annotations

import os
from collections import Counter
from datetime import datetime
from pathlib import Path

from common import slugify
from ledger_report.access_html import render_access
from ledger_report.bits import GLYPH, ORDER, evidence_html, fmt_date, h, ht
from ledger_report.i18n import t
from ledger_report.map_svg import render_map
from ledger_report.paths_svg import render_paths
from ledger_report.timeline_svg import render_timeline
from redact import find_secrets

ASSETS = Path(__file__).resolve().parent / "ledger_report" / "assets"
SECTIONS = (("sec_map", ("where_data", "what_costs"), "map"),
            ("sec_access", ("who_can_see",), "access"),
            ("sec_timeline", ("what_breaks", "open_debts"), "timeline"))
FIXABLE = ("broken", "partial", "pending")
STORES = ("database", "storage")


def counts(ledger: dict) -> dict:
    c = Counter(p["status"] for p in ledger["promises"])
    return {s: c.get(s, 0) for s in ORDER}


def summaries(ledger: dict, lang: str) -> dict:
    """Deterministic one-liners built from verified data only."""
    sep = t(lang, "sep")
    nodes = ledger["map"]["nodes"]
    stores = [n["label"] for n in nodes if n["kind"] in STORES]
    sent = [n["label"] for n in nodes if n["kind"] == "third_party"]
    paid = [n["label"] for n in nodes if n.get("paid")]
    where = t(lang, "sum_where", stores=sep.join(stores)) if stores else t(lang, "sum_where_none")
    if sent:
        where += t(lang, "sum_sent", others=sep.join(sent))
    res = ledger["access"]["resources"]
    anon = sum(1 for r in res if r["cells"].get("anonymous", {}).get("read") == "allow")
    conflicts = sum(len(c.get("conflicts", [])) for r in res for c in r["cells"].values())
    return {
        "where_data": where,
        "what_costs": t(lang, "sum_costs", paid=sep.join(paid)) if paid else t(lang, "sum_costs_none"),
        "who_can_see": t(lang, "sum_access", n=len(res), anon=anon, conflicts=conflicts) if res else t(lang, "no_database"),
        "what_breaks": t(lang, "sum_breaks", comp=sum(1 for c in ledger["compromises"] if c.get("still_present") is True),
                         broken=sum(1 for p in ledger["promises"] if p["status"] == "broken")),
        "open_debts": t(lang, "sum_debts", n=sum(1 for p in ledger["promises"]
                                                 if p["type"] == "deferred" and p["status"] == "pending")),
    }


def _origin(p: dict, ev: dict, lang: str) -> str:
    for i in p["source"]:
        e = ev.get(i, {})
        if e.get("ok"):
            who = t(lang, "said_by_user") if e.get("role") == "user" else t(lang, "said_by_ai")
            return t(lang, "said_on", who=who, date=fmt_date(e.get("ts")))
    return ""


def _card(p: dict, ev: dict, lang: str) -> str:
    s = p["status"]
    out = [f'<article class="card s-{s}" id="{h(p["id"])}">',
           f'<div class="card-head"><span class="pill s-{s}">{GLYPH[s]} {h(t(lang, "status_" + s))}</span>'
           f'<span class="origin">{h(_origin(p, ev, lang))}</span></div>',
           f'<p class="promise">{h(p["plain"])}</p>',
           f'<p class="verdict">{h(p["verdict_plain"])}</p>',
           f'<p class="verdict-dev dev-only">{h(p["verdict_dev"])}</p>']
    if p.get("downgraded_from"):
        old = t(lang, "status_" + p["downgraded_from"])
        out.append(f'<p class="note">{h(t(lang, "downgraded", old=old))}</p>')
    if p.get("conflict_with"):
        out.append(f'<p class="note">{h(t(lang, "conflict"))}{h(t(lang, "colon"))}{h(", ".join(p["conflict_with"]))}</p>')
    out.append(evidence_html(p["source"] + p["evidence"], ev, lang))
    if s in FIXABLE and p.get("fix_prompt"):
        out.append(f'<button class="copy" type="button" data-text="{h(p["fix_prompt"])}" '
                   f'data-done="{h(t(lang, "copied"))}">{h(t(lang, "copy_fix"))}</button>')
    out.append("</article>")
    return "".join(out)


def _ledger_table(ledger: dict, lang: str) -> str:
    ev = ledger["evidence"]
    rows = []
    for p in sorted(ledger["promises"], key=lambda p: ORDER.index(p["status"])):
        s = p["status"]
        rows.append(f'<tr data-status="{s}"><td><span class="pill s-{s}">{GLYPH[s]} {h(t(lang, "status_" + s))}</span></td>'
                    f'<td>{h(p["plain"])}{evidence_html(p["source"] + p["evidence"], ev, lang)}</td>'
                    f'<td>{h(_origin(p, ev, lang))}</td>'
                    f'<td>{h(p["verdict_plain"])}<div class="dev-only">{h(p["verdict_dev"])}</div></td></tr>')
    if not rows:
        return f'<p class="empty">{h(t(lang, "no_promises"))}</p>'
    c = counts(ledger)
    buttons = (f'<button type="button" class="filter on" data-filter="all">{h(t(lang, "filter_all"))}</button>'
               + "".join(f'<button type="button" class="filter" data-filter="{s}">{GLYPH[s]} {c[s]}</button>'
                         for s in ORDER if c[s]))
    head = "".join(f"<th>{h(t(lang, k))}</th>" for k in ("col_status", "col_promise", "col_who", "col_verdict"))
    return (f'<div class="filters">{buttons}</div><div class="matrix-wrap"><table class="ledger">'
            f'<thead><tr>{head}</tr></thead><tbody>{"".join(rows)}</tbody></table></div>')


def _coverage(ledger: dict, run: dict, probes: dict, lang: str) -> str:
    s = run.get("sessions", {})
    by = s.get("by_agent", {})
    li = [h(t(lang, "cov_sessions", claude=by.get("claude-code", 0), codex=by.get("codex", 0)))]
    if s.get("archived_threads"):
        li.append(h(t(lang, "cov_archived", n=s["archived_threads"])))
    ignored = sum((s.get("ignored_types") or {}).values())
    if ignored:
        li.append(h(t(lang, "cov_ignored", n=ignored)))
    if s.get("bad_lines"):
        li.append(h(t(lang, "cov_bad", n=s["bad_lines"])))
    un = run.get("unattributed", [])
    if un:
        files = "".join(f"<li><code>{ht(f, 90)}</code></li>" for f in un[:20]) + ("<li>…</li>" if len(un) > 20 else "")
        li.append(f'{h(t(lang, "cov_unattributed", n=len(un)))}<ul>{files}</ul>')
    li.append(h(t(lang, "cov_probes", ran=", ".join(probes.get("ran", [])) or t(lang, "cov_none"))))
    if probes.get("skipped"):
        skipped = "; ".join(f'{x["probe"]} ({x["reason"]})' for x in probes["skipped"])
        li.append(h(t(lang, "cov_skipped", skipped=skipped)))
    unsupported = probes.get("stack", {}).get("unsupported", [])
    items = [f"<li>{x}</li>" for x in li]
    if unsupported:
        items.append(f'<li class="warn">{h(t(lang, "cov_unsupported", stacks=", ".join(unsupported)))}</li>')
    failed = [(k, e) for k, e in ledger["evidence"].items() if not e.get("ok")]
    if failed:
        sub = "".join(f'<li><code>{h(k)}</code> {ht(e.get("reason", ""), 160)}</li>' for k, e in failed[:30])
        items.append(f'<li>{h(t(lang, "cov_failed", n=len(failed)))}<ul>{sub}</ul></li>')
    rejected = ledger.get("rejected", [])
    if rejected:
        sub = "".join(f'<li>{ht(r.get("plain") or r.get("id", ""), 120)} — {ht(r.get("reason", ""), 160)}</li>'
                      for r in rejected[:30])
        items.append(f'<li>{h(t(lang, "cov_rejected", n=len(rejected)))}<ul>{sub}</ul></li>')
    warnings = s.get("warnings", [])
    if warnings:
        sub = "".join(f"<li>{ht(w, 200)}</li>" for w in warnings[:20])
        items.append(f'<li class="warn">{h(t(lang, "cov_warnings"))}<ul>{sub}</ul></li>')
    return f'<ul class="coverage">{"".join(items)}</ul>'


def assert_no_secrets(doc: str) -> None:
    leaks = find_secrets(doc)
    if leaks:
        kinds = ", ".join(sorted({k for _, _, k in leaks}))
        raise RuntimeError(f"refusing to write the report: it would contain {len(leaks)} unmasked secret(s) ({kinds})")


def render_html(ledger: dict, run: dict, probes: dict, lang: str) -> str:
    ev = ledger["evidence"]
    c = counts(ledger)
    sums = summaries(ledger, lang)
    s = run.get("sessions", {})
    has_tx = bool(s.get("records"))
    sub = (t(lang, "subtitle", threads=s.get("threads", 0), start=fmt_date(s.get("earliest"))[:10],
             end=fmt_date(s.get("latest"))[:10]) if has_tx else t(lang, "subtitle_none"))
    name = run.get("project_name", "")
    body = [f'<header><h1>{h(t(lang, "title", name=name))}</h1><p class="sub">{h(sub)}</p>'
            f'<button id="view-toggle" class="toggle" type="button" aria-pressed="false">'
            f'<span class="plain-only">{h(t(lang, "view_dev"))}</span><span class="dev-only">{h(t(lang, "view_plain"))}</span></button>'
            '<div class="counts">'
            + "".join(f'<span class="count s-{st}">{GLYPH[st]} {h(t(lang, "status_" + st))} <b>{c[st]}</b></span>' for st in ORDER)
            + "</div></header>"]
    diagrams = {"map": render_map(ledger, lang), "access": render_access(ledger, lang),
                "timeline": render_timeline(ledger, lang, has_tx)}
    for title, questions, key in SECTIONS:
        part = [f"<section><h2>{h(t(lang, title))}</h2>"]
        part += [f'<p class="summary"><b>{h(t(lang, "q_" + q))}{h(t(lang, "colon"))}</b>{h(sums[q])}</p>' for q in questions]
        part.append(diagrams[key])
        cards = sorted((p for p in ledger["promises"] if p["question"] in questions), key=lambda p: ORDER.index(p["status"]))
        if cards:
            part.append('<div class="cards">' + "".join(_card(p, ev, lang) for p in cards) + "</div>")
        part.append("</section>")
        body.append("".join(part))
    body.append(f'<section class="dev-only"><h2>{h(t(lang, "sec_paths"))}</h2>{render_paths(ledger, lang)}</section>')
    body.append(f'<section><h2>{h(t(lang, "sec_ledger"))}</h2>{_ledger_table(ledger, lang)}</section>')
    body.append(f'<section><h2>{h(t(lang, "sec_coverage"))}</h2>{_coverage(ledger, run, probes, lang)}</section>')
    css = (ASSETS / "report.css").read_text(encoding="utf-8")
    js = (ASSETS / "report.js").read_text(encoding="utf-8")
    html_lang = "zh-CN" if lang == "zh" else "en"
    doc = (f'<!doctype html><html lang="{html_lang}"><head><meta charset="utf-8">'
           f'<meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>{h(t(lang, "doc_title", name=name))}</title><style>{css}</style></head>'
           f'<body><div class="wrap">{"".join(body)}</div><script>{js}</script></body></html>')
    assert_no_secrets(doc)
    return doc


def deliver(html: str, run_dir, project_name: str, out_dir=None) -> Path:
    """Write the report to the run folder and to where the user will look."""
    run_dir = Path(run_dir)
    (run_dir / "report.html").write_text(html, encoding="utf-8")
    name = f"vibe-ledger-{slugify(project_name)}-{datetime.now().strftime('%Y%m%d-%H%M')}.html"
    env = os.environ.get("VIBE_LEDGER_OUT_DIR")
    if out_dir:
        targets = [(Path(out_dir), True)]
    elif env:
        targets = [(Path(env), True)]
    else:
        targets = [(Path.home() / "Desktop", False), (Path.home() / "Downloads", False)]
    for folder, create in targets:
        try:
            if create:
                folder.mkdir(parents=True, exist_ok=True)
            if folder.is_dir():
                target = folder / name
                target.write_text(html, encoding="utf-8")
                return target
        except OSError:
            continue  # e.g. macOS privacy settings can block Desktop/Downloads
    return run_dir / "report.html"
```

- [ ] **Step 10: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_render_page.py`
Expected: PASS.

- [ ] **Step 11: Commit**

```bash
git add scripts/ledger_report/__init__.py scripts/ledger_report/bits.py scripts/ledger_report/i18n.py scripts/ledger_report/assets/report.css scripts/ledger_report/assets/report.js scripts/ledger_report/map_svg.py scripts/ledger_report/access_html.py scripts/ledger_report/timeline_svg.py scripts/ledger_report/paths_svg.py scripts/render.py tests/helpers/verified.py tests/test_render_page.py
git commit -m "feat: report page with cards, ledger table, coverage and safe delivery"
```

---
### Task 11: Diagram A (app map) and diagram B (access matrix)

**Files:**
- Modify (replace the Task 10 stubs): `scripts/ledger_report/map_svg.py`, `scripts/ledger_report/access_html.py`
- Test: `tests/test_render_map_access.py`

**Interfaces:**
- Consumes: `ledger_report.bits.{h, ht, GLYPH, evidence_html}`, `ledger_report.i18n.t` (Task 10); `helpers.verified.sample` (Task 10).
- Produces:
  - `map_svg.MAX_NODES = 12`, `map_svg.select_nodes(map_section) -> (shown, overflow)` (risky nodes first, then paid, then most evidence), `map_svg.render_map(ledger, lang) -> str` — an inline `<svg class="diagram map">` inside `<div class="diagram-wrap">`, three fixed lanes, followed by "others" and "unverified" notes.
  - `access_html.SUBJECTS = ("anonymous", "signed_in", "owner")`, `access_html.is_problem(resource, statuses) -> bool`, `access_html.render_access(ledger, lang) -> str` — problem rows in the main table, the rest folded in `<details class="ok-rows">`.

- [ ] **Step 1: Write the failing tests**

`tests/test_render_map_access.py`:
```python
import re

from helpers.verified import sample
from ledger_report import access_html, map_svg


def svg_part(html):
    return html[html.index("<svg"):html.index("</svg>")]


def test_map_lanes_nodes_edges_and_legend():
    html = map_svg.render_map(sample(), "zh")
    svg = svg_part(html)
    for label in ("浏览器", "你的服务器", "存储与第三方服务", "首页", "/api/summarize", "Supabase", "OpenAI"):
        assert label in svg
    assert svg.count('<g class="node') == 4
    assert svg.count("<path class=\"edge") == 3
    assert svg.count('class="edge risk"') == 1 and "陌生人也能读" in svg
    assert svg.count("💰") == 2  # the OpenAI node and the legend
    assert 'class="node-ref dev-only"' in svg and "supabase/migrations/001.sql:3" in svg


def test_unverified_nodes_are_listed_not_drawn():
    html = map_svg.render_map(sample(), "zh")
    assert "Stripe" not in svg_part(html)
    assert "未核实，没画进图里" in html and "Stripe" in html


def test_map_caps_nodes_and_lists_overflow():
    led = sample()
    led["map"]["nodes"] = [{"id": f"n{i}", "lane": "server", "kind": "function", "label": f"fn{i}", "holds": [],
                            "paid": False, "evidence": ["E2"]} for i in range(15)]
    led["map"]["edges"] = []
    html = map_svg.render_map(led, "en")
    assert svg_part(html).count('<g class="node') == map_svg.MAX_NODES
    assert "Others (no room on the map)" in html and "fn14" in html


def test_select_nodes_puts_risky_and_paid_first():
    m = sample()["map"]
    shown, overflow = map_svg.select_nodes(m)
    assert [n["id"] for n in shown][:2] == ["web", "db"] and shown[2]["id"] == "ai" and overflow == []


def test_empty_map():
    led = sample()
    led["map"] = {"nodes": [], "edges": [], "unverified_nodes": [], "unverified_edges": []}
    assert "没能从代码里确认任何数据去向" in map_svg.render_map(led, "zh")


def test_map_svg_coordinates_are_finite_numbers():
    svg = svg_part(map_svg.render_map(sample(), "zh"))
    for num in re.findall(r'(?:x|y|width|height)="([^"]+)"', svg):
        float(num)


def test_access_matrix_rows_cells_and_frames():
    html = access_html.render_access(sample(), "zh")
    main = html.split('<details class="ok-rows">')[0]
    assert "notes" in main and "陌生人" in main and "其他登录用户" in main and "本人" in main
    assert main.count('class="cell frame') == 2  # anonymous + signed_in on a broken requirement
    assert "只有我自己能看到我的笔记" in main and "❌" in main
    assert '<details class="ok-rows">' in html and "其余 1 类数据" in html and "profiles" in html.split("ok-rows")[1]


def test_access_conflicts_unknown_and_probe_notes():
    led = sample()
    cells = led["access"]["resources"][0]["cells"]
    cells["anonymous"] = {"read": "deny", "write": "unknown", "evidence": ["E2"], "from_probe": ["secrets_exposed:.env.local:2"],
                          "conflicts": [{"perm": "read", "probe": "p", "probe_says": "allow", "ledger_says": "deny",
                                         "message": "RLS is off for notes"}]}
    html = access_html.render_access(led, "zh")
    assert "说法冲突" in html and "RLS is off for notes" in html
    assert 'class="unknown"' in html and 'class="probe-note dev-only"' in html


def test_star_resource_and_empty():
    led = sample()
    led["access"]["resources"] = [{"name": "*", "required_by": None, "cells": {
        "anonymous": {"read": "allow", "write": "allow", "evidence": []}}}]
    assert "所有数据" in access_html.render_access(led, "zh")
    led["access"]["resources"] = []
    assert "没有检测到数据库" in access_html.render_access(led, "zh")


def test_is_problem():
    statuses = {"P1": "broken", "P4": "kept"}
    ok = {"name": "x", "required_by": "P4", "cells": {"anonymous": {"read": "deny", "write": "deny"}}}
    assert not access_html.is_problem(ok, statuses)
    assert access_html.is_problem({**ok, "required_by": "P1"}, statuses)
    assert access_html.is_problem({"name": "y", "cells": {"anonymous": {"read": "allow", "write": "deny"}}}, statuses)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_render_map_access.py`
Expected: FAIL — the stubs return only the empty-state paragraph.

- [ ] **Step 3: Write `scripts/ledger_report/map_svg.py`**

```python
"""Diagram A: where the data goes. Three fixed lanes (browser | your server |
storage & outside services) so the layout is the same every time."""
from __future__ import annotations

from ledger_report.bits import h, ht
from ledger_report.i18n import t

LANES = ("browser", "server", "storage")
MAX_NODES = 12
WIDTH, LANE_W = 960, 290
LANE_X = (15, 335, 655)
NODE_H, GAP, TOP = 66, 18, 62


def _risky(m: dict) -> set:
    ids = set()
    for e in m["edges"]:
        if e.get("risk"):
            ids.update((e["from"], e["to"]))
    return ids


def select_nodes(m: dict) -> tuple[list, list]:
    risky = _risky(m)
    ranked = sorted(m["nodes"], key=lambda n: (n["id"] not in risky, not n.get("paid"), -len(n.get("evidence", []))))
    return ranked[:MAX_NODES], ranked[MAX_NODES:]


def _code_ref(node: dict, evidence: dict) -> str:
    for eid in node.get("evidence", []):
        e = evidence.get(eid, {})
        if e.get("ok") and e.get("kind") in ("code", "probe") and e.get("path"):
            return f"{e['path']}:{e.get('line', '')}"
    return ""


def _edge(a: tuple, b: tuple, e: dict) -> str:
    (ax, ay), (bx, by) = a, b
    if ax < bx:
        x1, x2 = ax + LANE_W, bx
    elif ax > bx:
        x1, x2 = ax, bx + LANE_W
    else:
        x1 = x2 = ax + LANE_W
    y1, y2 = ay + NODE_H / 2, by + NODE_H / 2
    if x1 == x2:
        d = f"M{x1},{y1:.1f} C{x1 + 46},{y1:.1f} {x2 + 46},{y2:.1f} {x2},{y2:.1f}"
        mx = x1 + 40
    else:
        dx = (x2 - x1) / 2
        d = f"M{x1},{y1:.1f} C{x1 + dx:.1f},{y1:.1f} {x2 - dx:.1f},{y2:.1f} {x2},{y2:.1f}"
        mx = (x1 + x2) / 2
    risk = bool(e.get("risk"))
    label = e.get("carries") or ""
    if risk:
        label = f"⚠ {label} — {e['risk']}" if label else f"⚠ {e['risk']}"
    marker = "arrow-map-risk" if risk else "arrow-map"
    return (f'<path class="edge{" risk" if risk else ""}" d="{d}" marker-end="url(#{marker})"/>'
            f'<text class="edge-label{" risk" if risk else ""}" x="{mx:.1f}" y="{(y1 + y2) / 2 - 7:.1f}" '
            f'text-anchor="middle">{ht(label, 36)}</text>')


def _notes(overflow: list, unverified: list, lang: str) -> str:
    sep = h(t(lang, "sep"))
    out = ""
    if overflow:
        out += f'<p class="note">{h(t(lang, "other_nodes"))}' + sep.join(ht(n["label"], 30) for n in overflow) + "</p>"
    if unverified:
        out += (f'<p class="note unverified">{h(t(lang, "unverified_nodes"))}'
                + sep.join(ht(n["label"], 30) for n in unverified) + "</p>")
    return out


def render_map(ledger: dict, lang: str) -> str:
    m, ev = ledger["map"], ledger["evidence"]
    shown, overflow = select_nodes(m)
    notes = _notes(overflow, m.get("unverified_nodes", []), lang)
    if not shown:
        return f'<p class="empty">{h(t(lang, "no_map"))}</p>' + notes
    risky = _risky(m)
    pos, used = {}, {lane: 0 for lane in LANES}
    for n in shown:
        i = used[n["lane"]]
        used[n["lane"]] += 1
        pos[n["id"]] = (LANE_X[LANES.index(n["lane"])], TOP + i * (NODE_H + GAP))
    height = TOP + max(used.values()) * (NODE_H + GAP) + 34
    out = [f'<div class="diagram-wrap"><svg class="diagram map" viewBox="0 0 {WIDTH} {height}" role="img" '
           f'aria-label="{h(t(lang, "sec_map"))}"><defs>'
           '<marker id="arrow-map" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="8" markerHeight="8" orient="auto">'
           '<path class="arrowhead" d="M0,0 L8,4 L0,8 z"/></marker>'
           '<marker id="arrow-map-risk" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="8" markerHeight="8" orient="auto">'
           '<path class="arrowhead risk" d="M0,0 L8,4 L0,8 z"/></marker></defs>']
    for i, lane in enumerate(LANES):
        x = LANE_X[i]
        out.append(f'<rect class="lane" x="{x - 6}" y="12" width="{LANE_W + 12}" height="{height - 40}" rx="14"/>')
        out.append(f'<text class="lane-title" x="{x + LANE_W / 2:.1f}" y="40" text-anchor="middle">{h(t(lang, "lane_" + lane))}</text>')
    for e in m["edges"]:
        if e["from"] in pos and e["to"] in pos:
            out.append(_edge(pos[e["from"]], pos[e["to"]], e))
    for n in shown:
        x, y = pos[n["id"]]
        out.append(f'<g class="node{" risky" if n["id"] in risky else ""}">'
                   f'<rect x="{x}" y="{y}" width="{LANE_W}" height="{NODE_H}" rx="10"/>'
                   f'<text class="node-label" x="{x + 14}" y="{y + 24}">{ht(n["label"], 26)}</text>')
        holds = ", ".join(n.get("holds", []))
        if holds:
            out.append(f'<text class="node-sub" x="{x + 14}" y="{y + 43}">{ht(holds, 40)}</text>')
        ref = _code_ref(n, ev)
        if ref:
            out.append(f'<text class="node-ref dev-only" x="{x + 14}" y="{y + 59}">{ht(ref, 44)}</text>')
        if n.get("paid"):
            out.append(f'<text class="paid" x="{x + LANE_W - 12}" y="{y + 24}" text-anchor="end">💰</text>')
        out.append("</g>")
    out.append(f'<text class="legend" x="15" y="{height - 10}">{h(t(lang, "legend_map"))}</text></svg></div>')
    return "".join(out) + notes
```

- [ ] **Step 4: Write `scripts/ledger_report/access_html.py`**

```python
"""Diagram B: who can see what. A matrix is the honest encoding here: rows
are kinds of data, columns are who is asking."""
from __future__ import annotations

from ledger_report.bits import GLYPH, evidence_html, h, ht
from ledger_report.i18n import t

SUBJECTS = ("anonymous", "signed_in", "owner")
BAD = ("broken", "partial")


def is_problem(r: dict, statuses: dict) -> bool:
    if statuses.get(r.get("required_by")) in BAD:
        return True
    for subject, cell in r.get("cells", {}).items():
        if cell.get("conflicts"):
            return True
        if subject == "anonymous" and "allow" in (cell.get("read"), cell.get("write")):
            return True
    return False


def _row(r: dict, statuses: dict, plains: dict, ev: dict, lang: str) -> str:
    req = r.get("required_by")
    bad_req = statuses.get(req) in BAD
    name = t(lang, "all_data") if r["name"] == "*" else r["name"]
    th = f'<th scope="row">{ht(name, 40)}'
    if req:
        th += (f'<small class="req{" bad" if bad_req else ""}">{h(t(lang, "required"))}{ht(plains.get(req, ""), 40)} '
               f'{GLYPH.get(statuses.get(req, "unknown"), "")}</small>')
    th += "</th>"
    tds = []
    for s in SUBJECTS:
        cell = r.get("cells", {}).get(s, {"read": "unknown", "write": "unknown", "evidence": []})
        frame = bad_req and s != "owner" and "allow" in (cell.get("read"), cell.get("write"))
        cls = "cell" + (" frame" if frame else "") + (" conflict" if cell.get("conflicts") else "")
        body = "".join(f'<div class="perm"><span>{h(t(lang, "perm_" + p))}</span>'
                       f'<b class="{cell.get(p, "unknown")}">{h(t(lang, cell.get(p, "unknown")))}</b></div>'
                       for p in ("read", "write"))
        for cf in cell.get("conflicts", []):
            body += (f'<div class="conflict-note">⚠ {h(t(lang, "conflict"))}{h(t(lang, "colon"))}'
                     f'{h(t(lang, "probe_says", msg=cf["message"]))}</div>')
        if cell.get("from_probe"):
            body += f'<div class="probe-note dev-only">{h(t(lang, "probe"))}{h(t(lang, "colon"))}{ht(", ".join(cell["from_probe"]), 80)}</div>'
        body += evidence_html(cell.get("evidence", []), ev, lang)
        tds.append(f'<td class="{cls}">{body}</td>')
    return f"<tr>{th}{''.join(tds)}</tr>"


def render_access(ledger: dict, lang: str) -> str:
    resources = ledger["access"]["resources"]
    if not resources:
        return f'<p class="empty">{h(t(lang, "no_database"))}</p>'
    statuses = {p["id"]: p["status"] for p in ledger["promises"]}
    plains = {p["id"]: p["plain"] for p in ledger["promises"]}
    ev = ledger["evidence"]
    head = "<tr><th></th>" + "".join(f'<th>{h(t(lang, "subj_" + s))}<small>{h(t(lang, "subj_" + s + "_sub"))}</small></th>'
                                     for s in SUBJECTS) + "</tr>"
    problems = [r for r in resources if is_problem(r, statuses)]
    fine = [r for r in resources if not is_problem(r, statuses)]

    def table(rows) -> str:
        return (f'<div class="matrix-wrap"><table class="matrix"><thead>{head}</thead><tbody>'
                + "".join(_row(r, statuses, plains, ev, lang) for r in rows) + "</tbody></table></div>")

    out = table(problems) if problems else ""
    if fine:
        out += f'<details class="ok-rows"><summary>{h(t(lang, "ok_rows", n=len(fine)))}</summary>{table(fine)}</details>'
    return out
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_render_map_access.py tests/test_render_page.py`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/ledger_report/map_svg.py scripts/ledger_report/access_html.py tests/test_render_map_access.py
git commit -m "feat: app map and access matrix diagrams"
```

---
### Task 12: Diagram C (conversation timeline) and diagram E (call paths)

**Files:**
- Modify (replace the Task 10 stubs): `scripts/ledger_report/timeline_svg.py`, `scripts/ledger_report/paths_svg.py`
- Test: `tests/test_render_timeline_paths.py`

**Interfaces:**
- Consumes: `ledger_report.bits.{h, ht, GLYPH, ORDER}`, `ledger_report.i18n.t` (Task 10); `helpers.verified.sample`.
- Produces:
  - `timeline_svg.LANES = ("you_said", "error", "ai_changed", "deferred")`, `timeline_svg.MAX_ITEMS = 16`, `timeline_svg.build_items(ledger) -> (items, overflow)` — one item per promise with a passing source and per compromise with a passing error or change; item = `{"key", "status", "label", "lane", "events": [(ts, lane, quote)], "compromise": bool, "still"?}`; compromise status = `broken` if still present, `kept` if gone, `unknown` if unclear; items sorted by status severity then time.
  - `timeline_svg.render_timeline(ledger, lang, has_transcripts) -> str` — `<div class="scroll-x"><svg class="diagram timeline" …>`: four lanes, events in time order (evenly spaced, so gaps are compressed), date ticks when the day changes, a "today" column with one status pill per item, an arc from each item's last event to its pill.
  - `paths_svg.PER_ROW = 4`, `paths_svg.render_paths(ledger, lang) -> str` — one `<svg class="diagram paths">` per path: step boxes in rows of four, arrows between them, `⚠` text under warned steps, dashed boxes marked unverified.

- [ ] **Step 1: Write the failing tests**

`tests/test_render_timeline_paths.py`:
```python
import re

from helpers.verified import sample
from ledger_report import paths_svg, timeline_svg


def test_build_items_order_and_compromise_status():
    items, overflow = timeline_svg.build_items(sample())
    assert [it["key"] for it in items] == ["P1", "C1", "P2", "P3", "P4"]
    c1 = items[1]
    assert c1["compromise"] and c1["status"] == "broken" and [e[1] for e in c1["events"]] == ["error", "ai_changed"]
    assert items[2]["lane"] == "deferred" and items[3]["lane"] == "ai_changed" and overflow == []


def test_timeline_svg_contents():
    html = timeline_svg.render_timeline(sample(), "zh", True)
    for word in ("你说的", "报错", "AI 改的", "以后再说", "今天", "09-12", "09-13"):
        assert word in html
    assert html.count('<g class="tl-pill') == 5
    assert html.count('class="mk s-') == 6
    assert html.count('class="arc s-') == 5 and html.count('class="tl-link s-') == 1
    assert "妥协: RLS · 仍在代码里" in html
    assert "<title>只有我自己能看到我的笔记</title>" in html


def test_timeline_without_transcripts_or_items():
    assert "没找到对话记录" in timeline_svg.render_timeline(sample(), "zh", False)
    led = sample()
    for e in led["evidence"].values():
        if e["kind"] == "transcript":
            e["ok"] = False
    assert "能核实的事件" in timeline_svg.render_timeline(led, "zh", True)


def test_timeline_overflow_note():
    led = sample()
    base = led["promises"][3]
    led["promises"] += [{**base, "id": f"X{i}"} for i in range(20)]
    items, overflow = timeline_svg.build_items(led)
    assert len(items) == timeline_svg.MAX_ITEMS and overflow
    assert "放不下" in timeline_svg.render_timeline(led, "zh", True)


def test_timeline_dimensions_are_numbers():
    html = timeline_svg.render_timeline(sample(), "en", True)
    w, h = re.search(r'viewBox="0 0 (\d+) (\d+(?:\.\d+)?)"', html).groups()
    assert int(w) > 400 and float(h) > 200


def test_paths_steps_warnings_and_unverified():
    html = paths_svg.render_paths(sample(), "zh")
    assert html.count('<g class="step') == 3
    assert 'class="step warn"' in html and "⚠ 没有登录检查" in html
    assert 'class="step unverified"' in html and "未核实" in html
    assert "app/api/summarize/route.ts:3" in html and "点“AI 总结”" in html
    assert html.count('class="flow"') == 2


def test_paths_wrap_rows():
    led = sample()
    step = led["paths"][0]["steps"][0]
    led["paths"] = [{"action": "long", "steps": [{**step, "label": f"s{i}"} for i in range(6)]}]
    html = paths_svg.render_paths(led, "en")
    assert html.count('<g class="step') == 6 and html.count('class="flow"') == 5


def test_paths_empty():
    led = sample()
    led["paths"] = []
    assert "没有可展示的操作路径" in paths_svg.render_paths(led, "zh")
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_render_timeline_paths.py`
Expected: FAIL — `AttributeError: module 'ledger_report.timeline_svg' has no attribute 'build_items'`.

- [ ] **Step 3: Write `scripts/ledger_report/timeline_svg.py`**

```python
"""Diagram C: the conversation over time. Four lanes (you said / error /
AI changed / for later) and a 'today' column showing where each item stands."""
from __future__ import annotations

from collections import Counter

from ledger_report.bits import GLYPH, ORDER, h, ht
from ledger_report.i18n import t

LANES = ("you_said", "error", "ai_changed", "deferred")
LANE_OF_TYPE = {"user_requirement": "you_said", "ai_claim": "ai_changed", "deferred": "deferred"}
MAX_ITEMS = 16
X0, TODAY_W, PILL_H, TOP = 130, 270, 24, 58
COMPROMISE_STATUS = {True: "broken", False: "kept", None: "unknown"}


def build_items(ledger: dict) -> tuple[list, list]:
    ev = ledger["evidence"]
    items = []
    for p in ledger["promises"]:
        src = next((ev[i] for i in p["source"] if ev.get(i, {}).get("ok")), None)
        if src is None:
            continue
        lane = LANE_OF_TYPE[p["type"]]
        items.append({"key": p["id"], "status": p["status"], "label": p["plain"], "lane": lane,
                      "events": [(src.get("ts", ""), lane, src.get("quote", ""))], "compromise": False})
    for c in ledger["compromises"]:
        events = []
        err = ev.get(c["error"], {})
        if err.get("ok"):
            events.append((err.get("ts", ""), "error", err.get("quote", "")))
        change = next((ev[i] for i in c["change"] if ev.get(i, {}).get("ok")), None)
        if change:
            events.append((change.get("ts", ""), "ai_changed", change.get("quote", "")))
        if events:
            items.append({"key": c["id"], "status": COMPROMISE_STATUS[c.get("still_present")],
                          "label": c.get("bypassed", ""), "lane": "error", "events": events,
                          "compromise": True, "still": c.get("still_present")})
    items.sort(key=lambda it: (ORDER.index(it["status"]), min(e[0] for e in it["events"])))
    return items[:MAX_ITEMS], items[MAX_ITEMS:]


def _marker(lane: str, x: float, y: float, status: str, quote: str) -> str:
    cls = f"mk s-{status}"
    tip = f"<title>{ht(quote, 160)}</title>"
    if lane == "you_said":
        return f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="7">{tip}</circle>'
    if lane == "error":
        return f'<path class="{cls}" d="M{x:.1f},{y - 8:.1f} L{x + 8:.1f},{y + 6:.1f} L{x - 8:.1f},{y + 6:.1f} Z">{tip}</path>'
    if lane == "ai_changed":
        return f'<rect class="{cls}" x="{x - 6.5:.1f}" y="{y - 6.5:.1f}" width="13" height="13" rx="2">{tip}</rect>'
    return f'<path class="{cls}" d="M{x:.1f},{y - 8:.1f} L{x + 8:.1f},{y:.1f} L{x:.1f},{y + 8:.1f} L{x - 8:.1f},{y:.1f} Z">{tip}</path>'


def _pill_text(it: dict, lang: str) -> str:
    if it["compromise"]:
        word = {True: t(lang, "still_present"), False: t(lang, "fixed"), None: t(lang, "unclear")}[it["still"]]
        return f'{GLYPH[it["status"]]} {t(lang, "compromise")}: {it["label"]} · {word}'
    return f'{GLYPH[it["status"]]} {it["label"]}'


def render_timeline(ledger: dict, lang: str, has_transcripts: bool) -> str:
    if not has_transcripts:
        return f'<p class="empty">{h(t(lang, "no_transcripts_timeline"))}</p>'
    items, overflow = build_items(ledger)
    if not items:
        return f'<p class="empty">{h(t(lang, "no_timeline_items"))}</p>'
    events = sorted((ts, lane, k, quote) for k, it in enumerate(items) for ts, lane, quote in it["events"])
    step = max(34.0, min(90.0, 640.0 / len(events)))
    x_today = X0 + len(events) * step + 40
    width = int(x_today + TODAY_W)
    per_lane = Counter(it["lane"] for it in items)
    lane_h = {lane: max(52, per_lane[lane] * (PILL_H + 6) + 16) for lane in LANES}
    lane_y, y = {}, TOP
    for lane in LANES:
        lane_y[lane] = y
        y += lane_h[lane]
    height = y + 16
    mid = {lane: lane_y[lane] + (lane_h[lane] - 4) / 2 for lane in LANES}
    out = [f'<div class="scroll-x"><svg class="diagram timeline" viewBox="0 0 {width} {height}" width="{width}" '
           f'height="{height}" role="img" aria-label="{h(t(lang, "sec_timeline"))}">']
    for lane in LANES:
        out.append(f'<rect class="tl-band" x="0" y="{lane_y[lane]}" width="{width}" height="{lane_h[lane] - 4}" rx="8"/>')
        out.append(f'<text class="tl-lane" x="12" y="{mid[lane] + 5:.1f}">{h(t(lang, "lane_" + lane))}</text>')
    out.append(f'<rect class="tl-today" x="{x_today - 14:.1f}" y="{TOP - 30}" width="{TODAY_W - 2}" '
               f'height="{height - TOP + 26}" rx="10"/>')
    out.append(f'<text class="tl-date today" x="{x_today:.1f}" y="{TOP - 12}">{h(t(lang, "today"))}</text>')
    positions: dict[int, list] = {}
    last_day = None
    for idx, (ts, lane, k, quote) in enumerate(events):
        x = X0 + idx * step + step / 2
        day = ts[5:10]
        if day and day != last_day:
            out.append(f'<text class="tl-date" x="{x:.1f}" y="{TOP - 12}" text-anchor="middle">{h(day)}</text>')
            last_day = day
        positions.setdefault(k, []).append((x, mid[lane], lane, quote))
    used, pill_y = Counter(), {}
    for k, it in enumerate(items):
        pill_y[k] = lane_y[it["lane"]] + 8 + used[it["lane"]] * (PILL_H + 6)
        used[it["lane"]] += 1
    for k, it in enumerate(items):
        pts = positions[k]
        for (x1, y1, _, _), (x2, y2, _, _) in zip(pts, pts[1:]):
            out.append(f'<path class="tl-link s-{it["status"]}" d="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}"/>')
        x, yv = pts[-1][0], pts[-1][1]
        py = pill_y[k] + PILL_H / 2
        out.append(f'<path class="arc s-{it["status"]}" d="M{x:.1f},{yv:.1f} C{x + 60:.1f},{yv:.1f} '
                   f'{x_today - 70:.1f},{py:.1f} {x_today - 8:.1f},{py:.1f}"/>')
    for k, it in enumerate(items):
        for x, yv, lane, quote in positions[k]:
            out.append(_marker(lane, x, yv, it["status"], quote))
        out.append(f'<g class="tl-pill s-{it["status"]}"><rect x="{x_today - 6:.1f}" y="{pill_y[k]}" '
                   f'width="{TODAY_W - 22}" height="{PILL_H}" rx="12"/>'
                   f'<text x="{x_today + 6:.1f}" y="{pill_y[k] + 16}">{ht(_pill_text(it, lang), 30)}</text></g>')
    out.append("</svg></div>")
    if overflow:
        out.append(f'<p class="note">{h(t(lang, "more_items", n=len(overflow)))}</p>')
    return "".join(out)
```

- [ ] **Step 4: Write `scripts/ledger_report/paths_svg.py`**

```python
"""Diagram E (developer view): what happens, step by step, after one action."""
from __future__ import annotations

from ledger_report.bits import h, ht
from ledger_report.i18n import t

BOX_W, BOX_H, GAP, ROW_GAP, PER_ROW = 200, 58, 40, 46, 4


def _ref(step: dict, evidence: dict) -> str:
    e = evidence.get(step.get("evidence"), {})
    if e.get("ok") and e.get("path"):
        return f"{e['path']}:{e.get('line', '')}"
    return ""


def render_paths(ledger: dict, lang: str) -> str:
    if not ledger["paths"]:
        return f'<p class="empty">{h(t(lang, "no_paths"))}</p>'
    ev = ledger["evidence"]
    out = []
    for path in ledger["paths"]:
        steps = path["steps"]
        rows = max(1, (len(steps) + PER_ROW - 1) // PER_ROW)
        width = 20 + PER_ROW * (BOX_W + GAP)
        height = 40 + rows * (BOX_H + ROW_GAP)
        svg = [f'<div class="diagram-wrap"><svg class="diagram paths" viewBox="0 0 {width} {height}" role="img" '
               f'aria-label="{ht(path["action"], 60)}"><defs><marker id="arrow-path" viewBox="0 0 8 8" refX="7" refY="4" '
               'markerWidth="8" markerHeight="8" orient="auto"><path class="arrowhead" d="M0,0 L8,4 L0,8 z"/></marker></defs>',
               f'<text class="path-title" x="10" y="22">{ht(path["action"], 60)}</text>']
        for i, st in enumerate(steps):
            r, c = divmod(i, PER_ROW)
            x, y = 10 + c * (BOX_W + GAP), 36 + r * (BOX_H + ROW_GAP)
            if i + 1 < len(steps):
                if c < PER_ROW - 1:
                    svg.append(f'<path class="flow" d="M{x + BOX_W},{y + BOX_H / 2} L{x + BOX_W + GAP - 4},{y + BOX_H / 2}" '
                               'marker-end="url(#arrow-path)"/>')
                else:
                    ny = y + BOX_H + ROW_GAP
                    svg.append(f'<path class="flow" d="M{x + BOX_W / 2},{y + BOX_H} L{x + BOX_W / 2},{y + BOX_H + ROW_GAP / 2} '
                               f'L{10 + BOX_W / 2},{y + BOX_H + ROW_GAP / 2} L{10 + BOX_W / 2},{ny - 4}" marker-end="url(#arrow-path)"/>')
            cls = "step" + (" warn" if st.get("warning") else "") + (" unverified" if st.get("unverified") else "")
            svg.append(f'<g class="{cls}"><rect x="{x}" y="{y}" width="{BOX_W}" height="{BOX_H}" rx="9"/>'
                       f'<text class="step-label" x="{x + 12}" y="{y + 24}">{ht(st["label"], 24)}</text>')
            ref = _ref(st, ev)
            if ref:
                svg.append(f'<text class="step-ref" x="{x + 12}" y="{y + 44}">{ht(ref, 30)}</text>')
            if st.get("unverified"):
                svg.append(f'<text class="step-unv" x="{x + BOX_W - 10}" y="{y + 16}" text-anchor="end">{h(t(lang, "unverified"))}</text>')
            if st.get("warning"):
                svg.append(f'<text class="step-warn" x="{x + 4}" y="{y + BOX_H + 16}">{ht("⚠ " + st["warning"], 30)}</text>')
            svg.append("</g>")
        svg.append("</svg></div>")
        out.append("".join(svg))
    return "".join(out)
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_render_timeline_paths.py tests/test_render_map_access.py tests/test_render_page.py`
Expected: PASS.

- [ ] **Step 6: Commit**

```bash
git add scripts/ledger_report/timeline_svg.py scripts/ledger_report/paths_svg.py tests/test_render_timeline_paths.py
git commit -m "feat: conversation timeline and call-path diagrams"
```

---
### Task 13: The CLI (`vl.py`) and screenshots (`shot.py`)

**Files:**
- Create: `scripts/vl.py`, `scripts/shot.py`
- Test: `tests/test_cli.py`

**Interfaces:**
- Consumes: `sessions.collect/default_claude_dir/default_codex_dir/Stats` (Tasks 2–3), `candidates.run` (Task 4), `probes.run_all` (Task 5), `ledger.merge/LedgerError` (Task 7), `verify.verify_ledger/summary_lines` (Task 9), `render.render_html/deliver` (Task 10), `common.*` (Task 1).
- Produces:
  - `vl.main(argv: list[str] | None = None) -> int` with subcommands:
    - `start --project DIR [--lang zh|en] [--claude-dir D] [--codex-dir D]`
    - `merge --project DIR [--parts-dir D]` (default `<run>/parts`, reads `part_*.json`)
    - `check --project DIR [--ledger FILE]`
    - `render --project DIR [--lang zh|en] [--out-dir D]`
    - `shot --project DIR`
    - `retention [--set DAYS] [--settings FILE]`
    - `--version`
  - Run folder files: `digest.jsonl`, `candidates.json`, `reading_pack_NN.md`, `probes.json`, `run.json`, then `ledger.json` (written by the agent), `ledger.verified.json`, `report.html`, `shots/*.png`. `latest_run.txt` in the project workdir holds the current run path.
  - `run.json` keys: `version, project_root, project_name, project_id, run_dir, created, lang, sessions (Stats.to_dict()), candidates (stats), probes ({ran, skipped, stack}), packs [file names], unattributed [paths], retention ({days, source, settings_path, earliest})`, plus `report_path` after render.
  - `vl.unattributed(root, recs) -> list[str]`, `vl.read_retention(path) -> (days, source)`, `vl.claude_settings_path() -> Path`.
  - `shot.find_chrome() -> str | None`, `shot.take_shots(report: Path, out_dir: Path, chrome: str, height: int = 6000) -> list[Path]` (desktop 1280 px, dark, and a true 390 px phone width via an iframe inside a 500 px window).

- [ ] **Step 1: Write the failing tests**

`tests/test_cli.py`:
```python
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

import pytest

import vl
from common import load_json
from helpers.fake_logs import ClaudeSession


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("VIBE_LEDGER_HOME", str(tmp_path / "home"))
    monkeypatch.setenv("VIBE_LEDGER_OUT_DIR", str(tmp_path / "out"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))  # never read the real ~/.codex in tests
    return tmp_path


def make_project(tmp_path, name="app"):
    app = tmp_path / name
    (app / "supabase" / "migrations").mkdir(parents=True)
    (app / "supabase" / "migrations" / "001.sql").write_text(
        "create table notes (id uuid);\n\nalter table notes disable row level security;\n", encoding="utf-8")
    (app / "package.json").write_text(json.dumps({"dependencies": {"@supabase/supabase-js": "2"}}), encoding="utf-8")
    s = ClaudeSession(app, "s1")
    uid = s.user("只有我自己能看到我的笔记")
    s.bash("npx supabase db push", "Error: new row violates row-level security policy", is_error=True)
    s.edit(app / "supabase/migrations/001.sql", "enable row level security", "disable row level security")
    s.save(tmp_path / "claude" / "projects")
    return app, uid


def next_commands(out):
    return [shlex.split(line.strip()) for line in out.splitlines() if line.strip().startswith("python3 ")]


def minimal_ledger(uid):
    return {"evidence": {
                "E1": {"kind": "transcript", "session": "s1", "msg_id": uid, "quote": "只有我自己能看到我的笔记"},
                "E2": {"kind": "code", "path": "supabase/migrations/001.sql", "line": 3,
                       "snippet": "alter table notes disable row level security;"}},
            "promises": [{"id": "P1", "type": "user_requirement", "question": "who_can_see",
                          "plain": "只有我自己能看到我的笔记", "source": ["E1"], "status": "broken",
                          "verdict_plain": "陌生人也能读", "verdict_dev": "RLS off", "evidence": ["E2"],
                          "fix_prompt": "Enable RLS on notes."}]}


def test_start_writes_the_run_folder(env, capsys):
    app, _ = make_project(env)
    assert vl.main(["start", "--project", str(app)]) == 0
    out = capsys.readouterr().out
    run = vl.latest_run(app)
    for name in ("digest.jsonl", "candidates.json", "reading_pack_01.md", "probes.json", "run.json"):
        assert (run / name).exists(), name
    manifest = load_json(run / "run.json")
    assert manifest["lang"] == "zh" and manifest["sessions"]["threads"] == 1
    assert manifest["retention"]["days"] == 30 and manifest["packs"] == ["reading_pack_01.md"]
    assert "supabase_rls" in manifest["probes"]["ran"]
    assert "NEXT" in out and "retention --set" in out
    assert not any(p.name.startswith(".vibe") for p in app.iterdir())  # nothing written into the project


def test_start_prints_runnable_next_commands_for_unusual_path(env, capsys):
    app, uid = make_project(env, name="我的 应用")
    assert vl.main(["start", "--project", str(app)]) == 0
    cmds = next_commands(capsys.readouterr().out)
    check = next(c for c in cmds if "check" in c)
    (vl.latest_run(app) / "ledger.json").write_text(json.dumps(minimal_ledger(uid), ensure_ascii=False), encoding="utf-8")
    res = subprocess.run([sys.executable] + check[1:], capture_output=True, text=True)
    assert res.returncode == 0, res.stdout + res.stderr
    assert (vl.latest_run(app) / "ledger.verified.json").exists()
    render_cmd = next(c for c in next_commands(res.stdout) if "render" in c)
    res2 = subprocess.run([sys.executable] + render_cmd[1:], capture_output=True, text=True)
    assert res2.returncode == 0, res2.stdout + res2.stderr
    report = re.search(r"Report: (.+)", res2.stdout).group(1).strip()
    assert report.endswith(".html") and Path(report).parent == env / "out"


def test_check_reports_format_problems_and_missing_ledger(env, capsys):
    app, uid = make_project(env)
    vl.main(["start", "--project", str(app)])
    capsys.readouterr()
    assert vl.main(["check", "--project", str(app)]) == 2
    assert "does not exist yet" in capsys.readouterr().out
    bad = minimal_ledger(uid)
    bad["promises"][0]["status"] = "maybe"
    (vl.latest_run(app) / "ledger.json").write_text(json.dumps(bad), encoding="utf-8")
    assert vl.main(["check", "--project", str(app)]) == 2
    assert "status must be one of" in capsys.readouterr().out
    (vl.latest_run(app) / "ledger.json").write_text("{not json", encoding="utf-8")
    assert vl.main(["check", "--project", str(app)]) == 2


def test_merge_reads_parts_dir(env, capsys):
    app, uid = make_project(env)
    vl.main(["start", "--project", str(app)])
    parts = vl.latest_run(app) / "parts"
    parts.mkdir()
    (parts / "part_01.json").write_text(json.dumps(minimal_ledger(uid), ensure_ascii=False), encoding="utf-8")
    assert vl.main(["merge", "--project", str(app)]) == 0
    merged = load_json(vl.latest_run(app) / "ledger.json")
    assert [p["id"] for p in merged["promises"]] == ["p1_P1"]
    assert "check" in capsys.readouterr().out


def test_render_requires_check_first(env, capsys):
    app, _ = make_project(env)
    vl.main(["start", "--project", str(app)])
    assert vl.main(["render", "--project", str(app)]) == 2


def test_commands_before_start_explain_what_to_do(env, capsys):
    app, _ = make_project(env)
    with pytest.raises(SystemExit) as exc:
        vl.main(["check", "--project", str(app)])
    assert "start" in str(exc.value)


def test_missing_project_folder(env):
    with pytest.raises(SystemExit) as exc:
        vl.main(["start", "--project", str(env / "nope")])
    assert "not found" in str(exc.value)


def test_start_without_git_and_without_logs(env, capsys):
    app = env / "bare"
    app.mkdir()
    (app / "index.html").write_text("<h1>hi</h1>", encoding="utf-8")
    assert vl.main(["start", "--project", str(app)]) == 0
    out = capsys.readouterr().out
    assert "No conversations were found" in out
    assert load_json(vl.latest_run(app) / "run.json")["unattributed"] == ["index.html"]


def test_retention_read_and_set(env, capsys):
    settings = env / "settings.json"
    assert vl.main(["retention", "--settings", str(settings)]) == 0
    assert "30 days" in capsys.readouterr().out
    settings.write_text(json.dumps({"theme": "dark"}), encoding="utf-8")
    assert vl.main(["retention", "--settings", str(settings), "--set", "365"]) == 0
    data = load_json(settings)
    assert data == {"theme": "dark", "cleanupPeriodDays": 365}
    assert (env / "settings.json.vibe-ledger.bak").exists()
    settings.write_text("{oops", encoding="utf-8")
    assert vl.main(["retention", "--settings", str(settings), "--set", "365"]) == 2
    assert settings.read_text() == "{oops"
    assert vl.main(["retention", "--settings", str(settings), "--set", "0"]) == 2


def test_two_starts_in_the_same_second_get_distinct_runs(env):
    app, _ = make_project(env)
    vl.main(["start", "--project", str(app)])
    first = vl.latest_run(app)
    vl.main(["start", "--project", str(app)])
    assert vl.latest_run(app) != first


def test_shot_without_chrome_says_so(env, capsys, monkeypatch):
    app, uid = make_project(env)
    vl.main(["start", "--project", str(app)])
    (vl.latest_run(app) / "ledger.json").write_text(json.dumps(minimal_ledger(uid), ensure_ascii=False), encoding="utf-8")
    vl.main(["check", "--project", str(app)])
    vl.main(["render", "--project", str(app)])
    import shot
    monkeypatch.setattr(shot, "find_chrome", lambda: None)
    capsys.readouterr()
    assert vl.main(["shot", "--project", str(app)]) == 1
    assert "not found" in capsys.readouterr().out


def test_version(capsys):
    with pytest.raises(SystemExit):
        vl.main(["--version"])
    assert "0.1.0" in capsys.readouterr().out
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_cli.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'vl'`.
- [ ] **Step 3: Write `scripts/shot.py`**

```python
"""Screenshot a rendered report in headless Chrome: desktop, dark mode and a
true 390 px phone width (macOS headless Chrome will not go narrower than
500 px, so the phone view is a 390 px iframe inside a 500 px window)."""
from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path

CANDIDATES = ("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium")
NAMES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome")


def find_chrome() -> str | None:
    env = os.environ.get("VIBE_LEDGER_CHROME")
    if env and Path(env).exists():
        return env
    for c in CANDIDATES:
        if Path(c).exists():
            return c
    for n in NAMES:
        found = shutil.which(n)
        if found:
            return found
    return None


def _shoot(chrome: str, url: str, out: Path, width: int, height: int) -> bool:
    try:
        subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        f"--window-size={width},{height}", f"--screenshot={out}", url],
                       capture_output=True, timeout=90)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return out.exists() and out.stat().st_size > 0


def take_shots(report: Path, out_dir: Path, chrome: str, height: int = 6000) -> list[Path]:
    report = Path(report).resolve()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    phone_page = out_dir / "phone.html"
    phone_page.write_text(
        '<!doctype html><meta charset="utf-8"><body style="margin:0">'
        f'<iframe src="{report.as_uri()}" style="width:390px;height:{height}px;border:0"></iframe>',
        encoding="utf-8")
    jobs = [(report.as_uri(), out_dir / "desktop.png", 1280),
            (report.as_uri() + "?theme=dark", out_dir / "desktop-dark.png", 1280),
            (phone_page.as_uri(), out_dir / "phone-390.png", 500)]
    return [out for url, out, width in jobs if _shoot(chrome, url, out, width, height)]
```

- [ ] **Step 4: Write `scripts/vl.py`**

```python
#!/usr/bin/env python3
"""vibe-ledger command line.

start -> (the agent writes ledger.json) -> check -> render -> shot.
Every step prints the exact next command; run it as printed."""
from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
from datetime import datetime, timezone
from pathlib import Path

SELF = Path(__file__).resolve()
sys.path.insert(0, str(SELF.parent))

import candidates  # noqa: E402
import probes  # noqa: E402
import render  # noqa: E402
import sessions  # noqa: E402
import shot  # noqa: E402
import verify  # noqa: E402
from common import (SOURCE_EXTS, __version__, detect_lang, git_ls_files, is_within, iter_files,  # noqa: E402
                    load_json, project_id, project_workdir, read_jsonl, rel, write_json, write_jsonl)
from ledger import LedgerError, merge  # noqa: E402

GUIDE = SELF.parent.parent / "references" / "extraction-guide.md"


def cmd(*args) -> str:
    return " ".join(shlex.quote(str(a)) for a in ("python3", SELF, *args))


def _root(args) -> Path:
    root = Path(args.project).expanduser().resolve()
    if not root.is_dir():
        raise SystemExit(f"error: project folder not found: {root}")
    return root


def latest_run(root: Path) -> Path:
    marker = project_workdir(root) / "latest_run.txt"
    if not marker.exists():
        raise SystemExit(f"error: no run yet for {root}. Run start first:\n  {cmd('start', '--project', root)}")
    return Path(marker.read_text(encoding="utf-8").strip())


def claude_settings_path() -> Path:
    return Path(os.environ.get("CLAUDE_CONFIG_DIR") or Path.home() / ".claude") / "settings.json"


def read_retention(path: Path) -> tuple[int, str]:
    if not path.exists():
        return 30, "default"
    try:
        value = json.loads(path.read_text(encoding="utf-8")).get("cleanupPeriodDays")
    except (json.JSONDecodeError, AttributeError):
        return 30, "unreadable settings file, assuming the default"
    return (value, "settings") if isinstance(value, int) else (30, "default")


def unattributed(root: Path, recs: list[dict]) -> list[str]:
    touched = {rel(f, root) for r in recs for f in r["files"] if is_within(f, root)}
    files = git_ls_files(root)
    if files is None:
        files = [rel(p, root) for p in iter_files(root, SOURCE_EXTS)]
    return sorted(f for f in files if Path(f).suffix.lower() in SOURCE_EXTS and f not in touched)


def do_start(args) -> int:
    root = _root(args)
    work = project_workdir(root)
    base = datetime.now().strftime("%Y%m%d-%H%M%S")
    run, n = work / "runs" / base, 1
    while run.exists():
        run, n = work / "runs" / f"{base}-{n}", n + 1
    run.mkdir(parents=True)
    (work / "latest_run.txt").write_text(str(run), encoding="utf-8")

    claude_dir = Path(args.claude_dir).expanduser() if args.claude_dir else sessions.default_claude_dir()
    codex_dir = Path(args.codex_dir).expanduser() if args.codex_dir else sessions.default_codex_dir()
    recs, stats = sessions.collect(root, claude_dir, codex_dir, archive_dir=work / "digests")
    write_jsonl(run / "digest.jsonl", recs)
    cands = candidates.run(root, recs)
    packs = []
    for k, text in enumerate(cands.pop("packs_text"), 1):
        name = f"reading_pack_{k:02d}.md"
        (run / name).write_text(text, encoding="utf-8")
        packs.append(name)
    write_json(run / "candidates.json", cands)
    pr = probes.run_all(root)
    write_json(run / "probes.json", pr)
    days, source = read_retention(claude_settings_path())
    claude_ts = [r["ts"] for r in recs if r["agent"] == "claude-code" and r["ts"]]
    manifest = {
        "version": __version__, "project_root": str(root), "project_name": root.name, "project_id": project_id(root),
        "run_dir": str(run), "created": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "lang": args.lang or detect_lang(r["text"] for r in recs if r["role"] == "user"),
        "sessions": stats.to_dict(), "candidates": cands["stats"],
        "probes": {"ran": pr["ran"], "skipped": pr["skipped"], "stack": pr["stack"]},
        "packs": packs, "unattributed": unattributed(root, recs),
        "retention": {"days": days, "source": source, "settings_path": str(claude_settings_path()),
                      "earliest": min(claude_ts) if claude_ts else ""},
    }
    write_json(run / "run.json", manifest)
    _print_start(manifest, run, root)
    return 0


def _print_start(m: dict, run: Path, root: Path) -> None:
    s, c, p = m["sessions"], m["candidates"], m["probes"]
    print(f"vibe-ledger {__version__} — run folder: {run}")
    if s["threads"]:
        print(f"Conversations: {s['threads']} ({', '.join(f'{k} {v}' for k, v in s['by_agent'].items())}), "
              f"{s['earliest'][:10]} → {s['latest'][:10]}; {s['archived_threads']} restored from the archive")
    else:
        print("No conversations were found for this project. Promises need a conversation source, so leave "
              "`promises` empty and record only map, access and paths from the code.")
    print(f"Candidates: {c['compromises']} error→change, {c['deferrals']} put off, {c['claims']} AI claims, "
          f"{c['todos']} code TODOs")
    print(f"Probes ran: {', '.join(p['ran']) or 'none'}; skipped: {', '.join(x['probe'] for x in p['skipped']) or 'none'}")
    if p["stack"]["unsupported"]:
        print(f"Not covered by probes: {', '.join(p['stack']['unsupported'])}")
    print(f"Reading packs: {len(m['packs'])} ({', '.join(f'{n} {k:,} chars' for n, k in zip(m['packs'], c['pack_chars']))})")
    print(f"Report language: {m['lang']}")
    r = m["retention"]
    print(f"Claude Code keeps transcripts for {r['days']} days ({r['source']}).")
    for w in s["warnings"]:
        print(f"WARNING: {w}")
    if r["days"] < 365 and s["by_agent"].get("claude-code"):
        print("NEXT (only after the user agrees — it edits their Claude Code settings):")
        print("  " + cmd("retention", "--set", 365))
    if len(m["packs"]) == 1:
        print(f"NEXT: read {run / m['packs'][0]}, {run / 'probes.json'} and the project code; write "
              f"{run / 'ledger.json'} as {GUIDE} describes; then run:")
    else:
        print(f"NEXT: give each reading pack in {run} to its own subagent (or do them one by one). Each writes "
              f"{run / 'parts'}/part_NN.json with evidence, promises and compromises only ({GUIDE}); then run:")
        print("  " + cmd("merge", "--project", root))
        print(f"and add map, access and paths to {run / 'ledger.json'}; then run:")
    print("  " + cmd("check", "--project", root))


def do_merge(args) -> int:
    root = _root(args)
    run = latest_run(root)
    parts_dir = Path(args.parts_dir) if args.parts_dir else run / "parts"
    files = sorted(parts_dir.glob("part_*.json"))
    if not files:
        print(f"error: no part_*.json files in {parts_dir}")
        return 2
    try:
        led = merge([load_json(f) for f in files])
    except json.JSONDecodeError as exc:
        print(f"error: a part is not valid JSON: {exc}")
        return 2
    except LedgerError as exc:
        print("The parts do not match the ledger format:")
        for problem in exc.problems:
            print("  -", problem)
        return 2
    write_json(run / "ledger.json", led)
    print(f"Merged {len(files)} parts: {len(led['promises'])} promises, {len(led['compromises'])} compromises → {run / 'ledger.json'}")
    print(f"NEXT: add map, access and paths from the code ({GUIDE}), then run:")
    print("  " + cmd("check", "--project", root))
    return 0


def do_check(args) -> int:
    root = _root(args)
    run = latest_run(root)
    path = Path(args.ledger) if args.ledger else run / "ledger.json"
    if not path.exists():
        print(f"error: {path} does not exist yet; write the ledger first ({GUIDE})")
        return 2
    try:
        led = load_json(path)
    except json.JSONDecodeError as exc:
        print(f"error: {path} is not valid JSON: {exc}")
        return 2
    index = {obj["id"]: obj for _, obj in read_jsonl(run / "digest.jsonl") if obj}
    try:
        out = verify.verify_ledger(led, index, root, load_json(run / "probes.json"))
    except LedgerError as exc:
        print("The ledger does not match the format (references/ledger-schema.md):")
        for problem in exc.problems:
            print("  -", problem)
        print("NEXT: fix these, then run:\n  " + cmd("check", "--project", root))
        return 2
    write_json(run / "ledger.verified.json", out)
    for line in verify.summary_lines(out):
        print(line)
    print("NEXT: if a quote or snippet failed only because it was mis-copied, fix it from the real text and run "
          "check again. Otherwise run:")
    print("  " + cmd("render", "--project", root))
    return 0


def do_render(args) -> int:
    root = _root(args)
    run = latest_run(root)
    verified = run / "ledger.verified.json"
    if not verified.exists():
        print("error: run check first:\n  " + cmd("check", "--project", root))
        return 2
    manifest = load_json(run / "run.json")
    html = render.render_html(load_json(verified), manifest, load_json(run / "probes.json"), args.lang or manifest["lang"])
    out = render.deliver(html, run, manifest["project_name"], args.out_dir)
    manifest["report_path"] = str(out)
    write_json(run / "run.json", manifest)
    print(f"Report: {out}")
    print("NEXT: take screenshots and look at every diagram before telling the user it is done:")
    print("  " + cmd("shot", "--project", root))
    return 0


def do_shot(args) -> int:
    root = _root(args)
    run = latest_run(root)
    report = load_json(run / "run.json").get("report_path")
    if not report or not Path(report).exists():
        print("error: render first:\n  " + cmd("render", "--project", root))
        return 2
    chrome = shot.find_chrome()
    if not chrome:
        print(f"Chrome or Chromium was not found, so no screenshots were taken. Open the report and look: {report}")
        return 1
    paths = shot.take_shots(Path(report), run / "shots", chrome)
    for p in paths:
        print(f"Screenshot: {p}")
    if not paths:
        print(f"Chrome did not produce screenshots. Open the report and look: {report}")
        return 1
    print("NEXT: open every screenshot and check that each diagram is readable, nothing overlaps or is cut off, "
          "the counts match the ledger, and the phone view has no text running off the edge. Fix and re-render if not.")
    return 0


def do_retention(args) -> int:
    path = Path(args.settings).expanduser() if args.settings else claude_settings_path()
    days, source = read_retention(path)
    if args.set is None:
        print(f"Claude Code keeps transcripts for {days} days ({source}; {path}).")
        return 0
    if args.set < 1:
        print("error: --set needs a number of days of at least 1")
        return 2
    data, backup = {}, None
    if path.exists():
        text = path.read_text(encoding="utf-8")
        try:
            data = json.loads(text)
        except json.JSONDecodeError:
            print(f"error: {path} is not valid JSON; leaving it untouched")
            return 2
        backup = path.with_name(path.name + ".vibe-ledger.bak")
        backup.write_text(text, encoding="utf-8")
    data["cleanupPeriodDays"] = args.set
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Set cleanupPeriodDays to {args.set} in {path}" + (f" (backup: {backup})" if backup else ""))
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="vl.py", description=__doc__)
    ap.add_argument("--version", action="version", version=f"vibe-ledger {__version__}")
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("start", help="find the conversations, write reading packs, run probes")
    p.add_argument("--project", required=True)
    p.add_argument("--lang", choices=("zh", "en"))
    p.add_argument("--claude-dir")
    p.add_argument("--codex-dir")
    p = sub.add_parser("merge", help="merge chunk ledgers into ledger.json")
    p.add_argument("--project", required=True)
    p.add_argument("--parts-dir")
    p = sub.add_parser("check", help="verify ledger.json")
    p.add_argument("--project", required=True)
    p.add_argument("--ledger")
    p = sub.add_parser("render", help="write the HTML report")
    p.add_argument("--project", required=True)
    p.add_argument("--lang", choices=("zh", "en"))
    p.add_argument("--out-dir")
    p = sub.add_parser("shot", help="screenshot the report")
    p.add_argument("--project", required=True)
    p = sub.add_parser("retention", help="show or change how long Claude Code keeps transcripts")
    p.add_argument("--set", type=int)
    p.add_argument("--settings")
    args = ap.parse_args(argv)
    return {"start": do_start, "merge": do_merge, "check": do_check, "render": do_render,
            "shot": do_shot, "retention": do_retention}[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_cli.py`
Expected: PASS.

- [ ] **Step 6: Run the whole suite**

Run: `python3 -m pytest`
Expected: PASS (every test file so far).

- [ ] **Step 7: Commit**

```bash
git add scripts/vl.py scripts/shot.py tests/test_cli.py
git commit -m "feat: vl.py CLI with runnable next steps, retention control and screenshots"
```

---
### Task 14: `SKILL.md` and `references/`

**Files:**
- Create: `SKILL.md`
- Create: `references/extraction-guide.md`, `references/ledger-schema.md`, `references/five-questions.md`, `references/probes.md`, `references/candidates.md`
- Test: `tests/test_docs.py`

**Interfaces:**
- Consumes: the CLI subcommands (Task 13), ledger constants (Task 7), probe names (Tasks 5–6), candidate rules (Task 4).
- Produces: the agent-facing workflow. `tests/test_docs.py` pins the docs to the code: every `vl.py <subcommand>` named in `SKILL.md` exists; every `references/*.md` named exists; the references mention every status, question, promise type, subject and probe name the code uses.

- [ ] **Step 1: Write the failing test**

`tests/test_docs.py`:
```python
import re
from pathlib import Path

import ledger
import probes
import vl

REPO = Path(__file__).resolve().parents[1]
SKILL = (REPO / "SKILL.md").read_text(encoding="utf-8")
REFS = {p.name: p.read_text(encoding="utf-8") for p in (REPO / "references").glob("*.md")}


def test_frontmatter():
    m = re.match(r"^---\nname: vibe-ledger\ndescription: (.+?)\n---\n", SKILL, re.S)
    assert m and len(m.group(1)) < 1024


def test_every_subcommand_named_in_skill_exists():
    parser_cmds = {"start", "merge", "check", "render", "shot", "retention"}
    named = set(re.findall(r"vl\.py (\w+)", SKILL))
    assert named and named <= parser_cmds
    assert {"start", "check", "render", "shot"} <= named


def test_every_reference_named_exists():
    named = set(re.findall(r"references/([\w-]+\.md)", SKILL + "".join(REFS.values())))
    assert named and named <= set(REFS)


def test_references_cover_the_code_vocabulary():
    text = "".join(REFS.values())
    vocab = (list(ledger.STATUSES) + list(ledger.QUESTIONS) + list(ledger.TYPES) + list(ledger.SUBJECTS)
             + list(ledger.LANES) + list(ledger.NODE_KINDS) + [m.NAME for m in probes._modules()])
    missing = [w for w in vocab if f"`{w}`" not in text]
    assert not missing, missing


def test_skill_stays_short():
    assert len(SKILL.splitlines()) < 120


def test_worked_example_in_the_guide_is_a_valid_ledger():
    import json
    block = re.search(r"`{3}json\n(.+?)\n`{3}", REFS["extraction-guide.md"], re.S).group(1)
    ledger.validate(json.loads(block))
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest tests/test_docs.py`
Expected: FAIL — `FileNotFoundError` for `SKILL.md`.

- [ ] **Step 3: Write `SKILL.md`**

````markdown
---
name: vibe-ledger
description: Explain an AI-built ("vibe-coded") app to the person who made it and check it at the same time. Reads the Claude Code and Codex conversations that built the project plus the current code, turns what the user asked for, what the AI claimed it did and what it put off "for later" into a ledger of promises, checks each one against verified code evidence, and renders an offline HTML report with diagrams (app map, who-can-see matrix, conversation timeline, call paths). Use when someone wants to understand or sanity-check an app an AI wrote for them — "explain my app", "what did the AI actually build", "is my vibe-coded app safe", "where is my data stored", "who can see my data", "what in my app costs money", "帮我看懂这个 AI 写的项目", "我的数据存在哪", "谁能看到我的数据", "检查一下 AI 写的代码有没有问题". Runs locally and sends nothing anywhere.
---

# vibe-ledger

Turns *what was asked, claimed and put off* into a ledger of promises, checks every promise against the code, and draws the result. **Every conclusion carries evidence a script verifies. Anything that fails verification shows as ❓ — it is never drawn as fact.**

## Rules

1. **Never invent evidence.** Copy quotes character for character from a reading pack, and code snippets from the file. `check` rejects anything else, and the report shows the rejection.
2. **Only the five questions** (references/five-questions.md): where data lives, what costs money, who can see it, where it is most likely to break, what was put off. Leave cosmetic and feature requests out.
3. **A status other than `unknown` needs code or probe evidence.** When unsure, write `unknown`.
4. **Two voices.** `verdict_plain` is one sentence for someone who cannot read code (an analogy only if it is accurate). `verdict_dev` names the file and the mechanism. Write both in the run's language (`lang` in `run.json`).
5. **Ask before `retention --set`.** It edits the user's Claude Code settings.
6. **Transcripts are private.** Quote only what a promise needs. The digest is already masked; never unmask or repeat a secret.

## Steps

Run everything as `python3 <this skill's folder>/scripts/vl.py …`. Each step prints the exact next command — run it as printed.

1. **Start** — `vl.py start --project <app folder>`. It finds the conversations, writes reading packs, runs the probes and archives a masked digest. Read its summary aloud to yourself: conversation count, candidates, probes, warnings. If it prints a retention line, ask the user (rule 5).
2. **Extract** — follow references/extraction-guide.md.
   - One reading pack: read it, `probes.json`, `candidates.json` and the code it points at; write `<run>/ledger.json`.
   - Several packs: give each pack to its own subagent (or work through them one by one) → `<run>/parts/part_NN.json` with evidence, promises and compromises only; then `vl.py merge --project <app folder>`; then add `map`, `access` and `paths` to `<run>/ledger.json` yourself.
3. **Check** — `vl.py check --project <app folder>`. Fix a failed quote or snippet only by copying the real text. Downgrades to ❓ are the honest result, not something to work around.
4. **Render** — `vl.py render --project <app folder>`.
5. **Look** — `vl.py shot --project <app folder>`, then open all three screenshots. Every diagram must be readable and say what the ledger says; nothing may overlap or run off the edge at phone width. Fix and re-render if not. If no browser is available, open the HTML and read it.
6. **Tell the user** — the report path; the counts (✅ ❌ ⚠️ ⏳ ❓); the three most important problems in plain words, each with the fix it suggests; and what the report could not see (its last section).

## When there are no conversations

`start` says so. Leave `promises` empty, still record `map`, `access` and `paths` from the code, and tell the user the report checked the code only.

## Reference

- references/extraction-guide.md — how to write the ledger, with a worked example
- references/ledger-schema.md — every field
- references/five-questions.md — what belongs under each question
- references/probes.md — what each probe checks and where it is blind
- references/candidates.md — how candidates are found
````

- [ ] **Step 4: Write `references/five-questions.md`**

```markdown
# The five questions

Every promise sits under exactly one question. If a promise fits none of them, it does not belong in the ledger.

| Key | Question | Belongs here | Does not belong here |
|---|---|---|---|
| `where_data` | Where does the data live? | "save notes in Supabase", "keep photos in S3", "don't store card numbers" | "use a blue theme" |
| `what_costs` | What costs money? | "don't let strangers run up my OpenAI bill", "only call the AI when I press the button", "stay on the free tier" | "make it fast" |
| `who_can_see` | Who can see it? | "only I can see my notes", "teammates can read but not edit", "the admin page is password-protected" | "add a dark mode" |
| `what_breaks` | Where is it most likely to break? | "it must not crash when the list is empty", promises about backups, error handling around payments | general code style |
| `open_debts` | What was put off "for later"? | "for now the key is in the frontend", "test mode until launch", "hardcode the admin password for now" | ideas never agreed on |

Put a `deferred` promise under `open_debts` unless it is clearly about another question (a key "for now in the frontend" is `open_debts`; its consequence for `what_costs` goes in the verdict).

Subjects in the access matrix:

- `anonymous` — anyone on the internet who is not signed in;
- `signed_in` — another signed-in user who does not own the data;
- `owner` — the person the data belongs to.
```

- [ ] **Step 5: Write `references/ledger-schema.md`**

````markdown
# Ledger fields

`ledger.json` is one JSON object. `evidence` and `promises` are required; `compromises`, `map`, `access` and `paths` may be left out. `vl.py check` lists every format problem at once.

## evidence — `{id: item}`

| kind | fields |
|---|---|
| `transcript` | `session`, `msg_id` (the `[ID]` from a reading pack), `quote` (≥ 4 characters, copied exactly) |
| `code` | `path` (relative to the project), `line` (integer), `snippet` (1–3 lines copied exactly) |
| `probe` | `finding_id` (an `id` from `probes.json`) |

`check` adds `ok` and, when it fails, `reason`. Timestamps always come from the logs.

## promises — list

| field | values |
|---|---|
| `id` | unique, e.g. `P1` |
| `type` | `user_requirement` (the user asked), `ai_claim` (the AI said it did it), `deferred` (put off for later) |
| `question` | `where_data`, `what_costs`, `who_can_see`, `what_breaks`, `open_debts` |
| `plain` | the promise in a short sentence, in the run's language |
| `source` | transcript evidence ids — where it was said |
| `status` | `kept`, `broken`, `partial`, `pending` (only for `deferred`: still not done), `unknown` |
| `verdict_plain` / `verdict_dev` | see SKILL.md rule 4 |
| `evidence` | code/probe evidence ids that support the status |
| `fix_prompt` | optional; an instruction the user can paste to their AI (file, change, how to confirm). Never include a secret. |

## compromises — list

`id`, `error` (transcript id of the error), `change` (transcript ids of the change), `bypassed` (a few words: "RLS", "CORS check"), `still_present` (`true`/`false`), `now` (code/probe ids showing the current state), `breaks` (promise id or `null`).

## map

`nodes`: `id`, `lane` (`browser`, `server`, `storage`), `kind` (`page`, `route`, `function`, `database`, `storage`, `third_party`, `client`), `label`, `holds` (data names), `paid` (true when it charges per use), `evidence`.
`edges`: `from`, `to`, `carries` (what data), `risk` (short text or `null`), `evidence`.

## access

`resources`: `name` (table, collection, bucket — or `*` for all data), `required_by` (promise id or `null`), `cells` keyed by `anonymous`, `signed_in`, `owner`, each `{read, write, evidence}` with values `allow`, `deny`, `unknown`.

## paths

Each: `action` (what the user does, e.g. "press Save"), `steps`: `[{label, evidence (one id), warning (text or null)}]`.
````
- [ ] **Step 6: Write `references/extraction-guide.md`**

````markdown
# Writing the ledger

You turn a reading pack, `probes.json`, `candidates.json` and the project code into `<run>/ledger.json`. The scripts check everything you write; the report shows what passed.

## 1. Read in this order

1. `probes.json` — deterministic findings. Each has an `id`, `level` (`certain`, `hint`, `fact`), `path`, `line`, `message`. `fact` findings from `routes` list the pages and endpoints.
2. The reading pack — every user message, plus candidates: **K** (an error followed by a change), **D** (something put off), **A** (the AI saying it did something). Candidates are hints; judge each one.
3. The code the pack and probes point at. Open the files; do not guess what they contain.

## 2. Promises

Write one promise for each thing that matters to one of the five questions (references/five-questions.md):

- `user_requirement` — the user asked for it ("只有我自己能看到我的笔记").
- `ai_claim` — the AI said it was done ("接口已经加了登录保护"). Claims are worth checking because they are often only partly true.
- `deferred` — someone said it would be done later ("for now the key is in the frontend").

Pick the status from the code, not from the conversation:

| The code shows… | status |
|---|---|
| the promise holds | `kept` |
| the opposite | `broken` |
| some of it (one route protected, another not) | `partial` |
| a `deferred` item that was never done | `pending` |
| you cannot tell from the code | `unknown` |

Every status except `unknown` needs at least one `code` or `probe` evidence that shows it. A transcript quote proves something was *said*, never that it is *true*.

## 3. Evidence

- Transcript: `msg_id` is the `[ID]` in the pack header line; `quote` is copied exactly from the text under it (one sentence is enough; at least 4 characters). Never quote across a "not shown" marker.
- Code: `path` relative to the project, the `line` where the snippet starts, and a `snippet` of 1–3 lines copied from the file. Prefer the line that *decides* the behaviour (the `disable row level security`, the missing check, the `NEXT_PUBLIC_` variable).
- Probe: `finding_id` from `probes.json`. Use it when a probe already found the thing — it is the strongest evidence.

## 4. Compromises (from K candidates)

A compromise is a change made to get past an error that **weakened a protection**: switching off row level security, setting CORS to `*`, silencing type checks, skipping verification, using the service key in the browser, swallowing an error, replacing real data with mock data. A correct fix (adding the missing policy, fixing the query) is not a compromise — skip it.

For each real compromise: `error` = the error's transcript evidence; `change` = the change's transcript evidence (quote from the edit record); `bypassed` = a few words; `still_present` = whether the weakening is in the code **now** (check the file; `now` lists the code/probe evidence); `breaks` = the promise it breaks, if any.

## 5. Map (diagram A)

Nodes go in three lanes: `browser` (pages, client code), `server` (routes, server functions), `storage` (databases, file storage and outside services). Kinds: `page`, `route`, `function`, `database`, `storage`, `third_party`, `client`. Set `paid: true` for services that charge per use (AI APIs, SMS, email, payments). Edges say what data moves (`carries`) and, when it is risky, why (`risk`, a few words). Every node and edge needs code or probe evidence — the route probe's `fact` findings are good evidence for route nodes. Keep it to the parts that matter: at most 12 nodes are drawn.

## 6. Access (diagram B)

One resource per table, collection or bucket that holds user data. For each of `anonymous`, `signed_in`, `owner`, write what the code allows for `read` and `write` (`allow`, `deny`, `unknown`) with evidence. Link `required_by` to the promise that asked for privacy. Probe findings are merged in automatically: when a probe says "anyone can read", it fills unknown cells and flags cells that disagree — do not copy probe conclusions you cannot see in the code.

## 7. Paths (diagram E, developer view)

One to four key actions (save data, call the AI, pay, sign in). Each step is a function or request with one code evidence; put a short `warning` on the step where the problem is (e.g. "no login check").

## 8. Writing style

- `plain`: the promise as the user would say it, short.
- `verdict_plain`: one sentence a non-programmer understands. An analogy only if it is accurate ("the front door is locked but the back window is open" fits RLS off with a login page; it does not fit a slow page).
- `verdict_dev`: file, line and mechanism.
- `fix_prompt` (for `broken`, `partial`, `pending`): what to change, where, and how to confirm it — written so the user can paste it to their AI. No secrets.
- Write in the run's language (`lang` in `run.json`).

## 9. Several reading packs

Each subagent writes `<run>/parts/part_NN.json` holding `evidence`, `promises` and `compromises` for its pack (ids only need to be unique inside the part). `vl.py merge` renames ids, drops duplicates and flags promises two parts judged differently. You then add `map`, `access` and `paths` to the merged `ledger.json`, referring to the merged promise ids (`p1_P3` …).

## 10. A worked example

The pack shows `[s1-u1] USER … 只有我自己能看到我的笔记`, candidate K1 with `[s1-u3] TOOL-OUTPUT … new row violates row-level security policy` and `[s1-u4] AI … EDIT supabase/migrations/001.sql … disable row level security`; `probes.json` has `supabase_rls:supabase/migrations/001.sql:3`.

```json
{
  "evidence": {
    "E1": {"kind": "transcript", "session": "s1", "msg_id": "s1-u1", "quote": "只有我自己能看到我的笔记"},
    "E2": {"kind": "probe", "finding_id": "supabase_rls:supabase/migrations/001.sql:3"},
    "E3": {"kind": "transcript", "session": "s1", "msg_id": "s1-u3", "quote": "new row violates row-level security policy"},
    "E4": {"kind": "transcript", "session": "s1", "msg_id": "s1-u4", "quote": "disable row level security"},
    "E5": {"kind": "code", "path": "lib/supabase.ts", "line": 3, "snippet": "export const supabase = createClient("}
  },
  "promises": [{
    "id": "P1", "type": "user_requirement", "question": "who_can_see", "plain": "只有我自己能看到我的笔记",
    "source": ["E1"], "status": "broken",
    "verdict_plain": "笔记表的访问规则被关掉了：任何人拿到网页里公开的密钥，就能读到所有人的笔记。",
    "verdict_dev": "supabase/migrations/001.sql:3 disables RLS on notes; no policy limits rows to auth.uid().",
    "evidence": ["E2"],
    "fix_prompt": "In supabase/migrations, re-enable row level security on notes and add select/insert policies using (auth.uid() = user_id). Then sign in as a second user and confirm you cannot see the first user's notes."
  }],
  "compromises": [{"id": "C1", "error": "E3", "change": ["E4"], "bypassed": "RLS",
                   "still_present": true, "now": ["E2"], "breaks": "P1"}],
  "map": {"nodes": [
            {"id": "web", "lane": "browser", "kind": "page", "label": "笔记页", "holds": [], "paid": false, "evidence": ["E5"]},
            {"id": "db", "lane": "storage", "kind": "database", "label": "Supabase", "holds": ["notes"], "paid": false, "evidence": ["E2"]}],
          "edges": [{"from": "web", "to": "db", "carries": "笔记", "risk": "陌生人也能读", "evidence": ["E2"]}]},
  "access": {"resources": [{"name": "notes", "required_by": "P1", "cells": {
            "owner": {"read": "allow", "write": "allow", "evidence": ["E5"]}}}]},
  "paths": []
}
```

The anonymous and signed-in cells are left out on purpose: the probe fills them.
````

- [ ] **Step 7: Write `references/probes.md`**

```markdown
# Probes

Deterministic checks that run during `start`. Each finding has a `level`: `certain` (the code says so), `hint` (likely, confirm in the code) or `fact` (a neutral observation). A probe that does not apply to the project is skipped and listed in the report; a probe that crashes is listed too.

| Probe | Runs for | Checks | Blind spots |
|---|---|---|---|
| `secrets_exposed` | every project | env vars starting with `NEXT_PUBLIC_`, `VITE_`, `EXPO_PUBLIC_`, `REACT_APP_` that hold a real secret or are named SECRET/SERVICE_ROLE/PRIVATE/PASSWORD; OpenAI/Anthropic/Stripe/AWS/GitHub/Slack keys and service-role JWTs written in code; `.env` files tracked by git | keys set in a hosting dashboard; secrets in formats it does not know. Supabase anon keys and Stripe publishable keys are public by design and not reported. |
| `supabase_rls` | Supabase projects | tables created without enabling row level security, RLS switched off, policies with `using (true)`, tables used in code but missing from migrations, the service-role key in browser code | anything changed in the Supabase dashboard rather than in migrations: a table created without RLS here may have it switched on there (so that finding fills no access cells) |
| `firebase_rules` | Firebase projects | rules that allow everything (`if true`), test-mode rules (`request.time < timestamp.date(...)`), Realtime Database rules set to `true` | rules deployed from the console and not in the repo |
| `cors_wildcard` | every project | `origin: '*'`, `Access-Control-Allow-Origin: *`, `cors()` with no options; notes when credentials are allowed too | CORS set on a proxy or hosting platform |
| `paid_api_unauthed` | Next.js, Express | server endpoints that import a paid SDK (OpenAI, Anthropic, Replicate, Stripe, Twilio, Resend, Google AI, Groq, Cohere, ElevenLabs) directly or through one local import, with no login check in the file | login enforced by middleware in another file (a false alarm — hence `hint`); rate limits are not checked |
| `routes` | Next.js, Express | pages (`PAGE /x`), API routes (`API /api/x`, `POST /api/x`) and Express routes | routes built dynamically |

Stacks with no probes (Flask, Django, FastAPI, Rails, Go, PHP, …) are named in the report as "not covered"; their promises can still be checked by reading the code.
```

- [ ] **Step 8: Write `references/candidates.md`**

```markdown
# How candidates are found

`start` marks places in the conversations worth reading closely. They are hints from simple rules; the ledger only records what you confirm.

## K — an error, then a change

- **Error**: a tool call that failed; command output with an error line (`Error:`, `permission denied`, `violates row-level security`, 401/403/500, CORS blocked, compile failure, a traceback); or a user saying it is broken ("报错了", "还是不行", "still not working", "blocked by CORS").
- **Window**: from the error to 20 digest records later or the end of the next user turn, whichever is earlier. Overlapping windows merge.
- **Change**: any edit, or a command that writes files or runs SQL / database tools.
- **Bypass hints** (raise priority only): `rls_disabled`, `policy_allows_all`, `cors_wildcard`, `type_check_silenced`, `verify_skipped`, `service_role_used`, `empty_catch`, `mock_data`, `commented_out`, `removed_guard` (an auth/policy/verify/check/validate/permission/require word disappeared).

## D — put off for later

User or AI text containing phrases such as for now, temporarily, placeholder, mock, hardcode, stub, in production you should, quick fix, workaround, before launch, 暂时, 先这样, 之后再, 后续再, 以后再, 临时, 写死, 模拟数据, 先跑起来, 先不管, 上线前. Code comments with TODO, FIXME, HACK, XXX, for now, temporary, mock, placeholder, hardcoded, 暂时, 临时, 写死 are listed at the end of the first pack.

## A — the AI says it did something

The last AI message of each turn when it contains phrases such as "I've added", "now protected", "is now", "已经", "已实现", "已添加", "已修复", "✅".
```

- [ ] **Step 9: Run the test to verify it passes**

Run: `python3 -m pytest tests/test_docs.py`
Expected: PASS.

- [ ] **Step 10: Commit**

```bash
git add SKILL.md references/extraction-guide.md references/ledger-schema.md references/five-questions.md references/probes.md references/candidates.md tests/test_docs.py
git commit -m "docs: SKILL.md workflow and references for writing the ledger"
```

---
### Task 15: Fixture apps, conversation scenarios, scorer, deterministic end-to-end tests

**Files:**
- Create: `tests/fixtures/apps/notes-supabase/{package.json,.env.local,supabase/migrations/001_notes.sql,lib/supabase.ts,app/page.tsx,app/api/summarize/route.ts}`
- Create: `tests/fixtures/apps/habits-firebase/{package.json,firebase.json,firestore.rules,src/firebase.ts,src/App.tsx}`
- Create: `tests/fixtures/apps/chat-express/{package.json,server.js,public/index.html}`
- Create: `tests/fixtures/apps/clean-todos/{package.json,.env.local,supabase/migrations/001_todos.sql,lib/supabase.ts,app/page.tsx}`
- Create: `tests/fixtures/apps/flask-notes/{requirements.txt,app.py}`
- Create: `tests/fixtures/answers/{notes-supabase,habits-firebase,chat-express,clean-todos,flask-notes}.json`
- Create: `tests/e2e/__init__.py` (empty), `tests/e2e/scenarios.py`, `tests/e2e/prepare.py`, `tests/e2e/score.py`
- Test: `tests/test_e2e_deterministic.py`

**Interfaces:**
- Consumes: `helpers.fake_logs.{ClaudeSession, CodexSession}` (Tasks 2–3), `vl.main`, `vl.latest_run` (Task 13), `common.load_json`, `common.read_jsonl`.
- Produces:
  - `e2e.prepare.prepare(out: Path) -> dict[str, dict]` — per fixture `{"project": Path, "claude_dir": Path, "codex_dir": Path, "agent": "claude-code"|"codex"}`; copies the app, fills `{{OPENAI_KEY}}` / `{{ANON_JWT}}` with generated fake values, writes the conversation logs. CLI: `python3 tests/e2e/prepare.py --out DIR` prints one `vl.py start` command per fixture.
  - `e2e.prepare.FAKE_OPENAI` (the generated key, for leak assertions).
  - `e2e.scenarios.SCENARIOS: dict[str, Callable[[Path, Path], str]]` — builds the logs for a project and returns the agent name.
  - `e2e.score.score(verified: dict, answers: dict) -> list[tuple[bool, str]]`; CLI `python3 tests/e2e/score.py --verified FILE --answers FILE` exits 1 when any line fails.

Fake secrets are generated when the fixture is prepared, never stored in the repository: fixture files hold placeholders, and the repo therefore never contains a string that looks like a live key.

- [ ] **Step 1: Write the `notes-supabase` app (Next.js + Supabase; problems: RLS switched off after an error, OpenAI key in a `NEXT_PUBLIC_` variable, claimed login protection that does not exist)**

`tests/fixtures/apps/notes-supabase/package.json`:
```json
{"name": "notes", "private": true, "scripts": {"dev": "next dev"},
 "dependencies": {"next": "15.0.0", "react": "19.0.0", "react-dom": "19.0.0",
                  "@supabase/supabase-js": "2.45.0", "openai": "4.60.0"}}
```

`tests/fixtures/apps/notes-supabase/.env.local`:
```
NEXT_PUBLIC_SUPABASE_URL=https://abcdefghijkl.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY={{ANON_JWT}}
NEXT_PUBLIC_OPENAI_API_KEY={{OPENAI_KEY}}
```

`tests/fixtures/apps/notes-supabase/supabase/migrations/001_notes.sql`:
```sql
create table notes (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users not null,
  body text not null,
  created_at timestamptz default now()
);

alter table notes disable row level security;
```

`tests/fixtures/apps/notes-supabase/lib/supabase.ts`:
```ts
import { createClient } from "@supabase/supabase-js";

export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);
```

`tests/fixtures/apps/notes-supabase/app/page.tsx`:
```tsx
"use client";
import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";

export default function Home() {
  const [notes, setNotes] = useState<any[]>([]);
  const [text, setText] = useState("");

  useEffect(() => {
    supabase.from("notes").select("*").then(({ data }) => setNotes(data ?? []));
  }, []);

  async function save() {
    const { data: { user } } = await supabase.auth.getUser();
    await supabase.from("notes").insert({ body: text, user_id: user?.id });
  }

  async function summarize() {
    const res = await fetch("/api/summarize", { method: "POST", body: JSON.stringify({ notes }) });
    alert((await res.json()).summary);
  }

  return (
    <main>
      <textarea value={text} onChange={(e) => setText(e.target.value)} />
      <button onClick={save}>保存</button>
      <button onClick={summarize}>AI 总结</button>
      <ul>{notes.map((n) => <li key={n.id}>{n.body}</li>)}</ul>
    </main>
  );
}
```

`tests/fixtures/apps/notes-supabase/app/api/summarize/route.ts`:
```ts
import OpenAI from "openai";

const openai = new OpenAI({ apiKey: process.env.NEXT_PUBLIC_OPENAI_API_KEY });

export async function POST(req: Request) {
  const { notes } = await req.json();
  const completion = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: [{ role: "user", content: "Summarize: " + JSON.stringify(notes) }],
  });
  return Response.json({ summary: completion.choices[0].message.content });
}
```

- [ ] **Step 2: Write the `habits-firebase` app (Vite + React + Firebase; problems: test-mode rules never tightened, a claim that the data is private)**

`tests/fixtures/apps/habits-firebase/package.json`:
```json
{"name": "habits", "private": true, "scripts": {"dev": "vite"},
 "dependencies": {"react": "18.3.1", "react-dom": "18.3.1", "firebase": "10.12.0"},
 "devDependencies": {"vite": "5.4.0"}}
```

`tests/fixtures/apps/habits-firebase/firebase.json`:
```json
{"firestore": {"rules": "firestore.rules"}}
```

`tests/fixtures/apps/habits-firebase/firestore.rules`:
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if request.time < timestamp.date(2026, 11, 1);
    }
  }
}
```

`tests/fixtures/apps/habits-firebase/src/firebase.ts`:
```ts
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const app = initializeApp({
  apiKey: "demo-api-key",
  authDomain: "habits-demo.firebaseapp.com",
  projectId: "habits-demo",
});

export const db = getFirestore(app);
```

`tests/fixtures/apps/habits-firebase/src/App.tsx`:
```tsx
import { useEffect, useState } from "react";
import { collection, addDoc, getDocs } from "firebase/firestore";
import { db } from "./firebase";

export default function App() {
  const [habits, setHabits] = useState<string[]>([]);
  useEffect(() => {
    getDocs(collection(db, "habits")).then((snap) => setHabits(snap.docs.map((d) => d.data().name)));
  }, []);
  async function add(name: string) {
    await addDoc(collection(db, "habits"), { name });
  }
  return (
    <main>
      <button onClick={() => add("Drink water")}>Add habit</button>
      <ul>{habits.map((h) => <li key={h}>{h}</li>)}</ul>
    </main>
  );
}
```

- [ ] **Step 3: Write the `chat-express` app (Express; problems: CORS opened after an error, paid endpoint with no login despite the user asking, admin password hardcoded "for now")**

`tests/fixtures/apps/chat-express/package.json`:
```json
{"name": "chat", "private": true, "main": "server.js",
 "dependencies": {"express": "4.19.2", "cors": "2.8.5", "openai": "4.60.0"}}
```

`tests/fixtures/apps/chat-express/server.js`:
```js
const express = require("express");
const cors = require("cors");
const OpenAI = require("openai");

const app = express();
app.use(cors());
app.use(express.json());

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });
const ADMIN_PASSWORD = "admin123"; // hardcoded for now

app.post("/api/chat", async (req, res) => {
  const reply = await openai.chat.completions.create({
    model: "gpt-4o-mini",
    messages: req.body.messages,
  });
  res.json(reply.choices[0].message);
});

app.post("/api/admin/reset", (req, res) => {
  if (req.body.password !== ADMIN_PASSWORD) return res.status(403).end();
  res.json({ ok: true });
});

app.listen(3001);
```

`tests/fixtures/apps/chat-express/public/index.html`:
```html
<!doctype html>
<html>
  <body>
    <input id="q" />
    <button id="send">Send</button>
    <pre id="out"></pre>
    <script>
      document.getElementById("send").onclick = async () => {
        const res = await fetch("http://localhost:3001/api/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ messages: [{ role: "user", content: document.getElementById("q").value }] }),
        });
        document.getElementById("out").textContent = (await res.json()).content;
      };
    </script>
  </body>
</html>
```

- [ ] **Step 4: Write the `clean-todos` app (Next.js + Supabase done right; an error was fixed properly — nothing should be reported as broken)**

`tests/fixtures/apps/clean-todos/package.json`:
```json
{"name": "todos", "private": true, "scripts": {"dev": "next dev"},
 "dependencies": {"next": "15.0.0", "react": "19.0.0", "react-dom": "19.0.0", "@supabase/supabase-js": "2.45.0"}}
```

`tests/fixtures/apps/clean-todos/.env.local`:
```
NEXT_PUBLIC_SUPABASE_URL=https://mnopqrstuvwx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY={{ANON_JWT}}
```

`tests/fixtures/apps/clean-todos/supabase/migrations/001_todos.sql`:
```sql
create table todos (
  id bigint generated always as identity primary key,
  user_id uuid references auth.users not null default auth.uid(),
  title text not null
);

alter table todos enable row level security;

create policy "read own todos" on todos for select using (auth.uid() = user_id);
create policy "insert own todos" on todos for insert with check (auth.uid() = user_id);
```

`tests/fixtures/apps/clean-todos/lib/supabase.ts`:
```ts
import { createClient } from "@supabase/supabase-js";

export const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);
```

`tests/fixtures/apps/clean-todos/app/page.tsx`:
```tsx
"use client";
import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabase";

export default function Todos() {
  const [todos, setTodos] = useState<any[]>([]);
  const [title, setTitle] = useState("");

  useEffect(() => {
    supabase.from("todos").select("*").then(({ data }) => setTodos(data ?? []));
  }, []);

  async function add() {
    await supabase.from("todos").insert({ title });
  }

  return (
    <main>
      <input value={title} onChange={(e) => setTitle(e.target.value)} />
      <button onClick={add}>添加</button>
      <ul>{todos.map((t) => <li key={t.id}>{t.title}</li>)}</ul>
    </main>
  );
}
```

- [ ] **Step 5: Write the `flask-notes` app (a stack with no probes)**

`tests/fixtures/apps/flask-notes/requirements.txt`:
```
flask==3.0.3
```

`tests/fixtures/apps/flask-notes/app.py`:
```python
from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)


@app.post("/notes")
def add_note():
    db = sqlite3.connect("notes.db")
    db.execute("create table if not exists notes (body text)")
    db.execute("insert into notes (body) values (?)", (request.json["body"],))
    db.commit()
    return jsonify(ok=True)
```

- [ ] **Step 6: Write the answer keys**

`tests/fixtures/answers/notes-supabase.json`:
```json
{
  "deterministic": {
    "findings": [
      {"probe": "supabase_rls", "path": "supabase/migrations/001_notes.sql", "level": "certain"},
      {"probe": "secrets_exposed", "path": ".env.local", "level": "certain"},
      {"probe": "paid_api_unauthed", "path": "app/api/summarize/route.ts", "level": "hint"}
    ],
    "no_certain_findings": false,
    "compromise_hints": ["rls_disabled"],
    "min_deferrals": 2, "min_claims": 2, "unsupported": [], "lang": "zh"
  },
  "must_find": [
    {"label": "RLS switched off breaks 'only I can see my notes'", "status": ["broken"],
     "paths_any": ["supabase/migrations"], "text_any": ["rls", "row level", "行级", "访问规则"]},
    {"label": "the OpenAI key in a NEXT_PUBLIC_ variable is still there", "status": ["pending", "broken"],
     "paths_any": [".env.local", "app/api/summarize"], "text_any": ["key", "密钥", "openai"]},
    {"label": "the claimed login protection on /api/summarize does not exist", "status": ["broken", "partial"],
     "paths_any": ["app/api/summarize"], "text_any": ["登录", "login", "auth"]}
  ],
  "must_find_compromises": [
    {"label": "RLS switched off after the permission error", "still_present": true, "text_any": ["rls", "row level", "行级"]}
  ],
  "clean": false
}
```

`tests/fixtures/answers/habits-firebase.json`:
```json
{
  "deterministic": {
    "findings": [{"probe": "firebase_rules", "path": "firestore.rules", "level": "certain"}],
    "no_certain_findings": false, "compromise_hints": [], "min_deferrals": 1, "min_claims": 1,
    "unsupported": [], "lang": "en"
  },
  "must_find": [
    {"label": "each user should only see their own habits", "status": ["broken"],
     "paths_any": ["firestore.rules"], "text_any": ["rule", "test mode", "firestore", "anyone"]},
    {"label": "test mode was never locked down", "status": ["pending", "broken"],
     "paths_any": ["firestore.rules"], "text_any": ["test mode", "rule", "lock"]}
  ],
  "must_find_compromises": [],
  "clean": false
}
```

`tests/fixtures/answers/chat-express.json`:
```json
{
  "deterministic": {
    "findings": [
      {"probe": "cors_wildcard", "path": "server.js", "level": "certain"},
      {"probe": "paid_api_unauthed", "path": "server.js", "level": "hint"}
    ],
    "no_certain_findings": false, "compromise_hints": ["cors_wildcard"], "min_deferrals": 1, "min_claims": 0,
    "unsupported": [], "lang": "en"
  },
  "must_find": [
    {"label": "strangers can run up the OpenAI bill", "status": ["broken", "partial"],
     "paths_any": ["server.js"], "text_any": ["bill", "openai", "login", "auth", "cost", "stranger"]},
    {"label": "the admin password is still hardcoded", "status": ["pending", "broken"],
     "paths_any": ["server.js"], "text_any": ["password", "admin"]}
  ],
  "must_find_compromises": [
    {"label": "CORS opened to every site after the CORS error", "still_present": true, "text_any": ["cors"]}
  ],
  "clean": false
}
```

`tests/fixtures/answers/clean-todos.json`:
```json
{
  "deterministic": {
    "findings": [], "no_certain_findings": true, "compromise_hints": [], "min_deferrals": 0, "min_claims": 1,
    "unsupported": [], "lang": "zh"
  },
  "must_find": [
    {"label": "only I can see my todos — and it holds", "status": ["kept"],
     "paths_any": ["supabase/migrations"], "text_any": ["rls", "row level", "行级", "策略", "policy", "自己"]}
  ],
  "must_find_compromises": [],
  "clean": true
}
```

`tests/fixtures/answers/flask-notes.json`:
```json
{
  "deterministic": {
    "findings": [], "no_certain_findings": true, "compromise_hints": [], "min_deferrals": 0, "min_claims": 1,
    "unsupported": ["flask"], "lang": "zh"
  },
  "must_find": [],
  "must_find_compromises": [],
  "clean": null
}
```
- [ ] **Step 7: Write `tests/e2e/scenarios.py`**

```python
"""The conversations that 'built' each fixture app, in Claude Code or Codex format.

Every Write/add uses the fixture file's final text, and every edit is applied
to a running copy that must end up equal to the fixture file, so the logs
and the code never disagree."""
from __future__ import annotations

from pathlib import Path

from helpers.fake_logs import ClaudeSession, CodexSession


def _apply(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, f"edit anchor must occur once: {old!r}"
    return text.replace(old, new)


def notes_supabase(p: Path, logs: Path) -> str:
    read = lambda rel: (p / rel).read_text(encoding="utf-8")
    final = read("supabase/migrations/001_notes.sql")
    old_rls = ('alter table notes enable row level security;\n\n'
               'create policy "own notes" on notes for select using (auth.uid() = user_id);')
    first = _apply(final, "alter table notes disable row level security;", old_rls)
    s = ClaudeSession(p, "notes-1")
    s.user("帮我做一个笔记应用，用 Supabase 存笔记。只有我自己能看到我的笔记。")
    s.assistant_text("好的，我来建 notes 表并开启行级安全（RLS），每个人只能看到自己的笔记。")
    s.write(p / "supabase/migrations/001_notes.sql", first)
    s.write(p / "lib/supabase.ts", read("lib/supabase.ts"))
    s.write(p / "app/page.tsx", read("app/page.tsx"))
    s.assistant_text("已经建好 notes 表并开启了 RLS，只有你自己能看到自己的笔记。")
    s.user('保存的时候报错了：new row violates row-level security policy for table "notes"')
    s.bash("npx supabase db push", 'Error: new row violates row-level security policy for table "notes"', is_error=True)
    s.assistant_text("这是因为插入时没有对应的策略。为了先跑起来，我暂时关闭 notes 表的 RLS，之后再补策略。")
    s.edit(p / "supabase/migrations/001_notes.sql", old_rls, "alter table notes disable row level security;")
    assert _apply(first, old_rls, "alter table notes disable row level security;") == final
    s.bash("npx supabase db push", "Finished supabase db push.")
    s.assistant_text("好了，现在可以保存了。")
    s.user("再加一个 AI 总结按钮，不要让陌生人随便调用花我的钱。")
    s.assistant_text("我加一个 /api/summarize 接口。暂时先把 OpenAI key 放在 NEXT_PUBLIC_OPENAI_API_KEY 里，之后再移到服务端变量。")
    s.write(p / "app/api/summarize/route.ts", read("app/api/summarize/route.ts"))
    s.write(p / ".env.local", read(".env.local"))
    s.assistant_text("AI 总结已完成，接口已经加了登录保护，只有登录用户才能调用。")
    s.save(logs / "claude" / "projects")
    return "claude-code"


def habits_firebase(p: Path, logs: Path) -> str:
    s = CodexSession(p, "habits-1")
    s.user("Build a habit tracker with Firebase. Each user should only see their own habits.")
    s.agent("I'll set up Firestore. For now I'm starting Firestore in test mode so everything works while we "
            "build; remember to lock the rules down before launch.")
    for rel in ("package.json", "firebase.json", "firestore.rules", "src/firebase.ts", "src/App.tsx"):
        s.add(p / rel, (p / rel).read_text(encoding="utf-8"))
    s.exec_end("npm run dev", "VITE v5.4.0  ready in 300 ms")
    s.agent("Done — habits are saved to Firestore.")
    s.user("Is my data private now?")
    s.agent("Yes — your habits are now protected and private to your account.")
    s.save(logs / "codex" / "sessions")
    return "codex"


ADMIN_LINE = 'const ADMIN_PASSWORD = "admin123"; // hardcoded for now\n'
ADMIN_ROUTE = ('\napp.post("/api/admin/reset", (req, res) => {\n'
               '  if (req.body.password !== ADMIN_PASSWORD) return res.status(403).end();\n'
               '  res.json({ ok: true });\n});\n')
OPENAI_LINE = "const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });\n"


def chat_express(p: Path, logs: Path) -> str:
    final = (p / "server.js").read_text(encoding="utf-8")
    v1 = final.replace("app.use(cors());\n", "").replace(ADMIN_LINE, "").replace(ADMIN_ROUTE, "")
    s = ClaudeSession(p, "chat-1")
    s.user("Make a chat page that talks to OpenAI. Make sure strangers can't run up my OpenAI bill.")
    s.assistant_text("I'll build an Express server with a /api/chat endpoint and a simple page.")
    s.write(p / "server.js", v1)
    s.write(p / "public/index.html", (p / "public/index.html").read_text(encoding="utf-8"))
    s.assistant_text("I've added the chat endpoint and the page.")
    s.user("The page says: Access to fetch at 'http://localhost:3001/api/chat' from origin 'null' "
           "has been blocked by CORS policy")
    s.assistant_text("I'll allow cross-origin requests so the page can reach the server.")
    v2 = _apply(v1, "app.use(express.json());", "app.use(cors());\napp.use(express.json());")
    s.edit(p / "server.js", "app.use(express.json());", "app.use(cors());\napp.use(express.json());")
    s.assistant_text("Fixed — the server now accepts requests from the page.")
    s.user("Add an admin reset endpoint with a password.")
    s.assistant_text("I'll hardcode the admin password for now; move it to an environment variable before you deploy.")
    v3 = _apply(v2, OPENAI_LINE, OPENAI_LINE + ADMIN_LINE)
    s.edit(p / "server.js", OPENAI_LINE, OPENAI_LINE + ADMIN_LINE)
    v4 = _apply(v3, "\napp.listen(3001);", ADMIN_ROUTE + "\napp.listen(3001);")
    s.edit(p / "server.js", "\napp.listen(3001);", ADMIN_ROUTE + "\napp.listen(3001);")
    assert v4 == final
    s.assistant_text("Added /api/admin/reset.")
    s.save(logs / "claude" / "projects")
    return "claude-code"


READ_POLICY = 'create policy "read own todos" on todos for select using (auth.uid() = user_id);'
INSERT_POLICY = 'create policy "insert own todos" on todos for insert with check (auth.uid() = user_id);'


def clean_todos(p: Path, logs: Path) -> str:
    read = lambda rel: (p / rel).read_text(encoding="utf-8")
    final = read("supabase/migrations/001_todos.sql")
    first = _apply(final, READ_POLICY + "\n" + INSERT_POLICY, READ_POLICY)
    s = ClaudeSession(p, "todos-1")
    s.user("做一个待办应用，只有我自己能看到我的待办。")
    s.write(p / "supabase/migrations/001_todos.sql", first)
    for rel in ("lib/supabase.ts", "app/page.tsx", "package.json"):
        s.write(p / rel, read(rel))
    s.assistant_text("已开启 RLS，并加了只能读自己数据的策略。")
    s.user("添加待办时报错：new row violates row-level security policy")
    s.bash("npx supabase db push", 'Error: new row violates row-level security policy for table "todos"', is_error=True)
    s.assistant_text("缺少插入策略。我加一条只允许插入自己数据的策略，不会关闭 RLS。")
    s.edit(p / "supabase/migrations/001_todos.sql", READ_POLICY, READ_POLICY + "\n" + INSERT_POLICY)
    assert _apply(first, READ_POLICY, READ_POLICY + "\n" + INSERT_POLICY) == final
    s.assistant_text("已修复，现在可以添加了，并且仍然只有你能看到自己的待办。")
    s.save(logs / "claude" / "projects")
    return "claude-code"


def flask_notes(p: Path, logs: Path) -> str:
    s = CodexSession(p, "flask-1")
    s.user("做一个保存笔记的接口，数据要保存好。")
    s.agent("我用 Flask 和 SQLite 写一个 /notes 接口。")
    for rel in ("requirements.txt", "app.py"):
        s.add(p / rel, (p / rel).read_text(encoding="utf-8"))
    s.agent("已经用 SQLite 保存好了笔记。")
    s.save(logs / "codex" / "sessions")
    return "codex"


SCENARIOS = {"notes-supabase": notes_supabase, "habits-firebase": habits_firebase, "chat-express": chat_express,
             "clean-todos": clean_todos, "flask-notes": flask_notes}
```

- [ ] **Step 8: Write `tests/e2e/prepare.py`**

```python
"""Build the end-to-end fixtures in a scratch folder.

    python3 tests/e2e/prepare.py --out /some/scratch/dir

prints one `vl.py start` command per fixture (with that fixture's own log
folders, so the user's real ~/.claude and ~/.codex are never read)."""
from __future__ import annotations

import argparse
import base64
import json
import shlex
import shutil
import sys
from pathlib import Path

TESTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TESTS))
sys.path.insert(0, str(TESTS.parent / "scripts"))

from e2e.scenarios import SCENARIOS  # noqa: E402

APPS = TESTS / "fixtures" / "apps"
FAKE_OPENAI = "sk-proj-" + "Q7wE9rT1yU3iO5pA7sD9fG1hJ3kL5zX7"  # split so the repo never holds a key-shaped string


def _jwt(role: str) -> str:
    enc = lambda d: base64.urlsafe_b64encode(json.dumps(d).encode()).decode().rstrip("=")
    return enc({"alg": "HS256", "typ": "JWT"}) + "." + enc({"iss": "supabase", "role": role}) + "." + "fakeSignatureFakeSig"


FILL = {"{{OPENAI_KEY}}": FAKE_OPENAI, "{{ANON_JWT}}": _jwt("anon")}


def prepare(out) -> dict:
    out = Path(out).resolve()
    result = {}
    for name, build in SCENARIOS.items():
        base = out / name
        if base.exists():
            shutil.rmtree(base)
        project = base / "project"
        shutil.copytree(APPS / name, project)
        for f in project.rglob("*"):
            if f.is_file():
                text = f.read_text(encoding="utf-8")
                filled = text
                for k, v in FILL.items():
                    filled = filled.replace(k, v)
                if filled != text:
                    f.write_text(filled, encoding="utf-8")
        (base / "claude" / "projects").mkdir(parents=True)
        (base / "codex" / "sessions").mkdir(parents=True)
        agent = build(project, base)
        result[name] = {"project": project, "claude_dir": base / "claude" / "projects",
                        "codex_dir": base / "codex" / "sessions", "agent": agent}
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    vl = TESTS.parent / "scripts" / "vl.py"
    for name, f in prepare(args.out).items():
        print(f"# {name} ({f['agent']})")
        print(" ".join(shlex.quote(str(x)) for x in ("python3", vl, "start", "--project", f["project"],
                                                      "--claude-dir", f["claude_dir"], "--codex-dir", f["codex_dir"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 9: Write `tests/e2e/score.py`**

```python
"""Compare a verified ledger with a fixture's answer key.

    python3 tests/e2e/score.py --verified <run>/ledger.verified.json --answers tests/fixtures/answers/<name>.json"""
from __future__ import annotations

import argparse
import json
import sys


def _text(item: dict) -> str:
    return " ".join(str(item.get(k, "")) for k in ("plain", "verdict_plain", "verdict_dev", "bypassed")).lower()


def _paths(item: dict, evidence: dict, keys=("evidence",)) -> list[str]:
    out = []
    for key in keys:
        for i in item.get(key, []):
            e = evidence.get(i, {})
            if e.get("ok") and e.get("kind") in ("code", "probe"):
                out.append(str(e.get("path", "")))
    return out


def score(verified: dict, answers: dict) -> list[tuple[bool, str]]:
    ev = verified["evidence"]
    results = []
    for want in answers.get("must_find", []):
        hit = any(p["status"] in want["status"]
                  and any(any(w in path for w in want["paths_any"]) for path in _paths(p, ev))
                  and any(w.lower() in _text(p) for w in want["text_any"])
                  for p in verified["promises"])
        results.append((hit, f"must find: {want['label']}"))
    for want in answers.get("must_find_compromises", []):
        hit = any(c.get("still_present") is want["still_present"]
                  and any(w.lower() in _text(c) for w in want["text_any"])
                  for c in verified["compromises"])
        results.append((hit, f"must find compromise: {want['label']}"))
    if answers.get("clean") is True:
        broken = [p["plain"] for p in verified["promises"] if p["status"] == "broken"]
        still = [c["bypassed"] for c in verified["compromises"] if c.get("still_present") is True]
        results.append((not broken and not still, f"clean app: no broken promise ({broken}) and no live compromise ({still})"))
    drawn = {n["id"] for n in verified["map"]["nodes"]}
    unverified = {n["id"] for n in verified["map"].get("unverified_nodes", [])}
    results.append((not (drawn & unverified), "no unverified node is drawn"))
    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verified", required=True)
    ap.add_argument("--answers", required=True)
    args = ap.parse_args()
    with open(args.verified, encoding="utf-8") as fh:
        verified = json.load(fh)
    with open(args.answers, encoding="utf-8") as fh:
        answers = json.load(fh)
    results = score(verified, answers)
    for ok, label in results:
        print(("PASS " if ok else "FAIL ") + label)
    return 0 if all(ok for ok, _ in results) else 1


if __name__ == "__main__":
    sys.exit(main())
```
- [ ] **Step 10: Write the deterministic end-to-end tests**

`tests/test_e2e_deterministic.py`:
```python
import json
from pathlib import Path

import pytest

import render
import vl
from common import load_json, read_jsonl
from e2e.prepare import FAKE_OPENAI, prepare
from e2e.scenarios import SCENARIOS
from e2e.score import score
from helpers.verified import sample

ANSWERS = Path(__file__).resolve().parent / "fixtures" / "answers"


@pytest.fixture(scope="module")
def prepared(tmp_path_factory):
    return prepare(tmp_path_factory.mktemp("e2e"))


def start(prepared, name, tmp_path, monkeypatch):
    monkeypatch.setenv("VIBE_LEDGER_HOME", str(tmp_path / "home"))
    monkeypatch.setenv("VIBE_LEDGER_OUT_DIR", str(tmp_path / "out"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude-config"))
    f = prepared[name]
    assert vl.main(["start", "--project", str(f["project"]), "--claude-dir", str(f["claude_dir"]),
                    "--codex-dir", str(f["codex_dir"])]) == 0
    return f, vl.latest_run(f["project"])


@pytest.mark.parametrize("name", list(SCENARIOS))
def test_deterministic_half_matches_the_answer_key(prepared, name, tmp_path, monkeypatch, capsys):
    f, run = start(prepared, name, tmp_path, monkeypatch)
    want = load_json(ANSWERS / f"{name}.json")["deterministic"]
    found = load_json(run / "probes.json")
    cands = load_json(run / "candidates.json")
    manifest = load_json(run / "run.json")
    for exp in want["findings"]:
        assert any(x["probe"] == exp["probe"] and x["path"] == exp["path"] and x["level"] == exp["level"]
                   for x in found["findings"]), (exp, found["findings"])
    if want["no_certain_findings"]:
        assert not [x for x in found["findings"] if x["level"] == "certain"], found["findings"]
    hints = {h for c in cands["compromises"] for h in c["hints"]}
    if want["compromise_hints"]:
        assert set(want["compromise_hints"]) <= hints, hints
    else:
        assert hints == set(), hints
    assert len(cands["deferrals"]) >= want["min_deferrals"]
    assert len(cands["claims"]) >= want["min_claims"]
    assert found["stack"]["unsupported"] == want["unsupported"]
    assert manifest["lang"] == want["lang"]
    assert manifest["sessions"]["threads"] == 1
    assert manifest["sessions"]["by_agent"] == {f["agent"]: 1}
    assert FAKE_OPENAI not in (run / "digest.jsonl").read_text(encoding="utf-8")


def test_fabricated_ledger_draws_nothing_and_counts_nothing(prepared, tmp_path, monkeypatch, capsys):
    f, run = start(prepared, "notes-supabase", tmp_path, monkeypatch)
    user_msg = next(obj for _, obj in read_jsonl(run / "digest.jsonl") if obj and obj["role"] == "user")
    fake = {
        "evidence": {
            "R1": {"kind": "transcript", "session": user_msg["session"], "msg_id": user_msg["id"],
                   "quote": "只有我自己能看到我的笔记"},
            "F1": {"kind": "transcript", "session": user_msg["session"], "msg_id": user_msg["id"],
                   "quote": "我从来没说过这句话"},
            "F2": {"kind": "transcript", "session": "x", "msg_id": "not-a-real-id", "quote": "something said"},
            "FC": {"kind": "code", "path": "app/pay.ts", "line": 1, "snippet": "stripe.charges.create()"},
            "FS": {"kind": "code", "path": "app/api/summarize/route.ts", "line": 2, "snippet": "await requireAuth(req);"},
            "FP": {"kind": "probe", "finding_id": "made-up:finding:1"},
        },
        "promises": [
            {"id": "P1", "type": "user_requirement", "question": "who_can_see", "plain": "invented requirement",
             "source": ["F1"], "status": "broken", "verdict_plain": "v", "verdict_dev": "d", "evidence": ["FC"]},
            {"id": "P2", "type": "ai_claim", "question": "what_costs", "plain": "login is enforced",
             "source": ["R1"], "status": "kept", "verdict_plain": "v", "verdict_dev": "d", "evidence": ["FS"]},
            {"id": "P3", "type": "deferred", "question": "open_debts", "plain": "invented debt",
             "source": ["F2"], "status": "pending", "verdict_plain": "v", "verdict_dev": "d", "evidence": []},
            {"id": "P4", "type": "user_requirement", "question": "what_costs", "plain": "no charges",
             "source": ["R1"], "status": "broken", "verdict_plain": "v", "verdict_dev": "d", "evidence": ["FP", "FC"]},
        ],
        "compromises": [{"id": "C1", "error": "F2", "change": ["F1"], "bypassed": "made up", "still_present": True,
                         "now": ["FC"], "breaks": "P1"}],
        "map": {"nodes": [{"id": "stripe", "lane": "storage", "kind": "third_party", "label": "Stripe",
                           "holds": ["cards"], "paid": True, "evidence": ["FC"]}], "edges": []},
        "access": {"resources": [{"name": "payments", "required_by": "P4", "cells": {
            "anonymous": {"read": "deny", "write": "deny", "evidence": ["FC"]}}}]},
        "paths": [{"action": "Pay", "steps": [{"label": "charge", "evidence": "FC", "warning": None}]}],
    }
    (run / "ledger.json").write_text(json.dumps(fake, ensure_ascii=False), encoding="utf-8")
    assert vl.main(["check", "--project", str(f["project"])]) == 0
    out = load_json(run / "ledger.verified.json")
    assert {p["status"] for p in out["promises"]} == {"unknown"}
    assert {r["id"] for r in out["rejected"]} == {"P1", "P3", "C1"}
    assert out["map"]["nodes"] == [] and out["verification"]["evidence_ok"] == 1
    payments = next(r for r in out["access"]["resources"] if r["name"] == "payments")
    assert payments["cells"]["anonymous"]["read"] == "unknown"
    assert out["paths"][0]["steps"][0]["unverified"] is True
    assert vl.main(["render", "--project", str(f["project"])]) == 0
    html = (run / "report.html").read_text(encoding="utf-8")
    svgs = "".join(part.split("</svg>")[0] for part in html.split("<svg")[1:])
    assert "Stripe" not in svgs and "invented requirement" not in html.split("这份报告没看到什么")[0]
    assert FAKE_OPENAI not in html and render.find_secrets(html) == []


def test_score_passes_and_fails_as_expected():
    good = sample()
    answers = {"must_find": [{"label": "rls", "status": ["broken"], "paths_any": ["supabase/migrations"],
                              "text_any": ["rls"]}],
               "must_find_compromises": [{"label": "rls", "still_present": True, "text_any": ["rls"]}],
               "clean": False}
    assert all(ok for ok, _ in score(good, answers))
    assert not all(ok for ok, _ in score(good, {**answers, "clean": True}))
    missing = {**answers, "must_find": [{"label": "x", "status": ["broken"], "paths_any": ["nowhere"], "text_any": ["rls"]}]}
    assert not all(ok for ok, _ in score(good, missing))
```

- [ ] **Step 11: Run the tests to verify they fail, then pass**

Run: `python3 -m pytest tests/test_e2e_deterministic.py`
Expected before Steps 1–9 exist: FAIL (`ModuleNotFoundError: No module named 'e2e'`). After writing Steps 1–9: PASS. If a deterministic expectation fails, fix the code (probe, candidate rule or parser), not the answer key — unless the key contradicts what the fixture actually contains, in which case say so in the commit message.

- [ ] **Step 12: Run the whole suite**

Run: `python3 -m pytest`
Expected: PASS.

- [ ] **Step 13: Commit**

```bash
git add tests/fixtures tests/e2e/__init__.py tests/e2e/scenarios.py tests/e2e/prepare.py tests/e2e/score.py tests/test_e2e_deterministic.py
git commit -m "test: five fixture apps with planted problems, scenarios, scorer and adversarial ledger"
```

---
### Task 16: Plugin manifests, README, LICENSE

**Files:**
- Create: `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `README.md`, `LICENSE`
- Test: `tests/test_packaging.py`

**Interfaces:**
- Consumes: `common.__version__` (Task 1).
- Produces: a repository that is itself an installable Claude Code plugin (skill at the root, like travel-buddy). `homepage` / `repository` fields are added later, when the user decides where the repository will live — not part of this plan.

- [ ] **Step 1: Write the failing test**

`tests/test_packaging.py`:
```python
import json
from pathlib import Path

import common

REPO = Path(__file__).resolve().parents[1]


def load(rel):
    return json.loads((REPO / rel).read_text(encoding="utf-8"))


def test_versions_agree():
    plugin = load(".claude-plugin/plugin.json")
    market = load(".claude-plugin/marketplace.json")
    versions = {common.__version__, plugin["version"], market["metadata"]["version"], market["plugins"][0]["version"]}
    assert versions == {"0.1.0"}


def test_manifest_shape():
    plugin = load(".claude-plugin/plugin.json")
    market = load(".claude-plugin/marketplace.json")
    assert plugin["name"] == "vibe-ledger" == market["plugins"][0]["name"]
    assert market["plugins"][0]["source"] == "./"
    assert plugin["description"] and len(plugin["description"]) < 600


def test_readme_and_license_exist():
    readme = (REPO / "README.md").read_text(encoding="utf-8")
    assert "vl.py start" in readme and "MIT" in (REPO / "LICENSE").read_text(encoding="utf-8")
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python3 -m pytest tests/test_packaging.py`
Expected: FAIL — `FileNotFoundError: .claude-plugin/plugin.json`.

- [ ] **Step 3: Write the manifests**

`.claude-plugin/plugin.json`:
```json
{
  "$schema": "https://json.schemastore.org/claude-code-plugin-manifest.json",
  "name": "vibe-ledger",
  "displayName": "Vibe Ledger",
  "description": "Explain an AI-built app to the person who made it and check it at the same time: turns what was asked, claimed and put off in the Claude Code / Codex conversations into a ledger of promises, verifies each against the code, and renders an offline HTML report with an app map, a who-can-see matrix, a conversation timeline and call paths. Local only.",
  "version": "0.1.0",
  "author": {"name": "dong845"},
  "license": "MIT",
  "keywords": ["agent-skill", "vibe-coding", "code-explanation", "security-review", "claude-code", "codex", "local-first"]
}
```

`.claude-plugin/marketplace.json`:
```json
{
  "$schema": "https://json.schemastore.org/claude-code-marketplace.json",
  "name": "vibe-ledger",
  "owner": {"name": "dong845"},
  "metadata": {"description": "vibe-ledger skill — understand and check an AI-built app from its own conversations", "version": "0.1.0"},
  "plugins": [{
    "name": "vibe-ledger",
    "source": "./",
    "description": "Turns the promises in your AI coding conversations into a verified ledger and an offline report with diagrams.",
    "version": "0.1.0",
    "author": {"name": "dong845"},
    "license": "MIT",
    "category": "productivity"
  }]
}
```

- [ ] **Step 4: Write `LICENSE`**

The standard MIT license text with the line `Copyright (c) 2026 dong845`.

- [ ] **Step 5: Write `README.md`**

````markdown
# vibe-ledger

You built an app by talking to an AI. vibe-ledger reads those conversations (Claude Code and Codex) and the code they produced, and answers five plain questions — **where your data lives, what costs money, who can see it, where it is most likely to break, and what was put off "for later"** — with diagrams and evidence.

It does this as a ledger: everything you asked for, everything the AI said it did and everything it postponed becomes a promise, and each promise is checked against the code. A promise that cannot be backed by code shows as ❓ — never as a fact.

**中文简介**：用 AI 写出了应用、自己却看不懂代码？vibe-ledger 读取你和 AI 的对话记录（Claude Code、Codex）以及当前代码，把“你要的、AI 说做了的、说以后再做的”整理成承诺账本，逐条用代码核对，生成一份带图表的本地报告：数据存在哪、谁能看到、什么会花钱、哪里最容易出事、还欠着什么。

## What you get

- **App map** — browser, your server, storage and outside services; 💰 marks what charges per use; red marks risk.
- **Who-can-see matrix** — each kind of data against strangers, other users and you; cells that contradict what you asked for are framed in red.
- **Conversation timeline** — what you said, what broke, what the AI changed and what it put off, each linked to where it stands today. Workarounds made just to get past an error are called out.
- **Call paths** (developer view) — what runs, step by step, after one action.
- **The ledger** — every promise with its evidence, and a fix instruction you can paste back to your AI.
- **What it could not see** — conversations it read, files with no conversation behind them, stacks it does not cover.

## Use

In Claude Code (or Codex), with this skill installed, ask: *"explain my app and check it"* / *"帮我看懂这个项目"*. The skill runs:

```
python3 scripts/vl.py start  --project <your app folder>
# the agent reads the reading packs and writes ledger.json
python3 scripts/vl.py check  --project <your app folder>
python3 scripts/vl.py render --project <your app folder>
python3 scripts/vl.py shot   --project <your app folder>
```

The report lands on your Desktop (or Downloads).

## Privacy

Everything runs on your machine; nothing is sent anywhere. Secrets found in conversations or code are masked (`sk-proj-…wXyZ`) everywhere the tool writes, and the report refuses to be written if one slipped through. Working files live in `~/.vibe-ledger`, never inside your project.

Claude Code deletes conversations older than 30 days by default. vibe-ledger keeps a masked copy of each project's conversations and will offer — only with your agreement — to raise that limit.

## Limits

- Conversations: Claude Code and Codex only.
- Deterministic checks cover Next.js, Vite + React, Express, Supabase and Firebase. Other stacks are named in the report as not covered.
- It reads code; it does not run your app.

## Development

```
python3 -m pytest
python3 tests/e2e/prepare.py --out /tmp/vl-e2e   # fixture apps with planted problems
```

License: MIT.
````

- [ ] **Step 6: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_packaging.py tests/test_docs.py`
Expected: PASS.

- [ ] **Step 7: Commit**

```bash
git add .claude-plugin/plugin.json .claude-plugin/marketplace.json README.md LICENSE tests/test_packaging.py
git commit -m "chore: plugin manifests, README and license"
```

---

### Task 17: End-to-end run with a real agent, screenshots, cross-agent check

This task produces evidence, not new features. Fix whatever it uncovers in the module that owns the defect (with a regression test), then repeat the affected step.

**Files:**
- Modify: whichever module a defect is found in, plus its test file
- Create: nothing permanent outside `tests/`; all run output goes to the scratchpad

**Interfaces:**
- Consumes: everything above; `tests/e2e/prepare.py`, `tests/e2e/score.py`.
- Produces: per-fixture scores, screenshots that were opened and looked at, and a short written result for the user.

- [ ] **Step 1: Prepare the fixtures in a scratch folder**

Run: `python3 tests/e2e/prepare.py --out "$SCRATCH/e2e"` (where `$SCRATCH` is the session scratchpad directory). Set `export VIBE_LEDGER_HOME="$SCRATCH/vl-home" VIBE_LEDGER_OUT_DIR="$SCRATCH/vl-out" CLAUDE_CONFIG_DIR="$SCRATCH/claude-config"` so nothing touches the real `~/.claude`, `~/.codex` or Desktop.
Expected: five `start` commands printed.

- [ ] **Step 2: Run each fixture through the skill with a fresh agent**

For each fixture, dispatch one fresh general-purpose subagent with this prompt (fill in the placeholders):

```
You are using the vibe-ledger skill. Read <repo>/SKILL.md and follow it exactly for the app at <project>.
Use these environment variables for every command: VIBE_LEDGER_HOME=<...> VIBE_LEDGER_OUT_DIR=<...> CLAUDE_CONFIG_DIR=<...>.
Start with exactly this command: <the start command printed for this fixture>.
Do not ask the user about retention; answer "no" for this run. Stop after `check` and `render` succeed and report the report path and the counts.
```

Expected: each subagent ends with a report path and counts.

- [ ] **Step 3: Score each run**

Run, per fixture: `python3 tests/e2e/score.py --verified "$VIBE_LEDGER_HOME/projects/<id>/runs/<run>/ledger.verified.json" --answers tests/fixtures/answers/<name>.json` (the run path is in `latest_run.txt` under the project's workdir).
Expected: every line `PASS`. A `FAIL` means either the skill's guidance is unclear (fix `SKILL.md` / `references/`), a script is wrong (fix it with a test), or the agent did not follow the guidance — note which, fix, and rerun that fixture.

- [ ] **Step 4: Screenshot and look**

Run `vl.py shot --project <project>` for `notes-supabase`, `chat-express` and `clean-todos`. Open every PNG (desktop, dark, phone-390). Check by eye: four diagrams readable; no text overlapping or cut off; the counts in the header match the ledger; the phone view scrolls diagrams inside their boxes rather than overflowing the page; dark mode has readable contrast. Write down each problem seen and fix it in the renderer, then re-render and look again.

- [ ] **Step 5: Cross-agent check (Codex)**

Ask the user before running Codex (an autonomous `codex exec` run may be refused in auto mode). If they agree, run the same flow for `habits-firebase` with Codex, running only the commands the scripts print. If it is refused, give the user the exact command to run themselves. Record any step where the printed `NEXT:` command did not work as printed, and fix it.

- [ ] **Step 6: Run the full suite and commit fixes**

Run: `python3 -m pytest`
Expected: PASS.
Commit each fix separately, staging only the files it touched, e.g.:
```bash
git add scripts/ledger_report/map_svg.py tests/test_render_map_access.py
git commit -m "fix: map edge labels overlapped when two edges share a lane"
```

- [ ] **Step 7: Tell the user the results**

Report per fixture: PASS/FAIL lines from the scorer, what the screenshots showed, what was fixed, and anything still open. Attach the screenshot paths. Do not claim a fixture passes unless its scorer output says so.

---

### Task 18: Trial on one of the user's real projects (only with permission)

**Files:** none (findings feed back into Tasks 4–14 as fixes with tests).

- [ ] **Step 1: Ask the user** (AskUserQuestion) whether to run vibe-ledger on one of their own vibe-coded projects, and which one. Explain that it reads that project's Claude Code / Codex conversations locally and writes the report to the Desktop. Do not pick a project or read its conversations without a yes.

- [ ] **Step 2: If yes, run the skill end to end** on that project exactly as SKILL.md says (asking about retention when `start` suggests it), including `shot` and looking at the screenshots.

- [ ] **Step 3: Review the report with the user.** Ask whether they understood their app from it, and whether the diagrams — not just the text — carried that understanding (the spec's last acceptance criterion). Record what confused them.

- [ ] **Step 4: Turn each problem found into a fix with a test** (in the owning module), rerun the suite, and commit. Do not add the user's project or conversations to the repository as test data; build a synthetic fixture that reproduces the problem instead.
