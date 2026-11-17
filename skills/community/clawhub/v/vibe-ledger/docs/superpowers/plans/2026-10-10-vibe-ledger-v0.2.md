# vibe-ledger v0.2 Implementation Plan — file flowchart with click-to-explain

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the project's own file structure the main view: a layered, interactive file flowchart (dagre layout, colour cards with icons) where clicking a file shows its explanation — purpose, callers/callees, main functions, risks, history — with v0.1's report moved to an "Overview" tab.

**Architecture:** `scripts/graph.py` extracts a static file graph (imports, entries, notable externals, folders, scores) at `start` and writes `graph.json` + `explain_pack.md`. The agent writes `explain.json` for the top files; `scripts/explain.py` verifies it (functions really defined, backticked identifiers exist, history quotes real). `scripts/ledger_report/graph_page.py` builds masked page data; `assets/graph.js` lays it out with the vendored dagre and handles pan/zoom/select/panel; `render.py` wraps the graph tab and the v0.1 overview in one offline page.

**Tech Stack:** Python ≥ 3.11 stdlib; vendored `@dagrejs/dagre` 3.1.1 browser build (`dist/dagre.min.js`, 49 KB, MIT, global `dagre`, bundles graphlib); vanilla JS/CSS; pytest; headless Chrome for the layout check and screenshots.

**Spec:** `docs/superpowers/specs/2026-10-10-vibe-ledger-v0.2-file-graph-design.md` (builds on `docs/superpowers/specs/2026-10-09-vibe-ledger-design.md`).

## Global Constraints

- Everything from the v0.1 plan's Global Constraints still holds (stdlib only at runtime, no network, nothing written into the user's project, secrets masked everywhere, runnable `NEXT:` lines, stage named paths, never push).
- Graph files: `.js .jsx .ts .tsx .mjs .cjs .vue .svelte .py`; tests (`test/ tests/ __tests__/ spec/ fixtures/`, `*.test.* *.spec.*`) and config files (`*.config.*`, `.eslintrc*`, `.prettierrc*`, `jest.setup.*`, `setupTests.*`) are excluded and counted.
- Constants: folder collapse above **80** file nodes; at most **30** files get an AI explanation; explanation chunks of **8** files; function line tolerance **±3**; dev-view code snippets at most **8** lines.
- Node kinds/icons (style B): entry ▶ blue, logic ƒ slate, data ⛁ green, paid ✦ amber, folder ▤ stone. Selected node purple; others dimmed to opacity ≈0.28 (edges ≈0.18).
- Layout A: graph ≈63 % left, panel ≈37 % right; below 760 px wide, stacked (graph ≈55 vh on top).
- Page data is one `<script type="application/json" id="vl-data">` block; all strings masked before serialisation; `</` escaped as `<\/`; panel and node text written with `textContent` only.
- The vendored dagre file is inlined unchanged except its trailing `sourceMappingURL` comment; `LICENSE-dagre` ships next to it.

## Review Focus

1. **Monorepo-ish layouts and path aliases** — a Next.js app whose imports all use `@/` with a `tsconfig.json` that has comments and trailing commas. Expected: aliases still resolve (JSONC tolerated). Test: `test_tsconfig_with_comments_and_trailing_commas` (Task 1).
2. **TypeScript ESM convention** — `import x from "./util.js"` where only `util.ts` exists. Expected: resolves to `util.ts`. Test: `test_js_extension_import_resolves_to_ts_source` (Task 1).
3. **Hundreds of files** — a 150-file project. Expected: folders collapse at a level that splits into ≥ 3 groups, page stays usable. Test: `test_large_project_collapses_into_folders` (Task 2).
4. **Model-written explanation naming functions that do not exist or are only methods** — expected: invented names dropped with a reason, class methods and object methods recognised. Tests: `test_definitions_cover_common_forms`, `test_invented_function_is_dropped` (Task 3).
5. **Strings that break the page** — a quote or purpose containing `</script>` or a secret. Expected: page intact, secret masked. Test: `test_page_data_masks_secrets_and_escapes_script_close` (Task 4).

## File Structure

```
scripts/graph.py                         file graph: discovery, imports, resolution, entries, externals, exports, folders, scores, explain pack (Tasks 1–2)
scripts/explain.py                       explain.json format check, definitions finder, verification, merge (Task 3)
scripts/ledger_report/vendor/dagre.min.js + LICENSE-dagre   vendored dagre 3.1.1 browser build (Task 4)
scripts/ledger_report/graph_page.py      page data (risks attached, cards, summaries, snippets) + graph-tab HTML (Task 4)
scripts/ledger_report/i18n.py            + graph-tab strings (Task 4)
scripts/ledger_report/assets/graph.js    layout, drawing, pan/zoom/pinch, select, panel, search, folders, URL params (Task 5)
scripts/ledger_report/assets/graph.css   graph + panel styles, mobile stacking, dark mode (Task 5)
scripts/render.py                        tabbed page: graph tab + overview (v0.1 body) (Task 5)
scripts/shot.py                          + DOM layout check (Task 5), selected-file and overview shots (Task 6)
scripts/vl.py                            start/merge/check/render/shot changes (Task 6)
SKILL.md, references/explain-guide.md    explanation workflow (Task 7)
tests/test_graph_imports.py  tests/test_graph_build.py  tests/test_explain.py
tests/test_graph_page.py  tests/test_graph_render.py  tests/test_cli_v02.py  tests/test_e2e_medium.py
tests/helpers/graph_fixture.py           three-file project shared by the page and render tests (Task 4)
tests/e2e/medium.py                      generated 100-file project for the folder-collapse checks (Task 8)
tests/e2e/score.py                       + graph and explanation scores (Task 7)
tests/fixtures/answers/*.json            + "graph" expectations (Task 7)
tests/test_e2e_deterministic.py          + graph checks (Task 7)
```

`graph.json` shape (produced by `graph.build`, read by everything after it):
```jsonc
{"nodes": [{"id": "src/ai/client.js", "label": "client.js", "folder": "src/ai", "role": "entry|logic", "lines": 120,
            "exports": [{"name": "run", "line": 4}], "score": 7, "explain": true,
            "edits": {"count": 3, "first": "2026-09-12T09:00:00Z", "last": "2026-09-13T10:00:00Z"} | null}],
 "externals": [{"id": "ext:openai", "label": "OpenAI API", "kind": "paid|data",
                "evidence": [{"path": "src/ai/client.js", "line": 7, "snippet": "…"}]}],
 "edges": [{"from": "src/a.js", "to": "src/b.js" | "ext:openai", "line": 3, "names": ["run"]}],
 "entries": [{"path": "src/main.js", "reason": "index.html script"}],
 "folders": [{"id": "src/ai", "files": ["src/ai/a.js", "src/ai/b.js"]}],
 "collapsed": false, "unresolved": [{"from": "src/x.ts", "spec": "@/missing", "line": 4}],
 "excluded": {"tests": 2, "config": 1}, "languages": ["js"]}
```

`explain.json` shape (written by the agent, verified by `explain.verify`):
```jsonc
{"evidence": {"H1": {"kind": "transcript", "session": "s1", "msg_id": "m1", "quote": "…"}},
 "files": {"src/ai/client.js": {"purpose_plain": "…", "purpose_dev": "…",
                                "functions": [{"name": "run", "line": 4, "plain": "…"}],
                                "history": [{"plain": "…", "evidence": ["H1"]}]}}}
```

**Spec interpretation recorded here:** the explanation ranking runs at `start`, before the agent writes `ledger.json`, so its "risk" points come from probe findings (certain +3, hint +1). Ledger statuses still colour the nodes at render time (spec §4.4).

**More spec interpretations:**
- §3.3's Next.js row applies only to a Next.js project (`package.json` depends on `next`, or a `next.config.*` exists); otherwise a Vite app's `src/pages/` files would all count as entry points.
- §3.4's invisible sink for outside services is replaced by a fixed right-hand column (`graph.js` places externals after dagre runs, ordered by where their callers sit). Same picture, and the column stays straight when folders expand.
- §7 lists four screenshots; `shot` also takes `overview.png`, because the v0.1 diagrams now live in the Overview tab and still need looking at.

---
### Task 1: `graph.py` — files, imports and path resolution

**Files:**
- Create: `scripts/graph.py`
- Test: `tests/test_graph_imports.py`

**Interfaces:**
- Consumes: `common.iter_files`, `common.read_text`, `common.rel`, `common.is_within` (v0.1).
- Produces:
  - Constants `JS_EXTS`, `PY_EXT`, `RESOLVE_EXTS`, `TEST_FILE`, `CONFIG_FILE` (compiled regexes), `FOLDER_THRESHOLD = 80`, `EXPLAIN_MAX = 30`, `EXPLAIN_CHUNK = 8`.
  - `graph.collect_files(root) -> tuple[dict[str, Path], Counter]` — graph files keyed by POSIX path relative to root; counter of excluded `tests` / `config`.
  - `graph.strip_comments(text, lang) -> str` — comments blanked to spaces, newlines kept (line numbers survive); `lang` is `"js"` or `"py"`.
  - `graph.js_imports(text) -> list[tuple[str, int, list[str]]]` — (specifier, 1-based line, imported names), comments ignored.
  - `graph.py_imports(text) -> list[tuple[str, str, int, list[str]]]` — (leading dots, module, line, imported names).
  - `graph.load_aliases(root) -> list[tuple[str, list[str], bool]]` — (prefix, target dirs/files relative to root, is_wildcard), longest prefix first; reads `tsconfig.json` then `jsconfig.json` (JSONC tolerated).
  - `graph.resolve_js(spec, src, root, aliases) -> tuple[str, str | None]` — `("file", relpath)`, `("missing", None)` for an unresolvable local specifier, or `("package", spec)`.
  - `graph.resolve_py(dots, module, src, root) -> tuple[str, str | None]` — same three outcomes.

- [ ] **Step 1: Write the failing tests**

`tests/test_graph_imports.py`:
```python
import graph


def write(root, rel, text=""):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


JS = '''import React from "react";
import {
  runA,
  runB as other,
} from "./ai/client";
import "./styles.css";
export { helper } from "../shared/helper.js";
export * from "./types";
// import ghost from "./ghost";
/* import alsoGhost from "./ghost2"; */
const lazy = import("./lazy");
const fs = require("fs");
const local = require("./local.cjs");
export const notAnImport = "from here";
'''


def test_es_cjs_dynamic_and_reexport_imports():
    got = graph.js_imports(JS)
    specs = [(s, line) for s, line, _ in got]
    assert specs == [("react", 1), ("./ai/client", 2), ("./styles.css", 6), ("../shared/helper.js", 7),
                     ("./types", 8), ("./lazy", 11), ("fs", 12), ("./local.cjs", 13)]
    names = dict((s, n) for s, _, n in got)
    assert names["./ai/client"] == ["runA", "runB", "other"] and names["react"] == ["React"]


def test_comment_blanking_keeps_line_numbers():
    text = "/* a\nb */\nimport x from './x';\n"
    assert graph.js_imports(text) == [("./x", 3, ["x"])]
    assert graph.strip_comments(text, "js").count("\n") == text.count("\n")


def test_python_imports():
    text = "import os, app.db\nfrom . import views, models\nfrom ..core.auth import login  # comment\n# import ghost\nfrom flask import Flask\n"
    assert graph.py_imports(text) == [
        ("", "os", 1, []), ("", "app.db", 1, []), (".", "", 2, ["views", "models"]),
        ("..", "core.auth", 3, ["login"]), ("", "flask", 5, ["Flask"])]


def test_relative_index_and_extension_resolution(tmp_path):
    write(tmp_path, "src/ai/client.ts")
    write(tmp_path, "src/ui/index.tsx")
    write(tmp_path, "src/app.ts")
    assert graph.resolve_js("./ai/client", "src/app.ts", tmp_path, []) == ("file", "src/ai/client.ts")
    assert graph.resolve_js("./ui", "src/app.ts", tmp_path, []) == ("file", "src/ui/index.tsx")
    assert graph.resolve_js("./nope", "src/app.ts", tmp_path, []) == ("missing", None)
    assert graph.resolve_js("react", "src/app.ts", tmp_path, []) == ("package", "react")
    assert graph.resolve_js("@supabase/supabase-js", "src/app.ts", tmp_path, []) == ("package", "@supabase/supabase-js")


def test_js_extension_import_resolves_to_ts_source(tmp_path):
    write(tmp_path, "src/util.ts")
    assert graph.resolve_js("./util.js", "src/main.ts", tmp_path, []) == ("file", "src/util.ts")


def test_tsconfig_with_comments_and_trailing_commas(tmp_path):
    write(tmp_path, "tsconfig.json", '''{
      // editor settings
      "compilerOptions": {
        "baseUrl": ".",
        /* aliases */
        "paths": { "@lib/*": ["./src/lib/*"], "@cfg": ["./src/config.ts"], },
        "url": "http://example.com/not-a-comment",
      },
    }''')
    write(tmp_path, "src/lib/db.ts")
    write(tmp_path, "src/config.ts")
    aliases = graph.load_aliases(tmp_path)
    assert ("@lib/", ["src/lib"], True) in aliases and ("@cfg", ["src/config.ts"], False) in aliases
    assert graph.resolve_js("@lib/db", "src/app.ts", tmp_path, aliases) == ("file", "src/lib/db.ts")
    assert graph.resolve_js("@cfg", "src/app.ts", tmp_path, aliases) == ("file", "src/config.ts")


def test_at_alias_falls_back_to_src_then_root_and_vite_absolute(tmp_path):
    write(tmp_path, "src/lib/a.ts")
    write(tmp_path, "lib/b.ts")
    assert graph.resolve_js("@/lib/a", "app/page.tsx", tmp_path, []) == ("file", "src/lib/a.ts")
    assert graph.resolve_js("@/lib/b", "app/page.tsx", tmp_path, []) == ("file", "lib/b.ts")
    assert graph.resolve_js("~/lib/b", "app/page.tsx", tmp_path, []) == ("file", "lib/b.ts")
    assert graph.resolve_js("/src/lib/a.ts", "index.html", tmp_path, []) == ("file", "src/lib/a.ts")


def test_resolution_never_leaves_the_project(tmp_path):
    root = tmp_path / "app"
    write(root, "src/a.ts")
    write(tmp_path, "outside.ts")
    assert graph.resolve_js("../../outside", "src/a.ts", root, []) == ("missing", None)


def test_resolve_py_relative_and_absolute(tmp_path):
    write(tmp_path, "app/__init__.py")
    write(tmp_path, "app/views.py")
    write(tmp_path, "app/core/auth.py")
    write(tmp_path, "app/api/routes.py")
    assert graph.resolve_py(".", "missing_mod", "app/views.py", tmp_path) == ("missing", None)
    assert graph.resolve_py("..", "core.auth", "app/api/routes.py", tmp_path) == ("file", "app/core/auth.py")
    assert graph.resolve_py("", "app.views", "main.py", tmp_path) == ("file", "app/views.py")
    assert graph.resolve_py("", "app", "main.py", tmp_path) == ("file", "app/__init__.py")
    assert graph.resolve_py("", "flask", "main.py", tmp_path) == ("package", "flask")


def test_collect_files_excludes_tests_and_config(tmp_path):
    for rel in ("src/a.ts", "src/b.test.ts", "tests/c.py", "vite.config.ts", "src/__tests__/d.js",
                "src/styles.css", "node_modules/x/index.js", "app/main.py"):
        write(tmp_path, rel)
    files, excluded = graph.collect_files(tmp_path)
    assert sorted(files) == ["app/main.py", "src/a.ts"]
    assert excluded == {"tests": 3, "config": 1}
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_graph_imports.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'graph'`.

- [ ] **Step 3: Write `scripts/graph.py` (part 1)**

```python
"""The project's file graph: which files import which, where the app starts, and
which notable outside services and data stores the code reaches.

Everything here is static text analysis; nothing is executed."""
from __future__ import annotations

import json
import os
import re
from collections import Counter
from pathlib import Path, PurePosixPath

from common import is_within, iter_files, read_text, rel

JS_EXTS = (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".vue", ".svelte")
PY_EXT = ".py"
RESOLVE_EXTS = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue", ".svelte")
TEST_FILE = re.compile(r"(?:^|/)(?:tests?|__tests__|spec|fixtures?)/|\.(?:test|spec)\.[a-z]+$")
CONFIG_FILE = re.compile(r"(?:^|/)(?:[^/]+\.config\.[a-z]+|\.eslintrc[^/]*|\.prettierrc[^/]*|jest\.setup\.[a-z]+"
                         r"|setupTests\.[a-z]+)$")
FOLDER_THRESHOLD = 80
EXPLAIN_MAX = 30
EXPLAIN_CHUNK = 8

_BLOCK_COMMENT = re.compile(r"/\*.*?\*/", re.S)
_JS_LINE_COMMENT = re.compile(r"^[ \t]*//[^\n]*", re.M)
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


def strip_comments(text: str, lang: str) -> str:
    if lang == "py":
        return _PY_LINE_COMMENT.sub(_blank, text)
    return _JS_LINE_COMMENT.sub(_blank, _BLOCK_COMMENT.sub(_blank, text))


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


def collect_files(root) -> tuple[dict[str, Path], Counter]:
    root = Path(root).resolve()
    files: dict[str, Path] = {}
    excluded: Counter = Counter()
    for p in iter_files(root, set(JS_EXTS) | {PY_EXT}):
        r = rel(p, root)
        if TEST_FILE.search(r):
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


def load_aliases(root) -> list[tuple[str, list[str], bool]]:
    root = Path(root)
    for name in ("tsconfig.json", "jsconfig.json"):
        p = root / name
        if not p.is_file():
            continue
        try:
            cfg = json.loads(_strip_jsonc(read_text(p)))
        except json.JSONDecodeError:
            continue
        opts = cfg.get("compilerOptions") or {} if isinstance(cfg, dict) else {}
        base = opts.get("baseUrl") or "."
        out = []
        for key, targets in (opts.get("paths") or {}).items():
            wild = key.endswith("*")
            prefix = key[:-1] if wild else key
            outs = [_norm(str(PurePosixPath(base) / (t[:-1] if t.endswith("*") else t))) for t in targets or []]
            out.append((prefix, outs, wild))
        return sorted(out, key=lambda a: -len(a[0]))
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
    for top in (root, root / "src"):
        target = top.joinpath(*parts)
        for cand in (target.with_suffix(".py"), target / "__init__.py"):
            if cand.is_file():
                return "file", rel(cand, root)
    return "package", module
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_graph_imports.py`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/graph.py tests/test_graph_imports.py
git commit -m "feat(graph): collect files, extract JS/Python imports, resolve paths and aliases"
```

---
### Task 2: `graph.py` — entries, externals, exports, folders, scores, explain pack

**Files:**
- Modify: `scripts/graph.py` (append)
- Test: `tests/test_graph_build.py`

**Interfaces:**
- Consumes: everything Task 1 produced in `graph.py`; digest records (v0.1: `kind`, `files`, `ts`); `probes.json` findings (`path`, `level`, `message`, `line`).
- Produces:
  - `EXT_PACKAGES`, `PY_PACKAGES` (package root → `(key, label, kind)`), `EXT_URLS`, `STORAGE_APIS` (list of `(regex, (key, label, kind))`); kinds are `"paid"` or `"data"`.
  - `graph.exports(text, lang) -> list[{"name", "line"}]`
  - `graph.find_entries(root, files, texts=None) -> dict[str, str]` (path → reason; rule order: Next.js (only when `package.json` depends on `next` or a `next.config.*` exists), manifest, index.html, package.json, `.listen(`, Python)
  - `graph.edits_from_digest(recs, root) -> dict[str, {"count", "first", "last"}]`
  - `graph.folder_groups(paths) -> list[{"id", "files"}]`
  - `graph.build(root, recs, probes) -> dict` — the `graph.json` shape in File Structure.
  - `graph.explain_pack(g, root, probes) -> str` — markdown handed to the agent.

- [ ] **Step 1: Write the failing tests**

`tests/test_graph_build.py`:
```python
import json

import graph

NO_PROBES = {"findings": []}


def write(root, rel, text=""):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")
    return p


def test_entries_for_each_stack(tmp_path):
    write(tmp_path, "app/page.tsx", "export default function P() {}")
    write(tmp_path, "app/api/chat/route.ts", "export async function POST() {}")
    write(tmp_path, "pages/_app.tsx")
    write(tmp_path, "pages/about.tsx")
    write(tmp_path, "manifest.json", json.dumps({
        "manifest_version": 3, "background": {"service_worker": "src/background.js"},
        "content_scripts": [{"js": ["src/content.js"]}], "side_panel": {"default_path": "src/panel/panel.html"}}))
    write(tmp_path, "src/background.js")
    write(tmp_path, "src/content.js")
    write(tmp_path, "src/panel/panel.html", '<script type="module" src="panel.js"></script>')
    write(tmp_path, "src/panel/panel.js")
    write(tmp_path, "index.html", '<script type="module" src="/src/main.ts"></script><script src="https://cdn.example/x.js"></script>')
    write(tmp_path, "src/main.ts")
    write(tmp_path, "package.json", json.dumps({"main": "./server/index.js", "bin": {"tool": "bin/cli.js"},
                                                "dependencies": {"next": "15.0.0"}}))
    write(tmp_path, "server/index.js", "app.listen(3000);")
    write(tmp_path, "bin/cli.js")
    write(tmp_path, "worker.js", "server.listen(8080);")
    write(tmp_path, "tools/run.py", 'if __name__ == "__main__":\n    main()\n')
    write(tmp_path, "app.py")
    files, _ = graph.collect_files(tmp_path)
    entries = graph.find_entries(tmp_path, files)
    assert set(entries) == {"app/page.tsx", "app/api/chat/route.ts", "pages/about.tsx", "src/background.js",
                            "src/content.js", "src/panel/panel.js", "src/main.ts", "server/index.js", "bin/cli.js",
                            "worker.js", "tools/run.py", "app.py"}
    assert entries["src/panel/panel.js"] == "manifest side panel → src/panel/panel.html"
    assert entries["server/index.js"] == "package.json main"
    assert entries["worker.js"] == "starts a server (.listen)"


def test_pages_folder_is_ordinary_code_outside_nextjs(tmp_path):
    write(tmp_path, "index.html", '<script type="module" src="/src/main.tsx"></script>')
    write(tmp_path, "src/main.tsx", 'import "./pages/home";\n')
    write(tmp_path, "src/pages/home.tsx", "export default function Home() {}\n")
    write(tmp_path, "app/page.tsx", "export default function P() {}\n")
    write(tmp_path, "package.json", json.dumps({"dependencies": {"react": "18.3.1"}}))
    files, _ = graph.collect_files(tmp_path)
    assert graph.find_entries(tmp_path, files) == {"src/main.tsx": "index.html script"}
    write(tmp_path, "next.config.mjs", "export default {};\n")
    assert set(graph.find_entries(tmp_path, files)) == {"src/main.tsx", "src/pages/home.tsx", "app/page.tsx"}


def test_build_edges_unresolved_and_fallback_entries(tmp_path):
    write(tmp_path, "src/a.ts", 'import { run } from "./b";\nimport x from "./missing";\n')
    write(tmp_path, "src/b.ts", "export function run() {}\n")
    g = graph.build(tmp_path, [], NO_PROBES)
    assert g["edges"] == [{"from": "src/a.ts", "to": "src/b.ts", "line": 1, "names": ["run"]}]
    assert g["unresolved"] == [{"from": "src/a.ts", "spec": "./missing", "line": 2}]
    assert g["entries"] == [{"path": "src/a.ts", "reason": "not imported by any file"}]
    nodes = {n["id"]: n for n in g["nodes"]}
    assert nodes["src/a.ts"]["role"] == "entry" and nodes["src/b.ts"]["role"] == "logic"
    assert nodes["src/b.ts"]["exports"] == [{"name": "run", "line": 1}]
    assert g["languages"] == ["js"] and g["collapsed"] is False


def test_import_cycles_are_kept_and_self_imports_dropped(tmp_path):
    write(tmp_path, "src/a.ts", 'import { b } from "./b";\nexport const a = 1;\n')
    write(tmp_path, "src/b.ts", 'import { a } from "./a";\nexport const b = 2;\n')
    write(tmp_path, "src/self.ts", 'import "./self";\n')
    g = graph.build(tmp_path, [], NO_PROBES)
    assert {(e["from"], e["to"]) for e in g["edges"]} == {("src/a.ts", "src/b.ts"), ("src/b.ts", "src/a.ts")}
    assert g["entries"] == [{"path": "src/self.ts", "reason": "not imported by any file"}]


def test_externals_from_packages_urls_and_storage(tmp_path):
    write(tmp_path, "src/ai.ts", 'import OpenAI from "openai";\nimport { createClient } from "@supabase/supabase-js";\n'
                                 'import _ from "lodash";\nconst r = await fetch("https://api.anthropic.com/v1/messages");\n'
                                 'localStorage.setItem("k", "v");\nimport { getApp } from "firebase/app";\n')
    write(tmp_path, "src/db.py", "import sqlite3\nimport requests\n")
    g = graph.build(tmp_path, [], NO_PROBES)
    ext = {e["id"]: e for e in g["externals"]}
    assert set(ext) == {"ext:openai", "ext:supabase", "ext:anthropic", "ext:local-storage", "ext:firebase", "ext:sqlite"}
    assert ext["ext:openai"]["kind"] == "paid" and ext["ext:supabase"]["kind"] == "data"
    assert ext["ext:anthropic"]["evidence"] == [
        {"path": "src/ai.ts", "line": 4, "snippet": 'const r = await fetch("https://api.anthropic.com/v1/messages");'}]
    edges = {(e["from"], e["to"]) for e in g["edges"]}
    assert ("src/ai.ts", "ext:openai") in edges and ("src/db.py", "ext:sqlite") in edges
    assert all(not e["to"].startswith("ext:lodash") for e in g["edges"])


def test_exports_js_and_python():
    js = ("export default function Home() {}\nexport async function load() {}\nexport const API = 1;\n"
          "export class Store {}\nconst a = 1, b = 2;\nexport { a, b as bee };\nexports.legacy = () => 1;\n"
          "module.exports = { one, two };\nexport { helper } from './helper';\n")
    assert [(e["name"], e["line"]) for e in graph.exports(js, "js")] == [
        ("Home", 1), ("load", 2), ("API", 3), ("Store", 4), ("a", 6), ("bee", 6), ("legacy", 7), ("one", 8), ("two", 8)]
    py = "def run():\n    pass\nclass Store:\n    def method(self): pass\ndef _private(): pass\nasync def fetch(): pass\n"
    assert [(e["name"], e["line"]) for e in graph.exports(py, "py")] == [("run", 1), ("Store", 3), ("fetch", 6)]


def test_large_project_collapses_into_folders(tmp_path):
    for d in ("src/ai", "src/ui", "src/db", "src/util"):
        for i in range(40):
            write(tmp_path, f"{d}/f{i}.ts")
    write(tmp_path, "src/main.ts")
    g = graph.build(tmp_path, [], NO_PROBES)
    assert g["collapsed"] is True
    assert [f["id"] for f in g["folders"]] == ["src/ai", "src/db", "src/ui", "src/util"]
    assert all(len(f["files"]) == 40 for f in g["folders"])
    assert "src/main.ts" not in {x for f in g["folders"] for x in f["files"]}


def test_folder_groups_skip_single_file_groups():
    paths = ["a/x.ts", "a/y.ts", "b/z.ts", "c/w.ts", "c/v.ts", "root.ts"]
    assert graph.folder_groups(paths) == [{"id": "a", "files": ["a/x.ts", "a/y.ts"]},
                                          {"id": "c", "files": ["c/v.ts", "c/w.ts"]}]


def test_scores_and_explain_selection(tmp_path):
    write(tmp_path, "index.html", '<script type="module" src="/src/main.ts"></script>')
    write(tmp_path, "src/main.ts", 'import "./ai";\nimport "./util";\n')
    write(tmp_path, "src/ai.ts", 'import OpenAI from "openai";\nimport "./util";\n')
    write(tmp_path, "src/util.ts")
    write(tmp_path, "src/lonely.ts")
    probes = {"findings": [{"path": "src/ai.ts", "level": "certain", "message": "m", "line": 1},
                           {"path": "src/util.ts", "level": "hint", "message": "m", "line": 1}]}
    recs = [{"kind": "edit", "files": [str(tmp_path / "src/util.ts")], "ts": f"2026-09-12T09:0{i}:00Z"} for i in range(6)]
    g = graph.build(tmp_path, recs, probes)
    nodes = {n["id"]: n for n in g["nodes"]}
    assert {k: v["score"] for k, v in nodes.items()} == {"src/main.ts": 3, "src/ai.ts": 6, "src/util.ts": 5, "src/lonely.ts": 0}
    assert {k for k, v in nodes.items() if v["explain"]} == {"src/main.ts", "src/ai.ts", "src/util.ts"}
    assert nodes["src/util.ts"]["edits"] == {"count": 6, "first": "2026-09-12T09:00:00Z", "last": "2026-09-12T09:05:00Z"}
    assert nodes["src/lonely.ts"]["edits"] is None


def test_explain_pack_lists_files_and_groups(tmp_path):
    write(tmp_path, "src/main.ts", "".join(f'import "./m{i}";\n' for i in range(10)))
    for i in range(10):
        write(tmp_path, f"src/m{i}.ts", f"export function f{i}() {{}}\n")
    g = graph.build(tmp_path, [], NO_PROBES)
    pack = graph.explain_pack(g, tmp_path, NO_PROBES)
    assert "## Group 2 → parts/explain_02.json" in pack and "### src/main.ts" in pack
    assert "- exports: f3 (line 1)" in pack and "- used by: src/main.ts" in pack
    write(tmp_path / "small", "main.ts", 'import "./a";\n')
    write(tmp_path / "small", "a.ts", "export const a = 1;\n")
    small = graph.build(tmp_path / "small", [], NO_PROBES)
    assert "Group" not in graph.explain_pack(small, tmp_path / "small", NO_PROBES)
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_graph_build.py`
Expected: FAIL — `AttributeError: module 'graph' has no attribute 'find_entries'` (and the others).

- [ ] **Step 3: Append to `scripts/graph.py`**

Add `from collections import Counter, defaultdict` to the imports (replacing the `Counter`-only import).

```python
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
        if f.endswith(JS_EXTS) and LISTEN.search(texts[f]):
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
    """Group by the shallowest folder depth that splits the files into at least 3 groups;
    files above that depth, and groups of one file, stay as single nodes."""
    dirs = {p: PurePosixPath(p).parent.parts for p in paths}
    for depth in range(1, max((len(d) for d in dirs.values()), default=0) + 1):
        groups: dict[str, list[str]] = defaultdict(list)
        for p, parts in dirs.items():
            if len(parts) >= depth:
                groups["/".join(parts[:depth])].append(p)
        if len(groups) >= 3:
            return [{"id": k, "files": sorted(v)} for k, v in sorted(groups.items()) if len(v) >= 2]
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
    aliases = load_aliases(root)
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
                kind, target = resolve_js(spec, f, root, aliases)
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
                      "score": score, "explain": False, "edits": edits.get(f)})
    for n in sorted((n for n in nodes if n["score"] > 0), key=lambda n: (-n["score"], n["id"]))[:EXPLAIN_MAX]:
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
    return "\n".join(lines) + "\n"
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_graph_imports.py tests/test_graph_build.py`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/graph.py tests/test_graph_build.py
git commit -m "feat(graph): entries, notable externals, exports, folder collapse, scores and explain pack"
```

---
### Task 3: `explain.py` — format check, definitions, verification, merge

**Files:**
- Create: `scripts/explain.py`
- Test: `tests/test_explain.py`

**Interfaces:**
- Consumes: `graph.strip_comments`, `graph.build` (Tasks 1–2); `verify.check_transcript(e, index)` (v0.1); `common.read_text`.
- Produces:
  - `explain.TOLERANCE = 3`
  - `explain.ExplainError(problems)` with `.problems`
  - `explain.validate(doc) -> None`
  - `explain.find_definitions(text, lang) -> dict[str, list[int]]` — name → 1-based definition lines.
  - `explain.verify(doc, g, root, index) -> dict` — `explain.verified.json`: `evidence` (each with `ok`/`reason`/`ts`…), `files` (kept entries with `ok`, verified `functions` each carrying `line_corrected`, `dropped_functions`, `purpose_unverified`, `missing_identifiers`, verified `history`), `rejected` (`path`, `reason`), `verification` counts.
  - `explain.merge(parts) -> dict` — evidence ids prefixed `p<N>_`; first explanation of a path wins, later duplicates listed in `duplicates`.
  - `explain.summary_lines(verified) -> list[str]`

- [ ] **Step 1: Write the failing tests**

`tests/test_explain.py`:
```python
import pytest

import explain
import graph

CLIENT = '''import OpenAI from "openai";

export async function runAnthropic(request) {
  return fetch(request.url);
}

const runOpenAi = async (request) => {
  return request;
};

function helper() {}
const shared = function () {};
const tiny = x => x;

export default class Client {
  static create() {}
  async send(payload) {
    if (payload) {
      return payload;
    }
  }
}

const api = {
  ping() { return 1; },
  pong: async () => 2,
  pang: function () { return 3; },
};
'''
PY = "class Store:\n    def save(self):\n        pass\n\nasync def fetch_all():\n    pass\n\ndef run():\n    pass\n"


def test_definitions_cover_common_forms():
    defs = explain.find_definitions(CLIENT, "js")
    for name, line in (("runAnthropic", 3), ("runOpenAi", 7), ("helper", 11), ("shared", 12), ("tiny", 13),
                       ("Client", 15), ("create", 16), ("send", 17), ("ping", 25), ("pong", 26), ("pang", 27)):
        assert defs.get(name) == [line], (name, defs.get(name))
    assert "if" not in defs and "return" not in defs and "fetch" not in defs
    py = explain.find_definitions(PY, "py")
    assert py == {"Store": [1], "save": [2], "fetch_all": [5], "run": [8]}


@pytest.fixture
def project(tmp_path):
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "client.js").write_text(CLIENT, encoding="utf-8")
    (tmp_path / "src" / "main.js").write_text('import { runAnthropic } from "./client";\n', encoding="utf-8")
    g = graph.build(tmp_path, [], {"findings": []})
    index = {"m1": {"id": "m1", "session": "s1", "ts": "2026-09-12T09:00:00Z", "role": "user", "kind": "text",
                    "text": "AI 总结要调用 Anthropic，不要让陌生人随便用"}}
    return tmp_path, g, index


def doc(**entry):
    base = {"purpose_plain": "负责调用 AI 服务商。", "purpose_dev": "Wraps `runAnthropic`.", "functions": [], "history": []}
    base.update(entry)
    return {"evidence": {"H1": {"kind": "transcript", "session": "s1", "msg_id": "m1", "quote": "AI 总结要调用 Anthropic"},
                         "H2": {"kind": "transcript", "session": "s1", "msg_id": "m1", "quote": "我编的一句话"}},
            "files": {"src/client.js": base}}


def test_functions_are_checked_corrected_or_dropped(project):
    root, g, index = project
    out = explain.verify(doc(functions=[{"name": "runAnthropic", "line": 4, "plain": "a"},
                                        {"name": "send", "line": 40, "plain": "b"},
                                        {"name": "deleteEverything", "line": 3, "plain": "c"}]), g, root, index)
    f = out["files"]["src/client.js"]
    assert [(x["name"], x["line"], x["line_corrected"]) for x in f["functions"]] == [("runAnthropic", 3, False), ("send", 17, True)]
    assert f["dropped_functions"] == [{"name": "deleteEverything", "reason": "not defined in this file"}]
    assert out["verification"]["functions_dropped"] == 1


def test_invented_function_is_dropped(project):
    root, g, index = project
    out = explain.verify(doc(functions=[{"name": "stealKeys", "line": 1, "plain": "x"}]), g, root, index)
    assert out["files"]["src/client.js"]["functions"] == []


def test_backticked_identifiers_must_exist(project):
    root, g, index = project
    good = explain.verify(doc(purpose_plain="调用 `runAnthropic()`，被 `main.js` 使用，见 `npm run dev`。"), g, root, index)
    assert good["files"]["src/client.js"]["purpose_unverified"] is False
    bad = explain.verify(doc(purpose_dev="Uses `secretVault` and `ghost.ts`."), g, root, index)
    f = bad["files"]["src/client.js"]
    assert f["purpose_unverified"] is True and f["missing_identifiers"] == ["ghost.ts", "secretVault"]


def test_history_keeps_only_verified_quotes(project):
    root, g, index = project
    out = explain.verify(doc(history=[{"plain": "用户要求", "evidence": ["H1"]},
                                      {"plain": "编的", "evidence": ["H2"]}]), g, root, index)
    assert [h["plain"] for h in out["files"]["src/client.js"]["history"]] == ["用户要求"]
    assert out["evidence"]["H1"]["ok"] and not out["evidence"]["H2"]["ok"]


def test_paths_outside_the_graph_are_rejected(project):
    root, g, index = project
    d = doc()
    d["files"]["src/nope.js"] = d["files"].pop("src/client.js")
    out = explain.verify(d, g, root, index)
    assert out["files"] == {} and out["rejected"] == [{"path": "src/nope.js", "reason": "not a file in the graph"}]


@pytest.mark.parametrize("mutate, needle", [
    (lambda d: d["files"]["src/client.js"].pop("purpose_plain"), "purpose_plain"),
    (lambda d: d["files"]["src/client.js"].update(functions=[{"name": "x", "line": "3", "plain": "p"}]), "line"),
    (lambda d: d["files"]["src/client.js"].update(history=[{"plain": "p", "evidence": ["H9"]}]), "H9"),
    (lambda d: d["evidence"].update(H3={"kind": "code"}), "transcript"),
    (lambda d: d.update(files=[]), "files"),
])
def test_validate_lists_problems(mutate, needle):
    d = doc()
    mutate(d)
    with pytest.raises(explain.ExplainError) as exc:
        explain.validate(d)
    assert any(needle in p for p in exc.value.problems), exc.value.problems


def test_merge_prefixes_evidence_and_keeps_first_duplicate():
    a, b = doc(), doc()
    b["files"]["src/other.js"] = dict(b["files"]["src/client.js"], history=[{"plain": "h", "evidence": ["H1"]}])
    out = explain.merge([a, b])
    assert set(out["evidence"]) == {"p1_H1", "p1_H2", "p2_H1", "p2_H2"}
    assert out["files"]["src/other.js"]["history"][0]["evidence"] == ["p2_H1"]
    assert out["duplicates"] == ["src/client.js"]
    explain.validate(out)


def test_summary_lines(project):
    root, g, index = project
    out = explain.verify(doc(functions=[{"name": "ghost", "line": 1, "plain": "x"}]), g, root, index)
    text = "\n".join(explain.summary_lines(out))
    assert "1 files kept" in text and "ghost" in text
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_explain.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'explain'`.

- [ ] **Step 3: Write `scripts/explain.py`**

```python
"""explain.json: the agent's per-file explanations, checked against the code.

Function names must really be defined in the file, backticked identifiers in a
purpose must exist in the project, and history quotes must be in the conversations."""
from __future__ import annotations

import copy
import re
from pathlib import Path

from common import read_text
from graph import strip_comments
from verify import check_transcript

TOLERANCE = 3
_ID = r"[A-Za-z_$][\w$]*"
JS_DEFS = [
    re.compile(rf"^[ \t]*(?:export[ \t]+)?(?:default[ \t]+)?(?:async[ \t]+)?function\b[ \t]*\*?[ \t]*({_ID})", re.M),
    re.compile(rf"^[ \t]*(?:export[ \t]+)?(?:const|let|var)[ \t]+({_ID})[ \t]*=[ \t]*(?:async[ \t]*)?"
               rf"(?:function\b|\([^)]*\)[ \t]*=>|{_ID}[ \t]*=>)", re.M),
    re.compile(rf"^[ \t]*(?:export[ \t]+)?(?:default[ \t]+)?(?:abstract[ \t]+)?class[ \t]+({_ID})", re.M),
    re.compile(rf"^[ \t]*(?:static[ \t]+)?(?:async[ \t]+)?\*?[ \t]*({_ID})[ \t]*\([^)\n]*\)[ \t]*\{{", re.M),
    re.compile(rf"^[ \t]*({_ID})[ \t]*:[ \t]*(?:async[ \t]*)?(?:function\b|\([^)]*\)[ \t]*=>|{_ID}[ \t]*=>)", re.M),
]
PY_DEFS = [re.compile(r"^[ \t]*(?:async[ \t]+)?def[ \t]+([A-Za-z_]\w*)[ \t]*\(", re.M),
           re.compile(r"^[ \t]*class[ \t]+([A-Za-z_]\w*)", re.M)]
NOT_A_DEFINITION = {"if", "for", "while", "switch", "catch", "function", "return", "with", "else", "do", "try"}
BACKTICK = re.compile(r"`([^`\n]+)`")
IDENT_TOKEN = re.compile(rf"^{_ID}(?:\.{_ID})*$")
FILE_TOKEN = re.compile(r"^[\w./-]+\.(?:js|jsx|ts|tsx|mjs|cjs|vue|svelte|py|json|html|css)$")


class ExplainError(Exception):
    def __init__(self, problems: list[str]):
        super().__init__("\n".join(problems))
        self.problems = problems


def validate(doc) -> None:
    if not isinstance(doc, dict):
        raise ExplainError(["explain.json must be a JSON object"])
    p: list[str] = []
    ev = doc.get("evidence", {})
    if not isinstance(ev, dict):
        p.append("evidence: must be an object")
        ev = {}
    for eid, e in ev.items():
        if not isinstance(e, dict) or e.get("kind") != "transcript":
            p.append(f"evidence {eid}: kind must be transcript")
            continue
        for f in ("session", "msg_id", "quote"):
            if f not in e:
                p.append(f"evidence {eid}: missing {f}")
    files = doc.get("files")
    if not isinstance(files, dict):
        raise ExplainError(p + ["files: must be an object mapping file paths to explanations"])
    for path, entry in files.items():
        where = f"file {path}"
        if not isinstance(entry, dict):
            p.append(f"{where}: must be an object")
            continue
        if not isinstance(entry.get("purpose_plain"), str) or not entry.get("purpose_plain", "").strip():
            p.append(f"{where}: purpose_plain must be a non-empty string")
        if not isinstance(entry.get("purpose_dev", ""), str):
            p.append(f"{where}: purpose_dev must be a string")
        for fn in entry.get("functions", []):
            if not isinstance(fn, dict) or not isinstance(fn.get("name"), str) or not isinstance(fn.get("plain"), str):
                p.append(f"{where}: each function needs a name and a plain sentence")
            elif not isinstance(fn.get("line"), int):
                p.append(f"{where} function {fn['name']}: line must be an integer")
        for h in entry.get("history", []):
            if not isinstance(h, dict) or not isinstance(h.get("plain"), str) or not isinstance(h.get("evidence"), list):
                p.append(f"{where}: each history item needs plain and an evidence list")
                continue
            for i in h["evidence"]:
                if i not in ev:
                    p.append(f"{where} history: unknown evidence id {i}")
    if p:
        raise ExplainError(p)


def find_definitions(text: str, lang: str) -> dict[str, list[int]]:
    clean = strip_comments(text, lang)
    found: dict[str, set] = {}
    for rx in (PY_DEFS if lang == "py" else JS_DEFS):
        for m in rx.finditer(clean):
            name = m.group(1)
            if name in NOT_A_DEFINITION:
                continue
            found.setdefault(name, set()).add(clean.count("\n", 0, m.start(1)) + 1)
    return {name: sorted(lines) for name, lines in found.items()}


def _identifiers(text: str):
    for raw in BACKTICK.findall(text or ""):
        tok = raw.strip()
        tok = tok[:-2] if tok.endswith("()") else tok
        if FILE_TOKEN.match(tok):
            yield ("file", tok)
        elif IDENT_TOKEN.match(tok):
            yield ("ident", tok)
        # anything else (a command, a phrase) is not a name to check


def _exists(kind: str, tok: str, corpus: str, paths: set, labels: set) -> bool:
    if kind == "file":
        return tok in paths or tok in labels or any(p.endswith("/" + tok) for p in paths)
    return re.search(r"(?<![\w$])" + re.escape(tok) + r"(?![\w$])", corpus) is not None


def verify(doc: dict, g: dict, root, index: dict) -> dict:
    validate(doc)
    root = Path(root).resolve()
    out = copy.deepcopy(doc)
    out.setdefault("evidence", {})
    for e in out["evidence"].values():
        e.update(check_transcript(e, index))
    paths = {n["id"] for n in g["nodes"]}
    labels = {n["label"] for n in g["nodes"]}
    corpus = "\n".join(read_text(root / p) for p in sorted(paths))
    files, rejected = {}, []
    for path, entry in out["files"].items():
        if path not in paths:
            rejected.append({"path": path, "reason": "not a file in the graph"})
            continue
        defs = find_definitions(read_text(root / path), "py" if path.endswith(".py") else "js")
        kept, dropped = [], []
        for fn in entry.get("functions", []):
            lines = defs.get(fn["name"], [])
            near = [n for n in lines if abs(n - fn["line"]) <= TOLERANCE]
            if near:
                kept.append({**fn, "line": min(near, key=lambda n: abs(n - fn["line"])), "line_corrected": False})
            elif len(lines) == 1:
                kept.append({**fn, "line": lines[0], "line_corrected": True})
            elif lines:
                dropped.append({"name": fn["name"], "reason": f"defined {len(lines)} times in the file and none is "
                                                              f"within {TOLERANCE} lines of line {fn['line']}"})
            else:
                dropped.append({"name": fn["name"], "reason": "not defined in this file"})
        missing = sorted({tok for text in (entry.get("purpose_plain", ""), entry.get("purpose_dev", ""))
                          for kind, tok in _identifiers(text) if not _exists(kind, tok, corpus, paths, labels)})
        history = []
        for h in entry.get("history", []):
            ok_ids = [i for i in h["evidence"] if out["evidence"].get(i, {}).get("ok")]
            if ok_ids:
                history.append({**h, "evidence": ok_ids})
        files[path] = {**entry, "ok": True, "functions": kept, "dropped_functions": dropped,
                       "purpose_unverified": bool(missing), "missing_identifiers": missing, "history": history}
    out["files"] = files
    out["rejected"] = rejected
    out["verification"] = {
        "files": len(files), "rejected": len(rejected),
        "functions_dropped": sum(len(f["dropped_functions"]) for f in files.values()),
        "unverified_purposes": sum(1 for f in files.values() if f["purpose_unverified"]),
        "evidence_failed": [{"id": k, "reason": e.get("reason", "")} for k, e in out["evidence"].items() if not e.get("ok")],
    }
    return out


def merge(parts: list[dict]) -> dict:
    out: dict = {"evidence": {}, "files": {}, "duplicates": []}
    for n, part in enumerate(parts, 1):
        validate(part)
        pre = f"p{n}_"
        for eid, e in part.get("evidence", {}).items():
            out["evidence"][pre + eid] = copy.deepcopy(e)
        for path, entry in part["files"].items():
            if path in out["files"]:
                out["duplicates"].append(path)
                continue
            e = copy.deepcopy(entry)
            e["history"] = [{**h, "evidence": [pre + i for i in h["evidence"]]} for h in e.get("history", [])]
            out["files"][path] = e
    validate(out)
    return out


def summary_lines(verified: dict) -> list[str]:
    v = verified["verification"]
    lines = [f"Explanations: {v['files']} files kept, {v['rejected']} rejected"]
    lines += [f"  ✗ {r['path']}: {r['reason']}" for r in verified["rejected"]]
    lines.append(f"Functions dropped: {v['functions_dropped']}")
    for path, f in verified["files"].items():
        lines += [f"  - {path}: {d['name']} — {d['reason']}" for d in f["dropped_functions"]][:20]
    lines.append(f"Purposes marked unverified: {v['unverified_purposes']}")
    for path, f in verified["files"].items():
        if f["purpose_unverified"]:
            lines.append(f"  - {path}: not found in the project: {', '.join(f['missing_identifiers'])}")
    lines += [f"  ✗ evidence {x['id']}: {x['reason']}" for x in v["evidence_failed"]]
    return lines
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_explain.py`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add scripts/explain.py tests/test_explain.py
git commit -m "feat(explain): verify per-file explanations against definitions, identifiers and quotes"
```

---
### Task 4: Vendored dagre, graph-tab strings, page data

**Files:**
- Create: `scripts/ledger_report/vendor/dagre.min.js`, `scripts/ledger_report/vendor/LICENSE-dagre`
- Create: `scripts/ledger_report/graph_page.py`
- Modify: `scripts/ledger_report/i18n.py` (add the `g_*` keys in both languages)
- Create: `tests/helpers/graph_fixture.py` (a three-file project shared with Task 5's tests)
- Test: `tests/test_graph_page.py`

**Interfaces:**
- Consumes: `graph.build` output (Tasks 1–2); `explain.verify` output (Task 3); v0.1 verified ledger and `probes.json`; `redact.redact`; `ledger_report.bits.{GLYPH, fit, width, h, fmt_date}`; `ledger_report.i18n.{t, STR}`.
- Produces:
  - `graph_page.VENDOR_DIR` (Path of the vendor folder) and `graph_page.dagre_source() -> str` (the minified file without its `sourceMappingURL` line).
  - `graph_page.page_data(g, explained, ledger, probes, root, lang, has_transcripts) -> dict` with keys `lang`, `strings` (every `g_*` string for that language), `nodes` (`id`, `label` (full name), `short` (label fitted to 22 width units for the card), `sub` (fitted to 28 units), `role` ∈ entry/logic/data/paid, `state` ∈ ok/warn/bad, `badge`, `folder`, `card`), `edges` (`from`, `to`, `names`, `risky`), `folders` (`id`, `files`, `state`, `badge`, `label`, `short`, `sub`), `collapsed`, `summary`, `howto` (3 strings), `top` (≤ 3 file ids), `entries` (ids), `coverage` (`excluded`, `unresolved`, `rejected`, `dropped` — what the flowchart and the panel leave out, for the overview's last section).
  - `graph_page.data_script(data) -> str` — `<script type="application/json" id="vl-data">…</script>`, every string masked, `</` written as `<\/`.
  - `graph_page.render_graph_tab(lang) -> str` — the static skeleton (`#vlg`, `#vlg-svg`, `#vlg-viewport`, tool buttons with `data-act`, legend, `#vlg-panel`).
  - `tests/helpers/graph_fixture.py`: `OPENAI` (a fake key built by concatenation), `write(root, rel, text="")`, and `make_project(root, purpose="把文字发给 OpenAI 总结。") -> (root, g, explained, ledger, probes)` — `app/page.tsx → lib/ai.ts → OpenAI` plus a lone `lib/util.ts`.

- [ ] **Step 1: Vendor dagre 3.1.1 (MIT)**

Run (from the repo root; the scratch folder is outside the repo):
```bash
SCR=$(mktemp -d) && (cd "$SCR" && npm pack @dagrejs/dagre@3.1.1 --silent && tar xzf dagrejs-dagre-3.1.1.tgz)
mkdir -p scripts/ledger_report/vendor
cp "$SCR/package/dist/dagre.min.js" scripts/ledger_report/vendor/dagre.min.js
{ cat "$SCR/package/LICENSE"; echo; echo "--- bundled licences (dist/dagre.min.js.LEGAL.txt) ---"; cat "$SCR/package/dist/dagre.min.js.LEGAL.txt"; } > scripts/ledger_report/vendor/LICENSE-dagre
head -c 40 scripts/ledger_report/vendor/dagre.min.js; echo; wc -c scripts/ledger_report/vendor/dagre.min.js
```
Expected: the file starts with `"use strict";var dagre=(()=>{` and is about 49 KB; `LICENSE-dagre` starts with the MIT text (Copyright (c) 2012-2014 Chris Pettitt).

- [ ] **Step 2: Add the graph-tab strings to `scripts/ledger_report/i18n.py`**

Insert into the `"zh"` dict:
```python
        "g_tab_graph": "文件流程图", "g_tab_overview": "总览", "g_search": "搜索文件…",
        "g_zoom_in": "放大", "g_zoom_out": "缩小", "g_fit": "适应窗口",
        "g_expand_all": "全部展开", "g_collapse_all": "全部折叠",
        "g_band_entry": "入口 / 界面", "g_band_logic": "逻辑", "g_band_data": "数据与外部",
        "g_role_entry": "入口", "g_role_logic": "逻辑", "g_role_data": "数据", "g_role_paid": "付费服务", "g_role_folder": "文件夹",
        "g_legend_bad": "红框 = 有问题", "g_legend_warn": "黄框 = 只有提示", "g_legend_paid": "✦ = 按次收费",
        "g_legend_folder": "虚线框 = 折叠的文件夹",
        "g_badge_bad": "{n} 个问题", "g_badge_warn": "{n} 个提示",
        "g_summary": "{files} 个文件，{entries} 个入口，连到 {ext} 个外部服务（其中 {paid} 个按次收费）。",
        "g_howto_1": "从左往右读：入口 → 逻辑 → 数据与外部，箭头表示“谁调用谁”。",
        "g_howto_2": "点一个文件，右边会讲它是干什么的；它的上下游保持清晰，其余变淡。",
        "g_howto_3": "红框是有问题的文件，黄框是只有提示的文件。",
        "g_top": "问题最多的文件", "g_no_problems": "没有发现有问题的文件。",
        "g_calls": "它调用 →", "g_called_by": "谁调用它 ←", "g_functions": "主要函数", "g_exports": "对外提供",
        "g_risks": "风险与问题", "g_no_risks": "检查脚本没在这个文件里发现问题", "g_promises": "相关承诺",
        "g_history": "来历", "g_no_history_tx": "没有对话记录", "g_no_history": "对话里没找到和这个文件有关的记录",
        "g_edits": "对话里改过 {count} 次（{first} 至 {last}）",
        "g_no_explain": "暂无详细讲解，下面是自动摘要。", "g_unverified": "未核实：{ids} 在项目里找不到",
        "g_auto_entry": "这是一个入口文件（{reason}）。", "g_auto_exports": "对外提供 {n} 个名字：{names}。",
        "g_auto_noexports": "没有对外提供函数。", "g_auto_used": "被 {n} 个文件使用。",
        "g_auto_external": "{label}：项目里有 {n} 个文件连到它。",
        "g_folder_files": "{n} 个文件 · 点开展开", "g_folder_members": "包含的文件", "g_collapse": "收起这个文件夹",
        "g_lines": "{n} 行", "g_in_overview": "在总览里看", "g_where": "代码位置", "g_close": "关闭",
        "g_compromise": "报错后的妥协", "g_dev_snippet": "代码片段",
        "g_no_files": "这个项目里没有找到 JS/TS 或 Python 文件，所以流程图是空的。",
        "g_merged": "{n} 条引用",
        "cov_graph_excluded": "流程图没有画 {tests} 个测试文件和 {config} 个配置文件",
        "cov_unresolved": "{n} 个本地引用找不到对应的文件，流程图里没有这些线：",
        "cov_explain_dropped": "{n} 处文件讲解没通过核对，已从面板里去掉：",
```
Insert into the `"en"` dict:
```python
        "g_tab_graph": "File flowchart", "g_tab_overview": "Overview", "g_search": "Search files…",
        "g_zoom_in": "Zoom in", "g_zoom_out": "Zoom out", "g_fit": "Fit",
        "g_expand_all": "Expand all", "g_collapse_all": "Collapse all",
        "g_band_entry": "Entry / UI", "g_band_logic": "Logic", "g_band_data": "Data & outside",
        "g_role_entry": "Entry", "g_role_logic": "Logic", "g_role_data": "Data", "g_role_paid": "Paid service", "g_role_folder": "Folder",
        "g_legend_bad": "red = has problems", "g_legend_warn": "amber = hints only", "g_legend_paid": "✦ = charges per use",
        "g_legend_folder": "dashed = collapsed folder",
        "g_badge_bad": "{n} problems", "g_badge_warn": "{n} hints",
        "g_summary": "{files} files, {entries} entry points, reaching {ext} outside services ({paid} charge per use).",
        "g_howto_1": "Read left to right: entry → logic → data & outside; an arrow means \"calls\".",
        "g_howto_2": "Click a file to read what it does; its callers and callees stay sharp, the rest fades.",
        "g_howto_3": "Red cards have problems, amber cards have hints only.",
        "g_top": "Files with the most problems", "g_no_problems": "No file has problems.",
        "g_calls": "Calls →", "g_called_by": "Called by ←", "g_functions": "Main functions", "g_exports": "Provides",
        "g_risks": "Risks", "g_no_risks": "The checks found nothing in this file", "g_promises": "Related promises",
        "g_history": "History", "g_no_history_tx": "No conversations were found", "g_no_history": "No conversation touched this file",
        "g_edits": "Changed {count} times in the conversations ({first} to {last})",
        "g_no_explain": "No detailed explanation yet; this is the automatic summary.", "g_unverified": "Unverified: {ids} not found in the project",
        "g_auto_entry": "This is an entry point ({reason}).", "g_auto_exports": "Provides {n} names: {names}.",
        "g_auto_noexports": "Provides no functions.", "g_auto_used": "Used by {n} files.",
        "g_auto_external": "{label}: {n} files in the project reach it.",
        "g_folder_files": "{n} files · click to open", "g_folder_members": "Files inside", "g_collapse": "Collapse this folder",
        "g_lines": "{n} lines", "g_in_overview": "See in Overview", "g_where": "Where in the code", "g_close": "Close",
        "g_compromise": "Workaround after an error", "g_dev_snippet": "Code",
        "g_no_files": "No JS/TS or Python files were found in this project, so the flowchart is empty.",
        "g_merged": "{n} imports",
        "cov_graph_excluded": "The flowchart leaves out {tests} test files and {config} config files",
        "cov_unresolved": "{n} local imports point at no file, so the flowchart has no line for them:",
        "cov_explain_dropped": "{n} parts of the file explanations failed the checks and were left out of the panel:",
```

- [ ] **Step 3: Write the failing tests**

`tests/helpers/graph_fixture.py`:
```python
"""A three-file project with one paid service: app/page.tsx -> lib/ai.ts -> OpenAI, plus a lone lib/util.ts."""
import graph

OPENAI = "sk-proj-" + "Ab3dE5fG7hJ9kL1mN3pQ5rS7tU9vW1xY"


def write(root, rel, text=""):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def make_project(root, purpose="把文字发给 OpenAI 总结。"):
    write(root, "app/page.tsx", 'import { summarize } from "../lib/ai";\nexport default function Page() {}\n')
    write(root, "lib/ai.ts", 'import OpenAI from "openai";\nexport async function summarize(t) {\n  return t;\n}\n')
    write(root, "lib/util.ts", "export const x = 1;\n")
    write(root, "package.json", '{"dependencies": {"next": "15.0.0", "openai": "4.60.0"}}\n')
    g = graph.build(root, [], {"findings": []})
    ledger = {"evidence": {
                  "E1": {"kind": "code", "path": "lib/ai.ts", "line": 2, "snippet": "export async function summarize(t) {", "ok": True},
                  "Q1": {"kind": "transcript", "ok": True, "ts": "2026-09-12T09:00:00Z", "role": "user",
                         "quote": "不要让陌生人花我的钱", "msg_id": "m", "session": "s"}},
              "promises": [{"id": "P1", "type": "user_requirement", "question": "what_costs", "plain": "不要让陌生人花我的钱",
                            "source": ["Q1"], "status": "broken", "verdict_plain": "v", "verdict_dev": "d", "evidence": ["E1"]}],
              "compromises": [], "map": {"nodes": [], "edges": []}, "access": {"resources": []}, "paths": []}
    probes = {"findings": [{"id": "secrets_exposed:lib/util.ts:1", "probe": "secrets_exposed", "level": "hint",
                            "path": "lib/util.ts", "line": 1, "snippet": "export const x = 1;", "message": "A thing", "implies": []}]}
    explained = {"evidence": {}, "rejected": [], "files": {"lib/ai.ts": {
        "purpose_plain": purpose, "purpose_dev": "dev", "ok": True, "dropped_functions": [], "purpose_unverified": False,
        "missing_identifiers": [], "history": [], "functions": [{"name": "summarize", "line": 2, "plain": "发请求", "line_corrected": False}]}}}
    return root, g, explained, ledger, probes
```

`tests/test_graph_page.py`:
```python
import json
import re

from helpers.graph_fixture import OPENAI, make_project, write
from ledger_report import graph_page, i18n
from ledger_report.bits import width


def setup(tmp_path, purpose="把文字发给 OpenAI 总结。"):
    root, g, explained, ledger, probes = make_project(tmp_path, purpose=purpose)
    return graph_page.page_data(g, explained, ledger, probes, root, "zh", True)


def test_nodes_roles_states_badges_and_edges(tmp_path):
    data = setup(tmp_path)
    nodes = {n["id"]: n for n in data["nodes"]}
    assert set(nodes) == {"app/page.tsx", "lib/ai.ts", "lib/util.ts", "ext:openai"}
    assert nodes["ext:openai"]["role"] == "paid" and nodes["lib/ai.ts"]["role"] == "logic"
    assert nodes["lib/ai.ts"]["state"] == "bad" and nodes["lib/ai.ts"]["badge"] == "1 个问题"
    assert nodes["lib/util.ts"]["state"] == "warn" and nodes["lib/util.ts"]["badge"] == "1 个提示"
    assert nodes["app/page.tsx"]["state"] == "ok" and nodes["app/page.tsx"]["badge"] == ""
    edges = {(e["from"], e["to"]): e for e in data["edges"]}
    assert edges[("app/page.tsx", "lib/ai.ts")]["risky"] is True and edges[("app/page.tsx", "lib/ai.ts")]["names"] == ["summarize"]
    assert data["summary"] == "3 个文件，1 个入口，连到 1 个外部服务（其中 1 个按次收费）。"  # app/page.tsx is a Next.js entry
    assert data["top"] == ["lib/ai.ts", "lib/util.ts"] and len(data["howto"]) == 3
    assert data["strings"]["g_tab_graph"] == "文件流程图"


def test_explained_and_automatic_cards(tmp_path):
    data = setup(tmp_path)
    cards = {n["id"]: n["card"] for n in data["nodes"]}
    ai = cards["lib/ai.ts"]
    assert ai["explained"] and ai["purpose_plain"] == "把文字发给 OpenAI 总结。"
    assert [f["name"] for f in ai["functions"]] == ["summarize"]
    assert ai["snippets"][0]["code"].startswith("export async function summarize(t) {")
    assert ai["promises"] == [{"id": "P1", "status": "broken", "glyph": "❌", "plain": "不要让陌生人花我的钱"}]
    assert ai["risks"][0]["level"] == "bad" and ai["called_by"] == ["app/page.tsx"] and ai["calls"] == ["ext:openai"]
    util = cards["lib/util.ts"]
    assert not util["explained"] and "对外提供 1 个名字：x。" in util["auto"]
    ext = cards["ext:openai"]
    assert "OpenAI API：项目里有 1 个文件连到它。" == ext["auto"] and ext["evidence"][0]["where"] == "lib/ai.ts:1"
    assert ai["history_note"] == "对话里没找到和这个文件有关的记录"


def test_page_data_masks_secrets_and_escapes_script_close(tmp_path):
    data = setup(tmp_path, purpose=f"注意 </script><b>x</b> 密钥 {OPENAI}")
    script = graph_page.data_script(data)
    assert OPENAI not in script and "</script><b>" not in script and "<\\/script>" in script
    inner = re.search(r'<script type="application/json" id="vl-data">(.*)</script>$', script, re.S).group(1)
    back = json.loads(inner)
    purpose = {n["id"]: n for n in back["nodes"]}["lib/ai.ts"]["card"]["purpose_plain"]
    assert purpose.startswith("注意 </script><b>x</b>") and "sk-proj-…" in purpose


def test_card_text_is_fitted_but_full_text_is_kept(tmp_path):
    write(tmp_path, "components/SubscriptionCheckoutConfirmationDialog.tsx", "export const a = 1;\n")
    data = setup(tmp_path, purpose="这个文件负责把用户输入的长文本切成小段，再逐段发给模型总结")
    nodes = {n["id"]: n for n in data["nodes"]}
    long = nodes["components/SubscriptionCheckoutConfirmationDialog.tsx"]
    assert long["label"] == "SubscriptionCheckoutConfirmationDialog.tsx"
    assert long["short"].endswith("…") and width(long["short"]) <= graph_page.LABEL_UNITS
    ai = nodes["lib/ai.ts"]
    assert ai["short"] == "ai.ts" and ai["sub"].endswith("…") and width(ai["sub"]) <= graph_page.SUB_UNITS
    assert ai["card"]["purpose_plain"].endswith("总结")  # the panel keeps the whole sentence


def test_coverage_lists_what_the_flowchart_left_out(tmp_path):
    root, g, explained, ledger, probes = make_project(tmp_path)
    g["unresolved"] = [{"from": "lib/ai.ts", "spec": "./gone", "line": 9}]
    g["excluded"] = {"tests": 2, "config": 1}
    explained["rejected"] = [{"path": "lib/nope.ts", "reason": "not a file in the graph"}]
    explained["files"]["lib/ai.ts"]["dropped_functions"] = [{"name": "sendEmail", "reason": "not defined in this file"}]
    cov = graph_page.page_data(g, explained, ledger, probes, root, "zh", True)["coverage"]
    assert cov["excluded"] == {"tests": 2, "config": 1} and cov["unresolved"][0]["spec"] == "./gone"
    assert cov["rejected"] == [{"path": "lib/nope.ts", "reason": "not a file in the graph"}]
    assert cov["dropped"] == [{"path": "lib/ai.ts", "name": "sendEmail", "reason": "not defined in this file"}]


def test_render_graph_tab_skeleton():
    html = graph_page.render_graph_tab("zh")
    for needle in ('id="vlg-svg"', 'id="vlg-viewport"', 'id="vlg-panel"', 'data-act="fit"', "红框 = 有问题", "✦ = 按次收费"):
        assert needle in html


def test_dagre_source_is_vendored_and_stripped():
    src = graph_page.dagre_source()
    assert src.startswith('"use strict";var dagre=') and "sourceMappingURL" not in src
    assert (graph_page.VENDOR_DIR / "LICENSE-dagre").read_text(encoding="utf-8").startswith("Copyright")


def test_graph_strings_exist_in_both_languages():
    zh = {k for k in i18n.STR["zh"] if k.startswith("g_")}
    en = {k for k in i18n.STR["en"] if k.startswith("g_")}
    assert zh == en and len(zh) >= 50
```

- [ ] **Step 4: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_graph_page.py`
Expected: FAIL — `ImportError: cannot import name 'graph_page'` (the string test may already pass after Step 2).

- [ ] **Step 5: Write `scripts/ledger_report/graph_page.py`**

```python
"""The file-flowchart tab: page data (masked) and the static skeleton graph.js fills."""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from common import read_text
from ledger_report.bits import GLYPH, fit, fmt_date, h
from ledger_report.i18n import STR, t
from redact import redact

VENDOR_DIR = Path(__file__).resolve().parent / "vendor"
SNIPPET_LINES = 8
LABEL_UNITS = 22  # what fits on a 236 px card at 14 px bold
SUB_UNITS = 28  # the same card's second line at 11.5 px
BAD_STATUSES = ("broken",)
WARN_STATUSES = ("partial", "pending")


def dagre_source() -> str:
    text = (VENDOR_DIR / "dagre.min.js").read_text(encoding="utf-8")
    return "\n".join(line for line in text.splitlines() if "sourceMappingURL" not in line)


def _mask(value):
    if isinstance(value, str):
        return redact(value)
    if isinstance(value, list):
        return [_mask(v) for v in value]
    if isinstance(value, dict):
        return {k: _mask(v) for k, v in value.items()}
    return value


def data_script(data: dict) -> str:
    payload = json.dumps(_mask(data), ensure_ascii=False).replace("</", "<\\/")
    return f'<script type="application/json" id="vl-data">{payload}</script>'


def _evidence_paths(ids, evidence) -> set:
    return {evidence[i]["path"] for i in ids if evidence.get(i, {}).get("ok")
            and evidence[i].get("kind") in ("code", "probe") and evidence[i].get("path")}


def _file_risks(ledger: dict, probes: dict, lang: str) -> tuple[dict, dict]:
    risks: dict[str, list] = defaultdict(list)
    promises: dict[str, list] = defaultdict(list)
    for f in probes.get("findings", []):
        if f.get("level") in ("certain", "hint"):
            risks[f["path"]].append({"level": "bad" if f["level"] == "certain" else "warn",
                                     "text": f.get("message", ""), "where": f"{f['path']}:{f.get('line', '')}"})
    ev = ledger.get("evidence", {})
    for p in ledger.get("promises", []):
        for path in _evidence_paths(p.get("evidence", []), ev):
            promises[path].append({"id": p["id"], "status": p["status"], "glyph": GLYPH[p["status"]], "plain": p["plain"]})
            if p["status"] in BAD_STATUSES or p["status"] in WARN_STATUSES:
                risks[path].append({"level": "bad" if p["status"] in BAD_STATUSES else "warn",
                                    "text": f"{GLYPH[p['status']]} {p['plain']}", "where": path})
    for c in ledger.get("compromises", []):
        if c.get("still_present") is True:
            for path in _evidence_paths(c.get("now", []), ev):
                risks[path].append({"level": "bad", "text": f"{t(lang, 'g_compromise')}: {c.get('bypassed', '')}", "where": path})
    return risks, promises


def _state(items) -> tuple[str, int, int]:
    bad = sum(1 for r in items if r["level"] == "bad")
    warn = sum(1 for r in items if r["level"] == "warn")
    return ("bad" if bad else "warn" if warn else "ok"), bad, warn


def _badge(lang, state, bad, warn) -> str:
    if state == "bad":
        return t(lang, "g_badge_bad", n=bad)
    if state == "warn":
        return t(lang, "g_badge_warn", n=warn)
    return ""


def _snippets(root: Path, path: str, functions) -> list[dict]:
    lines = read_text(root / path).splitlines()
    return [{"name": f["name"], "line": f["line"],
             "code": "\n".join(lines[f["line"] - 1:f["line"] - 1 + SNIPPET_LINES])} for f in functions]


def page_data(g: dict, explained: dict, ledger: dict, probes: dict, root, lang: str, has_transcripts: bool) -> dict:
    root = Path(root).resolve()
    risks, promises = _file_risks(ledger, probes, lang)
    calls, called_by = defaultdict(list), defaultdict(list)
    for e in g["edges"]:
        calls[e["from"]].append(e["to"])
        called_by[e["to"]].append(e["from"])
    entry_reason = {e["path"]: e["reason"] for e in g["entries"]}
    exp_files = explained.get("files", {})
    exp_evidence = explained.get("evidence", {})
    nodes, state_of = [], {}
    for n in g["nodes"]:
        fid = n["id"]
        state, bad, warn = _state(risks.get(fid, []))
        state_of[fid] = state
        exp = exp_files.get(fid)
        names = ", ".join(x["name"] for x in n["exports"][:5])
        auto = (t(lang, "g_auto_entry", reason=entry_reason[fid]) if fid in entry_reason else "")
        auto += (t(lang, "g_auto_exports", n=len(n["exports"]), names=names) if n["exports"] else t(lang, "g_auto_noexports"))
        auto += t(lang, "g_auto_used", n=len(called_by[fid]))
        history = []
        for item in (exp or {}).get("history", []):
            e = exp_evidence.get(item["evidence"][0], {})
            history.append({"plain": item["plain"], "date": fmt_date(e.get("ts")), "quote": e.get("quote", "")})
        edits = n.get("edits")
        card = {
            "path": fid, "label": n["label"], "folder": n["folder"], "role": n["role"],
            "role_label": t(lang, "g_role_" + n["role"]), "lines": t(lang, "g_lines", n=n["lines"]),
            "explained": exp is not None,
            "purpose_plain": exp["purpose_plain"] if exp else "", "purpose_dev": exp.get("purpose_dev", "") if exp else "",
            "purpose_unverified": bool(exp and exp.get("purpose_unverified")),
            "unverified_note": t(lang, "g_unverified", ids=", ".join(exp["missing_identifiers"]))
            if exp and exp.get("purpose_unverified") else "",
            "auto": auto, "calls": calls[fid], "called_by": called_by[fid],
            "functions": [{"name": f["name"], "line": f["line"], "plain": f["plain"]} for f in (exp or {}).get("functions", [])],
            "exports": n["exports"], "risks": risks.get(fid, []), "promises": promises.get(fid, []),
            "history": history,
            "history_note": "" if history else (t(lang, "g_no_history") if has_transcripts else t(lang, "g_no_history_tx")),
            "edits": t(lang, "g_edits", count=edits["count"], first=fmt_date(edits["first"])[:10],
                       last=fmt_date(edits["last"])[:10]) if edits else "",
            "snippets": _snippets(root, fid, (exp or {}).get("functions", [])),
        }
        sub = (exp["purpose_plain"] if exp else n["folder"] or "")
        nodes.append({"id": fid, "label": n["label"], "short": fit(n["label"], LABEL_UNITS), "sub": fit(sub, SUB_UNITS),
                      "role": n["role"], "state": state,
                      "badge": _badge(lang, state, bad, warn), "folder": n["folder"], "card": card})
    for x in g["externals"]:
        users = called_by[x["id"]]
        card = {"path": x["id"], "label": x["label"], "folder": "", "role": x["kind"],
                "role_label": t(lang, "g_role_" + x["kind"]), "auto": t(lang, "g_auto_external", label=x["label"], n=len(users)),
                "called_by": users, "calls": [], "evidence": [{"where": f"{e['path']}:{e['line']}", "code": e["snippet"]}
                                                              for e in x["evidence"]]}
        nodes.append({"id": x["id"], "label": x["label"], "short": fit(x["label"], LABEL_UNITS),
                      "sub": t(lang, "g_role_" + x["kind"]), "role": x["kind"],
                      "state": "ok", "badge": "", "folder": "", "card": card})
    folders = []
    for f in g.get("folders", []):
        state, bad, warn = _state([r for fid in f["files"] for r in risks.get(fid, [])])
        folders.append({"id": f["id"], "files": f["files"], "state": state, "badge": _badge(lang, state, bad, warn),
                        "label": f["id"], "short": fit(f["id"].rsplit("/", 1)[-1], LABEL_UNITS - 2) + " ▸",
                        "sub": t(lang, "g_folder_files", n=len(f["files"]))})
    edges = [{"from": e["from"], "to": e["to"], "names": e["names"],
              "risky": state_of.get(e["from"]) == "bad" or state_of.get(e["to"]) == "bad"} for e in g["edges"]]
    ranked = sorted((n for n in nodes if n["state"] != "ok" and not n["id"].startswith("ext:")),
                    key=lambda n: (-sum(r["level"] == "bad" for r in n["card"]["risks"]),
                                   -sum(r["level"] == "warn" for r in n["card"]["risks"]), n["id"]))
    paid = sum(1 for x in g["externals"] if x["kind"] == "paid")
    return {"lang": lang, "strings": {k: v for k, v in STR.get(lang, STR["en"]).items() if k.startswith("g_")},
            "nodes": nodes, "edges": edges, "folders": folders, "collapsed": bool(g.get("collapsed")),
            "entries": [e["path"] for e in g["entries"]],
            "summary": t(lang, "g_summary", files=len(g["nodes"]), entries=len(g["entries"]), ext=len(g["externals"]), paid=paid),
            "howto": [t(lang, "g_howto_1"), t(lang, "g_howto_2"), t(lang, "g_howto_3")],
            "top": [n["id"] for n in ranked[:3]],
            "coverage": {"excluded": g.get("excluded", {}), "unresolved": g.get("unresolved", []),
                         "rejected": explained.get("rejected", []),
                         "dropped": [{"path": p, "name": d["name"], "reason": d["reason"]}
                                     for p, f in sorted(exp_files.items()) for d in f.get("dropped_functions", [])]}}


def render_graph_tab(lang: str) -> str:
    legend = "".join(f'<span class="vlg-legend-item k-{k}">{h(t(lang, key))}</span>'
                     for k, key in (("bad", "g_legend_bad"), ("warn", "g_legend_warn"), ("paid", "g_legend_paid"),
                                    ("folder", "g_legend_folder")))
    tools = "".join(f'<button type="button" data-act="{act}" title="{h(t(lang, key))}">{label}</button>'
                    for act, key, label in (("zoom-in", "g_zoom_in", "+"), ("zoom-out", "g_zoom_out", "−"),
                                            ("fit", "g_fit", h(t(lang, "g_fit")))))
    folder_tools = "".join(f'<button type="button" data-act="{act}" hidden>{h(t(lang, key))}</button>'
                           for act, key in (("expand-all", "g_expand_all"), ("collapse-all", "g_collapse_all")))
    return ('<div class="vlg" id="vlg"><div class="vlg-canvas" id="vlg-canvas">'
            '<svg id="vlg-svg" xmlns="http://www.w3.org/2000/svg" role="img"><g id="vlg-viewport"></g></svg>'
            f'<div class="vlg-tools">{tools}{folder_tools}</div><div class="vlg-legend">{legend}</div></div>'
            '<aside class="vlg-panel" id="vlg-panel" aria-live="polite"></aside></div>')
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_graph_page.py tests/test_render_page.py`
Expected: PASS (`test_render_page.py`'s i18n checks still pass: both languages have the same keys).

- [ ] **Step 7: Commit**

```bash
git add scripts/ledger_report/vendor/dagre.min.js scripts/ledger_report/vendor/LICENSE-dagre scripts/ledger_report/graph_page.py scripts/ledger_report/i18n.py tests/helpers/graph_fixture.py tests/test_graph_page.py
git commit -m "feat(graph-page): vendor dagre 3.1.1, graph-tab strings, masked page data with risks and cards"
```

---
### Task 5: The flowchart in the browser — `graph.js`, `graph.css`, tabbed page, DOM layout check

**Files:**
- Create: `scripts/ledger_report/assets/graph.js`, `scripts/ledger_report/assets/graph.css`
- Modify: `scripts/render.py` (replace `render_html`; `_coverage` gains the graph gaps; add imports)
- Modify: `scripts/shot.py` (append `dump_dom`, `layout_report`)
- Test: `tests/test_graph_render.py`

**Interfaces:**
- Consumes: `graph_page.page_data / data_script / render_graph_tab / dagre_source` (Task 4); `helpers.graph_fixture.make_project` (Task 4); v0.1 `render_html` internals; `shot.find_chrome`.
- Produces:
  - `render.render_html(ledger, run, probes, lang, graph_data=None) -> str` — unchanged output when `graph_data` is None; otherwise a tabbed page: sticky top bar (`h1`, tabs `[data-tab=graph|overview]`, `#vlg-search` + `#vlg-files` datalist, `#view-toggle`), `#tab-graph` (graph skeleton), `#tab-overview` (the v0.1 body, hidden), the data script, `report.js`, the inlined dagre, `graph.js`.
  - The page sets `<body data-layout="done">` after layout; each node is `<g class="vlg-node r-<role> s-<state> [sel] [dim]" data-id data-x data-y data-w data-h data-dim>`; URL params `select`, `tab`, `view`, `theme`.
  - `shot.dump_dom(chrome, url, timeout=90) -> str` and `shot.layout_report(dom) -> {"done": bool, "nodes": [{"id","x","y","w","h","cls","dim"}], "overlaps": [[a, b]], "selected": [ids]}`.

- [ ] **Step 1: Write the failing tests**

`tests/test_graph_render.py`:
```python
import pytest

import render
import shot
from helpers.graph_fixture import make_project
from helpers.verified import PROBES, RUN, sample
from ledger_report import graph_page


def page(tmp_path, lang="zh", **kw):
    root, g, explained, ledger, probes = make_project(tmp_path, **kw)
    data = graph_page.page_data(g, explained, ledger, probes, root, lang, True)
    return render.render_html(sample(), RUN, PROBES, lang, graph_data=data)


def test_tabbed_page_structure(tmp_path):
    html = page(tmp_path)
    assert html.count("<h1>") == 1 and 'class="vl-tabs"' in html and 'data-tab="overview"' in html
    assert 'id="vl-data"' in html and html.count("var dagre=") == 1 and "vlg-viewport" in html
    assert '<section id="tab-overview" class="vl-tabpanel" hidden>' in html and "对账表" in html
    assert html.index('id="vl-data"') < html.index("var dagre=") < html.index("function computeLayout")
    assert "<!--VL_DAGRE-->" not in html
    assert render.find_secrets(html.replace(graph_page.dagre_source(), "")) == []


def test_untabbed_page_is_unchanged():
    html = render.render_html(sample(), RUN, PROBES, "zh")
    assert "vl-tabs" not in html and "var dagre=" not in html and html.count("<h1>") == 1


def test_overview_coverage_lists_graph_gaps(tmp_path):
    root, g, explained, ledger, probes = make_project(tmp_path)
    g["unresolved"] = [{"from": "lib/ai.ts", "spec": "./gone", "line": 9}]
    g["excluded"] = {"tests": 2, "config": 1}
    explained["files"]["lib/ai.ts"]["dropped_functions"] = [{"name": "sendEmail", "reason": "not defined in this file"}]
    data = graph_page.page_data(g, explained, ledger, probes, root, "zh", True)
    overview = render.render_html(sample(), RUN, PROBES, "zh", graph_data=data).split('id="vl-data"')[0]
    assert "流程图没有画 2 个测试文件和 1 个配置文件" in overview
    assert "lib/ai.ts:9" in overview and "./gone" in overview and "lib/ai.ts · sendEmail" in overview


def test_dagre_has_no_script_breaking_text():
    assert "</script" not in graph_page.dagre_source().lower()


def _browser_or_skip():
    chrome = shot.find_chrome()
    if not chrome:
        pytest.skip("Chrome/Chromium not available")
    return chrome


def test_layout_and_selection_in_a_real_browser(tmp_path):
    chrome = _browser_or_skip()
    out = tmp_path / "report.html"
    out.write_text(page(tmp_path / "proj"), encoding="utf-8")
    dom = shot.dump_dom(chrome, out.as_uri() + "?select=lib/ai.ts")
    rep = shot.layout_report(dom)
    assert rep["done"] and rep["overlaps"] == []
    ids = {n["id"]: n for n in rep["nodes"]}
    assert set(ids) == {"app/page.tsx", "lib/ai.ts", "lib/util.ts", "ext:openai"}
    assert ids["ext:openai"]["x"] > ids["app/page.tsx"]["x"]
    assert ids["lib/util.ts"]["x"] > ids["app/page.tsx"]["x"]  # an unimported non-entry file is not drawn left of the entry
    assert rep["selected"] == ["lib/ai.ts"]
    assert ids["app/page.tsx"]["dim"] == "0" and ids["lib/util.ts"]["dim"] == "1"
    assert "把文字发给 OpenAI 总结。" in dom


def test_large_graph_collapses_without_overlaps_in_a_real_browser(tmp_path):
    chrome = _browser_or_skip()
    root = tmp_path / "big"
    for d in ("src/ai", "src/ui", "src/db", "src/util"):
        for i in range(40):
            p = root / d / f"f{i}.ts"
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(f'import "../util/f{(i + 1) % 40}";\n' if d != "src/util" else "", encoding="utf-8")
    (root / "src" / "main.ts").write_text('import "./ai/f0";\nimport "./ui/f0";\nimport "./db/f0";\n', encoding="utf-8")
    import graph
    g = graph.build(root, [], {"findings": []})
    data = graph_page.page_data(g, {"files": {}, "evidence": {}}, sample(), {"findings": []}, root, "en", False)
    out = tmp_path / "big.html"
    out.write_text(render.render_html(sample(), RUN, PROBES, "en", graph_data=data), encoding="utf-8")
    rep = shot.layout_report(shot.dump_dom(chrome, out.as_uri()))
    assert rep["done"] and rep["overlaps"] == []
    assert {n["id"] for n in rep["nodes"]} == {"folder:src/ai", "folder:src/ui", "folder:src/db", "folder:src/util", "src/main.ts"}


def test_layout_report_parses_nodes_and_finds_overlaps():
    dom = ('<body data-layout="done"><svg><g class="vlg-node r-logic s-ok sel" data-id="a" data-x="0" data-y="0" '
           'data-w="100" data-h="50" data-dim="0"></g><g class="vlg-node r-logic s-ok" data-id="b" data-x="90" '
           'data-y="10" data-w="100" data-h="50" data-dim="1"></g><g class="vlg-node" data-id="c" data-x="300" '
           'data-y="0" data-w="100" data-h="50" data-dim="1"></g></svg></body>')
    rep = shot.layout_report(dom)
    assert rep["done"] and rep["selected"] == ["a"] and rep["overlaps"] == [["a", "b"]] and len(rep["nodes"]) == 3
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_graph_render.py`
Expected: FAIL — `TypeError: render_html() got an unexpected keyword argument 'graph_data'` and `AttributeError: module 'shot' has no attribute 'dump_dom'`.

- [ ] **Step 3: Write `scripts/ledger_report/assets/graph.js`**

```javascript
/* vibe-ledger file flowchart: dagre layout, drawing, pan/zoom/pinch, selection, explanation panel. */
(function () {
  "use strict";
  var dataEl = document.getElementById("vl-data");
  if (!dataEl || typeof dagre === "undefined") return;
  var data = JSON.parse(dataEl.textContent);
  var S = data.strings;
  var NS = "http://www.w3.org/2000/svg";
  var W = 236, H = 58, EXT_GAP = 100, ROW_GAP = 22, RANK_GAP = 72;
  var ICON = { entry: "▶", logic: "ƒ", data: "⛁", paid: "✦", folder: "▤" };
  var svg = document.getElementById("vlg-svg");
  var viewport = document.getElementById("vlg-viewport");
  var panel = document.getElementById("vlg-panel");
  var byId = {}, folderOf = {}, folderById = {};
  data.nodes.forEach(function (n) { byId[n.id] = n; });
  data.folders.forEach(function (f) { folderById[f.id] = f; f.files.forEach(function (id) { folderOf[id] = f.id; }); });
  var expanded = {}, selected = null, view = { s: 1, x: 0, y: 0 }, layout = null, fitted = false;
  var pointers = {}, drag = null, pinch = null, moved = false;

  function fmt(s, kv) { return String(s).replace(/\{(\w+)\}/g, function (_, k) { return kv[k] == null ? "" : kv[k]; }); }
  function el(tag, cls, text) { var e = document.createElement(tag); if (cls) e.className = cls; if (text != null) e.textContent = text; return e; }
  function sv(tag, attrs) { var e = document.createElementNS(NS, tag); Object.keys(attrs || {}).forEach(function (k) { e.setAttribute(k, attrs[k]); }); return e; }
  function units(s) { var n = 0; for (var i = 0; i < s.length; i++) n += s.charCodeAt(i) > 0x2e80 ? 2 : 1; return n; }
  function dist(a, b) { return Math.hypot(a.x - b.x, a.y - b.y); }
  function isExt(id) { return id.indexOf("ext:") === 0; }
  function isFolder(id) { return id.indexOf("folder:") === 0; }
  function visibleId(id) { var f = folderOf[id]; return data.collapsed && f && !expanded[f] ? "folder:" + f : id; }
  function entity(vid) { return isFolder(vid) ? folderById[vid.slice(7)] : byId[vid]; }
  function roleOf(vid) { return isFolder(vid) ? "folder" : byId[vid].role; }

  function computeLayout() {
    var g = new dagre.graphlib.Graph();
    g.setGraph({ rankdir: "LR", nodesep: ROW_GAP, ranksep: RANK_GAP, marginx: 40, marginy: 40 });
    g.setDefaultEdgeLabel(function () { return {}; });
    var visible = {}, edges = {};
    data.nodes.forEach(function (n) {
      if (isExt(n.id)) return;
      var v = visibleId(n.id);
      if (!visible[v]) { visible[v] = true; g.setNode(v, { width: W, height: H }); }
    });
    data.edges.forEach(function (e) {
      var a = visibleId(e.from), b = isExt(e.to) ? e.to : visibleId(e.to);
      if (a === b) return;
      var k = a + "\u0001" + b;
      var x = edges[k] || (edges[k] = { from: a, to: b, count: 0, risky: false, names: [] });
      x.count += 1;
      x.risky = x.risky || e.risky;
      (e.names || []).forEach(function (nm) { if (x.names.indexOf(nm) < 0 && x.names.length < 6) x.names.push(nm); });
    });
    Object.keys(edges).forEach(function (k) { if (!isExt(edges[k].to)) g.setEdge(edges[k].from, edges[k].to); });
    if (data.entries.length) {
      g.setNode("__src", { width: 1, height: 1 });
      var isEntry = {}, hasIn = {};
      data.entries.forEach(function (id) { var v = visibleId(id); isEntry[v] = true; if (visible[v]) g.setEdge("__src", v); });
      Object.keys(edges).forEach(function (k) { hasIn[edges[k].to] = true; });
      // a file nothing imports that is not an entry belongs in the logic column, never left of the entries
      Object.keys(visible).forEach(function (v) { if (!isEntry[v] && !hasIn[v]) g.setEdge("__src", v, { minlen: 2 }); });
    }
    dagre.layout(g);
    var boxes = {}, ids = Object.keys(visible), maxRight = 0, minY = Infinity, maxY = -Infinity;
    ids.forEach(function (v) {
      var p = g.node(v), b = { id: v, x: p.x - W / 2, y: p.y - H / 2 };
      boxes[v] = b;
      maxRight = Math.max(maxRight, b.x + W);
      minY = Math.min(minY, b.y);
      maxY = Math.max(maxY, b.y + H);
    });
    if (!ids.length) { minY = 40; maxY = 40; }
    // outside services get their own column on the right, ordered by where their callers sit
    var exts = data.nodes.filter(function (n) { return isExt(n.id); }).map(function (n) {
      var ys = Object.keys(edges).filter(function (k) { return edges[k].to === n.id && boxes[edges[k].from]; })
        .map(function (k) { return boxes[edges[k].from].y; });
      return { id: n.id, order: ys.length ? ys.reduce(function (a, b) { return a + b; }, 0) / ys.length : 0 };
    }).sort(function (a, b) { return a.order - b.order || (a.id < b.id ? -1 : 1); });
    var colX = (ids.length ? maxRight : 40) + EXT_GAP;
    var total = exts.length * H + Math.max(0, exts.length - 1) * ROW_GAP;
    var y0 = (minY + maxY) / 2 - total / 2;
    exts.forEach(function (x, i) { boxes[x.id] = { id: x.id, x: colX, y: y0 + i * (H + ROW_GAP) }; });
    return { g: g, edges: edges, boxes: boxes };
  }

  function curve(pts) {
    var d = "M" + pts[0].x + "," + pts[0].y;
    if (pts.length < 3) return d + " L" + pts[pts.length - 1].x + "," + pts[pts.length - 1].y;
    for (var i = 0; i < pts.length - 1; i++) {
      var p0 = pts[i - 1] || pts[i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2] || p2;
      d += " C" + (p1.x + (p2.x - p0.x) / 6) + "," + (p1.y + (p2.y - p0.y) / 6) + " " +
        (p2.x - (p3.x - p1.x) / 6) + "," + (p2.y - (p3.y - p1.y) / 6) + " " + p2.x + "," + p2.y;
    }
    return d;
  }

  function link(a, b) {
    var dx = Math.max(40, (b.x - a.x) / 2);
    return "M" + a.x + "," + a.y + " C" + (a.x + dx) + "," + a.y + " " + (b.x - dx) + "," + b.y + " " + b.x + "," + b.y;
  }

  function drawBands(list) {
    if (!list.length) return;
    var minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
    list.forEach(function (b) { minX = Math.min(minX, b.x); maxX = Math.max(maxX, b.x + W); minY = Math.min(minY, b.y); maxY = Math.max(maxY, b.y + H); });
    var entryX = list.filter(function (b) { return !isExt(b.id) && roleOf(b.id) === "entry"; }).map(function (b) { return b.x; });
    var extX = list.filter(function (b) { return isExt(b.id); }).map(function (b) { return b.x; });
    var top = minY - 56, height = maxY - minY + 80, bands = [];
    var entryEnd = entryX.length ? Math.min.apply(null, entryX) + W + 18 : null;
    var dataStart = extX.length ? Math.min.apply(null, extX) - 18 : null;
    if (entryEnd !== null) bands.push([minX - 18, entryEnd, S.g_band_entry]);
    var ls = entryEnd !== null ? entryEnd + 10 : minX - 18, le = dataStart !== null ? dataStart - 10 : maxX + 18;
    if (le - ls > 40) bands.push([ls, le, S.g_band_logic]);
    if (dataStart !== null) bands.push([dataStart, maxX + 18, S.g_band_data]);
    var layer = sv("g", { "class": "vlg-bands" });
    bands.forEach(function (b) {
      layer.appendChild(sv("rect", { "class": "vlg-band", x: b[0], y: top, width: b[1] - b[0], height: height, rx: 16 }));
      var t = sv("text", { "class": "vlg-band-label", x: (b[0] + b[1]) / 2, y: top + 24, "text-anchor": "middle" });
      t.textContent = b[2];
      layer.appendChild(t);
    });
    viewport.appendChild(layer);
  }

  function drawNode(b) {
    var ent = entity(b.id), role = roleOf(b.id), state = ent.state || "ok";
    var g = sv("g", { "class": "vlg-node r-" + role + " s-" + state, "data-id": b.id, "data-x": b.x.toFixed(1),
      "data-y": b.y.toFixed(1), "data-w": W, "data-h": H, "data-dim": "0",
      transform: "translate(" + b.x.toFixed(1) + "," + b.y.toFixed(1) + ")", tabindex: "0" });
    g.appendChild(sv("rect", { "class": "vlg-card", width: W, height: H, rx: 14 }));
    g.appendChild(sv("circle", { "class": "vlg-icon-bg", cx: 24, cy: H / 2, r: 14 }));
    var icon = sv("text", { "class": "vlg-icon", x: 24, y: H / 2 + 5, "text-anchor": "middle" });
    icon.textContent = ICON[role] || "";
    g.appendChild(icon);
    var label = sv("text", { "class": "vlg-label", x: 46, y: 24 });
    label.textContent = ent.short || ent.label;
    g.appendChild(label);
    var sub = sv("text", { "class": "vlg-sub", x: 46, y: 42 });
    sub.textContent = ent.sub || "";
    g.appendChild(sub);
    if (ent.badge) {
      var bw = units(ent.badge) * 6.2 + 16;
      g.appendChild(sv("rect", { "class": "vlg-badge-bg", x: W - bw + 8, y: -9, width: bw, height: 18, rx: 9 }));
      var bt = sv("text", { "class": "vlg-badge", x: W - bw / 2 + 8, y: 4, "text-anchor": "middle" });
      bt.textContent = ent.badge;
      g.appendChild(bt);
    }
    var title = sv("title", {});
    title.textContent = isFolder(b.id) ? b.id.slice(7) : b.id;
    g.appendChild(title);
    g.addEventListener("click", function (ev) { ev.stopPropagation(); if (!moved) onNodeClick(b.id); });
    g.addEventListener("keydown", function (ev) { if (ev.key === "Enter") onNodeClick(b.id); });
    return g;
  }

  function draw() {
    layout = computeLayout();
    while (viewport.firstChild) viewport.removeChild(viewport.firstChild);
    var boxes = layout.boxes, ids = Object.keys(boxes);
    drawBands(ids.map(function (v) { return boxes[v]; }));
    var edgeLayer = sv("g", { "class": "vlg-edges" }), nodeLayer = sv("g", { "class": "vlg-nodes" });
    var labelLayer = sv("g", { "class": "vlg-edge-labels" });
    Object.keys(layout.edges).forEach(function (k) {
      var e = layout.edges[k], a = boxes[e.from], b = boxes[e.to];
      if (!a || !b) return;
      var d, mid;
      if (isExt(e.to)) {
        var p = { x: a.x + W, y: a.y + H / 2 }, q = { x: b.x, y: b.y + H / 2 };
        d = link(p, q);
        mid = { x: (p.x + q.x) / 2, y: (p.y + q.y) / 2 };
      } else {
        var pts = layout.g.edge(e.from, e.to).points;
        d = curve(pts);
        mid = pts[Math.floor(pts.length / 2)];
      }
      edgeLayer.appendChild(sv("path", { d: d, "class": "vlg-edge" + (e.risky ? " risky" : ""), "data-from": e.from,
        "data-to": e.to, "marker-end": "url(#vlg-arrow" + (e.risky ? "-risky" : "") + ")" }));
      // a link between folders stands for several imports: say how many in both views; names are for developers
      var merged = (isFolder(e.from) || isFolder(e.to)) && e.count > 1;
      if (merged || e.names.length) {
        var t = sv("text", { x: mid.x.toFixed(1), y: (mid.y - 6).toFixed(1),
          "class": "vlg-edge-label" + (merged ? "" : " dev-only"), "text-anchor": "middle", "data-from": e.from, "data-to": e.to });
        t.textContent = merged ? fmt(S.g_merged, { n: e.count }) : e.names.join(", ");
        labelLayer.appendChild(t);
      }
    });
    viewport.appendChild(edgeLayer);
    viewport.appendChild(nodeLayer);
    viewport.appendChild(labelLayer);
    ids.forEach(function (v) { nodeLayer.appendChild(drawNode(boxes[v])); });
    applySelection();
    document.body.setAttribute("data-layout", "done");
  }

  function neighborsOf(vid) {
    var set = {};
    set[vid] = true;
    Object.keys(layout.edges).forEach(function (k) {
      var e = layout.edges[k];
      if (e.from === vid) set[e.to] = true;
      if (e.to === vid) set[e.from] = true;
    });
    return set;
  }

  function applySelection() {
    var vid = selected ? visibleId(selected) : null, nb = vid ? neighborsOf(vid) : null;
    viewport.querySelectorAll(".vlg-node").forEach(function (g) {
      var id = g.getAttribute("data-id"), dim = !!nb && !nb[id];
      g.classList.toggle("sel", id === vid);
      g.classList.toggle("dim", dim);
      g.setAttribute("data-dim", dim ? "1" : "0");
    });
    viewport.querySelectorAll("[data-from]").forEach(function (e) {
      var hot = !!vid && (e.getAttribute("data-from") === vid || e.getAttribute("data-to") === vid);
      e.classList.toggle("hot", hot);
      e.classList.toggle("dim", !!vid && !hot);
      if (e.tagName.toLowerCase() === "path") {
        e.setAttribute("marker-end", "url(#vlg-arrow" + (hot ? "-hot" : e.classList.contains("risky") ? "-risky" : "") + ")");
      }
    });
  }

  function apply() {
    viewport.setAttribute("transform", "translate(" + view.x.toFixed(1) + "," + view.y.toFixed(1) + ") scale(" + view.s.toFixed(4) + ")");
  }

  function bbox() {
    var minX = Infinity, minY = Infinity, maxX = -Infinity, maxY = -Infinity;
    Object.keys(layout.boxes).forEach(function (k) {
      var b = layout.boxes[k];
      minX = Math.min(minX, b.x); minY = Math.min(minY, b.y); maxX = Math.max(maxX, b.x + W); maxY = Math.max(maxY, b.y + H);
    });
    if (minX === Infinity) return { x: 0, y: 0, w: 400, h: 300 };
    return { x: minX - 30, y: minY - 70, w: maxX - minX + 60, h: maxY - minY + 100 };
  }

  function fit() {
    var r = svg.getBoundingClientRect();
    if (!r.width || !r.height) return;
    var b = bbox(), s = Math.min((r.width - 40) / b.w, (r.height - 40) / b.h, 1.25);
    s = Math.max(s, r.width < 560 ? 0.55 : 0.2);  // on a phone keep cards readable; the user drags to see the rest
    var gw = b.w * s, gh = b.h * s;
    view.s = s;
    view.x = gw <= r.width ? (r.width - gw) / 2 - b.x * s : 12 - b.x * s;  // too wide: start at the entries
    view.y = gh <= r.height ? (r.height - gh) / 2 - b.y * s : 12 - b.y * s;
    apply();
    fitted = true;
  }

  function zoomTo(ns, cx, cy) {
    ns = Math.max(0.15, Math.min(3, ns));
    view.x = cx - (cx - view.x) * (ns / view.s);
    view.y = cy - (cy - view.y) * (ns / view.s);
    view.s = ns;
    apply();
  }

  function zoomBy(f) { var r = svg.getBoundingClientRect(); zoomTo(view.s * f, r.width / 2, r.height / 2); }

  function centerOn(id) {
    var b = layout.boxes[visibleId(id)], r = svg.getBoundingClientRect();
    if (!b || !r.width) return;
    view.x = r.width / 2 - (b.x + W / 2) * view.s;
    view.y = r.height / 2 - (b.y + H / 2) * view.s;
    apply();
  }

  function onNodeClick(vid) {
    if (isFolder(vid)) {
      expanded[vid.slice(7)] = true;
      draw();
      fit();
      return;
    }
    select(vid, false);
  }

  function select(id, center) {
    if (!byId[id]) return;
    if (visibleId(id) !== id) { expanded[folderOf[id]] = true; draw(); }
    selected = id;
    applySelection();
    renderPanel();
    if (center) centerOn(id);
  }

  function clearSelection() { selected = null; applySelection(); renderPanel(); }
  function chip(id) {
    var n = byId[id], b = el("button", "vlg-chip r-" + (n ? n.role : "logic"), n ? n.label : id);
    b.type = "button";
    b.title = id;
    b.addEventListener("click", function () { select(id, true); });
    return b;
  }

  function section(title) {
    var s = el("div", "vlg-sec");
    s.appendChild(el("h3", null, title));
    panel.appendChild(s);
    return s;
  }

  function chips(parent, ids) {
    var box = el("div", "vlg-chips");
    ids.forEach(function (id) { box.appendChild(chip(id)); });
    parent.appendChild(box);
  }

  function renderOverview() {
    if (!data.nodes.some(function (n) { return !isExt(n.id); })) panel.appendChild(el("p", "vlg-warnnote", S.g_no_files));
    panel.appendChild(el("p", "vlg-purpose", data.summary));
    var ul = el("ul", "vlg-howto");
    data.howto.forEach(function (line) { ul.appendChild(el("li", null, line)); });
    panel.appendChild(ul);
    var sec = section(S.g_top);
    if (!data.top.length) { sec.appendChild(el("p", "vlg-ok", S.g_no_problems)); return; }
    data.top.forEach(function (id) {
      var n = byId[id], b = el("button", "vlg-top-item s-" + n.state);
      b.type = "button";
      b.appendChild(el("span", null, n.label));
      b.appendChild(el("span", "vlg-top-badge", n.badge));
      b.addEventListener("click", function () { select(id, true); });
      sec.appendChild(b);
    });
  }

  function renderPanel() {
    while (panel.firstChild) panel.removeChild(panel.firstChild);
    if (!selected) { renderOverview(); return; }
    var c = byId[selected].card, dev = document.body.classList.contains("dev");
    var close = el("button", "vlg-close", "×");
    close.type = "button";
    close.title = S.g_close;
    close.addEventListener("click", clearSelection);
    panel.appendChild(close);
    if (c.folder) panel.appendChild(el("div", "vlg-path", c.folder + "/"));
    panel.appendChild(el("h2", null, c.label));
    panel.appendChild(el("span", "vlg-role r-" + c.role, c.role_label));
    if (isExt(selected)) {
      panel.appendChild(el("p", "vlg-purpose", c.auto));
      if (c.called_by.length) chips(section(S.g_called_by), c.called_by);
      var evs = section(S.g_where);
      c.evidence.forEach(function (e) {
        evs.appendChild(el("div", "vlg-path", e.where));
        if (dev) evs.appendChild(el("pre", null, e.code));
      });
      return;
    }
    if (c.explained) {
      panel.appendChild(el("p", "vlg-purpose", c.purpose_plain));
      if (c.purpose_unverified) panel.appendChild(el("p", "vlg-warnnote", c.unverified_note));
      if (dev && c.purpose_dev) panel.appendChild(el("p", "vlg-muted", c.purpose_dev));
    } else {
      panel.appendChild(el("p", "vlg-muted", S.g_no_explain));
      panel.appendChild(el("p", "vlg-purpose", c.auto));
    }
    if (dev) panel.appendChild(el("p", "vlg-muted", c.path + " · " + c.lines));
    if (c.calls.length) chips(section(S.g_calls), c.calls);
    if (c.called_by.length) chips(section(S.g_called_by), c.called_by);
    if (c.functions.length) {
      var fs = section(S.g_functions);
      c.functions.forEach(function (f) {
        var row = el("div", "vlg-fn");
        row.appendChild(el("code", null, f.name + (dev ? ":" + f.line : "")));
        row.appendChild(document.createTextNode(" " + f.plain));
        fs.appendChild(row);
        var snip = dev ? c.snippets.filter(function (s) { return s.name === f.name; })[0] : null;
        if (snip) fs.appendChild(el("pre", null, snip.code));
      });
    } else if (c.exports.length) {
      var ex = section(S.g_exports), box = el("div", "vlg-chips");
      c.exports.forEach(function (x) { box.appendChild(el("code", "vlg-export", x.name + (dev ? ":" + x.line : ""))); });
      ex.appendChild(box);
    }
    var rs = section(S.g_risks);
    if (!c.risks.length) rs.appendChild(el("p", "vlg-ok", "✅ " + S.g_no_risks));
    c.risks.forEach(function (r) {
      var row = el("details", "vlg-risk " + r.level);  // the evidence opens on click
      row.appendChild(el("summary", null, r.text));
      row.appendChild(el("div", "vlg-path", r.where));
      rs.appendChild(row);
    });
    if (c.promises.length) {
      var ps = section(S.g_promises);
      c.promises.forEach(function (p) {
        var row = el("div", "vlg-promise", p.glyph + " " + p.plain + " ");
        var a = el("a", null, S.g_in_overview);
        a.href = "#" + p.id;
        a.addEventListener("click", function () { showTab("overview"); });
        row.appendChild(a);
        ps.appendChild(row);
      });
    }
    var hs = section(S.g_history);
    if (c.history.length) {
      c.history.forEach(function (item) {
        hs.appendChild(el("div", null, item.plain + (item.date ? " · " + item.date : "")));
        if (item.quote) hs.appendChild(el("blockquote", null, item.quote));
      });
    } else {
      hs.appendChild(el("p", "vlg-muted", c.history_note));
    }
    if (c.edits) hs.appendChild(el("p", "vlg-muted", c.edits));
    if (data.collapsed && folderOf[selected] && expanded[folderOf[selected]]) {
      var fold = el("button", "vlg-chip", S.g_collapse);
      fold.type = "button";
      fold.addEventListener("click", function () {
        delete expanded[folderOf[selected]];
        selected = null;
        draw();
        fit();
        renderPanel();
      });
      panel.appendChild(fold);
    }
  }

  function showTab(name) {
    document.querySelectorAll(".vl-tab").forEach(function (b) { b.classList.toggle("on", b.getAttribute("data-tab") === name); });
    document.querySelectorAll(".vl-tabpanel").forEach(function (p) { p.hidden = p.id !== "tab-" + name; });
    if (name === "graph" && !fitted) fit();
  }

  function findNode(q) {
    q = (q || "").trim().toLowerCase();
    if (!q) return null;
    var exact = data.nodes.filter(function (n) { return n.id.toLowerCase() === q || n.label.toLowerCase() === q; })[0];
    return exact || data.nodes.filter(function (n) {
      return n.id.toLowerCase().indexOf(q) >= 0 || n.label.toLowerCase().indexOf(q) >= 0;
    })[0] || null;
  }

  function wire() {
    var defs = sv("defs", {});
    [["vlg-arrow", ""], ["vlg-arrow-risky", " risky"], ["vlg-arrow-hot", " hot"]].forEach(function (m) {
      var mk = sv("marker", { id: m[0], viewBox: "0 0 8 8", refX: 7, refY: 4, markerWidth: 7, markerHeight: 7, orient: "auto" });
      mk.appendChild(sv("path", { d: "M0,0 L8,4 L0,8 z", "class": "vlg-arrow" + m[1] }));
      defs.appendChild(mk);
    });
    svg.insertBefore(defs, viewport);
    svg.addEventListener("pointerdown", function (ev) {
      pointers[ev.pointerId] = { x: ev.clientX, y: ev.clientY };
      moved = false;
      var ids = Object.keys(pointers);
      if (ids.length === 1) drag = { x: ev.clientX, y: ev.clientY, vx: view.x, vy: view.y };
      else if (ids.length === 2) {
        var a = pointers[ids[0]], b = pointers[ids[1]];
        pinch = { d: dist(a, b) || 1, s: view.s, cx: (a.x + b.x) / 2, cy: (a.y + b.y) / 2 };
        drag = null;
      }
    });
    window.addEventListener("pointermove", function (ev) {
      if (!pointers[ev.pointerId]) return;
      pointers[ev.pointerId] = { x: ev.clientX, y: ev.clientY };
      var ids = Object.keys(pointers);
      if (pinch && ids.length === 2) {
        var a = pointers[ids[0]], b = pointers[ids[1]], r = svg.getBoundingClientRect();
        zoomTo(pinch.s * dist(a, b) / pinch.d, pinch.cx - r.left, pinch.cy - r.top);
        moved = true;
      } else if (drag) {
        var dx = ev.clientX - drag.x, dy = ev.clientY - drag.y;
        if (Math.abs(dx) + Math.abs(dy) > 4) moved = true;
        view.x = drag.vx + dx;
        view.y = drag.vy + dy;
        apply();
      }
    });
    function end(ev) {
      delete pointers[ev.pointerId];
      if (Object.keys(pointers).length < 2) pinch = null;
      if (!Object.keys(pointers).length) drag = null;
    }
    window.addEventListener("pointerup", end);
    window.addEventListener("pointercancel", end);
    svg.addEventListener("wheel", function (ev) {
      ev.preventDefault();
      var r = svg.getBoundingClientRect();
      zoomTo(view.s * (ev.deltaY < 0 ? 1.12 : 1 / 1.12), ev.clientX - r.left, ev.clientY - r.top);
    }, { passive: false });
    svg.addEventListener("click", function (ev) { if (!moved && !ev.target.closest(".vlg-node")) clearSelection(); });
    document.querySelectorAll(".vlg-tools [data-act]").forEach(function (b) {
      var act = b.getAttribute("data-act");
      if ((act === "expand-all" || act === "collapse-all") && data.collapsed) b.hidden = false;
      b.addEventListener("click", function () {
        if (act === "zoom-in") zoomBy(1.2);
        else if (act === "zoom-out") zoomBy(1 / 1.2);
        else if (act === "fit") fit();
        else if (act === "expand-all") { data.folders.forEach(function (f) { expanded[f.id] = true; }); draw(); fit(); }
        else if (act === "collapse-all") {
          expanded = {};
          if (selected && folderOf[selected]) selected = null;
          draw();
          fit();
          renderPanel();
        }
      });
    });
    document.querySelectorAll(".vl-tab").forEach(function (b) {
      b.addEventListener("click", function () { showTab(b.getAttribute("data-tab")); });
    });
    var search = document.getElementById("vlg-search"), list = document.getElementById("vlg-files");
    if (list) data.nodes.forEach(function (n) { var o = document.createElement("option"); o.value = isExt(n.id) ? n.label : n.id; list.appendChild(o); });
    if (search) {
      var go = function () { var n = findNode(search.value); if (n) { showTab("graph"); select(n.id, true); } };
      search.addEventListener("change", go);
      search.addEventListener("keydown", function (ev) { if (ev.key === "Enter") go(); });
    }
    var toggle = document.getElementById("view-toggle");
    if (toggle) toggle.addEventListener("click", function () { setTimeout(renderPanel, 0); });
    document.addEventListener("keydown", function (ev) { if (ev.key === "Escape") clearSelection(); });
    window.addEventListener("resize", function () { if (fitted) fit(); });
  }

  wire();
  draw();
  var params = new URLSearchParams(location.search);
  showTab(params.get("tab") === "overview" ? "overview" : "graph");
  var want = params.get("select");
  if (want && byId[want]) select(want, true); else renderPanel();
})();
```

- [ ] **Step 4: Write `scripts/ledger_report/assets/graph.css`**

```css
body.tabbed{overflow-x:hidden}
.vl-top{position:sticky;top:0;z-index:5;display:flex;align-items:center;gap:12px;padding:10px 16px;background:var(--bg);
  border-bottom:1px solid var(--line)}
.vl-top h1{font-size:18px;line-height:1.3;margin:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
.vl-tabs{display:flex;gap:6px;flex:none}
.vl-tab{font:inherit;font-size:14px;padding:5px 14px;border-radius:999px;border:1px solid var(--line);background:var(--card);
  color:var(--fg);cursor:pointer;white-space:nowrap}
.vl-tab.on{background:var(--fg);color:var(--bg);border-color:var(--fg)}
#vlg-search{margin-left:auto;font:inherit;font-size:14px;padding:6px 10px;border:1px solid var(--line);border-radius:10px;
  background:var(--card);color:var(--fg);width:220px;min-width:0}
.vl-tabpanel{margin-top:0}  /* report.css gives every section a top margin */
.vl-tabpanel[hidden]{display:none}
.vlg{display:flex;height:calc(100vh - 58px);min-height:520px}
.vlg-canvas{position:relative;flex:63 1 0;min-width:0;background:var(--bg)}
#vlg-svg{width:100%;height:100%;display:block;touch-action:none;cursor:grab;user-select:none;-webkit-user-select:none}
.vlg-panel{flex:37 1 0;min-width:300px;max-width:560px;overflow-y:auto;border-left:1px solid var(--line);background:var(--card);
  padding:18px 20px 40px}
.vlg-tools{position:absolute;top:12px;right:12px;display:flex;gap:6px}
.vlg-tools button{font:inherit;font-size:13px;min-width:32px;padding:5px 9px;border-radius:8px;border:1px solid var(--line);
  background:var(--card);color:var(--fg);cursor:pointer}
.vlg-tools button[hidden]{display:none}
.vlg-legend{position:absolute;left:12px;bottom:12px;display:flex;flex-wrap:wrap;gap:12px;font-size:12px;color:var(--muted);
  background:color-mix(in srgb,var(--bg) 88%,transparent);padding:6px 10px;border-radius:8px}
.vlg-legend-item.k-bad{color:var(--bad)}.vlg-legend-item.k-warn{color:var(--warn)}.vlg-legend-item.k-paid{color:var(--paid)}
.vlg-band{fill:var(--soft)}.vlg-band-label{font-size:13px;font-weight:650;fill:var(--muted)}
.vlg-node{cursor:pointer;outline:none}
.vlg-node .vlg-card{fill:var(--nf);stroke:var(--nf);stroke-width:1.2}
.vlg-node.r-entry{--nf:#e8efff;--ni:#1d4ed8}.vlg-node.r-logic{--nf:#eef0f3;--ni:#334155}
.vlg-node.r-data{--nf:#e2f5f1;--ni:#0f766e}.vlg-node.r-paid{--nf:#fff1dc;--ni:#b45309}
.vlg-node.r-folder{--nf:#f1f0ed;--ni:#44403c}
.vlg-node.r-folder .vlg-card{stroke:#a8a29e;stroke-dasharray:6 4}
.vlg-node.s-warn .vlg-card{stroke:var(--warn);stroke-width:2.4;stroke-dasharray:none}
.vlg-node.s-bad .vlg-card{stroke:var(--bad);stroke-width:2.6;stroke-dasharray:none}
.vlg-node.sel .vlg-card{stroke:#7c3aed;stroke-width:3.2}
.vlg-node:focus-visible .vlg-card{stroke:#7c3aed}
.vlg-node.dim{opacity:.28}
.vlg-icon-bg{fill:var(--card)}.vlg-icon{font-size:14px;font-weight:700;fill:var(--ni)}
.vlg-label{font-size:14px;font-weight:700;fill:var(--ni)}.vlg-sub{font-size:11.5px;fill:var(--muted)}
.vlg-badge-bg{fill:var(--bad)}.vlg-node.s-warn .vlg-badge-bg{fill:var(--warn)}
.vlg-badge{font-size:10.5px;font-weight:700;fill:#fff}
.vlg-edge{fill:none;stroke:#a3a3a3;stroke-width:1.5}.vlg-edge.risky{stroke:var(--bad);stroke-width:2}
.vlg-edge.hot{stroke:#7c3aed;stroke-width:2.6}
.vlg-edge.dim,.vlg-edge-label.dim{opacity:.18}
.vlg-edge-label{font-size:11px;fill:var(--muted);paint-order:stroke;stroke:var(--bg);stroke-width:4px;stroke-linejoin:round}
.vlg-arrow{fill:#a3a3a3}.vlg-arrow.risky{fill:var(--bad)}.vlg-arrow.hot{fill:#7c3aed}
.vlg-panel h2{font-size:19px;margin:2px 0 6px;word-break:break-all}
.vlg-path{font-size:12px;color:var(--muted);word-break:break-all}
.vlg-role{display:inline-block;font-size:12px;padding:1px 9px;border-radius:999px;background:var(--soft);color:var(--muted)}
.vlg-close{float:right;font:inherit;border:0;background:none;color:var(--muted);font-size:20px;line-height:1;cursor:pointer}
.vlg-purpose{font-size:15px;line-height:1.6;margin:10px 0}
.vlg-howto{padding-left:18px;color:var(--muted);font-size:14px}
.vlg-sec{margin-top:16px}.vlg-sec h3{font-size:13.5px;margin:0 0 6px}
.vlg-chips{display:flex;flex-wrap:wrap;gap:6px}
.vlg-chip{font:inherit;font-size:12.5px;padding:3px 9px;border-radius:8px;border:1px solid var(--line);background:var(--bg);
  color:var(--fg);cursor:pointer;margin-top:8px}
.vlg-chips .vlg-chip{margin-top:0}
.vlg-chip.r-paid{border-color:#f3d9b1;background:#fff8ec}.vlg-chip.r-data{border-color:#b8e3d9;background:#effaf7}
.vlg-export{font-size:12.5px;padding:2px 7px;border-radius:6px;background:var(--soft)}
.vlg-fn{margin:5px 0}.vlg-fn code{font-weight:650}
.vlg-risk{margin:5px 0;padding-left:10px;border-left:3px solid var(--warn)}.vlg-risk.bad{border-color:var(--bad)}
.vlg-risk summary{cursor:pointer}.vlg-risk .vlg-path{margin-top:3px}
.vlg-promise{margin:5px 0}.vlg-promise a{font-size:12.5px;color:var(--accent)}
.vlg-ok{color:var(--ok)}.vlg-muted{color:var(--muted)}.vlg-warnnote{color:var(--warn);font-size:13px}
.vlg-panel pre{white-space:pre-wrap;word-break:break-word;background:var(--soft);padding:6px 8px;border-radius:6px;
  font:12px/1.45 ui-monospace,Menlo,monospace;margin:4px 0}
.vlg-panel blockquote{margin:4px 0;padding-left:10px;border-left:3px solid var(--line);color:var(--muted)}
.vlg-top-item{display:flex;justify-content:space-between;gap:10px;width:100%;text-align:left;font:inherit;padding:8px 10px;
  margin:4px 0;border:1px solid var(--line);border-radius:10px;background:var(--bg);color:var(--fg);cursor:pointer}
.vlg-top-item.s-bad .vlg-top-badge{color:var(--bad)}.vlg-top-item.s-warn .vlg-top-badge{color:var(--warn)}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]) .vlg-node.r-entry{--nf:#1d2a4b;--ni:#9db8ff}
  :root:not([data-theme=light]) .vlg-node.r-logic{--nf:#262a31;--ni:#cbd5e1}
  :root:not([data-theme=light]) .vlg-node.r-data{--nf:#123a33;--ni:#7ddcc4}
  :root:not([data-theme=light]) .vlg-node.r-paid{--nf:#3d2a10;--ni:#f5c271}
  :root:not([data-theme=light]) .vlg-node.r-folder{--nf:#2a2826;--ni:#d6d3d1}
  :root:not([data-theme=light]) .vlg-chip.r-paid{background:#3d2a10;border-color:#6b4a1c}
  :root:not([data-theme=light]) .vlg-chip.r-data{background:#123a33;border-color:#1f5c50}}
:root[data-theme=dark] .vlg-node.r-entry{--nf:#1d2a4b;--ni:#9db8ff}
:root[data-theme=dark] .vlg-node.r-logic{--nf:#262a31;--ni:#cbd5e1}
:root[data-theme=dark] .vlg-node.r-data{--nf:#123a33;--ni:#7ddcc4}
:root[data-theme=dark] .vlg-node.r-paid{--nf:#3d2a10;--ni:#f5c271}
:root[data-theme=dark] .vlg-node.r-folder{--nf:#2a2826;--ni:#d6d3d1}
:root[data-theme=dark] .vlg-chip.r-paid{background:#3d2a10;border-color:#6b4a1c}
:root[data-theme=dark] .vlg-chip.r-data{background:#123a33;border-color:#1f5c50}
@media (max-width:760px){
  .vl-top{flex-wrap:wrap}
  #vlg-search{flex:1 1 160px;width:auto;margin-left:0}
  .vlg{flex-direction:column;height:auto}
  .vlg-canvas{height:55vh;flex:none}
  .vlg-panel{flex:none;overflow:visible;max-width:none;min-width:0;border-left:0;border-top:1px solid var(--line)}
}
```

- [ ] **Step 5: Replace `render_html` in `scripts/render.py`**

Add to the imports: `from ledger_report.graph_page import dagre_source, data_script, render_graph_tab`, and below `FIXABLE` add `DAGRE_SLOT = "<!--VL_DAGRE-->"`. Replace the whole `render_html` function with:

```python
def render_html(ledger: dict, run: dict, probes: dict, lang: str, graph_data: dict | None = None) -> str:
    ev = ledger["evidence"]
    c = counts(ledger)
    s = run.get("sessions", {})
    has_tx = bool(s.get("records"))
    sums = summaries(ledger, lang, has_tx)
    sub = (t(lang, "subtitle", threads=s.get("threads", 0), start=fmt_date(s.get("earliest"))[:10],
             end=fmt_date(s.get("latest"))[:10]) if has_tx else t(lang, "subtitle_none"))
    name = run.get("project_name", "")
    tabbed = graph_data is not None
    title = f'<h1>{h(t(lang, "title", name=name))}</h1>'
    toggle = (f'<button id="view-toggle" class="toggle" type="button" aria-pressed="false">'
              f'<span class="plain-only">{h(t(lang, "view_dev"))}</span><span class="dev-only">{h(t(lang, "view_plain"))}</span></button>')
    counts_html = ('<div class="counts">'
                   + "".join(f'<span class="count s-{st}">{GLYPH[st]} {h(t(lang, "status_" + st))} <b>{c[st]}</b></span>' for st in ORDER)
                   + "</div>" if has_tx else f'<p class="note">{h(t(lang, "no_tx_counts"))}</p>')
    body = [f'<header>{"" if tabbed else title}<p class="sub">{h(sub)}</p>{"" if tabbed else toggle}{counts_html}</header>']
    diagrams = {"map": render_map(ledger, lang), "access": render_access(ledger, lang),
                "timeline": render_timeline(ledger, lang, has_tx)}
    for sec_title, questions, key in SECTIONS:
        part = [f"<section><h2>{h(t(lang, sec_title))}</h2>"]
        part += [f'<p class="summary"><b>{h(t(lang, "q_" + q))}{h(t(lang, "colon"))}</b>{h(sums[q])}</p>' for q in questions]
        part.append(diagrams[key])
        cards = sorted((p for p in ledger["promises"] if p["question"] in questions), key=lambda p: ORDER.index(p["status"]))
        if cards:
            part.append('<div class="cards">' + "".join(_card(p, ev, lang) for p in cards) + "</div>")
        part.append("</section>")
        body.append("".join(part))
    body.append(f'<section class="dev-only"><h2>{h(t(lang, "sec_paths"))}</h2>{render_paths(ledger, lang)}</section>')
    body.append(f'<section><h2>{h(t(lang, "sec_ledger"))}</h2>{_ledger_table(ledger, lang)}</section>')
    graph_cov = graph_data.get("coverage") if tabbed else None
    body.append(f'<section><h2>{h(t(lang, "sec_coverage"))}</h2>{_coverage(ledger, run, probes, lang, graph_cov)}</section>')
    css = (ASSETS / "report.css").read_text(encoding="utf-8")
    if tabbed:
        css += "\n" + (ASSETS / "graph.css").read_text(encoding="utf-8")
    js = (ASSETS / "report.js").read_text(encoding="utf-8")
    html_lang = "zh-CN" if lang == "zh" else "en"
    head = (f'<!doctype html><html lang="{html_lang}"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{h(t(lang, "doc_title", name=name))}</title><style>{css}</style></head>')
    if not tabbed:
        doc = head + f'<body><div class="wrap">{"".join(body)}</div><script>{js}</script></body></html>'
        assert_no_secrets(doc)
        return doc
    tabs = "".join(f'<button type="button" class="vl-tab{" on" if key == "graph" else ""}" data-tab="{key}">{h(t(lang, label))}</button>'
                   for key, label in (("graph", "g_tab_graph"), ("overview", "g_tab_overview")))
    top = (f'<header class="vl-top">{title}<nav class="vl-tabs">{tabs}</nav>'
           f'<input id="vlg-search" type="search" list="vlg-files" placeholder="{h(t(lang, "g_search"))}" autocomplete="off">'
           f'<datalist id="vlg-files"></datalist>{toggle}</header>')
    gjs = (ASSETS / "graph.js").read_text(encoding="utf-8")
    doc = (head + f'<body class="tabbed">{top}<section id="tab-graph" class="vl-tabpanel">{render_graph_tab(lang)}</section>'
           f'<section id="tab-overview" class="vl-tabpanel" hidden><div class="wrap">{"".join(body)}</div></section>'
           f'{data_script(graph_data)}<script>{js}</script>{DAGRE_SLOT}<script>{gjs}</script></body></html>')
    assert_no_secrets(doc)  # the vendored library is static, so it goes in after the check
    return doc.replace(DAGRE_SLOT, "<script>" + dagre_source() + "</script>", 1)
```

Then change `_coverage`'s signature to `def _coverage(ledger: dict, run: dict, probes: dict, lang: str, graph_cov: dict | None = None) -> str:` and insert, directly after the `if unsupported:` block (before `failed = …`):
```python
    if graph_cov:
        ex = graph_cov.get("excluded", {})
        if ex.get("tests") or ex.get("config"):
            items.append(f'<li>{h(t(lang, "cov_graph_excluded", tests=ex.get("tests", 0), config=ex.get("config", 0)))}</li>')
        unres = graph_cov.get("unresolved", [])
        if unres:
            sub = "".join(f'<li><code>{ht(u["from"], 80)}:{u["line"]}</code> → <code>{ht(u["spec"], 80)}</code></li>'
                          for u in unres[:30])
            items.append(f'<li>{h(t(lang, "cov_unresolved", n=len(unres)))}<ul>{sub}</ul></li>')
        bad = ([(r["path"], r["reason"]) for r in graph_cov.get("rejected", [])]
               + [(f'{d["path"]} · {d["name"]}', d["reason"]) for d in graph_cov.get("dropped", [])])
        if bad:
            sub = "".join(f"<li><code>{ht(a, 90)}</code> — {ht(b, 160)}</li>" for a, b in bad[:30])
            items.append(f'<li>{h(t(lang, "cov_explain_dropped", n=len(bad)))}<ul>{sub}</ul></li>')
```

- [ ] **Step 6: Append the DOM layout check to `scripts/shot.py`**

Add `from html.parser import HTMLParser` to the imports, then append:
```python
class _NodeParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.nodes: list[dict] = []
        self.done = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "body" and a.get("data-layout") == "done":
            self.done = True
        if tag == "g" and "vlg-node" in (a.get("class") or "").split():
            self.nodes.append({"id": a.get("data-id"), "x": float(a.get("data-x") or 0), "y": float(a.get("data-y") or 0),
                               "w": float(a.get("data-w") or 0), "h": float(a.get("data-h") or 0),
                               "cls": a.get("class") or "", "dim": a.get("data-dim") or "0"})


def dump_dom(chrome: str, url: str, timeout: int = 90) -> str:
    """The page's DOM after its scripts ran (headless Chrome)."""
    try:
        res = subprocess.run([chrome, "--headless=new", "--disable-gpu", "--window-size=1400,900",
                              "--virtual-time-budget=5000", "--dump-dom", url],
                             capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return res.stdout


def layout_report(dom: str) -> dict:
    p = _NodeParser()
    p.feed(dom or "")
    nodes, overlaps = p.nodes, []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            a, b = nodes[i], nodes[j]
            if (a["x"] < b["x"] + b["w"] - 1 and b["x"] < a["x"] + a["w"] - 1
                    and a["y"] < b["y"] + b["h"] - 1 and b["y"] < a["y"] + a["h"] - 1):
                overlaps.append([a["id"], b["id"]])
    return {"done": p.done, "nodes": nodes, "overlaps": overlaps,
            "selected": [n["id"] for n in nodes if "sel" in n["cls"].split()]}
```

- [ ] **Step 7: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_graph_render.py tests/test_render_page.py tests/test_render_map_access.py tests/test_render_timeline_paths.py`
Expected: PASS (the two browser tests are skipped only where Chrome is missing — on this machine they must run).

- [ ] **Step 8: Look at the page**

Write the fixture page to the scratchpad and screenshot it (desktop, phone 390 px, dark, `?select=lib/ai.ts`) with `shot.take_shots`; open the PNGs. Check: cards are coloured by type with icons, the selected card is purple and its neighbours stay sharp, the panel shows purpose / calls / functions / risks / history, bands are labelled, nothing overlaps, the phone view stacks. Fix CSS or `graph.js` and repeat until it reads clearly.

- [ ] **Step 9: Commit**

```bash
git add scripts/ledger_report/assets/graph.js scripts/ledger_report/assets/graph.css scripts/render.py scripts/shot.py tests/test_graph_render.py
git commit -m "feat(graph): interactive file flowchart tab with dagre layout, selection, panel and layout check"
```

---
### Task 6: Command line — graph at `start`, explanation parts at `merge`, `explain.json` at `check`, tabbed `render`, selected shot and layout check at `shot`

**Files:**
- Modify: `scripts/vl.py` (imports, `do_start`, `_print_start`, `do_merge`, `do_check`, `do_render`, `do_shot`, `main`; new `graph_stats`, `top_file`, `_check_explain`, `_print_layout`)
- Modify: `scripts/shot.py` (replace `take_shots`; module docstring)
- Modify: `tests/test_cli.py`, `tests/test_e2e_deterministic.py` (write an `explain.json` before `check`)
- Test: `tests/test_cli_v02.py`

**Interfaces:**
- Consumes: `graph.build`, `graph.explain_pack`, `graph.EXPLAIN_CHUNK` (Tasks 1–2); `explain.verify`, `explain.merge`, `explain.summary_lines`, `explain.ExplainError` (Task 3); `graph_page.page_data` (Task 4); `render.render_html(..., graph_data=...)`, `shot.dump_dom`, `shot.layout_report` (Task 5).
- Produces:
  - Run folder files: `graph.json`, `explain_pack.md` (at `start`); `explain.json` (agent, or `merge` from `parts/explain_*.json`); `explain.verified.json` (at `check`).
  - `run.json` gains `"graph": {"files", "edges", "externals", "entries", "explain", "explain_groups", "collapsed", "unresolved", "excluded"}`.
  - `vl.EXPLAIN_GUIDE` (Path of `references/explain-guide.md`, written in Task 7), `vl.graph_stats(g) -> dict`, `vl.top_file(g) -> str | None` (highest score, ties by path).
  - `vl.py check --explain PATH` (default `<run>/explain.json`). `check` deletes any old `explain.verified.json` first and exits 2 when `explain.json` is missing, malformed or the run has no `graph.json`.
  - `shot.take_shots(report, out_dir, chrome, select=None, height=6000) -> list[Path]` — `desktop.png`, `desktop-dark.png`, `phone-390.png` (390 px iframe, 1400 px tall, opened on the selected file), `selected.png` (only when `select` is given) and `overview.png` (`?tab=overview`, full height).

- [ ] **Step 1: Write the failing tests**

`tests/test_cli_v02.py`:
```python
import json
import re
from pathlib import Path

import pytest

import shot
import vl
from common import load_json
from helpers.fake_logs import ClaudeSession

LEDGER = {"evidence": {}, "promises": []}
EXPLAIN = {"evidence": {}, "files": {"lib/ai.ts": {
    "purpose_plain": "把文字发给 OpenAI 总结。", "purpose_dev": "Wraps `summarize` around the OpenAI client.",
    "functions": [{"name": "summarize", "line": 3, "plain": "把文字发出去，取回总结"},
                  {"name": "sendEmail", "line": 9, "plain": "发邮件"}]}}}
OVERLAP_DOM = ('<body data-layout="done"><svg><g class="vlg-node" data-id="app/page.tsx" data-x="0" data-y="0" '
               'data-w="236" data-h="58" data-dim="0"></g><g class="vlg-node sel" data-id="lib/ai.ts" data-x="100" '
               'data-y="20" data-w="236" data-h="58" data-dim="0"></g></svg></body>')


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("VIBE_LEDGER_HOME", str(tmp_path / "home"))
    monkeypatch.setenv("VIBE_LEDGER_OUT_DIR", str(tmp_path / "out"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    return tmp_path


def write(root, rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def make_app(tmp_path, name="app"):
    """app/page.tsx (Next.js entry) and lib/util.ts both use lib/ai.ts, which calls OpenAI."""
    app = tmp_path / name
    write(app, "app/page.tsx", 'import { summarize } from "../lib/ai";\nexport default function Page() {\n  return summarize("x");\n}\n')
    write(app, "lib/ai.ts", 'import OpenAI from "openai";\nconst client = new OpenAI();\n'
                            'export async function summarize(text) {\n  return client.responses.create({ input: text });\n}\n')
    write(app, "lib/util.ts", 'import { summarize } from "./ai";\nexport const twice = (t) => summarize(t + t);\n')
    write(app, "package.json", json.dumps({"dependencies": {"next": "14", "openai": "4"}}))
    s = ClaudeSession(app, "s1")
    s.user("帮我做一个把文字总结成一句话的网页")
    s.edit(app / "lib/ai.ts", "return text;", "return client.responses.create({ input: text });")
    s.save(tmp_path / "claude" / "projects")
    return app


def start(app):
    assert vl.main(["start", "--project", str(app)]) == 0
    return vl.latest_run(app)


def put(run, name, doc):
    (run / name).write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")


def through_render(app):
    run = start(app)
    put(run, "ledger.json", LEDGER)
    put(run, "explain.json", EXPLAIN)
    assert vl.main(["check", "--project", str(app)]) == 0
    assert vl.main(["render", "--project", str(app)]) == 0
    return run


def test_start_writes_graph_and_explain_pack(env, capsys):
    run = start(make_app(env))
    out = capsys.readouterr().out
    g = load_json(run / "graph.json")
    assert {n["id"] for n in g["nodes"]} == {"app/page.tsx", "lib/ai.ts", "lib/util.ts"}
    assert [x["id"] for x in g["externals"]] == ["ext:openai"]
    assert "### lib/ai.ts" in (run / "explain_pack.md").read_text(encoding="utf-8")
    stats = load_json(run / "run.json")["graph"]
    assert stats["files"] == 3 and stats["externals"] == 1 and stats["explain_groups"] == 1
    assert "File graph: 3 files" in out and str(run / "explain.json") in out and "explain-guide.md" in out
    assert vl.top_file(g) == "lib/ai.ts"


def test_start_with_many_files_asks_for_explain_parts(env, capsys):
    app = env / "many"
    write(app, "src/main.ts", "".join(f'import "./m{i}";\n' for i in range(10)))
    for i in range(10):
        write(app, f"src/m{i}.ts", f"export function f{i}() {{}}\n")
    run = start(app)
    out = capsys.readouterr().out
    assert load_json(run / "run.json")["graph"]["explain_groups"] == 2
    assert "explain_NN.json" in out and "merge --project" in out and "check --project" in out


def test_merge_combines_explanation_parts(env, capsys):
    run = start(make_app(env))
    parts = run / "parts"
    parts.mkdir()
    put(parts, "explain_01.json", EXPLAIN)
    put(parts, "explain_02.json", {"evidence": {}, "files": {
        "lib/ai.ts": {"purpose_plain": "第二份，应被跳过"},
        "app/page.tsx": {"purpose_plain": "首页，调用总结功能。"}}})
    capsys.readouterr()
    assert vl.main(["merge", "--project", str(env / "app")]) == 0
    merged = load_json(run / "explain.json")
    assert set(merged["files"]) == {"lib/ai.ts", "app/page.tsx"} and merged["duplicates"] == ["lib/ai.ts"]
    assert merged["files"]["lib/ai.ts"]["purpose_plain"] == "把文字发给 OpenAI 总结。"
    out = capsys.readouterr().out
    assert "Merged 2 explanation parts" in out and "check --project" in out
    assert not (run / "ledger.json").exists()


def test_merge_reports_bad_explanation_parts(env, capsys):
    run = start(make_app(env))
    (run / "parts").mkdir()
    put(run / "parts", "explain_01.json", {"files": {"lib/ai.ts": {}}})
    capsys.readouterr()
    assert vl.main(["merge", "--project", str(env / "app")]) == 2
    assert "purpose_plain must be a non-empty string" in capsys.readouterr().out


def test_check_lists_explain_problems_then_drops_invented_functions(env, capsys):
    app = make_app(env)
    run = start(app)
    put(run, "ledger.json", LEDGER)
    put(run, "explain.json", {"files": {"lib/ai.ts": {"functions": []}}})
    capsys.readouterr()
    assert vl.main(["check", "--project", str(app)]) == 2
    assert "purpose_plain must be a non-empty string" in capsys.readouterr().out
    put(run, "explain.json", EXPLAIN)
    assert vl.main(["check", "--project", str(app)]) == 0
    out = capsys.readouterr().out
    assert "Functions dropped: 1" in out and "sendEmail — not defined in this file" in out and "render --project" in out
    kept = load_json(run / "explain.verified.json")["files"]["lib/ai.ts"]["functions"]
    assert [f["name"] for f in kept] == ["summarize"]


def test_check_needs_explain_json_and_render_needs_a_passing_check(env, capsys):
    app = make_app(env)
    run = through_render(app)
    (run / "explain.json").unlink()
    capsys.readouterr()
    assert vl.main(["check", "--project", str(app)]) == 2
    out = capsys.readouterr().out
    assert "explain.json does not exist yet" in out and "explain_pack.md" in out
    assert not (run / "explain.verified.json").exists()
    assert vl.main(["render", "--project", str(app)]) == 2


def test_check_on_a_run_without_graph_asks_to_start_again(env, capsys):
    app = make_app(env)
    run = start(app)
    put(run, "ledger.json", LEDGER)
    put(run, "explain.json", EXPLAIN)
    (run / "graph.json").unlink()
    capsys.readouterr()
    assert vl.main(["check", "--project", str(app)]) == 2
    out = capsys.readouterr().out
    assert "older version" in out and "start --project" in out


def test_render_builds_the_flowchart_page(env, capsys):
    run = through_render(make_app(env))
    html = (run / "report.html").read_text(encoding="utf-8")
    assert 'class="vl-tabs"' in html and 'id="vl-data"' in html and html.count("var dagre=") == 1
    assert "把文字发给 OpenAI 总结。" in html and "sendEmail" not in html


def test_project_without_code_files_still_renders(env, capsys):
    app = env / "bare"
    write(app, "index.html", "<h1>hi</h1>")
    run = start(app)
    assert "File graph: 0 files" in capsys.readouterr().out
    put(run, "ledger.json", LEDGER)
    put(run, "explain.json", {"evidence": {}, "files": {}})
    assert vl.main(["check", "--project", str(app)]) == 0
    assert vl.main(["render", "--project", str(app)]) == 0
    assert '"g_no_files"' in (run / "report.html").read_text(encoding="utf-8")


def test_shot_passes_the_top_file_and_reports_overlaps(env, capsys, monkeypatch):
    app = make_app(env)
    through_render(app)
    seen = {}

    def fake_shots(report, out_dir, chrome, select=None):
        seen["select"] = select
        return [Path(out_dir) / "desktop.png"]
    monkeypatch.setattr(shot, "find_chrome", lambda: "/fake/chrome")
    monkeypatch.setattr(shot, "take_shots", fake_shots)
    monkeypatch.setattr(shot, "dump_dom", lambda chrome, url, timeout=90: OVERLAP_DOM)
    capsys.readouterr()
    assert vl.main(["shot", "--project", str(app)]) == 1
    out = capsys.readouterr().out
    assert seen["select"] == "lib/ai.ts"
    assert "Layout check FAILED" in out and "app/page.tsx ↔ lib/ai.ts" in out
    monkeypatch.setattr(shot, "dump_dom", lambda chrome, url, timeout=90: "")
    assert vl.main(["shot", "--project", str(app)]) == 1
    assert "did not finish drawing" in capsys.readouterr().out


def test_shots_in_a_real_browser(env, capsys):
    if not shot.find_chrome():
        pytest.skip("Chrome/Chromium not available")
    app = make_app(env)
    through_render(app)
    capsys.readouterr()
    assert vl.main(["shot", "--project", str(app)]) == 0
    out = capsys.readouterr().out
    names = {Path(m.strip()).name for m in re.findall(r"Screenshot: (.+)", out)}
    assert names == {"desktop.png", "desktop-dark.png", "phone-390.png", "selected.png", "overview.png"}
    assert "none overlap; selected lib/ai.ts" in out
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_cli_v02.py`
Expected: FAIL — `graph.json` does not exist after `start`, `vl` has no `top_file`, and `check` still passes without `explain.json`.

- [ ] **Step 3: Replace `take_shots` in `scripts/shot.py`**

Change the module docstring's first sentence to `"""Screenshot a rendered report in headless Chrome: the flowchart (desktop, dark, a selected file), the overview tab, and a true 390 px phone width (macOS headless Chrome will not go narrower than 500 px, so the phone view is a 390 px iframe inside a 500 px window)."""`, add `from urllib.parse import quote` to the imports, add below `NAMES`:
```python
GRAPH_W, GRAPH_H = 1400, 900  # the flowchart fills the window, so it is shot at a normal screen size
PHONE_H = 1400  # tall enough to show the stacked graph (55 vh) and the top of the panel
```
and replace `take_shots` with:
```python
def take_shots(report: Path, out_dir: Path, chrome: str, select: str | None = None, height: int = 6000) -> list[Path]:
    report = Path(report).resolve()
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    url = report.as_uri()
    sel = f"?select={quote(select, safe='/')}" if select else ""
    phone_page = out_dir / "phone.html"
    phone_page.write_text(
        '<!doctype html><meta charset="utf-8"><body style="margin:0">'
        f'<iframe src="{url}{sel}" style="width:390px;height:{PHONE_H}px;border:0"></iframe>',
        encoding="utf-8")
    jobs = [(url, "desktop.png", GRAPH_W, GRAPH_H),
            (url + "?theme=dark", "desktop-dark.png", GRAPH_W, GRAPH_H),
            (phone_page.as_uri(), "phone-390.png", 500, PHONE_H)]
    if select:
        jobs.append((url + sel, "selected.png", GRAPH_W, GRAPH_H))
    jobs.append((url + "?tab=overview", "overview.png", 1280, height))
    return [out_dir / name for u, name, w, h in jobs if _shoot(chrome, u, out_dir / name, w, h)]
```

- [ ] **Step 4: Change `scripts/vl.py`**

Imports — add `from urllib.parse import quote` with the stdlib imports, and with the project imports:
```python
import explain  # noqa: E402
import graph  # noqa: E402
from ledger_report import graph_page  # noqa: E402
```
Below `GUIDE` add:
```python
EXPLAIN_GUIDE = SELF.parent.parent / "references" / "explain-guide.md"
```

Add these helpers below `unattributed`:
```python
def graph_stats(g: dict) -> dict:
    chosen = sum(1 for n in g["nodes"] if n["explain"])
    return {"files": len(g["nodes"]), "edges": len(g["edges"]), "externals": len(g["externals"]),
            "entries": len(g["entries"]), "explain": chosen, "explain_groups": -(-chosen // graph.EXPLAIN_CHUNK),
            "collapsed": g["collapsed"], "unresolved": len(g["unresolved"]), "excluded": g["excluded"]}


def top_file(g: dict) -> str | None:
    ranked = sorted(g.get("nodes", []), key=lambda n: (-n["score"], n["id"]))
    return ranked[0]["id"] if ranked else None
```

In `do_start`, right after `write_json(run / "probes.json", pr)` add:
```python
    g = graph.build(root, recs, pr)
    write_json(run / "graph.json", g)
    (run / "explain_pack.md").write_text(graph.explain_pack(g, root, pr), encoding="utf-8")
```
and add `"graph": graph_stats(g),` to `manifest` after the `"probes"` entry.

Replace `_print_start` from the line `if r["days"] < 365 ...` to the end of the function with:
```python
    gs = m["graph"]
    print(f"File graph: {gs['files']} files, {gs['edges']} links, {gs['externals']} outside services, "
          f"{gs['entries']} entry points" + ("; large project, so folders start collapsed" if gs["collapsed"] else ""))
    if gs["unresolved"]:
        print(f"Imports that could not be resolved: {gs['unresolved']} (listed in {run / 'graph.json'})")
    print(f"Files to explain: {gs['explain']}" + (f" in {gs['explain_groups']} groups" if gs["explain_groups"] > 1 else ""))
    if r["days"] < 365 and s["by_agent"].get("claude-code"):
        print("NEXT (only after the user agrees — it edits their Claude Code settings):")
        print("  " + cmd("retention", "--set", 365))
    parts, pack = run / "parts", run / "explain_pack.md"
    print("NEXT: write two files, then run the checks.")
    if len(m["packs"]) == 1:
        print(f"  1. Ledger: read {run / m['packs'][0]}, {run / 'probes.json'} and the project code; write "
              f"{run / 'ledger.json'} as {GUIDE} describes.")
    else:
        print(f"  1. Ledger: give each reading pack in {run} to its own subagent (or do them one by one). Each writes "
              f"{parts}/part_NN.json with evidence, promises and compromises only ({GUIDE}). After the merge below, "
              f"add map, access and paths to {run / 'ledger.json'}.")
    if gs["explain_groups"] > 1:
        print(f"  2. Explanations: give each group in {pack} to its own subagent (or do them one by one). Each writes "
              f"the {parts}/explain_NN.json named in its heading, as {EXPLAIN_GUIDE} describes.")
    else:
        print(f"  2. Explanations: read {pack} and the files it lists; write {run / 'explain.json'} as "
              f"{EXPLAIN_GUIDE} describes.")
    if len(m["packs"]) > 1 or gs["explain_groups"] > 1:
        print("Merge the parts:")
        print("  " + cmd("merge", "--project", root))
    print("Then run:")
    print("  " + cmd("check", "--project", root))
```

Replace `do_merge` with:
```python
def do_merge(args) -> int:
    root = _root(args)
    run = latest_run(root)
    parts_dir = Path(args.parts_dir) if args.parts_dir else run / "parts"
    ledger_files = sorted(parts_dir.glob("part_*.json"))
    explain_files = sorted(parts_dir.glob("explain_*.json"))
    if not ledger_files and not explain_files:
        print(f"error: no part_*.json or explain_*.json files in {parts_dir}")
        return 2
    docs = {}
    for f in ledger_files + explain_files:
        try:
            docs[f] = load_json(f)
        except json.JSONDecodeError as exc:
            print(f"error: {f.name} is not valid JSON: {exc}")
            return 2
    if ledger_files:
        try:
            led = merge([docs[f] for f in ledger_files])
        except LedgerError as exc:
            print("The parts do not match the ledger format:")
            for problem in exc.problems:
                print("  -", problem)
            return 2
        write_json(run / "ledger.json", led)
        print(f"Merged {len(ledger_files)} parts: {len(led['promises'])} promises, {len(led['compromises'])} "
              f"compromises → {run / 'ledger.json'}")
    if explain_files:
        try:
            exp = explain.merge([docs[f] for f in explain_files])
        except explain.ExplainError as exc:
            print(f"The explanation parts do not match the explain.json format ({EXPLAIN_GUIDE}):")
            for problem in exc.problems:
                print("  -", problem)
            return 2
        write_json(run / "explain.json", exp)
        dup = f"; explained twice, kept the first: {', '.join(exp['duplicates'])}" if exp["duplicates"] else ""
        print(f"Merged {len(explain_files)} explanation parts: {len(exp['files'])} files{dup} → {run / 'explain.json'}")
    if ledger_files:
        print(f"NEXT: add map, access and paths from the code ({GUIDE}), then run:")
    else:
        print("NEXT: run:")
    print("  " + cmd("check", "--project", root))
    return 0
```

In `do_check`, replace everything after `write_json(run / "ledger.verified.json", out)` to the end of the function (the summary loop, the two NEXT prints and `return 0`) with the following, and add `_check_explain` below it:
```python
    for line in verify.summary_lines(out):
        print(line)
    code = _check_explain(args, root, run, index)
    if code:
        return code
    print("NEXT: if a quote, snippet or function line failed only because it was mis-copied, fix it from the real "
          "text and run check again. Otherwise run:")
    print("  " + cmd("render", "--project", root))
    return 0


def _check_explain(args, root: Path, run: Path, index: dict) -> int:
    verified = run / "explain.verified.json"
    verified.unlink(missing_ok=True)  # never let render use explanations from an earlier check
    again = "  " + cmd("check", "--project", root)
    if not (run / "graph.json").exists():
        print("error: this run has no graph.json (it was started by an older version of vibe-ledger). Start again:\n"
              "  " + cmd("start", "--project", root))
        return 2
    path = Path(args.explain) if args.explain else run / "explain.json"
    if not path.exists():
        print(f"error: {path} does not exist yet. The flowchart needs it: write it from {run / 'explain_pack.md'} as "
              f"{EXPLAIN_GUIDE} describes (or merge parts/explain_NN.json), then run:\n{again}")
        return 2
    try:
        doc = load_json(path)
    except json.JSONDecodeError as exc:
        print(f"error: {path} is not valid JSON: {exc}")
        return 2
    try:
        out = explain.verify(doc, load_json(run / "graph.json"), root, index)
    except explain.ExplainError as exc:
        print(f"{path.name} does not match the format ({EXPLAIN_GUIDE}):")
        for problem in exc.problems:
            print("  -", problem)
        print("NEXT: fix these, then run:\n" + again)
        return 2
    write_json(verified, out)
    for line in explain.summary_lines(out):
        print(line)
    return 0
```

Replace `do_render` with:
```python
def do_render(args) -> int:
    root = _root(args)
    run = latest_run(root)
    verified, explained = run / "ledger.verified.json", run / "explain.verified.json"
    if not verified.exists() or not explained.exists():
        print("error: run check first; it has to pass for both ledger.json and explain.json:\n  "
              + cmd("check", "--project", root))
        return 2
    manifest = load_json(run / "run.json")
    lang = args.lang or manifest["lang"]
    ledger_doc, probes_doc = load_json(verified), load_json(run / "probes.json")
    data = graph_page.page_data(load_json(run / "graph.json"), load_json(explained), ledger_doc, probes_doc, root,
                                lang, bool(manifest.get("sessions", {}).get("records")))
    html = render.render_html(ledger_doc, manifest, probes_doc, lang, graph_data=data)
    out = render.deliver(html, run, manifest["project_name"], args.out_dir)
    manifest["report_path"] = str(out)
    write_json(run / "run.json", manifest)
    print(f"Report: {out}")
    print("NEXT: take screenshots and look at the flowchart, a selected file and the overview before telling the "
          "user it is done:")
    print("  " + cmd("shot", "--project", root))
    return 0
```

Replace `do_shot` with (and add `_print_layout` below it):
```python
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
    top = top_file(load_json(run / "graph.json")) if (run / "graph.json").exists() else None
    paths = shot.take_shots(Path(report), run / "shots", chrome, select=top)
    for p in paths:
        print(f"Screenshot: {p}")
    if not paths:
        print(f"Chrome did not produce screenshots. Open the report and look: {report}")
        return 1
    url = Path(report).resolve().as_uri() + (f"?select={quote(top, safe='/')}" if top else "")
    ok = _print_layout(shot.layout_report(shot.dump_dom(chrome, url)), top)
    print("NEXT: open every screenshot and check: the flowchart reads left to right and no cards overlap; the "
          "selected file's panel explains it; the overview diagrams are readable and the counts match the ledger; "
          "the phone view has no text running off the edge. Fix and re-render if not.")
    return 0 if ok else 1


def _print_layout(rep: dict, top: str | None) -> bool:
    if not rep["done"]:
        print("Layout check: the flowchart did not finish drawing in headless Chrome. Open the report and look; "
              "a script error is the usual cause.")
        return False
    if rep["overlaps"]:
        pairs = "; ".join(f"{a} ↔ {b}" for a, b in rep["overlaps"][:10])
        print(f"Layout check FAILED: {len(rep['overlaps'])} pairs of cards overlap: {pairs}")
        return False
    if top and rep["selected"] != [top]:
        print(f"Layout check FAILED: opening the page with ?select={top} selected {rep['selected'] or 'nothing'}")
        return False
    sel = f"; selected {top}" if top else ""
    print(f"Layout check: {len(rep['nodes'])} cards drawn, none overlap{sel}.")
    return True
```

In `main`, add to the `check` parser:
```python
    p.add_argument("--explain")
```

- [ ] **Step 5: Give the v0.1 tests an `explain.json`**

`check` now refuses to pass without one. In `tests/test_cli.py`, add below `minimal_ledger`:
```python
EMPTY_EXPLAIN = {"evidence": {}, "files": {}}
```
and, in `test_start_prints_runnable_next_commands_for_unusual_path` and `test_shot_without_chrome_says_so`, directly after the line that writes `ledger.json`, add:
```python
    (vl.latest_run(app) / "explain.json").write_text(json.dumps(EMPTY_EXPLAIN), encoding="utf-8")
```
In `tests/test_e2e_deterministic.py` `test_fabricated_ledger_draws_nothing_and_counts_nothing`, directly after the line that writes `ledger.json`, add:
```python
    (run / "explain.json").write_text(json.dumps({"evidence": {}, "files": {}}), encoding="utf-8")
```

- [ ] **Step 6: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_cli_v02.py tests/test_cli.py tests/test_e2e_deterministic.py`
Expected: PASS (`test_shots_in_a_real_browser` runs here — Chrome is installed on this machine; it takes about 20 s).

- [ ] **Step 7: Run the whole suite**

Run: `python3 -m pytest -q`
Expected: PASS, no failures. (`test_version` still expects 0.1.0; Task 7 changes the version.)

- [ ] **Step 8: Commit**

```bash
git add scripts/vl.py scripts/shot.py tests/test_cli_v02.py tests/test_cli.py tests/test_e2e_deterministic.py
git commit -m "feat(cli): graph and explain pack at start, explanation merge and check, tabbed render, selected shot and layout check"
```

---
### Task 7: Skill docs, explanation guide, answer keys for the graph, version 0.2.0

**Files:**
- Create: `references/explain-guide.md`
- Modify: `SKILL.md` (replace), `README.md` (two sections), `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `scripts/common.py` (version and description)
- Modify: `tests/fixtures/answers/*.json` (add `graph` and `explain`), `tests/e2e/score.py` (add `score_graph`, `score_explain`, two CLI flags)
- Test: `tests/test_docs.py`, `tests/test_packaging.py`, `tests/test_cli.py` (`test_version`), `tests/test_e2e_deterministic.py`

**Interfaces:**
- Consumes: `explain.validate`, `explain.TOLERANCE` (Task 3); `graph.EXPLAIN_MAX`, `graph.EXPLAIN_CHUNK`, `graph.build` output (Tasks 1–2); `vl.py` commands and messages (Task 6).
- Produces:
  - `references/explain-guide.md` — the rules `check` enforces, with a worked example that `explain.validate` accepts.
  - `e2e.score.score_graph(g, want) -> list[(bool, str)]` and `e2e.score.score_explain(explained, g, want) -> list[(bool, str)]`; `score.py --graph <run>/graph.json --explained <run>/explain.verified.json`.
  - Answer keys: `"graph": {"nodes", "entries", "externals", "edges"}` and `"explain": [{"path", "label", "text_any"}]`.
  - Version `0.2.0` everywhere.

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_docs.py`:
```python
def test_explain_guide_example_is_valid_and_named_in_skill():
    import json

    import explain
    block = re.search(r"`{3}json\n(.+?)\n`{3}", REFS["explain-guide.md"], re.S).group(1)
    explain.validate(json.loads(block))
    assert "references/explain-guide.md" in SKILL and "explain.json" in SKILL and "vl.py merge" in SKILL


def test_explain_guide_states_the_checked_limits():
    import explain
    import graph
    text = REFS["explain-guide.md"]
    assert f"±{explain.TOLERANCE}" in text and f"at most {graph.EXPLAIN_MAX}" in text
    assert f"more than {graph.EXPLAIN_CHUNK} files" in text
```

In `tests/test_packaging.py` change `assert versions == {"0.1.0"}` to `assert versions == {"0.2.0"}`. In `tests/test_cli.py` `test_version`, change `"0.1.0"` to `"0.2.0"`.

In `tests/test_e2e_deterministic.py`, change the scorer import to `from e2e.score import score, score_explain, score_graph` and append:
```python
@pytest.mark.parametrize("name", list(SCENARIOS))
def test_graph_matches_the_answer_key(prepared, name, tmp_path, monkeypatch, capsys):
    f, run = start(prepared, name, tmp_path, monkeypatch)
    results = score_graph(load_json(run / "graph.json"), load_json(ANSWERS / f"{name}.json")["graph"])
    assert all(ok for ok, _ in results), [label for ok, label in results if not ok]


def test_graph_and_explain_scores_fail_as_expected():
    g = {"nodes": [{"id": "a.ts", "explain": True}, {"id": "b.ts", "explain": False}], "externals": [{"id": "ext:openai"}],
         "entries": [{"path": "a.ts"}], "edges": [{"from": "a.ts", "to": "ext:openai"}]}
    want = {"nodes": ["a.ts", "b.ts"], "entries": ["a.ts"], "externals": ["ext:openai"], "edges": [["a.ts", "ext:openai"]]}
    assert all(ok for ok, _ in score_graph(g, want))
    assert not all(ok for ok, _ in score_graph(g, {**want, "edges": [["b.ts", "a.ts"]]}))
    assert not all(ok for ok, _ in score_graph(g, {**want, "entries": ["b.ts"]}))
    explained = {"files": {"a.ts": {"purpose_plain": "把文字发给 OpenAI 总结", "purpose_dev": ""}}, "rejected": [],
                 "verification": {"functions_dropped": 0, "unverified_purposes": 0}}
    keys = [{"path": "a.ts", "label": "calls OpenAI", "text_any": ["openai"]}]
    assert all(ok for ok, _ in score_explain(explained, g, keys))
    assert not all(ok for ok, _ in score_explain({**explained, "files": {}}, g, keys))
    dropped = {**explained, "verification": {"functions_dropped": 1, "unverified_purposes": 0}}
    assert not all(ok for ok, _ in score_explain(dropped, g, keys))
    rejected = {**explained, "rejected": [{"path": "zzz.ts", "reason": "not a file in the graph"}]}
    assert not all(ok for ok, _ in score_explain(rejected, g, keys))
```

- [ ] **Step 2: Run the tests to verify they fail**

Run: `python3 -m pytest tests/test_docs.py tests/test_packaging.py tests/test_cli.py::test_version tests/test_e2e_deterministic.py`
Expected: FAIL — `KeyError: 'explain-guide.md'`, version mismatch, `ImportError: cannot import name 'score_explain'`.

- [ ] **Step 3: Write `references/explain-guide.md`**

````markdown
# Writing the explanations

`start` picks the files that matter most — entry points, files with check findings, files many others use; at most 30 — and lists them in `<run>/explain_pack.md`. You write `<run>/explain.json`: what each of those files does, its main functions, and, when the conversations show it, how it came to be. Every other file gets an automatic summary. The flowchart's side panel shows what you write, after `check` has verified it.

## 1. Read

For each file in the pack, read its lines in the pack (role, exports, what it uses, who uses it, check findings) and then **the whole file**. Never explain a file you have not opened.

## 2. Write one entry per file

- `purpose_plain` — one or two sentences for someone who cannot read code: what the file does for the person using the app, and where data goes (which store, which outside service). Say "your notes", "the AI service", "the database" — not function names. Write in the run's language (`lang` in `run.json`).
- `purpose_dev` — one sentence for a developer naming the mechanism, with identifiers in backticks (`createClient`, `lib/supabase.ts`). **Every backticked name must exist in the project.** If one does not, the purpose is shown as unverified.
- `functions` — the 2–5 functions a reader most needs, each `{"name", "line", "plain"}`:
  - `name` exactly as this file defines it: a function, an arrow function or function expression assigned to a name, a class, a class method or an object method. Not something the file only imports or calls.
  - `line` — the line where that definition starts. `check` accepts ±3 lines, corrects the line of a name defined only once in the file, and drops any other name with the reason.
  - `plain` — one sentence in plain words.
  - A file with no functions of its own (markup, a config object, one exported client) gets `"functions": []`.
- `history` (optional) — only when the reading packs show how the file came about: `{"plain": "…", "evidence": ["H1"]}`. Each id points to a transcript quote in the top-level `evidence` map, copied word for word from a reading pack under the same rules as the ledger (references/extraction-guide.md): `msg_id` is the `[ID]` in the pack's header line and the quote is at least 4 characters. Items whose quotes fail are dropped. With no conversations, leave `history` out.

Do not write risks here. They come from the probes and the verified ledger and are attached to each file automatically.

## 3. Paths, groups and empty packs

- Use paths exactly as the pack prints them (relative to the project, forward slashes). An entry whose path is not in the graph is rejected as a whole.
- When the pack lists more than 8 files it splits them into groups. Each group writes `<run>/parts/explain_NN.json` in this same format (give each group to its own subagent, or do them one by one); evidence ids only need to be unique within one part. `vl.py merge` combines the parts into `explain.json`; a file explained twice keeps the first explanation.
- When the pack lists no files, write `{"evidence": {}, "files": {}}` — `check` needs the file to exist.

## 4. Example

```json
{
  "evidence": {
    "H1": {"kind": "transcript", "session": "s1", "msg_id": "u-3", "quote": "帮我加一个总结按钮，用 OpenAI"}
  },
  "files": {
    "app/api/summarize/route.ts": {
      "purpose_plain": "你点“总结”时，这个文件把你的笔记发给 OpenAI，再把它写的总结送回页面。",
      "purpose_dev": "Next.js route handler: `POST` reads `notes` from the request body and asks OpenAI for a summary.",
      "functions": [{"name": "POST", "line": 5, "plain": "收到页面发来的笔记，请 OpenAI 写总结并返回"}],
      "history": [{"plain": "你要求加一个用 OpenAI 的总结按钮，AI 随后写了这个文件。", "evidence": ["H1"]}]
    },
    "lib/supabase.ts": {
      "purpose_plain": "连接存放笔记的数据库（Supabase），其他文件都通过它读写笔记。",
      "purpose_dev": "Creates the shared client with `createClient` from the public URL and anon key.",
      "functions": []
    }
  }
}
```

## 5. What `check` does with it

- A format problem (missing `purpose_plain`, a line that is not a number, an unknown evidence id) is listed and `check` exits with code 2. Fix it and run `check` again.
- Function names are looked up in the file: kept, line-corrected or dropped. Backticked names are looked up in the project. History quotes are looked up in the conversations.
- The result goes to `explain.verified.json`, which `render` uses. Fix a mis-copied line or quote only by copying from the real file or message; a dropped name is the honest result, not something to work around.
````

- [ ] **Step 4: Replace `SKILL.md`**

````markdown
---
name: vibe-ledger
description: Explain an AI-built ("vibe-coded") app to the person who made it and check it at the same time. Draws the project's files as an interactive flowchart — click a file to read what it does, what calls it, its main functions, its risks and how it came to be — and, from the Claude Code and Codex conversations that built it, keeps a ledger of what was asked for, claimed and put off, each checked against verified code evidence. Renders one offline HTML page (flowchart plus an overview with app map, who-can-see matrix, conversation timeline and call paths). Use when someone wants to understand or sanity-check an app an AI wrote — "explain my app", "how do my files connect", "what did the AI actually build", "is my vibe-coded app safe", "帮我看懂这个 AI 写的项目", "这些文件之间怎么调用的", "检查一下 AI 写的代码有没有问题". Runs locally and sends nothing anywhere.
---

# vibe-ledger

Draws the project's files as a flowchart the user can click through, and turns *what was asked, claimed and put off* into a ledger of promises checked against the code. **Every conclusion carries evidence a script verifies. Anything that fails verification shows as ❓ or "unverified" — it is never shown as fact.**

## Rules

1. **Never invent evidence.** Copy quotes character for character from a reading pack, and code snippets from the file. `check` rejects anything else, and the report shows the rejection.
2. **Only the five questions** (references/five-questions.md): where data lives, what costs money, who can see it, where it is most likely to break, what was put off. Leave cosmetic and feature requests out of the ledger.
3. **A status other than `unknown` needs code or probe evidence.** When unsure, write `unknown`.
4. **Two voices.** Plain text is for someone who cannot read code (an analogy only if it is accurate); dev text names the file and the mechanism. Write both in the run's language (`lang` in `run.json`).
5. **Explanations name only what exists.** Function names are copied from their definitions; a name goes in backticks only if it is in the project. Describe what a file does, not what it should do.
6. **Ask before `retention --set`.** It edits the user's Claude Code settings.
7. **Transcripts are private.** Quote only what a promise or a file's history needs. The digest is already masked; never unmask or repeat a secret.

## Steps

Run everything as `python3 <this skill's folder>/scripts/vl.py …`. Each step prints the exact next command — run it as printed.

1. **Start** — `vl.py start --project <app folder>`. It finds the conversations, writes reading packs, runs the probes, builds the file graph and writes `explain_pack.md`. Read its summary: conversations, candidates, probes, file graph, files to explain, warnings. If it prints a retention line, ask the user (rule 6).
2. **Ledger** — follow references/extraction-guide.md.
   - One reading pack: read it, `probes.json`, `candidates.json` and the code it points at; write `<run>/ledger.json`.
   - Several packs: give each pack to its own subagent (or work through them one by one) → `<run>/parts/part_NN.json` with evidence, promises and compromises only.
3. **Explanations** — follow references/explain-guide.md.
   - One group (8 files or fewer): read `explain_pack.md` and every file it lists; write `<run>/explain.json`.
   - Several groups: give each group to its own subagent → `<run>/parts/explain_NN.json`.
4. **Merge** (only if step 2 or 3 wrote parts) — `vl.py merge --project <app folder>`. It merges both kinds of part. Then add `map`, `access` and `paths` to `<run>/ledger.json` yourself.
5. **Check** — `vl.py check --project <app folder>`. It verifies `ledger.json` and `explain.json`; it stops if either is missing or malformed. Fix a failed quote, snippet or function line only by copying the real text. Downgrades to ❓, dropped function names and "unverified" purposes are the honest result, not something to work around.
6. **Render** — `vl.py render --project <app folder>`.
7. **Look** — `vl.py shot --project <app folder>`. It must print `Layout check: … none overlap`. Then open every screenshot: the flowchart reads left to right with no overlapping cards; the selected file's panel explains it; the overview diagrams say what the ledger says; nothing runs off the edge at phone width. Fix and re-render if not. If no browser is available, open the HTML and read it.
8. **Tell the user** — the report path; how to read it (start on the flowchart, click a file, red cards have problems); the counts (✅ ❌ ⚠️ ⏳ ❓); the three most important problems in plain words, each with the fix it suggests; and what the report could not see (the overview's last section).

## When there are no conversations

`start` says so. Leave `promises` empty, still record `map`, `access` and `paths` from the code, write `explain.json` without `history`, and tell the user the report checked the code only.

## Reference

- references/extraction-guide.md — how to write the ledger, with a worked example
- references/explain-guide.md — how to write the file explanations, with a worked example
- references/ledger-schema.md — every ledger field
- references/five-questions.md — what belongs under each question
- references/probes.md — what each probe checks and where it is blind
- references/candidates.md — how candidates are found
````

- [ ] **Step 5: Update `README.md`**

Replace the first paragraph's ending "— with diagrams and evidence." with "— with a clickable flowchart of your files, diagrams and evidence." Replace the `## What you get` list's first line with these two lines (keep the rest of the list):
```markdown
- **File flowchart** — every file as a card, laid out left to right from entry points through logic to data and outside services; arrows mean "calls". Click a file to read what it does, what calls it, its main functions, its risks and how it came to be. Red cards have problems; ✦ marks services that charge per use.
- **App map** — browser, your server, storage and outside services; 💰 marks what charges per use; red marks risk.
```
In `## Use`, replace the code block with:
```
python3 scripts/vl.py start  --project <your app folder>
# the agent writes ledger.json (from the reading packs) and explain.json (from explain_pack.md)
python3 scripts/vl.py check  --project <your app folder>
python3 scripts/vl.py render --project <your app folder>
python3 scripts/vl.py shot   --project <your app folder>
```
In `## Limits`, add the line `- The flowchart covers JS/TS and Python files and static imports; it does not trace what runs at runtime.`

- [ ] **Step 6: Bump the version to 0.2.0**

- `scripts/common.py`: `__version__ = "0.2.0"`.
- `.claude-plugin/plugin.json`: `"version": "0.2.0"` and `"description": "Explain an AI-built app to the person who made it and check it at the same time: an interactive flowchart of the project's files (click one to read what it does, who calls it, its risks and history), plus a ledger of what was asked, claimed and put off in the Claude Code / Codex conversations, each verified against the code. One offline HTML page. Local only."`
- `.claude-plugin/marketplace.json`: both `"version"` values → `"0.2.0"`.

- [ ] **Step 7: Add the graph and explanation expectations to the answer keys**

Add these two top-level keys to each answer file (inside its outer object, after `"deterministic"`):

`tests/fixtures/answers/notes-supabase.json`:
```json
  "graph": {"nodes": ["app/api/summarize/route.ts", "app/page.tsx", "lib/supabase.ts"],
            "entries": ["app/api/summarize/route.ts", "app/page.tsx"],
            "externals": ["ext:openai", "ext:supabase"],
            "edges": [["app/page.tsx", "lib/supabase.ts"], ["app/api/summarize/route.ts", "ext:openai"],
                      ["lib/supabase.ts", "ext:supabase"]]},
  "explain": [{"path": "app/api/summarize/route.ts", "label": "sends the notes to OpenAI", "text_any": ["openai", "总结", "summar"]},
              {"path": "lib/supabase.ts", "label": "connects to the database", "text_any": ["supabase", "数据库", "database"]}],
```
`tests/fixtures/answers/chat-express.json`:
```json
  "graph": {"nodes": ["server.js"], "entries": ["server.js"], "externals": ["ext:openai"],
            "edges": [["server.js", "ext:openai"]]},
  "explain": [{"path": "server.js", "label": "relays chat messages to OpenAI", "text_any": ["openai", "chat", "聊天"]}],
```
`tests/fixtures/answers/clean-todos.json`:
```json
  "graph": {"nodes": ["app/page.tsx", "lib/supabase.ts"], "entries": ["app/page.tsx"], "externals": ["ext:supabase"],
            "edges": [["app/page.tsx", "lib/supabase.ts"], ["lib/supabase.ts", "ext:supabase"]]},
  "explain": [{"path": "lib/supabase.ts", "label": "connects to the database", "text_any": ["supabase", "数据库", "database"]}],
```
`tests/fixtures/answers/flask-notes.json`:
```json
  "graph": {"nodes": ["app.py"], "entries": ["app.py"], "externals": ["ext:sqlite"], "edges": [["app.py", "ext:sqlite"]]},
  "explain": [{"path": "app.py", "label": "stores notes in SQLite", "text_any": ["sqlite", "数据库", "database", "note", "笔记"]}],
```
`tests/fixtures/answers/habits-firebase.json`:
```json
  "graph": {"nodes": ["src/App.tsx", "src/firebase.ts"], "entries": ["src/App.tsx"], "externals": ["ext:firebase"],
            "edges": [["src/App.tsx", "src/firebase.ts"], ["src/App.tsx", "ext:firebase"], ["src/firebase.ts", "ext:firebase"]]},
  "explain": [{"path": "src/firebase.ts", "label": "connects to Firebase", "text_any": ["firebase", "firestore", "数据库", "database"]}],
```
If `test_graph_matches_the_answer_key` then fails for a fixture, open that fixture's files and `graph.json` and decide which is wrong: fix `graph.py` (with a unit test in `tests/test_graph_build.py`) when the graph misses a real import, entry or service; fix the answer key only when the key misread the fixture. Record which in the commit message.

- [ ] **Step 8: Add the graph and explanation scores to `tests/e2e/score.py`**

Change the module docstring's usage line to:
```
    python3 tests/e2e/score.py --verified <run>/ledger.verified.json --answers tests/fixtures/answers/<name>.json \
        [--graph <run>/graph.json [--explained <run>/explain.verified.json]]
```
Add below `score`:
```python
def score_graph(g: dict, want: dict) -> list[tuple[bool, str]]:
    ids = {n["id"] for n in g["nodes"]}
    ext = {x["id"] for x in g["externals"]}
    entries = {e["path"] for e in g["entries"]}
    edges = {(e["from"], e["to"]) for e in g["edges"]}
    missing = [e for e in want["edges"] if tuple(e) not in edges]
    return [(ids == set(want["nodes"]), f"file nodes: want {sorted(want['nodes'])}, got {sorted(ids)}"),
            (entries == set(want["entries"]), f"entries: want {sorted(want['entries'])}, got {sorted(entries)}"),
            (ext == set(want["externals"]), f"outside services: want {sorted(want['externals'])}, got {sorted(ext)}"),
            (not missing, f"links present (missing: {missing})")]


def score_explain(explained: dict, g: dict, want: list) -> list[tuple[bool, str]]:
    chosen = {n["id"] for n in g["nodes"] if n.get("explain")}
    kept = explained["files"]
    v = explained["verification"]
    results = [(chosen <= set(kept), f"every chosen file is explained (missing: {sorted(chosen - set(kept))})"),
               (not explained["rejected"], f"no explanation rejected ({[r['path'] for r in explained['rejected']]})"),
               (v["functions_dropped"] == 0, f"no invented function names ({v['functions_dropped']} dropped)"),
               (v["unverified_purposes"] == 0, f"purposes name only real identifiers ({v['unverified_purposes']} unverified)")]
    for w in want:
        entry = kept.get(w["path"], {})
        text = f"{entry.get('purpose_plain', '')} {entry.get('purpose_dev', '')}".lower()
        results.append((any(t.lower() in text for t in w["text_any"]), f"explains {w['path']}: {w['label']}"))
    return results
```
In `main`, add after the `--answers` argument:
```python
    ap.add_argument("--graph", help="<run>/graph.json: also score the file graph")
    ap.add_argument("--explained", help="<run>/explain.verified.json: also score the explanations (needs --graph)")
```
and replace `results = score(verified, answers)` with:
```python
    results = score(verified, answers)
    if args.graph:
        with open(args.graph, encoding="utf-8") as fh:
            g = json.load(fh)
        results += score_graph(g, answers["graph"])
        if args.explained:
            with open(args.explained, encoding="utf-8") as fh:
                results += score_explain(json.load(fh), g, answers.get("explain", []))
```

- [ ] **Step 9: Run the tests to verify they pass**

Run: `python3 -m pytest tests/test_docs.py tests/test_packaging.py tests/test_cli.py tests/test_e2e_deterministic.py`
Expected: PASS.

- [ ] **Step 10: Run the whole suite**

Run: `python3 -m pytest -q`
Expected: PASS, no failures.

- [ ] **Step 11: Commit**

```bash
git add references/explain-guide.md SKILL.md README.md .claude-plugin/plugin.json .claude-plugin/marketplace.json scripts/common.py tests/fixtures/answers/notes-supabase.json tests/fixtures/answers/chat-express.json tests/fixtures/answers/clean-todos.json tests/fixtures/answers/flask-notes.json tests/fixtures/answers/habits-firebase.json tests/e2e/score.py tests/test_docs.py tests/test_packaging.py tests/test_cli.py tests/test_e2e_deterministic.py
git commit -m "docs: explanation guide and skill steps for the flowchart; graph answer keys and scores; version 0.2.0"
```

---
### Task 8: End to end — a generated 100-file project, fresh agents on the five fixtures, screenshots, and a rerun on a real project

**Files:**
- Create: `tests/e2e/medium.py` (writes a deterministic ~100-file project)
- Test: `tests/test_e2e_medium.py`
- No product code changes unless a step below finds a defect; each defect gets its own failing test first, in the test file of the module it lives in.

**Interfaces:**
- Consumes: the whole CLI (`vl.py start/merge/check/render/shot`), `shot.dump_dom`, `shot.layout_report`, `e2e.prepare.prepare`, `e2e.score.score/score_graph/score_explain`.
- Produces: `e2e.medium.make_medium(root) -> Path` — 100 source files under `src/{pages,components,lib,api,utils}` plus `src/main.tsx` and an `index.html` that loads it; `src/api/*` call OpenAI and Supabase.

- [ ] **Step 1: Write the failing test**

`tests/test_e2e_medium.py`:
```python
import json

import pytest

import shot
import vl
from common import load_json
from e2e.medium import make_medium


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("VIBE_LEDGER_HOME", str(tmp_path / "home"))
    monkeypatch.setenv("VIBE_LEDGER_OUT_DIR", str(tmp_path / "out"))
    monkeypatch.setenv("CLAUDE_CONFIG_DIR", str(tmp_path / "claude"))
    monkeypatch.setenv("CODEX_HOME", str(tmp_path / "codex"))
    return tmp_path


def test_medium_project_collapses_into_folders(env, capsys):
    app = make_medium(env / "medium")
    assert vl.main(["start", "--project", str(app)]) == 0
    g = load_json(vl.latest_run(app) / "graph.json")
    assert len(g["nodes"]) == 101 and g["collapsed"] is True
    assert [f["id"] for f in g["folders"]] == ["src/api", "src/components", "src/lib", "src/pages", "src/utils"]
    assert {x["id"] for x in g["externals"]} == {"ext:openai", "ext:supabase"}
    assert [e["path"] for e in g["entries"]] == ["src/main.tsx"]
    assert sum(n["explain"] for n in g["nodes"]) == 30
    assert "large project, so folders start collapsed" in capsys.readouterr().out


def test_medium_project_renders_without_overlaps_in_a_real_browser(env, capsys):
    chrome = shot.find_chrome()
    if not chrome:
        pytest.skip("Chrome/Chromium not available")
    app = make_medium(env / "medium")
    assert vl.main(["start", "--project", str(app)]) == 0
    run = vl.latest_run(app)
    (run / "ledger.json").write_text(json.dumps({"evidence": {}, "promises": []}), encoding="utf-8")
    (run / "explain.json").write_text(json.dumps({"evidence": {}, "files": {"src/api/a0.ts": {
        "purpose_plain": "把用户的问题发给 OpenAI。", "functions": [{"name": "ask0", "line": 4, "plain": "发问题"}]}}},
        ensure_ascii=False), encoding="utf-8")
    assert vl.main(["check", "--project", str(app)]) == 0
    assert vl.main(["render", "--project", str(app)]) == 0
    page = (run / "report.html").as_uri()
    closed = shot.layout_report(shot.dump_dom(chrome, page))
    assert closed["done"] and closed["overlaps"] == []
    assert {n["id"] for n in closed["nodes"]} == {"folder:src/api", "folder:src/components", "folder:src/lib",
                                                   "folder:src/pages", "folder:src/utils", "src/main.tsx",
                                                   "ext:openai", "ext:supabase"}
    opened = shot.layout_report(shot.dump_dom(chrome, page + "?select=src/api/a0.ts"))
    assert opened["done"] and opened["overlaps"] == [] and opened["selected"] == ["src/api/a0.ts"]
    assert "folder:src/api" not in {n["id"] for n in opened["nodes"]}
```

- [ ] **Step 2: Run it to verify it fails**

Run: `python3 -m pytest tests/test_e2e_medium.py`
Expected: FAIL — `ModuleNotFoundError: No module named 'e2e.medium'`.

- [ ] **Step 3: Write `tests/e2e/medium.py`**

```python
"""A generated ~100-file Vite + React project for the folder-collapse checks.

    python3 tests/e2e/medium.py --out <folder>"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

COUNTS = {"pages": 12, "components": 30, "lib": 20, "api": 8, "utils": 30}  # 100 files + src/main.tsx


def _write(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def make_medium(root) -> Path:
    root = Path(root)
    _write(root, "index.html", '<!doctype html><div id="root"></div><script type="module" src="/src/main.tsx"></script>\n')
    _write(root, "package.json", '{"dependencies": {"react": "18.3.1", "openai": "4.60.0", "@supabase/supabase-js": "2.45.0"}}\n')
    _write(root, "src/main.tsx", "".join(f'import "./pages/p{i}";\n' for i in range(COUNTS["pages"])))
    for i in range(COUNTS["pages"]):
        _write(root, f"src/pages/p{i}.tsx",
               f'import {{ C{i} }} from "../components/c{i}";\nimport {{ L{i} }} from "../lib/l{i}";\n'
               f"export default function Page{i}() {{\n  return C{i}(L{i}());\n}}\n")
    for i in range(COUNTS["components"]):
        _write(root, f"src/components/c{i}.tsx",
               f'import {{ u{i} }} from "../utils/u{i}";\nexport function C{i}(x) {{\n  return u{i}(x);\n}}\n')
    for i in range(COUNTS["lib"]):
        api = f'import {{ ask{i % COUNTS["api"]} }} from "../api/a{i % COUNTS["api"]}";\n'
        _write(root, f"src/lib/l{i}.ts", f"{api}export function L{i}() {{\n  return ask{i % COUNTS['api']}('q');\n}}\n")
    for i in range(COUNTS["api"]):
        sdk = 'import OpenAI from "openai";\n' if i % 2 == 0 else 'import { createClient } from "@supabase/supabase-js";\n'
        _write(root, f"src/api/a{i}.ts", f"{sdk}\n\nexport async function ask{i}(q) {{\n  return q;\n}}\n")
    for i in range(COUNTS["utils"]):
        _write(root, f"src/utils/u{i}.ts", f"export const u{i} = (x) => x;\n")
    return root


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    print(make_medium(Path(ap.parse_args().out)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```
(`src/api/a0.ts`: line 1 imports OpenAI, lines 2–3 are blank, line 4 defines `ask0` — the line the test's explanation names.)

- [ ] **Step 4: Run it to verify it passes**

Run: `python3 -m pytest tests/test_e2e_medium.py`
Expected: PASS. If the explain count is not 30, check the scores in `graph.json` before touching the test — the medium project has well over 30 files with a score above zero, so `EXPLAIN_MAX` must cap it.

- [ ] **Step 5: Commit**

```bash
git add tests/e2e/medium.py tests/test_e2e_medium.py
git commit -m "test(e2e): generated 100-file project collapses into folders and lays out without overlaps"
```

- [ ] **Step 6: Run the five fixtures with fresh agents**

Prepare the fixtures in the scratchpad (outside the repo):
```bash
python3 tests/e2e/prepare.py --out "$SCRATCH/e2e"
```
It prints one `start` command per fixture (with `--claude-dir` and `--codex-dir`). For each fixture, dispatch one fresh subagent (general-purpose, sonnet) in parallel, with `VIBE_LEDGER_HOME="$SCRATCH/vl-home"` and `VIBE_LEDGER_OUT_DIR="$SCRATCH/out"` set in every command it runs, and this prompt (fill the two placeholders):

> You are using the vibe-ledger skill. Read `<vibe-ledger repo>/SKILL.md` and follow it exactly on this project, starting with this command: `<the start command prepare.py printed for this fixture>`. Prefix every `vl.py` command with `VIBE_LEDGER_HOME=<SCRATCH>/vl-home VIBE_LEDGER_OUT_DIR=<SCRATCH>/out`. Do not open anything under `tests/` in the vibe-ledger repo. Do not run `retention --set`. Finish with step 7 (`shot`) and report: the report path, the `check` summary lines, the `shot` layout-check line, and anything that confused you in SKILL.md or the guides.

When each agent finishes, score its run (the run folder is the one `start` printed):
```bash
python3 tests/e2e/score.py --verified <run>/ledger.verified.json --answers tests/fixtures/answers/<name>.json \
    --graph <run>/graph.json --explained <run>/explain.verified.json
```
Expected: every line `PASS` for all five fixtures. A `FAIL` on the graph lines is a `graph.py` defect (Step 7 of Task 7 explains how to tell). A `FAIL` on the explanation lines is either a guide that misled the agent (fix `references/explain-guide.md` or `SKILL.md`, quoting what confused the agent) or a verifier that rejected a correct explanation (fix `explain.py` with a failing test first). Re-run only the fixtures that failed, each with a new fresh agent.

- [ ] **Step 7: Look at the screenshots**

For two fixtures (notes-supabase, habits-firebase) open every PNG in `<run>/shots/` with the Read tool: `desktop.png`, `desktop-dark.png`, `selected.png`, `phone-390.png`, `overview.png`. Check each against this list and fix what fails (CSS/JS fixes need a re-render and a re-shot; a layout defect gets a failing test in `tests/test_graph_render.py` first):
- cards are coloured by type with their icon; entry cards in the left band, outside services in the right column;
- arrows run from caller to callee and none passes through a card it does not connect to;
- the selected card is purple, its neighbours stay sharp, the rest is faded;
- the panel shows purpose, calls / called by, main functions, risks and history (or the "no conversations" note) with no text cut off;
- the dark screenshot has readable contrast on cards, labels, arrows and the panel;
- the phone view stacks the graph above the panel with nothing running off the edge;
- the overview shows the v0.1 sections, unchanged.

- [ ] **Step 8: Re-run the real project for the user**

The v0.1 trial ran on a real Chrome-extension project of the user's (its run.json records that `project_root`; the user approved that trial). Its conversations have aged out, so the ledger is code-only. Run the skill on it yourself, following SKILL.md: `start`, `ledger.json` with empty `promises` plus `map`/`access`/`paths`, `explain.json` for every file `explain_pack.md` lists (in Chinese, `lang` is `zh`), `check`, `render`, `shot`. Open all five screenshots as in Step 7. The report lands on the Desktop. Then ask the user with AskUserQuestion, giving them the report path:

- question: "新版报告（文件流程图 + 点击看讲解）现在能看懂这个项目了吗？"
- options: "看懂了，主要靠图" / "图有用，但讲解还不够清楚" / "图还是看不懂" / "想换个方式"

If the answer is anything but the first option, ask what was unclear and fix it before calling v0.2 done (spec §9.4).

- [ ] **Step 9: Run the whole suite**

Run: `python3 -m pytest -q`
Expected: PASS, no failures. Commit any fixes from Steps 6–8 with their tests, staging each path by name. Nothing is pushed.
